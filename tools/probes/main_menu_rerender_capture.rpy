# External-search-path probe for the August 31, 2026 main-menu art rerender.
#
# This file is never loaded by a normal build. Set RENPY_SEARCHPATH to this
# directory and RENPY_MAIN_MENU_RERENDER_CAPTURE_DIR to an existing output
# directory, then launch the real project. The hook keeps Ren'Py in its normal
# title lifecycle while capturing all three atmosphere levels and the two
# cold-open consumers of the bedroom plate.

init 999 python:
    import os
    if os.environ.get("RENPY_MAIN_MENU_RERENDER_CAPTURE_DIR"):
        renpy.session["_main_menu_screen"] = "main_menu_rerender_capture_boot"


screen main_menu_rerender_capture_boot():

    timer 0.05 action Call("main_menu_rerender_capture")


label main_menu_rerender_capture:

    python:
        import os
        _mm_rerender_capture_dir = os.environ[
            "RENPY_MAIN_MENU_RERENDER_CAPTURE_DIR"
        ]

        def _mm_rerender_capture(name):
            path = os.path.join(_mm_rerender_capture_dir, name)
            if not renpy.screenshot(path):
                raise Exception("Could not save main-menu capture: %s" % path)

    # Off proves the shipping PNG on its own. Light proves the held additive
    # quads still sit on their painted sources. Full adds drift, dust, grain,
    # and the animated light states.
    $ persistent.enter_m_atmos_quality = "off"
    $ renpy.show_screen("main_menu")
    $ renpy.restart_interaction()
    $ renpy.pause(1.00, hard=True)
    $ _mm_rerender_capture("2026-08-31-main-menu-bedroom-rerender-off-live-gl2.png")

    $ persistent.enter_m_atmos_quality = "light"
    $ renpy.hide_screen("main_menu")
    $ renpy.show_screen("main_menu")
    $ renpy.restart_interaction()
    $ renpy.pause(1.00, hard=True)
    $ _mm_rerender_capture("2026-08-31-main-menu-bedroom-rerender-light-live-gl2.png")

    $ persistent.enter_m_atmos_quality = "full"
    $ renpy.hide_screen("main_menu")
    $ renpy.show_screen("main_menu")
    $ renpy.restart_interaction()
    $ renpy.pause(1.20, hard=True)
    $ _mm_rerender_capture("2026-08-31-main-menu-bedroom-rerender-full-live-gl2.png")

    # Credits is the clearest title-context secondary consumer.
    $ renpy.hide_screen("main_menu")
    $ renpy.show_screen("credits_menu")
    $ renpy.pause(0.95, hard=True)
    $ _mm_rerender_capture("2026-08-31-main-menu-bedroom-rerender-credits-live-gl2.png")

    # Both cold-open plates consume the same PNG at a stronger push with their
    # own rails, grain, washes, and dark overlays.
    $ renpy.hide_screen("credits_menu")
    $ renpy.show_screen("enter_m_splash_intro")
    $ renpy.pause(1.72, hard=True)
    $ _mm_rerender_capture("2026-08-31-main-menu-bedroom-rerender-intro-live-gl2.png")

    $ renpy.hide_screen("enter_m_splash_intro")
    $ renpy.pause(0.10, hard=True)
    $ renpy.show_screen(
        "enter_m_splash_warning",
        "This game contains mature themes and disturbing content."
    )
    $ renpy.pause(1.20, hard=True)
    $ _mm_rerender_capture("2026-08-31-main-menu-bedroom-rerender-warning-live-gl2.png")

    $ renpy.quit()
