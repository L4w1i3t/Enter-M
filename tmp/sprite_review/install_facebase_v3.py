from __future__ import annotations

import hashlib
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = Path(__file__).resolve().parent / "facebase_v3"
SPRITE_ROOT = PROJECT_ROOT / "game" / "mod_assets" / "char_sprites"
EXPRESSIONS = (
    "afraid",
    "angry",
    "annoyed",
    "crying",
    "curious",
    "determined",
    "disgusted",
    "embarrassed",
    "empty",
    "frustrated",
    "happy",
    "nervous",
    "panicked",
    "sad",
    "shocked",
    "smug",
    "teasing",
    "thinking",
    "unamused",
    "worried",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


installed: list[str] = []
for character in ("asahina", "matsuda"):
    source = SOURCE_ROOT / character
    destination = SPRITE_ROOT / character
    names = [
        "neut_face_base.png",
        "neut_uniform_face_base.png",
        "face_neut_casual.png",
        "face_neut_uniform.png",
        *(f"face_{expression}.png" for expression in EXPRESSIONS),
    ]
    for name in names:
        source_path = source / name
        destination_path = destination / name
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        shutil.copyfile(source_path, destination_path)
        if sha256(source_path) != sha256(destination_path):
            raise RuntimeError(f"Copy verification failed: {destination_path}")
        installed.append(str(destination_path.relative_to(PROJECT_ROOT)))

print(f"Installed and hash-verified {len(installed)} sprite assets.")
print("\n".join(installed))
