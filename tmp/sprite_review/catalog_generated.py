from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


GENERATED_ROOT = Path(r"C:\Users\Admin\.codex\generated_images")
DIRECTORIES = (
    "01a02683-677a-7631-92b0-7c5eb1a4d575",
    "01a02685-b515-7832-8beb-22a2bc93168e",
    "01a02685-a556-7493-b0c9-42e9b7e8acf4",
    "01a02685-99a6-7ca3-96c2-038d1d52b1d3",
)
OUTPUT_ROOT = Path(__file__).resolve().parent


paths = sorted(
    [path for directory in DIRECTORIES for path in (GENERATED_ROOT / directory).glob("*.png")],
    key=lambda path: path.stat().st_mtime,
)
columns = 6
cell_width = 280
cell_height = 415
rows = (len(paths) + columns - 1) // columns
sheet = Image.new("RGB", (columns * cell_width, rows * cell_height), (20, 20, 24))
draw = ImageDraw.Draw(sheet)
font = ImageFont.load_default(size=15)

for index, path in enumerate(paths):
    image = Image.open(path).convert("RGB")
    thumbnail = image.copy()
    thumbnail.thumbnail((250, 340), Image.Resampling.LANCZOS)
    column = index % columns
    row = index // columns
    x = column * cell_width
    y = row * cell_height
    sheet.paste(thumbnail, (x + (cell_width - thumbnail.width) // 2, y + 4))
    timestamp = datetime.fromtimestamp(path.stat().st_mtime).strftime("%H:%M:%S")
    identifier = path.stem.removeprefix("exec-")[:8]
    draw.text(
        (x + cell_width // 2, y + 355),
        f"{index:02d}  {identifier}",
        fill=(245, 245, 248),
        font=font,
        anchor="ma",
    )
    draw.text(
        (x + cell_width // 2, y + 377),
        timestamp,
        fill=(170, 174, 184),
        font=font,
        anchor="ma",
    )

sheet.save(OUTPUT_ROOT / "generated_expression_catalog.jpg", quality=94)

head_sheet = Image.new("RGB", (columns * cell_width, rows * 300), (20, 20, 24))
head_draw = ImageDraw.Draw(head_sheet)
for index, path in enumerate(paths):
    image = Image.open(path).convert("RGB").crop((260, 100, 760, 600))
    image.thumbnail((250, 250), Image.Resampling.LANCZOS)
    column = index % columns
    row = index // columns
    x = column * cell_width
    y = row * 300
    head_sheet.paste(image, (x + (cell_width - image.width) // 2, y + 4))
    identifier = path.stem.removeprefix("exec-")[:8]
    head_draw.text(
        (x + cell_width // 2, y + 265),
        f"{index:02d}  {identifier}",
        fill=(245, 245, 248),
        font=font,
        anchor="ma",
    )
head_sheet.save(OUTPUT_ROOT / "generated_expression_heads.jpg", quality=96)
