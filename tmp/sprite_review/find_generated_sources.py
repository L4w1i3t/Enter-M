from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[2]
GENERATED_ROOT = Path(r"C:\Users\Admin\.codex\generated_images")
ASAHINA_ROOT = PROJECT_ROOT / "game" / "mod_assets" / "char_sprites" / "asahina"
CANVAS_SIZE = (1023, 1537)
CROP_BOX = (300, 150, 730, 560)
SAMPLE_STEP = 4


candidate_crops: list[tuple[Path, np.ndarray]] = []
for source_path in GENERATED_ROOT.rglob("*.png"):
    with Image.open(source_path) as source_image:
        normalized = source_image.convert("RGBA").resize(
            CANVAS_SIZE, Image.Resampling.LANCZOS
        )
        crop = np.asarray(normalized.crop(CROP_BOX), dtype=np.int16)
        candidate_crops.append((source_path, crop))


for face_path in sorted(ASAHINA_ROOT.glob("face_*.png")):
    if face_path.name == "face_neut.png":
        continue
    with Image.open(face_path) as face_image:
        target = np.asarray(face_image.convert("RGBA").crop(CROP_BOX), dtype=np.int16)

    target_sample = target[::SAMPLE_STEP, ::SAMPLE_STEP]
    target_mask = target_sample[:, :, 3] >= 240
    scores: list[tuple[float, Path]] = []
    for source_path, candidate in candidate_crops:
        candidate_sample = candidate[::SAMPLE_STEP, ::SAMPLE_STEP]
        difference = np.abs(
            candidate_sample[:, :, :3] - target_sample[:, :, :3]
        )
        score = float(difference[target_mask].mean())
        scores.append((score, source_path))

    best = sorted(scores)[:3]
    print(face_path.stem)
    for score, source_path in best:
        print(f"  {score:7.3f} | {source_path}")
