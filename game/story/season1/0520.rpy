label a0520:
    # --- Day 6: 2025-05-20 ---
    scene black
    $ show_calendar()
    # CRITIQUE: Cute opening, but the Monika text banter now has a familiar rhythm: joke, counter-joke, cute tag. Watch repetition before the relationship starts sounding scripted rather than alive.
    python:
        _phone_messages = [
            phone_msg("me", "Morning. Minor life update: my foot has been promoted from Problem to Mostly Normal."),
            phone_msg("them", "Good morning! Also good! Does that mean track is back?"),
            phone_msg("me", "Starting tomorrow, yeah. Coach cleared me for light practice."),
            phone_msg("me", "Which I assume means I get to suffer in moderation."),
            phone_msg("them", "Responsible suffering. The best kind."),
            phone_msg("me", "So I'll start dividing afternoons again. Track some days, club the others."),
            phone_msg("them", "Ah, so the club room is losing full custody of you."),
            phone_msg("me", "Joint custody. Very modern arrangement."),
            phone_msg("them", "I'll prepare one extremely tasteful poem for your first day back."),
            phone_msg("me", "If I die during warmups, tell everyone I was brave and not stupid."),
            phone_msg("them", "No promises on that second part~"),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0520_1
    $ hide_calendar()
    scene bg kitchen
    $ show_calendar()
    show mood_home zorder 3 
    with dissolve_scene_full
    play music dailyleisure
    window auto
    "The kitchen light is too bright for a Tuesday morning, which feels like a municipal violation."
    "I stand at the counter with a glass of water, a packet of allergy medicine, and the heroic posture of someone losing a battle against pollen."
    "My sinuses have chosen violence."
    # CRITIQUE: Meme phrasing like "chosen violence" can date the narration quickly. MC's voice is quippy, but repeated internet idioms may age faster than the character work around them.
    "{i}Trees reproduce one time and suddenly I have to negotiate with my own face.{/i}"
    "I pop the tablet from the foil and wash it down with water that has not had enough time to become anything but cold."
    mc "...God, I suck at swallowing these things..."
    mc "You can do it, pill. Just like we practiced..."
    "The floor creaks behind me."
    show mom neut at t11
    mom "I hope you're not giving motivational speeches to medicine."
    mc "It needs to know I believe in it."
    mom "I see."
    mom "And does it believe in you?"
    mc "Give it twenty minutes."
    "Mom sets her work bag on one chair and starts the kettle with the tired precision of someone who has already been awake too long."
    "She's dressed for court-adjacent warfare: blouse, slacks, hair pinned back, expression calm enough to make other people nervous."
    mc "Early start?"
    mom "Unfortunately."
    mom "A case landed on my desk yesterday afternoon, which is always a promising start."
    mc "Landed how?"
    mom "Hot-potatoed."
    mc "Ah. Professional."
    mom "That is the legal term, obviously."
    mom "The short version is that another attorney had a scheduling conflict, the client is anxious, and I'm now catching up on a file that's decided to be much thicker than advertised."
    "She says it like the file personally betrayed her."
    mc "Can files do that?"
    mom "Constantly."
    "The kettle begins its low hiss."
    "Mom checks her phone, then turns it facedown before the screen can ask more of her."
    mom "I may be home especially late tonight."
    mc "How late are we talking?"
    mom "Late enough that dinner shouldn't wait on me."
    mc "That feels like an intentionally vague unit of time."
    mom "It is."
    mom "There are leftovers, and Asahina already asked if Sam could come over after homework."
    "I blink once."
    mc "She asked you before asking me?"
    mom "Unfortunately, you're not the household scheduling office."
    mc "I would like that in writing for future disputes."
    mom "Denied."
    "She pulls a mug from the cabinet and points at me with it."
    mom "Doors stay open. Food stays in the kitchen. If anyone breaks anything, I will know."
    mc "Do I get a badge, or is this more of an unpaid internship kinda thing?"
    mom "You get my trust."
    # CRITIQUE: Strong line. After it, give MC one physical reaction or private discomfort before the next joke; trust should land heavier than a punchline.
    "{i}Damn. She used the serious currency.{/i}"
    mc "Got it."
    mom "Good."
    mom "Also, take another dose after dinner if the pollen is still bothering you. Not before."
    mc "Yes, doctor mom."
    mom "Counselor mom, actually. Doctor mom bills more."
    "The kettle clicks off. Morning continues doing morning things."
    show mom at thide
    hide mom
    $ hide_calendar()
    scene black with wipeleft_scene
    # CRITIQUE: Proofreading nit: "dumbell" should be "dumbbell."
    nier "The rest of breakfast happens in the usual fragments: toast, bag checks, Asahina shouting from upstairs that she is not late while clearly being late, and mom leaving with a folder thick enough to count as a dumbell."
    nier "By the time I step outside, the allergy medicine has achieved the advanced medical state known as maybe doing something."
    call nier_clear from _call_nier_clear_0520_1
    stop music fadeout 1.0
    pause 1.0
    scene bg class_day
    $ show_calendar()
    show mood_afternoon zorder 3 
    with dissolve_scene_full
    play music dailyfantasy
    # CRITIQUE: Midterm pressure is mostly delivered as a list. Make the burden sensory: overfull bag, crowded margins, sore hand, classmates bargaining with panic.
    "By the middle of the school day, science has become a room full of diagrams that look simple until someone asks what they mean."
    "The teacher draws a cell on the board, labels the nucleus, and taps the chalk against it twice."
    show science_teacher neut at t11
    science_teacher "Remember, the point is not to memorize the diagram as a picture."
    science_teacher "You need to understand what each structure does and how it contributes to the larger system."
    "A few students write that down with the panic of people who know a phrase has just become test material."
    "{i}Larger system. Got it. Cells are just tiny bureaucracies with better membranes.{/i}"
    "My pencil moves across the page anyway."
    "Nucleus. Mitochondria. Ribosomes. Endoplasmic reticulum."
    "{i}The endoplasmic reticulum sounds like a dungeon that asks for a membership card.{/i}"
    science_teacher "Also, before anyone tries to leave this room under the protection of selective hearing..."
    "The chalk returns to the tray."
    science_teacher "Midterm exams begin next Monday."
    "The whole class makes the quiet sound of a group remembering consequences exist."
    science_teacher "Science will be on the second day, but do {i}not{/i} use that as an excuse to start studying on the first day."
    science_teacher "The review guide is posted. It covers a review on cell structure, intermediate genetics, and the first half of our ecology unit."
    "Somewhere behind me, someone whispers something that sounds like a prayer."
    "{i}Right. Midterms. Track practice. Club time. The new game. Homework. Existing as a person.{/i}"
    "{i}Very cool. Very balanced. Love this for me.{/i}"
    science_teacher "Questions?"
    "No one moves."
    "It is the silence of people with many questions and no desire to be perceived."
    science_teacher "Excellent. Then we continue."
    show science_teacher at thide
    hide science_teacher
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Science carries on from there, which is rude but legally allowed."
    nier "The rest of the day stacks itself into homework reminders, exam warnings, and a lunch period that ends approximately thirty seconds after I finally stop thinking about school."
    nier "By the final bell, my bag feels heavier despite containing the same number of objects. This is probably physics, but I refuse to ask science for anything else today."
    call nier_clear from _call_nier_clear_0520_2
    scene bg club_day
    $ show_calendar()
    show mood_afternoon zorder 3 
    with wipeleft_scene
    "The club room is quiet when I arrive."
    "Not empty, thankfully. Just quiet in the way rooms get when afternoon light turns everything into a suggestion."
    show monika 1a at t11
    "Monika is at the front desk with a stack of papers, one notebook, and the unmistakable posture of someone pretending she is not making a list."
    m "Hey, there he is!"
    mc "Reporting for joint custody."
    m "I knew that would stick~"
    "I drop my bag beside my usual desk and lower myself into the chair."
    mc "Biology reminded us midterms start next Monday."
    m "Yeah..."
    m "I was trying to enjoy the last few minutes before someone said the word midterms in here."
    mc "My bad. I brought the academic haunting indoors."
    m "It's fine. It was going to find us eventually."
    "She taps the stack of papers into alignment."
    m "Anyway, nothing dramatic today. I figured we could read for a while, then do a light writing prompt if we still have brain cells left."
    mc "I have at least two."
    m "Perfect. One for reading and one for writing."
    mc "What about breathing?"
    m "Automatic process, doesn't count."
    "I pull a paperback from my bag and open it to the bookmark."
    "Monika returns to her notebook, pen moving in small, neat lines."
    "For a while, that's all club is."
    "Page turns, pencil scratches, and a chair creaking once because I apparently cannot sit like a normal organism."
    show monika at thide
    hide monika
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Club time passes without incident."
    nier "Surprisingly, there were no dramatic declarations all day from people wearing gloves indoors."
    nier "Monika gives us a prompt about writing a place that feels safe without using the word safe, which is exactly the kind of assignment that sounds harmless until you try to do it."
    # CRITIQUE: This prompt is thematically perfect for MC, and you skip the piece. Show a few lines about the bus seat; it would reveal more than another summary can.
    nier "I write about a bus seat by the window and then decide that says more about me than I want reviewed in public."
    call nier_clear from _call_nier_clear_0520_3
    scene bg club_day
    $ show_calendar()
    show mood_evening zorder 3 
    show monika 1a at t11
    with wipeleft_scene
    "By the time the light starts waning around the windows, Monika closes her notebook."
    m "Not bad today!"
    mc "For the club, or for civilization?"
    m "Let's not grade civilization before midterms. I don't think it studied."
    mc "...I guess?"
    "I pack slowly, partly because I don't want to forget anything and partly because leaving means Tuesday gets to continue."
    m "Good luck with track tomorrow!"
    mc "Oh come on, I'm not THAT out of shape! Still though, appreciate it."
    mc "If I limp in here Thursday, pretend not to notice."
    m "Absolutely not. I will notice rrrrrresponsibly."
    mc "That sounds kinda worse."
    m "It is...kinda."
    "I give her a lazy salute with two fingers."
    mc "Later."
    m "Later, alligator~"
    show monika at thide
    hide monika
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The trip home is exactly normal, which makes it suspicious for about three seconds before my attention span gives up."
    nier "I stop by the convenience store for a drink, regret the price, buy it anyway, and make it home with the heroic pride of someone who has survived yet another Tuesday."
    call nier_clear from _call_nier_clear_0520_4
    stop music fadeout 1.0
    pause 1.0
    scene bg bedroom
    $ show_calendar()
    show mood_home zorder 3 
    with wipeleft_scene
    play music fantasyserenity
    "Evening settles into my room with the specific laziness of a weekday that knows it has homework as leverage."
    "I have my notebook open, my pen in hand, and absolutely none of the moral strength required to start the first problem about energy conservation."
    "My phone buzzes before I can be forced to grow as a person."
    python:
        _phone_messages = [
            phone_msg("them", "Acquisition complete."),
            phone_msg("me", "You bought it?"),
            phone_msg("them", "Indeed. My wallet died with honor."),
            phone_msg("them", "Installation begins now. If this game wastes my evening, I will hold you emotionally accountable."),
            phone_msg("me", "You chose this."),
            phone_msg("them", "I choose many things. Accountability is for witnesses."),
            phone_msg("them", "I shall keep you updated."),
            phone_msg("me", "Please define updated."),
            phone_msg("them", "Updated. Adjective. Having the most recent information at a given point in time."),
            phone_msg("me", "...")
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, append=True) from _call_phone_text_conversation_0520_2
    "I set the phone facedown."
    "It buzzes again almost immediately and I valiantly resist the urge to pick it back up."
    "{i}Boundaries. Look at me. Personal growth at desk level.{/i}"
    "The phone buzzes a third time."
    "{i}...Tiny personal growth.{/i}"
    "Before I can lose the battle completely, a laugh rises from downstairs--Asahina's laugh."
    "Then a second one, lower and smoother."
    "{i}Right. The guy's here.{/i}"
    "I close my notebook with the relief of someone whose procrastination has found legal representation."
    $ hide_calendar()
    scene black with wipeleft_scene
    scene bg living_room_night
    $ show_calendar()
    show mood_home zorder 3 
    with wipeleft_scene
    "The living room has turned into a small-scale occupation."
    "Asahina is on the floor by the coffee table with one controller in her lap, and Sam is on the couch leaning forward like the game has personally challenged his bloodline."
    show asahina neut at t21
    show sam neut at t22
    "The TV is paused on a character select screen bright enough to qualify as weather."
    
    ah "Oh, look. The responsible adult has emerged."
    
    mc "I, uh, came downstairs for water."
    sa "Convenient. We need a third."
    mc "For what?"
    
    ah "Party mode."
    ah "Unless your old bones can't handle it."
    
    mc "I am {i}two{/i} years older than you."
    
    ah "Yeah, you're practically a fossil, God you're so old."
    
    sa "Do I need to make you a tomb?"
    "He says it casually, like we're already the kind of people who can insult each other without filing paperwork first."
    "{i}That's probably a good sign.{/i}"
    "I rub my temples."
    mc "You know, I was actually very busy upstairs."
    
    ah "Doing homework?"
    
    mc "Opening the notebook is part of the process."
    
    ah "So...no."
    ah "Hey, me neither, don't feel bad, brotato chip."
    
    mc "...Move over."
    sa "Aaaaand there it is."
    "I take the empty spot on the floor, which puts me beside the coffee table and directly in the jurisdiction of snack crumbs."
    "Asahina hands me the crappy third-party AngryDawgz controller."
    ah "Try not to embarrass the family."
    mc "Our family has survived your quote-unquote group projects. It can survive anything."
    ah "Rude!"
    
    "She hits me right in the ribcage."
    sa "I don't know, your poster looked pretty good."
    "Asahina's whole face tries to pretend that didn't matter."
    "It fails with the enthusiasm of a cheap lock."
    ah "It was decent, methinks."
    mc "She spent all weekend acting like the glue bottle was like some outland commander that was her sworn enemy."
    # CRITIQUE: Proofreading nit: the sentence ends with both "!." Pick one mark.
    ah "Because it WAS, okay? You have no idea!."
    sa "Then congratulations on your victory."
    "She bumps his knee with her shoulder and looks back at the TV before her face can give away anything more incriminating."
    "{i}Wow.{/i}"
    "{i}I am suddenly in a room with subtitles I cannot read.{/i}"
    "During my own monologue, the game starts."
    show asahina at thide
    hide asahina
    show sam at thide
    hide sam
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Party mode is, in theory, a game about timing, luck, and mild betrayal."
    nier "In practice, it becomes Asahina and Sam developing an entire two-person ecosystem while I sit three feet away and occasionally get hit by cartoon explosives."
    nier "They don't ignore me exactly. That would be easier to process."
    nier "Sam passes me snacks without asking. Asahina tells him which character I always pick. Sam remembers that information two rounds later."
    nier "Somehow, that makes me feel more like a guest than being ignored would have."
    call nier_clear from _call_nier_clear_0520_5
    scene bg living_room_night
    $ show_calendar()
    show mood_home zorder 3 
    show asahina neut at t21
    show sam neut at t22
    with wipeleft_scene
    mc "Okay, hold on. Since when do you use that shortcut?"
    
    ah "Since forever."
    
    mc "You absolutely did not know that last month."
    sa "We practiced."
    mc "...'We.'"
    ah "Yes, we. People are allowed to improve when you're not looking."
    mc "That sounds fake as hell."
    sa "No, it's true. I looked it up."
    "The two of them exchange a glance."
    "Not even a long one--just enough for some private joke to pass between them without needing to say a word."
    # CRITIQUE: This is excellent third-wheel material because the details are concrete: snacks, remembered character picks, shared glances. Resist ending every discovery with a joke, because the alienation is the actual scene.
    "{i}Ah.{/i}"
    "{i}So this is what third-wheeling feels like when nobody is technically doing anything wrong.{/i}"
    ah "You good?"
    mc "Yeah. Just calculating how hard I'm getting carried."
    sa "Not that hard."
    ah "Pretty hard."
    mc "Balanced feedback, thank you, we take those."
    "My phone buzzes against my leg."
    "Matsuda, probably, sending another progress report from whatever digital battlefield she has thrown herself into."
    "I leave it alone."
    "For once, it's probably the easiest thing I can do right now."
    "The round ends with Asahina winning by a margin that feels medically suspicious."
    ah "Ha! Get rekt! I'm just better!"
    mc "...This household needs stricter humility laws."
    sa "I'd vote for that."
    ah "Traitor!"
    sa "I said I'd vote. I didn't say which way."
    "Asahina points at him like she has discovered corruption at the highest level."
    "Sam smiles back, completely unbothered."
    "{i}Yeah. He's good at this.{/i}"
    "{i}Still not necessarily bad.{/i}"
    "{i}Still definitely a thing.{/i}"
    show asahina at thide
    hide asahina
    show sam at thide
    hide sam
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The night moves on through more rounds, takeout that Sam ordered, and mom texting that the case is still eating her evening."
    nier "Sam helps carry dishes to the kitchen without making a production out of it."
    nier "Asahina notices and tries not to look pleased...again. This is becoming a recurring household sport."
    call nier_clear from _call_nier_clear_0520_6
    scene bg doornight
    $ show_calendar()
    show mood_night zorder 3 
    with wipeleft_scene
    "Sam leaves a little before mom said she'd get back."
    show asahina neut at t21
    show sam neut at t22
    "Asahina walks him to the door, which is normal."
    "They proceed to stand by the door after it has already opened, which is also apparently normal if you are sixteen and allergic to efficient goodbyes."
    sa "Thanks for letting me hang out."
    mc "Yeah. No problem."
    
    ah "He means thanks for helping him lose."
    
    mc "...I mean no such thing."
    sa "Hey, regardless, I had fun."
    # CRITIQUE: Sam's direct inclusion is effective. Because the roadmap positions him as a catalyst with a hidden edge, consider planting one tiny ambiguity here instead of letting him read as purely wholesome.
    "He looks at me when he says it."
    "{i}Directly{/i} at me, like he remembered the room had three people in it."
    mc "Yeah. Same."
    "And I mean it, which is inconvenient."
    sa "Cool! See you 'round, [player]."
    mc "Later."
    show sam at thide
    hide sam
    play sound moddoorclose
    "He steps outside."
    "Asahina follows him just far enough to say whatever goodbye did not qualify for indoor broadcast."
    "I turn away before she can accuse me of spying, because for once I would like to be innocent on a technicality."
    show asahina neut at t11
    "When she comes back in, her face is aggressively neutral."
    mc "Fun night?"
    ah "It was fine."
    mc "That's your it-was-fun voice."
    ah "Shut the hell your mouth!"
    
    "There it is."
    "A small, familiar victory."
    "I start up the stairs before she can recover."
    show asahina at thide
    hide asahina
    $ hide_calendar()
    scene black with wipeleft_scene
    scene bg bedroom
    $ show_calendar()
    show mood_night zorder 3 
    with wipeleft_scene
    "My room has not moved, which is considerate of it."
    "My homework is still open on the desk. My phone is still carrying the weight of several unread messages."
    "I check Matsuda's thread first, because curiosity has apparently survived all attempts at discipline."
    python:
        _phone_messages = [
            phone_msg("them", "Update the first: tutorial complete. Combat has hands."),
            phone_msg("them", "Update the second: I have been betrayed by poopy menu design."),
            phone_msg("them", "Update the third: okay, it is preeeeeeetty good. You win this round."),
            phone_msg("me", "Historically bad, remember?"),
            phone_msg("them", "Yeah, for my sleep schedule."),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, append=True) from _call_phone_text_conversation_0520_3
    "I put the phone down and rub my eyes."
    "Tomorrow has track practice. Next Monday has midterms. Somewhere downstairs, Asahina is probably texting Sam the parts of tonight I did not need to hear in real time."
    play sound moddooropen
    "Mom gets home late enough that I only catch the front door opening through the floorboards."
    "{i}Longer day than I'm used to.{/i}"
    "{i}...Whatever those are worth.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Sleep takes a while to find me."
    nier "Not because anything is wrong, exactly."
    nier "Just because today was full of small things, and small things have a way of taking up more space after the lights are off."
    call nier_clear from _call_nier_clear_0520_7
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0520_1
    jump a0521
