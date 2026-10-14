# Developer-only authoring surface. No game state, unlocks or rewards are written.
# The grid scrolls under a fixed playhead like FNF's chart editor: the song
# position is the one source of truth and the view is derived from it.
# The document owns the selection (note keys) and the clipboard; the grid only
# turns presses and drags into place, select and move operations on it.

# The wide FX lane (Ctrl+E). A studio layout preference, kept between sessions.
default persistent.asahina_rhythm_editor_fx_wide = False

init python:
    import bisect as _are_bisect
    import copy as _are_copy
    import math as _are_math
    import os as _are_os
    import re as _are_re
    import time as _are_time
    import pygame_sdl2 as _are_pygame
    from asahina_rhythm_editor import (ChartDocument as _ARChartDocument, beats_text as are_beats_text,
                                       note_column as _are_note_column, note_key as _are_note_key,
                                       plural as _are_plural, EFFECT_NAMES as ARE_EFFECT_NAMES,
                                       effect_key as _are_effect_key, SIDE_NAMES as ARE_SIDE_NAMES,
                                       EFFECT_GROUPS as ARE_EFFECT_GROUPS)
    from asahina_rhythm_core import (SongClock as _ARESongClock, camera_plan as _are_camera_plan,
                                     measure_index as _are_measure_index, BURST_EFFECTS as _ARE_BURSTS,
                                     EFFECT_KINDS as ARE_EFFECT_KINDS, EFFECT_SIDES as ARE_EFFECT_SIDES,
                                     REACTIVE_EFFECTS as _ARE_REACTIVE)

    renpy.music.register_channel("asahina_editor", mixer="music", loop=False, stop_on_mute=False)
    if not renpy.music.channel_defined("asahina_editor_hits"):
        renpy.music.register_channel("asahina_editor_hits", mixer="sfx", loop=False, stop_on_mute=False)

    # Grid geometry, in pixels inside the grid displayable. Left to right: the
    # measure and beat gutter, the CAM lane, the FX lane (side-by-side tracks for
    # effects that overlap), then Asahina's four lanes and the player's. The FX
    # lane and the note lanes change width together; see AREditorLayout.
    ARE_GRID_X, ARE_GRID_Y, ARE_GRID_W, ARE_GRID_H = 304, 124, 712, 512
    ARE_GUTTER, ARE_CAM_X, ARE_CAM_W = 48, 50, 28
    ARE_FX_X, ARE_DIVIDER = 82, 12
    ARE_BEAT_PX = 52
    ARE_PLAYHEAD = 150
    # A press turns into a drag after this many pixels, and a drag this close to
    # the top or bottom edge scrolls the chart.
    ARE_DRAG_SLOP, ARE_SCROLL_EDGE = 5, 36
    # How near an effect's end the pointer must be to drag its length instead of it.
    ARE_FX_EDGE = 7
    ARE_SELECT_COLOR, ARE_BOX_COLOR, ARE_BLOCKED_COLOR = "#ffe08a", "#5fd8e8", "#ff5a6e"
    ARE_FOCUS_COLORS = {"opponent": "#f06ba8", "player": "#5fd8e8", "center": "#b59cff"}
    ARE_FOCUS_NAMES = {None: "AUTO", "opponent": "ASAHINA", "player": "YOU", "center": "BOTH"}
    # The concert half runs warm and saturated; the dread half is cold, drained
    # or sick, so which half of the palette a chart is using reads off the FX
    # lane without reading a single label.
    ARE_FX_COLORS = {"fanfare": "#ffd36a", "spotlights": "#f06ba8", "lasers": "#87e766", "haze": "#b59cff",
                     "blackout": "#8a7aa8", "pulse": "#ff8fc8", "crowd": "#5fd8e8", "flash": "#ffffff",
                     "confetti": "#fa698b", "sparks": "#ffb347", "quake": "#ff7a5c", "strobe": "#ffe9f5",
                     "lunge": "#c874ed", "shockwave": "#52d5ef",
                     "dread": "#4f4766", "watchers": "#e4dcc4", "static": "#8fa3b5", "hollow": "#557a76",
                     "footlights": "#9fc0c4", "rot": "#6b7d3f", "arrhythmia": "#a8394c",
                     "doubles": "#8c79b8", "gutter": "#585269", "recoil": "#c06a8a",
                     "fracture": "#cfd8e8", "cut": "#7a7490", "tear": "#5fb0a0", "glimpse": "#f0e6ff",
                     "veins": "#a3283c", "blood": "#7e1018", "convulse": "#d4566a", "redwash": "#e02030",
                     "invert": "#f2f2f2", "negative": "#9a9aa8", "infrared": "#36e07a",
                     "fried": "#ff8c1a", "bitcrush": "#3fb6d8"}
    ARE_FX_SHORT = {"fanfare": "FA", "spotlights": "SP", "lasers": "LA", "haze": "HZ", "blackout": "BK",
                    "pulse": "PU", "crowd": "CR", "flash": "FL", "confetti": "CF", "sparks": "SK",
                    "quake": "QK", "strobe": "ST", "lunge": "LU", "shockwave": "SW",
                    "dread": "DR", "watchers": "WA", "static": "SC", "hollow": "HO", "footlights": "FO",
                    "rot": "RO", "arrhythmia": "AR", "doubles": "DB", "gutter": "GU", "recoil": "RC",
                    "fracture": "FR", "cut": "CU", "tear": "TR", "glimpse": "GL",
                    "veins": "VN", "blood": "BL", "convulse": "CV", "redwash": "RW",
                    "invert": "IV", "negative": "NG", "infrared": "IR", "fried": "DF",
                    "bitcrush": "BC"}
    # The singer a reactive span answers, marked on its bar in the FX lane.
    ARE_SIDE_SHORT = {"opponent": "A", "player": "Y", "both": "*"}
    ARE_FX_HINTS = {
        "fanfare": "Hits score x2 while the player's streak holds, and x3 after 30 in a row.",
        "spotlights": "Four lamps sweep the stage from above.",
        "lasers": "Laser fans cross the stage from both corners.",
        "haze": "Low fog drifts across the floor.",
        "blackout": "The stage goes dark, with a spotlight on each singer.",
        "pulse": "The camera punches in on every beat.",
        "crowd": "A crowd with glow sticks along the bottom of the screen.",
        "flash": "One white flash.",
        "confetti": "Confetti cannons fire from the bottom corners.",
        "sparks": "Spark fountains go off at the bottom edges.",
        "quake": "Every note the singer lands knocks the whole frame. A four-lane chord hits hardest.",
        "strobe": "Every note the singer lands flares the frame in their colour.",
        "lunge": "The camera shoves toward the singer on every note they land.",
        "shockwave": "A ring blows out of the singer on every note they land.",
        "dread": "The dark closes in from the edges, breathing to nothing in the song.",
        "watchers": "Eyes open in the dark past the stage, blink, and do not leave.",
        "static": "Signal grain over the picture, with a seam walking down it.",
        "hollow": "The crowd goes out. Needs Crowd running to be seen at all.",
        "footlights": "The rig inverts: the lamps die and cold light comes up off the floor.",
        "rot": "Something creeps in at the corners and spreads. It takes light, never adds it.",
        "arrhythmia": "A heartbeat at 46 BPM whatever the song is, so it never lines up.",
        "doubles": "Each singer has company standing behind them, a breath out of step.",
        "gutter": "The stage lighting fails on its own schedule, and half comes back.",
        "recoil": "The camera flinches AWAY from the singer on every note they land.",
        "fracture": "The frame cracks where the singer stands, and the cracks stay.",
        "cut": "Everything drops out for a moment. The song keeps playing.",
        "tear": "The picture loses its hold and slips sideways in bands.",
        "glimpse": "Someone is standing there for a tenth of a second.",
        "veins": "Something branches in under the picture from the corners, and pulses.",
        "blood": "It runs down from the top of the frame and gathers at the bottom.",
        "convulse": "The singers shake where they stand. Not to the beat.",
        "redwash": "The whole frame goes red. Tints the picture rather than painting over it.",
        "invert": "One frame of pure negative. A hard glitch, like Cut and Tear.",
        "negative": "The picture holds inverted for as long as the cue runs.",
        "infrared": "Watched through a night camera: green, blown out, grainy, scanlined.",
        "fried": "Contrast and colour crushed past what the picture can hold.",
        "bitcrush": "The stage loses resolution and goes to blocks. The lanes stay sharp.",
    }
    ARE_SHORTCUTS = (
        ("MOUSE", (
            ("Click", "Place a note, or select one"),
            ("Drag a note", "Move the selection"),
            ("Drag empty grid", "Box-select notes"),
            ("Shift/Ctrl+click", "Add or remove one note"),
            ("Shift/Ctrl+drag", "Add a box to the selection"),
            ("Right-click", "Delete a note"),
            ("Beat gutter", "Drag selects beats; click seeks"),
            ("CAM lane", "Click cycles; right-click resets"),
            ("FX lane", "Click adds or selects; right-click deletes"),
            ("Drag an effect", "Move it; drag its end to set its length"),
            ("Wheel", "One beat; Shift: one grid step"),
        )),
        ("EDIT", (
            ("Ctrl+C / X / V", "Copy, cut, paste at the playhead"),
            ("Ctrl+D", "Duplicate into the next measures"),
            ("Delete", "Delete the selection"),
            ("Ctrl+A", "Select every note"),
            ("Esc", "Cancel a drag, then deselect"),
            ("Ctrl+Up / Down", "Move a grid step; Shift: a beat"),
            ("Ctrl+Left / Right", "Move one lane"),
            ("Ctrl+M / F / G", "Mirror, swap singer, snap"),
            ("[  /  ]", "Shorter or longer hold or effect"),
            ("Ctrl+1 / 2 / 3", "A reactive effect answers Asahina, you, both"),
            ("Ctrl+Z / Y", "Undo or redo"),
        )),
        ("PLAYBACK", (
            ("Space", "Play or pause"),
            ("Up / Down", "Step the playhead"),
            ("PgUp / PgDn", "Eight beats"),
            ("Home / End", "Song start or last note"),
            ("Alt+1..8", "Toggle a note at the playhead"),
            ("Ctrl+S", "Save the chart"),
            ("Ctrl+E", "Widen or narrow the FX lane"),
            ("F1", "Show or hide this sheet"),
        )),
    )

    class AREditorLayout(object):
        """Where the FX tracks and the note lanes sit.

        The note lanes stay flush with the grid's right edge, so a wider FX lane
        takes its room from them, and the lane sprites shrink to match.
        """
        def __init__(self, tracks, track_w, lane_w):
            self.fx_tracks = tracks
            self.track_w = track_w
            self.fx_w = tracks * track_w
            self.lane_w = lane_w
            self.lane_x0 = ARE_GRID_W - 8 * lane_w - ARE_DIVIDER
            # Against the 70 px lane the small note sprites (84 px canvases) are drawn for.
            self.zoom = lane_w / 70.0

        def column_x(self, column):
            return self.lane_x0 + column * self.lane_w + (ARE_DIVIDER if column >= 4 else 0)

    # Narrow, then wide (Ctrl+E or the FX header). Wide gives nine 22 px tracks
    # for 52 px note lanes. Both leave 4 px between the FX lane and the notes.
    ARE_LAYOUTS = (AREditorLayout(3, 18, 70), AREditorLayout(9, 22, 52))

    def are_layout():
        return ARE_LAYOUTS[bool(persistent.asahina_rhythm_editor_fx_wide)]

    def are_clock(seconds):
        seconds = max(0.0, seconds)
        return "%d:%06.3f" % (int(seconds // 60), seconds % 60)

    def are_bar_beat(editor, seconds):
        """(measure index, beats into it). The nudge keeps a note on a downbeat from reading as the beat before."""
        beat = editor.beat_at(seconds) + .000001
        measure = int(_are_math.floor(beat / 4.0))
        return measure, beat - measure * 4

    def are_position(editor, seconds):
        measure, within = are_bar_beat(editor, seconds)
        return "M%d.%d" % (measure + 1, int(within) + 1)

    def are_offset_text(steps, columns):
        parts = []
        if steps:
            parts.append("%s %s" % (_are_plural(abs(steps), "grid step"), "later" if steps > 0 else "earlier"))
        if columns:
            parts.append("%s %s" % (_are_plural(abs(columns), "lane"), "right" if columns > 0 else "left"))
        return " and ".join(parts)

    def ar_editor_refresh_files():
        # MatsuPy 8.6 maintains a case-normalized index as well as the directory
        # list. Earlier SDKs exposed only the directory-cache reset operation.
        refresh = getattr(renpy.loader, "index_files", None)
        if refresh is None:
            refresh = renpy.loader.cleardirfiles
        refresh()

    class ARChartEditor(_ARChartDocument):
        def __init__(self, chart):
            super(ARChartEditor, self).__init__(chart, lambda: bool(config.developer))
            self.playing = False
            self.clock = None
            self.started_at = 0.0
            self.awaiting_audio = False
            self.search = ""
            self.hitsounds = False
            self.grid = ARChartGrid(self)
            self.timeline = ARChartTimeline(self)

        def run(self, method, *args, **kwargs):
            try:
                self.require_developer()
                # Function actions treat a non-None return as a screen result.
                # Save paths and other operation results must stay inside the UI.
                getattr(self, method)(*args, **kwargs)
                renpy.redraw(self.grid, 0)
                renpy.redraw(self.timeline, 0)
            except (ValueError, TypeError, OSError, UnicodeError) as error:
                self.status = str(error)
                renpy.notify(self.status)
            return None

        def resolve_audio(self):
            source = self.data["audio"]
            path = getattr(audio, source, source)
            if not isinstance(path, str) or not renpy.loadable(path):
                raise ValueError("Audio is unavailable: %s" % source)
            return path

        def beat_at(self, seconds):
            return (seconds - self.data["offset"]) / self.beat

        def stop(self):
            if self.playing:
                self.tick()
            self.playing = False
            renpy.music.stop(channel="asahina_editor", fadeout=0)

        def play_pause(self):
            self.require_developer()
            if self.playing:
                self.stop()
                return
            self.apply_metadata()
            if self.position >= self.data["duration"] - .05:
                self.position = 0.0
            self.started_at = _are_time.perf_counter()
            self.clock = _ARESongClock(self.started_at, self.position)
            self.awaiting_audio = True
            renpy.music.play("<from %.6f>" % self.position + self.resolve_audio(),
                channel="asahina_editor", loop=False, fadeout=0, synchro_start=False)
            self.playing = True
            # The grid and timeline only reschedule themselves while playing.
            renpy.redraw(self.grid, 0)
            renpy.redraw(self.timeline, 0)

        def tick(self):
            if not self.playing:
                return
            now = _are_time.perf_counter()
            position = renpy.music.get_pos(channel="asahina_editor")
            duration = renpy.music.get_duration(channel="asahina_editor")
            # Audio length is a readout until explicitly adopted. The authored
            # chart endpoint can trim an outro; neither choice rescales notes.
            if duration > 0:
                self.measured_duration = duration
            if self.awaiting_audio and position is None and now - self.started_at < .5:
                return
            if self.awaiting_audio:
                self.clock = _ARESongClock(now, self.position)
                self.awaiting_audio = False
            self.position = min(self.data["duration"], self.clock.sample(now, position))
            if self.position >= self.data["duration"]:
                self.playing = False
                renpy.music.stop(channel="asahina_editor", fadeout=0)

        def seek(self, seconds):
            self.require_developer()
            was_playing = self.playing
            self.stop()
            self.position = max(0.0, min(self.data["duration"], float(seconds)))
            self.page_beat = max(0.0, _are_math.floor(self.beat_at(self.position) / 8) * 8.0)
            if was_playing:
                self.play_pause()

        def seek_end(self):
            ends = [note["time"] + note["length"] for note in self.data["notes"]]
            self.seek(max(ends) if ends else self.data["duration"])

        def page(self, direction):
            self.seek(self.position + direction * 8 * self.beat)

        def nudge(self, beats):
            self.seek(self.position + beats * self.beat)

        def step(self, direction):
            grid = self.beat / self.snap
            index = _are_math.floor((self.position - self.data["offset"]) / grid + .5)
            self.seek(self.data["offset"] + (index + direction) * grid)

        def set_snap(self, divisor):
            self.snap = divisor

        def place_at_cursor(self, column):
            self.note(self.position, column % 4, "opponent" if column < 4 else "player", toggle=True)

        def paste_here(self):
            self.paste(self.position)

        def move_selected(self, steps):
            """Ctrl+Up/Down: the selected notes, or the selected effect when no notes are selected."""
            if not self.selection and self.selected_effect() is not None:
                self.move_effect(steps)
            else:
                self.move_selection(steps=steps)

        def move_beats(self, direction):
            self.move_selected(direction * self.snap)

        def step_length(self, direction):
            """[ and ]: the hold length, or the selected effect's length when no notes are selected."""
            if not self.selection and self.selected_effect() is not None:
                self.resize_effect(direction)
            else:
                self.step_hold(direction)

        def step_effect_beats(self, direction):
            """The length a new span effect gets, doubling or halving between 1 and 64 beats."""
            lengths = (1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0)
            if direction > 0:
                self.effect_beats = next((n for n in lengths if n > self.effect_beats + .000001), 64.0)
            else:
                self.effect_beats = next((n for n in reversed(lengths) if n < self.effect_beats - .000001), 1.0)
            self.fx_new_text = are_beats_text(self.effect_beats)
            self.status = "New effects run %s beats." % self.fx_new_text

        def camera_here(self, focus):
            self.set_camera(self.position, focus)

        def toggle_hitsounds(self):
            self.hitsounds = not self.hitsounds

        def toggle_fx_wide(self):
            """Swap between the narrow FX lane and the wide one. The note lanes resize to make room."""
            grid = self.grid
            # A drag's pixel anchors belong to the old geometry.
            grid.cancel_drag()
            grid.hover = grid.fx_hover = grid.fx_hovered = grid.fx_press = None
            persistent.asahina_rhythm_editor_fx_wide = not persistent.asahina_rhythm_editor_fx_wide
            grid.refresh()
            tracks = are_layout().fx_tracks
            self.status = "The FX lane has %d tracks. Ctrl+E makes it %s." % (
                tracks, "narrow again" if persistent.asahina_rhythm_editor_fx_wide else "wide")
            if grid.fx_stacked:
                self.status += " %s share a track with another." % _are_plural(grid.fx_stacked, "effect")

        def charts(self):
            root = "addons/Asahina Rhythm/charts/"
            return sorted(path for path in renpy.list_files()
                if path.startswith(root) and path.endswith(".json") and "/" not in path[len(root):])

        def songs(self):
            extensions = (".ogg", ".opus", ".mp3", ".mp2", ".flac", ".wav")
            paths = sorted(path for path in renpy.list_files() if path.lower().endswith(extensions))
            query = self.search.casefold().strip()
            return [path for path in paths if not query or query in path.casefold()]

        def load_chart(self, path):
            self.require_developer()
            with renpy.open_file(path) as stream:
                chart = self.decode(stream.read(8 * 1024 * 1024 + 1))
            self.stop()
            self.data = chart
            self.saved = _are_copy.deepcopy(chart)
            self.history = []
            self.future = []
            # The clipboard survives on purpose: copy in one chart, paste in another.
            self.selected = None
            self.position = self.page_beat = 0.0
            self.current_path = path
            if hasattr(self, "measured_duration"):
                del self.measured_duration
            self.sync_fields()
            self.status = "Loaded " + path.rsplit("/", 1)[-1]
            renpy.hide_screen("ar_editor_browser")

        def new_song(self, path):
            self.require_developer()
            if path not in self.songs() and not renpy.loadable(path):
                raise ValueError("Choose an existing supported audio file.")
            source = path
            for alias in sorted(vars(audio)):
                if getattr(audio, alias, None) == path and _are_re.fullmatch(r"[A-Za-z0-9_\-]{1,80}", alias):
                    source = alias
                    break
            identifier = _are_re.sub(r"[^A-Za-z0-9_\-]", "_", path.rsplit("/", 1)[-1].rsplit(".", 1)[0])[:72] or "new_song"
            chart = dict(version=1, id=identifier, title=identifier.replace("_", " ").title(),
                audio=source, bpm=120.0, offset=0.0, duration=180.0, notes=[])
            self.stop()
            self.commit(chart)
            self.position = self.page_beat = 0.0
            self.status = "New chart. Set BPM / duration, then play to inspect the audio's measured length."
            self.current_path = None
            if hasattr(self, "measured_duration"):
                del self.measured_duration
            renpy.hide_screen("ar_editor_browser")

        def save_chart(self, export=False):
            self.require_developer()
            path = self.save(_are_os.path.join(config.gamedir, "addons", "Asahina Rhythm", "charts"), export=export)
            ar_editor_refresh_files()
            return path

        def use_audio_duration(self):
            self.duration_text = "%.6f" % self.measured_duration
            self.apply_metadata()

        def apply_field(self, field):
            self.require_developer()
            if field == "hold":
                self.set_hold()
            elif field == "fx":
                self.set_effect_beats()
            elif field == "fx_new":
                self.set_new_effect_beats()
            elif field == "fx_every":
                self.set_repeat_beats()
            else:
                self.apply_metadata()
            renpy.hide_screen("ar_editor_field")

        def request_preview(self, autoplay=False):
            self.require_developer()
            self.apply_metadata()
            self.resolve_audio()
            self.stop()
            renpy.end_interaction(("preview", autoplay))

    class ARChartGrid(renpy.Displayable):
        # Pointer state. A drag is a dict whose "kind" is "box" (select inside a
        # rectangle), "range" (select whole beats from the gutter) or "move".
        # Class defaults keep a grid pickled before these existed working.
        drag = None
        mouse = None
        right_armed = False
        scroll_wall = None
        move_preview = (None, None, None)
        # The FX lane: (effect index, track) per effect, how many effects found no
        # free track, the snapped time under the pointer, and the effect it last hovered.
        fx_layout = ()
        fx_stacked = 0
        fx_hover = None
        fx_hovered = None
        # Lane sprites resized for the wide FX layout, keyed (sprite key, zoom).
        scaled = None
        # A left press on an empty FX spot, as (snapped time, x, y); its release opens the menu.
        fx_press = None

        def __init__(self, editor, **kwargs):
            super(ARChartGrid, self).__init__(**kwargs)
            self.editor = editor
            self.labels = {}
            self.sprites = {}
            self.solids = {}
            self.plan_key = None
            self.plan = []
            self.times = []
            self.longest = 0.0
            self.hover = None
            self.last_hit = None
            for lane in range(4):
                for kind in ("note", "receptor", "confirm"):
                    self._sprite((kind, lane), AR_UI + "small_%s_%d.png" % (kind, lane))
            self._sprite("ring", AR_UI + "select_ring.png")
            for name in ("asahina", "asahiko"):
                self._sprite(("icon", name), AR_UI + "icon_small_%s.png" % name)

        def _sprite(self, key, path):
            if key not in self.sprites:
                self.sprites[key] = (Transform(Image(path), zoom=.5) if renpy.loadable(path)
                                     else Solid("#302944", xysize=(40, 40)))
            return self.sprites[key]

        def _art(self, key, zoom):
            """A lane sprite at the layout's size. The narrow layout draws the sprites as loaded."""
            if zoom == 1.0:
                return self.sprites[key]
            if self.scaled is None:
                self.scaled = {}
            sized = self.scaled.get((key, zoom))
            if sized is None:
                sized = self.scaled[(key, zoom)] = Transform(self.sprites[key], zoom=zoom)
            return sized

        def visit(self):
            return list(self.sprites.values()) + list(self.solids.values()) + list((self.scaled or {}).values())

        def _label(self, text, size=12, color="#c8bfdc", font=None):
            key = (text, size, color, font)
            if key not in self.labels:
                if len(self.labels) > 400:
                    self.labels.clear()
                self.labels[key] = Text(text, font=font or AR_UI_FONT, size=size, color=color, substitute=False)
            return self.labels[key]

        def _blit(self, rv, child, x, y, st, at, alpha=1.0):
            rendered = renpy.render(child, ARE_GRID_W, ARE_GRID_H, st, at)
            width, height = rendered.get_size()
            if alpha < 1:
                wrap = renpy.Render(width, height)
                wrap.blit(rendered, (0, 0))
                rendered = ar_fade(wrap, alpha)
            rv.subpixel_blit(rendered, (x - width / 2.0, y - height / 2.0))

        def _rect(self, rv, color, x, y, width, height, st, at, alpha=1.0):
            if width < .5 or height < .5:
                return
            if color not in self.solids:
                self.solids[color] = Solid(color)
            block = renpy.render(self.solids[color], width, height, st, at)
            if alpha < 1:
                wrap = renpy.Render(width, height)
                wrap.blit(block, (0, 0))
                block = ar_fade(wrap, alpha)
            rv.subpixel_blit(block, (x, y))

        def refresh(self):
            data = self.editor.data
            notes = data["notes"]
            tracks = are_layout().fx_tracks
            # Commits replace the document dict, but a freed id can be reused, so
            # the key also fingerprints the content the plan depends on.
            key = (id(data), data["bpm"], data["offset"], data["duration"], len(notes),
                   sum(n["time"] + 3.1 * n["length"] + .7 * n["lane"] + (n["side"] == "player") for n in notes),
                   tuple((e["time"], e["focus"]) for e in data.get("camera", ())),
                   tuple((e["time"], e["kind"], e["length"]) for e in data.get("effects", ())), tracks)
            if key != self.plan_key:
                self.plan = _are_camera_plan(data)
                self.times = [n["time"] for n in notes]
                self.longest = max([n["length"] for n in notes] or [0.0])
                self.fx_layout, self.fx_stacked = self._pack_effects(data, tracks)
                self.plan_key = key

        def _pack_effects(self, data, tracks):
            """(effect index, track) per effect, and how many found every track busy.

            Overlapping effects of different kinds take side-by-side tracks. With
            every track busy, an effect is drawn over the last one.
            """
            beat = 60.0 / data["bpm"]
            ends = [-1.0] * tracks
            layout = []
            stacked = 0
            for index, effect in enumerate(data.get("effects", ())):
                track = next((t for t in range(tracks) if ends[t] <= effect["time"] + .000001), None)
                if track is None:
                    track = tracks - 1
                    stacked += 1
                # A burst still takes half a beat of room so the next cue can't sit on top of it.
                ends[track] = max(ends[track], effect["time"] + max(effect["length"], beat * .5))
                layout.append((index, track))
            return layout, stacked

        def effect_under(self, x, y):
            """The effect drawn under the pointer in its FX track. Another track's effect doesn't count,
            so an empty track beside a running effect still takes a new one."""
            self.refresh()
            editor = self.editor
            effects = editor.data.get("effects", ())
            seconds = self.seconds_at(y)
            # Bursts are short ticks, so they take a few pixels either way.
            reach = 6.0 / ARE_BEAT_PX * editor.beat
            layout = are_layout()
            track = max(0, min(layout.fx_tracks - 1, int((x - ARE_FX_X) / float(layout.track_w))))
            found = []
            for index, where in self.fx_layout:
                if where != track:
                    continue
                effect = effects[index]
                if effect["kind"] in _ARE_BURSTS:
                    hit = abs(effect["time"] - seconds) <= reach
                else:
                    hit = effect["time"] - reach <= seconds < effect["time"] + effect["length"]
                if hit:
                    found.append((-effect["time"], index))
            return min(found)[1] if found else None

        def focus_at(self, seconds):
            self.refresh()
            index = _are_measure_index(self.editor.data, seconds)
            if not self.plan:
                return "center", False, index
            entry = self.plan[max(0, min(len(self.plan) - 1, index - self.plan[0]["index"]))]
            return entry["focus"], entry["override"], index

        def view_top(self):
            editor = self.editor
            return editor.beat_at(editor.position) - ARE_PLAYHEAD / float(ARE_BEAT_PX)

        def seconds_at(self, y):
            editor = self.editor
            return editor.data["offset"] + (self.view_top() + y / float(ARE_BEAT_PX)) * editor.beat

        def y_at(self, seconds):
            return (self.editor.beat_at(seconds) - self.view_top()) * ARE_BEAT_PX

        def column_at(self, x):
            layout = are_layout()
            for column in range(8):
                left = layout.column_x(column)
                if left <= x < left + layout.lane_w:
                    return column
            return None

        def columns_between(self, x0, x1):
            layout = are_layout()
            low, high = sorted((x0, x1))
            return set(column for column in range(8)
                       if layout.column_x(column) <= high and layout.column_x(column) + layout.lane_w > low)

        def note_under(self, column, y):
            """The note drawn under the pointer: the one on the snapped line, else the nearest head close by."""
            editor = self.editor
            lane, side = column % 4, ("opponent" if column < 4 else "player")
            seconds = self.seconds_at(y)
            index = editor.at(editor.snap_time(seconds), lane, side)
            if index is not None:
                return index
            # Off-grid notes: within half a grid step and never past 10 px, so a
            # click on the next free line still places a note.
            self.refresh()
            reach = min(10.0, ARE_BEAT_PX / (2.0 * editor.snap)) / ARE_BEAT_PX * editor.beat
            notes = editor.data["notes"]
            first = _are_bisect.bisect_left(self.times, seconds - reach)
            last = _are_bisect.bisect_right(self.times, seconds + reach)
            nearby = [(abs(notes[i]["time"] - seconds), i) for i in range(first, last)
                      if notes[i]["lane"] == lane and notes[i]["side"] == side]
            return min(nearby)[1] if nearby else None

        def render(self, width, height, st, at):
            editor = self.editor
            editor.tick()
            self._autoscroll()
            self.refresh()
            data = editor.data
            top = self.view_top()
            bottom = top + ARE_GRID_H / float(ARE_BEAT_PX)
            layout = are_layout()
            lane_w, zoom = layout.lane_w, layout.zoom
            right = layout.column_x(7) + lane_w
            selection = editor.selection
            drag = self.drag if self.drag is not None and self.drag["moved"] else None
            moving = drag is not None and drag["kind"] == "move"

            def y_of(beat):
                return (beat - top) * ARE_BEAT_PX

            rv = renpy.Render(ARE_GRID_W, ARE_GRID_H)
            # Notes and icons straddle the edges; gl2 turns these flags into a clip
            # polygon, so nothing spills onto the header or the timeline.
            rv.xclipping = True
            rv.yclipping = True
            # Canvas colours must be opaque: the canvas writes alpha, it doesn't blend.
            canvas = rv.canvas()
            canvas.rect("#0e0a18", (0, 0, ARE_GRID_W, ARE_GRID_H))
            canvas.rect("#140e22", (0, 0, ARE_GUTTER, ARE_GRID_H))
            # Alternate tracks are shaded so a click can aim at a free one.
            for track in range(layout.fx_tracks):
                canvas.rect("#140f22" if track % 2 else "#110c1d",
                            (ARE_FX_X + track * layout.track_w, 0, layout.track_w, ARE_GRID_H))
            first_measure = int(_are_math.floor(top / 4.0))
            last_measure = int(_are_math.ceil(bottom / 4.0))
            for measure in range(first_measure, last_measure + 1):
                y0, y1 = int(round(y_of(measure * 4))), int(round(y_of(measure * 4 + 4)))
                even = measure % 2 == 0
                canvas.rect("#1c1430" if even else "#171027", (layout.lane_x0, y0, 4 * lane_w, y1 - y0))
                canvas.rect("#12242f" if even else "#0f1d27", (layout.column_x(4), y0, 4 * lane_w, y1 - y0))
            song_start, song_end = y_of(editor.beat_at(0.0)), y_of(editor.beat_at(data["duration"]))
            if song_start > 0:
                canvas.rect("#07050d", (ARE_CAM_X, 0, right - ARE_CAM_X, int(song_start)))
            if song_end < ARE_GRID_H:
                canvas.rect("#07050d", (ARE_CAM_X, max(0, int(song_end)), right - ARE_CAM_X, ARE_GRID_H))
            for column in range(1, 8):
                if column != 4:
                    canvas.line("#261c3a", (layout.column_x(column), 0), (layout.column_x(column), ARE_GRID_H), 1)
            snap = editor.snap
            for step in range(int(_are_math.floor(top * snap)), int(_are_math.ceil(bottom * snap)) + 1):
                y = int(round(y_of(step / float(snap))))
                if step % (snap * 4) == 0:
                    canvas.line("#a48fd0", (ARE_CAM_X, y), (right, y), 2)
                elif step % snap == 0:
                    canvas.line("#4b3e6a", (layout.lane_x0, y), (right, y), 1)
                else:
                    canvas.line("#2a2140", (layout.lane_x0, y), (right, y), 1)

            for measure in range(first_measure, last_measure + 1):
                y = y_of(measure * 4)
                if -24 < y < ARE_GRID_H:
                    rv.blit(renpy.render(self._label("M%d" % (measure + 1), 14, "#f9a3ca", AR_FONT), 80, 24, st, at),
                            (6, int(y) + 3))
                for count in (1, 2, 3):
                    yb = y_of(measure * 4 + count)
                    if 0 <= yb < ARE_GRID_H:
                        rv.blit(renpy.render(self._label(str(count + 1), 11, "#8a7ea6"), 40, 20, st, at), (34, int(yb) - 7))

            # The camera lane: pinned measures are solid, automatic ones tinted.
            if self.plan:
                base = self.plan[0]["index"]
                for measure in range(max(first_measure, base), min(last_measure, base + len(self.plan) - 1) + 1):
                    entry = self.plan[measure - base]
                    y0, y1 = y_of(measure * 4) + 3, y_of(measure * 4 + 4) - 3
                    color = ARE_FOCUS_COLORS[entry["focus"]]
                    if entry["override"]:
                        self._rect(rv, color, ARE_CAM_X + 3, y0, ARE_CAM_W - 6, y1 - y0, st, at)
                    else:
                        self._rect(rv, color, ARE_CAM_X + 3, y0, ARE_CAM_W - 6, y1 - y0, st, at, alpha=.24)
                        self._rect(rv, color, ARE_CAM_X + 3, y0, 3, y1 - y0, st, at)
                    icon_y = min(max(y0, 0) + 17, y1 - 17)
                    centre = ARE_CAM_X + ARE_CAM_W / 2.0
                    if entry["focus"] == "center":
                        self._blit(rv, self.sprites[("icon", "asahina")], centre, icon_y, st, at)
                        self._blit(rv, self.sprites[("icon", "asahiko")], centre, icon_y + 28, st, at)
                    else:
                        self._blit(rv, self.sprites[("icon", AR_CAST[entry["focus"]])], centre, icon_y, st, at)

            self._draw_effects(rv, y_of, st, at)

            for section in data.get("sections", ()):
                try:
                    y = y_of(editor.beat_at(float(section.get("time", 0))))
                except (TypeError, ValueError):
                    continue
                if -2 <= y < ARE_GRID_H:
                    self._rect(rv, "#ffe08a", layout.lane_x0, y, right - layout.lane_x0, 1, st, at, alpha=.7)
                    label = renpy.render(self._label(str(section.get("name", ""))[:30], 11, "#160f24"), 300, 20, st, at)
                    lw, lh = label.get_size()
                    self._rect(rv, "#ffe08a", right - lw - 12, y, lw + 10, lh + 2, st, at)
                    rv.blit(label, (int(right - lw - 7), int(y) + 1))

            # A ghost strumline at the playhead; notes light it as they cross.
            for column in range(8):
                self._blit(rv, self._art(("receptor", column % 4), zoom), layout.column_x(column) + lane_w / 2.0,
                           ARE_PLAYHEAD, st, at, alpha=.40)

            # Box and range selections sit under the notes they pick up.
            if drag is not None and not moving:
                self._draw_area(rv, drag, y_of, right, st, at)

            t_top = data["offset"] + top * editor.beat
            t_bottom = data["offset"] + bottom * editor.beat
            lo = _are_bisect.bisect_left(self.times, t_top - self.longest - .01)
            hi = _are_bisect.bisect_right(self.times, t_bottom + .2)
            for index in range(lo, hi):
                note = data["notes"][index]
                lane = note["lane"]
                column = lane + (4 if note["side"] == "player" else 0)
                left = layout.column_x(column)
                centre = left + lane_w / 2.0
                y = y_of(editor.beat_at(note["time"]))
                chosen = _are_note_key(note) in selection
                # A dragged selection leaves faded originals behind its ghosts.
                fade = .35 if moving and chosen else 1.0
                if note["length"] > 0:
                    y_end = y_of(editor.beat_at(note["time"] + note["length"]))
                    if y_end > -4 and y < ARE_GRID_H + 4:
                        span_top, span_bottom = max(-4.0, y), min(ARE_GRID_H + 4.0, y_end)
                        self._rect(rv, AR_COLORS[lane], centre - 7 * zoom, span_top, 14 * zoom, span_bottom - span_top, st, at, alpha=.75 * fade)
                        self._rect(rv, AR_COLORS[lane], centre - 14 * zoom, y_end - 3, 28 * zoom, 6, st, at, alpha=fade)
                if -40 < y < ARE_GRID_H + 40:
                    if chosen and not moving:
                        self._rect(rv, ARE_SELECT_COLOR, left + 3, y - 17 * zoom, lane_w - 6, 34 * zoom, st, at, alpha=.16)
                        self._blit(rv, self._art("ring", zoom), centre, y, st, at)
                    lit = editor.playing and -.02 <= editor.position - note["time"] <= .10
                    self._blit(rv, self._art(("confirm" if lit else "note", lane), zoom), centre, y, st, at, alpha=fade)

            if moving:
                self._draw_ghosts(rv, drag, y_of, st, at)

            if self.fx_hover is not None and not editor.playing and self.drag is None and self.fx_hovered is None:
                y = y_of(editor.beat_at(self.fx_hover))
                self._rect(rv, ARE_FX_COLORS[editor.effect_kind], ARE_FX_X, y - 1, layout.fx_w, 2, st, at, alpha=.55)

            if self.hover is not None and not editor.playing and self.drag is None:
                column, when = self.hover
                lane, side = column % 4, ("opponent" if column < 4 else "player")
                centre = layout.column_x(column) + lane_w / 2.0
                y = y_of(editor.beat_at(when))
                self._rect(rv, "#ffffff", layout.column_x(column), y - 1, lane_w, 2, st, at, alpha=.30)
                if editor.at(when, lane, side) is None:
                    self._blit(rv, self._art(("note", lane), zoom), centre, y, st, at, alpha=.45)
                else:
                    self._blit(rv, self._art("ring", zoom), centre, y, st, at, alpha=.60)

            self._rect(rv, "#ffe08a", ARE_CAM_X, ARE_PLAYHEAD - 1, right - ARE_CAM_X, 2, st, at)
            self._rect(rv, "#ffe08a", 0, ARE_PLAYHEAD - 10, ARE_GUTTER - 2, 20, st, at)
            measure, within = are_bar_beat(editor, editor.position)
            rv.blit(renpy.render(self._label("%d.%d" % (measure + 1, int(within) + 1), 12, "#160f24"), 60, 20, st, at),
                    (5, ARE_PLAYHEAD - 8))

            if editor.playing and editor.hitsounds:
                if self.last_hit is not None and 0 < editor.position - self.last_hit < .25:
                    if _are_bisect.bisect_right(self.times, editor.position) > _are_bisect.bisect_right(self.times, self.last_hit):
                        renpy.music.play(audio.tick, channel="asahina_editor_hits", loop=False)
                self.last_hit = editor.position
            else:
                self.last_hit = None
            if editor.playing:
                renpy.redraw(self, 0)
            return rv

        def _draw_area(self, rv, drag, y_of, right, st, at):
            editor = self.editor
            if drag["kind"] == "box":
                # Drawn on the edges of the lanes it covers, which is exactly what it
                # selects, so a straight-down drag in one lane still shows a box.
                columns = self.columns_between(drag["x"], self.mouse[0])
                if not columns:
                    return
                layout = are_layout()
                x0, x1 = layout.column_x(min(columns)) + 1, layout.column_x(max(columns)) + layout.lane_w - 1
                y0, y1 = sorted((y_of(editor.beat_at(drag["time"])), self.mouse[1]))
                color = ARE_BOX_COLOR
            elif drag.get("end") is not None:
                x0, x1 = 0, right
                y0, y1 = sorted((y_of(editor.beat_at(drag["time"])), y_of(editor.beat_at(drag["end"]))))
                color = ARE_SELECT_COLOR
            else:
                return
            x0, x1 = max(0, x0), min(ARE_GRID_W, x1)
            y0, y1 = max(-2, y0), min(ARE_GRID_H + 2, y1)
            if x1 - x0 < 1 or y1 - y0 < 1:
                return
            self._rect(rv, color, x0, y0, x1 - x0, y1 - y0, st, at, alpha=.14)
            for bx, by, bw, bh in ((x0, y0, x1 - x0, 1), (x0, y1 - 1, x1 - x0, 1), (x0, y0, 1, y1 - y0), (x1 - 1, y0, 1, y1 - y0)):
                self._rect(rv, color, bx, by, bw, bh, st, at, alpha=.9)

        def _draw_ghosts(self, rv, drag, y_of, st, at):
            editor = self.editor
            shift = drag["steps"] * editor.beat / editor.snap
            blocked = self.move_preview[2] is not None
            layout = are_layout()
            lane_w, zoom = layout.lane_w, layout.zoom
            half = 17 * zoom
            for note in editor.selected_notes():
                column = _are_note_column(note) + drag["columns"]
                if not 0 <= column < 8:
                    continue
                lane = column % 4
                left = layout.column_x(column)
                centre = left + lane_w / 2.0
                y = y_of(editor.beat_at(note["time"] + shift))
                if note["length"] > 0:
                    y_end = y_of(editor.beat_at(note["time"] + shift + note["length"]))
                    if y_end > -4 and y < ARE_GRID_H + 4:
                        span_top, span_bottom = max(-4.0, y), min(ARE_GRID_H + 4.0, y_end)
                        self._rect(rv, AR_COLORS[lane], centre - 7 * zoom, span_top, 14 * zoom, span_bottom - span_top, st, at, alpha=.6)
                if -40 < y < ARE_GRID_H + 40:
                    if blocked:
                        # A refused move: outlined red cells and no selection ring.
                        self._rect(rv, ARE_BLOCKED_COLOR, left + 3, y - half, lane_w - 6, 2 * half, st, at, alpha=.38)
                        for bx, by, bw, bh in ((left + 3, y - half, lane_w - 6, 2), (left + 3, y + half - 2, lane_w - 6, 2),
                                               (left + 3, y - half, 2, 2 * half), (left + lane_w - 5, y - half, 2, 2 * half)):
                            self._rect(rv, ARE_BLOCKED_COLOR, bx, by, bw, bh, st, at)
                        self._blit(rv, self._art(("note", lane), zoom), centre, y, st, at, alpha=.6)
                    else:
                        self._rect(rv, ARE_SELECT_COLOR, left + 3, y - half, lane_w - 6, 2 * half, st, at, alpha=.16)
                        self._blit(rv, self._art("ring", zoom), centre, y, st, at, alpha=.9)
                        self._blit(rv, self._art(("note", lane), zoom), centre, y, st, at, alpha=.85)

        def _draw_effects(self, rv, y_of, st, at):
            """The FX lane: a bar for as long as each effect runs, a short tick for a burst."""
            editor = self.editor
            effects = editor.data.get("effects", ())
            chosen = editor.effect_selected
            width = are_layout().track_w
            drag = self.drag
            dragging = (drag["key"] if drag is not None and drag["kind"] in ("fx_move", "fx_resize")
                        and drag["moved"] and drag["preview"] is not None else None)
            for index, track in self.fx_layout:
                effect = effects[index]
                kind = effect["kind"]
                burst = kind in _ARE_BURSTS
                x = ARE_FX_X + track * width + 1
                color = ARE_FX_COLORS[kind]
                when, span = effect["time"], effect["length"]
                if dragging is not None and _are_effect_key(effect) == dragging:
                    # Where it sits now, faintly, so the move reads as a move.
                    g0 = y_of(editor.beat_at(when)) - (5 if burst else 0)
                    g1 = g0 + 10 if burst else y_of(editor.beat_at(when + span))
                    self._rect(rv, color, x, g0, width - 2, max(2, g1 - g0), st, at, alpha=.16)
                    when, span = drag["preview"]
                y0 = y_of(editor.beat_at(when))
                y1 = y0 + 5 if burst else y_of(editor.beat_at(when + span))
                if burst:
                    y0 -= 5
                if y1 < -2 or y0 > ARE_GRID_H + 2:
                    continue
                if burst:
                    self._rect(rv, color, x, y0, width - 2, y1 - y0, st, at)
                else:
                    self._rect(rv, color, x, y0, width - 2, y1 - y0, st, at, alpha=.45)
                    self._rect(rv, color, x, y0, width - 2, 3, st, at)
                    if y1 - y0 >= 18:
                        mark = ARE_FX_SHORT[kind]
                        if kind in _ARE_REACTIVE:
                            mark = ARE_SIDE_SHORT[effect.get("side", "opponent")] + mark
                        label = renpy.render(self._label(mark, 10, "#ffffff"), 40, 16, st, at)
                        rv.blit(label, (int(x + (width - 2 - label.get_size()[0]) / 2), int(y0) + 4))
                if chosen == _are_effect_key(effect):
                    for bx, by, bw, bh in ((x - 1, y0 - 1, width, 1), (x - 1, y1, width, 1),
                                           (x - 1, y0 - 1, 1, y1 - y0 + 2), (x + width - 2, y0 - 1, 1, y1 - y0 + 2)):
                        self._rect(rv, ARE_SELECT_COLOR, bx, by, bw, bh, st, at)
                    if not burst:
                        # The handle that drags the length, thick enough to aim at.
                        self._rect(rv, ARE_SELECT_COLOR, x - 1, y1 - 2, width, 3, st, at)

        def _autoscroll(self):
            """Scroll while a drag holds the pointer near the top or bottom edge. Paused only."""
            drag, editor = self.drag, self.editor
            if drag is None or not drag["moved"] or self.mouse is None or editor.playing:
                self.scroll_wall = None
                return
            y = self.mouse[1]
            if y < ARE_SCROLL_EDGE:
                speed = -min(3.0, (ARE_SCROLL_EDGE - y) / float(ARE_SCROLL_EDGE))
            elif y > ARE_GRID_H - ARE_SCROLL_EDGE:
                speed = min(3.0, (y - ARE_GRID_H + ARE_SCROLL_EDGE) / float(ARE_SCROLL_EDGE))
            else:
                self.scroll_wall = None
                return
            wall = _are_time.perf_counter()
            if self.scroll_wall is not None:
                # Twelve beats a second at the edge, up to 36 when dragged well past it.
                beats = speed * 12.0 * min(.05, wall - self.scroll_wall)
                editor.position = max(0.0, min(editor.data["duration"], editor.position + beats * editor.beat))
                self._update_drag()
                renpy.redraw(editor.timeline, 0)
            self.scroll_wall = wall
            renpy.redraw(self, 0)

        def _update_drag(self):
            """Re-derive a drag's live result from the pointer; autoscroll calls this too."""
            drag, editor = self.drag, self.editor
            if drag is None or not drag["moved"] or self.mouse is None:
                return
            x, y = self.mouse
            if drag["kind"] in ("fx_move", "fx_resize"):
                self._update_effect_drag(drag, y)
                return
            if drag["kind"] == "move":
                grid = editor.beat / editor.snap
                drag["steps"] = int(round((editor.snap_time(self.seconds_at(y)) - drag["anchor"]) / grid))
                column = self.column_at(x)
                if column is not None:
                    drag["columns"] = column - drag["column"]
                key = (drag["steps"], drag["columns"], id(editor.data), len(editor.selection))
                if self.move_preview[0] != key:
                    if drag["steps"] or drag["columns"]:
                        moved, error = editor.preview_move(drag["steps"], drag["columns"])
                    else:
                        moved, error = None, None
                    self.move_preview = (key, moved, error)
                offset = are_offset_text(drag["steps"], drag["columns"])
                if self.move_preview[2]:
                    editor.status = self.move_preview[2]
                elif offset:
                    editor.status = "Release to move %s %s." % (_are_plural(len(editor.selection), "note"), offset)
                else:
                    editor.status = "Drag to move %s." % _are_plural(len(editor.selection), "note")
                return
            editor.selection = set(drag["base"])
            if drag["kind"] == "box":
                editor.select_range(drag["time"], self.seconds_at(y), self.columns_between(drag["x"], x), add=True)
            else:
                drag["end"] = editor.snap_time(self.seconds_at(y))
                editor.select_range(drag["time"], drag["end"], add=True, include_end=False)

        def _press_effect(self, index, x, y):
            """A press on an effect: its end grabs the length, anywhere else moves the whole thing.

            The grab offset is kept so a long span does not jump its start to the
            pointer, and the key rather than the index survives the commit that
            re-sorts the list on release.
            """
            editor = self.editor
            effect = editor.data["effects"][index]
            kind = "fx_move"
            if effect["kind"] not in _ARE_BURSTS and effect["length"] > 0:
                if abs(y - self.y_at(effect["time"] + effect["length"])) <= ARE_FX_EDGE:
                    kind = "fx_resize"
            return dict(kind=kind, x=x, y=y, moved=False, key=_are_effect_key(effect),
                        grab=self.seconds_at(y) - effect["time"], time=effect["time"],
                        length=effect["length"], preview=None)

        def _update_effect_drag(self, drag, y):
            """Where the dragged effect would land. Clamped here so the preview is what commits."""
            editor = self.editor
            index = editor.effect_index(drag["key"])
            if index is None:
                return
            name = ARE_EFFECT_NAMES[editor.data["effects"][index]["kind"]]
            if drag["kind"] == "fx_move":
                target = editor.snap_time(self.seconds_at(y) - drag["grab"])
                earliest, latest, unused = editor.effect_room(index, target)
                drag["preview"] = (min(max(target, earliest), latest), drag["length"])
                editor.status = "Release to move %s to %s." % (name, are_position(editor, drag["preview"][0]))
            else:
                smallest = editor.beat / editor.snap
                longest = editor.effect_room(index)[2]
                length = max(smallest, min(longest, editor.snap_time(self.seconds_at(y)) - drag["time"]))
                drag["preview"] = (drag["time"], length)
                editor.status = "Release to run %s for %s beats." % (name, are_beats_text(length / editor.beat))

        def _press_lane(self, column, x, y, button, additive):
            editor = self.editor
            index = self.note_under(column, y)
            if button == 3:
                if index is not None:
                    editor.run("delete_note", index)
                return
            seconds = self.seconds_at(y)
            key = None if index is None else _are_note_key(editor.data["notes"][index])
            if additive:
                self.drag = dict(kind="box", x=x, y=y, time=seconds, moved=False, base=set(editor.selection), toggle=key)
            elif key is not None:
                # Pressing an unselected note selects it, so it can be dragged at once.
                if key not in editor.selection:
                    editor.run("select_note", index)
                self.drag = dict(kind="move", x=x, y=y, moved=False, key=key, column=column,
                                 anchor=editor.snap_time(seconds), steps=0, columns=0)
            else:
                self.drag = dict(kind="box", x=x, y=y, time=seconds, moved=False, base=set(),
                                 place=(seconds, column % 4, "opponent" if column < 4 else "player"))

        def _finish_drag(self):
            drag, editor = self.drag, self.editor
            self.drag = None
            self.scroll_wall = None
            self.move_preview = (None, None, None)
            if drag is None:
                return
            if drag["kind"] in ("fx_move", "fx_resize"):
                index = editor.effect_index(drag["key"])
                if drag["moved"] and index is not None and drag["preview"] is not None:
                    when, length = drag["preview"]
                    if drag["kind"] == "fx_move":
                        editor.run("place_effect", index, when)
                    else:
                        editor.run("stretch_effect", index, when + length)
                return
            if drag["kind"] == "move":
                if drag["moved"] and (drag["steps"] or drag["columns"]):
                    editor.run("move_selection", drag["steps"], drag["columns"])
                elif drag["moved"]:
                    editor._selection_changed()
                else:
                    # A click on one note of a group narrows the selection to it.
                    index = editor.index_of(drag["key"])
                    if index is not None:
                        editor.run("select_note", index)
            elif drag["moved"]:
                return
            elif drag["kind"] == "range":
                editor.run("seek", drag["time"])
            elif drag.get("toggle") is not None:
                index = editor.index_of(drag["toggle"])
                if index is not None:
                    editor.run("toggle_selected", index)
            elif drag.get("place") is not None:
                if len(editor.selection) > 1:
                    # The first click away from a group only drops the group.
                    editor.run("clear_selection")
                else:
                    editor.run("note", *drag["place"])

        def cancel_drag(self):
            drag, editor = self.drag, self.editor
            self.drag = None
            self.scroll_wall = None
            self.move_preview = (None, None, None)
            if drag is None:
                return False
            if drag["kind"] in ("box", "range") and drag["moved"]:
                editor.selection = set(drag["base"])
            editor.status = "Drag cancelled."
            renpy.redraw(self, 0)
            return True

        def event(self, ev, x, y, st):
            if not config.developer:
                return None
            editor = self.editor
            inside = 0 <= x < ARE_GRID_W and 0 <= y < ARE_GRID_H
            fx_end = ARE_FX_X + are_layout().fx_w
            if ev.type == _are_pygame.MOUSEMOTION:
                if self.drag is not None:
                    # Only motion with the left button down steers a drag, so a
                    # stray pointer event can't drag the box or the notes around.
                    if getattr(ev, "buttons", (0,))[0]:
                        drag = self.drag
                        self.mouse = (x, y)
                        if not drag["moved"] and max(abs(x - drag["x"]), abs(y - drag["y"])) >= ARE_DRAG_SLOP:
                            drag["moved"] = True
                        self._update_drag()
                        renpy.redraw(self, 0)
                    raise renpy.IgnoreEvent()
                column = self.column_at(x) if inside else None
                hover = None if column is None else (column, editor.snap_time(self.seconds_at(y)))
                in_fx = inside and ARE_FX_X <= x < fx_end
                fx_hover = editor.snap_time(self.seconds_at(y)) if in_fx else None
                under = self.effect_under(x, y) if in_fx else None
                if under is not None and under != self.fx_hovered:
                    effect = editor.data["effects"][under]
                    editor.status = "%s. Drag to move it%s; right-click deletes it." % (
                        editor.effect_text(effect),
                        "" if effect["kind"] in _ARE_BURSTS else ", or drag its end to set its length")
                if hover != self.hover or fx_hover != self.fx_hover or under != self.fx_hovered:
                    self.hover = hover
                    self.fx_hover = fx_hover
                    self.fx_hovered = under
                    renpy.redraw(self, 0)
                return None
            if ev.type == _are_pygame.MOUSEBUTTONUP:
                if ev.button == 3 and self.right_armed:
                    # The grid used this right click, so its release must not
                    # reach the hide-windows binding underneath.
                    self.right_armed = False
                    raise renpy.IgnoreEvent()
                if ev.button == 1 and self.fx_press is not None:
                    # The effect menu opens on the release, as a button does. Opened on
                    # the press, this same release reached the menu's click-outside
                    # button (button_select includes mouseup_1) and closed it at once.
                    when, px, py = self.fx_press
                    self.fx_press = None
                    if inside and ARE_FX_X <= x < fx_end and self.effect_under(x, y) is None:
                        # Whole pixels: event coordinates arrive as floats, and a float
                        # xpos in a screen is a fraction of the screen, not a pixel count.
                        renpy.show_screen("ar_editor_fx_menu", editor=editor, seconds=when,
                                          x=int(ARE_GRID_X + px), y=int(ARE_GRID_Y + py))
                    renpy.restart_interaction()
                    raise renpy.IgnoreEvent()
                if ev.button != 1 or self.drag is None:
                    return None
                self.mouse = (x, y)
                self._update_drag()
                self._finish_drag()
            elif ev.type != _are_pygame.MOUSEBUTTONDOWN or not inside:
                return None
            elif ev.button in (4, 5):
                mods = _are_pygame.key.get_mods()
                editor.run("step" if mods & _are_pygame.KMOD_SHIFT else "nudge", -1 if ev.button == 4 else 1)
                self.hover = None
                self._update_drag()
            elif ev.button in (1, 3):
                self.fx_press = None
                if self.drag is not None:
                    # A release that never arrived (focus lost mid-drag): drop that drag.
                    self.cancel_drag()
                additive = bool(_are_pygame.key.get_mods() & (_are_pygame.KMOD_SHIFT | _are_pygame.KMOD_CTRL))
                self.mouse = (x, y)
                self.hover = None
                self.fx_hover = None
                seconds = self.seconds_at(y)
                column = self.column_at(x)
                if ev.button == 3:
                    self.right_armed = True
                if ARE_CAM_X <= x < ARE_CAM_X + ARE_CAM_W:
                    if ev.button == 1:
                        editor.run("cycle_camera", seconds)
                    else:
                        editor.run("set_camera", seconds, None)
                elif ARE_FX_X <= x < fx_end:
                    index = self.effect_under(x, y)
                    if index is None:
                        if ev.button == 1:
                            # Choosing a kind comes first. The menu opens on the release and
                            # places the effect on this grid line.
                            self.fx_press = (editor.snap_time(seconds), x, y)
                    elif ev.button == 3:
                        editor.run("delete_effect", index)
                    else:
                        # Pressing an effect selects it, so it can be dragged at once.
                        editor.run("select_effect", index)
                        self.drag = self._press_effect(index, x, y)
                elif column is not None:
                    self._press_lane(column, x, y, ev.button, additive)
                elif x < ARE_CAM_X and ev.button == 1:
                    self.drag = dict(kind="range", x=x, y=y, time=editor.snap_time(seconds), end=None, moved=False,
                                     base=set(editor.selection) if additive else set())
            else:
                return None
            renpy.redraw(self, 0)
            renpy.restart_interaction()
            raise renpy.IgnoreEvent()

    class ARChartTimeline(renpy.Displayable):
        def __init__(self, editor, **kwargs):
            super(ARChartTimeline, self).__init__(**kwargs)
            self.editor = editor
            self.marker_key = None
            self.markers = []

        def render(self, width, height, st, at):
            editor = self.editor
            grid = editor.grid
            grid.refresh()
            data = editor.data
            scale = (ARE_GRID_W - 2) / data["duration"]
            rv = renpy.Render(ARE_GRID_W, 44)
            canvas = rv.canvas()
            canvas.rect("#140e22", (0, 0, ARE_GRID_W, 44))
            sections = sorted((s for s in data.get("sections", ()) if isinstance(s.get("time"), (int, float))),
                              key=lambda s: s["time"])
            for i, section in enumerate(sections):
                x0 = int(section["time"] * scale)
                x1 = int(sections[i + 1]["time"] * scale) if i + 1 < len(sections) else ARE_GRID_W
                canvas.rect("#1f1734" if i % 2 else "#191229", (x0, 7, max(1, x1 - x0), 37))
                canvas.line("#3a2d55", (x0, 7), (x0, 44), 1)
            for entry in grid.plan:
                x0, x1 = max(0, int(entry["start"] * scale)), min(ARE_GRID_W, int(entry["end"] * scale))
                if x1 > x0:
                    canvas.rect(ARE_FOCUS_COLORS[entry["focus"]], (x0, 0, x1 - x0, 5))
            for effect in data.get("effects", ()):
                x0 = int(effect["time"] * scale)
                x1 = min(ARE_GRID_W, max(x0 + 2, int((effect["time"] + effect["length"]) * scale)))
                canvas.rect(ARE_FX_COLORS[effect["kind"]], (x0, 37, x1 - x0, 4))
            if self.marker_key != grid.plan_key:
                self.markers = sorted(set((int(n["time"] * scale), n["side"]) for n in data["notes"]))
                self.marker_key = grid.plan_key
            for x, side in self.markers:
                if side == "opponent":
                    canvas.line("#e481c4", (x, 10), (x, 21), 1)
                else:
                    canvas.line("#73ddeb", (x, 23), (x, 34), 1)
            view_start = data["offset"] + grid.view_top() * editor.beat
            view_span = ARE_GRID_H / float(ARE_BEAT_PX) * editor.beat
            vx0 = int(max(0, view_start * scale))
            vx1 = int(min(ARE_GRID_W - 1, (view_start + view_span) * scale))
            if vx1 > vx0:
                canvas.rect("#d9cdea", (vx0, 6, vx1 - vx0, 38), 1)
            x = int(editor.position * scale)
            canvas.line("#ffe08a", (x, 0), (x, 44), 3)
            if editor.playing:
                renpy.redraw(self, .03)
            return rv

        def event(self, ev, x, y, st):
            if not config.developer:
                return None
            editor = self.editor
            inside = 0 <= x <= ARE_GRID_W and 0 <= y <= 44
            # Dragging scrubs while paused; while playing only a click seeks, so the
            # audio is not restarted on every motion event.
            drag = (ev.type == _are_pygame.MOUSEMOTION and inside and ev.buttons[0] and not editor.playing)
            if (ev.type == _are_pygame.MOUSEBUTTONDOWN and ev.button == 1 and inside) or drag:
                editor.run("seek", max(0, x) / float(ARE_GRID_W - 2) * editor.data["duration"])
                renpy.restart_interaction()
                raise renpy.IgnoreEvent()
            return None

    class AREditorEscape(Action):
        """Esc backs out one step at a time: a drag, then the selection, then the studio."""
        def __init__(self, editor):
            self.editor = editor

        def __call__(self):
            editor = self.editor
            if editor.grid.cancel_drag():
                renpy.restart_interaction()
                return None
            if editor.selection or editor.effect_selected is not None:
                editor.run("clear_selection")
                renpy.restart_interaction()
                return None
            return renpy.run(ar_editor_exit_action(editor))

    def ar_editor_exit_action(editor):
        if editor.dirty:
            return Confirm("Discard unsaved chart changes?", Return("close"))
        return Return("close")

    def ar_editor_browser_action(editor, kind):
        action = [Function(editor.stop), SetField(editor, "search", ""), Show("ar_editor_browser", editor=editor, kind=kind)]
        return Confirm("Discard unsaved changes when another chart is selected?", action) if editor.dirty else action

style ar_editor_text is default:
    font AR_UI_FONT
    size 15
    color "#ece4f8"
style ar_editor_frame is default:
    background Solid("#1a1230")
    padding (14, 12)
style ar_editor_button is default:
    background Solid("#2a2040")
    hover_background Solid("#4a3566")
    selected_background Solid("#7a3f6c")
    selected_hover_background Solid("#94507f")
    insensitive_background Solid("#1f182f")
    padding (10, 6)
    hover_sound None
    activate_sound None
style ar_editor_button_text is ar_editor_text:
    size 14
    hover_color "#ffffff"
    selected_color "#ffffff"
    insensitive_color "#6f6485"
style ar_editor_kicker is ar_editor_text:
    size 13
    color "#f9a3ca"
    kerning 2.0
style ar_editor_logo is ar_editor_text:
    font AR_FONT
    size 28
    color "#ffe3f1"
    outlines [(4, "#2a0f3a", 0, 2)]
style ar_editor_side is ar_editor_text:
    font AR_FONT
    size 18
    outlines [(3, "#160f24", 0, 1)]
style ar_editor_dim is ar_editor_text:
    size 13
    color "#a595bd"
style ar_editor_label is ar_editor_text:
    size 14
style ar_editor_hint is ar_editor_text:
    size 12
    color "#9d8fb5"
style ar_editor_keycap is ar_editor_text:
    size 13
    color "#ffe08a"
style ar_editor_clock is ar_editor_text:
    size 30
    color "#ffe08a"
style ar_editor_status is ar_editor_text:
    size 13
    color "#ffe6a4"
style ar_editor_panel_viewport is default
style ar_editor_panel_side is default:
    spacing 2
style ar_editor_panel_vscrollbar is vscrollbar:
    xsize 8
    base_bar Solid("#171024")
    thumb Solid("#4a3769")
    hover_thumb Solid("#f06ba8")
    unscrollable "hide"
style ar_editor_seg is ar_editor_button:
    padding (8, 5)
style ar_editor_seg_text is ar_editor_button_text:
    size 13
style ar_editor_tool is ar_editor_seg:
    xsize 79
style ar_editor_tool_text is ar_editor_seg_text:
    xalign .5
style ar_editor_square is ar_editor_button:
    xysize (34, 30)
    padding (0, 0)
style ar_editor_square_text is ar_editor_button_text:
    size 15
    xalign .5
    yalign .5
style ar_editor_value is ar_editor_button
style ar_editor_value_text is ar_editor_button_text:
    color "#ffe08a"
style ar_editor_play is ar_editor_button:
    background Solid("#f06ba8")
    hover_background Solid("#ff8cc4")
    padding (14, 6)
style ar_editor_play_text is ar_editor_button_text:
    font AR_FONT
    size 16
    color "#ffffff"
style ar_editor_close is ar_editor_button:
    background Solid("#3a2233")
    hover_background Solid("#a8435f")
style ar_editor_close_text is ar_editor_button_text
style ar_editor_link is ar_editor_button:
    background Solid("#23324a")
    hover_background Solid("#2f6f7a")
    padding (8, 4)
style ar_editor_link_text is ar_editor_button_text:
    size 12
    color "#9fe7f1"
style ar_editor_fx_choice is ar_editor_button:
    padding (6, 4)
style ar_editor_lane_toggle is ar_editor_button:
    padding (0, 0)
    ysize 22
style ar_editor_lane_toggle_text is ar_editor_button_text:
    size 12
    color "#9d8fb5"
    hover_color "#ffffff"
    selected_color "#ffffff"
    xalign .5
    yalign .5
style ar_editor_lane_toggle_busy_text is ar_editor_lane_toggle_text:
    color "#ffe08a"
style ar_editor_pill is default:
    padding (10, 4)
style ar_editor_pill_text is ar_editor_text:
    size 13
    color "#160f24"

screen asahina_rhythm_chart_editor_screen(editor):
    modal True
    zorder 200
    style_prefix "ar_editor"
    if config.developer:
        add Solid("#0b0814")
        add Tile(AR_UI + "stripes.png") xysize (1280, 720)
        timer .1 repeat True action Function(editor.tick)
        on "hide" action Function(editor.stop)
        $ notes = editor.data["notes"]
        $ _are_any = bool(editor.selection)
        $ _are_tip = GetTooltip()

        # Keys come before the grid on purpose. Events reach the last child first,
        # so the grid, added last, owns its drags before any button sees them.
        key "K_SPACE" action Function(editor.run, "play_pause")
        key "ctrl_noshift_K_z" action Function(editor.run, "undo")
        key "ctrl_shift_K_z" action Function(editor.run, "undo", True)
        key "ctrl_K_y" action Function(editor.run, "undo", True)
        key "ctrl_K_s" action Function(editor.run, "save_chart")
        key "ctrl_K_c" action Function(editor.run, "copy_selection")
        key "ctrl_K_x" action Function(editor.run, "cut_selection")
        key "ctrl_K_v" action Function(editor.run, "paste_here")
        key "ctrl_K_d" action Function(editor.run, "duplicate_selection")
        key "ctrl_K_a" action Function(editor.run, "select_all")
        key "ctrl_K_m" action Function(editor.run, "mirror_selection")
        key "ctrl_K_f" action Function(editor.run, "flip_sides")
        key "ctrl_K_g" action Function(editor.run, "quantize_selection")
        for _are_number, _are_side in enumerate(ARE_EFFECT_SIDES):
            key ("ctrl_K_%d" % (_are_number + 1)) action Function(editor.run, "set_effect_side", _are_side)
        key "K_DELETE" action Function(editor.run, "delete_selection")
        key "K_BACKSPACE" action Function(editor.run, "delete_selection")
        key "anyrepeat_ctrl_noshift_K_UP" action Function(editor.run, "move_selected", -1)
        key "anyrepeat_ctrl_noshift_K_DOWN" action Function(editor.run, "move_selected", 1)
        key "anyrepeat_ctrl_shift_K_UP" action Function(editor.run, "move_beats", -1)
        key "anyrepeat_ctrl_shift_K_DOWN" action Function(editor.run, "move_beats", 1)
        key "anyrepeat_ctrl_K_LEFT" action Function(editor.run, "move_selection", 0, -1)
        key "anyrepeat_ctrl_K_RIGHT" action Function(editor.run, "move_selection", 0, 1)
        key "anyrepeat_K_LEFTBRACKET" action Function(editor.run, "step_length", -1)
        key "anyrepeat_K_RIGHTBRACKET" action Function(editor.run, "step_length", 1)
        key "K_PAGEUP" action Function(editor.run, "page", -1)
        key "K_PAGEDOWN" action Function(editor.run, "page", 1)
        key "K_HOME" action Function(editor.run, "seek", 0.0)
        key "K_END" action Function(editor.run, "seek_end")
        key "anyrepeat_K_UP" action Function(editor.run, "step", -1)
        key "anyrepeat_K_DOWN" action Function(editor.run, "step", 1)
        for column in range(8):
            key ("alt_K_%d" % (column + 1)) action Function(editor.run, "place_at_cursor", column)
        key "ctrl_K_e" action Function(editor.run, "toggle_fx_wide")
        key "K_F1" action Show("ar_editor_keys")
        key "game_menu" action AREditorEscape(editor)

        # ---- top bar ----
        add Solid("#160f26") xysize (1280, 56)
        add Solid(AR_PINK) ypos 56 xysize (1280, 2)
        text "CHART STUDIO" style "ar_editor_logo" xpos 20 ypos 10
        text ("%s   /   %s" % (editor.data["title"][:28], editor.save_name()[:33])) style "ar_editor_dim" xpos 252 ypos 9 substitute False
        text ("%d notes  •  %d yours  •  %d holds  •  %d camera pins  •  %d effects" % (len(notes), sum(n["side"] == "player" for n in notes), sum(n["length"] > 0 for n in notes), len(editor.data.get("camera", ())), len(editor.data.get("effects", ())))) style "ar_editor_hint" xpos 252 ypos 31
        frame:
            style "ar_editor_pill"
            background Solid("#ffe08a" if editor.dirty else "#5fd8e8")
            xpos 770 ypos 17
            text ("UNSAVED" if editor.dirty else "SAVED") style "ar_editor_pill_text"
        hbox:
            xanchor 1.0 xpos 1264 ypos 12
            spacing 6
            textbutton "Keys" id "ar_editor_keys_button" selected False action Show("ar_editor_keys") tooltip "Every mouse and keyboard shortcut  (F1)"
            textbutton "Load" id "ar_editor_load" selected False action ar_editor_browser_action(editor, "charts") tooltip "Open another chart"
            textbutton "New song" id "ar_editor_new" selected False action ar_editor_browser_action(editor, "songs") tooltip "Start a chart for any audio file in the game"
            textbutton "Save" id "ar_editor_save" action Function(editor.run, "save_chart") tooltip "Save to the charts folder  (Ctrl+S)"
            textbutton "Export" id "ar_editor_export" action Function(editor.run, "save_chart", True) tooltip "Write a copy to charts/exports"
            textbutton "Close" id "ar_editor_back" style "ar_editor_close" action ar_editor_exit_action(editor) tooltip "Leave the studio  (Esc)"

        # ---- left: song, grid and edit cards ----
        viewport:
            style_prefix "ar_editor_panel"
            xpos 16 ypos 70
            xysize (288, 616)
            mousewheel True
            draggable False
            scrollbars "vertical"
            vbox:
                style_prefix "ar_editor"
                xsize 276
                spacing 10
                frame:
                    xfill True
                    vbox:
                        spacing 6
                        text "SONG" style "ar_editor_kicker"
                        textbutton ("Title   " + editor.title_text[:22]) xfill True action Show("ar_editor_field", editor=editor, field="title", title="Song title")
                        textbutton ("ID   " + editor.id_text[:24]) xfill True action Show("ar_editor_field", editor=editor, field="id", title="Filename / chart ID")
                        text ("Audio   " + editor.data["audio"].rsplit("/", 1)[-1][:26]) style "ar_editor_dim"
                        hbox:
                            spacing 6
                            textbutton ("BPM  " + editor.bpm_text[:6]) action Show("ar_editor_field", editor=editor, field="bpm", title="BPM (20-400)")
                            textbutton ("Offset  " + editor.offset_text[:8]) action Show("ar_editor_field", editor=editor, field="offset", title="First beat offset / seconds")
                        textbutton ("Length  " + editor.duration_text[:11] + " s") xfill True action Show("ar_editor_field", editor=editor, field="duration", title="Chart end / seconds")
                        if hasattr(editor, "measured_duration"):
                            textbutton ("Use audio length  %.3f s" % editor.measured_duration) style "ar_editor_link" action Function(editor.run, "use_audio_duration")
                frame:
                    xfill True
                    vbox:
                        spacing 7
                        text "GRID" style "ar_editor_kicker"
                        hbox:
                            spacing 4
                            for divisor, caption in ((1, "1/4"), (2, "1/8"), (3, "1/12"), (4, "1/16"), (8, "1/32")):
                                textbutton caption style "ar_editor_seg" selected editor.snap == divisor action Function(editor.run, "set_snap", divisor)
                        hbox:
                            spacing 6
                            text "Hold" style "ar_editor_label" yalign .5
                            textbutton "-" style "ar_editor_square" action Function(editor.run, "step_hold", -1) tooltip "Shorter hold, one grid step  ([)"
                            textbutton (editor.hold_text + " beats") id "ar_editor_hold" style "ar_editor_value" action Show("ar_editor_field", editor=editor, field="hold", title="Hold length / beats (0 = tap)") tooltip "Type a hold length for the selection or the next note"
                            textbutton "+" style "ar_editor_square" action Function(editor.run, "step_hold", 1) tooltip "Longer hold, one grid step  (])"
                frame:
                    xfill True
                    vbox:
                        spacing 7
                        text "EDIT" style "ar_editor_kicker"
                        grid 3 4:
                            spacing 5
                            textbutton "Undo" style "ar_editor_tool" sensitive bool(editor.history) action Function(editor.run, "undo") tooltip "Undo  (Ctrl+Z)"
                            textbutton "Redo" style "ar_editor_tool" sensitive bool(editor.future) action Function(editor.run, "undo", True) tooltip "Redo  (Ctrl+Y)"
                            textbutton "Delete" id "ar_editor_delete" style "ar_editor_tool" sensitive _are_any action Function(editor.run, "delete_selection") tooltip "Delete the selection  (Delete)"
                            textbutton "Copy" id "ar_editor_copy" style "ar_editor_tool" sensitive _are_any action Function(editor.run, "copy_selection") tooltip "Copy the selection  (Ctrl+C)"
                            textbutton "Cut" id "ar_editor_cut" style "ar_editor_tool" sensitive _are_any action Function(editor.run, "cut_selection") tooltip "Cut the selection  (Ctrl+X)"
                            textbutton "Paste" id "ar_editor_paste" style "ar_editor_tool" sensitive bool(editor.clipboard) action Function(editor.run, "paste_here") tooltip "Paste at the playhead  (Ctrl+V)"
                            textbutton "Duplicate" id "ar_editor_duplicate" style "ar_editor_tool" sensitive _are_any action Function(editor.run, "duplicate_selection") tooltip "Copy the selection into the measures after it  (Ctrl+D)"
                            textbutton "Mirror" style "ar_editor_tool" sensitive _are_any action Function(editor.run, "mirror_selection") tooltip "Mirror the lanes left to right  (Ctrl+M)"
                            textbutton "Swap side" style "ar_editor_tool" sensitive _are_any action Function(editor.run, "flip_sides") tooltip "Give the notes to the other singer  (Ctrl+F)"
                            textbutton "Select all" id "ar_editor_select_all" style "ar_editor_tool" sensitive bool(notes) action Function(editor.run, "select_all") tooltip "Select every note  (Ctrl+A)"
                            textbutton "Deselect" style "ar_editor_tool" sensitive _are_any action Function(editor.run, "clear_selection") tooltip "Clear the selection  (Esc)"
                            textbutton "Snap" style "ar_editor_tool" sensitive _are_any action Function(editor.run, "quantize_selection") tooltip "Snap the selection to the grid  (Ctrl+G)"
        text (_are_tip or "F1 or Keys lists every shortcut.") style "ar_editor_dim" xpos 18 ypos 712 yanchor 1.0 xmaximum 274 substitute False

        # ---- centre: side headers, grid, timeline ----
        $ _are_layout = are_layout()
        $ _are_wide = bool(persistent.asahina_rhythm_editor_fx_wide)
        $ editor.grid.refresh()
        $ _are_stacked = editor.grid.fx_stacked
        if _are_wide:
            $ _are_fx_tip = "Narrow the FX lane to %d tracks  (Ctrl+E)" % ARE_LAYOUTS[0].fx_tracks
        else:
            $ _are_fx_tip = "Widen the FX lane to %d tracks  (Ctrl+E)" % ARE_LAYOUTS[1].fx_tracks
        if _are_stacked:
            $ _are_fx_tip = "%s share a track.  %s" % (_are_plural(_are_stacked, "effect"), _are_fx_tip)
        fixed:
            xpos ARE_GRID_X ypos 64
            xysize (ARE_GRID_W, 58)
            text "CAM" style "ar_editor_hint" xcenter (ARE_CAM_X + ARE_CAM_W // 2) ypos 38
            # The FX header widens or narrows the lane, and turns yellow while effects share a track.
            textbutton ("<  FX" if _are_wide else "FX  >"):
                id "ar_editor_fx_wide"
                style "ar_editor_lane_toggle"
                text_style ("ar_editor_lane_toggle_busy_text" if _are_stacked else "ar_editor_lane_toggle_text")
                xpos ARE_FX_X ypos 34 xsize _are_layout.fx_w
                selected _are_wide
                action Function(editor.run, "toggle_fx_wide")
                tooltip _are_fx_tip
            add AR_UI + "icon_small_asahina.png" zoom .75 xpos _are_layout.lane_x0 ypos 8
            text "ASAHINA" style "ar_editor_side" color AR_PINK xpos (_are_layout.lane_x0 + 46) ypos 16
            add AR_UI + "icon_small_asahiko.png" zoom .75 xpos _are_layout.column_x(4) ypos 8
            text "YOU" style "ar_editor_side" color AR_CYAN xpos (_are_layout.column_x(4) + 46) ypos 16
        add editor.timeline id "ar_editor_timeline" xpos ARE_GRID_X ypos 646
        text editor.status style "ar_editor_status" xpos ARE_GRID_X ypos 698 xmaximum ARE_GRID_W substitute False

        # ---- right: playback, camera, selection ----
        viewport:
            style_prefix "ar_editor_panel"
            xpos 1022 ypos 70
            xysize (248, 640)
            mousewheel True
            draggable False
            scrollbars "vertical"
            vbox:
                style_prefix "ar_editor"
                xsize 236
                spacing 8
                frame:
                    xfill True
                    vbox:
                        spacing 6
                        text "PLAYBACK" style "ar_editor_kicker"
                        text are_clock(editor.position) style "ar_editor_clock"
                        $ _are_measure, _are_within = are_bar_beat(editor, editor.position)
                        text ("of %s   •   M%d  beat %.2f" % (are_clock(editor.data["duration"]), _are_measure + 1, _are_within + 1)) style "ar_editor_dim"
                        hbox:
                            spacing 4
                            textbutton "|<" style "ar_editor_square" action Function(editor.run, "seek", 0.0) tooltip "Back to the start  (Home)"
                            textbutton "-8" style "ar_editor_square" action Function(editor.run, "page", -1) tooltip "Eight beats back  (Page Up)"
                            textbutton ("PAUSE" if editor.playing else "PLAY") id "ar_editor_play" style "ar_editor_play" action Function(editor.run, "play_pause") tooltip "Play or pause  (Space)"
                            textbutton "+8" style "ar_editor_square" action Function(editor.run, "page", 1) tooltip "Eight beats on  (Page Down)"
                        textbutton ("Hitsounds  ON" if editor.hitsounds else "Hitsounds  OFF") xfill True selected editor.hitsounds action Function(editor.run, "toggle_hitsounds")
                        hbox:
                            spacing 6
                            textbutton "Test here" id "ar_editor_test" action Function(editor.run, "request_preview", False) tooltip "Play the chart from the playhead"
                            textbutton "Auto here" id "ar_editor_auto" action Function(editor.run, "request_preview", True) tooltip "Watch autoplay from the playhead"
                frame:
                    xfill True
                    vbox:
                        spacing 6
                        text "CAMERA" style "ar_editor_kicker"
                        $ _are_focus, _are_pinned, _are_index = editor.grid.focus_at(editor.position)
                        $ _are_here = editor.camera_override(editor.position)
                        text ("M%d frames %s" % (_are_index + 1, ARE_FOCUS_NAMES[_are_focus])) style "ar_editor_label" color ARE_FOCUS_COLORS[_are_focus]
                        text ("pinned" if _are_pinned else "automatic: follows the notes") style "ar_editor_hint"
                        grid 2 2:
                            spacing 4
                            for _are_option in (None, "opponent", "player", "center"):
                                textbutton ARE_FOCUS_NAMES[_are_option] style "ar_editor_seg" xsize 100 selected _are_here == _are_option action Function(editor.run, "camera_here", _are_option)
                frame:
                    xfill True
                    vbox:
                        spacing 4
                        text "SELECTION" style "ar_editor_kicker"
                        $ _are_stats = editor.selection_stats()
                        $ _are_effect = editor.selected_effect()
                        if _are_stats is None and _are_effect is not None:
                            text ARE_EFFECT_NAMES[_are_effect["kind"]].upper() style "ar_editor_label" color ARE_FX_COLORS[_are_effect["kind"]]
                            text ("%.3f s   •   %s" % (_are_effect["time"], are_position(editor, _are_effect["time"]))) style "ar_editor_dim"
                            if _are_effect["kind"] in _ARE_REACTIVE:
                                hbox:
                                    spacing 4
                                    for _are_side in ARE_EFFECT_SIDES:
                                        textbutton ARE_SIDE_NAMES[_are_side] id ("ar_editor_fx_side_" + _are_side) style "ar_editor_seg" xsize 66 selected _are_effect.get("side", "opponent") == _are_side action Function(editor.run, "set_effect_side", _are_side) tooltip "Whose notes set it off"
                            if _are_effect["kind"] in _ARE_BURSTS:
                                text "One moment, so no length" style "ar_editor_dim"
                            else:
                                hbox:
                                    spacing 4
                                    textbutton "-" id "ar_editor_fx_shorter" style "ar_editor_square" action Function(editor.run, "resize_effect", -1, True) tooltip "One beat shorter  ([ for a grid step)"
                                    textbutton ("%s beats" % are_beats_text(_are_effect["length"] / editor.beat)) id "ar_editor_fx_beats" style "ar_editor_value" xminimum 84 action [SetField(editor, "fx_text", are_beats_text(_are_effect["length"] / editor.beat)), Show("ar_editor_field", editor=editor, field="fx", title="Effect length / beats")] tooltip "Type how many beats it runs"
                                    textbutton "+" id "ar_editor_fx_longer" style "ar_editor_square" action Function(editor.run, "resize_effect", 1, True) tooltip "One beat longer  (] for a grid step)"
                            hbox:
                                spacing 4
                                textbutton "Earlier" id "ar_editor_fx_earlier" style "ar_editor_seg" action Function(editor.run, "move_effect", -1) tooltip "One grid step earlier  (Ctrl+Up)"
                                textbutton "Later" id "ar_editor_fx_later" style "ar_editor_seg" action Function(editor.run, "move_effect", 1) tooltip "One grid step later  (Ctrl+Down)"
                                textbutton "Delete" id "ar_editor_fx_delete" style "ar_editor_seg" action Function(editor.run, "delete_effect") tooltip "Delete the effect  (Delete)"
                            if _are_effect["kind"] not in _ARE_BURSTS:
                                textbutton "Whole song" id "ar_editor_fx_whole" style "ar_editor_seg" xfill True action Function(editor.run, "whole_song_effect") tooltip "Run it from the start of the song to the end, replacing every other span of its kind"
                            hbox:
                                spacing 4
                                text "Every" style "ar_editor_label" yalign .5
                                textbutton editor.fx_every_text id "ar_editor_fx_every" style "ar_editor_value" xminimum 40 substitute False action Show("ar_editor_field", editor=editor, field="fx_every", title="Repeat gap / beats") tooltip "Type the gap between copies, in beats"
                                textbutton "Repeat" id "ar_editor_fx_repeat" style "ar_editor_seg" action Function(editor.run, "repeat_effect") tooltip "Copy it every few beats to the end of the song"
                        elif _are_stats is None:
                            text "Nothing selected" style "ar_editor_label"
                            text "Click a note or an effect, or drag across the grid." style "ar_editor_hint"
                        elif _are_stats["count"] == 1:
                            $ _are_note = editor.selected_notes()[0]
                            text ("%s   %s" % ("ASAHINA" if _are_note["side"] == "opponent" else "YOU", AR_POSES[_are_note["lane"]].upper())) style "ar_editor_label" color AR_COLORS[_are_note["lane"]]
                            text ("%.3f s   •   %s" % (_are_note["time"], are_position(editor, _are_note["time"]))) style "ar_editor_dim"
                            text ("hold %s beats" % are_beats_text(_are_note["length"] / editor.beat)) style "ar_editor_dim"
                        else:
                            text ("%d notes" % _are_stats["count"]) style "ar_editor_label" color ARE_SELECT_COLOR
                            text ("%d Asahina   •   %d you" % (_are_stats["opponent"], _are_stats["player"])) style "ar_editor_dim"
                            text ("%s  •  %s to %s" % (_are_plural(_are_stats["holds"], "hold"), are_position(editor, _are_stats["start"]), are_position(editor, _are_stats["end"]))) style "ar_editor_dim"
                        add Solid("#2e2447") xysize (208, 1)
                        if editor.clipboard:
                            text ("Clipboard   %s, %s beats" % (_are_plural(len(editor.clipboard), "note"), are_beats_text(editor.clipboard_beats()))) style "ar_editor_hint"
                        else:
                            text "Clipboard empty" style "ar_editor_hint"

        # Added last, so it is the first to see every mouse event.
        add editor.grid id "ar_editor_grid" xpos ARE_GRID_X ypos ARE_GRID_Y

screen ar_editor_keys():
    modal True
    zorder 230
    style_prefix "ar_editor"
    if config.developer:
        add Solid("#07040ee6")
        frame:
            xalign .5 yalign .5 xsize 1180
            padding (28, 22)
            vbox:
                spacing 14
                add Solid(AR_PINK) xysize (1124, 3)
                fixed:
                    xysize (1124, 36)
                    text "SHORTCUTS" style "ar_editor_side" color "#ffe3f1" yalign .5
                    textbutton "Close" id "ar_editor_keys_close" style "ar_editor_close" xpos 1.0 xanchor 1.0 yalign .5 action Hide("ar_editor_keys")
                hbox:
                    spacing 28
                    for _are_title, _are_rows in ARE_SHORTCUTS:
                        vbox:
                            xsize 356
                            spacing 6
                            text _are_title style "ar_editor_kicker"
                            for _are_keys, _are_what in _are_rows:
                                hbox:
                                    spacing 10
                                    text _are_keys style "ar_editor_keycap" xsize 136 substitute False
                                    text _are_what style "ar_editor_hint" xsize 210 substitute False
                text "With several notes selected, the first click on empty grid clears the selection instead of placing a note." style "ar_editor_hint"
        key "K_F1" action Hide("ar_editor_keys")
        key "game_menu" action Hide("ar_editor_keys")

screen ar_editor_fx_menu(editor, seconds, x, y):
    # Opened by a click on an empty spot in the FX lane: pick what to place there.
    modal True
    zorder 225
    style_prefix "ar_editor"
    if config.developer:
        button:
            xysize (1280, 720)
            background None
            hover_background None
            action Hide("ar_editor_fx_menu")
            alternate Hide("ar_editor_fx_menu")
        frame:
            # One column per group. The palette is grouped rather than listed
            # because the groups do different jobs: a chart that wants the dread
            # set almost never wants a confetti cannon in the same measure, and
            # reading down one column is how you find that out. Four columns of
            # at most fourteen also keeps the panel shorter than the screen,
            # which two columns of nineteen would not have.
            xpos int(min(x + 14, 1280 - 604)) ypos int(max(8, min(y - 40, 720 - 604)))
            xsize 592
            padding (12, 10)
            vbox:
                spacing 6
                text ("ADD EFFECT AT %s" % are_position(editor, seconds)) style "ar_editor_kicker"
                hbox:
                    spacing 8
                    for _are_group, _are_kinds in ARE_EFFECT_GROUPS:
                        vbox:
                            spacing 4
                            text _are_group style "ar_editor_label"
                            for kind in _are_kinds:
                                button:
                                    id ("ar_editor_fx_choice_" + kind)
                                    style "ar_editor_fx_choice"
                                    xysize (136, 26)
                                    selected kind == editor.effect_kind
                                    tooltip ARE_FX_HINTS[kind]
                                    action [Hide("ar_editor_fx_menu"), Function(editor.run, "add_effect", seconds, kind)]
                                    hbox:
                                        spacing 6
                                        add Solid(ARE_FX_COLORS[kind]) xysize (8, 16) yalign .5
                                        text ARE_EFFECT_NAMES[kind] style "ar_editor_button_text" yalign .5
                hbox:
                    spacing 6
                    text "Answers" style "ar_editor_label" yalign .5
                    for _are_side in ARE_EFFECT_SIDES:
                        textbutton ARE_SIDE_NAMES[_are_side] id ("ar_editor_fx_menu_side_" + _are_side) style "ar_editor_seg" xsize 74 selected editor.effect_side == _are_side action Function(editor.run, "set_effect_side", _are_side) tooltip "Whose notes set a reactive effect off: Quake, Strobe, Lunge, Shockwave, Recoil, Fracture"
                hbox:
                    spacing 6
                    text "New span length" style "ar_editor_label" yalign .5
                    textbutton "-" id "ar_editor_fx_menu_shorter" style "ar_editor_square" action Function(editor.run, "step_effect_beats", -1)
                    textbutton ("%s beats" % editor.fx_new_text) id "ar_editor_fx_menu_beats" style "ar_editor_value" xminimum 78 substitute False action Show("ar_editor_field", editor=editor, field="fx_new", title="New effect length / beats") tooltip "Type how many beats a new effect runs"
                    textbutton "+" id "ar_editor_fx_menu_longer" style "ar_editor_square" action Function(editor.run, "step_effect_beats", 1)
                $ _are_fx_tip = GetTooltip()
                text (_are_fx_tip or "Flash, Confetti, Sparks, Cut, Tear, Glimpse and Invert happen at one moment.") style "ar_editor_hint" xmaximum 568 substitute False
        key "game_menu" action Hide("ar_editor_fx_menu")

screen ar_editor_field(editor, field, title):
    modal True
    # Above the FX menu at 225, so a length can be typed without closing it.
    zorder 230
    style_prefix "ar_editor"
    default original_value = getattr(editor, field + "_text")
    if config.developer:
        add Solid("#07040ecc")
        frame:
            xalign .5 yalign .5 xsize 580
            padding (26, 22)
            vbox:
                spacing 16
                add Solid(AR_PINK) xysize (528, 3)
                text title style "ar_editor_side" color "#ffe3f1"
                frame:
                    background Solid("#0b0814")
                    padding (12, 10)
                    xfill True
                    input value FieldInputValue(editor, field + "_text") length (110 if field == "title" else 80 if field == "id" else 16) font "DejaVuSans.ttf" size 21 color "#ffffff"
                if field == "fx":
                    text "How many beats the selected effect runs. It stops short if it reaches the next one of its kind." style "ar_editor_hint" xmaximum 520
                elif field == "fx_new":
                    text "How many beats an effect placed from the FX menu runs." style "ar_editor_hint" xmaximum 520
                elif field == "fx_every":
                    text "The gap between copies that Repeat places, to the end of the song." style "ar_editor_hint" xmaximum 520
                elif field != "hold":
                    text "BPM and offset adjust the grid; existing notes keep their times." style "ar_editor_hint" xmaximum 520
                elif len(editor.selection) > 1:
                    text "Every selected note gets this hold when you apply." style "ar_editor_hint" xmaximum 520
                elif editor.selection:
                    text "The selected note changes when you apply." style "ar_editor_hint" xmaximum 520
                else:
                    text "The next note you place gets this hold." style "ar_editor_hint" xmaximum 520
                hbox:
                    spacing 10
                    textbutton "Apply" id "ar_editor_field_apply" style "ar_editor_play" action Function(editor.run, "apply_field", field)
                    textbutton "Cancel" id "ar_editor_field_cancel" action [SetField(editor, field + "_text", original_value), Hide("ar_editor_field")]
        key "K_RETURN" action Function(editor.run, "apply_field", field)
        key "game_menu" action [SetField(editor, field + "_text", original_value), Hide("ar_editor_field")]

screen ar_editor_browser(editor, kind):
    modal True
    zorder 220
    style_prefix "ar_editor"
    if config.developer:
        add Solid("#07040edd")
        frame:
            xalign .5 yalign .5 xsize 1020 ysize 610
            padding (24, 20)
            vbox:
                spacing 12
                add Solid(AR_PINK) xysize (972, 3)
                text ("LOAD CHART" if kind == "charts" else "NEW CHART  /  CHOOSE AUDIO") style "ar_editor_side" color "#ffe3f1"
                if kind == "songs":
                    hbox:
                        spacing 12
                        text "Search" style "ar_editor_label" yalign .5
                        frame:
                            background Solid("#0b0814")
                            padding (10, 6)
                            input value FieldInputValue(editor, "search") length 100 font "DejaVuSans.ttf" size 18 color "#ffffff" xsize 800
                viewport:
                    ysize 440
                    scrollbars "vertical"
                    mousewheel True
                    draggable False
                    vbox:
                        spacing 4
                        for path in (editor.charts() if kind == "charts" else editor.songs()):
                            textbutton path text_size 14 xfill True action Function(editor.run, "load_chart" if kind == "charts" else "new_song", path)
                textbutton "Cancel" action Hide("ar_editor_browser")
        key "game_menu" action Hide("ar_editor_browser")

init python:
    def ar_editor_chart_path(chart_id=None):
        """The chart file the studio opens: charts/<id>.json, else the file holding that ID, else the first chart."""
        root = AR_ROOT + "charts/"
        files = sorted(path for path in renpy.list_files()
                       if path.startswith(root) and path.endswith(".json") and "/" not in path[len(root):])
        if chart_id:
            if root + chart_id + ".json" in files:
                return root + chart_id + ".json"
            for path in files:
                try:
                    with renpy.open_file(path) as stream:
                        if ar_json.loads(stream.read().decode("utf-8-sig")).get("id") == chart_id:
                            return path
                except (IOError, OSError, ValueError):
                    continue
        return files[0] if files else None

# are_chart_id: the song to open, as song select passes it. None opens the first chart.
label asahina_rhythm_chart_editor(are_chart_id=None):
    if not config.developer:
        return
    $ renpy.block_rollback()
    python:
        _are_path = ar_editor_chart_path(are_chart_id)
        if _are_path:
            with renpy.open_file(_are_path) as _are_file:
                _are_chart = _ARChartDocument.decode(_are_file.read())
        else:
            # No charts yet: a placeholder document, with the audio browser open to start a real one.
            _are_chart = dict(version=1, id="new_song", title="New Song", audio="asarhythm_menu",
                              bpm=120.0, offset=0.0, duration=180.0, notes=[])
        _are_editor = ARChartEditor(_are_chart)
        # Every song keeps one file, charts/<id>.json. Save writes there, and moves a
        # chart that was opened from a differently named file.
        _are_editor.current_path = _are_path
        if not _are_path:
            renpy.show_screen("ar_editor_browser", editor=_are_editor, kind="songs")
        _are_previous_music = renpy.music.get_playing(channel="music")
        _are_previous_pause = renpy.music.get_pause(channel="music")
        renpy.music.set_pause(True, channel="music")
    $ _are_done = False
    while not _are_done:
        call screen asahina_rhythm_chart_editor_screen(_are_editor)
        if _return == "close":
            $ _are_done = True
        else:
            $ _are_autoplay = _return[1]
            call asahina_rhythm_editor_preview(_are_editor.data, start_time=_are_editor.position, autoplay=_are_autoplay) from _call_asahina_rhythm_editor_preview
    $ _are_editor.stop()
    $ renpy.music.set_pause(_are_previous_pause, channel="music")
    $ renpy.block_rollback()
    return
