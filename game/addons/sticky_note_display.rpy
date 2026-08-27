# =============================================================================
# sticky_note_display.rpy -- reusable handwritten sticky-note presentation
# =============================================================================
#
# PUBLIC ENTRY POINT
#   call enter_m_show_sticky_note(lines, signature=None, ink=None, sfx=True)
#
#   `lines` is a plain string (one line) or a sequence of strings -- one per
#   handwritten line. Long lines wrap inside the note; keep each entry to a
#   sentence or clause and let the note break it. `signature` is a bare name;
#   the note draws the em dash itself, so pass "Mom", not "-- Mom".
#
#   Lines write themselves out one character at a time, top to bottom, with the
#   signature last. A dismiss input while writing fast-forwards to the finished
#   note; the next one closes it. Escape always closes. AFM is temporarily
#   disabled while the note is up.
#
# WHY IT EXISTS
#   Mom's notes around the house used to be plain italic narration, which read
#   as MC's inner voice rather than as an object on the counter. This gives them
#   a physical page. Call sites: game/story/season1/0522, 0523, 0525, 0530.
#
# RELATIONSHIP TO planner_display.rpy
#   This deliberately MIRRORS the planner's reveal technique instead of importing
#   from it, so either file can be dropped without breaking the other. If you fix
#   a reveal bug here, check whether the planner has the same one.
#
# HOW THE WRITING WORKS (and why it's done this way)
#   The reveal is driven by a repeating `timer` + plain Python state (the
#   _enter_m_sticky_* store vars below), NOT by Text(slow=...). The slow-text
#   path is unreliable inside a re-evaluating screen (it tends to pop the whole
#   line in at once) and gives no clean signal for "writing is still happening",
#   which the sustained pen SFX needs.
#
#   To keep text from reflowing as it types (words jumping lines when they wrap),
#   the FULL line stays laid out and the un-written tail is hidden with an
#   {alpha=0} tag -- only the written prefix shows. This is also what lets the
#   whole block sit vertically centred on the note without shifting as it fills.
#   (Assumes note text contains no raw { or [ -- the story data is plain text.)
#
# GEOMETRY -- read this before moving any number
#   The art (assets/gui/enter_m/stickynote.png, 960x640) has the note drawn ALREADY
#   TILTED about 5 degrees counter-clockwise, so the text has to be tilted to
#   match. Rather than hand-place rotated text, the writing sits in its own
#   960x640 overlay in "note space" -- axis-aligned coordinates, as if the note
#   were straight -- and the whole overlay is rotated by ENTER_M_STICKY_TILT.
#   Both the paper and the overlay are centred (align 0.5, 0.5) in the outer
#   fixed, because rotate/blur padding re-centres a displayable and would throw
#   off an xpos/ypos of 0.
#
#   Measured from the art, in note space:
#     note quad        x 213..768, y 52..583
#     bottom-right     the peeled corner eats everything past about (663, 517),
#                      so the writing area stops short of it
#   ENTER_M_STICKY_AREA is that safe writing area. If you swap the art, re-measure.
#
# WRITING SFX
#   `modwriting` (assets/audio/sfx/writing.ogg) loops on its own "sticky_write"
#   channel for the writing duration and stops the moment the last character
#   lands. page_turn plays once when the note appears. Pass sfx=False for a note
#   that should appear without the pen loop.
# =============================================================================

# -----------------------------------------------------------------------------
# Tunables
# -----------------------------------------------------------------------------
define ENTER_M_STICKY_TICK = 0.026    # seconds between reveal ticks
define ENTER_M_STICKY_CPS = 1         # characters revealed per tick (~38 cps)
define ENTER_M_STICKY_CLOSE = 0.24    # how long the exit animation runs before Return

# 0.84 keeps the note visibly SMALLER than the planner spread -- at 0.92 a scrap
# of paper read as big as a two-page planner and lost its scale.
define ENTER_M_STICKY_ZOOM = 0.84     # on-screen scale of the 960x640 art
define ENTER_M_STICKY_TILT = -5.05    # degrees; matches the lean drawn into the art
define ENTER_M_STICKY_AREA = (265, 96, 451, 420)   # note-space x, y, w, h to write in
define ENTER_M_STICKY_YALIGN = 0.48   # where the block sits in that area (0 = top)
define ENTER_M_STICKY_INK = "#2a3a52" # default ballpoint blue-black

image enter_m_sticky_paper = "assets/gui/enter_m/stickynote.png"

# Manual-reveal state (set fresh each open by _enter_m_sticky_reset).
default _enter_m_sticky_texts = []     # flat, ordered list of strings to write
default _enter_m_sticky_total = 0      # len(texts)
default _enter_m_sticky_step = 0       # index of the line currently being written
default _enter_m_sticky_revealed = 0   # chars revealed of the current line
default _enter_m_sticky_finish = False # True once writing is force-finished/done
default _enter_m_sticky_sfx_on = False # is the writing loop currently playing?
default _enter_m_sticky_sfx_want = True # does this note want the pen loop at all?


init python:
    # Dedicated looping channel for the pen loop, on the sfx mixer so the SFX
    # volume slider controls it. try/except keeps autoreload from erroring on a
    # re-register.
    try:
        renpy.music.register_channel("sticky_write", mixer="sfx", loop=True)
    except Exception:
        pass

    def enter_m_sticky_lines(lines):
        # Accept a bare string or any sequence; drop empties so a stray "" can't
        # cost the player a click on a blank line.
        if lines is None:
            return []
        if isinstance(lines, str):
            lines = [lines]
        return [l for l in lines if l]

    def enter_m_sticky_signature(signature):
        # The note draws its own em dash so every call site signs the same way.
        if not signature:
            return None
        return u"— " + signature

    def _enter_m_sticky_reset(texts, want_sfx=True):
        # Prime the reveal state for a fresh note (called from the label).
        store._enter_m_sticky_texts = list(texts)
        store._enter_m_sticky_total = len(store._enter_m_sticky_texts)
        store._enter_m_sticky_step = 0
        store._enter_m_sticky_revealed = 0
        store._enter_m_sticky_finish = False
        store._enter_m_sticky_sfx_on = False
        store._enter_m_sticky_sfx_want = bool(want_sfx)

    def _enter_m_sticky_writing():
        # True while there is still text left to write out.
        return (not store._enter_m_sticky_finish) and store._enter_m_sticky_step < store._enter_m_sticky_total

    def _enter_m_sticky_sfx(on):
        # Start/stop the looping pen SFX. Idempotent (won't double-play/stop), and
        # only starts if this note wants it and something is actually being written.
        if on:
            if store._enter_m_sticky_sfx_want and _enter_m_sticky_writing() and not store._enter_m_sticky_sfx_on:
                renpy.music.play(audio.modwriting, channel="sticky_write", loop=True)
                store._enter_m_sticky_sfx_on = True
        else:
            if store._enter_m_sticky_sfx_on:
                renpy.music.stop(channel="sticky_write", fadeout=0.18)
            store._enter_m_sticky_sfx_on = False

    def enter_m_sticky_reveal_text(full, shown):
        # Return the line with only the first `shown` characters visible, keeping
        # the rest laid out but transparent so the text never reflows mid-write.
        full = full or ""
        shown = max(0, min(int(shown), len(full)))
        if shown >= len(full):
            return full
        return full[:shown] + "{alpha=0}" + full[shown:] + "{/alpha}"

    def _enter_m_sticky_tick():
        # One reveal step: advance the visible character count for the current
        # line; when it's fully shown, move to the next. Stops the SFX the instant
        # the last line finishes.
        if not _enter_m_sticky_writing():
            _enter_m_sticky_sfx(False)
            return

        current = store._enter_m_sticky_texts[store._enter_m_sticky_step]
        store._enter_m_sticky_revealed += ENTER_M_STICKY_CPS

        if store._enter_m_sticky_revealed >= len(current):
            store._enter_m_sticky_step += 1
            store._enter_m_sticky_revealed = 0

        if not _enter_m_sticky_writing():
            _enter_m_sticky_sfx(False)

        renpy.restart_interaction()

    def _enter_m_sticky_finish_now():
        # Force every line to fully written (the "click to finish" path).
        store._enter_m_sticky_finish = True
        store._enter_m_sticky_step = store._enter_m_sticky_total
        _enter_m_sticky_sfx(False)
        renpy.restart_interaction()


# -----------------------------------------------------------------------------
# Transforms
# -----------------------------------------------------------------------------

# The lean drawn into the art. Applied to the writing overlay only -- the paper
# is already tilted. subpixel keeps the rotated handwriting from stair-stepping.
transform enter_m_sticky_tilt:
    rotate ENTER_M_STICKY_TILT
    subpixel True

# Drop shadow: the same paper flattened to black, blurred, and nudged down-right.
# TintMatrix multiplies every channel to zero and leaves alpha alone, so this is
# the note's exact silhouette.
transform enter_m_sticky_shadow:
    matrixcolor TintMatrix("#000000")
    alpha 0.5
    blur 14
    xoffset 18
    yoffset 22

# The note comes in like it's being turned to face you: up from below, a touch
# small, over-tilted, then settling flat.
transform enter_m_sticky_open:
    alpha 0.0
    zoom (ENTER_M_STICKY_ZOOM * 0.94)
    yoffset 30
    rotate 1.8
    easeout 0.28 alpha 1.0 zoom ENTER_M_STICKY_ZOOM yoffset 0 rotate 0.0

# Near-mirror of the open: settles back, shrinks slightly, drifts down, fades.
transform enter_m_sticky_close:
    alpha 1.0
    zoom ENTER_M_STICKY_ZOOM
    yoffset 0
    rotate 0.0
    easein 0.22 alpha 0.0 zoom (ENTER_M_STICKY_ZOOM * 0.965) yoffset 26 rotate -1.2

# Fade for the dim backdrop + hint text. Alpha only, so the full-screen tint
# never shifts and exposes the scene behind it.
transform enter_m_sticky_veil_in:
    alpha 0.0
    easeout 0.20 alpha 1.0

transform enter_m_sticky_veil_out:
    alpha 1.0
    easein 0.22 alpha 0.0


# -----------------------------------------------------------------------------
# Styles
# -----------------------------------------------------------------------------

style enter_m_sticky_line:
    font "assets/gui/font/Halogen.ttf"
    size 36
    color "#2a3a52"
    outlines []
    line_spacing 3

style enter_m_sticky_sign is enter_m_sticky_line

style enter_m_sticky_hint:
    font gui.interface_font
    size 15
    color "#eee7d8cc"
    outlines [(1, "#000000aa", 0, 1)]
    kerning 2


# -----------------------------------------------------------------------------
# Screen
# -----------------------------------------------------------------------------

screen enter_m_sticky_note(lines, signature=None, ink=None):
    modal True
    zorder 250

    default sticky_closing = False   # True once the exit animation is playing

    # Kick off the pen SFX as soon as the note appears (the tick stops it when
    # the last character lands).
    on "show" action Function(_enter_m_sticky_sfx, True)
    on "replace" action Function(_enter_m_sticky_sfx, True)

    # Pull the live reveal state out of the store vars.
    $ _active_step = _enter_m_sticky_step
    $ _revealed = _enter_m_sticky_revealed
    $ _finish = _enter_m_sticky_finish
    $ _total = _enter_m_sticky_total

    $ _ink = ink or ENTER_M_STICKY_INK
    $ _sig_text = enter_m_sticky_signature(signature)
    $ _sig_step = len(lines) if _sig_text else None   # signature writes last

    $ _writing_complete = _finish or _active_step >= _total

    # Closing sequence: stop the pen loop, rustle the paper, and flag the screen
    # as closing so the note + veil play their exit transforms. (A timer below
    # then Returns once the exit has had time to play -- ENTER_M_STICKY_CLOSE.)
    $ _sticky_close = [Function(_enter_m_sticky_sfx, False), Play("sound", audio.page_turn), SetScreenVariable("sticky_closing", True)]

    # What a click/space does, depending on state:
    if sticky_closing:
        $ _dismiss_action = NullAction()                           # already closing -> ignore
    elif _writing_complete:
        $ _dismiss_action = _sticky_close                          # done writing -> animate out
    else:
        $ _dismiss_action = Function(_enter_m_sticky_finish_now)   # still writing -> finish it

    # Escape closes (with the same animation) from any state.
    $ _escape_action = NullAction() if sticky_closing else _sticky_close
    $ _hint_text = "CLICK / SPACE TO CLOSE" if _writing_complete else "WRITING...  /  CLICK TO FINISH"

    $ _sticky_note_anim = enter_m_sticky_close if sticky_closing else enter_m_sticky_open
    $ _sticky_veil_anim = enter_m_sticky_veil_out if sticky_closing else enter_m_sticky_veil_in

    key "dismiss" action _dismiss_action
    key "skip" action _dismiss_action
    key "game_menu" action _escape_action

    add Solid("#030507bb") at _sticky_veil_anim

    fixed:
        xysize (960, 640)
        align (0.5, 0.46)
        at _sticky_note_anim

        add "enter_m_sticky_paper":
            at enter_m_sticky_shadow
            align (0.5, 0.5)

        add "enter_m_sticky_paper":
            align (0.5, 0.5)

        # The writing overlay: note-space coordinates, tilted to match the art.
        fixed:
            xysize (960, 640)
            align (0.5, 0.5)
            at enter_m_sticky_tilt

            fixed:
                xpos ENTER_M_STICKY_AREA[0]
                ypos ENTER_M_STICKY_AREA[1]
                xysize (ENTER_M_STICKY_AREA[2], ENTER_M_STICKY_AREA[3])

                vbox:
                    xsize ENTER_M_STICKY_AREA[2]
                    yalign ENTER_M_STICKY_YALIGN
                    spacing 11

                    for _line_index, _line in enumerate(lines):
                        # Written lines show in full; the active one shows `revealed`
                        # chars; later ones aren't drawn at all yet. The {alpha=0}
                        # tail means the block's height never changes, so nothing
                        # slides while it fills.
                        if _finish or _line_index <= _active_step:
                            $ _line_shown = len(_line) if (_finish or _line_index < _active_step) else _revealed
                            text enter_m_sticky_reveal_text(_line, _line_shown):
                                style "enter_m_sticky_line"
                                color _ink
                                xmaximum ENTER_M_STICKY_AREA[2]

                    if _sig_text and (_finish or _sig_step <= _active_step):
                        $ _sig_shown = len(_sig_text) if (_finish or _sig_step < _active_step) else _revealed
                        # Right-aligned via fixed + xpos/xanchor: xalign inside a
                        # sized box does not reliably right-pack here.
                        fixed:
                            xsize ENTER_M_STICKY_AREA[2]
                            yfit True

                            text enter_m_sticky_reveal_text(_sig_text, _sig_shown):
                                style "enter_m_sticky_sign"
                                color _ink
                                xpos ENTER_M_STICKY_AREA[2]
                                xanchor 1.0

    # The reveal driver: ticks only while writing (and not mid-close).
    if not _writing_complete and not sticky_closing:
        timer ENTER_M_STICKY_TICK repeat True action Function(_enter_m_sticky_tick)

    # Skipping jumps straight to the finished note.
    if renpy.is_skipping() and not _writing_complete and not sticky_closing:
        timer 0.01 action Function(_enter_m_sticky_finish_now)

    # Once closing, let the exit transforms play, then actually leave the screen.
    if sticky_closing:
        timer ENTER_M_STICKY_CLOSE action Return()

    text _hint_text style "enter_m_sticky_hint":
        at _sticky_veil_anim
        xalign 0.5
        ypos 680


# PUBLIC: present a sticky note and block until the player writes it out and
# clicks it away. See the header for the argument shapes.
label enter_m_show_sticky_note(lines, signature=None, ink=None, sfx=True):
    window hide
    $ _enter_m_sticky_prev_afm = renpy.game.preferences.afm_enable
    $ renpy.game.preferences.afm_enable = False

    # Build the flat, ordered list of strings to write (lines, then signature)
    # and prime the reveal state.
    python:
        _sticky_note_lines = enter_m_sticky_lines(lines)
        _sticky_note_flat = list(_sticky_note_lines)
        _sticky_note_sig = enter_m_sticky_signature(signature)
        if _sticky_note_sig:
            _sticky_note_flat.append(_sticky_note_sig)
        _enter_m_sticky_reset(_sticky_note_flat, sfx)

    play sound page_turn

    call screen enter_m_sticky_note(_sticky_note_lines, signature, ink)

    # Safety: stop the pen loop no matter how the screen was dismissed (e.g.
    # Escape mid-write returns immediately).
    $ _enter_m_sticky_sfx(False)
    $ renpy.game.preferences.afm_enable = _enter_m_sticky_prev_afm
    window auto
    return
