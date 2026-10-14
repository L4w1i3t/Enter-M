label a0520:
    # --- Day 6: 2025-05-20 ---
    scene black
    $ show_calendar()
    pause 2.0
    python:
        _phone_messages = [
            phone_msg("me", "Morning. Minor life update: my foot has been promoted from complete doodoo to mostly doodoo."),
            phone_msg("them", "Good morning, and that's good! Does that mean track is back?"),
            phone_msg("me", "Starting tomorrow, yeah. Light practice."),
            phone_msg("me", "Which I assume means I get to suffer in moderation."),
            phone_msg("them", "Responsible suffering. The best kind."),
            phone_msg("me", "So I'll start dividing afternoons again. Track some days, club the others."),
            phone_msg("them", "Ah. So the club room is losing full custody of you."),
            phone_msg("me", "Joint custody. Very modern arrangement."),
            phone_msg("them", "I'll allow it. I had you to myself for a whole month."),
            phone_msg("them", "That's basically greedy by club standards."),
            phone_msg("me", "If I die during warmups, tell everyone I was brave and not stupid."),
            phone_msg("them", "No promises!"),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0520_1
    $ hide_calendar()
    pause 2.0
    scene bg kitchen
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music house_day_a
    "I'm trying to open the allergy medicine without putting down my drink, which goes about as well as it sounds."
    "{i}All this because a tree wants to reproduce...{/i}"
    mc "You can do it, pill. Just like we practiced..."
    "I pop the tablet from the foil and chase it with water straight from the fridge."
    mc "...God, I suck at swallowing these."
    "The floor creaks behind me."
    show mom uniform happy at l11
    mom "Hahaha, I know you're not sweet-talking medicine."
    mc "It needs to know I believe in it."
    mom teasing "I see..."
    mom "And {i}does{/i} it believe in you?"
    mc "Give it twenty minutes."
    "She sets her work bag on the counter and starts the kettle. Her tea is already measured out beside the stove."
    mc "Early start?"
    show mom uniform unamused
    mom "Unfortunately."
    mom "I got handed a case yesterday afternoon. The hearing is this week."
    mc "How did it end up with you?"
    mom "Hot-potatoed."
    mc "Ah. Professional."
    show mom uniform smug
    mom "That is the legal term, obviously."
    mom "Another guy has a scheduling conflict, so I've got the file, but I still need the witness statements from the office."
    show mom uniform frustrated
    "She rubs both hands down her face."
    mom "And the handover notes are only three lines long..."
    mc "Better than nothing."
    mom "One of them is 'see attached' and there's literally nothing attached!"
    "The kettle begins its low hiss."
    show mom uniform neut
    "She checks her phone and turns it facedown beside it."
    mom "I may be home especially late tonight."
    mc "How late are we talking?"
    mom "Past dinner. Don't wait on me."
    mc "Should we save you something?"
    mom "If you don't mind. There's plenty of stuff here to get creative, and Asahina already asked if Sam could come over after homework."
    "I blink once."
    mc "She asked you before asking me?"
    show mom uniform teasing
    mom "Fortunately or otherwise, you're not the household scheduling office."
    mc "Well I know who to go to next time she asks me for more stuff."
    show mom uniform unamused
    mom "Denied."
    show mom uniform determined
    "She pulls a mug from the cabinet and points at me with it."
    mom "Same rules as Friday. If anyone breaks anything, I'll know."
    mc "So I'm responsible, but I don't get a say. Heh, wonderful."
    show mom uniform neut
    mom "You get my trust."
    "{i}Oh wow, she used the serious currency.{/i}"
    mc "...Got it."
    mom "Good."
    mom "Also, put the packet away when you're done. You left the empty one on the counter yesterday."
    mc "Yes, Mom..."
    show mom uniform smug
    mom "Thank you. My kitchen appreciates it."
    # SFX SUGGESTION: The kettle's switch snapping off with a fading boil underneath.
    "The kettle clicks off and her hand finds it by memory."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 1.0
    scene bg dining_table
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    "I take the cheese out for toast while Mom pours her tea."
    "Asahina arrives at 7:41 with one sock on and her hair doing something that will require a decision later."
    show asahina uniform annoyed at t11
    ah "Dude, you could have knocked!"
    mc "Your alarm went off. Twice."
    show asahina uniform unamused
    ah "Yeah, I heard. That was the problem."
    "She takes the last of the good jam without even so much as a glance at me and does not apologize for it."
    show asahina uniform neut
    ah "Sam's coming over after homework. He asked yesterday and I already said yes."
    mc "Mom told me. Apparently I'm the last to know."
    show asahina uniform smug
    ah "Yeah, chain of command, don'tcha know?"
    mc "There isn't--"
    ah "Then be around when I ask! You're always upstairs or out somewhere."
    "She spreads jam right up to the crust and bites into it."
    mc "...Wow. Okay, then."
    "I reach for the container, where she's left the knife in it, handle first."
    show asahina uniform teasing
    ah "Anyway, you can play with us tonight or whatever. Just don't stand behind the couch telling us what to do."
    mc "What's wrong with the advice?"
    ah "'I'd have taken the shortcut.' That same stupid voice."
    mc "I mean... I would have taken the shortcut."
    "She puts her plate in the sink instead of near it. Technically progress."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Mom leaves with a folder that could double as a dumbbell."
    nier "By the time I step outside, the allergy medicine has reached the advanced medical state known as maybe doing something."
    call nier_clear from _call_nier_clear_0520_1
    stop music fadeout 1.0
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with dissolve_scene_full
    play music quiz
    "In biology, a cell diagram fills the board beside the results of three experiments."
    show science_teacher neut at t11
    science_teacher "Remember, the point is not to memorize the diagram as a picture."
    science_teacher "Use it to trace the protein through the cell. Then look at where it accumulates in each experiment."
    "Several pens sprint to catch up the instant it sounds testable."
    science_teacher "Before we compare answers, check that you have the review guide."
    "The chalk returns to the tray."
    science_teacher "Remember: midterm exams begin next Monday."
    "{i}Ah, right, yes, the regularly scheduled judge for whether Monika or I gets valedictorian.{/i}"
    "A chair creaks behind me. Someone asks their neighbor which day chemistry is on."
    science_teacher "Your sciences will be on the second day, but do {i}not{/i} use that as an excuse to start studying on the first day."
    science_teacher "The review guide is posted. It covers cell structure, intermediate genetics, and the first half of our ecology unit."
    "To my left, a girl is already color-coding a study plan with four highlighters."
    "I write Tuesday above the science review list."
    science_teacher "Questions?"
    "A hand goes halfway up, then down again when the teacher points to the posted schedule."
    science_teacher "Excellent. Then we continue."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 1.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    "I eat in the hallway outside the third-year rooms, on the floor, between two window frames."
    "The cafeteria is louder than any room needs to be, so I have never once regretted the trade."
    "Lunch is whatever Mom assembled at six in the morning, which turns out to be rice and two things that used to be last night's dinner."
    show sam uniform neut at t11
    "Sam stops beside me with a wrapped sandwich and looks along the crowded hall. I pull my bag off the patch of floor by the window."
    sa "So this is the place, eh?"
    mc "You could've texted."
    sa "Yeah, if only I actually had you as a contact. Ah well, we're here now."
    "He sits and turns his phone toward me. A narrow walkway now crosses the moat around the house he showed me Friday, stopping in front of a tree."
    mc "Isn't that in front of the door? You could move it a bit."
    sa "Yeah, but I can see it from upstairs. I keep forgetting the house is supposed to work."
    "I enlarge the picture to see what holds the walkway up before handing it back. Sam puts the phone away and unwraps his sandwich."
    show sam uniform curious
    sa "Track tomorrow, right? Asa said you got cleared."
    mc "Seventy percent, then stop, or something like that. I was half asleep on the phone with my coach."
    sa "Is seventy percent a real number, or just one you made up?"
    mc "...Both, probably."
    "{i}That makes total sense.{/i}"
    show sam uniform happy
    sa "Yeah, sounds about right. My cousin got the same speech about a wrist and came back in nine days."
    mc "And how'd that go?"
    sa "Badly. I don't think she actually ever really recovered..."
    "Someone kicks my bag on the way past and apologizes to the wall behind me."
    show sam uniform neut
    sa "Exams start Monday for you guys too?"
    mc "Monday. Sciences on day two."
    sa "So Monday night is science night. I've got my worst one first."
    mc "That's rough."
    sa "I'll live. You got anything planned tonight besides revision?"
    mc "Uhhhhhhh... I don't know, actually. Today doesn't really have a schedule, school aside."
    "The corridor does its ordinary lunch noise around us."
    "My phone lights up beside the lunch box, and I turn it facedown while he finishes his bite."
    sa "I wish I had nothing to do... Gotta run to the fricken' auto store for my parents right after the last bell."
    show sam uniform curious
    sa "Actually, mind if I ask you something slightly random?"
    mc "Depends how much of it there is."
    sa "One question, and you can honestly tell me anything."
    menu:
        "(Answer straight.)":
            $ s1_pick("sam_lunch", "straight")
            mc "Sure. Go ahead."
        "(Answer sideways.)":
            $ s1_pick("sam_lunch", "sideways")
            mc "Ask it, and I'll decide afterward whether it counted."
        "(Say nothing and wait.)":
            $ s1_pick("sam_lunch", "wait")
            "I don't answer. I keep eating and let him get to it."
    show sam uniform neut
    sa "Soooo, does Asa talk to you about the volleyball stuff, or is that just a me thing?"
    "My chopsticks stop halfway up."
    mc "...That's a loaded question."
    sa "She was annoyed after practice, but she wouldn't tell me why. I wondered if she'd said anything at home."
    sa curious "I-I swear I'm trying not to be that kinda guy, but I was honestly kinda concerned."
    "I think about it for longer than the question probably wanted."
    mc "I get the scores. Sometimes a complaint about the coach or whoever was acting stupid during drills. Nothing this week, though."
    show sam uniform thinking
    sa "Yeah. That's about where I got to as well."
    "He nods and folds the loose end of his sandwich wrapper under his thumb."
    show sam uniform happy
    sa "Anyway. See you tonight, allegedly."
    mc "Allegedly?"
    sa "Asa invited me, then said you might be 'doing something lame.' Tonight's an open question."
    mc "...Apparently I've been overruled in advance."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Sam stays until the warning bell. We finish arguing about the shortcut on the way to class."
    nier "The afternoon stacks itself with homework and exam warnings."
    call nier_clear from _call_nier_clear_0520_2
    stop music fadeout 1.0
    pause 2.0
    scene bg club_day
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with wipeleft_scene
    play music school_day_a
    "{i}Alrighty, club. What do you got for me this time...?{/i}"
    "Hikari sits by the window, scribbling a line and crossing it out with equal violence. Her pink hair reflects the light in a way that's right in my eyes."
    "Homura annotates someone's draft in the far corner, her handwriting too curved to be casual. The way her pen glides across the paper is almost enough to give somebody a tickling feeling."
    show monika forward uniform neut cm oe nobl rdown ldown at t11
    "Monika is at the front desk with a stack of papers and her pen tucked behind one ear."
    m forward uniform happ om oe nobl rdown ldown "Hey, there he is!"
    mc "Reporting for joint custody."
    m forward uniform happ cm ce nobl rdown ldown "I knew that would stick~"
    "I drop my bag beside my usual desk and lower myself into the chair."
    mc "So, we got exams next week..."
    m forward uniform happ om ce nobl rdown ldown "Yeah..."
    m forward uniform wry cm oe nobl rhip ldown "I was trying to enjoy the last few minutes before someone said the word midterms in here."
    mc "Sorry. I could complain about pollen instead, if that's what you want."
    m forward uniform happ om oe nobl rhip ldown "Please spare me the pollen review. Get your book out, cause I wanna tear something else apart!"
    "She taps the stack of papers into alignment."
    m forward uniform happ om oe nobl rhip ldown "...Okay, I lied, bit of an exaggeration. Nothing dramatic today. I figured we could read for a while, then do a light writing prompt if we still have brain cells left."
    mc "I have at least two."
    m forward uniform laug om ce nobl rdown ldown "Perfect! One for reading and one for writing."
    "While she returns to her notebook, I open my paperback at the bookmark. For a while, we get on with it."
    "Pages turn and pencils scratch. Every so often Hikari punishes her notebook, or my chair reports another failure of posture."
    "After reading the same paragraph three times, I look up at the clock that has been two minutes fast since April. It still hasn't become anyone's job."
    "Homura reaches the end of somebody's draft, turns the page over, and starts again from the top."
    "When nobody answers Hikari's question about whether poems should have colons at the ends, she writes one in anyway."
    "Monika's pen stops for a brief moment as she uncaps a highlighter, sees the mark it leaves on her thumb, and goes searching through the stack for a scrap of paper."
    "I slide yesterday's handout across. She wipes her thumb on a margin I wasn't using."
    show monika forward uniform neut cm oe nobl rdown ldown
    m forward uniform curi om oe nobl rdown ldown "How's the book?"
    mc "It's about a guy who won't say what he wants."
    m forward uniform happ cm oe nobl rhip ldown "Ah. A documentary."
    mc "...Rude."
    m forward uniform laug om ce nobl rdown ldown "Don't blame me, you walked into it!"
    "She goes back to her page. The pen keeps moving after the smile stops."
    "Somebody drags a desk across the floor above us."
    "I've read six pages, and I don't particularly want to go anywhere."
    $ hide_calendar()
    scene black with wipeleft_scene
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
    "By the time the window light thins, Monika closes her notebook."
    m forward uniform happ om oe nobl rdown ldown "Not bad today!"
    mc "For the club, or for civilization?"
    m forward uniform laug om ce nobl rhip ldown "Let's not grade civilization before midterms... May be too much of a cheap shot."
    "I pack slowly, partly so I don't forget anything, and partly because leaving means Tuesday gets to continue."
    m forward uniform happ om oe nobl rdown ldown "Good luck with track tomorrow!"
    mc "If I limp in here Thursday, please at least pretend not to notice."
    m forward uniform happ om oe nobl rdown lpoint "Then I'm taking your bag and making you sit down."
    mc "Not a bad deal at all."
    m forward uniform happ om oe nobl rdown ldown "Good. Now go home so that you actually catch the bus."
    "I give her a lazy salute with two fingers."
    mc "Later."
    m forward uniform happ cm ce nobl rdown ldown "See you!"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I stop by the convenience store for a can of green tea on the way home. The price is a mistake I pay for anyway."
    call nier_clear from _call_nier_clear_0520_4
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    play music night_a
    "At home, I spread the homework across my desk and leave a space for literally anything else."
    "I have absolutely none of the moral strength required to start the first chemistry problem about reaction yield."
    # SFX SUGGESTION: A notification buzz here, followed by the same buzz at shorter intervals below.
    "Ten minutes of staring into the abyss, then my phone buzzes, and I am spared having to grow as a person."
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
    "I turn the phone over and leave it there. It buzzes again almost immediately, and I valiantly resist picking it back up."
    "By the third buzz, Asahina is laughing downstairs and Sam's voice follows hers."
    "I close the notebook with my pencil inside to hold the page, then go down to see what they're playing."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg living_room_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    "My sister sits on the living-room floor with a controller in her lap, while Sam leans so far forward on the couch that he might as well join her."
    "{i}The gamer stance already, eh?{/i}"
    show asahina teasing at t21
    show sam neut at t22
    "The TV is paused on a character select screen so bright it counts as weather."
    ah "Oh hey, there you are! You're playing next round."
    mc "I, uh, came downstairs for a snack."
    show sam casual pose_open_hand
    sa "Grab a controller. I'll start a new match."
    mc "For... what?"
    ah "Party mode. You can manage that, old man."
    mc "I am {i}two{/i} years older than you."
    show sam casual teasing
    sa "We can turn the speed or sensitivity down for you~"
    "He moves his feet so I can get past the couch."
    "I rub my temples."
    mc "You know, I was actually very busy upstairs."
    ah shocked "Doing homework? Or...? Oh, you {i}were{/i}, weren't you?"
    mc "Opening the notebook is part of the process of--"
    ah smug "Uh-huh, don't worry, I did that too earlier. Now sit down, you're blocking the screen."
    mc "...Move over."
    show sam casual happy
    sa "That was easy. I thought she'd have to go up and get you."
    "I take the empty spot beside the coffee table, directly in the field of cracker jack crumbs."
    "Asahina hands me the crappy third-party AngryDawgz controller."
    show asahina smug
    ah "Try not to embarrass the family. We {i}barely{/i} just got over bowling."
    mc "Our family survived your group projects. I think it can survive anything."
    show asahina annoyed
    ah "Rude!"
    # SFX SUGGESTION: A soft, cloth-muted body thump rather than a heavy combat impact.
    "She jabs my side with her elbow."
    show sam casual happy
    sa "I don't know about that. Her poster looked good, and I'm not being nice."
    show asahina embarrassed
    ah "...Maybe it didn't suck."
    show sam casual teasing
    sa "Then congratulations on your victory. Put that on the next one."
    "She bumps his knee with her shoulder and looks back at the TV, pressing the {i}START{/i} button on the screen."
    "Party mode is theoretically about luck and mild betrayal. Timing decides who gets to blame the controller."
    "Asahina mentions my usual character while Sam passes me snacks. Two rounds later, he actually remembers."
    show asahina smug
    show sam neut
    mc "Okay, hold on. Since when do {i}you{/i} use that shortcut?"
    ah "Since forever."
    mc "You absolutely did not know that last month."
    sa "We practiced."
    mc "...'We?'"
    show asahina unamused
    ah "Yes, we. We're not NPCs. We don't derender when you leave the room."
    mc "Pffft, that sounds fake as hell."
    show sam casual smug
    sa "It's true. I looked it up, and there's a whole page with citations."
    "They exchange a glance, barely a second long. A whole joke crosses the table inside it."
    "I knew all her shortcuts last month. Now I'm watching for one while the two of them laugh at something I missed."
    "My character drives straight past the turn."
    show asahina curious
    ah "You good?"
    mc "Yeah."
    mc "...Just calculating how hard I'm getting reamed."
    ah smug "Preeeetty firetruckin' hard."
    show sam casual happy
    sa "Nah, I think you're fine. You've taken two of the last five, which beats my first night."
    show asahina teasing
    ah "You drove into a wall, dude."
    mc "The council has spoken. Thank you both."
    "The third-party controller drops another phantom input. Sam watches it happen, then holds out his own."
    sa casual teasing "Take mine. If you lose with a working controller, at least it can be personal."
    "I take it and lo and behold, the next input lands."
    "My phone buzzes against my leg. Probably Matsuda, sending another progress report from whatever digital battlefield she has thrown herself into."
    "I choose to leave it alone for once and try to enjoy the company that I currently have."
    "The round ends with Asahina winning by a margin that feels medically suspicious."
    show asahina teasing
    ah "YES! Third win! Let's goooooo, I'm just better!"
    mc "...This household needs stricter humility laws."
    show sam casual smug
    sa "I'd vote for that. Somebody in this house should lose gracefully."
    show asahina shocked
    ah "Traitor!"
    show sam casual teasing
    sa "Hey, I said I'd {i}vote{/i}. I didn't say which way."
    "Asahina points at him while she tries to decide whether that counts as betrayal."
    show sam casual happy
    "He starts the next round before she can decide, and she grabs her controller with both hands."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The night goes through more rounds than anyone is counting."
    nier "Then the doorbell rings. Asahina pauses mid-turn and sends me to get the pizza."
    call nier_clear from _call_nier_clear_0520_6
    pause 2.0
    scene bg living_room_night
    $ show_calendar()
    $ atmos("home_night")
    show asahina happy at t21
    show sam casual neut at t22
    with wipeleft_scene
    "The pizza takes the coffee table hostage. The controllers go on the floor, where they will be inevitably stepped on later."
    "Asahina opens the box and holds the lid up like she is presenting evidence."
    ah "Behold!"
    mc "It's... it's pizza."
    show asahina at h21
    ah "Specially ordered on Mom's card, with permission of course. So behold harder!"
    "She takes a slice and folds it in half. Sam, on the other hand, takes two and folds nothing."
    show sam casual happy
    sa "Okay, trust me, I'm not going to make it a thing."
    show asahina teasing
    ah "I don't need permission from a guy who eats what looks like crust-first."
    sa "Crust-first is a strategy. The end of the slice is the worst part, so you handle it early."
    mc "...That's annoyingly reason--"
    show asahina annoyed
    ah "Don't take his side! You have NEVER taken mine! Not once! I keep a list!"
    mc "I like to think I'm more on the floor than on either side of this."
    sa thinking "But I mean, {i}technically{/i} that's a side. Just not a SIDE side."
    "My phone lights up against the couch leg. Mom, from the office: the case is still eating her evening, and did the food arrive."
    "I tell her it arrived and that nobody has broken anything yet."
    "{i}Yet is doing a lot of work in that sentence.{/i}"
    show asahina neut
    # NUDGE KEEP: the pizza beat, whole, through "In a minute." It's the food thread's best escalation so far.
    "Asahina is still on her first slice. Two bites out of the wide end, and the rest of it is being used to conduct an argument about kart racers."
    "Sam eats and lets her keep the floor. Every so often he puts a question in to keep it moving."
    show sam casual curious
    sa "So what's the actual rule? You said there was a rule."
    ah "The rule is simple. First place on the last lap. You deserve whatever happens."
    sa shocked "That's not a rule! That's a threat with a scoreboard!"
    show asahina smug
    ah "It's both, and that's exactly why it works."
    "She laughs at her own line and sets the slice down on a napkin. It stays there until the end of time."
    "There are still several slices in the box when Sam reaches for a napkin."
    show sam casual neut
    sa "There's plenty left, if anybody wants seconds or thirds."
    "He says it to the room."
    show asahina teasing
    ah "I'm not--in a minute."
    "I take another slice and burn the roof of my mouth on the cheese."
    show asahina happy
    ah "Okay. Rematch, and the loser clears the table."
    mc "That's you assigning me a chore in advance."
    show sam casual teasing
    sa "It's a good system. I'd use it."
    mc "...You two are a menace."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg home_entry_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    "Sam checks his bus time and starts looking for his bag."
    show asahina teasing at t21
    show sam casual pose_phone at t22
    "Asahina walks him to the door. The distance does not justify the ceremony."
    show sam casual neut
    "They stand by the door after it has already opened."
    "Normal, if you are mostly through puberty and allergic to efficient goodbyes."
    sa "Thanks for tonight. And for not blaming every loss on my controller."
    ah "He means thanks for helping him lose. Twice. Once by a lot."
    mc "I won a few; I just think you're both remembering selectively."
    show sam casual happy
    sa "Either way, I had fun. Come down next time without needing a reason."
    "He looks at me over Asahina's shoulder, waiting while I wind the controller cable."
    mc "Yeah. That was fun."
    "I leave the controllers beside the console, with the decent one on top for next time."
    show sam casual happy
    sa "Sounds good. See you around, [player]."
    mc "Later."
    show sam at thide
    hide sam
    "He steps outside and holds the door for Asahina."
    show asahina at thide
    hide asahina
    "Asahina follows him out, pulling the door shut behind her."
    play sound moddoorclose
    "I turn away before she can accuse me of spying, because for once I would like to be innocent on a technicality."
    show asahina neut at l11
    "When she comes back in, her face is aggressively neutral."
    mc "Fun night?"
    ah "It was fine."
    mc "That's your it-was-fun voice."
    ah "Shut your mouth up!"
    "I am four steps up the stairs by the time she recovers."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    "Upstairs, the homework is still open where I left it, though the phone beside it now shows several unread messages."
    "I check Matsuda's thread first because curiosity has survived all attempts at discipline."
    python:
        _phone_messages = [
            phone_msg("them", "Update the first: tutorial complete. Combat has hands."),
            phone_msg("them", "Update the second: this menu design is so ass lmao"),
            phone_msg("them", "Update the third: okay, it's preeeeeeetty good. You win this round."),
            phone_msg("me", "Historically bad, remember?"),
            phone_msg("them", "Yeah, for my sleep schedule."),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, append=True) from _call_phone_text_conversation_0520_3
    "I put the phone down beside the notebook and work through the first problem. Downstairs, Asahina laughs at something I can't hear."
    play sound moddooropen
    "I hear the front door latch from upstairs, which I'm assuming is someone finally getting home after a long day at work."
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0520_1
    jump a0521
