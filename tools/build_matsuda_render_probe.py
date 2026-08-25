#!/usr/bin/env python3
"""Build and optionally run an isolated Ren'Py probe for Matsuda's sprites.

The probe copies only Matsuda's installed two neutral bases, 42 outfit-native
face layers, and five standalone reaction poses into a generated project under
``tmp/``.  It imports the public image statements from ``def_characters.rpy``
instead of recreating them, renders every story-facing token on light, dark,
and checker backgrounds, and can assemble labeled full-body/head contact
sheets from the resulting screenshots.

Production assets are read-only inputs.  Every generated file stays beneath
``tmp/matsuda_render_probe_project`` or ``tmp/matsuda_render_probe``.
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
from pathlib import Path
from typing import Any, Sequence

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEMP_ROOT = PROJECT_ROOT / "tmp"
PROBE_ROOT = TEMP_ROOT / "matsuda_render_probe_project"
PROBE_GAME = PROBE_ROOT / "game"
PROBE_IMAGES = PROBE_GAME / "images" / "matsuda"
SCREENSHOT_DIR = TEMP_ROOT / "matsuda_render_probe"
SOURCE_IMAGES = (
    PROJECT_ROOT / "game" / "mod_assets" / "char_sprites" / "matsuda"
)
STAGED_FACE_IMAGES = TEMP_ROOT / "matsuda_rebuild_fresh" / "faces"
CHARACTER_DEFINITIONS = (
    PROJECT_ROOT / "game" / "mod_assets" / "def_characters.rpy"
)

PRODUCTION_PREFIX = "mod_assets/char_sprites/matsuda/"
PROBE_PREFIX = "images/matsuda/"
SOURCE_CANVAS = (1023, 1537)
SCREEN_SIZE = (1280, 960)
DISPLAY_BOX = (640, 960)
HEAD_SOURCE_BOX = (300, 80, 720, 500)
EYE_LEAKAGE_SOURCE_BOX = (300, 160, 720, 500)

OUTFITS = ("casual", "uniform")
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
EYE_LEAKAGE_TOKENS = ("neut", "smug", "thinking")
EYE_LEAKAGE_STORY_SITES = (
    {
        "file": "game/story/season1/0517.rpy",
        "show_line": 297,
        "dialogue_line": 298,
        "outfit_source_line": 285,
        "outfit_source": "show matsuda casual curious",
        "display": "matsuda casual smug",
        "dialogue": "Shorter, yes, albeit far less accurate.",
    },
    {
        "file": "game/story/season1/0517.rpy",
        "show_line": 311,
        "dialogue_line": 312,
        "outfit_source_line": 285,
        "outfit_source": "show matsuda casual curious",
        "display": "matsuda casual thinking",
        "dialogue": "[player]... (Asahiko... with the default player name)",
    },
)
BASE_FILENAMES = ("neutral.png", "neut_uniform.png")
POSE_SPECS = (
    ("uniform", "pose_facepalm", "pose_facepalm_uniform.png"),
    ("uniform", "pose_chuuni", "pose_chuuni_uniform.png"),
    ("uniform", "pose_shrug", "pose_shrug_uniform.png"),
    ("casual", "pose_laughing", "pose_laughing_casual.png"),
    ("uniform", "pose_laughing", "pose_laughing_uniform.png"),
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

DEFAULT_SDK_ROOT = PROJECT_ROOT.parents[1] / "RenPy 8" / "matsupy-sdk"
DEFAULT_RENPY_PYTHON = (
    DEFAULT_SDK_ROOT / "lib" / "py3-windows-x86_64" / "python.exe"
)
DEFAULT_RENPY_ENTRY = DEFAULT_SDK_ROOT / "matsupy.py"

OPTIONS = '''define config.name = "Matsuda Sprite Probe"
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
        _matsuda_probe_dir = os.environ["MATSUDA_PROBE_DIR"].replace("\\", "/")
'''


def face_layer_filenames() -> tuple[str, ...]:
    """Return the exact 42-layer runtime contract in render order."""

    return tuple(
        f"face_{token}_{outfit}.png"
        for outfit in OUTFITS
        for token in FACE_TOKENS
    )


def all_runtime_filenames() -> tuple[str, ...]:
    return (
        *BASE_FILENAMES,
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
    lines = ["attribute casual default:", "attribute uniform:"]
    for token in FACE_TOKENS:
        casual_default = " default" if token == "neut" else ""
        lines.extend(
            (
                f'attribute {token}{casual_default} if_all "casual":',
                f'attribute {token} if_all "uniform":',
            )
        )
    return Counter(lines)


def runtime_definition_block() -> str:
    """Extract and validate Matsuda's production-facing Ren'Py statements."""

    source = CHARACTER_DEFINITIONS.read_text(encoding="utf-8")
    transform = top_level_block(source, "transform matsuda_sprite_size:")
    layered = top_level_block(source, "layeredimage matsuda:")

    if "group pose:" in layered:
        raise ValueError("Matsuda probe found a retired layered-image pose group")
    if "at matsuda_sprite_size, Flatten" not in layered:
        raise ValueError("Matsuda layered image no longer uses its fixed flattened size")

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
            "Matsuda layered-image attributes changed; "
            f"missing={missing}, extra={extra}"
        )

    layered_assets = re.findall(
        re.escape(PRODUCTION_PREFIX) + r'([^"\n]+\.png)', layered
    )
    expected_layered_assets = Counter((*BASE_FILENAMES, *face_layer_filenames()))
    if Counter(layered_assets) != expected_layered_assets:
        missing = sorted((expected_layered_assets - Counter(layered_assets)).elements())
        extra = sorted((Counter(layered_assets) - expected_layered_assets).elements())
        raise ValueError(
            "Matsuda layered-image file contract changed; "
            f"missing={missing}, extra={extra}"
        )

    expected_poses = {
        f"matsuda {outfit} {token}": filename
        for outfit, token, filename in POSE_SPECS
    }
    pose_lines: list[str] = []
    actual_poses: dict[str, str] = {}
    pose_pattern = re.compile(
        r'^image\s+(?P<tag>matsuda\s+(?:casual|uniform)\s+pose_[a-z_]+)\s*='
        r'.*?"'
        + re.escape(PRODUCTION_PREFIX)
        + r'(?P<filename>[^"\n]+\.png)"'
    )
    for line in source.splitlines():
        if not line.startswith("image matsuda "):
            continue
        match = pose_pattern.match(line)
        if match is None:
            raise ValueError(f"Unrecognized Matsuda image declaration: {line}")
        tag = match.group("tag")
        if tag in actual_poses:
            raise ValueError(f"Duplicate Matsuda image declaration: {tag}")
        actual_poses[tag] = match.group("filename")
        pose_lines.append(line.rstrip())

    if actual_poses != expected_poses:
        raise ValueError(
            "Matsuda standalone pose contract changed; "
            f"expected={expected_poses}, actual={actual_poses}"
        )

    block = "\n\n".join((transform, layered, "\n".join(pose_lines))) + "\n"
    if re.search(r"(?:^|[/_])(old|post_)", block, flags=re.IGNORECASE):
        raise ValueError("Matsuda production definitions reference obsolete assets")
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
                    "display": f"matsuda {outfit} {token}",
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
                "display": f"matsuda {outfit} {token}",
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


def probe_script(*, eye_only: bool = False) -> str:
    lines = [PROBE_SCRIPT_HEADER.rstrip(), ""]
    for background, image_name in BACKGROUNDS:
        lines.extend((f"    scene {image_name}", ""))
        records = (
            eye_leakage_records(background)
            if eye_only
            else [*expression_records(background), *pose_records(background)]
        )
        for record in records:
            lines.extend(
                (
                    f'    show {record["display"]} at probe_center',
                    "    $ renpy.pause(0.10, hard=True)",
                    "    $ renpy.screenshot("
                    f'_matsuda_probe_dir + "/{record["relative_path"]}")',
                    "",
                )
            )
    lines.extend(("    $ renpy.quit()", "    return", ""))
    return "\n".join(lines)


def reset_generated_directory(path: Path) -> None:
    resolved_temp_root = TEMP_ROOT.resolve()
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


def validate_source_png(path: Path) -> None:
    if not path.is_file() or path.is_symlink():
        raise FileNotFoundError(f"Missing or unsafe Matsuda runtime asset: {path}")
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        if image.mode != "RGBA" or image.size != SOURCE_CANVAS:
            raise ValueError(
                f"Expected RGBA {SOURCE_CANVAS}, got {image.mode} {image.size}: {path}"
            )


def copy_runtime_assets() -> list[dict[str, Any]]:
    copied: list[dict[str, Any]] = []
    for filename in all_runtime_filenames():
        lowered = filename.casefold()
        if "old" in lowered or lowered.startswith("post_"):
            raise ValueError(f"Disallowed Matsuda probe source: {filename}")
        source = SOURCE_IMAGES / filename
        validate_source_png(source)
        destination = PROBE_IMAGES / filename
        shutil.copy2(source, destination)
        source_hash = sha256(source)
        copied_hash = sha256(destination)
        if copied_hash != source_hash:
            raise RuntimeError(f"Probe copy hash mismatch: {filename}")
        copied.append(
            {
                "filename": filename,
                "bytes": source.stat().st_size,
                "sha256": source_hash,
                "copied_sha256": copied_hash,
            }
        )
    return copied


def write_checker_tile() -> None:
    tile = Image.new("RGB", (64, 64), "#eeeeee")
    draw = ImageDraw.Draw(tile)
    draw.rectangle((0, 0, 31, 31), fill="#bfc2c8")
    draw.rectangle((32, 32, 63, 63), fill="#bfc2c8")
    tile.save(PROBE_GAME / "images" / "probe_checker.png", optimize=True)


def build_project(*, eye_only: bool = False) -> dict[str, Any]:
    reset_generated_directory(PROBE_ROOT)
    reset_generated_directory(SCREENSHOT_DIR)
    PROBE_IMAGES.mkdir(parents=True, exist_ok=True)
    for background, _image_name in BACKGROUNDS:
        (SCREENSHOT_DIR / background / "expressions").mkdir(parents=True)
        (SCREENSHOT_DIR / background / "poses").mkdir(parents=True)

    definitions = runtime_definition_block()
    copied = copy_runtime_assets()
    write_checker_tile()
    (PROBE_GAME / "options.rpy").write_text(OPTIONS, encoding="utf-8")
    (PROBE_GAME / "script.rpy").write_text(
        definitions + "\n" + probe_script(eye_only=eye_only), encoding="utf-8"
    )

    render_records = eye_only_render_records() if eye_only else all_render_records()

    manifest: dict[str, Any] = {
        "schema_version": 1,
        "render_mode": "eye_only" if eye_only else "full",
        "production_directory": str(SOURCE_IMAGES.resolve()),
        "production_definitions": str(CHARACTER_DEFINITIONS.resolve()),
        "production_definitions_sha256": sha256(CHARACTER_DEFINITIONS),
        "probe_project": str(PROBE_ROOT.resolve()),
        "screenshot_directory": str(SCREENSHOT_DIR.resolve()),
        "canvas": list(SOURCE_CANVAS),
        "screen": list(SCREEN_SIZE),
        "outfits": list(OUTFITS),
        "face_tokens": list(FACE_TOKENS),
        "pose_tokens": [
            f"matsuda {outfit} {token}" for outfit, token, _filename in POSE_SPECS
        ],
        "unique_expression_renders": len(OUTFITS) * len(FACE_TOKENS),
        "unique_pose_renders": len(POSE_SPECS),
        "backgrounds": [name for name, _image_name in BACKGROUNDS],
        "expected_raw_screenshots": len(render_records),
        "copied_assets": copied,
    }
    (PROBE_ROOT / "probe_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
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
    records: Sequence[dict[str, str]],
    *,
    crop: tuple[int, int, int, int],
    thumbnail_size: tuple[int, int],
    columns: int,
    title: str,
    destination: Path,
    pixel_exact: bool = False,
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
    resampling = resampling_modes.NEAREST if pixel_exact else resampling_modes.LANCZOS

    for index, record in enumerate(records):
        screenshot = SCREENSHOT_DIR / record["relative_path"]
        with Image.open(screenshot) as source:
            if source.size != SCREEN_SIZE:
                raise ValueError(
                    f"Expected screenshot {SCREEN_SIZE}, got {source.size}: {screenshot}"
                )
            thumbnail = source.convert("RGB").crop(crop).resize(
                thumbnail_size, resampling
            )
        column = index % columns
        row = index // columns
        x = column * thumb_width
        y = title_height + row * (thumb_height + label_height)
        sheet.paste(thumbnail, (x, y))
        label_box = (x, y + thumb_height, x + thumb_width, y + thumb_height + label_height)
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


def eye_leakage_records(background: str) -> list[dict[str, str]]:
    by_attribute = {
        (record["outfit"], record["token"]): record
        for record in expression_records(background)
    }
    return [
        by_attribute[(outfit, token)]
        for outfit in OUTFITS
        for token in EYE_LEAKAGE_TOKENS
    ]


def make_runtime_eye_leakage_sheet(
    destination: Path, *, background: str = "light"
) -> None:
    crop = source_box_to_screen(EYE_LEAKAGE_SOURCE_BOX)
    width = (crop[2] - crop[0]) * 2
    height = (crop[3] - crop[1]) * 2
    make_contact_sheet(
        eye_leakage_records(background),
        crop=crop,
        thumbnail_size=(width, height),
        columns=len(EYE_LEAKAGE_TOKENS),
        title=(
            f"Matsuda eye-leakage regression / {background} / GL2 runtime "
            "pixels at 2x / neutral vs story expressions"
        ),
        destination=destination,
        pixel_exact=True,
    )


def make_source_eye_leakage_sheet(
    destination: Path,
    *,
    base_directory: Path = PROBE_IMAGES,
    face_directory: Path = PROBE_IMAGES,
    title: str = "Matsuda eye-leakage regression / isolated source composite at 1:1",
) -> None:
    x0, y0, x1, y1 = EYE_LEAKAGE_SOURCE_BOX
    crop_size = (x1 - x0, y1 - y0)
    title_height = 48
    label_height = 32
    columns = len(EYE_LEAKAGE_TOKENS)
    rows = len(OUTFITS)
    sheet = Image.new(
        "RGB",
        (
            columns * crop_size[0],
            title_height + rows * (crop_size[1] + label_height),
        ),
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
    base_names = {"casual": "neutral.png", "uniform": "neut_uniform.png"}
    backdrop = Image.new(
        "RGBA", SOURCE_CANVAS, (*SOLID_BACKGROUND_RGB["light"], 255)
    )
    outfit_tokens = (
        (outfit, token) for outfit in OUTFITS for token in EYE_LEAKAGE_TOKENS
    )

    for index, (outfit, token) in enumerate(outfit_tokens):
        base_path = base_directory / base_names[outfit]
        face_path = face_directory / f"face_{token}_{outfit}.png"
        validate_source_png(base_path)
        validate_source_png(face_path)
        with Image.open(base_path) as base_source:
            base = base_source.convert("RGBA")
        with Image.open(face_path) as face_source:
            face = face_source.convert("RGBA")
        composite = Image.alpha_composite(base, face)
        rendered = Image.alpha_composite(backdrop, composite).convert("RGB")
        thumbnail = rendered.crop(EYE_LEAKAGE_SOURCE_BOX)

        column = index % columns
        row = index // columns
        x = column * crop_size[0]
        y = title_height + row * (crop_size[1] + label_height)
        sheet.paste(thumbnail, (x, y))
        label_box = (x, y + crop_size[1], x + crop_size[0], y + crop_size[1] + label_height)
        draw.rectangle(label_box, fill="#111318")
        centered_text(
            draw,
            label_box,
            f"{outfit} {token}",
            font=label_font,
            fill="#f6f6f7",
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(destination, optimize=True)


def build_staged_eye_leakage_sheet() -> dict[str, Any]:
    destination = SCREENSHOT_DIR / "contact_eye_leakage_staged_source.png"
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    make_source_eye_leakage_sheet(
        destination,
        base_directory=SOURCE_IMAGES,
        face_directory=STAGED_FACE_IMAGES,
        title=(
            "Matsuda eye-leakage regression / staged faces on production bases "
            "/ source 1:1"
        ),
    )
    inputs = []
    base_names = {"casual": "neutral.png", "uniform": "neut_uniform.png"}
    for outfit in OUTFITS:
        base_path = SOURCE_IMAGES / base_names[outfit]
        inputs.append(
            {
                "role": f"{outfit}_base",
                "path": str(base_path.resolve()),
                "sha256": sha256(base_path),
            }
        )
        for token in EYE_LEAKAGE_TOKENS:
            face_path = STAGED_FACE_IMAGES / f"face_{token}_{outfit}.png"
            inputs.append(
                {
                    "role": f"{outfit}_{token}_face",
                    "path": str(face_path.resolve()),
                    "sha256": sha256(face_path),
                }
            )
    summary: dict[str, Any] = {
        "schema_version": 1,
        "sheet": destination.name,
        "sheet_sha256": sha256(destination),
        "tokens": list(EYE_LEAKAGE_TOKENS),
        "story_sites": list(EYE_LEAKAGE_STORY_SITES),
        "inputs": inputs,
    }
    (SCREENSHOT_DIR / "eye_leakage_staged_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def expected_background_pixel(background: str, x: int, y: int) -> tuple[int, int, int]:
    if background in SOLID_BACKGROUND_RGB:
        return SOLID_BACKGROUND_RGB[background]
    if background != "checker":
        raise ValueError(f"Unknown probe background: {background}")
    if ((x // 32) + (y // 32)) % 2 == 0:
        return (191, 194, 200)
    return (238, 238, 238)


def validate_render_screenshot(path: Path, background: str) -> None:
    """Reject wrong-sized captures and known broken-renderer background damage."""

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
            f"Probe background fidelity failed at {len(mismatches)} sampled pixel(s) "
            f"in {path}; first mismatch={mismatches[0]}"
        )


def rendered_backend() -> str | None:
    log_path = PROBE_ROOT / "log.txt"
    if not log_path.is_file():
        return None
    match = re.search(
        r"^Initializing\s+([a-z0-9]+)\s+renderer:",
        log_path.read_text(encoding="utf-8", errors="replace"),
        flags=re.MULTILINE | re.IGNORECASE,
    )
    return match.group(1).casefold() if match else None


def verify_probe_asset_hashes(manifest: dict[str, Any]) -> int:
    if sha256(CHARACTER_DEFINITIONS) != manifest["production_definitions_sha256"]:
        raise RuntimeError("Production definitions changed during the probe run")
    verified = 0
    for record in manifest["copied_assets"]:
        filename = record["filename"]
        expected = record["sha256"]
        source_hash = sha256(SOURCE_IMAGES / filename)
        copied_hash = sha256(PROBE_IMAGES / filename)
        if source_hash != expected or copied_hash != expected:
            raise RuntimeError(
                f"Probe asset hash changed during rendering: {filename}; "
                f"expected={expected}, source={source_hash}, copy={copied_hash}"
            )
        verified += 1
    return verified


def eye_only_render_records() -> list[dict[str, str]]:
    return [
        record
        for background, _image_name in BACKGROUNDS
        for record in eye_leakage_records(background)
    ]


def assemble_eye_only() -> dict[str, Any]:
    manifest_path = PROBE_ROOT / "probe_manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(manifest_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    records = eye_only_render_records()
    if manifest.get("render_mode") != "eye_only":
        raise ValueError("Probe manifest is not an eye-only render")
    if manifest.get("expected_raw_screenshots") != len(records):
        raise ValueError("Eye-only manifest screenshot count changed")

    expected_paths = {record["relative_path"] for record in records}
    actual_paths = {
        path.relative_to(SCREENSHOT_DIR).as_posix()
        for background, _image_name in BACKGROUNDS
        for path in (SCREENSHOT_DIR / background).rglob("*.png")
    }
    missing = sorted(expected_paths - actual_paths)
    unexpected = sorted(actual_paths - expected_paths)
    if missing or unexpected:
        raise ValueError(
            "Eye-only screenshot contract failed; "
            f"missing={missing}, unexpected={unexpected}"
        )

    backend = rendered_backend()
    if backend is None or not backend.endswith("2"):
        raise ValueError(f"Eye-only probe did not use a GL2-family renderer: {backend}")
    for record in records:
        validate_render_screenshot(
            SCREENSHOT_DIR / record["relative_path"], record["background"]
        )
    verified_assets = verify_probe_asset_hashes(manifest)

    destinations: list[Path] = []
    for background, _image_name in BACKGROUNDS:
        destination = SCREENSHOT_DIR / (
            "contact_eye_leakage_runtime.png"
            if background == "light"
            else f"contact_eye_leakage_runtime_{background}.png"
        )
        make_runtime_eye_leakage_sheet(destination, background=background)
        destinations.append(destination)

    source_destination = SCREENSHOT_DIR / "contact_eye_leakage_source.png"
    make_source_eye_leakage_sheet(source_destination)
    destinations.append(source_destination)

    summary: dict[str, Any] = {
        "schema_version": 1,
        "render_mode": "eye_only",
        "raw_screenshots": len(records),
        "renderer": backend,
        "verified_asset_hashes": verified_assets,
        "verified_background_samples_per_screenshot": 30,
        "tokens": list(EYE_LEAKAGE_TOKENS),
        "story_sites": list(EYE_LEAKAGE_STORY_SITES),
        "contact_sheets": [
            {
                "filename": destination.name,
                "bytes": destination.stat().st_size,
                "sha256": sha256(destination),
            }
            for destination in destinations
        ],
    }
    (SCREENSHOT_DIR / "eye_render_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def assemble_contact_sheets() -> dict[str, Any]:
    records = all_render_records()
    missing = [
        record["relative_path"]
        for record in records
        if not (SCREENSHOT_DIR / record["relative_path"]).is_file()
    ]
    if missing:
        sample = ", ".join(missing[:8])
        suffix = " ..." if len(missing) > 8 else ""
        raise FileNotFoundError(
            f"Missing {len(missing)} Matsuda probe screenshot(s): {sample}{suffix}"
        )

    backend = rendered_backend()
    if backend == "sw":
        raise ValueError(
            "Refusing software-renderer screenshots: this Ren'Py 8.1.1 Windows "
            "build corrupts them. Rerun with the normal accelerated renderer."
        )
    for record in records:
        validate_render_screenshot(
            SCREENSHOT_DIR / record["relative_path"], record["background"]
        )

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
                "expressions_full",
                f"Matsuda expressions / {background} / full-body / 42 renders",
            ),
            (
                expressions,
                head_crop_box(),
                (224, 224),
                7,
                "expressions_head",
                f"Matsuda expressions / {background} / head detail / 42 renders",
            ),
            (
                poses,
                display_crop_box(),
                (192, 288),
                5,
                "poses",
                f"Matsuda standalone poses / {background} / 5 renders",
            ),
        )
        for group, crop, thumbnail_size, columns, stem, title in specifications:
            destination = SCREENSHOT_DIR / f"contact_{stem}_{background}.png"
            make_contact_sheet(
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

    focused_sheets = (
        (
            SCREENSHOT_DIR / "contact_eye_leakage_runtime.png",
            make_runtime_eye_leakage_sheet,
        ),
        (
            SCREENSHOT_DIR / "contact_eye_leakage_source.png",
            make_source_eye_leakage_sheet,
        ),
    )
    for destination, builder in focused_sheets:
        builder(destination)
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
        "eye_leakage_regression": {
            "tokens": list(EYE_LEAKAGE_TOKENS),
            "story_sites": list(EYE_LEAKAGE_STORY_SITES),
            "runtime_sheet": "contact_eye_leakage_runtime.png",
            "source_sheet": "contact_eye_leakage_source.png",
        },
        "contact_sheets": outputs,
    }
    (SCREENSHOT_DIR / "render_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def run_probe(renpy_python: Path, renpy_entry: Path) -> None:
    for path in (renpy_python, renpy_entry):
        if not path.is_file():
            raise FileNotFoundError(path)
    environment = os.environ.copy()
    environment["MATSUDA_PROBE_DIR"] = str(SCREENSHOT_DIR.resolve())
    environment["SDL_AUDIODRIVER"] = "dummy"
    environment["RENPY_PERFORMANCE_TEST"] = "0"
    # Ren'Py 8.1.1's software renderer corrupts screenshots on this Windows
    # build (RGB scanlines and missing backdrop regions).  Let Ren'Py select
    # its normal accelerated renderer for a faithful production-path capture.
    environment.pop("SDL_VIDEODRIVER", None)
    environment.pop("RENPY_RENDERER", None)
    command = (
        str(renpy_python.resolve()),
        str(renpy_entry.resolve()),
        str(PROBE_ROOT.resolve()),
        "run",
    )
    print("Running isolated Ren'Py probe:")
    print("  " + subprocess.list2cmdline(command))
    subprocess.run(command, cwd=PROJECT_ROOT, env=environment, check=True)


def print_prepare_summary(manifest: dict[str, Any]) -> None:
    print(f"Probe project: {PROBE_ROOT.resolve()}")
    print(f"Render output: {SCREENSHOT_DIR.resolve()}")
    if manifest["render_mode"] == "eye_only":
        print(
            "Prepared the 6 focused neutral/smug/thinking outfit composites "
            f"across {len(manifest['backgrounds'])} backgrounds "
            f"({manifest['expected_raw_screenshots']} screenshots)."
        )
    else:
        print(
            "Prepared "
            f"{manifest['unique_expression_renders']} layered expressions and "
            f"{manifest['unique_pose_renders']} standalone poses across "
            f"{len(manifest['backgrounds'])} backgrounds "
            f"({manifest['expected_raw_screenshots']} screenshots)."
        )
    print("One-command local-display render and contact-sheet build:")
    run_flag = "--run-eye-only" if manifest["render_mode"] == "eye_only" else "--run"
    print(f'  python "{Path(__file__).resolve()}" {run_flag}')
    if manifest["render_mode"] == "eye_only":
        return
    print("Manual render environment:")
    print(f'  $env:MATSUDA_PROBE_DIR="{SCREENSHOT_DIR.resolve()}"')
    print('  $env:SDL_AUDIODRIVER="dummy"')
    print('  $env:RENPY_PERFORMANCE_TEST="0"')
    manual = (
        str(DEFAULT_RENPY_PYTHON.resolve()),
        str(DEFAULT_RENPY_ENTRY.resolve()),
        str(PROBE_ROOT.resolve()),
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
        help="Prepare, render through the local display, verify, and assemble sheets.",
    )
    mode.add_argument(
        "--run-eye-only",
        action="store_true",
        help=(
            "Render only neutral/smug/thinking for both outfits on three "
            "backgrounds (18 captures), then verify and assemble focused sheets."
        ),
    )
    mode.add_argument(
        "--assemble-only",
        action="store_true",
        help="Assemble contact sheets from an existing complete render output.",
    )
    mode.add_argument(
        "--staged-eye-only",
        action="store_true",
        help=(
            "Build only the focused 1:1 eye-regression sheet from staged faces "
            "and production bases; do not prepare or run Ren'Py."
        ),
    )
    parser.add_argument(
        "--renpy-python",
        type=Path,
        default=DEFAULT_RENPY_PYTHON,
        help="Bundled Python executable for the target Ren'Py SDK.",
    )
    parser.add_argument(
        "--renpy-entry",
        type=Path,
        default=DEFAULT_RENPY_ENTRY,
        help="renpy.py or this project's renamed equivalent.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.staged_eye_only:
        summary = build_staged_eye_leakage_sheet()
        print(
            "Assembled staged source eye-leakage sheet: "
            f"{SCREENSHOT_DIR / summary['sheet']}"
        )
        return 0
    if args.assemble_only:
        summary = assemble_contact_sheets()
        print(
            f"Assembled {len(summary['contact_sheets'])} contact sheets from "
            f"{summary['raw_screenshots']} verified screenshots in "
            f"{SCREENSHOT_DIR.resolve()}"
        )
        return 0

    manifest = build_project(eye_only=args.run_eye_only)
    print_prepare_summary(manifest)
    if args.run_eye_only:
        run_probe(args.renpy_python, args.renpy_entry)
        summary = assemble_eye_only()
        print(
            f"Rendered and verified {summary['raw_screenshots']} focused "
            f"screenshots with {summary['renderer']}; verified "
            f"{summary['verified_asset_hashes']} copied asset hashes and assembled "
            f"{len(summary['contact_sheets'])} focused contact sheets."
        )
        return 0
    if args.run:
        run_probe(args.renpy_python, args.renpy_entry)
        summary = assemble_contact_sheets()
        print(
            f"Rendered {summary['raw_screenshots']} screenshots and assembled "
            f"{len(summary['contact_sheets'])} contact sheets."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
