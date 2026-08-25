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
            return bool(getattr(store, "phone_open_" + str(value), False))

        if kind == "seen":
            return value in phone_state_list("phone_random_seen")

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

        The phone screens are closed first and the contacts list is reopened
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
        renpy.show_screen("phone_contacts_screen")


    # =========================================================================
    # THE CATALOG
    # Casual, throwaway, and in character. Voices, for reference:
    #   Asa      all lowercase, no apostrophes, texts like she talks
    #   Mom      a civil lawyer and good at her job. Complete sentences, precise,
    #            dryly funny, warm underneath. She is NOT bad with technology and
    #            is never the butt of the joke for not understanding something --
    #            her comedy is understatement and being tired, not incompetence
    #   Monika   chatty, over-punctuated, enthusiastic about small things
    #   Matsuda  theatrical one line, completely blunt the next
    #   MC       dry, short, gives in eventually
    # =========================================================================
    PHONE_RANDOM_CONVERSATIONS = [

        {
            "id": "asa_leftovers",
            "contact": "Asa",
            "kind": "text",
            "unlock": ("open", "asa"),
            "body": [
                phone_msg("them", "did u eat the last of the rice"),
                phone_msg("me", "No."),
                phone_msg("them", "u hesitated"),
                phone_msg("me", "This is a text message. You can't see me hesitate."),
                phone_msg("them", "i can FEEL it"),
                phone_msg("me", "I ate the last of the rice."),
                phone_msg("them", "KNEW IT"),
                phone_msg("them", "ur buying me food. thats the law now"),
            ],
        },

        {
            "id": "asa_spider",
            "contact": "Asa",
            "kind": "text",
            "unlock": ("seen", "asa_leftovers"),
            "body": [
                phone_msg("them", "code red"),
                phone_msg("them", "theres a thing in the bathroom"),
                phone_msg("me", "What kind of thing?"),
                phone_msg("them", "a spider thing"),
                phone_msg("them", "its doing a POSE"),
                phone_msg("me", "Spiders don't pose."),
                phone_msg("them", "this one is POSING"),
                phone_msg("me", "You're one room away from me."),
                phone_msg("them", "then COME GET IT"),
            ],
        },

        {
            "id": "asa_wrong_chat",
            "contact": "Asa",
            "kind": "text",
            # Last of the Asa ladder: the joke only lands once she has already
            # been caught out twice.
            "unlock": ("seen", "asa_spider"),
            "body": [
                phone_msg("them", "ok but dont tell my brother"),
                phone_msg("me", "I am your brother."),
                phone_msg("them", "..."),
                phone_msg("them", "wrong chat"),
                phone_msg("me", "Don't tell me what?"),
                phone_msg("them", "wrong chat!!!!"),
                phone_msg("me", "Asa."),
                phone_msg("them", "goodnight"),
            ],
        },

        {
            "id": "mom_discoverable",
            "contact": "Mom",
            "kind": "text",
            "unlock": ("open", "mom"),
            "body": [
                phone_msg("them", "Question. Your sister described her day as 'mid'."),
                phone_msg("them", "Context suggests it is not a compliment."),
                phone_msg("me", "It means mediocre."),
                phone_msg("them", "Mediocre."),
                phone_msg("me", "Yeah."),
                phone_msg("them", "She used it about my cooking."),
                phone_msg("me", "..."),
                phone_msg("me", "I'm going to need you to forget I confirmed that."),
                phone_msg("them", "Too late. It's discoverable."),
            ],
        },

        {
            "id": "monika_waypoint",
            "contact": "Monika",
            "kind": "text",
            "unlock": ("open", "monika"),
            "body": [
                phone_msg("them", "Okay, I finished it and I need someone to be normal about this with me."),
                phone_msg("them", "Are you normal about books?"),
                phone_msg("me", "Historically, no."),
                phone_msg("them", "Perfect!!"),
                phone_msg("them", "So there's this bit on page 212 where--"),
                phone_msg("them", "No. No, you have to read it clean. I'm not spoiling it."),
                phone_msg("me", "You already sent me the page number."),
                phone_msg("them", "That's not a spoiler, that's a waypoint."),
                phone_thumb("me"),
            ],
        },

        {
            "id": "monika_asterisk",
            "contact": "Monika",
            "kind": "text",
            # Her second one. Typing three corrections in a row at someone is a
            # thing you do to a person you already text badly at.
            "unlock": ("seen", "monika_waypoint"),
            "body": [
                phone_msg("them", "hey do you still have the handout form yesterday"),
                phone_msg("them", "*from"),
                phone_msg("them", "*handout"),
                phone_msg("them", "I don't know what happened there."),
                phone_msg("me", "You spelled 'handout' correctly the first time."),
                phone_msg("them", "Let me have this."),
            ],
        },

        {
            "id": "matsuda_omen",
            "contact": "Matsuda Akai",
            "kind": "text",
            "unlock": ("open", "matsuda"),
            "body": [
                phone_msg("them", "The vending machine has given me two drinks."),
                phone_msg("them", "This is an omen."),
                phone_msg("me", "It's a loose spring."),
                phone_msg("them", "It is an OMEN, %NAME%."),
                phone_msg("them", "The universe has selected me for something."),
                phone_msg("me", "For what?"),
                phone_msg("them", "I'll know when it happens."),
                phone_msg("them", "Do you want the second one or not"),
                phone_msg("me", "Yes."),
            ],
        },

        # --- voice calls ------------------------------------------------------

        {
            "id": "mom_big_pot",
            "contact": "Mom",
            "kind": "call",
            "unlock": ("open", "mom_call"),
            "status": "Connected",
            "body": [
                phone_call_line("them", "Where is the big pot?"),
                phone_call_line("me", "Which big pot?"),
                phone_call_line("them", "The big one."),
                phone_call_note("There are three pots in this house and all of them are the big one."),
                phone_call_line("me", "Cabinet under the sink."),
                phone_call_line("them", "That is the bucket."),
                phone_call_line("me", "...Then the cupboard over the fridge."),
                phone_call_line("them", "That is where the vases live."),
                phone_call_line("me", "You put it there."),
                phone_call_line("them", "I would never."),
                phone_call_note("A cabinet opens. A long pause."),
                phone_call_line("them", "I put it there."),
            ],
        },

        {
            "id": "monika_paragraph",
            "contact": "Monika",
            "kind": "call",
            "unlock": ("open", "monika_call"),
            "status": "Connected",
            "body": [
                phone_call_line("them", "Are you outside? I can hear outside."),
                phone_call_line("me", "Walking home."),
                phone_call_line("them", "Oh, don't let me keep you--"),
                phone_call_line("me", "You're not."),
                phone_call_line("them", "Okay, good, because I have a question and it's a stupid one."),
                phone_call_line("me", "Go."),
                phone_call_line("them", "If a poem doesn't rhyme, is it still a poem, or is it a paragraph with confidence?"),
                phone_call_line("me", "The second one. Definitely the second one."),
                phone_call_line("them", "That's what I said! Nobody agrees with me!"),
                phone_call_note("A car goes past. She waits it out."),
                phone_call_line("them", "...Anyway. Get home safe."),
            ],
        },

        # --- video calls ------------------------------------------------------

        {
            "id": "matsuda_hat",
            "contact": "Matsuda Akai",
            "kind": "facetime",
            # Both: the camera has to be on the table AND she has to have already
            # pulled the vending-machine bit, or "Behold" arrives with no runway.
            "unlock": [("open", "matsuda_video"), ("seen", "matsuda_omen")],
            "body": [
                phone_call_line("them", "Behold."),
                phone_call_line("me", "That's a hat."),
                phone_call_line("them", "It is a STATEMENT."),
                phone_call_line("me", "It's a hat with a duck on it."),
                phone_call_line("them", "The duck is the statement."),
                phone_call_note("She turns the camera to show the duck from a second angle."),
                phone_call_line("them", "Verdict."),
                phone_call_line("me", "...It's a good hat."),
                phone_call_line("them", "I KNEW you had taste. Everyone said you didn't."),
                phone_call_line("me", "Who's everyone?"),
                phone_call_line("them", "Goodbye!"),
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
