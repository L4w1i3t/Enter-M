# =============================================================================
# ENTER-M :: FRAME RATE CAP
# -----------------------------------------------------------------------------
# Matsu'Py ships with no frame rate cap: `preferences.gl_framerate` defaults to
# None, which makes the GL swap interval 1, which means the game renders at the
# monitor's full refresh rate. On a 240Hz panel that is 240 frames per second of
# a shader-heavy scene -- four times the work needed, and a source cadence no
# 60fps screen-capture encoder (Discord, OBS) can resample cleanly. Fullscreen
# makes it worse: every `mesh True` render target is allocated at *drawable*
# resolution (renpy/gl2/gl2texture.pyx, `drawable_resolution` defaults True), so
# 1280x720 -> 1920x1080 is 2.25x the fragment work on the whole stack.
#
# THE ENGINE ONLY OFFERS DIVISORS. Matsu'Py does not pace frames in software; it
# picks a GL swap interval `n` and lets vsync do the limiting:
#
#     sync_frames = int(round(refresh_rate) / gl_framerate)     # min 1
#
# so the only achievable rates are refresh/1, refresh/2, refresh/3, ... A slider
# that offered a free 30..240 choice would be lying -- asking for 100fps on a
# 240Hz panel silently gives you 120. Instead the slider walks the divisors that
# land at or above ENTER_M_FPS_FLOOR, and the readout states what you actually
# get. `enter_m_fps_target_for` inverts the engine's formula so the stored
# preference is guaranteed to produce the divisor we picked.
#
# RESTART REQUIRED. The swap interval is applied by GL2Draw.init() via
# `pygame.display.gl_set_attribute(GL_SWAP_CONTROL, vsync)`, and init() runs
# exactly once, from Interface.set_mode() at startup. The built-in
# `Preference("gl framerate", n)` action pairs itself with `_DisplayReset()`,
# but a display reset only re-runs on_resize() -- it never re-enters init() --
# so in stock 8.1.1 nothing re-applies the interval mid-session. The setting is
# therefore stored now and honoured on the next launch; the UI says so.
# (Fixing that properly belongs in the engine: on display reset, re-run the
# framerate selection and call SDL_GL_SetSwapInterval on the live context.)
# =============================================================================

# The slowest cap offered. Divisors that fall below this are not shown.
define ENTER_M_FPS_FLOOR = 30

# The cap applied on a fresh profile, in frames per second. Snapped to the
# nearest divisor the player's monitor can actually produce.
define ENTER_M_FPS_DEFAULT = 60

# Stand-in refresh rate used only to draw a sane slider if the display has not
# reported one. Never used to choose the stored default -- see the migration.
define ENTER_M_FPS_FALLBACK_RATE = 60

# VSync modes. "on" = sync to the display; "adaptive" = tear instead of stalling
# when a frame lands late (negative swap interval); "off" = no sync AND no cap.
define ENTER_M_VSYNC_MODES = ("on", "adaptive", "off")
default persistent.enter_m_vsync = "on"


init python:

    def enter_m_fps_raw_refresh_rate():
        """
        The refresh rate the *engine* will divide, as an int. 0 = not readable.

        Deliberately reads renpy.display.get_info() rather than
        renpy.get_refresh_rate(): get_refresh_rate() rounds to a multiple of 5
        (239 -> 240), but GL2Draw.init() divides the raw value. Rounding here
        would compute a target that misses the divisor we intended. get_info()
        caches its pygame.display.Info() in a module global, so this returns the
        identical object the renderer reads later.

        Returns 0 rather than a guess when the display has not reported a rate.
        Callers that need a number to draw a slider with can use
        enter_m_fps_refresh_rate(); the *migration* must not, because a made-up
        rate picks a wrong stop and then persists it forever. See below.
        """

        try:
            return int(renpy.display.get_info().refresh_rate or 0)
        except Exception:
            return 0

    def enter_m_fps_refresh_rate():
        """Refresh rate for building the slider, falling back to 60Hz."""

        return enter_m_fps_raw_refresh_rate() or ENTER_M_FPS_FALLBACK_RATE

    def enter_m_fps_target_for(rate, n):
        """
        The `gl_framerate` value that makes the engine choose swap interval `n`.

        The engine computes int(round(rate) / target), so any target in
        (rate/(n+1), rate/n] selects `n`. Integer-flooring rate/n lands inside
        that window for every realistic refresh rate. Verified against 60, 75,
        120, 144, 165, 239, 240 and 360Hz for every divisor down to 30fps.
        """

        return None if n <= 1 else max(rate // n, 1)

    def enter_m_fps_stops():
        """
        Selectable caps for the current monitor, slowest first.

        Each entry is (gl_framerate value, resulting fps). The last entry is
        always (None, refresh_rate) -- uncapped. Cached on the function itself
        rather than in a store variable so it is not dragged through rollback or
        written into saves; it is keyed by refresh rate, so it rebuilds by
        itself if the player moves the window to another monitor.
        """

        rate = enter_m_fps_refresh_rate()

        cache = getattr(enter_m_fps_stops, "cache", None)
        if cache is not None and cache[0] == rate:
            return cache[1]

        stops = []
        seen = set()

        n = 1
        while True:
            actual = rate / float(n)
            if actual < ENTER_M_FPS_FLOOR:
                break

            target = enter_m_fps_target_for(rate, n)
            if target not in seen:
                seen.add(target)
                stops.append((target, actual))

            n += 1

        # Built fastest-first; the slider reads slowest-first.
        stops.reverse()

        enter_m_fps_stops.cache = (rate, stops)
        return stops

    def enter_m_fps_nearest_index(fps):
        """
        Index of the stop whose real frame rate is closest to `fps`.

        Ties break toward the *faster* stop. Divisors are sparse enough that
        exact ties are common -- a 144Hz panel is equidistant from 48 and 72
        when aiming at 60 -- and picking the slower one there would cap the game
        well under the requested rate for no reason.
        """

        stops = enter_m_fps_stops()
        return min(
            range(len(stops)),
            key=lambda i: (abs(stops[i][1] - fps), -stops[i][1]),
        )

    def enter_m_fps_index():
        """
        Slider position for the stored preference.

        A profile can hold a `gl_framerate` that is not one of our stops -- set
        on a different monitor, or by an older build. Rather than reset it,
        push it through the engine's own formula to find the rate it would
        actually produce here, and select the stop closest to that.
        """

        stops = enter_m_fps_stops()
        current = renpy.game.preferences.gl_framerate

        for i, (target, _actual) in enumerate(stops):
            if target == current:
                return i

        if current is None:
            return len(stops) - 1

        rate = enter_m_fps_refresh_rate()
        try:
            n = max(int(round(1.0 * rate) / current), 1)
        except (TypeError, ZeroDivisionError):
            return len(stops) - 1

        return enter_m_fps_nearest_index(rate / float(n))

    def enter_m_fps_set_index(index):
        """Store the cap for slider position `index`."""

        stops = enter_m_fps_stops()
        index = max(0, min(int(index), len(stops) - 1))
        renpy.game.preferences.gl_framerate = stops[index][0]

    def enter_m_fps_label():
        """Readout for the current stop, e.g. '60 FPS' or 'Uncapped (240 FPS)'."""

        target, actual = enter_m_fps_stops()[enter_m_fps_index()]

        if target is None:
            return __("Uncapped (%d FPS)") % round(actual)

        return __("%d FPS") % round(actual)

    def enter_m_fps_needs_restart():
        """
        True when the stored cap is not the one the renderer is running under.

        ENTER_M_FPS_BOOT is captured at the end of init, which is the value
        GL2Draw.init() goes on to read -- see the header note on why nothing
        re-applies it mid-session.
        """

        return renpy.game.preferences.gl_framerate != ENTER_M_FPS_BOOT

    def enter_m_vsync_mode():
        """The stored VSync mode, validated."""

        mode = getattr(persistent, "enter_m_vsync", "on")

        if mode not in ENTER_M_VSYNC_MODES:
            mode = "on"
            persistent.enter_m_vsync = mode

        return mode

    def enter_m_vsync_apply(mode):
        """
        Translate a VSync mode into the two knobs GL2Draw.init() reads.

        `gl_tearing` flips the swap interval negative, which is SDL's adaptive
        vsync: sync normally, tear instead of stalling a whole refresh when a
        frame lands late. The frame cap still applies.

        "off" has to go through RENPY_GL_VSYNC because Matsu'Py has no preference
        for interval 0 -- `vsync = int(os.environ.get("RENPY_GL_VSYNC",
        sync_frames))`, so the variable overrides the computed interval outright.
        That also means it overrides the *cap*: with vsync off Matsu'Py has no
        limiter of any kind and will render as fast as the GPU allows. The
        Settings screen says so.
        """

        import os

        renpy.game.preferences.gl_tearing = (mode == "adaptive")

        if mode == "off":
            os.environ["RENPY_GL_VSYNC"] = "0"
        else:
            os.environ.pop("RENPY_GL_VSYNC", None)

    def enter_m_vsync_needs_restart():
        """True when the stored VSync mode is not the one the renderer came up under."""

        return enter_m_vsync_mode() != ENTER_M_VSYNC_BOOT

    def enter_m_fps_sample():
        """
        Sample the real presented frame rate from config.frames.

        Driven by a repeating timer on the Settings screen (developer only).
        The timer forces a redraw every tick, which is what makes this measure
        the *ceiling* rather than Matsu'Py's idle floor -- an idle screen presents
        about 5fps by design (gl_powersave + redraw_period), and reading that as
        "the frame rate" would be meaningless.
        """

        import time

        now = time.time()
        frames = config.frames
        prev = getattr(enter_m_fps_sample, "prev", None)
        enter_m_fps_sample.prev = (now, frames)

        if prev is None:
            return

        dt = now - prev[0]
        if dt > 0:
            enter_m_fps_sample.value = (frames - prev[1]) / dt
            renpy.restart_interaction()

    def enter_m_fps_measured():
        """The last sampled frame rate, as display text."""

        # Not "--": config.replace_text (options.rpy) rewrites a double hyphen
        # into an em dash, so the placeholder would silently change shape.
        value = getattr(enter_m_fps_sample, "value", None)
        return u"…" if value is None else "%.0f" % value

    class EnterMFramerateValue(ui.BarValue):
        """
        Slider over `enter_m_fps_stops()`.

        force_step keeps the handle on real divisors instead of letting the
        player park it between two rates the hardware cannot produce.
        """

        def get_adjustment(self):
            stops = enter_m_fps_stops()

            return ui.adjustment(
                range=max(len(stops) - 1, 1),
                value=enter_m_fps_index(),
                changed=self.changed,
                step=1,
                force_step=True,
            )

        def changed(self, value):
            enter_m_fps_set_index(value)
            renpy.restart_interaction()

        def get_style(self):
            return "slider", "vslider"


# `default` only writes when the stored value is None, and gl_framerate lives in
# preferences (not persistent) where None is the legitimate "uncapped" setting --
# so there is no way to tell "never chosen" from "chosen uncapped" without a
# marker. Same shape as the Archive unlock migration in archive.rpy.
default persistent.enter_m_fps_cap_migrated = False

# init 50: after the `default` above has run (defaults execute at priority 0),
# and still comfortably before Interface.set_mode() reads the preference -- init
# code all runs before the renderer is created, so the cap applies on the very
# boot that migrates it.
init 50 python:

    if not persistent.enter_m_fps_cap_migrated:

        if enter_m_fps_raw_refresh_rate() > 0:
            enter_m_fps_set_index(enter_m_fps_nearest_index(ENTER_M_FPS_DEFAULT))
            persistent.enter_m_fps_cap_migrated = True

        else:
            # The display has not reported a refresh rate yet. Do NOT fall back
            # to a nominal 60Hz and pick a stop from it: on a nominal-60Hz stop
            # list the nearest stop to 60fps is the *uncapped* one, so the
            # fallback would quietly store "no cap at all" and -- because the
            # marker would be set -- keep it forever. That is the one way this
            # file can produce the bug it exists to fix.
            #
            # Store the literal target instead. The engine turns it into the
            # right divisor on any monitor (int(240/60)=4, int(60/60)=1), and
            # the marker stays clear so a later launch that *can* read the rate
            # snaps it to an exact stop.
            renpy.game.preferences.gl_framerate = ENTER_M_FPS_DEFAULT

    # VSync has to be translated into gl_tearing / RENPY_GL_VSYNC before the
    # renderer reads them, which is exactly what init 50 is: still init code,
    # so still ahead of Interface.set_mode().
    enter_m_vsync_apply(enter_m_vsync_mode())

    # The cap and VSync mode the renderer is about to come up with. Compared
    # against the live values to decide whether to show the restart notice.
    # Re-evaluated on every init, so a hot reload (config.autoreload)
    # re-baselines them -- that is wrong only in that the notice disappears, and
    # a reload has not re-run GL2Draw.init() either way.
    ENTER_M_FPS_BOOT = renpy.game.preferences.gl_framerate
    ENTER_M_VSYNC_BOOT = enter_m_vsync_mode()
