from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MATSUDА_ROOT = PROJECT_ROOT / "game" / "mod_assets" / "char_sprites" / "matsuda"
OUTPUT_ROOT = Path(__file__).resolve().parent / "matsuda_faces_v2"
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
WIDTH = 1023
HEIGHT = 1537


base = np.asarray(Image.open(MATSUDА_ROOT / "neut_uniform.png").convert("RGBA"))
base_rgb = base[:, :, :3]
casual_base = np.asarray(
    Image.open(
        PROJECT_ROOT
        / "game"
        / "mod_assets"
        / "char_sprites"
        / "matsuda"
        / "neutral.png"
    ).convert("RGBA")
)
shared_opaque = (base[:, :, 3] == 255) & (casual_base[:, :, 3] == 255)
y_grid, x_grid = np.ogrid[:HEIGHT, :WIDTH]


def ellipse(center_x: float, center_y: float, radius_x: float, radius_y: float) -> np.ndarray:
    return (
        ((x_grid - center_x) / radius_x) ** 2
        + ((y_grid - center_y) / radius_y) ** 2
        <= 1.0
    )


allowed_expression = (
    ellipse(410, 305, 72, 58)
    | ellipse(512, 297, 76, 58)
    | ellipse(466, 361, 112, 70)
    | ellipse(466, 337, 125, 72)
)


def edge_map(rgb: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
    horizontal = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    vertical = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    return cv2.GaussianBlur(cv2.magnitude(horizontal, vertical), (0, 0), 1.0)


def register_generated_expression(source_rgb: np.ndarray) -> np.ndarray:
    reference_edges = edge_map(base_rgb)
    source_edges = edge_map(source_rgb)
    head_region = (
        (x_grid >= 260)
        & (x_grid <= 760)
        & (y_grid >= 80)
        & (y_grid <= 590)
    )
    expression_region = ellipse(466, 335, 145, 125)
    stable_mask = (
        head_region
        & ~expression_region
        & (base[:, :, 3] >= 240)
        & (source_rgb.max(axis=2) >= 24)
    ).astype(np.uint8) * 255
    warp = np.eye(2, 3, dtype=np.float32)
    score, warp = cv2.findTransformECC(
        reference_edges,
        source_edges,
        warp,
        cv2.MOTION_AFFINE,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-7),
        inputMask=stable_mask,
        gaussFiltSize=5,
    )
    print(f"generated disgusted ECC {score:.4f}; warp={warp.tolist()}")
    aligned_rgb = cv2.warpAffine(
        source_rgb,
        warp,
        (WIDTH, HEIGHT),
        flags=cv2.INTER_LANCZOS4 | cv2.WARP_INVERSE_MAP,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0),
    )
    return np.dstack((aligned_rgb, np.full((HEIGHT, WIDTH), 255, dtype=np.uint8)))


def feature_mask(source: np.ndarray) -> np.ndarray:
    difference = np.max(
        np.abs(source[:, :, :3].astype(np.int16) - base_rgb.astype(np.int16)),
        axis=2,
    ).astype(np.uint8)
    seed = ((difference >= 20) & allowed_expression).astype(np.uint8) * 255
    count, labels, stats, _ = cv2.connectedComponentsWithStats(seed, connectivity=8)
    retained = np.zeros_like(seed)
    for label in range(1, count):
        if stats[label, cv2.CC_STAT_AREA] >= 12:
            retained[labels == label] = 255

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    retained = cv2.morphologyEx(retained, cv2.MORPH_CLOSE, kernel)
    retained = cv2.dilate(retained, kernel, iterations=1)
    retained = cv2.GaussianBlur(retained, (0, 0), 3.0)
    retained = np.minimum(retained, source[:, :, 3])
    retained[~allowed_expression] = 0
    retained[~shared_opaque] = 0
    return retained


for face_path in sorted(MATSUDА_ROOT.glob("face_*.png")):
    source = np.asarray(Image.open(face_path).convert("RGBA"))
    if face_path.name == "face_crying.png":
        source = cv2.warpAffine(
            source,
            np.array(((1.0, 0.0, 1.0), (0.0, 1.0, -6.0)), dtype=np.float32),
            (WIDTH, HEIGHT),
            flags=cv2.INTER_LANCZOS4,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0, 0, 0, 0),
        )
    if face_path.name == "face_disgusted.png":
        generated_path = Path(__file__).resolve().parent / "matsuda_disgusted_generated.png"
        if generated_path.exists():
            generated_rgb = np.asarray(Image.open(generated_path).convert("RGB"))
            source = register_generated_expression(generated_rgb)
    output = source.copy()
    if face_path.name == "face_neut.png":
        output[:] = 0
    else:
        output[:, :, 3] = feature_mask(source)
    output[output[:, :, 3] == 0, :3] = 0
    Image.fromarray(output, "RGBA").save(OUTPUT_ROOT / face_path.name)


labels_and_images: list[tuple[str, Image.Image]] = []
base_image = Image.fromarray(base)
for face_path in sorted(OUTPUT_ROOT.glob("face_*.png")):
    if face_path.name == "face_neut.png":
        continue
    face = Image.open(face_path).convert("RGBA")
    composite = Image.alpha_composite(base_image, face)
    labels_and_images.append((face_path.stem.removeprefix("face_"), composite))

columns = 5
cell_size = (384, 412)
crop_box = (280, 140, 700, 560)
rows = (len(labels_and_images) + columns - 1) // columns
sheet = Image.new("RGB", (columns * cell_size[0], rows * cell_size[1]), (24, 24, 28))
draw = ImageDraw.Draw(sheet)
font = ImageFont.load_default(size=16)
for index, (label, composite) in enumerate(labels_and_images):
    column = index % columns
    row = index // columns
    x = column * cell_size[0]
    y = row * cell_size[1]
    crop = composite.crop(crop_box).resize((360, 360), Image.Resampling.LANCZOS)
    sheet.paste(crop.convert("RGB"), (x + 12, y + 8))
    draw.text(
        (x + cell_size[0] // 2, y + 380),
        label,
        font=font,
        fill=(238, 238, 242),
        anchor="ma",
    )
sheet.save(Path(__file__).resolve().parent / "matsuda_heads_v2.jpg", quality=95)
