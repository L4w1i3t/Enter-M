# Shared visual vocabulary for the domestic menu family.
#
# This file is intentionally isolated from Arcade and Archive. Those screens
# have authored interface identities of their own; only Main Menu, Settings,
# Records, and Credits opt into these constants and assets.

define -100 ROOM_MENU_INK = "#f4ecde"
define -100 ROOM_MENU_PAPER = "#e8dbc5"
define -100 ROOM_MENU_MUTED = "#a9b9b5"
define -100 ROOM_MENU_TEAL = "#70bbb3"
define -100 ROOM_MENU_CORAL = "#d87b6d"
define -100 ROOM_MENU_OCHRE = "#d6a354"
define -100 ROOM_MENU_LAVENDER = "#a99bc4"
define -100 ROOM_MENU_PANEL = "#071116dc"

# The palette is consumed by top-level ``define`` tables in Data Bank and
# Credits. An explicit early init priority keeps that dependency correct even
# if this file is renamed; filesystem order is not an initialization contract.
define -100 ROOM_MENU_SELECTOR_IDLE = Frame("assets/gui/menu/room_theme/selector_idle.png", 18, 18, 20, 18, tile=False)
define -100 ROOM_MENU_SELECTOR_HOVER = Frame("assets/gui/menu/room_theme/selector_hover.png", 18, 18, 20, 18, tile=False)
define -100 ROOM_MENU_SELECTOR_SELECTED = Frame("assets/gui/menu/room_theme/selector_selected.png", 18, 18, 20, 18, tile=False)
define -100 ROOM_MENU_SELECTOR_DANGER = Frame("assets/gui/menu/room_theme/selector_danger.png", 18, 18, 20, 18, tile=False)
define -100 ROOM_MENU_SELECTOR_YES_HOVER = Frame("assets/gui/menu/room_theme/selector_yes_hover.png", 18, 18, 20, 18, tile=False)
define -100 ROOM_MENU_SELECTOR_NO_HOVER = Frame("assets/gui/menu/room_theme/selector_no_hover.png", 18, 18, 20, 18, tile=False)


transform room_menu_bg_arrive:
    alpha 0.0
    easeout 0.55 alpha 1.0


transform room_menu_panel_arrive:
    subpixel True
    alpha 0.0
    xoffset -18
    pause 0.06
    easeout_cubic 0.42 alpha 1.0 xoffset 0


transform room_menu_rule_arrive:
    subpixel True
    xanchor 0.0
    xzoom 0.0
    pause 0.26
    easeout_cubic 0.42 xzoom 1.0


style room_menu_heading is gui_text:
    font gui.default_font
    size 30
    color ROOM_MENU_INK
    outlines [(2, "#05090db8", 0, 1)]

style room_menu_kicker is gui_text:
    font gui.interface_font
    size 10
    kerning 1.4
    color ROOM_MENU_TEAL
    outlines [(1, "#05090d99", 0, 1)]

style room_menu_body is gui_text:
    font gui.default_font
    size 16
    color ROOM_MENU_PAPER
    outlines [(1, "#05090daa", 0, 1)]

style room_menu_meta is gui_text:
    font gui.interface_font
    size 10
    kerning 0.8
    color ROOM_MENU_MUTED
    outlines [(1, "#05090d99", 0, 1)]

style room_menu_button is gui_button:
    background ROOM_MENU_SELECTOR_IDLE
    hover_background ROOM_MENU_SELECTOR_HOVER
    selected_background ROOM_MENU_SELECTOR_SELECTED
    selected_hover_background ROOM_MENU_SELECTOR_SELECTED
    insensitive_background ROOM_MENU_SELECTOR_IDLE
    padding (18, 9, 18, 9)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style room_menu_button_text is gui_button_text:
    font gui.default_font
    size 17
    color ROOM_MENU_PAPER
    hover_color "#fff8ea"
    selected_color "#fff8ea"
    insensitive_color "#71807e"
    outlines [(1, "#05090db8", 0, 1)]


# -----------------------------------------------------------------------------
# Shared domestic submenu shell
# -----------------------------------------------------------------------------
#
# Settings, Records, History, Calendar, About, and Credits opt into this family.
# Arcade, Archive, and the authored combat overlays retain their own identities.

screen room_menu_navigation(nav_main, current_screen):

    vbox:
        style "room_menu_navigation"

        if nav_main:

            textbutton _("New Game"):
                style "room_menu_nav_button"
                action Start()

            textbutton _("Load Game"):
                style "room_menu_nav_button"
                action [SetVariable("_game_menu_screen", "data_bank"), ShowMenu("data_bank", start_mode="restore")]
                sensitive (renpy.get_screen("data_bank") == None)
                selected (current_screen == "data_bank")

            textbutton _("Archive"):
                style "room_menu_nav_button"
                action [SetVariable("_game_menu_screen", "archive"), ShowMenu("archive")]

            textbutton _("Credits"):
                style "room_menu_nav_button"
                action [SetVariable("_game_menu_screen", "credits_menu"), ShowMenu("credits_menu")]
                selected (current_screen == "credits_menu")

        else:

            textbutton _("History"):
                style "room_menu_nav_button"
                action [SetVariable("_game_menu_screen", "history"), ShowMenu("history"), SensitiveIf(renpy.get_screen("history") == None)]
                selected (current_screen == "history")

            textbutton _("Calendar"):
                style "room_menu_nav_button"
                action [SetVariable("_game_menu_screen", "calendar_menu"), ShowMenu("calendar_menu")]
                sensitive (renpy.get_screen("calendar_menu") == None)
                selected (current_screen == "calendar_menu")

            textbutton _("Records"):
                style "room_menu_nav_button"
                action [SetVariable("_game_menu_screen", "data_bank"), ShowMenu("data_bank", start_mode="write")]
                sensitive (not msbf_save_load_locked() and renpy.get_screen("data_bank") == None)
                selected (current_screen == "data_bank")

            textbutton _("Main Menu"):
                style "room_menu_nav_button"
                action MainMenu()

        textbutton _("Settings"):
            style "room_menu_nav_button"
            action [SetVariable("_game_menu_screen", "preferences"), ShowMenu("preferences"), SensitiveIf(renpy.get_screen("preferences") == None)]
            selected (current_screen == "preferences")

        if renpy.variant("pc"):

            textbutton _("Quit"):
                style "room_menu_nav_button"
                action Quit(confirm=not nav_main)

        null height 3

        textbutton _("Return"):
            style "room_menu_return_button"
            action Return()


screen room_menu_shell(title, current_screen):

    python:
        room_shell_kickers = {
            "preferences": _("A QUIET PLACE TO ADJUST THINGS"),
            "data_bank": _("A PLACE TO LEAVE AND RETURN"),
            "save": _("A PLACE TO LEAVE AND RETURN"),
            "load": _("A PLACE TO LEAVE AND RETURN"),
            "history": _("WHAT THE STORY REMEMBERS"),
            "calendar_menu": _("DAYS KEPT IN THEIR ORDER"),
            "about": _("NOTES FROM BEHIND THE CURTAIN"),
        }
        room_shell_kicker = room_shell_kickers.get(current_screen, _("A QUIET PLACE BETWEEN PAGES"))
        room_shell_identity = current_screen.replace("_", " ").upper()

    if main_menu:

        add gui.main_menu_background at room_menu_bg_arrive

    else:

        key "mouseup_3" action Return()
        add gui.game_menu_background at room_menu_bg_arrive

    # A cool shadow keeps the UI legible while the low-opacity warm wash lets
    # the backdrop's own colour survive behind it.
    add Solid("#0310158f")
    add Solid("#d6a3540d")

    frame:
        style "room_menu_outer_frame"
        at room_menu_panel_arrive

        hbox:
            spacing 16

            frame:
                style "room_menu_navigation_frame"

                fixed:
                    xfill True
                    yfill True

                    add "assets/gui/logo.png":
                        xpos 0
                        ypos 0
                        xysize (104, 104)

                    add Solid(ROOM_MENU_TEAL) xysize (52, 2) xpos 0 ypos 138
                    add Solid(ROOM_MENU_CORAL) xysize (34, 2) xpos 56 ypos 138
                    add Solid(ROOM_MENU_OCHRE) xysize (24, 2) xpos 94 ypos 138
                    add Solid("#e8dbc52d") xysize (224, 1) xpos 0 ypos 146

                    use room_menu_navigation(main_menu, current_screen)

                    text ("LOCAL / " + room_shell_identity):
                        style "room_menu_nav_footer"
                        xpos 2
                        ypos 576

            frame:
                style "room_menu_content_frame"

                transclude

    text room_shell_kicker:
        style "room_menu_shell_kicker"

    text title:
        style "room_menu_shell_title"

    add Solid("#e8dbc536") xysize (868, 1) xpos 348 ypos 119
    add Solid(ROOM_MENU_TEAL) xysize (92, 2) xpos 348 ypos 118 at room_menu_rule_arrive
    add Solid(ROOM_MENU_CORAL) xysize (48, 2) xpos 444 ypos 118 at room_menu_rule_arrive

    frame:
        style "room_menu_context_badge"

        hbox:
            spacing 7
            add Solid(ROOM_MENU_OCHRE) xysize (6, 6) yalign 0.5
            text ("TITLE / EVENING" if main_menu else "STORY / PAUSED"):
                style "room_menu_context_badge_text"

    text ("v" + config.version):
        style "room_menu_version"

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style room_menu_outer_frame is empty:
    xpos 44
    ypos 42
    xsize 1192
    ysize 636
    padding (0, 0, 0, 0)
    background None

style room_menu_navigation_frame is empty:
    xsize 272
    ysize 636
    padding (24, 22, 24, 20)
    background "#071116ee"

style room_menu_content_frame is empty:
    xsize 904
    ysize 636
    padding (34, 84, 34, 32)
    background "#10191ddb"

style room_menu_navigation is vbox:
    xpos 0
    ypos 158
    xsize 224
    spacing 7

style room_menu_nav_button is room_menu_button:
    xsize 224
    ysize 38
    padding (16, 6, 16, 7)
    selected_insensitive_background ROOM_MENU_SELECTOR_SELECTED

style room_menu_nav_button_text is room_menu_button_text:
    font gui.interface_font
    size 15
    xalign 0.0
    text_align 0.0
    selected_color "#fff8ea"
    selected_insensitive_color "#fff8ea"

style room_menu_return_button is room_menu_nav_button:
    background ROOM_MENU_SELECTOR_SELECTED
    hover_background ROOM_MENU_SELECTOR_HOVER

style room_menu_return_button_text is room_menu_nav_button_text:
    color ROOM_MENU_INK

style room_menu_nav_footer is gui_text:
    font gui.interface_font
    size 9
    kerning 0.8
    color "#778b87"
    outlines [(1, "#05090d99", 0, 1)]

style room_menu_shell_kicker is gui_text:
    xpos 350
    ypos 55
    font gui.interface_font
    size 10
    kerning 1.2
    color ROOM_MENU_OCHRE
    outlines [(1, "#05090d99", 0, 1)]

style room_menu_shell_title is gui_text:
    xpos 348
    ypos 70
    font gui.default_font
    size 34
    color ROOM_MENU_INK
    outlines [(2, "#05090db8", 0, 1)]

style room_menu_context_badge is empty:
    xpos 1214
    xanchor 1.0
    ypos 65
    padding (12, 7, 12, 7)
    background "#2a2520d9"

style room_menu_context_badge_text is gui_text:
    font gui.interface_font
    size 10
    kerning 0.7
    color ROOM_MENU_PAPER
    outlines [(1, "#05090d99", 0, 1)]

style room_menu_version is room_menu_meta:
    xpos 1214
    xanchor 1.0
    ypos 652

style room_game_menu_sv_vscrollbar:
    xsize 8
    base_bar Frame(Solid("#172126b8"), 0, 0, 0, 0)
    thumb Frame(Solid(ROOM_MENU_TEAL + "d8"), 2, 2, 2, 2)
    unscrollable "hide"

style room_game_menu_sv_side:
    spacing 12


# -----------------------------------------------------------------------------
# Settings-only controls
# -----------------------------------------------------------------------------

style room_pref_panel is empty:
    xsize 620
    background "#111a1dd6"

style room_pref_section_body is empty:
    xsize 620
    padding (16, 12, 16, 14)

style room_pref_section_button is button:
    xsize 620
    ysize 42
    padding (16, 7, 16, 7)
    background ROOM_MENU_SELECTOR_IDLE
    hover_background ROOM_MENU_SELECTOR_HOVER
    selected_background ROOM_MENU_SELECTOR_SELECTED
    selected_hover_background ROOM_MENU_SELECTOR_HOVER
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style room_pref_section_title is gui_text:
    font gui.default_font
    size 20
    color ROOM_MENU_INK
    outlines [(1, "#05090db8", 0, 1)]

style room_pref_index_label is gui_text:
    font gui.interface_font
    size 13
    kerning 0.8
    color ROOM_MENU_MUTED
    outlines [(1, "#05090d99", 0, 1)]

style room_pref_row_label is gui_text:
    font gui.interface_font
    size 16
    color ROOM_MENU_PAPER
    outlines [(1, "#05090daa", 0, 1)]
    top_margin 2

style room_pref_note_label is room_pref_row_label:
    size 13
    color ROOM_MENU_MUTED
    top_margin 1

style room_pref_button_row is hbox:
    spacing 10

style room_pref_audio_row is hbox:
    spacing 10
    yalign 0.5

style room_pref_radio_button is gui_button:
    xsize 289
    ysize 34
    padding (12, 4, 12, 5)
    background ROOM_MENU_SELECTOR_IDLE
    hover_background ROOM_MENU_SELECTOR_HOVER
    selected_background ROOM_MENU_SELECTOR_SELECTED
    selected_hover_background ROOM_MENU_SELECTOR_HOVER
    insensitive_background ROOM_MENU_SELECTOR_IDLE
    selected_insensitive_background ROOM_MENU_SELECTOR_SELECTED
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style room_pref_radio_button_text is gui_button_text:
    font gui.interface_font
    size 16
    color ROOM_MENU_MUTED
    hover_color "#fff8ea"
    selected_color ROOM_MENU_INK
    selected_hover_color "#fff8ea"
    insensitive_color "#71807e"
    selected_insensitive_color ROOM_MENU_INK
    outlines [(1, "#05090daa", 0, 1)]

style room_pref_check_button is room_pref_radio_button
style room_pref_check_button_text is room_pref_radio_button_text

style room_pref_small_button is room_pref_radio_button:
    xsize 189

style room_pref_small_button_text is room_pref_radio_button_text

style room_pref_action_button is room_pref_radio_button:
    xsize 289

style room_pref_action_button_text is room_pref_radio_button_text

style room_pref_index_button is room_pref_radio_button:
    xsize 116
    ysize 28
    padding (8, 3, 8, 4)

style room_pref_index_button_text is room_pref_radio_button_text:
    size 14

style room_pref_full_slider is slider:
    xsize 588
    ysize 10
    base_bar Solid("#33403f")
    thumb Solid(ROOM_MENU_CORAL)

style room_pref_full_audio_slider is room_pref_full_slider:
    xsize 514

style room_pref_test_button is room_pref_radio_button:
    xsize 64
    ysize 34
    padding (8, 4, 8, 5)

style room_pref_test_button_text is room_pref_radio_button_text:
    size 14

style room_pref_preset_row is hbox:
    spacing 8
    top_margin 2

style room_pref_preset_button is room_pref_radio_button:
    xsize 141
    padding (6, 4, 6, 5)

style room_pref_preset_button_text is room_pref_radio_button_text:
    size 14

style room_pref_reset_button is room_pref_radio_button:
    xsize 620
    background ROOM_MENU_SELECTOR_DANGER
    hover_background ROOM_MENU_SELECTOR_HOVER
    selected_background ROOM_MENU_SELECTOR_DANGER

style room_pref_reset_button_text is room_pref_radio_button_text:
    size 16
    color ROOM_MENU_PAPER

style room_pref_sv_vscrollbar:
    xsize 8
    base_bar Frame(Solid("#172126b8"), 0, 0, 0, 0)
    thumb Frame(Solid(ROOM_MENU_TEAL + "d8"), 2, 2, 2, 2)
    unscrollable "hide"

style room_pref_sv_side:
    spacing 12
