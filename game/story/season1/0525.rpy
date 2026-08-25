label a0525:
    # --- Day 11: 2025-05-25 ---
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music dailyleisure
    window auto
    "I beat the first alarm by one minute."
    "Not fifteen minutes after it, not in the middle of a dream where a coffee mug started accusing me, one minute before. Completely unheard of for me"
    "The screen reads 7:14. The other three alarms sit beneath the first like backup prosecutors, in which I disable all of them."
    "For a few seconds, I stay under the blanket and listen."
    # SFX SUGGESTION: Sparse house ambience: a pipe tick, low refrigerator hum, and one car passing outside.
    "Pipes settling, the faint hum of the refrigerator downstairs, somebody's car passing on the street with no interest the world."
    "My bag is already packed beside the desk. Oddly enough, I don't remember prepping it."
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
    nier "My breakfast was more peaceful, without a nagging sister and a silently judgmental mother."
    nier "It took me not long to finish eating, that way I had a sliver of time to relax and see my weekend exactly as it is instead of some calm before the storm."
    nier "Soon enough, I'm out the door."
    nier "The trip downtown is too ordinary to complain about. The bus is half-empty. The morning streets are washed in clean light. A kid across the aisle kicks his shoes against the seat until his mother gives him a glare."
    nier "I text Mom when I reach the library steps, because she asked and because forgetting would create its own problem."
    call nier_clear from _call_nier_clear_0525_2
    stop music fadeout 1.0
    pause 2.0
    scene bg city_morning
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music daily
    "The public library sits above the sidewalk, having watched generations of students panic under better lighting."
    "{i}Good morning, library.{/i}"
    "{i}Please be useful by noon...{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    scene enter_m_op_bg_library
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    "The second floor smells like paper and carpet cleaner. Sunlight falls across the study tables in pale rectangles, and the textbooks look briefly innocent."
    "Monika is already there, seated at a place that visibly screams that it's a meeting spot."
    show monika forward casual dist cm oe nobl rdown ldown at t11
    "{i}Of course she is already there, what else did I expect?{/i}"
    "Two chairs arranged and a row of sticky notes color-coded with quiet conviction."
    "Her hair ribbon is tied neatly, though her eyes look less so."
    m forward casual happ om oe nobl rdown ldown "Look who made it~"
    mc "I did promise, didn't I?"
    m forward casual wry cm oe nobl rhip ldown "You also promised to sleep at a reasonable time."
    mc "By my standards, I did. The hour is between me, myself, and I."
    "She gestures to the non-vacant chair, begging to be sat on."
    m forward casual happ om ce nobl rhip lpoint "Just saying, the padding on these are like heaven..."
    mc "Oh yeah?"
    "I take not a second longer before placing myself into a vindictive seat."
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
    "Her hand is close enough to pass me a card without either of us needing to stand."
    m om lpoint "Okay, Mr. Smartass, no idle chatting then. Warmup question, since you want to hit the ground running."
    m "Wait, hold on--"
    "She holds up a notecard with presumably a question on it."
    m "When a court strikes down a law because it conflicts with the constitution, what principle is being applied?"
    mc "Judicial review."
    m forward casual curi om oe nobl rhip ldown "Definition?"
    mc "The judiciary reviews government action for constitutional compatibility."
    
    # rewriting this whole section because it felt unnaturally paced and the whole hangout with monika and subsequent scenes should be:
    # MC finds monika and has that whole thing above
    # warmup question followed by some lighthearted banter before the REAL study session (you know, "how's it going?" and all that)
    # actual study session that isn't just rattling off notecards with a question-answer exchange. actually have it be interactive with player input and everything. all exam questions do have to be covered in some capacity though'
    # during the study session, have cuts to black to show progression of time and windows that cover each subject, that way it's not all in one chunk
    # noon hits, they break for the day, and go to the cafe
    # random street conversation about the club and everything (should also take a subtle jab at DDLC and its modding scene for if the player knows)
    # cafe date. kotonoha is the barista. MC and monika have a tender heart-to-heart (NOT DATING) and it's just overall a feel-good scene
    # after saying goodbye, mc gets home to asahina doing her own cramming and notices that she has the same books and everything from when HE was a first-year (not the same content as his senior schedule, but you get what i mean)
    # scene to the next one with his jog and getting butt-dialed by mom. residential_day should have an evening atmosphere/filter

    scene bg residential_day
    $ show_calendar()
    $ atmos("evening")
    stop music fadeout 1.0
    with wipeleft_scene
    play music dailyleisure
    "The evening air is cooler than the afternoon, and the pavement is still holding onto the day."
    "I start slow. Actually slow, knowing that Coach would have my hide if I showed up a double cripple."
    "My foot stays quiet, thankfully."
    # SFX SUGGESTION: Even running footfalls and measured breathing, briefly isolated from the music.
    "Footfall. Breath. Shoulder loose. Turn at the corner."
    "My phone buzzes in mt hand, completely interrupting my playlist and subsequent adrenaline."
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
            phone_call_line("them", "Oh, for-- did I call you? I put my phone away in my bag two minutes ago."),
            phone_call_line("me", "And lost the round, it seems."),
            phone_call_line("them", "The plums here started it!"),
            phone_call_line("them", "Wait-- why are you breathing like that. Are you running?"),
            phone_call_line("me", "Easy jog. Heavy emphasis on easy."),
            phone_call_line("them", "I can hear the emphasis working very hard to cover for you."),
            phone_call_line("me", "I'm basically walking."),
            phone_call_line("them", "Then keep basically walking. It's the night before exams, not-- hang on--"),
            phone_call_line("them", "...yes, just these two, thank you-- no, I don't need a bag..."),
            phone_call_line("me", "...You still alive over there?"),
            phone_call_line("them", "I'm checking out right now. It's always fine checking out. Hey-- miss? I have a case of water under here that stll needs scanned."),
            phone_call_line("me", "Sounds like you're having a lot of fun."),
            phone_call_line("them", "Okay, I actually have to-- be home before it's fully dark, please."),
            phone_call_line("me", "Yeah. Already turning back."),
            phone_call_line("them", "Good. And drink some-- you know what, you already know."),
            phone_call_line("me", "There it is."),
            phone_call_line("them", "Love you, sweetheart-- ugh, the card reader won't-- okay, one second--"),
            phone_call_line("me", "Love you. Go rage against the machine."),
            phone_call_line("them", "Always do."),
        ]
    call phone_call_conversation("Mom", _phone_call_lines, status="Connected") from _call_phone_call_conversation_0525_1
    # Her pocket called him and she ran the whole errand out loud anyway. After
    # this, "where is the big pot" is a call she would obviously make.
    $ phone_open("mom_call")
    "The call ends."
    "I stand on the sidewalk with the phone in my hand and the evening cooling at the back of my neck."
    "I put the phone away and jog home slower than before."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Mom comes home with groceries, asks Asahina three questions that sound casual and function like a study audit, then makes tea and declines to hold court over it."
    call nier_clear from _call_nier_clear_0525_8
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home_night")
    stop music fadeout 1.0
    with wipeleft_scene
    "Night returns me to my desk."
    "The review sheets are still there. The alarm list is still there. Tomorrow is still there."
    "I review lightly."
    "Enough to keep the shape. Not enough to scrape the paint off it."
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
    "I put the phone away, then actually put the notes away too."
    "My room looks cleaner without the papers spread open."
    "{i}Tomorrow there's no folder to reopen. No draft. No bracket to hide the part I'm not sure of.{/i}"
    "{i}Whatever I put on the page is the answer. That's supposed to be the simple part.{/i}"
    "{i}Tonight it sounds more like a warning.{/i}"
    "Downstairs, a cabinet closes."
    "Sunday has been too gentle. Gentle in a way that makes Monday look sharper by contrast."
    "That should be comforting."
    "Mostly, it is."
    "Mostly."
    $ update_character_thought("monika", "Monika reserved the table, brought flashcards for subjects she isn't taking, and told me she'd rather bomb Monday than fake it.")
    $ update_character_thought("asahina", "Asahina's first-year science packet is the same photocopy I got two years ago. She waited until panic had a pulse before asking, then let me help anyway.")
    $ update_character_thought("kotonoha", "Kotonoha works Sundays at the cafe by the old bank. This is apparently normal, which makes it more impressive.")
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
