"""Build a staging-only full-master Tsubaki brow ownership prototype."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
STAGING = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(STAGING))

import process_sam_sprites as sparse  # noqa: E402
import process_tsubaki_face_patches as face  # noqa: E402
import process_tsubaki_sprites as tsubaki  # noqa: E402
from analyze_full_brows import extract_brows  # noqa: E402
from prototype_brow_repair import duplicate_arc_guard, full_arc_cleanup  # noqa: E402


OUT = STAGING / "full_brow_output"
REPORTED = ("worried", "unamused", "disgusted")
TARGET_CORE_CONTRAST = 32
TARGET_HALO_CONTRAST = 16


def font(size: int) -> ImageFont.ImageFont:
    candidate = Path("C:/Windows/Fonts/arial.ttf")
    return ImageFont.truetype(str(candidate), size) if candidate.is_file() else ImageFont.load_default()


def ellipse_mask(
    shape: tuple[int, int], center: tuple[float, float], axes: tuple[int, int]
) -> np.ndarray:
    mask = np.zeros(shape, dtype=np.uint8)
    cv2.ellipse(
        mask,
        (round(center[0]), round(center[1])),
        axes,
        0.0,
        0.0,
        360.0,
        1,
        thickness=-1,
    )
    return mask.astype(bool)


def target_brow_layer(
    raw_mask: np.ndarray,
    aligned_master: np.ndarray,
    canonical_blank: np.ndarray,
    canonical_to_target: np.ndarray,
    target_blank: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    initial = cv2.warpAffine(
        raw_mask.astype(np.uint8),
        canonical_to_target,
        face.OUTPUT_SIZE,
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    ).astype(bool)
    warped_expression = face.warp_rgb(aligned_master, canonical_to_target)
    warped_blank = face.warp_rgb(canonical_blank, canonical_to_target)
    delta = warped_expression.astype(np.int16) - warped_blank.astype(np.int16)
    contrast = np.abs(delta).max(axis=2)
    core = initial & (contrast >= TARGET_CORE_CONTRAST)
    halo_candidate = initial & (contrast >= TARGET_HALO_CONTRAST)
    halo = cv2.dilate(
        core.astype(np.uint8),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
    ).astype(bool) & halo_candidate
    support = core | halo
    # Retain only components that contain strong authored contrast.  This
    # rejects low-contrast hair-registration residue in the fitted corridor.
    support = sparse.retain_seeded_components(support, core, minimum_area=2)
    rgb = np.clip(target_blank.astype(np.int16) + delta, 0, 255).astype(np.uint8)
    return support, rgb, {
        "initial_pixels": int(initial.sum()),
        "core_pixels": int(core.sum()),
        "halo_pixels": int((halo & ~core).sum()),
        "support_pixels": int(support.sum()),
        "bbox": list(face.mask_bbox(support) or ()),
        "minimum_active_contrast": int(contrast[support].min()) if np.any(support) else None,
        "maximum_active_contrast": int(contrast[support].max()) if np.any(support) else None,
    }


def native_comparison(
    output: Path,
    outfit: str,
    expression: str,
    base: np.ndarray,
    target_eyes: np.ndarray,
) -> Image.Image:
    before = face.load_rgba(
        face.DEFAULT_OUTPUT_DIR / f"face_{expression}_{outfit}.png", face.OUTPUT_SIZE
    )
    after = face.load_rgba(
        output / f"face_{expression}_{outfit}.png", face.OUTPUT_SIZE
    )
    width, height = 300, 220
    eye_mid = target_eyes.mean(axis=0)
    left = round(float(eye_mid[0] - width / 2))
    top = round(float(eye_mid[1] - 116))
    box = (left, top, left + width, top + height)
    before_crop = Image.fromarray(face.alpha_composite(base, before), "RGBA").crop(box).convert("RGB")
    after_crop = Image.fromarray(face.alpha_composite(base, after), "RGBA").crop(box).convert("RGB")
    label_height = 28
    panel = Image.new("RGB", (width * 2, height + label_height), (24, 27, 31))
    panel.paste(before_crop, (0, 0))
    panel.paste(after_crop, (width, 0))
    draw = ImageDraw.Draw(panel)
    draw.text((7, height + 5), f"{expression}: schema-v4", font=font(15), fill=(240, 242, 246))
    draw.text((width + 7, height + 5), f"{expression}: full-master brow", font=font(15), fill=(240, 242, 246))
    return panel


def brow_bank(
    output: Path,
    outfit: str,
    base: np.ndarray,
    target_eyes: np.ndarray,
) -> Image.Image:
    columns = 4
    expressions = list(face.EXPRESSIONS[1:])
    rows = math.ceil(len(expressions) / columns)
    crop_width, crop_height, label_height = 270, 112, 24
    sheet = Image.new(
        "RGB",
        (columns * crop_width, rows * (crop_height + label_height)),
        (24, 27, 31),
    )
    draw = ImageDraw.Draw(sheet)
    eye_mid = target_eyes.mean(axis=0)
    left = round(float(eye_mid[0] - crop_width / 2))
    top = round(float(eye_mid[1] - 88))
    box = (left, top, left + crop_width, top + crop_height)
    for index, expression in enumerate(expressions):
        layer = face.load_rgba(
            output / f"face_{expression}_{outfit}.png", face.OUTPUT_SIZE
        )
        crop = Image.fromarray(face.alpha_composite(base, layer), "RGBA").crop(box).convert("RGB")
        x = (index % columns) * crop_width
        y = (index // columns) * (crop_height + label_height)
        sheet.paste(crop, (x, y))
        draw.text((x + 6, y + crop_height + 3), expression, font=font(14), fill=(240, 242, 246))
    return sheet


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    review = OUT / "_review"
    review.mkdir(parents=True, exist_ok=True)
    tsubaki.configure_sparse_processor()

    canonical_blank = face.load_rgb(
        face.DEFAULT_MASTER_DIR / "head_raw.png", face.SOURCE_SIZE
    )
    canonical_valid = sparse.checker_foreground(canonical_blank)
    canonical_rgba = np.dstack(
        (canonical_blank, canonical_valid.astype(np.uint8) * 255)
    )
    source_head = face.load_rgba(
        face.DEFAULT_PART_DIR / "forward_head.png", face.SOURCE_SIZE
    )
    source_neutral = face.load_rgba(
        face.DEFAULT_SOURCE_DIR / "face_neut.png", face.SOURCE_SIZE
    )
    source_composite = face.alpha_composite(source_head, source_neutral)
    source_eyes = face.amber_iris_centers(source_composite, face.SOURCE_EYE_ROI)
    source_metrics = json.loads(
        (face.DEFAULT_SOURCE_DIR / "metrics.json").read_text(encoding="utf-8")
    )
    production_matrix = np.asarray(
        source_metrics["production_matrix"], dtype=np.float32
    )

    raw_brows: dict[str, np.ndarray] = {}
    aligned_masters: dict[str, np.ndarray] = {}
    extraction_metrics: dict[str, object] = {}
    for expression in face.EXPRESSIONS[1:]:
        filename = face.MASTER_OVERRIDES.get(expression, f"expression_{expression}.png")
        donor = face.load_rgb(face.DEFAULT_MASTER_DIR / filename, face.SOURCE_SIZE)
        donor_valid = sparse.checker_foreground(donor)
        registration = face.registration_matrix(
            source_metrics["layers"][expression]["registration"]
        )
        aligned = sparse.warp_rgb(donor, registration)
        aligned_valid = sparse.warp_mask(donor_valid, registration)
        raw_sparse, _, _ = sparse.build_expression_layer(
            expression,
            canonical_rgba,
            aligned,
            aligned_valid,
            canonical_blank,
            canonical_valid,
        )
        mask, sides, _ = extract_brows(
            expression, aligned, aligned_valid, canonical_blank, raw_sparse
        )
        raw_brows[expression] = mask
        aligned_masters[expression] = aligned
        extraction_metrics[expression] = {
            "pixels": int(mask.sum()),
            "bbox": list(face.mask_bbox(mask) or ()),
            "sides": sides,
        }

    bases: dict[str, np.ndarray] = {}
    report: dict[str, object] = {
        "schema": "staging-full-master-brow-v1",
        "production_untouched": True,
        "target_contrast": {
            "core_minimum": TARGET_CORE_CONTRAST,
            "halo_minimum": TARGET_HALO_CONTRAST,
        },
        "source_extraction": extraction_metrics,
        "outfits": {},
    }
    transparent = np.zeros((face.OUTPUT_SIZE[1], face.OUTPUT_SIZE[0], 4), dtype=np.uint8)

    for outfit, spec in face.OUTFITS.items():
        base = face.load_rgba(face.SPRITE_DIR / spec["base"], face.OUTPUT_SIZE)
        featureless_rgb = face.load_rgb(
            face.DEFAULT_DONOR_DIR / spec["featureless"], face.OUTPUT_SIZE
        )
        target_eyes = face.amber_iris_centers(base, spec["target_roi"])
        matrix = face.similarity_from_two_points(source_eyes, target_eyes)
        registered = face.registered_detail_layers(face.DEFAULT_SOURCE_DIR, matrix)
        detail_layers = registered[0]
        eye_mid = target_eyes.mean(axis=0)
        patch_center = (
            float(eye_mid[0]),
            float(eye_mid[1] + face.PATCH_CENTER_BELOW_EYES),
        )
        target_skin = face.face_skin_component(
            featureless_rgb, (round(patch_center[0]), round(patch_center[1]))
        )
        patch_alpha = face.feathered_face_mask(
            base.shape[:2], patch_center, target_skin, base[:, :, 3]
        )
        patch_alpha, _ = face.normalize_interior_partial_alpha(
            patch_alpha, patch_center
        )
        featureless_matched, _, _ = face.match_donor_skin(
            featureless_rgb, base[:, :, :3], target_skin, patch_center
        )
        neutral_alpha, _ = face.base_neutral_guard_alpha(
            source_neutral, source_eyes, matrix, base[:, :, 3]
        )
        neutral_layer = np.dstack((featureless_matched, neutral_alpha))
        neutral_layer[neutral_alpha == 0, :3] = 0
        canonical_to_target = face.compose_affine(matrix, production_matrix)

        broad_brow_zone = np.zeros(target_skin.shape, dtype=bool)
        for eye_x, eye_y in target_eyes:
            broad_brow_zone |= ellipse_mask(
                target_skin.shape,
                (float(eye_x), float(eye_y - 42.0)),
                (78, 31),
            )

        target_brows: dict[str, np.ndarray] = {}
        target_brow_rgbs: dict[str, np.ndarray] = {}
        target_brow_metrics: dict[str, object] = {}
        brow_union = np.zeros(target_skin.shape, dtype=bool)
        for expression in face.EXPRESSIONS[1:]:
            support, rgb, metrics = target_brow_layer(
                raw_brows[expression],
                aligned_masters[expression],
                canonical_blank,
                canonical_to_target,
                featureless_matched,
            )
            target_brows[expression] = support
            target_brow_rgbs[expression] = rgb
            target_brow_metrics[expression] = metrics
            brow_union |= support

        accepted_details: dict[str, np.ndarray] = {}
        donor_matrices: dict[str, np.ndarray] = {}
        detail_union = np.zeros(target_skin.shape, dtype=bool)
        rejection_metrics: dict[str, object] = {}
        for expression in face.EXPRESSIONS[1:]:
            donor_registration = face.registration_matrix(
                source_metrics["layers"][expression]["registration"]
            )
            donor_to_target = face.compose_affine(
                matrix,
                face.compose_affine(production_matrix, donor_registration),
            )
            donor_matrices[expression] = donor_to_target
            reject = duplicate_arc_guard(donor_to_target, base[:, :, 3])
            accepted = detail_layers[expression] & ~broad_brow_zone & ~reject
            accepted_details[expression] = accepted
            detail_union |= accepted
            rejection_metrics[expression] = {
                "sparse_brow_pixels_replaced": int(
                    (detail_layers[expression] & broad_brow_zone).sum()
                ),
                "duplicate_corridor_pixels_rejected": int(
                    (detail_layers[expression] & reject).sum()
                ),
            }

        ownership_union = detail_union | brow_union
        face.save_rgba(OUT / f"face_neut_{outfit}.png", transparent)
        layer_reports: dict[str, object] = {}
        for expression in face.EXPRESSIONS[1:]:
            filename = face.MASTER_OVERRIDES.get(expression, f"expression_{expression}.png")
            donor = face.load_rgb(face.DEFAULT_MASTER_DIR / filename, face.SOURCE_SIZE)
            donor_to_target = donor_matrices[expression]
            warped = face.warp_rgb(donor, donor_to_target)
            corrected, _, _ = face.match_donor_skin(
                warped, base[:, :, :3], target_skin, patch_center
            )
            authored = corrected.copy()
            corrected, cleanup = full_arc_cleanup(
                corrected,
                featureless_matched,
                base[:, :, 3],
                donor_to_target,
            )
            broad_layer = np.dstack((corrected, patch_alpha))
            broad_layer[patch_alpha == 0, :3] = 0
            output = face.alpha_composite(neutral_layer, broad_layer).copy()
            output, semantic = face.restore_semantic_detail(
                base,
                output,
                authored,
                accepted_details[expression],
                ownership_union,
                patch_alpha,
            )
            # Ownership union already made the region opaque; active brow RGB
            # is now supplied from the same canonical transform as its mask.
            active_brow = target_brows[expression]
            output[active_brow, :3] = target_brow_rgbs[expression][active_brow]
            output[active_brow, 3] = 255
            output[output[:, :, 3] == 0, :3] = 0
            destination = OUT / f"face_{expression}_{outfit}.png"
            face.save_rgba(destination, output)
            layer_reports[expression] = {
                **rejection_metrics[expression],
                "full_brow": target_brow_metrics[expression],
                "full_brow_pixels": int(active_brow.sum()),
                "full_brow_pixels_outside_target_skin": int(
                    (active_brow & ~target_skin).sum()
                ),
                "semantic_active_pixels": semantic["active_pixels"],
                "cleanup_guard_pixels": cleanup["raw_guard_pixels"],
            }

        bases[outfit] = base
        report["outfits"][outfit] = {
            "target_eye_centers": target_eyes.round(4).tolist(),
            "full_brow_union_pixels": int(brow_union.sum()),
            "full_brow_union_outside_target_skin": int(
                (brow_union & ~target_skin).sum()
            ),
            "layers": layer_reports,
        }
        panels = [
            native_comparison(OUT, outfit, expression, base, target_eyes)
            for expression in REPORTED
        ]
        sheet = Image.new(
            "RGB",
            (max(panel.width for panel in panels), sum(panel.height for panel in panels)),
            (24, 27, 31),
        )
        y = 0
        for panel in panels:
            sheet.paste(panel, (0, y))
            y += panel.height
        sheet.save(review / f"{outfit}_reported_native_before_after.png", optimize=True)
        brow_bank(OUT, outfit, base, target_eyes).save(
            review / f"{outfit}_full_brow_bank_native.png", optimize=True
        )

    (OUT / "metrics.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    face.make_review(OUT, bases)
    print(f"Built full-master brow prototype: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
