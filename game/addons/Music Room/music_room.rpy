# =============================================================================
# music_room.rpy  --  MUSIC ROOM / SOUNDTRACK PLAYER (archive feature)
# =============================================================================
#
# WHAT THIS FILE PROVIDES
#   A jukebox for the mod's soundtrack: a scrollable track list on the left and a
#   "now playing" player on the right (random CG art, title/artist, a live
#   progress bar + time, and prev/play-pause/next controls).
#
# HOW IT IS REACHED
#   - Archive "Music Room" card -> Show("music_room")   (see game/archive.rpy).
#
# UNLOCKING
#   Every track is locked until the player has HEARD it -- anywhere, on any music
#   channel, in the story or a fight or the menus. music_scan_now_playing() runs
#   once per interaction and marks whatever is coming out of the speakers as
#   recovered; see the comment on it for why this is a scan and not a call
#   beside every `play music`. Locked rows keep their slot and their number but
#   show "???", and prev/next/shuffle step over them.
#   The room ITSELF is still gated as a whole by persistent.archive_unlocked_music
#   (end of Chapter 0.5) -- it is the Archive's one whole-panel reward.
#
# RUNTIME STATE (module-level python vars, NOT persistent)
#   - music_library    : list[MusicTrack], built once by init_music_library().
#   - current_track    : the MusicTrack currently selected/playing (or None).
#   - is_playing       : bool play/pause flag the UI reads to pick its icon.
#   - music_current_cg : path of the random CG shown as "now playing" art.
#   Audio uses Matsu'Py's "music" channel. Repeat-one explicitly loops the current
#   file; repeat-all/no-repeat explicitly do not, so the poller can detect the
#   track end and advance or stop. renpy.restart_interaction() after each change
#   forces the screen to redraw with the new state.
#
# CROSS-FILE DEPENDENCY
#   - pick_random_cg() reads cg_gallery_catalog from
#     game/addons/CG View/cg_gallery.rpy. Wrapped in try/except so the Music Room
#     still works even if that catalog is missing/empty.
#
# IMPORTANT EXIT BEHAVIOUR
#   leave_music_room() restores the archive BGM (roster_place.ogg) so closing the
#   player does not leave the menu silent. Both ESC and the header Return call it.
#
# SHARED THEME BORROWED FROM game/archive.rpy
#   - screen archive_backdrop, screen archive_header(...)
#   - style archive_shell_frame; viewport style_prefix "cs_sv" (undefined ->
#     Matsu'Py default scrollbar, same as cg_gallery.rpy).
# =============================================================================

# Music Room Addon
# Provides a music player for listening to the mod's soundtrack

init python:
    # Channels a track can be HEARD on. Any of these playing a file in the
    # library counts as the player having encountered that track -- def_audio.rpy
    # registers track1..track4 as extra music channels for the fights and the
    # arcade modes, so watching "music" alone would leave half the soundtrack
    # permanently unrecoverable.
    MUSIC_ROOM_LISTEN_CHANNELS = ("music", "track1", "track2", "track3", "track4")

    def music_key_from_path(file_path):
        """
        Turn "assets/audio/bgm/13am.ogg" into "music_heard_mod_assets_bgm_13am".

        Same reasoning as cg_key_from_path (CG View/cg_gallery.rpy): the track IS
        its file, the library is long enough that a hand-written second column
        would drift, and a derived key cannot disagree with the audio it gates.
        Existing entries pass their pre-consolidation path explicitly below;
        those derived values are now stable IDs, independent of where the audio
        file lives today.
        """
        cleaned = str(file_path).lower()
        for junk in ("\\", "/", " ", "-", ".", "'"):
            cleaned = cleaned.replace(junk, "_")
        while "__" in cleaned:
            cleaned = cleaned.replace("__", "_")
        for suffix in ("_ogg", "_mp3", "_wav", "_opus"):
            if cleaned.endswith(suffix):
                cleaned = cleaned[:-len(suffix)]
        return "music_heard_" + cleaned.strip("_")

    # One soundtrack entry. A track is locked until the player has actually heard
    # it somewhere in the game (see music_scan_now_playing below); the room as a
    # whole is gated upstream by persistent.archive_unlocked_music.
    class MusicTrack:
        def __init__(self, title, artist, file_path, legacy_file_path=None):
            self.title = title
            self.artist = artist
            self.file_path = file_path
            # Unlock keys used to be derived from physical paths. Keep deriving
            # them from each track's OLD path so moving bgm/ + assets/audio/bgm/
            # into assets/audio/bgm/ does not relock existing profiles.
            self.persistent_key = music_key_from_path(legacy_file_path or file_path)

        @property
        def is_unlocked(self):
            return bool(getattr(persistent, self.persistent_key, False))

    # The playlist. Rebuilt at init by init_music_library() (see init 5 below).
    # Track ORDER here is the order shown in the list and the order prev/next cycle.
    music_library = []

    def init_music_library():
        global music_library
        music_library = [
            MusicTrack(
                "The Way Home",
                "San-Z Studio",
                audio.roster_place,
                "assets/audio/bgm/roster_place.ogg"
            ),
            # Add more tracks here as they become available
            MusicTrack(
                "13 AM",
                "Toby Fox",
                audio.hopeless,
                "assets/audio/bgm/13am.ogg"
            ),
            MusicTrack(
                "12 AM",
                "Toby Fox",
                audio.twelveam,
                "assets/audio/bgm/12am.ogg"
            ),
            MusicTrack(
                "Can You Feel",
                "Torchkas",
                audio.canyoufeel,
                "assets/audio/bgm/canyoufeel.ogg"
            ),
            MusicTrack(
                "Lofi Coffee",
                "M ali",
                audio.mainmenu,
                "assets/audio/bgm/mainmenu.ogg"
            ),
            MusicTrack(
                "Grandma",
                "Square Enix",
                audio.grandma,
                "assets/audio/bgm/grandma.mp3"
            ),
            MusicTrack(
                "The Incomplete Stone",
                "Square Enix",
                audio.stone,
                "assets/audio/bgm/stone.mp3"
            ),
            MusicTrack(
                "City of Commerce",
                "Square Enix",
                audio.seafront,
                "assets/audio/bgm/seafront.mp3"
            ),
            MusicTrack(
                "Fleeting Words - Family",
                "Square Enix",
                audio.family,
                "assets/audio/bgm/family.mp3"
            ),
            MusicTrack(
                "Snow in Summer",
                "Square Enix",
                audio.sis,
                "assets/audio/bgm/sis.mp3"
            ),
            MusicTrack(
                "Song of the Ancients - Devola",
                "Square Enix",
                audio.devola,
                "assets/audio/bgm/devola.mp3"
            ),
            MusicTrack(
                "Song of the Ancients - Popola",
                "Square Enix",
                audio.popola,
                "assets/audio/bgm/popola.mp3"
            ),
            MusicTrack(
                "Song of the Ancients - Hollow Dreams",
                "Square Enix",
                audio.hollow,
                "assets/audio/bgm/hollow.mp3"
            ),
            MusicTrack(
                "This Dream",
                "Square Enix",
                audio.dream,
                "assets/audio/bgm/dream.mp3"
            ),
            MusicTrack(
                "Beautiful Days (16-bit)",
                "Spike Chunsoft",
                audio.beautiful,
                "assets/audio/bgm/beautiful.mp3"
            ),
            MusicTrack(
                "All Star Apologies (16-bit)",
                "Spike Chunsoft",
                audio.apology,
                "assets/audio/bgm/apology.mp3"
            ),
            MusicTrack(
                "Dump",
                "Toby Fox",
                audio.dump,
                "assets/audio/bgm/dump.ogg"
            ),
            MusicTrack(
                "Temple of Drifting Sands",
                "Square Enix",
                audio.sands,
                "assets/audio/bgm/sands.mp3"
            ),
            MusicTrack(
                "Wretched Automatons",
                "Square Enix",
                audio.automatons,
                "assets/audio/bgm/automatons.mp3"
            ),
            MusicTrack(
                "Blu Bird",
                "Square Enix",
                audio.blubird,
                "assets/audio/bgm/blubird.mp3"
            ),
            MusicTrack(
                "60% Daily Fantasy",
                "San-Z Studio",
                audio.dailyfantasy,
                "assets/audio/bgm/dailyfantasy.ogg"
            ),
            MusicTrack(
                "60% Fantasy Passion",
                "San-Z Studio",
                audio.fantasypassion,
                "assets/audio/bgm/fantasypassion.ogg"
            ),
            MusicTrack(
                "60% Daily Leisure",
                "San-Z Studio",
                audio.dailyleisure,
                "assets/audio/bgm/dailyleisure.ogg"
            ),
            MusicTrack(
                "60% Daily",
                "San-Z Studio",
                audio.daily,
                "assets/audio/bgm/daily.ogg"
            ),
            MusicTrack(
                "60% Fantasy Serenity",
                "San-Z Studio",
                audio.fantasyserenity,
                "assets/audio/bgm/fantasyserenity.ogg"
            ),
            MusicTrack(
                "Scheduled Programming",
                "L4w1i3t",
                audio.holdmusic,
                "assets/audio/bgm/holdmusic.ogg"
            ),
            MusicTrack(
                "Black Knife",
                "Toby Fox",
                audio.epicbattlephase1,
                "assets/audio/bgm/epicbattlephase1.ogg"
            ),
            MusicTrack(
                "GUARDIAN",
                "Toby Fox",
                audio.epicbattlephase2,
                "assets/audio/bgm/epicbattlephase2.ogg"
            ),
            MusicTrack(
                "Safety",
                "--",
                audio.safety,
                "assets/audio/bgm/safety.ogg"
            ),
            MusicTrack(
                "Mike, the BOARD Please!",
                "Toby Fox",
                audio.quiz,
                "assets/audio/bgm/quiz.ogg"
            ),
            MusicTrack(
                "School Days",
                "ATLUS",
                audio.schooldays,
                "assets/audio/bgm/schooldays.ogg"
            ),
            MusicTrack(
                "03/31",
                "ATLUS",
                audio.enterm,
                "assets/audio/bgm/enterm.ogg"
            ),
            MusicTrack(
                "Scamall Hollow",
                "San-Z Studio",
                audio.scamall,
                "assets/audio/bgm/scamall.ogg"
            ),
            MusicTrack(
                "Montagem Toma",
                "MXZI, sk3tch01, X972",
                audio.enter_m_op,
                "assets/audio/bgm/opsong.ogg"
            ),
            MusicTrack(
                "Sound of Justice",
                "Toby Fox",
                audio.mm_phase4,
                "assets/audio/bgm/mm_phase4.ogg"
            ),
            MusicTrack(
                "Embraced by the Flame (Inst.)",
                "UNDEAD CORPORATION",
                audio.embracedflame_inst,
                "assets/audio/bgm/embracedbytheflameinst.ogg"
            ),
            MusicTrack(
                "Embraced by the Flame (Vocal)",
                "UNDEAD CORPORATION",
                audio.embracedflame_vocal,
                "assets/audio/bgm/embracedbytheflamevocal.ogg"
            ),
            MusicTrack(
                "Petal Dance",
                "Toby Fox",
                audio.kotoboss,
                "assets/audio/bgm/kotobossmusic.ogg"
            ),
            MusicTrack(
                "worldenddominator",
                "zts",
                audio.kotoendlessmode,
                "assets/audio/bgm/kotoendlessmode.ogg"
            ),
            MusicTrack(
                "Dusk",
                "Team Salvato",
                audio.hearttoheart,
                "assets/audio/bgm/hearttoheart.ogg"
            ),
            MusicTrack(
                "muirtA dnoceS",
                "xoF yboT",
                audio.tails,
                "assets/audio/bgm/tails.ogg"
            ),
            MusicTrack(
                "Green Room",
                "Toby Fox",
                audio.arcade_theme,
                "assets/audio/bgm/arcade.ogg"
            ),
            MusicTrack(
                "Flower Man",
                "Toby Fox",
                audio.tsubaphase1,
                "assets/audio/bgm/tsubaphase1.ogg"
            ),
            MusicTrack(
                "Flower Man (Teto Cover)",
                "Toby Fox, TheCappuccino04",
                audio.tsubaphase2,
                "assets/audio/bgm/tsubaphase2.ogg"
            ),
            MusicTrack(
                "YOU Actually Changed!",
                "Toby Fox",
                audio.noreturn,
                "assets/audio/bgm/noreturn.ogg"
            ),
            MusicTrack(
                "Smooth Sailing",
                "Dylan Sitts",
                audio.smoothsailing,
                "assets/audio/bgm/ch4_night.ogg"
            ),
            MusicTrack(
                "Samsara",
                "Nihilore",
                audio.samsara,
                "assets/audio/bgm/ch4_serious.ogg"
            ),
            MusicTrack(
                "Emotions",
                "Falling Forever",
                audio.emotions,
                "assets/audio/bgm/ch4_day.ogg"
            ),
            MusicTrack(
                "Opus No. 1",
                "Tim Carleton",
                audio.opus1,
                "assets/audio/bgm/ch5_day.ogg"
            ),
            MusicTrack(
                "ReDreaming Angel",
                "San-Z Studio",
                audio.tetris,
                "assets/audio/bgm/tetris.ogg"
            ),
            MusicTrack(
                "Black Wolf",
                "San-Z Studio",
                audio.blackwolf,
                "assets/audio/bgm/blackwolf.ogg"
            ),
            MusicTrack(
                "Black Wolf (Corruptive Barrier)",
                "San-Z Studio",
                audio.blackwolf_corruptive,
                "assets/audio/bgm/blackwolf_corruptive.ogg"
            ),
        ]

    # -------------------------------------------------------------------------
    # UNLOCKING: a track is recovered by being heard, wherever it played.
    #
    # WHY A SCAN AND NOT A CALL AT EVERY `play music`. There are hundreds of play
    # statements across the story, the fights, the arcade cabinets and the menus,
    # and every one of them would need a partner line that could be forgotten --
    # and a forgotten one is invisible, because the symptom is a track quietly
    # missing from a room the player may not open for hours. Watching what is
    # actually coming out of the speakers has no such failure mode, and it is
    # correct by construction: heard is exactly the unlock condition.
    #
    # This runs on config.start_interact_callbacks (once per line of dialogue,
    # menu, or pause), which is far more often than the music changes -- so the
    # common path is a handful of get_playing() calls and a dict hit.
    # -------------------------------------------------------------------------
    _music_by_file = {}

    def music_index_library():
        """Rebuild the filename -> MusicTrack lookup the scan reads."""
        global _music_by_file
        _music_by_file = {_music_normalize_file(t.file_path): t for t in music_library}

    def _music_normalize_file(name):
        """Strip Matsu'Py's playback prefix: "<from 3.0 loop 0>bgm/x.ogg" -> "bgm/x.ogg"."""
        text = str(name or "")
        if ">" in text:
            text = text.rsplit(">", 1)[1]
        return text.strip().lower().replace("\\", "/")

    def music_unlock(*file_paths):
        """Mark tracks heard, by file path. The scan below is the usual caller."""
        changed = False

        for file_path in file_paths:
            track = _music_by_file.get(_music_normalize_file(file_path))
            if track is None or track.is_unlocked:
                continue
            setattr(persistent, track.persistent_key, True)
            changed = True

        if changed:
            renpy.save_persistent()

    def music_scan_now_playing():
        for channel in MUSIC_ROOM_LISTEN_CHANNELS:
            try:
                playing = renpy.music.get_playing(channel=channel)
            except Exception:
                continue
            if playing:
                music_unlock(playing)

    def music_unlocked_tracks():
        return [t for t in music_library if t.is_unlocked]

    def music_all_keys():
        """Every track's persistent key (for the dev all-content switch)."""
        return tuple(t.persistent_key for t in music_library)

    # --- Playback state (read by the screen) ---
    current_track = None
    is_playing = False
    music_current_cg = None

    # Play-mode: how the room behaves when a track finishes.
    #   REPEAT_ALL -> advance to the next track (wraps / respects shuffle)
    #   REPEAT_ONE -> loop the current track forever
    #   NO_REPEAT  -> stop at the end of the current track
    MODE_REPEAT_ALL = 0
    MODE_REPEAT_ONE = 1
    MODE_NO_REPEAT = 2
    play_mode = MODE_REPEAT_ALL
    shuffle_on = False

    # Internal: guards the auto-advance poller against a false "ended" reading in
    # the brief window between issuing renpy.music.play and the file actually
    # starting. We only treat "nothing playing" as a real end once we've seen the
    # channel report a live track at least once for the current selection.
    _seen_playing = False

    def pick_random_cg():
        """Return the path of a random unlocked CG, or None if none exist yet."""
        # Reads the CG catalog from CG View/cg_gallery.rpy. try/except guards
        # against that file being absent or the catalog being empty.
        import random
        try:
            unlocked = [
                cg.image_path
                for act in cg_gallery_catalog
                for ch in act.chapters
                for cg in ch.cgs
                if cg.unlocked
            ]
        except Exception:
            unlocked = []
        return random.choice(unlocked) if unlocked else None

    # Format a float seconds value as "M:SS" for the time readouts.
    def format_time(seconds):
        if seconds is None or seconds < 0:
            return "0:00"
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return "{}:{:02d}".format(minutes, secs)

    # Human labels for the play-mode toggle button.
    def play_mode_label():
        return {
            MODE_REPEAT_ALL: "REPEAT ALL",
            MODE_REPEAT_ONE: "REPEAT ONE",
            MODE_NO_REPEAT: "NO REPEAT",
        }.get(play_mode, "REPEAT ALL")

    def _loop_current():
        """Should the currently-issued file be told to loop forever?"""
        return play_mode == MODE_REPEAT_ONE

    def _play_current_file(from_pos=None):
        """Issue current_track with an explicit loop flag for the active mode."""
        if current_track is None:
            return

        should_loop = _loop_current()
        prefix = ""

        if from_pos is not None:
            if from_pos < 0:
                from_pos = 0.0
            if should_loop:
                prefix = "<from {:.3f} loop 0>".format(from_pos)
            else:
                prefix = "<from {:.3f}>".format(from_pos)
        elif should_loop:
            prefix = "<loop 0>"

        renpy.music.play(
            prefix + current_track.file_path,
            channel="music",
            loop=should_loop)

    def start_track(track):
        """Core: begin playback of `track`, honouring the current loop mode."""
        global current_track, is_playing, music_current_cg, _seen_playing
        if track is None:
            return
        current_track = track
        is_playing = True
        _seen_playing = False
        music_current_cg = pick_random_cg()
        _play_current_file()
        renpy.restart_interaction()

    # Every step below walks the UNLOCKED list, not the library: prev/next and
    # shuffle must not be a back door into a track the player has not heard yet,
    # and skipping over locked entries is also what a player expects -- the gaps
    # in the list are not stops.
    def _neighbour_track(step):
        """Sequential step (+1/-1) through the unlocked tracks, wrapping."""
        unlocked = music_unlocked_tracks()
        if not unlocked:
            return None
        try:
            i = unlocked.index(current_track)
        except ValueError:
            return unlocked[0]
        return unlocked[(i + step) % len(unlocked)]

    def _random_track():
        """A random unlocked track other than the current one (if possible)."""
        import random
        unlocked = music_unlocked_tracks()
        if not unlocked:
            return None
        choices = [t for t in unlocked if t is not current_track] or unlocked
        return random.choice(choices)

    def play_next_track():
        """Advance to the next track (random when shuffle is on)."""
        start_track(_random_track() if shuffle_on else _neighbour_track(1))

    def play_previous_track():
        """Back a track. Like most players, if we're a few seconds into the
        current track, restart it instead of skipping to the previous one."""
        pos = renpy.music.get_pos(channel="music")
        if current_track is not None and pos is not None and pos > 3.0:
            start_track(current_track)
            return
        start_track(_random_track() if shuffle_on else _neighbour_track(-1))

    def toggle_playback():
        """Play/pause. Uses real channel pause so the position is preserved."""
        global is_playing
        if current_track is None:
            unlocked = music_unlocked_tracks()
            if unlocked:
                start_track(unlocked[0])
            return
        if is_playing:
            is_playing = False
            renpy.music.set_pause(True, channel="music")
            renpy.restart_interaction()
        else:
            # Paused mid-track -> resume; ended/stopped -> replay from the top.
            if renpy.music.get_playing(channel="music") is not None:
                is_playing = True
                renpy.music.set_pause(False, channel="music")
                renpy.restart_interaction()
            else:
                start_track(current_track)

    def toggle_shuffle():
        global shuffle_on
        shuffle_on = not shuffle_on
        renpy.restart_interaction()

    def cycle_play_mode():
        """Rotate REPEAT ALL -> REPEAT ONE -> NO REPEAT. If a track is playing,
        re-issue it from its current position so the new loop flag takes effect
        immediately rather than only at the next track change."""
        global play_mode, _seen_playing
        play_mode = (play_mode + 1) % 3
        if current_track is not None and is_playing:
            pos = renpy.music.get_pos(channel="music")
            if pos is None or pos < 0:
                pos = 0.0
            _seen_playing = False
            _play_current_file(pos)
        renpy.restart_interaction()

    def music_poll_playback():
        """Called on a screen timer: when the current track has finished, do
        whatever the play-mode dictates (advance / stop). REPEAT ONE loops on its
        own so it is never treated as finished."""
        global is_playing, _seen_playing
        if not is_playing or current_track is None or _loop_current():
            return
        if renpy.music.get_playing(channel="music") is not None:
            _seen_playing = True
            return
        # Channel reports nothing playing.
        if _seen_playing:
            _seen_playing = False
            if play_mode == MODE_REPEAT_ALL:
                play_next_track()
            else:  # MODE_NO_REPEAT
                is_playing = False
                renpy.music.stop(channel="music")
                renpy.restart_interaction()

    def leave_music_room():
        """Clean exit: stop playback, restore archive BGM, hide screen."""
        # Critical so the Archive isn't left silent after the room closes.
        global current_track, is_playing, _seen_playing
        is_playing = False
        current_track = None
        _seen_playing = False
        renpy.music.play(audio.roster_place, channel="music")
        renpy.hide_screen("music_room")

    # The two callbacks below feed DynamicDisplayable widgets that re-evaluate on
    # a timer (the second tuple element is the redraw delay in seconds): current
    # position polls ~10x/sec, total duration ~1x/sec.
    def music_time_current(st, at):
        """DynamicDisplayable callback for current position."""
        pos = renpy.music.get_pos(channel="music")
        if pos is None:
            pos = 0.0
        return Text(format_time(pos), style="music_time"), 0.1

    def music_time_total(st, at):
        """DynamicDisplayable callback for total duration."""
        duration = renpy.music.get_duration(channel="music")
        if duration is None or duration <= 0:
            duration = 0.0
        return Text(format_time(duration), style="music_time"), 1.0

    def music_volume_pct(mixer="music"):
        """The deck's volume readout, as the SLIDER'S OWN position (0-100).

        Not the stored amplitude. Ren'Py mixer sliders are logarithmic over
        config.volume_db_range unless config.quadratic_volumes is on, so
        `get_volume() * 100` reads about 3% with the handle sitting exactly
        halfway -- which looks like a bug rather than a scale. Dividing the
        mixer position by the same range the adjustment uses makes the number
        and the handle agree at every point.
        """
        rng = 1.0 if config.quadratic_volumes else (config.volume_db_range * 1.0)
        if not rng:
            return 0
        return int(round(100.0 * MixerValue(mixer).get_mixer() / rng))

# init 5 so music_library is rebuilt after the class above is defined.
init 5 python:
    init_music_library()
    music_index_library()

# init 6 so the lookup the scan reads already exists. Same guarded-append pattern
# as atmosphere.rpy / achievements.rpy -- see roster_scan_worn_outfits for the
# note on hot reloads slipping past the guard (the scan is idempotent, so a
# duplicate costs one no-op pass).
init 6 python:
    if music_scan_now_playing not in config.start_interact_callbacks:
        config.start_interact_callbacks.append(music_scan_now_playing)

# Named transforms for music room (panel entrances; cosmetic).
transform music_panel_left:
    alpha 0.0
    xoffset -25
    pause 0.15
    easein 0.35 alpha 1.0 xoffset 0

transform music_panel_right:
    alpha 0.0
    xoffset 25
    pause 0.15
    easein 0.35 alpha 1.0 xoffset 0

# One bouncing equalizer bar. `d` staggers each bar; `lo` is the resting height.
# Anchored at the bottom so yzoom grows the bar upward like a real EQ.
transform music_eq_bar(d=0.0, lo=0.35):
    subpixel True
    yanchor 1.0
    ypos 20
    yzoom lo
    pause d
    block:
        easeout 0.30 yzoom 1.0
        easein 0.30 yzoom lo
        repeat

# Tiny 3-bar equalizer used as the "now playing" indicator on the active row.
# When inactive it shows three short flat stubs instead.
screen music_eq(active):
    fixed:
        xysize (20, 20)
        if active:
            add Solid("#56d7ff") xysize (4, 20) xpos 0 at music_eq_bar(0.0, 0.35)
            add Solid("#56d7ff") xysize (4, 20) xpos 8 at music_eq_bar(0.18, 0.6)
            add Solid("#56d7ff") xysize (4, 20) xpos 16 at music_eq_bar(0.34, 0.25)
        else:
            add Solid("#33414d") xysize (4, 6) xpos 0 ypos 14
            add Solid("#33414d") xysize (4, 6) xpos 8 ypos 14
            add Solid("#33414d") xysize (4, 6) xpos 16 ypos 14

# =============================================================================
# MUSIC ROOM SCREEN
# Layout: header, then an hbox of [track list panel | player panel].
# =============================================================================
# Music Room Main Screen
screen music_room():
    modal True

    # Search query for the track-list filter (QoL for a long soundtrack).
    default query = ""

    # Stop the archive BGM on open (the player will handle its own audio)
    on "show" action Function(renpy.music.stop, channel="music")

    use archive_backdrop

    # ESC / header Return both go through leave_music_room() to restore BGM.
    key "game_menu" action Function(leave_music_room)
    key "K_ESCAPE" action Function(leave_music_room)

    # Auto-advance driver: polls twice a second so a finished track can hand off
    # to the next one (or stop) per the current play-mode.
    timer 0.5 action Function(music_poll_playback) repeat True

    # Build the filtered view of the library. Each entry keeps its ORIGINAL index
    # so track numbering stays stable even while filtering.
    #
    # A SEARCH ONLY EVER MATCHES RECOVERED TRACKS. Locked rows show "???" rather
    # than their title, so letting the filter read the real title would hand the
    # player a way to confirm a track exists -- and its name -- by typing at it.
    # With a query live the locked rows simply drop out; with no query they stay
    # in place, because the gaps in the list are the point.
    python:
        _q = query.strip().lower()
        _filtered = [
            (i, t) for i, t in enumerate(music_library)
            if (not _q) or (t.is_unlocked and (_q in t.title.lower() or _q in t.artist.lower()))
        ]
        _now_title = current_track.title if current_track else None
        _m_found = len(music_unlocked_tracks())
        _mvol = music_volume_pct()

    frame:
        style "archive_shell_frame"
        at archive_frame_enter(40, 0.4)

        vbox:
            spacing 12

            use archive_header("MUSIC ROOM", Function(leave_music_room))

            # Census / readout strip: track count + live now-playing status.
            use archive_readout(
                "SOUNDTRACK // {}/{} TRACKS RECOVERED".format(_m_found, len(music_library)),
                ("NOW PLAYING: " + _now_title) if _now_title else "IDLE")

            hbox:
                spacing 18
                xalign 0.5

                # --- LEFT: scrollable track list --------------------------
                frame:
                    style "music_list_frame"
                    at music_panel_left

                    vbox:
                        spacing 8

                        # Header + result count.
                        frame:
                            background Solid("#07111dcc")
                            xfill True
                            padding (12, 7)

                            hbox:
                                yalign 0.5
                                text "TRACK LIST" style "music_list_header"
                                null width 1 xfill True
                                text "{}/{}".format(len(_filtered), len(music_library)):
                                    style "music_list_count"
                                    yalign 0.5

                        # Search box (filters by title or artist).
                        frame:
                            background Solid("#050811cc")
                            xfill True
                            padding (12, 6)

                            hbox:
                                spacing 10
                                yalign 0.5

                                add Solid("#56d7ff") xysize (3, 18) yalign 0.5
                                text "FIND" style "music_search_label" yalign 0.5

                                fixed:
                                    xysize (400, 24)
                                    yalign 0.5

                                    if query == "":
                                        text "Search title or artist..." style "music_search_hint" yalign 0.5
                                    input:
                                        value ScreenVariableInputValue("query")
                                        style "music_search_input"
                                        yalign 0.5
                                        copypaste True
                                        pixel_width 400

                                if query != "":
                                    textbutton "CLEAR":
                                        style "music_clear_button"
                                        yalign 0.5
                                        action SetScreenVariable("query", "")

                        # Scrollable track list
                        viewport:
                            style_prefix "archive_sv"
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            pagekeys True
                            xsize 530
                            ysize 392

                            vbox:
                                spacing 6
                                xsize 510

                                if not _filtered:
                                    frame:
                                        xfill True
                                        ysize 120
                                        background Solid("#07111dcc")

                                        text "No tracks match \"[query]\".":
                                            style "music_no_track"
                                            align (0.5, 0.5)
                                else:
                                    for _row, (idx, track) in enumerate(_filtered):
                                        # Highlight the row matching current_track.
                                        $ _is_active = (track == current_track)
                                        $ _is_found = track.is_unlocked

                                        button:
                                            style "music_track_button"
                                            sensitive _is_found
                                            if _is_active:
                                                background Solid("#12314af2")
                                                hover_background Solid("#17415fee")
                                            action Function(start_track, track)
                                            at transform:
                                                on show:
                                                    alpha 0.0
                                                    xoffset 15
                                                    pause _row * 0.04   # staggered list reveal
                                                    easein 0.25 alpha 1.0 xoffset 0

                                            hbox:
                                                spacing 12
                                                yalign 0.5

                                                # Index column doubles as the now-playing indicator.
                                                fixed:
                                                    xysize (28, 34)
                                                    yalign 0.5
                                                    if _is_active:
                                                        use music_eq(is_playing)
                                                    else:
                                                        $ _tnum = idx + 1
                                                        text "[_tnum].":
                                                            style ("music_track_number" if _is_found else "music_track_number_locked")
                                                            align (0.0, 0.5)

                                                vbox:
                                                    spacing 2
                                                    yalign 0.5

                                                    # An unheard track keeps its
                                                    # SLOT and its number -- the
                                                    # player can see how much of
                                                    # the soundtrack is still out
                                                    # there, and where -- but not
                                                    # its title, which for a
                                                    # score is half the spoiler.
                                                    if _is_found:
                                                        text track.title style "music_track_title"
                                                        text track.artist style "music_track_artist"
                                                    else:
                                                        text "???" style "music_track_title_locked"
                                                        text "NOT YET HEARD" style "music_track_artist_locked"

                # --- RIGHT: now-playing player ----------------------------
                frame:
                    style "music_player_frame"
                    at music_panel_right

                    vbox:
                        spacing 10
                        xalign 0.5

                        frame:
                            background Solid("#07111dcc")
                            xfill True
                            padding (12, 7)

                            hbox:
                                spacing 10
                                yalign 0.5
                                xalign 0.5
                                use music_eq(is_playing and current_track is not None)
                                text "NOW PLAYING" style "music_player_header" yalign 0.5

                        null height 2

                        # Visualization area — random CG thumbnail
                        # (music_current_cg is chosen by pick_random_cg() on each
                        #  track change; placeholder text if no CGs exist.)
                        frame:
                            xsize 340
                            ysize 150
                            xalign 0.5
                            background Solid("#07101add")
                            padding (0, 0, 0, 0)

                            if music_current_cg:
                                add music_current_cg:
                                    fit "cover"
                                    xsize 340
                                    ysize 150
                                    xalign 0.5
                                    yalign 0.5
                            else:
                                text "No Track Selected" style "music_no_track"

                        null height 4

                        # Track info (always rendered, placeholder when empty)
                        vbox:
                            spacing 5
                            xalign 0.5
                            xsize 340

                            if current_track:
                                text current_track.title style "music_now_playing_title"
                                text current_track.artist style "music_now_playing_artist"
                            else:
                                text "---" style "music_now_playing_title"
                                text " " style "music_now_playing_artist"

                            null height 4

                            # Progress bar -- AudioPositionValue auto-tracks the
                            # "music" channel playhead (read-only display).
                            bar:
                                value AudioPositionValue(channel="music")
                                xsize 320
                                ysize 6
                                xalign 0.5
                                left_bar Solid("#56d7ff")
                                right_bar Solid("#102338")
                                thumb None
                                thumb_offset 0

                            # Time display (current | total) via DynamicDisplayables.
                            hbox:
                                xsize 320
                                xalign 0.5

                                add DynamicDisplayable(music_time_current)

                                text " " xalign 0.5

                                add DynamicDisplayable(music_time_total):
                                    xalign 1.0

                        null height 4

                        # Transport controls.
                        # |<< previous   ||/>  play-pause   >>| next
                        hbox:
                            spacing 15
                            xalign 0.5

                            textbutton "|<<":
                                style "music_control_button"
                                action Function(play_previous_track)

                            # Icon flips between pause "||" and play ">".
                            $ _play_label = "||" if is_playing else ">"
                            textbutton _play_label:
                                style "music_play_button"
                                action Function(toggle_playback)

                            textbutton ">>|":
                                style "music_control_button"
                                action Function(play_next_track)

                        # Mode toggles: shuffle + repeat mode.
                        hbox:
                            spacing 10
                            xalign 0.5

                            textbutton "SHUFFLE":
                                style "music_toggle_button"
                                selected shuffle_on
                                action Function(toggle_shuffle)

                            textbutton play_mode_label():
                                style "music_toggle_button"
                                action Function(cycle_play_mode)

                        # Output level. This is the one room in the game you sit
                        # in to LISTEN, so the music mixer belongs on the deck
                        # rather than four clicks away in Settings -- and it is
                        # the same persistent preference, so a level set here is
                        # the level the rest of the game plays at.
                        hbox:
                            spacing 10
                            xalign 0.5
                            ysize 24

                            add Solid("#56d7ff") xysize (3, 16) yalign 0.5
                            text "VOL" style "music_volume_label" yalign 0.5

                            bar:
                                value Preference("music volume")
                                style "music_volume_slider"
                                yalign 0.5

                            text "[_mvol]%" style "music_volume_pct" yalign 0.5

    # Console brackets framing the shell (cohesion with the archive hub).
    use archive_shell_brackets()

# =============================================================================
# STYLES
# =============================================================================
# Styles
style music_room_frame:
    xalign 0.5
    yalign 0.5
    xsize 950
    ysize 620
    background Solid("#050811e8")
    padding (25, 18)

style music_room_title:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 34
    color "#f4fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]


style music_list_frame:
    xsize 560
    ysize 540
    background Solid("#07101add")
    padding (10, 10)

style music_list_header:
    font gui.interface_font
    size 20
    color "#f4fbff"
    xalign 0.5
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style music_track_button:
    xsize 510
    ysize 52
    background Solid("#07111dcc")
    hover_background Solid("#12314aee")
    insensitive_background Solid("#050811cc")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (10, 8)

style music_track_number:
    font gui.interface_font
    color "#56d7ff"
    size 18
    bold True
    outlines [(1, "#02040b", 0, 0)]

style music_track_title:
    font gui.interface_font
    color "#dff8ff"
    size 17
    bold True
    outlines [(1, "#02040b", 0, 0)]

style music_track_artist:
    font gui.interface_font
    color "#9fc9d6"
    size 13
    outlines [(1, "#02040b", 0, 0)]

# Unheard rows: same geometry, drained of colour. Matching the archive's other
# locked states (#4f5b67 pips, #687787 "???") keeps one vocabulary across the hub.
style music_track_number_locked is music_track_number:
    color "#4f5b67"

style music_track_title_locked is music_track_title:
    color "#687787"

style music_track_artist_locked is music_track_artist:
    color "#4f5b67"

style music_player_frame:
    xsize 440
    ysize 540
    background Solid("#07101add")
    padding (10, 10)

style music_player_header:
    font gui.interface_font
    size 20
    color "#f4fbff"
    xalign 0.5
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style music_visualizer:
    font gui.interface_font
    size 90
    color "#56d7ff"
    xalign 0.5
    yalign 0.5
    outlines [(2, "#02040b", 0, 0)]

style music_no_track:
    font gui.interface_font
    size 20
    color "#687787"
    xalign 0.5
    yalign 0.5
    outlines [(1, "#02040b", 0, 0)]

style music_now_playing_title:
    font gui.interface_font
    size 20
    color "#dff8ff"
    xalign 0.5
    text_align 0.5
    bold True
    outlines [(1, "#02040b", 0, 0)]

style music_now_playing_artist:
    font gui.interface_font
    size 16
    color "#9fc9d6"
    xalign 0.5
    text_align 0.5
    outlines [(1, "#02040b", 0, 0)]

style music_time:
    font gui.interface_font
    size 14
    color "#9fc9d6"
    outlines [(1, "#02040b", 0, 0)]

style music_control_button:
    xysize (55, 55)
    background Solid("#07111dcc")
    hover_background Solid("#12314af2")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (8, 8)

style music_control_button_text:
    font gui.interface_font
    size 22
    color "#dff8ff"
    xalign 0.5
    yalign 0.5
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style music_play_button is music_control_button:
    xysize (65, 55)

# The volume strip. slider_slider is the same base the Settings screen and the
# Matsuda pause menu use, so the drag feel (and the log scale) is identical
# everywhere; only the width and the palette change.
style music_volume_label:
    font gui.interface_font
    size 13
    color "#56d7ff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style music_volume_pct:
    font gui.interface_font
    size 13
    color "#9fc9d6"
    xsize 42
    text_align 1.0
    outlines [(1, "#02040b", 0, 0)]

style music_volume_slider is slider_slider:
    xsize 250
    ysize 10
    base_bar Solid("#102338")
    thumb Solid("#56d7ff")

style music_play_button_text is music_control_button_text:
    size 24

# --- New chrome: result count, search box, mode toggles ----------------------
style music_list_count:
    font gui.interface_font
    size 13
    color "#7fcfe0"
    kerning 1.0
    outlines [(1, "#02040b", 0, 0)]

style music_search_label:
    font gui.interface_font
    size 13
    color "#56d7ff"
    bold True
    kerning 1.0
    outlines [(1, "#02040b", 0, 0)]

style music_search_hint:
    font gui.interface_font
    size 15
    color "#4f6472"
    italic True
    outlines [(1, "#02040b", 0, 0)]

style music_search_input:
    font gui.interface_font
    size 15
    color "#eaffff"
    outlines [(1, "#02040b", 0, 0)]

style music_clear_button:
    background Solid("#07111dcc")
    hover_background Solid("#12314af2")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (8, 4)

style music_clear_button_text:
    font gui.interface_font
    size 12
    color "#9fc9d6"
    hover_color "#ffffff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style music_toggle_button:
    xysize (152, 34)
    background Solid("#07111dcc")
    hover_background Solid("#12314af2")
    selected_background Solid("#1c4a68f2")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (10, 6)

style music_toggle_button_text:
    font gui.interface_font
    size 14
    color "#8fb6c5"
    hover_color "#ffffff"
    selected_color "#eaffff"
    xalign 0.5
    yalign 0.5
    text_align 0.5
    bold True
    outlines [(1, "#02040b", 0, 0)]
