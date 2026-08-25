#!/usr/bin/env python3
"""Matte and place one generated full-canvas sprite-part donor.

The image generator may re-center an isolated head, body, arm, or prop even
when the prompt requests production coordinates.  This review-stage tool first
extracts the opaque checker matte, then applies one measured uniform scale and
translation into the shared 1024x1536 production canvas.  It never installs
files into ``game/`` on its own.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

import numpy as np
from PIL import Image

import process_sam_poses as checker_processor
from process_sprite_reference import (
    clear_unprotected_pale_islands,
    parse_rectangle,
    save_rgba,
    warp_rgba_to_canvas,
    write_json,
)


PRODUCTION_CANVAS_SIZE = (1024, 1536)


def parse_point(raw: str) -> tuple[float, float]:
    try:
        x_coordinate, y_coordinate = (float(value) for value in raw.split(","))
    except (TypeError, ValueError) as error:
        raise argparse.ArgumentTypeError("point must be X,Y") from error
    return x_coordinate, y_coordinate


def parse_ellipse(raw: str) -> tuple[float, float, float, float]:
    try:
        center_x, center_y, radius_x, radius_y = (
            float(value) for value in raw.split(",")
        )
    except (TypeError, ValueError) as error:
        raise argparse.ArgumentTypeError("ellipse must be CENTER_X,CENTER_Y,RX,RY") from error
    if radius_x <= 0 or radius_y <= 0:
        raise argparse.ArgumentTypeError("ellipse radii must be positive")
    return center_x, center_y, radius_x, radius_y


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--scale", type=float, required=True)
    parser.add_argument("--source-anchor", type=parse_point, required=True)
    parser.add_argument("--target-anchor", type=parse_point, required=True)
    parser.add_argument("--feather-radius", type=float, default=1.35)
    parser.add_argument("--checker-tolerance", type=float, default=17.0)
    parser.add_argument(
        "--clear-unprotected-pale-islands",
        action="store_true",
        help="Remove residual near-white checker islands after matte extraction.",
    )
    parser.add_argument(
        "--preserve-pale-rect",
        action="append",
        default=[],
        type=parse_rectangle,
        metavar="LEFT,TOP,RIGHT,BOTTOM",
    )
    parser.add_argument(
        "--clear-source-ellipse",
        action="append",
        default=[],
        type=parse_ellipse,
        metavar="CENTER_X,CENTER_Y,RX,RY",
        help="Source-space region to make transparent before placement; repeatable.",
    )
    return parser


def run(args: argparse.Namespace) -> int:
    if not args.input.is_file():
        raise ValueError(f"input does not exist: {args.input}")
    if args.scale <= 0:
        raise ValueError("--scale must be positive")
    if args.feather_radius <= 0 or args.checker_tolerance <= 0:
        raise ValueError("matte parameters must be positive")

    with Image.open(args.input) as source_image:
        source_width, source_height = source_image.size
        source_rgb = np.asarray(source_image.convert("RGB"), dtype=np.uint8)
    checker_processor.CANVAS_WIDTH = source_width
    checker_processor.CANVAS_HEIGHT = source_height
    checker_processor.CANVAS_SIZE = (source_width, source_height)
    matte = checker_processor.extract_checker_matte(
        args.input,
        feather_radius=args.feather_radius,
        palette_tolerance=args.checker_tolerance,
    )

    pale_cleanup_metrics: dict[str, Any] | None = None
    if args.clear_unprotected_pale_islands:
        hard_foreground, pale_cleanup_metrics = clear_unprotected_pale_islands(
            source_rgb,
            matte.hard_foreground,
            args.preserve_pale_rect,
        )
        cleaned_rgba, cleanup_alpha_metrics = (
            checker_processor.soften_and_decontaminate(
                source_rgb,
                hard_foreground,
                args.feather_radius,
            )
        )
        matte = checker_processor.MatteResult(
            rgba=cleaned_rgba,
            hard_foreground=hard_foreground,
            metrics={
                **matte.metrics,
                "part_pale_cleanup": pale_cleanup_metrics,
                "part_pale_cleanup_alpha": cleanup_alpha_metrics,
            },
        )

    if args.clear_source_ellipse:
        hard_foreground = matte.hard_foreground.copy()
        y_grid, x_grid = np.ogrid[:source_height, :source_width]
        for center_x, center_y, radius_x, radius_y in args.clear_source_ellipse:
            ellipse = (
                ((x_grid - center_x) / radius_x) ** 2
                + ((y_grid - center_y) / radius_y) ** 2
                <= 1.0
            )
            hard_foreground[ellipse] = False
        cleaned_rgba, cleanup_alpha_metrics = (
            checker_processor.soften_and_decontaminate(
                source_rgb,
                hard_foreground,
                args.feather_radius,
            )
        )
        matte = checker_processor.MatteResult(
            rgba=cleaned_rgba,
            hard_foreground=hard_foreground,
            metrics={
                **matte.metrics,
                "cleared_source_ellipses": [
                    list(ellipse) for ellipse in args.clear_source_ellipse
                ],
                "source_ellipse_cleanup_alpha": cleanup_alpha_metrics,
            },
        )

    source_anchor_x, source_anchor_y = args.source_anchor
    target_anchor_x, target_anchor_y = args.target_anchor
    translate_x = target_anchor_x - args.scale * source_anchor_x
    translate_y = target_anchor_y - args.scale * source_anchor_y
    placed = warp_rgba_to_canvas(
        matte.rgba,
        scale=args.scale,
        translate_x=translate_x,
        translate_y=translate_y,
        canvas_size=PRODUCTION_CANVAS_SIZE,
    )
    alpha = placed[:, :, 3]
    placed_bbox = checker_processor.mask_bbox(alpha >= 128)
    transparent = alpha == 0
    hidden_rgb_values = int(np.count_nonzero(placed[:, :, :3][transparent]))
    report: dict[str, Any] = {
        "schema_version": 1,
        "input": str(args.input.resolve()),
        "source_canvas": [source_width, source_height],
        "target_canvas": list(PRODUCTION_CANVAS_SIZE),
        "scale": args.scale,
        "source_anchor": list(args.source_anchor),
        "target_anchor": list(args.target_anchor),
        "translate_x": round(translate_x, 8),
        "translate_y": round(translate_y, 8),
        "placed_foreground_bbox": placed_bbox.as_list(),
        "hidden_rgb_values_under_zero_alpha": hidden_rgb_values,
        "matte": matte.metrics,
        "output": str(args.output.resolve()),
    }
    save_rgba(args.output, placed)
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
