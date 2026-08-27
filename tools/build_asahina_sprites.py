"""Build and review Asahina's replacement-style layered sprites.

The canonical full sprites remain ``neutral.png`` and ``neut_uniform.png``.
Fresh expression masters are staged under ``tmp/asahina_fresh/masters``; this
tool turns them into registered, full-canvas face plates and creates review
sheets used before anything is installed into ``game/``.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "tmp" / "asahina_fresh"
MASTERS = STAGING / "masters"
REVIEW = STAGING / "review"
BUILT = STAGING / "built"
ASSET_DIR = ROOT / "game" / "assets" / "characters" / "asahina"

CANVAS = (1023, 1537)
FACE_MASK_BOX = (310, 140, 670, 470)
FACE_FEATHER = 10
MAX_CANONICAL_GREEN_EXCESS = 2
POSE_NAMES = ("hairflip", "pointing", "eyeroll", "phone_panic")
OBSOLETE_ASSETS = (
    "neut_face_base.png",
    "neut_uniform_face_base.png",
    "face_neut_casual.png",
    "face_neut_uniform.png",
)

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


def _font(size: int) -> ImageFont.ImageFont:
    candidates = (
        Path(r"C:\Windows\Fonts\arial.ttf"),
        Path(r"C:\Windows\Fonts\segoeui.ttf"),
    )
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def make_master_contact_sheet() -> Path:
    """Create a tight head-crop sheet for reviewing fresh generation output."""

    REVIEW.mkdir(parents=True, exist_ok=True)
    crop_box = (285, 80, 735, 555)
    tile_size = (270, 310)
    columns = 5
    rows = (len(EMOTIONS) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * tile_size[0], rows * tile_size[1]), "#dadada")
    draw = ImageDraw.Draw(sheet)
    label_font = _font(22)

    for index, emotion in enumerate(EMOTIONS):
        source = MASTERS / f"expression_{emotion}.png"
        if not source.exists():
            raise FileNotFoundError(source)
        master = Image.open(source).convert("RGB")
        crop = master.crop(crop_box)
        crop.thumbnail((tile_size[0], tile_size[1] - 36), Image.Resampling.LANCZOS)
        x = (index % columns) * tile_size[0]
        y = (index // columns) * tile_size[1]
        sheet.paste(crop, (x + (tile_size[0] - crop.width) // 2, y + 32))
        draw.text((x + 8, y + 5), emotion, fill="#111111", font=label_font)

    output = REVIEW / "expression_masters.png"
    sheet.save(output, optimize=True)
    return output


def _edge_magnitude(image: np.ndarray) -> np.ndarray:
    gray = image.astype(np.float32).mean(axis=2)
    dx = np.zeros_like(gray)
    dy = np.zeros_like(gray)
    dx[:, 1:-1] = gray[:, 2:] - gray[:, :-2]
    dy[1:-1] = gray[2:] - gray[:-2]
    return np.hypot(dx, dy)


def _best_head_translation(base: Image.Image, master: Image.Image) -> tuple[int, int, float]:
    """Register stable hair/head edges while ignoring expression features."""

    base_rgb = np.asarray(base.convert("RGB"))
    master_rgb = np.asarray(master.convert("RGB"))
    base_edge = _edge_magnitude(base_rgb)
    master_edge = _edge_magnitude(master_rgb)
    base_alpha = np.asarray(base.getchannel("A"))

    region = np.zeros((CANVAS[1], CANVAS[0]), dtype=bool)
    region[40:560, 285:750] = True
    region[225:455, 365:625] = False
    region &= base_alpha > 32

    best = (-2.0, 0, 0)
    for dy in range(-8, 9):
        for dx in range(-8, 9):
            base_y0, base_y1 = max(0, dy), min(CANVAS[1], CANVAS[1] + dy)
            base_x0, base_x1 = max(0, dx), min(CANVAS[0], CANVAS[0] + dx)
            master_y0, master_y1 = max(0, -dy), min(CANVAS[1], CANVAS[1] - dy)
            master_x0, master_x1 = max(0, -dx), min(CANVAS[0], CANVAS[0] - dx)

            active = region[base_y0:base_y1, base_x0:base_x1]
            a = base_edge[base_y0:base_y1, base_x0:base_x1][active]
            b = master_edge[master_y0:master_y1, master_x0:master_x1][active]
            significant = (a > 7.0) | (b > 7.0)
            if significant.sum() < 500:
                continue
            a = a[significant]
            b = b[significant]
            if a.std() == 0 or b.std() == 0:
                continue
            correlation = float(np.corrcoef(a, b)[0, 1])
            if correlation > best[0]:
                best = (correlation, dx, dy)

    correlation, dx, dy = best
    return dx, dy, correlation


def _translate_rgb(image: Image.Image, dx: int, dy: int) -> Image.Image:
    translated = Image.new("RGB", CANVAS, "black")
    translated.paste(image.convert("RGB"), (dx, dy))
    return translated


def _face_alpha_mask(casual: Image.Image, uniform: Image.Image) -> Image.Image:
    """Return one fixed feathered plate mask safe over both canonical bases."""

    ellipse = Image.new("L", CANVAS, 0)
    ImageDraw.Draw(ellipse).ellipse(FACE_MASK_BOX, fill=255)
    ellipse = ellipse.filter(ImageFilter.GaussianBlur(FACE_FEATHER))
    shared_subject = Image.fromarray(
        np.minimum(
            np.asarray(casual.getchannel("A")),
            np.asarray(uniform.getchannel("A")),
        ).astype(np.uint8),
        "L",
    )
    alpha = np.minimum(np.asarray(ellipse), np.asarray(shared_subject)).astype(np.uint8)
    alpha[alpha < 2] = 0
    alpha[alpha > 253] = 255
    return Image.fromarray(alpha, "L")


def build_faces() -> dict[str, object]:
    BUILT.mkdir(parents=True, exist_ok=True)
    casual = Image.open(ASSET_DIR / "neutral.png").convert("RGBA")
    uniform = Image.open(ASSET_DIR / "neut_uniform.png").convert("RGBA")
    if casual.size != CANVAS or uniform.size != CANVAS:
        raise ValueError("Asahina canonical bases must both be 1023x1537.")

    alpha = _face_alpha_mask(casual, uniform)
    alpha_array = np.asarray(alpha)
    metrics: dict[str, object] = {
        "face_mask_box": FACE_MASK_BOX,
        "face_feather": FACE_FEATHER,
        "face_alpha_bbox": alpha.getbbox(),
        "expressions": {},
    }

    transparent = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    transparent.save(BUILT / "face_neut.png", optimize=True)

    for emotion in EMOTIONS:
        master_path = MASTERS / f"expression_{emotion}.png"
        master = Image.open(master_path).convert("RGB")
        if master.size != CANVAS:
            raise ValueError(f"{master_path} is {master.size}, expected {CANVAS}")
        dx, dy, correlation = _best_head_translation(uniform, master)
        aligned = _translate_rgb(master, dx, dy)
        rgba = aligned.convert("RGBA")
        rgba.putalpha(alpha)
        pixels = np.asarray(rgba).copy()
        pixels[alpha_array == 0, :3] = 0
        layer = Image.fromarray(pixels, "RGBA")
        layer.save(BUILT / f"face_{emotion}.png", optimize=True)
        metrics["expressions"][emotion] = {
            "translation": [dx, dy],
            "head_edge_correlation": round(correlation, 6),
        }

    return metrics


def _smoothstep(values: np.ndarray) -> np.ndarray:
    values = np.clip(values, 0.0, 1.0)
    return values * values * (3.0 - 2.0 * values)


def _key_green_background(source: Image.Image) -> Image.Image:
    """Convert the generated #00ff00 matte to clean straight-alpha RGBA."""

    rgb = np.asarray(source.convert("RGB")).astype(np.float32)
    red, green, blue = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    green_excess = green - np.maximum(red, blue)

    # The generator paints a very slight vignette/noise over the requested
    # green. The top and side borders are guaranteed empty by the prompt, so
    # use their darkest chroma as the transparent end of the matte ramp.
    border_excess = np.concatenate(
        (green_excess[:20].ravel(), green_excess[:, :20].ravel(), green_excess[:, -20:].ravel())
    )
    transparent_excess = max(170.0, float(border_excess.min()) - 2.0)
    opaque_excess = 30.0
    alpha = _smoothstep(
        (transparent_excess - green_excess) / (transparent_excess - opaque_excess)
    )
    alpha[alpha < 0.01] = 0.0
    alpha[alpha > 0.995] = 1.0

    border_rgb = np.concatenate(
        (rgb[:20].reshape(-1, 3), rgb[:, :20].reshape(-1, 3), rgb[:, -20:].reshape(-1, 3)),
        axis=0,
    )
    background = np.median(border_rgb, axis=0).astype(np.float32)
    safe_alpha = np.maximum(alpha[..., None], 1.0 / 255.0)
    foreground = (rgb - (1.0 - alpha[..., None]) * background) / safe_alpha
    foreground = np.clip(foreground, 0.0, 255.0)

    # Straight-alpha RGB at a keyed edge is numerically fragile and can retain
    # a neon fringe even when its alpha is correct. Extend the nearest fully
    # opaque foreground color through only the partial-alpha rim. This is the
    # standard texture-padding treatment used for sprites and preserves the
    # soft matte without carrying green/magenta contamination into Ren'Py.
    opaque = alpha >= 0.995
    partial = (alpha > 0.0) & ~opaque
    nearest = ndimage.distance_transform_edt(
        ~opaque,
        return_distances=False,
        return_indices=True,
    )
    nearest_rgb = rgb[nearest[0], nearest[1]]
    foreground[partial] = nearest_rgb[partial]

    # The image model can paint a narrow green bounce-light line directly on
    # otherwise opaque silhouette pixels. It is not part of Asahina's palette.
    # Replace only those chroma-contaminated pixels from the nearest clean
    # opaque texel; real skin, hair, uniform, eye, and gold-button colors all
    # have red or blue at least as strong as green.
    foreground_excess = foreground[..., 1] - np.maximum(
        foreground[..., 0], foreground[..., 2]
    )
    clean_opaque = opaque & (foreground_excess <= MAX_CANONICAL_GREEN_EXCESS)
    clean_nearest = ndimage.distance_transform_edt(
        ~clean_opaque,
        return_distances=False,
        return_indices=True,
    )
    contaminated = (alpha > 0.0) & (foreground_excess > MAX_CANONICAL_GREEN_EXCESS)
    clean_rgb = foreground[clean_nearest[0], clean_nearest[1]]
    foreground[contaminated] = clean_rgb[contaminated]
    foreground[alpha == 0.0] = 0.0

    rgba = np.dstack((foreground, alpha[..., None] * 255.0)).round().astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def build_poses() -> dict[str, object]:
    BUILT.mkdir(parents=True, exist_ok=True)
    output_names = {
        "hairflip": "pose_hairflip_uniform.png",
        "pointing": "pose_pointing_uniform.png",
        "eyeroll": "pose_eyeroll_uniform.png",
        "phone_panic": "pose_phone_panic_uniform.png",
    }
    metrics: dict[str, object] = {"poses": {}}
    for pose in POSE_NAMES:
        source_path = MASTERS / f"pose_{pose}.png"
        source = Image.open(source_path)
        if source.size != CANVAS:
            raise ValueError(f"{source_path} is {source.size}, expected {CANVAS}")
        cutout = _key_green_background(source)
        output_path = BUILT / output_names[pose]
        cutout.save(output_path, optimize=True)
        alpha = np.asarray(cutout.getchannel("A"))
        rgb = np.asarray(cutout)[..., :3].astype(np.int16)
        visible = alpha > 0
        green_excess = rgb[..., 1] - np.maximum(rgb[..., 0], rgb[..., 2])
        metrics["poses"][pose] = {
            "alpha_bbox": cutout.getchannel("A").getbbox(),
            "partially_transparent_pixels": int(((alpha > 0) & (alpha < 255)).sum()),
            "visible_green_excess_over_canonical": int(
                (visible & (green_excess > MAX_CANONICAL_GREEN_EXCESS)).sum()
            ),
        }
    # Keep the historical asset path fresh as well as the public Ren'Py image
    # alias. New code uses the descriptive filename; external tooling that
    # still opens terror.png receives identical new pixels rather than old art.
    shutil.copy2(BUILT / output_names["phone_panic"], BUILT / "terror.png")
    return metrics


def build_all() -> Path:
    metrics = build_faces()
    metrics.update(build_poses())
    metrics_path = STAGING / "metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    return metrics_path


def _checker(size: tuple[int, int], square: int = 24) -> Image.Image:
    width, height = size
    yy, xx = np.indices((height, width))
    cells = (xx // square + yy // square) % 2
    colors = np.where(cells[..., None] == 0, 235, 190).astype(np.uint8)
    return Image.fromarray(np.repeat(colors, 3, axis=2), "RGB")


def _composite(background: Image.Image, foreground: Image.Image) -> Image.Image:
    canvas = background.convert("RGBA")
    canvas.alpha_composite(foreground)
    return canvas.convert("RGB")


def _make_face_review(base_name: str, background_kind: str) -> Path:
    base = Image.open(ASSET_DIR / base_name).convert("RGBA")
    crop_box = (270, 70, 735, 565)
    tile_size = (300, 350)
    columns = 5
    rows = (len(EMOTIONS) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * tile_size[0], rows * tile_size[1]), "#d0d0d0")
    draw = ImageDraw.Draw(sheet)
    label_font = _font(21)

    if background_kind == "checker":
        backdrop = _checker(CANVAS)
    elif background_kind == "light":
        backdrop = Image.new("RGB", CANVAS, "#f5f1ea")
    elif background_kind == "dark":
        backdrop = Image.new("RGB", CANVAS, "#181a22")
    else:
        raise ValueError(background_kind)

    for index, emotion in enumerate(EMOTIONS):
        layer = Image.open(BUILT / f"face_{emotion}.png").convert("RGBA")
        composed = base.copy()
        composed.alpha_composite(layer)
        preview = _composite(backdrop, composed).crop(crop_box)
        preview.thumbnail((tile_size[0], tile_size[1] - 34), Image.Resampling.LANCZOS)
        x = (index % columns) * tile_size[0]
        y = (index // columns) * tile_size[1]
        sheet.paste(preview, (x + (tile_size[0] - preview.width) // 2, y + 30))
        draw.text((x + 7, y + 4), emotion, fill="#111111", font=label_font)

    outfit = "casual" if base_name == "neutral.png" else "uniform"
    output = REVIEW / f"faces_{outfit}_{background_kind}.png"
    sheet.save(output, optimize=True)
    return output


def make_built_review_sheets() -> list[Path]:
    REVIEW.mkdir(parents=True, exist_ok=True)
    outputs = [
        _make_face_review(base, background)
        for base in ("neutral.png", "neut_uniform.png")
        for background in ("checker", "light", "dark")
    ]

    tile_size = (280, 470)
    pose_items = (
        ("neutral", ASSET_DIR / "neut_uniform.png"),
        ("hairflip", BUILT / "pose_hairflip_uniform.png"),
        ("pointing", BUILT / "pose_pointing_uniform.png"),
        ("eyeroll", BUILT / "pose_eyeroll_uniform.png"),
        ("phone_panic", BUILT / "pose_phone_panic_uniform.png"),
    )
    sheet = Image.new("RGB", (len(pose_items) * tile_size[0], tile_size[1]), "#d0d0d0")
    draw = ImageDraw.Draw(sheet)
    label_font = _font(21)
    checker = _checker(CANVAS)
    for index, (pose, source) in enumerate(pose_items):
        cutout = Image.open(source).convert("RGBA")
        preview = _composite(checker, cutout)
        preview.thumbnail((tile_size[0], tile_size[1] - 34), Image.Resampling.LANCZOS)
        x = index * tile_size[0]
        sheet.paste(preview, (x + (tile_size[0] - preview.width) // 2, 30))
        draw.text((x + 7, 4), pose, fill="#111111", font=label_font)
    pose_output = REVIEW / "poses_checker.png"
    sheet.save(pose_output, optimize=True)
    outputs.append(pose_output)
    return outputs


def validate_built() -> list[str]:
    errors: list[str] = []
    face_masks: list[bytes] = []
    expected_face_bbox: tuple[int, int, int, int] | None = None
    for name in ("neut", *EMOTIONS):
        path = BUILT / f"face_{name}.png"
        image = Image.open(path)
        if image.mode != "RGBA" or image.size != CANVAS:
            errors.append(f"{path.name}: expected RGBA {CANVAS}, got {image.mode} {image.size}")
            continue
        alpha = image.getchannel("A")
        if name == "neut":
            if alpha.getbbox() is not None:
                errors.append("face_neut.png is not fully transparent")
            continue
        if expected_face_bbox is None:
            expected_face_bbox = alpha.getbbox()
        elif alpha.getbbox() != expected_face_bbox:
            errors.append(f"{path.name}: alpha bbox differs from the fixed face plate")
        face_masks.append(alpha.tobytes())
        pixels = np.asarray(image)
        if np.any(pixels[pixels[..., 3] == 0, :3]):
            errors.append(f"{path.name}: nonzero RGB residue in transparent pixels")
    if face_masks and any(mask != face_masks[0] for mask in face_masks[1:]):
        errors.append("expression face masks are not pixel-identical")

    pose_files = (
        "pose_hairflip_uniform.png",
        "pose_pointing_uniform.png",
        "pose_eyeroll_uniform.png",
        "pose_phone_panic_uniform.png",
        "terror.png",
    )
    for name in pose_files:
        path = BUILT / name
        image = Image.open(path)
        if image.mode != "RGBA" or image.size != CANVAS:
            errors.append(f"{name}: expected RGBA {CANVAS}, got {image.mode} {image.size}")
            continue
        alpha = np.asarray(image.getchannel("A"))
        pixels = np.asarray(image)
        if alpha[0].max() or alpha[:, 0].max() or alpha[:, -1].max():
            errors.append(f"{name}: subject touches the top or side canvas edge")
        if np.any(pixels[alpha == 0, :3]):
            errors.append(f"{name}: RGB residue remains in fully transparent pixels")
        visible = alpha > 8
        rgb = pixels[..., :3].astype(np.int16)
        green_excess = rgb[..., 1] - np.maximum(rgb[..., 0], rgb[..., 2])
        if int((visible & (green_excess > MAX_CANONICAL_GREEN_EXCESS)).sum()) != 0:
            errors.append(f"{name}: possible green-screen residue")
    if (BUILT / "terror.png").read_bytes() != (BUILT / "pose_phone_panic_uniform.png").read_bytes():
        errors.append("terror.png is not the exact fresh phone-panic compatibility copy")
    return errors


def install_built() -> list[Path]:
    errors = validate_built()
    if errors:
        raise RuntimeError("Refusing install:\n" + "\n".join(errors))
    installed: list[Path] = []
    for source in sorted(BUILT.glob("*.png")):
        destination = ASSET_DIR / source.name
        shutil.copy2(source, destination)
        installed.append(destination)
    for obsolete_name in OBSOLETE_ASSETS:
        obsolete = ASSET_DIR / obsolete_name
        if obsolete.exists():
            obsolete.unlink()
    return installed


def validate_installed() -> list[str]:
    errors = validate_built()
    for source in sorted(BUILT.glob("*.png")):
        installed = ASSET_DIR / source.name
        if not installed.exists():
            errors.append(f"missing installed asset: {installed.name}")
        elif source.read_bytes() != installed.read_bytes():
            errors.append(f"installed asset differs from staging: {installed.name}")
    for obsolete_name in OBSOLETE_ASSETS:
        if (ASSET_DIR / obsolete_name).exists():
            errors.append(f"obsolete Asahina decomposition remains installed: {obsolete_name}")

    definitions = (
        ROOT / "game" / "asset_definitions" / "def_characters.rpy"
    ).read_text(
        encoding="utf-8"
    )
    required_references = (
        '"assets/characters/asahina/neutral.png"',
        '"assets/characters/asahina/neut_uniform.png"',
        '"assets/characters/asahina/face_neut.png"',
        '"assets/characters/asahina/pose_phone_panic_uniform.png"',
    )
    for reference in required_references:
        if reference not in definitions:
            errors.append(f"missing runtime reference: {reference}")
    for obsolete_name in OBSOLETE_ASSETS:
        if f"asahina/{obsolete_name}" in definitions:
            errors.append(f"runtime still references obsolete asset: {obsolete_name}")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=(
            "contact",
            "build",
            "review",
            "validate",
            "validate-installed",
            "install",
            "all",
        ),
        help="Build the requested review artifact.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "contact":
        print(make_master_contact_sheet())
    elif args.command == "build":
        print(build_all())
    elif args.command == "review":
        print(*make_built_review_sheets(), sep="\n")
    elif args.command == "validate":
        errors = validate_built()
        if errors:
            raise SystemExit("\n".join(errors))
        print("Asahina staging validation passed.")
    elif args.command == "validate-installed":
        errors = validate_installed()
        if errors:
            raise SystemExit("\n".join(errors))
        print("Asahina installed validation passed.")
    elif args.command == "install":
        print(*install_built(), sep="\n")
    elif args.command == "all":
        print(build_all())
        print(*make_built_review_sheets(), sep="\n")
        errors = validate_built()
        if errors:
            raise SystemExit("\n".join(errors))
        print("Asahina staging validation passed.")


if __name__ == "__main__":
    main()
