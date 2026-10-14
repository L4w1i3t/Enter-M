# First-install notice: an illustrated four-leaf programme before the cold open.
# Original copy is retained. SVG artwork is cached by the normal image loader;
# all movement finishes, leaving a still, readable page.

define FIRST_BOOT_LEAVES = (
    ("THE DEMO", "Before you enter.", (
        "This is an early demo build of ENTER M.",
        "This build contains placeholder art, temporary audio, unfinished systems, proofs of concept, and experimental scenes.",
        "Some presentation, story flow, and archive features may change before a later release.",
    )),
    ("FROM THE CREATOR", "A personal note.", (
        "{b}Personal note: some placeholder artwork in this demo was created using Stable Diffusion (with my own trained generation models and pipelines).{/b}",
        "{b}They're PLACEHOLDERS. This game is being developed by one person who can't draw worth anything, nor can a dedicated artist be afforded.{/b}",
        "{b}If that upsets you or gives you tunnel vision that automatically invalidates the rest of the game, then I'm sorry for being a talentless hack.{/b}",
    )),
    ("FROM THE CREATOR / CONTINUED", "Give it a shot.", (
        "{b}All I ask is that you don't antagonize me for it, and at least give the game a shot.{/b}",
        "{b}Anyway...{/b}",
    )),
    ("CONTENT NOTICE", "Reader discretion.", (
        "The full story is planned to include mature topics.",
        "By playing this game, you agree that you are of sufficient age and mental state to handle the contents within.",
    )),
)

# Dark ink for copy/buttons, luminous matching ink for the illustrated cover.
# The creator's continued page is the invitation beat, hence its gold accent.
define FIRST_BOOT_INKS = ("#246761", "#714966", "#80591e", "#a13e3d")
define FIRST_BOOT_LIGHTS = ("#83c9ba", "#d6a4c6", "#edc77e", "#ed9989")
define FIRST_BOOT_ART = ("demo", "creator", "invitation", "content")
define FIRST_BOOT_CAPTIONS = ("A WORK IN PROGRESS", "A NOTE FROM THE CREATOR", "AN OPEN INVITATION", "BEFORE YOU STEP INSIDE")

transform first_boot_cover_half(mode="open", side=1):
    subpixel True
    xoffset (side * 670 if mode == "close" else 0)
    pause (0.38 if mode == "open" else 0.04 if mode == "reveal" else 0.0)
    easein_cubic (0.80 if mode == "open" else 0.68 if mode == "reveal" else 0.58) xoffset (0 if mode == "close" else side * 670)

transform first_boot_cover_type(mode="open"):
    alpha (1.0 if mode == "reveal" else 0.0)
    pause (0.28 if mode == "close" else 0.0)
    linear (0.18 if mode == "reveal" else 0.20) alpha (0.0 if mode == "reveal" else 1.0)
    pause (0.18 if mode == "open" else 0.0)
    linear (0.20 if mode == "open" else 0.0) alpha (1.0 if mode == "close" else 0.0)

transform first_boot_from_black:
    alpha 1.0
    linear 0.30 alpha 0.0

transform first_boot_art_arrive(leaf=0):
    subpixel True
    rotate_pad False
    alpha (0.0 if _preferences.transitions != 0 else 1.0)
    # Include the leaf in the compiled block so ATL restarts on page changes.
    xoffset (36 + leaf * 2 if _preferences.transitions != 0 else 0)
    rotate (4 if _preferences.transitions != 0 else 0)
    easein_cubic (0.48 if _preferences.transitions != 0 else 0.0) alpha 1.0 xoffset 0 rotate 0

transform first_boot_leaf_arrive(leaf=0):
    subpixel True
    alpha (0.0 if _preferences.transitions != 0 else 1.0)
    yoffset (12 + leaf if _preferences.transitions != 0 else 0)
    easein_cubic (0.32 if _preferences.transitions != 0 else 0.0) alpha 1.0 yoffset 0

screen enter_m_boot_cover(mode="open"):
    zorder 210
    modal True
    key "game_menu" action NullAction()
    key "dismiss" action NullAction()
    add Transform("assets/gui/first_boot/opening_seal.svg", crop=(0, 0, 640, 720)) at first_boot_cover_half(mode, -1)
    add Transform("assets/gui/first_boot/opening_seal.svg", crop=(640, 0, 640, 720)) xpos 640 at first_boot_cover_half(mode, 1)
    fixed:
        at first_boot_cover_type(mode)
        text "ENTER M":
            style "first_boot_brand"
            size 44
            xalign 0.5
            ypos 560
        text ("BEFORE THE STORY" if mode == "open" else "NOW PRESENTING"):
            style "first_boot_micro"
            color "#d1b88c"
            xalign 0.5
            ypos 624
    if mode == "open":
        add Solid("#000000") at first_boot_from_black
        timer 1.20 action Hide("enter_m_boot_cover")
    elif mode == "reveal":
        timer 0.74 action Hide("enter_m_boot_cover")

screen enter_m_first_boot_notice():
    modal True
    zorder 200
    default leaf = 0
    default closing = False

    # Only the final explicit action acknowledges the notice. Normal dialogue
    # dismissal, rollback, skip, and the game-menu binding cannot bypass it.
    key "game_menu" action NullAction()
    key "rollback" action NullAction()
    key "rollforward" action NullAction()

    add "assets/gui/first_boot/backdrop.svg"
    add Solid(FIRST_BOOT_INKS[leaf]) xysize (7, 720)
    add Solid(FIRST_BOOT_INKS[leaf]) xpos 64 ypos 99 xysize (42, 3)
    add Solid("#74695750") xpos 119 ypos 100 xysize (651, 1)

    fixed:
        xpos 874
        ypos 168
        xysize (360, 400)
        at first_boot_art_arrive(leaf)
        add "assets/gui/first_boot/" + FIRST_BOOT_ART[leaf] + ".svg"

    text "ENTER M":
        style "first_boot_brand"
        xpos 897
        ypos 50
    text "%02d / 04" % (leaf + 1):
        style "first_boot_micro"
        color FIRST_BOOT_LIGHTS[leaf]
        size 15
        xpos 898
        ypos 600
    text FIRST_BOOT_CAPTIONS[leaf]:
        style "first_boot_micro"
        size 13
        color FIRST_BOOT_LIGHTS[leaf]
        xpos 898
        ypos 633
    text "A story in progress.":
        style "first_boot_body"
        color "#aabbb8"
        size 18
        xpos 898
        ypos 662

    text "PLEASE READ / FIRST VISIT":
        style "first_boot_micro"
        xpos 64
        ypos 54

    fixed:
        at first_boot_leaf_arrive(leaf)
        text FIRST_BOOT_LEAVES[leaf][0]:
            style "first_boot_micro"
            color FIRST_BOOT_INKS[leaf]
            xpos 64
            ypos 123
        text FIRST_BOOT_LEAVES[leaf][1]:
            style "first_boot_heading"
            xpos 62
            ypos 151
        vbox:
            xpos 64
            ypos 242
            xsize 706
            spacing (13 if leaf == 1 else 24)
            for paragraph in FIRST_BOOT_LEAVES[leaf][2]:
                text paragraph:
                    style "first_boot_body"
                    size (21 if leaf == 1 else 26)

    add Solid("#74695760") xpos 64 ypos 593 xysize (708, 1)
    hbox:
        xpos 64
        ypos 615
        spacing 10
        for index in range(len(FIRST_BOOT_LEAVES)):
            fixed:
                xysize (44, 44)
                add Solid(FIRST_BOOT_INKS[index] if leaf == index else "#e0d7c7")
                add Solid(FIRST_BOOT_INKS[index]) ypos 41 xysize (44, 3)
                text "%02d" % (index + 1):
                    style "first_boot_micro"
                    color ("#fff0d9" if leaf == index else FIRST_BOOT_INKS[index])
                    align (0.5, 0.5)

    if leaf > 0:
        textbutton "Back":
            id "notice_back"
            style "first_boot_back"
            xpos 308
            ypos 615
            sensitive not closing
            action SetScreenVariable("leaf", leaf - 1)

    textbutton ("I understand. Enter." if leaf == len(FIRST_BOOT_LEAVES) - 1 else "Continue  >"):
        id "notice_continue"
        style "first_boot_button"
        background Solid(FIRST_BOOT_INKS[leaf])
        hover_background Solid("#28343c")
        xpos 484
        ypos 610
        xysize (288, 54)
        default_focus True
        sensitive not closing
        action (If(_preferences.transitions == 0, Return(True), [SetScreenVariable("closing", True), Show("enter_m_boot_cover", mode="close")]) if leaf == len(FIRST_BOOT_LEAVES) - 1 else SetScreenVariable("leaf", leaf + 1))

    # Closing is presentation only: the caller acknowledges after this return.
    # Repeated input cannot advance or write persistent state during the wipe.
    if closing:
        timer 0.64 action Return(True)

    text "Take your time. Continue when you're ready.":
        style "first_boot_micro"
        size 12
        kerning 0.0
        xpos 64
        ypos 684

style first_boot_body is default:
    font gui.default_font
    color "#233132"
    size 26
    outlines []
    line_spacing 3
    slow_cps 0
    xmaximum 706

style first_boot_heading is first_boot_body:
    size 54
    bold True
    line_spacing 0

style first_boot_micro is first_boot_body:
    font gui.interface_font
    size 14
    kerning 1.2
    color "#53615e"

style first_boot_brand is first_boot_micro:
    size 31
    color "#e9dfce"
    kerning 4.0

style first_boot_button is button:
    background Solid("#243b3e")
    hover_background Solid("#9d433e")
    padding (16, 10)
    hover_sound None
    activate_sound None

style first_boot_button_text is first_boot_body:
    font gui.interface_font
    size 20
    color "#fff0d9"
    hover_color "#ffffff"
    align (0.5, 0.5)

style first_boot_back is first_boot_button:
    background None
    hover_background Solid("#d6cbbb")

style first_boot_back_text is first_boot_button_text:
    color "#53615e"
    hover_color "#233132"
