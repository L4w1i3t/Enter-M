#!/usr/bin/env python3
"""Turn fresh full-sprite Sam expression masters into shared face plates.

Sam's casual and uniform sprites have the same registered head.  Each generated
master is therefore clipped once to a soft head-shaped mask and can be layered
over either intact outfit base, matching Himeko's base-plus-face setup.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CANVAS_SIZE = (1023, 1537)
SPRITE_DIR = PROJECT_ROOT / "game" / "assets" / "characters" / "masayami"
DEFAULT_MASTER_DIR = PROJECT_ROOT / "tmp" / "sam_rebuild_fresh" / "masters"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "tmp" / "sam_rebuild_fresh" / "staged"

# The ellipse covers Sam's complete facial anatomy and enough surrounding hair
# to hide the old expression.  Its broad feather keeps the generated donor from
# forming a visible cut line against either untouched outfit base.
HEAD_PLATE_BOX = (316, 160, 674, 458)
HEAD_PLATE_FEATHER = 28


def load_canvas(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    if image.size != CANVAS_SIZE:
        raise ValueError(f"{path}: expected {CANVAS_SIZE}, found {image.size}")
    return image


def shared_head_mask() -> Image.Image:
    casual_alpha = load_canvas(SPRITE_DIR / "neutral.png").getchannel("A")
    uniform_alpha = load_canvas(SPRITE_DIR / "neut_uniform.png").getchannel("A")

    # Only retain pixels that are fully inside both canonical silhouettes.  The
    # generator's baked transparency checker can never enter the exported PNG.
    shared_interior = ImageChops.darker(casual_alpha, uniform_alpha).point(
        lambda alpha: 255 if alpha >= 250 else 0
    )

    outer_ellipse = Image.new("L", CANVAS_SIZE, 0)
    ImageDraw.Draw(outer_ellipse).ellipse(HEAD_PLATE_BOX, fill=255)

    left, top, right, bottom = HEAD_PLATE_BOX
    inset_box = (
        left + HEAD_PLATE_FEATHER,
        top + HEAD_PLATE_FEATHER,
        right - HEAD_PLATE_FEATHER,
        bottom - HEAD_PLATE_FEATHER,
    )
    feathered_ellipse = Image.new("L", CANVAS_SIZE, 0)
    ImageDraw.Draw(feathered_ellipse).ellipse(inset_box, fill=255)
    feathered_ellipse = feathered_ellipse.filter(
        ImageFilter.GaussianBlur(HEAD_PLATE_FEATHER / 2)
    )
    feathered_ellipse = ImageChops.multiply(feathered_ellipse, outer_ellipse)
    feathered_ellipse = feathered_ellipse.point(lambda alpha: 0 if alpha < 3 else alpha)
    return ImageChops.multiply(feathered_ellipse, shared_interior)


def build_face_plate(master_path: Path, mask: Image.Image) -> Image.Image:
    master = load_canvas(master_path)
    red, green, blue, _ = master.split()
    plate = Image.merge("RGBA", (red, green, blue, mask))

    # Zero fully transparent RGB so no checker or matte color remains hidden in
    # the file and later filtering cannot resurrect it at an edge.
    transparent = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    plate = Image.composite(
        plate, transparent, mask.point(lambda alpha: 255 if alpha else 0)
    )
    plate.putalpha(mask)

    return plate


def save_png(image: Image.Image, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, optimize=True)
    print(destination)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--master-dir", type=Path, default=DEFAULT_MASTER_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    arguments = parse_args()
    master_paths = sorted(arguments.master_dir.glob("expression_*.png"))
    if not master_paths:
        raise SystemExit(f"No expression_*.png masters found in {arguments.master_dir}")

    mask = shared_head_mask()
    neutral_master = arguments.master_dir / "expression_neut.png"
    if neutral_master not in master_paths:
        raise SystemExit(f"Missing canonical neutral master: {neutral_master}")

    # Bake the new, registered neutral face into both canonical outfit bases.
    # This makes their expression area pixel-identical while preserving each
    # original body, outfit, silhouette, and public filename.
    neutral_plate = build_face_plate(neutral_master, mask)
    for source_name in ("neutral.png", "neut_uniform.png"):
        rebuilt_base = Image.alpha_composite(
            load_canvas(SPRITE_DIR / source_name), neutral_plate
        )
        save_png(rebuilt_base, arguments.output_dir / source_name)

    # Neutral lives in the rebuilt bases, just as it does in Asahina's bank.
    save_png(
        Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0)),
        arguments.output_dir / "face_neut.png",
    )

    for master_path in master_paths:
        expression = master_path.stem.removeprefix("expression_")
        if expression == "neut":
            continue
        destination = arguments.output_dir / f"face_{expression}.png"
        save_png(build_face_plate(master_path, mask), destination)


if __name__ == "__main__":
    main()
