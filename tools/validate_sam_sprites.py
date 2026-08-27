#!/usr/bin/env python3
"""Validate and visually review Sam's fresh shared-face sprite bank.

The accepted bank is intentionally small and has no compatibility path for the
retired featureless-base/outfit-conditioned system:

* ``neutral.png`` and ``neut_uniform.png`` are intact 1023x1537 RGBA bases;
* ``face_neut.png`` is a fully transparent compatibility layer;
* the 20 ``face_<expression>.png`` alternates share one full-canvas alpha mask;
* the shared mask is feathered, stays inside both base silhouettes, and owns the
  registered face core; and
* four silhouette-changing poses remain standalone 1023x1537 RGBA sprites.

By default this validates the installed production folder and writes six visual
review sheets (expressions and poses on dark, light, and checker backgrounds).
Pass ``--sprite-dir`` and ``--review-dir`` to validate a pre-install staging
folder without touching production assets.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import sys
from collections import Counter
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_DIR = PROJECT_ROOT / "game" / "assets" / "characters" / "masayami"
DEFAULT_REVIEW_DIR = PROJECT_ROOT / "tmp" / "sam_sprite_review"

CANVAS_SIZE = (1023, 1537)
CANVAS_WIDTH, CANVAS_HEIGHT = CANVAS_SIZE

# A full-canvas layer is required, but its visible plate must remain confined to
# Sam's registered head. This catches accidental cropped placement, whole-body
# donors, and preview rectangles while leaving generous authoring tolerance.
FACE_SAFE_BOUNDS = (250, 100, 750, 600)
FACE_REVIEW_CROP = (260, 70, 740, 550)
CHECKER_PERIODICITY_LIMIT = 0.28
GRID_PERIODICITY_LIMIT = 0.55

EXPRESSIONS = (
    "happy",
    "smug",
    "teasing",
    "thinking",
    "curious",
    "unamused",
    "annoyed",
    "frustrated",
    "angry",
    "sad",
    "crying",
    "embarrassed",
    "nervous",
    "worried",
    "shocked",
    "afraid",
    "panicked",
    "determined",
    "empty",
    "disgusted",
)
ALL_EXPRESSIONS = ("neut",) + EXPRESSIONS


@dataclass(frozen=True)
class OutfitSpec:
    name: str
    filename: str


@dataclass(frozen=True)
class PoseSpec:
    token: str
    outfit: str
    filename: str


OUTFITS = (
    OutfitSpec("casual", "neutral.png"),
    OutfitSpec("uniform", "neut_uniform.png"),
)

POSES = (
    PoseSpec("open_hand", "casual", "pose_open_hand_casual.png"),
    PoseSpec("crossed", "uniform", "pose_crossed_uniform.png"),
    PoseSpec("thinking", "uniform", "pose_thinking_uniform.png"),
    PoseSpec("phone", "casual", "pose_phone_casual.png"),
)


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def check(self, condition: bool, message: str) -> bool:
        if not condition:
            self.errors.append(message)
        return condition

    def error(self, message: str) -> None:
        self.errors.append(message)

    def note(self, message: str) -> None:
        self.notes.append(message)


def expected_filenames() -> set[str]:
    names = {outfit.filename for outfit in OUTFITS}
    names.add("face_neut.png")
    names.update(f"face_{expression}.png" for expression in EXPRESSIONS)
    names.update(pose.filename for pose in POSES)
    return names


def mask_bbox(mask: np.ndarray) -> tuple[int, int, int, int] | None:
    rows, columns = np.nonzero(mask)
    if not len(columns):
        return None
    return (
        int(columns.min()),
        int(rows.min()),
        int(columns.max()) + 1,
        int(rows.max()) + 1,
    )


def format_bbox(bounds: tuple[int, int, int, int] | None) -> str:
    if bounds is None:
        return "empty"
    left, top, right, bottom = bounds
    return f"({left},{top})-({right},{bottom})"


def alpha_composite(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    return np.asarray(
        Image.alpha_composite(
            Image.fromarray(base, "RGBA"),
            Image.fromarray(overlay, "RGBA"),
        ),
        dtype=np.uint8,
    ).copy()


def connected_component_areas(mask: np.ndarray) -> list[int]:
    """Return 8-connected foreground component areas, largest first.

    Horizontal run labeling keeps full-canvas checks fast without requiring
    OpenCV or SciPy merely for sprite hygiene.
    """

    if mask.ndim != 2:
        raise ValueError(f"component mask must be 2D, got {mask.shape}")

    parents: list[int] = []
    run_areas: list[int] = []

    def find(label: int) -> int:
        root = label
        while parents[root] != root:
            root = parents[root]
        while parents[label] != label:
            parent = parents[label]
            parents[label] = root
            label = parent
        return root

    def union(first: int, second: int) -> None:
        first_root = find(first)
        second_root = find(second)
        if first_root != second_root:
            parents[second_root] = first_root

    previous_runs: list[tuple[int, int, int]] = []
    for row in np.asarray(mask, dtype=bool):
        padded = np.pad(row, (1, 1), constant_values=False)
        transitions = np.diff(padded.astype(np.int8))
        starts = np.flatnonzero(transitions == 1)
        stops = np.flatnonzero(transitions == -1)
        current_runs: list[tuple[int, int, int]] = []
        previous_index = 0

        for start_value, stop_value in zip(starts, stops, strict=True):
            start = int(start_value)
            end = int(stop_value) - 1
            label = len(parents)
            parents.append(label)
            run_areas.append(end - start + 1)

            while (
                previous_index < len(previous_runs)
                and previous_runs[previous_index][1] < start - 1
            ):
                previous_index += 1
            overlap_index = previous_index
            while (
                overlap_index < len(previous_runs)
                and previous_runs[overlap_index][0] <= end + 1
            ):
                union(label, previous_runs[overlap_index][2])
                overlap_index += 1
            current_runs.append((start, end, label))

        previous_runs = current_runs

    totals: Counter[int] = Counter()
    for label, area in enumerate(run_areas):
        totals[find(label)] += area
    return sorted(totals.values(), reverse=True)


def shifted_correlation(
    values: np.ndarray,
    support: np.ndarray,
    dy: int,
    dx: int,
) -> float | None:
    height, width = support.shape
    if abs(dy) >= height or abs(dx) >= width:
        return None

    first_y = slice(0, height - dy) if dy >= 0 else slice(-dy, height)
    second_y = slice(dy, height) if dy >= 0 else slice(0, height + dy)
    first_x = slice(0, width - dx) if dx >= 0 else slice(-dx, width)
    second_x = slice(dx, width) if dx >= 0 else slice(0, width + dx)

    valid = support[first_y, first_x] & support[second_y, second_x]
    if int(valid.sum()) < 500:
        return None

    first = values[first_y, first_x][valid].astype(np.float64)
    second = values[second_y, second_x][valid].astype(np.float64)
    first -= first.mean()
    second -= second.mean()
    denominator = math.sqrt(float(np.dot(first, first) * np.dot(second, second)))
    if denominator <= 1e-9:
        return None
    return float(np.dot(first, second) / denominator)


def checker_grid_periodicity_scores(
    composite: np.ndarray,
    base: np.ndarray,
    support: np.ndarray,
) -> tuple[float, int | None, float, int | None]:
    """Measure baked checker alternation and repeating two-axis grid lines."""

    bounds = mask_bbox(support)
    if bounds is None or int(support.sum()) < 2_000:
        return 0.0, None, 0.0, None
    left, top, right, bottom = bounds
    local_support = support[top:bottom, left:right]
    weights = np.asarray((0.2126, 0.7152, 0.0722), dtype=np.float32)
    difference = (
        composite[top:bottom, left:right, :3].astype(np.float32)
        - base[top:bottom, left:right, :3].astype(np.float32)
    ) @ weights
    if float(difference[local_support].std()) < 0.35:
        return 0.0, None, 0.0, None

    padded = np.pad(difference, 1, mode="edge")
    smooth = (
        sum(
            padded[y : y + difference.shape[0], x : x + difference.shape[1]]
            for y in range(3)
            for x in range(3)
        )
        / 9.0
    )
    high_pass = difference - smooth
    high_pass_has_signal = float(high_pass[local_support].std()) >= 0.35

    best_checker = 0.0
    checker_tile: int | None = None
    best_grid = 0.0
    grid_tile: int | None = None
    for tile in range(3, 33):
        raw_correlations = (
            shifted_correlation(difference, local_support, 0, tile),
            shifted_correlation(difference, local_support, tile, 0),
            shifted_correlation(difference, local_support, 0, tile * 2),
            shifted_correlation(difference, local_support, tile * 2, 0),
        )
        if all(value is not None for value in raw_correlations):
            horizontal_flip, vertical_flip, horizontal_repeat, vertical_repeat = (
                float(value) for value in raw_correlations
            )
            checker_score = min(
                -horizontal_flip,
                -vertical_flip,
                horizontal_repeat,
                vertical_repeat,
            )
            if checker_score > best_checker:
                best_checker = checker_score
                checker_tile = tile

        if high_pass_has_signal:
            grid_correlations = (
                shifted_correlation(high_pass, local_support, 0, tile),
                shifted_correlation(high_pass, local_support, tile, 0),
            )
            if all(value is not None for value in grid_correlations):
                grid_score = min(float(value) for value in grid_correlations)
                if grid_score > best_grid:
                    best_grid = grid_score
                    grid_tile = tile

    return (
        max(0.0, best_checker),
        checker_tile,
        max(0.0, best_grid),
        grid_tile,
    )


@lru_cache(maxsize=None)
def neutral_feature_core() -> np.ndarray:
    """Return conservative brow/eye/mouth cores the face plate must own."""

    # These are intentionally smaller than the authored features. Requiring a
    # fully opaque center prevents the old neutral eyes/mouth from ghosting
    # through while leaving the plate's outer skin/hair feather unconstrained.
    ellipses = (
        (426.0, 269.0, 28.0, 6.0),
        (535.0, 250.0, 32.0, 6.0),
        (427.0, 305.0, 40.0, 18.0),
        (539.0, 285.0, 40.0, 18.0),
        (498.0, 378.0, 38.0, 12.0),
    )
    y_grid, x_grid = np.ogrid[:CANVAS_HEIGHT, :CANVAS_WIDTH]
    result = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH), dtype=bool)
    for center_x, center_y, radius_x, radius_y in ellipses:
        result |= ((x_grid - center_x) / radius_x) ** 2 + (
            (y_grid - center_y) / radius_y
        ) ** 2 <= 1.0
    return result


def load_bank(sprite_dir: Path, report: ValidationReport) -> dict[str, np.ndarray]:
    required = expected_filenames()
    present = {path.name: path for path in sprite_dir.glob("*.png") if path.is_file()}

    missing = sorted(required - set(present))
    unexpected = sorted(set(present) - required)
    if missing:
        report.error(
            f"{sprite_dir}: missing {len(missing)} required PNG(s):\n"
            + "\n".join(f"  - {name}" for name in missing)
        )
    if unexpected:
        report.error(
            f"{sprite_dir}: unexpected PNG(s) violate the fresh 27-file contract "
            "(remove obsolete outfit-conditioned/base aliases):\n"
            + "\n".join(f"  - {name}" for name in unexpected)
        )

    images: dict[str, np.ndarray] = {}
    for name in sorted(required & set(present)):
        path = present[name]
        try:
            with Image.open(path) as image:
                report.check(
                    image.format == "PNG",
                    f"{path}: format is {image.format!r}, expected PNG",
                )
                valid_size = report.check(
                    image.size == CANVAS_SIZE,
                    f"{path}: canvas is {image.size}, expected {CANVAS_SIZE}",
                )
                valid_mode = report.check(
                    image.mode == "RGBA",
                    f"{path}: stored mode is {image.mode!r}, expected RGBA",
                )
                pixels = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
        except (OSError, ValueError) as exc:
            report.error(f"{path}: cannot decode PNG: {exc}")
            continue

        if not (valid_size and valid_mode):
            continue
        alpha = pixels[:, :, 3]
        hidden_rgb = (alpha == 0) & np.any(pixels[:, :, :3] != 0, axis=2)
        report.check(
            not np.any(hidden_rgb),
            f"{path}: {int(hidden_rgb.sum())} zero-alpha pixels retain RGB data",
        )
        images[name] = pixels

    return images


def validate_subject_canvas(
    label: str,
    pixels: np.ndarray,
    report: ValidationReport,
    *,
    require_bottom_contact: bool,
) -> None:
    alpha = pixels[:, :, 3]
    visible = alpha > 0
    bounds = mask_bbox(visible)
    if not report.check(bounds is not None, f"{label}: alpha silhouette is empty"):
        return
    assert bounds is not None
    left, top, right, bottom = bounds
    report.check(
        left > 0 and top > 0 and right < CANVAS_WIDTH,
        f"{label}: silhouette touches a forbidden canvas edge; bbox={format_bbox(bounds)}",
    )
    if require_bottom_contact:
        report.check(
            bottom == CANVAS_HEIGHT,
            f"{label}: stage baseline drift; expected bottom={CANVAS_HEIGHT}, got {bottom}",
        )
    report.check(
        bool(np.any(alpha == 255)),
        f"{label}: silhouette has no opaque interior",
    )
    report.check(
        bool(np.any((alpha > 0) & (alpha < 255))),
        f"{label}: silhouette has no antialiased/soft edge pixels",
    )

    areas = connected_component_areas(visible)
    total = int(visible.sum())
    dominant = areas[0] if areas else 0
    detached = total - dominant
    largest_detached = areas[1] if len(areas) > 1 else 0
    report.check(
        dominant / max(1, total) >= 0.999,
        f"{label}: fragmented silhouette; dominant={dominant}/{total}, detached={detached}",
    )
    report.check(
        detached <= 512 and largest_detached <= 64,
        f"{label}: detached alpha debris is too large; total={detached}, "
        f"largest={largest_detached}",
    )
    report.note(
        f"{label}: bbox={format_bbox(bounds)} visible={total} "
        f"components={len(areas)} detached={detached} alpha-levels={len(np.unique(alpha))}"
    )


def validate_bases(
    images: dict[str, np.ndarray], report: ValidationReport
) -> dict[str, np.ndarray]:
    bases: dict[str, np.ndarray] = {}
    for outfit in OUTFITS:
        pixels = images.get(outfit.filename)
        if pixels is None:
            continue
        bases[outfit.name] = pixels
        validate_subject_canvas(
            f"sam/{outfit.name}/base",
            pixels,
            report,
            require_bottom_contact=True,
        )
    return bases


def validate_faces(
    images: dict[str, np.ndarray],
    bases: dict[str, np.ndarray],
    report: ValidationReport,
) -> bool:
    neutral = images.get("face_neut.png")
    if neutral is not None:
        report.check(
            not np.any(neutral),
            "sam/face_neut.png: neutral compatibility layer must be zero RGBA",
        )

    layers: list[tuple[str, np.ndarray]] = []
    for expression in EXPRESSIONS:
        layer = images.get(f"face_{expression}.png")
        if layer is not None:
            layers.append((expression, layer))
    if len(layers) != len(EXPRESSIONS):
        return False

    canonical_alpha = layers[0][1][:, :, 3]
    bounds = mask_bbox(canonical_alpha > 0)
    if not report.check(bounds is not None, "sam/shared-face-mask: mask is empty"):
        return False
    assert bounds is not None
    left, top, right, bottom = bounds
    safe_left, safe_top, safe_right, safe_bottom = FACE_SAFE_BOUNDS
    report.check(
        left >= safe_left
        and top >= safe_top
        and right <= safe_right
        and bottom <= safe_bottom,
        f"sam/shared-face-mask: bbox={format_bbox(bounds)} escapes safe head bounds "
        f"{format_bbox(FACE_SAFE_BOUNDS)}",
    )
    visible = canonical_alpha > 0
    opaque = canonical_alpha == 255
    partial = visible & ~opaque
    levels = len(np.unique(canonical_alpha))
    report.check(
        10_000 <= int(visible.sum()) <= 200_000,
        f"sam/shared-face-mask: implausible visible area {int(visible.sum())}",
    )
    report.check(
        bool(np.any(opaque)) and bool(np.any(partial)) and levels >= 32,
        f"sam/shared-face-mask: expected opaque core plus feathered edge; "
        f"opaque={int(opaque.sum())}, partial={int(partial.sum())}, levels={levels}",
    )
    uncovered_core = neutral_feature_core() & ~opaque
    report.check(
        not np.any(uncovered_core),
        f"sam/shared-face-mask: {int(uncovered_core.sum())} registered neutral-feature "
        "core pixels are not fully owned; duplicate eyes/brows/mouth can leak through",
    )

    areas = connected_component_areas(visible)
    detached = int(visible.sum()) - (areas[0] if areas else 0)
    report.check(
        detached <= 8,
        f"sam/shared-face-mask: detached mask debris totals {detached} pixels",
    )

    alpha_digest = hashlib.sha256(canonical_alpha.tobytes()).hexdigest()
    layer_digests: dict[str, str] = {}
    for expression, layer in layers:
        alpha = layer[:, :, 3]
        report.check(
            np.array_equal(alpha, canonical_alpha),
            f"sam/face_{expression}.png: alpha mask differs from the shared mask",
        )
        layer_digests[expression] = hashlib.sha256(layer.tobytes()).hexdigest()
    digest_groups: dict[str, list[str]] = {}
    for expression, digest in layer_digests.items():
        digest_groups.setdefault(digest, []).append(expression)
    duplicates = [group for group in digest_groups.values() if len(group) > 1]
    report.check(
        not duplicates,
        "sam/faces: duplicate expression layer(s): "
        + "; ".join(", ".join(group) for group in duplicates),
    )

    for outfit, base in bases.items():
        outside = visible & (base[:, :, 3] == 0)
        report.check(
            not np.any(outside),
            f"sam/{outfit}/shared-face-mask: {int(outside.sum())} pixels extend "
            "outside the base silhouette",
        )

    if all(outfit.name in bases for outfit in OUTFITS):
        casual = bases["casual"]
        uniform = bases["uniform"]
        core_mismatch = opaque & np.any(casual[:, :, :3] != uniform[:, :, :3], axis=2)
        report.check(
            not np.any(core_mismatch),
            f"sam/shared-face-core: {int(core_mismatch.sum())} opaque-core pixels differ "
            "between neutral.png and neut_uniform.png; heads are not registered",
        )

    checker_metrics: list[tuple[float, str, str, int | None]] = []
    grid_metrics: list[tuple[float, str, str, int | None]] = []
    for outfit, base in bases.items():
        composite_digests: dict[str, str] = {}
        changed_counts: list[int] = []
        for expression, layer in layers:
            composite = alpha_composite(base, layer)
            changed = np.any(composite[:, :, :3] != base[:, :, :3], axis=2)
            changed_count = int(changed.sum())
            changed_counts.append(changed_count)
            report.check(
                changed_count >= 1_000,
                f"sam/{outfit}/{expression}: composite is effectively neutral "
                f"({changed_count} changed pixels)",
            )
            composite_digests[expression] = hashlib.sha256(
                composite.tobytes()
            ).hexdigest()
            checker, checker_tile, grid, grid_tile = checker_grid_periodicity_scores(
                composite,
                base,
                opaque,
            )
            report.check(
                checker < CHECKER_PERIODICITY_LIMIT,
                f"sam/{outfit}/{expression}: checker-like residue detected "
                f"(score={checker:.3f}, tile={checker_tile}px)",
            )
            report.check(
                grid < GRID_PERIODICITY_LIMIT,
                f"sam/{outfit}/{expression}: repeating grid residue detected "
                f"(score={grid:.3f}, tile={grid_tile}px)",
            )
            checker_metrics.append((checker, outfit, expression, checker_tile))
            grid_metrics.append((grid, outfit, expression, grid_tile))

        composite_groups: dict[str, list[str]] = {}
        for expression, digest in composite_digests.items():
            composite_groups.setdefault(digest, []).append(expression)
        duplicate_composites = [
            group for group in composite_groups.values() if len(group) > 1
        ]
        report.check(
            not duplicate_composites,
            f"sam/{outfit}: duplicate expression composite(s): "
            + "; ".join(", ".join(group) for group in duplicate_composites),
        )
        if changed_counts:
            report.note(
                f"sam/{outfit}/faces: distinct={len(composite_groups)}/20 "
                f"changed-range={min(changed_counts)}-{max(changed_counts)}"
            )

    strongest_checker = max(checker_metrics, default=(0.0, "none", "none", None))
    strongest_grid = max(grid_metrics, default=(0.0, "none", "none", None))
    report.note(
        f"sam/shared-face-mask: sha256={alpha_digest[:12]} "
        f"bbox={format_bbox(bounds)} visible={int(visible.sum())} "
        f"opaque={int(opaque.sum())} partial={int(partial.sum())} levels={levels} "
        f"checker-max={strongest_checker[0]:.3f}/"
        f"{strongest_checker[1]}-{strongest_checker[2]}@{strongest_checker[3]}px "
        f"grid-max={strongest_grid[0]:.3f}/"
        f"{strongest_grid[1]}-{strongest_grid[2]}@{strongest_grid[3]}px"
    )
    return True


def validate_poses(images: dict[str, np.ndarray], report: ValidationReport) -> bool:
    complete = True
    for pose in POSES:
        pixels = images.get(pose.filename)
        if pixels is None:
            complete = False
            continue
        validate_subject_canvas(
            f"sam/{pose.outfit}/pose_{pose.token}",
            pixels,
            report,
            require_bottom_contact=True,
        )
        alpha = pixels[:, :, 3]
        visible = alpha > 0
        red, green, blue = [
            pixels[:, :, channel].astype(np.int16) for channel in range(3)
        ]
        dominant_green = (
            visible & (green - red > 10) & (green - blue > 10) & (green > 80)
        )
        dominant_magenta = (
            visible
            & (red - green > 30)
            & (blue - green > 20)
            & (
                np.maximum.reduce((red, green, blue))
                - np.minimum.reduce((red, green, blue))
                > 55
            )
            & (red > 130)
            & (blue > 100)
        )
        report.check(
            not np.any(dominant_green),
            f"sam/{pose.outfit}/pose_{pose.token}: "
            f"{int(dominant_green.sum())} visible chroma-green residue pixels",
        )
        report.check(
            not np.any(dominant_magenta),
            f"sam/{pose.outfit}/pose_{pose.token}: "
            f"{int(dominant_magenta.sum())} visible magenta residue pixels",
        )
        report.note(
            f"sam/{pose.outfit}/pose_{pose.token}: chroma-residue green="
            f"{int(dominant_green.sum())} magenta={int(dominant_magenta.sum())}"
        )
    return complete


@lru_cache(maxsize=None)
def load_font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # Pillow < 10.
        return ImageFont.load_default()


def make_background(kind: str, size: tuple[int, int]) -> Image.Image:
    if kind == "dark":
        return Image.new("RGBA", size, (22, 24, 31, 255))
    if kind == "light":
        return Image.new("RGBA", size, (240, 241, 244, 255))
    if kind != "checker":
        raise ValueError(f"unknown review background {kind!r}")

    image = Image.new("RGBA", size, (210, 212, 218, 255))
    draw = ImageDraw.Draw(image)
    tile = 16
    for top in range(0, size[1], tile):
        for left in range(0, size[0], tile):
            if (left // tile + top // tile) % 2:
                draw.rectangle(
                    (left, top, left + tile - 1, top + tile - 1),
                    fill=(164, 168, 177, 255),
                )
    return image


def contained_copy(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    result = image.copy()
    result.thumbnail(size, Image.Resampling.LANCZOS)
    return result


def expression_panel(
    sprite: Image.Image,
    background_kind: str,
    label: str,
) -> Image.Image:
    width, height = (240, 340)
    footer_height = 30
    art_height = height - footer_height
    panel = make_background(background_kind, (width, height))

    full = contained_copy(sprite, (222, art_height - 8))
    panel.alpha_composite(full, ((width - full.width) // 2, art_height - full.height))

    head = contained_copy(sprite.crop(FACE_REVIEW_CROP), (108, 108))
    inset = make_background(background_kind, (114, 114))
    inset.alpha_composite(head, ((114 - head.width) // 2, (114 - head.height) // 2))
    inset_draw = ImageDraw.Draw(inset)
    inset_draw.rectangle((0, 0, 113, 113), outline=(69, 205, 224, 255), width=2)
    panel.alpha_composite(inset, (width - 120, 6))

    draw = ImageDraw.Draw(panel)
    draw.rectangle((0, art_height, width - 1, height - 1), fill=(14, 16, 22, 245))
    draw.text(
        (width // 2, art_height + footer_height // 2),
        label,
        font=load_font(14),
        fill=(242, 245, 250, 255),
        anchor="mm",
    )
    draw.rectangle((0, 0, width - 1, height - 1), outline=(76, 81, 92, 255))
    return panel


def pose_panel(
    sprite: Image.Image,
    background_kind: str,
    label: str,
) -> Image.Image:
    width, height = (300, 440)
    footer_height = 34
    art_height = height - footer_height
    panel = make_background(background_kind, (width, height))
    full = contained_copy(sprite, (282, art_height - 10))
    panel.alpha_composite(full, ((width - full.width) // 2, art_height - full.height))
    draw = ImageDraw.Draw(panel)
    draw.rectangle((0, art_height, width - 1, height - 1), fill=(14, 16, 22, 245))
    draw.text(
        (width // 2, art_height + footer_height // 2),
        label,
        font=load_font(15),
        fill=(242, 245, 250, 255),
        anchor="mm",
    )
    draw.rectangle((0, 0, width - 1, height - 1), outline=(76, 81, 92, 255))
    return panel


def save_expression_sheet(
    images: dict[str, np.ndarray],
    background_kind: str,
    destination: Path,
) -> None:
    panel_width, panel_height = (240, 340)
    columns = 7
    rows = math.ceil((len(ALL_EXPRESSIONS) * len(OUTFITS)) / columns)
    header_height = 70
    sheet = Image.new(
        "RGBA",
        (columns * panel_width, header_height + rows * panel_height),
        (16, 18, 24, 255),
    )
    draw = ImageDraw.Draw(sheet)
    draw.text(
        (18, 18),
        f"SAM SHARED-FACE EXPRESSIONS - {background_kind.upper()}",
        font=load_font(22),
        fill=(242, 246, 252, 255),
    )
    draw.text(
        (18, 47),
        "21 expressions x casual/uniform; each panel shows full registration plus head inset",
        font=load_font(13),
        fill=(166, 177, 191, 255),
    )

    index = 0
    for outfit in OUTFITS:
        base = images[outfit.filename]
        for expression in ALL_EXPRESSIONS:
            overlay = images[f"face_{expression}.png"]
            sprite = Image.fromarray(alpha_composite(base, overlay), "RGBA")
            panel = expression_panel(
                sprite,
                background_kind,
                f"{outfit.name} / {'neutral' if expression == 'neut' else expression}",
            )
            row, column = divmod(index, columns)
            sheet.alpha_composite(
                panel,
                (column * panel_width, header_height + row * panel_height),
            )
            index += 1

    destination.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(destination, format="PNG", compress_level=6)


def save_pose_sheet(
    images: dict[str, np.ndarray],
    background_kind: str,
    destination: Path,
) -> None:
    panel_width, panel_height = (300, 440)
    header_height = 70
    sheet = Image.new(
        "RGBA",
        (len(POSES) * panel_width, header_height + panel_height),
        (16, 18, 24, 255),
    )
    draw = ImageDraw.Draw(sheet)
    draw.text(
        (18, 18),
        f"SAM STANDALONE POSES - {background_kind.upper()}",
        font=load_font(22),
        fill=(242, 246, 252, 255),
    )
    draw.text(
        (18, 47),
        "Canvas registration, silhouette edges, hands, cuffs, and bottom baseline",
        font=load_font(13),
        fill=(166, 177, 191, 255),
    )

    for index, pose in enumerate(POSES):
        panel = pose_panel(
            Image.fromarray(images[pose.filename], "RGBA"),
            background_kind,
            f"{pose.outfit} / {pose.token.replace('_', ' ')}",
        )
        sheet.alpha_composite(panel, (index * panel_width, header_height))

    destination.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(destination, format="PNG", compress_level=6)


def build_review_sheets(images: dict[str, np.ndarray], review_dir: Path) -> list[Path]:
    outputs: list[Path] = []
    for background in ("dark", "light", "checker"):
        expression_path = review_dir / f"sam_expressions_{background}.png"
        pose_path = review_dir / f"sam_poses_{background}.png"
        save_expression_sheet(images, background, expression_path)
        save_pose_sheet(images, background, pose_path)
        outputs.extend((expression_path, pose_path))
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sprite-dir",
        "--sprite-root",
        dest="sprite_dir",
        type=Path,
        default=PRODUCTION_DIR,
        help="production or staged Sam sprite directory (default: installed production)",
    )
    parser.add_argument(
        "--review-dir",
        type=Path,
        default=DEFAULT_REVIEW_DIR,
        help="directory for six dark/light/checker contact sheets",
    )
    parser.add_argument(
        "--skip-review",
        action="store_true",
        help="validate without writing contact sheets",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    sprite_dir = arguments.sprite_dir.resolve()
    review_dir = arguments.review_dir.resolve()
    report = ValidationReport()

    if not sprite_dir.is_dir():
        report.error(f"{sprite_dir}: Sam sprite directory does not exist")
        images: dict[str, np.ndarray] = {}
    else:
        images = load_bank(sprite_dir, report)

    bases = validate_bases(images, report)
    faces_complete = validate_faces(images, bases, report)
    poses_complete = validate_poses(images, report)

    required_loaded = expected_filenames() <= set(images)
    if (
        not arguments.skip_review
        and required_loaded
        and faces_complete
        and poses_complete
    ):
        try:
            outputs = build_review_sheets(images, review_dir)
            report.note(f"review: wrote {len(outputs)} sheet(s) to {review_dir}")
        except (OSError, ValueError, KeyError) as exc:
            report.error(f"cannot write Sam review sheets to {review_dir}: {exc}")
    elif not arguments.skip_review:
        report.note("review: skipped because required valid inputs are incomplete")

    output_stream = sys.stderr if report.errors else sys.stdout
    if report.notes:
        print("SAM SPRITE VALIDATION METRICS", file=output_stream)
        for note in report.notes:
            print(f"  {note}", file=output_stream)

    if report.errors:
        print(
            f"\nSAM SPRITE VALIDATION FAILED ({len(report.errors)} issue(s))",
            file=output_stream,
        )
        for index, error in enumerate(report.errors, start=1):
            print(
                f"  {index}. {error.replace(chr(10), chr(10) + '    ')}",
                file=output_stream,
            )
        return 1

    print(
        "\nSAM SPRITE VALIDATION PASSED: 2 intact bases, 21 shared face layers "
        "(transparent neutral + 20 fixed-mask alternates), 4 canvas-safe poses, "
        "clean transparent RGB, distinct composites, and checker-safe rendering."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
