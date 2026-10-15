# Illustrated title sidebar: palette, entrance, selection marker and hover.
# Sidebar gestures settle after playing; main_menu_fx.rpy owns the room's
# continuing camera, grade and particles under the Atmosphere preference.

define MM_ROOM_INK = ROOM_MENU_INK
define MM_ROOM_TEAL = ROOM_MENU_TEAL
define MM_ROOM_RED = ROOM_MENU_CORAL
define MM_ROOM_SHADOW = "#061014c5"


transform mm_room_bg_arrive:
    alpha 0.0
    easeout 0.65 alpha 1.0


transform mm_room_panel_arrive:
    subpixel True
    alpha 0.0
    xoffset -22
    pause 0.08
    easeout_cubic 0.46 alpha 1.0 xoffset 0


transform mm_room_rule_arrive:
    subpixel True
    xanchor 0.0
    xzoom 0.0
    pause 0.34
    easeout_cubic 0.48 xzoom 1.0


transform mm_room_option_arrive(delay=0.0):
    subpixel True
    alpha 0.0
    xoffset -16
    pause delay
    parallel:
        easeout 0.28 alpha 1.0
    parallel:
        easeout_cubic 0.34 xoffset 0


# Button events reach the direct child, so the visible row is that child and
# the stationary button remains the complete mouse/focus target.
transform mm_room_option_focus:
    subpixel True
    xoffset 0
    on hover:
        easeout_cubic 0.16 xoffset 7
    on idle:
        easeout_cubic 0.16 xoffset 0


# Changing the selected row rebuilds this transform with a new key and replays
# the small arrival. It is event-driven, not a perpetual ambient animation.
transform mm_room_detail_swap(key=0):
    subpixel True
    alpha 0.0
    xoffset -8
    easeout 0.20 alpha 1.0 xoffset 0


screen main_menu():

    tag menu
    on "show" action [Function(illustrated_menu_predict), Function(enter_m_check_updates)]
    on "replace" action [Function(illustrated_menu_predict), Function(enter_m_check_updates)]
    on "hide" action Function(illustrated_menu_stop_predict)
    on "replaced" action Function(illustrated_menu_stop_predict)

    default mm_room_sel = 0

    python:
        # One table owns the visible row, its quiet category, the contextual
        # sentence below the list, and the action that opens it.
        mm_room_entries = [
            (_("New Game"),  _("BEGIN"),    _("Start at the first page."),                         [Function(illustrated_menu_stop_predict), Start()]),
            (_("Load Game"), _("RETURN"),   _("Pick up from a place you left behind."),            ShowMenu("data_bank")),
            (_("Arcade"),    _("PLAY"),     _("Spend a while somewhere with no story attached."), ShowMenu("arcade_hub")),
            (_("Archive"),   _("REMEMBER"), _("Look through everything the game kept."),          ShowMenu("archive")),
            (_("Credits"),   _("NAMES"),    _("See who made all of this."),                        ShowMenu("credits_menu")),
            (_("Donate"),    _("SUPPORT"),  _("Leave something in the tip jar."),                  OpenURL("https://ko-fi.com/l4w1i3t")),
            (_("Settings"),  _("ADJUST"),   _("Make the room feel right."),                        ShowMenu("preferences")),
            (_("Quit"),      _("LEAVE"),    _("Close the window for now."),                        Quit(confirm=False)),
        ]
        mm_room_cur = min(mm_room_sel, len(mm_room_entries) - 1)
        mm_room_label, mm_room_kind, mm_room_note, mm_room_action = mm_room_entries[mm_room_cur]

        # Atmosphere Off leaves the whole screen exactly as painted -- no
        # light layer, no loops, and no blinking cursor either.
        mm_room_lit = mmfx_lit()
        mm_room_alive = mmfx_alive()
        mm_room_ui_fx = (mmfx_level() != "off")

    # The room, its lights, its air and its grade. main_menu_fx.rpy.
    use mmfx_room_layer

    # The scene owns its own light. The sidebar is a single quiet value block,
    # not a full-screen filter, so the orrery keeps its colour beside it.
    add Solid(MM_ROOM_SHADOW) xysize (430, 720)
    add Solid("#eadbc02e") xpos 429 ypos 24 xysize (1, 672)
    add Solid("#70bbb34a") xpos 426 ypos 24 xysize (2, 672)

    # A node riding that seam. Its travel is derived from the seam Solid above,
    # so it stops exactly where the rail does.
    if mm_room_lit and mm_room_alive:
        add mmfx_quad(20, MMFX_SEAM_NODE_H) xpos 417 at mmfx_seam_scan

    fixed:
        at mm_room_panel_arrive

        # Under the logo plate, so it arrives with the panel rather than
        # popping in ahead of it.
        if mm_room_lit:
            add mmfx_quad(210, 210) xpos -27 ypos -33 at (mmfx_logo_halo if mm_room_alive else mmfx_logo_halo_still)

        add "assets/gui/logo.png":
            xpos 24
            ypos 18
            xysize (108, 108)

        hbox:
            xpos 150
            ypos 41
            spacing 11

        text "A QUIET PLACE BETWEEN STORIES":
            style "mm_room_header_note"
            xpos 151
            ypos 68

        add Solid("#d9cdb654") xpos 150 ypos 97 xysize (248, 1) at mm_room_rule_arrive
        add Solid(ROOM_MENU_OCHRE) xpos 150 ypos 96 xysize (52, 2) at mm_room_rule_arrive

    for mm_room_i, (mm_room_i_label, mm_room_i_kind, mm_room_i_note, mm_room_i_action) in enumerate(mm_room_entries):

        button:
            id ("main_menu_option_%d" % mm_room_i)
            style "mm_room_option_button"
            xysize (376, 42)
            xpos 28
            ypos (140 + mm_room_i * 48)
            background (ROOM_MENU_SELECTOR_SELECTED if mm_room_i == mm_room_cur else ROOM_MENU_SELECTOR_IDLE)
            hover_background ROOM_MENU_SELECTOR_HOVER
            action mm_room_i_action
            hovered SetScreenVariable("mm_room_sel", mm_room_i)
            default_focus (mm_room_i == 0)

            fixed:
                at [mm_room_option_arrive(0.16 + 0.035 * mm_room_i), mm_room_option_focus]
                xfill True
                yfill True

                frame:
                    style "mm_room_option_bar"
                    xysize (3, 34)
                    xpos 8
                    yalign 0.5

                text ("%02d" % (mm_room_i + 1)):
                    style "mm_room_option_number"
                    xpos 21
                    yalign 0.5

                text mm_room_i_label:
                    style "mm_room_option_label"
                    xpos 59
                    yalign 0.5

                text mm_room_i_kind:
                    style "mm_room_option_kind"
                    xanchor 1.0
                    xpos 355
                    yalign 0.5

    # Two ways of saying "this one", drawn OVER the plates. Neither is a
    # button, so neither can steal a click from the row underneath it.
    #
    # The marker is a light in the gutter, left of the plate entirely: at this
    # falloff it has fallen to half a percent by the time it reaches the slot
    # number, so it never tints anything the player is reading. It travels.
    # The glint arrives, crosses the row once, and is gone.
    #
    # The shader transform is FIRST in the at_list, i.e. innermost: the marker
    # that slides has to wrap the light, not the other way round. A mesh blits
    # its child at (0, 0) and never looks at its pixels, so an outer travelling
    # transform would leave the glow parked at the top of the list.
    if mm_room_lit:
        add mmfx_quad(84, 64) xpos -20 at [mmfx_marker_bloom, mmfx_row_marker(mm_room_cur, -11)]
        add mmfx_quad(MMFX_ROW_W, MMFX_ROW_H) xpos 28 at mmfx_row_glint(mm_room_cur)
    else:
        add Solid(MM_ROOM_RED) xysize (3, 26) xpos 18 at [mmfx_marker_in, mmfx_row_marker(mm_room_cur, 8)]

    frame:
        background ROOM_MENU_SELECTOR_IDLE
        at mm_room_detail_swap(mm_room_cur)
        xpos 29
        ypos 539
        xysize (374, 91)
        padding (17, 12, 17, 10)

        fixed:
            xfill True
            yfill True

            text mm_room_note:
                style "mm_room_note"
                xmaximum 338

            # A cursor sitting in front of the key line. It is the one thing on
            # the sidebar that moves without being asked to, and it can afford
            # to: instant alpha steps with real pauses between them, so it
            # costs two redraws a second and nothing in between. At Off it is
            # still drawn, just not blinking -- the tick is part of the layout,
            # and taking it away would leave the line indented around nothing.
            if mm_room_ui_fx:
                add Solid(MM_ROOM_RED) xysize (3, 11) ypos 63 at mmfx_caret_blink
            else:
                add Solid(MM_ROOM_RED) xysize (3, 11) ypos 63

            text ("%s / %02d" % (mm_room_kind, mm_room_cur + 1)):
                style "mm_room_note_key"
                xpos 10
                ypos 61

    if enter_m_updates.checker.available_version:
        textbutton _("New build available - view release"):
            id "main_menu_update_available"
            style "mm_room_update_button"
            xpos 29
            ypos 642
            xysize (374, 32)
            action OpenURL(enter_m_updates.RELEASES_URL)

    text "UP / DOWN   ENTER / CHOOSE":
        style "mm_room_footer"
        xpos 29
        ypos 683

    text ("v" + config.version):
        style "mm_room_footer"
        xanchor 1.0
        xpos 402
        ypos 683

    # The developer hub is optional by construction. Deleting its addon leaves
    # no dangling dependency in the shipping title screen.
    if config.developer and renpy.has_screen("dev_hub_mount"):
        use dev_hub_mount

    key "K_ESCAPE" action Quit(confirm=False)


style mm_room_identity is gui_text:
    font gui.interface_font
    size 11
    kerning 1.5
    color "#aebbb8"
    outlines [(1, "#05090d99", 0, 1)]

style mm_room_header_note is gui_text:
    font gui.interface_font
    size 9
    kerning 1.1
    color "#8da09e"
    outlines [(1, "#05090d99", 0, 1)]

style mm_room_option_button is gui_button:
    padding (0, 0, 0, 0)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style mm_room_option_bar is empty:
    background "#e7d7bb24"
    hover_background "#fff0d256"

style mm_room_option_number is gui_text:
    font gui.interface_font
    size 11
    color "#718b8d"
    hover_color "#dfaaa2"
    outlines [(1, "#05090d99", 0, 1)]

style mm_room_option_label is gui_text:
    font gui.default_font
    size 21
    color "#dddcd5"
    hover_color "#fff8ed"
    outlines [(1, "#05090db8", 0, 1)]

style mm_room_option_kind is gui_text:
    font gui.interface_font
    size 10
    kerning 1.0
    color "#829594"
    hover_color MM_ROOM_TEAL
    outlines [(1, "#05090d99", 0, 1)]

style mm_room_note is gui_text:
    font gui.default_font
    size 16
    color "#d4d5ce"
    line_spacing 3
    outlines [(1, "#05090db8", 0, 1)]

style mm_room_note_key is gui_text:
    font gui.interface_font
    size 10
    kerning 1.0
    color MM_ROOM_RED
    outlines [(1, "#05090d99", 0, 1)]

style mm_room_footer is gui_text:
    font gui.interface_font
    size 10
    color "#7f918f"
    outlines [(1, "#05090d99", 0, 1)]


style mm_room_update_button is mm_room_option_button:
    background ROOM_MENU_SELECTOR_IDLE
    hover_background ROOM_MENU_SELECTOR_HOVER
    padding (10, 0)

style mm_room_update_button_text is gui_button_text:
    font gui.interface_font
    size 15
    color MM_ROOM_TEAL
    hover_color ROOM_MENU_INK
    xalign 0.0
    yalign 0.5
    outlines [(1, "#05090d99", 0, 1)]
