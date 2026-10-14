# Video calls share voice-call transcript data and the phone chassis.
# phone_video_call(contact, lines=None, sprite=, ...) plays the feed/transcript;
# phone_facetime forwards to it. Continue advances lines; End call follows the last.
# A contact portrait, MC self-view and clock identify the call. PHONE_VIDEO_FEED_ZOOM
# and PHONE_VIDEO_FEED_HEAD_BIAS frame the normalized portrait canvas.

init -2 python:
    # --- feed geometry, inside the phone's 394x668 body ----------------------
    PHONE_VIDEO_FEED_X = 34
    PHONE_VIDEO_FEED_Y = 110
    PHONE_VIDEO_FEED_WIDTH = 326
    PHONE_VIDEO_FEED_HEIGHT = 414

    # How much taller than the feed the scaled sprite is. Bigger = closer crop.
    # 2.1 puts head and shoulders in frame for a standard 960-tall sprite.
    PHONE_VIDEO_FEED_ZOOM = 2.1
    # Fraction of the scaled sprite trimmed off the top, to lose dead canvas
    # above the head without cutting into it.
    PHONE_VIDEO_FEED_HEAD_BIAS = 0.02

    # Native height every sprite in this project is normalised to.
    PHONE_SPRITE_HEIGHT = 960.0

    def phone_video_feed(sprite, feed_height=None, zoom=None, head_bias=None):
        """
        A standing sprite, scaled and offset so the feed window lands on head
        and shoulders. Returns a displayable to be dropped in a clipping
        container (the feed viewport) and animated by phone_video_handheld.
        """
        feed_height = PHONE_VIDEO_FEED_HEIGHT if feed_height is None else feed_height
        zoom = PHONE_VIDEO_FEED_ZOOM if zoom is None else zoom
        head_bias = PHONE_VIDEO_FEED_HEAD_BIAS if head_bias is None else head_bias

        scaled_height = feed_height * float(zoom)

        return Transform(
            sprite,
            zoom=(scaled_height / PHONE_SPRITE_HEIGHT),
            xalign=0.5,
            yalign=0.0,
            yoffset=-int(round(scaled_height * head_bias)),
        )

    def phone_contact_feed(contact_name, sprite, feed_height=None):
        """
        The feed for a contact, honouring the per-contact "feed_zoom" and
        "feed_bias" keys in PHONE_CONTACT_CATALOG. Those exist because the two
        sprite sets in this game are not framed alike: the project's own
        characters nearly fill their 960px canvas, while the DDLC composites
        leave a good deal of room above the head, so a single crop that suits
        one leaves the other looking distant.
        """
        contact = phone_get_contact(contact_name)
        return phone_video_feed(
            sprite,
            feed_height,
            contact.get("feed_zoom"),
            contact.get("feed_bias"),
        )


# =============================================================================
#  FEED ANIMATION
# =============================================================================

# The framing drifts and breathes: somebody is holding the other phone.
transform phone_video_handheld:
    subpixel True
    parallel:
        block:
            ease 3.1 xoffset 5 yoffset -4
            ease 2.6 xoffset -4 yoffset 3
            ease 3.4 xoffset 3 yoffset 4
            ease 2.9 xoffset -5 yoffset -3
            repeat
    parallel:
        block:
            ease 4.3 zoom 1.03
            ease 4.7 zoom 1.0
            repeat

# =============================================================================
#  SCREENS
# =============================================================================

# The video call: handset left with the feed on it, conversation on the right.
# `lines` may be None, in which case the call is a still tableau the player
# dismisses -- the pre-existing behaviour, kept so old call sites still work.
screen phone_video_call_screen(contact_name, lines=None, sprite=None, status="Video Call", date_label=None):
    modal True
    zorder 230

    default line_index = 0
    default call_seconds = 0
    default reveal_chars = 0

    $ _phone_date_label = phone_call_date_label(date_label)
    $ _feed_sprite = sprite if sprite is not None else phone_contact_sprite(contact_name)

    $ _all_lines = lines or []
    $ _line_total = len(_all_lines)
    $ _has_lines = _line_total > 0
    $ _index = max(0, min(line_index, _line_total - 1)) if _has_lines else 0
    $ _line = _all_lines[_index] if _has_lines else None
    $ _sender = _line.get("sender", "them") if _line else "system"
    $ _is_note = (_sender == "system")
    $ _body = phone_emojify(_line.get("body", "")) if _line else ""
    $ _speaker = phone_call_speaker_name(_sender, contact_name)
    $ _body_length = phone_visible_length(_body)
    $ _line_done = (not _has_lines) or reveal_chars >= _body_length
    $ _shown_body = _body if _line_done else phone_reveal_markup(_body, reveal_chars)
    $ _complete = (_index >= _line_total - 1)
    # Same contract as the voice call: finish the line, then move on.
    $ _next_line_action = Return("end") if (_complete or not _has_lines) else [
        SetScreenVariable("line_index", _index + 1),
        SetScreenVariable("reveal_chars", 0),
    ]
    $ _advance_action = _next_line_action if _line_done else SetScreenVariable("reveal_chars", _body_length)

    use phone_device(
        screen_fill="#141820",
        status_clock=_phone_date_label,
        device_xalign=PHONE_CALL_DEVICE_XALIGN if _has_lines else 0.5,
        scrim=PHONE_CALL_SCRIM):

        use phone_video_face(contact_name, _feed_sprite, phone_call_clock(call_seconds), _advance_action, _complete and _line_done, status)

    # --- the conversation, read beside the handset ---------------------------
    if _has_lines:
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
                    text ("[[ " + phone_safe_text(_speaker) + " ]") style "phone_call_speaker_line":
                        xalign 0.5

                    text ("\"" + _shown_body + ("\"" if _line_done else "")) style "phone_call_body_line":
                        xalign 0.5

            if _line_done:
                add phone_ui_icon("chevron", 26, "#cfe0f5") at phone_call_advance_blink:
                    xanchor 1.0
                    xpos PHONE_CALL_TEXT_WIDTH - 44
                    ypos 668

    timer 1.0 repeat True action SetScreenVariable("call_seconds", call_seconds + 1)

    if _has_lines and not _line_done:
        timer PHONE_CALL_REVEAL_TICK repeat True action SetScreenVariable("reveal_chars", reveal_chars + 1)

    if _has_lines and renpy.is_skipping():
        timer 0.05 repeat True action _advance_action

    key "dismiss" action _advance_action
    key "skip" action _advance_action


# The handset's display during a video call: the feed, the name plate over it,
# the self-view, and the controls.
screen phone_video_face(contact_name, feed_sprite, clock_text, advance_action, can_end=False, status="Video Call"):

    hbox:
        xpos PHONE_VIDEO_FEED_X + 6
        ypos 79
        spacing 9

        add phone_ui_icon("video", 18, "#b8c7ef"):
            yalign 0.5

        text phone_safe_text(status) style "phone_video_status":
            xmaximum 290

    fixed:
        xpos PHONE_VIDEO_FEED_X
        ypos PHONE_VIDEO_FEED_Y
        xysize (PHONE_VIDEO_FEED_WIDTH, PHONE_VIDEO_FEED_HEIGHT)
        at phone_round(18)

        add phone_ui_surface("surface"):
            xysize (PHONE_VIDEO_FEED_WIDTH, PHONE_VIDEO_FEED_HEIGHT)

        if feed_sprite:
            # The viewport is here purely to CLIP: the feed is deliberately
            # bigger than its window and drifts inside it, and a plain fixed
            # would happily let the sprite spill over the phone's bezel.
            viewport:
                xysize (PHONE_VIDEO_FEED_WIDTH, PHONE_VIDEO_FEED_HEIGHT)

                fixed:
                    xysize (PHONE_VIDEO_FEED_WIDTH, PHONE_VIDEO_FEED_HEIGHT)
                    add phone_contact_feed(contact_name, feed_sprite) at phone_video_handheld

        else:
            # No sprite on file: an honest "camera off" card rather than a
            # blank rectangle that looks like a bug.
            fixed:
                xalign 0.5
                ypos 132
                xysize (108, 108)

                use phone_avatar(contact_name, 108, "phone_video_avatar_text")

            text "Camera off" style "phone_video_status":
                xalign 0.5
                ypos 262

        # Name plate, bottom-left of the feed the way a call app labels it.
        text phone_safe_text(contact_name) style "phone_video_nameplate":
            xpos 14
            ypos PHONE_VIDEO_FEED_HEIGHT - 34
            xmaximum 190

    text clock_text style "phone_video_clock":
        xpos PHONE_VIDEO_FEED_X + 14
        ypos PHONE_VIDEO_FEED_Y + 12

    # --- self-view -----------------------------------------------------------
    fixed:
        xpos 260
        ypos 396
        xysize (86, 112)
        at phone_round(12)

        add phone_ui_surface("surface"):
            xysize (86, 112)

        # MC is a layered image, so its public attribute string resolves through
        # the normal non-exact image lookup rather than an exact registry key.
        if renpy.has_image("mc neut", exact=False):
            viewport:
                xysize (86, 112)

                # The inner fixed is NOT decoration -- it is what the feed's
                # xalign centres against. A viewport hands its child unlimited
                # width, so an oversized sprite added straight to one has
                # nothing to align to and renders flush left, putting the head
                # against the right edge of the window. Sizing a box first gives
                # xalign something to work with. (Same reason the main feed has
                # one; this is the pair of them.)
                fixed:
                    xysize (86, 112)

                    add phone_video_feed("mc neut", 112) at phone_video_handheld
        else:
            text "YOU" style "phone_video_self_text":
                xalign 0.5
                yalign 0.5

    # --- controls ------------------------------------------------------------
    use phone_call_progress_button(advance_action, can_end, 549)

    text ("Call complete" if can_end else "Click or press Space to continue") style "phone_call_prompt":
        xalign 0.5
        ypos 610


# =============================================================================
#  STYLES
# =============================================================================

style phone_video_avatar_text:
    font PHONE_UI_FONT
    size 38
    color "#ffffff"
    bold True
    outlines [(2, "#00000066", 0, 0)]

style phone_video_status:
    font PHONE_UI_FONT
    size 15
    color "#aab2c0"
    text_align 0.5
    outlines []

# Over live picture, so both of these carry a hard outline.
style phone_video_nameplate:
    font PHONE_UI_FONT
    size 17
    color "#ffffff"
    bold True
    outlines [(2, "#000000cc", 0, 0)]

style phone_video_clock:
    font PHONE_UI_FONT
    size 13
    color "#dbe6f5"
    bold True
    outlines [(2, "#000000cc", 0, 0)]

style phone_video_self_text:
    font PHONE_UI_FONT
    size 14
    color "#f8fafc"
    bold True
    outlines [(1, "#000000", 0, 0)]

# =============================================================================
#  PUBLIC LABELS
# =============================================================================

# PUBLIC: show the video-call screen; returns "end".
#   lines  : optional transcript (phone_call_line/phone_call_note dicts). With
#            none, the call is a tableau the player dismisses.
#   sprite : override the contact's catalog sprite for this call (a different
#            outfit or expression). None uses phone_contact_sprite().
label phone_video_call(contact_name, lines=None, status="Video Call", clock_text=None, date_label=None, sprite=None):
    if audio.phone_open:
        $ renpy.music.play(audio.phone_open, channel="phone_alert", loop=False)
    $ _phone_video_date_label = phone_call_date_label(date_label)
    call screen phone_video_call_screen(contact_name, lines, sprite, status, _phone_video_date_label)
    $ _phone_video_call_result = _return
    return _phone_video_call_result

# PUBLIC ALIAS: same as phone_video_call, friendlier name for story scripts.
label phone_facetime(contact_name, lines=None, status="Video Call", clock_text=None, date_label=None, sprite=None):
    call phone_video_call(contact_name, lines, status, clock_text, date_label, sprite) from _call_phone_video_alias
    return _return
