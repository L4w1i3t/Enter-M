################################################################################
# Phone Model
################################################################################

# Shared visual construction for the in-story phone. The message/call apps live in
# neighboring files and reuse these dimensions so the model stays consistent.

define audio.phone_text_in = None
define audio.phone_text_out = None
define audio.phone_open = None

init -2 python:
    PHONE_MODEL_WIDTH = 394
    PHONE_MODEL_HEIGHT = 668
    PHONE_SCREEN_X = 13
    PHONE_SCREEN_Y = 18
    PHONE_SCREEN_WIDTH = 368
    PHONE_SCREEN_HEIGHT = 632
    PHONE_SAFE_LEFT = 28
    PHONE_SAFE_TOP = 26

    def phone_contact_initials(name):
        parts = [p for p in name.replace("_", " ").split() if p]
        if not parts:
            return "?"
        if len(parts) == 1:
            return parts[0][0].upper()
        return (parts[0][0] + parts[1][0]).upper()

transform phone_model_enter:
    on show:
        alpha 0.0
        yoffset 34
        zoom 0.985
        easeout_quad 0.22 alpha 1.0 yoffset 0 zoom 1.0
    on hide:
        alpha 1.0
        yoffset 0
        easein_quad 0.14 alpha 0.0 yoffset 18

transform phone_soft_blink:
    alpha 0.30
    linear 0.9 alpha 0.62
    linear 0.9 alpha 0.30
    repeat


screen phone_home_screen(title="Phone", subtitle=None):
    modal True
    zorder 220

    add Solid("#00000099")

    frame:
        style "phone_model_body"
        at phone_model_enter

        fixed:
            xysize (PHONE_MODEL_WIDTH, PHONE_MODEL_HEIGHT)

            use phone_side_keys

            add Solid("#05070b"):
                xpos PHONE_SCREEN_X
                ypos PHONE_SCREEN_Y
                xsize PHONE_SCREEN_WIDTH
                ysize PHONE_SCREEN_HEIGHT

            add Solid("#0b1220"):
                xpos 24
                ypos 30
                xsize 346
                ysize 596

            add Solid("#05070b"):
                xpos 190
                ypos 37
                xsize 12
                ysize 12

            add Solid("#30394a"):
                xpos 162
                ypos 618
                xsize 70
                ysize 3

            use phone_status_bar("21:12")

            text title style "phone_home_title":
                xalign 0.5
                ypos 88

            if subtitle:
                text subtitle style "phone_home_subtitle":
                    xalign 0.5
                    ypos 126

            grid 2 2:
                xpos 78
                ypos 210
                spacing 28

                use phone_app_icon("MSG", "Messages", "#2f7dff")
                use phone_app_icon("CAL", "Calendar", "#cc2233")
                use phone_app_icon("CON", "Contacts", "#25a66a")
                use phone_app_icon("TEL", "Calls", "#41b65b")

            add Solid("#ffffff70"):
                xpos 150
                ypos 627
                xsize 94
                ysize 4

    key "dismiss" action Return()


screen phone_side_keys():
    add Solid("#131a26"):
        xpos 389
        ypos 128
        xsize 5
        ysize 78

    add Solid("#131a26"):
        xpos 389
        ypos 224
        xsize 5
        ysize 48

    add Solid("#131a26"):
        xpos 0
        ypos 176
        xsize 5
        ysize 92


screen phone_status_bar(clock_text="21:12", dark=False):
    $ _phone_status_style = "phone_status_dark_text" if dark else "phone_status_text"
    $ _phone_status_color = "#101722" if dark else "#f8fafc"
    $ _phone_status_dim = "#10172288" if dark else "#f8fafc88"
    $ _phone_battery_cutout = "#f5f7fb" if dark else "#101722"

    fixed:
        xpos 31
        ypos 47
        xysize (332, 24)

        text clock_text style _phone_status_style:
            xpos 0
            yalign 0.5

        hbox:
            xalign 1.0
            yalign 0.5
            spacing 5

            text "LTE" style _phone_status_style

            hbox:
                spacing 2
                yalign 0.5
                add Solid(_phone_status_color):
                    xsize 3
                    ysize 5
                    yalign 1.0
                add Solid(_phone_status_color):
                    xsize 3
                    ysize 8
                    yalign 1.0
                add Solid(_phone_status_color):
                    xsize 3
                    ysize 11
                    yalign 1.0
                add Solid(_phone_status_dim):
                    xsize 3
                    ysize 14
                    yalign 1.0

            frame:
                xysize (22, 11)
                background Solid(_phone_status_color)
                padding (2, 2, 2, 2)

                add Solid(_phone_battery_cutout):
                    xsize 13
                    ysize 7
                    xalign 0.0
                    yalign 0.5


screen phone_app_icon(short_label, label, color):
    fixed:
        xysize (92, 104)

        frame:
            xalign 0.5
            xysize (58, 58)
            background Solid(color)
            padding (0, 0)

            text short_label style "phone_app_icon_text":
                xalign 0.5
                yalign 0.5

        text label style "phone_app_label":
            xalign 0.5
            ypos 67


style phone_model_body is empty:
    xalign 0.5
    yalign 0.5
    xysize (394, 668)
    background Solid("#01030a")
    padding (0, 0)

style phone_status_text:
    font gui.interface_font
    size 13
    color "#f8fafc"
    bold True
    outlines []

style phone_status_dark_text is phone_status_text:
    color "#101722"

style phone_home_title:
    font gui.name_font
    size 31
    color "#f8fafc"
    text_align 0.5
    outlines [(2, "#000000", 0, 0)]

style phone_home_subtitle:
    font gui.interface_font
    size 16
    color "#aab2c0"
    text_align 0.5
    outlines []

style phone_app_icon_text:
    font gui.name_font
    size 17
    color "#ffffff"
    bold True
    text_align 0.5
    outlines [(1, "#00000066", 0, 0)]

style phone_app_label:
    font gui.interface_font
    size 14
    color "#e6edf7"
    text_align 0.5
    outlines [(1, "#000000", 0, 0)]


label phone_home(title="Phone", subtitle=None):
    window hide
    play sound phone_open
    call screen phone_home_screen(title, subtitle)
    window auto
    return
