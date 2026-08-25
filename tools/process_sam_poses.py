#!/usr/bin/env python3
"""Extract and stage-normalize generated full-body pose art for Sam.

This is a review-stage tool.  It deliberately writes only to the requested
output directory; it does not install sprites or edit Ren'Py declarations.

Examples:

    python tools/process_sam_poses.py \
        --input-dir tmp/sam_pose_masters \
        --output-dir tmp/sprite_review/sam_pose_processed

    python tools/process_sam_poses.py \
        --input pose_open_hand_casual=tmp/open_hand.png \
        --input pose_crossed_uniform=tmp/crossed.png \
        --output-dir tmp/sprite_review/sam_pose_processed

An input-map JSON file may also be supplied.  It must be an object whose keys
are the supported pose stems and whose values are image paths.  Relative paths
inside the map are resolved relative to the map file.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from scipy import ndimage


CANVAS_WIDTH = 1023
CANVAS_HEIGHT = 1537
CANVAS_SIZE = (CANVAS_WIDTH, CANVAS_HEIGHT)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANONICAL_DIRECTORY = (
    PROJECT_ROOT / "game" / "mod_assets" / "char_sprites" / "masayami"
)

# Keep this order stable: it controls deterministic processing, metrics, and
# contact-sheet row order.
POSE_OUTFITS: dict[str, str] = {
    "pose_open_hand_casual": "casual",
    "pose_crossed_uniform": "uniform",
    "pose_thinking_uniform": "uniform",
    "pose_phone_casual": "casual",
}
CANONICAL_FILENAMES = {
    "casual": "neutral.png",
    "uniform": "neut_uniform.png",
}
SUPPORTED_INPUT_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


class PoseRejected(ValueError):
    """Raised when an input cannot be processed without risking bad art."""


@dataclass(frozen=True)
class BoundingBox:
    """An exclusive-right/exclusive-bottom pixel bounding box."""

    left: int
    top: int
    right: int
    bottom: int

    @property
    def width(self) -> int:
        return self.right - self.left

    @property
    def height(self) -> int:
        return self.bottom - self.top

    def as_list(self) -> list[int]:
        return [self.left, self.top, self.right, self.bottom]

    def margins(self) -> dict[str, int]:
        return {
            "left": self.left,
            "top": self.top,
            "right": CANVAS_WIDTH - self.right,
            "bottom": CANVAS_HEIGHT - self.bottom,
        }


@dataclass(frozen=True)
class CanonicalStage:
    outfit: str
    source_path: Path
    core_bbox: BoundingBox
    lower_body_anchor_x: float

    def as_metrics(self) -> dict[str, Any]:
        return {
            "reference": str(self.source_path),
            "core_bbox": self.core_bbox.as_list(),
            "margins": self.core_bbox.margins(),
            "lower_body_anchor_x": round(self.lower_body_anchor_x, 4),
            "baseline_y_exclusive": self.core_bbox.bottom,
        }


@dataclass(frozen=True)
class MatteResult:
    rgba: np.ndarray
    hard_foreground: np.ndarray
    metrics: dict[str, Any]


@dataclass(frozen=True)
class ProcessedPose:
    name: str
    image: Image.Image
    metrics: dict[str, Any]


def mask_bbox(mask: np.ndarray) -> BoundingBox:
    rows, columns = np.nonzero(mask)
    if rows.size == 0:
        raise PoseRejected("no foreground survived matte extraction")
    return BoundingBox(
        left=int(columns.min()),
        top=int(rows.min()),
        right=int(columns.max()) + 1,
        bottom=int(rows.max()) + 1,
    )


def largest_run_center(row_mask: np.ndarray) -> float | None:
    """Return the center of the widest foreground run in one scanline."""

    columns = np.flatnonzero(row_mask)
    if columns.size == 0:
        return None
    split_points = np.flatnonzero(np.diff(columns) > 1) + 1
    runs = np.split(columns, split_points)
    widest = max(runs, key=lambda run: (run.size, -int(run[0])))
    return (float(widest[0]) + float(widest[-1])) / 2.0


def lower_body_anchor_x(mask: np.ndarray, bbox: BoundingBox) -> float:
    """Find a pose-stable horizontal anchor from the bottom 12% of the body.

    The widest run is used per row so a hanging hand or separated accessory
    cannot pull the character sideways.  A median across rows makes the anchor
    insensitive to a single irregular hemline or anti-aliased scanline.
    """

    band_start = max(bbox.top, bbox.bottom - max(24, round(bbox.height * 0.12)))
    centers = [
        center
        for row in range(band_start, bbox.bottom)
        if (center := largest_run_center(mask[row])) is not None
    ]
    if len(centers) < 8:
        raise PoseRejected("not enough lower-body pixels to establish stage alignment")
    return float(np.median(np.asarray(centers, dtype=np.float64)))


def load_canonical_stages(canonical_directory: Path) -> dict[str, CanonicalStage]:
    stages: dict[str, CanonicalStage] = {}
    for outfit, filename in CANONICAL_FILENAMES.items():
        source_path = canonical_directory / filename
        if not source_path.is_file():
            raise FileNotFoundError(
                f"missing {outfit} canonical reference: {source_path}"
            )
        with Image.open(source_path) as source_image:
            rgba = np.asarray(source_image.convert("RGBA"))
        if (rgba.shape[1], rgba.shape[0]) != CANVAS_SIZE:
            raise ValueError(
                f"canonical reference {source_path} is {rgba.shape[1]}x{rgba.shape[0]}, "
                f"expected {CANVAS_WIDTH}x{CANVAS_HEIGHT}"
            )
        core = rgba[:, :, 3] >= 128
        bbox = mask_bbox(core)
        stages[outfit] = CanonicalStage(
            outfit=outfit,
            source_path=source_path.resolve(),
            core_bbox=bbox,
            lower_body_anchor_x=lower_body_anchor_x(core, bbox),
        )
    return stages


def learn_checker_palette(
    rgb: np.ndarray,
    frame_mask: np.ndarray,
    minimum: np.ndarray,
    chroma: np.ndarray,
) -> tuple[np.ndarray, int, int, float]:
    """Learn light neutral checker colors from the safe canvas frame.

    Only the top, left, and right borders are sampled.  Sam is intentionally
    cut at the bottom stage baseline, so treating the bottom as a matte seed
    could erase pale clothing that legitimately reaches that edge.
    """

    neutral_frame = frame_mask & (minimum >= 150) & (chroma <= 40)
    frame_size = int(np.count_nonzero(frame_mask))
    neutral_fraction = float(np.count_nonzero(neutral_frame)) / max(frame_size, 1)
    if neutral_fraction < 0.65:
        raise PoseRejected(
            "top/side canvas frame is not predominantly a light neutral checker "
            f"({neutral_fraction:.1%} neutral)"
        )

    neutral_minimum = minimum[neutral_frame]
    matte_minimum = int(
        np.clip(np.percentile(neutral_minimum, 5.0) - 12.0, 170.0, 235.0)
    )
    neutral_chroma = chroma[neutral_frame]
    matte_chroma = int(
        np.clip(np.percentile(neutral_chroma, 95.0) + 8.0, 20.0, 40.0)
    )

    palette_pixels = rgb[
        frame_mask & (minimum >= matte_minimum) & (chroma <= matte_chroma)
    ]
    if palette_pixels.shape[0] < 256:
        raise PoseRejected("not enough checker pixels were found along the canvas frame")

    # Quantized RGB modes provide deterministic palette centers without relying
    # on random k-means initialization.  Four modes cover two checker shades and
    # mild encoding/anti-alias variants while remaining selective around white
    # or gray clothing.
    quantized = (palette_pixels.astype(np.uint16) // 4).astype(np.int16)
    encoded = (
        quantized[:, 0].astype(np.int32) * 4096
        + quantized[:, 1].astype(np.int32) * 64
        + quantized[:, 2].astype(np.int32)
    )
    values, counts = np.unique(encoded, return_counts=True)
    selected_centers: list[np.ndarray] = []
    for value in values[np.argsort(counts)[::-1]]:
        member_pixels = palette_pixels[encoded == value]
        center = np.median(member_pixels, axis=0).astype(np.float32)
        if all(np.linalg.norm(center - prior) >= 5.0 for prior in selected_centers):
            selected_centers.append(center)
        if len(selected_centers) == 4:
            break
    if not selected_centers:
        raise PoseRejected("could not learn checker colors from the canvas frame")

    return (
        np.stack(selected_centers, axis=0),
        matte_minimum,
        matte_chroma,
        neutral_fraction,
    )


def nearest_palette_distance(rgb: np.ndarray, palette: np.ndarray) -> np.ndarray:
    pixels = rgb.astype(np.float32)
    minimum_squared_distance = np.full(rgb.shape[:2], np.inf, dtype=np.float32)
    for color in palette:
        squared_distance = np.sum(
            np.square(pixels - color.reshape(1, 1, 3)), axis=2
        )
        np.minimum(minimum_squared_distance, squared_distance, out=minimum_squared_distance)
    np.sqrt(minimum_squared_distance, out=minimum_squared_distance)
    return minimum_squared_distance


def canvas_frame_mask(height: int, width: int) -> np.ndarray:
    frame_width = max(8, min(height, width) // 64)
    frame = np.zeros((height, width), dtype=bool)
    frame[:frame_width, :] = True
    frame[:, :frame_width] = True
    frame[:, width - frame_width :] = True
    # Exclude the bottom portion of the side strips for the same reason that the
    # bottom edge is not used as a flood-fill seed.
    frame[height - frame_width :, :] = False
    return frame


def learn_checker_pattern(
    rgb: np.ndarray,
    frame_mask: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, dict[str, float]]:
    """Model the checker's global light/dark phase at every canvas pixel.

    Palette similarity alone is unsafe for Sam's white uniform shirt and cuffs.
    The generated checker is an axis-aligned alternating grid, so top and left
    background strips provide its exact horizontal and vertical phase without
    assuming one fixed tile size across generated masters.
    """

    luminance = rgb.astype(np.float32).mean(axis=2)
    stripe_width = 8
    horizontal_profile = np.median(luminance[:stripe_width, :], axis=0)
    vertical_profile = np.median(luminance[:, :stripe_width], axis=1)
    profile_values = np.concatenate((horizontal_profile, vertical_profile))

    dark_level, light_level = np.percentile(profile_values, (20.0, 80.0))
    for _ in range(16):
        midpoint = (dark_level + light_level) / 2.0
        dark_values = profile_values[profile_values <= midpoint]
        light_values = profile_values[profile_values > midpoint]
        if dark_values.size == 0 or light_values.size == 0:
            raise PoseRejected("could not separate the two checker shades")
        updated_dark = float(dark_values.mean())
        updated_light = float(light_values.mean())
        if abs(updated_dark - dark_level) + abs(updated_light - light_level) < 1e-4:
            dark_level, light_level = updated_dark, updated_light
            break
        dark_level, light_level = updated_dark, updated_light

    if light_level - dark_level < 3.0:
        raise PoseRejected(
            "light background does not contain a measurable checker pattern"
        )
    split_level = (dark_level + light_level) / 2.0
    horizontal_light = horizontal_profile > split_level
    vertical_light = vertical_profile > split_level
    top_left_light = bool(np.median(luminance[:stripe_width, :stripe_width]) > split_level)
    expected_light = np.logical_xor(
        np.logical_xor(vertical_light[:, None], horizontal_light[None, :]),
        top_left_light,
    )
    observed_light = luminance > split_level
    phase_match = observed_light == expected_light
    expected_luminance = np.where(
        expected_light, light_level, dark_level
    ).astype(np.float32)
    luminance_error = np.abs(luminance - expected_luminance)

    return phase_match, luminance_error, {
        "checker_dark_luminance": round(dark_level, 4),
        "checker_light_luminance": round(light_level, 4),
        "checker_phase_frame_accuracy": round(
            float(np.mean(phase_match[frame_mask])), 6
        ),
    }


def connected_checker_regions(
    candidate: np.ndarray,
    rgb: np.ndarray,
    chroma: np.ndarray,
    palette_distance: np.ndarray,
    palette_tolerance: float,
    checker_phase_match: np.ndarray,
    checker_luminance_error: np.ndarray,
    include_bottom_edge: bool = False,
    accept_large_enclosed_gaps: bool = False,
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    """Separate canvas-connected checker from safe checker-colored islands."""

    component_count, labels, stats, _ = cv2.connectedComponentsWithStats(
        candidate.astype(np.uint8), connectivity=8
    )
    height, width = candidate.shape
    canvas_background = np.zeros_like(candidate, dtype=bool)
    island_background = np.zeros_like(candidate, dtype=bool)
    canvas_components = 0
    island_components = 0
    phase_checker_components = 0
    hair_gap_components = 0
    skin_gap_components = 0
    protected_pale_components = 0
    large_enclosed_gap_components = 0
    protected_component_details: list[dict[str, Any]] = []

    for label in range(1, component_count):
        left = int(stats[label, cv2.CC_STAT_LEFT])
        top = int(stats[label, cv2.CC_STAT_TOP])
        component_width = int(stats[label, cv2.CC_STAT_WIDTH])
        component_height = int(stats[label, cv2.CC_STAT_HEIGHT])
        area = int(stats[label, cv2.CC_STAT_AREA])
        component_slice = np.s_[
            top : top + component_height,
            left : left + component_width,
        ]
        local_component = labels[component_slice] == label

        # Bottom-only contact is intentionally excluded: the character is
        # supposed to meet the canvas there.  Any real exterior matte still
        # reaches one of the other three sides when those sides are uncropped.
        touches_safe_canvas = (
            left == 0
            or top == 0
            or left + component_width == width
            or (
                include_bottom_edge
                and top + component_height == height
            )
        )
        if touches_safe_canvas:
            local_background = canvas_background[component_slice]
            local_background[local_component] = True
            canvas_components += 1
            continue

        if area < 6:
            continue
        distances = palette_distance[component_slice][local_component]
        palette_match_fraction = float(np.mean(distances <= palette_tolerance))
        strongly_neutral_fraction = float(
            np.mean(chroma[component_slice][local_component] <= 12)
        )

        if palette_match_fraction < 0.90 or strongly_neutral_fraction < 0.90:
            continue

        phase_fraction = float(
            np.mean(checker_phase_match[component_slice][local_component])
        )
        mean_luminance_error = float(
            np.mean(checker_luminance_error[component_slice][local_component])
        )

        expanded_left = max(0, left - 3)
        expanded_top = max(0, top - 3)
        expanded_right = min(width, left + component_width + 3)
        expanded_bottom = min(height, top + component_height + 3)
        expanded_slice = np.s_[
            expanded_top:expanded_bottom,
            expanded_left:expanded_right,
        ]
        expanded_component = labels[expanded_slice] == label
        boundary = cv2.dilate(
            expanded_component.astype(np.uint8), np.ones((7, 7), dtype=np.uint8)
        ).astype(bool) & ~expanded_component
        boundary_rgb = rgb[expanded_slice][boundary].astype(np.int16)
        red, green, blue = (
            boundary_rgb[:, 0],
            boundary_rgb[:, 1],
            boundary_rgb[:, 2],
        )
        skin_fraction = float(
            np.mean(
                (red - green >= 8)
                & (green - blue >= 4)
                & (red >= 170)
                & (green >= 120)
            )
        )
        blond_hair_fraction = float(
            np.mean(
                (red - blue >= 35)
                & (red - green >= 8)
                & (red >= 150)
            )
        )

        # Large genuine gaps reproduce both the checker's color and its global
        # alternating phase.  Small checker pockets enclosed by flyaway hair or
        # spread fingers may be locally inpainted by the generator, so those two
        # narrowly identifiable boundary cases are also accepted.  Crucially,
        # flat white collar/cuff/eye components match none of these rules.
        follows_checker_pattern = (
            area >= 200
            and phase_fraction >= 0.82
            and mean_luminance_error <= 5.0
        )
        # A generator can redraw the checker inside a fully enclosed negative
        # space with a different phase.  Full-body references commonly expose
        # one such tall, narrow region between the legs.  Keep this opt-in so
        # production-pose processing continues to protect broad white clothes.
        large_enclosed_gap = accept_large_enclosed_gaps and (
            (
                area >= 5_000
                and component_height >= component_width * 4
                and palette_match_fraction >= 0.98
                and strongly_neutral_fraction >= 0.98
            )
            # Some enclosed gaps are regenerated with the right checker
            # colors but a locally reset phase.  Near-exact palette matches
            # remain safe to remove even when that phase differs.
            or (
                area >= 150
                and palette_match_fraction >= 0.985
                and strongly_neutral_fraction >= 0.99
                and mean_luminance_error <= 4.8
            )
            # Narrow negative spaces around hair and limbs can pick up more
            # antialias contamination than the exact-palette rule tolerates.
            # Their extreme aspect ratio distinguishes them from white shirt
            # panels and cuffs.
            or (
                area >= 250
                and component_height >= component_width * 4
                and palette_match_fraction >= 0.95
                and strongly_neutral_fraction >= 0.99
            )
        )
        enclosed_by_top_hair = (
            top + component_height <= 220 and blond_hair_fraction >= 0.45
        )
        small_gap_between_skin = (
            top >= 400
            and area <= 200
            and skin_fraction >= 0.40
            and blond_hair_fraction < 0.40
        )
        if (
            follows_checker_pattern
            or large_enclosed_gap
            or enclosed_by_top_hair
            or small_gap_between_skin
        ):
            local_background = island_background[component_slice]
            local_background[local_component] = True
            island_components += 1
            if follows_checker_pattern:
                phase_checker_components += 1
            elif large_enclosed_gap:
                large_enclosed_gap_components += 1
            elif enclosed_by_top_hair:
                hair_gap_components += 1
            else:
                skin_gap_components += 1
        else:
            protected_pale_components += 1
            protected_component_details.append(
                {
                    "bbox": [
                        left,
                        top,
                        left + component_width,
                        top + component_height,
                    ],
                    "area": area,
                    "palette_match_fraction": round(palette_match_fraction, 6),
                    "neutral_fraction": round(strongly_neutral_fraction, 6),
                    "checker_phase_fraction": round(phase_fraction, 6),
                    "mean_luminance_error": round(mean_luminance_error, 6),
                }
            )

    return canvas_background, island_background, {
        "candidate_component_count": component_count - 1,
        "canvas_checker_components": canvas_components,
        "enclosed_checker_components": island_components,
        "phase_matched_checker_components": phase_checker_components,
        "large_enclosed_gap_components": large_enclosed_gap_components,
        "top_hair_checker_components": hair_gap_components,
        "small_skin_gap_checker_components": skin_gap_components,
        "protected_pale_components": protected_pale_components,
        "largest_protected_pale_components": sorted(
            protected_component_details,
            key=lambda component: component["area"],
            reverse=True,
        )[:12],
    }


def retain_character_components(
    foreground: np.ndarray,
    palette_distance: np.ndarray,
    palette_tolerance: float,
) -> tuple[np.ndarray, dict[str, Any]]:
    """Drop checker debris while preserving plausible detached drawn details."""

    component_count, labels, stats, _ = cv2.connectedComponentsWithStats(
        foreground.astype(np.uint8), connectivity=8
    )
    if component_count <= 1:
        raise PoseRejected("matte extraction produced no connected foreground")

    areas = stats[1:, cv2.CC_STAT_AREA]
    main_label = int(np.argmax(areas)) + 1
    main_component = labels == main_label
    distance_from_main = ndimage.distance_transform_edt(~main_component)
    retained = main_component.copy()
    retained_components = 1
    dropped_components = 0
    dropped_pixels = 0

    for label in range(1, component_count):
        if label == main_label:
            continue
        left = int(stats[label, cv2.CC_STAT_LEFT])
        top = int(stats[label, cv2.CC_STAT_TOP])
        component_width = int(stats[label, cv2.CC_STAT_WIDTH])
        component_height = int(stats[label, cv2.CC_STAT_HEIGHT])
        component_slice = np.s_[
            top : top + component_height,
            left : left + component_width,
        ]
        local_component = labels[component_slice] == label
        area = int(stats[label, cv2.CC_STAT_AREA])
        checker_fraction = float(
            np.mean(
                palette_distance[component_slice][local_component]
                <= palette_tolerance * 1.35
            )
        )
        separation = float(
            distance_from_main[component_slice][local_component].min()
        )

        looks_drawn = checker_fraction < 0.65
        close_fine_detail = area >= 8 and separation <= 96.0
        substantial_detail = area >= 64
        if looks_drawn and (close_fine_detail or substantial_detail):
            local_retained = retained[component_slice]
            local_retained[local_component] = True
            retained_components += 1
        else:
            dropped_components += 1
            dropped_pixels += area

    return retained, {
        "foreground_component_count_before_cleanup": component_count - 1,
        "foreground_component_count_retained": retained_components,
        "foreground_component_count_dropped": dropped_components,
        "disconnected_pixels_dropped": dropped_pixels,
    }


def soften_and_decontaminate(
    rgb: np.ndarray,
    foreground: np.ndarray,
    feather_radius: float,
) -> tuple[np.ndarray, dict[str, int]]:
    """Build a soft alpha edge and replace matte-polluted transition colors."""

    inside_distance = ndimage.distance_transform_edt(foreground)
    outside_distance = ndimage.distance_transform_edt(~foreground)
    signed_distance = inside_distance - outside_distance
    alpha_float = np.clip(
        0.5 + signed_distance / (2.0 * feather_radius), 0.0, 1.0
    )

    safe_distance = max(2.0, float(np.ceil(feather_radius)))
    safe_foreground = foreground & (inside_distance >= safe_distance)
    if not np.any(safe_foreground):
        raise PoseRejected("foreground is too thin to decontaminate safely")

    _, nearest_indices = ndimage.distance_transform_edt(
        ~safe_foreground, return_indices=True
    )
    nearest_rgb = rgb[nearest_indices[0], nearest_indices[1]]
    alpha = np.rint(alpha_float * 255.0).astype(np.uint8)
    transition = (alpha > 0) & (alpha < 255)
    transparent = alpha == 0

    cleaned_rgb = rgb.copy()
    cleaned_rgb[transition] = nearest_rgb[transition]
    cleaned_rgb[transparent] = 0
    cleaned_rgba = np.dstack((cleaned_rgb, alpha))
    return cleaned_rgba, {
        "soft_alpha_pixels": int(np.count_nonzero(transition)),
        "decontaminated_transition_pixels": int(np.count_nonzero(transition)),
        "transparent_pixels": int(np.count_nonzero(transparent)),
        "nonzero_rgb_values_under_zero_alpha": int(
            np.count_nonzero(cleaned_rgba[:, :, :3][transparent])
        ),
    }


def extract_checker_matte(
    source_path: Path,
    feather_radius: float,
    palette_tolerance: float,
    include_bottom_edge: bool = False,
    accept_large_enclosed_gaps: bool = False,
    minimum_foreground_fraction: float = 0.05,
) -> MatteResult:
    try:
        with Image.open(source_path) as opened_image:
            source_image = ImageOps.exif_transpose(opened_image)
            rgba = np.asarray(source_image.convert("RGBA"))
    except (OSError, ValueError) as error:
        raise PoseRejected(f"cannot read input image: {error}") from error

    height, width = rgba.shape[:2]
    if (width, height) != CANVAS_SIZE:
        raise PoseRejected(
            f"input is {width}x{height}; expected opaque "
            f"{CANVAS_WIDTH}x{CANVAS_HEIGHT}"
        )
    input_alpha = rgba[:, :, 3]
    if np.any(input_alpha != 255):
        raise PoseRejected(
            "input already contains transparency; expected an opaque generated master"
        )

    rgb = rgba[:, :, :3]
    maximum = rgb.max(axis=2)
    minimum = rgb.min(axis=2)
    chroma = maximum - minimum
    frame_mask = canvas_frame_mask(height, width)
    (
        checker_palette,
        matte_minimum,
        matte_chroma,
        neutral_frame_fraction,
    ) = learn_checker_palette(rgb, frame_mask, minimum, chroma)
    palette_distance = nearest_palette_distance(rgb, checker_palette)
    (
        checker_phase_match,
        checker_luminance_error,
        checker_pattern_metrics,
    ) = learn_checker_pattern(rgb, frame_mask)
    background_candidate = (
        (minimum >= matte_minimum)
        & (chroma <= matte_chroma)
        & (palette_distance <= palette_tolerance * 1.75)
    )

    safe_edge = np.zeros((height, width), dtype=bool)
    safe_edge[0, :] = True
    safe_edge[:, 0] = True
    safe_edge[:, -1] = True
    safe_edge[-1, :] = False
    edge_checker_fraction = float(np.mean(background_candidate[safe_edge]))
    if edge_checker_fraction < 0.70:
        raise PoseRejected(
            "top/side edge does not contain enough recognized checker matte "
            f"({edge_checker_fraction:.1%})"
        )

    (
        canvas_background,
        island_background,
        component_metrics,
    ) = connected_checker_regions(
        background_candidate,
        rgb,
        chroma,
        palette_distance,
        palette_tolerance,
        checker_phase_match,
        checker_luminance_error,
        include_bottom_edge=include_bottom_edge,
        accept_large_enclosed_gaps=accept_large_enclosed_gaps,
    )
    background = canvas_background | island_background
    foreground = ~background

    # Remove neutral matte pixels directly along every known matte boundary.
    # This severs contaminated checker rims before connected-component cleanup.
    inside_distance = ndimage.distance_transform_edt(foreground)
    broad_neutral_matte = (
        (minimum >= max(145, matte_minimum - 55))
        & (chroma <= min(55, matte_chroma + 18))
        & (palette_distance <= palette_tolerance * 2.5)
    )
    fringe = foreground & (inside_distance <= 3.0) & broad_neutral_matte
    foreground &= ~fringe

    foreground, cleanup_metrics = retain_character_components(
        foreground, palette_distance, palette_tolerance
    )
    foreground_pixels = int(np.count_nonzero(foreground))
    foreground_fraction = foreground_pixels / float(width * height)
    if not minimum_foreground_fraction <= foreground_fraction <= 0.80:
        raise PoseRejected(
            "implausible extracted foreground coverage "
            f"({foreground_fraction:.1%}); checker segmentation is unsafe"
        )

    cleaned_rgba, alpha_metrics = soften_and_decontaminate(
        rgb, foreground, feather_radius
    )
    palette_as_lists = [
        [round(float(channel), 2) for channel in color]
        for color in checker_palette
    ]
    metrics: dict[str, Any] = {
        "checker_palette_rgb": palette_as_lists,
        "checker_minimum_channel_threshold": matte_minimum,
        "checker_chroma_threshold": matte_chroma,
        "checker_palette_tolerance": palette_tolerance,
        "neutral_frame_fraction": round(neutral_frame_fraction, 6),
        "edge_checker_fraction": round(edge_checker_fraction, 6),
        "canvas_checker_pixels": int(np.count_nonzero(canvas_background)),
        "enclosed_checker_pixels": int(np.count_nonzero(island_background)),
        "neutral_fringe_pixels_removed": int(np.count_nonzero(fringe)),
        "hard_foreground_pixels": foreground_pixels,
        "hard_foreground_fraction": round(foreground_fraction, 6),
        **checker_pattern_metrics,
        **component_metrics,
        **cleanup_metrics,
        **alpha_metrics,
    }
    return MatteResult(
        rgba=cleaned_rgba,
        hard_foreground=foreground,
        metrics=metrics,
    )


def reject_cropped_bbox(
    bbox: BoundingBox,
    crop_margin: int,
    stage: str,
) -> None:
    margins = bbox.margins()
    unsafe = [
        side
        for side in ("top", "left", "right")
        if margins[side] < crop_margin
    ]
    if unsafe:
        rendered = ", ".join(f"{side}={margins[side]}px" for side in unsafe)
        raise PoseRejected(
            f"{stage} foreground is cropped or unsafe at {rendered}; "
            f"required margin is {crop_margin}px"
        )


def warp_rgba_premultiplied(rgba: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    """Affine-warp RGBA without introducing transparent-edge color halos."""

    source = rgba.astype(np.float32) / 255.0
    alpha = source[:, :, 3:4]
    premultiplied = np.concatenate((source[:, :, :3] * alpha, alpha), axis=2)
    warped = cv2.warpAffine(
        premultiplied,
        matrix.astype(np.float32),
        CANVAS_SIZE,
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0.0, 0.0, 0.0, 0.0),
    )
    warped_alpha = np.clip(warped[:, :, 3:4], 0.0, 1.0)
    warped_rgb = np.divide(
        np.clip(warped[:, :, :3], 0.0, 1.0),
        warped_alpha,
        out=np.zeros_like(warped[:, :, :3]),
        where=warped_alpha > 1e-5,
    )
    output = np.concatenate((warped_rgb, warped_alpha), axis=2)
    output = np.rint(np.clip(output, 0.0, 1.0) * 255.0).astype(np.uint8)
    output[output[:, :, 3] == 0, :3] = 0
    return output


def normalize_to_stage(
    matte: MatteResult,
    canonical: CanonicalStage,
    crop_margin: int,
) -> tuple[np.ndarray, dict[str, Any]]:
    source_bbox = mask_bbox(matte.hard_foreground)
    reject_cropped_bbox(source_bbox, crop_margin, "source")
    source_anchor = lower_body_anchor_x(matte.hard_foreground, source_bbox)

    scale = canonical.core_bbox.height / float(source_bbox.height)
    translate_x = canonical.lower_body_anchor_x - scale * source_anchor
    translate_y = canonical.core_bbox.bottom - scale * source_bbox.bottom

    transformed_left = scale * source_bbox.left + translate_x
    transformed_right = scale * source_bbox.right + translate_x
    transformed_top = scale * source_bbox.top + translate_y
    if transformed_left < crop_margin or transformed_right > CANVAS_WIDTH - crop_margin:
        raise PoseRejected(
            "stage normalization would crop a side of the pose "
            f"(predicted x extent {transformed_left:.2f}..{transformed_right:.2f})"
        )
    if transformed_top < crop_margin:
        raise PoseRejected(
            "stage normalization would crop the top of the pose "
            f"(predicted y={transformed_top:.2f})"
        )

    matrix = np.asarray(
        ((scale, 0.0, translate_x), (0.0, scale, translate_y)),
        dtype=np.float32,
    )
    normalized_rgba = warp_rgba_premultiplied(matte.rgba, matrix)
    output_core = normalized_rgba[:, :, 3] >= 128
    output_bbox = mask_bbox(output_core)
    reject_cropped_bbox(output_bbox, crop_margin, "normalized")
    output_visible_bbox = mask_bbox(normalized_rgba[:, :, 3] > 0)
    # Validation and Ren'Py both see even a low-alpha edge pixel.  Requiring a
    # one-pixel clear border catches feather or Lanczos support that was clipped
    # despite the >=128 core remaining nominally inside the canvas.
    reject_cropped_bbox(output_visible_bbox, 1, "normalized soft-alpha")

    transparent = normalized_rgba[:, :, 3] == 0
    rgb_under_zero = int(
        np.count_nonzero(normalized_rgba[:, :, :3][transparent])
    )
    if rgb_under_zero:
        raise PoseRejected(
            f"normalization left {rgb_under_zero} RGB values under zero alpha"
        )

    metrics: dict[str, Any] = {
        "source_core_bbox": source_bbox.as_list(),
        "source_margins": source_bbox.margins(),
        "source_lower_body_anchor_x": round(source_anchor, 4),
        "scale": round(scale, 8),
        "translation_x": round(translate_x, 6),
        "translation_y": round(translate_y, 6),
        "predicted_transformed_extent": {
            "left": round(transformed_left, 4),
            "top": round(transformed_top, 4),
            "right": round(transformed_right, 4),
            "bottom": canonical.core_bbox.bottom,
        },
        "output_core_bbox": output_bbox.as_list(),
        "output_margins": output_bbox.margins(),
        "output_visible_bbox": output_visible_bbox.as_list(),
        "output_visible_margins": output_visible_bbox.margins(),
        "output_soft_alpha_pixels": int(
            np.count_nonzero(
                (normalized_rgba[:, :, 3] > 0)
                & (normalized_rgba[:, :, 3] < 255)
            )
        ),
        "output_nonzero_rgb_values_under_zero_alpha": rgb_under_zero,
    }
    return normalized_rgba, metrics


def process_pose(
    name: str,
    source_path: Path,
    canonical: CanonicalStage,
    feather_radius: float,
    palette_tolerance: float,
    crop_margin: int,
) -> ProcessedPose:
    matte = extract_checker_matte(source_path, feather_radius, palette_tolerance)
    normalized_rgba, stage_metrics = normalize_to_stage(
        matte, canonical, crop_margin
    )
    output_image = Image.fromarray(normalized_rgba, mode="RGBA")
    metrics: dict[str, Any] = {
        "name": name,
        "outfit": canonical.outfit,
        "status": "accepted",
        "input": str(source_path.resolve()),
        "source_dimensions": [CANVAS_WIDTH, CANVAS_HEIGHT],
        "input_was_fully_opaque": True,
        "matte": matte.metrics,
        "stage_normalization": stage_metrics,
    }
    return ProcessedPose(name=name, image=output_image, metrics=metrics)


def normalize_pose_name(raw_name: str) -> str:
    candidate = raw_name.strip()
    if Path(candidate).suffix.lower() in SUPPORTED_INPUT_SUFFIXES:
        candidate = Path(candidate).stem
    if candidate not in POSE_OUTFITS:
        supported = ", ".join(POSE_OUTFITS)
        raise ValueError(f"unsupported pose name {raw_name!r}; expected one of: {supported}")
    return candidate


def parse_assignment(assignment: str) -> tuple[str, Path]:
    if "=" not in assignment:
        raise ValueError(
            f"invalid --input {assignment!r}; expected POSE_NAME=IMAGE_PATH"
        )
    raw_name, raw_path = assignment.split("=", 1)
    if not raw_path.strip():
        raise ValueError(f"missing path in --input {assignment!r}")
    return normalize_pose_name(raw_name), Path(raw_path.strip())


def inputs_from_assignments(assignments: Sequence[str]) -> dict[str, Path]:
    inputs: dict[str, Path] = {}
    for assignment in assignments:
        name, source_path = parse_assignment(assignment)
        if name in inputs:
            raise ValueError(f"pose {name!r} was mapped more than once")
        inputs[name] = source_path
    return inputs


def inputs_from_json(map_path: Path) -> dict[str, Path]:
    try:
        raw_mapping = json.loads(map_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read input map {map_path}: {error}") from error
    if not isinstance(raw_mapping, Mapping):
        raise ValueError("input-map JSON must contain an object")

    inputs: dict[str, Path] = {}
    for raw_name, raw_path in raw_mapping.items():
        if not isinstance(raw_name, str) or not isinstance(raw_path, str):
            raise ValueError("input-map keys and values must both be strings")
        name = normalize_pose_name(raw_name)
        if name in inputs:
            raise ValueError(f"pose {name!r} was mapped more than once")
        source_path = Path(raw_path)
        if not source_path.is_absolute():
            source_path = map_path.parent / source_path
        inputs[name] = source_path
    return inputs


def inputs_from_directory(input_directory: Path) -> dict[str, Path]:
    if not input_directory.is_dir():
        raise ValueError(f"input directory does not exist: {input_directory}")
    discovered: dict[str, list[Path]] = {name: [] for name in POSE_OUTFITS}
    for candidate in input_directory.iterdir():
        if not candidate.is_file() or candidate.suffix.lower() not in SUPPORTED_INPUT_SUFFIXES:
            continue
        if candidate.stem.lower() in discovered:
            discovered[candidate.stem.lower()].append(candidate)

    ambiguous = {name: paths for name, paths in discovered.items() if len(paths) > 1}
    if ambiguous:
        details = "; ".join(
            f"{name}: {', '.join(path.name for path in paths)}"
            for name, paths in ambiguous.items()
        )
        raise ValueError(f"ambiguous pose masters in {input_directory}: {details}")
    return {
        name: paths[0]
        for name, paths in discovered.items()
        if len(paths) == 1
    }


def checker_background(width: int, height: int, tile_size: int = 16) -> Image.Image:
    rows, columns = np.indices((height, width))
    alternating = ((rows // tile_size) + (columns // tile_size)) % 2
    first = np.asarray((222, 222, 222), dtype=np.uint8)
    second = np.asarray((250, 250, 250), dtype=np.uint8)
    rgb = np.where(alternating[:, :, None] == 0, first, second)
    return Image.fromarray(rgb.astype(np.uint8), mode="RGB")


def composite_preview(
    sprite: Image.Image,
    background_name: str,
    preview_size: tuple[int, int],
) -> Image.Image:
    if background_name == "dark":
        background = Image.new("RGB", preview_size, (20, 23, 31))
    elif background_name == "light":
        background = Image.new("RGB", preview_size, (246, 246, 246))
    elif background_name == "checker":
        background = checker_background(*preview_size)
    else:  # pragma: no cover - internal invariant
        raise ValueError(f"unknown preview background: {background_name}")

    resized = sprite.resize(preview_size, Image.Resampling.LANCZOS)
    background.paste(resized, (0, 0), resized)
    return background


def make_contact_sheet(
    processed_poses: Iterable[ProcessedPose],
    preview_width: int,
) -> Image.Image:
    poses = list(processed_poses)
    if not poses:
        raise ValueError("cannot build a contact sheet without accepted poses")

    preview_height = round(preview_width * CANVAS_HEIGHT / CANVAS_WIDTH)
    backgrounds = ("dark", "light", "checker")
    margin = 16
    column_gap = 12
    heading_height = 30
    row_label_height = 28
    row_gap = 18
    sheet_width = (
        margin * 2
        + preview_width * len(backgrounds)
        + column_gap * (len(backgrounds) - 1)
    )
    sheet_height = (
        margin * 2
        + heading_height
        + len(poses) * (row_label_height + preview_height)
        + (len(poses) - 1) * row_gap
    )
    sheet = Image.new("RGB", (sheet_width, sheet_height), (45, 47, 54))
    draw = ImageDraw.Draw(sheet)

    for column, background_name in enumerate(backgrounds):
        left = margin + column * (preview_width + column_gap)
        draw.text(
            (left + 4, margin + 6),
            background_name.upper(),
            fill=(242, 242, 244),
        )

    row_top = margin + heading_height
    for pose in poses:
        draw.text(
            (margin + 4, row_top + 6),
            pose.name,
            fill=(242, 242, 244),
        )
        preview_top = row_top + row_label_height
        for column, background_name in enumerate(backgrounds):
            left = margin + column * (preview_width + column_gap)
            preview = composite_preview(
                pose.image, background_name, (preview_width, preview_height)
            )
            sheet.paste(preview, (left, preview_top))
            draw.rectangle(
                (
                    left,
                    preview_top,
                    left + preview_width - 1,
                    preview_top + preview_height - 1,
                ),
                outline=(92, 95, 104),
                width=1,
            )
        row_top = preview_top + preview_height + row_gap
    return sheet


def save_png(image: Image.Image, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, format="PNG", optimize=True)


def ordered_inputs(inputs: Mapping[str, Path]) -> list[tuple[str, Path]]:
    return [(name, inputs[name]) for name in POSE_OUTFITS if name in inputs]


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Extract checker-backed Sam pose masters, normalize them to Sam's "
            "canonical stage placement, and write audit artifacts."
        )
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--input-dir",
        type=Path,
        help="directory containing any supported pose masters by exact stem",
    )
    input_group.add_argument(
        "--input",
        action="append",
        metavar="POSE=PATH",
        help="map one supported pose name to a master; may be repeated",
    )
    input_group.add_argument(
        "--input-map",
        type=Path,
        help="JSON object mapping supported pose names to master paths",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="review output directory (never installed automatically)",
    )
    parser.add_argument(
        "--canonical-dir",
        type=Path,
        default=DEFAULT_CANONICAL_DIRECTORY,
        help="directory containing Sam's neutral.png and neut_uniform.png",
    )
    parser.add_argument(
        "--require-all",
        action="store_true",
        help="reject the run unless all four expected pose masters are present",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite same-named review outputs in the output directory",
    )
    parser.add_argument(
        "--feather-radius",
        type=float,
        default=2.0,
        help="soft-alpha half-width in source pixels (default: 2.0)",
    )
    parser.add_argument(
        "--checker-tolerance",
        type=float,
        default=18.0,
        help="RGB distance allowed from learned checker colors (default: 18)",
    )
    parser.add_argument(
        "--crop-margin",
        type=int,
        default=2,
        help="minimum safe top/side core margin in pixels (default: 2)",
    )
    parser.add_argument(
        "--contact-width",
        type=int,
        default=280,
        help="width of each contact-sheet preview column (default: 280)",
    )
    return parser


def validate_options(args: argparse.Namespace) -> None:
    if not 0.5 <= args.feather_radius <= 8.0:
        raise ValueError("--feather-radius must be between 0.5 and 8.0")
    if not 2.0 <= args.checker_tolerance <= 64.0:
        raise ValueError("--checker-tolerance must be between 2 and 64")
    if not 1 <= args.crop_margin <= 32:
        raise ValueError("--crop-margin must be between 1 and 32")
    if not 128 <= args.contact_width <= 640:
        raise ValueError("--contact-width must be between 128 and 640")


def resolve_inputs(args: argparse.Namespace) -> dict[str, Path]:
    if args.input_dir is not None:
        inputs = inputs_from_directory(args.input_dir)
    elif args.input_map is not None:
        inputs = inputs_from_json(args.input_map)
    else:
        inputs = inputs_from_assignments(args.input or [])

    if not inputs:
        expected = ", ".join(f"{name}.png" for name in POSE_OUTFITS)
        raise ValueError(f"no supported pose masters were found; expected: {expected}")
    if args.require_all:
        missing = [name for name in POSE_OUTFITS if name not in inputs]
        if missing:
            raise ValueError(
                "missing required pose masters: " + ", ".join(missing)
            )

    for name, source_path in inputs.items():
        if not source_path.is_file():
            raise ValueError(f"input for {name} does not exist: {source_path}")
    return inputs


def reject_unsafe_output_paths(
    inputs: Mapping[str, Path],
    output_directory: Path,
    force: bool,
) -> None:
    source_paths = {path.resolve() for path in inputs.values()}
    planned = [output_directory / f"{name}.png" for name in inputs]
    planned.extend(
        (output_directory / "metrics.json", output_directory / "contact_sheet.png")
    )
    overlap = [path for path in planned if path.resolve() in source_paths]
    if overlap:
        raise ValueError(
            "output would overwrite an opaque source master: "
            + ", ".join(str(path) for path in overlap)
        )
    existing = [path for path in planned if path.exists()]
    if existing and not force:
        raise ValueError(
            "review outputs already exist (pass --force to replace them): "
            + ", ".join(str(path) for path in existing)
        )


def write_metrics(metrics: Mapping[str, Any], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(metrics, indent=2, sort_keys=False) + "\n", encoding="utf-8"
    )


def run(args: argparse.Namespace) -> int:
    validate_options(args)
    inputs = resolve_inputs(args)
    output_directory = args.output_dir
    reject_unsafe_output_paths(inputs, output_directory, args.force)
    canonical_stages = load_canonical_stages(args.canonical_dir)

    accepted: list[ProcessedPose] = []
    pose_metrics: list[dict[str, Any]] = []
    for name, source_path in ordered_inputs(inputs):
        outfit = POSE_OUTFITS[name]
        canonical = canonical_stages[outfit]
        try:
            processed = process_pose(
                name=name,
                source_path=source_path,
                canonical=canonical,
                feather_radius=args.feather_radius,
                palette_tolerance=args.checker_tolerance,
                crop_margin=args.crop_margin,
            )
        except PoseRejected as error:
            pose_metrics.append(
                {
                    "name": name,
                    "outfit": outfit,
                    "status": "rejected",
                    "input": str(source_path.resolve()),
                    "reason": str(error),
                }
            )
            print(f"REJECTED {name}: {error}", file=sys.stderr)
            continue
        accepted.append(processed)
        pose_metrics.append(processed.metrics)

    output_directory.mkdir(parents=True, exist_ok=True)
    for processed in accepted:
        output_path = output_directory / f"{processed.name}.png"
        save_png(processed.image, output_path)
        processed.metrics["output"] = str(output_path.resolve())
        print(f"ACCEPTED {processed.name} -> {output_path}")

    contact_path: Path | None = None
    if accepted:
        contact_path = output_directory / "contact_sheet.png"
        contact_sheet = make_contact_sheet(accepted, args.contact_width)
        save_png(contact_sheet, contact_path)

    rejected_count = len(pose_metrics) - len(accepted)
    aggregate_status = "accepted" if rejected_count == 0 else "rejected"
    metrics: dict[str, Any] = {
        "schema_version": 1,
        "tool": "tools/process_sam_poses.py",
        "status": aggregate_status,
        "canvas_dimensions": [CANVAS_WIDTH, CANVAS_HEIGHT],
        "expected_pose_outfits": POSE_OUTFITS,
        "canonical_stages": {
            outfit: canonical_stages[outfit].as_metrics()
            for outfit in CANONICAL_FILENAMES
        },
        "settings": {
            "feather_radius": args.feather_radius,
            "checker_tolerance": args.checker_tolerance,
            "crop_margin": args.crop_margin,
            "contact_width": args.contact_width,
        },
        "accepted_count": len(accepted),
        "rejected_count": rejected_count,
        "contact_sheet": str(contact_path.resolve()) if contact_path else None,
        "poses": pose_metrics,
    }
    metrics_path = output_directory / "metrics.json"
    write_metrics(metrics, metrics_path)
    print(f"METRICS {metrics_path}")
    if contact_path is not None:
        print(f"CONTACT {contact_path}")
    return 2 if rejected_count else 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)
    try:
        return run(args)
    except (FileNotFoundError, ValueError) as error:
        parser.error(str(error))
    return 2  # pragma: no cover - argparse.error exits


if __name__ == "__main__":
    raise SystemExit(main())
