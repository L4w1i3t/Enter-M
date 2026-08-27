#!/usr/bin/env python3
"""Build and optionally run an isolated Ren'Py probe for Kotonoha's sprites.

The generated fixture copies only Kotonoha's two production bases, 42
outfit-conditioned face layers, and three standalone poses.  It extracts the
shipping image declarations from ``def_characters.rpy``, renders every state
on light, dark, and checker backgrounds, verifies the captures and copied
inputs, and creates labeled review sheets plus JSON metrics.

Production files are read-only inputs.  Defaults place generated files below
``tmp/kotonoha_render_probe_project`` and ``tmp/kotonoha_render_probe``;
project, source, definition, temporary, SDK, and output paths are configurable
from the command line for staged or relocated checkouts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Sequence

from PIL import Image, ImageChops, ImageDraw, ImageFont


SCRIPT_PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_CANVAS = (1023, 1537)
SCREEN_SIZE = (1280, 960)
DISPLAY_BOX = (640, 960)
HEAD_SOURCE_BOX = (270, 70, 755, 570)

PRODUCTION_PREFIX = "assets/characters/kotonoha/"
PROBE_PREFIX = "images/kotonoha/"

OUTFITS = ("casual", "work")
BASE_FILENAMES = {
    "casual": "neutral.png",
    "work": "work.png",
}
FACE_TOKENS = (
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
POSE_SPECS = (
    ("work", "pose_exact_fold", "pose_exact_fold_work.png"),
    ("casual", "pose_watching", "pose_watching_casual.png"),
    ("casual", "pose_open_hands", "pose_open_hands_casual.png"),
)
BACKGROUNDS = (
    ("light", "probe_background_light"),
    ("dark", "probe_background_dark"),
    ("checker", "probe_background_checker"),
)
SOLID_BACKGROUND_RGB = {
    "light": (236, 233, 226),
    "dark": (32, 34, 41),
}

OPTIONS = '''define config.name = "Kotonoha Sprite Probe"
define config.version = "1.0"
define config.screen_width = 1280
define config.screen_height = 960
define config.developer = True
define config.save_directory = None
define config.autosave_on_quit = False
'''

PROBE_SCRIPT_HEADER = r'''
image probe_background_light = Solid("#ece9e2")
image probe_background_dark = Solid("#202229")
image probe_background_checker = Tile("images/probe_checker.png")

transform probe_center:
    xalign 0.5
    yalign 1.0


label start:
    python:
        import os
        _kotonoha_probe_dir = os.environ["KOTONOHA_PROBE_DIR"].replace("\\", "/")
'''


@dataclass(frozen=True)
class ProbePaths:
    """Resolved paths used by one probe invocation."""

    project_root: Path
    temp_root: Path
    source_images: Path
    character_definitions: Path
    probe_root: Path
    screenshot_dir: Path
    renpy_python: Path
    renpy_entry: Path

    @property
    def probe_game(self) -> Path:
        return self.probe_root / "game"

    @property
    def probe_images(self) -> Path:
        return self.probe_game / "images" / "kotonoha"


def face_layer_filenames() -> tuple[str, ...]:
    """Return the exact 42-layer contract in deterministic render order."""

    return tuple(
        f"face_{token}_{outfit}.png"
        for outfit in OUTFITS
        for token in FACE_TOKENS
    )


def all_runtime_filenames() -> tuple[str, ...]:
    return (
        *(BASE_FILENAMES[outfit] for outfit in OUTFITS),
        *face_layer_filenames(),
        *(filename for _outfit, _token, filename in POSE_SPECS),
    )


def top_level_block(source: str, header: str) -> str:
    """Return one top-level Ren'Py statement and its indented body."""

    lines = source.splitlines(keepends=True)
    try:
        start = next(
            index for index, line in enumerate(lines) if line.rstrip() == header
        )
    except StopIteration as exc:
        raise ValueError(f"Missing Ren'Py block: {header}") from exc

    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line.strip() and not line[0].isspace():
            end = index
            break
    return "".join(lines[start:end]).rstrip()


def expected_attribute_lines() -> Counter[str]:
    lines = ["attribute casual default:", "attribute work:"]
    for token in FACE_TOKENS:
        casual_default = " default" if token == "neut" else ""
        lines.extend(
            (
                f'attribute {token}{casual_default} if_all "casual":',
                f'attribute {token} if_all "work":',
            )
        )
    return Counter(lines)


def runtime_definition_block(paths: ProbePaths) -> str:
    """Extract and validate Kotonoha's production-facing image statements."""

    source = paths.character_definitions.read_text(encoding="utf-8")
    transform = top_level_block(source, "transform kotonoha_sprite_size:")
    layered = top_level_block(source, "layeredimage kotonoha:")

    if "group pose:" in layered:
        raise ValueError("Kotonoha probe found a layered-image pose group")
    if "at kotonoha_sprite_size, Flatten" not in layered:
        raise ValueError(
            "Kotonoha layered image no longer uses its fixed flattened size"
        )

    actual_attributes = Counter(
        line.strip()
        for line in layered.splitlines()
        if line.lstrip().startswith("attribute ")
    )
    expected_attributes = expected_attribute_lines()
    if actual_attributes != expected_attributes:
        missing = sorted((expected_attributes - actual_attributes).elements())
        extra = sorted((actual_attributes - expected_attributes).elements())
        raise ValueError(
            "Kotonoha layered-image attributes changed; "
            f"missing={missing}, extra={extra}"
        )

    layered_assets = re.findall(
        re.escape(PRODUCTION_PREFIX) + r'([^"\n]+\.png)', layered
    )
    expected_layered_assets = Counter(
        (*BASE_FILENAMES.values(), *face_layer_filenames())
    )
    actual_layered_assets = Counter(layered_assets)
    if actual_layered_assets != expected_layered_assets:
        missing = sorted(
            (expected_layered_assets - actual_layered_assets).elements()
        )
        extra = sorted(
            (actual_layered_assets - expected_layered_assets).elements()
        )
        raise ValueError(
            "Kotonoha layered-image file contract changed; "
            f"missing={missing}, extra={extra}"
        )

    expected_poses = {
        f"kotonoha {outfit} {token}": filename
        for outfit, token, filename in POSE_SPECS
    }
    pose_pattern = re.compile(
        r'^image\s+(?P<tag>kotonoha\s+(?:casual|work)\s+pose_[a-z_]+)\s*='
        r'.*?"'
        + re.escape(PRODUCTION_PREFIX)
        + r'(?P<filename>[^"\n]+\.png)"'
    )
    actual_poses: dict[str, str] = {}
    pose_lines: list[str] = []
    for line in source.splitlines():
        if not line.startswith("image kotonoha ") or " pose_" not in line:
            continue
        match = pose_pattern.match(line)
        if match is None:
            raise ValueError(f"Unrecognized Kotonoha pose declaration: {line}")
        tag = match.group("tag")
        if tag in actual_poses:
            raise ValueError(f"Duplicate Kotonoha pose declaration: {tag}")
        actual_poses[tag] = match.group("filename")
        pose_lines.append(line.rstrip())

    if actual_poses != expected_poses:
        raise ValueError(
            "Kotonoha standalone pose contract changed; "
            f"expected={expected_poses}, actual={actual_poses}"
        )

    block = "\n\n".join((transform, layered, "\n".join(pose_lines))) + "\n"
    if re.search(r"(?:^|[/_])(old|post_)", block, flags=re.IGNORECASE):
        raise ValueError("Kotonoha production definitions reference obsolete assets")
    return block.replace(PRODUCTION_PREFIX, PROBE_PREFIX)


def expression_records(background: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    number = 1
    for outfit in OUTFITS:
        for token in FACE_TOKENS:
            relative = Path(background) / "expressions" / (
                f"{number:02d}_{outfit}_{token}.png"
            )
            records.append(
                {
                    "background": background,
                    "kind": "expression",
                    "outfit": outfit,
                    "token": token,
                    "display": f"kotonoha {outfit} {token}",
                    "label": f"{outfit} {token}",
                    "relative_path": relative.as_posix(),
                }
            )
            number += 1
    return records


def pose_records(background: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for number, (outfit, token, _filename) in enumerate(POSE_SPECS, start=1):
        relative = Path(background) / "poses" / (
            f"{number:02d}_{outfit}_{token}.png"
        )
        records.append(
            {
                "background": background,
                "kind": "pose",
                "outfit": outfit,
                "token": token,
                "display": f"kotonoha {outfit} {token}",
                "label": f"{outfit} {token}",
                "relative_path": relative.as_posix(),
            }
        )
    return records


def all_render_records() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for background, _image_name in BACKGROUNDS:
        records.extend(expression_records(background))
        records.extend(pose_records(background))
    return records


def probe_script() -> str:
    lines = [PROBE_SCRIPT_HEADER.rstrip(), ""]
    for background, image_name in BACKGROUNDS:
        lines.extend((f"    scene {image_name}", ""))
        for record in (*expression_records(background), *pose_records(background)):
            lines.extend(
                (
                    f'    show {record["display"]} at probe_center',
                    "    $ renpy.pause(0.10, hard=True)",
                    "    $ renpy.screenshot("
                    f'_kotonoha_probe_dir + "/{record["relative_path"]}")',
                    "",
                )
            )
    lines.extend(("    $ renpy.quit()", "    return", ""))
    return "\n".join(lines)


def reset_generated_directory(path: Path, temp_root: Path) -> None:
    resolved_temp_root = temp_root.resolve()
    resolved_path = path.resolve()
    if (
        resolved_path == resolved_temp_root
        or resolved_temp_root not in resolved_path.parents
    ):
        raise ValueError(f"Refusing to reset non-probe directory: {resolved_path}")
    if resolved_path.exists():
        shutil.rmtree(resolved_path)
    resolved_path.mkdir(parents=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def count_mask(mask: Image.Image) -> int:
    return mask.convert("L").histogram()[255]


def threshold_mask(channel: Image.Image, predicate: Any) -> Image.Image:
    return channel.point(lambda value: 255 if predicate(value) else 0)


def and_masks(*masks: Image.Image) -> Image.Image:
    if not masks:
        raise ValueError("At least one mask is required")
    result = masks[0]
    for mask in masks[1:]:
        result = ImageChops.multiply(result, mask)
    return result


def png_metrics(path: Path) -> dict[str, Any]:
    """Validate one source PNG and report alpha/matte residue diagnostics."""

    if not path.is_file() or path.is_symlink():
        raise FileNotFoundError(f"Missing or unsafe Kotonoha runtime asset: {path}")
    with Image.open(path) as opened:
        opened.verify()
    with Image.open(path) as opened:
        if opened.mode != "RGBA" or opened.size != SOURCE_CANVAS:
            raise ValueError(
                f"Expected RGBA {SOURCE_CANVAS}, got {opened.mode} "
                f"{opened.size}: {path}"
            )
        image = opened.copy()

    red, green, blue, alpha = image.split()
    visible = threshold_mask(alpha, lambda value: value > 0)
    hidden = threshold_mask(alpha, lambda value: value == 0)
    rgb_nonzero = threshold_mask(
        ImageChops.lighter(ImageChops.lighter(red, green), blue),
        lambda value: value > 0,
    )
    hidden_rgb_pixels = count_mask(and_masks(hidden, rgb_nonzero))
    if hidden_rgb_pixels:
        raise ValueError(
            f"Hidden RGB survived beneath zero alpha in {path}: "
            f"{hidden_rgb_pixels} pixels"
        )

    exact_checker_dark = and_masks(
        visible,
        threshold_mask(red, lambda value: value == 191),
        threshold_mask(green, lambda value: value == 194),
        threshold_mask(blue, lambda value: value == 200),
    )
    exact_checker_light = and_masks(
        visible,
        threshold_mask(red, lambda value: value == 238),
        threshold_mask(green, lambda value: value == 238),
        threshold_mask(blue, lambda value: value == 238),
    )
    near_black = and_masks(
        visible,
        threshold_mask(red, lambda value: value <= 2),
        threshold_mask(green, lambda value: value <= 2),
        threshold_mask(blue, lambda value: value <= 2),
    )
    near_white = and_masks(
        visible,
        threshold_mask(red, lambda value: value >= 253),
        threshold_mask(green, lambda value: value >= 253),
        threshold_mask(blue, lambda value: value >= 253),
    )
    magenta = and_masks(
        visible,
        threshold_mask(red, lambda value: value >= 245),
        threshold_mask(green, lambda value: value <= 32),
        threshold_mask(blue, lambda value: value >= 245),
    )
    histogram = alpha.histogram()
    return {
        "filename": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "mode": "RGBA",
        "size": list(image.size),
        "alpha_bbox_xyxy_exclusive": list(alpha.getbbox() or (0, 0, 0, 0)),
        "alpha_nonzero_pixels": sum(histogram[1:]),
        "alpha_opaque_pixels": histogram[255],
        "alpha_levels": sum(1 for count in histogram if count),
        "hidden_rgb_nonzero_pixels": hidden_rgb_pixels,
        "visible_exact_checker_dark_pixels": count_mask(exact_checker_dark),
        "visible_exact_checker_light_pixels": count_mask(exact_checker_light),
        "visible_near_black_pixels": count_mask(near_black),
        "visible_near_white_pixels": count_mask(near_white),
        "visible_magenta_pixels": count_mask(magenta),
    }


def validate_expression_composites(paths: ProbePaths) -> dict[str, Any]:
    """Ensure each face layer preserves its outfit base's exact silhouette."""

    report: dict[str, Any] = {}
    for outfit in OUTFITS:
        base_path = paths.source_images / BASE_FILENAMES[outfit]
        with Image.open(base_path) as opened:
            base = opened.convert("RGBA")
        base_alpha = base.getchannel("A")
        composite_hashes: dict[str, str] = {}
        for token in FACE_TOKENS:
            face_path = paths.source_images / f"face_{token}_{outfit}.png"
            with Image.open(face_path) as opened:
                face = opened.convert("RGBA")
            composite = Image.alpha_composite(base, face)
            alpha_difference = ImageChops.difference(
                composite.getchannel("A"), base_alpha
            )
            difference_bbox = alpha_difference.getbbox()
            if difference_bbox is not None:
                raise ValueError(
                    f"face_{token}_{outfit}.png changes the {outfit} base "
                    f"silhouette at {difference_bbox}"
                )
            composite_hashes[token] = hashlib.sha256(composite.tobytes()).hexdigest()
        duplicate_composites: dict[str, list[str]] = {}
        for token, digest in composite_hashes.items():
            duplicate_composites.setdefault(digest, []).append(token)
        duplicate_composites = {
            digest: tokens
            for digest, tokens in duplicate_composites.items()
            if len(tokens) > 1
        }
        if duplicate_composites:
            raise ValueError(
                f"{outfit} expression composites are not all distinct: "
                f"{list(duplicate_composites.values())}"
            )
        report[outfit] = {
            "base": BASE_FILENAMES[outfit],
            "base_alpha_bbox_xyxy_exclusive": list(
                base_alpha.getbbox() or (0, 0, 0, 0)
            ),
            "silhouette_preserved_for_all_faces": True,
            "unique_composites": len(set(composite_hashes.values())),
            "composite_sha256": composite_hashes,
        }
    return report


def copy_runtime_assets(paths: ProbePaths) -> list[dict[str, Any]]:
    copied: list[dict[str, Any]] = []
    for filename in all_runtime_filenames():
        lowered = filename.casefold()
        name_tokens = set(Path(filename).stem.casefold().split("_"))
        if "old" in name_tokens or lowered.startswith("post_"):
            raise ValueError(f"Disallowed Kotonoha probe source: {filename}")
        source = paths.source_images / filename
        metrics = png_metrics(source)
        destination = paths.probe_images / filename
        shutil.copy2(source, destination)
        copied_hash = sha256(destination)
        if copied_hash != metrics["sha256"]:
            raise RuntimeError(f"Probe copy hash mismatch: {filename}")
        copied.append({**metrics, "copied_sha256": copied_hash})
    return copied


def write_checker_tile(paths: ProbePaths) -> None:
    tile = Image.new("RGB", (64, 64), "#eeeeee")
    draw = ImageDraw.Draw(tile)
    draw.rectangle((0, 0, 31, 31), fill="#bfc2c8")
    draw.rectangle((32, 32, 63, 63), fill="#bfc2c8")
    tile.save(paths.probe_game / "images" / "probe_checker.png", optimize=True)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_project(paths: ProbePaths) -> dict[str, Any]:
    reset_generated_directory(paths.probe_root, paths.temp_root)
    reset_generated_directory(paths.screenshot_dir, paths.temp_root)
    paths.probe_images.mkdir(parents=True, exist_ok=True)
    for background, _image_name in BACKGROUNDS:
        (paths.screenshot_dir / background / "expressions").mkdir(parents=True)
        (paths.screenshot_dir / background / "poses").mkdir(parents=True)

    definitions = runtime_definition_block(paths)
    copied = copy_runtime_assets(paths)
    expression_composites = validate_expression_composites(paths)
    write_checker_tile(paths)
    (paths.probe_game / "options.rpy").write_text(OPTIONS, encoding="utf-8")
    (paths.probe_game / "script.rpy").write_text(
        definitions + "\n" + probe_script(), encoding="utf-8"
    )

    records = all_render_records()
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "production_directory": str(paths.source_images),
        "production_definitions": str(paths.character_definitions),
        "production_definitions_sha256": sha256(paths.character_definitions),
        "probe_project": str(paths.probe_root),
        "screenshot_directory": str(paths.screenshot_dir),
        "canvas": list(SOURCE_CANVAS),
        "screen": list(SCREEN_SIZE),
        "outfits": list(OUTFITS),
        "face_tokens": list(FACE_TOKENS),
        "pose_tokens": [
            f"kotonoha {outfit} {token}"
            for outfit, token, _filename in POSE_SPECS
        ],
        "unique_expression_renders": len(OUTFITS) * len(FACE_TOKENS),
        "unique_pose_renders": len(POSE_SPECS),
        "backgrounds": [name for name, _image_name in BACKGROUNDS],
        "expected_raw_screenshots": len(records),
        "expression_composite_validation": expression_composites,
        "copied_assets": copied,
    }
    write_json(paths.probe_root / "probe_manifest.json", manifest)
    write_json(paths.screenshot_dir / "source_metrics.json", manifest)
    return manifest


def default_font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # Pillow before 10.1.
        return ImageFont.load_default()


def centered_text(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    value: str,
    *,
    font: ImageFont.ImageFont,
    fill: str,
) -> None:
    bounds = draw.textbbox((0, 0), value, font=font)
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    x = box[0] + ((box[2] - box[0] - width) // 2)
    y = box[1] + ((box[3] - box[1] - height) // 2) - bounds[1]
    draw.text((x, y), value, font=font, fill=fill)


def display_crop_box() -> tuple[int, int, int, int]:
    screen_width, screen_height = SCREEN_SIZE
    display_width, display_height = DISPLAY_BOX
    left = (screen_width - display_width) // 2
    top = screen_height - display_height
    return (left, top, left + display_width, top + display_height)


def source_box_to_screen(
    source_box: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    source_width, source_height = SOURCE_CANVAS
    display_width, display_height = DISPLAY_BOX
    screen_width, screen_height = SCREEN_SIZE
    scale = min(display_width / source_width, display_height / source_height)
    rendered_width = source_width * scale
    rendered_height = source_height * scale
    left = (screen_width - rendered_width) / 2
    top = screen_height - rendered_height
    x0, y0, x1, y1 = source_box
    return (
        round(left + x0 * scale),
        round(top + y0 * scale),
        round(left + x1 * scale),
        round(top + y1 * scale),
    )


def head_crop_box() -> tuple[int, int, int, int]:
    return source_box_to_screen(HEAD_SOURCE_BOX)


def make_contact_sheet(
    paths: ProbePaths,
    records: Sequence[dict[str, str]],
    *,
    crop: tuple[int, int, int, int],
    thumbnail_size: tuple[int, int],
    columns: int,
    title: str,
    destination: Path,
) -> None:
    label_height = 32
    title_height = 48
    thumb_width, thumb_height = thumbnail_size
    rows = (len(records) + columns - 1) // columns
    sheet = Image.new(
        "RGB",
        (columns * thumb_width, title_height + rows * (thumb_height + label_height)),
        "#15171c",
    )
    draw = ImageDraw.Draw(sheet)
    title_font = default_font(20)
    label_font = default_font(13)
    centered_text(
        draw,
        (0, 0, sheet.width, title_height),
        title,
        font=title_font,
        fill="#f6f6f7",
    )
    resampling_modes = getattr(Image, "Resampling", Image)

    for index, record in enumerate(records):
        screenshot = paths.screenshot_dir / record["relative_path"]
        with Image.open(screenshot) as source:
            if source.size != SCREEN_SIZE:
                raise ValueError(
                    f"Expected screenshot {SCREEN_SIZE}, got {source.size}: "
                    f"{screenshot}"
                )
            thumbnail = source.convert("RGB").crop(crop).resize(
                thumbnail_size, resampling_modes.LANCZOS
            )
        column = index % columns
        row = index // columns
        x = column * thumb_width
        y = title_height + row * (thumb_height + label_height)
        sheet.paste(thumbnail, (x, y))
        label_box = (
            x,
            y + thumb_height,
            x + thumb_width,
            y + thumb_height + label_height,
        )
        draw.rectangle(label_box, fill="#111318")
        centered_text(
            draw,
            label_box,
            record["label"],
            font=label_font,
            fill="#f6f6f7",
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(destination, optimize=True)


def expected_background_pixel(
    background: str, x: int, y: int
) -> tuple[int, int, int]:
    if background in SOLID_BACKGROUND_RGB:
        return SOLID_BACKGROUND_RGB[background]
    if background != "checker":
        raise ValueError(f"Unknown probe background: {background}")
    if ((x // 32) + (y // 32)) % 2 == 0:
        return (191, 194, 200)
    return (238, 238, 238)


@lru_cache(maxsize=len(BACKGROUNDS))
def background_image(background: str) -> Image.Image:
    if background in SOLID_BACKGROUND_RGB:
        return Image.new("RGB", SCREEN_SIZE, SOLID_BACKGROUND_RGB[background])
    tile = Image.new("RGB", (64, 64), (238, 238, 238))
    draw = ImageDraw.Draw(tile)
    draw.rectangle((0, 0, 31, 31), fill=(191, 194, 200))
    draw.rectangle((32, 32, 63, 63), fill=(191, 194, 200))
    backdrop = Image.new("RGB", SCREEN_SIZE)
    for y in range(0, SCREEN_SIZE[1], tile.height):
        for x in range(0, SCREEN_SIZE[0], tile.width):
            backdrop.paste(tile, (x, y))
    return backdrop


def validate_render_screenshot(path: Path, background: str) -> dict[str, Any]:
    """Reject damaged captures and report the rendered foreground bounds."""

    sample_points = tuple(
        (x, y)
        for x in (8, 41, 96, 159, 255)
        for y in (8, 41, 96, 255, 511, 900)
    )
    with Image.open(path) as source:
        if source.size != SCREEN_SIZE:
            raise ValueError(
                f"Expected screenshot {SCREEN_SIZE}, got {source.size}: {path}"
            )
        rendered = source.convert("RGB")
    mismatches = [
        (point, rendered.getpixel(point), expected_background_pixel(background, *point))
        for point in sample_points
        if rendered.getpixel(point) != expected_background_pixel(background, *point)
    ]
    if mismatches:
        raise ValueError(
            f"Probe background fidelity failed at {len(mismatches)} sampled "
            f"pixel(s) in {path}; first mismatch={mismatches[0]}"
        )

    difference = ImageChops.difference(rendered, background_image(background))
    foreground = threshold_mask(
        ImageChops.lighter(
            ImageChops.lighter(difference.getchannel("R"), difference.getchannel("G")),
            difference.getchannel("B"),
        ),
        lambda value: value > 0,
    )
    bbox = foreground.getbbox()
    if bbox is None:
        raise ValueError(f"Rendered sprite is empty: {path}")
    if bbox[0] <= 0 or bbox[2] >= SCREEN_SIZE[0] or bbox[1] <= 0:
        raise ValueError(f"Rendered sprite is cropped at an unexpected edge: {path} {bbox}")
    return {
        "relative_path": path.as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "background_samples_verified": len(sample_points),
        "foreground_bbox_xyxy_exclusive": list(bbox),
        "foreground_pixels": count_mask(foreground),
    }


def rendered_backend(paths: ProbePaths) -> str | None:
    log_path = paths.probe_root / "log.txt"
    if not log_path.is_file():
        return None
    match = re.search(
        r"^Initializing\s+([a-z0-9]+)\s+renderer:",
        log_path.read_text(encoding="utf-8", errors="replace"),
        flags=re.MULTILINE | re.IGNORECASE,
    )
    return match.group(1).casefold() if match else None


def verify_probe_asset_hashes(paths: ProbePaths, manifest: dict[str, Any]) -> int:
    if sha256(paths.character_definitions) != manifest["production_definitions_sha256"]:
        raise RuntimeError("Production definitions changed during the probe run")
    verified = 0
    for record in manifest["copied_assets"]:
        filename = record["filename"]
        expected = record["sha256"]
        source_hash = sha256(paths.source_images / filename)
        copied_hash = sha256(paths.probe_images / filename)
        if source_hash != expected or copied_hash != expected:
            raise RuntimeError(
                f"Probe asset hash changed during rendering: {filename}; "
                f"expected={expected}, source={source_hash}, copy={copied_hash}"
            )
        verified += 1
    return verified


def assemble_review_sheets(paths: ProbePaths) -> dict[str, Any]:
    manifest_path = paths.probe_root / "probe_manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(manifest_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    records = all_render_records()
    if manifest.get("expected_raw_screenshots") != len(records):
        raise ValueError("Probe manifest screenshot count changed")

    expected_paths = {record["relative_path"] for record in records}
    actual_paths = {
        path.relative_to(paths.screenshot_dir).as_posix()
        for background, _image_name in BACKGROUNDS
        for path in (paths.screenshot_dir / background).rglob("*.png")
    }
    missing = sorted(expected_paths - actual_paths)
    unexpected = sorted(actual_paths - expected_paths)
    if missing or unexpected:
        raise ValueError(
            "Kotonoha screenshot contract failed; "
            f"missing={missing}, unexpected={unexpected}"
        )

    backend = rendered_backend(paths)
    if backend == "sw":
        raise ValueError(
            "Refusing software-renderer screenshots: this Ren'Py 8.1.1 "
            "Windows build can corrupt them. Use the accelerated renderer."
        )

    screenshot_metrics: list[dict[str, Any]] = []
    for record in records:
        path = paths.screenshot_dir / record["relative_path"]
        metrics = validate_render_screenshot(path, record["background"])
        metrics["relative_path"] = record["relative_path"]
        metrics["kind"] = record["kind"]
        metrics["outfit"] = record["outfit"]
        metrics["token"] = record["token"]
        screenshot_metrics.append(metrics)

    verified_assets = verify_probe_asset_hashes(paths, manifest)
    outputs: list[dict[str, Any]] = []
    for background, _image_name in BACKGROUNDS:
        expressions = expression_records(background)
        poses = pose_records(background)
        specifications = (
            (
                expressions,
                display_crop_box(),
                (160, 240),
                7,
                "expressions_mid_thigh",
                f"Kotonoha expressions / {background} / mid-thigh / 42 renders",
            ),
            (
                expressions,
                head_crop_box(),
                (224, 232),
                7,
                "expressions_head",
                f"Kotonoha expressions / {background} / head detail / 42 renders",
            ),
            (
                poses,
                display_crop_box(),
                (192, 288),
                3,
                "poses_mid_thigh",
                f"Kotonoha poses / {background} / mid-thigh / 3 renders",
            ),
        )
        for group, crop, thumbnail_size, columns, stem, title in specifications:
            destination = paths.screenshot_dir / f"review_{stem}_{background}.png"
            make_contact_sheet(
                paths,
                group,
                crop=crop,
                thumbnail_size=thumbnail_size,
                columns=columns,
                title=title,
                destination=destination,
            )
            outputs.append(
                {
                    "filename": destination.name,
                    "bytes": destination.stat().st_size,
                    "sha256": sha256(destination),
                }
            )

    summary: dict[str, Any] = {
        "schema_version": 1,
        "raw_screenshots": len(records),
        "unique_expressions": len(OUTFITS) * len(FACE_TOKENS),
        "unique_poses": len(POSE_SPECS),
        "backgrounds": [name for name, _image_name in BACKGROUNDS],
        "renderer": backend,
        "verified_asset_hashes": verified_assets,
        "verified_background_samples_per_screenshot": 30,
        "review_sheets": outputs,
        "screenshots": screenshot_metrics,
    }
    write_json(paths.screenshot_dir / "render_metrics.json", summary)
    return summary


def run_probe(paths: ProbePaths) -> None:
    for path in (paths.renpy_python, paths.renpy_entry):
        if not path.is_file():
            raise FileNotFoundError(path)
    environment = os.environ.copy()
    environment["KOTONOHA_PROBE_DIR"] = str(paths.screenshot_dir)
    environment["SDL_AUDIODRIVER"] = "dummy"
    environment["RENPY_PERFORMANCE_TEST"] = "0"
    environment.pop("SDL_VIDEODRIVER", None)
    environment.pop("RENPY_RENDERER", None)
    command = (
        str(paths.renpy_python),
        str(paths.renpy_entry),
        str(paths.probe_root),
        "run",
    )
    print("Running isolated Ren'Py probe:")
    print("  " + subprocess.list2cmdline(command))
    subprocess.run(command, cwd=paths.project_root, env=environment, check=True)


def print_prepare_summary(paths: ProbePaths, manifest: dict[str, Any]) -> None:
    print(f"Probe project: {paths.probe_root}")
    print(f"Render output: {paths.screenshot_dir}")
    print(
        f"Prepared {manifest['unique_expression_renders']} layered expressions "
        f"and {manifest['unique_pose_renders']} standalone poses across "
        f"{len(manifest['backgrounds'])} backgrounds "
        f"({manifest['expected_raw_screenshots']} screenshots)."
    )
    print("One-command render and review build:")
    print(f'  python "{Path(__file__).resolve()}" --run')
    print("Manual render environment:")
    print(f'  $env:KOTONOHA_PROBE_DIR="{paths.screenshot_dir}"')
    print('  $env:SDL_AUDIODRIVER="dummy"')
    print('  $env:RENPY_PERFORMANCE_TEST="0"')
    manual = (
        str(paths.renpy_python),
        str(paths.renpy_entry),
        str(paths.probe_root),
        "run",
    )
    print("  & " + subprocess.list2cmdline(manual))
    print(f'  python "{Path(__file__).resolve()}" --assemble-only')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--run",
        action="store_true",
        help="Prepare, render through the local display, verify, and build reviews.",
    )
    mode.add_argument(
        "--assemble-only",
        action="store_true",
        help="Verify and build reviews from an existing complete render output.",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=SCRIPT_PROJECT_ROOT,
        help="ENTER M project root (defaults to the parent of tools/).",
    )
    parser.add_argument(
        "--temp-root",
        type=Path,
        help="Generated-file root (defaults to PROJECT_ROOT/tmp).",
    )
    parser.add_argument(
        "--source-images",
        type=Path,
        help="Kotonoha PNG directory (defaults to the production sprite directory).",
    )
    parser.add_argument(
        "--character-definitions",
        type=Path,
        help="Ren'Py character definition file (defaults to def_characters.rpy).",
    )
    parser.add_argument(
        "--probe-root",
        type=Path,
        help="Generated Ren'Py project (must remain beneath TEMP_ROOT).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Screenshots/reviews/metrics directory (must remain beneath TEMP_ROOT).",
    )
    parser.add_argument(
        "--sdk-root",
        type=Path,
        help="Ren'Py SDK root (defaults to the checkout's matsupy-sdk).",
    )
    parser.add_argument(
        "--renpy-python",
        type=Path,
        help="Bundled Python executable; overrides --sdk-root.",
    )
    parser.add_argument(
        "--renpy-entry",
        type=Path,
        help="renpy.py or renamed equivalent; overrides --sdk-root.",
    )
    return parser.parse_args()


def resolved(path: Path) -> Path:
    return path.expanduser().resolve()


def paths_from_args(args: argparse.Namespace) -> ProbePaths:
    project_root = resolved(args.project_root)
    temp_root = resolved(args.temp_root or (project_root / "tmp"))
    source_images = resolved(
        args.source_images
        or (project_root / "game" / "assets" / "characters" / "kotonoha")
    )
    character_definitions = resolved(
        args.character_definitions
        or (project_root / "game" / "asset_definitions" / "def_characters.rpy")
    )
    probe_root = resolved(
        args.probe_root or (temp_root / "kotonoha_render_probe_project")
    )
    screenshot_dir = resolved(
        args.output_dir or (temp_root / "kotonoha_render_probe")
    )
    sdk_root = resolved(
        args.sdk_root or (project_root.parents[1] / "RenPy 8" / "matsupy-sdk")
    )
    renpy_python = resolved(
        args.renpy_python
        or (sdk_root / "lib" / "py3-windows-x86_64" / "python.exe")
    )
    renpy_entry = resolved(args.renpy_entry or (sdk_root / "matsupy.py"))
    if probe_root == screenshot_dir:
        raise ValueError("Probe project and screenshot output must be different paths")
    if probe_root in screenshot_dir.parents or screenshot_dir in probe_root.parents:
        raise ValueError(
            "Probe project and screenshot output must not contain one another"
        )
    return ProbePaths(
        project_root=project_root,
        temp_root=temp_root,
        source_images=source_images,
        character_definitions=character_definitions,
        probe_root=probe_root,
        screenshot_dir=screenshot_dir,
        renpy_python=renpy_python,
        renpy_entry=renpy_entry,
    )


def main() -> int:
    args = parse_args()
    paths = paths_from_args(args)
    if args.assemble_only:
        summary = assemble_review_sheets(paths)
        print(
            f"Verified {summary['raw_screenshots']} screenshots and assembled "
            f"{len(summary['review_sheets'])} review sheets in "
            f"{paths.screenshot_dir}"
        )
        return 0

    manifest = build_project(paths)
    print_prepare_summary(paths, manifest)
    if args.run:
        run_probe(paths)
        summary = assemble_review_sheets(paths)
        print(
            f"Rendered and verified {summary['raw_screenshots']} screenshots "
            f"with {summary['renderer']}; verified "
            f"{summary['verified_asset_hashes']} copied assets and assembled "
            f"{len(summary['review_sheets'])} review sheets."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
