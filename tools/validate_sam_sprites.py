#!/usr/bin/env python3
"""Validate Sam's layered-image sprite bank and build its review sheet.

The production contract checked here is deliberately stricter than "Pillow can
open the file".  Sam's two original neutral sprites must be reconstructed
pixel-for-pixel by outfit-native featureless bases plus neutral face layers;
all alternate faces must remain inside the registered face area; and fixed
poses must retain a soft, unclipped silhouette.

Run from anywhere inside or outside the project::

    python tools/validate_sam_sprites.py

By default a visual review sheet is written to
``tmp/sprite_review/sam_contact_sheet.png``.  It shows every casual and uniform
expression on dark, light, and checker backgrounds, followed by the four fixed
poses on the same backgrounds.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CANVAS_SIZE = (1023, 1537)

# Both original outfits use the same registered head.  The rectangle remains a
# useful coarse diagnostic, but it is not the expression-layer allow-list.  The
# much tighter semantic masks below are authoritative.
FACE_BOUNDS = (330, 195, 675, 490)  # left, top, right, bottom (exclusive)
FACE_CONTACT_CROP = (275, 130, 730, 585)

# Strict semantic layer geometry.  Brows and eyes deliberately have independent
# masks: one generous eye+brow oval admitted the skin bridge, nose fragments,
# and pieces of Sam's bangs visible in the rejected 2026-08-22 layer sheets.
# The radii include only a roughly two-pixel antialiasing allowance around the
# sparse exporter masks.  Any non-zero alpha outside these masks is a failure.
FACE_INTERIOR_ELLIPSE = (493.0, 329.0, 123.0, 125.0)
BROW_ELLIPSES = (
    (426.0, 269.0, 56.0, 15.0, -17.0),
    (535.0, 250.0, 56.0, 15.0, -17.0),
)
EYE_ELLIPSES = (
    (427.0, 305.0, 54.0, 29.0),
    (539.0, 285.0, 55.0, 29.0),
)
IRIS_CORE_ELLIPSES = (
    (429.0, 298.0, 34.0, 27.0),
    (539.0, 281.0, 34.0, 27.0),
)
MOUTH_ELLIPSE = (498.0, 378.0, 64.0, 32.0)
# The canonical neutral smile has one detached authored endpoint outside the
# alternate-expression mouth oval.  This lobe is neutral-only so generated
# expressions cannot use it as a route into the nose/cheek area.
NEUTRAL_MOUTH_CORNER_ELLIPSE = (543.0, 360.0, 18.0, 6.0, -55.0)
NOSE_ELLIPSE = (490.0, 343.0, 25.0, 37.0)
TEAR_ELLIPSES = (
    (427.0, 351.0, 33.0, 65.0),
    (548.0, 336.0, 33.0, 65.0),
)
CHEEK_ELLIPSES = (
    (415.0, 354.0, 62.0, 41.0),
    (565.0, 338.0, 62.0, 41.0),
)
# Blush is the only intentionally broad paint in a face layer.  It must remain
# translucent, red-biased, and small in equivalent opaque area.  These limits
# tolerate soft six-sigma feathering while rejecting an opaque cheek/skin plate.
BLUSH_ALPHA_LIMIT = 64
BLUSH_VISIBLE_PIXEL_LIMIT = 9_000
BLUSH_EQUIVALENT_OPAQUE_LIMIT = 1_250.0
TEAR_EXPRESSIONS = {"crying"}
BLUSH_EXPRESSIONS = {
    "crying",
    "embarrassed",
    "nervous",
    "worried",
    "afraid",
    "panicked",
}

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
    original_name: str
    base_name: str
    neutral_layer_name: str

    def expression_name(self, expression: str) -> str:
        return f"face_{expression}_{self.name}.png"


@dataclass(frozen=True)
class PoseSpec:
    attribute: str
    outfit: str
    filename: str


OUTFITS = (
    OutfitSpec(
        name="casual",
        original_name="neutral.png",
        base_name="neut_face_base.png",
        neutral_layer_name="face_neut_casual.png",
    ),
    OutfitSpec(
        name="uniform",
        original_name="neut_uniform.png",
        base_name="neut_uniform_face_base.png",
        neutral_layer_name="face_neut_uniform.png",
    ),
)

POSES = (
    PoseSpec("pose_open_hand", "casual", "pose_open_hand_casual.png"),
    PoseSpec("pose_crossed", "uniform", "pose_crossed_uniform.png"),
    PoseSpec("pose_thinking", "uniform", "pose_thinking_uniform.png"),
    PoseSpec("pose_phone", "casual", "pose_phone_casual.png"),
)

# The generator checker is nearly white, as are Sam's rolled uniform cuffs. A
# matte extractor once classified the cuffs as background, leaving holes that
# were invisible on light but obvious on dark/checker. These canonical-stage
# probes cover cuff cores (not silhouette edges), so they catch that regression
# without rejecting intentional negative space between limbs.
POSE_PALE_INTERIOR_PROBES = {
    "pose_crossed_uniform.png": (
        ("viewer-left rolled cuff", (180, 815, 300, 990)),
        ("viewer-right rolled cuff", (390, 880, 520, 1035)),
    ),
    "pose_thinking_uniform.png": (
        ("raised-arm rolled cuff", (490, 695, 655, 845)),
        ("folded-arm rolled cuff", (205, 850, 340, 1020)),
    ),
}


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
    names = {
        outfit.original_name
        for outfit in OUTFITS
    }
    names.update(outfit.base_name for outfit in OUTFITS)
    names.update(outfit.neutral_layer_name for outfit in OUTFITS)
    names.update(
        outfit.expression_name(expression)
        for outfit in OUTFITS
        for expression in EXPRESSIONS
    )
    names.update(pose.filename for pose in POSES)
    return names


def mask_bbox(mask: np.ndarray) -> tuple[int, int, int, int] | None:
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def format_bbox(bounds: tuple[int, int, int, int] | None) -> str:
    if bounds is None:
        return "empty"
    left, top, right, bottom = bounds
    return f"({left},{top})-({right},{bottom})"


def changed_mask(first: np.ndarray, second: np.ndarray) -> np.ndarray:
    return np.any(first != second, axis=2)


def alpha_composite(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    return np.asarray(
        Image.alpha_composite(Image.fromarray(base, "RGBA"), Image.fromarray(overlay, "RGBA"))
    ).copy()


@lru_cache(maxsize=None)
def face_region_mask() -> np.ndarray:
    left, top, right, bottom = FACE_BOUNDS
    region = np.zeros((CANVAS_SIZE[1], CANVAS_SIZE[0]), dtype=bool)
    region[top:bottom, left:right] = True
    return region


@lru_cache(maxsize=None)
def ellipse_mask(spec: tuple[float, float, float, float]) -> np.ndarray:
    center_x, center_y, radius_x, radius_y = spec
    y_grid, x_grid = np.ogrid[: CANVAS_SIZE[1], : CANVAS_SIZE[0]]
    return (
        ((x_grid - center_x) / radius_x) ** 2
        + ((y_grid - center_y) / radius_y) ** 2
        <= 1.0
    )


@lru_cache(maxsize=None)
def rotated_ellipse_mask(
    spec: tuple[float, float, float, float, float]
) -> np.ndarray:
    center_x, center_y, radius_x, radius_y, angle_degrees = spec
    y_grid, x_grid = np.ogrid[: CANVAS_SIZE[1], : CANVAS_SIZE[0]]
    x_delta = x_grid - center_x
    y_delta = y_grid - center_y
    angle = math.radians(angle_degrees)
    cosine = math.cos(angle)
    sine = math.sin(angle)
    rotated_x = cosine * x_delta + sine * y_delta
    rotated_y = -sine * x_delta + cosine * y_delta
    return (rotated_x / radius_x) ** 2 + (rotated_y / radius_y) ** 2 <= 1.0


@lru_cache(maxsize=None)
def union_ellipses(
    specs: tuple[tuple[float, float, float, float], ...]
) -> np.ndarray:
    region = np.zeros((CANVAS_SIZE[1], CANVAS_SIZE[0]), dtype=bool)
    for spec in specs:
        region |= ellipse_mask(spec)
    return region


@lru_cache(maxsize=None)
def brow_expression_region() -> np.ndarray:
    brows = np.zeros((CANVAS_SIZE[1], CANVAS_SIZE[0]), dtype=bool)
    for spec in BROW_ELLIPSES:
        brows |= rotated_ellipse_mask(spec)
    return brows


@lru_cache(maxsize=None)
def core_expression_region() -> np.ndarray:
    return (
        brow_expression_region()
        | union_ellipses(EYE_ELLIPSES)
        | ellipse_mask(MOUTH_ELLIPSE)
    )


@lru_cache(maxsize=None)
def tear_expression_region() -> np.ndarray:
    y_grid, _ = np.indices((CANVAS_SIZE[1], CANVAS_SIZE[0]))
    return (
        union_ellipses(TEAR_ELLIPSES)
        & (y_grid >= 292)
        & ellipse_mask(FACE_INTERIOR_ELLIPSE)
        & ~ellipse_mask(NOSE_ELLIPSE)
    )


@lru_cache(maxsize=None)
def blush_expression_region() -> np.ndarray:
    return (
        union_ellipses(CHEEK_ELLIPSES)
        & ellipse_mask(FACE_INTERIOR_ELLIPSE)
        & ~ellipse_mask(NOSE_ELLIPSE)
    )


@lru_cache(maxsize=None)
def allowed_expression_region(expression: str) -> np.ndarray:
    # Never mutate the cached core mask while adding emotion-specific regions.
    allowed = core_expression_region().copy()
    if expression == "neut":
        allowed |= rotated_ellipse_mask(NEUTRAL_MOUTH_CORNER_ELLIPSE)
    if expression in TEAR_EXPRESSIONS:
        allowed |= tear_expression_region()
    if expression in BLUSH_EXPRESSIONS:
        allowed |= blush_expression_region()
    allowed &= ellipse_mask(FACE_INTERIOR_ELLIPSE)
    allowed &= ~ellipse_mask(NOSE_ELLIPSE)
    return allowed


def dilate_mask(mask: np.ndarray, radius: int) -> np.ndarray:
    """Dilate a boolean mask with a small square kernel using NumPy only."""

    if radius <= 0:
        return mask.copy()
    padded = np.pad(mask, radius, mode="constant", constant_values=False)
    result = np.zeros_like(mask)
    height, width = mask.shape
    for y_offset in range(radius * 2 + 1):
        for x_offset in range(radius * 2 + 1):
            result |= padded[
                y_offset : y_offset + height,
                x_offset : x_offset + width,
            ]
    return result


def protected_native_hair(neutral: np.ndarray) -> np.ndarray:
    """Conservatively identify bright golden hair in the original neutral."""

    rgb = neutral[:, :, :3].astype(np.int16)
    red, green, blue = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    feature_exemptions = (
        union_ellipses(IRIS_CORE_ELLIPSES) | brow_expression_region()
    )
    hair = (
        (neutral[:, :, 3] == 255)
        & (red >= 120)
        & ((red - blue) >= 100)
        & ((green - blue) >= 38)
        & ((red - green) >= 20)
        & ~feature_exemptions
    )
    # Amber irises and the warm-gold canonical brows share part of the hair
    # palette and are legitimate expression ink.  Only those strict feature
    # masks are exempt.  A one-pixel halo protects the dark/antialiased edge of
    # each surrounding bang without clipping the brows themselves.
    protected = dilate_mask(hair, radius=1)
    return protected & ~feature_exemptions


def skin_fragment_mask(layer: np.ndarray) -> np.ndarray:
    rgb = layer[:, :, :3].astype(np.int16)
    red, green, blue = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    return (
        (layer[:, :, 3] >= 160)
        & (red >= 145)
        & (green >= 90)
        & (blue >= 70)
        & (red >= green)
        & (green >= blue - 8)
        & ((red - blue) >= 20)
        & ((red - blue) <= 135)
    )


def cyan_artifact_mask(layer: np.ndarray) -> np.ndarray:
    """Return saturated cyan/blue-green generator residue.

    Near-white sclera/tears can have tiny channel imbalances, so this requires
    both cool channels to dominate red materially.  Sam's canonical facial
    palette contains no such colors.
    """

    rgb = layer[:, :, :3].astype(np.int16)
    red, green, blue = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    return (
        (layer[:, :, 3] > 0)
        & (green >= 72)
        & (blue >= 72)
        & ((green - red) >= 18)
        & ((blue - red) >= 18)
    )


def load_production_pngs(
    sprite_root: Path,
    report: ValidationReport,
    *,
    canonical_root: Path | None = None,
    pose_root: Path | None = None,
) -> dict[str, np.ndarray]:
    required = expected_filenames()
    present_paths = {path.name: path for path in sprite_root.glob("*.png")}
    if canonical_root is not None:
        for outfit in OUTFITS:
            path = canonical_root / outfit.original_name
            if path.is_file():
                present_paths[outfit.original_name] = path
    if pose_root is not None:
        for pose in POSES:
            path = pose_root / pose.filename
            if path.is_file():
                present_paths[pose.filename] = path
    missing = sorted(required - set(present_paths))
    if missing:
        report.error(
            f"{sprite_root}: missing {len(missing)} required production PNG(s):\n"
            + "\n".join(f"  - {name}" for name in missing)
        )

    images: dict[str, np.ndarray] = {}
    for name, path in sorted(present_paths.items()):
        try:
            with Image.open(path) as image:
                report.check(
                    image.format == "PNG",
                    f"{path}: format is {image.format!r}, expected PNG",
                )
                canvas_is_valid = report.check(
                    image.size == CANVAS_SIZE,
                    f"{path}: canvas is {image.size}, expected {CANVAS_SIZE}",
                )
                report.check(
                    image.mode == "RGBA",
                    f"{path}: mode is {image.mode!r}, expected stored RGBA",
                )
                rgba = np.asarray(image.convert("RGBA")).copy()
        except (OSError, ValueError) as exc:
            report.error(f"{path}: cannot decode PNG: {exc}")
            continue

        alpha = rgba[:, :, 3]
        hidden_rgb = (alpha == 0) & np.any(rgba[:, :, :3] != 0, axis=2)
        if hidden_rgb.any():
            first_y, first_x = np.argwhere(hidden_rgb)[0]
            report.error(
                f"{path}: {int(hidden_rgb.sum())} fully transparent pixels retain RGB "
                f"(first at x={int(first_x)}, y={int(first_y)}); hidden RGB must be zero"
            )

        # Downstream checks assume one common authoring canvas.  Keep reporting
        # hygiene above, but do not let one malformed file trigger a misleading
        # NumPy broadcast traceback later.
        if canvas_is_valid:
            images[name] = rgba

    return images


def rectangle_signature(alpha: np.ndarray) -> tuple[bool, str]:
    """Identify a large, nearly solid axis-aligned alpha plate.

    Real eye/brow/mouth masks are sparse, and even a whole feathered face patch
    has curved sides.  A generator-preview rectangle instead has a large opaque
    core whose bounding box is almost completely filled on every edge.
    """

    opaque = alpha >= 250
    bounds = mask_bbox(opaque)
    if bounds is None:
        return False, "no opaque pixels"

    left, top, right, bottom = bounds
    width = right - left
    height = bottom - top
    crop = opaque[top:bottom, left:right]
    area = width * height
    fill_ratio = float(crop.mean())
    strip = max(1, min(3, width // 4, height // 4))
    edge_fill = min(
        float(crop[:strip, :].mean()),
        float(crop[-strip:, :].mean()),
        float(crop[:, :strip].mean()),
        float(crop[:, -strip:].mean()),
    )
    suspicious = (
        width >= 90
        and height >= 65
        and area >= 10_000
        and fill_ratio >= 0.88
        and edge_fill >= 0.62
    )
    detail = (
        f"opaque_bbox={format_bbox(bounds)}, fill={fill_ratio:.3f}, "
        f"edge_fill={edge_fill:.3f}"
    )
    return suspicious, detail


def connected_component_summary(mask: np.ndarray) -> tuple[int, int]:
    """Return (component count, largest area) using 8-way connectivity.

    Face masks are confined to a small authoring box, so a local flood fill is
    fast and avoids making this validator depend on OpenCV merely for one QA
    statistic. A legitimate feature layer is split among eyes, brows, mouth,
    tears, and blush; a ghosted face plate tends to bridge most of them into one
    dominant component.
    """

    bounds = mask_bbox(mask)
    if bounds is None:
        return 0, 0
    left, top, right, bottom = bounds
    crop = mask[top:bottom, left:right]
    visited = np.zeros_like(crop)
    component_count = 0
    largest_area = 0
    height, width = crop.shape

    for start_y, start_x in np.argwhere(crop):
        y = int(start_y)
        x = int(start_x)
        if visited[y, x]:
            continue
        component_count += 1
        visited[y, x] = True
        stack = [(y, x)]
        area = 0
        while stack:
            current_y, current_x = stack.pop()
            area += 1
            for neighbor_y in range(max(0, current_y - 1), min(height, current_y + 2)):
                for neighbor_x in range(max(0, current_x - 1), min(width, current_x + 2)):
                    if (
                        not visited[neighbor_y, neighbor_x]
                        and crop[neighbor_y, neighbor_x]
                    ):
                        visited[neighbor_y, neighbor_x] = True
                        stack.append((neighbor_y, neighbor_x))
        largest_area = max(largest_area, area)

    return component_count, largest_area


def shifted_correlation(
    values: np.ndarray,
    support: np.ndarray,
    dy: int,
    dx: int,
) -> float | None:
    height, width = support.shape
    if abs(dy) >= height or abs(dx) >= width:
        return None

    if dy >= 0:
        first_y = slice(0, height - dy)
        second_y = slice(dy, height)
    else:
        first_y = slice(-dy, height)
        second_y = slice(0, height + dy)
    if dx >= 0:
        first_x = slice(0, width - dx)
        second_x = slice(dx, width)
    else:
        first_x = slice(-dx, width)
        second_x = slice(0, width + dx)

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


def checker_periodicity_score(
    composite: np.ndarray,
    neutral: np.ndarray,
    support: np.ndarray,
) -> tuple[float, int | None]:
    """Return evidence for an axis-aligned checker baked into changed pixels.

    A checker reverses sign after one tile and repeats after two tiles in *both*
    axes.  Requiring all four correlations keeps ordinary eyes, line art, and
    horizontal blush strokes from being mistaken for a grid.
    """

    if int(support.sum()) < 2_000:
        return 0.0, None

    bounds = mask_bbox(support)
    if bounds is None:
        return 0.0, None
    left, top, right, bottom = bounds
    composite = composite[top:bottom, left:right]
    neutral = neutral[top:bottom, left:right]
    support = support[top:bottom, left:right]

    rgb_weights = np.array((0.2126, 0.7152, 0.0722), dtype=np.float32)
    difference = (
        composite[:, :, :3].astype(np.float32) - neutral[:, :, :3].astype(np.float32)
    ) @ rgb_weights
    if float(difference[support].std()) < 0.35:
        return 0.0, None

    best_score = 0.0
    best_tile: int | None = None
    for tile in range(3, 33):
        correlations = (
            shifted_correlation(difference, support, 0, tile),
            shifted_correlation(difference, support, tile, 0),
            shifted_correlation(difference, support, 0, tile * 2),
            shifted_correlation(difference, support, tile * 2, 0),
        )
        if any(value is None for value in correlations):
            continue
        horizontal_flip, vertical_flip, horizontal_repeat, vertical_repeat = correlations
        score = min(
            -float(horizontal_flip),
            -float(vertical_flip),
            float(horizontal_repeat),
            float(vertical_repeat),
        )
        if score > best_score:
            best_score = score
            best_tile = tile
    return max(0.0, best_score), best_tile


def validate_face_layer(
    *,
    label: str,
    expression: str,
    layer: np.ndarray,
    base: np.ndarray,
    neutral: np.ndarray,
    report: ValidationReport,
    require_distinct_expression: bool,
) -> tuple[np.ndarray, np.ndarray]:
    alpha = layer[:, :, 3]
    visible = alpha > 0
    visible_count = int(visible.sum())
    bounds = mask_bbox(visible)
    region = face_region_mask()

    report.check(visible_count >= 100, f"{label}: face layer is empty or implausibly small ({visible_count} pixels)")
    report.check(
        visible_count <= 80_000,
        f"{label}: face layer covers {visible_count} pixels; expected contained feature ink, not a broad patch",
    )
    outside_count = int((visible & ~region).sum())
    report.check(
        outside_count == 0,
        f"{label}: {outside_count} visible layer pixels escape face bounds {FACE_BOUNDS}; bbox={format_bbox(bounds)}",
    )
    semantic_region = allowed_expression_region(expression)
    outside_semantic = visible & ~semantic_region
    outside_semantic_count = int(outside_semantic.sum())
    report.check(
        outside_semantic_count == 0,
        f"{label}: {outside_semantic_count} layer pixels escape the strict "
        "brow/eye/mouth masks (only crying tears and controlled blush are "
        f"allowed); forbidden bbox={format_bbox(mask_bbox(outside_semantic))}",
    )
    hair_overlap_count = int((visible & protected_native_hair(neutral)).sum())
    report.check(
        hair_overlap_count == 0,
        f"{label}: {hair_overlap_count} layer pixels repaint native bangs/hair; hair must remain on the base",
    )
    nonopaque_base = int((visible & (base[:, :, 3] != 255)).sum())
    report.check(
        nonopaque_base == 0,
        f"{label}: {nonopaque_base} layer pixels land outside Sam's fully opaque facial interior",
    )

    core_region = core_expression_region()
    tear_region = tear_expression_region() if expression in TEAR_EXPRESSIONS else np.zeros_like(visible)
    if expression in BLUSH_EXPRESSIONS:
        # Eye/mouth/tear pixels may legitimately be opaque where the cheek masks
        # overlap them.  Only cheek-exclusive paint is subject to blush limits.
        blush_only = visible & blush_expression_region() & ~core_region & ~tear_region
        blush_count = int(blush_only.sum())
        blush_alpha = alpha[blush_only]
        blush_max_alpha = int(blush_alpha.max()) if blush_alpha.size else 0
        blush_equivalent_opaque = float(blush_alpha.astype(np.float64).sum() / 255.0)
        report.check(
            blush_count <= BLUSH_VISIBLE_PIXEL_LIMIT,
            f"{label}: blush covers {blush_count} cheek-only pixels; limit is "
            f"{BLUSH_VISIBLE_PIXEL_LIMIT}",
        )
        report.check(
            blush_max_alpha <= BLUSH_ALPHA_LIMIT,
            f"{label}: cheek-only blush reaches alpha {blush_max_alpha}; "
            f"controlled blush must remain <= {BLUSH_ALPHA_LIMIT}",
        )
        report.check(
            blush_equivalent_opaque <= BLUSH_EQUIVALENT_OPAQUE_LIMIT,
            f"{label}: blush equivalent opaque area is {blush_equivalent_opaque:.1f} "
            f"pixels; limit is {BLUSH_EQUIVALENT_OPAQUE_LIMIT:.1f}",
        )
        layer_values = layer[:, :, :3].astype(np.int16)
        red = layer_values[:, :, 0]
        green = layer_values[:, :, 1]
        blue = layer_values[:, :, 2]
        material_blush = blush_only & (alpha >= 4)
        non_red_blush = material_blush & (
            (red < green + 12) | (red < blue + 8)
        )
        non_red_blush_count = int(non_red_blush.sum())
        material_blush_count = int(material_blush.sum())
        report.check(
            non_red_blush_count <= max(64, math.ceil(material_blush_count * 0.02)),
            f"{label}: {non_red_blush_count}/{material_blush_count} material "
            "cheek-only blush pixels are not red-biased; likely a skin/checker patch",
        )
    else:
        blush_count = 0
        blush_max_alpha = 0
        blush_equivalent_opaque = 0.0

    rectangle, rectangle_detail = rectangle_signature(alpha)
    report.check(
        not rectangle,
        f"{label}: broad opaque rectangle detected ({rectangle_detail})",
    )

    composite = alpha_composite(base, layer)
    report.check(
        np.array_equal(composite[:, :, 3], base[:, :, 3]),
        f"{label}: compositing changes the base silhouette",
    )
    changed_from_base = changed_mask(composite, base)
    effective_count = int(changed_from_base.sum())
    report.check(
        effective_count >= 100,
        f"{label}: only {effective_count} pixels have a visible effect after compositing",
    )
    if visible_count:
        effective_ratio = effective_count / visible_count
        report.check(
            effective_ratio >= 0.12,
            f"{label}: only {effective_ratio:.1%} of its alpha footprint changes the base; likely a padded face plate",
        )
    else:
        effective_ratio = 0.0

    changed_from_neutral = changed_mask(composite, neutral)
    changed_outside = int((changed_from_neutral & ~region).sum())
    report.check(
        changed_outside == 0,
        f"{label}: composite changes {changed_outside} pixels outside the contained face region",
    )
    if require_distinct_expression:
        report.check(
            int(changed_from_neutral.sum()) >= 100,
            f"{label}: alternate expression is effectively identical to the original neutral",
        )

    component_count, largest_component = connected_component_summary(visible)
    largest_component_ratio = largest_component / max(1, visible_count)
    layer_rgb = layer[:, :, :3].astype(np.int16)
    cool_artifact = visible & (
        ((layer_rgb[:, :, 2] - layer_rgb[:, :, 0]) >= 18)
        | ((layer_rgb[:, :, 1] - layer_rgb[:, :, 0]) >= 18)
    )
    cool_artifact_count = int(cool_artifact.sum())
    cool_artifact_ratio = cool_artifact_count / max(1, visible_count)
    pale_ink = visible & (layer_rgb.min(axis=2) >= 225)
    pale_ink_count = int(pale_ink.sum())
    pale_ink_ratio = pale_ink_count / max(1, visible_count)

    cyan_artifact = cyan_artifact_mask(layer)
    cyan_artifact_count = int(cyan_artifact.sum())
    report.check(
        cyan_artifact_count <= 8,
        f"{label}: {cyan_artifact_count} visible pixels contain non-native "
        f"cyan/blue-green generator residue; bbox={format_bbox(mask_bbox(cyan_artifact))}",
    )

    # Exempt the compact amber iris cores from a generic warm-skin classifier.
    # Everywhere else, a large opaque skin-colored footprint means the donor's
    # face plate was exported instead of sparse feature ink.
    skin_fragments = (
        skin_fragment_mask(layer)
        & visible
        & core_region
        & ~union_ellipses(IRIS_CORE_ELLIPSES)
    )
    core_visible = visible & core_region
    skin_fragment_count = int(skin_fragments.sum())
    skin_fragment_ratio = skin_fragment_count / max(1, int(core_visible.sum()))
    skin_count_limit = 4_500 if not require_distinct_expression else 3_000
    skin_ratio_limit = 0.50 if not require_distinct_expression else 0.42
    report.check(
        skin_fragment_count <= skin_count_limit
        and skin_fragment_ratio <= skin_ratio_limit,
        f"{label}: broad opaque skin fragments cover {skin_fragment_count} core "
        f"pixels ({skin_fragment_ratio:.1%}); limits are {skin_count_limit} pixels "
        f"and {skin_ratio_limit:.0%}",
    )

    if require_distinct_expression:
        report.check(
            largest_component_ratio <= 0.72,
            f"{label}: one connected alpha region contains {largest_component_ratio:.1%} "
            f"of the layer ({largest_component}/{visible_count}); likely a ghosted face plate",
        )
        # Sam's native facial palette is warm brown/amber. Cyan generator
        # outlines are not present even in tears or eye highlights, while small
        # antialiasing fluctuations remain below both limits here.
        report.check(
            cool_artifact_count <= 100 or cool_artifact_ratio <= 0.008,
            f"{label}: non-native cyan/cool linework covers {cool_artifact_count} pixels "
            f"({cool_artifact_ratio:.2%} of the layer)",
        )
        report.check(
            pale_ink_ratio <= 0.35,
            f"{label}: pale/white ink covers {pale_ink_count} pixels "
            f"({pale_ink_ratio:.2%}); likely a white generator outline or matte",
        )

    checker_score, checker_tile = checker_periodicity_score(
        composite,
        neutral,
        visible & region,
    )
    report.check(
        checker_score < 0.28,
        f"{label}: checker-like two-axis periodicity detected "
        f"(score={checker_score:.3f}, estimated tile={checker_tile}px)",
    )
    report.note(
        f"{label}: bbox={format_bbox(bounds)} visible={visible_count} "
        f"effective={effective_count} ({effective_ratio:.1%}) checker={checker_score:.3f} "
        f"largest_component={largest_component_ratio:.1%}/{component_count} "
        f"cool={cool_artifact_ratio:.2%} cyan={cyan_artifact_count} pale={pale_ink_ratio:.2%} "
        f"outside_semantic={outside_semantic_count} hair={hair_overlap_count} "
        f"skin={skin_fragment_count}/{skin_fragment_ratio:.1%} "
        f"blush={blush_count}/{blush_max_alpha}/{blush_equivalent_opaque:.1f}eq"
    )
    return composite, visible


def validate_outfit_bases(
    images: dict[str, np.ndarray], report: ValidationReport
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray]]:
    originals: dict[str, np.ndarray] = {}
    bases: dict[str, np.ndarray] = {}
    region = face_region_mask()

    for outfit in OUTFITS:
        required = (
            outfit.original_name,
            outfit.base_name,
            outfit.neutral_layer_name,
        )
        if any(name not in images for name in required):
            continue
        original = images[outfit.original_name]
        base = images[outfit.base_name]
        neutral_layer = images[outfit.neutral_layer_name]
        originals[outfit.name] = original
        bases[outfit.name] = base

        report.check(
            np.array_equal(base[:, :, 3], original[:, :, 3]),
            f"sam/{outfit.name}: featureless base does not preserve the original alpha silhouette exactly",
        )
        base_changes = changed_mask(base, original)
        outside_changes = int((base_changes & ~region).sum())
        report.check(
            outside_changes == 0,
            f"sam/{outfit.name}: featureless base changes {outside_changes} pixels outside face bounds {FACE_BOUNDS}",
        )
        outside_neutral_features = int(
            (base_changes & ~allowed_expression_region("neut")).sum()
        )
        report.check(
            outside_neutral_features == 0,
            f"sam/{outfit.name}: featureless base changes {outside_neutral_features} pixels "
            "outside the neutral eye/brow + mouth zones (hair, nose, jaw, chin, "
            "ears, and face perimeter must remain exact)",
        )
        base_hair_changes = int((base_changes & protected_native_hair(original)).sum())
        report.check(
            base_hair_changes == 0,
            f"sam/{outfit.name}: featureless base alters {base_hair_changes} native hair pixels",
        )
        changed_count = int(base_changes.sum())
        report.check(
            500 <= changed_count <= 80_000,
            f"sam/{outfit.name}: implausible featureless-base edit area ({changed_count} pixels)",
        )

        reconstructed, _ = validate_face_layer(
            label=f"sam/{outfit.name}/neut",
            expression="neut",
            layer=neutral_layer,
            base=base,
            neutral=original,
            report=report,
            require_distinct_expression=False,
        )
        reconstruction_changes = changed_mask(reconstructed, original)
        if reconstruction_changes.any():
            report.error(
                f"sam {outfit.name if outfit.name != 'casual' else ''} neut".replace("  ", " ")
                + f": base + neutral layer differs from the original at "
                f"{int(reconstruction_changes.sum())} pixels; diff bbox="
                f"{format_bbox(mask_bbox(reconstruction_changes))}"
            )
        report.note(
            f"sam/{outfit.name}/base: changed={changed_count} "
            f"bbox={format_bbox(mask_bbox(base_changes))}; exact neutral reconstruction="
            f"{'yes' if not reconstruction_changes.any() else 'NO'}"
        )

    return originals, bases


def validate_expression_bank(
    images: dict[str, np.ndarray],
    originals: dict[str, np.ndarray],
    bases: dict[str, np.ndarray],
    report: ValidationReport,
) -> set[tuple[str, str]]:
    validated: set[tuple[str, str]] = set()

    for expression in EXPRESSIONS:
        expression_masks: dict[str, np.ndarray] = {}
        for outfit in OUTFITS:
            filename = outfit.expression_name(expression)
            if (
                filename not in images
                or outfit.name not in originals
                or outfit.name not in bases
            ):
                continue
            _, visible = validate_face_layer(
                label=f"sam/{outfit.name}/{expression}",
                expression=expression,
                layer=images[filename],
                base=bases[outfit.name],
                neutral=originals[outfit.name],
                report=report,
                require_distinct_expression=True,
            )
            validated.add((outfit.name, expression))
            expression_masks[outfit.name] = visible

        if "casual" not in expression_masks or "uniform" not in expression_masks:
            continue
        casual = expression_masks["casual"]
        uniform = expression_masks["uniform"]
        casual_bbox = mask_bbox(casual)
        uniform_bbox = mask_bbox(uniform)
        if casual_bbox is None or uniform_bbox is None:
            continue

        casual_area = int(casual.sum())
        uniform_area = int(uniform.sum())
        area_ratio = max(casual_area, uniform_area) / max(1, min(casual_area, uniform_area))
        casual_y, casual_x = np.nonzero(casual)
        uniform_y, uniform_x = np.nonzero(uniform)
        centroid_distance = math.hypot(
            float(casual_x.mean() - uniform_x.mean()),
            float(casual_y.mean() - uniform_y.mean()),
        )
        bbox_delta = max(
            abs(casual_bbox[index] - uniform_bbox[index]) for index in range(4)
        )
        intersection = int((casual & uniform).sum())
        union = int((casual | uniform).sum())
        iou = intersection / max(1, union)

        report.check(
            area_ratio <= 1.80,
            f"sam/{expression}: casual/uniform layer areas diverge by {area_ratio:.2f}x",
        )
        report.check(
            centroid_distance <= 15.0,
            f"sam/{expression}: casual/uniform layer centroids are {centroid_distance:.1f}px apart",
        )
        report.check(
            bbox_delta <= 24,
            f"sam/{expression}: casual/uniform face bboxes differ by up to {bbox_delta}px "
            f"({format_bbox(casual_bbox)} vs {format_bbox(uniform_bbox)})",
        )
        report.check(
            iou >= 0.35,
            f"sam/{expression}: casual/uniform masks overlap poorly (IoU={iou:.3f}); likely misregistered",
        )

    return validated


def silhouette_boundary(visible: np.ndarray) -> np.ndarray:
    outside = ~visible
    adjacent_outside = np.zeros_like(visible)
    adjacent_outside[1:, :] |= outside[:-1, :]
    adjacent_outside[:-1, :] |= outside[1:, :]
    adjacent_outside[:, 1:] |= outside[:, :-1]
    adjacent_outside[:, :-1] |= outside[:, 1:]
    return visible & adjacent_outside


def validate_poses(images: dict[str, np.ndarray], report: ValidationReport) -> None:
    width, height = CANVAS_SIZE
    for pose in POSES:
        if pose.filename not in images:
            continue
        rgba = images[pose.filename]
        alpha = rgba[:, :, 3]
        visible = alpha > 0
        bounds = mask_bbox(visible)
        if bounds is None:
            report.error(f"sam/{pose.attribute}: pose is fully transparent")
            continue
        left, top, right, bottom = bounds
        report.check(
            left > 0 and right < width,
            f"sam/{pose.attribute}: horizontal crop/edge contact at bbox={format_bbox(bounds)}",
        )
        report.check(
            top > 0,
            f"sam/{pose.attribute}: top crop/edge contact at bbox={format_bbox(bounds)}",
        )
        # bottom == height is explicitly valid: all original full-body sprites sit
        # on the bottom edge of the authoring canvas.

        visible_count = int(visible.sum())
        soft = visible & (alpha < 255)
        soft_count = int(soft.sum())
        soft_ratio = soft_count / max(1, visible_count)
        boundary = silhouette_boundary(visible)
        boundary_count = int(boundary.sum())
        soft_boundary_ratio = int((boundary & (alpha < 250)).sum()) / max(1, boundary_count)

        rgb = rgba[:, :, :3]
        neutral_white = (
            (rgb.min(axis=2) >= 235)
            & ((rgb.max(axis=2).astype(np.int16) - rgb.min(axis=2).astype(np.int16)) <= 15)
        )
        fringe_support = soft & (alpha < 250)
        fringe_count = int(fringe_support.sum())
        white_fringe_count = int((fringe_support & neutral_white).sum())
        white_fringe_ratio = white_fringe_count / max(1, fringe_count)

        report.check(
            visible_count >= 50_000,
            f"sam/{pose.attribute}: implausibly small visible silhouette ({visible_count} pixels)",
        )
        report.check(
            soft_count >= 500 and 0.001 <= soft_ratio <= 0.12,
            f"sam/{pose.attribute}: unhealthy soft-alpha coverage "
            f"({soft_count} pixels, {soft_ratio:.3%} of visible art)",
        )
        report.check(
            soft_boundary_ratio >= 0.35,
            f"sam/{pose.attribute}: only {soft_boundary_ratio:.1%} of the outer boundary is softened; likely hard-cut",
        )
        report.check(
            white_fringe_count < 150 or white_fringe_ratio < 0.025,
            f"sam/{pose.attribute}: likely white matte fringe "
            f"({white_fringe_count}/{fringe_count}, {white_fringe_ratio:.2%})",
        )
        probe_notes: list[str] = []
        rgb_values = rgb.astype(np.int16)
        pale_clothing = (
            visible
            & (rgb_values.min(axis=2) >= 155)
            & ((rgb_values.max(axis=2) - rgb_values.min(axis=2)) <= 105)
        )
        for probe_label, (probe_left, probe_top, probe_right, probe_bottom) in (
            POSE_PALE_INTERIOR_PROBES.get(pose.filename, ())
        ):
            probe_alpha = alpha[probe_top:probe_bottom, probe_left:probe_right]
            probe_area = probe_alpha.size
            transparent_count = int((probe_alpha == 0).sum())
            transparent_ratio = transparent_count / max(1, probe_area)
            pale_count = int(
                pale_clothing[probe_top:probe_bottom, probe_left:probe_right].sum()
            )
            report.check(
                transparent_ratio <= 0.06,
                f"sam/{pose.attribute}: {probe_label} contains {transparent_count} "
                f"transparent pixels ({transparent_ratio:.1%}); likely a checker-extraction hole",
            )
            report.check(
                pale_count >= 2_000,
                f"sam/{pose.attribute}: {probe_label} retains only {pale_count} pale clothing "
                "pixels; the white cuff may have been removed with the checker",
            )
            probe_notes.append(
                f"{probe_label} transparent={transparent_ratio:.1%} pale={pale_count}"
            )
        report.note(
            f"sam/{pose.attribute}: bbox={format_bbox(bounds)} soft={soft_count} "
            f"({soft_ratio:.3%}) soft_boundary={soft_boundary_ratio:.1%} "
            f"white_fringe={white_fringe_ratio:.2%} "
            f"bottom={'touches (allowed)' if bottom == height else f'margin {height - bottom}px'}"
            + (f"; {'; '.join(probe_notes)}" if probe_notes else "")
        )


def layeredimage_block(definition: str, tag: str) -> str | None:
    lines = definition.splitlines()
    start_pattern = re.compile(rf"^layeredimage\s+{re.escape(tag)}\s*:\s*$")
    start = next((index for index, line in enumerate(lines) if start_pattern.match(line)), None)
    if start is None:
        return None

    block = [lines[start]]
    for line in lines[start + 1 :]:
        stripped = line.strip()
        if stripped and not line.startswith((" ", "\t")) and not stripped.startswith("#"):
            break
        block.append(line)
    return "\n".join(block)


def validate_definitions(definition_path: Path, report: ValidationReport) -> None:
    if not definition_path.is_file():
        report.error(f"{definition_path}: def_characters.rpy not found")
        return
    try:
        definition = definition_path.read_text(encoding="utf-8")
    except OSError as exc:
        report.error(f"{definition_path}: cannot read definitions: {exc}")
        return

    referenced = {
        path.replace("\\", "/")
        for path in re.findall(
            r'["\'](mod_assets/char_sprites/[^"\'\n]+\.png)["\']',
            definition,
        )
        if "<" not in path
    }
    missing_references = sorted(
        path for path in referenced if not (PROJECT_ROOT / "game" / path).is_file()
    )
    if missing_references:
        report.error(
            f"{definition_path}: {len(missing_references)} referenced sprite file(s) do not exist:\n"
            + "\n".join(f"  - {path}" for path in missing_references)
        )
    report.note(f"def_characters.rpy: {len(referenced)} concrete sprite PNG references exist")

    block = layeredimage_block(definition, "sam")
    if block is None:
        report.error(f"{definition_path}: missing `layeredimage sam:` declaration")
        return
    report.check(
        re.search(r"\bat\s+sam_sprite_size\s*,\s*Flatten\b", block) is not None,
        f"{definition_path}: Sam layeredimage must use `at sam_sprite_size, Flatten`",
    )
    report.check(
        re.search(r"^transform\s+sam_sprite_size\s*:", definition, re.MULTILINE) is not None,
        f"{definition_path}: missing `transform sam_sprite_size:`",
    )
    report.check(
        re.search(r"^image\s+sam(?:\s+uniform)?\s+neut\s*=", definition, re.MULTILINE) is None,
        f"{definition_path}: legacy flattened `image sam [uniform] neut =` overrides remain",
    )

    for outfit in OUTFITS:
        base_path = f"mod_assets/char_sprites/masayami/{outfit.base_name}"
        base_pattern = re.compile(
            rf"attribute\s+{outfit.name}(?:\s+default)?\s*:\s*\n\s*"
            rf'"{re.escape(base_path)}"'
        )
        report.check(
            base_pattern.search(block) is not None,
            f"{definition_path}: Sam {outfit.name} outfit is not wired to {base_path}",
        )

        layers = (("neut", outfit.neutral_layer_name),) + tuple(
            (expression, outfit.expression_name(expression)) for expression in EXPRESSIONS
        )
        for attribute, filename in layers:
            asset_path = f"mod_assets/char_sprites/masayami/{filename}"
            attribute_pattern = re.compile(
                rf"attribute\s+{attribute}(?:\s+default)?\s+if_all\s+"
                rf'"{outfit.name}"\s*:\s*\n\s*"{re.escape(asset_path)}"'
            )
            report.check(
                attribute_pattern.search(block) is not None,
                f"{definition_path}: Sam `{outfit.name} {attribute}` is not conditioned to {asset_path}",
            )

    for pose in POSES:
        asset_path = f"mod_assets/char_sprites/masayami/{pose.filename}"
        pose_pattern = re.compile(
            rf"^image\s+sam\s+{pose.outfit}\s+{pose.attribute}\s*=\s*"
            rf'Transform\(\s*"{re.escape(asset_path)}"',
            re.MULTILINE,
        )
        report.check(
            pose_pattern.search(definition) is not None,
            f"{definition_path}: missing fixed pose declaration `sam {pose.outfit} {pose.attribute}` -> {asset_path}",
        )


@lru_cache(maxsize=None)
def load_font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # Pillow < 10 has no size argument.
        return ImageFont.load_default()


def make_background(kind: str, size: tuple[int, int]) -> Image.Image:
    if kind == "dark":
        return Image.new("RGBA", size, (22, 24, 31, 255))
    if kind == "light":
        return Image.new("RGBA", size, (239, 240, 244, 255))
    if kind != "checker":
        raise ValueError(f"unknown review background: {kind}")

    image = Image.new("RGBA", size, (206, 208, 214, 255))
    draw = ImageDraw.Draw(image)
    tile = 14
    for top in range(0, size[1], tile):
        for left in range(0, size[0], tile):
            if (left // tile + top // tile) % 2:
                draw.rectangle(
                    (left, top, left + tile - 1, top + tile - 1),
                    fill=(166, 169, 177, 255),
                )
    return image


def review_panel(sprite: np.ndarray, background_kind: str, footer: str) -> Image.Image:
    panel_size = (220, 306)
    art_height = 280
    panel = make_background(background_kind, panel_size)
    sprite_image = Image.fromarray(sprite, "RGBA")
    full = sprite_image.copy()
    full.thumbnail((202, art_height - 4), Image.Resampling.LANCZOS)
    panel.alpha_composite(
        full,
        ((panel_size[0] - full.width) // 2, art_height - full.height),
    )

    # The inset keeps subtle eye/mouth differences reviewable without sacrificing
    # the full-body framing check in the same panel.
    head = sprite_image.crop(FACE_CONTACT_CROP)
    head.thumbnail((92, 92), Image.Resampling.LANCZOS)
    inset = make_background(background_kind, (98, 98))
    inset.alpha_composite(head, ((98 - head.width) // 2, (98 - head.height) // 2))
    inset_draw = ImageDraw.Draw(inset)
    inset_draw.rectangle((0, 0, 97, 97), outline=(71, 210, 224, 255), width=2)
    panel.alpha_composite(inset, (panel_size[0] - 104, 8))

    draw = ImageDraw.Draw(panel)
    draw.rectangle((0, art_height, panel_size[0] - 1, panel_size[1] - 1), fill=(12, 14, 19, 235))
    draw.text(
        (panel_size[0] // 2, art_height + 12),
        footer,
        font=load_font(13),
        fill=(240, 243, 248, 255),
        anchor="mm",
    )
    draw.rectangle((0, 0, panel_size[0] - 1, panel_size[1] - 1), outline=(72, 77, 88, 255))
    return panel


def blank_review_panel(message: str) -> Image.Image:
    panel = Image.new("RGBA", (220, 306), (31, 34, 42, 255))
    draw = ImageDraw.Draw(panel)
    draw.line((0, 0, 219, 305), fill=(63, 68, 80, 255), width=2)
    draw.line((219, 0, 0, 305), fill=(63, 68, 80, 255), width=2)
    draw.text(
        (110, 153),
        message,
        font=load_font(14),
        fill=(150, 155, 168, 255),
        anchor="mm",
    )
    return panel


def build_contact_sheet(
    images: dict[str, np.ndarray],
    bases: dict[str, np.ndarray],
    validated_expressions: set[tuple[str, str]],
    output_path: Path,
) -> None:
    panel_width, panel_height = (220, 306)
    label_width = 150
    header_height = 104
    row_gap = 8
    pose_divider_height = 46
    columns = tuple(
        (outfit, background)
        for outfit in ("casual", "uniform")
        for background in ("dark", "light", "checker")
    )
    width = label_width + panel_width * len(columns)
    height = (
        header_height
        + len(ALL_EXPRESSIONS) * (panel_height + row_gap)
        + pose_divider_height
        + len(POSES) * (panel_height + row_gap)
    )
    sheet = Image.new("RGBA", (width, height), (16, 18, 24, 255))
    draw = ImageDraw.Draw(sheet)
    title_font = load_font(22)
    label_font = load_font(16)
    small_font = load_font(13)

    draw.text((18, 18), "SAM SPRITE REVIEW - 21 EXPRESSIONS x 2 OUTFITS + 4 POSES", font=title_font, fill=(240, 244, 250, 255))
    draw.text(
        (18, 49),
        "Each panel includes full framing and a registered face inset. Bottom contact is allowed; x/top contact is not.",
        font=small_font,
        fill=(168, 177, 190, 255),
    )
    for column_index, (outfit, background) in enumerate(columns):
        center_x = label_width + column_index * panel_width + panel_width // 2
        draw.text(
            (center_x, 83),
            f"{outfit.upper()} / {background}",
            font=small_font,
            fill=(113, 224, 236, 255),
            anchor="mm",
        )

    current_y = header_height
    for expression in ALL_EXPRESSIONS:
        draw.text(
            (label_width - 14, current_y + panel_height // 2),
            "NEUTRAL" if expression == "neut" else expression.upper(),
            font=label_font,
            fill=(235, 238, 244, 255),
            anchor="rm",
        )
        for column_index, (outfit, background) in enumerate(columns):
            if expression == "neut":
                spec = next(item for item in OUTFITS if item.name == outfit)
                sprite = alpha_composite(bases[outfit], images[spec.neutral_layer_name])
            else:
                if (outfit, expression) not in validated_expressions:
                    raise KeyError(f"missing validated composite for {outfit}/{expression}")
                spec = next(item for item in OUTFITS if item.name == outfit)
                sprite = alpha_composite(
                    bases[outfit],
                    images[spec.expression_name(expression)],
                )
            panel = review_panel(sprite, background, f"{outfit} / {background}")
            sheet.alpha_composite(panel, (label_width + column_index * panel_width, current_y))
        current_y += panel_height + row_gap

    draw.rectangle((0, current_y, width - 1, current_y + pose_divider_height - 8), fill=(27, 31, 40, 255))
    draw.text(
        (18, current_y + (pose_divider_height - 8) // 2),
        "FIXED FULL-BODY POSES",
        font=label_font,
        fill=(113, 224, 236, 255),
        anchor="lm",
    )
    current_y += pose_divider_height

    for pose in POSES:
        draw.text(
            (label_width - 14, current_y + panel_height // 2),
            pose.attribute.removeprefix("pose_").replace("_", " ").upper(),
            font=label_font,
            fill=(235, 238, 244, 255),
            anchor="rm",
        )
        for column_index, (outfit, background) in enumerate(columns):
            if outfit == pose.outfit:
                panel = review_panel(
                    images[pose.filename],
                    background,
                    f"{pose.outfit} / {background}",
                )
            else:
                panel = blank_review_panel(f"fixed {pose.outfit} pose")
            sheet.alpha_composite(panel, (label_width + column_index * panel_width, current_y))
        current_y += panel_height + row_gap

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(output_path, format="PNG", compress_level=6)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sprite-root",
        type=Path,
        default=PROJECT_ROOT / "game" / "mod_assets" / "char_sprites" / "masayami",
        help="Sam's production sprite directory",
    )
    parser.add_argument(
        "--canonical-root",
        type=Path,
        help=(
            "optional directory supplying only neutral.png and neut_uniform.png; "
            "use this when --sprite-root is a pre-install temp face bank"
        ),
    )
    parser.add_argument(
        "--pose-root",
        type=Path,
        help=(
            "optional directory supplying the four pose PNGs; use this when "
            "--sprite-root is a pre-install temp face bank"
        ),
    )
    parser.add_argument(
        "--definitions",
        type=Path,
        default=PROJECT_ROOT / "game" / "mod_assets" / "def_characters.rpy",
        help="Ren'Py character-image declarations to audit",
    )
    parser.add_argument(
        "--contact-sheet",
        type=Path,
        default=PROJECT_ROOT / "tmp" / "sprite_review" / "sam_contact_sheet.png",
        help="PNG review-sheet destination",
    )
    parser.add_argument(
        "--skip-contact-sheet",
        action="store_true",
        help="run validation without writing the visual review sheet",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sprite_root = args.sprite_root.resolve()
    canonical_root = args.canonical_root.resolve() if args.canonical_root else None
    pose_root = args.pose_root.resolve() if args.pose_root else None
    definition_path = args.definitions.resolve()
    output_path = args.contact_sheet.resolve()
    report = ValidationReport()

    if not sprite_root.is_dir():
        report.error(f"{sprite_root}: Sam sprite directory does not exist")
        images: dict[str, np.ndarray] = {}
    else:
        images = load_production_pngs(
            sprite_root,
            report,
            canonical_root=canonical_root,
            pose_root=pose_root,
        )

    originals, bases = validate_outfit_bases(images, report)
    validated_expressions = validate_expression_bank(
        images,
        originals,
        bases,
        report,
    )
    validate_poses(images, report)
    validate_definitions(definition_path, report)

    contact_inputs_complete = (
        all(outfit.name in bases for outfit in OUTFITS)
        and all(outfit.neutral_layer_name in images for outfit in OUTFITS)
        and all(
            (outfit.name, expression) in validated_expressions
            for outfit in OUTFITS
            for expression in EXPRESSIONS
        )
        and all(pose.filename in images for pose in POSES)
    )
    if not args.skip_contact_sheet and contact_inputs_complete:
        try:
            build_contact_sheet(images, bases, validated_expressions, output_path)
            report.note(f"contact sheet: {output_path}")
        except (OSError, ValueError, KeyError) as exc:
            report.error(f"cannot write contact sheet {output_path}: {exc}")
    elif not args.skip_contact_sheet:
        report.note("contact sheet: not written because required sprite inputs are missing")

    output_stream = sys.stderr if report.errors else sys.stdout
    if report.notes:
        print("SAM SPRITE VALIDATION METRICS", file=output_stream)
        for note in report.notes:
            print(f"  {note}", file=output_stream)

    if report.errors:
        print(f"\nSAM SPRITE VALIDATION FAILED ({len(report.errors)} issue(s))", file=output_stream)
        for index, error in enumerate(report.errors, start=1):
            indented = error.replace("\n", "\n    ")
            print(f"  {index}. {indented}", file=output_stream)
        return 1

    expected_face_count = len(ALL_EXPRESSIONS) * len(OUTFITS)
    print(
        f"\nSAM SPRITE VALIDATION PASSED: {expected_face_count} outfit-expression "
        f"composites, {len(POSES)} poses, exact neutral reconstruction, and "
        "all def_characters sprite references verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
