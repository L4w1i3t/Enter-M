init offset = -1

style default:
    font gui.default_font
    size gui.text_size
    color gui.text_color
    outlines [(1, "#02050acc", 0, 1)]
    line_overlap_split 1
    line_spacing 1

style default_monika is normal:
    slow_cps 30

style edited is default:
    font gui.interface_font
    outlines [(2, "#02050a", 0, 1)]
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos
    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

style normal is default:
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos

    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

style input:
    color gui.accent_color

style hyperlink_text:
    color gui.accent_color
    hover_color gui.hover_color
    hover_underline True

style splash_text:
    size 28
    color "#f4fbff"
    font gui.default_font
    text_align 0.5
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style splash_warning_panel is empty:
    xalign 0.5
    yalign 0.5
    xsize 760
    yminimum 250
    padding (48, 36, 48, 40)
    background "#050811dd"

style splash_warning_heading is gui_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 30
    color "#ff4968"
    xalign 0.5
    text_align 0.5
    outlines [(2, "#02040b", 0, 0), (1, "#ffffff66", 1, 1)]

# Logo-splash "system boot" chrome (see enter_m_splash_intro in splash.rpy).
style splash_boot_caption is gui_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 19
    color "#bfeeff"
    text_align 0.5
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff66", 0, 0)]

style splash_boot_micro is gui_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 13
    color "#5fbcd6"
    outlines [(1, "#02040b", 0, 0)]

style poemgame_text:
    yalign 0.5
    font gui.interface_font
    size 30
    color "#101820"
    outlines []

    hover_xoffset -3
    hover_outlines [(2, "#56d7ff88", 0, 0)]

style gui_text:
    font gui.interface_font
    color gui.interface_text_color
    size gui.interface_text_size


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.button_text_properties("button")
    yalign 0.5


style label_text is gui_text:
    color gui.accent_color
    size gui.label_text_size

style prompt_text is gui_text:
    color gui.text_color
    size gui.interface_text_size

style vbar:
    xsize gui.bar_size
    top_bar Solid("#56d7ff")
    bottom_bar Solid("#102431")

style bar:
    ysize 10
    base_bar Solid("#132532")
    thumb Solid("#56d7ff")

style scrollbar:
    ysize 10
    base_bar Solid("#132532")
    thumb Solid("#56d7ff")
    unscrollable "hide"
    bar_invert True


style vscrollbar:
    xsize 10
    base_bar Solid("#132532")
    thumb Solid("#56d7ff")
    unscrollable "hide"
    bar_invert True

style slider:
    ysize 10
    base_bar Solid("#132532")
    thumb Solid("#ff315b")

style vslider:
    xsize gui.slider_size
    base_bar Solid("#132532")
    thumb Solid("#ff315b")

style frame:
    padding gui.frame_borders.padding
    background Frame("assets/gui/frame.png", gui.frame_borders, tile=gui.frame_tile)

screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        text what id "what" size enter_m_auto_say_text_size(what)

        if who is not None:

            window:
                style "namebox"
                text who id "who"



    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0

    use quick_menu

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue
style namebox is default
style namebox_label is say_label

# --- Live textbox opacity ---------------------------------------------------
# The dialogue box image is wrapped in a DynamicDisplayable so its alpha tracks
# persistent.textbox_opacity (exposed as a slider in Settings). DynamicDisplayable
# re-reads the persistent value whenever the say screen re-renders, so changing
# the slider takes effect on the very next line without any restart plumbing.
default persistent.textbox_opacity = 1.0

init python:
    def _enter_m_textbox_bg(st, at):
        try:
            a = float(persistent.textbox_opacity)
        except (TypeError, ValueError):
            a = 1.0
        a = max(0.0, min(1.0, a))
        # Map slider 0..1 to alpha 0.2..1.0 so the box stays faintly visible at
        # the low end -- the text never floats over a fully transparent panel.
        a = 0.2 + 0.8 * a
        return Transform("assets/gui/textbox.png", alpha=a, xalign=0.5, yalign=1.0), None

image enter_m_textbox_bg = DynamicDisplayable(_enter_m_textbox_bg)

style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background "enter_m_textbox_bg"

style window_monika is window:
    background "enter_m_textbox_bg"

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("assets/gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    color gui.accent_color
    font gui.name_font
    size gui.name_text_size
    xalign gui.name_xalign
    yalign 0.5
    outlines [(3, "#123a5a", 0, 0), (1, "#02050a", 1, 1)]

style say_dialogue:
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos
    size gui.say_text_size

    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

image ctc:
    xalign 0.81 yalign 0.98 xoffset -5 alpha 0.0 subpixel True
    "assets/gui/ctc.png"
    block:
        easeout 0.75 alpha 1.0 xoffset 0
        easein 0.75 alpha 0.5 xoffset -5
        repeat

style ctc_text is gui_text:
    color "#ff315b"
    size 20
    outlines [(1, "#02050a", 0, 1)]

image input_caret:
    Solid("#ff315b")
    size (2,25) subpixel True
    block:
        linear 0.35 alpha 0
        linear 0.35 alpha 1
        repeat

screen input(prompt):
    style_prefix "input"

    window:

        has vbox:
            xpos gui.text_xpos
            xanchor 0.5
            ypos gui.text_ypos

        text prompt style "input_prompt"
        input id "input"

style input_prompt is default

style input_prompt:
    xmaximum gui.text_width
    xalign gui.text_xalign
    text_align gui.text_xalign

style input:
    caret "input_caret"
    xmaximum gui.text_width
    xalign 0.5
    text_align 0.5

screen choice(items):
    style_prefix "choice"

    vbox:
        for idx, i in enumerate(items):
            textbutton i.caption action exam_guard_choice_action(i.action) at choice_button_in(idx * 0.07), choice_button_hover

style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 280
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    xsize gui.choice_button_width
    padding (26, 13, 26, 13)
    background "#071019e8"
    hover_background "#2a1020f2"
    selected_background "#183447f2"
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")
    outlines [(1, "#02050a", 0, 1)]

transform choice_button_hover:
    subpixel True
    on hover:
        easeout 0.12 xoffset 10
    on idle:
        easeout 0.16 xoffset 0

# Entrance animation for the choice option boxes: each box flies in from off the
# right edge, overshoots slightly PAST its resting spot, then recoils back to 0,
# fading in as it travels. `delay` staggers the boxes so they cascade in (the
# screens below pass index * a small step).
#
# This is applied TOGETHER with choice_button_hover via `at ..., choice_button_hover`.
# They are two independent transforms, each tracking its own xoffset, and Matsu'Py
# adds composed offsets -- so the slide-in settling at 0 and the hover's +10 nudge
# coexist without clobbering each other.
transform choice_button_in(delay=0.0):
    subpixel True
    alpha 0.0
    xoffset 720          # start fully off-screen to the right
    pause delay          # per-button stagger
    parallel:
        easeout 0.16 alpha 1.0
    parallel:
        easeout 0.34 xoffset -20   # slide in, overshoot a touch past rest
        easein 0.20 xoffset 0      # ...then recoil back to the resting spot
# --- Feel knobs (tweak to taste) ---------------------------------------------
#   xoffset 720    : how far off-screen-right they start (bigger = longer travel).
#   easeout 0.34   : slide-in speed (smaller number = snappier).
#   xoffset -20    : recoil depth -- how far PAST rest they overshoot (more = bouncier).
#   easein 0.20    : recoil settle speed.
#   idx * 0.07 (in the screens below): per-box cascade gap (bigger = more staggered).

define config.narrator_menu = True

style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 280
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    xsize gui.choice_button_width
    padding (26, 13, 26, 13)
    background "#071019e8"
    hover_background "#2a1020f2"
    selected_background "#183447f2"
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")
    outlines [(1, "#02050a", 0, 1)]

screen quick_menu():

    zorder 100

    if quick_menu:

        $ _phone_quick_count = phone_notification_count()

        vbox:
            style_prefix "quick"

            xpos 12
            yalign 1.0
            yoffset -12
            spacing 4

            textbutton _("History") action ShowMenu('history')
            textbutton _("Skip") action Skip()
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            # textbutton _("Save") action ShowMenu('save')
            # textbutton _("Load") action ShowMenu('load')
            button:
                style "quick_button"
                action [Hide("phone_notification_alert"), Show("phone_contacts_screen")]

                fixed:
                    xysize (72, 21)

                    text _("Phone") style "quick_button_text":
                        xalign (0.0 if _phone_quick_count else 0.5)
                        yalign 0.5

                    if _phone_quick_count:
                        $ _phone_quick_badge_width = phone_badge_width(_phone_quick_count, min_width=18)

                        fixed:
                            xalign 1.0
                            yalign 0.5
                            xysize (_phone_quick_badge_width, 18)
                            at phone_notification_badge_arrive

                            add PhonePanel(_phone_quick_badge_width, 18, "#0a84ff", bottom="#0066d6", radius=9)

                            text str(_phone_quick_count) style "phone_badge_text":
                                xalign 0.5
                                yalign 0.5

            textbutton _("People") action Show("character_thoughts_screen")
            textbutton _("Settings") action ShowMenu('preferences')

        # Polling is cheap (the current catalog is tiny) and action-driven, so
        # no sound or saved-state mutation happens during screen prediction.
        # The Function action must stay void: a False/True result would end the
        # active say interaction and make dialogue advance without Auto enabled.
        timer 0.5 repeat True action Function(phone_notification_poll_action, _update_screens=False)

default quick_menu = True

style quick_button:
    properties gui.button_properties("quick_button")
    xsize 88
    ysize 26
    background Solid("#05090fcc")
    hover_background Solid("#2a1020f2")
    padding (8, 2, 8, 3)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style quick_button_text:
    properties gui.button_text_properties("quick_button")
    font gui.interface_font
    size 12
    color "#d6e6ee"
    hover_color "#ff315b"
    text_align 0.5
    xalign 0.5
    yalign 0.5
    outlines [(1, "#02050a", 0, 1)]

init python:
    def FinishEnterName():
        if not player: return
        persistent.playername = player
        renpy.save_persistent()
        renpy.hide_screen("name_input")
        renpy.jump_out_of_context("start")

screen navigation(menu_context=None, embedded=False):

    $ nav_main = main_menu if menu_context is None else menu_context
    $ _msbf_save_load_locked = (not nav_main and msbf_save_load_locked())

    vbox:

        style_prefix "navigation"
        xfill True

        if not embedded:
            if nav_main:
                xpos gui.navigation_xpos
                yalign 0.8
            else:
                xalign 0.5
                yalign 0.0

        spacing gui.navigation_spacing

        # ONE DOOR WHERE THERE WERE TWO. Save and Load were never two ideas --
        # they were one list of slots drawn twice, and only the click differed.
        # Both now open the RECORD BANK (game/data_bank.rpy), which restores,
        # writes, copies, re-labels and erases off that one list. The door is
        # still called "Load Game" at the title, because with no session
        # running that is the only one of the five it can do; in-game it is
        # "Records", because from there it can do all of them.
        if nav_main:

            textbutton _("New Game") action Start()

            textbutton _("Load Game") action ShowMenu("data_bank", start_mode="restore") sensitive (renpy.get_screen("data_bank") == None)

        else:

            textbutton _("History") action [ShowMenu("history"), SensitiveIf(renpy.get_screen("history") == None)]
            # Custom Calendar button
            textbutton _("Calendar") action ShowMenu("calendar_menu") sensitive renpy.get_screen("calendar_menu") == None

            textbutton _("Records") action ShowMenu("data_bank", start_mode="write") sensitive (not _msbf_save_load_locked and renpy.get_screen("data_bank") == None)

        if nav_main:

            textbutton _("Archive") action ShowMenu("archive")
            textbutton _("Credits") action ShowMenu("credits_menu")

        else:
            textbutton _("Main Menu") action MainMenu()

        textbutton _("Settings") action [ShowMenu("preferences"), SensitiveIf(renpy.get_screen("preferences") == None)]

        if renpy.variant("pc"):

            textbutton _("Quit") action Quit(confirm=not nav_main)

style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")
    xsize 238
    ysize 42
    padding (14, 5, 14, 5)
    background "#071019dd"
    hover_background "#2a1020f2"
    selected_background "#183447f2"
    insensitive_background "#03070baa"
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style navigation_button_text:
    properties gui.button_text_properties("navigation_button")
    font "assets/fonts/SF Automaton Extended.ttf"
    size 19
    color "#eaf8ff"
    hover_color "#ff315b"
    selected_color "#8bd7ff"
    insensitive_color "#7b8795"
    outlines [(2, "#02050a", 0, 1)]
    hover_outlines [(2, "#02050a", 0, 1), (1, "#ff315b99", 0, 0)]
    insensitive_outlines [(1, "#02050a", 0, 1)]

# -----------------------------------------------------------------------------
# LEGACY MAIN MENU -- the former broadcast-desk treatment.
#
# The live title screen now lives in ``main_menu_room.rpy``. This authored
# version remains available under an explicit legacy name for comparison and
# rollback, but nothing invokes it during normal play.
#
# THE LAYOUT, AND WHY IT IS THIS ONE
#   Nearly every VN puts its options in a vertical list down one side. This one
#   spreads them along the bottom as a rail of numbered CHANNEL CARDS and gives
#   the whole middle of the screen over to a STAGE MONITOR that previews
#   whichever card is under the cursor. Left of the monitor is the title block
#   and a live ON AIR tally; right of it is the telemetry stack. The result is
#   a desk somebody is running a broadcast from -- which is the only kind of
#   room Matsuda would agree to be in -- while still being a plain row of eight
#   labelled buttons that you click.
#
# HOW IT HANGS TOGETHER
#   `mm_channels` is the single source of truth. The rail draws from it, the
#   monitor reads the selected row out of it, and the beam between the two is
#   positioned from the same arithmetic. Adding an option means adding a row.
#   `mm_sel` is the previewed channel; every card sets it on hover, and because
#   Matsu'Py treats keyboard focus as hover, arrowing along the rail previews too.
#
# STYLE
#   Same retro-terminal chrome as the pause menu and boot splash
#   (Steins;Gate-INSPIRED, not lifted -- our own SIGNAL / LINK / 0x4D motif;
#   cyan #56d7ff, red #ff315b). Every flourish is ATL / Solid / Text based, so
#   it is rock-solid at cold start -- this is the first screen shown and no
#   shader scene has loaded yet.
# -----------------------------------------------------------------------------

# --- ambient field ----------------------------------------------------------

# Faint rolling grain over the whole field.
transform mm_grain:
    subpixel True
    alpha 0.0
    easeout 0.9 alpha 0.05

# A second scanline sweeping UP (red), counter to menu_scanline_slow's descent.
transform mm_scanline_up:
    subpixel True
    ypos 744
    alpha 0.0
    pause 1.1
    block:
        alpha 0.0
        ypos 744
        linear 0.14 alpha 0.5
        linear 5.5 ypos -24
        linear 0.2 alpha 0.0
        pause 3.1
        repeat

# --- boot-in ----------------------------------------------------------------

# Any panel of the desk arriving on start-up.
transform mm_panel_in(delay=0.0, xoff=-48, yoff=0):
    subpixel True
    alpha 0.0
    xoffset xoff
    yoffset yoff
    pause delay
    easeout 0.45 alpha 1.0 xoffset 0 yoffset 0

# Bright scan node that rides down the spine between the title block and the
# monitor, on a loop.
#
# THE TRAVEL IS THE SPINE MINUS THE NODE, and it has to be written that way
# because ypos moves the node's TOP. The spine is 356px from MM_MY, the node is
# MM_SCAN_H tall, and the old end value was a bare 448 -- which put the node's
# foot at 482 against a spine that stops at 464, so twice every nine seconds a
# bright bar hung 19px off the end of the rail into open air, held there for
# the whole 0.18s fade. Deriving both ends from the spine means the node lands
# flush on it instead.
define MM_SCAN_H = 34

transform mm_rail_scan:
    subpixel True
    ypos MM_MY
    alpha 0.0
    pause 0.7
    block:
        alpha 0.0
        ypos MM_MY
        linear 0.18 alpha 1.0
        linear 2.4 ypos (MM_MY + MM_MH - MM_SCAN_H)
        linear 0.18 alpha 0.0
        pause 1.5
        repeat

# RGB-split ghosts for the title: a cyan copy drifting left, a red copy right,
# both twitching on an occasional glitch beat under the crisp white master.
# `d` is the direction the ghost drifts: -1 for cyan, +1 for red. They were two
# hand-mirrored copies of the same beat, which meant retiming the glitch had to
# be done twice in lockstep or the two ghosts desynced.
transform mm_glitch(d=-1):
    subpixel True
    xoffset (1 * d)
    alpha 0.38
    block:
        pause 1.7
        linear 0.03 xoffset (4 * d) alpha 0.62
        linear 0.03 xoffset (1 * d) alpha 0.34
        linear 0.03 xoffset (3 * d) alpha 0.5
        linear 0.04 xoffset (1 * d) alpha 0.38
        pause 1.0
        linear 0.03 xoffset (5 * d)
        linear 0.03 xoffset (1 * d)
        pause 0.5
        repeat

# Accent underline that wipes out from the left, then shimmers.
transform mm_underline(delay=0.55):
    subpixel True
    xanchor 0.0
    xzoom 0.0
    alpha 0.0
    pause delay
    parallel:
        easeout 0.5 xzoom 1.0
    parallel:
        easeout 0.35 alpha 1.0
    block:
        ease 2.2 alpha 0.45
        ease 2.2 alpha 1.0
        repeat

# One equalizer bar: grows from its baseline (yanchor 1.0) on a staggered loop.
transform mm_eq_bar(delay=0.0, period=0.75, lo=0.2):
    subpixel True
    yanchor 1.0
    yzoom lo
    pause delay
    block:
        ease period yzoom 1.0
        ease period yzoom lo
        repeat

# The ON AIR tally lamp: a slow, deliberate throb that never quite goes out.
transform mm_tally_lamp:
    subpixel True
    alpha 1.0
    block:
        easeout 0.55 alpha 0.34
        easein 0.55 alpha 1.0
        repeat

# --- the rail ---------------------------------------------------------------

# THE MENU-WARMING EXPERIMENT WAS REMOVED (Aug 27 2026). What it did, and why
# it is not coming back in that form -- the finding underneath it is real and
# somebody will be tempted again:
#
#   Opening a menu stalls for one frame while its art is decoded. Measured cold
#   from this desk: Arcade 186ms, Settings 44ms, Archive 34ms. Ren'Py has a
#   predictive loader for exactly that, and IT NEVER RUNS HERE -- prediction
#   only happens on an "expensive" idle frame, which core.py gates on
#   `needs_redraw` being false, and this desk animates something every frame by
#   design. So `renpy.start_predict_screen` alone does nothing at all (measured
#   at 0.3s, 0.6s, 1s, 2s and 4s of lead: 180ms every time), and
#   `force_prediction` does the whole walk in a single 115ms frame, which is
#   not fixing a stall, only moving it.
#
#   Driving the coroutine by hand from `config.periodic_callbacks` DID fix the
#   menu -- Arcade 186ms -> 50ms. It also put a callback into every interaction
#   in the game and left `_predict_screen` pointing at five menu screens after
#   the desk was gone, pinning their textures in the image cache and re-walking
#   their trees during play. That is a bad trade for a boss fight, and it is
#   why this is gone.
#
# THE ACTUAL PROBLEM IS THE ART, NOT THE LOADER. The Arcade's five covers are
# 1254x1254 for a shelf that draws them at 156px and a featured box that draws
# them at 320px -- fifteen times the pixels they ever show. Ablating them
# dropped the Arcade's cold open from 186ms to 41ms on its own. Resize the
# covers and there is nothing left to hide.

# How far a card climbs when it takes focus, and how far down its own alpha
# sits when it has not. A card RESTS at yoffset MM_CARD_LIFT and arrives at 0
# -- the raised position is the zero -- so the button underneath it can own
# both rows of pixels at once. See the rail loop for why that matters.
define MM_CARD_LIFT = 11
define MM_CARD_DIM = 0.82

# A channel card, in TWO transforms that are deliberately kept apart: the one
# that brings it in, and the one that answers the pointer. Both of them hear
# every event -- a Button hands hover/idle to its direct child and a Transform
# passes it on down its own chain, so an at_list of two transforms is two
# independent listeners -- and each simply ignores what it has no handler for.
#
# `ON SHOW` DOES NOT WORK ON A BUTTON INSIDE A SCREEN, and this entrance used
# to be written with one, so it had never once played (measured: every card was
# already at rest 0.12s in, before the first stagger delay was even up). A
# screen relays "show" to its top-level children from update(), and Ren'Py runs
# every screen's update() BEFORE focus.before_interact() -- which immediately
# calls Button.unfocus(default=True) on all eight cards, overwriting the
# pending event with "idle". A transform only ever sees the LAST event set
# before its first execute, so "show" was gone before anything could read it,
# and the `on show` block was dead code that left the cards at their defaults:
# fully opaque, already home. The entrance therefore lives in a plain timed
# block, which starts at st=0 and cannot be interrupted by an event it has no
# handler for. This is the same shape mm_panel_in above already uses.
transform mm_card_rise(delay=0.0):
    subpixel True
    alpha 0.0
    yoffset 26
    pause delay
    parallel:
        easeout 0.34 alpha 1.0
    parallel:
        easeout_cubic 0.42 yoffset 0

# THE LIFT IS A MEASUREMENT, NOT A TASTE. 11 is exactly the gap between the
# rail's marker line and the top of a card: the marker is 3px at
# mm_rail_line_y (486) and the cards rest at mm_rail_y (500), so a focused card
# rising 11px puts its own bezel at 489 -- the pixel the marker ends on. The
# two become one continuous band, which is the whole gesture: the selected
# channel reaches up and joins the rail feeding the monitor.
#
# WHICH IS WHY THERE IS NO `zoom` HERE. A scale on this transform is anchored
# at the card's top-left, so it grew the card RIGHTWARD: at 1.035 the 142px
# card became 147px while the marker above it stayed 142px, and the accent
# overhung the marker by 5px on the right (measured: marker x 493-634, accent
# x 493-639). It also ate half the 10px gap to the next card, so the rail's
# spacing went uneven on hover. Keep every card exactly one slot wide.
#
# This one DOES want events, and it is the only reason the two are separate: an
# `on idle` in the same transform as the entrance would fire at startup and
# overwrite it. Here it has nothing to overwrite.
#
# The plate brightens on the same eased curve instead of snapping, so the lift
# and the lamp are one movement rather than a slide with a flashbulb in it.
# Hover and idle share a duration on purpose: sweeping along the rail puts two
# cards in the air at once, and the one falling has to fall at the rate the one
# rising rises, or the pair reads as a stutter.
transform mm_card_lift:
    subpixel True
    alpha MM_CARD_DIM
    yoffset MM_CARD_LIFT
    on hover:
        easeout_cubic 0.18 alpha 1.0 yoffset 0
    on idle:
        easeout_cubic 0.18 alpha MM_CARD_DIM yoffset MM_CARD_LIFT

# The marker under the rail and the beam up to the monitor take the selected
# card's x as a PARAMETER, which is the point: changing a screen transform's
# arguments rebuilds it, and the rebuild inherits the old xpos, so these ease
# across to the new card instead of snapping to it.
transform mm_marker_slide(tx=0):
    subpixel True
    easeout_cubic 0.24 xpos tx

# The monitor's readout, likewise re-armed by the selection so that every
# channel change replays its own arrival...
transform mm_readout_swap(key=0):
    subpixel True
    alpha 0.0
    xoffset -18
    easeout 0.20 alpha 1.0 xoffset 0

# ...under the tube flare that covers the change.
transform mm_channel_flash(key=0):
    subpixel True
    additive 1.0
    alpha 0.30
    linear 0.18 alpha 0.0

# A scanline confined to the monitor glass.
transform mm_monitor_scan(top=138, bottom=460):
    subpixel True
    ypos top
    alpha 0.0
    block:
        alpha 0.0
        ypos top
        linear 0.12 alpha 0.42
        linear 3.2 ypos bottom
        linear 0.16 alpha 0.0
        pause 1.6
        repeat


# --- desk geometry ----------------------------------------------------------
# The rail row is centred as a whole, so adding or removing a channel re-spaces
# everything without another number having to move. The stage monitor's box has
# ONE home; everything drawn on the glass is placed relative to these four.
define MM_CARD_W = 142
define MM_CARD_H = 130
define MM_CARD_GAP = 10
define MM_RAIL_Y = 500
define MM_RAIL_LINE_Y = 486
define MM_MX = 324
define MM_MY = 108
define MM_MW = 620
define MM_MH = 356


# The channel-card plate is authored at its 205px nine-slice source size. This
# avoids decoding and scaling the old 1024px placeholder on the title screen;
# only its quiet gradient centre stretches into the 142x130 card face.
define MM_PLATE = Frame("assets/gui/menu/channel_plate.png", 6, 6)


# The step wedge on the stage monitor's test card: light to dark, warm white
# through to the panel's own blue-black, so the monitor always has something
# calibrated-looking on it even when no channel is selected.
define MM_TEST_WEDGE = [
    "#eaf8ff", "#cfe9f4", "#b3d9ea", "#97c9e0", "#7cb9d6", "#61a8cc", "#4d97c0",
    "#3d85ad", "#31739a", "#276187", "#1e5074", "#173f60", "#11304d", "#0c223a",
]

# The nine equalizer bars' start phases. A plain list rather than a `$` inside
# the screen, which was one more statement running on every execution.
define MM_SIGNAL_PHASE = [0.0, 0.18, 0.36, 0.06, 0.28, 0.10, 0.22, 0.40, 0.14]

# The wedge and the equalizer, each collapsed from a screen `for` loop into ONE
# constant displayable. A `for` in screen language is never constant -- its
# loop variable is not -- so fourteen wedge bars and nine equalizer bars were
# twenty-three nodes rebuilt on every execution, to draw a picture that has
# never once changed. Built here instead, they are two nodes that are built
# once. The ATL on each bar keeps running exactly as it did; a transform does
# not care whether the screen re-executed around it.
init python:

    @renpy.pure
    def enter_m_mm_wedge(bar_w=18, pitch=22, bar_h=82):
        return Fixed(
            *[Solid(c, xysize=(bar_w, bar_h), xpos=i * pitch, ypos=0)
            for i, c in enumerate(MM_TEST_WEDGE)],
            xysize=((len(MM_TEST_WEDGE) - 1) * pitch + bar_w, bar_h)
        )

    # yanchor 1.0 twice over, and both are load-bearing: the INNER one is
    # mm_eq_bar's own, so yzoom shrinks the bar toward its foot instead of its
    # head, and the OUTER one pins that shrunken render's foot to the baseline
    # so the bar grows up out of the panel floor rather than hanging from a
    # ceiling.
    @renpy.pure
    def enter_m_mm_eq(bar_w=16, pitch=26, bar_h=40):
        bars = [
            Transform(
                At(Solid("#56d7ff", xysize=(bar_w, bar_h)),
                mm_eq_bar(phase, 0.62 + 0.04 * j, 0.18)),
                xpos=j * pitch, ypos=bar_h, yanchor=1.0,
            )
            for j, phase in enumerate(MM_SIGNAL_PHASE)
        ]
        return Fixed(
            *bars,
            xysize=((len(MM_SIGNAL_PHASE) - 1) * pitch + bar_w, bar_h)
        )


# --- Reusable pieces of the desk --------------------------------------------

# The telemetry row and the legend row used to be `use` screens here. They are
# now the pure factories `enter_m_readout_row` / `enter_m_legend_row` further
# down this file, for the reason documented alongside them.

screen main_menu_terminal_legacy():

    tag menu

    # Which channel the stage monitor is previewing. Every card sets this when
    # it takes focus, and it deliberately does NOT reset when focus is lost, so
    # the monitor keeps showing the last thing the player looked at.
    default mm_sel = 0

    python:
        # ONE table drives the whole desk: the rail of cards, the monitor
        # readout, and the beam that ties the two together.
        #   (button label, the line the monitor prints, what clicking it does)
        mm_channels = [
            (_("New Game"),  _("START A NEW RECORDING."),             Start()),
            (_("Load Game"), _("RESUME A SAVED RECORDING."),          ShowMenu("data_bank")),
            (_("Arcade"),    _("CABINET FLOOR. NO STORY ATTACHED."),  ShowMenu("arcade_hub")),
            (_("Archive"),   _("EVERYTHING THE TERMINAL HAS KEPT."),  ShowMenu("archive")),
            (_("Credits"),   _("WHO IS RESPONSIBLE FOR ALL THIS."),   ShowMenu("credits_menu")),
            (_("Donate"),    _("PUT A COIN IN THE SLOT."),            OpenURL("https://ko-fi.com/l4w1i3t")),
            (_("Settings"),  _("TUNE THE SET UNTIL IT LOOKS RIGHT."), ShowMenu("preferences")),
            (_("Quit"),      _("CUT THE FEED."),                      Quit(confirm=False)),
        ]

        # Rail geometry, derived from the module-level constants at the top of
        # this section so the values the chrome is built from are the values
        # the screen lays out with.
        mm_count = len(mm_channels)
        mm_card_w, mm_card_h, mm_card_gap = MM_CARD_W, MM_CARD_H, MM_CARD_GAP
        mm_rail_w = mm_count * mm_card_w + (mm_count - 1) * mm_card_gap
        mm_rail_x = (1280 - mm_rail_w) // 2
        mm_rail_y = MM_RAIL_Y
        mm_rail_line_y = MM_RAIL_LINE_Y
        mm_mx, mm_my, mm_mw, mm_mh = MM_MX, MM_MY, MM_MW, MM_MH

        # The previewed channel, clamped in case the table ever shrinks under a
        # stale selection.
        mm_cur = min(mm_sel, mm_count - 1)
        mm_label, mm_strap, mm_action = mm_channels[mm_cur]
        mm_cur_x = mm_rail_x + mm_cur * (mm_card_w + mm_card_gap)

    # --- background field ---
    add gui.main_menu_background
    # The control-room plate is already dark. A restrained grade keeps the
    # cyan/red interface readable without burying the physical set dressing.
    add Solid("#02050a63")
    add "vignette":
        alpha 0.40
    add "noise" at mm_grain
    add Solid("#56d7ff20") xysize (1280, 2) at menu_scanline_slow
    add Solid("#ff2f5f14") xysize (1280, 1) at mm_scanline_up

    # --- header micro-line, both ends ---
    hbox:
        xpos 44
        ypos 30
        spacing 8
        add Solid("#ff315b") xysize (6, 6) yalign 0.5 at console_blink
        text "MAIN TERMINAL // 0x4D":
            style "mm_micro"

    text "BUILD v[config.version]  ::  SIGNAL LOCKED":
        style "mm_micro"
        xanchor 1.0
        xpos 1236
        ypos 30

    # =========================================================================
    # LEFT: title block, ON AIR tally, controls
    # =========================================================================

    fixed:
        at mm_panel_in(0.04, -64, 0)

        # RGB-split glitch title (three stacked copies of the same word)
        fixed:
            xysize (256, 48)
            xpos 44
            ypos 62
            text "ENTER-M":
                style "mm_title_ghost_c"
                at mm_glitch(-1)
            text "ENTER-M":
                style "mm_title_ghost_r"
                at mm_glitch(1)
            text "ENTER-M":
                style "mm_title"

        add Solid("#56d7ff") xysize (220, 2) xpos 44 ypos 118 at mm_underline(0.55)

        text "BROADCAST DESK // 0x4D":
            style "mm_micro"
            xpos 44
            ypos 130

    # The tally. It is always lit, because this terminal is always transmitting
    # something at somebody.
    fixed:
        at mm_panel_in(0.26, -48, 0)

        add Solid("#170410f2") xysize (236, 66) xpos 44 ypos 186
        add Solid("#ff315b") xysize (4, 66) xpos 44 ypos 186
        add Solid("#ff5c7d") xysize (16, 16) xpos 70 ypos 211 at mm_tally_lamp
        text "ON AIR":
            style "mm_tally_text"
            xpos 102
            ypos 204
        add enter_m_brackets(236, 66, "#ff315b66", 14, 2) xpos 44 ypos 186

    fixed:
        at mm_panel_in(0.38, -40, 0)

        text "CONTROLS":
            style "mm_section_label"
            xpos 44
            ypos 300
        add Solid("#56d7ff33") xysize (236, 1) xpos 44 ypos 320

        add enter_m_legend_row(_("< >"), _("BROWSE CHANNELS")) xpos 44 ypos 334
        add enter_m_legend_row(_("ENTER"), _("OPEN CHANNEL")) xpos 44 ypos 368
        add enter_m_legend_row(_("CLICK"), _("SELECT CHANNEL")) xpos 44 ypos 402
        add enter_m_legend_row(_("ESC"), _("CUT THE FEED")) xpos 44 ypos 436

    # The spine that separates the title column from the monitor, with a scan
    # node riding down it.
    add Solid("#56d7ff55") xysize (2, 356) xpos 302 ypos 108 at mm_panel_in(0.10, -24, 0)
    add Solid("#8fe6ff") xysize (2, 34) xpos 302 at mm_rail_scan

    # =========================================================================
    # CENTRE: the stage monitor
    # =========================================================================

    fixed:
        at mm_panel_in(0.20, 0, 26)

        # glass, header strip, accent lip
        add Solid("#040c15f4") xpos mm_mx ypos mm_my xysize (mm_mw, mm_mh)
        add Solid("#0f2c42") xpos mm_mx ypos mm_my xysize (mm_mw, 28)
        add Solid("#56d7ff") xpos mm_mx ypos (mm_my + 28) xysize (mm_mw, 2)

        add Solid("#56d7ff") xysize (6, 6) xpos (mm_mx + 14) ypos (mm_my + 11) at console_blink
        text "STAGE MONITOR":
            style "mm_monitor_title"
            xpos (mm_mx + 30)
            ypos (mm_my + 5)
        text ("CH.%02d" % (mm_cur + 1)):
            style "mm_monitor_code"
            xanchor 1.0
            xpos (mm_mx + mm_mw - 14)
            ypos (mm_my + 6)

        # --- the readout, re-armed on every channel change ---
        fixed:
            xysize (mm_mw, mm_mh - 30)
            xpos mm_mx
            ypos (mm_my + 30)
            at mm_readout_swap(mm_cur)

            text ("%02d" % (mm_cur + 1)):
                style "mm_channel_number"
                xpos 30
                ypos 26
            text mm_label:
                style "mm_channel_name"
                xpos 150
                ypos 44
            add Solid("#56d7ff") xysize (300, 2) xpos 152 ypos 98
            text mm_strap:
                style "mm_channel_strap"
                xpos 152
                ypos 112
                xmaximum 420

        # --- the test card ---
        # A step wedge and the station ident, which is what a monitor with
        # nothing to show shows. It also gives the logo a home now that it is
        # not sitting in a box of its own on the right of the screen.
        add Solid("#56d7ff1a") xysize (mm_mw - 60, 1) xpos (mm_mx + 30) ypos (mm_my + 184)

        add enter_m_mm_wedge() xpos (MM_MX + 30) ypos (MM_MY + 198)

        add Solid("#56d7ff26") xysize (1, 94) xpos (mm_mx + 366) ypos (mm_my + 192)
        add "assets/gui/logo.png":
            xcenter (mm_mx + 476)
            ycenter (mm_my + 232)
            zoom 0.17
            alpha 0.85
        text "STATION IDENT // 0x4D":
            style "mm_monitor_foot"
            xanchor 0.5
            xcenter (mm_mx + 476)
            ypos (mm_my + 282)

        add Solid("#56d7ff26") xysize (mm_mw - 60, 1) xpos (mm_mx + 30) ypos (mm_my + 312)
        text "LIVE FEED // 0x4D":
            style "mm_monitor_foot"
            xpos (mm_mx + 30)
            ypos (mm_my + 322)
        text ("CHANNEL %d OF %d" % (mm_cur + 1, mm_count)):
            style "mm_monitor_foot"
            xanchor 1.0
            xpos (mm_mx + mm_mw - 30)
            ypos (mm_my + 322)

        # scanline confined to the glass, then the flare that covers a change
        add Solid("#8be6ff1e") xysize (mm_mw, 2) xpos mm_mx at mm_monitor_scan(mm_my + 30, mm_my + mm_mh - 6)
        add Solid("#56d7ff") xpos mm_mx ypos mm_my xysize (mm_mw, mm_mh) at mm_channel_flash(mm_cur)

        add enter_m_brackets(MM_MW, MM_MH, "#56d7ff7a", 22, 2) xpos MM_MX ypos MM_MY

    # =========================================================================
    # RIGHT: telemetry stack
    # =========================================================================

    fixed:
        at mm_panel_in(0.32, 48, 0)

        # --- signal panel ---
        add Solid("#070f1af2") xpos 968 ypos 108 xysize (268, 150)
        add Solid("#12324a") xpos 968 ypos 108 xysize (268, 26)
        add Solid("#56d7ff") xpos 968 ypos 134 xysize (268, 2)
        add Solid("#56d7ff") xysize (6, 6) xpos 984 ypos 118 at console_blink
        text "SIGNAL // MAIN":
            style "mm_monitor_title"
            xpos 1000
            ypos 112

        add enter_m_mm_eq() xpos 988 ypos 174

        add Solid("#ff315b") xysize (6, 6) xpos 984 ypos 230 at console_blink
        text "LINK STABLE":
            style "mm_telemetry_accent"
            xpos 1000
            ypos 225
        add enter_m_brackets(268, 150, "#56d7ff6e", 18, 2) xpos 968 ypos 108

        # --- readout panel ---
        add Solid("#070f1af2") xpos 968 ypos 272 xysize (268, 192)
        add Solid("#12324a") xpos 968 ypos 272 xysize (268, 26)
        add Solid("#56d7ff") xpos 968 ypos 298 xysize (268, 2)
        add Solid("#56d7ff") xysize (6, 6) xpos 984 ypos 282 at console_blink
        text "TERMINAL // 0x4D":
            style "mm_monitor_title"
            xpos 1000
            ypos 276

        add enter_m_readout_row(_("FEED"), _("MAIN"), 236) xpos 984 ypos 316
        add enter_m_readout_row(_("BUILD"), "v" + config.version, 236) xpos 984 ypos 344
        add enter_m_readout_row(_("CHANNELS"), ("%02d" % mm_count), 236) xpos 984 ypos 372
        add enter_m_readout_row(_("SELECTED"), ("%02d" % (mm_cur + 1)), 236) xpos 984 ypos 400
        add enter_m_readout_row(_("STATUS"), _("NOMINAL"), 236) xpos 984 ypos 428

        add enter_m_brackets(268, 192, "#56d7ff6e", 18, 2) xpos 968 ypos 272

    # =========================================================================
    # BOTTOM: the channel rail
    # =========================================================================

    add Solid("#56d7ff26") xysize (mm_rail_w, 1) xpos mm_rail_x ypos (mm_rail_line_y + 1) at mm_panel_in(0.14, 0, 12)

    # The beam that ties the previewed card to the monitor above it. Drawn as
    # one sliding group so the marker and the beam can never disagree.
    fixed:
        at mm_marker_slide(mm_cur_x)
        add Solid("#56d7ff8c") xysize (2, 20) xpos (mm_card_w // 2) ypos 466
        add Solid("#bdf6ff") xysize (mm_card_w, 3) ypos mm_rail_line_y

    for mm_k, (mm_k_label, mm_k_strap, mm_k_action) in enumerate(mm_channels):

        # THE BUTTON IS TALLER THAN THE CARD, BY EXACTLY THE LIFT. The card
        # moves and the focus rectangle does not -- add_focus reports the
        # button's own rect, never the child's offset one -- so a button cut to
        # the card's size left an 11px strip along the top that was visibly
        # part of a raised card and not clickable, and a matching 11px strip
        # along the bottom that was clickable and empty. Starting the button
        # one lift HIGHER and letting the card rest at the bottom of it makes
        # the hot rectangle the union of both positions: wherever the card is,
        # the pointer is over it.
        button:
            style "mm_card_button"
            xysize (mm_card_w, mm_card_h + MM_CARD_LIFT)
            xpos (mm_rail_x + mm_k * (mm_card_w + mm_card_gap))
            ypos (mm_rail_y - MM_CARD_LIFT)
            action mm_k_action
            hovered SetScreenVariable("mm_sel", mm_k)
            default_focus (mm_k == 0)

            # This `fixed` is the button's ONLY child on purpose: hover and idle
            # transform events reach a button's direct child and stop there, so
            # anything nested deeper would never learn it was being pointed at.
            # Colour changes go through styles instead, which DO recurse. It
            # fills the whole button rather than just the card so its placement
            # inside the window can never come into it; the plate below is what
            # says where the card face actually starts.
            fixed:
                at [mm_card_rise(0.16 + 0.035 * mm_k), mm_card_lift]
                xysize (mm_card_w, mm_card_h + MM_CARD_LIFT)

                frame:
                    style "mm_card_plate"
                    xysize (mm_card_w, mm_card_h)
                text ("%02d" % (mm_k + 1)):
                    style "mm_card_slot"
                    xpos 12
                    ypos 16
                frame:
                    style "mm_card_pip"
                    xysize (6, 6)
                    xpos (mm_card_w - 18)
                    ypos 18
                text mm_k_label:
                    style "mm_card_label"
                    xalign 0.5
                    ypos 58
                text ">":
                    style "mm_card_caret"
                    xpos 12
                    ypos 98

    # =========================================================================
    # FOOTER + FRAME
    # =========================================================================

    add Solid("#56d7ff1a") xysize (1192, 2) xpos 44 ypos 664
    hbox:
        xpos 44
        ypos 674
        spacing 8
        add Solid("#345a6b") xysize (5, 5) yalign 0.5 at console_blink
        text "ENTER-M.SYS  ::  STATUS NOMINAL  //  MAIN TERMINAL":
            style "mm_footer_text"

    text ("%d CHANNELS ONLINE" % mm_count):
        style "mm_footer_text"
        xanchor 1.0
        xpos 1236
        ypos 674

    add enter_m_brackets(1252, 692, "#56d7ff3a", 26, 2) xpos 14 ypos 14

    # The Developer Hub's ONE hook into the shipping game. Everything it does
    # lives in addons/Dev Hub/; has_screen means deleting that folder removes
    # the feature cleanly instead of leaving a dangling `use` behind.
    if config.developer and renpy.has_screen("dev_hub_mount"):
        use dev_hub_mount

    key "K_ESCAPE" action Quit(confirm=False)


# --- Main-menu styles -------------------------------------------------------

style mm_micro is gui_text:
    font gui.interface_font
    size 12
    color "#6fb6c9"
    outlines [(1, "#02050a", 0, 1)]

style mm_title is gui_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 40
    color "#f2fbff"
    outlines [(2, "#02050a", 0, 1), (1, "#56d7ff88", 0, 0)]

style mm_title_ghost_c is mm_title:
    color "#56d7ff"
    outlines []

style mm_title_ghost_r is mm_title:
    color "#ff315b"
    outlines []

style mm_section_label is gui_text:
    font gui.interface_font
    size 12
    color "#4e8195"
    outlines [(1, "#02050a", 0, 1)]

style mm_tally_text is gui_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 26
    color "#ffd9e2"
    outlines [(2, "#02050a", 0, 1), (1, "#ff315baa", 0, 0)]

style mm_keycap is empty:
    background "#0d1c28"
    padding (8, 3, 8, 4)
    xsize 66
    ysize 22

style mm_keycap_text is gui_text:
    font gui.interface_font
    size 11
    color "#9fd8e8"
    xalign 0.5
    outlines [(1, "#02050a", 0, 1)]

style mm_legend_text is gui_text:
    font gui.interface_font
    size 12
    color "#7fa3b0"
    outlines [(1, "#02050a", 0, 1)]

# --- monitor ---

style mm_monitor_title is gui_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 16
    color "#f2fbff"
    outlines [(2, "#02050a", 0, 1)]

style mm_monitor_foot is gui_text:
    font gui.interface_font
    size 12
    color "#5f97a8"
    outlines [(1, "#02050a", 0, 1)]

# Channel codes stay in the UI font for the same reason the big slot number
# does: SF Automaton's 1 is a bare vertical bar, so "CH.01" reads as "CH.0I".
style mm_monitor_code is mm_monitor_title:
    font gui.interface_font
    size 15

# The big slot number is set in the UI font, NOT the display face: SF Automaton
# draws a 1 as a bare vertical bar, which makes "01" read as "0I".
style mm_channel_number is gui_text:
    font gui.interface_font
    size 68
    color "#173b4d"
    outlines [(1, "#56d7ff44", 0, 0)]

style mm_channel_name is gui_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 38
    color "#f2fbff"
    outlines [(2, "#02050a", 0, 1), (1, "#56d7ff88", 0, 0)]

style mm_channel_strap is gui_text:
    font gui.interface_font
    size 14
    color "#9fc9d6"
    line_spacing 4
    outlines [(1, "#02050a", 0, 1)]

# --- telemetry ---

style mm_telemetry_text is gui_text:
    font gui.interface_font
    size 13
    color "#9fc9d6"
    outlines [(1, "#02050a", 0, 1)]

style mm_telemetry_accent is mm_telemetry_text:
    color "#ff315b"

style mm_readout_key is gui_text:
    font gui.interface_font
    size 12
    color "#4e8195"
    outlines [(1, "#02050a", 0, 1)]

style mm_readout_value is gui_text:
    font gui.interface_font
    size 13
    color "#cfe9f2"
    outlines [(1, "#02050a", 0, 1)]

style mm_footer_text is gui_text:
    font gui.interface_font
    size 13
    color "#5f8b9a"
    outlines [(1, "#02050a", 0, 1)]

# --- channel cards ---
# Everything that has to react to the pointer does so through a style, because
# style prefixes recurse into a button's whole subtree while transform events
# do not.

# The button itself draws NOTHING. It is a lift taller than the card face and
# sits with its top edge inside the marker band, so a background on it would
# paint over the rail line the card is reaching up to join.
style mm_card_button is gui_button:
    background None
    hover_background None
    padding (0, 0, 0, 0)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

# The plate graphic IS the card now; its bezel does the job the 3px accent bar
# and the 2px lip used to split between them, so both are gone. Nothing swaps
# here on hover -- a second plate cutting in at full opacity would snap, and
# the lift transform already brightens this one on a curve.
style mm_card_plate is empty:
    background MM_PLATE

# The plate's own face is far lighter than the flat "#071019" card these three
# were picked against, so the values that read as "quiet" on the old face read
# as "gone" on this one -- the caret in particular was #2f5262 sitting on a
# #1a3a58 gradient, the same luminance as its background. Lifted until each
# clears the plate, and no further: the label is still the loud thing on a card.
style mm_card_pip is empty:
    background "#5d94ab"
    hover_background "#ff315b"

style mm_card_slot is gui_text:
    font gui.interface_font
    size 11
    color "#86b9cd"
    hover_color "#ff8ba6"
    outlines [(1, "#02050a", 0, 1)]

style mm_card_label is gui_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 17
    color "#eaf8ff"
    hover_color "#ff315b"
    text_align 0.5
    outlines [(2, "#02050a", 0, 1)]
    hover_outlines [(2, "#02050a", 0, 1), (1, "#ff315b99", 0, 0)]

style mm_card_caret is gui_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 15
    color "#6fa6bd"
    hover_color "#ff315b"
    outlines [(1, "#02050a", 0, 1)]

# Inherited by the version stamp on the Settings screen.
style main_menu_version is gui_text:
    font gui.interface_font
    color "#9bb0b8"
    size 16
    outlines [(1, "#02050a", 0, 1)]


# --- Console chrome helpers -------------------------------------------------
# Retro-terminal technical dressing (Steins;Gate-inspired) reused across the
# pause-menu screens. It's our own SIGNAL/LINK/0x4D readout language, not lifted.

# WHY THERE ARE TWO OF THESE, AND WHICH ONE TO REACH FOR
#
#   `enter_m_brackets(w, h, ...)` returns ONE displayable and is declared pure,
#   so a call with constant arguments is folded at screen-prepare time and the
#   result is reused forever. `use console_brackets(...)` builds eight `add`
#   nodes and, because SL2 cannot see constants across a `use` boundary
#   (SLUse.prepare takes the constness of the TARGET screen's body, and that
#   body reads its own parameters), all eight are re-executed on every screen
#   execution -- which means every hover, every timer, every slider drag.
#
#   Measured on the main menu, which had five bracket frames: forty of its 112
#   non-constant nodes were these. Prefer the function anywhere the rectangle
#   is fixed; keep the screen for a rect that genuinely moves.
#
# The function takes a SIZE and is placed by the caller, rather than taking a
# rect, so that the same brackets can be positioned with ordinary xpos/ypos.
init python:

    @renpy.pure
    def enter_m_brackets(w, h, col="#56d7ff7a", blen=20, th=2):
        def bar(bw, bh, x, y):
            return Solid(col, xysize=(bw, bh), xpos=x, ypos=y)

        return Fixed(
            bar(blen, th, 0, 0),                        # top-left
            bar(th, blen, 0, 0),
            bar(blen, th, w - blen, 0),                 # top-right
            bar(th, blen, w - th, 0),
            bar(blen, th, 0, h - th),                   # bottom-left
            bar(th, blen, 0, h - blen),
            bar(blen, th, w - blen, h - th),            # bottom-right
            bar(th, blen, w - th, h - blen),
            xysize=(w, h),
        )

    # One labelled row of the telemetry stack, and one line of the controls
    # legend. Same story as the brackets: these were `use` screens taking their
    # geometry as parameters, so five readout rows and four legend rows came to
    # thirty-one nodes rebuilt on every execution. `_` is in Ren'Py's own pure
    # set, so `_("FEED")` folds too -- and because the memo key is the
    # ALREADY-TRANSLATED string, changing language yields a different constant
    # rather than a stale one.
    #
    # Built as a `fixed` with explicit xpos rather than as an hbox, because a
    # box given an xsize spreads its children instead of packing them and the
    # value column comes out crooked.
    @renpy.pure
    def enter_m_readout_row(rkey, rvalue, rwidth):
        return Fixed(
            Text(rkey, style="mm_readout_key", xpos=0, ypos=0),
            Text(rvalue, style="mm_readout_value", xpos=rwidth, xanchor=1.0, ypos=0),
            xysize=(rwidth, 20),
        )

    @renpy.pure
    def enter_m_legend_row(cap, what):
        return Fixed(
            Window(Text(cap, style="mm_keycap_text"), style="mm_keycap", xpos=0, ypos=0),
            Text(what, style="mm_legend_text", xpos=78, ypos=4),
            xysize=(240, 24),
        )


# Four L-shaped corner brackets framing an arbitrary rect. Drawn with thin Solids
# so it costs nothing and scales to any panel without a bespoke border asset.
#
# Prefer `enter_m_brackets()` above for a rect that does not move; see the note
# there. This stays for the screens whose rect is computed from live state.
screen console_brackets(bx, by, bw, bh, col="#56d7ff7a", blen=20, th=2):
    # top-left
    add Solid(col) xysize (blen, th) pos (bx, by)
    add Solid(col) xysize (th, blen) pos (bx, by)
    # top-right
    add Solid(col) xysize (blen, th) pos (bx + bw - blen, by)
    add Solid(col) xysize (th, blen) pos (bx + bw - th, by)
    # bottom-left
    add Solid(col) xysize (blen, th) pos (bx, by + bh - th)
    add Solid(col) xysize (th, blen) pos (bx, by + bh - blen)
    # bottom-right
    add Solid(col) xysize (blen, th) pos (bx + bw - blen, by + bh - th)
    add Solid(col) xysize (th, blen) pos (bx + bw - th, by + bh - blen)

# Slow heartbeat for status indicator dots.
transform console_blink:
    alpha 1.0
    block:
        easeout 0.75 alpha 0.25
        easein 0.75 alpha 1.0
        repeat

screen game_menu_m():
    add gui.game_menu_background
    add Solid("#02050add")
    timer 0.3 action Hide("game_menu_m")

screen game_menu(title, scroll=None, current_screen="menu"):

    # About, Calendar, and any future standard game-menu consumer inherit the
    # domestic shell here. Arcade and Archive never use this helper and keep
    # their authored interfaces. The shell's content aperture is the same
    # 836x520 box the terminal frame exposed, so existing transclusions retain
    # their measured layout.
    use room_menu_shell(title, current_screen):

        if scroll == "viewport":

            viewport:
                style_prefix "room_game_menu_sv"
                xysize (836, 520)
                scrollbars "vertical"
                mousewheel True
                draggable True
                yinitial 0.0
                side_yfill True

                vbox:
                    xsize 810
                    transclude

        elif scroll == "vpgrid":

            vpgrid:
                style_prefix "room_game_menu_sv"
                cols 1
                xysize (836, 520)
                yinitial 0.0
                scrollbars "vertical"
                mousewheel True
                draggable True
                side_yfill True
                transclude

        else:

            transclude

style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    xpos 44
    ypos 42
    xsize 1192
    ysize 636
    padding (0, 0, 0, 0)
    background None

style game_menu_navigation_frame:
    xsize 272
    ysize 636
    padding (24, 28, 20, 24)
    background "#05090fee"

style game_menu_content_frame:
    xsize 904
    ysize 636
    padding (34, 84, 34, 32)
    background "#071019e8"

style game_menu_viewport:
    xsize 828

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 10

style game_menu_label:
    xpos 348
    ypos 62
    xsize 830
    ysize 58

style game_menu_label_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 36
    color "#f2fbff"
    outlines [(2, "#02050a", 0, 1), (1, "#56d7ff88", 0, 0)]
    yalign 0.5

style return_button:
    xsize 246
    ysize 42

style game_menu_nav_title is gui_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 24
    color "#f2fbff"
    outlines [(2, "#02050a", 0, 1), (1, "#56d7ff88", 0, 0)]

style game_menu_nav_subtitle is gui_text:
    font gui.interface_font
    size 11
    color "#6f8c9a"
    kerning 1.5
    outlines [(1, "#02050a", 0, 1)]

style game_menu_nav_footer is gui_text:
    font gui.interface_font
    size 10
    color "#5d7886"
    kerning 1.0
    yalign 0.5
    outlines [(1, "#02050a", 0, 1)]

style game_menu_subtitle is gui_text:
    xpos 350
    ypos 104
    font gui.interface_font
    size 11
    color "#7895a3"
    kerning 1.5
    outlines [(1, "#02050a", 0, 1)]

style game_menu_badge is empty:
    xpos 1216
    xanchor 1.0
    ypos 58
    padding (12, 7, 12, 7)
    background "#102b3ae6"

style game_menu_badge_text is gui_text:
    font gui.interface_font
    size 12
    color "#bfeeff"
    outlines [(1, "#02050a", 0, 1)]

style game_menu_footer is hbox:
    xpos 350
    ypos 650

style game_menu_footer_text is gui_text:
    font gui.interface_font
    size 9
    color "#58727f"
    kerning 1.0
    yalign 0.5

screen about():

    tag menu

    use game_menu(_("About"), scroll="viewport", current_screen="about"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            if gui.about:

                text "[gui.about!t]\n"

            text _("Made with Matsu'Py, built on {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")

style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    font gui.default_font
    size 24
    color ROOM_MENU_INK
    outlines [(2, "#05090db8", 0, 1)]

style about_text:
    font gui.default_font
    size 16
    color ROOM_MENU_PAPER
    line_spacing 4
    outlines [(1, "#05090daa", 0, 1)]

# -----------------------------------------------------------------------------
# SAVE / LOAD  --  moved out to game/data_bank.rpy
# -----------------------------------------------------------------------------
# `screen save`, `screen load`, `screen file_slots` and the page/slot styles
# that dressed them used to live here. They are gone: both doors now open the
# RECORD BANK, one screen that restores, writes, copies, re-labels and erases
# saves off a single list, and both old screen names survive there as thin
# shims onto it. Read the header of data_bank.rpy for the why.
#
# The two styles below stay behind because they are the only part of the old
# file menu the bank still uses -- `bank_locked` borrows them, so the panel the
# boss fight puts up is lettered exactly as it always was.

style locked_file_menu_text is gui_text
style locked_file_menu_hint is gui_text

style locked_file_menu_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 24
    color "#eaf8ff"
    outlines [(2, "#02050a", 0, 1), (1, "#56d7ff88", 0, 0)]

style locked_file_menu_hint:
    font gui.interface_font
    size 18
    color "#9bb0b8"
    outlines [(1, "#02050a", 0, 1)]

# =============================================================================
# SETTINGS  --  the configuration index
# =============================================================================
# WHY THIS IS AN ACCORDION AND NOT FOUR PANELS IN TWO COLUMNS
#   Settings had grown to four fixed panels stacked two-by-two, which meant
#   everything was on screen at once, in a reading order nobody could guess:
#   the frame-rate slider and the textbox opacity slider sat in the same panel
#   because they were both "display", and finding the skip toggles meant reading
#   the whole page. It is now ONE centred column of six collapsible sections --
#   DISPLAY, GRAPHICS, AUDIO, TEXT, GAME, ASSIST -- so the screen opens as an
#   index you read rather than a wall you scan.
#
# THE WIDTH IS THE LAYOUT
#   The column is 620 wide (588 inside the panel padding) and every control row
#   is sized to fill it exactly: two buttons at 289 + 10, three at 189 + 10,
#   four presets at 141 + 8, sliders at 588. That is why the button widths live
#   in styles rather than on the rows -- change the column width and those five
#   numbers are the whole job. `pref_wide_slider` is NOT one of them: the boss
#   fight's pause menu borrows it, so the accordion has its own
#   `pref_full_slider` and leaves that one at 360.
#
# IT IS AN ACCORDION: AT MOST ONE SECTION IS OPEN, AND SETTINGS ALWAYS OPENS
# SHUT. Opening a section closes whichever one was open, and arriving on the
# screen -- from the main menu or from the pause menu, first visit or fiftieth
# -- collapses everything. The column is 520px tall and several sections are
# taller than that on their own, so anything that could leave two of them open
# put the one you came for below the fold behind a scrollbar.
#
# The open section is still parked in `persistent` even though it no longer
# survives a visit. That is not a leftover: it is the one store both contexts
# can write without ceremony -- Settings is reachable from the main menu, where
# there is no rollback, and from a live game, where a plain store variable
# would go into the rollback log and the save file for something that is
# thrown away on the next `show` anyway.

init python:

    ENTER_M_PREF_SECTIONS = ("display", "graphics", "audio", "text", "game", "assist")

    def enter_m_pref_section_toggle(key):
        """
        Open one section and close every other one. Re-clicking the open
        section shuts it, so the screen can be put back to all-closed without
        hunting for a separate control.

        Stored as a SET of one rather than a bare key so that a profile written
        by the old multi-open version still loads: any stale set, list or None
        collapses to a single key the first time a header is clicked.
        """

        already_open = key in (persistent.enter_m_pref_open or ())
        persistent.enter_m_pref_open = set() if already_open else {key}
        renpy.restart_interaction()

    def enter_m_pref_sections_close():
        """Collapse everything. Called on every arrival at the screen."""
        persistent.enter_m_pref_open = set()
        renpy.restart_interaction()

    def enter_m_pref_section_is_open(key):
        return key in (persistent.enter_m_pref_open or ())

    def enter_m_restore_default_preferences():
        _preferences.fullscreen = False
        _preferences.desktop_rollback_side = "disable"
        _preferences.mobile_rollback_side = "disable"
        _preferences.skip_unseen = False
        _preferences.skip_after_choices = False
        _preferences.afm_enable = False
        _preferences.afm_after_click = False
        _preferences.text_cps = 50
        _preferences.afm_time = 15
        _preferences.transitions = 2
        persistent.textbox_opacity = 1.0
        autofocus_set_dim_mode("darken")
        persistent.enter_m_atmos_quality = "full"
        persistent.enter_m_panels = True
        stage_panels_refresh()
        atmos_refresh()

        for mixer, volume in (("main", 1.0), ("music", 1.0), ("sfx", 1.0), ("voice", 1.0)):
            _preferences.set_volume(mixer, volume)
            _preferences.set_mute(mixer, False)

        renpy.restart_interaction()

    def enter_m_max_volume():
        for mixer in ("main", "music", "sfx", "voice"):
            _preferences.set_volume(mixer, 1.0)
            _preferences.set_mute(mixer, False)

        renpy.restart_interaction()

default persistent.enter_m_pref_open = set()

transform pref_panel_enter(delay=0.0):
    alpha 0.0
    yoffset 14
    pause delay
    easeout 0.18 alpha 1.0 yoffset 0

# The body of a section that has just been opened. It is a NEW displayable
# every time the section is toggled, so this plays on every open -- and is left
# holding its end state through the screen rebuilds a slider drag causes.
transform pref_body_open:
    subpixel True
    alpha 0.0
    yoffset -8
    easeout 0.16 alpha 1.0 yoffset 0

transform pref_button_hover:
    subpixel True
    on show:
        xoffset 0
    on hover:
        easeout 0.10 xoffset 6
    on idle:
        easeout 0.14 xoffset 0


# One collapsible section. The caller supplies the body as a transcluded block,
# and it is only built when the section is open -- a closed section costs
# nothing but its header.
screen pref_section(pref_key, pref_title, pref_accent="#56d7ff", pref_delay=0.0):

    $ _pref_open = enter_m_pref_section_is_open(pref_key)

    frame:
        style "room_pref_panel"
        at pref_panel_enter(pref_delay)

        # Spacing 0 and a header that spans the WHOLE panel: give the panel its
        # own padding instead and a closed section shows a plate behind its
        # header that is wider than the header, which reads as a misalignment
        # rather than as a heading. The body brings the padding with it.
        vbox:
            spacing 0

            button:
                style "room_pref_section_button"
                action Function(enter_m_pref_section_toggle, pref_key)

                # This `fixed` is the button's ONLY child on purpose -- the same
                # rule the main-menu rail obeys. Hover and idle transform events
                # reach a button's direct child and stop there.
                fixed:
                    xysize (568, 28)

                    add Solid(pref_accent) xysize (4, 22) xpos 0 ypos 3
                    text pref_title:
                        style "room_pref_section_title"
                        xpos 14
                        ypos 0

                    # The open/closed tell: a minus that grows a stroke when the
                    # section is shut. Drawn out of Solids rather than set as a
                    # caret glyph because every triangle in the three fonts this
                    # game ships is tofu.
                    add Solid(pref_accent) xysize (14, 2) xpos 550 ypos 13
                    if not _pref_open:
                        add Solid(pref_accent) xysize (2, 14) xpos 556 ypos 7

            if _pref_open:
                frame:
                    style "room_pref_section_body"
                    at pref_body_open

                    vbox:
                        spacing 10
                        transclude


screen preferences():
    tag menu

    # Always arrive collapsed. Both events are needed: "show" covers opening
    # Settings over a menu that is not itself tagged `menu`, "replace" covers
    # the usual case of it taking the tag from the screen it replaces.
    on "show" action Function(enter_m_pref_sections_close)
    on "replace" action Function(enter_m_pref_sections_close)

    use room_menu_shell(_("Settings"), "preferences"):

        viewport:
            # 620px belongs to the controls, not to the scrollbar side. Give
            # Ren'Py a separate 8px bar plus a 12px gutter so the right edge of
            # a section never sits underneath the side container when a tall
            # accordion panel activates scrolling.
            style_prefix "room_pref_sv"
            xsize 640
            ysize 520
            xalign 0.5
            yalign 0.5
            scrollbars "vertical"
            mousewheel True
            draggable False
            side_yfill True

            vbox:
                spacing 14

                # --- the index bar --------------------------------------
                # "Expand All" was removed when this became an accordion: a
                # button whose entire job is to open every section at once
                # cannot coexist with a rule that at most one may be open.
                # "Collapse All" survives because shutting the open one from
                # here still saves aiming at its header.
                #
                # It stops 14px short of the column's right edge: the vertical
                # scrollbar lands flush against it the moment a section opens
                # far enough to need one, and a button pressed up against the
                # scrollbar reads as clipped.
                fixed:
                    xysize (620, 30)
                    at pref_panel_enter(0.00)

                    text _("CONFIGURATION INDEX"):
                        style "room_pref_index_label"
                        xpos 2
                        ypos 7

                    textbutton _("Collapse All"):
                        style "room_pref_index_button"
                        xpos 490
                        ypos 1
                        action Function(enter_m_pref_sections_close)

                # --- DISPLAY: the window and what the hardware is doing --
                use pref_section("display", _("Display"), ROOM_MENU_TEAL, 0.03):

                    if renpy.variant("pc"):
                        hbox:
                            style "room_pref_button_row"
                            textbutton _("Window") style "room_pref_radio_button" action Preference("display", "window")
                            textbutton _("Fullscreen") style "room_pref_radio_button" action Preference("display", "fullscreen")

                    # THE FRAME RATE CAP AND THE VSYNC PICKER USED TO LIVE HERE
                    # and are gone (Aug 27 2026). The game runs at the display's
                    # refresh rate; framerate.rpy has the measurements for why a
                    # cap was actively harmful in the real-time modes. Nothing
                    # replaced them, because there is nothing left to choose.
                    #
                    # The meter stays, developer-only: it is how a "the frame
                    # rate feels wrong" report gets turned into a number. The
                    # timer forces the redraws that make this read the ceiling
                    # rather than the idle floor.
                    if config.developer:
                        timer 1.0 repeat True action Function(enter_m_fps_sample)
                        $ _enter_m_fps_now = enter_m_fps_measured()
                        $ _enter_m_hz = enter_m_refresh_rate_label()
                        text _("measured: [_enter_m_fps_now!t] fps  //  display: [_enter_m_hz!t]") style "room_pref_note_label"

                # --- GRAPHICS: what the picture costs -------------------
                use pref_section("graphics", _("Graphics"), ROOM_MENU_CORAL, 0.06):

                    text _("Scene Transitions") style "room_pref_row_label"
                    hbox:
                        style "room_pref_button_row"
                        textbutton _("Full") style "room_pref_radio_button" action Preference("transitions", "all") selected (_preferences.transitions == 2)
                        textbutton _("Off") style "room_pref_radio_button" action Preference("transitions", "none") selected (_preferences.transitions == 0)

                    text _("Atmosphere") style "room_pref_row_label"
                    hbox:
                        style "room_pref_button_row"
                        textbutton _("Full") style "room_pref_small_button" action [SetField(persistent, "enter_m_atmos_quality", "full"), Function(atmos_refresh)] selected (persistent.enter_m_atmos_quality == "full")
                        textbutton _("Light") style "room_pref_small_button" action [SetField(persistent, "enter_m_atmos_quality", "light"), Function(atmos_refresh)] selected (persistent.enter_m_atmos_quality == "light")
                        textbutton _("Off") style "room_pref_small_button" action [SetField(persistent, "enter_m_atmos_quality", "off"), Function(atmos_refresh)] selected (persistent.enter_m_atmos_quality == "off")

                    text _("Story Panels") style "room_pref_row_label"
                    hbox:
                        style "room_pref_button_row"
                        textbutton _("On") style "room_pref_radio_button" action Function(stage_panels_set_enabled, True) selected persistent.enter_m_panels
                        textbutton _("Off") style "room_pref_radio_button" action Function(stage_panels_set_enabled, False) selected (not persistent.enter_m_panels)

                    # The boss fights only. Every stop still draws every
                    # effect; what changes is the internal resolution the
                    # procedural layers are rendered at before being scaled to
                    # the frame. Sprites, text and UI are never touched. See
                    # addons/Matsuda's Sick Boss Fight/perf.rpy.
                    text _("Fight Effects") style "room_pref_row_label"
                    hbox:
                        style "room_pref_button_row"
                        textbutton _("Native") style "room_pref_small_button" action SetField(persistent, "msbf_gfx", "ultra") selected (msbf_gfx_level() == "ultra")
                        textbutton _("720p") style "room_pref_small_button" action SetField(persistent, "msbf_gfx", "high") selected (msbf_gfx_level() == "high")
                        textbutton _("Fast") style "room_pref_small_button" action SetField(persistent, "msbf_gfx", "performance") selected (msbf_gfx_level() == "performance")

                    text _("Textbox Opacity") style "room_pref_row_label"
                    bar value FieldValue(persistent, "textbox_opacity", range=1.0, max_is_zero=False, style="slider") style "room_pref_full_slider"

                # --- AUDIO ----------------------------------------------
                use pref_section("audio", _("Audio"), ROOM_MENU_OCHRE, 0.09):

                    if config.has_music:
                        text _("Music Volume") style "room_pref_row_label"
                        bar value Preference("music volume") style "room_pref_full_slider"

                    if config.has_sound:
                        text _("Sound Volume") style "room_pref_row_label"
                        hbox:
                            style "room_pref_audio_row"
                            bar value Preference("sound volume") style ("room_pref_full_audio_slider" if config.sample_sound else "room_pref_full_slider")

                            if config.sample_sound:
                                textbutton _("Test") style "room_pref_test_button" action Play("sound", config.sample_sound)

                    if config.has_voice:
                        text _("Voice Volume") style "room_pref_row_label"
                        hbox:
                            style "room_pref_audio_row"
                            bar value Preference("voice volume") style ("room_pref_full_audio_slider" if config.sample_voice else "room_pref_full_slider")

                            if config.sample_voice:
                                textbutton _("Test") style "room_pref_test_button" action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        hbox:
                            style "room_pref_button_row"
                            textbutton _("Mute All") style "room_pref_check_button" action Preference("all mute", "toggle")
                            textbutton _("Max Volume") style "room_pref_action_button" action Function(enter_m_max_volume)

                # --- TEXT: the speed the prose arrives at ---------------
                use pref_section("text", _("Text"), ROOM_MENU_LAVENDER, 0.12):

                    text _("Text Speed") style "room_pref_row_label"
                    bar value FieldValue(_preferences, "text_cps", range=180, max_is_zero=False, style="slider", offset=20) style "room_pref_full_slider"

                    hbox:
                        style "room_pref_preset_row"
                        textbutton _("Slow") style "room_pref_preset_button" action SetField(_preferences, "text_cps", 20) selected (_preferences.text_cps == 20)
                        textbutton _("Normal") style "room_pref_preset_button" action SetField(_preferences, "text_cps", 60) selected (_preferences.text_cps == 60)
                        textbutton _("Fast") style "room_pref_preset_button" action SetField(_preferences, "text_cps", 120) selected (_preferences.text_cps == 120)
                        textbutton _("Instant") style "room_pref_preset_button" action SetField(_preferences, "text_cps", 0) selected (_preferences.text_cps == 0)

                    hbox:
                        style "room_pref_button_row"
                        textbutton _("Auto Mode") style "room_pref_check_button" action Preference("auto-forward", "toggle")
                        textbutton _("After Click") style "room_pref_check_button" action Preference("auto-forward after click", "toggle")

                    text _("Auto-Forward Delay") style "room_pref_row_label"
                    bar value Preference("auto-forward time") style "room_pref_full_slider"

                # --- GAME: how far the player is allowed to jump --------
                use pref_section("game", _("Game"), ROOM_MENU_CORAL, 0.15):

                    text _("Skip") style "room_pref_row_label"
                    hbox:
                        style "room_pref_button_row"
                        textbutton _("Unseen Text") style "room_pref_check_button" action Preference("skip", "toggle")
                        textbutton _("After Choices") style "room_pref_check_button" action Preference("after choices", "toggle")

                    if config.developer:
                        text _("Rollback Edge") style "room_pref_row_label"
                        hbox:
                            style "room_pref_button_row"
                            textbutton _("Off") style "room_pref_small_button" action Preference("rollback side", "disable")
                            textbutton _("Left") style "room_pref_small_button" action Preference("rollback side", "left")
                            textbutton _("Right") style "room_pref_small_button" action Preference("rollback side", "right")

                # --- ASSIST ---------------------------------------------
                use pref_section("assist", _("Assist"), ROOM_MENU_TEAL, 0.18):

                    hbox:
                        style "room_pref_button_row"
                        textbutton _("Cursor Assist") style "room_pref_check_button" action Preference("automatic move", "toggle")
                        textbutton _("Audio Focus") style "room_pref_check_button" action Preference("emphasize audio", "toggle")

                    text _("Speaker Focus") style "room_pref_row_label"
                    hbox:
                        style "room_pref_button_row"
                        textbutton _("None") style "room_pref_small_button" action Function(autofocus_set_dim_mode, "none") selected (persistent.autofocus_dim_mode == "none")
                        textbutton _("Opaque") style "room_pref_small_button" action Function(autofocus_set_dim_mode, "opaque") selected (persistent.autofocus_dim_mode == "opaque")
                        textbutton _("Darken") style "room_pref_small_button" action Function(autofocus_set_dim_mode, "darken") selected (persistent.autofocus_dim_mode == "darken")

                # --- the footer, which never collapses ------------------
                vbox:
                    spacing 10
                    at pref_panel_enter(0.21)

                    add Solid("#d6a3543d") xysize (620, 1)

                    textbutton _("Reset to Defaults"):
                        style "room_pref_reset_button"
                        action Function(enter_m_restore_default_preferences)

style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text
style pref_panel is empty
style pref_section_body is empty
style pref_section_button is button
style pref_section_title is gui_text
style pref_index_label is gui_text
style pref_row_label is gui_text
style pref_note_label is pref_row_label
style pref_button_row is hbox
style pref_audio_row is hbox
style pref_small_button is radio_button
style pref_small_button_text is radio_button_text
style pref_action_button is radio_button
style pref_action_button_text is radio_button_text
style pref_test_button is slider_button
style pref_test_button_text is slider_button_text
style pref_wide_slider is slider_slider
style pref_audio_slider is slider_slider

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 2

style pref_label_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 24
    color "#f2fbff"
    outlines [(2, "#02050a", 0, 1), (1, "#56d7ff88", 0, 0)]
    yalign 1.0

style pref_vbox:
    xsize 246

style pref_panel:
    xsize 620
    background "#071019df"

style pref_section_body:
    xsize 620
    padding (16, 12, 16, 14)

# The whole header is the toggle, so it gets a plate of its own rather than the
# 6px slide the controls use -- a full-width bar that slides reads as a glitch.
style pref_section_button:
    xsize 620
    ysize 42
    padding (16, 7, 16, 7)
    background "#0e2130df"
    hover_background "#1d4058f2"
    selected_background "#0e2130df"
    selected_hover_background "#1d4058f2"
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style pref_section_title:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 22
    color "#f2fbff"
    outlines [(2, "#02050a", 0, 1), (1, "#56d7ff88", 0, 0)]

style pref_index_label:
    font gui.interface_font
    size 14
    color "#7f97a4"
    outlines [(1, "#02050a", 0, 1)]

style pref_row_label:
    font gui.interface_font
    size 17
    color "#d4e8f1"
    outlines [(1, "#02050a", 0, 1)]
    top_margin 2

style pref_note_label:
    size 14
    color "#8fa6b2"
    top_margin 1

style pref_button_row:
    spacing 10

style pref_audio_row:
    spacing 10
    yalign 0.5

style radio_vbox:
    spacing gui.pref_button_spacing

# The idle plate sits ON the panel plate, so it has to be lighter than it --
# at 289 wide an unselected option with the old #071019cc background read as
# floating text rather than as the other half of a pair.
style radio_button:
    properties gui.button_properties("radio_button")
    xsize 289
    ysize 34
    padding (12, 4, 12, 5)
    background "#0e2130df"
    hover_background "#2a1020f2"
    selected_background "#12314af2"
    selected_hover_background "#321223f2"
    insensitive_background "#03070baa"
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style radio_button_text:
    properties gui.button_text_properties("radio_button")
    font gui.interface_font
    size 18
    color "#b8c7cf"
    hover_color "#ff315b"
    selected_color "#8bd7ff"
    selected_hover_color "#ff315b"
    outlines [(1, "#02050a", 0, 1)]
    hover_outlines [(1, "#02050a", 0, 1), (1, "#ff315b88", 0, 0)]
    selected_outlines [(1, "#02050a", 0, 1), (1, "#56d7ff88", 0, 0)]
    selected_hover_outlines [(1, "#02050a", 0, 1), (1, "#ff315b99", 0, 0)]

# The three widths the 588-wide column is cut into: two across, three across,
# and (below) four presets across. Change the column and change these.
style pref_small_button:
    xsize 189

style pref_action_button:
    xsize 289

style pref_index_button is radio_button:
    xsize 116
    ysize 28
    padding (8, 3, 8, 4)

style pref_index_button_text is radio_button_text:
    size 15

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    xsize 289
    ysize 34
    padding (12, 4, 12, 5)
    background "#0e2130df"
    hover_background "#2a1020f2"
    selected_background "#12314af2"
    selected_hover_background "#321223f2"
    insensitive_background "#03070baa"
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style check_button_text:
    properties gui.button_text_properties("check_button")
    font gui.interface_font
    size 18
    color "#b8c7cf"
    hover_color "#ff315b"
    selected_color "#8bd7ff"
    selected_hover_color "#ff315b"
    outlines [(1, "#02050a", 0, 1)]
    hover_outlines [(1, "#02050a", 0, 1), (1, "#ff315b88", 0, 0)]
    selected_outlines [(1, "#02050a", 0, 1), (1, "#56d7ff88", 0, 0)]
    selected_hover_outlines [(1, "#02050a", 0, 1), (1, "#ff315b99", 0, 0)]

style slider_slider:
    xsize 330
    ysize 10

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 10

style slider_button_text:
    properties gui.button_text_properties("slider_button")
    color "#b8c7cf"
    hover_color "#ff315b"
    outlines [(1, "#02050a", 0, 1)]

# NOT for the accordion. The boss fight's pause menu borrows this one for its
# own 700-wide audio panel, so it stays where it was; the Settings column uses
# pref_full_slider below.
style pref_wide_slider:
    xsize 360

style pref_audio_slider:
    xsize 286

style pref_full_slider:
    xsize 588

style pref_full_audio_slider:
    xsize 514

style pref_test_button:
    xsize 64
    ysize 34
    left_margin 0
    padding (8, 4, 8, 5)
    background "#071019cc"
    hover_background "#2a1020f2"
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style pref_test_button_text:
    size 16
    color "#b8c7cf"
    hover_color "#ff315b"
    outlines [(1, "#02050a", 0, 1)]

style pref_preset_row is hbox:
    spacing 8
    top_margin 2

style pref_preset_button is radio_button:
    xsize 141
    padding (6, 4, 6, 5)

style pref_preset_button_text is radio_button_text:
    size 15

style pref_reset_button is radio_button:
    xsize 620
    background "#13212ecc"
    hover_background "#321223f2"
    selected_background "#13212ecc"

style pref_reset_button_text is radio_button_text:
    size 17
    color "#d4e8f1"

style slider_vbox:
    xsize 400










screen history():
    tag menu
    predict False

    $ history_count = len(_history_list)
    $ history_count_text = _("{count} ENTRIES").format(count=history_count)

    use room_menu_shell(_("History"), "history"):

        fixed:
            xysize (836, 520)

            vbox:
                xalign 0.5
                spacing 8

                fixed:
                    style "history_header"
                    xalign 0.5

                    vbox:
                        spacing 1

                        text _("SESSION TRANSCRIPT"):
                            style "history_title"

                        text _("DIALOGUE, NARRATION, AND THE ORDER THEY ARRIVED"):
                            style "history_subtitle"

                    frame:
                        style "history_count_badge"
                        xalign 1.0
                        yalign 0.5

                        hbox:
                            spacing 8

                            add Solid(ROOM_MENU_OCHRE):
                                xysize (6, 6)
                                yalign 0.5

                            text history_count_text:
                                style "history_count_text"

                fixed:
                    xsize 812
                    ysize 2
                    xalign 0.5

                    add Solid("#e8dbc536") xysize (812, 1) ypos 1
                    add Solid(ROOM_MENU_TEAL) xysize (92, 2)
                    add Solid(ROOM_MENU_CORAL) xysize (48, 2) xpos 96

                viewport:
                    id "history_viewport"
                    style "history_viewport"
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    yinitial 1.0
                    side_yfill True

                    vbox:
                        style "history_list"

                        if _history_list:
                            for history_index, h in enumerate(_history_list):
                                $ history_entry_number = "{:03d}".format(history_index + 1)

                                # Spoken lines and narration are the same
                                # entry with four things swapped, so the
                                # differences are resolved up front rather
                                # than duplicating the whole entry layout.
                                $ history_named = bool(h.who)
                                $ history_entry_color = h.who_args.get("color", ROOM_MENU_TEAL) if history_named else "#718b88"
                                $ history_label_color = history_entry_color if history_named else ROOM_MENU_MUTED
                                $ history_speaker_style = "history_speaker" if history_named else "history_narrator"
                                $ history_body_style = "history_dialogue" if history_named else "history_narration_text"

                                frame:
                                    style "history_entry_rail"
                                    background Solid(history_entry_color)

                                    frame:
                                        style ("history_entry" if history_named else "history_entry_narration")

                                        vbox:
                                            style "history_entry_body"

                                            fixed:
                                                xsize 776
                                                ysize 25

                                                text (h.who if history_named else _("NARRATION")):
                                                    style history_speaker_style
                                                    color history_label_color
                                                    substitute False

                                                text history_entry_number:
                                                    style "history_entry_number"
                                                    xalign 1.0

                                            text h.what:
                                                style history_body_style
                                                substitute False

                        else:
                            frame:
                                style "history_empty"

                                vbox:
                                    xalign 0.5
                                    yalign 0.5
                                    spacing 8

                                    text _("Nothing here yet."):
                                        style "history_empty_title"
                                        xalign 0.5

                                    text _("Dialogue will be kept here as you play."):
                                        style "history_empty_text"
                                        xalign 0.5

                fixed:
                    style "history_footer"
                    xalign 0.5

                    text _("MOUSE WHEEL / DRAG  •  REVIEW"):
                        style "history_footer_text"

                    text _("ESC / RMB  •  RETURN"):
                        style "history_footer_text"
                        xpos 720
                        xanchor 1.0


style history_outer_frame is game_menu_outer_frame
style history_content_frame is empty
style history_header is fixed
style history_viewport is gui_viewport
style history_vscrollbar is gui_vscrollbar
style history_side is gui_side
style history_list is vbox
style history_entry_rail is empty
style history_entry is empty
style history_entry_narration is history_entry
style history_entry_body is vbox
style history_count_badge is empty
style history_footer is fixed
style history_empty is empty

style history_content_frame:
    xsize 904
    ysize 636
    padding (30, 20, 22, 18)
    background ROOM_MENU_PANEL

style history_header:
    xsize 812
    ysize 44

style history_title is gui_text:
    font gui.default_font
    size 22
    color ROOM_MENU_INK
    outlines [(2, "#05090db8", 0, 1)]

style history_subtitle is gui_text:
    font gui.interface_font
    size 9
    color ROOM_MENU_MUTED
    kerning 1.1
    outlines [(1, "#05090d99", 0, 1)]

style history_count_badge:
    padding (12, 6, 12, 6)
    background ROOM_MENU_SELECTOR_IDLE

style history_count_text is gui_text:
    font gui.interface_font
    size 10
    color ROOM_MENU_PAPER
    kerning 0.8
    outlines [(1, "#05090d99", 0, 1)]

style history_viewport:
    xsize 836
    ysize 424

style history_vscrollbar:
    xsize 8
    base_bar Frame(Solid("#172126b8"), 0, 0, 0, 0)
    thumb Frame(Solid(ROOM_MENU_TEAL + "d8"), 2, 2, 2, 2)
    unscrollable "hide"

style history_side:
    spacing 12

style history_list:
    xsize 812
    spacing 8
    padding (0, 4, 0, 4)

style history_entry_rail:
    xsize 812
    padding (4, 0, 0, 0)

style history_entry:
    xsize 808
    padding (16, 11, 16, 12)
    background ROOM_MENU_SELECTOR_IDLE

style history_entry_narration:
    background "#0c1619d6"

style history_entry_body:
    xsize 776
    spacing 5

style history_speaker is gui_text:
    font gui.default_font
    size 18
    outlines [(1, "#05090db8", 0, 1)]

style history_narrator is gui_text:
    font gui.interface_font
    size 11
    color ROOM_MENU_MUTED
    kerning 1.2
    outlines [(1, "#05090d99", 0, 1)]

style history_entry_number is gui_text:
    font gui.interface_font
    size 10
    color "#718b88"
    yalign 0.5

style history_dialogue is gui_text:
    font gui.default_font
    size 18
    color ROOM_MENU_PAPER
    xsize 776
    line_spacing 3
    outlines [(1, "#05090d99", 0, 1)]

style history_narration_text is history_dialogue:
    color ROOM_MENU_MUTED
    italic True

style history_footer:
    xsize 812
    ysize 16

style history_footer_text is gui_text:
    font gui.interface_font
    size 9
    color "#718b88"
    kerning 0.8

style history_empty:
    xsize 812
    ysize 400
    background ROOM_MENU_SELECTOR_IDLE

style history_empty_title is gui_text:
    font gui.default_font
    size 22
    color ROOM_MENU_PAPER
    outlines [(1, "#05090db8", 0, 1)]

style history_empty_text is gui_text:
    font gui.interface_font
    size 13
    color ROOM_MENU_MUTED
    outlines [(1, "#05090d99", 0, 1)]












































































































































































screen name_input(message, ok_action):


    modal True

    zorder 200

    style_prefix "confirm"

    add Solid("#02050ad9")
    key "K_RETURN" action [Play("sound", gui.activate_sound), ok_action]

    frame:

        has vbox:
            xalign .5
            yalign .5
            spacing 22

        text "// ENTER-M  IDENTITY INPUT":
            style "confirm_tag"
            xalign 0.5

        add Solid("#56d7ff4a") xysize (360, 2) xalign 0.5

        label _(message):
            style "confirm_prompt"
            xalign 0.5

        input default "" value VariableInputValue("player") length 12 allow "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"






        hbox:
            xalign 0.5
            spacing 100

            textbutton _("OK") action ok_action

screen dialog(message, ok_action):


    modal True

    zorder 200

    style_prefix "confirm"

    add Solid("#02050ad9")

    frame:

        has vbox:
            xalign .5
            yalign .5
            spacing 22

        text "// ENTER-M  SYSTEM NOTICE":
            style "confirm_tag"
            xalign 0.5

        add Solid("#56d7ff4a") xysize (360, 2) xalign 0.5

        label _(message):
            style "confirm_prompt"
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("OK") action ok_action

screen confirm(message, yes_action, no_action):


    modal True

    zorder 200

    style_prefix "room_confirm"

    key "game_menu" action no_action

    add Solid("#031015bd")
    add Solid("#d6a3540b")

    frame:

        has vbox:
            xalign .5
            yalign .5
            spacing 18

        add "assets/gui/logo.png":
            xysize (54, 54)
            xalign 0.5

        text _("A MOMENT TO BE SURE"):
            style "room_confirm_tag"
            xalign 0.5

        fixed:
            xysize (520, 2)
            xalign 0.5

            add Solid(ROOM_MENU_TEAL) xysize (240, 2)
            add Solid(ROOM_MENU_CORAL) xysize (160, 2) xpos 240
            add Solid(ROOM_MENU_OCHRE) xysize (120, 2) xpos 400

        text _(message):
            style "room_confirm_prompt_text"
            xsize 600
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 14

            textbutton _("Yes"):
                style "room_confirm_yes_button"
                text_style "room_confirm_yes_button_text"
                action yes_action

            textbutton _("No"):
                style "room_confirm_no_button"
                text_style "room_confirm_no_button_text"
                action no_action
                default_focus True





style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text
style confirm_tag is gui_text

style confirm_frame:
    background "#06101bf5"
    padding (46, 34, 46, 36)
    xalign .5
    yalign .5
    xmaximum 880

style confirm_tag:
    font gui.interface_font
    size 11
    color "#56d7ff"
    kerning 2.0
    text_align 0.5
    outlines [(1, "#02050a", 0, 1)]

style confirm_prompt_text:
    font gui.interface_font
    color "#eaf8ff"
    size 22
    text_align 0.5
    layout "subtitle"
    outlines [(1, "#02050a", 0, 1)]

style confirm_button:
    xsize 172
    ysize 44
    padding (14, 6, 14, 7)
    background "#071019dd"
    hover_background "#2a1020f2"
    insensitive_background "#03070baa"
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style confirm_button_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 20
    color "#eaf8ff"
    hover_color "#ff315b"
    insensitive_color "#7b8795"
    selected_color "#8bd7ff"
    outlines [(2, "#02050a", 0, 1)]
    hover_outlines [(2, "#02050a", 0, 1), (1, "#ff315b99", 0, 0)]
    xalign 0.5
    yalign 0.5
    text_align 0.5


# The room-family confirmation is deliberately isolated from ``name_input``
# and ``dialog``, which still use the legacy ``confirm_*`` style namespace.
style room_confirm_frame is empty
style room_confirm_prompt is gui_prompt
style room_confirm_prompt_text is gui_prompt_text
style room_confirm_button is gui_medium_button
style room_confirm_button_text is gui_medium_button_text
style room_confirm_tag is gui_text

style room_confirm_frame:
    xsize 680
    padding (40, 30, 40, 34)
    xalign 0.5
    yalign 0.5
    background ROOM_MENU_PANEL

style room_confirm_tag:
    font gui.interface_font
    size 10
    color ROOM_MENU_OCHRE
    kerning 1.4
    text_align 0.5
    outlines [(1, "#05090d99", 0, 1)]

style room_confirm_prompt:
    xsize 600

style room_confirm_prompt_text:
    font gui.default_font
    color ROOM_MENU_INK
    size 21
    xsize 600
    xalign 0.5
    text_align 0.5
    layout "subtitle"
    outlines [(2, "#05090db8", 0, 1)]

style room_confirm_button:
    xsize 250
    ysize 46
    padding (14, 7, 14, 8)
    background ROOM_MENU_SELECTOR_IDLE
    hover_background ROOM_MENU_SELECTOR_HOVER
    insensitive_background ROOM_MENU_SELECTOR_IDLE
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style room_confirm_yes_button is room_confirm_button:
    background ROOM_MENU_SELECTOR_DANGER
    hover_background ROOM_MENU_SELECTOR_YES_HOVER
    selected_hover_background ROOM_MENU_SELECTOR_YES_HOVER

style room_confirm_yes_button_text is room_confirm_button_text:
    hover_color "#fffdf5"
    hover_outlines [(2, "#ff9d87cc", 0, 0), (1, "#05090db8", 0, 1)]

style room_confirm_no_button is room_confirm_button:
    background ROOM_MENU_SELECTOR_SELECTED
    hover_background ROOM_MENU_SELECTOR_NO_HOVER
    selected_hover_background ROOM_MENU_SELECTOR_NO_HOVER

style room_confirm_no_button_text is room_confirm_button_text:
    hover_color "#fffdf5"
    hover_outlines [(2, "#70bbb3cc", 0, 0), (1, "#05090db8", 0, 1)]

style room_confirm_button_text:
    font gui.default_font
    size 18
    color ROOM_MENU_PAPER
    hover_color "#fff8ea"
    insensitive_color "#71807e"
    outlines [(1, "#05090db8", 0, 1)]
    xalign 0.5
    yalign 0.5
    text_align 0.5








screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        has hbox:
            spacing 6

        text _("Skipping")

        text ">" at delayed_blink(0.0, 1.0) style "skip_triangle"
        text ">" at delayed_blink(0.2, 1.0) style "skip_triangle"
        text ">" at delayed_blink(0.4, 1.0) style "skip_triangle"



transform delayed_blink(delay, cycle):
    alpha .5

    pause delay
    block:

        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Solid("#05090fed")
    padding gui.skip_frame_borders.padding

style skip_text:
    color "#d6e6ee"
    size gui.notify_text_size

style skip_triangle:
    color "#ff315b"
    font gui.interface_font









screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text message

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Solid("#05090fed")
    padding gui.notify_frame_borders.padding

style notify_text:
    color "#d6e6ee"
    size gui.notify_text_size
