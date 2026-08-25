from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASAHINA_ROOT = PROJECT_ROOT / "game" / "mod_assets" / "char_sprites" / "asahina"
OUTPUT_ROOT = Path(__file__).resolve().parent / "asahina_faces_v2"
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
WIDTH = 1023
HEIGHT = 1537
FACE_CENTER = (510, 330)


def edge_map(rgb: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
    horizontal = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    vertical = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    magnitude = cv2.magnitude(horizontal, vertical)
    return cv2.GaussianBlur(magnitude, (0, 0), 1.0)


base = np.asarray(Image.open(ASAHINA_ROOT / "neut_uniform.png").convert("RGBA"))
base_rgb = base[:, :, :3]
casual_base = np.asarray(Image.open(ASAHINA_ROOT / "neutral.png").convert("RGBA"))
shared_opaque = (base[:, :, 3] == 255) & (casual_base[:, :, 3] == 255)
reference_edges = edge_map(base_rgb)

y_grid, x_grid = np.ogrid[:HEIGHT, :WIDTH]
outer_face = (
    ((x_grid - FACE_CENTER[0]) / 190.0) ** 2
    + ((y_grid - FACE_CENTER[1]) / 175.0) ** 2
    <= 1.0
)
allowed_expression = (
    (((x_grid - 450.0) / 100.0) ** 2 + ((y_grid - 320.0) / 75.0) ** 2 <= 1.0)
    | (((x_grid - 570.0) / 105.0) ** 2 + ((y_grid - 300.0) / 75.0) ** 2 <= 1.0)
    | (((x_grid - 510.0) / 145.0) ** 2 + ((y_grid - 400.0) / 90.0) ** 2 <= 1.0)
)
stable_registration = outer_face.copy()
stable_registration &= ~(
    (((x_grid - 510.0) / 145.0) ** 2 + ((y_grid - 365.0) / 120.0) ** 2)
    <= 1.0
)
stable_registration &= base[:, :, 3] >= 240


REGISTRATION = {
    "afraid": (-11, 0, 1.011),
    "angry": (-13, 2, 1.0095),
    "annoyed": (-8, 0, 0.9915),
    "curious": (0, 0, 1.010),
    "determined": (-6, -1, 1.0),
    "embarrassed": (4, 0, 1.0095),
    "frustrated": (0, 0, 1.009),
    "happy": (0, 0, 1.0085),
    "panicked": (-4, -1, 1.0),
    "shocked": (-7, 0, 1.0),
    "teasing": (-5, -1, 1.0),
    "thinking": (1, 4, 1.0),
    "worried": (1, 2, 1.0),
}


def register(source: np.ndarray, expression: str) -> tuple[np.ndarray, tuple[float, float, float]]:
    shift_x, shift_y, scale = REGISTRATION.get(expression, (0, 0, 1.0))
    warp = np.array(
        [
            [scale, 0.0, (1.0 - scale) * FACE_CENTER[0] + shift_x],
            [0.0, scale, (1.0 - scale) * FACE_CENTER[1] + shift_y],
        ],
        dtype=np.float32,
    )
    aligned = cv2.warpAffine(
        source,
        warp,
        (WIDTH, HEIGHT),
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0, 0),
    )
    return aligned, (shift_x, shift_y, scale)


def make_mask(aligned: np.ndarray) -> np.ndarray:
    difference = np.max(
        np.abs(aligned[:, :, :3].astype(np.int16) - base_rgb.astype(np.int16)),
        axis=2,
    ).astype(np.uint8)
    # A low seed catches blush and subtle eyelid changes; a high seed ensures
    # the complete old/new eye and mouth footprints are always replaced.
    seed = ((difference >= 14) & allowed_expression).astype(np.uint8) * 255
    count, labels, stats, _ = cv2.connectedComponentsWithStats(seed, connectivity=8)
    retained = np.zeros_like(seed)
    for label in range(1, count):
        if stats[label, cv2.CC_STAT_AREA] >= 18:
            retained[labels == label] = 255

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
    retained = cv2.morphologyEx(retained, cv2.MORPH_CLOSE, kernel)
    retained = cv2.dilate(retained, kernel, iterations=1)
    retained = cv2.GaussianBlur(retained, (0, 0), 4.0)
    retained = np.minimum(retained, aligned[:, :, 3])
    retained[~allowed_expression] = 0
    retained[~shared_opaque] = 0
    return retained


reports: list[str] = []
for face_path in sorted(ASAHINA_ROOT.glob("face_*.png")):
    source = np.asarray(Image.open(face_path).convert("RGBA"))
    if face_path.name == "face_neut.png":
        Image.fromarray(source).save(OUTPUT_ROOT / face_path.name)
        continue
    expression = face_path.stem.removeprefix("face_")
    aligned, (shift_x, shift_y, scale) = register(source, expression)
    aligned[:, :, 3] = make_mask(aligned)
    aligned[aligned[:, :, 3] == 0, :3] = 0
    Image.fromarray(aligned).save(OUTPUT_ROOT / face_path.name)
    reports.append(
        f"{face_path.stem}: install shift ({shift_x:+.0f}, {shift_y:+.0f}), scale {scale:.4f}"
    )

(OUTPUT_ROOT / "registration.txt").write_text("\n".join(reports) + "\n", encoding="utf-8")


labels_and_images: list[tuple[str, Image.Image]] = []
for face_path in sorted(OUTPUT_ROOT.glob("face_*.png")):
    if face_path.name == "face_neut.png":
        continue
    face = Image.open(face_path).convert("RGBA")
    composite = Image.alpha_composite(Image.fromarray(base), face)
    labels_and_images.append((face_path.stem.removeprefix("face_"), composite))

columns = 5
cell_size = (384, 412)
crop_box = (260, 120, 760, 620)
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
sheet.save(Path(__file__).resolve().parent / "asahina_heads_v2.jpg", quality=95)
