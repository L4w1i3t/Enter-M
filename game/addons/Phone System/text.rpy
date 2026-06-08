################################################################################
# Phone Texting
################################################################################

init -1 python:
    import re
    import store

    def phone_msg(sender, body, time=None, kind="text"):
        return {
            "sender": sender,
            "body": body,
            "time": time,
            "kind": kind,
        }

    def phone_thumb(sender="them", time=None):
        return phone_msg(sender, "", time, "thumb")

    def phone_note(body):
        return {
            "sender": "system",
            "body": body,
            "time": None,
            "kind": "note",
        }

    def phone_date_note(date_label):
        return {
            "sender": "system",
            "body": date_label,
            "time": None,
            "kind": "date",
        }

    def phone_message_sound(messages):
        if not messages:
            return None #no phone sfx for now

        sender = messages[-1].get("sender", "them")
        if sender == "me":
            return None
        if sender == "system":
            return None
        return None

    def phone_safe_text(value):
        return str(value or "").replace("[", "[[")

    def phone_compact_text(value, max_length=32):
        text = re.sub(r"\s+", " ", str(value or "")).strip()

        if len(text) > max_length:
            text = text[:max_length - 3].rstrip() + "..."

        return phone_safe_text(text)

    def phone_clock_from_timestamp(timestamp):
        if not timestamp:
            return "--:--"

        parts = timestamp.split()
        if len(parts) < 3:
            return "--:--"

        time_text = parts[-2]
        period = parts[-1].upper()

        if ":" not in time_text or period not in ("AM", "PM"):
            return "--:--"

        try:
            hour_text, minute_text = time_text.split(":", 1)
            hour = int(hour_text)
            minute = int(minute_text)
        except Exception:
            return "--:--"

        if period == "PM" and hour != 12:
            hour += 12
        elif period == "AM" and hour == 12:
            hour = 0

        return "{:02d}:{:02d}".format(hour, minute)

    def phone_current_date_label():
        calendar_obj = getattr(store, "calendar", None)

        if calendar_obj is not None:
            try:
                snapshot = calendar_obj.get_snapshot()
                return "{}, {} {}".format(
                    snapshot["dow_short"].title(),
                    snapshot["month_short"].title(),
                    snapshot["day"],
                )
            except Exception:
                pass

        return None

    def phone_status_text(timestamp=None, clock_text=None):
        if clock_text:
            return clock_text
        if timestamp:
            return timestamp
        return phone_current_date_label() or ""

    PHONE_CONTACT_ORDER = [
        "monika",
        "mom",
        "asahina",
        "matsuda",
    ]

    PHONE_CONTACT_CATALOG = {
        "monika": {
            "id": "monika",
            "name": "Monika",
            "subtitle": "Club",
            "status": "Messages",
        },
        "mom": {
            "id": "mom",
            "name": "Mom",
            "subtitle": "Family",
            "status": "Messages",
        },
        "asahina": {
            "id": "asahina",
            "name": "Asa",
            "subtitle": "Family",
            "status": "Messages",
        },
        "matsuda": {
            "id": "matsuda",
            "name": "Matsuda Akai",
            "subtitle": "New Contact",
            "status": "Messages",
        },
    }

    PHONE_CONTACT_ALIASES = {
        "monika": "monika",
        "mom": "mom",
        "himeko": "mom",
        "asahina": "asahina",
        "asa": "asahina",
        "matsuda": "matsuda",
        "matsuda akai": "matsuda",
    }

    def phone_state_list(name):
        value = getattr(store, name, None)
        if value is None:
            value = []
            setattr(store, name, value)
        return value

    def phone_state_dict(name):
        value = getattr(store, name, None)
        if value is None:
            value = {}
            setattr(store, name, value)
        return value

    def phone_clone_messages(messages):
        cloned = []
        for message in messages or []:
            cloned.append({
                "sender": message.get("sender", "them"),
                "body": message.get("body", ""),
                "time": message.get("time", None),
                "kind": message.get("kind", "text"),
            })
        return cloned

    def phone_message_signature(message):
        return (
            message.get("sender", "them"),
            message.get("body", ""),
            message.get("time", None),
            message.get("kind", "text"),
        )

    def phone_messages_are_prefix(prefix, messages):
        if len(prefix) > len(messages):
            return False

        for index, message in enumerate(prefix):
            if phone_message_signature(message) != phone_message_signature(messages[index]):
                return False

        return True

    def phone_common_prefix_count(prefix, messages):
        count = 0
        max_count = min(len(prefix), len(messages))

        while count < max_count:
            if phone_message_signature(prefix[count]) != phone_message_signature(messages[count]):
                break
            count += 1

        return count

    def phone_is_date_note(message):
        return message.get("sender") == "system" and message.get("kind") == "date"

    def phone_latest_date_note(messages):
        for message in reversed(messages):
            if phone_is_date_note(message):
                return message.get("body", "")

        return None

    def phone_apply_date_label(old_messages, messages, date_label):
        messages = phone_clone_messages(messages)

        if not date_label or not messages:
            return messages

        if phone_latest_date_note(messages) == date_label:
            return messages

        if phone_messages_are_prefix(old_messages, messages):
            insert_index = len(old_messages)
            if insert_index < len(messages) and phone_latest_date_note(old_messages) != date_label:
                messages.insert(insert_index, phone_date_note(date_label))
            return messages

        if not phone_is_date_note(messages[0]):
            messages.insert(0, phone_date_note(date_label))

        return messages

    def phone_extend_messages(old_messages, messages):
        extended = phone_clone_messages(old_messages)
        extended.extend(phone_clone_messages(messages))
        return extended

    def phone_animation_start_count(old_messages, messages):
        count = phone_common_prefix_count(old_messages, messages)

        while count < len(messages) and phone_is_date_note(messages[count]):
            count += 1

        return count

    def phone_message_needs_typing(message):
        if not message:
            return False

        sender = message.get("sender", "them")
        kind = message.get("kind", "text")
        return sender in ("me", "them") and kind in ("text", "thumb")

    def phone_message_reveal_delay(message):
        if not phone_message_needs_typing(message):
            return 0.05

        if message.get("kind") == "thumb":
            return 0.45

        body_length = len(message.get("body", ""))
        return min(1.25, max(0.55, 0.35 + (body_length * 0.012)))

    def phone_typing_text(phase):
        return "." * (((phase // 2) % 3) + 1)

    def phone_contact_id_from_name(contact_name):
        normalized = (contact_name or "").strip().lower()
        if normalized in PHONE_CONTACT_ALIASES:
            return PHONE_CONTACT_ALIASES[normalized]

        for contact_id, contact in PHONE_CONTACT_CATALOG.items():
            if normalized == contact["name"].lower():
                return contact_id

        generated = re.sub(r"[^a-z0-9]+", "_", normalized).strip("_")
        return generated or "unknown"

    def phone_get_contact(contact_id):
        contact_id = phone_contact_id_from_name(contact_id)

        if contact_id in PHONE_CONTACT_CATALOG:
            return dict(PHONE_CONTACT_CATALOG[contact_id])

        custom_contacts = phone_state_dict("phone_custom_contacts")
        if contact_id in custom_contacts:
            contact = dict(custom_contacts[contact_id])
            contact["id"] = contact_id
            return contact

        return {
            "id": contact_id,
            "name": contact_id.replace("_", " ").title(),
            "subtitle": "Contact",
            "status": "Messages",
        }

    def phone_mark_contact_met(contact_id, contact_name=None, subtitle="Contact"):
        contact_id = phone_contact_id_from_name(contact_id)

        if contact_id not in PHONE_CONTACT_CATALOG:
            custom_contacts = phone_state_dict("phone_custom_contacts")
            custom_contacts[contact_id] = {
                "name": contact_name or contact_id.replace("_", " ").title(),
                "subtitle": subtitle,
                "status": "Messages",
            }

        met_contacts = phone_state_list("phone_met_contacts")
        if contact_id not in met_contacts:
            met_contacts.append(contact_id)

        return contact_id

    def phone_store_thread(contact_id, messages, status="Messages", timestamp=None, clock_text=None, contact_name=None, unread=False):
        contact_id = phone_contact_id_from_name(contact_id)
        phone_mark_contact_met(contact_id, contact_name)

        threads = phone_state_dict("phone_thread_messages")
        old_thread = threads.get(contact_id, {})
        old_messages = phone_clone_messages(old_thread.get("messages", []))
        dated_messages = phone_apply_date_label(old_messages, messages, timestamp)

        threads[contact_id] = {
            "messages": dated_messages,
            "status": status or "Messages",
            "timestamp": timestamp,
            "clock_text": clock_text,
        }

        unread_threads = phone_state_list("phone_unread_threads")
        if unread:
            if contact_id not in unread_threads:
                unread_threads.append(contact_id)
        elif contact_id in unread_threads:
            unread_threads.remove(contact_id)

        return contact_id

    def phone_record_conversation(contact_name, messages, status="Messages", timestamp=None, clock_text=None):
        contact_id = phone_contact_id_from_name(contact_name)
        return phone_store_thread(contact_id, messages, status, timestamp, clock_text, contact_name)

    def phone_thread_messages_for(contact_id):
        thread = phone_get_thread(contact_id)
        return phone_clone_messages(thread["messages"])

    def phone_get_thread(contact_id):
        contact_id = phone_contact_id_from_name(contact_id)
        contact = phone_get_contact(contact_id)
        threads = phone_state_dict("phone_thread_messages")
        thread = dict(threads.get(contact_id, {}))
        timestamp = thread.get("timestamp", None)
        messages = phone_clone_messages(thread.get("messages", []))

        if timestamp and messages and not phone_latest_date_note(messages):
            messages = phone_apply_date_label([], messages, timestamp)

        return {
            "messages": messages,
            "status": thread.get("status", contact.get("status", "Messages")),
            "timestamp": timestamp,
            "clock_text": thread.get("clock_text", None),
        }

    def phone_thread_preview(contact_id):
        thread = phone_get_thread(contact_id)
        messages = [m for m in thread["messages"] if m.get("sender") != "system"]

        if not messages:
            return "No messages yet."

        last_message = messages[-1]
        if last_message.get("kind") == "thumb":
            body = "Thumbs up"
        else:
            body = last_message.get("body", "")

        if last_message.get("sender") == "me":
            return phone_compact_text("You: {}".format(body))
        return phone_compact_text(body)

    def phone_visible_contacts():
        met_contacts = phone_state_list("phone_met_contacts")
        threads = phone_state_dict("phone_thread_messages")
        custom_contacts = phone_state_dict("phone_custom_contacts")

        ordered_ids = []
        for contact_id in PHONE_CONTACT_ORDER:
            if contact_id in met_contacts or contact_id in threads:
                ordered_ids.append(contact_id)

        for contact_id in sorted(custom_contacts.keys()):
            if contact_id not in ordered_ids:
                ordered_ids.append(contact_id)

        for contact_id in sorted(threads.keys()):
            if contact_id not in ordered_ids:
                ordered_ids.append(contact_id)

        return [phone_get_contact(contact_id) for contact_id in ordered_ids]


default phone_met_contacts = []
default phone_thread_messages = {}
default phone_unread_threads = []
default phone_custom_contacts = {}


screen phone_text_screen(contact_name, messages, status="Messages", timestamp=None, clock_text=None, dismiss_action=None, back_action=None, start_visible_count=None, animate=False, auto_advance=False):
    modal True
    zorder 230

    default visible_count = start_visible_count if start_visible_count is not None else len(messages or [])
    default pending_active = animate and (start_visible_count if start_visible_count is not None else len(messages or [])) < len(messages or [])
    default typing_phase = 0
    default pending_elapsed = 0.0
    default scroll_revision = 1

    $ _phone_all_messages = messages or []
    $ _phone_has_pending_messages = animate and visible_count < len(_phone_all_messages)
    $ _phone_visible_messages = _phone_all_messages[:visible_count]
    $ _phone_next_message = _phone_all_messages[visible_count] if _phone_has_pending_messages else None
    $ _phone_typing_message = _phone_next_message if pending_active and phone_message_needs_typing(_phone_next_message) else None
    $ _phone_reveal_delay = phone_message_reveal_delay(_phone_next_message) if _phone_has_pending_messages else None
    $ _phone_close_action = dismiss_action if dismiss_action is not None else Return()
    $ _phone_reveal_count = min(visible_count + 1, len(_phone_all_messages))
    $ _phone_reveal_action = [
        SetScreenVariable("visible_count", _phone_reveal_count),
        SetScreenVariable("pending_active", auto_advance and _phone_reveal_count < len(_phone_all_messages)),
        SetScreenVariable("pending_elapsed", 0.0),
        SetScreenVariable("scroll_revision", scroll_revision + 1),
    ]
    $ _phone_start_typing_action = [
        SetScreenVariable("pending_active", True),
        SetScreenVariable("typing_phase", 0),
        SetScreenVariable("pending_elapsed", 0.0),
        SetScreenVariable("scroll_revision", scroll_revision + 1),
    ]
    $ _phone_skip_action = _phone_reveal_action if _phone_has_pending_messages else _phone_close_action
    $ _phone_dismiss_action = _phone_reveal_action if pending_active and _phone_has_pending_messages else (_phone_start_typing_action if _phone_has_pending_messages else _phone_close_action)
    $ _phone_auto_reveal_action = [
        SetScreenVariable("visible_count", min(visible_count + 1, len(_phone_all_messages))),
        SetScreenVariable("pending_active", auto_advance and min(visible_count + 1, len(_phone_all_messages)) < len(_phone_all_messages)),
        SetScreenVariable("pending_elapsed", 0.0),
        SetScreenVariable("typing_phase", typing_phase + 1),
        SetScreenVariable("scroll_revision", scroll_revision + 1),
    ]

    add Solid("#00000099")

    use phone_thread_model(contact_name, _phone_visible_messages, status, timestamp, clock_text, _phone_close_action, back_action, _phone_typing_message, typing_phase)

    if scroll_revision:
        timer 0.01 action [
            Scroll("phone_thread_viewport", "vertical increase", 1.0),
            SetScreenVariable("scroll_revision", 0),
        ]

    if _phone_has_pending_messages and pending_active:
        timer 0.1 repeat True action If(
            pending_elapsed + 0.1 >= _phone_reveal_delay,
            _phone_auto_reveal_action,
            [
                SetScreenVariable("pending_elapsed", pending_elapsed + 0.1),
                SetScreenVariable("typing_phase", typing_phase + 1),
            ],
        )

    if renpy.is_skipping():
        timer 0.05 repeat True action _phone_skip_action

    key "dismiss" action _phone_dismiss_action
    key "skip" action _phone_skip_action


screen phone_contacts_screen():
    modal True
    zorder 225

    $ _phone_contacts = phone_visible_contacts()

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

            use phone_status_bar(phone_status_text())

            frame:
                xpos 24
                ypos 72
                xysize (346, 68)
                background Solid("#111827")
                padding (0, 0)

                add Solid("#2c3748"):
                    xpos 0
                    ypos 67
                    xsize 346
                    ysize 1

                text "Contacts" style "phone_thread_contact":
                    xalign 0.5
                    ypos 11

                text "Messages" style "phone_thread_status":
                    xalign 0.5
                    ypos 40

                textbutton "X":
                    style "phone_header_button"
                    xpos 306
                    ypos 16
                    action Hide("phone_contacts_screen")

            viewport:
                xpos 40
                ypos 154
                xysize (314, 414)
                mousewheel True

                vbox:
                    spacing 8
                    xfill True

                    if not _phone_contacts:
                        text "No contacts yet." style "phone_thread_note":
                            xalign 0.5
                    else:
                        for _contact in _phone_contacts:
                            $ _contact_id = _contact["id"]
                            $ _contact_preview = phone_thread_preview(_contact_id)
                            $ _contact_thread = phone_get_thread(_contact_id)
                            $ _contact_date = _contact_thread["timestamp"] or ""

                            button:
                                style "phone_contact_button"
                                action [Hide("phone_contacts_screen"), Show("phone_thread_history_screen", contact_id=_contact_id)]

                                hbox:
                                    spacing 10
                                    yalign 0.5

                                    frame:
                                        style "phone_contact_avatar"

                                        text phone_contact_initials(_contact["name"]) style "phone_contact_avatar_text":
                                            xalign 0.5
                                            yalign 0.5

                                    fixed:
                                        yalign 0.5
                                        xysize (230, 62)

                                        text _contact["name"] style "phone_contact_name":
                                            xpos 0
                                            ypos 0
                                            xmaximum 148

                                        if _contact_date:
                                            text _contact_date style "phone_contact_time":
                                                xalign 1.0
                                                ypos 2

                                        text _contact["subtitle"] style "phone_contact_subtitle":
                                            xpos 0
                                            ypos 24

                                        text _contact_preview style "phone_contact_preview":
                                            xpos 0
                                            ypos 43

            add Solid("#dbe4f080"):
                xpos 150
                ypos 627
                xsize 94
                ysize 4

    key "K_ESCAPE" action Hide("phone_contacts_screen")


screen phone_thread_history_screen(contact_id):
    modal True
    zorder 230

    $ _phone_contact = phone_get_contact(contact_id)
    $ _phone_thread = phone_get_thread(contact_id)

    add Solid("#00000099")

    use phone_thread_model(
        _phone_contact["name"],
        _phone_thread["messages"],
        _phone_thread["status"],
        _phone_thread["timestamp"],
        _phone_thread["clock_text"],
        Hide("phone_thread_history_screen"),
        [Hide("phone_thread_history_screen"), Show("phone_contacts_screen")]
    )

    key "K_ESCAPE" action Hide("phone_thread_history_screen")


screen phone_thread_model(contact_name, messages, status="Messages", timestamp=None, clock_text=None, dismiss_action=None, back_action=None, typing_message=None, typing_phase=0):
    $ _phone_status_text = phone_status_text(timestamp, clock_text)
    $ _phone_messages = messages or []
    $ _phone_dismiss_action = dismiss_action if dismiss_action is not None else Return()

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

            add Solid("#090d16"):
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

            use phone_status_bar(_phone_status_text)

            frame:
                xpos 24
                ypos 72
                xysize (346, 68)
                background Solid("#111827")
                padding (0, 0)

                add Solid("#2c3748"):
                    xpos 0
                    ypos 67
                    xsize 346
                    ysize 1

                if back_action:
                    textbutton "<":
                        style "phone_header_button"
                        xpos 10
                        ypos 16
                        action back_action

                text contact_name style "phone_thread_contact":
                    xalign 0.5
                    ypos 11
                    xmaximum 238

                text status style "phone_thread_status":
                    xalign 0.5
                    ypos 40

                textbutton "X":
                    style "phone_header_button"
                    xpos 306
                    ypos 16
                    action _phone_dismiss_action

            viewport:
                id "phone_thread_viewport"
                xpos 42
                ypos 154
                xysize (310, 414)
                yinitial 1.0
                mousewheel True

                vbox:
                    spacing 8
                    xfill True

                    if not _phone_messages:
                        text "No messages yet." style "phone_thread_note":
                            xalign 0.5

                    for _message in _phone_messages:
                        $ _sender = _message.get("sender", "them")
                        $ _body = _message.get("body", "")
                        $ _time = _message.get("time", None)
                        $ _kind = _message.get("kind", "text")

                        if _sender == "system":
                            text _body style "phone_thread_note":
                                xalign 0.5

                        elif _sender == "me":
                            hbox:
                                xfill True

                                null width 55

                                vbox:
                                    spacing 2
                                    xalign 1.0

                                    frame:
                                        style "phone_bubble_me"

                                        if _kind == "thumb":
                                            use phone_thumb_icon("#ffffff", "#dbeafe")
                                        else:
                                            text _body style "phone_bubble_me_text"

                                    if _time:
                                        text _time style "phone_bubble_time":
                                            xalign 1.0

                        else:
                            hbox:
                                xfill True

                                vbox:
                                    spacing 2

                                    frame:
                                        style "phone_bubble_them"

                                        if _kind == "thumb":
                                            use phone_thumb_icon("#111827", "#f2c36b")
                                        else:
                                            text _body style "phone_bubble_them_text"

                                    if _time:
                                        text _time style "phone_bubble_time"

                                null width 55

                    if typing_message:
                        $ _typing_sender = typing_message.get("sender", "them")

                        if _typing_sender == "me":
                            hbox:
                                xfill True

                                null width 55

                                vbox:
                                    xalign 1.0

                                    frame:
                                        style "phone_bubble_me"

                                        text phone_typing_text(typing_phase) style "phone_typing_me_text"
                        else:
                            hbox:
                                xfill True

                                frame:
                                    style "phone_bubble_them"

                                    text phone_typing_text(typing_phase) style "phone_typing_them_text"

                                null width 55

            frame:
                xpos 40
                ypos 582
                xysize (314, 32)
                background Solid("#dce4f0")
                padding (12, 0, 12, 0)

                text "Message" style "phone_input_placeholder":
                    yalign 0.5

            add Solid("#dbe4f080"):
                xpos 150
                ypos 627
                xsize 94
                ysize 4


screen phone_thumb_icon(line="#111827", fill="#f2c36b"):
    fixed:
        xysize (32, 32)

        add Solid(fill):
            xpos 11
            ypos 4
            xsize 10
            ysize 20

        add Solid(fill):
            xpos 18
            ypos 10
            xsize 10
            ysize 7

        add Solid(fill):
            xpos 18
            ypos 18
            xsize 8
            ysize 7

        add Solid(fill):
            xpos 6
            ypos 16
            xsize 9
            ysize 12

        add Solid(line):
            xpos 7
            ypos 27
            xsize 18
            ysize 2


style phone_thread_contact:
    font gui.name_font
    size 22
    color "#f8fafc"
    bold True
    text_align 0.5
    outlines [(1, "#000000", 0, 0)]

style phone_thread_status:
    font gui.interface_font
    size 13
    color "#a8b3c7"
    text_align 0.5
    outlines []

style phone_thread_timestamp:
    font gui.interface_font
    size 12
    color "#6d7890"
    text_align 0.5
    outlines []

style phone_thread_note:
    font gui.interface_font
    size 12
    color "#6d7890"
    text_align 0.5
    xmaximum 252
    outlines []

style phone_header_button:
    xysize (30, 30)
    background Solid("#1f2937")
    hover_background Solid("#2f7dff")
    padding (0, 0)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style phone_header_button_text:
    font gui.interface_font
    size 15
    color "#f8fafc"
    bold True
    xalign 0.5
    yalign 0.5
    text_align 0.5
    outlines []

style phone_contact_button:
    xysize (314, 78)
    background Solid("#111827")
    hover_background Solid("#1f3a5f")
    padding (10, 8, 10, 8)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style phone_contact_avatar:
    xysize (44, 44)
    background Solid("#2f7dff")
    padding (0, 0)
    yalign 0.5

style phone_contact_avatar_text:
    font gui.name_font
    size 16
    color "#ffffff"
    bold True
    text_align 0.5
    outlines [(1, "#00000088", 0, 0)]

style phone_contact_name:
    font gui.interface_font
    size 17
    color "#f8fafc"
    bold True
    outlines []

style phone_contact_time:
    font gui.interface_font
    size 9
    color "#8a96aa"
    outlines []

style phone_contact_subtitle:
    font gui.interface_font
    size 11
    color "#7f8aa0"
    outlines []

style phone_contact_preview:
    font gui.interface_font
    size 12
    color "#cbd5e1"
    xmaximum 222
    outlines []

style phone_bubble_me:
    background Solid("#006bea")
    xmaximum 250
    padding (12, 8, 12, 8)

style phone_bubble_them:
    background Solid("#cfd9e8")
    xmaximum 250
    padding (12, 8, 12, 8)

style phone_bubble_me_text:
    font gui.default_font
    size 19
    color "#ffffff"
    line_spacing 0
    xmaximum 226
    outlines []

style phone_bubble_them_text:
    font gui.default_font
    size 19
    color "#0b1020"
    line_spacing 0
    xmaximum 226
    outlines []

style phone_bubble_time:
    font gui.interface_font
    size 10
    color "#6d7890"
    outlines []

style phone_typing_me_text is phone_bubble_me_text:
    size 20
    bold True
    xminimum 24
    text_align 0.5

style phone_typing_them_text is phone_bubble_them_text:
    size 20
    bold True
    xminimum 24
    text_align 0.5

style phone_input_placeholder:
    font gui.default_font
    size 16
    color "#6d7890"
    outlines []


label phone_text_conversation(contact_name, messages, status="Messages", timestamp=None, clock_text=None, append=False):
    window hide
    $ _phone_date_label = timestamp or phone_current_date_label()
    $ _phone_contact_id = phone_contact_id_from_name(contact_name)
    $ _phone_old_messages = phone_thread_messages_for(_phone_contact_id)
    if append:
        $ _phone_store_messages = phone_extend_messages(_phone_old_messages, messages)
    else:
        $ _phone_store_messages = phone_clone_messages(messages)
    $ phone_store_thread(_phone_contact_id, _phone_store_messages, status, _phone_date_label, clock_text, contact_name)
    $ _phone_display_messages = phone_thread_messages_for(_phone_contact_id)
    $ _phone_start_visible_count = phone_animation_start_count(_phone_old_messages, _phone_display_messages)
    $ _phone_sfx = phone_message_sound(messages)
    if _phone_sfx:
        $ renpy.sound.play(_phone_sfx, channel="sound")
    call screen phone_text_screen(contact_name, _phone_display_messages, status, _phone_date_label, clock_text, start_visible_count=_phone_start_visible_count, animate=True)
    window auto
    return
