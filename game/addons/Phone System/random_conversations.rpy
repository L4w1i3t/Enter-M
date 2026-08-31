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
#     unlock   see phone_random_unlocked below. Defaults to "met", but prefer an
#              ("open", channel) and/or date gate so the chatter arrives after
#              the story has earned it. Runtime entries stay independent: never
#              gate one on another random conversation's seen state.
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
# ONE-SHOT AND INDEPENDENT BY DESIGN
#   Each conversation plays once per save (phone_random_seen) and text ones are
#   appended to the real thread, so the history the player scrolls back through
#   is the history they actually made. Catalog entries may wait for a story beat
#   or date, but none depends on another random conversation being played first.
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
    #   monika_video   0525  their long study day and night check-in make an
    #                        unplanned video call a natural next step
    #   matsuda        0520  the first time she reaches out that ISN'T May 17 --
    #                        May 17 is the introduction, and a number taken off a
    #                        sidewalk collision is not yet an open line
    #   matsuda_video  0529  by now she is sending unprompted bits; a camera is
    #                        the natural next escalation for her specifically
    #
    # All eight land inside Chapter 0.5, so a player who finishes the prologue has
    # had the chance at every idle conversation currently written.
    PHONE_OPEN_CHANNELS = (
        "asa", "mom", "mom_call", "monika", "monika_call", "monika_video", "matsuda", "matsuda_video",
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
        "monika_video": "0525",
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
    # Old saves may still contain these strings in phone_random_seen. Keeping
    # only the IDs documents that harmless state without constructing retired
    # message bodies or calling phone_msg helpers during init.
    PHONE_RANDOM_RETIRED_IDS = (
        "asa_leftovers",
        "asa_spider",
        "asa_wrong_chat",
        "asa_controller",
        "asa_poster_rescue",
        "mom_discoverable",
        "mom_laundry_receipt",
        "mom_mug_inquiry",
        "monika_waypoint",
        "monika_asterisk",
        "monika_four_bars",
        "monika_bookmark_number",
        "matsuda_omen",
        "matsuda_patch_notes",
        "matsuda_dice_test",
        "matsuda_hat_setup",
        "asa_tier_argument",
        "mom_big_pot",
        "mom_house_rule",
        "monika_paragraph",
        "monika_two_versions",
        "matsuda_boss_name",
        "matsuda_hat",
    )

    # The 2026-08-30 rebuild. These twelve entries are the only runtime random
    # conversations. Their fresh IDs ensure existing saves can see the rewritten
    # material even if they completed a retired conversation with a similar idea.
    PHONE_RANDOM_CONVERSATIONS = [

        # --- Asahina ---------------------------------------------------------

        {
            "id": "rc2_asa_ashen_vow",
            "contact": "Asa",
            "kind": "text",
            "unlock": ("open", "asa"),
            "body": [
                phone_msg("me", "How's Ashen Vow going?"),
                phone_msg("them", "bell widow killed me again"),
                phone_msg("them", "her grab hitbox is actual fraud"),
                phone_msg("me", "Git gud."),
                phone_msg("them", "i asked for SUPPORT"),
                phone_msg("me", "That was support."),
                phone_msg("them", "i hope ur next boss has 4 phases"),
            ],
        },

        {
            "id": "rc2_asa_mr_toast",
            "contact": "Asa",
            "kind": "text",
            "unlock": [("open", "asa"), ("date", "0523")],
            "body": [
                phone_msg("me", "Did you find Mr. Toast?"),
                phone_msg("them", "NO"),
                phone_msg("them", "and dont act innocent"),
                phone_msg("me", "I haven't touched your stuffed rabbit."),
                phone_msg("them", "he was on my pillow and now hes GONE"),
                phone_msg("me", "Check under the blanket."),
                phone_msg("them", "checked"),
                phone_msg("me", "Laundry basket?"),
                phone_msg("them", "CHECKED"),
                phone_msg("them", "if u hid him i swear"),
                phone_msg("me", "Look between the bed and the wall."),
                phone_msg("them", "..."),
                phone_msg("me", "Well?"),
                phone_msg("them", "he fell"),
                phone_msg("me", "The kidnapping case collapses."),
                phone_msg("them", "he was scared and alone asshole"),
                phone_msg("me", "Tell him I'm sorry gravity did that."),
                phone_msg("them", "tell him urself"),
            ],
        },

        {
            "id": "rc2_asa_soup_store",
            "contact": "Asa",
            "kind": "call",
            "unlock": ["met", ("date", "0527")],
            "status": "Connected",
            "body": [
                phone_call_line("them", "What?"),
                phone_call_line("me", "You left for detergent forty minutes ago. Where are you?"),
                phone_call_line("them", "The store."),
                phone_call_line("me", "Which part of the store?"),
                phone_call_line("them", "Clothes."),
                phone_call_line("me", "Why do I hear cans?"),
                phone_call_note("Metal clatters somewhere on her end."),
                phone_call_line("them", "Because I'm by the soup."),
                phone_call_line("me", "Why are you shopping for clothes in the soup aisle?"),
                phone_call_line("them", "I'm not! I thought the sign said apparel!"),
                phone_call_line("me", "The sign led you to soup?"),
                phone_call_line("them", "That's why I followed the arrow!"),
                phone_call_line("me", "Read it again."),
                phone_call_note("A long silence. A cart squeaks past."),
                phone_call_line("them", "...It says appetizers."),
                phone_call_line("me", "Come home."),
                phone_call_line("them", "I still need detergent!"),
                phone_call_line("me", "Then stop buying imaginary clothes next to the soup!"),
                phone_call_line("them", "I'M LOOKING FOR THE EXIT!"),
            ],
        },

        # --- Matsuda ---------------------------------------------------------

        {
            "id": "rc2_matsuda_ui_review",
            "contact": "Matsuda Akai",
            "kind": "text",
            "unlock": [("open", "matsuda"), ("date", "0521")],
            "body": [
                phone_msg("me", "Final verdict on the game?"),
                phone_msg("them", "Combat sings. Story has teeth. Soundtrack could resurrect a mall."),
                phone_msg("me", "That's positive."),
                phone_msg("them", "HOWEVER"),
                phone_msg("them", "the inventory sort resets every time you equip something"),
                phone_msg("them", "the map cursor snaps back to the shrine whenever i breathe"),
                phone_msg("them", "and it asks me to confirm closing the menu"),
                phone_msg("me", "That last one sounds considerate."),
                phone_msg("them", "No. The UI can eat my fat ass."),
                phone_msg("me", "Score?"),
                phone_msg("them", "Nine out of ten"),
                phone_msg("me", "Despite the jank?"),
                phone_msg("them", "I didn't say the jank was bad"),
                phone_msg("me", "You...just said it could eat your ass though?"),
                phone_msg("them", "Not the same thing, don't make it weird"),
                phone_msg("me", "???????????????"),
            ],
        },

        {
            "id": "rc2_matsuda_wrong_person",
            "contact": "Matsuda Akai",
            "kind": "text",
            "unlock": [("open", "matsuda"), ("date", "0525")],
            "body": [
                phone_msg("them", "if he calls the game fine again put me out of my misery"),
                phone_msg("me", "Do I want to know who that was meant for?"),
                phone_msg("them", "What was meant for whom"),
                phone_msg("me", "The message directly above this one."),
                phone_msg("them", "..."),
                phone_msg("them", "Kareda."),
                phone_msg("me", "Thought so."),
                phone_msg("them", "Why were you in her contact slot?"),
                phone_msg("me", "I wasn't. You selected me."),
                phone_msg("them", "Your names occupy adjacent spiritual territory."),
                phone_msg("me", "They aren't alphabetically adjacent either."),
                phone_msg("them", "Then your phone number was standing suspiciously close to hers."),
                phone_msg("me", "On your phone."),
                phone_msg("them", "At last, we locate the crime scene."),
                phone_msg("me", "You texted the wrong person and somehow I'm at fault."),
                phone_msg("them", "I'm glad you understand."),
            ],
        },

        {
            "id": "rc2_matsuda_duck_hat",
            "contact": "Matsuda Akai",
            "kind": "facetime",
            "unlock": ("open", "matsuda_video"),
            "sprite": "phone_matsuda_duck_hat",
            "body": [
                phone_call_line("them", "Can you see the whole thing?"),
                phone_call_line("me", "I can see one enormous duck eye."),
                phone_call_note("The feed jerks back. A yellow beak, two soft wings, and Matsuda's grin come into frame."),
                phone_call_line("them", "Behold. The apex of modern headwear."),
                phone_call_line("me", "You called me to show off a duck hat."),
                phone_call_line("them", "I called because text cannot carry its majesty."),
                phone_call_line("me", "Did you buy it?"),
                phone_call_line("them", "Tsubaki said I lacked the courage to wear it in public."),
                phone_call_line("me", "So you bought it out of spite."),
                phone_call_line("them", "No. I bought it because doubt demands rebuttal."),
                phone_call_line("me", "Are you actually wearing it outside?"),
                phone_call_line("them", "...That depends."),
                phone_call_line("me", "On what?"),
                phone_call_line("them", "Whether it looks good."),
                phone_call_line("me", "It looks good."),
                phone_call_note("Her grin goes still for half a beat."),
                phone_call_line("them", "Correct answer."),
                phone_call_note("She reaches for the end-call button, misses, and fills the camera with one yellow wing."),
                phone_call_line("them", "How do I--"),
                phone_call_note("The feed cuts out."),
            ],
        },

        # --- Himeko ----------------------------------------------------------

        {
            "id": "rc2_mom_mid",
            "contact": "Mom",
            "kind": "text",
            "unlock": ("open", "mom"),
            "body": [
                phone_msg("me", "Why did you ask if dinner was mid?"),
                phone_msg("them", "Asahina used the word. I am establishing what she meant before I respond."),
                phone_msg("me", "It means average. Mediocre."),
                phone_msg("them", "I see."),
                phone_msg("them", "She had seconds."),
                phone_msg("me", "Then her testimony conflicts with the physical evidence."),
                phone_msg("them", "Precisely."),
                phone_msg("me", "Are you going to confront her?"),
                phone_msg("them", "No. I am making the same dinner Thursday."),
                phone_msg("me", "Cold."),
                phone_msg("them", "Apparently only mid."),
            ],
        },

        {
            "id": "rc2_mom_autocorrect",
            "contact": "Mom",
            "kind": "text",
            "unlock": [("open", "mom"), ("date", "0526")],
            "body": [
                phone_msg("me", "Did you mean to ask me to 'defrost the witness'?"),
                phone_msg("them", "Chicken. I typed chicken."),
                phone_msg("me", "Your keyboard has been at work too long."),
                phone_msg("them", "Please take the client breasts out of the freezer."),
                phone_msg("them", "CHICKEN BREASTS."),
                phone_msg("me", "I was going to give context a chance."),
                phone_msg("them", "Put them in the sink. Do not cook the children."),
                phone_msg("them", "CHICKEN."),
                phone_msg("me", "This is becoming discoverable."),
                phone_msg("them", "Please disregard every sentence my phone has offered into evidence."),
                phone_msg("me", "I'll defrost the chicken."),
                phone_msg("them", "Thank you. I am turning autocorrect off before it ends my career."),
            ],
        },

        {
            "id": "rc2_mom_work_opinion",
            "contact": "Mom",
            "kind": "call",
            "unlock": [("open", "mom_call"), ("date", "0528")],
            "status": "Connected",
            "body": [
                phone_call_line("them", "Good timing. I need a civilian opinion."),
                phone_call_line("me", "That's a comforting way to describe your son."),
                phone_call_line("them", "The firm is doing a free tenant-rights workshop. Which title would make you attend?"),
                phone_call_line("them", "'Residential Tenancy Rights and Obligations,' or 'Know Your Lease Before You Sign'?"),
                phone_call_line("me", "The second one, easily."),
                phone_call_line("them", "Why?"),
                phone_call_line("me", "The first sounds like homework assigned by a building."),
                phone_call_note("A pen scratches across paper on her end."),
                phone_call_line("them", "Good. That is almost exactly what I told my partner."),
                phone_call_line("me", "So I'm not giving an opinion. I'm supplying ammunition."),
                phone_call_line("them", "Independent corroboration."),
                phone_call_line("me", "Do I get credit?"),
                phone_call_line("them", "You get dinner and the satisfaction of improving public outreach."),
                phone_call_line("me", "Dinner was already in the contract."),
                phone_call_line("them", "Then I raised you to negotiate. I'm very proud."),
            ],
        },

        # --- Monika ----------------------------------------------------------

        {
            "id": "rc2_monika_vague_draft",
            "contact": "Monika",
            "kind": "text",
            "unlock": [("open", "monika"), ("date", "0519")],
            "body": [
                phone_msg("me", "You said you wanted an opinion on your draft?"),
                phone_msg("them", "Yes! Do you think the opening is too quiet?"),
                phone_msg("me", "What happens in it?"),
                phone_msg("them", "It establishes the mood."),
                phone_msg("me", "What mood?"),
                phone_msg("them", "The one the rest of the piece complicates."),
                phone_msg("me", "Genre?"),
                phone_msg("them", "It would bias you if I said."),
                phone_msg("me", "Length?"),
                phone_msg("them", "Longer than the opening, shorter than it might be."),
                phone_msg("me", "Have I read a single word of this?"),
                phone_msg("them", "Not yet! It's not ready."),
                phone_msg("me", "Then my official opinion is that it certainly exists."),
                phone_msg("them", "I knew you'd understand."),
                phone_msg("me", "I understand nothing."),
                phone_msg("them", "Perfect. Fresh eyes~"),
            ],
        },

        {
            "id": "rc2_monika_horror_verdict",
            "contact": "Monika",
            "kind": "text",
            "unlock": [("open", "monika"), ("date", "0524")],
            "body": [
                phone_msg("me", "Why did the horror committee send me a verdict?"),
                phone_msg("them", "Because you were tried in absentia."),
                phone_msg("me", "For what?"),
                phone_msg("them", "You said practical effects don't automatically make a movie good."),
                phone_msg("me", "They don't."),
                phone_msg("them", "Count one: aggravated bad taste."),
                phone_msg("them", "Count two: reckless indifference to texture."),
                phone_msg("them", "Count three: disrespecting a model train that took six weeks to build."),
                phone_msg("me", "The model train was excellent. The movie wasn't."),
                phone_msg("them", "The court recognizes no distinction."),
                phone_msg("me", "Sentence?"),
                phone_msg("them", "You have to watch the director's cut with me."),
                phone_msg("me", "This committee is corrupt."),
                phone_msg("them", "Objection overruled~"),
            ],
        },

        {
            "id": "rc2_monika_vp_rant",
            "contact": "Monika",
            "kind": "facetime",
            "unlock": ("open", "monika_video"),
            "body": [
                phone_call_line("them", "Oh, good. You're here. I need a neutral witness."),
                phone_call_line("me", "I thought this was a normal video call."),
                phone_call_line("them", "It was, until the vice president sent me meeting minutes with no minutes in them."),
                phone_call_line("me", "An empty file?"),
                phone_call_line("them", "Worse. A title page, three decorative lines, and 'Monika will fill in the details.'"),
                phone_call_note("She lifts a printed page to the camera. Most of it is, indeed, blank."),
                phone_call_line("them", "He also approved the basketball club and drama club for the gym at the same time."),
                phone_call_line("me", "Joint production?"),
                phone_call_line("them", "Don't give him ideas! He'll call it interdisciplinary and leave me to schedule it."),
                phone_call_line("me", "Have you told him any of this?"),
                phone_call_line("them", "I used calm words. He said we'd circle back."),
                phone_call_line("them", "If he says circle back one more time, I'm making him physically circle the building."),
                phone_call_line("me", "Very presidential."),
                phone_call_line("them", "I am off the clock and he is bad at his job."),
                phone_call_note("Her eyes narrow at something below the camera."),
                phone_call_line("them", "Are you reaching for the end-call button?"),
                phone_call_line("me", "No."),
                phone_call_line("them", "Your thumb is in frame."),
                phone_call_line("me", "I was adjusting morale."),
                phone_call_line("them", "Great. Morale can stay for the budget story."),
                phone_call_line("me", "There's a budget story?"),
                phone_call_line("them", "There are three."),
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
default phone_open_monika_video = False
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
