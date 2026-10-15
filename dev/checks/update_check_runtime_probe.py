"""Run the production title-screen update indicator in an isolated GL2 fixture.

The fixture copies only title UI dependencies and the update checker. Release
metadata is injected; threading and dispatch still use the real engine APIs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time


PROJECT = Path(__file__).resolve().parents[2]
WORK = PROJECT / "tmp/update-check-2026-10-14"
EVIDENCE = PROJECT / "docs/engineering/evidence/update-check-2026-10-14"
SDK = PROJECT.parents[1] / "RenPy 8/matsupy-sdk-860"
SOURCES = (
    "gui.rpy", "room_menu_theme.rpy", "main_menu_fx.rpy",
    "main_menu_room.rpy", "update_check.rpy",
    "python-packages/enter_m_updates.py",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def shared_snapshot():
    roots = (PROJECT / "game/saves", Path(os.environ["APPDATA"]) / "RenPy/ENTERM",
             Path(os.environ["APPDATA"]) / "RenPy/tokens")
    return {str(root): {str(path.relative_to(root)): {
        "sha256": digest(path), "mtime_ns": path.stat().st_mtime_ns,
    } for path in sorted(root.rglob("*")) if path.is_file()} if root.exists() else None
        for root in roots}


LAUNCHER = r'''
# These overrides apply only to the copied QA entrypoint.
import atexit
import json
_qa_work = os.path.realpath(os.environ["UPDATE_QA_WORK"])
_qa_evidence = os.path.realpath(os.environ["UPDATE_QA_EVIDENCE"])
_qa_run = os.path.realpath(os.environ["UPDATE_QA_RUN"])
_qa_blocked = []

def path_to_renpy_base():
    return os.environ["UPDATE_QA_SDK"]

def path_to_common(renpy_base):
    return os.path.join(_qa_work, "common")

def path_to_saves(gamedir, save_directory=None):
    return os.path.join(_qa_run, "private", save_directory or "saves")

def _qa_inside(path):
    if not isinstance(path, (str, bytes, os.PathLike)):
        return True
    value = os.path.normcase(os.path.realpath(os.fsdecode(path)))
    return any(os.path.commonpath([value, allowed]) == allowed
               for allowed in (os.path.normcase(_qa_work), os.path.normcase(_qa_evidence)))

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
            raise PermissionError("Update QA refused external mutation: " + str(path))

def _qa_write_audit():
    with open(os.path.join(_qa_run, "write_guard.json"), "w", encoding="utf-8") as handle:
        json.dump({"blocked": _qa_blocked}, handle, indent=2)

sys.dont_write_bytecode = True
sys.addaudithook(_qa_audit)
atexit.register(_qa_write_audit)
main()
'''


FIXTURE = r'''
init -200 python:
    import os
    import json
    import time
    import threading
    import renpy as _qa_engine
    _qa_engine.safe_mode_checked = True
    config.name = "ENTER M update indicator QA"
    config.version = __VERSION__
    config.save_directory = "UpdateCheck20261014"
    config.window_title = "ENTER M update indicator QA"
    config.has_sound = False
    config.has_music = False
    config.has_voice = False
    config.autosave_on_quit = False
    config.autosave_on_choice = False
    config.autosave_frequency = None
    config.has_sync = False
    config.rollback_enabled = False
    config.developer = False
    config.mouse = {"default": [("invisible.png", 0, 0)]}
    config.images_directory = None
    config.physical_width = 1280
    config.physical_height = 720
    _preferences.fullscreen = False
    _preferences.renderer = "gl2"
    persistent.enter_m_atmos_quality = "off"
    audio.uihover = None
    audio.uiselect = None

init python:
    # Menu prediction is unrelated to this focused indicator fixture.
    def illustrated_menu_predict():
        pass

    def illustrated_menu_stop_predict():
        pass

    def qa_assert_private():
        root = os.path.normcase(os.path.realpath(os.environ["UPDATE_QA_RUN"]))
        active = [config.savedir] + list(config.extra_savedirs)
        active.extend(location.directory for location in renpy.loadsave.location.locations)
        active.append(renpy.savetoken.token_dir)
        assert os.environ.get("MATSU_FRESH_RUN") == "1"
        assert renpy.game.args.savedir
        for path in active:
            if path is not None:
                value = os.path.normcase(os.path.realpath(path))
                assert os.path.commonpath([root, value]) == root, path
        assert not renpy.has_label("cs_mom_01")
        return active

    def qa_capture(name):
        path = os.path.join(os.environ["UPDATE_QA_RUN"], name + ".png")
        assert renpy.screenshot(path), path
        return path

label main_menu:
    jump start

label start:
    window hide
    python:
        renpy.pause(0.1, hard=True)
        qa_report = {
            "active_save_paths": qa_assert_private(),
            "renderer": renpy.get_renderer_info(),
            "virtual_resolution": [config.screen_width, config.screen_height],
            "engine": renpy.version_string,
            "audio": "dummy", "atmosphere": "off", "scenarios": [],
            "scope": "Copied production title UI and update checker; controlled release metadata with real worker/dispatch. No browser launch, packaging, full-story, or old-save coverage.",
        }
        __SCENARIOS__
        with open(os.path.join(os.environ["UPDATE_QA_RUN"], "runtime.json"), "w", encoding="utf-8") as qa_handle:
            json.dump(qa_report, qa_handle, indent=2)
        renpy.quit(relaunch=False, status=0, save=False)
'''


def prepare():
    fixture = WORK / "fixture"
    game = fixture / "game"
    game.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    common = WORK / "common"
    if not common.exists():
        shutil.copytree(SDK / "renpy/common", common,
                        ignore=shutil.ignore_patterns("*.rpyc", "*.rpymc", "__pycache__"))
    sources = []
    for relative in SOURCES:
        source = PROJECT / "game" / relative
        target = game / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        sources.append(source)
    for relative in ("assets/gui/menu/room_theme", "assets/gui/menu/illustrated/title"):
        for source in sorted((PROJECT / "game" / relative).glob("*")):
            if source.is_file():
                target = game / relative / source.name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
                sources.append(source)
    for relative in ("assets/gui/logo.png", "assets/fonts/Myanmar.otf",
                     "assets/fonts/NovaSquare-Regular.ttf", "assets/fonts/SF Automaton Extended.ttf"):
        source = PROJECT / "game" / relative
        target = game / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        sources.append(source)
    # Preserve the production base text/button styles without loading unrelated screens.
    screens = PROJECT / "game/screens.rpy"
    styles = screens.read_text(encoding="utf-8").split("style label_text", 1)[0]
    (game / "base_styles.rpy").write_text(styles, encoding="utf-8")
    sources.append(screens)
    atmosphere = PROJECT / "game/atmosphere.rpy"
    shader_source = atmosphere.read_text(encoding="utf-8").split("init -10 python:", 1)[1].split("init -9 python:", 1)[0]
    (game / "atmosphere_shaders.rpy").write_text("init -10 python:" + shader_source, encoding="utf-8")
    sources.append(atmosphere)
    options = PROJECT / "game/options.rpy"
    version = re.search(r'^define config.version = "([^"]+)"', options.read_text(encoding="utf-8"), re.M).group(1)
    sources.append(options)
    script = FIXTURE.replace("__VERSION__", repr(version)).replace("__SCENARIOS__", SCENARIOS.strip())
    (game / "probe.rpy").write_text(script, encoding="utf-8")
    launcher_text = (SDK / "matsupy.py").read_text(encoding="utf-8").rsplit('if __name__ == "__main__":', 1)[0]
    launcher = WORK / "update_probe.py"
    launcher.write_text(launcher_text + LAUNCHER, encoding="utf-8")
    from PIL import Image
    Image.new("RGBA", (1, 1)).save(game / "invisible.png")
    write_json(EVIDENCE / "source_hashes.json", {
        str(path.relative_to(PROJECT)): digest(path) for path in sources})
    print(f"Prepared {fixture}")
    return fixture, launcher


def run(fixture, launcher, live=False):
    run_dir = EVIDENCE / time.strftime("run_%Y%m%d_%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=False)
    private = run_dir / "private/saves"
    private.mkdir(parents=True)
    run_temp = run_dir / "private/temp"
    run_temp.mkdir(parents=True)
    before = shared_snapshot()
    write_json(run_dir / "shared_before.json", before)
    env = dict(os.environ, MATSU_FRESH_RUN="1", PYTHONDONTWRITEBYTECODE="1",
               SDL_AUDIODRIVER="dummy", RENPY_RENDERER="gl2", UPDATE_QA_WORK=str(WORK),
               UPDATE_QA_EVIDENCE=str(EVIDENCE), UPDATE_QA_RUN=str(run_dir), UPDATE_QA_SDK=str(SDK),
               UPDATE_QA_LIVE="1" if live else "0",
               TEMP=str(run_temp), TMP=str(run_temp))
    command = [str(SDK / "lib/py3-windows-x86_64/python.exe"), "-B", str(launcher),
               str(fixture), "run", "--savedir", str(private)]
    for name in ("traceback.txt", "errors.txt"):
        (fixture / name).unlink(missing_ok=True)
    started = time.monotonic()
    with (run_dir / "stdout.txt").open("wb") as out, (run_dir / "stderr.txt").open("wb") as err:
        process = subprocess.Popen(command, cwd=fixture, env=env, stdout=out, stderr=err,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            while process.poll() is None:
                if (fixture / "traceback.txt").exists() or (fixture / "errors.txt").exists():
                    raise RuntimeError("Fixture exception; preserve traceback without waiting on the error screen.")
                if time.monotonic() - started > 90:
                    raise TimeoutError("Fixture exceeded 90 seconds")
                time.sleep(0.25)
            returncode = process.returncode
        except (RuntimeError, TimeoutError):
            process.terminate()
            returncode = process.wait(timeout=10)
    after = shared_snapshot()
    write_json(run_dir / "shared_after.json", after)
    summary = {"exit_code": returncode, "elapsed_seconds": round(time.monotonic() - started, 2),
               "shared_unchanged": before == after,
               "shared_file_count": sum(len(value or {}) for value in before.values()),
               "run_directory": str(run_dir), "command": command, "fresh_run": True}
    write_json(run_dir / "summary.json", summary)
    for name in ("log.txt", "traceback.txt", "errors.txt"):
        source = fixture / name
        if source.exists():
            shutil.copy2(source, run_dir / name)
    print(json.dumps(summary, indent=2))
    assert before == after, "Shared save/token state changed; do not reset it."
    assert returncode == 0, "Engine probe failed; inspect its logs."
    assert json.loads((run_dir / "write_guard.json").read_text(encoding="utf-8")) == {"blocked": []}
    report = json.loads((run_dir / "runtime.json").read_text(encoding="utf-8"))
    assert len(report["scenarios"]) == (4 if live else 3)
    return run_dir


SCENARIOS = r'''
        qa_original_fetch = enter_m_updates.fetch_latest_release
        qa_main_thread = threading.get_ident()
        qa_cases = [("newer", "available", True), ("equal", "no_update", False),
                    ("offline", "unavailable", False)]
        if os.environ.get("UPDATE_QA_LIVE") == "1":
            qa_cases.append(("live_endpoint", "unavailable", False))
        for qa_case, qa_expected, qa_visible in qa_cases:
            qa_fetch_threads = []
            qa_finish_threads = []
            qa_http_errors = []
            def qa_fetch():
                qa_fetch_threads.append(threading.get_ident())
                if qa_case == "live_endpoint":
                    try:
                        return qa_original_fetch()
                    except Exception as error:
                        qa_http_errors.append({"type": type(error).__name__, "status": getattr(error, "code", None), "detail": str(error)})
                        raise
                time.sleep(0.15)
                if qa_case == "offline":
                    raise OSError("Controlled offline fixture")
                return {"tag_name": "v999.0.0" if qa_case == "newer" else "v" + config.version,
                        "draft": False, "prerelease": False}
            enter_m_updates.fetch_latest_release = qa_fetch
            enter_m_updates.checker = enter_m_updates.UpdateChecker()
            qa_original_finish = enter_m_updates.checker._finish
            def qa_finish(*args):
                qa_finish_threads.append(threading.get_ident())
                return qa_original_finish(*args)
            enter_m_updates.checker._finish = qa_finish
            renpy.show_screen("main_menu")
            qa_deadline = time.monotonic() + 15.0
            while enter_m_updates.checker.state in ("idle", "checking"):
                assert time.monotonic() < qa_deadline, (qa_case, "check did not finish")
                renpy.pause(0.05, hard=True)
            renpy.pause(0.9, hard=True)
            assert enter_m_updates.checker.state == qa_expected, (qa_case, enter_m_updates.checker.state)
            qa_widget = renpy.get_displayable("main_menu", "main_menu_update_available", base=True)
            assert (qa_widget is not None) == qa_visible, qa_case
            assert len(qa_fetch_threads) == 1 and qa_fetch_threads[0] != qa_main_thread, qa_fetch_threads
            assert qa_finish_threads == [qa_main_thread], qa_finish_threads
            qa_target = None
            if qa_visible:
                qa_target = qa_widget.action.url
                assert qa_target == enter_m_updates.RELEASES_URL
                assert qa_widget.style.xpos == 29 and qa_widget.style.ypos == 642
                assert renpy.render(qa_widget, 1280, 720, 1.0, 1.0).get_size() == (374, 32)
            if qa_case == "live_endpoint":
                assert len(qa_http_errors) == 1, qa_http_errors
                assert qa_http_errors[0]["type"] == "HTTPError" and qa_http_errors[0]["status"] == 404, qa_http_errors
            qa_shot = qa_capture(qa_case)
            # Visiting the title again must keep the session result and not refetch.
            renpy.hide_screen("main_menu")
            renpy.pause(0.05, hard=True)
            renpy.show_screen("main_menu")
            renpy.pause(0.1, hard=True)
            assert len(qa_fetch_threads) == 1, (qa_case, "duplicate release request")
            assert (renpy.get_displayable("main_menu", "main_menu_update_available") is not None) == qa_visible
            qa_report["scenarios"].append({
                "case": qa_case, "state": enter_m_updates.checker.state,
                "available_version": enter_m_updates.checker.available_version,
                "indicator_visible": qa_visible, "requests_after_revisit": len(qa_fetch_threads),
                "worker_was_background": True, "completion_was_main_thread": True,
                "release_url": qa_target, "http_errors": qa_http_errors, "screenshot": qa_shot,
            })
            renpy.hide_screen("main_menu")
            renpy.pause(0.05, hard=True)
        enter_m_updates.fetch_latest_release = qa_original_fetch
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="Launch the copied title-screen probe.")
    parser.add_argument("--live", action="store_true", help="Also check graceful failure for the currently empty public feed through the SDK.")
    args = parser.parse_args()
    fixture, launcher = prepare()
    if args.run:
        run(fixture, launcher, args.live)
