#!/usr/bin/env python3
"""Build Asahiko's fixed front-facing layered-expression sprite bank.

The image generator supplies a transparent neutral anchor and full-canvas
expression masters.  This tool keeps the neutral body byte-stable after one
canvas normalisation pass, then exports every alternate through one shared,
feathered face mask.  Only the staged output directory is written; installing
the reviewed bank into ``game/assets/characters/mc`` remains a separate step.
"""

from __future__ import annotations

import argparse
import hashlib
import math
from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


CANVAS_SIZE = (1023, 1537)
EXPRESSIONS = (
    "happy",
    "smug",
    "teasing",
    "thinking",
    "curious",
    "unamused",
    "annoyed",
    "frustrated",
    "angry",
    "sad",
    "crying",
    "embarrassed",
    "nervous",
    "worried",
    "shocked",
    "afraid",
    "panicked",
    "determined",
    "empty",
    "disgusted",
)

# The opaque core owns all brows, eyes, nose, cheeks, and mouth.  The feather
# ends inside the canonical head silhouette, preventing both duplicate neutral
# features and a visible oval seam against the untouched hair and neck.
FACE_PLATE_BOX = (356, 157, 668, 425)
FACE_PLATE_FEATHER = 28


def load_rgba(path: Path) -> Image.Image:
    with Image.open(path) as opened:
        image = opened.convert("RGBA")
    if image.size != CANVAS_SIZE:
        # Resize premultiplied color so transparent-edge RGB cannot create a
        # bright fringe while 1024x1536 generator output is normalised to the
        # project's established 1023x1537 sprite canvas.
        image = image.convert("RGBa").resize(
            CANVAS_SIZE, Image.Resampling.LANCZOS
        ).convert("RGBA")
    pixels = np.asarray(image, dtype=np.uint8).copy()
    alpha = pixels[:, :, 3]
    # Built-in background extraction can leave a nearly invisible alpha mist
    # outside the subject and a 253/254 interior.  Snap only those endpoint
    # ranges; preserve the real antialiased transition between them.
    alpha[alpha <= 16] = 0
    alpha[alpha >= 240] = 255
    pixels[:, :, 3] = alpha
    return zero_transparent_rgb(Image.fromarray(pixels, "RGBA"))


def zero_transparent_rgb(image: Image.Image) -> Image.Image:
    pixels = np.asarray(image, dtype=np.uint8).copy()
    pixels[pixels[:, :, 3] == 0, :3] = 0
    return Image.fromarray(pixels, "RGBA")


def shared_face_mask(base: Image.Image) -> Image.Image:
    base_alpha = base.getchannel("A")
    outer = Image.new("L", CANVAS_SIZE, 0)
    ImageDraw.Draw(outer).ellipse(FACE_PLATE_BOX, fill=255)

    left, top, right, bottom = FACE_PLATE_BOX
    inset = FACE_PLATE_FEATHER
    core = Image.new("L", CANVAS_SIZE, 0)
    ImageDraw.Draw(core).ellipse(
        (left + inset, top + inset, right - inset, bottom - inset), fill=255
    )
    feathered = core.filter(ImageFilter.GaussianBlur(inset / 2.0))
    feathered = ImageChops.multiply(feathered, outer)
    feathered = feathered.point(lambda alpha: 0 if alpha < 3 else alpha)
    return ImageChops.multiply(feathered, base_alpha)


def face_plate(master: Image.Image, mask: Image.Image) -> Image.Image:
    red, green, blue, _ = master.split()
    plate = Image.merge("RGBA", (red, green, blue, mask))
    return zero_transparent_rgb(plate)


def save_png(image: Image.Image, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, optimize=True)
    print(destination)


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("sprite has an empty alpha silhouette")
    return bbox


def validate_bank(output_dir: Path, base: Image.Image, mask: Image.Image) -> None:
    expected = {"neutral.png", "face_neut.png"} | {
        f"face_{expression}.png" for expression in EXPRESSIONS
    }
    actual = {path.name for path in output_dir.glob("*.png")}
    missing = expected - actual
    if missing:
        raise ValueError("missing staged sprite(s): " + ", ".join(sorted(missing)))

    base_pixels = np.asarray(base, dtype=np.uint8)
    base_alpha = base_pixels[:, :, 3]
    if not np.any(base_alpha == 255):
        raise ValueError("neutral base has no fully opaque interior")
    if np.any(base_pixels[base_alpha == 0, :3]):
        raise ValueError("neutral base retains RGB beneath zero alpha")

    neutral = np.asarray(Image.open(output_dir / "face_neut.png").convert("RGBA"))
    if np.any(neutral):
        raise ValueError("face_neut.png must be completely transparent black")

    canonical_alpha = np.asarray(mask, dtype=np.uint8)
    digests: dict[str, list[str]] = {}
    for expression in EXPRESSIONS:
        path = output_dir / f"face_{expression}.png"
        pixels = np.asarray(Image.open(path).convert("RGBA"), dtype=np.uint8)
        if (pixels.shape[1], pixels.shape[0]) != CANVAS_SIZE:
            raise ValueError(f"{path}: wrong canvas {pixels.shape[1]}x{pixels.shape[0]}")
        if not np.array_equal(pixels[:, :, 3], canonical_alpha):
            raise ValueError(f"{path}: alpha mask differs from the shared mask")
        if np.any(pixels[pixels[:, :, 3] == 0, :3]):
            raise ValueError(f"{path}: RGB remains beneath zero alpha")
        digest = hashlib.sha256(pixels.tobytes()).hexdigest()
        digests.setdefault(digest, []).append(expression)

    duplicates = [names for names in digests.values() if len(names) > 1]
    if duplicates:
        raise ValueError(
            "duplicate expression plate(s): "
            + "; ".join(", ".join(names) for names in duplicates)
        )

    left, top, right, bottom = alpha_bbox(base)
    mask_bbox = mask.getbbox()
    print(
        "MC SPRITE VALIDATION PASSED: "
        f"base bbox=({left}, {top}, {right}, {bottom}); "
        f"face mask bbox={mask_bbox}; 21 distinct expressions; shared alpha; "
        "transparent RGB clean."
    )


def review_panel(sprite: Image.Image, label: str) -> Image.Image:
    panel_size = (236, 350)
    art_height = 320
    panel = Image.new("RGBA", panel_size, (32, 35, 43, 255))
    display = sprite.copy()
    display.thumbnail((224, art_height - 8), Image.Resampling.LANCZOS)
    panel.alpha_composite(display, ((panel.width - display.width) // 2, art_height - display.height))
    draw = ImageDraw.Draw(panel)
    draw.rectangle((0, art_height, panel.width - 1, panel.height - 1), fill=(13, 15, 20, 255))
    try:
        font = ImageFont.load_default(size=14)
    except TypeError:
        font = ImageFont.load_default()
    draw.text((panel.width // 2, 335), label, anchor="mm", font=font, fill=(245, 247, 251, 255))
    draw.rectangle((0, 0, panel.width - 1, panel.height - 1), outline=(85, 91, 104, 255))
    return panel


def write_review_sheet(output_dir: Path, destination: Path) -> None:
    base = Image.open(output_dir / "neutral.png").convert("RGBA")
    entries: list[tuple[str, Image.Image]] = [("neut", base)]
    for expression in EXPRESSIONS:
        layer = Image.open(output_dir / f"face_{expression}.png").convert("RGBA")
        entries.append((expression, Image.alpha_composite(base, layer)))

    columns = 7
    rows = math.ceil(len(entries) / columns)
    sheet = Image.new("RGBA", (columns * 236, rows * 350), (17, 19, 25, 255))
    for index, (label, sprite) in enumerate(entries):
        row, column = divmod(index, columns)
        sheet.alpha_composite(review_panel(sprite, label), (column * 236, row * 350))
    destination.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(destination, optimize=True)
    print(destination)


def expression_paths(master_dir: Path) -> Iterable[tuple[str, Path]]:
    for expression in EXPRESSIONS:
        yield expression, master_dir / f"expression_{expression}.png"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--anchor", type=Path, required=True)
    parser.add_argument("--master-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--review-sheet", type=Path)
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    if not arguments.anchor.is_file():
        raise SystemExit(f"missing neutral anchor: {arguments.anchor}")

    missing_masters = [
        path for _expression, path in expression_paths(arguments.master_dir) if not path.is_file()
    ]
    if missing_masters:
        raise SystemExit(
            "missing expression master(s):\n  "
            + "\n  ".join(str(path) for path in missing_masters)
        )

    base = load_rgba(arguments.anchor)
    save_png(base, arguments.output_dir / "neutral.png")
    transparent = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    save_png(transparent, arguments.output_dir / "face_neut.png")

    mask = shared_face_mask(base)
    for expression, path in expression_paths(arguments.master_dir):
        save_png(
            face_plate(load_rgba(path), mask),
            arguments.output_dir / f"face_{expression}.png",
        )

    validate_bank(arguments.output_dir, base, mask)
    if arguments.review_sheet is not None:
        write_review_sheet(arguments.output_dir, arguments.review_sheet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
