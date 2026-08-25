from __future__ import annotations

import hashlib
import re
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SPRITE_ROOT = PROJECT_ROOT / "game" / "mod_assets" / "char_sprites"
REVIEWED_ROOT = PROJECT_ROOT / "tmp" / "sprite_review" / "facebase_v3"
CANVAS = (1023, 1537)
EXPRESSIONS = (
    "happy",
    "smug",
    "teasing",
    "thinking",
    "curious",
    "unamused",
    "annoyed",
    "frustrated",
    "angry",
    "sad",
    "crying",
    "embarrassed",
    "nervous",
    "worried",
    "shocked",
    "afraid",
    "panicked",
    "determined",
    "empty",
    "disgusted",
)


def load_rgba(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        assert image.size == CANVAS, f"{path}: {image.size}, expected {CANVAS}"
        return np.asarray(image.convert("RGBA")).copy()


def alpha_composite(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    return np.asarray(
        Image.alpha_composite(Image.fromarray(base), Image.fromarray(overlay))
    )


def bbox(mask: np.ndarray) -> tuple[int, int, int, int]:
    ys, xs = np.nonzero(mask)
    assert len(xs), "empty mask"
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assert_clean_transparency(path: Path, rgba: np.ndarray) -> None:
    hidden_rgb = np.any(rgba[:, :, :3] != 0, axis=2) & (rgba[:, :, 3] == 0)
    assert not hidden_rgb.any(), (
        f"{path}: {int(hidden_rgb.sum())} nonzero transparent RGB pixels"
    )


def warm_skin_mask(rgba: np.ndarray) -> np.ndarray:
    rgb = rgba[:, :, :3].astype(np.int16)
    red, green, blue = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    return (
        (red >= 145)
        & (green >= 100)
        & (blue >= 85)
        & (red >= green - 4)
        & (green >= blue - 12)
        & ((red - blue) >= 16)
        & (rgba[:, :, 3] >= 245)
    )


base_limits = {
    "asahina": {
        "count": (10_000, 12_500),
        "bbox": (370, 240, 605, 425),
        "expression_count": (1_000, 16_000),
    },
    "matsuda": {
        "count": (6_500, 8_500),
        "bbox": (345, 245, 575, 415),
        "expression_count": (1_000, 13_000),
    },
}

for character in ("asahina", "matsuda"):
    installed_root = SPRITE_ROOT / character
    reviewed_root = REVIEWED_ROOT / character
    originals = {
        "casual": load_rgba(installed_root / "neutral.png"),
        "uniform": load_rgba(installed_root / "neut_uniform.png"),
    }
    bases = {
        "casual": load_rgba(installed_root / "neut_face_base.png"),
        "uniform": load_rgba(installed_root / "neut_uniform_face_base.png"),
    }
    neutral_layers = {
        "casual": load_rgba(installed_root / "face_neut_casual.png"),
        "uniform": load_rgba(installed_root / "face_neut_uniform.png"),
    }

    for outfit in ("casual", "uniform"):
        base_name = "neut_face_base.png" if outfit == "casual" else "neut_uniform_face_base.png"
        neutral_name = f"face_neut_{outfit}.png"
        base_path = installed_root / base_name
        neutral_path = installed_root / neutral_name

        assert sha256(base_path) == sha256(reviewed_root / base_name), (
            f"{base_path}: differs from reviewed v3 asset"
        )
        assert sha256(neutral_path) == sha256(reviewed_root / neutral_name), (
            f"{neutral_path}: differs from reviewed v3 asset"
        )
        assert_clean_transparency(base_path, bases[outfit])
        assert_clean_transparency(neutral_path, neutral_layers[outfit])
        assert np.array_equal(bases[outfit][:, :, 3], originals[outfit][:, :, 3]), (
            f"{character}/{outfit}: featureless base changes the sprite silhouette"
        )

        changed = (
            np.any(bases[outfit][:, :, :3] != originals[outfit][:, :, :3], axis=2)
            & (originals[outfit][:, :, 3] > 0)
        )
        changed_count = int(changed.sum())
        minimum, maximum = base_limits[character]["count"]
        assert minimum <= changed_count <= maximum, (
            f"{character}/{outfit}: implausible face-base edit area {changed_count}"
        )
        x0, y0, x1, y1 = bbox(changed)
        limit_x0, limit_y0, limit_x1, limit_y1 = base_limits[character]["bbox"]
        assert x0 >= limit_x0 and y0 >= limit_y0 and x1 <= limit_x1 and y1 <= limit_y1, (
            f"{character}/{outfit}: base edit escapes face ({x0},{y0})-({x1},{y1})"
        )

        reconstructed = alpha_composite(bases[outfit], neutral_layers[outfit])
        assert np.array_equal(reconstructed, originals[outfit]), (
            f"{character}/{outfit}: neutral layer does not reconstruct original exactly"
        )

    uniform_skin = warm_skin_mask(bases["uniform"])
    for expression in EXPRESSIONS:
        path = installed_root / f"face_{expression}.png"
        reviewed_path = reviewed_root / f"face_{expression}.png"
        layer = load_rgba(path)
        assert sha256(path) == sha256(reviewed_path), (
            f"{path}: differs from reviewed v3 asset"
        )
        assert_clean_transparency(path, layer)

        alpha = layer[:, :, 3]
        visible = alpha > 0
        visible_count = int(visible.sum())
        minimum, maximum = base_limits[character]["expression_count"]
        assert minimum <= visible_count <= maximum, (
            f"{path}: implausible expression area {visible_count}"
        )
        assert int((alpha == 255).sum()) >= 1_000, f"{path}: lacks opaque feature cores"
        x0, y0, x1, y1 = bbox(visible)
        assert x0 >= 340 and y0 >= 225 and x1 <= 650 and y1 <= 460, (
            f"{path}: expression escapes face ({x0},{y0})-({x1},{y1})"
        )
        assert not np.any(visible & ~uniform_skin), (
            f"{path}: paints outside the featureless facial skin"
        )
        if character == "asahina" and expression == "thinking":
            assert not visible[405:, :].any(), (
                "Asahina thinking layer still contains the shifted jaw/side-face artifact"
            )

        for outfit, base in bases.items():
            composite = alpha_composite(base, layer)
            assert np.array_equal(composite[:, :, 3], base[:, :, 3]), (
                f"{path}: changes {outfit} silhouette"
            )
            assert np.array_equal(composite[~visible], base[~visible]), (
                f"{path}: changes {outfit} pixels outside its visible alpha"
            )


processed_poses = (
    SPRITE_ROOT / "asahina" / "pose_hairflip_uniform.png",
    SPRITE_ROOT / "asahina" / "pose_pointing_uniform.png",
    SPRITE_ROOT / "asahina" / "pose_eyeroll_uniform.png",
    SPRITE_ROOT / "matsuda" / "pose_laughing_casual.png",
    SPRITE_ROOT / "matsuda" / "pose_laughing_uniform.png",
    SPRITE_ROOT / "himeko" / "pose_furious_casual.png",
    SPRITE_ROOT / "himeko" / "pose_objection_uniform.png",
)
for path in processed_poses:
    pose = load_rgba(path)
    assert_clean_transparency(path, pose)
    x0, y0, x1, y1 = bbox(pose[:, :, 3] > 0)
    assert x0 > 0 and x1 < CANVAS[0], f"{path}: horizontally clipped ({x0}, {x1})"
    assert y0 > 0, f"{path}: top edge clipped"
    print(f"{path.relative_to(PROJECT_ROOT)} bbox=({x0},{y0})-({x1},{y1})")


# The eye-roll master previously had an opaque white wedge at this exact location.
eyeroll = load_rgba(SPRITE_ROOT / "asahina" / "pose_eyeroll_uniform.png")
rgb = eyeroll[:, :, :3]
maximum = rgb.max(axis=2)
minimum = rgb.min(axis=2)
neutral = (
    (minimum >= 150)
    & ((maximum - minimum) <= 40)
    & (eyeroll[:, :, 3] > 0)
)
assert not neutral[305:376, 377:398].any(), "Asahina eye-roll white matte remains"


# Both Matsuda laughing variants should occupy the same authored height.
matsuda_root = SPRITE_ROOT / "matsuda"
casual_laugh = load_rgba(matsuda_root / "pose_laughing_casual.png")
uniform_laugh = load_rgba(matsuda_root / "pose_laughing_uniform.png")
casual_bbox = bbox(casual_laugh[:, :, 3] > 0)
uniform_bbox = bbox(uniform_laugh[:, :, 3] > 0)
assert abs(casual_bbox[1] - uniform_bbox[1]) <= 8, (
    f"Matsuda laughing top mismatch: {casual_bbox[1]} vs {uniform_bbox[1]}"
)
assert abs((casual_bbox[3] - casual_bbox[1]) - (uniform_bbox[3] - uniform_bbox[1])) <= 10, (
    "Matsuda laughing height mismatch"
)


definition_path = PROJECT_ROOT / "game" / "mod_assets" / "def_characters.rpy"
definition = definition_path.read_text(encoding="utf-8")
referenced = {
    path
    for path in re.findall(r'"(mod_assets/char_sprites/[^"\n]+\.png)"', definition)
    if "<" not in path
}
missing = sorted(path for path in referenced if not (PROJECT_ROOT / "game" / path).is_file())
assert not missing, "Missing sprite references: " + ", ".join(missing)

for character in ("asahina", "matsuda"):
    for outfit in ("casual", "uniform"):
        expected = f'"mod_assets/char_sprites/{character}/face_neut_{outfit}.png"'
        assert expected in definition, f"{character}: missing conditioned {outfit} neutral layer"

assert re.search(
    r"layeredimage matsuda:.*?attribute disgusted:\s*\n\s*"
    r'"mod_assets/char_sprites/matsuda/face_disgusted\.png"',
    definition,
    re.DOTALL,
), "Matsuda disgusted layer is not declared"

print(f"Validated {2 * len(EXPRESSIONS)} alternate face layers, 4 neutral paths, and {len(processed_poses)} poses.")
print(f"Validated {len(referenced)} sprite references in def_characters.rpy.")
