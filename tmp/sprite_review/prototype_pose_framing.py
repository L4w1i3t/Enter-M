from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MATSUDA_ROOT = PROJECT_ROOT / "game" / "mod_assets" / "char_sprites" / "matsuda"
OUTPUT_ROOT = Path(__file__).resolve().parent / "matsuda_poses_v2"
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
WIDTH = 1023
HEIGHT = 1537


def warp_rgba_premultiplied(rgba: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    source = rgba.astype(np.float32) / 255.0
    alpha = source[:, :, 3:4]
    premultiplied = np.concatenate((source[:, :, :3] * alpha, alpha), axis=2)
    warped = cv2.warpAffine(
        premultiplied,
        matrix.astype(np.float32),
        (WIDTH, HEIGHT),
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


casual = np.asarray(
    Image.open(MATSUDA_ROOT / "pose_laughing_casual.png").convert("RGBA")
)
scale = 1505.0 / 1449.0
casual_matrix = np.array(
    (
        (scale, 0.0, 511.5 - scale * 534.0),
        (0.0, scale, HEIGHT - scale * HEIGHT),
    )
)
casual = warp_rgba_premultiplied(casual, casual_matrix)
Image.fromarray(casual, "RGBA").save(OUTPUT_ROOT / "pose_laughing_casual.png")


uniform_source = np.asarray(
    Image.open(MATSUDA_ROOT / "pose_laughing_uniform.png").convert("RGBA")
)
edge_rows = uniform_source[:, -1, 3] > 0
edge_rows = cv2.dilate(
    edge_rows[:, None].astype(np.uint8), np.ones((9, 1), np.uint8)
)[:, 0].astype(bool)
uniform = warp_rgba_premultiplied(
    uniform_source,
    np.array(((1.0, 0.0, -18.0), (0.0, 1.0, 0.0)), dtype=np.float32),
)

# The source's long ponytail was cut by the right canvas edge. After centering
# the figure, taper only those rows into a natural transparent strand ending.
hard_edge_x = WIDTH - 1 - 18
tail_width = 28
fade = np.ones((HEIGHT, WIDTH), dtype=np.float32)
for x in range(hard_edge_x - tail_width, hard_edge_x + 1):
    fade[edge_rows, x] = (hard_edge_x - x) / tail_width
uniform_alpha = np.rint(uniform[:, :, 3].astype(np.float32) * fade).astype(np.uint8)
uniform[:, :, 3] = uniform_alpha
uniform[uniform_alpha == 0, :3] = 0
Image.fromarray(uniform, "RGBA").save(OUTPUT_ROOT / "pose_laughing_uniform.png")
