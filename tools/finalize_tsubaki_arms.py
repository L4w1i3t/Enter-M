"""Finalize Tsubaki's arm variants as full-canvas production layers.

Default and reserved donors contain touching hands, so their already-calibrated
combined RGBA art is partitioned into two disjoint arm files; recomposition is
pixel-exact.  Notebook donors contain two disconnected assemblies and are split
by connected component.  The uniform notebook components receive small
component-local shifts so their generated shoulder stubs meet the canonical
torso rather than landing over the lapels.

The stifled-laugh donor is asymmetric: its raised hand belongs in ``arm_over``
above the face, while its low arm remains in an ordinary arm group.  Those two
isolated components are independently scaled and anchored to the shared body.
"""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

import process_sam_poses as checker_processor
from process_sprite_reference import save_rgba, warp_rgba_to_canvas


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MASTER_DIR = PROJECT_ROOT / "tmp" / "tsubaki_sprite_masters"
PART_DIR = PROJECT_ROOT / "tmp" / "tsubaki_sprite_parts"
CANVAS_SIZE = (1024, 1536)


def load_rgba(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        if image.size != CANVAS_SIZE:
            raise ValueError(f"{path}: got {image.size}, expected {CANVAS_SIZE}")
        return np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()


def clean_layer(rgba: np.ndarray) -> np.ndarray:
    result = np.asarray(rgba, dtype=np.uint8).copy()
    result[result[:, :, 3] == 0, :3] = 0
    return result


def component_masks(rgba: np.ndarray) -> list[np.ndarray]:
    visible = rgba[:, :, 3] >= 32
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(
        visible.astype(np.uint8), connectivity=8
    )
    components: list[tuple[float, np.ndarray]] = []
    for label in range(1, count):
        if stats[label, cv2.CC_STAT_AREA] < 300:
            continue
        components.append((float(centroids[label, 0]), labels == label))
    components.sort(key=lambda item: item[0])
    return [mask for _, mask in components]


def layer_from_mask(rgba: np.ndarray, mask: np.ndarray) -> np.ndarray:
    layer = np.zeros_like(rgba)
    layer[mask] = rgba[mask]
    return clean_layer(layer)


def shift_rgba(rgba: np.ndarray, shift_x: int, shift_y: int) -> np.ndarray:
    result = np.zeros_like(rgba)
    height, width = rgba.shape[:2]
    source_left = max(0, -shift_x)
    source_top = max(0, -shift_y)
    source_right = min(width, width - shift_x)
    source_bottom = min(height, height - shift_y)
    if source_right <= source_left or source_bottom <= source_top:
        return result
    target_left = source_left + shift_x
    target_top = source_top + shift_y
    target_right = source_right + shift_x
    target_bottom = source_bottom + shift_y
    result[target_top:target_bottom, target_left:target_right] = rgba[
        source_top:source_bottom, source_left:source_right
    ]
    return clean_layer(result)


def grade_notebook(
    rgba: np.ndarray, region: tuple[int, int, int, int]
) -> tuple[np.ndarray, int]:
    """Move the generated ochre cover into an unmistakable golden yellow.

    The hue operation is limited to a measured notebook rectangle and to
    saturated orange pixels, so skin, white page edges, sleeves, and stitching
    retain their original colors.
    """

    result = clean_layer(rgba)
    left, top, right, bottom = region
    rgb = result[:, :, :3]
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    yy, xx = np.indices(result.shape[:2])
    in_region = (xx >= left) & (xx < right) & (yy >= top) & (yy < bottom)
    cover = (
        in_region
        & (result[:, :, 3] > 0)
        & (hsv[:, :, 0] >= 8)
        & (hsv[:, :, 0] <= 24)
        & (hsv[:, :, 1] >= 105)
        & (hsv[:, :, 2] >= 55)
    )
    hsv[:, :, 0][cover] = np.minimum(
        hsv[:, :, 0][cover].astype(np.int16) + 8, 179
    ).astype(np.uint8)
    graded_rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    result[:, :, :3][cover] = graded_rgb[cover]
    return clean_layer(result), int(cover.sum())


def split_touching_pair(outfit: str, pose: str) -> dict[str, object]:
    source_path = PART_DIR / f"forward_{outfit}_arms_{pose}.png"
    rgba = load_rgba(source_path)
    visible = rgba[:, :, 3] > 0
    _, xx = np.indices(visible.shape)
    left_mask = visible & (xx < 512)
    right_mask = visible & ~left_mask
    left = layer_from_mask(rgba, left_mask)
    right = layer_from_mask(rgba, right_mask)
    save_rgba(PART_DIR / f"forward_{outfit}_arm_l_{pose}.png", left)
    save_rgba(PART_DIR / f"forward_{outfit}_arm_r_{pose}.png", right)
    reconstructed = np.asarray(
        Image.alpha_composite(Image.fromarray(left), Image.fromarray(right)),
        dtype=np.uint8,
    )
    exact = bool(np.array_equal(reconstructed, rgba))
    if not exact:
        raise RuntimeError(f"{outfit}/{pose}: arm split did not reconstruct exactly")
    return {
        "source": str(source_path),
        "left_pixels": int((left[:, :, 3] > 0).sum()),
        "right_pixels": int((right[:, :, 3] > 0).sum()),
        "reconstruction_exact": exact,
    }


def split_notebook_pair(outfit: str) -> dict[str, object]:
    source_path = PART_DIR / f"forward_{outfit}_arms_notebook.png"
    rgba = load_rgba(source_path)
    masks = component_masks(rgba)
    if len(masks) != 2:
        raise RuntimeError(f"{source_path}: expected 2 arm components, found {len(masks)}")
    left = layer_from_mask(rgba, masks[0])
    right = layer_from_mask(rgba, masks[1])
    shifts = {"casual": ((0, 0), (0, 0)), "uniform": ((-70, 25), (-55, 25))}
    left_shift, right_shift = shifts[outfit]
    left = shift_rgba(left, *left_shift)
    right = shift_rgba(right, *right_shift)
    if outfit == "casual":
        left, graded_pixels = grade_notebook(left, (190, 970, 430, 1230))
    else:
        right, graded_pixels = grade_notebook(right, (500, 840, 760, 1120))
    save_rgba(PART_DIR / f"forward_{outfit}_arm_l_notebook.png", left)
    save_rgba(PART_DIR / f"forward_{outfit}_arm_r_notebook.png", right)
    return {
        "source": str(source_path),
        "left_shift": list(left_shift),
        "right_shift": list(right_shift),
        "left_pixels": int((left[:, :, 3] > 0).sum()),
        "right_pixels": int((right[:, :, 3] > 0).sum()),
        "notebook_hue_shift": 8,
        "notebook_graded_pixels": graded_pixels,
    }


def matte_raw(path: Path) -> np.ndarray:
    checker_processor.CANVAS_WIDTH, checker_processor.CANVAS_HEIGHT = CANVAS_SIZE
    checker_processor.CANVAS_SIZE = CANVAS_SIZE
    matte = checker_processor.extract_checker_matte(
        path,
        feather_radius=1.35,
        palette_tolerance=17.0,
        minimum_foreground_fraction=0.01,
    )
    return clean_layer(matte.rgba)


def place_component(
    source: np.ndarray,
    mask: np.ndarray,
    *,
    scale: float,
    source_anchor: tuple[float, float],
    target_anchor: tuple[float, float],
) -> np.ndarray:
    component = layer_from_mask(source, mask)
    translate_x = target_anchor[0] - scale * source_anchor[0]
    translate_y = target_anchor[1] - scale * source_anchor[1]
    return clean_layer(
        warp_rgba_to_canvas(
            component,
            scale=scale,
            translate_x=translate_x,
            translate_y=translate_y,
            canvas_size=CANVAS_SIZE,
        )
    )


def process_stifled_pair(outfit: str) -> dict[str, object]:
    source_path = MASTER_DIR / f"arms_stifled_laugh_{outfit}_raw.png"
    rgba = matte_raw(source_path)
    masks = component_masks(rgba)
    if len(masks) != 2:
        raise RuntimeError(f"{source_path}: expected 2 arm components, found {len(masks)}")
    if outfit == "casual":
        raised_spec = (1.02, (345.0, 699.0), (345.0, 800.0))
        low_spec = (1.00, (715.0, 776.0), (680.0, 820.0))
    else:
        raised_spec = (0.62, (310.0, 880.0), (380.0, 880.0))
        low_spec = (1.05, (690.0, 710.0), (680.0, 820.0))
    raised = place_component(
        rgba,
        masks[0],
        scale=raised_spec[0],
        source_anchor=raised_spec[1],
        target_anchor=raised_spec[2],
    )
    low = place_component(
        rgba,
        masks[1],
        scale=low_spec[0],
        source_anchor=low_spec[1],
        target_anchor=low_spec[2],
    )
    save_rgba(PART_DIR / f"forward_{outfit}_over_stifled_laugh.png", raised)
    save_rgba(PART_DIR / f"forward_{outfit}_arm_r_stifled_laugh.png", low)
    return {
        "source": str(source_path),
        "raised": {
            "scale": raised_spec[0],
            "source_anchor": list(raised_spec[1]),
            "target_anchor": list(raised_spec[2]),
            "visible_pixels": int((raised[:, :, 3] > 0).sum()),
        },
        "low": {
            "scale": low_spec[0],
            "source_anchor": list(low_spec[1]),
            "target_anchor": list(low_spec[2]),
            "visible_pixels": int((low[:, :, 3] > 0).sum()),
        },
    }


def main() -> int:
    PART_DIR.mkdir(parents=True, exist_ok=True)
    report: dict[str, object] = {"schema_version": 1, "variants": {}}
    variants = report["variants"]
    assert isinstance(variants, dict)
    for outfit in ("casual", "uniform"):
        for pose in ("default", "reserved"):
            variants[f"{outfit}/{pose}"] = split_touching_pair(outfit, pose)
        variants[f"{outfit}/notebook"] = split_notebook_pair(outfit)
        variants[f"{outfit}/stifled_laugh"] = process_stifled_pair(outfit)
    report_path = PART_DIR / "arm_metrics.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Finalized 8 Tsubaki outfit/arm-pose combinations: {PART_DIR}")
    print(f"Metrics: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
