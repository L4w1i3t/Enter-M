label a0515:
    stop music # here for scene viewer later on
    # --- Day 1: 2025-05-15 ---
    $ calendar.set_date(2025, 5, 15)
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with dissolve_scene_full
    window auto
    # Short sequence before the player can finally enter MC's name. Monika finds
    # his dropped ID during her assigned council sweep and returns it to him.
    show monika forward uniform happ om oe nobl rdown ldown at t11
    m forward uniform happ om oe nobl rdown ldown "...Of course, see you then!"
    window hide
    pause 2.0
    window auto
    m forward uniform anno om oe nobl rdown ldown "...Ah. Inappropriate flyer here..."
    m forward uniform anno om oe awkw rdown ldown "Student council's end-of-day sweep sounded shorter when it was still on paper..."
    m forward uniform neut om oe nobl rdown ldown "Alright, flyer in the trash bag... One more pass by the stairs, then club."
    window hide
    pause 1.5
    window auto
    m forward uniform anno om ce nobl rdown ldown "Aaaaand...of course he left this thing here."
    m forward uniform worr om oe nobl rhip ldown "Come on, you're better than this..."
    window hide
    pause 1.0
    window auto
    # The only fourth-wall break in the chapter. Staged deliberately SMALL: she
    # is still mid-cleanup and still holding the card, so the line stays
    # deniable as something said to it. The meta thread is dormant until later
    # acts, and this should not promise more than those acts pay back.
    m forward uniform angr om oe nobl rdown ldown "...What do {i}you{/i} want?"
    window hide(None)
    show monika at thide
    hide monika
    play sound tick
    scene black
    pause 5.0
    scene bg club_day
    $ atmos("afternoon", particles="motes")
    with dissolve_scene_soft
    play music dailyfantasy
    window auto
    # Perspective shift immediately onto MC
    # SFX SUGGESTION: A single dry pen tap against the desktop, prominent in the quiet room.
    "My pen rolls between my fingers and taps once against the desk. It is the loudest thing in the club room."
    "When the room gets this quiet, small details start volunteering themselves. The back locker door sits at a perfect right angle, outlined by a thread of afternoon light."
    "I roll my shoulders to loosen my neck. That's when a fingertip taps the right one while they're still up."
    "{i}Same shoulder, same timing,{/i} I think to myself."
    $ player = "???"
    mc "...Monika."
    "She pivots seamlessly into my line of sight."
    show monika forward uniform happ cm oe nobl rdown ldown at l11
    m forward uniform happ om oe nobl rdown ldown "Hey! You knew it was me for once."
    mc "You know you're getting predictable, yeah?"
    mc "Also, holy crap, what perfume did you put on today?"
    m forward uniform nerv om oe awkw rdown ldown "I...may or may not have spilled my bottle getting ready this morning."
    m forward uniform happ om oe nobl rhip ldown "But hey, I'll take that as a compliment!"
    "I lean back, giving myself more room to breathe."
    mc "So, what did I do this time?"
    "Monika flicks up her hand."
    m forward uniform curi om oe nobl rhip ldown "Well, for starters..."
    "A quick turn of her wrist reveals an ID card."
    m forward uniform happ om oe nobl rhip ldown "Looks like this has your name on it. Found it face-down near the stairs, staging a tragedy for a piece of plastic."
    "The plastic sleeve hanging from my lanyard has split at one corner. That explains the escape and why I've spent all day wearing a ribbon."
    mc "Oh! I was wondering where that went. Thanks."
    "She flips the card toward me as if it were a coin, and I catch it between two fingers mostly by accident."
    show monika forward uniform happ cm ce nobl rdown ldown
    m forward uniform happ cm ce nobl rdown ldown "Anytime. Try not to make a hobby of it."
    "{i}Not trusting that sleeve twice.{/i} I check the information, then zip the card into the front pocket of my bag."
    $ hide_calendar()
    $ atmos_clear()
    scene black with dissolve_scene_full
    pause 2.0
    scene bg ether with dissolve_scene_full
    call screen id_card_info_entry
    scene bg club_day
    $ atmos("afternoon", particles="motes")
    $ show_calendar()
    with dissolve_scene_full
    window auto
    show monika forward uniform happ cm oe nobl rdown lpoint at t11
    m forward uniform happ om oe nobl rdown lpoint "Be sure not to lose it again, 'kay?"
    mc "Yeah, yeah..."
    "She giggles at that and gives me a light nudge on the shoulder."
    show monika forward uniform happ cm oe nobl rdown ldown
    mc "So...what's on the agenda today?"
    m forward uniform nerv om oe awkw rdown ldown "Honestly, I didn't get around to planning anything special today..."
    m forward uniform wry om oe awkw rdown ldown "I had a few ideas this morning, then classes happened, and now those ideas are somewhere under a pile of other council members' paperwork."
    "Monika shrugs. There are bags under her eyes that weren't there last week."
    mc "Usual routine works for me. I brought something you can tear apart, actually."
    m forward uniform pout om oe nobl rdown ldown "Oh come on, it sounds harsh when you say I'll tear it apart..."
    m forward uniform happ om oe nobl rdown lpoint "How about the term 'tough love' or simply 'constructive feedback?'"
    "I pull the pages from my bag. Changing my mind can miss its window."
    mc "Just don't make the margins bleed too much."
    "She takes the pages and reads the way she always does: lips parted, pen capped but held ready, like the cap is the only thing keeping her professional."
    "I already know which lines she'll stop on. To be fair, I wrote them so that she would, then pretended I hadn't."
    "{i}The desk is just a desk. [[It is not standing in for anything. I checked twice.]{/i}"
    "{i}I keep the good pens in the bag I never open. [[No reason. Don't look at me.]{/i}"
    play sound audio.modwriting
    "She uncaps the pen after all and writes something small in the margin. The page comes back face-down."
    mc "...That bad?"
    m forward uniform curi om oe nobl rhip ldown "Opposite problem, actually."
    "Next to the brackets, in her neat slanted hand:"
    "{i}\"The brackets are part of the poem, you just haven't admitted it yet!\"{/i}"
    mc "I'll...take it under advisement."
    m forward uniform happ om ce nobl rhip ldown "Knowing you, you'll take it under a pile and forget it."
    mc "...Or that."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The rest of the session goes to trading drafts and reading two aloud. We leave one argument unresolved: whether a sunset can be 'smug.'"
    nier "Unlike the rest of my day, I show up for this part on purpose."
    call nier_clear from _call_nier_clear_0515_1
    nier "By late afternoon the other members had shuffled out, leaving just Monika and me to lock up."
    call nier_clear from _call_nier_clear_0515_2
    pause 2.0
    scene bg club_day
    $ atmos("evening")
    show monika forward uniform dist cm oe nobl rdown ldown at t11
    $ show_calendar()
    with wipeleft_scene
    mc "Alrighty, so, same time tomorrow?"
    m forward uniform laug om ce nobl rdown ldown "You betcha!"
    m forward uniform nerv om oe awkw rhip ldown "Oh, and I was actually thinking, [player]..."
    m "I got two presale tickets to that neat-looking horror flick coming out on Sunday, so..."
    menu:
        "\"You bought two tickets before you had a second person.\"":
            $ s1_pick("monika_invite", "joke")
            mc "You bought two tickets before you had a second person."
            m forward uniform pout om oe awkw rdown ldown "I had a {i}candidate{/i}."
            mc "I'd love to see the rest of the shortlist."
            m forward uniform nerv om ce blaw rdown ldown "It was a...very...exclusive list."
            mc "Uh-huh..."
            mc "Well, I got nothing going on, so...sure."
        "\"Sunday works.\"":
            $ s1_pick("monika_invite", "plain")
            mc "Sunday works."
            m forward uniform vsur om oe nobl rdown ldown "...That easy?"
            mc "That easy."
            m forward uniform laug om ce nobl rdown ldown "Noted. I had an entire argument prepared."
        "(Say the other thing.)":
            $ s1_pick("monika_invite", "swallowed")
            mc "Sunday. Yeah, I--"
            mc "...You could've just texted me."
            "{i}Not what I was going to say.{/i}"
            m forward uniform pout om oe nobl rdown ldown "Where's the fun in that?"
            mc "In any case, I'm down, medium aside."
    show monika forward uniform happ om ce blus rdown ldown at h11
    m forward uniform happ om ce blus rdown ldown "It's a date, then!"
    play sound moddooropen
    # Monika is still the focused speaker here, so Autofocus has not lifted her
    # hf11 back to t11 yet -- and an attribute show with no at_list gets hf11
    # re-injected by sticky_positions, which replays the hop a second time.
    # Naming the rest slot settles her instead.
    show monika forward uniform happ cm ce nobl rdown ldown at t11
    "Monika waltzes to the door."
    m forward uniform happ cm ce nobl rdown ldown "I'm outta here now, so see you tomorrow!"
    "I hold my hand up in a wave."
    mc "Later, Ms. President."
    show monika at thide
    hide monika
    play sound moddoorclose
    "Once she is out of both sight and earshot, I let out a long sigh and sling my bag over my shoulder."
    $ phone_mark_contact_met("monika")
    $ mark_character_met("monika")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Bus, then the short walk home. The usual."
    nier "It produces one anomaly: a strange bottle cap beside a power line."
    nier "A quick internet search says it came from an imported Scottish soda." # planting a seed for matsuda because she drinks imported drinks (i.e. this universe's version of Irn Bru). also characterization for MC having weird bouts of curiosity
    call nier_clear from _call_nier_clear_0515_3
    pause 2.0
    scene bg house
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with wipeleft_scene
    "By the time I reach the front gate, smoked meat and melted cheese hit first. Then salt and fryer grease drift from a paper bag gone translucent in spots."
    "My little sister Asahina is on the swing in the yard, one foot planted in the dirt so she can keep herself rocking while she eats."
    show asahina uniform neut at t11
    "She catches me in her peripheral vision and tips her chin, mid-bite."
    show asahina uniform unamused
    mc "Bill's Flamey Double again?"
    "She swallows her bite."
    ah "...Yeah, what about it?"
    mc "I'm starting to think they put your name on a stool in there."
    ah "And your point is?"
    mc "Nothing. I'm just saying the cashier probably starts your order the second he sees you cross the street."
    show asahina uniform annoyed
    ah annoyed "Yeah, well, I've got money and practice burns it off. That cashier doesn't even know my name, actually."
    mc "Sure he doesn't... I'd say he's just too polite to use it."
    "A fry bounces off my cheek before I get to enjoy that one."
    show asahina uniform frustrated
    ah "Okay, listen here, you little--!"
    "{i}It's always too easy with her, I swear.{/i}"
    "I hold the blank smile too long. Something in her face goes still."
    mc "...Anyway. I'm heading in."
    mc "Leave some food for other paying customers, please."
    show asahina uniform unamused
    ah "Screw you too."
    "Asahina raises her empty hand as I approach the front mat. Her middle finger follows."
    $ phone_mark_contact_met("asahina")
    $ mark_character_met("asahina")
    $ hide_calendar()
    scene black with wipeleft_scene
    play sound moddooropen
    pause 2.0
    scene bg home_entry_day
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    play sound moddoorclose
    mc "Hey, Mom."
    show mom happy at t11
    mom "Ah, hey there, [player]!"
    show mom neut
    mom neut "Just in time, actually. I wanted to go over something with you when you're available."
    mc "Oh, uh, alright."
    "{i}I literally just walked in.{/i}"
    mc "I'm free. Just let me get situated first..."
    show mom happy
    mom "Take your time."
    mom "Oh, wait, question: katsudon sound good for dinner? I'm trying to find an excuse to use these pork loins before they expire."
    mc "Yeah, fine by me. Anyway, off I go."
    "I tip my head toward the stairs and shift my bag on my shoulder."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    # SFX SUGGESTION: A soft, weighted bag thump against the floor.
    "I drop my bag by the side of my desk and stretch my arms overhead."
    "I pace once around the room, then pull out my phone and check the time."
    "{i}Still early. I could get a head start on something.{/i}"
    "..."
    "I flop onto my bed and stare at the ceiling instead."
    "{i}...Guess that's not the worst thing in the world.{/i}"
    $ phone_mark_contact_met("mom")
    $ mark_character_met("mom")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Before long, I find myself back downstairs."
    call nier_clear from _call_nier_clear_0515_4
    pause 2.0
    scene bg kitchen_evening
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    "Mom's already at the counter with vegetables lined up beside a bowl of spice mix. The pork loins thaw in cold water in the sink."
    show mom happy at t11
    mc "Need a hand?"
    mom "You know it, kiddo."
    "She gestures at the cutting board beside her."
    show mom teasing
    mom "You're better than me at dicing onions, so have at it."
    "{i}Gonna make me cry, huh?{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Time passes over the rice cooker and cutting board. Soon we're breading the loins together."
    call nier_clear from _call_nier_clear_0515_5
    pause 2.0
    scene bg kitchen_evening
    show mom neut at t11
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    # SFX SUGGESTION: A steady frying-oil sizzle under the kitchen conversation.
    "Once the meat's in the pan, we both take a deep breath at almost the same time."
    mc "So...you wanted to run something by me?"
    "She wipes her hands and slides a folded printout across the counter, still warm from the printer. A campus photo on the front: all glass and a courtyard with grass too green to be real."
    mom "I was digging around earlier and found a school I think would actually fit you."
    "There's a line near the bottom already buried in yellow highlighter: the program name. It's the exact one I'd have circled myself, if I felt like admitting I'd already looked it up."
    "My hands stop moving on the pan."
    mc "...Already, huh?"
    show mom teasing
    mom "Oh, don't be like that. If anything, we're late to the party."
    show mom neut
    mom "You graduate in less than a year. I don't want to be the parent who nags, but it's time to start thinking about what comes after."
    "I make myself nod."
    mc "...When you put it that way."
    mc "I know a few classmates who already have the whole thing mapped. Major, city, the exact dorm they want, et cetera."
    "{i}Monika's probably had this figured out since the day she started primary or something.{/i}"
    mc "Anyway, go on. I'm listening."
    show mom happy
    mom "It checks a lot of boxes. Well-regarded faculty, tranquil setting..."
    mom happy "Good reputation, too. Top twenty, matter of fact."
    mom teasing "You get to 'see the world,' and I can still threaten you in person after one train ride."
    show mom curious
    mom curious "Could we perhaps do more digging together this coming week? Only if you want, though."
    mom "I won't push."
    mc "I, uh..."
    mc "...Yeah, I mean, sure. I'm down."
    show mom smug
    mom "You don't have to commit to anything right {i}now{/i}, buuuuuut you do have to start thinking about it."
    "I shuffle the pan a little bit and hold up an \"okay\" sign with my other hand."
    mc "Crystal clear."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "About twenty minutes pass as we finish preparing the katsudon and readying our plates."
    call nier_clear from _call_nier_clear_0515_6
    pause 2.0
    scene bg dining_table_night
    $ show_calendar()
    show mom curious at t22
    show asahina neut at t21
    $ atmos("home_night")
    with wipeleft_scene
    "My sister takes her seat, not even giving her own plate the time of day."
    ah "...Smells good."
    mom curious "That's all you're having...? A spoonful of rice and the smallest wedge?"
    show asahina unamused
    ah "Yeah."
    ah "I'm not that hungry today."
    menu:
        "\"I put extra mirin in this time.\"":
            $ s1_pick("asahina_plate", "joke")
            mc "You know, I added some extra mirin this time..."
            ah "Cool."
            show asahina teasing
            ah "I can taste it from here...with my nose."
        "(Say nothing.)":
            $ s1_pick("asahina_plate", "quiet")
            "I take a sip of water to stop myself from tattling."
        "\"That's not a dinner.\"":
            $ s1_pick("asahina_plate", "named")
            mc "That's more of a garnish than anything."
            show asahina annoyed
            ah "It's a portion."
            ah "People have portions. Is it a crime to have {i}portions{/i}?"
            "She says it like it was in an easy-access chamber."
    show mom neut
    mom worried "Asahina, you should really eat something proper. Those empty chip bags in your room aren't much of a dinner."
    mom "And fast food isn't exactly a balanced diet, either."
    mc "Wait, so that's where my snacks have been going?!"
    mc "...You owe me."
    show asahina neut
    "Asahina picks up her chopsticks and nudges the pork without lifting it."
    ah "Yeah, I guess."
    "She takes a small bite, careful, like she's expecting the food to argue back."
    show mom worried
    "Mom watches until Asahina looks back. Then she lowers her eyes to her own plate, chopsticks motionless."
    "I catch myself cataloguing it the way I catalogue everything: literally not my problem."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Dinner somehow finds a second wind. By the third quarter, the plates are clear and everyone has drifted to a separate corner of the house."
    nier "On my end, I crank out whatever homework I have in five minutes flat. That's what it feels like, anyway."
    nier "With nothing else to do, I fall back on the usual: an obligatory poem for Monika's club, then a JRPG with about fifteen self-imposed restrictions."
    call nier_clear from _call_nier_clear_0515_7
    stop music fadeout 2.0
    pause 2.0
    scene bg home_entry_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music fantasypassion
    "Night envelops the world with its stygian embrace." # poetic on purpose, as it's facetiously dramatic
    # SFX SUGGESTION: Quiet page turns layered with faint handheld button taps.
    "Tonight that amounts to Mom flipping the pages of her book in the living room, and Asahina on the floor tapping away at her handheld."
    "As for me, I decide to wrap things up early. My previous night of doomscrolling random wiki articles is to thank."
    "Before clocking out, I drink some water, take my medication, and--"
    show asahina curious at l11
    ah "You know if we have any glue anywhere? The white, sticky kind outta the bottle, not the sticks."
    "{i}Dude, phrasing...{/i}"
    mc "...Uhhh...I don't know, actually."
    mc "You check that one drawer yet?"
    show asahina frustrated
    ah "You think I haven't?! Uuuuughhhhh, what do I do...?"
    mc "What do you need it for, anyway?"
    ah "Stupid me completely forgot to make this poster that I've been putting off for a week now!"
    ah "Volleyball wants ME of all people doing the freaking recruiting stuff, and it was due 'as soon as humanly possible' like a week ago!"
    show asahina shocked at h11
    mom "Language, Asahina!"
    show asahina annoyed at t11
    ah "I didn't even swear that time!"
    show asahina neut
    ah "...So, anyway. Yeah."
    mc "...And what exactly am I supposed to do about it? You've always been the artsy one."
    # mc "Me? I can't draw a straight line with a ruler." # cut because it's tangential
    show asahina nervous
    ah nervous "Urgh, I dunno..."
    "Saturday's game run gives me an idea."
    mc "Well, I was going to pick up this new game on launch Saturday..."
    mc "If you want me to grab some glue while I'm out, I can do that."
    "Asahina sighs and takes a subtle bow."
    show asahina happy
    ah "Yes, that'd be amazing!"
    show asahina embarrassed
    ah "And, uh, in return, I can...uhhh...restock your chips! Yeah!"
    mc "Yeah, sure, why not. It's a deal."
    "I finish the rest of my water without noticing."
    mc "Now, I hate to be that guy, but I'm dozing off as we speak."
    show asahina teasing
    ah "Then go to bed, doofus!"
    mc "Says the staller."
    show asahina at thide
    hide asahina
    "{i}Way for her to trip me into doing her fetch quests...{/i}"
    $ hide_calendar()
    scene black with dissolve_scene_full
    nier "I set a reminder for the extra stop tomorrow, then pass through the kitchen for another glass of water."
    nier "Asahina's plate is already rinsed and face-down in the rack. A paper towel lies flat across the trash in the bin under the sink."
    nier "I put my glass beside her plate and go up."
    call nier_clear from _call_nier_clear_0515_8
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0515_1
    jump a0516
