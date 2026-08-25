from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parent / "facebase_v3" / "asahina"

for name in ("happy", "thinking", "empty", "embarrassed"):
    rgba = np.asarray(Image.open(ROOT / f"face_{name}.png").convert("RGBA"))
    for threshold in (1, 32, 128, 254):
        mask = (rgba[:, :, 3] >= threshold).astype(np.uint8)
        count, _, stats, centroids = cv2.connectedComponentsWithStats(mask, 8)
        components = []
        for label in range(1, count):
            x, y, width, height, area = stats[label]
            if area >= 8:
                components.append(
                    (
                        int(area),
                        (int(x), int(y), int(x + width), int(y + height)),
                        tuple(round(float(value), 1) for value in centroids[label]),
                    )
                )
        components.sort(reverse=True)
        print(f"{name} alpha>={threshold}: {components[:16]}")
