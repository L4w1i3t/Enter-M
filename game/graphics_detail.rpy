# =============================================================================
# EFFECTS DETAIL -- one graphics preference for the game's heavy modes
# =============================================================================
# Settings > Graphics > Effects Detail: "full" (the default) or "low".
#
# WHO IT IS FOR
#   Integrated graphics and handhelds. Measured Oct 9 2026 with the Dev Hub's
#   spec emulator, what Low buys is mostly CPU time in the busiest moments --
#   every decorative particle, afterimage and glow is Python work each frame
#   (Kotonoha's flood with bombs: 13.1 -> 8.5ms a frame) -- plus a little GPU
#   time. The big GPU costs that pass found were waste, not decoration, and
#   were fixed for everyone without changing the picture. Numbers:
#   docs/history/2026-10-09-stress-test-and-low-detail.md.
#
# THE RULE: LOW TAKES THE GARNISH, NEVER THE READ.
#   Bullets, hazards, telegraphs, hit flashes, health and every piece of
#   interface stay exactly as they are. What goes is what the eye was never
#   asked to act on: ambient particles, trailing afterimages, second-order
#   glows, decorative backdrop motion. A mode honours the switch at its own
#   call sites (each one is a judgment about what counts as the picture), and
#   a 60Hz displayable reads it ONCE per frame, not per draw.
#
#   Honoured by: Matsuda's fight and Id Mode, Kotonoha, Tsubaki and the
#   Archivist Invasions. NOT by Asarhythm -- measured, it already holds 60fps
#   on the emulated 2018 laptop at 1080p, and its effects are choreography
#   with their own Photosensitive switch -- and not by the story, whose look
#   has its own Atmosphere setting. Scope the Settings copy to this list.
# =============================================================================

default persistent.enter_m_fx_detail = None

init -100 python:

    ENTER_M_FX_DETAIL_LEVELS = ("full", "low")

    def enter_m_fx_detail():
        """The validated detail stop, "full" or "low"."""
        level = getattr(persistent, "enter_m_fx_detail", None)
        return level if level in ENTER_M_FX_DETAIL_LEVELS else "full"

    def enter_m_low_detail():
        """True when the heavy modes should drop their decorative layers."""
        return getattr(persistent, "enter_m_fx_detail", None) == "low"

    def enter_m_set_fx_detail(level):
        if level not in ENTER_M_FX_DETAIL_LEVELS:
            level = "full"
        persistent.enter_m_fx_detail = level
        renpy.restart_interaction()


init 1 python:

    # One-time seed for a profile that has never chosen. The old "Fast" stop of
    # the fight-effects dial ALSO dropped decoration; that half of it moved
    # here, so a player who picked Fast keeps getting it. Stored outright
    # (not derived on every read) so changing the resolution dial later can
    # never flip this switch behind the player's back.
    if getattr(persistent, "enter_m_fx_detail", None) not in ENTER_M_FX_DETAIL_LEVELS:
        persistent.enter_m_fx_detail = (
            "low" if getattr(persistent, "msbf_gfx", None) == "performance" else "full")
