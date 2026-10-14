# Display preferences are applied before the renderer starts.
# No engine frame-rate divisor; Low-Resource Mode controls idle redraws.

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


# The player choice is persistent; gl_powersave is derived from it each launch.
# False requests continuous presentation; True permits the renderer to idle.
default persistent.enter_m_low_resource = False


init 50 python:

    # Ahead of set_mode, alongside the other forced display preferences. The
    # flag is also read live by can_block() on every pass of the interact loop,
    # so the in-game toggle applies immediately with no display reset.
    renpy.game.preferences.gl_powersave = bool(persistent.enter_m_low_resource)


init python:

    def enter_m_low_resource():
        """True when the engine is allowed to idle instead of presenting."""

        return bool(persistent.enter_m_low_resource)

    def enter_m_set_low_resource(enabled):
        """Hand the idle cadence back to the engine, or take it away."""

        persistent.enter_m_low_resource = bool(enabled)
        renpy.game.preferences.gl_powersave = bool(enabled)
        renpy.restart_interaction()


init python:

    def enter_m_fps_sample():
        """Sample presented frames over monotonic elapsed time.

        The developer-screen timer requests redraws, so this samples an active
        screen rather than measuring an untouched idle screen.
        """

        import time

        sample_time = time.perf_counter()
        frame_count = config.frames
        previous_sample = getattr(enter_m_fps_sample, "prev", None)
        enter_m_fps_sample.prev = (sample_time, frame_count)

        if previous_sample is None:
            return

        elapsed_seconds = sample_time - previous_sample[0]
        if elapsed_seconds > 0:
            enter_m_fps_sample.value = (frame_count - previous_sample[1]) / elapsed_seconds
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
