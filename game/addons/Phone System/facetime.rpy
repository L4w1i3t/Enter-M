################################################################################
# Phone Video Calls
################################################################################

screen phone_video_call_screen(contact_name, status="Video Call", date_label=None):
    modal True
    zorder 230

    $ _initials = phone_contact_initials(contact_name)
    $ _phone_date_label = phone_call_date_label(date_label)

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

            add Solid("#101722"):
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

            use phone_status_bar(_phone_date_label)

            frame:
                xpos 40
                ypos 90
                xysize (314, 408)
                background Solid("#172033")
                padding (0, 0)

                add Solid("#ffffff10"):
                    xpos 0
                    ypos 0
                    xsize 314
                    ysize 408

                frame:
                    xalign 0.5
                    yalign 0.5
                    xysize (112, 112)
                    background Solid("#2f7dff")
                    padding (0, 0)

                    text _initials style "phone_video_avatar_text":
                        xalign 0.5
                        yalign 0.5

                text contact_name style "phone_video_contact":
                    xalign 0.5
                    ypos 292

                text status style "phone_video_status":
                    xalign 0.5
                    ypos 326

            frame:
                xpos 252
                ypos 398
                xysize (84, 84)
                background Solid("#0b0f18")
                padding (0, 0)

                text "YOU" style "phone_video_self_text":
                    xalign 0.5
                    yalign 0.5

            hbox:
                xalign 0.5
                ypos 530
                spacing 18

                textbutton "Mute":
                    style "phone_video_tool_button"
                    action NullAction()

                textbutton "End":
                    style "phone_video_end_button"
                    action Return("end")

                textbutton "Cam":
                    style "phone_video_tool_button"
                    action NullAction()

            add Solid("#ffffff70"):
                xpos 150
                ypos 627
                xsize 94
                ysize 4

    key "dismiss" action Return("dismiss")


style phone_video_avatar_text:
    font gui.name_font
    size 38
    color "#ffffff"
    bold True
    outlines [(2, "#00000066", 0, 0)]

style phone_video_contact:
    font gui.name_font
    size 24
    color "#f8fafc"
    text_align 0.5
    outlines [(2, "#000000", 0, 0)]

style phone_video_status:
    font gui.interface_font
    size 15
    color "#aab2c0"
    text_align 0.5
    outlines []

style phone_video_self_text:
    font gui.interface_font
    size 14
    color "#f8fafc"
    bold True
    outlines [(1, "#000000", 0, 0)]

style phone_video_tool_button is button:
    xysize (64, 42)
    background Solid("#26334a")
    hover_background Solid("#344762")
    padding (0, 0)

style phone_video_tool_button_text is button_text:
    font gui.interface_font
    size 13
    color "#ffffff"
    bold True
    xalign 0.5
    yalign 0.5
    text_align 0.5
    outlines [(1, "#00000066", 0, 0)]

style phone_video_end_button is phone_video_tool_button:
    background Solid("#c92a3d")
    hover_background Solid("#e13b50")

style phone_video_end_button_text is phone_video_tool_button_text


label phone_video_call(contact_name, status="Video Call", clock_text=None, date_label=None):
    window hide
    play sound phone_open
    $ _phone_video_date_label = phone_call_date_label(date_label)
    call screen phone_video_call_screen(contact_name, status, _phone_video_date_label)
    $ _phone_video_call_result = _return
    window auto
    return _phone_video_call_result

label phone_facetime(contact_name, status="Video Call", clock_text=None, date_label=None):
    call phone_video_call(contact_name, status, clock_text, date_label) from _call_phone_video_alias
    return _return
