from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REVIEW_ROOT = Path(__file__).resolve().parent
OUTPUT_ROOT = REVIEW_ROOT / "cleaned_poses"
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def keep_significant_components(mask: np.ndarray, minimum_area: int = 12) -> np.ndarray:
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        mask.astype(np.uint8), connectivity=8
    )
    retained = np.zeros_like(mask, dtype=bool)
    for label in range(1, count):
        if stats[label, cv2.CC_STAT_AREA] >= minimum_area:
            retained[labels == label] = True
    return retained


def soften_and_decontaminate(rgb: np.ndarray, foreground: np.ndarray) -> np.ndarray:
    foreground = keep_significant_components(foreground)
    inside_distance = ndimage.distance_transform_edt(foreground)
    outside_distance = ndimage.distance_transform_edt(~foreground)
    signed_distance = inside_distance - outside_distance
    alpha = np.clip(0.5 + signed_distance / 4.0, 0.0, 1.0)

    safe_foreground = foreground & (inside_distance >= 2.0)
    if not safe_foreground.any():
        safe_foreground = foreground
    _, nearest_indices = ndimage.distance_transform_edt(
        ~safe_foreground, return_indices=True
    )
    nearest_rgb = rgb[nearest_indices[0], nearest_indices[1]]
    cleaned_rgb = rgb.copy()
    transition = (alpha > 0.0) & (alpha < 1.0)
    cleaned_rgb[transition] = nearest_rgb[transition]
    cleaned_rgb[alpha <= 0.0] = 0

    return np.dstack((cleaned_rgb, np.rint(alpha * 255.0).astype(np.uint8)))


def extract_checkerboard(
    source_path: Path, destination_path: Path, prior_alpha_path: Path | None = None
) -> None:
    rgb = np.asarray(Image.open(source_path).convert("RGB"))
    maximum = rgb.max(axis=2)
    minimum = rgb.min(axis=2)
    chroma = maximum - minimum
    background_candidate = (minimum >= 218) & (chroma <= 18)

    # Only background-like pixels connected to the canvas count as matte. This
    # protects pale clothing and skin enclosed by the character's linework.
    flood_source = background_candidate.astype(np.uint8)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        flood_source, connectivity=8
    )
    canvas_background = np.zeros_like(background_candidate)
    island_background = np.zeros_like(background_candidate)
    height, width = background_candidate.shape
    for label in range(1, count):
        x = stats[label, cv2.CC_STAT_LEFT]
        y = stats[label, cv2.CC_STAT_TOP]
        component_width = stats[label, cv2.CC_STAT_WIDTH]
        component_height = stats[label, cv2.CC_STAT_HEIGHT]
        touches_canvas = (
            x == 0
            or y == 0
            or x + component_width == width
            or y + component_height == height
        )
        component = labels == label
        component_minimum = minimum[component]
        component_chroma = chroma[component]
        clean_checker_island = (
            stats[label, cv2.CC_STAT_AREA] >= 4
            and float(component_minimum.mean()) >= 236.0
            and float(component_chroma.mean()) <= 4.0
        )
        if touches_canvas:
            canvas_background[component] = True
        elif clean_checker_island:
            island_background[component] = True

    background = canvas_background | island_background

    if prior_alpha_path is not None:
        prior_alpha = np.asarray(
            Image.open(prior_alpha_path).convert("RGBA")
        )[:, :, 3]
        prior_core = cv2.erode(
            (prior_alpha >= 128).astype(np.uint8),
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)),
        ).astype(bool)
        prior_region = cv2.dilate(
            (prior_alpha > 0).astype(np.uint8),
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41)),
        ).astype(bool)
        # An isolated pale component inside the old silhouette is clothing or
        # skin, not a checker tile trapped between limbs. Canvas-connected pale
        # regions remain background even if the regenerated contour moved.
        background[island_background & prior_core] = False

    foreground = ~background
    if prior_alpha_path is not None:
        foreground &= prior_region

    inside_distance = ndimage.distance_transform_edt(foreground)
    pale_neutral_fringe = (
        foreground
        & (inside_distance <= 3.0)
        & (minimum >= 170)
        & (chroma <= 35)
    )
    foreground &= ~pale_neutral_fringe

    cleaned = soften_and_decontaminate(rgb, foreground)
    Image.fromarray(cleaned, "RGBA").save(destination_path)


def clean_existing_alpha(
    source_path: Path,
    destination_path: Path,
    remove_eyeroll_matte: bool = False,
) -> None:
    rgba = np.asarray(Image.open(source_path).convert("RGBA"))
    rgb = rgba[:, :, :3]
    original_foreground = rgba[:, :, 3] > 0
    inside_distance = ndimage.distance_transform_edt(original_foreground)
    maximum = rgb.max(axis=2)
    minimum = rgb.min(axis=2)
    chroma = maximum - minimum
    pale_neutral_fringe = (
        original_foreground
        & (inside_distance <= 3.0)
        & (minimum >= 170)
        & (chroma <= 35)
    )
    foreground = original_foreground & ~pale_neutral_fringe

    if remove_eyeroll_matte:
        # The source eye-roll pose contains one opaque white extraction wedge
        # between the left-side hair strands, not just a one-pixel fringe.
        # Select that isolated neutral component, including its anti-aliased
        # rim, without touching the character's pale shirt or skin.
        neutral = (
            original_foreground
            & (minimum >= 150)
            & (chroma <= 40)
        )
        search = np.zeros_like(neutral)
        search[275:425, 340:430] = True
        count, labels, stats, _ = cv2.connectedComponentsWithStats(
            (neutral & search).astype(np.uint8), connectivity=8
        )
        matte = np.zeros_like(neutral)
        for label in range(1, count):
            x, y, width, height, area = stats[label]
            if x <= 390 and y <= 330 and area >= 100:
                matte[labels == label] = True
        matte = cv2.dilate(
            matte.astype(np.uint8),
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
        ).astype(bool)
        matte &= (minimum >= 120) & (chroma <= 60)
        foreground &= ~matte

    cleaned = soften_and_decontaminate(rgb, foreground)
    Image.fromarray(cleaned, "RGBA").save(destination_path)


asahina_root = PROJECT_ROOT / "game" / "mod_assets" / "char_sprites" / "asahina"
for pose_name in ("hairflip", "pointing", "eyeroll"):
    extract_checkerboard(
        REVIEW_ROOT / f"asahina_{pose_name}_generated.png",
        OUTPUT_ROOT / f"asahina_{pose_name}.png",
        asahina_root / f"pose_{pose_name}_uniform.png",
    )
    clean_existing_alpha(
        asahina_root / f"pose_{pose_name}_uniform.png",
        OUTPUT_ROOT / f"asahina_{pose_name}_original_cleaned.png",
        remove_eyeroll_matte=pose_name == "eyeroll",
    )

himeko_root = PROJECT_ROOT / "game" / "mod_assets" / "char_sprites" / "himeko"
for filename in ("pose_furious_casual.png", "pose_objection_uniform.png"):
    clean_existing_alpha(himeko_root / filename, OUTPUT_ROOT / f"himeko_{filename}")
