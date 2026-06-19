label a0527:
    # --- Day 13: 2025-05-27 --
    scene bg class_day
    $ show_calendar()
    show mood_afternoon zorder 3
    with dissolve_scene_full
    play music quiz
    window auto
    # Day 2: morning Biology, afternoon Chemistry.
    $ exam_guard_checkpoint_or_jump("biology", "exam_start", "a0527_biology_save_scum")
    "Second day of exams."
    if persistent.did_save_scum_civics or persistent.did_save_scum_la:
        "Morning arrives without giving yesterday the decency to become past tense."
        "My bag is the same weight, but the straps bite harder."
        "Somewhere inside the building is a folder, an email, a note, or whatever administrative shape cheating takes when adults make it real."
        "{i}Mom knows. The office knows. Monika still does not know. That does not make it better. That makes it unevenly distributed.{/i}"
    else:
        "Morning arrives with less mystery than yesterday and more resentment."
        "My bag is the same weight, but it feels personally heavier now that two completed exams have no interest in leaving my head."
    "{i}Let's see what we have this time.{/i}"
    "To nobody's surprise, it's biology."
    "The paper starts with cell structure, then genetics, then ecology."
    "{i}Tiny systems, inherited problems, and communities changing when one piece disappears.{/i}"
    "{i}Biology has range, unfortunately.{/i}"
    show science_teacher neut at t11
    science_teacher "Same rules as yesterday. Phones away, eyes on your own paper."
    science_teacher "You may begin."
    show science_teacher at thide
    hide science_teacher
    $ exam_guard_checkpoint_or_jump("biology", "q1_open", "a0527_biology_save_scum")
    "{i}Question 1. Which organelle modifies, sorts, and packages proteins for transport out of the cell?{/i}"
    show mood_pressure zorder 4
    show vignette zorder 5 at ambient_vignette(0.24)
    with dissolve
    menu:
        "Mitochondrion.":
            hide mood_pressure
            hide vignette
            with dissolve
            "Mitochondria make ATP."
            "That is energy, not packaging."
            "{i}The powerhouse of the cell cannot do every job just because the phrase is famous.{/i}"
        "Golgi apparatus.":
            hide mood_pressure
            hide vignette
            with dissolve
            "Golgi apparatus."
            "The cell's shipping department."
            "{i}A useful organelle. Respectfully employed.{/i}"
        "Nucleus.":
            hide mood_pressure
            hide vignette
            with dissolve
            "The nucleus supervises the genetic information."
            "It is less shipping desk and more office nobody is allowed to enter without a reason."
            "{i}Golgi apparatus. I can almost hear the review guide judging me.{/i}"
    $ exam_guard_checkpoint_or_jump("biology", "q1_answered", "a0527_biology_save_scum")
    "The next page moves into heredity."
    "Punnett squares stare up at me with the smugness of boxes that know they are about to ruin somebody's morning."
    $ exam_guard_checkpoint_or_jump("biology", "q2_open", "a0527_biology_save_scum")
    "{i}Question 2. During meiosis, which two processes most directly increase genetic variation among gametes?{/i}"
    show mood_pressure zorder 4
    show vignette zorder 5 at ambient_vignette(0.24)
    with dissolve
    menu:
        "Crossing over and independent assortment.":
            hide mood_pressure
            hide vignette
            with dissolve
            "Crossing over and independent assortment."
            "Chromosomes trade pieces, then line up in different combinations."
            "{i}Messy process, useful outcome.{/i}"
        "Binary fission and budding.":
            hide mood_pressure
            hide vignette
            with dissolve
            "That belongs closer to asexual reproduction than meiosis."
            "Useful concepts, wrong process."
            "{i}Crossing over and independent assortment. Stay with meiosis.{/i}"
        "Diffusion and osmosis.":
            hide mood_pressure
            hide vignette
            with dissolve
            "Transport across membranes does not explain why gametes differ genetically."
            "Good for water, bad for this question."
            "{i}The answer is crossing over and independent assortment. Correction made.{/i}"
    $ exam_guard_checkpoint_or_jump("biology", "q2_answered", "a0527_biology_save_scum")
    "Ecology waits at the back like it is pretending not to be the part everyone reviewed last."
    $ exam_guard_checkpoint_or_jump("biology", "q3_open", "a0527_biology_save_scum")
    "{i}Question 3. Removing a keystone species from an ecosystem is most likely to cause what result?{/i}"
    show mood_pressure zorder 4
    show vignette zorder 5 at ambient_vignette(0.24)
    with dissolve
    menu:
        "No change unless the species was the largest predator.":
            hide mood_pressure
            hide vignette
            with dissolve
            "Size is not the point."
            "A keystone species matters because of its role in the system, not because it won the physical intimidation contest."
            "{i}Cascade of changes. Role beats volume.{/i}"
        "Immediate primary succession from bare rock.":
            hide mood_pressure
            hide vignette
            with dissolve
            "Primary succession starts where soil basically does not exist yet."
            "Removing one species from an existing ecosystem is not the same disaster category."
            "{i}A cascade, then. Ecology keeps its nuance.{/i}"
        "A cascade of changes across the community.":
            hide mood_pressure
            hide vignette
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
    scene bg corridor
    $ show_calendar()
    show mood_afternoon zorder 3
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
        "I refill my water bottle, buy a snack I do not strictly need, and watch a classmate flip through chemistry notes with absolute concentration."
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
    scene bg class_day
    $ show_calendar()
    show mood_afternoon zorder 3
    stop music fadeout 1.0
    with wipeleft_scene
    play music quiz
    $ exam_guard_checkpoint_or_jump("chemistry", "exam_start", "a0527_chemistry_save_scum")
    show science_teacher neut at t11
    science_teacher "Chemistry section. Calculators are permitted. Talking is not."
    "A few calculators click awake around the room."
    science_teacher "Begin."
    show science_teacher at thide
    hide science_teacher
    $ exam_guard_checkpoint_or_jump("chemistry", "q1_open", "a0527_chemistry_save_scum")
    "{i}Question 1. For the reaction N2 plus 3H2 reversibly forms 2NH3, what happens if more H2 is added at equilibrium?{/i}"
    show mood_pressure zorder 4
    show vignette zorder 5 at ambient_vignette(0.24)
    with dissolve
    menu:
        "The equilibrium shifts toward N2 and H2.":
            hide mood_pressure
            hide vignette
            with dissolve
            "That would make more reactants after adding a reactant, which is not how the stress gets reduced."
            "The system should consume added hydrogen by shifting toward ammonia."
            "{i}Le Chatelier, not wishful thinking.{/i}"
        "The equilibrium shifts toward NH3.":
            hide mood_pressure
            hide vignette
            with dissolve
            "The equilibrium shifts toward ammonia."
            "Le Chatelier's principle: add stress, system moves to reduce it."
            "{i}Chemistry is conflict management in miniature.{/i}"
        "The equilibrium constant changes immediately.":
            hide mood_pressure
            hide vignette
            with dissolve
            "Concentrations change, but the equilibrium constant stays tied to temperature."
            "Adding hydrogen shifts the position, not the value of K."
            "{i}Toward NH3. The constant stays constant.{/i}"
    $ exam_guard_checkpoint_or_jump("chemistry", "q1_answered", "a0527_chemistry_save_scum")
    "A calculation question follows, then another, then one with enough units to slow the room down."
    $ exam_guard_checkpoint_or_jump("chemistry", "q2_open", "a0527_chemistry_save_scum")
    "{i}Question 2. How does a solution with pH 3 compare to a solution with pH 4?{/i}"
    show mood_pressure zorder 4
    show vignette zorder 5 at ambient_vignette(0.24)
    with dissolve
    menu:
        "It is twice as acidic.":
            hide mood_pressure
            hide vignette
            with dissolve
            "Twice would be too merciful."
            "Each pH step changes hydrogen ion concentration by a factor of ten."
            "{i}pH 3 is ten times more acidic than pH 4.{/i}"
        "It is ten times more basic.":
            hide mood_pressure
            hide vignette
            with dissolve
            "Lower pH means more acidic, not more basic."
            "A pH of 3 is on the acidic side."
            "{i}Ten times more acidic. The scale is strict.{/i}"
        "It is ten times more acidic.":
            hide mood_pressure
            hide vignette
            with dissolve
            "Ten times more acidic."
            "The pH scale is logarithmic."
            "{i}One number, tenfold concentration.{/i}"
    $ exam_guard_checkpoint_or_jump("chemistry", "q2_answered", "a0527_chemistry_save_scum")
    "The limiting reagent problem waits near the end."
    "It is exactly the kind of question that punishes rushing."
    $ exam_guard_checkpoint_or_jump("chemistry", "q3_open", "a0527_chemistry_save_scum")
    "{i}Question 3. For 2H2 plus O2 yields 2H2O, if you have 5 moles of H2 and 2 moles of O2, which reactant limits the reaction?{/i}"
    show mood_pressure zorder 4
    show vignette zorder 5 at ambient_vignette(0.24)
    with dissolve
    menu:
        "O2.":
            hide mood_pressure
            hide vignette
            with dissolve
            "Oxygen limits it."
            "Two moles of O2 need four moles of H2. I have five, so hydrogen remains extra."
            "{i}Oxygen is the bottleneck. Stoichiometry holds still for once.{/i}"
        "H2.":
            hide mood_pressure
            hide vignette
            with dissolve
            "Hydrogen looks suspicious because there are more moles of it, but the coefficient matters."
            "Two moles of O2 only need four moles of H2, and I have five."
            "{i}Oxygen limits. Hydrogen remains in excess.{/i}"
        "Neither; they are exactly balanced.":
            hide mood_pressure
            hide vignette
            with dissolve
            "Exactly balanced would require four moles of H2 for two moles of O2."
            "Five moles of H2 leaves one mole unreacted."
            "{i}O2 is limiting. The amounts do not balance exactly.{/i}"
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
        scene bg living_room_night
        $ show_calendar()
        show mood_home zorder 3
        stop music fadeout 1.0
        with wipeleft_scene
        play music hopeless
        "The laptop stays downstairs."
        "That is the first rule I touch when I come home, because it is physical enough to obey without having to translate it."
        "Mom sits at the end of the coffee table with her work notes on one side and my algebra sheet on the other."
        show mom neut at t11
        mom "Science?"
        mc "I took it clean."
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
        show asahina neut at t22
        "She slows near the couch."
        ah "Math tomorrow?"
        mc "Yeah."
        ah "Do the one with the weird x restriction right."
        mc "...Domain restrictions?"
        ah "Sure."
        "She sets the water near me, not quite beside my hand."
        ah "Good luck with the x thing."
        show asahina at thide
        hide asahina
        show mom neut at t11
        "Mom does not comment on it."
        "Neither do I."
        "The page waits."
        "I keep working."
        show mom at thide
        hide mom
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "Tuesday night does not soften the consequence."
        nier "It gives it a table, a lamp, and enough quiet to do the next problem without pretending the week is fixed."
        call nier_clear from _call_nier_clear_0527_4_scum
    else:
        scene bg track_day
        $ show_calendar()
        show mood_evening zorder 3
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
        mc "I was not planning to."
        track_coach "Good. Twenty minutes easy. If the foot talks, you listen before it raises its voice."
        mc "Twenty easy."
        track_coach "And hydrate."
        mc "There it is."
        track_coach "There it will remain."
        show track_coach at thide
        hide track_coach
        "I start in the outside lane."
        "The first lap is stiff, not from pain but from two days of sitting in rooms where every movement felt like it might cost focus."
        "By the second lap, my shoulders remember how to drop."
        "By the third, breathing becomes something I can count without turning it into math."
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
        mc "Exam brain is not in charge."
        track_coach "I admire the ambition of that statement."
        show track_coach at thide
        hide track_coach
        "I stretch until my calves loosen."
        "The sunset catches the edge of the bleachers, making the metal look briefly soft."
        "It is not a solution."
        "It is still good to see."
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "I leave practice with my foot quiet, my shirt damp, and tomorrow's algebra still waiting."
        nier "The day has not become lighter."
        nier "It has at least remembered how to have air in it."
        call nier_clear from _call_nier_clear_0527_4
        scene bg kitchen
        $ show_calendar()
        show mood_home zorder 3
        stop music fadeout 1.0
        with wipeleft_scene
        play music dailyleisure
        "At home, the kitchen table has become a small academic triage center."
        "My algebra sheet is on one end."
        "Asahina's history notes are on the other."
        "A bowl of cut fruit sits between them like Mom is trying to bribe several subjects at once."
        show mom neut at t31
        show asahina neut at t32
        mom "Eat first. Panic second."
        ah "Can I schedule panic for after fruit?"
        mom "That was the instruction, yes."
        mc "Efficient household."
        mom "Tired household."
        "That is more accurate, so nobody corrects her."
        "Asahina flips one page over and points her pen at the margin."
        ah "If I write 'causes were complicated' for every history answer, does that count as mature nuance?"
        mom "It counts as your teacher calling me."
        ah "Mature nuance rejected."
        "She eats a slice of apple with the expression of someone accepting a temporary ceasefire."
        "I take one too."
        "For a few minutes, the table is only paper, fruit, and the little rhythm of people trying to get through the same week in different grades."
        "Mom reaches over and turns my water bottle so the cap faces me."
        "She says nothing."
        "She does not have to."
        mc "I know."
        mom "Good."
        "Asahina looks between us."
        ah "Hydration agenda."
        mc "You are next."
        ah "I refuse recruitment."
        mom "Drink water."
        ah "...Fine."
        "She drinks."
        "The victory is small, domestic, and not worth celebrating out loud."
        "Naturally, I celebrate it by not saying anything."
        show mom at thide
        hide mom
        show asahina at thide
        hide asahina
        $ update_character_thought("mom", "Mom has started communicating through water bottles, which is somehow one of her clearer parenting methods.")
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
    scene bg class_day
    $ show_calendar()
    show mood_pressure zorder 3
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
    scene bg class_day
    $ show_calendar()
    show mood_pressure zorder 3
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
