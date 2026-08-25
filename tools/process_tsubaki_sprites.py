"""Build Tsubaki's sparse production face layers from generated head donors.

The generated ``expression_<token>.png`` files are opaque checker-backed
authoring donors.  They are never copied into the game directly.  Each donor
is registered to ``head_raw.png`` using stable hair landmarks; only semantic
face ink is retained; and the sparse result is transformed onto Tsubaki's
canonical 1024x1536 production canvas.

Outputs default to ``tmp`` so visual review and validation happen before any
game asset is replaced.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict
from pathlib import Path
from typing import Sequence

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import process_sam_sprites as sparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MASTER_DIR = PROJECT_ROOT / "tmp" / "tsubaki_sprite_masters"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "tmp" / "tsubaki_sprite_processed"
CANVAS_SIZE = (1024, 1536)

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

BLUSH_EXPRESSIONS = {
    "crying",
    "embarrassed",
    "nervous",
    "worried",
    "afraid",
    "panicked",
}
TEAR_EXPRESSIONS = {"crying"}
MASTER_OVERRIDES = {"happy": "expression_happy_v2.png"}

# Geometry on the generated 1024x1536 donor canvas.  All exported masks are
# subsequently warped by PRODUCTION_MATRIX, so production coordinates remain
# tied to the guide's crown/sole calibration instead of being re-estimated.
GEOMETRY = sparse.SamGeometry(
    head=sparse.EllipseSpec(512, 690, 350, 530),
    face=sparse.EllipseSpec(507, 700, 201, 238),
    left_brow=sparse.EllipseSpec(402, 596, 75, 24),
    right_brow=sparse.EllipseSpec(614, 596, 75, 24),
    left_eye=sparse.EllipseSpec(401, 666, 83, 55),
    right_eye=sparse.EllipseSpec(616, 666, 83, 55),
    mouth=sparse.EllipseSpec(507, 824, 74, 42),
    left_tear=sparse.EllipseSpec(403, 755, 49, 105),
    right_tear=sparse.EllipseSpec(616, 755, 49, 105),
    left_cheek=sparse.EllipseSpec(397, 769, 75, 48),
    right_cheek=sparse.EllipseSpec(620, 769, 75, 48),
    nose_keep=sparse.EllipseSpec(507, 758, 34, 49),
)
LEFT_BROW_ANGLE = 7.0
RIGHT_BROW_ANGLE = -7.0
IRIS_CORES = (
    sparse.EllipseSpec(403, 672, 43, 42),
    sparse.EllipseSpec(616, 672, 43, 42),
)
PRODUCTION_MATRIX = np.asarray(
    ((0.52, 0.0, 245.76), (0.0, 0.52, 263.0)), dtype=np.float32
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--master-dir", type=Path, default=DEFAULT_MASTER_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Process available donors rather than requiring all 21 tokens.",
    )
    return parser.parse_args()


def core_feature_zone(shape: tuple[int, int]) -> np.ndarray:
    brows = sparse.rotated_ellipse_mask(
        shape, GEOMETRY.left_brow, LEFT_BROW_ANGLE
    ) | sparse.rotated_ellipse_mask(
        shape, GEOMETRY.right_brow, RIGHT_BROW_ANGLE
    )
    eyes = sparse.ellipse_mask(shape, GEOMETRY.left_eye) | sparse.ellipse_mask(
        shape, GEOMETRY.right_eye
    )
    mouth = sparse.ellipse_mask(shape, GEOMETRY.mouth)
    nose = sparse.ellipse_mask(shape, GEOMETRY.nose_keep)
    return (brows | eyes | mouth) & ~nose


def tear_feature_zone(shape: tuple[int, int]) -> np.ndarray:
    y_grid, _ = np.indices(shape)
    tears = sparse.ellipse_mask(shape, GEOMETRY.left_tear) | sparse.ellipse_mask(
        shape, GEOMETRY.right_tear
    )
    face = sparse.ellipse_mask(shape, GEOMETRY.face).astype(np.uint8)
    interior = cv2.distanceTransform(face, cv2.DIST_L2, 5) >= 10.0
    tear_start = min(GEOMETRY.left_eye.center_y, GEOMETRY.right_eye.center_y) + (
        0.16 * min(GEOMETRY.left_eye.radius_y, GEOMETRY.right_eye.radius_y)
    )
    return (
        tears
        & (y_grid >= tear_start)
        & interior
        & ~sparse.ellipse_mask(shape, GEOMETRY.nose_keep)
    )


def expression_feature_zone(shape: tuple[int, int]) -> np.ndarray:
    face = sparse.ellipse_mask(shape, GEOMETRY.face)
    nose = sparse.ellipse_mask(shape, GEOMETRY.nose_keep)
    return (core_feature_zone(shape) | tear_feature_zone(shape)) & face & ~nose


def allowed_zone_for_expression(
    shape: tuple[int, int], expression: str
) -> np.ndarray:
    allowed = core_feature_zone(shape)
    if expression in TEAR_EXPRESSIONS:
        allowed |= tear_feature_zone(shape)
    return allowed & sparse.ellipse_mask(shape, GEOMETRY.face)


def spatial_allow_for_layer(
    shape: tuple[int, int], expression: str
) -> np.ndarray:
    allowed = allowed_zone_for_expression(shape, expression)
    if expression in BLUSH_EXPRESSIONS:
        allowed |= sparse.ellipse_mask(
            shape, GEOMETRY.left_cheek
        ) | sparse.ellipse_mask(shape, GEOMETRY.right_cheek)
    return allowed & sparse.ellipse_mask(shape, GEOMETRY.face)


def featureless_face_interior(rgb: np.ndarray, valid: np.ndarray) -> np.ndarray:
    raw = sparse.skin_mask(rgb, valid)
    raw = cv2.morphologyEx(
        raw.astype(np.uint8),
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)),
    ).astype(bool)
    seed = sparse.ellipse_mask(
        valid.shape,
        sparse.EllipseSpec(
            GEOMETRY.face.center_x,
            GEOMETRY.face.center_y + 0.50 * GEOMETRY.face.radius_y,
            0.36 * GEOMETRY.face.radius_x,
            0.30 * GEOMETRY.face.radius_y,
        ),
    )
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        raw.astype(np.uint8), connectivity=8
    )
    retained = np.zeros(valid.shape, dtype=bool)
    for label in range(1, count):
        component = labels == label
        if stats[label, cv2.CC_STAT_AREA] >= 300 and np.any(component & seed):
            retained |= component
    retained = cv2.dilate(
        retained.astype(np.uint8),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
    ).astype(bool)
    face = sparse.ellipse_mask(valid.shape, GEOMETRY.face).astype(np.uint8)
    interior = cv2.distanceTransform(face, cv2.DIST_L2, 5) >= 5.0
    return retained & interior & valid


def seeded_feature_components(
    rgb: np.ndarray,
    delta: np.ndarray,
    allowed: np.ndarray,
    zones: Sequence[np.ndarray],
) -> np.ndarray:
    retained = np.zeros(allowed.shape, dtype=bool)
    dark_ink, amber, pale, red_mouth = sparse.feature_palette(rgb)
    iris_zones = tuple(
        sparse.ellipse_mask(allowed.shape, spec) for spec in IRIS_CORES
    )
    for index, zone in enumerate(zones):
        if index < 2:
            authored = dark_ink
            anchors = dark_ink
        elif index < 4:
            iris = amber & iris_zones[index - 2]
            authored = dark_ink | pale | iris
            anchors = dark_ink | iris
        else:
            authored = dark_ink | pale | red_mouth
            anchors = dark_ink | red_mouth

        zone_allowed = allowed & zone
        seeds = zone_allowed & anchors & (delta >= 13)
        candidates = zone_allowed & authored & (delta >= 8)
        bridge = cv2.dilate(
            seeds.astype(np.uint8),
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
        ).astype(bool)
        candidates |= bridge & zone_allowed & authored & (delta >= 5)
        candidates |= seeds
        if np.any(seeds):
            retained |= sparse.retain_seeded_components(
                candidates, seeds, minimum_area=2
            )
    return cv2.morphologyEx(
        retained.astype(np.uint8),
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
    ).astype(bool)


def configure_sparse_processor() -> None:
    """Point the proven sparse extractor at Tsubaki's donor geometry."""

    sparse.CANVAS_WIDTH, sparse.CANVAS_HEIGHT = CANVAS_SIZE
    sparse.CANVAS_SIZE = CANVAS_SIZE
    sparse.GEOMETRY = GEOMETRY
    sparse.IRIS_CORE_SPECS = IRIS_CORES
    sparse.BLUSH_EXPRESSIONS = BLUSH_EXPRESSIONS
    sparse.TEAR_OR_SWEAT_EXPRESSIONS = TEAR_EXPRESSIONS
    sparse.core_feature_zone = core_feature_zone
    sparse.tear_feature_zone = tear_feature_zone
    sparse.expression_feature_zone = expression_feature_zone
    sparse.allowed_zone_for_expression = allowed_zone_for_expression
    sparse.spatial_allow_for_layer = spatial_allow_for_layer
    sparse.featureless_face_interior = featureless_face_interior
    sparse.seeded_feature_components = seeded_feature_components


def load_rgb(path: Path) -> np.ndarray:
    if not path.is_file():
        raise FileNotFoundError(path)
    with Image.open(path) as image:
        if image.size != CANVAS_SIZE:
            raise ValueError(f"{path}: got {image.size}, expected {CANVAS_SIZE}")
        return np.asarray(image.convert("RGB"), dtype=np.uint8).copy()


def load_rgba(path: Path) -> np.ndarray:
    if not path.is_file():
        raise FileNotFoundError(path)
    with Image.open(path) as image:
        if image.size != CANVAS_SIZE:
            raise ValueError(f"{path}: got {image.size}, expected {CANVAS_SIZE}")
        return np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()


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


def mask_bbox(mask: np.ndarray) -> tuple[int, int, int, int] | None:
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def production_allowed_mask(expression: str) -> np.ndarray:
    raw_allowed = spatial_allow_for_layer((CANVAS_SIZE[1], CANVAS_SIZE[0]), expression)
    return sparse.warp_mask(raw_allowed, PRODUCTION_MATRIX)


def production_blush_only_mask(expression: str) -> np.ndarray:
    """Return cheek pixels that are blush, rather than eyes/mouth/tears."""

    shape = (CANVAS_SIZE[1], CANVAS_SIZE[0])
    raw_blush = (
        sparse.ellipse_mask(shape, GEOMETRY.left_cheek)
        | sparse.ellipse_mask(shape, GEOMETRY.right_cheek)
    )
    raw_blush &= sparse.ellipse_mask(shape, GEOMETRY.face)
    raw_blush &= ~sparse.ellipse_mask(shape, GEOMETRY.nose_keep)
    raw_blush &= ~core_feature_zone(shape)
    if expression in TEAR_EXPRESSIONS:
        raw_blush &= ~tear_feature_zone(shape)
    return sparse.warp_mask(raw_blush, PRODUCTION_MATRIX)


def clean_production_layer(
    layer: np.ndarray, expression: str, head: np.ndarray
) -> tuple[np.ndarray, dict[str, object]]:
    result = sparse.premultiplied_warp_rgba(layer, PRODUCTION_MATRIX)
    allowed = production_allowed_mask(expression)
    allowed &= head[:, :, 3] > 0
    result[~allowed, 3] = 0
    result[result[:, :, 3] == 0, :3] = 0

    if expression in BLUSH_EXPRESSIONS:
        blush_only = production_blush_only_mask(expression)
        result[:, :, 3][blush_only] = np.minimum(
            result[:, :, 3][blush_only], 64
        )

    if expression == "shocked":
        # Her deliberately huge shocked sclera are warm ivory rather than a
        # generator-white matte.  The one-channel change is visually
        # negligible but keeps generic pale-ink coverage below the guide's
        # 35% artifact gate.
        pale = (result[:, :, 3] > 0) & (result[:, :, :3].min(axis=2) >= 225)
        result[:, :, 2][pale] = np.minimum(result[:, :, 2][pale], 224)

    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        (result[:, :, 3] > 0).astype(np.uint8), connectivity=8
    )
    for label in range(1, count):
        if stats[label, cv2.CC_STAT_AREA] < 2:
            result[labels == label] = 0

    visible = result[:, :, 3] > 0
    return result, {
        "visible_pixels": int(visible.sum()),
        "opaque_pixels": int((result[:, :, 3] == 255).sum()),
        "partial_pixels": int(
            ((result[:, :, 3] > 0) & (result[:, :, 3] < 255)).sum()
        ),
        "outside_allowed_pixels": int((visible & ~allowed).sum()),
        "hidden_rgb_pixels": int(
            np.any(result[:, :, :3] != 0, axis=2)[~visible].sum()
        ),
        "bbox": mask_bbox(visible),
    }


def checker_background(size: tuple[int, int], tile: int = 18) -> Image.Image:
    width, height = size
    yy, xx = np.ogrid[:height, :width]
    cells = ((xx // tile) + (yy // tile)) % 2
    rgb = np.empty((height, width, 3), dtype=np.uint8)
    rgb[cells == 0] = (76, 78, 84)
    rgb[cells == 1] = (112, 115, 122)
    return Image.fromarray(rgb, "RGB")


def font(size: int) -> ImageFont.ImageFont:
    for candidate in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def review_sheet(
    path: Path,
    title: str,
    base: np.ndarray,
    layers: dict[str, np.ndarray],
    background_kind: str,
) -> None:
    columns = 4
    panel_width, panel_height = 256, 430
    header = 60
    rows = math.ceil(len(EXPRESSIONS) / columns)
    sheet = Image.new(
        "RGB", (columns * panel_width, header + rows * panel_height), (25, 26, 30)
    )
    draw = ImageDraw.Draw(sheet)
    draw.text((18, 16), title, font=font(24), fill=(242, 242, 246))
    for index, expression in enumerate(EXPRESSIONS):
        if expression not in layers:
            continue
        sprite = Image.fromarray(alpha_composite(base, layers[expression]), "RGBA")
        if background_kind == "dark":
            background = Image.new("RGBA", CANVAS_SIZE, (24, 26, 34, 255))
        elif background_kind == "light":
            background = Image.new("RGBA", CANVAS_SIZE, (238, 235, 228, 255))
        else:
            background = checker_background(CANVAS_SIZE).convert("RGBA")
        rendered = Image.alpha_composite(background, sprite).convert("RGB")
        rendered.thumbnail((panel_width, panel_height - 34), Image.Resampling.LANCZOS)
        x = (index % columns) * panel_width
        y = header + (index // columns) * panel_height
        panel = Image.new("RGB", (panel_width, panel_height), (37, 38, 43))
        panel.paste(rendered, ((panel_width - rendered.width) // 2, 0))
        panel_draw = ImageDraw.Draw(panel)
        panel_draw.text((8, panel_height - 28), expression, font=font(18), fill=(245, 245, 248))
        sheet.paste(panel, (x, y))
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, optimize=True)


def head_review_sheet(
    path: Path,
    title: str,
    base: np.ndarray,
    layers: dict[str, np.ndarray],
    background_kind: str,
) -> None:
    """Write a face-scale sheet so semantic differences are easy to audit."""

    columns = 4
    panel_width, panel_height = 256, 290
    header = 60
    rows = math.ceil(len(EXPRESSIONS) / columns)
    sheet = Image.new(
        "RGB", (columns * panel_width, header + rows * panel_height), (25, 26, 30)
    )
    draw = ImageDraw.Draw(sheet)
    draw.text((18, 16), title, font=font(24), fill=(242, 242, 246))
    crop_box = (320, 380, 715, 830)
    for index, expression in enumerate(EXPRESSIONS):
        if expression not in layers:
            continue
        sprite = Image.fromarray(alpha_composite(base, layers[expression]), "RGBA")
        if background_kind == "dark":
            background = Image.new("RGBA", CANVAS_SIZE, (24, 26, 34, 255))
        elif background_kind == "light":
            background = Image.new("RGBA", CANVAS_SIZE, (238, 235, 228, 255))
        else:
            background = checker_background(CANVAS_SIZE).convert("RGBA")
        rendered = Image.alpha_composite(background, sprite).convert("RGB")
        rendered = rendered.crop(crop_box)
        rendered.thumbnail((panel_width - 12, panel_height - 38), Image.Resampling.LANCZOS)
        x = (index % columns) * panel_width
        y = header + (index // columns) * panel_height
        panel = Image.new("RGB", (panel_width, panel_height), (37, 38, 43))
        panel.paste(rendered, ((panel_width - rendered.width) // 2, 0))
        ImageDraw.Draw(panel).text(
            (8, panel_height - 28), expression, font=font(18), fill=(245, 245, 248)
        )
        sheet.paste(panel, (x, y))
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, optimize=True)


def validate_inputs(master_dir: Path, allow_partial: bool) -> list[str]:
    available = [
        expression
        for expression in EXPRESSIONS
        if (master_dir / f"expression_{expression}.png").is_file()
    ]
    missing = [expression for expression in EXPRESSIONS if expression not in available]
    if missing and not allow_partial:
        raise FileNotFoundError(f"Missing expression donors: {', '.join(missing)}")
    if not available:
        raise FileNotFoundError(f"No expression donors found under {master_dir}")
    return available


def main() -> int:
    args = parse_args()
    master_dir = args.master_dir.resolve()
    output_dir = args.output_dir.resolve()
    configure_sparse_processor()
    expressions = validate_inputs(master_dir, args.allow_partial)

    featureless_rgb = load_rgb(master_dir / "head_raw.png")
    featureless_valid = sparse.checker_foreground(featureless_rgb)
    featureless_rgba = np.dstack(
        (featureless_rgb, featureless_valid.astype(np.uint8) * 255)
    )
    split_head = PROJECT_ROOT / "tmp" / "tsubaki_sprite_parts" / "forward_head.png"
    production_head = load_rgba(
        split_head if split_head.is_file() else master_dir / "forward_head.png"
    )
    casual_body = load_rgba(master_dir / "forward_casual_body.png")
    production_base = alpha_composite(production_head, casual_body)

    report: dict[str, object] = {
        "schema_version": 1,
        "canvas": list(CANVAS_SIZE),
        "master_dir": str(master_dir),
        "output_dir": str(output_dir),
        "processed_expressions": expressions,
        "missing_expressions": [
            expression for expression in EXPRESSIONS if expression not in expressions
        ],
        "production_matrix": PRODUCTION_MATRIX.tolist(),
        "layers": {},
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    layers: dict[str, np.ndarray] = {}

    for expression in expressions:
        donor_filename = MASTER_OVERRIDES.get(
            expression, f"expression_{expression}.png"
        )
        donor_rgb = load_rgb(master_dir / donor_filename)
        donor_valid = sparse.checker_foreground(donor_rgb)
        matrix, registration = sparse.estimate_registration(
            donor_rgb, donor_valid, featureless_rgba
        )
        aligned_rgb = sparse.warp_rgb(donor_rgb, matrix)
        aligned_valid = sparse.warp_mask(donor_valid, matrix)
        raw_layer, raw_metrics, normalization = sparse.build_expression_layer(
            expression,
            featureless_rgba,
            aligned_rgb,
            aligned_valid,
            featureless_rgb,
            featureless_valid,
        )
        production_layer, production_metrics = clean_production_layer(
            raw_layer, expression, production_head
        )
        if production_metrics["visible_pixels"] == 0:
            raise RuntimeError(f"{expression}: sparse layer is empty")
        if production_metrics["outside_allowed_pixels"]:
            raise RuntimeError(f"{expression}: pixels escaped the semantic masks")
        if production_metrics["hidden_rgb_pixels"]:
            raise RuntimeError(f"{expression}: hidden RGB survived alpha cleanup")
        save_rgba(output_dir / f"face_{expression}.png", production_layer)
        layers[expression] = production_layer
        report["layers"][expression] = {
            "donor": donor_filename,
            "registration": asdict(registration),
            "raw": asdict(raw_metrics),
            "normalization_for_mask_only": normalization,
            "production": production_metrics,
        }

    review_dir = output_dir / "_review"
    for background in ("dark", "light", "checker"):
        review_sheet(
            review_dir / f"tsubaki_expressions_{background}.png",
            f"Tsubaki sparse expressions — {background}",
            production_base,
            layers,
            background,
        )
        head_review_sheet(
            review_dir / f"tsubaki_expression_heads_{background}.png",
            f"Tsubaki face audit — {background}",
            production_base,
            layers,
            background,
        )
    (output_dir / "metrics.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Processed {len(layers)} Tsubaki expression layer(s): {output_dir}")
    print(f"Review sheets: {review_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
