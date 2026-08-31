"""Inspect pale semantic components crossing Tsubaki's ghost-arc guard."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

import process_sam_sprites as sparse  # noqa: E402
import process_tsubaki_face_patches as patches  # noqa: E402


SOURCE_DIR = PROJECT_ROOT / "tmp" / "tsubaki_sprite_processed"
OUT_DIR = PROJECT_ROOT / "tmp" / "tsubaki_brow_diagnosis" / "ghost_components"


def font(size: int) -> ImageFont.ImageFont:
    for name in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    metrics = json.loads((SOURCE_DIR / "metrics.json").read_text(encoding="utf-8"))
    production = np.asarray(metrics["production_matrix"], dtype=np.float32)
    raw_guard = np.zeros((patches.SOURCE_SIZE[1], patches.SOURCE_SIZE[0]), dtype=np.uint8)
    for path in patches.SOURCE_CREASE_PATHS:
        cv2.polylines(
            raw_guard,
            [np.asarray(path, dtype=np.int32)],
            isClosed=False,
            color=1,
            thickness=patches.SOURCE_CREASE_THICKNESS,
            lineType=cv2.LINE_AA,
        )
    raw_guard = raw_guard > 0

    expressions = patches.EXPRESSIONS[1:]
    cols = 4
    cell_w, cell_h = 500, 250
    rows = (len(expressions) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), (25, 26, 30))
    draw = ImageDraw.Draw(sheet)
    lines: list[str] = []
    for index, expression in enumerate(expressions):
        source = patches.load_rgba(SOURCE_DIR / f"face_{expression}.png", patches.SOURCE_SIZE)
        registration = patches.registration_matrix(
            metrics["layers"][expression]["registration"]
        )
        donor_to_production = patches.compose_affine(production, registration)
        guard = cv2.warpAffine(
            raw_guard.astype(np.uint8),
            donor_to_production,
            patches.SOURCE_SIZE,
            flags=cv2.INTER_NEAREST,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=0,
        ).astype(bool)
        support = source[:, :, 3] >= patches.DETAIL_ALPHA_MINIMUM
        dark, amber, pale, red = sparse.feature_palette(source[:, :, :3])
        pale_support = support & pale
        count, labels, stats, _ = cv2.connectedComponentsWithStats(
            pale_support.astype(np.uint8), connectivity=8
        )
        selected = np.zeros(support.shape, dtype=bool)
        component_summaries: list[str] = []
        for label in range(1, count):
            component = labels == label
            overlap = int((component & guard).sum())
            if not overlap:
                continue
            left = int(stats[label, cv2.CC_STAT_LEFT])
            top = int(stats[label, cv2.CC_STAT_TOP])
            width = int(stats[label, cv2.CC_STAT_WIDTH])
            height = int(stats[label, cv2.CC_STAT_HEIGHT])
            area = int(stats[label, cv2.CC_STAT_AREA])
            component_summaries.append(
                f"({left},{top},{width},{height},area={area},guard={overlap})"
            )
            # Initial hypothesis only; the sheet makes false selections clear.
            if width >= 4 and height <= 8 and area <= 180:
                selected |= component

        preview = patches.alpha_composite(
            patches.load_rgba(
                PROJECT_ROOT / "tmp" / "tsubaki_sprite_parts" / "forward_head.png",
                patches.SOURCE_SIZE,
            ),
            source,
        )[:, :, :3]
        overlay = preview.copy()
        overlay[guard] = np.clip(
            overlay[guard].astype(np.float32) * 0.55
            + np.asarray((235, 175, 25), dtype=np.float32) * 0.45,
            0,
            255,
        ).astype(np.uint8)
        overlay[pale_support] = np.asarray((65, 220, 85), dtype=np.uint8)
        overlay[selected] = np.asarray((35, 205, 245), dtype=np.uint8)
        crop = Image.fromarray(overlay, "RGB").crop((350, 520, 700, 665))
        crop = crop.resize((cell_w, 205), Image.Resampling.NEAREST)
        x = (index % cols) * cell_w
        y = (index // cols) * cell_h
        sheet.paste(crop, (x, y))
        draw.text((x + 6, y + 210), expression, fill=(245, 245, 248), font=font(22))
        lines.append(
            f"{expression}: guard={int(guard.sum())} support_overlap={int((guard & support).sum())} "
            f"dark={int((guard & support & dark).sum())} amber={int((guard & support & amber).sum())} "
            f"pale_overlap={int((guard & pale_support).sum())} red={int((guard & support & red).sum())} "
            f"unclassified={int((guard & support & ~(dark | amber | pale | red)).sum())} "
            f"selected={int(selected.sum())} "
            + " ".join(component_summaries)
        )

    sheet.save(OUT_DIR / "pale_components.png", optimize=True)
    (OUT_DIR / "metrics.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(OUT_DIR / "pale_components.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
