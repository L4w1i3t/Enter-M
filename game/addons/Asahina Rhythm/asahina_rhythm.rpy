# Asarhythm — a four-lane, audio-clock rhythm cabinet staged like FNF.
# One persistent CDD draws two cameras. The WORLD camera (stage, cast, rating
# pops) pans to whoever carries the measure and punches in on the downbeat; the
# HUD camera (strums, notes, bars) only takes the bump. Screen language changes
# for setup, pause and results, never per note. Displayables are cached;
# Renders are built fresh every frame.
#
# asahina_rhythm_fx.rpy draws the chart-cued stage effects, and
# asahina_rhythm_menu.rpy holds song select, its music and its face-off.

default persistent.asahina_rhythm_records = {}
default persistent.asahina_rhythm_cleared = False
default persistent.asahina_rhythm_input_ms = 0
default persistent.asahina_rhythm_visual_ms = 0
# Scroll speed multiplies AR_SCROLL. Tempo scroll replaces it with the song's BPM
# over AR_TEMPO_BPM, so notes a beat apart sit the same distance apart in every
# song.
default persistent.asahina_rhythm_speed = AR_SPEED_DEFAULT
default persistent.asahina_rhythm_tempo_scroll = False
default persistent.asahina_rhythm_downscroll = False
default persistent.asahina_rhythm_practice = False
default persistent.asahina_rhythm_autoplay = False
# The song the player last chose, so returning from a run lands back on it.
default persistent.asahina_rhythm_last_song = None
# Song select's switches: modifier ids from AR_HARDER and AR_EASIER (practice
# and autoplay keep their own flags above), and whether the player sings both sides.
default persistent.asahina_rhythm_mods = []
default persistent.asahina_rhythm_duet = False

# MIGRATION (2026-09): 1.0x now means what 2.0x used to (AR_SCROLL went from 520
# to 1040 px/s), so a stored speed is halved once and plays exactly as fast as
# before. The exception is a 1.0 that no earlier migration touched: that is a
# fresh profile's new default or the old untouched default, and both become the
# new 1.0x. asahina_rhythm_speed_migrated is from a same-day step that moved an
# untouched 1.0 to 2.0; where it is set, the 1.0 was a real pick in the old
# units. init 50 runs after the defaults (0).
default persistent.asahina_rhythm_speed_rescaled = False

init 50 python:
    if not persistent.asahina_rhythm_speed_rescaled:
        _ar_old_speed = persistent.asahina_rhythm_speed
        if _ar_old_speed is not None and (_ar_old_speed != 1.0 or persistent.asahina_rhythm_speed_migrated):
            persistent.asahina_rhythm_speed = round(_ar_old_speed / 2.0, 3)
        persistent.asahina_rhythm_speed_rescaled = True

# The stage art as a VN backdrop for the story prelude and outros.
image asarhythm_stage = "addons/Asahina Rhythm/art/stage.png"

init -1 python:
    import bisect as ar_bisect
    import json as ar_json
    import math as ar_math
    import random as ar_random
    import time as ar_time
    import pygame_sdl2 as ar_pg
    from asahina_rhythm_core import (normalize_chart, RhythmSession, SongClock, HIT_WINDOW,
                                     camera_plan, camera_focus, EXCLUSIVE_MODIFIERS as AR_EXCLUSIVE,
                                     FIGHT_FLOOR as AR_FIGHT_FLOOR, TIERS as AR_TIERS,
                                     WIDE_TIMING as AR_WIDE_TIMING)

    AR_ROOT = "addons/Asahina Rhythm/"
    AR_ART = AR_ROOT + "art/"
    AR_UI = AR_ART + "ui/"
    AR_CHANNEL = "asahina_rhythm"
    AR_COUNTDOWN_READY = "assets/audio/sfx/asarhythm/Ready.ogg"
    AR_COUNTDOWN_SET = "assets/audio/sfx/asarhythm/Set.ogg"
    AR_COUNTDOWN_GO = "assets/audio/sfx/asarhythm/Go.ogg"
    AR_COUNTDOWN_READY_CH = "asahina_rhythm_countdown_ready"
    AR_COUNTDOWN_SET_CH = "asahina_rhythm_countdown_set"
    AR_COUNTDOWN_GO_CH = "asahina_rhythm_countdown_go"
    AR_FONT = "assets/gui/font/RifficFree-Bold.ttf"
    AR_UI_FONT = "assets/fonts/NovaSquare-Regular.ttf"
    AR_COLORS = ("#c874ed", "#52d5ef", "#87e766", "#fa698b")
    AR_POSES = ("left", "down", "up", "right")
    AR_DIRS = ((-1, 0), (0, 1), (0, -1), (1, 0))
    AR_CAST = {"opponent": "asahina", "player": "asahiko"}
    AR_PINK, AR_CYAN, AR_GOLD, AR_INK = "#f06ba8", "#5fd8e8", "#ffe08a", "#160f24"
    AR_RATING = {"SICK!": ("SICK!!", "#ffe066"), "GOOD": ("GOOD", "#8ff0a4"),
                 "OKAY": ("OKAY", "#8fc8ff"), "YUCKY": ("YUCKY", "#c7a0ff"),
                 "MISS": ("MISS", "#ff6b8a"), "BROKEN": ("HOLD BROKEN", "#ff6b8a")}

    # ---- world camera ------------------------------------------------------
    # The stage master at native pixels. At zoom 1 the camera frames 1280x720 of
    # it, leaving ~390px to pan through. Everything below is in world pixels.
    AR_WORLD = (1672, 941)
    AR_FEET_Y = 850
    # The singers stand 692px apart, clear of the speaker's cones (552 before Sep
    # 13 2026). Each side's shot moved out with its singer, so framing is unchanged.
    AR_SPOT_X = {"opponent": 490, "player": 1182}
    AR_SHOT = {"opponent": (650, 590, 1.05), "player": (1022, 590, 1.05), "center": (836, 576, .99)}
    AR_CAM_EASE = .40       # FNF's 0.04-per-frame lerp at 60fps is a ~0.4s time constant.
    AR_ZOOM_EASE = .60
    AR_NUDGE = 16           # The camera leans this far toward the framed singer's arrow.
    AR_BUMP_WORLD, AR_BUMP_HUD, AR_BUMP_FALL = .018, .030, .24

    # ---- HUD ---------------------------------------------------------------
    # FNF's strum geometry at 1280 wide: 110px lane pitch, 106px arrows.
    AR_LANE = 110
    AR_STRUM_LEFT = (92, 732)   # Left edge of lane 0: opponent, player.
    AR_STRUM_Y = (100, 620)     # Receptor centres: upscroll, downscroll.
    AR_SCROLL = 1040.0          # Note travel in px/s at scroll speed 1.0.
    AR_SPEED_MIN, AR_SPEED_MAX, AR_SPEED_DEFAULT, AR_SPEED_STEP = .3, 1.5, 1.0, .05
    # Tempo scroll runs a song at this tempo at 1.0x, whatever the speed setting.
    # 120 is the usual default tempo, and the story song's 115 is close enough
    # that it plays about the same either way.
    AR_TEMPO_BPM = 120.0
    AR_DIZZY_SWING = 42.0       # Dizzy's widest sideways swing, in px.

    # ---- song select -------------------------------------------------------
    # The song list's fixed row pitch. PEEK is how much of the row after the last
    # whole one stays visible: the list is cut off mid-row so that having more
    # songs than fit is legible without reading anything.
    AR_SONG_ROW, AR_SONG_GAP, AR_SONG_VIEW, AR_SONG_PEEK = 54, 5, 2, 22
    AR_SONG_PITCH = AR_SONG_ROW + AR_SONG_GAP
    AR_LIST_W = 604          # The left column, and the song rows across it.

    # ---- modifiers -----------------------------------------------------------
    # (id, name, what it does). HARDER ones keep records, and a clear remembers
    # which of them were on. EASIER ones, practice included, keep no records or
    # rewards. Names and descriptions stay plain: these are controls.
    AR_HARDER = (
        ("dizzy", "DIZZY", "Notes swing side to side on their way to the outlines."),
        ("vanish", "VANISH", "Notes fade out before they reach the outlines."),
        ("mirror", "MIRROR", "The chart is flipped left to right."),
        ("no_miss", "NO MISSES", "One miss ends the song."),
        ("flawless", "FLAWLESS", "Anything but SICK!! ends the song, and so does a miss."),
        ("fights_back", "FIGHTS BACK", "Asahina's notes push the bar toward her side. Only your misses can finish you."),
    )
    AR_EASIER = (
        ("practice", "PRACTICE", "The bar can't run out. No records or rewards."),
        ("wide_timing", "WIDE TIMING", "Hit windows are half again as wide. No records or rewards."),
        ("half_damage", "HALF DAMAGE", "Misses cost half as much health. No records or rewards."),
        ("autoplay", "AUTOPLAY", "The song plays itself, so you can watch the chart. No records or rewards."),
    )
    AR_MOD_NAMES = dict((mod, name) for mod, name, hint in AR_HARDER + AR_EASIER)
    AR_MOD_NAMES["duet"] = "DUET"
    AR_MOD_ORDER = ("duet",) + tuple(mod for mod, name, hint in AR_HARDER + AR_EASIER)
    AR_CHALLENGES = frozenset(mod for mod, name, hint in AR_HARDER)
    # These two are not modifier ids the session accepts; each is its own
    # constructor argument with its own persistent flag, so they never reach
    # normalize_modifiers (which refuses an id it does not know).
    AR_FLAGS = {"practice": "asahina_rhythm_practice", "autoplay": "asahina_rhythm_autoplay"}
    AR_SWITCHES = frozenset(mod for mod, name, hint in AR_HARDER + AR_EASIER if mod not in AR_FLAGS)

    AR_KEYS_SOLO = {ar_pg.K_LEFT: 0, ar_pg.K_d: 0, ar_pg.K_DOWN: 1, ar_pg.K_f: 1,
                    ar_pg.K_UP: 2, ar_pg.K_j: 2, ar_pg.K_RIGHT: 3, ar_pg.K_k: 3}
    # A duet's left hand sings Asahina's lanes (columns 4-7) and its right hand the player's.
    AR_KEYS_DUET = {ar_pg.K_a: 4, ar_pg.K_s: 5, ar_pg.K_d: 6, ar_pg.K_f: 7,
                    ar_pg.K_j: 0, ar_pg.K_k: 1, ar_pg.K_l: 2, ar_pg.K_SEMICOLON: 3,
                    ar_pg.K_LEFT: 0, ar_pg.K_DOWN: 1, ar_pg.K_UP: 2, ar_pg.K_RIGHT: 3}

    if not renpy.music.channel_defined(AR_CHANNEL):
        renpy.music.register_channel(AR_CHANNEL, mixer="music", loop=False,
                                     stop_on_mute=False)
    if not renpy.music.channel_defined(AR_COUNTDOWN_READY_CH):
        renpy.music.register_channel(AR_COUNTDOWN_READY_CH, mixer="sfx", loop=False,
                                     stop_on_mute=False)
    if not renpy.music.channel_defined(AR_COUNTDOWN_SET_CH):
        renpy.music.register_channel(AR_COUNTDOWN_SET_CH, mixer="sfx", loop=False,
                                     stop_on_mute=False)
    if not renpy.music.channel_defined(AR_COUNTDOWN_GO_CH):
        renpy.music.register_channel(AR_COUNTDOWN_GO_CH, mixer="sfx", loop=False,
                                     stop_on_mute=False)

    def ar_resolve_audio(chart):
        source = chart["audio"]
        filename = getattr(audio, source, None) if "/" not in source and "." not in source else source
        if not isinstance(filename, str) or not renpy.loadable(filename):
            raise ValueError("The song '%s' is missing. Choose an existing audio alias or file." % source)
        return filename

    def ar_load_chart(path):
        with renpy.file(path) as source:
            chart = normalize_chart(ar_json.loads(source.read().decode("utf-8-sig")))
        ar_resolve_audio(chart)
        return chart

    def ar_catalog():
        songs, errors = [], []
        # A protected build lists its private-bundle members LOWERCASED
        # ("addons/asahina rhythm/charts/home.json"), so match without case.
        # Loading by the listed name still works: file lookups ignore case.
        root = (AR_ROOT + "charts/").lower()
        for path in sorted(renpy.list_files()):
            name = path.lower()
            if name.startswith(root) and name.endswith(".json") and "/" not in name[len(root):]:
                try:
                    songs.append(ar_load_chart(path))
                except (ValueError, TypeError, OSError) as exc:
                    errors.append("%s: %s" % (path.rsplit("/", 1)[-1], exc))
        return songs, errors

    # Digesting a 900-note chart is not free, and song select now asks every row
    # in the list for its record. The cache holds the notes list it keyed, so an
    # id() can never be reused by a later chart while its entry is still live.
    AR_KEY_CACHE = {}

    def ar_record_key(chart, duet=False):
        # Recharting a song must not compare incomparable note totals. A small
        # deterministic digest keeps previous versions' scores available.
        # Fanfares change what a run can score, so a chart that has any hashes
        # them too; a chart without them keeps the key it always had. A duet is
        # a different game and keeps its own records.
        import hashlib
        notes = chart["notes"]
        cached = AR_KEY_CACHE.get(id(notes))
        if cached is not None and cached[0] is notes and cached[1] == chart["id"]:
            key = cached[2]
        else:
            fanfare = [[cue["time"], cue["length"]] for cue in chart.get("effects", ()) if cue["kind"] == "fanfare"]
            content = dict(notes=notes, fanfare=fanfare) if fanfare else notes
            payload = ar_json.dumps(content, sort_keys=True, separators=(",", ":"))
            key = chart["id"] + ":" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
            if len(AR_KEY_CACHE) > 64:
                AR_KEY_CACHE.clear()
            AR_KEY_CACHE[id(notes)] = (notes, chart["id"], key)
        return key + ":duet" if duet else key

    def ar_best(chart, duet=False):
        return (persistent.asahina_rhythm_records or {}).get(ar_record_key(chart, duet), {})

    def ar_record_result(chart, result):
        if not result.get("eligible", False) or result["outcome"] == "quit":
            return
        records = dict(persistent.asahina_rhythm_records or {})
        key = ar_record_key(chart, result.get("duet", False))
        old = records.get(key, {})
        entry = dict(old)
        entry["attempts"] = int(old.get("attempts", 0)) + 1
        entry["title"] = chart["title"]
        if result["outcome"] == "clear":
            entry["clears"] = int(old.get("clears", 0)) + 1
            persistent.asahina_rhythm_cleared = True
            current_best = (result["score"], result["accuracy"], result["max_combo"], -result["misses"])
            previous_best = (old.get("score", -1), old.get("accuracy", 0), old.get("max_combo", 0), -old.get("misses", 0))
            if current_best > previous_best:
                entry.update(score=result["score"], accuracy=result["accuracy"],
                             rank=result["rank"], misses=result["misses"], max_combo=result["max_combo"])
                result["new_record"] = True
            # The harder modifiers a clear was earned under, remembered per song.
            earned = set(result.get("modifiers", ())) & AR_CHALLENGES
            known = set(old.get("mod_clears", ()))
            if earned - known:
                entry["mod_clears"] = sorted(earned | known)
                result["new_mod_clears"] = sorted(earned - known)
        records[key] = entry
        persistent.asahina_rhythm_records = records
        renpy.save_persistent()

    def ar_active_mods():
        """The modifier ids the next run plays with. Stale ids and clashing pairs never reach the session."""
        mods = set(mod for mod in (persistent.asahina_rhythm_mods or ()) if mod in AR_SWITCHES)
        if persistent.asahina_rhythm_duet:
            mods.add("duet")
        for pair in AR_EXCLUSIVE:
            if pair <= mods:
                # Only a hand-edited profile reaches this; duet and flawless win.
                mods.discard("fights_back" if "duet" in pair else "no_miss")
        return frozenset(mods)

    def ar_mod_on(mod):
        if mod in AR_FLAGS:
            return bool(getattr(persistent, AR_FLAGS[mod]))
        return mod in ar_active_mods()

    def ar_mod_available(mod):
        # Asahina can't fight back when the player is singing her part.
        return not (mod == "fights_back" and persistent.asahina_rhythm_duet)

    def ar_toggle_mod(mod):
        if mod in AR_FLAGS:
            setattr(persistent, AR_FLAGS[mod], not getattr(persistent, AR_FLAGS[mod]))
            return
        chosen = set(m for m in (persistent.asahina_rhythm_mods or ()) if m in AR_SWITCHES)
        if mod in chosen:
            chosen.discard(mod)
        elif ar_mod_available(mod):
            chosen.add(mod)
            # The newer switch wins its pair.
            for pair in AR_EXCLUSIVE:
                if mod in pair:
                    chosen -= pair - set([mod])
        persistent.asahina_rhythm_mods = sorted(chosen)

    def ar_set_duet(on):
        persistent.asahina_rhythm_duet = bool(on)
        if on:
            persistent.asahina_rhythm_mods = [m for m in (persistent.asahina_rhythm_mods or ()) if m != "fights_back"]

    def ar_clear_mods():
        persistent.asahina_rhythm_mods = []
        for field in AR_FLAGS.values():
            setattr(persistent, field, False)

    def ar_mod_names(mods, practice=False, autoplay=False):
        """A run's switches as display names, in menu order. Autoplay stands in for
        practice: a song that plays itself was never a practice run of anything."""
        labels = ["AUTOPLAY"] if autoplay else (["PRACTICE"] if practice else [])
        return labels + [AR_MOD_NAMES[mod] for mod in AR_MOD_ORDER if mod in mods and mod not in AR_FLAGS]

    def ar_mod_summary(mods, practice=False, autoplay=False):
        """The next run's switches on one line, for song select.

        The two that cost a run its records lead. Song select shortens this line
        from the right, and those are the last switches that should be cut. Both
        can show here, unlike ar_mod_names: each has its own lit tile on the page."""
        labels = [AR_MOD_NAMES[mod] for mod, on in (("autoplay", autoplay), ("practice", practice)) if on]
        labels += [AR_MOD_NAMES[mod] for mod in AR_MOD_ORDER if mod not in AR_FLAGS and mod in mods]
        return "   •   ".join(labels) if labels else "NO MODIFIERS"

    def ar_fail_text(result):
        """Why a run ended early, for the results card; empty unless it failed."""
        if result.get("outcome") != "failed":
            return ""
        at = ar_time_label(result.get("song_time", 0))
        rule = result.get("fail_reason")
        if rule in AR_MOD_NAMES:
            return "%s ended the run at %s." % (AR_MOD_NAMES[rule], at)
        return "The bar ran out at %s." % at

    def ar_window_text(mods=()):
        scale = AR_WIDE_TIMING if "wide_timing" in mods else 1.0
        parts = []
        for window, name, points, weight in AR_TIERS:
            ms = int(round(window * scale * 1000))
            parts.append("SICK ±%d ms" % ms if name == "SICK!" else "%s ±%d" % (name, ms))
        return "   •   ".join(parts)

    AR_FIT_CACHE = {}

    def ar_fit_text(text, width, font=None, size=20, outlines=()):
        """``text`` shortened with an ellipsis until it fits ``width`` pixels, breaking at a word when one is near."""
        key = (text, width, font, size, tuple(outlines))
        if key in AR_FIT_CACHE:
            return AR_FIT_CACHE[key]

        def measure(value):
            return Text(value, font=font or AR_UI_FONT, size=size, outlines=list(outlines), substitute=False).size()[0]

        fitted = text
        if measure(text) > width:
            low, high = 0, len(text)
            while low < high:
                middle = (low + high + 1) // 2
                if measure(text[:middle].rstrip() + "…") <= width:
                    low = middle
                else:
                    high = middle - 1
            cut = text[:low].rstrip()
            space = cut.rfind(" ")
            if space > len(cut) * .6:
                cut = cut[:space]
            # Never leave a bracket or a quotation open in front of the ellipsis.
            if cut.count("(") > cut.count(")"):
                cut = cut[:cut.rfind("(")]
            if cut.count('"') % 2:
                cut = cut[:cut.rfind('"')]
            fitted = (cut.rstrip(" ([{-,:;") or text[:max(1, low)]) + "…"
        if len(AR_FIT_CACHE) > 256:
            AR_FIT_CACHE.clear()
        AR_FIT_CACHE[key] = fitted
        return fitted

    def ar_adjust_setting(name, amount, minimum, maximum):
        value = getattr(persistent, name)
        setattr(persistent, name, round(max(minimum, min(maximum, value + amount)), 3))

    def ar_scroll_factor(chart):
        """How many times AR_SCROLL this chart's notes travel. Tempo scroll ignores the
        speed setting and uses the song's BPM over AR_TEMPO_BPM instead."""
        if persistent.asahina_rhythm_tempo_scroll:
            return chart["bpm"] / AR_TEMPO_BPM
        return max(AR_SPEED_MIN, min(AR_SPEED_MAX, persistent.asahina_rhythm_speed or AR_SPEED_DEFAULT))

    def ar_speed_label(speed):
        """1.0x, 0.95x, 2.5x: two decimals, less a trailing zero."""
        text = "%.2f" % speed
        return (text[:-1] if text.endswith("0") else text) + "x"

    def ar_time_label(seconds):
        seconds = max(0, int(seconds))
        return "%d:%02d" % (seconds // 60, seconds % 60)

    def ar_stop():
        renpy.music.stop(channel=AR_CHANNEL, fadeout=0)
        renpy.music.set_pause(False, channel=AR_CHANNEL)

    def ar_lane_x(side, lane):
        return AR_STRUM_LEFT[side] + AR_LANE * .5 + lane * AR_LANE

    def ar_fade(render, alpha, additive=False):
        """Fade a freshly made Render exactly as Transform(alpha=) does under gl2."""
        over = 0.0 if additive else 1.0
        render.alpha = alpha
        render.over = over
        render.add_shader("renpy.alpha")
        render.add_uniform("u_renpy_alpha", alpha)
        render.add_uniform("u_renpy_over", over)
        return render

    def ar_ease_out(t):
        t = max(0.0, min(1.0, t))
        return 1 - (1 - t) ** 3

    def ar_edge_alpha(adjustment, top, trans, st, at):
        """Fade one end of the song list in proportion to how far it can still
        scroll that way, so the scrim shows a cut row and never a real end.

        A curried Transform function: renpy.curry passes what was bound BEFORE
        the (trans, st, at) the Transform calls it with, so the two settings
        lead. Curry compares equal, so re-executing the screen reuses the
        Transform instead of building a new one every frame."""
        room = adjustment.value if top else max(0.0, adjustment.range - adjustment.value)
        trans.alpha = max(0.0, min(1.0, room / 18.0))
        return 0

    ar_list_edge = renpy.curry(ar_edge_alpha)

    def ar_last_song_index(songs):
        """Where the song cursor starts. Coming back from a run lands on the song
        that was just played, not back at the top of the list."""
        for i, song in enumerate(songs):
            if song["id"] == persistent.asahina_rhythm_last_song:
                return i
        return 0

    def ar_song_adjustment(songs, index):
        """The list's scroll, already placed so the starting song is whole and on
        screen. The range is stated up front, or a first value past 1 is clamped
        away before the viewport has measured anything."""
        count = len(songs)
        view = ar_song_list_height(count)
        limit = max(0, count * AR_SONG_PITCH - AR_SONG_GAP - view)
        return ui.adjustment(range=limit, value=max(0, min(limit, index * AR_SONG_PITCH + AR_SONG_ROW - view)))

    def ar_song_list_height(count):
        """How tall the song list is. Short lists fit exactly; a longer one is cut
        off mid-row on purpose, because a half-drawn row says 'scroll' by itself."""
        if count <= AR_SONG_VIEW:
            return max(AR_SONG_ROW, count * AR_SONG_PITCH - AR_SONG_GAP)
        return AR_SONG_VIEW * AR_SONG_PITCH + AR_SONG_PEEK

    def ar_reveal_song(adjustment, index, count):
        """Scroll the song list so ``index`` is whole and on screen."""
        if adjustment is None or count < 1:
            return
        # The viewport may not have measured this list yet, and a stale range
        # would clamp the jump; song rows are a fixed pitch, so state it.
        view = ar_song_list_height(count)
        limit = max(0, count * AR_SONG_PITCH - AR_SONG_GAP - view)
        if adjustment.range != limit:
            adjustment.range = limit
        top = index * AR_SONG_PITCH
        if top < adjustment.value:
            adjustment.change(max(0, top))
        elif top + AR_SONG_ROW > adjustment.value + view:
            adjustment.change(max(0, min(limit, top + AR_SONG_ROW - view)))

    def ar_step_song(delta, count, adjustment=None):
        """Move the song cursor from its LIVE value; key repeat outruns screen re-execution."""
        screen = renpy.current_screen()
        if screen is None or count < 1:
            return
        chosen = (screen.scope.get("selected", 0) + delta) % count
        screen.scope["selected"] = chosen
        ar_reveal_song(adjustment, chosen, count)
        renpy.restart_interaction()

    def ar_pick_song(index, count, adjustment=None):
        """Choose a song by clicking its row, keeping it whole in the list."""
        screen = renpy.current_screen()
        if screen is None:
            return
        screen.scope["selected"] = index
        ar_reveal_song(adjustment, index, count)
        renpy.restart_interaction()

    def ar_song_stats(chart, duet=False):
        notes = [n for n in chart["notes"] if duet or n["side"] == "player"]
        # Measured tempos carry decimals (114.9925); the chip only needs the feel.
        return (ar_time_label(chart["duration"]), "%g BPM" % round(chart["bpm"], 1),
                "%d NOTES" % len(notes), "%d HOLDS" % sum(1 for n in notes if n["length"] > .075))

    AR_MENU_POSES = {}

    def ar_menu_pose(name, pose, period):
        key = (name, pose, period)
        if key not in AR_MENU_POSES:
            AR_MENU_POSES[key] = ar_frame_menu_pose(name, pose, period)
        return AR_MENU_POSES[key]

    def ar_result_rows(result):
        counts = result["counts"]
        return (("SICK!!", counts["SICK!"], "#ffe066"), ("GOOD", counts["GOOD"], "#8ff0a4"),
                ("OKAY", counts["OKAY"], "#8fc8ff"), ("YUCKY", counts["YUCKY"], "#c7a0ff"),
                ("MISS", result["misses"], "#ff6b8a"))

    def ar_count_up(st, at, value, delay=.35, duration=.9):
        t = max(0.0, min(1.0, (st - delay) / duration))
        shown = int(round(value * (1 - (1 - t) ** 3)))
        return (Text("{:,}".format(shown), font=AR_UI_FONT, size=54, color="#ffffff",
                     outlines=[(3, AR_INK, 0, 2)], substitute=False),
                None if t >= 1 else 1 / 60.0)

    class ARStage(renpy.Displayable):
        # Class defaults, so a stage pickled before these fields existed (a hot
        # reload mid-song) still draws.
        quake_px = (0.0, 0.0)
        tilt_rigs = None

        def __init__(self, chart, practice=False, autoplay=False, start_time=0.0, modifiers=(), wipes=False,
                     quit_cover=True, **kwargs):
            super(ARStage, self).__init__(**kwargs)
            self.game = RhythmSession(chart, practice, autoplay, start_time, modifiers)
            self.chart = self.game.chart
            self.song = ar_resolve_audio(chart)
            self.input_offset = max(-250, min(250, persistent.asahina_rhythm_input_ms or 0)) / 1000.0
            self.visual_offset = max(-250, min(250, persistent.asahina_rhythm_visual_ms or 0)) / 1000.0
            self.speed = ar_scroll_factor(self.chart)
            self.downscroll = bool(persistent.asahina_rhythm_downscroll)
            mods = self.game.modifiers
            self.dizzy = "dizzy" in mods
            self.vanish = "vanish" in mods
            self.keymap = AR_KEYS_DUET if self.game.duet else AR_KEYS_SOLO
            self.tags = ar_mod_names(mods, practice=self.game.practice, autoplay=self.game.autoplay)
            self.title_label = None
            self.beat_len = 60.0 / self.chart["bpm"]
            self.plan = camera_plan(self.chart)
            notes = self.game.notes
            self.first_note = notes[0]["time"] if notes else 0.0
            self.last_note = max([n["time"] + n["length"] for n in notes] or [0.0])
            self.max_tail = max([n["length"] for n in notes] or [0.0])
            self.now = start_time
            self.clock = None
            self.countdown_start = None
            self.countdown_length = 4 * self.beat_len
            self.countdown_remaining = self.countdown_length
            self.countdown_step = 0
            self.started = False
            self.paused = False
            self.pause_wall = 0
            self.resume_until = 0
            self.seek_on_resume = False
            self.result = None
            self.keys = set()
            self.last_wall = None
            self.keyboard_focus = True
            # Per side: (pose, began, duration) in song seconds.
            self.pose = {"opponent": ("idle", -10.0, 0.0), "player": ("idle", -10.0, 0.0)}
            # Per strumline row (0 is Asahina's, 1 the player's) and lane.
            self.confirm = [[-10.0] * 4 for unused in range(2)]
            self.confirm_end = [[-10.0] * 4 for unused in range(2)]
            self.splashes = []
            self.popups = []
            # Gameplay shouts over the HUD: (word, colour, song time).
            self.shouts = []
            self.rule_shout = -10.0
            self.push_time = -10.0
            self.fanfare_span = None
            self.volley_count = 0
            self.rng = ar_random.Random(len(notes) * 7919 + int(start_time * 1000))
            self.score_bump = -10.0
            self.cam = None
            self.cam_time = None
            # Screen pixels the quake is knocking the frame by this frame.
            self.quake_px = (0.0, 0.0)
            self.nudge = [0.0, 0.0]
            self.view = AR_SHOT["center"]
            self.st = self.at = 0
            self.text_cache = {}
            self.images = {}
            self.solids = {}
            self._image("stage", AR_ART + "stage_wide.webp")
            self._image("vignette", AR_UI + "vignette.png")
            self._image("shadow", AR_UI + "shadow.png", zoom=.5)
            # Fixed model parts animate continuously from the existing song clock.
            for name, parts in (("speaker", ("cabinet", "cone", "leds")),
                                ("matsuda", ("body", "ponytail", "earring"))):
                for part in parts:
                    self._image((name, part), AR_ART + "%s/rig/%s.png" % (name, part))
            self.matsuda_gaze = ARMatsudaGaze()
            head = Composite((256, 224), (0, 0), self.matsuda_gaze,
                             (198, 113), self.images[("matsuda", "earring")])
            # Do not set rotate in constructor kwargs: it would reset dynamic
            # rotation during Transform.update_state on every render.
            self.images[("matsuda", "head_rig")] = Transform(head, rotate_pad=True)
            self.images[("matsuda", "tail_rig")] = Transform(
                self.images[("matsuda", "ponytail")], rotate_pad=True)
            for lane in range(4):
                for kind in ("note", "receptor", "press", "confirm"):
                    self._image((kind, lane), AR_UI + "%s_%d.png" % (kind, lane), zoom=.5)
                for kind in ("hold", "hold_end", "hold_end_up"):
                    self._image((kind, lane), AR_UI + "%s_%d.png" % (kind, lane))
                for variant in range(2):
                    self._image(("splash", lane, variant), AR_UI + "splash_%d_%d.png" % (lane, variant), zoom=.5)
            for name in ("asahina", "asahiko"):
                self.images[("singer", name)] = ARSingerFrames(name)
                for state in ("normal", "losing", "winning"):
                    self._image(("icon", name, state), AR_ART + "icons/%s_%s.png" % (name, state))
            # Loads only the effect textures this chart uses.
            self.fx = ARStageFX(self)
            self.tilt_rigs = {}
            if self.game.fights_back:
                self.fx.texture("glow", "pink")
            # The endings and the wipes (asahina_rhythm_finale.rpy). Without
            # `wipes` (the Chart Studio's preview) a result is handed straight back.
            self.finale = None
            self.end_time = None
            self.heads = []
            self.quit_cover = quit_cover
            self.intro_wipe = self.exit_wipe = None
            self.intro_delay = 0.0
            if wipes:
                ARFinale.preload(self)
                self.intro_wipe = ARWipe("uncover", "enter", title=self.chart["title"],
                                         subtitle="   •   ".join(self.tags) or None, hold=AR_WIPE_TITLE_HOLD, block=False)
                self.exit_wipe = ARWipe("cover")
                # The countdown starts once the title card is half cleared.
                self.intro_delay = AR_WIPE_TITLE_HOLD + AR_WIPE_TIME * .5

        # ---- caches and drawing primitives --------------------------------

        def _image(self, key, path, zoom=1.0, **properties):
            if key not in self.images:
                if renpy.loadable(path):
                    child = Image(path)
                    if zoom != 1.0 or properties:
                        child = Transform(child, zoom=zoom, **properties)
                else:
                    # Missing assets surface in project validation. Keep the stage
                    # playable while a developer is replacing art.
                    child = Solid("#302944", xysize=(64, 64))
                self.images[key] = child
            return self.images[key]

        def visit(self):
            return list(self.images.values()) + list(self.solids.values())

        def _text(self, text, size=20, color="#fff6ed", font=None, outlines=((2, "#100b20", 0, 0),)):
            key = (text, size, color, font, outlines)
            if key not in self.text_cache:
                if len(self.text_cache) > 240:
                    self.text_cache.clear()
                self.text_cache[key] = Text(text, font=font or AR_UI_FONT, size=size, color=color,
                                            outlines=list(outlines), substitute=False)
            return self.text_cache[key]

        def _solid(self, color):
            if color not in self.solids:
                self.solids[color] = Solid(color)
            return self.solids[color]

        def _rect(self, target, color, x, y, width, height):
            if width >= .5 and height >= .5:
                target.subpixel_blit(renpy.render(self._solid(color), width, height, self.st, self.at), (x, y))

        def _place(self, target, child, x, y, scale=1.0, alpha=1.0, xanchor=.5, yanchor=.5, sy=None, additive=False):
            """Blit ``child`` with its anchor at (x, y), scaled and faded about that anchor."""
            if alpha <= .003:
                return
            rendered = renpy.render(child, 1280, 720, self.st, self.at)
            width, height = rendered.get_size()
            sx, sy = scale, scale if sy is None else sy
            if sx == 1 and sy == 1 and alpha >= 1 and not additive:
                target.subpixel_blit(rendered, (x - width * xanchor, y - height * yanchor))
                return
            wrap = renpy.Render(width, height)
            if sx != 1 or sy != 1:
                wrap.zoom(sx, sy)
            wrap.blit(rendered, (0, 0))
            if alpha < 1 or additive:
                ar_fade(wrap, min(1.0, alpha), additive)
            target.subpixel_blit(wrap, (x - width * sx * xanchor, y - height * sy * yanchor))

        # ---- clock, pause and judgment (unchanged rules) ---------------------

        def _start_music(self, wall):
            self.countdown_step = 3
            self.started = True
            self.clock = SongClock(wall, self.game.start_time)
            spec = self.song
            if self.game.start_time > 0:
                spec = "<from %.6f>" % self.game.start_time + spec
            renpy.music.play(spec, channel=AR_CHANNEL, loop=False, fadeout=0, synchro_start=False)
            renpy.music.pump()
            # Both singers throw a "hey" on GO; the first sung note overrides it.
            for side in ("opponent", "player"):
                self.pose[side] = ("hey", self.game.start_time, min(.5, self.beat_len * 1.5))

        def set_pause(self, paused=True):
            if self.result or paused == self.paused:
                return
            wall = ar_time.perf_counter()
            if paused:
                self.paused = True
                self.pause_wall = wall
                if self.clock:
                    self.clock.pause(wall)
                renpy.music.set_pause(True, channel=AR_CHANNEL)
                self.keys.clear()
                self.game.clear_keys()
            else:
                self.paused = False
                if self.countdown_start is not None and not self.started:
                    self.countdown_start += wall - self.pause_wall
                # The song remains paused during a one-second ready cue.
                self.resume_until = wall + 1.0
            renpy.restart_interaction()
            renpy.redraw(self, 0)

        def finish(self, outcome):
            if self.result is None:
                self.game.outcome = outcome
                self.result = self.game.snapshot()
                self.end_time = self.now
                ar_stop()
                if self.exit_wipe is not None and (outcome != "quit" or self.quit_cover):
                    self.finale = ARFinale(self, outcome)
                renpy.redraw(self, 0)

        def escape(self):
            """Esc and right-click: pause or resume, or hurry an ending along."""
            if self.finale is not None:
                self.finale.skip()
            elif self.result is None:
                self.set_pause(not self.paused)

        def _trigger_countdown_sfx(self, elapsed):
            while self.countdown_step < 3 and elapsed >= self.beat_len * (self.countdown_step + 1):
                self.countdown_step += 1
                if self.countdown_step == 1:
                    renpy.music.play(AR_COUNTDOWN_READY, channel=AR_COUNTDOWN_READY_CH,
                                     loop=False, fadeout=0, synchro_start=False)
                elif self.countdown_step == 2:
                    renpy.music.play(AR_COUNTDOWN_SET, channel=AR_COUNTDOWN_SET_CH,
                                     loop=False, fadeout=0, synchro_start=False)
                else:
                    renpy.music.play(AR_COUNTDOWN_GO, channel=AR_COUNTDOWN_GO_CH,
                                     loop=False, fadeout=0, synchro_start=False)

        def _step(self):
            # This SDK's Windows monotonic() is GetTickCount64 (15.625 ms).
            # perf_counter() is also monotonic and uses high-resolution QPC.
            wall = ar_time.perf_counter()
            # The engine can consume SDL focus events before CDD dispatch.
            # Observe its keyboard-focus state too, once per focus-loss edge.
            focused = bool(getattr(renpy.game.interface, "keyboard_focused", True))
            lost_focus = self.keyboard_focus and not focused
            self.keyboard_focus = focused
            if lost_focus and not self.paused:
                self.set_pause(True)
            # Window drags can suppress focus events. Stop before processing a
            # long stalled interval, then seek to the last judged time on resume.
            if self.last_wall is not None and wall - self.last_wall > .75 and self.started and not self.paused and not self.resume_until:
                self.set_pause(True)
                self.seek_on_resume = True
            self.last_wall = wall
            if self.result:
                if self.finale is not None:
                    self.finale.step(wall)
                return
            if self.paused:
                return
            if self.resume_until:
                if wall < self.resume_until:
                    return
                self.resume_until = 0
                if self.seek_on_resume:
                    renpy.music.play("<from %.6f>" % max(0, self.now) + self.song,
                        channel=AR_CHANNEL, loop=False, fadeout=0)
                    renpy.music.pump()
                    self.seek_on_resume = False
                else:
                    renpy.music.set_pause(False, channel=AR_CHANNEL)
                if self.clock:
                    self.clock.resume(wall)
                elif self.countdown_start is not None:
                    self.countdown_start += 1.0
            if not self.started:
                if self.countdown_start is None:
                    if self.intro_wipe is not None and self.intro_wipe.elapsed < self.intro_delay:
                        return
                    self.countdown_start = wall
                self.countdown_remaining = self.countdown_length - (wall - self.countdown_start)
                countdown_elapsed = self.countdown_length - self.countdown_remaining
                if self.countdown_remaining <= 0:
                    self._start_music(wall)
                else:
                    self.now = self.game.start_time - self.countdown_remaining
                    self._trigger_countdown_sfx(countdown_elapsed)
                    return
            self.now = self.clock.sample(wall, renpy.music.get_pos(channel=AR_CHANNEL))
            self.game.update(self.now - self.input_offset, opponent_time=self.now)
            self._consume_events()
            if self.game.outcome:
                self.finish(self.game.outcome)

        def _consume_events(self):
            for kind, column, value, t, error in self.game.events:
                if kind == "fanfare":
                    self._fanfare_event(value)
                    continue
                if kind == "rule":
                    # Only practice lives to see this; a real run ends on the spot.
                    if self.now - self.rule_shout > 1.2:
                        self.rule_shout = self.now
                        self._shout(AR_MOD_NAMES.get(value, value.upper()) + " BROKEN", "#ff6b8a")
                    continue
                side = "opponent" if column >= 4 else "player"
                row, lane = (0 if column >= 4 else 1), column % 4
                if kind == "opponent":
                    length = float(value)
                    self._sing("opponent", lane, length)
                    self.confirm[0][lane] = self.now
                    self.confirm_end[0][lane] = self.now + max(.15, length)
                    self._land("opponent", t)
                    if self.game.fights_back:
                        self.push_time = self.now
                elif kind == "hit":
                    self._sing(side, lane, 0.0)
                    # error is the note's own time subtracted from the judged one.
                    self._land("opponent" if column >= 4 else "player", t - error)
                    self.confirm[row][lane] = self.now
                    self.confirm_end[row][lane] = self.now + .15
                    self.score_bump = self.now
                    self._pop_rating(value, error, side)
                    if value == "SICK!":
                        self.splashes.append((row, lane, self.now, self.rng.randrange(2)))
                elif kind in ("miss", "break", "ghost"):
                    self.pose[side] = ("miss", self.now, .36)
                    self._pop_rating("BROKEN" if kind == "break" else "MISS", None, side)
            self.game.events[:] = []
            self.splashes = [s for s in self.splashes[-8:] if self.now - s[2] < .30]

        def _shout(self, word, color):
            self.shouts.append((word, color, self.now))
            del self.shouts[:-3]

        def _fanfare_event(self, value):
            if value == "lost":
                self._shout("FANFARE OUT", "#b9a8d6")
                return
            self._shout("FANFARE!" if value == "relit" else "×3!", AR_GOLD)
            self.fx.flashes.append(self.now)
            del self.fx.flashes[:-6]
            if value == "top":
                self._volley()

        def _volley(self):
            self.volley_count += 1
            self.fx.volleys.append((90000 + 131 * self.volley_count, self.now))
            del self.fx.volleys[:-4]

        def _watch_fanfare(self):
            """Mark each fanfare's start with a shout, a flash and a confetti volley."""
            if "fanfare" not in self.fx.used:
                return
            span = self.fx.fanfare.span_at(self.now)
            if span != self.fanfare_span:
                if span is not None and self.started and self.now - span[0] < .5:
                    self._shout("FANFARE!", AR_GOLD)
                    self.fx.flashes.append(self.now)
                    del self.fx.flashes[:-6]
                    self._volley()
                self.fanfare_span = span

        def _land(self, side, when):
            """Tell the reactive effects a note of ``side`` just landed, and how big its chord is."""
            if self.fx.reactive:
                self.fx.impact(side, when, self.fx.chord_at(side, when))

        def _sing(self, side, lane, length):
            # FNF holds a sing pose about a beat past the note, longer through a sustain.
            self.pose[side] = (AR_POSES[lane], self.now, max(self.beat_len * .9, length + self.beat_len * .35))

        def _pop_rating(self, label, error, side="player"):
            # FNF's ratings live in the world: they spawn where the screen's
            # centre-right is right now, then get left behind as the camera moves.
            # A duet's ratings for Asahina's lanes spawn centre-left instead.
            cx, cy, z = self.view
            x, y = cx + (60 if side == "player" else -190) / z, cy - 42 / z
            rng = self.rng
            word, color = AR_RATING[label]
            fall = dict(vx=-rng.uniform(0, 14), vy=-rng.uniform(150, 185), g=560.0, born=self.now,
                        hold=max(.32, self.beat_len))
            self.popups.append(dict(fall, x=x, y=y, disp=self._text(word, 62 if len(word) < 8 else 44, color,
                                    AR_FONT, ((8, AR_INK, 0, 4), (4, "#ffffff", 0, 0)))))
            if error is not None:
                ms = int(round(error * 1000))
                tint = "#ffffff" if abs(ms) < 12 else ("#ffb38a" if ms > 0 else "#9fd0ff")
                self.popups = [pop for pop in self.popups if pop.get("kind") != "ms"]
                self.popups.append(dict(fall, x=x, y=y + 50, kind="ms",
                                        disp=self._text("%+d ms" % ms if ms else "0 ms", 18, tint, AR_UI_FONT,
                                                        ((3, AR_INK, 0, 1),))))
                combo = self.game.combo
                if combo >= 10:
                    # Only the newest count stays up: at this chart's density two or
                    # three older counts were still falling and read as one garbled number.
                    self.popups = [pop for pop in self.popups if pop.get("kind") != "combo"]
                    digits = "%03d" % combo if combo < 1000 else str(combo)
                    for i, digit in enumerate(digits):
                        self.popups.append(dict(x=x - 40 + i * 40, y=y + 96, vx=rng.uniform(-6, 6),
                                                vy=-rng.uniform(130, 160), g=rng.uniform(220, 300),
                                                born=self.now, hold=self.beat_len * 2, kind="combo",
                                                disp=self._text(digit, 46, "#ffffff", AR_UI_FONT, ((6, AR_INK, 0, 3),))))
            del self.popups[:-28]

        # ---- camera ---------------------------------------------------------

        def _bump(self):
            """Closed-form downbeat punch: 1 on each measure's first beat, then falls away."""
            if not self.started or not self.game.notes:
                return 0.0
            if not self.first_note - 4 * self.beat_len <= self.now <= self.last_note + 4 * self.beat_len:
                return 0.0
            beat = (self.now - self.chart["offset"]) / self.beat_len
            return ar_math.exp(-((beat % 4.0) * self.beat_len) / AR_BUMP_FALL)

        def _update_camera(self):
            """Ease the camera toward its framing; returns (downbeat bump, effect punch)."""
            if self.finale is not None:
                view = self.finale.camera()
                if view is not None:
                    self.view = view
                    return 0.0, 0.0
            now = self.now
            # Look half a beat ahead so the move starts before the phrase does.
            focus = camera_focus(self.plan, self.chart, now + self.beat_len * .5)
            tx, ty, tz = AR_SHOT[focus]
            nx = ny = 0.0
            if focus != "center":
                pose, began, duration = self.pose[focus]
                if pose in AR_POSES and began <= now <= began + duration:
                    nx, ny = AR_DIRS[AR_POSES.index(pose)]
            if self.cam is None:
                self.cam = [tx, ty, tz]
                dt = 0.0
            else:
                dt = max(0.0, min(.1, now - self.cam_time))
            self.cam_time = now
            if dt:
                # Exponential easing on song time: frame-rate independent, and it
                # freezes with the song during pauses and the resume cue.
                k = 1 - ar_math.exp(-dt / AR_CAM_EASE)
                kz = 1 - ar_math.exp(-dt / AR_ZOOM_EASE)
                kn = 1 - ar_math.exp(-dt / .14)
                self.cam[0] += (tx - self.cam[0]) * k
                self.cam[1] += (ty - self.cam[1]) * k
                self.cam[2] += (tz - self.cam[2]) * kz
                self.nudge[0] += (nx * AR_NUDGE - self.nudge[0]) * kn
                self.nudge[1] += (ny * AR_NUDGE * .6 - self.nudge[1]) * kn
            bump = self._bump()
            punch = self.fx.punch()
            qx, qy, quake = self.fx.quake()
            lx, lunge = self.fx.lunge()
            self.quake_px = (qx, qy)
            z = self.cam[2] + AR_BUMP_WORLD * bump + .012 * punch + .034 * quake + .026 * lunge
            half_w, half_h = 640.0 / z, 360.0 / z
            # The knock is in screen pixels; the camera lives in world ones.
            x = min(max(self.cam[0] + self.nudge[0] + lx + qx / z, half_w), AR_WORLD[0] - half_w)
            y = min(max(self.cam[1] + self.nudge[1] + qy / z, half_h), AR_WORLD[1] - half_h)
            self.view = (x, y, z)
            return bump, punch

        # ---- world ----------------------------------------------------------

        def _draw_world(self, r, bump):
            x, y, z = self.view
            fx = self.fx
            layer = renpy.Render(*AR_WORLD)
            # Bitcrush resamples the stage's CHILDREN one at a time, here and in
            # _draw_backstage and _draw_character, rather than the finished
            # world layer: by then the world is a Render, and a Render cannot be
            # resampled. When the effect is idle fx.crush hands each child
            # straight back, so this costs one call and nothing else.
            layer.blit(renpy.render(fx.crush(self.images["stage"], AR_WORLD, "stage"),
                                    AR_WORLD[0], AR_WORLD[1], self.st, self.at), (0, 0))
            fx.draw_world_back(layer)
            self._draw_backstage(layer)
            fx.draw_world_mid(layer)
            for side in ("opponent", "player"):
                if side == "player" and self.finale is not None:
                    self.finale.draw_world_veil(layer)
                self._draw_character(layer, side)
            fx.draw_world_front(layer)
            self._draw_popups(layer)
            if self.finale is not None:
                self.finale.draw_world_burst(layer)
            # Render.zoom scales children about the origin but not blit offsets,
            # so the whole world goes in as one layer at (0, 0).
            wrap = renpy.Render(*AR_WORLD)
            wrap.zoom(z, z)
            wrap.blit(layer, (0, 0))
            # Normally one blit. A Tear breaks it into bands that slip against
            # each other, which is the one effect that has to happen at the
            # seam between the world and the frame rather than inside either.
            fx.blit_world(r, wrap, 640 - x * z, 360 - y * z)
            if bump > .02 and not fx.safe:
                # The downbeat lifts the whole frame a touch: additive and
                # whole-frame, so it follows any stage art, not one painted lamp.
                # A burning fanfare turns it gold and harder. Skipped outright
                # under Photosensitive Mode -- a full-frame brightness step
                # once a measure is small, but it is the metronome the rest of
                # the switch's work would be fighting.
                fan = fx.fanfare_glow()
                flash = renpy.Render(1280, 720)
                flash.blit(renpy.render(self._solid("#ffcf5a" if fan > .5 else "#ff8fc8"), 1280, 720, self.st, self.at), (0, 0))
                r.blit(ar_fade(flash, (.045 + .05 * fan) * bump, additive=True), (0, 0))
            fx.draw_crowd(r)
            r.blit(renpy.render(self.images["vignette"], 1280, 720, self.st, self.at), (0, 0))
            fx.draw_screen(r)

        def _draw_backstage(self, layer):
            # Separate cabinet/cones and body/head/tail retain the same geometry
            # and one earring throughout the dance. All curves are periodic, so
            # beat boundaries have no image-swap or sawtooth discontinuity.
            self.matsuda_gaze.now = self.now
            beat = (self.now - self.chart["offset"]) / self.beat_len
            angle = ar_math.pi * beat
            pulse = (.5 + .5 * ar_math.cos(2 * angle)) ** 4
            crush = self.fx.crush
            self._place(layer, self.images["shadow"], 836, 814, scale=1.0, alpha=.72)
            self._place(layer, crush(self.images[("speaker", "cabinet")], (512, 256), "cabinet"),
                        836, 812, yanchor=238 / 256.0)
            for x in (749, 923):
                self._place(layer, crush(self.images[("speaker", "cone")], (128, 128), "cone"), x, 715,
                            scale=.96 + .08 * pulse)
            self._place(layer, self.images[("speaker", "leds")], 836, 636,
                        alpha=.25 + .75 * pulse)

            squash = .5 + .5 * ar_math.cos(2 * angle)
            sy = 1 - .045 * squash
            neck = (834, 608 - 96 * sy)
            head_angle = 5.0 * ar_math.sin(angle)
            theta = ar_math.radians(head_angle)
            c, s = ar_math.cos(theta), ar_math.sin(theta)
            # Tail attachment is expressed in head coordinates, not screen
            # coordinates; it follows the head even while its own swing lags.
            tail_origin = (neck[0] + c * 29 + s * 107,
                           neck[1] + s * 29 - c * 107)
            self._place_rig(layer, self.images[("matsuda", "tail_rig")],
                            (256, 320), (55, 68), tail_origin,
                            head_angle + 7 * ar_math.sin(angle - .65))
            self._place(layer, self.images[("matsuda", "body")], 836, 608,
                        sy=sy, yanchor=272 / 448.0)
            self._place_rig(layer, self.images[("matsuda", "head_rig")],
                            (256, 224), (141, 147), neck, head_angle)

        def _place_rig(self, target, part, size, pivot, point, degrees):
            """Rotate a cached cutout about its authored attachment point."""
            part.rotate = degrees
            part.update()
            rendered = renpy.render(part, 1280, 720, self.st, self.at)
            width, height = rendered.get_size()
            theta = ar_math.radians(degrees)
            c, s = ar_math.cos(theta), ar_math.sin(theta)
            dx, dy = pivot[0] - size[0] * .5, pivot[1] - size[1] * .5
            mapped_x = width * .5 + c * dx - s * dy
            mapped_y = height * .5 + s * dx + c * dy
            target.subpixel_blit(rendered, (point[0] - mapped_x, point[1] - mapped_y))

        def _draw_character(self, layer, side):
            name = AR_CAST[side]
            now = self.now
            beat = (now - self.chart["offset"]) / self.beat_len
            pose, began, duration = self.pose[side]
            age = now - began
            active = pose != "idle" and 0 <= age <= duration
            held = None
            base = 0 if side == "player" else 4
            if side == "player" or self.game.duet:
                for column in self.game.holds:
                    if base <= column < base + 4 and self.game.held[column]:
                        held = column - base
                        break
            forced = self.finale.pose(side) if self.finale is not None else None
            if forced is not None:
                pose = forced
            elif held is not None and not (active and pose == "miss"):
                pose = AR_POSES[held]
            elif not active:
                pose = "idle"
            # Complete authored drawings keep their existing acting. Each note
            # plays one ordered gesture; holds never alternate at step speed.
            presentation = now
            if self.finale is not None and self.finale.kind == "failed":
                # Failed songs freeze now; clears already advance now inside
                # ARFinale.step. Respect the hit stop without doubling clear time.
                presentation += max(0.0, self.finale.age - AR_FAIL_FREEZE)
            singer = self.images[("singer", name)]
            token = (pose, "finale") if forced is not None else began
            gesture_duration = duration if active and forced is None and held is None else None
            if forced == "miss":
                gesture_duration = .30
            singer.set_pose(pose, presentation, event=token, held=held is not None, duration=gesture_duration)
            singer.set_clock(presentation, beat, self.beat_len)
            spot = AR_SPOT_X[side]
            # Convulse shakes the singer where she stands. It moves the SHADOW
            # with her sideways but not vertically: a shadow that leaves the
            # floor reads as a sprite sliding around, not as a body shaking.
            tx, ty, tilt = self.fx.tremor(side)
            spot += tx
            self._place(layer, self.images["shadow"], spot, AR_FEET_Y + 4, scale=.78, alpha=.9)
            # Doubles: copies of this singer standing behind her. They go in
            # HERE rather than in the FX layer's own passes because this is the
            # only point in the frame where her pose clock is already set for
            # this frame -- drawn from draw_world_mid they would be a frame
            # stale, and drawn from draw_world_front they would be in front of
            # her, which is a different and much worse effect.
            drawn = self.fx.crush(singer, (384, 448), ("singer", name))
            for dx, dy, alpha in self.fx.doubles(side):
                self._place(layer, drawn, spot + dx, AR_FEET_Y + dy + ty, alpha=alpha, yanchor=430 / 448.0)
            if tilt:
                # The lean needs a rotate, so it takes the cached rig path
                # rather than _place. Pivot at the feet: a body shaking pivots
                # on the floor, and rotating about the sprite's centre would
                # swing her shoes out from under her.
                self._place_tilted(layer, drawn, (name, self.fx.crush_factor()),
                                   spot, AR_FEET_Y + ty, tilt)
            else:
                self._place(layer, drawn, spot, AR_FEET_Y + ty, yanchor=430 / 448.0)

        def _place_tilted(self, layer, child, key, x, y, degrees):
            """``child``, leaning ``degrees`` about the singer's own feet. Convulse only.

            Keyed by (who, at what crush) rather than by id(): this stage is
            pickled on a hot reload, and a recycled id would hand one singer
            another's rig. See the transform-identity note in the memory.
            """
            if self.tilt_rigs is None:
                self.tilt_rigs = {}
            rig = self.tilt_rigs.get(key)
            if rig is None:
                rig = self.tilt_rigs[key] = Transform(child, rotate_pad=True)
            ar_blit_turned(layer, rig, (384, 448), (192, 430), (x, y), degrees, self.st, self.at,
                           alpha=1.0, additive=False)

        def _draw_popups(self, layer):
            now = self.now
            alive = []
            for pop in self.popups:
                age = max(0.0, now - pop["born"])
                if age > pop["hold"] + .22:
                    continue
                alive.append(pop)
                alpha = 1.0 if age < pop["hold"] else 1 - (age - pop["hold"]) / .22
                scale = 1 + .14 * ar_math.exp(-age / .05)
                self._place(layer, pop["disp"], pop["x"] + pop["vx"] * age,
                            pop["y"] + pop["vy"] * age + .5 * pop["g"] * age * age, scale, alpha)
            self.popups = alive

        # ---- HUD ------------------------------------------------------------

        def _draw_hud(self, r, bump, punch):
            hud = renpy.Render(1280, 720)
            ry = AR_STRUM_Y[1 if self.downscroll else 0]
            fin = self.finale
            collapsing = fin is not None and fin.collapsing()
            if collapsing:
                # The tails fade while the finale drops the outlines and spills the heads.
                fade = 1 - (fin.age - AR_FAIL_FREEZE) / .2
                if fade > .003:
                    tails = renpy.Render(1280, 720)
                    self._draw_notes(tails, ry, draw_heads=False)
                    hud.blit(ar_fade(tails, fade), (0, 0))
            else:
                fade = fin.lanes_alpha() if fin is not None else 1.0
                lanes = hud if fade >= 1 else renpy.Render(1280, 720)
                if fade > .003:
                    self.fx.draw_strum_glow(lanes, ry)
                    self._draw_strums(lanes, ry)
                    self._draw_notes(lanes, ry)
                    for row, lane, began, variant in self.splashes:
                        t = (self.now - began) / .30
                        if 0 <= t < 1:
                            self._place(lanes, self.images[("splash", lane, variant)], ar_lane_x(row, lane), ry,
                                        .70 + .50 * ar_ease_out(t), 1 - t * t)
                    if lanes is not hud:
                        hud.blit(ar_fade(lanes, fade), (0, 0))
            fade = fin.chrome_alpha() if fin is not None else 1.0
            chrome = hud if fade >= 1 else renpy.Render(1280, 720)
            if fade > .003:
                self._draw_bar(chrome, player_icon=not collapsing)
                self._draw_timebar(chrome)
                self.fx.draw_banner(chrome)
                self._draw_callouts(chrome)
                if chrome is not hud:
                    hud.blit(ar_fade(chrome, fade), (0, 0))
            if fin is not None:
                fin.draw_hud(hud, ry)
            ox, oy = fin.shake() if fin is not None else (0.0, 0.0)
            qx, qy = self.quake_px
            ox, oy = ox + qx, oy + qy
            zoom = 1 + AR_BUMP_HUD * bump + .016 * punch
            if zoom > 1.0005:
                wrap = renpy.Render(1280, 720)
                wrap.zoom(zoom, zoom)
                wrap.blit(hud, (0, 0))
                r.subpixel_blit(wrap, (640 - 640 * zoom + ox, 360 - 360 * zoom + oy))
            elif ox or oy:
                r.subpixel_blit(hud, (ox, oy))
            else:
                r.blit(hud, (0, 0))

        def _intro_seconds(self):
            """Seconds since the countdown began, continuing through the song."""
            if self.started:
                return self.countdown_length + (self.now - self.game.start_time)
            return max(0.0, self.countdown_length - self.countdown_remaining)

        def _draw_strums(self, hud, ry):
            now = self.now
            game = self.game
            intro = self._intro_seconds()
            lift = 18 if self.downscroll else -18
            for side in (0, 1):
                # Asahina's strumline is the player's too in a duet.
                playable = side == 1 or game.duet
                for lane in range(4):
                    # Strums drop in one at a time during the countdown, as in FNF.
                    appear = ar_ease_out((intro - .05 - .07 * (side * 4 + lane)) / .32)
                    if appear <= 0:
                        continue
                    column = lane if side == 1 else lane + 4
                    x, y = ar_lane_x(side, lane), ry + lift * (1 - appear)
                    held = playable and game.held[column]
                    sustaining = held and column in game.holds
                    if now < self.confirm_end[side][lane] or sustaining:
                        pop = 1 + .10 * ar_math.exp(-max(0.0, now - self.confirm[side][lane]) / .07)
                        self._place(hud, self.images[("confirm", lane)], x, y, pop, appear)
                    elif held and not game.autoplay:
                        self._place(hud, self.images[("press", lane)], x, y, .92, appear)
                    else:
                        self._place(hud, self.images[("receptor", lane)], x, y, 1.0, appear * (1.0 if playable else .85))
            if not game.autoplay:
                # Key letters under each playable strumline until the song is under way.
                fade = min(1.0, max(0.0, self.countdown_length + 1.6 - intro))
                rows = ((0, "ASDF"), (1, "JKL;")) if game.duet else ((1, "DFJK"),)
                for side, letters in rows:
                    for lane, letter in enumerate(letters):
                        self._place(hud, self._text(letter, 22, "#ffffff", AR_UI_FONT, ((4, AR_INK, 0, 1),)),
                                    ar_lane_x(side, lane), ry - lift * 3.7, 1.0, fade * ar_ease_out((intro - .4) / .4))

        def _note_shift(self, y, ry, lane):
            """Dizzy: how far a note ``y`` px down its lane swings sideways. It settles onto its outline."""
            if not self.dizzy:
                return 0.0
            distance = abs(y - ry)
            return AR_DIZZY_SWING * min(1.0, distance / 260.0) * ar_math.sin(distance / 88.0 + self.now * 2.6 + lane * .9)

        def _note_alpha(self, y, ry):
            """Vanish: a note fades out over the last stretch before its outline and stays gone past it."""
            if not self.vanish:
                return 1.0
            ahead = (y - ry) * (-1 if self.downscroll else 1)
            return max(0.0, min(1.0, (ahead - 150.0) / 110.0))

        def _draw_notes(self, hud, ry, draw_heads=True):
            game = self.game
            velocity = AR_SCROLL * self.speed
            direction = -1 if self.downscroll else 1
            shown = self.now - self.visual_offset
            lo = ar_bisect.bisect_left(game.times, shown - max(240.0 / velocity, self.max_tail + .05))
            hi = ar_bisect.bisect_right(game.times, shown + 820.0 / velocity)
            heads = []
            for index in range(lo, hi):
                state = game.states[index]
                if state == 3:
                    continue
                note = game.notes[index]
                side = 1 if note["side"] == "player" else 0
                lane = note["lane"]
                column = lane if side == 1 else lane + 4
                x = ar_lane_x(side, lane)
                y = ry + (note["time"] - shown) * velocity * direction
                end = note["time"] + note["length"]
                if note["length"] > .075 and not (state == 1 and end < shown):
                    dim = state == 2
                    hold = game.holds.get(column) if (side == 1 or game.duet) else None
                    if hold is not None and hold["index"] == index and hold["broken"] and not game.held[column]:
                        dim = True
                    # A sustain being sung is clipped at the strum, like FNF's clipRect.
                    head = ry if state == 1 else y
                    self._draw_hold(hud, lane, x, head, ry + (end - shown) * velocity * direction, .38 if dim else 1.0, ry)
                if state == 0:
                    heads.append((x, y, lane, 1.0))
                elif state == 2:
                    # A missed note keeps scrolling past the strum, greyed out.
                    heads.append((x, y, lane, .35))
            if not draw_heads:
                return
            # What was drawn is kept: a failed song spills these heads off the highway.
            drawn = []
            for x, y, lane, alpha in heads:
                if -70 < y < 790:
                    x, alpha = x + self._note_shift(y, ry, lane), alpha * self._note_alpha(y, ry)
                    self._place(hud, self.images[("note", lane)], x, y, 1.0, alpha)
                    if alpha > .003:
                        drawn.append((x, y, lane, alpha))
            self.heads = drawn

        def _draw_hold(self, hud, lane, x, head, tail, alpha, ry):
            length = abs(tail - head)
            if length < 1:
                return
            cap = min(48.0, length)
            if self.downscroll:
                body_top, body_bottom, cap_top, cap_key = tail + cap - 1, head, tail, "hold_end_up"
            else:
                body_top, body_bottom, cap_top, cap_key = head, tail - cap + 1, tail - cap, "hold_end"
            top, bottom = max(-20.0, body_top), min(740.0, body_bottom)
            warped = self.dizzy or self.vanish
            if bottom - top >= .5:
                # The body sprite is identical in every row, so stretching it is lossless.
                body = renpy.render(self.images[("hold", lane)], 88, 8, self.st, self.at)
                # Dizzy and vanish change along a tail, so it is drawn in short slices.
                step = 10.0 if warped else bottom - top
                y0 = top
                while y0 < bottom - .25:
                    y1 = min(bottom, y0 + step)
                    middle = (y0 + y1) * .5
                    shade = alpha * self._note_alpha(middle, ry)
                    if shade > .003:
                        wrap = renpy.Render(88, 8)
                        wrap.zoom(.5, (y1 - y0) / 8.0)
                        wrap.blit(body, (0, 0))
                        if shade < 1:
                            ar_fade(wrap, shade)
                        hud.subpixel_blit(wrap, (x - 22 + self._note_shift(middle, ry, lane), y0))
                    y0 = y1
            if -60 < cap_top < 780:
                middle = cap_top + cap * .5
                shade = alpha * self._note_alpha(middle, ry)
                if shade > .003:
                    end = renpy.render(self.images[(cap_key, lane)], 88, 96, self.st, self.at)
                    wrap = renpy.Render(88, 96)
                    wrap.zoom(.5, cap / 96.0)
                    wrap.blit(end, (0, 0))
                    if shade < 1:
                        ar_fade(wrap, shade)
                    hud.subpixel_blit(wrap, (x - 22 + self._note_shift(middle, ry, lane), cap_top))

        def _draw_bar(self, hud, player_icon=True):
            cy = 72 if self.downscroll else 650
            width, height = 600.0, 16.0
            left, top = 640 - width / 2, cy - height / 2
            health = max(0.0, min(1.0, self.game.health))
            split = left + width * (1 - health)
            self._rect(hud, AR_INK, left - 5, top - 5, width + 10, height + 10)
            self._rect(hud, AR_PINK, left, top, split - left, height)
            self._rect(hud, AR_CYAN, split, top, left + width - split, height)
            self._rect(hud, "#ffffff3a", left, top, width, 4)
            push = 0.0
            if self.game.fights_back:
                # The line Asahina can't push past; only the player's misses move the bar beyond it.
                self._rect(hud, "#ffffffb0", left + width * (1 - AR_FIGHT_FLOOR) - 1, top - 3, 2, height + 6)
                push = ar_math.exp(-max(0.0, self.now - self.push_time) / .18)
                if push > .02:
                    self._place(hud, self.images[("fx", "glow", "pink")], split, cy, .32, .9 * push, additive=True)
            beat = (self.now - self.chart["offset"]) / self.beat_len
            thump = ar_math.exp(-((beat % 1.0) * self.beat_len) / .10) if self.started else 0.0
            size = .72 + .14 * thump
            rival = "losing" if health > .8 else ("winning" if health < .2 else "normal")
            mine = "winning" if health > .8 else ("losing" if health < .2 else "normal")
            self._place(hud, self.images[("icon", "asahina", rival)], split + 8 + 6 * push, cy - 8, size, xanchor=1.0)
            if player_icon:
                self._place(hud, self.images[("icon", "asahiko", mine)], split - 8, cy - 8, size, xanchor=0.0)
            game = self.game
            accuracy = ("%.2f%%" % game.accuracy) if game.judged else "--"
            line = "SCORE {:,}   •   MISSES {}   •   ACCURACY {}".format(game.score, game.misses, accuracy)
            pop = 1 + .06 * ar_math.exp(-max(0.0, self.now - self.score_bump) / .10)
            color = AR_GOLD if self.fx.fanfare_glow() > .5 else "#ffffff"
            self._place(hud, self._text(line, 19, color, AR_UI_FONT, ((3, AR_INK, 0, 1),)), 640, cy + 44, pop)

        def _draw_timebar(self, hud):
            cy = 700 if self.downscroll else 22
            width, height = 360.0, 20.0
            left, top = 640 - width / 2, cy - height / 2
            duration = self.chart["duration"]
            progress = max(0.0, min(1.0, self.now / duration))
            self._rect(hud, AR_INK, left - 4, top - 4, width + 8, height + 8)
            self._rect(hud, "#2a2140", left, top, width, height)
            self._rect(hud, "#f39cc9", left, top, width * progress, height)
            outline = ((3, AR_INK, 0, 0),)
            # A long title ends in an ellipsis before it can reach the clock.
            if self.title_label is None:
                self.title_label = ar_fit_text(self.chart["title"].upper(), width - 84, AR_UI_FONT, 15, outline)
            self._place(hud, self._text(self.title_label, 15, "#ffffff", AR_UI_FONT, outline), left + 10, cy, xanchor=0.0)
            self._place(hud, self._text(ar_time_label(duration - max(0.0, self.now)), 15, "#ffffff", AR_UI_FONT, outline),
                        left + width - 10, cy, xanchor=1.0)

        def _word(self, hud, word, beats, color):
            beats = max(0.0, beats)
            scale = 1 + .16 * ar_math.exp(-beats / .10)
            alpha = 1.0 if beats < .5 else max(0.0, 1 - (beats - .5) / .5)
            disp = self._text(word, 96, color, AR_FONT, ((12, AR_INK, 0, 6), (6, "#ffffff", 0, 0)))
            self._place(hud, disp, 640, 300 - 14 * beats, scale, alpha)

        def _draw_callouts(self, hud):
            intro = self._intro_seconds() / self.beat_len
            for index, word, color in ((1, "READY?", "#ffe066"), (2, "SET", "#8fc8ff"), (3, "GO!", "#87e766")):
                span = 1.5 if index == 3 else 1.0
                if index <= intro < index + span:
                    self._word(hud, word, (intro - index) / span, color)
            if self.resume_until:
                remaining = max(0.0, self.resume_until - ar_time.perf_counter())
                pulse = .5 + .5 * ar_math.cos(remaining * ar_math.pi * 4)
                self._place(hud, self._text("READY?", 72, "#ffe066", AR_FONT, ((10, AR_INK, 0, 5), (5, "#ffffff", 0, 0))),
                            640, 300, 1 + .04 * pulse)
            # Shouts: a fanfare lit or put out, or a rule broken in practice.
            shout_y = 204 if self.downscroll else 546
            for word, color, born in self.shouts:
                age = self.now - born
                if 0 <= age < .9:
                    alpha = 1.0 if age < .6 else max(0.0, 1 - (age - .6) / .3)
                    disp = self._text(word, 34, color, AR_FONT, ((6, AR_INK, 0, 3), (3, "#ffffff", 0, 0)))
                    self._place(hud, disp, 640, shout_y - 16 * ar_ease_out(age / .9), 1 + .22 * ar_math.exp(-age / .08), alpha)
            # The run's switches, stacked in the gap between the two strumlines.
            for i, tag in enumerate(self.tags):
                y = (674 - 17 * i) if self.downscroll else (48 + 17 * i)
                self._place(hud, self._text(tag, 13, AR_GOLD, AR_UI_FONT, ((3, AR_INK, 0, 1),)), 640, y)

        def render(self, width, height, st, at):
            self.st, self.at = st, at
            # Read once a frame, not once per effect: the switch is reachable
            # from the pause menu mid-song, and the FX layer asks about it in a
            # dozen places inside one frame. See accessibility.rpy.
            self.fx.safe = enter_m_photosensitive()
            self._step()
            self._watch_fanfare()
            bump, punch = self._update_camera()
            r = renpy.Render(1280, 720)
            self._draw_world(r, bump)
            self._draw_hud(r, bump, punch)
            if self.finale is not None:
                self.finale.draw_screen(r)
            # The engine's frame limiter/vsync owns presentation cadence.
            # Scheduling exactly 1/60 can miss the next vblank and halve FPS.
            renpy.redraw(self, 0 if (not self.paused or self.finale is not None) else .1)
            renpy.timeout(.02)
            return r

        def event(self, ev, x, y, st):
            if self.result is not None:
                if self.finale is None:
                    return self.result
                # The exit wipe hands the result back once it has closed.
                if ev.type in (ar_pg.KEYDOWN, ar_pg.MOUSEBUTTONDOWN):
                    self.finale.skip()
                    raise renpy.IgnoreEvent()
                return None
            if ev.type == getattr(ar_pg, "WINDOWFOCUSLOST", -123) or (ev.type == ar_pg.ACTIVEEVENT and not ev.gain and ev.state & 2):
                self.set_pause(True)
                return None
            if self.paused:
                return None
            keys = self.keymap
            if ev.type in (ar_pg.KEYDOWN, ar_pg.KEYUP) and ev.key in keys:
                column = keys[ev.key]
                if ev.type == ar_pg.KEYDOWN:
                    if ev.key in self.keys:
                        raise renpy.IgnoreEvent()
                    self.keys.add(ev.key)
                    if self.started and not self.resume_until and not self.game.autoplay:
                        self._step()
                        self.game.press(column, self.now - self.input_offset)
                    else:
                        self.game.held[column] = True
                else:
                    self.keys.discard(ev.key)
                    if not any(keys[key] == column for key in self.keys):
                        if self.started and not self.resume_until:
                            self._step()
                            self.game.release(column, self.now - self.input_offset)
                        else:
                            self.game.held[column] = False
                self._consume_events()
                renpy.redraw(self, 0)
                raise renpy.IgnoreEvent()
            return None


transform ar_bop(period=.8):
    # Squat into the floor on the beat and rise back; never hop off it.
    yzoom 1.0 xzoom 1.0
    block:
        linear (period * .16) yzoom .965 xzoom 1.02
        ease (period * .84) yzoom 1.0 xzoom 1.0
        repeat

transform ar_drift:
    # stripes.png repeats every 48px along the diagonal, so this loops seamlessly.
    xoffset 0 yoffset 0
    linear 3.2 xoffset -48 yoffset -48
    repeat

transform ar_rise(delay=0.0):
    alpha 0.0 yoffset 18
    pause delay
    ease .38 alpha 1.0 yoffset 0

transform ar_slide(delay=0.0, distance=40):
    alpha 0.0 xoffset distance
    pause delay
    ease .40 alpha 1.0 xoffset 0

transform ar_stamp(delay=0.0):
    # The rank lands like a rubber stamp.
    alpha 0.0 zoom 2.2 rotate -14
    pause delay
    easeout .22 alpha 1.0 zoom .92 rotate 4
    ease .16 zoom 1.0 rotate 0

transform ar_spin(period=18.0):
    rotate 0
    linear period rotate 360
    repeat

transform ar_grow(delay=0.0):
    xzoom 0.0
    pause delay
    easein .5 xzoom 1.0

# chart: the song selected in song select, so tempo scroll can say what it does to it.
screen asahina_rhythm_settings(chart=None):
    $ tempo = bool(persistent.asahina_rhythm_tempo_scroll)
    # Tempo scroll overrides the speed setting, so its row shows the result and hides the steppers.
    if not tempo:
        $ speed = (ar_speed_label(persistent.asahina_rhythm_speed), "Note travel only; the song is unchanged.", True)
    elif chart:
        $ speed = (ar_speed_label(ar_scroll_factor(chart)), "Set by tempo scroll: this song is %g BPM." % round(chart["bpm"], 1), False)
    else:
        $ speed = ("AUTO", "Set by tempo scroll: 1.0x at %g BPM." % AR_TEMPO_BPM, False)
    $ rows = (("INPUT OFFSET", "%+d ms" % persistent.asahina_rhythm_input_ms, "asahina_rhythm_input_ms", 5, -250, 250, "Positive accepts later presses.", True),
              ("VISUAL OFFSET", "%+d ms" % persistent.asahina_rhythm_visual_ms, "asahina_rhythm_visual_ms", 5, -250, 250, "Positive makes notes arrive later.", True),
              ("SCROLL SPEED", speed[0], "asahina_rhythm_speed", AR_SPEED_STEP, AR_SPEED_MIN, AR_SPEED_MAX, speed[1], speed[2]))
    vbox:
        spacing 6
        for label, value, field, step, low, high, hint, adjustable in rows:
            fixed:
                xysize (516, 46)
                add Solid("#ffffff0d")
                text label style "ar_opt_label" xpos 14 ypos 5
                text hint style "ar_opt_hint" xpos 14 ypos 27
                if adjustable:
                    textbutton "-" style "ar_step" xpos 352 yalign .5 action Function(ar_adjust_setting, field, -step, low, high)
                    textbutton "+" style "ar_step" xpos 474 yalign .5 action Function(ar_adjust_setting, field, step, low, high)
                text value style "ar_opt_value" xanchor .5 xpos 429 yalign .5
        null height 2
        hbox:
            spacing 8
            textbutton ("DOWNSCROLL  ON" if persistent.asahina_rhythm_downscroll else "DOWNSCROLL  OFF"):
                style "ar_toggle"
                action ToggleField(persistent, "asahina_rhythm_downscroll")
            textbutton ("TEMPO SCROLL  ON" if tempo else "TEMPO SCROLL  OFF"):
                id "ar_setup_tempo_scroll"
                style "ar_toggle"
                tooltip ("Faster songs scroll faster, in place of the speed setting: 1.0x at %g BPM." % AR_TEMPO_BPM)
                action ToggleField(persistent, "asahina_rhythm_tempo_scroll")
        null height 2
        # Photosensitive Mode lives HERE, not in the game's Settings, because
        # this mode is the only thing it changes. A switch sitting in general
        # settings is read as covering the general game, and this one does not.
        # The flag itself is global (persistent.enter_m_photosensitive, see
        # accessibility.rpy) so the day a second mode honours it, the control
        # moves up to Settings and nothing else has to change.
        #
        # It gets its own row rather than a third chip beside Downscroll and
        # Tempo Scroll: it is the one setting in here somebody might be reaching
        # for because of their health, and it should not be two small words on a
        # button you have to already know about to find.
        fixed:
            xysize (516, 46)
            add Solid("#ffffff0d")
            text "PHOTOSENSITIVE" style "ar_opt_label" xpos 14 ypos 5
            text "Removes strobes, flashes and hard glitches. The slow effects stay." style "ar_opt_hint" xpos 14 ypos 27
            textbutton ("ON" if persistent.enter_m_photosensitive else "OFF"):
                id "ar_setup_photosensitive"
                style "ar_toggle"
                xanchor 1.0 xpos 502 yalign .5
                tooltip "Takes the rapid brightness changes out of this mode and leaves the rest of it standing."
                action ToggleField(persistent, "enter_m_photosensitive")

screen asahina_rhythm_play(stage):
    modal True
    zorder 20
    use enter_m_input_lock()
    add stage
    if stage.paused:
        add Solid("#0a0616c4")
        add AR_UI + "vignette.png"
        vbox:
            xpos 96 ypos 176
            spacing 0
            text "PAUSED" style "ar_kicker" size 20 at ar_rise(0.0)
            null height 14
            button:
                id "ar_pause_resume"
                style "ar_pause_item"
                default_focus True
                action Function(stage.set_pause, False)
                at ar_slide(.02, -40)
                hbox:
                    spacing 14
                    text "‣" style "ar_pause_mark"
                    text "RESUME" style "ar_pause_text"
            button:
                id "ar_pause_retry"
                style "ar_pause_item"
                action Function(stage.finish, "retry")
                at ar_slide(.06, -40)
                hbox:
                    spacing 14
                    text "‣" style "ar_pause_mark"
                    text "RESTART SONG" style "ar_pause_text"
            button:
                id "ar_pause_quit"
                style "ar_pause_item"
                action Function(stage.finish, "quit")
                at ar_slide(.10, -40)
                hbox:
                    spacing 14
                    text "‣" style "ar_pause_mark"
                    text "LEAVE STAGE" style "ar_pause_text"
        vbox:
            xanchor 1.0 xpos 1220 ypos 44
            spacing 4
            at ar_rise(.05)
            text ar_fit_text(stage.chart["title"], 620, AR_FONT, 30, ((4, "#160f24", 0, 2),)) style "ar_pause_title" xalign 1.0 substitute False
            text ("%s / %s" % (ar_time_label(max(0, stage.now)), ar_time_label(stage.chart["duration"]))) style "ar_opt_value" xalign 1.0
            text ("SCORE {:,}".format(stage.game.score)) style "ar_opt_label" xalign 1.0
            if stage.tags:
                text "   •   ".join(stage.tags) style "ar_kicker" xalign 1.0 substitute False
        vbox:
            xpos 100 ypos 560
            spacing 8
            text "MUSIC VOLUME" style "ar_kicker"
            bar value Preference("music volume") xsize 380
            text "Timing and scroll options live in Song Select." style "ar_hint"
    key "K_ESCAPE" action Function(stage.escape)
    key "mouseup_3" action Function(stage.escape)
    # Last, so the wipes see input first (asahina_rhythm_finale.rpy).
    if stage.intro_wipe is not None:
        add stage.intro_wipe
    if stage.exit_wipe is not None:
        add stage.exit_wipe

screen asahina_rhythm_results(result, story=False, uncover=None):
    modal True
    zorder 40
    use enter_m_input_lock()
    # Arriving on a covered frame (asahina_rhythm_finale.rpy), the page clears
    # left to right, so each side's entrances wait for the plate to pass it.
    default enter_wipe = (ARWipe("uncover", uncover, hold=AR_WIPE_HOLD, grace=.45) if uncover else None)
    default leave_wipe = ARWipe("cover")
    default backdrop = ARResultsFX(result["outcome"] == "clear")
    default ribbon = ARRibbon(AR_PINK if result["outcome"] == "clear" else "#8a2a55", AR_GOLD if result["outcome"] == "clear" else "#fa698b", delay=(AR_WIPE_HOLD + AR_WIPE_TIME * .35) if uncover else 0.0)
    $ won = result["outcome"] == "clear"
    $ left = (AR_WIPE_HOLD + AR_WIPE_TIME * .35) if uncover else 0.0
    $ right = (AR_WIPE_HOLD + AR_WIPE_TIME * .75) if uncover else 0.0
    $ hero, rival = ("asahiko", "asahina") if won else ("asahina", "asahiko")
    $ total = max(1, sum(result["counts"].values()) + result["misses"])
    $ reason = ar_fail_text(result)
    $ reached = max(0.0, min(1.0, result.get("song_time", 0) / max(.001, result.get("song_length", 0))))
    $ tags = "   •   ".join(ar_mod_names(result.get("modifiers", ()), result["practice"], result["autoplay"]))
    $ accent = AR_PINK if won else "#fa698b"
    $ retry = Function(leave_wipe.arm, "retry", "enter", result["title"], tags or None)
    add AR_ART + "stage_blur.webp"
    add Solid("#12082ac4" if won else "#0a0512e6")
    add backdrop
    add Tile(AR_UI + "stripes.png") xysize (1376, 816) alpha (.5 if won else .2) at ar_drift
    add AR_UI + "vignette.png"

    # The winner takes the stage; the other one slumps in the wings.
    if won:
        add AR_FX + "burst_gold.png" zoom .95 xcenter 250 ycenter 452 alpha .30 at ar_spin(26.0)
    add AR_UI + "shadow.png" zoom .52 xcenter 486 ycenter 668
    add ar_menu_pose(rival, "lose", 1.2) zoom .80 xanchor .5 yanchor .96 xpos 486 ypos 672 matrixcolor SaturationMatrix(.5) * BrightnessMatrix(-.10 if won else -.14) at ar_rise(.30 + left)
    add AR_UI + "shadow.png" zoom .80 xcenter 250 ycenter 706
    add ar_menu_pose(hero, "win", .9) zoom 1.20 xanchor .5 yanchor .96 xpos 250 ypos 712 at ar_bop(.9)

    # ---- the header: the ribbon, the word, the song and why it ended ----
    add ribbon xpos 0 ypos 30
    use ar_results_header(("STAGE CLEAR!" if won else "SONG FAILED"), won, .10 + left)
    text ar_fit_text(result["title"], 560, AR_UI_FONT, 20, ((2, "#12082a", 0, 0),)) style "ar_tagline" size 20 xpos 48 ypos 150 substitute False at ar_rise(.45 + left)
    if reason:
        text reason style "ar_opt_hint" size 14 color "#fa8caa" xpos 48 ypos 177 substitute False at ar_rise(.55 + left)

    # ---- the card ----
    frame:
        style "ar_card"
        xpos 640 ypos 36 xysize (592, 648)
        at ar_slide(max(.05, right - .10), 60)
        fixed:
            add Solid(accent) xysize (548, 4)
            text "SCORE" style "ar_kicker" ypos 22
            add DynamicDisplayable(ar_count_up, value=result["score"], delay=.35 + right) ypos 40
            text ("ACCURACY  %.2f%%" % result["accuracy"]) style "ar_opt_value" ypos 104
            if won:
                if result["rank"] != "-":
                    fixed:
                        xpos 390 ypos 4 xysize (158, 158)
                        add AR_UI + "burst.png" zoom .30 align (.5, .5) matrixcolor TintMatrix("#ffcf5a") at ar_spin(18.0)
                        text result["rank"] style "ar_rank" align (.5, .5) at ar_stamp(.45 + right)
            else:
                # How far the song got, and a mark where it stopped.
                text "REACHED" style "ar_kicker" xanchor 1.0 xpos 548 ypos 22
                text ar_time_label(result.get("song_time", 0)) style "ar_reached" xanchor 1.0 xpos 548 ypos 38
                text ("OF " + ar_time_label(result.get("song_length", 0))) style "ar_opt_hint" size 14 xanchor 1.0 xpos 548 ypos 96
                fixed:
                    ypos 132 xysize (548, 24)
                    add Solid("#ffffff14") yalign .5 xysize (548, 8)
                    add Solid(accent) yalign .5 xysize (max(2, int(548 * reached)), 8) at ar_grow(.45 + right)
                    add Solid("#ffffff") xysize (12, 12) rotate 45 xanchor .5 yanchor .5 xpos int(548 * reached) ypos .5 at ar_rise(.95 + right)
            for i, (name, count, color) in enumerate(ar_result_rows(result)):
                fixed:
                    ypos 176 + i * 36
                    xysize (548, 32)
                    at ar_slide(.50 + right + i * .05, 24)
                    text name style "ar_tier" color color xpos 0 yalign .5
                    add Solid("#ffffff14") xpos 128 yalign .5 xysize (330, 12)
                    add Solid(color) xpos 128 yalign .5 xysize (max(2, int(330 * count / total)), 12) at ar_grow(.60 + right + i * .06)
                    text str(count) style "ar_tier_count" xanchor 1.0 xpos 548 yalign .5
            text ("BEST COMBO  {}      HOLD TICKS  {} / {}".format(result["max_combo"], result["hold_hits"], result["hold_total"])) style "ar_opt_label" ypos 366
            if result.get("fanfare_bonus"):
                text ("FANFARE BONUS  +{:,}".format(result["fanfare_bonus"])) style "ar_opt_value" size 17 ypos 390
            hbox:
                ypos 420
                xmaximum 548
                box_wrap True
                spacing 8
                box_wrap_spacing 6
                if result.get("new_record"):
                    frame:
                        style "ar_pill"
                        background Solid("#5fd8e833")
                        text "NEW PERSONAL BEST" style "ar_pill_text" color AR_CYAN
                for mod in result.get("new_mod_clears", ()):
                    frame:
                        style "ar_pill"
                        background Solid("#ffe08a2e")
                        text ("FIRST CLEAR WITH %s" % AR_MOD_NAMES[mod]) style "ar_pill_text" color AR_GOLD
                if result.get("coins"):
                    frame:
                        style "ar_pill"
                        background Solid("#ffe08a2e")
                        text ("+%d MATSUCOINS" % result["coins"]) style "ar_pill_text" color AR_GOLD
                if result["autoplay"]:
                    frame:
                        style "ar_pill"
                        text "AUTOPLAY: NO RECORDS OR REWARDS" style "ar_pill_text"
                elif result["practice"]:
                    frame:
                        style "ar_pill"
                        text "PRACTICE: NO RECORDS OR REWARDS" style "ar_pill_text"
                elif result.get("assisted"):
                    frame:
                        style "ar_pill"
                        text "EASIER MODIFIERS: NO RECORDS OR REWARDS" style "ar_pill_text"
                if tags:
                    frame:
                        style "ar_pill"
                        text tags style "ar_pill_text" color "#d9cdea" substitute False
            hbox:
                ypos 576
                spacing 12
                textbutton "RETRY" id "ar_results_retry" style "ar_button_primary" action retry
                if story:
                    textbutton "CONTINUE" id "ar_results_leave" style "ar_button" action Return("leave")
                else:
                    textbutton "SONGS" id "ar_results_songs" style "ar_button" action Function(leave_wipe.arm, "songs", "enter")
                    textbutton "LEAVE" id "ar_results_leave" style "ar_button" action Return("leave")
    key "K_ESCAPE" action Return("leave")
    # In the story, advancing past the card continues the scene; it never restarts the song.
    key "K_RETURN" action (Return("leave") if story else retry)
    # Last, so the wipes see input first.
    if enter_wipe is not None:
        add enter_wipe
    add leave_wipe

# ar_story: the Matsuda story owns the resolution, so a walk-off ends the mode
# and the results card offers CONTINUE in place of SONGS and LEAVE.
# ar_start_id: a story runback names its chart and skips song select once.
label asahina_rhythm_mode(arcade=False, ar_story=False, ar_start_id=None):
    python:
        _ar_previous_ui = (quick_menu, _game_menu_screen, _skipping, _dismiss_pause)
        renpy.context_dynamic("quick_menu", "_game_menu_screen", "_skipping", "_dismiss_pause")
        quick_menu = False
        _game_menu_screen = None
        _skipping = False
        _dismiss_pause = False
        renpy.block_rollback()
        _ar_previous_music_paused = renpy.music.get_pause(channel="music")
        renpy.music.set_pause(True, channel="music")
        _ar_last_result = None
        _ar_leave = False
        _ar_skip_to = ar_start_id
        # The palette of the wipe the last screen closed on, or None if it did
        # not close on one. The next screen clears that same wipe.
        _ar_wipe = None
    while not _ar_leave:
        $ _ar_songs, _ar_errors = ar_catalog()
        $ _ar_choice = next((i for i, song in enumerate(_ar_songs) if song["id"] == _ar_skip_to), None) if _ar_skip_to else None
        $ _ar_skip_to = None
        if _ar_choice is None:
            $ ar_menu_music(True)
            call screen asahina_rhythm_setup(_ar_songs, _ar_errors, uncover=_ar_wipe)
            $ _ar_choice = _return
            $ _ar_wipe = "enter" if isinstance(_ar_choice, int) else None
        if _ar_choice == "back":
            $ _ar_leave = True
        elif _ar_choice == "editor" or (isinstance(_ar_choice, tuple) and _ar_choice[0] == "editor"):
            $ ar_menu_music(False, fade=.3)
            if config.developer and renpy.has_label("asahina_rhythm_chart_editor"):
                # The studio opens the song that is selected in song select.
                call asahina_rhythm_chart_editor(_ar_songs[_ar_choice[1]]["id"] if isinstance(_ar_choice, tuple) else None) from _call_asahina_rhythm_chart_editor
        else:
            # The menu track fades under the countdown; the song starts on GO.
            $ ar_menu_music(False, fade=1.2)
            $ renpy.save_persistent()
            $ _ar_chart = _ar_songs[_ar_choice]
            $ _ar_retry = True
            while _ar_retry:
                $ _ar_stage = ARStage(_ar_chart, practice=persistent.asahina_rhythm_practice,
                                      autoplay=persistent.asahina_rhythm_autoplay,
                                      modifiers=ar_active_mods(), wipes=True, quit_cover=not ar_story)
                call screen asahina_rhythm_play(_ar_stage)
                $ _ar_result = _return
                # How far the run got, for the story outros. The core snapshot
                # stays free of timing, so its frame-rate tests keep comparing equal.
                # end_time is where the song stopped; a clear's outro keeps `now` running.
                $ _ar_result["song_time"] = max(0.0, _ar_stage.now if _ar_stage.end_time is None else _ar_stage.end_time)
                $ _ar_wipe = {"failed": "fail", "clear": "clear", "retry": "enter", "quit": None if ar_story else "enter"}.get(_ar_result["outcome"])
                $ _ar_result["song_length"] = _ar_chart["duration"]
                $ ar_stop()
                $ _ar_stage = None
                if _ar_result["outcome"] == "quit":
                    $ _ar_last_result = _ar_result
                    $ _ar_retry = False
                    if ar_story:
                        $ _ar_leave = True
                elif _ar_result["outcome"] == "retry":
                    pass
                else:
                    $ ar_record_result(_ar_chart, _ar_result)
                    if arcade and hasattr(store, "arcade_asahina_rhythm_award"):
                        $ _ar_result["coins"] = arcade_asahina_rhythm_award(_ar_result)
                    $ _ar_last_result = _ar_result
                    call screen asahina_rhythm_results(_ar_result, story=ar_story, uncover=_ar_wipe)
                    $ _ar_wipe = "enter" if _return in ("retry", "songs") else None
                    $ _ar_retry = _return == "retry"
                    $ _ar_leave = _return == "leave"
    python:
        ar_stop()
        ar_menu_music(False, fade=.5)
        renpy.music.set_pause(_ar_previous_music_paused, channel="music")
        quick_menu, _game_menu_screen, _skipping, _dismiss_pause = _ar_previous_ui
        renpy.block_rollback()
    return _ar_last_result

label asahina_rhythm_editor_preview(chart_data, start_time=0.0, autoplay=False):
    if not config.developer:
        return
    python:
        _ar_preview_chart = normalize_chart(chart_data)
        _ar_preview_start = max(0.0, min(start_time, _ar_preview_chart["duration"] - .1))
        _ar_preview_stage = ARStage(_ar_preview_chart, practice=True, autoplay=autoplay, start_time=_ar_preview_start)
    call screen asahina_rhythm_play(_ar_preview_stage)
    $ _ar_preview_result = _return
    $ ar_stop()
    $ _ar_preview_stage = None
    return _ar_preview_result

style ar_logo:
    font AR_FONT
    size 66
    color "#ffe3f1"
    outlines [(8, "#2a0f3a", 0, 5), (4, "#f06ba8", 0, 0)]
style ar_tagline:
    font AR_UI_FONT
    size 18
    color "#d9cdea"
    outlines [(2, "#12082a", 0, 0)]
style ar_kicker:
    font AR_UI_FONT
    size 15
    color "#f9a3ca"
    kerning 2.0
style ar_body:
    font AR_UI_FONT
    size 17
    color "#e2d7ef"
    xmaximum 570
style ar_hint:
    font AR_UI_FONT
    size 14
    color "#a595bd"

style ar_song:
    padding (0, 0)
    background Frame(AR_UI + "row_idle.png", 100, 12)
    hover_background Frame(AR_UI + "row_hover.png", 100, 12)
    selected_background Frame(AR_UI + "row_on.png", 100, 12)
    selected_hover_background Frame(AR_UI + "row_on_hot.png", 100, 12)
style ar_song_mark:
    font AR_UI_FONT
    size 34
    color "#00000000"
    hover_color "#f06ba8aa"
    selected_color AR_PINK
style ar_song_title:
    font AR_FONT
    size 40
    color "#bba9d0"
    hover_color "#ffe3f1"
    selected_color "#ffffff"
    outlines [(4, "#160f24", 0, 2)]
style ar_chip:
    background Frame(AR_UI + "tile_idle.png", 11, 11)
    padding (12, 5)
style ar_chip_text:
    font AR_UI_FONT
    size 15
    color "#efe6ff"
style ar_key:
    background Solid("#f6eefc")
    padding (10, 4)
    xminimum 34
style ar_key_text:
    font AR_UI_FONT
    size 19
    color "#1e1433"
    xalign .5

style ar_card:
    background Solid("#140c26e8")
    padding (22, 0, 22, 16)
style ar_name:
    font AR_FONT
    size 22
    outlines [(4, "#160f24", 0, 2)]
style ar_vs:
    font AR_FONT
    size 56
    color "#ffe08a"
    outlines [(7, "#160f24", 0, 4), (3, "#ffffff", 0, 0)]
style ar_best_rank:
    font AR_FONT
    size 62
    color "#ffe08a"
    outlines [(6, "#160f24", 0, 3)]
style ar_best_empty:
    font AR_FONT
    size 30
    color "#8d7fa6"

style ar_opt_label:
    font AR_UI_FONT
    size 17
    color "#f4ecff"
style ar_opt_hint:
    font AR_UI_FONT
    size 12
    color "#9d8fb5"
style ar_opt_value:
    font AR_UI_FONT
    size 19
    color "#ffe08a"
style ar_step:
    xysize (36, 32)
    background Frame(AR_UI + "plate_idle.png", 14, 14)
    hover_background Frame(AR_UI + "plate_pink.png", 14, 14)
style ar_step_text:
    font AR_UI_FONT
    size 20
    color "#ffffff"
    outlines [(2, "#160f24", 0, 1)]
    xalign .5
    yalign .5
style ar_toggle:
    padding (14, 8)
    background Frame(AR_UI + "plate_idle.png", 14, 14)
    hover_background Frame(AR_UI + "plate_hover.png", 14, 14)
    selected_background Frame(AR_UI + "plate_cyan.png", 14, 14)
    selected_hover_background Frame(AR_UI + "plate_cyan_hot.png", 14, 14)
style ar_toggle_text:
    font AR_UI_FONT
    size 16
    color "#d9cdea"
    selected_color "#0d2b33"

style ar_button:
    padding (24, 11)
    background Frame(AR_UI + "plate_idle.png", 14, 14)
    hover_background Frame(AR_UI + "plate_hover.png", 14, 14)
    insensitive_background Frame(AR_UI + "plate_off.png", 14, 14)
style ar_button_text:
    font AR_FONT
    size 24
    color "#fff3ef"
    insensitive_color "#7d6f90"
    outlines [(3, "#160f24", 0, 2)]
style ar_button_primary is ar_button:
    background Frame(AR_UI + "plate_pink.png", 14, 14)
    hover_background Frame(AR_UI + "plate_pink_hot.png", 14, 14)
style ar_button_primary_text is ar_button_text

style ar_rank:
    font AR_FONT
    size 92
    color "#ffffff"
    outlines [(8, "#160f24", 0, 4)]
style ar_tier:
    font AR_FONT
    size 21
    outlines [(3, "#160f24", 0, 1)]
style ar_tier_count:
    font AR_UI_FONT
    size 20
    color "#ffffff"
style ar_pill:
    background Frame(AR_UI + "tile_idle.png", 11, 11)
    padding (13, 6)
style ar_pill_text:
    font AR_UI_FONT
    size 14
    color "#f4ecff"

style ar_pause_item:
    padding (0, 2)
style ar_pause_mark:
    font AR_UI_FONT
    size 42
    color "#00000000"
    hover_color AR_PINK
    yalign .5
style ar_pause_text:
    font AR_FONT
    size 54
    color "#8d7fa6"
    hover_color "#ffffff"
    outlines [(5, "#160f24", 0, 3)]
style ar_pause_title:
    font AR_FONT
    size 30
    color "#ffffff"
    outlines [(4, "#160f24", 0, 2)]
