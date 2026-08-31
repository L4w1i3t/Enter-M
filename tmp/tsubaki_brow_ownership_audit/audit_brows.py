"""Diagnostic-only extraction of authored Tsubaki eyebrow ownership.

This script never writes production assets.  It aligns each approved full
expression master to the featureless authoring head, compares the authored
ink with the featureless control, and extends the already trusted sparse brow
seed through the bangs.  Near-horizontal line filtering rejects the much
steeper bang outlines and the y-limited brow ROIs exclude upper-eyelid arcs.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

import process_sam_sprites as sparse  # noqa: E402
import process_tsubaki_sprites as tsubaki  # noqa: E402


OUTPUT_DIR = Path(__file__).resolve().parent
MASTER_DIR = PROJECT_ROOT / "tmp" / "tsubaki_sprite_masters"


def line_kernel(length: int, angle_degrees: float) -> np.ndarray:
    size = length * 2 + 1
    kernel = np.zeros((size, size), dtype=np.uint8)
    center = length
    radius = length // 2
    angle = math.radians(angle_degrees)
    dx = round(radius * math.cos(angle))
    dy = round(radius * math.sin(angle))
    cv2.line(
        kernel,
        (center - dx, center - dy),
        (center + dx, center + dy),
        1,
        thickness=1,
    )
    return kernel


def retain_seeded(mask: np.ndarray, seed: np.ndarray) -> np.ndarray:
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        mask.astype(np.uint8), connectivity=8
    )
    retained = np.zeros(mask.shape, dtype=bool)
    for label in range(1, count):
        component = labels == label
        if stats[label, cv2.CC_STAT_AREA] >= 3 and np.any(component & seed):
            retained |= component
    return retained


def mask_bbox(mask: np.ndarray) -> list[int] | None:
    yy, xx = np.nonzero(mask)
    if not len(xx):
        return None
    return [int(xx.min()), int(yy.min()), int(xx.max()) + 1, int(yy.max()) + 1]


def fitted_curve_band(seed: np.ndarray, roi: np.ndarray) -> np.ndarray:
    """Return a narrow quadratic band through the trusted skin-side brow ink."""

    yy, xx = np.nonzero(seed)
    if len(xx) < 8:
        return np.zeros(seed.shape, dtype=bool)
    keep = np.ones(len(xx), dtype=bool)
    coefficients = np.polyfit(xx, yy, deg=2)
    for _ in range(4):
        prediction = np.polyval(coefficients, xx)
        residual = np.abs(yy - prediction)
        next_keep = residual <= max(4.0, float(np.percentile(residual, 68)))
        if int(next_keep.sum()) < 8 or np.array_equal(next_keep, keep):
            break
        keep = next_keep
        coefficients = np.polyfit(xx[keep], yy[keep], deg=2)

    all_y, all_x = np.indices(seed.shape)
    expected_y = np.polyval(coefficients, all_x)
    x_min = max(0, int(xx[keep].min()) - 38)
    x_max = min(seed.shape[1], int(xx[keep].max()) + 39)
    return (
        roi
        & (all_x >= x_min)
        & (all_x < x_max)
        & (np.abs(all_y - expected_y) <= 7.0)
    )


def get_font(size: int) -> ImageFont.ImageFont:
    for name in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tsubaki.configure_sparse_processor()

    featureless_rgb = tsubaki.load_rgb(MASTER_DIR / "head_raw.png")
    featureless_valid = sparse.checker_foreground(featureless_rgb)
    featureless_rgba = np.dstack(
        (featureless_rgb, featureless_valid.astype(np.uint8) * 255)
    )
    shape = featureless_valid.shape

    brow_rois = {
        "left": sparse.rotated_ellipse_mask(
            shape, sparse.EllipseSpec(402, 596, 94, 34), 7.0
        ),
        "right": sparse.rotated_ellipse_mask(
            shape, sparse.EllipseSpec(614, 596, 94, 34), -7.0
        ),
    }
    trusted_brow_rois = {
        "left": sparse.rotated_ellipse_mask(
            shape, tsubaki.GEOMETRY.left_brow, tsubaki.LEFT_BROW_ANGLE
        ),
        "right": sparse.rotated_ellipse_mask(
            shape, tsubaki.GEOMETRY.right_brow, tsubaki.RIGHT_BROW_ANGLE
        ),
    }
    eye_exclusion = (
        sparse.ellipse_mask(shape, sparse.EllipseSpec(401, 666, 92, 38))
        | sparse.ellipse_mask(shape, sparse.EllipseSpec(616, 666, 92, 38))
    )
    y_grid = np.indices(shape)[0]
    brow_height_limit = y_grid <= 630
    orientation_kernels = [
        line_kernel(9, angle) for angle in (-32, -24, -16, -8, 0, 8, 16, 24, 32)
    ]
    bridge_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 3))
    seed_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 7))

    panels: list[tuple[str, Image.Image]] = []
    report: dict[str, object] = {
        "schema_version": 1,
        "coordinate_space": "aligned 1024x1536 authoring master",
        "intent": "continuous authored brows over bangs",
        "expressions": {},
    }

    for expression in tsubaki.EXPRESSIONS:
        master_name = tsubaki.MASTER_OVERRIDES.get(
            expression, f"expression_{expression}.png"
        )
        donor_rgb = tsubaki.load_rgb(MASTER_DIR / master_name)
        donor_valid = sparse.checker_foreground(donor_rgb)
        registration, registration_metrics = sparse.estimate_registration(
            donor_rgb, donor_valid, featureless_rgba
        )
        aligned_rgb = sparse.warp_rgb(donor_rgb, registration)
        aligned_valid = sparse.warp_mask(donor_valid, registration)
        normalized_rgb, _ = sparse.normalize_rgb_diagonal(
            aligned_rgb,
            aligned_valid,
            featureless_rgb,
            featureless_valid,
        )
        delta = sparse.maximum_color_delta(normalized_rgb, featureless_rgb)
        dark_ink, _, _, _ = sparse.feature_palette(aligned_rgb)
        gray = cv2.cvtColor(aligned_rgb, cv2.COLOR_RGB2GRAY)
        local_dark_ridge = cv2.morphologyEx(
            gray,
            cv2.MORPH_BLACKHAT,
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 9)),
        )

        raw_layer, _, _ = sparse.build_expression_layer(
            expression,
            featureless_rgba,
            aligned_rgb,
            aligned_valid,
            featureless_rgb,
            featureless_valid,
        )
        raw_support = raw_layer[:, :, 3] >= 8

        expression_mask = np.zeros(shape, dtype=bool)
        side_metrics: dict[str, object] = {}
        for side, roi in brow_rois.items():
            roi = (
                roi
                & aligned_valid
                & featureless_valid
                & ~eye_exclusion
                & brow_height_limit
            )
            trusted_seed = (
                raw_support
                & trusted_brow_rois[side]
                & dark_ink
                & (delta >= 7)
                & brow_height_limit
            )
            curve_band = fitted_curve_band(trusted_seed, roi)
            authored_candidate = (
                roi
                & dark_ink
                & (delta >= 3)
                & (local_dark_ridge >= 5)
                & curve_band
            )

            oriented = np.zeros(shape, dtype=bool)
            candidate_u8 = authored_candidate.astype(np.uint8)
            for kernel in orientation_kernels:
                opened = cv2.morphologyEx(candidate_u8, cv2.MORPH_OPEN, kernel)
                oriented |= opened.astype(bool)
            oriented = cv2.dilate(
                oriented.astype(np.uint8),
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
            ).astype(bool)
            oriented &= authored_candidate

            # Trusted sparse ink anchors the identity of the line.  Limited
            # horizontal closing crosses subpixel/registration gaps without
            # following steep bang contours across the ROI.
            connected = oriented | trusted_seed
            connected = cv2.morphologyEx(
                connected.astype(np.uint8), cv2.MORPH_CLOSE, bridge_kernel
            ).astype(bool)
            anchored = retain_seeded(
                connected,
                cv2.dilate(trusted_seed.astype(np.uint8), seed_kernel).astype(bool),
            )
            anchored &= (authored_candidate | trusted_seed)

            # Prevent an intersecting bang edge from escaping vertically.
            seed_y, seed_x = np.nonzero(trusted_seed)
            if len(seed_x):
                median_y = float(np.median(seed_y))
                anchored &= np.abs(np.indices(shape)[0] - median_y) <= 22.0

            expression_mask |= anchored
            side_metrics[side] = {
                "trusted_seed_pixels": int(trusted_seed.sum()),
                "candidate_pixels": int(authored_candidate.sum()),
                "owned_pixels": int(anchored.sum()),
                "bbox": mask_bbox(anchored),
            }

        rgba = np.zeros((*shape, 4), dtype=np.uint8)
        rgba[expression_mask, :3] = aligned_rgb[expression_mask]
        rgba[expression_mask, 3] = 255
        Image.fromarray(rgba, "RGBA").save(
            OUTPUT_DIR / f"brow_{expression}.png", optimize=True
        )

        crop = Image.fromarray(aligned_rgb, "RGB").crop((300, 525, 715, 660))
        crop_array = np.asarray(crop).copy()
        crop_mask = expression_mask[525:660, 300:715]
        crop_seed = raw_support[525:660, 300:715]
        crop_array[crop_seed] = (
            0.35 * crop_array[crop_seed] + 0.65 * np.asarray([255, 70, 40])
        ).astype(np.uint8)
        crop_array[crop_mask] = (
            0.30 * crop_array[crop_mask] + 0.70 * np.asarray([40, 245, 100])
        ).astype(np.uint8)
        panels.append((expression, Image.fromarray(crop_array, "RGB")))

        report["expressions"][expression] = {
            "master": master_name,
            "registration": {
                "method": registration_metrics.method,
                "scale": registration_metrics.scale,
                "rotation_degrees": registration_metrics.rotation_degrees,
                "translate_x": registration_metrics.translate_x,
                "translate_y": registration_metrics.translate_y,
            },
            "owned_pixels": int(expression_mask.sum()),
            "bbox": mask_bbox(expression_mask),
            "eye_overlap_pixels": int((expression_mask & eye_exclusion).sum()),
            "sides": side_metrics,
        }

    columns = 3
    panel_width, panel_height = 415, 168
    rows = math.ceil(len(panels) / columns)
    sheet = Image.new(
        "RGB", (columns * panel_width, rows * panel_height), (30, 31, 35)
    )
    draw = ImageDraw.Draw(sheet)
    label_font = get_font(18)
    for index, (expression, panel) in enumerate(panels):
        x = (index % columns) * panel_width
        y = (index // columns) * panel_height
        sheet.paste(panel, (x, y))
        draw.rectangle((x, y + 135, x + panel_width, y + panel_height), fill=(30, 31, 35))
        draw.text((x + 8, y + 140), expression, fill=(245, 245, 248), font=label_font)
    sheet.save(OUTPUT_DIR / "brow_ownership_contact.png", optimize=True)
    (OUTPUT_DIR / "metrics.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
