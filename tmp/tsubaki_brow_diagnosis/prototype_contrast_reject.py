"""Prototype contrast-aware rejection of Tsubaki's duplicate upper-lid arcs."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

import process_tsubaki_face_patches as patches  # noqa: E402


OUT_DIR = PROJECT_ROOT / "tmp" / "tsubaki_brow_diagnosis" / "contrast_reject"
EXPRESSIONS = patches.EXPRESSIONS[1:]
VARIANTS = ((20, 32, 16),)
CROP = (385, 315, 630, 430)
SCALE = 2
LABEL_HEIGHT = 38


def font(size: int) -> ImageFont.ImageFont:
    for candidate in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def raw_guard(
    matrix: np.ndarray, base_alpha: np.ndarray, thickness: int
) -> np.ndarray:
    source_guard = np.zeros((patches.SOURCE_SIZE[1], patches.SOURCE_SIZE[0]), np.uint8)
    for path in patches.SOURCE_CREASE_PATHS:
        cv2.polylines(
            source_guard,
            [np.asarray(path, dtype=np.int32)],
            isClosed=False,
            color=1,
            thickness=thickness,
            lineType=cv2.LINE_AA,
        )
    target = cv2.warpAffine(
        source_guard,
        matrix,
        patches.OUTPUT_SIZE,
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    ).astype(bool)
    return target & (base_alpha == 255)


def clean(
    authored: np.ndarray,
    featureless: np.ndarray,
    guard: np.ndarray,
    keep: np.ndarray,
    base_alpha: np.ndarray,
) -> np.ndarray:
    cleanup = guard & ~keep
    core = cv2.erode(
        cleanup.astype(np.uint8),
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
    ).astype(bool)
    weight = cv2.GaussianBlur(cleanup.astype(np.float32), (0, 0), 0.75)
    weight *= cleanup
    weight[core] = 1.0
    weight *= base_alpha / 255.0
    return np.clip(
        np.rint(
            authored.astype(np.float32) * (1.0 - weight[:, :, None])
            + featureless.astype(np.float32) * weight[:, :, None]
        ),
        0,
        255,
    ).astype(np.uint8)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    source_head = patches.load_rgba(
        patches.DEFAULT_PART_DIR / "forward_head.png", patches.SOURCE_SIZE
    )
    source_neutral = patches.load_rgba(
        patches.DEFAULT_SOURCE_DIR / "face_neut.png", patches.SOURCE_SIZE
    )
    source_composite = patches.alpha_composite(source_head, source_neutral)
    source_eyes = patches.amber_iris_centers(source_composite, patches.SOURCE_EYE_ROI)
    source_metrics = json.loads(
        (patches.DEFAULT_SOURCE_DIR / "metrics.json").read_text(encoding="utf-8")
    )
    production = np.asarray(source_metrics["production_matrix"], np.float32)
    metrics_lines: list[str] = []

    for outfit, spec in patches.OUTFITS.items():
        base = patches.load_rgba(
            patches.SPRITE_DIR / str(spec["base"]), patches.OUTPUT_SIZE
        )
        featureless = patches.load_rgb(
            patches.DEFAULT_DONOR_DIR / str(spec["featureless"]), patches.OUTPUT_SIZE
        )
        target_eyes = patches.amber_iris_centers(base, spec["target_roi"])
        source_to_target = patches.similarity_from_two_points(source_eyes, target_eyes)
        detail_layers, _, ownership, _ = patches.registered_detail_layers(
            patches.DEFAULT_SOURCE_DIR, source_to_target
        )
        center = (
            float(target_eyes.mean(axis=0)[0]),
            float(target_eyes.mean(axis=0)[1] + patches.PATCH_CENTER_BELOW_EYES),
        )
        skin = patches.face_skin_component(featureless, (round(center[0]), round(center[1])))
        patch_alpha = patches.feathered_face_mask(
            base.shape[:2], center, skin, base[:, :, 3]
        )
        patch_alpha, _ = patches.normalize_interior_partial_alpha(patch_alpha, center)
        featureless_matched, _, _ = patches.match_donor_skin(
            featureless, base[:, :, :3], skin, center
        )
        neutral_alpha, _ = patches.base_neutral_guard_alpha(
            source_neutral, source_eyes, source_to_target, base[:, :, 3]
        )
        neutral_layer = np.dstack((featureless_matched, neutral_alpha))
        neutral_layer[neutral_alpha == 0, :3] = 0

        variants = (("current", None),) + tuple(
            (
                f"width{thickness}/core{core}/halo{halo}",
                (thickness, core, halo),
            )
            for thickness, core, halo in VARIANTS
        )
        columns = 4
        expression_rows = (len(EXPRESSIONS) + columns - 1) // columns
        crop_w, crop_h = CROP[2] - CROP[0], CROP[3] - CROP[1]
        cell_w, cell_h = crop_w * SCALE, crop_h * SCALE + LABEL_HEIGHT
        sheet = Image.new(
            "RGB",
            (
                columns * cell_w,
                expression_rows * len(variants) * cell_h,
            ),
            (27, 29, 34),
        )
        draw = ImageDraw.Draw(sheet)

        for index, expression in enumerate(EXPRESSIONS):
            master = patches.MASTER_OVERRIDES.get(expression, f"expression_{expression}.png")
            donor = patches.load_rgb(patches.DEFAULT_MASTER_DIR / master, patches.SOURCE_SIZE)
            registration = patches.registration_matrix(
                source_metrics["layers"][expression]["registration"]
            )
            donor_to_production = patches.compose_affine(production, registration)
            donor_to_target = patches.compose_affine(source_to_target, donor_to_production)
            warped = patches.warp_rgb(donor, donor_to_target)
            authored, _, _ = patches.match_donor_skin(
                warped, base[:, :, :3], skin, center
            )
            guard = raw_guard(
                donor_to_target,
                base[:, :, 3],
                patches.SOURCE_CREASE_THICKNESS,
            )
            support = detail_layers[expression]
            delta = np.abs(
                authored.astype(np.int16) - featureless_matched.astype(np.int16)
            ).max(axis=2)

            bins = (0, 8, 16, 24, 32, 40, 48, 64, 96, 256)
            counts = [
                int((guard & support & (delta >= low) & (delta < high)).sum())
                for low, high in zip(bins, bins[1:])
            ]
            metrics_lines.append(
                f"{outfit}/{expression}: guard={int(guard.sum())} "
                f"support={int((guard & support).sum())} bins={counts}"
            )

            for variant_index, (label, thresholds) in enumerate(variants):
                if thresholds is None:
                    source_path = (
                        patches.DEFAULT_OUTPUT_DIR / f"face_{expression}_{outfit}.png"
                    )
                    layer = patches.load_rgba(source_path, patches.OUTPUT_SIZE)
                else:
                    thickness, core_threshold, halo_threshold = thresholds
                    guard = raw_guard(donor_to_target, base[:, :, 3], thickness)
                    keep_core = support & (delta >= core_threshold)
                    near_core = cv2.dilate(
                        keep_core.astype(np.uint8),
                        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
                    ).astype(bool)
                    keep = keep_core | (support & near_core & (delta >= halo_threshold))
                    corrected = clean(
                        authored, featureless_matched, guard, keep, base[:, :, 3]
                    )
                    face = np.dstack((corrected, patch_alpha))
                    face[patch_alpha == 0, :3] = 0
                    layer = patches.alpha_composite(neutral_layer, face).copy()
                    effective = support & ~(guard & ~keep)
                    layer, _ = patches.restore_semantic_detail(
                        base,
                        layer,
                        authored,
                        effective,
                        ownership,
                        patch_alpha,
                    )
                composite = patches.alpha_composite(base, layer)
                crop = Image.fromarray(composite, "RGBA").convert("RGB").crop(CROP)
                crop = crop.resize(
                    (crop_w * SCALE, crop_h * SCALE), Image.Resampling.NEAREST
                )
                x = (index % columns) * cell_w
                expression_row = index // columns
                y = (expression_row * len(variants) + variant_index) * cell_h
                sheet.paste(crop, (x, y))
                draw.text(
                    (x + 6, y + crop.height + 5),
                    f"{expression} | {label}",
                    fill=(243, 243, 247),
                    font=font(21),
                )

        output = OUT_DIR / f"{outfit}_thresholds.png"
        sheet.save(output, optimize=True)
        print(output)

    (OUT_DIR / "metrics.txt").write_text(
        "\n".join(metrics_lines) + "\n", encoding="utf-8"
    )
    print("\n".join(metrics_lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
