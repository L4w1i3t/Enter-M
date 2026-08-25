from __future__ import annotations

import hashlib
import os
import zlib
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OBJECT_ROOT = PROJECT_ROOT / ".git" / "objects"
OUTPUT_ROOT = Path(__file__).resolve().parent / "prechange"
COMMIT = "dd99eb063a967ee39b658a580d2e41157637554d"
TARGETS = (
    "game/mod_assets/char_sprites/asahina",
    "game/mod_assets/char_sprites/matsuda",
)
RECOVERED_BLOBS = {
    "asahina/neut_uniform_face_base.png": "62a73c9fa6dafeb2f870a6a94309b5ee2d0952e7",
    "matsuda/neut_face_base.png": "f7efd8ba1727d5f1392add7678821022df5d2262",
    "matsuda/neut_uniform_face_base.png": "230e491596b46d8be8ffc537211a11c0a4500a8f",
}


def read_object(object_id: str) -> tuple[str, bytes]:
    directory = OBJECT_ROOT / object_id[:2]
    stem = object_id[2:]
    candidates = [directory / stem, *sorted(directory.glob(f"{stem}.sync-conflict-*"))]
    path = next((candidate for candidate in candidates if candidate.is_file()), None)
    if path is None:
        raise FileNotFoundError(f"Missing loose Git object {object_id}")
    packed = zlib.decompress(path.read_bytes())
    header, content = packed.split(b"\0", 1)
    kind, size_text = header.decode("ascii").split(" ", 1)
    if len(content) != int(size_text):
        raise ValueError(f"Wrong size for {object_id}")
    actual = hashlib.sha1(header + b"\0" + content).hexdigest()
    if actual != object_id:
        raise ValueError(f"Hash mismatch for {path}: {actual} != {object_id}")
    return kind, content


def tree_entries(object_id: str) -> dict[str, tuple[str, str]]:
    kind, content = read_object(object_id)
    if kind != "tree":
        raise TypeError(f"Expected tree {object_id}, got {kind}")
    entries: dict[str, tuple[str, str]] = {}
    position = 0
    while position < len(content):
        separator = content.index(b"\0", position)
        mode_and_name = content[position:separator]
        mode, name = mode_and_name.split(b" ", 1)
        child_id = content[separator + 1 : separator + 21].hex()
        entries[name.decode("utf-8", errors="surrogateescape")] = (
            mode.decode("ascii"),
            child_id,
        )
        position = separator + 21
    return entries


def resolve(root_tree: str, relative_path: str) -> tuple[str, str]:
    current_id = root_tree
    current_mode = "40000"
    for part in relative_path.split("/"):
        current_mode, current_id = tree_entries(current_id)[part]
    return current_mode, current_id


def extract_entry(mode: str, object_id: str, destination: Path) -> None:
    if mode.startswith("04") or mode == "40000":
        destination.mkdir(parents=True, exist_ok=True)
        for name, (child_mode, child_id) in tree_entries(object_id).items():
            extract_entry(child_mode, child_id, destination / name)
        return
    kind, content = read_object(object_id)
    if kind != "blob":
        raise TypeError(f"Expected blob {object_id}, got {kind}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)


commit_kind, commit_content = read_object(COMMIT)
if commit_kind != "commit":
    raise TypeError(f"Expected commit {COMMIT}, got {commit_kind}")
tree_id = commit_content.splitlines()[0].decode("ascii").removeprefix("tree ")
for target in TARGETS:
    target_mode, target_id = resolve(tree_id, target)
    extract_entry(target_mode, target_id, OUTPUT_ROOT / target)
    print(f"Recovered {target}")

for relative_path, object_id in RECOVERED_BLOBS.items():
    object_kind, object_content = read_object(object_id)
    if object_kind != "blob":
        raise TypeError(f"Expected blob {object_id}, got {object_kind}")
    destination = OUTPUT_ROOT / "recovered_layers" / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(object_content)
    print(f"Recovered loose blob {relative_path}")
