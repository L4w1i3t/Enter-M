# Shared save bank: restore, write, copy, rename and erase. Destructive UI
# actions confirm first. Modes use teal (read), ochre (write), lavender (copy/rename)
# and coral (erase); EMB_* constants describe the 836x520 content frame.
#
# Indices 1..36 retain Ren'Py slot names 1-1..6-6. Occupied slots outside that
# range are appended, preserving access to older saves. Extra save metadata
# records chapter, date and runtime; absent metadata is handled by the UI.
# EnterMBankUI is transient python_object state shared with confirmation
# overlays. Player labels live in persistent.enter_m_bank_labels, keyed by
# slot; copying carries the label and successful overwrite/erase clears it.
# Save/load availability also honors msbf_save_load_locked().

define EMB_W = 836
define EMB_H = 520

define EMB_MODE_W = 128                 # one mode button
define EMB_MODE_H = 32
define EMB_MODE_GAP = 8                 # 5 * 128 + 4 * 8 = 672, ends at x 672
define EMB_RULE_Y = 42                  # the tinted rule under the strip

define EMB_LIST_X = 0
define EMB_LIST_Y = 66
define EMB_LIST_W = 372
define EMB_LIST_H = 441                 # exactly 12 rows: 12 * 34 + 11 * 3

define EMB_ROW_W = 356                  # list width less the scrollbar gutter
define EMB_ROW_H = 34

define EMB_MON_X = 388
define EMB_MON_Y = 64
define EMB_MON_W = 448
define EMB_MON_H = 456

define EMB_SHOT_X = 404                 # EMB_MON_X + 16 padding
define EMB_SHOT_Y = 80
define EMB_SHOT_W = 416                 # EMB_MON_W - 32
define EMB_SHOT_H = 234                 # 16:9 of the above

define EMB_TITLE_Y = 322
define EMB_READ_Y = 354                 # first readout row
define EMB_READ_H = 23
define EMB_FOOT_Y = 474                 # rule under the readout
define EMB_HINT_Y = 480


# -----------------------------------------------------------------------------
# THE MODES
# One table drives the strip, the tint and the dispatch. `family` is the colour
# grammar documented at the top of the file, not decoration: it is what the
# player reads to know whether a click is safe.
# -----------------------------------------------------------------------------

define EMB_MODES = [
    ("restore", _("RESTORE"), "read"),
    ("write",   _("WRITE"),   "write"),
    ("copy",    _("COPY"),    "write"),
    ("rename",  _("RENAME"),  "write"),
    ("erase",   _("ERASE"),   "wipe"),
]

define EMB_ACCENT = {
    "read":  ROOM_MENU_TEAL,
    "write": ROOM_MENU_OCHRE,
    "wipe":  ROOM_MENU_CORAL,
}

# Family still owns the safety semantics. This second table only lets COPY and
# RENAME carry Matsuda's quieter lavender note without changing dispatch.
define EMB_MODE_ACCENT = {
    "restore": ROOM_MENU_TEAL,
    "write":   ROOM_MENU_OCHRE,
    "copy":    ROOM_MENU_LAVENDER,
    "rename":  ROOM_MENU_LAVENDER,
    "erase":   ROOM_MENU_CORAL,
}

# The shared selectors are authored for the 56px title/settings controls. The
# bank's dense directory rows are only 34px high, so they use the same bitmap
# family with compact nine-slice borders rather than crushing the large corners.
define EMB_SELECTOR_COMPACT_IDLE = Frame("assets/gui/menu/room_theme/selector_idle.png", 12, 8, 14, 8, tile=False)
define EMB_SELECTOR_COMPACT_HOVER = Frame("assets/gui/menu/room_theme/selector_hover.png", 12, 8, 14, 8, tile=False)
define EMB_SELECTOR_COMPACT_SELECTED = Frame("assets/gui/menu/room_theme/selector_selected.png", 12, 8, 14, 8, tile=False)
define EMB_SELECTOR_COMPACT_DANGER = Frame("assets/gui/menu/room_theme/selector_danger.png", 12, 8, 14, 8, tile=False)

define EMB_FAMILY = {
    "restore": "read",
    "write":   "write",
    "copy":    "write",
    "rename":  "write",
    "erase":   "wipe",
}

# How many slots the bank stands up, and how many of them Ren'Py calls a page.
# SLOTS must stay a multiple of PER_PAGE or the last page comes out ragged.
define EMB_PER_PAGE = 6
define EMB_SLOTS = 36


# -----------------------------------------------------------------------------
# RECORD LABELS
# Slot name -> the name the player typed. Deliberately persistent rather than
# per-save: it has to be readable from the main menu, where no save is loaded.
# -----------------------------------------------------------------------------

default persistent.enter_m_bank_labels = { }


# -----------------------------------------------------------------------------
# SAVE METADATA
# Three keys onto every new save, which is what the record card's readout reads.
# Registered at init -10 so the callback is in place before anything can save.
# Every field is guarded on its own: a save must never fail because a menu
# wanted a nicer caption.
# -----------------------------------------------------------------------------

init -10 python:

    def enter_m_bank_json(metadata):
        try:
            metadata["em_chapter"] = int(store.chapter)
        except Exception:
            pass

        try:
            metadata["em_date"] = store.calendar.get_formatted_date("full")
        except Exception:
            pass

        try:
            metadata["em_runtime"] = int(renpy.get_game_runtime())
        except Exception:
            pass

    # Drop any copy a hot reload left behind before adding this one: an init
    # block re-runs on Shift+R, and a callback registered twice writes the same
    # three keys twice into every save for the rest of the session.
    config.save_json_callbacks = [
        _cb for _cb in config.save_json_callbacks
        if getattr(_cb, "__name__", "") != "enter_m_bank_json"
    ]
    config.save_json_callbacks.append(enter_m_bank_json)


# -----------------------------------------------------------------------------
# THE MODEL
# -----------------------------------------------------------------------------

init python:

    class EnterMBankUI(python_object):
        """
        Which button is lit, which record is being copied, which record is
        being re-labelled, and which one the record card is showing.

        `python_object` and not `object`: inside a .rpy python block the bare
        name `object` is RevertableObject, and this state must survive a
        rollback rather than be undone by one. Mutated in place and never
        reassigned, so it stays out of save files entirely.
        """

        def __init__(self):
            self.mode = "restore"
            self.copy_src = None  # Slot selected as the copy source.
            self.rename = None  # Slot whose label is being edited.
            self.sel = None  # Slot displayed in the detail panel.

        def open(self, mode):
            """Called from the screen's `on "show"`. A visit always starts
            clean: a half-finished copy or a live rename must not be waiting
            for the player the next time they walk in."""
            if store.main_menu and mode == "write":
                mode = "restore"
            self.mode = mode
            self.copy_src = None
            self.rename = None
            self.sel = None
            renpy.restart_interaction()

        def set_mode(self, mode):
            self.mode = mode
            self.copy_src = None
            self.rename = None
            renpy.restart_interaction()

        def set_source(self, name):
            """Step one of a copy, and the click that backs out of it."""
            self.copy_src = None if self.copy_src == name else name
            renpy.restart_interaction()

        def select(self, name):
            if self.sel != name:
                self.sel = name
                renpy.restart_interaction()

    enter_m_bank_ui = EnterMBankUI()

    def enter_m_bank_name(bank_index):
        """Bank index (1-based) -> the slot name Ren'Py already uses.

        This is the whole of the backwards compatibility story: index 1 is
        "1-1", index 7 is "2-1", and every save the old page grid ever wrote is
        still addressed by the name it was written under."""
        return "%d-%d" % ((bank_index - 1) // EMB_PER_PAGE + 1, (bank_index - 1) % EMB_PER_PAGE + 1)

    def enter_m_bank_occupied():
        """The set of page-and-slot saves that exist right now.

        `list_saved_games(fast=True)` reads a dict the save location keeps in
        memory and rescans only when a file is written, so this is cheap enough
        to call on every screen execution -- which matters, because a screen
        `for` loop re-executes on every hover."""
        try:
            return set(renpy.list_saved_games(r"^\d+-\d+$", fast=True))
        except Exception:
            return set()

    def enter_m_bank_rows(occupied_slots):
        """The rows the list draws: the standing 36, then any occupied slot
        that falls outside them. The tail is what keeps the UI from stranding a
        save made on an old page 7-9; it is normally empty."""
        rows = [enter_m_bank_name(bank_index) for bank_index in range(1, EMB_SLOTS + 1)]
        known = set(rows)

        extra_slots = [slot_name for slot_name in occupied_slots if slot_name not in known]
        if extra_slots:
            def slot_sort_key(slot_name):
                try:
                    page, slot = slot_name.split("-", 1)
                    return (int(page), int(slot))
                except Exception:
                    return (9999, 9999)
            rows += sorted(extra_slots, key=slot_sort_key)

        return rows

    def enter_m_bank_json_of(name):
        try:
            return renpy.slot_json(name) or { }
        except Exception:
            return { }

    def enter_m_bank_label(name):
        """The player's own name for a record, or "" if it has none."""
        try:
            return persistent.enter_m_bank_labels.get(name, "") or ""
        except Exception:
            return ""

    def enter_m_bank_title(name, occupied):
        """What the row and the record card call this record."""
        if not occupied:
            return None

        custom_label = enter_m_bank_label(name).strip()
        if custom_label:
            return custom_label

        metadata = enter_m_bank_json_of(name)

        save_name = (metadata.get("_save_name") or "").strip()
        if save_name:
            return save_name

        date = (metadata.get("em_date") or "").strip()
        if date:
            return date

        return __("UNTITLED RECORD")

    def enter_m_bank_short(text, max_characters):
        """Row labels are drawn into a fixed 196px column and Ren'Py's Text has
        no ellipsis, so long names are cut here. Three ASCII dots on purpose --
        U+2026 is not in NovaSquare, and a missing glyph draws as tofu."""
        if text is None:
            return ""
        if len(text) <= max_characters:
            return text
        return text[:max_characters - 3].rstrip() + "..."

    def enter_m_bank_runtime(seconds):
        try:
            seconds = int(seconds)
        except Exception:
            return None
        if seconds < 60:
            return __("under a minute")
        hours, minutes = divmod(seconds // 60, 60)
        if hours:
            return "%dh %02dm" % (hours, minutes)
        return "%dm" % minutes

    def enter_m_bank_clear_label(name):
        """A label describes a recording. Overwrite or erase the recording and
        the label goes with it, or slot 04 keeps calling itself "before the
        fight" over a save from three chapters later."""
        try:
            if name in persistent.enter_m_bank_labels:
                del persistent.enter_m_bank_labels[name]
                renpy.save_persistent()
        except Exception:
            pass
        renpy.restart_interaction()

    def enter_m_bank_do_copy(source_slot, destination_slot):
        """Duplicate a record, label and all, and drop out of the two-step."""
        try:
            renpy.copy_save(source_slot, destination_slot)
        except Exception:
            enter_m_bank_ui.copy_src = None
            renpy.restart_interaction()
            return

        try:
            custom_label = enter_m_bank_label(source_slot)
            if custom_label:
                persistent.enter_m_bank_labels[destination_slot] = custom_label
            elif destination_slot in persistent.enter_m_bank_labels:
                del persistent.enter_m_bank_labels[destination_slot]
            renpy.save_persistent()
        except Exception:
            pass

        enter_m_bank_ui.copy_src = None
        renpy.restart_interaction()

    def enter_m_bank_do_erase(name):
        try:
            renpy.unlink_save(name)
        except Exception:
            # Keep the label attached when the underlying save could not be erased.
            renpy.restart_interaction()
            return
        enter_m_bank_clear_label(name)

    def enter_m_bank_begin_rename(name):
        enter_m_bank_ui.rename = name
        enter_m_bank_ui.sel = name
        renpy.restart_interaction()

    def enter_m_bank_end_rename():
        """Commit. The label was already being written on every keystroke (see
        the InputValue below), so this only has to flush it and put the panel
        back; an empty box means "no name", not an empty name."""
        name = enter_m_bank_ui.rename
        try:
            if name and not enter_m_bank_label(name).strip():
                persistent.enter_m_bank_labels.pop(name, None)
            renpy.save_persistent()
        except Exception:
            pass
        enter_m_bank_ui.rename = None
        renpy.restart_interaction()

    class EnterMBankLabelValue(InputValue):
        """Types straight into `persistent.enter_m_bank_labels[slot]`, so the
        record card's title line updates under the caret as you type.

        `enter()` must return None. Ren'Py's Input hands whatever it returns
        back as the interaction's result, and a non-None result here would
        return out of the menu."""

        def __init__(self, slot):
            self.slot = slot
            self.default = True
            self.editable = True
            self.returnable = False

        def get_text(self):
            return enter_m_bank_label(self.slot)

        def set_text(self, s):
            try:
                persistent.enter_m_bank_labels[self.slot] = s[:24]
            except Exception:
                pass
            renpy.restart_interaction()

        def enter(self):
            enter_m_bank_end_rename()
            return None

    # -------------------------------------------------------------------------
    # DISPATCH
    # One function decides what a row does, which keeps the "what happens when
    # I click" question answerable in one place instead of five branches deep
    # in screen language.
    # -------------------------------------------------------------------------

    def enter_m_bank_row_action(mode, name, record_index, occupied, copy_source):
        label = "%02d" % record_index

        if mode == "restore":
            if not occupied:
                return None
            load = FileLoad(name, confirm=False, slot=True)
            if store.main_menu:
                return load
            return Confirm(
                __("RESTORE RECORD %s? THE SESSION IN PROGRESS IS NOT SAVED.") % label,
                load)

        if mode == "write":
            if store.main_menu:
                return None
            done = Function(enter_m_bank_clear_label, name)
            write = FileSave(name, confirm=False, slot=True, action=done)
            if occupied:
                return Confirm(
                    __("RECORD %s IS OCCUPIED. OVERWRITE IT?") % label, write)
            return write

        if mode == "copy":
            if copy_source is None:
                if not occupied:
                    return None
                return Function(enter_m_bank_ui.set_source, name)
            if name == copy_source:
                # Clicking the source again backs out of the two-step.
                return Function(enter_m_bank_ui.set_source, name)
            copy = Function(enter_m_bank_do_copy, copy_source, name)
            if occupied:
                return Confirm(
                    __("SLOT %s IS OCCUPIED. OVERWRITE IT WITH THE COPY?") % label,
                    copy)
            return copy

        if mode == "rename":
            if not occupied:
                return None
            return Function(enter_m_bank_begin_rename, name)

        if mode == "erase":
            if not occupied:
                return None
            return Confirm(
                __("ERASE RECORD %s? THE RECORDING CANNOT BE RECOVERED.") % label,
                Function(enter_m_bank_do_erase, name))

        return None

    def enter_m_bank_hint(mode, copy_source, locked):
        """The line under the readout. It says what the next click does, in
        words, because the colour alone cannot say "you are half way through a
        copy"."""
        if store.main_menu and mode == "write":
            return __("NOTHING IS RUNNING. START OR RESTORE A SESSION BEFORE WRITING.")

        if mode == "restore":
            return __("SELECT A RECORD TO RESTORE IT.")
        if mode == "write":
            return __("SELECT A SLOT TO WRITE THE CURRENT SESSION INTO.")
        if mode == "copy":
            if copy_source is None:
                return __("SELECT THE RECORD TO DUPLICATE.")
            return __("NOW PICK THE SLOT TO COPY INTO -- OR THE SOURCE AGAIN TO CANCEL.")
        if mode == "rename":
            return __("SELECT A RECORD TO RE-LABEL IT.")
        if mode == "erase":
            return __("SELECT A RECORD TO ERASE. THIS CANNOT BE UNDONE.")
        return ""

    # -------------------------------------------------------------------------
    # THE EMPTY RECORD PLATE
    # Empty slots use a quiet folio placeholder rather than the old terminal
    # test card. Pure, so its handful of paper rules are built once.
    # -------------------------------------------------------------------------

    @renpy.pure
    def enter_m_bank_empty_card(w, h):
        return Fixed(
            Solid("#0b1418f2", xysize=(w, h)),
            Solid(ROOM_MENU_TEAL + "18", xysize=(w, 34), xpos=0, ypos=0),
            Solid(ROOM_MENU_CORAL + "30", xysize=(52, 3), xpos=24, ypos=28),
            Solid(ROOM_MENU_PAPER + "16", xysize=(w - 48, 1), xpos=24, ypos=66),
            Solid(ROOM_MENU_PAPER + "10", xysize=(w - 98, 1), xpos=24, ypos=84),
            Solid(ROOM_MENU_LAVENDER + "1e", xysize=(76, 76), xpos=w - 104, ypos=h - 100),
            Solid(ROOM_MENU_OCHRE + "22", xysize=(42, 42), xpos=w - 128, ypos=h - 66),
            xysize=(w, h),
        )

    # One labelled line of the record readout. Built as a `fixed` with two
    # absolute children rather than an hbox, because a box given an xsize
    # spreads its children instead of packing them and the value column comes
    # out crooked -- the same lesson as enter_m_readout_row in screens.rpy.
    def enter_m_bank_readout(rkey, rvalue, rwidth):
        return Fixed(
            Text(rkey, style="bank_readout_key", xpos=0, ypos=3),
            Text(rvalue, style="bank_readout_value", xpos=rwidth, xanchor=1.0, ypos=0),
            xysize=(rwidth, EMB_READ_H),
        )


# -----------------------------------------------------------------------------
# MOTION
# The record preview settles once. The old monitor sweep ran forever and kept a
# terminal metaphor alive after the title screen had left it behind.
# -----------------------------------------------------------------------------

transform bank_preview_arrive:
    subpixel True
    alpha 0.0
    yoffset 5
    easeout 0.24 alpha 1.0 yoffset 0


# =============================================================================
# THE SCREEN
# =============================================================================

screen data_bank(start_mode="restore"):

    tag menu

    # BOTH EVENTS, AND THE SECOND ONE IS THE LOAD-BEARING ONE. Ren'Py sends
    # "show" only when nothing with this screen's tag is on the layer already;
    # if there is, it sends "replace" instead (display/core.py, the
    # set_transform_event branch in SceneLists.add). Every screen here carries
    # `tag menu`, so arriving from the title -- where `main_menu` is already
    # showing under that tag -- fires "replace" and nothing else. With only an
    # `on "show"` handler the bank kept whatever mode the last visit left it
    # in: pause, save, Main Menu, Load Game and the strip was still on WRITE.
    on "show" action Function(enter_m_bank_ui.open, start_mode)
    on "replace" action Function(enter_m_bank_ui.open, start_mode)

    use bank_shell


# `save` and `load` are kept as doors, not as screens: every caller that still
# asks for one of the old two -- an addon, an orphaned .rpyc, or the engine's
# own `_game_menu_screen` if a `save_screen` label ever turns up -- lands in
# the bank with the right mode already lit, instead of on a missing screen.
# There is one implementation and it is `bank_shell`.
screen save():

    tag menu

    on "show" action Function(enter_m_bank_ui.open, "write")
    on "replace" action Function(enter_m_bank_ui.open, "write")

    use bank_shell


screen load():

    tag menu

    on "show" action Function(enter_m_bank_ui.open, "restore")
    on "replace" action Function(enter_m_bank_ui.open, "restore")

    use bank_shell


screen bank_shell():

    use room_menu_shell(_("Records"), "data_bank"):

        if msbf_save_load_locked() and not main_menu:
            use bank_locked
        else:
            use bank_body


# The boss fight holds the disk. Same wording as the panel this replaced, on
# the same chrome, so the fight's ESC key lands somewhere that explains itself.
screen bank_locked():

    frame:
        xalign 0.5
        yalign 0.5
        xsize 650
        ysize 150
        background ROOM_MENU_SELECTOR_IDLE
        padding (24, 22)

        vbox:
            spacing 12

            text _("The record bank is sealed during Matsuda's boss fight."):
                style "bank_locked_title"
                xalign 0.5
                text_align 0.5

            text _("Finish or leave the battle to reach your records."):
                style "bank_locked_hint"
                xalign 0.5
                text_align 0.5


screen bank_body():

    python:
        emb_mode = enter_m_bank_ui.mode
        emb_family = EMB_FAMILY.get(emb_mode, "read")
        emb_accent = EMB_MODE_ACCENT.get(emb_mode, EMB_ACCENT[emb_family])
        emb_src = enter_m_bank_ui.copy_src
        emb_rename = enter_m_bank_ui.rename

        emb_have = enter_m_bank_occupied()
        emb_rows = enter_m_bank_rows(emb_have)
        emb_used = sum(1 for r in emb_rows if r in emb_have)

        # The card holds the last record the pointer touched. Opening onto the
        # newest record means RESTORE is one click away from a cold start.
        emb_sel = enter_m_bank_ui.sel
        if emb_sel is None:
            emb_newest = None
            emb_newest_t = -1.0
            for r in emb_rows:
                if r in emb_have:
                    t = renpy.slot_mtime(r) or 0.0
                    if t > emb_newest_t:
                        emb_newest_t = t
                        emb_newest = r
            emb_sel = emb_newest or emb_rows[0]

        emb_sel_used = emb_sel in emb_have
        emb_sel_idx = emb_rows.index(emb_sel) + 1 if emb_sel in emb_rows else 1
        emb_sel_json = enter_m_bank_json_of(emb_sel) if emb_sel_used else { }
        emb_row_style = "bankrow_%s_button" % emb_family

        # Where the lit segment of the rule under the strip sits. Derived from
        # the mode's position in EMB_MODES so the strip and the underline can
        # never disagree about which button is on.
        emb_mode_i = 0
        for emb_n, emb_m in enumerate(EMB_MODES):
            if emb_m[0] == emb_mode:
                emb_mode_i = emb_n
        emb_mode_x = emb_mode_i * (EMB_MODE_W + EMB_MODE_GAP)

    fixed:
        xysize (EMB_W, EMB_H)

        # =====================================================================
        # THE MODE STRIP -- what the next click does
        # =====================================================================

        for emb_k, (emb_id, emb_caption, emb_fam) in enumerate(EMB_MODES):

            textbutton emb_caption:
                style_prefix ("bankmode_" + emb_fam)
                xpos (emb_k * (EMB_MODE_W + EMB_MODE_GAP))
                ypos 0
                xysize (EMB_MODE_W, EMB_MODE_H)
                action Function(enter_m_bank_ui.set_mode, emb_id)
                selected (emb_mode == emb_id)
                sensitive (not (main_menu and emb_id == "write"))

        text ("%s  %02d / %02d" % (__("FOLIO"), emb_used, len(emb_rows))):
            style "bank_strip_count"
            xpos EMB_W
            xanchor 1.0
            ypos 10

        add Solid(emb_accent + "3a") xysize (EMB_W, 2) ypos EMB_RULE_Y
        add Solid(emb_accent) xysize (EMB_MODE_W, 2) ypos EMB_RULE_Y xpos emb_mode_x

        # =====================================================================
        # THE LIST -- one flat directory of records
        # =====================================================================

        text _("RECORD"):
            style "bank_column_head"
            xpos 12
            ypos 50

        text _("SAVED"):
            style "bank_column_head"
            xpos EMB_ROW_W
            xanchor 1.0
            ypos 50

        vpgrid:
            style_prefix "bank_sv"

            cols 1
            xpos EMB_LIST_X
            ypos EMB_LIST_Y
            xsize EMB_LIST_W
            ysize EMB_LIST_H
            spacing 3
            scrollbars "vertical"
            mousewheel True
            draggable True
            side_yfill True

            for emb_i, emb_name in enumerate(emb_rows):

                $ emb_idx = emb_i + 1
                $ emb_used_row = emb_name in emb_have
                $ emb_title = enter_m_bank_title(emb_name, emb_used_row)
                $ emb_act = enter_m_bank_row_action(emb_mode, emb_name, emb_idx, emb_used_row, emb_src)

                button:
                    style emb_row_style
                    action emb_act
                    hovered Function(enter_m_bank_ui.select, emb_name)
                    sensitive (emb_act is not None)

                    # The button's ONLY child. Hover and idle transform events
                    # reach a button's direct child and stop there; colour
                    # changes go through styles instead, which do recurse.
                    fixed:
                        xysize (EMB_ROW_W, EMB_ROW_H)

                        if emb_name == emb_sel:
                            add Solid(emb_accent) xysize (3, EMB_ROW_H) xpos 0 ypos 0

                        if emb_name == emb_src:
                            add Solid(ROOM_MENU_LAVENDER) xysize (3, EMB_ROW_H) xpos 0 ypos 0

                        text ("%02d" % emb_idx):
                            style ("bank_row_index" if emb_used_row else "bank_row_index_free")
                            xpos 14
                            ypos 9

                        if emb_used_row:

                            text enter_m_bank_short(emb_title, 26):
                                style "bank_row_name"
                                xpos 48
                                ypos 9

                        else:

                            text _("FREE"):
                                style "bank_row_free"
                                xpos 48
                                ypos 10

                        # The right-hand column carries ONE thing. While a copy
                        # is half done the source row says so instead of giving
                        # its timestamp, because both were right-aligned to the
                        # same edge and printed on top of each other.
                        if emb_name == emb_src:

                            text _("SOURCE"):
                                style "bank_row_source"
                                xpos (EMB_ROW_W - 12)
                                xanchor 1.0
                                ypos 11

                        elif emb_used_row:

                            text FileTime(emb_name, format=_("{#file_time}%b %d  %H:%M"), empty="", slot=True):
                                style "bank_row_time"
                                xpos (EMB_ROW_W - 12)
                                xanchor 1.0
                                ypos 11

        # =====================================================================
        # THE RECORD CARD -- the record the pointer is on, full size
        # =====================================================================

        add ROOM_MENU_SELECTOR_IDLE xysize (EMB_MON_W, EMB_MON_H) xpos EMB_MON_X ypos EMB_MON_Y
        add Solid(emb_accent + "c8") xysize (4, EMB_MON_H - 24) xpos (EMB_MON_X + 8) ypos (EMB_MON_Y + 12)

        # A warm hairline gives the stored frame the feel of a photograph laid
        # into a folio rather than a signal trapped behind monitor glass.
        add Solid(ROOM_MENU_PAPER + "38") xysize (EMB_SHOT_W + 4, EMB_SHOT_H + 4) xpos (EMB_SHOT_X - 2) ypos (EMB_SHOT_Y - 2)

        if emb_sel_used:

            add Transform(
                FileScreenshot(emb_sel, slot=True),
                xysize=(EMB_SHOT_W, EMB_SHOT_H),
                fit="cover") xpos EMB_SHOT_X ypos EMB_SHOT_Y at bank_preview_arrive

        else:

            add enter_m_bank_empty_card(EMB_SHOT_W, EMB_SHOT_H) xpos EMB_SHOT_X ypos EMB_SHOT_Y at bank_preview_arrive

            text _("EMPTY SLOT"):
                style "bank_nosignal"
                xpos (EMB_SHOT_X + EMB_SHOT_W // 2)
                xanchor 0.5
                ypos (EMB_SHOT_Y + EMB_SHOT_H // 2 - 12)

        text (enter_m_bank_short(enter_m_bank_title(emb_sel, emb_sel_used), 28) if emb_sel_used else _("SLOT FREE")):
            style ("bank_monitor_title" if emb_sel_used else "bank_monitor_title_free")
            xpos EMB_SHOT_X
            ypos EMB_TITLE_Y

        add enter_m_bank_readout(
            _("SLOT"),
            ("%02d  ::  %s" % (emb_sel_idx, emb_sel)),
            EMB_SHOT_W) xpos EMB_SHOT_X ypos EMB_READ_Y

        add enter_m_bank_readout(
            _("WRITTEN"),
            (FileTime(emb_sel, format=_("{#file_time}%b %d %Y   %H:%M"), empty="--", slot=True) if emb_sel_used else "--"),
            EMB_SHOT_W) xpos EMB_SHOT_X ypos (EMB_READ_Y + EMB_READ_H)

        add enter_m_bank_readout(
            _("IN-GAME"),
            (emb_sel_json.get("em_date") or "--"),
            EMB_SHOT_W) xpos EMB_SHOT_X ypos (EMB_READ_Y + EMB_READ_H * 2)

        add enter_m_bank_readout(
            _("CHAPTER"),
            ("%s" % emb_sel_json["em_chapter"] if "em_chapter" in emb_sel_json else "--"),
            EMB_SHOT_W) xpos EMB_SHOT_X ypos (EMB_READ_Y + EMB_READ_H * 3)

        add enter_m_bank_readout(
            _("PLAYED"),
            (enter_m_bank_runtime(emb_sel_json.get("em_runtime")) or "--"),
            EMB_SHOT_W) xpos EMB_SHOT_X ypos (EMB_READ_Y + EMB_READ_H * 4)

        add Solid(emb_accent + "38") xysize (EMB_SHOT_W, 2) xpos EMB_SHOT_X ypos EMB_FOOT_Y

        # ---------------------------------------------------------------------
        # The foot of the record card is either the instruction for the current
        # mode, or -- while a record is being re-labelled -- the box you type
        # the new name into.
        # ---------------------------------------------------------------------

        if emb_rename:

            frame:
                xpos EMB_SHOT_X
                ypos EMB_HINT_Y
                xysize (EMB_SHOT_W, 34)
                background EMB_SELECTOR_COMPACT_SELECTED
                padding (10, 6, 10, 6)

                fixed:
                    xysize (EMB_SHOT_W - 20, 22)

                    text _("LABEL"):
                        style "bank_readout_key"
                        xpos 0
                        ypos 5

                    add Solid(ROOM_MENU_LAVENDER) xysize (2, 16) xpos 48 ypos 3

                    input:
                        style "bank_input"
                        value EnterMBankLabelValue(emb_rename)
                        length 24
                        exclude "{}[]"
                        xpos 58
                        ypos 2
                        xmaximum 236

                    textbutton _("DONE"):
                        style_prefix "bank_small"
                        xpos (EMB_SHOT_W - 20)
                        xanchor 1.0
                        ypos 0
                        xysize (66, 22)
                        action Function(enter_m_bank_end_rename)

        else:

            text enter_m_bank_hint(emb_mode, emb_src, False):
                style ("bank_hint_wipe" if emb_family == "wipe" else "bank_hint")
                xpos EMB_SHOT_X
                ypos EMB_HINT_Y
                xmaximum EMB_SHOT_W


# =============================================================================
# STYLES
# =============================================================================

style bank_locked_title is room_menu_heading:
    size 24

style bank_locked_hint is room_menu_body:
    size 17
    color ROOM_MENU_MUTED

# --- the mode strip ----------------------------------------------------------

style bankmode_read_button:
    xysize (EMB_MODE_W, EMB_MODE_H)
    padding (6, 4, 6, 4)
    background EMB_SELECTOR_COMPACT_IDLE
    hover_background EMB_SELECTOR_COMPACT_HOVER
    selected_background EMB_SELECTOR_COMPACT_SELECTED
    selected_hover_background EMB_SELECTOR_COMPACT_SELECTED
    insensitive_background EMB_SELECTOR_COMPACT_IDLE
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style bankmode_read_button_text:
    font gui.interface_font
    size 12
    kerning 1.0
    xalign 0.5
    yalign 0.5
    color ROOM_MENU_MUTED
    hover_color "#fff8ea"
    selected_color ROOM_MENU_INK
    insensitive_color "#64716f"
    outlines [(1, "#02050a", 0, 1)]

style bankmode_write_button is bankmode_read_button:
    hover_background EMB_SELECTOR_COMPACT_HOVER
    selected_background EMB_SELECTOR_COMPACT_SELECTED
    selected_hover_background EMB_SELECTOR_COMPACT_SELECTED

style bankmode_write_button_text is bankmode_read_button_text:
    hover_color "#fff2d5"
    selected_color ROOM_MENU_INK

style bankmode_wipe_button is bankmode_read_button:
    hover_background EMB_SELECTOR_COMPACT_DANGER
    selected_background EMB_SELECTOR_COMPACT_DANGER
    selected_hover_background EMB_SELECTOR_COMPACT_DANGER

style bankmode_wipe_button_text is bankmode_read_button_text:
    hover_color "#ffe5df"
    selected_color "#fff1ed"

style bank_strip_count is gui_text:
    font gui.interface_font
    size 11
    kerning 1.4
    color ROOM_MENU_MUTED
    outlines [(1, "#02050a", 0, 1)]

style bank_column_head is gui_text:
    font gui.interface_font
    size 9
    kerning 1.6
    color ROOM_MENU_TEAL
    outlines [(1, "#02050a", 0, 1)]

# --- the list ----------------------------------------------------------------

style bank_sv_vscrollbar:
    xsize 6
    base_bar Frame(Solid("#172126b8"), 0, 0, 0, 0)
    thumb Frame(Solid(ROOM_MENU_TEAL + "b8"), 2, 2, 2, 2)
    unscrollable "hide"

style bank_sv_side:
    spacing 4

# The three row families. Only the background differs: the hue is the mode's,
# so the strip and the row you are about to click always agree about what is
# going to happen to the file under the pointer.
style bankrow_read_button:
    xysize (EMB_ROW_W, EMB_ROW_H)
    padding (0, 0, 0, 0)
    background EMB_SELECTOR_COMPACT_IDLE
    hover_background EMB_SELECTOR_COMPACT_HOVER
    insensitive_background EMB_SELECTOR_COMPACT_IDLE
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style bankrow_write_button is bankrow_read_button:
    hover_background EMB_SELECTOR_COMPACT_HOVER

style bankrow_wipe_button is bankrow_read_button:
    hover_background EMB_SELECTOR_COMPACT_DANGER

style bank_row_index is gui_text:
    font gui.interface_font
    size 13
    color ROOM_MENU_TEAL
    hover_color ROOM_MENU_INK
    insensitive_color "#46514f"
    outlines [(1, "#02050a", 0, 1)]

style bank_row_index_free is bank_row_index:
    color "#53605e"

style bank_row_name is gui_text:
    font gui.default_font
    size 14
    color ROOM_MENU_PAPER
    hover_color "#fff8ea"
    insensitive_color "#596360"
    outlines [(1, "#02050a", 0, 1)]

style bank_row_time is gui_text:
    font gui.interface_font
    size 10
    color ROOM_MENU_MUTED
    hover_color ROOM_MENU_PAPER
    insensitive_color "#4b5553"
    outlines [(1, "#02050a", 0, 1)]

style bank_row_free is gui_text:
    font gui.interface_font
    size 11
    kerning 1.6
    color "#687572"
    hover_color ROOM_MENU_MUTED
    insensitive_color "#46504e"
    outlines [(1, "#02050a", 0, 1)]

style bank_row_source is gui_text:
    font gui.interface_font
    size 10
    kerning 1.4
    color ROOM_MENU_LAVENDER
    hover_color "#e5dcf4"
    outlines [(1, "#02050a", 0, 1)]

# --- the record card ---------------------------------------------------------

style bank_monitor_title is gui_text:
    font gui.default_font
    size 21
    color ROOM_MENU_INK
    outlines [(2, "#02050a", 0, 1)]

style bank_monitor_title_free is bank_monitor_title:
    color "#747e79"
    outlines [(2, "#02050a", 0, 1)]

style bank_nosignal is gui_text:
    font gui.default_font
    size 20
    kerning 1.0
    color ROOM_MENU_MUTED
    outlines [(2, "#02050a", 0, 1)]

style bank_readout_key is gui_text:
    font gui.interface_font
    size 11
    kerning 1.2
    color ROOM_MENU_TEAL
    outlines [(1, "#02050a", 0, 1)]

style bank_readout_value is gui_text:
    font gui.interface_font
    size 13
    color ROOM_MENU_PAPER
    outlines [(1, "#02050a", 0, 1)]

style bank_hint is gui_text:
    font gui.interface_font
    size 11
    kerning 1.0
    line_spacing 4
    color ROOM_MENU_MUTED
    outlines [(1, "#02050a", 0, 1)]

style bank_hint_wipe is bank_hint:
    color ROOM_MENU_CORAL

style bank_input is gui_text:
    font gui.default_font
    size 14
    color "#e9dff8"
    outlines [(1, "#02050a", 0, 1)]

style bank_small_button:
    padding (6, 3, 6, 3)
    background EMB_SELECTOR_COMPACT_SELECTED
    hover_background EMB_SELECTOR_COMPACT_HOVER
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style bank_small_button_text:
    font gui.interface_font
    size 11
    kerning 1.2
    xalign 0.5
    yalign 0.5
    color ROOM_MENU_PAPER
    hover_color "#fff8ea"
    outlines [(1, "#02050a", 0, 1)]
