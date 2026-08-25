"""Build an isolated Ren'Py project that renders Tsubaki's face-only bank.

The fixture copies the 42 installed outfit-conditioned face layers plus the
two approved, byte-unchanged neutral bases. It then renders every combination
of two outfits and 21 face tokens. All generated files stay under ``tmp/``.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from install_tsubaki_sprites import DESTINATION, production_manifest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEMP_ROOT = PROJECT_ROOT / "tmp"
PROBE_ROOT = TEMP_ROOT / "tsubaki_render_probe_project"
PROBE_GAME = PROBE_ROOT / "game"
PROBE_IMAGES = PROBE_GAME / "images" / "tsubaki"
SCREENSHOT_DIR = TEMP_ROOT / "tsubaki_render_probe"
CHARACTER_DEFINITIONS = (
    PROJECT_ROOT / "game" / "mod_assets" / "def_characters.rpy"
)

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
BASE_FILENAMES = ("neutral.png", "neut_uniform.png")

OPTIONS = '''define config.name = "Tsubaki Face-Patch Probe"
define config.version = "2.0"
define config.screen_width = 1280
define config.screen_height = 960
define config.developer = True
define config.save_directory = None
'''

PROBE_SCRIPT_HEADER = r'''
image probe_background = Solid("#ece9e2")

transform probe_center:
    xalign 0.5
    yalign 1.0


label start:
    python:
        import os
        _tsubaki_probe_dir = os.environ["TSUBAKI_PROBE_DIR"].replace("\\", "/")

    scene probe_background
'''


def expected_face_layer_filenames() -> tuple[str, ...]:
    return tuple(
        f"face_{token}_{outfit}.png"
        for outfit in OUTFITS
        for token in FACE_TOKENS
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


def layeredimage_block() -> str:
    source = CHARACTER_DEFINITIONS.read_text(encoding="utf-8")
    transform = top_level_block(source, "transform tsubaki_sprite_size:")
    layeredimage = top_level_block(source, "layeredimage tsubaki:")
    if "group pose:" in layeredimage:
        raise ValueError("Tsubaki probe found the retired pose group")

    block = transform + "\n\n" + layeredimage + "\n"
    production_prefix = "mod_assets/char_sprites/tsubaki/"
    if production_prefix not in block:
        raise ValueError("Tsubaki layeredimage contains no production asset paths")
    return block.replace(production_prefix, "images/tsubaki/")


def probe_script() -> str:
    lines = [PROBE_SCRIPT_HEADER.rstrip(), ""]
    screenshot_number = 1
    for outfit in OUTFITS:
        for token in FACE_TOKENS:
            filename = f"{screenshot_number:02d}_{outfit}_{token}.png"
            lines.extend(
                (
                    f"    show tsubaki {outfit} {token} at probe_center",
                    "    $ renpy.pause(0.25, hard=True)",
                    f'    $ renpy.screenshot(_tsubaki_probe_dir + "/{filename}")',
                    "",
                )
            )
            screenshot_number += 1
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


def copy_runtime_assets() -> None:
    manifest_filenames = set(production_manifest())
    expected_layers = set(expected_face_layer_filenames())
    if manifest_filenames != expected_layers:
        missing = sorted(expected_layers - manifest_filenames)
        extra = sorted(manifest_filenames - expected_layers)
        raise ValueError(
            "Tsubaki installer manifest is not the exact 42-layer contract; "
            f"missing={missing}, extra={extra}"
        )

    runtime_filenames = (*BASE_FILENAMES, *sorted(expected_layers))
    for filename in runtime_filenames:
        if "old" in filename.casefold() or filename.startswith("post_"):
            raise ValueError(f"Disallowed Tsubaki probe source: {filename}")
        source = DESTINATION / filename
        if not source.is_file():
            raise FileNotFoundError(source)
        shutil.copy2(source, PROBE_IMAGES / filename)


def main() -> int:
    reset_generated_directory(PROBE_ROOT)
    reset_generated_directory(SCREENSHOT_DIR)
    PROBE_IMAGES.mkdir(parents=True, exist_ok=True)
    copy_runtime_assets()

    (PROBE_GAME / "options.rpy").write_text(OPTIONS, encoding="utf-8")
    (PROBE_GAME / "script.rpy").write_text(
        layeredimage_block() + "\n" + probe_script(), encoding="utf-8"
    )
    print(PROBE_ROOT)
    print(SCREENSHOT_DIR)
    print(f"Prepared {len(OUTFITS) * len(FACE_TOKENS)} Tsubaki renders")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
