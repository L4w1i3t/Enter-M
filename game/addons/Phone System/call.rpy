# Voice calls on the shared phone chassis.
# phone_call(contact, ...) returns answer/decline/dismiss from the ringing screen;
# phone_call_conversation(contact, lines, ...) advances the connected transcript.
# Build lines with phone_call_line(sender, body, time=) or phone_call_note(body).
# The ringing handset is centered; connected calls move left beside the transcript.
# Contact/date helpers are shared with text.rpy, transcript data with facetime.rpy.

init -2 python:
    # --- side-by-side call layout --------------------------------------------
    # The handset is pushed to the left edge and the conversation is read in the
    # space beside it. xalign is a fraction of the LEFTOVER width, so on a 1280
    # screen a 394-wide device at 0.10 sits with its left edge at ~89px and its
    # right edge at ~483 -- which is where the text column starts.
    PHONE_CALL_DEVICE_XALIGN = 0.10
    PHONE_CALL_TEXT_X = 516
    PHONE_CALL_TEXT_WIDTH = 1280 - PHONE_CALL_TEXT_X - 24

    # Lighter than the centred apps' wash: during a call the scene behind is
    # still half the picture, not a backdrop to be blotted out.
    PHONE_CALL_SCRIM = "#0000009e"


init -1 python:
    import store

    # --- line-by-line reveal --------------------------------------------------
    # Spoken lines are typed out rather than dropped in whole, so a call reads at
    # the same pace as the rest of the game's dialogue. One click completes the
    # line in progress; the next moves on -- the standard VN contract.
    #
    # The reveal counts VISIBLE characters and steps over {...} tags whole, so an
    # emoji that phone_emojify turned into {image=emoji_1f44d} appears in one go
    # instead of being sliced down the middle into a parse error.
    PHONE_CALL_REVEAL_TICK = 0.025   # seconds per revealed character (~40 cps)

    def _phone_walk_markup(markup):
        # Yield (chunk, counts_as_a_character) over Matsu'Py text markup.
        #
        # BOTH kinds of bracket come out whole. A tag cut down the middle is a
        # parse error, and so is a cut interpolation -- revealing "[player]" one
        # character at a time would hand Matsu'Py "[play", which is not a typo on
        # screen, it is a crash. Names arrive in one piece instead.
        index, length = 0, len(markup)
        while index < length:
            pair = markup[index:index + 2]
            if pair in ("{{", "[["):
                yield pair, True                       # an escaped literal bracket
                index += 2
            elif markup[index] == "{":
                close = markup.find("}", index)
                if close == -1:
                    yield markup[index:], True
                    return
                chunk = markup[index:close + 1]
                # Inline images occupy one visible character. Treating them
                # as formatting made an emoji appear before its reveal tick.
                yield chunk, chunk.startswith("{image=")
                index = close + 1
            elif markup[index] == "[":
                # Interpolation can contain nested indexing and quoted closing
                # brackets, such as [people[0].name] or [names['a]b']]. A first-
                # closing-bracket search would reveal an invalid expression.
                close, depth, quote = index + 1, 1, None
                while close < length and depth:
                    character = markup[close]
                    if quote:
                        if character == "\\":
                            close += 2
                            continue
                        if character == quote:
                            quote = None
                    elif character in ("'", '"'):
                        quote = character
                    elif character == "[":
                        depth += 1
                    elif character == "]":
                        depth -= 1
                    close += 1
                if depth:
                    yield markup[index:], True
                    return
                yield markup[index:close], True        # an interpolation: whole
                index = close
            else:
                yield markup[index], True
                index += 1

    def phone_visible_length(markup):
        return sum(1 for _chunk, counts in _phone_walk_markup(markup or "") if counts)

    def phone_reveal_markup(markup, count):
        # The first `count` visible characters of `markup`, tags kept intact.
        # Ren'Py closes formatting tags at the end of a text block, so a
        # partially revealed emphasis span is valid as well.
        if not markup:
            return ""
        shown, out = 0, []
        for chunk, counts in _phone_walk_markup(markup):
            if counts:
                if shown >= count:
                    break
                shown += 1
            out.append(chunk)
        return "".join(out)

    def phone_call_clock(seconds):
        # Call duration as MM:SS (HH:MM:SS once a call runs past an hour).
        seconds = max(0, int(seconds))
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        return "{:02d}:{:02d}".format(minutes, seconds)

    def phone_call_speaker_name(sender, contact_name):
        # Who to put in the brackets. The player's own lines are attributed to
        # him by name when the story has one, which is what makes the right-hand
        # column read like a conversation rather than a log of "You:" entries.
        if sender == "me":
            return getattr(store, "player", None) or "You"
        return contact_name

    # A transcript line: {sender, body, time}. phone_call_note = a centered
    # "system" line (e.g. "Call connected").
    def phone_call_line(sender, body, time=None):
        return {
            "sender": sender,
            "body": body,
            "time": time,
        }

    def phone_call_note(body):
        return phone_call_line("system", body)

    def phone_call_date_label(date_label=None):
        text = str(date_label or "").strip()

        if text and ":" not in text:
            return text

        return phone_current_date_label() or ""


# Incoming-call screen: avatar, name, status, and an explicit Answer button.
# Optional calls also expose Decline. Returns via Return("...").
screen phone_call_screen(contact_name, status="Calling...", date_label=None, can_decline=True):
    modal True
    zorder 230

    $ _dismiss_action = Return("dismiss") if can_decline else Return("answer")
    $ _phone_date_label = phone_call_date_label(date_label)

    use phone_device(screen_fill="#141820", status_clock=_phone_date_label):

        text "INCOMING CALL" style "phone_call_eyebrow":
            xalign 0.5
            ypos 94

        fixed:
            xalign 0.5
            ypos 157
            xysize (116, 116)

            use phone_avatar(contact_name, 116, "phone_call_avatar_text")

        text phone_safe_text(contact_name) style "phone_call_contact":
            xalign 0.5
            ypos 302
            xmaximum 302

        text phone_safe_text(status) style "phone_call_status":
            xalign 0.5
            ypos 349
            xmaximum 302

        hbox:
            xalign 0.5
            ypos 497
            spacing 22

            if can_decline:
                button:
                    id "phone_call_decline"
                    style "phone_call_decline_button"
                    action Return("decline")
                    alt "Decline call"
                    hbox:
                        xalign 0.5
                        yalign 0.5
                        spacing 8
                        add phone_ui_icon("call_end", 20) yalign 0.5
                        text "Decline" style "phone_call_button_text"

            button:
                id "phone_call_answer"
                style "phone_call_answer_button"
                action Return("answer")
                alt "Answer call"
                hbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 8
                    add phone_ui_icon("phone", 20) yalign 0.5
                    text "Answer" style "phone_call_button_text"

        text "Tap Answer to connect" style "phone_call_prompt":
            xalign 0.5
            ypos 573

    key "dismiss" action _dismiss_action


# =============================================================================
# ACTIVE CALL  --  handset on the left, conversation read on the right
# =============================================================================
# The transcript used to live INSIDE the phone: a 310x316 viewport that a
# fifty-line call had to be scrolled through at four words a line, while the
# rest of the screen sat empty. It is now laid out the way the call actually
# divides -- the handset is pushed to the left edge and shows what a phone
# shows during a call (who, how long, and a reading control), and the
# talking happens beside it at reading size, one line at a time like any other
# conversation in the game.
#
# The scene behind stays visible through a light scrim, because during a call
# the player is still standing wherever the story left him.
#
# `lines` is unchanged -- the same phone_call_line/phone_call_note dicts, so no
# story script needs editing. "system" lines print centered and unattributed;
# everyone else gets a bracketed speaker and their line in quotes.
screen phone_active_call_screen(contact_name, lines, start_line_index=0, status="Connected", date_label=None):
    modal True
    zorder 230

    default line_index = start_line_index
    default call_seconds = 0
    default reveal_chars = 0

    $ _phone_date_label = phone_call_date_label(date_label)
    $ _all_lines = lines or []
    $ _line_total = len(_all_lines)
    $ _index = max(0, min(line_index, _line_total - 1)) if _line_total else 0
    $ _line = _all_lines[_index] if _line_total else None
    $ _sender = _line.get("sender", "them") if _line else "system"
    $ _is_note = (_sender == "system")
    $ _body = phone_emojify(_line.get("body", "")) if _line else ""
    $ _speaker = phone_call_speaker_name(_sender, contact_name)
    $ _body_length = phone_visible_length(_body)
    $ _line_done = reveal_chars >= _body_length
    $ _shown_body = _body if _line_done else phone_reveal_markup(_body, reveal_chars)
    $ _complete = (_index >= _line_total - 1)
    # One click finishes the line being spoken; the next one moves on.
    $ _next_line_action = Return("end") if _complete else [
        SetScreenVariable("line_index", _index + 1),
        SetScreenVariable("reveal_chars", 0),
    ]
    $ _advance_action = _next_line_action if _line_done else SetScreenVariable("reveal_chars", _body_length)

    use phone_device(
        screen_fill="#141820",
        status_clock=_phone_date_label,
        device_xalign=PHONE_CALL_DEVICE_XALIGN,
        scrim=PHONE_CALL_SCRIM):

        use phone_in_call_face(contact_name, phone_call_clock(call_seconds), _advance_action, _complete and _line_done, status)

    # --- the conversation, read beside the handset ---------------------------
    fixed:
        xpos PHONE_CALL_TEXT_X
        ypos 0
        xysize (PHONE_CALL_TEXT_WIDTH, 720)

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 18
            xmaximum PHONE_CALL_TEXT_WIDTH - 60

            if _is_note:
                text _shown_body style "phone_call_note_line":
                    xalign 0.5
            else:
                # "[[" is an escaped literal bracket -- a bare "[" would open a
                # Matsu'Py interpolation and eat the speaker's name.
                text ("[[ " + phone_safe_text(_speaker) + " ]") style "phone_call_speaker_line":
                    xalign 0.5

                # The closing quote is held back until the line finishes, so a
                # half-spoken line does not look like a complete short one.
                text ("\"" + _shown_body + ("\"" if _line_done else "")) style "phone_call_body_line":
                    xalign 0.5

        # Advance chevron, bottom right, exactly where the say screen puts one.
        # Only once there is nothing left to say.
        if _line_done:
            add phone_ui_icon("chevron", 26, "#cfe0f5") at phone_call_advance_blink:
                xanchor 1.0
                xpos PHONE_CALL_TEXT_WIDTH - 44
                ypos 668

    # The call clock. Ticks in real seconds, so a long call reads long.
    timer 1.0 repeat True action SetScreenVariable("call_seconds", call_seconds + 1)

    if not _line_done:
        timer PHONE_CALL_REVEAL_TICK repeat True action SetScreenVariable("reveal_chars", reveal_chars + 1)

    if renpy.is_skipping():
        timer 0.05 repeat True action _advance_action

    key "dismiss" action _advance_action
    key "skip" action _advance_action


# The handset follows the transcript's actual action: Continue while there is
# more to read, End call once the last line has finished revealing.
screen phone_in_call_face(contact_name, clock_text, advance_action, can_end=False, status="Connected"):

    text "VOICE CALL" style "phone_call_eyebrow":
        xalign 0.5
        ypos 96

    text phone_safe_text(contact_name) style "phone_in_call_contact":
        xalign 0.5
        ypos 145
        xmaximum 302

    hbox:
        xalign 0.5
        ypos 190
        spacing 10

        add phone_ui_icon("phone", 16, "#a9bdf5"):
            yalign 0.5

        text (phone_safe_text(status) + "  ·  " + clock_text) style "phone_in_call_clock":
            xmaximum 272

    fixed:
        xalign 0.5
        ypos 265
        xysize (132, 132)

        use phone_avatar(contact_name, 132, "phone_call_avatar_text")

    text ("Call complete" if can_end else "Conversation in progress") style "phone_call_prompt":
        xalign 0.5
        ypos 451

    use phone_call_progress_button(advance_action, can_end, 504)

    text ("Ready to hang up" if can_end else "Click or press Space to continue") style "phone_call_prompt":
        xalign 0.5
        ypos 574


screen phone_call_progress_button(advance_action, can_end=False, button_y=548):
    button:
        id "phone_call_progress"
        style "phone_call_progress_button"
        xalign 0.5
        ypos button_y
        background phone_ui_surface("call_end" if can_end else "outgoing")
        hover_background phone_ui_surface("call_end_hover" if can_end else "surface_hover")
        action advance_action

        hbox:
            xalign 0.5
            yalign 0.5
            spacing 12

            add phone_ui_icon("call_end" if can_end else "chevron", 22, "#ffffff"):
                yalign 0.5

            text ("End call" if can_end else "Continue") style "phone_call_button_text"



transform phone_call_advance_blink:
    alpha 1.0
    block:
        easeout 0.6 alpha 0.25
        easein 0.6 alpha 1.0
        repeat


style phone_call_avatar_text:
    font PHONE_UI_FONT
    size 38
    color "#ffffff"
    bold True
    outlines [(2, "#00000066", 0, 0)]

style phone_call_contact:
    font PHONE_UI_FONT
    size 29
    color "#f8fafc"
    text_align 0.5
    outlines []

style phone_call_status:
    font PHONE_UI_FONT
    size 16
    color "#bcc4d4"
    text_align 0.5
    outlines []

style phone_call_prompt:
    font PHONE_UI_FONT
    size 12
    color "#aeb8ca"
    text_align 0.5
    outlines []

style phone_call_eyebrow is phone_call_prompt:
    size 12
    color "#b8c7ef"
    kerning 1.5

style phone_call_button is button:
    xysize (132, 54)
    padding (0, 0)

style phone_call_button_text is button_text:
    font PHONE_UI_FONT
    size 15
    color "#ffffff"
    bold True
    xalign 0.5
    yalign 0.5
    text_align 0.5
    outlines []

style phone_call_decline_button is phone_call_button:
    background phone_ui_surface("call_end")
    hover_background phone_ui_surface("call_end_hover")

style phone_call_decline_button_text is phone_call_button_text

style phone_call_answer_button is phone_call_button:
    background phone_ui_surface("call_accept")
    hover_background phone_ui_surface("call_accept_hover")

style phone_call_answer_button_text is phone_call_button_text

# --- the handset's in-call display ------------------------------------------

style phone_in_call_contact:
    font PHONE_UI_FONT
    size 27
    color "#f8fafc"
    text_align 0.5
    outlines []

style phone_in_call_clock:
    font PHONE_UI_FONT
    size 14
    color "#94a1b8"
    text_align 0.5
    outlines []

style phone_call_progress_button is button:
    xysize (184, 52)
    padding (0, 0)
    background None
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

# --- the conversation, beside the handset -----------------------------------
# Sized to be read from across a room, not squinted at inside a 310px viewport.

style phone_call_speaker_line:
    font gui.name_font
    size 25
    color "#dfe8f5"
    text_align 0.5
    outlines [(2, "#000000", 0, 0)]

style phone_call_body_line:
    font gui.default_font
    size 27
    color "#ffffff"
    text_align 0.5
    line_spacing 4
    outlines [(2, "#000000", 0, 0)]

style phone_call_note_line:
    font gui.interface_font
    size 19
    color "#9aa8bf"
    text_align 0.5
    italic True
    outlines [(2, "#000000", 0, 0)]

# PUBLIC: show the incoming-call screen; returns "answer"/"decline"/"dismiss".
label phone_call(contact_name, status="Calling...", clock_text=None, can_decline=True, date_label=None):
    $ _phone_call_date_label = phone_call_date_label(date_label)
    # Ring on the dedicated looping channel until the player answers/declines.
    $ renpy.music.play(audio.phone_ringtone, channel="phone_ring", loop=True)
    call screen phone_call_screen(contact_name, status, _phone_call_date_label, can_decline)
    $ renpy.music.stop(channel="phone_ring")
    $ _phone_call_result = _return
    return _phone_call_result

# PUBLIC: play a call transcript (no-op if `lines` is empty); returns "end".
label phone_call_conversation(contact_name, lines, status="Connected", clock_text=None, date_label=None):
    $ _phone_active_lines = lines or []
    if _phone_active_lines:
        $ _phone_call_date_label = phone_call_date_label(date_label)
        call screen phone_active_call_screen(contact_name, _phone_active_lines, start_line_index=0, status=status, date_label=_phone_call_date_label)
        $ _phone_call_conversation_result = _return
        return _phone_call_conversation_result
    return
