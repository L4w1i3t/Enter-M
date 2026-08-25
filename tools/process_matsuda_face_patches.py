"""Build Matsuda's neutral-base expression patches and visual review sheets.

The runtime bases are the canonical ``neutral.png`` and ``neut_uniform.png``
sprites.  Every non-neutral expression is exported twice on the same
1023x1537 canvas, once registered to each outfit, under one fixed feathered
mask per outfit.  The damaged featureless bases are never used as RGB donors.

Most expression masters come from the recovered full-face source plates that
predate the feature-fragment runtime.  Crying and shocked use their original
full generated sources, while disgusted uses its later replacement source.
Those three sources already share Matsuda's canonical framing and only need
canvas normalization before the same fixed-mask export path is applied.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SPRITE_DIR = PROJECT_ROOT / "game" / "mod_assets" / "char_sprites" / "matsuda"
RECOVERED_DIR = (
    PROJECT_ROOT
    / "tmp"
    / "sprite_review"
    / "recovered_layers"
    / "matsuda_faces_named"
)
GENERATED_ROOT = Path(r"C:\Users\Admin\.codex\generated_images")
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "tmp" / "matsuda_sprite_redo" / "faces"

CANVAS_SIZE = (1023, 1537)
EXPRESSIONS = (
    "neut",
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

GENERATED_MASTERS = {
    "crying": GENERATED_ROOT
    / "019ffe3c-4463-7322-805c-4ff8a6580355"
    / "exec-b3189aa9-f8e6-404f-8517-8890520ba632.png",
    "shocked": GENERATED_ROOT
    / "019ffe3c-4463-7322-805c-4ff8a6580355"
    / "exec-c2ed0b8e-99db-47bf-bc2f-358617c2cf1e.png",
    "disgusted": PROJECT_ROOT
    / "tmp"
    / "sprite_review"
    / "matsuda_disgusted_generated.png",
}

OUTFITS = {
    "casual": "neutral.png",
    "uniform": "neut_uniform.png",
}

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def load_rgba(path: Path, size: tuple[int, int] = CANVAS_SIZE) -> np.ndarray:
    if not path.is_file():
        raise FileNotFoundError(path)
    with Image.open(path) as image:
        normalized = image.convert("RGBA")
        if normalized.size != size:
            normalized = normalized.resize(size, Image.Resampling.LANCZOS)
        return np.asarray(normalized, dtype=np.uint8).copy()


def save_rgba(path: Path, rgba: np.ndarray) -> None:
    clean = np.asarray(rgba, dtype=np.uint8).copy()
    clean[clean[:, :, 3] == 0, :3] = 0
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(clean, "RGBA").save(path, optimize=True)


def alpha_composite(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    return np.asarray(
        Image.alpha_composite(
            Image.fromarray(base, "RGBA"), Image.fromarray(overlay, "RGBA")
        ),
        dtype=np.uint8,
    )


def green_iris_centers(rgba: np.ndarray) -> np.ndarray:
    rgb = rgba[:, :, :3]
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    height, width = rgba.shape[:2]
    yy, xx = np.indices((height, width))
    allowed = (
        (xx >= 330)
        & (xx < 590)
        & (yy >= 220)
        & (yy < 410)
        & (rgba[:, :, 3] >= 192)
    )
    green = (
        allowed
        & (hsv[:, :, 0] >= 30)
        & (hsv[:, :, 0] <= 85)
        & (hsv[:, :, 1] >= 60)
        & (hsv[:, :, 2] >= 50)
    )
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(
        green.astype(np.uint8), connectivity=8
    )
    components: list[tuple[int, float, float]] = []
    for label in range(1, count):
        area = int(stats[label, cv2.CC_STAT_AREA])
        if 100 <= area <= 900:
            components.append(
                (area, float(centroids[label, 0]), float(centroids[label, 1]))
            )
    if len(components) < 2:
        raise RuntimeError(f"Expected two green irises, found {components}")
    chosen = sorted(components, reverse=True)[:2]
    chosen.sort(key=lambda component: component[1])
    return np.asarray([[item[1], item[2]] for item in chosen], dtype=np.float64)


def similarity_from_two_points(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    source_vector = source[1] - source[0]
    target_vector = target[1] - target[0]
    scale = float(np.linalg.norm(target_vector) / np.linalg.norm(source_vector))
    angle = math.atan2(target_vector[1], target_vector[0]) - math.atan2(
        source_vector[1], source_vector[0]
    )
    cosine = math.cos(angle) * scale
    sine = math.sin(angle) * scale
    linear = np.asarray(((cosine, -sine), (sine, cosine)), dtype=np.float64)
    translation = target[0] - linear @ source[0]
    return np.column_stack((linear, translation)).astype(np.float32)


def warp_rgba(rgba: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    return cv2.warpAffine(
        rgba,
        matrix,
        CANVAS_SIZE,
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0, 0),
    )


def fixed_patch_alpha(neutral_source: np.ndarray) -> np.ndarray:
    binary = (neutral_source[:, :, 3] >= 128).astype(np.uint8)
    # Feather inward so no hidden RGB beyond the recovered source footprint is
    # ever exposed.  A six-pixel solid-to-clear transition survives Ren'Py's
    # 640x960 downsample without creating a visible rectangular plate.
    distance = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
    alpha = np.clip(np.rint(distance / 6.0 * 255.0), 0, 255).astype(np.uint8)
    alpha[neutral_source[:, :, 3] == 0] = 0
    return alpha


def smooth_color_delta(target: np.ndarray, source: np.ndarray) -> np.ndarray:
    delta = target[:, :, :3].astype(np.float32) - source[:, :, :3].astype(np.float32)
    delta = cv2.GaussianBlur(delta, (0, 0), sigmaX=5.0, sigmaY=5.0)
    return np.clip(delta, -24.0, 24.0)


def checker(size: tuple[int, int], tile: int = 16) -> Image.Image:
    width, height = size
    yy, xx = np.indices((height, width))
    cells = ((xx // tile) + (yy // tile)) % 2
    rgb = np.empty((height, width, 3), dtype=np.uint8)
    rgb[cells == 0] = (78, 81, 88)
    rgb[cells == 1] = (116, 120, 128)
    return Image.fromarray(rgb, "RGB")


def font(size: int) -> ImageFont.ImageFont:
    for candidate in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def make_review(output_dir: Path, bases: dict[str, np.ndarray]) -> None:
    columns = 4
    rows = math.ceil(len(EXPRESSIONS) / columns)
    thumb_size = (256, 384)
    label_height = 30
    head_size = (300, 300)
    head_label_height = 30
    review_dir = output_dir / "_review"
    review_dir.mkdir(parents=True, exist_ok=True)

    for outfit, base in bases.items():
        for background_name, background_factory in (
            ("light", lambda: Image.new("RGB", CANVAS_SIZE, (238, 235, 228))),
            ("dark", lambda: Image.new("RGB", CANVAS_SIZE, (24, 26, 34))),
            ("checker", lambda: checker(CANVAS_SIZE)),
        ):
            sheet = Image.new(
                "RGB",
                (columns * thumb_size[0], rows * (thumb_size[1] + label_height)),
                (31, 33, 38),
            )
            heads = Image.new(
                "RGB",
                (columns * head_size[0], rows * (head_size[1] + head_label_height)),
                (31, 33, 38),
            )
            sheet_draw = ImageDraw.Draw(sheet)
            head_draw = ImageDraw.Draw(heads)
            for index, expression in enumerate(EXPRESSIONS):
                layer = load_rgba(
                    output_dir / f"face_{expression}_{outfit}.png"
                )
                sprite = alpha_composite(base, layer)
                background = background_factory().convert("RGBA")
                rendered = Image.alpha_composite(
                    background, Image.fromarray(sprite, "RGBA")
                ).convert("RGB")

                thumb = rendered.copy()
                thumb.thumbnail(thumb_size, Image.Resampling.LANCZOS)
                column = index % columns
                row = index // columns
                cell_x = column * thumb_size[0]
                cell_y = row * (thumb_size[1] + label_height)
                sheet.paste(
                    thumb,
                    (
                        cell_x + (thumb_size[0] - thumb.width) // 2,
                        cell_y + thumb_size[1] - thumb.height,
                    ),
                )
                sheet_draw.text(
                    (cell_x + 6, cell_y + thumb_size[1] + 3),
                    expression,
                    fill=(235, 235, 238),
                    font=font(18),
                )

                head = rendered.crop((315, 185, 610, 480))
                head.thumbnail(head_size, Image.Resampling.LANCZOS)
                head_x = column * head_size[0]
                head_y = row * (head_size[1] + head_label_height)
                heads.paste(
                    head,
                    (
                        head_x + (head_size[0] - head.width) // 2,
                        head_y + head_size[1] - head.height,
                    ),
                )
                head_draw.text(
                    (head_x + 6, head_y + head_size[1] + 3),
                    expression,
                    fill=(235, 235, 238),
                    font=font(18),
                )

            sheet.save(
                review_dir / f"matsuda_{outfit}_faces_{background_name}.png",
                optimize=True,
            )
            heads.save(
                review_dir / f"matsuda_{outfit}_heads_{background_name}.png",
                optimize=True,
            )


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    bases = {
        outfit: load_rgba(SPRITE_DIR / filename)
        for outfit, filename in OUTFITS.items()
    }
    uniform = bases["uniform"]
    casual = bases["casual"]
    uniform_eyes = green_iris_centers(uniform)
    casual_eyes = green_iris_centers(casual)
    outfit_matrices = {
        "uniform": np.eye(2, 3, dtype=np.float32),
        "casual": similarity_from_two_points(uniform_eyes, casual_eyes),
    }

    neutral_source = load_rgba(RECOVERED_DIR / "face_neut.png")
    uniform_alpha = fixed_patch_alpha(neutral_source)
    uniform_base_warped = uniform
    casual_base_from_uniform = warp_rgba(uniform, outfit_matrices["casual"])
    color_deltas = {
        "uniform": np.zeros((*uniform.shape[:2], 3), dtype=np.float32),
        "casual": smooth_color_delta(casual, casual_base_from_uniform),
    }

    transparent = np.zeros((CANVAS_SIZE[1], CANVAS_SIZE[0], 4), dtype=np.uint8)
    report: dict[str, object] = {
        "schema_version": 1,
        "canvas_size": list(CANVAS_SIZE),
        "runtime_bases": {
            outfit: str(SPRITE_DIR / filename)
            for outfit, filename in OUTFITS.items()
        },
        "expressions": list(EXPRESSIONS),
        "uniform_eye_centers": uniform_eyes.round(4).tolist(),
        "casual_eye_centers": casual_eyes.round(4).tolist(),
        "outfit_matrices": {
            key: value.astype(float).tolist()
            for key, value in outfit_matrices.items()
        },
        "layers": {},
    }

    for outfit in OUTFITS:
        save_rgba(args.output_dir / f"face_neut_{outfit}.png", transparent)

    for expression in EXPRESSIONS[1:]:
        source_path = RECOVERED_DIR / f"face_{expression}.png"
        registration: dict[str, object]
        if source_path.is_file():
            master = load_rgba(source_path)
            registration = {"kind": "already_registered", "path": str(source_path)}
        else:
            generated_path = GENERATED_MASTERS[expression]
            master = load_rgba(generated_path)
            registration = {
                "kind": "normalized_generated_master",
                "path": str(generated_path),
            }

        expression_report: dict[str, object] = {"source": registration, "outfits": {}}
        for outfit in OUTFITS:
            matrix = outfit_matrices[outfit]
            warped_master = warp_rgba(master, matrix)
            warped_alpha = cv2.warpAffine(
                uniform_alpha,
                matrix,
                CANVAS_SIZE,
                flags=cv2.INTER_LANCZOS4,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=0,
            )
            # Never let the fixed face plate expand the outfit silhouette.
            # The slight uniform-to-casual registration transform can otherwise
            # leave a handful of feather pixels just beyond the casual base.
            warped_alpha[bases[outfit][:, :, 3] == 0] = 0
            corrected_rgb = np.clip(
                warped_master[:, :, :3].astype(np.float32) + color_deltas[outfit],
                0,
                255,
            ).astype(np.uint8)
            layer = np.dstack((corrected_rgb, warped_alpha))
            layer[warped_alpha == 0, :3] = 0
            destination = args.output_dir / f"face_{expression}_{outfit}.png"
            save_rgba(destination, layer)
            alpha_bbox = Image.fromarray(warped_alpha).getbbox()
            expression_report["outfits"][outfit] = {
                "path": str(destination),
                "alpha_bbox": list(alpha_bbox) if alpha_bbox else None,
                "nonzero_alpha_pixels": int((warped_alpha > 0).sum()),
                "partial_alpha_pixels": int(
                    ((warped_alpha > 0) & (warped_alpha < 255)).sum()
                ),
                "opaque_alpha_pixels": int((warped_alpha == 255).sum()),
            }
        report["layers"][expression] = expression_report

    (args.output_dir / "metrics.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    make_review(args.output_dir, bases)
    print(
        f"Built {len(EXPRESSIONS) * len(OUTFITS)} Matsuda face layers in "
        f"{args.output_dir}"
    )
    print(f"Metrics: {args.output_dir / 'metrics.json'}")
    print(f"Reviews: {args.output_dir / '_review'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
