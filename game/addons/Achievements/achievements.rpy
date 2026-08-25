# =============================================================================
# achievements.rpy  --  THE ACHIEVEMENTS MODULE (Archive slot 6)
# =============================================================================
#
# WHAT THIS FILE IS
#   The sixth Archive module: a tiered achievement / completion checklist. It is
#   reached from the Archive hub (game/archive.rpy) just like Roster, CG Gallery,
#   Music Room, Side Stories and Lost Records, and it deliberately reuses that
#   hub's shared chrome (archive_backdrop / archive_header / the archive_sv
#   scrollbar / the chip + meta text styles) so it reads as the same subsystem.
#
# TWO KINDS OF ACHIEVEMENT, ONE CODE PATH
#   * DERIVED  -- an `earned` predicate (or a `flag` name) evaluated against state
#                 the game already persists (exam-guard scum flags, kotomode
#                 records, id_mode_unlocked, the cs_*_unlocked and
#                 archive_unlocked_music flags, and the Archive's three
#                 collections: CGs seen, outfits worn, roster slots identified).
#                 These need NO extra hooks: they light up the moment their
#                 underlying state is met and ach_sync() next runs.
#   * EXPLICIT -- granted by a single ach_grant("id") call dropped at a story beat
#                 for things nothing else persists (the Id Mode superboss clear;
#                 the Monika date-mode win). These fire an instant toast.
#
# HOW EARNING WORKS (persistence + platinum)
#   persistent.ach_earned is a *set of ids that have been locked in*. Once an id
#   is in that set it stays earned forever, even if the underlying derived flag
#   later resets (the exam-guard flags, for instance, are wiped on a new game).
#   ach_sync() evaluates every condition, locks in the newly-true ones, and queues
#   a toast for each. PLATINUM is defined as "every non-platinum achievement is in
#   ach_earned", so it auto-fires the instant the last other one is earned.
#
# WHERE SYNC IS TRIGGERED (so derived unlocks are never missed)
#   * config.after_load_callbacks -> ach_sync   (loading a save)
#   * screen archive() / achievements() on "show" -> ach_sync
#     (returning to the hub after a fight / side story catches those unlocks)
#   * ach_grant() runs ach_sync afterwards so granting the last one trips platinum.
#   Any system that wants an INSTANT derived toast can just call ach_sync() right
#   after it flips its flag (see the cs_matsuda_02 victory hook for the pattern).
#
# EDITING THE CATALOG
#   The whole catalog is the ACHIEVEMENTS list below -- add/cut/retier by editing
#   one Achievement(...) line. Tiers: "bronze" / "silver" / "gold" / "platinum".
#   Platinum is reserved for the single 100%-completion entry. Threshold targets
#   marked "# TUNE" are first-pass guesses meant to be adjusted.
# =============================================================================

# -----------------------------------------------------------------------------
# PERSISTENT / RUNTIME STATE
# persistent.ach_earned : the locked-in set of earned ids (survives forever).
# _ach_rt : toast queue + dev toggle. Deliberately a NoRollback object created
#   at init, NOT `default` store variables: the old store-variable queue was
#   rolled back with the game (a rollback could vaporize or resurrect pending
#   toasts) and was written into every save -- and once it held Achievement
#   objects (whose predicates are lambdas) the save itself crashed on pickling.
#   An init-time NoRollback object is never saved and never rolled back, and
#   the queue holds plain id strings besides.
# -----------------------------------------------------------------------------
default persistent.ach_earned = set()
# Every id EVER earned, across dev clears. ach_earned answers "is it unlocked
# right now"; ach_history answers "has the player ever done the thing". The
# dev shop's CLEAR ALL wipes only ach_earned, so anything in history still
# reads READY (and re-earns on sync) -- achievements never silently un-happen
# just because the earned set was reset. REVOKE is the hard relock: it removes
# the id from BOTH sets so the real trigger can be re-tested from scratch.
default persistent.ach_history = set()
# Toasts owed to the player that could not be shown when they were earned:
# ach_lock() fires inside the exam-guard catch labels, which end in
# renpy.utter_restart()/full_restart() -- that destroys any live toast AND
# resets _ach_rt. Ids parked here (plain strings, safe to pickle) are drained
# into the toast queue at the next main-menu interaction / after a load.
default persistent.ach_toast_pending = []

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

    _ach_rt = _AchRuntime()

    # -- TIER TABLE -----------------------------------------------------------
    # color : the badge / rail fill.  glow : the brighter accent (progress fill,
    # toast label).  Platinum is your UI's own cyan so it literally glows like
    # the rest of the console.
    ACH_TIER_ORDER = ["bronze", "silver", "gold", "platinum"]
    ACH_TIERS = {
        "bronze":   {"label": "BRONZE",   "short": "B", "color": "#b9793f", "glow": "#e2a768"},
        "silver":   {"label": "SILVER",   "short": "S", "color": "#9fb0bd", "glow": "#dbe7ef"},
        "gold":     {"label": "GOLD",     "short": "G", "color": "#e0ac33", "glow": "#ffd45e"},
        "platinum": {"label": "PLATINUM", "short": "P", "color": "#5fd3ef", "glow": "#a8f0ff"},
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

    # -- FLAG GROUPS the predicates lean on -----------------------------------
    # Every group is READ FROM ITS OWNING CATALOG rather than copied here.
    # A hand-kept copy goes stale the moment a story, a CG or an outfit is added
    # or commented out, and a listed flag that no live content can ever flip
    # makes its "collect them all" achievement -- and therefore platinum --
    # unearnable.
    #
    # These are functions, not lists, because this file inits BEFORE the catalogs
    # they read (same init priority, earlier filename), so nothing exists yet at
    # definition time. Every caller is a predicate lambda evaluated later, so the
    # lazy read costs nothing.
    def _ach_side_story_flags():
        return tuple(
            story.persistent_key
            for category in (globals().get("character_story_catalog") or ())
            for story in category.stories
            if story.persistent_key
        )

    # The stricter half of the same catalog: read-to-the-end, not just held.
    def _ach_side_story_done_flags():
        return tuple(
            story.completed_key
            for category in (globals().get("character_story_catalog") or ())
            for story in category.stories
            if story.completed_key
        )

    # The three collections that replaced "bring Archive modules online" once the
    # Archive shell started shipping open (game/archive.rpy). Same lazy-read rule
    # as the two groups above: this file inits before their owning catalogs.
    def _ach_cg_flags():
        fn = globals().get("cg_all_keys", None)
        return fn() if fn else ()

    def _ach_outfit_flags():
        fn = globals().get("roster_outfit_keys", None)
        return fn() if fn else ()

    def _ach_roster_ids():
        fn = globals().get("roster_gated_ids", None)
        return fn() if fn else ()

    def _ach_roster_progress(target=None):
        ids = _ach_roster_ids()
        met = getattr(persistent, "roster_met_ids", None) or ()
        total = len(ids) if target is None else target
        return (min(sum(1 for i in ids if i in met), total), total)

    def _ach_count_true(flags):
        return sum(1 for f in flags if getattr(persistent, f, False))

    # `flags_fn` is one of the group readers above. Resolving it once per call
    # keeps the "collect them all" pairs (earned + progress) from disagreeing,
    # and the total > 0 guard means an empty catalog reads as 0/0 UNEARNED
    # rather than trivially complete.
    def _ach_progress(flags_fn, target=None):
        flags = flags_fn()
        total = len(flags) if target is None else target
        return (min(_ach_count_true(flags), total), total)

    def _ach_complete(flags_fn, target=None):
        done, total = _ach_progress(flags_fn, target)
        return total > 0 and done >= total

    # A "get some of them" achievement must be a FRACTION of the catalog, never a
    # hard number. side_half shipped asking for 5 side stories when 8 existed;
    # at 20 stories that is a participation trophy, and if stories were ever cut
    # below 5 it would be unearnable and would take platinum down with it.
    def _ach_fraction_target(flags_fn, fraction):
        total = len(flags_fn())
        if not total:
            return 0
        return max(1, int(total * fraction + 0.5))

    # Same "0/0 is UNEARNED, not trivially complete" rule, for the collections
    # that hand back a (done, total) pair directly instead of a list of flags.
    def _ach_complete_pair(progress_fn, *args):
        done, total = progress_fn(*args)
        return total > 0 and done >= total

    def _ach_scum_count():
        # exam_guard.rpy owns this; fall back to counting the flags directly so
        # this module never hard-depends on that file loading first.
        fn = globals().get("exam_guard_scum_count", None)
        if fn:
            try:
                return fn()
            except Exception:
                pass
        return len(getattr(persistent, "exam_save_scum_subjects", None) or [])

    # -- THE CATALOG (first pass -- edit freely) ------------------------------
    # TUNE targets: these two thresholds are placeholders until playtested.
    ACH_KOTO_SCORE_TARGET = 15000000     # TUNE: Kotonoha-mode high score goal
    ACH_KOTO_WAVE_TARGET  = 10         # TUNE: Endless-mode wave goal

    ACHIEVEMENTS = [
        # --- BRONZE : early / participation --------------------------------
        # ARCHIVE tier, rewritten 2026-08. These used to count Archive MODULES
        # ("bring any/every panel online"), which stopped meaning anything the
        # moment five of the six panels started shipping open -- arch_first would
        # have been earned on the title screen of a brand new save, and arch_full
        # would have collapsed into a duplicate of music_on. The Archive's real
        # progression now lives one level down, in what is inside each panel, so
        # that is what these count.
        Achievement("arch_first", "bronze", "Signal Acquired",
            "Recover your first CG.",
            earned=lambda: _ach_count_true(_ach_cg_flags()) >= 1, cat="ARCHIVE"),
        Achievement("music_on", "bronze", "Now Playing",
            "Restore the Music Room.",
            flag="archive_unlocked_music", cat="ARCHIVE"),
        # Was "records_open" (Lost Records access), which is now unconditional
        # and so was free at boot. Renamed rather than repointed in place: an old
        # profile keeps the retired id sitting in ach_earned, which is harmless
        # (platinum only ever asks whether the LIVE ids are all present), and the
        # new one correctly starts unearned.
        Achievement("roster_all", "bronze", "Names to Faces",
            "Put a name to everyone the registry has a slot for.",
            earned=lambda: _ach_complete_pair(_ach_roster_progress),
            progress=_ach_roster_progress, cat="ARCHIVE"),
        Achievement("side_first", "bronze", "Between the Lines",
            "Recover your first Side Story.",
            earned=lambda: _ach_count_true(_ach_side_story_flags()) >= 1, cat="STORIES"),
        Achievement("caught_once", "bronze", "The Exam Remembers",
            "Try to take back an answer you already gave.",   # vague: exam save-scum
            earned=lambda: _ach_scum_count() >= 1, cat="SECRET"),
        Achievement("hina_donotread", "bronze", "obviously read",
            "Some filenames are dares.",                       # vague: Hina's World DO_NOT_READ file
            cat="SECRET"),                                     # EXPLICIT: ach_grant("hina_donotread")

        # --- SILVER : real effort / hidden content -------------------------
        Achievement("arch_full", "silver", "Full Spectrum",
            "Recover every CG on record.",
            earned=lambda: _ach_complete(_ach_cg_flags),
            progress=lambda: _ach_progress(_ach_cg_flags),
            cat="ARCHIVE"),
        Achievement("wardrobe_all", "silver", "Costume Department",
            "Catch every last one of them in every last thing they own.",
            earned=lambda: _ach_complete(_ach_outfit_flags),
            progress=lambda: _ach_progress(_ach_outfit_flags),
            cat="ARCHIVE"),
        Achievement("side_half", "silver", "Supporting Cast",
            "Recover over half of the Side Stories.",
            earned=lambda: _ach_complete(_ach_side_story_flags, _ach_fraction_target(_ach_side_story_flags, 0.5)),
            progress=lambda: _ach_progress(_ach_side_story_flags, _ach_fraction_target(_ach_side_story_flags, 0.5)),
            cat="STORIES"),
        Achievement("beat_matsuda", "silver", "Boss? What Boss?",
            "Win a fight some people insist never happened.",  # vague: Matsuda boss fight
            flag="id_mode_unlocked", cat="SECRET"),
        Achievement("koto_clear", "silver", "Eight Bars",
            "Read the pattern all the way to the last one.",   # vague: Kotonoha Touhou mode
            flag="kotomode_cleared", cat="SECRET"),
        Achievement("scum_two", "silver", "Pattern of Behavior",
            "Push the same luck one time too many.",           # vague: exam bad-end path
            earned=lambda: _ach_scum_count() >= 2, cat="SECRET"),
        Achievement("date_win", "silver", "Hard Pass",
            "Mean every word of it, right to the end.",        # vague: Monika date mode (reject-to-win)
            cat="SECRET"),                                     # EXPLICIT: ach_grant("date_win")
        Achievement("hina_tender", "silver", "Let Her Be Little",
            "Leave the site the way you found her.",           # vague: Hina's World "tender" ending tone
            cat="SECRET"),                                     # EXPLICIT: ach_grant("hina_tender")
        Achievement("same_coin", "silver", "Same Coin",
            "See both faces.",                                 # vague: FINISH Tsubaki's "Heads" + "Tails"
            # _completed, NOT _unlocked: the unlock flags are availability and
            # get force-set by the dev all-content unlocks at boot / 0531.
            earned=lambda: bool(getattr(persistent, "cs_tsubaki_01_completed", False)) and bool(getattr(persistent, "cs_tsubaki_02_completed", False)),
            progress=lambda: (sum(1 for _f in ("cs_tsubaki_01_completed", "cs_tsubaki_02_completed") if getattr(persistent, _f, False)), 2),
            cat="STORIES"),
        Achievement("msbf_genres", "silver", "Genre Savvy",
            "Beat the script at all three of its own games.",  # vague: phase-3 genre-shift microgames
            earned=lambda: len(set(getattr(persistent, "msbf_micro_wins", None) or [])) >= 3,
            progress=lambda: (min(len(set(getattr(persistent, "msbf_micro_wins", None) or [])), 3), 3),
            cat="SECRET"),
        Achievement("tsuba_fell", "silver", "Camellias Fall Whole",
            "End the act nobody wrote the way camellias end.", # vague: Tsubaki mode, violence route
            cat="SECRET"),                                     # EXPLICIT: ach_grant("tsuba_fell")
        Achievement("tsuba_spare", "silver", "Unstrung",
            "Cut all five strings.",                            # Tsubaki mode, string-cut route
            cat="SECRET"),                                     # EXPLICIT: ach_grant("tsuba_spare")

        # --- GOLD : mastery / completion sweeps ----------------------------
        # READ, not merely recovered. side_first and side_half are about
        # collecting; the gold sweep should be about actually going through
        # them, and recovery no longer distinguishes anybody -- the end of
        # Chapter 0.5 hands over the whole catalog in one beat, so an
        # availability-gated "The Whole Story" was earned by finishing the
        # prologue without opening a single side story. Same reasoning as
        # same_coin, which has always used the _completed flags.
        Achievement("side_all", "gold", "The Whole Story",
            "Read every Side Story to the end.",
            earned=lambda: _ach_complete(_ach_side_story_done_flags),
            progress=lambda: _ach_progress(_ach_side_story_done_flags),
            cat="STORIES"),
        Achievement("koto_score", "gold", "Pro Gamer",
            "Post a frankly unreasonable score in the endless mode.",  # endless-mode score (matches blurb)
            earned=lambda: int(getattr(persistent, "kotomode_endless_hiscore", 0) or 0) >= ACH_KOTO_SCORE_TARGET,
            progress=lambda: (min(int(getattr(persistent, "kotomode_endless_hiscore", 0) or 0), ACH_KOTO_SCORE_TARGET), ACH_KOTO_SCORE_TARGET),
            cat="SECRET"),
        Achievement("koto_endless", "gold", "No Curtain Call",
            "Refuse to let the encore end.",                   # vague: Endless-mode waves
            earned=lambda: int(getattr(persistent, "kotomode_endless_wave", 0) or 0) >= ACH_KOTO_WAVE_TARGET,
            progress=lambda: (min(int(getattr(persistent, "kotomode_endless_wave", 0) or 0), ACH_KOTO_WAVE_TARGET), ACH_KOTO_WAVE_TARGET),
            cat="SECRET"),
        Achievement("matsuda_id", "gold", "She Swore She'd Never Build It",
            "Beat the version that wasn't supposed to exist.", # vague: Id Mode superboss
            cat="SECRET"),                                     # EXPLICIT: ach_grant("matsuda_id")
        Achievement("hina_guard", "gold", "No New Messages",
            "See everything, let nothing in.",                 # vague: full Hina's World run, guest never warmed
            cat="SECRET"),                                     # EXPLICIT: ach_grant("hina_guard")
        Achievement("msbf_no_downs", "gold", "No One Gets Written Out",
            "Win the fight that never happened with the whole party still standing.",
            cat="SECRET"),                                     # EXPLICIT: ach_grant("msbf_no_downs")
        Achievement("koto_nomiss", "gold", "Untouched",
            "Read every bar without dropping a single life.",  # vague: Kotonoha-mode no-miss clear
            cat="SECRET"),                                     # EXPLICIT: ach_grant("koto_nomiss")
        Achievement("koto_allcaps", "gold", "Eight Seals",
            "Capture every spell card in a single reading.",   # vague: Kotonoha-mode all captures
            cat="SECRET"),                                     # EXPLICIT: ach_grant("koto_allcaps")
        Achievement("date_flawless", "gold", "Never Once",
            "Say no every time. All night.", # vague: date mode, zero slips
            cat="SECRET"),                                     # EXPLICIT: ach_grant("date_flawless")
        Achievement("tsuba_mended", "gold", "The Needle of Noticing",
            "Cut every string without FIGHT or reset.",         # Tsubaki pacifist, no FIGHT selection or re-entry
            cat="SECRET"),                                     # EXPLICIT: ach_grant("tsuba_mended")

        # --- PLATINUM : reserved for 100% ----------------------------------
        Achievement("platinum", "platinum", "ENTER: Mastered",
            "Earn every other achievement.",
            cat="COMPLETION"),                                 # condition is special-cased
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
        persistent.ach_history.update(persistent.ach_earned)
        # MIGRATION (2026-07): "same_coin" briefly shipped keyed to the
        # cs_tsubaki_*_unlocked AVAILABILITY flags, which the dev all-content
        # unlocks force-set at boot -- so it self-granted on polluted saves.
        # Revoke it (earned AND history, or history would re-earn it on the
        # next sync) unless both _completed flags are honestly set.
        if ("same_coin" in persistent.ach_earned or "same_coin" in persistent.ach_history):
            if not (getattr(persistent, "cs_tsubaki_01_completed", False) and getattr(persistent, "cs_tsubaki_02_completed", False)):
                persistent.ach_earned.discard("same_coin")
                persistent.ach_history.discard("same_coin")

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

    def ach_condition_met(a):
        # Evaluate the achievement's OWN condition (not the locked-in set).
        # Platinum stays strictly "all others CURRENTLY earned" -- it never
        # carries over from history on its own.
        if a.tier == "platinum":
            return all(x.id in persistent.ach_earned
                        for x in ACHIEVEMENTS if x.tier != "platinum")
        # Ever earned before = the thing HAPPENED; a dev clear (or a volatile
        # flag being wiped) doesn't un-happen it. This is what makes previously
        # earned explicit/volatile achievements read READY after CLEAR ALL and
        # re-earn on the next sync instead of demanding a replay.
        if a.id in (getattr(persistent, "ach_history", None) or ()):
            return True
        try:
            if a.earned is not None:
                return bool(a.earned())
            if a.flag is not None:
                return bool(getattr(persistent, a.flag, False))
        except Exception:
            return False
        return False   # explicit-only: only ever set via ach_grant

    def ach_sync(notify=True):
        """Auto-unlock pass: evaluate all conditions and lock in newly-true ones
        (non-platinum first so platinum can see them in the same pass).
        EVERY newly-earned achievement gets a toast -- the queue plays them one
        at a time -- UNLESS the pass unlocks more than ACH_TOAST_BATCH_MAX at
        once. That is a reconciliation (retrofitted save, dev reset with content
        already unlocked), not a moment, so it stays silent. One action tripping
        two conditions (a story unlock + side_first, say) toasts both.
        DEV: a no-op in developer builds while the dev shop's session-only
        AUTO-UNLOCK toggle is off; release builds always sync."""
        _ach_ensure_store()
        if config.developer and not _ach_rt.autounlock:
            return []
        newly = []
        for a in ACHIEVEMENTS:
            if a.tier == "platinum":
                continue
            if a.id not in persistent.ach_earned and ach_condition_met(a):
                persistent.ach_earned.add(a.id)
                newly.append(a)
        for a in ACHIEVEMENTS:
            if a.tier != "platinum":
                continue
            if a.id not in persistent.ach_earned and ach_condition_met(a):
                persistent.ach_earned.add(a.id)
                newly.append(a)
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
        # "start the game" (-> the dev date picker in developer builds). Always
        # return None here so the show event is a pure side effect.
        ach_sync()
        return None

    def ach_grant(aid, notify=True):
        """Explicit unlock from a story beat. Idempotent."""
        _ach_ensure_store()
        a = ACH_BY_ID.get(aid, None)
        if a is None or aid in persistent.ach_earned:
            return
        persistent.ach_earned.add(aid)
        if notify:
            ach_push_toast(a)
        # A grant can complete the set -> let sync trip platinum (and anything
        # else that just became true).
        ach_sync(notify=notify)

    def ach_lock(*ids):
        """Lock in specific achievements whose condition is CURRENTLY met, and
        DEFER their toasts. For VOLATILE derived state that gets wiped before
        the Archive can sync -- the exam-guard scum flags are cleared on the
        next New Game, so a caught save-scum must be recorded into the permanent
        ach_earned set the instant it happens (see exam_guard_mark_scummed).
        The toast CANNOT play here: the catch labels end in renpy.utter_restart()
        (bad ending: full_restart), which kills a live toast mid-animation and
        rebuilds _ach_rt -- and once the id sits in ach_earned, no later
        ach_sync would ever toast it. So the ids are parked in the persistent
        ach_toast_pending list and _ach_drain_pending() plays them at the title
        screen the restart lands on (or right after a load).
        Conditional on ach_condition_met so e.g. scum_two only locks at 2+."""
        _ach_ensure_store()
        pending = list(getattr(persistent, "ach_toast_pending", None) or [])
        for aid in ids:
            a = ACH_BY_ID.get(aid, None)
            if a is not None and aid not in persistent.ach_earned and ach_condition_met(a):
                persistent.ach_earned.add(aid)
                if aid not in pending:
                    pending.append(aid)
        persistent.ach_toast_pending = pending

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
        persistent.ach_toast_pending = []
        del _ach_rt.queue[:]
        _ach_rt.started = None
        try:
            renpy.save_persistent()
        except Exception:
            pass
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
            ach_push_toast(a)
            try:
                renpy.save_persistent()
            except Exception:
                pass
        return None

    def ach_dev_revoke(aid):
        """DEV: HARD relock -- removes the id from ach_earned AND ach_history,
        so the achievement reads LOCKED and its REAL trigger must fire again.
        (CLEAR ALL is the soft reset: it keeps history, so everything previously
        earned stays READY and carries back over on sync.)"""
        _ach_ensure_store()
        persistent.ach_earned.discard(aid)
        persistent.ach_history.discard(aid)
        try:
            renpy.save_persistent()
        except Exception:
            pass
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

    def _ach_drain_pending(force=False):
        """Play the toasts ach_lock() parked in persistent.ach_toast_pending.
        Runs at the start of every interaction (config.interact_callbacks) but
        only fires ON THE MAIN MENU -- the exam-guard catch labels still say a
        couple of lines between ach_lock and their utter_restart, and draining
        there would start a toast the restart then destroys, losing it for good.
        Both restarts land on the title screen, so that is where delivery is
        guaranteed. force=True (the after-load path) skips the gate: a load can
        only happen from a menu, and afterwards the game is safely interactive."""
        pending = getattr(persistent, "ach_toast_pending", None)
        if not pending:
            return
        if not force and not renpy.get_screen("main_menu"):
            return
        persistent.ach_toast_pending = []
        try:
            renpy.save_persistent()
        except Exception:
            pass
        for aid in pending:
            ach_push_toast(aid)

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

    if _ach_drain_pending not in config.interact_callbacks:
        config.interact_callbacks.append(_ach_drain_pending)

    # -- SYNC ON LOAD ---------------------------------------------------------
    def _ach_after_load():
        ach_sync()
        _ach_drain_pending(force=True)
    if _ach_after_load not in config.after_load_callbacks:
        config.after_load_callbacks.append(_ach_after_load)


# =============================================================================
# UNLOCK TOAST  (compact bottom-right card + chime; see TOAST ENGINE above)
# =============================================================================
transform ach_toast_drive:
    subpixel True
    function _ach_toast_anim

screen achievement_toaster():
    # Hosted by config.always_shown_screens -- present in every context, renders
    # NOTHING while the queue is empty. Above the dev shop (300) so GRANTs are
    # visible while the shop is open.
    zorder 400

    if _ach_rt.queue:
        $ _a = ACH_BY_ID.get(_ach_rt.queue[0], None)
        if _a is not None:
            $ _t = ACH_TIERS.get(_a.tier, ACH_TIERS["bronze"])

            # Fixed-size card, two tight lines: [tier] UNLOCKED / title.
            # NOTE: no yfill anywhere -- a fill inside this size-less frame is
            # what stretched the old toast down the whole right edge of the
            # screen (same gotcha as the custom say UI's themed frames).
            frame:
                style "ach_toast_frame"
                anchor (1.0, 1.0)
                pos (0.988, 0.965)
                ysize 62
                at ach_toast_drive

                hbox:
                    spacing 0

                    # tier rail
                    add Solid(_t["color"]) xysize (5, 62)
                    null width 14

                    vbox:
                        yalign 0.5
                        spacing 2

                        hbox:
                            spacing 7
                            frame:
                                background Solid(_t["color"])
                                padding (6, 1)
                                yalign 0.5
                                text _t["label"] style "ach_toast_chip"
                            text "UNLOCKED" style "ach_toast_kicker" yalign 0.5

                        text _a.title style "ach_toast_title" layout "nobreak"

                    null width 16


# =============================================================================
# THE ACHIEVEMENTS SCREEN  (Archive slot 6)
# Modal overlay shown OVER the archive hub, mirroring character_stories: return
# is Hide("achievements"), which reveals the hub underneath.
# =============================================================================
screen achievements():
    modal True

    # Refresh derived unlocks every time it opens (also toasts anything newly met).
    on "show" action Function(ach_refresh)

    default ach_filter = "all"

    use archive_backdrop

    key "game_menu" action Hide("achievements")
    key "K_ESCAPE" action Hide("achievements")

    $ _ach_all = ACHIEVEMENTS
    $ _ach_total = len(_ach_all)
    $ _ach_done = ach_earned_count()
    $ _ach_pct = int(round(100.0 * _ach_done / _ach_total)) if _ach_total else 0
    $ _ach_tc = ach_tier_counts()
    $ _ach_shown = [a for a in _ach_all if ach_filter == "all" or a.tier == ach_filter]
    $ _ach_plat_done = ach_is_earned("platinum")

    frame:
        style "archive_shell_frame"
        padding (24, 20)
        at archive_frame_enter()

        vbox:
            spacing 12

            use archive_header("ACHIEVEMENTS", Hide("achievements"))

            # ---- readout strip: overall + per-tier tally --------------------
            # The shared strip (archive.rpy), transcluding the tier tally into
            # its right slot -- the layout gotchas live there, once.
            use archive_readout("TROPHY INDEX // %d/%d UNLOCKED // %d%%" % (_ach_done, _ach_total, _ach_pct), right_slot=True):
                for _tk in ACH_TIER_ORDER:
                    text "%s %d/%d" % (ACH_TIERS[_tk]["short"], _ach_tc[_tk][0], _ach_tc[_tk][1]):
                        style "archive_meta_text"
                        color ACH_TIERS[_tk]["glow"]
                        yalign 0.5

            # ---- tier filter chips -----------------------------------------
            # The chip row keeps its own hbox (it wants the spacing), but it and the
            # right-hand status sit in a `fixed` so the status actually reaches the
            # right edge -- see the note on the readout strip above.
            fixed:
                xsize 1150
                ysize 40

                hbox:
                    spacing 10
                    xpos 0
                    yalign 0.5

                    for _fk, _flabel in [("all", "ALL"), ("bronze", "BRONZE"), ("silver", "SILVER"), ("gold", "GOLD"), ("platinum", "PLATINUM")]:
                        textbutton _flabel:
                            style "ach_filter_button"
                            action SetScreenVariable("ach_filter", _fk)
                            selected (ach_filter == _fk)

                hbox:
                    spacing 12
                    xanchor 1.0
                    xpos 1150
                    yalign 0.5

                    # Dev-only: opens the grant/revoke shop. Hidden in release builds.
                    if config.developer:
                        textbutton "DEV SHOP":
                            style "ach_dev_pill"
                            yalign 0.5
                            action Show("ach_dev_shop")

                    text ("PLATINUM SECURED" if _ach_plat_done else "PLATINUM // LOCKED"):
                        style "archive_meta_text"
                        color (ACH_TIERS["platinum"]["glow"] if _ach_plat_done else "#5d7886")
                        yalign 0.5

            # ---- scrolling achievement list --------------------------------
            viewport:
                xsize 1150
                ysize 396
                mousewheel True
                scrollbars "vertical"
                style_prefix "archive_sv"

                vbox:
                    spacing 8

                    for a in _ach_shown:
                        $ _e = ach_is_earned(a)
                        $ _t = ACH_TIERS[a.tier]
                        $ _rail = _t["glow"] if _e else "#33414d"

                        frame:
                            xsize 1116
                            ysize 86
                            background Solid("#08131fdd" if _e else "#060b12b0")
                            padding (0, 0)

                            hbox:
                                yfill True
                                # xfill so the `null width 1 xfill True` below has
                                # somewhere to expand into -- without it this hbox
                                # shrink-wraps and the status chip ends up butted
                                # against the objective text instead of sitting on
                                # the row's right edge.
                                xfill True

                                add Solid(_rail) xysize (6, 86)
                                null width 16

                                # tier badge
                                vbox:
                                    yalign 0.5
                                    xsize 104
                                    frame:
                                        background Solid(_t["color"] if _e else "#1a2731")
                                        padding (10, 4)
                                        xalign 0.5
                                        text _t["label"]:
                                            style ("archive_chip_on_text" if _e else "archive_chip_off_text")

                                null width 18

                                # title + objective (+ progress)
                                vbox:
                                    yalign 0.5
                                    xsize 604
                                    spacing 3

                                    text a.title:
                                        style ("ach_row_title" if _e else "ach_row_title_locked")
                                    text a.blurb style "ach_row_blurb"

                                    if a.progress is not None:
                                        $ _cur, _tgt = a.progress()
                                        $ _frac = 0.0 if not _tgt else max(0.0, min(1.0, float(_cur) / float(_tgt)))
                                        hbox:
                                            spacing 10
                                            yalign 0.5
                                            fixed:
                                                xysize (240, 6)
                                                yalign 0.5
                                                add Solid("#0e1c26") xysize (240, 6)
                                                add Solid(_t["glow"]) xysize (max(0, int(240 * _frac)), 6)
                                            text "%d/%d" % (_cur, _tgt) style "ach_progress_text" yalign 0.5

                                null width 1 xfill True

                                # status chip
                                vbox:
                                    yalign 0.5
                                    if _e:
                                        frame:
                                            background Solid(_t["color"])
                                            padding (12, 5)
                                            xalign 1.0
                                            text "UNLOCKED" style "archive_chip_on_text"
                                    else:
                                        frame:
                                            background Solid("#12202a")
                                            padding (12, 5)
                                            xalign 1.0
                                            text "LOCKED" style "archive_chip_off_text"

                                null width 18

            # ---- footer ----------------------------------------------------
            fixed:
                xsize 1150
                ysize 16

                add Solid("#345a6b") xysize (5, 5) xpos 0 yalign 0.5
                text "ACHIEVEMENTS.SYS :: [_ach_done] OF [_ach_total] SECURED":
                    style "archive_footer_text"
                    xpos 13
                    yalign 0.5
                text "PLATINUM = 100% COMPLETION":
                    style "archive_footer_text"
                    xanchor 1.0
                    xpos 1150
                    yalign 0.5

    # Brackets sized to the 1200-wide shell frame (matches char_stories); the
    # old 1160 values were narrower than the frame and clipped the right edge.
    use archive_shell_brackets()


# =============================================================================
# DEV ACHIEVEMENT SHOP  (config.developer only; opened from the DEV SHOP pill
# on the achievements screen). Nier-style manual control: flip AUTO-UNLOCK off
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

                textbutton "SYNC NOW":
                    style "ach_filter_button"
                    action Function(ach_refresh)

                null width 1 xfill True

                text "EARNED [_done]/%d  //  AUTO-UNLOCK is session-only  //  CLEAR ALL keeps READY history; REVOKE hard-relocks" % len(ACHIEVEMENTS):
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
# =============================================================================
style ach_row_title:
    font gui.interface_font
    color "#eafcff"
    size 22
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style ach_row_title_locked is ach_row_title:
    color "#8195a2"
    outlines [(2, "#02040b", 0, 0)]

style ach_row_blurb:
    font gui.interface_font
    color "#9fc9d6"
    size 15
    outlines [(1, "#02040b", 0, 0)]

style ach_progress_text:
    font gui.interface_font
    color "#7fcfe0"
    size 12
    kerning 1.0
    outlines [(1, "#02040b", 0, 0)]

style ach_filter_button:
    background Solid("#07111dcc")
    hover_background Solid("#12314af2")
    selected_background Solid("#12314af2")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (16, 6)

style ach_filter_button_text:
    font gui.interface_font
    color "#9fc0cd"
    hover_color "#ffffff"
    selected_color "#eafcff"
    size 15
    bold True
    outlines [(1, "#02040b", 0, 0)]

# ---- dev-only pill (opens the shop from the achievements menu) ----
style ach_dev_pill:
    background Solid("#2a0d16")
    hover_background Solid("#5b1526")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (12, 5)

style ach_dev_pill_text:
    font gui.interface_font
    color "#ff9fb4"
    hover_color "#ffffff"
    size 13
    bold True
    kerning 1.0
    outlines [(1, "#02040b", 0, 0)]

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
    background Solid("#05090ff2")
    padding (0, 0)

style ach_toast_chip:
    font gui.interface_font
    color "#04121a"
    size 10
    bold True

style ach_toast_kicker:
    font gui.interface_font
    color "#7fcfe0"
    size 10
    kerning 2.0
    bold True
    outlines [(1, "#02040b", 0, 0)]

style ach_toast_title:
    font gui.interface_font
    color "#eafcff"
    size 17
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]


# =============================================================================
# CONTENT REACHABILITY AUDIT  (developer builds only)
# -----------------------------------------------------------------------------
# WHY THIS EXISTS. Three of the achievements above -- and therefore platinum --
# are "collect every X" sweeps read live from their catalogs, which is what makes
# them scale for free when content is added. The flip side is that adding a
# catalogue ENTRY without also adding the thing that unlocks it makes that sweep,
# and platinum, quietly impossible: the CG simply never appears, and nothing
# anywhere says why. That failure is invisible in play and invisible to lint.
#
# So this walks the project's own source at init and checks that every
# catalogued item has somewhere it can actually come from:
#     CG            -> a `cg_unlock("Title")` call site
#     side story    -> a `cs_mark_completed("label")` call site, and something
#                      that sets its _unlocked flag
#     outfit        -> a `show <tag> ... <attr>` somewhere
#     track         -> a `play`/`queue` naming its audio alias or its path
# It reports and never raises: a warning is right for content that is merely
# not wired up yet (a story written before its unlock beat exists), and a hard
# error here would block booting the game to work on exactly that.
#
# Run it any time with `ach_audit_content()` from the console. It is skipped
# entirely in release builds -- it reads every .rpy in the project.
# =============================================================================

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

        # --- the indexes every check below reads from -------------------------
        # Two of the four checks ask a line-scoped question -- "is there a line
        # that PLAYS this track?", "is there a line that SHOWS this tag wearing
        # this attribute?" -- and each one used to answer it with its own regex
        # sweep of the whole 4 MB blob: `\b(play|queue)\b[^\n]*\b<needle>\b`,
        # once per needle, ~4 needles per track, 56 tracks. That pattern makes
        # the engine walk to the end of the line and backtrack at every one of
        # the 485 play/queue keywords in the project, and the miss case then
        # rebuilt a 4 MB blob.lower() on top. Measured: 8.5 SECONDS of every
        # single boot, which is most of the game's startup time.
        #
        # The questions are line-scoped, so the answers live in two small
        # indexes built in ONE pass: the text following each play/queue keyword
        # (~11 KB), and the text following each `show <tag>` keyed by tag. Same
        # answers, measured at 0.06s. The plain `in line` guards are C-speed
        # substring tests that keep the regexes off the ~110k lines that cannot
        # match. Keep any new check line-scoped and it costs nothing.
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
            """Every string literal passed to `func(...)` anywhere in the source."""
            found = set()
            for call in re.findall(r"\b%s\s*\(([^)]*)\)" % func, blob):
                for literal in re.findall(r"""["']([^"']+)["']""", call):
                    found.add(literal.strip().lower())
            return found

        problems = []

        # --- CGs --------------------------------------------------------------
        unlocked_names = quoted_args("cg_unlock")
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
        # `play music hopeless` counts for mod_assets/bgm/13am.ogg.
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
