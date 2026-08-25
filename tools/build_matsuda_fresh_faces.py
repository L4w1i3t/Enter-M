#!/usr/bin/env python3
"""Build Matsuda's face-only layeredimage assets from fresh RGB masters.

This is intentionally a clean-room processor.  Its only sprite inputs are the
two canonical neutral bases and the twenty explicitly named fresh RGB masters
under ``tmp/matsuda_rebuild_fresh/masters``.  It does not discover, inspect, or
reuse any existing Matsuda face layer.

Outputs are staged under ``tmp/matsuda_rebuild_fresh`` only.  Nothing in
``game`` is modified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, __version__ as PILLOW_VERSION


CANVAS_WIDTH = 1023
CANVAS_HEIGHT = 1537
CANVAS_SIZE = (CANVAS_WIDTH, CANVAS_HEIGHT)

TOKENS: tuple[str, ...] = (
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
OUTFITS: tuple[str, ...] = ("uniform", "casual")

# Stable regions deliberately avoid the expression itself.  Registration uses
# red hair geometry, not eyes or mouths, so extreme expressions cannot pull the
# fit off-model.
HEAD_ROI = (275, 25, 760, 520)  # x0, y0, x1, y1
EYE_ROI = (340, 260, 590, 370)
HEAD_CROP = (330, 205, 640, 485)

# The polygon follows the visible facial plane inside the hairline and jaw.
# A soft, fixed mask avoids seams while keeping ears, hair silhouette, and neck
# on the canonical base.  It is never inferred independently per expression.
UNIFORM_FACE_POLYGON: tuple[tuple[int, int], ...] = (
    (438, 222),
    (500, 223),
    (551, 242),
    (581, 270),
    (597, 303),
    (599, 340),
    (589, 375),
    (566, 407),
    (535, 433),
    (491, 449),
    (454, 439),
    (420, 419),
    (389, 394),
    (360, 367),
    (347, 333),
    (348, 299),
    (362, 268),
    (391, 241),
)
MASK_FEATHER_SIGMA = 6.25

# These authored regions encompass both brows, every eyelash/eye/iris pixel,
# the nose, and the mouth.  They are forced fully opaque so no neutral feature
# can survive beneath an alternate expression.  The broad outer polygon still
# supplies the feathered transition through stable cheek/forehead skin.
UNIFORM_MANDATORY_FEATURE_POLYGONS: tuple[tuple[tuple[int, int], ...], ...] = (
    (
        (358, 275),
        (548, 244),
        (575, 270),
        (580, 312),
        (563, 343),
        (530, 354),
        (390, 358),
        (361, 344),
        (350, 316),
    ),
    (
        (420, 350),
        (542, 345),
        (550, 385),
        (530, 414),
        (472, 424),
        (450, 414),
        (438, 398),
        (418, 380),
    ),
)


class BuildError(RuntimeError):
    """Raised when an input or generated asset violates the build contract."""


@dataclass(frozen=True)
class Registration:
    matrix: np.ndarray
    method: str
    keypoints_source: int
    keypoints_target: int
    good_matches: int
    inliers: int
    inlier_rmse: float
    scale: float
    rotation_degrees: float
    translation: tuple[float, float]

    def as_json(self) -> dict[str, Any]:
        return {
            "method": self.method,
            "matrix_source_to_target": rounded_matrix(self.matrix),
            "keypoints_source": self.keypoints_source,
            "keypoints_target": self.keypoints_target,
            "good_matches": self.good_matches,
            "inliers": self.inliers,
            "inlier_rmse_pixels": round(self.inlier_rmse, 5),
            "scale": round(self.scale, 8),
            "rotation_degrees": round(self.rotation_degrees, 6),
            "translation_pixels": [
                round(self.translation[0], 6),
                round(self.translation[1], 6),
            ],
        }


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=project_root(),
        help="Repository root (defaults to the parent of tools/).",
    )
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rounded_matrix(matrix: np.ndarray) -> list[list[float]]:
    return [[round(float(value), 9) for value in row] for row in matrix]


def affine_properties(matrix: np.ndarray) -> tuple[float, float, tuple[float, float]]:
    scale = math.hypot(float(matrix[0, 0]), float(matrix[1, 0]))
    angle = math.degrees(math.atan2(float(matrix[1, 0]), float(matrix[0, 0])))
    translation = (float(matrix[0, 2]), float(matrix[1, 2]))
    return scale, angle, translation


def compose_affines(second: np.ndarray, first: np.ndarray) -> np.ndarray:
    """Return an affine that applies *first*, then *second*."""

    first_3 = np.vstack((first.astype(np.float64), (0.0, 0.0, 1.0)))
    second_3 = np.vstack((second.astype(np.float64), (0.0, 0.0, 1.0)))
    return (second_3 @ first_3)[:2].astype(np.float64)


def load_rgba(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        if image.mode != "RGBA":
            raise BuildError(f"Expected RGBA input, got {image.mode}: {path}")
        if image.size != CANVAS_SIZE:
            raise BuildError(f"Expected {CANVAS_SIZE}, got {image.size}: {path}")
        return np.asarray(image, dtype=np.uint8).copy()


def load_rgb(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        if image.mode != "RGB":
            raise BuildError(f"Expected RGB master, got {image.mode}: {path}")
        if image.size != CANVAS_SIZE:
            raise BuildError(f"Expected {CANVAS_SIZE}, got {image.size}: {path}")
        return np.asarray(image, dtype=np.uint8).copy()


def atomic_save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    image.save(temporary, format="PNG", optimize=True)
    os.replace(temporary, path)


def atomic_save_json(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    os.replace(temporary, path)


def corner_anchor(rgb: np.ndarray) -> np.ndarray:
    samples = np.concatenate(
        (
            rgb[:16, :16].reshape(-1, 3),
            rgb[:16, -16:].reshape(-1, 3),
            rgb[-16:, :16].reshape(-1, 3),
            rgb[-16:, -16:].reshape(-1, 3),
        ),
        axis=0,
    )
    return np.median(samples.astype(np.float32), axis=0)


def master_foreground_mask(rgb: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    anchor = corner_anchor(rgb)
    if not (anchor[0] >= 230 and anchor[1] <= 50 and anchor[2] >= 180):
        raise BuildError(f"Master background is not the expected magenta anchor: {anchor}")

    delta = rgb.astype(np.float32) - anchor[None, None, :]
    distance = np.sqrt(np.sum(delta * delta, axis=2))
    foreground = distance > 36.0
    background_fraction = float(np.mean(~foreground))
    if not 0.35 <= background_fraction <= 0.75:
        raise BuildError(
            f"Implausible magenta-background fraction {background_fraction:.4f}"
        )
    return foreground, anchor, background_fraction


def red_hair_mask(rgb: np.ndarray, valid: np.ndarray) -> np.ndarray:
    red = rgb[:, :, 0].astype(np.int16)
    green = rgb[:, :, 1].astype(np.int16)
    blue = rgb[:, :, 2].astype(np.int16)
    return (
        valid
        & (red > 72)
        & (red * 100 > green * 123)
        & (red * 100 > blue * 104)
        & (green < 145)
        & (blue < 165)
    )


def globalize_local_affine(matrix: np.ndarray, origin: tuple[int, int]) -> np.ndarray:
    result = matrix.astype(np.float64).copy()
    offset = np.asarray(origin, dtype=np.float64)
    result[:, 2] += offset - result[:, :2] @ offset
    return result


def silhouette_translation(
    source_foreground: np.ndarray,
    target_foreground: np.ndarray,
    max_shift: int = 12,
) -> tuple[np.ndarray, float]:
    """Integer translation fallback using the magenta/alpha silhouette anchor."""

    x0, y0, x1, y1 = HEAD_ROI
    source = source_foreground[y0:y1, x0:x1]
    target = target_foreground[y0:y1, x0:x1]
    best_score = -1.0
    best_shift = (0, 0)
    for dy in range(-max_shift, max_shift + 1):
        for dx in range(-max_shift, max_shift + 1):
            transform = np.asarray(((1.0, 0.0, dx), (0.0, 1.0, dy)), np.float64)
            shifted = cv2.warpAffine(
                source.astype(np.uint8),
                transform,
                (source.shape[1], source.shape[0]),
                flags=cv2.INTER_NEAREST,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=0,
            ).astype(bool)
            union = np.count_nonzero(shifted | target)
            score = 0.0 if union == 0 else np.count_nonzero(shifted & target) / union
            if score > best_score:
                best_score = score
                best_shift = (dx, dy)
    matrix = np.asarray(
        ((1.0, 0.0, float(best_shift[0])), (0.0, 1.0, float(best_shift[1]))),
        dtype=np.float64,
    )
    return matrix, best_score


def register_master_to_uniform(
    source_rgb: np.ndarray,
    source_foreground: np.ndarray,
    target_rgba: np.ndarray,
) -> Registration:
    x0, y0, x1, y1 = HEAD_ROI
    target_rgb = target_rgba[:, :, :3]
    target_valid = target_rgba[:, :, 3] > 128
    source_hair = red_hair_mask(source_rgb, source_foreground)
    target_hair = red_hair_mask(target_rgb, target_valid)

    source_gray = cv2.cvtColor(source_rgb, cv2.COLOR_RGB2GRAY)[y0:y1, x0:x1]
    target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_RGB2GRAY)[y0:y1, x0:x1]
    source_mask = (source_hair[y0:y1, x0:x1].astype(np.uint8) * 255)
    target_mask = (target_hair[y0:y1, x0:x1].astype(np.uint8) * 255)

    sift = cv2.SIFT_create(nfeatures=1200, contrastThreshold=0.015, edgeThreshold=12)
    source_keypoints, source_descriptors = sift.detectAndCompute(source_gray, source_mask)
    target_keypoints, target_descriptors = sift.detectAndCompute(target_gray, target_mask)

    good_matches: list[cv2.DMatch] = []
    if source_descriptors is not None and target_descriptors is not None:
        pairs = cv2.BFMatcher(cv2.NORM_L2).knnMatch(
            source_descriptors, target_descriptors, k=2
        )
        good_matches = [
            nearest
            for nearest, runner_up in pairs
            if nearest.distance < 0.72 * runner_up.distance
        ]

    matrix_local: np.ndarray | None = None
    inlier_mask: np.ndarray | None = None
    source_points: np.ndarray | None = None
    target_points: np.ndarray | None = None
    if len(good_matches) >= 12:
        source_points = np.float32(
            [source_keypoints[match.queryIdx].pt for match in good_matches]
        )
        target_points = np.float32(
            [target_keypoints[match.trainIdx].pt for match in good_matches]
        )
        matrix_local, inlier_mask = cv2.estimateAffinePartial2D(
            source_points,
            target_points,
            method=cv2.RANSAC,
            ransacReprojThreshold=2.5,
            maxIters=3000,
            confidence=0.999,
            refineIters=20,
        )

    use_sift = matrix_local is not None and inlier_mask is not None
    if use_sift:
        matrix = globalize_local_affine(matrix_local, (x0, y0))
        scale, angle, translation = affine_properties(matrix)
        inlier_count = int(np.count_nonzero(inlier_mask))
        use_sift = (
            inlier_count >= 20
            and inlier_count / len(good_matches) >= 0.55
            and 0.98 <= scale <= 1.02
            and abs(angle) <= 1.5
            and max(abs(translation[0]), abs(translation[1])) <= 12.0
        )

    if not use_sift:
        matrix, score = silhouette_translation(
            source_foreground, target_rgba[:, :, 3] > 8
        )
        if score < 0.90:
            raise BuildError(f"Hair registration and silhouette fallback both failed ({score=})")
        scale, angle, translation = affine_properties(matrix)
        return Registration(
            matrix=matrix,
            method="magenta_silhouette_translation",
            keypoints_source=len(source_keypoints),
            keypoints_target=len(target_keypoints),
            good_matches=len(good_matches),
            inliers=0,
            inlier_rmse=0.0,
            scale=scale,
            rotation_degrees=angle,
            translation=translation,
        )

    assert source_points is not None
    assert target_points is not None
    assert inlier_mask is not None
    local_inliers = inlier_mask.ravel().astype(bool)
    predicted = cv2.transform(source_points[None, :, :], matrix_local)[0]
    residual = predicted[local_inliers] - target_points[local_inliers]
    rmse = float(np.sqrt(np.mean(np.sum(residual * residual, axis=1))))
    if rmse > 1.75:
        raise BuildError(f"Hair registration reprojection error is too high: {rmse:.3f}px")
    scale, angle, translation = affine_properties(matrix)
    return Registration(
        matrix=matrix,
        method="sift_hair_geometry_ransac",
        keypoints_source=len(source_keypoints),
        keypoints_target=len(target_keypoints),
        good_matches=len(good_matches),
        inliers=int(np.count_nonzero(inlier_mask)),
        inlier_rmse=rmse,
        scale=scale,
        rotation_degrees=angle,
        translation=translation,
    )


def detect_eye_centers(rgba: np.ndarray) -> list[tuple[float, float]]:
    x0, y0, x1, y1 = EYE_ROI
    rgb = rgba[:, :, :3]
    red = rgb[:, :, 0].astype(np.int16)
    green = rgb[:, :, 1].astype(np.int16)
    blue = rgb[:, :, 2].astype(np.int16)
    green_score = green - np.maximum(red, blue)
    candidate = (
        (rgba[:, :, 3] > 128)
        & (green_score > 18)
        & (green > 70)
        & (red < 145)
    )
    roi = candidate[y0:y1, x0:x1].astype(np.uint8)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(roi, connectivity=8)
    components: list[tuple[int, int]] = []
    for label in range(1, count):
        area = int(stats[label, cv2.CC_STAT_AREA])
        if 40 <= area <= 500:
            components.append((area, label))
    components.sort(reverse=True)
    if len(components) < 2:
        raise BuildError("Could not identify both canonical green irises")

    centers: list[tuple[float, float]] = []
    for _, label in components[:2]:
        ys, xs = np.where(labels == label)
        weights = green_score[y0 + ys, x0 + xs].astype(np.float64)
        centers.append(
            (
                float(np.average(x0 + xs, weights=weights)),
                float(np.average(y0 + ys, weights=weights)),
            )
        )
    centers.sort(key=lambda point: point[0])
    if centers[1][0] - centers[0][0] < 70.0:
        raise BuildError(f"Detected iris centers are implausibly close: {centers}")
    return centers


def similarity_from_point_pair(
    source_points: Sequence[tuple[float, float]],
    target_points: Sequence[tuple[float, float]],
) -> np.ndarray:
    source = np.asarray(source_points, dtype=np.float64)
    target = np.asarray(target_points, dtype=np.float64)
    source_vector = source[1] - source[0]
    target_vector = target[1] - target[0]
    scale = float(np.linalg.norm(target_vector) / np.linalg.norm(source_vector))
    angle = math.atan2(target_vector[1], target_vector[0]) - math.atan2(
        source_vector[1], source_vector[0]
    )
    linear = scale * np.asarray(
        ((math.cos(angle), -math.sin(angle)), (math.sin(angle), math.cos(angle))),
        dtype=np.float64,
    )
    translation = target[0] - linear @ source[0]
    return np.column_stack((linear, translation))


def canonical_outfit_registration(
    uniform_rgba: np.ndarray, casual_rgba: np.ndarray
) -> tuple[np.ndarray, dict[str, Any]]:
    uniform_eyes = detect_eye_centers(uniform_rgba)
    casual_eyes = detect_eye_centers(casual_rgba)
    matrix = similarity_from_point_pair(uniform_eyes, casual_eyes)
    scale, angle, translation = affine_properties(matrix)
    if not (
        0.97 <= scale <= 1.03
        and abs(angle) <= 2.0
        and max(abs(translation[0]), abs(translation[1])) <= 15.0
    ):
        raise BuildError(
            "Canonical uniform-to-casual eye transform is implausible: "
            f"scale={scale:.5f}, angle={angle:.3f}, translation={translation}"
        )
    payload = {
        "method": "canonical_green_iris_pair_similarity",
        "uniform_eye_centers": [[round(x, 5), round(y, 5)] for x, y in uniform_eyes],
        "casual_eye_centers": [[round(x, 5), round(y, 5)] for x, y in casual_eyes],
        "matrix_uniform_to_casual": rounded_matrix(matrix),
        "scale": round(scale, 8),
        "rotation_degrees": round(angle, 6),
        "translation_pixels": [round(translation[0], 6), round(translation[1], 6)],
    }
    return matrix, payload


def make_uniform_feature_coverage() -> np.ndarray:
    coverage = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH), dtype=np.uint8)
    for points in UNIFORM_MANDATORY_FEATURE_POLYGONS:
        polygon = np.asarray(points, dtype=np.int32)
        cv2.fillPoly(coverage, [polygon], 255, lineType=cv2.LINE_8)
    return coverage > 0


def apply_lower_jaw_inset(mask: np.ndarray, canonical_alpha: np.ndarray) -> np.ndarray:
    canonical_opaque = canonical_alpha == 255
    silhouette_distance = cv2.distanceTransform(
        canonical_opaque.astype(np.uint8), cv2.DIST_L2, 5
    )
    yy = np.indices(canonical_opaque.shape)[0]
    jaw_region = yy >= 360
    jaw_ramp = np.clip(
        np.rint((silhouette_distance - 4.0) * (255.0 / 8.0)), 0.0, 255.0
    ).astype(np.uint8)
    result = mask.copy()
    result[jaw_region] = np.minimum(result[jaw_region], jaw_ramp[jaw_region])
    return result


def make_uniform_face_mask(canonical_alpha: np.ndarray) -> np.ndarray:
    binary = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH), dtype=np.float32)
    polygon = np.asarray(UNIFORM_FACE_POLYGON, dtype=np.int32)
    cv2.fillPoly(binary, [polygon], 1.0, lineType=cv2.LINE_8)
    feathered = cv2.GaussianBlur(
        binary,
        (0, 0),
        sigmaX=MASK_FEATHER_SIGMA,
        sigmaY=MASK_FEATHER_SIGMA,
        borderType=cv2.BORDER_CONSTANT,
    )
    mask = np.clip(np.rint(feathered * 255.0), 0.0, 255.0).astype(np.uint8)
    canonical_opaque = canonical_alpha == 255
    mask[~canonical_opaque] = 0
    mask = apply_lower_jaw_inset(mask, canonical_alpha)
    mandatory = make_uniform_feature_coverage() & canonical_opaque
    mask[mandatory] = 255
    return keep_largest_alpha_component(mask)


def keep_largest_alpha_component(mask: np.ndarray) -> np.ndarray:
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        (mask > 0).astype(np.uint8), connectivity=8
    )
    if count <= 2:
        return mask
    largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    cleaned = mask.copy()
    cleaned[labels != largest] = 0
    return cleaned


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
    warped = cv2.warpAffine(
        mask,
        matrix,
        CANVAS_SIZE,
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )
    return keep_largest_alpha_component(warped)


def warp_binary(mask: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    return cv2.warpAffine(
        mask.astype(np.uint8),
        matrix,
        CANVAS_SIZE,
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    ).astype(bool)


def anchor_like_pixels(rgb: np.ndarray) -> np.ndarray:
    return (
        (rgb[:, :, 0] >= 220)
        & (rgb[:, :, 1] <= 70)
        & (rgb[:, :, 2] >= 175)
        & (rgb[:, :, 0].astype(np.int16) - rgb[:, :, 1].astype(np.int16) >= 145)
    )


def chroma_key_fringe_like_pixels(rgb: np.ndarray) -> np.ndarray:
    """Catch diluted magenta fringes that no longer match the exact key color."""

    red = rgb[:, :, 0].astype(np.int16)
    green = rgb[:, :, 1].astype(np.int16)
    blue = rgb[:, :, 2].astype(np.int16)
    return (
        (red > 120)
        & (blue > 100)
        & (green < 110)
        & ((np.minimum(red, blue) - green) > 45)
    )


def infill_anchor_matte(
    expression_rgb: np.ndarray,
    canonical_rgb: np.ndarray,
    active_alpha: np.ndarray,
) -> tuple[np.ndarray, int]:
    contaminated = anchor_like_pixels(expression_rgb) & (active_alpha > 0)
    count = int(np.count_nonzero(contaminated))
    if count == 0:
        return expression_rgb, 0
    repaired = expression_rgb.copy()
    repaired[contaminated] = canonical_rgb[contaminated]
    return repaired, count


def canonical_hair_guard(
    canonical_rgba: np.ndarray, mandatory_features: np.ndarray
) -> np.ndarray:
    """Protect canonical hair/clothing while allowing face art to be replaced."""

    hair = red_hair_mask(canonical_rgba[:, :, :3], canonical_rgba[:, :, 3] > 128)
    hair = cv2.morphologyEx(
        hair.astype(np.uint8),
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
    ).astype(bool)
    hair = cv2.dilate(
        hair.astype(np.uint8),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
        iterations=1,
    ).astype(bool)
    non_skin = ~skin_pixels(canonical_rgba[:, :, :3])
    opaque = canonical_rgba[:, :, 3] == 255
    silhouette_distance = cv2.distanceTransform(opaque.astype(np.uint8), cv2.DIST_L2, 5)
    yy = np.indices(opaque.shape)[0]
    lower_face_rim = (yy >= 360) & (silhouette_distance <= 3.2)
    return ((hair | non_skin) & ~mandatory_features) | lower_face_rim


def preserve_canonical_hair(
    expression_rgb: np.ndarray,
    canonical_rgb: np.ndarray,
    guard: np.ndarray,
    active_alpha: np.ndarray,
) -> np.ndarray:
    protected = guard & (active_alpha > 0)
    if not np.any(protected):
        return expression_rgb
    result = expression_rgb.copy()
    result[protected] = canonical_rgb[protected]
    return result


def skin_pixels(rgb: np.ndarray) -> np.ndarray:
    red = rgb[:, :, 0].astype(np.int16)
    green = rgb[:, :, 1].astype(np.int16)
    blue = rgb[:, :, 2].astype(np.int16)
    return (
        (red > 165)
        & (green > 100)
        & (blue > 82)
        & (red * 100 > green * 106)
        & (green * 100 > blue * 101)
    )


def stable_skin_zone() -> np.ndarray:
    zone = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH), dtype=bool)
    # Forehead, outer cheek, and lower jaw remain expression-independent.
    zone[250:286, 456:535] = True
    zone[323:388, 535:565] = True
    zone[386:430, 425:535] = True
    zone[350:390, 392:422] = True
    return zone


def master_color_offset(
    aligned_rgb: np.ndarray, uniform_rgb: np.ndarray, uniform_mask: np.ndarray
) -> tuple[np.ndarray, int]:
    reference = (
        stable_skin_zone()
        & (uniform_mask >= 240)
        & skin_pixels(aligned_rgb)
        & skin_pixels(uniform_rgb)
    )
    if np.count_nonzero(reference) < 1000:
        raise BuildError("Too few stable skin pixels for master color normalization")
    difference = uniform_rgb.astype(np.int16) - aligned_rgb.astype(np.int16)
    offset = np.median(difference[reference], axis=0)
    offset = np.clip(offset, -8.0, 8.0).astype(np.float32)
    return offset, int(np.count_nonzero(reference))


def apply_color_offset(rgb: np.ndarray, offset: np.ndarray) -> np.ndarray:
    corrected = rgb.astype(np.float32) + offset[None, None, :]
    return np.clip(np.rint(corrected), 0.0, 255.0).astype(np.uint8)


def casual_tone_field(
    uniform_rgba: np.ndarray,
    casual_rgba: np.ndarray,
    uniform_to_casual: np.ndarray,
) -> np.ndarray:
    warped_uniform = warp_rgb(uniform_rgba[:, :, :3], uniform_to_casual)
    difference = casual_rgba[:, :, :3].astype(np.float32) - warped_uniform.astype(
        np.float32
    )
    low_frequency = cv2.GaussianBlur(
        difference,
        (0, 0),
        sigmaX=14.0,
        sigmaY=14.0,
        borderType=cv2.BORDER_REFLECT,
    )
    return np.clip(low_frequency, -12.0, 12.0)


def make_layer(rgb: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    rgba = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH, 4), dtype=np.uint8)
    rgba[:, :, :3] = rgb
    rgba[:, :, 3] = alpha
    rgba[alpha == 0, :3] = 0
    return rgba


def alpha_metrics(alpha: np.ndarray) -> dict[str, Any]:
    nonzero = alpha > 0
    count, _, stats, _ = cv2.connectedComponentsWithStats(
        nonzero.astype(np.uint8), connectivity=8
    )
    components = count - 1
    if np.any(nonzero):
        ys, xs = np.where(nonzero)
        bbox: list[int] | None = [
            int(xs.min()),
            int(ys.min()),
            int(xs.max()),
            int(ys.max()),
        ]
    else:
        bbox = None
    component_areas = sorted(
        (int(stats[index, cv2.CC_STAT_AREA]) for index in range(1, count)),
        reverse=True,
    )
    return {
        "nonzero_pixels": int(np.count_nonzero(nonzero)),
        "fully_opaque_pixels": int(np.count_nonzero(alpha == 255)),
        "partial_alpha_pixels": int(np.count_nonzero((alpha > 0) & (alpha < 255))),
        "unique_alpha_levels": int(np.unique(alpha).size),
        "components": components,
        "component_areas": component_areas,
        "nonzero_bbox_xyxy": bbox,
    }


def lower_jaw_inset_metrics(
    alpha: np.ndarray, canonical_alpha: np.ndarray, mandatory_features: np.ndarray
) -> dict[str, Any]:
    opaque = canonical_alpha == 255
    distance = cv2.distanceTransform(opaque.astype(np.uint8), cv2.DIST_L2, 5)
    yy = np.indices(opaque.shape)[0]
    nonfeature_support = (alpha > 0) & (yy >= 360) & ~mandatory_features
    minimum = (
        float(np.min(distance[nonfeature_support]))
        if np.any(nonfeature_support)
        else None
    )
    return {
        "lower_nonfeature_minimum_silhouette_inset_pixels": (
            None if minimum is None else round(minimum, 6)
        ),
        "lower_nonfeature_support_at_or_below_4px_inset": int(
            np.count_nonzero(nonfeature_support & (distance <= 4.0))
        ),
    }


def checker_periodicity(rgb: np.ndarray, alpha: np.ndarray) -> dict[str, float]:
    """Measure square-grid correlation on smooth skin; lower is better."""

    x0, y0, x1, y1 = 365, 235, 585, 455
    crop = rgb[y0:y1, x0:x1].astype(np.float32)
    valid = (alpha[y0:y1, x0:x1] >= 240) & skin_pixels(rgb[y0:y1, x0:x1])
    luminance = 0.2126 * crop[:, :, 0] + 0.7152 * crop[:, :, 1] + 0.0722 * crop[:, :, 2]
    results: dict[str, float] = {}
    yy, xx = np.indices(luminance.shape)
    for period in (2, 4, 8, 12, 16):
        smooth = cv2.GaussianBlur(luminance, (0, 0), sigmaX=max(2.0, period / 2))
        residual = luminance - smooth
        best = 0.0
        step = max(1, period // 3)
        for y_shift in range(0, period, step):
            for x_shift in range(0, period, step):
                pattern = (
                    (((xx + x_shift) // period + (yy + y_shift) // period) & 1)
                    * 2.0
                    - 1.0
                )
                values = residual[valid]
                pattern_values = pattern[valid]
                if values.size < 500:
                    continue
                values = values - np.mean(values)
                pattern_values = pattern_values - np.mean(pattern_values)
                denominator = float(
                    np.sqrt(np.sum(values * values) * np.sum(pattern_values * pattern_values))
                )
                correlation = 0.0 if denominator == 0 else abs(float(np.sum(values * pattern_values)) / denominator)
                best = max(best, correlation)
        results[str(period)] = round(best, 7)
    return results


def layer_metrics(rgba: np.ndarray, expected_alpha: np.ndarray) -> dict[str, Any]:
    alpha = rgba[:, :, 3]
    rgb = rgba[:, :, :3]
    hidden = alpha == 0
    edge = (alpha > 0) & (alpha < 255)
    magenta = (
        (rgb[:, :, 0] >= 220)
        & (rgb[:, :, 1] <= 70)
        & (rgb[:, :, 2] >= 175)
        & (rgb[:, :, 0].astype(np.int16) - rgb[:, :, 1].astype(np.int16) >= 145)
    )
    magenta_fringe = chroma_key_fringe_like_pixels(rgb)
    pure_black = np.all(rgb <= 2, axis=2)
    pure_white = np.all(rgb >= 253, axis=2)
    common_checker = (
        np.all(rgb == np.asarray((192, 192, 192), dtype=np.uint8), axis=2)
        | np.all(rgb == np.asarray((128, 128, 128), dtype=np.uint8), axis=2)
        | np.all(rgb == np.asarray((224, 224, 224), dtype=np.uint8), axis=2)
    )
    metrics = alpha_metrics(alpha)
    metrics.update(
        {
            "alpha_matches_fixed_outfit_mask": bool(np.array_equal(alpha, expected_alpha)),
            "hidden_rgb_nonzero_values": int(np.count_nonzero(rgb[hidden])),
            "active_magenta_anchor_pixels": int(np.count_nonzero(magenta & (alpha > 0))),
            "active_diluted_magenta_fringe_pixels": int(
                np.count_nonzero(magenta_fringe & (alpha > 0))
            ),
            "feather_edge_pure_black_pixels": int(np.count_nonzero(pure_black & edge)),
            "feather_edge_pure_white_pixels": int(np.count_nonzero(pure_white & edge)),
            "active_common_checker_palette_pixels": int(
                np.count_nonzero(common_checker & (alpha > 0))
            ),
            "checker_periodicity_by_tile_pixels": checker_periodicity(rgb, alpha),
        }
    )
    return metrics


def composite_character(base_rgba: np.ndarray, layer_rgba: np.ndarray) -> Image.Image:
    base = Image.fromarray(base_rgba, mode="RGBA")
    layer = Image.fromarray(layer_rgba, mode="RGBA")
    return Image.alpha_composite(base, layer)


def checker_background(size: tuple[int, int], tile: int = 16) -> Image.Image:
    width, height = size
    yy, xx = np.indices((height, width))
    cells = ((xx // tile + yy // tile) & 1).astype(bool)
    rgb = np.empty((height, width, 4), dtype=np.uint8)
    rgb[cells] = (105, 105, 105, 255)
    rgb[~cells] = (165, 165, 165, 255)
    return Image.fromarray(rgb, mode="RGBA")


def solid_background(size: tuple[int, int], value: int) -> Image.Image:
    return Image.new("RGBA", size, (value, value, value, 255))


def labeled_cell(
    character: Image.Image,
    label: str,
    background_kind: str,
    content_size: tuple[int, int],
    crop: tuple[int, int, int, int] | None,
) -> Image.Image:
    label_height = 22
    width, height = content_size
    if background_kind == "checker":
        background = checker_background(character.size)
        cell_background = checker_background((width, height + label_height))
        label_fill = (245, 245, 245, 255)
        label_back = (40, 40, 40, 255)
    else:
        level = 238 if background_kind == "light" else 24
        background = solid_background(character.size, level)
        cell_background = solid_background((width, height + label_height), level)
        label_fill = (24, 24, 24, 255) if level > 128 else (240, 240, 240, 255)
        label_back = (level, level, level, 255)

    rendered = Image.alpha_composite(background, character)
    if crop is not None:
        rendered = rendered.crop(crop)
    rendered = rendered.resize(content_size, Image.Resampling.LANCZOS)
    cell_background.alpha_composite(rendered, (0, 0))
    draw = ImageDraw.Draw(cell_background)
    draw.rectangle((0, height, width, height + label_height), fill=label_back)
    font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), label, font=font)
    text_width = bbox[2] - bbox[0]
    draw.text(
        (max(4, (width - text_width) // 2), height + 5),
        label,
        fill=label_fill,
        font=font,
    )
    return cell_background


def make_contact_sheet(
    entries: Sequence[tuple[str, Image.Image]],
    background_kind: str,
    columns: int,
    content_size: tuple[int, int],
    crop: tuple[int, int, int, int] | None,
) -> Image.Image:
    rows = math.ceil(len(entries) / columns)
    cell_width, content_height = content_size
    cell_height = content_height + 22
    sheet = solid_background(
        (cell_width * columns, cell_height * rows),
        238 if background_kind == "light" else 24,
    )
    for index, (label, character) in enumerate(entries):
        cell = labeled_cell(
            character, label, background_kind, content_size=content_size, crop=crop
        )
        x = (index % columns) * cell_width
        y = (index // columns) * cell_height
        sheet.alpha_composite(cell, (x, y))
    return sheet.convert("RGB")


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def validate_declared_inputs(paths: Iterable[Path]) -> None:
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise BuildError("Missing required input(s): " + ", ".join(map(str, missing)))


def run(root: Path) -> dict[str, Any]:
    root = root.resolve()
    matsuda_dir = root / "game" / "mod_assets" / "char_sprites" / "matsuda"
    build_dir = root / "tmp" / "matsuda_rebuild_fresh"
    masters_dir = build_dir / "masters"
    faces_dir = build_dir / "faces"
    diagnostics_dir = build_dir / "diagnostics"

    base_paths = {
        "uniform": matsuda_dir / "neut_uniform.png",
        "casual": matsuda_dir / "neutral.png",
    }
    master_paths = {
        token: masters_dir / f"face_{token}_uniform.png" for token in TOKENS
    }
    allowed_inputs = [*base_paths.values(), *master_paths.values()]
    validate_declared_inputs(allowed_inputs)
    expected_master_names = {path.name for path in master_paths.values()}
    staged_master_names = {
        path.name for path in masters_dir.glob("*.png") if path.is_file()
    }
    if staged_master_names != expected_master_names:
        missing = sorted(expected_master_names - staged_master_names)
        unexpected = sorted(staged_master_names - expected_master_names)
        raise BuildError(
            "Fresh master set must contain exactly the 20 declared expressions; "
            f"missing={missing}, unexpected={unexpected}"
        )

    expected_face_names = {
        f"face_neut_{outfit}.png" for outfit in OUTFITS
    } | {
        f"face_{token}_{outfit}.png" for token in TOKENS for outfit in OUTFITS
    }
    faces_dir.mkdir(parents=True, exist_ok=True)
    unexpected_existing = {
        path.name for path in faces_dir.glob("*.png") if path.name not in expected_face_names
    }
    if unexpected_existing:
        raise BuildError(
            "Refusing to mix undeclared PNGs into the 42-file output set: "
            + ", ".join(sorted(unexpected_existing))
        )

    bases = {outfit: load_rgba(path) for outfit, path in base_paths.items()}
    uniform_to_casual, outfit_registration = canonical_outfit_registration(
        bases["uniform"], bases["casual"]
    )

    registrations: dict[str, Any] = {}
    per_expression: dict[str, Any] = {}
    background_anchors: dict[str, Any] = {}
    master_data: dict[str, tuple[np.ndarray, np.ndarray, Registration]] = {}
    for token in TOKENS:
        master_rgb = load_rgb(master_paths[token])
        foreground, anchor, background_fraction = master_foreground_mask(master_rgb)
        registration = register_master_to_uniform(
            master_rgb, foreground, bases["uniform"]
        )
        master_data[token] = (master_rgb, foreground, registration)
        registrations[token] = registration.as_json()
        background_anchors[token] = {
            "corner_median_rgb": [round(float(value), 4) for value in anchor],
            "background_fraction": round(background_fraction, 7),
        }

    mandatory_features = {"uniform": make_uniform_feature_coverage()}
    mandatory_features["casual"] = warp_binary(
        mandatory_features["uniform"], uniform_to_casual
    )
    masks = {"uniform": make_uniform_face_mask(bases["uniform"][:, :, 3])}
    masks["casual"] = warp_mask(masks["uniform"], uniform_to_casual)
    masks["casual"][bases["casual"][:, :, 3] != 255] = 0
    masks["casual"] = apply_lower_jaw_inset(
        masks["casual"], bases["casual"][:, :, 3]
    )
    masks["casual"][
        mandatory_features["casual"] & (bases["casual"][:, :, 3] == 255)
    ] = 255
    masks["casual"] = keep_largest_alpha_component(masks["casual"])
    hair_guards = {
        outfit: canonical_hair_guard(bases[outfit], mandatory_features[outfit])
        for outfit in OUTFITS
    }
    for outfit, mask in masks.items():
        mask_report = alpha_metrics(mask)
        if mask_report["components"] != 1:
            raise BuildError(f"{outfit} mask is not one connected component")
        if mask_report["unique_alpha_levels"] != 256:
            raise BuildError(
                f"{outfit} feather mask must contain all 256 uint8 alpha levels; "
                f"found {mask_report['unique_alpha_levels']}"
            )
        if np.any((mask > 0) & (bases[outfit][:, :, 3] != 255)):
            raise BuildError(f"{outfit} mask extends outside the opaque base silhouette")
        uncovered_features = int(
            np.count_nonzero(
                mandatory_features[outfit]
                & (bases[outfit][:, :, 3] == 255)
                & (mask != 255)
            )
        )
        if uncovered_features:
            raise BuildError(
                f"{outfit} mask leaves {uncovered_features} mandatory feature pixels "
                "below full opacity"
            )

    casual_field = casual_tone_field(
        bases["uniform"], bases["casual"], uniform_to_casual
    )

    transparent = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH, 4), dtype=np.uint8)
    layers: dict[tuple[str, str], np.ndarray] = {}
    layers[("neut", "uniform")] = transparent.copy()
    layers[("neut", "casual")] = transparent.copy()

    for token in TOKENS:
        master_rgb, _, registration = master_data[token]

        uniform_aligned = warp_rgb(master_rgb, registration.matrix)
        uniform_aligned, uniform_matte_infill = infill_anchor_matte(
            uniform_aligned, bases["uniform"][:, :, :3], masks["uniform"]
        )
        offset, sample_count = master_color_offset(
            uniform_aligned, bases["uniform"][:, :, :3], masks["uniform"]
        )
        uniform_expression = apply_color_offset(uniform_aligned, offset)
        uniform_expression = preserve_canonical_hair(
            uniform_expression,
            bases["uniform"][:, :, :3],
            hair_guards["uniform"],
            masks["uniform"],
        )
        uniform_layer = make_layer(uniform_expression, masks["uniform"])

        master_to_casual = compose_affines(uniform_to_casual, registration.matrix)
        casual_expression = warp_rgb(master_rgb, master_to_casual).astype(np.float32)
        casual_expression += offset[None, None, :]
        casual_expression += casual_field
        casual_expression = np.clip(np.rint(casual_expression), 0.0, 255.0).astype(
            np.uint8
        )
        casual_expression, casual_matte_infill = infill_anchor_matte(
            casual_expression, bases["casual"][:, :, :3], masks["casual"]
        )
        casual_expression = preserve_canonical_hair(
            casual_expression,
            bases["casual"][:, :, :3],
            hair_guards["casual"],
            masks["casual"],
        )
        casual_layer = make_layer(casual_expression, masks["casual"])

        layers[(token, "uniform")] = uniform_layer
        layers[(token, "casual")] = casual_layer
        per_expression[token] = {
            "uniform_skin_color_offset_rgb": [float(value) for value in offset],
            "skin_reference_samples": sample_count,
            "matrix_master_to_casual": rounded_matrix(master_to_casual),
            "uniform_magenta_matte_pixels_infilled": uniform_matte_infill,
            "casual_magenta_matte_pixels_infilled": casual_matte_infill,
        }

    output_metrics: dict[str, Any] = {}
    output_hashes: dict[str, str] = {}
    ordered_keys: list[tuple[str, str]] = []
    for outfit in OUTFITS:
        ordered_keys.append(("neut", outfit))
        ordered_keys.extend((token, outfit) for token in TOKENS)

    for token, outfit in ordered_keys:
        filename = f"face_{token}_{outfit}.png"
        path = faces_dir / filename
        layer = layers[(token, outfit)]
        expected_alpha = (
            np.zeros_like(masks[outfit]) if token == "neut" else masks[outfit]
        )
        metrics = layer_metrics(layer, expected_alpha)
        layer_alpha_16 = layer[:, :, 3].astype(np.uint16)
        base_alpha_16 = bases[outfit][:, :, 3].astype(np.uint16)
        composite_alpha = layer_alpha_16 + (
            base_alpha_16 * (255 - layer_alpha_16) + 127
        ) // 255
        metrics["composite_alpha_matches_canonical_base"] = bool(
            np.array_equal(composite_alpha.astype(np.uint8), bases[outfit][:, :, 3])
        )
        if metrics["hidden_rgb_nonzero_values"] != 0:
            raise BuildError(f"{filename} has hidden RGB under zero alpha")
        if metrics["active_magenta_anchor_pixels"] != 0:
            raise BuildError(f"{filename} retained magenta anchor pixels")
        if metrics["active_diluted_magenta_fringe_pixels"] != 0:
            raise BuildError(f"{filename} retained diluted magenta fringe pixels")
        if not metrics["alpha_matches_fixed_outfit_mask"]:
            raise BuildError(f"{filename} does not use its fixed outfit alpha")
        if not metrics["composite_alpha_matches_canonical_base"]:
            raise BuildError(f"{filename} changes the canonical base silhouette")
        if token != "neut" and metrics["components"] != 1:
            raise BuildError(f"{filename} has detached alpha components")
        if token == "neut" and metrics["nonzero_pixels"] != 0:
            raise BuildError(f"{filename} is not fully transparent")
        atomic_save_png(Image.fromarray(layer, mode="RGBA"), path)
        output_metrics[filename] = metrics
        output_hashes[filename] = sha256_file(path)

    actual_face_names = {path.name for path in faces_dir.glob("*.png")}
    if actual_face_names != expected_face_names:
        missing = sorted(expected_face_names - actual_face_names)
        extra = sorted(actual_face_names - expected_face_names)
        raise BuildError(f"Output set mismatch; missing={missing}, extra={extra}")

    composite_uniqueness: dict[str, Any] = {}
    for outfit in OUTFITS:
        signatures: dict[str, str] = {}
        duplicates: list[dict[str, str]] = []
        for token in ("neut", *TOKENS):
            composite = np.asarray(
                composite_character(bases[outfit], layers[(token, outfit)]),
                dtype=np.uint8,
            )
            signature = hashlib.sha256(composite.tobytes()).hexdigest()
            previous = signatures.get(signature)
            if previous is not None:
                duplicates.append({"token": token, "duplicates": previous})
            signatures[signature] = token
        if duplicates:
            raise BuildError(f"{outfit} expression composites are duplicated: {duplicates}")
        composite_uniqueness[outfit] = {
            "expression_count": len(signatures),
            "unique_composite_count": len(signatures),
            "pairwise_distinct": True,
        }

    diagnostics_dir.mkdir(parents=True, exist_ok=True)
    mask_paths: dict[str, Path] = {}
    for outfit, mask in masks.items():
        path = diagnostics_dir / f"mask_{outfit}.png"
        atomic_save_png(Image.fromarray(mask, mode="L"), path)
        mask_paths[outfit] = path

    rendered_entries: list[tuple[str, Image.Image]] = []
    for outfit in OUTFITS:
        for token in ("neut", *TOKENS):
            rendered_entries.append(
                (
                    f"{outfit}/{token}",
                    composite_character(bases[outfit], layers[(token, outfit)]),
                )
            )

    story_regressions = [
        (
            f"casual/{token} — 0517.rpy",
            composite_character(bases["casual"], layers[(token, "casual")]),
        )
        for token in ("neut", "smug", "thinking")
    ]

    diagnostic_hashes: dict[str, str] = {}
    for background_kind in ("light", "dark", "checker"):
        full_path = diagnostics_dir / f"contact_{background_kind}.png"
        head_path = diagnostics_dir / f"heads_{background_kind}.png"
        regression_path = diagnostics_dir / f"regression_0517_{background_kind}.png"
        full_sheet = make_contact_sheet(
            rendered_entries,
            background_kind,
            columns=7,
            content_size=(180, 270),
            crop=None,
        )
        head_sheet = make_contact_sheet(
            rendered_entries,
            background_kind,
            columns=5,
            content_size=(310, 280),
            crop=HEAD_CROP,
        )
        regression_sheet = make_contact_sheet(
            story_regressions,
            background_kind,
            columns=1,
            content_size=(620, 560),
            crop=HEAD_CROP,
        )
        atomic_save_png(full_sheet, full_path)
        atomic_save_png(head_sheet, head_path)
        atomic_save_png(regression_sheet, regression_path)
        diagnostic_hashes[full_path.name] = sha256_file(full_path)
        diagnostic_hashes[head_path.name] = sha256_file(head_path)
        diagnostic_hashes[regression_path.name] = sha256_file(regression_path)

    mask_reports = {
        outfit: {
            **alpha_metrics(mask),
            **lower_jaw_inset_metrics(
                mask, bases[outfit][:, :, 3], mandatory_features[outfit]
            ),
            "mandatory_feature_pixels": int(
                np.count_nonzero(
                    mandatory_features[outfit] & (bases[outfit][:, :, 3] == 255)
                )
            ),
            "mandatory_feature_pixels_below_full_opacity": int(
                np.count_nonzero(
                    mandatory_features[outfit]
                    & (bases[outfit][:, :, 3] == 255)
                    & (mask != 255)
                )
            ),
            "sha256": sha256_file(mask_paths[outfit]),
            "path": relative(mask_paths[outfit], root),
        }
        for outfit, mask in masks.items()
    }
    max_checker_score = max(
        score
        for name, metrics in output_metrics.items()
        if "_neut_" not in name
        for score in metrics["checker_periodicity_by_tile_pixels"].values()
    )
    validation = {
        "passed": True,
        "face_png_count": len(actual_face_names),
        "expected_face_png_count": 42,
        "all_dimensions_1023x1537": True,
        "all_rgba": True,
        "neutral_pair_fully_transparent": True,
        "alternate_alpha_is_fixed_per_outfit": True,
        "zero_hidden_rgb": True,
        "zero_active_magenta_anchor_pixels": True,
        "zero_active_diluted_magenta_fringe_pixels": True,
        "no_detached_alpha_components": True,
        "composite_alpha_matches_canonical_bases": True,
        "all_expression_composites_pairwise_distinct": True,
        "composite_uniqueness": composite_uniqueness,
        "maximum_checker_periodicity_score": round(float(max_checker_score), 7),
    }

    payload: dict[str, Any] = {
        "schema_version": 1,
        "builder": relative(Path(__file__), root),
        "builder_sha256": sha256_file(Path(__file__)),
        "canvas": {"width": CANVAS_WIDTH, "height": CANVAS_HEIGHT},
        "versions": {
            "python": sys.version.split()[0],
            "opencv": cv2.__version__,
            "pillow": PILLOW_VERSION,
            "numpy": np.__version__,
        },
        "input_policy": {
            "clean_room": True,
            "opened_sprite_inputs": [relative(path, root) for path in allowed_inputs],
            "opened_sprite_input_count": len(allowed_inputs),
            "master_pattern": "tmp/matsuda_rebuild_fresh/masters/face_<token>_uniform.png",
            "legacy_or_existing_face_layers_opened": False,
            "generation_anchor_files_opened": False,
        },
        "inputs": {
            relative(path, root): {
                "sha256": sha256_file(path),
                "role": (
                    "canonical_neutral_base"
                    if path in base_paths.values()
                    else "fresh_rgb_expression_master"
                ),
            }
            for path in allowed_inputs
        },
        "uniform_master_registration": registrations,
        "uniform_to_casual_registration": outfit_registration,
        "master_background_anchors": background_anchors,
        "expression_processing": per_expression,
        "masks": mask_reports,
        "outputs": {
            "directory": relative(faces_dir, root),
            "sha256": output_hashes,
            "metrics": output_metrics,
        },
        "diagnostics": {
            "directory": relative(diagnostics_dir, root),
            "sha256": diagnostic_hashes,
        },
        "validation": validation,
    }
    metrics_path = build_dir / "face_build_metrics.json"
    atomic_save_json(payload, metrics_path)
    return payload


def main() -> int:
    args = parse_args()
    try:
        payload = run(args.project_root)
    except (BuildError, OSError, ValueError, cv2.error) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    validation = payload["validation"]
    print(
        "Built and validated "
        f"{validation['face_png_count']} Matsuda face layers; "
        f"max checker score={validation['maximum_checker_periodicity_score']:.5f}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
