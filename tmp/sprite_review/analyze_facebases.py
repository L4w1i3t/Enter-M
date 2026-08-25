from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SPRITES = ROOT / "game" / "mod_assets" / "char_sprites"
RECOVERED = Path(__file__).resolve().parent / "prechange" / "recovered_layers"


def load(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGBA"))


def bbox(mask: np.ndarray) -> tuple[int, int, int, int] | None:
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


for character, outfit, neutral_name, recovered_name in (
    ("asahina", "uniform", "neut_uniform.png", "neut_uniform_face_base.png"),
    ("matsuda", "casual", "neutral.png", "neut_face_base.png"),
    ("matsuda", "uniform", "neut_uniform.png", "neut_uniform_face_base.png"),
):
    neutral_path = SPRITES / character / neutral_name
    recovered_path = RECOVERED / character / recovered_name
    neutral = load(neutral_path)
    recovered = load(recovered_path)
    rgb_diff = np.max(
        np.abs(neutral[:, :, :3].astype(np.int16) - recovered[:, :, :3].astype(np.int16)),
        axis=2,
    )
    alpha_diff = neutral[:, :, 3] != recovered[:, :, 3]
    shared_visible = (neutral[:, :, 3] > 0) & (recovered[:, :, 3] > 0)
    shared_opaque = (neutral[:, :, 3] == 255) & (recovered[:, :, 3] == 255)
    print(
        f"{character}/{outfit}: size={neutral.shape[1]}x{neutral.shape[0]} "
        f"rgb_changed={int((rgb_diff > 0).sum())} bbox={bbox(rgb_diff > 0)} "
        f"rgb_gt8={int((rgb_diff > 8).sum())} bbox8={bbox(rgb_diff > 8)} "
        f"alpha_changed={int(alpha_diff.sum())} bbox_alpha={bbox(alpha_diff)} "
        f"visible_rgb_changed={int(((rgb_diff > 0) & shared_visible).sum())} "
        f"visible_bbox={bbox((rgb_diff > 0) & shared_visible)} "
        f"opaque_rgb_gt8={int(((rgb_diff > 8) & shared_opaque).sum())} "
        f"opaque_bbox8={bbox((rgb_diff > 8) & shared_opaque)} "
        f"recovered_alpha_zero={int((recovered[:, :, 3] == 0).sum())} "
        f"recovered_alpha_opaque={int((recovered[:, :, 3] == 255).sum())}"
    )


for character in ("asahina", "matsuda"):
    print(f"\n{character} installed overlays")
    for path in sorted((SPRITES / character).glob("face_*.png")):
        rgba = load(path)
        alpha = rgba[:, :, 3]
        nonzero = alpha > 0
        levels = np.unique(alpha[nonzero]) if nonzero.any() else np.array([], dtype=np.uint8)
        print(
            f"{path.stem.removeprefix('face_'):12s} pixels={int(nonzero.sum()):6d} "
            f"bbox={bbox(nonzero)} partial={int(((alpha > 0) & (alpha < 255)).sum()):6d} "
            f"opaque={int((alpha == 255).sum()):6d} levels={len(levels):3d}"
        )
