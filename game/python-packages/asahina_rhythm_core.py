"""Deterministic chart and judgment rules; deliberately independent of Ren'Py.

Chart times and sustain lengths are seconds in the audio file. ``offset`` only
anchors the editor's beat grid; it is never added to note timestamps again.
``duration`` is the authored chart endpoint, which may trim an audio outro.
All notes/effects must fit it; a clear follows that endpoint plus HIT_WINDOW.

A session judges input by COLUMN. Columns 0-3 are the player's lanes. In a duet
the player also sings Asahina's part, and her lanes are columns 4-7.
"""
import bisect
import math
import re

HIT_WINDOW = 0.160
HOLD_TICK = 0.125
RELEASE_GRACE = 0.075
TIERS = ((0.045, "SICK!", 350, 1.0), (0.090, "GOOD", 200, .75),
         (0.135, "OKAY", 100, .4), (HIT_WINDOW, "YUCKY", 50, .1))
CAMERA_FOCI = ("opponent", "player", "center")
MISS_DAMAGE = .052

# ---- modifiers ----------------------------------------------------------------
# One run's rule changes. dizzy and vanish only change how notes are drawn; they
# are listed here so results and records can name them.
MODIFIERS = ("dizzy", "vanish", "mirror", "no_miss", "flawless", "fights_back",
             "wide_timing", "half_damage", "duet")
# Assists make a clear easier, so a run with one keeps no records or rewards.
ASSIST_MODIFIERS = frozenset(("wide_timing", "half_damage"))
EXCLUSIVE_MODIFIERS = (frozenset(("no_miss", "flawless")), frozenset(("duet", "fights_back")))
WIDE_TIMING = 1.5
# fights_back: each of Asahina's notes takes FIGHT_DRAIN health but never pushes
# the bar below FIGHT_FLOOR. She can corner the player; only their misses finish them.
FIGHT_DRAIN = .014
FIGHT_FLOOR = .10

# ---- chart effects --------------------------------------------------------------
# Span effects run for a length. Bursts happen at one moment and store length 0.
# Reactive spans are a third shape: they run for a length like any span, but
# nothing happens until a note lands. Each carries the side whose notes drive it.
# New kinds are APPENDED. The sort key below is this tuple's index, so moving
# an existing kind would reorder the effects of every chart already on disk and
# stop a saved chart comparing equal to the one the editor just loaded.
EFFECT_KINDS = ("fanfare", "spotlights", "lasers", "haze", "blackout", "pulse", "crowd",
                "quake", "strobe", "lunge", "shockwave",
                "flash", "confetti", "sparks",
                # The dread set. Same three shapes, opposite job: the concert
                # kinds above add light and answer the beat, these take light
                # away and mostly refuse to keep time with anything.
                "dread", "watchers", "static", "hollow", "footlights", "rot",
                "arrhythmia", "doubles", "gutter",
                "recoil", "fracture",
                "cut", "tear", "glimpse",
                # The body: what the dread set does to the people in it.
                "veins", "blood", "convulse", "redwash",
                # The signal: what it does to the picture they are recorded on.
                # These five are pure colour and resolution work, done with GL
                # blend functions and a mesh resample rather than a shader.
                "invert", "negative", "infrared", "fried", "bitcrush")
# Stable serialized order, looked up once per cue during sorting.
_EFFECT_ORDER = {kind: index for index, kind in enumerate(EFFECT_KINDS)}
BURST_EFFECTS = frozenset(("flash", "confetti", "sparks", "cut", "tear", "glimpse", "invert"))
REACTIVE_EFFECTS = frozenset(("quake", "strobe", "lunge", "shockwave", "recoil", "fracture"))
EFFECT_SIDES = ("opponent", "player", "both")
# How hard a reactive effect hits, indexed by how many notes land together.
# A lone note is a knock; the full four-lane chord is the wallop the ladder
# exists for. Index 0 is never used: no notes means no impact.
IMPACT_GAIN = (0.0, 0.55, 0.80, 1.05, 1.40)
# A fanfare scores x2 from its start. A miss inside it puts it out until
# FANFARE_RELIGHT hits in a row relight it, and FANFARE_TOP hits in a row while
# it is lit raise it to x3.
FANFARE_RELIGHT = 10
FANFARE_TOP = 30


def _number(value, name, minimum, maximum):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("%s must be a number." % name)
    value = float(value)
    if not math.isfinite(value) or not minimum <= value <= maximum:
        raise ValueError("%s must be between %s and %s." % (name, minimum, maximum))
    return value


def normalize_chart(data):
    """Validate external/editor input before constructing a mutable session."""
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("This mode reads version 1 chart objects.")
    normalized = dict(data)
    chart_id = data.get("id")
    if not isinstance(chart_id, str) or not re.fullmatch(r"[A-Za-z0-9_\-]{1,80}", chart_id):
        raise ValueError("id must be a plain identifier (letters, digits, _ or -).")
    source = data.get("audio")
    if (not isinstance(source, str) or not source or len(source) > 300 or
            any(c in source for c in "<>\\:\x00") or source.startswith("/") or
            any(part in ("", ".", "..") for part in source.split("/"))):
        raise ValueError("Audio must be an alias or a safe game-relative audio path.")
    if not isinstance(data.get("title"), str) or not data["title"].strip():
        raise ValueError("A chart needs a title.")
    normalized["title"] = data["title"].strip()[:120]
    normalized["bpm"] = _number(data.get("bpm"), "BPM", 20, 400)
    normalized["offset"] = _number(data.get("offset", 0), "Grid offset", -30, 120)
    normalized["duration"] = _number(data.get("duration"), "Duration", .1, 3600)
    notes = data.get("notes")
    if not isinstance(notes, list) or len(notes) > 50000:
        raise ValueError("Notes must be a list of at most 50,000 notes.")
    normalized_notes = []
    for note_index, note in enumerate(notes):
        if not isinstance(note, dict):
            raise ValueError("Note %d must be an object." % note_index)
        lane, side = note.get("lane"), note.get("side")
        if type(lane) is not int or lane not in range(4) or side not in ("player", "opponent"):
            raise ValueError("Note %d needs lane 0..3 and side player or opponent." % note_index)
        note_time = _number(note.get("time"), "Note %d time" % note_index, 0, normalized["duration"])
        length = _number(note.get("length", 0), "Note %d length" % note_index, 0, normalized["duration"])
        if note_time + length > normalized["duration"] + .001:
            raise ValueError("Note %d extends beyond the song duration." % note_index)
        normalized_notes.append(dict(time=note_time, lane=lane, side=side, length=length))
    normalized_notes.sort(key=lambda note: (note["time"], note["side"], note["lane"]))
    previous = {}
    for note in normalized_notes:
        key = (note["side"], note["lane"])
        prior = previous.get(key)
        if prior and note["time"] < prior["time"] + max(.001, prior["length"]) - .000001:
            raise ValueError("Overlapping notes in %s lane %d at %.3fs." % (key[0], key[1], note["time"]))
        previous[key] = note
    normalized["notes"] = normalized_notes
    camera = data.get("camera", [])
    if not isinstance(camera, list) or len(camera) > 10000:
        raise ValueError("Camera events must be a list of at most 10,000 entries.")
    normalized_camera = []
    for event_index, event in enumerate(camera):
        if not isinstance(event, dict) or event.get("focus") not in CAMERA_FOCI:
            raise ValueError("Camera event %d needs a focus of opponent, player or center." % event_index)
        normalized_camera.append(dict(time=_number(event.get("time"), "Camera event %d time" % event_index, 0, normalized["duration"]),
                          focus=event["focus"]))
    normalized_camera.sort(key=lambda event: event["time"])
    # An empty override list is the same chart as none, so it must compare equal.
    if normalized_camera:
        normalized["camera"] = normalized_camera
    else:
        normalized.pop("camera", None)
    effects = data.get("effects", [])
    if not isinstance(effects, list) or len(effects) > 5000:
        raise ValueError("Effects must be a list of at most 5,000 entries.")
    cues = []
    for event_index, event in enumerate(effects):
        if not isinstance(event, dict) or event.get("kind") not in EFFECT_KINDS:
            raise ValueError("Effect %d needs a kind: %s." % (event_index, ", ".join(EFFECT_KINDS)))
        kind = event["kind"]
        event_time = _number(event.get("time"), "Effect %d time" % event_index, 0, normalized["duration"])
        if kind in BURST_EFFECTS:
            length = 0.0
        else:
            length = _number(event.get("length"), "Effect %d length" % event_index, .05, normalized["duration"])
        if event_time + length > normalized["duration"] + .001:
            raise ValueError("Effect %d runs past the end of the song." % event_index)
        cue = dict(time=event_time, kind=kind, length=length)
        if kind in REACTIVE_EFFECTS:
            # Only a reactive span stores a side, so an effect dict stays canonical
            # and two charts that mean the same thing still compare equal.
            side = event.get("side", "opponent")
            if side not in EFFECT_SIDES:
                raise ValueError("Effect %d needs a side: %s." % (event_index, ", ".join(EFFECT_SIDES)))
            cue["side"] = side
        cues.append(cue)
    cues.sort(key=lambda event: (event["time"], _EFFECT_ORDER[event["kind"]]))
    # Two cues of one kind never overlap; different kinds layer freely.
    end_by_kind = {}
    for cue in cues:
        if cue["time"] < end_by_kind.get(cue["kind"], -1.0) - .000001:
            raise ValueError("Two %s effects overlap at %.3fs." % (cue["kind"], cue["time"]))
        end_by_kind[cue["kind"]] = cue["time"] + max(.001, cue["length"])
    if cues:
        normalized["effects"] = cues
    else:
        normalized.pop("effects", None)
    return normalized


def normalize_modifiers(modifiers):
    """The modifier ids as a frozenset; unknown ids and exclusive pairs are refused."""
    chosen = frozenset(modifiers or ())
    unknown = chosen.difference(MODIFIERS)
    if unknown:
        raise ValueError("Unknown modifier: %s." % ", ".join(sorted(unknown)))
    for pair in EXCLUSIVE_MODIFIERS:
        if pair <= chosen:
            raise ValueError("%s can't be combined." % " and ".join(sorted(pair)))
    return chosen


def column_of(note):
    """A note's input column: 0-3 for the player's lanes, 4-7 for Asahina's."""
    return note["lane"] + (4 if note["side"] == "opponent" else 0)


class EffectTrack:
    """One span effect's cues, merged where they touch, queried by song time."""
    def __init__(self, cues):
        merged = []
        for start, end in sorted(cues):
            if merged and start <= merged[-1][1] + .001:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))
        self.cues = merged
        self.starts = [start for start, end in merged]

    def span_at(self, t):
        """The (start, end) cue covering ``t``, or None."""
        i = bisect.bisect_right(self.starts, t) - 1
        if i >= 0 and t < self.cues[i][1]:
            return self.cues[i]
        return None

    def level(self, t, rise=.35, fall=.5):
        """0..1: eases up over ``rise`` from a cue's start and down over ``fall`` after its end.

        A cue that starts while the previous one is still fading picks up from
        that fade instead of dropping to zero.
        """
        i = bisect.bisect_right(self.starts, t) - 1
        if i < 0:
            return 0.0
        start, end = self.cues[i]
        if t >= end:
            return max(0.0, 1.0 - (t - end) / fall) if fall > 0 else 0.0
        value = min(1.0, (t - start) / rise) if rise > 0 else 1.0
        if i > 0 and fall > 0:
            value = max(value, 1.0 - (t - self.cues[i - 1][1]) / fall)
        return value


class BurstTrack:
    """One burst effect's moments."""
    def __init__(self, times):
        self.times = sorted(times)

    def recent(self, t, lifetime):
        """(index, age) for every burst that went off at most ``lifetime`` seconds before ``t``."""
        hi = bisect.bisect_right(self.times, t)
        lo = bisect.bisect_left(self.times, t - lifetime)
        return [(i, t - self.times[i]) for i in range(lo, hi)]


def effect_tracks(chart):
    """{kind: EffectTrack or BurstTrack} for every effect kind, empty ones included."""
    cues = chart.get("effects", ())
    tracks = {}
    for kind in EFFECT_KINDS:
        chosen = [cue for cue in cues if cue["kind"] == kind]
        if kind in BURST_EFFECTS:
            tracks[kind] = BurstTrack([cue["time"] for cue in chosen])
        else:
            tracks[kind] = EffectTrack([(cue["time"], cue["time"] + cue["length"]) for cue in chosen])
    return tracks


class ImpactTrack:
    """One reactive effect's spans, each with the side whose notes drive it.

    Unlike EffectTrack these are never merged: two spans that touch may name
    different sides, and which one is running is the whole point.
    """
    def __init__(self, cues):
        self.cues = sorted(cues)
        self.starts = [start for start, end, side in self.cues]

    def side_at(self, t):
        """The side driving at song time ``t``, or None when nothing is running."""
        i = bisect.bisect_right(self.starts, t) - 1
        if i >= 0 and t < self.cues[i][1]:
            return self.cues[i][2]
        return None

    def drives(self, t, side):
        """Whether a note landing on ``side`` at ``t`` should set this effect off."""
        chosen = self.side_at(t)
        return chosen is not None and chosen in ("both", side)


def impact_tracks(chart):
    """{kind: ImpactTrack} for every reactive kind, empty ones included."""
    cues = chart.get("effects", ())
    return {kind: ImpactTrack([(cue["time"], cue["time"] + cue["length"], cue.get("side", "opponent"))
                               for cue in cues if cue["kind"] == kind])
            for kind in REACTIVE_EFFECTS}


def chord_sizes(chart):
    """{side: {note time: how many notes land on it}}.

    A reactive effect scales with this, so the size is read off the chart rather
    than counted from the event stream: the player's own chord arrives as
    separate key presses, which would otherwise each look like a lone note.
    """
    rows = {"opponent": {}, "player": {}}
    for note in chart["notes"]:
        row = rows[note["side"]]
        key = round(note["time"], 3)
        row[key] = row.get(key, 0) + 1
    return rows


def measure_index(chart, t):
    """The 4-beat measure containing song time ``t``; negative before the grid."""
    return int(math.floor((t - chart["offset"]) * chart["bpm"] / 240.0 + .000001))


def camera_plan(chart):
    """One entry per 4-beat measure: who the stage camera frames.

    Auto framing follows whoever carries the measure; a close mix of both voices
    frames the pair. An empty measure keeps the previous framing. An authored
    camera event overrides only the measure containing it, so BPM or offset
    edits can never smear one override across the rest of the song.
    """
    measure = 240.0 / chart["bpm"]
    beat = measure / 4
    first = measure_index(chart, 0.0)
    last = max(first, measure_index(chart, chart["duration"]))
    weights = {}
    for note in chart["notes"]:
        side = weights.setdefault(measure_index(chart, note["time"]), {"opponent": 0.0, "player": 0.0})
        # A held beat is a sung beat: it counts as much as another tap would.
        side[note["side"]] += 1.0 + min(note["length"], measure) / beat
    overrides = dict((measure_index(chart, e["time"]), e["focus"]) for e in chart.get("camera", ()))
    auto = chart["notes"][0]["side"] if chart["notes"] else "center"
    plan = []
    for index in range(first, last + 1):
        side = weights.get(index)
        if side:
            big, small = max(side.values()), min(side.values())
            if small and big < 1.6 * small:
                auto = "center"
            else:
                auto = "opponent" if side["opponent"] > side["player"] else "player"
        start = chart["offset"] + index * measure
        plan.append(dict(index=index, start=start, end=start + measure, auto=auto,
                         focus=overrides.get(index, auto), override=index in overrides))
    return plan


def camera_focus(plan, chart, t):
    """Framing at song time ``t``; clamps before the first and after the last measure."""
    if not plan:
        return "center"
    i = measure_index(chart, t) - plan[0]["index"]
    return plan[max(0, min(len(plan) - 1, i))]["focus"]


class SongClock:
    """Audio-led monotonic clock, with a wall-clock fallback for muted audio.

    Audio backends can repeat a position for several frames. Interpolate only
    briefly between samples; a newly advancing audio sample is authoritative.
    A backward backend jump never re-judges notes. Pauses explicitly re-anchor
    the fallback, so time spent in an overlay cannot become chart time.
    """
    def __init__(self, now, start=0.0):
        self.position = float(start)
        self.anchor_position = float(start)
        self.anchor_wall = now
        self.last_audio = None
        self.last_audio_wall = now
        self.paused = False
        self.fallback = True

    def sample(self, now, audio_position=None):
        if self.paused:
            return self.position
        valid = audio_position is not None and math.isfinite(audio_position) and audio_position >= 0
        if valid and (self.last_audio is None or audio_position > self.last_audio + .00001):
            self.last_audio = float(audio_position)
            self.last_audio_wall = now
            self.anchor_position = self.last_audio
            self.anchor_wall = now
            self.fallback = False
        elif not valid or now - self.last_audio_wall > .20:
            self.fallback = True
        # The short interpolation bridges coarse audio callback positions.
        predicted = self.anchor_position + max(0, now - self.anchor_wall)
        self.position = max(self.position, predicted)
        return self.position

    def pause(self, now):
        self.paused = True

    def resume(self, now):
        self.anchor_position = self.position
        self.anchor_wall = now
        self.last_audio_wall = now
        self.paused = False


class RhythmSession:
    """Single-pass cursors per column; update cost depends on notes due now.

    Events are (kind, column, value, song time, timing error). Kinds: "hit",
    "miss", "break" and "ghost" for judged columns; "opponent" when Asahina
    sings a note on her own (column 4-7); "fanfare" with value "relit", "top"
    or "lost"; "rule" with the modifier whose rule a miss or rating broke.
    """
    def __init__(self, chart, practice=False, autoplay=False, start_time=0.0, modifiers=()):
        chart = normalize_chart(chart)
        self.modifiers = normalize_modifiers(modifiers)
        if "mirror" in self.modifiers:
            mirrored = [dict(note, lane=3 - note["lane"]) for note in chart["notes"]]
            mirrored.sort(key=lambda n: (n["time"], n["side"], n["lane"]))
            chart = dict(chart, notes=mirrored)
        self.chart = chart
        self.duet = "duet" in self.modifiers
        self.fights_back = "fights_back" in self.modifiers
        self.assisted = bool(self.modifiers & ASSIST_MODIFIERS)
        scale = WIDE_TIMING if "wide_timing" in self.modifiers else 1.0
        self.hit_window = HIT_WINDOW * scale
        self.tiers = tuple((window * scale, name, points, weight) for window, name, points, weight in TIERS)
        self.miss_damage = MISS_DAMAGE * (.5 if "half_damage" in self.modifiers else 1.0)
        self.notes = self.chart["notes"]
        self.times = [n["time"] for n in self.notes]
        self.states = [0] * len(self.notes)  # 0 pending, 1 hit, 2 missed, 3 skipped.
        self.columns = 8 if self.duet else 4
        self.lanes = [[] for unused in range(self.columns)]
        self.opponent = []
        for i, n in enumerate(self.notes):
            if n["time"] < start_time - .000001:
                self.states[i] = 3
            elif n["side"] == "player" or self.duet:
                self.lanes[column_of(n)].append(i)
            else:
                self.opponent.append(i)
        self.cursors = [0] * self.columns
        self.opponent_cursor = 0
        self.held = [False] * self.columns
        self.holds = {}
        self.practice, self.autoplay = bool(practice), bool(autoplay)
        self.start_time = start_time
        self.position = start_time
        self.health = .5
        self.score = self.combo = self.max_combo = self.misses = 0
        self.hits = self.judged = self.hold_hits = self.hold_total = 0
        self.weight = 0.0
        self.counts = dict((name, 0) for _, name, _, _ in TIERS)
        self.outcome = None
        self.fail_reason = None
        self.events = []
        self.fanfare = sorted((cue["time"], cue["time"] + cue["length"])
                              for cue in self.chart.get("effects", ()) if cue["kind"] == "fanfare")
        self.fanfare_starts = [start for start, end in self.fanfare]
        self.fanfare_window = None
        self.fanfare_lit = False
        self.fanfare_streak = 0
        self.fanfare_bonus = 0

    @property
    def accuracy(self):
        return 100.0 * self.weight / self.judged if self.judged else 0.0

    @property
    def rank(self):
        if self.outcome != "clear":
            return "-"
        if self.misses == 0 and self.accuracy >= 99.999:
            return "S+"
        for threshold, grade in ((95, "S"), (90, "A"), (80, "B"), (70, "C"), (60, "D")):
            if self.accuracy >= threshold:
                return grade
        return "E"

    def _emit(self, kind, column, value="", error=0.0):
        self.events.append((kind, column, value, self.position, error))

    def _fail(self, reason):
        if not self.practice and not self.outcome:
            self.outcome = "failed"
            self.fail_reason = reason

    def _break_rule(self, rule):
        # Practice keeps playing, but the stage still says which rule broke.
        self._emit("rule", -1, rule)
        self._fail(rule)

    def _damage(self, column, kind="miss", when=None):
        self.misses += 1
        self.combo = 0
        self.health = max(0, self.health - self.miss_damage)
        self._emit(kind, column, "MISS")
        self._fanfare_miss(when)
        if self.health <= 0:
            self._fail("health")
        for rule in ("no_miss", "flawless"):
            if rule in self.modifiers:
                self._break_rule(rule)

    # ---- fanfare ------------------------------------------------------------------

    def _fanfare_index(self, when):
        i = bisect.bisect_right(self.fanfare_starts, when + .000001) - 1
        if i >= 0 and when < self.fanfare[i][1] - .000001:
            return i
        return None

    def _fanfare_enter(self, when):
        """The window containing ``when``; the first judgment inside a window finds it lit."""
        i = self._fanfare_index(when)
        if i is not None and i != self.fanfare_window:
            self.fanfare_window, self.fanfare_lit, self.fanfare_streak = i, True, 0
        return i

    def _fanfare_multiplier(self):
        if not self.fanfare_lit:
            return 1
        return 3 if self.fanfare_streak >= FANFARE_TOP else 2

    def _fanfare_hit(self, when):
        if self._fanfare_enter(when) is None:
            return 1
        # The hit is scored as the fanfare stood before it.
        multiplier = self._fanfare_multiplier()
        self.fanfare_streak += 1
        if not self.fanfare_lit and self.fanfare_streak >= FANFARE_RELIGHT:
            self.fanfare_lit, self.fanfare_streak = True, 0
            self._emit("fanfare", -1, "relit")
        elif self.fanfare_lit and self.fanfare_streak == FANFARE_TOP:
            self._emit("fanfare", -1, "top")
        return multiplier

    def _fanfare_tick(self, when):
        if self._fanfare_enter(when) is None:
            return 1
        return self._fanfare_multiplier()

    def _fanfare_miss(self, when):
        if when is None or self._fanfare_enter(when) is None:
            return
        if self.fanfare_lit:
            self._emit("fanfare", -1, "lost")
        self.fanfare_lit, self.fanfare_streak = False, 0

    def fanfare_state(self, when):
        """(inside, lit, multiplier, streak) as a judgment at song time ``when`` would find it."""
        i = self._fanfare_index(when)
        if i is None:
            return False, False, 1, 0
        if i != self.fanfare_window:
            return True, True, 2, 0
        return True, self.fanfare_lit, self._fanfare_multiplier(), self.fanfare_streak

    # ---- judgment -----------------------------------------------------------------

    def _hit(self, index, t):
        note = self.notes[index]
        column = column_of(note)
        error = t - note["time"]
        for window, name, points, weight in self.tiers:
            if abs(error) <= window + .0000001:
                break
        self.states[index] = 1
        multiplier = self._fanfare_hit(note["time"])
        self.score += points * multiplier
        self.fanfare_bonus += points * (multiplier - 1)
        self.combo += 1
        self.max_combo = max(self.combo, self.max_combo)
        self.hits += 1
        self.judged += 1
        self.weight += weight
        self.counts[name] += 1
        self.health = min(1.0, self.health + .018 * max(.25, weight))
        self._emit("hit", column, name, error)
        if note["length"] > RELEASE_GRACE:
            # A short tail still gets one tick at its exact endpoint.
            self.holds[column] = dict(index=index, end=note["time"] + note["length"],
                tick=note["time"] + min(HOLD_TICK, note["length"]), broken=False, released=None)
        if name != "SICK!" and "flawless" in self.modifiers:
            self._break_rule("flawless")

    def press(self, lane, t):
        if self.outcome or not 0 <= lane < self.columns or self.held[lane]:
            return
        self.update(t)
        if self.outcome:
            return
        self.held[lane] = True
        if lane in self.holds:
            self.holds[lane]["released"] = None
        entries, cursor = self.lanes[lane], self.cursors[lane]
        if cursor < len(entries):
            index = entries[cursor]
            if abs(t - self.notes[index]["time"]) <= self.hit_window + .0000001:
                self._hit(index, t)
                self.cursors[lane] += 1
                return
        # Empty taps are safe only outside a player's phrase, meaning no lane's
        # next note is within 0.4 s. Repeated held keydown events cannot score,
        # and mashing through a phrase costs HP.
        nearby = any(self.cursors[l] < len(self.lanes[l]) and
            abs(self.notes[self.lanes[l][self.cursors[l]]]["time"] - t) < .40 for l in range(self.columns))
        if nearby and lane not in self.holds:
            self.judged += 1
            self._damage(lane, "ghost", t)

    def release(self, lane, t):
        if not 0 <= lane < self.columns:
            return
        self.update(t)
        self.held[lane] = False
        if lane in self.holds:
            self.holds[lane]["released"] = t

    def clear_keys(self):
        # Focus loss uses this while paused. A resume grace window lets a
        # player put their fingers back on an in-progress sustain.
        self.held = [False] * self.columns
        for hold in self.holds.values():
            hold["released"] = self.position + .20

    def update(self, t, opponent_time=None):
        if self.outcome:
            return
        t = max(self.position, t)
        self.position = t
        while self.opponent_cursor < len(self.opponent):
            index = self.opponent[self.opponent_cursor]
            note = self.notes[index]
            if note["time"] > (t if opponent_time is None else opponent_time):
                break
            self.opponent_cursor += 1
            self.states[index] = 1
            self._emit("opponent", column_of(note), note["length"])
            if self.fights_back and self.health > FIGHT_FLOOR:
                self.health = max(FIGHT_FLOOR, self.health - FIGHT_DRAIN)
        for lane in range(self.columns):
            entries = self.lanes[lane]
            while self.cursors[lane] < len(entries):
                index = entries[self.cursors[lane]]
                note = self.notes[index]
                if self.autoplay and note["time"] <= t:
                    self.held[lane] = True
                    self._hit(index, note["time"])
                    self.cursors[lane] += 1
                    if self.outcome:
                        return
                elif note["time"] + self.hit_window < t - .0000001:
                    self.states[index] = 2
                    self.cursors[lane] += 1
                    self.judged += 1
                    if note["length"] > RELEASE_GRACE:
                        missed_ticks = int(math.ceil(note["length"] / HOLD_TICK - .0000001))
                        self.hold_total += missed_ticks
                        self.judged += missed_ticks
                    self._damage(lane, "miss", note["time"])
                    if self.outcome:
                        return
                else:
                    break
        for lane, hold in list(self.holds.items()):
            while hold["tick"] <= t + .0000001:
                tick = hold["tick"]
                self.hold_total += 1
                self.judged += 1
                grace = hold["released"] is not None and tick - hold["released"] <= RELEASE_GRACE
                if self.held[lane] or grace or self.autoplay:
                    multiplier = self._fanfare_tick(tick)
                    self.hold_hits += 1
                    self.weight += 1
                    self.score += 25 * multiplier
                    self.fanfare_bonus += 25 * (multiplier - 1)
                    self.health = min(1.0, self.health + .002)
                elif not hold["broken"]:
                    hold["broken"] = True
                    self._damage(lane, "break", tick)
                if tick >= hold["end"] - .000001:
                    del self.holds[lane]
                    break
                hold["tick"] = min(hold["end"], tick + HOLD_TICK)
            if self.outcome:
                return
        if t >= self.chart["duration"] + HIT_WINDOW:
            self.outcome = "clear"

    def visible_indices(self, t, lookahead=2.0):
        # Holds can begin outside the visible time window. Include the few
        # active holds separately, without walking the entire chart per frame.
        lo = bisect.bisect_left(self.times, t - .25)
        hi = bisect.bisect_right(self.times, t + lookahead)
        return range(lo, hi)

    def snapshot(self):
        return dict(outcome=self.outcome or "quit", score=self.score,
            accuracy=round(self.accuracy, 2), misses=self.misses,
            max_combo=self.max_combo, combo=self.combo, rank=self.rank,
            practice=self.practice, autoplay=self.autoplay, start_time=self.start_time,
            eligible=bool(any(self.lanes)) and not (self.practice or self.autoplay or self.assisted
                                                    or self.start_time > 0),
            chart_id=self.chart["id"], title=self.chart["title"], counts=dict(self.counts),
            hold_hits=self.hold_hits, hold_total=self.hold_total, hits=self.hits,
            modifiers=sorted(self.modifiers), assisted=self.assisted, duet=self.duet,
            fail_reason=self.fail_reason, fanfare_bonus=self.fanfare_bonus)
