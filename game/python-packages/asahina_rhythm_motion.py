"""Timing for Asarhythm's original whole-body drawings; no Ren'Py dependency."""

import math


# Bounded registration of the original drawings' stance, in native pixels.
# Two planted shoes have equal weight, regardless of shoe size or ink area.
# Lifted-leg hey/win drawings were reviewed at the pelvis instead: counting
# only their remaining bottom shoe pulls the whole body sideways by 40px.
# No runtime image analysis or per-pose resizing changes these authored poses.
STANCE_OFFSETS = {
    "asahina": {
        "idle": (12, 2, -5, 7), "left": (-13, -14, -14, -21),
        "down": (-2, 4, 4, 1), "up": (8, -4, -4, -2),
        "right": (16, 7, 4, 5), "miss": (-24, 2, 6, 5),
        "hey": (-12, -13, -9, -4), "win": (-7, 0), "lose": (10, 0),
    },
    "asahiko": {
        "idle": (-9, -11, -13, -12), "left": (-18, -13, -19, -22),
        "down": (-7, -9, -11, -8), "up": (-7, -6, -7, -4),
        "right": (-7, 7, 10, -4), "miss": (-4, -4, -9, -7),
        "hey": (-7, -2, 0, -7), "win": (-6, -1), "lose": (-4, -16),
    },
}


def sequence_frame(age, frames, durations):
    """Loop an explicitly timed sequence without accumulating render-frame dt."""
    phase = max(0.0, float(age)) % sum(durations)
    for frame, duration in zip(frames, durations):
        if phase < duration:
            return frame
        phase -= duration
    return frames[-1]


class SingerFrames:
    IDLE_FRAMES = {"asahina": (1, 0, 2, 3, 0),
                   "asahiko": (2, 0, 1, 3, 0)}
    COUNTS = {"idle": 4, "left": 4, "down": 4, "up": 4, "right": 4,
              "miss": 4, "hey": 4, "win": 2, "lose": 2}

    def __init__(self, name="asahina"):
        self.idle_frames = self.IDLE_FRAMES[name]
        self.pose = "idle"
        self.began = 0.0
        self.event = None
        self.time = None
        self.held = False
        self.loop_period = 1.2
        self.beat_len = .5
        self.gesture_time = .30

    def set_pose(self, pose, now, event=None, held=False, duration=None):
        pose = pose if pose in self.COUNTS else "idle"
        now = float(now)
        rewind = self.time is not None and now < self.time
        gesture_time = .30 if duration is None else max(.12, min(.30, float(duration) * .8))
        # A sustain keeps one event and never toggles attack drawings every
        # 50 ms at 300 BPM. Fresh sung notes replay anticipation->attack->settle.
        fresh_note = pose != "idle" and event != self.event
        # Every distinct hit restarts, including repeated hits on one arrow.
        # Rendering or ticking the same sustain keeps its event and does not.
        if self.time is None or rewind or pose != self.pose or fresh_note:
            self.began = now
        self.pose, self.event, self.time, self.held = pose, event, now, bool(held)
        self.gesture_time = gesture_time

    def sample(self, now, beat=None):
        age = max(0.0, float(now) - self.began)
        beat_len = max(.05, self.beat_len)
        beat = float(now) / beat_len if beat is None else float(beat)
        if self.pose == "idle":
            # Land each singer's designated beat pose every two beats.
            # Use the song's supplied beat, so re-entering idle stays in phase.
            phase = ((beat + 1e-9) % 2.0) / 2.0
            frame = sequence_frame(phase, self.idle_frames, (.16, .20, .20, .24, .20))
        elif self.pose in ("win", "lose"):
            period = max(1.2, self.loop_period)
            frame = sequence_frame(age, (0, 1), (period * .55, period * .45))
        else:
            # Four drawings remain readable, then the fourth rests on the hold.
            phase = age / self.gesture_time
            frame = 0 if phase < .25 else 1 if phase < .60 else 2 if phase < 1.0 else 3
        # Shared across poses: a note never resets the beat-locked compression.
        # Less than two pixels at head height, with the floor anchored at y=430.
        sy = 1.0 - .004 * (.5 + .5 * math.cos(beat * math.pi))
        return frame, sy
