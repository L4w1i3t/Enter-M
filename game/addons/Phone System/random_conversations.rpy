# =============================================================================
# Random Phone Conversations  --  IDLE CHATTER THE PLAYER STARTS
# =============================================================================
#
# WHAT THIS FILE IS
#   The small, casual, day-to-day conversations MC can have with a contact
#   whenever he feels like it, instead of only when the story hands him a phone
#   scene. They are deliberately low-stakes and often nonsense -- leftovers,
#   spiders, a hat -- because the point is that the world keeps going and the
#   phone is a place people live in, not a cutscene delivery mechanism.
#
#   This file holds BOTH the data (PHONE_RANDOM_CONVERSATIONS) and the small
#   engine around it. The UI lives in text.rpy: opening a contact gives you a
#   live compose bar, a call key and a video key, each lit only when that
#   contact actually has something of that kind waiting.
#
# WRITING A NEW ONE
#   Append a dict to PHONE_RANDOM_CONVERSATIONS:
#     id       unique and permanent -- it is what gets written to the save when
#              the conversation has been used, so renaming one makes it replay.
#     contact  any name/alias the phone knows ("Asa", "Matsuda Akai", "Mom").
#     kind     "text" | "call" | "facetime".
#     unlock   see phone_random_unlocked below. Defaults to "met", but almost
#              nothing should actually use that -- prefer ("open", channel) for
#              a first conversation and ("seen", id) for a follow-up, so the
#              chatter arrives after the story has earned it.
#     body     for kind "text": a list of phone_msg/phone_thumb.
#              for "call"/"facetime": a list of phone_call_line/phone_call_note.
#     sprite   "facetime" only, and optional -- defaults to the contact's own
#              sprite from PHONE_CONTACT_CATALOG.
#
#   Use %NAME% anywhere the player's name should appear. It is substituted at
#   play time, NOT with "[player]": a "me" message is typed out character by
#   character by the compose animation, and a half-typed "[play" is a Matsu'Py
#   parse error rather than a typo on screen.
#
# ONE-SHOT BY DESIGN
#   Each conversation plays once per save (phone_random_seen) and text ones are
#   appended to the real thread, so the history the player scrolls back through
#   is the history they actually made.
# =============================================================================

# Phone-only art stays outside Matsuda's strict layered-image pose contract.
# The video feed expects the same normalised 640x960 canvas as every cast sprite.
image phone_matsuda_duck_hat = Transform("assets/characters/matsuda/facetime_duck_hat.png", fit="contain", xysize=(640, 960))

# init 1: the catalog is built out of phone_msg / phone_call_line, which are
# defined at init -1 in text.rpy and call.rpy. Same-priority files run in
# filename order, and "random_conversations" sorts before "text", so building
# this at init -1 would call helpers that do not exist yet.
init 1 python:

    # --- unlock rules ---------------------------------------------------------
    # "met"                -> the contact is in the player's phone at all.
    # ("date", "MMDD")     -> on or after that story date.
    # ("flag", "var_name") -> that store variable is truthy.
    # ("open", "channel")  -> the story has opened that line -- see below.
    # ("seen", "entry_id") -> another random conversation has already happened.
    # ("unseen", "entry_id") -> another random conversation has not happened yet.
    # A list of rules means ALL of them must pass.
    #
    # WHY "open" AND NOT JUST "met". Having someone's number is not the same as
    # having a reason to use it. "met" fires the moment a contact card exists,
    # which for most of the cast is day one -- so gating on it meant the phone
    # handed the player seven idle chats before anybody in the story had texted
    # them unprompted, and Matsuda's "the vending machine gave me two drinks" was
    # available the same evening she introduced herself. An "open channel" is the
    # beat where THAT PERSON reaches out on their own, in that medium: after it,
    # unprompted small talk is in character; before it, it is the player texting
    # a stranger. The channels are per-medium (a text thread being warm does not
    # mean you video-call someone) and they are opened by phone_open() calls in
    # the day files -- see PHONE_OPEN_CHANNELS for the full list and where each
    # one is opened.

    def _phone_random_story_key(month, day):
        """
        Order a story date so it can be compared with >=.

        The story year starts in May and runs into January, so a plain MMDD
        comparison puts New Year's Day (0101) BEFORE the first day of the story
        (0515) and every January unlock would read as already passed. Counting
        months from May instead keeps the year in the order it is played.
        """
        return ((int(month) - 5) % 12) * 100 + int(day)

    def _phone_random_today_key():
        calendar_obj = getattr(store, "calendar", None)
        if calendar_obj is None:
            return None
        try:
            snapshot = calendar_obj.get_snapshot()
            return _phone_random_story_key(snapshot["month"], snapshot["day"])
        except Exception:
            return None

    # Every channel the story can open, and the beat that opens it. A channel is
    # a (person, medium) pair, because being comfortable enough to text someone
    # about nothing is a different threshold from ringing their phone.
    #
    #   asa            0518  she texts her brother from one room away
    #   mom            0521  her first thread that is not a note on the counter
    #   mom_call       0525  her first actual phone call
    #   monika         0518  her first out-of-hours text
    #   monika_call    0521  her first call
    #   matsuda        0520  the first time she reaches out that ISN'T May 17 --
    #                        May 17 is the introduction, and a number taken off a
    #                        sidewalk collision is not yet an open line
    #   matsuda_video  0529  by now she is sending unprompted bits; a camera is
    #                        the natural next escalation for her specifically
    #
    # All seven land inside Chapter 0.5, so a player who finishes the prologue has
    # had the chance at every idle conversation currently written.
    PHONE_OPEN_CHANNELS = (
        "asa", "mom", "mom_call", "monika", "monika_call", "matsuda", "matsuda_video",
    )

    # Saves created before this system existed never ran the phone_open() calls
    # above. One story day after a channel's establishing beat, its date becomes
    # a compatibility fallback. The strict > keeps a fresh playthrough from
    # unlocking a channel early on the same day, before that beat is reached.
    PHONE_OPEN_FALLBACK_DATES = {
        "asa": "0518",
        "mom": "0521",
        "mom_call": "0525",
        "monika": "0518",
        "monika_call": "0521",
        "matsuda": "0520",
        "matsuda_video": "0529",
    }

    def phone_open(*channels):
        """
        Story API: "this person now reaches out on their own, in this medium."

        Called from the day files at the beat that earns it. Per-save (a store
        variable), NOT persistent: whether a line is warm is a fact about this
        playthrough, unlike the Archive's unlocks, which are facts about the
        profile.
        """
        for channel in channels:
            if channel not in PHONE_OPEN_CHANNELS and config.developer:
                raise Exception("phone_open: %r is not in PHONE_OPEN_CHANNELS." % (channel,))
            setattr(store, "phone_open_" + channel, True)

    def _phone_random_rule_passes(rule, contact_id):
        if rule == "met":
            return contact_id in phone_state_list("phone_met_contacts")

        try:
            kind, value = rule
        except Exception:
            return False

        if kind == "date":
            today = _phone_random_today_key()
            if today is None:
                return False
            text = str(value).zfill(4)
            return today >= _phone_random_story_key(text[:2], text[2:])

        if kind == "flag":
            return bool(getattr(store, value, False))

        if kind == "open":
            channel = str(value)
            if bool(getattr(store, "phone_open_" + channel, False)):
                return True

            fallback = PHONE_OPEN_FALLBACK_DATES.get(channel)
            today = _phone_random_today_key()
            if fallback is None or today is None:
                return False

            text = str(fallback).zfill(4)
            return today > _phone_random_story_key(text[:2], text[2:])

        if kind == "seen":
            return value in phone_state_list("phone_random_seen")

        if kind == "unseen":
            return value not in phone_state_list("phone_random_seen")

        return False

    def phone_random_unlocked(entry):
        contact_id = phone_contact_id_from_name(entry["contact"])
        rules = entry.get("unlock", "met")

        # A bare rule and a list of rules are both allowed; ("date", "0520") is
        # itself a 2-tuple, so only a list counts as "several rules".
        if not isinstance(rules, list):
            rules = [rules]

        return all(_phone_random_rule_passes(rule, contact_id) for rule in rules)

    # --- lookup ---------------------------------------------------------------

    def phone_random_entry(entry_id):
        for entry in PHONE_RANDOM_CONVERSATIONS:
            if entry["id"] == entry_id:
                return entry
        return None

    def phone_random_available(contact_id=None, kind=None):
        """Every unlocked, unplayed conversation, optionally narrowed."""
        seen = phone_state_list("phone_random_seen")
        wanted = phone_contact_id_from_name(contact_id) if contact_id else None
        out = []

        for entry in PHONE_RANDOM_CONVERSATIONS:
            if entry["id"] in seen:
                continue
            if kind is not None and entry.get("kind", "text") != kind:
                continue
            if wanted is not None and phone_contact_id_from_name(entry["contact"]) != wanted:
                continue
            if not phone_random_unlocked(entry):
                continue
            out.append(entry)

        return out

    def phone_random_next_id(contact_id, kind):
        # Oldest-first, so a catalog reads in the order it was written.
        entries = phone_random_available(contact_id, kind)
        return entries[0]["id"] if entries else None

    def phone_random_has(contact_id, kind=None):
        return bool(phone_random_available(contact_id, kind))

    def phone_random_count(contact_id=None, kind=None):
        return len(phone_random_available(contact_id, kind))

    def phone_random_hint(contact_name, has_text, has_call, has_video):
        """
        The line printed above the compose bar telling the player, in words,
        what to press.

        A badge that cannot be explained is worse than no badge: a first-time
        player reads an unread dot as something they have failed to clear and
        has no way to learn that the dead-looking grey bar at the bottom is now
        a button. So the thread says it outright, and names the contact so it
        reads as a prompt rather than as UI furniture.
        """
        if not (has_text or has_call or has_video):
            return None

        first_name = str(contact_name or "").split()[0] if contact_name else "them"

        if has_text and (has_call or has_video):
            return "Tap the bar to text %s, or a key to call" % first_name
        if has_text:
            return "Tap the bar to text %s" % first_name
        if has_call and has_video:
            return "Tap a key to call %s" % first_name
        if has_video:
            return "Tap the camera key to video-call %s" % first_name
        return "Tap the phone key to call %s" % first_name

    def phone_random_mark_seen(entry_id):
        seen = phone_state_list("phone_random_seen")
        if entry_id not in seen:
            seen.append(entry_id)

    # --- content preparation --------------------------------------------------

    def phone_random_body(entry):
        """
        A fresh copy of the entry's messages with %NAME% resolved.

        Copied because the catalog is init data: handing the live dicts to
        phone_store_thread would let a save alias them, and the next playthrough
        would inherit whatever the last one did to them.
        """
        name = getattr(store, "player", None) or "you"
        prepared = []

        for message in entry.get("body", []):
            copy = dict(message)
            body = copy.get("body")
            if body:
                copy["body"] = body.replace("%NAME%", name)
            prepared.append(copy)

        return prepared

    # --- launching from the phone UI -----------------------------------------

    def phone_random_launch(contact_id, kind):
        """
        Screen action: play the next conversation of `kind` with this contact.

        The phone screens are closed first and the contact thread is reopened
        afterwards, so the conversation is not drawn on top of the menu that
        started it. It runs in a NEW CONTEXT because the phone is opened from
        the quick menu in the middle of a story statement -- a plain `call`
        would hijack that statement, while a new context plays out and hands
        control straight back. (It must only ever `return`; jumping out of a
        new context unwinds to the main menu.)
        """
        entry_id = phone_random_next_id(contact_id, kind)
        if entry_id is None:
            return

        renpy.hide_screen("phone_thread_history_screen")
        renpy.hide_screen("phone_contacts_screen")
        renpy.call_in_new_context("phone_random_play", entry_id)
        renpy.show_screen(
            "phone_thread_history_screen",
            contact_id=phone_contact_id_from_name(contact_id),
        )


    # =========================================================================
    # THE CATALOG
    # Casual, throwaway, and in character. Voices, for reference:
    #   Asa      lowercase, compressed, starts in the middle; spoken calls use
    #            normal dialogue rather than reading her text style aloud
    #   Mom      a civil lawyer and good at her job. Complete sentences, precise,
    #            dryly funny, warm underneath. She is NOT bad with technology and
    #            is never the butt of the joke for not understanding something --
    #            her calls loosen when she is thinking or doing something else
    #   Monika   multi-text enthusiasm, tangents, corrections, occasional ~
    #   Matsuda  theatrical one line, blunt/slangy the next; the register switch
    #            matters more than making every sentence a performance
    #   MC       proper casing, dry and short, practical care under the complaint
    #
    # The player starts these from the compose/call controls. Texts therefore
    # begin with something MC actually chose to send. Calls begin with the callee
    # answering, then establish why he rang. Date gates keep follow-ups from all
    # piling into the first evening their channel opens.
    # =========================================================================
    PHONE_RANDOM_CONVERSATIONS = [

        {
            "id": "asa_leftovers",
            "contact": "Asa",
            "kind": "text",
            "unlock": ("open", "asa"),
            "body": [
                phone_msg("me", "Were you saving the rice in the fridge?"),
                phone_msg("them", "why"),
                phone_msg("me", "Just asking."),
                phone_msg("them", "why are u asking like a cop"),
                phone_msg("me", "I ate it."),
                phone_msg("them", "i KNEW it"),
                phone_msg("me", "I'll make more."),
                phone_msg("them", "with egg"),
                phone_msg("me", "Fine."),
            ],
        },

        {
            "id": "asa_spider",
            "contact": "Asa",
            "kind": "text",
            "unlock": [("seen", "asa_leftovers"), ("date", "0521")],
            "body": [
                phone_msg("me", "Whatever happened to the sink spider?"),
                phone_msg("them", "it moved itself"),
                phone_msg("me", "Where?"),
                phone_msg("them", "..."),
                phone_msg("me", "Asa."),
                phone_msg("them", "ur room maybe"),
                phone_msg("me", "Why would it go to my room?"),
                phone_msg("them", "ur older"),
                phone_msg("me", "That's not how spiders work."),
                phone_msg("them", "its how siblings work"),
                phone_msg("me", "I'm changing the locks."),
            ],
        },

        {
            "id": "asa_wrong_chat",
            "contact": "Asa",
            "kind": "text",
            # Legacy ID retained because it may already be stored in old saves.
            "unlock": [("seen", "asa_spider"), ("date", "0524")],
            "body": [
                phone_msg("me", "Did you tell Sam I couldn't play tonight?"),
                phone_msg("them", "maybe"),
                phone_msg("me", "I didn't say no."),
                phone_msg("them", "i know"),
                phone_msg("me", "Then why'd you tell him that?"),
                phone_msg("them", "because u were doing homework"),
                phone_msg("me", "...Thanks, I think."),
                phone_msg("them", "ur welcome. dont make it weird"),
            ],
        },

        {
            "id": "asa_controller",
            "contact": "Asa",
            "kind": "text",
            "unlock": [("seen", "asa_wrong_chat"), ("date", "0527")],
            "body": [
                phone_msg("me", "Why is jump on R3 now?"),
                phone_msg("them", "idk"),
                phone_msg("me", "You were the last one using it."),
                phone_msg("them", "prove it"),
                phone_msg("me", "You inverted the camera too."),
                phone_msg("them", "thats better"),
                phone_msg("me", "So you did it."),
                phone_msg("them", "that proves nothing"),
                phone_msg("me", "Put it back."),
                phone_msg("them", "after this match"),
            ],
        },

        {
            "id": "asa_poster_rescue",
            "contact": "Asa",
            "kind": "text",
            "unlock": [("seen", "asa_controller"), ("date", "0530")],
            "body": [
                phone_msg("me", "I'm fixing the club flyer. Left-aligned or centered?"),
                phone_msg("them", "send both"),
                phone_msg("me", "That bad?"),
                phone_msg("them", "worse"),
                phone_msg("them", "why are there 4 fonts"),
                phone_msg("me", "There are two."),
                phone_msg("them", "still 1 too many"),
                phone_msg("them", "send me the file"),
                phone_msg("me", "You're fixing it?"),
                phone_msg("them", "im preventing an incident"),
            ],
        },

        {
            "id": "mom_discoverable",
            "contact": "Mom",
            "kind": "text",
            # This lands after the May 24 curry dinner it refers back to.
            "unlock": [("open", "mom"), ("date", "0525")],
            "body": [
                phone_msg("me", "Asa called the curry 'mid.'"),
                phone_msg("them", "I heard."),
                phone_msg("me", "Are you taking feedback?"),
                phone_msg("them", "From you, yes."),
                phone_msg("me", "She added hot sauce before tasting it."),
                phone_msg("them", "Exactly. Her feedback has been assigned the appropriate weight."),
                phone_msg("me", "Which is?"),
                phone_msg("them", "Very little."),
                phone_msg("me", "I'll keep that to myself."),
                phone_msg("them", "Please do."),
            ],
        },

        {
            "id": "mom_laundry_receipt",
            "contact": "Mom",
            "kind": "text",
            "unlock": [("seen", "mom_discoverable"), ("date", "0527")],
            "body": [
                phone_msg("me", "Was the receipt in your black jacket important?"),
                phone_msg("them", "Why?"),
                phone_msg("me", "It went through the wash."),
                phone_msg("them", "...Can you still read it?"),
                phone_msg("me", "It says '8' and nothing else."),
                phone_msg("them", "Then apparently it cost eight."),
                phone_msg("me", "That's very calm."),
                phone_msg("them", "I'm choosing to believe it was lunch."),
                phone_msg("me", "Sorry."),
                phone_msg("them", "I know. You checked the other pockets?"),
                phone_msg("me", "After that, yes."),
                phone_msg("them", "Good."),
            ],
        },

        {
            "id": "mom_mug_inquiry",
            "contact": "Mom",
            "kind": "text",
            "unlock": [("seen", "mom_laundry_receipt"), ("date", "0530")],
            "body": [
                phone_msg("me", "I need to confess something about your work mug."),
                phone_msg("them", "What happened?"),
                phone_msg("me", "The handle chipped. Sharp edge."),
                phone_msg("them", "All right. Throw it out."),
                phone_msg("me", "Already did."),
                phone_msg("them", "You could have led with that."),
                phone_msg("me", "Would that have helped?"),
                phone_msg("them", "No."),
                phone_msg("me", "That sounded painful."),
                phone_msg("them", "It was a very good mug..."),
            ],
        },

        {
            "id": "monika_waypoint",
            "contact": "Monika",
            "kind": "text",
            "unlock": ("open", "monika"),
            "body": [
                phone_msg("me", "How's the book?"),
                phone_msg("them", "Finished!!"),
                phone_msg("them", "Where are you now?"),
                phone_msg("me", "Page 212."),
                phone_msg("them", "THE WINDOW SCENE!!"),
                phone_msg("them", "Did it work for you?"),
                phone_msg("me", "Annoyingly, yes."),
                phone_msg("them", "Okay. Good."),
                phone_msg("them", "Wait--what did you think of the last line?"),
                phone_msg("me", "I need the rest of the chapter first."),
                phone_msg("them", "Right. Sorry!! I'll stop hovering. Enjoy~"),
            ],
        },

        {
            "id": "monika_asterisk",
            "contact": "Monika",
            "kind": "text",
            # Legacy ID retained; the old multi-asterisk routine was too visibly
            # constructed, but saves may already know it by this name.
            "unlock": [("seen", "monika_waypoint"), ("date", "0520")],
            "body": [
                phone_msg("me", "Do you still have the handout from class?"),
                phone_msg("them", "I think so! Give me a sec"),
                phone_msg("them", "Found--"),
                phone_msg("them", "No, that's a debate outline."),
                phone_msg("them", "Okay. Now I found it."),
                phone_msg("me", "Take your time."),
                phone_msg("them", "I'm sending it before I open anything else."),
                phone_msg("me", "Probably safest."),
            ],
        },

        {
            "id": "monika_four_bars",
            "contact": "Monika",
            "kind": "text",
            "unlock": [("seen", "monika_asterisk"), ("date", "0524")],
            "body": [
                phone_msg("me", "How'd piano go?"),
                phone_msg("them", "Bad!"),
                phone_msg("them", "Not bad bad. Just..."),
                phone_msg("them", "I have four bars that hate me"),
                phone_msg("me", "Only four?"),
                phone_msg("them", "They repeat."),
                phone_msg("me", "Take a break?"),
                phone_msg("them", "I did!"),
                phone_msg("them", "I spent the break thinking about bar three."),
                phone_msg("me", "That's not a break."),
                phone_msg("them", "I know :("),
                phone_msg("me", "Send me both versions when you have them."),
                phone_msg("them", "Can I call instead? It'll sound awful in voice notes."),
                phone_msg("me", "Sure."),
            ],
        },

        {
            "id": "monika_bookmark_number",
            "contact": "Monika",
            "kind": "text",
            "unlock": [("seen", "monika_four_bars"), ("date", "0529")],
            "body": [
                phone_msg("me", "What's the 47 on the bookmark you lent me?"),
                phone_msg("them", "Oh no."),
                phone_msg("me", "Helpful."),
                phone_msg("them", "It could be a page number?"),
                phone_msg("me", "It was sitting at page 86."),
                phone_msg("them", "Wait--does it have a circle around it?"),
                phone_msg("me", "No."),
                phone_msg("them", "Then I have absolutely no idea."),
                phone_msg("me", "Okay."),
                phone_msg("them", "Sorry!! I really don't remember"),
                phone_msg("me", "It's fine. I was just checking."),
            ],
        },

        {
            "id": "matsuda_omen",
            "contact": "Matsuda Akai",
            "kind": "text",
            "unlock": ("open", "matsuda"),
            "body": [
                phone_msg("me", "Still playing?"),
                phone_msg("them", "More importantly, the vending machine gave me two drinks."),
                phone_msg("me", "That's unrelated."),
                phone_msg("them", "Nothing is unrelated when the universe is paying attention."),
                phone_msg("me", "Loose spring."),
                phone_msg("them", "Omen."),
                phone_msg("me", "What flavor?"),
                phone_msg("them", "Coffee and melon soda."),
                phone_msg("them", "Do you want the soda or not"),
                phone_msg("me", "Yeah."),
            ],
        },

        {
            "id": "matsuda_patch_notes",
            "contact": "Matsuda Akai",
            "kind": "text",
            "unlock": [("seen", "matsuda_omen"), ("date", "0522")],
            "body": [
                phone_msg("me", "Final verdict on the game?"),
                phone_msg("them", "PATCH NOTES:"),
                phone_msg("them", "combat: delicious"),
                phone_msg("them", "story: suspiciously literate"),
                phone_msg("them", "menu: still ass"),
                phone_msg("me", "You sound invested."),
                phone_msg("them", "I found the fishing minigame."),
                phone_msg("me", "There is no water in that game."),
                phone_msg("them", "THERE IS ONE FOUNTAIN."),
                phone_msg("me", "How long?"),
                phone_msg("them", "..."),
                phone_msg("them", "irrelevant"),
            ],
        },

        {
            "id": "matsuda_dice_test",
            "contact": "Matsuda Akai",
            "kind": "text",
            "unlock": [("seen", "matsuda_patch_notes"), ("date", "0526")],
            "body": [
                phone_msg("me", "Do those dice earrings actually roll?"),
                phone_msg("them", "Only one way to find out."),
                phone_msg("them", "hold on"),
                phone_msg("them", "..."),
                phone_msg("them", "it rolled"),
                phone_msg("me", "What'd you get?"),
                phone_msg("them", "under the dresser"),
                phone_msg("me", "That's not a number."),
                phone_msg("them", "idk i cant see it"),
                phone_msg("me", "Need help?"),
                phone_msg("them", "No. Preserve my dignity."),
                phone_msg("them", "actually yes do you have a flashlight"),
                phone_msg("me", "You're holding one."),
                phone_msg("them", "..."),
                phone_msg("them", "dont say anything"),
            ],
        },

        {
            "id": "matsuda_hat_setup",
            "contact": "Matsuda Akai",
            "kind": "text",
            # Old saves may already have seen the original hat call. Do not give
            # those players a new text that points at a camera key with no call.
            "unlock": [("open", "matsuda_video"), ("seen", "matsuda_dice_test"), ("unseen", "matsuda_hat")],
            "body": [
                phone_msg("me", "Did you find the earring?"),
                phone_msg("them", "Yes. More importantly, I own something greater."),
                phone_msg("me", "That sounds expensive."),
                phone_msg("them", "Worse. Words would reduce it."),
                phone_msg("me", "That's never stopped you before."),
                phone_msg("them", "Camera. Now."),
            ],
        },

        # --- voice calls ------------------------------------------------------

        {
            "id": "asa_tier_argument",
            "contact": "Asa",
            "kind": "call",
            "unlock": [("seen", "asa_controller"), ("date", "0529")],
            "status": "Connected",
            "body": [
                phone_call_line("them", "Why are you calling me?"),
                phone_call_line("me", "Because typing this is taking too long. The healer isn't S-tier."),
                phone_call_line("them", "Wrong."),
                phone_call_line("me", "You spend every fight on the floor."),
                phone_call_line("them", "Because nobody protects me!"),
                phone_call_line("me", "You're the healer."),
                phone_call_line("them", "I can't heal if I'm dead!"),
                phone_call_line("me", "That's my point."),
                phone_call_line("them", "No, your point is--wait. I had a point."),
                phone_call_note("Buttons click rapidly on her end."),
                phone_call_line("me", "Are you playing right now?"),
                phone_call_line("them", "Maybe."),
                phone_call_line("me", "You're dead again, aren't you?"),
                phone_call_note("The buttons stop."),
                phone_call_line("them", "...Yeah."),
            ],
        },

        {
            "id": "mom_big_pot",
            "contact": "Mom",
            "kind": "call",
            "unlock": ("open", "mom_call"),
            "status": "Connected",
            "body": [
                phone_call_line("them", "Hi. Everything okay?"),
                phone_call_line("me", "Yeah. What's the actual name of the big pot?"),
                phone_call_line("them", "The stockpot."),
                phone_call_line("me", "Then why don't we call it that?"),
                phone_call_line("them", "I did. Asahina asked what stock we kept in it."),
                phone_call_line("me", "She was joking."),
                phone_call_line("them", "She maintained eye contact for an uncomfortable amount of time."),
                phone_call_line("me", "So...maybe not."),
                phone_call_line("them", "Exactly. Big pot."),
                phone_call_line("me", "That's all I needed."),
                phone_call_line("them", "I'm glad we resolved this."),
            ],
        },

        {
            "id": "mom_house_rule",
            "contact": "Mom",
            "kind": "call",
            "unlock": [("open", "mom_call"), ("seen", "mom_big_pot"), ("date", "0530")],
            "status": "Connected",
            "body": [
                phone_call_line("them", "Hello?"),
                phone_call_line("me", "Copper Crown. If the market locks, do you still draw?"),
                phone_call_line("them", "No."),
                phone_call_line("me", "Asa says yes."),
                phone_call_line("them", "Asahina also buys every attack card she sees."),
                phone_call_line("me", "That's not evidence."),
                phone_call_line("them", "It's character evidence."),
                phone_call_note("Cardboard scrapes against wood. Pages turn."),
                phone_call_line("them", "Oh. No, wait--that's the solo rule. One second."),
                phone_call_note("Another page turns."),
                phone_call_line("them", "Yes. She was right."),
                phone_call_line("me", "I'll tell her."),
                phone_call_line("them", "You don't need to sound that pleased."),
                phone_call_line("me", "I really do."),
            ],
        },

        {
            "id": "monika_paragraph",
            "contact": "Monika",
            "kind": "call",
            "unlock": ("open", "monika_call"),
            "status": "Connected",
            "body": [
                phone_call_line("them", "Hey! What's up?"),
                phone_call_line("me", "Quick question. If a poem doesn't rhyme, when does it turn into a paragraph?"),
                phone_call_line("them", "Is this about something you're writing?"),
                phone_call_line("me", "That's not an answer."),
                phone_call_line("them", "You called me with a poem question. It counts."),
                phone_call_line("me", "I'm working on nothing."),
                phone_call_line("them", "Mm-hm."),
                phone_call_note("A page turns on her end."),
                phone_call_line("them", "Can I read the nothing when it's done?"),
                phone_call_line("me", "...Maybe."),
            ],
        },

        {
            "id": "monika_two_versions",
            "contact": "Monika",
            "kind": "call",
            "unlock": [("open", "monika_call"), ("seen", "monika_paragraph"), ("seen", "monika_four_bars"), ("date", "0528")],
            "status": "Connected",
            "body": [
                phone_call_line("them", "Hi!"),
                phone_call_line("me", "I have headphones. Go ahead."),
                phone_call_line("them", "Perfect! Okay, don't say anything until you hear both."),
                phone_call_note("Four quiet piano bars play through the speaker."),
                phone_call_line("them", "That's one."),
                phone_call_note("The same four bars play again."),
                phone_call_line("them", "And...two."),
                phone_call_line("me", "They were the same."),
                phone_call_line("them", "No, they weren't."),
                phone_call_line("me", "Play two again."),
                phone_call_note("The phrase repeats. A bench creaks, then nothing."),
                phone_call_line("them", "...I opened the wrong recording."),
                phone_call_line("me", "I was about to lie politely."),
                phone_call_line("them", "Don't! Give me one second--"),
                phone_call_note("The phone touches down. A different ending follows; the last chord lifts instead of falling."),
                phone_call_line("them", "Okay. That was two."),
                phone_call_line("me", "Two."),
                phone_call_line("them", "That fast?"),
                phone_call_line("me", "Yeah."),
                phone_call_line("them", "Okay...good. I need to play it again. Thanks!"),
            ],
        },

        {
            "id": "matsuda_boss_name",
            "contact": "Matsuda Akai",
            "kind": "call",
            "unlock": [("seen", "matsuda_hat"), ("date", "0530")],
            "status": "Connected",
            "body": [
                phone_call_line("them", "Speak."),
                phone_call_line("me", "What was the name of that boss you hated?"),
                phone_call_line("them", "...Give me a second."),
                phone_call_line("me", "You forgot."),
                phone_call_line("them", "I remember the fight. Names are ornamental."),
                phone_call_line("me", "I need it to find a guide."),
                phone_call_line("them", "The magistrate...something."),
                phone_call_note("Rapid tapping, then a muffled groan."),
                phone_call_line("them", "Do NOT look it up before I do."),
                phone_call_line("me", "Too late."),
                phone_call_line("them", "Was it Geryon?"),
                phone_call_line("me", "No."),
                phone_call_line("them", "Don't tell me."),
            ],
        },

        # --- video calls ------------------------------------------------------

        {
            "id": "matsuda_hat",
            "contact": "Matsuda Akai",
            "kind": "facetime",
            # The preceding text explicitly sends the player to the camera key.
            "unlock": [("open", "matsuda_video"), ("seen", "matsuda_hat_setup")],
            "sprite": "phone_matsuda_duck_hat",
            "body": [
                phone_call_line("them", "Can you see the whole thing?"),
                phone_call_line("me", "I can see a duck."),
                phone_call_line("them", "Good. The duck is the whole thing."),
                phone_call_note("The feed drops to her jacket, then jerks back up."),
                phone_call_line("them", "Wait--there. Better?"),
                phone_call_line("me", "You bought that?"),
                phone_call_line("them", "Tsubaki said I wouldn't wear it in public."),
                phone_call_line("me", "So you bought it out of spite."),
                phone_call_line("them", "No. I bought it because I have vision."),
                phone_call_line("me", "Are you wearing that outside?"),
                phone_call_line("them", "...Depends."),
                phone_call_line("me", "On?"),
                phone_call_line("them", "Whether you say it looks good."),
                phone_call_line("me", "It looks good."),
                phone_call_line("them", "...Good."),
                phone_call_note("She reaches for the end-call button, misses, and fills the feed with one yellow wing."),
                phone_call_line("them", "How do I--"),
                phone_call_note("The feed cuts out."),
            ],
        },
    ]


# Which of these have already happened, per save.
default phone_random_seen = []

# Which lines the story has opened, per save. One `default` each rather than a
# set, so ("flag", "phone_open_x") keeps working as a plain store read and the
# whole list is greppable. Opened by phone_open() -- see PHONE_OPEN_CHANNELS
# above for which beat opens which.
default phone_open_asa = False
default phone_open_mom = False
default phone_open_mom_call = False
default phone_open_monika = False
default phone_open_monika_call = False
default phone_open_matsuda = False
default phone_open_matsuda_video = False


# =============================================================================
# PUBLIC: play one conversation by id. Called in a new context by
# phone_random_launch, so it must end by returning and nothing else.
# =============================================================================
label phone_random_play(entry_id):
    $ _prc_entry = phone_random_entry(entry_id)

    if _prc_entry is None:
        return

    $ _prc_kind = _prc_entry.get("kind", "text")
    $ _prc_contact = _prc_entry["contact"]
    $ _prc_body = phone_random_body(_prc_entry)
    # Marked before it plays, not after: if the player rolls back out of the
    # middle of one, it should still not be offered again as though it never
    # happened.
    $ phone_random_mark_seen(entry_id)

    if _prc_kind == "call":
        call phone_call_conversation(_prc_contact, _prc_body, _prc_entry.get("status", "Connected")) from _call_phone_random_call

    elif _prc_kind == "facetime":
        call phone_facetime(_prc_contact, _prc_body, sprite=_prc_entry.get("sprite")) from _call_phone_random_facetime

    else:
        # append=True so idle chatter lands in the same thread as the story's
        # messages and the player scrolls back through one continuous history.
        call phone_text_conversation(_prc_contact, _prc_body, _prc_entry.get("status", "Messages"), append=True) from _call_phone_random_text

    return
