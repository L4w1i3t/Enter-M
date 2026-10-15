label a0527:
    # --- Day 13: 2025-05-27 --
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    with dissolve_scene_full
    play music exam
    # Day 2: morning Biology, afternoon Chemistry.
    $ exam_guard_checkpoint_or_jump("biology", "exam_start", "a0527_biology_save_scum")
    "The room is full twenty minutes early, and every new arrival gets drafted into the genetics argument."
    "My desk catches my wrist in the same spot as yesterday, so I shove the pencil case over and give my arm the extra inch."
    if persistent.did_save_scum_civics or persistent.did_save_scum_la:
        "Mom's spare eraser is still the whitest thing in my pencil case."
        "I zip it out of sight while the last few seats fill."
    else:
        "Day two, at least, I know the drill: bag up front, paper facedown, and somebody coughing all the way through the instructions."
    # SFX SUGGESTION: A thick exam packet settling onto the desk with a soft paper slap.
    "The biology packet lands facedown with a soft, heavy slap, and I don't love what that says about the page count."
    show science_teacher neut at t11
    science_teacher "Same rules as yesterday, everyone. Phones away, eyes on your own paper."
    science_teacher "And read what the figures {i}actually{/i} establish. Naming an organelle isn't a senior biology answer."
    science_teacher "Use the data we've given you. If it can't settle something, say so. That counts as an answer too."
    science_teacher "You may begin."
    show science_teacher at thide
    hide science_teacher
    "I flip through it once: cells up front, genetics in the middle, ecology at the back, and a worrying amount of blank space under the long answers."
    $ exam_guard_checkpoint_or_jump("biology", "q1_open", "a0527_biology_save_scum")
    "{i}Question 1a. Labeled hormone appears in the rough ER of normal and treated cells at two minutes.{/i}"
    "{i}Only normal cells show it in the Golgi at ten minutes, and in the medium at thirty.{/i}"
    "{i}Which conclusion is best supported?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "The Golgi itself failed, because treated hormone never appears there.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "{i}Golgi{/i} is the label that grabs my eye first, so I mark it."
            "Then I trace the route again and find the treated signal vanishing earlier than that."
        "Synthesis begins, but ER-to-Golgi trafficking fails at an unidentified step.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "The hormone gets made and reaches the rough ER, then drops off the map somewhere short of the Golgi. That's as far as the evidence lets me pin it down."
        "Secretion is normal, but an extracellular enzyme destroys the hormone.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Nothing ever reaches the medium, so something chewing the hormone up outside the cell sounds plausible."
            "...Right up until the missing Golgi signal, which I blow straight past."
    $ exam_guard_checkpoint_or_jump("biology", "q1_answered", "a0527_biology_save_scum")
    "On to the testcross. I total its four columns in the margin before I let myself look at the answers."
    $ exam_guard_checkpoint_or_jump("biology", "q2_open", "a0527_biology_save_scum")
    "{i}Question 2a. A testcross produces 188 brown-long, 192 white-short, 62 brown-short, and 58 white-long offspring.{/i}"
    "{i}Which interpretation is best supported?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "The genes are linked: about 24 percent recombinant and 24 map units apart.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "The two small columns make one hundred twenty out of five hundred, so recombination lands at {i}twenty-four percent{/i}, and so does the map distance."
        "The genes assort independently because all four phenotypes appear.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "All four combinations show up, and my pencil's already moving before I've compared the heights of the columns."
        "The genes are linked about 76 map units apart because the parental classes total 76 percent.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "The parental classes dominate, and seventy-six percent is already sitting there in my arithmetic. I make the bigger share the map distance and keep moving."
    $ exam_guard_checkpoint_or_jump("biology", "q2_answered", "a0527_biology_save_scum")
    "Somebody behind me lets out a sigh with real feeling in it. I turn to ecology carefully, since the staple is one rough flip from tearing through the corner."
    $ exam_guard_checkpoint_or_jump("biology", "q3_open", "a0527_biology_save_scum")
    "{i}Question 3b. After a low-biomass grazer is removed, algal cover rises from eighteen to seventy-six percent and observed species fall from twelve to five.{/i}"
    "{i}Measured temperature and salinity remain similar.{/i}"
    "{i}Which conclusion is strongest?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "The removal proves the grazer alone caused every observed community change.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Steady temperature and salinity hold my attention longer than the word {i}measured{/i} does. I mark {i}alone{/i}."
        "The grazer cannot matter because its original biomass was small.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "With the clock ticking over my head, low biomass starts looking a lot like low influence. I ignore how big the change was."
        "The grazer had a disproportionate effect, though unmeasured factors remain possible.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "A small grazer and a huge change belong in the same sentence, but {i}measured{/i} keeps the conclusion one step short of proof."
    $ exam_guard_checkpoint_or_jump("biology", "q3_answered", "a0527_biology_save_scum")
    "By the last long response, on population limits, I'm bearing down on the pencil again. I loosen my grip and finish with just enough time to read the whole thing back."
label a0527_after_biology:
    $ hide_calendar()
    scene black with wipeleft_scene
    if persistent.did_save_scum_biology:
        nier "The bell goes, and the room packs up around me while I'm still staring at the same blank page."
        nier "I can't even pretend I ran out of time."
    else:
        nier "The bell lets us out into a lunch break that runs entirely on vending-machine sugar and resentment."
    call nier_clear from _call_nier_clear_0527_1
    stop music fadeout 1.0
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    if persistent.did_save_scum_biology:
        play music hopeless
    else:
        play music day_c
    if persistent.did_save_scum_biology:
        "I take my time at the fountain and keep both hands wrapped around my bottle. Every mention of biology tightens my grip."
        "{i}If Monika asks, I'll have to stand there and watch her understand.{/i}"
    else:
        "By the windows, a guy from two seats down asks me whether the testcross distance was twenty-four or seventy-six. I tell him biology and I aren't speaking right now."
        "Undeterred, he adds up the columns on the back of his hand. Then he stares at the total and whispers 'shit' to his own knuckles."
    $ hide_calendar()
    scene black with wipeleft_scene
    if persistent.did_save_scum_biology:
        nier "The bell catches my lunch mostly untouched."
        nier "Back in the same room, with the same teacher, I set my calculator flat on the desk before she reaches my row."
    else:
        nier "Lunch lasts about six minutes in my head. Then the bell puts us back at the same desks like the morning never ended."
    call nier_clear from _call_nier_clear_0527_2
    stop music fadeout 1.0
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music exam
    $ exam_guard_checkpoint_or_jump("chemistry", "exam_start", "a0527_chemistry_save_scum")
    show science_teacher neut at t11
    if persistent.did_save_scum_biology:
        "She hands out the chemistry papers and saves mine for last, keeping her hand flat on it until I look up."
        science_teacher "You may {i}still{/i} sit this section. After this morning, though, I have to supervise you differently."
        science_teacher "Calculator flat on the desk. If you need anything, raise your hand and wait for me to come to you."
        mc "...Understood."
        "It comes out as mostly breath. I take another one, then make myself look down at the paper under her hand."
    science_teacher "Chemistry section. Calculators are permitted. Talking is {i}not{/i}."
    # SFX SUGGESTION: Several calculator power buttons clicking in quick succession.
    "Calculators click awake across the room in a ragged little chorus, with mine coming in last."
    science_teacher "Begin."
    show science_teacher at thide
    hide science_teacher
    $ exam_guard_checkpoint_or_jump("chemistry", "q1_open", "a0527_chemistry_save_scum")
    "{i}Question 1. For A gas plus B gas reversibly forming two C gas, some C is removed at constant temperature.{/i}"
    "{i}The reaction quotient falls below the equilibrium constant.{/i}"
    "{i}What happens next?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "The system shifts left and the equilibrium constant decreases.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Removing product feels like pulling the reaction backward, so I let that first tug decide which way the whole system has to go."
        "The system shifts right until the quotient reaches the unchanged equilibrium constant.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "With the quotient under the constant, the reaction runs right until the two match again. Nobody touched the temperature, so the constant stays exactly where it was."
        "Nothing shifts because equilibrium had already been reached.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "{i}Equilibrium{/i} sounds like a finished state, so I treat it as permanent, never mind that somebody just disturbed the concentrations."
    $ exam_guard_checkpoint_or_jump("chemistry", "q1_answered", "a0527_chemistry_save_scum")
    "A page of calculations later, I reach a pH comparison with two numbers and nothing to punch in. I read it twice anyway."
    $ exam_guard_checkpoint_or_jump("chemistry", "q2_open", "a0527_chemistry_save_scum")
    "{i}Question 2. Equal volumes of solution A at pH 2.5 and solution B at pH 3.5 are tested.{/i}"
    "{i}Their compositions are not reported.{/i}"
    "{i}Which conclusion is justified?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "A contains exactly ten times as many total acid molecules as B.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "The familiar factor of ten is already in my head, so I hang it on total acid and never stop to ask what pH is actually counting."
        "B has ten times A's hydrogen-ion concentration.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Three-point-five is the bigger number. I let the scale run the intuitive way and forget, for exactly one answer, what pH measures."
        "A has ten times B's hydrogen-ion concentration, but total acid remains unknown.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "One pH unit means a tenfold difference in hydrogen-ion concentration, and nothing in the question lets me stretch that into total acid."
    $ exam_guard_checkpoint_or_jump("chemistry", "q2_answered", "a0527_chemistry_save_scum")
    "Near the end sits a limiting-reagent problem, the classic spot for one hurried ratio to quietly wreck everything after it. I make myself slow down."
    $ exam_guard_checkpoint_or_jump("chemistry", "q3_open", "a0527_chemistry_save_scum")
    "{i}Question 3. For two SO2 plus O2 yielding two SO3.{/i}"
    "{i}0.60 moles of SO2 and 0.40 moles of O2 produce 0.45 moles of SO3.{/i}"
    "{i}Which reactant limits the reaction, and what is the percent yield?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "SO2 limits. Theoretical product is 0.60 moles and yield is 75 percent.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "Six-tenths of SO2 only needs three-tenths of oxygen, so sulfur dioxide runs out first."
            "Point four-five over point six. Seventy-five percent."
        "O2 limits. Theoretical product is 0.80 moles and yield is 56.25 percent.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Four-tenths of oxygen could make eight-tenths of product, and I stop right there, never checking whether the sulfur dioxide can hold up its end."
        "Neither limits because the starting amounts are close. Yield is 75 percent.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "The starting amounts look almost cooperative, and a tidy seventy-five percent talks me out of checking which reactant runs out first."
    $ exam_guard_checkpoint_or_jump("chemistry", "q3_answered", "a0527_chemistry_save_scum")
    "The rest of the packet blurs into reaction types and significant figures, with solubility taking one last swing at me on the final page."
label a0527_after_chemistry:
    $ hide_calendar()
    scene black with wipeleft_scene
    if persistent.did_save_scum_biology or persistent.did_save_scum_chemistry:
        nier "When the bell rings, I pack my calculator twice, because my hands keep putting it in the wrong pocket."
        if persistent.did_save_scum_biology and persistent.did_save_scum_chemistry:
            nier "Two science zeros in {i}one day{/i}. It sounds worse every time I imagine saying it out loud."
        else:
            nier "One zero in science, and every time I close my eyes, there it is."
        nier "Math and foreign language are still tomorrow."
        nier "My head keeps skipping ahead to the part where I tell Mom exactly what I did."
    elif persistent.exam_save_scum_subjects:
        nier "Day two ends without applause. Biology and chemistry are both {i}clean{/i}, in the narrowest sense of the word."
        nier "Whatever happened yesterday walks out into the hallway right beside me."
        nier "Tomorrow's two papers can only show what I do with the next answer."
    else:
        nier "Day two ends without applause, just slow chair scrapes and tired hands collecting calculators."
        nier "Biology and chemistry go in my bag, and tomorrow's page is down to math and foreign language."
    call nier_clear from _call_nier_clear_0527_3
    if not persistent.exam_save_scum_subjects:
        pause 2.0
        scene bg corridor
        $ show_calendar()
        $ atmos("afternoon")
        with dissolve_scene_full
        # NUDGE KEEP (P1.8): the second exam-hallway scene to keep.
        "Outside the room, the first argument is already about the pH question."
        "One classmate is insisting on ten times more acid, while the other keeps tapping his notes and saying {i}hydrogen-ion concentration{/i} a little louder every time."
        "Then they both spot me and swing around in unison."
        mc "No. You can both be haunted independently."
        "The second guy points at me like I just endorsed him."
        "I keep walking and let the first one take his case to a higher court."
        $ hide_calendar()
        scene black with wipeleft_scene
    if exam_guard_day_scummed("biology", "chemistry"):
        call exam_guard_home_confrontation("May 27", "biology", "chemistry") from _call_exam_guard_home_confrontation_0527
    if exam_guard_should_bad_end():
        jump exam_guard_bad_ending
    if exam_guard_day_scummed("biology", "chemistry"):
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "Tuesday closes with my phone downstairs and two exams still left on the calendar."
        nier "I set the clock on my desk and open the algebra review, and every creak from the floor below stops my pencil."
        nier "Nothing I write tonight shrinks what happened in science, and tomorrow's paper still opens on time."
        call nier_clear from _call_nier_clear_0527_4_new_scum
    elif persistent.exam_save_scum_subjects:
        stop music fadeout 1.0
        pause 2.0
        scene bg living_room_night
        $ show_calendar()
        $ atmos("home_night")
        with wipeleft_scene
        play music hopeless
        "The laptop lives downstairs now. Of all the new rules, it's the easiest to keep: I set it on the coffee table and nobody needs an explanation."
        "Mom is at the other end with her work notes on one side and my algebra sheet on the other, and when I sit down, she slides the sheet clear of her keyboard."
        show mom worried at t11
        mom "Science...?"
        mc "Clean. Both of them. I didn't change anything."
        show mom determined
        "Her eyes catch mine, and I make myself hold them until she's the one who looks back down."
        show mom sad
        mom "...Good."
        "I sit on the floor by the table and work through domain restrictions while she answers emails she doesn't talk about."
        "Whenever I rub out a line, her typing stops. I leave the next correction visible."
        "Asahina wanders through while I'm grinding a pencil in the sharpener and digs a mechanical one out of her pocket."
        show mom sad at t21
        show asahina curious at t22
        ah "Math tomorrow, right?"
        mc "Yeah."
        show asahina unamused
        ah "Use this. That noise is driving me up the wall."
        mc "You sure?"
        ah "It's a pencil. Bring it back."
        "She rolls it across the table, and it comes to rest against the algebra sheet, right between Mom and me."
        show asahina neut
        ah "And don't chew it!"
        show asahina at thide
        hide asahina
        show mom determined at t11
        "Mom goes back to her email, and I do the next problem with Asahina's pencil. The lead clicks once. Mom keeps typing."
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "Tuesday night runs past eleven on pencil scratches and Mom's keyboard."
        nier "I finish the page before either sound stops."
        call nier_clear from _call_nier_clear_0527_4_scum
    else:
        stop music fadeout 1.0
        pause 2.0
        scene bg track_evening
        $ show_calendar()
        $ atmos("evening")
        with wipeleft_scene
        play music day_c
        "I want to run before I'm even at the track, and getting out of my uniform feels better than finishing chemistry did."
        "Late heat is still coming up off the rubber, and somebody's cleats tick along the concrete by the equipment shed."
        "My foot stays quiet while I lace up. I test my weight on it once, just in case, then cross over to Coach."
        show track_coach neut at t11
        track_coach "[player]."
        mc "Coach."
        track_coach "Science done?"
        mc "Done. Can I run now?"
        track_coach "Then don't celebrate by being stupid."
        mc "Wasn't planning to."
        track_coach "All right, twenty minutes easy. If the foot starts talking, listen before it has to raise its voice."
        mc "Twenty easy."
        track_coach "And yes, you still have to hydrate."
        mc "Knew the water speech was coming."
        track_coach "It always is."
        show track_coach at thide
        hide track_coach
        # SFX SUGGESTION: Shoe strikes on rubber track settling into a steady jogging rhythm.
        "I start out stiff in the outside lane, but by the second lap my shoulders have come down and my breathing has started running itself."
        "Down the straightaway, a few sprinters are practicing starts, cleats biting and letting go, until somebody jumps the gun and the rest of them chase him across the infield, laughing and trying to pants him."
        "The laughing carries all the way to the curve, where a headwind grabs my shirt. I lean into it and hold the pace."
        "I could happily go another few laps by the time Coach's whistle goes at twenty minutes."
        show track_coach neut at t11
        "He waves me toward the water bottles while I jog the last few steps down to a walk."
        track_coach "That's twenty!"
        mc "That's all?"
        track_coach "That is {i}plenty{/i}. Stretch, drink, and go home before your exam brain decides it's earned extra work."
        mc "Exam brain isn't in charge here."
        track_coach "Sure. Keep telling it that while you stretch."
        show track_coach at thide
        hide track_coach
        "I stretch by the water bottles while the sunset climbs the bleachers, and by the time I stand up, the last of the light has retreated to the top row."
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "I leave practice with my foot quiet and the last lap cooling out of my shirt."
        nier "Running has shrunk tomorrow's algebra back down to the size of the packet in my bag."
        call nier_clear from _call_nier_clear_0527_4
        pause 2.0
        scene bg store_checkout
        $ show_calendar()
        $ atmos("evening")
        with wipeleft_scene
        # NUDGE KEEP: the Kotonoha cold-pack scene. "Six papers in three days" is a Chapter 5 seed.
        "The corner store on the way home stocks four of everything and eleven of the wrong thing."
        "I go in for water and end up in front of the first-aid shelf, doing arithmetic about my own hand."
        show kotonoha work neut at t11
        "Kotonoha is two aisles down, hanging battery packs on a hook with her sleeves pushed to the elbow."
        ko "Good evening."
        mc "Hey. Is there a small cold pack anywhere? All I'm finding are the enormous ones."
        ko "Second shelf, beside your hand."
        "She squares the last three packs on the hook and comes around the end of the aisle."
        show kotonoha work curious
        ko "Is it for your foot?"
        mc "Nah, the foot's fine."
        ko "What hurts?"
        mc "My hand, from writing. I just came from track, and somehow {i}that's{/i} the injury I'm bringing home."
        show kotonoha work neut
        ko "Six papers in three days is a lot of writing."
        mc "And the last two are tomorrow."
        ko "I know. We've nearly sold out of pens."
        "She takes a box off the second shelf and holds it out. Instant cold pack, cheapest one, nothing on the front but instructions."
        ko "Check the directions before you open it. This one's single use."
        mc "Then I'd better get a whole exam's worth out of it. Thanks."
        "She takes the water off me while I'm reading the side of the box and rings them up together."
        ko "Do you need a bag?"
        mc "No, I've got room."
        show kotonoha work pose_exact_fold
        "The receipt comes out crooked. She squares it against the counter before she folds it."
        show kotonoha work neut
        ko "The water is cheaper if you buy two."
        mc "I'll stick with one. I'd have to carry the savings home."
        show kotonoha work neut
        ko "Good luck tomorrow."
        mc "You too. Uh... enjoy the rest of your shift."
        ko "Thank you."
        show kotonoha at thide
        hide kotonoha
        "By the time I reach the door, she's back at the battery hook."
        $ hide_calendar()
        scene black with wipeleft_scene
        stop music fadeout 1.0
        pause 2.0
        scene bg dining_table_night
        $ show_calendar()
        $ atmos("home_night")
        with wipeleft_scene
        play music house_day_a
        "Asahina has buried her end of the dining table in history notes, leaving my end just enough room for the algebra sheet Mom found on the couch."
        "A bowl of cut fruit holds down the only patch of table neither of us has claimed."
        show mom determined at t22
        show asahina teasing at t21
        mom "Eat first. If you still need to panic afterward, the material will wait. It's had all semester to practice."
        ah "So I can reschedule my panic for after the fruit?"
        show mom smug
        mom "That was the instruction, yes."
        mc "See? Efficient household."
        show mom frustrated
        mom "We're a {i}tired{/i} household. Eat."
        show mom neut
        "Asahina drops her pen onto the page as I reach for the fruit. Mom doesn't take a slice for herself until both of us have one."
        # SFX SUGGESTION: A page flip and a light pen tap against the margin.
        show asahina smug
        "Asahina flips a page and taps her pen against one sentence in the margin."
        ah "Okay, real question. If I write 'the causes were complicated' on every single history answer, is that mature nuance, or do I actually need dates?"
        show mom teasing
        mom "It counts as your teacher calling me to ask whether you studied."
        ah "Fine, but I'm keeping the sentence. It took me, like, ten minutes."
        "Under that sentence, she's chained four dated events together with arrows and crammed a real explanation into the margin. When I lean over to read the last line, her wrist slides over it."
        mc "You already wrote the actual answer, though."
        show asahina unamused
        ah "I know. I'm trying to make it shorter."
        "She bites into an apple slice and keeps glaring at me while she chews."
        "By my third domain restriction, half the fruit is gone and her history dates have started migrating into every margin she owns."
        show mom neut
        "Mom moves my water out from behind the textbook to make room for her own notes, then settles in with us."
        show asahina curious
        "Asahina takes a drink and rereads her margin, and I get busy with the next problem so she can't ask me how much of her answer to cross out."
        show asahina at thide
        hide asahina
        show mom neut at t11
        "Around eleven, she hauls her history upstairs. Mom stays where she is, deep in her own notes."
        "It's twelve-forty by the time I finish the algebra review, with the cold pack gone lukewarm on my wrist."
        "My transit card is lying next to my keys, and the yellow note on it has started to curl at one corner. I take a picture of it and send it to Monika."
        python:
            _phone_messages = [
                phone_msg("me", "Going to bed, as instructed."),
                phone_msg("them", "Look at you, actually following it!"),
                phone_msg("them", "I'm literally on the last section of my folder, and then I'm following it too."),
                phone_msg("me", "No midnight review spirals, right?"),
                phone_msg("them", "This isn't a spiral! It's a very organized loop~"),
                phone_msg("them", "Now go to sleep! You have algebra in, like, seven hours!"),
            ]
        call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0527_1
        $ update_character_thought("mom", "Mom put out fruit while we reviewed and moved my water aside to make room for her own work.")
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "Tuesday ends on the stairs, between Mom's page turns below me and Asahina muttering history dates somewhere above."
        call nier_clear from _call_nier_clear_0527_5
    # Keep a guarded handoff through the overnight/opening transition. A save
    # made before tomorrow's exam_start must still point at the upcoming paper.
    $ exam_guard_checkpoint_or_jump("algebra", "day_ready", "a0528_algebra_save_scum")
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0527_1
    jump a0528

label a0527_biology_save_scum:
    $ exam_guard_mark_scummed("biology")
    $ calendar.set_date(2025, 5, 27)
    $ hide_calendar()
    scene black with dissolve_scene_full
    stop music fadeout 0.5
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("pressure")
    with dissolve_scene_full
    play music safety
    show science_teacher neut at t11
    science_teacher "[player]."
    "Pencils keep scratching. She crouches beside my desk instead of making me stand, one hand flat against its edge."
    science_teacher "Leave the paper where it is, please. I'll be collecting it."
    mc "I thought..."
    "I can't find an ending for that sentence that makes it any better."
    science_teacher "You are {i}not{/i} lost in this material, [player]. Don't ask me to grade this like a mistake."
    science_teacher "Biology is a zero. Turn the paper over."
    "I flip it too fast, and the sheet skids halfway off the desk. She catches the corner and lays it back down, as quiet as ever."
    mc "Do I... leave?"
    science_teacher "No. You stay in your seat until the bell."
    "She stands. The room keeps working."
    "I stare at the blank back of the page and don't trust myself to move."
    show science_teacher at thide
    hide science_teacher
    play music hopeless fadeout 1.0
    jump a0527_after_biology

label a0527_chemistry_save_scum:
    $ exam_guard_mark_scummed("chemistry")
    $ calendar.set_date(2025, 5, 27)
    $ hide_calendar()
    scene black with dissolve_scene_full
    stop music fadeout 0.5
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("pressure")
    with dissolve_scene_full
    play music safety
    show science_teacher neut at t11
    science_teacher "[player]."
    "Her hand settles on the corner of my answer sheet and holds it still under my pencil."
    "Two desks over, somebody keeps balancing an equation."
    if persistent.did_save_scum_biology:
        science_teacher "After this morning, I really thought we'd get through the afternoon without doing this again."
        "I look down before she reaches the last word."
    else:
        science_teacher "The calculator's there because this section needs one. It doesn't explain why your answer changed."
    mc "...Right."
    science_teacher "I'd have gone through a wrong answer with you afterward. You know that."
    "She presses the corner of the sheet flat while I keep staring at the calculator."
    science_teacher "Now I have to stop your section."
    mc "I... I get it."
    science_teacher "Then turn the calculator off."
    "My thumb hits equals instead, and the display changes one last time before I find the off button."
    science_teacher "Chemistry is a zero."
    mc "Please don't call my mom--not during the day."
    "The teacher keeps looking at me."
    "I want the sentence back, and there's nowhere to put it."
    science_teacher "The school will contact her today. I can't promise you a time."
    "{i}Mom's at work. She'll answer if the school calls.{/i}"
    "Around us, everyone else's pencils keep moving while mine lies beside the dark calculator."
    show science_teacher at thide
    hide science_teacher
    play music hopeless fadeout 1.0
    jump a0527_after_chemistry
