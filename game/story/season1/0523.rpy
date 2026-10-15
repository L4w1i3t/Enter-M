label a0523:
    # --- Day 9: 2025-05-23 ---
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music house_day_a
    "This morning, the alarms and I come to terms. It only takes {i}STILL WAKE UP{/i} to close the deal."
    "I'd tell Monika, except she'd take a victory lap around the entire school."
    "The only casualty of the morning is Asahina's toast, which came out of the toaster the color of a barbecue accident."
    "{i}Sucks to be you~{/i}"
    show mom uniform neut at t22
    show asahina uniform annoyed at t21
    "Across from me, my sister has one knee hooked up on her chair and is scraping the blackest bits onto her plate with a butter knife, like that's going to save it."
    "Mom's dressed for work and still sitting down, with a case folder propped on one knee. On a weekday, that's practically a state occasion."
    mom thinking "Track again today, right?"
    mc "Yeah, assuming the foot cooperates. Coach is also threatening me with a resistance parachute once I'm properly back, so that's something to look forward to."
    show asahina uniform teasing
    ah "Oh my God, someone {i}has{/i} to film that. I'm making it my lock screen."
    mom unamused "Let him survive a full week first. Your toast is getting cold."
    show asahina uniform neut
    "Asahina snaps off the blackened crust and goes back to eating."
    "For a while, breakfast is just cutlery and the kettle working itself up. Apple juice after jam turns out to be a mistake, so I switch to water."
    show mom uniform neut
    mom "Oh, [player], before I forget..."
    "{i}And there goes the quiet breakfast.{/i}"
    "She pins her place in the folder with one thumb."
    mc "...Should I be worried?"
    show mom uniform teasing
    mom "Not unless there's something you'd like to tell me."
    mom "That university. We did say {i}this week{/i}, and I'd point out, purely for the record, that it's Friday."
    mom "I'm home tonight, so after dinner we could sit down and look at it together. Half an hour, if there's anything left of you after practice."
    show mom uniform determined
    "She looks at me over her glasses while I turn the handle of my cup away from her."
    mc "...Tonight?"
    mom "Tonight. The program page, then admissions, then what it would actually take to get you there."
    show mom uniform neut
    mom "Nobody's deciding your whole life in one evening, rest assured."
    show asahina uniform neut
    ah "That'd be kinda efficient, though."
    "Her voice is softer than the words."
    show mom uniform thinking
    "Mom's eyes flick to her, then back to me."
    mom "We'll need longer than that to find his passport."
    mc "...Yeah, okay. It's not like I have plans."
    show mom uniform smug
    mom "Good. Bring your laptop down after you've showered, so we're not fighting over one screen."
    mc "Whoopty doo."
    show asahina uniform smug
    "Asahina makes the tiny nose-sound reserved for laughs she decides not to spend energy on."
    # SFX SUGGESTION: A kettle switch clicking off as the boiling sound fades.
    "Mom closes her folder and stands, and just like that the future gets put into a work bag for later."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Mom calls goodbye from the front door while Asahina digs through her bag to make sure her lunch made it in. Before I follow them out, I check that my socks match."
    call nier_clear from _call_nier_clear_0523_1
    stop music fadeout 1.0
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    with dissolve_scene_full
    play music quiz
    "In class, somebody asks whether Monday's exam covers the first unit. The teacher says yes, so I flip back to April and discover that I used to write legibly."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "By lunch, the useful notes share a page with three attempts to draw a character from my game. None of them have convincing legs."
    call nier_clear from _call_nier_clear_0523_1_5
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    stop music fadeout 1.0
    with wipeleft_scene
    play music school_day_a
    "Asahina finds me while I'm still deciding where to eat."
    show asahina uniform neut at t11
    ah "Roof?"
    mc "...No greeting?"
    show asahina uniform unamused
    ah "Hi. Roof?"
    "She says it like the correction cost her actual money."
    mc "Sure."
    "We ride the lunch rush as far as the stairwell, then peel off and leave the rest of it to the cafeteria."
    "She walks a step ahead with her phone out, and when she slows down to answer something, I slide her lunch bag off her wrist so she can text two-handed. She doesn't ask for it back."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg rooftop
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play sound moddooropen
    # SFX SUGGESTION: The rooftop door's metal latch and hinge, followed by a light gust of wind.
    "The door opens onto sun and a light breeze, and Tsubaki is already up here, sitting against the same shaded wall as on Wednesday."
    "Her lunchbox is open in her lap, with one hand parked on a yellow notebook so the wind can't flip the cover."
    show tsubaki uniform happy at t22
    show asahina uniform curious at t21
    "She starts to wave when she sees us, then shifts her lunchbox off the space beside her instead."
    show tsubaki uniform nervous
    ts "Oh, uh... what's up?"
    ah "Hey, you beat us!"
    mc "We got stuck behind half the first-years on the stairs."
    show tsubaki uniform neut
    ts "I came straight up after biology."
    mc "On purpose, huh?"
    show tsubaki uniform nervous
    ts "Well--you said I could sit up here. And Wednesday was nice."
    show tsubaki uniform embarrassed
    ts "I was kind of hoping you'd come back, actually. Is that weird?"
    show tsubaki uniform sad
    "She wraps both hands around her lunchbox and looks down into it."
    show asahina uniform unamused
    ah "No! We're here, aren't we?"
    mc "Asa picked the roof. I didn't even get a vote."
    ah "Because you take forever. You'd still be choosing a hallway."
    show tsubaki uniform worried
    ts "Oh, good. I was about to go down and look for you."
    show asahina uniform happy
    ah "Yep. Now scoot, you're hogging the good shade."
    show tsubaki uniform happy
    "Tsubaki is scooting before Asahina gets to the end of the sentence."
    "The wind picks at the corner of Asahina's napkin until she pins it under her drink."
    "Tsubaki eats neatly. Asahina eats like an office worker with thirty seconds left on her break."
    show tsubaki uniform curious
    ts "How was practice on Wednesday? It's plantar fasciitis, right?"
    show tsubaki uniform disgusted
    ts "Ugh, that one's the worst. I wouldn't wish it on anyone."
    mc "It's healing, more or less."
    show asahina uniform annoyed
    ah "He ran for the bus yesterday! Tell her that part."
    mc "And then I walked, like a responsible adult. It's fine today."
    mc "...Wait, hold on. Who told you I was injured?"
    show tsubaki uniform neut
    ts "Charlie."
    mc "...And who the hell is Charlie?"
    show tsubaki uniform curious
    ts "My friend? I thought you were both distance. No?"
    mc "Maybe? A bunch of people joined while I was out, and I'm still working through the roster."
    ts "So, um. What events do you run?"
    mc "Sixteen hundred and up. The longer the better, once I'm done regretting the first lap."
    show asahina uniform smug
    ah "Yeah, that tracks. Pun {i}very{/i} intended."
    show tsubaki uniform embarrassed
    ts "Oh, I could never. One lap in gym is plenty for me. I get bored before I get tired."
    mc "I used to count the windows on the second lap. Then somebody would pass me, and I'd lose my place."
    show tsubaki uniform neut
    "Tsubaki's gaze drifts through the fence to the rows of classroom windows below."
    show asahina uniform happy
    ah "Oh, by the way, you were right about the poster."
    show tsubaki uniform curious
    ts "Yeah?"
    show asahina uniform embarrassed
    ah "Somebody asked if I'd do the next one too. I said {i}maybe{/i}."
    show tsubaki uniform happy
    ts "So... are you going to?"
    "Asahina nods into her napkin and takes another bite."
    show tsubaki uniform neut
    ts "You two don't mind sitting here without talking."
    "She holds a bite over her lunch until the rice starts sliding loose, then lowers her chopsticks."
    show tsubaki uniform nervous
    mc "We've been talking since we got here."
    show asahina uniform teasing
    ah "Badly? Goodly?"
    show tsubaki uniform happy
    "Tsubaki smiles, but it arrives a little late."
    show tsubaki uniform thinking
    ts "I mean when you stop. Nobody has to start again straight away."
    "When the wind lifts the notebook cover, she presses it flat and leaves her hand there."
    show tsubaki uniform sad
    ts "It's nice. That's all."
    show asahina uniform neut
    "It still makes Asahina put her drink down."
    ah "I'm eating. He gets me for the rest of the day."
    mc "Speak for yourself. My silence is extremely sophisticated."
    "Asahina's eyes make the trip to me and back to Tsubaki."
    show asahina uniform happy
    ah "You can be quiet up here too, if you want."
    show tsubaki uniform happy
    ts "I can probably manage that."
    "Asahina nudges an unopened juice box toward her."
    ah "You want this? I hate the peach one."
    show tsubaki uniform curious
    ts "Oh... sure. Thanks."
    mc "You hate peach now?"
    show asahina uniform unamused
    ah "I've got water. Eat your rice."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg rooftop
    show asahina uniform neut at t21
    show tsubaki uniform neut at t22
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    "Lunch settles into the quiet Tsubaki was talking about."
    ts "Does the vending machine downstairs still eat coins?"
    ah "Only the one by the gym. Use the music-room machine."
    show asahina uniform annoyed
    "Tsubaki sips the peach juice. When the wind snatches a napkin and plasters it to the fence, Asahina goes after it, swearing at the sky."
    stop music fadeout 1.0
    play sound moddooropen
    show asahina uniform shocked
    show tsubaki uniform shocked
    "Then the rooftop door bangs open, and all three of us jump."
    ah "Jesus!"
    show asahina uniform shocked at t31
    show tsubaki uniform shocked at t32
    show matsuda uniform happy at t33
    "Matsuda plants one foot past the threshold and lifts a folded sheet of paper between two gloved fingers, her other hand spread beside her face to frame one eye."
    "The wind catches her ponytail right on cue. I can't prove she arranged that, but I wouldn't rule it out."
    play music theme_matsuda_a
    show matsuda determined
    # This encounter is deliberately a chuuni-hero performance. The natural
    # conversation belongs around the act; it must not replace the act itself.
    ma "Rejoice, Kareda! The curse of the Crimson Deadline is BROKEN!"
    ma "Alone, I breached the faculty fortress and stood before the Keeper of Deadlines himself--well, alone except for the guy refilling the copier, but he doesn't count--and where he would have sealed your fate, I have torn open a path... to MONDAY!"
    "Three stares meet her."
    show tsubaki uniform unamused
    "Tsubaki lowers the juice box and looks straight past the hand to the paper."
    ts "You got the extension signed?"
    show matsuda unamused
    ma "{i}Signed?{/i} This is the mark of his surrender!"
    "She turns the page around so we can see the signature, pinning the corner that wants to flap with her thumb."
    show asahina uniform curious
    ah "...What extension form?"
    show tsubaki uniform embarrassed
    ts "I left my assignment in the wrong notebook and didn't notice until everyone handed theirs in."
    ts "So Matsuda offered to take my extension request to the faculty office. I asked for Monday."
    show matsuda smug
    ma "And Monday it shall be! Guard this seal well, for even I cannot tear the same hole in fate twice."
    mc "Was there a line?"
    show matsuda determined
    ma "A trial of endurance! The clock devoured my lunch break, yet I refused to yield. Such is the price of forbidden power!"
    show tsubaki uniform worried
    "She brings the form down toward Tsubaki in a long, ceremonial arc. Tsubaki takes it by both edges halfway through."
    show tsubaki uniform happy
    ts "Thank you."
    show matsuda happy
    ma "No ally of mine shall perish beneath a pile of unsigned forms!"
    show matsuda determined
    # WEIRD ROUTE INSERTION 1 -- THE FIRST "RELIEF".
    # Both branches are sincere support; the split is collaboration versus
    # substitution. The substitution branch is deliberately the better scene --
    # faster relief, warmer payoff, an actual laugh -- because a blind player
    # has to finish it believing they found the most attentive way to care for
    # her. Nothing here is ominous and nothing foreshadows. The only tell is
    # physical and nobody in the scene remarks on it: in the substitution
    # branch the yellow notebook never opens, and she never writes anything
    # down in her own hand.
    #
    # THE GATE IS ALL-OR-NOTHING. This is box one of an unbroken chain: the
    # route requires the substitution branch at EVERY insertion, and the
    # collaborative branch here ends it permanently for this playthrough. That
    # is not a punishment for choosing it--it is what makes the far end of
    # the route addressable only to someone who chose substitution every single
    # time. See dependency_route.rpy for the full contract.
    show tsubaki uniform sad
    ts "I really need to stop doing this. That's the second time this month."
    mc "Do you forget where you put them, or forget to bring them?"
    show tsubaki uniform embarrassed
    ts "Both? Sometimes I put one down so I won't forget it, then walk right past it on the way out."
    show tsubaki uniform unamused
    ts "I'd need both hands to count all the extensions I've asked for this year."
    show asahina uniform teasing
    ah "Oh man, and I thought I was bad. I once turned in a grocery list."
    mc "I remember that. You took the homework to the grocery store instead."
    "Tsubaki slides the extension form into the yellow notebook edge first, without opening it."
    show tsubaki uniform neut
    ts "The work's done, too. That's the stupid part."
    show tsubaki uniform nervous
    ts "I filled the form out, then stood outside the office trying to figure out how to say I'd done it again. I was still standing there when Matsuda came past."
    show asahina uniform unamused
    ah "Ugh, I hate that door. You knock and nobody answers, but you're still supposed to go in."
    show tsubaki uniform happy
    ts "Exactly! I didn't want to walk in while someone was getting yelled at."
    "She laughs at herself once, and it comes out closer to an exhale."
    "Over by the fence, Matsuda has turned to face the skyline, one hand still raised beside her eye. Every time the wind shifts, she adjusts her stance to match."
    mc "Anyway, Tsubaki..."
    menu:
        "I can help you make a system.":
            # The non-dependency branch. He hands her a method, not a service.
            # The friction is the whole point: she does the writing, it's
            # slightly awkward, and it works about as well as a first draft
            # works. No reward beat -- this branch is simply ordinary.
            #
            # This ENDS the hidden route for the playthrough, permanently and
            # silently. Nothing acknowledges it, now or ever; from here the
            # story is just the story.
            $ dep_break("0523 rooftop -- helped her build her own system")
            mc "I could help you keep track of them, if you want."
            show tsubaki uniform curious
            ts "Meaning?"
            mc "A list, mostly. If I can't see it when I pack my bag, it doesn't exist. Then I don't have to remember the deadline {i}and{/i} where I left the paper."
            show asahina uniform smug
            ah "Oh no, he's doing the thing. Next he's gonna make you buy sticky notes."
            mc "She's already got a notebook."
            show tsubaki uniform annoyed
            "The yellow notebook receives a look of personal betrayal."
            ts "...It's for other stuff."
            mc "Could you use the back? Or would you rather keep it separate?"
            # pose_notebook is this branch's silent signature: the notebook leaves her
            # hands' safekeeping and opens. The substitution branch below never reaches
            # for it, which is the physical half of the tell described above.
            show tsubaki uniform nervous
            "She opens it from the back and turns past a sketch before settling on a blank page."
            mc "Three short lines for now: what it is, when it's due, and where you put it."
            show tsubaki uniform curious
            ts "Where I {i}put{/i} it?"
            mc "Half your problem's the paper, not the deadline. You always know the date. It's the paper that wanders off."
            show tsubaki uniform unamused
            ts "...Okay, that's annoyingly fair."
            show tsubaki uniform determined
            "She writes in small, careful strokes, stopping twice to fit the line into the margin."
            show asahina uniform neut
            ah "Put a Friday check on it."
            show tsubaki uniform curious
            ts "A what?"
            ah "Every Friday, you look at the list. That's literally the whole thing."
            ah "I do it for volleyball. It's not deep."
            show tsubaki uniform thinking
            ts "That feels too easy..."
            mc "Try it for a week. If it doesn't help, we'll try something else."
            "She adds the line, then reads all four back to herself with her lips barely moving."
            show tsubaki uniform embarrassed
            ts "This is going to look so stupid in a week when I forget to check it."
            mc "I forget to check mine sometimes. You just look at it when you remember."
            show tsubaki uniform neut
            "Tsubaki doesn't answer that, but she doesn't close the notebook, either."
            $ update_character_thought("tsubaki", "Tsubaki has four lines in the back of a yellow notebook now. We'll see if she looks at them.")
        "You can leave it to me.":
            # The hidden-route branch. Generous, and genuinely so -- it is also
            # a warm, bounded trial. The offer covers one board photo today;
            # it does not make him her standing assignment manager. The
            # notebook stays closed throughout this branch.
            $ dep_take("tsubaki_assignments", "one board-photo check by [player], end of day", day="0523")
            mc "For today, send me one photo of the board before you leave."
            show tsubaki uniform curious
            ts "...Just today?"
            mc "One trial. I'll check it for anything easy to miss and send back what I see. What you do with it after that is up to you."
            show tsubaki uniform shocked
            "Tsubaki blinks, then looks down at the notebook under her hand."
            ts "You'd actually do that?"
            mc "It's one photo. I read those recreationally."
            show asahina uniform teasing
            ah "...He does, and it's actual goblin behavior."
            # SFX SUGGESTION: something small and warm under this line -- the
            # jingle is scoring her relief, not the player's click.
            play sound weirdjingle
            show tsubaki uniform happy
            "Her shoulders drop before she catches them."
            ts "Okay. So, just the board, at the end of the day?"
            mc "{i}Tsubaki{/i}."
            show tsubaki uniform embarrassed
            ts "Right. One picture."
            show tsubaki uniform nervous
            ts "Wait, I don't have your number."
            mc "That would've been a strong obstacle."
            "Both phones come out for the trade. Tsubaki checks the last four digits once before she locks her screen."
            show tsubaki uniform happy
            "Her smile arrives before the next qualification does."
            show asahina uniform happy
            ah "Okay, that's a pretty good deal. Can I get one?"
            mc "Ask Mom. I can only take one at a time."
            show asahina uniform unamused
            ah "So it's favoritism, got it."
            mc "The trial offer has limited enrollment."
            "Tsubaki laughs while Asahina tries to wedge her own phone in between ours."
            ts "That'll make tonight so much easier. I can stop thinking about it until I send the picture."
            show asahina uniform teasing
            ah "Nice. He can worry about it for once."
            show tsubaki uniform happy
            ts "Thanks, [player]."
            "The yellow notebook stays under her hand."
            $ update_character_thought("tsubaki", "Tsubaki is sending me one photo of today's board before she leaves. I'll check the picture, and she handles whatever comes after.")

    show matsuda uniform pose_chuuni
    "Matsuda turns back and extends an open hand toward us, keeping the other one beside her face."
    ma "You may lower your guard, comrades! While the Azure Eye watches over this sanctuary, no darkness shall cross its threshold!"
    mc "...Azure Eye?"
    ma "The power sealed within me! I would reveal its true nature, but your minds must survive until fifth period."
    "{i}But your eyes are green...{/i}"
    "She looks at each of us in turn, both hands still up. Asahina starts to lift hers, then catches Tsubaki shaking her head."
    mc "Do we need to do the hand thing too?"
    show matsuda uniform smug
    ma "Not yet. Your bodies would shatter under the strain."
    show asahina uniform curious
    ah "Okay, no, I need to learn the hand thing. I'm doing it at practice."
    show tsubaki uniform unamused
    ts "She'll make you shout the name."
    show matsuda determined
    ma "Of COURSE! What is a forbidden technique without a name that strikes terror into the hearts of your enemies? Or, in your case, the other team."
    show matsuda happy
    "Then her attention swings back to me, and her smile holds too still."
    if s1_was("matsuda_stop", "blunt"):
        "Her raised hand sinks a couple of inches before she points at me with two fingers. When she speaks, it's a notch below her usual volume."
    elif s1_was("matsuda_stop", "gentle"):
        "She points at me with two fingers, then drops her voice to a mutter."
        ma "Thirty-five percent, as negotiated."
    else:
        "She points at me with two fingers and comes in at full volume, same as Monday's hallway ballad."
    ma "And you, [player]! The drowned station lies along your path. Have you dared cross its threshold?"
    mc "Not yet. Don't tell me what happens."
    ma "Then heed my warning! The boss has this move where--"
    "I hold up a hand, and she stops with her mouth still open."
    show matsuda uniform determined
    ma "...Where you must discover your own destiny. Yes. I shall speak no more of it."
    "I take another drink while she clamps her lips shut, like the spoiler might still make a break for it."
    show matsuda determined
    ma "My work here is complete! Soon the bell will restore the barrier, and I must resume my civilian disguise!"
    "She straightens the ribbon at her collar as though that will do it."
    show tsubaki uniform worried
    ts "Wait. Hold on. Did you eat?"
    show matsuda smug
    ma "One melon bread, consumed in transit. Its power still burns within me!"
    "{i}That's called heartburn.{/i}"
    show tsubaki uniform annoyed
    ts "That is NOT lunch! You said you'd get something after the form!"
    show matsuda annoyed
    ma "This vessel requires no earthly sustenance! I have transcended such petty--"
    show tsubaki uniform determined
    "Tsubaki digs a small wrapped rice cracker out of her lunch bag and holds it up. She doesn't say a word."
    show matsuda embarrassed
    "Both of Matsuda's hands come down. She takes the cracker carefully, cupping the loose wrapper so the wind can't have it."
    ma "...Thanks."
    show tsubaki uniform neut
    ts "Eat real food later. Please."
    show matsuda smug
    ma "You have my word. This vessel shall dine {i}magnificently{/i}!"
    show matsuda happy
    ma "Until our paths cross again! Should the heavens split before then, you will know who intervened!"
    mc "I'll check the forecast."
    show matsuda uniform happy
    ma "They will call it a weather anomaly. They always do."
    show matsuda at thide
    hide matsuda
    show asahina at t21
    show tsubaki at t22
    stop music fadeout 1.0
    play sound moddoorclose
    "She sweeps out through the door with the rice cracker cradled in one hand."
    "Her footsteps clatter away down the stairwell. None of us says anything until they're gone."
    show asahina uniform neut at t21
    show tsubaki uniform neut at t22
    play music day_a
    mc "Somehow I still don't know what the eye does."
    show tsubaki uniform smug
    ts "It's mostly a hand position."
    show asahina uniform curious
    "My sister points at the door, puzzled."
    # NUDGE KEEP: exactly as written. The first deniable tracking beat.
    ah "Wait, she knew you were up here? Did you tell her?"
    show tsubaki uniform thinking
    "Tsubaki presses her lips together."
    ts "I... don't know. Maybe she saw me come up? Or she asked someone."
    show tsubaki uniform nervous
    ts "Sometimes she just guesses right. Yesterday she sent me three messages from the wrong floor."
    mc "That clears up nothing."
    ts "I wasn't keeping track, okay? I don't know how she found me."
    mc "Does she do that a lot?"
    show tsubaki uniform worried
    ts "The guessing? ...Sometimes."
    show asahina uniform neut
    "Asahina lowers her drink and looks straight at me."
    ah "She {i}said{/i} she doesn't know."
    show tsubaki uniform teasing
    ts "Ask Matsuda. It'll take longer, but you'll get a better story."
    "Asahina's eyes haven't left me. I find something very important to do with the lid of my lunch."
    show asahina uniform pose_pointing
    ah "Next time she asks, tell her we stole you. I want to hear the rescue speech."
    # SFX SUGGESTION: A thin warning bell carrying up from inside the school.
    "The warning bell rings below us, thin and distant."
    mc "We should go before the staircase fills up."
    show asahina uniform unamused
    ah "That was painfully practical..."
    show tsubaki uniform teasing
    ts "Ask the Azure Eye to hold the bell."
    mc "Oh my lord..."
    show asahina uniform happy
    "Tsubaki lifts a hand beside her eye, then drops it when Asahina laughs. She's smiling as we head for the door."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The afternoon drags itself through two more lessons. By the time I'm changed for practice, Wednesday's session is down to a dull ache in my hips, and the foot hasn't said a word all day."
    call nier_clear from _call_nier_clear_0523_2
    stop music fadeout 1.0
    pause 2.0
    scene bg track_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music day_c
    "The distance group is roughhousing on the infield, putting off being miserable on purpose for as long as Coach lets them."
    "{i}My people, unfortunately.{/i}"
    show track_coach neut at t11
    track_coach "How's it going, [player]?"
    "He doesn't shout it this time. He just inspects me from the shoes up, like he's checking whether I arrived fully assembled."
    track_coach "Foot?"
    mc "Quiet."
    track_coach "Twenty minutes easy on the outside, then four strides if all's good. Like the other day, I want rhythm, not proof."
    mc "Twenty easy, then four strides."
    track_coach "I know {i}you{/i} heard me. I just want your legs to hear it."
    show track_coach at thide
    hide track_coach
    "I join the outside lane and let the first hundred meters be ugly. My foot stays quiet. My lungs take a full lap to agree."
    "Two laps in, I can't stop checking who's ahead of me, and by how much."
    "By lap three, my shoulders are up around my ears and my left foot is reaching way out in front."
    show track_coach neut at t11
    track_coach "Arms!"
    track_coach "Shorter step! You're reaching!"
    "It helps immediately. Good advice is annoying that way."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I work on landing under my hips. When somebody passes me on the bend, I let him go."
    call nier_clear from _call_nier_clear_0523_3
    pause 2.0
    scene bg track_evening
    $ show_calendar()
    $ atmos("evening")
    with wipeleft_scene
    "By the cooldown, the light is tilting toward evening. The foot's quiet, but my lower back is still billing me for Wednesday."
    show track_coach neut at t11
    track_coach "Your shoulders creep when you get impatient, and you overstride when you think about pace instead of feel."
    mc "So... it's mental again, right?"
    track_coach "Your brain is useful when it stays in its lane. Same as your feet."
    "One of the distance guys coughs 'nerd' into his fist over by the cooler. I'm filing that under allergies, not betrayal."
    track_coach "Stretch, hydrate, and get out of here. Do not turn tonight or tomorrow night into extra training because you feel behind."
    mc "The invitational's in three weeks, though. If I want both races--"
    track_coach "I'd rather have you slow in June than gone in July."
    mc "...Got it."
    track_coach "Good. Once exams are done, we reassess."
    track_coach "Academic stress makes athletes stupid in creative ways, and I would like you to avoid contributing to the data."
    mc "I'll do my best to protect the sample."
    track_coach "Keep to the reduced weekend plan. If the foot hurts, stop and tell me."
    show track_coach at thide
    hide track_coach
    "Then he's off to bother the sprinters, and I stretch until my hamstrings quit complaining."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "On the way out, I swing past the club room. Lights off, no bags."
    nier "I pick up a newspaper for Mom on the walk home. She likes to spread it across the whole table, including whatever part of it I happen to be using."
    call nier_clear from _call_nier_clear_0523_4
    stop music fadeout 1.0
    pause 2.0
    scene bg kitchen_evening
    $ show_calendar()
    $ atmos("evening")
    with wipeleft_scene
    play music house_day_a
    "Home smells like clean laundry and a dinner that already happened without me."
    "A covered plate waits for me on the counter, labeled twice: once with my name, and once with instructions."
    call enter_m_show_sticky_note(("Eat first.", "Shower second.", "Laptop third."), signature="Mom") from _call_enter_m_show_sticky_note_0523_1
    "The order is too specific to argue with."
    "The first two bites happen standing at the counter. Then I remember I'm technically civilized and carry the plate to the table."
    if dep_took("tsubaki_assignments"):
        "Tsubaki's photo has been waiting since practice: the board, as promised, tilted a little to the left."
        "The chemistry correction deadline is crammed into the bottom corner, under the lab schedule."
        "I send back the date and nothing else. Her reply comes a few seconds later."
        "{i}Got it, thank you.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I shower until practice stops living on my skin."
    nier "While my hair dries, I sit on the bed with the laptop and close the walkthrough I left open last night. Underneath it, the university link is still waiting in my history."
    call nier_clear from _call_nier_clear_0523_5
    stop music fadeout 1.0
    pause 2.0
    scene bg living_room_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music night_b
    "Mom's in the living room when I come down, and the coffee table has been cleared of everything except a black leather notebook and two pens."
    "Asahina is nowhere in sight. Her closed door upstairs probably means homework has blurred into texting Sam again."
    show mom neut at t11
    mom "Look who survived."
    mc "Foot's fine. Coach says my mechanics are rusty, but what else is new?"
    mom "One day at a time, though, right?"
    mc "Yeah, pretty much. That's all I {i}can{/i} do."
    "I sit and set my laptop on the coffee table. Neither of us scrambles to open it."
    show mom neut
    mom "Before we open that, ground rules."
    mc "Okay..."
    mom "We're looking at an option, not handing down a verdict on the rest of your life."
    mom "We write down questions and close the laptop before the numbers psych us out."
    mc "Numbers always have their way..."
    mom "That's why this is just recon."
    "I open the laptop."
    "The blank search bar waits with more confidence than either of us."
    mc "When I said I wanted to see the world, I wasn't picturing application forms. It was more of an... eventually thing."
    mc "Now you've actually found a place, and I'm supposed to know if that's what I meant."
    show mom teasing
    mom "You don't have to like this one just because I found it."
    show mom determined
    "She writes the date at the top of the notebook, then underlines it once."
    mom "You're graduating in less than a year, and applications won't wait until you feel ready."
    mom "Deadlines don't care whether the house has had a long week."
    show mom unamused
    mom "And believe me, after this week, I wish they did--"
    "She exhales through her nose."
    show mom neut
    mom "But they don't."
    mc "Mhm..."
    "The laptop fan starts its tiny unnecessary whisper."
    mc "I know I have to think about it."
    mc "...I just hate what it does to everything else."
    show mom curious
    mom "What part?"
    mc "If I go somewhere far away, I can't just come home because I've had a bad day."
    mc "But if I stay close, I'll wonder whether I was ever going to do it. I can make either choice sound bad."
    show mom determined
    mom "You could change your mind once you get there."
    mc "After we pay for it? That's a pretty expensive way to find out."
    show mom neut
    mom "It is. That's why I want us to look carefully, including at the cost of coming home."
    mom "I'm not expecting you to guarantee four perfect years. It isn't a life sentence."
    "That gets a dry little laugh out of me."
    mc "You were waiting to use that one."
    show mom smug
    mom "Lawyer Mom is {i}very{/i} careful with sentence length."
    "I turn back to the search bar. Encouraging her would be a mistake."
    show mom curious
    mom "Can I ask you something before we look?"
    mc "You've been asking me things for ten minutes."
    mom teasing "One more, then."
    mc "All right."
    show mom thinking
    mom "Really. When you imagine leaving, what comes first?"
    "I look at her."
    "The obvious answers line up. They're all true, and none of them is any use on its own."
    menu:
        "\"Relief.\"":
            $ s1_pick("himeko_first", "relief")
            mc "Relief."
            mc "...Which I feel bad about roughly one second later, so write that down too."
            show mom neut
            mom "Noted."
        "\"That I'd be bad at it.\"":
            $ s1_pick("himeko_first", "fear")
            mc "That I'd be bad at it."
            mc "Not the classes. Literally everything else."
            show mom neut
            mom "Most people do. The ones who don't worry me more."
        "\"Guilty.\"":
            $ s1_pick("himeko_first", "guilt")
            mc "Guilty."
            mom "About?"
            mc "...Ask me again in a minute. I kind of just blurted that out."
    mc "I want to find out what I'd do somewhere new, where nobody already knows me as the guy who's good at school."
    mc "I could try something and be bad at it without everyone asking what happened."
    show mom thinking
    "She lets that sit."
    mom curious "So you want somewhere nobody knows you."
    mc "Not nobody. Just nobody with a completed file on me."
    "Her pen stops above the notebook."
    mom "All right. That's different."
    mom neut "I think I understand that."
    mc "It sounds kinda selfish if you ask me."
    show mom neut
    mom "I don't think wanting that makes you selfish. You've spent more time worrying about leaving us than looking at the place."
    "I rub my palms against my knees."
    mc "What about Asa?"
    mom determined "...What about her?"
    mc "She still comes looking for me, even when it's only to complain about a controller or borrow stuff."
    mc "Lately I can't tell whether she wants help or wants me to shut up and sit there. I'm not sure how that works from somewhere else."
    mom "Trust me, Asahina will miss you when you leave."
    "I pick at a loose thread on the couch until it comes away in my fingers. I still don't have an answer."
    show mom sad
    mom "So will I."
    "She caps the pen. Then uncaps it and writes nothing."
    show mom determined
    mom "But that is {i}not{/i} a reason to stop building a future."
    mc "It's... it's just hard, Mom. Picking something to run toward, with no idea how it'll turn out..."
    mom "Who said you needed to run? Walk instead if you need to."
    "She taps the end of her pen against the notebook once."
    mom "If it makes you feel better, she asked about dorms earlier."
    mc "...Asa did? What's next, raining frogs?"
    show mom teasing
    mom "While pretending to look for the good charger, she asked whether dorms meant you would only come home on holidays."
    "My eyes go to the stairs. Her door's still shut up there."
    mc "What did you tell her?"
    mom "That we hadn't even opened the website yet."
    mc "I mean, we haven't, so..."
    "I look away."
    "From here I can see the scuff Asahina left when she tried to move the couch by herself. We still haven't covered it."
    mc "I could pick a school just because it's far away, then spend four years there. That seems like a pretty stupid way to choose."
    show mom neut
    mom "Then we'd better find out whether you actually like it. You've had plenty to say about the distance."
    mom "And after we look, you may decide this school isn't worth moving for."
    mc "I like the part where I can reject it."
    mom "That's why we gather information before panicking."
    mc "...Okay. Let's look. But if I hate it, I'm saying so."
    mom "After you, then."
    "She slides last week's printout over. The last of her three handwritten bullet points has a question mark beside it."
    "{i}Merit scholarship? Ask counselor.{/i}"
    "The site loads a wall of clean photos, full of students arranged so carefully they stop looking like students."
    show mom teasing
    mom "Ah, ah... Admissions first."
    "Entrance requirements: met. Application windows: comfortably far off. The personal statement is listed as {i}optional{/i}, and Mom writes that one down with suspicious care."
    mc "Optional in the way teachers say participation is optional?"
    show mom determined
    mom "It says they consider it alongside your grades. You have time to write one, and I can read a draft if you want."
    "The program page is worse, because it's actually interesting."
    "{i}Ooh, game design as an elective? Huh. Wonder how hard that is to get into.{/i}"
    "The student projects come with screenshots and real names, and the page stops feeling like an ad."
    show mom smug
    mom "Something catch your eye? You leaned in."
    mc "No I didn't."
    mom "Oh yes you did."
    mc "I had to. The font got smaller."
    show mom unamused
    mom "..."
    mc "...This part looks good."
    mom "Yes."
    mc "And expensive."
    mom "Also yes."
    show mom neut
    mom "That's why we look at scholarships, aid, commuting, housing, and backups."
    mom "An option isn't a commitment, the same way a rough draft isn't a final one."
    mc "Didn't you write one of your own essays the night before?"
    mom "I did, and I hated every minute. You don't have to copy that part."
    "She sorts firm dates from counselor questions, then hands me the pen to add one about the student projects."
    mc "Thanks for doing this with me. I wouldn't have gotten past the first page."
    show mom happy
    mom "You're choosing the next one. I refuse to do all the browsing."
    "She turns the notebook so the next blank line faces me."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg living_room_night
    $ show_calendar()
    $ atmos("home_night")
    show mom neut at t11
    with wipeleft_scene
    mom "All right, that's enough notes for one night."
    mom "I know you're juggling a lot. I just wanted that door open sooner rather than later. Midterms come first."
    mc "It's open. Believe me."
    "She reaches over and squeezes my shoulder once."
    mom "Now go rest before you start trying to solve your entire life in one sitting."
    mc "One sitting is efficient."
    mom teasing "One sitting is how bad essays are born."
    mc "...Fair."
    mom worried "Save the links. Then sleep at a normal hour, please. I know how you get when something's weighing on you."
    mc "Yes, counselor."
    show mom at thide
    hide mom
    "After she's gone, I copy the project-page link into the folder with the admissions notes. Then I close the laptop, as instructed."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "On my way up, Asahina laughs once behind her door, too muffled to make out, while Mom rinses her mug in the kitchen below."
    call nier_clear from _call_nier_clear_0523_6
    pause 1.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    "The student projects are still running laps in my head when my phone starts buzzing against the desk."
    "Matsuda Akai."
    "{i}Of course...{/i}"
    python:
        _phone_messages = [
            phone_msg("them", "Rooftop report: Kareda has returned to class with the official paper intact. Mission success!"),
            phone_msg("them", "You and that other peon appear to have accepted her into the lunch territory faster than projected."),
            phone_msg("them", "This is useful intel. Our emerging circle may be viable after all."),
            phone_msg("them", "Sunday field exercise: bookstore, maybe a shrine, then somewhere to study. I've already told Kareda you'll show us around. Bring the other weird girl too, if she's willing."),
            # NUDGE DECIDE 10.9: is the Portrait of Zahrath a deliberate setup? Fine as flavor either way; just decide.
            phone_msg("them", "There is also a shop that might have the old tale of the Portrait of Zahrath, which my Azure Eye HUNGERS for."),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, append=True) from _call_phone_text_conversation_0523_1
    "I read them twice. They don't get any better."
    "{i}Can you, like, not...?{/i}"
    menu:
        "(Flat. No cushioning.)":
            $ s1_pick("matsuda_callout", "flat")
        "(Say it kindly. Say it anyway.)":
            $ s1_pick("matsuda_callout", "kind")
        "(Keep it light. Keep it firm.)":
            $ s1_pick("matsuda_callout", "sharp")
    python:
        _stance = s1_stance("matsuda_callout", "flat")
        if _stance == "kind":
            _phone_messages = [
                phone_msg("me", "Hey. I'm glad you want to hang out, I mean that. But you skipped the part where you ask me."),
                phone_msg("me", "We met six days ago."),
                phone_msg("me", "You don't get to plan my weekend, or call people an emerging circle like it's already a thing."),
                phone_msg("me", "Midterms already own most of my weekend, and whatever's left is mine to plan."),
                phone_msg("me", "Please tell Tsubaki I never agreed to it."),
                phone_msg("me", "And my sister's name is Asahina. She isn't a peon."),
            ]
        elif _stance == "sharp":
            _phone_messages = [
                phone_msg("me", "Counterproposal: you retract that entire message, and we all pretend the word 'peon' never happened."),
                phone_msg("me", "We met six days ago."),
                phone_msg("me", "You don't get to plan my weekend or call people an emerging circle like it's already a thing."),
                phone_msg("me", "Midterms already own most of my weekend, and whatever's left is mine to plan."),
                phone_msg("me", "ASK me before you tell people I'm coming. That's the important part."),
                phone_msg("me", "And my sister's name is Asahina. Use it."),
            ]
        else:
            _phone_messages = [
                phone_msg("me", "Matsuda."),
                phone_msg("them", "That reads like a gavel..."),
                phone_msg("me", "We met six days ago."),
                phone_msg("me", "You don't get to plan my weekend or call people an emerging circle like it's already a thing."),
                phone_msg("me", "Midterms already own most of my weekend, and whatever's left is mine to plan."),
                phone_msg("me", "If you want to hang out, ASK before you tell people I'm coming."),
                phone_msg("me", "And my sister, whose name is Asahina, isn't a peon. Get it straight."),
            ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, append=True) from _call_phone_text_conversation_0523_1b
    # SFX SUGGESTION: An uneven air-conditioner rattle with a trash bin scraping past outside.
    "No reply. The air conditioner keeps up its uneven little rattle, and somewhere outside, someone drags a trash bin across concrete."
    "My thumb circles the edge of the phone while I wait."
    "{i}Too harsh?{/i}"
    "{i}I didn't agree to Sunday. That's the part that matters.{/i}"
    "The typing indicator appears, disappears, and appears again."
    python:
        _phone_messages = [
            phone_msg("them", "Understood."),
            phone_msg("them", "I overstepped."),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, append=True) from _call_phone_text_conversation_0523_2
    "I wait for the next bubble. With her, there's always a next bubble."
    "The typing indicator doesn't come back."
    "I turn the phone face down on the desk. A minute later I've picked it back up, rereading two messages that haven't changed."
    "One knock touches the open door. Asahina reaches in and drops the good charger beside my phone."
    ah "Found it."
    mc "That was in your room."
    ah "And now it isn't."
    "Then she's back across the hall with her door shut."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Before bed, I check Monday's exam schedule one more time and open my alarms. Asahina's three are all still on. I add a fourth."
    call nier_clear from _call_nier_clear_0523_7
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0523_1
    jump a0524
