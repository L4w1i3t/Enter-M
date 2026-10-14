label a0515:
    stop music # here for scene viewer later on
    # --- Day 1: 2025-05-15 ---
    $ calendar.set_date(2025, 5, 15)
    pause 2.0
    scene bg corridor
    $ atmos("afternoon", particles="motes")
    with dissolve_scene_full
    # Short sequence before the player can finally enter MC's name. Monika finds
    # his dropped ID during her assigned council sweep and returns it to him.
    show monika forward uniform happ om oe nobl rdown ldown at t11
    m forward uniform happ om oe nobl rdown ldown "...Of course, see you then!"
    pause 2.0
    m forward uniform anno om oe nobl rdown ldown "Oh, come on. They put it back up?"
    m forward uniform anno om oe awkw rdown ldown "I just took this down at lunch."
    m forward uniform neut om oe nobl rdown ldown "Okay. Stairs, then I'm done."
    pause 1.5
    m forward uniform anno om ce nobl rdown ldown "Aaaaand... of course he left this thing here."
    m forward uniform worr om oe nobl rhip ldown "Come on, you're better than this..."
    pause 1.0
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
    pause 3.0
    scene bg club_day
    $ atmos("afternoon", particles="motes")
    with dissolve_scene_soft
    play music day_a
    # Perspective shift immediately onto MC
    # SFX SUGGESTION: A single dry pen tap against the desktop, prominent in the quiet room.
    "I roll my pen between my fingers until it taps the desk, loud enough in the empty club room that I stop doing it."
    "Club starts in nine minutes, though I have been here for twelve and counting with no other person in sight."
    "Afternoon light catches the edge of the back locker door, which somebody has left open at a surprisingly perfect right angle."
    "My headphones drown out any possible noise that could be in my vicinity."
    "When I roll my shoulders to loosen my neck, a fingertip catches the right one with a {i}tap-tap-tap{/i}. Same pace, same pause."
    "{i}She could at least try the other side,{/i} I think to myself."
    $ player = "???"
    mc "...Monika."
    "She steps into my line of sight and rolls my headphones off my dome."
    show monika forward uniform happ cm oe nobl rdown ldown at l11
    m forward uniform happ om oe nobl rdown ldown "Hey! You knew it was me for once."
    mc "You know you're getting predictable, yeah?"
    mc "Also, holy crap. Is that your perfume?"
    m forward uniform nerv om oe awkw rdown ldown "Still? I spilled some on my sleeve this morning..."
    m forward uniform happ om oe nobl rhip ldown "I was hoping it had worn off. Apparently I just got used to it, aha..."
    "I lean back, giving myself more room to breathe."
    mc "So, what did I do this time?"
    "Monika flicks up her hand."
    m forward uniform curi om oe nobl rhip ldown "Well, for starters..."
    "A quick turn of her wrist reveals an ID card."
    m forward uniform happ om oe nobl rhip ldown "Looks like this has your name on it. Face-down by the stairs, very dramatic, no note or anything."
    "The plastic sleeve on my lanyard has split at one corner. I have been effectively wearing a ribbon all day."
    mc "Oh! Uh, I was wondering where that went. Thanks."
    "She flips the card toward me, and I catch it almost on instinct against my chest before it can escape again."
    show monika forward uniform happ cm ce nobl rdown ldown
    m forward uniform happ cm ce nobl rdown ldown "Anytime. Try not to make a hobby of it."
    "{i}Not trusting that sleeve twice.{/i} I check the information, then zip the card into the front pocket of my bag without reservation."
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
    show monika forward uniform happ cm oe nobl rdown lpoint at t11
    m forward uniform happ om oe nobl rdown lpoint "Be sure not to lose it again, 'kay?"
    mc "Yeah, yeah..."
    "She giggles at that and gives me a light nudge on the shoulder."
    show monika forward uniform happ cm oe nobl rdown ldown
    mc "So... what's on the agenda today?"
    m forward uniform nerv om oe awkw rdown ldown "Honestly, I didn't get around to planning anything special today..."
    m forward uniform wry om oe awkw rdown ldown "I had a few ideas this morning, then classes happened, and now those ideas are somewhere under a pile of other council members' paperwork."
    "Monika shrugs. There are bags under her eyes that weren't there last week."
    mc "Usual routine works for me. I finished that draft, if you want first crack at it."
    m forward uniform pout om oe nobl rdown ldown "You make me sound vicious..."
    m forward uniform happ om ce nobl rdown lpoint "But yes, I want it. Hand it over, right now... please."
    "I pull the pages from my bag, smoothing the corner that's been folded under a textbook since first period."
    mc "Just don't make the margins bleed too much."
    "She reads with her lips slightly parted, turning the capped pen between her fingers whenever something makes her pause."
    "She stops at the brackets. I could have taken them out last night, but then I'd have had to finish the lines around them."
    "{i}The desk is just a desk. [[It is not standing in for anything. I checked twice.]{/i}"
    "{i}I keep the good pens in the bag I never open. [[No reason. Don't look at me.]{/i}"
    play sound audio.modwriting
    "She uncaps the pen after all and writes something small in the thinly-veiled margin. The page comes back face-down."
    mc "...Oof. That bad?"
    m forward uniform curi om oe nobl rhip ldown "Opposite problem, actually."
    "Next to the brackets, in her neat slanted hand:"
    "{i}\"The brackets are part of the poem, you just haven't admitted it yet!\"{/i}"
    mc "I'll... take it under advisement."
    m forward uniform happ om ce nobl rhip ldown "Knowing you, you'll take it under a pile and forget it."
    mc "Hey, the pile's part of the process. Don't knock my style if it works."
    m forward uniform curi om ce nobl rhip lpoint "Does it, though...?"
    "She squares the page to the desk with two fingers."
    m forward uniform happ om oe nobl rhip ldown "Okay. Read me the second stanza out loud. I want to hear where you breathe."
    mc "Here?"
    m forward uniform happ cm oe nobl rhip ldown "Right here. I'm listening."
    "Two second-years have slipped in and started disagreeing about a line break at the back desks. I lower my page so they can't read over my shoulder."
    "I get through most of the stanza without trouble, but my voice drops on the word I spent longest choosing."
    show monika forward uniform curi cm oe nobl rdown ldown
    m forward uniform curi om oe nobl rdown ldown "Boom, there. You went quiet on 'smug.'"
    mc "I was trying not to make it sound ridiculous."
    m forward uniform happ om oe nobl rdown lpoint "That might be the word's fault! Read it without apologizing for it."
    mc "...'A sunset can be smug.'"
    m forward uniform wry cm oe nobl rhip ldown "A sunset can be plenty of things. Smug needs an audience."
    mc "Uh, yeah, it has one. They're sitting right here, actually."
    "Monika opens her mouth to answer, then closes it and writes something down instead."
    mc "What are you writing?"
    m forward uniform laug om ce nobl rdown ldown "Your defense of smug sunsets. I want to remember it when you bring me the revision."
    "She slides the notebook out of reach before I can look at it."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "We trade pages twice more as the other members arrive. Someone borrows my pen and returns it without the cap."
    nier "One of the second-years reads something about a train station, so quietly I miss the last line. Monika asks her to read it again."
    nier "By the time somebody's phone alarm goes off, I've found the cap under my chair. Three people all start packing at once."
    nier "Monika says all four of their names on the way out--something she does every single time, and it grates on me."
    nier "The light moves off the desks and onto the back wall."
    nier "I put the draft away with 'smug' still circled and a note to find a better defense for it tomorrow."
    nier "Unlike the rest of my day, I show up for this part on purpose."
    call nier_clear from _call_nier_clear_0515_1
    nier "The last of the others leave, and Monika brings the sign-out sheet over while I put the chairs up."
    call nier_clear from _call_nier_clear_0515_2
    pause 2.0
    scene bg club_day
    $ atmos("evening")
    show monika forward uniform anno cm oe nobl rdown ldown at t11
    $ show_calendar()
    with wipeleft_scene
    "Monika holds the sheet at arm's length like the handwriting has insulted her personally."
    m forward uniform anno om oe nobl rhip ldown "Geez Louise, look at this... Two people signed in as me."
    mc "Bold."
    m forward uniform wry cm oe nobl rhip ldown "One of them dotted the i with a heart, which is either an insult or a compliment, and I have decided not to find out which."
    "I lift the last two chairs onto their desks while she sorts out who actually came."
    m forward uniform happ om oe nobl rdown ldown "You don't have to do that, I'm still right here."
    mc "I know. Your point?"
    "She goes back to the sheet while I turn the wobbly chair toward the wall, where it will stay put."
    show monika forward uniform dist cm oe nobl rdown ldown
    "The room is done, but Monika stays beside the desk with her bag at her feet. I check the window latches while she finishes whatever she's thinking about."
    show monika forward uniform happ cm oe nobl rdown ldown
    mc "Same time tomorrow?"
    m forward uniform laug om ce nobl rdown ldown "Yep! See you here!"
    show monika forward uniform nerv om oe awkw rhip ldown at hf11
    m "Oh--wait, I was actually thinking, [player]..."
    m "I got two presale vouchers for that horror movie opening Saturday. Want to see it with me Sunday?"
    menu:
        "\"You bought two tickets before you had a second person.\"":
            $ s1_pick("monika_invite", "joke")
            mc "You bought two tickets before you had a second person."
            m forward uniform pout om oe awkw rdown ldown "I had a {i}candidate{/i}..."
            mc "I'd love to see the rest of the shortlist."
            m forward uniform nerv om ce blaw rdown ldown "It was a... very... exclusive... list."
            mc "Uh-huh..."
            mc "Okay, yeah, I'd like that. Sunday it is."
        "\"Sunday works.\"":
            $ s1_pick("monika_invite", "plain")
            mc "Sunday works."
            m forward uniform vsur om oe nobl rdown ldown "...That easy?"
            mc "That easy."
            m forward uniform laug om ce nobl rdown ldown "Noted. I had an entire argument prepared. Bullet points and everything."
        "(Say the other thing.)":
            $ s1_pick("monika_invite", "swallowed")
            mc "Sunday. Yeah, I--"
            mc "...You know you could've just texted me."
            "{i}Not what I was going to say.{/i}"
            m forward uniform pout om oe nobl rdown ldown "Okay, but where's the fun in that?"
            mc "Anyhoo, yes, that sounds nice. Got nothing else planned, so I say send it."
    show monika forward uniform happ om ce blus rdown ldown at h11
    m "It's a date, then!"
    play sound moddooropen
    # Monika is still the focused speaker here, so Autofocus has not lifted her
    # hf11 back to t11 yet -- and an attribute show with no at_list gets hf11
    # re-injected by sticky_positions, which replays the hop a second time.
    # Naming the rest slot settles her instead.
    show monika forward uniform happ cm ce nobl rdown ldown at t41
    "Monika waltzes to the door."
    m forward uniform happ cm ce nobl rdown ldown "I'm outta here now, so I'll see you tomorrow!"
    "I hold my hand up in a wave."
    mc "Later, Ms. President."
    show monika at thide
    hide monika
    play sound moddoorclose
    pause 1.0
    "Once the door closes, I let out a long sigh and sling my bag over my shoulder."
    $ phone_mark_contact_met("monika")
    $ mark_character_met("monika")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "After the bus ride, I take the short walk home. A bright orange bottle cap beside a utility pole catches my eye."
    nier "I pick it up and rub the dirt off the lettering. It's a brand that I don't initially recognize."
    nier "A quick internet search says it came from an imported orange soft drink." # planting a seed for matsuda because she drinks imported drinks (i.e. this universe's version of Irn Bru). also characterization for MC having weird bouts of curiosity
    nier "I pocket the cap and keep walking, still looking at pictures of peculiar orange drinks."
    call nier_clear from _call_nier_clear_0515_3
    pause 2.0
    scene bg house
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with wipeleft_scene
    "By the time I reach the front gate, I can smell smoked meat and melted cheese from a stained, brown paper bag."
    "My little sister Asahina is on the swing in the yard, one foot planted in the dirt so she can keep herself rocking while she eats."
    show asahina uniform neut at t11
    "She tips her chin at me, mid-bite."
    show asahina uniform unamused
    mc "Bill's Flamey Double again?"
    "She swallows her bite."
    ah "Yeah. Whadya want?"
    mc "Do they start making yours when you turn the corner, or is this a 'premium customer' thing?"
    ah "I wish. I waited twenty minutes for this."
    mc "You should complain. Get your regular's privileges and all that jazz."
    show asahina uniform smug
    ah "Okay, you joke, but I could've gotten home, made a sandwich, and walked back in that time."
    mc "And yet... here you are."
    ah "Because I wanted a burger instead. Shooooocking, I knooooow."
    show asahina uniform annoyed
    ah annoyed "Anyway, practice burns it off. And the cashier doesn't even know my name, so eff off."
    mc "Just your order, then."
    "A fry bounces off my cheek and drops onto my shoe."
    "She starts the swing moving again, working one foot against the dirt while I sit on the low wall by the gate. The chain has been squeaking since we moved here."
    "The fries stay on her side of the gap, so I brush the one she threw off my shoe."
    show asahina uniform neut
    ah "How was the poetry cult or whatever?"
    mc "Productive."
    ah "What, your girlfriend make you feel bad about a comma?"
    mc "...That is a wildly specific guess."
    show asahina uniform smug
    ah "Hey, I listen sometimes. You've ranted to me about stupider shit for longer."
    mc "Could've fooled me."
    show asahina uniform frustrated
    ah "Okay, listen here, you little--!"
    "I grin at her over the top of the bag."
    show asahina uniform unamused
    "She holds my stare until I look down at my shoe again."
    mc "...Anyway. I'm heading in."
    mc "Enjoy the rest of your order, but please leave some for the {i}other{/i} paying customers."
    ah "Screw you too."
    "Asahina raises her empty hand as I approach the front mat, her middle finger following my tracks."
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
    "I carry the grocery bag that's still by the door into the next room, supporting it underneath before its handles give out."
    show mom happy at t11
    mom "Ah, hey there, [player]!"
    show mom neut
    mom neut "I've got something to show you when you've put your things down."
    mc "Oh, uh, alright."
    "{i}I literally just walked in.{/i}"
    mc "Give me a few minutes?"
    show mom happy
    mom "Take your time."
    "She goes through the mail on the counter and puts two of the four envelopes straight into the recycling."
    mom unamused "Another one for the man who doesn't live here. {i}*sigh*{/i} Fourth year running."
    mc "Didn't you send the last one back?"
    show mom smug
    mom "With the same note. Apparently neither of us is learning."
    show mom happy
    mom "Oh, wait, question: katsudon sound good for dinner? I'm trying to find an excuse to use these pork loins before they expire."
    mc "Yeah. Save me something to chop."
    "I tip my head toward the stairs and shift my bag on my shoulder."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    # SFX SUGGESTION: A soft, weighted bag thump against the floor.
    "I pace once around the hardwood floor of my bedroom, then pull out my phone and check the time."
    "{i}Still early. I could get a head start on something...{/i}"
    "..."
    "I flop onto my bed and stare at the ceiling instead."
    "{i}...Guess that's not the worst thing in the world.{/i}"
    "The water stain above the desk still looks a little like a rabbit with one ear missing."
    "Downstairs, I can hear the faint clanging of Mom opening and closing cabinets until she finds whichever pan she wants."
    "Four minutes. I turn the phone over before I can spend the next fifty checking it."
    "A drawer slides shut downstairs, followed by Mom testing the tap. I stay where I am until the world requires more of me."
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
    mom "You're better than me at dicing onions, so... have at it."
    "{i}Gonna make me cry, huh?{/i}"
    "Mom shifts left to make room while I take the knife and pull the board closer."
    show mom neut
    mom "Root end stays on. It holds the rest of it together."
    mc "...I know."
    show mom teasing
    mom "Yes, I know you know. I just like saying it."
    "By the second onion my eyes are watering. Mom nudges the tissue box toward me without interrupting her measuring."
    "The rice cooker clicks over to its warming light."
    show mom neut
    mom "Asahina's still outside."
    mc "She's on the swing."
    mom thinking "She was on the swing when you came in. That was, what, half an hour ago?"
    "I keep dicing."
    "Mom looks through the window over the sink before returning to the spice mix."
    mom "Well. She'll come in when she's hungry."
    "{i}Fat chance there.{/i}"
    "She measures the flour twice."
    "Once the onions are done, I help her bread the pork while the oil heats. Breadcrumbs end up on both sides of the counter."
    # SFX SUGGESTION: A steady frying-oil sizzle under the kitchen conversation.
    "As the meat bubbles and fries in the pan, we both take a deep breath at almost the same time."
    mc "So... you wanted to run something by me?"
    "She wipes her hands and gets a folded printout from beside the mail. The campus photo on the front has a glass building and grass too green to be real."
    mom "I was digging around earlier and found a school I think would actually fit you."
    "There's a line near the bottom already buried in yellow highlighter: the program name. It's the exact one I'd have circled myself, if I felt like admitting I'd already looked it up."
    "I leave the tongs resting on the edge of the pan."
    mc "We're doing this now?"
    show mom teasing
    mom "Oh, don't be like that. If anything, we're late to the party."
    show mom neut
    mom "You graduate in {i}less than a year{/i}. I don't want to be the parent who nags, but it's time to start thinking about what comes after."
    "I make myself nod."
    mc "...When you put it that way."
    mc "I know classmates who have the whole thing mapped. Major, city, the exact dorm, the whole nine yards."
    "{i}Monika's probably had this figured out since the day she started primary or something.{/i}"
    mc "Anyway, go on. I'm listening."
    show mom neut
    mom "We don't need to pick your whole future over the stove. Let's start with where you'd be willing to live."
    mc "...Okay."
    mom "Would you rather be close enough to visit on a Friday, or would you be alright with a whole weekend of travel?"
    mc "Close enough to come back on a Friday. I'd rather not spend the whole visit on a train."
    show mom smug
    mom "There. That helps narrow it down."
    "She writes 'close to home' in the corner of the printout, then underlines it while I turn the pork."
    mc "You're taking notes again, I see."
    mom "Otherwise I'll find this next week and forget why I kept it."
    show mom happy
    mom "The course list looks promising. A fair amount of practical work, from what I could find."
    mom happy "We'll need to look past the brochure, of course. Even the parking lot looks wonderful in these photos."
    mom teasing "You get to 'see the world,' and I can still threaten you in person after one train ride."
    mom curious "Have a look sometime within the next week, and then we can sit down together. Would that help?"
    mom "You can tell me if this one's wrong for you."
    mc "No, I do want to look at it. Just... give me a sec."
    show mom smug
    mom "Take a few days if you need to. Just make sure you actually read it before deciding it's too much."
    "I shuffle the pan a little bit and hold up an \"okay\" sign with my other hand."
    mc "Crystal clear."
    "{i}Okay. Actual steps: read the page, look up the program, write down two questions.{/i}"
    "{i}I can manage three things, right?{/i}"
    "I turn the heat down under the pan and count them again on the way to the sink."
    "The printout ends up under the fruit bowl."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "About twenty minutes pass as we finish preparing the katsudon and readying our plates."
    nier "By dinner, the lighting and noise have reduced themselves to more preferable volumes, ignoring someone outside having a conversation loud enough to notify the whole street."
    call nier_clear from _call_nier_clear_0515_6
    pause 2.0
    scene bg dining_table_night
    $ show_calendar()
    show mom curious at t22
    show asahina neut at t21
    $ atmos("home_night")
    with wipeleft_scene
    "Asahina looks over the table as she takes her seat, then moves her glass away from the plate."
    ah "...Smells good."
    mom curious "That's {i}all{/i} you're having...? A tiddly-wink of rice and the smallest wedge?"
    show asahina unamused
    ah "Yeah."
    ah "I'm not that hungry today."
    menu:
        "\"I put extra mirin in this time.\"":
            $ s1_pick("asahina_plate", "joke")
            mc "You know, I added some extra mirin this time..."
            ah "Cool."
            show asahina teasing
            ah "I can taste it from here... with my nose."
        "(Say nothing.)":
            $ s1_pick("asahina_plate", "quiet")
            "I take a sip of water to stop myself from tattling."
        "\"That's not a dinner.\"":
            $ s1_pick("asahina_plate", "named")
            mc "That's more of a garnish than anything."
            show asahina annoyed
            ah "It's a portion."
            ah "People have portions. Is it a crime to have {i}portions{/i}?"
    mom worried "Asahina, you should really eat something proper. Those empty chip bags in your room aren't much of a dinner."
    mom "And fast food isn't exactly a balanced diet, either."
    mc "Wait, so that's where my snacks have been going?!"
    mc "...You owe me."
    show asahina neut
    "Asahina picks up her chopsticks and nudges the pork without lifting it."
    ah "Yeah, I guess."
    "She takes one small bite and chews it much longer than it needs."
    show mom worried
    mom "Asahina, if you're not--{i}*sigh*{/i}"
    "Mom stops and reaches for her drink, watching my sister until she looks back. Her chopsticks stay against the edge of her plate."
    "{i}She had a whole burger less than two hours ago. She can tell her that herself.{/i}"
    "Asahina catches me looking and slides her plate closer to herself. I reflexively take another bite of my own dinner."
    "Mom asks about some sort of poster project. Asahina has to finish chewing before she can complain about the size of the board they gave her."
    "I pass her the water jug when she reaches for it."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Dinner runs into a debate over whether particular supplies will fit in Asahina's locker. After we clear the table, I promptly head upstairs."
    nier "The remaining homework is mostly checking answers I finished in class. I get through it before my console finishes updating."
    nier "That leaves the poem. I pull out today's draft to see whether Monika was right about anything or if she's truly lost it."
    call nier_clear from _call_nier_clear_0515_7
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    "I use the pen already on my desk, leaving the good ones in their unopened box inside my bag."
    "After four lines, I go back to the top and try reading it the way Monika made me."
    "..."
    play sound modwriting
    "I cross out the second line and try another verb. Then I put the first one back after a minute of deliberation."
    "{i}It only has to exist by tomorrow. That is the entire standard.{/i}"
    "The word she circled this afternoon is still sitting in the second stanza. I leave it for a future disaster."
    "{i}She's going to ask why it's still there, and I'll have to pretend I didn't spend ten minutes on it.{/i}"
    mc "...Hm."
    mc "Ah, screw it..."
    "I put the notebook on top of my bag after rounds of looking at words until they don't look like words anymore."
    "With everything else packed to the bare minimum standard, I turn on the console and pick up the run I've made needlessly difficult for myself."
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 2.0
    pause 2.0
    scene bg home_entry_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music night_a
    "Night envelops the world with its stygian embrace." # poetic on purpose, as it's facetiously dramatic and macabre
    # SFX SUGGESTION: Quiet page turns layered with faint handheld button taps.
    "Tonight that amounts to Mom flipping the pages of her book in the living room, and Asahina on the floor tapping away at her handheld."
    "As for me, I decide to wrap things up early. My previous night of doomscrolling random wiki articles is to thank for that."
    "With the TV off, a little victory jingle from Asahina's game carries across the room while paper is rustled a little too forcefully."
    "She tilts the screen away when I pass. Whatever she's playing, I'm apparently not allowed to help."
    "A flavor packet patiently waits its turn as I pour water into a timeworn glass."
    # NUDGE DECIDE 10.8: if this is the allergy pill from May 20, say "my allergy pill". Otherwise cut "prescribed" or plan to follow it up.
    "Before clocking out, I take a massive swig, down my medication, and--"
    show asahina curious at l11
    ah "Do we have any glue? Bottle glue with the white, sticky stuff, not the useless stick that's all dried up."
    "{i}Dude, phrasing...{/i}"
    mc "I... think? Have you checked the drawer with the scissors?"
    show asahina frustrated
    ah "You think I haven't?! Uuuuughhhhh, what do I do...?"
    mc "What do you need it for, anyway?"
    ah "The poster! I thought we had everything, so I honestly didn't check until now."
    mc "The one you said was--"
    ah unamused "Don't. Do not finish that sentence, I swear."
    ah angry "They said 'as soon as humanly possible.' Like what the hell does that mean? Give me an actual day!"
    show asahina shocked at h11
    mom "I can hear you, Asahina."
    show asahina annoyed at t11
    ah "That's barely swearing!"
    show asahina neut
    ah "...So, anyway. Yeah."
    mc "Well, I can't make glue."
    show asahina nervous
    ah nervous "I know. I'm asking if you've seen any."
    "My planned game run on Saturday gives me an idea."
    mc "Actually, hear me out. Know that new RPG I preordered way back when? It comes out Saturday, so I can grab glue while I'm at the store picking it up. Will that be soon enough?"
    "Asahina sighs and takes a subtle bow."
    show asahina happy
    ah "Yes! That'd be amazing! Best brother in the house."
    mc "Also only brother in the house."
    ah smug "Uh, yeah, winner by default."
    show asahina embarrassed
    ah "And I'll replace your chips. Before you start, yes, I was already going to."
    mc "Yeah, sure, why not. It's a deal."
    show asahina teasing
    ah "Shake on it."
    mc "Uh, no. I'm not falling for one of your whoopie cushion antics."
    ah annoyed "God, fine. Verbal agreement."
    show asahina neut
    "I tip my glass for another drink and find it empty. At some point during the glue negotiations, I finished it."
    mc "Can I go to bed now, or am I buying anything else?"
    show asahina teasing
    ah "Nah, I'm good now. You're free to go."
    mc "Says the staller."
    mom "Both of you. It's a school night."
    show asahina annoyed
    ah "It's not even that late!"
    mom "Then you can wind down before it is."
    show asahina teasing
    show asahina at thide
    hide asahina
    "{i}Way for her to trip me into doing her fetch quests...{/i}"
    $ hide_calendar()
    scene black with dissolve_scene_full
    nier "I set a reminder to check the arts-and-crafts aisle Saturday, then pass through the kitchen for something sweet."
    nier "Asahina's plate is already rinsed and face-down in the rack. A paper towel lies flat across the trash in the bin under the sink."
    nier "I put my glass beside her plate and go up."
    call nier_clear from _call_nier_clear_0515_8
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0515_1
    jump a0516
