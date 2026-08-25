"""Split Tsubaki's calibrated head into back-hair, head, and front-hair layers.

The source is already a clean full-canvas RGBA asset.  This script performs a
pixel partition (never a resynthesis): every visible source pixel is assigned to
exactly one output layer, so recomposing the three layers without a body is
pixel-exact.  The selected inner lower locks become ``hair_front``; the outer
lengths remain behind the outfit body.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = PROJECT_ROOT / "tmp" / "tsubaki_sprite_masters" / "forward_head.png"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "tmp" / "tsubaki_sprite_parts"
CANVAS_SIZE = (1024, 1536)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def polygon_mask(points: list[tuple[int, int]]) -> np.ndarray:
    image = Image.new("1", CANVAS_SIZE, 0)
    ImageDraw.Draw(image).polygon(points, fill=1)
    return np.asarray(image, dtype=bool)


def save_rgba(path: Path, rgba: np.ndarray) -> None:
    clean = rgba.copy()
    clean[clean[:, :, 3] == 0, :3] = 0
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(clean, "RGBA").save(path, optimize=True)


def alpha_composite(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    return np.asarray(
        Image.alpha_composite(Image.fromarray(base, "RGBA"), Image.fromarray(overlay, "RGBA")),
        dtype=np.uint8,
    )


def extend_neck_stub(source: np.ndarray) -> np.ndarray:
    """Extend the shared neck beneath both collars by more than forty pixels.

    The generated head ends in a curved bust cut at roughly y=830.  Tsubaki's
    casual crew neck exposes another forty pixels below that cut, while the
    uniform collar happens to hide it.  A stretched sample of the existing
    neck shading fills only this collar-underlay region; the original head is
    composited back on top unchanged.
    """

    extension = np.zeros_like(source)
    # Median across several fully opaque source-neck rows gives a stable
    # horizontal shading profile without copying any transparent edge pixels.
    sample = source[808:823, 464:561]
    profile = np.zeros((97, 3), dtype=np.float32)
    for offset in range(97):
        column = sample[:, offset]
        valid = column[:, 3] >= 240
        if np.any(valid):
            profile[offset] = np.median(column[valid, :3], axis=0)
        elif offset:
            profile[offset] = profile[offset - 1]
        else:
            profile[offset] = (248, 197, 166)
    # Fill any leading holes from the first populated sample.
    populated = np.where(np.any(profile > 0, axis=1))[0]
    if len(populated):
        profile[: populated[0]] = profile[populated[0]]

    for y in range(805, 891):
        if y <= 850:
            half_width = 48.0 + (y - 805) * (20.0 / 45.0)
        else:
            half_width = 68.0 - (y - 850) * (32.0 / 40.0)
        left = int(math.floor(512.0 - half_width))
        right = int(math.ceil(512.0 + half_width))
        xs = np.arange(left, right + 1)
        u = np.clip((xs - (512.0 - half_width)) / (2.0 * half_width), 0.0, 1.0)
        source_x = u * 96.0
        low = np.floor(source_x).astype(int)
        high = np.minimum(low + 1, 96)
        fraction = (source_x - low)[:, None]
        colors = profile[low] * (1.0 - fraction) + profile[high] * fraction
        # Preserve the source highlight while gently warming the lower chest.
        warmth = min(5.0, max(0.0, (y - 825) / 16.0))
        colors[:, 0] = np.clip(colors[:, 0] + warmth, 0, 255)
        colors[:, 2] = np.clip(colors[:, 2] + warmth * 0.35, 0, 255)
        extension[y, xs, :3] = np.rint(colors).astype(np.uint8)
        extension[y, xs, 3] = 255
        # A two-pixel soft outer edge remains hidden by either collar in normal
        # composition but prevents a hard fringe in diagnostic isolation.
        extension[y, left, 3] = 72
        extension[y, right, 3] = 72
        if right - left >= 3:
            extension[y, left + 1, 3] = 190
            extension[y, right - 1, 3] = 190

    return alpha_composite(extension, source)


def main() -> int:
    args = parse_args()
    source_path = args.source.resolve()
    output_dir = args.output_dir.resolve()
    with Image.open(source_path) as image:
        if image.size != CANVAS_SIZE:
            raise ValueError(f"{source_path}: got {image.size}, expected {CANVAS_SIZE}")
        source = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()

    source = extend_neck_stub(source)

    alpha = source[:, :, 3]
    visible = alpha > 0
    rgb = source[:, :, :3].astype(np.int16)
    red, green, blue = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
    warm_brown = (
        visible
        & (red >= 72)
        & (red >= green + 16)
        & (green >= blue + 7)
        & (blue <= 176)
        & (luminance <= 210)
    )
    warm_brown = cv2.morphologyEx(
        warm_brown.astype(np.uint8),
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)),
    ).astype(bool)
    warm_brown = cv2.dilate(
        warm_brown.astype(np.uint8),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
    ).astype(bool)

    yy, xx = np.indices((CANVAS_SIZE[1], CANVAS_SIZE[0]))
    below_bangs = yy >= 615
    outside_face_core = (((xx - 512) / 176.0) ** 2 + ((yy - 650) / 174.0) ** 2) >= 1.0
    neck_keep = (xx >= 438) & (xx <= 586) & (yy >= 685)
    detachable_hair = warm_brown & below_bangs & outside_face_core & ~neck_keep

    # Inner locks that naturally fall in front of either outfit.  The remainder
    # of the detached lengths stays behind the headless body.
    front_region = polygon_mask(
        [(373, 604), (463, 620), (497, 730), (471, 850), (419, 954), (370, 886)]
    ) | polygon_mask(
        [(548, 604), (635, 620), (688, 795), (662, 932), (600, 971), (556, 845)]
    )
    front_mask = detachable_hair & front_region
    back_mask = detachable_hair & ~front_mask
    head_mask = visible & ~detachable_hair

    # The canonical source carries most crown/side hair in the same bitmap as
    # the featureless face.  Move the safe outer hair mass into ``hair_back``
    # as a pure pixel partition: both layers render before the body, so the
    # recomposed image is unchanged, while the small wispy back layer is no
    # longer dominated by partially transparent edge pixels.  The generous
    # protected core keeps the face, ears, bangs behind expression ink, and
    # every possible tear/blush pixel fully opaque in ``head``.
    protected_head_core = (
        ((xx - 510.0) / 155.0) ** 2 + ((yy - 625.0) / 170.0) ** 2
    ) <= 1.0
    outer_hair_mass = head_mask & warm_brown & ~protected_head_core & ~neck_keep
    back_mask |= outer_hair_mass
    head_mask &= ~outer_hair_mass

    layers: dict[str, np.ndarray] = {}
    for name, mask in (
        ("forward_hair_back", back_mask),
        ("forward_head", head_mask),
        ("forward_hair_front", front_mask),
    ):
        layer = np.zeros_like(source)
        layer[mask] = source[mask]
        layer[layer[:, :, 3] == 0, :3] = 0
        layers[name] = layer
        save_rgba(output_dir / f"{name}.png", layer)

    reconstructed = alpha_composite(
        alpha_composite(layers["forward_hair_back"], layers["forward_head"]),
        layers["forward_hair_front"],
    )
    if not np.array_equal(reconstructed, source):
        changed = int(np.any(reconstructed != source, axis=2).sum())
        raise RuntimeError(f"head partition failed exact reconstruction at {changed} pixels")

    for body_name, review_name in (
        ("forward_casual_body.png", "split_casual.png"),
        ("forward_uniform_body.png", "split_uniform.png"),
    ):
        body_path = source_path.parent / body_name
        if not body_path.is_file():
            continue
        with Image.open(body_path) as body_image:
            body = np.asarray(body_image.convert("RGBA"), dtype=np.uint8).copy()
        composite = layers["forward_hair_back"]
        composite = alpha_composite(composite, layers["forward_head"])
        composite = alpha_composite(composite, body)
        composite = alpha_composite(composite, layers["forward_hair_front"])
        save_rgba(output_dir / "_review" / review_name, composite)

    print(
        "Split Tsubaki head exactly: "
        f"back={int(back_mask.sum())} head={int(head_mask.sum())} "
        f"front={int(front_mask.sum())} visible pixels"
    )
    print(f"Assets: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
