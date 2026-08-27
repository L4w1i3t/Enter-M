# =============================================================================
# perf.rpy  --  MATSUDA'S SICK BOSS FIGHT :: FRAME BUDGET
# =============================================================================
#
# WHAT THIS FILE IS
#   Two things every fight in this folder shares, and nothing else:
#
#   1. A LIVE FRAME PROFILER (F3 in any fight). Frame time, the worst frame in
#      the last few seconds, how many screen executions per second, and the
#      Python cost of whichever creator-defined displayable is driving the
#      mode. Plus a rolling graph, because a mean frame time cannot tell you
#      the difference between "slow" and "hitching", and hitching is what a
#      player actually feels.
#
#   2. A GRAPHICS BUDGET (persistent.msbf_gfx). One dial, four stops, read by
#      the modes to decide how much the picture is allowed to cost.
#
# WHY A PROFILER AND NOT JUST A FPS COUNTER
#   Matsu'Py is single-threaded Python driving a GL renderer, so a dropped
#   frame in a fight is almost always one of exactly four things:
#
#     * a SCREEN EXECUTION -- something called restart_interaction (a timer, a
#       SetScreenVariable, a hover) and the entire battle screen was rebuilt
#       from source: every Transform, every Text, every button. This is the
#       expensive one, it is spiky rather than sustained, and it is invisible
#       to a frames-per-second average.
#     * a CDD's own render() -- the danmaku stages draw a few hundred sprites
#       from Python every frame.
#     * a RENDER-TO-TEXTURE -- every `mesh True` allocates a texture at the
#       DRAWABLE resolution and copies the framebuffer into it, so a fullscreen
#       1440p window pays four times what a 720p window pays for the same
#       effect.
#     * plain fragment cost -- the full-screen shaders.
#
#   The readout names all four so a drop can be attributed instead of guessed
#   at. `SCR/s` climbing into double digits is the screen-execution case;
#   `SIM`/`DRAW` climbing is the CDD case; a high steady frame time with both
#   of those flat is the GPU.
#
# THE GRAPHICS BUDGET, AND THE ONE RULE BEHIND IT
#   Cutting the internal resolution of an effect is free ONLY IF THE EFFECT HAS
#   NO DETAIL TO LOSE. A fog field whose whole signal is three or four soft
#   blobs across the frame looks identical rendered at 720p and blown up; a
#   grid of one-pixel hairlines converging on a vanishing point does not, and
#   neither do scanlines, film grain, or a row-tear glitch. So the budget sorts
#   effects into those two families and only ever scales the first one by
#   default:
#
#     ultra        (default) native resolution for everything. Nothing is
#                  wrapped, nothing is softened, and above 720p the fights cost
#                  exactly what they cost. This is the stop the fights are
#                  authored at.
#     high         no effect renders above 1280x720 internally. At a 720p
#                  window this is a no-op; at 1080p it is 2.25x less fragment
#                  work on the wrapped passes, at 1440p 4x. Sprites, text and
#                  every piece of UI are untouched -- only the procedural
#                  layers are capped.
#     performance  low-frequency at 768x432, high-frequency at 960x540, and
#                  the optional decoration passes are dropped outright.
#
#   ULTRA IS THE DEFAULT ON PURPOSE. Capping is a real (if small) trade of
#   sharpness for headroom, and a fight should look the way it was authored
#   until somebody asks otherwise. Everything else this codebase does for frame
#   rate -- the tick-rate draw governors on the danmaku stages, the arena's
#   horizon branch, the culls -- costs nothing at all and is always on.
#
#   Nothing here ever turns a shader OFF -- MSBF_FX_SHADERS / MSBF_ARENA_SHADERS
#   already own that, and they are about whether gl2 registered the shader at
#   all, not about taste.
#
# HOW THE CAP IS IMPLEMENTED (verified against the 8.1.1 SDK)
#   `Transform(child, mesh=True)` makes gl2 render the child to a texture and
#   then draw that texture as a model with the custom shader. The texture's
#   size comes from `properties["drawable_resolution"]` in gl2texture.pyx --
#   True (the default) means "the size this occupies on the physical display",
#   False means "exactly the virtual size". And the SHADER runs during that
#   render-to-texture pass, at that viewport (gl2texture.GLTexture.from_render
#   sets `glViewport(0, 0, tw, th)` before drawing).
#
#   So wrapping an effect in an OUTER mesh with gl_drawable_resolution False
#   pins the whole inner pass -- shader included -- to a fixed pixel budget no
#   matter how big the window is, and the outer draw scales the result back up.
#   `u_model_size` is taken from the render's virtual size, so shaders that use
#   it do not change behaviour; only their sampling density does.
#
# =============================================================================


# The four stops. Ordered cheapest-picture-last, which is the order the
# settings row shows them in.
define MSBF_GFX_LEVELS = ("ultra", "high", "performance")

# Internal-resolution caps, as (low_frequency, high_frequency) scale factors
# against the 1280x720 virtual frame. 1.0 means "1280x720 at most"; None means
# "no cap at all, render at the physical resolution".
define MSBF_GFX_CAPS = {
    "ultra":       (None, None),
    "high":        (1.00, 1.00),
    "performance": (0.60, 0.75),
}

# Whether a level still draws the optional decoration passes (extra particle
# layers, second-order glows -- anything a mode marks as garnish).
define MSBF_GFX_GARNISH = {
    "ultra": True, "high": True, "performance": False,
}

default persistent.msbf_gfx = "ultra"

# Draw-rate ceiling for the stages that DO interpolate between simulation ticks
# (the phase-3 shmup). Expressed as a period because renpy.redraw takes a delay:
# the engine wakes at the first vblank at or after it, so a 60Hz display is
# unaffected and only a high-refresh one is throttled.
define MSBF_DRAW_PERIOD = 1.0 / 90.0

# NovaSquare for the readout, not the display face: SF Automaton draws a 1 as a
# bare vertical bar, and every number on this panel is a measurement.
define MSBF_PERF_FONT = "assets/fonts/NovaSquare-Regular.ttf"

# The profiler is off until asked for, and it is not remembered across runs --
# it forces a continuous redraw to sample, which is not a state to leave a
# player stuck in by accident.
default msbf_perf_on = False


init -20 python:

    import time as _msbf_perf_time

    # --- THE SAMPLER ---------------------------------------------------------

    class MSBFPerf(object):
        """
        Rolling frame-time record plus a set of named cost marks.

        Every method is written to be safe to call when the profiler is OFF,
        because the call sites are inside render loops: `if MSBF_PERF.on:` is
        one attribute lookup and a branch, which is the entire price of leaving
        the instrumentation in shipping code.
        """

        # Frames kept for the graph. 180 at 60fps is three seconds, which is
        # about as long as a person can hold "that felt bad" in mind.
        WINDOW = 180

        def __init__(self):
            self.on = False
            self.reset()

        def reset(self):
            self.times = []          # frame durations in ms, newest last
            self._last = None
            self.marks = {}          # name -> [last_ms, ema_ms]
            self.counts = {}         # name -> events since the last rollover
            self.rates = {}          # name -> events/sec, from the last second
            self._rate_at = None
            self.notes = {}          # name -> a bare number to print
            self.worst = 0.0
            self.hitches = 0
            self.frames = 0

        # ----- per-frame ------------------------------------------------------

        def frame(self):
            """Called once per drawn frame by MSBFPerfGraph.render."""

            now = _msbf_perf_time.perf_counter()

            if self._last is not None:
                dt = (now - self._last) * 1000.0
                # A frame longer than a quarter second is the game having been
                # away (a load, a transition, alt-tab), not a slow frame.
                if 0.0 < dt < 250.0:
                    times = self.times
                    times.append(dt)
                    if len(times) > self.WINDOW:
                        del times[:-self.WINDOW]
                    self.frames += 1
                    if dt > self.worst:
                        self.worst = dt

            self._last = now

            if self._rate_at is None:
                self._rate_at = now
            elif now - self._rate_at >= 1.0:
                span = now - self._rate_at
                self.rates = dict(
                    (k, v / span) for k, v in self.counts.items())
                self.counts = {}
                self._rate_at = now
                # The worst frame is a three-second-ish claim, so it decays
                # rather than standing forever after one hitch on load.
                self.worst = self.p_high() or 0.0

        # ----- what the readout prints ---------------------------------------

        def mean(self):
            times = self.times
            if not times:
                return 0.0
            return sum(times) / len(times)

        def p_high(self):
            """
            The 95th-percentile frame, which is the number that matches what a
            player calls "smooth". A mean hides one 40ms frame per second
            completely; this does not.
            """
            times = self.times
            if not times:
                return 0.0
            ordered = sorted(times)
            return ordered[min(len(ordered) - 1, int(len(ordered) * 0.95))]

        def fps(self):
            m = self.mean()
            return (1000.0 / m) if m > 0.0 else 0.0

        # ----- named marks ----------------------------------------------------

        def mark(self, name, ms):
            """Record a timed section, in milliseconds."""
            slot = self.marks.get(name)
            if slot is None:
                self.marks[name] = [ms, ms]
            else:
                slot[0] = ms
                # Heavy smoothing: these are read while the numbers are moving,
                # and an unsmoothed per-frame figure is unreadable.
                slot[1] += (ms - slot[1]) * 0.08

        def count(self, name, n=1):
            """Record an event, reported as a per-second rate."""
            self.counts[name] = self.counts.get(name, 0) + n

        def note(self, name, value):
            """Record a plain number to display as-is (bullet counts, etc)."""
            self.notes[name] = value

        def rate(self, name):
            return self.rates.get(name, 0.0)

        def ms(self, name):
            slot = self.marks.get(name)
            return slot[1] if slot else 0.0

    MSBF_PERF = MSBFPerf()

    # Guard against the same F3 press being handled twice. Several fight
    # screens are up at once (the battle screen AND the shmup overlay, say) and
    # each of them `use enter_m_input_lock()`, so the key is bound more than
    # once; a Keymap action that returns None lets the event keep propagating,
    # and the second binding would toggle straight back off.
    _msbf_perf_last_toggle = -99.0

    def msbf_perf_toggle():
        """F3. Clears the record on the way in so the first reading is live."""

        now = _msbf_perf_time.perf_counter()
        if now - store._msbf_perf_last_toggle < 0.25:
            return
        store._msbf_perf_last_toggle = now

        store.msbf_perf_on = not store.msbf_perf_on
        MSBF_PERF.on = store.msbf_perf_on
        MSBF_PERF.reset()

        if store.msbf_perf_on:
            renpy.show_screen("msbf_perf_hud")
        else:
            renpy.hide_screen("msbf_perf_hud")
        renpy.restart_interaction()

    def msbf_perf_t0():
        """Start a timed section. Returns a stamp for msbf_perf_t1."""
        return _msbf_perf_time.perf_counter()

    def msbf_perf_t1(name, t0):
        MSBF_PERF.mark(name, (_msbf_perf_time.perf_counter() - t0) * 1000.0)


init -19 python:

    # --- THE GRAPHICS BUDGET -------------------------------------------------

    # The stop a profile falls back to. Deliberately the same string as the
    # `default persistent.msbf_gfx` above -- an earlier build shipped a
    # "balanced" stop, and a profile still carrying it has to repair to what a
    # fresh profile would have had, not to some other stop.
    MSBF_GFX_FALLBACK = "ultra"

    def msbf_gfx_level():
        """The validated budget stop. Repairs a profile carrying a dead value."""
        level = getattr(persistent, "msbf_gfx", MSBF_GFX_FALLBACK)
        if level not in MSBF_GFX_LEVELS:
            level = MSBF_GFX_FALLBACK
            persistent.msbf_gfx = level
        return level

    def msbf_gfx_garnish():
        """False when the budget says to drop optional decoration passes."""
        return MSBF_GFX_GARNISH.get(msbf_gfx_level(), True)

    def msbf_draw_overscale():
        """
        How much bigger the physical frame is than the 1280x720 virtual one.

        1.0 in a 720p window, 1.5 at 1080p, 2.0 at 1440p, 3.0 at 4K. Read from
        the live drawable transform rather than from the window size, so it is
        the same number gl2texture will use to size a render target.
        """
        try:
            draw = renpy.display.draw
            w, h = draw.virt_to_draw.transform(1280.0, 720.0)
            return max(abs(w) / 1280.0, abs(h) / 720.0)
        except Exception:
            return 1.0

    def msbf_fx_scaled(d, w=1280, h=720, high_freq=False):
        """
        Cap the internal resolution an effect is rendered at.

        `d` is a displayable that already carries its own mesh/shader --
        typically `At(Solid("#00000000"), <a shader transform>)`. `w`/`h` are
        the virtual size it should occupy on screen.

        THIS HELPER OWNS THE SIZING. It always returns something already sized
        to (w, h), so a call site must NOT also set xysize -- position it
        (xcenter / ycenter / xpos) and nothing else. Doing the sizing in here is
        exactly what lets the scaled path hand the effect a SMALLER size than
        the one it ends up drawn at.

        Pass high_freq=True for anything whose output carries detail at the
        pixel scale: hairlines, scanlines, grain, row tears. Those get the more
        conservative cap.

        Returns a plainly-sized wrapper whenever a cap would not actually save
        anything, so a 720p window never pays for the extra pass. And the wrap
        is only ever worth it on genuinely expensive fragment work: it costs a
        texture allocation, a framebuffer copy and a full-screen blit, which is
        more than a gradient would have cost unwrapped. Reserve it for shaders
        that do real per-pixel work -- the arena and the atmosphere field.
        """

        size = (int(w), int(h))

        caps = MSBF_GFX_CAPS.get(msbf_gfx_level(), (None, None))
        cap = caps[1] if high_freq else caps[0]

        if cap is None:
            return Transform(d, xysize=size)

        over = msbf_draw_overscale()
        if over <= cap * 1.01:
            # The physical frame is already at or below the cap: wrapping it
            # would cost an extra pass and save nothing.
            return Transform(d, xysize=size)

        iw = max(2, int(round(w * cap)))
        ih = max(2, int(round(h * cap)))

        # INNER: the effect, offered the reduced size, so its shader runs over
        # a smaller quad. OUTER: a mesh whose render-to-texture is pinned to the
        # virtual size (gl_drawable_resolution False -- see the header), scaled
        # back up. Two transforms and not one, because the inner has to be a
        # finished render before the outer can be told how big its texture may
        # be.
        return Transform(
            Transform(d, xysize=(iw, ih)),
            mesh=True,
            gl_drawable_resolution=False,
            zoom=(float(w) / iw),
            subpixel=True,
        )


# -----------------------------------------------------------------------------
# THE READOUT
# -----------------------------------------------------------------------------
# The graph is a creator-defined displayable for two reasons. It is the only
# thing on screen that legitimately wants a frame every frame, so it is also
# the natural place to take the sample; and 180 bars drawn as 180 Solids would
# make the profiler the most expensive thing in the fight.
# -----------------------------------------------------------------------------
init python:

    class MSBFPerfGraph(renpy.Displayable):

        # One Solid per colour, reused for every bar. Class-level so it
        # survives the displayable being rebuilt by a screen execution.
        _solids = {}

        def __init__(self, width=248, height=54, **kwargs):
            super(MSBFPerfGraph, self).__init__(**kwargs)
            self.gw = width
            self.gh = height

        def _solid(self, color):
            d = MSBFPerfGraph._solids.get(color)
            if d is None:
                d = Solid(color)
                MSBFPerfGraph._solids[color] = d
            return d

        def render(self, width, height, st, at):
            MSBF_PERF.frame()

            gw = self.gw
            gh = self.gh
            rv = renpy.Render(gw, gh)

            # One render per colour per frame, blitted at many sizes. A Render
            # can be blitted repeatedly, but it may not be kept past this call.
            cache = {}

            def bar(color, x, y, w, h):
                if h < 1:
                    h = 1
                key = (color, int(w), int(h))
                r = cache.get(key)
                if r is None:
                    r = renpy.render(self._solid(color), int(w), int(h), st, at)
                    rv.depends_on(r)
                    cache[key] = r
                rv.blit(r, (int(x), int(y)))

            bar("#00000099", 0, 0, gw, gh)

            # The 16.7ms line: the only reference mark that matters, because a
            # bar over it is a frame that missed 60Hz.
            budget = 1000.0 / 60.0
            # Scale so the budget line sits a third of the way up, which keeps
            # ordinary frames low and makes a spike unmissable.
            span = budget * 3.0
            budget_y = gh - int(gh * (budget / span))
            bar("#55ddff44", 0, budget_y, gw, 1)

            times = MSBF_PERF.times
            if times:
                n = min(len(times), gw)
                start = len(times) - n
                for i in range(n):
                    ms = times[start + i]
                    h = int(gh * min(1.0, ms / span))
                    if ms > budget * 2.0:
                        col = "#ff3868"
                    elif ms > budget:
                        col = "#ffcf66"
                    else:
                        col = "#66e08a"
                    bar(col, gw - n + i, gh - h, 1, h)

            renpy.redraw(self, 0)
            return rv


screen msbf_perf_hud():
    zorder 32000

    # Counting this screen's own executions is the whole point of it being a
    # screen: every restart_interaction anywhere re-runs every shown screen, so
    # this body running IS one screen execution, and the rate it runs at is the
    # rate the battle screen is being rebuilt at.
    $ MSBF_PERF.count("screen")

    frame:
        xpos 1016
        ypos 8
        xsize 256
        background Solid("#02060cd8")
        padding (8, 6)

        vbox:
            spacing 2

            text "FRAME BUDGET  --  F3" size 11 color "#55ddff" font MSBF_PERF_FONT

            add MSBFPerfGraph(240, 54)

            $ _pf_mean = MSBF_PERF.mean()
            $ _pf_p95 = MSBF_PERF.p_high()
            $ _pf_fps = MSBF_PERF.fps()

            use msbf_perf_row("FRAME", "%.1f ms   %d fps" % (_pf_mean, int(_pf_fps)),
                              "#66e08a" if _pf_mean <= 16.7 else "#ffcf66")
            use msbf_perf_row("95th", "%.1f ms" % _pf_p95,
                              "#66e08a" if _pf_p95 <= 16.7 else ("#ffcf66" if _pf_p95 <= 33.3 else "#ff3868"))
            use msbf_perf_row("SCR/s", "%.0f" % MSBF_PERF.rate("screen"),
                              "#66e08a" if MSBF_PERF.rate("screen") < 8 else "#ffcf66")

            $ _pf_sim = MSBF_PERF.ms("sim")
            $ _pf_draw = MSBF_PERF.ms("draw")
            if _pf_sim > 0.0 or _pf_draw > 0.0:
                use msbf_perf_row("SIM", "%.2f ms" % _pf_sim, "#9aa8bd")
                use msbf_perf_row("DRAW", "%.2f ms" % _pf_draw, "#9aa8bd")

            for _pf_k, _pf_v in sorted(MSBF_PERF.notes.items()):
                use msbf_perf_row(_pf_k.upper(), "%s" % _pf_v, "#6f7f95")

            use msbf_perf_row("GFX", "%s  x%.2f" % (msbf_gfx_level(), msbf_draw_overscale()), "#6f7f95")


screen msbf_perf_row(label, value, color):
    hbox:
        xfill True
        text label size 11 color "#6f7f95" font MSBF_PERF_FONT
        text value size 11 color color font MSBF_PERF_FONT xalign 1.0
