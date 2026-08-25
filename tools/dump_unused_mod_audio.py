from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


AUDIO_EXTENSIONS = {
    ".aac",
    ".flac",
    ".m4a",
    ".mp3",
    ".ogg",
    ".opus",
    ".wav",
}

TEXT_EXTENSIONS = {
    ".bat",
    ".cfg",
    ".cmd",
    ".css",
    ".csv",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".rpy",
    ".rpym",
    ".rpyw",
    ".toml",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

DEFAULT_MOD_AUDIO_ROOTS = (
    Path("game/mod_assets"),
    Path("game/addons"),
)

DEFAULT_DEFINITION_FILES = (
    Path("game/mod_assets/misc_def.rpy"),
    Path("game/definitions.rpy"),
)

DEFAULT_DUMP_DIR = Path("game/mod_assets/dump")
DEFAULT_DUMP_SUBDIR = Path("_unused_audio")

IGNORED_DIR_NAMES = {
    ".git",
    ".renpy-temp",
    "__pycache__",
}

FILENAME_BOUNDARY_CHARS = frozenset("abcdefghijklmnopqrstuvwxyz0123456789_-.")


@dataclass(frozen=True)
class TextCorpus:
    all_text: str
    definitions_text: str
    scanned_file_count: int


@dataclass(frozen=True)
class AudioDecision:
    source: Path
    target: Path
    reason: str
    matched_token: str | None = None


def normalize_for_search(value: str) -> str:
    return value.replace("\\", "/").casefold()


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def has_ignored_part(path: Path, root: Path) -> bool:
    try:
        relative_parts = path.relative_to(root).parts
    except ValueError:
        relative_parts = path.parts

    return any(part in IGNORED_DIR_NAMES for part in relative_parts)


def read_text(path: Path) -> str:
    data = path.read_bytes()

    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue

    return data.decode("utf-8", errors="replace")


def iter_text_files(root: Path, dump_dir: Path) -> list[Path]:
    files: list[Path] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if has_ignored_part(path, root):
            continue
        if is_relative_to(path, dump_dir):
            continue
        if path.suffix.casefold() not in TEXT_EXTENSIONS:
            continue

        files.append(path)

    return files


def build_corpus(root: Path, dump_dir: Path, definition_files: tuple[Path, ...]) -> TextCorpus:
    all_chunks: list[str] = []
    definition_chunks: list[str] = []
    text_files = iter_text_files(root, dump_dir)

    definition_set = {path.resolve() for path in definition_files if path.exists()}

    for path in text_files:
        try:
            text = read_text(path)
        except OSError as exc:
            print(f"Warning: could not read {path}: {exc}", file=sys.stderr)
            continue

        normalized = normalize_for_search(text)
        all_chunks.append(normalized)

        if path.resolve() in definition_set:
            definition_chunks.append(normalized)

    return TextCorpus(
        all_text="\n".join(all_chunks),
        definitions_text="\n".join(definition_chunks),
        scanned_file_count=len(text_files),
    )


def iter_audio_candidates(root: Path, mod_audio_roots: tuple[Path, ...], dump_dir: Path) -> list[Path]:
    candidates: list[Path] = []
    resolved_dump_dir = dump_dir.resolve()

    for mod_root in mod_audio_roots:
        if not mod_root.exists():
            continue

        for path in mod_root.rglob("*"):
            if not path.is_file():
                continue
            if is_relative_to(path.resolve(), resolved_dump_dir):
                continue
            if path.suffix.casefold() not in AUDIO_EXTENSIONS:
                continue

            candidates.append(path)

    return sorted(set(candidates), key=lambda item: normalize_for_search(str(item)))


def search_tokens(root: Path, game_dir: Path, audio_file: Path) -> list[str]:
    tokens: list[str] = []

    def add(value: str) -> None:
        normalized = normalize_for_search(value)
        if normalized and normalized not in tokens:
            tokens.append(normalized)

    add(str(audio_file))
    add(audio_file.as_posix())

    try:
        repo_relative = audio_file.relative_to(root)
        add(str(repo_relative))
        add(repo_relative.as_posix())
    except ValueError:
        pass

    try:
        game_relative = audio_file.relative_to(game_dir)
        add(str(game_relative))
        add(game_relative.as_posix())
    except ValueError:
        pass

    add(audio_file.name)

    return tokens


def token_matches(token: str, haystack: str) -> bool:
    if "/" in token:
        return token in haystack

    index = haystack.find(token)
    while index != -1:
        before = haystack[index - 1] if index > 0 else ""
        after_index = index + len(token)
        after = haystack[after_index] if after_index < len(haystack) else ""

        before_is_boundary = not before or before not in FILENAME_BOUNDARY_CHARS
        after_is_boundary = not after or after not in FILENAME_BOUNDARY_CHARS
        if before_is_boundary and after_is_boundary:
            return True

        index = haystack.find(token, index + 1)

    return False


def first_matching_token(tokens: list[str], haystack: str) -> str | None:
    for token in tokens:
        if token_matches(token, haystack):
            return token
    return None


def unique_target(path: Path) -> Path:
    if not path.exists():
        return path

    for index in range(1, 10000):
        candidate = path.with_name(f"{path.stem}__{index}{path.suffix}")
        if not candidate.exists():
            return candidate

    raise RuntimeError(f"Could not find an unused target name for {path}")


def target_for_audio(root: Path, game_dir: Path, dump_dir: Path, audio_file: Path) -> Path:
    try:
        relative = audio_file.relative_to(game_dir)
    except ValueError:
        relative = audio_file.relative_to(root)

    return unique_target(dump_dir / DEFAULT_DUMP_SUBDIR / relative)


def classify_audio(
    root: Path,
    game_dir: Path,
    dump_dir: Path,
    corpus: TextCorpus,
    audio_files: list[Path],
) -> tuple[list[AudioDecision], list[AudioDecision]]:
    keep: list[AudioDecision] = []
    move: list[AudioDecision] = []

    for audio_file in audio_files:
        tokens = search_tokens(root, game_dir, audio_file)
        definition_match = first_matching_token(tokens, corpus.definitions_text)
        if definition_match:
            keep.append(AudioDecision(audio_file, audio_file, "defined", definition_match))
            continue

        reference_match = first_matching_token(tokens, corpus.all_text)
        if reference_match:
            keep.append(AudioDecision(audio_file, audio_file, "referenced", reference_match))
            continue

        move.append(
            AudioDecision(
                audio_file,
                target_for_audio(root, game_dir, dump_dir, audio_file),
                "unused",
            )
        )

    return keep, move


def move_audio(decisions: list[AudioDecision]) -> None:
    for decision in decisions:
        decision.target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(decision.source), str(decision.target))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Move unused mod audio into game/mod_assets/dump/_unused_audio. "
            "A mod audio file is kept if it is defined in misc_def.rpy or definitions.rpy, "
            "or if any scanned text file references its path or filename."
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would move without changing files.",
    )
    parser.add_argument(
        "--dump-dir",
        type=Path,
        default=DEFAULT_DUMP_DIR,
        help="Dump directory to move unused audio under. Defaults to game/mod_assets/dump.",
    )
    parser.add_argument(
        "--include-game-root",
        action="store_true",
        help=(
            "Also scan loose audio directly under game/, excluding vanilla-style game/bgm "
            "and game/sfx folders. The default only scans game/mod_assets and game/addons."
        ),
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="List kept files and the token that protected each one.",
    )
    return parser.parse_args()


def find_project_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "game").is_dir() and (candidate / "MODCEN_MARK").exists():
            return candidate.resolve()

    return Path.cwd().resolve()


def main() -> int:
    args = parse_args()
    root = find_project_root(Path(__file__).resolve().parent)
    game_dir = root / "game"
    dump_dir = (root / args.dump_dir).resolve()
    definition_files = tuple((root / path).resolve() for path in DEFAULT_DEFINITION_FILES)

    mod_audio_roots = tuple((root / path).resolve() for path in DEFAULT_MOD_AUDIO_ROOTS)
    if args.include_game_root:
        mod_audio_roots = mod_audio_roots + (game_dir.resolve(),)

    audio_files = iter_audio_candidates(root, mod_audio_roots, dump_dir)
    if args.include_game_root:
        vanilla_roots = {
            (game_dir / "bgm").resolve(),
            (game_dir / "sfx").resolve(),
        }
        audio_files = [
            path
            for path in audio_files
            if not any(is_relative_to(path.resolve(), vanilla_root) for vanilla_root in vanilla_roots)
        ]

    corpus = build_corpus(root, dump_dir, definition_files)
    keep, move = classify_audio(root, game_dir, dump_dir, corpus, audio_files)

    action = "Would move" if args.dry_run else "Moving"
    print(f"Scanned text files: {corpus.scanned_file_count}")
    print(f"Scanned mod audio files: {len(audio_files)}")
    print(f"Kept: {len(keep)}")
    print(f"{action}: {len(move)}")

    if args.verbose and keep:
        print("\nKept audio:")
        for decision in keep:
            rel_source = decision.source.relative_to(root)
            print(f"  keep {rel_source} ({decision.reason}: {decision.matched_token})")

    if move:
        print("\nUnused audio:")
        for decision in move:
            rel_source = decision.source.relative_to(root)
            rel_target = decision.target.relative_to(root)
            print(f"  {rel_source} -> {rel_target}")

    if not args.dry_run:
        move_audio(move)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
