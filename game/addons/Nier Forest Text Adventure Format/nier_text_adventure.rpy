# =============================================================================
# nier_text_adventure.rpy  --  NIER REPLICANT-STYLE PROSE TEXT ADVENTURE
# =============================================================================
#
# Prose-style text adventure on a black background, built on NVL mode.
# Text accumulates on screen. The player clicks to advance and picks choices.
#
# USAGE
#
#   call nier_enter                  -- fade to black, activate mode
#   nier "Prose text."               -- text (accumulates)
#   call nier_section("Title")       -- section heading (clears + title card)
#   call nier_clear                  -- clear accumulated text
#   menu (screen="nier_nvl_choice"): -- choices
#       "Option A":
#           ...
#       "Option B":
#           ...
#   call nier_exit                   -- fade out, deactivate
#
# WHO USES THIS
#   game/addons/Character Stories/cs_kotonoha_01.rpy ("The Girl with Every Face")
#   game/addons/Character Stories/cs_kotonoha_02.rpy ("The Void Hunter")
#   Both run their whole story inside this mode and use `menu (screen=
#   "nier_nvl_choice")` for the attention-check questions.
#
# WHAT THIS FILE EXPOSES
#   Character : `nier`                  -- the NVL narrator (routes to nier_nvl).
#   Screens   : nier_nvl (the prose),   nier_nvl_choice (menu choices),
#               nier_section_display (a title card).
#   Labels    : nier_enter / nier_exit / nier_section(title) / nier_clear.
#   State     : nier_ta_active (is the mode on?), nier_ta_prev_quick_menu (saved
#               quick_menu flag, restored on exit).
#
# GOTCHA (FROM THE CHEATSHEET)
#   Always `call nier_exit` before returning to normal ADV scenes. The shared
#   window-auto policy resumes ordinary ADV ownership on its own.
# =============================================================================


# Flag so other scripts can check whether the mode is active (+ saved quick_menu).
default nier_ta_active = False
default nier_ta_prev_quick_menu = True


# =============================================================================
#  CHARACTERS
# =============================================================================

# Unattributed narrator (NVL-based, routed to our custom screen).
define nier = Character(
    None,
    kind=nvl,
    screen="nier_nvl",
    what_style="nier_nvl_dialogue",
    window_style="nier_nvl_entry",
)


# =============================================================================
#  NVL SCREEN -- Nier variant
# =============================================================================
# Prose-style accumulating text, top-left, on black.

# The NVL display the `nier` character renders into: a scrolling, bottom-anchored
# vpgrid of accumulated prose `window`s on black. If a menu is shown with this
# screen, its choices render inline at the bottom (the `items` block).
screen nier_nvl(dialogue, items=None):

    add "#000000"

    # Belt-and-suspenders: keep the quick menu hidden while prose is on screen.
    on "show" action SetVariable("quick_menu", False)
    on "replace" action SetVariable("quick_menu", False)

    vpgrid:
        cols 1
        xpos 36
        ypos 36
        xsize 1208
        ymaximum 648
        mousewheel True
        yinitial 1.0
        spacing 4

        if dialogue:
            for d in dialogue:
                window:
                    id d.window_id
                    style "nier_nvl_entry"
                    text d.what id d.what_id style "nier_nvl_dialogue"

        # Inline choices
        if items:
            null height 10
            for i in items:
                hbox:
                    spacing 8
                    xoffset 32
                    text "\u2023" color "#ffffff66" size 22 yalign 0.5 outlines [] font gui.interface_font
                    textbutton i.caption:
                        style "nier_nvl_choice_button"
                        action i.action


# =============================================================================
#  NVL CHOICE SCREEN -- for `menu (screen="nier_nvl_choice"):`
# =============================================================================

screen nier_nvl_choice(items):
    modal True

    add "#000000"

    vbox:
        xpos 68
        ypos 200
        spacing 10

        for i in items:
            hbox:
                spacing 8
                text "\u2023" color "#ffffff66" size 22 yalign 0.5 outlines [] font gui.interface_font
                textbutton i.caption:
                    style "nier_nvl_choice_button"
                    action i.action


# =============================================================================
#  SECTION TITLE SCREEN
# =============================================================================

screen nier_section_display(title):
    modal True
    add "#000000"

    text title:
        xalign 0.5
        yalign 0.45
        color "#cccccc"
        font gui.default_font
        size 34
        text_align 0.5
        outlines []

    timer 0.01 action With(Dissolve(0.6))
    timer 3.5 action Return()
    key "dismiss" action Return()


# =============================================================================
#  STYLES
# =============================================================================

# -- Individual NVL entry (reset all NVL positioning) --
style nier_nvl_entry is default:
    background None
    padding (0, 2, 0, 2)
    xpos 20
    ypos 20
    xfill True
    xmaximum 1180

# -- Prose text (reset NVL text positioning) --
style nier_nvl_dialogue is default:
    color "#e8e8e8"
    font gui.default_font
    size 24
    outlines []
    xpos 20
    ypos 20
    xmaximum 1140

# -- Choice buttons --
style nier_nvl_choice_button:
    background None
    hover_background Solid("#ffffff18")
    padding (6, 4)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style nier_nvl_choice_button_text:
    color "#888888"
    hover_color "#ffffff"
    font gui.default_font
    size 24
    outlines []


# =============================================================================
#  TRANSITIONS
# =============================================================================


# =============================================================================
#  HELPER LABELS
# =============================================================================

# Activate mode: save+disable quick_menu, set the active flag, fade to black,
# and beat. (Text isn't cleared here -- use nier_clear / nier_section for that.)
label nier_enter:
    $ nier_ta_prev_quick_menu = quick_menu
    $ nier_ta_active = True
    $ quick_menu = False
    scene black
    $ renpy.pause(0.8)
    return

# Deactivate mode: fade out, restore state.
label nier_exit:
    nvl clear
    $ nier_ta_active = False
    $ quick_menu = nier_ta_prev_quick_menu
    scene black
    return

# Show a section title card. Clears accumulated text.
label nier_section(title=""):
    nvl clear
    scene black
    with dissolve
    $ renpy.pause(0.3)
    call screen nier_section_display(title)
    scene black
    $ renpy.pause(0.3)
    return

# Manually clear accumulated text without leaving nier mode.
label nier_clear:
    nvl clear
    return
