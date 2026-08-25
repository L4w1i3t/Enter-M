"""Normalize the generated Kotonoha boss art into a deterministic sprite sheet.

The image generator supplies a transparent, approximately regular 4x4 layout.
This tool finds the dominant connected sprite in each source tile, removes
detached generation noise, applies one global scale, and anchors every frame to
the same bottom-center point.  The runtime can therefore crop cells without
frame jitter or neighboring-frame bleed.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


ROWS = 4
COLS = 4
ALPHA_THRESHOLD = 48
MIN_COMPONENT_AREA = 256
PALETTE_COLORS = 48


def _component_for_tile(
    labels: np.ndarray,
    component_areas: np.ndarray,
    row: int,
    column: int,
) -> int:
    """Return the largest component whose centroid belongs to one grid tile."""

    height, width = labels.shape
    x0 = width * column / COLS
    x1 = width * (column + 1) / COLS
    y0 = height * row / ROWS
    y1 = height * (row + 1) / ROWS

    candidates: list[tuple[int, int]] = []
    for component_id in range(1, len(component_areas)):
        area = int(component_areas[component_id])
        if area < MIN_COMPONENT_AREA:
            continue
        yy, xx = np.nonzero(labels == component_id)
        if not len(xx):
            continue
        center_x = float(xx.mean())
        center_y = float(yy.mean())
        if x0 <= center_x < x1 and y0 <= center_y < y1:
            candidates.append((area, component_id))

    if not candidates:
        raise ValueError(f"No sprite component found in source cell ({row}, {column}).")
    candidates.sort(reverse=True)
    return candidates[0][1]


def _extract_frames(source: Image.Image) -> list[Image.Image]:
    rgba = np.asarray(source.convert("RGBA"))
    mask = rgba[:, :, 3] >= ALPHA_THRESHOLD
    labels, count = ndimage.label(mask, structure=np.ones((3, 3), dtype=np.uint8))
    if count < ROWS * COLS:
        raise ValueError(f"Expected at least 16 opaque components, found {count}.")

    component_areas = np.bincount(labels.ravel())
    frames: list[Image.Image] = []
    used_components: set[int] = set()

    for row in range(ROWS):
        for column in range(COLS):
            component_id = _component_for_tile(labels, component_areas, row, column)
            if component_id in used_components:
                raise ValueError(
                    f"Component {component_id} was assigned to more than one cell."
                )
            used_components.add(component_id)

            yy, xx = np.nonzero(labels == component_id)
            left = int(xx.min())
            top = int(yy.min())
            right = int(xx.max()) + 1
            bottom = int(yy.max()) + 1

            crop = rgba[top:bottom, left:right].copy()
            crop_labels = labels[top:bottom, left:right]
            crop[crop_labels != component_id] = (0, 0, 0, 0)
            crop[:, :, 3] = np.where(crop_labels == component_id, 255, 0).astype(
                np.uint8
            )
            frames.append(Image.fromarray(crop))

    if len(frames) != ROWS * COLS:
        raise AssertionError(f"Expected 16 frames, extracted {len(frames)}.")
    return frames


def _validate_sheet(sheet: Image.Image, cell_size: int, padding: int) -> None:
    expected_size = (cell_size * COLS, cell_size * ROWS)
    if sheet.size != expected_size:
        raise ValueError(f"Expected output size {expected_size}, got {sheet.size}.")

    alpha = np.asarray(sheet.getchannel("A"))
    alpha_values = set(int(value) for value in np.unique(alpha))
    if not alpha_values.issubset({0, 255}):
        raise ValueError(f"Output alpha is not binary: {sorted(alpha_values)}")

    unique_frames: set[bytes] = set()
    for row in range(ROWS):
        for column in range(COLS):
            left = column * cell_size
            top = row * cell_size
            frame = sheet.crop((left, top, left + cell_size, top + cell_size))
            bbox = frame.getchannel("A").getbbox()
            if bbox is None:
                raise ValueError(f"Output cell ({row}, {column}) is empty.")
            if bbox[0] < padding or bbox[1] < padding:
                raise ValueError(
                    f"Output cell ({row}, {column}) violates top/left padding: {bbox}"
                )
            if bbox[2] > cell_size - padding or bbox[3] > cell_size - padding:
                raise ValueError(
                    f"Output cell ({row}, {column}) violates bottom/right padding: {bbox}"
                )
            unique_frames.add(frame.tobytes())

    if len(unique_frames) != ROWS * COLS:
        raise ValueError(f"Expected 16 distinct frames, found {len(unique_frames)}.")

    rgba = np.asarray(sheet)
    opaque_rgb = rgba[rgba[:, :, 3] == 255, :3]
    color_count = len(np.unique(opaque_rgb, axis=0))
    if color_count > PALETTE_COLORS:
        raise ValueError(
            f"Expected at most {PALETTE_COLORS} opaque colors, found {color_count}."
        )

    print(f"validated=16 distinct cells, binary alpha, {color_count} opaque colors")


def build_sheet(
    source_path: Path, output_path: Path, cell_size: int, padding: int
) -> None:
    if cell_size <= padding * 2:
        raise ValueError("Cell size must be larger than twice the padding.")

    with Image.open(source_path) as source:
        frames = _extract_frames(source)

    max_width = max(frame.width for frame in frames)
    max_height = max(frame.height for frame in frames)
    available = cell_size - padding * 2
    scale = min(available / max_width, available / max_height)
    if scale <= 0.0:
        raise ValueError("Computed an invalid frame scale.")

    sheet = Image.new("RGBA", (cell_size * COLS, cell_size * ROWS), (0, 0, 0, 0))
    frame_boxes: list[tuple[int, int, int, int]] = []

    for index, frame in enumerate(frames):
        width = max(1, round(frame.width * scale))
        height = max(1, round(frame.height * scale))
        resized = frame.resize((width, height), Image.Resampling.NEAREST)

        row, column = divmod(index, COLS)
        cell_left = column * cell_size
        cell_top = row * cell_size
        x = cell_left + (cell_size - width) // 2
        y = cell_top + cell_size - padding - height
        sheet.alpha_composite(resized, (x, y))
        frame_boxes.append((x - cell_left, y - cell_top, width, height))

    # A single no-dither palette pass keeps all 16 frames visually cohesive.
    # Re-threshold alpha afterward so the shipping sheet retains hard pixel edges.
    alpha = sheet.getchannel("A").point(lambda value: 255 if value >= 128 else 0)
    sheet = sheet.quantize(
        colors=PALETTE_COLORS,
        method=Image.Quantize.FASTOCTREE,
        dither=Image.Dither.NONE,
    ).convert("RGBA")
    sheet.putalpha(alpha)

    _validate_sheet(sheet, cell_size, padding)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, format="PNG", optimize=True)

    print(f"source={source_path}")
    print(f"output={output_path}")
    print(
        f"sheet={sheet.width}x{sheet.height} cell={cell_size}x{cell_size} scale={scale:.4f}"
    )
    for index, box in enumerate(frame_boxes):
        row, column = divmod(index, COLS)
        print(f"frame[{row},{column}] x={box[0]} y={box[1]} w={box[2]} h={box[3]}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--cell-size", type=int, default=128)
    parser.add_argument("--padding", type=int, default=6)
    args = parser.parse_args()
    build_sheet(args.source, args.output, args.cell_size, args.padding)


if __name__ == "__main__":
    main()
