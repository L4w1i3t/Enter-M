# =============================================================================
# lost_records.rpy  --  LOST RECORDS (archive feature)
# =============================================================================
#
# WHAT THIS FILE PROVIDES
#   An in-universe catalog of the creator's older/"lost" DDLC projects, presented
#   as recoverable archive entries. Left = scrollable list of records; right =
#   detail panel for the selected record with an "Open Record" button that (when
#   the record is marked playable) launches a story label.
#
# HOW IT IS REACHED
#   - Archive "Lost Records" card -> Show("lost_records")  (see game/archive.rpy).
#   - Also available as a blocking `call screen` via the `lost_records` label
#     at the bottom of this file.
#   NOTE: the screen and the label are BOTH named "lost_records" (Matsu'Py allows a
#   screen and a label to share a name; `Show(...)`/`call screen` target the
#   screen, `call lost_records`/`Start` targets the label).
#
# DATA MODEL (built once by init_lost_records(); see init 5 python)
#   lost_records = [ RecordsProfile(...) , ... ]
#   RecordsProfile fields:
#     title, genre, thumbnail, creation_date ("MMYYYY" or "MMDDYYYY" string),
#     can_play (bool), label_name (story label to Start when opened),
#     variants (optional list of (button text, story label) tuples).
#   Computed props:
#     display_date  -> human date via convert_to_date()
#     playable      -> can_play AND a label_name or variants are set
#     thumbnail_path-> the thumbnail or a placeholder fallback
#
#   Records default to can_play=False, so they show "NOT RESTORED" and the Open
#   button raises the "not restored yet" dialog. To make one playable, pass
#   can_play=True and either label_name="some_label" or variants=[(...), ...].
#
# SHARED THEME BORROWED FROM game/archive.rpy
#   - screen archive_backdrop, screen archive_header(...)
#   - styles archive_shell_frame / archive_sidebar_panel / archive_panel
#   - transform archive_frame_enter; viewport style_prefix "archive_sv"
#   - generic "dialog" screen (unavailable popup)
# =============================================================================

# Lost Records addon
# A catalog of stories that span the creator's history.

init python:
    import datetime

    # One catalogued (possibly not-yet-restored) project.
    class RecordsProfile:
        def __init__(self, title, genre, thumbnail=None, creation_date=None, can_play=False, label_name=None, variants=None):
            self.title = title
            self.genre = genre
            self.thumbnail = thumbnail
            self.creation_date = creation_date
            self.can_play = can_play          # has its story file been "restored"?
            self.label_name = label_name      # label to Start() when opened
            self.variants = variants or []    # optional alternate playable versions

        # Human-readable creation date (delegates to convert_to_date below).
        @property
        def display_date(self):
            return convert_to_date(self.creation_date)

        # Only truly openable if flagged playable AND at least one target label is set.
        @property
        def playable(self):
            return self.can_play and (bool(self.label_name) or bool(self.variants))

        # Falls back to a placeholder image when no thumbnail is supplied.
        @property
        def thumbnail_path(self):
            return self.thumbnail or "assets/dump/icon_placeholder.png"

    # The catalog the screen renders. Rebuilt at init (see init 5 python below).
    lost_records = []

    def init_lost_records():
        global lost_records
        lost_records = [
            RecordsProfile(
                "The Answer",
                "Psychological Horror/Mystery",
                thumbnail="lost_records/The Answer/ta_logo.png",
                creation_date="052022",
            ),
            RecordsProfile(
                "SVHS TAP-05052022",
                "Psychological Horror",
                thumbnail="lost_records/SVHS TAP-05052022/svhs_logo.png",
                creation_date="022022",
            ),
            RecordsProfile(
                "Mika: A DDLC Short Story",
                "Slice-of-Life",
                thumbnail="lost_records/Mika/nothumbnail.png",
                creation_date="082021",
                # can_play=True,
                # variants=[
                #     ("Original Record", "ch_mika"),
                #     #("Rewritten Record", "ch_mika_rewrite"),
                # ],
            ),
            RecordsProfile(
                "Doki Doki Funni Club",
                "Sketch Humor",
                thumbnail="lost_records/DDFC/ddfc_logo.png",
                creation_date="102021",
            ),
            RecordsProfile(
                "DDLC: Lost Media",
                "Psychological Horror",
                thumbnail="lost_records/DDLM/nothumbnail.png",
                creation_date="062022",
            ),
        ]

    # Parse a compact date string into a pretty label. Accepts two widths:
    #   6 chars  = "MMYYYY"    -> "Month YYYY"        (e.g. "052022" -> "May 2022")
    #   8 chars  = "MMDDYYYY"  -> "Month DD, YYYY"
    # Anything empty/malformed/out-of-range returns "Unknown".
    def convert_to_date(creation_date):
        if not creation_date:
            return "Unknown"

        creation_date = str(creation_date)

        try:
            # MMYYYY format
            if len(creation_date) == 6:
                month = int(creation_date[:2])
                year = int(creation_date[2:])

                return datetime.datetime(year, month, 1).strftime("%B %Y")

            # MMDDYYYY format
            if len(creation_date) == 8:
                month = int(creation_date[:2])
                day = int(creation_date[2:4])
                year = int(creation_date[4:])

                return datetime.datetime(year, month, day).strftime("%B %d, %Y")
        except ValueError:
            pass

        return "Unknown"

# init 5 so the catalog is built after RecordsProfile is defined.
init 5 python:
    init_lost_records()

# Shell entrance/exit, matching the other archive sub-screens.
# Entry stagger (list rows slide in from the left), with a small hover slide so
# rows feel selectable (mirrors the Side Stories sidebar rows).
transform lr_record_anim(delay=0.0):
    subpixel True
    alpha 0.0
    xoffset -18
    pause delay
    easein_quad 0.28 alpha 1.0 xoffset 0
    on idle:
        easeout 0.16 xoffset 0
    on hover:
        easeout 0.14 xoffset 6

# Detail panel re-entrance. Keyed on the selected record so it replays each time
# the selection changes (the panel content slides in fresh).
transform lr_detail_enter:
    alpha 0.0
    xoffset 22
    subpixel True
    pause 0.05
    easeout_quad 0.30 alpha 1.0 xoffset 0

# =============================================================================
# LOST RECORDS SCREEN
# selected_idx (screen-local) tracks which record's detail is shown on the right.
# =============================================================================
screen lost_records():
    modal True

    default selected_idx = 0

    use archive_backdrop

    key "game_menu" action Hide("lost_records")
    key "K_ESCAPE" action Hide("lost_records")

    # Keyboard navigation through the record list (QoL: browse without the mouse).
    if len(lost_records) > 1:
        key "K_UP" action SetScreenVariable("selected_idx", (selected_idx - 1) % len(lost_records))
        key "K_DOWN" action SetScreenVariable("selected_idx", (selected_idx + 1) % len(lost_records))

    # Live census for the readout strip.
    $ _lr_total = len(lost_records)
    $ _lr_restored = sum(1 for _r in lost_records if _r.playable)

    frame:
        style "archive_shell_frame"
        padding (24, 20)
        at archive_frame_enter(50, 0.5, 30)

        vbox:
            spacing 12

            use archive_header("LOST RECORDS", Hide("lost_records"))

            # Census / readout strip (shared with the archive hub + Side Stories).
            use archive_readout(
                "SALVAGE ARCHIVE // {}/{} RECORDS RESTORED".format(_lr_restored, _lr_total),
                "ENTRIES {}".format(_lr_total))

            hbox:
                spacing 0

                # --- LEFT: scrollable record list -------------------------
                frame:
                    xsize 400
                    ysize 520
                    style "archive_sidebar_panel"
                    padding (14, 16)

                    viewport:
                        style_prefix "archive_sv"
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        xsize 372
                        ysize 488

                        vbox:
                            spacing 8

                            if lost_records:
                                for idx, record in enumerate(lost_records):
                                    $ _record_delay = idx * 0.05
                                    $ _lr_sel = (idx == selected_idx)

                                    button:
                                        xfill True
                                        ysize 108
                                        padding (0, 0)
                                        hover_sound gui.hover_sound
                                        activate_sound gui.activate_sound
                                        at lr_record_anim(_record_delay)
                                        action SetScreenVariable("selected_idx", idx)

                                        # Highlight the selected row.
                                        if _lr_sel:
                                            background Solid("#12314af2")
                                            hover_background Solid("#17415fee")
                                        else:
                                            background Solid("#07111dcc")
                                            hover_background Solid("#12314aee")

                                        hbox:
                                            spacing 0
                                            yfill True

                                            # Selection accent rail (pulses when active).
                                            if _lr_sel:
                                                add Solid("#56d7ff") xysize (4, 108) at enter_m_pip_pulse
                                            else:
                                                add Solid("#0c1a27") xysize (4, 108)

                                            hbox:
                                                spacing 12
                                                yalign 0.5
                                                xoffset 10

                                                frame:
                                                    xsize 64
                                                    ysize 64
                                                    yalign 0.5
                                                    background Solid("#07101add")
                                                    padding (3, 3)

                                                    add record.thumbnail_path:
                                                        fit "contain"
                                                        xalign 0.5
                                                        yalign 0.5

                                                vbox:
                                                    spacing 4
                                                    yalign 0.5
                                                    xsize 268

                                                    text record.title style "lr_record_name"
                                                    text record.genre style "lr_record_meta"

                                                    # Date + a live restored/indexed pip.
                                                    hbox:
                                                        spacing 8
                                                        yalign 0.5

                                                        if record.playable:
                                                            add Solid("#56d7ff") xysize (6, 6) yalign 0.5 at console_blink
                                                        else:
                                                            add Solid("#374654") xysize (6, 6) yalign 0.5
                                                        text record.display_date style "lr_record_date"
                            else:
                                # Empty-catalog state.
                                text "No records found." style "lr_empty_text":
                                    xalign 0.5
                                    yalign 0.5

                add Solid("#56d7ff44"):
                    xsize 2
                    ysize 520

                # --- RIGHT: detail panel for the selected record ----------
                frame:
                    xsize 748
                    ysize 520
                    style "archive_panel"
                    padding (24, 22)

                    if lost_records:
                        $ _sel_record = lost_records[selected_idx]

                        # `at` keyed on selected_idx: the whole dossier re-enters
                        # each time the selection changes.
                        vbox:
                            spacing 16
                            at lr_detail_enter

                            hbox:
                                spacing 22

                                # Shared framed portrait window (scanline + rules).
                                use archive_portrait(_sel_record.thumbnail_path, 210, 172, "contain", False)

                                vbox:
                                    spacing 10
                                    yalign 0.5
                                    xsize 456

                                    hbox:
                                        spacing 10
                                        yalign 0.5
                                        add Solid("#56d7ff") xysize (9, 9) yalign 0.5 at console_blink
                                        text _sel_record.title style "lr_detail_title"

                                    text _sel_record.genre style "lr_detail_genre"

                                    hbox:
                                        spacing 8
                                        yalign 0.5
                                        text "CREATED" style "lr_detail_label"
                                        text _sel_record.display_date style "lr_detail_value"

                                    null height 2

                                    # Restored vs. not-restored status chip.
                                    if _sel_record.playable:
                                        frame:
                                            background Solid("#56d7ff")
                                            padding (14, 6)
                                            text "RESTORED" style "archive_chip_on_text"
                                    else:
                                        frame:
                                            background Solid("#1b2832")
                                            padding (14, 6)
                                            text "NOT RESTORED" style "archive_chip_off_text"

                            add Solid("#56d7ff22"):
                                xsize 700
                                ysize 1

                            frame:
                                xfill True
                                ysize 176
                                background Solid("#050811cc")
                                padding (24, 20)

                                vbox:
                                    spacing 10
                                    yalign 0.5

                                    hbox:
                                        spacing 10
                                        yalign 0.5
                                        add Solid("#56d7ff") xysize (4, 22) yalign 0.5
                                        text "ARCHIVE ENTRY" style "lr_section_title"

                                    if _sel_record.playable and _sel_record.variants:
                                        text "This record has multiple restored versions. Choose which playback to open." style "lr_body_text"
                                    elif _sel_record.playable:
                                        text "This record has been restored and is ready for playback." style "lr_body_text"
                                    else:
                                        text "This record has been indexed for the archive. Playback will become available once its story file is restored." style "lr_body_text"

                            null height 2

                            # Open if playable (Start the label); else show dialog.
                            if _sel_record.playable:
                                if _sel_record.variants:
                                    hbox:
                                        spacing 12

                                        for _variant_title, _variant_label in _sel_record.variants:
                                            textbutton _variant_title:
                                                style "lr_open_button"
                                                action Start(_variant_label)
                                else:
                                    textbutton "Open Record":
                                        style "lr_open_button"
                                        action Start(_sel_record.label_name)
                            else:
                                textbutton "Unavailable":
                                    style "lr_open_button_disabled"
                                    action Show("dialog", message="This record has not been restored yet.", ok_action=Hide("dialog"))

                    else:
                        text "No records found." style "lr_empty_text":
                            xalign 0.5
                            yalign 0.5

    # Console brackets framing the shell (cohesion with the archive hub).
    use archive_shell_brackets()

# Blocking-call entry point (story/script use). The Show() in archive.rpy uses
# the screen directly; this label wraps it as `call screen` + return.
label lost_records:
    call screen lost_records
    return

# =============================================================================
# STYLES  (same cyan-on-near-black archive palette)
# =============================================================================
style lr_record_name:
    font gui.interface_font
    color "#dff8ff"
    size 20
    bold True
    outlines [(1, "#02040b", 0, 0)]

style lr_record_meta:
    font gui.interface_font
    color "#9fc9d6"
    size 13
    outlines [(1, "#02040b", 0, 0)]

style lr_record_date:
    font gui.interface_font
    color "#56d7ff"
    size 12
    bold True
    outlines [(1, "#02040b", 0, 0)]

style lr_detail_title:
    font gui.interface_font
    color "#f4fbff"
    size 30
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style lr_detail_genre:
    font gui.interface_font
    color "#9fc9d6"
    size 16
    outlines [(1, "#02040b", 0, 0)]

style lr_detail_label:
    font gui.interface_font
    color "#56d7ff"
    size 13
    bold True
    outlines [(1, "#02040b", 0, 0)]

style lr_detail_value:
    font gui.interface_font
    color "#dff8ff"
    size 14
    outlines [(1, "#02040b", 0, 0)]

style lr_status_ready:
    font gui.interface_font
    color "#56d7ff"
    size 14
    bold True
    outlines [(1, "#02040b", 0, 0)]

style lr_status_locked:
    font gui.interface_font
    color "#4f5b67"
    size 14
    bold True
    outlines [(1, "#02040b", 0, 0)]

style lr_section_title:
    font gui.interface_font
    color "#f4fbff"
    size 18
    bold True
    outlines [(1, "#02040b", 0, 0)]

style lr_body_text:
    font gui.interface_font
    color "#9fc9d6"
    size 16
    line_spacing 3
    outlines [(1, "#02040b", 0, 0)]

style lr_empty_text:
    font gui.interface_font
    color "#687787"
    size 20
    bold True
    outlines [(1, "#02040b", 0, 0)]

style lr_open_button:
    xysize (180, 46)
    background Solid("#07111dcc")
    hover_background Solid("#12314af2")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (14, 10)

style lr_open_button_text:
    font gui.interface_font
    color "#dff8ff"
    hover_color "#ffffff"
    size 20
    bold True
    xalign 0.5
    text_align 0.5
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style lr_open_button_disabled is lr_open_button:
    background Solid("#050811cc")
    hover_background Solid("#07111dcc")

style lr_open_button_disabled_text is lr_open_button_text:
    color "#4f5b67"
    hover_color "#687787"
