# =============================================================================
# ENTER-M :: THE VAULT  ("the one room that isn't finished")
# -----------------------------------------------------------------------------
# WHAT THIS IS
#   A room off the Archive that does nothing, on purpose. It is a promise about
#   a mechanic that ships with the full release, dressed as a records vault
#   that has been shut for long enough to grow cobwebs.
#
#   The first time the player opens it, Kotonoha is standing there and tells
#   them so. Every time after that the room is empty and the interface is flat,
#   which is the joke landing rather than the joke wearing off: she said she
#   would not be here, and she isn't.
#
# WHY THE UI IS DELIBERATELY DULL
#   Every other interface family in this game is trying to seduce the player --
#   the Archive is a warm library, the Arcade is a cabinet, the title screen is
#   somebody's bedroom. This one is a filing system. Six drawers, no contents,
#   one number that reads zero, and a notice taped to the far wall. Nothing
#   here is clickable except the way out.
#
#   That is a design decision and not an unfinished screen, and the difference
#   between those two things is entirely in the execution: the layout is
#   precise, the type is set, the entrance is choreographed, and the room
#   around it is doing more work than any other menu in the game. It is meant
#   to look like an empty room built with care -- not like a TODO.
#
# WHY IT IS A LAYER OVER THE ARCHIVE, NOT A MENU OF ITS OWN
#   The Vault is an Archive door, so it opens the way every other Archive door
#   does: SHOWN over the hub and HIDDEN again, like the Roster and the Music
#   Room. It has no `tag menu`, deliberately. A menu-tagged screen would
#   REPLACE the Archive rather than cover it, and its way out would then be a
#   Return() -- which from the title is ShowMenu("main_menu"), so leaving the
#   Vault would have dropped the player on the title screen instead of back
#   among the shelves they just walked in from. Nothing here reads or writes
#   `_game_menu_screen` either, which is the variable the pause menu routes on.
#
# WHAT LIVES WHERE
#   vault.rpy      (here)  the DOOR and the UI -- the open/close pair the
#                          Archive calls, the room screen, the ledger, the
#                          greeting.
#   vault_fx.rpy           the ROOM -- grade, fluorescent stutter, air, filth.
#
# THE ONLY HOOKS INTO THE REST OF THE GAME
#   1. archive.rpy      one bottom-right corner button, guarded by
#                       renpy.has_screen("vault").
#   2. def_images.rpy   `image bg vault`.
#   Delete this folder and 1 no-ops on its own guard; 2 becomes an unused image
#   definition. Nothing else in the game refers to the Vault, except the Dev
#   Hub's FLAGS page, which checks for `vault_greeting` before it offers to
#   re-arm the greeting.
#
# RELATED READING
#   menu_transitions.rpy section 6 -- why the music is handed over the way it
#   is below, and why it is asked for in the same interaction that starts the
#   move rather than after it.
# =============================================================================


# -----------------------------------------------------------------------------
# STATE
# -----------------------------------------------------------------------------
# Persistent rather than a save flag, and that is the point: the greeting is
# addressed to the PLAYER -- the one opening every drawer in the Archive to see
# what each one does -- not to a character in a save file. Starting a new game
# does not make you a stranger to Kotonoha again.
#
# To see the greeting a second time (for testing, or after changing her
# lines): Dev Hub -> FLAGS -> RE-ARM, then open the Vault again.
default persistent.vault_greeted = False


# -----------------------------------------------------------------------------
# PALETTE
# -----------------------------------------------------------------------------
# Four greys and one rust. The rust is the only chromatic thing in the whole
# interface and it appears exactly three times -- the status word, the drawer
# handles, and the second line of the notice -- so that when the room finally
# does hold something, there is somewhere obvious for that something to be.
define VAULT_INK = "#c6cacb"        # what you are meant to read
define VAULT_MUTED = "#7d8588"      # what you are meant to skim
define VAULT_DIM = "#525a5e"        # what is only there for the layout
define VAULT_RUST = "#a06d45"       # the one accent, spent sparingly
define VAULT_PANEL = "#06080ad6"    # the rail's own value block
define VAULT_PLATE = "#12161899"    # an empty label, waiting for a label

# Geometry the rail and its contents both have to agree on. The rail is
# narrower than the title screen's 430 because the picture behind it is the
# whole point of the room and a wider panel would cover the drawers it is
# describing.
define VAULT_RAIL_W = 372
define VAULT_ROW_X = 28
define VAULT_ROW_W = 316
define VAULT_ROW_H = 44
define VAULT_ROW_Y0 = 168
define VAULT_ROW_PITCH = 52
define VAULT_ROWS = 6


# -----------------------------------------------------------------------------
# ENTRANCE
# -----------------------------------------------------------------------------
# Slower than every other menu in the game, and that is the only thing this
# screen does slowly. A room this dead should not snap open; the drawers should
# arrive at the pace of somebody reading a list they already know is empty.
#
# Every ATL here comes to rest. The rail settles, the rows settle, the notice
# settles, and then the only thing still moving on the screen is the dust --
# which is exactly the impression the room is supposed to leave.
transform vault_rail_arrive:
    subpixel True
    alpha 0.0
    xoffset -18
    easeout_cubic 0.52 alpha 1.0 xoffset 0


transform vault_rule_arrive:
    subpixel True
    xanchor 0.0
    xzoom 0.0
    pause 0.30
    easeout_cubic 0.54 xzoom 1.0


# One drawer at a time, and the stagger is generous: 0.055s a row over six rows
# is a third of a second of list, which is long enough to read as a sequence
# rather than as one block fading up.
transform vault_row_arrive(delay=0.0):
    subpixel True
    alpha 0.0
    xoffset -12
    pause delay
    parallel:
        easeout 0.34 alpha 1.0
    parallel:
        easeout_cubic 0.40 xoffset 0


transform vault_notice_arrive:
    subpixel True
    alpha 0.0
    pause 0.62
    easeout 0.70 alpha 1.0


# Button events reach the direct child, so the visible plate is that child and
# the stationary button stays the complete mouse and focus target. Same rule as
# the title screen's rows and the Arcade's cartridges.
transform vault_return_focus:
    subpixel True
    xoffset 0
    on hover:
        easeout_cubic 0.16 xoffset 6
    on idle:
        easeout_cubic 0.16 xoffset 0


# -----------------------------------------------------------------------------
# THE DOOR
# -----------------------------------------------------------------------------
# The Archive's bottom-right corner button calls vault_open(); everything that
# leaves the room calls vault_close(). They are a matched pair on purpose --
# the way in hands the music to dump.ogg and the way out hands it back to the
# Archive's own track, each in the SAME interaction that starts its move,
# because that is what lets the picture and the sound land together (see
# menu_transitions.rpy section 6). The doorway transition is the one every
# Archive child uses, and its black hold is timed to that handoff.
init python:

    def vault_open():
        """Open the Vault over the Archive, greeting a first-timer on the way.

        The greeting runs as its own context, exactly like an Arcade cabinet
        (arcade_context.rpy) and the Archive's own OP replay: a self-contained
        VN scene that unwinds cleanly back to the caller. It ends on black, so
        the room is shown with NO transition afterwards -- the doorway would
        first redraw the Archive just to close over it, flashing the shelves
        the player left a whole conversation ago. Coming out of black, the
        room's own staggered entrance is the arrival.

        Returns None explicitly. A screen action's return value propagates, and
        an action list that hands back a truthy value from the middle of itself
        is the bug that Chapter Select found the hard way.
        """

        enter_m_menu_music(audio.dump)

        if not persistent.vault_greeted:
            renpy.call_in_new_context("vault_greeting")
        else:
            renpy.transition(enter_m_menu_doorway)

        renpy.show_screen("vault")
        renpy.restart_interaction()
        return None

    def vault_close():
        """Hide the Vault and give the Archive its own music back.

        Hiding the room does not re-run the Archive's `on "show"` handler --
        the Archive was never hidden -- so without the explicit handoff here
        the player would be back among the shelves with dump.ogg still playing.
        """

        enter_m_menu_music(audio.archive)
        renpy.transition(enter_m_menu_doorway)
        renpy.hide_screen("vault")
        renpy.restart_interaction()
        return None


# -----------------------------------------------------------------------------
# THE ROOM
# -----------------------------------------------------------------------------
# Modal, because it is drawn OVER the Archive: without it a click on empty
# floor would fall through to whichever catalogue card happens to sit beneath
# that spot. The room covers the whole frame, so nothing of the hub shows.
screen vault():

    modal True

    # dump.ogg is asked for here as well as in vault_open(), so the room
    # brings its own track however it comes to be shown. The intent guard in
    # enter_m_menu_music makes the redundant ask free -- it returns immediately
    # when the track it is being asked for is already playing.
    on "show" action EnterMMenuMusic(audio.dump)

    # Both keys close the room and nothing else. Keys reach the topmost screen
    # first, so the Archive's own game_menu handler underneath -- which leaves
    # the Archive entirely -- never sees these presses.
    key "game_menu" action Function(vault_close)
    key "K_ESCAPE" action Function(vault_close)

    # The room, its grade, its stutter and its air. vault_fx.rpy.
    use vault_room_layer

    # --- the rail ------------------------------------------------------------
    # A flat value block rather than a framed panel. The picture behind it is
    # already doing the texture; a bevelled or bordered panel on top of it
    # would be two surfaces arguing.
    add Solid(VAULT_PANEL) xysize (VAULT_RAIL_W, 720)
    add Solid("#2b3134") xpos (VAULT_RAIL_W - 2) ypos 0 xysize (1, 720)
    add Solid("#0a0d0f") xpos (VAULT_RAIL_W - 1) ypos 0 xysize (1, 720)

    fixed:
        at vault_rail_arrive

        text "THE VAULT":
            style "vault_title"
            xpos VAULT_ROW_X
            ypos 44

        add Solid("#2f3538") xpos VAULT_ROW_X ypos 88 xysize (232, 1) at vault_rule_arrive
        add Solid(VAULT_RUST) xpos VAULT_ROW_X ypos 87 xysize (44, 2) at vault_rule_arrive

        text "RECORDS / DEPOSIT AND RETRIEVAL":
            style "vault_subtitle"
            xpos VAULT_ROW_X
            ypos 98

        # --- the readout -----------------------------------------------------
        # A fixed with explicit xpos/xanchor, NOT an hbox with a greedy null.
        # Measured in this project already: giving a box an explicit xsize
        # stops it packing its children left and spreads them instead, and
        # text_align on a Text is inert. See the note above archive_readout.
        fixed:
            xpos VAULT_ROW_X
            ypos 128
            xysize (VAULT_ROW_W, 16)

            text "HOLDINGS   0" style "vault_readout" yalign 0.5

            text "SEALED":
                style "vault_readout_key"
                xanchor 1.0
                xpos VAULT_ROW_W
                yalign 0.5

    # --- the drawers ---------------------------------------------------------
    # Six of them, all empty, none of them a button. Making these focusable
    # would be a lie about what this room does -- there is nothing behind any
    # of them yet -- and it would put six dead stops in the way of the one
    # control that works. Keyboard focus goes straight to Return.
    #
    # Each row is a drawer front read left to right: the slot number, the blank
    # label plate where a name will eventually be typed, and the handle. All
    # three are geometry rather than glyphs.
    for vault_i in range(VAULT_ROWS):

        fixed:
            at vault_row_arrive(0.24 + 0.055 * vault_i)
            xpos VAULT_ROW_X
            ypos (VAULT_ROW_Y0 + vault_i * VAULT_ROW_PITCH)
            xysize (VAULT_ROW_W, VAULT_ROW_H)

            add Solid("#0d1113a0") xysize (VAULT_ROW_W, VAULT_ROW_H)
            add Solid("#22282b") xysize (VAULT_ROW_W, 1)
            add Solid("#05080a") ypos (VAULT_ROW_H - 1) xysize (VAULT_ROW_W, 1)

            text ("%02d" % (vault_i + 1)):
                style "vault_slot"
                xpos 13
                yalign 0.5

            # The empty label. A plate and a rule under it, because a plate on
            # its own reads as a disabled button and a plate with a line under
            # it reads as somewhere to write.
            add Solid(VAULT_PLATE) xpos 44 ypos 13 xysize (196, 18)
            add Solid("#262c2f") xpos 44 ypos 31 xysize (196, 1)

            # The handle.
            add Solid(VAULT_RUST) xpos 262 ypos 20 xysize (34, 4)
            add Solid("#0a0d0f") xpos 262 ypos 24 xysize (34, 2)

    fixed:
        at vault_rail_arrive

        add Solid("#22282b") xpos VAULT_ROW_X ypos 494 xysize (VAULT_ROW_W, 1)

        text "NO CONTENTS ON RECORD.":
            style "vault_smallprint"
            xpos VAULT_ROW_X
            ypos 508

        text "LAST INSPECTION: NOT ON FILE.":
            style "vault_smallprint"
            xpos VAULT_ROW_X
            ypos 526

    button:
        id "vault_return"
        style "vault_return_button"
        xpos VAULT_ROW_X
        ypos 644
        xysize (156, 34)
        action Function(vault_close)
        default_focus True

        fixed:
            at vault_return_focus
            xfill True
            yfill True

            add Solid(VAULT_RUST) xysize (3, 18) ypos 8
            text "RETURN" style "vault_return_text" xpos 16 yalign 0.5

    # --- the notice ----------------------------------------------------------
    # The one thing in the right-hand two thirds of the screen, low and
    # centred in what is left of the frame after the rail. It carries the
    # actual tease, in the register the room would use to say it: a facilities
    # notice, not a marketing line.
    frame:
        style "vault_notice"
        xpos 624
        ypos 592
        xysize (404, 74)
        at vault_notice_arrive

        fixed:
            xfill True
            yfill True

            text "THIS FACILITY IS NOT IN SERVICE":
                style "vault_notice_head"
                xalign 0.5
                ypos 14

            text "SCHEDULED TO REOPEN AT FULL RELEASE":
                style "vault_notice_body"
                xalign 0.5
                ypos 40


# -----------------------------------------------------------------------------
# THE GREETING
# -----------------------------------------------------------------------------
# Runs once, in its own context, launched from vault_open().
#
# WHY A CONTEXT AND NOT A SCREEN
#   This is dialogue -- a named speaker, quote marks, a click-to-continue, the
#   history buffer, the player's own text speed. All of that is the say screen's
#   job, and the say screen needs a context that is not a menu. Reimplementing
#   any of it inside a menu screen would be building a second, worse say screen
#   for eight lines of one conversation.
#
# WHY THE BACKGROUND IS PUT UP BY HAND
#   The room screen gets its background from `use vault_room_layer`, which
#   cannot be used here: a screen draws above the master layer, and Kotonoha
#   has to stand IN the room rather than behind it. So the graded background
#   goes on the master layer under her, and only the air, the clouds and the
#   lens go on the screens layer over her -- which is where they belong anyway.
#   Dust is between you and a person; a vignette is on the lens, not on the
#   wall.
init python:

    def vault_room_scene():
        """Put the graded room on the master layer, under the cast.

        The quality branch has to happen here rather than in an ATL, because an
        ATL cannot ask a question. Shader first (innermost), camera second: a
        mesh blits its child at (0, 0) and never looks at its pixels, so a
        camera on the inside would be graded through a stationary lens.
        """

        _vault_at = [vault_camera if vaultfx_alive() else vault_camera_still]

        if vaultfx_lit():
            _vault_at.insert(
                0, vault_grade if vaultfx_alive() else vault_grade_still)

        renpy.scene("master")
        renpy.show("bg vault", at_list=_vault_at, layer="master")


label vault_greeting:

    python:
        # The title screen's identity must not follow us in here -- same
        # reasoning, and the same values, as arcade_context.rpy. The SDK
        # restores every one of them when this context exits.
        #
        # `_atmos_state` is on the list for a different reason, and it matters
        # more than it looks. atmosphere.rpy re-shows its master-layer grade
        # after EVERY `scene` statement unless the context says it is the main
        # menu -- and this context has just been told it is not. So the story's
        # lighting preset, if one is held, would be painted over the Vault.
        #
        # The obvious fix, atmos_clear(), was here for one build and is WRONG:
        # it empties the state dict IN PLACE, and that dict is the story's own
        # (a `default`, saved with the game). Scoping the NAME and binding a
        # fresh dict to it gives this context an empty grade while the story's
        # dict is never touched -- and the SDK rebinds the original on exit.
        renpy.context_dynamic(
            "main_menu", "_menu", "_game_menu_screen", "quick_menu",
            "_atmos_state")
        main_menu = False
        _menu = False
        _game_menu_screen = None
        quick_menu = False
        renpy.context()._menu = False
        renpy.context()._main_menu = False

        if hasattr(store, "_atmos_default_state"):
            _atmos_state = _atmos_default_state()

        # The camera-layer saturation atmosphere.rpy uses is per-context scene
        # state, so resetting it here resets it for this context alone.
        renpy.show_layer_at([], layer="master", camera=True, reset=False)

        # Nothing hides the Archive here, and nothing needs to:
        # renpy.call_in_new_context takes `_clear_layers`, it defaults to True,
        # and a new context therefore starts with every layer already empty --
        # master, screens and all. An explicit hide was here for one build and
        # was measured to be a no-op. (Verified the other way round too: a
        # screen shown in the parent before the call does NOT survive into the
        # child.)

    scene black
    pause 2.0

    # The room arrives on its own, slowly, before anybody is in it. A beat of
    # empty room first is what makes her being there register as a surprise.
    $ vault_room_scene()
    $ renpy.show_screen("vault_air_layer", _zorder=-1)
    with Dissolve(0.85)

    pause 1.0
    
    # t53 rather than the usual solo t11: same centre, 0.68 zoom instead of
    # 0.80. She is describing the room, and at t11 she stands in front of
    # most of it. The wider read is the direction, not an oversight.
    show kotonoha casual smug at t53
    with Dissolve(2.0)
    ko "Oh... There you are."
    ko casual teasing "Checking every little nook and cranny, aren't you? Every drawer, every corner, every button that probably shouldn't exist..."
    ko "...Hey, hey, I'm not criticizing. It's how I read, too. Back cover, index, spine, one or two middle bits, and only then the beginning."
    ko casual neut "Unfortunately, you have found the one room that isn't finished."
    ko casual thinking "It's called the Vault. It's meant to hold what you've earned and set aside... Eventually..."
    ko "At the moment it holds dust, some cobwebs, a drawer somebody left open, and, unfortunately, me."
    ko casual smug "{i}*sigh*{/i} Here I am, doing an unpaid maid service to check this place every now and then..."
    ko casual neut "Come back at full release. I think there will be something in the drawers by then. Maybe even some cleanup."
    ko "Or come back tomorrow and stand in an empty room for a while. I won't stop you."
    ko casual happy "You do seem to have the temperament for it."
    ko casual neut "...Do mind the dust. That bunny over there in the corner's my favorite."

    show kotonoha at thide
    hide kotonoha

    # A held beat of the room without her in it. This is the shot the player
    # will get every time from now on, and showing it once while they are still
    # expecting her to say something is what sells that.
    pause 1.2

    $ persistent.vault_greeted = True

    scene black
    with Dissolve(0.40)

    $ renpy.hide_screen("vault_air_layer")

    return


# -----------------------------------------------------------------------------
# STYLES
# -----------------------------------------------------------------------------
# Almost everything here is the interface face (NovaSquare), which is the most
# mechanical of the three and the only one that suits a filing system. The
# title is the name face, set large and widely tracked, because a stencilled
# room name is the one place this interface is allowed a voice.
#
# No glyph in any of these is anything but ASCII. All three of this project's
# fonts render every arrow, triangle and pictogram as tofu, so every mark in
# this screen that is not a letter is a Solid.

style vault_title is gui_text:
    font gui.name_font
    size 33
    kerning 3.4
    color VAULT_INK
    outlines [(2, "#03060899", 0, 1)]

style vault_subtitle is gui_text:
    font gui.interface_font
    size 9
    kerning 1.4
    color VAULT_DIM
    outlines [(1, "#03060899", 0, 1)]

style vault_readout is gui_text:
    font gui.interface_font
    size 10
    kerning 1.2
    color VAULT_MUTED
    outlines [(1, "#03060899", 0, 1)]

style vault_readout_key is vault_readout:
    color VAULT_RUST

style vault_slot is gui_text:
    font gui.interface_font
    size 11
    kerning 1.0
    color VAULT_DIM
    outlines [(1, "#03060899", 0, 1)]

style vault_smallprint is gui_text:
    font gui.interface_font
    size 9
    kerning 0.8
    color "#4a5155"
    outlines [(1, "#03060899", 0, 1)]

style vault_return_button is gui_button:
    padding (0, 0, 0, 0)
    background None
    hover_background "#141a1c9e"
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style vault_return_text is gui_text:
    font gui.interface_font
    size 13
    kerning 2.0
    color VAULT_MUTED
    hover_color VAULT_INK
    outlines [(1, "#03060899", 0, 1)]

# The notice sits over the painting rather than over the rail, so it carries
# its own value block and a heavier outline than anything on the rail needs.
style vault_notice is empty:
    background Solid("#05080ad2")
    padding (0, 0, 0, 0)

style vault_notice_head is gui_text:
    font gui.interface_font
    size 13
    kerning 2.2
    color VAULT_MUTED
    outlines [(2, "#02040699", 0, 1)]

style vault_notice_body is gui_text:
    font gui.interface_font
    size 10
    kerning 1.5
    color VAULT_RUST
    outlines [(2, "#02040699", 0, 1)]
