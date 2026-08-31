"""Read-only classifier audit for Tsubaki's source-master ghost eyelid arcs.

This script writes diagnostics only beside itself.  It reconstructs the exact
schema-v4 pre-cleanup RGB and semantic support for both outfit registrations,
then evaluates conservative negative-mask thresholds inside the already traced
SOURCE_CREASE_PATHS corridors.  No production or authoring input is modified.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import process_sam_sprites as sparse  # noqa: E402
import process_tsubaki_face_patches as patches  # noqa: E402
import process_tsubaki_sprites as tsubaki_sparse  # noqa: E402


OUT_DIR = Path(__file__).resolve().parent
METRICS_PATH = ROOT / "tmp" / "tsubaki_face_patch" / "output" / "metrics.json"


def bbox(mask: np.ndarray) -> list[int] | None:
    value = patches.mask_bbox(mask)
    return list(value) if value is not None else None


def luminance(rgb: np.ndarray) -> np.ndarray:
    values = rgb.astype(np.float32)
    return (
        0.2126 * values[:, :, 0]
        + 0.7152 * values[:, :, 1]
        + 0.0722 * values[:, :, 2]
    )


def components(mask: np.ndarray, minimum_area: int = 2) -> list[dict[str, object]]:
    count, _, stats, centroids = cv2.connectedComponentsWithStats(
        mask.astype(np.uint8), connectivity=8
    )
    rows: list[dict[str, object]] = []
    for label in range(1, count):
        x, y, width, height, area = (int(value) for value in stats[label])
        if area < minimum_area:
            continue
        rows.append(
            {
                "area": area,
                "bbox": [x, y, x + width, y + height],
                "aspect": round(width / height, 3),
                "centroid": [
                    round(float(centroids[label, 0]), 3),
                    round(float(centroids[label, 1]), 3),
                ],
            }
        )
    return sorted(rows, key=lambda item: int(item["area"]), reverse=True)


def percentile(values: np.ndarray, quantiles: tuple[int, ...]) -> dict[str, float]:
    if not values.size:
        return {}
    return {
        f"p{quantile}": round(float(np.percentile(values, quantile)), 3)
        for quantile in quantiles
    }


def channel_percentiles(
    values: np.ndarray, quantiles: tuple[int, ...] = (0, 10, 25, 50, 75, 90, 100)
) -> dict[str, dict[str, float]]:
    if not values.size:
        return {}
    names = ("r", "g", "b")
    return {
        name: percentile(values[:, index], quantiles)
        for index, name in enumerate(names)
    }


def adaptive_above_lash_band(
    detail: np.ndarray,
    dark_ink: np.ndarray,
    eye_centers: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, list[dict[str, object]]]:
    """Build a narrow band 2-10 px above each expression's dark eye component."""

    height, width = detail.shape
    band = np.zeros((height, width), dtype=bool)
    selected_mask = np.zeros((height, width), dtype=bool)
    selected: list[dict[str, object]] = []
    for center_x_value, center_y_value in eye_centers:
        center_x = int(round(float(center_x_value)))
        center_y = int(round(float(center_y_value)))
        x0 = max(0, center_x - 76)
        x1 = min(width, center_x + 77)
        y0 = max(0, center_y - 28)
        y1 = min(height, center_y + 16)
        local = (detail & dark_ink)[y0:y1, x0:x1].astype(np.uint8)
        count, labels, stats, centroids = cv2.connectedComponentsWithStats(
            local, connectivity=8
        )
        candidates: list[tuple[float, int]] = []
        for label in range(1, count):
            x, y, component_width, component_height, area = (
                int(value) for value in stats[label]
            )
            if area < 8 or component_width < 10:
                continue
            centroid_y = float(centroids[label, 1] + y0)
            score = (
                component_width * 4.0
                + area * 0.5
                - abs(centroid_y - (center_y - 3.0)) * 5.0
            )
            candidates.append((score, label))
        if not candidates:
            selected.append(
                {
                    "eye_center": [center_x, center_y],
                    "component": None,
                }
            )
            continue
        _, label = max(candidates)
        component = labels == label
        selected_mask[y0:y1, x0:x1] |= component
        component_xs = np.nonzero(component)[1]
        local_min_x = int(component_xs.min())
        local_max_x = int(component_xs.max())
        profile_x: list[int] = []
        profile_y: list[int] = []
        for local_x in range(local_min_x, local_max_x + 1):
            ys = np.nonzero(component[:, local_x])[0]
            if len(ys):
                profile_x.append(local_x + x0)
                profile_y.append(int(ys.min()) + y0)
        full_x = np.arange(profile_x[0], profile_x[-1] + 1)
        top_y = np.interp(full_x, profile_x, profile_y)
        top_y = cv2.medianBlur(
            np.rint(top_y).astype(np.float32)[None, :], 5
        )[0].astype(int)
        profile_median = int(round(float(np.median(top_y))))
        clamped_top_y = np.clip(
            top_y,
            profile_median - 4,
            profile_median + 4,
        )
        for x, top in zip(full_x, clamped_top_y, strict=True):
            upper = max(0, int(top) - 10)
            lower = max(0, int(top) - 1)
            band[upper:lower, int(x)] = True
        band[:, max(0, profile_x[0] - 2) : min(width, profile_x[-1] + 3)] |= cv2.dilate(
            band[:, max(0, profile_x[0] - 2) : min(width, profile_x[-1] + 3)].astype(
                np.uint8
            ),
            cv2.getStructuringElement(cv2.MORPH_RECT, (3, 1)),
        ).astype(bool)
        x, y, component_width, component_height, area = (
            int(value) for value in stats[label]
        )
        selected.append(
            {
                "eye_center": [center_x, center_y],
                "component": {
                    "area": area,
                    "bbox": [x + x0, y + y0, x + x0 + component_width, y + y0 + component_height],
                    "centroid": [
                        round(float(centroids[label, 0] + x0), 3),
                        round(float(centroids[label, 1] + y0), 3),
                    ],
                    "score": round(float(max(candidates)[0]), 3),
                },
                "profile_x_range": [profile_x[0], profile_x[-1] + 1],
                "profile_y_range": [int(top_y.min()), int(top_y.max()) + 1],
                "profile_y_median": profile_median,
                "clamped_profile_y_range": [
                    int(clamped_top_y.min()),
                    int(clamped_top_y.max()) + 1,
                ],
            }
        )
    return band, selected_mask, selected


def retain_horizontal_components(
    mask: np.ndarray,
    minimum_width: int = 8,
    minimum_area: int = 4,
    minimum_aspect: float = 1.6,
) -> np.ndarray:
    """Retain line-like components while rejecting vertical bang fragments."""

    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        mask.astype(np.uint8), connectivity=8
    )
    retained = np.zeros(mask.shape, dtype=bool)
    for label in range(1, count):
        _, _, width, height, area = (int(value) for value in stats[label])
        if (
            area >= minimum_area
            and width >= minimum_width
            and width / max(height, 1) >= minimum_aspect
        ):
            retained |= labels == label
    return retained


def main() -> int:
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    source_guard = np.zeros(
        (patches.SOURCE_SIZE[1], patches.SOURCE_SIZE[0]), dtype=np.uint8
    )
    for path in patches.SOURCE_CREASE_PATHS:
        cv2.polylines(
            source_guard,
            [np.asarray(path, dtype=np.int32)],
            isClosed=False,
            color=1,
            thickness=patches.SOURCE_CREASE_THICKNESS,
            lineType=cv2.LINE_AA,
        )
    source_guard = source_guard > 0
    source_brow_zone = sparse.rotated_ellipse_mask(
        (patches.SOURCE_SIZE[1], patches.SOURCE_SIZE[0]),
        tsubaki_sparse.GEOMETRY.left_brow,
        tsubaki_sparse.LEFT_BROW_ANGLE,
    ) | sparse.rotated_ellipse_mask(
        (patches.SOURCE_SIZE[1], patches.SOURCE_SIZE[0]),
        tsubaki_sparse.GEOMETRY.right_brow,
        tsubaki_sparse.RIGHT_BROW_ANGLE,
    )

    report: dict[str, object] = {
        "schema": 2,
        "metrics": str(METRICS_PATH.relative_to(ROOT)),
        "rule": {
            "variant": "adaptive_interfeature_corridor_v1",
            "classification_space": (
                "registered target-space pre-cleanup corrected/authored RGB "
                "against outfit-matched featureless RGB"
            ),
            "eye_component": {
                "roi": "target eye center +/-76 x, -28..+15 y",
                "dark_ink": {
                    "luminance_maximum": 132.0,
                    "minimum_channel_maximum": 108,
                },
                "component_minimum_area": 8,
                "component_minimum_width": 10,
                "selection_score": (
                    "4*width + 0.5*area - "
                    "5*abs(centroid_y-(eye_center_y-3))"
                ),
            },
            "profile": {
                "definition": "topmost selected-component y per x",
                "gap_fill": "linear interpolation",
                "median_filter_width": 5,
                "clamp": "profile median +/-4 target pixels",
                "negative_band": "2..10 target pixels above profile",
                "horizontal_dilation": 1,
            },
            "hard_keeps": {
                "brow": "3x3 dilation of donor-registered canonical brow ellipses",
                "lash": "3x3 dilation of selected dark eye component",
            },
            "seed": {
                "maximum_channel_delta_minimum": 6,
                "signed_luminance_drop_minimum": 2.0,
            },
            "close": {
                "kernel": "3x3 ellipse",
                "maximum_channel_delta_minimum": 3,
                "signed_luminance_drop_minimum": 1.0,
            },
            "fringe": {
                "kernel": "3x3 ellipse",
                "maximum_channel_delta_minimum": 2,
                "signed_luminance_drop_minimum": 0.5,
            },
            "ownership": (
                "negative mask must be subtracted from effective detail "
                "support and remain excluded during semantic restoration"
            ),
        },
        "outfits": {},
    }

    for outfit, spec in patches.OUTFITS.items():
        outfit_metrics = metrics["outfits"][outfit]
        base = patches.load_rgba(
            patches.SPRITE_DIR / spec["base"], patches.OUTPUT_SIZE
        )
        featureless = patches.load_rgb(
            patches.DEFAULT_DONOR_DIR / spec["featureless"], patches.OUTPUT_SIZE
        )
        patch_center = tuple(float(value) for value in outfit_metrics["patch_center"])
        skin_component = patches.face_skin_component(
            featureless,
            (round(patch_center[0]), round(patch_center[1])),
        )
        featureless_matched, _, _ = patches.match_donor_skin(
            featureless,
            base[:, :, :3],
            skin_component,
            patch_center,
        )
        source_to_target = np.asarray(outfit_metrics["matrix"], dtype=np.float32)
        target_eye_centers = np.asarray(
            outfit_metrics["target_eye_centers"], dtype=np.float32
        )
        outfit_report: dict[str, object] = {"expressions": {}}

        for expression in patches.EXPRESSIONS[1:]:
            layer_metrics = outfit_metrics["layers"][expression]
            donor_to_target = np.asarray(
                layer_metrics["donor_to_target_matrix"], dtype=np.float32
            )
            master_name = patches.MASTER_OVERRIDES.get(
                expression, f"expression_{expression}.png"
            )
            donor = patches.load_rgb(
                patches.DEFAULT_MASTER_DIR / master_name, patches.SOURCE_SIZE
            )
            authored, _, _ = patches.match_donor_skin(
                patches.warp_rgb(donor, donor_to_target),
                base[:, :, :3],
                skin_component,
                patch_center,
            )
            source_detail = patches.load_rgba(
                patches.DEFAULT_SOURCE_DIR / f"face_{expression}.png",
                patches.SOURCE_SIZE,
            )
            detail = cv2.warpAffine(
                (source_detail[:, :, 3] >= patches.DETAIL_ALPHA_MINIMUM).astype(
                    np.uint8
                ),
                source_to_target,
                patches.OUTPUT_SIZE,
                flags=cv2.INTER_NEAREST,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=0,
            ).astype(bool)
            guard = cv2.warpAffine(
                source_guard.astype(np.uint8),
                donor_to_target,
                patches.OUTPUT_SIZE,
                flags=cv2.INTER_NEAREST,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=0,
            ).astype(bool)
            guard &= base[:, :, 3] == 255

            auth_luma = luminance(authored)
            clean_luma = luminance(featureless_matched)
            luma_drop = clean_luma - auth_luma
            channel_delta = np.max(
                np.abs(
                    authored.astype(np.int16)
                    - featureless_matched.astype(np.int16)
                ),
                axis=2,
            )
            minimum_channel = authored.min(axis=2)
            dark_ink = (auth_luma <= 132.0) & (minimum_channel <= 108)

            changed_guard = guard & (channel_delta >= 8)
            changed_support = changed_guard & detail
            signed_line = changed_guard & (luma_drop >= 4.0)
            reject_core = signed_line & ~dark_ink
            true_dark_keep = changed_support & dark_ink
            dark_keep_fringe = cv2.dilate(
                true_dark_keep.astype(np.uint8),
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
            ).astype(bool)
            reject_fringe = cv2.dilate(
                reject_core.astype(np.uint8),
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
            ).astype(bool)
            reject_fringe &= guard & ~dark_keep_fringe
            reject = reject_core | reject_fringe

            adaptive_band, selected_eye_mask, selected_eye_components = adaptive_above_lash_band(
                detail, dark_ink, target_eye_centers
            )
            adaptive_seed = (
                adaptive_band
                & (channel_delta >= 6)
                & (luma_drop >= 2.0)
            )
            adaptive_core = cv2.morphologyEx(
                adaptive_seed.astype(np.uint8),
                cv2.MORPH_CLOSE,
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
            ).astype(bool)
            adaptive_core &= (
                adaptive_band
                & (channel_delta >= 3)
                & (luma_drop >= 1.0)
            )
            adaptive_reject = cv2.dilate(
                adaptive_core.astype(np.uint8),
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
            ).astype(bool)
            adaptive_reject &= adaptive_band

            target_brow_zone = cv2.warpAffine(
                source_brow_zone.astype(np.uint8),
                donor_to_target,
                patches.OUTPUT_SIZE,
                flags=cv2.INTER_NEAREST,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=0,
            ).astype(bool)
            brow_keep = cv2.dilate(
                target_brow_zone.astype(np.uint8),
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
            ).astype(bool)
            lash_keep = cv2.dilate(
                selected_eye_mask.astype(np.uint8),
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
            ).astype(bool)
            refined_zone = adaptive_band & ~brow_keep & ~lash_keep
            # The sparse alpha is the strongest available provenance signal:
            # it marks pixels authored as expression detail rather than smooth
            # skin.  A small horizontal close joins anti-aliased arc gaps but
            # does not bridge vertically into the true lash.
            refined_seed = (
                refined_zone
                & detail
                & (channel_delta >= 6)
                & (luma_drop >= 2.0)
            )
            refined_joined = cv2.morphologyEx(
                refined_seed.astype(np.uint8),
                cv2.MORPH_CLOSE,
                cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1)),
            ).astype(bool)
            refined_joined &= (
                refined_zone
                & (channel_delta >= 3)
                & (luma_drop >= 1.0)
            )
            refined_core = retain_horizontal_components(refined_joined)
            refined_reject = cv2.dilate(
                refined_core.astype(np.uint8),
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
            ).astype(bool)
            refined_reject &= (
                refined_zone
                & (channel_delta >= 2)
                & (luma_drop >= 0.5)
            )

            # A vertical black-hat transform detects thin horizontal dark
            # ridges while naturally ignoring long vertical bang strands and
            # broad skin-tone mismatch.  Sparse detail remains the seed
            # provenance, but the one-pixel fringe may extend beyond it to
            # remove anti-aliasing completely.
            auth_luma_u8 = np.clip(np.rint(auth_luma), 0, 255).astype(np.uint8)
            vertical_close = cv2.morphologyEx(
                auth_luma_u8,
                cv2.MORPH_CLOSE,
                cv2.getStructuringElement(cv2.MORPH_RECT, (1, 9)),
            )
            vertical_blackhat = vertical_close.astype(np.int16) - auth_luma_u8.astype(
                np.int16
            )
            ridge_seed = (
                refined_zone
                & (vertical_blackhat >= 4)
                & (channel_delta >= 6)
                & (luma_drop >= 2.0)
            )
            ridge_joined = cv2.morphologyEx(
                ridge_seed.astype(np.uint8),
                cv2.MORPH_CLOSE,
                cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1)),
            ).astype(bool)
            ridge_joined &= (
                refined_zone
                & (vertical_blackhat >= 2)
                & (channel_delta >= 3)
                & (luma_drop >= 1.0)
            )
            ridge_core = retain_horizontal_components(
                ridge_joined,
                minimum_width=6,
                minimum_area=3,
                minimum_aspect=1.5,
            )
            ridge_reject = cv2.dilate(
                ridge_core.astype(np.uint8),
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
            ).astype(bool)
            ridge_reject &= (
                refined_zone
                & (vertical_blackhat >= 1)
                & (channel_delta >= 2)
                & (luma_drop >= 0.5)
            )

            # Conservative complete-corridor replacement: unlike the ridge
            # experiment, this deliberately owns every donor-darker changed
            # pixel in the narrow inter-feature band.  The explicit brow and
            # lash exclusions are geometric invariants, and the positive
            # signed-drop gate prevents bright sclera/highlights from entering.
            corridor_seed = (
                refined_zone
                & (channel_delta >= 6)
                & (luma_drop >= 2.0)
            )
            corridor_core = cv2.morphologyEx(
                corridor_seed.astype(np.uint8),
                cv2.MORPH_CLOSE,
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
            ).astype(bool)
            corridor_core &= (
                refined_zone
                & (channel_delta >= 3)
                & (luma_drop >= 1.0)
            )
            corridor_reject = cv2.dilate(
                corridor_core.astype(np.uint8),
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
            ).astype(bool)
            corridor_reject &= (
                refined_zone
                & (channel_delta >= 2)
                & (luma_drop >= 0.5)
            )

            current_layer = patches.load_rgba(
                patches.SPRITE_DIR / f"face_{expression}_{outfit}.png",
                patches.OUTPUT_SIZE,
            )
            current_composite = patches.alpha_composite(base, current_layer)[:, :, :3]
            current_luma_drop = luminance(featureless_matched) - luminance(
                current_composite
            )
            current_channel_delta = np.max(
                np.abs(
                    current_composite.astype(np.int16)
                    - featureless_matched.astype(np.int16)
                ),
                axis=2,
            )

            ambiguous = changed_support & ~reject & ~true_dark_keep
            expression_report = {
                "guard_pixels": int(guard.sum()),
                "guard_bbox": bbox(guard),
                "semantic_overlap_pixels": int((guard & detail).sum()),
                "changed_semantic_overlap_pixels": int(changed_support.sum()),
                "changed_guard_pixels": int(changed_guard.sum()),
                "true_dark_keep_pixels": int(true_dark_keep.sum()),
                "true_dark_keep_bbox": bbox(true_dark_keep),
                "reject_core_pixels": int(reject_core.sum()),
                "reject_core_bbox": bbox(reject_core),
                "reject_core_adjacent_dark_pixels": int(
                    (reject_core & dark_keep_fringe).sum()
                ),
                "reject_fringe_pixels": int(reject_fringe.sum()),
                "reject_pixels": int(reject.sum()),
                "reject_bbox": bbox(reject),
                "reject_components": components(reject),
                "ambiguous_changed_support_pixels": int(ambiguous.sum()),
                "reject_dark_overlap_pixels": int((reject & true_dark_keep).sum()),
                "adaptive_band_pixels": int(adaptive_band.sum()),
                "adaptive_band_bbox": bbox(adaptive_band),
                "adaptive_eye_components": selected_eye_components,
                "adaptive_seed_pixels": int(adaptive_seed.sum()),
                "adaptive_core_pixels": int(adaptive_core.sum()),
                "adaptive_reject_pixels": int(adaptive_reject.sum()),
                "adaptive_reject_bbox": bbox(adaptive_reject),
                "adaptive_reject_components": components(adaptive_reject),
                "adaptive_reject_dark_overlap_pixels": int(
                    (adaptive_reject & true_dark_keep).sum()
                ),
                "refined_zone_pixels": int(refined_zone.sum()),
                "refined_zone_bbox": bbox(refined_zone),
                "refined_seed_pixels": int(refined_seed.sum()),
                "refined_seed_components": components(refined_seed, 1),
                "refined_core_pixels": int(refined_core.sum()),
                "refined_core_components": components(refined_core, 1),
                "refined_reject_pixels": int(refined_reject.sum()),
                "refined_reject_bbox": bbox(refined_reject),
                "refined_reject_components": components(refined_reject, 1),
                "refined_brow_overlap_pixels": int(
                    (refined_reject & target_brow_zone).sum()
                ),
                "refined_lash_overlap_pixels": int(
                    (refined_reject & selected_eye_mask).sum()
                ),
                "refined_bright_overlap_pixels": int(
                    (refined_reject & (luma_drop < 0.0)).sum()
                ),
                "refined_dark_pixels": int((refined_reject & dark_ink).sum()),
                "ridge_seed_pixels": int(ridge_seed.sum()),
                "ridge_seed_components": components(ridge_seed, 1),
                "ridge_core_pixels": int(ridge_core.sum()),
                "ridge_core_components": components(ridge_core, 1),
                "ridge_reject_pixels": int(ridge_reject.sum()),
                "ridge_reject_bbox": bbox(ridge_reject),
                "ridge_reject_components": components(ridge_reject, 1),
                "ridge_brow_overlap_pixels": int(
                    (ridge_reject & target_brow_zone).sum()
                ),
                "ridge_lash_overlap_pixels": int(
                    (ridge_reject & selected_eye_mask).sum()
                ),
                "ridge_bright_overlap_pixels": int(
                    (ridge_reject & (luma_drop < 0.0)).sum()
                ),
                "ridge_dark_pixels": int((ridge_reject & dark_ink).sum()),
                "ridge_blackhat": percentile(
                    vertical_blackhat[ridge_reject],
                    (0, 10, 25, 50, 75, 90, 100),
                ),
                "ridge_luma_drop": percentile(
                    luma_drop[ridge_reject],
                    (0, 10, 25, 50, 75, 90, 100),
                ),
                "ridge_channel_delta": percentile(
                    channel_delta[ridge_reject],
                    (0, 10, 25, 50, 75, 90, 100),
                ),
                "corridor_seed_pixels": int(corridor_seed.sum()),
                "corridor_core_pixels": int(corridor_core.sum()),
                "corridor_reject_pixels": int(corridor_reject.sum()),
                "corridor_reject_bbox": bbox(corridor_reject),
                "corridor_reject_components": components(corridor_reject, 1),
                "corridor_brow_overlap_pixels": int(
                    (corridor_reject & target_brow_zone).sum()
                ),
                "corridor_lash_overlap_pixels": int(
                    (corridor_reject & selected_eye_mask).sum()
                ),
                "corridor_bright_overlap_pixels": int(
                    (corridor_reject & (luma_drop < 0.0)).sum()
                ),
                "corridor_dark_pixels": int((corridor_reject & dark_ink).sum()),
                "corridor_luma_drop": percentile(
                    luma_drop[corridor_reject],
                    (0, 10, 25, 50, 75, 90, 100),
                ),
                "corridor_channel_delta": percentile(
                    channel_delta[corridor_reject],
                    (0, 10, 25, 50, 75, 90, 100),
                ),
                "current_corridor_nonidentical_pixels": int(
                    (corridor_reject & (current_channel_delta > 0)).sum()
                ),
                "current_corridor_luma_drop": percentile(
                    current_luma_drop[corridor_reject],
                    (0, 10, 25, 50, 75, 90, 100),
                ),
                "current_corridor_channel_delta": percentile(
                    current_channel_delta[corridor_reject],
                    (0, 10, 25, 50, 75, 90, 100),
                ),
                "signed_line_luminance_drop": percentile(
                    luma_drop[signed_line], (0, 10, 25, 50, 75, 90, 100)
                ),
                "signed_line_channel_delta": percentile(
                    channel_delta[signed_line], (0, 10, 25, 50, 75, 90, 100)
                ),
                "reject_rgb_ranges": {
                    "minimum": (
                        authored[reject_core].min(axis=0).astype(int).tolist()
                        if np.any(reject_core)
                        else None
                    ),
                    "maximum": (
                        authored[reject_core].max(axis=0).astype(int).tolist()
                        if np.any(reject_core)
                        else None
                    ),
                },
                "known_arc_sample_pixels": int(
                    (guard & detail & ~dark_ink & (luma_drop >= 4.0)).sum()
                ),
                "known_arc_sample_rgb": channel_percentiles(
                    authored[guard & detail & ~dark_ink & (luma_drop >= 4.0)]
                ),
                "known_arc_sample_luma_drop": percentile(
                    luma_drop[guard & detail & ~dark_ink & (luma_drop >= 4.0)],
                    (0, 10, 25, 50, 75, 90, 100),
                ),
                "known_arc_sample_delta": percentile(
                    channel_delta[guard & detail & ~dark_ink & (luma_drop >= 4.0)],
                    (0, 10, 25, 50, 75, 90, 100),
                ),
            }
            outfit_report["expressions"][expression] = expression_report

            if outfit == "uniform" and expression in {
                "worried",
                "unamused",
                "disgusted",
            }:
                crop = (400, 338, 612, 366)
                x0, y0, x1, y1 = crop
                plain = authored[y0:y1, x0:x1].copy()
                overlay = plain.copy()
                local_dark = true_dark_keep[y0:y1, x0:x1]
                local_core = reject_core[y0:y1, x0:x1]
                local_fringe = reject_fringe[y0:y1, x0:x1]
                overlay[local_fringe] = np.asarray((32, 96, 255), dtype=np.uint8)
                overlay[local_core] = np.asarray((255, 32, 32), dtype=np.uint8)
                overlay[local_dark] = np.asarray((32, 220, 64), dtype=np.uint8)
                scale = 4
                width = (x1 - x0) * scale
                height = (y1 - y0) * scale
                diagnostic = Image.new("RGB", (width, height * 2), "white")
                diagnostic.paste(
                    Image.fromarray(plain, "RGB").resize(
                        (width, height), Image.Resampling.NEAREST
                    ),
                    (0, 0),
                )
                diagnostic.paste(
                    Image.fromarray(overlay, "RGB").resize(
                        (width, height), Image.Resampling.NEAREST
                    ),
                    (0, height),
                )
                draw = ImageDraw.Draw(diagnostic)
                draw.text((4, 3), "authored", fill=(0, 0, 255))
                draw.text(
                    (4, height + 3),
                    "green=dark keep red=reject core blue=fringe",
                    fill=(0, 0, 0),
                )
                diagnostic.save(
                    OUT_DIR / f"{expression}_uniform_rule_overlay.png",
                    optimize=True,
                )

                current = current_composite
                direct = current.copy()
                direct[reject] = featureless_matched[reject]
                comparison = Image.new("RGB", (width, height * 2), "white")
                comparison.paste(
                    Image.fromarray(current[y0:y1, x0:x1], "RGB").resize(
                        (width, height), Image.Resampling.NEAREST
                    ),
                    (0, 0),
                )
                comparison.paste(
                    Image.fromarray(direct[y0:y1, x0:x1], "RGB").resize(
                        (width, height), Image.Resampling.NEAREST
                    ),
                    (0, height),
                )
                comparison_draw = ImageDraw.Draw(comparison)
                comparison_draw.text((4, 3), "current", fill=(0, 0, 255))
                comparison_draw.text(
                    (4, height + 3),
                    "direct reject replacement prototype",
                    fill=(0, 0, 255),
                )
                comparison.save(
                    OUT_DIR / f"{expression}_uniform_direct_prototype.png",
                    optimize=True,
                )

                geometry_reject = guard & ~dark_ink
                geometry_direct = current.copy()
                geometry_direct[geometry_reject] = featureless_matched[
                    geometry_reject
                ]
                geometry_image = Image.fromarray(
                    geometry_direct[y0:y1, x0:x1], "RGB"
                ).resize((width, height), Image.Resampling.NEAREST)
                geometry_image.save(
                    OUT_DIR / f"{expression}_uniform_geometry_prototype.png",
                    optimize=True,
                )
                guard_overlay = authored.copy()
                guard_overlay[guard] = np.rint(
                    0.35 * guard_overlay[guard]
                    + 0.65 * np.asarray((255, 0, 255), dtype=np.float32)
                ).astype(np.uint8)
                Image.fromarray(
                    guard_overlay[y0:y1, x0:x1], "RGB"
                ).resize((width, height), Image.Resampling.NEAREST).save(
                    OUT_DIR / f"{expression}_uniform_guard_overlay.png",
                    optimize=True,
                )

                adaptive_direct = current.copy()
                adaptive_direct[adaptive_reject] = featureless_matched[
                    adaptive_reject
                ]
                Image.fromarray(
                    adaptive_direct[y0:y1, x0:x1], "RGB"
                ).resize((width, height), Image.Resampling.NEAREST).save(
                    OUT_DIR / f"{expression}_uniform_adaptive_prototype.png",
                    optimize=True,
                )
                full_crop = (390, 300, 620, 382)
                fx0, fy0, fx1, fy1 = full_crop
                full_width = (fx1 - fx0) * 3
                full_height = (fy1 - fy0) * 3
                full_comparison = Image.new(
                    "RGB", (full_width, full_height * 2), "white"
                )
                full_comparison.paste(
                    Image.fromarray(current[fy0:fy1, fx0:fx1], "RGB").resize(
                        (full_width, full_height), Image.Resampling.NEAREST
                    ),
                    (0, 0),
                )
                full_comparison.paste(
                    Image.fromarray(
                        adaptive_direct[fy0:fy1, fx0:fx1], "RGB"
                    ).resize(
                        (full_width, full_height), Image.Resampling.NEAREST
                    ),
                    (0, full_height),
                )
                full_draw = ImageDraw.Draw(full_comparison)
                full_draw.text((4, 3), "current", fill=(0, 0, 255))
                full_draw.text(
                    (4, full_height + 3),
                    "adaptive prototype",
                    fill=(0, 0, 255),
                )
                full_comparison.save(
                    OUT_DIR / f"{expression}_uniform_adaptive_full.png",
                    optimize=True,
                )
                adaptive_overlay = authored.copy()
                adaptive_overlay[adaptive_band] = np.rint(
                    0.45 * adaptive_overlay[adaptive_band]
                    + 0.55 * np.asarray((255, 0, 255), dtype=np.float32)
                ).astype(np.uint8)
                adaptive_overlay[adaptive_reject] = np.asarray(
                    (255, 32, 32), dtype=np.uint8
                )
                Image.fromarray(
                    adaptive_overlay[y0:y1, x0:x1], "RGB"
                ).resize((width, height), Image.Resampling.NEAREST).save(
                    OUT_DIR / f"{expression}_uniform_adaptive_overlay.png",
                    optimize=True,
                )

                refined_direct = current.copy()
                refined_direct[refined_reject] = featureless_matched[
                    refined_reject
                ]
                refined_full = Image.new(
                    "RGB", (full_width, full_height * 2), "white"
                )
                refined_full.paste(
                    Image.fromarray(current[fy0:fy1, fx0:fx1], "RGB").resize(
                        (full_width, full_height), Image.Resampling.NEAREST
                    ),
                    (0, 0),
                )
                refined_full.paste(
                    Image.fromarray(
                        refined_direct[fy0:fy1, fx0:fx1], "RGB"
                    ).resize(
                        (full_width, full_height), Image.Resampling.NEAREST
                    ),
                    (0, full_height),
                )
                refined_draw = ImageDraw.Draw(refined_full)
                refined_draw.text((4, 3), "current", fill=(0, 0, 255))
                refined_draw.text(
                    (4, full_height + 3),
                    "refined semantic prototype",
                    fill=(0, 0, 255),
                )
                refined_full.save(
                    OUT_DIR / f"{expression}_uniform_refined_full.png",
                    optimize=True,
                )

                ridge_direct = current.copy()
                ridge_direct[ridge_reject] = featureless_matched[ridge_reject]
                ridge_full = Image.new(
                    "RGB", (full_width, full_height * 2), "white"
                )
                ridge_full.paste(
                    Image.fromarray(current[fy0:fy1, fx0:fx1], "RGB").resize(
                        (full_width, full_height), Image.Resampling.NEAREST
                    ),
                    (0, 0),
                )
                ridge_full.paste(
                    Image.fromarray(ridge_direct[fy0:fy1, fx0:fx1], "RGB").resize(
                        (full_width, full_height), Image.Resampling.NEAREST
                    ),
                    (0, full_height),
                )
                ridge_draw = ImageDraw.Draw(ridge_full)
                ridge_draw.text((4, 3), "current", fill=(0, 0, 255))
                ridge_draw.text(
                    (4, full_height + 3),
                    "vertical-ridge prototype",
                    fill=(0, 0, 255),
                )
                ridge_full.save(
                    OUT_DIR / f"{expression}_uniform_ridge_full.png",
                    optimize=True,
                )

                corridor_direct = current.copy()
                corridor_direct[corridor_reject] = featureless_matched[
                    corridor_reject
                ]
                corridor_full = Image.new(
                    "RGB", (full_width, full_height * 2), "white"
                )
                corridor_full.paste(
                    Image.fromarray(current[fy0:fy1, fx0:fx1], "RGB").resize(
                        (full_width, full_height), Image.Resampling.NEAREST
                    ),
                    (0, 0),
                )
                corridor_full.paste(
                    Image.fromarray(
                        corridor_direct[fy0:fy1, fx0:fx1], "RGB"
                    ).resize(
                        (full_width, full_height), Image.Resampling.NEAREST
                    ),
                    (0, full_height),
                )
                corridor_draw = ImageDraw.Draw(corridor_full)
                corridor_draw.text((4, 3), "current", fill=(0, 0, 255))
                corridor_draw.text(
                    (4, full_height + 3),
                    "safe corridor prototype",
                    fill=(0, 0, 255),
                )
                corridor_full.save(
                    OUT_DIR / f"{expression}_uniform_corridor_full.png",
                    optimize=True,
                )

        report["outfits"][outfit] = outfit_report

    destination = OUT_DIR / "ghost_arc_rule_audit.json"
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
