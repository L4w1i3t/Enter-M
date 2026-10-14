"""Developer chart document operations, independent of Ren'Py's UI."""
import bisect
import copy
import json
import math
import os
import re
import tempfile

from asahina_rhythm_core import (BURST_EFFECTS, CAMERA_FOCI, EFFECT_KINDS, EFFECT_SIDES,
                                 REACTIVE_EFFECTS, measure_index, normalize_chart)

SIDES = ("opponent", "player")
EMPTY_SELECTION = "Select some notes first: click one, or drag across the grid."
EFFECT_NAMES = {"fanfare": "Fanfare", "spotlights": "Spotlights", "lasers": "Lasers", "haze": "Haze",
                "blackout": "Blackout", "pulse": "Pulse", "crowd": "Crowd", "flash": "Flash",
                "confetti": "Confetti", "sparks": "Sparks", "quake": "Quake", "strobe": "Strobe",
                "lunge": "Lunge", "shockwave": "Shockwave",
                "dread": "Dread", "watchers": "Watchers", "static": "Static", "hollow": "Hollow",
                "footlights": "Footlights", "rot": "Rot", "arrhythmia": "Arrhythmia",
                "doubles": "Doubles", "gutter": "Gutter", "recoil": "Recoil",
                "fracture": "Fracture", "cut": "Cut", "tear": "Tear", "glimpse": "Glimpse",
                "veins": "Veins", "blood": "Blood", "convulse": "Convulse", "redwash": "Red Wash",
                "invert": "Invert", "negative": "Negative", "infrared": "Infrared",
                "fried": "Deep Fried", "bitcrush": "Bitcrush"}
# The four groups the Chart Studio's add menu lays out as columns. They are
# slices, so a kind appended to EFFECT_KINDS lands in the last group unless a
# boundary moves with it.
CONCERT_KINDS = EFFECT_KINDS[:14]
DREAD_KINDS = EFFECT_KINDS[14:28]
BODY_KINDS = EFFECT_KINDS[28:32]
SIGNAL_KINDS = EFFECT_KINDS[32:]
EFFECT_GROUPS = (("CONCERT", CONCERT_KINDS), ("DREAD", DREAD_KINDS),
                 ("BODY", BODY_KINDS), ("SIGNAL", SIGNAL_KINDS))
# Whose notes set a reactive effect off, as the panel says it.
SIDE_NAMES = {"opponent": "Asahina", "player": "You", "both": "Both"}


def note_key(note):
    """A note's identity. Two notes can never share a lane at the same moment."""
    return (round(note["time"], 6), note["side"], note["lane"])


def effect_key(effect):
    """An effect's identity. Two effects of one kind never start at the same moment."""
    return (round(effect["time"], 6), effect["kind"])


def note_column(note):
    """Grid column: 0-3 are Asahina's lanes, 4-7 the player's."""
    return note["lane"] + 4 * SIDES.index(note["side"])


def collides(first, second):
    """normalize_chart's same-lane rule: a tap occupies a millisecond, a hold its length."""
    return (first["side"] == second["side"] and first["lane"] == second["lane"] and
            first["time"] < second["time"] + max(.001, second["length"]) - .000001 and
            second["time"] < first["time"] + max(.001, first["length"]) - .000001)


def blocking_notes(incoming, existing):
    """The notes in ``existing`` that any note in ``incoming`` would overlap, searched lane by lane."""
    lanes = {}
    for note in sorted(existing, key=lambda n: n["time"]):
        lanes.setdefault((note["side"], note["lane"]), []).append(note)
    starts = {key: [note["time"] for note in lane] for key, lane in lanes.items()}
    reach = {key: max(max(.001, note["length"]) for note in lane) for key, lane in lanes.items()}
    blocked = {}
    for note in incoming:
        key = (note["side"], note["lane"])
        if key not in lanes:
            continue
        lane = lanes[key]
        index = bisect.bisect_left(starts[key], note["time"] + max(.001, note["length"]))
        # Walk back only as far as the lane's longest hold could reach.
        while index > 0:
            index -= 1
            other = lane[index]
            if other["time"] + reach[key] < note["time"]:
                break
            if collides(other, note):
                blocked[id(other)] = other
    return list(blocked.values())


def plural(count, word):
    return "%d %s%s" % (count, word, "" if count == 1 else "s")


def beats_text(beats):
    """A beat count as people type it: 2, 0.5, 0.333; never 2.000."""
    return ("%.3f" % beats).rstrip("0").rstrip(".") or "0"


class ChartDocument:
    # Class defaults keep a document pickled before these fields existed (a hot
    # reload mid-session) working. They are only ever replaced, never mutated.
    selection = frozenset()
    clipboard = ()
    # The selected effect's key. One thing is selected at a time: selecting an
    # effect drops the note selection, and selecting notes drops the effect.
    effect_selected = None
    # The kind the FX menu offers first, and a new span effect's length in beats.
    effect_kind = "spotlights"
    effect_beats = 8.0
    effect_side = "opponent"
    # Typed beat counts: the selected span's length, the length a newly placed
    # span gets, and the gap between repeats. The first two are separate numbers
    # on purpose: the FX menu sets what comes next without touching a selection.
    fx_text = "8"
    fx_new_text = "8"
    fx_every_text = "4"

    def __init__(self, chart, developer_check=None):
        self.developer_check = developer_check or (lambda: False)
        self.data = normalize_chart(chart)
        self.saved = copy.deepcopy(self.data)
        self.history = []
        self.future = []
        # Note keys, not indices: every commit re-sorts the note list.
        self.selection = set()
        # Copied notes relative to the first one, in beats, so a paste keeps its
        # musical spacing in a chart with a different tempo.
        self.clipboard = []
        self.position = 0.0
        self.page_beat = 0.0
        self.snap = 4
        self.hold_text = "0"
        self.fx_text = beats_text(self.effect_beats)
        self.fx_new_text = beats_text(self.effect_beats)
        self.fx_every_text = "4"
        self.status = "Click places or selects a note; drag selects. F1 lists every shortcut."
        self.current_path = None
        self.sync_fields()

    def require_developer(self):
        if not self.developer_check():
            raise PermissionError("The chart editor is available only in developer mode.")

    @property
    def beat(self):
        return 60.0 / self.data["bpm"]

    @property
    def dirty(self):
        return self.data != self.saved or any(str(getattr(self, key + "_text")) != str(self.data[key])
            for key in ("id", "title", "bpm", "offset", "duration"))

    def sync_fields(self):
        for key in ("id", "title", "bpm", "offset", "duration"):
            setattr(self, key + "_text", str(self.data[key]))

    def commit(self, candidate):
        self.require_developer()
        candidate = normalize_chart(candidate)
        if candidate != self.data:
            self.history.append(copy.deepcopy(self.data))
            self.history = self.history[-80:]
            self.future = []
            self.data = candidate
            self.selection = set()
        self.sync_fields()

    def apply_metadata(self):
        candidate = copy.deepcopy(self.data)
        for key in ("id", "title"):
            candidate[key] = getattr(self, key + "_text").strip()
        for key in ("bpm", "offset", "duration"):
            try:
                candidate[key] = float(getattr(self, key + "_text"))
            except (ValueError, TypeError):
                raise ValueError("%s must be a number." % key.capitalize())
        selection = set(self.selection)
        self.commit(candidate)
        # Metadata never moves notes, so the selection is still valid.
        self.selection = selection & {note_key(note) for note in self.data["notes"]}
        self.position = min(self.position, self.data["duration"])
        self.status = "Metadata applied. BPM and offset move the grid; note times stay fixed."

    def undo(self, redo=False):
        self.require_developer()
        source, target = (self.future, self.history) if redo else (self.history, self.future)
        if source:
            target.append(copy.deepcopy(self.data))
            self.data = source.pop()
            self.selection = set()
            self.effect_selected = None
            self.sync_fields()
            self.status = "Redone." if redo else "Undone."

    def snap_time(self, seconds):
        grid = self.beat / self.snap
        steps = math.floor((seconds - self.data["offset"]) / grid + .5)
        return round(max(0, min(self.data["duration"], self.data["offset"] + steps * grid)), 6)

    def tidy_time(self, seconds):
        """Round to microseconds, pulling float drift of up to 5 us back onto the nearest grid line."""
        line = self.snap_time(seconds)
        return line if abs(line - seconds) <= .000005 else round(seconds, 6)

    def at(self, seconds, lane, side):
        tolerance = min(.060, self.beat / self.snap * .46)
        matches = [(abs(note["time"] - seconds), index) for index, note in enumerate(self.data["notes"])
                   if note["lane"] == lane and note["side"] == side and abs(note["time"] - seconds) <= tolerance]
        return min(matches)[1] if matches else None

    # ---- selection ------------------------------------------------------------

    @property
    def selected(self):
        """The index of the one selected note, for single-note tools; None otherwise."""
        if len(self.selection) != 1:
            return None
        indices = self.selected_indices()
        return indices[0] if indices else None

    @selected.setter
    def selected(self, index):
        self.selection = set() if index is None else {note_key(self.data["notes"][index])}
        self.effect_selected = None

    def selected_indices(self):
        return [index for index, note in enumerate(self.data["notes"]) if note_key(note) in self.selection]

    def selected_notes(self):
        return [self.data["notes"][index] for index in self.selected_indices()]

    def index_of(self, key):
        for index, note in enumerate(self.data["notes"]):
            if note_key(note) == key:
                return index
        return None

    def selection_stats(self):
        chosen = self.selected_notes()
        if not chosen:
            return None
        return dict(count=len(chosen), opponent=sum(note["side"] == "opponent" for note in chosen),
                    player=sum(note["side"] == "player" for note in chosen),
                    holds=sum(note["length"] > 0 for note in chosen), start=chosen[0]["time"],
                    end=max(note["time"] + note["length"] for note in chosen))

    def clipboard_beats(self):
        return max([item["beats"] + item["hold"] for item in self.clipboard] or [0.0])

    def _selection_changed(self):
        chosen = self.selected_notes()
        if chosen:
            self.effect_selected = None
        if len(chosen) == 1:
            self.hold_text = beats_text(chosen[0]["length"] / self.beat)
        self.status = (plural(len(chosen), "note") + " selected.") if chosen else "Nothing selected."

    def select_note(self, index):
        self.selected = index
        note = self.data["notes"][index]
        self.hold_text = beats_text(note["length"] / self.beat)
        self.status = "Selected %s lane %d at %.3fs." % (note["side"], note["lane"] + 1, note["time"])

    def toggle_selected(self, index):
        self.selection = self.selection ^ {note_key(self.data["notes"][index])}
        self._selection_changed()

    def select_range(self, start, end, columns=None, add=False, include_end=True):
        """Select every note whose head lies between two song times, optionally in some columns only."""
        low, high = sorted((start, end))
        found = {note_key(note) for note in self.data["notes"]
                 if low - .000001 <= note["time"]
                 and (note["time"] <= high + .000001 if include_end else note["time"] < high - .000001)
                 and (columns is None or note_column(note) in columns)}
        self.selection = (self.selection | found) if add else found
        self._selection_changed()

    def select_all(self):
        if not self.data["notes"]:
            raise ValueError("The chart has no notes yet.")
        self.selection = {note_key(note) for note in self.data["notes"]}
        self._selection_changed()

    def clear_selection(self):
        self.status = "Selection cleared." if self.selection or self.effect_selected else "Nothing selected."
        self.selection = set()
        self.effect_selected = None

    def _require_selection(self):
        chosen = self.selected_notes()
        if not chosen:
            raise ValueError(EMPTY_SELECTION)
        return chosen

    # ---- note edits -------------------------------------------------------------

    def hold_length(self):
        try:
            beats = float(self.hold_text)
        except (ValueError, TypeError):
            raise ValueError("Hold length must be a number of beats; 0 creates a tap.")
        if not math.isfinite(beats) or not 0 <= beats <= 64:
            raise ValueError("Hold length must be between 0 and 64 beats.")
        return round(beats * self.beat, 6)

    def note(self, seconds, lane, side, delete=False, toggle=False):
        self.require_developer()
        when = self.snap_time(seconds)
        index = self.at(when, lane, side)
        if index is not None and not delete and not toggle:
            self.select_note(index)
        elif index is not None:
            self.delete_note(index)
        elif not delete:
            candidate = copy.deepcopy(self.data)
            candidate["notes"].append(dict(time=when, lane=lane, side=side, length=self.hold_length()))
            self.commit(candidate)
            self.selected = self.at(when, lane, side)
            self.status = "Added %s lane %d at %.3fs." % (side, lane + 1, when)

    def delete_note(self, index):
        self.require_developer()
        remaining = self.selection - {note_key(self.data["notes"][index])}
        candidate = copy.deepcopy(self.data)
        del candidate["notes"][index]
        self.commit(candidate)
        # Deleting one note moves no other, so the rest of the selection still holds.
        self.selection = remaining
        self.status = "Note deleted."

    def _plan_transform(self, change):
        """Apply ``change`` to a copy of each selected note; returns (changed notes, unselected notes).

        Raises ValueError when a result would leave the song or land on a note
        outside the selection.
        """
        indices = self.selected_indices()
        if not indices:
            raise ValueError(EMPTY_SELECTION)
        chosen = set(indices)
        duration = self.data["duration"]
        results = []
        for index in indices:
            note = change(dict(self.data["notes"][index]))
            note["time"] = self.tidy_time(note["time"])
            note["length"] = round(note["length"], 6)
            if not 0 <= note["time"] <= duration or note["time"] + note["length"] > duration + .001:
                raise ValueError("That would push notes outside the song.")
            results.append(note)
        others = [note for index, note in enumerate(self.data["notes"]) if index not in chosen]
        blocked = blocking_notes(results, others)
        if blocked:
            raise ValueError("Overlapping notes: %s in the way." % plural(len(blocked), "other note"))
        return results, others

    def _transform_selection(self, change):
        """Replace the selection with its changed copies as one undoable edit; returns (notes, changed).

        A refusal leaves the document untouched. Collisions inside the selection
        itself, such as two notes snapping onto one grid line, are caught by
        normalize_chart during the commit.
        """
        self.require_developer()
        results, others = self._plan_transform(change)
        before = self.data
        candidate = copy.deepcopy(self.data)
        candidate["notes"] = others + results
        self.commit(candidate)
        self.selection = {note_key(note) for note in results}
        return results, self.data is not before

    def set_hold(self):
        length = self.hold_length()
        if not self.selection:
            self.status = "Hold length set for the next note."
            return
        results, changed = self._transform_selection(lambda note: dict(note, length=length))
        self.status = ("Selected hold updated." if len(results) == 1
                       else "Hold set to %s beats on %s." % (self.hold_text, plural(len(results), "note")))

    def step_hold(self, direction):
        """Lengthen or shorten the hold by one grid step (1/snap of a beat)."""
        try:
            beats = float(self.hold_text)
        except (ValueError, TypeError):
            beats = 0.0
        steps = round(beats * self.snap) + direction
        beats = max(0.0, min(64.0, steps / float(self.snap)))
        self.hold_text = beats_text(beats)
        self.set_hold()

    def delete_selection(self):
        self.require_developer()
        indices = set(self.selected_indices())
        if not indices:
            if self.selected_effect() is not None:
                self.delete_effect()
                return
            self.status = "Nothing selected."
            return
        candidate = copy.deepcopy(self.data)
        candidate["notes"] = [note for index, note in enumerate(candidate["notes"]) if index not in indices]
        self.commit(candidate)
        self.status = "Deleted %s." % plural(len(indices), "note")

    delete_selected = delete_selection

    def _mover(self, steps, columns):
        grid = self.beat / self.snap

        def change(note):
            column = note_column(note) + columns
            if not 0 <= column < 8:
                raise ValueError("That would move notes off the grid.")
            return dict(note, time=note["time"] + steps * grid, lane=column % 4, side=SIDES[column // 4])

        return change

    def preview_move(self, steps=0, columns=0):
        """(moved notes, None) when a move is allowed, else (None, the reason). Edits nothing."""
        try:
            return self._plan_transform(self._mover(steps, columns))[0], None
        except ValueError as error:
            return None, str(error)

    def move_selection(self, steps=0, columns=0):
        """Shift the selection by grid steps in time and by columns across the eight lanes."""
        results, changed = self._transform_selection(self._mover(steps, columns))
        self.status = "Moved %s." % plural(len(results), "note")

    def mirror_selection(self):
        results, changed = self._transform_selection(lambda note: dict(note, lane=3 - note["lane"]))
        self.status = "Mirrored %s." % plural(len(results), "note")

    def flip_sides(self):
        results, changed = self._transform_selection(
            lambda note: dict(note, side=SIDES[1 - SIDES.index(note["side"])]))
        self.status = "Moved %s to the other singer." % plural(len(results), "note")

    def quantize_selection(self):
        results, changed = self._transform_selection(lambda note: dict(note, time=self.snap_time(note["time"])))
        self.status = ("Snapped %s to the grid." % plural(len(results), "note")) if changed else "Already on the grid."

    # ---- clipboard ----------------------------------------------------------------

    def copy_selection(self):
        chosen = self._require_selection()
        first = chosen[0]["time"]
        self.clipboard = [dict(beats=(note["time"] - first) / self.beat, lane=note["lane"],
                               side=note["side"], hold=note["length"] / self.beat) for note in chosen]
        self.status = "Copied %s." % plural(len(chosen), "note")

    def cut_selection(self):
        self.copy_selection()
        count = len(self.clipboard)
        self.delete_selection()
        self.status = "Cut %s." % plural(count, "note")

    @staticmethod
    def _paste_details(replaced, skipped):
        details = []
        if replaced:
            details.append("replacing %d" % replaced)
        if skipped:
            details.append("%d past the end skipped" % skipped)
        return (", " + ", ".join(details)) if details else ""

    def paste(self, seconds, snap=True):
        """Paste the clipboard with its first note at ``seconds``; returns (pasted, replaced, skipped).

        Pasted notes replace anything they land on in their own lanes, holds are
        trimmed at the end of the song, and notes past the end are skipped. The
        pasted notes become the selection, so they can be moved straight away.
        """
        self.require_developer()
        if not self.clipboard:
            raise ValueError("The clipboard is empty. Select notes and copy them first.")
        anchor = self.snap_time(seconds) if snap else seconds
        duration = self.data["duration"]
        incoming = []
        skipped = 0
        for item in self.clipboard:
            # Beats-to-seconds float error must not leave a pasted note a microsecond off its line.
            when = self.tidy_time(anchor + item["beats"] * self.beat)
            if when < 0 or when > duration:
                skipped += 1
                continue
            length = round(max(0.0, min(item["hold"] * self.beat, duration - when)), 6)
            incoming.append(dict(time=when, lane=item["lane"], side=item["side"], length=length))
        if not incoming:
            raise ValueError("Nothing to paste there: every copied note would fall outside the song.")
        doomed = {id(note) for note in blocking_notes(incoming, self.data["notes"])}
        candidate = copy.deepcopy(self.data)
        candidate["notes"] = [note for note in self.data["notes"] if id(note) not in doomed] + incoming
        self.commit(candidate)
        self.selection = {note_key(note) for note in incoming}
        self.effect_selected = None
        self.status = "Pasted %s%s." % (plural(len(incoming), "note"), self._paste_details(len(doomed), skipped))
        return len(incoming), len(doomed), skipped

    def duplicate_selection(self):
        """Copy the selection whole measures later, far enough that the copy never lands on itself."""
        chosen = self._require_selection()
        first = chosen[0]["time"]
        end = max(note["time"] + max(.001, note["length"]) for note in chosen)
        measure = self.beat * 4
        measures = max(1, int(math.ceil((end - first) / measure - .000001)))
        if first + measures * measure > self.data["duration"]:
            raise ValueError("No room for a copy: the song ends first.")
        clipboard = self.clipboard
        try:
            self.copy_selection()
            count, replaced, skipped = self.paste(first + measures * measure, snap=False)
        finally:
            self.clipboard = clipboard
        self.status = "Duplicated %s %s later%s." % (plural(count, "note"), plural(measures, "measure"),
                                                     self._paste_details(replaced, skipped))

    # ---- camera -------------------------------------------------------------------

    def camera_override(self, seconds):
        index = measure_index(self.data, seconds)
        for event in self.data.get("camera", ()):
            if measure_index(self.data, event["time"]) == index:
                return event["focus"]
        return None

    def set_camera(self, seconds, focus):
        """Pin the framing of the measure at ``seconds``; ``None`` returns it to auto."""
        self.require_developer()
        if focus is not None and focus not in CAMERA_FOCI:
            raise ValueError("Camera focus must be opponent, player, center or automatic.")
        index = measure_index(self.data, seconds)
        measure = self.beat * 4
        start = self.data["offset"] + index * measure
        if start + measure <= 0 or start > self.data["duration"]:
            raise ValueError("That measure is outside the song.")
        candidate = copy.deepcopy(self.data)
        events = [e for e in candidate.get("camera", []) if measure_index(candidate, e["time"]) != index]
        if focus is not None:
            # Stored mid-measure, so a later small BPM or offset correction keeps
            # the event inside the measure it was authored for.
            middle = max(0.0, min(self.data["duration"], start + measure / 2))
            events.append(dict(time=round(middle, 6), focus=focus))
        candidate["camera"] = events
        selection = set(self.selection)
        self.commit(candidate)
        self.selection = selection
        self.status = ("Measure %d camera pinned to %s." % (index + 1, focus) if focus
                       else "Measure %d camera follows the notes." % (index + 1))

    def cycle_camera(self, seconds, backwards=False):
        order = (None,) + CAMERA_FOCI
        current = order.index(self.camera_override(seconds))
        self.set_camera(seconds, order[(current + (-1 if backwards else 1)) % len(order)])

    # ---- effects ------------------------------------------------------------------
    # Effects keep absolute song times like notes, so BPM and offset edits never
    # move them. Spans of one kind never overlap; different kinds layer freely.

    def effects(self):
        return self.data.get("effects", [])

    def effect_index(self, key):
        for index, effect in enumerate(self.effects()):
            if effect_key(effect) == key:
                return index
        return None

    def selected_effect(self):
        index = None if self.effect_selected is None else self.effect_index(self.effect_selected)
        return None if index is None else self.effects()[index]

    def effects_at(self, seconds, tolerance=None):
        """Indices of effects under ``seconds``: spans that cover it, bursts within ``tolerance``."""
        if tolerance is None:
            tolerance = min(.060, self.beat / self.snap * .46)
        found = []
        for index, effect in enumerate(self.effects()):
            if effect["kind"] in BURST_EFFECTS:
                if abs(effect["time"] - seconds) <= tolerance:
                    found.append(index)
            elif effect["time"] - tolerance <= seconds < effect["time"] + effect["length"]:
                found.append(index)
        return found

    def effect_text(self, effect):
        name = EFFECT_NAMES[effect["kind"]]
        if effect["kind"] in REACTIVE_EFFECTS:
            name = "%s on %s" % (name, SIDE_NAMES[effect.get("side", "opponent")])
        if effect["kind"] in BURST_EFFECTS:
            return "%s at %.3fs" % (name, effect["time"])
        return "%s at %.3fs for %s beats" % (name, effect["time"], beats_text(effect["length"] / self.beat))

    def _commit_effects(self, effects, select):
        """Replace the effect list as one undoable edit, then select ``select`` (an effect key or None)."""
        self.require_developer()
        candidate = copy.deepcopy(self.data)
        candidate["effects"] = effects
        self.commit(candidate)
        self.selection = set()
        self.effect_selected = select

    def _require_effect(self):
        index = None if self.effect_selected is None else self.effect_index(self.effect_selected)
        if index is None:
            self.effect_selected = None
            raise ValueError("Select an effect first: click one in the FX lane.")
        return index

    def add_effect(self, seconds, kind=None, beats=None):
        """Place an effect at the snapped time. A span runs ``beats`` beats, stopping where the next of its kind starts."""
        self.require_developer()
        kind = kind or self.effect_kind
        if kind not in EFFECT_KINDS:
            raise ValueError("Unknown effect: %s." % kind)
        when = self.snap_time(seconds)
        duration = self.data["duration"]
        name = EFFECT_NAMES[kind]
        same = [effect for effect in self.effects() if effect["kind"] == kind]
        if kind in BURST_EFFECTS:
            length = 0.0
            if any(abs(effect["time"] - when) < .001 for effect in same):
                raise ValueError("There is already a %s there." % name.lower())
        else:
            if when >= duration - .05:
                raise ValueError("No room for %s at the very end of the song." % name.lower())
            if any(effect["time"] - .000001 <= when < effect["time"] + effect["length"] - .000001 for effect in same):
                raise ValueError("%s is already running there." % name)
            beats = self.effect_beats if beats is None else float(beats)
            length = min(beats * self.beat, duration - when)
            later = [effect["time"] for effect in same if effect["time"] > when]
            if later:
                length = min(length, min(later) - when)
            length = round(length, 6)
            if length < .05:
                raise ValueError("No room for %s there." % name.lower())
            self.effect_beats = beats
            self.fx_new_text = beats_text(beats)
        self.effect_kind = kind
        placed = dict(time=when, kind=kind, length=length)
        if kind in REACTIVE_EFFECTS:
            placed["side"] = self.effect_side
        effects = copy.deepcopy(self.effects()) + [placed]
        self._commit_effects(effects, (round(when, 6), kind))
        self.status = "Added %s." % self.effect_text(self.selected_effect())

    def select_effect(self, index):
        effect = self.effects()[index]
        self.selection = set()
        self.effect_selected = effect_key(effect)
        self.effect_kind = effect["kind"]
        if effect["kind"] in REACTIVE_EFFECTS:
            self.effect_side = effect.get("side", "opponent")
        if effect["kind"] not in BURST_EFFECTS:
            self.effect_beats = effect["length"] / self.beat
            self.fx_text = beats_text(self.effect_beats)
        self.status = "Selected %s." % self.effect_text(effect)

    def delete_effect(self, index=None):
        self.require_developer()
        index = self._require_effect() if index is None else index
        effects = copy.deepcopy(self.effects())
        removed = effects.pop(index)
        self._commit_effects(effects, None)
        self.status = "%s deleted." % EFFECT_NAMES[removed["kind"]]

    def _change_effect(self, change):
        """Apply ``change`` to a copy of the selected effect as one undoable edit; a refusal changes nothing."""
        self.require_developer()
        index = self._require_effect()
        effects = copy.deepcopy(self.effects())
        effect = change(dict(effects[index]))
        effect["time"] = self.tidy_time(effect["time"])
        effect["length"] = round(effect["length"], 6)
        if effect["time"] < 0 or effect["time"] + effect["length"] > self.data["duration"] + .001:
            raise ValueError("That would push %s outside the song." % EFFECT_NAMES[effect["kind"]].lower())
        effects[index] = effect
        self._commit_effects(effects, effect_key(effect))
        return effect

    def move_effect(self, steps):
        """Shift the selected effect by grid steps."""
        grid = self.beat / self.snap
        effect = self._change_effect(lambda e: dict(e, time=e["time"] + steps * grid))
        self.status = "Moved to %s." % self.effect_text(effect)

    def resize_effect(self, steps, beats=False):
        """Lengthen or shorten the selected span by grid steps, or by whole beats.

        Never below one grid step, and never past the end of the song: growing a
        span that already reaches the end changes nothing.
        """
        current = self.selected_effect()
        if current is not None and current["kind"] in BURST_EFFECTS:
            self.status = "%s happens at one moment, so it has no length." % EFFECT_NAMES[current["kind"]]
            return
        unit = self.beat if beats else self.beat / self.snap
        smallest = self.beat / self.snap
        room = None if current is None else self.data["duration"] - current["time"]
        if current is not None and steps > 0 and current["length"] >= room - .000001:
            self.status = "%s already runs to the end of the song." % EFFECT_NAMES[current["kind"]]
            return
        effect = self._change_effect(
            lambda e: dict(e, length=min(self.data["duration"] - e["time"], max(smallest, e["length"] + steps * unit))))
        self.effect_beats = effect["length"] / self.beat
        self.fx_text = beats_text(self.effect_beats)
        self.status = "%s now runs %s beats." % (EFFECT_NAMES[effect["kind"]], beats_text(effect["length"] / self.beat))

    # ---- effect measurements ------------------------------------------------------
    # Beats, not seconds, are how effects are actually authored: "four bars of
    # haze", "a flash every 8 beats". These turn a typed beat count or a dragged
    # position into one undoable edit.

    def _beats_field(self, text, what, smallest, largest):
        try:
            beats = float(text)
        except (ValueError, TypeError):
            raise ValueError("%s must be a number of beats." % what)
        if not math.isfinite(beats) or not smallest <= beats <= largest:
            raise ValueError("%s must be between %s and %s beats."
                             % (what, beats_text(smallest), beats_text(largest)))
        return beats

    def effect_room(self, index, time=None):
        """How much room the effect at ``index`` has: (earliest start, latest start, longest length).

        Two effects of one kind may never overlap, so the nearest one of its own
        kind on either side bounds it; different kinds layer freely. ``time``
        asks about a position it is being dragged to rather than the one it
        holds. Bursts keep a whole grid step from their neighbours, since they
        only ever sit on grid lines and a hairline gap would read as off-grid.
        """
        effect = self.effects()[index]
        when = effect["time"] if time is None else time
        burst = effect["kind"] in BURST_EFFECTS
        gap = self.beat / self.snap if burst else 0.0
        span = 0.0 if burst else effect["length"]
        floor, ceiling = 0.0, self.data["duration"]
        for other, neighbour in enumerate(self.effects()):
            if other == index or neighbour["kind"] != effect["kind"]:
                continue
            if neighbour["time"] > when:
                ceiling = min(ceiling, neighbour["time"])
            else:
                floor = max(floor, neighbour["time"] + max(neighbour["length"], gap))
        return round(floor, 6), round(max(floor, ceiling - max(span, gap)), 6), round(max(0.0, ceiling - when), 6)

    def place_effect(self, index, seconds):
        """Move the effect at ``index`` to a snapped time, clamped inside its room.

        The drag in the FX lane commits through here, so a whole drag is one
        undo step however many frames the pointer took over it. A moved effect
        keeps its length: the clamp stops it short of the next one of its kind
        rather than squeezing it.
        """
        self.require_developer()
        target = self.snap_time(seconds)
        earliest, latest, unused = self.effect_room(index, target)
        effects = copy.deepcopy(self.effects())
        effect = dict(effects[index], time=round(min(max(target, earliest), latest), 6))
        effects[index] = effect
        self._commit_effects(effects, effect_key(effect))
        self.status = "Moved to %s." % self.effect_text(effect)
        return effect

    def stretch_effect(self, index, seconds):
        """Drag on a span's end: run it from its start to the snapped time under the pointer."""
        self.require_developer()
        effect = self.effects()[index]
        if effect["kind"] in BURST_EFFECTS:
            raise ValueError("%s happens at one moment, so it has no length." % EFFECT_NAMES[effect["kind"]])
        smallest = self.beat / self.snap
        longest = self.effect_room(index)[2]
        length = round(max(smallest, min(longest, self.snap_time(seconds) - effect["time"])), 6)
        effects = copy.deepcopy(self.effects())
        effects[index] = dict(effect, length=length)
        self._commit_effects(effects, effect_key(effects[index]))
        self.effect_beats = length / self.beat
        self.fx_text = beats_text(self.effect_beats)
        self.status = "%s now runs %s beats." % (EFFECT_NAMES[effect["kind"]], beats_text(self.effect_beats))

    def set_effect_side(self, side):
        """Whose notes drive the selected reactive effect, or the next one placed."""
        if side not in EFFECT_SIDES:
            raise ValueError("A reactive effect answers %s." % ", ".join(EFFECT_SIDES))
        self.effect_side = side
        effect = self.selected_effect()
        if effect is None or effect["kind"] not in REACTIVE_EFFECTS:
            self.status = "New reactive effects answer %s." % SIDE_NAMES[side]
            return
        index = self._require_effect()
        effects = copy.deepcopy(self.effects())
        effects[index] = dict(effect, side=side)
        self._commit_effects(effects, effect_key(effects[index]))
        self.status = "%s." % self.effect_text(effects[index])

    def set_new_effect_beats(self):
        """The span length the next effect placed gets. Never touches the selection."""
        beats = self._beats_field(self.fx_new_text, "An effect length", .0625, 4096)
        self.effect_beats = beats
        self.fx_new_text = beats_text(beats)
        self.status = "New effects run %s beats." % self.fx_new_text

    def set_effect_beats(self):
        """Run the selected span for the typed number of beats."""
        beats = self._beats_field(self.fx_text, "An effect length", .0625, 4096)
        effect = self.selected_effect()
        if effect is None:
            # Nothing selected: the number can only mean the next effect placed.
            self.fx_new_text = self.fx_text
            self.set_new_effect_beats()
            return
        if effect["kind"] in BURST_EFFECTS:
            self.status = "%s happens at one moment, so it has no length." % EFFECT_NAMES[effect["kind"]]
            return
        index = self._require_effect()
        smallest = self.beat / self.snap
        longest = self.effect_room(index)[2]
        length = round(max(smallest, min(longest, beats * self.beat)), 6)
        effects = copy.deepcopy(self.effects())
        effects[index] = dict(effect, length=length)
        self._commit_effects(effects, effect_key(effects[index]))
        actual = beats_text(length / self.beat)
        # The box always shows what the effect really runs, not what was typed.
        clamped, self.fx_text = actual != self.fx_text, actual
        self.effect_beats = length / self.beat
        self.status = ("%s runs %s beats: it reaches the next one of its kind."
                       % (EFFECT_NAMES[effect["kind"]], actual) if clamped
                       else "%s now runs %s beats." % (EFFECT_NAMES[effect["kind"]], actual))

    def set_repeat_beats(self):
        """Store the typed gap between repeats; the Repeat button is what places them."""
        self.fx_every_text = beats_text(self._beats_field(self.fx_every_text, "A repeat gap", .0625, 4096))
        self.status = "Repeat places a copy every %s beats." % self.fx_every_text

    def whole_song_effect(self):
        """One span of the selected kind over the entire song, replacing every other span of it."""
        self.require_developer()
        index = self._require_effect()
        kind = self.effects()[index]["kind"]
        if kind in BURST_EFFECTS:
            raise ValueError("%s happens at one moment. Repeat it instead." % EFFECT_NAMES[kind])
        removed = sum(1 for effect in self.effects() if effect["kind"] == kind) - 1
        keep = [copy.deepcopy(e) for e in self.effects() if e["kind"] != kind]
        span = dict(time=0.0, kind=kind, length=round(self.data["duration"], 6))
        if kind in REACTIVE_EFFECTS:
            span["side"] = self.effects()[index].get("side", "opponent")
        self._commit_effects(keep + [span], effect_key(span))
        self.effect_beats = span["length"] / self.beat
        self.fx_text = beats_text(self.effect_beats)
        self.status = ("%s now runs the whole song." % EFFECT_NAMES[kind] if not removed
                       else "%s now runs the whole song, replacing %s."
                            % (EFFECT_NAMES[kind], plural(removed, "other span")))

    def repeat_effect(self):
        """Copy the selected effect every N beats to the end of the song.

        Positions already taken by that kind are skipped rather than refused, so
        repeating over a stretch that is partly filled fills in the gaps.
        """
        self.require_developer()
        index = self._require_effect()
        effect = self.effects()[index]
        every = self._beats_field(self.fx_every_text, "A repeat gap", .0625, 4096) * self.beat
        span = 0.0 if effect["kind"] in BURST_EFFECTS else effect["length"]
        if every < span - .000001:
            raise ValueError("Repeat every %s beats or more: that is how long this span runs."
                             % beats_text(span / self.beat))
        duration = self.data["duration"]
        taken = [(e["time"], e["time"] + max(e["length"], .001)) for e in self.effects() if e["kind"] == effect["kind"]]
        effects = copy.deepcopy(self.effects())
        when, added = effect["time"] + every, 0
        # A song is at most an hour, so this walk is bounded by the gap, not the loop.
        while when + span <= duration + .001 and added < 4000:
            place = round(when, 6)
            if not any(start - .000001 < place + max(span, .001) and place < end - .000001 for start, end in taken):
                copied = dict(time=place, kind=effect["kind"], length=round(span, 6))
                if effect["kind"] in REACTIVE_EFFECTS:
                    copied["side"] = effect.get("side", "opponent")
                effects.append(copied)
                taken.append((place, place + max(span, .001)))
                added += 1
            when += every
        if not added:
            raise ValueError("No room to repeat %s before the end of the song." % EFFECT_NAMES[effect["kind"]].lower())
        self._commit_effects(effects, effect_key(effect))
        self.status = "%s repeated every %s beats: %s added." % (
            EFFECT_NAMES[effect["kind"]], beats_text(every / self.beat),
            "1 copy" if added == 1 else "%d copies" % added)

    # ---- files --------------------------------------------------------------------

    def export_text(self):
        self.require_developer()
        self.apply_metadata()
        return json.dumps(normalize_chart(self.data), ensure_ascii=False, indent=2, allow_nan=False) + "\n"

    def save_name(self):
        """The file Save writes: every song keeps one chart file, named after its ID."""
        return self.data["id"] + ".json"

    def save(self, chart_root, export=False):
        """Atomic local write; filenames never escape the designated chart folder.

        Every song keeps one chart file, charts/<id>.json. A chart opened from a
        file with another name is written to <id>.json and the old file removed,
        so no stale copy of the song is left beside it. A save never replaces a
        different chart's file. Export always writes exports/<id>.json.
        """
        self.require_developer()
        contents = self.export_text()
        root = os.path.realpath(chart_root)
        directory = os.path.realpath(os.path.join(root, "exports")) if export else root
        identifier = self.data["id"]
        if not re.fullmatch(r"[A-Za-z0-9_\-]{1,80}", identifier):
            raise ValueError("Use only letters, digits, underscores or hyphens for the chart ID.")
        name = self.save_name()
        target = os.path.realpath(os.path.join(directory, name))
        if os.path.commonpath((root, target)) != root:
            raise ValueError("The chart path must stay inside the chart folder.")
        previous = None
        if not export and self.current_path:
            previous = os.path.realpath(os.path.join(root, os.path.basename(self.current_path)))
        same_file = previous is not None and os.path.normcase(previous) == os.path.normcase(target)
        if not export and os.path.exists(target) and not same_file:
            raise ValueError("charts/%s belongs to another chart. Give this chart another ID, or load that one." % name)
        os.makedirs(directory, exist_ok=True)
        handle, temporary = tempfile.mkstemp(prefix=".chart-", suffix=".tmp", dir=directory)
        try:
            with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
                stream.write(contents)
            os.replace(temporary, target)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        moved = None
        if not export:
            # Only after the new file is safely written does the old name go.
            if previous is not None and not same_file and os.path.exists(previous):
                os.remove(previous)
                moved = os.path.basename(previous)
            self.saved = copy.deepcopy(self.data)
            self.current_path = target
        self.status = (("Exported to charts/exports/" if export else "Saved charts/") + name +
                       (" (was %s)" % moved if moved else ""))
        return target

    @staticmethod
    def decode(contents):
        if len(contents) > 8 * 1024 * 1024:
            raise ValueError("Chart files must be smaller than 8 MiB.")
        if isinstance(contents, bytes):
            contents = contents.decode("utf-8-sig")
        return normalize_chart(json.loads(contents))
