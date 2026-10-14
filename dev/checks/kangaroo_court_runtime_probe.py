"""Isolated visual integration probe for the 2026-10-12 courtroom refresh.

Default invocation only prepares the fixture. Add --run after final assets and
definitions are installed. No full-project code is loaded and no story is activated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

PROJECT = Path(__file__).resolve().parents[2]
WORK = PROJECT / "tmp/kangaroo_court_refresh_2026_10_12"
EVIDENCE = PROJECT / "docs/assets/kangaroo_court/refresh_2026-10-12/runtime"
SDK = PROJECT.parents[1] / "RenPy 8/matsupy-sdk-860"

BACKGROUNDS = [
    "bg kc car highway day", "bg kc lobby day", "bg kc lobby panic",
    "bg kc courtroom overview", "bg kc prosecution bench", "bg kc defense bench",
    "bg kc witness stand", "bg kc judge bench",
]
PORTRAITS = [
    ("kc himeko " + pose, "bg kc prosecution bench", "kc_desk prosecution")
    for pose in ("neutral", "objection", "concerned", "shaken")
] + [
    ("kc stan dard " + pose, "bg kc defense bench", "kc_desk defense")
    for pose in ("neutral", "objection", "concerned")
] + [("kc naoto mori neutral", "bg kc witness stand", "kc_desk witness")] + [
    ("kc judge " + pose, "bg kc judge bench", "kc_desk judge")
    for pose in ("neutral", "stern", "surprised")
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def shared_snapshot():
    roots = [PROJECT / "game/saves", Path(os.environ["APPDATA"]) / "RenPy/ENTERM",
             Path(os.environ["APPDATA"]) / "RenPy/tokens"]
    return {str(root): {str(p.relative_to(root)): {
        "sha256": digest(p), "mtime_ns": p.stat().st_mtime_ns,
    } for p in sorted(root.rglob("*")) if p.is_file()} if root.exists() else None
        for root in roots}


def prepare():
    fixture = WORK / "fixture"
    game = fixture / "game"
    game.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    car = PROJECT / "game/assets/backgrounds/kangaroo_court/car_highway_day.png"
    car_baseline = WORK / "protected_car_sha256.txt"
    if car_baseline.exists():
        assert digest(car) == car_baseline.read_text(encoding="ascii").strip(), "Excluded car background changed."
    else:
        car_baseline.write_text(digest(car) + "\n", encoding="ascii")
    common = WORK / "common"
    if not common.exists():
        shutil.copytree(SDK / "renpy/common", common,
                        ignore=shutil.ignore_patterns("*.rpyc", "*.rpymc", "__pycache__"))
    definitions = PROJECT / "game/addons/Character Stories/kangaroo_court_assets.rpy"
    shutil.copy2(definitions, game / "kangaroo_court_assets.rpy")
    sources = [definitions]
    for relative in ("assets/backgrounds/kangaroo_court", "assets/characters/kangaroo_court",
                     "assets/gui/kangaroo_court"):
        for src in sorted((PROJECT / "game" / relative).glob("*.png")):
            target = game / relative / src.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)
            sources.append(src)
    write_json(EVIDENCE / "source_hashes.json", {
        str(p.relative_to(PROJECT)): digest(p) for p in sources})
    launcher_text = (SDK / "matsupy.py").read_text(encoding="utf-8")
    launcher_text = launcher_text.rsplit('if __name__ == "__main__":', 1)[0]
    launcher_text += r'''
# Private launcher substitutions apply only to this copied QA entrypoint.
import atexit
import json
_qa_root = os.path.realpath(os.environ["KC_QA_WORK"])
_qa_evidence = os.path.realpath(os.environ["KC_QA_EVIDENCE"])
_qa_run = os.path.realpath(os.environ["KC_QA_RUN"])
_qa_sdk = os.environ["KC_QA_SDK"]
_qa_blocked = []

def path_to_renpy_base():
    return _qa_sdk

def path_to_common(renpy_base):
    return os.path.join(_qa_root, "common")

def path_to_saves(gamedir, save_directory=None):
    return os.path.join(_qa_run, "private", save_directory or "saves")

def _qa_inside(path):
    if not isinstance(path, (str, bytes, os.PathLike)):
        return True
    value = os.path.normcase(os.path.realpath(os.fsdecode(path)))
    return any(os.path.commonpath([value, allowed]) == allowed
               for allowed in (os.path.normcase(_qa_root), os.path.normcase(_qa_evidence)))

def _qa_audit(event, args):
    paths = []
    if event == "open":
        path, mode, flags = args
        if (mode and any(c in mode for c in "wax+")) or flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
            paths = [path]
    elif event in ("os.remove", "os.rmdir", "os.mkdir", "os.chmod", "os.utime"):
        paths = [args[0]]
        if event == "os.remove" and not os.path.exists(args[0]):
            return
    elif event in ("os.rename", "os.replace"):
        paths = args[:2]
    for path in paths:
        if not _qa_inside(path):
            _qa_blocked.append({"event": event, "path": str(path)})
            raise PermissionError("Courtroom QA refused external mutation: " + str(path))

def _qa_write_audit():
    with open(os.path.join(_qa_run, "write_guard.json"), "w", encoding="utf-8") as handle:
        json.dump({"blocked": _qa_blocked}, handle, indent=2)

sys.dont_write_bytecode = True
sys.addaudithook(_qa_audit)
atexit.register(_qa_write_audit)
main()
'''
    launcher = WORK / "kc_refresh_probe.py"
    launcher.write_text(launcher_text, encoding="utf-8")
    fixture_script = r'''
init -100 python:
    import os
    import json
    import renpy as _kc_engine
    _kc_engine.safe_mode_checked = True
    config.name = "Kangaroo Court isolated visual probe"
    config.version = "2026-10-12"
    config.screen_width = 1280
    config.screen_height = 720
    config.physical_width = 1280
    config.physical_height = 720
    config.save_directory = "KCRefresh20261012"
    config.window_title = "Kangaroo Court asset QA"
    config.has_sound = False
    config.has_music = False
    config.has_voice = False
    config.autosave_on_quit = False
    config.autosave_on_choice = False
    config.autosave_frequency = None
    config.has_sync = False
    config.rollback_enabled = False
    config.mouse = {"default": [("invisible.png", 0, 0)]}
    _preferences.fullscreen = False
    _preferences.renderer = "gl2"

init python:
    kc_qa_backgrounds = __BACKGROUNDS__
    kc_qa_portraits = __PORTRAITS__

    def kc_qa_assert_private():
        private_root = os.path.normcase(os.path.realpath(os.environ["KC_QA_RUN"]))
        active = [config.savedir] + list(config.extra_savedirs)
        active.extend(location.directory for location in renpy.loadsave.location.locations)
        active.append(renpy.savetoken.token_dir)
        assert os.environ.get("MATSU_FRESH_RUN") == "1"
        assert renpy.game.args.savedir
        for path in active:
            if path is not None:
                value = os.path.normcase(os.path.realpath(path))
                assert os.path.commonpath([private_root, value]) == private_root, path
        assert not renpy.has_label("cs_mom_01")
        for name in kc_qa_backgrounds + [p[0] for p in kc_qa_portraits] + [p[2] for p in kc_qa_portraits]:
            assert renpy.has_image(name, exact=True), name
        return active

    def kc_qa_capture(name):
        path = os.path.join(os.environ["KC_QA_RUN"], name + ".png")
        renpy.pause(0.12, hard=True)
        assert renpy.screenshot(path), path
        return path

label main_menu:
    jump start

label start:
    window hide
    python:
        renpy.pause(0.1, hard=True)
        kc_report = {"active_save_paths": kc_qa_assert_private(), "captures": [],
                     "renderer": renpy.get_renderer_info(),
                     "virtual_resolution": [config.screen_width, config.screen_height],
                     "engine": renpy.version_string, "audio": "dummy",
                     "scope": "Copied production static assets only; no main-story, trial UI, pacing, packaging, or old-save coverage."}
        for kc_bg in kc_qa_backgrounds:
            renpy.scene()
            renpy.show(kc_bg)
            kc_report["captures"].append(kc_qa_capture(kc_bg.replace(" ", "_")))
        for kc_actor, kc_bg, kc_desk in kc_qa_portraits:
            renpy.scene()
            renpy.show(kc_bg)
            renpy.show(kc_actor)
            kc_report["captures"].append(kc_qa_capture(kc_actor.replace(" ", "_")))
            if os.environ.get("KC_QA_DESK_LAYERS") == "1":
                assert renpy.has_image(kc_desk, exact=True), kc_desk
                renpy.show(kc_desk, zorder=10)
                kc_report["captures"].append(kc_qa_capture(kc_actor.replace(" ", "_") + "_desk"))
        for kc_desk in sorted(set(p[2] for p in kc_qa_portraits)):
            renpy.scene()
            renpy.show("qa_black", what=Solid("#000000"))
            renpy.show(kc_desk, zorder=10)
            kc_report["captures"].append(kc_qa_capture(kc_desk.replace(" ", "_") + "_mask_diagnostic"))
        with open(os.path.join(os.environ["KC_QA_RUN"], "runtime.json"), "w", encoding="utf-8") as kc_handle:
            json.dump(kc_report, kc_handle, indent=2)
        renpy.quit(relaunch=False, status=0, save=False)
'''
    fixture_script = fixture_script.replace("__BACKGROUNDS__", repr(BACKGROUNDS)).replace("__PORTRAITS__", repr(PORTRAITS))
    (game / "probe.rpy").write_text(fixture_script, encoding="utf-8")
    # A transparent cursor avoids capturing the host pointer over the art.
    from PIL import Image
    Image.new("RGBA", (1, 1)).save(game / "invisible.png")
    print(f"Prepared {fixture}")
    return fixture, launcher


def run(fixture, launcher, desk_layers):
    run_dir = EVIDENCE / time.strftime("run_%Y%m%d_%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=False)
    private = run_dir / "private/saves"
    private.mkdir(parents=True)
    run_temp = run_dir / "private/temp"
    run_temp.mkdir(parents=True)
    before = shared_snapshot()
    write_json(run_dir / "shared_before.json", before)
    env = dict(os.environ, MATSU_FRESH_RUN="1", PYTHONDONTWRITEBYTECODE="1",
               SDL_AUDIODRIVER="dummy", RENPY_RENDERER="gl2", KC_QA_WORK=str(WORK),
               KC_QA_EVIDENCE=str(EVIDENCE), KC_QA_RUN=str(run_dir), KC_QA_SDK=str(SDK),
               KC_QA_DESK_LAYERS="1" if desk_layers else "0", TEMP=str(run_temp), TMP=str(run_temp))
    command = [str(SDK / "lib/py3-windows-x86_64/python.exe"), "-B", str(launcher),
               str(fixture), "run", "--savedir", str(private)]
    started = time.monotonic()
    with (run_dir / "stdout.txt").open("wb") as out, (run_dir / "stderr.txt").open("wb") as err:
        proc = subprocess.Popen(command, cwd=fixture, env=env, stdout=out, stderr=err,
                                creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            returncode = proc.wait(timeout=120)
        except subprocess.TimeoutExpired:
            proc.terminate()
            returncode = proc.wait(timeout=10)
    after = shared_snapshot()
    write_json(run_dir / "shared_after.json", after)
    summary = {"exit_code": returncode, "elapsed_seconds": round(time.monotonic() - started, 2),
               "shared_unchanged": before == after,
               "shared_file_count": sum(len(v or {}) for v in before.values()),
               "run_directory": str(run_dir), "desk_layers": desk_layers,
               "command": command, "fresh_run": True}
    write_json(run_dir / "summary.json", summary)
    for name in ("log.txt", "traceback.txt", "errors.txt"):
        source = fixture / name
        if source.exists():
            shutil.copy2(source, run_dir / name)
    print(json.dumps(summary, indent=2))
    assert before == after, "Shared save/token state changed; do not reset it."
    assert returncode == 0, "Engine probe failed; inspect its logs."
    report = json.loads((run_dir / "runtime.json").read_text(encoding="utf-8"))
    assert len(report["captures"]) == 8 + 11 * (2 if desk_layers else 1) + 4
    return run_dir


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="Launch after copying final installed assets.")
    parser.add_argument("--desk-layers", action="store_true", help="Also capture front-desk occlusion for every pose.")
    args = parser.parse_args()
    fixture, launcher = prepare()
    if args.run:
        run(fixture, launcher, args.desk_layers)
