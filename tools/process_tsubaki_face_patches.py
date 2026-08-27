"""Build Tsubaki's Himeko-style face patches from the approved neutral sprites.

The shipped bases remain the original 1023x1537 ``neutral.png`` and
``neut_uniform.png`` files. Alternate expressions are reconstructed from the
already-registered expression masters. Featureless edits made from the two
approved bases provide the face-skin topology used to constrain one fixed
feathered export mask per outfit. Their color-matched RGB is used only inside
the guarded brow/upper-eyelid cleanup corridors; no featureless full face is
installed.

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
SPRITE_DIR = PROJECT_ROOT / "game" / "assets" / "characters" / "tsubaki"
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

# Every generated expression master carries a pale upper-eyelid arc that reads
# as a second eyebrow once the authored brow moves away from the neutral line.
# These two narrow source-space paths trace that arc while leaving the
# expressive brow above and the eyelashes below outside the cleanup region.
# They are warped with the same per-expression affine as the face donor.
SOURCE_CREASE_PATHS = (
    (
        (339, 641),
        (350, 635),
        (367, 630),
        (386, 626),
        (405, 625),
        (424, 628),
        (444, 634),
        (458, 641),
    ),
    (
        (556, 641),
        (570, 635),
        (590, 630),
        (612, 627),
        (634, 629),
        (653, 634),
        (670, 641),
    ),
)
SOURCE_CREASE_THICKNESS = 8

# The intact outfit bases contain their neutral eyebrows. Alternate face plates
# must fully own that region before drawing the replacement face, or a sliver
# of the old brow survives beside the bangs. In the flattened sparse neutral
# layer, brow ink shares components with a few bang and upper-eye fragments, so
# this deliberately conservative source-space guard owns the complete region.
# The cleanup plate sits below the alternate face and is exposed only where the
# broader face mask previously failed to cover base-brow/bang intersections.
SOURCE_NEUTRAL_GUARD_Y_OFFSET = -37.0
SOURCE_NEUTRAL_GUARD_AXES = (52, 18)


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


def retain_components(
    mask: np.ndarray,
    *,
    minimum_area: int,
    maximum_area: int | None = None,
) -> np.ndarray:
    """Keep only connected components within a controlled area range."""

    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        mask.astype(np.uint8), connectivity=8
    )
    retained = np.zeros(mask.shape, dtype=bool)
    for label in range(1, count):
        area = int(stats[label, cv2.CC_STAT_AREA])
        if area < minimum_area:
            continue
        if maximum_area is not None and area > maximum_area:
            continue
        retained |= labels == label
    return retained


def base_neutral_guard_alpha(
    source_neutral: np.ndarray,
    source_eyes: np.ndarray,
    source_to_target: np.ndarray,
    base_alpha: np.ndarray,
) -> tuple[np.ndarray, dict[str, object]]:
    """Build a conservative underlay for the intact base-brow region.

    A strict eyebrow-only mask cannot be recovered from the flattened sparse
    neutral RGBA: brow, bang, and upper-eye ink touch in several components.
    The eye-relative guard therefore overincludes that local feature region,
    then sits below the alternate face plate. It becomes visible only where
    the broader face mask previously left base-brow/bang ink uncovered or
    partially blended.
    """

    source_shape = source_neutral.shape[:2]
    guard = np.zeros(source_shape, dtype=np.uint8)
    for eye_x, eye_y in source_eyes:
        cv2.ellipse(
            guard,
            (
                round(float(eye_x)),
                round(float(eye_y + SOURCE_NEUTRAL_GUARD_Y_OFFSET)),
            ),
            SOURCE_NEUTRAL_GUARD_AXES,
            0.0,
            0.0,
            360.0,
            1,
            thickness=-1,
        )
    source_guard_footprint = (
        guard.astype(bool)
        & (source_neutral[:, :, 3] > 0)
    )
    source_guard_footprint = retain_components(
        source_guard_footprint,
        minimum_area=2,
        maximum_area=900,
    )
    if not np.any(source_guard_footprint):
        raise RuntimeError("Could not isolate the guarded sparse-neutral region")

    guard_footprint = cv2.warpAffine(
        source_guard_footprint.astype(np.uint8),
        source_to_target,
        OUTPUT_SIZE,
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    ).astype(bool)
    guard_footprint &= base_alpha > 0

    core = cv2.dilate(
        guard_footprint.astype(np.uint8),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)),
    ).astype(bool)
    core &= base_alpha > 0
    feather = cv2.GaussianBlur(
        core.astype(np.float32), (0, 0), sigmaX=0.85, sigmaY=0.85
    )
    feather[core] = 1.0
    feather *= (base_alpha / 255.0)
    alpha = np.clip(np.rint(feather * 255.0), 0, 255).astype(np.uint8)
    unowned_guard = int(np.count_nonzero(alpha[guard_footprint] != 255))
    if unowned_guard:
        raise RuntimeError(
            "Neutral-feature guard left "
            f"{unowned_guard} guarded pixels non-opaque"
        )

    ys, xs = np.nonzero(alpha)
    bbox = None
    if len(xs):
        bbox = [
            int(xs.min()),
            int(ys.min()),
            int(xs.max()) + 1,
            int(ys.max()) + 1,
        ]
    return alpha, {
        "source_guard_footprint_pixels": int(source_guard_footprint.sum()),
        "guard_footprint_pixels": int(guard_footprint.sum()),
        "unowned_guard_pixels": unowned_guard,
        "opaque_pixels": int((alpha == 255).sum()),
        "partial_pixels": int(((alpha > 0) & (alpha < 255)).sum()),
        "bbox": bbox,
    }


def remove_duplicate_eyelid_arcs(
    face_rgb: np.ndarray,
    featureless_rgb: np.ndarray,
    base_alpha: np.ndarray,
    donor_to_target: np.ndarray,
) -> tuple[np.ndarray, dict[str, object]]:
    """Replace only the pale lower ghost-brow arcs with matched facial skin."""

    source_guard = np.zeros((SOURCE_SIZE[1], SOURCE_SIZE[0]), dtype=np.uint8)
    for path in SOURCE_CREASE_PATHS:
        cv2.polylines(
            source_guard,
            [np.asarray(path, dtype=np.int32)],
            isClosed=False,
            color=1,
            thickness=SOURCE_CREASE_THICKNESS,
            lineType=cv2.LINE_AA,
        )
    source_guard = source_guard > 0
    guard = cv2.warpAffine(
        source_guard.astype(np.uint8),
        donor_to_target,
        OUTPUT_SIZE,
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    ).astype(bool)
    guard &= base_alpha > 0
    if not np.any(guard):
        raise RuntimeError("Duplicate-arc cleanup guard is empty after registration")

    # The corridors sit strictly between the authored brows and eyelashes.
    # Replace their complete interior so antialiased fragments cannot survive
    # as a dotted second brow.  The featureless donor was edited from the same
    # outfit base and therefore also restores any bang pixels crossing a guard.
    core = cv2.erode(
        guard.astype(np.uint8),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
    ).astype(bool)
    weight = cv2.GaussianBlur(
        guard.astype(np.float32), (0, 0), sigmaX=0.75, sigmaY=0.75
    )
    weight *= guard
    weight[core] = 1.0
    weight *= base_alpha / 255.0
    cleaned = np.clip(
        np.rint(
            face_rgb.astype(np.float32) * (1.0 - weight[:, :, None])
            + featureless_rgb.astype(np.float32) * weight[:, :, None]
        ),
        0,
        255,
    ).astype(np.uint8)

    changed = np.any(cleaned != face_rgb, axis=2)
    if np.any(changed & ~guard):
        raise RuntimeError("Duplicate-arc cleanup escaped its guarded corridors")
    core_residual = int(
        np.max(
            np.abs(
                cleaned[core].astype(np.int16)
                - featureless_rgb[core].astype(np.int16)
            )
        )
    )
    if core_residual:
        raise RuntimeError(
            "Duplicate-arc cleanup did not fully replace its traced core"
        )
    ys, xs = np.nonzero(changed)
    bbox = None
    if len(xs):
        bbox = [
            int(xs.min()),
            int(ys.min()),
            int(xs.max()) + 1,
            int(ys.max()) + 1,
        ]
    return cleaned, {
        "guard_pixels": int(guard.sum()),
        "core_pixels": int(core.sum()),
        "core_residual_max_channel_delta": core_residual,
        "changed_pixels": int(changed.sum()),
        "bbox": bbox,
    }


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
        "schema_version": 2,
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

        featureless_matched_rgb, featureless_offsets, featureless_samples = (
            match_donor_skin(
                featureless_rgb,
                base[:, :, :3],
                skin_component,
                patch_center,
            )
        )
        neutral_guard_alpha, neutral_guard_metrics = base_neutral_guard_alpha(
            source_neutral,
            source_eyes,
            matrix,
            base[:, :, 3],
        )
        neutral_guard_layer = np.dstack(
            (featureless_matched_rgb, neutral_guard_alpha)
        )
        neutral_guard_layer[neutral_guard_alpha == 0, :3] = 0

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
            "featureless_skin_offsets": featureless_offsets,
            "featureless_skin_samples": featureless_samples,
            "base_neutral_guard": neutral_guard_metrics,
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
            corrected_rgb, arc_cleanup_metrics = remove_duplicate_eyelid_arcs(
                corrected_rgb,
                featureless_matched_rgb,
                base[:, :, 3],
                donor_to_target,
            )
            face_layer = np.dstack((corrected_rgb, patch_alpha))
            face_layer[patch_alpha == 0, :3] = 0
            output = alpha_composite(neutral_guard_layer, face_layer).copy()
            output[output[:, :, 3] == 0, :3] = 0
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
                "duplicate_arc_cleanup": arc_cleanup_metrics,
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
