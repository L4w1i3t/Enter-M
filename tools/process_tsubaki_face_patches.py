"""Build Tsubaki's Himeko-style face patches from the approved neutral sprites.

The shipped bases remain the original 1023x1537 ``neutral.png`` and
``neut_uniform.png`` files. Alternate expressions are reconstructed from the
already-registered expression masters. Featureless edits made from the two
approved bases provide only the face-skin topology used to constrain one fixed
feathered export mask per outfit; their RGB pixels are never installed.

Tsubaki's casual and uniform heads differ by roughly seven source pixels, so
the output is outfit-conditioned.  This keeps the runtime model simple
(whole-body neutral base + one face patch) without introducing the visible
expression jump that a shared patch would cause.
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
SPRITE_DIR = PROJECT_ROOT / "game" / "mod_assets" / "char_sprites" / "tsubaki"
DEFAULT_SOURCE_DIR = PROJECT_ROOT / "tmp" / "tsubaki_sprite_processed"
DEFAULT_PART_DIR = PROJECT_ROOT / "tmp" / "tsubaki_sprite_parts"
DEFAULT_DONOR_DIR = PROJECT_ROOT / "tmp" / "tsubaki_face_patch"
DEFAULT_MASTER_DIR = PROJECT_ROOT / "tmp" / "tsubaki_sprite_masters"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "tmp" / "tsubaki_face_patch" / "output"

OUTPUT_SIZE = (1023, 1537)
SOURCE_SIZE = (1024, 1536)

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

MASTER_OVERRIDES = {"happy": "expression_happy_v2.png"}

OUTFITS = {
    "casual": {
        "base": "neutral.png",
        "featureless": "featureless_casual_generated.png",
        # Start below the warm-brown fringe.  The wider vertical window used
        # during prototyping could mistake a detached hair highlight for the
        # viewer-right amber iris and rotate the complete expression plate.
        "target_roi": (420, 360, 600, 420),
    },
    "uniform": {
        "base": "neut_uniform.png",
        "featureless": "featureless_uniform_generated.png",
        "target_roi": (420, 355, 600, 415),
    },
}

SOURCE_EYE_ROI = (430, 580, 590, 650)
PATCH_RADIUS = (155.0, 135.0)
PATCH_CENTER_BELOW_EYES = 31.0
PATCH_SOLID_RADIUS = 0.84


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--part-dir", type=Path, default=DEFAULT_PART_DIR)
    parser.add_argument("--donor-dir", type=Path, default=DEFAULT_DONOR_DIR)
    parser.add_argument("--master-dir", type=Path, default=DEFAULT_MASTER_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def load_rgba(path: Path, expected_size: tuple[int, int]) -> np.ndarray:
    if not path.is_file():
        raise FileNotFoundError(path)
    with Image.open(path) as image:
        if image.size != expected_size:
            raise ValueError(f"{path}: got {image.size}, expected {expected_size}")
        return np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()


def load_rgb(path: Path, expected_size: tuple[int, int]) -> np.ndarray:
    if not path.is_file():
        raise FileNotFoundError(path)
    with Image.open(path) as image:
        if image.size != expected_size:
            raise ValueError(f"{path}: got {image.size}, expected {expected_size}")
        return np.asarray(image.convert("RGB"), dtype=np.uint8).copy()


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


def amber_iris_centers(
    rgba: np.ndarray,
    roi: tuple[int, int, int, int],
) -> np.ndarray:
    rgb = rgba[:, :, :3]
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    height, width = rgba.shape[:2]
    yy, xx = np.indices((height, width))
    left, top, right, bottom = roi
    allowed = (
        (xx >= left)
        & (xx < right)
        & (yy >= top)
        & (yy < bottom)
        & (rgba[:, :, 3] >= 64)
    )
    amber = (
        allowed
        & (hsv[:, :, 0] >= 5)
        & (hsv[:, :, 0] <= 35)
        & (hsv[:, :, 1] >= 85)
        & (hsv[:, :, 2] >= 45)
    )
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(
        amber.astype(np.uint8), connectivity=8
    )
    components: list[tuple[int, float, float]] = []
    for label in range(1, count):
        area = int(stats[label, cv2.CC_STAT_AREA])
        if 250 <= area <= 1800:
            components.append(
                (area, float(centroids[label, 0]), float(centroids[label, 1]))
            )
    if len(components) < 2:
        raise RuntimeError(f"Expected two amber irises in ROI {roi}, found {components}")
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


def warp_rgb(rgb: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    return cv2.warpAffine(
        rgb,
        matrix,
        OUTPUT_SIZE,
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0),
    )


def registration_matrix(metrics: dict[str, object]) -> np.ndarray:
    scale = float(metrics["scale"])
    angle = math.radians(float(metrics["rotation_degrees"]))
    cosine = scale * math.cos(angle)
    sine = scale * math.sin(angle)
    return np.asarray(
        (
            (cosine, -sine, float(metrics["translate_x"])),
            (sine, cosine, float(metrics["translate_y"])),
        ),
        dtype=np.float32,
    )


def compose_affine(first: np.ndarray, second: np.ndarray) -> np.ndarray:
    """Return the affine that applies ``second`` and then ``first``."""

    first_h = np.vstack((first, (0.0, 0.0, 1.0)))
    second_h = np.vstack((second, (0.0, 0.0, 1.0)))
    return (first_h @ second_h)[:2].astype(np.float32)


def face_skin_component(rgb: np.ndarray, seed: tuple[int, int]) -> np.ndarray:
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    skin = (
        (hsv[:, :, 0] <= 24)
        & (hsv[:, :, 1] >= 12)
        & (hsv[:, :, 1] <= 115)
        & (hsv[:, :, 2] >= 145)
    )
    skin = cv2.morphologyEx(
        skin.astype(np.uint8),
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)),
    )
    count, labels = cv2.connectedComponents(skin, connectivity=8)
    seed_x, seed_y = seed
    label = int(labels[seed_y, seed_x])
    if label == 0 or label >= count:
        raise RuntimeError(f"Featureless face skin seed {seed} did not hit skin")
    component = labels == label
    component = cv2.morphologyEx(
        component.astype(np.uint8),
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)),
    )
    return component.astype(bool)


def feathered_face_mask(
    shape: tuple[int, int],
    center: tuple[float, float],
    skin_component: np.ndarray,
    base_alpha: np.ndarray,
) -> np.ndarray:
    yy, xx = np.indices(shape)
    center_x, center_y = center
    radius_x, radius_y = PATCH_RADIUS
    distance = np.sqrt(
        ((xx - center_x) / radius_x) ** 2
        + ((yy - center_y) / radius_y) ** 2
    )
    feather = np.zeros(shape, dtype=np.float32)
    feather[distance <= PATCH_SOLID_RADIUS] = 1.0
    transition = (distance > PATCH_SOLID_RADIUS) & (distance < 1.0)
    feather[transition] = (1.0 - distance[transition]) / (
        1.0 - PATCH_SOLID_RADIUS
    )
    feather = feather * feather * (3.0 - 2.0 * feather)

    # The replacement plate stops above the chin/neck join.  The expression
    # donors have a slightly different jaw shadow, and allowing that shadow
    # onto the original whole-body base creates a dark wedge below the cheek.
    # Every authored mouth, tear, and blush ends above this smooth cutoff.
    lower_start = center_y + 85.0
    lower_end = center_y + 105.0
    lower = np.clip((lower_end - yy) / (lower_end - lower_start), 0.0, 1.0)
    lower = lower * lower * (3.0 - 2.0 * lower)
    feather *= lower

    skin_alpha = cv2.GaussianBlur(
        skin_component.astype(np.float32), (0, 0), sigmaX=1.35, sigmaY=1.35
    )
    alpha = feather * np.clip(skin_alpha, 0.0, 1.0) * (base_alpha / 255.0)
    return np.clip(np.rint(alpha * 255.0), 0, 255).astype(np.uint8)


def match_donor_skin(
    donor_rgb: np.ndarray,
    base_rgb: np.ndarray,
    skin_component: np.ndarray,
    center: tuple[float, float],
) -> tuple[np.ndarray, list[float], int]:
    yy, xx = np.indices(skin_component.shape)
    center_x, center_y = center
    sample = (
        skin_component
        & ((((xx - center_x) / 105.0) ** 2 + ((yy - center_y) / 92.0) ** 2) <= 1.0)
    )
    base_hsv = cv2.cvtColor(base_rgb, cv2.COLOR_RGB2HSV)
    donor_hsv = cv2.cvtColor(donor_rgb, cv2.COLOR_RGB2HSV)
    donor_skin = (
        (donor_hsv[:, :, 0] <= 24)
        & (donor_hsv[:, :, 1] >= 12)
        & (donor_hsv[:, :, 1] <= 115)
        & (donor_hsv[:, :, 2] >= 145)
    )
    sample &= (
        (base_hsv[:, :, 0] <= 24)
        & (base_hsv[:, :, 1] >= 12)
        & (base_hsv[:, :, 1] <= 115)
        & (base_hsv[:, :, 2] >= 145)
        & donor_skin
    )
    if int(sample.sum()) < 1000:
        raise RuntimeError(f"Insufficient skin samples: {int(sample.sum())}")
    offsets = np.median(
        base_rgb[sample].astype(np.float32)
        - donor_rgb[sample].astype(np.float32),
        axis=0,
    )
    corrected = donor_rgb.astype(np.float32)
    corrected[skin_component & donor_skin] += offsets
    corrected = np.clip(np.rint(corrected), 0, 255).astype(np.uint8)
    return (
        corrected,
        [round(float(value), 3) for value in offsets],
        int(sample.sum()),
    )


def font(size: int) -> ImageFont.ImageFont:
    for candidate in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def checker(size: tuple[int, int], tile: int = 16) -> Image.Image:
    width, height = size
    yy, xx = np.indices((height, width))
    cells = ((xx // tile) + (yy // tile)) % 2
    rgb = np.empty((height, width, 3), dtype=np.uint8)
    rgb[cells == 0] = (78, 81, 88)
    rgb[cells == 1] = (116, 120, 128)
    return Image.fromarray(rgb, "RGB")


def make_review(
    output_dir: Path,
    bases: dict[str, np.ndarray],
) -> None:
    thumb_size = (256, 384)
    label_height = 30
    columns = 4
    rows = math.ceil(len(EXPRESSIONS) / columns)
    for outfit, base in bases.items():
        for background_name, background_factory in (
            ("light", lambda: Image.new("RGB", OUTPUT_SIZE, (238, 235, 228))),
            ("dark", lambda: Image.new("RGB", OUTPUT_SIZE, (24, 26, 34))),
            ("checker", lambda: checker(OUTPUT_SIZE)),
        ):
            sheet = Image.new(
                "RGB",
                (columns * thumb_size[0], rows * (thumb_size[1] + label_height)),
                (31, 33, 38),
            )
            draw = ImageDraw.Draw(sheet)
            for index, expression in enumerate(EXPRESSIONS):
                if expression == "neut":
                    sprite = base
                else:
                    layer = load_rgba(
                        output_dir / f"face_{expression}_{outfit}.png", OUTPUT_SIZE
                    )
                    sprite = alpha_composite(base, layer)
                background = background_factory().convert("RGBA")
                rendered = Image.alpha_composite(
                    background, Image.fromarray(sprite, "RGBA")
                ).convert("RGB")
                rendered.thumbnail(thumb_size, Image.Resampling.LANCZOS)
                cell_x = (index % columns) * thumb_size[0]
                cell_y = (index // columns) * (thumb_size[1] + label_height)
                paste_x = cell_x + (thumb_size[0] - rendered.width) // 2
                paste_y = cell_y + (thumb_size[1] - rendered.height)
                sheet.paste(rendered, (paste_x, paste_y))
                draw.text(
                    (cell_x + 6, cell_y + thumb_size[1] + 3),
                    expression,
                    fill=(235, 235, 238),
                    font=font(18),
                )
            review_dir = output_dir / "_review"
            review_dir.mkdir(parents=True, exist_ok=True)
            sheet.save(
                review_dir / f"tsubaki_{outfit}_faces_{background_name}.png",
                optimize=True,
            )

            head_cell = (300, 300)
            head_label_height = 30
            head_sheet = Image.new(
                "RGB",
                (
                    columns * head_cell[0],
                    rows * (head_cell[1] + head_label_height),
                ),
                (31, 33, 38),
            )
            head_draw = ImageDraw.Draw(head_sheet)
            for index, expression in enumerate(EXPRESSIONS):
                if expression == "neut":
                    sprite = base
                else:
                    layer = load_rgba(
                        output_dir / f"face_{expression}_{outfit}.png", OUTPUT_SIZE
                    )
                    sprite = alpha_composite(base, layer)
                background = background_factory().convert("RGBA")
                rendered = Image.alpha_composite(
                    background, Image.fromarray(sprite, "RGBA")
                ).convert("RGB")
                head = rendered.crop((330, 220, 690, 550))
                head.thumbnail(head_cell, Image.Resampling.LANCZOS)
                cell_x = (index % columns) * head_cell[0]
                cell_y = (index // columns) * (head_cell[1] + head_label_height)
                paste_x = cell_x + (head_cell[0] - head.width) // 2
                paste_y = cell_y + (head_cell[1] - head.height)
                head_sheet.paste(head, (paste_x, paste_y))
                head_draw.text(
                    (cell_x + 6, cell_y + head_cell[1] + 3),
                    expression,
                    fill=(235, 235, 238),
                    font=font(18),
                )
            head_sheet.save(
                review_dir / f"tsubaki_{outfit}_heads_{background_name}.png",
                optimize=True,
            )


def main() -> int:
    args = parse_args()
    source_head = load_rgba(args.part_dir / "forward_head.png", SOURCE_SIZE)
    source_neutral = load_rgba(args.source_dir / "face_neut.png", SOURCE_SIZE)
    source_composite = alpha_composite(source_head, source_neutral)
    source_eyes = amber_iris_centers(source_composite, SOURCE_EYE_ROI)
    source_metrics = json.loads(
        (args.source_dir / "metrics.json").read_text(encoding="utf-8")
    )
    production_matrix = np.asarray(
        source_metrics["production_matrix"], dtype=np.float32
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    bases: dict[str, np.ndarray] = {}
    report: dict[str, object] = {
        "schema_version": 1,
        "output_size": list(OUTPUT_SIZE),
        "source_size": list(SOURCE_SIZE),
        "expressions": list(EXPRESSIONS),
        "outfits": {},
    }

    transparent = np.zeros((OUTPUT_SIZE[1], OUTPUT_SIZE[0], 4), dtype=np.uint8)
    for outfit, spec in OUTFITS.items():
        base = load_rgba(SPRITE_DIR / spec["base"], OUTPUT_SIZE)
        featureless_rgb = load_rgb(args.donor_dir / spec["featureless"], OUTPUT_SIZE)
        target_eyes = amber_iris_centers(base, spec["target_roi"])
        matrix = similarity_from_two_points(source_eyes, target_eyes)
        eye_midpoint = target_eyes.mean(axis=0)
        patch_center = (
            float(eye_midpoint[0]),
            float(eye_midpoint[1] + PATCH_CENTER_BELOW_EYES),
        )
        skin_component = face_skin_component(
            featureless_rgb,
            (round(patch_center[0]), round(patch_center[1])),
        )
        patch_alpha = feathered_face_mask(
            base.shape[:2], patch_center, skin_component, base[:, :, 3]
        )
        if int((patch_alpha == 255).sum()) < 20000:
            raise RuntimeError(f"{outfit}: face patch has too little opaque coverage")

        save_rgba(args.output_dir / f"face_neut_{outfit}.png", transparent)
        outfit_report: dict[str, object] = {
            "base": str(SPRITE_DIR / spec["base"]),
            "featureless_donor": str(args.donor_dir / spec["featureless"]),
            "source_eye_centers": source_eyes.round(4).tolist(),
            "target_eye_centers": target_eyes.round(4).tolist(),
            "matrix": matrix.astype(float).tolist(),
            "patch_center": [round(value, 4) for value in patch_center],
            "patch_radius": list(PATCH_RADIUS),
            "patch_solid_radius": PATCH_SOLID_RADIUS,
            "visible_mask_pixels": int((patch_alpha > 0).sum()),
            "opaque_mask_pixels": int((patch_alpha == 255).sum()),
            "partial_mask_pixels": int(
                ((patch_alpha > 0) & (patch_alpha < 255)).sum()
            ),
            "layers": {},
        }
        layers = outfit_report["layers"]
        assert isinstance(layers, dict)
        for expression in EXPRESSIONS[1:]:
            master_filename = MASTER_OVERRIDES.get(
                expression, f"expression_{expression}.png"
            )
            donor = load_rgb(args.master_dir / master_filename, SOURCE_SIZE)
            layer_metrics = source_metrics["layers"][expression]
            donor_registration = registration_matrix(layer_metrics["registration"])
            donor_to_production = compose_affine(
                production_matrix, donor_registration
            )
            donor_to_target = compose_affine(matrix, donor_to_production)
            warped_rgb = warp_rgb(donor, donor_to_target)
            corrected_rgb, skin_offsets, skin_samples = match_donor_skin(
                warped_rgb,
                base[:, :, :3],
                skin_component,
                patch_center,
            )
            output = np.dstack((corrected_rgb, patch_alpha))
            output[patch_alpha == 0, :3] = 0
            destination = args.output_dir / f"face_{expression}_{outfit}.png"
            save_rgba(destination, output)
            visible = output[:, :, 3] > 0
            changed = np.any(
                alpha_composite(base, output)[:, :, :3] != base[:, :, :3], axis=2
            )
            layers[expression] = {
                "path": str(destination),
                "visible_pixels": int(visible.sum()),
                "changed_pixels": int(changed.sum()),
                "donor": str(args.master_dir / master_filename),
                "donor_to_target_matrix": donor_to_target.astype(float).tolist(),
                "skin_offsets": skin_offsets,
                "skin_samples": skin_samples,
                "hidden_rgb_pixels": int(
                    np.any(output[:, :, :3] != 0, axis=2)[~visible].sum()
                ),
            }
        bases[outfit] = base
        outfits = report["outfits"]
        assert isinstance(outfits, dict)
        outfits[outfit] = outfit_report

    (args.output_dir / "metrics.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    make_review(args.output_dir, bases)
    print(
        f"Built {len(EXPRESSIONS) * len(OUTFITS)} Tsubaki face layers: "
        f"{args.output_dir}"
    )
    print(f"Metrics: {args.output_dir / 'metrics.json'}")
    print(f"Reviews: {args.output_dir / '_review'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
