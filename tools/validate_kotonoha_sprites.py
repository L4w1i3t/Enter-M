#!/usr/bin/env python3
"""Validate Kotonoha's production expression bank and fixed pose sprites.

The accepted production contract is deliberately narrow:

* the original ``neutral.png`` and ``work.png`` files are preserved byte-for-byte;
* 21 full-canvas RGBA face layers exist for each outfit, including a completely
  blank neutral layer and one fixed feather mask shared by all 20 alternates;
* three fixed, mid-thigh-and-up poses live outside the layered image; and
* ``def_characters.rpy`` exposes the exact conditioned attributes without
  breaking the existing ``kotonoha neut`` and ``kotonoha work neut`` names.

Validation is read-only.  Passing ``--review-sheet PATH`` is the sole optional
write and produces a dark/light/checker contact sheet for human art review.
The validator intentionally reports every issue it can find before exiting.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from functools import lru_cache
from itertools import combinations
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPRITE_ROOT = PROJECT_ROOT / "game" / "mod_assets" / "char_sprites" / "kotonoha"
DEFAULT_DEFINITIONS = PROJECT_ROOT / "game" / "mod_assets" / "def_characters.rpy"
DEFAULT_STORY_ROOT = PROJECT_ROOT / "game"

CANVAS_SIZE = (1023, 1537)
CANVAS_WIDTH, CANVAS_HEIGHT = CANVAS_SIZE

# These are the source files present before the 2026-08-24 sprite-bank work.
# The file digest catches metadata/re-encoding changes; the decoded digest makes
# a pixel mismatch explicit in the error even if a future tool rewrites the PNG.
ORIGINAL_BASE_DIGESTS = {
    "neutral.png": (
        "3cc12dcd7bd018724a7232fe8aeaef505e312f7117b80f284c1b4719ba6a866b",
        "1e81bb84217ce9c90aef6f12a729807e40395b9a86edcdd94fb13ec39e3fd6b2",
    ),
    "work.png": (
        "72bc79cc551f8895ae66e94aacd551f01dfd7d6e74d35c59863132c0841d889c",
        "6f903f9dbe3665cd0b255355c00d3d6e978e3cb85e1b39aa816e721bbde74966",
    ),
}

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
ALTERNATE_TOKENS = FACE_TOKENS[1:]

# Kotonoha's source sprites share one registration.  These are deliberately
# looser than the actual face, but tight enough to reject a shifted head patch
# or a whole-torso generator plate.
FACE_PATCH_LIMITS = (330, 175, 700, 500)
FACE_CENTER = (510.0, 335.0)
FACE_CENTER_TOLERANCE = (48.0, 55.0)
FACE_MASK_WIDTH_RANGE = (170, 370)
FACE_MASK_HEIGHT_RANGE = (145, 315)
EXPECTED_FACE_ALPHA_LEVELS = 256
MIN_FACE_PARTIAL_PIXELS = 512
MIN_FACE_OPAQUE_PIXELS = 8_000
MIN_ALTERNATE_CHANGED_PIXELS = 500
MIN_PAIRWISE_CHANGED_PIXELS = 96
CHECKER_PERIODICITY_LIMIT = 0.28
GRID_PERIODICITY_LIMIT = 0.55

CHARACTER_COMPONENT_LIMIT = 8
CHARACTER_DOMINANT_COMPONENT_MIN = 0.995
# neutral.png contains one deliberate 21-pixel detached antialiased hair wisp.
# Specks smaller than that remain suspect, while the byte-exact hash separately
# guarantees that this exception cannot hide a new change to either source base.
CHARACTER_DETACHED_COMPONENT_MIN_AREA = 16


@dataclass(frozen=True)
class OutfitSpec:
    name: str
    base_name: str

    def face_name(self, token: str) -> str:
        return f"face_{token}_{self.name}.png"

    def face_reference(self, token: str) -> str:
        return f"mod_assets/char_sprites/kotonoha/{self.face_name(token)}"

    @property
    def base_reference(self) -> str:
        return f"mod_assets/char_sprites/kotonoha/{self.base_name}"


OUTFITS = (
    OutfitSpec("casual", "neutral.png"),
    OutfitSpec("work", "work.png"),
)


@dataclass(frozen=True)
class PoseSpec:
    outfit: str
    attribute: str
    filename: str

    @property
    def reference(self) -> str:
        return f"mod_assets/char_sprites/kotonoha/{self.filename}"


POSES = (
    PoseSpec("work", "pose_exact_fold", "pose_exact_fold_work.png"),
    PoseSpec("casual", "pose_watching", "pose_watching_casual.png"),
    PoseSpec("casual", "pose_open_hands", "pose_open_hands_casual.png"),
)


@dataclass(frozen=True)
class AttributeRecord:
    name: str
    is_default: bool
    if_all: tuple[str, ...]
    asset: str | None


@dataclass(frozen=True)
class HeadProfile:
    top: int
    center_x: float
    median_width: float
    upper_area: int
    skin_area: int
    skin_center_x: float | None
    skin_center_y: float | None


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


def expected_face_names() -> set[str]:
    return {outfit.face_name(token) for outfit in OUTFITS for token in FACE_TOKENS}


def expected_asset_names() -> set[str]:
    return {
        *(outfit.base_name for outfit in OUTFITS),
        *expected_face_names(),
        *(pose.filename for pose in POSES),
    }


def expected_layered_references() -> set[str]:
    return {
        *(outfit.base_reference for outfit in OUTFITS),
        *(outfit.face_reference(token) for outfit in OUTFITS for token in FACE_TOKENS),
    }


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


def changed_mask(first: np.ndarray, second: np.ndarray) -> np.ndarray:
    return np.any(first != second, axis=2)


def alpha_composite(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    return np.asarray(
        Image.alpha_composite(
            Image.fromarray(base, "RGBA"), Image.fromarray(overlay, "RGBA")
        ),
        dtype=np.uint8,
    ).copy()


def connected_component_areas(mask: np.ndarray) -> list[int]:
    """Return 8-connected foreground component areas, largest first.

    Horizontal run labelling keeps full-canvas checks quick without adding an
    OpenCV or SciPy dependency to this standalone QA tool.
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


def components_connected_to_seed(mask: np.ndarray, seeds: np.ndarray) -> np.ndarray:
    """Return 8-connected ``mask`` pixels reachable from the supplied seeds."""

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


def dilate_mask(mask: np.ndarray, radius: int) -> np.ndarray:
    if radius <= 0:
        return np.asarray(mask, dtype=bool).copy()
    source = np.asarray(mask, dtype=bool)
    height, width = source.shape
    padded = np.pad(source, radius, constant_values=False)
    result = np.zeros_like(source)
    for y_offset in range(radius * 2 + 1):
        for x_offset in range(radius * 2 + 1):
            result |= padded[
                y_offset : y_offset + height,
                x_offset : x_offset + width,
            ]
    return result


@lru_cache(maxsize=None)
def ellipse_mask(spec: tuple[float, float, float, float]) -> np.ndarray:
    center_x, center_y, radius_x, radius_y = spec
    y_grid, x_grid = np.ogrid[:CANVAS_HEIGHT, :CANVAS_WIDTH]
    return ((x_grid - center_x) / radius_x) ** 2 + (
        (y_grid - center_y) / radius_y
    ) ** 2 <= 1.0


def neutral_feature_footprint(base: np.ndarray) -> np.ndarray:
    """Extract Kotonoha's neutral brows, eyes/irises, and mouth footprint.

    A fixed semantic layout plus local detail is safer than accepting any broad
    face rectangle.  The resulting footprint is used only to ensure the opaque
    core of every alternate fully replaces the old neutral features; it never
    dictates the expression artwork itself.
    """

    left, top, right, bottom = (365, 220, 665, 430)
    crop = base[top:bottom, left:right]
    rgb_u8 = crop[:, :, :3]
    rgb = rgb_u8.astype(np.int16)
    blurred = np.asarray(
        Image.fromarray(rgb_u8, "RGB").filter(ImageFilter.GaussianBlur(2.0)),
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

    eyes = ellipse(443, 306, 55, 32) | ellipse(558, 296, 55, 32)
    brows = ellipse(443, 270, 50, 12) | ellipse(553, 263, 47, 12)
    mouth = ellipse(507, 383, 55, 25)
    dark_ink = (luminance <= 115) & (rgb.max(axis=2) <= 175)
    purple_iris = (blue - red >= 12) & (blue - green >= 5) & (blue >= 70) & (red >= 40)
    pale_feature = (rgb.min(axis=2) >= 205) & (channel_spread <= 40)
    warm_feature = (red - green >= 18) & (red - blue >= 10) & (luminance <= 190)
    local_feature = (
        (eyes & ((local_detail >= 14) | dark_ink | purple_iris | pale_feature))
        | (brows & ((local_detail >= 10) | dark_ink | purple_iris))
        | (mouth & ((local_detail >= 10) | dark_ink | warm_feature | pale_feature))
    )

    footprint = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH), dtype=bool)
    footprint[top:bottom, left:right] = local_feature
    footprint = dilate_mask(footprint, 1)
    return footprint & (base[:, :, 3] == 255)


def shifted_correlation(
    values: np.ndarray,
    support: np.ndarray,
    dy: int,
    dx: int,
) -> float | None:
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


def periodicity_scores(
    values: np.ndarray,
    support: np.ndarray,
) -> tuple[float, int | None, float, int | None]:
    """Measure alternating checker tiles and repeating two-axis grid lines."""

    bounds = mask_bbox(support)
    if bounds is None or int(support.sum()) < 2_000:
        return 0.0, None, 0.0, None
    left, top, right, bottom = bounds
    local_support = support[top:bottom, left:right]
    difference = values[top:bottom, left:right].astype(np.float32)
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


def composite_periodicity_scores(
    composite: np.ndarray,
    base: np.ndarray,
    support: np.ndarray,
) -> tuple[float, int | None, float, int | None]:
    weights = np.asarray((0.2126, 0.7152, 0.0722), dtype=np.float32)
    difference = (
        composite[:, :, :3].astype(np.float32) - base[:, :, :3].astype(np.float32)
    ) @ weights
    return periodicity_scores(difference, support)


def standalone_periodicity_scores(
    pixels: np.ndarray,
    support: np.ndarray,
) -> tuple[float, int | None, float, int | None]:
    """Seek a baked checker/grid in a standalone pose conservatively.

    Removing a broad Gaussian baseline leaves small periodic texture while
    suppressing normal character shading.  Both axes must agree before either
    score is considered suspicious.
    """

    luminance = np.asarray(
        Image.fromarray(pixels[:, :, :3], "RGB").convert("L"), dtype=np.float32
    )
    baseline = np.asarray(
        Image.fromarray(luminance.astype(np.uint8), "L").filter(
            ImageFilter.GaussianBlur(6.0)
        ),
        dtype=np.float32,
    )
    return periodicity_scores(luminance - baseline, support)


def residue_masks(pixels: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return conservative low-alpha black/white and vivid-magenta mattes."""

    alpha = pixels[:, :, 3]
    rgb = pixels[:, :, :3].astype(np.int16)
    red, green, blue = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    low_alpha = (alpha > 0) & (alpha <= 64)
    channel_spread = rgb.max(axis=2) - rgb.min(axis=2)
    near_black = low_alpha & (rgb.max(axis=2) <= 8)
    near_white = low_alpha & (rgb.min(axis=2) >= 247) & (channel_spread <= 4)

    # Kotonoha legitimately uses lavender hair and violet irises.  Only the
    # near-electric corner of magenta is treated as chroma-key residue.
    vivid_magenta = (
        (alpha > 3)
        & (red >= 200)
        & (blue >= 200)
        & (green <= 80)
        & (np.minimum(red, blue) - green >= 120)
    )
    return near_black, near_white, vivid_magenta


def validate_character_components(
    visible: np.ndarray,
    label: str,
    report: ValidationReport,
) -> tuple[int, int, int, float]:
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
        f"{label}: silhouette is fragmented into {len(areas)} components; "
        f"limit={CHARACTER_COMPONENT_LIMIT}, largest={areas[:10]}",
    )
    report.check(
        dominant_ratio >= CHARACTER_DOMINANT_COMPONENT_MIN,
        f"{label}: dominant component contains only {dominant_ratio:.3%} of "
        f"visible alpha ({largest}/{visible_count}); detached={detached}",
    )
    report.check(
        not small_detached,
        f"{label}: detached alpha specks found; areas={small_detached[:20]} "
        f"(minimum intentional detached area is {CHARACTER_DETACHED_COMPONENT_MIN_AREA})",
    )
    return len(areas), largest, detached, dominant_ratio


def validate_character_residue(
    pixels: np.ndarray,
    label: str,
    report: ValidationReport,
) -> tuple[int, int, int, int]:
    alpha = pixels[:, :, 3]
    near_black, near_white, vivid_magenta = residue_masks(pixels)
    low_alpha_count = int(np.count_nonzero((alpha > 0) & (alpha <= 64)))
    black_count = int(near_black.sum())
    white_count = int(near_white.sum())
    magenta_count = int(vivid_magenta.sum())
    black_ratio = black_count / max(1, low_alpha_count)
    white_ratio = white_count / max(1, low_alpha_count)
    report.check(
        black_count <= 512 and black_ratio <= 0.12,
        f"{label}: suspicious low-alpha black matte covers "
        f"{black_count}/{low_alpha_count} edge pixels ({black_ratio:.2%})",
    )
    report.check(
        white_count <= 512 and white_ratio <= 0.12,
        f"{label}: suspicious low-alpha white matte covers "
        f"{white_count}/{low_alpha_count} edge pixels ({white_ratio:.2%})",
    )
    report.check(
        magenta_count == 0,
        f"{label}: {magenta_count} visible pixels look like vivid magenta "
        "chroma-key residue",
    )
    return low_alpha_count, black_count, white_count, magenta_count


def load_rgba(path: Path, label: str, report: ValidationReport) -> np.ndarray | None:
    if not path.is_file() or path.is_symlink():
        report.error(f"{label}: missing or unsafe PNG: {path}")
        return None
    try:
        with Image.open(path) as image:
            report.check(
                image.format == "PNG",
                f"{label}: format is {image.format!r}, expected PNG: {path}",
            )
            if image.mode != "RGBA" or image.size != CANVAS_SIZE:
                report.error(
                    f"{label}: expected stored RGBA {CANVAS_SIZE}, got "
                    f"{image.mode} {image.size}: {path}"
                )
                return None
            pixels = np.asarray(image, dtype=np.uint8).copy()
    except (OSError, ValueError) as exc:
        report.error(f"{label}: cannot decode {path}: {exc}")
        return None

    alpha = pixels[:, :, 3]
    hidden_rgb = (alpha == 0) & np.any(pixels[:, :, :3] != 0, axis=2)
    hidden_count = int(hidden_rgb.sum())
    report.check(
        hidden_count == 0,
        f"{label}: {hidden_count} fully transparent pixels retain RGB matte "
        f"data; first={format_bbox(mask_bbox(hidden_rgb))}",
    )
    return pixels


def validate_manifest(sprite_root: Path, report: ValidationReport) -> None:
    expected = expected_asset_names()
    raster_suffixes = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tga", ".gif"}
    actual = {
        path.name
        for path in sprite_root.glob("*.png")
        if path.is_file() and not path.is_symlink()
    }
    unsafe = sorted(
        path.name for path in sprite_root.glob("*.png") if path.is_symlink()
    )
    report.check(
        actual == expected,
        "Kotonoha production PNG manifest is not the exact 47-file bank "
        "(2 original bases + 42 conditioned faces + 3 poses); "
        f"missing={sorted(expected - actual)} unexpected={sorted(actual - expected)}",
    )
    report.check(
        not unsafe,
        f"Kotonoha production bank contains unsafe PNG symlinks: {unsafe}",
    )
    unexpected_rasters = sorted(
        str(path.relative_to(sprite_root))
        for path in sprite_root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in raster_suffixes
        and not (path.parent == sprite_root and path.name in expected)
    )
    report.check(
        not unexpected_rasters,
        "Kotonoha production folder contains raster files outside the exact "
        f"top-level allowlist: {unexpected_rasters}",
    )

    # These patterns catch obsolete iterations even if somebody changed their
    # extension or parked them alongside production assets.
    obsolete = sorted(
        path.name
        for path in sprite_root.iterdir()
        if path.is_file()
        and (
            re.search(
                r"(?:^|[_-])(?:old|legacy|draft|temp|backup|bak)(?:[_\.-]|$)",
                path.name,
                re.I,
            )
            or path.name.startswith(("forward_", "neut_face_base", "work_face_base"))
            or (
                re.fullmatch(r"face_[a-z0-9_]+\.png", path.name, re.I)
                and not path.stem.endswith(("_casual", "_work"))
            )
        )
    )
    report.check(
        not obsolete,
        f"obsolete/unconditioned Kotonoha sprite iteration(s) remain: {obsolete}",
    )


def validate_bases(
    sprite_root: Path,
    report: ValidationReport,
) -> dict[str, np.ndarray]:
    bases: dict[str, np.ndarray] = {}
    for outfit in OUTFITS:
        path = sprite_root / outfit.base_name
        label = f"kotonoha/{outfit.name}/base"
        pixels = load_rgba(path, label, report)
        if pixels is None:
            continue

        expected_file_digest, expected_pixel_digest = ORIGINAL_BASE_DIGESTS[
            outfit.base_name
        ]
        try:
            actual_file_digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as exc:
            report.error(f"{label}: cannot hash original file: {exc}")
            actual_file_digest = "unavailable"
        actual_pixel_digest = hashlib.sha256(pixels.tobytes()).hexdigest()
        file_is_exact = actual_file_digest == expected_file_digest
        pixels_are_exact = actual_pixel_digest == expected_pixel_digest
        report.check(
            file_is_exact,
            f"{label}: original {outfit.base_name} file changed; "
            f"sha256={actual_file_digest}, expected={expected_file_digest}",
        )
        report.check(
            pixels_are_exact,
            f"{label}: decoded original pixels changed; "
            f"sha256={actual_pixel_digest}, expected={expected_pixel_digest}",
        )

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
                f"{label}: unsafe top/horizontal edge contact; bbox={format_bbox(bounds)}",
            )
            report.check(
                bottom == CANVAS_HEIGHT,
                f"{label}: original mid-thigh crop must reach the canvas baseline; "
                f"bbox={format_bbox(bounds)}",
            )

        components, _largest, detached, dominant_ratio = validate_character_components(
            visible, label, report
        )
        low_alpha, black, white, magenta = validate_character_residue(
            pixels, label, report
        )
        bases[outfit.name] = pixels
        report.note(
            f"{label}: exact-file={'yes' if file_is_exact else 'NO'} "
            f"exact-pixels={'yes' if pixels_are_exact else 'NO'} "
            f"bbox={format_bbox(bounds)} "
            f"visible={int(visible.sum())} components={components} "
            f"dominant={dominant_ratio:.3%} detached={detached} "
            f"low-alpha={low_alpha} black={black} white={white} magenta={magenta}"
        )
    return bases


def validate_fixed_face_mask(
    alpha: np.ndarray,
    base: np.ndarray,
    neutral_features: np.ndarray,
    label: str,
    report: ValidationReport,
) -> None:
    visible = alpha > 0
    opaque = alpha == 255
    partial = visible & ~opaque
    bounds = mask_bbox(visible)
    levels = len(np.unique(alpha))
    component_areas = connected_component_areas(visible)

    report.check(bool(np.any(visible)), f"{label}: fixed mask is empty")
    report.check(
        int(opaque.sum()) >= MIN_FACE_OPAQUE_PIXELS,
        f"{label}: opaque core has only {int(opaque.sum())} pixels; "
        f"minimum={MIN_FACE_OPAQUE_PIXELS}",
    )
    report.check(
        int(partial.sum()) >= MIN_FACE_PARTIAL_PIXELS,
        f"{label}: feather has only {int(partial.sum())} partial-alpha pixels; "
        f"minimum={MIN_FACE_PARTIAL_PIXELS}",
    )
    report.check(
        levels == EXPECTED_FACE_ALPHA_LEVELS,
        f"{label}: mask has {levels} alpha levels; expected all "
        f"{EXPECTED_FACE_ALPHA_LEVELS} uint8 levels for the approved feather",
    )
    report.check(
        len(component_areas) == 1,
        f"{label}: mask has {len(component_areas)} connected alpha components; "
        f"areas={component_areas[:20]}",
    )

    if bounds is not None:
        left, top, right, bottom = bounds
        limit_left, limit_top, limit_right, limit_bottom = FACE_PATCH_LIMITS
        width = right - left
        height = bottom - top
        center_x = (left + right) / 2.0
        center_y = (top + bottom) / 2.0
        report.check(
            left >= limit_left
            and top >= limit_top
            and right <= limit_right
            and bottom <= limit_bottom,
            f"{label}: face patch escapes registered limits {FACE_PATCH_LIMITS}; "
            f"bbox={format_bbox(bounds)}",
        )
        report.check(
            FACE_MASK_WIDTH_RANGE[0] <= width <= FACE_MASK_WIDTH_RANGE[1]
            and FACE_MASK_HEIGHT_RANGE[0] <= height <= FACE_MASK_HEIGHT_RANGE[1],
            f"{label}: implausible face-mask dimensions {width}x{height}; expected "
            f"width={FACE_MASK_WIDTH_RANGE}, height={FACE_MASK_HEIGHT_RANGE}",
        )
        report.check(
            abs(center_x - FACE_CENTER[0]) <= FACE_CENTER_TOLERANCE[0]
            and abs(center_y - FACE_CENTER[1]) <= FACE_CENTER_TOLERANCE[1],
            f"{label}: mask center ({center_x:.1f},{center_y:.1f}) is not aligned "
            f"to Kotonoha's face near {FACE_CENTER}",
        )
        report.check(
            left > 0 and top > 0 and right < CANVAS_WIDTH and bottom < CANVAS_HEIGHT,
            f"{label}: face mask touches a canvas edge; bbox={format_bbox(bounds)}",
        )

    border_count = int(
        np.count_nonzero(alpha[0, :])
        + np.count_nonzero(alpha[-1, :])
        + np.count_nonzero(alpha[:, 0])
        + np.count_nonzero(alpha[:, -1])
    )
    report.check(
        border_count == 0,
        f"{label}: {border_count} nontransparent samples touch the canvas edge",
    )
    outside_base = (alpha > 0) & (base[:, :, 3] == 0)
    report.check(
        not np.any(outside_base),
        f"{label}: {int(outside_base.sum())} mask pixels extend outside the "
        f"base silhouette; bbox={format_bbox(mask_bbox(outside_base))}",
    )
    # A handful of antialiased outer-brow samples in the source footprint land
    # at 243-254 in the approved Gaussian feather.  At >=240 the old feature's
    # maximum possible contribution is below 6%; lower alpha is a real leak.
    uncovered = neutral_features & (alpha < 240)
    report.check(
        not np.any(uncovered),
        f"{label}: >=240-alpha replacement misses {int(uncovered.sum())} canonical neutral "
        "brow/eye/iris/mouth pixels, allowing the old face to leak through; "
        f"bbox={format_bbox(mask_bbox(uncovered))}",
    )
    report.note(
        f"{label}: bbox={format_bbox(bounds)} visible={int(visible.sum())} "
        f"opaque={int(opaque.sum())} partial={int(partial.sum())} levels={levels}"
    )


def validate_face_layer_residue(
    layer: np.ndarray,
    composite: np.ndarray,
    base: np.ndarray,
    label: str,
    report: ValidationReport,
) -> tuple[float, int | None, float, int | None, int, int, int]:
    alpha = layer[:, :, 3]
    rgb = layer[:, :, :3].astype(np.int16)
    visible = alpha > 0
    partial = (alpha > 0) & (alpha < 255)
    color_delta = np.max(
        np.abs(composite[:, :, :3].astype(np.int16) - base[:, :, :3].astype(np.int16)),
        axis=2,
    )
    visibly_changed_fringe = partial & (color_delta >= 24)
    channel_spread = rgb.max(axis=2) - rgb.min(axis=2)
    broad_black = visible & (rgb.max(axis=2) <= 8)
    broad_white = visible & (rgb.min(axis=2) >= 247) & (channel_spread <= 4)
    authored_seed = alpha >= 160
    supported_black = components_connected_to_seed(
        broad_black, broad_black & authored_seed
    )
    supported_white = components_connected_to_seed(
        broad_white, broad_white & authored_seed
    )
    fringe_black = visibly_changed_fringe & broad_black & ~supported_black
    fringe_white = visibly_changed_fringe & broad_white & ~supported_white
    black_count = int(fringe_black.sum())
    white_count = int(fringe_white.sum())
    visible_count = int(visible.sum())
    broad_black_ratio = int(broad_black.sum()) / max(1, visible_count)
    broad_white_ratio = int(broad_white.sum()) / max(1, visible_count)
    _low_black, _low_white, vivid_magenta = residue_masks(layer)
    magenta_count = int(vivid_magenta.sum())

    report.check(
        black_count <= 8,
        f"{label}: {black_count} visibly changed, unanchored feather pixels "
        "look like black matte residue; limit=8",
    )
    report.check(
        white_count <= 8,
        f"{label}: {white_count} visibly changed, unanchored feather pixels "
        "look like white matte residue; limit=8",
    )
    report.check(
        broad_black_ratio <= 0.20,
        f"{label}: near-black pixels occupy {broad_black_ratio:.2%} of the face "
        "plate; likely a black background/matte",
    )
    report.check(
        broad_white_ratio <= 0.16,
        f"{label}: near-white pixels occupy {broad_white_ratio:.2%} of the face "
        "plate; likely a white background/matte",
    )
    report.check(
        magenta_count == 0,
        f"{label}: {magenta_count} pixels look like vivid magenta chroma-key residue",
    )

    checker, checker_tile, grid, grid_tile = composite_periodicity_scores(
        composite, base, alpha == 255
    )
    report.check(
        checker < CHECKER_PERIODICITY_LIMIT,
        f"{label}: checker-like two-axis periodicity detected "
        f"(score={checker:.3f}, tile={checker_tile}px)",
    )
    report.check(
        grid < GRID_PERIODICITY_LIMIT,
        f"{label}: repeating two-axis grid residue detected "
        f"(score={grid:.3f}, tile={grid_tile}px)",
    )
    return (
        checker,
        checker_tile,
        grid,
        grid_tile,
        black_count,
        white_count,
        magenta_count,
    )


def validate_face_bank(
    sprite_root: Path,
    bases: dict[str, np.ndarray],
    report: ValidationReport,
) -> dict[tuple[str, str], np.ndarray]:
    composites: dict[tuple[str, str], np.ndarray] = {}
    outfit_masks: dict[str, np.ndarray] = {}

    for outfit in OUTFITS:
        base = bases.get(outfit.name)
        fixed_alpha: np.ndarray | None = None
        fixed_source: str | None = None
        neutral_features = neutral_feature_footprint(base) if base is not None else None
        if neutral_features is not None:
            report.check(
                int(neutral_features.sum()) >= 10_000,
                f"kotonoha/{outfit.name}/neutral-features: extracted only "
                f"{int(neutral_features.sum())} pixels; face registration audit "
                "cannot be trusted",
            )

        changed_counts: list[int] = []
        checker_metrics: list[tuple[float, str, int | None]] = []
        grid_metrics: list[tuple[float, str, int | None]] = []
        fringe_black_counts: list[int] = []
        fringe_white_counts: list[int] = []
        magenta_counts: list[int] = []
        outfit_composites: dict[str, np.ndarray] = {}
        signatures: dict[bytes, str] = {}

        for token in FACE_TOKENS:
            filename = outfit.face_name(token)
            label = f"kotonoha/{outfit.name}/face/{token}"
            layer = load_rgba(sprite_root / filename, label, report)
            if layer is None:
                continue
            alpha = layer[:, :, 3]

            if token == "neut":
                report.check(
                    not np.any(layer),
                    f"{label}: neutral overlay must be entirely zero RGBA so "
                    "the original base is preserved exactly",
                )
            else:
                report.check(
                    bool(np.any(alpha)),
                    f"{label}: alternate expression overlay is fully transparent",
                )
                if fixed_alpha is None:
                    fixed_alpha = alpha.copy()
                    fixed_source = filename
                    if base is not None and neutral_features is not None:
                        validate_fixed_face_mask(
                            fixed_alpha,
                            base,
                            neutral_features,
                            f"kotonoha/{outfit.name}/face-mask",
                            report,
                        )
                else:
                    report.check(
                        np.array_equal(alpha, fixed_alpha),
                        f"{label}: alpha differs from fixed mask {fixed_source}; "
                        f"all 20 {outfit.name} alternates must share one mask",
                    )

            if base is None:
                continue
            outside_base = (alpha > 0) & (base[:, :, 3] == 0)
            report.check(
                not np.any(outside_base),
                f"{label}: {int(outside_base.sum())} pixels extend outside the "
                f"original base alpha; bbox={format_bbox(mask_bbox(outside_base))}",
            )
            composite = alpha_composite(base, layer)
            composites[(outfit.name, token)] = composite
            outfit_composites[token] = composite
            report.check(
                np.array_equal(composite[:, :, 3], base[:, :, 3]),
                f"{label}: composite changes the original base alpha/silhouette",
            )
            changed = int(changed_mask(composite, base).sum())
            if token == "neut":
                report.check(
                    changed == 0 and np.array_equal(composite, base),
                    f"{label}: neutral composite changes {changed} original pixels",
                )
            else:
                report.check(
                    changed >= MIN_ALTERNATE_CHANGED_PIXELS,
                    f"{label}: only {changed} pixels differ from neutral; "
                    f"minimum={MIN_ALTERNATE_CHANGED_PIXELS}",
                )
                effective_ratio = changed / max(1, int((alpha > 0).sum()))
                report.check(
                    effective_ratio >= 0.12,
                    f"{label}: only {effective_ratio:.1%} of the fixed plate has "
                    "a visible effect; likely padded/empty output",
                )
                changed_counts.append(changed)
                (
                    checker,
                    checker_tile,
                    grid,
                    grid_tile,
                    fringe_black,
                    fringe_white,
                    magenta,
                ) = validate_face_layer_residue(layer, composite, base, label, report)
                checker_metrics.append((checker, token, checker_tile))
                grid_metrics.append((grid, token, grid_tile))
                fringe_black_counts.append(fringe_black)
                fringe_white_counts.append(fringe_white)
                magenta_counts.append(magenta)

            signature = hashlib.sha256(composite.tobytes()).digest()
            previous = signatures.get(signature)
            report.check(
                previous is None,
                f"{label}: composite duplicates {previous}; expressions must be "
                "pairwise distinct",
            )
            signatures[signature] = label

        # A hash catches exact duplicates.  This catches nominally different
        # files containing only microscopic/noise differences.
        for first_token, second_token in combinations(outfit_composites, 2):
            first = outfit_composites[first_token]
            second = outfit_composites[second_token]
            difference_count = int(changed_mask(first, second).sum())
            minimum = (
                MIN_ALTERNATE_CHANGED_PIXELS
                if "neut" in {first_token, second_token}
                else MIN_PAIRWISE_CHANGED_PIXELS
            )
            report.check(
                difference_count >= minimum,
                f"kotonoha/{outfit.name}/pair/{first_token}-{second_token}: "
                f"only {difference_count} pixels differ; minimum={minimum}",
            )

        if fixed_alpha is not None:
            outfit_masks[outfit.name] = fixed_alpha
        if changed_counts:
            strongest_checker = max(checker_metrics, default=(0.0, "none", None))
            strongest_grid = max(grid_metrics, default=(0.0, "none", None))
            report.note(
                f"kotonoha/{outfit.name}/alternates: distinct={len(signatures)}/"
                f"{len(FACE_TOKENS)} changed={min(changed_counts)}-"
                f"{max(changed_counts)} checker-max={strongest_checker[0]:.3f}/"
                f"{strongest_checker[1]}@{strongest_checker[2]}px "
                f"grid-max={strongest_grid[0]:.3f}/"
                f"{strongest_grid[1]}@{strongest_grid[2]}px "
                f"fringe-black-max={max(fringe_black_counts, default=0)} "
                f"fringe-white-max={max(fringe_white_counts, default=0)} "
                f"magenta-max={max(magenta_counts, default=0)}"
            )

    casual_mask = outfit_masks.get("casual")
    work_mask = outfit_masks.get("work")
    if casual_mask is not None and work_mask is not None:
        casual_visible = casual_mask > 0
        work_visible = work_mask > 0
        intersection = int((casual_visible & work_visible).sum())
        union = int((casual_visible | work_visible).sum())
        iou = intersection / max(1, union)
        casual_bounds = mask_bbox(casual_visible)
        work_bounds = mask_bbox(work_visible)
        if casual_bounds is not None and work_bounds is not None:
            casual_center = (
                (casual_bounds[0] + casual_bounds[2]) / 2.0,
                (casual_bounds[1] + casual_bounds[3]) / 2.0,
            )
            work_center = (
                (work_bounds[0] + work_bounds[2]) / 2.0,
                (work_bounds[1] + work_bounds[3]) / 2.0,
            )
            center_delta = math.dist(casual_center, work_center)
            report.check(
                center_delta <= 12.0,
                "kotonoha/cross-outfit masks: centers differ by "
                f"{center_delta:.2f}px; casual={casual_center}, work={work_center}",
            )
        else:
            center_delta = float("inf")
        report.check(
            iou >= 0.80,
            f"kotonoha/cross-outfit masks: overlap IoU={iou:.3f}; expected >=0.800",
        )
        report.note(
            f"kotonoha/cross-outfit masks: IoU={iou:.3f} "
            f"center-delta={center_delta:.2f}px"
        )

    return composites


def silhouette_boundary(visible: np.ndarray) -> np.ndarray:
    outside = ~visible
    adjacent_outside = np.zeros_like(visible)
    adjacent_outside[1:, :] |= outside[:-1, :]
    adjacent_outside[:-1, :] |= outside[1:, :]
    adjacent_outside[:, 1:] |= outside[:, :-1]
    adjacent_outside[:, :-1] |= outside[:, 1:]
    return visible & adjacent_outside


def head_profile(pixels: np.ndarray) -> HeadProfile | None:
    alpha = pixels[:, :, 3]
    visible = alpha > 0
    bounds = mask_bbox(visible)
    if bounds is None:
        return None
    _left, top, _right, _bottom = bounds
    band_top = min(CANVAS_HEIGHT, top + 40)
    band_bottom = min(CANVAS_HEIGHT, top + 430)
    widths: list[int] = []
    centers: list[float] = []
    for row_index in range(band_top, band_bottom):
        columns = np.flatnonzero(visible[row_index])
        if columns.size:
            widths.append(int(columns[-1] - columns[0] + 1))
            centers.append(float(columns[0] + columns[-1]) / 2.0)
    if not widths:
        return None

    rgb = pixels[:, :, :3].astype(np.int16)
    red, green, blue = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    face_window = ellipse_mask((FACE_CENTER[0], FACE_CENTER[1], 175.0, 190.0))
    skin = (
        visible
        & face_window
        & (red >= 150)
        & (green >= 100)
        & (blue >= 75)
        & (red >= green + 5)
        & (green >= blue - 8)
        & (red - blue >= 18)
        & (red - blue <= 130)
    )
    skin_rows, skin_columns = np.nonzero(skin)
    return HeadProfile(
        top=top,
        center_x=float(np.median(centers)),
        median_width=float(np.median(widths)),
        upper_area=int(visible[top:band_bottom].sum()),
        skin_area=int(skin.sum()),
        skin_center_x=(float(np.median(skin_columns)) if skin_columns.size else None),
        skin_center_y=(float(np.median(skin_rows)) if skin_rows.size else None),
    )


def validate_poses(
    sprite_root: Path,
    bases: dict[str, np.ndarray],
    report: ValidationReport,
) -> dict[str, np.ndarray]:
    pose_images: dict[str, np.ndarray] = {}
    pose_signatures: dict[bytes, str] = {}

    for pose in POSES:
        label = f"kotonoha/{pose.outfit}/{pose.attribute}"
        pixels = load_rgba(sprite_root / pose.filename, label, report)
        if pixels is None:
            continue
        pose_images[pose.filename] = pixels
        alpha = pixels[:, :, 3]
        visible = alpha > 0
        bounds = mask_bbox(visible)
        report.check(bool(np.any(visible)), f"{label}: pose is fully transparent")
        report.check(
            bool(np.any(~visible)), f"{label}: pose has no transparent exterior"
        )
        if bounds is not None:
            left, top, right, bottom = bounds
            report.check(
                left >= 12 and top >= 20 and right <= CANVAS_WIDTH - 12,
                f"{label}: pose is cropped or lacks a safe top/horizontal margin; "
                f"bbox={format_bbox(bounds)}",
            )
            report.check(
                bottom == CANVAS_HEIGHT,
                f"{label}: mid-thigh crop must meet the shared bottom baseline; "
                f"bbox={format_bbox(bounds)}",
            )
            report.check(
                bottom - top >= 1_380,
                f"{label}: visible height is only {bottom - top}px; expected a "
                "registered mid-thigh-and-up sprite, not a small/full-body figure",
            )

        components, _largest, detached, dominant_ratio = validate_character_components(
            visible, label, report
        )
        low_alpha, black, white, magenta = validate_character_residue(
            pixels, label, report
        )

        visible_count = int(visible.sum())
        soft = visible & (alpha < 255)
        soft_count = int(soft.sum())
        soft_ratio = soft_count / max(1, visible_count)
        boundary = silhouette_boundary(visible)
        boundary_count = int(boundary.sum())
        soft_boundary_ratio = int((boundary & (alpha < 250)).sum()) / max(
            1, boundary_count
        )
        report.check(
            soft_count >= 500 and 0.001 <= soft_ratio <= 0.12,
            f"{label}: unhealthy soft-alpha coverage ({soft_count} pixels, "
            f"{soft_ratio:.3%} of visible art)",
        )
        report.check(
            soft_boundary_ratio >= 0.30,
            f"{label}: only {soft_boundary_ratio:.1%} of outer boundary is "
            "softened; likely a hard cutout",
        )

        checker, checker_tile, grid, grid_tile = standalone_periodicity_scores(
            pixels, alpha >= 160
        )
        # Standalone art has legitimate fabric/hair texture, so these limits are
        # higher than base-difference checks while still rejecting a strong
        # baked transparency checker or regular two-axis extraction grid.
        report.check(
            checker < 0.60,
            f"{label}: strong checker periodicity detected in opaque art "
            f"(score={checker:.3f}, tile={checker_tile}px)",
        )
        report.check(
            grid < 0.82,
            f"{label}: strong two-axis grid periodicity detected in opaque art "
            f"(score={grid:.3f}, tile={grid_tile}px)",
        )

        base = bases.get(pose.outfit)
        profile = head_profile(pixels)
        reference_profile = head_profile(base) if base is not None else None
        bottom_area = int(visible[-64:, :].sum())
        if base is not None:
            base_visible = base[:, :, 3] > 0
            base_count = int(base_visible.sum())
            base_bottom_area = int(base_visible[-64:, :].sum())
            area_ratio = visible_count / max(1, base_count)
            bottom_ratio = bottom_area / max(1, base_bottom_area)
            report.check(
                0.62 <= area_ratio <= 1.55,
                f"{label}: visible-area ratio to {pose.outfit} base is "
                f"{area_ratio:.3f}; expected 0.62-1.55 for the same scale/framing",
            )
            report.check(
                0.50 <= bottom_ratio <= 1.90,
                f"{label}: bottom-64px occupancy ratio is {bottom_ratio:.3f} "
                "(expected 0.50-1.90); "
                "the crop does not read as the same mid-thigh framing",
            )
        else:
            area_ratio = float("nan")
            bottom_ratio = float("nan")

        if profile is None:
            report.error(f"{label}: cannot derive head-scale profile")
            head_width_ratio = float("nan")
            head_area_ratio = float("nan")
            skin_ratio = float("nan")
        elif reference_profile is not None:
            head_width_ratio = profile.median_width / max(
                1.0, reference_profile.median_width
            )
            head_area_ratio = profile.upper_area / max(1, reference_profile.upper_area)
            skin_ratio = profile.skin_area / max(1, reference_profile.skin_area)
            report.check(
                abs(profile.top - reference_profile.top) <= 75,
                f"{label}: head top shifts {profile.top - reference_profile.top:+d}px "
                f"from the {pose.outfit} base; pose is vertically misregistered",
            )
            report.check(
                abs(profile.center_x - reference_profile.center_x) <= 70,
                f"{label}: upper-silhouette center shifts "
                f"{profile.center_x - reference_profile.center_x:+.1f}px from base",
            )
            report.check(
                0.72 <= head_width_ratio <= 1.35,
                f"{label}: head-width proxy ratio is {head_width_ratio:.3f}; "
                "expected 0.72-1.35 at the established sprite scale",
            )
            report.check(
                0.62 <= head_area_ratio <= 1.48,
                f"{label}: upper-head area ratio is {head_area_ratio:.3f}; "
                "likely inconsistent head scale or framing",
            )
            report.check(
                profile.skin_area >= 8_000 and 0.48 <= skin_ratio <= 1.75,
                f"{label}: face-skin proxy is {profile.skin_area}px / "
                f"ratio={skin_ratio:.3f}; head may be too small, too large, or shifted",
            )
            if (
                profile.skin_center_x is not None
                and reference_profile.skin_center_x is not None
                and profile.skin_center_y is not None
                and reference_profile.skin_center_y is not None
            ):
                skin_shift = math.dist(
                    (profile.skin_center_x, profile.skin_center_y),
                    (
                        reference_profile.skin_center_x,
                        reference_profile.skin_center_y,
                    ),
                )
                report.check(
                    skin_shift <= 85.0,
                    f"{label}: face-skin center shifts {skin_shift:.1f}px from "
                    f"the {pose.outfit} base; likely head misalignment",
                )
        else:
            head_width_ratio = float("nan")
            head_area_ratio = float("nan")
            skin_ratio = float("nan")

        signature = hashlib.sha256(pixels.tobytes()).digest()
        previous = pose_signatures.get(signature)
        report.check(
            previous is None,
            f"{label}: standalone pose duplicates {previous}",
        )
        pose_signatures[signature] = label
        report.note(
            f"{label}: bbox={format_bbox(bounds)} visible={visible_count} "
            f"components={components} dominant={dominant_ratio:.3%} "
            f"detached={detached} soft={soft_ratio:.3%} "
            f"soft-boundary={soft_boundary_ratio:.1%} bottom64={bottom_area} "
            f"area-ratio={area_ratio:.3f} bottom-ratio={bottom_ratio:.3f} "
            f"head-width={head_width_ratio:.3f} head-area={head_area_ratio:.3f} "
            f"skin={skin_ratio:.3f} checker={checker:.3f}@{checker_tile}px "
            f"grid={grid:.3f}@{grid_tile}px low-alpha={low_alpha} "
            f"black={black} white={white} magenta={magenta}"
        )

    return pose_images


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
        r'"(?P<asset>mod_assets/char_sprites/kotonoha/[^"\n]+\.png)"'
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
        layered = indented_block(source, "layeredimage kotonoha:", 0)
        outfit_group = indented_block(layered, "    group outfit:", 4)
        face_group = indented_block(layered, "    group face:", 4)
    except (OSError, UnicodeError, ValueError) as exc:
        report.error(f"cannot audit Kotonoha definition: {exc}")
        return

    transform_count = len(
        re.findall(r"^transform kotonoha_sprite_size:\s*$", source, re.MULTILINE)
    )
    try:
        transform = indented_block(source, "transform kotonoha_sprite_size:", 0)
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
        "Kotonoha definition: kotonoha_sprite_size must contain exactly "
        '`fit "contain"` and `xysize (640, 960)`; '
        f"occurrences={transform_count} body={transform_lines}",
    )
    at_clauses = re.findall(r"^\s+at\s+(.+?)\s*$", layered, re.MULTILINE)
    report.check(
        at_clauses == ["kotonoha_sprite_size, Flatten"],
        "Kotonoha definition: layeredimage must use exactly "
        f"`at kotonoha_sprite_size, Flatten`; actual={at_clauses}",
    )
    forbidden_adjustors = sorted(
        set(
            re.findall(
                r"\b(?:fit|xoffset|yoffset|xzoom|yzoom|zoom|xsize|ysize|xysize|height)\b"
                r"|\bTransform\s*\(",
                layered,
            )
        )
    )
    report.check(
        not forbidden_adjustors,
        "Kotonoha definition: layeredimage contains forbidden per-layer "
        f"size/offset/zoom adjustment(s): {forbidden_adjustors}",
    )
    report.check(
        "    group pose:" not in layered and "pose_" not in layered,
        "Kotonoha definition: fixed poses must remain standalone, not layered "
        "over the default torso/face",
    )

    outfit_records = Counter(parse_attribute_records(outfit_group))
    expected_outfits = Counter(
        {
            AttributeRecord("casual", True, (), OUTFITS[0].base_reference): 1,
            AttributeRecord("work", False, (), OUTFITS[1].base_reference): 1,
        }
    )
    report.check(
        outfit_records == expected_outfits,
        "Kotonoha definition: outfit mapping must be exactly "
        "casual(default)->neutral.png and work->work.png; "
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
        "Kotonoha definition: face attributes differ from the exact 21-token x "
        "2-outfit conditioned contract; "
        f"missing={list((expected_faces - face_records).elements())} "
        f"extra={list((face_records - expected_faces).elements())}",
    )

    reference_pattern = re.compile(r'"(mod_assets/char_sprites/kotonoha/[^"\n]+\.png)"')
    layered_counts = Counter(reference_pattern.findall(layered))
    expected_layered = expected_layered_references()
    report.check(
        set(layered_counts) == expected_layered
        and all(count == 1 for count in layered_counts.values()),
        "Kotonoha definition: layeredimage references are not the exact "
        "2-base + 42-face manifest; "
        f"missing={sorted(expected_layered - set(layered_counts))} "
        f"extra={sorted(set(layered_counts) - expected_layered)} "
        f"duplicates={sorted(ref for ref, count in layered_counts.items() if count != 1)}",
    )

    # Explicit flattened neutrals would override the layered image.  The two
    # legacy names remain available because casual+neut are defaults and work
    # has its own conditioned neut overlay.
    legacy_neutral_headers = re.findall(
        r"^image\s+kotonoha(?:\s+work)?\s+neut\s*=.*$",
        source,
        re.MULTILINE,
    )
    report.check(
        not legacy_neutral_headers,
        "Kotonoha definition: legacy flattened neutral declarations override "
        f"the layered image: {legacy_neutral_headers}",
    )

    pose_pattern = re.compile(
        r"^image\s+kotonoha\s+(?P<outfit>\w+)\s+"
        r"(?P<attribute>pose_\w+)\s*=\s*"
        r'Transform\(\s*"(?P<asset>mod_assets/char_sprites/kotonoha/[^"\n]+\.png)"\s*,'
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
    pose_headers = Counter(
        (match.group("outfit"), match.group("attribute"))
        for match in re.finditer(
            r"^image\s+kotonoha\s+(?P<outfit>\w+)\s+"
            r"(?P<attribute>pose_\w+)\s*=",
            source,
            re.MULTILINE,
        )
    )
    expected_pose_headers = Counter((pose.outfit, pose.attribute) for pose in POSES)
    report.check(
        pose_headers == expected_pose_headers,
        "Kotonoha definition: pose outfit/attribute declarations are not the "
        "exact expected three; "
        f"missing={list((expected_pose_headers - pose_headers).elements())} "
        f"extra={list((pose_headers - expected_pose_headers).elements())}",
    )
    report.check(
        pose_records == expected_pose_records,
        "Kotonoha definition: standalone pose mappings or Transform syntax "
        "differ from the exact contract; "
        f"missing={list((expected_pose_records - pose_records).elements())} "
        f"extra={list((pose_records - expected_pose_records).elements())}",
    )

    all_references = Counter(reference_pattern.findall(source))
    expected_all = expected_layered | {pose.reference for pose in POSES}
    report.check(
        set(all_references) == expected_all
        and all(count == 1 for count in all_references.values()),
        "Kotonoha definition contains obsolete, missing, or duplicate sprite "
        "references; "
        f"missing={sorted(expected_all - set(all_references))} "
        f"extra={sorted(set(all_references) - expected_all)} "
        f"duplicates={sorted(ref for ref, count in all_references.items() if count != 1)}",
    )
    for reference in expected_all:
        asset = sprite_root / Path(reference).name
        report.check(
            asset.is_file() and not asset.is_symlink(),
            f"Kotonoha definition reference does not resolve safely: {reference} "
            f"(expected {asset})",
        )

    report.check(
        bool(
            re.search(
                r"^define\s+ko\s*=\s*DynamicCharacter\([^\n]+"
                r"image\s*=\s*['\"]kotonoha['\"]",
                source,
                re.MULTILINE,
            )
        ),
        "Kotonoha definition: DynamicCharacter image tag `kotonoha` is missing",
    )
    report.note(
        "kotonoha/definition: exact transform, 2 bases, 42 conditioned faces, "
        "3 standalone poses, default casual/neut compatibility, and image tag checked"
    )


def validate_story(story_root: Path, report: ValidationReport) -> None:
    """Ensure existing show statements still resolve under the new attributes."""

    allowed = {
        "casual",
        "work",
        *FACE_TOKENS,
        *(pose.attribute for pose in POSES),
    }
    show_pattern = re.compile(r"^\s*show\s+kotonoha\b(?P<tail>[^#]*)")
    modifier_pattern = re.compile(
        r"\s+(?:at|as|behind|onlayer|zorder|with)\b", re.IGNORECASE
    )
    unknown_uses: list[str] = []
    show_count = 0
    for script_path in sorted(story_root.rglob("*.rpy")):
        try:
            lines = script_path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            report.error(f"cannot read {script_path} for Kotonoha story audit: {exc}")
            continue
        for line_number, line in enumerate(lines, start=1):
            match = show_pattern.match(line)
            if not match:
                continue
            show_count += 1
            attribute_text = modifier_pattern.split(match.group("tail"), maxsplit=1)[0]
            attributes = [token.lstrip("-") for token in attribute_text.split()]
            unknown = [token for token in attributes if token and token not in allowed]
            if unknown:
                relative = script_path.relative_to(PROJECT_ROOT)
                unknown_uses.append(
                    f"{relative}:{line_number}: {', '.join(sorted(set(unknown)))}"
                )
    report.check(
        not unknown_uses,
        "unresolved attributes remain on `show kotonoha` calls:\n"
        + "\n".join(f"  - {entry}" for entry in unknown_uses),
    )
    report.note(f"kotonoha/story: {show_count} `show kotonoha` call(s) audited")


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
    width, height = size
    rows, columns = np.indices((height, width))
    cells = ((columns // 14) + (rows // 14)) % 2
    rgba = np.empty((height, width, 4), dtype=np.uint8)
    rgba[cells == 0] = (82, 86, 96, 255)
    rgba[cells == 1] = (128, 133, 144, 255)
    return Image.fromarray(rgba, "RGBA")


def review_panel(
    sprite: np.ndarray,
    background_kind: str,
    panel_size: tuple[int, int] = (158, 244),
) -> Image.Image:
    art_size = (panel_size[0] - 8, panel_size[1] - 20)
    full_background = make_background(background_kind, CANVAS_SIZE)
    rendered = Image.alpha_composite(full_background, Image.fromarray(sprite, "RGBA"))
    rendered.thumbnail(art_size, Image.Resampling.LANCZOS)
    panel = make_background(background_kind, panel_size)
    panel.alpha_composite(
        rendered,
        (
            (panel_size[0] - rendered.width) // 2,
            panel_size[1] - rendered.height - 4,
        ),
    )
    ImageDraw.Draw(panel).rectangle(
        (0, 0, panel_size[0] - 1, panel_size[1] - 1),
        outline=(72, 77, 89, 255),
    )
    return panel


def build_review_sheet(
    sprite_root: Path,
    output_path: Path,
) -> None:
    backgrounds = ("dark", "light", "checker")
    panel_size = (158, 244)
    label_width = 116
    header_height = 72
    expression_columns = tuple(
        (outfit, background) for outfit in OUTFITS for background in backgrounds
    )
    pose_rows = len(POSES)
    total_rows = len(FACE_TOKENS) + pose_rows
    sheet = Image.new(
        "RGBA",
        (
            label_width + panel_size[0] * len(expression_columns),
            header_height + panel_size[1] * total_rows,
        ),
        (16, 18, 24, 255),
    )
    draw = ImageDraw.Draw(sheet)
    font = load_font(13)
    title_font = load_font(17)
    draw.text(
        (12, 10),
        "KOTONOHA EXPRESSION + MID-THIGH POSE REVIEW",
        fill="white",
        font=title_font,
    )
    for column, (outfit, background) in enumerate(expression_columns):
        center_x = label_width + column * panel_size[0] + panel_size[0] // 2
        draw.text(
            (center_x, 51),
            f"{outfit.name}/{background}",
            fill=(183, 165, 230, 255),
            font=font,
            anchor="mm",
        )

    bases: dict[str, np.ndarray] = {}
    for outfit in OUTFITS:
        with Image.open(sprite_root / outfit.base_name) as image:
            bases[outfit.name] = np.asarray(
                image.convert("RGBA"), dtype=np.uint8
            ).copy()

    for row, token in enumerate(FACE_TOKENS):
        top = header_height + row * panel_size[1]
        draw.text(
            (label_width - 9, top + panel_size[1] // 2),
            token.upper(),
            fill="white",
            font=font,
            anchor="rm",
        )
        for outfit_index, outfit in enumerate(OUTFITS):
            with Image.open(sprite_root / outfit.face_name(token)) as image:
                layer = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
            composite = alpha_composite(bases[outfit.name], layer)
            for background_index, background in enumerate(backgrounds):
                column = outfit_index * len(backgrounds) + background_index
                left = label_width + column * panel_size[0]
                sheet.alpha_composite(
                    review_panel(composite, background, panel_size), (left, top)
                )

    for pose_index, pose in enumerate(POSES):
        row = len(FACE_TOKENS) + pose_index
        top = header_height + row * panel_size[1]
        draw.text(
            (label_width - 9, top + panel_size[1] // 2),
            pose.attribute.replace("pose_", "").upper(),
            fill=(255, 221, 158, 255),
            font=font,
            anchor="rm",
        )
        with Image.open(sprite_root / pose.filename) as image:
            pixels = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
        for background_index, background in enumerate(backgrounds):
            # Center the three background panels in the six-column grid.
            column = background_index + 1
            left = label_width + column * panel_size[0]
            sheet.alpha_composite(
                review_panel(pixels, background, panel_size), (left, top)
            )
            draw.text(
                (left + panel_size[0] // 2, top + 10),
                f"{pose.outfit}/{background}",
                fill="white",
                font=font,
                anchor="mm",
            )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(output_path, format="PNG", compress_level=6)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sprite-root",
        type=Path,
        default=DEFAULT_SPRITE_ROOT,
        help="Kotonoha production/staging sprite directory",
    )
    parser.add_argument(
        "--definitions",
        type=Path,
        default=DEFAULT_DEFINITIONS,
        help="Ren'Py character image declarations to audit",
    )
    parser.add_argument(
        "--story-root",
        type=Path,
        default=DEFAULT_STORY_ROOT,
        help="directory recursively audited for `show kotonoha` calls",
    )
    parser.add_argument(
        "--review-sheet",
        type=Path,
        default=None,
        help="optional contact-sheet output (the validator is otherwise read-only)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sprite_root = args.sprite_root.resolve()
    definitions = args.definitions.resolve()
    story_root = args.story_root.resolve()
    report = ValidationReport()

    if not sprite_root.is_dir():
        report.error(f"Kotonoha sprite directory does not exist: {sprite_root}")
    else:
        validate_manifest(sprite_root, report)
    bases = validate_bases(sprite_root, report)
    validate_face_bank(sprite_root, bases, report)
    validate_poses(sprite_root, bases, report)
    validate_definition(definitions, sprite_root, report)
    if story_root.is_dir():
        validate_story(story_root, report)
    else:
        report.error(f"Kotonoha story audit root does not exist: {story_root}")

    if args.review_sheet is not None:
        output_path = args.review_sheet.resolve()
        try:
            build_review_sheet(sprite_root, output_path)
            report.note(f"kotonoha/review: {output_path}")
        except (OSError, ValueError) as exc:
            report.error(f"cannot write Kotonoha review sheet {output_path}: {exc}")

    output = sys.stderr if report.errors else sys.stdout
    if report.notes:
        print("KOTONOHA SPRITE VALIDATION METRICS", file=output)
        for note in report.notes:
            print(f"  {note}", file=output)

    if report.errors:
        print(
            f"\nKOTONOHA SPRITE VALIDATION FAILED ({len(report.errors)} issue(s))",
            file=output,
        )
        for index, error in enumerate(report.errors, start=1):
            print(
                f"  {index}. {error.replace(chr(10), chr(10) + '    ')}",
                file=output,
            )
        return 1

    print(
        "\nKOTONOHA SPRITE VALIDATION PASSED: 2 byte-exact original bases, "
        "42 outfit-conditioned RGBA face layers with blank neutrals and fixed "
        "registered masks, pairwise-distinct residue-free composites, 3 clean "
        "mid-thigh poses at the established head scale, exact Ren'Py wiring, "
        "and compatible story attributes."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
