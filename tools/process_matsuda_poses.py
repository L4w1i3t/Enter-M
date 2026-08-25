"""Key Matsuda's generated pose masters and build visual-review artifacts.

The five image-generation masters deliberately use a saturated magenta field.
This script converts that field to real transparency without eroding the
one-pixel hair and line-art details.  The matte is derived from magenta chroma,
then the background contribution is removed from partially transparent pixels
so that edges remain clean over light, dark, and checkerboard backgrounds.

Production-sized RGBA files are written to ``tmp/matsuda_sprite_redo/poses``.
Nothing in ``game/`` is modified by this tool.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = PROJECT_ROOT / "tmp" / "matsuda_sprite_redo" / "generated"
OUTPUT_DIR = PROJECT_ROOT / "tmp" / "matsuda_sprite_redo" / "poses"
REVIEW_DIR = OUTPUT_DIR / "_review"
CANVAS_SIZE = (1023, 1537)

POSES = (
    ("pose_shrug_uniform_magenta.png", "pose_shrug_uniform.png", "Uniform shrug"),
    (
        "pose_facepalm_uniform_magenta.png",
        "pose_facepalm_uniform.png",
        "Uniform facepalm",
    ),
    ("pose_chuuni_uniform_magenta.png", "pose_chuuni_uniform.png", "Uniform chuuni"),
    (
        "pose_laughing_uniform_magenta.png",
        "pose_laughing_uniform.png",
        "Uniform laughing",
    ),
    (
        "pose_laughing_casual_magenta.png",
        "pose_laughing_casual.png",
        "Casual laughing",
    ),
)

# Chroma-key constants are intentionally fixed so repeated runs are byte-stable.
# They are expressed relative to the background sampled from each source rather
# than hard-coding a single RGB value: image generation produced five slightly
# different, but uniformly saturated, magenta fields.
FOREGROUND_CHROMA_FLOOR = 18.0
RAW_ALPHA_FLOOR = 0.035
OPAQUE_ALPHA_CEILING = 0.985
BACKGROUND_RED_BLUE_TOLERANCE = 22.0
BACKGROUND_GREEN_TOLERANCE = 24.0
BACKGROUND_CHROMA_TOLERANCE = 35.0
DETACHED_COMPONENT_MIN_AREA = 3
DETACHED_COMPONENT_MIN_ALPHA = 0.72


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_rgb(path: Path) -> np.ndarray:
    if not path.is_file():
        raise FileNotFoundError(path)
    with Image.open(path) as image:
        if image.size != CANVAS_SIZE:
            raise ValueError(f"{path}: got {image.size}, expected {CANVAS_SIZE}")
        return np.asarray(image.convert("RGB"), dtype=np.uint8).copy()


def estimate_background(rgb: np.ndarray) -> np.ndarray:
    """Return a robust RGB estimate from the clear upper-corner field."""

    height, width = rgb.shape[:2]
    sample_height = max(32, height // 12)
    sample_width = max(32, width // 10)
    samples = np.concatenate(
        (
            rgb[:sample_height, :sample_width].reshape(-1, 3),
            rgb[:sample_height, -sample_width:].reshape(-1, 3),
        )
    ).astype(np.float32)
    chroma = np.minimum(samples[:, 0], samples[:, 2]) - samples[:, 1]
    # Selecting the upper part of the chroma distribution excludes any stray
    # anti-aliased hair tip that happens to enter an upper corner.
    candidates = samples[chroma >= np.percentile(chroma, 70.0)]
    background = np.median(candidates, axis=0).astype(np.float32)
    background_chroma = min(background[0], background[2]) - background[1]
    if background_chroma < 150.0:
        raise ValueError(
            "Source does not contain the expected saturated magenta background: "
            f"sampled RGB {background.astype(int).tolist()}"
        )
    return background


def connected_component_filter(
    alpha: np.ndarray,
) -> tuple[np.ndarray, int, int, int]:
    """Discard background flecks while retaining real detached fine lines.

    No dilation, erosion, or contour simplification is performed.  The largest
    component is always retained, while a detached component survives when it
    contains at least three pixels and one confidently foreground pixel.  This
    keeps authored hair strands without admitting low-alpha magenta noise.
    """

    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        (alpha > 0.0).astype(np.uint8), connectivity=8
    )
    if count <= 1:
        raise ValueError("Chroma key produced no foreground components")

    components: list[tuple[int, int, float]] = []
    for label in range(1, count):
        values = alpha[labels == label]
        components.append((label, int(stats[label, cv2.CC_STAT_AREA]), float(values.max())))

    largest_label = max(components, key=lambda item: item[1])[0]
    kept_labels = [
        label
        for label, area, maximum in components
        if label == largest_label
        or (
            area >= DETACHED_COMPONENT_MIN_AREA
            and maximum >= DETACHED_COMPONENT_MIN_ALPHA
        )
    ]
    keep = np.isin(labels, kept_labels)
    filtered = alpha.copy()
    discarded_pixels = int(np.count_nonzero(filtered > 0.0) - np.count_nonzero(keep))
    filtered[~keep] = 0.0
    return filtered, count - 1, len(kept_labels), discarded_pixels


def key_pose(rgb_u8: np.ndarray) -> tuple[np.ndarray, dict[str, object]]:
    rgb = rgb_u8.astype(np.float32)
    background = estimate_background(rgb_u8)
    background_chroma = float(min(background[0], background[2]) - background[1])
    denominator = background_chroma - FOREGROUND_CHROMA_FLOOR
    if denominator <= 0.0:
        raise ValueError(f"Invalid background chroma denominator: {denominator}")

    chroma = np.minimum(rgb[:, :, 0], rgb[:, :, 2]) - rgb[:, :, 1]
    raw_alpha = np.clip(
        (background_chroma - chroma) / denominator,
        0.0,
        1.0,
    )

    # Fully clear pixels satisfy both RGB proximity and chroma proximity.  This
    # removes the generated field's tiny spatial texture before component
    # analysis, but deliberately leaves mixed edge pixels for matte recovery.
    definite_background = (
        (rgb[:, :, 0] >= background[0] - BACKGROUND_RED_BLUE_TOLERANCE)
        & (rgb[:, :, 2] >= background[2] - BACKGROUND_RED_BLUE_TOLERANCE)
        & (rgb[:, :, 1] <= background[1] + BACKGROUND_GREEN_TOLERANCE)
        & (chroma >= background_chroma - BACKGROUND_CHROMA_TOLERANCE)
    )
    alpha = raw_alpha.copy()
    alpha[definite_background] = 0.0
    alpha[alpha < RAW_ALPHA_FLOOR] = 0.0
    alpha[alpha > OPAQUE_ALPHA_CEILING] = 1.0
    alpha, component_count, kept_component_count, discarded_pixels = (
        connected_component_filter(alpha)
    )

    # Invert C = alpha * F + (1 - alpha) * B for every surviving pixel.  This
    # is the crucial despill step: simply deleting pink pixels would leave a
    # bright magenta halo around red hair, white gloves, and shirt cuffs.
    foreground = np.zeros_like(rgb)
    visible = alpha > 0.0
    foreground[visible] = (
        rgb[visible] - (1.0 - alpha[visible, None]) * background
    ) / alpha[visible, None]
    foreground = np.clip(np.rint(foreground), 0.0, 255.0).astype(np.uint8)
    alpha_u8 = np.rint(alpha * 255.0).astype(np.uint8)

    rgba = np.dstack((foreground, alpha_u8))
    rgba[alpha_u8 == 0, :3] = 0
    visible_u8 = alpha_u8 > 0
    if not np.any(visible_u8):
        raise ValueError("Chroma key produced an empty sprite")
    if np.all(visible_u8):
        raise ValueError("Chroma key left the entire canvas opaque")

    y, x = np.where(visible_u8)
    output_chroma = (
        np.minimum(rgba[:, :, 0].astype(np.int16), rgba[:, :, 2].astype(np.int16))
        - rgba[:, :, 1].astype(np.int16)
    )
    hidden_rgb_pixels = int(
        np.count_nonzero(np.any(rgba[:, :, :3] != 0, axis=2) & ~visible_u8)
    )
    if hidden_rgb_pixels:
        raise AssertionError(f"Hidden RGB was not cleared: {hidden_rgb_pixels} pixels")

    metrics: dict[str, object] = {
        "sampled_background_rgb": [int(round(value)) for value in background],
        "sampled_background_chroma": round(background_chroma, 4),
        "alpha_bbox_exclusive": [
            int(x.min()),
            int(y.min()),
            int(x.max()) + 1,
            int(y.max()) + 1,
        ],
        "visible_pixels": int(np.count_nonzero(visible_u8)),
        "opaque_pixels": int(np.count_nonzero(alpha_u8 == 255)),
        "semitransparent_pixels": int(
            np.count_nonzero((alpha_u8 > 0) & (alpha_u8 < 255))
        ),
        "transparent_pixels": int(np.count_nonzero(alpha_u8 == 0)),
        "hidden_rgb_pixels": hidden_rgb_pixels,
        "visible_high_magenta_pixels": int(
            np.count_nonzero(visible_u8 & (output_chroma > 40))
        ),
        "source_components": component_count,
        "kept_components": kept_component_count,
        "discarded_noise_pixels": discarded_pixels,
        "alpha_on_borders": {
            "top": int(np.count_nonzero(alpha_u8[0, :])),
            "bottom": int(np.count_nonzero(alpha_u8[-1, :])),
            "left": int(np.count_nonzero(alpha_u8[:, 0])),
            "right": int(np.count_nonzero(alpha_u8[:, -1])),
        },
    }
    return rgba, metrics


def save_rgba(path: Path, rgba: np.ndarray) -> None:
    clean = rgba.copy()
    clean[clean[:, :, 3] == 0, :3] = 0
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(clean, "RGBA").save(path, optimize=True)


def checkerboard(size: tuple[int, int], tile: int = 32) -> Image.Image:
    width, height = size
    yy, xx = np.indices((height, width))
    cells = (xx // tile + yy // tile) % 2
    colors = np.array(((224, 224, 224), (174, 174, 174)), dtype=np.uint8)
    return Image.fromarray(colors[cells], "RGB").convert("RGBA")


def make_contact_sheet(
    sprites: list[tuple[str, np.ndarray]], background_name: str
) -> Image.Image:
    columns = 3
    rows = 2
    cell_width = 330
    cell_height = 510
    padding = 15
    label_height = 34
    maximum_sprite = (cell_width - 2 * padding, cell_height - label_height - 2 * padding)

    if background_name == "light":
        background_factory = lambda: Image.new("RGBA", CANVAS_SIZE, (238, 235, 228, 255))
        sheet_color = (220, 217, 210)
        text_color = (24, 26, 34)
    elif background_name == "dark":
        background_factory = lambda: Image.new("RGBA", CANVAS_SIZE, (24, 26, 34, 255))
        sheet_color = (13, 15, 21)
        text_color = (238, 238, 242)
    elif background_name == "checker":
        background_factory = lambda: checkerboard(CANVAS_SIZE)
        sheet_color = (146, 146, 146)
        text_color = (20, 20, 20)
    else:
        raise ValueError(background_name)

    sheet = Image.new("RGB", (columns * cell_width, rows * cell_height), sheet_color)
    draw = ImageDraw.Draw(sheet)
    for index, (label, rgba) in enumerate(sprites):
        row, column = divmod(index, columns)
        cell_x = column * cell_width
        cell_y = row * cell_height
        sprite = Image.fromarray(rgba, "RGBA")
        rendered = Image.alpha_composite(background_factory(), sprite).convert("RGB")
        rendered.thumbnail(maximum_sprite, Image.Resampling.LANCZOS)
        image_x = cell_x + (cell_width - rendered.width) // 2
        image_y = cell_y + label_height + (cell_height - label_height - rendered.height) // 2
        sheet.paste(rendered, (image_x, image_y))
        draw.text((cell_x + padding, cell_y + 10), label, fill=text_color)
    return sheet


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)

    sprites: list[tuple[str, np.ndarray]] = []
    report: dict[str, object] = {
        "schema_version": 1,
        "canvas_size": list(CANVAS_SIZE),
        "algorithm": {
            "foreground_chroma_floor": FOREGROUND_CHROMA_FLOOR,
            "raw_alpha_floor": RAW_ALPHA_FLOOR,
            "opaque_alpha_ceiling": OPAQUE_ALPHA_CEILING,
            "background_red_blue_tolerance": BACKGROUND_RED_BLUE_TOLERANCE,
            "background_green_tolerance": BACKGROUND_GREEN_TOLERANCE,
            "background_chroma_tolerance": BACKGROUND_CHROMA_TOLERANCE,
            "detached_component_min_area": DETACHED_COMPONENT_MIN_AREA,
            "detached_component_min_alpha": DETACHED_COMPONENT_MIN_ALPHA,
            "morphology": "none",
            "edge_decontamination": "inverse alpha composite against sampled background",
        },
        "poses": {},
    }

    for source_name, output_name, label in POSES:
        source_path = SOURCE_DIR / source_name
        output_path = OUTPUT_DIR / output_name
        rgba, metrics = key_pose(load_rgb(source_path))
        save_rgba(output_path, rgba)
        metrics.update(
            {
                "input": str(source_path.relative_to(PROJECT_ROOT)),
                "output": str(output_path.relative_to(PROJECT_ROOT)),
                "input_sha256": sha256(source_path),
                "output_sha256": sha256(output_path),
            }
        )
        report["poses"][output_name] = metrics
        sprites.append((label, rgba))
        print(
            f"{output_name}: {metrics['visible_pixels']} visible pixels, "
            f"bbox {metrics['alpha_bbox_exclusive']}"
        )

    for background_name in ("light", "dark", "checker"):
        review_path = REVIEW_DIR / f"matsuda_poses_{background_name}.png"
        make_contact_sheet(sprites, background_name).save(review_path, optimize=True)

    metrics_path = OUTPUT_DIR / "pose_metrics.json"
    metrics_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Metrics: {metrics_path}")
    print(f"Reviews: {REVIEW_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
