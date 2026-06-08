################################################################################
# Phone Calls
################################################################################

init -1 python:
    def phone_call_line(sender, body, time=None):
        return {
            "sender": sender,
            "body": body,
            "time": time,
        }

    def phone_call_note(body):
        return phone_call_line("system", body)

    def phone_call_duration_text(visible_count):
        seconds = max(0, visible_count - 1) * 8
        return "{:02d}:{:02d}".format(seconds // 60, seconds % 60)

    def phone_call_date_label(date_label=None):
        text = str(date_label or "").strip()

        if text and ":" not in text:
            return text

        return phone_current_date_label() or ""


screen phone_call_screen(contact_name, status="Calling...", date_label=None, can_decline=True):
    modal True
    zorder 230

    $ _initials = phone_contact_initials(contact_name)
    $ _dismiss_action = Return("dismiss") if can_decline else Return("answer")
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
                xalign 0.5
                ypos 128
                xysize (104, 104)
                background Solid("#2f7dff")
                padding (0, 0)

                text _initials style "phone_call_avatar_text":
                    xalign 0.5
                    yalign 0.5

            text contact_name style "phone_call_contact":
                xalign 0.5
                ypos 256

            text status style "phone_call_status":
                xalign 0.5
                ypos 294

            if can_decline:
                hbox:
                    xalign 0.5
                    ypos 514
                    spacing 54

                    textbutton "Decline":
                        style "phone_call_decline_button"
                        action Return("decline")

                    textbutton "Answer":
                        style "phone_call_answer_button"
                        action Return("answer")
            else:
                text "Tap to answer" style "phone_call_prompt":
                    xalign 0.5
                    ypos 530

            add Solid("#ffffff70"):
                xpos 150
                ypos 627
                xsize 94
                ysize 4

    key "dismiss" action _dismiss_action


screen phone_active_call_screen(contact_name, lines, start_visible_count=1, status="Connected", date_label=None):
    modal True
    zorder 230

    default visible_count = start_visible_count
    default scroll_revision = 1

    $ _initials = phone_contact_initials(contact_name)
    $ _phone_date_label = phone_call_date_label(date_label)
    $ _all_lines = lines or []
    $ _visible_count = min(visible_count, len(_all_lines))
    $ _visible_lines = _all_lines[:_visible_count]
    $ _complete = _visible_count >= len(_all_lines)
    $ _advance_action = Return("end") if _complete else [
        SetScreenVariable("visible_count", _visible_count + 1),
        SetScreenVariable("scroll_revision", scroll_revision + 1),
    ]
    $ _advance_label = "Tap to end call" if _complete else "Tap to continue"

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

            use phone_status_bar(_phone_date_label)

            frame:
                xpos 24
                ypos 72
                xysize (346, 102)
                background Solid("#111827")
                padding (0, 0)

                add Solid("#2c3748"):
                    xpos 0
                    ypos 101
                    xsize 346
                    ysize 1

                frame:
                    xpos 24
                    ypos 18
                    xysize (54, 54)
                    background Solid("#2f7dff")
                    padding (0, 0)

                    text _initials style "phone_active_call_avatar_text":
                        xalign 0.5
                        yalign 0.5

                text contact_name style "phone_active_call_contact":
                    xpos 92
                    ypos 18
                    xmaximum 216

                text status style "phone_active_call_status":
                    xpos 92
                    ypos 50
                    xmaximum 216

            text "Call Transcript" style "phone_active_call_transcript_label":
                xalign 0.5
                ypos 178

            viewport:
                id "phone_active_call_viewport"
                xpos 42
                ypos 204
                xysize (310, 316)
                yinitial 1.0
                mousewheel True

                vbox:
                    spacing 9
                    xfill True

                    for _line in _visible_lines:
                        $ _sender = _line.get("sender", "them")
                        $ _body = _line.get("body", "")
                        $ _time = _line.get("time", None)

                        if _sender == "system":
                            text _body style "phone_active_call_note":
                                xalign 0.5

                        elif _sender == "me":
                            hbox:
                                xfill True

                                null width 42

                                vbox:
                                    spacing 2
                                    xalign 1.0

                                    text "You" style "phone_active_call_speaker_me":
                                        xalign 1.0

                                    frame:
                                        style "phone_active_call_bubble_me"

                                        text _body style "phone_active_call_bubble_me_text"

                                    if _time:
                                        text _time style "phone_active_call_time":
                                            xalign 1.0

                        else:
                            hbox:
                                xfill True

                                vbox:
                                    spacing 2

                                    text contact_name style "phone_active_call_speaker_them"

                                    frame:
                                        style "phone_active_call_bubble_them"

                                        text _body style "phone_active_call_bubble_them_text"

                                    if _time:
                                        text _time style "phone_active_call_time"

                                null width 42

            text _advance_label style "phone_active_call_prompt":
                xalign 0.5
                ypos 552

            add Solid("#ffffff70"):
                xpos 150
                ypos 627
                xsize 94
                ysize 4

    if scroll_revision:
        timer 0.01 action [
            Scroll("phone_active_call_viewport", "vertical increase", 1.0),
            SetScreenVariable("scroll_revision", 0),
        ]

    if renpy.is_skipping():
        timer 0.05 repeat True action _advance_action

    key "dismiss" action _advance_action
    key "skip" action _advance_action


style phone_call_avatar_text:
    font gui.name_font
    size 38
    color "#ffffff"
    bold True
    outlines [(2, "#00000066", 0, 0)]

style phone_call_contact:
    font gui.name_font
    size 30
    color "#f8fafc"
    text_align 0.5
    outlines [(2, "#000000", 0, 0)]

style phone_call_status:
    font gui.interface_font
    size 17
    color "#aab2c0"
    text_align 0.5
    outlines []

style phone_call_prompt:
    font gui.interface_font
    size 15
    color "#a8b3c7"
    bold True
    text_align 0.5
    outlines []

style phone_call_button is button:
    xysize (92, 46)
    padding (0, 0)

style phone_call_button_text is button_text:
    font gui.interface_font
    size 15
    color "#ffffff"
    bold True
    xalign 0.5
    yalign 0.5
    text_align 0.5
    outlines [(1, "#00000066", 0, 0)]

style phone_call_decline_button is phone_call_button:
    background Solid("#c92a3d")
    hover_background Solid("#e13b50")

style phone_call_decline_button_text is phone_call_button_text

style phone_call_answer_button is phone_call_button:
    background Solid("#2a9d55")
    hover_background Solid("#34b967")

style phone_call_answer_button_text is phone_call_button_text

style phone_active_call_avatar_text:
    font gui.name_font
    size 22
    color "#ffffff"
    bold True
    outlines [(1, "#00000066", 0, 0)]

style phone_active_call_contact:
    font gui.name_font
    size 24
    color "#f8fafc"
    bold True
    outlines [(1, "#000000", 0, 0)]

style phone_active_call_status:
    font gui.interface_font
    size 13
    color "#a8b3c7"
    outlines []

style phone_active_call_transcript_label:
    font gui.interface_font
    size 12
    color "#7f8da3"
    bold True
    text_align 0.5
    outlines []

style phone_active_call_note:
    font gui.interface_font
    size 12
    color "#78869c"
    text_align 0.5
    xmaximum 262
    outlines []

style phone_active_call_speaker_me:
    font gui.interface_font
    size 11
    color "#8bbcff"
    bold True
    outlines []

style phone_active_call_speaker_them:
    font gui.interface_font
    size 11
    color "#a8b3c7"
    bold True
    outlines []

style phone_active_call_bubble_me:
    background Solid("#006bea")
    xmaximum 252
    padding (11, 7, 11, 7)

style phone_active_call_bubble_them:
    background Solid("#d7e0ee")
    xmaximum 252
    padding (11, 7, 11, 7)

style phone_active_call_bubble_me_text:
    font gui.default_font
    size 16
    color "#ffffff"
    line_spacing 0
    xmaximum 230
    outlines []

style phone_active_call_bubble_them_text:
    font gui.default_font
    size 16
    color "#0b1020"
    line_spacing 0
    xmaximum 230
    outlines []

style phone_active_call_time:
    font gui.interface_font
    size 10
    color "#6d7890"
    outlines []

style phone_active_call_prompt:
    font gui.interface_font
    size 14
    color "#a8b3c7"
    bold True
    text_align 0.5
    outlines []


label phone_call(contact_name, status="Calling...", clock_text=None, can_decline=True, date_label=None):
    window hide
    play sound phone_open
    $ _phone_call_date_label = phone_call_date_label(date_label)
    call screen phone_call_screen(contact_name, status, _phone_call_date_label, can_decline)
    $ _phone_call_result = _return
    window auto
    return _phone_call_result

label phone_call_conversation(contact_name, lines, status="Connected", clock_text=None, date_label=None):
    window hide
    $ _phone_active_lines = lines or []
    if _phone_active_lines:
        $ _phone_call_date_label = phone_call_date_label(date_label)
        call screen phone_active_call_screen(contact_name, _phone_active_lines, 1, status, _phone_call_date_label)
        $ _phone_call_conversation_result = _return
        window auto
        return _phone_call_conversation_result
    window auto
    return
