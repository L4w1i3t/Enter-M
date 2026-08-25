from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SPRITE_ROOT = PROJECT_ROOT / "game" / "mod_assets" / "char_sprites"
REVIEW_ROOT = Path(__file__).resolve().parent
RECOVERED_ROOT = REVIEW_ROOT / "prechange" / "recovered_layers"
OUTPUT_ROOT = REVIEW_ROOT / "facebase_v3"
CANVAS = (1023, 1537)
EXPRESSIONS = (
    "afraid",
    "angry",
    "annoyed",
    "crying",
    "curious",
    "determined",
    "disgusted",
    "embarrassed",
    "empty",
    "frustrated",
    "happy",
    "nervous",
    "panicked",
    "sad",
    "shocked",
    "smug",
    "teasing",
    "thinking",
    "unamused",
    "worried",
)


# These are forward registrations from the currently-installed face sources to
# the original neutral head. cv2.warpAffine consumes them directly.
ASAHINA_AFFINES = {
    "afraid": ((0.995, 0.0, 11.55), (0.0, 0.995, 0.65)),
    "angry": ((0.997, 0.0, 12.53), (0.0, 0.997, -2.01)),
    "annoyed": ((1.016, 0.0, -0.16), (0.0, 1.016, -6.28)),
    "crying": ((1.009, 0.0, -3.59), (0.0, 1.009, -2.97)),
    "curious": ((0.990, 0.0, 5.10), (0.0, 0.990, 3.30)),
    "determined": ((0.998, 0.0, 7.02), (0.0, 0.998, 1.66)),
    "disgusted": ((1.008, 0.0, -4.08), (0.0, 1.008, -2.64)),
    "embarrassed": ((0.992, 0.0, -0.92), (0.0, 0.992, 1.64)),
    "empty": ((1.003, 0.0, -0.53), (0.0, 1.003, -0.99)),
    "frustrated": ((0.991, 0.0, 5.59), (0.0, 0.991, 2.97)),
    "happy": ((0.992, 0.0, 5.08), (0.0, 0.992, 2.64)),
    "nervous": ((1.005, 0.0, -1.55), (0.0, 1.005, -1.65)),
    "panicked": ((0.996, 0.0, 7.04), (0.0, 0.996, 2.32)),
    "sad": ((1.004, 0.0, -2.04), (0.0, 1.004, -2.32)),
    "shocked": ((1.003, 0.0, 5.47), (0.0, 1.003, -0.99)),
    "smug": ((1.004, 0.0, -1.04), (0.0, 1.004, -1.32)),
    "teasing": ((1.002, 0.0, 3.98), (0.0, 1.002, 0.34)),
    # The scale estimate for thinking was low-confidence. Translation-only is
    # safer for this face and avoids noticeably inflating its eyes.
    "thinking": ((1.0, 0.0, -2.0), (0.0, 1.0, -6.0)),
    "unamused": ((1.008, 0.0, -3.08), (0.0, 1.008, -3.64)),
    "worried": ((1.005, 0.0, -4.55), (0.0, 1.005, -3.65)),
}

MATSUDA_TRANSLATIONS = {
    "afraid": (0, 0),
    "angry": (0, -2),
    "annoyed": (0, 0),
    "crying": (-1, 8),
    "curious": (0, -1),
    "determined": (0, -2),
    "disgusted": (0, -1),
    "embarrassed": (-2, -2),
    "empty": (0, -3),
    "frustrated": (0, -1),
    "happy": (0, 1),
    "nervous": (0, -1),
    "panicked": (1, -2),
    "sad": (0, 0),
    "shocked": (0, 0),
    "smug": (0, -1),
    "teasing": (0, -2),
    "thinking": (0, -1),
    "unamused": (0, 0),
    "worried": (0, -1),
}


@dataclass(frozen=True)
class FaceGeometry:
    face_ellipse: tuple[float, float, float, float]
    eye_left: tuple[float, float, float, float]
    eye_right: tuple[float, float, float, float]
    mouth: tuple[float, float, float, float]
    cheek_left: tuple[float, float, float, float]
    cheek_right: tuple[float, float, float, float]
    nose_keep: tuple[float, float, float, float]


GEOMETRY = {
    "asahina": FaceGeometry(
        face_ellipse=(507, 357, 135, 127),
        eye_left=(443, 322, 75, 56),
        eye_right=(553, 311, 78, 57),
        mouth=(507, 405, 76, 42),
        cheek_left=(438, 367, 65, 42),
        cheek_right=(571, 357, 68, 43),
        nose_keep=(505, 367, 18, 23),
    ),
    "matsuda": FaceGeometry(
        face_ellipse=(463, 337, 122, 105),
        eye_left=(410, 305, 67, 50),
        eye_right=(512, 297, 70, 51),
        mouth=(463, 367, 68, 40),
        cheek_left=(401, 348, 57, 36),
        cheek_right=(523, 342, 58, 36),
        nose_keep=(462, 347, 16, 21),
    ),
}


def load_rgba(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        assert image.size == CANVAS, f"{path}: {image.size}, expected {CANVAS}"
        return np.asarray(image.convert("RGBA")).copy()


def save_rgba(path: Path, rgba: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    clean = rgba.copy()
    clean[clean[:, :, 3] == 0, :3] = 0
    Image.fromarray(clean.astype(np.uint8), "RGBA").save(path, optimize=True)


def ellipse(shape: tuple[int, int], spec: tuple[float, float, float, float]) -> np.ndarray:
    height, width = shape
    center_x, center_y, radius_x, radius_y = spec
    y_grid, x_grid = np.ogrid[:height, :width]
    return (
        ((x_grid - center_x) / radius_x) ** 2
        + ((y_grid - center_y) / radius_y) ** 2
        <= 1.0
    )


def premultiplied_warp(rgba: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    alpha = rgba[:, :, 3].astype(np.float32) / 255.0
    premultiplied = rgba[:, :, :3].astype(np.float32) * alpha[:, :, None]
    warped_alpha = cv2.warpAffine(
        alpha,
        matrix,
        CANVAS,
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )
    warped_alpha = np.clip(warped_alpha, 0.0, 1.0)
    warped_premultiplied = cv2.warpAffine(
        premultiplied,
        matrix,
        CANVAS,
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0),
    )
    warped_rgb = np.zeros_like(warped_premultiplied)
    visible = warped_alpha > (1.0 / 255.0)
    warped_rgb[visible] = warped_premultiplied[visible] / warped_alpha[visible, None]
    return np.dstack(
        (
            np.clip(np.rint(warped_rgb), 0, 255).astype(np.uint8),
            np.clip(np.rint(warped_alpha * 255.0), 0, 255).astype(np.uint8),
        )
    )


def compose(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    return np.asarray(
        Image.alpha_composite(Image.fromarray(base, "RGBA"), Image.fromarray(overlay, "RGBA"))
    )


def build_blank_bases(character: str) -> dict[str, np.ndarray]:
    root = SPRITE_ROOT / character
    neutral_casual = load_rgba(root / "neutral.png")
    neutral_uniform = load_rgba(root / "neut_uniform.png")

    recovered_uniform = load_rgba(
        RECOVERED_ROOT / character / "neut_uniform_face_base.png"
    )
    shared_visible = (neutral_uniform[:, :, 3] > 0) & (recovered_uniform[:, :, 3] > 0)
    changed_uniform = shared_visible & np.any(
        neutral_uniform[:, :, :3] != recovered_uniform[:, :, :3], axis=2
    )

    geometry = GEOMETRY[character]
    safe_face = ellipse(neutral_uniform.shape[:2], geometry.face_ellipse)
    changed_uniform &= safe_face
    # Outfit transfer is restricted to pixels that are skin on the finished
    # featureless donor, so harmless donor changes along the bangs cannot be
    # recolored by the casual-outfit lighting fit.
    feature_erasure = changed_uniform & skin_mask(recovered_uniform, character)

    blank_uniform = neutral_uniform.copy()
    blank_uniform[changed_uniform, :3] = recovered_uniform[changed_uniform, :3]

    blank_casual = neutral_casual.copy()
    if character == "matsuda":
        recovered_casual = load_rgba(RECOVERED_ROOT / character / "neut_face_base.png")
        # The recovered casual PNG contains stray alpha away from the face. Only
        # its native face-erasure RGB is used; the original casual alpha and all
        # pixels outside the verified uniform erasure footprint remain exact.
        blank_casual[feature_erasure, :3] = recovered_casual[feature_erasure, :3]
    else:
        # There is no older casual blank for Asahina. Her two neutral heads have
        # identical geometry, but transferring the raw erasure delta also
        # transfers outfit-specific differences in the blue eyes. Instead, fit
        # a robust color/lighting map on unchanged facial skin and apply that map
        # to the already-featureless uniform plate.
        skin_uniform = skin_mask(neutral_uniform, character)
        skin_casual = skin_mask(neutral_casual, character)
        erased_margin = cv2.dilate(
            feature_erasure.astype(np.uint8),
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17)),
            iterations=1,
        ).astype(bool)
        stable = skin_uniform & skin_casual & ~erased_margin
        yy, xx = np.nonzero(stable)
        source_values = neutral_uniform[stable, :3].astype(np.float64)
        target_values = neutral_casual[stable, :3].astype(np.float64)
        features = np.column_stack(
            (
                source_values,
                np.ones(len(source_values)),
                (xx - GEOMETRY[character].face_ellipse[0]) / 150.0,
                (yy - GEOMETRY[character].face_ellipse[1]) / 150.0,
            )
        )
        coefficients, *_ = np.linalg.lstsq(features, target_values, rcond=None)
        residual = np.linalg.norm(features @ coefficients - target_values, axis=1)
        inliers = residual <= np.percentile(residual, 78)
        coefficients, *_ = np.linalg.lstsq(
            features[inliers], target_values[inliers], rcond=None
        )
        all_y, all_x = np.indices(neutral_uniform.shape[:2])
        recovered_values = recovered_uniform[:, :, :3].astype(np.float64)
        all_features = np.dstack(
            (
                recovered_values,
                np.ones(recovered_values.shape[:2] + (1,)),
                ((all_x - GEOMETRY[character].face_ellipse[0]) / 150.0)[..., None],
                ((all_y - GEOMETRY[character].face_ellipse[1]) / 150.0)[..., None],
            )
        )
        mapped = np.clip(all_features @ coefficients, 0, 255).astype(np.uint8)
        blank_casual[feature_erasure, :3] = mapped[feature_erasure]

    # The authored silhouettes are authoritative even if a recovered PNG had
    # stale/stray alpha or hidden transparent RGB.
    blank_uniform[:, :, 3] = neutral_uniform[:, :, 3]
    blank_casual[:, :, 3] = neutral_casual[:, :, 3]
    return {
        "neutral_casual": neutral_casual,
        "neutral_uniform": neutral_uniform,
        "blank_casual": blank_casual,
        "blank_uniform": blank_uniform,
        "erasure_mask": feature_erasure,
    }


def exact_neutral_overlay(neutral: np.ndarray, blank: np.ndarray) -> np.ndarray:
    changed = np.any(neutral[:, :, :3] != blank[:, :, :3], axis=2)
    changed &= neutral[:, :, 3] == 255
    overlay = np.zeros_like(neutral)
    overlay[changed, :3] = neutral[changed, :3]
    overlay[changed, 3] = 255
    return overlay


def skin_mask(blank: np.ndarray, character: str) -> np.ndarray:
    rgb = blank[:, :, :3].astype(np.int16)
    red, green, blue = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    warm_skin = (
        (red >= 145)
        & (green >= 100)
        & (blue >= 85)
        & (red >= green - 4)
        & (green >= blue - 12)
        & ((red - blue) >= 16)
    )
    return (
        warm_skin
        & (blank[:, :, 3] >= 245)
        & ellipse(blank.shape[:2], GEOMETRY[character].face_ellipse)
    )


def color_delta(source: np.ndarray, blank: np.ndarray) -> np.ndarray:
    return np.max(
        np.abs(source[:, :, :3].astype(np.int16) - blank[:, :, :3].astype(np.int16)),
        axis=2,
    ).astype(np.uint8)


def retain_components(seed: np.ndarray, minimum_area: int) -> np.ndarray:
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        seed.astype(np.uint8), connectivity=8
    )
    result = np.zeros(seed.shape, dtype=np.uint8)
    for label in range(1, count):
        if stats[label, cv2.CC_STAT_AREA] >= minimum_area:
            result[labels == label] = 255
    return result


def retain_components_touching(
    seed: np.ndarray, anchor: np.ndarray, minimum_area: int
) -> np.ndarray:
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        seed.astype(np.uint8), connectivity=8
    )
    result = np.zeros(seed.shape, dtype=np.uint8)
    for label in range(1, count):
        component = labels == label
        if stats[label, cv2.CC_STAT_AREA] >= minimum_area and np.any(component & anchor):
            result[component] = 255
    return result


def build_expression_overlay(
    character: str,
    expression: str,
    source: np.ndarray,
    blank_uniform: np.ndarray,
) -> tuple[np.ndarray, dict[str, int]]:
    if character == "asahina":
        matrix = np.asarray(ASAHINA_AFFINES[expression], dtype=np.float32)
    else:
        shift_x, shift_y = MATSUDA_TRANSLATIONS[expression]
        matrix = np.asarray(((1.0, 0.0, shift_x), (0.0, 1.0, shift_y)), dtype=np.float32)
    aligned = premultiplied_warp(source, matrix)

    geometry = GEOMETRY[character]
    shape = aligned.shape[:2]
    eye_left = ellipse(shape, geometry.eye_left)
    eye_right = ellipse(shape, geometry.eye_right)
    eyes = eye_left | eye_right
    mouth = ellipse(shape, geometry.mouth)
    cheeks = ellipse(shape, geometry.cheek_left) | ellipse(shape, geometry.cheek_right)
    keep_nose = ellipse(shape, geometry.nose_keep)
    native_skin = skin_mask(blank_uniform, character)
    skin_distance = cv2.distanceTransform(native_skin.astype(np.uint8), cv2.DIST_L2, 5)
    interior_skin = native_skin & (skin_distance >= 5.0)
    strong_zone = (eyes | mouth) & interior_skin & ~keep_nose
    blush_zone = cheeks & native_skin

    delta = color_delta(aligned, blank_uniform)
    source_alpha = aligned[:, :, 3]
    rgb = aligned[:, :, :3].astype(np.int16)
    luminance = (
        0.2126 * rgb[:, :, 0] + 0.7152 * rgb[:, :, 1] + 0.0722 * rgb[:, :, 2]
    )
    channel_spread = rgb.max(axis=2) - rgb.min(axis=2)

    dark_ink = luminance <= 148
    pale_feature = (
        (rgb.min(axis=2) >= 176) & (channel_spread <= 42) & (delta >= 20)
    )
    if character == "asahina":
        colored_iris = (
            (rgb[:, :, 2] >= rgb[:, :, 0] + 5)
            & (rgb[:, :, 2] >= rgb[:, :, 1] - 4)
            & (channel_spread >= 28)
        )
    else:
        colored_iris = (
            (rgb[:, :, 1] >= rgb[:, :, 0] + 4)
            & (rgb[:, :, 1] >= rgb[:, :, 2] - 5)
            & (channel_spread >= 25)
        )
    red_mouth = (
        ((rgb[:, :, 0] - rgb[:, :, 1]) >= 18)
        & ((rgb[:, :, 0] - rgb[:, :, 2]) >= 12)
        & (luminance <= 192)
    )
    eye_color = dark_ink | pale_feature | colored_iris
    eye_seed_left = eye_left & eye_color
    eye_seed_right = eye_right & eye_color
    mouth_seed = mouth & (dark_ink | pale_feature | red_mouth)
    common_seed = strong_zone & (source_alpha >= 30) & (delta >= 11)

    def eye_anchor(spec: tuple[float, float, float, float]) -> np.ndarray:
        center_x, center_y, radius_x, radius_y = spec
        eye_core = ellipse(
            shape, (center_x, center_y + 4, radius_x * 0.72, radius_y * 0.58)
        )
        brow_core = ellipse(
            shape,
            (center_x, center_y - radius_y * 0.53, radius_x * 0.62, radius_y * 0.22),
        )
        return eye_core | brow_core

    mouth_x, mouth_y, mouth_rx, mouth_ry = geometry.mouth
    mouth_anchor = ellipse(
        shape, (mouth_x, mouth_y, mouth_rx * 0.70, mouth_ry * 0.68)
    )
    retained = retain_components_touching(
        common_seed & eye_seed_left, eye_anchor(geometry.eye_left), minimum_area=3
    )
    retained = np.maximum(
        retained,
        retain_components_touching(
            common_seed & eye_seed_right, eye_anchor(geometry.eye_right), minimum_area=3
        ),
    )
    retained = np.maximum(
        retained,
        retain_components_touching(
            common_seed & mouth_seed, mouth_anchor, minimum_area=3
        ),
    )
    if character == "asahina" and expression == "thinking":
        # This source contains a second shifted jaw and right face edge. Keep
        # only its authored eyes/brows and its small central thinking mouth.
        y_grid, x_grid = np.ogrid[: shape[0], : shape[1]]
        thinking_eyes = (y_grid < 350) & ((x_grid < 563) | (y_grid < 315))
        thinking_mouth = (
            (x_grid >= 455)
            & (x_grid <= 505)
            & (y_grid >= 378)
            & (y_grid <= 400)
        )
        retained[~(thinking_eyes | thinking_mouth)] = 0
    retained = cv2.morphologyEx(
        retained,
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
    )
    expanded = cv2.dilate(
        retained,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
        iterations=1,
    )
    retained[(source_alpha < 12) | ~strong_zone] = 0
    expanded[(source_alpha < 5) | ~strong_zone] = 0

    # Feather only the outside two pixels. Core expression pixels are fully
    # opaque, so they cannot reveal any face below them.
    feather = cv2.GaussianBlur(expanded, (0, 0), 0.65)
    feature_alpha = np.maximum(retained, feather)
    feature_alpha[retained >= 250] = 255

    # Heavy intentional blush is handled as a low-opacity color tint, never as a
    # generated skin patch. This preserves the base's native skin texture and
    # prevents checker/noise or a hard hole around the retained nose.
    blank_rgb = blank_uniform[:, :, :3].astype(np.int16)
    source_redness = rgb[:, :, 0] - (rgb[:, :, 1] + rgb[:, :, 2]) / 2.0
    blank_redness = blank_rgb[:, :, 0] - (
        blank_rgb[:, :, 1] + blank_rgb[:, :, 2]
    ) / 2.0
    blush_strength = np.clip(
        (source_redness - blank_redness - 9.0) * 0.9, 0.0, 42.0
    ).astype(np.uint8)
    blush_seed = (
        blush_zone
        & (source_alpha >= 28)
        & (blush_strength > 0)
        & (delta >= 10)
    )
    blush = np.where(blush_seed, blush_strength, 0).astype(np.uint8)
    blush = cv2.GaussianBlur(blush, (0, 0), 5.5)
    if expression not in {"embarrassed", "crying", "nervous"}:
        blush[:] = 0
    cheek_feather = cv2.GaussianBlur(cheeks.astype(np.uint8) * 255, (0, 0), 5.0)
    blush = np.rint(blush.astype(np.float32) * cheek_feather / 255.0).astype(np.uint8)
    blush[(source_alpha < 5) | ~native_skin] = 0

    feature_alpha[keep_nose] = 0
    final_alpha = np.maximum(feature_alpha, blush).astype(np.uint8)
    final_alpha[~native_skin] = 0

    overlay = aligned.copy()
    tint_only = (blush > feature_alpha) & (blush > 0)
    overlay[tint_only, :3] = np.asarray((238, 104, 112), dtype=np.uint8)
    overlay[:, :, 3] = final_alpha
    overlay[final_alpha == 0, :3] = 0
    return overlay, {
        "pixels": int((final_alpha > 0).sum()),
        "opaque": int((final_alpha == 255).sum()),
        "partial": int(((final_alpha > 0) & (final_alpha < 255)).sum()),
        "blush": int((blush > 0).sum()),
    }


def checker(size: tuple[int, int], tile: int = 18) -> Image.Image:
    width, height = size
    y_grid, x_grid = np.ogrid[:height, :width]
    cells = ((x_grid // tile) + (y_grid // tile)) % 2
    rgb = np.empty((height, width, 3), dtype=np.uint8)
    rgb[cells == 0] = (72, 72, 78)
    rgb[cells == 1] = (105, 105, 112)
    return Image.fromarray(rgb, "RGB")


def rgba_on_background(rgba: np.ndarray, background: Image.Image) -> Image.Image:
    return Image.alpha_composite(
        background.convert("RGBA"), Image.fromarray(rgba, "RGBA")
    ).convert("RGB")


def make_contact_sheet(
    path: Path,
    title: str,
    items: list[tuple[str, np.ndarray]],
    crop_box: tuple[int, int, int, int],
    columns: int = 5,
) -> None:
    crop_width = crop_box[2] - crop_box[0]
    crop_height = crop_box[3] - crop_box[1]
    render_width = 340
    render_height = round(crop_height * render_width / crop_width)
    label_height = 42
    margin = 12
    cell_width = render_width + margin * 2
    cell_height = render_height + label_height + margin
    rows = (len(items) + columns - 1) // columns
    title_height = 42
    sheet = Image.new(
        "RGB", (columns * cell_width, title_height + rows * cell_height), (22, 22, 26)
    )
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=16)
    draw.text((14, 12), title, font=font, fill=(245, 245, 248))
    for index, (label, rgba) in enumerate(items):
        column = index % columns
        row = index // columns
        x = column * cell_width + margin
        y = title_height + row * cell_height + margin
        crop = rgba[crop_box[1] : crop_box[3], crop_box[0] : crop_box[2]]
        background = checker((crop_width, crop_height))
        rendered = rgba_on_background(crop, background).resize(
            (render_width, render_height), Image.Resampling.LANCZOS
        )
        sheet.paste(rendered, (x, y))
        draw.text(
            (x + render_width // 2, y + render_height + 10),
            label,
            font=font,
            fill=(238, 238, 242),
            anchor="ma",
        )
    sheet.save(path, quality=96)


def main() -> None:
    reports: list[str] = []
    composites: dict[tuple[str, str, str], np.ndarray] = {}
    overlays: dict[tuple[str, str], np.ndarray] = {}
    bases_by_character: dict[str, dict[str, np.ndarray]] = {}

    for character in ("asahina", "matsuda"):
        paths = build_blank_bases(character)
        bases_by_character[character] = paths
        output = OUTPUT_ROOT / character
        save_rgba(output / "neut_face_base.png", paths["blank_casual"])
        save_rgba(output / "neut_uniform_face_base.png", paths["blank_uniform"])

        neutral_casual = exact_neutral_overlay(
            paths["neutral_casual"], paths["blank_casual"]
        )
        neutral_uniform = exact_neutral_overlay(
            paths["neutral_uniform"], paths["blank_uniform"]
        )
        save_rgba(output / "face_neut_casual.png", neutral_casual)
        save_rgba(output / "face_neut_uniform.png", neutral_uniform)

        for outfit in ("casual", "uniform"):
            base = paths[f"blank_{outfit}"]
            neutral_layer = neutral_casual if outfit == "casual" else neutral_uniform
            composites[(character, outfit, "neut")] = compose(base, neutral_layer)

        for expression in EXPRESSIONS:
            source = load_rgba(SPRITE_ROOT / character / f"face_{expression}.png")
            layer, metrics = build_expression_overlay(
                character, expression, source, paths["blank_uniform"]
            )
            overlays[(character, expression)] = layer
            save_rgba(output / f"face_{expression}.png", layer)
            reports.append(
                f"{character}/{expression}: pixels={metrics['pixels']} "
                f"opaque={metrics['opaque']} partial={metrics['partial']} "
                f"blush={metrics['blush']}"
            )
            for outfit in ("casual", "uniform"):
                composites[(character, outfit, expression)] = compose(
                    paths[f"blank_{outfit}"], layer
                )

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUTPUT_ROOT / "metrics.txt").write_text("\n".join(reports) + "\n", encoding="utf-8")

    for character, crop_box in (
        ("asahina", (315, 175, 700, 525)),
        ("matsuda", (315, 180, 625, 465)),
    ):
        for outfit in ("casual", "uniform"):
            items = [("neut", composites[(character, outfit, "neut")])]
            items.extend(
                (expression, composites[(character, outfit, expression)])
                for expression in EXPRESSIONS
            )
            make_contact_sheet(
                OUTPUT_ROOT / f"{character}_{outfit}_heads.png",
                f"{character.title()} {outfit}: featureless native base + opaque feature layers",
                items,
                crop_box,
            )

        overlay_items = [
            (expression, overlays[(character, expression)]) for expression in EXPRESSIONS
        ]
        make_contact_sheet(
            OUTPUT_ROOT / f"{character}_layers_checker.png",
            f"{character.title()} expression layers only (checker audit)",
            overlay_items,
            crop_box,
        )

    primary = [
        (
            "Asahina uniform embarrassed",
            composites[("asahina", "uniform", "embarrassed")],
        ),
        ("Asahina uniform happy", composites[("asahina", "uniform", "happy")]),
        ("Matsuda casual curious", composites[("matsuda", "casual", "curious")]),
    ]
    make_contact_sheet(
        OUTPUT_ROOT / "screenshot_expression_checks.png",
        "Exact expressions used in the three reported screenshots",
        primary,
        (300, 150, 710, 530),
        columns=3,
    )
    print(f"Wrote {OUTPUT_ROOT}")
    print("\n".join(reports))


if __name__ == "__main__":
    main()
