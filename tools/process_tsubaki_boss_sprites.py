#!/usr/bin/env python3
"""Normalize generated Tsubaki-mode boss sprites for Ren'Py.

The image generator's cleanup pass supplies opaque monochrome art on black.
This tool makes that matte exactly black, converts all artwork to a four-tone
pixel palette, tightly registers every pose on one small battle-sprite cell,
and writes a manifest used to audit registration. The live fight turns the
grayscale luminance into alpha, matching its original Undertale-style render.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_DIR = PROJECT_ROOT / "docs" / "archive" / "tsubaki-boss"
DEFAULT_OUTPUT_DIR = (
    PROJECT_ROOT
    / "game"
    / "addons"
    / "Matsuda's Sick Boss Fight"
    / "tsubakimode"
)

CANVAS_WIDTH = 184
CANVAS_HEIGHT = 344
BASELINE_Y = 334
TARGET_LOWER_ANCHOR_X = 92.0
OUTPUT_SCALE = 0.25
MATTE_CUTOFF = 22
CONTENT_CUTOFF = 42
PIXEL_LEVELS = (0, 96, 176, 255)

SPRITES = (
    ("phase1_black_master.png", "phase1.png"),
    ("phase1_strained_black_master.png", "phase1_strained.png"),
    ("phase2_black_master.png", "phase2.png"),
    ("phase2_exhausted_black_master.png", "phase2_exhausted.png"),
    ("phase2_limp_black_master.png", "phase2_limp.png"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--metadata",
        type=Path,
        default=DEFAULT_INPUT_DIR / "processed_manifest.json",
    )
    return parser.parse_args()


def mask_bbox(mask: np.ndarray) -> tuple[int, int, int, int]:
    rows, columns = np.where(mask)
    if not len(rows):
        raise ValueError("sprite cleanup produced an empty image")
    return (
        int(columns.min()),
        int(rows.min()),
        int(columns.max()) + 1,
        int(rows.max()) + 1,
    )


def manifest_path(path: Path) -> str:
    """Prefer stable project-relative paths in the checked-in audit."""
    resolved = path.resolve()
    try:
        return resolved.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return str(resolved)


def lower_body_anchor_x(mask: np.ndarray, bbox: tuple[int, int, int, int]) -> float:
    _, top, _, bottom = bbox
    lower_top = top + int((bottom - top) * 0.72)
    row_grid = np.indices(mask.shape)[0]
    _, columns = np.where(mask & (row_grid >= lower_top))
    if not len(columns):
        return (bbox[0] + bbox[2]) * 0.5
    return float(np.median(columns))


def normalize_master(source: Path) -> tuple[np.ndarray, np.ndarray]:
    with Image.open(source) as image:
        rgb = np.asarray(image.convert("RGB"), dtype=np.uint8)
    # The fight is intentionally achromatic. Collapsing generator channel
    # noise before thresholding prevents colored fringes around rotated art.
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    gray[gray < MATTE_CUTOFF] = 0
    gray[gray > 248] = 255

    # Reject isolated low-energy background flecks while retaining every
    # substantial white fill, ink highlight, hair strand, and feather detail.
    content = gray >= CONTENT_CUTOFF
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        content.astype(np.uint8), connectivity=8
    )
    if count <= 1:
        raise ValueError(f"{source}: no visible sprite content")
    areas = stats[1:, cv2.CC_STAT_AREA]
    largest_label = int(np.argmax(areas)) + 1
    main = labels == largest_label
    distance_from_main = cv2.distanceTransform(
        (~main).astype(np.uint8), cv2.DIST_L2, 5
    )
    retained = main.copy()
    for label in range(1, count):
        if label == largest_label:
            continue
        component = labels == label
        area = int(stats[label, cv2.CC_STAT_AREA])
        separation = float(distance_from_main[component].min())
        if area >= 48 or (area >= 5 and separation <= 72.0):
            retained |= component

    # Keep antialias/shading immediately around retained ink, and force every
    # other background pixel to mathematically exact black.
    support = cv2.dilate(
        retained.astype(np.uint8), np.ones((5, 5), dtype=np.uint8), iterations=1
    ).astype(bool)
    gray[~support] = 0
    return np.dstack((gray, gray, gray)), retained


def place_on_canvas(
    rgb: np.ndarray,
    translate_x: float,
    translate_y: float,
) -> np.ndarray:
    matrix = np.asarray(
        [
            [OUTPUT_SCALE, 0.0, translate_x],
            [0.0, OUTPUT_SCALE, translate_y],
        ],
        dtype=np.float32,
    )
    placed = cv2.warpAffine(
        rgb,
        matrix,
        (CANVAS_WIDTH, CANVAS_HEIGHT),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0),
    )
    gray = cv2.cvtColor(placed, cv2.COLOR_RGB2GRAY)
    quantized = np.zeros_like(gray)
    quantized[gray >= 34] = PIXEL_LEVELS[1]
    quantized[gray >= 120] = PIXEL_LEVELS[2]
    quantized[gray >= 218] = PIXEL_LEVELS[3]
    return np.dstack((quantized, quantized, quantized))


def process_one(source: Path, destination: Path) -> dict[str, object]:
    rgb, foreground = normalize_master(source)
    source_bbox = mask_bbox(foreground)
    source_anchor_x = lower_body_anchor_x(foreground, source_bbox)
    translate_x = TARGET_LOWER_ANCHOR_X - OUTPUT_SCALE * source_anchor_x
    translate_y = BASELINE_Y - OUTPUT_SCALE * source_bbox[3]
    placed = place_on_canvas(rgb, translate_x, translate_y)
    visible = cv2.cvtColor(placed, cv2.COLOR_RGB2GRAY) >= CONTENT_CUTOFF
    output_bbox = mask_bbox(visible)

    # Interpolation can grow a thresholded edge by one pixel after scaling.
    # Snap the final visible bottom, not merely the source-space estimate, so
    # every pose swaps on exactly the same foot line.
    baseline_adjust_y = BASELINE_Y - output_bbox[3]
    if baseline_adjust_y:
        placed = np.roll(placed, baseline_adjust_y, axis=0)
        if baseline_adjust_y > 0:
            placed[:baseline_adjust_y, :, :] = 0
        else:
            placed[baseline_adjust_y:, :, :] = 0
        translate_y += baseline_adjust_y
        visible = cv2.cvtColor(placed, cv2.COLOR_RGB2GRAY) >= CONTENT_CUTOFF
        output_bbox = mask_bbox(visible)

    destination.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(placed, "RGB").save(destination, optimize=True)
    expanded_visible = cv2.dilate(
        visible.astype(np.uint8), np.ones((3, 3), dtype=np.uint8), iterations=1
    ).astype(bool)
    return {
        "source": manifest_path(source),
        "output": manifest_path(destination),
        "source_canvas": [int(rgb.shape[1]), int(rgb.shape[0])],
        "output_canvas": [CANVAS_WIDTH, CANVAS_HEIGHT],
        "source_content_bbox": list(source_bbox),
        "output_content_bbox": list(output_bbox),
        "source_lower_body_anchor_x": round(source_anchor_x, 3),
        "target_lower_body_anchor_x": TARGET_LOWER_ANCHOR_X,
        "baseline_y": BASELINE_Y,
        "scale": OUTPUT_SCALE,
        "translate": [round(translate_x, 3), round(translate_y, 3)],
        "baseline_adjust_y": int(baseline_adjust_y),
        "visible_pixels": int(np.count_nonzero(visible)),
        "nonzero_background_channels": int(
            np.count_nonzero(placed[~expanded_visible])
        ),
    }


def main() -> int:
    args = parse_args()
    records: list[dict[str, object]] = []
    for source_name, output_name in SPRITES:
        source = args.input_dir / source_name
        if not source.is_file():
            raise FileNotFoundError(source)
        records.append(process_one(source, args.output_dir / output_name))

    payload = {
        "schema_version": 1,
        "canvas": [CANVAS_WIDTH, CANVAS_HEIGHT],
        "baseline_y": BASELINE_Y,
        "lower_body_anchor_x": TARGET_LOWER_ANCHOR_X,
        "matte_cutoff": MATTE_CUTOFF,
        "output_scale": OUTPUT_SCALE,
        "pixel_levels": list(PIXEL_LEVELS),
        "sprites": records,
    }
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
