# =============================================================================
# Phone Calls  --  INCOMING-CALL + ACTIVE-CALL TRANSCRIPT screens
# =============================================================================
#
# WHAT THIS FILE PROVIDES
#   The voice-call half of the phone: a ringing/incoming screen (answer/decline)
#   and an active-call screen that plays the conversation line-by-line. Builds on
#   the shared chassis (phone_model_construct.rpy) and reuses helpers from
#   text.rpy (phone_contact_initials, phone_current_date_label).
#
# LAYOUT
#   The RINGING screen is centred -- a phone going off is the only thing
#   happening. Once the call connects the handset moves to the LEFT edge and the
#   conversation is read in the space beside it, one line at a time, over the
#   scene the player is still standing in. See phone_active_call_screen.
#
# PUBLIC API (story labels)
#   call phone_call(contact, status=, can_decline=, date_label=)
#       -> shows the incoming-call screen; returns "answer" | "decline" | "dismiss".
#   call phone_call_conversation(contact, lines, status=, date_label=)
#       -> plays a transcript (tap to advance); returns "end" (or nothing if empty).
#   Line builders: phone_call_line(sender, body, time=), phone_call_note(body)
#       [sender is "me" | "them" | "system"].
#   (See docs/addons/ADDON_CHEATSHEET.md for usage; not used in s1 story yet.)
# =============================================================================

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
                yield markup[index:close + 1], False   # a tag: whole, uncounted
                index = close + 1
            elif markup[index] == "[":
                close = markup.find("]", index)
                if close == -1:
                    yield markup[index:], True
                    return
                yield markup[index:close + 1], True    # an interpolation: whole
                index = close + 1
            else:
                yield markup[index], True
                index += 1

    def phone_visible_length(markup):
        return sum(1 for _chunk, counts in _phone_walk_markup(markup or "") if counts)

    def phone_reveal_markup(markup, count):
        # The first `count` visible characters of `markup`, tags kept intact.
        # (Phone bodies only ever carry self-closing {image=...} tags, so there
        # is never an open tag left dangling by cutting here.)
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


# Incoming-call screen: big avatar + name + status, and either Answer/Decline
# buttons (can_decline) or a "tap to answer" prompt. Returns via Return("...").
screen phone_call_screen(contact_name, status="Calling...", date_label=None, can_decline=True):
    modal True
    zorder 230

    $ _dismiss_action = Return("dismiss") if can_decline else Return("answer")
    $ _phone_date_label = phone_call_date_label(date_label)

    use phone_device(screen_fill="#101722", status_clock=_phone_date_label):

        fixed:
            xalign 0.5
            ypos 128
            xysize (104, 104)

            use phone_avatar(contact_name, 104, "phone_call_avatar_text")

        text contact_name style "phone_call_contact":
            xalign 0.5
            ypos 256

        text status style "phone_call_status":
            xalign 0.5
            ypos 294

        if can_decline:
            hbox:
                xalign 0.5
                ypos 510
                spacing 50

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

    key "dismiss" action _dismiss_action


# =============================================================================
# ACTIVE CALL  --  handset on the left, conversation read on the right
# =============================================================================
# The transcript used to live INSIDE the phone: a 310x316 viewport that a
# fifty-line call had to be scrolled through at four words a line, while the
# rest of the screen sat empty. It is now laid out the way the call actually
# divides -- the handset is pushed to the left edge and shows what a phone
# shows during a call (who, how long, and the button that ends it), and the
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
    $ _index = min(line_index, _line_total - 1) if _line_total else 0
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
        screen_fill="#101722",
        status_clock=_phone_date_label,
        device_xalign=PHONE_CALL_DEVICE_XALIGN,
        scrim=PHONE_CALL_SCRIM):

        use phone_in_call_face(contact_name, phone_call_clock(call_seconds), _advance_action)

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
            text "‣" style "phone_call_advance" at phone_call_advance_blink:
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


# The handset's own display during a call: who you are talking to, how long it
# has been, and the button that hangs up. Deliberately NOT the transcript --
# that is what the right-hand side of the screen is for.
screen phone_in_call_face(contact_name, clock_text, end_action):

    text contact_name style "phone_in_call_contact":
        xalign 0.5
        ypos 118
        xmaximum 300

    text clock_text style "phone_in_call_clock":
        xalign 0.5
        ypos 152

    fixed:
        xalign 0.5
        ypos 226
        xysize (132, 132)

        use phone_avatar(contact_name, 132, "phone_call_avatar_text")

    button:
        style "phone_hangup_button"
        xalign 0.5
        ypos 497
        action end_action

        fixed:
            xysize (58, 58)

            add PhonePanel(58, 58, "#f4566b", bottom="#d3283f", radius=29)

            fixed:
                xysize (30, 30)
                xalign 0.5
                yalign 0.5
                at phone_hangup_tilt

                use phone_handset_glyph("#ffffff")


# A telephone handset drawn out of three rounded plates: the grip and the two
# bells. Tilted by phone_hangup_tilt at the call site, which is what turns it
# from "call" into "hang up".
screen phone_handset_glyph(color="#ffffff"):
    # Grip along the top, earpiece and mouthpiece hanging off it at the ends.
    #
    # THE ONE THING THAT MATTERS: the two bells flare to ONE SIDE of the grip
    # only -- the side that goes against your face. Centre them on the grip so
    # they stand out above and below equally and the silhouette stops being a
    # telephone and becomes a dumbbell.
    add PhonePanel(24, 6, color, radius=3):
        xpos 3
        ypos 5
    add PhonePanel(11, 14, color, radius=4):
        xpos 0
        ypos 5
    add PhonePanel(11, 14, color, radius=4):
        xpos 19
        ypos 5


# rotate_pad keeps the tilted glyph from being cropped by its own box.
#
# 225 is not arbitrary -- it is the only tilt at which this silhouette reads as
# a telephone. Compared side by side at 4x: flat it is a staple, and at the
# 133/135 the hang-up icon conventionally uses it turns into a tick mark. The
# red disc behind it is what says "end"; the glyph only has to say "phone".
transform phone_hangup_tilt:
    subpixel True
    rotate_pad True
    rotate 225

transform phone_call_advance_blink:
    alpha 1.0
    block:
        easeout 0.6 alpha 0.25
        easein 0.6 alpha 1.0
        repeat


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
    xysize (112, 50)
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
    background PhonePanel(112, 50, "#d23b4e", bottom="#b32638", radius=25)
    hover_background PhonePanel(112, 50, "#e8485c", bottom="#c92f43", radius=25)

style phone_call_decline_button_text is phone_call_button_text

style phone_call_answer_button is phone_call_button:
    background PhonePanel(112, 50, "#34b869", bottom="#1f9b51", radius=25)
    hover_background PhonePanel(112, 50, "#42cc78", bottom="#2aae5e", radius=25)

style phone_call_answer_button_text is phone_call_button_text

# --- the handset's in-call display ------------------------------------------

style phone_in_call_contact:
    font gui.name_font
    size 27
    color "#f8fafc"
    text_align 0.5
    outlines [(2, "#000000", 0, 0)]

style phone_in_call_clock:
    font gui.interface_font
    size 14
    color "#94a1b8"
    text_align 0.5
    outlines []

style phone_hangup_button is button:
    xysize (58, 58)
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

# The advance arrow is U+2023 (TRIANGULAR BULLET) in the INTERFACE font, and
# that pairing is not a matter of taste -- it is the only combination in the
# project that draws. Measured against all three fonts: every U+25Bx arrow
# (25B6/25B8/25BA/25B7) is a tofu box in ALL of them, and the default dialogue
# font (Myanmar) has no arrow glyph whatsoever. NovaSquare renders 2023 as the
# solid right-pointing triangle we actually want. Change either half of this
# and you get a hollow rectangle.
style phone_call_advance:
    font gui.interface_font
    size 26
    color "#cfe0f5"
    outlines [(2, "#000000", 0, 0)]


# PUBLIC: show the incoming-call screen; returns "answer"/"decline"/"dismiss".
label phone_call(contact_name, status="Calling...", clock_text=None, can_decline=True, date_label=None):
    $ _phone_call_date_label = phone_call_date_label(date_label)
    # Ring on the dedicated looping channel until the player answers/declines.
    $ renpy.music.play(audio.phone_ringtone, channel="phone_ring", loop=False)
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
