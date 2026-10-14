# Archive soundtrack player: a now-playing deck beside the library, with
# favourites and a play queue. music_scan_now_playing() observes
# MUSIC_ROOM_LISTEN_CHANNELS at interaction boundaries; heard tracks unlock by
# persistent key. The Archive music module itself uses
# persistent.archive_unlocked_music. Locked tracks are skipped by playback
# controls. Repeat mode governs explicit loops versus poller advancement.
# leave_music_room() restores Archive music. Existing legacy_file_path values are
# stable unlock IDs and must survive asset moves, even when no file exists there.

init python:
    # Channels a track can be HEARD on. Any of these playing a file in the
    # library counts as the player having encountered that track -- def_audio.rpy
    # registers track1..track4 as extra music channels for the fights and the
    # arcade modes, so watching "music" alone would leave half the soundtrack
    # permanently unrecoverable.
    MUSIC_ROOM_LISTEN_CHANNELS = ("music", "track1", "track2", "track3", "track4")

    def music_key_from_path(file_path):
        """Map assets/audio/bgm/13am.ogg to music_heard_assets_audio_bgm_13am.

        Existing tracks pass legacy paths to retain their established unlock IDs.
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

    # Display credits use romanized names supported by gui.interface_font.

    # One soundtrack entry. A track is locked until the player has actually heard
    # it somewhere in the game (see music_scan_now_playing below); the room as a
    # whole is gated upstream by persistent.archive_unlocked_music.
    class MusicTrack:
        def __init__(self, title, artist, file_path, legacy_file_path=None):
            self.title = title
            self.artist = artist
            self.file_path = file_path
            # A legacy path preserves unlock identity across physical asset moves.
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
                audio.archive,
                "assets/audio/bgm/archive.ogg"
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
                "Crying Over You",
                "Christopher Morrow",
                audio.day_a,
                "assets/audio/bgm/day_a.ogg"
            ),
            MusicTrack(
                "The 4 PM Walk Philosophy",
                "Nekoto",
                audio.night_a,
                "assets/audio/bgm/night_a.ogg"
            ),
            MusicTrack(
                "Sometimes",
                "KHAIM",
                audio.house_day_a,
                "assets/audio/bgm/house_day_a.ogg"
            ),
            MusicTrack(
                "Slow life continues",
                "junichirou",
                audio.day_c,
                "assets/audio/bgm/daily.ogg"
            ),
            MusicTrack(
                "As Time Carries Us Away",
                "Yosuke Matsuura",
                audio.night_b,
                "assets/audio/bgm/night_b.ogg"
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
            # NUDGE P3/P5: "Safety" (here) ships with "--" as the artist. Find the credit, or decide whether unattributed tracks ship.
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
            # Artist attribution remains unknown; keep the playable track listed.
            MusicTrack(
                "Quiz",
                "Toby Fox",
                audio.exam,
                "assets/audio/bgm/exam.ogg"
            ),
            MusicTrack(
                "Chasing the Summer",
                "shinsanworks",
                audio.school_day_a,
                "assets/audio/bgm/school_day_a.ogg"
            ),
            MusicTrack(
                "A Quiet Place Among Strangers",
                "Yosuke Matsuura",
                audio.theme_matsuda_a,
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
                audio.ch4_night,
                "assets/audio/bgm/ch4_night.ogg"
            ),
            MusicTrack(
                "Samsara",
                "Nihilore",
                audio.ch4_serious,
                "assets/audio/bgm/ch4_serious.ogg"
            ),
            MusicTrack(
                "Emotions",
                "Falling Forever",
                audio.ch4_day,
                "assets/audio/bgm/ch4_day.ogg"
            ),
            MusicTrack(
                "Kingdom of Quiet Clouds",
                "Yosuke Matsuura",
                audio.ch5_day,
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
            MusicTrack(
                "Killing Time",
                "Kevin MacLeod",
                audio.day_b,
                "assets/audio/bgm/day_b.ogg"
            ),
            MusicTrack(
                "Meatball Parade",
                "Kevin MacLeod",
                audio.meatballparade,
                "assets/audio/bgm/meatballparade.ogg"
            ),
            MusicTrack(
                "you know what",
                "Edamame88",
                audio.club_b,
                "assets/audio/bgm/club_b.ogg"
            ),
            MusicTrack(
                "Scorching Eurobeat",
                "Maniira",
                audio.scorchingeurobeat,
                "assets/audio/bgm/scorchingeurobeat.ogg"
            ),
            MusicTrack(
                "Friends",
                "Toby Fox",
                audio.tendermoment,
                "assets/audio/bgm/tendermoment.ogg"
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

    # Repeat mode, kept between visits in persistent.music_play_mode:
    #   REPEAT_ALL -> the list wraps around
    #   REPEAT_ONE -> loop the current track forever
    #   NO_REPEAT  -> play to the end of the list, then stop
    MODE_REPEAT_ALL = 0
    MODE_REPEAT_ONE = 1
    MODE_NO_REPEAT = 2

    # PLAY ORDER. The queue plays first. Then the list the player last started a
    # track from (music_context: "all" heard tracks, or "fav") carries on after
    # _music_anchor -- in order, or from a shuffled deck dealt up front so Up Next
    # can show the real order. Shuffle's Previous walks _music_history back and
    # puts the track it leaves on top of the deck, so Next returns to it.
    music_queue = []
    music_context = "all"
    _music_anchor = None
    _music_deck = []
    _music_history = []
    _music_from_queue = False

    # Where a drag on the scrubber sits; None when nobody is dragging.
    _music_scrub = None

    # A seek (or a loop-flag change) made while paused waits here for resume:
    # a re-issued file always starts playing, whatever the channel's pause flag.
    _music_resume_at = None

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

    def music_repeat_tip():
        return {
            MODE_REPEAT_ALL: "Repeat: all",
            MODE_REPEAT_ONE: "Repeat: one",
            MODE_NO_REPEAT: "Repeat: off",
        }.get(persistent.music_play_mode, "Repeat: all")

    def music_source_label():
        """The readout's right-hand line: where the current track came from."""
        if current_track is None:
            return "IDLE"
        if _music_from_queue:
            return "PLAYING FROM QUEUE"
        return "PLAYING FROM FAVORITES" if music_context == "fav" else "PLAYING FROM ALL TRACKS"

    def music_is_favorite(track):
        return track.persistent_key in persistent.music_favorites

    def music_toggle_favorite(track):
        # Reassigned rather than mutated in place: only a setattr stamps
        # persistent's change time, which decides the winner when the save
        # locations are merged at load.
        persistent.music_favorites = set(persistent.music_favorites) ^ {track.persistent_key}

    def music_pool():
        """The list auto-advance plays through."""
        tracks = music_unlocked_tracks()
        if music_context == "fav":
            return [t for t in tracks if music_is_favorite(t)]
        return tracks

    def _music_reshuffle():
        """Deal a fresh shuffled deck of the pool, minus what is playing."""
        global _music_deck
        import random
        _music_deck = [t for t in music_pool() if t is not current_track]
        random.shuffle(_music_deck)

    def _music_repeats():
        return persistent.music_play_mode != MODE_NO_REPEAT

    def _music_list_after(wrap):
        """The pool after the anchor, in order; wrapped round when `wrap`."""
        pool = music_pool()
        anchor = _music_anchor if _music_anchor in pool else current_track
        i = pool.index(anchor) + 1 if anchor in pool else 0
        return pool[i:] + (pool[:i] if wrap else [])

    def music_list_next(limit):
        """What the list plays after the current track. The queue comes first."""
        if persistent.music_shuffle:
            pool = music_pool()
            rest = [t for t in _music_deck if t in pool]
        else:
            rest = [t for t in _music_list_after(_music_repeats()) if t is not current_track]
        return rest[:limit]

    def _music_take_next(auto):
        """Consume whatever plays next: (track, from_list), or (None, False) at
        the end of a list that does not repeat. A manual skip always wraps."""
        global _music_deck
        if music_queue:
            return music_queue.pop(0), False
        pool = music_pool()
        if not pool:
            return None, False
        wrap = not auto or _music_repeats()
        if persistent.music_shuffle:
            _music_deck = [t for t in _music_deck if t in pool]
            if not _music_deck:
                if not wrap:
                    return None, False
                _music_reshuffle()
            # An empty deck here means the pool is just the current track.
            return (_music_deck.pop(0) if _music_deck else pool[0]), True
        rest = _music_list_after(wrap)
        return (rest[0] if rest else None), True

    def _loop_current():
        """Should the currently-issued file be told to loop forever?"""
        return persistent.music_play_mode == MODE_REPEAT_ONE

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

    def start_track(track, from_list=True, remember=True):
        """Begin playback of `track`. A queued track (from_list=False) leaves the
        list's place alone. Previous passes remember=False so stepping back does
        not push onto the history it is popping."""
        global current_track, is_playing, music_current_cg, _seen_playing
        global _music_anchor, _music_from_queue, _music_resume_at
        if track is None:
            return
        _music_resume_at = None
        if track is not current_track:
            if remember and current_track is not None:
                _music_history.append(current_track)
                del _music_history[:-100]
            # New art per track; a restart or a seek keeps what is up.
            music_current_cg = pick_random_cg()
        if from_list:
            _music_anchor = track
        _music_from_queue = not from_list
        if track in _music_deck:
            _music_deck.remove(track)
        current_track = track
        is_playing = True
        _seen_playing = False
        # The pause flag lives on the channel, not the file: clear it, or a track
        # picked while paused would start silent.
        renpy.music.set_pause(False, channel="music")
        _play_current_file()
        renpy.restart_interaction()

    def play_next_track(auto=False):
        """Skip ahead. Only an automatic advance at the end of a list that does
        not repeat stops the deck."""
        global is_playing
        track, from_list = _music_take_next(auto)
        if track is None:
            is_playing = False
            renpy.music.stop(channel="music")
            renpy.restart_interaction()
            return
        start_track(track, from_list)

    def play_previous_track():
        """Back a track. Like most players, if we're a few seconds into the
        current track, restart it instead. Otherwise shuffle walks back through
        what actually played, and the list steps up one."""
        if current_track is not None and music_pos_duration()[0] > 3.0:
            start_track(current_track)
            return
        if persistent.music_shuffle:
            if _music_history:
                if current_track is not None:
                    _music_deck.insert(0, current_track)
                start_track(_music_history.pop(), remember=False)
            else:
                start_track(current_track)
            return
        pool = music_pool()
        if pool:
            i = pool.index(current_track) if current_track in pool else 0
            start_track(pool[(i - 1) % len(pool)])

    def music_play_from(track, context):
        """A library row: play `track` and carry on through the list it is in."""
        global music_context
        music_context = context
        _music_reshuffle()
        start_track(track)

    def music_play_queued(i):
        start_track(music_queue.pop(i), from_list=False)

    def music_unqueue(i):
        del music_queue[i]

    def music_toggle_queued(track):
        if track in music_queue:
            music_queue.remove(track)
        else:
            music_queue.append(track)

    def toggle_playback():
        """Play/pause. Uses real channel pause so the position is preserved."""
        global is_playing, _seen_playing, _music_resume_at
        if current_track is None:
            play_next_track()
            return
        if is_playing:
            is_playing = False
            renpy.music.set_pause(True, channel="music")
            renpy.restart_interaction()
        elif renpy.music.get_playing(channel="music") is not None:
            # Paused mid-track -> resume, from a spot picked while paused if any.
            is_playing = True
            renpy.music.set_pause(False, channel="music")
            if _music_resume_at is not None:
                _seen_playing = False
                _play_current_file(_music_resume_at)
                _music_resume_at = None
            renpy.restart_interaction()
        else:
            # Ended or stopped -> replay from the top.
            start_track(current_track)

    def toggle_shuffle():
        persistent.music_shuffle = not persistent.music_shuffle
        _music_reshuffle()

    def cycle_play_mode():
        """Rotate REPEAT ALL -> REPEAT ONE -> OFF. Only REPEAT ONE changes the
        file's loop flag, so only entering or leaving it re-issues the track
        from its current position (on resume, if paused)."""
        global _seen_playing, _music_resume_at
        was_looping = _loop_current()
        persistent.music_play_mode = (persistent.music_play_mode + 1) % 3
        if _loop_current() != was_looping and renpy.music.get_playing(channel="music") is not None:
            pos = music_pos_duration()[0]
            if is_playing:
                _seen_playing = False
                _play_current_file(pos)
            else:
                _music_resume_at = pos

    def music_seek(pos):
        """Move the playhead. Paused, the spot is held for resume."""
        global is_playing, _seen_playing, _music_resume_at
        if current_track is None:
            return
        playing = renpy.music.get_playing(channel="music")
        if playing is not None and not is_playing:
            _music_resume_at = pos
            return
        if playing is None:
            # The track had ended: seeking into it plays it again.
            is_playing = True
            renpy.music.set_pause(False, channel="music")
        _seen_playing = False
        _play_current_file(pos)

    def music_seek_preview(value):
        global _music_scrub
        _music_scrub = value

    def music_seek_commit():
        global _music_scrub
        pos, _music_scrub = _music_scrub, None
        if pos is not None:
            music_seek(pos)

    def music_pos_duration():
        pos = _music_resume_at
        if pos is None:
            pos = renpy.music.get_pos(channel="music") or 0.0
        duration = renpy.music.get_duration(channel="music") or 0.0
        return pos, duration

    class MusicSeekValue(BarValue):
        """The scrubber: follows the playhead; a drag only previews, and the
        release seeks (music_seek_commit). Every instance compares equal, so a
        screen update reuses the live bar instead of swapping it mid-drag."""

        def __init__(self):
            self.adjustment = None

        def __eq__(self, other):
            return type(other) is type(self)

        def __ne__(self, other):
            return not self.__eq__(other)

        def __hash__(self):
            return hash(type(self))

        def get_adjustment(self):
            pos, duration = music_pos_duration()
            self.adjustment = ui.adjustment(value=pos, range=max(duration, 1.0), step=5.0,
                adjustable=True, changed=music_seek_preview)
            return self.adjustment

        def periodic(self, st):
            if _music_scrub is None:
                pos, duration = music_pos_duration()
                # Assigned, not change()d: change() would call music_seek_preview.
                self.adjustment.range = max(duration, 1.0)
                self.adjustment.value = pos
                self.adjustment.update()
            return 0.1

    def music_poll_playback():
        """Screen timer: when the current track has finished, advance per the
        play order. REPEAT ONE loops in the mixer, so it never finishes. Runs
        without a screen update; start_track restarts the interaction itself."""
        global _seen_playing
        if not is_playing or current_track is None or _loop_current():
            return
        if renpy.music.get_playing(channel="music") is not None:
            _seen_playing = True
        elif _seen_playing:
            _seen_playing = False
            play_next_track(auto=True)

    def music_room_open():
        """Stop the Archive BGM (the deck plays its own) and deal the shuffle."""
        renpy.music.stop(channel="music")
        _music_reshuffle()

    def leave_music_room():
        """Clean exit: stop playback, restore archive BGM, hide screen."""
        # Critical so the Archive isn't left silent after the room closes.
        global current_track, is_playing, _seen_playing, _music_anchor, music_context
        global _music_scrub, _music_resume_at
        is_playing = False
        current_track = None
        _seen_playing = False
        _music_anchor = None
        _music_scrub = None
        _music_resume_at = None
        music_context = "all"
        del music_queue[:]
        del _music_history[:]
        # A pause would outlive the room on the channel and mute the Archive.
        renpy.music.set_pause(False, channel="music")
        renpy.music.play(audio.archive, channel="music")
        # Favourites, shuffle and repeat: written once per visit, not per click.
        renpy.save_persistent()
        renpy.hide_screen("music_room")

    # The two callbacks below feed DynamicDisplayable widgets that re-evaluate on
    # a timer (the second tuple element is the redraw delay in seconds): current
    # position polls ~10x/sec, total duration ~1x/sec. A drag on the scrubber
    # shows where the release will land.
    def music_time_current(st, at):
        """DynamicDisplayable callback for current position."""
        pos = _music_scrub if _music_scrub is not None else music_pos_duration()[0]
        return Text(format_time(pos), style="music_time"), 0.1

    def music_time_total(st, at):
        """DynamicDisplayable callback for total duration."""
        return Text(format_time(music_pos_duration()[1]), style="music_time"), 1.0

    # Built once so a screen update reuses them rather than restarting them.
    MUSIC_TIME_NOW = DynamicDisplayable(music_time_current)
    MUSIC_TIME_TOTAL = DynamicDisplayable(music_time_total)

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

    # --- Art -------------------------------------------------------------------
    # CGs are all 1280x720, so the sleeve is the centre square of one, and the
    # deck's backdrop is the same CG blurred once on the CPU at thumbnail size
    # (cached like any image) and cropped to the 470x540 card.
    def music_cover(cg):
        key = ("cover", cg)
        rv = _music_disp.get(key)
        if rv is None:
            rv = _music_disp[key] = Transform(cg, crop=(0.21875, 0.0, 0.5625, 1.0),
                crop_relative=True, xysize=(216, 216))
        return rv

    def music_ambient(cg):
        key = ("ambient", cg)
        rv = _music_disp.get(key)
        if rv is None:
            rv = _music_disp[key] = Transform(im.Blur(im.Scale(cg, 128, 72), 2.5),
                crop=(0.2552, 0.0, 0.4896, 1.0), crop_relative=True, xysize=(470, 540))
        return rv

    # The record behind the sleeve turns at 33 1/3 rpm while the deck plays and
    # holds its angle through a pause (an ATL spin would snap back to zero).
    _music_spin = [0.0, None]

    def music_vinyl_spin(trans, st, at):
        last = _music_spin[1]
        if is_playing and last is not None and st > last:
            _music_spin[0] = (_music_spin[0] + (st - last) * 200.0) % 360.0
        _music_spin[1] = st
        trans.rotate = _music_spin[0]
        return 0 if is_playing else 0.25

    MUSIC_VINYL = Transform(MUSIC_ART + "vinyl.svg", function=music_vinyl_spin,
        rotate_pad=False, subpixel=True)

# Icon and fill helpers run before the styles below are built.
init -2 python:
    MUSIC_ART = "assets/gui/music_room/"
    MUSIC_ACCENT = "#56d7ff"
    MUSIC_HEART = "#ff7aa8"
    _music_disp = {}

    def music_icon(name, color, size=None):
        """A tinted icon from the room's SVG set. One object per argument tuple,
        so a screen update reuses the node instead of rebuilding it."""
        key = (name, color, size)
        rv = _music_disp.get(key)
        if rv is None:
            rv = _music_disp[key] = Transform(MUSIC_ART + name + ".svg",
                matrixcolor=TintMatrix(color), xysize=(size, size) if size else None)
        return rv

    def music_round(color, alpha=1.0):
        """A rounded-corner fill that stretches to any box (rows, tabs, tips)."""
        return Transform(Frame(MUSIC_ART + "round.svg", 8, 8),
            matrixcolor=TintMatrix(color), alpha=alpha)

    def music_bar(color):
        """A 4 px rounded track, centred in a 16 px tall bar."""
        return Transform(Frame(MUSIC_ART + "track.svg", 3, 6, 3, 6),
            matrixcolor=TintMatrix(color))

# Favourites hold persistent_keys, so they survive asset moves like unlocks do.
default persistent.music_favorites = set()
default persistent.music_play_mode = 0
default persistent.music_shuffle = False

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

# The record slides out from behind the sleeve while the deck plays and back in
# when it stops. A changed `out` rebuilds this, and it eases from where it was.
transform music_vinyl_slide(out):
    subpixel True
    anchor (0.5, 0.5)
    pos (191, 156)
    ease 0.6 xoffset (88 if out else 0)

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

# One track row. `kind` picks the side buttons: "lib" (favourite + queue),
# "queue" (remove entry `qi`) or "next" (none -- Up Next is read-only order).
screen music_row(num, track, play_action, kind="lib", qi=None):
    $ _active = track is current_track
    $ _ok = track.is_unlocked

    fixed:
        xysize (626, 50)

        button:
            style "music_row_button"
            selected _active
            sensitive _ok
            action play_action

            # Index column doubles as the now-playing indicator.
            if _active:
                fixed:
                    xysize (20, 20)
                    xpos 14
                    ycenter 25
                    use music_eq(is_playing)
            else:
                text str(num):
                    style ("music_track_number" if _ok else "music_track_number_locked")
                    xcenter 24
                    ycenter 25

            vbox:
                xpos 50
                ycenter 25
                xmaximum 480

                # An unheard track keeps its SLOT and its number -- the player
                # can see how much of the soundtrack is still out there, and
                # where -- but not its title, which for a score is half the
                # spoiler.
                if _ok:
                    text track.title style "music_track_title"
                    text track.artist style "music_track_artist"
                else:
                    text "???" style "music_track_title_locked"
                    text "NOT YET HEARD" style "music_track_artist_locked"

        if kind == "queue":
            imagebutton:
                style "music_icon_button"
                xcenter 602
                ycenter 25
                idle music_icon("remove", "#6f8898")
                hover music_icon("remove", "#ffffff")
                action Function(music_unqueue, qi)
                alt "Remove from queue"
        elif kind == "lib" and _ok:
            $ _f = music_is_favorite(track)
            $ _inq = track in music_queue
            imagebutton:
                style "music_icon_button"
                xcenter 564
                ycenter 25
                idle music_icon("heart_fill" if _f else "heart", MUSIC_HEART if _f else "#56697a")
                hover music_icon("heart_fill" if _f else "heart", MUSIC_HEART if _f else "#ffffff")
                action Function(music_toggle_favorite, track)
                alt ("Remove from favorites" if _f else "Add to favorites")
            imagebutton:
                style "music_icon_button"
                xcenter 602
                ycenter 25
                idle music_icon("queue_done" if _inq else "queue_add", MUSIC_ACCENT if _inq else "#56697a")
                hover music_icon("queue_done" if _inq else "queue_add", "#ffffff")
                action Function(music_toggle_queued, track)
                alt ("Remove from queue" if _inq else "Add to queue")

# =============================================================================
# MUSIC ROOM SCREEN
# Layout: header, readout, then [now-playing deck | library with tabs].
# =============================================================================
screen music_room():
    modal True

    # Search query for the library filter, and the library tab: "all", "fav"
    # or "queue".
    default query = ""
    default tab = "all"

    # The list's scroll. A viewport carries its pan over from the one it
    # replaces, so a tab switch puts this back to the top by hand.
    default list_y = ui.adjustment()

    on "show" action Function(music_room_open)

    use archive_backdrop

    # ESC / header Return both go through leave_music_room() to restore BGM.
    key "game_menu" action [Function(leave_music_room), With(enter_m_menu_doorway)]
    key "K_ESCAPE" action [Function(leave_music_room), With(enter_m_menu_doorway)]

    # Hardware media keys drive the deck, like any desktop player.
    key "K_AUDIOPLAY" action Function(toggle_playback)
    key "K_AUDIONEXT" action Function(play_next_track)
    key "K_AUDIOPREV" action Function(play_previous_track)

    # Auto-advance driver. A tick that finds nothing to do must not re-run this
    # screen, so it skips the screen update; start_track restarts on a hand-off.
    timer 0.5 action Function(music_poll_playback, _update_screens=False) repeat True

    # A SEARCH ONLY EVER MATCHES RECOVERED TRACKS. Locked rows show "???" rather
    # than their title, so letting the filter read the real title would hand the
    # player a way to confirm a track exists -- and its name -- by typing at it.
    # With a query live the locked rows simply drop out; with no query they stay
    # in place, because the gaps in the list are the point.
    python:
        _found = music_unlocked_tracks()
        _favs = [t for t in _found if music_is_favorite(t)]
        _q = query.strip().lower()
        _rows = list(enumerate(_favs if tab == "fav" else music_library, 1))
        if _q:
            _rows = [(n, t) for n, t in _rows if t.is_unlocked and (_q in t.title.lower() or _q in t.artist.lower())]
        _up = (music_queue + music_list_next(1))[:1]
        _num = music_library.index(current_track) + 1 if current_track in music_library else 0
        _fav = current_track is not None and music_is_favorite(current_track)
        _shuf = persistent.music_shuffle
        _mode = persistent.music_play_mode
        _muted = preferences.get_mute("music")
        _mvol = music_volume_pct()
        _tip = GetTooltip()

    frame:
        style "archive_shell_frame"
        at archive_frame_enter(40, 0.4)

        vbox:
            spacing 12

            use archive_header("MUSIC ROOM", [Function(leave_music_room), With(enter_m_menu_doorway)])

            use archive_readout(
                "SOUNDTRACK // {}/{} TRACKS RECOVERED".format(len(_found), len(music_library)),
                music_source_label())

            hbox:
                spacing 18
                xalign 0.5

                # --- LEFT: the deck -----------------------------------------
                fixed:
                    xysize (470, 540)
                    at music_panel_left

                    # The current CG twice: blurred behind everything, and as
                    # the sleeve. A random unlocked one per track.
                    if music_current_cg:
                        add music_ambient(music_current_cg)
                    else:
                        add Solid("#0b1622")
                    add MUSIC_ART + "scrim.svg"
                    add Solid("#56d7ff44") xysize (470, 1)
                    add Solid("#56d7ff44") xysize (470, 1) ypos 539

                    hbox:
                        xpos 24
                        ypos 16
                        spacing 10
                        use music_eq(is_playing)
                        text "NOW PLAYING" style "music_deck_label" yalign 0.5

                    if _num:
                        text "TRACK {:02d}".format(_num) style "music_deck_meta" xanchor 1.0 xpos 446 ypos 19

                    add MUSIC_VINYL at music_vinyl_slide(is_playing)
                    add MUSIC_ART + "cover_shadow.png" xpos 63 ypos 34
                    if music_current_cg:
                        add music_cover(music_current_cg) xpos 83 ypos 48
                    else:
                        add Solid("#0f1d2a") xysize (216, 216) xpos 83 ypos 48
                        add music_icon("note", "#3c5566") xcenter 191 ycenter 156
                    add Solid("#ffffff1f") xysize (216, 1) xpos 83 ypos 48

                    # Anchored to the bottom, so a title that wraps grows up
                    # into the gap under the sleeve instead of off the card.
                    vbox:
                        xpos 24
                        yanchor 1.0
                        ypos 522

                        fixed:
                            xsize 422
                            yfit True

                            vbox:
                                xmaximum 364
                                spacing 2
                                if current_track:
                                    # Long titles drop a size so most stay on one line.
                                    text current_track.title:
                                        style "music_deck_title"
                                        size (26 if len(current_track.title) <= 24 else 21)
                                    text current_track.artist style "music_deck_artist"
                                else:
                                    text "Nothing playing" style "music_deck_title"
                                    text "Pick a track to start the deck" style "music_deck_artist"

                            if current_track:
                                imagebutton:
                                    style "music_icon_button"
                                    xanchor 1.0
                                    xpos 428
                                    ypos -2
                                    idle music_icon("heart_fill" if _fav else "heart", MUSIC_HEART if _fav else "#9fb4c2")
                                    hover music_icon("heart_fill" if _fav else "heart", MUSIC_HEART if _fav else "#ffffff")
                                    action Function(music_toggle_favorite, current_track)
                                    tooltip ("Remove from favorites" if _fav else "Add to favorites")
                                    alt ("Remove from favorites" if _fav else "Add to favorites")

                        null height 16

                        # Click or drag to seek; the release commits.
                        bar:
                            style "music_seek_bar"
                            value MusicSeekValue()
                            released Function(music_seek_commit)

                        fixed:
                            xsize 422
                            ysize 20
                            add MUSIC_TIME_NOW ypos 3
                            add MUSIC_TIME_TOTAL xanchor 1.0 xpos 422 ypos 3

                        null height 4

                        # Transport: shuffle, previous, play/pause, next, repeat.
                        fixed:
                            xsize 422
                            ysize 72

                            imagebutton:
                                style "music_icon_button"
                                xcenter 47
                                ycenter 36
                                idle music_icon("shuffle", MUSIC_ACCENT if _shuf else "#8aa3b2")
                                hover music_icon("shuffle", "#ffffff")
                                action Function(toggle_shuffle)
                                tooltip ("Shuffle: on" if _shuf else "Shuffle: off")
                                alt ("Shuffle: on" if _shuf else "Shuffle: off")
                            if _shuf:
                                add Solid(MUSIC_ACCENT) xysize (4, 4) xcenter 47 ycenter 60

                            imagebutton:
                                style "music_transport_button"
                                xcenter 129
                                ycenter 36
                                idle music_icon("prev", "#dbe9f1")
                                hover music_icon("prev", MUSIC_ACCENT)
                                action Function(play_previous_track)
                                tooltip "Previous"
                                alt "Previous"

                            button:
                                style "music_play_button"
                                xcenter 211
                                ycenter 36
                                action Function(toggle_playback)
                                tooltip ("Pause" if is_playing else "Play")
                                alt ("Pause" if is_playing else "Play")
                                add music_icon("pause" if is_playing else "play", "#04121a"):
                                    align (0.5, 0.5)
                                    xoffset (0 if is_playing else 2)

                            imagebutton:
                                style "music_transport_button"
                                xcenter 293
                                ycenter 36
                                idle music_icon("next", "#dbe9f1")
                                hover music_icon("next", MUSIC_ACCENT)
                                action Function(play_next_track)
                                tooltip "Next"
                                alt "Next"

                            $ _rep = "repeat_one" if _mode == MODE_REPEAT_ONE else "repeat"
                            imagebutton:
                                style "music_icon_button"
                                xcenter 375
                                ycenter 36
                                idle music_icon(_rep, "#8aa3b2" if _mode == MODE_NO_REPEAT else MUSIC_ACCENT)
                                hover music_icon(_rep, "#ffffff")
                                action Function(cycle_play_mode)
                                tooltip music_repeat_tip()
                                alt music_repeat_tip()
                            if _mode != MODE_NO_REPEAT:
                                add Solid(MUSIC_ACCENT) xysize (4, 4) xcenter 375 ycenter 60

                        null height 4

                        # Output level. This is the one room in the game you sit
                        # in to LISTEN, so the music mixer belongs on the deck
                        # rather than four clicks away in Settings -- and it is
                        # the same persistent preference, so a level set here is
                        # the level the rest of the game plays at.
                        fixed:
                            xsize 422
                            ysize 30

                            imagebutton:
                                style "music_icon_button"
                                xpos -6
                                ycenter 15
                                idle music_icon("mute" if _muted else "volume", "#8aa3b2")
                                hover music_icon("mute" if _muted else "volume", "#ffffff")
                                action Preference("music mute", "toggle")
                                tooltip ("Unmute" if _muted else "Mute")
                                alt ("Unmute" if _muted else "Mute")

                            bar:
                                style "music_volume_bar"
                                value Preference("music volume")
                                xpos 40
                                ycenter 15

                            text ("MUTED" if _muted else "{}%".format(_mvol)):
                                style "music_volume_pct"
                                xanchor 1.0
                                xpos 422
                                ycenter 15

                # --- RIGHT: the library -------------------------------------
                frame:
                    style "music_list_frame"
                    at music_panel_right

                    vbox:
                        spacing 8

                        # Tabs, and the search box for the two track lists.
                        fixed:
                            xsize 644
                            ysize 38

                            hbox:
                                spacing 6
                                ycenter 19

                                textbutton "ALL TRACKS  {}".format(len(_found)):
                                    style "music_tab_button"
                                    selected tab == "all"
                                    action [SetScreenVariable("tab", "all"), Function(list_y.change, 0)]
                                textbutton "FAVORITES  {}".format(len(_favs)):
                                    style "music_tab_button"
                                    selected tab == "fav"
                                    action [SetScreenVariable("tab", "fav"), Function(list_y.change, 0)]
                                textbutton "QUEUE  {}".format(len(music_queue)):
                                    style "music_tab_button"
                                    selected tab == "queue"
                                    action [SetScreenVariable("tab", "queue"), Function(list_y.change, 0)]

                            if tab != "queue":
                                frame:
                                    style "music_search_frame"
                                    xanchor 1.0
                                    xpos 644
                                    ycenter 19

                                    hbox:
                                        spacing 8
                                        add music_icon("search", "#6f8898") yalign 0.5

                                        fixed:
                                            xysize (150, 22)
                                            yalign 0.5

                                            if query == "":
                                                text "Search" style "music_search_hint" yalign 0.5
                                            input:
                                                value ScreenVariableInputValue("query")
                                                style "music_search_input"
                                                yalign 0.5
                                                copypaste True
                                                pixel_width 150

                                        if query:
                                            imagebutton:
                                                style "music_clear_button"
                                                yalign 0.5
                                                idle music_icon("remove", "#6f8898", 16)
                                                hover music_icon("remove", "#ffffff", 16)
                                                action SetScreenVariable("query", "")
                                                alt "Clear search"

                        viewport:
                            style_prefix "archive_sv"
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            pagekeys True
                            xsize 644
                            ysize 426
                            yadjustment list_y

                            vbox:
                                spacing 4
                                xsize 626

                                if tab == "queue":
                                    $ _later = music_list_next(30)

                                    if music_queue:
                                        fixed:
                                            xsize 626
                                            ysize 30
                                            text "NEXT IN QUEUE" style "music_section_text" ypos 9
                                            textbutton "CLEAR":
                                                style "music_small_button"
                                                xanchor 1.0
                                                xpos 626
                                                ypos 2
                                                action Function(music_queue.clear)
                                        for _i, _t in enumerate(music_queue):
                                            use music_row(_i + 1, _t, Function(music_play_queued, _i), "queue", _i)

                                    if _later:
                                        fixed:
                                            xsize 626
                                            ysize 30
                                            text "NEXT FROM {}{}".format("FAVORITES" if music_context == "fav" else "ALL TRACKS", "  ·  SHUFFLED" if _shuf else ""):
                                                style "music_section_text"
                                                ypos 9
                                        for _i, _t in enumerate(_later):
                                            use music_row(len(music_queue) + _i + 1, _t, Function(start_track, _t), "next")

                                    if not music_queue and not _later:
                                        frame:
                                            style "music_empty_frame"
                                            text "Nothing up next. Queue a track with the button at the end of its row." style "music_no_track"

                                elif not _rows:
                                    frame:
                                        style "music_empty_frame"
                                        if _q:
                                            text "No heard tracks match \"[query!q]\"." style "music_no_track"
                                        else:
                                            text "No favorites yet. Tap the heart on a track to keep it here." style "music_no_track"

                                else:
                                    for _n, _t in _rows:
                                        use music_row(_n, _t, Function(music_play_from, _t, tab))

                        # What plays next; opens the full queue.
                        button:
                            style "music_footer_button"
                            action [SetScreenVariable("tab", "queue"), Function(list_y.change, 0)]

                            text "UP NEXT" style "music_footer_label" xpos 16 ycenter 20
                            if _up:
                                text "{}  ·  {}".format(_up[0].title, _up[0].artist):
                                    style "music_footer_text"
                                    xpos 100
                                    ycenter 20
                            else:
                                text ("Starts over" if current_track and _mode != MODE_NO_REPEAT else "End of list"):
                                    style "music_footer_text"
                                    xpos 100
                                    ycenter 20
                            text "›" style "music_footer_label" xanchor 1.0 xpos 628 ycenter 20

    # Console brackets framing the shell (cohesion with the archive hub).
    use archive_shell_brackets()

    # Labels for the icon-only deck controls.
    if _tip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                style "music_tip_frame"
                xalign 0.5
                text _tip style "music_tip_text"

# =============================================================================
# STYLES
# =============================================================================
style music_list_frame:
    xsize 664
    ysize 540
    background Solid("#07101add")
    padding (10, 10)

style music_deck_label:
    font gui.interface_font
    size 13
    color "#9fd9ee"
    bold True
    kerning 2.0
    outlines [(1, "#02040b", 0, 0)]

style music_deck_meta is music_deck_label:
    color "#7f97a6"
    bold False

style music_deck_title:
    font gui.interface_font
    size 26
    color "#f2fbff"
    bold True
    outlines [(2, "#02040b", 0, 0)]

style music_deck_artist:
    font gui.interface_font
    size 16
    color "#a9c6d4"
    outlines [(1, "#02040b", 0, 0)]

style music_time:
    font gui.interface_font
    size 13
    color "#9fc9d6"
    outlines [(1, "#02040b", 0, 0)]

# Seek and volume share one look: a thin rounded track and a dot that grows
# under the pointer. Both dots are 16 px so the bar's travel never shifts.
style music_seek_bar:
    xsize 422
    ysize 16
    left_bar music_bar("#56d7ff")
    right_bar music_bar("#24384a")
    thumb music_icon("dot", "#eaf7ff")
    hover_thumb music_icon("dot_big", "#ffffff")
    thumb_offset 8

style music_volume_bar is music_seek_bar:
    xsize 330

style music_volume_pct:
    font gui.interface_font
    size 13
    color "#9fc9d6"
    outlines [(1, "#02040b", 0, 0)]

# Every button here sets its own size: a style named *_button inherits gui's
# button height as a hard max (see enter-m row-alignment notes).
style music_icon_button:
    xysize (36, 36)
    padding (6, 6)
    background None
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style music_transport_button is music_icon_button:
    xysize (42, 42)

style music_clear_button is music_icon_button:
    xysize (22, 22)
    padding (3, 3)

style music_play_button:
    xysize (64, 64)
    padding (0, 0)
    background music_icon("circle", "#56d7ff")
    hover_background music_icon("circle", "#eaffff")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style music_tab_button:
    ysize 34
    padding (14, 0)
    background None
    hover_background music_round("#16324a", 0.85)
    selected_background music_round("#1c4a68", 0.95)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style music_tab_button_text:
    font gui.interface_font
    size 14
    color "#7f97a6"
    hover_color "#ffffff"
    selected_color "#eaffff"
    bold True
    kerning 1.0
    yalign 0.5
    outlines [(1, "#02040b", 0, 0)]

style music_search_frame:
    ysize 34
    padding (12, 6)
    background music_round("#050811", 0.85)

style music_search_hint:
    font gui.interface_font
    size 14
    color "#4f6472"
    italic True
    outlines [(1, "#02040b", 0, 0)]

style music_search_input:
    font gui.interface_font
    size 14
    color "#eaffff"
    outlines [(1, "#02040b", 0, 0)]

style music_row_button:
    xysize (626, 50)
    padding (0, 0)
    background music_round("#0a1724", 0.7)
    hover_background music_round("#14304a", 0.9)
    selected_background music_round("#16405f", 0.95)
    insensitive_background music_round("#060c14", 0.55)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style music_track_number:
    font gui.interface_font
    color "#56d7ff"
    size 16
    bold True
    outlines [(1, "#02040b", 0, 0)]

style music_track_title:
    font gui.interface_font
    color "#dff8ff"
    hover_color "#ffffff"
    selected_color "#56d7ff"
    size 17
    bold True
    outlines [(1, "#02040b", 0, 0)]

style music_track_artist:
    font gui.interface_font
    color "#8fb3c2"
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

style music_section_text:
    font gui.interface_font
    size 12
    color "#7fcfe0"
    bold True
    kerning 1.5
    outlines [(1, "#02040b", 0, 0)]

style music_small_button:
    ysize 26
    padding (10, 0)
    background music_round("#0c1c2a", 0.9)
    hover_background music_round("#14304a", 0.95)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style music_small_button_text:
    font gui.interface_font
    size 12
    color "#9fc9d6"
    hover_color "#ffffff"
    bold True
    yalign 0.5
    outlines [(1, "#02040b", 0, 0)]

style music_empty_frame:
    xsize 626
    ysize 120
    padding (24, 10)
    background music_round("#07111d", 0.8)

style music_no_track:
    font gui.interface_font
    size 16
    color "#687787"
    xalign 0.5
    yalign 0.5
    text_align 0.5
    outlines [(1, "#02040b", 0, 0)]

style music_footer_button:
    xysize (644, 40)
    padding (0, 0)
    background music_round("#0b1a28", 0.9)
    hover_background music_round("#14304a", 0.95)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style music_footer_label:
    font gui.interface_font
    size 12
    color "#56d7ff"
    bold True
    kerning 1.5
    outlines [(1, "#02040b", 0, 0)]

style music_footer_text:
    font gui.interface_font
    size 14
    color "#cfe6f0"
    hover_color "#ffffff"
    outlines [(1, "#02040b", 0, 0)]

style music_tip_frame:
    padding (10, 5)
    background music_round("#050a10", 0.95)

style music_tip_text:
    font gui.interface_font
    size 13
    color "#eaf7ff"
    outlines []
