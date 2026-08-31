label a0525:
    # --- Day 11: 2025-05-25 ---
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music dailyleisure
    "I beat the first alarm by one minute, which is completely unheard of for me. Not fifteen minutes after it or from inside another dream where a coffee mug accuses me: one minute before."
    "The screen reads 7:14. The other three alarms sit beneath it like backup prosecutors, and I disable all of them."
    "For a few seconds, I stay under the blanket and listen."
    # SFX SUGGESTION: Sparse house ambience: a pipe tick, low refrigerator hum, and one car passing outside.
    "A pipe ticks while the refrigerator hums downstairs. One car passes outside with no interest in the world."
    "My bag is already packed beside the desk, though I don't remember prepping it."
    "{i}I really have to go out today, huh? Kinda did it to myself.{/i}"
    "The thought does something annoying to my chest that makes me sit up."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg kitchen
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    "A note is stuck to the counter beside a covered plate in the kitchen."
    call enter_m_show_sticky_note(("Breakfast.", "Text when you arrive.", "Do not live on pastries."), signature="Mom") from _call_enter_m_show_sticky_note_0525_1
    "My phone buzzes and lights up before I can start digging into my food."
    python:
        _phone_messages = [
            phone_msg("them", "Morning. Are you awake?"),
            phone_msg("me", "Before the alarm, somehow."),
            phone_msg("them", "That's either impressive or concerning."),
            phone_msg("me", "Both can be true."),
            phone_msg("them", "I'm leaving in a few minutes. I brought flashcards and a terrifying amount of sticky notes."),
            phone_msg("me", "Define terrifying."),
            phone_msg("them", "You'll know it when you see it."),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0525_1
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Breakfast is quieter without Asahina needling me from across the table or Mom silently grading my choices."
    nier "I finish early and sit with the calm for a few minutes. Then I'm out the door."
    nier "The trip downtown is too ordinary to complain about. The bus is half-empty, and the morning streets are washed in clean light."
    nier "A kid across the aisle kicks his shoes against the seat until his mother gives him a glare. He stops immediately."
    nier "I text Mom when I reach the library steps, because she asked and because forgetting would create its own problem."
    call nier_clear from _call_nier_clear_0525_2
    stop music fadeout 1.0
    pause 2.0
    scene bg city_morning
    $ show_calendar()
    $ atmos_clear()
    with wipeleft_scene
    play music daily
    "The public library sits above the sidewalk, having watched generations of students panic under better lighting."
    "{i}Good morning, library.{/i}"
    "{i}Please be useful by noon...{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    scene bg library
    $ show_calendar()
    $ atmos_clear()
    with wipeleft_scene
    "The second floor smells like paper and carpet cleaner. Sunlight falls across the study tables in pale rectangles, and the textbooks look briefly innocent."
    "Monika is already at the table by the windows. Two chairs and a row of color-coded sticky notes make the meeting spot hard to mistake."
    show monika forward casual dist cm oe nobl rdown ldown at t11
    "{i}Of course she is already there, what else did I expect?{/i}"
    "Her hair ribbon is tied neatly, though her eyes look less so."
    m forward casual happ om oe nobl rdown ldown "Look who made it~"
    mc "I did promise, didn't I?"
    m forward casual wry cm oe nobl rhip ldown "You also promised to sleep at a reasonable time."
    mc "By my standards, I did. The exact hour is privileged information."
    "She gestures to the open chair beside her."
    m forward casual happ om ce nobl rhip lpoint "Just saying, the padding on these chairs is like heaven..."
    mc "Oh yeah?"
    "I take less than a second to test the allegedly heavenly chair."
    "My bag lands beside me with a small thud, like it already gave up the ghost."
    m forward casual happ cm ce nobl rdown ldown "I didn't make us a minute-by-minute schedule, before you ask."
    mc "Pretty sure that's a mercy."
    m forward casual happ om oe nobl rhip ldown "Topic rotation. Civics and language arts first, then science, then algebra, then English."
    m "Short blocks. Breaks when one of us starts sounding exhausted or grumpy."
    mc "Consider the sesh dead on arrival, then."
    m anno cm oe nobl rhip ldown "..."
    mc "...Was it something I said?"
    show monika forward casual neut cm oe nobl at t11
    "She squares her stack of sticky notes against the edge of the table, then opens the civics folder."
    "She can pass me a card without either of us standing."
    m om lpoint "Okay, Mr. Smartass, no idle chatting then. Warmup question, since you want to hit the ground running."
    mc "Wait, hold on--"
    "She holds up a notecard with presumably a question on it."
    m "When a court strikes down a law because it conflicts with the constitution, what principle is being applied?"
    mc "Judicial review."
    m forward casual curi om oe nobl rhip ldown "Definition?"
    mc "The judiciary reviews government action for constitutional compatibility."
    m forward casual happ cm oe nobl rhip ldown "Good. Now say it like you aren't submitting it to the committee."
    mc "...A court checks whether the government crossed a constitutional line."
    m forward casual happ om ce nobl rdown ldown "Heeeey, there he is!"
    "She lays the card faceup beside the folder. A green sticky note marked {i}JUDICIAL REVIEW{/i} waits above it."
    mc "Was the first answer somehow incorrect?"
    m forward casual wry cm oe nobl rhip ldown "It was correct like an instruction manual written by a robot."
    mc "Is it that much of a difference? Harsh."
    m forward casual happ om oe nobl rhip ldown "Useful, though. If you can put it in your own words, you probably know it."
    "Her fingers find the next card, but she doesn't turn it over."
    m forward casual curi om oe nobl rdown ldown "Okay, before we actually start...how's it going?"
    mc "The review or me?"
    m forward casual neut cm oe nobl rdown ldown "You. Who else would it be?"
    "The library carries on quietly around the question. A page turns two tables away while somebody rolls a pencil along a windowsill."
    mc "I'm awake and dressed. I even made it to the correct building."
    m forward casual wry cm ce nobl rdown ldown "You make it sound inspiring."
    mc "I like to set achievable benchmarks."
    m forward casual happ cm oe nobl rhip ldown "Seriously..."
    "She says it gently, so I let the joke go."
    mc "A little nervous, not falling-apart nervous. More like Monday's standing behind me, breathing through its mouth."
    m forward casual happ cm oe nobl rdown ldown "That's disgustingly vivid."
    mc "Thank you. How about you?"
    m forward casual nerv om oe awkw rdown ldown "I'm good."
    "Her eyes drift toward the row of sticky notes."
    mc "Did the manual write that one?"
    m forward casual nerv cm oe awkw rdown ldown "Excuse me?"
    mc "You called mine an instruction manual written by a robot."
    "A laugh escapes before she can defend herself. She hides it behind one hand."
    m forward casual happ cm ce nobl rdown ldown "Okay...I'm tired, then. A little nervous, too."
    mc "There, now I believe you."
    m forward casual wry om oe nobl rhip ldown "Don't get too proud. You're one question in."
    m forward casual curi om oe nobl rdown ldown "And your foot?"
    mc "It's been quiet since yesterday. The plan is not to give it a reason to start arguing."
    m forward casual happ cm oe nobl rdown ldown "Good. Let's keep it that way."
    "She finally turns over the next card, then stops again."
    m forward casual nerv om oe awkw rdown ldown "Actually...one rule for today."
    mc "Only one? Your system is slipping."
    m forward casual neut om oe nobl rhip ldown "If either of us doesn't understand something, we say so. No bluffing and hoping the other person moves on."
    "She keeps one finger on the face-down card and waits."
    mc "Even if the thing is embarrassing?"
    m forward casual happ cm oe nobl rdown ldown "Especially then."
    mc "Fine. We can be confused out loud together."
    m forward casual happ om ce nobl rdown ldown "That's the spirit~"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "We start with civics and language arts."
    nier "The warmup card turns into an argument over whether a city council can be described as a bad roommate, and sticky notes slowly spread across the table."
    call nier_clear from _call_nier_clear_0525_3
    pause 2.0
    scene bg library
    $ show_calendar()
    $ atmos_clear()
    show monika forward casual dist cm oe nobl rdown ldown at t11
    with wipeleft_scene
    "Monika draws three boxes across a sheet of scrap paper. The first holds a law rejected for violating the constitution."
    "National and local governments split authority in the next. In the last, the government tries to take somebody's property without warning."
    m forward casual happ om oe nobl rhip lpoint "No definitions this time. Sort the situations."
    mc "You made them definitions wearing little hats."
    m forward casual happ cm ce nobl rhip ldown "And yet they're working."
    "I drag the first sticky note beneath judicial review, where it joins the warmup question. {i}Federalism{/i} takes longer to surface because several equally governmental words keep crowding it out."
    menu:
        "Place the shared national-and-local powers under federalism.":
            mc "It's federalism: different levels of government exercising power in their own spheres."
            m forward casual happ cm oe nobl rhip ldown "Exactly! Different floors of the same building, with both sides still fighting over the kitchen."
        "Place the shared national-and-local powers under separation of powers.":
            mc "Separation of powers?"
            m forward casual wry cm oe nobl rhip ldown "Separation of powers is branches at the same level keeping each other in check. Here, we're looking at layers."
            "She writes {i}FEDERALISM{/i} above the second box."
            mc "Right, same building, different floors."
            m forward casual happ cm oe nobl rdown ldown "And, of course, a recurring fight over the kitchen."
        "Place the shared national-and-local powers under popular sovereignty.":
            mc "Would it be popular sovereignty?"
            m forward casual curi om oe nobl rhip ldown "That's authority coming from the people. Here, the important part is the two levels."
            "She writes {i}FEDERALISM{/i} above the second box."
            mc "Right, same building, different floors."
            m forward casual happ cm oe nobl rdown ldown "And, of course, a recurring fight over the kitchen."
    "I tap the last box."
    mc "Before the government takes liberty or property, it has to warn you and give you a chance to answer. That's the whole legal-flavored meal."
    m forward casual happ om oe nobl rhip lpoint "Due process."
    mc "Mom would be devastated to hear it reduced to a meal."
    m forward casual happ cm ce nobl rdown ldown "Your mom would improve the metaphor and bill us for the hour."
    "Monika caps the green pen and trades it for a blue one."
    m forward casual curi om oe nobl rhip ldown "And now...language arts."
    mc "Oh, so blue means regime change?"
    m forward casual happ cm oe nobl rdown ldown "Read this."
    "She turns her notebook around. Four short sentences sit alone in the middle of the page."
    "{i}The door was left open. The lamp was switched off. A cup was moved to the far side of the table. Nothing else in the room had changed.{/i}"
    "{i}The cup again? Teachers really do have one prop between them.{/i}"
    m forward casual neut om oe nobl rhip ldown "In the paragraph below this one, the narrator keeps showing concrete actions but never names who did them. What does that make the reader do?"
    menu:
        "Assign the missing agency themselves.":
            mc "The reader has to assign the missing agency. The actions stay visible, but responsibility gets slippery."
            m forward casual happ cm oe nobl rdown ldown "Yes! Name what the writing does, then explain why it matters. That's the whole chain."
        "Trust the narrator for staying objective.":
            mc "Trust the narrator for staying objective?"
            "Monika slides the notebook back half an inch."
            m forward casual curi om oe nobl rhip ldown "Do you trust someone more when they keep showing you consequences and hiding who caused them?"
            mc "When you phrase it with all that accusation, no."
            m forward casual happ cm oe nobl rdown ldown "The omission makes the reader assign agency. The actions stay visible while responsibility gets slippery."
        "Stop feeling any tension because no actor is named.":
            mc "It removes the tension because nobody is named."
            m forward casual wry cm oe nobl rhip ldown "Did it feel less tense when you read it?"
            "I look over the paragraph again. Nothing about it feels neutral."
            mc "No. Annoyingly."
            m forward casual happ om oe nobl rdown ldown "The reader has to assign the missing agency. The actions stay visible while responsibility gets slippery."
    "I write the note in the margin."
    mc "So an unreliable narrator is the same trick?"
    m forward casual neut om oe nobl rhip ldown "Related, not the same. Unreliable doesn't just mean first person or liar."
    m "Their account has to conflict with the story's evidence, or give us a reason to check the room around them before accepting it."
    mc "So the narrator says the cup never moved, but it's sitting across the room."
    m forward casual happ cm oe nobl rdown ldown "You've got it! Even the furniture gets a rebuttal."
    "She draws a tiny door beside the paragraph, then another beneath it."
    m forward casual curi om oe nobl rhip ldown "Now say that locked door appears every time a character avoids making a choice."
    mc "Then it supports the theme. The image returns every time the character dodges a choice."
    m forward casual happ om ce nobl rdown ldown "There you go. Now the recurring image is actually doing something."
    mc "As opposed to a blue curtain existing once because the room needed curtains."
    m forward casual wry cm oe nobl rhip ldown "Be careful. Somewhere, a literature teacher just sat upright."
    "We give the imaginary teacher a respectful second to settle back down."
    "The remaining humanities pages go faster. We return to legitimacy and public trust, where authority needs reasons people can recognize instead of only consequences they fear."
    "Then we read a restrained paragraph twice and track how its omissions change our sympathy for the narrator. Monika makes me name the effect instead of hoping the grader accepts {i}it feels more serious{/i}."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Sciences rear their ugly heads next."
    nier "The green and blue notes move aside. Monika produces a yellow stack for two classes she isn't taking, which is either friendship or evidence of a larger organizational problem."
    call nier_clear from _call_nier_clear_0525_4
    pause 2.0
    scene bg library
    $ show_calendar()
    $ atmos_clear()
    show monika forward casual happ cm oe nobl rdown ldown at t11
    with wipeleft_scene
    mc "You made cards for my biology and chemistry classes?"
    m forward casual nerv om oe awkw rdown ldown "Only for the topics in the photos you sent me."
    mc "You're not even in either of these classes."
    m forward casual happ cm ce nobl rdown ldown "Which makes me the perfect test audience. Teach it to me without hiding behind vocabulary."
    mc "This feels like a trap built by a very supportive person."
    m forward casual happ om oe nobl rhip lpoint "I'll take that as a compliment! Start with the cell."
    "She puts a blank sticky note in the center of the table and writes {i}PROTEIN{/i} on it."
    mc "The Golgi apparatus modifies the protein, then sorts it into a package for transport."
    m forward casual curi om oe nobl rhip ldown "So...the cell's post office?"
    mc "More or less, yeah."
    "She folds the sticky note into a tiny square and slides it toward my bag."
    m forward casual happ cm oe nobl rdown ldown "Modified, sorted, packaged, shipped."
    mc "Your visual aid is leaving glue on the table."
    m forward casual wry cm oe nobl rhip ldown "Knowledge has a cost, apparently."
    "For meiosis, the sticky notes become chromosomes. She tears two colors in half and swaps the ends before mixing the pairs into new rows."
    mc "Crossing over trades pieces between homologous chromosomes. Independent assortment changes which combinations line up into gametes."
    m forward casual neut om oe nobl rhip ldown "Both increase genetic variation, but in different ways. Trade pieces, then deal the deck."
    mc "That's irritatingly better than my textbook."
    m forward casual happ cm ce nobl rdown ldown "I'm available for licensing."
    "She draws a small food web next: plants, insects, birds, and one badly rendered predator in the middle."
    mc "If that middle one is a keystone species and it disappears, the result isn't automatically nothing just because it wasn't the largest thing there."
    "I lift the center note, and three arrows lose their destination."
    mc "The change cascades across the community. Role matters more than size."
    m forward casual curi om oe nobl rhip ldown "Your ecosystem has fallen apart because I drew a terrible fox."
    mc "Nature's cruel, especially when you draw it."
    "Biology goes into a small completed pile. Chemistry replaces it with an equation and five pen caps Monika must have collected for this exact purpose."
    m forward casual happ om oe nobl rhip lpoint "Two hydrogen molecules plus one oxygen molecule make two water molecules. We have five moles of hydrogen and two of oxygen, so which runs out first?"
    "I group the caps into two complete batches. They use four hydrogen and both oxygen, leaving one hydrogen stranded beside them."
    menu:
        "Oxygen is the limiting reactant.":
            mc "Oxygen. Two moles of it can only use four moles of hydrogen, so oxygen limits the reaction and one mole of hydrogen is left over."
            m forward casual happ cm oe nobl rdown ldown "There it is! The lonely cap survives."
        "Hydrogen is the limiting reactant.":
            mc "Hydrogen."
            m forward casual curi om oe nobl rhip ldown "Build the second batch."
            "I do: four hydrogen caps and both oxygen caps disappear into imaginary water, leaving one hydrogen behind."
            mc "Right, oxygen runs out first."
            m forward casual happ cm oe nobl rdown ldown "The lonely cap survives."
        "Neither reactant limits it.":
            mc "Neither? It balances."
            m forward casual wry cm oe nobl rhip ldown "The equation balances, but our amounts don't."
            "I build two complete batches. Four hydrogen caps and both oxygen caps disappear into imaginary water, leaving one hydrogen behind."
            mc "Oxygen runs out first."
            m forward casual happ cm oe nobl rdown ldown "The lonely cap survives."
    "Monika returns the surviving cap to her pencil with more ceremony than it deserves."
    m forward casual neut om oe nobl rhip ldown "Equilibrium next: nitrogen and hydrogen reversibly form ammonia, and then we add more hydrogen."
    mc "The system shifts toward ammonia to use some of what we added."
    m forward casual happ cm oe nobl rdown ldown "Which means it moves toward the products."
    mc "Then the extra hydrogen becomes ammonia, so now it's somebody else's problem."
    m forward casual happ om ce nobl rdown ldown "Apparently chemistry avoids conflict, too."
    "The last yellow card has a tiny pH scale drawn along one edge."
    m forward casual curi om oe nobl rhip ldown "Compare a solution at pH three with one at pH four."
    mc "Ten times more acidic. The scale is logarithmic, so the one-point difference is a factor of ten."
    m forward casual nerv om ce blaw rdown ldown "...So not three-fourths as acidic."
    mc "Please tell me that wasn't on one of your answer drafts."
    m forward casual happ cm ce nobl rdown ldown "I said it so you wouldn't have to."
    "The last yellow cards move faster. Biology gets feedback loops and population limits, while chemistry makes us revisit significant figures."
    "We sort reaction types and check solubility rules after that. None of it becomes pleasant, but at least it's recognizable when we put the stack away."
    "I drink some water and reset the conversation. Monika follows, apparently satisfied that hydration counts as a study technique."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "After biology and chemistry, algebra gets its turn."
    nier "Science leaves the table looking like an abandoned craft project. The loose pen caps should confuse the library staff later."
    call nier_clear from _call_nier_clear_0525_5
    pause 2.0
    scene bg library
    $ show_calendar()
    $ atmos_clear()
    show monika forward casual anno cm oe nobl rdown ldown at t11
    with wipeleft_scene
    "Monika's algebra sheet is already open to a rational function. The denominator is boxed so firmly that it has embossed the next page."
    m forward casual anno om oe nobl rhip ldown "I know I can't divide by zero. What keeps getting me is turning that into the domain without losing a sign."
    mc "Then don't start with the domain. Start with what would make the denominator zero."
    "I factor {i}x squared minus nine{/i} and leave the two terms apart."
    mc "Negative three and positive three make the denominator zero, so the domain is every real number except those two."
    m forward casual neut om oe nobl rhip ldown "Find the forbidden values first, then state the domain."
    mc "That's it."
    "She writes {i}x cannot equal negative three or three{/i} in the margin, then underlines both signs separately."
    m forward casual curi om oe nobl rdown ldown "Try mine: log base two of x minus one equals four."
    menu:
        "Rewrite it as x minus one equals sixteen, so x equals seventeen.":
            mc "Two to the fourth is sixteen, which means x minus one is sixteen. So x is seventeen."
            m forward casual happ cm oe nobl rdown ldown "Seventeen keeps the logarithm's input positive, and we're done."
        "Multiply four by two, so x equals nine.":
            mc "Four times two is eight, then I add one...nine?"
            m forward casual wry cm oe nobl rhip ldown "Logs don't multiply the base by the exponent. Rewrite it exponentially."
            mc "Two to the fourth is sixteen, so x minus one equals sixteen and x is seventeen."
            m forward casual happ cm oe nobl rdown ldown "And seventeen keeps the input positive."
        "Subtract the base from four, so x equals three.":
            mc "Four minus two, then add one...three?"
            m forward casual curi om oe nobl rhip ldown "What does log base two actually ask?"
            mc "It's asking what power of two gives x minus one. Right...two to the fourth is sixteen, so x is seventeen."
            m forward casual happ cm oe nobl rdown ldown "And seventeen keeps the input positive."
    "The next problem is already in vertex form: two times x minus three squared, minus five."
    m forward casual neut cm oe nobl rdown ldown "The vertex is three, negative five. The positive two means it opens up."
    mc "You knew that one."
    m forward casual nerv om oe awkw rdown ldown "I...wanted confirmation."
    mc "Rule one."
    "Her pen stops."
    m forward casual nerv cm oe awkw rdown ldown "I knew the vertex, but I was guessing about the direction."
    mc "A positive coefficient opens up, while a negative one opens down."
    m forward casual happ cm oe nobl rdown ldown "Thank you."
    "She says it without trying to turn it into a smaller admission. I draw a tiny upward parabola beside the answer and give it an unnecessarily happy face."
    m forward casual happ om ce nobl rdown ldown "The happy face really sells the rigor."
    mc "Without it, the whole proof falls apart."
    "We spend another stretch on matrices, taking turns saying row times column until it stops sounding like English."
    "By the fourth example, Monika catches me reversing the result dimensions before I can write them down wrong."
    "Functions and sequences follow. A word problem disguises itself as a train schedule, but Monika strips the story down to the pattern before it can collect a fare."
    mc "Okay...maybe the terrifying sticky notes stay."
    m forward casual happ cm oe nobl rhip ldown "At last! Office supplies have won you over."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "And finally, foreign language."
    nier "The sun reaches Monika's elbow as calculators give way to workbooks. Somehow, grammar can also be made to look accusatory."
    call nier_clear from _call_nier_clear_0525_6
    pause 2.0
    scene bg library
    $ show_calendar()
    $ atmos_clear()
    show monika forward casual dist cm oe nobl rdown ldown at t11
    with wipeleft_scene
    m forward casual happ om oe nobl rhip lpoint "Present perfect with {i}since{/i}: pick the sentence you would actually hand in."
    menu:
        "She has lived here since 2020.":
            mc "She has lived here since 2020."
            m forward casual happ cm oe nobl rdown ldown "It started then, and it's still true now."
        "She lives here since 2020.":
            mc "She lives here since 2020."
            m forward casual wry cm oe nobl rhip ldown "Understandable, but not the form they're testing."
            mc "She {i}has lived{/i} here since 2020. She started then, and it's still true now."
            m forward casual happ cm oe nobl rdown ldown "There you go."
        "She has lived here for 2020.":
            mc "She has lived here for 2020."
            m forward casual curi om oe nobl rhip ldown "Use {i}for{/i} with a duration and {i}since{/i} with a starting point."
            mc "Right, she has lived here {i}since{/i} 2020."
            m forward casual happ cm oe nobl rdown ldown "It started then, and it's still true now."
    "She draws a line from 2020 to a tiny dot marked {i}NOW{/i}."
    m forward casual neut om oe nobl rhip ldown "Try an unreal past condition: something didn't happen, so we imagine a different result."
    mc "If I had studied more, I would have felt less nervous."
    m forward casual wry cm oe nobl rdown ldown "That example sounds suspiciously relevant."
    mc "The workbook knows where we live."
    m forward casual happ om oe nobl rhip ldown "Had plus past participle, then would have plus past participle! Heh, try saying that three times fast~"
    mc "If I had slept more, I would have resented the alarm less."
    m forward casual happ cm ce nobl rdown ldown "Now you're learning."
    "The final page gives us a short passage about a student offered a summer program in another city."
    "His acceptance email stays open beside a calendar filled with his younger brother's appointments. He still hasn't sent a reply."
    m forward casual curi om oe nobl rhip ldown "Why is he hesitant? Only use what the passage earns."
    mc "He wants to go, but he's worried about leaving people who depend on him."
    m forward casual neut om oe nobl rdown ldown "Exactly. Nothing in the passage says he hates travel or distrusts the program."
    m "It puts what he wants against the people he feels responsible for."
    mc "A reading question whose radical answer is reading what it says."
    m forward casual happ cm oe nobl rhip ldown "You'd be amazed."
    "The workbook ends with a short opinion prompt about distance, and we settle on the least embarrassing honest answer we can manage."
    "Distance can be healthy when it gives people room, but not when it becomes disappearance. Monika checks the grammar while I make sure the sentence still sounds believable."
    "Her phone alarm vibrates against the table, and we both look at it before either of us can turn the page."
    m forward casual lsur om oe nobl rdown ldown "Noon already?"
    "Beyond the second-floor windows, clean morning light has thickened into ordinary midday brightness."
    "The library changed shifts while we weren't looking. More chairs are occupied now, and somewhere downstairs a child is negotiating loudly with a printer."
    mc "We did all five blocks."
    m forward casual curi om oe nobl rhip ldown "Six subjects in total for you. We combined civics and language arts."
    mc "You know what I meant and you know I know."
    m forward casual happ om ce nobl rdown ldown "I do! I wanted the numerical victory."
    "We look at the table. Every tested idea has migrated into one of five small piles: constitutional rules, narrative devices, living systems and reactions, algebra, English."
    "We haven't mastered any of it. Still, every pile looks handled, and that may be more useful today."
    mc "I think my brain has reached capacity."
    m forward casual happ cm oe nobl rhip ldown "Then your brain filled up right on schedule. The cafe's about ten minutes from here."
    "She starts gathering the sticky notes. Two cling to her sweater sleeve, and one's stuck to the back of my hand."
    mc "It seems your system's making a run for it."
    m forward casual laug om ce nobl rdown ldown "Don't let the due process note leave. We need that one tomorrow."
    "I peel it off and return it to the correct stack."
    "Before I shoulder my bag, I text Mom that the library part's done and the cafe's next."
    "Her reply beats the zipper closed."
    "{i}Actual lunch. Not a bunch of sweets.{/i}"
    m forward casual happ cm ce nobl rdown ldown "She knows you~"
    mc "Can you not peer over my shoulder like that...?"
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 1.0
    pause 2.0
    scene bg city_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music dailyfantasy
    "Downtown on a Sunday has room to move without ever becoming empty."
    "The historic district begins where the sidewalks narrow and the storefronts start pretending every brick has a meaningful past."
    "Monika walks beside me with her folder tucked under one arm. I carry the bag of textbooks because my contribution to scholarship has become manual labor."
    show monika forward casual happ cm oe nobl rdown ldown at t11
    m forward casual curi om oe nobl rhip ldown "So, which was worse? The language arts passage or mediating Hikari and Homura on Thursday?"
    mc "The passage never shouted back."
    m forward casual happ cm ce nobl rdown ldown "Hikari was just expressing herself at evacuation volume."
    mc "The windows were expressing concern."
    "We wait at a crosswalk while a bus exhales at the curb."
    m forward casual neut om oe nobl rhip ldown "They did work it out, though, and that's all that matters."
    mc "Yeah, once everyone stopped arguing against the worst possible version of what the other had said."
    m forward casual happ cm oe nobl rdown ldown "That's most club problems, honestly."
    "The signal changes. We cross with a family carrying three shopping bags and a paper windmill."
    m forward casual nerv om oe awkw rdown ldown "I've been thinking about changing the feedback format after exams. Smaller groups, maybe a rotating partner system."
    mc "You already run the place like a minor government."
    m forward casual wry cm oe nobl rhip ldown "A minor government with no budget and four pens that work."
    mc "At least you can rest easy knowing bureaucracy's had worse foundations."
    m forward casual happ om ce nobl rdown ldown "See? You're still studying!"
    "We pass an old bookstore with handwritten recommendations taped inside the glass."
    m forward casual neut om oe nobl rdown ldown "I just don't want the club to turn into one fixed thing because I got too comfortable running it one way."
    mc "I don't think literature clubs, or any clubs for that matter, stay one thing even if you try."
    m forward casual curi om oe nobl rhip ldown "What do they turn into?"
    mc "Believe me, give the internet four recognizable personalities in a clubroom with tea."
    mc "It'll write eight different worlds around them before letting them have one ordinary meeting."
    m forward casual wry cm oe nobl rdown ldown "Only eight?"
    mc "Half of them stop after the prologue, and the other half are better off on a shitty fanfic website sorted under 'New'."
    "Her laugh follows us past the bookstore. A couple coming the other way hears it and smiles at us."
    "The old bank appears at the end of the block, pale stone and tall windows. Across from it, a green awning shades a storefront full of plants."
    m forward casual happ om oe nobl rdown lpoint "There we are!"
    mc "Hey, you remembered it!"
    m forward casual happ cm ce nobl rdown ldown "That makes two numerical victories today."
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 1.0
    pause 2.0
    scene bg cafe
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music dailyleisure
    "The cafe used to sell stationery. It still has the long front windows and narrow wooden shelves."
    "Only now, trailing plants spill between ceramic cups on the shelves. Bags of coffee sit alongside them with serious little biographies."
    "The lunch crowd has thinned, leaving us a few choices. A table near the window sits open between two potted ferns."
    show monika forward casual happ cm oe nobl rdown ldown at t22
    show kotonoha work neut at t21
    "Kotonoha stands behind the register in a dark apron, using the counter edge to level a row of paper cups."
    mc "Afternoon, Kotonoha."
    ko "Good afternoon."
    m forward casual lsur om oe nobl rdown ldown "Kotonoha?"
    ko "Monika. [player]."
    mc "Looks like we caught your Sunday shift."
    ko "I'm here until four."
    mc "Got it."
    show monika forward casual happ cm ce nobl rdown ldown
    "Monika catches up and smiles."
    m forward casual happ om ce nobl rdown ldown "Hi."
    ko work happy "Hi."
    "A small menu stands beside the register. Monika reads every line while I get as far as {i}toasted chicken sandwich{/i} and stop pretending the rest has a chance."
    m forward casual curi om oe nobl rhip ldown "Is the rosemary soup good?"
    ko work thinking "Yes. The bread is better with it."
    m forward casual happ cm oe nobl rdown ldown "I'll have the soup with bread and an iced tea, please."
    mc "Chicken sandwich and iced coffee, please. Oh, and whatever pastry is least capable of ruining dinner."
    ko "The lemon cake is small."
    mc "Perfect! I'll take one strategically modest cake."
    "Kotonoha enters the order without judging the strategy."
    ko work neut "You can take the window table. I'll bring the food over."
    m forward casual happ om oe nobl rdown ldown "Thank you!"
    mc "Thanks."
    show kotonoha at thide
    hide kotonoha
    show monika forward casual happ cm oe nobl rdown ldown at t11
    "We claim the table between the ferns. Outside, buses stop along the far side of the old bank and carry pieces of the street away."
    "Monika sets her folder on the seat beside her instead of between us. For the first time since nine, the table has no work on it."
    m forward casual happ om ce nobl rdown ldown "Oh, this is nice."
    mc "The chairs are objectively better than the library."
    m forward casual wry cm oe nobl rhip ldown "That's your first observation?"
    mc "My back has a voice, and I respect it."
    "Kotonoha brings the drinks first. I move my coffee by the rim to make space for the little number stand."
    "Monika's eyes follow my hand, then settle on the cup."
    m forward casual nerv cm oe awkw rdown ldown "...Huh."
    mc "What?"
    "The answer reaches me before she can hide it: a table near the window, with two cups between us."
    "My hand won't leave the rim alone. Her cup is still waiting for a lipstick mark while buses practice leaving outside."
    mc "You cheated."
    m forward casual vsur om oe nobl rdown ldown "What?"
    mc "Your poem yesterday."
    "Color arrives at her cheeks in stages."
    m forward casual flus om oe blaw rdown ldown "I didn't cheat!"
    mc "You wrote today before it happened."
    m forward casual flus cm oe blus rdown ldown "I wrote a table. Those aren't exactly rare."
    mc "The two cups by the window? The buses outside?"
    "She looks through the glass at a bus pulling away from the curb, which does very little for her defense."
    m forward casual nerv om ce blaw rdown ldown "Okay, maybe I had a specific table in mind."
    mc "You hadn't even been here yet."
    m forward casual nerv om oe awkw rdown ldown "I saw the pictures when I looked up the menu, and I knew what we were doing today."
    "Her thumb slowly traces a clear path through the condensation."
    m forward casual neut om oe blus rdown ldown "I wanted today to go well, so the poem borrowed that."
    mc "It did."
    m forward casual curi om oe nobl rdown ldown "The poem?"
    mc "Today, so far."
    "Her shoulders loosen."
    m forward casual happ cm ce blus rdown ldown "I'm glad."
    "A little lipstick reaches the edge of her glass when she drinks, and the poem settles into the table without either of us pointing it out."
    "For a minute, we talk about the cafe's heroic commitment to plants and whether the lemon cake counts as lunch if cut diagonally."
    "When the register jams, the library printer argument appears to have followed us here in spirit."
    mc "You did it again."
    m forward casual curi om oe nobl rhip ldown "Hm?"
    mc "I mean earlier, when I asked how you were doing."
    "Her straw stops against the ice."
    m forward casual nerv cm oe awkw rdown ldown "Hey, I {i}did{/i} correct it."
    mc "You upgraded from good to tired and nervous. That was very brave."
    m forward casual wry cm oe nobl rhip ldown "Do I get partial credit?"
    mc "Depends, because you brought chemistry flashcards for a class you don't take."
    "She glances toward the folder on the neighboring chair."
    m forward casual nerv om oe awkw rdown ldown "Making those was easier than staring at my own notes."
    mc "That's what I was asking."
    m forward casual nerv cm oe awkw rdown ldown "Don't sound so pleased."
    mc "I'm not. I'm just listening."
    "The espresso machine starts behind the counter. We let it fill the space until it finishes."
    m forward casual neut om oe nobl rdown ldown "I keep thinking if I organize enough things, I'll eventually feel organized. Give me a council schedule or a stack of club feedback and I'm fine."
    m forward casual nerv om oe awkw rdown ldown "Then I open my own folder, and it's still mine."
    mc "That's a pretty serious design flaw."
    m forward casual neut om oe nobl rdown ldown "Right? I'm scared I'll freeze tomorrow."
    "She looks at me when she says it."
    m forward casual nerv om oe awkw rdown ldown "Not fail everything. I know that's probably not going to happen."
    m "Just...sit there and find out I spent all this time learning how to explain things to everyone else, not how to put my own answer down."
    mc "Yeah, I know what you mean."
    "My coffee sits untouched, and the ice shifts on its own."
    mc "Tomorrow, you can't put a little note beside your answer explaining which part you're unsure of."
    m forward casual neut cm oe nobl rdown ldown "That's exactly it."
    mc "I hate that part too."
    "Monika looks down at the ring of water beneath her glass."
    m forward casual nerv om oe awkw rdown ldown "I think I needed permission not to be fine for an hour, though. Now I can go home and be nervous without turning it into a whole performance."
    mc "That sounds suspiciously healthy."
    m forward casual wry cm oe nobl rhip ldown "Don't worry. It feels suspicious to me too."
    mc "Tomorrow, you might get something wrong. I might forget every constitutional word except kitchen."
    m forward casual happ cm oe nobl rdown ldown "Then bad roommates can teach you federalism again."
    mc "See? It's useful already."
    show monika forward casual happ cm oe nobl rdown ldown at t21
    show kotonoha work thinking at t22
    "That earns a small laugh just as Kotonoha arrives with our food. She takes in the quiet at the table."
    ko "Soup with bread for Monika. Chicken sandwich and strategically modest cake for [player]."
    mc "It's earned the title."
    "She sets the plates down without asking what she interrupted."
    ko work worried "The soup bowl is hot."
    m forward casual happ om oe nobl rdown ldown "Thanks, Kotonoha."
    ko work happy "You're welcome."
    show kotonoha at thide
    hide kotonoha
    show monika forward casual happ cm oe nobl rdown ldown at t11
    "Once the food arrives, we have something to do with our hands. Monika tears her bread in half and passes me a piece, so I slide the lemon cake toward the center."
    "The soup is apparently as good as advertised, and the sandwich is better than anything assembled near an exam packet has a right to be."
    "We trade bites, then complaints about teachers who put {i}all of the above{/i} on tests like a personal threat."
    "Monika tells me the student council copier has developed a grinding noise and a belief that every third page should be blank. I tell her the fox in her food web looked like a haunted loaf of bread."
    m forward casual pout om oe nobl rdown lpoint "You understood the ecosystem."
    mc "The ecosystem feared its god."
    m forward casual laug om ce nobl rdown ldown "Oh, shut up!"
    "Lunch stretches on, and neither of us checks the time for several minutes."
    "By the time the plates are empty, water rings overlap beneath our cups and a folded napkin has wedged itself under Monika's phone. The table looks used now, not staged."
    "I turn my empty cup once by the rim."
    m forward casual happ cm oe nobl rhip ldown "You're doing that on purpose now."
    mc "I'm supporting the arts."
    "She looks outside so I don't get to see all of the smile, but the window gives it back anyway."
    "The check arrives in a little wooden tray. Monika reaches first."
    mc "No."
    m forward casual curi om oe nobl rhip ldown "I invited you."
    mc "You used that at the theater. That argument's retired."
    m forward casual wry cm oe nobl rdown ldown "It still has precedent."
    mc "We're splitting it before my mother senses a budget violation from across town."
    "Monika considers appealing, then puts down cash for her half."
    m forward casual happ cm ce nobl rdown ldown "Fine! Due process has been observed."
    mc "The republic survives."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg city_day
    $ show_calendar()
    $ atmos("afternoon")
    stop music fadeout 1.0
    with wipeleft_scene
    play music fantasyserenity
    "Outside, the old bank throws a clean block of shade across the sidewalk. The lunch crowd has given the district back to buses and people with nowhere urgent to be."
    show monika forward casual happ cm oe nobl rdown ldown at t11
    "Monika and I walk together until the next corner separates her bus stop from mine."
    "She adjusts the folder against her chest. One yellow sticky note has survived near the bottom edge."
    mc "And for the record, you can ask me for help before manufacturing an entire curriculum."
    m forward casual happ om oe nobl rhip ldown "Same to you."
    mc "I walked into that one."
    "Her bus appears at the far end of the block."
    m forward casual neut om oe nobl rdown ldown "Light review tonight, and then you stop."
    mc "You too. No midnight spirals, and don't reorganize your notes because the tabs looked lonely."
    "She holds out her hand, but instead of the handshake I expect, I get the loose yellow sticky note."
    "In tidy block letters, it says {i}SLEEP IS PART OF STUDYING.{/i}"
    mc "You're handing out propaganda now?"
    m forward casual happ om ce nobl rdown ldown "Only when it's evidence-based."
    "The bus sighs to a stop beside us."
    m forward casual happ om oe nobl rdown ldown "Text me when you get home?"
    mc "Yeah, you too."
    m forward casual happ cm oe nobl rdown ldown "See you tomorrow, [player]."
    mc "See you then."
    "She boards, then lifts the same hand through the glass as the bus pulls away."
    "I keep the sticky note instead of letting the nearest trash can make a decision for me."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The ride home takes twenty quiet minutes. By my stop, Monika has sent a picture of her closed folder, and I answer with the yellow note stuck to my transit card."
    call nier_clear from _call_nier_clear_0525_7
    stop music fadeout 1.0
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    play music dailyfantasy
    "Home is quiet until I reach the dining room and hear a pencil erase the same spot for the fourth time."
    show asahina worried at t11
    "Asahina has occupied half the table and built a defensive perimeter out of exam material. Her laptop is wedged between two open textbooks."
    "A review packet sits under one elbow, its top corner bent into a gray little triangle. The water beside it hasn't been touched."
    ah "Before you say anything, I {i}am{/i} studying."
    mc "I'd gathered that from the active crime scene."
    show asahina unamused
    ah "Then keep gathering somewhere else."
    "I set my bag down by the stairs, but the science packet catches my eye again."
    "Same faded cell diagram. The crooked arrow still leads out of the nucleus, and the master copy's old shadow still stains the left margin."
    mc "...No way."
    show asahina curious
    ah "What?"
    mc "They still use that packet?"
    ah "What do you mean, still?"
    "I pull the corner free and read the title. {i}FIRST-YEAR INTEGRATED SCIENCE: MIDTERM REVIEW.{/i}"
    mc "I had this exact thing two years ago."
    show asahina annoyed
    ah "It's not your exact one, dumbass. It has my name on it!"
    mc "It's the same master copy. Look, the mitochondrion label is floating three miles away from the mitochondrion."
    "She looks. The label really is floating."
    show asahina unamused
    ah "Maybe it moved."
    mc "Cell migration must be an advanced topic."
    "The civics book beneath it looks familiar too, right down to the city-hall photograph on the cover. This copy has a strip of clear tape keeping the spine politically unified."
    "Her English workbook is the newer edition, but the page layout still makes my hand remember where the grammar boxes used to sit."
    "This isn't my senior schedule spread across the table. The units are older and the questions smaller, but the panic hasn't changed size."
    mc "How's it going?"
    show asahina neut
    ah "Fine."
    mc "You sound like an instruction manual."
    show asahina annoyed
    ah "What the hell does that mean?"
    mc "Nothing. I'm trying out a new phrase."
    "I come back from the kitchen with another glass and set it beside hers, still untouched."
    mc "You want help?"
    show asahina unamused
    ah "Nope."
    mc "Cool."
    "I sit at the far end of the table and check my phone. Monika has made it home, her own yellow note stuck to a closed binder in answer to mine."
    "Asahina erases the same box again, but I keep my eyes on my phone. The refrigerator hums while her pencil taps twice, stops, then taps once more."
    ah "...If the amount of sunlight changes, that's the dependent one, right?"
    "The question arrives aimed at the worksheet instead of me."
    mc "It's independent because the experimenter changes it on purpose."
    show asahina thinking
    ah "But the plant depends on it, doesn't it?"
    mc "You're thinking like the plant. Here, try volleyball."
    "That gets one eye off the page."
    mc "You choose how many minutes a player practices serving, then measure how many serves land in bounds."
    ah "So practice time is independent because you set it."
    mc "Right, so what depends on that?"
    ah "The successful serves, right? Those change in response."
    mc "And that's what you measure."
    "She writes it down, smaller than the words around it."
    show asahina neut
    ah "That's a stupid naming system."
    mc "You can put that on the exam after the correct answer."
    show asahina smug
    ah "I'll cite you."
    "I move to the chair beside her only after she nudges the packet into the space between us."
    "The next few pages come back in pieces. Controlled variables give way to basic cell transport."
    "By the food-web page, I'm looking at the same misshapen hawk I accused of tax fraud at fifteen."
    "Asahina pretends not to need the explanations, then asks detailed follow-ups that ruin the performance. I let her keep pretending."
    show asahina worried
    ah "Does it get easier?"
    mc "Science?"
    ah "No. Exams. All of it."
    mc "I don't know if easier is the word."
    show asahina unamused
    ah "That's not what I asked."
    mc "It's the honest answer. You get better at knowing whether you're actually stuck or panic is just getting loud."
    show asahina worried
    ah "Then which is {i}this{/i}?"
    mc "Right now? A little of both."
    show asahina neut
    ah "Wow. Glad I asked."
    mc "You asked for honest, not inspiring."
    "She bumps her shoulder into mine with barely any force."
    ah "Thanks, shitass."
    mc "Anytime, assface."
    "We finish the food-web page. After that, she closes the science packet herself and reaches for the civics book instead of opening everything at once."
    "Late-afternoon light has moved off the table and halfway up the wall by the time the last question stops turning into three more."
    "The yellow note from Monika is still stuck to my transit card, and Asahina spots it when I stand."
    show asahina teasing
    ah "Did your girlfriend assign you a bedtime?"
    mc "My friend shared evidence-based propaganda."
    ah "Uh-huh."
    mc "Don't make that noise like you cracked a code."
    show asahina smug
    ah "Uh-huh..."
    "The household is a hostile environment for original material."
    mc "I'm going for an easy jog before dinner."
    show asahina curious
    ah "On your foot?"
    mc "Coach said I could, as long as I keep it easy."
    show asahina unamused
    ah "If you come back limping, I'm telling Mom before you get through the door."
    mc "Why's everyone a regulatory agency now?"
    ah "Due process, bitch."
    "I look at her open civics book."
    mc "You know what? That earns full credit."
    "My phone buzzes against the table. Mom wants to know whether the grocery list missed anything."
    "I tell her we're good, and a thumbs-up returns before I pocket the phone."
    "She takes a drink of water at last. By the time I leave, civics is the only book open and the science packet is no longer pinned beneath her elbow."
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 1.0
    pause 2.0

    scene bg residential_day
    $ show_calendar()
    $ atmos("evening")
    with wipeleft_scene
    play music dailyleisure
    "The evening air is cooler than the afternoon, and the pavement is still holding onto the day."
    "I start slow. Actually slow, knowing Coach would have my hide if I turned up limping on both sides."
    "My foot stays quiet, thankfully."
    # SFX SUGGESTION: Even running footfalls and measured breathing, briefly isolated from the music.
    "Footfall. Breath."
    "Shoulders loose. Turn at the corner."
    "My phone buzzes in my hand, cutting through the playlist and whatever rhythm I had going."
    "I slow to a halt and check the screen."
    "{i}If this is a reminder to hydrate, I am going to hear Coach's voice behind hers.{/i}"
    call phone_call("Mom", status="Incoming Call", can_decline=False) from _call_phone_call_0525_1
    python:
        _phone_call_lines = [
            phone_call_line("me", "Hey, Mom."),
            phone_call_line("them", "..."),
            phone_call_line("me", "...Mom?"),
            phone_call_line("them", "...no, not those, the ones in the back aren't bruised to hell..."),
            phone_call_line("me", "Hello?"),
            phone_call_line("them", "...is this on sale, or is the little sign just lying to me..."),
            phone_call_line("me", "Mom, you're talking into my ear."),
            phone_call_line("them", "...and the list, now where did I put the-- hm?"),
            phone_call_line("me", "MOOOOOOOOOOOM!"),
            phone_call_line("them", "...What? Hold on--"),
            phone_call_line("them", "Oh, for-- did I call you? I checked your reply and shoved my phone in my bag without locking it."),
            phone_call_line("me", "And lost the round, it seems."),
            phone_call_line("them", "The plums here started it!"),
            phone_call_line("them", "Wait-- why are you breathing like that. Are you running?"),
            phone_call_line("me", "Easy jog. Heavy emphasis on {i}easy{/i}."),
            phone_call_line("them", "I can hear the emphasis working very hard to cover for you."),
            phone_call_line("me", "I'm basically walking."),
            phone_call_line("them", "Then keep basically walking. It's the night before exams, not-- hang on--"),
            phone_call_line("them", "...yes, just these two, thank you-- no, I don't need a bag..."),
            phone_call_line("me", "...You still alive over there?"),
            phone_call_line("them", "I'm fine, just checking out right now."),
            phone_call_line("them", "Hey, miss? I have a case of water under here that still needs to be scanned."),
            phone_call_line("me", "Sounds like you're having a lot of fun."),
            phone_call_line("them", "Okay, I actually have to-- be home before it's fully dark, please."),
            phone_call_line("me", "Yeah. Already turning back."),
            phone_call_line("them", "Good. And drink some-- you know what, you already know."),
            phone_call_line("me", "There's the hydration order."),
            phone_call_line("them", "Love you, sweetheart-- ugh, the card reader won't-- okay, one second--"),
            phone_call_line("me", "Love you. Go rage against the machine."),
            phone_call_line("them", "Always do."),
        ]
    call phone_call_conversation("Mom", _phone_call_lines, status="Connected") from _call_phone_call_conversation_0525_1
    # Her still-open grocery thread pocket-called him, and she ran the whole
    # errand out loud anyway. After this, calling her about a household question
    # too trivial to justify a call is normal between them.
    $ phone_open("mom_call")
    "The call ends. I stand on the sidewalk, phone in hand, while the evening cools the back of my neck."
    "I put the phone away and jog home slower than before."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Mom comes home with groceries and asks Asahina three questions that sound casual but function like a study audit. Then she makes tea and declines to hold court over it."
    call nier_clear from _call_nier_clear_0525_8
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music fantasypassion
    "Night returns me to my desk."
    "The review sheets and alarm list are still there. Tomorrow is too."
    "I review lightly. A light pass keeps the shape without scraping the paint off it."
    "The screen lights up beside my elbow."
    python:
        _phone_messages = [
            phone_msg("them", "Final check-in before I become responsible and sleep."),
            phone_msg("me", "You first."),
            phone_msg("them", "I'm literally putting my notes away right now."),
            phone_msg("me", "I'm almost putting mine away."),
            phone_msg("them", "Physical version, please."),
            phone_msg("me", "Fine."),
            phone_msg("them", "No midnight review spirals."),
            phone_msg("me", "Same to you."),
            phone_msg("them", "Deal."),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0525_2
    # After a full day together and an unprompted night check-in, a casual video
    # call is no longer a leap. This opens Monika's independent FaceTime chatter.
    $ phone_open("monika_video")
    "I put the phone away, then actually put the notes away too."
    "My room looks cleaner without the papers spread open."
    "{i}Tomorrow there's no folder to reopen. No draft to revise.{/i}"
    "{i}No bracket to hide the part I'm not sure of.{/i}"
    "{i}Whatever I put on the page is the answer. That's supposed to be the simple part.{/i}"
    "{i}Tonight it sounds more like a warning.{/i}"
    "Downstairs, a cabinet closes."
    "Sunday has been too gentle. Gentle in a way that makes Monday look sharper by contrast."
    "That should be comforting."
    "Mostly, it is."
    "Mostly."
    $ update_character_thought("monika", "Monika reserved the table and brought flashcards for subjects she isn't taking. Making other people's plans is easier than opening her own folder.")
    $ update_character_thought("asahina", "Asahina's first-year science packet is the same photocopy I got two years ago. She waited until panic had a pulse before asking, then let me help anyway.")
    $ update_character_thought("kotonoha", "Kotonoha works Sundays at the cafe by the old bank. She keeps the counter running like any other shift.")
    $ update_character_thought("mom", "Mom's pocket called me during my jog. Even by accident, she managed to check whether I was overdoing it.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Sunday ends without an explosion."
    nier "Tomorrow, the papers turn over."
    call nier_clear from _call_nier_clear_0525_9
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0525_1
    jump a0526
