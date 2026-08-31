#!/usr/bin/env python3
"""Validate Tsubaki's installed oval face plates and live Ren'Py API.

The pixel audit is delegated to the canonical builder so validation exactly
replays every registered master, pre-slice upper-lid cleanup, smooth oval, and
installed byte. This wrapper independently checks the conditioned layeredimage
wiring and every explicit or say-image Tsubaki expression used by story code.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from collections import Counter
from pathlib import Path

import build_tsubaki_faceplates as faceplates
from PIL import Image


SHOW_RE = re.compile(r"^\s*show\s+tsubaki\b(?P<tail>.*)$")
SAY_IMAGE_RE = re.compile(r"^\s*ts\s+(?P<face>[a-z_][a-z0-9_]*)\s+(?=[\"'])")
STATEMENT_KEYWORDS = {"as", "at", "behind", "onlayer", "with", "zorder"}
ALLOWED_SHOW_ATTRIBUTES = set(faceplates.EXPRESSIONS) | set(faceplates.OUTFITS)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--staging",
        type=Path,
        default=faceplates.DEFAULT_STAGING,
        help="Validated oval build used as installed provenance",
    )
    parser.add_argument(
        "--story-root",
        type=Path,
        default=faceplates.ROOT / "game",
    )
    parser.add_argument(
        "--definitions",
        type=Path,
        default=faceplates.DEFINITIONS,
    )
    parser.add_argument(
        "--render-root",
        type=Path,
        help="Optional directory containing the isolated 42-state screenshots",
    )
    return parser.parse_args()


def tsubaki_definition_block(path: Path) -> str:
    source = path.read_text(encoding="utf-8")
    match = re.search(
        r"(?ms)^layeredimage tsubaki:\s*$.*?(?=^layeredimage\s+\w+\s*:|\Z)",
        source,
    )
    if match is None:
        raise RuntimeError(f"Missing layeredimage tsubaki block in {path}")
    return match.group(0)


def validate_definition(path: Path) -> list[str]:
    block = tsubaki_definition_block(path)
    errors: list[str] = []
    for outfit, spec in faceplates.OUTFITS.items():
        base_reference = f'"assets/characters/tsubaki/{spec["base"]}"'
        if block.count(base_reference) != 1:
            errors.append(
                f"Tsubaki definition must reference {spec['base']} exactly once"
            )
        for expression in faceplates.EXPRESSIONS:
            filename = f"face_{expression}_{outfit}.png"
            pattern = re.compile(
                rf"(?m)^\s*attribute\s+{re.escape(expression)}"
                rf"(?:\s+default)?\s+if_all\s+\"{outfit}\"\s*:\s*$"
                rf"\s*^\s*\"assets/characters/tsubaki/{filename}\"\s*$"
            )
            if len(pattern.findall(block)) != 1:
                errors.append(
                    f"Tsubaki definition lacks one conditioned {outfit}/{expression} layer"
                )
    if "pose_" in block:
        errors.append("Tsubaki definition still contains a retired pose_ attribute")
    return errors


def show_attributes(tail: str) -> tuple[str, ...]:
    attributes: list[str] = []
    for word in re.findall(r"[a-z_][a-z0-9_]*", tail.lower()):
        if word in STATEMENT_KEYWORDS:
            break
        attributes.append(word)
    return tuple(attributes)


def validate_story(root: Path) -> tuple[list[str], Counter[str], int, int]:
    errors: list[str] = []
    usage: Counter[str] = Counter()
    show_count = 0
    say_image_count = 0
    for path in sorted(root.rglob("*.rpy")):
        relative = path.relative_to(faceplates.ROOT)
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8-sig").splitlines(), start=1
        ):
            if line.lstrip().startswith("#"):
                continue
            show_match = SHOW_RE.match(line)
            if show_match:
                show_count += 1
                for attribute in show_attributes(show_match.group("tail")):
                    if attribute not in ALLOWED_SHOW_ATTRIBUTES:
                        errors.append(
                            f"{relative}:{line_number}: unknown Tsubaki attribute "
                            f"{attribute!r}"
                        )
                    elif attribute in faceplates.EXPRESSIONS:
                        usage[attribute] += 1
            say_match = SAY_IMAGE_RE.match(line)
            if say_match:
                say_image_count += 1
                expression = say_match.group("face")
                if expression not in faceplates.EXPRESSIONS:
                    errors.append(
                        f"{relative}:{line_number}: unknown ts say-image expression "
                        f"{expression!r}"
                    )
                else:
                    usage[expression] += 1

    missing = sorted(set(faceplates.EXPRESSIONS) - set(usage))
    if missing:
        errors.append(f"No live story use found for Tsubaki faces: {missing}")
    return errors, usage, show_count, say_image_count


def validate_renders(root: Path) -> list[str]:
    errors: list[str] = []
    expected = []
    number = 1
    for outfit in faceplates.OUTFITS:
        for expression in faceplates.EXPRESSIONS:
            expected.append(f"{number:02d}_{outfit}_{expression}.png")
            number += 1
    actual = sorted(path.name for path in root.glob("*.png") if path.is_file())
    if actual != sorted(expected):
        errors.append(
            "runtime screenshot manifest mismatch: "
            f"missing={sorted(set(expected) - set(actual))}, "
            f"extra={sorted(set(actual) - set(expected))}"
        )

    pixel_signatures: set[bytes] = set()
    for filename in expected:
        path = root / filename
        if not path.is_file():
            continue
        with Image.open(path) as image:
            image.load()
            if image.size != (1280, 960):
                errors.append(f"{filename}: runtime render size is {image.size}")
            pixel_signatures.add(
                hashlib.sha256(image.convert("RGB").tobytes()).digest()
            )
    if len(pixel_signatures) != len(expected):
        errors.append(
            f"runtime probe produced {len(pixel_signatures)} unique renders; "
            f"expected {len(expected)}"
        )
    return errors


def main() -> int:
    args = parse_args()
    staging = args.staging.resolve()
    errors = faceplates.validate(staging, installed=True)
    errors.extend(validate_definition(args.definitions.resolve()))
    story_errors, usage, show_count, say_image_count = validate_story(
        args.story_root.resolve()
    )
    errors.extend(story_errors)
    if args.render_root is not None:
        errors.extend(validate_renders(args.render_root.resolve()))
    if errors:
        raise RuntimeError("Tsubaki validation failed:\n- " + "\n- ".join(errors))
    print("validated: 42 installed oval face layers and 2 unchanged neutral bases")
    print(
        f"story API: {show_count} explicit shows + {say_image_count} say-image calls; "
        f"all {len(usage)} face tokens live"
    )
    if args.render_root is not None:
        print(
            "runtime probe: 42 decodable, correctly sized, pixel-distinct GL2 renders"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
