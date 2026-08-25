label a0528:
    # --- Day 14: 2025-05-28 --
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    with dissolve_scene_full
    play music quiz
    window auto
    # Day 3: morning College Algebra, afternoon English.
    $ exam_guard_checkpoint_or_jump("algebra", "exam_start", "a0528_algebra_save_scum")
    "Third day of exams."
    if persistent.exam_save_scum_subjects:
        "The word third should mean progress."
        "Instead, it means I have had two nights to imagine the school office turning my name into a conversation."
        "Mom knowing has not made the fear smaller."
        "It has only given the fear a chair at the table."
        "{i}Math, finally.{/i}"
        "{i}Please let me not make this worse.{/i}"
    else:
        "{i}Math, finally.{/i}"
        "{i}A walk in the park, says the part of me that should not be trusted with forecasts.{/i}"
    # SFX SUGGESTION: A heavy exam packet landing flat on the desk.
    "The thought dies the moment the algebra exam hits my desk at a page count that feels personal."
    "College algebra does not threaten you directly."
    "It simply places a rational expression in front of you and waits for arrogance to do the rest."
    show math_teacher neut at t11
    math_teacher "Read each question carefully."
    math_teacher "If a value is excluded from a domain, I expect to see that exclusion respected."
    math_teacher "Begin."
    show math_teacher at thide
    hide math_teacher
    $ exam_guard_checkpoint_or_jump("algebra", "q1_open", "a0528_algebra_save_scum")
    "{i}Question 1. What is the domain of f(x) equals (x plus 2) over (x squared minus 9)?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "All real numbers except x equals -2.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "I mark it."
        "All real numbers except x equals -3 and x equals 3.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "All real numbers except negative three and positive three."
            "The denominator factors into x minus three and x plus three, and division by zero remains out of bounds."
            "{i}Boundaries respected.{/i}"
        "All real numbers.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "I mark it and move on."
    $ exam_guard_checkpoint_or_jump("algebra", "q1_answered", "a0528_algebra_save_scum")
    "The next few problems ask for transformations, intercepts, and one graph that looks like it got scared halfway through existing."
    $ exam_guard_checkpoint_or_jump("algebra", "q2_open", "a0528_algebra_save_scum")
    "{i}Question 2. Solve log base 2 of (x minus 1) equals 4.{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "x equals 17.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "x equals seventeen."
            "If log base two of x minus one is four, then x minus one is sixteen."
            "{i}The algebra behaves. I check it twice.{/i}"
        "x equals 15.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "The pencil goes down before I can talk myself back out of it."
        "x equals 8.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "It looks right enough at this speed."
    $ exam_guard_checkpoint_or_jump("algebra", "q2_answered", "a0528_algebra_save_scum")
    "The third section gives me a quadratic in vertex form."
    "I almost relax, then remember relaxation is how signs ambush people."
    $ exam_guard_checkpoint_or_jump("algebra", "q3_open", "a0528_algebra_save_scum")
    "{i}Question 3. For f(x) equals 2 times (x minus 3) squared minus 5, what is the vertex and does the graph open up or down?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "Vertex (-3, -5), opens up.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "I circle it and keep going."
        "Vertex (3, -5), opens down.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Good enough. Next question."
        "Vertex (3, -5), opens up.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "Vertex three, negative five, opens up."
            "The coefficient is positive, so the parabola opens upward."
            "{i}One sign behaving itself.{/i}"
    $ exam_guard_checkpoint_or_jump("algebra", "q3_answered", "a0528_algebra_save_scum")
    "The rest of the exam passes through functions, sequences, and one word problem that tries to disguise itself as a train schedule."
    "I finish with five minutes left and spend four of them checking signs."
    "The remaining minute is for staring at the wall and letting my hand stop clenching."
label a0528_after_algebra:
    $ hide_calendar()
    scene black with wipeleft_scene
    if persistent.did_save_scum_algebra:
        nier "The morning session ends with a bell that does not release me."
        nier "It only proves the room can move on from a public failure faster than the person inside it can."
        nier "Outside the classroom, people compare answers immediately. I hear the number seventeen twice and feel my stomach fold around itself."
    else:
        nier "The morning session ends with a bell and the particular relief of surviving a subject that can punish you for a single missing minus sign."
        nier "Outside the classroom, people compare answers immediately. I hear the number seventeen twice and decide that is all the validation I am emotionally prepared to receive."
    call nier_clear from _call_nier_clear_0528_1
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    stop music fadeout 1.0
    with wipeleft_scene
    if persistent.did_save_scum_algebra:
        play music hopeless
    else:
        play music daily
    if persistent.did_save_scum_algebra:
        "Lunch on the final exam day has an unstable mood."
        "Everyone else has started acting alive again."
        "I am close enough to the end to understand how much damage can still fit into one afternoon."
        "I open my English notes and read the same line four times."
        "The line says something about conditionals."
        "{i}If I had not been stupid.{/i}"
        "{i}If Mom had not trusted me to handle midterms.{/i}"
        "{i}If Monika never asks why I stopped showing up in the top score cluster.{/i}"
        "None of those are useful English sentences."
        "They are still the only ones my brain wants to conjugate."
    else:
        "Lunch on the final exam day has an unstable mood."
        "Everyone is quieter, and the end is near enough that hope keeps making people careless."
        "Someone near the vending machines announces that English will be easy."
        "Three people tell him to shut up with impressive unity."
        "{i}The room has spoken.{/i}"
        "I drink water, eat what I packed, and refuse to open my English notes until five minutes before the bell."
        "Then I open them with six minutes left."
        "{i}Discipline remains easier in theory.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The afternoon pulls us back in."
    nier "By this point, desks feel less like furniture and more like assigned positions."
    call nier_clear from _call_nier_clear_0528_2
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    stop music fadeout 1.0
    with wipeleft_scene
    play music quiz
    $ exam_guard_checkpoint_or_jump("english", "exam_start", "a0528_english_save_scum")
    show english_teacher neut at t11
    english_teacher "Last exam of the set."
    english_teacher "Listening section first, grammar and reading after that. Stay with the timing."
    "The speakers crackle once."
    "A recorded voice greets us. Whoever recorded it was never going to be in the room."
    english_teacher "Begin."
    show english_teacher at thide
    hide english_teacher
    "The listening section comes and goes in neat little conversations about train stations, weather plans, and one student who apparently cannot find his umbrella despite the recording giving him three clues."
    $ exam_guard_checkpoint_or_jump("english", "q1_open", "a0528_english_save_scum")
    "{i}Question 1. Choose the sentence that correctly uses the present perfect with since.{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "She lived here since 2020.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "I mark it."
        "She has lived here since 2020.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "She has lived here since 2020."
            "Started in the past, still true now. Since gets the starting point."
            "{i}Grammar behaving like a timeline. Fine.{/i}"
        "She has lived here for 2020.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "I mark it and move on."
    $ exam_guard_checkpoint_or_jump("english", "q1_answered", "a0528_english_save_scum")
    "The next grammar question looks friendlier."
    "Experience says friendliness is how exams lure people into rushing."
    $ exam_guard_checkpoint_or_jump("english", "q2_open", "a0528_english_save_scum")
    "{i}Question 2. Which sentence correctly expresses an unreal past condition?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "If I had studied more, I would have felt less nervous.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "If I had studied more, I would have felt less nervous."
            "Past perfect in the condition, would have in the result."
            "{i}Also known as the official grammar of regret.{/i}"
        "If I study more, I would have felt less nervous.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "The pencil goes down before I can talk myself back out of it."
        "If I had studied more, I feel less nervous.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "It looks right enough at this speed."
    $ exam_guard_checkpoint_or_jump("english", "q2_answered", "a0528_english_save_scum")
    "The reading passage is about a student deciding whether to join a volunteer program abroad."
    "Which feels targeted."
    "There are paragraphs about wanting distance, worrying about family, and learning that leaving does not automatically mean abandoning people."
    "{i}Even the foreign language exam has discovered my home life.{/i}"
    $ exam_guard_checkpoint_or_jump("english", "q3_open", "a0528_english_save_scum")
    "{i}Question 3. Based on the passage, why is the narrator hesitant to join the program?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "He dislikes travel and wants to avoid new places.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "I circle it and keep going."
        "He believes the program has no academic value.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Good enough. Next question."
        "He wants the opportunity but worries about leaving people who depend on him.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "He wants the opportunity but worries about leaving people who depend on him."
            "Main idea with emotional friction."
            "{i}I resent how answerable this is.{/i}"
    $ exam_guard_checkpoint_or_jump("english", "q3_answered", "a0528_english_save_scum")
    "The last written response asks for a short opinion in English."
    "I choose the least embarrassing version of honesty and write that distance can be healthy if it does not become disappearance."
    "It looks simple."
    "It still takes me longer than it should."
label a0528_after_english:
    $ hide_calendar()
    scene black with wipeleft_scene
    # SFX SUGGESTION: The final bell followed by chairs dragging back and the room's held breath releasing.
    if persistent.exam_save_scum_subjects:
        nier "When the final bell rings, the exam period does not loosen."
        nier "Not for me."
        nier "For everyone else, chairs drag and shoulders drop and someone laughs at absolutely nothing because the body occasionally discovers freedom before the mind catches up."
        nier "My body discovers a different message."
        nier "Go to the office. Tell Mom. Explain Monika. Rebuild, if rebuilding is even available."
    else:
        nier "When the final bell rings, the exam period does not explode into cheers."
        nier "It loosens."
        nier "Shoulders drop. Chairs drag. Someone laughs at absolutely nothing because the body occasionally discovers freedom before the mind catches up."
    call nier_clear from _call_nier_clear_0528_3
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    stop music fadeout 1.0
    with wipeleft_scene
    if persistent.exam_save_scum_subjects:
        play music hopeless
    else:
        play music daily
    # SFX SUGGESTION: One close phone buzz cutting sharply through the released hallway noise.
    if persistent.exam_save_scum_subjects:
        "The corridor outside class is loud in a way it has not been since Monday morning."
        "Not happy exactly -- just released."
        "I pick up my bag and almost drop it because my hand forgets how straps work."
        "My phone buzzes."
        "The sound cuts straight through the hallway."
        "{i}Mom? Monika? The office?{/i}"
        "I do not check it immediately because for three seconds I would rather not know which future has reached me first."
        "Then I check it anyway."
        "Nothing important."
        "That is worse, because it means the important thing is still coming."
    else:
        "The corridor outside class is loud in a way it has not been since Monday morning."
        "Not happy exactly -- just released."
        "I shoulder my bag and let the crowd move around me for a second."
        "{i}Six subjects. Three days. Still standing.{/i}"
        "My phone buzzes."
        "I do not check it immediately."
        "The world can wait until I make it down the hall."
    $ hide_calendar()
    scene black with wipeleft_scene
    if persistent.exam_save_scum_subjects:
        nier "Midterms are over."
        nier "Not graded, not forgotten, not harmless."
        nier "The word over has never sounded less like an ending."
        nier "Somewhere between Friday's college page and today's zero, I gave every adult in my life a new question to ask."
        nier "And Mom, unfortunately, is very good at questions."
    else:
        nier "Midterms are over."
        nier "Not graded, not forgotten, not harmless."
        nier "Just over. Enough for the afternoon to feel like it has opened one window."
    call nier_clear from _call_nier_clear_0528_4
    if exam_guard_day_scummed("algebra", "english"):
        call exam_guard_home_confrontation("May 28", "algebra", "english") from _call_exam_guard_home_confrontation_0528
    if exam_guard_should_bad_end():
        jump exam_guard_bad_ending
    if persistent.exam_save_scum_subjects:
        pause 2.0
        scene bg living_room_night
        $ show_calendar()
        $ atmos("home_night")
        stop music fadeout 1.0
        with wipeleft_scene
        play music hopeless
        "Midterms being over does not give the house permission to relax."
        "My bag stays by the coffee table."
        "My phone stays with Mom."
        "The laptop stays downstairs, closed, visible, and much less interesting than all the silence around it."
        show mom neut at t11
        mom "The exams are done."
        mc "Yeah."
        show mom determined
        mom "That means tomorrow is about meetings and repair, not escape."
        mc "I know."
        show mom thinking
        "She studies me long enough to make sure the answer is not just a reflex."
        mom "I hope so."
        "There is no clean response to that."
        "The house fills it with ordinary sounds instead."
        "Water moving through pipes."
        "A cabinet closing in the kitchen."
        "Asahina's footsteps upstairs, stopping once near the landing before deciding not to come down."
        "The week is over for everyone else in the shape people recognize."
        "For me, it has changed shape rather than ending."
        "I sit with that until the living room light starts to feel too bright."
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "Wednesday ends without release."
        nier "There are no more exam papers to take honestly tomorrow."
        nier "Only the part where honesty has to survive without a paper in front of it."
        call nier_clear from _call_nier_clear_0528_5_scum
    else:
        pause 2.0
        scene bg corridor
        $ show_calendar()
        $ atmos("afternoon")
        stop music fadeout 1.0
        with wipeleft_scene
        play music schooldays
        "I make it halfway down the hall before checking my phone."
        "There are three messages."
        "One from Mom, asking for the required confirmation that I remain alive."
        "One from Asahina, consisting only of the word {i}food{/i} and six question marks."
        "One from Monika."
        python:
            _phone_messages = [
                phone_msg("them", "Club room for a little bit?"),
                phone_msg("them", "No studying. I mean it."),
                phone_msg("me", "I'll hold you to that."),
                phone_msg("them", "Please do."),
                phone_msg("me", "On my way."),
            ]
        call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0528_1
        "I text Mom first."
        "Then Asahina, who replies with {i}rude{/i} when I tell her dinner exists as a concept but not yet as an object."
        "By the time I reach the club hallway, the building has started making the noise of students remembering their bodies are allowed to leave."
        $ hide_calendar()
        scene black with wipeleft_scene
        pause 2.0
        scene bg club_day
        $ show_calendar()
        $ atmos("afternoon")
        with wipeleft_scene
        play sound moddooropen
        show monika forward uniform dist cm oe nobl rdown ldown at t11
        "The club room has no study materials on the center desks."
        "This is so strange that I stop in the doorway."
        "On the board, Monika has written two words in clean letters."
        "{i}NO STUDYING.{/i}"
        "Below them, in smaller writing:"
        "{i}Leave before you start reviewing again.{/i}"
        m forward uniform happ cm ce nobl rdown ldown "I told you."
        mc "You prepared the absence of studying."
        m forward uniform happ om oe nobl rdown lpoint "I needed proof."
        "A couple of members near the back gather their bags and leave with tired little waves."
        "Then the room is mostly empty."
        "She sits at one of the center desks and sets her folder facedown where neither of us can open it by accident."
        "I take the chair beside her."
        "For a minute, neither of us does anything."
        "The windows are cracked open enough to let in traffic noise from the street."
        "Someone laughs in the hallway, already moving on to the part of the week where exams become stories instead of events."
        mc "This feels wrong."
        m forward uniform curi om oe nobl rdown ldown "Doing nothing?"
        mc "Doing nothing on purpose."
        m forward uniform happ om oe nobl rdown ldown "That's why we're practicing."
        "The lightness is a choice. Her shoulders have not been that low all week."
        "The quiet does not ask us to make it interesting."
        "It just holds."
        "Eventually, Monika lets out a breath that almost becomes a laugh."
        m forward uniform wry om oe nobl rdown ldown "This is harder than studying."
        mc "Doing nothing?"
        m forward uniform happ cm oe nobl rdown ldown "Letting the week stop."
        mc "...Yeah."
        "My answer stays in the room."
        "For a second, the club room is only late light, stacked desks, and two people letting their hands rest empty on the table."
        "She smiles."
        "Not the quiet library version -- a real one, still tired but freer around the edges."
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "The meeting lasts less than half an hour."
        nier "No poems are exchanged. No grades are predicted. No one says the phrase final answer."
        nier "The club room simply lets the exam period end without asking us to feel relieved on schedule."
        call nier_clear from _call_nier_clear_0528_5
        pause 2.0
        scene bg club_day
        $ show_calendar()
        $ atmos("evening")
        show monika forward uniform dist cm oe nobl rdown ldown at t11
        with wipeleft_scene
        "Monika stays behind to straighten the chairs."
        "I help because standing near her is easier than deciding how to leave."
        m forward uniform happ cm ce nobl rdown ldown "We made it."
        mc "Pending grading, yes."
        m forward uniform curi om oe nobl rdown ldown "[player]."
        mc "Sorry."
        "She sets the last chair in place."
        mc "Yeah."
        mc "We made it."
        "It isn't triumphant."
        "It's quieter than that, maybe more useful."
        "The late light has gone amber across the desks, and the rule is still on the board where she left it."
        "The rule on the board gets one more look before she turns to me."
        m forward uniform neut cm oe nobl rhip ldown "No studying tonight."
        mc "None?"
        m forward uniform neut cm oe nobl rdown ldown "None."
        mc "That feels illegal."
        m forward uniform happ cm ce nobl rdown ldown "Then be brave."
        "She smiles when she says it."
        "I do not argue."
        $ update_character_thought("monika", "Monika kept her no-studying promise by making us sit still long enough for the end of midterms to feel real.")
        $ hide_calendar()
        scene black with wipeleft_scene
        pause 2.0
        scene bg dining_table_night
        $ show_calendar()
        $ atmos("home_night")
        stop music fadeout 1.0
        with wipeleft_scene
        play music dailyleisure
        "Home smells like rice, eggs, and the faint sweet edge of something Mom is pretending not to have bought for morale."
        show mom determined at t31
        show asahina neut at t32
        mom "Shoes off, hands washed, bag down."
        ah "Food?"
        show mom unamused
        mom "After he washes his hands."
        ah "Food soon?"
        show mom teasing
        mom "That's the spirit."
        "Asahina turns on me flat and unfiltered, her last exam having stripped out several settings she normally runs."
        ah "Are yours over?"
        mc "Over."
        ah "Mine too."
        "We stare at each other for a second."
        "Then she holds out one fist."
        "I bump it with mine."
        "It is not ceremonial."
        "It just happens, which makes it better."
        show mom neut
        mom "No one ask anyone how it went until after dessert."
        mc "There's dessert?"
        show asahina shocked
        ah "You hid dessert?"
        show mom smug
        mom "I preserved dessert."
        "She opens the freezer and produces a small carton of ice cream with the care she usually reserves for important documents."
        show asahina happy
        ah "Oh my god."
        mc "Morale confirmed."
        mom "Dessert waits until after dinner."
        "Dinner is simple enough to trust."
        "Eggs over rice. Soup. Pickles. A plate of vegetables that Asahina circles with strategic reluctance until Mom raises one eyebrow."
        "No one successfully avoids the vegetables."
        "No one mentions answer keys."
        "The conversation finds other work."
        "Asahina explains that Sam sent her a sticker of a calculator on fire, which Mom says sounds less encouraging than intended."
        "I tell them Monika banned studying in the club room."
        "Asahina asks whether that counts as a club activity."
        "Mom wants to know whether it worked."
        "I say it did for a few minutes."
        "They both accept that more easily than I expect."
        "After dinner, Mom divides the ice cream into three bowls."
        "Not evenly -- deliberately unevenly."
        show asahina annoyed
        ah "Hey."
        mom "Randomized distribution."
        mc "That's not random. Mine's larger."
        show mom unamused
        mom "Interesting claim."
        show asahina unamused
        ah "Objection."
        show mom teasing
        mom "Sustained. Trade if you want."
        "Asahina and I swap bowls twice and end up with the same ones we started with."
        show mom happy
        "Mom watches this, tired and quietly pleased. She engineered a small household argument purely to prove the house could still have one."
        "The ice cream is cold enough to make my teeth complain."
        "It tastes like the week finally stopped pressing on the back of my neck."
        $ update_character_thought("asahina", "Asahina and I ended midterms with a fist bump and an argument about ice cream portions. That feels exactly right.")
        $ update_character_thought("mom", "Mom bought morale ice cream and pretended uneven servings were randomized. She knew exactly what she was doing.")
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "Wednesday night does not become a victory lap."
        nier "It becomes dishes, a freezer spoon rinsed clean, the club room's no-studying rule, and a bag left unopened by the door."
        nier "Grades will come later."
        nier "For tonight, later is allowed to stay later."
        call nier_clear from _call_nier_clear_0528_6
    $ exam_guard_clear_active_checkpoint()
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0528_1
    jump a0529

label a0528_algebra_save_scum:
    $ exam_guard_mark_scummed("algebra")
    $ calendar.set_date(2025, 5, 28)
    $ hide_calendar()
    scene black with dissolve_scene_full
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("pressure")
    stop music fadeout 0.5
    with dissolve_scene_full
    play music safety
    show math_teacher neut at t11
    math_teacher "[player]."
    "The teacher does not raise his voice."
    "He just taps the answer sheet with two fingers, which is worse."
    math_teacher "Walk me through this."
    "I know exactly what he is asking. That is the whole problem."
    mc "...I'd rather not."
    math_teacher "I imagine not."
    math_teacher "You saw the domain restriction, made a choice, and then still ended up back at the same decision point with new information."
    "He keeps his hand on the paper."
    "His handwriting on the board is always clean."
    "His anger is not."
    math_teacher "You are one of the students I use as a pacing check."
    math_teacher "If you look lost, I know the problem is too dense. If you look bored, I know we can move faster."
    math_teacher "So I am struggling to decide whether this is laziness, arrogance, or panic."
    mc "...I don't know."
    "That is the most honest thing I have said all morning, and it still sounds pathetic."
    "{i}Honor students are supposed to make teachers worry less.{/i}"
    "{i}I have apparently discovered a way to become extra paperwork.{/i}"
    math_teacher "Then take the zero and figure that part out."
    math_teacher "Algebra section is done. Pencil down."
    mc "What happens to my standing?"
    "The words come out too fast. Both of us hear where my head already is."
    math_teacher "That depends on what happens after this room."
    math_teacher "Which is why you should spend less energy calculating outcomes and more energy deciding how honest you intend to be."
    "{i}A missing minus sign would have been a mistake -- he'd have marked it, I'd have learned it, and tonight would just be a bad grade. This isn't a sign error, and there's no honest version of it waiting on the next line for me to fix.{/i}"
    show math_teacher at thide
    hide math_teacher
    play music hopeless fadeout 1.0
    jump a0528_after_algebra

label a0528_english_save_scum:
    $ exam_guard_mark_scummed("english")
    $ calendar.set_date(2025, 5, 28)
    $ hide_calendar()
    scene black with dissolve_scene_full
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("pressure")
    stop music fadeout 0.5
    with dissolve_scene_full
    play music safety
    show english_teacher neut at t11
    english_teacher "[player]."
    "The recorded voice keeps talking a moment longer before the teacher stops the audio."
    "The sudden silence pulls half the room upright."
    english_teacher "Paper facedown, [player]."
    mc "...Did I miss the timing?"
    english_teacher "Do not."
    "One syllable, flat and tired and sharper than the red pen in her hand."
    english_teacher "You have spent this whole year answering reading questions by noticing what a passage tries to hide."
    english_teacher "You know when timing matters. You know when a correction belongs to a draft and when it does not belong to an exam."
    "She glances at the sheet, then back at me."
    english_teacher "I am not angry because you failed English."
    english_teacher "I am angry because you did not."
    "The room pretends not to hear that."
    "I wish it were better at pretending."
    english_teacher "Zero for the section. Paper facedown."
    mc "Is Monika going to hear about this?"
    "I hate myself the second I ask, and the worst part is that it isn't even the wrong fear -- it just isn't the only one."
    english_teacher "I am not discussing other students with you during an exam."
    english_teacher "You should be more concerned with what you are going to say when an adult asks you the same question without giving you answer choices."
    "{i}Unreal past condition, real present consequence.{/i}"
    "{i}If I had studied more, I would have felt less nervous.{/i}"
    "{i}If I had been honest, I would still have something clean to be nervous about.{/i}"
    show english_teacher at thide
    hide english_teacher
    play music hopeless fadeout 1.0
    jump a0528_after_english
