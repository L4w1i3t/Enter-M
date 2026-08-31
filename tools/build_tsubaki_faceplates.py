"""Build Tsubaki's expressions as Himeko/Asahina-style oval face plates.

The canonical casual and uniform sprites stay intact. Each alternate expression
is registered to its outfit, copied through one smooth oval that includes the
face, eyebrows, and surrounding bangs, and composited by Ren'Py over the neutral
base. No feature segmentation or eyebrow repair underlay participates in the
exported plate. A bounded pre-slice source cleanup replaces pale detached arc
residue without changing the plate's simple geometric alpha.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "game" / "assets" / "characters" / "tsubaki"
DEFINITIONS = ROOT / "game" / "asset_definitions" / "def_characters.rpy"
MASTER_DIR = ROOT / "tmp" / "tsubaki_sprite_masters"
SOURCE_DIR = ROOT / "tmp" / "tsubaki_sprite_processed"
PART_DIR = ROOT / "tmp" / "tsubaki_sprite_parts"
FEATURELESS_DIR = ROOT / "tmp" / "tsubaki_face_patch"
DEFAULT_STAGING = ROOT / "tmp" / "tsubaki_oval_faceplates"

CANVAS = (1023, 1537)
SOURCE_CANVAS = (1024, 1536)
SOURCE_EYE_ROI = (430, 580, 590, 650)

# This is the Himeko/Asahina construction scaled to Tsubaki's smaller rendered
# head: one fixed geometric ellipse clipped only by base alpha.  The solid core
# fully owns the old neutral-brow footprint, while the smaller outer edge avoids
# replacing unrelated jaw, neck, and outer-hair pixels.
PLATE_RADIUS = (155.0, 135.0)
PLATE_CENTER_BELOW_EYES = 31.0
PLATE_SOLID_RADIUS = 0.84
PLATE_LOWER_FADE = (85.0, 105.0)

EMOTIONS = (
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
EXPRESSIONS = ("neut", *EMOTIONS)
MASTER_OVERRIDES = {"happy": "expression_happy_v2.png"}
OUTFITS = {
    "casual": {
        "base": "neutral.png",
        "featureless": "featureless_casual_generated.png",
        "target_roi": (420, 360, 600, 420),
    },
    "uniform": {
        "base": "neut_uniform.png",
        "featureless": "featureless_uniform_generated.png",
        "target_roi": (420, 355, 600, 415),
    },
}
EXPECTED_BROW_FOOTPRINTS = {
    "casual": {
        "pixels": 2930,
        "bbox": [407, 324, 602, 375],
        "sha256": "7416bdcb16da6fc9e8b73dedadc9f63baf4d9ea3e336171374ce41cfea125e51",
    },
    "uniform": {
        "pixels": 2848,
        "bbox": [408, 318, 602, 369],
        "sha256": "e005da546d595659a34186a08347cdea11e073538d382f008cd7dab0caccd42f",
    },
}


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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def bundle_sha256(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.name):
        if not path.is_file() or path.is_symlink():
            raise FileNotFoundError(f"Missing or unsafe authoring input: {path}")
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def mask_bbox(mask: np.ndarray) -> list[int] | None:
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]


def amber_iris_centers(rgba: np.ndarray, roi: tuple[int, int, int, int]) -> np.ndarray:
    hsv = cv2.cvtColor(rgba[:, :, :3], cv2.COLOR_RGB2HSV)
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
        raise RuntimeError(f"Expected two amber irises in ROI {roi}: {components}")
    chosen = sorted(components, reverse=True)[:2]
    chosen.sort(key=lambda item: item[1])
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


def plate_center(target_eyes: np.ndarray) -> tuple[float, float]:
    eye_midpoint = target_eyes.mean(axis=0)
    return (
        float(eye_midpoint[0]),
        float(eye_midpoint[1] + PLATE_CENTER_BELOW_EYES),
    )


def warp_rgb(rgb: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    return cv2.warpAffine(
        rgb,
        matrix,
        CANVAS,
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0),
    )


def border_checker_mask(rgb: np.ndarray) -> np.ndarray:
    """Find the border-connected near-gray checker matte in a source master."""

    channels = rgb.astype(np.int16)
    candidate = (channels.max(axis=2) - channels.min(axis=2) <= 8) & (
        channels.min(axis=2) >= 210
    )
    count, labels = cv2.connectedComponents(candidate.astype(np.uint8), connectivity=8)
    if count <= 1:
        return np.zeros(candidate.shape, dtype=bool)
    border_labels = np.unique(
        np.concatenate((labels[0], labels[-1], labels[:, 0], labels[:, -1]))
    )
    border_labels = border_labels[border_labels != 0]
    if not len(border_labels):
        return np.zeros(candidate.shape, dtype=bool)
    return candidate & np.isin(labels, border_labels)


def warp_mask(mask: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    return cv2.warpAffine(
        mask.astype(np.uint8),
        matrix,
        CANVAS,
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    ).astype(bool)


def oval_alpha(base_alpha: np.ndarray, center: tuple[float, float]) -> np.ndarray:
    yy, xx = np.indices(base_alpha.shape, dtype=np.float32)
    center_x, center_y = center
    radius_x, radius_y = PLATE_RADIUS
    distance = np.sqrt(
        ((xx - center_x) / radius_x) ** 2 + ((yy - center_y) / radius_y) ** 2
    )
    feather = np.clip((1.0 - distance) / (1.0 - PLATE_SOLID_RADIUS), 0.0, 1.0)
    feather = feather * feather * (3.0 - 2.0 * feather)
    # Tsubaki's masters are detached heads rather than full-body edits.  Stop
    # the geometric plate before the base's chin/neck join, with a smooth fade,
    # so checker-matte or alternate jaw-shadow pixels cannot reach clothing.
    lower_start = center_y + PLATE_LOWER_FADE[0]
    lower_end = center_y + PLATE_LOWER_FADE[1]
    lower = np.clip((lower_end - yy) / (lower_end - lower_start), 0.0, 1.0)
    lower = lower * lower * (3.0 - 2.0 * lower)
    feather *= lower
    alpha = np.rint(feather * (base_alpha.astype(np.float32) / 255.0) * 255.0)
    alpha = np.clip(alpha, 0, 255).astype(np.uint8)
    alpha[alpha < 2] = 0
    alpha[alpha > 253] = 255
    return alpha


def skin_match(
    donor_rgb: np.ndarray,
    base_rgb: np.ndarray,
    base_alpha: np.ndarray,
    plate_alpha: np.ndarray,
    center: tuple[float, float],
) -> tuple[np.ndarray, list[float], int]:
    """Match only donor skin color; preserve all authored feature/hair RGB."""

    yy, xx = np.indices(base_alpha.shape)
    center_x, center_y = center
    inner = (((xx - center_x) / 105.0) ** 2 + ((yy - center_y) / 92.0) ** 2) <= 1.0
    base_hsv = cv2.cvtColor(base_rgb, cv2.COLOR_RGB2HSV)
    donor_hsv = cv2.cvtColor(donor_rgb, cv2.COLOR_RGB2HSV)

    def is_skin(hsv: np.ndarray) -> np.ndarray:
        return (
            (hsv[:, :, 0] <= 24)
            & (hsv[:, :, 1] >= 12)
            & (hsv[:, :, 1] <= 115)
            & (hsv[:, :, 2] >= 145)
        )

    base_skin = is_skin(base_hsv)
    donor_skin = is_skin(donor_hsv)
    sample = inner & base_skin & donor_skin & (base_alpha == 255) & (plate_alpha == 255)
    sample_count = int(sample.sum())
    if sample_count < 1000:
        raise RuntimeError(f"Insufficient shared skin samples: {sample_count}")
    offsets = np.median(
        base_rgb[sample].astype(np.float32) - donor_rgb[sample].astype(np.float32),
        axis=0,
    )
    corrected = donor_rgb.astype(np.float32)
    correction_support = donor_skin & (plate_alpha > 0)
    corrected[correction_support] += offsets
    corrected = np.clip(np.rint(corrected), 0, 255).astype(np.uint8)
    return corrected, [round(float(value), 3) for value in offsets], sample_count


def rgb_luminance(rgb: np.ndarray) -> np.ndarray:
    values = rgb.astype(np.float32)
    return (
        0.2126 * values[:, :, 0] + 0.7152 * values[:, :, 1] + 0.0722 * values[:, :, 2]
    )


def skin_pixels(rgb: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    return (
        (hsv[:, :, 0] <= 24)
        & (hsv[:, :, 1] >= 10)
        & (hsv[:, :, 1] <= 125)
        & (hsv[:, :, 2] >= 135)
    )


def lash_relative_band(
    detail: np.ndarray, dark_ink: np.ndarray, eye_centers: np.ndarray
) -> tuple[np.ndarray, np.ndarray, list[dict[str, object]]]:
    """Trace a generous corridor above each expression's real upper lash."""

    height, width = detail.shape
    band = np.zeros((height, width), dtype=bool)
    selected_mask = np.zeros((height, width), dtype=bool)
    selected: list[dict[str, object]] = []
    for center_x_value, center_y_value in eye_centers:
        center_x = int(round(float(center_x_value)))
        center_y = int(round(float(center_y_value)))
        x0 = max(0, center_x - 78)
        x1 = min(width, center_x + 79)
        y0 = max(0, center_y - 34)
        y1 = min(height, center_y + 17)
        local = (detail & dark_ink)[y0:y1, x0:x1].astype(np.uint8)
        count, labels, stats, centroids = cv2.connectedComponentsWithStats(
            local, connectivity=8
        )
        candidates: list[tuple[float, int]] = []
        for label in range(1, count):
            _, _, component_width, _, area = (int(value) for value in stats[label])
            if area < 8 or component_width < 10:
                continue
            centroid_y = float(centroids[label, 1] + y0)
            score = (
                component_width * 4.0
                + area * 0.5
                - abs(centroid_y - (center_y - 3.0)) * 5.0
            )
            candidates.append((score, label))
        if not candidates:
            raise RuntimeError(
                f"Could not locate upper lash near eye {(center_x, center_y)}"
            )
        score, label = max(candidates)
        component = labels == label
        selected_mask[y0:y1, x0:x1] |= component
        component_xs = np.nonzero(component)[1]
        local_min_x = int(component_xs.min())
        local_max_x = int(component_xs.max())
        profile_x: list[int] = []
        profile_y: list[int] = []
        for local_x in range(local_min_x, local_max_x + 1):
            ys = np.nonzero(component[:, local_x])[0]
            if len(ys):
                profile_x.append(local_x + x0)
                profile_y.append(int(ys.min()) + y0)
        full_x = np.arange(profile_x[0], profile_x[-1] + 1)
        top_y = np.interp(full_x, profile_x, profile_y)
        top_y = cv2.medianBlur(np.rint(top_y).astype(np.float32)[None, :], 5)[0].astype(
            int
        )
        profile_median = int(round(float(np.median(top_y))))
        top_y = np.clip(top_y, profile_median - 5, profile_median + 5)
        for x, top in zip(full_x, top_y, strict=True):
            band[max(0, int(top) - 16) : max(0, int(top)), int(x)] = True
        x, y, component_width, component_height, area = (
            int(value) for value in stats[label]
        )
        selected.append(
            {
                "eye_center": [center_x, center_y],
                "component_area": area,
                "component_bbox": [
                    x + x0,
                    y + y0,
                    x + x0 + component_width,
                    y + y0 + component_height,
                ],
                "component_score": round(float(score), 3),
                "profile_y_median": profile_median,
            }
        )
    band = cv2.dilate(
        band.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
    ).astype(bool)
    return band, selected_mask, selected


def remove_pale_upper_lid_arcs(
    face_rgb: np.ndarray,
    featureless_rgb: np.ndarray,
    base_alpha: np.ndarray,
    eye_centers: np.ndarray,
) -> tuple[np.ndarray, dict[str, object]]:
    """Scrub light source-painted lid arcs before the oval is sliced.

    Unlike the retired semantic repair, this is a source-RGB preprocessing step.
    It fills the entire qualifying skin-colored corridor and nothing later
    restores pixels from sparse feature masks.
    """

    face_luminance = rgb_luminance(face_rgb)
    featureless_luminance = rgb_luminance(featureless_rgb)
    luminance_drop = featureless_luminance - face_luminance
    channel_delta = np.max(
        np.abs(face_rgb.astype(np.int16) - featureless_rgb.astype(np.int16)), axis=2
    )
    minimum_channel = face_rgb.min(axis=2)
    dark_ink = (face_luminance <= 135.0) & (minimum_channel <= 112)
    detail = channel_delta >= 5
    band, selected_lash, lash_metrics = lash_relative_band(
        detail, dark_ink, eye_centers
    )
    keep_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 3))
    dark_keep = cv2.dilate((dark_ink & detail).astype(np.uint8), keep_kernel).astype(
        bool
    )
    lash_keep = cv2.dilate(selected_lash.astype(np.uint8), keep_kernel).astype(bool)
    corridor = (
        band
        & ~dark_keep
        & ~lash_keep
        & skin_pixels(face_rgb)
        & skin_pixels(featureless_rgb)
        & (base_alpha == 255)
    )
    seed = corridor & (channel_delta >= 2) & (luminance_drop >= 0.25)
    cleanup = cv2.morphologyEx(
        seed.astype(np.uint8),
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
    ).astype(bool)
    cleanup &= corridor & (channel_delta >= 1) & (luminance_drop >= 0.0)
    if not np.any(cleanup):
        raise RuntimeError("Upper-lid cleanup mask is empty")
    cleaned = face_rgb.copy()
    cleaned[cleanup] = featureless_rgb[cleanup]
    if not np.array_equal(cleaned[dark_keep], face_rgb[dark_keep]):
        raise RuntimeError("Upper-lid scrub altered protected dark features")
    return cleaned, {
        "method": "pre-slice-lash-relative-light-arc-scrub",
        "band_pixels": int(band.sum()),
        "band_bbox": mask_bbox(band),
        "protected_dark_pixels": int(dark_keep.sum()),
        "cleanup_pixels": int(cleanup.sum()),
        "cleanup_bbox": mask_bbox(cleanup),
        "cleanup_sha256": sha256_bytes(cleanup.astype(np.uint8).tobytes()),
        "lash_components": lash_metrics,
    }


def source_inputs() -> tuple[np.ndarray, np.ndarray, dict[str, object], np.ndarray]:
    source_head = load_rgba(PART_DIR / "forward_head.png", SOURCE_CANVAS)
    source_neutral = load_rgba(SOURCE_DIR / "face_neut.png", SOURCE_CANVAS)
    source_composite = alpha_composite(source_head, source_neutral)
    source_eyes = amber_iris_centers(source_composite, SOURCE_EYE_ROI)
    metrics = json.loads((SOURCE_DIR / "metrics.json").read_text(encoding="utf-8"))
    production_matrix = np.asarray(metrics["production_matrix"], dtype=np.float32)
    return source_neutral, source_eyes, metrics, production_matrix


def render_expression_layer(
    emotion: str,
    base: np.ndarray,
    featureless_rgb: np.ndarray,
    alpha: np.ndarray,
    center: tuple[float, float],
    target_eyes: np.ndarray,
    source_to_target: np.ndarray,
    source_metrics: dict[str, object],
    production_matrix: np.ndarray,
) -> tuple[np.ndarray, dict[str, object]]:
    master_name = MASTER_OVERRIDES.get(emotion, f"expression_{emotion}.png")
    master_path = MASTER_DIR / master_name
    donor = load_rgb(master_path, SOURCE_CANVAS)
    layers = source_metrics["layers"]
    assert isinstance(layers, dict)
    layer_metrics = layers[emotion]
    assert isinstance(layer_metrics, dict)
    registration = layer_metrics["registration"]
    assert isinstance(registration, dict)
    donor_to_source = registration_matrix(registration)
    donor_to_production = compose_affine(production_matrix, donor_to_source)
    donor_to_target = compose_affine(source_to_target, donor_to_production)
    warped = warp_rgb(donor, donor_to_target)
    corrected, offsets, samples = skin_match(
        warped, base[:, :, :3], base[:, :, 3], alpha, center
    )
    corrected, arc_cleanup = remove_pale_upper_lid_arcs(
        corrected, featureless_rgb, base[:, :, 3], target_eyes
    )

    registered_checker = warp_mask(border_checker_mask(donor), donor_to_target)
    checker_core = registered_checker & (alpha == 255)
    checker_fringe = registered_checker & (alpha > 0) & (alpha < 255)
    if np.any(checker_core):
        raise RuntimeError(
            f"{emotion}: {int(checker_core.sum())} checker pixels entered the solid core"
        )
    # This should be zero with the fixed lower cutoff.  Keeping the fallback
    # makes future source drift safe without changing the common alpha plane.
    corrected[checker_fringe] = base[:, :, :3][checker_fringe]
    layer = np.dstack((corrected, alpha))
    layer[alpha == 0, :3] = 0
    return layer, {
        "master": master_name,
        "master_to_target_matrix": donor_to_target.astype(float).tolist(),
        "skin_offsets": offsets,
        "skin_samples": samples,
        "upper_lid_cleanup": arc_cleanup,
        "checker_core_pixels": int(checker_core.sum()),
        "checker_fringe_pixels": int(checker_fringe.sum()),
    }


def expected_face_names() -> list[str]:
    return [
        f"face_{expression}_{outfit}.png"
        for outfit in OUTFITS
        for expression in EXPRESSIONS
    ]


def build(staging: Path) -> Path:
    built = staging / "built"
    built.mkdir(parents=True, exist_ok=True)
    source_neutral, source_eyes, source_metrics, production_matrix = source_inputs()
    master_paths = [
        MASTER_DIR / MASTER_OVERRIDES.get(emotion, f"expression_{emotion}.png")
        for emotion in EMOTIONS
    ]
    report: dict[str, object] = {
        "schema": "tsubaki-oval-faceplate-v1",
        "architecture": "intact outfit base plus registered full-master oval",
        "canvas": list(CANVAS),
        "plate_radius": list(PLATE_RADIUS),
        "plate_center_below_eyes": PLATE_CENTER_BELOW_EYES,
        "plate_solid_radius": PLATE_SOLID_RADIUS,
        "plate_lower_fade": list(PLATE_LOWER_FADE),
        "source_bundles": {
            "masters": bundle_sha256(master_paths),
            "registration": bundle_sha256(
                [SOURCE_DIR / "metrics.json", PART_DIR / "forward_head.png"]
            ),
            "bases": bundle_sha256(
                [ASSET_DIR / spec["base"] for spec in OUTFITS.values()]
            ),
            "featureless": bundle_sha256(
                [FEATURELESS_DIR / spec["featureless"] for spec in OUTFITS.values()]
            ),
        },
        "outfits": {},
    }
    transparent = np.zeros((CANVAS[1], CANVAS[0], 4), dtype=np.uint8)

    for outfit, spec in OUTFITS.items():
        base_path = ASSET_DIR / str(spec["base"])
        base = load_rgba(base_path, CANVAS)
        target_eyes = amber_iris_centers(base, spec["target_roi"])
        source_to_target = similarity_from_two_points(source_eyes, target_eyes)
        center = plate_center(target_eyes)
        alpha = oval_alpha(base[:, :, 3], center)
        if int((alpha == 255).sum()) < 42_000 or int((alpha > 0).sum()) < 60_000:
            raise RuntimeError(f"{outfit}: oval plate is unexpectedly small")
        brow_footprint = neutral_brow_footprint(
            source_neutral, source_to_target, target_eyes, base[:, :, 3]
        )
        if np.any(alpha[brow_footprint] != 255):
            raise RuntimeError(f"{outfit}: oval does not fully own the neutral brows")
        featureless_source = load_rgb(
            FEATURELESS_DIR / str(spec["featureless"]), CANVAS
        )
        featureless_rgb, featureless_offsets, featureless_samples = skin_match(
            featureless_source,
            base[:, :, :3],
            base[:, :, 3],
            alpha,
            center,
        )

        save_rgba(built / f"face_neut_{outfit}.png", transparent)
        outfit_report: dict[str, object] = {
            "base": str(base_path.relative_to(ROOT)).replace("\\", "/"),
            "base_sha256": file_sha256(base_path),
            "source_eye_centers": source_eyes.round(4).tolist(),
            "target_eye_centers": target_eyes.round(4).tolist(),
            "source_to_target_matrix": source_to_target.astype(float).tolist(),
            "plate_center": [round(value, 4) for value in center],
            "alpha_bbox": mask_bbox(alpha > 0),
            "visible_alpha_pixels": int((alpha > 0).sum()),
            "opaque_alpha_pixels": int((alpha == 255).sum()),
            "partial_alpha_pixels": int(((alpha > 0) & (alpha < 255)).sum()),
            "alpha_sha256": sha256_bytes(alpha.tobytes()),
            "neutral_brow_ownership": {
                "pixels": int(brow_footprint.sum()),
                "bbox": mask_bbox(brow_footprint),
                "sha256": sha256_bytes(brow_footprint.astype(np.uint8).tobytes()),
            },
            "featureless_skin_offsets": featureless_offsets,
            "featureless_skin_samples": featureless_samples,
            "layers": {},
        }
        layers = outfit_report["layers"]
        assert isinstance(layers, dict)

        for emotion in EMOTIONS:
            layer, layer_report = render_expression_layer(
                emotion,
                base,
                featureless_rgb,
                alpha,
                center,
                target_eyes,
                source_to_target,
                source_metrics,
                production_matrix,
            )
            destination = built / f"face_{emotion}_{outfit}.png"
            save_rgba(destination, layer)
            composite = alpha_composite(base, layer)
            layer_report.update(
                {
                    "layer_sha256": file_sha256(destination),
                    "head_composite_sha256": sha256_bytes(
                        composite[230:575, 320:705].tobytes()
                    ),
                }
            )
            layers[emotion] = layer_report

        outfits = report["outfits"]
        assert isinstance(outfits, dict)
        outfits[outfit] = outfit_report

    metrics_path = staging / "metrics.json"
    metrics_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return metrics_path


def neutral_brow_footprint(
    source_neutral: np.ndarray,
    source_to_target: np.ndarray,
    target_eyes: np.ndarray,
    base_alpha: np.ndarray,
) -> np.ndarray:
    registered = cv2.warpAffine(
        source_neutral[:, :, 3],
        source_to_target,
        CANVAS,
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )
    height, width = base_alpha.shape
    yy, xx = np.indices((height, width))
    left = float(target_eyes[0, 0] - 60)
    right = float(target_eyes[1, 0] + 60)
    top = float(min(target_eyes[:, 1]) - 70)
    bottom = float(target_eyes[:, 1].mean() - 5)
    roi = (xx >= left) & (xx <= right) & (yy >= top) & (yy <= bottom)
    return roi & (registered >= 8) & (base_alpha > 0)


def validate(staging: Path, *, installed: bool = False) -> list[str]:
    built = staging / "built"
    metrics_path = staging / "metrics.json"
    errors: list[str] = []
    if not metrics_path.is_file():
        return [f"missing build metrics: {metrics_path}"]
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    if metrics.get("schema") != "tsubaki-oval-faceplate-v1":
        errors.append("metrics schema is not tsubaki-oval-faceplate-v1")

    source_neutral, source_eyes, source_metrics, production_matrix = source_inputs()
    current_bundles = {
        "masters": bundle_sha256(
            [
                MASTER_DIR / MASTER_OVERRIDES.get(emotion, f"expression_{emotion}.png")
                for emotion in EMOTIONS
            ]
        ),
        "registration": bundle_sha256(
            [SOURCE_DIR / "metrics.json", PART_DIR / "forward_head.png"]
        ),
        "bases": bundle_sha256([ASSET_DIR / spec["base"] for spec in OUTFITS.values()]),
        "featureless": bundle_sha256(
            [FEATURELESS_DIR / spec["featureless"] for spec in OUTFITS.values()]
        ),
    }
    if metrics.get("source_bundles") != current_bundles:
        errors.append(
            "build provenance no longer matches current masters/registration/bases"
        )
    expected_names = set(expected_face_names())
    actual_names = {path.name for path in built.glob("face_*.png")}
    if actual_names != expected_names:
        errors.append(
            f"built face manifest mismatch: missing={sorted(expected_names - actual_names)}, "
            f"extra={sorted(actual_names - expected_names)}"
        )

    for outfit, spec in OUTFITS.items():
        base = load_rgba(ASSET_DIR / str(spec["base"]), CANVAS)
        target_eyes = amber_iris_centers(base, spec["target_roi"])
        source_to_target = similarity_from_two_points(source_eyes, target_eyes)
        center = plate_center(target_eyes)
        expected_alpha = oval_alpha(base[:, :, 3], center)
        featureless_source = load_rgb(
            FEATURELESS_DIR / str(spec["featureless"]), CANVAS
        )
        featureless_rgb, _, _ = skin_match(
            featureless_source,
            base[:, :, :3],
            base[:, :, 3],
            expected_alpha,
            center,
        )
        brow_footprint = neutral_brow_footprint(
            source_neutral, source_to_target, target_eyes, base[:, :, 3]
        )
        brow_metrics = {
            "pixels": int(brow_footprint.sum()),
            "bbox": mask_bbox(brow_footprint),
            "sha256": sha256_bytes(brow_footprint.astype(np.uint8).tobytes()),
        }
        if brow_metrics != EXPECTED_BROW_FOOTPRINTS[outfit]:
            errors.append(
                f"{outfit}: incumbent neutral-brow footprint drifted: {brow_metrics}"
            )
        recorded_outfit = metrics.get("outfits", {}).get(outfit, {})
        if recorded_outfit.get("neutral_brow_ownership") != brow_metrics:
            errors.append(f"{outfit}: recorded neutral-brow footprint is not exact")

        alphas: list[bytes] = []
        head_hashes: set[str] = set()
        for expression in EXPRESSIONS:
            path = built / f"face_{expression}_{outfit}.png"
            if not path.is_file():
                continue
            layer = load_rgba(path, CANVAS)
            alpha = layer[:, :, 3]
            if expression == "neut":
                if np.any(layer):
                    errors.append(
                        f"{path.name}: neutral compatibility layer is not empty"
                    )
                continue
            alphas.append(alpha.tobytes())
            if not np.array_equal(alpha, expected_alpha):
                errors.append(f"{path.name}: alpha is not the canonical smooth oval")
            if np.any(layer[alpha == 0, :3]):
                errors.append(f"{path.name}: hidden RGB remains under alpha zero")
            if np.any(alpha[base[:, :, 3] == 0]):
                errors.append(f"{path.name}: oval escapes the canonical silhouette")
            uncovered_brow = int((brow_footprint & (alpha != 255)).sum())
            if uncovered_brow:
                errors.append(
                    f"{path.name}: {uncovered_brow} incumbent brow pixels are not opaque"
                )
            expected_layer, expected_report = render_expression_layer(
                expression,
                base,
                featureless_rgb,
                expected_alpha,
                center,
                target_eyes,
                source_to_target,
                source_metrics,
                production_matrix,
            )
            if not np.array_equal(layer, expected_layer):
                differing = int(np.any(layer != expected_layer, axis=2).sum())
                errors.append(
                    f"{path.name}: {differing} pixels differ from direct registered-master replay"
                )
            if (
                expected_report["checker_core_pixels"]
                or expected_report["checker_fringe_pixels"]
            ):
                errors.append(
                    f"{path.name}: checker matte reaches face plate: "
                    f"core={expected_report['checker_core_pixels']} "
                    f"fringe={expected_report['checker_fringe_pixels']}"
                )
            composite = alpha_composite(base, layer)
            solid = alpha == 255
            if not np.array_equal(composite[:, :, :3][solid], layer[:, :, :3][solid]):
                errors.append(
                    f"{path.name}: base RGB survives inside the solid plate core"
                )
            head_hashes.add(sha256_bytes(composite[230:575, 320:705].tobytes()))
            recorded_layer = recorded_outfit.get("layers", {}).get(expression, {})
            if recorded_layer.get("layer_sha256") != file_sha256(path):
                errors.append(f"{path.name}: metrics do not pin the staged layer bytes")

        if alphas and any(alpha != alphas[0] for alpha in alphas[1:]):
            errors.append(f"{outfit}: expression alpha masks are not pixel-identical")
        if len(head_hashes) != len(EMOTIONS):
            errors.append(
                f"{outfit}: expected {len(EMOTIONS)} distinct composites, got {len(head_hashes)}"
            )
        if int((expected_alpha > 0).sum()) < 60_000:
            errors.append(f"{outfit}: plate does not have full-face oval coverage")

    definition_source = DEFINITIONS.read_text(encoding="utf-8")
    for outfit, spec in OUTFITS.items():
        if f'"assets/characters/tsubaki/{spec["base"]}"' not in definition_source:
            errors.append(f"definition misses {spec['base']}")
        for expression in EXPRESSIONS:
            reference = f'"assets/characters/tsubaki/face_{expression}_{outfit}.png"'
            if definition_source.count(reference) != 1:
                errors.append(f"definition reference count is not one: {reference}")

    if installed:
        for name in expected_names:
            staged = built / name
            production = ASSET_DIR / name
            if not production.is_file():
                errors.append(f"missing installed face: {name}")
            elif staged.is_file() and staged.read_bytes() != production.read_bytes():
                errors.append(f"installed face differs from validated build: {name}")
        for outfit, spec in OUTFITS.items():
            recorded = metrics["outfits"][outfit]["base_sha256"]
            if file_sha256(ASSET_DIR / str(spec["base"])) != recorded:
                errors.append(f"{outfit}: canonical neutral base changed after build")
    return errors


def font(size: int) -> ImageFont.ImageFont:
    for candidate in (
        Path(r"C:\Windows\Fonts\segoeui.ttf"),
        Path(r"C:\Windows\Fonts\arial.ttf"),
    ):
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def checker(size: tuple[int, int], tile: int = 16) -> Image.Image:
    image = Image.new("RGBA", size, "#e5e5e5")
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], tile):
        for x in range(0, size[0], tile):
            if ((x // tile) + (y // tile)) % 2:
                draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill="#bdbdbd")
    return image


def review(staging: Path) -> list[Path]:
    errors = validate(staging)
    if errors:
        raise RuntimeError("Refusing review:\n" + "\n".join(errors))
    built = staging / "built"
    review_dir = staging / "review"
    review_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    label_font = font(22)

    for outfit, spec in OUTFITS.items():
        base = Image.open(ASSET_DIR / str(spec["base"])).convert("RGBA")
        layouts = (
            ("composites", (320, 215, 705, 585), 1, "#ece9e2"),
            ("brows_native_3x", (385, 300, 635, 430), 3, "#ece9e2"),
            ("oval_layers", (300, 205, 720, 605), 1, "checker"),
        )
        for suffix, crop_box, scale, background in layouts:
            crop_width = crop_box[2] - crop_box[0]
            crop_height = crop_box[3] - crop_box[1]
            tile_width = crop_width * scale
            tile_height = crop_height * scale + 32
            columns = 4
            rows = math.ceil(len(EMOTIONS) / columns)
            sheet = Image.new(
                "RGBA", (columns * tile_width, rows * tile_height), "#202226"
            )
            draw = ImageDraw.Draw(sheet)
            for index, emotion in enumerate(EMOTIONS):
                layer = Image.open(built / f"face_{emotion}_{outfit}.png").convert(
                    "RGBA"
                )
                if suffix == "oval_layers":
                    canvas = checker(CANVAS)
                    canvas.alpha_composite(layer)
                else:
                    sprite = base.copy()
                    sprite.alpha_composite(layer)
                    canvas = Image.new("RGBA", CANVAS, background)
                    canvas.alpha_composite(sprite)
                tile = canvas.crop(crop_box)
                if scale != 1:
                    tile = tile.resize(
                        (tile_width, crop_height * scale), Image.Resampling.NEAREST
                    )
                x = (index % columns) * tile_width
                y = (index // columns) * tile_height
                sheet.alpha_composite(tile, (x, y + 32))
                draw.text((x + 7, y + 4), emotion, fill="#f4f4f4", font=label_font)
            output = review_dir / f"tsubaki_{outfit}_{suffix}.png"
            sheet.convert("RGB").save(output, optimize=True)
            outputs.append(output)

    # Preserve a native-pixel before/after gate for the exact uniform states
    # that exposed the eyebrow-like upper-lid artifacts in gameplay.
    focus_expressions = (
        "unamused",
        "worried",
        "disgusted",
        "annoyed",
        "embarrassed",
        "shocked",
    )
    focus_crop = (390, 305, 625, 380)
    focus_scale = 4
    focus_width = (focus_crop[2] - focus_crop[0]) * focus_scale
    focus_height = (focus_crop[3] - focus_crop[1]) * focus_scale
    focus_sheet = Image.new(
        "RGBA",
        (focus_width * 2, (focus_height + 36) * len(focus_expressions)),
        "#202226",
    )
    focus_draw = ImageDraw.Draw(focus_sheet)
    uniform_base = Image.open(ASSET_DIR / "neut_uniform.png").convert("RGBA")
    for row, expression in enumerate(focus_expressions):
        before = uniform_base.copy()
        before.alpha_composite(
            Image.open(ASSET_DIR / f"face_{expression}_uniform.png").convert("RGBA")
        )
        after = uniform_base.copy()
        after.alpha_composite(
            Image.open(built / f"face_{expression}_uniform.png").convert("RGBA")
        )
        y = row * (focus_height + 36)
        for column, (label, sprite) in enumerate(
            (("before", before), ("new oval", after))
        ):
            crop = sprite.crop(focus_crop).resize(
                (focus_width, focus_height), Image.Resampling.NEAREST
            )
            x = column * focus_width
            focus_sheet.alpha_composite(crop, (x, y + 36))
            focus_draw.text(
                (x + 8, y + 5),
                f"{expression} - {label}",
                fill="#f4f4f4",
                font=label_font,
            )
    focus_output = review_dir / "tsubaki_uniform_focus_before_after_native_4x.png"
    focus_sheet.convert("RGB").save(focus_output, optimize=True)
    outputs.append(focus_output)
    return outputs


def install(staging: Path) -> list[Path]:
    errors = validate(staging)
    if errors:
        raise RuntimeError("Refusing install:\n" + "\n".join(errors))
    built = staging / "built"
    backup = staging / "pre_install_backup"
    backup.mkdir(parents=True, exist_ok=True)
    installed: list[Path] = []
    for name in expected_face_names():
        source = built / name
        destination = ASSET_DIR / name
        backup_path = backup / name
        if destination.is_file() and not backup_path.exists():
            shutil.copy2(destination, backup_path)
        shutil.copy2(source, destination)
        installed.append(destination)
    return installed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action",
        choices=("build", "review", "validate", "install", "validate-installed", "all"),
    )
    parser.add_argument("--staging", type=Path, default=DEFAULT_STAGING)
    return parser.parse_args()


def raise_validation(errors: list[str]) -> None:
    if errors:
        raise RuntimeError("\n".join(errors))


def main() -> int:
    args = parse_args()
    staging = args.staging.resolve()
    if args.action in {"build", "all"}:
        print(f"built: {build(staging)}")
    if args.action in {"review", "all"}:
        for output in review(staging):
            print(f"review: {output}")
    if args.action in {"validate", "all"}:
        raise_validation(validate(staging))
        print("validated: 42 oval face plates; all incumbent brow pixels are owned")
    if args.action in {"install", "all"}:
        installed = install(staging)
        print(f"installed: {len(installed)} face layers")
    if args.action in {"validate-installed", "all"}:
        raise_validation(validate(staging, installed=True))
        print("validated installed: production byte-matches the oval build")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
