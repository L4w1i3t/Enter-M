"""Prototype a hair-aware Tsubaki brow repair without touching production.

This staging-only builder starts from the same approved bases, featureless
donors, expression masters, sparse semantic layers, and registration metrics
as ``tools/process_tsubaki_face_patches.py``.  It changes three ownership
rules in the forehead region:

* the traced duplicate-arc corridors are an explicit negative/reject mask;
* semantic ink is clipped to the target outfit's featureless skin topology;
* target-base bang pixels are restored above the finished face plate.

The canonical source skin opening is locally registered to each target brow
opening with a small integer translation before brow-only semantic pixels are
restored.  Eyes, mouths, tears, blush, and the broad authored face plate keep
their existing global registration.
"""

from __future__ import annotations

import argparse
import inspect
import json
import math
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = PROJECT_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import process_sam_sprites as sparse  # noqa: E402
import process_tsubaki_face_patches as face  # noqa: E402
import process_tsubaki_sprites as source  # noqa: E402


DEFAULT_OUTPUT = PROJECT_ROOT / "tmp" / "tsubaki_brow_prototype_agent" / "output"
REPORTED = ("worried", "unamused", "disgusted")
BROW_CENTER_ABOVE_EYE = 42.0
BROW_ZONE_AXES = (72, 25)
BROW_BAND_ABOVE_EYE = (92, 6)
LOCAL_SHIFT_RADIUS = 6
LOCAL_SHIFT_PENALTY = 0.35


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--disable-local-shift",
        action="store_true",
        help="Keep the global eye registration for brows while retaining all other repairs.",
    )
    parser.add_argument(
        "--reset-brow-corridor",
        action="store_true",
        help="Experimental: erase the broad-master brow before sparse restoration.",
    )
    parser.add_argument(
        "--disable-bang-occlusion",
        action="store_true",
        help="Do not clip semantic pixels under bangs (house-style comparison).",
    )
    return parser.parse_args()


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


def shift_mask(mask: np.ndarray, dx: int, dy: int) -> np.ndarray:
    return cv2.warpAffine(
        mask.astype(np.uint8),
        np.asarray(((1.0, 0.0, dx), (0.0, 1.0, dy)), dtype=np.float32),
        face.OUTPUT_SIZE,
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    ).astype(bool)


def shift_rgb(rgb: np.ndarray, dx: int, dy: int) -> np.ndarray:
    return cv2.warpAffine(
        rgb,
        np.asarray(((1.0, 0.0, dx), (0.0, 1.0, dy)), dtype=np.float32),
        face.OUTPUT_SIZE,
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0),
    )


def registered_sparse_rgb(source_rgba: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    """Warp sparse authored RGB through its own alpha to preserve registration."""

    alpha = source_rgba[:, :, 3].astype(np.float32) / 255.0
    premultiplied = source_rgba[:, :, :3].astype(np.float32) * alpha[:, :, None]
    warped_alpha = cv2.warpAffine(
        alpha,
        matrix,
        face.OUTPUT_SIZE,
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )
    warped_premultiplied = cv2.warpAffine(
        premultiplied,
        matrix,
        face.OUTPUT_SIZE,
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0),
    )
    warped_alpha = np.clip(warped_alpha, 0.0, 1.0)
    warped_rgb = np.zeros_like(warped_premultiplied)
    valid = warped_alpha > (1.0 / 255.0)
    warped_rgb[valid] = warped_premultiplied[valid] / warped_alpha[valid, None]
    nearest_rgb = cv2.warpAffine(
        source_rgba[:, :, :3],
        matrix,
        face.OUTPUT_SIZE,
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0),
    )
    warped_rgb[~valid] = nearest_rgb[~valid]
    return np.clip(np.rint(warped_rgb), 0, 255).astype(np.uint8)


def duplicate_arc_guard(
    donor_to_target: np.ndarray, base_alpha: np.ndarray
) -> np.ndarray:
    source_guard = np.zeros((face.SOURCE_SIZE[1], face.SOURCE_SIZE[0]), dtype=np.uint8)
    for path in face.SOURCE_CREASE_PATHS:
        cv2.polylines(
            source_guard,
            [np.asarray(path, dtype=np.int32)],
            isClosed=False,
            color=1,
            thickness=face.SOURCE_CREASE_THICKNESS,
            lineType=cv2.LINE_AA,
        )
    guard = cv2.warpAffine(
        source_guard,
        donor_to_target,
        face.OUTPUT_SIZE,
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    ).astype(bool)
    return guard & (base_alpha == 255)


def full_arc_cleanup(
    rgb: np.ndarray,
    featureless_rgb: np.ndarray,
    base_alpha: np.ndarray,
    donor_to_target: np.ndarray,
) -> tuple[np.ndarray, dict[str, object]]:
    """Call either the schema-v4 or in-flight cleanup API defensively."""

    empty = np.zeros(base_alpha.shape, dtype=bool)
    parameter_count = len(inspect.signature(face.remove_duplicate_eyelid_arcs).parameters)
    if parameter_count == 5:
        result = face.remove_duplicate_eyelid_arcs(
            rgb, featureless_rgb, base_alpha, donor_to_target, empty
        )
    elif parameter_count == 6:
        result = face.remove_duplicate_eyelid_arcs(
            rgb, featureless_rgb, base_alpha, donor_to_target, empty, empty
        )
    else:
        raise RuntimeError(
            f"Unsupported cleanup API with {parameter_count} parameters"
        )
    return result[0], result[1]


def local_skin_shift(
    source_skin: np.ndarray,
    target_skin: np.ndarray,
    zone: np.ndarray,
) -> tuple[tuple[int, int], dict[str, object]]:
    """Find a conservative translation matching the bang/skin opening.

    The score uses skin XOR plus a boundary XOR term.  A quadratic penalty
    keeps the solution at zero unless the target topology supplies clear
    evidence for a local correction.
    """

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    target_boundary = cv2.morphologyEx(
        target_skin.astype(np.uint8), cv2.MORPH_GRADIENT, kernel
    ).astype(bool)
    trials: list[dict[str, object]] = []
    for dy in range(-LOCAL_SHIFT_RADIUS, LOCAL_SHIFT_RADIUS + 1):
        for dx in range(-LOCAL_SHIFT_RADIUS, LOCAL_SHIFT_RADIUS + 1):
            shifted = shift_mask(source_skin, dx, dy)
            shifted_boundary = cv2.morphologyEx(
                shifted.astype(np.uint8), cv2.MORPH_GRADIENT, kernel
            ).astype(bool)
            skin_xor = int(((shifted ^ target_skin) & zone).sum())
            boundary_xor = int(
                ((shifted_boundary ^ target_boundary) & zone).sum()
            )
            score = (
                float(skin_xor)
                + 1.75 * float(boundary_xor)
                + LOCAL_SHIFT_PENALTY * float(dx * dx + dy * dy)
            )
            trials.append(
                {
                    "dx": dx,
                    "dy": dy,
                    "score": round(score, 4),
                    "skin_xor": skin_xor,
                    "boundary_xor": boundary_xor,
                }
            )
    trials.sort(key=lambda item: (item["score"], abs(item["dx"]) + abs(item["dy"])))
    winner = trials[0]
    zero = next(item for item in trials if item["dx"] == 0 and item["dy"] == 0)
    return (
        (int(winner["dx"]), int(winner["dy"])),
        {
            "winner": winner,
            "zero_shift": zero,
            "score_improvement": round(float(zero["score"]) - float(winner["score"]), 4),
            "runner_up": trials[1],
        },
    )


def font(size: int) -> ImageFont.ImageFont:
    for candidate in (
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeui.ttf"),
    ):
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def composite(base: np.ndarray, layer: np.ndarray) -> np.ndarray:
    return face.alpha_composite(base, layer)


def scaled_crop(
    rgba: np.ndarray,
    box: tuple[int, int, int, int],
    scale: int = 3,
) -> Image.Image:
    crop = Image.fromarray(rgba, "RGBA").crop(box)
    return crop.resize((crop.width * scale, crop.height * scale), Image.Resampling.NEAREST)


def make_brow_bank(
    output_dir: Path,
    bases: dict[str, np.ndarray],
    target_eyes: dict[str, np.ndarray],
) -> None:
    review = output_dir / "_review"
    review.mkdir(parents=True, exist_ok=True)
    columns = 4
    scale = 3
    crop_width = 270
    crop_height = 112
    label_height = 31
    cell_width = crop_width * scale
    cell_height = crop_height * scale + label_height
    for outfit in face.OUTFITS:
        expressions = list(face.EXPRESSIONS[1:])
        rows = math.ceil(len(expressions) / columns)
        sheet = Image.new(
            "RGB", (columns * cell_width, rows * cell_height), (24, 27, 31)
        )
        draw = ImageDraw.Draw(sheet)
        eye_mid = target_eyes[outfit].mean(axis=0)
        left = round(float(eye_mid[0] - crop_width / 2))
        top = round(float(eye_mid[1] - 88))
        box = (left, top, left + crop_width, top + crop_height)
        for index, expression in enumerate(expressions):
            layer = face.load_rgba(
                output_dir / f"face_{expression}_{outfit}.png", face.OUTPUT_SIZE
            )
            image = scaled_crop(composite(bases[outfit], layer), box, scale).convert("RGB")
            x = (index % columns) * cell_width
            y = (index // columns) * cell_height
            sheet.paste(image, (x, y))
            draw.rectangle(
                (x, y + crop_height * scale, x + cell_width, y + cell_height),
                fill=(24, 27, 31),
            )
            draw.text(
                (x + 10, y + crop_height * scale + 5),
                expression,
                fill=(238, 240, 244),
                font=font(20),
            )
        sheet.save(review / f"{outfit}_brow_bank_3x.png", optimize=True)


def make_reported_comparisons(
    output_dir: Path,
    bases: dict[str, np.ndarray],
    target_eyes: dict[str, np.ndarray],
) -> None:
    review = output_dir / "_review"
    review.mkdir(parents=True, exist_ok=True)
    baseline_dir = face.DEFAULT_OUTPUT_DIR
    scale = 3
    crop_width = 285
    crop_height = 205
    label_height = 34
    cell_width = crop_width * scale
    cell_height = crop_height * scale + label_height
    for outfit in face.OUTFITS:
        sheet = Image.new(
            "RGB", (2 * cell_width, len(REPORTED) * cell_height), (24, 27, 31)
        )
        draw = ImageDraw.Draw(sheet)
        eye_mid = target_eyes[outfit].mean(axis=0)
        left = round(float(eye_mid[0] - crop_width / 2))
        top = round(float(eye_mid[1] - 115))
        box = (left, top, left + crop_width, top + crop_height)
        for row, expression in enumerate(REPORTED):
            before = face.load_rgba(
                baseline_dir / f"face_{expression}_{outfit}.png", face.OUTPUT_SIZE
            )
            after = face.load_rgba(
                output_dir / f"face_{expression}_{outfit}.png", face.OUTPUT_SIZE
            )
            for column, (label, layer) in enumerate(
                (("current schema-v4", before), ("hair-aware prototype", after))
            ):
                image = scaled_crop(composite(bases[outfit], layer), box, scale).convert("RGB")
                x = column * cell_width
                y = row * cell_height
                sheet.paste(image, (x, y))
                draw.rectangle(
                    (x, y + crop_height * scale, x + cell_width, y + cell_height),
                    fill=(24, 27, 31),
                )
                draw.text(
                    (x + 10, y + crop_height * scale + 5),
                    f"{expression} | {label}",
                    fill=(238, 240, 244),
                    font=font(20),
                )
        sheet.save(review / f"{outfit}_reported_before_after_3x.png", optimize=True)


def main() -> int:
    args = parse_args()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    source.configure_sparse_processor()
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

    canonical_featureless = face.load_rgb(
        face.DEFAULT_MASTER_DIR / "head_raw.png", face.SOURCE_SIZE
    )
    canonical_valid = sparse.checker_foreground(canonical_featureless)
    canonical_skin = source.featureless_face_interior(
        canonical_featureless, canonical_valid
    )

    bases: dict[str, np.ndarray] = {}
    target_eyes_by_outfit: dict[str, np.ndarray] = {}
    report: dict[str, object] = {
        "schema": "prototype-brow-hair-ownership-v1",
        "production_untouched": True,
        "local_shift_enabled": not args.disable_local_shift,
        "brow_corridor_reset_enabled": args.reset_brow_corridor,
        "bang_occlusion_enabled": not args.disable_bang_occlusion,
        "semantic_rgb_source": "registered sparse RGBA, not separately warped full master",
        "expressions": list(face.EXPRESSIONS),
        "rejected_semantics": "all sparse support inside traced duplicate-arc corridors",
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
        eye_midpoint = target_eyes.mean(axis=0)
        patch_center = (
            float(eye_midpoint[0]),
            float(eye_midpoint[1] + face.PATCH_CENTER_BELOW_EYES),
        )
        target_skin = face.face_skin_component(
            featureless_rgb,
            (round(patch_center[0]), round(patch_center[1])),
        )
        patch_alpha = face.feathered_face_mask(
            base.shape[:2], patch_center, target_skin, base[:, :, 3]
        )
        patch_alpha, _ = face.normalize_interior_partial_alpha(
            patch_alpha, patch_center
        )
        featureless_matched_rgb, _, _ = face.match_donor_skin(
            featureless_rgb, base[:, :, :3], target_skin, patch_center
        )
        neutral_guard_alpha, _ = face.base_neutral_guard_alpha(
            source_neutral,
            source_eyes,
            matrix,
            base[:, :, 3],
        )
        neutral_guard_layer = np.dstack(
            (featureless_matched_rgb, neutral_guard_alpha)
        )
        neutral_guard_layer[neutral_guard_alpha == 0, :3] = 0

        canonical_to_target = face.compose_affine(matrix, production_matrix)
        registered_skin = cv2.warpAffine(
            canonical_skin.astype(np.uint8),
            canonical_to_target,
            face.OUTPUT_SIZE,
            flags=cv2.INTER_NEAREST,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=0,
        ).astype(bool)

        brow_zones: list[np.ndarray] = []
        shift_metrics: list[dict[str, object]] = []
        shifts: list[tuple[int, int]] = []
        for side, (eye_x, eye_y) in zip(("viewer-left", "viewer-right"), target_eyes):
            zone = ellipse_mask(
                target_skin.shape,
                (float(eye_x), float(eye_y - BROW_CENTER_ABOVE_EYE)),
                BROW_ZONE_AXES,
            )
            shift, metrics = local_skin_shift(registered_skin, target_skin, zone)
            proposed_shift = shift
            if args.disable_local_shift:
                shift = (0, 0)
            brow_zones.append(zone)
            shifts.append(shift)
            shift_metrics.append(
                {
                    "side": side,
                    "proposed_shift": list(proposed_shift),
                    "applied_shift": list(shift),
                    **metrics,
                }
            )

        donor_matrices: dict[str, np.ndarray] = {}
        reject_guards: dict[str, np.ndarray] = {}
        accepted_details: dict[str, np.ndarray] = {}
        accepted_brows: dict[str, list[np.ndarray]] = {}
        semantic_rgbs: dict[str, np.ndarray] = {}
        per_expression_acceptance: dict[str, object] = {}
        accepted_union = np.zeros(target_skin.shape, dtype=bool)
        combined_brow_zone = np.logical_or.reduce(brow_zones)
        brow_reset_mask = cv2.dilate(
            combined_brow_zone.astype(np.uint8),
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
        ).astype(bool)
        brow_reset_mask &= target_skin

        for expression in face.EXPRESSIONS[1:]:
            layer_metrics = source_metrics["layers"][expression]
            donor_registration = face.registration_matrix(
                layer_metrics["registration"]
            )
            donor_to_production = face.compose_affine(
                production_matrix, donor_registration
            )
            donor_to_target = face.compose_affine(matrix, donor_to_production)
            donor_matrices[expression] = donor_to_target
            reject_guard = duplicate_arc_guard(donor_to_target, base[:, :, 3])
            reject_guards[expression] = reject_guard

            original = detail_layers[expression]
            sparse_rgba = face.load_rgba(
                face.DEFAULT_SOURCE_DIR / f"face_{expression}.png",
                face.SOURCE_SIZE,
            )
            semantic_rgbs[expression] = registered_sparse_rgb(sparse_rgba, matrix)
            non_brow = original & ~combined_brow_zone
            shifted_brow_parts: list[np.ndarray] = []
            for zone, (dx, dy) in zip(brow_zones, shifts):
                shifted_brow_parts.append(shift_mask(original & zone, dx, dy))
            shifted_brow = np.logical_or.reduce(shifted_brow_parts)
            accepted = (non_brow | shifted_brow) & target_skin & ~reject_guard
            accepted_details[expression] = accepted
            accepted_brows[expression] = shifted_brow_parts
            accepted_union |= accepted
            per_expression_acceptance[expression] = {
                "original_pixels": int(original.sum()),
                "original_pixels_over_target_hair": int((original & ~target_skin).sum()),
                "raw_guard_overlap_rejected": int((original & reject_guard).sum()),
                "shifted_brow_pixels": int(shifted_brow.sum()),
                "accepted_pixels": int(accepted.sum()),
                "accepted_pixels_over_target_hair": int((accepted & ~target_skin).sum()),
                "accepted_pixels_inside_reject_guard": int((accepted & reject_guard).sum()),
            }

        if np.any(accepted_union & ~target_skin):
            raise RuntimeError(f"{outfit}: accepted detail escaped target skin")

        eye_y = float(target_eyes[:, 1].mean())
        band_top = round(eye_y - BROW_BAND_ABOVE_EYE[0])
        band_bottom = round(eye_y - BROW_BAND_ABOVE_EYE[1])
        band_left = round(float(target_eyes[0, 0] - 90))
        band_right = round(float(target_eyes[1, 0] + 90))
        brow_band = np.zeros(target_skin.shape, dtype=bool)
        brow_band[band_top:band_bottom, band_left:band_right] = True
        ownership_nearby = cv2.dilate(
            accepted_union.astype(np.uint8),
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)),
        ).astype(bool)
        bang_occlusion = (
            brow_band
            & ~target_skin
            & (base[:, :, 3] == 255)
            & ((patch_alpha > 0) | ownership_nearby)
        )

        face.save_rgba(output_dir / f"face_neut_{outfit}.png", transparent)
        expression_reports: dict[str, object] = {}
        for expression in face.EXPRESSIONS[1:]:
            master_filename = face.MASTER_OVERRIDES.get(
                expression, f"expression_{expression}.png"
            )
            donor = face.load_rgb(
                face.DEFAULT_MASTER_DIR / master_filename, face.SOURCE_SIZE
            )
            donor_to_target = donor_matrices[expression]
            warped_rgb = face.warp_rgb(donor, donor_to_target)
            corrected_rgb, _, _ = face.match_donor_skin(
                warped_rgb, base[:, :, :3], target_skin, patch_center
            )
            authored_rgb = corrected_rgb.copy()

            # The traced corridor is a hard negative class.  Restore accepted
            # semantic detail after cleanup, never protect corridor pixels.
            corrected_rgb, cleanup_metrics = full_arc_cleanup(
                corrected_rgb,
                featureless_matched_rgb,
                base[:, :, 3],
                donor_to_target,
            )
            # Remove the globally warped brow and any master-specific hair
            # residue from the target's exposed forehead.  A single accepted
            # sparse brow is restored below, avoiding doubled lines when a
            # local topology correction is applied.
            if args.reset_brow_corridor:
                corrected_rgb[brow_reset_mask, :3] = featureless_matched_rgb[
                    brow_reset_mask, :3
                ]
            face_layer = np.dstack((corrected_rgb, patch_alpha))
            face_layer[patch_alpha == 0, :3] = 0
            output = face.alpha_composite(neutral_guard_layer, face_layer).copy()

            shifted_authored = semantic_rgbs[expression].copy()
            for zone, shifted_part, (dx, dy) in zip(
                brow_zones, accepted_brows[expression], shifts
            ):
                moved_rgb = shift_rgb(semantic_rgbs[expression], dx, dy)
                shifted_authored[shifted_part, :3] = moved_rgb[shifted_part, :3]

            output, semantic_metrics = face.restore_semantic_detail(
                base,
                output,
                shifted_authored,
                accepted_details[expression],
                accepted_union,
                patch_alpha,
            )

            # Encode the target base's foreground bangs above every face
            # expression.  This is visually a no-op relative to the base, but
            # it prevents face/brow RGB from surviving on top of hair.
            if not args.disable_bang_occlusion:
                output[bang_occlusion, :3] = base[bang_occlusion, :3]
                output[bang_occlusion, 3] = 255
            output[output[:, :, 3] == 0, :3] = 0

            destination = output_dir / f"face_{expression}_{outfit}.png"
            face.save_rgba(destination, output)
            rendered = face.alpha_composite(base, output)
            hair_delta = np.abs(
                rendered[:, :, :3].astype(np.int16) - base[:, :, :3].astype(np.int16)
            )
            hair_max_delta = (
                int(hair_delta[bang_occlusion].max())
                if not args.disable_bang_occlusion
                else None
            )
            if hair_max_delta:
                raise RuntimeError(
                    f"{outfit}/{expression}: foreground hair delta {hair_max_delta}"
                )
            expression_reports[expression] = {
                **per_expression_acceptance[expression],
                "output": str(destination.relative_to(PROJECT_ROOT)),
                "cleanup_guard_pixels": cleanup_metrics["raw_guard_pixels"],
                "cleanup_post_protection_pixels": cleanup_metrics[
                    "post_protection_guard_pixels"
                ],
                "semantic_newly_owned_pixels": semantic_metrics[
                    "newly_owned_alpha_pixels"
                ],
                "foreground_hair_max_channel_delta": hair_max_delta,
            }

        bases[outfit] = base
        target_eyes_by_outfit[outfit] = target_eyes
        report["outfits"][outfit] = {
            "target_eye_centers": target_eyes.round(4).tolist(),
            "global_matrix": matrix.astype(float).tolist(),
            "canonical_skin_pixels": int(registered_skin.sum()),
            "target_skin_pixels": int(target_skin.sum()),
            "local_brow_registration": shift_metrics,
            "accepted_union_pixels": int(accepted_union.sum()),
            "accepted_union_over_target_hair": int(
                (accepted_union & ~target_skin).sum()
            ),
            "bang_occlusion_pixels": int(bang_occlusion.sum()) if not args.disable_bang_occlusion else 0,
            "bang_occlusion_bbox": list(face.mask_bbox(bang_occlusion) or ()),
            "brow_reset_pixels": int(brow_reset_mask.sum()) if args.reset_brow_corridor else 0,
            "layers": expression_reports,
        }

    (output_dir / "metrics.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    face.make_review(output_dir, bases)
    make_brow_bank(output_dir, bases, target_eyes_by_outfit)
    make_reported_comparisons(output_dir, bases, target_eyes_by_outfit)
    print(f"Built hair-aware staging bank: {output_dir}")
    print(f"Metrics: {output_dir / 'metrics.json'}")
    print(f"Reviews: {output_dir / '_review'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
