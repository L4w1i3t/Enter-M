label a0528:
    # --- Day 14: 2025-05-28 --
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    with dissolve_scene_full
    play music exam
    # Day 3: morning College Algebra, afternoon English.
    $ exam_guard_checkpoint_or_jump("algebra", "exam_start", "a0528_algebra_save_scum")
    "By day three, sitting down at this desk feels less like arriving and more like picking up something I left half-finished overnight."
    if persistent.exam_save_scum_subjects:
        "The last day should mean almost done, but my hand stalls on the pencil-case zipper while last night's silence comes back."
        "{i}Math, finally. Please, just let me get through one paper and not make anything worse.{/i}"
    else:
        "{i}Math, finally. This should be the easy part.{/i}"
        "{i}... Says the part of me that has never once been trusted with a forecast.{/i}"
    # SFX SUGGESTION: A heavy exam packet landing flat on the desk.
    "The algebra packet lands flat on my desk, a few pages longer than I'd like."
    show math_teacher neut at t11
    math_teacher "All right, everyone. One reminder before you start."
    math_teacher "If the original domain excludes a value, it stays excluded after you simplify, and I expect to see that on the page."
    math_teacher "Canceling a factor doesn't hand you a new function. Keep the {i}original{/i} domain in view."
    math_teacher "You may begin."
    show math_teacher at thide
    hide math_teacher
    $ exam_guard_checkpoint_or_jump("algebra", "q1_open", "a0528_algebra_save_scum")
    "{i}Question 1. For g of x equals (x squared minus x minus 6) over (x squared minus 5x plus 6).{/i}"
    "{i}Identify the discontinuities.{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "A hole at 2 and a vertical asymptote at 3.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "I factor the denominator, write its first root beside {i}hole{/i}, and don't bother checking which factor actually canceled."
        "A hole at 3 and an asymptote at 2. Both remain excluded.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "The factor cancels out of the formula. Not out of the {i}original domain{/i}."
            "So three stays excluded as the hole, and two stays the asymptote."
        "Only 2 is excluded, because canceling x minus 3 restores 3.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Once it's simplified, the expression stops dividing by x minus three. I let that cancellation hand back an input the original function never allowed."
    $ exam_guard_checkpoint_or_jump("algebra", "q1_answered", "a0528_algebra_save_scum")
    "I get through transformations and intercepts and reach the logarithms with plenty of room left on my scratch paper."
    $ exam_guard_checkpoint_or_jump("algebra", "q2_open", "a0528_algebra_save_scum")
    "{i}Question 2. Solve log base 2 of (x minus 2), plus log base 2 of (x minus 4), equals 3.{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "Combine the logs, reject 0 from the original domain, and keep x equals 6.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "The quadratic offers zero and six. The original logarithms throw zero straight back out."
        "Keep both x equals 0 and x equals 6 because both solve the quadratic.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "The quadratic hands me two roots, so I keep both. Neither one ever has to report back to the logarithms that produced it."
        "Add the inputs inside one logarithm and get x equals 7.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Somewhere in my head, the two logarithms merge into one, and I add their inputs instead of multiplying them. Seven appears."
    $ exam_guard_checkpoint_or_jump("algebra", "q2_answered", "a0528_algebra_save_scum")
    "The third section restricts a quadratic to half its graph, then asks me to reverse what's left."
    $ exam_guard_checkpoint_or_jump("algebra", "q3_open", "a0528_algebra_save_scum")
    "{i}Question 3. For f of x equals 3 times (x plus 1) squared minus 2, restricted to x greater than or equal to negative 1.{/i}"
    "{i}Choose its inverse.{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "Negative 1 minus the square-root branch. The domain starts at negative 2.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "The square root opens up two directions, and I take the negative one. The original restriction had already kept the other half of the parabola."
        "Negative 1 plus or minus both square-root branches.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "The plus-or-minus shows up on autopilot after the square root. I copy both branches and never ask whether the result is still a function."
        "Negative 1 plus the square-root branch. The domain starts at negative 2.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "The original restriction keeps the {i}positive{/i} square-root branch, and the old range becomes the inverse's domain."
    $ exam_guard_checkpoint_or_jump("algebra", "q3_answered", "a0528_algebra_save_scum")
    "The remaining functions and sequences go quickly until a word problem buries a simple recurrence under three different arrival times."
    "I finish with five minutes to spare and spend four of them checking signs. The last one goes to staring at the wall while my hand remembers how to unclench."
label a0528_after_algebra:
    $ hide_calendar()
    scene black with wipeleft_scene
    if persistent.did_save_scum_algebra:
        nier "The bell ends the morning session, but it doesn't let me go."
        nier "Everyone else is packed by the time my hand agrees to move."
        nier "Outside, people start comparing answers immediately, and by the second time somebody says {i}six{/i}, my stomach has folded in on itself."
    else:
        nier "The bell sounds unusually merciful after a subject where one missing minus sign can sink a whole page."
        nier "The exam follows us into the hall anyway."
        nier "Somebody says {i}six{/i} in three different conversations. Another student argues for zero."
        nier "I bury both hands in my pockets and keep walking."
    call nier_clear from _call_nier_clear_0528_1
    stop music fadeout 1.0
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    if persistent.did_save_scum_algebra:
        play music hopeless
    else:
        play music day_c
    if persistent.did_save_scum_algebra:
        "With one paper left, the corridor has already started acting alive again. I'm still one afternoon away from making the week worse."
        "I open my foreign language notes and read the same line about conditionals four times. I never make it past the first clause."
        "{i}If I hadn't changed it...{/i}"
        "Every ending I supply puts Mom back across the table from me."
        "I shut the notes and leave the sentence where it is."
    else:
        "Somebody by the vending machines announces that foreign language is going to be easy and gets told to shut the hell up by three people at once."
        "I swear off my foreign language notes until five minutes before the bell, then cave with six to go. Close enough."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The afternoon bell herds us back to our assigned desks one last time."
    call nier_clear from _call_nier_clear_0528_2
    stop music fadeout 1.0
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music exam
    $ exam_guard_checkpoint_or_jump("english", "exam_start", "a0528_english_save_scum")
    show english_teacher neut at t11
    english_teacher "All right. Last exam of the set."
    english_teacher "Listening first, then grammar and reading. Stay with the timing, and when the recording moves on, so do you."
    english_teacher "Some grammar choices are going to look right at first. Read the whole sentence, then choose the one that matches the time relationship and emphasis you were actually given."
    english_teacher "For the reading, mark the strongest claim the evidence {i}earns{/i}, not the stronger one you can imagine around it."
    "The speakers crackle overhead, and a recorded voice greets us with the impossible calm of somebody who will never have to wait for our answers."
    english_teacher "You may begin."
    show english_teacher at thide
    hide english_teacher
    "The listening section passes in tidy conversations about train stations and weather plans. One recorded student gets three separate chances to find his umbrella and blows all of them."
    $ exam_guard_checkpoint_or_jump("english", "q1_open", "a0528_english_save_scum")
    "{i}Question 1. Mei began translating at nine o'clock and is still doing it.{/i}"
    "{i}The speaker wants to emphasize the continuing activity.{/i}"
    "{i}Which sentence fits?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "Mei translates the report since nine o'clock.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "The translating is true right now, so simple present starts to feel defensible. I leave {i}since{/i} to carry the rest of the timeline by itself."
        "Mei has been translating the report since nine o'clock.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "The translating started earlier and is {i}still happening{/i}. Only present perfect progressive carries both the start and the work that hasn't stopped."
        "Mei had been translating the report since nine o'clock.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Past perfect progressive looks suitably complicated on the page. I mark it and ignore the missing later event."
    $ exam_guard_checkpoint_or_jump("english", "q1_answered", "a0528_english_save_scum")
    "The next grammar question looks friendlier, and I catch myself rushing before I've even reached the second sentence."
    $ exam_guard_checkpoint_or_jump("english", "q2_open", "a0528_english_save_scum")
    "{i}Question 2. Riku rejected an internship last year. As a result, he still lives in his hometown now.{/i}"
    "{i}Which sentence expresses that unreal past condition and present result?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "If Riku had accepted the internship last year, he would be living in a large city now.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "{i}Had accepted{/i} reaches back to the unreal decision, while {i}would be living{/i} carries its result into the present."
        "If Riku accepted the internship last year, he would have lived in a large city now.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "The completed form in {i}would have lived{/i} sounds properly unreal. I mark it before I ever look back at {i}now{/i}."
        "If Riku had accepted the internship last year, he will be living in a large city now.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "The unreal past is right, so I stop checking after {i}had accepted{/i} and leave the present result to a future form that can't hold it."
    $ exam_guard_checkpoint_or_jump("english", "q2_answered", "a0528_english_save_scum")
    "The reading passage reports that students who chose to listen to foreign-language podcasts outside class later scored higher on a listening test."
    "Nobody measured their earlier proficiency, and the groups selected themselves."
    "For once, a question seems willing to admit how much it doesn't know."
    $ exam_guard_checkpoint_or_jump("english", "q3_open", "a0528_english_save_scum")
    "{i}Question 3. Which conclusion is best supported by the report?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "Podcast listening caused the higher scores.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "The listeners scored higher, and practice is the obvious route to improvement. I upgrade a plausible explanation into proof the study never produced."
        "The report shows no meaningful relationship because groups were self-selected.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "No random assignment means no proof of cause, and I stretch that warning into {i}no relationship{/i}, erasing a real score difference along the way."
        "Podcast use was associated with higher scores, but causation remains unproven.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "Podcast use and higher scores moved together in the report, but the design never established why they did."
    $ exam_guard_checkpoint_or_jump("english", "q3_answered", "a0528_english_save_scum")
    "The final response asks whether the school should recommend the podcasts, and I argue for a voluntary trial with better follow-up data instead of pretending the report settled anything."
    "Every hedged verb takes longer to write than the confident one I put down first."
    "I keep all of them."
label a0528_after_english:
    $ hide_calendar()
    scene black with wipeleft_scene
    # SFX SUGGESTION: The final bell followed by chairs dragging back and the room's held breath releasing.
    if exam_guard_day_scummed("algebra", "english"):
        nier "The last bell goes. Chairs drag back. Somebody laughs at nothing at all."
        nier "None of the pressure lets up anywhere near my desk."
        if exam_guard_scummed_subjects_outside(exam_guard_scummed_subjects("algebra", "english")):
            nier "An office notice outside will add a second stopped section to the one Mom already knows about."
        else:
            nier "The bell hands me one clear instruction."
            nier "Go to the office. Tell Mom. Say what I changed before anybody has to pull it out of me."
    elif persistent.exam_save_scum_subjects:
        nier "When the final bell rings, chairs scrape back around me, and my two clean papers leave with everybody else's."
        nier "This time, nobody stops at my desk."
    else:
        nier "Nobody cheers at the last bell of exam week."
        nier "Chairs drag back, shoulders drop, and somebody starts laughing at absolutely nothing until two other people join in."
    call nier_clear from _call_nier_clear_0528_3
    stop music fadeout 1.0
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    if persistent.exam_save_scum_subjects:
        play music hopeless
    else:
        play music day_c
    # SFX SUGGESTION: One close phone buzz cutting sharply through the released hallway noise.
    if persistent.exam_save_scum_subjects:
        "The corridor's louder than it's been since Monday morning, voices ricocheting off the lockers while the whole released crowd shoves toward every exit at once."
        if exam_guard_day_scummed("algebra", "english"):
            "I reach for my bag and miss the strap. It takes a second try to catch it, with fingers that won't settle."
            if exam_guard_scummed_subjects_outside(exam_guard_scummed_subjects("algebra", "english")):
                "A phone buzzes somewhere behind me, and my hand still goes to the pocket Mom emptied."
                "The school doesn't need my phone to reach her. I remember that a little too late."
            else:
                "My phone vibrates against my hip, and I turn so fast that my shoulder clips the locker."
                "{i}Mom? The office?{/i}"
                "It's only a carrier notification. A thin laugh gets out of me, and somebody nearby looks over."
        else:
            "I get my bag onto one shoulder and let the crowd break around me."
            "A phone buzzes somewhere behind us, and my hand goes to the pocket Mom emptied."
            "{i}She still has mine. The next notification that matters is the review tomorrow morning.{/i}"
        "A woman from student services catches me before the stairs and checks my face against the name on her clipboard."
        "She holds out a sealed envelope and doesn't bother trying to talk over the hallway."
        "The front reads {i}ACADEMIC CONDUCT REVIEW: MAY 29, 7:40 A.M.{/i}"
        "Beneath that, three smaller lines. Counselor. Examining teacher. Notified parent or guardian."
        "Students stream around us, making plans for food, sleep, and karaoke."
        "I brace the receipt against the wall to sign it while, behind me, somebody tries to fit six people into one celebration photo."
        "The woman tears off my copy and reminds me not to be late."
        "I slide the envelope into my bag, careful not to bend it."
        "My fingers keep shaking until the zipper catches."
    else:
        "The corridor's louder than it's been since Monday morning, every voice breaking loose at once."
        "I get my bag onto one shoulder and step aside to let the first rush go by."
        "{i}Six subjects in three days, and I'm still standing.{/i}"
        "My pocket buzzes. I leave the phone where it is until I've made it down the hall at whatever pace my legs feel like offering."
        "Somebody two doors down is explaining, at volume, exactly which conditional he chose."
        "Nobody stops him. Nobody agrees with him, either."
        "Near the stairs, a first-year is asleep upright against the wall with her bag still on both shoulders."
        "Her friend is guarding her with an arm out, the way you'd guard a full cup."
        "{i}... That's the whole week, honestly.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    if exam_guard_day_scummed("algebra", "english"):
        nier "Midterms are over. The last papers haven't even been graded yet, and the conduct notice is already in my bag."
        if exam_guard_scum_count() >= 2:
            if len(exam_guard_scummed_subjects("algebra", "english")) > 1:
                nier "The last day added two zeros before I'd even made it out of the building."
            else:
                nier "The last day added another zero to a week that was already under review."
            nier "Mom is about to hear that I did it again."
            nier "Every opening line I try falls apart before I reach the stairs."
        else:
            nier "Friday's college page keeps flashing behind my eyes while I walk."
            nier "When Mom asks me why, I still won't have an answer that survives being said out loud."
    elif persistent.exam_save_scum_subjects:
        nier "Midterms are over, and the last two sections stayed clean."
        nier "The first zero is still in a folder somewhere, with tomorrow morning stapled to it."
        nier "Whatever repair looks like, it's scheduled to start at 7:40."
    else:
        nier "Midterms are over."
        nier "For the first time since Monday, the grades can wait somewhere I don't have to follow them."
    call nier_clear from _call_nier_clear_0528_4
    if exam_guard_day_scummed("algebra", "english"):
        call exam_guard_home_confrontation("May 28", "algebra", "english") from _call_exam_guard_home_confrontation_0528
    if exam_guard_should_bad_end():
        jump exam_guard_bad_ending
    if exam_guard_day_scummed("algebra", "english"):
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "Wednesday ends upstairs, with my phone downstairs and the review notice still square inside my bag."
        nier "At 7:40 tomorrow, I have to say it all again, in front of my teacher and Mom."
        call nier_clear from _call_nier_clear_0528_5_new_scum
    elif persistent.exam_save_scum_subjects:
        stop music fadeout 1.0
        pause 2.0
        scene bg living_room_night
        $ show_calendar()
        $ atmos("home_night")
        with wipeleft_scene
        play music hopeless
        "I come in and leave my bag beside the coffee table. Mom has my phone next to her, and I set the closed laptop down between us."
        show mom sad at t11
        mom "The exams are done."
        mc "Yeah."
        show mom determined
        mom "I've arranged to be there tomorrow. We'll hear what the school needs from you, then talk at home."
        mc "I know."
        show mom worried
        "She waits for something past the familiar answer."
        "I make myself hold her eyes instead of reaching for the same one again."
        mom "I hope so."
        "Upstairs, Asahina takes two steps toward the landing and turns back."
        "Mom hears it too. She keeps looking at me."
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "Wednesday ends without settling anything, and tomorrow begins at 7:40 in student services."
        call nier_clear from _call_nier_clear_0528_5_scum
    else:
        stop music fadeout 1.0
        pause 2.0
        scene bg corridor
        $ show_calendar()
        $ atmos("afternoon")
        with wipeleft_scene
        play music school_day_a
        "Halfway down the hall, I give in and check my phone. Mom wants confirmation that I'm still alive, and Asahina's entire contribution is {i}food??????{/i}"
        "Monika's two messages are waiting underneath theirs."
        python:
            _phone_messages = [
                phone_msg("them", "We're FREE! Club room for a little bit?"),
                phone_msg("them", "No studying. I mean it."),
                phone_msg("me", "I'll hold you to that."),
                phone_msg("them", "Please do."),
                phone_msg("me", "On my way."),
            ]
        call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0528_1
        "I answer Mom, then inform Asahina that dinner exists as a concept but not yet as an object."
        "{i}rude{/i} arrives before I've even reached the club hallway."
        "Down there, lockers are slamming, and the footsteps outside the club room have finally lost their exam-week hush."
        $ hide_calendar()
        scene black with wipeleft_scene
        pause 2.0
        scene bg club_day
        $ show_calendar()
        $ atmos("afternoon")
        with wipeleft_scene
        play sound moddooropen
        show monika forward uniform dist cm oe nobl rdown ldown at t11
        # NUDGE KEEP: Monika's piano scene.
        "Monika has rubbed Monday's warning off the board, though {i}POSTMORTEMS{/i} survives as a gray smudge."
        m forward uniform happ cm ce nobl rdown ldown "There. We're allowed to complain again."
        mc "Good, because I've got a queue."
        m forward uniform wry om oe nobl rdown lpoint "Oh, so have I, believe me. I just don't want to spend the whole afternoon on it."
        "The last two members head out with tired waves, leaving us the center desks and the traffic noise through the cracked windows."
        "She nudges her folder under the chair beside hers with one foot, and I sit down on that one, folder and all."
        mc "Then show me what you were listening to on the way in."
        m forward uniform curi om oe nobl rdown ldown "You saw me?"
        mc "From the stairs. You were conducting with your keys."
        "She checks the open doorway before she takes out her phone."
        m forward uniform nerv om oe awkw rdown ldown "I was {i}counting{/i}. There's a piano part I want to learn, and I keep losing track of where the left hand comes in."
        mc "Play it. I want to hear what justifies that much key movement."
        "She sets the phone between us and turns it down until we both have to lean in toward the speaker."
        "I recognize the tune as soon as the piano comes in, though only from an ad where a dog runs across a carpet."
        mc "Oh, it's the vacuum-cleaner song."
        m forward uniform anno om oe nobl rhip ldown "Please don't call it that."
        "The melody gets to the bit where the dog usually knocks something over. I try not to watch her hands."
        m forward uniform wry om oe nobl rdown ldown "You're picturing the dog, aren't you?"
        mc "He's very well trained."
        m forward uniform laug om ce nobl rdown ldown "I liked this {i}before{/i} that stupid ad! And now you've put the dog back in my head."
        "She starts it again from the passage she wants to learn, tapping out the two parts with different hands. I lose her at the third bar."
        mc "Okay, fine. That's doing a lot more than selling a vacuum."
        m forward uniform happ cm oe nobl rdown ldown "Thank you!"
        "When she finds the full recording, I turn the phone so we can both see the title."
        mc "Leave it on. I want to hear what happens after the bit I know."
        "Her fingers stop tapping once we're past that passage, and we listen while the last voices in the hall drift toward the stairs."
        $ atmos("evening")
        "When the track ends, Monika stretches both arms over her head and gets up, pocketing her phone while I put my chair back."
        m forward uniform happ cm ce nobl rdown ldown "We made it."
        mc "Yeah. We did."
        show monika forward uniform dist cm oe nobl rdown ldown
        "She rests both hands on the back of her chair and doesn't push it in right away."
        "The light across the desks has gone amber."
        "She looks over at the gray smudge on the board, then back at me."
        m forward uniform neut cm oe blus rdown ldown "Send me something to listen to on the bus?"
        mc "I've got a few. How long is the ride?"
        m forward uniform happ cm ce nobl rdown ldown "Twenty minutes. Please leave room for me to get off."
        "I start looking through my music while she checks that we've closed the windows."
        $ update_character_thought("monika", "Monika wants to learn the piano piece I know from a vacuum-cleaner ad. We listened to the full recording after exams, and she asked me to pick something for her bus ride.")
        $ hide_calendar()
        scene black with wipeleft_scene
        stop music fadeout 1.0
        pause 2.0
        scene bg dining_table_night
        $ show_calendar()
        $ atmos("home_night")
        with wipeleft_scene
        play music house_day_a
        "The smell of rice and eggs meets me at the door, and there's a stack of dessert bowls waiting on the counter. I approve of whatever that means."
        show mom determined at t22
        show asahina neut at t21
        mom "Dinner's ready. Go wash up, and I'll bring the soup over."
        ah "Finally! All I've had since second period is a granola bar."
        show mom neut
        mom "There's plenty. Take a bowl."
        show asahina neut
        "Asahina pulls out her chair, then goes back for the chopsticks before Mom has to ask."
        ah "Oh, wait--are yours over?"
        mc "Over."
        ah "Mine too."
        "We look at each other. Then she holds out a fist."
        "I bump it with mine, and she's already turning toward the table when our hands drop."
        show mom neut
        mom "Nobody asks how anybody did until after dessert. I mean it."
        mc "There's dessert?"
        show asahina shocked
        ah "Wait, where? I checked the freezer yesterday!"
        show mom smug
        mom "I {i}preserved{/i} dessert. There's a difference."
        "She opens the freezer and presents a small carton of ice cream on both palms until Asahina notices."
        show asahina happy
        ah "Oh my god!"
        mc "Behind the frozen peas. You were never going to look there."
        mom "And it waits until after dinner."
        "Dinner is eggs over rice with soup and pickles, and Asahina circles the vegetables with strategic reluctance until Mom raises one eyebrow over her bowl."
        "She takes some without comment."
        "Then she announces, apropos of nothing, that Sam sent her a sticker of a calculator on fire."
        ah teasing "That's supportive, right?"
        mom thinking "Was it meant to be encouraging?"
        ah unamused "...Probably."
        mc "Monika played me the vacuum-cleaner song. Apparently there's a whole other two minutes."
        mom curious "The one with the dog?"
        mc "Don't tell her you said that."
        "Mom hums the tune until Asahina joins in, and then they can't agree on how the next part goes."
        "From there, the conversation drifts back to whether a burning calculator is motivational."
        show mom neut
        "After dinner, Mom divides the ice cream among three bowls, and the portions are visibly uneven before the carton's even back in the freezer."
        show asahina annoyed
        ah "Hey, hold on."
        mom "You both have ice cream."
        mc "Mine's definitely bigger."
        show mom unamused
        mom "Then switch if it bothers you."
        show asahina unamused
        ah "No, because now I don't trust him. He looked at both of them way too long. That's evidence."
        show mom teasing
        mom "Both bowls are on the table. Work it out before they melt."
        "Asahina and I inspect both bowls from three angles and swap twice. We end up with the ones we started with."
        show mom happy
        "Mom eats from hers through the whole thing, watching over the rim of her spoon, and does not help."
        "When my eyes drift toward Asahina's bowl, she licks her spoon and plants it in the ice cream like a flag."
        "The first bite makes my teeth complain. I take another one anyway."
        "The dishes wait in the sink, and nobody reaches for a textbook."
        $ update_character_thought("asahina", "Asahina and I fist-bumped over surviving exams, then spent dessert trading the same two bowls of ice cream.")
        $ update_character_thought("mom", "Mom bought ice cream for morale and pretended the uneven servings did not matter. Mine was larger.")
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "My bag spends the night zipped shut by the door, and I don't go near it."
        nier "What I keep seeing instead is Monika's folder, nudged under my chair with one foot and still shut when she picked it up to leave."
        call nier_clear from _call_nier_clear_0528_6
    $ exam_guard_finish_exam_period()
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0528_1
    jump a0529

label a0528_algebra_save_scum:
    $ exam_guard_mark_scummed("algebra")
    $ calendar.set_date(2025, 5, 28)
    $ hide_calendar()
    scene black with dissolve_scene_full
    stop music fadeout 0.5
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("pressure")
    with dissolve_scene_full
    play music safety
    show math_teacher neut at t11
    math_teacher "[player]."
    "He taps my answer sheet with two fingers while the calculators around us keep clicking."
    math_teacher "Walk me through this."
    mc "I... made a mistake."
    math_teacher "Which mistake?"
    "My pencil lead snaps against the paper, and the answer I need doesn't come out with it."
    math_teacher "The answer I saw before you turned the page is gone. This one uses the restriction you missed the first time."
    math_teacher "I use you to pace this class, [player]. I {i}know{/i} what you look like when a problem has you stuck, and that wasn't it."
    mc "...I don't know."
    math_teacher "Then don't hand me an explanation you don't believe. Take the zero, and figure that part out before you try to explain it again."
    mc "Can I at least finish the other problems?"
    math_teacher "No. Algebra is done for you, so put the pencil down."
    "He moves to the next row. Somebody presses a calculator key."
    "The broken point stays caught beneath the side of my hand."
    show math_teacher at thide
    hide math_teacher
    play music hopeless fadeout 1.0
    jump a0528_after_algebra

label a0528_english_save_scum:
    $ exam_guard_mark_scummed("english")
    $ calendar.set_date(2025, 5, 28)
    $ hide_calendar()
    scene black with dissolve_scene_full
    stop music fadeout 0.5
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("pressure")
    with dissolve_scene_full
    play music safety
    show english_teacher neut at t11
    english_teacher "[player]."
    "She reaches my desk before I hear her cross the room."
    "One hand settles on the blank margin. Three nearby pencils pause, then start moving again."
    english_teacher "Paper facedown, [player]."
    "I turn it over too fast and crease it down the middle under my palm."
    mc "...Did I miss the timing?"
    english_teacher "{i}Do not.{/i}"
    english_teacher "You know the difference between revising your work in this room and replacing an answer afterward."
    english_teacher "You were doing fine on this paper, and you changed it anyway. That's why I'm angry."
    "Nobody looks up, though the silence around the nearest desks tells me they heard."
    english_teacher "Zero for this section. Leave the paper facedown."
    mc "...Can we do this outside?"
    english_teacher "No. Everyone else is still working."
    "She returns to the front, and the room's paper-and-pencil noise closes over me."
    "I can't make myself smooth out the crease under my hand."
    show english_teacher at thide
    hide english_teacher
    play music hopeless fadeout 1.0
    jump a0528_after_english
