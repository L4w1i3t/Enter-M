#!/usr/bin/env python3
"""Validate and transactionally install Matsuda's clean-room sprite rebuild.

The installer accepts only the 42 staged face layers and five staged pose
sprites produced by the fresh Matsuda builders. It binds every staged file and
canonical base to the builders' SHA-256 provenance, validates a complete
candidate directory, and then performs file-by-file atomic replacement with
rollback. Unrelated Matsuda assets such as ``convention_fullbody.png`` are left
untouched.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SPRITE_DIR = ROOT / "game" / "mod_assets" / "char_sprites" / "matsuda"
FACE_STAGE = ROOT / "tmp" / "matsuda_rebuild_fresh" / "faces"
POSE_STAGE = ROOT / "tmp" / "matsuda_rebuild_fresh" / "poses"
FACE_REPORT = ROOT / "tmp" / "matsuda_rebuild_fresh" / "face_build_metrics.json"
POSE_REPORT = POSE_STAGE / "provenance_metrics.json"
VALIDATOR = ROOT / "tools" / "validate_matsuda_sprites.py"
DEFINITIONS = ROOT / "game" / "mod_assets" / "def_characters.rpy"
CANVAS_SIZE = (1023, 1537)

TOKENS = (
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
OUTFITS = ("casual", "uniform")
FACE_NAMES = tuple(f"face_{token}_{outfit}.png" for outfit in OUTFITS for token in TOKENS)
POSE_NAMES = (
    "pose_facepalm_uniform.png",
    "pose_chuuni_uniform.png",
    "pose_shrug_uniform.png",
    "pose_laughing_casual.png",
    "pose_laughing_uniform.png",
)
BASE_NAMES = ("neutral.png", "neut_uniform.png")


def load_runtime_png(path: Path) -> np.ndarray:
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"Missing or unsafe PNG: {path}")
    with Image.open(path) as image:
        if image.mode != "RGBA" or image.size != CANVAS_SIZE:
            raise RuntimeError(
                f"Expected RGBA {CANVAS_SIZE}, got {image.mode} {image.size}: {path}"
            )
        pixels = np.asarray(image, dtype=np.uint8).copy()
    hidden_rgb = (pixels[:, :, 3] == 0) & np.any(pixels[:, :, :3] != 0, axis=2)
    if np.any(hidden_rgb):
        raise RuntimeError(f"Transparent pixels retain RGB data: {path}")
    return pixels


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"Missing or unsafe provenance report: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Cannot read provenance report {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"Provenance report is not an object: {path}")
    return payload


def provenance_hashes() -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    face_report = load_json(FACE_REPORT)
    pose_report = load_json(POSE_REPORT)
    try:
        face_hashes = dict(face_report["outputs"]["sha256"])
        pose_hashes = {
            name: record["output"]["sha256"]
            for name, record in pose_report["poses"].items()
        }
        base_hashes = {}
        for name in BASE_NAMES:
            relative = f"game/mod_assets/char_sprites/matsuda/{name}"
            face_hash = face_report["inputs"][relative]["sha256"]
            pose_hash = pose_report["canonical_bases"][name]["sha256"]
            if face_hash != pose_hash:
                raise RuntimeError(
                    f"Builders disagree about canonical base {name}: "
                    f"face={face_hash}, pose={pose_hash}"
                )
            base_hashes[name] = face_hash
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError(f"Malformed Matsuda provenance report: {exc}") from exc

    if set(face_hashes) != set(FACE_NAMES):
        raise RuntimeError("Face provenance does not describe the exact 42-file set")
    if set(pose_hashes) != set(POSE_NAMES):
        raise RuntimeError("Pose provenance does not describe the exact five-file set")
    return face_hashes, pose_hashes, base_hashes


def copy_checked_png(source: Path, destination: Path, expected_hash: str) -> None:
    load_runtime_png(source)
    actual_hash = sha256_file(source)
    if actual_hash != expected_hash:
        raise RuntimeError(
            f"Provenance hash mismatch for {source}: "
            f"expected={expected_hash}, actual={actual_hash}"
        )
    shutil.copyfile(source, destination)


def atomic_install(source: Path, destination: Path) -> None:
    temporary = destination.with_name(f".{destination.name}.matsuda-install.tmp")
    shutil.copyfile(source, temporary)
    os.replace(temporary, destination)


def install_with_rollback(candidate: Path, names: tuple[str, ...]) -> None:
    backup = candidate / "_rollback"
    backup.mkdir()
    for name in names:
        destination = SPRITE_DIR / name
        if not destination.is_file() or destination.is_symlink():
            raise RuntimeError(f"Missing or unsafe runtime destination: {destination}")
        shutil.copyfile(destination, backup / name)

    installed: list[str] = []
    try:
        for name in names:
            atomic_install(candidate / name, SPRITE_DIR / name)
            installed.append(name)
    except OSError as install_error:
        rollback_errors: list[str] = []
        for name in reversed(installed):
            try:
                atomic_install(backup / name, SPRITE_DIR / name)
            except OSError as rollback_error:
                rollback_errors.append(f"{name}: {rollback_error}")
        if rollback_errors:
            raise RuntimeError(
                "Matsuda install failed and rollback was incomplete: "
                + "; ".join(rollback_errors)
            ) from install_error
        raise RuntimeError("Matsuda install failed; prior files were restored") from install_error


def main() -> None:
    face_hashes, pose_hashes, base_hashes = provenance_hashes()
    expected_faces = set(FACE_NAMES)
    staged_faces = {path.name for path in FACE_STAGE.glob("face_*.png") if path.is_file()}
    if staged_faces != expected_faces:
        missing = sorted(expected_faces - staged_faces)
        unexpected = sorted(staged_faces - expected_faces)
        raise RuntimeError(f"Face staging mismatch; missing={missing}, unexpected={unexpected}")
    staged_poses = {
        path.name for path in POSE_STAGE.glob("pose_*.png") if path.is_file()
    }
    expected_poses = set(POSE_NAMES)
    if staged_poses != expected_poses:
        missing = sorted(expected_poses - staged_poses)
        unexpected = sorted(staged_poses - expected_poses)
        raise RuntimeError(f"Pose staging mismatch; missing={missing}, unexpected={unexpected}")

    candidate_parent = ROOT / "tmp" / "matsuda_rebuild_fresh"
    candidate_parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="install_candidate_", dir=candidate_parent) as temporary:
        candidate = Path(temporary)
        for name in BASE_NAMES:
            copy_checked_png(SPRITE_DIR / name, candidate / name, base_hashes[name])
        for name in FACE_NAMES:
            copy_checked_png(FACE_STAGE / name, candidate / name, face_hashes[name])
        for name in POSE_NAMES:
            copy_checked_png(POSE_STAGE / name, candidate / name, pose_hashes[name])

        command = (
            sys.executable,
            str(VALIDATOR),
            "--sprite-root",
            str(candidate),
            "--definitions",
            str(DEFINITIONS),
        )
        subprocess.run(command, cwd=ROOT, check=True)

        install_with_rollback(candidate, (*BASE_NAMES, *FACE_NAMES, *POSE_NAMES))

    print(
        "Installed Matsuda's 2 bases, "
        f"{len(FACE_NAMES)} face layers, and {len(POSE_NAMES)} poses."
    )


if __name__ == "__main__":
    main()
