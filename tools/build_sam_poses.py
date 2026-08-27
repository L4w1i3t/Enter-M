#!/usr/bin/env python3
"""Extract and stage-register Sam's fresh green-screen pose masters.

The generated source uses a saturated chroma-green matte that is absent from
Sam's palette.  Alpha comes from the largest non-green silhouette, while every
boundary RGB value comes from the nearest verified non-green interior pixel.
This yields clean straight-alpha PNGs without green spill or hidden matte RGB.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CANVAS_SIZE = (1023, 1537)
DEFAULT_INPUT_DIR = PROJECT_ROOT / "tmp" / "sam_rebuild_fresh" / "pose_masters_green"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "tmp" / "sam_rebuild_fresh" / "staged"
POSE_OUTFITS = {
    "pose_open_hand_casual": "casual",
    "pose_crossed_uniform": "uniform",
    "pose_thinking_uniform": "uniform",
    "pose_phone_casual": "casual",
}
LOWER_BODY_TARGET_X = {"casual": 372.5, "uniform": 380.0}
STAGE_TOP = 31


def largest_component(mask: np.ndarray) -> np.ndarray:
    component_count, labels, statistics, _ = cv2.connectedComponentsWithStats(
        mask.astype(np.uint8), connectivity=8
    )
    if component_count <= 1:
        raise ValueError("no connected foreground silhouette found")
    largest_label = 1 + int(np.argmax(statistics[1:, cv2.CC_STAT_AREA]))
    return labels == largest_label


def load_rgb(path: Path) -> np.ndarray:
    image = np.asarray(Image.open(path).convert("RGB"))
    if (image.shape[1], image.shape[0]) != CANVAS_SIZE:
        raise ValueError(f"{path}: expected {CANVAS_SIZE}, found {image.shape[1::-1]}")
    return image


def chroma_key(master_path: Path) -> np.ndarray:
    """Return clean straight-alpha RGBA from one green-screen source."""

    image = load_rgb(master_path)
    red, green, blue = [image[:, :, channel].astype(np.int16) for channel in range(3)]
    green_score = np.minimum(green - red, green - blue)
    dominant_green = (green > 145) & ((green - red) > 45) & ((green - blue) > 45)
    # Generated antialiasing can mix the matte into blond hair while leaving
    # red a few levels above green, so plain green dominance misses lime/white
    # wedges.  Include those colors only when they belong to the large
    # canvas-connected background field; similar highlights enclosed inside
    # the subject are not promoted to background.
    lime_mixture = (green > 80) & ((green - red) > -10) & ((green - blue) > 20)
    # Alpha geometry comes only from definite chroma green.  Pale skin, blond
    # highlights, and the off-white shirt can resemble a lime mixture, so they
    # must never participate in a connected flood or the silhouette develops
    # polygonal bites.  Lime detection below can soften boundary coverage and
    # reject unsafe RGB, but it never changes the connected subject geometry.
    foreground = largest_component(~dominant_green)
    foreground = cv2.morphologyEx(
        foreground.astype(np.uint8),
        cv2.MORPH_CLOSE,
        np.ones((3, 3), dtype=np.uint8),
    ).astype(bool)

    inside_distance = cv2.distanceTransform(foreground.astype(np.uint8), cv2.DIST_L2, 5)
    outside_distance = cv2.distanceTransform(
        (~foreground).astype(np.uint8), cv2.DIST_L2, 5
    )
    signed_distance = inside_distance - outside_distance
    alpha = np.rint(np.clip(0.5 + signed_distance / 3.0, 0.0, 1.0) * 255.0).astype(
        np.uint8
    )

    # A generated green matte can mix into pale blond/skin edge pixels without
    # remaining green-dominant.  Fade only those boundary mixtures according
    # to their distance from definite matte; never flood through connected
    # face, neck, hair, or clothing geometry.
    lime_coverage = np.clip((inside_distance - 0.5) / 4.0, 0.0, 1.0)
    alpha_float = alpha.astype(np.float32) / 255.0
    alpha_float[lime_mixture] *= lime_coverage[lime_mixture]
    alpha = np.rint(alpha_float * 255.0).astype(np.uint8)

    # Source colors at the matte transition are necessarily green mixtures.
    # Pull all boundary RGB from a spatially safe, non-green interior and only
    # restore original pixels where both opacity and chroma prove them clean.
    trusted_color = (inside_distance >= 8.0) & (green_score < 10) & ~lime_mixture
    if not np.any(trusted_color):
        raise ValueError(f"{master_path}: no clean interior colors found")
    _, nearest = ndimage.distance_transform_edt(~trusted_color, return_indices=True)
    foreground_rgb = image[nearest[0], nearest[1]].copy()
    safe_opaque = (alpha == 255) & (green_score < 8) & ~lime_mixture
    foreground_rgb[safe_opaque] = image[safe_opaque]
    foreground_rgb[alpha == 0] = 0

    return np.dstack((foreground_rgb, alpha))


def alpha_bounds(alpha: np.ndarray) -> tuple[int, int, int, int]:
    y_values, x_values = np.nonzero(alpha >= 8)
    if not len(x_values):
        raise ValueError("pose is fully transparent")
    return (
        int(x_values.min()),
        int(y_values.min()),
        int(x_values.max()) + 1,
        int(y_values.max()) + 1,
    )


def lower_body_anchor(alpha: np.ndarray, bounds: tuple[int, int, int, int]) -> float:
    left, top, right, bottom = bounds
    start_y = max(top, bottom - max(24, round((bottom - top) * 0.12)))
    row_centers: list[float] = []
    for row in alpha[start_y:bottom] >= 128:
        x_values = np.flatnonzero(row)
        if len(x_values):
            row_centers.append(float(x_values[0] + x_values[-1]) / 2.0)
    if not row_centers:
        return float(left + right) / 2.0
    return float(np.median(row_centers))


def stage_register(
    rgba: np.ndarray, outfit: str
) -> tuple[np.ndarray, float, float, float]:
    alpha = rgba[..., 3]
    bounds = alpha_bounds(alpha)
    source_height = bounds[3] - bounds[1]
    scale = (CANVAS_SIZE[1] - STAGE_TOP) / float(source_height)
    source_anchor_x = lower_body_anchor(alpha, bounds)
    translate_x = LOWER_BODY_TARGET_X[outfit] - scale * source_anchor_x
    translate_y = STAGE_TOP - scale * bounds[1]
    matrix = np.array(
        ((scale, 0.0, translate_x), (0.0, scale, translate_y)), dtype=np.float32
    )

    alpha_float = rgba[..., 3].astype(np.float32) / 255.0
    premultiplied = rgba[..., :3].astype(np.float32) * alpha_float[..., None]
    warped_alpha = cv2.warpAffine(
        alpha_float,
        matrix,
        CANVAS_SIZE,
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )
    warped_alpha = np.clip(warped_alpha, 0.0, 1.0)
    warped_premultiplied = cv2.warpAffine(
        premultiplied,
        matrix,
        CANVAS_SIZE,
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )
    warped_rgb = np.zeros_like(warped_premultiplied)
    visible = warped_alpha > 1.0 / 255.0
    warped_rgb[visible] = np.clip(
        warped_premultiplied[visible] / warped_alpha[visible, None], 0.0, 255.0
    )
    output = np.rint(np.dstack((warped_rgb, warped_alpha * 255.0))).astype(np.uint8)
    # PNG RGB values are semantically undefined under alpha zero.  Keeping them
    # explicitly zero makes later QA deterministic and prevents stale colors
    # from surfacing in tools that mishandle unassociated alpha.
    output[..., :3][output[..., 3] == 0] = 0
    return output, scale, translate_x, translate_y


def save_review_strip(rgba: np.ndarray, destination: Path) -> None:
    """Save full-resolution black/white/checker composites for edge QA."""

    height, width = rgba.shape[:2]
    alpha = rgba[..., 3:4].astype(np.float32) / 255.0
    foreground = rgba[..., :3].astype(np.float32)
    black = np.zeros((height, width, 3), dtype=np.uint8)
    white = np.full((height, width, 3), 255, dtype=np.uint8)
    y_grid, x_grid = np.indices((height, width))
    checker_value = np.where(((x_grid // 32) + (y_grid // 32)) % 2, 192, 224)
    checker = np.repeat(checker_value[..., None], 3, axis=2).astype(np.uint8)

    panels = []
    for background in (black, white, checker):
        composite = foreground * alpha + background.astype(np.float32) * (1.0 - alpha)
        panels.append(np.rint(composite).astype(np.uint8))
    destination.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.concatenate(panels, axis=1), "RGB").save(
        destination, optimize=True
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--review-dir",
        type=Path,
        help="optional directory for full-resolution black/white/checker strips",
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_args()
    arguments.output_dir.mkdir(parents=True, exist_ok=True)
    for pose_name, outfit in POSE_OUTFITS.items():
        source = arguments.input_dir / f"{pose_name}.png"
        if not source.is_file():
            raise SystemExit(f"Missing green-screen pose master: {source}")
        extracted = chroma_key(source)
        registered, scale, translate_x, translate_y = stage_register(extracted, outfit)
        destination = arguments.output_dir / source.name
        Image.fromarray(registered, "RGBA").save(destination, optimize=True)
        if arguments.review_dir is not None:
            save_review_strip(
                registered, arguments.review_dir / f"{pose_name}_review.png"
            )
        bounds = alpha_bounds(registered[..., 3])
        print(
            f"{destination}: bbox={bounds} scale={scale:.5f} "
            f"translate=({translate_x:.2f}, {translate_y:.2f})"
        )


if __name__ == "__main__":
    main()
