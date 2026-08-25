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
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 30
    color "#ff4968"
    xalign 0.5
    text_align 0.5
    outlines [(2, "#02040b", 0, 0), (1, "#ffffff66", 1, 1)]

# Logo-splash "system boot" chrome (see enter_m_splash_intro in splash.rpy).
style splash_boot_caption is gui_text:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 19
    color "#bfeeff"
    text_align 0.5
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff66", 0, 0)]

style splash_boot_micro is gui_text:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
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
    background Frame("mod_assets/gui/frame.png", gui.frame_borders, tile=gui.frame_tile)

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
        return Transform("mod_assets/gui/textbox.png", alpha=a, xalign=0.5, yalign=1.0), None

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

    background Frame("mod_assets/gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
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
    "gui/ctc.png"
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
            textbutton _("Phone") action Show("phone_contacts_screen")
            textbutton _("People") action Show("character_thoughts_screen")
            textbutton _("Settings") action ShowMenu('preferences')

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

        if nav_main:

            textbutton _("New Game") action Start()

        else:

            textbutton _("History") action [ShowMenu("history"), SensitiveIf(renpy.get_screen("history") == None)]
            # Custom Calendar button
            textbutton _("Calendar") action ShowMenu("calendar_menu") sensitive renpy.get_screen("calendar_menu") == None

            textbutton _("Save Game") action ShowMenu("save") sensitive (not _msbf_save_load_locked and renpy.get_screen("save") == None)

        textbutton _("Load Game") action ShowMenu("load") sensitive (not _msbf_save_load_locked and renpy.get_screen("load") == None)

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
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 19
    color "#eaf8ff"
    hover_color "#ff315b"
    selected_color "#8bd7ff"
    insensitive_color "#7b8795"
    outlines [(2, "#02050a", 0, 1)]
    hover_outlines [(2, "#02050a", 0, 1), (1, "#ff315b99", 0, 0)]
    insensitive_outlines [(1, "#02050a", 0, 1)]
    hover_xoffset 8

# -----------------------------------------------------------------------------
# MAIN MENU -- "the main terminal", laid out as a BROADCAST DESK rather than as
# the visual-novel column of buttons it used to be.
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
transform mm_rail_scan:
    subpixel True
    ypos 110
    alpha 0.0
    pause 0.7
    block:
        alpha 0.0
        ypos 110
        linear 0.18 alpha 1.0
        linear 2.4 ypos 448
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

# A channel card. `on show` staggers it up off the rail; `on hover` / `on idle`
# lift it toward the monitor. Both focus handlers restate EVERY property the
# other animates -- including alpha, which only `on show` would otherwise set --
# because a handler that fires mid-entrance strands whatever it omits.
#
# THE LIFT IS A MEASUREMENT, NOT A TASTE. -11 is exactly the gap between the
# rail's marker line and the top of a card: the marker is 3px at
# mm_rail_line_y (486) and the cards sit at mm_rail_y (500), so a hovered card
# rising 11px puts its own accent bar at 489 -- the pixel the marker ends on.
# The two become one continuous 6px band, which is the whole gesture: the
# selected channel reaches up and joins the rail feeding the monitor.
#
# WHICH IS WHY THERE IS NO `zoom` HERE. A scale on this transform is anchored
# at the card's top-left, so it grew the card RIGHTWARD: at 1.035 the 142px
# card became 147px while the marker above it stayed 142px, and the accent
# overhung the marker by 5px on the right (measured: marker x 493-634, accent
# x 493-639). It also ate half the 10px gap to the next card, so the rail's
# spacing went uneven on hover. The lift alone carries the pop; the colour
# swap in the styles carries the rest. Keep every card exactly one slot wide.
transform mm_card_face(delay=0.0):
    subpixel True
    on show:
        alpha 0.0
        yoffset 30
        pause delay
        parallel:
            easeout 0.34 alpha 1.0
        parallel:
            easeout_cubic 0.42 yoffset 0
    on hover:
        easeout_cubic 0.14 alpha 1.0 yoffset -11
    on idle:
        easeout_cubic 0.20 alpha 1.0 yoffset 0

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


# The step wedge on the stage monitor's test card: light to dark, warm white
# through to the panel's own blue-black, so the monitor always has something
# calibrated-looking on it even when no channel is selected.
define MM_TEST_WEDGE = [
    "#eaf8ff", "#cfe9f4", "#b3d9ea", "#97c9e0", "#7cb9d6", "#61a8cc", "#4d97c0",
    "#3d85ad", "#31739a", "#276187", "#1e5074", "#173f60", "#11304d", "#0c223a",
]


# --- Reusable pieces of the desk --------------------------------------------

# One labelled row of the telemetry stack. Built as a `fixed` with explicit
# xpos rather than as an hbox, because a box given an xsize spreads its
# children instead of packing them and the value column comes out crooked.
screen mm_readout_row(rkey, rvalue, rwidth, rx, ry):
    fixed:
        xysize (rwidth, 20)
        xpos rx
        ypos ry
        text rkey:
            style "mm_readout_key"
            xpos 0
        text rvalue:
            style "mm_readout_value"
            xanchor 1.0
            xpos rwidth

# One line of the controls legend: a keycap chip and what it does.
screen mm_legend_row(cap, what, lx, ly):
    fixed:
        xysize (240, 24)
        xpos lx
        ypos ly
        frame:
            style "mm_keycap"
            xpos 0
            text cap style "mm_keycap_text"
        text what:
            style "mm_legend_text"
            xpos 78
            ypos 4


screen main_menu():

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
            (_("Load Game"), _("RESUME A SAVED RECORDING."),          ShowMenu("load")),
            (_("Arcade"),    _("CABINET FLOOR. NO STORY ATTACHED."),  ShowMenu("arcade_hub")),
            (_("Archive"),   _("EVERYTHING THE TERMINAL HAS KEPT."),  ShowMenu("archive")),
            (_("Credits"),   _("WHO IS RESPONSIBLE FOR ALL THIS."),   ShowMenu("credits_menu")),
            (_("Donate"),    _("PUT A COIN IN THE SLOT."),            OpenURL("https://ko-fi.com/l4w1i3t")),
            (_("Settings"),  _("TUNE THE SET UNTIL IT LOOKS RIGHT."), ShowMenu("preferences")),
            (_("Quit"),      _("CUT THE FEED."),                      Quit(confirm=False)),
        ]

        # Rail geometry. The row is centred as a whole, so adding or removing a
        # channel re-spaces everything without another number having to move.
        mm_count = len(mm_channels)
        mm_card_w, mm_card_h, mm_card_gap = 142, 130, 10
        mm_rail_w = mm_count * mm_card_w + (mm_count - 1) * mm_card_gap
        mm_rail_x = (1280 - mm_rail_w) // 2
        mm_rail_y = 500
        mm_rail_line_y = 486

        # The stage monitor's box has ONE home; everything drawn on the glass is
        # placed relative to these four numbers.
        mm_mx, mm_my, mm_mw, mm_mh = 324, 108, 620, 356

        # The previewed channel, clamped in case the table ever shrinks under a
        # stale selection.
        mm_cur = min(mm_sel, mm_count - 1)
        mm_label, mm_strap, mm_action = mm_channels[mm_cur]
        mm_cur_x = mm_rail_x + mm_cur * (mm_card_w + mm_card_gap)

    # --- background field ---
    add "menu_bg"
    add Solid("#02050ad2")
    add "vignette":
        alpha 0.55
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
        use console_brackets(44, 186, 236, 66, "#ff315b66", 14, 2)

    fixed:
        at mm_panel_in(0.38, -40, 0)

        text "CONTROLS":
            style "mm_section_label"
            xpos 44
            ypos 300
        add Solid("#56d7ff33") xysize (236, 1) xpos 44 ypos 320

        use mm_legend_row(_("< >"), _("BROWSE CHANNELS"), 44, 334)
        use mm_legend_row(_("ENTER"), _("OPEN CHANNEL"), 44, 368)
        use mm_legend_row(_("CLICK"), _("SELECT CHANNEL"), 44, 402)
        use mm_legend_row(_("ESC"), _("CUT THE FEED"), 44, 436)

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

        for mm_i, mm_shade in enumerate(MM_TEST_WEDGE):
            add Solid(mm_shade) xysize (18, 82) xpos (mm_mx + 30 + mm_i * 22) ypos (mm_my + 198)

        add Solid("#56d7ff26") xysize (1, 94) xpos (mm_mx + 366) ypos (mm_my + 192)
        add "mod_assets/gui/logo.png":
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

        use console_brackets(mm_mx, mm_my, mm_mw, mm_mh, "#56d7ff7a", 22, 2)

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

        $ mm_sig = [0.0, 0.18, 0.36, 0.06, 0.28, 0.10, 0.22, 0.40, 0.14]
        for mm_j in range(len(mm_sig)):
            add Solid("#56d7ff") xysize (16, 40) xpos (988 + mm_j * 26) ypos 214 yanchor 1.0 at mm_eq_bar(mm_sig[mm_j], 0.62 + 0.04 * mm_j, 0.18)

        add Solid("#ff315b") xysize (6, 6) xpos 984 ypos 230 at console_blink
        text "LINK STABLE":
            style "mm_telemetry_accent"
            xpos 1000
            ypos 225
        use console_brackets(968, 108, 268, 150, "#56d7ff6e", 18, 2)

        # --- readout panel ---
        add Solid("#070f1af2") xpos 968 ypos 272 xysize (268, 192)
        add Solid("#12324a") xpos 968 ypos 272 xysize (268, 26)
        add Solid("#56d7ff") xpos 968 ypos 298 xysize (268, 2)
        add Solid("#56d7ff") xysize (6, 6) xpos 984 ypos 282 at console_blink
        text "TERMINAL // 0x4D":
            style "mm_monitor_title"
            xpos 1000
            ypos 276

        use mm_readout_row(_("FEED"), _("MAIN"), 236, 984, 316)
        use mm_readout_row(_("BUILD"), "v[config.version]", 236, 984, 344)
        use mm_readout_row(_("CHANNELS"), ("%02d" % mm_count), 236, 984, 372)
        use mm_readout_row(_("SELECTED"), ("%02d" % (mm_cur + 1)), 236, 984, 400)
        use mm_readout_row(_("STATUS"), _("NOMINAL"), 236, 984, 428)

        use console_brackets(968, 272, 268, 192, "#56d7ff6e", 18, 2)

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

        button:
            style "mm_card_button"
            xysize (mm_card_w, mm_card_h)
            xpos (mm_rail_x + mm_k * (mm_card_w + mm_card_gap))
            ypos mm_rail_y
            action mm_k_action
            hovered SetScreenVariable("mm_sel", mm_k)
            default_focus (mm_k == 0)

            # This `fixed` is the button's ONLY child on purpose: hover and idle
            # transform events reach a button's direct child and stop there, so
            # anything nested deeper would never learn it was being pointed at.
            # Colour changes go through styles instead, which DO recurse.
            fixed:
                at mm_card_face(0.16 + 0.035 * mm_k)
                xysize (mm_card_w, mm_card_h)

                frame:
                    style "mm_card_accent"
                    xysize (mm_card_w, 3)
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
                frame:
                    style "mm_card_lip"
                    xysize (mm_card_w, 2)
                    ypos (mm_card_h - 2)

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

    use console_brackets(14, 14, 1252, 692, "#56d7ff3a", 26, 2)

    key "K_ESCAPE" action Quit(confirm=False)


# --- Main-menu styles -------------------------------------------------------

style mm_micro is gui_text:
    font gui.interface_font
    size 12
    color "#6fb6c9"
    outlines [(1, "#02050a", 0, 1)]

style mm_title is gui_text:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
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
    font "mod_assets/fonts/SF Automaton Extended.ttf"
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
    font "mod_assets/fonts/SF Automaton Extended.ttf"
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
    font "mod_assets/fonts/SF Automaton Extended.ttf"
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

style mm_card_button is gui_button:
    background "#071019e0"
    hover_background "#22091af2"
    padding (0, 0, 0, 0)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style mm_card_accent is empty:
    background "#56d7ff"
    hover_background "#ff315b"

style mm_card_pip is empty:
    background "#2a5c70"
    hover_background "#ff315b"

style mm_card_lip is empty:
    background "#123243"
    hover_background "#ff315b"

style mm_card_slot is gui_text:
    font gui.interface_font
    size 11
    color "#4e8195"
    hover_color "#ff8ba6"
    outlines [(1, "#02050a", 0, 1)]

style mm_card_label is gui_text:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 17
    color "#eaf8ff"
    hover_color "#ff315b"
    text_align 0.5
    outlines [(2, "#02050a", 0, 1)]
    hover_outlines [(2, "#02050a", 0, 1), (1, "#ff315b99", 0, 0)]

style mm_card_caret is gui_text:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 15
    color "#2f5262"
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

# Four L-shaped corner brackets framing an arbitrary rect. Drawn with thin Solids
# so it costs nothing and scales to any panel without a bespoke border asset.
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
    add "game_menu_bg"
    add Solid("#02050add")
    timer 0.3 action Hide("game_menu_m")

screen game_menu(title, scroll=None):

    if main_menu:

        add gui.main_menu_background

    else:

        key "mouseup_3" action Return()
        add gui.game_menu_background

    add Solid("#02050acc")
    add Solid("#56d7ff1c") xysize (1280, 2) at menu_scanline_slow

    style_prefix "game_menu"

    frame:
        style "game_menu_outer_frame"
        at menu_panel_enter(0.0, -28, 0)

        hbox:
            spacing 16

            frame:
                style "game_menu_navigation_frame"

                vbox:
                    xfill True
                    spacing 12

                    text "ENTER-M":
                        style "game_menu_nav_title"

                    text "TERMINAL LS":
                        style "game_menu_nav_subtitle"

                    null height 1
                    add Solid("#56d7ff3a") xysize (224, 2)
                    null height 1

                    use navigation(main_menu, embedded=True)

                    null height 8

                    textbutton _("Return"):
                        style "return_button"
                        action Return()

                    null height 4

                    hbox:
                        spacing 7
                        add Solid("#ff315b") xysize (5, 5) yalign 0.5 at console_blink
                        text "CONNECTION STABLE":
                            style "game_menu_nav_footer"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        yinitial 1.0
                        side_yfill True
                        has vbox
                        transclude

                elif scroll == "vpgrid":

                    vpgrid:

                        cols 1
                        yinitial 1.0
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        side_yfill True
                        transclude

                else:

                    transclude

    # --- Console chrome layered over the content panel ----------------------
    use console_brackets(332, 42, 904, 636, "#56d7ff7a", 22, 2)

    label title

    text "ENTER-M // SYSTEM CONSOLE":
        style "game_menu_subtitle"

    add Solid("#56d7ff2e") xysize (868, 2) xpos 348 ypos 118

    frame:
        style "game_menu_badge"

        hbox:
            spacing 8
            add Solid("#56d7ff") xysize (6, 6) yalign 0.5 at console_blink
            text "LINK 0x4D // STABLE":
                style "game_menu_badge_text"

    hbox:
        style "game_menu_footer"
        spacing 7
        add Solid("#345a6b") xysize (5, 5) yalign 0.5
        text "ENTER-M.SYS  ::  STATUS NOMINAL":
            style "game_menu_footer_text"

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")

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
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 36
    color "#f2fbff"
    outlines [(2, "#02050a", 0, 1), (1, "#56d7ff88", 0, 0)]
    yalign 0.5

style return_button:
    xsize 246
    ysize 42

style game_menu_nav_title is gui_text:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
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

    use game_menu(_("About"), scroll="viewport"):

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
    size gui.label_text_size

screen save():

    tag menu
    if msbf_save_load_locked() and not main_menu:
        use locked_file_menu(_("Save"), _("Saving is unavailable during Matsuda's boss fight."))
    else:
        use file_slots(_("Save"))


screen load():

    tag menu
    if msbf_save_load_locked() and not main_menu:
        use locked_file_menu(_("Load"), _("Loading is unavailable during Matsuda's boss fight."))
    else:
        use file_slots(_("Load"))

screen locked_file_menu(title, message):
    use game_menu(title):
        frame:
            xalign 0.5
            yalign 0.5
            xsize 650
            ysize 150
            background Solid("#050811e8")
            padding (24, 22)

            vbox:
                spacing 12
                text message style "locked_file_menu_text":
                    xalign 0.5
                    text_align 0.5
                text _("Finish or leave the battle before using save files.") style "locked_file_menu_hint":
                    xalign 0.5
                    text_align 0.5

init python:
    def FileActionMod(name, page=None, **kwargs):
        if msbf_save_load_locked():
            return NullAction()
        return FileAction(name)


screen file_slots(title):

    default page_name_value = FilePageNameInputValue()

    use game_menu(title):

        fixed:

            order_reverse True

            button:
                style "page_label"


                xalign 0.5


                input:
                    style "page_label_text"
                    value page_name_value


            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileActionMod(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)


            hbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                spacing gui.page_spacing








                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)




style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text
style locked_file_menu_text is gui_text
style locked_file_menu_hint is gui_text

style page_label:
    xpadding 50
    ypadding 3

style page_label_text:
    color "#f2fbff"
    outlines [(1, "#02050a", 0, 1)]
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")
    background "#071019cc"
    hover_background "#2a1020f2"
    selected_background "#183447f2"

style page_button_text:
    properties gui.button_text_properties("page_button")
    color "#b8c7cf"
    hover_color "#ff315b"
    selected_color "#8bd7ff"
    outlines [(1, "#02050a", 0, 1)]

style slot_button:
    properties gui.button_properties("slot_button")
    background "#071019dd"
    hover_background "#2a1020f2"
    selected_background "#183447f2"
    insensitive_background "#03070baa"

style slot_button_text:
    properties gui.button_text_properties("slot_button")
    color "#b8c7cf"
    hover_color "#ff315b"
    selected_color "#8bd7ff"
    outlines [(1, "#02050a", 0, 1)]

style locked_file_menu_text:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
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
# WHICH SECTIONS ARE OPEN is a per-profile preference, not screen state, so it
# survives leaving Settings and closing the game. DISPLAY starts open so the
# screen never opens empty.

init python:

    ENTER_M_PREF_SECTIONS = ("display", "graphics", "audio", "text", "game", "assist")

    def enter_m_pref_section_toggle(key):
        """
        Open or close one section.

        Rebuilds the set and REASSIGNS it rather than mutating in place: an
        attribute assignment is what tells `persistent` it has changed, and
        rebuilding also quietly repairs a profile whose stored value is a stale
        list, a None, or a set full of section keys that no longer exist.
        """

        open_keys = set(persistent.enter_m_pref_open or ())
        open_keys &= set(ENTER_M_PREF_SECTIONS)

        if key in open_keys:
            open_keys.discard(key)
        else:
            open_keys.add(key)

        persistent.enter_m_pref_open = open_keys
        renpy.restart_interaction()

    def enter_m_pref_sections_set(open_all):
        persistent.enter_m_pref_open = set(ENTER_M_PREF_SECTIONS) if open_all else set()
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

default persistent.enter_m_pref_open = set(["display"])

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
        style "pref_panel"
        at pref_panel_enter(pref_delay)

        # Spacing 0 and a header that spans the WHOLE panel: give the panel its
        # own padding instead and a closed section shows a plate behind its
        # header that is wider than the header, which reads as a misalignment
        # rather than as a heading. The body brings the padding with it.
        vbox:
            spacing 0

            button:
                style "pref_section_button"
                action Function(enter_m_pref_section_toggle, pref_key)

                # This `fixed` is the button's ONLY child on purpose -- the same
                # rule the main-menu rail obeys. Hover and idle transform events
                # reach a button's direct child and stop there.
                fixed:
                    xysize (568, 28)

                    add Solid(pref_accent) xysize (4, 22) xpos 0 ypos 3
                    text pref_title:
                        style "pref_section_title"
                        xpos 14
                        ypos 0

                    # The open/closed tell: a minus that grows a stroke when the
                    # section is shut. Drawn out of Solids rather than set as a
                    # caret glyph because every triangle in the three fonts this
                    # game ships is tofu.
                    add Solid("#8bd7ff") xysize (14, 2) xpos 550 ypos 13
                    if not _pref_open:
                        add Solid("#8bd7ff") xysize (2, 14) xpos 556 ypos 7

            if _pref_open:
                frame:
                    style "pref_section_body"
                    at pref_body_open

                    vbox:
                        spacing 10
                        transclude


screen preferences():
    tag menu

    use game_menu(_("Settings")):

        viewport:
            xsize 620
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
                # The two buttons stop 14px short of the column's right edge:
                # the vertical scrollbar lands flush against it the moment a
                # section opens far enough to need one, and a button pressed up
                # against the scrollbar reads as clipped.
                fixed:
                    xysize (620, 30)
                    at pref_panel_enter(0.00)

                    text _("CONFIGURATION INDEX"):
                        style "pref_index_label"
                        xpos 2
                        ypos 7

                    textbutton _("Expand All"):
                        style "pref_index_button"
                        xpos 366
                        ypos 1
                        action Function(enter_m_pref_sections_set, True)
                        at pref_button_hover

                    textbutton _("Collapse All"):
                        style "pref_index_button"
                        xpos 490
                        ypos 1
                        action Function(enter_m_pref_sections_set, False)
                        at pref_button_hover

                # --- DISPLAY: the window and what the hardware is doing --
                use pref_section("display", _("Display"), "#56d7ff", 0.03):

                    if renpy.variant("pc"):
                        hbox:
                            style "pref_button_row"
                            textbutton _("Window") style "radio_button" action Preference("display", "window") at pref_button_hover
                            textbutton _("Fullscreen") style "radio_button" action Preference("display", "fullscreen") at pref_button_hover

                    # The slider walks the divisors of the monitor's refresh
                    # rate -- the only rates Matsu'Py's swap interval can
                    # produce. See framerate.rpy.
                    $ _enter_m_fps_readout = enter_m_fps_label()
                    text _("Frame Rate — [_enter_m_fps_readout!t]") style "pref_row_label"
                    bar value EnterMFramerateValue() style "pref_full_slider"
                    if enter_m_vsync_mode() == "off":
                        text _("VSync is off — the cap does nothing.") style "pref_note_label"
                    elif enter_m_fps_needs_restart():
                        text _("Restart to apply.") style "pref_note_label"

                    # Dev-only readout, so the cap can be confirmed rather than
                    # guessed at. The timer forces the redraws that make this
                    # measure the ceiling.
                    if config.developer:
                        timer 1.0 repeat True action Function(enter_m_fps_sample)
                        $ _enter_m_fps_now = enter_m_fps_measured()
                        text _("measured: [_enter_m_fps_now!t] fps") style "pref_note_label"

                    text _("VSync") style "pref_row_label"
                    hbox:
                        style "pref_button_row"
                        textbutton _("On") style "pref_small_button" action SetField(persistent, "enter_m_vsync", "on") selected (enter_m_vsync_mode() == "on") at pref_button_hover
                        textbutton _("Adaptive") style "pref_small_button" action SetField(persistent, "enter_m_vsync", "adaptive") selected (enter_m_vsync_mode() == "adaptive") at pref_button_hover
                        textbutton _("Off") style "pref_small_button" action SetField(persistent, "enter_m_vsync", "off") selected (enter_m_vsync_mode() == "off") at pref_button_hover
                    if enter_m_vsync_needs_restart():
                        text _("Restart to apply.") style "pref_note_label"

                # --- GRAPHICS: what the picture costs -------------------
                use pref_section("graphics", _("Graphics"), "#56d7ff", 0.06):

                    text _("Scene Transitions") style "pref_row_label"
                    hbox:
                        style "pref_button_row"
                        textbutton _("Full") style "radio_button" action Preference("transitions", "all") selected (_preferences.transitions == 2) at pref_button_hover
                        textbutton _("Off") style "radio_button" action Preference("transitions", "none") selected (_preferences.transitions == 0) at pref_button_hover

                    text _("Atmosphere") style "pref_row_label"
                    hbox:
                        style "pref_button_row"
                        textbutton _("Full") style "pref_small_button" action [SetField(persistent, "enter_m_atmos_quality", "full"), Function(atmos_refresh)] selected (persistent.enter_m_atmos_quality == "full") at pref_button_hover
                        textbutton _("Light") style "pref_small_button" action [SetField(persistent, "enter_m_atmos_quality", "light"), Function(atmos_refresh)] selected (persistent.enter_m_atmos_quality == "light") at pref_button_hover
                        textbutton _("Off") style "pref_small_button" action [SetField(persistent, "enter_m_atmos_quality", "off"), Function(atmos_refresh)] selected (persistent.enter_m_atmos_quality == "off") at pref_button_hover

                    text _("Story Panels") style "pref_row_label"
                    hbox:
                        style "pref_button_row"
                        textbutton _("On") style "radio_button" action Function(stage_panels_set_enabled, True) selected persistent.enter_m_panels at pref_button_hover
                        textbutton _("Off") style "radio_button" action Function(stage_panels_set_enabled, False) selected (not persistent.enter_m_panels) at pref_button_hover

                    # The boss fights only. Every stop still draws every
                    # effect; what changes is the internal resolution the
                    # procedural layers are rendered at before being scaled to
                    # the frame. Sprites, text and UI are never touched. See
                    # addons/Matsuda's Sick Boss Fight/perf.rpy.
                    text _("Fight Effects") style "pref_row_label"
                    hbox:
                        style "pref_button_row"
                        textbutton _("Native") style "pref_small_button" action SetField(persistent, "msbf_gfx", "ultra") selected (msbf_gfx_level() == "ultra") at pref_button_hover
                        textbutton _("720p") style "pref_small_button" action SetField(persistent, "msbf_gfx", "high") selected (msbf_gfx_level() == "high") at pref_button_hover
                        textbutton _("Fast") style "pref_small_button" action SetField(persistent, "msbf_gfx", "performance") selected (msbf_gfx_level() == "performance") at pref_button_hover

                    text _("Textbox Opacity") style "pref_row_label"
                    bar value FieldValue(persistent, "textbox_opacity", range=1.0, max_is_zero=False, style="slider") style "pref_full_slider"

                # --- AUDIO ----------------------------------------------
                use pref_section("audio", _("Audio"), "#56d7ff", 0.09):

                    if config.has_music:
                        text _("Music Volume") style "pref_row_label"
                        bar value Preference("music volume") style "pref_full_slider"

                    if config.has_sound:
                        text _("Sound Volume") style "pref_row_label"
                        hbox:
                            style "pref_audio_row"
                            bar value Preference("sound volume") style ("pref_full_audio_slider" if config.sample_sound else "pref_full_slider")

                            if config.sample_sound:
                                textbutton _("Test") style "pref_test_button" action Play("sound", config.sample_sound) at pref_button_hover

                    if config.has_voice:
                        text _("Voice Volume") style "pref_row_label"
                        hbox:
                            style "pref_audio_row"
                            bar value Preference("voice volume") style ("pref_full_audio_slider" if config.sample_voice else "pref_full_slider")

                            if config.sample_voice:
                                textbutton _("Test") style "pref_test_button" action Play("voice", config.sample_voice) at pref_button_hover

                    if config.has_music or config.has_sound or config.has_voice:
                        hbox:
                            style "pref_button_row"
                            textbutton _("Mute All") style "mute_all_button" action Preference("all mute", "toggle") at pref_button_hover
                            textbutton _("Max Volume") style "pref_action_button" action Function(enter_m_max_volume) at pref_button_hover

                # --- TEXT: the speed the prose arrives at ---------------
                use pref_section("text", _("Text"), "#ff315b", 0.12):

                    text _("Text Speed") style "pref_row_label"
                    bar value FieldValue(_preferences, "text_cps", range=180, max_is_zero=False, style="slider", offset=20) style "pref_full_slider"

                    hbox:
                        style "pref_preset_row"
                        textbutton _("Slow") style "pref_preset_button" action SetField(_preferences, "text_cps", 20) selected (_preferences.text_cps == 20) at pref_button_hover
                        textbutton _("Normal") style "pref_preset_button" action SetField(_preferences, "text_cps", 60) selected (_preferences.text_cps == 60) at pref_button_hover
                        textbutton _("Fast") style "pref_preset_button" action SetField(_preferences, "text_cps", 120) selected (_preferences.text_cps == 120) at pref_button_hover
                        textbutton _("Instant") style "pref_preset_button" action SetField(_preferences, "text_cps", 0) selected (_preferences.text_cps == 0) at pref_button_hover

                    hbox:
                        style "pref_button_row"
                        textbutton _("Auto Mode") style "check_button" action Preference("auto-forward", "toggle") at pref_button_hover
                        textbutton _("After Click") style "check_button" action Preference("auto-forward after click", "toggle") at pref_button_hover

                    text _("Auto-Forward Delay") style "pref_row_label"
                    bar value Preference("auto-forward time") style "pref_full_slider"

                # --- GAME: how far the player is allowed to jump --------
                use pref_section("game", _("Game"), "#ff315b", 0.15):

                    text _("Skip") style "pref_row_label"
                    hbox:
                        style "pref_button_row"
                        textbutton _("Unseen Text") style "check_button" action Preference("skip", "toggle") at pref_button_hover
                        textbutton _("After Choices") style "check_button" action Preference("after choices", "toggle") at pref_button_hover

                    if config.developer:
                        text _("Rollback Edge") style "pref_row_label"
                        hbox:
                            style "pref_button_row"
                            textbutton _("Off") style "pref_small_button" action Preference("rollback side", "disable") at pref_button_hover
                            textbutton _("Left") style "pref_small_button" action Preference("rollback side", "left") at pref_button_hover
                            textbutton _("Right") style "pref_small_button" action Preference("rollback side", "right") at pref_button_hover

                # --- ASSIST ---------------------------------------------
                use pref_section("assist", _("Assist"), "#56d7ff", 0.18):

                    hbox:
                        style "pref_button_row"
                        textbutton _("Cursor Assist") style "check_button" action Preference("automatic move", "toggle") at pref_button_hover
                        textbutton _("Audio Focus") style "check_button" action Preference("emphasize audio", "toggle") at pref_button_hover

                    text _("Speaker Focus") style "pref_row_label"
                    hbox:
                        style "pref_button_row"
                        textbutton _("None") style "pref_small_button" action Function(autofocus_set_dim_mode, "none") selected (persistent.autofocus_dim_mode == "none") at pref_button_hover
                        textbutton _("Opaque") style "pref_small_button" action Function(autofocus_set_dim_mode, "opaque") selected (persistent.autofocus_dim_mode == "opaque") at pref_button_hover
                        textbutton _("Darken") style "pref_small_button" action Function(autofocus_set_dim_mode, "darken") selected (persistent.autofocus_dim_mode == "darken") at pref_button_hover

                # --- the footer, which never collapses ------------------
                vbox:
                    spacing 10
                    at pref_panel_enter(0.21)

                    add Solid("#56d7ff26") xysize (620, 1)

                    textbutton _("Reset to Defaults"):
                        style "pref_reset_button"
                        action Function(enter_m_restore_default_preferences)
                        at pref_button_hover

    text "v[config.version]":
        xalign 1.0 yalign 1.0
        xoffset -10 yoffset -10
        style "main_menu_version"

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
    font "mod_assets/fonts/SF Automaton Extended.ttf"
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
    font "mod_assets/fonts/SF Automaton Extended.ttf"
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

    if main_menu:
        add gui.main_menu_background
    else:
        key "mouseup_3" action Return()
        add gui.game_menu_background

    add Solid("#02050acc")
    add Solid("#56d7ff1c") xysize (1280, 2) at menu_scanline_slow

    style_prefix "history"

    frame:
        style "history_outer_frame"
        at menu_panel_enter(0.0, -28, 0)

        hbox:
            spacing 16

            frame:
                style "game_menu_navigation_frame"

                vbox:
                    xfill True
                    spacing 14

                    text "ENTER-M":
                        style "game_menu_nav_title"

                    use navigation(main_menu, embedded=True)

                    null height 10

                    textbutton _("Return"):
                        style "return_button"
                        action Return()

            frame:
                style "history_content_frame"

                vbox:
                    spacing 8

                    fixed:
                        style "history_header"

                        vbox:
                            spacing 1

                            text _("HISTORY"):
                                style "history_title"

                            text _("SESSION TRANSCRIPT // ACTIVE MEMORY"):
                                style "history_subtitle"

                        frame:
                            style "history_count_badge"
                            xalign 1.0
                            yalign 0.5

                            hbox:
                                spacing 8

                                add Solid("#56d7ff"):
                                    xysize (6, 6)
                                    yalign 0.5

                                text history_count_text:
                                    style "history_count_text"

                    add Solid("#56d7ff55"):
                        xysize (812, 2)

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
                                    # than by writing the whole 25-line entry
                                    # out twice and keeping the shared header
                                    # geometry in sync by hand.
                                    $ history_named = bool(h.who)
                                    $ history_entry_color = h.who_args.get("color", gui.accent_color) if history_named else "#607d8c"
                                    # The narration label keeps history_narrator's own grey; only a
                                    # named speaker takes their character colour.
                                    $ history_label_color = history_entry_color if history_named else "#8ba4b0"
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
                                                    xsize 777
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

                                        text "NO TRANSCRIPT DATA":
                                            style "history_empty_title"
                                            xalign 0.5

                                        text _("Dialogue will be archived here as you play."):
                                            style "history_empty_text"
                                            xalign 0.5

                    fixed:
                        style "history_footer"

                        text _("MOUSE WHEEL / DRAG  •  REVIEW TRANSCRIPT"):
                            style "history_footer_text"

                        text _("ESC / RMB  •  RETURN"):
                            style "history_footer_text"
                            xalign 1.0

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


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
    background "#071019ed"

style history_header:
    xsize 812
    ysize 56

style history_title is gui_text:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 34
    color "#f2fbff"
    outlines [(2, "#02050a", 0, 1), (1, "#56d7ff88", 0, 0)]

style history_subtitle is gui_text:
    font gui.interface_font
    size 11
    color "#7895a3"
    kerning 1.5

style history_count_badge:
    padding (12, 7, 12, 7)
    background "#102b3ae6"

style history_count_text is gui_text:
    font gui.interface_font
    size 12
    color "#bfeeff"

style history_viewport:
    xsize 834
    ysize 494

style history_vscrollbar:
    unscrollable gui.unscrollable

style history_side:
    spacing 10

style history_list:
    xsize 812
    spacing 8
    padding (0, 4, 0, 4)

style history_entry_rail:
    xsize 812
    padding (3, 0, 0, 0)

style history_entry:
    xsize 809
    padding (16, 11, 16, 12)
    background "#0a1722e8"

style history_entry_narration:
    background "#08131cce"

style history_entry_body:
    xsize 777
    spacing 5

style history_speaker is gui_text:
    font gui.name_font
    size 20
    outlines [(1, "#02050a", 0, 1)]

style history_narrator is gui_text:
    font gui.interface_font
    size 12
    color "#8ba4b0"
    kerning 1.5

style history_entry_number is gui_text:
    font gui.interface_font
    size 10
    color "#4e6875"
    yalign 0.5

style history_dialogue is gui_text:
    font gui.default_font
    size 20
    color "#edf6f7"
    xsize 777
    line_spacing 3
    outlines [(1, "#02050a99", 0, 1)]

style history_narration_text is history_dialogue:
    color "#c8d6d9"
    italic True

style history_footer:
    xsize 812
    ysize 16

style history_footer_text is gui_text:
    font gui.interface_font
    size 9
    color "#58727f"
    kerning 1.0

style history_empty:
    xsize 812
    ysize 460
    background "#08131c99"

style history_empty_title is gui_text:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 24
    color "#76919d"

style history_empty_text is gui_text:
    font gui.interface_font
    size 14
    color "#58727f"












































































































































































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

    style_prefix "confirm"

    add Solid("#02050ad9")

    frame:

        has vbox:
            xalign .5
            yalign .5
            spacing 22

        text "// ENTER-M  SYSTEM QUERY":
            style "confirm_tag"
            xalign 0.5

        add Solid("#56d7ff4a") xysize (360, 2) xalign 0.5

        label _(message):
            style "confirm_prompt"
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 48

            textbutton _("Yes") action yes_action
            textbutton _("No") action no_action





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
    font "mod_assets/fonts/SF Automaton Extended.ttf"
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
