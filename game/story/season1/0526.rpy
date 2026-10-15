label a0526:
    # --- Day 12: 2025-05-26 --
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music house_day_a
    "I eat breakfast with my pencil case open beside the bowl, counting pens between bites. Three. Still three. I leave them alone."
    show mom uniform neut at t22
    show asahina uniform unamused at t21
    "Mom reaches across the table and drops a clean white eraser into the case, right next to the one I packed last night."
    mc "I {i}did{/i} pack one, you know."
    mom "I know. Now if you lose one, it's annoying instead of a crisis."
    show asahina uniform annoyed
    ah "Hey, where's mine? He already {i}had{/i} one!"
    show mom uniform unamused
    mom "Front pocket of your bag. Please try to bring this one home in one piece."
    ah "The pieces still work!"
    mc "Collectively."
    "Asahina kicks my ankle under the table, then sizes up the pencil case like she's planning a demonstration. I pull it out of range."
    "The spare eraser settles against the zipper, too white to get lost among everything I've already used."
    $ hide_calendar()
    scene black with wipeleft_scene
    "Asahina's transit card turns up under a shoe ten minutes after Mom leaves. She swears at the shoe and still makes it out the door ahead of me."
    pause 2.0
    scene bg residential_day
    $ show_calendar()
    $ atmos("morning")
    with wipeleft_scene
    "Two doors down, somebody is losing an argument with a car that won't start."
    if s1_slept_in:
        "{i}Up before every alarm this morning. I'd tell somebody, but then I'd have to explain why that's news.{/i}"
    "Asahina is at the crossing with her bag on one shoulder and the signal already against her."
    show asahina uniform annoyed at t11
    ah "Don't."
    mc "I haven't said a word."
    ah "You were {i}winding up{/i}. I could hear it from here."
    mc "Did the shoe apologize?"
    show asahina uniform frustrated
    ah "Okay, your card's sleeping in my sweatiest shoe tonight. We'll see who's laughing in the morning."
    "The light changes, and she lets everybody else at the curb go first."
    mc "For somebody who beat me out the door, you're in no hurry."
    show asahina uniform neut
    ah "First-years have tests this week too, you know. It's not just the senior show."
    mc "I did know that."
    ah "Then act like it."
    "She says it to the crosswalk instead of to me."
    show asahina uniform curious
    ah "Are senior exams way worse than ours? Be honest."
    mc "Longer answers, mostly. And a lot more explaining why the obvious answer is a trap."
    show asahina uniform teasing
    ah "Oh, you'd {i}love{/i} that."
    mc "Only when nobody's making me write it down."
    "She punts a loose pebble ahead of us."
    show asahina uniform unamused
    ah "Ugh, I'd take another serving drill over this. At least those end when the whistle blows."
    mc "So does an exam."
    ah "Yeah, but you can still be stuck on question two when it does."
    "At the shopping street she stops to dig through the front pocket of her bag, then zips it shut again with nothing in her hand."
    show asahina uniform neut
    ah "I'll get something at school."
    mc "You packed."
    ah "I packed a {i}tangerine{/i}."
    mc "That's technically packing."
    show asahina uniform annoyed
    ah "It's technically nothing! Go take your stupid test."
    "She speeds up until the gap between us stops being a conversation."
    show asahina at thide
    hide asahina
    if s1_was("asahina_plate", "named"):
        "The last time I had an opinion about her plate, I called it a garnish and got cross-examined on whether portions are a crime."
    elif s1_was("asahina_plate", "joke"):
        "{i}Bold move, bringing one tangerine to a three-day siege.{/i}"
        "My extra-mirin joke at that dinner bought me exactly one \"Cool,\" so this one stays in my pocket."
    else:
        "When Mom asked about her tiddly-wink of rice that night, I drank my water and stayed out of it."
    "She crosses with the next clump of students, and I let the gap stand."
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 1.0
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    with dissolve_scene_full
    play music exam
    # Three days of exams. Day 1: morning Civics, afternoon Language Arts.
    #
    # May 25 carries the in-world academic-integrity cue. Start the guard before
    # the first checkpoint without interrupting the paper for a mechanics warning.
    "Nobody talks while the civics teacher counts out papers row by row, and a knee two seats over is drumming against the underside of a desk."
    show civics_teacher neut at t11
    civics_teacher "All right, phones away. Bags at the front."
    "Somebody behind me picks that exact moment to cough up a lung."
    civics_teacher "You may begin when the bell rings."
    "My paper arrives facedown with one corner curling up, and I pin it flat under my palm while we wait."
    show civics_teacher at thide
    hide civics_teacher
    $ exam_guard_begin_exam_period()
    $ exam_guard_checkpoint_or_jump("civics", "exam_start", "a0526_civics_save_scum")
    # SFX SUGGESTION: A stark exam bell with no crowd noise following it.
    "The bell cuts through the room."
    "I turn the paper over and file my cold fingertips under bad circulation."
    $ exam_guard_checkpoint_or_jump("civics", "q1_open", "a0526_civics_save_scum")
    "{i}Question 1. A referendum passes with seventy-two percent support and bars one religious group from renting public halls open to everyone else.{/i}"
    "{i}A court invalidates it.{/i}"
    "{i}Which defense of the ruling is strongest?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "Federalism gives local voters exclusive control of local property.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "The halls belong to the city, and {i}local{/i} sounds like the whole answer."
            "I let that one word carry my pencil to the first option before the rest of the facts catch up."
        "Constitutional rights limit majorities. Judicial review enforces that limit.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "Seventy-two percent is {i}support{/i}, not immunity, and winning the vote doesn't put the majority beyond a constitutional limit."
        "Popular sovereignty makes any valid referendum immune from review.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "My pencil pauses over {i}popular sovereignty{/i}. Seventy-two percent looks decisive when I stop reading there."
    $ exam_guard_checkpoint_or_jump("civics", "q1_answered", "a0526_civics_save_scum")
    "The next page gives the national government one column and the regions another, then lets a river cross between them."
    $ exam_guard_checkpoint_or_jump("civics", "q2_open", "a0526_civics_save_scum")
    "{i}Question 2. The national legislature sets minimum water-quality standards for rivers.{/i}"
    "{i}Regions may enact stricter limits and use their own inspectors, while a national agency handles cross-border violations.{/i}"
    "{i}Which analysis is best supported?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "Separation of powers: lawmakers set the standard and an agency enforces it.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "I circle separation of powers after spotting lawmakers and an agency, then notice the regional inspectors in the next line."
        "Federalism: national and regional governments retain distinct, overlapping roles.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "The national rule is only a floor. Regional lawmakers and inspectors keep room to impose and enforce stricter limits of their own."
        "Preemption: the national standard automatically bars stricter regional limits.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "I see {i}national{/i} and assume it clears the field, handing the minimum standard more force than the facts ever gave it."
    $ exam_guard_checkpoint_or_jump("civics", "q2_answered", "a0526_civics_save_scum")
    # SFX SUGGESTION: A wooden pencil clattering once against the hard classroom floor.
    "A pencil drops somewhere behind me and rolls until a desk leg stops it. Nobody looks up to claim it."
    $ exam_guard_checkpoint_or_jump("civics", "q3_open", "a0526_civics_save_scum")
    "{i}Question 3. A licensing board suspends a nurse based on an undisclosed complaint.{/i}"
    "{i}It announces the suspension without showing the evidence or offering a hearing.{/i}"
    "{i}What is the strongest constitutional concern?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "The board's expertise makes the procedure sufficient.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "The word {i}expertise{/i} gives me somewhere easy to stop."
            "I mark it, then go back to the missing complaint and the missing hearing."
        "Separation of powers forbids an agency from deciding licenses.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "The board investigates and then imposes the result itself. That sounds like too much power in one place."
            "...Except the question keeps circling back to what the nurse never received."
        "Procedural due process: the nurse had no meaningful chance to answer the evidence.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "No disclosed evidence and no hearing means the nurse never had a meaningful chance to answer what the board used against her."
    $ exam_guard_checkpoint_or_jump("civics", "q3_answered", "a0526_civics_save_scum")
    "The last page asks about legitimacy and public trust. I write that disagreement is easier to survive when an institution explains both its authority and its limits."
    "Then my pencil hovers past the period, hunting for one more qualification, until I make myself turn the page facedown."
label a0526_after_civics:
    $ hide_calendar()
    scene black with wipeleft_scene
    if persistent.did_save_scum_civics:
        nier "Civics keeps going without me. Pencils move, and three people glance over before bending back to their own answer bubbles."
        nier "By the bell, my unfinished paper sits alone on the teacher's desk, squared so neatly that my face burns when I walk past it."
    else:
        nier "Civics ends with the papers passing forward through a silence nobody wants to be the one to break."
        # SFX SUGGESTION: Several chairs scraping back as the exam-room silence breaks into low chatter.
        nier "Then the chairs scrape back, and people barely have their bags before they start asking each other questions whose answers can only hurt them."
        nier "I do {i}not{/i} participate."
    call nier_clear from _call_nier_clear_0526_1
    stop music fadeout 1.0
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    if persistent.did_save_scum_civics:
        play music hopeless
    else:
        play music day_c
    if persistent.did_save_scum_civics:
        "I sit with my lunch bag against my knee while people compare answers around me. The food warms through the wrapper, and the zipper stays shut."
        "A classmate comes over with his notes folded into his back pocket and a question already on his face."
        "He looks past my shoulder first, to the civics teacher. She's still by the classroom door with someone from the office, holding my paper flat against her folder."
        "He asks whether the vending machine ate my money instead."
        "I tell him I never used it, and neither of us can find anywhere sensible for the conversation to go."
        "Behind us, somebody launches into a defense of the nurse answer. A laugh comes up out of pure habit and dies as a breath."
        "Then Friday's scholarship page comes back to me, with Mom sitting beside it."
        "{i}She is going to hear that I cheated.{/i}"
        "{i}... Does the university hear it too?{/i}"
        "I keep both hands on the lunch bag until the bell and never open it."
    else:
        "By lunch, everyone has forty minutes and no idea what to do with them, so the hallway outside the classroom turns into a trading floor for answers nobody can change."
        "One classmate insists the nurse question was a trick. Another tells him every question's a trick if you show up unprepared."
        # NUDGE KEEP (P1.8): one of the two exam-hallway scenes to keep (with May 27's pH argument).
        "A guy from the next row catches me by the windows to ask whether the national water standard wiped out the stricter regional limits, already watching my face like I keep the answer key behind it."
        mc "It said {i}minimum{/i}, so... no, I don't think so. The regions still had their own inspectors."
        "He starts to argue, then thinks better of it and tucks his notes under one arm."
        mc "It was annoying, sure. But at least it was {i}consistently{/i} annoying."
        "That gets a tired laugh out of him before he leaves me to my lunch."
        "By the time the bell rings, my fingers have stopped aching every time I close them."
    $ hide_calendar()
    scene black with wipeleft_scene
    if persistent.did_save_scum_civics:
        nier "I file back in behind everybody complaining about civics. Wherever their papers ended up, mine isn't with them."
    else:
        nier "The afternoon bell cuts lunch short right as people start looking human again, and it sends us back in resentful and far less interested in comparing answers."
    call nier_clear from _call_nier_clear_0526_2
    stop music fadeout 1.0
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music exam
    "The language arts papers come with wider margins and cleaner type, though what I'd really appreciate is fewer pages."
    $ exam_guard_checkpoint_or_jump("la", "exam_start", "a0526_la_save_scum")
    "Three short excerpts share the first page, and all the blank space around them makes me suspicious of the questions."
    show japanese_teacher neut at t11
    japanese_teacher "Definitions are only a first step, not an answer. Tell me what the technique makes the reader do, and use the passage in front of you."
    "Her gaze sweeps the room and stops on anyone whose hand is still in a pencil case."
    japanese_teacher "Begin."
    show japanese_teacher at thide
    hide japanese_teacher
    $ exam_guard_checkpoint_or_jump("la", "q1_open", "a0526_la_save_scum")
    "{i}Rain worried the roof all afternoon, threading down the gutters and blurring the garden beyond the glass.{/i}"
    "{i}At dusk, the power failed. The house went still.{/i}"
    "{i}Question 1. What is the strongest effect of the shorter final sentences?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "They prove the narrator is frightened by the storm.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "The stillness feels threatening, so I hand the fear to the narrator."
            "The passage never tells me who is afraid."
        "They compress the change and make the outage feel abrupt.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "The weather has room to gather inside the long first sentence."
            "Then the two short stops make the outage arrive all at once."
        "They make the scene objective by removing descriptive detail.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "The description narrows after the power fails, but the change in rhythm still shapes how the moment feels."
            "Fewer details don't make a passage objective."
    $ exam_guard_checkpoint_or_jump("la", "q1_answered", "a0526_la_save_scum")
    "The second excerpt follows a museum visitor through the closing announcement and the dimming gallery lights."
    $ exam_guard_checkpoint_or_jump("la", "q2_open", "a0526_la_save_scum")
    "{i}The guard announces closing.{/i}"
    "{i}Ren reads the same label a third time, then straightens the frame beside it after the gallery lights dim.{/i}"
    "{i}Question 2. What does the external narration most strongly suggest?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "Ren cannot understand the exhibit without reading the label again.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "I stop at the third reading and mark confusion, leaving the straightened frame stranded in the next sentence."
        "The frame is crooked because another visitor disturbed it.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Ren straightens the frame, but the passage never says who disturbed it."
            "I supply another visitor because the empty space bothers me."
        "Ren's repeated, unnecessary actions carry a reluctance to leave.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "Closing has already been announced, and Ren keeps reading and straightening things that no longer need it."
            "Each small task is another delay."
    $ exam_guard_checkpoint_or_jump("la", "q2_answered", "a0526_la_save_scum")
    "By the short-response section, my wrist throbs every time the pencil changes direction, so I shake the hand out beneath the desk and keep writing while the feeling crawls back into my fingers."
    $ exam_guard_checkpoint_or_jump("la", "q3_open", "a0526_la_save_scum")
    "{i}A river stone first serves as a child's game piece.{/i}"
    "{i}Years later it holds down an eviction notice, then is returned to the current in the final scene.{/i}"
    "{i}Question 3. Which interpretation best follows the pattern?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "The stone moves from play to burden, then becomes part of an act of release.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "The stone stays ordinary while the scenes change what its weight has to carry."
            "A game, then a burden, then release."
        "The recurring stone merely provides continuity between otherwise separate scenes.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Continuity is true and already on the page."
            "I mark it and never follow the stone from the game to the notice."
        "Returning the stone proves the character has rejected every childhood memory.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Returning the stone may close one part of the past."
            "I make that single act reject an entire childhood the passage never asked it to erase."
    $ exam_guard_checkpoint_or_jump("la", "q3_answered", "a0526_la_save_scum")
    "The final response asks how sound and syntax move the first excerpt from endurance into interruption."
    "My first attempt sprawls halfway down the margin, so I cross out the worst of it and try again in language a grader can follow."
label a0526_after_la:
    $ hide_calendar()
    scene black with wipeleft_scene
    if persistent.did_save_scum_civics or persistent.did_save_scum_la:
        if persistent.did_save_scum_civics and persistent.did_save_scum_la:
            nier "By the bell, two teachers have stopped two papers in {i}one day{/i}."
            nier "Two is such a stupidly small number. I can't make it look real."
        else:
            nier "By the bell, one paper has become a zero, and every chair scrape and locker slam seems to turn my way."
        nier "On the way to the door, I rehearse three explanations."
        nier "In all three, I get to the pressure before I get to the answer I changed."
    else:
        nier "The second session ends quieter than the first, since by now even the loudest people have learned what comparing answers does to them."
        nier "I leave with two subjects crossed off and four more lined up for Tuesday and Wednesday."
    call nier_clear from _call_nier_clear_0526_3
    if persistent.did_save_scum_civics or persistent.did_save_scum_la:
        pause 2.0
        scene bg corridor
        $ show_calendar()
        $ atmos("afternoon")
        with dissolve_scene_full
        if persistent.did_save_scum_la:
            show japanese_teacher neut at t11
            "The language arts teacher is waiting outside the classroom with a narrow envelope pressed to her attendance folder, and she watches me all the way over."
            japanese_teacher "Take this to student services before you leave. Your signature only means you received it."
            mc "Can I read it first?"
            japanese_teacher "You may read {i}every word{/i}. Just do it before you try to argue with me in the hallway."
            "She offers it by one corner and lets go as soon as I have it."
            show japanese_teacher at thide
            hide japanese_teacher
        else:
            show civics_teacher neut at t11
            "The civics teacher is waiting by the stairwell with a narrow envelope against her attendance folder, and there's no route past her that would look accidental."
            civics_teacher "Student services needs this before you leave. Your signature means you received it, not that you agree."
            mc "Right..."
            "The word barely clears my teeth, and whatever else is on my face makes her hesitate before she holds out the envelope."
            civics_teacher "Read it first, [player]. We're not having the rest of this conversation in a hallway."
            show civics_teacher at thide
            hide civics_teacher
        "Through the thin seal, the folded notice presses against my thumb. I'm still holding it there when two students come around the corner arguing about the stone question."
        "They see the envelope and go quiet until they're past me."
        "It leaves me nothing to push back against."
        $ hide_calendar()
        scene black with wipeleft_scene
    if exam_guard_day_scummed("civics", "la"):
        call exam_guard_home_confrontation("May 26", "civics", "la") from _call_exam_guard_home_confrontation_0526
    if exam_guard_should_bad_end():
        jump exam_guard_bad_ending
    if persistent.exam_save_scum_subjects:
        stop music fadeout 1.0
        pause 2.0
        scene bg bedroom_night
        $ show_calendar()
        $ atmos("home_night")
        with wipeleft_scene
        play music hopeless
        "My room looks almost normal, apart from the bare spots where my phone and laptop should be."
        "I sit at the desk with the biology packet open, but every creak from downstairs sends me back to the top of the paragraph."
        "Then something scrapes softly outside my door."
        "When I open it, there's a glass of water on the hall floor, set dead center where nobody will catch it with a heel. Across the hall, Asahina's door clicks shut."
        "The water stays cold against my palm while I stand there deciding whether knocking would make it worse."
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "Monday ends with biology still open on my desk and the glass empty beside it."
        nier "One finished page sits beneath the alarm clock, set for the usual time."
        call nier_clear from _call_nier_clear_0526_4_scum
    else:
        stop music fadeout 1.0
        pause 2.0
        scene bg corridor
        $ show_calendar()
        $ atmos("afternoon")
        with wipeleft_scene
        play music night_b
        "My fingers still ache when I hitch my strap higher and join the slow shuffle toward the stairs, through a hallway of unzipped bags and exhausted arguments."
        show monika forward uniform dist cm oe nobl rdown ldown at t11
        "Monika waits near the stairwell with her folder hugged to her chest, letting the last few people pass before she steps over to me."
        m forward uniform curi om oe nobl rdown ldown "Please tell me you didn't ask anybody about the short response..."
        mc "Absolutely not. I'd like to sleep this week."
        m forward uniform happ cm ce nobl rdown ldown "Good. I couldn't make myself ask, either, and I {i}really{/i} wanted to."
        mc "That was a test, wasn't it?"
        m forward uniform happ om oe nobl rdown lpoint "Barely! But you passed~"
        show monika forward uniform dist cm oe nobl rdown ldown
        "She rubs under one eye with a knuckle, and as we reach the stairs, she looks back down the club hallway."
        m forward uniform nerv om oe nobl rdown ldown "Hey, um... do you want to sit in the club room for a few minutes? I'm not ready to go home and open another folder just yet."
        mc "I thought we were preserving brain function."
        m forward uniform happ om oe nobl rdown ldown "We are! That's why there's {i}no exam talk{/i} for fifteen whole minutes."
        mc "...All right. Fifteen minutes."
        "On the way, two students pass us arguing about the stone question, and Monika gives the nearest fire-safety notice her complete attention until their voices fade."
        $ hide_calendar()
        scene black with wipeleft_scene
        pause 2.0
        scene bg club_day
        $ show_calendar()
        $ atmos("afternoon")
        with wipeleft_scene
        play sound moddooropen
        show monika forward uniform dist cm oe nobl rdown ldown at t11
        "Monika writes {i}NO POSTMORTEMS FOR FIFTEEN MINUTES{/i} on the board and leaves the chalk in the tray."
        "Hikari is behind a manga, Homura has her face buried in her arms, and another member is quietly working through a bun."
        m forward uniform curi om oe nobl rhip ldown "That includes indirect questions, too. And meaningful looks."
        mc "You've ruled out most of my conversation."
        m forward uniform happ cm oe nobl rhip ldown "You'll manage! I've seen you carry entire conversations with your eyebrows."
        "Her bottle cap won't budge until I hold the bottle steady for her, and when she sits, it ends up next to mine."
        homura "The reading passage about the stone--"
        hikari "Board."
        homura "I was merely going to ask what {i}she{/i} wrote. Not what I wrote."
        hikari "{i}Board.{/i}"
        "Homura looks from the board to the clock and lowers her chin back onto her arms."
        homura "Eleven minutes is an extraordinarily long time."
        "Monika picks her bottle up by the neck and sets it down with a hollow knock, then smiles across the desk."
        m forward uniform happ om oe nobl rhip ldown "It's four minutes shorter than it was when you started arguing, so let's enjoy what we have left, shall we?"
        if s1_was("club_mediation", "homura"):
            "Homura sits up and slides a folded square of paper over until it rests on Hikari's open manga."
            "Hikari reads it where it landed, then tucks it behind the back cover."
        elif s1_was("club_mediation", "hikari"):
            "Hikari's eyes stay on her page, but one hand comes out toward Homura, palm up."
            "Homura stares at it. Then she fishes a folded square of paper out of her sleeve and lays it there."
            "Hikari pockets it and turns the page."
        elif s1_was("club_mediation", "both"):
            "Homura nudges a folded square of paper over to Hikari's side. Hikari takes it, then slides back a folded page of her own from the back of her manga."
            "They each tuck the other's away, and nobody unfolds anything."
        "Hikari turns her manga sideways for a double-page spread, and I catch a glimpse of a dragon in an apron."
        mc "Is that the one where the dragon opens a restaurant?"
        hikari "The landlord's a dragon. The chef's a {i}different{/i} dragon."
        mc "Right. Rookie mistake."
        "She holds up the cover when I ask for the title, and Monika leans across to look."
        m forward uniform happ om oe nobl rdown ldown "Oh, you were telling me about this one! The soup one?"
        mc "The soup is {i}one{/i} episode. You make it sound like I've been following a broth for twelve weeks."
        m forward uniform laug om ce nobl rdown ldown "You sent me three messages about it!"
        mc "He threw away the stock. I needed someone else to know."
        "Monika takes out her phone and scrolls back while I try to remember what else I said."
        m forward uniform wry om oe nobl rdown ldown "Four messages. And a picture of your dinner."
        hikari "Hey, I'm only on volume {i}two{/i}. Take your soup fight somewhere else!"
        "I swivel my chair toward Monika, and she swivels hers to match, both of us trying to do it quietly."
        mc "One episode. I'll send it tonight, and you can judge for yourself."
        m forward uniform happ cm oe nobl rdown ldown "Fine. But I'm eating first. Last time you did this, I had to get up and make toast."
        "Homura surfaces from her arms to ask for the link."
        # SFX SUGGESTION: A restrained phone-timer buzz in the otherwise quiet club room.
        "When the timer finally buzzes, the manga closes and chair legs begin to scrape."
        "Monika is still showing me the dinner photo when the other members start packing. I'd forgotten the burnt corner was in frame."
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "Monika waves goodbye from the hallway, her folder still shut."
        nier "I head out scrolling for the episode on my phone, and it takes me three tries to get the title right."
        call nier_clear from _call_nier_clear_0526_4
        stop music fadeout 1.0
        pause 2.0
        scene bg dining_table_night
        $ show_calendar()
        $ atmos("home_night")
        with wipeleft_scene
        play music house_day_a
        "Mom is finishing the carrots when Asahina wanders in after the smell of soup and sets the rice bowl down where my glass used to be."
        show mom determined at t22
        show asahina teasing at t21
        mom "Before either of you starts, the exams can wait until everyone has eaten."
        ah "Wait, the projector doesn't count as exam talk. It literally started {i}smoking{/i} in the middle of class."
        show mom curious
        mom "Smoking? Was everyone all right?"
        mc "Careful, Asa. She's going to ask who reported it."
        show mom smug
        mom "Yes, I am. Start there."
        show asahina annoyed
        ah "I don't know who reported it! Everyone's {i}fine{/i}. The teacher yanked the plug and spent the next ten minutes teaching around the smell."
        show asahina neut
        show mom neut
        "Asahina nudges the serving spoon my way with her knuckles while Mom turns back to the cutting board."
        ah "You still functioning?"
        mc "Apparently. You?"
        ah "Ask me after dinner."
        "She looks down while she scoops rice. Mom passes the soup around and leaves both answers alone."
        "{i}So, did the tangerine count as lunch, or...?{/i}"
        "I drink my soup instead, and the question goes down with it."
        "For a while the loudest thing at the table is chopsticks against bowls."
        "Then all three pairs drift toward the last piece of fried tofu at once, and Asahina's chopsticks get there first."
        mc "Oh, come on! You saw me going for that."
        show mom teasing
        mom "So did she."
        show asahina smug
        ah "Skill issue."
        "Mom hides a smile behind her soup, and Asahina makes a show of chewing until I give up on a better complaint."
        $ update_character_thought("monika", "Monika remembered my complaints about the dragon-restaurant show and dug up all four messages. I owe her the episode.")
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "Biology gets the table after dinner, and I rename tomorrow's alarm {i}BIOLOGY, DIPSHIT{/i}."
        nier "On my way up to bed, I pass Asahina's bag slumped at the foot of the stairs, its front pocket hanging open."
        nier "The tangerine is still in there, unpeeled."
        call nier_clear from _call_nier_clear_0526_5
    # Keep a guarded handoff through the overnight/opening transition. A save
    # made before tomorrow's exam_start must still point at the upcoming paper.
    $ exam_guard_checkpoint_or_jump("biology", "day_ready", "a0527_biology_save_scum")
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0526_1
    jump a0527

label a0526_civics_save_scum:
    $ exam_guard_mark_scummed("civics")
    $ calendar.set_date(2025, 5, 26)
    $ hide_calendar()
    scene black with dissolve_scene_full
    stop music fadeout 0.5
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("pressure")
    with dissolve_scene_full
    play music safety
    show civics_teacher neut at t11
    civics_teacher "[player]."
    "The other pencils keep scratching while she stands beside my desk, holding my answer sheet below the next row's sightline."
    civics_teacher "Put your pencil down."
    "My pencil clips the edge of the desk and rolls into the open case, where Mom's spare eraser stops it."
    mc "...Did I do something?"
    "My voice thins on the last word."
    civics_teacher "Please don't make this worse by pretending you're confused."
    civics_teacher "You know exactly how a wrong answer differs from a dishonest one. I expected better from you."
    civics_teacher "I am disappointed in you, [player]."
    mc "I'm sorry. I was just--"
    "The sentence breaks there, and my face is too hot to go looking for the rest of it."
    civics_teacher "I heard you."
    civics_teacher "Civics is a zero. Keep your eyes forward, and we will not discuss it again until the session ends."
    mc "...Yes, ma'am."
    "Someone turns a page behind me, the clock keeps moving, and the eraser stays exactly where the pencil knocked it."
    "{i}Mom put that there. This morning.{/i}"
    "I keep my eyes on the clock. I know what happens if I look at the eraser again."
    show civics_teacher at thide
    hide civics_teacher
    play music hopeless fadeout 1.0
    jump a0526_after_civics

label a0526_la_save_scum:
    $ exam_guard_mark_scummed("la")
    $ calendar.set_date(2025, 5, 26)
    $ hide_calendar()
    scene black with dissolve_scene_full
    stop music fadeout 0.5
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("pressure")
    with dissolve_scene_full
    play music safety
    show japanese_teacher neut at t11
    japanese_teacher "[player]."
    "A page turns behind me at the same moment, but her voice still finds the space beneath it."
    japanese_teacher "Close the exam, please."
    "My thumb misses the cover the first time, and I have to try again while she waits."
    mc "...Why?"
    japanese_teacher "Because the answer I saw earlier is gone, and the correction in its place wasn't made in this room."
    if persistent.did_save_scum_civics:
        japanese_teacher "After this morning, I hoped you understood the problem."
        mc "I... I do."
        japanese_teacher "Understanding it now doesn't undo it."
    japanese_teacher "There isn't a literary argument to make here, [player]. You changed an answer after it was recorded."
    mc "I can explain."
    japanese_teacher "Explain what, exactly?"
    "My mouth stays open, but the explanation never shows up."
    japanese_teacher "The altered answer is already on the page. Language arts is a zero, and we'll discuss the rest after the session."
    mc "Is this... going to the office?"
    japanese_teacher "Yes."
    "Somebody nearby erases for several long seconds while the rest of the room keeps working, and I sit there listening to the rubber drag across the paper."
    "The office is waiting somewhere past the bell."
    "A chair, and an adult who will ask me to say plainly what I just tried to explain away."
    show japanese_teacher at thide
    hide japanese_teacher
    play music hopeless fadeout 1.0
    jump a0526_after_la
