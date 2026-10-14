# Messages app: contact discovery, saved threads, typing/reveal and history UI.
# Build messages with phone_msg/phone_thumb/phone_note, then call
# phone_text_conversation(contact, messages, ...). append=True extends history
# and reveals only the new messages; the default replaces the thread.
#
# Per-save defaults own met contacts, thread records, unread IDs, custom metadata
# and the random-conversation notification snapshot. Name/alias helpers normalize
# identity through PHONE_CONTACT_CATALOG / ALIASES / ORDER. Missing timestamps use
# the Calendar snapshot. Optional playback and history stay within story scope.
# Layout reuses phone_device and the shared chassis constants.

init -1 python:
    import math
    import random
    import re
    import store

    # --- Message constructors -------------------------------------------------
    # A "message" is just a dict {sender, body, time, kind}. Helpers below keep
    # callers from hand-writing the dict. kind is "text" | "thumb" | "note" | "date".
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

    # Per-message reveal SFX: a "sent" tick for the player's outgoing bubbles and
    # a "received" tone for the contact's incoming ones. System / date notes (and
    # already-shown history, which never re-reveals) stay silent.
    # phone_play_reveal_sound is the action-safe wrapper the thread screen fires as
    # each bubble appears; it also stays quiet while skipping so fast-forward
    # doesn't machine-gun the sounds.
    def phone_message_reveal_sound(message):
        if not message or not phone_message_needs_typing(message):
            return None

        sender = message.get("sender", "them")
        if sender == "me":
            return audio.phone_text_out
        if sender == "them":
            return audio.phone_text_in
        return None

    def phone_play_reveal_sound(message):
        if renpy.is_skipping():
            return

        sound = phone_message_reveal_sound(message)
        if sound:
            renpy.sound.play(sound, channel="sound")

    # --- Text utilities -------------------------------------------------------
    # phone_safe_text escapes "[" so Matsu'Py text interpolation can't fire on user
    # data; phone_compact_text collapses whitespace + ellipsizes for list previews.
    # Contact rows reserve one line for this text. Keep the preview short enough
    # for the 222px text column; long authored words must never make a second
    # line spill below the 78px row surface.
    PHONE_CONTACT_PREVIEW_MAX_LENGTH = 27
    def phone_safe_text(value):
        return str(value or "").replace("[", "[[")

    def phone_compact_text(value, max_length=32):
        # Strip complete authored tags BEFORE truncating. Cutting a preview
        # through "{i}" or "{image=...}" can otherwise leave an invalid tag.
        plain = renpy.filter_text_tags(str(value or ""), allow=[]).replace("{{", "{")
        text = re.sub(r"\s+", " ", plain).strip()

        if len(text) > max_length:
            text = text[:max_length - 3].rstrip() + "..."

        return phone_typing_display(text)

    # --- Date / clock helpers -------------------------------------------------
    # phone_clock_from_timestamp parses a "...H:MM AM/PM" string into 24h "HH:MM".
    # phone_current_date_label reads the live in-game date from the Calendar System.
    # phone_status_text picks what the status bar shows: explicit clock > timestamp
    # > current calendar date.
    def phone_clock_from_timestamp(timestamp):
        if not timestamp:
            return "--:--"

        parts = str(timestamp).split()
        if len(parts) < 2:
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

        if not (1 <= hour <= 12 and 0 <= minute < 60):
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

    # --- Contact catalog ------------------------------------------------------
    # ORDER drives the contacts-list ordering; CATALOG holds the known contacts;
    # ALIASES map spoken names ("asa", "matsuda akai") to canonical ids.
    PHONE_CONTACT_ORDER = [
        "monika",
        "mom",
        "asahina",
        "matsuda",
    ]

    # "pfp" (optional): a profile-photo path relative to game/. When present (and
    # loadable) the avatar shows the photo cropped to a circle; otherwise it falls
    # back to the contact's initials chip. See phone_contact_pfp + the phone_avatar
    # screen (phone_model_construct.rpy).
    #
    # "sprite" (optional): the image tag used as this contact's face on a VIDEO
    # call -- their standing sprite, cropped to head-and-shoulders and animated
    # by the feed (see facetime.rpy). Any standard 960-tall sprite works; a
    # contact without one falls back to their avatar on a "camera off" card.
    PHONE_CONTACT_CATALOG = {
        "monika": {
            "id": "monika",
            "name": "Monika",
            "subtitle": "Club",
            "status": "Messages",
            "pfp": "addons/Phone System/monikpfp.png",
            "sprite": "monika 1a",
            # The DDLC composites carry more empty canvas above the head than
            # this project's own sprites, so hers is cropped in a little harder.
            "feed_bias": 0.075,
        },
        "mom": {
            "id": "mom",
            "name": "Mom",
            "subtitle": "Family",
            "status": "Messages",
            "pfp": "addons/Phone System/mompfp.png",
            "sprite": "mom neut",
        },
        "asahina": {
            "id": "asahina",
            "name": "Asa",
            "subtitle": "Family",
            "status": "Messages",
            "pfp": "addons/Phone System/asapfp.png",
            "sprite": "asahina neut",
        },
        "matsuda": {
            "id": "matsuda",
            "name": "Matsuda Akai",
            "subtitle": "New Contact",
            "status": "Messages",
            "pfp": "addons/Phone System/matsupfp.png",
            "sprite": "matsuda neut",
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

    # --- Save-state accessors -------------------------------------------------
    # Lazily fetch/create the named store var as a list/dict (same pattern as the
    # roster's thought_state_* helpers). Used for the phone_* state vars below.
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

    # --- Append / dedupe machinery --------------------------------------------
    # These power append=True: clone messages (so saved state isn't aliased),
    # compare by signature, find the common prefix between the old thread and the
    # new full list, and decide which messages are "new" so only those animate.
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

    # Insert a "date" separator note at the right spot: at the join point when
    # appending to an existing thread, or at the very top for a fresh thread --
    # but only if the latest date note isn't already this same label.
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

    # --- Reveal / typing helpers ----------------------------------------------
    # animation_start_count = how many messages are already "old" (shown instantly);
    # the rest animate in. The other helpers decide whether a message types out,
    # how long its reveal delay is, and the "..." typing-dots text.
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

        # The player's own messages are not guessed at -- they are watched being
        # written, so the bubble lands exactly when the typing animation ends.
        if message.get("sender") == "me":
            return phone_typing_duration(message.get("body", ""))

        body_length = len(message.get("body", ""))
        return min(1.25, max(0.55, 0.35 + (body_length * 0.012)))


    # =========================================================================
    # MC'S OWN TYPING
    # =========================================================================
    # The recipient's half of a pending message is a "..." bubble, because you
    # cannot see what somebody else is writing. The PLAYER's half is different:
    # his message is written into the compose bar the way it would be on a real
    # phone -- a keystroke at a time, with the occasional fumbled key that he
    # notices a beat later and backspaces over.
    #
    # WHY THE SEQUENCE IS PRE-BUILT AND CACHED
    #   The thread screen rebuilds ~20x a second while a message is being typed.
    #   Rolling the dice inside the screen would re-randomise the typos on every
    #   one of those rebuilds, so the text would seethe instead of type. Instead
    #   the whole keystroke sequence is built ONCE per message body, cached, and
    #   then just indexed into by frame number. The RNG is seeded FROM THE BODY,
    #   so a given message always types itself the same way -- across rebuilds,
    #   rollback, save/load and a fresh launch.

    PHONE_TYPING_TICK = 0.05        # seconds of animation per keystroke frame
    PHONE_TYPING_MAX_FRAMES = 46    # ~2.3s ceiling; past it he types in bursts
    PHONE_TYPING_MIN_TYPO_LEN = 16  # nobody fumbles "ok" -- short messages are clean

    # --- compose field geometry ----------------------------------------------
    # The field behaves like a real phone's: one line to start, GROWING UPWARD
    # off a fixed bottom edge as the message wraps, and once it hits its line
    # limit it stops growing and scrolls to keep the caret in view.
    #
    # It has to be measured rather than estimated. The first version capped the
    # text at a character count, which is not a width: 32 characters of a
    # proportional font wrapped to two lines inside a box built for one, and the
    # message spilled straight out of the bar.
    PHONE_COMPOSE_TEXT_WIDTH = 248   # px of text room inside the field
    PHONE_COMPOSE_MIN_HEIGHT = 44    # comfortable one-line pointer/touch target
    PHONE_COMPOSE_MAX_LINES = 4      # stop growing here and start scrolling
    PHONE_COMPOSE_PAD_Y = 8          # padding above and below the text
    PHONE_COMPOSE_BOTTOM = 614       # the edge the field grows away from
    PHONE_THREAD_VIEWPORT_HEIGHT = 414   # at its tallest, with the field at rest

    # Adjacent keys on a QWERTY board. A slip is a real neighbouring key rather
    # than a random letter, which is what makes it read as a fumble instead of
    # as noise.
    _PHONE_KEY_NEIGHBOURS = {
        "a": "qws", "b": "vgn", "c": "xdv", "d": "sfec", "e": "wrd",
        "f": "dgrv", "g": "fhtb", "h": "gjyn", "i": "uok", "j": "hkum",
        "k": "jlim", "l": "kop", "m": "njk", "n": "bmhj", "o": "ipl",
        "p": "ol", "q": "wa", "r": "etf", "s": "adwx", "t": "ryg",
        "u": "yij", "v": "cfb", "w": "qes", "x": "zsc", "y": "tuh",
        "z": "asx",
    }

    _PHONE_TYPING_CACHE_MAX = 128
    _phone_typing_cache = {}

    def _phone_typing_seed(body):
        # A stable digest of the body. Python's own hash() of a str is salted
        # per process, so it would give the same message different typos on
        # every launch; this does not.
        digest = 0
        for ch in body:
            digest = (digest * 131 + ord(ch)) & 0xFFFFFFFF
        return digest

    def _phone_wrong_key(ch, rng):
        # A believable mis-key for `ch`, matching its case.
        neighbours = _PHONE_KEY_NEIGHBOURS.get(ch.lower())
        if not neighbours:
            return ch
        wrong = rng.choice(neighbours)
        return wrong.upper() if ch.isupper() else wrong

    def _phone_build_typing_frames(body):
        """
        Build the frame-by-frame record of `body` being typed: a list of the
        strings the compose bar shows, one per PHONE_TYPING_TICK. Repeating a
        string holds it for another frame, which is how pauses are spelled.
        """

        if not body:
            return [""]

        rng = random.Random(_phone_typing_seed(body))
        length = len(body)

        # Long messages are typed several characters per frame rather than
        # taking ten seconds. It still reads as typing, just as fast typing.
        burst = max(1, int(math.ceil(length / float(PHONE_TYPING_MAX_FRAMES))))

        # At most a couple of fumbles per message, and none at all in a short
        # one -- the brief is "occasional", not "cannot use a keyboard".
        if length < PHONE_TYPING_MIN_TYPO_LEN:
            typo_budget = 0
        else:
            typo_budget = rng.choice([0, 1, 1, 1, 2])

        frames = []
        typed = ""
        index = 0

        while index < length:

            # --- a fumble: wrong keys, a beat, then backspaces --------------
            if (
                typo_budget > 0
                and index > 3
                and body[index].isalpha()
                and rng.random() < 0.05
            ):
                typo_budget -= 1
                slip_length = rng.randint(1, 2)

                slip = ""
                for offset in range(slip_length):
                    source = body[index + offset] if index + offset < length else body[index]
                    slip += _phone_wrong_key(source, rng)

                for ch in slip:
                    typed += ch
                    frames.append(typed)

                # He notices.
                for _ in range(rng.randint(2, 4)):
                    frames.append(typed)

                # Backspaces come fast, then a beat before he carries on.
                for _ in range(len(slip)):
                    typed = typed[:-1]
                    frames.append(typed)
                frames.append(typed)

                continue

            # --- ordinary typing --------------------------------------------
            chunk = body[index:index + burst]
            typed += chunk
            index += burst
            frames.append(typed)

            # A tiny rest after end-of-sentence punctuation.
            if chunk and chunk[-1] in ".,!?":
                frames.append(typed)
                frames.append(typed)

        # A held beat on the finished message, just before it is sent.
        frames.append(typed)
        frames.append(typed)

        return frames

    def phone_typing_frames(body):
        cached = _phone_typing_cache.get(body)
        if cached is None:
            cached = _phone_build_typing_frames(body)
            if len(_phone_typing_cache) >= _PHONE_TYPING_CACHE_MAX:
                _phone_typing_cache.clear()
            _phone_typing_cache[body] = cached
        return cached

    def phone_typing_duration(body):
        return max(1, len(phone_typing_frames(body))) * PHONE_TYPING_TICK

    def phone_typing_frame_at(body, frame_index):
        frames = phone_typing_frames(body)
        if not frames:
            return ""
        return frames[max(0, min(int(frame_index), len(frames) - 1))]

    def phone_typing_display(typed):
        """
        Neutralise BOTH of Matsu'Py's text markers in a half-written message.
        Escaping matters more here than anywhere else in the phone: a partial
        string can end mid-tag -- typing "{i}" passes through "{i", which is a
        parse error, not a stray character.
        """
        return typed.replace("{", "{{").replace("[", "[[")

    def phone_typing_caret(frame_index):
        """
        The caret, blinking ~0.3s on / 0.3s off at PHONE_TYPING_TICK.

        It blinks by going TRANSPARENT rather than by being swapped for a space:
        the glyph is laid out either way, so the line it sits on keeps exactly
        the same width, and a message parked on a wrap boundary cannot flicker
        between one line and two in time with the blink.
        """
        on = (int(frame_index) // 6) % 2 == 0
        return "{alpha=%s}|{/alpha}" % ("1.0" if on else "0.0")

    # --- compose field measurement -------------------------------------------
    # Rendering is the only way to learn a Text's real extent (same reasoning as
    # AGCanvas.measure in the Arcade framework, and _enter_m_say_text_render_height
    # in auto_dialogue_font_size.rpy, which this follows).

    _PHONE_COMPOSE_CACHE_MAX = 256
    _phone_compose_cache = {}
    _phone_compose_budget_cache = {}

    def _phone_compose_height(marked_up):
        cached = _phone_compose_cache.get(marked_up)
        if cached is not None:
            return cached
        displayable = Text(
            marked_up,
            style="phone_input_typing",
            xsize=PHONE_COMPOSE_TEXT_WIDTH,
            slow=False,
            substitute=False,
        )
        # int(), NOT the raw render size. get_size() hands back FLOATS, and a
        # float given to a Matsu'Py size/position property is read as a FRACTION
        # of the parent, not as pixels -- ysize 66.0 asks for sixty-six times
        # the phone's height, and the whole compose field leaves the screen.
        height = int(math.ceil(renpy.render(displayable, PHONE_COMPOSE_TEXT_WIDTH, 4096, 0, 0).get_size()[1]))
        if len(_phone_compose_cache) >= _PHONE_COMPOSE_CACHE_MAX:
            _phone_compose_cache.clear()
        _phone_compose_cache[marked_up] = height
        return height

    def _phone_compose_budget():
        # The pixel height of PHONE_COMPOSE_MAX_LINES lines, measured the same
        # way the real text is, so the two are directly comparable.
        key = (PHONE_COMPOSE_MAX_LINES, PHONE_COMPOSE_TEXT_WIDTH)
        cached = _phone_compose_budget_cache.get(key)
        if cached is None:
            cached = _phone_compose_height("\n".join(["Ag"] * PHONE_COMPOSE_MAX_LINES))
            _phone_compose_budget_cache[key] = cached
        return cached

    def phone_compose_fit(full_body, frame_index):
        """
        -> (markup, field_height) for the compose field.

        `full_body` is the WHOLE message; this picks the keystroke frame for
        `frame_index` itself (phone_typing_frames, typos and backspaces and
        all). Passing an already-framed string in would show the message
        complete from the start and kill the typing animation.

        While the message fits inside PHONE_COMPOSE_MAX_LINES the field simply
        grows to hold it. Past that it stops growing and drops characters off
        the FRONT until the tail fits -- which is what a real compose box does
        when you keep typing: it scrolls to stay with the caret.
        """
        body = phone_typing_frame_at(full_body, frame_index)
        caret = phone_typing_caret(frame_index)
        budget = _phone_compose_budget()

        markup = phone_typing_display(body) + caret
        height = _phone_compose_height(markup)

        if height > budget:
            # Smallest number of leading characters to drop. Binary search, so a
            # long message costs ~8 measurements instead of one per character.
            low, high = 0, len(body)
            while low < high:
                mid = (low + high) // 2
                if _phone_compose_height(phone_typing_display(body[mid:]) + caret) <= budget:
                    high = mid
                else:
                    low = mid + 1
            # Slice the original text, then escape it. Slicing escaped markup
            # can split a doubled brace/bracket and expose an incomplete tag.
            markup = phone_typing_display(body[low:]) + caret
            height = _phone_compose_height(markup)

        return markup, int(max(PHONE_COMPOSE_MIN_HEIGHT, height + 2 * PHONE_COMPOSE_PAD_Y))

    def phone_pending_me_body(message):
        # The body the compose bar should be writing, or None when the pending
        # message is not the player's (or is a thumbs-up, which has no text).
        if not message:
            return None
        if message.get("sender") != "me":
            return None
        if message.get("kind", "text") != "text":
            return None
        return message.get("body", "")

    # --- Contact resolution + thread storage ----------------------------------
    # id_from_name: alias/catalog/exact-name lookup, else a generated slug.
    # get_contact: full contact dict (catalog -> custom -> synthesized fallback).
    # mark_contact_met: unlock a contact (registering a custom one if unknown).
    # store_thread / record_conversation: write a thread into phone_thread_messages.
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

    def phone_contact_pfp(contact_name):
        # Resolve a contact (by name/alias/id) to its profile-photo path, or None
        # when there's no image on file. The phone_avatar screen falls back to the
        # initials chip when this returns None.
        pfp = phone_get_contact(contact_name).get("pfp")
        if pfp and renpy.loadable(pfp):
            return pfp
        return None

    def phone_contact_sprite(contact_name):
        # Resolve a contact (by name/alias/id) to the image tag used as their
        # face on a video call, or None when they have no sprite on file (or the
        # tag has gone stale). renpy.has_image keeps a renamed sprite from taking
        # the call screen down with it -- it falls back to "camera off" instead.
        sprite = phone_get_contact(contact_name).get("sprite")
        if sprite and renpy.has_image(sprite):
            return sprite
        return None

    def phone_mark_contact_met(contact_id, contact_name=None, subtitle=None, pfp=None):
        contact_id = phone_contact_id_from_name(contact_id)

        if contact_id not in PHONE_CONTACT_CATALOG:
            custom_contacts = phone_state_dict("phone_custom_contacts")
            existing = custom_contacts.get(contact_id, {})
            entry = dict(existing)
            entry.update({
                "name": contact_name or existing.get("name") or contact_id.replace("_", " ").title(),
                "subtitle": subtitle or existing.get("subtitle") or "Contact",
                "status": existing.get("status", "Messages"),
            })
            # Keep a photo once set: later met-calls (e.g. from phone_store_thread)
            # don't pass pfp and shouldn't wipe it.
            if pfp:
                entry["pfp"] = pfp
            elif existing and existing.get("pfp"):
                entry["pfp"] = existing["pfp"]
            custom_contacts[contact_id] = entry

        met_contacts = phone_state_list("phone_met_contacts")
        if contact_id not in met_contacts:
            met_contacts.append(contact_id)

        return contact_id

    def phone_mark_thread_read(contact_id):
        """Screen action: clear this thread's unread marker without dismissing."""
        if not enter_m_main_story_active():
            return None

        contact_id = phone_contact_id_from_name(contact_id)
        unread_threads = phone_state_list("phone_unread_threads")
        while contact_id in unread_threads:
            unread_threads.remove(contact_id)
        return None

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

    # `thread` lets a caller that already holds one skip the rebuild:
    # phone_get_thread clones every message in the thread, so asking for it
    # twice to read a preview line and a timestamp doubles that work for
    # nothing (see the contacts list).
    def phone_thread_preview(contact_id, thread=None):
        if thread is None:
            thread = phone_get_thread(contact_id)
        messages = [m for m in thread["messages"] if m.get("sender") != "system"]

        if not messages:
            return "No messages yet."

        last_message = messages[-1]
        if last_message.get("kind") == "thumb":
            body = "Thumbs up"
        else:
            # Drop emoji from the preview: a 24px inline image can't fit the row.
            body = phone_strip_emoji(last_message.get("body", "")) or "Emoji"

        if last_message.get("sender") == "me":
            return phone_compact_text("You: {}".format(body), PHONE_CONTACT_PREVIEW_MAX_LENGTH)
        return phone_compact_text(body, PHONE_CONTACT_PREVIEW_MAX_LENGTH)

    # --- Available-conversation notifications --------------------------------
    # The random-conversation catalog is built later (init 1), so these helpers
    # resolve its API dynamically at runtime. Nothing here knows entry ids,
    # channels, or a fixed catalog size: replacing the catalog automatically
    # changes every count and alert.
    _PHONE_NOTIFICATION_BLOCKING_SCREENS = (
        "phone_contacts_screen",
        "phone_thread_history_screen",
        "phone_text_screen",
        "phone_thread_static",
        "phone_home_screen",
        "phone_call_screen",
        "phone_active_call_screen",
        "phone_video_call_screen",
    )

    def phone_notification_entries():
        if not enter_m_main_story_active():
            return []

        available = getattr(store, "phone_random_available", None)
        if available is None:
            return []
        try:
            return list(available())
        except Exception as exc:
            if config.developer:
                renpy.log("ENTER-M PHONE: availability check failed: %r" % (exc,))
            return []

    def phone_notification_ids():
        return [
            str(entry["id"])
            for entry in phone_notification_entries()
            if entry.get("id") is not None
        ]

    def phone_notification_count():
        return len(phone_notification_ids())

    def phone_notification_ui_open():
        return any(renpy.get_screen(name) is not None for name in _PHONE_NOTIFICATION_BLOCKING_SCREENS)

    def phone_notification_poll():
        """
        Announce each availability transition once, never once per render.

        The saved snapshot tracks the exact ids that were available on the last
        completed poll. This catches a newly unlocked entry even when the total
        stays unchanged, avoids replaying the chime after save/load, and lets a
        developer reset make the same entry a genuine new transition again.
        While a phone screen is open, polling pauses so a new item that appears
        behind the handset is announced only after the player closes it.
        """
        # Scope denial happens before any saved phone state is read or changed.
        # If an alert crossed the boundary with us, remove only that UI; keeping
        # the snapshot intact prevents every old id re-alerting on story return.
        if not enter_m_main_story_active():
            alert_open = renpy.get_screen("phone_notification_alert") is not None
            if alert_open:
                renpy.hide_screen("phone_notification_alert")
            return alert_open

        if phone_notification_ui_open():
            return False

        current_ids = phone_notification_ids()
        snapshot = phone_state_list("phone_notification_snapshot")
        new_ids = [entry_id for entry_id in current_ids if entry_id not in snapshot]

        # Defer rather than discard an alert crossed during fast-forward. Once
        # skipping stops, the player gets one cue for the whole accumulated set.
        if renpy.is_skipping():
            return False

        snapshot[:] = current_ids

        if not new_ids:
            return False

        sound = getattr(audio, "phone_notification", None)
        if sound:
            renpy.sound.play(sound, channel="phone_alert")

        renpy.show_screen(
            "phone_notification_alert",
            count=len(current_ids),
            new_count=len(new_ids),
        )
        return True

    def phone_notification_poll_action():
        """Screen-action wrapper: update only on change and never return a value."""
        changed = phone_notification_poll()
        if changed:
            renpy.restart_interaction()
        # A non-None Function result ends the current interaction. In the quick
        # menu that would dismiss the active say statement every half-second.
        return None

    def phone_ready_count_label(count, singular, plural=None):
        count = max(0, int(count))
        noun = singular if count == 1 else (plural or singular + "s")
        return "%d %s" % (count, noun)

    def phone_ready_status(count, fallback="Messages"):
        if not count:
            return fallback
        return phone_ready_count_label(count, "conversation") + " ready"

    def phone_random_action_summary(text_count, call_count, video_count):
        parts = []
        if text_count:
            parts.append(phone_ready_count_label(text_count, "text"))
        if call_count:
            parts.append(phone_ready_count_label(call_count, "call"))
        if video_count:
            parts.append(phone_ready_count_label(video_count, "video call"))
        return "Ready: " + " / ".join(parts) if parts else None

    # Build the ordered contacts-list data: catalog contacts that are met/have a
    # thread first (in PHONE_CONTACT_ORDER), then custom contacts, then any other
    # threads -- de-duplicated.
    def phone_visible_contacts():
        met_contacts = phone_state_list("phone_met_contacts")
        threads = phone_state_dict("phone_thread_messages")
        custom_contacts = phone_state_dict("phone_custom_contacts")
        waiting_contacts = []
        for entry in phone_notification_entries():
            contact_id = phone_contact_id_from_name(entry.get("contact"))
            if contact_id not in waiting_contacts:
                waiting_contacts.append(contact_id)

        ordered_ids = []
        for contact_id in PHONE_CONTACT_ORDER:
            if contact_id in met_contacts or contact_id in threads or contact_id in waiting_contacts:
                ordered_ids.append(contact_id)

        for contact_id in sorted(custom_contacts.keys()):
            if contact_id not in ordered_ids:
                ordered_ids.append(contact_id)

        for contact_id in sorted(threads.keys()):
            if contact_id not in ordered_ids:
                ordered_ids.append(contact_id)

        # An available conversation must always have a route into the UI, even
        # on a compatibility save whose old contact/thread state is incomplete.
        for contact_id in waiting_contacts:
            if contact_id not in ordered_ids:
                ordered_ids.append(contact_id)

        return [phone_get_contact(contact_id) for contact_id in ordered_ids]

    # --- Group chat / per-speaker rendering -----------------------------------
    # Group threads reuse the plain "them" sender and encode the speaker as a
    # "Name: body" prefix (see the s1 Chapter 0.5 group chats), and carry a status
    # like "3 participants". These helpers turn that convention into per-message
    # avatars + name labels WITHOUT any change to the stored message data:
    #   phone_group_thread(status) : is this thread a group? (status mentions
    #                                "participant").
    #   phone_split_speaker(body)  : ("Matsuda", "rest") if body is a "Name: ..."
    #                                tag, else (None, body). Guarded so ordinary
    #                                sentences with a colon aren't mis-split.
    #   phone_thread_rows(...)     : one render dict per message with the resolved
    #                                speaker, the display body (prefix stripped),
    #                                and iMessage-style run flags (show the name at
    #                                the start of a speaker's run, the avatar at the
    #                                end of it).
    _PHONE_SPEAKER_RE = re.compile(r"^\s*([^:\n]{1,24}?):\s+(\S.*)$", re.S)
    _PHONE_SPEAKER_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9 .'’_-]*$")
    _PHONE_SPEAKER_COLORS = [
        "#7fb0ff", "#f2c36b", "#7fd6a0", "#c9a8ff", "#ff9db1", "#6fe0d6", "#f6a97c",
    ]

    def phone_group_thread(status):
        return "participant" in str(status or "").lower()

    def phone_split_speaker(body):
        match = _PHONE_SPEAKER_RE.match(body or "")
        if not match:
            return (None, body)

        name = match.group(1).strip()
        # A speaker tag is a short name (<= 3 words), not a sentence clause that
        # happens to contain a colon.
        if not name or len(name.split()) > 3 or not _PHONE_SPEAKER_NAME_RE.match(name):
            return (None, body)

        return (name, match.group(2))

    def phone_speaker_key(name):
        return phone_contact_id_from_name(name) if name else None

    def phone_speaker_color(name):
        key = phone_speaker_key(name) or ""
        digest = 0
        for ch in key:
            digest = (digest * 31 + ord(ch)) & 0xFFFFFFFF
        return _PHONE_SPEAKER_COLORS[digest % len(_PHONE_SPEAKER_COLORS)]

    def phone_resolve_speaker(message, contact_name, is_group):
        # -> (speaker_name_or_None, display_body). In a group, split the "Name:"
        # tag; in a 1:1 thread the speaker is just the contact.
        body = message.get("body", "")
        if message.get("sender", "them") != "them":
            return (None, body)
        if is_group:
            return phone_split_speaker(body)
        return (contact_name, body)

    def phone_thread_rows(messages, contact_name, is_group):
        resolved = []
        for message in messages or []:
            speaker, body = phone_resolve_speaker(message, contact_name, is_group)
            resolved.append({
                "sender": message.get("sender", "them"),
                "kind": message.get("kind", "text"),
                "time": message.get("time", None),
                "speaker": speaker,
                "body": body,
            })

        total = len(resolved)
        for index, row in enumerate(resolved):
            row["show_name"] = False
            row["show_avatar"] = False
            if row["sender"] != "them":
                continue

            key = phone_speaker_key(row["speaker"])
            prev_key = phone_speaker_key(resolved[index - 1]["speaker"]) if index > 0 and resolved[index - 1]["sender"] == "them" else None
            next_key = phone_speaker_key(resolved[index + 1]["speaker"]) if index + 1 < total and resolved[index + 1]["sender"] == "them" else None

            row["show_name"] = is_group and row["speaker"] is not None and key != prev_key
            # iMessage-style: the avatar caps the LAST bubble of a speaker's run.
            row["show_avatar"] = row["speaker"] is not None and key != next_key

        return resolved


# Per-save phone state (see the header for what each holds).
default phone_met_contacts = []
default phone_thread_messages = {}
default phone_unread_threads = []
default phone_custom_contacts = {}
default phone_notification_snapshot = []


# -----------------------------------------------------------------------------
# SCREEN: phone_notification_alert -- a compact, diegetic heads-up beside the
# quick menu. It is deliberately not a renpy.notify toast: the small phone icon
# identifies the source, the existing Phone button remains the persistent home
# for the count, and the chip gets out of the scene after a few seconds.
# -----------------------------------------------------------------------------
screen phone_notification_alert(count=1, new_count=1):
    zorder 150

    if enter_m_main_story_active():
        $ _phone_alert_count = max(0, int(count))
        $ _phone_alert_new = max(1, int(new_count))
        $ _phone_alert_badge_width = phone_badge_width(_phone_alert_count, min_width=28)
        $ _phone_alert_title = (_("New phone conversation") if _phone_alert_new == 1 else _("%d new phone conversations") % _phone_alert_new)
        $ _phone_alert_detail = _("Open Phone - %d ready total") % _phone_alert_count

        button:
            style "phone_notification_alert_button"
            xpos 108
            yalign 1.0
            # Sit above both the dialogue box and the quick menu's first row. The
            # extra height grows upward, so the alert never covers the current line.
            yoffset -198
            at phone_notification_alert_enter
            action [Hide("phone_notification_alert"), Show("phone_contacts_screen")]

            fixed:
                xysize (344, 76)

                add phone_ui_surface("alert"):
                    xysize (344, 76)

                fixed:
                    xpos 18
                    yalign 0.5
                    xysize (18, 25)

                    use phone_notification_glyph("#8bc7ff")

                vbox:
                    xpos 54
                    yalign 0.5
                    xsize 220
                    spacing 5

                    text _phone_alert_title style "phone_notification_alert_title":
                        xmaximum 220

                    text _phone_alert_detail style "phone_notification_alert_detail":
                        xmaximum 220

                fixed:
                    xpos 328 - _phone_alert_badge_width
                    yalign 0.5
                    xysize (_phone_alert_badge_width, 28)

                    add phone_ui_surface("badge"):
                        xysize (_phone_alert_badge_width, 28)

                    text str(_phone_alert_count) style "phone_badge_text":
                        xalign 0.5
                        yalign 0.5

        timer 3.25 action Hide("phone_notification_alert")
    else:
        # A carried screen must not remain a clickable route back into Phone.
        timer 0.01 action Hide("phone_notification_alert")


# -----------------------------------------------------------------------------
# SCREEN: phone_text_screen -- the ANIMATED thread player used during a live
# conversation (phone_text_conversation calls this). It is a little state
# machine over screen-local vars:
#   visible_count   : how many messages are currently shown
#   pending_active  : whether a typing/reveal cycle is running
#   typing_phase    : frames elapsed since THIS message started being written.
#                     Drives the contact's "..." dots, and doubles as the frame
#                     index into MC's keystroke sequence -- which is why every
#                     reveal resets it to 0 rather than letting it run on.
#   pending_elapsed : timer accumulator toward the next reveal
#   scroll_revision : bumped to retrigger auto-scroll-to-bottom
# The precomputed _phone_*_action lists below wire taps/skip/auto-advance to the
# right state transitions; the actual visuals are delegated to phone_thread_model.
#
# TICK RATE: the loop normally runs at 0.1s, but while the player is writing it
# runs at PHONE_TYPING_TICK so the keystrokes land at a human rate. Both the
# timer interval and the accumulator step read the SAME _phone_tick, so the
# reveal still fires exactly when phone_message_reveal_delay says it should.
# -----------------------------------------------------------------------------
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
    # While MC is the one writing, the loop has to tick at keystroke rate.
    $ _phone_tick = PHONE_TYPING_TICK if phone_pending_me_body(_phone_typing_message) is not None else 0.1
    $ _phone_reveal_delay = phone_message_reveal_delay(_phone_next_message) if _phone_has_pending_messages else None
    $ _phone_close_action = dismiss_action if dismiss_action is not None else Return()
    $ _phone_reveal_count = min(visible_count + 1, len(_phone_all_messages))
    $ _phone_reveal_action = [
        Function(phone_play_reveal_sound, _phone_next_message),
        SetScreenVariable("visible_count", _phone_reveal_count),
        SetScreenVariable("pending_active", auto_advance and _phone_reveal_count < len(_phone_all_messages)),
        SetScreenVariable("pending_elapsed", 0.0),
        SetScreenVariable("typing_phase", 0),
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
        Function(phone_play_reveal_sound, _phone_next_message),
        SetScreenVariable("visible_count", min(visible_count + 1, len(_phone_all_messages))),
        SetScreenVariable("pending_active", auto_advance and min(visible_count + 1, len(_phone_all_messages)) < len(_phone_all_messages)),
        SetScreenVariable("pending_elapsed", 0.0),
        SetScreenVariable("typing_phase", 0),
        SetScreenVariable("scroll_revision", scroll_revision + 1),
    ]

    use phone_thread_model(contact_name, _phone_visible_messages, status, timestamp, clock_text, _phone_close_action, back_action, _phone_typing_message, typing_phase,
        advance_action=_phone_dismiss_action,
        advance_label=(("Send message" if pending_active else "Write message") if phone_pending_me_body(_phone_next_message) is not None else "Next message") if _phone_has_pending_messages else "Done",
        can_close=not _phone_has_pending_messages)

    if scroll_revision:
        timer 0.01 action [
            Scroll("phone_thread_viewport", "vertical increase", 1.0),
            SetScreenVariable("scroll_revision", 0),
        ]

    if _phone_has_pending_messages and pending_active:
        timer _phone_tick repeat True action If(
            pending_elapsed + _phone_tick >= _phone_reveal_delay,
            _phone_auto_reveal_action,
            [
                SetScreenVariable("pending_elapsed", pending_elapsed + _phone_tick),
                SetScreenVariable("typing_phase", typing_phase + 1),
            ],
        )

    if renpy.is_skipping():
        timer 0.05 repeat True action _phone_skip_action

    key "dismiss" action _phone_dismiss_action
    key "skip" action _phone_skip_action


# -----------------------------------------------------------------------------
# SCREEN: phone_contacts_screen -- the contacts list (the quick-menu "Phone").
# Each row opens that contact's saved history via phone_thread_history_screen.
# -----------------------------------------------------------------------------
screen phone_contacts_screen(close_action=None, title="Messages", subtitle=None):
    tag phone_browser
    modal True
    zorder 225

    $ _phone_contacts = phone_visible_contacts()
    $ _phone_contacts_close = close_action if close_action is not None else Hide("phone_contacts_screen")

    use phone_device(screen_fill="#0b1220", status_clock=phone_status_text(), page_direction=-1) id "phone_browser_device":

        frame:
            style "phone_thread_header"
            xpos 24
            ypos 72

            text title style "phone_thread_contact":
                xalign 0.5
                ypos 11

            $ _phone_waiting_total = phone_notification_count()

            text (subtitle or phone_ready_status(_phone_waiting_total)):
                style ("phone_thread_status_live" if _phone_waiting_total else "phone_thread_status")
                xalign 0.5
                ypos 40

            button:
                style "phone_header_button"
                xpos 298
                ypos 12
                action [Hide("phone_notification_alert"), _phone_contacts_close]
                id "phone_contacts_close"
                alt "Close phone"
                add phone_ui_icon("close", 20) xalign 0.5 yalign 0.5

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
                        $ _contact_thread = phone_get_thread(_contact_id)
                        $ _contact_preview = phone_thread_preview(_contact_id, _contact_thread)
                        $ _contact_date = _contact_thread["timestamp"] or ""

                        button:
                            style "phone_contact_button"
                            id ("phone_contact_" + _contact_id)
                            action [Hide("phone_notification_alert"), Show("phone_thread_history_screen", contact_id=_contact_id, return_to_home=(close_action is not None))]

                            hbox:
                                spacing 10
                                yalign 0.5

                                fixed:
                                    yalign 0.5
                                    xysize (40, 40)

                                    use phone_avatar(_contact["name"], 40, "phone_contact_avatar_text")

                                fixed:
                                    yalign 0.5
                                    xysize (236, 62)

                                    text _contact["name"] style "phone_contact_name":
                                        xpos 0
                                        ypos 0
                                        xmaximum 148

                                    $ _contact_waiting = phone_random_count(_contact_id)
                                    $ _contact_badge_width = phone_badge_width(_contact_waiting, min_width=22)

                                    if _contact_date:
                                        text _contact_date style "phone_contact_time":
                                            xalign 1.0
                                            ypos 2

                                    # The count badge sits at the right edge under
                                    # the timestamp, where a phone puts an unread
                                    # count -- it is the one piece of chrome that
                                    # needs no explaining. The instruction for
                                    # what to DO about it lives inside the thread,
                                    # next to the control that clears it: printing
                                    # it on every row turned the list into four
                                    # lines of the same shouted advice.
                                    if _contact_waiting:
                                        fixed:
                                            xalign 1.0
                                            ypos 24
                                            xysize (_contact_badge_width, 20)

                                            add phone_ui_surface("badge"):
                                                xysize (_contact_badge_width, 20)

                                            text str(_contact_waiting) style "phone_badge_text":
                                                xalign 0.5
                                                yalign 0.5

                                    text phone_ready_status(_contact_waiting, _contact["subtitle"]):
                                        style ("phone_contact_ready" if _contact_waiting else "phone_contact_subtitle")
                                        xpos 0
                                        ypos 24
                                        xmaximum 180

                                    text _contact_preview style "phone_contact_preview":
                                        xpos 0
                                        ypos 43

    key "game_menu" action [Hide("phone_notification_alert"), _phone_contacts_close]


# -----------------------------------------------------------------------------
# SCREEN: phone_thread_history_screen -- STATIC view of a saved thread (no
# animation), opened from the contacts list. Reuses phone_thread_model to draw.
# -----------------------------------------------------------------------------
screen phone_thread_history_screen(contact_id, return_to_home=False):
    tag phone_browser
    modal True
    zorder 230

    on "show" action Function(phone_mark_thread_read, contact_id)
    on "replace" action Function(phone_mark_thread_read, contact_id)
    $ _phone_history_back = Show("phone_home_screen") if return_to_home else Show("phone_contacts_screen")
    $ _phone_contact = phone_get_contact(contact_id)
    $ _phone_thread = phone_get_thread(contact_id)
    # Exact entry counts, not three booleans: two waiting texts are two
    # notifications even though they share one launch control.
    $ _phone_text_waiting = phone_random_count(contact_id, "text")
    $ _phone_call_waiting = phone_random_count(contact_id, "call")
    $ _phone_video_waiting = phone_random_count(contact_id, "facetime")
    $ _phone_waiting_total = _phone_text_waiting + _phone_call_waiting + _phone_video_waiting

    use phone_thread_model(
        _phone_contact["name"],
        _phone_thread["messages"],
        phone_ready_status(_phone_waiting_total, _phone_thread["status"]),
        _phone_thread["timestamp"],
        _phone_thread["clock_text"],
        (Return() if return_to_home else Hide("phone_thread_history_screen")),
        _phone_history_back,
        compose_action=(Function(phone_random_launch, contact_id, "text", return_to_home=return_to_home) if _phone_text_waiting else None),
        call_action=(Function(phone_random_launch, contact_id, "call", return_to_home=return_to_home) if _phone_call_waiting else None),
        video_action=(Function(phone_random_launch, contact_id, "facetime", return_to_home=return_to_home) if _phone_video_waiting else None),
        action_hint=phone_random_action_summary(_phone_text_waiting, _phone_call_waiting, _phone_video_waiting),
        text_waiting=_phone_text_waiting,
        call_waiting=_phone_call_waiting,
        video_waiting=_phone_video_waiting,
        page_direction=1,
    )

    key "game_menu" action _phone_history_back


# -----------------------------------------------------------------------------
# SCREEN: phone_thread_static -- a thread shown with NO animation and NO state
# change, for scenes that need to display messages without recording them.
#
# WHY THIS EXISTS
#   phone_thread_model is only the visuals. It is `use`d by the screens that own
#   the interaction, so it deliberately has no `modal True` and no dismiss key of
#   its own -- adding them there would collide with phone_text_screen's dismiss,
#   which has reveal/typing logic bound to it.
#   That makes `call screen phone_thread_model(...)` a trap: it renders fine and
#   then swallows every click, because the only way out is the 20px "X" in the
#   header. Use THIS instead. It supplies the modal, the click-anywhere dismiss
#   and the skip key, and nothing else.
#
# WHEN TO USE IT
#   Unsent drafts, a thread being read over somebody's shoulder, a screenshot --
#   anything the phone's saved state must never learn about. Build the rows with
#   phone_clone_messages(phone_thread_messages_for(id)) + your extra bubbles, so
#   phone_store_thread is never called and the real thread stays untouched.
# -----------------------------------------------------------------------------
screen phone_thread_static(contact_name, messages, status="Messages", timestamp=None, clock_text=None, back_action=None):
    modal True
    zorder 230

    use phone_thread_model(contact_name, messages, status, timestamp, clock_text, Return(), back_action)

    key "dismiss" action Return()
    key "skip" action Return()


# -----------------------------------------------------------------------------
# SCREEN: phone_thread_model -- the SHARED thread visuals (header, scrolling
# bubble list, compose/progression control). Both the live player (phone_text_screen) and the
# static history view use this; it renders whatever `messages` it's handed, plus
# an optional in-progress `typing_message` bubble. "me" = right blue bubble,
# "them" = left grey bubble, "system" = centered note; kind "thumb" = thumbs-up icon.
# -----------------------------------------------------------------------------
screen phone_thread_model(contact_name, messages, status="Messages", timestamp=None, clock_text=None, dismiss_action=None, back_action=None, typing_message=None, typing_phase=0, compose_action=None, call_action=None, video_action=None, action_hint=None, text_waiting=0, call_waiting=0, video_waiting=0, advance_action=None, advance_label="Next message", can_close=True, page_direction=None):
    $ _phone_status_text = phone_status_text(timestamp, clock_text)
    $ _phone_messages = messages or []
    $ _phone_dismiss_action = dismiss_action if dismiss_action is not None else Return()
    $ _phone_is_group = phone_group_thread(status)
    $ _phone_rows = phone_thread_rows(_phone_messages, contact_name, _phone_is_group)
    # Non-None only while the pending message is one the PLAYER is writing; it
    # sends the text to the compose bar instead of to a "..." bubble.
    $ _phone_me_typing_body = phone_pending_me_body(typing_message)
    # The compose field sizes itself to what has been written so far, and the
    # thread gives up exactly the height the field takes -- so a growing field
    # pushes the conversation up instead of covering the last thing said.
    $ _phone_compose = phone_compose_fit(_phone_me_typing_body, typing_phase) if _phone_me_typing_body is not None else None
    $ _phone_compose_height = _phone_compose[1] if _phone_compose else PHONE_COMPOSE_MIN_HEIGHT
    $ _phone_text_waiting = max(0, int(text_waiting))
    $ _phone_call_waiting = max(0, int(call_waiting))
    $ _phone_video_waiting = max(0, int(video_waiting))
    # The hint line takes its space out of the thread, same as a grown compose
    # field does, so nothing it says lands on top of the conversation.
    $ _phone_hint_space = 22 if action_hint else 0
    $ _phone_thread_height = PHONE_THREAD_VIEWPORT_HEIGHT - (_phone_compose_height - PHONE_COMPOSE_MIN_HEIGHT) - _phone_hint_space

    use phone_device(screen_fill=("#0b1220" if page_direction is not None else "#090d16"), status_clock=_phone_status_text, wallpaper_alpha=(0.55 if page_direction is not None else 0.28), page_direction=page_direction) id "phone_browser_device":

        frame:
            style "phone_thread_header"
            xpos 24
            ypos 72

            if back_action:
                button:
                    style "phone_header_button"
                    xpos 4
                    ypos 12
                    action back_action
                    id "phone_thread_back"
                    alt "Back to contacts"
                    add phone_ui_icon("back", 22) xalign 0.5 yalign 0.5

            text contact_name style "phone_thread_contact":
                xalign 0.5
                ypos 11
                xmaximum 238

            text status style "phone_thread_status":
                xalign 0.5
                ypos 40

            if can_close:
                button:
                    style "phone_header_button"
                    xpos 298
                    ypos 12
                    action _phone_dismiss_action
                    id "phone_thread_close"
                    alt "Close conversation"
                    add phone_ui_icon("close", 20) xalign 0.5 yalign 0.5

        viewport:
            id "phone_thread_viewport"
            xpos 42
            ypos 154
            xysize (310, _phone_thread_height)
            yinitial 1.0
            mousewheel True

            vbox:
                spacing 8
                xfill True

                if not _phone_messages:
                    text "No messages yet." style "phone_thread_note":
                        xalign 0.5

                for _row in _phone_rows:
                    $ _sender = _row["sender"]
                    $ _body = phone_emojify(_row["body"])
                    $ _time = _row["time"]
                    $ _kind = _row["kind"]

                    if _sender == "system":
                        text _body style "phone_thread_note":
                            xalign 0.5

                    elif _sender == "me":
                        use phone_me_row(time=_time):
                            if _kind == "thumb":
                                use phone_thumb_glyph("#ffffff", "#dbeafe")
                            else:
                                text _body style "phone_bubble_me_text"

                    else:
                        use phone_them_row(speaker=_row["speaker"], show_name=_row["show_name"], show_avatar=_row["show_avatar"], time=_time):
                            if _kind == "thumb":
                                use phone_thumb_glyph("#111827", "#f2c36b")
                            else:
                                text _body style "phone_bubble_them_text"

                # A message the PLAYER is writing does not get a bubble here --
                # it is being written in the compose bar below, and only becomes
                # a bubble when he sends it. Only the contact's side shows "...".
                if typing_message and _phone_me_typing_body is None:
                    $ _typing_sender = typing_message.get("sender", "them")

                    if _typing_sender == "me":
                        use phone_me_row():
                            use phone_typing_indicator()
                    else:
                        $ _typing_speaker = phone_resolve_speaker(typing_message, contact_name, _phone_is_group)[0]
                        $ _typing_prev_key = phone_speaker_key(_phone_rows[-1]["speaker"]) if _phone_rows and _phone_rows[-1]["sender"] == "them" else None
                        $ _typing_show_name = _phone_is_group and _typing_speaker is not None and phone_speaker_key(_typing_speaker) != _typing_prev_key

                        use phone_them_row(speaker=_typing_speaker, show_name=_typing_show_name, show_avatar=True):
                            use phone_typing_indicator()

        # The instruction line. It sits directly above the bar it is talking
        # about, and pulses gently so the eye is taken from the badge in the
        # contacts list down to the control that clears it.
        if action_hint:
            text action_hint:
                style "phone_action_hint"
                xalign 0.5
                ypos PHONE_COMPOSE_BOTTOM - _phone_compose_height - 19
                at phone_hint_pulse

        # Available calls are explicit, labeled targets. Live text progression
        # is a separate bottom action, so a disabled fake input never eats taps.
        $ _phone_side_keys = [k for k in (("video", video_action), ("phone", call_action)) if k[1] is not None]
        $ _phone_bar_x = 40 + len(_phone_side_keys) * 46
        $ _phone_bar_width = 314 - len(_phone_side_keys) * 46
        $ _phone_bar_action = compose_action if compose_action is not None else advance_action

        for _key_index, _key in enumerate(_phone_side_keys):
            $ _phone_key_count = _phone_video_waiting if _key[0] == "video" else _phone_call_waiting
            button:
                style "phone_attach_key"
                id ("phone_thread_" + _key[0])
                xpos 40 + _key_index * 46
                ypos PHONE_COMPOSE_BOTTOM - 42
                action _key[1]
                alt ("Start video call" if _key[0] == "video" else "Start phone call")
                fixed:
                    xysize (40, 40)
                    add phone_ui_icon(_key[0], 22, "#c4ceff") xalign 0.5 yalign 0.5
                    if _phone_key_count:
                        text str(_phone_key_count) style "phone_action_badge_text":
                            xalign 1.0
                            ypos -2

        button:
            style "phone_compose_button"
            xpos _phone_bar_x
            ypos PHONE_COMPOSE_BOTTOM
            yanchor 1.0
            xysize (_phone_bar_width, _phone_compose_height)
            action _phone_bar_action
            id "phone_thread_progress"
            sensitive (_phone_bar_action is not None)
            alt (("Start text conversation" if compose_action is not None else advance_label) if _phone_bar_action is not None else "Conversation history")

            fixed:
                xysize (_phone_bar_width, _phone_compose_height)
                if _phone_compose is not None:
                    text _phone_compose[0]:
                        style "phone_input_typing"
                        xpos 16
                        ypos PHONE_COMPOSE_PAD_Y
                        xsize PHONE_COMPOSE_TEXT_WIDTH
                else:
                    text (("Text · %d ready" % _phone_text_waiting) if compose_action is not None else (advance_label if advance_action is not None else ("No new texts" if _phone_side_keys else "You're all caught up"))):
                        style "phone_input_placeholder"
                        xpos 16
                        yalign 0.5
                        xmaximum _phone_bar_width - 48

                if _phone_bar_action is not None:
                    add phone_ui_icon("send" if (_phone_compose is not None or compose_action is not None) else ("check" if advance_label == "Done" else "chevron"), 22, "#c4ceff"):
                        xpos _phone_bar_width - 34
                        ypos _phone_compose_height - 32


# -----------------------------------------------------------------------------
# SCREEN: phone_them_row -- the left ("them") side of the thread: a fixed avatar
# gutter + the bubble stack, with the bubble content transcluded. `show_avatar`
# fills the gutter with the speaker's circular avatar (it caps the last bubble of
# a run; mid-run rows keep the gutter empty so bubbles stay aligned). `show_name`
# prints a colored speaker label above the bubble (group chats only).
# -----------------------------------------------------------------------------
# The outgoing ("me") column, mirroring phone_them_row. Both sides of the thread
# now have exactly one definition, so the 55px gutter and the phone_round(18)
# corner radius are set in one place per column instead of being restated at
# every bubble site.
screen phone_typing_indicator():
    hbox:
        spacing 5
        ysize 22
        for _dot in range(3):
            add phone_ui_icon("dot", 7, "#d4dcf3") at phone_typing_dot(_dot * 0.13):
                yalign 0.5

transform phone_typing_dot(delay=0.0):
    alpha 0.4
    yoffset 2
    pause delay
    block:
        ease 0.20 alpha 1.0 yoffset -3
        ease 0.20 alpha 0.4 yoffset 2
        pause 0.46
        repeat


screen phone_me_row(time=None):
    hbox:
        xfill True

        null width 55

        vbox:
            spacing 2
            xalign 1.0

            frame:
                style "phone_bubble_me"

                transclude

            if time:
                text time style "phone_bubble_time":
                    xalign 1.0


screen phone_them_row(speaker=None, show_name=False, show_avatar=False, time=None):
    hbox:
        spacing 7

        fixed:
            xysize (30, 30)
            yalign 1.0

            if show_avatar and speaker:
                use phone_avatar(speaker, 30, "phone_group_avatar_text")

        vbox:
            spacing 3

            if show_name and speaker:
                text speaker style "phone_group_speaker" color phone_speaker_color(speaker)

            # The inner hbox pins the bubble hard-left so a short bubble (a one-word
            # reply, or the typing "...") never drifts toward center of the column.
            hbox:
                frame:
                    style "phone_bubble_them"

                    transclude

            if time:
                text time style "phone_bubble_time"


screen phone_thumb_glyph(line="#111827", fill="#f2c36b", size=38):
    if phone_emoji_loadable("1f44d"):
        add Transform("assets/emoji/1f44d.png", size=(size, size))
    else:
        add phone_ui_icon("thumb", size, fill)


transform phone_notification_alert_enter:
    on show:
        alpha 0.0
        xoffset -12
        easeout_quad 0.20 alpha 1.0 xoffset 0
    on hide:
        easein_quad 0.14 alpha 0.0 xoffset -8


transform phone_notification_badge_arrive:
    on show:
        alpha 0.0
        zoom 0.72
        easeout_back 0.24 alpha 1.0 zoom 1.0


style phone_notification_alert_button is empty:
    xysize (344, 76)
    padding (0, 0)
    background None
    hover_background None
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style phone_notification_alert_title:
    font PHONE_UI_FONT
    size 14
    color "#f3f8ff"
    bold True
    outlines []

style phone_notification_alert_detail:
    font PHONE_UI_FONT
    size 11
    color "#8da4bf"
    outlines []


style phone_thread_contact:
    font PHONE_UI_FONT
    size 22
    color "#f8fafc"
    bold True
    text_align 0.5
    outlines []

style phone_thread_status:
    font PHONE_UI_FONT
    size 13
    color "#a8b3c7"
    text_align 0.5
    outlines []

# The contacts header when there is something to do, so the count is visible
# before the player has scrolled the list.
style phone_thread_status_live is phone_thread_status:
    color "#6fb2ff"
    bold True

style phone_thread_timestamp:
    font PHONE_UI_FONT
    size 12
    color "#a7b2c8"
    text_align 0.5
    outlines []

style phone_thread_note:
    font PHONE_UI_FONT
    size 12
    color "#a7b2c8"
    text_align 0.5
    xmaximum 252
    outlines []

style phone_thread_header is empty:
    xysize (346, 68)
    background phone_ui_surface("surface")
    padding (0, 0)

style phone_header_button:
    xysize (44, 44)
    background None
    hover_background phone_ui_surface("surface_hover")
    padding (0, 0)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style phone_header_button_text:
    font PHONE_UI_FONT
    size 15
    color "#f8fafc"
    bold True
    xalign 0.5
    yalign 0.5
    text_align 0.5
    outlines []

style phone_contact_button:
    xysize (314, 78)
    background phone_ui_surface("surface")
    hover_background phone_ui_surface("surface_hover")
    padding (12, 8, 12, 8)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style phone_contact_avatar_text:
    font PHONE_UI_FONT
    size 16
    color "#ffffff"
    bold True
    text_align 0.5
    outlines [(1, "#00000088", 0, 0)]

style phone_contact_name:
    font PHONE_UI_FONT
    size 17
    color "#f8fafc"
    bold True
    outlines []

style phone_contact_time:
    font PHONE_UI_FONT
    size 9
    color "#8a96aa"
    outlines []

style phone_contact_subtitle:
    font PHONE_UI_FONT
    size 11
    color "#7f8aa0"
    outlines []

style phone_contact_ready is phone_contact_subtitle:
    color "#6fb2ff"
    bold True

style phone_contact_preview:
    font PHONE_UI_FONT
    size 12
    color "#cbd5e1"
    xmaximum 222
    ymaximum 16
    outlines []

# Nine-slice artwork preserves bubble corners at every message height.
style phone_bubble_me:
    background phone_ui_surface("outgoing")
    xmaximum 250
    padding (13, 9, 13, 9)

style phone_bubble_them:
    background phone_ui_surface("incoming")
    xmaximum 250
    padding (13, 9, 13, 9)

style phone_bubble_me_text:
    font PHONE_UI_FONT
    size 17
    color "#ffffff"
    line_spacing 2
    xmaximum 224
    outlines []

style phone_bubble_them_text:
    font PHONE_UI_FONT
    size 17
    color "#edf0f9"
    line_spacing 2
    xmaximum 224
    outlines []

style phone_bubble_time:
    font PHONE_UI_FONT
    size 10
    color "#a7b2c8"
    outlines []

# Group-chat speaker label above a "them" bubble; the color is overridden per
# speaker (phone_speaker_color) at the call site.
style phone_group_speaker:
    font PHONE_UI_FONT
    size 11
    color "#8bbcff"
    bold True
    xpos 4
    xmaximum 220
    outlines []

# Initials fallback inside the small 30px in-thread avatar.
style phone_group_avatar_text:
    font PHONE_UI_FONT
    size 13
    color "#ffffff"
    bold True
    text_align 0.5
    outlines [(1, "#00000088", 0, 0)]

# Slow and shallow on purpose: enough movement to be noticed on a screen the
# player is already looking at, not enough to nag.
transform phone_hint_pulse:
    alpha 0.55
    block:
        easeout 1.1 alpha 1.0
        easein 1.1 alpha 0.55
        repeat

style phone_action_hint:
    font PHONE_UI_FONT
    size 12
    color "#6fb2ff"
    bold True
    text_align 0.5
    xmaximum 320
    outlines []

# The unread-style count badge on a contacts row.
style phone_badge_text:
    font PHONE_UI_FONT
    size 11
    color "#15203d"
    bold True
    text_align 0.5
    outlines []

style phone_action_badge_text is phone_badge_text:
    size 9
    color "#c4ceff"

# Compose controls share artwork for idle, typing and actionable states.
style phone_compose_plate is empty:
    padding (0, 0)

style phone_compose_button is phone_compose_plate:
    background phone_ui_surface("compose")
    hover_background phone_ui_surface("surface_hover")
    insensitive_background phone_ui_surface("compose")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

# The call / video keys beside the compose bar.
style phone_attach_key is empty:
    xysize (40, 42)
    padding (0, 0)
    background phone_ui_surface("compose")
    hover_background phone_ui_surface("surface_hover")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style phone_input_placeholder:
    font PHONE_UI_FONT
    size 16
    color "#a7b2c8"
    outlines []

# What MC has written so far. Darker than the placeholder (it is real text, not
# a prompt) and kept to one line -- phone_typing_display scrolls the tail in.
style phone_input_typing is phone_input_placeholder:
    color "#f0f3ff"


# =============================================================================
# PUBLIC LABEL: phone_text_conversation -- the main story entry point.
# Records the conversation into saved state, computes which messages are new
# (so only those animate), then plays the animated thread screen.
#   append=True : extend the existing thread (old messages shown instantly).
#   append=False: replace the thread with `messages`.
#   timestamp   : date label for the thread (defaults to current calendar date).
# The blocking call screen participates in automatic dialogue-window management.
# =============================================================================
label phone_text_conversation(contact_name, messages, status="Messages", timestamp=None, clock_text=None, append=False):
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
    call screen phone_text_screen(contact_name, _phone_display_messages, status, _phone_date_label, clock_text, start_visible_count=_phone_start_visible_count, animate=True)
    return
