label a0527:
    # --- Day 13: 2025-05-27 --
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    with dissolve_scene_full
    play music quiz
    window auto
    # Day 2: morning Biology, afternoon Chemistry.
    $ exam_guard_checkpoint_or_jump("biology", "exam_start", "a0527_biology_save_scum")
    "Second day of exams."
    if persistent.did_save_scum_civics or persistent.did_save_scum_la:
        "Yesterday has declined to become past tense."
        "My bag is the same weight, but the straps bite harder."
        "Somewhere inside the building is a folder, an email, a note, or whatever administrative shape cheating takes when adults make it real."
        "{i}Mom knows. The office knows. Monika still does not know. That does not make it better. That makes it unevenly distributed.{/i}"
    else:
        "Less mystery than yesterday, and considerably more resentment."
        "My bag is the same weight, but it feels personally heavier now that two completed exams have no interest in leaving my head."
    "{i}Let's see what we have this time.{/i}"
    "To nobody's surprise, it's biology."
    # SFX SUGGESTION: A thick exam packet settling onto the desk with a soft paper slap.
    "The paper starts with cell structure, then genetics, then ecology."
    "{i}Tiny systems, inherited problems, and communities changing when one piece disappears.{/i}"
    "{i}Biology has range, unfortunately.{/i}"
    show science_teacher neut at t11
    science_teacher "Same rules as yesterday. Phones away, eyes on your own paper."
    science_teacher "You may begin."
    show science_teacher at thide
    hide science_teacher
    $ exam_guard_checkpoint_or_jump("biology", "q1_open", "a0527_biology_save_scum")
    "{i}Question 1a. Which organelle modifies, sorts, and packages proteins for transport out of the cell?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "Mitochondrion.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "I mark it."
        "Golgi apparatus.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "Golgi apparatus."
            "The cell's shipping department."
            "{i}A useful organelle. Respectfully employed.{/i}"
        "Nucleus.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "I mark it and move on."
    $ exam_guard_checkpoint_or_jump("biology", "q1_answered", "a0527_biology_save_scum")
    "The next page moves into heredity."
    "Punnett squares stare up at me with the smugness of boxes that know they are about to ruin somebody's morning."
    $ exam_guard_checkpoint_or_jump("biology", "q2_open", "a0527_biology_save_scum")
    "{i}Question 2a. During meiosis, which two processes most directly increase genetic variation among gametes?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "Crossing over and independent assortment.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "Crossing over and independent assortment."
            "Chromosomes trade pieces, then line up in different combinations."
            "{i}Messy process, useful outcome.{/i}"
        "Binary fission and budding.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "The pencil goes down before I can talk myself back out of it."
        "Diffusion and osmosis.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "It looks right enough at this speed."
    $ exam_guard_checkpoint_or_jump("biology", "q2_answered", "a0527_biology_save_scum")
    "Ecology waits at the back like it is pretending not to be the part everyone reviewed last."
    $ exam_guard_checkpoint_or_jump("biology", "q3_open", "a0527_biology_save_scum")
    "{i}Question 3b. Removing a keystone species from an ecosystem is most likely to cause what result?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "No change unless the species was the largest predator.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "I circle it and keep going."
        "Immediate primary succession from bare rock.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Good enough. Next question."
        "A cascade of changes across the community.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "A cascade of changes across the community."
            "One species leaves, and the whole arrangement has to admit it was less stable than it looked."
            "{i}Role matters more than appearances. Noted again.{/i}"
    $ exam_guard_checkpoint_or_jump("biology", "q3_answered", "a0527_biology_save_scum")
    "The final page asks about feedback loops and population limits."
    "I write until my hand starts making the same small complaint it made yesterday, and keep writing until the proctor calls time."
label a0527_after_biology:
    $ hide_calendar()
    scene black with wipeleft_scene
    if persistent.did_save_scum_biology:
        nier "Biology ends around me."
        nier "I do not get to feel finished because I did not finish. I was stopped."
        nier "The distinction keeps repeating itself in my head with the patience of a lab result."
    else:
        nier "Biology ends, but the morning does not feel finished."
        nier "It just folds itself into lunch and sits there beside me while I eat."
        nier "Several people attempt to diagnose the genetics section out loud. I move two seats away in defense of my central nervous system."
    call nier_clear from _call_nier_clear_0527_1
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    stop music fadeout 1.0
    with wipeleft_scene
    if persistent.did_save_scum_biology:
        play music hopeless
    else:
        play music daily
    if persistent.did_save_scum_biology:
        "The corridor has less energy today."
        "Or maybe it has the same amount and I am the one losing voltage."
        "I refill my water bottle because it gives my hands a job that is not shaking."
        "Every time someone says biology, my spine tightens."
        "{i}Mom can argue with institutions for a living, but she cannot cross-examine a security log into making me innocent.{/i}"
        "{i}Monika would ask what happened with that careful president voice, and I would have to watch the exact second she understood.{/i}"
        "{i}The honor-student version of me feels suddenly fictional. Like a profile page nobody updated after the bug report.{/i}"
        "{i}Chemistry in the afternoon. Same teacher. Same room. Same me, unfortunately.{/i}"
    else:
        "The corridor has less energy today."
        "Yesterday's panic had novelty. Today's panic has office hours."
        "I refill my water bottle and buy a snack I do not strictly need. A classmate two seats down flips through chemistry notes with absolute concentration."
        "{i}Chemistry in the afternoon.{/i}"
        "{i}One more paper before the day lets go.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    if persistent.did_save_scum_biology:
        nier "Lunch disappears without feeding anything useful."
        nier "One bell later, I am back in the same room with the same teacher, trying to look like a person who can be trusted with a calculator."
    else:
        nier "Lunch disappears through the usual administrative loopholes."
        nier "One bell later, we are back at our desks with a fresh paper and the posture of people who have been sitting too long."
    call nier_clear from _call_nier_clear_0527_2
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    stop music fadeout 1.0
    with wipeleft_scene
    play music quiz
    $ exam_guard_checkpoint_or_jump("chemistry", "exam_start", "a0527_chemistry_save_scum")
    show science_teacher neut at t11
    science_teacher "Chemistry section. Calculators are permitted. Talking is not."
    # SFX SUGGESTION: Several calculator power buttons clicking in quick succession.
    "A few calculators click awake around the room."
    science_teacher "Begin."
    show science_teacher at thide
    hide science_teacher
    $ exam_guard_checkpoint_or_jump("chemistry", "q1_open", "a0527_chemistry_save_scum")
    "{i}Question 1. For the reaction N2 plus 3H2 reversibly forms 2NH3, what happens if more H2 is added at equilibrium?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "The equilibrium shifts toward N2 and H2.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "I mark it."
        "The equilibrium shifts toward NH3.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "The equilibrium shifts toward ammonia."
            "Le Chatelier's principle: add stress, system moves to reduce it."
            "{i}Chemistry is conflict management in miniature.{/i}"
        "The equilibrium constant changes immediately.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "I mark it and move on."
    $ exam_guard_checkpoint_or_jump("chemistry", "q1_answered", "a0527_chemistry_save_scum")
    "A calculation question follows, then another, then one carrying so many units that the whole room slows down."
    $ exam_guard_checkpoint_or_jump("chemistry", "q2_open", "a0527_chemistry_save_scum")
    "{i}Question 2. How does a solution with pH 3 compare to a solution with pH 4?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "It is twice as acidic.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "The pencil goes down before I can talk myself back out of it."
        "It is ten times more basic.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "It looks right enough at this speed."
        "It is ten times more acidic.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "Ten times more acidic."
            "The pH scale is logarithmic."
            "{i}One number, tenfold concentration.{/i}"
    $ exam_guard_checkpoint_or_jump("chemistry", "q2_answered", "a0527_chemistry_save_scum")
    "The limiting reagent problem waits near the end."
    "It is exactly the sort of question that punishes rushing."
    $ exam_guard_checkpoint_or_jump("chemistry", "q3_open", "a0527_chemistry_save_scum")
    "{i}Question 3. For 2H2 plus O2 yields 2H2O, if you have 5 moles of H2 and 2 moles of O2, which reactant limits the reaction?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "O2.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "Oxygen limits it."
            "Two moles of O2 need four moles of H2. I have five, so hydrogen remains extra."
            "{i}Oxygen is the bottleneck. Stoichiometry holds still for once.{/i}"
        "H2.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "I circle it and keep going."
        "Neither; they are exactly balanced.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Good enough. Next question."
    $ exam_guard_checkpoint_or_jump("chemistry", "q3_answered", "a0527_chemistry_save_scum")
    "The last few problems blur into sig figs, reaction types, and one final multiple choice that asks me to respect solubility rules."
    "I do, barely."
label a0527_after_chemistry:
    $ hide_calendar()
    scene black with wipeleft_scene
    if persistent.did_save_scum_biology or persistent.did_save_scum_chemistry:
        nier "Day two ends without applause and with too much record-keeping."
        if persistent.did_save_scum_biology and persistent.did_save_scum_chemistry:
            nier "Two science zeros in one day only gets worse when I imagine saying it out loud."
        else:
            nier "One science zero follows me out of the classroom like it has already learned my route home."
        nier "Tomorrow is math and English."
        nier "The schedule says two subjects remain."
        nier "My head says the real exam is going to be explaining why I gave the future a reason to close its folder."
    elif persistent.exam_save_scum_subjects:
        nier "Day two ends without applause."
        nier "Biology and chemistry are clean, technically."
        nier "That word does a lot of work when the rest of the week is already carrying one ugly mark."
        nier "Tomorrow is math and English, and the only thing I can still prove is that the next answer belongs to me the first time."
    else:
        nier "Day two ends without applause."
        nier "The classroom empties more slowly than usual, like everyone is waiting for the building to confirm we are allowed to leave."
        nier "Biology and chemistry are behind me now. Tomorrow is math and English, which sounds cleaner until I remember both subjects can make simple things difficult."
    call nier_clear from _call_nier_clear_0527_3
    if exam_guard_day_scummed("biology", "chemistry"):
        call exam_guard_home_confrontation("May 27", "biology", "chemistry") from _call_exam_guard_home_confrontation_0527
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
        "The laptop stays downstairs."
        "That is the first rule I touch when I come home, because it is physical, and I can obey it without translating it first."
        "Mom sits at the end of the coffee table with her work notes on one side and my algebra sheet on the other."
        show mom neut at t11
        mom "Science?"
        mc "I took it clean."
        show mom thinking
        "She looks at me."
        "Not long enough to punish the sentence."
        "Long enough to make sure I hear myself."
        mom "Good."
        "Good is not forgiveness."
        "Tonight, it is just a fact placed carefully where a fact belongs."
        "I sit on the floor by the table and work through domain restrictions while Mom answers emails she does not discuss."
        "The living room light makes the page look flatter than it does in my bedroom."
        "Maybe that helps."
        "Less room for drama. More room for the answer to either be honest or wrong."
        "Asahina passes through once with a glass of water."
        show mom neut at t21
        show asahina curious at t22
        "She slows near the couch."
        ah "Math tomorrow?"
        mc "Yeah."
        ah "Do the one with the weird x restriction right."
        mc "...Domain restrictions?"
        ah "Sure."
        "She sets the water near me, not quite beside my hand."
        show asahina neut
        ah "Good luck with the x thing."
        show asahina at thide
        hide asahina
        show mom neut at t11
        "Mom does not comment on it."
        "Neither do I."
        "The page waits."
        "I keep working."
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "Tuesday night does not soften the consequence."
        nier "It gives it a table, a lamp, and enough quiet to do the next problem without pretending the week is fixed."
        call nier_clear from _call_nier_clear_0527_4_scum
    else:
        pause 2.0
        scene bg track_day
        $ show_calendar()
        $ atmos("evening")
        stop music fadeout 1.0
        with wipeleft_scene
        play music daily
        "Track after chemistry feels like stepping into a different language."
        "The track does not care about pH, limiting reagents, or whether I remembered independent assortment in the correct order."
        "It cares about shoes, weather, lanes, and the quiet contract between my foot and the ground."
        show track_coach neut at t11
        track_coach "[player]."
        mc "Coach."
        track_coach "Science done?"
        mc "Done."
        track_coach "Then we do not celebrate by being stupid."
        mc "I wasn't planning to."
        track_coach "Good. Twenty minutes easy. If the foot talks, you listen before it raises its voice."
        mc "Twenty easy."
        track_coach "And hydrate."
        mc "There it is."
        track_coach "There it will remain."
        show track_coach at thide
        hide track_coach
        # SFX SUGGESTION: Shoe strikes on rubber track settling into a steady jogging rhythm.
        "I start in the outside lane."
        "The first lap is stiff, not from pain but from two days of sitting in rooms where every movement felt like it might cost focus."
        "By the second lap, my shoulders remember how to drop."
        "By the third, breathing becomes something I can count instead of something I have to solve."
        "A few sprinters are doing starts near the straightaway."
        "Someone laughs after a false start, short and harmless."
        "The sound carries across the infield and disappears into the evening."
        "For twenty minutes, the day becomes physical in the plainest way possible."
        "Turn. Straight. Foot quiet. Breath steady."
        "No proving."
        "No heroic comeback."
        "Just a body allowed to do one ordinary thing after a day full of small questions."
        show track_coach neut at t11
        "Coach waves me down near the water bottles."
        track_coach "Good."
        mc "That's all?"
        track_coach "That is plenty."
        track_coach "Stretch and go home before your exam brain decides it earned extra work."
        mc "Exam brain isn't in charge."
        track_coach "I admire the ambition of that statement."
        show track_coach at thide
        hide track_coach
        "I stretch until my calves loosen."
        "The sunset catches the edge of the bleachers, making the metal look briefly soft."
        "It is not a solution."
        "It is still good to see."
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "I leave practice with my foot quiet and tomorrow's algebra still waiting."
        nier "The day has not become lighter."
        nier "It has at least remembered how to have air in it."
        call nier_clear from _call_nier_clear_0527_4
        pause 2.0
        scene bg dining_table_night
        $ show_calendar()
        $ atmos("home_night")
        stop music fadeout 1.0
        with wipeleft_scene
        play music dailyleisure
        "At home, the dining table has become a small academic triage center."
        "My algebra sheet is on one end."
        "Asahina's history notes are on the other."
        "A bowl of cut fruit sits between them like Mom is trying to bribe several subjects at once."
        show mom determined at t31
        show asahina teasing at t32
        mom "Eat first. Panic second."
        ah "Can I schedule panic for after fruit?"
        show mom smug
        mom "That was the instruction, yes."
        mc "Efficient household."
        show mom neut
        mom "Tired household."
        "That is more accurate, so nobody corrects her."
        # SFX SUGGESTION: A page flip and a light pen tap against the margin.
        show asahina smug
        "Asahina flips one page over and points her pen at the margin."
        ah "If I write 'causes were complicated' for every history answer, does that count as mature nuance?"
        show mom teasing
        mom "It counts as your teacher calling me."
        ah "Mature nuance rejected."
        show asahina unamused
        "She eats a slice of apple with the expression of someone accepting a temporary ceasefire."
        "I take one too."
        "For a few minutes, the table is only paper, fruit, and the little rhythm of people trying to get through the same week in different grades."
        show mom neut
        "Mom reaches over and turns my water bottle so the cap faces me."
        "She says nothing."
        "She does not have to."
        mc "I know."
        mom "Good."
        show asahina curious
        "Asahina looks between us."
        ah "Hydration agenda."
        mc "You're next."
        ah "I refuse recruitment."
        show mom determined
        mom "Drink water."
        show asahina unamused
        ah "...Fine."
        "She drinks."
        "The victory is small, domestic, and not worth celebrating out loud."
        "Naturally, I celebrate it by not saying anything."
        $ update_character_thought("mom", "Mom has started communicating through water bottles, which is one of her clearer parenting methods.")
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "Tuesday ends in fragments: algebra reviewed, English grammar circled, history dates muttered through the floorboards."
        nier "Nobody is done with the week."
        nier "But the house makes room for another night of trying."
        call nier_clear from _call_nier_clear_0527_5
    $ exam_guard_clear_active_checkpoint()
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0527_1
    jump a0528

label a0527_biology_save_scum:
    $ exam_guard_mark_scummed("biology")
    $ calendar.set_date(2025, 5, 27)
    $ hide_calendar()
    scene black with dissolve_scene_full
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("pressure")
    stop music fadeout 0.5
    with dissolve_scene_full
    play music safety
    show science_teacher neut at t11
    science_teacher "[player]."
    "The room pauses like even the ventilation system wants to hear the charge."
    "The teacher crouches slightly beside my desk instead of making me stand."
    science_teacher "I am going to keep my voice down because I do not think humiliating you improves the situation."
    "The restraint is too deliberate to mistake for calm."
    science_teacher "But do not confuse that with me being calm."
    mc "...Okay."
    science_teacher "You are not lost in this material."
    science_teacher "You understand systems. You understand how one dishonest input changes every result downstream."
    "My mouth goes dry."
    science_teacher "That is why I cannot grade this as a mistake."
    mc "I know."
    "I do know."
    "That is the problem."
    "If I were actually confused, there would be a place to put this feeling besides directly on myself."
    science_teacher "Good. Then you also know what happens now."
    science_teacher "Zero for biology. Paper facedown. Do not turn this into a larger disruption."
    mc "Is this...is this going on my record?"
    "My voice cracks on record."
    "The teacher's face tightens, not enough for the class to read, but enough for me."
    science_teacher "That is an administrative decision."
    science_teacher "Which means you will have to speak with people who are paid to ask questions you should have avoided creating."
    "{i}One dishonest input, and everything downstream of it comes out contaminated. I studied that exact principle this morning, and I still managed to be the contamination.{/i}"
    "{i}She's right that it's an administrative decision, but the administration I'm walking home to is a civil lawyer who reads people for a living and happens to share my last name.{/i}"
    "{i}There's no clean version of tonight, because I already ran the reaction and the product doesn't get to change its mind.{/i}"
    show science_teacher at thide
    hide science_teacher
    play music hopeless fadeout 1.0
    jump a0527_after_biology

label a0527_chemistry_save_scum:
    $ exam_guard_mark_scummed("chemistry")
    $ calendar.set_date(2025, 5, 27)
    $ hide_calendar()
    scene black with dissolve_scene_full
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("pressure")
    stop music fadeout 0.5
    with dissolve_scene_full
    play music safety
    show science_teacher neut at t11
    science_teacher "[player]."
    "The teacher's hand lands on the corner of my answer sheet -- not hard, just enough pressure to keep the paper from going anywhere."
    if persistent.did_save_scum_biology:
        science_teacher "After this morning, I was hoping the afternoon would be uneventful."
        "The disappointment in that sentence is worse than a second accusation."
    else:
        science_teacher "I gave you a calculator because this section requires tools."
        science_teacher "Tools are not loopholes."
    mc "...Right."
    science_teacher "You are capable of doing this work honestly."
    science_teacher "That is the part making me angry, not the score."
    "The word {i}angry{/i} is almost swallowed before it reaches the room, but it makes the last few inches out loud."
    science_teacher "A wrong answer would have told me what to teach next."
    science_teacher "This tells me I have to stop the section."
    mc "I get it."
    "I do not sound like I get it."
    "I sound like someone trying not to throw up on a lab table."
    science_teacher "Then calculator off."
    science_teacher "Zero for chemistry."
    mc "Please don't call my mom during the day."
    "That sentence is out before I can murder it."
    "The teacher stares at me."
    science_teacher "That is not what you should be worried about first."
    "It is, though, and not because it matters most. It's the part of this with a face attached -- a kitchen, a couch, the question of how I walk back into a house I've spent three days lying inside of."
    "{i}A controlled reaction would have needed control from me first, and I had the formula sitting right in front of me when I picked the version that goes off.{/i}"
    show science_teacher at thide
    hide science_teacher
    play music hopeless fadeout 1.0
    jump a0527_after_chemistry
