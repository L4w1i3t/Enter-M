# =============================================================================
# planner_display.rpy -- reusable immersive planner presentation
# =============================================================================
#
# PUBLIC ENTRY POINT
#   call enter_m_show_planner(
#       left_day, left_date, left_items,
#       right_day, right_date, right_items,
#       left_note=None, right_note=None,
#   )
#
# Each item is a (category, text) pair; notes are plain strings. Entries write
# themselves out one character at a time, in order, left page then right page.
# A dismiss input while writing fast-forwards to the finished planner; the next
# one closes it. Escape always closes. AFM is temporarily disabled while open.
#
# HOW THE WRITING WORKS (and why it's done this way)
#   The reveal is driven manually by a repeating `timer` + plain Python state
#   (the _enter_m_planner_* store vars below), NOT by Text(slow=...). The slow-
#   text path is unreliable inside a re-evaluating screen (it tends to pop the
#   whole line in at once), and it gives no clean signal for "writing is still
#   happening" -- which we need for the sustained pencil SFX. The manual driver
#   is deterministic and exposes that signal via _enter_m_planner_writing().
#
#   To avoid text reflowing as it types (words jumping lines when they wrap), we
#   keep the FULL line laid out and hide the un-written tail with an {alpha=0}
#   tag -- only the written prefix shows. See enter_m_planner_reveal_text().
#   (Assumes planner text contains no raw { or [ -- the story data is plain text.)
#
# WRITING SFX
#   `modwriting` (mod_assets/sfx/writing.ogg) loops on its own "planner_write"
#   channel for the entire writing duration, then stops the moment the last
#   character lands. page_turn still plays once when the planner opens.
# =============================================================================

# Tunables for the typewriter pacing.
define ENTER_M_PLANNER_TICK = 0.03   # seconds between reveal ticks
define ENTER_M_PLANNER_CPS = 1       # characters revealed per tick (~33 cps)
define ENTER_M_PLANNER_CLOSE = 0.24  # how long the exit animation runs before Return

# Manual-reveal state (set fresh each open by _enter_m_planner_reset).
default _enter_m_planner_texts = []     # flat, ordered list of strings to write
default _enter_m_planner_total = 0      # len(texts)
default _enter_m_planner_step = 0       # index of the entry currently being written
default _enter_m_planner_revealed = 0   # chars revealed of the current entry
default _enter_m_planner_finish = False # True once writing is force-finished/done
default _enter_m_planner_sfx_on = False # is the writing loop currently playing?

init python:
    # Dedicated looping channel for the pencil-scratch loop, on the sfx mixer so
    # the SFX volume slider controls it. try/except keeps autoreload from erroring
    # on a re-register.
    try:
        renpy.music.register_channel("planner_write", mixer="sfx", loop=True)
    except Exception:
        pass

    def _enter_m_planner_reset(texts):
        # Prime the reveal state for a fresh planner (called from the label).
        store._enter_m_planner_texts = list(texts)
        store._enter_m_planner_total = len(store._enter_m_planner_texts)
        store._enter_m_planner_step = 0
        store._enter_m_planner_revealed = 0
        store._enter_m_planner_finish = False
        store._enter_m_planner_sfx_on = False

    def _enter_m_planner_writing():
        # True while there is still text left to type out.
        return (not store._enter_m_planner_finish) and store._enter_m_planner_step < store._enter_m_planner_total

    def _enter_m_planner_sfx(on):
        # Start/stop the looping writing SFX. Idempotent (won't double-play/stop),
        # and only starts if there's actually something being written.
        if on:
            if _enter_m_planner_writing() and not store._enter_m_planner_sfx_on:
                renpy.music.play(audio.modwriting, channel="planner_write", loop=True)
                store._enter_m_planner_sfx_on = True
        else:
            if store._enter_m_planner_sfx_on:
                renpy.music.stop(channel="planner_write", fadeout=0.18)
            store._enter_m_planner_sfx_on = False

    def enter_m_planner_reveal_text(full, shown):
        # Return the line with only the first `shown` characters visible, keeping
        # the rest laid out but transparent so the text never reflows mid-type.
        full = full or ""
        shown = max(0, min(int(shown), len(full)))
        if shown >= len(full):
            return full
        return full[:shown] + "{alpha=0}" + full[shown:] + "{/alpha}"

    def _enter_m_planner_tick():
        # One reveal step: advance the visible character count for the current
        # entry; when it's fully shown, move to the next entry. Stops the SFX the
        # instant the last entry finishes.
        if not _enter_m_planner_writing():
            _enter_m_planner_sfx(False)
            return

        current = store._enter_m_planner_texts[store._enter_m_planner_step]
        store._enter_m_planner_revealed += ENTER_M_PLANNER_CPS

        if store._enter_m_planner_revealed >= len(current):
            store._enter_m_planner_step += 1
            store._enter_m_planner_revealed = 0

        if not _enter_m_planner_writing():
            _enter_m_planner_sfx(False)

        renpy.restart_interaction()

    def _enter_m_planner_finish_now():
        # Force every entry to fully written (the "click to finish" path).
        store._enter_m_planner_finish = True
        store._enter_m_planner_step = store._enter_m_planner_total
        _enter_m_planner_sfx(False)
        renpy.restart_interaction()


transform enter_m_planner_open:
    alpha 0.0
    zoom 0.97
    yoffset 18
    easeout 0.24 alpha 1.0 zoom 1.0 yoffset 0

# Exit transform for the planner panel -- a near-mirror of the open: it settles
# back, shrinks slightly, drifts down, and fades out. Swapped in when the screen
# flips planner_closing (see the screen below).
transform enter_m_planner_close:
    alpha 1.0
    zoom 1.0
    yoffset 0
    easein 0.22 alpha 0.0 zoom 0.965 yoffset 24

# Fade for the dim backdrop + hint text -- in on show, out on close. Alpha only,
# so the full-screen tint never shifts and exposes the scene behind it.
transform enter_m_planner_veil_in:
    alpha 0.0
    easeout 0.20 alpha 1.0

transform enter_m_planner_veil_out:
    alpha 1.0
    easein 0.22 alpha 0.0


style enter_m_planner_day:
    font gui.interface_font
    size 27
    color "#3e342d"
    bold True
    outlines []

style enter_m_planner_date:
    font gui.interface_font
    size 17
    color "#7d6658"
    outlines []

style enter_m_planner_category:
    font gui.interface_font
    size 14
    color "#a14e4c"
    bold True
    outlines []
    kerning 2

style enter_m_planner_checkbox:
    font gui.interface_font
    size 21
    color "#4b443d"
    outlines []

style enter_m_planner_entry:
    font "gui/font/Halogen.ttf"
    size 27
    color "#292724"
    outlines []
    line_spacing 2

style enter_m_planner_note:
    font "gui/font/Halogen.ttf"
    size 22
    color "#65564c"
    outlines []
    italic True

style enter_m_planner_hint:
    font gui.interface_font
    size 15
    color "#eee7d8cc"
    outlines [(1, "#000000aa", 0, 1)]
    kerning 2


# One planner page. Renders the day header, ruled lines, and the items written
# so far. Reveal state is read from the active_step / revealed / finish_writing
# args (which mirror the _enter_m_planner_* store vars). An item is drawn when it
# is the active step or earlier (or when writing is finished); the active item is
# sliced to `revealed` chars, completed items show in full.
screen enter_m_planner_page(day_name, date_label, items, item_offset, active_step, revealed, finish_writing, note=None, note_step=None):
    fixed:
        xysize (486, 548)

        add Solid("#f7f0d8")
        add Solid("#e8ddbd"):
            xysize (18, 548)

        for _line_y in range(112, 518, 32):
            add Solid("#7299ad44"):
                xpos 24
                ypos _line_y
                xysize (440, 1)

        add Solid("#b85d5a66"):
            xpos 42
            ypos 90
            xysize (1, 428)

        text day_name style "enter_m_planner_day":
            xpos 54
            ypos 24

        text date_label style "enter_m_planner_date":
            xpos 54
            ypos 62

        vbox:
            xpos 56
            ypos 112
            xsize 386
            spacing 13

            for _item_index, (_category, _entry) in enumerate(items):
                $ _entry_step = item_offset + _item_index

                if finish_writing or _entry_step <= active_step:
                    # Completed entries show fully; the active one shows `revealed` chars.
                    $ _entry_shown = len(_entry) if (finish_writing or _entry_step < active_step) else revealed

                    vbox:
                        spacing 0

                        text _category.upper() style "enter_m_planner_category"

                        hbox:
                            spacing 8

                            text "[[ ]" style "enter_m_planner_checkbox"
                            text enter_m_planner_reveal_text(_entry, _entry_shown):
                                style "enter_m_planner_entry"
                                xmaximum 340

        if note and (finish_writing or (note_step is not None and note_step <= active_step)):
            $ _note_shown = len(note) if (finish_writing or (note_step is not None and note_step < active_step)) else revealed
            text enter_m_planner_reveal_text(note, _note_shown):
                style "enter_m_planner_note"
                xmaximum 380
                xpos 58
                ypos 474


screen enter_m_planner(left_day, left_date, left_items, right_day, right_date, right_items, left_note=None, right_note=None):
    modal True
    zorder 250

    default planner_closing = False   # True once the exit animation is playing

    # Kick off the writing SFX as soon as the planner appears (the tick stops it
    # when the last character lands).
    on "show" action Function(_enter_m_planner_sfx, True)
    on "replace" action Function(_enter_m_planner_sfx, True)

    # Pull the live reveal state out of the store vars.
    $ _active_step = _enter_m_planner_step
    $ _revealed = _enter_m_planner_revealed
    $ _finish = _enter_m_planner_finish
    $ _total = _enter_m_planner_total

    # Step bookkeeping (must match the flat order built in the label: left items,
    # left note, right items, right note).
    $ _left_note_count = 1 if left_note else 0
    $ _right_item_offset = len(left_items) + _left_note_count
    $ _left_note_step = len(left_items) if left_note else None
    $ _right_note_step = _right_item_offset + len(right_items) if right_note else None

    $ _writing_complete = _finish or _active_step >= _total

    # Closing sequence: stop the pencil loop, flip a page, and flag the screen as
    # closing so the panel + veil play their exit transforms. (A timer below then
    # Returns once the exit has had time to play -- see ENTER_M_PLANNER_CLOSE.)
    $ _planner_close = [Function(_enter_m_planner_sfx, False), Play("sound", audio.page_turn), SetScreenVariable("planner_closing", True)]

    # What a click/space does, depending on state:
    if planner_closing:
        $ _dismiss_action = NullAction()                            # already closing -> ignore
    elif _writing_complete:
        $ _dismiss_action = _planner_close                          # done writing -> animate out
    else:
        $ _dismiss_action = Function(_enter_m_planner_finish_now)   # still writing -> finish it

    # Escape closes (with the same animation) from any state.
    $ _escape_action = NullAction() if planner_closing else _planner_close
    $ _hint_text = "CLICK / SPACE TO CLOSE" if _writing_complete else "WRITING...  /  CLICK TO FINISH"

    # Swap enter vs exit transforms for the panel and the veil (backdrop + hint).
    $ _planner_panel_anim = enter_m_planner_close if planner_closing else enter_m_planner_open
    $ _planner_veil_anim = enter_m_planner_veil_out if planner_closing else enter_m_planner_veil_in

    key "dismiss" action _dismiss_action
    key "skip" action _dismiss_action
    key "game_menu" action _escape_action

    add Solid("#030507bb") at _planner_veil_anim

    fixed:
        xysize (1080, 620)
        align (0.5, 0.48)
        at _planner_panel_anim

        add Solid("#00000066"):
            xpos 14
            ypos 16
            xysize (1052, 586)

        frame:
            xysize (1060, 594)
            align (0.5, 0.5)
            background Solid("#573d34")
            padding (22, 22)

            fixed:
                hbox:
                    align (0.5, 0.5)
                    spacing 26

                    use enter_m_planner_page(left_day, left_date, left_items, 0, _active_step, _revealed, _finish, left_note, _left_note_step)
                    use enter_m_planner_page(right_day, right_date, right_items, _right_item_offset, _active_step, _revealed, _finish, right_note, _right_note_step)

                add Solid("#3e2d29"):
                    xalign 0.5
                    yalign 0.5
                    xysize (18, 548)

                for _ring_y in range(25, 535, 51):
                    add Solid("#b9aaa0"):
                        xalign 0.5
                        ypos _ring_y
                        xysize (42, 4)

    # The reveal driver: ticks only while writing (and not mid-close).
    if not _writing_complete and not planner_closing:
        timer ENTER_M_PLANNER_TICK repeat True action Function(_enter_m_planner_tick)

    # Skipping jumps straight to the finished planner.
    if renpy.is_skipping() and not _writing_complete and not planner_closing:
        timer 0.01 action Function(_enter_m_planner_finish_now)

    # Once closing, let the exit transforms play, then actually leave the screen.
    if planner_closing:
        timer ENTER_M_PLANNER_CLOSE action Return()

    text _hint_text style "enter_m_planner_hint":
        at _planner_veil_anim
        xalign 0.5
        ypos 680


label enter_m_show_planner(left_day, left_date, left_items, right_day, right_date, right_items, left_note=None, right_note=None):
    window hide
    $ _enter_m_planner_prev_afm = renpy.game.preferences.afm_enable
    $ renpy.game.preferences.afm_enable = False

    # Build the flat, ordered list of strings to write (left items -> left note ->
    # right items -> right note) and prime the reveal state.
    python:
        _planner_flat = [_e for (_c, _e) in left_items]
        if left_note:
            _planner_flat.append(left_note)
        _planner_flat += [_e for (_c, _e) in right_items]
        if right_note:
            _planner_flat.append(right_note)
        _enter_m_planner_reset(_planner_flat)

    play sound page_turn

    call screen enter_m_planner(left_day, left_date, left_items, right_day, right_date, right_items, left_note, right_note)

    # Safety: stop the writing loop no matter how the screen was dismissed
    # (e.g. Escape mid-write returns immediately).
    $ _enter_m_planner_sfx(False)
    $ renpy.game.preferences.afm_enable = _enter_m_planner_prev_afm
    window auto
    return
