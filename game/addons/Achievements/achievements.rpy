# Archive trophy catalog, earned ledgers, toast queue and developer controls.
# ach_grant() records explicit events; ach_sync() reconciles persistent predicates
# on load and Archive entry. Earned IDs remain recorded after their source flags
# reset. Only live ACHIEVEMENTS entries appear, count, notify and pay rewards.
# _ach_rt is init-time NoRollback runtime state; its queue holds plain ID strings,
# keeping pending UI and callable predicates out of save data.
# The developer source reachability audit runs after catalogs initialize.

default persistent.ach_earned = set()
# Every id EVER earned, across dev clears. ach_earned answers "is it unlocked
# right now"; ach_history answers "has the player ever done the thing". The
# dev shop's CLEAR ALL wipes only ach_earned, so anything in history still
# reads READY (and re-earns on sync) -- achievements never silently un-happen
# just because the earned set was reset. REVOKE is the hard relock: it removes
# the id from BOTH sets so the real trigger can be re-tested from scratch.
default persistent.ach_history = set()
# Dedicated story-completion signal. Older builds used the Music Room unlock as
# a proxy; _ach_ensure_store migrates that one-time historical state below.
default persistent.chapter05_completed = False
default persistent.ach_chapter05_migration_done = False

init python:

    class _AchRuntime(NoRollback):
        def __init__(self):
            self.queue = []         # FIFO of achievement ids waiting to toast
            self.started = None     # wall-clock start of the current toast; None = not rendered yet
            # DEV, session-only: gates ach_sync in developer builds so a CLEAR
            # ALL does not instantly re-earn everything. The old persistent
            # version of this flag could be left OFF and silently kill all
            # derived earning (and every toast) in every later session.
            self.autounlock = True
            # DEV, session-only: ids hard-revoked in the shop stay locked even
            # when their persistent objective flag is already true. Every live
            # objective has an exact ach_grant event hook; replaying that event
            # clears the latch and proves the real award path still works.
            self.retest = set()

    _ach_rt = _AchRuntime()

    # -- TIER TABLE -----------------------------------------------------------
    # color : the badge / rail fill.  glow : the brighter accent (progress fill,
    # toast label).
    ACH_TIER_ORDER = ["bronze", "silver", "gold"]
    ACH_TIERS = {
        "bronze":   {"label": "BRONZE",   "short": "B", "color": "#b9793f", "glow": "#e2a768"},
        "silver":   {"label": "SILVER",   "short": "S", "color": "#9fb0bd", "glow": "#dbe7ef"},
        "gold":     {"label": "GOLD",     "short": "G", "color": "#e0ac33", "glow": "#ffd45e"},
    }

    class Achievement(object):
        """One achievement row.
        id       : stable string key stored in persistent.ach_earned.
        tier     : one of ACH_TIER_ORDER.
        title    : short display name.
        blurb    : one-line objective. Kept deliberately vague for spoilery ones.
        earned   : callable() -> bool, evaluated against persistent state. None
                    for explicit-only achievements (granted via ach_grant).
        flag     : convenience shorthand for earned=lambda: bool(persistent.<flag>).
        progress : callable() -> (current, target) to draw a progress bar. Optional.
        cat      : loose grouping label (unused by the UI yet; handy for filters).
        """
        def __init__(self, id, tier, title, blurb, earned=None, flag=None,
                    progress=None, cat="GENERAL"):
            self.id = id
            self.tier = tier
            self.title = title
            self.blurb = blurb
            self.earned = earned
            self.flag = flag
            self.progress = progress
            self.cat = cat

    # -- LIVE PROGRESS HELPERS ------------------------------------------------
    ACH_CARD_TARGET = 30

    def _ach_unique_card_count():
        """Count owned cards against the live catalog when it is available."""
        census = globals().get("mc_collection_counts", None)
        if census is not None:
            try:
                return int(census()[0])
            except Exception:
                pass
        # Early-init/dev fallback for an interaction before mc_cards.rpy exists.
        owned = getattr(persistent, "mc_cards_owned", None) or ()
        if isinstance(owned, dict):
            owned = owned.keys()
        try:
            return len(set(owned))
        except Exception:
            return 0

    def _ach_card_progress():
        return (min(_ach_unique_card_count(), ACH_CARD_TARGET), ACH_CARD_TARGET)

    def _ach_tsubaki_route_cleared(route):
        """Read exact route history, with the old last-clear field as migration."""
        cleared = getattr(persistent, "tsubamode_routes_cleared", None) or ()
        return (route in cleared
                or getattr(persistent, "tsubamode_outcome", None) == route)

    # -- THE LIVE CATALOG ------------------------------------------------------
    # Keep this list honest about the current build. More rows arrive alongside
    # playable content; the roadmap indicator in the screen is not a trophy.

    ACHIEVEMENTS = [
        # --- BRONZE : main-story completion ---------------------------------
        Achievement("music_on", "bronze", "Curtain Call (For Now)",
            "Complete Chapter 0.5.",
            flag="chapter05_completed", cat="STORY"),

        # --- SILVER : mode clears / collection milestone --------------------
        Achievement("beat_matsuda", "silver", "Boss? What Boss?",
            "Beat the Matsuda boss fight on Normal Mode.",
            flag="id_mode_unlocked", cat="SECRET"),
        Achievement("koto_clear", "silver", "Eight Bars",
            "Beat the Kotonoha Touhou mode.",
            flag="kotomode_cleared", cat="SECRET"),
        Achievement("date_win", "silver", "Hard Pass",
            "Beat the Monika date mode.",
            flag="arcade_monika_cleared", cat="SECRET"),       # EXPLICIT + derived recovery
        Achievement("cards_30", "silver", "Thirty of a Kind",
            "Pull at least 30 unique cards.",
            earned=lambda: _ach_unique_card_count() >= ACH_CARD_TARGET,
            progress=_ach_card_progress, cat="COLLECTION"),

        # --- GOLD : alternate or route-specific clears ----------------------
        Achievement("matsuda_id", "gold", "She Swore She'd Never Build It",
            "Beat the Matsuda boss fight on Id Mode.",
            flag="arcade_id_cleared", cat="SECRET"),           # EXPLICIT + derived recovery
        Achievement("tsuba_spare", "gold", "Unstrung",
            "Beat Tsubaki Soul through pacifism.",
            earned=lambda: _ach_tsubaki_route_cleared("pacifist"),
            cat="SECRET"),                                     # EXPLICIT + derived migration
        Achievement("tsuba_violence", "gold", "Camellias Fall Whole",
            "Beat Tsubaki Soul through violence.",
            earned=lambda: _ach_tsubaki_route_cleared("violence"),
            cat="SECRET"),                                     # EXPLICIT + derived migration
        Achievement("tsuba_betrayal", "gold", "The Last Thread",
            "Beat Tsubaki Soul through betrayal.",
            earned=lambda: _ach_tsubaki_route_cleared("betrayal"),
            cat="SECRET"),                                     # EXPLICIT + derived migration
    ]

    ACH_BY_ID = {a.id: a for a in ACHIEVEMENTS}

    # -- STORE HELPERS --------------------------------------------------------
    def _ach_ensure_store():
        # Both persistent sets must always be real sets (guards old saves), and
        # history absorbs the current earned set here -- so every earn site
        # (sync, grant, lock, dev shop) feeds history without its own hook, and
        # pre-history persistents migrate the first time this runs.
        if not isinstance(getattr(persistent, "ach_earned", None), set):
            persistent.ach_earned = set(getattr(persistent, "ach_earned", None) or [])
        if not isinstance(getattr(persistent, "ach_history", None), set):
            persistent.ach_history = set(getattr(persistent, "ach_history", None) or [])
        # Full restarts construct this on the class, but keep Shift+R/hot-reload
        # sessions safe when an older _AchRuntime instance is still alive.
        if not isinstance(getattr(_ach_rt, "retest", None), set):
            _ach_rt.retest = set(getattr(_ach_rt, "retest", None) or ())
        persistent.ach_history.update(persistent.ach_earned)
        # Pre-rebuild profiles completed 0531 by unlocking the Music Room. Copy
        # that historical fact ONCE, so moving the room's unlock later cannot
        # move this trophy with it. The sentinel is also important in developer
        # builds: after migration has been considered, using ALL SIDE CONTENT to
        # open the Music Room cannot masquerade as completing Chapter 0.5.
        if not getattr(persistent, "ach_chapter05_migration_done", False):
            legacy_music_trophy = "music_on" in (
                set(getattr(persistent, "ach_earned", None) or ())
                | set(getattr(persistent, "ach_history", None) or ())
            )
            if (not getattr(persistent, "chapter05_completed", False)
                    and getattr(persistent, "archive_unlocked_music", False)
                    and (not config.developer or legacy_music_trophy)):
                persistent.chapter05_completed = True
            persistent.ach_chapter05_migration_done = True
    def ach_is_earned(a):
        _ach_ensure_store()
        aid = a.id if hasattr(a, "id") else a
        return aid in persistent.ach_earned

    def ach_earned_count():
        return sum(1 for a in ACHIEVEMENTS if ach_is_earned(a))

    def ach_tier_counts():
        counts = {t: [0, 0] for t in ACH_TIER_ORDER}
        for a in ACHIEVEMENTS:
            counts[a.tier][1] += 1
            if ach_is_earned(a):
                counts[a.tier][0] += 1
        return counts

    def ach_raw_condition_met(a):
        """Evaluate only the objective's persisted condition.

        This deliberately ignores ach_history. Exact event hooks use it before
        calling ach_grant(), so a developer clearing the card collection cannot
        re-award Thirty of a Kind merely because it was earned in an older run.
        """
        try:
            if a.earned is not None:
                return bool(a.earned())
            if a.flag is not None:
                return bool(getattr(persistent, a.flag, False))
        except Exception:
            return False
        return False

    def ach_condition_met(a):
        # Evaluate the achievement's OWN condition (not the locked-in set), with
        # history as the soft-reset recovery latch used by CLEAR ALL.
        # Ever earned before = the thing HAPPENED; a dev clear (or a volatile
        # flag being wiped) doesn't un-happen it. This is what makes previously
        # earned explicit/volatile achievements read READY after CLEAR ALL and
        # re-earn on the next sync instead of demanding a replay.
        if config.developer and a.id in _ach_rt.retest:
            return False
        if a.id in (getattr(persistent, "ach_history", None) or ()):
            return True
        return ach_raw_condition_met(a)

    def _ach_save_persistent():
        """Best-effort durability for the handful of lifetime trophy writes."""
        try:
            renpy.save_persistent()
        except Exception:
            pass

    def ach_sync(notify=True):
        """Auto-unlock pass: evaluate all conditions and lock in newly-true ones
        in catalog order. EVERY newly-earned achievement gets a toast -- the queue plays them one
        at a time -- UNLESS the pass unlocks more than ACH_TOAST_BATCH_MAX at
        once. That is a reconciliation (retrofitted save, dev reset with content
        already unlocked), not a moment, so it stays silent. One action tripping
        two conditions still toasts both.
        DEV: a no-op in developer builds while the dev shop's session-only
        AUTO-UNLOCK toggle is off; release builds always sync."""
        _ach_ensure_store()
        if config.developer and not _ach_rt.autounlock:
            return []
        newly = []
        for a in ACHIEVEMENTS:
            if a.id not in persistent.ach_earned and ach_condition_met(a):
                persistent.ach_earned.add(a.id)
                newly.append(a)
        if newly:
            # Keep the two ledgers atomic. Previously history only absorbed a
            # derived award on the *next* achievement interaction, leaving a
            # small crash/quit window in which CLEAR ALL forgot it had happened.
            persistent.ach_history.update(a.id for a in newly)
            _ach_save_persistent()
        if notify and newly and len(newly) <= ACH_TOAST_BATCH_MAX:
            for a in newly:
                ach_push_toast(a)
        return newly

    def ach_refresh():
        # VOID wrapper for screen `on "show"` / `on "replace"` handlers.
        # ach_sync() returns the list of newly-earned achievements, but a screen
        # EVENT action that returns a non-None value ends the interaction and
        # bubbles that value up like Return() -- which closed the Archive the
        # instant it opened and the main-menu context read the non-None result as
        # "start the game" (-> Chapter Select; it was the dev date picker when
        # this was found). Always return None here so the show event is a pure
        # side effect.
        ach_sync()
        return None

    def ach_grant(aid, notify=True):
        """Explicit unlock from a story beat. Idempotent and durable."""
        _ach_ensure_store()
        a = ACH_BY_ID.get(aid, None)
        if a is None:
            return False
        newly = aid not in persistent.ach_earned
        if newly:
            persistent.ach_earned.add(aid)
            persistent.ach_history.add(aid)
            if notify:
                ach_push_toast(a)
        _ach_rt.retest.discard(aid)
        # Always pick up derived conditions changed by the same story beat. The
        # old early return skipped this cascade on a replay of an earned event.
        ach_sync(notify=notify)
        if newly:
            _ach_save_persistent()
        return newly

    def ach_grant_if_met(aid, notify=True):
        """Exact-event bridge for a derived objective.

        The caller identifies the real completion beat (the card reveal closing,
        for example); the persisted predicate remains the authority on whether
        the objective is actually satisfied. Other derived state is reconciled
        either way so this is a drop-in replacement for ach_refresh(). This is
        intentionally a VOID wrapper: it is called through a screen Function
        action, where a non-None result can terminate the interaction.
        """
        _ach_ensure_store()
        a = ACH_BY_ID.get(aid, None)
        if a is None:
            return None
        if ach_raw_condition_met(a):
            ach_grant(aid, notify=notify)
        else:
            ach_sync(notify=notify)
        return None

    def ach_dev_clear(notify=True):
        """DEV: wipe the earned set so toasts can be re-tested WITHOUT touching
        save data or ach_history. Everything previously earned -- derived AND
        explicit -- therefore reads READY afterwards and comes back on the next
        ach_sync (silently, if more than ACH_TOAST_BATCH_MAX return at once) or
        one at a time via GRANT with auto-unlock off. Use REVOKE instead when a
        specific achievement's REAL trigger needs re-testing from LOCKED.
        Callable from the Matsu'Py console (Shift+O): ach_dev_clear()"""
        _ach_ensure_store()
        n = len(persistent.ach_earned)
        persistent.ach_earned = set()
        _ach_rt.retest.clear()
        del _ach_rt.queue[:]
        _ach_rt.started = None
        _ach_save_persistent()
        if notify:
            try:
                renpy.notify("Cleared %d achievement(s)." % n)
            except Exception:
                pass
        renpy.restart_interaction()
        return None

    # -- DEV SHOP (Nier-style manual grant/revoke, one at a time) --------------
    def ach_status(a):
        """'earned' (locked in) / 'ready' (condition met OR ever earned before
        -- would auto-unlock on sync) / 'locked' (never done, needs its real
        trigger)."""
        if ach_is_earned(a):
            return "earned"
        if ach_condition_met(a):
            return "ready"
        return "locked"

    def ach_dev_grant(aid):
        """DEV: unlock one achievement by hand, with its toast. No cascade sync,
        so granting one never drags the rest of the 'ready' ones in behind it."""
        _ach_ensure_store()
        a = ACH_BY_ID.get(aid, None)
        if a is not None and aid not in persistent.ach_earned:
            persistent.ach_earned.add(aid)
            persistent.ach_history.add(aid)
            _ach_rt.retest.discard(aid)
            ach_push_toast(a)
            _ach_save_persistent()
        return None

    def ach_dev_grant_all(notify=True):
        """DEV: unlock the complete live catalog in one deterministic pass."""
        _ach_ensure_store()
        newly = [a for a in ACHIEVEMENTS if a.id not in persistent.ach_earned]
        persistent.ach_earned.update(a.id for a in newly)
        persistent.ach_history.update(a.id for a in newly)
        _ach_rt.retest.clear()
        del _ach_rt.queue[:]
        _ach_rt.started = None
        _ach_save_persistent()
        if notify:
            try:
                renpy.notify("Granted %d achievement(s)." % len(newly))
            except Exception:
                pass
        renpy.restart_interaction()
        return None

    def ach_dev_revoke(aid):
        """DEV: hard relock for this session.

        Removes both persistent ledgers and suppresses derived reconciliation
        until the objective's exact ach_grant event runs again. The suppression
        is intentionally session-only so a forgotten dev latch cannot leak into
        a later player session. CLEAR ALL is the soft reset: it keeps history,
        so everything previously earned stays READY and carries back on sync.
        """
        _ach_ensure_store()
        persistent.ach_earned.discard(aid)
        persistent.ach_history.discard(aid)
        if aid in ACH_BY_ID:
            _ach_rt.retest.add(aid)
        was_current = bool(_ach_rt.queue and _ach_rt.queue[0] == aid)
        _ach_rt.queue[:] = [queued for queued in _ach_rt.queue if queued != aid]
        if was_current:
            _ach_rt.started = None
        _ach_save_persistent()
        renpy.restart_interaction()
        return None

    def ach_dev_toggle_autounlock():
        # Session-only on purpose (resets to ON every launch) -- see _AchRuntime.
        _ach_rt.autounlock = not _ach_rt.autounlock
        return None

    # -- TOAST ENGINE (always-shown screen + wall-clock ATL driver) ------------
    # HOSTING: the toaster is registered in config.always_shown_screens, so the
    # engine itself re-shows it at EVERY interaction, in EVERY context -- story,
    # the ShowMenu("archive") menu context, side stories, the boss fights --
    # even while overlays are suppressed (renpy/display/screen.py,
    # show_overlay_screens). The old renpy.show_screen() approach put the toast
    # in whichever context granted it, so leaving that context (closing the
    # Archive, a side story ending right after its ach_grant) killed the toast
    # before it drew a single frame. Never show/hide this screen by hand.
    # TIMING: one ATL `function` drives entry/dwell/exit per frame from
    # time.time(). Wall-clock, so skip mode cannot compress it and interaction
    # restarts cannot re-zero it -- and the clock only starts once the card
    # actually RENDERS, so a toast granted mid-transition still gets its full
    # dwell instead of expiring unseen.
    import time as _ach_time

    ACH_TOAST_IN        = 0.35    # entry slide (easeOutBack)
    ACH_TOAST_HOLD      = 3.0     # full-visibility dwell
    ACH_TOAST_OUT       = 0.45    # exit fade + drift
    ACH_TOAST_TOTAL     = ACH_TOAST_IN + ACH_TOAST_HOLD + ACH_TOAST_OUT
    ACH_TOAST_BATCH_MAX = 4       # sync batches larger than this reconcile silently

    def _ach_play_chime():
        snd = audio.notif
        try:
            if snd:
                renpy.play(snd, channel="sound")
        except Exception:
            pass

    def ach_push_toast(a):
        aid = a.id if hasattr(a, "id") else a
        if aid in ACH_BY_ID and aid not in _ach_rt.queue:
            _ach_rt.queue.append(aid)
        # The always-shown screen re-evaluates on interaction restart; force one
        # so a toast pushed mid-interaction appears immediately.
        renpy.restart_interaction()

    def _ach_toast_anim(trans, st, at):
        """ATL function on the toast card. Runs once per frame while a card is
        on screen: positions/fades it from wall-clock elapsed time, then pops
        the queue when the card's run ends. Returns 0 = call again next frame."""
        if renpy.predicting():
            return 0
        if not _ach_rt.queue:
            trans.alpha = 0.0
            return 0
        now = _ach_time.time()
        if _ach_rt.started is None:
            _ach_rt.started = now
            _ach_play_chime()
        el = now - _ach_rt.started

        if el < ACH_TOAST_IN:
            # entry: slide in from the right with a small overshoot
            p = el / ACH_TOAST_IN
            q = p - 1.0
            ease = 1.0 + 2.70158 * q * q * q + 1.70158 * q * q   # easeOutBack
            trans.alpha = min(1.0, p * 2.0)
            trans.xoffset = 60.0 * (1.0 - ease)
        elif el < ACH_TOAST_IN + ACH_TOAST_HOLD:
            trans.alpha = 1.0
            trans.xoffset = 0.0
        elif el < ACH_TOAST_TOTAL:
            # exit: quadratic fade while drifting back out
            p = (el - ACH_TOAST_IN - ACH_TOAST_HOLD) / ACH_TOAST_OUT
            trans.alpha = 1.0 - p * p
            trans.xoffset = 40.0 * p * p
        else:
            # done -> advance to the next card (or to nothing)
            _ach_rt.queue.pop(0)
            _ach_rt.started = None
            trans.alpha = 0.0
            renpy.restart_interaction()
        return 0

    if "achievement_toaster" not in config.always_shown_screens:
        config.always_shown_screens.append("achievement_toaster")

    # -- SYNC ON LOAD ---------------------------------------------------------
    def _ach_after_load():
        ach_sync()
        # Official Ren'Py guidance requires after-load callbacks that migrate or
        # reconcile data to block rollback across the migration boundary.
        renpy.block_rollback()
    if _ach_after_load not in config.after_load_callbacks:
        config.after_load_callbacks.append(_ach_after_load)


# =============================================================================
# UNLOCK TOAST  (compact bottom-right card + chime; see TOAST ENGINE above)
# =============================================================================
transform ach_toast_drive:
    subpixel True
    function _ach_toast_anim

# One struck medal per tier (60x84, ribbon on top), and the empty mount a medal
# not yet earned would hang in.
define ACH_MEDALS = {
    "bronze": "assets/gui/menu/illustrated/archive/medal_bronze.svg",
    "silver": "assets/gui/menu/illustrated/archive/medal_silver.svg",
    "gold": "assets/gui/menu/illustrated/archive/medal_gold.svg",
}
define ACH_MEDAL_LOCKED = "assets/gui/menu/illustrated/archive/medal_locked.svg"

# A medal hangs from its ribbon, so it swings in and settles, pivoting on the
# ribbon's top edge (anchor 0.5, 0.0 + transform_anchor). `key` is unused in
# the body; a new value restarts the swing. Comes to rest.
transform ach_medal_swing(delay=0.0, key=None):
    subpixel True
    anchor (0.5, 0.0)
    transform_anchor True
    alpha 0.0
    rotate -16
    pause delay
    parallel:
        easeout_quad 0.16 alpha 1.0
    parallel:
        ease 0.22 rotate 9
        ease 0.20 rotate -4
        ease 0.18 rotate 1.5
        ease 0.16 rotate 0

# A row of the case: fades up into place, staggered by `delay`.
transform ach_row_enter(delay=0.0):
    subpixel True
    alpha 0.0
    yoffset 10
    pause delay
    easeout_quad 0.26 alpha 1.0 yoffset 0

screen achievement_toaster():
    # Hosted by config.always_shown_screens -- present in every context, renders
    # NOTHING while the queue is empty. Above the dev shop (300) so GRANTs are
    # visible while the shop is open.
    zorder 400

    if _ach_rt.queue:
        $ _a = ACH_BY_ID.get(_ach_rt.queue[0], None)
        if _a is not None:
            $ _t = ACH_TIERS.get(_a.tier, ACH_TIERS["bronze"])

            # Fixed-size card, two tight lines beside the medal just struck.
            # NOTE: no yfill anywhere -- a fill inside this size-less frame is
            # what stretched the old toast down the whole right edge of the
            # screen (same gotcha as the custom say UI's themed frames).
            frame:
                style "ach_toast_frame"
                anchor (1.0, 1.0)
                pos (0.988, 0.965)
                ysize 66
                at ach_toast_drive

                hbox:
                    spacing 0

                    # tier rail
                    add Solid(_t["color"]) xysize (4, 66)
                    null width 12

                    # The medal swings in with the card; keyed on the
                    # achievement so each queued toast gets its own swing.
                    fixed:
                        xysize (40, 66)
                        add Transform(ACH_MEDALS.get(_a.tier, ACH_MEDALS["bronze"]), zoom=0.62):
                            xpos 20
                            ypos 5
                            at ach_medal_swing(0.05, _a.id)

                    null width 10

                    vbox:
                        yalign 0.5
                        spacing 2

                        text ("%s  /  UNLOCKED" % _t["label"]) style "ach_toast_kicker" color _t["glow"]
                        text _a.title style "ach_toast_title" layout "nobreak"

                    null width 18


# =============================================================================
# THE ACHIEVEMENTS SCREEN  (Archive slot 6) -- the medal case
# Modal overlay shown OVER the archive hub, mirroring character_stories: return
# is Hide("achievements"), which reveals the hub underneath. Every achievement
# is a medal on its ribbon beside its engraved line; one not yet earned is the
# empty mount it will hang in.
# =============================================================================
screen achievements():
    modal True

    # Refresh derived unlocks every time it opens (also toasts anything newly met).
    on "show" action Function(ach_refresh)

    default ach_filter = "all"

    use archive_backdrop

    key "game_menu" action Hide("achievements", transition=enter_m_menu_doorway)
    key "K_ESCAPE" action Hide("achievements", transition=enter_m_menu_doorway)

    $ _ach_all = ACHIEVEMENTS
    $ _ach_total = len(_ach_all)
    $ _ach_done = ach_earned_count()
    $ _ach_pct = int(round(100.0 * _ach_done / _ach_total)) if _ach_total else 0
    $ _ach_tc = ach_tier_counts()
    $ _ach_shown = [a for a in _ach_all if ach_filter == "all" or a.tier == ach_filter]

    frame:
        style "archive_shell_frame"
        padding (24, 20)
        at archive_frame_enter()

        vbox:
            spacing 12

            use archive_header("ACHIEVEMENTS", Hide("achievements", transition=enter_m_menu_doorway))

            # ---- readout strip: overall + per-tier tally --------------------
            # The shared strip (archive.rpy), transcluding the tier tally into
            # its right slot -- the layout gotchas live there, once.
            use archive_readout("THE MEDAL CASE / %d OF %d STRUCK / %d%%" % (_ach_done, _ach_total, _ach_pct), right_slot=True):
                for _tk in ACH_TIER_ORDER:
                    text "%s %d/%d" % (ACH_TIERS[_tk]["short"], _ach_tc[_tk][0], _ach_tc[_tk][1]):
                        style "archive_meta_text"
                        color ACH_TIERS[_tk]["glow"]
                        yalign 0.5

            # ---- tier filter tabs (Credits' cloth index tabs) ---------------
            hbox:
                spacing 10

                for _fk, _flabel in [("all", "ALL"), ("bronze", "BRONZE"), ("silver", "SILVER"), ("gold", "GOLD")]:
                    textbutton _flabel:
                        style "ach_filter_button"
                        action SetScreenVariable("ach_filter", _fk)
                        selected (ach_filter == _fk)

            # ---- the case --------------------------------------------------
            viewport:
                xsize 1150
                ysize 440
                mousewheel True
                scrollbars "vertical"
                style_prefix "archive_sv"

                vbox:
                    spacing 0

                    # Keyed on (filter, achievement): changing the filter hangs a
                    # fresh set, so every medal swings in again rather than the
                    # survivors sitting still while only the newcomers move.
                    for _i, a index (ach_filter, a.id) in enumerate(_ach_shown):
                        $ _e = ach_is_earned(a)
                        $ _t = ACH_TIERS[a.tier]

                        frame:
                            xsize 1116
                            ysize 94
                            padding (0, 0)
                            background (Solid("#d9cdb60b") if _e else None)
                            at ach_row_enter(_i * 0.05)

                            fixed:
                                xysize (1116, 94)

                                add Solid("#d9cdb622") xysize (1116, 1) ypos 93

                                if _e:
                                    add ACH_MEDALS[a.tier] xpos 56 ypos 5 at ach_medal_swing(0.10 + _i * 0.05, ach_filter)
                                else:
                                    add ACH_MEDAL_LOCKED xpos 56 ypos 5 xanchor 0.5

                                text a.title style ("ach_row_title" if _e else "ach_row_title_locked") xpos 116 ypos 14
                                text a.blurb style "ach_row_blurb" xpos 116 ypos 47

                                if a.progress is not None:
                                    $ _cur, _tgt = a.progress()
                                    $ _frac = 0.0 if not _tgt else max(0.0, min(1.0, float(_cur) / float(_tgt)))
                                    add Solid("#d9cdb633") xpos 116 ypos 77 xysize (240, 1)
                                    add Solid(_t["glow"]) xpos 116 ypos 76 xysize (max(0, int(240 * _frac)), 3)
                                    text "%d/%d" % (_cur, _tgt) style "ach_progress_text" xpos 366 ypos 71

                                # tier + status, pinned right
                                text _t["label"]:
                                    style "ach_row_tier"
                                    color (_t["glow"] if _e else "#77716a")
                                    xanchor 1.0
                                    xpos 1092
                                    ypos 26
                                text ("UNLOCKED" if _e else "LOCKED"):
                                    style ("ach_row_state" if _e else "ach_row_state_locked")
                                    xanchor 1.0
                                    xpos 1092
                                    ypos 48

                    # Roadmap indicator only: deliberately absent from
                    # ACHIEVEMENTS, so it never counts against completion.
                    if ach_filter == "all":
                        frame:
                            xsize 1116
                            ysize 94
                            padding (0, 0)
                            background None
                            at ach_row_enter(len(_ach_shown) * 0.05)

                            fixed:
                                xysize (1116, 94)

                                add ACH_MEDAL_LOCKED xpos 56 ypos 5 xanchor 0.5 alpha 0.6
                                text "More Medals on the Way" style "ach_row_title_locked" xpos 116 ypos 14
                                text "The case will fill as new chapters and modes arrive." style "ach_row_blurb" xpos 116 ypos 47
                                text "IN DEVELOPMENT" style "ach_row_state_locked" xanchor 1.0 xpos 1092 ypos 48

            # ---- footer ----------------------------------------------------
            fixed:
                xsize 1150
                ysize 16

                add Solid(IM_PLUM) xysize (5, 5) xpos 0 yalign 0.5 rotate 45
                text "MEDALS ARE STRUCK AS THEY ARE EARNED":
                    style "archive_footer_text"
                    xpos 13
                    yalign 0.5
                text "MORE ARE ON THE WAY":
                    style "archive_footer_text"
                    xanchor 1.0
                    xpos 1150
                    yalign 0.5

    # Brackets sized to the 1200-wide shell frame (matches char_stories); the
    # old 1160 values were narrower than the frame and clipped the right edge.
    use archive_shell_brackets()


# =============================================================================
# DEV ACHIEVEMENT SHOP  (config.developer only; opened from the Developer Hub
# -- main menu, top-right, or F9. It used to hang off a pill on the achievement
# list itself, which put a dev control inside a player screen; the hub owns
# every entry point now, and this screen stays here because the LOGIC belongs
# to Achievements.) Nier-style manual control: flip AUTO-UNLOCK off
# (session-only) so a reset does not swarm, then GRANT the "ready" (already-
# satisfied) ones one at a time to watch each toast.
# =============================================================================
screen ach_dev_shop():
    modal True
    zorder 300

    key "game_menu" action Hide("ach_dev_shop")
    key "K_ESCAPE" action Hide("ach_dev_shop")

    add "menu_bg"
    add Solid("#02050af2")

    $ _auto = _ach_rt.autounlock
    $ _done = ach_earned_count()

    frame:
        style "archive_shell_frame"
        padding (24, 20)

        vbox:
            spacing 12

            hbox:
                xfill True
                ysize 52
                text "ACHIEVEMENT DEV SHOP" style "archive_title" yalign 0.5
                null width 1 xfill True
                textbutton "CLOSE":
                    style "archive_return_button"
                    yalign 0.5
                    action Hide("ach_dev_shop")

            # controls
            hbox:
                xsize 1150
                spacing 12
                yalign 0.5

                textbutton ("AUTO-UNLOCK: ON" if _auto else "AUTO-UNLOCK: OFF"):
                    style "ach_filter_button"
                    selected _auto
                    action Function(ach_dev_toggle_autounlock)

                textbutton "CLEAR ALL":
                    style "ach_filter_button"
                    action Function(ach_dev_clear)

                textbutton "GRANT ALL":
                    style "ach_filter_button"
                    action Function(ach_dev_grant_all)

                textbutton "SYNC NOW":
                    style "ach_filter_button"
                    action Function(ach_refresh)

                null width 1 xfill True

                text "EARNED [_done]/%d  //  AUTO is session-only  //  CLEAR keeps READY history" % len(ACHIEVEMENTS):
                    style "archive_footer_text"
                    yalign 0.5

            add Solid("#56d7ff66") xysize (1150, 2)

            viewport:
                xsize 1150
                ysize 424
                mousewheel True
                scrollbars "vertical"
                style_prefix "archive_sv"

                vbox:
                    spacing 6

                    for a in ACHIEVEMENTS:
                        $ _st = ach_status(a)
                        $ _t = ACH_TIERS[a.tier]
                        $ _rail = _t["glow"] if _st == "earned" else ("#5fa06a" if _st == "ready" else "#33414d")

                        frame:
                            xsize 1116
                            ysize 52
                            background Solid("#08131fdd" if _st == "earned" else "#060b12b0")
                            padding (0, 0)

                            hbox:
                                yfill True

                                add Solid(_rail) xysize (5, 52)
                                null width 12

                                frame:
                                    yalign 0.5
                                    background Solid(_t["color"])
                                    padding (8, 3)
                                    text _t["label"] style "archive_chip_on_text"

                                null width 14
                                text a.title style "ach_row_title" yalign 0.5 xsize 470

                                text _st.upper():
                                    style "archive_meta_text"
                                    yalign 0.5
                                    xsize 130
                                    color (_t["glow"] if _st == "earned" else ("#8ad9a2" if _st == "ready" else "#5d7886"))

                                null width 1 xfill True

                                if _st == "earned":
                                    textbutton "REVOKE":
                                        style "ach_shop_btn"
                                        yalign 0.5
                                        action Function(ach_dev_revoke, a.id)
                                else:
                                    textbutton "GRANT":
                                        style "ach_shop_btn"
                                        yalign 0.5
                                        action Function(ach_dev_grant, a.id)

                                null width 14

    use archive_shell_brackets()


# =============================================================================
# STYLES  (reuses archive_* styles where possible; adds only what's new)
# Paper ink on the case's dark lining; the tiers keep their own metals.
# =============================================================================
style ach_row_title is gui_text:
    font gui.default_font
    color IM_PAPER
    size 22
    outlines []

style ach_row_title_locked is ach_row_title:
    color "#8f8a86"

style ach_row_blurb is gui_text:
    font gui.default_font
    color "#bdb4a6"
    size 15
    outlines []

style ach_progress_text is gui_text:
    font gui.interface_font
    color "#d9c9a8"
    size 10
    kerning 1.2
    outlines []

style ach_row_tier is gui_text:
    font gui.interface_font
    size 11
    kerning 2.0
    outlines []

style ach_row_state is ach_row_tier:
    size 10
    kerning 1.4
    color IM_PAPER

style ach_row_state_locked is ach_row_state:
    color "#77716a"

style ach_filter_button:
    ysize 40
    xminimum 112
    background Frame("assets/gui/menu/illustrated/credits/section_tab.svg", 12, 10, 12, 10)
    hover_background Frame("assets/gui/menu/illustrated/credits/section_tab_selected.svg", 12, 10, 12, 10)
    selected_background Frame("assets/gui/menu/illustrated/credits/section_tab_selected.svg", 12, 10, 12, 10)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (20, 6)

style ach_filter_button_text:
    font gui.interface_font
    color "#d9c9a8"
    hover_color "#ffffff"
    selected_color IM_PAPER
    size 14
    kerning 1.4
    xalign 0.5
    yalign 0.5
    outlines []

# ---- dev shop grant/revoke button ----
style ach_shop_btn:
    xsize 108
    background Solid("#0c2a1d")
    hover_background Solid("#155636")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (12, 6)

style ach_shop_btn_text:
    font gui.interface_font
    color "#bfe6cf"
    hover_color "#ffffff"
    size 15
    bold True
    text_align 0.5
    xalign 0.5
    outlines [(1, "#02040b", 0, 0)]

# ---- toast ----
style ach_toast_frame is empty:
    background IM_DARK_PANEL
    padding (0, 0)

style ach_toast_kicker:
    font gui.interface_font
    size 10
    kerning 2.0
    outlines []

style ach_toast_title:
    font gui.default_font
    color IM_PAPER
    size 19
    outlines []


# Developer source audit for catalog unlock/completion/show/play references.
# This is a heuristic reachability warning, not proof that a route is playable.
# Runs after catalogs initialize in developer builds; ach_audit_content() can
# also be called from the console. Missing/unreadable source files are skipped.

init python:
    def ach_audit_content(verbose=True):
        """Report catalogued content that nothing in the script can unlock."""
        import os
        import re

        sources = []
        for root, _dirs, files in os.walk(renpy.config.gamedir):
            for name in files:
                if name.endswith(".rpy"):
                    try:
                        with open(os.path.join(root, name), "r", encoding="utf-8") as handle:
                            sources.append((name, handle.read()))
                    except Exception:
                        continue

        blob = "\n".join(text for _name, text in sources)

        # Index play/queue lines and sprite show lines once. Per-item checks
        # then search these small indexes instead of the whole source corpus.
        blob_lower = blob.lower()

        play_keyword = re.compile(r"\b(?:play|queue)\b")
        show_keyword = re.compile(r"\bshow\s+(\w+)\b")

        play_tails = []     # text following a play/queue keyword
        show_tails = {}     # sprite tag -> text following each `show <tag>`

        for line in blob.split("\n"):

            if ("play" in line) or ("queue" in line):
                # Only the FIRST keyword on the line needs recording -- its tail
                # already contains every later one's.
                found = play_keyword.search(line)
                if found is not None:
                    play_tails.append(line[found.end():])

            if "show" in line:
                for found in show_keyword.finditer(line):
                    show_tails.setdefault(found.group(1), []).append(line[found.end():])

        play_blob = "\n".join(play_tails)
        show_blob = { tag: "\n".join(tails) for tag, tails in show_tails.items() }

        def named_after(needle, haystack):
            """True if `needle` appears in `haystack` as a whole word."""
            return re.search(r"\b%s\b" % re.escape(needle), haystack) is not None

        def quoted_args(func):
            """Approximate quoted call arguments; nested calls are not parsed."""
            found = set()
            literal_pattern = re.compile(
                r'"([^"\\]*(?:\\.[^"\\]*)*)"|'
                r"'([^'\\]*(?:\\.[^'\\]*)*)'"
            )
            for call in re.findall(r"\b%s\s*\(([^)]*)\)" % func, blob):
                # Match the opening delimiter so apostrophes inside double-quoted
                # titles (for example, "Hina's World") remain part of the title.
                for match in literal_pattern.finditer(call):
                    literal = match.group(1) if match.group(1) is not None else match.group(2)
                    found.add(literal.strip().lower())
            return found

        problems = []

        # --- CGs --------------------------------------------------------------
        unlocked_names = quoted_args("cg_unlock")
        # The OP routes its unlocks through a soft wrapper so that pulling a CG
        # out of the gallery cannot crash the opening (see enter_m_op_cg_unlock
        # in Sick Ass Anime OP/op.rpy). Those are real call sites, but the
        # word-boundary anchor in the scan above cannot match the suffixed name,
        # so ask for it by name too.
        unlocked_names.update(quoted_args("enter_m_op_cg_unlock"))
        # Archive panel CGs unlock from a data-driven module-flag table rather
        # than seven hand-written calls. Count those declared titles as real
        # reachability sites while retaining the ordinary call-site audit for
        # every authored story CG.
        unlocked_names.update(
            str(title).strip().lower()
            for _archive_key, title in globals().get("archive_panel_cg_unlocks", ())
        )
        for act in globals().get("cg_gallery_catalog", ()):
            for chapter in act.chapters:
                for cg in chapter.cgs:
                    if (cg.title.lower() not in unlocked_names
                            and cg.image_path.lower() not in unlocked_names):
                        problems.append(
                            "CG %r (%s / %s) has no cg_unlock() call site."
                            % (cg.title, act.name, chapter.name))

        # --- Side stories -----------------------------------------------------
        completed_labels = quoted_args("cs_mark_completed")
        for category in globals().get("character_story_catalog", ()):
            for story in category.stories:
                if not story.persistent_key:
                    continue
                if story.label_name.lower() not in completed_labels:
                    problems.append(
                        "Side story %r (%s) has no cs_mark_completed() call site, "
                        "so it can never be marked read." % (story.title, category.name))
                # The flag has to be set by SOMETHING other than its own default
                # line and the dev switch, or the story is unreachable.
                sets = len(re.findall(
                    r"%s(?!\s*=\s*False)" % re.escape(story.persistent_key), blob))
                if sets <= 1:
                    problems.append(
                        "Side story %r (%s) is never unlocked: nothing sets %s."
                        % (story.title, category.name, story.persistent_key))

        # --- Outfits ----------------------------------------------------------
        for profile in globals().get("character_roster", ()):
            for outfit in profile.outfits:
                if outfit.is_default:
                    continue
                tag = str(outfit.image).split()[0]
                if not named_after(outfit.attr, show_blob.get(tag, "")):
                    problems.append(
                        "Outfit %s/%s is never worn: no `show %s ... %s` anywhere."
                        % (profile.name, outfit.id, tag, outfit.attr))

        # --- Music ------------------------------------------------------------
        # Map each library file back to the audio.<alias> it was defined as, so a
        # `play music hopeless` counts for assets/audio/bgm/13am.ogg.
        try:
            aliases = {}
            for name in dir(store.audio):
                if name.startswith("_"):
                    continue
                value = getattr(store.audio, name, None)
                if isinstance(value, str):
                    aliases.setdefault(value.lower().replace("\\", "/"), []).append(name)

            for track in globals().get("music_library", ()):
                path = str(track.file_path).lower().replace("\\", "/")
                names = aliases.get(path, [])
                needles = [path] + ["audio.%s" % n for n in names] + names
                # A bare alias only counts as a play if a play/queue statement
                # names it; the string on its own is just the definition.
                heard = any(named_after(n, play_blob) for n in needles)
                if not heard and path not in blob_lower:
                    problems.append(
                        "Track %r is in the Music Room but is never played, so it "
                        "can never be recovered." % (track.title,))
        except Exception as audit_error:
            problems.append("Music audit skipped: %r" % (audit_error,))

        if verbose:
            print("\n=== ENTER M content reachability audit ===")
            if problems:
                for line in problems:
                    print("  WARN  " + line)
            print("  %d unreachable item(s) across %d source files."
                % (len(problems), len(sources)))
            print("=" * 42 + "\n")

        return problems


# init 999: after every catalog exists. Dev builds only -- it reads the whole
# project source, which is pointless work in a release build where the content
# is already fixed.
init 999 python:
    if config.developer:
        ach_audit_content()
