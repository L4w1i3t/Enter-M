label a0522:
    # --- Day 8: 2025-05-22 ---
    scene bg ether
    $ show_calendar()
    show mood_pressure zorder 3
    show noise zorder 4 at noise_alpha
    show vignette zorder 5 at ambient_vignette(0.34)
    with dissolve_scene_full
    play music holdmusic
    window auto
    # CRITIQUE (ADDRESSED): Reduced the gag density so the dream reads as subconscious pressure, not a sketch. Kept the strong images (waiting room, blank ticket, cup, open door, conveyor belt), cut the joke class names entirely, and pointed the classroom board at the day's omitted-agency lesson -- a passive sentence with no named actor, which is also a mirror of MC's own evasive narration.
    "The first thing the dream gives me is a waiting room."
    "Before me is a row of plastic chairs, a number dispenser, and a plant that looks awfully lopsided."
    "The music is soft enough to be polite and repetitive enough to be an earworm."
    "{i}Scheduled programming.{/i}"
    "{i}Please remain where you are while your regularly assigned programming is located.{/i}"
    "I look down at the ticket in my hand."
    "It says A-17, except the seven keeps trying to become a question mark."
    mc "...That seems rather concerning."
    "A speaker clicks overhead."
    "\"Now serving: everyone who thought one more video would be fine.\""
    "The chairs turn toward me without moving."
    "{i}That should be impossible. The dream does not seem concerned about it.{/i}"
    "The number dispenser coughs out another ticket."
    "This one is blank."
    # CRITIQUE (ADDRESSED): Sentence-level nit: "I could barely reach out my hand before..." reads off in the current tense. "I barely have time to reach..." would match the scene's immediacy.
    "I barely have time to reach before the weird-looking plant takes it."
    mc "...Okay. Sure."
    "Somewhere to my left, a classroom bell rings underwater."
    "Somewhere to my right, a microwave counts down toward a number it never reaches."
    $ hide_calendar()
    scene black with wipeleft_scene
    scene bg classroom_purg
    $ show_calendar()
    show mood_pressure zorder 3 
    show noise zorder 4 at noise_alpha
    show vignette zorder 5 at ambient_vignette(0.36)
    with wipeleft_scene
    "The waiting room becomes that classroom without committing to the bit."
    "Desks float in neat rows over a floor that reflects too much light. Every clock on the wall points to a different form of late."
    "At the front of the room, the board is already full."
    "It's a single sentence, written over and over in a hand that might be mine."
    "{i}The room was left this way.{/i}"
    "{i}The room was left this way. The room was left this way.{/i}"
    "Nowhere on the board is anyone named. The verb just sits there, politely holding the door for whoever did it."
    mc "...Teacher, I think there's something wrong with--"
    "A floating piece of chalk underlines a formula by itself."
    "A cup waits on the teacher's desk."
    "A door stands open beside it, almost expecting someone to enter."
    "Neither of them admits anything."
    "The cup slides an inch closer to the door, which refuses to look at me."
    "I don't say anything. In here, naming the actor feels like volunteering."
    "The speaker clicks again."
    "\"For today's lesson, please identify the actor responsible for your own sleep schedule.\""
    "{i}No thank you.{/i}"
    "My desk becomes a bus seat."
    "The bus seat becomes my bed."
    "My bed becomes a conveyor belt carrying notebooks, spaghetti, track shoes, one lonely cup, and a phone that keeps playing the same cheerful waiting music."
    "The dream tries to keep going, but the phone has better speakers."
    $ hide_calendar()
    scene black with dissolve_scene_full
    scene bg bedroom
    $ show_calendar()
    show mood_home zorder 3 
    show noise zorder 4:
        alpha 0.10
        linear 2.0 alpha 0.0
    with dissolve_scene_full
    "The music does not stop when I wake up."
    "For several seconds, my room continues to behave like an underfunded outpatient clinic."
    "Then my ceiling becomes my ceiling, my blanket becomes my blanket, and the rectangle of light beside my pillow becomes my motormouthed phone."
    "A video plays on the screen."
    "The title has too many capital letters, two numbers, and the phrase {i}you won't believe what happens next{/i} doing emotional blackmail at the end."
    "{i}Autoplay.{/i}"
    "{i}Of course.{/i}"
    "Apparently, at some point after Monika's call, my phone slipped from responsible background noise into a bottomless staircase of increasingly unrelated videos."
    "The current one involves a man in safety goggles explaining how to polish a toaster with common household objects."
    "The next thumbnail appears to be a documentary about abandoned escalators."
    mc "...No."
    stop music fadeout 0.4
    "I jab the screen until the music dies."
    hide noise
    "Silence falls so suddenly that it feels like the room took a breath."
    "Then I see the time."
    "7:47."
    mc "...SHIT."
    "I sit up too fast, which gives my spine the chance to briefly file its own complaint."
    # CRITIQUE (ADDRESSED): Gave the panic one non-funny beat so the consequence reads as real -- he never set the alarm because he let the autoplay keep going, and he's "not surprised," which is the quiet part. A small ledger note that his slipping is starting to feel normal to him, before the comedy resumes.
    "My alarm is sitting under the edge of my notebook, smothered by last night's chemistry notes and a mechanical pencil."
    "I never set it. I meant to. I remember meaning to, right up until the phone offered me one more video and I let it."
    "It's a small thing. It is. But I notice I'm not surprised, and that's the part I don't love."
    "Across the hall, Asahina's door is open."
    "Her room is empty in the loud, insulting way a room gets when someone has already left and did not even have the decency to bother you first."
    mc "...Asa?"
    "No answer."
    "{i}Cool. Fantastic. My sister truly has abandoned me in a moment of need.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    scene bg kitchen
    $ show_calendar()
    show mood_home zorder 3 
    with wipeleft_scene
    "The kitchen confirms it all."
    "One bowl in the sink, one chair pushed back, one suspiciously tiny smear of jam on the counter."
    "Mom's mug is gone too, which means the case from work has claimed her before breakfast could become a family activity."
    "A sticky note waits on the table."
    "{i}Late court prep. Breakfast in fridge. Don't forget to ice if your foot complains. - Mom{/i}"
    "{i}Breakfast in fridge.{/i}"
    "{i}If only I had the FREAKING TIME TO.{/i}"
    "I grab a convenience-store rice ball from the fridge, shove it into my bag, and discover that I have mismatching socks on."
    mc "Today's gonna be a wonderful day."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The next fifteen minutes become a private athletic event with worse shoes."
    nier "I brush my teeth with the commitment of a man fixing things the morning of a dentist appointment, throw on the rest of my uniform, check my bag twice for the big three, and leave the house while still trying to convince myself that I'm still dreaming."
    nier "The walk to the station is mostly a jog, which oddly becomes a negotiation with yesterday's track practice."
    nier "Somehow, the bus is more punctual than most other days."
    nier "...If only I could say the same about the stoplights that were all red."
    call nier_clear from _call_nier_clear_0522_1
    scene bg corridor
    $ show_calendar()
    show mood_afternoon zorder 3 
    with wipeleft_scene
    play music schooldays
    "The school corridor is doing that pre-homeroom thing where everyone moves in straight lines until someone stops in the worst possible place."
    "The warning bell has already rung while the real bell is loading its chamber."
    "I round the corner with exactly enough dignity left to pretend this was a brisk walk."
    show monika 1d at t11
    m "[player]?"
    mc "Morning."
    "It comes out too breathless to qualify as casual."
    m "Did you...run here?"
    mc "I like doing some extra cardio every now and then."
    m "That's a worrying phrase."
    mc "...Autoplay tried to kill me."
    m "Autoplay?"
    mc "Long story. Involves a toaster, a chair...I think, and my alarm just not going off at all."
    m "...That does sound like a long story, yeah."
    "The final bell rings before either of us can decide whether the sentence deserves help."
    m "You made it, at least."
    mc "By the most lenient form of the word..."
    "We split at the classroom door, and I slide into my seat with one second left."
    show monika at thide
    hide monika
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Thursday proceeds as if it has no idea how close it came to losing me."
    nier "Homeroom passes, history reviews imperial reforms, math turns a worksheet into a personality test--the works, really."
    nier "Teachers keep saying midterms like repetition will make the word develop mercy."
    nier "There was even one of my classmates who tried to \"cancel\" midterms by betting the teacher if he could make a half-room shot into the trash can."
    call nier_clear from _call_nier_clear_0522_2
    scene bg class_day
    $ show_calendar()
    show mood_afternoon zorder 3 
    stop music fadeout 1.0
    with dissolve_scene_full
    play music quiz
    "By the last period, my notebook has become a battlefield of arrows, boxed terms, and tiny notes to myself that already look disappointed in me."
    "The room smells like chalk dust and the collective restraint of people not asking the obvious question of whether the review guide will be on the test."
    "{i}If I survive Monday, I am retiring from thought.{/i}"
    "{i}...Oh, who am I kidding? These exams are just trash mobs.{/i}"
    "The final bell arrives with all the grace of a door opening in a fire drill."
    # CRITIQUE (ADDRESSED): Smoothed the clunky "partly due to me being."
    "Half the class stands before the sound finishes. I move slower, partly because I'm an airhead lost in thought about some random nonsense."
    $ hide_calendar()
    scene black with wipeleft_scene
    scene bg club_day
    $ show_calendar()
    show mood_afternoon zorder 3 
    stop music fadeout 1.0
    with wipeleft_scene
    play music dailyfantasy
    "The club room is not quiet today."
    play sound moddooropen
    # CRITIQUE (ADDRESSED): Per the author response below, kept Hikari and Homura as minor background texture rather than plot-relevant setup -- but seeded them in the May 20 club scene (Hikari scribbling and crossing out, Homura annotating in tiny handwriting) so the argument here reads as a known tension surfacing, not strangers imported with a theme.
    # Critique response: They can be named, but their role here is minor/background club texture rather than plot-relevant side-character setup.
    "I hear the argument before I get the door all the way open."
    show hikari neut at t21
    show homura neut at t22
    "One girl stands near the closet with a paper held tight in one hand."
    "Another is by the front row of desks, one arm folded across her stomach and the other hand curled against her sleeve."
    "Monika is between them in spirit, if not yet in actual proximity."
    hikari "That's NOT what I said!"
    homura "I'm not accusing you of saying it directly!"
    homura "I am saying the implication of the ending is somewhat...dismissive."
    hikari "There it is again! You keep saying somewhat like that makes it nicer!"
    homura "I was trying to be careful, okay?!"
    hikari "No, you were trying to make simple sound stupid without having to say simple is stupid."
    "{i}Ah.{/i}"
    "{i}This is not today's first waiting room.{/i}"
    "The shape of the argument is old enough that the room seems to remember it before I do."
    "It's short lines versus long ones, directness versus atmosphere -- one person hearing condescension, the other hearing carelessness."
    "{i}A tale as old as time.{/i}"
    show monika 1d at t32
    m "Okay, let's slow down a little..."
    # CRITIQUE (ADDRESSED): Kept the "cup did it" callback from derailing the resolution -- MC now thinks it instead of saying it, and Monika silently shares the joke, which is more intimate than the spoken version and lets Homura's olive-branch land clean. See below.
    hikari "I AM slow! I'm literally explaining it!"
    homura "That's not what slow down means in this context!"
    hikari "Oh my GOD, see?!"
    "Monika's expression enters emergency management mode."
    "She catches my eye with the expression of a confused yet curious individual."
    mc "What did I miss?"
    m "Just a little feedback gone wrong..."
    mc "That sounds optimistic."
    hikari "Homura thinks my poem ends too easy."
    homura "I said the final image resolves the tension sooner than the rest of the poem seems to want."
    hikari "That is the same thing, motherfu--"
    mc "OKAY, Okay!"
    play sound moddoorclose
    "I close the door behind me very carefully and, dare I say it, very gently." # this is a nod to vanilla DDLC. KEEP THIS AT ALL COSTS
    "{i}No sudden movements around live disputes.{/i}"
    mc "Procedural pause."
    hikari "...Procedural what?"
    mc "Pause. Fancy word so it sounds like I know what I'm doing."
    m "I'll allow it."
    "Hikari crosses her arms."
    "Homura looks at the paper instead of either of us."
    mc "Homura, are you saying the poem is bad because the ending is direct?"
    homura "No."
    homura "I don't think directness is inherently weak. The final line is memorable."
    hikari "...It is?"
    homura "Yes."
    homura "It has impact because it refuses ornamentation."
    mc "Great. Hikari, are you saying Homura is not allowed to want the tension carried a little longer?"
    hikari "No."
    hikari "I'm saying she could say that without acting like the freaking prose police."
    homura "I didn't mean to imply that, I swear."
    m "There we go, we're getting somewhere."
    m "New club rule: nobody gets to translate someone else's feedback into the least charitable version and then argue with that."
    m "Basically, always be civil! Kinda makes you wonder why that wasn't there in the first place."
    "The corner of Hikari's mouth twitches like it is fighting for neutrality. Homura exhales, quiet but visible."
    homura "I should have phrased it better."
    homura "The ending made me feel as if the piece wanted to stop before the speaker was finished being honest."
    hikari "..."
    hikari "Okay, that's...actually useful."
    homura "And I did like the image with the paper cup."
    "{i}The cup did it.{/i}"
    "I keep that one to myself. Some inside jokes are load-bearing, and this isn't the moment to test whether it holds."
    "Across the room, Monika presses her lips together, which means she thought the exact same thing and is being more professional about it."
    hikari "Fine."
    hikari "Maybe I can hold the ending for one more line."
    hikari "Not, like, smother it in metaphors or whatever."
    homura "I wasn't asking you to smother it."
    hikari "I know, I'm just saying."
    "The argument deflates enough that the room stops bracing for impact."
    m "How about this?"
    m "Hikari tries one alternate ending. Homura writes one note about what the current ending does well."
    m "Then nobody touches the closet shelves, the desk arrangement, or each other's dignity for the rest of the afternoon."
    hikari "...Fine."
    homura "That sounds fair."
    mc "And here I was ready to sell tickets."
    # CRITIQUE (ADDRESSED): Swapped the graphic "skin you alive" for a smaller, sharper, in-context jab (it's a writing club) that keeps Hikari's bite without breaking the just-de-escalated room.
    hikari "...I will workshop you into the ground."
    m "No monetizing workshop conflict, [player]."
    mc "This club keeps refusing perfectly normal revenue streams, and for what?"
    homura "I would prefer not to be monetized."
    show hikari at thide
    hide hikari
    show homura at thide
    hide homura
    show monika at thide
    hide monika
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Club settles down after that."
    nier "Near adjournment, Monika gives me a small thumbs-up from across the room like I have completed a minor diplomatic mission."
    nier "All I really do is shrug and smile in the way that says \"I was trained by being forged in fire.\""
    call nier_clear from _call_nier_clear_0522_3
    scene bg club_day
    $ show_calendar()
    show mood_evening zorder 3 
    show monika 1a at t11
    with wipeleft_scene
    "By the time the sun begins its descent, bags are packed and there are three too many empty bottles of soda on the floor."
    "Everyone else leaves separately but without theatrical door usage, which counts as peace."
    m "That was a pretty solid save earlier."
    mc "I mostly repeated what they said with less emotional velocity."
    m "There's a term for that, you know. It's called mediation."
    mc "...Uh, yeah. Though that kinda sounds like a premium word locked behind a paywall."
    m "Maybe you should start a discount on using it."
    mc "The club can't afford me."
    m "The club has zero clams and several pens with bite marks on them, so I'm sure we can."
    "She stacks the remaining papers into a tidy pile."
    "Her smile is light, but the day has left a little tiredness at the corners."
    m "You okay, by the way?"
    mc "From this morning? Yeah. I was just given a more...strict time limit."
    m "Good. Double check your alarm tonight before bed."
    # CRITIQUE (ADDRESSED): Thinned the nickname parade. Instead of closing on another cute label, Monika visibly loads one and lets it go, landing a plain, warm beat instead -- intimacy that isn't a label. (Her nicknames still exist elsewhere; they just don't have to carry every tender moment.)
    mc "No promises."
    "I sling my bag over one shoulder."
    mc "Later, Monika."
    m "Later."
    "No nickname this time. She just looks at me for a second, the way she does when she's deciding whether to say the real thing."
    m "...I'm glad you made it here in one piece today. Even the breathless version."
    "She waves me out with the same smile she gives to me specifically."
    show monika at thide
    hide monika
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Nothing much happens after that."
    nier "I leave school at a normal pace, ignore my phone's attempt to recommend another video, and decide the rest of Thursday can stay mercifully undescribed."
    nier "For once, that sounds like the healthiest available option."
    call nier_clear from _call_nier_clear_0522_4
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0522_1
    jump a0523
