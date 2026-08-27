define planner_0516_saturday = (
    ("SCHOOL", "Turn in my English homework, finish essay rough draft, survive classes."),
    ("ERRAND", "Get game."),
    ("ERRAND", "Grab glue for Stinky's poster."),
    ("MAYBE", "Look at that school with Mom."),
)

define planner_0516_sunday = (
    ("TEXT", "Monika in the morning, don't let her beat you."),
    ("PLAN", "Horror flick with Monika."),
    ("REMINDER", "Do NOT get lost in press-turn battles."),
    ("MAYBE", "Work on that piece I promised I would.")
)


label a0516:
    # --- Day 2: 2025-05-16 ---
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music dailyleisure
    window auto
    "Last night's reminder goes off before my alarm gets a turn, so Asahina's errand reaches my brain before anything of mine does."
    # SFX SUGGESTION: A phone vibrating against wood, followed by a distant toaster pop.
    "The phone buzzes its way toward the edge of the desk. I nearly kick the corner of the bed reaching for it, and downstairs the toaster announces that the rest of the house has already accepted reality."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    $ atmos("home", particles="motes")
    with wipeleft_scene
    show mom uniform neut at t22
    "Mom is still in the kitchen when I come in, moving between the toaster and stove without looking rushed."
    show asahina uniform thinking at t21
    "Asahina sits at the table with her head tilted over one shoulder while she tries to fix a twist in her sleeve by feel alone."
    mc "Morning."
    mom "Morning, [player]."
    show mom uniform teasing
    mom "Eggs are almost done, so don't disappear upstairs again."
    show asahina uniform neut
    ah "He just got here, Mom."
    mc "No, no, she does have a point."
    show mom uniform smug
    mom "Exactly."
    "I take my seat and reach for the cranberry juice in front of me."
    "Asahina catches me looking at the sleeve and narrows her eyes."
    mc "...I wasn't going to say anything!"
    show asahina uniform unamused
    ah "You were thinking it with your whole face."
    "Mom plates the eggs and sets them down."
    show mom uniform neut
    mom "Food first, commentary after."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Mom asks about homework while I answer vaguely. Across the table, Asahina pretends not to smile at whatever lit up her phone."
    call nier_clear from _call_nier_clear_0516_1
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    show mom uniform neut at t22
    show asahina uniform neut at t21
    $ atmos("home")
    with wipeleft_scene
    "I finish the last of my toast and push my plate forward."
    mc "Glue tomorrow. Big bottle, not the stick."
    ah "Mhm."
    show mom uniform curious
    mom "The poster you were supposed to start last week?"
    "Asahina's expression tightens by about one millimeter."
    show asahina uniform unamused
    ah "...The same poster I was absolutely, totally, one-hundred-percent starting tonight."
    mc "So it's gone from idea to actual threat."
    show asahina uniform smug
    ah "Keep talking and I'm making you pose for it."
    mc "I'd rather die. Also catch me if you can."
    show asahina uniform pose_hairflip
    ah "With THAT bum foot? HA!"
    show asahina uniform smug
    show mom uniform teasing
    mom "I'd frame the attempt, at least."
    mc "...Et tu, Brute...?"
    "{i}At least the eggs are good.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "A few minutes later, we're out the door. Asahina leaves first, still pretending she isn't rushing."
    nier "I check my bag and lanyard twice, along with the loose obligations apparently required for personhood."
    call nier_clear from _call_nier_clear_0516_2
    stop music fadeout 1.0
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with dissolve_scene_full
    play music quiz
    "By the afternoon, I'm sitting through college-level algebra."
    "On a transcript, the class probably looks clean and impressive. In person, it immediately starts swinging a chair the second you sit down."
    show math_teacher neut at t11
    math_teacher "All right, everyone. Last time we covered transformations of logarithmic functions."
    math_teacher "Today, we're combining that with domain restrictions."
    "Chalk taps against the board."
    show math_teacher neut
    math_teacher "Suppose we have f(x) equals log base two of x minus one, plus three."
    math_teacher "Before we talk about the graph itself, can anyone tell me what the domain is?"
    "A few students look down at their notes like the answer might crawl out and save them."
    "Unfortunately, I make the mistake of looking halfway attentive."
    math_teacher "[player], you surely know the answer, right?"
    math_teacher "Come on, it's a layup."
    $ atmos_pressure()
    with dissolve
    "{i}Right. Death by eye contact. Classic mistake.{/i}"
    menu:
        "x greater than one":
            jump rightanswer1
        "x less than one":
            jump wronganswer1
        "x":
            jump wronganswer1
    label rightanswer1:
        $ atmos_pressure_clear()
        with dissolve
        math_teacher "Correct. Why?"
        mc "Because the argument of the logarithm has to be positive, so x minus one has to be greater than zero."
        "The teacher underlines the x minus one part twice."
        show math_teacher neut
        math_teacher "The shift affects where the graph can exist, not just where it looks nice."
        math_teacher "And believe me, get used to functions looking like this. Higher-level math is all sorts of ugly."
        "A few pencils move across paper, and others...well..."
        math_teacher "Now, for the vertical shift..."
        jump answer1done
    label wronganswer1:
        $ atmos_pressure_clear()
        with dissolve
        math_teacher "Not quite. Remember that the argument of a logarithm must be positive."
        math_teacher "So x minus one has to be greater than zero, which means x must be greater than 1."
        mc "Oh...right. Got it."
        "A few students murmur and write the correction down."
        jump answer1done
    label answer1done:
        pass
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Equations, graph sketches, one student asking whether this will be on the exam, and the teacher answering with a smile that says absolutely."
    nier "By the end of class, my notebook has more arrows than actual words."
    call nier_clear from _call_nier_clear_0516_3
    stop music fadeout 1.0
    pause 2.0
    scene bg club_day
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with wipeleft_scene
    play music dailyfantasy
    "After school, I reach the club room a little late. The bathroom break was poorly negotiated."
    "I expect the usual occupied desks and overlapping voices, probably centered on whether a poem can be too purple."
    show monika forward uniform dist cm oe nobl rdown ldown at t11
    "Monika is already here, flipping through a thin notebook with a pen tucked behind her ear. Nobody else is."
    m forward uniform happ om oe nobl rdown ldown "Hey, you made it!"
    mc "Against all odds. Where is everybody?"
    m forward uniform neut cm oe nobl rdown ldown "Hikari has tutoring on Fridays, and Homura goes wherever Hikari goes."
    m forward uniform happ om oe nobl rhip ldown "They'll be back Tuesday to argue about commas."
    m forward uniform nerv om oe awkw rdown ldown "As for everyone else, they, uh...all collectively told me they were gonna run late."
    mc "I see..."
    m forward uniform curi om oe nobl rdown ldown "Rough day?"
    mc "Not really. Algebra noticed me looking alive and decided to correct that."
    m forward uniform happ om oe nobl rdown lpoint "Well? Did you at least survive with your dignity?"
    mc "I gave an answer, got zero applause, so it's still under review."
    m forward uniform wry cm ce nobl rdown ldown "Wow. This school really is falling apart..."
    "I take my usual seat and drop my bag beside the desk."
    "She closes her notebook halfway, keeping one finger between the pages."
    m forward uniform happ om oe nobl rhip ldown "Today's agenda is pretty light. I was thinking we could read for a bit, then workshop whatever you brought yesterday some more."
    mc "You mean the draft with all the brackets still in it?"
    m "That's the one~"
    m forward uniform neut cm oe nobl rhip ldown "The brackets are useful, actually. Take that first stanza: I think the metacommentary works in your favor."
    mc "You're making my bad habits sound organized."
    m forward uniform wry cm oe nobl rhip ldown "Only because they are. That's why I can find them so easily."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Monika reads with the focused little frown she gets when she's trying not to rewrite an entire paragraph in her head. Much to my chagrin, she crosses out an entire section I thought was clever."
    call nier_clear from _call_nier_clear_0516_4
    pause 2.0
    scene bg club_day
    $ show_calendar()
    show monika forward uniform anno cm oe nobl rdown ldown at t11
    $ atmos("evening")
    with wipeleft_scene
    "By the time the light outside begins to wane, Monika stacks her notebook on top of mine."
    m forward uniform happ om oe nobl rdown ldown "There. Nothing too brutal, right?"
    mc "It was within the blast zone, yeah."
    "She turns my second page around. Beside a line I'd buried three brackets deep, her neat slant reads:"
    "{i}You're describing how this looks here so that you can avoid the elephant in the room.{/i}"
    "I read it twice."
    mc "...I think you're making me catch strays."
    m forward uniform happ om ce nobl rdown lpoint "Consider it a freebie."
    "I slip the papers back into my bag. The sentence can commute by itself."
    mc "Anything I need to remember for tomorrow?"
    m forward uniform curi om oe nobl rhip ldown "Tomorrow? Survive classes, first of all."
    mc "I'll...pencil that in."
    show monika forward uniform laug om ce nobl rdown ldown at h11
    m forward uniform laug om ce nobl rdown ldown "Saturday classes, at least. TGIS, am I right?"
    m forward uniform wry om oe nobl rhip ldown "No club afterward, though. I'm not spending my free afternoon pretending to be responsible."
    m forward uniform happ cm oe nobl rhip ldown "And text me Sunday morning so we can pick a time."
    "I take a deep sigh."
    mc "...Will do."
    m forward uniform wry om oe nobl rdown lpoint "Now go home before I find another responsibility to hand you."
    mc "Before the list grows, then. Later, Monika."
    show monika at thide
    hide monika
    play sound moddoorclose
    "She waves me off, and I take the exit while it is on offer."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The walk home follows its usual route until the vending machine. It has been sold out of one particular drink all week."
    call nier_clear from _call_nier_clear_0516_5
    pause 2.0
    scene bg residential_day
    $ show_calendar()
    $ atmos("overcast")
    with wipeleft_scene
    "I slow down near the corner store when I notice someone standing by the curb with a neatly folded umbrella tucked under one arm."
    show kotonoha casual neut at t11
    "It's Kotonoha, who is technically in my year, though most people know her by sight before they know anything else."
    "She is always either coming from somewhere or going somewhere. Nobody I know has ever seen her arrive."
    mc "Oh. Hey, Kotonoha."
    ko "Good afternoon, [player]."
    mc "Waiting for someone?"
    ko "A bus."
    mc "Right. That would make sense at a bus stop."
    ko casual unamused "It's running late."
    mc "Yeah...they do that."
    "A light breeze passes through the street. She adjusts the bag in her hand, and the convenience store logo crinkles under her fingers."
    show kotonoha casual neut
    mc "Coming from work?"
    ko "One of them."
    "I nod, because that's how people generally answer Kotonoha. You simply keep the line moving."
    mc "Long day, then."
    ko "Average."
    "{i}For her, maybe.{/i}"
    # SFX SUGGESTION: Wet tires passing close, ending in a short gutter splash.
    "A car rolls by, kicking up a brief hiss of water from a shallow gutter puddle. She steps back as the water reaches the curb."
    mc "Woah, good timing."
    ko "I watch where cars are."
    mc "Useful habit."
    ko casual thinking "Most people watch where cars were."
    mc "...Huh."
    # SFX SUGGESTION: A distant bus engine groan with a soft pneumatic-brake hiss.
    show kotonoha casual neut at t21
    "The bus finally groans around the corner in the distance."
    ko "Oh, that's mine."
    mc "Yeah. Guess I'll see you around."
    ko casual teasing "Probably. We keep ending up in the same five minutes."
    show kotonoha casual neut
    "She gives a small bow, then steps toward the curb as the bus pulls in."
    show kotonoha at thide
    hide kotonoha
    "The bus leaves a wet tread mark along the curb and a fading engine groan."
    $ mark_character_met("kotonoha")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The rest of the walk goes quiet. My brain starts making gibberish out of normal things."
    nier "I look along the power lines and imagine a badass dude running on them without any other objective."
    nier "{i}Damn, I wish that were me.{/i}"
    call nier_clear from _call_nier_clear_0516_6
    play sound moddooropen
    pause 2.0
    scene bg home_entry_day
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    play sound moddoorclose
    "When I step inside, there is already an unfamiliar pair of men's loafers lined up near the entrance."
    "{i}Please don't let this be one of Mom's surprise errands in human form.{/i}"
    mc "I'm home..."
    ah "Living room!"
    "Her voice lands halfway between a summons and the opening move of a prank."
    $ hide_calendar()
    pause 2.0
    scene bg living_room
    $ show_calendar()
    show asahina uniform determined at t31
    show sam uniform neut at t33
    $ atmos("home")
    with wipeleft_scene
    "Asahina is standing near the couch, arms folded in a way she keeps adjusting. Beside her is a guy I recognize mostly from context clues."
    ah "This is Sam."
    "{i}Look at me, solving mysteries in my own living room.{/i}"
    sa "Hey, I'm Masayami Inugami, but basically everyone calls me Sam. Please do the same."
    mc "[player]."
    mc "...I'm the brother."
    show sam uniform happy
    sa "So I've heard!"
    show asahina uniform happy
    ah "All good things though, so don't get mad."
    mc "Good things, huh?"
    show sam uniform smug
    sa "...Mostly good things."
    "Asahina elbows him in the side, but he takes it like he saw it coming five seconds ago."
    show asahina uniform annoyed
    ah "I said ALL good things."
    show sam uniform teasing
    sa "You said he was smart, sarcastic, and impossible in the morning."
    mc "Hey, that's more of a profile than I expected. I'd think she'd completely drag my name through the mud."
    "He offers his hand. The handshake is firm and brief."
    show sam uniform neut
    "I hate that I notice that."
    mc "So, uh...welcome."
    sa "Thanks for having me."
    show sam uniform nervous
    sa "And, ah...sorry for dropping in without much warning. I'd be mad about short notice too."
    show asahina uniform teasing
    ah "There was some warning, ya goof~"
    mc "There was?"
    show asahina uniform smug
    ah "Yeah! I told Mom."
    mc "Wooooow, incredible. Seems like the mailing list has me blocked."
    show sam uniform smug
    sa "If it helps, I'm not on it either."
    "He catches the awkwardness and redirects it at himself. Annoyingly effective."
    "He's been nothing but friendly. That's sort of the problem, actually."
    play sound moddooropen
    "...Then again, it's only been two nanoseconds."
    play sound moddoorclose
    show mom uniform happy at t32
    mom "Ah, you're home!"
    mom "Sam, this is my son, [player]. [player], this is Sam."
    mc "We got through the tutorial already."
    show mom uniform smug
    mom "Good. Then I can skip the part where I remind everyone of the house rules."
    show mom uniform teasing
    mom "...BUUUUUUUUT I'm going to reiterate them anyway so that everyone hears me loud and clear."
    show asahina uniform embarrassed
    ah "Mom..."
    show sam uniform pose_crossed
    "Mom points at my sister."
    mom uniform pose_objection "Doors stay open, no exceptions. Homework comes before movies."
    mom "Absolutely zero PDA under any circumstances."
    "She points from Sam to Asahina, then to me."
    show mom uniform neut
    mom "And if anyone gets hungry, there are leftovers."
    "Sam's eyes flick toward Asahina, then back to Mom."
    sa uniform determined "Understood, ma'am."
    show mom uniform smug
    mom "Good answer."
    show asahina uniform smug
    ah "See? He's not an alien, bro."
    mc "I never said he was! Don't put words in my mouth."
    show asahina uniform unamused
    ah "You did the face thing again."
    mc "...There's so much wrong with you."
    sa "For what it's worth, I get it. If I had a younger sister bringing a guy home, I'd probably do the same kinda scan."
    mc "Oh?"
    sa "Shoes, posture, handshake, whether I say something stupid in the first thirty seconds..."
    "{i}Okay, now that's just unfair.{/i}"
    mc "You passed two and a half."
    sa "Out of?"
    mc "...Classified."
    "He shrugs."
    sa "I'll take it."
    show asahina uniform teasing
    ah "Don't encourage him, he's a freaking weirdo."
    "A smile keeps tugging at one corner of her mouth."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Mom heats leftovers while Asahina and Sam spread homework across the coffee table. Only one of them treats homework as the main event."
    call nier_clear from _call_nier_clear_0516_7
    pause 2.0
    scene bg kitchen_evening
    $ show_calendar()
    show mom neut at t22
    show sam uniform neut at t21
    $ atmos("home")
    with wipeleft_scene
    "Later, I find him in the kitchen rinsing a glass while Mom packs the last of the rice into a container."
    mom "You don't have to do that, Sam."
    sa "It's fine, really. I used it, so I should clean it."
    mc "Careful. If you keep being useful, she'll invite you back."
    mom "He can come back."
    "Sam's grin breaks wide before he can smooth it back down."
    sa uniform happy "I'd like that."
    "Asahina, from the living room, makes a triumphant noise."
    ah "Booyah!"
    mom angry "Homework!"
    ah "...Yes, ma'am..."
    "The victory dies instantly."
    show sam uniform neut
    mom curious "Think Asahina will take this for lunch tomorrow? She barely touched dinner."
    "Sam dries the glass and glances toward the living room. The towel stops in his hands."
    sa neut "She's been working hard, you know."
    mc "At volleyball? School?"
    sa uniform thinking "That too, but..."
    sa uniform nervous "I probably shouldn't be the one saying this."
    mom curious "Saying what?"
    sa uniform thinking "She's been trying hard to eat better lately. Cutting back on junk, mostly."
    "He says it to the glass he's drying, without looking up."
    "{i}Mom is standing three feet away, and Sam still lowers his voice.{/i}"
    sa uniform worried "I want to support her. I just don't want to make it weird."
    mc "Yeah. She's modest like that."
    sa uniform determined "I noticed. Still, you gotta respect someone who wants to better themself."
    "Mom presses the lid onto the container. It takes her two tries."
    $ mark_character_met("sam")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Sam leaves sometime after dinner. Asahina walks him to the door and takes three times longer than necessary to come back inside."
    nier "Nobody comments on it."
    call nier_clear from _call_nier_clear_0516_8
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music fantasypassion
    "By night, I am back in my room with my phone in one hand and my planner open on my desk."
    "I only get the planner out when memory alone has started to feel like a terrible idea, and this not-quite-weekend qualifies. Saturday still has school attached to it like a punishment with better branding."
    call enter_m_show_planner("SATURDAY", "MAY 17", planner_0516_saturday, "SUNDAY", "MAY 18", planner_0516_sunday, "chip restitution = Asa's problem", "'date' is a normal word. stop thinking about it.") from _call_enter_m_show_planner_0516_1
    "{i}My free time already feels pre-owned.{/i}"
    "A muffled laugh rises from downstairs, probably Asahina texting Sam. Mom says something after that, too faint for me to catch."
    $ hide_calendar()
    scene black with dissolve_scene_full
    nier "The checklist stays open beside a tired brain. My phone's blue glow fades into sleep mode."
    call nier_clear from _call_nier_clear_0516_9
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0516_1
    jump a0517
