from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SPRITE_ROOT = PROJECT_ROOT / "game" / "mod_assets" / "char_sprites"
OUTPUT_ROOT = Path(__file__).resolve().parent
CANVAS_SIZE = (1023, 1537)
THUMBNAIL_SIZE = (220, 330)
CELL_SIZE = (248, 376)
COLUMNS = 7
HEAD_CROP = (260, 120, 760, 620)
HEAD_THUMBNAIL_SIZE = (360, 360)
HEAD_CELL_SIZE = (384, 412)
HEAD_COLUMNS = 5


def checkerboard(size: tuple[int, int], tile_size: int = 16) -> Image.Image:
    background = Image.new("RGBA", size, (48, 48, 52, 255))
    draw = ImageDraw.Draw(background)
    for y in range(0, size[1], tile_size):
        for x in range(0, size[0], tile_size):
            shade = 70 if (x // tile_size + y // tile_size) % 2 else 54
            draw.rectangle(
                (x, y, x + tile_size - 1, y + tile_size - 1),
                fill=(shade, shade, shade + 3, 255),
            )
    return background


def fit_sprite(image: Image.Image) -> Image.Image:
    sprite = image.convert("RGBA")
    sprite.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
    panel = checkerboard(THUMBNAIL_SIZE)
    x = (THUMBNAIL_SIZE[0] - sprite.width) // 2
    y = THUMBNAIL_SIZE[1] - sprite.height
    panel.alpha_composite(sprite, (x, y))
    return panel


def make_character_sheet(character: str) -> None:
    character_root = SPRITE_ROOT / character
    uniform_base_path = character_root / "neut_uniform_face_base.png"
    casual_base_path = character_root / "neut_face_base.png"
    uniform_base = Image.open(uniform_base_path).convert("RGBA")
    casual_base = Image.open(casual_base_path).convert("RGBA")

    entries: list[tuple[str, Image.Image]] = [
        ("base casual", casual_base),
        ("base uniform", uniform_base),
    ]

    for face_path in sorted(character_root.glob("face_*.png")):
        if face_path.name == "face_neut.png":
            continue
        face = Image.open(face_path).convert("RGBA")
        entries.append(
            (
                face_path.stem.removeprefix("face_"),
                Image.alpha_composite(uniform_base, face),
            )
        )

    for pose_path in sorted(character_root.glob("pose_*.png")):
        entries.append((pose_path.stem, Image.open(pose_path).convert("RGBA")))

    for legacy_name in ("terror.png", "wasted.png"):
        legacy_path = character_root / legacy_name
        if legacy_path.exists():
            entries.append((legacy_path.stem, Image.open(legacy_path).convert("RGBA")))

    rows = (len(entries) + COLUMNS - 1) // COLUMNS
    sheet = Image.new(
        "RGBA",
        (COLUMNS * CELL_SIZE[0], rows * CELL_SIZE[1]),
        (24, 24, 28, 255),
    )
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=16)

    for index, (label, image) in enumerate(entries):
        column = index % COLUMNS
        row = index // COLUMNS
        cell_x = column * CELL_SIZE[0]
        cell_y = row * CELL_SIZE[1]
        sheet.alpha_composite(fit_sprite(image), (cell_x + 14, cell_y + 8))
        draw.text(
            (cell_x + CELL_SIZE[0] // 2, cell_y + 344),
            label,
            font=font,
            fill=(238, 238, 242, 255),
            anchor="ma",
        )

    sheet.convert("RGB").save(OUTPUT_ROOT / f"{character}_contact_sheet.jpg", quality=92)

    head_entries = entries[:2] + [
        entry for entry in entries[2:] if not entry[0].startswith("pose_")
    ]
    head_rows = (len(head_entries) + HEAD_COLUMNS - 1) // HEAD_COLUMNS
    head_sheet = Image.new(
        "RGB",
        (HEAD_COLUMNS * HEAD_CELL_SIZE[0], head_rows * HEAD_CELL_SIZE[1]),
        (24, 24, 28),
    )
    head_draw = ImageDraw.Draw(head_sheet)
    for index, (label, image) in enumerate(head_entries):
        column = index % HEAD_COLUMNS
        row = index // HEAD_COLUMNS
        cell_x = column * HEAD_CELL_SIZE[0]
        cell_y = row * HEAD_CELL_SIZE[1]
        crop = image.convert("RGBA").crop(HEAD_CROP)
        crop.thumbnail(HEAD_THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
        panel = checkerboard(HEAD_THUMBNAIL_SIZE, tile_size=20)
        panel.alpha_composite(
            crop,
            (
                (HEAD_THUMBNAIL_SIZE[0] - crop.width) // 2,
                (HEAD_THUMBNAIL_SIZE[1] - crop.height) // 2,
            ),
        )
        head_sheet.paste(panel.convert("RGB"), (cell_x + 12, cell_y + 8))
        head_draw.text(
            (cell_x + HEAD_CELL_SIZE[0] // 2, cell_y + 380),
            label,
            font=font,
            fill=(238, 238, 242),
            anchor="ma",
        )
    head_sheet.save(OUTPUT_ROOT / f"{character}_heads.jpg", quality=95)


for character_name in ("asahina", "matsuda", "himeko"):
    make_character_sheet(character_name)
