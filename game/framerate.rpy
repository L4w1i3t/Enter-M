# =============================================================================
# ENTER-M :: FRAME RATE
# -----------------------------------------------------------------------------
# THE GAME RUNS AT THE DISPLAY'S REFRESH RATE. There is no cap setting and no
# VSync setting; both were removed on Aug 27 2026 because they were costing more
# than they bought. What is left is one forced preference and a dev-only meter.
#
# WHY THE CAP HAD TO GO. Matsu'Py does not pace frames in software. It picks a
# GL swap interval and lets vsync do the limiting:
#
#     sync_frames = int(round(refresh_rate) / gl_framerate)      # min 1
#
# so "60fps" on a 240Hz panel is not a 60fps pacer -- it is **swap interval 4**,
# and every consequence of that is bad for a game with real-time modes:
#
#   * INPUT LATENCY QUADRUPLES. Input is sampled once per presented frame, so a
#     keypress waits up to 16.7ms to reach the screen instead of up to 4.2ms.
#     That is what made the boss fights feel mushy on the keyboard.
#   * A LATE FRAME COSTS FOUR REFRESHES, NOT ONE. Overrun a 16.7ms budget by a
#     hair and the swap blocks until the next 4-interval boundary: 33ms. The
#     same overrun at interval 1 costs 4ms. Small hitches became big ones.
#   * IT BEAT AGAINST THE SIMULATION. The danmaku stages deliberately tick and
#     draw at a fixed 60Hz (`KT_TICK`, and the same governor in tsubaki_soul and
#     the Archivist Invasions stages), scheduling their next frame with
#     `renpy.redraw(self, KT_TICK - acc)`. A 60Hz sim against a 60Hz present
#     that share no phase drop and double frames in a slow cycle -- motion that
#     is technically at rate and visibly not smooth. At interval 1 each tick
#     lands cleanly on every fourth refresh instead.
#
# The draw-rate governors are what make the high-refresh case affordable, and
# they are unaffected by any of this: the stages still simulate and draw 60
# times a second on a 240Hz panel, they just get presented promptly.
#
# WHAT THIS COSTS. Uncapped high-refresh rendering is more GPU work than a cap
# was, and a 240Hz source still does not resample cleanly into a 60fps capture
# encoder -- if streaming judder comes back, that is where it comes from, and
# the answer is a capture-side frame limiter or a driver-level per-exe vsync
# profile, not a setting in here. See [[enter-m-framerate-cap]] for the full
# measurement history, including why the engine can only ever offer divisors.
# =============================================================================

# init 50: still init code, so still ahead of Interface.set_mode() -- which is
# the only place the swap interval is ever applied (GL2Draw.init() runs exactly
# once, from set_mode(), at startup). Anything written here lands on this boot.
init 50 python:

    # None is the engine's "no divisor" -- swap interval 1, i.e. the panel's own
    # refresh rate. Forced on every launch rather than defaulted, because a
    # profile that played before this change still has a stored cap in
    # preferences and would otherwise keep it forever.
    renpy.game.preferences.gl_framerate = None

    # Adaptive sync tore instead of stalling when a frame landed late. With no
    # cap there is nothing to stall against, and tearing is just tearing.
    renpy.game.preferences.gl_tearing = False

    # Both settings kept persistent state. Clear it so a stale "off" cannot
    # come back to life if either ever returns.
    persistent.enter_m_vsync = None
    persistent.enter_m_fps_cap_migrated = None


init python:

    def enter_m_fps_sample():
        """
        Sample the real presented frame rate from config.frames.

        Driven by a repeating timer on the Dev Hub and the developer-only line
        in Settings. The timer forces a redraw every tick, which is what makes
        this measure the *ceiling* rather than Matsu'Py's idle floor -- an idle
        screen presents about 5fps by design (gl_powersave + redraw_period),
        and reading that as "the frame rate" would be meaningless.
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

    def enter_m_refresh_rate_label():
        """What the display reported, for the developer readout."""

        try:
            rate = renpy.display.get_info().refresh_rate
        except Exception:
            rate = 0

        # get_refresh_rate() rounds to a multiple of 5 (239 -> 240) but the
        # engine divides the RAW value, so the raw one is what to show.
        return u"…" if not rate else "%.0f Hz" % rate
