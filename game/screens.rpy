init offset = -1

style default:
    font gui.default_font
    size gui.text_size
    color gui.text_color
    outlines [(1, "#02050acc", 0, 1)]
    line_overlap_split 1
    line_spacing 1

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

# --- Live textbox opacity ---------------------------------------------------
# The dialogue box image is wrapped in a DynamicDisplayable so its alpha tracks
# persistent.textbox_opacity (exposed as a slider in Settings). DynamicDisplayable
# re-reads the persistent value whenever the say screen re-renders, so changing
# the slider takes effect on the very next line without any restart plumbing.
#
# RETURN THE SAME OBJECT UNTIL THE ALPHA CHANGES (Sep 21 2026, profiled).
# DynamicDisplayable calls this on every visit of the displayable tree, not
# once per line -- prediction, focus and per-interact walks all visit it -- and
# it only skips its rebuild when `raw_child != self.raw_child` is False. A fresh
# Transform every call never compares equal, so each visit duplicated the child
# and copied every transform property onto it (Transform.take_state). While
# skipping that was ~1,400 rebuilds a second: take_state was 7.1s of a 30s
# profile window and 41M getattr calls. Caching the last Transform makes the
# comparison an identity hit and the whole rebuild disappears.
default persistent.textbox_opacity = 0.75

init python:
    _enter_m_textbox_bg_last = [None, None]     # [alpha, Transform]
    _enter_m_dialogue_bg_last = [None, None]

    def _enter_m_textbox_bg(st, at, dialogue=False):
        try:
            a = float(persistent.textbox_opacity)
        except (TypeError, ValueError):
            a = 0.75
        a = max(0.0, min(1.0, a))
        # Map slider 0..1 to alpha 0.2..1.0 so the box stays faintly visible at
        # the low end -- the text never floats over a fully transparent panel.
        a = 0.2 + 0.8 * a
        # Keep separate identity caches: generic windows keep their original
        # background, while only the ADV say window uses the new coachwork.
        cached = _enter_m_dialogue_bg_last if dialogue else _enter_m_textbox_bg_last
        if cached[0] != a:
            cached[0] = a
            asset = "assets/gui/dialogue/body.svg" if dialogue else "assets/gui/textbox.png"
            cached[1] = Transform(asset, alpha=a, xalign=0.5, yalign=1.0)
        return cached[1], None

image enter_m_textbox_bg = DynamicDisplayable(_enter_m_textbox_bg)
image enter_m_dialogue_bg = DynamicDisplayable(_enter_m_textbox_bg, dialogue=True)

style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background "enter_m_textbox_bg"

# Do not restyle generic windows: input and custom screens inherit `window`.
# The say screen's style_prefix selects this subclass automatically.
style say_window is window:
    background "enter_m_dialogue_bg"

style namebox:
    xpos 248
    xanchor 0.0
    xminimum gui.namebox_width
    xmaximum 760
    xfill False
    ypos -3
    ysize gui.namebox_height

    background Frame("assets/gui/dialogue/nameplate.svg", 38, 6, 28, 5)
    padding (20, 5, 30, 6)

style say_label:
    color "#e0f0ef"
    font gui.interface_font
    size 22
    xalign 0.0
    yalign 0.5
    outlines [(1, "#08121980", 0, 1)]

style say_dialogue:
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos
    size gui.say_text_size

    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

image ctc:
    xalign 0.81 yalign 0.97 alpha 0.0 subpixel True
    "assets/gui/dialogue/advance.svg"
    block:
        easeout 0.85 alpha 1.0
        easein 0.85 alpha 0.45
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

# The story choice menu (`screen choice`), its styles and its motion live in
# choice_plates.rpy.

define config.narrator_menu = True

screen quick_menu():

    zorder 100

    if quick_menu:

        $ _main_story_scope = enter_m_main_story_active()
        $ _phone_quick_count = phone_notification_count() if _main_story_scope else 0

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
                sensitive _main_story_scope
                id "quick_phone"

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

                            add phone_ui_surface("badge"):
                                xysize (_phone_quick_badge_width, 18)

                            text str(_phone_quick_count) style "phone_badge_text":
                                xalign 0.5
                                yalign 0.5

            textbutton _("People") action Show("character_thoughts_screen") sensitive _main_story_scope
            textbutton _("Settings") action ShowMenu('preferences')

        # Polling is cheap (the current catalog is tiny) and action-driven, so
        # no sound or saved-state mutation happens during screen prediction.
        # The Function action must stay void: a False/True result would end the
        # active say interaction and make dialogue advance without Auto enabled.
        if _main_story_scope:
            timer 0.5 repeat True action Function(phone_notification_poll_action, _update_screens=False)

default quick_menu = True

# Quick-menu tabs, cut like the choice plates and the date badge. Three-slice
# in x, drawn at the source's
# own 26px height so the cut angle never changes. Selected is Auto-forward
# reading as lit; the state is a plain style swap, never a transform, so a
# tab can never move out from under the cursor.
define QUICK_TAB_IDLE = Frame("assets/gui/hud/quick_idle.png", 26, 0, 14, 0)
define QUICK_TAB_HOVER = Frame("assets/gui/hud/quick_hover.png", 26, 0, 14, 0)
define QUICK_TAB_SELECTED = Frame("assets/gui/hud/quick_selected.png", 26, 0, 14, 0)
define QUICK_TAB_INSENSITIVE = Frame("assets/gui/hud/quick_insensitive.png", 26, 0, 14, 0)

style quick_button:
    properties gui.button_properties("quick_button")
    xsize 96
    ysize 26
    background QUICK_TAB_IDLE
    hover_background QUICK_TAB_HOVER
    selected_background QUICK_TAB_SELECTED
    selected_hover_background QUICK_TAB_HOVER
    insensitive_background QUICK_TAB_INSENSITIVE
    selected_insensitive_background QUICK_TAB_INSENSITIVE
    padding (14, 2, 10, 3)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style quick_button_text:
    properties gui.button_text_properties("quick_button")
    font gui.interface_font
    size 12
    color "#d6e6ee"
    hover_color "#fff6f8"
    selected_color "#eaf8ff"
    selected_hover_color "#fff6f8"
    insensitive_color "#6b7c85"
    text_align 0.5
    xalign 0.5
    yalign 0.5
    outlines [(1, "#02050a", 0, 1)]

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

# --- Console readout and legend text (enter_m_readout_row, enter_m_legend_row) ---

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
        persistent.textbox_opacity = 0.75
        autofocus_set_dim_mode("darken")
        # persistent.enter_m_photosensitive is deliberately NOT reset here, and
        # its control lives in Asarhythm's own settings drawer while that is the
        # only mode wired to it. See accessibility.rpy.
        persistent.enter_m_atmos_quality = "full"
        persistent.enter_m_panels = True
        persistent.enter_m_fx_detail = "full"
        persistent.msbf_gfx = "ultra"
        stage_panels_refresh()
        atmos_refresh()

        # Goes through the setter, not the persistent, because the engine flag
        # it derives (gl_powersave) is only forced at startup -- writing the
        # persistent alone would leave the running session on the old cadence.
        enter_m_set_low_resource(False)

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
                        text _("Fullscreen fills the monitor. Windowed is easier to alt-tab out of and to capture as a single window.") style "room_pref_note_label"

                    # Presenting every frame is the default; this hands the idle
                    # cadence back to the engine. See framerate.rpy.
                    text _("Low-Resource Mode") style "room_pref_row_label"
                    hbox:
                        style "room_pref_button_row"
                        textbutton _("On") style "room_pref_radio_button" action Function(enter_m_set_low_resource, True) selected enter_m_low_resource()
                        textbutton _("Off") style "room_pref_radio_button" action Function(enter_m_set_low_resource, False) selected (not enter_m_low_resource())
                    text _("Lets the game idle instead of drawing every frame, saving power on a laptop or handheld. Costs you smooth recordings and streams, because capture software only sees the frames the game actually draws.") style "room_pref_note_label"

                    # Developer meter samples presented frames; its timer requests redraws.
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
                    text _("The dissolves and rack-focus blurs between scenes. Off cuts straight to the next shot, which is faster to read through.") style "room_pref_note_label"

                    text _("Atmosphere") style "room_pref_row_label"
                    hbox:
                        style "room_pref_button_row"
                        textbutton _("Full") style "room_pref_small_button" action [SetField(persistent, "enter_m_atmos_quality", "full"), Function(atmos_refresh)] selected (persistent.enter_m_atmos_quality == "full")
                        textbutton _("Light") style "room_pref_small_button" action [SetField(persistent, "enter_m_atmos_quality", "light"), Function(atmos_refresh)] selected (persistent.enter_m_atmos_quality == "light")
                        textbutton _("Off") style "room_pref_small_button" action [SetField(persistent, "enter_m_atmos_quality", "off"), Function(atmos_refresh)] selected (persistent.enter_m_atmos_quality == "off")
                    text _("Lighting, grain and drifting particles over the scene, and the living title screen. Light keeps the look but holds it still; Off leaves the artwork as painted.") style "room_pref_note_label"

                    text _("Story Panels") style "room_pref_row_label"
                    hbox:
                        style "room_pref_button_row"
                        textbutton _("On") style "room_pref_radio_button" action Function(stage_panels_set_enabled, True) selected persistent.enter_m_panels
                        textbutton _("Off") style "room_pref_radio_button" action Function(stage_panels_set_enabled, False) selected (not persistent.enter_m_panels)
                    text _("The split-screen comic layout that the main story is staged in. Off falls back to one plain background per scene.") style "room_pref_note_label"

                    # The heavy game modes (Matsuda's fight, Kotonoha, Tsubaki,
                    # the Archivist Invasions). Low drops layers that are only
                    # decoration and never anything read to play. See
                    # graphics_detail.rpy for who honours it.
                    text _("Effects Detail") style "room_pref_row_label"
                    hbox:
                        style "room_pref_button_row"
                        textbutton _("Full") style "room_pref_radio_button" action Function(enter_m_set_fx_detail, "full") selected (enter_m_fx_detail() == "full")
                        textbutton _("Low") style "room_pref_radio_button" action Function(enter_m_set_fx_detail, "low") selected (enter_m_fx_detail() == "low")
                    text _("Low thins out the decoration in certain scenarios, for laptops and handhelds: fewer particles and afterimages, quieter backdrops and glows. Bullets, hazards, warnings and the interface stay exactly as they are.") style "room_pref_note_label"

                    # Only backdrops measured to pay for a capped pass (it
                    # costs a render of its own): on Oct 9 2026 that was
                    # Biography's room alone; Matsuda's, Tsubaki's and the
                    # other rooms got slower capped. Every stop draws the same
                    # picture at a different internal resolution. Sprites,
                    # text, UI and any pass that carries them (the invasion
                    # lens) are never touched. See msbf_fx_scaled in perf.rpy.
                    text _("Effects Resolution") style "room_pref_row_label"
                    hbox:
                        style "room_pref_button_row"
                        textbutton _("Native") style "room_pref_small_button" action SetField(persistent, "msbf_gfx", "ultra") selected (msbf_gfx_level() == "ultra")
                        textbutton _("720p") style "room_pref_small_button" action SetField(persistent, "msbf_gfx", "high") selected (msbf_gfx_level() == "high")
                        textbutton _("540p") style "room_pref_small_button" action SetField(persistent, "msbf_gfx", "performance") selected (msbf_gfx_level() == "performance")
                    text _("The resolution the Archivist Invasions render their heaviest room at before scaling it up to the window. A stop only changes anything when the window is larger than it, and a lower stop eases the load on the graphics card. Sprites, text and the interface always stay sharp.") style "room_pref_note_label"

                    text _("Textbox Opacity") style "room_pref_row_label"
                    bar value FieldValue(persistent, "textbox_opacity", range=1.0, max_is_zero=False, style="slider") style "room_pref_full_slider"
                    text _("How solid the dialogue box is. Lower lets more of the scene through behind the words.") style "room_pref_note_label"

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
                        text _("Mute All silences everything without losing where the sliders were set. Max Volume puts them to full.") style "room_pref_note_label"

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
                    text _("How fast dialogue types itself out, in characters per second. Instant prints the whole line at once. Clicking always skips to the end of the line either way.") style "room_pref_note_label"

                    hbox:
                        style "room_pref_button_row"
                        textbutton _("Auto Mode") style "room_pref_check_button" action Preference("auto-forward", "toggle")
                        textbutton _("After Click") style "room_pref_check_button" action Preference("auto-forward after click", "toggle")
                    text _("Auto Mode advances the story on its own once a line has finished. After Click keeps it going after you have clicked, instead of stopping there.") style "room_pref_note_label"

                    text _("Auto-Forward Delay") style "room_pref_row_label"
                    bar value Preference("auto-forward time") style "room_pref_full_slider"
                    text _("How long Auto Mode waits on a finished line before moving on. Further right is faster.") style "room_pref_note_label"

                # --- GAME: how far the player is allowed to jump --------
                use pref_section("game", _("Game"), ROOM_MENU_CORAL, 0.15):

                    text _("Skip") style "room_pref_row_label"
                    hbox:
                        style "room_pref_button_row"
                        textbutton _("Unseen Text") style "room_pref_check_button" action Preference("skip", "toggle")
                        textbutton _("After Choices") style "room_pref_check_button" action Preference("after choices", "toggle")
                    text _("Holding Ctrl fast-forwards. By default it only skips text you have already read; Unseen Text lets it run through new writing too, and After Choices keeps it running past a decision instead of stopping at one.") style "room_pref_note_label"

                    if config.developer:
                        text _("Rollback Edge") style "room_pref_row_label"
                        hbox:
                            style "room_pref_button_row"
                            textbutton _("Off") style "room_pref_small_button" action Preference("rollback side", "disable")
                            textbutton _("Left") style "room_pref_small_button" action Preference("rollback side", "left")
                            textbutton _("Right") style "room_pref_small_button" action Preference("rollback side", "right")
                        text _("Drag from that edge of the screen to rewind, for input without a scroll wheel.") style "room_pref_note_label"

                # --- ASSIST ---------------------------------------------
                use pref_section("assist", _("Assist"), ROOM_MENU_TEAL, 0.18):

                    hbox:
                        style "room_pref_button_row"
                        textbutton _("Cursor Assist") style "room_pref_check_button" action Preference("automatic move", "toggle")
                        textbutton _("Audio Focus") style "room_pref_check_button" action Preference("emphasize audio", "toggle")
                    text _("Cursor Assist moves the pointer to the default button for you. Audio Focus ducks music and effects under the voice track.") style "room_pref_note_label"

                    text _("Speaker Focus") style "room_pref_row_label"
                    hbox:
                        style "room_pref_button_row"
                        textbutton _("None") style "room_pref_small_button" action Function(autofocus_set_dim_mode, "none") selected (persistent.autofocus_dim_mode == "none")
                        textbutton _("Opaque") style "room_pref_small_button" action Function(autofocus_set_dim_mode, "opaque") selected (persistent.autofocus_dim_mode == "opaque")
                        textbutton _("Darken") style "room_pref_small_button" action Function(autofocus_set_dim_mode, "darken") selected (persistent.autofocus_dim_mode == "darken")
                    text _("What happens to everyone who is not talking. Darken shades them back, Opaque leaves them lit, None treats every character on screen the same.") style "room_pref_note_label"


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

style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text

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
    add Solid("#101b24bd")
    frame:
        background IM_PAPER_PANEL
        align (0.5, 0.5)
        xsize 680
        padding (40, 30)
        has vbox:
            xfill True
            spacing 20
        text "ENTER M / NOTICE":
            font gui.interface_font
            size 14
            kerning 1.4
            color "#805e41"
            outlines []
            xalign 0.5
        add "assets/gui/menu/illustrated/tab_selected.svg" xysize (280, 3) xalign 0.5
        text _(message):
            font gui.default_font
            size 25
            color IM_INK
            outlines []
            slow_cps 0
            xmaximum 600
            text_align 0.5
            xalign 0.5
        textbutton _("OK"):
            id "dialog_ok"
            style "im_notice_button"
            xalign 0.5
            default_focus True
            action ok_action

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
