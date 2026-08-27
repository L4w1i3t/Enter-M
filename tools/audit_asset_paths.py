#!/usr/bin/env python3
"""Audit ENTER M's consolidated runtime asset paths.

The checker is intentionally static and conservative. It verifies concrete
``assets/...`` string literals, rejects live references to the retired asset
roots, and leaves the bundled Lost Records package alone because that package
owns its own internal layout.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = PROJECT_ROOT / "game"
ASSET_ROOT = GAME_ROOT / "assets"

SOURCE_SUFFIXES = {".rpy", ".py"}
VENDOR_PARTS = ("game", "lost_records")
LEGACY_COMPATIBILITY_FILES = {
    "game/addons/CG View/cg_gallery.rpy",
    "game/addons/Music Room/music_room.rpy",
}
LEGACY_DIRECTORIES = (
    "game/mod_assets",
    "game/images",
    "game/gui",
    "game/bgm",
    "game/sfx",
)
LEGACY_LITERAL_PREFIXES = (
    "mod_assets/",
    "images/",
    "gui/",
    "bgm/",
    "sfx/",
    "bg/",
    "menu/",
    "monika/",
    "natsuki/",
    "sayori/",
    "yuri/",
    "poem_special/",
)

# These two references predate the consolidation and were already absent from
# the imported MPT sprite pack. Keep them visible without making an otherwise
# clean consolidation audit fail.
KNOWN_MISSING = {
    "assets/mpt/natsuki/natsuki_turned_uniform_left_point.png",
    "assets/mpt/natsuki/natsuki_turned_casual_left_point.png",
}

STRING_LITERAL = re.compile(
    r"(?P<quote>['\"])(?P<value>(?:\\.|(?!\1).)*?)(?P=quote)"
)
DYNAMIC_MARKERS = ("[", "]", "%", "{", "}", "*", "<", ">")
AUDIO_DIRECTIVES = re.compile(r"^(?:<[^>]+>)+")


def relative_posix(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def is_vendor_source(path: Path) -> bool:
    relative_parts = path.relative_to(PROJECT_ROOT).parts
    return relative_parts[: len(VENDOR_PARTS)] == VENDOR_PARTS


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def build_case_index() -> tuple[dict[str, str], list[tuple[str, str]]]:
    index: dict[str, str] = {}
    collisions: list[tuple[str, str]] = []
    for path in GAME_ROOT.rglob("*"):
        relative = path.relative_to(GAME_ROOT).as_posix()
        folded = relative.casefold()
        previous = index.get(folded)
        if previous is not None and previous != relative:
            collisions.append((previous, relative))
        else:
            index[folded] = relative
    return index, collisions


def iter_sources() -> list[Path]:
    return [
        path
        for path in sorted(GAME_ROOT.rglob("*"))
        if path.is_file()
        and path.suffix.lower() in SOURCE_SUFFIXES
        and not is_vendor_source(path)
    ]


def audit() -> int:
    problems: list[str] = []
    warnings: list[str] = []
    checked_references = 0
    skipped_dynamic = 0

    if not ASSET_ROOT.is_dir():
        problems.append("missing consolidated root: game/assets")

    for relative in LEGACY_DIRECTORIES:
        if (PROJECT_ROOT / relative).exists():
            problems.append(f"retired physical directory still exists: {relative}")

    case_index, collisions = build_case_index()
    for first, second in collisions:
        problems.append(f"case-insensitive path collision: {first!r} vs {second!r}")

    for source in iter_sources():
        source_name = relative_posix(source)
        text = source.read_text(encoding="utf-8-sig")
        compatibility_file = source_name in LEGACY_COMPATIBILITY_FILES

        for match in STRING_LITERAL.finditer(text):
            value = match.group("value").replace("\\/", "/")
            normalized = value.replace("\\", "/")
            line = line_number(text, match.start())

            # Quoted examples in comments are documentation, not live paths.
            line_start = text.rfind("\n", 0, match.start()) + 1
            if text[line_start:match.start()].lstrip().startswith("#"):
                continue

            if not compatibility_file and normalized.startswith(LEGACY_LITERAL_PREFIXES):
                problems.append(
                    f"{source_name}:{line}: live legacy asset literal {value!r}"
                )

            live_path = AUDIO_DIRECTIVES.sub("", normalized)
            if not live_path.startswith("assets/"):
                continue

            asset_path = live_path.rstrip("/")
            if any(marker in asset_path for marker in DYNAMIC_MARKERS):
                skipped_dynamic += 1
                continue

            checked_references += 1
            actual = case_index.get(asset_path.casefold())
            if actual is None:
                message = f"{source_name}:{line}: missing asset {asset_path!r}"
                if asset_path in KNOWN_MISSING:
                    warnings.append(message + " (known imported-MPT gap)")
                else:
                    problems.append(message)
            elif actual != asset_path:
                problems.append(
                    f"{source_name}:{line}: asset case mismatch {asset_path!r}; "
                    f"disk path is {actual!r}"
                )

    for warning in warnings:
        print(f"WARNING: {warning}")
    for problem in problems:
        print(f"ERROR: {problem}")

    print(
        "Asset audit: "
        f"{checked_references} concrete references checked, "
        f"{skipped_dynamic} dynamic references skipped, "
        f"{len(warnings)} known warnings, {len(problems)} errors."
    )
    return 1 if problems else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    return audit()


if __name__ == "__main__":
    sys.exit(main())
