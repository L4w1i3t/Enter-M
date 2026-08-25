"""Extract Tsubaki's fixed stifled-laugh face and render pose reviews.

The failed-laugh gesture has a hand crossing the mouth, so it is represented as
an ordinary low arm, a whole-face ``special`` layer, and a raised ``arm_over``
layer.  The special first restores the canonical featureless head inside every
normal expression mask, then applies only the generated laugh ink.  That makes
the pose safe even when Ren'Py is retaining a previously selected face
attribute; skin from the generated hand and all head/hair resynthesis remain
excluded.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import numpy as np
from PIL import Image

import process_sam_sprites as sparse
import process_tsubaki_sprites as tsubaki


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MASTER_DIR = PROJECT_ROOT / "tmp" / "tsubaki_sprite_masters"
PART_DIR = PROJECT_ROOT / "tmp" / "tsubaki_sprite_parts"
FACE_DIR = PROJECT_ROOT / "tmp" / "tsubaki_sprite_processed"
CANVAS_SIZE = (1024, 1536)


def transformed_ellipse(spec: sparse.EllipseSpec) -> sparse.EllipseSpec:
    return sparse.EllipseSpec(
        245.76 + 0.52 * spec.center_x,
        263.0 + 0.52 * spec.center_y,
        0.52 * spec.radius_x,
        0.52 * spec.radius_y,
    )


def configure_production_geometry() -> None:
    raw = tsubaki.GEOMETRY
    production = sparse.SamGeometry(
        head=transformed_ellipse(raw.head),
        face=transformed_ellipse(raw.face),
        left_brow=transformed_ellipse(raw.left_brow),
        right_brow=transformed_ellipse(raw.right_brow),
        left_eye=transformed_ellipse(raw.left_eye),
        right_eye=transformed_ellipse(raw.right_eye),
        mouth=transformed_ellipse(raw.mouth),
        left_tear=transformed_ellipse(raw.left_tear),
        right_tear=transformed_ellipse(raw.right_tear),
        left_cheek=transformed_ellipse(raw.left_cheek),
        right_cheek=transformed_ellipse(raw.right_cheek),
        nose_keep=transformed_ellipse(raw.nose_keep),
    )
    tsubaki.GEOMETRY = production
    tsubaki.IRIS_CORES = tuple(transformed_ellipse(spec) for spec in tsubaki.IRIS_CORES)
    tsubaki.configure_sparse_processor()


def load_rgb(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        if image.size != CANVAS_SIZE:
            raise ValueError(f"{path}: got {image.size}, expected {CANVAS_SIZE}")
        return np.asarray(image.convert("RGB"), dtype=np.uint8).copy()


def load_rgba(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        if image.size != CANVAS_SIZE:
            raise ValueError(f"{path}: got {image.size}, expected {CANVAS_SIZE}")
        return np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()


def compose(*layers: np.ndarray) -> np.ndarray:
    result = np.zeros((CANVAS_SIZE[1], CANVAS_SIZE[0], 4), dtype=np.uint8)
    for layer in layers:
        result = np.asarray(
            Image.alpha_composite(Image.fromarray(result), Image.fromarray(layer)),
            dtype=np.uint8,
        )
    return result


def save_rgba(path: Path, rgba: np.ndarray) -> None:
    clean = rgba.copy()
    clean[clean[:, :, 3] == 0, :3] = 0
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(clean, "RGBA").save(path, optimize=True)


def main() -> int:
    configure_production_geometry()
    target = load_rgba(MASTER_DIR / "reference_casual_blank.png")
    donor_path = MASTER_DIR / "pose_stifled_laugh_casual_raw.png"
    donor_rgb = load_rgb(donor_path)
    donor_valid = sparse.checker_foreground(donor_rgb)
    matrix, registration = sparse.estimate_registration(donor_rgb, donor_valid, target)
    aligned_rgb = sparse.warp_rgb(donor_rgb, matrix)
    aligned_valid = sparse.warp_mask(donor_valid, matrix)
    target_rgb = target[:, :, :3]
    target_valid = target[:, :, 3] > 0
    layer, raw_metrics, normalization = sparse.build_expression_layer(
        "stifled_laugh",
        target,
        aligned_rgb,
        aligned_valid,
        target_rgb,
        target_valid,
    )
    allowed = tsubaki.spatial_allow_for_layer(layer.shape[:2], "stifled_laugh")
    head = load_rgba(PART_DIR / "forward_head.png")
    allowed &= head[:, :, 3] > 0
    # The source hand overlaps the viewer-left half of the grin.  Warm shaded
    # knuckle pixels can satisfy a generic red-mouth palette, so retain only
    # the exposed upper/right smile segment; the raised arm supplies the
    # occluding hand above this layer.
    yy, xx = np.indices(layer.shape[:2])
    mouth_zone = sparse.ellipse_mask(layer.shape[:2], tsubaki.GEOMETRY.mouth)
    # The reliable authored smile is the upper viewer-right segment.  The
    # lower/central pale component belongs to the generated knuckles and turns
    # into a conspicuous white spur once the real arm is composited.
    exposed_smile = (xx >= 506) & (yy <= 699)
    allowed &= ~mouth_zone | exposed_smile
    layer[~allowed, 3] = 0
    layer[layer[:, :, 3] == 0, :3] = 0
    if not np.any(layer[:, :, 3] > 0):
        raise RuntimeError("stifled-laugh special face is empty")

    # Ren'Py may retain a face attribute while a pose attribute changes.  A
    # special pose therefore has to erase every pixel that any ordinary face
    # layer can occupy before drawing its own fixed expression.  Copying those
    # pixels from the canonical featureless head is lossless and remains
    # confined to the established semantic masks.
    repair_mask = np.zeros(layer.shape[:2], dtype=bool)
    for expression in tsubaki.EXPRESSIONS:
        repair_mask |= tsubaki.spatial_allow_for_layer(
            layer.shape[:2], expression
        )
        face_path = FACE_DIR / f"face_{expression}.png"
        if not face_path.is_file():
            raise FileNotFoundError(face_path)
        # The ordinary layers use a nearest-neighbor-warped authoring mask.
        # Union their actual alpha too, eliminating one-pixel analytic/raster
        # disagreements at curved mouth and eye boundaries.
        repair_mask |= load_rgba(face_path)[:, :, 3] > 0
    repair_mask &= head[:, :, 3] == 255
    special = np.zeros_like(layer)
    special[repair_mask] = head[repair_mask]
    special = compose(special, layer).copy()
    special[special[:, :, 3] == 0, :3] = 0
    special_path = PART_DIR / "forward_special_stifled_laugh.png"
    save_rgba(special_path, special)

    hair_back = load_rgba(PART_DIR / "forward_hair_back.png")
    hair_front = load_rgba(PART_DIR / "forward_hair_front.png")
    review_dir = PART_DIR / "_review"
    for outfit in ("casual", "uniform"):
        production_body = PART_DIR / f"forward_{outfit}_body.png"
        body = load_rgba(
            production_body
            if production_body.is_file()
            else MASTER_DIR / f"forward_{outfit}_body.png"
        )
        low = load_rgba(PART_DIR / f"forward_{outfit}_arm_r_stifled_laugh.png")
        raised = load_rgba(PART_DIR / f"forward_{outfit}_over_stifled_laugh.png")
        sprite = compose(hair_back, head, body, low, special, hair_front, raised)
        save_rgba(review_dir / f"{outfit}_stifled_laugh.png", sprite)
        for background_name, color in (
            ("dark", (24, 26, 34, 255)),
            ("light", (238, 235, 228, 255)),
        ):
            background = Image.new("RGBA", CANVAS_SIZE, color)
            rendered = Image.alpha_composite(background, Image.fromarray(sprite))
            rendered.convert("RGB").save(
                review_dir / f"{outfit}_stifled_laugh_{background_name}.png",
                optimize=True,
            )

    report = {
        "schema_version": 1,
        "donor": str(donor_path),
        "output": str(special_path),
        "registration": asdict(registration),
        "raw_layer": asdict(raw_metrics),
        "normalization_for_mask_only": normalization,
        "laugh_ink_pixels": int((layer[:, :, 3] > 0).sum()),
        "repair_pixels": int(repair_mask.sum()),
        "visible_pixels": int((special[:, :, 3] > 0).sum()),
        "hidden_rgb_pixels": int(
            np.any(special[:, :, :3] != 0, axis=2)[special[:, :, 3] == 0].sum()
        ),
    }
    (PART_DIR / "special_metrics.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Processed Tsubaki stifled-laugh special: {special_path}")
    print(f"Reviews: {review_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
