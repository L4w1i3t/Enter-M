define counselor = Character("Counselor", **SAY_STYLE)


label a0529:
    # --- Day 15: 2025-05-29 ---
    # First day after exams (exams ran 0526-0528). Decompression contrasts exam-week tension.
    # Matsuda's post-exam ramp begins here and continues through 0530-0531 toward Chapter 1.
    # The increase should read as ordinary social momentum on a first playthrough: she makes a
    # visible effort to honor MC's request for a slower pace and invites him and Asahina into an
    # existing Saturday plan with Tsubaki. May 30 settles the logistics. The underlying pattern belongs to
    # hindsight, not MC's present-tense suspicion. Other meters moved: Asahina/food + Sam's
    # schedule-as-care wrong note, Mom's contract-read on both kids, track invitational ahead.
    $ _exam_one_catch = exam_guard_scum_count() == 1
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music house_day_a
    if _exam_one_catch:
        $ _exam_repair_subject_text = exam_guard_subjects_text(persistent.exam_save_scum_subjects)
        "My phone is still lying beside Mom's tablet, right where she set it down last night."
        "The screen stays dark. I look over anyway, every time her hand moves."
        show mom uniform neut at t22
        show asahina uniform unamused at t21
        "Mom is already dressed for work. Across the table, Asahina has been tearing the same slice of toast into smaller and smaller pieces since I came downstairs."
        mom "The review is at seven forty. Shoes on in {i}two minutes{/i}."
        mc "I know."
        show mom uniform determined
        mom "You read the notice? All of it?"
        "I make myself finish chewing first. Mom waits like she has all morning instead of two minutes."
        mc "Counselor, my [_exam_repair_subject_text] teacher, and one notified parent or guardian."
        "Asahina puts her toast down with enormous care. The plate still clicks."
        show asahina uniform neut
        ah "You want my other piece?"
        mc "No. Thanks."
        "She slides the plate over to my side all the same."
        mom "Everything else posts Monday. This morning is only about the section they stopped."
        mc "Right."
        mom "When they ask what happened, you will answer the question they ask."
        mc "I changed--"
        show mom uniform unamused
        mom "I know what you changed. Save it for the meeting, and let them hear it from you."
        "I set my chopsticks down."
        "Asahina picks her crust back up and can't find anywhere natural to look."
        "Mom collects her bag, and on her way behind my chair she slips a banana into the side pocket of mine."
        show mom uniform determined
        mom "You are still eating lunch today."
        mc "Okay."
        "She zips the pocket shut over it and leaves the bag propped against my foot."
    else:
        show mom uniform neut at t22
        show asahina uniform unamused at t21
        "With exams over, the table has been returned to civilian use: Mom's tablet at her end, and the jam no longer buried under anybody's notes."
        "Asahina is chewing with her eyes half shut and resting between bites, like the toast is a workout she never signed up for."
        mom "Morning."
        mc "Morning."
        ah "Mngh."
        mc "Eloquent."
        ah "You want full sentences, go make me coffee."
        "Her eyes stay shut through the next bite, and she finds her plate again by what I can only assume is sonar."
        show mom uniform teasing
        mom "Midterm results don't post until Monday, so nobody needs to refresh the portal over breakfast."
        show asahina uniform annoyed
        ah "I wasn't."
        mc "She was."
        ah "I was {i}going{/i} to. There's a difference."
        "She tears another strip off the toast and herds it around her plate."
        show mom uniform thinking
        mom "There is. Keep not doing it until the toast is gone."
        "Mom lowers the tablet as I reach past it for the rice."
        show mom uniform curious
        mom "Track today?"
        mc "Yep. Coach said we'd 'reassess' after exams."
        mc "...So, yelling, a little running, and then some more specific yelling."
        show mom uniform smug
        mom "A balanced program."
        mc "He's very holistic."
        show asahina uniform happy
        "Asahina snorts into her toast and slaps a hand over her mouth."
        "On her way past with her bag, Mom slips a banana into the side pocket of mine."
        show mom uniform determined
        mom "Eat lunch, both of you, and I mean an {i}actual{/i} one."
        show asahina uniform neut
        ah "I always eat lunch."
        show mom uniform neut
        mom "You always {i}bring{/i} lunch. I would also like it to stop coming home with you."
        "Asahina opens her mouth and turns to me, like I might have a defense drafted and ready to file."
        "All she gets from me is chewing. She closes her mouth again."
    $ hide_calendar()
    scene black with wipeleft_scene
    if _exam_one_catch:
        nier "Mom and I leave Asahina at the table with both pieces of toast."
        nier "On the walk, Mom doesn't rehearse a word of the meeting with me, and at the gate she slows down so I go in first."
    else:
        nier "Asahina and I walk to school without an argument, and neither of us mentions the unusual lack of one."
        nier "The closer we get, the louder the sidewalks are. Everybody's remembering they're allowed to talk about something besides exams."
        nier "Morning classes pass as one long post-exam shrug. Lunch comes with no roof invitation and no library plan, so I take my forty unclaimed minutes to the corridor windows."
    call nier_clear from _call_nier_clear_0529_1
    stop music fadeout 1.0
    if _exam_one_catch:
        pause 2.0
        scene bg class_day
        $ show_calendar()
        $ atmos("pressure")
        with dissolve_scene_full
        play music safety
        "Student services is too small for four chairs, so the counselor borrows an empty classroom before first bell and pushes two desks together."
        "My altered exam section sits in the middle, beside a blank incident form and a pen."
        show mom uniform neut at t22
        "Mom takes the chair on my right. Across from us, the teacher who stopped my section rests one hand on a closed folder."
        counselor "Before we discuss what happens next, we need your account in your own words."
        "The form is turned toward me, its first line empty."
        mc "I changed an answer after it was final."
        teacher "Which section?"
        "I look to Mom. She's watching the teacher."
        mc "The [_exam_repair_subject_text] section. I loaded an earlier save so I could change it."
        teacher "That is accurate."
        "The counselor ticks a box beside my account. I can hear the pen against the paper."
        counselor "The section remains a zero, and the incident goes to your senior advisor and into the school's internal file."
        counselor "A second incident would move it beyond this room. The section score itself cannot be appealed."
        show mom uniform thinking
        mom "What does he need to do now?"
        counselor "He signs his account today and meets his advisor Monday after the results post. Everything after that is completed under the ordinary rules."
        teacher "I'll supervise his next assessment. We'll discuss the arrangements with his advisor on Monday."
        "I take the pen and write my account on the first line, slowly, so nobody has to ask me to make it legible, then sign beneath it."
        "My hand doesn't start shaking until I put the pen down."
        show mom uniform determined
        mom "Tell me what you heard, [player]."
        mc "The zero stays. I sign this, meet my advisor Monday, and do the next work without looking for a way around it."
        mom "And?"
        "My name is printed on the tab of the teacher's folder. I keep my eyes on it while I answer."
        mc "And doing the next assignment right doesn't make this one disappear."
        "Mom's shoulders lower a fraction, but her hand stays flat beside the form."
        show mom uniform neut
        mom "All right."
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "The counselor keeps the signed page. The teacher keeps the exam section."
        nier "Mom and I walk out with nothing in our hands."
        call nier_clear from _call_nier_clear_0529_repair_1
        pause 2.0
        scene bg corridor
        $ show_calendar()
        $ atmos("pressure")
        with wipeleft_scene
        show mom uniform neut at t11
        "By the stairwell, Mom takes my phone out of her bag. She keeps hold of it until I meet her eyes."
        mom "I'm giving this back so we can reach each other. The restrictions still stand."
        mc "I understand."
        "She sets it in my palm and doesn't let go until my fingers close around the case."
        show mom uniform determined
        mom "School, track, home today. Tomorrow's scheduled club meeting counts as school, but it is not permission for a detour afterward."
        mom "The laptop stays downstairs, and your phone charges in the kitchen at ten. If you want anything after track Saturday, you {i}ask{/i} instead of announcing it on the way out."
        mc "Okay."
        mom "What time are you home today?"
        mc "After practice. Straight home."
        "She checks the time and starts for the administration stairs. At the foot of them, she turns back."
        show mom uniform neut
        mom "Eat the banana."
        mc "I will."
        show mom at thide
        hide mom
        "I stay by the stairwell until her footsteps fade toward the front office. The line I signed is still there every time I blink."
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "The first bell rings while the meeting still doesn't feel finished."
        nier "Three periods later, lunch comes with no roof invitation and no library plan, and I take my forty unclaimed minutes to the corridor windows."
        call nier_clear from _call_nier_clear_0529_repair_2
        stop music fadeout 1.0
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music day_c
    "I claim a stretch of windowsill and take my time with lunch, starting with the banana Mom issued me this morning. For once, there's no exam waiting when I finish."
    "My phone buzzes against the sill. It's Monika."
    if _exam_one_catch:
        python:
            _phone_messages = [
                phone_msg("them", "Hey! Haven't seen you today. Everything okay?"),
                phone_msg("me", "Still at school."),
                phone_msg("them", "Okay. Well, come find me if you feel like talking."),
                phone_msg("them", "Club's back to normal hours tomorrow, by the way. Actual writing, and I'm banning the word midterm."),
                phone_msg("me", "I'll be there."),
                phone_msg("them", "Good. See you tomorrow!"),
            ]
    else:
        python:
            _phone_messages = [
                phone_msg("them", "Okay, I listened to your songs on the bus!"),
                phone_msg("me", "And remembered to get off?"),
                phone_msg("them", "Yes! But the second one started right before my stop, so I stood outside the shelter and finished it like a weirdo."),
                phone_msg("me", "That's the one I was betting on."),
                phone_msg("them", "Send me the whole album when you get a minute?"),
                phone_msg("them", "Oh, and club's back to normal hours tomorrow."),
                phone_msg("me", "See you there. I'll dig up the album."),
            ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0529_1
    if _exam_one_catch:
        "There's room after {i}still at school{/i} for the rest of the morning."
        "...I open the calendar instead, type {i}advisor{/i} into Monday, and lock the phone."
    "I'm halfway through another bite when it buzzes again, Matsuda's name stretched across the screen this time."
    python:
        _phone_messages = [
            phone_msg("them", "Greetings, survivor."),
            phone_msg("them", "I trust the gauntlet did not consume you whole."),
            phone_msg("me", "Still assembled. Mostly."),
            phone_msg("them", "Good. I was about to ask how it went, but--ah, no. Visible effort."),
            phone_msg("them", "Observe! I am leaving the question unasked at {i}great personal cost{/i}."),
            phone_msg("me", "Your sacrifice has been noted."),
            phone_msg("them", "Are you on campus presently?"),
            phone_msg("me", "Corridor windows. Why?"),
            phone_msg("them", "No reason of consequence."),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, append=True) from _call_phone_text_conversation_0529_2
    stop music fadeout 1.0
    # SFX SUGGESTION: Fast, purposeful footsteps approaching along the corridor tile.
    "Mid-chew, I hear quick footsteps turn in at the far end of the corridor and keep coming."
    show matsuda uniform smug at t11
    "Matsuda rounds the corner with her phone still in hand and zeroes in on me."
    play music theme_matsuda_a
    ma "Aha! Phone and corridor are in perfect agreement!"
    mc "So 'no reason of consequence' meant you were already on your way."
    show matsuda teasing
    ma "A trifling omission made in service of the reveal."
    "Trading her phone for a melon bread on the way down, she drops onto the windowsill beside me with more flourish than painted concrete deserves."
    mc "Where's your conscience?"
    show matsuda happy
    ma "Kareda's class rotated lunch blocks. I am operating unsupervised and at tremendous personal risk."
    mc "That explains the melon bread."
    show matsuda unamused
    ma "The melon bread is a {i}choice{/i}, not a cry for help."
    show matsuda neut
    "She tears off a piece, and for a while we just eat and let the courtyard do the talking."
    "By the time she speaks again, half my lunch and most of the melon bread are gone."
    show matsuda happy
    ma "So! Kareda and I are thinking of investigating a used-book clearance on Saturday. There's an arcade nearby too, allegedly, full of machines that take your coins and insult your reflexes."
    mc "The arcade sounds more like your natural habitat."
    ma "I thrive wherever the lighting is hostile and victory produces tickets."
    show matsuda curious
    ma "We were thinking we might invite you and Asahina too, assuming the plan survives its next encounter with Kareda's common sense."
    # Converging. The invitation stands either way. This is the deliberately
    # performed shy-schoolgirl persona: its stutters and diminished confidence
    # belong to the act, not to a general dialogue-cadence rule. Let the reader
    # see the change without settling how much of the invitation she means.
    # Registered in s1_choices.rpy as 0529 arcade_invite.
    menu:
        "She has gone to some trouble to make this sound casual."

        "Leave it open.":
            $ s1_pick("arcade_invite", "open")
            mc "Keep me posted on whether it survives."

        "Say yes now.":
            $ s1_pick("arcade_invite", "yes")
            mc "I'd like that. And Asahina's gonna want in the second she hears the word arcade."
            show matsuda happy
            ma "Then the plan has acquired momentum! Momentum is the hardest part."

        "Ask why she's inviting us.":
            $ s1_pick("arcade_invite", "why")
            mc "Why us?"
            "It comes out blunter than I meant it to. I really was just asking."
            show matsuda neut
            "She turns to the courtyard instead of me, and no answer comes."

    show matsuda embarrassed
    "Then her knees draw together, and the last of the melon bread comes up to her chest in both hands like a love letter she can't work up the nerve to deliver. When she looks up at me, her chin stays down."
    "Her voice comes out at about a tenth of its usual volume."
    ma "U-Um... only if you w-want to, of course. I could show you where it is... or, or you could go with your other friends, and I could just hear about it after. I wouldn't mind. Much."
    mc "...You're the one who invited me."
    show matsuda nervous
    ma "I-I know! Sorry! It's just... you already have so many people, and I'm only some girl you crashed into on the sidewalk, and I'd hate for you to feel like you have to look after me..."
    "Her thumbs fret at the edge of the wrapper until a crumb drops into her lap, and she brushes it away like one more thing she's done wrong."
    mc "Hold on. Are you doing the shy transfer student right now?"
    show matsuda embarrassed
    ma "P-Please don't look at me like that... I practiced what I was going to say, and now it's all..."
    "She trails off toward her shoes, then risks one peek at me over the top of the melon bread."
    ma "...wrong."
    mc "Oh, you practiced, all right."
    show matsuda nervous
    ma "I-I could wait by the gate? After school? You wouldn't even have to talk to me. I just thought... maybe I could walk with you for a little bit. At a respectful distance."
    mc "Matsuda. You just invited me to an arcade."
    ma "Oh... r-right. I'm really not very good at this, am I?"
    "She holds a small, hopeful, extremely rehearsed smile while I try to finish chewing."
    mc "Okay. Can the shy transfer student give me one second to swallow?"
    show matsuda smug
    "She sits up straight and takes a huge, completely untroubled bite of melon bread. The shy voice is gone like it was never there, and the real one doesn't wait for her to swallow."
    ma "Admit it. The range was impeccable."
    mc "You almost got me with the gate."
    show matsuda unamused
    ma "I know."
    show matsuda neut
    ma "Seriously, though, I'll send you the plan once Kareda and I settle on a time."
    # SFX SUGGESTION: A paper-wrapper swish ending in a light hollow bin impact.
    "She finishes the last mouthful and lobs the balled-up wrapper across the hall."
    "It drops into the bin, nothing but net. When I turn back, she's already watching me, waiting for the review."
    mc "Okay, that was decent."
    show matsuda happy
    ma "A witness! My legend grows!"
    show matsuda annoyed
    "Her volume comes back with the legend, and she winces and dials it down herself."
    show matsuda happy
    "She gets up with a bow, scaled down to corridor size, and slips back into the lunch traffic."
    show matsuda at thide
    hide matsuda
    stop music fadeout 1.0
    "Once she's gone, I finish lunch trying to remember how much credit is left on my arcade card."
    $ update_character_thought("matsuda", "Matsuda and Tsubaki invited Asahina and me to a book sale and an arcade. She got through an entire shy-schoolgirl act before promising to send me the plan.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Afternoon classes drain away, and at the final bell I head straight for the track."
    call nier_clear from _call_nier_clear_0529_3
    stop music fadeout 1.0
    pause 2.0
    scene bg track_day
    $ show_calendar()
    $ atmos("afternoon")
    with dissolve_scene_full
    play music day_c
    "Late-spring warmth has soaked into the track and taken the edge off the smell of rubber, while the distance group loiters on the infield, stretching in a way that could pass for a warmup if Coach squints."
    "Coach waits by the lane line with his clipboard against one hip. He watches me test my left foot against the turf on the way over, so I resist the urge to jog the last few steps."
    show track_coach neut at t11
    track_coach "Exams done?"
    mc "Done."
    track_coach "Brain intact?"
    mc "Pending external review."
    track_coach "Good enough."
    track_coach "Here's the reassessment I promised. You are in no shape to be a hero today."
    mc "So the reassessment is mostly a threat."
    track_coach "If the threat keeps me from scraping you off the back straight, sure."
    track_coach "Twenty-five minutes {i}easy{/i}, and I mean conversational. If you cannot talk while you run it, you are running it wrong."
    mc "And the foot?"
    track_coach "If it talks, you stop. No arguing with it today."
    show track_coach at thide
    hide track_coach
    "I take the outside lane and make myself keep the first lap slow, even when the distance pack starts to pull away."
    if not _exam_one_catch:
        "On the next curve, one runner drifts back out of the pack and falls in beside me. His collar is dark with sweat, but he matches my pace like he's out for a stroll."
        show charlie neut at t11
        charlie "Conversational, right?"
        mc "That was the threat."
        charlie "Good. Has Coach said anything about entries yet? Sixteen, thirty-two?"
        mc "Not yet. I asked him for both."
        charlie "He said maybe to me. If we both get the sixteen, let's not kill each other in the first lap."
        "He knows my events, and I couldn't pick his face out of a lineup. Then again, there's exactly one distance runner Tsubaki has ever named for me."
        mc "You're Charlie."
        "His stride hiccups, and he turns his whole head to stare at me."
        charlie "We've been on the same team since April, man!"
        mc "Tsubaki mentioned you. I just never put the name to a face."
        charlie "Yeah, she warned me about that part."
        "I give the next curve my full attention while he grins at the side of my head."
        charlie "If Coach enters us, I'm thinking seventy-two through four hundred. We can decide whether to ruin our lives after that."
        mc "That's disturbingly reasonable."
        charlie "See? Conversation."
        "He surges back to the pack at the next curve, calling over his shoulder that I can try using his name next time."
        show charlie at thide
        hide charlie
        "I hold Coach's pace through the next lap, breathing on every third step while Charlie's pack opens the gap again. There's no race to decide today."
    else:
        "I settle into three steps in, three out, and keep my eyes on the lane instead of on the page I signed this morning."
    "My foot stays quiet, but around the fourth lap my shoulders start creeping up toward my ears, and I drop them myself so Coach doesn't have to yell it across the field."
    "{i}Relax the hands. Let the pace stay boring. Continuing is the plan.{/i}"
    if _exam_one_catch:
        "Well into the run, I realize I've stopped repeating the sentence I signed."
    else:
        "Well into the run, my brain finally loses track of exams, grades, and every minor sensation below the knee."
    "At twenty-five minutes his whistle catches me mid-curve. I finish the bend regardless."
    "Partly habit. Partly because my legs have remembered how much they resent an interruption."
    show track_coach neut at t11
    track_coach "Walk it out."
    "I keep to the outside lane and walk while he watches my first several steps instead of pretending not to."
    track_coach "Foot?"
    mc "Quiet. My calves know they exist, but nothing specific."
    track_coach "Good."
    "His pen moves twice across the clipboard."
    mc "Are either of those flattering?"
    track_coach "One says you finished without limping. The other says you immediately asked whether I was impressed."
    mc "Mixed review, then."
    track_coach "Invitational entries go in next week."
    "He says it to the clipboard, like it's paperwork and not the thing I've been waiting on since last Wednesday."
    mc "What are you thinking?"
    track_coach "Sixteen if the foot stays quiet. Thirty-two if Saturday's form is clean and you don't turn the easy work into a race."
    mc "Both, like I asked?"
    track_coach "Maybe."
    "His {i}maybe{/i} isn't even finished, and my eyes are already on the starting line."
    track_coach "Do not make that face."
    mc "What face?"
    track_coach "The one where you hear maybe and start planning for yes."
    "Out on the back straight, the distance group comes in by twos, their shoes slapping through the same bright strip of track."
    mc "I can handle both."
    track_coach "That was {i}not{/i} the question."
    mc "What was the question?"
    track_coach "Whether you can run both without setting yourself back. We'll decide after Saturday."
    "He finally lowers the clipboard."
    track_coach "Friday off. Saturday after classes, you do drills and short strides, and then you leave."
    track_coach "Sunday is easy mileage on your own, not a private test to see how much fitness you can win back."
    mc "Very inspiring."
    track_coach "Inspiration is how half this team gets shin splints. Follow the instructions."
    mc "Drills, short strides, leave. Easy Sunday."
    track_coach "Good. Your listening comprehension survived too."
    show track_coach at thide
    hide track_coach
    "I grab my bottle and walk one more lap, with the urge to turn it into a jog tailing me down the whole back straight."
    "I keep walking. It quits first."
    $ hide_calendar()
    scene black with wipeleft_scene
    if _exam_one_catch:
        nier "At the last corner I eye the long way around, then take the short one and get home well ahead of the time I gave Mom."
        nier "The laptop hasn't moved from the living-room table. Nobody comments when I walk past it."
    else:
        nier "I get home with the light gone long and the street still warm, to a house full of cupboard doors and running water: the noises it makes when nobody's bracing for a crisis."
    call nier_clear from _call_nier_clear_0529_4
    stop music fadeout 1.0
    pause 2.0
    scene bg dining_table_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music house_day_a
    play sound moddooropen
    "Home smells like ginger and fresh rice. Asahina has her phone propped against the soy sauce, and Mom is splitting herself between the stove and a work email, sleeves pushed up past her elbows."
    show mom teasing at t22
    show asahina happy at t21
    mom "Good timing. Wash up and take the rice over, will you?"
    mc "Do I get first serving for that?"
    show mom smug
    mom "You get to carry enough for all three of us."
    ah "Mom made the good ginger thing! Get in here before I decide you don't need any."
    mc "I smelled it from the entryway. Your threat's running late."
    ah "It's the good one, not the lazy one."
    show mom unamused
    mom "They are the same recipe."
    show asahina determined
    ah "{i}Fresh{/i} ginger. You can tell."
    show asahina smug
    "Mom declines to dignify that. Asahina takes the silence as a win."
    "By the time I've washed up and carried the rice over, the bowls are out and the two of them are already fighting over the last pickles."
    if _exam_one_catch:
        show asahina neut
        "Nobody says {i}office{/i}, though the appointment card is still tucked behind Mom's phone, Monday's advisor meeting written across the bottom."
        "Asahina starts a sentence with {i}At school today{/i}, thinks better of wherever it was going, and complains about the vending machine instead. Mom asks whether it stole her money again, and I keep eating."
    else:
        "For once, nobody says {i}grades{/i} or {i}answer key{/i} or any of the other words that took over this table during exams. The conversation sticks to pickles, the vending machine, and whether the ginger chicken tastes different tonight."
    show asahina neut
    ah "Sam said the senior portal stays locked until Monday too."
    "She says it to her bowl, nudging a stray grain of rice back in with her thumb."
    show mom neut
    mom "Then nobody has anything useful to refresh tonight."
    ah "He still offered to help me next time, though. Like, he sent me this whole study schedule and said I could change whatever I want."
    show mom thinking
    "Mom's spoon slows before it reaches the bowl."
    mom "That's thoughtful."
    mom "Did you ask him to make the schedule?"
    "Asahina taps her phone dark. I still catch a grid of colored blocks on the screen as it goes."
    show asahina nervous
    ah "Not exactly. I said I kept losing track of what to review, and he sent me a draft after that."
    mc "A draft."
    show asahina annoyed
    ah "It's useful."
    show mom neut
    mom "Then see if it works. You can always ask us, too."
    show asahina neut
    ah "I know, it's just... I said I was lost once, and he remembered. That's all."
    "She leaves the phone facedown and digs through the bag on her knee, and the back of her hand snags the lunchbox zipper. The lid tips up on a strip of rice and the apple slices Mom packed this morning."
    mc "Did you actually eat lunch today?"
    show asahina frustrated
    "Asahina's head snaps up, and the bag slides off her knee."
    ah "Why is that the second time someone's asked me that today?!"
    mc "Because you keep bringing lunch home like the inside of your bag needs feeding."
    ah "I ate {i}most{/i} of it! Practice started early."
    mom "Most."
    show asahina smug
    ah "Most is a passing grade in some subjects."
    show mom unamused
    mom "Not in mine."
    $ update_character_thought("asahina", "Sam sent Asahina a study schedule after she said she kept losing track of what to review. She says it helps and that she can move the blocks herself.")
    if _exam_one_catch:
        $ update_character_thought("mom", "Mom sat beside me while I signed my own account of changing a final exam answer, then returned my phone so she could reach me rather than because the incident was forgiven. My laptop stays downstairs, and any optional plan has to be asked for first.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I wash while Asahina dries exactly four things and declares her shift over. Mom ends a clipped work call on the word {i}tomorrow{/i} and finishes the drying herself."
    call nier_clear from _call_nier_clear_0529_6
    stop music fadeout 1.0
    pause 2.0
    scene bg living_room_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music night_b
    "I'm halfway to the stairs when Mom opens the cabinet under the television and reaches past a nest of old cables and the manuals for appliances we no longer own."
    "She comes back out with a battered box that has survived several moves and at least one disastrous winter break. The tape down one side is still holding that winter together."
    show mom smug at t22
    show asahina curious at t21
    mom "One round."
    ah "Of what?"
    "Mom turns the box around so the worn title faces us."
    "{i}COPPER CROWN: BUILD THE REALM, CONTROL THE MARKET.{/i}"
    mc "You said the day was over."
    show mom teasing
    mom "The workday is over. Beating both of you is recreational."
    show asahina smug
    ah "Wow. She brought out the box just to talk shit."
    if _exam_one_catch:
        mc "Am I... allowed?"
        show asahina neut
        "Asahina stops halfway to the rug, and Mom's hand settles on the lid."
        show mom sad
        mom "You came home when you said you would, and the laptop hasn't moved. One round is still one round."
        mc "That's not--I meant with you two."
        "This time, Mom doesn't pretend she misunderstood."
        mom "Yes, with us. Come sit down."
    else:
        mom "You both survived exams, and I am offering violence with cards before either of you disappears upstairs."
    mc "This is the game where you buy six useless villages and somehow make us pay for all of them."
    show mom unamused
    mom "They become useful when you build around them."
    show asahina neut
    ah "I have homework."
    "Her phone is still in her hand, the blue schedule open under her thumb."
    show mom smug
    mom "Tomorrow's biology can wait for tomorrow. You'll be done before bed."
    "Asahina appeals to me for backup."
    mc "You're on your own."
    show asahina unamused
    ah "Coward."
    # SFX SUGGESTION: Clean card shuffling and three hands dealt across the floor.
    "She drops onto the rug and leaves the space beside her open. Mom settles on the floor across from us and is dealing by the time I sit down."
    "Copper Crown starts each of us with seven coins, three laborers, and enough bad options to build an economy."
    show mom determined
    mom "Standard rules. No expansion cards."
    ah "Why not the sabotage expansion?"
    mom "Because your brother still argues about the Smuggler card every time it appears."
    mc "The rulebook says reveal, not discard."
    show mom unamused
    mom "The errata says discard."
    mc "They changed it after publication! I had already won the argument."
    show asahina frustrated
    ah "See? This is why nobody plays with either of you."
    show mom teasing
    mom "And yet here you are."
    "Asahina buys a Militia right away and starts attacking with a deck that can't back it up yet. Mom buys a single Quarry and trashes two starting cards with it, and by her third turn she's quietly drawing cleaner hands than either of us."
    mc "Already thinning?"
    show mom neut
    mom "If it helped on turn one but keeps wrecking my draw now, why would I keep it?"
    show asahina unamused
    ah "That sounded targeted."
    show mom smug
    mom "I said {i}card{/i}, Asahina."
    "Asahina answers by hitting both of us with Militia again. It does wonders for her mood."
    show asahina happy
    ah "Conscience says draw three."
    mc "Your conscience is a war criminal."
    "By the fifth round, Asahina owns nearly every attack card in the market, my expensive engine keeps arriving in the wrong order, and Mom's tiny deck produces yet another Crown."
    show asahina shocked
    ah "How do you have {i}another{/i} Crown?!"
    mom "Three useful cards."
    # SFX SUGGESTION: A work-phone ringtone intruding at full volume, then repeating below.
    "Mom's phone rings just as she lifts her next card."
    "A name from work lights the screen on the coffee table, and none of us moves."
    show mom unamused
    "She leaves the card suspended over the market row."
    mom "I told them {i}tomorrow{/i}."
    "The phone rings again."
    show mom determined
    "She sets the card facedown."
    mom "Do not touch my board."
    show asahina teasing
    ah "We have honor."
    mc "She means do not count her points."
    mom "Especially that."
    show mom at thide
    hide mom
    "She carries the call into the kitchen, her work voice coming through the wall without a single useful detail in it. Asahina waits until it settles into a rhythm, then counts Mom's three neat piles."
    show asahina unamused
    ah "She's winning."
    mc "By a lot."
    show asahina determined
    ah "We could stop attacking each other for, like, two turns and take one of her Provinces."
    mc "A coalition against Mom."
    ah "Oh, please. You'd sell me out for a Workshop."
    "I look from Asahina's pile of attack cards to the Crown Mom is going to buy the moment she sits back down."
    mc "What are your terms?"
    ah "Leave the last Militia for me, and I stop hitting you until she loses a Province."
    mc "Two turns."
    ah "Three."
    mc "Two, and I get first pick of the next good card."
    ah "Deal."
    "Asahina spits in her palm before we shake on it over the discard pile. I shake anyway, since the alternative is losing to Mom."
    "The agreement is about thirty seconds old when Mom comes back."
    show mom thinking at t22
    "She sits, turns her facedown card over, and studies the two of us until Asahina shifts on the rug."
    mom "What did you agree to?"
    show asahina neut
    ah "Nothing."
    mc "We were discussing our independent plans."
    show mom smug
    mom "So you coordinated badly. Understood."
    "Mom buys the Crown over our objections, and the alliance lasts exactly until Asahina draws both Militias and hits me early."
    "I take the Workshop she wanted out of pure spite. By the time she retaliates, Mom doesn't need to lift a finger."
    "When the last Province leaves the market, Mom wins by eleven points."
    show asahina frustrated
    ah "No. That score is fake."
    show mom unamused
    mom "Count again."
    "We count it together, and somehow the margin grows to twelve."
    mc "Recounting made it {i}worse{/i}."
    show mom smug
    mom "Then you should both be grateful we checked."
    # SFX SUGGESTION: A soft full-body thump into the rug.
    "Asahina lets herself fall backward onto the rug, one card still trapped under her hand."
    show asahina determined
    ah "Rematch Sunday. Sabotage expansion."
    show mom determined
    mom "After homework."
    ah "Fine. I'm cutting biology down to forty-five minutes. Watch me."
    mom "Then we can play after lunch."
    show asahina happy
    "Asahina raises one fist from the floor, still flat on her back."
    ah "Sunday."
    show mom happy
    "Mom leans over the market row and taps her knuckles against it."
    mom "Sunday."
    "Mom starts sorting the market cards into their labeled slots while I gather the starting decks. Asahina stays horizontal until Mom sets a stack on her stomach and leaves it there."
    if _exam_one_catch:
        $ update_character_thought("mom", "Mom included me in one round of Copper Crown after the conduct meeting and agreed to a Sunday rematch with Asahina. She took a work call mid-turn and still beat us.")
    else:
        $ update_character_thought("mom", "Mom marked the end of exams with one round of Copper Crown and agreed to a Sunday rematch with Asahina. She took a work call mid-turn and still beat us.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The box goes back under the television with its tape intact, and Mom's work phone stays facedown by the sink for the rest of the night."
    call nier_clear from _call_nier_clear_0529_6_5
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music night_a
    "The review sheets are in a folder shoved out of sight, and the calculator has retired to its quieter life as a paperweight."
    "I'm partway into a dungeon when my phone lights up beside the controller. Matsuda, naturally."
    python:
        _phone_messages = [
            phone_msg("them", "Kareda has informed me that melon bread is not dinner."),
            phone_msg("me", "She's right."),
            phone_msg("them", "Tyranny often begins with nutrition."),
            phone_msg("me", "So does staying alive. Eat something."),
            phone_msg("them", "Et tu, sidewalk? Fine. Goodnight, " + player + "."),
            phone_msg("me", "Night."),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, append=True) from _call_phone_text_conversation_0529_4
    # She is texting him her evening as a bit now, unprompted, twelve days in.
    # Pointing a camera at him is the next thing she would escalate to.
    $ phone_open("matsuda_video")
    "I push the phone aside and get back to the game, where the party has reached a checkpoint and a horned gatekeeper wants to know which banner we serve."
    mc "...Still neutral."
    "The gatekeeper stamps my travel pass, no follow-up questions, and the dungeon opens on the other side."
    $ update_character_thought("matsuda", "At lunch, Matsuda played a painfully shy schoolgirl to invite Asahina and me to a book sale and an arcade, stammering and offering to wait by the gate before she dropped the act and promised to send the plan. Tonight she reported that Tsubaki has ruled melon bread is not dinner.")
    $ hide_calendar()
    scene black with wipeleft_scene
    if _exam_one_catch:
        nier "At ten I take my phone down to the kitchen charger. Mom looks up from the table, and neither of us calls the day settled."
        nier "But she nods when I head back upstairs."
    else:
        nier "Thursday ends at a checkpoint, with my alarm set back to a regular school morning. Somewhere across town, Tsubaki is probably negotiating a vegetable into Matsuda's dinner."
    call nier_clear from _call_nier_clear_0529_7
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0529_1
    jump a0530
