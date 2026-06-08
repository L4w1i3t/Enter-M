# Lost Records addon
# A catalog of stories that span the creator's history.

init python:
    import datetime

    class RecordsProfile:
        def __init__(self, title, genre, thumbnail=None, creation_date=None, can_play=False, label_name=None):
            self.title = title
            self.genre = genre
            self.thumbnail = thumbnail
            self.creation_date = creation_date
            self.can_play = can_play
            self.label_name = label_name

        @property
        def display_date(self):
            return convert_to_date(self.creation_date)

        @property
        def playable(self):
            return self.can_play and bool(self.label_name)

        @property
        def thumbnail_path(self):
            return self.thumbnail or "mod_assets/dump/icon_placeholder.png"

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

init 5 python:
    init_lost_records()

transform lr_record_anim(delay=0.0):
    alpha 0.0
    xoffset -18
    subpixel True
    pause delay
    easein_quad 0.28 alpha 1.0 xoffset 0

transform lr_detail_enter:
    alpha 0.0
    xoffset 22
    subpixel True
    pause 0.12
    easeout_quad 0.32 alpha 1.0 xoffset 0

screen lost_records():
    modal True

    default selected_idx = 0

    use archive_backdrop

    key "game_menu" action Hide("lost_records")
    key "K_ESCAPE" action Hide("lost_records")

    frame:
        style "archive_shell_frame"
        padding (24, 20)
        at archive_frame_enter

        vbox:
            spacing 14

            use archive_header("LOST RECORDS", Hide("lost_records"))

            add Solid("#56d7ff66"):
                xsize 1150
                ysize 2
                xalign 0.5

            hbox:
                spacing 0

                frame:
                    xsize 420
                    ysize 556
                    style "archive_sidebar_panel"
                    padding (14, 16)

                    viewport:
                        style_prefix "archive_sv"
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        xsize 392
                        ysize 524

                        vbox:
                            spacing 8

                            if lost_records:
                                for idx, record in enumerate(lost_records):
                                    $ _record_delay = idx * 0.05

                                    button:
                                        xfill True
                                        ysize 92
                                        padding (10, 8)
                                        hover_sound gui.hover_sound
                                        activate_sound gui.activate_sound
                                        at lr_record_anim(_record_delay)

                                        if idx == selected_idx:
                                            background Solid("#12314af2")
                                            hover_background Solid("#17415fee")
                                        else:
                                            background Solid("#07111dcc")
                                            hover_background Solid("#12314aee")

                                        action SetScreenVariable("selected_idx", idx)

                                        hbox:
                                            spacing 12
                                            yalign 0.5

                                            frame:
                                                xsize 64
                                                ysize 64
                                                background Solid("#07101add")
                                                padding (3, 3)

                                                add record.thumbnail_path:
                                                    fit "contain"
                                                    xalign 0.5
                                                    yalign 0.5

                                            vbox:
                                                spacing 4
                                                yalign 0.5
                                                xsize 286

                                                text record.title style "lr_record_name"
                                                text record.genre style "lr_record_meta"
                                                text record.display_date style "lr_record_date"
                            else:
                                text "No records found." style "lr_empty_text":
                                    xalign 0.5
                                    yalign 0.5

                add Solid("#56d7ff44"):
                    xsize 2
                    ysize 556

                frame:
                    xsize 730
                    ysize 556
                    style "archive_panel"
                    padding (24, 24)
                    at lr_detail_enter

                    if lost_records:
                        $ _sel_record = lost_records[selected_idx]

                        vbox:
                            spacing 18

                            hbox:
                                spacing 22

                                frame:
                                    xsize 220
                                    ysize 180
                                    background Solid("#07101add")
                                    padding (8, 8)

                                    add _sel_record.thumbnail_path:
                                        fit "contain"
                                        xalign 0.5
                                        yalign 0.5

                                vbox:
                                    spacing 10
                                    yalign 0.5
                                    xsize 426

                                    text _sel_record.title style "lr_detail_title"
                                    text _sel_record.genre style "lr_detail_genre"

                                    hbox:
                                        spacing 8
                                        text "CREATED" style "lr_detail_label"
                                        text _sel_record.display_date style "lr_detail_value"

                                    if _sel_record.playable:
                                        text "RESTORED" style "lr_status_ready"
                                    else:
                                        text "NOT RESTORED" style "lr_status_locked"

                            add Solid("#56d7ff22"):
                                xsize 682
                                ysize 1

                            frame:
                                xfill True
                                ysize 190
                                background Solid("#050811cc")
                                padding (24, 20)

                                vbox:
                                    spacing 10
                                    yalign 0.5

                                    text "ARCHIVE ENTRY" style "lr_section_title"
                                    text "This record has been indexed for the archive. Playback will become available once its story file is restored." style "lr_body_text"

                            null height 4

                            if _sel_record.playable:
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

label lost_records:
    call screen lost_records
    return

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
