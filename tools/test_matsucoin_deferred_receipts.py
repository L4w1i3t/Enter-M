"""Focused contract test for Matsucoin payout persistence and dev resets.

This executes the Python model directly with tiny Ren'Py stubs. It is not a
replacement for compiling the project; it protects the failure-prone boundary
between an immediate wallet transaction and a receipt deferred until the next
main-menu entry.
"""

from __future__ import annotations

import pathlib
import types


ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game" / "addons" / "Matsucoin Currency and Gacha" / "matsucoin.rpy"


class _Music:
    def channel_defined(self, _name):
        return True

    def register_channel(self, *_args, **_kwargs):
        raise AssertionError("existing test channels should not be registered")

    def get_playing(self, **_kwargs):
        return None


class _Sound:
    def play(self, *_args, **_kwargs):
        return None


class _RenPy:
    def __init__(self, store):
        self.store = store
        self.music = _Music()
        self.sound = _Sound()
        self.saved = 0
        self.restarted = 0

    @staticmethod
    def pure(fn):
        return fn

    @staticmethod
    def predicting():
        return False

    def save_persistent(self):
        self.saved += 1

    def restart_interaction(self):
        self.restarted += 1


def _python_model_source():
    text = SOURCE.read_text(encoding="utf-8")
    marker = "init -5 python:\n"
    start = text.index(marker) + len(marker)
    lines = text[start:].splitlines()
    block = []
    for line in lines:
        if line and not line.startswith("    "):
            break
        block.append(line[4:] if line.startswith("    ") else line)
    return "\n".join(block)


def _load_model():
    persistent = types.SimpleNamespace(
        mc_balance=0,
        mc_lifetime=0,
        mc_spent=0,
        mc_paid_keys=set(),
        mc_pending_notice_amount=0,
        mc_pending_notice_events=0,
    )
    store = types.SimpleNamespace(main_menu=False)
    renpy = _RenPy(store)
    env = {
        "persistent": persistent,
        "renpy": renpy,
        "NoRollback": object,
        # Displayable names are resolved only if their builders are called.
        "Transform": lambda *args, **kwargs: (args, kwargs),
        "Fixed": lambda *args, **kwargs: (args, kwargs),
        "Solid": lambda *args, **kwargs: (args, kwargs),
        "Composite": lambda *args, **kwargs: (args, kwargs),
        "Crop": lambda *args, **kwargs: (args, kwargs),
    }
    exec(compile(_python_model_source(), str(SOURCE), "exec"), env)
    return env, persistent, store, renpy


def _finish_current_receipt(env):
    runtime = env["_mc_rt"]
    runtime.started = env["_mc_time"].time() - env["MC_TOAST_TOTAL"] - 1.0
    trans = types.SimpleNamespace(alpha=1.0, xoffset=0.0)
    env["_mc_toast_anim"](trans, 0.0, 0.0)


def main():
    source_text = SOURCE.read_text(encoding="utf-8")
    assert 'if name != "before_main_menu":' in source_text
    assert "config.label_callbacks.append(_mc_label_callback)" in source_text
    assert "if main_menu and _mc_rt.queue:" in source_text

    env, persistent, store, _renpy = _load_model()

    # Credit and ledger commit happen now; presentation does not.
    assert env["mc_award"](120, "TEST", key="test:once") == 120
    assert persistent.mc_balance == 120
    assert persistent.mc_lifetime == 120
    assert persistent.mc_paid_keys == {"test:once"}
    assert persistent.mc_pending_notice_amount == 120
    assert persistent.mc_pending_notice_events == 1
    assert env["_mc_rt"].queue == []

    # Re-running a one-time source is idempotent across every state field.
    assert env["mc_award"](120, "TEST", key="test:once") == 0
    assert persistent.mc_balance == 120
    assert persistent.mc_pending_notice_amount == 120

    # Cross-system recovery is ordered: an unsynced achievement gets a chance
    # to become an input before Matsucoin derives and stages this title receipt.
    order = []
    real_sync = env["mc_sync"]
    env["ach_sync"] = lambda: order.append("achievement")
    env["mc_sync"] = lambda: (order.append("matsucoin"), real_sync())[1]
    env["mc_main_menu_enter"]()
    assert order == ["achievement", "matsucoin"]
    env["mc_sync"] = real_sync

    # A gameplay render cannot start or acknowledge the pending receipt.
    env["mc_main_menu_enter"]()
    assert len(env["_mc_rt"].queue) == 1
    trans = types.SimpleNamespace(alpha=1.0, xoffset=0.0)
    env["_mc_toast_anim"](trans, 0.0, 0.0)
    assert env["_mc_rt"].started is None
    assert persistent.mc_pending_notice_amount == 120

    # Entering the title stages one summary. A later award is not erased when
    # the already-staged portion finishes.
    store.main_menu = True
    env["mc_main_menu_enter"]()
    assert env["_mc_rt"].queue[0][0] == 120
    assert env["mc_award"](35, "LATER", key="test:later") == 35
    assert persistent.mc_pending_notice_amount == 155
    _finish_current_receipt(env)
    assert persistent.mc_pending_notice_amount == 35
    assert persistent.mc_pending_notice_events == 1

    # A new runtime (relaunch) reconstructs the still-persistent receipt.
    env["_mc_rt"] = env["_McRuntime"]()
    env["mc_main_menu_enter"]()
    assert env["_mc_rt"].queue[0][0] == 35
    _finish_current_receipt(env)
    assert persistent.mc_pending_notice_amount == 0
    assert persistent.mc_pending_notice_events == 0

    # Developer RESET removes wallet telemetry and any staged receipt. Wiping
    # the ledger additionally makes one-time sources claimable again.
    env["mc_award"](20, "RESET ME", key="test:reset")
    env["mc_main_menu_enter"]()
    env["mc_dev_reset"](keep_ledger=False)
    assert persistent.mc_balance == 0
    assert persistent.mc_lifetime == 0
    assert persistent.mc_spent == 0
    assert persistent.mc_paid_keys == set()
    assert persistent.mc_pending_notice_amount == 0
    assert persistent.mc_pending_notice_events == 0
    assert env["_mc_rt"].queue == []

    # Derived reconciliation is one aggregate receipt with an honest source
    # count, even though each ledger key is still committed independently.
    env2, persistent2, _store2, _renpy2 = _load_model()
    env2["MC_DERIVED_RULES"] = (
        ("probe", 40, lambda: ("alpha", "beta")),
    )
    assert env2["mc_sync"]() == 80
    assert persistent2.mc_balance == 80
    assert persistent2.mc_paid_keys == {"probe:alpha", "probe:beta"}
    assert persistent2.mc_pending_notice_amount == 80
    assert persistent2.mc_pending_notice_events == 2
    assert env2["mc_sync"]() == 0

    # At the cap, a one-time award waits intact and does not burn its key. A
    # repeatable award may top up only the available room and reports that exact
    # credited amount in the pending receipt.
    persistent2.mc_balance = env2["MC_BALANCE_CAP"] - 10
    assert env2["mc_award"](20, key="probe:too_large") == 0
    assert "probe:too_large" not in persistent2.mc_paid_keys
    before_notice = persistent2.mc_pending_notice_amount
    assert env2["mc_award"](20) == 10
    assert persistent2.mc_pending_notice_amount == before_notice + 10

    print("matsucoin deferred receipt contract: PASS")


if __name__ == "__main__":
    main()
