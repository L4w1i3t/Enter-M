# =============================================================================
# Phone Video Calls  --  the "FaceTime"-style video-call screen
# =============================================================================
#
# WHAT THIS FILE PROVIDES
#   A video call laid out like the voice call in call.rpy -- handset pushed to
#   the LEFT, the conversation read in the space beside it -- with the contact's
#   own sprite living on the phone's screen as the video feed.
#
# WHAT MAKES IT READ AS A VIDEO CALL
#   A still portrait in a rectangle reads as a photograph. Four cheap, purely
#   ATL touches (no shaders -- see the u_time note in the project memory) turn
#   it into a picture coming down a wire:
#     1. phone_video_handheld : the framing drifts and breathes, because the
#        other end of a video call is somebody's hand, not a tripod.
#     2. phone_video_hitch    : every few seconds the picture twitches and
#        recovers -- the connection dipping.
#     3. phone_video_refresh  : a pale bar crawling down the feed.
#     4. phone_video_flicker  : the exposure hunting slightly, the way a phone
#        camera does indoors.
#   Plus the furniture that sells the frame: a self-view of MC in the corner,
#   a running call clock, and the Mute / End / Cam row.
#
# THE FEED CROP
#   Every sprite in this project is 960 tall (the project's own are
#   Transform(..., fit="contain", xysize=(640, 960)); the DDLC composites are
#   960x960), so the feed just scales by height and shows the top of the sprite
#   -- which is head and shoulders. PHONE_VIDEO_FEED_ZOOM / _HEAD_BIAS are the
#   two knobs if a particular character sits high or low in their canvas.
#
# PUBLIC API (story labels)
#   call phone_video_call(contact, lines=None, sprite=, status=, date_label=)
#       -> plays the conversation if given lines; returns "end" | "dismiss".
#   call phone_facetime(contact, ...) -> alias that forwards to phone_video_call.
#   Lines are the SAME phone_call_line / phone_call_note dicts the voice call
#   uses, so a scene can move between the two without rewriting anything.
#   Mute/Cam are decorative (NullAction); only End/dismiss return.
# =============================================================================

init -2 python:
    # --- feed geometry, inside the phone's 394x668 body ----------------------
    PHONE_VIDEO_FEED_X = 40
    PHONE_VIDEO_FEED_Y = 74
    PHONE_VIDEO_FEED_WIDTH = 314
    PHONE_VIDEO_FEED_HEIGHT = 452

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

# The connection dipping. Applied to the CONTAINER of the feed rather than
# stacked in the same at-list as the drift, so the two never fight over
# transform state (see the at_list/take_state note in the project memory).
transform phone_video_hitch:
    subpixel True
    block:
        pause 5.2
        xoffset 3
        pause 0.05
        xoffset -2
        pause 0.05
        xoffset 0
        pause 7.4
        xoffset -3
        pause 0.05
        yoffset 2
        pause 0.06
        xoffset 0
        yoffset 0
        repeat

# The exposure hunting, the way a phone camera does indoors.
transform phone_video_flicker:
    alpha 0.0
    block:
        ease 2.2 alpha 0.05
        ease 1.7 alpha 0.0
        ease 3.1 alpha 0.04
        ease 2.4 alpha 0.0
        repeat

# A pale bar crawling down the picture.
transform phone_video_refresh(travel=452):
    subpixel True
    block:
        alpha 0.0
        ypos 0
        linear 0.25 alpha 0.30
        linear 2.6 ypos travel
        linear 0.25 alpha 0.0
        pause 3.2
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
    $ _index = min(line_index, _line_total - 1) if _has_lines else 0
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
        screen_fill="#0a0f18",
        status_clock=_phone_date_label,
        device_xalign=PHONE_CALL_DEVICE_XALIGN,
        scrim=PHONE_CALL_SCRIM):

        use phone_video_face(contact_name, _feed_sprite, phone_call_clock(call_seconds), _advance_action)

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
                text "‣" style "phone_call_advance" at phone_call_advance_blink:
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
screen phone_video_face(contact_name, feed_sprite, clock_text, end_action):

    fixed:
        xpos PHONE_VIDEO_FEED_X
        ypos PHONE_VIDEO_FEED_Y
        xysize (PHONE_VIDEO_FEED_WIDTH, PHONE_VIDEO_FEED_HEIGHT)
        at phone_round(18)

        add PhonePanel(PHONE_VIDEO_FEED_WIDTH, PHONE_VIDEO_FEED_HEIGHT, "#161f31", bottom="#0c1220", radius=0)

        if feed_sprite:
            # The viewport is here purely to CLIP: the feed is deliberately
            # bigger than its window and drifts inside it, and a plain fixed
            # would happily let the sprite spill over the phone's bezel.
            viewport:
                xysize (PHONE_VIDEO_FEED_WIDTH, PHONE_VIDEO_FEED_HEIGHT)

                fixed:
                    xysize (PHONE_VIDEO_FEED_WIDTH, PHONE_VIDEO_FEED_HEIGHT)
                    at phone_video_hitch

                    add phone_contact_feed(contact_name, feed_sprite) at phone_video_handheld

            # Exposure hunt, then the refresh bar over the top of everything.
            add Solid("#dbeaff") at phone_video_flicker:
                xysize (PHONE_VIDEO_FEED_WIDTH, PHONE_VIDEO_FEED_HEIGHT)

            add Solid("#bfe0ff") at phone_video_refresh(PHONE_VIDEO_FEED_HEIGHT):
                xysize (PHONE_VIDEO_FEED_WIDTH, 2)

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
        text contact_name style "phone_video_nameplate":
            xpos 14
            ypos PHONE_VIDEO_FEED_HEIGHT - 34
            xmaximum 190

    text clock_text style "phone_video_clock":
        xpos PHONE_VIDEO_FEED_X + 14
        ypos PHONE_VIDEO_FEED_Y + 12

    # --- self-view -----------------------------------------------------------
    fixed:
        xpos 254
        ypos 396
        xysize (86, 112)
        at phone_round(12)

        add PhonePanel(86, 112, "#0d1220", bottom="#070a12", radius=0)

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
    hbox:
        xalign 0.5
        ypos 548
        spacing 18

        textbutton "Mute":
            style "phone_video_tool_button"
            action NullAction()

        textbutton "End":
            style "phone_video_end_button"
            action end_action

        textbutton "Cam":
            style "phone_video_tool_button"
            action NullAction()


# =============================================================================
#  STYLES
# =============================================================================

style phone_video_avatar_text:
    font gui.name_font
    size 38
    color "#ffffff"
    bold True
    outlines [(2, "#00000066", 0, 0)]

style phone_video_status:
    font gui.interface_font
    size 15
    color "#aab2c0"
    text_align 0.5
    outlines []

# Over live picture, so both of these carry a hard outline.
style phone_video_nameplate:
    font gui.interface_font
    size 17
    color "#ffffff"
    bold True
    outlines [(2, "#000000cc", 0, 0)]

style phone_video_clock:
    font gui.interface_font
    size 13
    color "#dbe6f5"
    bold True
    outlines [(2, "#000000cc", 0, 0)]

style phone_video_self_text:
    font gui.interface_font
    size 14
    color "#f8fafc"
    bold True
    outlines [(1, "#000000", 0, 0)]

style phone_video_tool_button is button:
    xysize (66, 44)
    background PhonePanel(66, 44, "#26334a", bottom="#1d2840", radius=14)
    hover_background PhonePanel(66, 44, "#344762", bottom="#283a55", radius=14)
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
    background PhonePanel(66, 44, "#d23b4e", bottom="#b32638", radius=14)
    hover_background PhonePanel(66, 44, "#e8485c", bottom="#c92f43", radius=14)

style phone_video_end_button_text is phone_video_tool_button_text


# =============================================================================
#  PUBLIC LABELS
# =============================================================================

# PUBLIC: show the video-call screen; returns "end" or "dismiss".
#   lines  : optional transcript (phone_call_line/phone_call_note dicts). With
#            none, the call is a tableau the player dismisses.
#   sprite : override the contact's catalog sprite for this call (a different
#            outfit or expression). None uses phone_contact_sprite().
label phone_video_call(contact_name, lines=None, status="Video Call", clock_text=None, date_label=None, sprite=None):
    play sound phone_open
    $ _phone_video_date_label = phone_call_date_label(date_label)
    call screen phone_video_call_screen(contact_name, lines, sprite, status, _phone_video_date_label)
    $ _phone_video_call_result = _return
    return _phone_video_call_result

# PUBLIC ALIAS: same as phone_video_call, friendlier name for story scripts.
label phone_facetime(contact_name, lines=None, status="Video Call", clock_text=None, date_label=None, sprite=None):
    call phone_video_call(contact_name, lines, status, clock_text, date_label, sprite) from _call_phone_video_alias
    return _return
