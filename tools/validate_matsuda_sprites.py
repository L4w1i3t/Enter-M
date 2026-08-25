#!/usr/bin/env python3
"""Validate Matsuda's production two-base sprite system.

The accepted runtime contract is deliberately narrow: ``neutral.png`` and
``neut_uniform.png`` are the only layered-image bases, each of the 21 face
attributes has one outfit-conditioned full-canvas layer, and the five moving
poses remain standalone images.  The validator is read-only and exits nonzero
after printing every issue it finds.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPRITE_ROOT = PROJECT_ROOT / "game" / "mod_assets" / "char_sprites" / "matsuda"
DEFAULT_DEFINITIONS = PROJECT_ROOT / "game" / "mod_assets" / "def_characters.rpy"
CANVAS_SIZE = (1023, 1537)
CANVAS_WIDTH, CANVAS_HEIGHT = CANVAS_SIZE
EXPECTED_FACE_ALPHA_LEVELS = 256
CHECKER_PERIODICITY_LIMIT = 0.28
GRID_PERIODICITY_LIMIT = 0.55
FACE_FRINGE_RESIDUE_LIMIT = 8
FACE_AUTHORED_ALPHA_SEED = 160
FACE_FEATURE_DETAIL_THRESHOLD = 18
FACE_FEATURE_DILATION = 1
FACE_FEATURE_MIN_PIXELS = 2_500
FACE_JAW_EXTERIOR_INSET = 4
FACE_JAW_ROI = (330, 360, 620, 480)
CHARACTER_COMPONENT_LIMIT = 8
CHARACTER_DOMINANT_COMPONENT_MIN = 0.995
CHARACTER_DETACHED_COMPONENT_MIN_AREA = 64

FACE_TOKENS = (
    "neut",
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


@dataclass(frozen=True)
class OutfitSpec:
    name: str
    base_name: str

    def face_name(self, token: str) -> str:
        return f"face_{token}_{self.name}.png"

    def face_reference(self, token: str) -> str:
        return f"mod_assets/char_sprites/matsuda/{self.face_name(token)}"

    @property
    def base_reference(self) -> str:
        return f"mod_assets/char_sprites/matsuda/{self.base_name}"


OUTFITS = (
    OutfitSpec("casual", "neutral.png"),
    OutfitSpec("uniform", "neut_uniform.png"),
)


@dataclass(frozen=True)
class PoseSpec:
    outfit: str
    attribute: str
    filename: str

    @property
    def reference(self) -> str:
        return f"mod_assets/char_sprites/matsuda/{self.filename}"


POSES = (
    PoseSpec("uniform", "pose_facepalm", "pose_facepalm_uniform.png"),
    PoseSpec("uniform", "pose_chuuni", "pose_chuuni_uniform.png"),
    PoseSpec("uniform", "pose_shrug", "pose_shrug_uniform.png"),
    PoseSpec("casual", "pose_laughing", "pose_laughing_casual.png"),
    PoseSpec("uniform", "pose_laughing", "pose_laughing_uniform.png"),
)


@dataclass(frozen=True)
class AttributeRecord:
    name: str
    is_default: bool
    if_all: tuple[str, ...]
    asset: str | None


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


def connected_component_areas(mask: np.ndarray) -> list[int]:
    """Return 8-connected foreground component areas, largest first.

    Horizontal run labeling keeps full-canvas checks fast without adding an
    OpenCV or SciPy dependency to this validator.
    """

    if mask.ndim != 2:
        raise ValueError(f"component mask must be two-dimensional, got {mask.shape}")

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


def components_connected_to_seed(
    mask: np.ndarray,
    seeds: np.ndarray,
) -> np.ndarray:
    """Return 8-connected ``mask`` pixels reachable from any seed pixel.

    Face ink can legitimately cross from a fully or substantially opaque mask
    interior into its feather.  A black/white matte fleck instead forms an
    unanchored component in that transition.  Cropping before flood fill keeps
    this dependency-free topology check small and fast.
    """

    if mask.ndim != 2 or seeds.shape != mask.shape:
        raise ValueError(
            f"seeded masks must share one 2D shape, got {mask.shape}/{seeds.shape}"
        )
    result = np.zeros_like(mask, dtype=bool)
    bounds = mask_bbox(mask)
    if bounds is None:
        return result
    left, top, right, bottom = bounds
    local_mask = np.asarray(mask[top:bottom, left:right], dtype=bool)
    local_seeds = np.asarray(seeds[top:bottom, left:right], dtype=bool) & local_mask
    if not np.any(local_seeds):
        return result

    supported = np.zeros_like(local_mask, dtype=bool)
    supported[local_seeds] = True
    stack = [(int(y), int(x)) for y, x in np.argwhere(local_seeds)]
    height, width = local_mask.shape
    while stack:
        y, x = stack.pop()
        for neighbor_y in range(max(0, y - 1), min(height, y + 2)):
            for neighbor_x in range(max(0, x - 1), min(width, x + 2)):
                if (
                    local_mask[neighbor_y, neighbor_x]
                    and not supported[neighbor_y, neighbor_x]
                ):
                    supported[neighbor_y, neighbor_x] = True
                    stack.append((neighbor_y, neighbor_x))
    result[top:bottom, left:right] = supported
    return result


def dilate_mask(
    mask: np.ndarray,
    radius: int,
    *,
    euclidean: bool = False,
) -> np.ndarray:
    """Dilate a binary mask with a square or integer-radius disk."""

    if mask.ndim != 2:
        raise ValueError(f"dilation mask must be two-dimensional, got {mask.shape}")
    if radius < 0:
        raise ValueError(f"dilation radius must be nonnegative, got {radius}")
    source = np.asarray(mask, dtype=bool)
    if radius == 0:
        return source.copy()
    height, width = source.shape
    padded = np.pad(source, radius, constant_values=False)
    result = np.zeros_like(source)
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if euclidean and dx * dx + dy * dy > radius * radius:
                continue
            result |= padded[
                radius + dy : radius + dy + height,
                radius + dx : radius + dx + width,
            ]
    return result


def neutral_feature_footprint(base: np.ndarray) -> np.ndarray:
    """Extract Matsuda's neutral brows, eyes/irises, and mouth footprint.

    Fixed semantic ellipses keep hair and the face silhouette out of scope.
    Within them, color cues plus local high-frequency detail select authored
    feature ink rather than requiring an unsafe opaque rectangle.  A one-pixel
    halo covers antialiasing and registration tolerance at outer eye corners.
    """

    if base.shape != (CANVAS_HEIGHT, CANVAS_WIDTH, 4):
        raise ValueError(f"unexpected Matsuda base shape: {base.shape}")

    left, top, right, bottom = (340, 235, 590, 430)
    crop = base[top:bottom, left:right]
    rgb_u8 = crop[:, :, :3]
    rgb = rgb_u8.astype(np.int16)
    blurred = np.asarray(
        Image.fromarray(rgb_u8, "RGB").filter(ImageFilter.GaussianBlur(2.2)),
        dtype=np.int16,
    )
    local_detail = np.max(np.abs(rgb - blurred), axis=2)
    red, green, blue = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    luminance = (54 * red + 183 * green + 19 * blue) // 256
    channel_spread = rgb.max(axis=2) - rgb.min(axis=2)

    rows, columns = np.ogrid[top:bottom, left:right]

    def ellipse(
        center_x: int,
        center_y: int,
        radius_x: int,
        radius_y: int,
    ) -> np.ndarray:
        return ((columns - center_x) / radius_x) ** 2 + (
            (rows - center_y) / radius_y
        ) ** 2 <= 1.0

    eyes = ellipse(414, 327, 63, 32) | ellipse(521, 300, 58, 31)
    brows = ellipse(414, 300, 44, 10) | ellipse(516, 273, 42, 9)
    mouth = ellipse(486, 393, 48, 23)
    semantic = eyes | brows | mouth
    dark_ink = (luminance <= 105) & (rgb.max(axis=2) <= 145) & (channel_spread <= 55)
    green_iris = (green - np.maximum(red, blue) > 12) & (green > 60) & (red < 160)
    pale_eye_or_teeth = (rgb.min(axis=2) >= 205) & (channel_spread <= 38)
    red_hair = (
        (red >= 65) & ((red - green) >= 30) & ((red - blue) >= 22) & (green < 150)
    )
    warm_feature = ((red - green) >= 24) & ((red - blue) >= 18) & (luminance <= 175)
    local_feature = (
        (
            eyes
            & (
                (local_detail >= FACE_FEATURE_DETAIL_THRESHOLD)
                | dark_ink
                | green_iris
                | pale_eye_or_teeth
            )
            & ~red_hair
        )
        | (brows & ((local_detail >= 12) | dark_ink | warm_feature))
        | (
            mouth
            & ((local_detail >= 12) | dark_ink | (warm_feature & (luminance <= 155)))
        )
    )

    footprint = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH), dtype=bool)
    semantic_full = np.zeros_like(footprint)
    brow_full = np.zeros_like(footprint)
    red_hair_full = np.zeros_like(footprint)
    footprint[top:bottom, left:right] = local_feature
    semantic_full[top:bottom, left:right] = semantic
    brow_full[top:bottom, left:right] = brows
    red_hair_full[top:bottom, left:right] = red_hair
    footprint = dilate_mask(footprint, FACE_FEATURE_DILATION)
    return (
        footprint
        & semantic_full
        & (~red_hair_full | brow_full)
        & (base[:, :, 3] == 255)
    )


def face_jaw_boundary_zone(base_alpha: np.ndarray) -> np.ndarray:
    """Return lower-face pixels too close to the canonical exterior boundary."""

    if base_alpha.shape != (CANVAS_HEIGHT, CANVAS_WIDTH):
        raise ValueError(f"unexpected Matsuda alpha shape: {base_alpha.shape}")
    canonical_opaque = base_alpha == 255
    near_nonopaque = dilate_mask(
        ~canonical_opaque,
        FACE_JAW_EXTERIOR_INSET,
        euclidean=True,
    )
    left, top, right, bottom = FACE_JAW_ROI
    roi = np.zeros_like(canonical_opaque)
    roi[top:bottom, left:right] = True
    return canonical_opaque & near_nonopaque & roi


def shifted_correlation(
    values: np.ndarray,
    support: np.ndarray,
    dy: int,
    dx: int,
) -> float | None:
    """Correlate supported samples with a spatially shifted copy."""

    height, width = support.shape
    if abs(dy) >= height or abs(dx) >= width:
        return None
    first_y = slice(max(0, -dy), min(height, height - dy))
    second_y = slice(max(0, dy), min(height, height + dy))
    first_x = slice(max(0, -dx), min(width, width - dx))
    second_x = slice(max(0, dx), min(width, width + dx))
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

    # Suppress ordinary broad face shading before seeking same-phase grid
    # lines. Checker alternation is measured on the raw difference so both
    # dark/light phases remain intact.
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


def alpha_composite(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    return np.asarray(
        Image.alpha_composite(
            Image.fromarray(base, "RGBA"), Image.fromarray(overlay, "RGBA")
        ),
        dtype=np.uint8,
    ).copy()


def residue_masks(pixels: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return conservative low-alpha black/white and magenta matte masks."""

    alpha = pixels[:, :, 3]
    rgb = pixels[:, :, :3].astype(np.int16)
    red, green, blue = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    low_alpha = (alpha > 0) & (alpha <= 64)
    channel_spread = rgb.max(axis=2) - rgb.min(axis=2)
    near_black = low_alpha & (rgb.max(axis=2) <= 8)
    near_white = low_alpha & (rgb.min(axis=2) >= 247) & (channel_spread <= 4)
    strong_magenta = (
        (alpha > 3)
        & (red >= 180)
        & (blue >= 160)
        & (green <= 100)
        & ((np.minimum(red, blue) - green) >= 100)
    )
    return near_black, near_white, strong_magenta


def validate_character_components(
    visible: np.ndarray,
    label: str,
    report: ValidationReport,
) -> tuple[int, int, int, float]:
    """Reject fragmented silhouettes and small detached alpha debris."""

    areas = connected_component_areas(visible)
    visible_count = int(visible.sum())
    largest = areas[0] if areas else 0
    detached = visible_count - largest
    dominant_ratio = largest / max(1, visible_count)
    small_detached = [
        area for area in areas[1:] if area < CHARACTER_DETACHED_COMPONENT_MIN_AREA
    ]
    report.check(
        len(areas) <= CHARACTER_COMPONENT_LIMIT,
        f"{label}: alpha silhouette is fragmented into {len(areas)} components; "
        f"limit={CHARACTER_COMPONENT_LIMIT}, largest areas={areas[:10]}",
    )
    report.check(
        dominant_ratio >= CHARACTER_DOMINANT_COMPONENT_MIN,
        f"{label}: dominant alpha component contains only {dominant_ratio:.3%} "
        f"of the silhouette ({largest}/{visible_count}); detached={detached}",
    )
    report.check(
        not small_detached,
        f"{label}: detached/isolated alpha specks found; component "
        f"areas={small_detached[:20]} (minimum intentional detached area is "
        f"{CHARACTER_DETACHED_COMPONENT_MIN_AREA})",
    )
    return len(areas), largest, detached, dominant_ratio


def validate_character_residue(
    pixels: np.ndarray,
    label: str,
    report: ValidationReport,
) -> tuple[int, int, int, int]:
    """Apply conservative matte-remnant checks to a full character image."""

    alpha = pixels[:, :, 3]
    near_black, near_white, strong_magenta = residue_masks(pixels)
    low_alpha_count = int(np.count_nonzero((alpha > 0) & (alpha <= 64)))
    black_count = int(near_black.sum())
    white_count = int(near_white.sum())
    magenta_count = int(strong_magenta.sum())
    black_ratio = black_count / max(1, low_alpha_count)
    white_ratio = white_count / max(1, low_alpha_count)
    report.check(
        black_count <= 512 and black_ratio <= 0.12,
        f"{label}: suspicious low-alpha black matte residue covers "
        f"{black_count}/{low_alpha_count} edge pixels ({black_ratio:.2%})",
    )
    report.check(
        white_count <= 512 and white_ratio <= 0.12,
        f"{label}: suspicious low-alpha white matte residue covers "
        f"{white_count}/{low_alpha_count} edge pixels ({white_ratio:.2%})",
    )
    report.check(
        magenta_count == 0,
        f"{label}: {magenta_count} visible pixels look like strong magenta "
        "chroma-key remnants",
    )
    return low_alpha_count, black_count, white_count, magenta_count


def load_rgba(path: Path, label: str, report: ValidationReport) -> np.ndarray | None:
    if not path.is_file() or path.is_symlink():
        report.error(f"{label}: missing or unsafe PNG: {path}")
        return None
    try:
        with Image.open(path) as image:
            if image.mode != "RGBA" or image.size != CANVAS_SIZE:
                report.error(
                    f"{label}: expected RGBA {CANVAS_SIZE}, got "
                    f"{image.mode} {image.size}: {path}"
                )
                return None
            pixels = np.asarray(image, dtype=np.uint8).copy()
    except (OSError, ValueError) as exc:
        report.error(f"{label}: cannot read {path}: {exc}")
        return None

    alpha = pixels[:, :, 3]
    hidden_rgb = int(
        np.count_nonzero((alpha == 0) & np.any(pixels[:, :, :3] != 0, axis=2))
    )
    report.check(
        hidden_rgb == 0,
        f"{label}: {hidden_rgb} fully transparent pixels retain RGB matte data",
    )
    return pixels


def expected_face_names() -> set[str]:
    return {outfit.face_name(token) for outfit in OUTFITS for token in FACE_TOKENS}


def validate_manifest(sprite_root: Path, report: ValidationReport) -> None:
    expected = expected_face_names()
    actual = {
        path.name
        for path in sprite_root.glob("face_*_*.png")
        if path.is_file() and not path.is_symlink()
    }
    report.check(
        actual == expected,
        "Matsuda conditioned-face manifest is not the exact 42-file bank; "
        f"missing={sorted(expected - actual)} unexpected={sorted(actual - expected)}",
    )


def validate_bases(
    sprite_root: Path, report: ValidationReport
) -> dict[str, np.ndarray]:
    bases: dict[str, np.ndarray] = {}
    signatures: dict[bytes, str] = {}
    for outfit in OUTFITS:
        label = f"matsuda/{outfit.name}/base"
        pixels = load_rgba(sprite_root / outfit.base_name, label, report)
        if pixels is None:
            continue
        alpha = pixels[:, :, 3]
        visible = alpha > 0
        bounds = mask_bbox(visible)
        report.check(bool(np.any(visible)), f"{label}: base is fully transparent")
        report.check(
            bool(np.any(~visible)), f"{label}: base has no transparent exterior"
        )
        if bounds is not None:
            left, top, right, bottom = bounds
            report.check(
                left > 0 and top > 0 and right < CANVAS_WIDTH,
                f"{label}: sprite touches the top or a horizontal canvas edge; "
                f"bbox={format_bbox(bounds)}",
            )
            report.check(
                bottom == CANVAS_HEIGHT,
                f"{label}: base must reach the shared canvas baseline; "
                f"bbox={format_bbox(bounds)}",
            )
        component_count, _largest, detached, dominant_ratio = (
            validate_character_components(visible, label, report)
        )
        low_alpha, black_count, white_count, magenta_count = validate_character_residue(
            pixels, label, report
        )
        signature = hashlib.sha256(pixels).digest()
        previous = signatures.get(signature)
        report.check(previous is None, f"{label}: base pixels duplicate {previous}")
        signatures[signature] = outfit.name
        bases[outfit.name] = pixels
        report.note(
            f"{label}: bbox={format_bbox(bounds)} visible={int(visible.sum())} "
            f"components={component_count} dominant={dominant_ratio:.3%} "
            f"detached={detached} low-alpha={low_alpha} "
            f"edge-black={black_count} edge-white={white_count} "
            f"strong-magenta={magenta_count}"
        )
    return bases


def validate_face_bank(
    sprite_root: Path,
    bases: dict[str, np.ndarray],
    report: ValidationReport,
) -> None:
    for outfit in OUTFITS:
        fixed_alpha: np.ndarray | None = None
        fixed_mask_source: str | None = None
        base = bases.get(outfit.name)
        neutral_features: np.ndarray | None = None
        jaw_boundary: np.ndarray | None = None
        if base is not None:
            neutral_features = neutral_feature_footprint(base)
            feature_count = int(neutral_features.sum())
            report.check(
                feature_count >= FACE_FEATURE_MIN_PIXELS,
                f"matsuda/{outfit.name}/neutral-features: extracted only "
                f"{feature_count} canonical brow/eye/iris/mouth pixels; expected "
                f"at least {FACE_FEATURE_MIN_PIXELS}",
            )
            jaw_boundary = face_jaw_boundary_zone(base[:, :, 3])
        composite_signatures: dict[bytes, str] = {}
        component_cache: dict[bytes, list[int]] = {}
        changed_counts: list[int] = []
        checker_metrics: list[tuple[float, str, int | None]] = []
        grid_metrics: list[tuple[float, str, int | None]] = []
        fringe_black_counts: list[int] = []
        fringe_white_counts: list[int] = []
        magenta_counts: list[int] = []
        uncovered_feature_counts: list[int] = []
        unsafe_jaw_counts: list[int] = []

        for token in FACE_TOKENS:
            filename = outfit.face_name(token)
            label = f"matsuda/{outfit.name}/face/{token}"
            layer = load_rgba(sprite_root / filename, label, report)
            if layer is None:
                continue
            alpha = layer[:, :, 3]

            if token == "neut":
                report.check(
                    not np.any(alpha),
                    f"{label}: neutral overlay must be fully transparent",
                )
                report.check(
                    not np.any(layer[:, :, :3]),
                    f"{label}: neutral overlay must contain zero RGB as well as "
                    "zero alpha",
                )
            else:
                report.check(
                    bool(np.any(alpha)),
                    f"{label}: alternate expression overlay is fully transparent",
                )
                levels = len(np.unique(alpha))
                report.check(
                    levels == EXPECTED_FACE_ALPHA_LEVELS,
                    f"{label}: face mask has {levels} alpha levels; expected "
                    f"exactly {EXPECTED_FACE_ALPHA_LEVELS} (all uint8 levels)",
                )
                alpha_signature = hashlib.sha256(alpha.tobytes()).digest()
                component_areas = component_cache.get(alpha_signature)
                if component_areas is None:
                    component_areas = connected_component_areas(alpha > 0)
                    component_cache[alpha_signature] = component_areas
                report.check(
                    len(component_areas) == 1,
                    f"{label}: face mask contains {len(component_areas)} "
                    "8-connected alpha components; detached/isolated specks are "
                    f"not allowed, areas={component_areas[:20]}",
                )

                if fixed_alpha is None:
                    fixed_alpha = alpha.copy()
                    fixed_mask_source = filename
                    bounds = mask_bbox(fixed_alpha > 0)
                    report.check(
                        bounds is not None,
                        f"{label}: fixed face mask is empty",
                    )
                    if bounds is not None:
                        left, top, right, bottom = bounds
                        report.check(
                            left > 0
                            and top > 0
                            and right < CANVAS_WIDTH
                            and bottom < CANVAS_HEIGHT,
                            f"{label}: face mask touches a canvas edge; "
                            f"bbox={format_bbox(bounds)}",
                        )
                    report.check(
                        bool(np.any(fixed_alpha == 255)),
                        f"{label}: fixed face mask has no opaque interior",
                    )
                else:
                    report.check(
                        np.array_equal(alpha, fixed_alpha),
                        f"{label}: alpha mask differs from {fixed_mask_source}; "
                        f"every alternate in {outfit.name} must share one fixed mask",
                    )

                if neutral_features is not None:
                    uncovered_features = neutral_features & (alpha != 255)
                    uncovered_count = int(uncovered_features.sum())
                    report.check(
                        uncovered_count == 0,
                        f"{label}: face mask leaves {uncovered_count} canonical "
                        "neutral brow/eye/iris/mouth pixels below full opacity; "
                        "the neutral expression can leak through, including at "
                        "outer eye corners; uncovered bbox="
                        f"{format_bbox(mask_bbox(uncovered_features))}",
                    )
                    uncovered_feature_counts.append(uncovered_count)
                if jaw_boundary is not None:
                    unsafe_jaw = (alpha > 0) & jaw_boundary
                    unsafe_jaw_count = int(unsafe_jaw.sum())
                    report.check(
                        unsafe_jaw_count == 0,
                        f"{label}: {unsafe_jaw_count} face-mask pixels lie within "
                        f"the forbidden {FACE_JAW_EXTERIOR_INSET}px lower jaw "
                        "inset from the canonical opaque-silhouette boundary; "
                        f"unsafe bbox={format_bbox(mask_bbox(unsafe_jaw))}",
                    )
                    unsafe_jaw_counts.append(unsafe_jaw_count)

            if base is not None:
                outside_base = int(np.count_nonzero((alpha > 0) & (base[:, :, 3] == 0)))
                report.check(
                    outside_base == 0,
                    f"{label}: {outside_base} face-mask pixels extend outside "
                    "the canonical base silhouette",
                )

                composite = alpha_composite(base, layer)
                report.check(
                    np.array_equal(composite[:, :, 3], base[:, :, 3]),
                    f"{label}: composite changes the canonical base silhouette",
                )
                changed = int(np.count_nonzero(np.any(composite != base, axis=2)))
                if token == "neut":
                    report.check(
                        changed == 0,
                        f"{label}: transparent neutral changes {changed} base pixels",
                    )
                else:
                    report.check(
                        changed > 0,
                        f"{label}: alternate composite is pixel-identical to neutral",
                    )
                    changed_counts.append(changed)

                    checker_score, checker_tile, grid_score, grid_tile = (
                        checker_grid_periodicity_scores(
                            composite,
                            base,
                            alpha == 255,
                        )
                    )
                    report.check(
                        checker_score < CHECKER_PERIODICITY_LIMIT,
                        f"{label}: checker-like two-axis periodicity detected "
                        f"(score={checker_score:.3f}, estimated tile={checker_tile}px)",
                    )
                    report.check(
                        grid_score < GRID_PERIODICITY_LIMIT,
                        f"{label}: repeating two-axis grid residue detected "
                        f"(score={grid_score:.3f}, estimated tile={grid_tile}px)",
                    )
                    checker_metrics.append((checker_score, token, checker_tile))
                    grid_metrics.append((grid_score, token, grid_tile))

                    rgb = layer[:, :, :3].astype(np.int16)
                    channel_spread = rgb.max(axis=2) - rgb.min(axis=2)
                    partial = (alpha > 0) & (alpha < 255)
                    color_delta = np.max(
                        np.abs(
                            composite[:, :, :3].astype(np.int16)
                            - base[:, :, :3].astype(np.int16)
                        ),
                        axis=2,
                    )
                    visibly_changed_fringe = partial & (color_delta >= 24)
                    visible = alpha > 0
                    broad_black = visible & (rgb.max(axis=2) <= 8)
                    broad_white = (
                        visible & (rgb.min(axis=2) >= 247) & (channel_spread <= 4)
                    )
                    authored_seed = alpha >= FACE_AUTHORED_ALPHA_SEED
                    supported_black = components_connected_to_seed(
                        broad_black,
                        broad_black & authored_seed,
                    )
                    supported_white = components_connected_to_seed(
                        broad_white,
                        broad_white & authored_seed,
                    )
                    fringe_black = (
                        visibly_changed_fringe & broad_black & ~supported_black
                    )
                    fringe_white = (
                        visibly_changed_fringe & broad_white & ~supported_white
                    )
                    black_count = int(fringe_black.sum())
                    white_count = int(fringe_white.sum())
                    visible_count = int(visible.sum())
                    broad_black_ratio = int(broad_black.sum()) / max(1, visible_count)
                    broad_white_ratio = int(broad_white.sum()) / max(1, visible_count)
                    _edge_black, _edge_white, strong_magenta = residue_masks(layer)
                    magenta_count = int(strong_magenta.sum())
                    report.check(
                        black_count <= FACE_FRINGE_RESIDUE_LIMIT,
                        f"{label}: {black_count} visibly changed, unanchored "
                        "feather pixels look like black matte residue; "
                        f"limit={FACE_FRINGE_RESIDUE_LIMIT}",
                    )
                    report.check(
                        white_count <= FACE_FRINGE_RESIDUE_LIMIT,
                        f"{label}: {white_count} visibly changed, unanchored "
                        "feather pixels look like white matte residue; "
                        f"limit={FACE_FRINGE_RESIDUE_LIMIT}",
                    )
                    report.check(
                        broad_black_ratio <= 0.20,
                        f"{label}: near-black pixels occupy "
                        f"{broad_black_ratio:.2%} of the face plate; likely black "
                        "background/matte residue",
                    )
                    report.check(
                        broad_white_ratio <= 0.12,
                        f"{label}: near-white pixels occupy "
                        f"{broad_white_ratio:.2%} of the face plate; likely white "
                        "background/matte residue",
                    )
                    report.check(
                        magenta_count == 0,
                        f"{label}: {magenta_count} visible pixels look like strong "
                        "magenta chroma-key remnants",
                    )
                    fringe_black_counts.append(black_count)
                    fringe_white_counts.append(white_count)
                    magenta_counts.append(magenta_count)

                composite_signature = hashlib.sha256(composite).digest()
                previous_composite = composite_signatures.get(composite_signature)
                report.check(
                    previous_composite is None,
                    f"{label}: composite duplicates {previous_composite}; every "
                    f"{outfit.name} expression must be pairwise distinct",
                )
                composite_signatures[composite_signature] = label

        if fixed_alpha is not None:
            visible = fixed_alpha > 0
            component_areas = connected_component_areas(visible)
            strongest_checker = max(checker_metrics, default=(0.0, "none", None))
            strongest_grid = max(grid_metrics, default=(0.0, "none", None))
            report.note(
                f"matsuda/{outfit.name}/face-mask: "
                f"bbox={format_bbox(mask_bbox(visible))} "
                f"visible={int(visible.sum())} opaque={int((fixed_alpha == 255).sum())} "
                f"levels={len(np.unique(fixed_alpha))} "
                f"components={len(component_areas)} areas={component_areas[:5]}"
            )
            if changed_counts:
                report.note(
                    f"matsuda/{outfit.name}/alternates: "
                    f"distinct-composites={len(composite_signatures)}/{len(FACE_TOKENS)} "
                    f"changed-range={min(changed_counts)}-{max(changed_counts)} "
                    f"checker-max={strongest_checker[0]:.3f}/"
                    f"{strongest_checker[1]}@{strongest_checker[2]}px "
                    f"grid-max={strongest_grid[0]:.3f}/"
                    f"{strongest_grid[1]}@{strongest_grid[2]}px "
                    f"fringe-black-max={max(fringe_black_counts, default=0)} "
                    f"fringe-white-max={max(fringe_white_counts, default=0)} "
                    f"strong-magenta-max={max(magenta_counts, default=0)} "
                    f"neutral-feature-footprint="
                    f"{int(neutral_features.sum()) if neutral_features is not None else 0} "
                    f"uncovered-feature-max="
                    f"{max(uncovered_feature_counts, default=0)} "
                    f"unsafe-jaw-max={max(unsafe_jaw_counts, default=0)}"
                )


def validate_poses(sprite_root: Path, report: ValidationReport) -> None:
    for pose in POSES:
        label = f"matsuda/{pose.outfit}/{pose.attribute}"
        pixels = load_rgba(sprite_root / pose.filename, label, report)
        if pixels is None:
            continue

        alpha = pixels[:, :, 3]
        visible = alpha > 0
        bounds = mask_bbox(visible)
        report.check(bool(np.any(visible)), f"{label}: pose is fully transparent")
        report.check(
            bool(np.any(~visible)), f"{label}: pose has no transparent exterior"
        )
        report.check(
            bounds != (0, 0, CANVAS_WIDTH, CANVAS_HEIGHT),
            f"{label}: alpha bbox fills the complete canvas",
        )
        if bounds is not None:
            left, top, right, bottom = bounds
            report.check(
                left > 0 and top > 0 and right < CANVAS_WIDTH,
                f"{label}: pose touches the top or a horizontal canvas edge; "
                f"bbox={format_bbox(bounds)}",
            )
            report.check(
                bottom == CANVAS_HEIGHT,
                f"{label}: pose must reach the shared canvas baseline; "
                f"bbox={format_bbox(bounds)}",
            )
        component_count, _largest, detached, dominant_ratio = (
            validate_character_components(visible, label, report)
        )
        low_alpha, black_count, white_count, magenta_count = validate_character_residue(
            pixels, label, report
        )
        report.note(
            f"{label}: bbox={format_bbox(bounds)} visible={int(visible.sum())} "
            f"components={component_count} dominant={dominant_ratio:.3%} "
            f"detached={detached} low-alpha={low_alpha} "
            f"edge-black={black_count} edge-white={white_count} "
            f"strong-magenta={magenta_count}"
        )


def indented_block(source: str, header: str, indent: int) -> str:
    lines = source.splitlines(keepends=True)
    try:
        start = next(
            index for index, line in enumerate(lines) if line.rstrip() == header
        )
    except StopIteration as exc:
        raise ValueError(f"missing block header: {header}") from exc
    body = [lines[start]]
    for line in lines[start + 1 :]:
        if line.strip() and len(line) - len(line.lstrip(" ")) <= indent:
            break
        body.append(line)
    return "".join(body)


def parse_attribute_records(group: str) -> list[AttributeRecord]:
    lines = group.splitlines()
    records: list[AttributeRecord] = []
    attribute_pattern = re.compile(r"^        attribute\s+(\w+)(?P<tail>[^:]*):\s*$")
    asset_pattern = re.compile(
        r'"(?P<asset>mod_assets/char_sprites/matsuda/[^"\n]+\.png)"'
    )
    for index, line in enumerate(lines):
        match = attribute_pattern.match(line)
        if not match:
            continue
        tail = match.group("tail")
        asset: str | None = None
        for child in lines[index + 1 :]:
            if child.strip() and len(child) - len(child.lstrip(" ")) <= 8:
                break
            asset_match = asset_pattern.search(child)
            if asset_match:
                asset = asset_match.group("asset")
                break
        records.append(
            AttributeRecord(
                name=match.group(1),
                is_default=bool(re.search(r"(?:^|\s)default(?:\s|$)", tail)),
                if_all=tuple(re.findall(r'\bif_all\s+"([^"]+)"', tail)),
                asset=asset,
            )
        )
    return records


def validate_definition(
    definitions: Path,
    sprite_root: Path,
    report: ValidationReport,
) -> None:
    try:
        source = definitions.read_text(encoding="utf-8")
        layered = indented_block(source, "layeredimage matsuda:", 0)
        outfit_group = indented_block(layered, "    group outfit:", 4)
        face_group = indented_block(layered, "    group face:", 4)
    except (OSError, UnicodeError, ValueError) as exc:
        report.error(f"cannot audit Matsuda definition: {exc}")
        return

    transform_count = len(
        re.findall(r"^transform matsuda_sprite_size:\s*$", source, re.MULTILINE)
    )
    try:
        transform = indented_block(source, "transform matsuda_sprite_size:", 0)
    except ValueError:
        transform = ""
    transform_lines = [
        line.strip()
        for line in transform.splitlines()[1:]
        if line.strip() and not line.lstrip().startswith("#")
    ]
    report.check(
        transform_count == 1
        and transform_lines == ['fit "contain"', "xysize (640, 960)"],
        "Matsuda definition: matsuda_sprite_size must contain exactly "
        '`fit "contain"` and `xysize (640, 960)`; '
        f"occurrences={transform_count} body={transform_lines}",
    )
    at_clauses = re.findall(r"^\s+at\s+(.+?)\s*$", layered, re.MULTILINE)
    report.check(
        at_clauses == ["matsuda_sprite_size, Flatten"],
        "Matsuda definition: layeredimage must use exactly "
        f"`at matsuda_sprite_size, Flatten`; actual={at_clauses}",
    )

    outfit_records = Counter(parse_attribute_records(outfit_group))
    expected_outfits = Counter(
        {
            AttributeRecord("casual", True, (), OUTFITS[0].base_reference): 1,
            AttributeRecord("uniform", False, (), OUTFITS[1].base_reference): 1,
        }
    )
    report.check(
        outfit_records == expected_outfits,
        "Matsuda definition: outfit attributes must be exactly "
        "casual(default)->neutral.png and uniform->neut_uniform.png; "
        f"actual={list(outfit_records.elements())}",
    )

    face_records = Counter(parse_attribute_records(face_group))
    expected_faces: Counter[AttributeRecord] = Counter()
    for token in FACE_TOKENS:
        for outfit in OUTFITS:
            expected_faces[
                AttributeRecord(
                    token,
                    token == "neut" and outfit.name == "casual",
                    (outfit.name,),
                    outfit.face_reference(token),
                )
            ] += 1
    report.check(
        face_records == expected_faces,
        "Matsuda definition: face attributes differ from the exact 21-token x "
        "2-outfit conditioned contract; "
        f"missing={list((expected_faces - face_records).elements())} "
        f"extra={list((face_records - expected_faces).elements())}",
    )

    reference_pattern = re.compile(r'"(mod_assets/char_sprites/matsuda/[^"\n]+\.png)"')
    layered_reference_counts = Counter(reference_pattern.findall(layered))
    expected_layered_references = {
        *(outfit.base_reference for outfit in OUTFITS),
        *(outfit.face_reference(token) for outfit in OUTFITS for token in FACE_TOKENS),
    }
    report.check(
        set(layered_reference_counts) == expected_layered_references
        and all(count == 1 for count in layered_reference_counts.values()),
        "Matsuda definition: layeredimage references are not the exact 2-base + "
        "42-face manifest; "
        f"missing={sorted(expected_layered_references - set(layered_reference_counts))} "
        f"extra={sorted(set(layered_reference_counts) - expected_layered_references)} "
        "duplicates="
        f"{sorted(ref for ref, count in layered_reference_counts.items() if count != 1)}",
    )

    for reference in layered_reference_counts:
        asset = sprite_root / Path(reference).name
        report.check(
            asset.is_file() and not asset.is_symlink(),
            f"Matsuda layeredimage reference does not resolve to a safe file: "
            f"{reference} (expected {asset})",
        )

    all_matsuda_references = reference_pattern.findall(source)
    retired_references = sorted(
        reference
        for reference in all_matsuda_references
        if Path(reference).name in {"neut_face_base.png", "neut_uniform_face_base.png"}
        or Path(reference).name.startswith("post_")
        or re.search(r"(?:^|[_-])old(?:[_-]|\.)", Path(reference).name, re.IGNORECASE)
    )
    report.check(
        not retired_references,
        "Matsuda definition: retired old/post_/featureless-base runtime "
        f"reference(s) remain: {retired_references}",
    )

    generic_face_references = sorted(
        reference
        for reference in all_matsuda_references
        if re.fullmatch(r"face_[a-z0-9_]+\.png", Path(reference).name)
        and not Path(reference).stem.endswith(("_casual", "_uniform"))
    )
    report.check(
        not generic_face_references,
        "Matsuda definition: unconditioned generic face-layer reference(s) "
        f"remain: {generic_face_references}",
    )

    pose_pattern = re.compile(
        r"^image\s+matsuda\s+(?P<outfit>\w+)\s+(?P<attribute>pose_\w+)\s*=\s*"
        r'Transform\(\s*"(?P<asset>mod_assets/char_sprites/matsuda/[^"\n]+\.png)"\s*,'
        r'\s*fit\s*=\s*"contain"\s*,\s*xysize\s*=\s*\(\s*640\s*,\s*960\s*\)\s*\)\s*$',
        re.MULTILINE,
    )
    pose_records = Counter(
        (match.group("outfit"), match.group("attribute"), match.group("asset"))
        for match in pose_pattern.finditer(source)
    )
    expected_pose_records = Counter(
        (pose.outfit, pose.attribute, pose.reference) for pose in POSES
    )
    pose_header_pattern = re.compile(
        r"^image\s+matsuda\s+(?P<outfit>\w+)\s+"
        r"(?P<attribute>pose_\w+)\s*=",
        re.MULTILINE,
    )
    pose_headers = Counter(
        (match.group("outfit"), match.group("attribute"))
        for match in pose_header_pattern.finditer(source)
    )
    expected_pose_headers = Counter((pose.outfit, pose.attribute) for pose in POSES)
    report.check(
        pose_headers == expected_pose_headers,
        "Matsuda definition: pose outfit/attribute declarations are not the "
        "exact expected five; "
        f"missing={list((expected_pose_headers - pose_headers).elements())} "
        f"extra={list((pose_headers - expected_pose_headers).elements())}",
    )
    report.check(
        pose_records == expected_pose_records,
        "Matsuda definition: standalone pose declarations differ from the exact "
        "five outfit/attribute/file mappings or their Transform syntax; "
        f"missing={list((expected_pose_records - pose_records).elements())} "
        f"extra={list((pose_records - expected_pose_records).elements())}",
    )
    for pose in POSES:
        asset = sprite_root / pose.filename
        report.check(
            asset.is_file() and not asset.is_symlink(),
            f"Matsuda pose definition does not resolve to a safe file: "
            f"{pose.reference} (expected {asset})",
        )

    report.note(
        "matsuda/definition: exact two-base, 42 conditioned-face, and five-pose "
        "wiring checked"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sprite-root",
        type=Path,
        default=DEFAULT_SPRITE_ROOT,
        help="Matsuda production sprite directory",
    )
    parser.add_argument(
        "--definitions",
        type=Path,
        default=DEFAULT_DEFINITIONS,
        help="Ren'Py character-image declarations to audit",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sprite_root = args.sprite_root.resolve()
    definitions = args.definitions.resolve()
    report = ValidationReport()

    if not sprite_root.is_dir():
        report.error(f"Matsuda sprite directory does not exist: {sprite_root}")
    else:
        validate_manifest(sprite_root, report)
    bases = validate_bases(sprite_root, report)
    validate_face_bank(sprite_root, bases, report)
    validate_poses(sprite_root, report)
    validate_definition(definitions, sprite_root, report)

    output = sys.stderr if report.errors else sys.stdout
    if report.notes:
        print("MATSUDA SPRITE VALIDATION METRICS", file=output)
        for note in report.notes:
            print(f"  {note}", file=output)

    if report.errors:
        print(
            f"\nMATSUDA SPRITE VALIDATION FAILED ({len(report.errors)} issue(s))",
            file=output,
        )
        for index, error in enumerate(report.errors, start=1):
            print(
                f"  {index}. {error.replace(chr(10), chr(10) + '    ')}",
                file=output,
            )
        return 1

    print(
        "\nMATSUDA SPRITE VALIDATION PASSED: 2 canonical bases, 42 "
        "outfit-conditioned face layers with exact 256-level connected masks, "
        "pairwise-distinct residue-free composites, 5 clean connected poses, "
        "and exact Ren'Py wiring."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
