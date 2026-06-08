label a0516:
    # --- Day 2: 2025-05-16 ---
    scene bg kitchen
    $ show_calendar()
    show mood_home zorder 3 
    with dissolve_scene_full
    play music dailyfantasy
    window auto
    "The next morning starts before I feel ready to participate in it."
    "My phone buzzes itself toward the edge of the desk, I nearly kick the corner of the bed, and downstairs the toaster announces that the rest of the house has already accepted reality."
    "Mom is at the counter when I come in, moving between the toaster and the stove with the practiced efficiency of someone who has made school mornings survivable through repetition."
    show mom neut at t22
    show asahina neut at t21
    "Asahina sits at the table with her head tilted over one shoulder while she tries to fix a twist in her sleeve without looking down."
    mc "Morning."
    mom "Morning, [player]."
    mom "Eggs are almost done, so don't disappear upstairs again."
    
    ah "He just got here, mom."
    
    mc "Past behavior casts a long shadow."
    mom "Exactly."
    "I take my seat and reach for the glass of water in front of me."
    "Asahina finally notices me watching her sleeve and narrows her eyes before I can say anything."
    mc "I wasn't going to say it."
    
    ah "You were thinking it with your whole face."
    
    "Mom plates the eggs and sets them down with enough finality to end the conversation."
    mom "Food first. Commentary after."
    mom "Now both of you, eat."
    show mom at thide
    hide mom
    show asahina at thide
    hide asahina
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Breakfast settles into the ordinary rhythm: mom asking about homework, me answering just enough to avoid a second question, and Asahina pretending not to smile at whatever message lit up her phone."
    nier "It lasts maybe fifteen minutes, which is long enough for the house to feel awake and short enough for nobody to make a speech out of it."
    call nier_clear from _call_nier_clear_0516_1
    scene bg kitchen
    $ show_calendar()
    show mom neut at t22
    show asahina neut at t21
    show mood_home zorder 3 
    with wipeleft_scene
    "I finish the last of my toast and push my plate forward."
    # CRITIQUE: The continuity from the glue errand is useful, but this exchange escalates to a suicide joke over a poster. For low-stakes sibling banter, that is cheap heat and makes the family tone wobble.
    mc "You're still expecting glue tomorrow, right?"
    
    ah "Yes. I have been accused of many things, but not forgetting favors that benefit me."
    
    mc "That's almost self-awareness."
    mom "And what is the glue for again?"
    
    ah "Volleyball recruitment poster. Theoretically."
    
    mom "The one you were supposed to start last week?"
    "Asahina's expression tightens by approximately one millimeter."
    
    ah "...Yeah. The same poster I was absolutely, totally, one-hundred-percent starting tonight."
    
    mc "So it has moved from concept to threat."
    
    ah "Keep talking and I'm making you pose for it."
    
    mc "I'd rather kill myself."
    mom "I'd frame it."
    mc "...Really, mom? You too...?"
    "{i}At least the eggs are good.{/i}"
    show mom at thide
    hide mom
    show asahina at thide
    hide asahina
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "A few minutes later, we're out the door."
    nier "Asahina leaves first, still pretending she isn't rushing."
    nier "I follow after double-checking my bag, my lanyard, and the loose collection of small obligations that apparently make up a human life."
    call nier_clear from _call_nier_clear_0516_2
    scene bg class_day
    $ show_calendar()
    show mood_afternoon zorder 3 
    with dissolve_scene_full
    # CRITIQUE: The algebra scene is cleanly staged, but it is isolated from MC's actual pressures. If school scenes recur, they need either theme, character pressure, or plot utility beyond "teacher asks question."
    # CRITIQUE: Worldbuilding check: "college-level algebra," "honor students," and later "ma'am" push the school toward an American register despite the Japanese-calendar framing. If this is a hybrid setting, establish that deliberately; if not, localize the academic/social terms.
    "By late morning, I'm sitting through college-level algebra, which is the part of the school day that exists to remind honor students that the word \"honor\" is mostly a threat."
    "On a transcript, the class probably looks clean and impressive. In person, it immediately starts swinging a chair the second you sit down."
    "Our teacher writes a function on the board with such clean handwriting that it somehow makes the problem look more insulting."
    show math_teacher neut at t11
    math_teacher "All right, everyone. Last time we covered transformations of logarithmic functions."
    math_teacher "Today, we're combining that with domain restrictions."
    "Chalk taps against the board."
    math_teacher "Suppose we have f(x) equals log base two of x minus one, plus three."
    math_teacher "Before we talk about the graph, what's the domain?"
    "A few students look down at their notes like the answer might crawl out and save them."
    "Unfortunately, I make the mistake of looking halfway attentive."
    math_teacher "[player], you surely know the answer, right?"
    math_teacher "Come on, it's a layup."
    show mood_pressure zorder 4
    show vignette zorder 5 at ambient_vignette(0.28)
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
        hide mood_pressure
        hide vignette
        with dissolve
        math_teacher "Correct. Why?"
        mc "Because the argument of the logarithm has to be positive, so x minus one has to be greater than zero."
        math_teacher "Exactly."
        "The teacher underlines the x minus one part twice."
        math_teacher "The shift affects where the graph can exist, not just where it looks nice."
        "A few pencils move across paper, and others...well..."
        "{i}I have to admit, it feels good when the answer comes out clean like that.{/i}"
        "{i}Not good enough to make me enjoy being called on, because I'm not broken, but good enough.{/i}"
        math_teacher "Now, for the vertical shift..."
        jump answer1done
    label wronganswer1:
        hide mood_pressure
        hide vignette
        with dissolve
        math_teacher "Not quite. Remember that the argument of a logarithm must be positive."
        math_teacher "So x minus one has to be greater than zero, which means x must be greater than 1."
        mc "Oh...right. Got it."
        "A few students murmur and write the correction down."
        jump answer1done
    label answer1done:
        pass
    show math_teacher at thide
    hide math_teacher
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The rest of class passes through the usual academic soup."
    nier "Equations, graph sketches, one student asking whether this will be on the exam, and the teacher answering with the kind of smile that says absolutely."
    nier "By lunch, my notebook has more arrows than actual words."
    nier "By the final bell, the arrows have somehow become my emotional state."
    call nier_clear from _call_nier_clear_0516_3
    scene bg club_day
    $ show_calendar()
    show mood_afternoon zorder 3 
    with wipeleft_scene
    "After school, I make my way to the club room."
    "For a second, I almost expect a full room: rows of desks, a handful of voices, and someone arguing with way too much confidence about whether a poem can be too purple."
    "Instead, I get the quiet version of reality."
    show monika 1a at t11
    "Monika is already there, flipping through a thin notebook with a pen tucked behind her ear."
    m "Hey, you made it!"
    mc "Against all odds."
    m "Rough day?"
    mc "Algebra noticed me looking alive and decided to correct that."
    m "Did you at least survive with your dignity?"
    mc "I gave an answer and received no applause, so dignity is still under review."
    m "Wow. This school really is falling apart..."
    "I take my usual seat and drop my bag beside the desk."
    "Monika closes her notebook halfway, keeping one finger between the pages."
    m "So, today's club agenda is pretty light."
    m "I was thinking we could read for a bit, then maybe workshop whatever you brought yesterday."
    mc "You mean the draft with all the brackets still in it?"
    m "That's the one~"
    m "The brackets are useful, actually. They show me where you stopped trusting the sentence."
    mc "You're making my bad habits sound organized."
    m "Only because they are. That's why I can find them."
    "{i}I can't even tell if that's encouragement or backhanded.{/i}"
    show monika at thide
    hide monika
    $ hide_calendar()
    scene black with wipeleft_scene
    # CRITIQUE: Again, the writing workshop is summarized at the exact point it could define Monika and MC's creative intimacy. Show the "especially fair" note so the hurt has substance.
    nier "Club time passes quietly."
    nier "Monika reads through my writing with the focused little frown she gets when she's trying not to rewrite an entire paragraph in her head."
    nier "I pretend not to notice."
    nier "She gives me a few notes, most of which are fair, and one of which hurts because it is especially fair."
    call nier_clear from _call_nier_clear_0516_4
    scene bg club_day
    $ show_calendar()
    show monika 1a at t11
    show mood_evening zorder 3 
    with wipeleft_scene
    "By the time the room starts to darken around the windows, Monika stacks her notebook on top of mine."
    m "There. Nothing too brutal, right?"
    mc "You stayed within club-approved damage."
    m "Good. I try to leave people functional."
    "I slip the papers back into my bag."
    mc "Anything I need to remember for tomorrow?"
    m "Tomorrow? Survive classes, first of all."
    mc "I'll...pencil that in."
    m "Saturday classes, at least. TGIS, am I right?"
    m "No club afterward, though. I'm not spending my free afternoon pretending to be responsible."
    mc "The movie, right, yep."
    m "The neat-looking horror movie, yes."
    m "I refuse to be stood up by someone who almost lost his own ID card yesterday."
    mc "That was one time."
    m "A very recent one time."
    mc "...I guess?!"
    m "Anyway, text me Sunday morning so we can pick a time."
    "I take a deep sigh."
    mc "...Will do."
    m "Good."
    m "Now go home before I find another responsibility to hand you."
    mc "Before the list grows, then. Later, Monika."
    show monika at thide
    hide monika
    play sound moddoorclose
    "She waves me off, and I leave the room before she can make good on that promise."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "My trip home starts the same way as always."
    nier "Down the corridor, out the gate, past the same storefronts, past the same utility poles, past the same vending machine that has been sold out of the same drink for a week."
    nier "Daily life repeats itself until some small change makes the pattern visible."
    call nier_clear from _call_nier_clear_0516_5
    scene bg residential_day
    $ show_calendar()
    show mood_overcast zorder 3 
    with wipeleft_scene
    "I slow down near the corner store when I notice someone standing by the curb with a neatly folded umbrella tucked under one arm."
    show kotonoha neut at t11
    "It's Kotonoha, who is technically in my year, though most people know her by sight before they know anything else."
    "She is always either coming from somewhere or going somewhere, and somehow that has become one of the school's accepted facts."
    mc "Oh. Hey, Kotonoha."
    ko "Good afternoon, [player]."
    "Her voice is polite, even, and completely unbothered by the late bus or the people walking around us."
    mc "Waiting for someone?"
    ko "A bus."
    mc "Right. That would make sense at a bus stop."
    "She gives a small nod, either accepting the obvious answer or giving it the courtesy of being complete."
    ko "It's running late."
    mc "Yeah, they do that."
    "A light breeze passes through the street."
    "Kotonoha adjusts the bag in her hand. The convenience store logo crinkles under her fingers."
    mc "Coming from work?"
    ko "One of them."
    "I nod, because that is how people generally answer Kotonoha. You simply keep the line moving."
    mc "Long day, then."
    ko "Average."
    "{i}For her, maybe.{/i}"
    "A car rolls by, kicking up a brief hiss of water from a shallow gutter puddle."
    "Kotonoha steps back without looking down."
    "She isn't startled or annoyed. She is simply already out of range before the splash reaches the curb."
    mc "Woah, good timing."
    ko "I watch where cars are."
    mc "Useful habit."
    ko "Most people watch where cars were."
    "I blink."
    mc "...Huh."
    "For a second, I don't have anything to add, even after all the filler I mustered up."
    "The bus finally groans around the corner in the distance."
    ko "Oh, that's mine."
    mc "Yeah. Guess I'll see you around."
    ko "You will."
    # CRITIQUE: "You will" has a nice eerie snap, but it risks sounding like forced mystique. Anchor Kotonoha's strangeness in behavior, as the car-splash dodge does, and use cryptic lines sparingly.
    "She gives a small bow, then steps toward the curb as the bus pulls in."
    show kotonoha at thide
    hide kotonoha
    "I stand there for an extra second after she leaves."
    "{i}You will.{/i}"
    "{i}She says it like a schedule, not a guess.{/i}"
    $ mark_character_met("kotonoha")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The rest of the walk home is quiet enough for my brain to start making nonsense out of normal things."
    nier "A late bus, a convenience store bag, a classmate who treats certainty like table manners. A Friday becomes something with texture."
    nier "Then I reach home, and the world goes back to being mostly shoes by the door and lights left on."
    call nier_clear from _call_nier_clear_0516_6
    scene bg doorday
    $ show_calendar()
    show mood_home zorder 3 
    with wipeleft_scene
    play sound moddooropen
    "When I step inside, there is already an unfamiliar pair of shoes lined up near the entrance."
    "They're men's shoes, clean and casual in a way that feels slightly too confident, assuming shoes can be confident."
    "{i}Please don't let this be one of mom's surprise errands in human form.{/i}"
    mc "I'm home."
    ah "Living room!"
    "That tone tells me she wants me to come in, and that she has prepared herself emotionally to be annoying about it."
    $ hide_calendar()
    scene bg living_room
    $ show_calendar()
    show asahina neut at t31
    show sam neut at t33
    show mood_home zorder 3 
    with wipeleft_scene
    # CRITIQUE: Sam's smoothness is the point, but the scene nearly turns him into a sitcom guest everyone riffs around. Let MC's unease linger longer before the handshake/profile jokes absorb it.
    "Asahina is standing near the couch with an expression that tries to be casual and fails by trying too hard."
    "Beside her is a guy I recognize mostly from context clues."
    "He's tall, relaxed, and has the kind of smile that looks like it has been tested in multiple social environments."
    "{i}So this is him, huh?{/i}"
    ah "This is Sam."
    "{i}Look at me, solving mysteries in my own living room.{/i}"
    sa "Hey. Masayami Inugami."
    sa "But Sam is easier for basically everyone, so please use that."
    mc "[player]."
    mc "...I'm the brother."
    sa "So I've heard."
    
    ah "Good things."
    
    mc "That was fast."
    sa "Mostly good things."
    "Asahina elbows him in the side, but he takes it like he saw it coming five seconds ago."
    
    ah "I said good things."
    
    sa "You said he was smart, sarcastic, and impossible in the morning."
    mc "That's more of a profile than I expected. I'd think she'd completely drag my name through the mud."
    "He offers his hand."
    "The handshake is firm without being dramatic about it."
    "I hate that I notice that."
    mc "So, uh...welcome."
    sa "Thanks."
    sa "Sorry for dropping in without much warning."
    
    ah "There was some warning, dummy~"
    
    mc "There was?"
    
    ah "I told mom."
    
    mc "Incredible. The brother has been cut from the mailing list."
    sa "If it helps, I didn't get the mailing list either."
    "His delivery is smooth enough that I almost miss how quickly he turns the awkwardness into a shared joke."
    "{i}He's good at this.{/i}"
    "{i}Not necessarily a bad thing, but definitely a thing.{/i}"
    show mom neut at t32
    mom "Ah, you're home!"
    mom "Sam, this is my son, [player]. [player], this is Sam."
    mc "We got through the tutorial already."
    mom "Good. Then I can skip the part where I remind everyone of the house rules."
    
    ah "Mom..."
    
    "Mom points at my sister."
    mom "Doors stay open."
    mom "Homework comes before movies."
    "She then pans her fingers around each of us."
    mom "And if anyone gets hungry, there are leftovers."
    sa "Understood, ma'am."
    # CRITIQUE: Sam clears every social test a little too cleanly here. One faintly wrong note--a pause that lasts too long, an over-specific answer, a glance toward Asahina before "ma'am"--would seed the later danger without spoiling him.
    "The \"ma'am\" lands perfectly: respectful without sounding like he's auditioning for a manners seminar."
    "Mom seems to approve, which is horrifying because it means he cleared the first boss fight."
    mom "Good answer."
    
    ah "See? Normal."
    
    mc "I never said he wasn't normal."
    
    ah "You thought it really loudly."
    
    mc "...There is so much wrong with you."
    sa "For what it's worth, I get it."
    sa "If I had a younger sister bringing a guy home, I'd probably do the same scan."
    mc "Scan?"
    sa "Shoes, posture, handshake, whether I say something stupid in the first thirty seconds."
    "I pause."
    "{i}Okay, now that's just unfair.{/i}"
    mc "You passed two and a half."
    sa "Out of?"
    mc "...Classified."
    sa "I'll take it."
    
    ah "Don't encourage him."
    
    "She says that while failing to hide a smile."
    show asahina at thide
    hide asahina
    show mom at thide
    hide mom
    show sam at thide
    hide sam
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The evening settles into something strangely normal."
    nier "Mom heats up leftovers. Asahina and Sam sit at the table with homework spread out between them, though only one of them appears to be treating homework as the primary activity."
    nier "Sam is easy to talk to in the way some people are easy to underestimate."
    nier "He laughs at the right times, listens at the right times, and never looks like he's searching for a place to put his hands."
    call nier_clear from _call_nier_clear_0516_7
    scene bg kitchen
    $ show_calendar()
    show mom neut at t22
    show sam neut at t21
    show mood_home zorder 3 
    with wipeleft_scene
    "Later, I find him in the kitchen rinsing a glass while mom packs away the last of the leftovers."
    mom "You don't have to do that, Sam."
    sa "It's fine. I used it, so I should clean it."
    mc "Careful. If you keep being useful, she'll invite you back."
    mom "He can come back."
    "Sam smiles at that, but not too much."
    sa "I'd like that."
    "Asahina, from the living room, makes a triumphant noise."
    ah "Ha!"
    mom "Homework!"
    ah "...Yes, ma'am..."
    "The victory dies instantly."
    "Sam dries his hands and glances toward the living room."
    sa "She's been working hard, you know."
    mc "At volleyball?"
    # CRITIQUE: "Trying to be a better person" is too vague for a line that is supposed to reveal Sam's insight. Give him one specific thing he noticed, or it reads like thematic placeholder dialogue.
    sa "That too, but she's, ah..."
    sa "...trying to be a better person? Is that the right words?"
    "He leaves it there."
    mc "Yeah. She does that."
    sa "I noticed."
    "Mom looks between us for a second, then goes back to the containers."
    "If she caught anything under the surface, she doesn't say it."
    $ mark_character_met("sam")
    show mom at thide
    hide mom
    show sam at thide
    hide sam
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Sam leaves sometime after dinner."
    nier "Asahina walks him to the door and takes about three times longer than necessary to come back inside."
    play sound moddoorclose
    nier "Nobody comments on it."
    nier "Technically, that's mercy."
    call nier_clear from _call_nier_clear_0516_8
    stop music fadeout 2.0
    pause 1.0
    scene bg bedroom
    $ show_calendar()
    show mood_night zorder 3 
    with wipeleft_scene
    play music fantasypassion
    "By night, I am back in my room with my phone in one hand and my planner open on my desk."
    "I don't usually use the planner unless things have reached the point where memory alone feels like a terrible idea."
    "This not-quite-weekend qualifies, mostly because Saturday still has school attached to it like a punishment with better branding."
    "{i}Saturday: survive classes, pick up the new game after school, and grab glue for Asa's poster. Chip restitution remains her problem, as legally established.{/i}"
    "{i}Maybe look at that university with mom too, assuming she brings it up and I don't conveniently evaporate first.{/i}"
    "{i}Sunday: text Monika in the morning, go to the horror movie, and try not to make the word \"date\" weird by thinking about it too much.{/i}"
    "I stare at the list for a while."
    "{i}Not exactly an impossible schedule.{/i}"
    "{i}Just enough to make my free time feel pre-owned.{/i}"
    "A muffled laugh rises from downstairs, probably Asahina texting Sam."
    "Mom says something after that, too faint for me to catch."
    "The house is alive in small, ordinary ways."
    "I set an alarm, plug in my phone, and lean back in my chair."
    "{i}School, club, home, errands, movie. Nothing major, really.{/i}"
    "{i}Just a normal Friday bleeding into a Saturday that still expects me to wear a uniform.{/i}"
    $ hide_calendar()
    scene black with dissolve_scene_full
    nier "The day ends without any grand conclusion."
    nier "Just a checklist, a tired brain, and the faint blue glow of a phone screen fading into sleep mode."
    nier "{i}Another day down.{/i}"
    nier "{i}And Saturday waiting its turn.{/i}"
    call nier_clear from _call_nier_clear_0516_9
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0516_1
    jump a0517
