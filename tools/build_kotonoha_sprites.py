#!/usr/bin/env python3
"""Build Kotonoha's clean-room expression bank and three alternate poses.

The only visual inputs are the two canonical production sprites and the fresh
magenta-backed masters in ``tmp/kotonoha_sprite_build/masters``.  Existing
Kotonoha face or pose assets are never read.  Outputs are staged under ``tmp``;
pass ``--install`` to atomically copy the validated 42 face layers and three
mid-thigh pose sprites into the production directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi

try:
    # Reuse the project's proven generic chroma-key implementation.  No Matsuda
    # art or Matsuda runtime asset is opened by this builder.
    from build_matsuda_fresh_poses import (
        chroma_key,
        clean_final_fringe,
        remove_final_detached_noise,
    )
except ImportError:  # pragma: no cover - module-style invocation from repo root.
    from tools.build_matsuda_fresh_poses import (  # type: ignore[no-redef]
        chroma_key,
        clean_final_fringe,
        remove_final_detached_noise,
    )

try:
    # Keep the builder and production validator on the same semantic definition
    # of Kotonoha's canonical neutral brows, eyes/irises, and mouth.
    from validate_kotonoha_sprites import neutral_feature_footprint
except ImportError:  # pragma: no cover - module-style invocation from repo root.
    from tools.validate_kotonoha_sprites import (  # type: ignore[no-redef]
        neutral_feature_footprint,
    )


CANVAS_SIZE = (1023, 1537)
CANVAS_WIDTH, CANVAS_HEIGHT = CANVAS_SIZE

FACE_TOKENS: tuple[str, ...] = (
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
OUTFITS = ("casual", "work")

CANONICAL_HASHES = {
    "neutral.png": "3cc12dcd7bd018724a7232fe8aeaeF505e312f7117b80f284c1b4719ba6a866b".lower(),
    "work.png": "72bc79cc551f8895ae66e94aacd551f01dfd7d6e74d35c59863132c0841d889c",
}

# Expression registration deliberately uses stable hair geometry, not eyes or
# mouths, so a shifted gaze or extreme expression cannot move the patch.
EXPRESSION_HEAD_ROI = (260, 40, 760, 590)
OUTFIT_HEAD_ROI = (260, 100, 760, 590)
HEAD_REVIEW_CROP = (330, 170, 680, 525)

# The polygon stays inside the facial plane.  A fixed feather is shared by all
# twenty alternates; expanded feature polygons force the neutral
# eyes/brows/mouth fully out of the composite.  Only large connected lavender
# hair regions are painted back after registration, never the similarly colored
# neutral brows or irises.
CASUAL_FACE_POLYGON: tuple[tuple[int, int], ...] = (
    (424, 224),
    (477, 202),
    (535, 204),
    (582, 227),
    (616, 264),
    (632, 307),
    (630, 351),
    (616, 392),
    (590, 428),
    (554, 456),
    (511, 470),
    (469, 464),
    (431, 443),
    (401, 414),
    (380, 378),
    (371, 337),
    (374, 294),
    (391, 255),
)
CASUAL_FEATURE_POLYGONS: tuple[tuple[tuple[int, int], ...], ...] = (
    # Viewer-left eye and brow.
    ((376, 267), (477, 253), (506, 278), (505, 344), (465, 360), (390, 347), (371, 315)),
    # Viewer-right eye and brow.
    ((516, 251), (606, 244), (636, 276), (635, 330), (600, 350), (522, 342), (508, 306)),
    # Nose, mouth, and the surrounding facial plane.
    ((428, 338), (575, 330), (590, 381), (579, 428), (548, 449), (470, 449), (438, 425), (422, 378)),
)
FACE_MASK_SIGMA = 5.75


@dataclass(frozen=True)
class PoseSpec:
    token: str
    outfit: str
    master_name: str
    output_name: str
    canonical_name: str


POSE_SPECS = (
    PoseSpec(
        "exact_fold",
        "work",
        "pose_exact_fold_work.png",
        "pose_exact_fold_work.png",
        "work.png",
    ),
    PoseSpec(
        "watching",
        "casual",
        "pose_watching_casual.png",
        "pose_watching_casual.png",
        "neutral.png",
    ),
    PoseSpec(
        "open_hands",
        "casual",
        "pose_open_hands_casual.png",
        "pose_open_hands_casual.png",
        "neutral.png",
    ),
)


class BuildError(RuntimeError):
    """Raised when an input or output violates the sprite contract."""


@dataclass(frozen=True)
class Registration:
    matrix: np.ndarray
    method: str
    source_keypoints: int
    target_keypoints: int
    good_matches: int
    inliers: int
    rmse: float
    scale: float
    rotation_degrees: float
    translation: tuple[float, float]

    def as_json(self) -> dict[str, Any]:
        return {
            "method": self.method,
            "matrix": rounded_matrix(self.matrix),
            "source_keypoints": self.source_keypoints,
            "target_keypoints": self.target_keypoints,
            "good_matches": self.good_matches,
            "inliers": self.inliers,
            "inlier_rmse_pixels": round(self.rmse, 6),
            "scale": round(self.scale, 9),
            "rotation_degrees": round(self.rotation_degrees, 7),
            "translation_pixels": [
                round(self.translation[0], 7),
                round(self.translation[1], 7),
            ],
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help=(
            "Atomically install validated staged PNGs into "
            "game/assets/characters/kotonoha."
        ),
    )
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rounded_matrix(matrix: np.ndarray) -> list[list[float]]:
    return [[round(float(value), 10) for value in row] for row in matrix]


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


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


def load_rgba(path: Path) -> np.ndarray:
    if not path.is_file() or path.is_symlink():
        raise BuildError(f"Missing or unsafe RGBA input: {path}")
    with Image.open(path) as image:
        if image.mode != "RGBA" or image.size != CANVAS_SIZE:
            raise BuildError(
                f"{path}: expected RGBA {CANVAS_SIZE}, got {image.mode} {image.size}"
            )
        pixels = np.asarray(image, dtype=np.uint8).copy()
    hidden = (pixels[:, :, 3] == 0) & np.any(pixels[:, :, :3] != 0, axis=2)
    if np.any(hidden):
        raise BuildError(f"{path}: {int(hidden.sum())} zero-alpha pixels retain RGB")
    return pixels


def load_rgb(path: Path) -> np.ndarray:
    if not path.is_file() or path.is_symlink():
        raise BuildError(f"Missing or unsafe RGB input: {path}")
    with Image.open(path) as image:
        if image.size != CANVAS_SIZE or image.mode not in {"RGB", "RGBA"}:
            raise BuildError(
                f"{path}: expected RGB/RGBA {CANVAS_SIZE}, got {image.mode} {image.size}"
            )
        return np.asarray(image.convert("RGB"), dtype=np.uint8).copy()


def validate_exact_manifest(directory: Path, expected: set[str]) -> None:
    present = {path.name for path in directory.glob("*.png") if path.is_file()}
    if present != expected:
        raise BuildError(
            f"Fresh master allowlist mismatch in {directory}: "
            f"missing={sorted(expected - present)}, unexpected={sorted(present - expected)}"
        )


def corner_anchor(rgb: np.ndarray) -> np.ndarray:
    samples = np.concatenate(
        (
            rgb[:24, :24].reshape(-1, 3),
            rgb[:24, -24:].reshape(-1, 3),
            rgb[-24:, :24].reshape(-1, 3),
            rgb[-24:, -24:].reshape(-1, 3),
        ),
        axis=0,
    )
    anchor = np.median(samples.astype(np.float32), axis=0)
    # Built-in image edits return a saturated production screen whose hue can
    # vary from red-magenta to true magenta.  Registration uses distance from
    # this measured per-master corner anchor, so require saturation/separation
    # rather than one exact blue-channel value.
    if not (
        anchor[0] >= 175
        and anchor[1] <= 55
        and anchor[2] >= 110
        and min(anchor[0], anchor[2]) - anchor[1] >= 100
    ):
        raise BuildError(f"Master background is not saturated red-magenta: {anchor}")
    return anchor


def foreground_from_magenta(rgb: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    anchor = corner_anchor(rgb)
    delta = rgb.astype(np.float32) - anchor[None, None, :]
    distance = np.sqrt(np.sum(delta * delta, axis=2))
    foreground = distance > 42.0
    fraction = float(np.mean(~foreground))
    if not 0.25 <= fraction <= 0.80:
        raise BuildError(f"Implausible magenta background fraction: {fraction:.5f}")
    return foreground, anchor, fraction


def lavender_hair_mask(rgb: np.ndarray, valid: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    red = rgb[:, :, 0].astype(np.int16)
    green = rgb[:, :, 1].astype(np.int16)
    blue = rgb[:, :, 2].astype(np.int16)
    screen_like = (
        (red >= 180)
        & (blue >= 170)
        & (green <= 100)
        & (np.minimum(red, blue) - green >= 80)
    )
    return (
        valid
        & ~screen_like
        & (hsv[:, :, 0] >= 115)
        & (hsv[:, :, 0] <= 175)
        & (hsv[:, :, 1] >= 16)
        & (hsv[:, :, 1] <= 120)
        & (hsv[:, :, 2] >= 35)
    )


def affine_properties(matrix: np.ndarray) -> tuple[float, float, tuple[float, float]]:
    scale = math.hypot(float(matrix[0, 0]), float(matrix[1, 0]))
    angle = math.degrees(math.atan2(float(matrix[1, 0]), float(matrix[0, 0])))
    return scale, angle, (float(matrix[0, 2]), float(matrix[1, 2]))


def globalize_local_affine(matrix: np.ndarray, origin: tuple[int, int]) -> np.ndarray:
    result = matrix.astype(np.float64).copy()
    offset = np.asarray(origin, dtype=np.float64)
    result[:, 2] += offset - result[:, :2] @ offset
    return result


def compose_affines(second: np.ndarray, first: np.ndarray) -> np.ndarray:
    """Return an affine that applies *first*, then *second*."""

    first_h = np.vstack((first.astype(np.float64), (0.0, 0.0, 1.0)))
    second_h = np.vstack((second.astype(np.float64), (0.0, 0.0, 1.0)))
    return (second_h @ first_h)[:2].astype(np.float64)


def register_hair_geometry(
    source_rgb: np.ndarray,
    source_valid: np.ndarray,
    target_rgba: np.ndarray,
    roi: tuple[int, int, int, int],
) -> Registration:
    x0, y0, x1, y1 = roi
    target_valid = target_rgba[:, :, 3] > 96
    source_mask = (
        lavender_hair_mask(source_rgb, source_valid)[y0:y1, x0:x1].astype(np.uint8)
        * 255
    )
    target_mask = (
        lavender_hair_mask(target_rgba[:, :, :3], target_valid)[y0:y1, x0:x1].astype(np.uint8)
        * 255
    )
    source_gray = cv2.cvtColor(source_rgb, cv2.COLOR_RGB2GRAY)[y0:y1, x0:x1]
    target_gray = cv2.cvtColor(target_rgba[:, :, :3], cv2.COLOR_RGB2GRAY)[y0:y1, x0:x1]

    sift = cv2.SIFT_create(nfeatures=1600, contrastThreshold=0.01, edgeThreshold=15)
    source_points, source_descriptors = sift.detectAndCompute(source_gray, source_mask)
    target_points, target_descriptors = sift.detectAndCompute(target_gray, target_mask)
    if source_descriptors is None or target_descriptors is None:
        raise BuildError("Hair registration produced no SIFT descriptors")

    pairs = cv2.BFMatcher(cv2.NORM_L2).knnMatch(
        source_descriptors, target_descriptors, k=2
    )
    good = [nearest for nearest, runner_up in pairs if nearest.distance < 0.72 * runner_up.distance]
    if len(good) < 24:
        raise BuildError(f"Too few stable lavender-hair matches: {len(good)}")

    source_xy = np.float32([source_points[item.queryIdx].pt for item in good])
    target_xy = np.float32([target_points[item.trainIdx].pt for item in good])
    local, inlier_mask = cv2.estimateAffinePartial2D(
        source_xy,
        target_xy,
        method=cv2.RANSAC,
        ransacReprojThreshold=2.5,
        maxIters=4000,
        confidence=0.999,
        refineIters=30,
    )
    if local is None or inlier_mask is None:
        raise BuildError("Lavender-hair RANSAC registration failed")
    matrix = globalize_local_affine(local, (x0, y0))
    inliers = inlier_mask.ravel().astype(bool)
    predicted = cv2.transform(source_xy[None, :, :], local)[0]
    residual = predicted[inliers] - target_xy[inliers]
    rmse = float(np.sqrt(np.mean(np.sum(residual * residual, axis=1))))
    scale, angle, translation = affine_properties(matrix)
    inlier_count = int(inliers.sum())
    if (
        inlier_count < 24
        or inlier_count / len(good) < 0.52
        or not 0.985 <= scale <= 1.015
        or abs(angle) > 0.75
        or max(abs(translation[0]), abs(translation[1])) > 8.0
        or rmse > 1.75
    ):
        raise BuildError(
            "Implausible hair registration: "
            f"matches={len(good)} inliers={inlier_count} scale={scale:.6f} "
            f"angle={angle:.4f} translation={translation} rmse={rmse:.4f}"
        )
    return Registration(
        matrix=matrix,
        method="lavender_hair_sift_ransac",
        source_keypoints=len(source_points),
        target_keypoints=len(target_points),
        good_matches=len(good),
        inliers=inlier_count,
        rmse=rmse,
        scale=scale,
        rotation_degrees=angle,
        translation=translation,
    )


def warp_rgb(rgb: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    return cv2.warpAffine(
        rgb,
        matrix,
        CANVAS_SIZE,
        # Face registrations are subpixel-scale adjustments. Bilinear
        # resampling stays smooth without Lanczos' high-contrast ringing,
        # which otherwise appears as faint dotted echoes above thin brows.
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0),
    )


def warp_mask(mask: np.ndarray, matrix: np.ndarray, nearest: bool = False) -> np.ndarray:
    return cv2.warpAffine(
        mask.astype(np.uint8),
        matrix,
        CANVAS_SIZE,
        flags=cv2.INTER_NEAREST if nearest else cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )


def keep_largest_component(mask: np.ndarray) -> np.ndarray:
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        (mask > 0).astype(np.uint8), connectivity=8
    )
    if count <= 1:
        return np.zeros_like(mask)
    largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    cleaned = mask.copy()
    cleaned[labels != largest] = 0
    return cleaned


def polygon_mask(polygons: Iterable[Sequence[tuple[int, int]]]) -> np.ndarray:
    result = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH), dtype=np.uint8)
    for points in polygons:
        cv2.fillPoly(result, [np.asarray(points, dtype=np.int32)], 255, lineType=cv2.LINE_8)
    return result


def make_casual_face_mask(base_alpha: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    binary = polygon_mask((CASUAL_FACE_POLYGON,)).astype(np.float32) / 255.0
    feathered = cv2.GaussianBlur(
        binary,
        (0, 0),
        sigmaX=FACE_MASK_SIGMA,
        sigmaY=FACE_MASK_SIGMA,
        borderType=cv2.BORDER_CONSTANT,
    )
    mask = np.clip(np.rint(feathered * 255.0), 0, 255).astype(np.uint8)
    # Give the eye/brow replacement a generous opaque ownership margin.  This
    # prevents a neutral brow from surviving just outside the visible new
    # stroke when an expression raises, lowers, or angles it.
    eye_brow_mandatory = polygon_mask(CASUAL_FEATURE_POLYGONS[:2])
    eye_brow_mandatory = cv2.dilate(
        eye_brow_mandatory,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41)),
        iterations=1,
    )
    lower_face_mandatory = polygon_mask(CASUAL_FEATURE_POLYGONS[2:])
    mandatory = (eye_brow_mandatory > 0) | (lower_face_mandatory > 0)
    opaque = base_alpha == 255
    mask[~opaque] = 0
    mask[mandatory & opaque] = 255
    return keep_largest_component(mask), mandatory


def skin_pixels(rgb: np.ndarray) -> np.ndarray:
    red = rgb[:, :, 0].astype(np.int16)
    green = rgb[:, :, 1].astype(np.int16)
    blue = rgb[:, :, 2].astype(np.int16)
    return (
        (red > 150)
        & (green > 95)
        & (blue > 78)
        & (red * 100 > green * 103)
        & (green * 100 > blue * 96)
    )


def stable_skin_zone() -> np.ndarray:
    zone = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH), dtype=bool)
    zone[334:392, 392:430] = True
    zone[323:385, 585:618] = True
    zone[406:449, 456:558] = True
    zone[348:405, 476:546] = True
    return zone


def color_match_face(
    aligned_rgb: np.ndarray,
    base_rgb: np.ndarray,
    mask: np.ndarray,
) -> tuple[np.ndarray, list[float], int]:
    samples = (
        stable_skin_zone()
        & (mask >= 224)
        & skin_pixels(aligned_rgb)
        & skin_pixels(base_rgb)
    )
    count = int(samples.sum())
    if count < 1500:
        raise BuildError(f"Too few stable face-skin samples: {count}")
    difference = base_rgb.astype(np.int16) - aligned_rgb.astype(np.int16)
    offset = np.clip(np.median(difference[samples], axis=0), -16.0, 16.0)
    corrected = np.clip(
        np.rint(aligned_rgb.astype(np.float32) + offset[None, None, :]), 0, 255
    ).astype(np.uint8)
    return corrected, [float(value) for value in offset], count


def canonical_detail_guard(
    base_rgba: np.ndarray, neutral_features: np.ndarray
) -> np.ndarray:
    """Protect canonical hair and outfit details outside the edited features.

    The source expression plates use Kotonoha's casual turtleneck.  Preserving
    non-skin canonical pixels outside the neutral brows/eyes/mouth footprint
    prevents that collar from bleeding into either runtime outfit while still
    leaving the complete expressive feature area available to the new plate.
    """

    hair = lavender_hair_mask(base_rgba[:, :, :3], base_rgba[:, :, 3] > 96)
    hair = cv2.morphologyEx(
        hair.astype(np.uint8),
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
    )
    # Color alone also selects Kotonoha's lavender eyebrows and irises.  Keep
    # large components to reject isolated noise, then explicitly subtract the
    # semantic neutral-feature footprint below; component size cannot safely
    # distinguish facial ink that touches a bang from the bang itself.
    component_count, labels, stats, _ = cv2.connectedComponentsWithStats(
        hair, connectivity=8
    )
    keep_labels = [
        label
        for label in range(1, component_count)
        if int(stats[label, cv2.CC_STAT_AREA]) >= 1000
    ]
    hair = np.isin(labels, keep_labels).astype(np.uint8)
    hair = cv2.dilate(
        hair,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
        iterations=1,
    ).astype(bool)
    non_skin_detail = (
        (base_rgba[:, :, 3] > 96)
        & ~skin_pixels(base_rgba[:, :, :3])
        & ~neutral_features
    )
    # Expression plates were generated from the casual sprite, whose tall
    # turtleneck otherwise lands inside the work sprite's open polo collar.
    # The actual mouth ends well above this guard; retaining the canonical
    # lower chin/neck also keeps the two outfits' neckline geometry exact.
    lower_chin_and_neck = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH), dtype=bool)
    lower_chin_and_neck[422:510, 400:625] = True
    lower_chin_and_neck &= base_rgba[:, :, 3] > 96
    canonical_face_detail = (hair | non_skin_detail) & ~neutral_features
    return canonical_face_detail | lower_chin_and_neck


def clean_pose_edge_residue(
    image: Image.Image, edge_radius: float = 24.0
) -> tuple[Image.Image, dict[str, int | float]]:
    """Replace generator/key colors at the outer silhouette with local art.

    Chroma decontamination handles translucent antialiasing, but generated
    masters can contain small *opaque* magenta, cyan, or white flecks next to
    fine hair.  Only suspicious colors inside a narrow outer edge band are
    replaced, using the nearest color-safe opaque subject pixel.  Alpha and
    therefore framing/silhouette geometry remain unchanged.
    """

    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    alpha = rgba[:, :, 3]
    visible = alpha > 0
    distance = ndi.distance_transform_edt(visible)
    edge = visible & (distance <= edge_radius)

    rgb_i16 = rgba[:, :, :3].astype(np.int16)
    red, green, blue = (rgb_i16[:, :, channel] for channel in range(3))
    magenta_score = (
        np.minimum(red, blue) - green - 0.18 * np.abs(red - blue)
    )
    hsv = cv2.cvtColor(rgba[:, :, :3], cv2.COLOR_RGB2HSV)
    hue, saturation, value = (hsv[:, :, channel] for channel in range(3))

    # The two irises are the only intentionally saturated magenta-violet
    # details.  Pose normalization registers them to this stable head zone, so
    # opaque key-colored flecks elsewhere can be repaired across the full
    # visible subject (including the centers of large fringe blobs).
    iris_zone = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH), dtype=bool)
    iris_zone[255:355, 395:620] = True
    magenta = visible & ~iris_zone & (magenta_score > 40.0)
    paper_white = edge & (np.minimum(np.minimum(red, green), blue) > 235)
    cyan_green = (
        edge
        & (hue >= 35)
        & (hue <= 105)
        & (saturation > 25)
        & (value > 170)
    )
    suspicious = magenta | paper_white | cyan_green

    safe_solid = (alpha >= 250) & ~suspicious
    if not np.any(safe_solid):
        raise BuildError("Pose has no color-safe opaque pixels for edge cleanup")
    _, safe_indices = ndi.distance_transform_edt(
        ~safe_solid, return_indices=True
    )
    ys, xs = np.nonzero(suspicious)
    rgba[ys, xs, :3] = rgba[
        safe_indices[0, ys, xs], safe_indices[1, ys, xs], :3
    ]
    rgba[alpha == 0, :3] = 0
    return Image.fromarray(rgba, "RGBA"), {
        "edge_radius_pixels": edge_radius,
        "magenta_pixels_replaced": int(magenta.sum()),
        "white_pixels_replaced": int(paper_white.sum()),
        "cyan_green_pixels_replaced": int(cyan_green.sum()),
        "total_pixels_replaced": int(suspicious.sum()),
    }


def make_face_layer(rgb: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    layer = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH, 4), dtype=np.uint8)
    layer[:, :, :3] = rgb
    layer[:, :, 3] = alpha
    layer[alpha == 0, :3] = 0
    return layer


def alpha_composite(base: np.ndarray, layer: np.ndarray) -> np.ndarray:
    return np.asarray(
        Image.alpha_composite(Image.fromarray(base, "RGBA"), Image.fromarray(layer, "RGBA")),
        dtype=np.uint8,
    ).copy()


def bbox(mask: np.ndarray) -> list[int] | None:
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]


def detect_purple_irises(rgb: np.ndarray, valid: np.ndarray) -> list[tuple[float, float]]:
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    yy, xx = np.indices(valid.shape)
    candidate = (
        valid
        & (xx >= 180)
        & (xx < 840)
        & (yy >= 60)
        & (yy < 600)
        & (hsv[:, :, 0] >= 125)
        & (hsv[:, :, 0] <= 175)
        & (hsv[:, :, 1] >= 85)
        & (hsv[:, :, 2] >= 35)
    )
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(
        candidate.astype(np.uint8), connectivity=8
    )
    components: list[tuple[int, float, float]] = []
    for label in range(1, count):
        area = int(stats[label, cv2.CC_STAT_AREA])
        center_x, center_y = (float(value) for value in centroids[label])
        if 150 <= area <= 1800 and 300 <= center_x <= 700 and 100 <= center_y <= 390:
            components.append((area, center_x, center_y))

    best: tuple[float, tuple[int, float, float], tuple[int, float, float]] | None = None
    for index, left in enumerate(components):
        for right in components[index + 1 :]:
            first, second = sorted((left, right), key=lambda item: item[1])
            separation = second[1] - first[1]
            vertical = abs(second[2] - first[2])
            area_ratio = min(first[0], second[0]) / max(first[0], second[0])
            if not (50 <= separation <= 180 and vertical <= 35 and area_ratio >= 0.38):
                continue
            score = first[0] + second[0] - vertical * 10.0 - abs(separation - 112.0)
            if best is None or score > best[0]:
                best = (score, first, second)
    if best is None:
        raise BuildError(f"Could not identify both purple irises; candidates={components}")
    return [(best[1][1], best[1][2]), (best[2][1], best[2][2])]


def similarity_from_pairs(
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


def warp_rgba_premultiplied(rgba: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    source = rgba.astype(np.float32) / 255.0
    alpha = source[:, :, 3:4]
    premultiplied = np.concatenate((source[:, :, :3] * alpha, alpha), axis=2)
    warped = cv2.warpAffine(
        premultiplied,
        matrix,
        CANVAS_SIZE,
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0, 0),
    )
    warped_alpha = np.clip(warped[:, :, 3:4], 0.0, 1.0)
    straight = np.zeros_like(warped)
    straight[:, :, 3:4] = warped_alpha
    np.divide(
        warped[:, :, :3],
        warped_alpha,
        out=straight[:, :, :3],
        where=warped_alpha > 1e-6,
    )
    result = np.clip(np.rint(straight * 255.0), 0, 255).astype(np.uint8)
    result[result[:, :, 3] == 0, :3] = 0
    return result


def checkerboard(size: tuple[int, int], tile: int = 20) -> Image.Image:
    width, height = size
    yy, xx = np.indices((height, width))
    cells = ((xx // tile) + (yy // tile)) % 2
    light = np.asarray((230, 232, 238), dtype=np.uint8)
    dark = np.asarray((169, 175, 188), dtype=np.uint8)
    return Image.fromarray(np.where(cells[:, :, None] == 0, light, dark), "RGB").convert("RGBA")


def review_background(kind: str, size: tuple[int, int]) -> tuple[Image.Image, tuple[int, int, int, int]]:
    colors = {
        "light": ((246, 246, 248, 255), (25, 25, 30, 255)),
        "dark": ((18, 20, 27, 255), (242, 243, 247, 255)),
        "gray": ((112, 116, 126, 255), (255, 255, 255, 255)),
        "green": ((20, 150, 90, 255), (255, 255, 255, 255)),
    }
    if kind == "checker":
        return checkerboard(size), (20, 22, 28, 255)
    background, text = colors[kind]
    return Image.new("RGBA", size, background), text


def contact_sheet(
    entries: Sequence[tuple[str, Image.Image]],
    kind: str,
    *,
    columns: int,
    content_size: tuple[int, int],
    crop: tuple[int, int, int, int] | None = None,
    nearest: bool = False,
) -> Image.Image:
    cell_width, cell_height = content_size
    label_height = 28
    gutter = 8
    rows = math.ceil(len(entries) / columns)
    size = (
        columns * cell_width + (columns + 1) * gutter,
        rows * (cell_height + label_height) + (rows + 1) * gutter,
    )
    sheet, text_color = review_background(kind, size)
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.load_default(size=14)
    except TypeError:
        font = ImageFont.load_default()
    resample = Image.Resampling.NEAREST if nearest else Image.Resampling.LANCZOS

    for index, (label, image) in enumerate(entries):
        row, column = divmod(index, columns)
        cell_x = gutter + column * (cell_width + gutter)
        cell_y = gutter + row * (cell_height + label_height)
        content = image.crop(crop) if crop is not None else image.copy()
        content.thumbnail((cell_width, cell_height), resample)
        x = cell_x + (cell_width - content.width) // 2
        y = cell_y + cell_height - content.height
        sheet.alpha_composite(content, (x, y))
        bounds = draw.textbbox((0, 0), label, font=font)
        draw.text(
            (cell_x + (cell_width - (bounds[2] - bounds[0])) // 2, cell_y + cell_height + 5),
            label,
            font=font,
            fill=text_color,
        )
    return sheet.convert("RGB")


def install_outputs(
    staged: Iterable[Path], production_dir: Path, expected_names: set[str]
) -> None:
    production_dir.mkdir(parents=True, exist_ok=True)
    unexpected = {
        path.name
        for pattern in ("face_*.png", "pose_*.png")
        for path in production_dir.glob(pattern)
        if path.name not in expected_names
    }
    if unexpected:
        raise BuildError(
            "Refusing to mix undeclared Kotonoha runtime assets into production: "
            + ", ".join(sorted(unexpected))
        )
    for source in staged:
        destination = production_dir / source.name
        temporary = destination.with_name(f".{destination.name}.installing")
        shutil.copyfile(source, temporary)
        os.replace(temporary, destination)


def build(root: Path, install: bool) -> dict[str, Any]:
    root = root.resolve()
    production_dir = root / "game" / "assets" / "characters" / "kotonoha"
    build_dir = root / "tmp" / "kotonoha_sprite_build"
    masters_dir = build_dir / "masters"
    faces_dir = build_dir / "faces"
    poses_dir = build_dir / "poses"
    review_dir = build_dir / "review"

    base_paths = {
        "casual": production_dir / "neutral.png",
        "work": production_dir / "work.png",
    }
    for path in base_paths.values():
        expected_hash = CANONICAL_HASHES[path.name]
        actual_hash = sha256_file(path)
        if actual_hash != expected_hash:
            raise BuildError(
                f"Canonical base hash changed for {path.name}: {actual_hash} != {expected_hash}"
            )
    bases = {outfit: load_rgba(path) for outfit, path in base_paths.items()}

    expected_master_names = {
        *(f"expression_{token}.png" for token in ALTERNATE_TOKENS),
        *(spec.master_name for spec in POSE_SPECS),
    }
    validate_exact_manifest(masters_dir, expected_master_names)

    # Register canonical casual geometry to the work head once.  Expression
    # masters are registered to casual, then composed through this transform.
    casual_to_work = register_hair_geometry(
        bases["casual"][:, :, :3],
        bases["casual"][:, :, 3] > 96,
        bases["work"],
        OUTFIT_HEAD_ROI,
    )

    casual_mask, casual_mandatory = make_casual_face_mask(bases["casual"][:, :, 3])
    work_mask = warp_mask(casual_mask, casual_to_work.matrix)
    work_mask[bases["work"][:, :, 3] != 255] = 0
    work_mask = keep_largest_component(work_mask)
    work_mandatory = warp_mask(
        casual_mandatory.astype(np.uint8) * 255,
        casual_to_work.matrix,
        nearest=True,
    ) > 0
    work_mask[work_mandatory & (bases["work"][:, :, 3] == 255)] = 255
    masks = {"casual": casual_mask, "work": work_mask}
    mandatory = {"casual": casual_mandatory, "work": work_mandatory}
    neutral_features = {
        outfit: neutral_feature_footprint(base) for outfit, base in bases.items()
    }
    detail_guards = {
        outfit: canonical_detail_guard(base, neutral_features[outfit])
        for outfit, base in bases.items()
    }

    for outfit in OUTFITS:
        mask = masks[outfit]
        if bbox(mask > 0) is None or np.any(mask[[0, -1], :]) or np.any(mask[:, [0, -1]]):
            raise BuildError(f"{outfit} face mask is empty or touches the canvas edge")
        if len(np.unique(mask)) < 96:
            raise BuildError(f"{outfit} face mask has insufficient feather levels")
        uncovered = mandatory[outfit] & (bases[outfit][:, :, 3] == 255) & (mask != 255)
        if np.any(uncovered):
            raise BuildError(
                f"{outfit} mask leaves {int(uncovered.sum())} mandatory pixels translucent"
            )
        guarded_features = detail_guards[outfit] & neutral_features[outfit]
        if np.any(guarded_features):
            raise BuildError(
                f"{outfit} canonical detail guard restores "
                f"{int(guarded_features.sum())} expression-owned feature pixels"
            )

    faces_dir.mkdir(parents=True, exist_ok=True)
    expression_records: dict[str, Any] = {}
    layers: dict[tuple[str, str], np.ndarray] = {}
    transparent = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH, 4), dtype=np.uint8)
    for outfit in OUTFITS:
        layers[("neut", outfit)] = transparent.copy()

    for token in ALTERNATE_TOKENS:
        master_path = masters_dir / f"expression_{token}.png"
        master_rgb = load_rgb(master_path)
        foreground, anchor, background_fraction = foreground_from_magenta(master_rgb)
        registration = register_hair_geometry(
            master_rgb,
            foreground,
            bases["casual"],
            EXPRESSION_HEAD_ROI,
        )
        matrices = {
            "casual": registration.matrix,
            "work": compose_affines(casual_to_work.matrix, registration.matrix),
        }
        outfit_records: dict[str, Any] = {}
        for outfit in OUTFITS:
            aligned = warp_rgb(master_rgb, matrices[outfit])
            corrected, offset, sample_count = color_match_face(
                aligned, bases[outfit][:, :, :3], masks[outfit]
            )
            # Chroma can only enter through a malformed/shifted face master.
            red = corrected[:, :, 0].astype(np.int16)
            green = corrected[:, :, 1].astype(np.int16)
            blue = corrected[:, :, 2].astype(np.int16)
            magenta = (
                (masks[outfit] > 0)
                & (red >= 180)
                & (blue >= 160)
                & (green <= 100)
                & (np.minimum(red, blue) - green >= 90)
            )
            corrected[magenta] = bases[outfit][:, :, :3][magenta]
            guard = detail_guards[outfit] & (masks[outfit] > 0)
            corrected[guard] = bases[outfit][:, :, :3][guard]
            layer = make_face_layer(corrected, masks[outfit])
            layers[(token, outfit)] = layer
            outfit_records[outfit] = {
                "matrix_master_to_outfit": rounded_matrix(matrices[outfit]),
                "skin_offset_rgb": offset,
                "skin_samples": sample_count,
                "magenta_pixels_repaired": int(magenta.sum()),
                "canonical_detail_pixels_preserved": int(guard.sum()),
            }
        expression_records[token] = {
            "master": relative(master_path, root),
            "master_sha256": sha256_file(master_path),
            "background_anchor_rgb": [round(float(value), 4) for value in anchor],
            "background_fraction": round(background_fraction, 7),
            "registration_to_casual": registration.as_json(),
            "outfits": outfit_records,
        }

    expected_face_names = {
        f"face_{token}_{outfit}.png" for token in FACE_TOKENS for outfit in OUTFITS
    }
    face_paths: list[Path] = []
    face_records: dict[str, Any] = {}
    composites: list[tuple[str, Image.Image]] = []
    for outfit in OUTFITS:
        signatures: dict[str, str] = {}
        for token in FACE_TOKENS:
            name = f"face_{token}_{outfit}.png"
            path = faces_dir / name
            layer = layers[(token, outfit)]
            alpha = layer[:, :, 3]
            expected_alpha = np.zeros_like(alpha) if token == "neut" else masks[outfit]
            if not np.array_equal(alpha, expected_alpha):
                raise BuildError(f"{name}: alpha differs from fixed {outfit} mask")
            if np.any((alpha == 0) & np.any(layer[:, :, :3] != 0, axis=2)):
                raise BuildError(f"{name}: hidden RGB remained under zero alpha")
            composite = alpha_composite(bases[outfit], layer)
            if not np.array_equal(composite[:, :, 3], bases[outfit][:, :, 3]):
                raise BuildError(f"{name}: composite changes the canonical silhouette")
            signature = hashlib.sha256(composite.tobytes()).hexdigest()
            if signature in signatures:
                raise BuildError(
                    f"{outfit}/{token} duplicates composite {signatures[signature]}"
                )
            signatures[signature] = token
            atomic_save_png(Image.fromarray(layer, "RGBA"), path)
            face_paths.append(path)
            composites.append((f"{outfit}/{token}", Image.fromarray(composite, "RGBA")))
            face_records[name] = {
                "sha256": sha256_file(path),
                "alpha_bbox": bbox(alpha > 0),
                "visible_pixels": int((alpha > 0).sum()),
                "partial_alpha_pixels": int(((alpha > 0) & (alpha < 255)).sum()),
            }
    actual_face_names = {path.name for path in faces_dir.glob("*.png")}
    if actual_face_names != expected_face_names:
        raise BuildError(
            f"Face output mismatch: missing={sorted(expected_face_names - actual_face_names)}, "
            f"unexpected={sorted(actual_face_names - expected_face_names)}"
        )

    poses_dir.mkdir(parents=True, exist_ok=True)
    pose_paths: list[Path] = []
    pose_entries: list[tuple[str, Image.Image]] = []
    pose_records: dict[str, Any] = {}
    for spec in POSE_SPECS:
        master_path = masters_dir / spec.master_name
        with Image.open(master_path) as opened:
            master_image = opened.convert("RGB")
        keyed_image, key_diagnostics = chroma_key(master_image)
        keyed = np.asarray(keyed_image, dtype=np.uint8).copy()
        source_eyes = detect_purple_irises(keyed[:, :, :3], keyed[:, :, 3] > 96)
        canonical = bases[spec.outfit]
        target_eyes = detect_purple_irises(
            canonical[:, :, :3], canonical[:, :, 3] > 96
        )
        matrix = similarity_from_pairs(source_eyes, target_eyes)
        scale, angle, translation = affine_properties(matrix)
        if not 0.88 <= scale <= 1.85 or abs(angle) > 5.0:
            raise BuildError(
                f"{spec.token}: implausible iris registration scale={scale:.5f}, angle={angle:.4f}"
            )
        normalized = warp_rgba_premultiplied(keyed, matrix)
        normalized_image = Image.fromarray(normalized, "RGBA")
        normalized_image, fringe_metrics = clean_final_fringe(normalized_image)
        normalized_image, edge_cleanup_metrics = clean_pose_edge_residue(
            normalized_image
        )
        normalized_image, component_metrics = remove_final_detached_noise(
            normalized_image, minimum_component_pixels=32
        )
        normalized = np.asarray(normalized_image, dtype=np.uint8).copy()
        normalized[normalized[:, :, 3] == 0, :3] = 0
        alpha = normalized[:, :, 3]
        bounds = bbox(alpha > 0)
        if bounds is None:
            raise BuildError(f"{spec.token}: normalized pose is empty")
        left, top, right, bottom = bounds
        if left <= 0 or top <= 0 or right >= CANVAS_WIDTH:
            raise BuildError(f"{spec.token}: unsafe top/side contact: {bounds}")
        if bottom != CANVAS_HEIGHT:
            raise BuildError(
                f"{spec.token}: expected mid-thigh stage-baseline crop at {CANVAS_HEIGHT}, got {bounds}"
            )
        if np.any((alpha == 0) & np.any(normalized[:, :, :3] != 0, axis=2)):
            raise BuildError(f"{spec.token}: hidden RGB remained after pose normalization")
        output_path = poses_dir / spec.output_name
        atomic_save_png(Image.fromarray(normalized, "RGBA"), output_path)
        pose_paths.append(output_path)
        pose_entries.append((f"{spec.outfit}/{spec.token}", Image.fromarray(normalized, "RGBA")))
        pose_records[spec.output_name] = {
            "master": relative(master_path, root),
            "master_sha256": sha256_file(master_path),
            "output_sha256": sha256_file(output_path),
            "outfit": spec.outfit,
            "source_iris_centers": [[round(x, 5), round(y, 5)] for x, y in source_eyes],
            "target_iris_centers": [[round(x, 5), round(y, 5)] for x, y in target_eyes],
            "matrix": rounded_matrix(matrix),
            "scale": round(scale, 8),
            "rotation_degrees": round(angle, 6),
            "translation_pixels": [round(translation[0], 6), round(translation[1], 6)],
            "alpha_bbox": bounds,
            "visible_pixels": int((alpha > 0).sum()),
            "bottom_contact_pixels": int(np.count_nonzero(alpha[-1, :])),
            "chroma_key": key_diagnostics,
            "fringe_cleanup": fringe_metrics,
            "edge_residue_cleanup": edge_cleanup_metrics,
            "component_cleanup": component_metrics,
        }

    expected_pose_names = {spec.output_name for spec in POSE_SPECS}
    actual_pose_names = {path.name for path in poses_dir.glob("*.png")}
    if actual_pose_names != expected_pose_names:
        raise BuildError(
            f"Pose output mismatch: missing={sorted(expected_pose_names - actual_pose_names)}, "
            f"unexpected={sorted(actual_pose_names - expected_pose_names)}"
        )

    review_dir.mkdir(parents=True, exist_ok=True)
    head_crop_dir = review_dir / "head_crops"
    head_crop_dir.mkdir(parents=True, exist_ok=True)
    for label, composite in composites:
        outfit, token = label.split("/", 1)
        atomic_save_png(
            composite.crop(HEAD_REVIEW_CROP),
            head_crop_dir / f"{outfit}_{token}.png",
        )
    raw_head_crop_dir = review_dir / "raw_head_crops"
    raw_head_crop_dir.mkdir(parents=True, exist_ok=True)
    for token in ALTERNATE_TOKENS:
        with Image.open(masters_dir / f"expression_{token}.png") as master:
            atomic_save_png(
                master.convert("RGB").crop(HEAD_REVIEW_CROP),
                raw_head_crop_dir / f"{token}.png",
            )
    review_hashes: dict[str, str] = {}
    for kind in ("light", "dark", "gray", "green", "checker"):
        full_path = review_dir / f"expressions_{kind}.png"
        heads_path = review_dir / f"heads_{kind}.png"
        poses_path = review_dir / f"poses_{kind}.png"
        atomic_save_png(
            contact_sheet(
                composites,
                kind,
                columns=7,
                content_size=(170, 260),
            ),
            full_path,
        )
        atomic_save_png(
            contact_sheet(
                composites,
                kind,
                columns=6,
                content_size=(300, 300),
                crop=HEAD_REVIEW_CROP,
                nearest=True,
            ),
            heads_path,
        )
        atomic_save_png(
            contact_sheet(
                pose_entries,
                kind,
                columns=3,
                content_size=(330, 500),
            ),
            poses_path,
        )
        for path in (full_path, heads_path, poses_path):
            review_hashes[path.name] = sha256_file(path)

    staged_paths = [*face_paths, *pose_paths]
    expected_runtime_names = expected_face_names | expected_pose_names
    if install:
        install_outputs(staged_paths, production_dir, expected_runtime_names)

    payload: dict[str, Any] = {
        "schema_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "builder": relative(Path(__file__), root),
        "builder_sha256": sha256_file(Path(__file__)),
        "canvas": list(CANVAS_SIZE),
        "policy": {
            "clean_room": True,
            "canonical_sources_only": [relative(path, root) for path in base_paths.values()],
            "legacy_kotonoha_art_opened": False,
            "existing_face_or_pose_assets_opened": False,
            "mid_thigh_pose_framing": True,
            "installed": install,
        },
        "canonical_inputs": {
            outfit: {
                "path": relative(path, root),
                "sha256": sha256_file(path),
                "alpha_bbox": bbox(bases[outfit][:, :, 3] > 0),
            }
            for outfit, path in base_paths.items()
        },
        "outfit_registration": casual_to_work.as_json(),
        "face_masks": {
            outfit: {
                "alpha_bbox": bbox(mask > 0),
                "visible_pixels": int((mask > 0).sum()),
                "opaque_pixels": int((mask == 255).sum()),
                "partial_alpha_pixels": int(((mask > 0) & (mask < 255)).sum()),
                "unique_alpha_levels": int(len(np.unique(mask))),
            }
            for outfit, mask in masks.items()
        },
        "expressions": expression_records,
        "face_outputs": face_records,
        "poses": pose_records,
        "reviews": {
            "directory": relative(review_dir, root),
            "sha256": review_hashes,
        },
        "installed_runtime_names": sorted(expected_runtime_names) if install else [],
    }
    atomic_save_json(payload, build_dir / "build_metrics.json")
    return payload


def main() -> int:
    args = parse_args()
    try:
        payload = build(args.project_root, args.install)
    except (BuildError, OSError, ValueError, cv2.error) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        "Built 42 Kotonoha face layers and 3 mid-thigh poses"
        + ("; installed production assets." if args.install else "; staging only.")
    )
    print(f"Review sheets: {payload['reviews']['directory']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
