"""Finalize Tsubaki's headless outfit bodies for production installation.

The generated casual torso is correctly registered at the collar and
shoulders, but its cropped lower-body silhouette sits 6.5 pixels left of the
guide's x=512 neutral anchor.  A smooth lower-only horizontal warp recenters the
jeans without moving any neck, collar, torso, or arm join.  The uniform body is
copied unchanged because its measured anchor is already compliant.
"""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MASTER_DIR = PROJECT_ROOT / "tmp" / "tsubaki_sprite_masters"
PART_DIR = PROJECT_ROOT / "tmp" / "tsubaki_sprite_parts"
CANVAS_SIZE = (1024, 1536)


def load_rgba(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        if image.size != CANVAS_SIZE or image.mode != "RGBA":
            raise ValueError(
                f"{path}: expected RGBA {CANVAS_SIZE}, got {image.mode} {image.size}"
            )
        return np.asarray(image, dtype=np.uint8).copy()


def save_rgba(path: Path, rgba: np.ndarray) -> None:
    clean = np.asarray(rgba, dtype=np.uint8).copy()
    clean[clean[:, :, 3] == 0, :3] = 0
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(clean, "RGBA").save(path, optimize=True)


def widest_run_center(row: np.ndarray) -> float | None:
    columns = np.flatnonzero(row)
    if columns.size == 0:
        return None
    runs = np.split(columns, np.flatnonzero(np.diff(columns) > 1) + 1)
    widest = max(runs, key=lambda run: (run.size, -int(run[0])))
    return (float(widest[0]) + float(widest[-1])) / 2.0


def lower_anchor(rgba: np.ndarray) -> float:
    visible = rgba[:, :, 3] >= 128
    rows = np.flatnonzero(np.any(visible, axis=1))
    if rows.size == 0:
        raise ValueError("Cannot measure an empty body")
    top, bottom = int(rows.min()), int(rows.max()) + 1
    band_start = max(top, bottom - max(24, round((bottom - top) * 0.12)))
    centers = [
        center
        for row in range(band_start, bottom)
        if (center := widest_run_center(visible[row])) is not None
    ]
    if len(centers) < 8:
        raise ValueError("Insufficient lower-body rows for an anchor")
    return float(np.median(np.asarray(centers, dtype=np.float64)))


def warp_lower_body(
    rgba: np.ndarray,
    *,
    final_shift_x: float,
    transition_start_y: int,
    transition_end_y: int,
) -> np.ndarray:
    """Shift only the lower silhouette with a smooth premultiplied-alpha warp."""

    height, width = rgba.shape[:2]
    yy, xx = np.indices((height, width), dtype=np.float32)
    progress = np.clip(
        (yy - float(transition_start_y))
        / float(transition_end_y - transition_start_y),
        0.0,
        1.0,
    )
    smooth_progress = progress * progress * (3.0 - 2.0 * progress)
    map_x = xx - final_shift_x * smooth_progress
    map_y = yy

    source = rgba.astype(np.float32) / 255.0
    source_alpha = source[:, :, 3]
    premultiplied = source[:, :, :3] * source_alpha[:, :, None]
    warped_alpha = cv2.remap(
        source_alpha,
        map_x,
        map_y,
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )
    warped_premultiplied = cv2.remap(
        premultiplied,
        map_x,
        map_y,
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )
    warped_rgb = np.zeros_like(warped_premultiplied)
    visible = warped_alpha > (0.5 / 255.0)
    warped_rgb[visible] = (
        warped_premultiplied[visible] / warped_alpha[visible, None]
    )
    result = np.dstack((warped_rgb, warped_alpha))
    result = np.clip(np.rint(result * 255.0), 0, 255).astype(np.uint8)
    result[result[:, :, 3] == 0, :3] = 0
    return result


def main() -> int:
    casual_source = load_rgba(MASTER_DIR / "forward_casual_body.png")
    uniform_source = load_rgba(MASTER_DIR / "forward_uniform_body.png")
    casual = warp_lower_body(
        casual_source,
        final_shift_x=7.0,
        transition_start_y=1050,
        transition_end_y=1250,
    )
    uniform = uniform_source.copy()

    save_rgba(PART_DIR / "forward_casual_body.png", casual)
    save_rgba(PART_DIR / "forward_uniform_body.png", uniform)
    report = {
        "schema_version": 1,
        "casual": {
            "source_anchor_x": lower_anchor(casual_source),
            "production_anchor_x": lower_anchor(casual),
            "final_shift_x": 7.0,
            "transition_y": [1050, 1250],
        },
        "uniform": {
            "source_anchor_x": lower_anchor(uniform_source),
            "production_anchor_x": lower_anchor(uniform),
            "final_shift_x": 0.0,
        },
    }
    (PART_DIR / "body_metrics.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(
        "Finalized Tsubaki bodies: "
        f"casual anchor {report['casual']['source_anchor_x']:.1f} -> "
        f"{report['casual']['production_anchor_x']:.1f}; "
        f"uniform {report['uniform']['production_anchor_x']:.1f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
