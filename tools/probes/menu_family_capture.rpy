# External-search-path probe for title-context menu QA.
#
# This file is never loaded by normal builds. Set RENPY_SEARCHPATH to this
# directory and RENPY_MENU_CAPTURE_DIR to an existing output directory, then
# launch the game. The init hook asks Ren'Py's normal main-menu label to show a
# one-frame boot screen, which calls the probe without replacing common labels.
# That keeps ``main_menu`` true and exercises the real title lifecycle.

init 999 python:
    import os
    if os.environ.get("RENPY_MENU_CAPTURE_DIR"):
        if os.environ.get("RENPY_MENU_CAPTURE_MODE") == "confirm_hover":
            renpy.session["_main_menu_screen"] = "menu_family_capture_confirm_hover_boot"
        elif os.environ.get("RENPY_MENU_CAPTURE_MODE") == "pause":
            renpy.session["_main_menu_screen"] = "menu_family_capture_pause_boot"
        else:
            renpy.session["_main_menu_screen"] = "menu_family_capture_boot"


screen menu_family_capture_boot():

    timer 0.05 action Call("menu_family_capture")


screen menu_family_capture_pause_boot():

    timer 0.05 action Start("menu_family_capture_pause")


screen menu_family_capture_confirm_hover_boot():

    timer 0.05 action Start("menu_family_capture_confirm_hover")


screen menu_family_confirm_capture_finish():

    zorder 300
    timer 0.85 action [Function(_menu_capture, "2026-08-30-confirm-room-family-live-gl2.png"), Quit(confirm=False)]


screen menu_family_confirm_hover_capture_finish():

    zorder 300
    # Ren'Py intentionally unifies pointer hover and keyboard focus styling.
    # Capture No in its initial safe default-focus state, then move one ordered
    # step left to exercise Yes without relying on OS cursor motion reaching
    # the automated window.
    timer 0.25 action Function(_menu_capture, "2026-08-31-confirm-no-hover-live-gl2.png")
    timer 0.35 action Function(renpy.display.focus.focus_ordered, -1)
    timer 0.65 action Function(_menu_capture, "2026-08-31-confirm-yes-hover-live-gl2.png")
    timer 0.75 action Quit(confirm=False)


label menu_family_capture:

    python:
        import os
        _menu_capture_dir = os.environ["RENPY_MENU_CAPTURE_DIR"]

        def _menu_capture(name):
            path = os.path.join(_menu_capture_dir, name)
            if not renpy.screenshot(path):
                raise Exception("Could not save menu capture: %s" % path)

    $ renpy.show_screen("main_menu")
    $ renpy.pause(1.20, hard=True)
    $ _menu_capture("2026-08-30-main-menu-room-family-live-gl2.png")

    $ renpy.show_screen("preferences")
    $ renpy.pause(0.20, hard=True)
    # Graphics is deliberately the tallest section. It activates the
    # scrollbar and proves the 620px control lane remains outside its gutter.
    $ persistent.enter_m_pref_open = {"graphics"}
    $ renpy.restart_interaction()
    $ renpy.pause(0.80, hard=True)
    $ _menu_capture("2026-08-30-settings-room-family-live-gl2.png")

    $ renpy.show_screen("data_bank", start_mode="restore")
    $ renpy.pause(0.85, hard=True)
    $ _menu_capture("2026-08-30-records-room-family-live-gl2.png")

    $ renpy.show_screen("credits_menu")
    $ renpy.pause(0.95, hard=True)
    $ _menu_capture("2026-08-30-credits-room-family-live-gl2.png")

    $ renpy.quit()


label menu_family_capture_pause:

    python:
        import os
        _menu_capture_dir = os.environ["RENPY_MENU_CAPTURE_DIR"]

        def _menu_capture(name):
            path = os.path.join(_menu_capture_dir, name)
            if not renpy.screenshot(path):
                raise Exception("Could not save menu capture: %s" % path)

        def _history_preview_entry(who, what, color=None):
            entry = renpy.character.HistoryEntry()
            entry.who = who
            entry.what = what
            entry.who_args = { "color": color } if color else { }
            return entry

        _history_list = [
            _history_preview_entry(None, "Evening settles against the window, soft enough to make the room feel certain."),
            _history_preview_entry("Matsuda", "The build is clean. The result is... undecided.", "#70bbb3"),
            _history_preview_entry("MC", "That sounds intentional.", "#d6a354"),
        ]

    $ renpy.show_screen("history")
    $ renpy.pause(0.85, hard=True)
    $ _menu_capture("2026-08-30-history-room-family-live-gl2.png")

    $ renpy.show_screen("calendar_menu")
    $ renpy.pause(0.85, hard=True)
    $ _menu_capture("2026-08-30-calendar-room-family-live-gl2.png")

    $ renpy.show_screen("about")
    $ renpy.pause(0.85, hard=True)
    $ _menu_capture("2026-08-30-about-room-family-live-gl2.png")

    $ renpy.show_screen("calendar_menu")
    $ renpy.show_screen("confirm", "Return to the main menu? Unsaved progress will be lost.", NullAction(), NullAction())
    $ renpy.show_screen("menu_family_confirm_capture_finish")
    $ renpy.pause(hard=True)


label menu_family_capture_confirm_hover:

    python:
        import os
        _menu_capture_dir = os.environ["RENPY_MENU_CAPTURE_DIR"]

        def _menu_capture(name):
            path = os.path.join(_menu_capture_dir, name)
            if not renpy.screenshot(path):
                raise Exception("Could not save menu capture: %s" % path)

    $ renpy.show_screen("data_bank", start_mode="write")
    $ renpy.show_screen("confirm", "Are you sure you want to quit?", NullAction(), NullAction())
    $ renpy.show_screen("menu_family_confirm_hover_capture_finish")
    $ renpy.pause(hard=True)
