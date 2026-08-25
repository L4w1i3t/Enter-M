"""Build Sam's layered-image face assets from generated full-sprite masters.

The image generator returns opaque RGB PNGs with a visible transparency
checker.  Those files are *donors*, never production sprites.  This tool:

* registers every donor independently to the casual and uniform head;
* uses ``featureless.png`` to erase only the canonical neutral features while
  preserving each outfit's native RGBA silhouette and surrounding texture;
* writes exact neutral repair layers and sparse, outfit-conditioned expression
  layers; and
* writes registration/alpha metrics plus contact sheets for visual review.

The default output is deliberately under ``tmp``.  Pass the production
``masayami`` directory explicitly after reviewing the contact sheets.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MASTER_DIR = PROJECT_ROOT / "tmp" / "sam_sprite_masters"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "tmp" / "sam_sprite_processed"
SAM_SPRITE_DIR = PROJECT_ROOT / "game" / "mod_assets" / "char_sprites" / "masayami"

CANVAS_WIDTH = 1023
CANVAS_HEIGHT = 1537
CANVAS_SIZE = (CANVAS_WIDTH, CANVAS_HEIGHT)

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

BLUSH_EXPRESSIONS = {
    "crying",
    "embarrassed",
    "nervous",
    "worried",
    "afraid",
    "panicked",
}

TEAR_OR_SWEAT_EXPRESSIONS = {"crying"}


@dataclass(frozen=True)
class EllipseSpec:
    center_x: float
    center_y: float
    radius_x: float
    radius_y: float


@dataclass(frozen=True)
class SamGeometry:
    """Conservative face geometry on Sam's canonical 1023x1537 canvas."""

    head: EllipseSpec = EllipseSpec(490, 267, 232, 248)
    face: EllipseSpec = EllipseSpec(493, 329, 123, 125)
    # These are deliberately feature-sized rather than face-patch-sized.  In
    # particular, their upper edges stop short of Sam's bangs.  A small
    # anti-aliasing fringe is added only after feature pixels have been found.
    left_brow: EllipseSpec = EllipseSpec(426, 269, 56, 15)
    right_brow: EllipseSpec = EllipseSpec(535, 250, 56, 15)
    left_eye: EllipseSpec = EllipseSpec(427, 305, 52, 27)
    right_eye: EllipseSpec = EllipseSpec(539, 285, 53, 27)
    mouth: EllipseSpec = EllipseSpec(498, 378, 62, 30)
    left_tear: EllipseSpec = EllipseSpec(427, 351, 31, 63)
    right_tear: EllipseSpec = EllipseSpec(548, 336, 31, 63)
    left_cheek: EllipseSpec = EllipseSpec(415, 354, 60, 39)
    right_cheek: EllipseSpec = EllipseSpec(565, 338, 60, 39)
    nose_keep: EllipseSpec = EllipseSpec(490, 343, 25, 37)


GEOMETRY = SamGeometry()

IRIS_CORE_SPECS = (
    EllipseSpec(429, 298, 34, 27),
    EllipseSpec(539, 281, 34, 27),
)
NEUTRAL_MOUTH_CORNER = EllipseSpec(543, 360, 18, 6)
NEUTRAL_MOUTH_CORNER_ANGLE = -55.0


@dataclass(frozen=True)
class RegistrationMetrics:
    method: str
    keypoint_matches: int
    inliers: int
    inlier_rms: float
    scale: float
    rotation_degrees: float
    translate_x: float
    translate_y: float


@dataclass(frozen=True)
class LayerMetrics:
    visible_pixels: int
    opaque_pixels: int
    partial_pixels: int
    hidden_rgb_pixels: int
    outside_allowed_pixels: int
    blush_pixels: int
    bounding_box: tuple[int, int, int, int] | None
    bounding_box_fill_ratio: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--master-dir",
        type=Path,
        default=DEFAULT_MASTER_DIR,
        help="Directory containing featureless.png and expression_<token>.png masters.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Destination for generated PNGs, metrics, and the _review directory.",
    )
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Process the expression masters that exist instead of requiring the full bank.",
    )
    return parser.parse_args()


def ellipse_mask(shape: tuple[int, int], spec: EllipseSpec) -> np.ndarray:
    height, width = shape
    y_grid, x_grid = np.ogrid[:height, :width]
    return (
        ((x_grid - spec.center_x) / spec.radius_x) ** 2
        + ((y_grid - spec.center_y) / spec.radius_y) ** 2
        <= 1.0
    )


def rotated_ellipse_mask(
    shape: tuple[int, int], spec: EllipseSpec, angle_degrees: float
) -> np.ndarray:
    y_grid, x_grid = np.ogrid[: shape[0], : shape[1]]
    x_delta = x_grid - spec.center_x
    y_delta = y_grid - spec.center_y
    angle = math.radians(angle_degrees)
    cosine = math.cos(angle)
    sine = math.sin(angle)
    rotated_x = cosine * x_delta + sine * y_delta
    rotated_y = -sine * x_delta + cosine * y_delta
    return (
        (rotated_x / spec.radius_x) ** 2
        + (rotated_y / spec.radius_y) ** 2
        <= 1.0
    )


def load_rgba(path: Path) -> np.ndarray:
    if not path.is_file():
        raise FileNotFoundError(path)
    with Image.open(path) as image:
        if image.size != CANVAS_SIZE:
            raise ValueError(f"{path}: got {image.size}, expected {CANVAS_SIZE}")
        return np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()


def load_master_rgb(path: Path) -> np.ndarray:
    if not path.is_file():
        raise FileNotFoundError(path)
    with Image.open(path) as image:
        if image.size != CANVAS_SIZE:
            raise ValueError(f"{path}: got {image.size}, expected {CANVAS_SIZE}")
        return np.asarray(image.convert("RGB"), dtype=np.uint8).copy()


def save_rgba(path: Path, rgba: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    clean = np.asarray(rgba, dtype=np.uint8).copy()
    clean[clean[:, :, 3] == 0, :3] = 0
    Image.fromarray(clean, "RGBA").save(path, optimize=True)


def compose_rgba(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    return np.asarray(
        Image.alpha_composite(
            Image.fromarray(base, "RGBA"), Image.fromarray(overlay, "RGBA")
        ),
        dtype=np.uint8,
    )


def checker_foreground(rgb: np.ndarray) -> np.ndarray:
    """Return a conservative subject mask for an opaque checker-backed master.

    The generator's checker is nearly achromatic and very light.  Only neutral
    components connected to the canvas count as background, so enclosed pale
    skin and clothing cannot turn into holes.
    """

    maximum = rgb.max(axis=2).astype(np.int16)
    minimum = rgb.min(axis=2).astype(np.int16)
    chroma = maximum - minimum
    background_candidate = (minimum >= 214) & (chroma <= 20)

    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        background_candidate.astype(np.uint8), connectivity=8
    )
    background = np.zeros(background_candidate.shape, dtype=bool)
    height, width = background_candidate.shape
    for label in range(1, count):
        x, y, component_width, component_height, area = stats[label]
        touches_canvas = (
            x == 0
            or y == 0
            or x + component_width == width
            or y + component_height == height
        )
        if touches_canvas and area >= 8:
            background[labels == label] = True

    foreground = ~background
    # Registration only needs the main figure.  Removing tiny islands also
    # drops checker compression specks without affecting face-interior pixels.
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        foreground.astype(np.uint8), connectivity=8
    )
    retained = np.zeros_like(foreground)
    for label in range(1, count):
        if stats[label, cv2.CC_STAT_AREA] >= 80:
            retained[labels == label] = True
    return retained


def grayscale_for_registration(rgb: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    gray = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)
    return gray


def registration_region(shape: tuple[int, int], foreground: np.ndarray) -> np.ndarray:
    head = ellipse_mask(shape, GEOMETRY.head)
    feature_exclusion = expression_feature_zone(shape)
    # Hair and the outer face/jaw carry stable landmarks.  Expression interiors
    # are explicitly excluded, including for the featureless donor.
    stable = head & foreground & ~feature_exclusion
    stable[:18, :] = False
    return stable


def expression_feature_zone(shape: tuple[int, int]) -> np.ndarray:
    """All coordinates where any face-layer pixel may ever be retained."""

    core = core_feature_zone(shape)
    tears = tear_feature_zone(shape)
    face = ellipse_mask(shape, GEOMETRY.face)
    nose = ellipse_mask(shape, GEOMETRY.nose_keep)
    return (core | tears) & face & ~nose


def core_feature_zone(shape: tuple[int, int]) -> np.ndarray:
    brows = rotated_ellipse_mask(shape, GEOMETRY.left_brow, -17.0) | (
        rotated_ellipse_mask(shape, GEOMETRY.right_brow, -17.0)
    )
    eyes = ellipse_mask(shape, GEOMETRY.left_eye) | ellipse_mask(
        shape, GEOMETRY.right_eye
    )
    mouth = ellipse_mask(shape, GEOMETRY.mouth)
    nose = ellipse_mask(shape, GEOMETRY.nose_keep)
    return (brows | eyes | mouth) & ~nose


def tear_feature_zone(shape: tuple[int, int]) -> np.ndarray:
    y_grid, _ = np.indices(shape)
    tears = ellipse_mask(shape, GEOMETRY.left_tear) | ellipse_mask(
        shape, GEOMETRY.right_tear
    )
    nose = ellipse_mask(shape, GEOMETRY.nose_keep)
    face = ellipse_mask(shape, GEOMETRY.face).astype(np.uint8)
    interior_face = cv2.distanceTransform(face, cv2.DIST_L2, 5) >= 9.0
    # Tear/sweat pixels begin below the upper eyelids; this prevents the tear
    # channel from becoming a second, overly broad eye/hair extractor.
    return tears & (y_grid >= 292) & interior_face & ~nose


def allowed_zone_for_expression(shape: tuple[int, int], expression: str) -> np.ndarray:
    allowed = core_feature_zone(shape)
    if expression == "neut":
        # The canonical smile has a detached viewer-right endpoint.  It belongs
        # only to neutral: erase it from the base and restore it exactly in the
        # neutral overlay so alternate expressions never inherit the slash.
        allowed |= rotated_ellipse_mask(
            shape, NEUTRAL_MOUTH_CORNER, NEUTRAL_MOUTH_CORNER_ANGLE
        )
    if expression in TEAR_OR_SWEAT_EXPRESSIONS:
        allowed |= tear_feature_zone(shape)
    return allowed & ellipse_mask(shape, GEOMETRY.face)


def protected_native_hair(neutral_rgba: np.ndarray) -> np.ndarray:
    """Mirror the validator's conservative canonical bang protection."""

    values = neutral_rgba[:, :, :3].astype(np.int16)
    red, green, blue = values[:, :, 0], values[:, :, 1], values[:, :, 2]
    iris_cores = ellipse_mask(values.shape[:2], IRIS_CORE_SPECS[0]) | ellipse_mask(
        values.shape[:2], IRIS_CORE_SPECS[1]
    )
    brow_cores = rotated_ellipse_mask(
        values.shape[:2], GEOMETRY.left_brow, -17.0
    ) | rotated_ellipse_mask(values.shape[:2], GEOMETRY.right_brow, -17.0)
    feature_exempt = iris_cores | brow_cores
    hair = (
        (neutral_rgba[:, :, 3] == 255)
        & (red >= 120)
        & ((red - blue) >= 100)
        & ((green - blue) >= 38)
        & ((red - green) >= 20)
        & ~feature_exempt
    )
    protected = cv2.dilate(
        hair.astype(np.uint8), np.ones((3, 3), dtype=np.uint8)
    ).astype(bool)
    return protected & ~feature_exempt


def enforce_native_feature_bounds(
    layer: np.ndarray,
    expression: str,
    neutral_rgba: np.ndarray,
) -> np.ndarray:
    """Hard-clip a sparse layer to semantic zones and native non-hair pixels."""

    result = layer.copy()
    allowed = spatial_allow_for_layer(result.shape[:2], expression)
    allowed &= neutral_rgba[:, :, 3] == 255
    allowed &= ~protected_native_hair(neutral_rgba)
    result[~allowed, 3] = 0
    result[result[:, :, 3] == 0, :3] = 0
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        (result[:, :, 3] > 0).astype(np.uint8), connectivity=8
    )
    for label in range(1, count):
        if stats[label, cv2.CC_STAT_AREA] < 10:
            result[labels == label] = 0
    return result


def _fallback_translation(
    source_gray: np.ndarray,
    target_gray: np.ndarray,
    source_mask: np.ndarray,
    target_mask: np.ndarray,
) -> tuple[np.ndarray, RegistrationMetrics]:
    """Find a safe translation if local feature matching is unavailable."""

    x0, y0, x1, y1 = 255, 15, 730, 525
    source_edges = cv2.Canny(source_gray, 55, 150)[y0:y1, x0:x1]
    target_edges = cv2.Canny(target_gray, 55, 150)[y0:y1, x0:x1]
    source_valid = source_mask[y0:y1, x0:x1]
    target_valid = target_mask[y0:y1, x0:x1]

    source_edges = cv2.resize(source_edges, None, fx=0.5, fy=0.5)
    target_edges = cv2.resize(target_edges, None, fx=0.5, fy=0.5)
    source_valid = cv2.resize(
        source_valid.astype(np.uint8), None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST
    ).astype(bool)
    target_valid = cv2.resize(
        target_valid.astype(np.uint8), None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST
    ).astype(bool)

    best_score = -math.inf
    best_shift = (0, 0)
    height, width = source_edges.shape
    for shift_y in range(-12, 13):
        for shift_x in range(-12, 13):
            source_x0 = max(0, -shift_x)
            source_x1 = min(width, width - shift_x)
            source_y0 = max(0, -shift_y)
            source_y1 = min(height, height - shift_y)
            target_x0 = source_x0 + shift_x
            target_x1 = source_x1 + shift_x
            target_y0 = source_y0 + shift_y
            target_y1 = source_y1 + shift_y
            valid = (
                source_valid[source_y0:source_y1, source_x0:source_x1]
                & target_valid[target_y0:target_y1, target_x0:target_x1]
            )
            if int(valid.sum()) < 500:
                continue
            source_values = source_edges[
                source_y0:source_y1, source_x0:source_x1
            ][valid].astype(np.float32)
            target_values = target_edges[
                target_y0:target_y1, target_x0:target_x1
            ][valid].astype(np.float32)
            score = float(
                np.mean(source_values * target_values)
                - 0.12 * np.mean(np.abs(source_values - target_values))
            )
            if score > best_score:
                best_score = score
                best_shift = (shift_x * 2, shift_y * 2)

    matrix = np.asarray(
        ((1.0, 0.0, best_shift[0]), (0.0, 1.0, best_shift[1])),
        dtype=np.float32,
    )
    metrics = RegistrationMetrics(
        method="edge_translation_fallback",
        keypoint_matches=0,
        inliers=0,
        inlier_rms=0.0,
        scale=1.0,
        rotation_degrees=0.0,
        translate_x=float(best_shift[0]),
        translate_y=float(best_shift[1]),
    )
    return matrix, metrics


def estimate_registration(
    source_rgb: np.ndarray,
    source_foreground: np.ndarray,
    target_rgba: np.ndarray,
) -> tuple[np.ndarray, RegistrationMetrics]:
    """Estimate a similarity transform from one master to one outfit head."""

    target_rgb = target_rgba[:, :, :3]
    target_foreground = target_rgba[:, :, 3] >= 240
    source_region = registration_region(source_foreground.shape, source_foreground)
    target_region = registration_region(target_foreground.shape, target_foreground)
    source_gray = grayscale_for_registration(source_rgb)
    target_gray = grayscale_for_registration(target_rgb)

    if not hasattr(cv2, "SIFT_create"):
        return _fallback_translation(
            source_gray, target_gray, source_region, target_region
        )

    sift = cv2.SIFT_create(nfeatures=1800, contrastThreshold=0.025, edgeThreshold=12)
    source_points, source_descriptors = sift.detectAndCompute(
        source_gray, source_region.astype(np.uint8) * 255
    )
    target_points, target_descriptors = sift.detectAndCompute(
        target_gray, target_region.astype(np.uint8) * 255
    )
    if source_descriptors is None or target_descriptors is None:
        return _fallback_translation(
            source_gray, target_gray, source_region, target_region
        )

    matcher = cv2.BFMatcher(cv2.NORM_L2)
    pairs = matcher.knnMatch(source_descriptors, target_descriptors, k=2)
    matches = []
    for pair in pairs:
        if len(pair) != 2:
            continue
        best, second = pair
        if best.distance >= 0.76 * second.distance:
            continue
        source_xy = np.asarray(source_points[best.queryIdx].pt)
        target_xy = np.asarray(target_points[best.trainIdx].pt)
        if float(np.linalg.norm(source_xy - target_xy)) <= 105.0:
            matches.append(best)

    if len(matches) < 6:
        return _fallback_translation(
            source_gray, target_gray, source_region, target_region
        )

    source_coordinates = np.float32(
        [source_points[match.queryIdx].pt for match in matches]
    )
    target_coordinates = np.float32(
        [target_points[match.trainIdx].pt for match in matches]
    )
    matrix, inlier_mask = cv2.estimateAffinePartial2D(
        source_coordinates,
        target_coordinates,
        method=cv2.RANSAC,
        ransacReprojThreshold=3.0,
        maxIters=5000,
        confidence=0.995,
        refineIters=20,
    )
    if matrix is None or inlier_mask is None:
        return _fallback_translation(
            source_gray, target_gray, source_region, target_region
        )

    inliers = inlier_mask.ravel().astype(bool)
    inlier_count = int(inliers.sum())
    scale = float(math.hypot(matrix[0, 0], matrix[0, 1]))
    rotation = float(math.degrees(math.atan2(matrix[1, 0], matrix[0, 0])))
    mapped = cv2.transform(source_coordinates[None, :, :], matrix)[0]
    residual = np.linalg.norm(mapped - target_coordinates, axis=1)
    rms = float(np.sqrt(np.mean(np.square(residual[inliers])))) if inlier_count else math.inf

    plausible = (
        inlier_count >= 5
        and 0.94 <= scale <= 1.06
        and abs(rotation) <= 4.0
        and abs(float(matrix[0, 2])) <= 65.0
        and abs(float(matrix[1, 2])) <= 65.0
        and rms <= 3.5
    )
    if not plausible:
        return _fallback_translation(
            source_gray, target_gray, source_region, target_region
        )

    matrix = matrix.astype(np.float32)
    metrics = RegistrationMetrics(
        method="sift_similarity",
        keypoint_matches=len(matches),
        inliers=inlier_count,
        inlier_rms=rms,
        scale=scale,
        rotation_degrees=rotation,
        translate_x=float(matrix[0, 2]),
        translate_y=float(matrix[1, 2]),
    )
    return matrix, metrics


def warp_rgb(rgb: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    return cv2.warpAffine(
        rgb,
        matrix,
        CANVAS_SIZE,
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0),
    )


def warp_mask(mask: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    return cv2.warpAffine(
        mask.astype(np.uint8),
        matrix,
        CANVAS_SIZE,
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    ).astype(bool)


def premultiplied_warp_rgba(rgba: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    """Warp RGBA without introducing colored fringes into transparent pixels."""

    alpha = rgba[:, :, 3].astype(np.float32) / 255.0
    premultiplied = rgba[:, :, :3].astype(np.float32) * alpha[:, :, None]
    warped_alpha = cv2.warpAffine(
        alpha,
        matrix,
        CANVAS_SIZE,
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )
    warped_premultiplied = cv2.warpAffine(
        premultiplied,
        matrix,
        CANVAS_SIZE,
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0),
    )
    warped_alpha = np.clip(warped_alpha, 0.0, 1.0)
    warped_rgb = np.zeros_like(warped_premultiplied)
    visible = warped_alpha > (1.0 / 255.0)
    warped_rgb[visible] = (
        warped_premultiplied[visible] / warped_alpha[visible, None]
    )
    result = np.dstack(
        (
            np.clip(np.rint(warped_rgb), 0, 255).astype(np.uint8),
            np.clip(np.rint(warped_alpha * 255.0), 0, 255).astype(np.uint8),
        )
    )
    result[result[:, :, 3] == 0, :3] = 0
    return result


def skin_mask(rgb: np.ndarray, valid: np.ndarray) -> np.ndarray:
    values = rgb.astype(np.int16)
    red, green, blue = values[:, :, 0], values[:, :, 1], values[:, :, 2]
    luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
    return (
        valid
        & (red >= 145)
        & (green >= 118)
        & (blue >= 103)
        & (luminance >= 166)
        & (red >= green - 4)
        & (green >= blue - 14)
        & ((red - blue) >= 13)
        # Golden hair can otherwise pass a generic warm-skin threshold.  These
        # two bounds retain Sam's peach face while excluding even pale bangs.
        & ((red - green) <= 63)
        & ((green - blue) <= 44)
        & ellipse_mask(valid.shape, GEOMETRY.face)
    )


def featureless_face_interior(rgb: np.ndarray, valid: np.ndarray) -> np.ndarray:
    """Return the connected skin field exposed by the featureless donor.

    A raw warm-color threshold occasionally admits an isolated blond highlight.
    Keeping only skin components connected to the lower central face turns the
    featureless master into a hard bangs/ears/jaw exclusion mask.  The two-pixel
    expansion is only enough to accommodate registered line-art anti-aliasing;
    it is not large enough to cross a hair boundary.
    """

    shape = valid.shape
    raw = skin_mask(rgb, valid)
    raw = cv2.morphologyEx(
        raw.astype(np.uint8),
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)),
    ).astype(bool)
    seed = ellipse_mask(shape, EllipseSpec(500, 373, 52, 46))
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        raw.astype(np.uint8), connectivity=8
    )
    retained = np.zeros(shape, dtype=bool)
    for label in range(1, count):
        component = labels == label
        if stats[label, cv2.CC_STAT_AREA] >= 100 and np.any(component & seed):
            retained |= component

    retained = cv2.dilate(
        retained.astype(np.uint8),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
    ).astype(bool)
    face = ellipse_mask(shape, GEOMETRY.face).astype(np.uint8)
    interior_face = cv2.distanceTransform(face, cv2.DIST_L2, 5) >= 5.0
    return retained & interior_face & valid


def fit_native_color_map(
    source_rgb: np.ndarray,
    source_valid: np.ndarray,
    target_rgba: np.ndarray,
) -> tuple[np.ndarray, dict[str, float | int]]:
    """Map donor face lighting into an outfit's native face color space."""

    shape = source_valid.shape
    target_rgb = target_rgba[:, :, :3]
    target_valid = target_rgba[:, :, 3] == 255
    face = ellipse_mask(shape, GEOMETRY.face)
    feature_margin = cv2.dilate(
        expression_feature_zone(shape).astype(np.uint8),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)),
    ).astype(bool)
    y_grid, _ = np.indices(shape)
    stable = (
        face
        & (y_grid >= 238)
        & ~feature_margin
        & skin_mask(source_rgb, source_valid)
        & skin_mask(target_rgb, target_valid)
    )

    y_coordinates, x_coordinates = np.nonzero(stable)
    if len(x_coordinates) < 300:
        raise RuntimeError(
            f"Only {len(x_coordinates)} stable skin pixels available for color fitting"
        )
    # A deterministic stride bounds the least-squares cost without changing
    # the spatial distribution of samples.
    stride = max(1, len(x_coordinates) // 24000)
    y_coordinates = y_coordinates[::stride]
    x_coordinates = x_coordinates[::stride]
    source_values = source_rgb[y_coordinates, x_coordinates].astype(np.float64)
    target_values = target_rgb[y_coordinates, x_coordinates].astype(np.float64)
    features = np.column_stack(
        (
            source_values,
            np.ones(len(source_values)),
            (x_coordinates - GEOMETRY.face.center_x) / 150.0,
            (y_coordinates - GEOMETRY.face.center_y) / 150.0,
        )
    )

    inliers = np.ones(len(features), dtype=bool)
    coefficients = np.zeros((features.shape[1], 3), dtype=np.float64)
    for percentile in (86, 78):
        coefficients, *_ = np.linalg.lstsq(
            features[inliers], target_values[inliers], rcond=None
        )
        residual = np.linalg.norm(features @ coefficients - target_values, axis=1)
        cutoff = float(np.percentile(residual[inliers], percentile))
        inliers = residual <= cutoff
    coefficients, *_ = np.linalg.lstsq(
        features[inliers], target_values[inliers], rcond=None
    )

    all_y, all_x = np.indices(shape)
    source_float = source_rgb.astype(np.float64)
    all_features = np.dstack(
        (
            source_float,
            np.ones(shape + (1,), dtype=np.float64),
            ((all_x - GEOMETRY.face.center_x) / 150.0)[..., None],
            ((all_y - GEOMETRY.face.center_y) / 150.0)[..., None],
        )
    )
    mapped = np.clip(np.rint(all_features @ coefficients), 0, 255).astype(np.uint8)
    fit_residual = np.linalg.norm(
        features[inliers] @ coefficients - target_values[inliers], axis=1
    )
    return mapped, {
        "samples": int(len(features)),
        "inliers": int(inliers.sum()),
        "mean_residual": float(fit_residual.mean()),
        "p95_residual": float(np.percentile(fit_residual, 95)),
    }


def maximum_color_delta(first_rgb: np.ndarray, second_rgb: np.ndarray) -> np.ndarray:
    return np.max(
        np.abs(first_rgb.astype(np.int16) - second_rgb.astype(np.int16)), axis=2
    ).astype(np.uint8)


def feature_palette(
    rgb: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    values = rgb.astype(np.int16)
    red, green, blue = values[:, :, 0], values[:, :, 1], values[:, :, 2]
    maximum = values.max(axis=2)
    minimum = values.min(axis=2)
    spread = maximum - minimum
    luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
    # Warm midtones are intentionally absent.  They describe both skin and
    # blond hair in the generated masters and caused the rejected wedges.  The
    # few authored warm colors we need are admitted later only inside an iris
    # core or the mouth zone.
    dark_ink = (luminance <= 132) & (minimum <= 108)
    amber = (
        (luminance <= 180)
        & (minimum <= 132)
        & (spread >= 44)
        & (red >= green + 8)
        & (green >= blue + 4)
    )
    pale_feature = (minimum >= 188) & (spread <= 29)
    red_mouth = (
        (luminance <= 188)
        & (green <= 165)
        & ((red - green) >= 24)
        & ((red - blue) >= 18)
    )
    return dark_ink, amber, pale_feature, red_mouth


def geodesic_grow(seed: np.ndarray, candidate: np.ndarray, steps: int) -> np.ndarray:
    result = seed.copy()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    for _ in range(steps):
        grown = cv2.dilate(result.astype(np.uint8), kernel).astype(bool) & candidate
        if np.array_equal(grown, result):
            break
        result = grown
    return result


def retain_seeded_components(
    candidate: np.ndarray,
    seed: np.ndarray,
    minimum_area: int = 2,
) -> np.ndarray:
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        candidate.astype(np.uint8), connectivity=8
    )
    retained = np.zeros(candidate.shape, dtype=bool)
    for label in range(1, count):
        component = labels == label
        if stats[label, cv2.CC_STAT_AREA] >= minimum_area and np.any(component & seed):
            retained[component] = True
    return retained


def seeded_feature_components(
    rgb: np.ndarray,
    delta: np.ndarray,
    allowed: np.ndarray,
    zones: Sequence[np.ndarray],
) -> np.ndarray:
    """Keep only authored feature components anchored by dark/colored ink.

    Independent generations have low-frequency skin differences even after
    color normalization.  Connected-component seeding lets pale sclera and
    teeth survive while rejecting those unanchored skin fields outright.
    """

    retained = np.zeros(allowed.shape, dtype=bool)
    dark_ink, amber, pale, red_mouth = feature_palette(rgb)
    iris_zones = (
        ellipse_mask(allowed.shape, EllipseSpec(427, 307, 31, 22)),
        ellipse_mask(allowed.shape, EllipseSpec(539, 287, 31, 22)),
    )
    for index, zone in enumerate(zones):
        if index < 2:
            authored = dark_ink
            anchors = dark_ink
        elif index < 4:
            iris = amber & iris_zones[index - 2]
            authored = dark_ink | pale | iris
            anchors = dark_ink | iris
        else:
            authored = dark_ink | pale | red_mouth
            anchors = dark_ink | red_mouth

        zone_allowed = allowed & zone
        zone_seed = zone_allowed & anchors & (delta >= 14)
        candidate = zone_allowed & authored & (delta >= 9)
        bridge = cv2.dilate(
            zone_seed.astype(np.uint8),
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
        ).astype(bool)
        candidate |= bridge & zone_allowed & authored & (delta >= 6)
        candidate |= zone_seed
        if not np.any(zone_seed):
            continue
        retained |= retain_seeded_components(
            candidate, zone_seed, minimum_area=2
        )
    return cv2.morphologyEx(
        retained.astype(np.uint8),
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
    ).astype(bool)


def normalize_rgb_diagonal(
    source_rgb: np.ndarray,
    source_valid: np.ndarray,
    reference_rgb: np.ndarray,
    reference_valid: np.ndarray,
) -> tuple[np.ndarray, dict[str, object]]:
    """Normalize skin for difference detection without recoloring features.

    A full cross-channel regression fits skin well but extrapolates wildly on
    dark eyes and pale sclera (the earlier cyan-outline failure).  Independent
    clipped channel fits are intentionally less expressive and are used only
    to compute a difference mask.  Exported feature RGB always comes from the
    unmodified casual master.
    """

    shape = source_valid.shape
    feature_margin = cv2.dilate(
        expression_feature_zone(shape).astype(np.uint8),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)),
    ).astype(bool)
    y_grid, _ = np.indices(shape)
    stable = (
        ellipse_mask(shape, GEOMETRY.face)
        & (y_grid >= 238)
        & ~feature_margin
        & skin_mask(source_rgb, source_valid)
        & skin_mask(reference_rgb, reference_valid)
    )
    y_coordinates, x_coordinates = np.nonzero(stable)
    if len(x_coordinates) < 250:
        raise RuntimeError(
            f"Only {len(x_coordinates)} stable skin pixels available for normalization"
        )
    stride = max(1, len(x_coordinates) // 20000)
    y_coordinates = y_coordinates[::stride]
    x_coordinates = x_coordinates[::stride]
    source_values = source_rgb[y_coordinates, x_coordinates].astype(np.float64)
    reference_values = reference_rgb[y_coordinates, x_coordinates].astype(np.float64)

    gains: list[float] = []
    offsets: list[float] = []
    residuals: list[np.ndarray] = []
    for channel in range(3):
        source_channel = source_values[:, channel]
        reference_channel = reference_values[:, channel]
        inliers = np.ones(len(source_channel), dtype=bool)
        gain = 1.0
        offset = 0.0
        for percentile in (88, 80):
            design = np.column_stack(
                (source_channel[inliers], np.ones(int(inliers.sum())))
            )
            fit, *_ = np.linalg.lstsq(
                design, reference_channel[inliers], rcond=None
            )
            gain = float(np.clip(fit[0], 0.88, 1.12))
            offset = float(
                np.clip(
                    np.median(reference_channel - gain * source_channel),
                    -24.0,
                    24.0,
                )
            )
            residual = np.abs(gain * source_channel + offset - reference_channel)
            cutoff = float(np.percentile(residual[inliers], percentile))
            inliers = residual <= cutoff
        gains.append(gain)
        offsets.append(offset)
        residuals.append(np.abs(gain * source_channel + offset - reference_channel))

    source_float = source_rgb.astype(np.float32)
    normalized = np.empty_like(source_rgb)
    for channel, (gain, offset) in enumerate(zip(gains, offsets)):
        normalized[:, :, channel] = np.clip(
            np.rint(source_float[:, :, channel] * gain + offset), 0, 255
        ).astype(np.uint8)
    combined_residual = np.column_stack(residuals)
    return normalized, {
        "samples": int(len(source_values)),
        "gains": gains,
        "offsets": offsets,
        "mean_absolute_residual": float(combined_residual.mean()),
        "p95_absolute_residual": float(np.percentile(combined_residual, 95)),
    }


def neutral_feature_mask(
    neutral_rgba: np.ndarray,
    mapped_featureless_rgb: np.ndarray,
    aligned_featureless_rgb: np.ndarray,
    featureless_valid: np.ndarray,
) -> np.ndarray:
    """Locate the authored neutral eyes/brows/mouth without taking a face patch."""

    shape = neutral_rgba.shape[:2]
    neutral_rgb = neutral_rgba[:, :, :3]
    delta = maximum_color_delta(neutral_rgb, mapped_featureless_rgb)
    target_valid = neutral_rgba[:, :, 3] == 255
    # Classify the raw donor, not the skin-fitted donor.  A skin-only regression
    # is undefined on hair and can otherwise make a golden bang look peach.
    donor_skin = featureless_face_interior(
        aligned_featureless_rgb, featureless_valid
    )
    allowed = (
        allowed_zone_for_expression(shape, "neut")
        & target_valid
        & featureless_valid
        & donor_skin
    )

    zones = (
        rotated_ellipse_mask(shape, GEOMETRY.left_brow, -17.0),
        rotated_ellipse_mask(shape, GEOMETRY.right_brow, -17.0),
        ellipse_mask(shape, GEOMETRY.left_eye),
        ellipse_mask(shape, GEOMETRY.right_eye),
        ellipse_mask(shape, GEOMETRY.mouth),
        rotated_ellipse_mask(
            shape, NEUTRAL_MOUTH_CORNER, NEUTRAL_MOUTH_CORNER_ANGLE
        ),
    )
    retained = seeded_feature_components(neutral_rgb, delta, allowed, zones)
    neutral_luminance = cv2.cvtColor(neutral_rgb, cv2.COLOR_RGB2GRAY).astype(
        np.int16
    )
    donor_luminance = cv2.cvtColor(
        mapped_featureless_rgb, cv2.COLOR_RGB2GRAY
    ).astype(np.int16)
    # Canonical brows and the detached smile endpoint contain warm brown
    # anti-aliasing that is neither dark enough to be line-art seed nor pale
    # enough to be sclera.  It is, however, consistently darker than the blank
    # skin donor.  Include that contrast only inside the strict feature zones.
    darker_feature = (
        allowed
        & ((donor_luminance - neutral_luminance) >= 8)
        & (delta >= 8)
        & (neutral_luminance <= 205)
    )
    retained |= darker_feature
    return cv2.morphologyEx(
        retained.astype(np.uint8),
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
    ).astype(bool)


def build_featureless_base(
    neutral_rgba: np.ndarray,
    aligned_featureless_rgb: np.ndarray,
    featureless_valid: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, dict[str, float | int]]:
    mapped_featureless, color_metrics = fit_native_color_map(
        aligned_featureless_rgb, featureless_valid, neutral_rgba
    )
    neutral_features = neutral_feature_mask(
        neutral_rgba,
        mapped_featureless,
        aligned_featureless_rgb,
        featureless_valid,
    )
    fillable_skin = featureless_face_interior(
        aligned_featureless_rgb, featureless_valid
    )
    core = cv2.dilate(
        neutral_features.astype(np.uint8),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)),
    ).astype(bool)
    core &= fillable_skin
    strict_allowed = allowed_zone_for_expression(core.shape, "neut")
    strict_allowed &= neutral_rgba[:, :, 3] == 255
    strict_allowed &= ~protected_native_hair(neutral_rgba)
    core &= cv2.dilate(
        allowed_zone_for_expression(core.shape, "neut").astype(np.uint8),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)),
    ).astype(bool)
    core &= strict_allowed
    core &= featureless_valid
    core &= neutral_rgba[:, :, 3] == 255

    expanded = cv2.dilate(
        core.astype(np.uint8),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
    )
    blend_alpha = cv2.GaussianBlur(expanded.astype(np.float32), (0, 0), 0.7)
    blend_alpha = np.clip(blend_alpha, 0.0, 1.0)
    blend_alpha[core] = 1.0
    blend_alpha[~fillable_skin] = 0.0
    blend_alpha[~featureless_valid] = 0.0
    blend_alpha[neutral_rgba[:, :, 3] != 255] = 0.0
    blend_alpha[~strict_allowed] = 0.0

    target_rgb = neutral_rgba[:, :, :3].astype(np.float32)
    donor_rgb = mapped_featureless.astype(np.float32)
    mixed_rgb = np.rint(
        target_rgb * (1.0 - blend_alpha[:, :, None])
        + donor_rgb * blend_alpha[:, :, None]
    ).astype(np.uint8)
    blank = neutral_rgba.copy()
    changed = blend_alpha > 0.0
    blank[changed, :3] = mixed_rgb[changed]
    # The canonical silhouette is authoritative; donor alpha is never copied.
    blank[:, :, 3] = neutral_rgba[:, :, 3]
    blank[blank[:, :, 3] == 0, :3] = 0

    metrics: dict[str, float | int] = dict(color_metrics)
    metrics.update(
        {
            "neutral_feature_pixels": int(neutral_features.sum()),
            "erasure_core_pixels": int(core.sum()),
            "erasure_feather_pixels": int(((blend_alpha > 0) & ~core).sum()),
        }
    )
    return blank, blend_alpha, metrics


def exact_neutral_overlay(neutral_rgba: np.ndarray, blank_rgba: np.ndarray) -> np.ndarray:
    if not np.array_equal(neutral_rgba[:, :, 3], blank_rgba[:, :, 3]):
        raise ValueError("A featureless base changed the canonical silhouette")
    changed = np.any(neutral_rgba[:, :, :3] != blank_rgba[:, :, :3], axis=2)
    if np.any(changed & (neutral_rgba[:, :, 3] != 255)):
        raise ValueError("Neutral repair would need to alter a translucent edge pixel")
    overlay = np.zeros_like(neutral_rgba)
    overlay[changed, :3] = neutral_rgba[changed, :3]
    overlay[changed, 3] = 255
    return overlay


def normalize_sam_iris_palette(
    layer: np.ndarray, canonical_neutral: np.ndarray
) -> tuple[np.ndarray, dict[str, float | int]]:
    """Normalize generated iris colors to Sam's canonical amber palette.

    Value is left untouched, near-black line art and pale highlights are left
    untouched, and only visible pixels inside the two eye cores are eligible.
    This corrects gray/blue/purple generator drift without tinting sclera or
    tears.
    """

    shape = layer.shape[:2]
    eye_zone = ellipse_mask(shape, GEOMETRY.left_eye) | ellipse_mask(
        shape, GEOMETRY.right_eye
    )
    reference_rgb = canonical_neutral[:, :, :3]
    reference_values = reference_rgb.astype(np.int16)
    reference_hsv = cv2.cvtColor(reference_rgb, cv2.COLOR_RGB2HSV)
    reference_amber = (
        eye_zone
        & (reference_values[:, :, 0] >= reference_values[:, :, 1] + 8)
        & (reference_values[:, :, 1] >= reference_values[:, :, 2] + 5)
        & (reference_hsv[:, :, 1] >= 42)
        & (reference_hsv[:, :, 2] >= 55)
        & (reference_hsv[:, :, 2] <= 205)
    )
    if int(reference_amber.sum()) < 20:
        amber_hue = 14
        amber_saturation = 150
    else:
        amber_hue = int(np.median(reference_hsv[:, :, 0][reference_amber]))
        amber_saturation = int(
            np.median(reference_hsv[:, :, 1][reference_amber])
        )

    result = layer.copy()
    rgb = result[:, :, :3]
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]
    candidate = (
        eye_zone
        & (result[:, :, 3] >= 96)
        & (value >= 66)
        & (value <= 195)
        & ((saturation >= 18) | (value <= 165))
    )
    if np.any(candidate):
        value_float = value[candidate].astype(np.float32)
        saturation_floor = amber_saturation * np.clip(
            0.90 - (value_float - 66.0) / 230.0, 0.35, 0.90
        )
        hsv[:, :, 0][candidate] = amber_hue
        hsv[:, :, 1][candidate] = np.clip(
            np.maximum(saturation[candidate], np.rint(saturation_floor)), 0, 255
        ).astype(np.uint8)
        result[:, :, :3] = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    result[result[:, :, 3] == 0, :3] = 0
    return result, {
        "recolored_pixels": int(candidate.sum()),
        "canonical_hue": amber_hue,
        "canonical_saturation": amber_saturation,
    }


def spatial_allow_for_layer(shape: tuple[int, int], expression: str) -> np.ndarray:
    allowed = allowed_zone_for_expression(shape, expression)
    if expression in BLUSH_EXPRESSIONS:
        allowed |= ellipse_mask(shape, GEOMETRY.left_cheek) | ellipse_mask(
            shape, GEOMETRY.right_cheek
        )
    allowed &= ellipse_mask(shape, GEOMETRY.face)
    return allowed


def measure_layer(
    layer: np.ndarray,
    allowed: np.ndarray,
    *,
    blush_pixels: int = 0,
) -> LayerMetrics:
    alpha = layer[:, :, 3]
    visible = alpha > 0
    y_coordinates, x_coordinates = np.nonzero(visible)
    if len(x_coordinates):
        bounding_box = (
            int(x_coordinates.min()),
            int(y_coordinates.min()),
            int(x_coordinates.max()) + 1,
            int(y_coordinates.max()) + 1,
        )
        box_area = (bounding_box[2] - bounding_box[0]) * (
            bounding_box[3] - bounding_box[1]
        )
        fill_ratio = float(visible.sum() / box_area)
    else:
        bounding_box = None
        fill_ratio = 0.0
    return LayerMetrics(
        visible_pixels=int(visible.sum()),
        opaque_pixels=int((alpha == 255).sum()),
        partial_pixels=int(((alpha > 0) & (alpha < 255)).sum()),
        hidden_rgb_pixels=int(
            np.any(layer[:, :, :3] != 0, axis=2)[alpha == 0].sum()
        ),
        outside_allowed_pixels=int((visible & ~allowed).sum()),
        blush_pixels=int(blush_pixels),
        bounding_box=bounding_box,
        bounding_box_fill_ratio=fill_ratio,
    )


def build_expression_layer(
    expression: str,
    blank_rgba: np.ndarray,
    aligned_expression_rgb: np.ndarray,
    expression_valid: np.ndarray,
    aligned_featureless_rgb: np.ndarray,
    featureless_valid: np.ndarray,
) -> tuple[np.ndarray, LayerMetrics, dict[str, object]]:
    normalized_expression, normalization_metrics = normalize_rgb_diagonal(
        aligned_expression_rgb,
        expression_valid,
        aligned_featureless_rgb,
        featureless_valid,
    )
    shape = blank_rgba.shape[:2]
    donor_skin = featureless_face_interior(
        aligned_featureless_rgb, featureless_valid
    )
    allowed_core = (
        core_feature_zone(shape)
        & donor_skin
        & expression_valid
        & featureless_valid
    )

    delta = maximum_color_delta(normalized_expression, aligned_featureless_rgb)
    zones = (
        rotated_ellipse_mask(shape, GEOMETRY.left_brow, -17.0),
        rotated_ellipse_mask(shape, GEOMETRY.right_brow, -17.0),
        ellipse_mask(shape, GEOMETRY.left_eye),
        ellipse_mask(shape, GEOMETRY.right_eye),
        ellipse_mask(shape, GEOMETRY.mouth),
    )
    retained = seeded_feature_components(
        aligned_expression_rgb, delta, allowed_core, zones
    )
    normalized_luminance = cv2.cvtColor(
        normalized_expression, cv2.COLOR_RGB2GRAY
    ).astype(np.int16)
    blank_luminance = cv2.cvtColor(
        aligned_featureless_rgb, cv2.COLOR_RGB2GRAY
    ).astype(np.int16)
    brow_line_zone = rotated_ellipse_mask(
        shape, EllipseSpec(426, 269, 52, 8), -17.0
    ) | rotated_ellipse_mask(shape, EllipseSpec(535, 250, 52, 8), -17.0)
    brow_contrast = (
        allowed_core
        & brow_line_zone
        & ((blank_luminance - normalized_luminance) >= 9)
        & (delta >= 8)
        & (normalized_luminance <= 205)
    )
    retained |= brow_contrast

    allowed = allowed_core.copy()
    if expression in TEAR_OR_SWEAT_EXPRESSIONS:
        tear_zone = tear_feature_zone(shape) & donor_skin
        values = aligned_expression_rgb.astype(np.int16)
        red, green, blue = values[:, :, 0], values[:, :, 1], values[:, :, 2]
        maximum = values.max(axis=2)
        minimum = values.min(axis=2)
        spread = maximum - minimum
        luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
        pale_tear = (minimum >= 198) & (spread <= 52) & (luminance >= 202)
        cool_tear = (
            (luminance >= 184)
            & (blue >= red - 8)
            & (blue >= green - 12)
            & (spread <= 62)
        )
        tear_seed = tear_zone & (pale_tear | cool_tear) & (delta >= 15)
        tear_candidate = (
            tear_zone
            & (luminance >= 176)
            & (spread <= 72)
            & (delta >= 10)
        )
        grown_tears = geodesic_grow(
            tear_seed, tear_candidate | tear_seed, steps=5
        )
        retained |= retain_seeded_components(
            grown_tears, tear_seed, minimum_area=3
        )
        allowed |= tear_zone

    retained &= allowed
    fringe_support = cv2.dilate(
        retained.astype(np.uint8),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
    ).astype(bool)
    fringe_support &= allowed
    fringe_support &= (delta >= 5) | retained
    feature_alpha = cv2.GaussianBlur(
        retained.astype(np.float32) * 255.0, (0, 0), 0.52
    )
    feature_alpha = np.clip(np.rint(feature_alpha), 0, 255).astype(np.uint8)
    feature_alpha[retained] = 255
    feature_alpha[~fringe_support] = 0

    blush_alpha = np.zeros(shape, dtype=np.uint8)
    if expression in BLUSH_EXPRESSIONS:
        expression_values = normalized_expression.astype(np.int16)
        blank_values = aligned_featureless_rgb.astype(np.int16)
        expression_redness = expression_values[:, :, 0] - (
            expression_values[:, :, 1] + expression_values[:, :, 2]
        ) / 2.0
        blank_redness = blank_values[:, :, 0] - (
            blank_values[:, :, 1] + blank_values[:, :, 2]
        ) / 2.0
        cheeks = ellipse_mask(shape, GEOMETRY.left_cheek) | ellipse_mask(
            shape, GEOMETRY.right_cheek
        )
        blush_seed = (
            cheeks
            & donor_skin
            & expression_valid
            & featureless_valid
            & ((expression_redness - blank_redness) >= 10.0)
            & (delta >= 10)
        )
        blush_strength = np.clip(
            (expression_redness - blank_redness - 10.0) * 0.70, 0.0, 22.0
        )
        blush_alpha[blush_seed] = np.rint(blush_strength[blush_seed]).astype(
            np.uint8
        )
        blush_alpha = cv2.GaussianBlur(blush_alpha, (0, 0), 4.5)
        cheek_feather = cv2.GaussianBlur(
            (cheeks & donor_skin).astype(np.uint8) * 255, (0, 0), 3.5
        )
        blush_alpha = np.rint(
            blush_alpha.astype(np.float32) * cheek_feather.astype(np.float32) / 255.0
        ).astype(np.uint8)
        blush_alpha = np.minimum(blush_alpha, 22).astype(np.uint8)
        blush_alpha[blush_alpha < 3] = 0

    final_alpha = np.maximum(feature_alpha, blush_alpha)
    final_alpha[~allowed & (blush_alpha == 0)] = 0
    layer = np.zeros_like(blank_rgba)
    # Do not export the skin-normalized RGB: even a safe skin fit is not a
    # valid color transform for irises, sclera, tears, or mouth ink.
    layer[:, :, :3] = aligned_expression_rgb
    tint_only = (blush_alpha > feature_alpha) & (blush_alpha > 0)
    layer[tint_only, :3] = np.asarray((236, 105, 112), dtype=np.uint8)
    layer[:, :, 3] = final_alpha
    layer[final_alpha == 0, :3] = 0

    spatial_allow = spatial_allow_for_layer(shape, expression)
    layer[~spatial_allow, 3] = 0
    layer[layer[:, :, 3] == 0, :3] = 0

    metrics = measure_layer(
        layer,
        spatial_allow,
        blush_pixels=int((blush_alpha > 0).sum()),
    )
    return layer, metrics, normalization_metrics


def checker_background(size: tuple[int, int], tile: int = 16) -> Image.Image:
    width, height = size
    y_grid, x_grid = np.ogrid[:height, :width]
    cells = ((x_grid // tile) + (y_grid // tile)) % 2
    rgb = np.empty((height, width, 3), dtype=np.uint8)
    rgb[cells == 0] = (72, 72, 78)
    rgb[cells == 1] = (106, 106, 113)
    return Image.fromarray(rgb, "RGB")


def rgba_on_background(rgba: np.ndarray, background: Image.Image) -> Image.Image:
    return Image.alpha_composite(
        background.convert("RGBA"), Image.fromarray(rgba, "RGBA")
    ).convert("RGB")


def contact_sheet(
    path: Path,
    title: str,
    items: Sequence[tuple[str, np.ndarray]],
    *,
    layer_only: bool = False,
    columns: int = 5,
) -> None:
    if not items:
        return
    crop_box = (275, 75, 705, 520)
    crop_width = crop_box[2] - crop_box[0]
    crop_height = crop_box[3] - crop_box[1]
    render_width = 300
    render_height = round(render_width * crop_height / crop_width)
    margin = 10
    label_height = 38
    title_height = 42
    cell_width = render_width + margin * 2
    cell_height = render_height + label_height + margin
    rows = (len(items) + columns - 1) // columns
    sheet = Image.new(
        "RGB",
        (columns * cell_width, title_height + rows * cell_height),
        (22, 22, 26),
    )
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.load_default(size=15)
    except TypeError:
        font = ImageFont.load_default()
    draw.text((12, 12), title, fill=(245, 245, 248), font=font)

    for index, (label, rgba) in enumerate(items):
        column = index % columns
        row = index // columns
        x = column * cell_width + margin
        y = title_height + row * cell_height + margin
        crop = rgba[crop_box[1] : crop_box[3], crop_box[0] : crop_box[2]]
        if layer_only:
            rendered = rgba_on_background(crop, checker_background((crop_width, crop_height)))
        else:
            rendered = rgba_on_background(
                crop, Image.new("RGB", (crop_width, crop_height), (35, 35, 40))
            )
        rendered = rendered.resize(
            (render_width, render_height), Image.Resampling.LANCZOS
        )
        sheet.paste(rendered, (x, y))
        draw.text(
            (x + render_width // 2, y + render_height + 9),
            label,
            fill=(238, 238, 242),
            font=font,
            anchor="ma",
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, optimize=True)


def aligned_master_preview(
    aligned_rgb: np.ndarray, aligned_foreground: np.ndarray
) -> np.ndarray:
    preview = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH, 4), dtype=np.uint8)
    preview[:, :, :3] = aligned_rgb
    preview[:, :, 3] = aligned_foreground.astype(np.uint8) * 255
    preview[~aligned_foreground, :3] = 0
    return preview


def validate_inputs(master_dir: Path, allow_partial: bool) -> list[str]:
    available = [
        expression
        for expression in EXPRESSIONS
        if (master_dir / f"expression_{expression}.png").is_file()
    ]
    missing = [expression for expression in EXPRESSIONS if expression not in available]
    if missing and not allow_partial:
        missing_text = ", ".join(missing)
        raise FileNotFoundError(
            f"Missing expression masters: {missing_text}. Re-run with --allow-partial "
            "for a pilot build."
        )
    if not available:
        raise FileNotFoundError(f"No expression_<token>.png masters found in {master_dir}")
    return available


def write_metrics_tsv(path: Path, report: dict[str, object]) -> None:
    lines = [
        "kind\toutfit\texpression\tmethod\tmatches\tinliers\trms\tscale\trotation\ttx\tty\tvisible\topaque\tpartial\tblush\thidden_rgb\toutside_allowed\tbbox_fill"
    ]
    registrations = report["registrations"]
    assert isinstance(registrations, dict)
    for outfit, by_master in registrations.items():
        assert isinstance(by_master, dict)
        for master, metrics in by_master.items():
            assert isinstance(metrics, dict)
            lines.append(
                "\t".join(
                    (
                        "registration",
                        outfit,
                        master,
                        str(metrics["method"]),
                        str(metrics["keypoint_matches"]),
                        str(metrics["inliers"]),
                        f"{float(metrics['inlier_rms']):.4f}",
                        f"{float(metrics['scale']):.7f}",
                        f"{float(metrics['rotation_degrees']):.5f}",
                        f"{float(metrics['translate_x']):.4f}",
                        f"{float(metrics['translate_y']):.4f}",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                    )
                )
            )
    layers = report.get("layers", {})
    assert isinstance(layers, dict)
    for outfit, by_expression in layers.items():
        assert isinstance(by_expression, dict)
        for expression, metrics in by_expression.items():
            assert isinstance(metrics, dict)
            lines.append(
                "\t".join(
                    (
                        "layer",
                        outfit,
                        expression,
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        str(metrics["visible_pixels"]),
                        str(metrics["opaque_pixels"]),
                        str(metrics["partial_pixels"]),
                        str(metrics["blush_pixels"]),
                        str(metrics["hidden_rgb_pixels"]),
                        str(metrics["outside_allowed_pixels"]),
                        f"{float(metrics['bounding_box_fill_ratio']):.5f}",
                    )
                )
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    master_dir = args.master_dir.resolve()
    output_dir = args.output_dir.resolve()
    expressions = validate_inputs(master_dir, args.allow_partial)
    casual_neutral = load_rgba(SAM_SPRITE_DIR / "neutral.png")
    uniform_neutral = load_rgba(SAM_SPRITE_DIR / "neut_uniform.png")
    outfits = {"casual": casual_neutral, "uniform": uniform_neutral}

    master_paths: dict[str, Path] = {
        expression: master_dir / f"expression_{expression}.png"
        for expression in expressions
    }
    featureless_path = master_dir / "featureless.png"
    if featureless_path.is_file():
        master_paths = {"featureless": featureless_path, **master_paths}
    elif not args.allow_partial:
        raise FileNotFoundError(
            f"Missing {featureless_path}; it is required to build featureless bases"
        )

    master_rgb: dict[str, np.ndarray] = {
        name: load_master_rgb(path) for name, path in master_paths.items()
    }
    master_foreground = {
        name: checker_foreground(rgb) for name, rgb in master_rgb.items()
    }

    registrations: dict[str, dict[str, tuple[np.ndarray, RegistrationMetrics]]] = {
        outfit: {} for outfit in outfits
    }
    aligned_rgb: dict[tuple[str, str], np.ndarray] = {}
    aligned_valid: dict[tuple[str, str], np.ndarray] = {}
    registration_sheet_items: list[tuple[str, np.ndarray]] = []
    for outfit, neutral in outfits.items():
        for name, rgb in master_rgb.items():
            matrix, metrics = estimate_registration(
                rgb, master_foreground[name], neutral
            )
            registrations[outfit][name] = (matrix, metrics)
            aligned = warp_rgb(rgb, matrix)
            valid = warp_mask(master_foreground[name], matrix)
            aligned_rgb[(outfit, name)] = aligned
            aligned_valid[(outfit, name)] = valid
            registration_sheet_items.append(
                (f"{outfit}/{name}", aligned_master_preview(aligned, valid))
            )

    # Expression RGB is authored once from the clean casual donor, then the
    # already-sparse RGBA layer is transferred to uniform.  We still estimate
    # every master-to-uniform registration above as an independent alignment
    # audit, but never sample broad RGB from those uniform-conditioned warps.
    casual_to_uniform_matrix, casual_to_uniform_metrics = estimate_registration(
        casual_neutral[:, :, :3],
        casual_neutral[:, :, 3] >= 240,
        uniform_neutral,
    )

    review_dir = output_dir / "_review"
    output_dir.mkdir(parents=True, exist_ok=True)
    contact_sheet(
        review_dir / "sam_registration_heads.png",
        "Sam masters independently registered to each outfit head",
        registration_sheet_items,
    )

    report: dict[str, object] = {
        "canvas": [CANVAS_WIDTH, CANVAS_HEIGHT],
        "master_dir": str(master_dir),
        "output_dir": str(output_dir),
        "allow_partial": bool(args.allow_partial),
        "processed_expressions": expressions,
        "missing_expressions": [
            expression for expression in EXPRESSIONS if expression not in expressions
        ],
        "registrations": {
            outfit: {
                name: asdict(metrics)
                for name, (_, metrics) in registrations[outfit].items()
            }
            for outfit in outfits
        },
        "canonical_casual_to_uniform": {
            "matrix": casual_to_uniform_matrix.tolist(),
            "metrics": asdict(casual_to_uniform_metrics),
            "layer_transfer": "premultiplied sparse casual RGBA",
        },
    }

    if "featureless" not in master_rgb:
        report["asset_generation_skipped"] = "featureless.png is missing"
        (output_dir / "metrics.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
        write_metrics_tsv(output_dir / "metrics.tsv", report)
        print(
            f"Registered {len(expressions)} expression master(s); skipped layer generation "
            "because featureless.png is missing."
        )
        print(f"Review: {review_dir}")
        return 0

    bases: dict[str, np.ndarray] = {}
    neutral_layers: dict[str, np.ndarray] = {}
    base_metrics: dict[str, object] = {}
    composites: dict[str, list[tuple[str, np.ndarray]]] = {}
    layer_previews: dict[str, list[tuple[str, np.ndarray]]] = {}
    layer_report: dict[str, dict[str, object]] = {}

    for outfit, neutral in outfits.items():
        blank, erasure_alpha, metrics = build_featureless_base(
            neutral,
            aligned_rgb[(outfit, "featureless")],
            aligned_valid[(outfit, "featureless")],
        )
        neutral_layer = exact_neutral_overlay(neutral, blank)
        reconstructed = compose_rgba(blank, neutral_layer)
        exact = bool(np.array_equal(reconstructed, neutral))
        if not exact:
            raise RuntimeError(f"{outfit} neutral overlay failed exact reconstruction")
        if not np.array_equal(blank[:, :, 3], neutral[:, :, 3]):
            raise RuntimeError(f"{outfit} featureless base changed canonical alpha")

        bases[outfit] = blank
        neutral_layers[outfit] = neutral_layer
        base_metrics[outfit] = {
            **metrics,
            "silhouette_exact": True,
            "neutral_reconstruction_exact": exact,
            "neutral_layer_pixels": int((neutral_layer[:, :, 3] > 0).sum()),
            "erasure_alpha_pixels": int((erasure_alpha > 0).sum()),
        }
        base_filename = (
            "neut_face_base.png" if outfit == "casual" else "neut_uniform_face_base.png"
        )
        save_rgba(output_dir / base_filename, blank)
        save_rgba(output_dir / f"face_neut_{outfit}.png", neutral_layer)
        composites[outfit] = [
            ("featureless base", blank),
            ("neut (exact)", reconstructed),
        ]
        layer_previews[outfit] = [("neut", neutral_layer)]
        layer_report[outfit] = {}

    for expression in expressions:
        casual_layer, preliminary_metrics, normalization_metrics = (
            build_expression_layer(
                expression,
                bases["casual"],
                aligned_rgb[("casual", expression)],
                aligned_valid[("casual", expression)],
                aligned_rgb[("casual", "featureless")],
                aligned_valid[("casual", "featureless")],
            )
        )
        casual_layer, iris_metrics = normalize_sam_iris_palette(
            casual_layer, casual_neutral
        )
        casual_layer = enforce_native_feature_bounds(
            casual_layer, expression, casual_neutral
        )
        casual_allowed = spatial_allow_for_layer(
            casual_layer.shape[:2], expression
        )
        casual_allowed &= casual_neutral[:, :, 3] == 255
        casual_allowed &= ~protected_native_hair(casual_neutral)
        casual_metrics = measure_layer(
            casual_layer,
            casual_allowed,
            blush_pixels=preliminary_metrics.blush_pixels,
        )
        if casual_metrics.visible_pixels == 0:
            raise RuntimeError(f"casual/{expression} produced an empty expression layer")
        if casual_metrics.hidden_rgb_pixels or casual_metrics.outside_allowed_pixels:
            raise RuntimeError(
                f"casual/{expression} failed sparse-layer hygiene: {casual_metrics}"
            )

        uniform_layer = premultiplied_warp_rgba(
            casual_layer, casual_to_uniform_matrix
        )
        uniform_layer = enforce_native_feature_bounds(
            uniform_layer, expression, uniform_neutral
        )
        uniform_allowed = spatial_allow_for_layer(
            uniform_layer.shape[:2], expression
        )
        uniform_allowed &= uniform_neutral[:, :, 3] == 255
        uniform_allowed &= ~protected_native_hair(uniform_neutral)
        uniform_metrics = measure_layer(
            uniform_layer,
            uniform_allowed,
            blush_pixels=int(
                round(
                    preliminary_metrics.blush_pixels
                    * casual_to_uniform_metrics.scale**2
                )
            ),
        )
        if uniform_metrics.visible_pixels == 0:
            raise RuntimeError(f"uniform/{expression} produced an empty expression layer")
        if uniform_metrics.hidden_rgb_pixels or uniform_metrics.outside_allowed_pixels:
            raise RuntimeError(
                f"uniform/{expression} failed sparse-layer hygiene: {uniform_metrics}"
            )

        for outfit, layer, metrics in (
            ("casual", casual_layer, casual_metrics),
            ("uniform", uniform_layer, uniform_metrics),
        ):
            save_rgba(output_dir / f"face_{expression}_{outfit}.png", layer)
            composites[outfit].append(
                (expression, compose_rgba(bases[outfit], layer))
            )
            layer_previews[outfit].append((expression, layer))
            layer_report[outfit][expression] = {
                **asdict(metrics),
                "normalization_for_mask_only": normalization_metrics,
                "iris_palette": iris_metrics,
                "layer_source": (
                    "registered casual master"
                    if outfit == "casual"
                    else "premultiplied canonical casual-to-uniform transfer"
                ),
            }

    report["bases"] = base_metrics
    report["layers"] = layer_report
    for outfit in outfits:
        contact_sheet(
            review_dir / f"sam_{outfit}_heads.png",
            f"Sam {outfit}: native featureless base + conditioned face layers",
            composites[outfit],
        )
        contact_sheet(
            review_dir / f"sam_{outfit}_layers_checker.png",
            f"Sam {outfit}: sparse RGBA layers on checker",
            layer_previews[outfit],
            layer_only=True,
        )

    (output_dir / "metrics.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    write_metrics_tsv(output_dir / "metrics.tsv", report)
    print(
        f"Processed {len(expressions)} expression(s) for casual and uniform; "
        "both neutral reconstructions are exact."
    )
    print(f"Assets: {output_dir}")
    print(f"Review: {review_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
