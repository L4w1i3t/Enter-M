"""Stage and visualize full-master brow extraction across Tsubaki's bangs."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import process_sam_sprites as sparse  # noqa: E402
import process_tsubaki_face_patches as face  # noqa: E402
import process_tsubaki_sprites as tsubaki  # noqa: E402


OUT = ROOT / "tmp" / "tsubaki_brow_prototype_agent" / "full_brow_analysis"
REPORTED = ("worried", "unamused", "disgusted")
RAW_CROP = (300, 530, 710, 655)


def font(size: int) -> ImageFont.ImageFont:
    candidate = Path("C:/Windows/Fonts/arial.ttf")
    return ImageFont.truetype(str(candidate), size) if candidate.is_file() else ImageFont.load_default()


def fit_curve(seed: np.ndarray, center_x: float) -> tuple[np.ndarray, dict[str, object]]:
    ys, xs = np.nonzero(seed)
    if len(xs) < 12:
        raise RuntimeError(f"insufficient brow seeds near x={center_x}: {len(xs)}")
    unique_x = np.unique(xs)
    med_x: list[float] = []
    med_y: list[float] = []
    for x in unique_x:
        values = ys[xs == x]
        if len(values):
            med_x.append(float(x))
            med_y.append(float(np.median(values)))
    x_values = np.asarray(med_x, dtype=np.float64)
    y_values = np.asarray(med_y, dtype=np.float64)
    keep = np.ones(len(x_values), dtype=bool)
    coefficients = np.polyfit(x_values, y_values, deg=2)
    for _ in range(4):
        predicted = np.polyval(coefficients, x_values)
        residual = np.abs(y_values - predicted)
        median = float(np.median(residual[keep])) if np.any(keep) else 0.0
        threshold = max(2.5, 2.5 * median)
        new_keep = residual <= threshold
        if int(new_keep.sum()) < 8:
            break
        keep = new_keep
        coefficients = np.polyfit(x_values[keep], y_values[keep], deg=2)
    residual = np.abs(y_values - np.polyval(coefficients, x_values))
    return coefficients, {
        "seed_pixels": int(seed.sum()),
        "seed_columns": int(len(unique_x)),
        "fit_columns": int(keep.sum()),
        "coefficients": [round(float(value), 8) for value in coefficients],
        "median_residual": round(float(np.median(residual[keep])), 4),
        "maximum_fit_residual": round(float(residual[keep].max()), 4),
        "x_extent": [int(x_values[keep].min()), int(x_values[keep].max())],
    }


def extract_brows(
    expression: str,
    aligned_rgb: np.ndarray,
    aligned_valid: np.ndarray,
    blank_rgb: np.ndarray,
    raw_sparse: np.ndarray,
) -> tuple[np.ndarray, list[dict[str, object]], np.ndarray]:
    normalized, _ = sparse.normalize_rgb_diagonal(
        aligned_rgb, aligned_valid, blank_rgb, sparse.checker_foreground(blank_rgb)
    )
    delta = sparse.maximum_color_delta(normalized, blank_rgb)
    expression_gray = cv2.cvtColor(normalized, cv2.COLOR_RGB2GRAY).astype(np.int16)
    blank_gray = cv2.cvtColor(blank_rgb, cv2.COLOR_RGB2GRAY).astype(np.int16)
    darkening = blank_gray - expression_gray
    yy, xx = np.indices(delta.shape)
    extracted = np.zeros(delta.shape, dtype=bool)
    corridor_union = np.zeros(delta.shape, dtype=bool)
    metrics: list[dict[str, object]] = []
    brow_specs = (
        ("viewer-left", tsubaki.GEOMETRY.left_brow),
        ("viewer-right", tsubaki.GEOMETRY.right_brow),
    )
    for side, spec in brow_specs:
        broad = sparse.rotated_ellipse_mask(
            delta.shape,
            sparse.EllipseSpec(spec.center_x, spec.center_y, 92, 42),
            0.0,
        )
        broad &= yy <= 623
        seed = (
            (raw_sparse[:, :, 3] >= face.DETAIL_ALPHA_MINIMUM)
            & broad
            & (expression_gray <= 205)
            & (darkening >= 5)
        )
        coefficients, fit_metrics = fit_curve(seed, spec.center_x)
        curve_y = np.polyval(coefficients, xx.astype(np.float64))
        corridor = broad & (np.abs(yy - curve_y) <= 5.25)
        corridor_union |= corridor
        core = (
            corridor
            & aligned_valid
            & (delta >= 7)
            & (expression_gray <= 205)
            & (darkening >= 3)
        )
        # Preserve the already-reviewed exposed segments, then admit only
        # nearby full-master ink inside the fitted horizontal brow corridor.
        core |= seed
        support = cv2.morphologyEx(
            core.astype(np.uint8),
            cv2.MORPH_CLOSE,
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 3)),
        ).astype(bool)
        relaxed = (
            corridor
            & aligned_valid
            & (delta >= 4)
            & (expression_gray <= 218)
            & (darkening >= 1)
        )
        support |= cv2.dilate(
            support.astype(np.uint8),
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
        ).astype(bool) & relaxed
        # Do not retain detached hair-registration noise: every final
        # component must touch a reviewed skin-visible seed.
        support = sparse.retain_seeded_components(support, seed, minimum_area=2)
        extracted |= support
        metrics.append(
            {
                "side": side,
                **fit_metrics,
                "candidate_pixels": int(core.sum()),
                "support_pixels": int(support.sum()),
                "support_over_featureless_hair": int(
                    (support & ~tsubaki.featureless_face_interior(
                        blank_rgb, sparse.checker_foreground(blank_rgb)
                    )).sum()
                ),
                "bbox": list(face.mask_bbox(support) or ()),
            }
        )
    return extracted, metrics, corridor_union


def diagnostic_panel(
    expression: str,
    aligned_rgb: np.ndarray,
    raw_sparse: np.ndarray,
    full_brow: np.ndarray,
    corridor: np.ndarray,
) -> Image.Image:
    left, top, right, bottom = RAW_CROP
    master = Image.fromarray(aligned_rgb, "RGB").crop(RAW_CROP).resize(
        ((right - left) * 2, (bottom - top) * 2), Image.Resampling.NEAREST
    )
    overlay = aligned_rgb.copy()
    seed = raw_sparse[:, :, 3] >= face.DETAIL_ALPHA_MINIMUM
    overlay[corridor] = np.clip(
        np.rint(0.75 * overlay[corridor] + 0.25 * np.asarray((45, 105, 255))),
        0,
        255,
    ).astype(np.uint8)
    overlay[seed] = (48, 235, 105)
    overlay[full_brow] = (246, 54, 72)
    marked = Image.fromarray(overlay, "RGB").crop(RAW_CROP).resize(
        ((right - left) * 2, (bottom - top) * 2), Image.Resampling.NEAREST
    )
    panel = Image.new("RGB", (master.width * 2, master.height + 34), (24, 27, 31))
    panel.paste(master, (0, 0))
    panel.paste(marked, (master.width, 0))
    draw = ImageDraw.Draw(panel)
    draw.text((8, master.height + 6), f"{expression}: master | red=full brow, green=sparse seed, blue=corridor", font=font(18), fill=(240, 242, 246))
    return panel


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    tsubaki.configure_sparse_processor()
    blank_rgb = face.load_rgb(face.DEFAULT_MASTER_DIR / "head_raw.png", face.SOURCE_SIZE)
    blank_valid = sparse.checker_foreground(blank_rgb)
    blank_rgba = np.dstack((blank_rgb, blank_valid.astype(np.uint8) * 255))
    source_metrics = json.loads(
        (face.DEFAULT_SOURCE_DIR / "metrics.json").read_text(encoding="utf-8")
    )
    expressions: dict[str, object] = {}
    panels: list[Image.Image] = []
    for expression in face.EXPRESSIONS[1:]:
        filename = face.MASTER_OVERRIDES.get(expression, f"expression_{expression}.png")
        donor_rgb = face.load_rgb(face.DEFAULT_MASTER_DIR / filename, face.SOURCE_SIZE)
        donor_valid = sparse.checker_foreground(donor_rgb)
        registration = face.registration_matrix(
            source_metrics["layers"][expression]["registration"]
        )
        aligned_rgb = sparse.warp_rgb(donor_rgb, registration)
        aligned_valid = sparse.warp_mask(donor_valid, registration)
        raw_sparse, _, _ = sparse.build_expression_layer(
            expression,
            blank_rgba,
            aligned_rgb,
            aligned_valid,
            blank_rgb,
            blank_valid,
        )
        full_brow, brow_metrics, corridor = extract_brows(
            expression, aligned_rgb, aligned_valid, blank_rgb, raw_sparse
        )
        rgba = np.zeros((face.SOURCE_SIZE[1], face.SOURCE_SIZE[0], 4), dtype=np.uint8)
        rgba[full_brow, :3] = aligned_rgb[full_brow, :3]
        rgba[full_brow, 3] = 255
        face.save_rgba(OUT / f"full_brow_{expression}.png", rgba)
        expressions[expression] = {
            "registration": registration.astype(float).tolist(),
            "sides": brow_metrics,
            "pixels": int(full_brow.sum()),
            "bbox": list(face.mask_bbox(full_brow) or ()),
        }
        if expression in REPORTED:
            panels.append(
                diagnostic_panel(expression, aligned_rgb, raw_sparse, full_brow, corridor)
            )
    if panels:
        sheet = Image.new(
            "RGB",
            (max(panel.width for panel in panels), sum(panel.height for panel in panels)),
            (24, 27, 31),
        )
        y = 0
        for panel in panels:
            sheet.paste(panel, (0, y))
            y += panel.height
        sheet.save(OUT / "reported_extraction_diagnostics.png", optimize=True)
    (OUT / "metrics.json").write_text(
        json.dumps({"expressions": expressions}, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Full-brow analysis: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
