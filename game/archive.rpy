# Custom screens/labels for archive

# Initialize archive unlock variables
default persistent.archive_unlocked_roster = False
default persistent.archive_unlocked_cgs = False
default persistent.archive_unlocked_music = False
default persistent.archive_unlocked_poems = False
default persistent.archive_unlocked_character_stories = False
default persistent.archive_unlocked_lost_records = False

# Data-driven archive item definitions
init python:
    # Each entry: (label, unlock_persistent_key, unlocked_action, icon)
    # unlock_persistent_key of None means always locked (placeholder)
    archive_items = [
        ("Roster",       "archive_unlocked_roster",            Show("roster_view_screen"), "mod_assets/dump/icon_placeholder.png"),
        ("CG Gallery",   "archive_unlocked_cgs",               Show("cg_gallery"),         "mod_assets/dump/icon_placeholder.png"),
        ("Music Room",   "archive_unlocked_music",             Show("music_room"),         "mod_assets/dump/icon_placeholder.png"),
        ("Side Stories", "archive_unlocked_character_stories", Show("character_stories"),  "mod_assets/dump/icon_placeholder.png"),
        ("Lost Records", "archive_unlocked_lost_records",      Show("lost_records"),       "mod_assets/dump/icon_placeholder.png"),
        ("???",        None,                        None,                         None),
    ]

    def archive_is_unlocked(key):
        if key:
            return getattr(persistent, key, False)
        return False

    def archive_return_action():
        """Shared action for leaving the archive back to the main menu."""
        renpy.music.play("mod_assets/bgm/map003.ogg")
        renpy.hide_screen("archive")
        renpy.return_statement()

label enter_m_archive_replay_op:
    $ renpy.hide_screen("archive")
    call enter_m_sick_ass_anime_op
    $ enter_m_op_cleanup_screens()
    scene black
    $ renpy.music.play("mod_assets/bgm/roster_place.ogg")
    $ renpy.show_screen("archive")
    return

# Combined entrance + hover for archive cards
transform archive_card_anim(delay=0.0):
    alpha 0.0
    yoffset 30
    subpixel True
    pause delay
    easein_back 0.45 alpha 1.0 yoffset 0
    on idle:
        ease 0.15 yoffset 0
    on hover:
        ease 0.15 yoffset -5

# Entrance for the main frame
transform archive_frame_enter:
    on show:
        alpha 0.0
        yoffset -40
        easein_back 0.45 alpha 1.0 yoffset 0
    on hide:
        alpha 1.0
        easeout_quad 0.25 alpha 0.0 yoffset -25

screen archive_backdrop():
    add "bg ether"
    add Solid("#00000050")
    add Solid("#75f7ff1f") xysize (1280, 2) at menu_scanline_slow

screen archive_header(title, return_action, return_text=_("Return")):
    hbox:
        xfill True
        ysize 64

        frame:
            style "archive_header_title_frame"
            at transform:
                on show:
                    alpha 0.0
                    xoffset -18
                    easeout 0.35 alpha 1.0 xoffset 0

            text title style "archive_title"

        add Solid("#56d7ff") xysize (3, 46) yalign 0.5 xoffset 16

        null width 1 xfill True

        textbutton return_text:
            style "archive_return_button"
            yalign 0.5
            action return_action
            at transform:
                on show:
                    alpha 0.0
                    pause 0.18
                    ease 0.25 alpha 1.0

screen archive():
    tag menu

    on "show" action Play("music", "mod_assets/bgm/roster_place.ogg")
    on "replace" action Play("music", "mod_assets/bgm/roster_place.ogg")

    use archive_backdrop

    key "game_menu" action [Play("music", "mod_assets/bgm/map003.ogg"), Return()]
    key "K_ESCAPE" action [Play("music", "mod_assets/bgm/map003.ogg"), Return()]

    frame:
        style "archive_frame"
        at archive_frame_enter

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 14

            use archive_header("ARCHIVE", [Play("music", "mod_assets/bgm/map003.ogg"), Return()])

            add Solid("#56d7ff66"):
                xsize 1100
                ysize 2
                xalign 0.5

            null height 10

            grid 3 2:
                spacing 25
                xalign 0.5

                for i, item in enumerate(archive_items):
                    $ a_label, a_key, a_action, a_icon = item
                    $ a_unlocked = archive_is_unlocked(a_key)
                    $ a_delay = i * 0.07

                    button:
                        style "archive_item_button"
                        at archive_card_anim(a_delay)

                        if a_unlocked and a_action:
                            action a_action
                        else:
                            action Show("dialog", message="This feature hasn't been unlocked yet.", ok_action=Hide("dialog"))

                        vbox:
                            xalign 0.5
                            yalign 0.5
                            spacing 10

                            if a_unlocked and a_icon:
                                add Transform(a_icon, size=(94, 132)) xalign 0.5
                                text a_label style "archive_item_text"
                                text "AVAILABLE" style "archive_item_status"
                            else:
                                add Transform("mod_assets/dump/unavailable_icon_placeholder.png", size=(94, 132)) xalign 0.5
                                text "???" style "archive_locked_text"
                                text "LOCKED" style "archive_locked_status"

    textbutton _("Replay OP"):
        style "archive_corner_button"
        xalign 0.985
        yalign 0.025
        action Function(renpy.call_in_new_context, "enter_m_archive_replay_op")
        at transform:
            on show:
                alpha 0.0
                xoffset 14
                pause 0.22
                easeout 0.22 alpha 1.0 xoffset 0

style archive_frame:
    xalign 0.5
    yalign 0.5
    xsize 1160
    ysize 650
    background Solid("#050811e8")
    padding (30, 22)

style archive_shell_frame is archive_frame:
    xsize 1200
    ysize 690
    padding (24, 16)

style archive_header_title_frame:
    background Solid("#07111dcc")
    padding (24, 12)
    yalign 0.5

style archive_title:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 40
    color "#f4fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (2, "#ff315bcc", 1, 1)]

style archive_item_button:
    xysize (250, 230)
    background Solid("#07111dcc")
    hover_background Solid("#12314af2")
    selected_background Solid("#12314af2")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (18, 12)

style archive_item_text:
    font gui.interface_font
    color "#dff8ff"
    size 22
    xalign 0.5
    text_align 0.5
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style archive_item_status:
    font gui.interface_font
    color "#56d7ff"
    size 12
    xalign 0.5
    text_align 0.5
    outlines [(1, "#02040b", 0, 0)]

style archive_locked_text:
    font gui.interface_font
    color "#687787"
    size 26
    xalign 0.5
    text_align 0.5
    bold True
    outlines [(2, "#02040b", 0, 0)]

style archive_locked_status is archive_item_status:
    color "#4f5b67"

style archive_return_button:
    xsize 126
    ysize 42
    background Solid("#07111dcc")
    hover_background Solid("#12314af2")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (15, 8)

style archive_return_button_text:
    font gui.interface_font
    color "#dff8ff"
    hover_color "#ffffff"
    size 22
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style archive_corner_button is archive_return_button:
    xsize 150
    ysize 38
    background Solid("#07111dee")
    hover_background Solid("#12314af2")

style archive_corner_button_text is archive_return_button_text:
    size 18

style archive_panel:
    background Solid("#07101add")
    padding (18, 18)

style archive_sidebar_panel is archive_panel:
    background Solid("#050811e8")

style archive_panel_label:
    font gui.interface_font
    color "#f4fbff"
    size 20
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style archive_panel_small:
    font gui.interface_font
    color "#9fc9d6"
    size 14
    outlines [(1, "#02040b", 0, 0)]

style archive_sv_vscrollbar:
    xsize 6
    base_bar Frame(Solid("#102338"), 0, 0, 0, 0)
    thumb Frame(Solid("#56d7ff"), 2, 2, 2, 2)
    unscrollable "hide"

# Placeholder screens for features
# CG Gallery screen is defined in addons/CG View/cg_gallery.rpy

screen poem_archive():
    tag menu
    frame:
        xalign 0.5
        yalign 0.5
        padding (50, 50)

        vbox:
            text "Poem Archive - Coming Soon" size 32
            null height 20
            textbutton "Return" action Return()
