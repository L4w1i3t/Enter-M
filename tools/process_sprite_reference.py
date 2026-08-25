#!/usr/bin/env python3
"""Matte and calibrate a generated full-body sprite reference.

Generated reference renders are opaque RGB files on a light checker.  This
tool reuses the project's reviewed checker extractor, measures the foreground,
and optionally maps a manually measured skull crown and shoe sole onto the
shared 1024x2816 reference canvas.  It writes only to the requested output and
metadata paths; installation into ``game/`` remains a separate reviewed step.

Examples::

    python tools/process_sprite_reference.py donor.png --analyze-only

    python tools/process_sprite_reference.py donor.png \
        --source-crown-row 170 --source-sole-row 1840 \
        --output tmp/tsubaki_sprite_masters/reference_uniform_fullbody.png \
        --metadata tmp/tsubaki_sprite_masters/reference_uniform_fullbody.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

import cv2
import numpy as np
from PIL import Image

import process_sam_poses as checker_processor


REFERENCE_CANVAS_SIZE = (1024, 2816)
PRODUCTION_CANVAS_HEIGHT = 1536
DEFAULT_TARGET_CROWN_ROW = 380
DEFAULT_TARGET_SOLE_ROW = 2812
DEFAULT_TARGET_ANCHOR_X = 512.0


def parse_rectangle(raw: str) -> tuple[int, int, int, int]:
    """Parse an exclusive-right/exclusive-bottom rectangle."""

    try:
        left, top, right, bottom = (int(value) for value in raw.split(","))
    except (TypeError, ValueError) as error:
        raise argparse.ArgumentTypeError(
            "rectangle must be LEFT,TOP,RIGHT,BOTTOM"
        ) from error
    if left < 0 or top < 0 or right <= left or bottom <= top:
        raise argparse.ArgumentTypeError(
            "rectangle coordinates must be non-negative with right>left and bottom>top"
        )
    return left, top, right, bottom


def configure_checker_processor(width: int, height: int) -> None:
    """Set the reviewed extractor's canvas contract for this donor."""

    checker_processor.CANVAS_WIDTH = width
    checker_processor.CANVAS_HEIGHT = height
    checker_processor.CANVAS_SIZE = (width, height)


def warp_rgba_to_canvas(
    rgba: np.ndarray,
    scale: float,
    translate_x: float,
    translate_y: float,
    canvas_size: tuple[int, int],
) -> np.ndarray:
    """Affine-warp RGBA through premultiplied color to avoid matte halos."""

    source = rgba.astype(np.float32) / 255.0
    alpha = source[:, :, 3:4]
    premultiplied = np.concatenate((source[:, :, :3] * alpha, alpha), axis=2)
    matrix = np.asarray(
        [[scale, 0.0, translate_x], [0.0, scale, translate_y]],
        dtype=np.float32,
    )
    canvas_width, canvas_height = canvas_size
    warped = cv2.warpAffine(
        premultiplied,
        matrix,
        (canvas_width, canvas_height),
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0.0, 0.0, 0.0, 0.0),
    )
    warped_alpha = np.clip(warped[:, :, 3:4], 0.0, 1.0)
    straight_rgb = np.zeros_like(warped[:, :, :3])
    np.divide(
        warped[:, :, :3],
        warped_alpha,
        out=straight_rgb,
        where=warped_alpha > (1.0 / 255.0),
    )
    straight_rgb = np.clip(straight_rgb, 0.0, 1.0)
    output = np.concatenate((straight_rgb, warped_alpha), axis=2)
    result = np.rint(output * 255.0).astype(np.uint8)
    result[result[:, :, 3] == 0, :3] = 0
    return result


def save_rgba(path: Path, rgba: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(path, optimize=True)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def clear_unprotected_pale_islands(
    rgb: np.ndarray,
    hard_foreground: np.ndarray,
    preserve_rectangles: Sequence[tuple[int, int, int, int]],
) -> tuple[np.ndarray, dict[str, Any]]:
    """Remove residual checker islands while protecting real pale artwork.

    Checker phases inside enclosed negative spaces are sometimes regenerated
    independently.  Those pixels remain near-neutral and near-white, whereas
    the real pale regions that matter (eyes, shirt, cuffs, accessories) can be
    named explicitly as probes.  Cleanup is opt-in and therefore cannot change
    the existing production-pose behavior.
    """

    maximum = rgb.max(axis=2).astype(np.int16)
    minimum = rgb.min(axis=2).astype(np.int16)
    chroma = maximum - minimum
    candidate = hard_foreground & (minimum >= 220) & (chroma <= 25)
    component_count, labels, stats, _ = cv2.connectedComponentsWithStats(
        candidate.astype(np.uint8), connectivity=8
    )
    preserve_mask = np.zeros(candidate.shape, dtype=bool)
    height, width = candidate.shape
    for left, top, right, bottom in preserve_rectangles:
        if right > width or bottom > height:
            raise ValueError(
                "preserve rectangle exceeds source canvas: "
                f"{left},{top},{right},{bottom} vs {width}x{height}"
            )
        preserve_mask[top:bottom, left:right] = True

    cleaned_foreground = hard_foreground.copy()
    removed_components: list[dict[str, Any]] = []
    protected_components = 0
    for label in range(1, component_count):
        left = int(stats[label, cv2.CC_STAT_LEFT])
        top = int(stats[label, cv2.CC_STAT_TOP])
        component_width = int(stats[label, cv2.CC_STAT_WIDTH])
        component_height = int(stats[label, cv2.CC_STAT_HEIGHT])
        area = int(stats[label, cv2.CC_STAT_AREA])
        component_slice = np.s_[
            top : top + component_height,
            left : left + component_width,
        ]
        local_component = labels[component_slice] == label
        if np.any(preserve_mask[component_slice] & local_component):
            protected_components += 1
            continue
        local_foreground = cleaned_foreground[component_slice]
        local_foreground[local_component] = False
        removed_components.append(
            {
                "bbox": [
                    left,
                    top,
                    left + component_width,
                    top + component_height,
                ],
                "area": area,
            }
        )

    return cleaned_foreground, {
        "preserve_rectangles": [list(rectangle) for rectangle in preserve_rectangles],
        "removed_component_count": len(removed_components),
        "removed_pixels": sum(component["area"] for component in removed_components),
        "protected_component_count": protected_components,
        "largest_removed_components": sorted(
            removed_components,
            key=lambda component: component["area"],
            reverse=True,
        )[:12],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Opaque checker-backed donor image.")
    parser.add_argument("--output", type=Path, help="Calibrated RGBA reference PNG.")
    parser.add_argument(
        "--production-preview",
        type=Path,
        help="Optional top 1024x1536 crop used to review the shipping frame.",
    )
    parser.add_argument("--metadata", type=Path, help="Optional measurement JSON path.")
    parser.add_argument(
        "--analyze-only",
        action="store_true",
        help="Extract and print measurements without writing calibrated art.",
    )
    parser.add_argument(
        "--source-crown-row",
        type=float,
        help="Measured top of skull in source pixels, excluding hair.",
    )
    parser.add_argument(
        "--source-sole-row",
        type=float,
        help="Measured bottom of shoe in source pixels.",
    )
    parser.add_argument(
        "--target-crown-row", type=float, default=DEFAULT_TARGET_CROWN_ROW
    )
    parser.add_argument(
        "--target-sole-row", type=float, default=DEFAULT_TARGET_SOLE_ROW
    )
    parser.add_argument(
        "--target-anchor-x", type=float, default=DEFAULT_TARGET_ANCHOR_X
    )
    parser.add_argument("--feather-radius", type=float, default=1.35)
    parser.add_argument("--checker-tolerance", type=float, default=17.0)
    parser.add_argument(
        "--clear-unprotected-pale-islands",
        action="store_true",
        help=(
            "Treat remaining enclosed near-white neutral components as matte; "
            "use --preserve-pale-rect for genuine white artwork."
        ),
    )
    parser.add_argument(
        "--preserve-pale-rect",
        action="append",
        default=[],
        type=parse_rectangle,
        metavar="LEFT,TOP,RIGHT,BOTTOM",
        help="Source-space rectangle protecting genuine pale artwork; repeatable.",
    )
    return parser


def validate_arguments(args: argparse.Namespace) -> None:
    if not args.input.is_file():
        raise ValueError(f"input does not exist: {args.input}")
    if args.feather_radius <= 0:
        raise ValueError("--feather-radius must be positive")
    if args.checker_tolerance <= 0:
        raise ValueError("--checker-tolerance must be positive")
    if not args.analyze_only:
        if args.output is None:
            raise ValueError("--output is required unless --analyze-only is used")
        if args.source_crown_row is None or args.source_sole_row is None:
            raise ValueError(
                "--source-crown-row and --source-sole-row are required for calibration"
            )
        if args.source_sole_row <= args.source_crown_row:
            raise ValueError("source sole row must be below source crown row")
        if args.target_sole_row <= args.target_crown_row:
            raise ValueError("target sole row must be below target crown row")


def run(args: argparse.Namespace) -> int:
    validate_arguments(args)
    with Image.open(args.input) as source_image:
        source_width, source_height = source_image.size
    configure_checker_processor(source_width, source_height)
    matte = checker_processor.extract_checker_matte(
        args.input,
        feather_radius=args.feather_radius,
        palette_tolerance=args.checker_tolerance,
        # A full-body reference has safe matte below the shoes.  The production
        # pose processor deliberately excludes this edge because its sprites
        # are cropped at the bottom of the stage canvas.
        include_bottom_edge=True,
        accept_large_enclosed_gaps=True,
    )
    pale_cleanup_metrics: dict[str, Any] | None = None
    if args.clear_unprotected_pale_islands:
        with Image.open(args.input) as source_image:
            source_rgb = np.asarray(source_image.convert("RGB"), dtype=np.uint8)
        cleaned_foreground, pale_cleanup_metrics = clear_unprotected_pale_islands(
            source_rgb,
            matte.hard_foreground,
            args.preserve_pale_rect,
        )
        cleaned_rgba, alpha_metrics = checker_processor.soften_and_decontaminate(
            source_rgb,
            cleaned_foreground,
            args.feather_radius,
        )
        matte = checker_processor.MatteResult(
            rgba=cleaned_rgba,
            hard_foreground=cleaned_foreground,
            metrics={
                **matte.metrics,
                "reference_pale_cleanup": pale_cleanup_metrics,
                "reference_pale_cleanup_alpha": alpha_metrics,
            },
        )
    source_bbox = checker_processor.mask_bbox(matte.hard_foreground)
    source_fullbody_anchor_x = checker_processor.lower_body_anchor_x(
        matte.hard_foreground, source_bbox
    )

    report: dict[str, Any] = {
        "schema_version": 1,
        "input": str(args.input.resolve()),
        "source_canvas": [source_width, source_height],
        "source_foreground_bbox": source_bbox.as_list(),
        "source_fullbody_lower_anchor_x": round(source_fullbody_anchor_x, 4),
        "matte": matte.metrics,
    }
    if args.analyze_only:
        print(json.dumps(report, indent=2))
        return 0

    source_stature = args.source_sole_row - args.source_crown_row
    target_stature = args.target_sole_row - args.target_crown_row
    scale = target_stature / source_stature
    source_production_bottom_row = int(
        round(
            args.source_crown_row
            + (PRODUCTION_CANVAS_HEIGHT - args.target_crown_row) / scale
        )
    )
    source_production_bottom_row = int(
        np.clip(source_production_bottom_row, 1, source_height)
    )
    production_visible_mask = matte.hard_foreground.copy()
    production_visible_mask[source_production_bottom_row:, :] = False
    production_visible_bbox = checker_processor.mask_bbox(production_visible_mask)
    source_production_anchor_x = checker_processor.lower_body_anchor_x(
        production_visible_mask, production_visible_bbox
    )
    translate_x = args.target_anchor_x - scale * source_production_anchor_x
    translate_y = args.target_crown_row - scale * args.source_crown_row
    calibrated = warp_rgba_to_canvas(
        matte.rgba,
        scale=scale,
        translate_x=translate_x,
        translate_y=translate_y,
        canvas_size=REFERENCE_CANVAS_SIZE,
    )
    alpha = calibrated[:, :, 3]
    calibrated_bbox = checker_processor.mask_bbox(alpha >= 128)
    transparent = alpha == 0
    hidden_rgb_values = int(np.count_nonzero(calibrated[:, :, :3][transparent]))
    report.update(
        {
            "target_canvas": list(REFERENCE_CANVAS_SIZE),
            "source_crown_row": args.source_crown_row,
            "source_sole_row": args.source_sole_row,
            "source_production_bottom_row": source_production_bottom_row,
            "source_production_lower_anchor_x": round(
                source_production_anchor_x, 4
            ),
            "target_crown_row": args.target_crown_row,
            "target_sole_row": args.target_sole_row,
            "target_lower_body_anchor_x": args.target_anchor_x,
            "scale": round(scale, 8),
            "translate_x": round(translate_x, 8),
            "translate_y": round(translate_y, 8),
            "calibrated_foreground_bbox": calibrated_bbox.as_list(),
            "hidden_rgb_values_under_zero_alpha": hidden_rgb_values,
            "output": str(args.output.resolve()),
        }
    )
    save_rgba(args.output, calibrated)
    if args.production_preview is not None:
        save_rgba(
            args.production_preview,
            calibrated[:PRODUCTION_CANVAS_HEIGHT, :, :],
        )
        report["production_preview"] = str(args.production_preview.resolve())
    if args.metadata is not None:
        write_json(args.metadata, report)
    print(json.dumps(report, indent=2))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args)
    except (OSError, ValueError, checker_processor.PoseRejected) as error:
        parser.error(str(error))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
