#!/usr/bin/env python3
"""Validate Tsubaki's two-base, outfit-conditioned expression bank.

The production contract is intentionally small:

* the untouched ``neutral.png`` and ``neut_uniform.png`` bases;
* 21 full-canvas face layers per outfit, with transparent neutral layers;
* one fixed feathered alpha mask shared by the 20 alternates in each outfit;
* a layeredimage containing only the two bases and those 42 face layers; and
* story ``show tsubaki`` calls containing no retired ``pose_*`` attributes.

Validation is read-only unless ``--review-sheet PATH`` is supplied.  A staging
bank can be checked before installation with ``--layer-root`` while the bases
continue to come from ``--sprite-root``.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPRITE_ROOT = (
    PROJECT_ROOT / "game" / "mod_assets" / "char_sprites" / "tsubaki"
)
DEFAULT_DEFINITIONS = PROJECT_ROOT / "game" / "mod_assets" / "def_characters.rpy"
DEFAULT_STORY_ROOT = PROJECT_ROOT / "game"
CANVAS_SIZE = (1023, 1537)
CANVAS_WIDTH, CANVAS_HEIGHT = CANVAS_SIZE

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
ALTERNATE_TOKENS = FACE_TOKENS[1:]


@dataclass(frozen=True)
class OutfitSpec:
    name: str
    base_name: str

    def face_name(self, token: str) -> str:
        return f"face_{token}_{self.name}.png"

    def face_reference(self, token: str) -> str:
        return f"mod_assets/char_sprites/tsubaki/{self.face_name(token)}"

    @property
    def base_reference(self) -> str:
        return f"mod_assets/char_sprites/tsubaki/{self.base_name}"


OUTFITS = (
    OutfitSpec("casual", "neutral.png"),
    OutfitSpec("uniform", "neut_uniform.png"),
)


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def check(self, condition: bool, message: str) -> bool:
        if not condition:
            self.errors.append(message)
        return condition

    def error(self, message: str) -> None:
        self.errors.append(message)

    def note(self, message: str) -> None:
        self.notes.append(message)


@dataclass(frozen=True)
class AttributeRecord:
    name: str
    is_default: bool
    if_all: tuple[str, ...]
    asset: str | None


def expected_face_names() -> set[str]:
    return {
        outfit.face_name(token) for outfit in OUTFITS for token in FACE_TOKENS
    }


def expected_layered_references() -> set[str]:
    references = {outfit.base_reference for outfit in OUTFITS}
    references.update(
        outfit.face_reference(token) for outfit in OUTFITS for token in FACE_TOKENS
    )
    return references


def mask_bbox(mask: np.ndarray) -> tuple[int, int, int, int] | None:
    rows, columns = np.nonzero(mask)
    if not len(columns):
        return None
    return (
        int(columns.min()),
        int(rows.min()),
        int(columns.max()) + 1,
        int(rows.max()) + 1,
    )


def format_bbox(bounds: tuple[int, int, int, int] | None) -> str:
    if bounds is None:
        return "empty"
    left, top, right, bottom = bounds
    return f"({left},{top})-({right},{bottom})"


def shifted_correlation(
    values: np.ndarray,
    support: np.ndarray,
    dy: int,
    dx: int,
) -> float | None:
    """Correlate supported samples with a spatially shifted copy."""

    height, width = support.shape
    if abs(dy) >= height or abs(dx) >= width:
        return None
    first_y = slice(max(0, -dy), min(height, height - dy))
    second_y = slice(max(0, dy), min(height, height + dy))
    first_x = slice(max(0, -dx), min(width, width - dx))
    second_x = slice(max(0, dx), min(width, width + dx))
    valid = support[first_y, first_x] & support[second_y, second_x]
    if int(valid.sum()) < 500:
        return None
    first = values[first_y, first_x][valid].astype(np.float64)
    second = values[second_y, second_x][valid].astype(np.float64)
    first -= first.mean()
    second -= second.mean()
    denominator = math.sqrt(float(np.dot(first, first) * np.dot(second, second)))
    if denominator <= 1e-9:
        return None
    return float(np.dot(first, second) / denominator)


def checker_periodicity_score(
    composite: np.ndarray,
    base: np.ndarray,
    support: np.ndarray,
) -> tuple[float, int | None]:
    """Measure two-axis flip/repeat evidence from a baked checker pattern."""

    bounds = mask_bbox(support)
    if bounds is None or int(support.sum()) < 2_000:
        return 0.0, None
    left, top, right, bottom = bounds
    support = support[top:bottom, left:right]
    weights = np.asarray((0.2126, 0.7152, 0.0722), dtype=np.float32)
    difference = (
        composite[top:bottom, left:right, :3].astype(np.float32)
        - base[top:bottom, left:right, :3].astype(np.float32)
    ) @ weights
    if float(difference[support].std()) < 0.35:
        return 0.0, None

    best_score = 0.0
    best_tile: int | None = None
    for tile in range(3, 33):
        correlations = (
            shifted_correlation(difference, support, 0, tile),
            shifted_correlation(difference, support, tile, 0),
            shifted_correlation(difference, support, 0, tile * 2),
            shifted_correlation(difference, support, tile * 2, 0),
        )
        if any(value is None for value in correlations):
            continue
        horizontal_flip, vertical_flip, horizontal_repeat, vertical_repeat = (
            float(value) for value in correlations
        )
        score = min(
            -horizontal_flip,
            -vertical_flip,
            horizontal_repeat,
            vertical_repeat,
        )
        if score > best_score:
            best_score = score
            best_tile = tile
    return max(0.0, best_score), best_tile


def load_rgba(
    path: Path, label: str, report: ValidationReport
) -> np.ndarray | None:
    if not path.is_file() or path.is_symlink():
        report.error(f"{label}: missing or unsafe PNG: {path}")
        return None
    try:
        with Image.open(path) as image:
            if image.mode != "RGBA" or image.size != CANVAS_SIZE:
                report.error(
                    f"{label}: expected RGBA {CANVAS_SIZE}, got "
                    f"{image.mode} {image.size}: {path}"
                )
                return None
            pixels = np.asarray(image, dtype=np.uint8).copy()
    except (OSError, ValueError) as exc:
        report.error(f"{label}: cannot read {path}: {exc}")
        return None

    alpha = pixels[:, :, 3]
    hidden_rgb = int(
        np.count_nonzero((alpha == 0) & np.any(pixels[:, :, :3] != 0, axis=2))
    )
    report.check(
        hidden_rgb == 0,
        f"{label}: {hidden_rgb} zero-alpha pixels retain RGB matte data",
    )
    return pixels


def validate_manifest(layer_root: Path, sprite_root: Path, report: ValidationReport) -> None:
    expected = expected_face_names()
    actual = {
        path.name
        for path in layer_root.glob("face_*_*.png")
        if path.is_file() and not path.is_symlink()
    }
    report.check(
        actual == expected,
        "conditioned face manifest is not the exact 42-file bank; "
        f"missing={sorted(expected - actual)} unexpected={sorted(actual - expected)}",
    )

    obsolete_shared = [
        sprite_root / f"face_{token}.png"
        for token in FACE_TOKENS
        if (sprite_root / f"face_{token}.png").exists()
    ]
    report.check(
        not obsolete_shared,
        "obsolete shared Tsubaki face files remain in production: "
        + ", ".join(path.name for path in obsolete_shared),
    )
    obsolete_parts = sorted(path.name for path in sprite_root.glob("forward_*.png"))
    report.check(
        not obsolete_parts,
        "obsolete multipart Tsubaki assets remain in production: "
        + ", ".join(obsolete_parts),
    )


def alpha_composite(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    return np.asarray(
        Image.alpha_composite(
            Image.fromarray(base, "RGBA"), Image.fromarray(overlay, "RGBA")
        ),
        dtype=np.uint8,
    ).copy()


def validate_bases(
    sprite_root: Path, report: ValidationReport
) -> dict[str, np.ndarray]:
    bases: dict[str, np.ndarray] = {}
    signatures: dict[bytes, str] = {}
    for outfit in OUTFITS:
        label = f"tsubaki/{outfit.name}/base"
        pixels = load_rgba(sprite_root / outfit.base_name, label, report)
        if pixels is None:
            continue
        alpha = pixels[:, :, 3]
        visible = alpha > 0
        bounds = mask_bbox(visible)
        report.check(bool(np.any(visible)), f"{label}: base is fully transparent")
        if bounds is not None:
            left, top, right, bottom = bounds
            report.check(
                left > 0 and top > 0 and right < CANVAS_WIDTH,
                f"{label}: unsafe top/horizontal canvas contact; "
                f"bbox={format_bbox(bounds)}",
            )
            report.check(
                bottom == CANVAS_HEIGHT,
                f"{label}: expected the approved raw base to reach the canvas "
                f"bottom; bbox={format_bbox(bounds)}",
            )
        signature = hashlib.sha256(pixels).digest()
        previous = signatures.get(signature)
        report.check(
            previous is None,
            f"{label}: base pixels duplicate {previous}",
        )
        signatures[signature] = outfit.name
        bases[outfit.name] = pixels
        report.note(
            f"{label}: bbox={format_bbox(bounds)} visible={int(visible.sum())}"
        )
    return bases


def validate_feather_mask(
    alpha: np.ndarray, label: str, report: ValidationReport
) -> None:
    visible = alpha > 0
    opaque = alpha == 255
    partial = visible & ~opaque
    bounds = mask_bbox(visible)
    report.check(bool(np.any(visible)), f"{label}: alternate mask is empty")
    report.check(bool(np.any(opaque)), f"{label}: mask has no solid interior")
    report.check(
        int(partial.sum()) >= 512,
        f"{label}: mask has too little feathering ({int(partial.sum())} partial pixels)",
    )
    report.check(
        len(np.unique(alpha)) >= 32,
        f"{label}: mask has only {len(np.unique(alpha))} alpha levels; "
        "expected a smooth feather",
    )
    if bounds is not None:
        left, top, right, bottom = bounds
        report.check(
            left > 0 and top > 0 and right < CANVAS_WIDTH and bottom < CANVAS_HEIGHT,
            f"{label}: face patch touches a canvas edge; bbox={format_bbox(bounds)}",
        )
    border_pixels = int(
        np.count_nonzero(alpha[0, :])
        + np.count_nonzero(alpha[-1, :])
        + np.count_nonzero(alpha[:, 0])
        + np.count_nonzero(alpha[:, -1])
    )
    report.check(
        border_pixels == 0,
        f"{label}: {border_pixels} nontransparent alpha samples touch the canvas edge",
    )
    report.note(
        f"{label}: bbox={format_bbox(bounds)} visible={int(visible.sum())} "
        f"opaque={int(opaque.sum())} partial={int(partial.sum())} "
        f"levels={len(np.unique(alpha))}"
    )


def validate_face_bank(
    layer_root: Path,
    bases: dict[str, np.ndarray],
    report: ValidationReport,
) -> None:
    layer_signatures: dict[bytes, str] = {}
    composite_signatures: dict[bytes, str] = {}

    for outfit in OUTFITS:
        base = bases.get(outfit.name)
        common_alpha: np.ndarray | None = None
        changed_counts: list[int] = []
        checker_scores: list[tuple[float, str, int | None]] = []

        for token in FACE_TOKENS:
            filename = outfit.face_name(token)
            label = f"tsubaki/{outfit.name}/face/{token}"
            layer = load_rgba(layer_root / filename, label, report)
            if layer is None:
                continue
            alpha = layer[:, :, 3]

            if token == "neut":
                report.check(
                    not np.any(alpha),
                    f"{label}: neutral layer must be fully transparent",
                )
            else:
                report.check(
                    bool(np.any(alpha)),
                    f"{label}: alternate layer is fully transparent",
                )
                if common_alpha is None:
                    common_alpha = alpha.copy()
                    validate_feather_mask(common_alpha, f"tsubaki/{outfit.name}/mask", report)
                else:
                    report.check(
                        np.array_equal(alpha, common_alpha),
                        f"{label}: alpha differs from the fixed {outfit.name} mask",
                    )

                layer_signature = hashlib.sha256(layer).digest()
                previous_layer = layer_signatures.get(layer_signature)
                report.check(
                    previous_layer is None,
                    f"{label}: alternate pixels duplicate {previous_layer}",
                )
                layer_signatures[layer_signature] = label

            if base is None:
                continue
            composite = alpha_composite(base, layer)
            report.check(
                np.array_equal(composite[:, :, 3], base[:, :, 3]),
                f"{label}: composite changes the approved base alpha/silhouette",
            )
            changed = int(np.count_nonzero(np.any(composite != base, axis=2)))
            if token == "neut":
                report.check(
                    changed == 0,
                    f"{label}: transparent neutral changes {changed} base pixels",
                )
            else:
                report.check(
                    changed > 0,
                    f"{label}: alternate composite is pixel-identical to neutral",
                )
                changed_counts.append(changed)
                checker_score, checker_tile = checker_periodicity_score(
                    composite,
                    base,
                    alpha == 255,
                )
                report.check(
                    checker_score < 0.28,
                    f"{label}: checker-like two-axis periodicity detected "
                    f"(score={checker_score:.3f}, estimated tile={checker_tile}px)",
                )
                checker_scores.append((checker_score, token, checker_tile))
                composite_signature = hashlib.sha256(composite).digest()
                previous_composite = composite_signatures.get(composite_signature)
                report.check(
                    previous_composite is None,
                    f"{label}: composite duplicates {previous_composite}",
                )
                composite_signatures[composite_signature] = label

        if common_alpha is not None and base is not None:
            outside_base = int(
                np.count_nonzero((common_alpha > 0) & (base[:, :, 3] == 0))
            )
            report.check(
                outside_base == 0,
                f"tsubaki/{outfit.name}/mask: {outside_base} pixels extend "
                "outside the approved base alpha",
            )
        if changed_counts:
            strongest_checker = max(checker_scores, default=(0.0, "none", None))
            report.note(
                f"tsubaki/{outfit.name}/alternates: distinct={len(changed_counts)} "
                f"changed-range={min(changed_counts)}-{max(changed_counts)} "
                f"checker-max={strongest_checker[0]:.3f}"
                f"/{strongest_checker[1]}@{strongest_checker[2]}px"
            )


def indented_block(source: str, header: str, indent: int) -> str:
    lines = source.splitlines(keepends=True)
    try:
        start = next(index for index, line in enumerate(lines) if line.rstrip() == header)
    except StopIteration as exc:
        raise ValueError(f"missing block header: {header}") from exc
    body = [lines[start]]
    for line in lines[start + 1 :]:
        if line.strip() and len(line) - len(line.lstrip(" ")) <= indent:
            break
        body.append(line)
    return "".join(body)


def parse_attribute_records(group: str) -> list[AttributeRecord]:
    lines = group.splitlines()
    records: list[AttributeRecord] = []
    attribute_pattern = re.compile(r"^        attribute\s+(\w+)(?P<tail>[^:]*):\s*$")
    asset_pattern = re.compile(
        r'"(?P<asset>mod_assets/char_sprites/tsubaki/[^"\n]+\.png)"'
    )
    for index, line in enumerate(lines):
        match = attribute_pattern.match(line)
        if not match:
            continue
        tail = match.group("tail")
        asset: str | None = None
        for child in lines[index + 1 :]:
            if child.strip() and len(child) - len(child.lstrip(" ")) <= 8:
                break
            asset_match = asset_pattern.search(child)
            if asset_match:
                asset = asset_match.group("asset")
                break
        records.append(
            AttributeRecord(
                name=match.group(1),
                is_default=bool(re.search(r"(?:^|\s)default(?:\s|$)", tail)),
                if_all=tuple(re.findall(r'\bif_all\s+"([^"]+)"', tail)),
                asset=asset,
            )
        )
    return records


def validate_definition(definitions: Path, report: ValidationReport) -> None:
    try:
        source = definitions.read_text(encoding="utf-8")
        layered = indented_block(source, "layeredimage tsubaki:", 0)
        outfit_group = indented_block(layered, "    group outfit:", 4)
        face_group = indented_block(layered, "    group face:", 4)
    except (OSError, UnicodeError, ValueError) as exc:
        report.error(f"cannot audit Tsubaki definition: {exc}")
        return

    transform_count = len(
        re.findall(r"^transform tsubaki_sprite_size:\s*$", source, re.MULTILINE)
    )
    try:
        transform_block = indented_block(
            source, "transform tsubaki_sprite_size:", 0
        )
    except ValueError:
        transform_block = ""
    transform_lines = [
        line.strip()
        for line in transform_block.splitlines()[1:]
        if line.strip() and not line.lstrip().startswith("#")
    ]
    report.check(
        transform_count == 1
        and transform_lines == ['fit "contain"', "xysize (640, 960)"],
        "tsubaki definition: shared sprite transform must contain exactly "
        "`fit \"contain\"` and `xysize (640, 960)` with no height/offset/zoom "
        f"adjustors; occurrences={transform_count}, body={transform_lines}",
    )
    layered_at_clauses = re.findall(r"^\s+at\s+(.+?)\s*$", layered, re.MULTILINE)
    report.check(
        layered_at_clauses == ["tsubaki_sprite_size, Flatten"],
        "tsubaki definition: layeredimage must use only "
        "`at tsubaki_sprite_size, Flatten`; "
        f"actual at clauses={layered_at_clauses}",
    )
    forbidden_adjustors = sorted(
        set(
            re.findall(
                r"\b(?:fit|xoffset|yoffset|xzoom|yzoom|zoom|xsize|ysize|xysize|height)\b"
                r"|\bTransform\s*\(",
                layered,
            )
        )
    )
    report.check(
        not forbidden_adjustors,
        "tsubaki definition: layeredimage contains forbidden per-layer "
        f"height/offset/zoom adjustor(s): {forbidden_adjustors}",
    )
    report.check(
        "    group pose:" not in layered and "pose_" not in layered,
        "tsubaki definition: retired pose group/attributes remain in layeredimage",
    )
    report.check(
        "forward_" not in layered,
        "tsubaki definition: obsolete multipart `forward_*` reference remains",
    )

    outfit_records = Counter(parse_attribute_records(outfit_group))
    expected_outfit_records = Counter(
        {
            AttributeRecord("casual", True, (), OUTFITS[0].base_reference): 1,
            AttributeRecord("uniform", False, (), OUTFITS[1].base_reference): 1,
        }
    )
    report.check(
        outfit_records == expected_outfit_records,
        "tsubaki definition: outfit mapping is not exactly casual(default)->"
        "neutral.png and uniform->neut_uniform.png; "
        f"actual={list(outfit_records.elements())}",
    )

    face_records = Counter(parse_attribute_records(face_group))
    expected_face_records: Counter[AttributeRecord] = Counter()
    for token in FACE_TOKENS:
        for outfit in OUTFITS:
            expected_face_records[
                AttributeRecord(
                    token,
                    token == "neut" and outfit.name == "casual",
                    (outfit.name,),
                    outfit.face_reference(token),
                )
            ] += 1
    report.check(
        face_records == expected_face_records,
        "tsubaki definition: conditioned face mappings differ from the exact "
        "21-token x 2-outfit contract; "
        f"missing={list((expected_face_records - face_records).elements())} "
        f"extra={list((face_records - expected_face_records).elements())}",
    )

    reference_pattern = re.compile(
        r'"(mod_assets/char_sprites/tsubaki/[^"\n]+\.png)"'
    )
    reference_counts = Counter(reference_pattern.findall(layered))
    expected_references = expected_layered_references()
    report.check(
        set(reference_counts) == expected_references
        and all(count == 1 for count in reference_counts.values()),
        "tsubaki definition: layeredimage references are not the exact 44-file "
        "base/face manifest; "
        f"missing={sorted(expected_references - set(reference_counts))} "
        f"extra={sorted(set(reference_counts) - expected_references)} "
        f"duplicates={sorted(name for name, count in reference_counts.items() if count != 1)}",
    )
    report.check(
        bool(
            re.search(
                r"^define ts = DynamicCharacter\([^\n]+image=['\"]tsubaki['\"]",
                source,
                re.MULTILINE,
            )
        ),
        "tsubaki definition: DynamicCharacter image tag is missing",
    )
    report.note(
        "tsubaki/definition: 2 raw bases, 42 conditioned faces, no multipart pose "
        "layers, exact transform and image tag verified"
    )


def validate_story(story_root: Path, report: ValidationReport) -> None:
    allowed = {"casual", "uniform", "post_neut", "post_revelation", *FACE_TOKENS}
    show_pattern = re.compile(r"^\s*show\s+tsubaki\b(?P<tail>[^#]*)")
    modifier_pattern = re.compile(
        r"\s+(?:at|as|behind|onlayer|zorder|with)\b", re.IGNORECASE
    )
    pose_uses: list[str] = []
    unknown_uses: list[str] = []
    show_count = 0

    for script_path in sorted(story_root.rglob("*.rpy")):
        try:
            lines = script_path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            report.error(f"cannot read {script_path} for story audit: {exc}")
            continue
        for line_number, line in enumerate(lines, start=1):
            match = show_pattern.match(line)
            if not match:
                continue
            show_count += 1
            attribute_text = modifier_pattern.split(match.group("tail"), maxsplit=1)[0]
            attributes = [token.lstrip("-") for token in attribute_text.split()]
            relative = script_path.relative_to(PROJECT_ROOT)
            retired = [token for token in attributes if token.startswith("pose_")]
            if retired:
                pose_uses.append(
                    f"{relative}:{line_number}: {', '.join(sorted(set(retired)))}"
                )
            unknown = [
                token
                for token in attributes
                if token and not token.startswith("pose_") and token not in allowed
            ]
            if unknown:
                unknown_uses.append(
                    f"{relative}:{line_number}: {', '.join(sorted(set(unknown)))}"
                )

    report.check(
        not pose_uses,
        "retired `pose_*` attributes remain on `show tsubaki` calls:\n"
        + "\n".join(f"  - {entry}" for entry in pose_uses),
    )
    report.check(
        not unknown_uses,
        "unresolved attributes remain on `show tsubaki` calls:\n"
        + "\n".join(f"  - {entry}" for entry in unknown_uses),
    )
    report.note(f"tsubaki/story: {show_count} `show tsubaki` call(s) audited")


def make_background(kind: str, size: tuple[int, int]) -> Image.Image:
    if kind == "dark":
        return Image.new("RGBA", size, (25, 27, 34, 255))
    if kind == "light":
        return Image.new("RGBA", size, (238, 235, 228, 255))
    width, height = size
    rows, columns = np.indices((height, width))
    cells = ((columns // 12) + (rows // 12)) % 2
    rgba = np.empty((height, width, 4), dtype=np.uint8)
    rgba[cells == 0] = (76, 80, 88, 255)
    rgba[cells == 1] = (116, 121, 130, 255)
    return Image.fromarray(rgba, "RGBA")


def build_review_sheet(
    sprite_root: Path,
    layer_root: Path,
    output_path: Path,
) -> None:
    backgrounds = ("dark", "light", "checker")
    panel_size = (160, 244)
    art_size = (150, 222)
    label_width = 112
    header_height = 76
    columns = tuple(
        (outfit, background) for outfit in OUTFITS for background in backgrounds
    )
    full_backgrounds = {
        background: make_background(background, CANVAS_SIZE)
        for background in backgrounds
    }
    panel_backgrounds = {
        background: make_background(background, panel_size)
        for background in backgrounds
    }
    sheet = Image.new(
        "RGBA",
        (
            label_width + panel_size[0] * len(columns),
            header_height + panel_size[1] * len(FACE_TOKENS),
        ),
        (16, 18, 24, 255),
    )
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((12, 12), "TSUBAKI CONDITIONED FACE REVIEW", fill="white", font=font)
    for column, (outfit, background) in enumerate(columns):
        center_x = label_width + column * panel_size[0] + panel_size[0] // 2
        draw.text(
            (center_x, 50),
            f"{outfit.name}/{background}",
            fill=(130, 225, 236, 255),
            font=font,
            anchor="mm",
        )

    bases: dict[str, np.ndarray] = {}
    for outfit in OUTFITS:
        with Image.open(sprite_root / outfit.base_name) as image:
            bases[outfit.name] = np.asarray(
                image.convert("RGBA"), dtype=np.uint8
            ).copy()

    for row, token in enumerate(FACE_TOKENS):
        top = header_height + row * panel_size[1]
        draw.text(
            (label_width - 10, top + panel_size[1] // 2),
            token.upper(),
            fill="white",
            font=font,
            anchor="rm",
        )
        for outfit_index, outfit in enumerate(OUTFITS):
            with Image.open(layer_root / outfit.face_name(token)) as image:
                layer = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
            sprite = alpha_composite(bases[outfit.name], layer)
            sprite_image = Image.fromarray(sprite, "RGBA")
            for background_index, background in enumerate(backgrounds):
                column = outfit_index * len(backgrounds) + background_index
                left = label_width + column * panel_size[0]
                rendered = Image.alpha_composite(
                    full_backgrounds[background], sprite_image
                )
                rendered.thumbnail(art_size, Image.Resampling.LANCZOS)
                panel = panel_backgrounds[background].copy()
                panel.alpha_composite(
                    rendered,
                    (
                        (panel_size[0] - rendered.width) // 2,
                        art_size[1] - rendered.height,
                    ),
                )
                panel_draw = ImageDraw.Draw(panel)
                panel_draw.rectangle(
                    (0, 0, panel_size[0] - 1, panel_size[1] - 1),
                    outline=(74, 79, 90, 255),
                )
                sheet.alpha_composite(panel, (left, top))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(output_path, format="PNG", compress_level=6)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sprite-root",
        type=Path,
        default=DEFAULT_SPRITE_ROOT,
        help="directory containing neutral.png and neut_uniform.png",
    )
    parser.add_argument(
        "--layer-root",
        type=Path,
        default=None,
        help="face-layer directory; defaults to --sprite-root",
    )
    parser.add_argument(
        "--definitions",
        type=Path,
        default=DEFAULT_DEFINITIONS,
        help="Ren'Py character-definition source",
    )
    parser.add_argument(
        "--story-root",
        type=Path,
        default=DEFAULT_STORY_ROOT,
        help="directory recursively audited for `show tsubaki` calls",
    )
    parser.add_argument(
        "--review-sheet",
        type=Path,
        default=None,
        help="optional contact-sheet output; omitted by default",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sprite_root = args.sprite_root.resolve()
    layer_root = (args.layer_root or args.sprite_root).resolve()
    definitions = args.definitions.resolve()
    story_root = args.story_root.resolve()
    report = ValidationReport()

    validate_manifest(layer_root, sprite_root, report)
    bases = validate_bases(sprite_root, report)
    validate_face_bank(layer_root, bases, report)
    validate_definition(definitions, report)
    validate_story(story_root, report)

    if args.review_sheet is not None:
        output_path = args.review_sheet.resolve()
        try:
            build_review_sheet(sprite_root, layer_root, output_path)
            report.note(f"tsubaki/review: {output_path}")
        except (OSError, ValueError) as exc:
            report.error(f"cannot write review sheet {output_path}: {exc}")

    output = sys.stderr if report.errors else sys.stdout
    if report.notes:
        print("TSUBAKI SPRITE VALIDATION METRICS", file=output)
        for note in report.notes:
            print(f"  {note}", file=output)

    if report.errors:
        print(
            f"\nTSUBAKI SPRITE VALIDATION FAILED ({len(report.errors)} issue(s))",
            file=output,
        )
        for index, error in enumerate(report.errors, start=1):
            print(
                f"  {index}. {error.replace(chr(10), chr(10) + '    ')}",
                file=output,
            )
        return 1

    print(
        "\nTSUBAKI SPRITE VALIDATION PASSED: 2 untouched neutral bases, "
        "42 conditioned face layers, transparent neutral, fixed feather masks, "
        "preserved silhouettes, distinct alternates, exact wiring, and no "
        "retired story pose attributes."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
