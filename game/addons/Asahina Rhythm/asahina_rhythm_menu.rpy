# Asarhythm's song select. The song list, the play style and the modifiers are
# the page. The face-off on the right is the room's animation. How to play is a
# tooltip, and timing and scroll settings sit in a drawer.
#
# Song select plays its own track on its own channel, so the mode's pause of the
# main music channel is never touched. The duo dances to that track's measured
# beat by reading its playback position, so the dance stays on the music across
# loops and after every return from a song.

define -50 audio.asarhythm_menu = "assets/audio/bgm/day_b.ogg"  # song select; a placeholder track

init -1 python:
    AR_MENU_CHANNEL = "asahina_rhythm_menu"
    # Measured from day_b.ogg on Sep 13 2026 (onset phase-lock, then a kick
    # fold for the beat and loudness rises for the bar): 100.00 BPM with a
    # downbeat at 1.6128 s. Re-measure when the track changes; the dance reads both.
    AR_MENU_BPM = 100.0
    AR_MENU_DOWNBEAT = 1.6128

    if not renpy.music.channel_defined(AR_MENU_CHANNEL):
        renpy.music.register_channel(AR_MENU_CHANNEL, mixer="music", loop=True, stop_on_mute=False)

    def ar_menu_music(play, fade=.6):
        if play:
            renpy.music.play(audio.asarhythm_menu, channel=AR_MENU_CHANNEL, loop=True, fadein=0.0, if_changed=True)
        else:
            renpy.music.stop(channel=AR_MENU_CHANNEL, fadeout=fade)

    class ARMenuClock(object):
        """The menu track's beat, smoothed between coarse audio positions. Wall time stands in while it is silent."""
        def __init__(self):
            self.clock = None
            self.last = None
            self.epoch = ar_time.perf_counter()

        def beat(self):
            wall = ar_time.perf_counter()
            position = renpy.music.get_pos(channel=AR_MENU_CHANNEL)
            beat_len = 60.0 / AR_MENU_BPM
            if position is None:
                self.clock = self.last = None
                return (wall - self.epoch) / beat_len
            if self.clock is None or position < self.last - .5:
                # The first sample, or the track looped back to its start.
                self.clock = SongClock(wall, position)
            self.last = position
            return (self.clock.sample(wall, position) - AR_MENU_DOWNBEAT) / beat_len

    AR_MENU_CLOCK = ARMenuClock()

    class ARBeatPulse(renpy.Displayable):
        """Its child, bumped a little bigger on every beat of the menu track."""
        def __init__(self, child, amount=.03, fall=.16, **kwargs):
            super(ARBeatPulse, self).__init__(**kwargs)
            self.child = renpy.displayable(child)
            self.amount, self.fall = amount, fall

        def visit(self):
            return [self.child]

        def render(self, width, height, st, at):
            rendered = renpy.render(self.child, width, height, st, at)
            w, h = rendered.get_size()
            zoom = 1 + self.amount * ar_beat_envelope(AR_MENU_CLOCK.beat(), 60.0 / AR_MENU_BPM, self.fall)
            wrap = renpy.Render(w, h)
            wrap.zoom(zoom, zoom)
            wrap.blit(rendered, (0, 0))
            rv = renpy.Render(w, h)
            rv.subpixel_blit(wrap, (w * (1 - zoom) * .5, h * (1 - zoom) * .5))
            renpy.redraw(self, 0)
            return rv

    class ARMenuLights(renpy.Displayable):
        """Three slow lamp beams and drifting bokeh behind song select, swelling on each bar of the menu track."""
        BEAMS = ((200.0, -14.0, 0.0, "pink"), (640.0, 0.0, 2.1, "cyan"), (1080.0, 14.0, 4.2, "gold"))
        GLOWS = ("pink", "cyan", "gold", "white")

        def __init__(self, **kwargs):
            super(ARMenuLights, self).__init__(**kwargs)
            self.images = {}
            for tint in self.GLOWS:
                self.images[("glow", tint)] = Image(AR_FX + "glow_%s.png" % tint)
            for x, rest, phase, tint in self.BEAMS:
                self.images[("beam", tint)] = Image(AR_FX + "beam_%s.png" % tint)
            self.rigs = [Transform(self.images[("beam", tint)], rotate_pad=True) for x, rest, phase, tint in self.BEAMS]

        def visit(self):
            return list(self.images.values())

        def render(self, width, height, st, at):
            rv = renpy.Render(1280, 720)
            beat = AR_MENU_CLOCK.beat()
            fade = min(1.0, st / .8)
            swell = ar_beat_envelope(beat, 60.0 / AR_MENU_BPM, .5, 4.0)
            for rig, (x, rest, phase, tint) in zip(self.rigs, self.BEAMS):
                degrees = rest + 12.0 * ar_math.sin(2 * ar_math.pi * beat / 16.0 + phase)
                ar_blit_turned(rv, rig, (220, 900), (110, 0), (x, -60), degrees, st, at, (.10 + .06 * swell) * fade)
            for i in range(14):
                speed = 8.0 + 14.0 * ar_unit(31, i, 1)
                x = (ar_unit(31, i) * 1380 + 30 * ar_math.sin(st * .2 + i)) % 1380 - 50
                y = 760 - ((st * speed + 840 * ar_unit(31, i, 2)) % 840)
                twinkle = .5 + .5 * ar_math.sin(st * (.8 + ar_unit(31, i, 3)) + i)
                ar_blit(rv, self.images[("glow", self.GLOWS[i % 4])], x, y, st, at, scale=.12 + .22 * ar_unit(31, i, 4),
                        alpha=(.10 + .12 * twinkle) * fade, additive=True)
            renpy.redraw(self, 0)
            return rv

    class ARMenuDuo(renpy.Displayable):
        """Song select's face-off. On the menu track's beat Asahina sings a three-note phrase and
        the player answers with the same one; every fourth phrase they both throw a hey instead.
        The menu's buttons call react() so a choice gets an answer."""
        SIZE = (560, 480)
        FLOOR = 432
        ZOOM = .68
        SINGERS = (("asahina", 140, -1, "pink"), ("asahiko", 420, 1, "cyan"))
        REACTIONS = {"harder": ("hey", "up"), "easier": ("hey", "down"), "song": ("hey", "hey"),
                     "duet": ("right", "left"), "ready": ("up", "hey")}

        def __init__(self, **kwargs):
            super(ARMenuDuo, self).__init__(**kwargs)
            self.images = {}
            self.singers = {name: ARSingerFrames(name) for name in ("asahina", "asahiko")}
            self.images["shadow"] = Image(AR_UI + "shadow.png")
            self.images["ring"] = Image(AR_FX + "ring_gold.png")
            for tint in ("pink", "cyan"):
                self.images[("glow", tint)] = Image(AR_FX + "glow_%s.png" % tint)
            self.images["vs"] = Text("VS", style="ar_vs")
            self.images[("name", "asahina")] = Text("ASAHINA", style="ar_name", color=AR_PINK)
            self.images[("name", "asahiko")] = Text("YOU", style="ar_name", color=AR_CYAN)
            self.vs_rig = Transform(self.images["vs"], rotate_pad=True)
            self.reaction = None

        def visit(self):
            return list(self.images.values()) + list(self.singers.values())

        def react(self, kind):
            """Answer a menu choice: harder, easier, song, duet, ready, or off for a switch turned off."""
            self.reaction = (kind, ar_time.perf_counter())
            renpy.redraw(self, 0)

        def react_mod(self, mod):
            if not ar_mod_on(mod):
                self.react("off")
            else:
                self.react("harder" if mod in AR_CHALLENGES else "easier")

        def _pose(self, index, beat, wall):
            """(pose, light_pulse, gesture_token), including one token per sustain."""
            beat_len = 60.0 / AR_MENU_BPM
            if self.reaction is not None:
                kind, began = self.reaction
                age = wall - began
                poses = self.REACTIONS.get(kind)
                if poses and age < 1.1:
                    return poses[index], ar_math.exp(-max(0.0, age - .08) / .14), ("reaction", began)
            cycle = int(ar_math.floor(beat / 8.0))
            within = beat - cycle * 8
            if cycle % 4 == 3:
                if within >= 6:
                    age = (within - 6) * beat_len
                    return "hey", ar_math.exp(-max(0.0, age - .08) / .14), ("hey", cycle)
            else:
                # Asahina sings beats 0-2 and holds the third note through beat 3;
                # the player answers with the same phrase on beats 4-7.
                step = within - 4 * index
                if 0 <= step < 4:
                    note = min(2, int(step))
                    lane = int(ar_unit(cycle, note, 11) * 4)
                    age = (step - note) * beat_len
                    return AR_POSES[lane], ar_math.exp(-max(0.0, age - .075) / .11), ("phrase", cycle, index, note)
            return "idle", 0.0, None

        def render(self, width, height, st, at):
            wall = ar_time.perf_counter()
            beat_len = 60.0 / AR_MENU_BPM
            beat = AR_MENU_CLOCK.beat()
            rv = renpy.Render(*self.SIZE)
            for index, (name, spot, side, tint) in enumerate(self.SINGERS):
                # Each singer slides in from their own side with a little overshoot.
                delay = .05 + .10 * index
                entrance = ar_ease_out_back((st - delay) / .55)
                appear = max(0.0, min(1.0, (st - delay) / .25))
                x = spot + side * 300 * (1 - entrance) + 3 * ar_math.sin(ar_math.pi * beat / 2 + index * 1.7)
                pose, punch, event = self._pose(index, beat, wall)
                singer = self.singers[name]
                singer.set_pose(pose, wall, event=event, duration=beat_len if pose in AR_POSES else None)
                singer.set_clock(wall, beat, beat_len)
                # The floor lights up under whoever is singing.
                ar_blit(rv, self.images[("glow", tint)], x, self.FLOOR + 4, st, at, scale=1.5, sy=.42,
                        alpha=(.22 if pose == "idle" else .52) * appear, additive=True)
                if pose != "idle" and punch > .05:
                    ring = .3 + .55 * (1 - punch)
                    ar_blit(rv, self.images["ring"], x, self.FLOOR, st, at, scale=ring, sy=ring * .32,
                            alpha=.7 * punch * appear, additive=True)
                ar_blit(rv, self.images["shadow"], x, self.FLOOR + 4, st, at, scale=.40, alpha=.85 * appear)
                ar_blit(rv, singer, x, self.FLOOR, st, at, scale=self.ZOOM,
                        alpha=appear, yanchor=430 / 448.0)
                ar_blit(rv, self.images[("name", name)], spot, self.FLOOR + 30, st, at, alpha=appear)
            stamp = max(0.0, min(1.0, (st - .35) / .25))
            if stamp > 0:
                zoom = 2.2 - 1.2 * ar_ease_out(stamp) + .08 * ar_beat_envelope(beat, beat_len, .12) * stamp
                degrees = -14 * (1 - stamp) + 3 * ar_math.sin(ar_math.pi * beat / 2) * stamp
                ar_blit_turned(rv, self.vs_rig, (2, 2), (1, 1), (280, 196), degrees, st, at, alpha=stamp,
                               additive=False, zoom=zoom)
            renpy.redraw(self, 0)
            return rv

screen asahina_rhythm_setup(songs, errors, uncover=None):
    modal True
    zorder 40
    use enter_m_input_lock()
    default selected = ar_last_song_index(songs)
    default song_scroll = ar_song_adjustment(songs, ar_last_song_index(songs))
    default panel = None
    default duo = ARMenuDuo()
    default lights = ARMenuLights()
    default logo = ARBeatPulse(Text("ASARHYTHM", style="ar_logo"))
    # The way in covers the page with the song's title card, then returns the
    # song's index. Arriving on a covered frame clears it (asahina_rhythm_finale.rpy).
    default leave_wipe = ARWipe("cover")
    default enter_wipe = (ARWipe("uncover", uncover, hold=AR_WIPE_HOLD, grace=.2) if uncover else None)
    $ chart = songs[selected] if songs else None
    $ duet = bool(persistent.asahina_rhythm_duet)
    $ practice = bool(persistent.asahina_rhythm_practice)
    $ autoplay = bool(persistent.asahina_rhythm_autoplay)
    $ mods_on = ar_active_mods()
    $ record = ar_best(chart, duet) if chart else {}
    $ clears = set(record.get("mod_clears", ()))
    $ tip = GetTooltip()
    $ go = Function(ar_leave_for_song, leave_wipe, selected, chart, duo) if chart else NullAction()
    # A list taller than its window is cut off mid-row on purpose. The counter,
    # the bobbing chevron, the bar and the faded cut all say the same thing.
    $ scrolls = len(songs) > AR_SONG_VIEW
    $ list_h = ar_song_list_height(len(songs))
    $ list_w = AR_LIST_W - (16 if scrolls else 0)

    add AR_ART + "stage_blur.webp"
    add Solid("#12082ab4")
    add lights
    add Tile(AR_UI + "stripes.png") xysize (1376, 816) alpha .5 at ar_drift
    add AR_UI + "shade_left.png"
    add AR_UI + "vignette.png"

    # ---- header ----
    add logo xpos 42 ypos 10 at ar_rise(0.0)
    hbox:
        xanchor 1.0 xpos 1236 ypos 30
        spacing 8
        textbutton "HOW TO PLAY" id "ar_setup_howto" style "ar_chip_button" selected panel == "howto" tooltip "howto" action ToggleScreenVariable("panel", "howto", None)
        textbutton "SETTINGS" id "ar_setup_settings" style "ar_chip_button" selected panel == "settings" tooltip "Input and visual offsets, scroll speed, tempo scroll and downscroll." action ToggleScreenVariable("panel", "settings", None)

    # ---- left: the song, how to sing it, and the modifiers ----
    vbox:
        xpos 48 ypos 92 xsize AR_LIST_W
        fixed:
            xysize (AR_LIST_W, 18)
            text "SONG" style "ar_kicker" yalign .5
            if songs:
                hbox:
                    xanchor 1.0 xpos AR_LIST_W yalign .5
                    spacing 7
                    text ("%d / %d" % (selected + 1, len(songs))) style "ar_count" yalign .5
                    if scrolls:
                        add AR_UI + "chevron_pink.png" yalign .5 at ar_nudge
        null height 6
        if songs:
            hbox:
                spacing 8
                fixed:
                    xysize (list_w, list_h)
                    viewport:
                        id "ar_song_list"
                        xysize (list_w, list_h)
                        yadjustment song_scroll
                        mousewheel True
                        vbox:
                            spacing AR_SONG_GAP
                            for i, song in enumerate(songs):
                                $ song_best = ar_best(song, duet)
                                button:
                                    style "ar_song"
                                    xysize (list_w, AR_SONG_ROW)
                                    selected i == selected
                                    tooltip (("Play %s." if i == selected else "Choose %s.") % song["title"])
                                    action (go if i == selected else [Function(ar_pick_song, i, len(songs), song_scroll), Function(duo.react, "song")])
                                    at ar_slide(.08 + i * .04)
                                    fixed:
                                        text "‣" style "ar_song_mark" size 30 xpos 6 yalign .5
                                        add AR_ART + "icons/asahina_normal.png" zoom .32 xpos 26 yalign .5
                                        text ar_fit_text(song["title"], list_w - 260, AR_FONT, 30, ((4, "#160f24", 0, 2),)) style "ar_song_title" size 30 xpos 74 yalign .5 substitute False
                                        if song_best.get("rank"):
                                            text song_best["rank"] style "ar_song_rank" xanchor 1.0 xpos (list_w - 80) yalign .5
                                        text ar_time_label(song["duration"]) style "ar_song_time" xanchor 1.0 xpos (list_w - 18) yalign .5
                    # Over the list, never in it: a cut row fades out instead of
                    # ending on a hard edge, so the clip reads as "there is more".
                    # Each end's scrim is only as strong as the scroll left in it.
                    if scrolls:
                        add AR_UI + "list_fade_top.png" xysize (list_w, 30) at Transform(function=ar_list_edge(song_scroll, True))
                        add AR_UI + "list_fade.png" xysize (list_w, 30) ypos (list_h - 30) at Transform(function=ar_list_edge(song_scroll, False))
                if scrolls:
                    vbar:
                        value YScrollValue("ar_song_list")
                        xysize (8, list_h)
                        style "ar_scroll"
        else:
            text "No playable chart found." style "ar_song_title"
        if chart:
            null height 8
            hbox:
                spacing 8
                for chip in ar_song_stats(chart, duet):
                    frame:
                        style "ar_chip"
                        text chip style "ar_chip_text"
            null height 6
            frame:
                style "ar_bestcard"
                xysize (AR_LIST_W, 48)
                fixed:
                    add Solid(AR_CYAN if duet else AR_PINK) xysize (3, 36) xpos 3 yalign .5
                    text ("DUET BEST" if duet else "PERSONAL BEST") style "ar_kicker" size 12 xpos 16 ypos 4
                    if "score" in record:
                        text "{:,}".format(record["score"]) style "ar_best_line" xpos 16 ypos 17
                        text ("%.2f%%   •   %d CLEAR%s" % (record["accuracy"], record.get("clears", 0), "" if record.get("clears", 0) == 1 else "S")) style "ar_opt_hint" xpos 150 ypos 27
                        text record["rank"] style "ar_best_rank" size 38 xanchor 1.0 xpos 578 yalign .5
                    else:
                        text "NO CLEAR YET" style "ar_best_empty" size 20 xpos 16 ypos 19
        null height 10
        text "PLAY AS" style "ar_kicker"
        null height 5
        hbox:
            spacing 6
            textbutton "SOLO" id "ar_setup_solo" style "ar_seg" selected not duet tooltip "Sing your own side on D F J K or the arrow keys." action [Function(ar_set_duet, False), Function(duo.react, "song")]
            textbutton "DUET  •  8 KEYS" id "ar_setup_duet" style "ar_seg" selected duet tooltip "Sing both sides: A S D F for Asahina's lanes, J K L ; or the arrow keys for yours. Duets keep their own records." action [Function(ar_set_duet, True), Function(duo.react, "duet")]
        null height 10
        fixed:
            xysize (AR_LIST_W, 18)
            text "MODIFIERS" style "ar_kicker" yalign .5
            if (mods_on - set(["duet"])) or practice or autoplay:
                textbutton "CLEAR ALL" id "ar_setup_clear_mods" style "ar_link" xanchor 1.0 xpos AR_LIST_W yalign .5 action [Function(ar_clear_mods), Function(duo.react, "off")]
        null height 4
        # Both groups are the same switch, drawn the same way; only the lit
        # colour and what the tile means differ.
        for group, tint, entries in (("HARDER", "pink", AR_HARDER), ("EASIER", "cyan", AR_EASIER)):
            text group style "ar_group"
            null height 3
            grid 3 2:
                spacing 6
                for mod, name, hint in entries:
                    button:
                        style ("ar_mod" if tint == "pink" else "ar_mod_easy")
                        xysize (197, 40)
                        selected ar_mod_on(mod)
                        sensitive ar_mod_available(mod)
                        tooltip (hint + (" You've cleared this song with it on." if mod in clears else ""))
                        action [Function(ar_toggle_mod, mod), Function(duo.react_mod, mod)]
                        fixed:
                            add (AR_UI + ("check_%s.png" % tint if ar_mod_on(mod) else "check_off.png")) xpos 10 yalign .5
                            text name style "ar_mod_name" xpos 40 yalign .5
                            if mod in clears:
                                add Solid(AR_GOLD) xysize (8, 8) rotate 45 xanchor .5 yanchor .5 xpos 180 ypos .5
                for spare in range(6 - len(entries)):
                    null
            null height 6

    # ---- right: the face-off and the way in ----
    add duo xpos 676 ypos 80
    text ar_fit_text(ar_mod_summary(mods_on, practice, autoplay), 552, AR_UI_FONT, 14) style "ar_hint" xanchor .5 xpos 956 ypos 572 substitute False
    hbox:
        xanchor .5 xpos 956 ypos 600
        spacing 12
        textbutton "LET'S GO" id "ar_setup_start" style "ar_button_primary" sensitive bool(songs) hovered Function(duo.react, "ready") action go
        textbutton "BACK" id "ar_setup_back" style "ar_button" action Return("back")
        if config.developer and renpy.has_label("asahina_rhythm_chart_editor"):
            textbutton "CHART EDITOR" id "ar_setup_editor" style "ar_button" action Return(("editor", selected) if songs else "editor")

    # The left column now runs to the hint line, so a broken chart reports on the right.
    if errors:
        text errors[0] style "ar_hint" color "#fa8caa" xanchor .5 xpos 956 ypos 658 xmaximum 560 text_align .5 substitute False
    text (tip if tip and tip != "howto" else "ENTER  play      ESC  back      UP / DOWN  choose song") style "ar_hint" xpos 50 ypos 697 substitute False

    # ---- the tooltip card and the settings drawer, over everything ----
    if panel == "howto" or tip == "howto":
        frame:
            style "ar_card"
            xanchor 1.0 xpos 1236 ypos 76 xsize 548
            at ar_rise(0.0)
            vbox:
                spacing 8
                add Solid(AR_CYAN) xysize (504, 3)
                text "HOW TO PLAY" style "ar_kicker"
                if duet:
                    hbox:
                        spacing 8
                        for letter in ("A", "S", "D", "F"):
                            frame:
                                style "ar_key"
                                text letter style "ar_key_text"
                        text "Asahina's lanes" style "ar_body" yalign .5
                    hbox:
                        spacing 8
                        for letter in ("J", "K", "L", ";"):
                            frame:
                                style "ar_key"
                                text letter style "ar_key_text"
                        text "your lanes, or the arrow keys" style "ar_body" yalign .5
                else:
                    hbox:
                        spacing 8
                        for letter in ("D", "F", "J", "K"):
                            frame:
                                style "ar_key"
                                text letter style "ar_key_text"
                        text "or the arrow keys" style "ar_body" yalign .5
                text "Hit your notes as they cross the outlines. Hold long notes through their tails." style "ar_body" xmaximum 504
                if duet:
                    text "You sing both sides, so Asahina's notes count exactly like yours." style "ar_body" xmaximum 504
                else:
                    text "Asahina sings the left side and you sing the right. Empty presses during your phrase cost health." style "ar_body" xmaximum 504
                text "ESC or right-click pauses. Losing focus pauses too." style "ar_body" xmaximum 504
                text ar_window_text(mods_on) style "ar_hint"
    if panel == "settings":
        frame:
            style "ar_card"
            xanchor 1.0 xpos 1236 ypos 76 xsize 560
            at ar_rise(0.0)
            vbox:
                spacing 8
                add Solid(AR_CYAN) xysize (516, 3)
                fixed:
                    xysize (516, 22)
                    text "SETTINGS" style "ar_kicker" yalign .5
                    textbutton "DONE" id "ar_setup_settings_done" style "ar_link" xanchor 1.0 xpos 516 yalign .5 action SetScreenVariable("panel", None)
                use asahina_rhythm_settings(chart)

    key "K_ESCAPE" action If(panel, SetScreenVariable("panel", None), Return("back"))
    if songs:
        key "K_RETURN" action go
        key "K_KP_ENTER" action go
        if len(songs) > 1:
            key "K_UP" action [Function(ar_step_song, -1, len(songs), song_scroll), Function(duo.react, "song")]
            key "K_DOWN" action [Function(ar_step_song, 1, len(songs), song_scroll), Function(duo.react, "song")]

    # Last, so the wipes see input first.
    if enter_wipe is not None:
        add enter_wipe
    add leave_wipe

# The song list's more-below chevron, bobbing so it reads as an invitation.
transform ar_nudge:
    yoffset 0
    easeout .55 yoffset 4
    easein .55 yoffset 0
    repeat

style ar_count:
    font AR_UI_FONT
    size 14
    color "#cbb9e0"
    kerning 1.2
style ar_song_time:
    font AR_UI_FONT
    size 18
    color "#bba9d0"
    selected_color "#ffe08a"
style ar_song_rank:
    font AR_FONT
    size 26
    color "#ffe08a"
    outlines [(4, "#160f24", 0, 2)]
style ar_scroll is vscrollbar:
    # vscrollbar carries bar_invert, without which the thumb counts up from the
    # bottom. bar_resizing makes its length say how much of the list is showing.
    xsize 8
    bar_resizing True
    base_bar Frame(AR_UI + "rail_track.png", 0, 6)
    thumb Frame(AR_UI + "rail_thumb.png", 0, 6)
    thumb_offset 0
style ar_bestcard:
    background Frame(AR_UI + "tile_idle.png", 11, 11)
    padding (0, 0)
style ar_best_line:
    font AR_UI_FONT
    size 24
    color "#ffffff"
    outlines [(2, "#160f24", 0, 1)]
style ar_chip_button:
    padding (14, 7)
    background Frame(AR_UI + "plate_idle.png", 14, 14)
    hover_background Frame(AR_UI + "plate_hover.png", 14, 14)
    selected_background Frame(AR_UI + "plate_cyan.png", 14, 14)
    selected_hover_background Frame(AR_UI + "plate_cyan_hot.png", 14, 14)
style ar_chip_button_text:
    font AR_UI_FONT
    size 14
    color "#ffffff"
    selected_color "#160f24"
    kerning 1.5
style ar_seg is ar_chip_button:
    padding (18, 8)
    selected_background Frame(AR_UI + "plate_pink.png", 14, 14)
    selected_hover_background Frame(AR_UI + "plate_pink_hot.png", 14, 14)
style ar_seg_text is ar_chip_button_text:
    size 16
    selected_color "#ffffff"
    outlines [(2, "#160f24", 0, 1)]
style ar_mod:
    padding (0, 0)
    background Frame(AR_UI + "tile_idle.png", 11, 11)
    hover_background Frame(AR_UI + "tile_hover.png", 11, 11)
    selected_background Frame(AR_UI + "tile_pink.png", 11, 11)
    selected_hover_background Frame(AR_UI + "tile_pink_hot.png", 11, 11)
    insensitive_background Frame(AR_UI + "tile_off.png", 11, 11)
style ar_mod_easy is ar_mod:
    selected_background Frame(AR_UI + "tile_cyan.png", 11, 11)
    selected_hover_background Frame(AR_UI + "tile_cyan_hot.png", 11, 11)
style ar_mod_name:
    font AR_FONT
    size 17
    color "#bba9d0"
    hover_color "#ffffff"
    selected_color "#ffffff"
    insensitive_color "#5d5170"
    outlines [(3, "#160f24", 0, 1)]
style ar_group:
    font AR_UI_FONT
    size 12
    color "#9d8fb5"
    kerning 2.0
style ar_link:
    padding (8, 2)
style ar_link_text:
    font AR_UI_FONT
    size 13
    color "#9fe7f1"
    hover_color "#ffffff"
    kerning 1.5
