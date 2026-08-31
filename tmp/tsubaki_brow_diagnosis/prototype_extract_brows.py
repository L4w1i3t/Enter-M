"""Prototype full-master brow recovery for Tsubaki (diagnostic only)."""

from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

import process_sam_sprites as sparse  # noqa: E402
import process_tsubaki_sprites as tsubaki  # noqa: E402


OUT_DIR = PROJECT_ROOT / "tmp" / "tsubaki_brow_diagnosis" / "prototype_full_brows"
MASTER_DIR = PROJECT_ROOT / "tmp" / "tsubaki_sprite_masters"
EXPRESSIONS = ("worried", "unamused", "disgusted", "sad", "angry", "shocked")


def font(size: int) -> ImageFont.ImageFont:
    for name in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def load_rgb(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        return np.asarray(image.convert("RGB"), dtype=np.uint8).copy()


def retain_seeded(candidate: np.ndarray, seed: np.ndarray) -> np.ndarray:
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        candidate.astype(np.uint8), connectivity=8
    )
    kept = np.zeros(candidate.shape, dtype=bool)
    for label in range(1, count):
        component = labels == label
        if int(stats[label, cv2.CC_STAT_AREA]) >= 2 and np.any(component & seed):
            kept |= component
    return kept


def brow_zone(spec: sparse.EllipseSpec, angle: float) -> np.ndarray:
    enlarged = sparse.EllipseSpec(
        spec.center_x,
        spec.center_y,
        spec.radius_x * 1.18,
        spec.radius_y * 1.35,
    )
    return sparse.rotated_ellipse_mask((1536, 1024), enlarged, angle)


def main() -> int:
    tsubaki.configure_sparse_processor()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    featureless_rgb = load_rgb(MASTER_DIR / "head_raw.png")
    featureless_valid = sparse.checker_foreground(featureless_rgb)
    featureless_rgba = np.dstack(
        (featureless_rgb, featureless_valid.astype(np.uint8) * 255)
    )
    left_zone = brow_zone(tsubaki.GEOMETRY.left_brow, tsubaki.LEFT_BROW_ANGLE)
    right_zone = brow_zone(tsubaki.GEOMETRY.right_brow, tsubaki.RIGHT_BROW_ANGLE)
    crop = (285, 525, 735, 660)

    sheet = Image.new("RGB", (1800, len(EXPRESSIONS) * 330), (26, 27, 31))
    draw = ImageDraw.Draw(sheet)
    report: list[str] = []
    for row, expression in enumerate(EXPRESSIONS):
        filename = tsubaki.MASTER_OVERRIDES.get(
            expression, f"expression_{expression}.png"
        )
        donor_rgb = load_rgb(MASTER_DIR / filename)
        donor_valid = sparse.checker_foreground(donor_rgb)
        matrix, _ = sparse.estimate_registration(
            donor_rgb, donor_valid, featureless_rgba
        )
        aligned_rgb = sparse.warp_rgb(donor_rgb, matrix)
        aligned_valid = sparse.warp_mask(donor_valid, matrix)
        raw_layer, _, _ = sparse.build_expression_layer(
            expression,
            featureless_rgba,
            aligned_rgb,
            aligned_valid,
            featureless_rgb,
            featureless_valid,
        )
        normalized, _ = sparse.normalize_rgb_diagonal(
            aligned_rgb,
            aligned_valid,
            featureless_rgb,
            featureless_valid,
        )
        delta = sparse.maximum_color_delta(normalized, featureless_rgb)
        gray = cv2.cvtColor(normalized, cv2.COLOR_RGB2GRAY)
        blank_gray = cv2.cvtColor(featureless_rgb, cv2.COLOR_RGB2GRAY)

        recovered = np.zeros(delta.shape, dtype=bool)
        seed_union = np.zeros(delta.shape, dtype=bool)
        candidate_union = np.zeros(delta.shape, dtype=bool)
        for zone in (left_zone, right_zone):
            seed = (raw_layer[:, :, 3] >= 8) & zone
            # The authored brows are dark, locally contrasting strokes.  A
            # relaxed candidate admits their anti-aliased rim; seeded
            # connectivity prevents unrelated low-frequency skin changes.
            candidate = (
                zone
                & aligned_valid
                & featureless_valid
                & (delta >= 8)
                & ((blank_gray.astype(np.int16) - gray.astype(np.int16)) >= 7)
                & (gray <= 190)
            )
            candidate = cv2.morphologyEx(
                candidate.astype(np.uint8),
                cv2.MORPH_CLOSE,
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
            ).astype(bool)
            grown_seed = cv2.dilate(
                seed.astype(np.uint8),
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
            ).astype(bool)
            kept = retain_seeded(candidate, grown_seed)
            recovered |= kept
            seed_union |= seed
            candidate_union |= candidate

        panels: list[Image.Image] = []
        panels.append(Image.fromarray(aligned_rgb, "RGB").crop(crop))
        for mask, color in (
            (seed_union, np.asarray((60, 220, 75), dtype=np.uint8)),
            (candidate_union, np.asarray((235, 180, 30), dtype=np.uint8)),
            (recovered, np.asarray((30, 205, 245), dtype=np.uint8)),
        ):
            preview = aligned_rgb.copy()
            preview[mask] = np.clip(
                preview[mask].astype(np.float32) * 0.25
                + color.astype(np.float32) * 0.75,
                0,
                255,
            ).astype(np.uint8)
            panels.append(Image.fromarray(preview, "RGB").crop(crop))

        y = row * 330
        for column, panel in enumerate(panels):
            sheet.paste(panel.resize((440, 264), Image.Resampling.NEAREST), (column * 450, y))
        draw.text((8, y + 272), expression, font=font(24), fill=(245, 245, 248))
        draw.text((450, y + 272), "sparse seed", font=font(24), fill=(245, 245, 248))
        draw.text((900, y + 272), "candidate", font=font(24), fill=(245, 245, 248))
        draw.text((1350, y + 272), "seeded recovery", font=font(24), fill=(245, 245, 248))
        report.append(
            f"{expression}: seed={int(seed_union.sum())} "
            f"candidate={int(candidate_union.sum())} recovered={int(recovered.sum())}"
        )

    sheet.save(OUT_DIR / "recovery_sheet.png", optimize=True)
    (OUT_DIR / "metrics.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    print(OUT_DIR / "recovery_sheet.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
