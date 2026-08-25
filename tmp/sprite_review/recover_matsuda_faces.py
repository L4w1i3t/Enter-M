from __future__ import annotations

import csv
import hashlib
import io
import zlib
from pathlib import Path

import numpy as np
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OBJECT_ROOT = PROJECT_ROOT / ".git" / "objects"
SPRITE_ROOT = PROJECT_ROOT / "game" / "mod_assets" / "char_sprites" / "matsuda"
OUTPUT_ROOT = (
    Path(__file__).resolve().parent
    / "recovered_layers"
    / "matsuda_faces_named"
)
CANVAS_SIZE = (1023, 1537)

# These blobs reproduce every high-alpha RGB pixel retained by the installed v2
# feature mask. Neutral is compared with the full neutral uniform sprite because
# the installed neutral overlay is intentionally transparent.
EXACT_SOURCES = {
    "afraid": "f45f4b34fcbcf0fe94d0c6419a7cf5632998b034",
    "angry": "eaefc0dd639d8efa1373f45c5226dacd761c9d35",
    "annoyed": "6c4917eae9476a0915b4c97b1dc4099777417aa0",
    "curious": "2a34626c6e3a8889e1d7e2cebb528f694ab8c87e",
    "determined": "656dd3a4c7387d10c34937e8db9adf10bf0b620c",
    "embarrassed": "00c5b2074776e97787c9c10bf1647a7822011042",
    "empty": "be2aba2115cf4be02253a2fc7ac6aeb32c838ea1",
    "frustrated": "9d1d22e39d49849c6b4df87a5468d91f4ae81a95",
    "happy": "f282bd2eac238caa84b907ca3df8fa2fcfbcb565",
    "nervous": "20939bff3d589361f1ff6695c2a59512413cdc67",
    "neut": "acb745b338d86fce097224ef90d4c4b25a500f7c",
    "panicked": "3ef1b8ed5341845750f0955248f823d0bbd42de0",
    "sad": "87af1341b0ce83259cf25d7d268046ebc979d8c5",
    "smug": "7ca851828c342fa32e0c9421d746baddc08236b6",
    "teasing": "d1440213b50e9b70fd2392adc1958628afaddc33",
    "thinking": "e37d64fb80beac5d9ef92a02df23a360987e10b0",
    "unamused": "eb98736c4c8f54bfd41ae683cacef75dc195ad22",
    "worried": "64ba5026953f56dcf77f58b9566310389103cd91",
}
EXPRESSION_BY_OID = {object_id: expression for expression, object_id in EXACT_SOURCES.items()}
UNRESOLVED_EXPRESSIONS = ("crying", "disgusted", "shocked")


def unpack_loose_object(path: Path) -> tuple[str, str, bytes]:
    packed = zlib.decompress(path.read_bytes())
    header, content = packed.split(b"\0", 1)
    kind, size_text = header.decode("ascii").split(" ", 1)
    if len(content) != int(size_text):
        raise ValueError(f"Wrong object length in {path}")
    object_id = hashlib.sha1(header + b"\0" + content).hexdigest()
    return object_id, kind, content


def loose_png_blobs() -> dict[str, bytes]:
    blobs: dict[str, bytes] = {}
    for directory in sorted(OBJECT_ROOT.iterdir()):
        if not directory.is_dir() or len(directory.name) != 2:
            continue
        try:
            int(directory.name, 16)
        except ValueError:
            continue
        for path in sorted(directory.iterdir()):
            if not path.is_file():
                continue
            try:
                object_id, kind, content = unpack_loose_object(path)
            except (OSError, ValueError, zlib.error):
                continue
            if kind == "blob" and content.startswith(b"\x89PNG\r\n\x1a\n"):
                blobs.setdefault(object_id, content)
    return blobs


def rgba_from_bytes(content: bytes) -> np.ndarray:
    with Image.open(io.BytesIO(content)) as image:
        return np.asarray(image.convert("RGBA"))


def rgba_from_path(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        return np.asarray(image.convert("RGBA"))


def alpha_bbox(alpha: np.ndarray) -> tuple[int, int, int, int] | None:
    ys, xs = np.nonzero(alpha)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)


def is_head_overlay(image: np.ndarray) -> bool:
    if (image.shape[1], image.shape[0]) != CANVAS_SIZE:
        return False
    bbox = alpha_bbox(image[:, :, 3])
    if bbox is None:
        return False
    x0, y0, x1, y1 = bbox
    return (
        250 <= x0 <= 450
        and 150 <= y0 <= 320
        and 500 <= x1 <= 700
        and 350 <= y1 <= 520
        and 100 <= x1 - x0 <= 350
        and 80 <= y1 - y0 <= 300
    )


def similarity(source: np.ndarray, target: np.ndarray) -> tuple[float, float]:
    target_mask = target[:, :, 3] >= 128
    source_mask = source[:, :, 3] >= 128
    overlap = target_mask & source_mask
    target_count = int(target_mask.sum())
    coverage = float(overlap.sum() / target_count) if target_count else 0.0
    if not overlap.any():
        return float("inf"), coverage
    delta = np.abs(
        source[:, :, :3].astype(np.int16) - target[:, :, :3].astype(np.int16)
    )
    return float(delta[overlap].mean()), coverage


def neutral_similarity(source: np.ndarray, neutral_sprite: np.ndarray) -> float:
    mask = source[:, :, 3] >= 128
    if not mask.any():
        return float("inf")
    delta = np.abs(
        source[:, :, :3].astype(np.int16)
        - neutral_sprite[:, :, :3].astype(np.int16)
    )
    return float(delta[mask].mean())


def confidence_for(best_mae: float, margin: float) -> str:
    # This is confidence in the nearest visual family, not proof of provenance.
    if best_mae <= 8.0 and margin >= 2.0:
        return "high_similarity"
    if best_mae <= 15.0 and margin >= 1.0:
        return "medium_similarity"
    return "low_similarity"


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


png_blobs = loose_png_blobs()
head_blobs: dict[str, tuple[bytes, np.ndarray]] = {}
for object_id, content in png_blobs.items():
    try:
        image = rgba_from_bytes(content)
    except (OSError, ValueError):
        continue
    if is_head_overlay(image):
        head_blobs[object_id] = content, image

if len(head_blobs) != 56:
    raise RuntimeError(f"Expected 56 loose full-canvas head overlays, found {len(head_blobs)}")
missing_exact = sorted(set(EXPRESSION_BY_OID) - set(head_blobs))
if missing_exact:
    raise RuntimeError(f"Missing exact source blobs: {', '.join(missing_exact)}")

installed = {
    path.stem.removeprefix("face_"): rgba_from_path(path)
    for path in sorted(SPRITE_ROOT.glob("face_*.png"))
    if path.stem != "face_neut"
}
neutral_sprite = rgba_from_path(SPRITE_ROOT / "neut_uniform.png")

OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

all_rows: list[dict[str, object]] = []
exact_rows: list[dict[str, object]] = []
for object_id, (content, source) in sorted(head_blobs.items()):
    bbox = alpha_bbox(source[:, :, 3])
    scores = []
    for expression, target in installed.items():
        mae, coverage = similarity(source, target)
        scores.append((mae, expression, coverage))
    scores.sort()
    best_mae, best_expression, best_coverage = scores[0]
    second_mae, second_expression, _ = scores[1]
    margin = second_mae - best_mae
    neutral_mae = neutral_similarity(source, neutral_sprite)

    exact_expression = EXPRESSION_BY_OID.get(object_id)
    if exact_expression is not None:
        assigned_expression = exact_expression
        confidence = "exact_source"
        destination = OUTPUT_ROOT / f"face_{exact_expression}.png"
        destination.write_bytes(content)
    else:
        assigned_expression = best_expression
        confidence = confidence_for(best_mae, margin)

    all_rows.append(
        {
            "object_id": object_id,
            "blob_bytes": len(content),
            "alpha_bbox": ",".join(str(value) for value in bbox or ()),
            "alpha_nonzero": int((source[:, :, 3] > 0).sum()),
            "alpha_128": int((source[:, :, 3] >= 128).sum()),
            "assigned_expression": assigned_expression,
            "confidence": confidence,
            "best_nonneutral_expression": best_expression,
            "best_nonneutral_mae": f"{best_mae:.6f}",
            "best_nonneutral_coverage": f"{best_coverage:.6f}",
            "second_nonneutral_expression": second_expression,
            "second_nonneutral_mae": f"{second_mae:.6f}",
            "mae_margin": f"{margin:.6f}",
            "neutral_fullsprite_mae": f"{neutral_mae:.6f}",
            "recovered_filename": f"face_{exact_expression}.png" if exact_expression else "",
        }
    )

    if exact_expression is None:
        continue

    if exact_expression == "neut":
        comparison_mask = source[:, :, 3] >= 128
        installed_alpha_128 = 0
        rgb_mae = neutral_similarity(source, neutral_sprite)
        coverage = 1.0
        extra_alpha_128 = int(comparison_mask.sum())
        comparison_target = "neut_uniform.png RGB"
    else:
        target = installed[exact_expression]
        comparison_mask = target[:, :, 3] >= 128
        installed_alpha_128 = int(comparison_mask.sum())
        rgb_mae, coverage = similarity(source, target)
        extra_alpha_128 = int(
            ((source[:, :, 3] >= 128) & (target[:, :, 3] < 128)).sum()
        )
        comparison_target = f"installed face_{exact_expression}.png high-alpha RGB"

    exact_rows.append(
        {
            "expression": exact_expression,
            "object_id": object_id,
            "blob_bytes": len(content),
            "source_alpha_bbox": ",".join(str(value) for value in bbox or ()),
            "source_alpha_nonzero": int((source[:, :, 3] > 0).sum()),
            "source_alpha_128": int((source[:, :, 3] >= 128).sum()),
            "installed_alpha_128": installed_alpha_128,
            "source_extra_alpha_128": extra_alpha_128,
            "rgb_comparison_target": comparison_target,
            "retained_rgb_mae": f"{rgb_mae:.6f}",
            "retained_mask_coverage": f"{coverage:.6f}",
            "cleaner_alpha_than_installed": "no",
            "quality_note": (
                "Exact original RGB source; broad near-opaque pre-v2 alpha is less clean "
                "than the installed feature-only mask."
            ),
        }
    )

all_rows.sort(key=lambda row: (str(row["assigned_expression"]), str(row["object_id"])))
exact_rows.sort(key=lambda row: str(row["expression"]))

write_tsv(
    OUTPUT_ROOT / "all_56_similarity.tsv",
    list(all_rows[0]),
    all_rows,
)
write_tsv(
    OUTPUT_ROOT / "exact_sources.tsv",
    list(exact_rows[0]),
    exact_rows,
)

readme = f"""# Recovered Matsuda face sources

This directory contains {len(exact_rows)} byte-exact pre-v2 source PNGs recovered from
loose Git blobs. The complete {len(all_rows)}-blob nearest-expression inventory is in
`all_56_similarity.tsv`; only rows marked `exact_source` were recovered as named PNGs.

These are reference/source layers, not recommended drop-in game assets. Their retained
RGB agrees exactly with the installed feature masks, but the old alpha covers a broad,
nearly opaque head rectangle. The installed v2 feature-only alpha is cleaner and avoids
the baked background/seam risk.

No exact loose-blob source was found for: {', '.join(UNRESOLVED_EXPRESSIONS)}.
`disgusted` was replaced from a newly generated source during v2 processing; `crying`
and `shocked` appear to have come from task intermediates that were never stored as
loose Git objects.
"""
(OUTPUT_ROOT / "README.md").write_text(readme, encoding="utf-8")

print(f"Catalogued {len(all_rows)} loose Matsuda head overlays")
print(f"Recovered {len(exact_rows)} exact named sources to {OUTPUT_ROOT}")
print("Unresolved exact sources: " + ", ".join(UNRESOLVED_EXPRESSIONS))
