"""Native-scale comparison of Tsubaki upper-face composites (diagnostic)."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

import process_tsubaki_face_patches as patches  # noqa: E402


OUT_DIR = PROJECT_ROOT / "tmp" / "tsubaki_brow_diagnosis"
EXPRESSIONS = ("worried", "unamused", "disgusted")
BUILDS = (
    ("schema-v4 production", PROJECT_ROOT / "tmp" / "tsubaki_face_patch" / "output"),
    (
        "adaptive corridor candidate",
        PROJECT_ROOT / "tmp" / "tsubaki_semantic_repair_staging_v4",
    ),
)
CROP = (385, 315, 630, 430)
SCALE = 3
LABEL_HEIGHT = 44


def font(size: int) -> ImageFont.ImageFont:
    for candidate in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def composite(build: Path, outfit: str, expression: str) -> Image.Image:
    spec = patches.OUTFITS[outfit]
    base = patches.load_rgba(
        patches.SPRITE_DIR / str(spec["base"]), patches.OUTPUT_SIZE
    )
    layer = patches.load_rgba(
        build / f"face_{expression}_{outfit}.png", patches.OUTPUT_SIZE
    )
    pixels = patches.alpha_composite(base, layer)
    return Image.fromarray(pixels, "RGBA").convert("RGB")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    crop_width = CROP[2] - CROP[0]
    crop_height = CROP[3] - CROP[1]
    cell = (crop_width * SCALE, crop_height * SCALE + LABEL_HEIGHT)
    columns = len(EXPRESSIONS)
    rows = len(BUILDS)
    for outfit in patches.OUTFITS:
        sheet = Image.new("RGB", (columns * cell[0], rows * cell[1]), (28, 30, 35))
        draw = ImageDraw.Draw(sheet)
        for row, (build_label, build) in enumerate(BUILDS):
            for column, expression in enumerate(EXPRESSIONS):
                crop = composite(build, outfit, expression).crop(CROP)
                crop = crop.resize(
                    (crop_width * SCALE, crop_height * SCALE),
                    Image.Resampling.NEAREST,
                )
                x = column * cell[0]
                y = row * cell[1]
                sheet.paste(crop, (x, y))
                draw.text(
                    (x + 8, y + crop.height + 6),
                    f"{expression} | {build_label}",
                    fill=(242, 242, 246),
                    font=font(24),
                )
        path = OUT_DIR / f"{outfit}_runtime_brow_comparison.png"
        sheet.save(path, optimize=True)
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
