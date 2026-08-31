"""Read-only forensic audit for Tsubaki's 42 shipped expression overlays.

Writes only diagnostic artifacts beside this script. Production art is never
modified. The audit distinguishes transparent holes shown as black by some
viewers from genuinely opaque dark pixels, checks alpha-mask topology and brow
coverage, compares casual/uniform pairs, and renders every expression over its
intended neutral base.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
ASSET_DIR = ROOT / "game" / "assets" / "characters" / "tsubaki"
OUT_DIR = Path(__file__).resolve().parent
BUILD_METRICS = ROOT / "tmp" / "tsubaki_face_patch" / "output" / "metrics.json"

EXPRESSIONS = (
    "afraid",
    "angry",
    "annoyed",
    "crying",
    "curious",
    "determined",
    "disgusted",
    "embarrassed",
    "empty",
    "frustrated",
    "happy",
    "nervous",
    "neut",
    "panicked",
    "sad",
    "shocked",
    "smug",
    "teasing",
    "thinking",
    "unamused",
    "worried",
)
OUTFITS = {
    "casual": "neutral.png",
    "uniform": "neut_uniform.png",
}
OLD_REFERENCES = (
    "neutralold.png",
    "neutralold2.png",
    "neut_uniformold.png",
    "post_neut.png",
    "post_rev.png",
)

# The brow-ownership bboxes are copied from the schema-v2 build metrics at
# runtime, not hard-coded. These broader bands are used only to report whether
# dark authored linework approaches the alpha boundary.
FACE_ROI = (360, 260, 660, 535)
FEATURE_CENTER_ROI = (420, 335, 600, 485)


def load_rgba(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGBA"), dtype=np.uint8)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bbox_from_mask(mask: np.ndarray) -> list[int] | None:
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)]


def connected_components(mask: np.ndarray, min_area: int = 1) -> list[dict[str, Any]]:
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(
        mask.astype(np.uint8), connectivity=8
    )
    rows: list[dict[str, Any]] = []
    for label in range(1, count):
        x, y, w, h, area = (int(value) for value in stats[label])
        if area < min_area:
            continue
        component = (labels == label).astype(np.uint8)
        contours, _ = cv2.findContours(component, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        perimeter = float(sum(cv2.arcLength(contour, True) for contour in contours))
        circularity = float(4.0 * math.pi * area / (perimeter * perimeter)) if perimeter else 0.0
        cx, cy = (float(value) for value in centroids[label])
        rows.append(
            {
                "area": area,
                "bbox": [x, y, x + w, y + h],
                "centroid": [round(cx, 3), round(cy, 3)],
                "circularity": round(circularity, 4),
                "aspect": round(w / h, 4) if h else None,
            }
        )
    return sorted(rows, key=lambda row: row["area"], reverse=True)


def valued_components(mask: np.ndarray, values: np.ndarray) -> list[dict[str, Any]]:
    """Return component geometry plus value range for a scalar image."""

    count, labels, stats, centroids = cv2.connectedComponentsWithStats(
        mask.astype(np.uint8), connectivity=8
    )
    rows: list[dict[str, Any]] = []
    for label in range(1, count):
        x, y, w, h, area = (int(value) for value in stats[label])
        selected = values[labels == label]
        cx, cy = (float(value) for value in centroids[label])
        rows.append(
            {
                "area": area,
                "bbox": [x, y, x + w, y + h],
                "centroid": [round(cx, 3), round(cy, 3)],
                "value_min": int(selected.min()),
                "value_max": int(selected.max()),
                "value_mean": round(float(selected.mean()), 3),
            }
        )
    return sorted(rows, key=lambda row: row["area"], reverse=True)


def enclosed_holes(mask: np.ndarray, roi: tuple[int, int, int, int]) -> list[dict[str, Any]]:
    """Find fully enclosed transparent regions inside an ROI.

    A transparent component touching the ROI edge is ordinary background and
    is excluded. Coordinates are returned in full-canvas space.
    """

    x0, y0, x1, y1 = roi
    transparent = (~mask[y0:y1, x0:x1]).astype(np.uint8)
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(transparent, 8)
    rows: list[dict[str, Any]] = []
    height, width = transparent.shape
    for label in range(1, count):
        x, y, w, h, area = (int(value) for value in stats[label])
        if x == 0 or y == 0 or x + w == width or y + h == height:
            continue
        component = (labels == label).astype(np.uint8)
        contours, _ = cv2.findContours(component, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        perimeter = float(sum(cv2.arcLength(contour, True) for contour in contours))
        circularity = float(4.0 * math.pi * area / (perimeter * perimeter)) if perimeter else 0.0
        cx, cy = (float(value) for value in centroids[label])
        rows.append(
            {
                "area": area,
                "bbox": [x + x0, y + y0, x + x0 + w, y + y0 + h],
                "centroid": [round(cx + x0, 3), round(cy + y0, 3)],
                "circularity": round(circularity, 4),
                "aspect": round(w / h, 4) if h else None,
            }
        )
    return sorted(rows, key=lambda row: row["area"], reverse=True)


def round_components(
    rows: list[dict[str, Any]],
    roi: tuple[int, int, int, int],
    *,
    min_area: int = 8,
) -> list[dict[str, Any]]:
    x0, y0, x1, y1 = roi
    result = []
    for row in rows:
        cx, cy = row["centroid"]
        aspect = row["aspect"] or 0.0
        if (
            row["area"] >= min_area
            and x0 <= cx < x1
            and y0 <= cy < y1
            and 0.70 <= aspect <= 1.30
            and row["circularity"] >= 0.62
        ):
            result.append(row)
    return result


def best_mask_alignment(a: np.ndarray, b: np.ndarray, radius: int = 10) -> dict[str, Any]:
    """Find the small translation of b that maximizes alpha-mask IoU with a."""

    best = {"dx": 0, "dy": 0, "iou": -1.0, "intersection": 0, "union": 0}
    h, w = a.shape
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            shifted = np.zeros_like(b)
            sx0 = max(0, -dx)
            sy0 = max(0, -dy)
            sx1 = min(w, w - dx)
            sy1 = min(h, h - dy)
            dx0 = sx0 + dx
            dy0 = sy0 + dy
            dx1 = sx1 + dx
            dy1 = sy1 + dy
            if sx1 <= sx0 or sy1 <= sy0:
                continue
            shifted[dy0:dy1, dx0:dx1] = b[sy0:sy1, sx0:sx1]
            intersection = int(np.count_nonzero(a & shifted))
            union = int(np.count_nonzero(a | shifted))
            iou = intersection / union if union else 1.0
            if iou > best["iou"]:
                best = {
                    "dx": dx,
                    "dy": dy,
                    "iou": round(float(iou), 6),
                    "intersection": intersection,
                    "union": union,
                }
    return best


def alpha_composite(base: np.ndarray, layer: np.ndarray) -> np.ndarray:
    return np.asarray(
        Image.alpha_composite(Image.fromarray(base, "RGBA"), Image.fromarray(layer, "RGBA")),
        dtype=np.uint8,
    )


def checkerboard(size: tuple[int, int], tile: int = 18) -> Image.Image:
    width, height = size
    yy, xx = np.indices((height, width))
    cells = ((xx // tile + yy // tile) % 2).astype(np.uint8)
    colors = np.where(cells[..., None] == 0, 238, 202).astype(np.uint8)
    rgb = np.repeat(colors, 3, axis=2)
    alpha = np.full((height, width, 1), 255, dtype=np.uint8)
    return Image.fromarray(np.concatenate([rgb, alpha], axis=2), "RGBA")


def flatten_over(image: Image.Image, background: Image.Image | tuple[int, int, int, int]) -> Image.Image:
    if isinstance(background, tuple):
        background = Image.new("RGBA", image.size, background)
    return Image.alpha_composite(background, image)


def draw_contact_sheet(
    composites: dict[tuple[str, str], Image.Image],
    layers: dict[tuple[str, str], Image.Image],
) -> None:
    crop = (330, 230, 690, 550)
    cell_w, cell_h = 270, 270
    label_h = 24
    rows = 7
    cols = 6
    font = ImageFont.load_default()

    for mode in ("composite_light", "layer_checker"):
        sheet = Image.new("RGB", (cols * cell_w, rows * (cell_h + label_h)), "white")
        draw = ImageDraw.Draw(sheet)
        for index, expression in enumerate(EXPRESSIONS):
            group_row, group_col = divmod(index, 3)
            for outfit_offset, outfit in enumerate(("casual", "uniform")):
                col = group_col * 2 + outfit_offset
                x = col * cell_w
                y = group_row * (cell_h + label_h)
                source = composites[(expression, outfit)] if mode == "composite_light" else layers[(expression, outfit)]
                head = source.crop(crop).resize((cell_w, cell_h), Image.Resampling.LANCZOS)
                if mode == "composite_light":
                    tile = flatten_over(head, (245, 245, 245, 255)).convert("RGB")
                else:
                    tile = flatten_over(head, checkerboard(head.size, 14)).convert("RGB")
                sheet.paste(tile, (x, y + label_h))
                draw.text((x + 5, y + 6), f"{expression} / {outfit}", fill="black", font=font)
        sheet.save(OUT_DIR / f"all_42_{mode}.png", optimize=True)


def draw_alpha_topology_sheet(layers: dict[tuple[str, str], Image.Image]) -> None:
    crop = (330, 230, 690, 550)
    cell_w, cell_h = 270, 270
    label_h = 24
    rows, cols = 7, 6
    sheet = Image.new("RGB", (cols * cell_w, rows * (cell_h + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for index, expression in enumerate(EXPRESSIONS):
        group_row, group_col = divmod(index, 3)
        for outfit_offset, outfit in enumerate(("casual", "uniform")):
            col = group_col * 2 + outfit_offset
            x = col * cell_w
            y = group_row * (cell_h + label_h)
            rgba = np.asarray(layers[(expression, outfit)], dtype=np.uint8)
            alpha = rgba[..., 3]
            rgb = np.zeros((*alpha.shape, 3), dtype=np.uint8)
            rgb[..., 0] = np.where(alpha == 0, 25, np.where(alpha == 255, 80, 235))
            rgb[..., 1] = np.where(alpha == 0, 25, np.where(alpha == 255, 190, 175))
            rgb[..., 2] = np.where(alpha == 0, 25, np.where(alpha == 255, 255, 35))
            topology = Image.fromarray(rgb, "RGB").crop(crop).resize((cell_w, cell_h), Image.Resampling.NEAREST)
            sheet.paste(topology, (x, y + label_h))
            draw.text((x + 5, y + 6), f"{expression} / {outfit}", fill="black", font=font)
    sheet.save(OUT_DIR / "all_42_alpha_topology.png", optimize=True)


def main() -> None:
    build = json.loads(BUILD_METRICS.read_text(encoding="utf-8"))
    bases = {outfit: load_rgba(ASSET_DIR / filename) for outfit, filename in OUTFITS.items()}
    layer_images: dict[tuple[str, str], Image.Image] = {}
    composite_images: dict[tuple[str, str], Image.Image] = {}
    records: list[dict[str, Any]] = []

    for outfit in OUTFITS:
        guard = build["outfits"][outfit]["base_neutral_guard"]
        gx0, gy0, gx1, gy1 = guard["bbox"]
        # Expand slightly so edge-contact reporting includes tapered line ends.
        brow_band = (gx0 - 8, gy0 - 8, gx1 + 8, gy1 + 8)
        for expression in EXPRESSIONS:
            path = ASSET_DIR / f"face_{expression}_{outfit}.png"
            rgba = load_rgba(path)
            layer_image = Image.fromarray(rgba, "RGBA")
            composite = alpha_composite(bases[outfit], rgba)
            composite_image = Image.fromarray(composite, "RGBA")
            layer_images[(expression, outfit)] = layer_image
            composite_images[(expression, outfit)] = composite_image

            rgb = rgba[..., :3]
            alpha = rgba[..., 3]
            visible = alpha > 0
            solid = alpha == 255
            partial = visible & ~solid
            partial_components = valued_components(partial, alpha)
            hidden_rgb = (~visible) & np.any(rgb != 0, axis=2)
            opaque_black = solid & (np.max(rgb, axis=2) <= 5)
            opaque_near_black = solid & (np.max(rgb, axis=2) <= 24)
            alpha_components = connected_components(visible)
            holes = enclosed_holes(visible, FACE_ROI)
            black_components = connected_components(opaque_near_black, min_area=2)
            round_black = round_components(black_components, FEATURE_CENTER_ROI)

            # Dark linework approaching the alpha edge within the metric-derived
            # brow band. A nonzero value is not automatically a defect (bangs
            # intentionally occlude brows), but exposes any suspicious contact.
            luma = (
                0.2126 * rgb[..., 0].astype(np.float32)
                + 0.7152 * rgb[..., 1].astype(np.float32)
                + 0.0722 * rgb[..., 2].astype(np.float32)
            )
            distance = cv2.distanceTransform(visible.astype(np.uint8), cv2.DIST_L2, 3)
            brow_mask = np.zeros_like(visible)
            bx0, by0, bx1, by1 = brow_band
            brow_mask[by0:by1, bx0:bx1] = True
            dark_brow = visible & brow_mask & (luma < 115)
            dark_brow_edge = dark_brow & (distance <= 2.0)

            base = bases[outfit]
            changed = np.any(composite[..., :3] != base[..., :3], axis=2)
            comp_near_black = np.max(composite[..., :3], axis=2) <= 24
            base_near_black = np.max(base[..., :3], axis=2) <= 24
            introduced_near_black = changed & comp_near_black & ~base_near_black
            introduced_components = connected_components(introduced_near_black, min_area=2)
            introduced_round = round_components(introduced_components, FEATURE_CENTER_ROI)

            records.append(
                {
                    "expression": expression,
                    "outfit": outfit,
                    "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "sha256": sha256(path),
                    "size": [int(rgba.shape[1]), int(rgba.shape[0])],
                    "alpha_bbox": bbox_from_mask(visible),
                    "visible_pixels": int(np.count_nonzero(visible)),
                    "opaque_pixels": int(np.count_nonzero(solid)),
                    "partial_pixels": int(np.count_nonzero(partial)),
                    "partial_alpha_components": partial_components,
                    "hidden_rgb_pixels": int(np.count_nonzero(hidden_rgb)),
                    "alpha_component_count": len(alpha_components),
                    "alpha_components": alpha_components[:12],
                    "enclosed_transparent_holes": holes,
                    "opaque_black_pixels": int(np.count_nonzero(opaque_black)),
                    "opaque_near_black_pixels": int(np.count_nonzero(opaque_near_black)),
                    "opaque_near_black_components": black_components[:30],
                    "round_opaque_near_black_center_components": round_black,
                    "brow_guard_bbox_from_build": guard["bbox"],
                    "brow_guard_footprint_pixels_from_build": guard["guard_footprint_pixels"],
                    "brow_guard_unowned_pixels_from_build": guard["unowned_guard_pixels"],
                    "dark_brow_band_pixels": int(np.count_nonzero(dark_brow)),
                    "dark_brow_band_pixels_within_2px_of_alpha_edge": int(np.count_nonzero(dark_brow_edge)),
                    "composite_changed_pixels": int(np.count_nonzero(changed)),
                    "composite_introduced_near_black_pixels": int(np.count_nonzero(introduced_near_black)),
                    "composite_round_introduced_near_black_center_components": introduced_round,
                }
            )

    by_key = {(row["expression"], row["outfit"]): row for row in records}
    pair_rows = []
    for expression in EXPRESSIONS:
        casual = load_rgba(ASSET_DIR / f"face_{expression}_casual.png")
        uniform = load_rgba(ASSET_DIR / f"face_{expression}_uniform.png")
        casual_mask = casual[..., 3] > 0
        uniform_mask = uniform[..., 3] > 0
        align = best_mask_alignment(casual_mask, uniform_mask)
        pair_rows.append(
            {
                "expression": expression,
                "casual_visible_pixels": by_key[(expression, "casual")]["visible_pixels"],
                "uniform_visible_pixels": by_key[(expression, "uniform")]["visible_pixels"],
                "visible_pixel_delta": by_key[(expression, "casual")]["visible_pixels"]
                - by_key[(expression, "uniform")]["visible_pixels"],
                "best_uniform_to_casual_mask_alignment": align,
            }
        )

    per_outfit = {}
    for outfit in OUTFITS:
        outfit_records = [row for row in records if row["outfit"] == outfit]
        mask_hashes: dict[str, list[str]] = {}
        for expression in EXPRESSIONS:
            alpha = load_rgba(ASSET_DIR / f"face_{expression}_{outfit}.png")[..., 3]
            digest = hashlib.sha256(alpha.tobytes()).hexdigest()
            mask_hashes.setdefault(digest, []).append(expression)
        per_outfit[outfit] = {
            "alpha_mask_groups": list(mask_hashes.values()),
            "any_hidden_rgb": any(row["hidden_rgb_pixels"] for row in outfit_records),
            "files_with_enclosed_alpha_holes": [
                row["expression"] for row in outfit_records if row["enclosed_transparent_holes"]
            ],
            "files_with_round_opaque_near_black_center_components": [
                row["expression"]
                for row in outfit_records
                if row["round_opaque_near_black_center_components"]
            ],
            "files_with_round_introduced_near_black_center_components": [
                row["expression"]
                for row in outfit_records
                if row["composite_round_introduced_near_black_center_components"]
            ],
            "max_dark_brow_edge_pixels": max(
                (row["dark_brow_band_pixels_within_2px_of_alpha_edge"] for row in outfit_records),
                default=0,
            ),
        }

    references = []
    for filename in (*OUTFITS.values(), *OLD_REFERENCES):
        path = ASSET_DIR / filename
        rgba = load_rgba(path)
        references.append(
            {
                "filename": filename,
                "sha256": sha256(path),
                "size": [int(rgba.shape[1]), int(rgba.shape[0])],
                "alpha_bbox": bbox_from_mask(rgba[..., 3] > 0),
                "visible_pixels": int(np.count_nonzero(rgba[..., 3] > 0)),
                "hidden_rgb_pixels": int(
                    np.count_nonzero((rgba[..., 3] == 0) & np.any(rgba[..., :3] != 0, axis=2))
                ),
            }
        )

    report = {
        "schema": 1,
        "asset_dir": str(ASSET_DIR),
        "record_count": len(records),
        "build_metrics_schema": build["schema_version"],
        "build_brow_guard": {
            outfit: build["outfits"][outfit]["base_neutral_guard"] for outfit in OUTFITS
        },
        "per_outfit_summary": per_outfit,
        "pairs": pair_rows,
        "layers": records,
        "bases_and_old_references": references,
    }
    (OUT_DIR / "forensics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "Tsubaki expression-layer forensics",
        f"Audited layers: {len(records)}",
        "",
    ]
    for outfit in OUTFITS:
        summary = per_outfit[outfit]
        guard = report["build_brow_guard"][outfit]
        lines.extend(
            [
                f"[{outfit}]",
                f"alpha mask groups: {summary['alpha_mask_groups']}",
                f"hidden RGB present: {summary['any_hidden_rgb']}",
                f"enclosed transparent holes: {summary['files_with_enclosed_alpha_holes']}",
                "round opaque near-black center components: "
                f"{summary['files_with_round_opaque_near_black_center_components']}",
                "round near-black center components introduced after composite: "
                f"{summary['files_with_round_introduced_near_black_center_components']}",
                f"build brow guard bbox: {guard['bbox']}",
                f"build brow guard footprint/unowned: {guard['guard_footprint_pixels']}/{guard['unowned_guard_pixels']}",
                f"max dark brow pixels within 2px of alpha edge: {summary['max_dark_brow_edge_pixels']}",
                "",
            ]
        )
    lines.append("casual/uniform mask alignment by expression:")
    for row in pair_rows:
        align = row["best_uniform_to_casual_mask_alignment"]
        lines.append(
            f"  {row['expression']}: delta={row['visible_pixel_delta']}, "
            f"shift=({align['dx']},{align['dy']}), IoU={align['iou']}"
        )
    (OUT_DIR / "forensics_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    draw_contact_sheet(composite_images, layer_images)
    draw_alpha_topology_sheet(layer_images)


if __name__ == "__main__":
    main()
