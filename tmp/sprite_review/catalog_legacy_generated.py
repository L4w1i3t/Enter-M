from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


GENERATED_ROOT = Path(r"C:\Users\Admin\.codex\generated_images")
DIRECTORIES = (
    "019ffe18-f0bb-7103-9751-b6f8ee91d8bd",
    "019ffe3c-4463-7322-805c-4ff8a6580355",
    "019ffe99-64f6-7b11-b348-f506e24cda0c",
    "019ffe99-c29e-7991-afb7-a99b7f516680",
    "019ffe99-966b-7f81-9981-7b2a893dc20f",
)
OUTPUT_ROOT = Path(__file__).resolve().parent
paths = sorted(
    [path for directory in DIRECTORIES for path in (GENERATED_ROOT / directory).glob("*.png")],
    key=lambda path: path.stat().st_mtime,
)

columns = 8
cell_width = 280
cell_height = 330
rows = (len(paths) + columns - 1) // columns
sheet = Image.new("RGB", (columns * cell_width, rows * cell_height), (20, 20, 24))
draw = ImageDraw.Draw(sheet)
font = ImageFont.load_default(size=15)
manifest: list[str] = []

for index, path in enumerate(paths):
    image = Image.open(path).convert("RGB")
    width, height = image.size
    if height / width >= 1.35:
        crop = image.crop((int(width * 0.20), int(height * 0.04), int(width * 0.80), int(height * 0.47)))
    else:
        crop = image
    crop.thumbnail((255, 255), Image.Resampling.LANCZOS)
    column = index % columns
    row = index // columns
    x = column * cell_width
    y = row * cell_height
    sheet.paste(crop, (x + (cell_width - crop.width) // 2, y + 4))
    identifier = path.stem.removeprefix("exec-")[:8]
    timestamp = datetime.fromtimestamp(path.stat().st_mtime).strftime("%m-%d %H:%M")
    draw.text(
        (x + cell_width // 2, y + 270),
        f"{index:02d} {identifier}",
        fill=(245, 245, 248),
        font=font,
        anchor="ma",
    )
    draw.text(
        (x + cell_width // 2, y + 292),
        timestamp,
        fill=(170, 174, 184),
        font=font,
        anchor="ma",
    )
    manifest.append(f"{index:02d}\t{identifier}\t{timestamp}\t{path}")

sheet.save(OUTPUT_ROOT / "legacy_generated_heads.jpg", quality=95)
(OUTPUT_ROOT / "legacy_generated_manifest.txt").write_text(
    "\n".join(manifest) + "\n", encoding="utf-8"
)
