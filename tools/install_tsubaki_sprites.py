#!/usr/bin/env python3
"""Install Tsubaki's reviewed, outfit-conditioned face patch bank.

The installer deliberately owns only the 42 ``face_<token>_<outfit>.png``
files produced in ``tmp/tsubaki_face_patch/output``.  It never copies, moves,
or removes Tsubaki's neutral bases, legacy ``*old*`` sprites, ``post_*``
sprites, or any unrelated asset.

Before installation, every source is validated and copied into a temporary
staging directory. The obsolete shared ``face_<token>.png`` bank is then
moved to ``tmp/tsubaki_face_patch/obsolete_modular_faces`` without overwriting
an earlier archive. Each validated layer is copied to a temporary sibling in
the production directory and atomically moved into place. Creating that
sibling in production is important on Windows: moving a file directly out of
``TemporaryDirectory`` retains its protected ACL and prevents sandboxed
viewers such as Windows Photos from opening the PNG.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = PROJECT_ROOT / "tmp" / "tsubaki_face_patch" / "output"
DESTINATION = PROJECT_ROOT / "game" / "assets" / "characters" / "tsubaki"
ARCHIVE_DIR = (
    PROJECT_ROOT / "tmp" / "tsubaki_face_patch" / "obsolete_modular_faces"
)
CANVAS_SIZE = (1023, 1537)

OUTFITS = ("casual", "uniform")
FACE_TOKENS = (
    "neut",
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
ALTERNATE_TOKENS = FACE_TOKENS[1:]


def conditioned_name(token: str, outfit: str) -> str:
    return f"face_{token}_{outfit}.png"


def shared_name(token: str) -> str:
    return f"face_{token}.png"


def production_manifest() -> dict[str, Path]:
    return {
        conditioned_name(token, outfit): SOURCE_DIR
        / conditioned_name(token, outfit)
        for token in FACE_TOKENS
        for outfit in OUTFITS
    }


def require_safe_child(path: Path, parent: Path, label: str) -> None:
    """Refuse a configured path whose parent escapes its intended directory."""

    resolved_parent = parent.resolve()
    resolved_candidate_parent = path.parent.resolve()
    if not resolved_candidate_parent.is_relative_to(resolved_parent):
        raise RuntimeError(f"Unsafe {label} path outside {resolved_parent}: {path}")


def load_validated_layer(path: Path, token: str) -> np.ndarray:
    if not path.is_file() or path.is_symlink():
        raise FileNotFoundError(f"Missing or unsafe source file: {path}")
    with Image.open(path) as image:
        if image.mode != "RGBA" or image.size != CANVAS_SIZE:
            raise ValueError(
                f"{path}: expected RGBA {CANVAS_SIZE}, got "
                f"{image.mode} {image.size}"
            )
        pixels = np.asarray(image, dtype=np.uint8).copy()

    alpha = pixels[:, :, 3]
    transparent = alpha == 0
    hidden_rgb = int(
        np.count_nonzero(transparent & np.any(pixels[:, :, :3] != 0, axis=2))
    )
    if hidden_rgb:
        raise ValueError(f"{path}: {hidden_rgb} zero-alpha pixels retain RGB")
    if token == "neut":
        if np.any(alpha):
            raise ValueError(f"{path}: neutral face layer must be fully transparent")
    elif not np.any(alpha):
        raise ValueError(f"{path}: alternate face layer is fully transparent")
    return pixels


def validate_sources(manifest: dict[str, Path]) -> None:
    if not SOURCE_DIR.is_dir() or SOURCE_DIR.is_symlink():
        raise FileNotFoundError(f"Missing or unsafe source directory: {SOURCE_DIR}")

    expected_names = set(manifest)
    actual_names = {
        path.name
        for path in SOURCE_DIR.glob("face_*.png")
        if path.is_file() and not path.is_symlink()
    }
    if actual_names != expected_names:
        missing = sorted(expected_names - actual_names)
        unexpected = sorted(actual_names - expected_names)
        raise ValueError(
            "Source face manifest differs from the exact 42-file bank: "
            f"missing={missing}, unexpected={unexpected}"
        )

    seen_alternates: dict[bytes, str] = {}
    for outfit in OUTFITS:
        neutral_name = conditioned_name("neut", outfit)
        neutral_source = manifest[neutral_name]
        require_safe_child(neutral_source, SOURCE_DIR, "source")
        load_validated_layer(neutral_source, "neut")

        common_alpha: np.ndarray | None = None
        for token in ALTERNATE_TOKENS:
            name = conditioned_name(token, outfit)
            source = manifest[name]
            require_safe_child(source, SOURCE_DIR, "source")
            layer = load_validated_layer(source, token)
            alpha = layer[:, :, 3]
            if common_alpha is None:
                common_alpha = alpha.copy()
            elif not np.array_equal(alpha, common_alpha):
                raise ValueError(
                    f"{name}: alpha mask differs "
                    f"from the fixed {outfit} alternate-expression mask"
                )
            signature = hashlib.sha256(layer).digest()
            previous = seen_alternates.get(signature)
            if previous is not None:
                raise ValueError(
                    f"Duplicate alternate face pixels: {previous} and "
                    f"{name}"
                )
            seen_alternates[signature] = name


def next_archive_path(filename: str) -> Path:
    """Return a nonexisting archive path without replacing older material."""

    candidate = ARCHIVE_DIR / filename
    if not candidate.exists() and not candidate.is_symlink():
        return candidate
    original = Path(filename)
    counter = 1
    while True:
        candidate = ARCHIVE_DIR / f"{original.stem}.{counter}{original.suffix}"
        if not candidate.exists() and not candidate.is_symlink():
            return candidate
        counter += 1


def archive_obsolete_shared_faces() -> list[tuple[Path, Path]]:
    candidates = [
        DESTINATION / shared_name(token)
        for token in FACE_TOKENS
        if (DESTINATION / shared_name(token)).exists()
    ]
    if not candidates:
        return []

    if ARCHIVE_DIR.exists() and (not ARCHIVE_DIR.is_dir() or ARCHIVE_DIR.is_symlink()):
        raise RuntimeError(f"Unsafe archive directory: {ARCHIVE_DIR}")
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    moved: list[tuple[Path, Path]] = []
    for source in candidates:
        require_safe_child(source, DESTINATION, "legacy production")
        if not source.is_file() or source.is_symlink():
            raise RuntimeError(f"Refusing non-file legacy face target: {source}")
        archive_path = next_archive_path(source.name)
        require_safe_child(archive_path, ARCHIVE_DIR, "archive")
        shutil.move(str(source), str(archive_path))
        moved.append((source, archive_path))
    return moved


def install_staged_files(staging_dir: Path, filenames: tuple[str, ...]) -> None:
    DESTINATION.mkdir(parents=True, exist_ok=True)
    for filename in filenames:
        target = DESTINATION / filename
        require_safe_child(target, DESTINATION, "production")
        if target.exists() and (not target.is_file() or target.is_symlink()):
            raise RuntimeError(f"Refusing unsafe production target: {target}")
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{filename}.",
            suffix=".tmp",
            dir=DESTINATION,
        )
        os.close(descriptor)
        temporary_target = Path(temporary_name)
        try:
            # The sibling inherits DESTINATION's ACL. os.replace then carries
            # that usable ACL to the final filename while keeping the content
            # update atomic.
            shutil.copy2(staging_dir / filename, temporary_target)
            load_validated_layer(
                temporary_target,
                filename.split("_")[1],
            )
            os.replace(temporary_target, target)
        finally:
            temporary_target.unlink(missing_ok=True)


def main() -> int:
    manifest = production_manifest()
    validate_sources(manifest)
    if DESTINATION.exists() and (
        not DESTINATION.is_dir() or DESTINATION.is_symlink()
    ):
        raise RuntimeError(f"Unsafe production directory: {DESTINATION}")

    staging_parent = SOURCE_DIR.parent
    with tempfile.TemporaryDirectory(
        prefix=".tsubaki-face-install-", dir=staging_parent
    ) as temporary:
        staging_dir = Path(temporary)
        for filename, source in manifest.items():
            staged = staging_dir / filename
            shutil.copy2(source, staged)
            load_validated_layer(staged, filename.split("_")[1])

        archived = archive_obsolete_shared_faces()
        install_staged_files(staging_dir, tuple(manifest))

    print(
        f"Installed {len(manifest)} reviewed Tsubaki face layers into "
        f"{DESTINATION}"
    )
    if archived:
        print(
            f"Archived {len(archived)} obsolete shared face files into "
            f"{ARCHIVE_DIR}"
        )
    else:
        print("No obsolete shared Tsubaki face files required archiving")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
