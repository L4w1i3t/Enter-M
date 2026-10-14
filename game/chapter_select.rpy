# New Game opens this six-card chapter selector in every build. A chapter is
# playable only when its entry label exists; Dev Hub owns direct date jumps.
# Card entrances settle so they do not continuously request redraws.
# The cancel sentinel contains a colon, which cannot be a script label name.
# Return(None) would return True from Ren'Py's action, so it is not a sentinel.

define CS_BACK = "chapter_select:back"


init python:

    ENTER_M_CHAPTERS = (
        # (name, span, entry label, the line under the grid)
        (
            "Chapter 0.5", "MAY 15 – MAY 31", "disclaimer",
            "Seventeen days in May, and most of a school year still ahead.",
        ),
        (
            "Chapter 1", "JUNE 1 – JULY 15", "a0601",
            None,
        ),
        (
            "Chapter 2", "JULY 16 – SEPTEMBER 1", "a0716",
            None,
        ),
        (
            "Chapter 3", "SEPTEMBER 2 – OCTOBER 15", "a0902",
            None,
        ),
        (
            "Chapter 4", "OCTOBER 16 – DECEMBER 31", "a1016",
            None,
        ),
        (
            "Chapter 5", "JANUARY 1 – MARCH 7", "a0101",
            None,
        ),
    )

    # The archive keeps the 1280x720 masters intact. Chapter panes use separate
    # 648x232 crops, twice their display size, so this grid does not
    # decode six full CGs just to paint its small windows.
    ENTER_M_CHAPTER_ART = (
        "assets/cg/chapter_select/chapter_05_open_invitation.png",
        "assets/cg/chapter_select/chapter_1_room_for_six.png",
        "assets/cg/chapter_select/chapter_2_summer_uncontained.png",
        "assets/cg/chapter_select/chapter_3_between_bells.png",
        "assets/cg/chapter_select/chapter_4_after_the_noise.png",
        "assets/cg/chapter_select/chapter_5_somewhere_warm.png",
    )
    ENTER_M_CHAPTER_THUMBNAILS = tuple(
        path.replace("assets/cg/", "assets/gui/").replace(".png", ".webp")
        for path in ENTER_M_CHAPTER_ART
    )

    def chapter_select_rows():
        """The grid, with each row's availability read off the script itself.

        Returns one `(name, span, entry, note, is_open)` per chapter. `entry`
        is None on a row that has nothing to jump to, so a caller cannot start
        a chapter this function has just called unplayable.
        """

        rows = []

        for name, span, entry, note in ENTER_M_CHAPTERS:
            is_open = bool(entry) and renpy.has_label(entry)
            rows.append((name, span, entry if is_open else None, note, is_open))

        return tuple(rows)

    def cs_card_at(index, is_open):
        """The card's at-list: staggered arrival, plus the lift if it is live.

        A dark card gets the arrival and nothing else -- lifting under the
        cursor would promise a click it does not honour.
        """

        arrive = cs_card_arrive(0.14 + 0.045 * index)

        if is_open:
            return [arrive, cs_card_focus]

        return arrive

    def chapter_select_locked_note():
        """The line a dark window shows, naming where the story stops for now."""

        written = [row[0] for row in chapter_select_rows() if row[4]]

        if not written:
            return _("Not available.")

        return _("Not available yet. The story currently ends with %s.") % written[-1]


# -----------------------------------------------------------------------------
# 2. GEOMETRY
# -----------------------------------------------------------------------------
# Three across, two down, on the same left margin as the header and the footer
# rule. Stated once here so the grid, the rules and the header cannot drift
# apart the next time a card grows.

define CS_CARD_W = 360
define CS_CARD_H = 220
define CS_GAP_X = 26
define CS_GAP_Y = 28
define CS_GRID_X = 74
define CS_GRID_Y = 156
define CS_ROW_W = (3 * CS_CARD_W + 2 * CS_GAP_X)

# The pane inside a card, inset clear of the plate's 9-patch border.
define CS_GLASS_X = 18
define CS_GLASS_Y = 16
define CS_GLASS_W = 324
define CS_GLASS_H = 116


# -----------------------------------------------------------------------------
# 3. ANIMATION
# -----------------------------------------------------------------------------

transform cs_header_arrive:
    subpixel True
    alpha 0.0
    xoffset -18
    pause 0.06
    easeout_cubic 0.40 alpha 1.0 xoffset 0


transform cs_rule_arrive(delay=0.24):
    subpixel True
    xanchor 0.0
    xzoom 0.0
    pause delay
    easeout_cubic 0.44 xzoom 1.0


transform cs_card_arrive(delay=0.0):
    subpixel True
    alpha 0.0
    yoffset 16
    pause delay
    parallel:
        easeout 0.30 alpha 1.0
    parallel:
        easeout_cubic 0.36 yoffset 0


# Button events reach the direct child, so the lift lives on that child and the
# stationary button stays the whole mouse target. Only a playable card lifts --
# a dark one answers a hover by explaining itself in the footer, and moving it
# would promise a click it does not honour.
transform cs_card_focus:
    subpixel True
    yoffset 0
    on hover:
        easeout_cubic 0.16 yoffset -5
    on idle:
        easeout_cubic 0.16 yoffset 0




transform cs_detail_swap(key=0):
    subpixel True
    alpha 0.0
    xoffset -8
    easeout 0.20 alpha 1.0 xoffset 0


# -----------------------------------------------------------------------------
# 3a. THE MOVE ON AND OFF THIS SCREEN
# -----------------------------------------------------------------------------
# New Game is a CONTEXT JUMP, not a ShowMenu, so none of the dispatchers in
# menu_transitions.rpy get a say in it: `Start()` pops the title context and
# `label start` resumes in the game context. Nothing asks for a transition
# along the way, so without the two requests in `chapter_select_open` the grid
# simply replaces the title screen between one frame and the next.
#
# It works because `Interface.old_scene` lives on the INTERFACE, not on a
# context -- so the outgoing frame really is the title screen the player just
# clicked, even though the game context's own scene lists say `black`.
#
# THE MOVE IN is the title doorway: menu_doorway.rpy sets `cs_move_open`.

# THE MOVE OFF, into the story. Every chapter entry takes the screen to black
# as its first act (the disclaimer via `nier_enter`), and a hard cut to black
# is the one move a threshold cannot afford. Requested at this call site only,
# so the shared Nier format keeps its own timing everywhere else it is used.
define cs_move_begin = Dissolve(0.45)


# -----------------------------------------------------------------------------
# 4. THE SCREEN
# -----------------------------------------------------------------------------

screen chapter_select():

    modal True

    default cs_sel = 0

    python:
        cs_rows = chapter_select_rows()
        cs_open = sum(1 for row in cs_rows if row[4])
        cs_dark_note = chapter_select_locked_note()

        cs_cur = min(cs_sel, len(cs_rows) - 1)
        cs_cur_name, cs_cur_span, cs_cur_entry, cs_cur_note, cs_cur_open = cs_rows[cs_cur]

        if cs_cur_open:
            cs_detail = cs_cur_note or _("Open.")
        else:
            cs_detail = cs_dark_note

        # First playable row, so the keyboard lands somewhere useful.
        cs_first_open = next((i for i, row in enumerate(cs_rows) if row[4]), None)

    key "K_ESCAPE" action Return(CS_BACK)
    key "game_menu" action Return(CS_BACK)

    # No arrival transform on the ground: the move in (section 3a) owns it.
    add illustrated_menu_backdrop("chapter")

    # --- header --------------------------------------------------------------
    fixed:
        at cs_header_arrive

        add illustrated_menu_motif("chapter", 86, 96) xpos 68 ypos 24

        text _("ACT ONE / THE CHAPTER FOLIO"):
            style "cs_kicker"
            xpos 172
            ypos 37

        text _("Chapter Select"):
            style "cs_title"
            xpos 168
            ypos 59

        text ("%d / %d OPEN" % (cs_open, len(cs_rows))):
            style "cs_meta"
            xanchor 1.0
            xpos (CS_GRID_X + CS_ROW_W)
            ypos 57

        text _("Six chapters. A place to begin."):
            style "cs_meta"
            xanchor 1.0
            xpos (CS_GRID_X + CS_ROW_W)
            ypos 82

    add Solid("#d9cdb654") xpos CS_GRID_X ypos 120 xysize (CS_ROW_W, 1) at cs_rule_arrive(0.22)
    add Solid(IM_PLUM) xpos CS_GRID_X ypos 119 xysize (52, 2) at cs_rule_arrive(0.22)

    # --- mounted chapter pictures -------------------------------------------
    for cs_i, (cs_i_name, cs_i_span, cs_i_entry, cs_i_note, cs_i_open) in enumerate(cs_rows):

        $ cs_art_path = ENTER_M_CHAPTER_THUMBNAILS[cs_i]
        # Future chapters keep a readable preview and an explicit locked state.
        $ cs_art_alpha = 1.0 if cs_i_open else 0.68

        button:
            style ("cs_card_button" if cs_i_open else "cs_card_locked_button")
            xysize (CS_CARD_W, CS_CARD_H)
            xpos (CS_GRID_X + (cs_i % 3) * (CS_CARD_W + CS_GAP_X))
            ypos (CS_GRID_Y + (cs_i // 3) * (CS_CARD_H + CS_GAP_Y))
            background None
            hover_background None

            # A dark card stays focusable on purpose -- hovering it is how the
            # footer gets to say why it is dark -- but it goes nowhere, and it
            # makes no selection sound doing it.
            id ("chapter_card_%d" % cs_i)
            action (Return(cs_i_entry) if cs_i_open else NullAction())
            hovered SetScreenVariable("cs_sel", cs_i)
            default_focus (cs_i == cs_first_open)

            fixed:
                at cs_card_at(cs_i, cs_i_open)
                xysize (CS_CARD_W, CS_CARD_H)

                add ("assets/gui/menu/illustrated/chapter/mount.svg" if cs_i_open else "assets/gui/menu/illustrated/chapter/mount_locked.svg")

                # The current environmental CGs remain the story preview.
                # Paper corners frame the image without drawing across it.
                add Transform(
                    cs_art_path,
                    xysize=(CS_GLASS_W, CS_GLASS_H),
                    fit="cover",
                    alpha=cs_art_alpha
                ):
                    xpos CS_GLASS_X
                    ypos CS_GLASS_Y

                if not cs_i_open:
                    add Solid("#41354828"):
                        xysize (CS_GLASS_W, CS_GLASS_H)
                        xpos CS_GLASS_X
                        ypos CS_GLASS_Y

                add "assets/gui/menu/illustrated/chapter/corners.svg"

                text "%02d" % (cs_i + 1):
                    style "cs_folio_number"
                    xpos 316
                    xanchor 0.5
                    ypos 140

                text cs_i_name:
                    style ("cs_name" if cs_i_open else "cs_name_locked")
                    xpos CS_GLASS_X
                    ypos 139

                text cs_i_span:
                    style ("cs_span" if cs_i_open else "cs_span_locked")
                    xpos CS_GLASS_X
                    ypos 178

                text (_("OPEN") if cs_i_open else _("NOT YET WRITTEN")):
                    style ("cs_strap" if cs_i_open else "cs_strap_locked")
                    xanchor 1.0
                    xpos (CS_GLASS_X + CS_GLASS_W)
                    ypos 197

    # --- footer --------------------------------------------------------------
    add Solid("#d9cdb62e") xpos CS_GRID_X ypos 646 xysize (CS_ROW_W, 1) at cs_rule_arrive(0.42)

    text cs_detail:
        style ("cs_note" if cs_cur_open else "cs_note_locked")
        at cs_detail_swap(cs_cur)
        xpos CS_GRID_X
        ypos 660
        xmaximum 820

    textbutton _("BACK TO TITLE"):
        style "cs_back_button"
        xanchor 1.0
        xpos (CS_GRID_X + CS_ROW_W + 10)
        ypos 654
        id "chapter_back"
        action Return(CS_BACK)


# -----------------------------------------------------------------------------
# 5. THE LABEL
# -----------------------------------------------------------------------------
# script.rpy calls this and nothing else.
#
# `_return` IS NOT OURS AND MUST BE CHECKED BEFORE IT IS BELIEVED.
#   It is one shared global. Every `call screen` in the game writes it -- the
#   pause menu's included, and the pause menu is reachable from inside the
#   story -- a screen event action that returns a non-None value bubbles up
#   through it (that is the bug the `ach_refresh` note in achievements.rpy
#   records), and an interaction cut short by a hot reload or by `Start()`
#   unwinding a context can leave whatever it likes in there. Handing that
#   straight to `jump expression` is a crash waiting for one of those: it shows
#   up as `LabelNotFound: could not find label 'True'`.
#
#   So the value is taken once, and it is only acted on if it is CS_BACK or a
#   string naming a label that exists. Anything else belongs to something that
#   is not this screen, and the honest answer is to show the grid again rather
#   than to crash or to dump the player at the title without explanation.
#
#   The back-out has its own sentinel for exactly this reason -- see CS_BACK in
#   section 1. `Return(None)` is NOT a way to say "nothing": the engine turns it
#   into `True`.
#
# The entry is JUMPED to, not called: the entry label owns the rest of the
# session, and a `return` out of it (declining the disclaimer, or reaching the
# end of a chapter) should land back in `start` and end the session there --
# exactly where `call disclaimer` used to land it. One frame, not two.

label chapter_select_open:

    $ _chapter_select_entry = None
    $ _chapter_select_chosen = False
    $ _chapter_select_arriving = True

    while not _chapter_select_chosen:

        # Only the first pass is an arrival. A re-ask is already looking at the
        # grid, and dissolving it into itself would flash the lamp for nothing.
        if _chapter_select_arriving:
            $ renpy.transition(cs_move_open)
            $ _chapter_select_arriving = False

        call screen chapter_select

        python:
            _chapter_select_entry = None

            if _return == CS_BACK:
                # The grid's own back-out.
                _chapter_select_chosen = True

            elif isinstance(_return, str) and renpy.has_label(_return):
                _chapter_select_entry = _return
                _chapter_select_chosen = True

            else:
                # Not ours. Ask again rather than act on it.
                _chapter_select_chosen = False

    # Backing out gets no transition of its own: ending the session hands the
    # move to config.end_game_transition, which is already the way home.
    if not _chapter_select_entry:
        return

    # The chapter image has been genuinely shown and selected at this point,
    # so it earns its archive unlock. Future chapter labels can be added here
    # without making their art available merely because it is registered.
    if _chapter_select_entry == "disclaimer":
        $ cg_unlock("Open Invitation")
    elif _chapter_select_entry == "a0601":
        $ cg_unlock("Room for Six")
    elif _chapter_select_entry == "a0716":
        $ cg_unlock("Summer Uncontained")
    elif _chapter_select_entry == "a0902":
        $ cg_unlock("Between Bells")
    elif _chapter_select_entry == "a1016":
        $ cg_unlock("After the Noise")
    elif _chapter_select_entry == "a0101":
        $ cg_unlock("Somewhere Warm")

    $ renpy.transition(cs_move_begin)

    jump expression _chapter_select_entry


# -----------------------------------------------------------------------------
# 6. STYLES
# -----------------------------------------------------------------------------
# Colour changes recurse through styles, which is why the cards' hover states
# live here rather than on the displayables: hover events themselves reach a
# button's direct child and stop there.

style cs_kicker is gui_text:
    font gui.interface_font
    size 10
    kerning 1.4
    color IM_PLUM
    outlines []

style cs_title is gui_text:
    font gui.default_font
    size 40
    # Was inherited by accident from a same-named dead style in char_stories.rpy;
    # stated here now that the other one is gone, so the title looks unchanged.
    bold True
    kerning 1.0
    color ROOM_MENU_INK
    outlines [(2, "#05090db8", 0, 1)]

style cs_meta is gui_text:
    font gui.interface_font
    size 12
    kerning 0.8
    color "#c0b5bb"
    outlines [(1, "#05090d99", 0, 1)]

style cs_card_button is gui_button:
    padding (0, 0, 0, 0)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style cs_card_locked_button is cs_card_button:
    activate_sound None

style cs_name is gui_text:
    font gui.default_font
    size 25
    color "#2c4947"
    hover_color "#246c60"
    outlines []

style cs_name_locked is cs_name:
    color "#655966"
    hover_color "#574556"

style cs_span is gui_text:
    font gui.interface_font
    size 10
    kerning 1.1
    color "#605a52"
    hover_color "#2b655e"
    outlines []

style cs_span_locked is cs_span:
    color "#796d74"
    hover_color "#665660"

style cs_strap is gui_text:
    font gui.interface_font
    size 10
    kerning 1.3
    color "#32695f"
    outlines []

style cs_strap_locked is cs_strap:
    color "#796777"
    hover_color "#695260"

style cs_note is gui_text:
    font gui.default_font
    size 16
    color "#d4d5ce"
    outlines [(1, "#05090db8", 0, 1)]

style cs_note_locked is cs_note:
    color "#8ea09f"

style cs_back_button is gui_button:
    background IM_RETURN_IDLE
    hover_background IM_RETURN_HOVER
    padding (15, 9, 15, 9)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style cs_back_button_text is gui_button_text:
    font gui.interface_font
    size 12
    kerning 1.0
    color IM_PAPER
    hover_color ROOM_MENU_CORAL
    outlines [(1, "#05090d99", 0, 1)]

style cs_folio_number is gui_text:
    font gui.interface_font
    size 15
    color "#f1e4cb"
    outlines []
