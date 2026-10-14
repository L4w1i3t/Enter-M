# Archive catalog of the creator's earlier projects.
# RecordsProfile owns title/genre/art/date plus can_play, label_name and variants.
# Playable entries launch a label or offer variant labels; unavailable entries
# retain their catalog slots and explain that restoration is pending.
# lost_records names both the screen and its blocking wrapper label; Show/call
# screen targets the former, while call lost_records enters the latter.

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
            self.label_name = label_name      # standalone label to launch
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

# THE METAPHOR: a shelf of tapes. Each record is a cassette with a paper label
# on its spine; choosing one draws it out of the shelf, and its paper insert
# slides up out of the case on the right.

# Label ink, one per tape in shelf order -- the coloured edge of a spine label.
define LR_LABEL_INK = ("#8a3b3b", "#2c5b59", "#a8803a", "#714966", "#3a4f6b")

# A tape on the shelf: the shelf fills in, a tape slides part-way out under the
# pointer, and the chosen one has been drawn further out. The pull is driven by
# BUTTON STATE (SetScreenVariable reports itself selected), not a parameter, so
# changing the selection never rebuilds a row and replays its entrance -- see
# cs_tab in Side Stories. Offsets stay >= 0: the list is a clipping viewport.
transform lr_record_anim(delay=0.0):
    subpixel True
    alpha 0.0
    xoffset 22
    pause delay
    easeout_quad 0.28 alpha 1.0 xoffset 0
    on idle:
        easeout_quad 0.18 xoffset 0
    on hover:
        easeout_quad 0.14 xoffset 8
    on selected_idle:
        easeout_quad 0.20 xoffset 14
    on selected_hover:
        easeout_quad 0.14 xoffset 14

# The insert slides up out of its case each time the selection changes. `key`
# is unused in the body; a new value is what restarts it.
transform lr_detail_enter(key=0):
    subpixel True
    alpha 0.0
    yoffset 26
    pause 0.05
    parallel:
        easeout_quad 0.34 yoffset 0
    parallel:
        easeout_quad 0.22 alpha 1.0

# =============================================================================
# LOST RECORDS SCREEN
# selected_idx (screen-local) tracks which record's insert is shown on the right.
# =============================================================================
screen lost_records():
    modal True

    default selected_idx = 0

    use archive_backdrop

    key "game_menu" action Hide("lost_records", transition=enter_m_menu_doorway)
    key "K_ESCAPE" action Hide("lost_records", transition=enter_m_menu_doorway)

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

            use archive_header("LOST RECORDS", Hide("lost_records", transition=enter_m_menu_doorway))

            use archive_readout(
                "THE TAPE SHELF / {} OF {} RECORDS RESTORED".format(_lr_restored, _lr_total),
                "{} ON THE SHELF".format(_lr_total))

            hbox:
                spacing 0

                # --- LEFT: the shelf of tapes -----------------------------
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
                                    button:
                                        style "lr_tape_button"
                                        at lr_record_anim(idx * 0.05)
                                        action SetScreenVariable("selected_idx", idx)

                                        # Tape geometry matches tape_spine.svg: the
                                        # case window is (10, 12, 62, 64), the label
                                        # x 82..339 with ruled lines at y 44 and 61.
                                        fixed:
                                            xysize (350, 88)

                                            add "assets/gui/menu/illustrated/archive/tape_spine.svg"
                                            add Solid(LR_LABEL_INK[idx % len(LR_LABEL_INK)]) xpos 82 ypos 9 xysize (7, 69)
                                            add Transform(record.thumbnail_path, fit="contain", xysize=(56, 58)) xpos 13 ypos 15

                                            text record.title style "lr_record_name" xpos 98 ypos 12
                                            text record.genre.upper() style "lr_record_meta" xpos 98 ypos 48
                                            text record.display_date.upper() style "lr_record_date" xpos 98 ypos 65

                                            if record.playable:
                                                text "RESTORED" style "lr_record_restored" xanchor 1.0 xpos 332 ypos 65
                            else:
                                # Empty-catalog state.
                                text "No records found." style "lr_empty_text":
                                    xalign 0.5
                                    yalign 0.5

                add Solid("#02050a66"):
                    xsize 2
                    ysize 520

                # --- RIGHT: the selected tape's insert --------------------
                frame:
                    xsize 748
                    ysize 520
                    style "archive_panel"
                    padding (24, 22)

                    if lost_records:
                        $ _sel_record = lost_records[selected_idx]

                        # Keyed on selected_idx: the insert slides up afresh
                        # each time a different tape is drawn.
                        vbox:
                            spacing 16
                            at lr_detail_enter(selected_idx)

                            frame:
                                style "lr_insert"

                                fixed:
                                    xysize (660, 212)

                                    # The cover, printed on the insert's front panel.
                                    add Solid("#1e2226") xysize (220, 196) ypos 0
                                    add Transform(_sel_record.thumbnail_path, fit="contain", xysize=(204, 180)) xpos 8 ypos 8

                                    add Solid(LR_LABEL_INK[selected_idx % len(LR_LABEL_INK)]) xpos 240 ypos 0 xysize (6, 196)

                                    vbox:
                                        xpos 262
                                        ypos 2
                                        spacing 8
                                        xmaximum 396

                                        text "LOST RECORD / NO. {:02d}".format(selected_idx + 1) style "lr_insert_kicker"
                                        text _sel_record.title style "lr_detail_title"
                                        text _sel_record.genre.upper() style "lr_detail_genre"

                                        null height 4

                                        hbox:
                                            spacing 10
                                            text "RECORDED" style "lr_detail_label" yalign 0.5
                                            text _sel_record.display_date style "lr_detail_value" yalign 0.5

                                        # Restored vs. not: a REC lamp, lit or dark.
                                        hbox:
                                            spacing 8
                                            add Solid("#c0392b" if _sel_record.playable else "#a39a92") xysize (8, 8) yalign 0.5
                                            text ("RESTORED" if _sel_record.playable else "NOT RESTORED"):
                                                style ("lr_status_on" if _sel_record.playable else "lr_status_off")
                                                yalign 0.5

                            # The liner notes, on the case itself.
                            vbox:
                                spacing 8

                                hbox:
                                    spacing 10
                                    add Solid(IM_PLUM) xysize (6, 6) rotate 45 yalign 0.5
                                    text "LINER NOTES" style "lr_section_title" yalign 0.5

                                if _sel_record.playable and _sel_record.variants:
                                    text "This record has multiple restored versions. Choose which playback to open." style "lr_body_text"
                                elif _sel_record.playable:
                                    text "This record has been restored and is ready for playback." style "lr_body_text"
                                else:
                                    text "This record has been indexed for the archive. Playback will become available once its story file is restored." style "lr_body_text"

                            # Open playable records in a clean game store; otherwise
                            # leave the Archive in place and explain the lock.
                            if _sel_record.playable:
                                if _sel_record.variants:
                                    hbox:
                                        spacing 12

                                        for _variant_title, _variant_label in _sel_record.variants:
                                            textbutton _variant_title:
                                                style "lr_open_button"
                                                action Function(archive_start_isolated_content, _variant_label)
                                else:
                                    textbutton "Play Record":
                                        style "lr_open_button"
                                        action Function(archive_start_isolated_content, _sel_record.label_name)
                            else:
                                textbutton "Unavailable":
                                    style "lr_open_button_disabled"
                                    action Show("dialog", message="This record has not been restored yet.", ok_action=Hide("dialog"))

                    else:
                        text "No records found." style "lr_empty_text":
                            xalign 0.5
                            yalign 0.5

    # Engraved corners framing the shell (cohesion with the archive hub).
    use archive_shell_brackets()

# Blocking-call entry point (story/script use). The Show() in archive.rpy uses
# the screen directly; this label wraps it as `call screen` + return.
label lost_records:
    call screen lost_records
    return

# =============================================================================
# STYLES  -- ink on paper labels and inserts, paper ink on the dark case
# =============================================================================
style lr_tape_button:
    xysize (350, 88)
    padding (0, 0)
    background None
    hover_background None
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style lr_record_name is gui_text:
    font gui.default_font
    size 19
    color IM_INK
    outlines []

style lr_record_meta is gui_text:
    font gui.interface_font
    size 9
    kerning 1.4
    color "#6c5f66"
    outlines []

style lr_record_date is lr_record_meta

style lr_record_restored is lr_record_meta:
    color "#2c5b59"

style lr_insert is frame:
    background IM_PAPER_PANEL
    xsize 700
    ysize 248
    padding (20, 18)

style lr_insert_kicker is lr_record_meta:
    size 10
    kerning 2.0
    color "#714966"

style lr_detail_title is gui_text:
    font gui.default_font
    size 30
    color IM_INK
    outlines []

style lr_detail_genre is lr_record_meta:
    size 11
    kerning 1.6

style lr_detail_label is lr_record_meta:
    size 10
    kerning 1.6
    color "#7a6472"

style lr_detail_value is gui_text:
    font gui.default_font
    size 17
    color "#2f3a3d"
    outlines []

style lr_status_on is lr_record_meta:
    size 10
    color "#2c5b59"

style lr_status_off is lr_record_meta:
    size 10
    color "#8f8580"

style lr_section_title is archive_meta_text:
    kerning 3.0

style lr_body_text is gui_text:
    font gui.default_font
    size 17
    color "#d4cdbf"
    line_spacing 4
    xmaximum 690
    outlines []

style lr_empty_text is gui_text:
    font gui.default_font
    size 20
    color IM_MUTED
    outlines []

style lr_open_button:
    xysize (200, 46)
    background IM_TAB_IDLE
    hover_background IM_TAB_HOVER
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (14, 10)

style lr_open_button_text:
    font gui.interface_font
    color IM_PAPER
    hover_color "#ffffff"
    size 18
    xalign 0.5
    text_align 0.5
    outlines []

style lr_open_button_disabled is lr_open_button:
    hover_background IM_TAB_IDLE

style lr_open_button_disabled_text is lr_open_button_text:
    color "#8f8a86"
    hover_color "#a9a39c"
