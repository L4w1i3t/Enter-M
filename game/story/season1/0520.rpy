label a0520:
    # --- Day 6: 2025-05-20 ---
    scene black
    $ show_calendar()
    pause 2.0
    python:
        _phone_messages = [
            phone_msg("me", "Morning. Minor life update: my foot has been promoted from Complete Doodoo to Kind of Doodoo."),
            phone_msg("them", "Good morning! Also good! Does that mean track is back?"),
            phone_msg("me", "Starting tomorrow, yeah. Coach called and cleared me for light practice."),
            phone_msg("me", "Which I assume means I get to suffer in moderation."),
            phone_msg("them", "Responsible suffering. The best kind."),
            phone_msg("me", "So I'll start dividing afternoons again. Track some days, club the others."),
            phone_msg("them", "Ah. So the club room is losing full custody of you."),
            phone_msg("me", "Joint custody. Very modern arrangement."),
            phone_msg("them", "I'll allow it. I had you to myself for a whole month. That's basically greedy by club standards."),
            phone_msg("me", "If I die during warmups, tell everyone I was brave and not stupid."),
            phone_msg("them", "No promises on that second part!"),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0520_1
    $ hide_calendar()
    pause 2.0
    scene bg kitchen
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music dailyleisure
    window auto
    "I stand at the counter with a glass of water and a packet of allergy medicine."
    "{i}Trees reproduce one time and suddenly they've chosen violence.{/i}"
    mc "You can do it, pill. Just like we practiced..."
    "I pop the tablet from the foil and wash it down with a drink that has not had enough time to become anything but cold."
    mc "...God, I suck at swallowing these."
    "The floor creaks behind me."
    show mom uniform happy at l11
    mom "Hahaha, I know you're not sweet-talking medicine."
    mc "It needs to know I believe in it."
    mom teasing "I see..."
    mom "And does it believe in you?"
    mc "Give it twenty minutes."
    "She sets her work bag on the end of the counter and starts the kettle in the precise, joyless way that means she has been up for hours already."
    "She's dressed for court-adjacent warfare: blouse, slacks, hair pinned back, and the calm that makes other people nervous."
    mc "Early start?"
    show mom uniform unamused
    mom "Unfortunately."
    mom "A case landed on my desk yesterday afternoon, which is...always a promising start."
    mc "Landed how?"
    mom "Hot-potatoed."
    mc "Ah. Professional."
    show mom uniform smug
    mom "That is the legal term, obviously."
    mom "The short version is that another attorney had a scheduling conflict, the client is anxious, and I'm now catching up on a file that's much thicker than advertised..."
    show mom uniform frustrated
    "She runs her hands over her face, pulling the bottoms of her eye sockets down."
    mom "Uuuugh, and it's the one thing I don't wanna do, too..."
    mc "...Files can advertise?"
    mom "You have no idea, kiddo..."
    "The kettle begins its low hiss."
    show mom uniform neut
    "She checks her phone, then turns it facedown before the screen can ask more of her."
    mom "I may be home especially late tonight."
    mc "How late are we talking?"
    mom "Late enough that dinner shouldn't wait on me."
    mc "That feels like an intentionally...vague unit of time."
    mom "It is."
    mom "There are leftovers, and Asahina already asked if Sam could come over after homework."
    "I blink once."
    mc "She asked you before asking me?"
    show mom uniform teasing
    mom "Unfortunately--or fortunately--you're not the household scheduling office."
    mc "I would like that in writing for future disputes."
    show mom uniform unamused
    mom "Denied."
    show mom uniform determined
    "She pulls a mug from the cabinet and points at me with it."
    mom "Same rules as Friday. If anyone breaks anything, I'll know."
    mc "Do I get a badge, or is this more of an 'unpaid internship' kinda thing?"
    show mom uniform neut
    mom "You get my trust."
    "{i}She used the serious currency.{/i}"
    mc "Got it."
    mom "Good."
    mom "Also, take another dose after dinner if the pollen is still bothering you. Not before."
    mc "Yes, doctor Mom."
    show mom uniform smug
    mom "Still counselor Mom here. Doctor Mom bills more."
    # SFX SUGGESTION: The kettle's switch snapping off with a fading boil underneath.
    "The kettle clicks off and her hand finds it by memory."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The rest of breakfast happens in the usual fragments: toast, bag checks, Asahina shouting from upstairs that she is not late while clearly being late, and Mom leaving with a folder thick enough to count as a dumbbell."
    nier "By the time I step outside, the allergy medicine has achieved the advanced medical state known as maybe, perhaps, doing something."
    call nier_clear from _call_nier_clear_0520_1
    stop music fadeout 1.0
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with dissolve_scene_full
    play music quiz
    "By the middle of the school day, science has become a room full of diagrams that look simple until someone asks what they mean."
    show science_teacher neut at t11
    "The teacher draws a cell on the board and taps the chalk twice against the nucleus."
    show science_teacher neut
    science_teacher "Remember, the point is not to memorize the diagram as a picture."
    science_teacher "You need to understand what each structure does and how it contributes to the larger system."
    "A few students write that down fast, the way you transcribe anything the second it turns into test material."
    "{i}Cells are just tiny bureaucracies with better membranes... Heh, good one, I'm hilarious.{/i}"
    "My pencil copies it down between rounds of self-congratulation."
    "Nucleus. Mitochondria. Ribosomes. Endoplasmic reticulum."
    science_teacher "Also, before anyone tries to leave this room with supposed selective hearing..."
    "The chalk returns to the tray."
    science_teacher "Midterm exams begin next Monday."
    "The whole class makes the quiet sound of a group remembering consequences exist."
    science_teacher "Your sciences will be on the second day, but do {i}not{/i} use that as an excuse to start studying on the first day."
    science_teacher "The review guide is posted. It covers a review on cell structure, intermediate genetics, and the first half of our ecology unit."
    "Somewhere behind me, someone whispers what sounds like a prayer. To my left, a girl is already color-coding a study plan with four highlighters, bargaining with the calendar in real time."
    "My bag is already too full. From this morning's commute, the strap has pressed a red line into my shoulder I don't remember it earning."
    science_teacher "Questions?"
    "No one moves."
    "The silence says there are people with many questions and no desire to be perceived."
    science_teacher "Excellent. Then we continue."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The rest of the day stacks itself into homework reminders, exam warnings, and a lunch period that ends about thirty seconds after I finally stop thinking about school."
    call nier_clear from _call_nier_clear_0520_2
    stop music fadeout 1.0
    pause 2.0
    scene bg club_day
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with wipeleft_scene
    play music schooldays
    "A couple of the regulars are scattered around the edges of the club room--Hikari by the window, scribbling a line and crossing it out with equal violence, and Homura in the far corner, annotating someone's draft in handwriting too small to be casual."
    show monika forward uniform neut cm oe nobl rdown ldown at t11
    "Monika is at the front desk with a stack of papers and the unmistakable posture of someone pretending she is not making a list."
    m forward uniform happ om oe nobl rdown ldown "Hey, there he is!"
    mc "Reporting for joint custody."
    m forward uniform happ cm ce nobl rdown ldown "I knew that would stick~"
    "I drop my bag beside my usual desk and lower myself into the chair."
    mc "So, we got exams next week..."
    m forward uniform happ om ce nobl rdown ldown "Yeah..."
    m forward uniform wry cm oe nobl rhip ldown "I was trying to enjoy the last few minutes before someone said the word midterms in here."
    mc "My bad. I brought the academic haunting indoors."
    m forward uniform happ om oe nobl rhip ldown "It's fine. It was going to find us eventually."
    "She taps the stack of papers into alignment."
    m forward uniform happ om oe nobl rhip ldown "Anyway, nothing dramatic today. I figured we could read for a while, then do a light writing prompt if we still have brain cells left."
    mc "I have at least two."
    m forward uniform laug om ce nobl rdown ldown "Perfect. One for reading and one for writing."
    "I pull a paperback from my bag and open it to the bookmark."
    "She returns to her notebook, pen moving in small, neat lines."
    "For a while, that's all club is."
    "Page turns, pencil scratches, someone slamming their notebook a bit too hard, and a chair creaking once because I apparently cannot sit like a normal organism."
    $ hide_calendar()
    scene black with wipeleft_scene
    # CRITIQUE (ADDRESSED): Stopped skipping the piece. A couple of rough lines of the bus-seat draft are shown -- the first, abandoned attempt at the poem finished on May 24 -- so the prompt reveals more about MC than another summary, his bracket-hedging habit recurs, and the later payoff has a visible seed.
    nier "Monika gives us a prompt about writing a place that feels safe without using the word safe, which sounds harmless right up until you actually try to do it."
    nier "I sit with it a while, then write the only place that comes without an argument."
    nier "{i}The window seat on the late bus, where the glass turns everyone outside into someone I don't have to answer.{/i}"
    nier "{i}Nobody on a bus asks how you're holding up. The seat doesn't keep score. [[That's the closest word I've got, and it isn't the one she banned.]{/i}"
    nier "Then I close the notebook over it before anyone can ask to read."
    call nier_clear from _call_nier_clear_0520_3
    pause 2.0
    scene bg club_day
    $ show_calendar()
    $ atmos("evening")
    show monika forward uniform happ cm oe nobl rdown ldown at t11
    with wipeleft_scene
    "By the time the light starts waning around the windows, Monika closes her notebook."
    m forward uniform happ om oe nobl rdown ldown "Not bad today!"
    mc "For the club, or for civilization?"
    m forward uniform laug om ce nobl rhip ldown "Let's not grade civilization before midterms. I don't think it studied."
    "I pack slowly, partly because I don't want to forget anything and partly because leaving means Tuesday gets to continue."
    m forward uniform happ om oe nobl rdown ldown "Good luck with track tomorrow!"
    mc "If I limp in here Thursday, pretend not to notice."
    m forward uniform happ om oe nobl rdown lpoint "Absolutely not. I will notice rrrrrresponsibly."
    mc "That sounds...kinda worse."
    m forward uniform nerv om oe awkw rdown ldown "It is...kinda."
    "I give her a lazy salute with two fingers."
    mc "Later."
    m forward uniform happ cm ce nobl rdown ldown "Ten-four, dinosaur~"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I stop by the convenience store for a drink on the way home, regret the price, and buy it anyway."
    call nier_clear from _call_nier_clear_0520_4
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    play music fantasypassion
    "Evening gets into my room and brings homework along as leverage."
    "I have absolutely none of the moral strength required to start the first problem about energy conservation."
    # SFX SUGGESTION: A notification buzz here, followed by the same buzz at shorter intervals below.
    "After about ten minutes of staring into the abyss, my phone buzzes before I can be forced to grow as a person."
    python:
        _phone_messages = [
            phone_msg("them", "Acquisition complete."),
            phone_msg("me", "You bought it?"),
            phone_msg("them", "Indeed. My wallet died with honor."),
            phone_msg("them", "Installation begins now. If this game wastes my evening, I will hold you emotionally accountable."),
            phone_msg("me", "Good luck. You chose this."),
            phone_msg("them", "I choose many things. Accountability is for witnesses."),
            phone_msg("them", "I shall keep you updated."),
            phone_msg("me", "Please define updated."),
            phone_msg("them", "Updated. Adjective. Having the most recent information at a given point in time."),
            phone_msg("me", "..."),
            phone_msg("me", "My fault for asking.")
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, append=True) from _call_phone_text_conversation_0520_2
    # THE first time Matsuda reaches out that isn't May 17. May 17 was her taking
    # his number off a sidewalk collision, which is an introduction, not an open
    # line; this is her texting him at night about nothing in particular. Her
    # idle chatter unlocks here and not a day earlier.
    $ phone_open("matsuda")
    "I turn the phone over and leave it there."
    "It buzzes again almost immediately and I valiantly resist the urge to pick it back up."
    "The phone buzzes a third time."
    "{i}...Tiny personal growth.{/i}"
    "Then a laugh rises from downstairs--Asahina's laugh."
    "Then a second one, lower and smoother."
    "{i}Right. The guy's here.{/i}"
    "{i}...Frick.{/i}"
    "I close my notebook."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg living_room_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    "The living room has been occupied."
    "Asahina is on the floor by the coffee table with one controller in her lap, and Sam is on the couch leaning forward like the game has personally challenged his bloodline."
    "{i}The gamer stance already, eh?{/i}"
    show asahina teasing at t21
    show sam neut at t22
    "The TV is paused on a character select screen so bright it counts as weather."
    ah "Oh, look. The responsible adult has emerged."
    mc "I, uh, came downstairs for water."
    show sam casual pose_open_hand
    sa "Convenient. We need a third."
    mc "For...what?"
    ah "Party mode. Unless your old bones can't handle it."
    mc "I am {i}two{/i} years older than you."
    show sam casual teasing
    sa "Do I need to make you a tomb?"
    "He says it casually, like we're already past the part where insulting each other needs a mediator."
    "I rub my temples."
    mc "You know, I was actually very busy upstairs."
    ah "Doing homework? Or...? Oh, you {i}were{/i}, weren't you?"
    mc "Opening the notebook is part of the process of doing homework."
    show asahina neut
    ah "So...the other thing."
    ah "Hey, me neither. Don't sweat it, dork."
    mc "...Move over."
    show sam casual smug
    sa "Aaaaand there it is."
    "I take the empty spot on the floor, beside the coffee table and directly in the backdrop of snack crumbs."
    "Asahina hands me the crappy third-party AngryDawgz controller."
    show asahina smug
    ah "Try not to embarrass the family."
    mc "Our family has survived your quote-unquote group projects. It can survive anything."
    show asahina annoyed
    ah "Rude!"
    # SFX SUGGESTION: A soft, cloth-muted body thump rather than a heavy combat impact.
    "She hits me right in the ribcage."
    show sam casual happy
    sa "I don't know, your poster looked pretty good."
    show asahina embarrassed
    ah "...It was decent, methinks."
    show sam casual teasing
    sa "Then congratulations on your victory."
    "She bumps his knee with her shoulder and looks back at the TV."
    # SFX SUGGESTION: A bright party-game round-start jingle from the television.
    "The game starts."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Party mode is, in theory, a game about timing, luck, and mild betrayal."
    nier "Sam passes me snacks without asking. Asahina tells him which character I always pick. Sam remembers that information two rounds later."
    call nier_clear from _call_nier_clear_0520_5
    pause 2.0
    scene bg living_room_night
    $ show_calendar()
    $ atmos("home_night")
    show asahina smug at t21
    show sam neut at t22
    with wipeleft_scene
    mc "Okay, hold on. Since when do you use that shortcut?"
    ah "Since forever."
    mc "You absolutely did not know that last month."
    sa "We practiced."
    mc "...'We.'"
    show asahina unamused
    ah "Yes, we. We're not NPCs that derender when you're not looking."
    mc "That sounds fake as hell."
    show sam casual smug
    sa "No, it's true. I looked it up."
    "The two of them exchange a glance. Not even a long one. A whole joke goes across the table inside it."
    # CRITIQUE (ADDRESSED): Let the alienation breathe before the deflection -- MC names the feeling (a small room he doesn't have a key to, snacks handed politely through the door) and notably doesn't say it to anyone, his self-hiding pattern, before the joke. The discovery isn't joked away.
    "It's not that they're shutting me out. It's that they've built a small room I don't have a key to, and they're being very polite about handing me snacks through the door."
    "...In my own house, no less."
    "I don't say any of that. I'm not sure who I'd even say it to."
    show asahina curious
    ah "You good?"
    mc "Yeah. Just calculating how hard I'm getting reamed."
    show sam casual happy
    sa "Not that hard."
    show asahina teasing
    ah "Pretty firetruckin' hard."
    mc "Balanced feedback, thank you, we take those."
    "My phone buzzes against my leg."
    "Matsuda, probably, sending another progress report from whatever digital battlefield she has thrown herself into."
    "I leave it alone."
    "The round ends with Asahina winning by a margin that feels medically suspicious."
    show asahina happy
    ah "Ha! Get wrecked! I'm just better!"
    mc "...This household needs stricter humility laws."
    show sam casual smug
    sa "I'd vote for that."
    show asahina shocked
    ah "Traitor!"
    show sam casual teasing
    sa "I said I'd vote. I didn't say which way."
    "Asahina points at him like she has discovered corruption at the highest level."
    show sam casual happy
    "Sam smiles back, completely unbothered."
    "{i}Yeah. He's good at this.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The night moves on through more rounds, pizza that Sam ordered, and Mom texting that the case is still eating her evening."
    call nier_clear from _call_nier_clear_0520_6
    pause 2.0
    scene bg doornight
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    "Sam leaves a little before Mom said she'd get back."
    show asahina teasing at t21
    show sam casual pose_phone at t22
    "Asahina walks him to the door. The distance does not justify the ceremony."
    show sam casual neut
    "They proceed to stand by the door after it has already opened, apparently a normal thing to do if you are sixteen and allergic to efficient goodbyes."
    sa "Thanks for letting me hang out."
    mc "Yeah. No problem."
    ah "He means thanks for helping him lose."
    mc "...I mean no such thing."
    show sam casual determined
    sa "Hey, either way, I had fun."
    # CRITIQUE (ADDRESSED): Sharpened the existing tiny ambiguity rather than adding a second red flag (Sam's one wrong note is the Day-2 "eating better" beat). His warmth toward MC reads, very slightly, as a move he remembered to make -- inclusion as technique -- which MC half-clocks and then talks himself out of, echoing his Day-2 "waiting for the seam" line. Deniable, on the page.
    "He looks at me when he says it. Directly, deliberately."
    mc "Yeah. Same."
    "And I mean it, which is the inconvenient part."
    show sam casual happy
    sa "Cool! See you 'round, [player]."
    mc "Later."
    show sam at thide
    hide sam
    play sound moddoorclose
    "He steps outside."
    show asahina at thide
    hide asahina
    "Asahina follows him out to say whatever goodbye did not qualify for indoor broadcast."
    "I turn away before she can accuse me of spying, because for once I would like to be innocent on a technicality."
    show asahina neut at l11
    "When she comes back in, her face is aggressively neutral."
    mc "Fun night?"
    ah "It was fine."
    mc "That's your it-was-fun voice."
    show asahina embarrassed
    ah "Shut the hell your mouth!"
    "I am four steps up the stairs by the time she recovers."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    "My room, at least, has not moved."
    "My homework is still open on the desk. My phone is still carrying the weight of several unread messages."
    "I check Matsuda's thread first, because curiosity has apparently survived all attempts at discipline."
    python:
        _phone_messages = [
            phone_msg("them", "Update the first: tutorial complete. Combat has hands."),
            phone_msg("them", "Update the second: this menu design is so ass lmao"),
            phone_msg("them", "Update the third: okay, it's preeeeeeetty good. You win this round."),
            phone_msg("me", "Historically bad, remember?"),
            phone_msg("them", "Yeah, for my sleep schedule."),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, append=True) from _call_phone_text_conversation_0520_3
    "I put the thread down and rub my eyes."
    "Tomorrow has track practice. Next Monday has midterms. Somewhere downstairs, Asahina is probably texting Sam the parts of tonight I did not need to hear in real time."
    play sound moddooropen
    "Mom gets home late enough that I only catch the sound of the front door opening through the small gap between my door and the floorboards."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Sleep takes a while to find me."
    call nier_clear from _call_nier_clear_0520_7
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0520_1
    jump a0521
