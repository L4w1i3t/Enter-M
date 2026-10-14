# Optional conversations selected from PHONE_RANDOM_CONVERSATIONS by contact/kind.
# Each permanent id plays once per save (phone_random_seen); texts append to saved
# threads. Unlocks use met/contact-channel/date gates and remain independent of
# other optional conversations. Story events supply progression requirements.
#
# Entries supply id, contact, kind, unlock and body; facetime may override sprite.
# Kinds are text/call/facetime. Bodies use message or call-line builders accordingly.
# Use %NAME% for the player's name: playback substitutes it before incremental
# typing, so incomplete interpolation syntax never reaches the text renderer.
# Phone-only art uses the normalized 640x960 feed canvas.

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

        The story year starts in May and runs into March, so a plain MMDD
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
            today = _phone_random_story_key(snapshot["month"], snapshot["day"])

            # CalendarSystem's clean-store placeholder is April 7. April is
            # outside the May 15 -> March 7 story, but cyclic ordering places it
            # after every real story date. Treat all out-of-story dates as no
            # date at all so a fresh standalone run cannot satisfy fallbacks.
            story_start = _phone_random_story_key(5, 15)
            story_end = _phone_random_story_key(3, 7)
            if today < story_start or today > story_end:
                return None

            return today
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

            # Compatibility is still derived from THIS save. A bare calendar
            # date is not enough: clean side content starts on April 7 and used
            # to invent contacts and eleven ready conversations from nothing.
            if contact_id not in phone_state_list("phone_met_contacts"):
                return False

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
        if not enter_m_main_story_active():
            return []

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

    def phone_random_count(contact_id=None, kind=None):
        return len(phone_random_available(contact_id, kind))

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

    def phone_random_launch(contact_id, kind, return_to_home=False):
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
        if not enter_m_main_story_active():
            return None

        # A second launch over a live phone interaction would overwrite its
        # temporary playback state. Check the active playback screens rather
        # than context depth: a blocking inbox can be called in a new context,
        # and returning from a menu must not leave its ready buttons inert.
        if any(renpy.get_screen(name) for name in (
            "phone_text_screen", "phone_thread_static", "phone_call_screen",
            "phone_active_call_screen", "phone_video_call_screen",
        )):
            return None

        entry_id = phone_random_next_id(contact_id, kind)
        if entry_id is None:
            return None

        renpy.hide_screen("phone_thread_history_screen")
        renpy.hide_screen("phone_contacts_screen")
        renpy.hide_screen("phone_home_screen")
        renpy.hide_screen("phone_notification_alert")
        # Contexts isolate the script stack and screens, but these window
        # variables live in the shared store. A child `call screen` hides the
        # window; leaking that flag makes the parent's next say dissolve in.
        # Restore the exact caller state even if playback is interrupted. The
        # conversation's saved history/seen flags deliberately remain shared.
        window_state = {
            name: getattr(store, name)
            for name in ("_window", "_window_auto", "_window_next", "_after_scene_show_hide")
            if hasattr(store, name)
        }
        try:
            renpy.call_in_new_context("phone_random_play", entry_id)
        finally:
            for name, value in window_state.items():
                setattr(store, name, value)
        if enter_m_main_story_active():
            renpy.show_screen(
                "phone_thread_history_screen",
                contact_id=phone_contact_id_from_name(contact_id),
                return_to_home=return_to_home,
            )
        return None


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
                phone_msg("them", "her grab hitbox is actual jank"),
                phone_msg("me", "Sounds like a major skill issue to me."),
                phone_msg("them", "stfu ive gone deathless in this run so far"),
                phone_msg("them", "this is just the worst designed boss in the game"),
                phone_msg("them", "like y does she dodge more often when u hit her weaknesses"),
                phone_msg("me", "I think I know how you can cheese the fight, actually."),
                phone_msg("them", "how"),
                phone_msg("me", "Just listen to this one piece of advice, I swear it's important:"),
                phone_msg("me", "Git gud scrub."),
                phone_msg("them", "UR SUCH A SHITHEAD"),
                phone_msg("them", "I DIED AGAIN THANKS TO U"),
                phone_msg("me", "Damn you suck lmaoooooooooo"),
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
                phone_msg("me", "I haven't touched your stuffed rabbit, dingus."),
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
                phone_msg("them", "tell him urself damn"),
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
                phone_call_line("me", "...And why do I hear cans?"),
                phone_call_line("them", "Because I'm by a lot of cans. Of soup. Duh."),
                phone_call_line("me", "Why are you shopping for clothes in the soup aisle?"),
                phone_call_line("them", "I'm noooooot-ah! I thought the sign said apparel!"),
                phone_call_line("me", "The sign led you to soup?"),
                phone_call_line("them", "That's why I followed the arrow!"),
                phone_call_line("me", "May wanna read it again."),
                phone_call_line("them", "..."),
                phone_call_line("them", "...Uh."),
                phone_call_line("me", "Didn't say apparel, did it?"),
                phone_call_line("them", "...It says appetizers."),
                phone_call_line("me", "Case closed. Come home."),
                phone_call_line("them", "I still need detergent!"),
                phone_call_line("me", "THEN STOP TRYING TO BUY SOUP ONESIES!"),
                phone_call_line("them", "I'M LOOKING FOR THE EXIT! GOD!"),
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
                phone_msg("them", "Combat sings. Story has teeth. Soundtrack absolutely SLAPS."),
                phone_msg("me", "That's positive."),
                phone_msg("them", "HOWEVER"),
                phone_msg("them", "the inventory sort resets every time you equip something"),
                phone_msg("them", "the map cursor snaps back to the shrine whenever i breathe"),
                phone_msg("them", "and it asks me to confirm closing the menu every time without a way to disable it"),
                phone_msg("me", "That last one sounds considerate."),
                phone_msg("them", "No. The UI can eat my whole fat ass."),
                phone_msg("me", "Score?"),
                phone_msg("them", "Nine out of ten"),
                phone_msg("me", "Despite the jank?"),
                phone_msg("them", "I didn't say the jank was bad"),
                phone_msg("me", "You...just said it could eat your ass though?"),
                phone_msg("them", "Not the same thing, don't make it weird"),
                phone_msg("me", "???????????????"),
                phone_msg("them", "Also why can't it just be easier to wall climb whilst mounted and doing backwards jumps on frame-perfect intervals"),
                phone_msg("them", "The devs must really hate the speedrunning community"),
                phone_msg("me", "You're already trying to discover speedrun tech? The hell kinda gamer are you?"),
                phone_msg("them", "ye"),
            ],
        },

        {
            "id": "rc2_matsuda_wrong_person",
            "contact": "Matsuda Akai",
            "kind": "text",
            "unlock": [("open", "matsuda"), ("date", "0525")],
            "body": [
                phone_msg("them", "if he calls the OP cringe again hold me back cause imma commit a hate crime"),
                phone_msg("me", "...Do I want to know who that was meant for?"),
                phone_msg("them", "What was meant for whom?"),
                phone_msg("me", "The message directly above this one."),
                phone_msg("them", "Uh"),
                phone_msg("them", "Kareda."),
                phone_msg("me", "Yeah, that tracks."),
                phone_msg("them", "Why were you in her contact slot?"),
                phone_msg("me", "I wasn't? You selected me."),
                phone_msg("them", "Your names occupy adjacent spiritual territory."),
                phone_msg("me", "They aren't alphabetically adjacent either, stop trying to sound like an astrology nut."),
                phone_msg("them", "Then your phone number was standing suspiciously close to hers."),
                phone_msg("me", "On YOUR phone."),
                phone_msg("them", "At last, we locate the crime scene."),
                phone_msg("me", "Okay, but how come I'm the one somehow at fault for your misinput?"),
                phone_msg("them", "bc you are"),
                phone_msg("me", "I'm going to strangle you when I find you."),
                phone_msg("them", "Naughty~~~"),
            ],
        },

        {
            "id": "rc2_matsuda_duck_hat",
            "contact": "Matsuda Akai",
            "kind": "facetime",
            "unlock": ("open", "matsuda_video"),
            "sprite": "phone_matsuda_duck_hat",
            "body": [
                phone_call_line("them", "Alrighty, can you see the whole thing?"),
                phone_call_line("me", "I can see a duck hat eating your head."),
                phone_call_line("them", "Behold! The apex of modern headwear!"),
                phone_call_line("me", "...Is this what you wanted to call me about, with you texting me \"URGENT\" in all caps?"),
                phone_call_line("them", "I called because text cannot carry its majesty, nor does a photo that's compressed to hell."),
                phone_call_line("me", "So I'm guessing you bought that thing, but... why?"),
                phone_call_line("them", "Kareda said I lacked the courage to wear it in public."),
                phone_call_line("me", "So you bought it out of spite."),
                phone_call_line("them", "No. I bought it because doubt demands rebuttal. And because I'm indeed not some pansy."),
                phone_call_line("me", "Are you actually wearing it outside?"),
                phone_call_line("them", "That depends."),
                phone_call_line("me", "On what?"),
                phone_call_line("them", "Whether it looks good."),
                phone_call_line("me", "I mean... you somehow pull it off. It does look surprisingly adorable."),
                phone_call_line("them", "An even more correct answer than I bargained for!"),
                phone_call_line("me", "...Okay, now are you punching your phone trying to hit a button?"),
                phone_call_line("them", "Yes, now why is this not--"),
            ],
        },

        # --- Himeko ----------------------------------------------------------

        {
            "id": "rc2_mom_mid",
            "contact": "Mom",
            "kind": "text",
            "unlock": ("open", "mom"),
            "body": [
                phone_msg("me", "Why did you ask what \"mid\" meant after dinner yesterday?"),
                phone_msg("them", "Asahina used the word. I am establishing what she meant before I respond."),
                phone_msg("me", "It means average. Mediocre. Subpar. It's honestly really stupid slang."),
                phone_msg("them", "I see."),
                phone_msg("them", "She had seconds after calling the carrots \"mid\" though."),
                phone_msg("me", "Then her testimony conflicts with the physical evidence."),
                phone_msg("them", "Now you get it."),
                phone_msg("me", "Are you going to confront her?"),
                phone_msg("them", "No. I am making the same dinner Thursday."),
                phone_msg("me", "Cold."),
                phone_msg("them", "Apparently only mid."),
                phone_msg("me", "So lukewarm?"),
                phone_msg("them", "Microwaved after getting cold."),
                phone_msg("me", "I guess this is what it means for revenge to be served mid."),
                phone_msg("them", "Righty-o, home skillet."),
                phone_msg("me", "...I think you're just as bad as her."),
            ],
        },

        {
            "id": "rc2_mom_autocorrect",
            "contact": "Mom",
            "kind": "text",
            "unlock": [("open", "mom"), ("date", "0526")],
            "body": [
                phone_msg("me", "Did you mean to ask me to 'defrost the chickpea'?"),
                phone_msg("them", "Chicken. I typed chicken."),
                phone_msg("me", "Your keyboard has been at work too long, methinks."),
                phone_msg("them", "Please take the client breasts out of the freezer."),
                phone_msg("them", "CHICKEN BREASTS."),
                phone_msg("me", "I was going to give context a chance."),
                phone_msg("them", "Put them in the sink. Do not cook the children."),
                phone_msg("them", "CHILDREN*"),
                phone_msg("them", "Let's see if speech does the trick. Please though the chick Ken."),
                phone_msg("them", "C H A C K E N"),
                phone_msg("them", "I give upstairs."),
                phone_msg("me", "At this rate, you may just need a new phone."),
                phone_msg("them", "Please disregard every text from the past two minutes."),
                phone_msg("them", "You know what to do. Heading into a meeting now."),
                phone_msg("me", "No worries. I'll go defrost Asa and her stuffed bunny."),
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
                phone_call_line("me", "The first sounds like some sort of research paper or outline for eye-grating documents."),
                phone_call_line("them", "Okay, okay... That is almost exactly what I told my partner."),
                phone_call_line("me", "So I'm just a rubber duck here?"),
                phone_call_line("them", "I'd say more like independent corroboration."),
                phone_call_line("me", "Do I get credit for helping in this creative process?"),
                phone_call_line("them", "You get dinner and the satisfaction of improving public outreach."),
                phone_call_line("me", "Dinner's already something we do normally."),
                phone_call_line("them", "Then I raised you to negotiate. I'm very proud."),
                phone_call_line("me", "How does that even...?"),
                phone_call_line("me", "{i}*sigh*{/i} ...Just go with the second one."),
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
                phone_msg("them", "I knew you'd understand!"),
                phone_msg("me", "I understand that you have given me literally nothing to work with."),
                phone_msg("them", "Perfect. Fresh eyes~"),
            ],
        },

        {
            "id": "rc2_monika_horror_verdict",
            "contact": "Monika",
            "kind": "text",
            "unlock": [("open", "monika"), ("date", "0524")],
            "body": [
                phone_msg("me", "Why did the horror committee send me a verdict in the form of a handwritten note in my locker?"),
                phone_msg("them", "Because you were tried in absentia."),
                phone_msg("me", "For what?"),
                phone_msg("them", "You said practical effects don't automatically make a movie good."),
                phone_msg("me", "They don't though."),
                phone_msg("them", "Count one: aggravated bad taste."),
                phone_msg("them", "Count two: reckless indifference to texture."),
                phone_msg("them", "Count three: disrespecting a model train that took six weeks to build because it \"looked like shit.\""),
                phone_msg("me", "Hey, I'm just saying I could probably cobble together a 3D model of that same train in less time."),
                phone_msg("me", "Not like it'd make the movie any better."),
                phone_msg("them", "The court recognizes no distinction."),
                phone_msg("me", "So what's my sentence?"),
                phone_msg("them", "You have to watch the director's cut with me."),
                phone_msg("me", "Absolutely not, that version has an even worse rating."),
                phone_msg("me", "You can't just take something that's objectively bad and call it slept on."),
                phone_msg("them", "Overruled~"),
                phone_msg("them", "I'll see you at 5."),
                phone_msg("me", "You and that movie can kiss my ass."),
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
                phone_call_line("them", "Worse. A title page, three colored margins, and 'Monika will fill in the details.'"),
                phone_call_line("them", "He also approved the basketball club and drama club for the gym at the same time! Can you believe this?!"),
                phone_call_line("me", "Joint production?"),
                phone_call_line("them", "Don't give him ideas! He'll call it interdisciplinary and leave me to schedule it."),
                phone_call_line("me", "Have you told him any of this?"),
                phone_call_line("them", "I used calm words, and aaaaaaaaaaaaaaaaall he said in his stupid-ass nasally voice was that we'd circle back."),
                phone_call_line("them", "If he says circle back one more time, hoooooooheheh... I'm making him physically circle the building until he finally sheds some of that flab. Friggin' fatass."),
                phone_call_line("me", "Normally I'd call that cruel and unusual punishment, but..."),
                phone_call_line("them", "I am off the clock and he is bad at his job, I can complain however-much-the-hell I want."),
                phone_call_line("them", "...Are you reaching for the end-call button? How dare you!"),
                phone_call_line("me", "Nah, gnat on my screen."),
                phone_call_line("them", "Your thumb is LITERALLY in frame!"),
                phone_call_line("me", "I was adjusting morale."),
                phone_call_line("them", "Great. Morale can stay for the budget story."),
                phone_call_line("me", "Oh, there's a budget story?~"),
                phone_call_line("them", "There are three, ALL from today."),
                phone_call_line("me", "Ah, I see. You'll have to tell me about them when I'm not trying to end the call."),
                phone_call_line("them", "YOU ARE {i}NOT{/i} HANGING UP ON ME, DON'T YOU FU--"),
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
    if not enter_m_main_story_active():
        return

    $ _prc_entry = phone_random_entry(entry_id)

    if _prc_entry is None or entry_id in phone_random_seen or not phone_random_unlocked(_prc_entry):
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
