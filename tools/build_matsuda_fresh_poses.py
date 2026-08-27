#!/usr/bin/env python3
"""Build Matsuda's fresh alternate poses from the five magenta masters.

This is intentionally independent of every earlier Matsuda pose pipeline.  It
reads only the explicitly allow-listed fresh masters plus the two canonical
neutral bases used for scale and color QA.  Runtime assets are written to the
fresh rebuild staging tree; nothing under ``game/`` is modified.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "tmp" / "matsuda_rebuild_fresh" / "masters" / "poses"
OUTPUT_DIR = ROOT / "tmp" / "matsuda_rebuild_fresh" / "poses"
CANONICAL_DIR = ROOT / "game" / "assets" / "characters" / "matsuda"

CANVAS_SIZE = (1023, 1537)
TARGET_TOP = 32
TARGET_BOTTOM = 1537  # Pillow-style exclusive lower bound.


@dataclass(frozen=True)
class PoseSpec:
    source: str
    output: str
    outfit: str
    canonical: str


POSES = (
    PoseSpec(
        "pose_chuuni_uniform_magenta.png",
        "pose_chuuni_uniform.png",
        "uniform",
        "neut_uniform.png",
    ),
    PoseSpec(
        "pose_facepalm_uniform_magenta.png",
        "pose_facepalm_uniform.png",
        "uniform",
        "neut_uniform.png",
    ),
    PoseSpec(
        "pose_laughing_casual_magenta.png",
        "pose_laughing_casual.png",
        "casual",
        "neutral.png",
    ),
    PoseSpec(
        "pose_laughing_uniform_magenta.png",
        "pose_laughing_uniform.png",
        "uniform",
        "neut_uniform.png",
    ),
    PoseSpec(
        "pose_shrug_uniform_magenta.png",
        "pose_shrug_uniform.png",
        "uniform",
        "neut_uniform.png",
    ),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_inputs() -> None:
    expected = {spec.source for spec in POSES}
    present = {path.name for path in SOURCE_DIR.glob("*_magenta.png")}
    if present != expected:
        missing = sorted(expected - present)
        unexpected = sorted(present - expected)
        raise RuntimeError(
            "Fresh-pose source allowlist mismatch: "
            f"missing={missing or 'none'}, unexpected={unexpected or 'none'}"
        )

    for spec in POSES:
        source_path = SOURCE_DIR / spec.source
        with Image.open(source_path) as image:
            if image.size != CANVAS_SIZE:
                raise ValueError(
                    f"{source_path.name}: expected {CANVAS_SIZE}, got {image.size}"
                )
            if image.mode not in {"RGB", "RGBA"}:
                raise ValueError(f"{source_path.name}: unsupported mode {image.mode}")

    for canonical_name in {spec.canonical for spec in POSES}:
        canonical_path = CANONICAL_DIR / canonical_name
        with Image.open(canonical_path) as image:
            if image.size != CANVAS_SIZE or image.mode != "RGBA":
                raise ValueError(
                    f"{canonical_path.name}: canonical must be RGBA {CANVAS_SIZE}; "
                    f"got {image.mode} {image.size}"
                )


def bbox_for_mask(mask: np.ndarray) -> list[int] | None:
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]


def component_details(alpha: np.ndarray, threshold: int) -> dict[str, Any]:
    mask = alpha >= threshold
    labels, count = ndi.label(mask, structure=np.ones((3, 3), dtype=np.uint8))
    if count == 0:
        return {"threshold": threshold, "count": 0, "components": []}

    sizes = np.bincount(labels.ravel())[1:]
    order = np.argsort(sizes)[::-1]
    components: list[dict[str, Any]] = []
    for index in order[:16]:
        label = int(index) + 1
        component_mask = labels == label
        components.append(
            {
                "pixels": int(sizes[index]),
                "bbox_xyxy_exclusive": bbox_for_mask(component_mask),
            }
        )
    return {
        "threshold": threshold,
        "count": int(count),
        "components": components,
    }


def retain_subject_components(seed: np.ndarray) -> tuple[np.ndarray, dict[str, int]]:
    """Keep the subject and nearby legitimate detached details, not key noise."""

    labels, count = ndi.label(seed, structure=np.ones((3, 3), dtype=np.uint8))
    if count == 0:
        raise RuntimeError("Chroma key did not find a foreground subject")

    sizes = np.bincount(labels.ravel())
    main_label = int(np.argmax(sizes[1:])) + 1
    main = labels == main_label
    distance_from_main = ndi.distance_transform_edt(~main)
    keep = main.copy()
    kept_components = 1
    removed_components = 0
    removed_pixels = 0

    for label in range(1, count + 1):
        if label == main_label:
            continue
        component = labels == label
        area = int(sizes[label])
        gap = float(distance_from_main[component].min())
        # Earrings and fine hair details can be detached by a few transparent
        # pixels.  Distant islands are background texture, irrespective of size.
        if area >= 2 and gap <= 18.0:
            keep |= component
            kept_components += 1
        else:
            removed_components += 1
            removed_pixels += area

    return keep, {
        "seed_components_total": int(count),
        "seed_components_kept": kept_components,
        "seed_components_removed": removed_components,
        "seed_pixels_removed": removed_pixels,
    }


def chroma_key(source: Image.Image) -> tuple[Image.Image, dict[str, Any]]:
    rgb_u8 = np.asarray(source.convert("RGB"), dtype=np.uint8)
    rgb = rgb_u8.astype(np.float32)
    red, green, blue = (rgb[:, :, channel] for channel in range(3))

    # A magenta screen has both red and blue above green.  Discounting red/blue
    # imbalance protects Matsuda's red hair while retaining a smooth key value
    # for neutral/white antialiasing at the silhouette.
    magenta_excess = np.minimum(red, blue) - green
    key_score = magenta_excess - 0.18 * np.abs(red - blue)

    top_sample = rgb[:24]
    top_score = key_score[:24]
    top_magenta = (
        (top_sample[:, :, 0] >= 160)
        & (top_sample[:, :, 2] >= 160)
        & (top_sample[:, :, 1] <= 120)
    )
    if not np.any(top_magenta):
        raise RuntimeError("Top-of-canvas background is not saturated magenta")

    sampled_scores = top_score[top_magenta]
    background_score = float(np.median(sampled_scores))
    background_core_threshold = float(np.percentile(sampled_scores, 2.0) - 2.0)
    foreground_core_threshold = min(24.0, background_score - 180.0)
    support_threshold = background_score - 48.0

    support_seed = key_score <= support_threshold
    retained_seed, cleanup = retain_subject_components(support_seed)

    # Eroding the chroma-derived subject support yields a color-safe interior
    # even where naturally red hair has a mildly positive magenta score.  It
    # also avoids declaring a blended outer pixel opaque merely because the
    # foreground itself is red.
    foreground_core = ndi.binary_erosion(
        retained_seed,
        structure=np.ones((3, 3), dtype=np.uint8),
        iterations=2,
        border_value=0,
    )
    if not np.any(foreground_core):
        raise RuntimeError("Chroma key did not find an opaque foreground core")

    background_core = (
        (key_score >= background_core_threshold)
        & (red >= 160.0)
        & (blue >= 160.0)
        & (green <= 120.0)
    )
    if not np.any(background_core):
        raise RuntimeError("Chroma key did not find an opaque background core")

    distance_from_subject = ndi.distance_transform_edt(~retained_seed)
    candidate = distance_from_subject <= 5.0

    # For fringe pixels, solve C = alpha*F + (1-alpha)*B using the nearest
    # confidently foreground/background colors.  This is substantially cleaner
    # than retaining a purple screen blend in RGB and merely lowering alpha.
    _, foreground_indices = ndi.distance_transform_edt(
        ~foreground_core, return_indices=True
    )
    _, background_indices = ndi.distance_transform_edt(
        ~background_core, return_indices=True
    )

    ys, xs = np.nonzero(candidate)
    observed = rgb[ys, xs]
    foreground = rgb[
        foreground_indices[0, ys, xs], foreground_indices[1, ys, xs]
    ]
    background = rgb[
        background_indices[0, ys, xs], background_indices[1, ys, xs]
    ]
    foreground_delta = foreground - background
    denominator = np.einsum("ij,ij->i", foreground_delta, foreground_delta)
    numerator = np.einsum("ij,ij->i", observed - background, foreground_delta)
    solved_alpha = np.divide(
        numerator,
        denominator,
        out=np.zeros_like(numerator),
        where=denominator > 16.0,
    )
    solved_alpha = np.clip(solved_alpha, 0.0, 1.0)

    score_alpha = np.clip(
        (background_score - key_score[ys, xs])
        / max(background_score - foreground_core_threshold, 1.0),
        0.0,
        1.0,
    )
    weak_solution = denominator <= 16.0
    solved_alpha[weak_solution] = score_alpha[weak_solution]
    # A mismatched nearest color must never make a visibly key-colored fringe
    # more opaque than the direct chroma evidence permits.
    solved_alpha = np.minimum(solved_alpha, np.clip(score_alpha * 1.04, 0.0, 1.0))

    alpha = np.zeros(key_score.shape, dtype=np.float32)
    alpha[ys, xs] = solved_alpha
    alpha[foreground_core] = 1.0
    alpha[alpha < 0.04] = 0.0
    alpha[alpha > 0.96] = 1.0

    # A second component pass removes any tiny islands introduced by the soft
    # solve while retaining small details close to the main silhouette.
    soft_seed = alpha > 0.0
    retained_soft, soft_cleanup = retain_subject_components(soft_seed)
    alpha[~retained_soft] = 0.0

    corrected = np.zeros_like(rgb, dtype=np.float32)
    visible_y, visible_x = np.nonzero(alpha > 0.0)
    visible_alpha = alpha[visible_y, visible_x]
    observed = rgb[visible_y, visible_x]
    foreground = rgb[
        foreground_indices[0, visible_y, visible_x],
        foreground_indices[1, visible_y, visible_x],
    ]
    background = rgb[
        background_indices[0, visible_y, visible_x],
        background_indices[1, visible_y, visible_x],
    ]

    # The nearest eroded subject color is a clean decontamination color for the
    # entire partial-alpha fringe.  Alpha still comes from the local F/B solve;
    # carrying the solved RGB itself would reintroduce tiny magenta/cyan ringing
    # when the normalized sprite is resampled.
    edge_color = foreground.copy()
    opaque = visible_alpha >= 0.995
    edge_color[opaque] = observed[opaque]

    # Final edge-only despill.  It cannot alter opaque art, but removes any
    # residual red+blue excess left by local background variation.
    edge_red = edge_color[:, 0]
    edge_green = edge_color[:, 1]
    edge_blue = edge_color[:, 2]
    spill = np.maximum(0.0, np.minimum(edge_red, edge_blue) - edge_green - 10.0)
    spill_weight = np.where(opaque, 0.0, 1.0)
    spill *= spill_weight
    edge_color[:, 0] -= spill
    edge_color[:, 2] -= spill
    corrected[visible_y, visible_x] = np.clip(edge_color, 0.0, 255.0)

    rgba = np.zeros((*alpha.shape, 4), dtype=np.uint8)
    rgba[:, :, :3] = np.rint(corrected).astype(np.uint8)
    rgba[:, :, 3] = np.rint(alpha * 255.0).astype(np.uint8)
    rgba[rgba[:, :, 3] == 0, :3] = 0

    diagnostics = {
        "background_key": {
            "score_median": round(background_score, 4),
            "background_core_threshold": round(background_core_threshold, 4),
            "foreground_core_threshold": round(foreground_core_threshold, 4),
            "support_threshold": round(support_threshold, 4),
            "sample_rgb_median": [
                round(float(value), 4)
                for value in np.median(top_sample[top_magenta], axis=0)
            ],
        },
        "component_cleanup": {**cleanup, **{f"soft_{k}": v for k, v in soft_cleanup.items()}},
    }
    return Image.fromarray(rgba, "RGBA"), diagnostics


def resize_rgba_premultiplied(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32) / 255.0
    alpha = rgba[:, :, 3:4]
    premultiplied = np.concatenate((rgba[:, :, :3] * alpha, alpha), axis=2)
    encoded = Image.fromarray(
        np.rint(np.clip(premultiplied, 0.0, 1.0) * 255.0).astype(np.uint8),
        "RGBA",
    )
    resized = np.asarray(
        encoded.resize(size, resample=Image.Resampling.BICUBIC), dtype=np.float32
    ) / 255.0
    resized_alpha = resized[:, :, 3:4]
    straight = np.zeros_like(resized)
    straight[:, :, 3:4] = resized_alpha
    np.divide(
        resized[:, :, :3],
        resized_alpha,
        out=straight[:, :, :3],
        where=resized_alpha > 0.0,
    )
    result = np.rint(np.clip(straight, 0.0, 1.0) * 255.0).astype(np.uint8)
    result[result[:, :, 3] == 0, :3] = 0
    return Image.fromarray(result, "RGBA")


def normalize_scale(image: Image.Image) -> tuple[Image.Image, dict[str, Any]]:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8)
    source_bbox = bbox_for_mask(rgba[:, :, 3] > 0)
    if source_bbox is None:
        raise RuntimeError("Cannot normalize an empty keyed image")

    x0, y0, x1, y1 = source_bbox
    source_width = x1 - x0
    source_height = y1 - y0
    desired_height = TARGET_BOTTOM - TARGET_TOP
    desired_scale = desired_height / source_height
    horizontal_scale_cap = (CANVAS_SIZE[0] - 2) / source_width
    applied_scale = min(desired_scale, horizontal_scale_cap)

    output_width = min(CANVAS_SIZE[0], max(1, round(source_width * applied_scale)))
    output_height = min(CANVAS_SIZE[1], max(1, round(source_height * applied_scale)))
    crop = image.crop((x0, y0, x1, y1))
    resized = resize_rgba_premultiplied(crop, (output_width, output_height))

    source_center_x = (x0 + x1) / 2.0
    transformed_center_x = (
        CANVAS_SIZE[0] / 2.0
        + (source_center_x - CANVAS_SIZE[0] / 2.0) * applied_scale
    )
    paste_x = round(transformed_center_x - output_width / 2.0)
    paste_x = max(0, min(CANVAS_SIZE[0] - output_width, paste_x))
    paste_y = TARGET_BOTTOM - output_height
    paste_y = max(0, min(CANVAS_SIZE[1] - output_height, paste_y))

    normalized = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    normalized.alpha_composite(resized, (paste_x, paste_y))
    normalized_array = np.asarray(normalized, dtype=np.uint8).copy()
    normalized_array[normalized_array[:, :, 3] == 0, :3] = 0
    normalized = Image.fromarray(normalized_array, "RGBA")

    output_bbox = bbox_for_mask(normalized_array[:, :, 3] > 0)
    return normalized, {
        "source_alpha_bbox_xyxy_exclusive": source_bbox,
        "target_vertical_span": [TARGET_TOP, TARGET_BOTTOM],
        "desired_uniform_scale": round(desired_scale, 8),
        "horizontal_scale_cap": round(horizontal_scale_cap, 8),
        "applied_uniform_scale": round(applied_scale, 8),
        "horizontal_cap_applied": bool(horizontal_scale_cap < desired_scale),
        "resized_subject_size": [output_width, output_height],
        "paste_xy": [paste_x, paste_y],
        "output_alpha_bbox_xyxy_exclusive": output_bbox,
    }


def remove_final_detached_noise(
    image: Image.Image, minimum_component_pixels: int = 64
) -> tuple[Image.Image, dict[str, Any]]:
    """Remove resampling islands after the sprite reaches its final canvas."""

    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    mask = rgba[:, :, 3] > 0
    labels, count = ndi.label(mask, structure=np.ones((3, 3), dtype=np.uint8))
    if count == 0:
        raise RuntimeError("Final normalized pose has no visible pixels")

    sizes = np.bincount(labels.ravel())
    main_label = int(np.argmax(sizes[1:])) + 1
    keep_labels = [
        label
        for label in range(1, count + 1)
        if label == main_label or int(sizes[label]) >= minimum_component_pixels
    ]
    keep = np.isin(labels, keep_labels)
    removed = mask & ~keep
    rgba[removed] = 0
    rgba[rgba[:, :, 3] == 0, :3] = 0
    return Image.fromarray(rgba, "RGBA"), {
        "minimum_component_pixels": minimum_component_pixels,
        "components_before": int(count),
        "components_after": len(keep_labels),
        "components_removed": int(count - len(keep_labels)),
        "pixels_removed": int(removed.sum()),
        "kept_component_pixel_counts": sorted(
            (int(sizes[label]) for label in keep_labels), reverse=True
        ),
    }


def clean_final_fringe(image: Image.Image) -> tuple[Image.Image, dict[str, Any]]:
    """Decontaminate resampled edge RGB and eliminate literal key-color traces."""

    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    alpha = rgba[:, :, 3]
    alpha[(alpha > 0) & (alpha < 3)] = 0
    alpha[alpha > 252] = 255
    rgba[:, :, 3] = alpha

    rgb_i16 = rgba[:, :, :3].astype(np.int16)
    red, green, blue = (rgb_i16[:, :, channel] for channel in range(3))
    excess = np.minimum(red, blue) - green
    screen_like_before = (
        (alpha > 3)
        & (red >= 180)
        & (blue >= 160)
        & (green <= 100)
        & (excess >= 100)
    )

    solid = alpha >= 250
    safe_solid = solid & ~screen_like_before
    if not np.any(safe_solid):
        raise RuntimeError("Final pose has no color-safe opaque core")
    _, safe_indices = ndi.distance_transform_edt(~safe_solid, return_indices=True)

    fringe = (alpha > 0) & (alpha < 250)
    fringe_y, fringe_x = np.nonzero(fringe)
    rgba[fringe_y, fringe_x, :3] = rgba[
        safe_indices[0, fringe_y, fringe_x],
        safe_indices[1, fringe_y, fringe_x],
        :3,
    ]

    # This strict second pass includes any fully opaque literal screen remnant.
    rgb_i16 = rgba[:, :, :3].astype(np.int16)
    red, green, blue = (rgb_i16[:, :, channel] for channel in range(3))
    excess = np.minimum(red, blue) - green
    screen_like_after_fringe = (
        (alpha > 3)
        & (red >= 180)
        & (blue >= 160)
        & (green <= 100)
        & (excess >= 100)
    )
    key_y, key_x = np.nonzero(screen_like_after_fringe)
    rgba[key_y, key_x, :3] = rgba[
        safe_indices[0, key_y, key_x], safe_indices[1, key_y, key_x], :3
    ]
    rgba[alpha == 0, :3] = 0
    return Image.fromarray(rgba, "RGBA"), {
        "partial_alpha_rgb_replaced_from_nearest_safe_core": int(fringe.sum()),
        "screen_like_pixels_before": int(screen_like_before.sum()),
        "screen_like_pixels_replaced_after_fringe": int(
            screen_like_after_fringe.sum()
        ),
    }


def visual_metrics(image: Image.Image) -> dict[str, Any]:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8)
    rgb = rgba[:, :, :3].astype(np.float32) / 255.0
    alpha = rgba[:, :, 3]
    weights = alpha.astype(np.float64) / 255.0
    visible = alpha > 0
    opaque = alpha >= 250
    total_weight = float(weights.sum())

    maximum = rgb.max(axis=2)
    minimum = rgb.min(axis=2)
    saturation = np.divide(
        maximum - minimum,
        maximum,
        out=np.zeros_like(maximum),
        where=maximum > 0.0,
    )
    brightness = (
        0.2126 * rgb[:, :, 0]
        + 0.7152 * rgb[:, :, 1]
        + 0.0722 * rgb[:, :, 2]
    )

    raw_rgb = rgba[:, :, :3].astype(np.int16)
    magenta_excess = (
        np.minimum(raw_rgb[:, :, 0], raw_rgb[:, :, 2]) - raw_rgb[:, :, 1]
    )
    # Match the runtime validator's deliberately conservative strong-magenta
    # screen-remnant definition.  The final fringe cleanup guarantees zero.
    key_colored = (
        (alpha > 3)
        & (raw_rgb[:, :, 0] >= 180)
        & (raw_rgb[:, :, 2] >= 160)
        & (raw_rgb[:, :, 1] <= 100)
        & (magenta_excess >= 100)
    )
    broad_magenta_hue = (
        visible
        & (raw_rgb[:, :, 0] >= 160)
        & (raw_rgb[:, :, 2] >= 160)
        & (raw_rgb[:, :, 1] <= 100)
        & (magenta_excess >= 80)
        & (np.abs(raw_rgb[:, :, 0] - raw_rgb[:, :, 2]) <= 28)
    )
    hidden_nonzero = (~visible) & np.any(rgba[:, :, :3] != 0, axis=2)

    return {
        "size": list(image.size),
        "mode": image.mode,
        "alpha_bbox_xyxy_exclusive": bbox_for_mask(visible),
        "opaque_bbox_xyxy_exclusive": bbox_for_mask(opaque),
        "alpha_pixels": int(visible.sum()),
        "opaque_pixels": int(opaque.sum()),
        "partial_alpha_pixels": int((visible & ~opaque).sum()),
        "alpha_weighted_saturation_mean": round(
            float((saturation * weights).sum() / total_weight), 6
        ),
        "alpha_weighted_brightness_mean": round(
            float((brightness * weights).sum() / total_weight), 6
        ),
        "magenta_residue_pixels": int(key_colored.sum()),
        "magenta_residue_fraction_of_visible": round(
            float(key_colored.sum() / max(int(visible.sum()), 1)), 10
        ),
        "broad_magenta_hue_pixels_diagnostic_only": int(
            broad_magenta_hue.sum()
        ),
        "zero_alpha_nonzero_rgb_pixels": int(hidden_nonzero.sum()),
        "components": {
            "alpha_ge_1": component_details(alpha, 1),
            "alpha_ge_128": component_details(alpha, 128),
            "alpha_ge_250": component_details(alpha, 250),
        },
    }


def comparison_metrics(
    pose_metrics: dict[str, Any], canonical_metrics: dict[str, Any]
) -> dict[str, Any]:
    saturation = pose_metrics["alpha_weighted_saturation_mean"]
    canonical_saturation = canonical_metrics["alpha_weighted_saturation_mean"]
    brightness = pose_metrics["alpha_weighted_brightness_mean"]
    canonical_brightness = canonical_metrics["alpha_weighted_brightness_mean"]
    return {
        "pose_saturation_mean": saturation,
        "canonical_saturation_mean": canonical_saturation,
        "saturation_delta": round(saturation - canonical_saturation, 6),
        "saturation_ratio": round(saturation / canonical_saturation, 6),
        "pose_brightness_mean": brightness,
        "canonical_brightness_mean": canonical_brightness,
        "brightness_delta": round(brightness - canonical_brightness, 6),
        "brightness_ratio": round(brightness / canonical_brightness, 6),
    }


def checkerboard(size: tuple[int, int], tile: int = 24) -> Image.Image:
    width, height = size
    yy, xx = np.indices((height, width))
    cells = ((xx // tile) + (yy // tile)) % 2
    light = np.array([232, 234, 239], dtype=np.uint8)
    dark = np.array([177, 182, 193], dtype=np.uint8)
    pixels = np.where(cells[:, :, None] == 0, light, dark)
    return Image.fromarray(pixels, "RGB").convert("RGBA")


def contact_sheet(
    poses: list[tuple[str, Image.Image]], background_kind: str
) -> Image.Image:
    columns = 3
    rows = math.ceil(len(poses) / columns)
    cell_width = 320
    preview_height = 465
    label_height = 34
    gutter = 12
    sheet_size = (
        columns * cell_width + (columns + 1) * gutter,
        rows * (preview_height + label_height) + (rows + 1) * gutter,
    )
    if background_kind == "light":
        sheet = Image.new("RGBA", sheet_size, (240, 242, 247, 255))
        text_color = (24, 27, 35, 255)
    elif background_kind == "dark":
        sheet = Image.new("RGBA", sheet_size, (24, 27, 35, 255))
        text_color = (238, 240, 245, 255)
    elif background_kind == "checker":
        sheet = checkerboard(sheet_size)
        text_color = (20, 23, 30, 255)
    else:
        raise ValueError(background_kind)

    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.load_default(size=16)
    except TypeError:  # Pillow versions before scalable built-in fonts.
        font = ImageFont.load_default()

    for index, (name, pose) in enumerate(poses):
        row, column = divmod(index, columns)
        cell_x = gutter + column * (cell_width + gutter)
        cell_y = gutter + row * (preview_height + label_height)
        preview = pose.copy()
        preview.thumbnail((cell_width, preview_height), Image.Resampling.LANCZOS)
        x = cell_x + (cell_width - preview.width) // 2
        y = cell_y + preview_height - preview.height
        sheet.alpha_composite(preview, (x, y))
        label = Path(name).stem
        label_box = draw.textbbox((0, 0), label, font=font)
        label_width = label_box[2] - label_box[0]
        draw.text(
            (cell_x + (cell_width - label_width) // 2, cell_y + preview_height + 7),
            label,
            fill=text_color,
            font=font,
        )
    return sheet.convert("RGB")


def main() -> None:
    validate_inputs()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    canonical_images: dict[str, Image.Image] = {}
    canonical_metrics: dict[str, dict[str, Any]] = {}
    canonical_provenance: dict[str, dict[str, str]] = {}
    for canonical_name in sorted({spec.canonical for spec in POSES}):
        path = CANONICAL_DIR / canonical_name
        with Image.open(path) as opened:
            image = opened.convert("RGBA")
        canonical_images[canonical_name] = image
        canonical_metrics[canonical_name] = visual_metrics(image)
        canonical_provenance[canonical_name] = {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha256(path),
            "usage": "scale/color QA only",
        }

    built: list[tuple[str, Image.Image]] = []
    pose_records: dict[str, Any] = {}
    for spec in POSES:
        source_path = SOURCE_DIR / spec.source
        output_path = OUTPUT_DIR / spec.output
        with Image.open(source_path) as opened:
            source = opened.convert("RGB")

        keyed, key_diagnostics = chroma_key(source)
        normalized, normalization = normalize_scale(keyed)
        normalized, fringe_cleanup = clean_final_fringe(normalized)
        normalized, final_cleanup = remove_final_detached_noise(normalized)
        metrics = visual_metrics(normalized)
        if metrics["size"] != list(CANVAS_SIZE):
            raise RuntimeError(f"{spec.output}: output canvas changed unexpectedly")
        if metrics["zero_alpha_nonzero_rgb_pixels"] != 0:
            raise RuntimeError(f"{spec.output}: nonzero RGB remained under zero alpha")

        normalized.save(output_path, format="PNG", optimize=True)
        built.append((spec.output, normalized))
        pose_records[spec.output] = {
            "source": {
                "path": source_path.relative_to(ROOT).as_posix(),
                "sha256": sha256(source_path),
                "size": list(source.size),
                "mode": source.mode,
            },
            "output": {
                "path": output_path.relative_to(ROOT).as_posix(),
                "sha256": sha256(output_path),
                "outfit": spec.outfit,
            },
            "canonical_match": spec.canonical,
            "chroma_key": key_diagnostics,
            "normalization": normalization,
            "final_fringe_cleanup": fringe_cleanup,
            "final_component_cleanup": final_cleanup,
            "metrics": metrics,
            "canonical_comparison": comparison_metrics(
                metrics, canonical_metrics[spec.canonical]
            ),
        }

    contact_records: dict[str, Any] = {}
    for background_kind in ("light", "dark", "checker"):
        filename = f"contact_sheet_{background_kind}.png"
        path = OUTPUT_DIR / filename
        sheet = contact_sheet(built, background_kind)
        sheet.save(path, format="PNG", optimize=True)
        contact_records[background_kind] = {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha256(path),
            "size": list(sheet.size),
            "mode": sheet.mode,
        }

    report = {
        "schema_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "processor": Path(__file__).relative_to(ROOT).as_posix(),
        "policy": {
            "source_allowlist": [spec.source for spec in POSES],
            "canonical_bases_are_qa_only": True,
            "runtime_assets_read": False,
            "previous_processors_read": False,
            "game_files_modified": False,
        },
        "canvas": {
            "size": list(CANVAS_SIZE),
            "canonical_vertical_span_xyxy_exclusive": [TARGET_TOP, TARGET_BOTTOM],
        },
        "canonical_bases": canonical_provenance,
        "canonical_metrics": canonical_metrics,
        "poses": pose_records,
        "contact_sheets": contact_records,
    }
    report_path = OUTPUT_DIR / "provenance_metrics.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"Built {len(built)} fresh Matsuda poses in {OUTPUT_DIR.relative_to(ROOT)}")
    for name, _ in built:
        record = pose_records[name]
        bbox = record["metrics"]["alpha_bbox_xyxy_exclusive"]
        residue = record["metrics"]["magenta_residue_pixels"]
        components = record["metrics"]["components"]["alpha_ge_1"]["count"]
        print(f"  {name}: bbox={bbox}, components={components}, magenta={residue}")
    print(f"  report: {report_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
