label a0522:
    # --- Day 8: 2025-05-22 ---
    pause 2.0
    scene bg ether
    $ show_calendar()
    $ atmos("pressure")
    show noise zorder 4 at noise_alpha
    with dissolve_scene_full
    play music holdmusic
    # CRITIQUE (ADDRESSED): Reduced the gag density so the dream reads as subconscious pressure, not a sketch. Kept the strong images (waiting room, blank ticket, cup, open door, conveyor belt), cut the joke class names entirely, and pointed the classroom board at the day's omitted-agency lesson -- a passive sentence with no named actor, which is also a mirror of MC's own evasive narration.
    "The dream gives me a waiting room."
    "Plastic chairs face a number dispenser. A lopsided plant occupies the corner."
    "The music is polite. It is also, after ninety seconds, permanent."
    "{i}Please remain where you are while your regularly assigned programming is located.{/i}"
    "I look down at the ticket in my hand."
    "It says A-17, except the seven keeps trying to become a question mark."
    mc "...That seems rather concerning."
    # SFX SUGGESTION: An old PA speaker click with a faint electrical crackle.
    "A speaker clicks overhead."
    "\"Now serving: everyone who thought one more video would be fine.\""
    "The chairs turn toward me without moving."
    "The number dispenser coughs out another ticket, wet and unmistakable."
    "This one is blank."
    # CRITIQUE (ADDRESSED): Sentence-level nit: "I could barely reach out my hand before..." reads off in the current tense. "I barely have time to reach..." would match the scene's immediacy.
    "I barely have time to reach for it before the weird-looking plant takes it."
    mc "...Okay. Sure."
    # SFX SUGGESTION: A heavily muffled school bell with a submerged, warbling reverb.
    "Somewhere to my left, a classroom bell rings underwater."
    "Somewhere to my right, a microwave counts down in slow motion toward a number it never reaches."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg classroom_purg
    $ show_calendar()
    $ atmos("pressure")
    show noise zorder 4 at noise_alpha
    with wipeleft_scene
    "The waiting room becomes a classroom without bothering with a transition."
    "Desks float in neat rows over a floor that reflects too much light. Every clock on the wall points to a different form of late."
    "At the front of the room, the board is already full."
    "It's a single sentence, written over and over in a hand that might be mine."
    "{i}The room was left this way.{/i}"
    "{i}The room was left this way. The room was left this way.{/i}"
    mc "...Teacher, I think there's something wrong with--"
    "A floating piece of chalk underlines a formula by itself."
    "A cup waits on the teacher's desk. A door stands open beside it, almost expecting someone to enter."
    "The cup slides an inch closer to the door."
    "The speaker clicks again."
    "\"For today's lesson, please identify the actor responsible for your own sleep schedule.\""
    "{i}No thank you.{/i}"
    "My desk becomes a bus seat."
    "The bus seat becomes my bed."
    "My bed becomes a conveyor belt carrying notebooks, spaghetti, track shoes, one lonely cup, and a radio that keeps playing the same cheerful waiting music."
    "The dream tries to keep going, but everything else has better speakers."
    $ hide_calendar()
    scene black with dissolve_scene_full
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home")
    show noise zorder 4:
        alpha 0.10
        linear 2.0 alpha 0.0
    with dissolve_scene_full
    "The music does not stop when I wake up."
    "Then the ceiling and blanket settle back into place. The rectangle of light beside my pillow becomes my motormouthed android again."
    "{i}Autoplay. Of course.{/i}"
    "After Monika's call, my phone must have slipped from responsible background noise into a bottomless staircase of increasingly unrelated videos."
    "The current one involves a man in safety goggles explaining how to polish a toaster with common household objects."
    mc "...No."
    stop music fadeout 0.4
    # SFX SUGGESTION: Several frantic touchscreen taps ending in an abrupt audio cutoff.
    "I jab the screen until the music dies."
    hide noise
    "Silence falls so suddenly that it feels like the room took a breath."
    "Then I see the display: 7:47."
    mc "...SHIT."
    "I sit up too fast and regret the entire maneuver."
    # CRITIQUE (ADDRESSED): Gave the panic one non-funny beat so the consequence reads as real -- he never set the alarm because he let the autoplay keep going. The evidence is left on the page without MC diagnosing what it means about him.
    "My alarm is under the edge of my notebook, buried beneath last night's chemistry notes."
    "I never set it, though I remember meaning to. Then the phone offered one more video, and I let it."
    "Across the hall, Asahina's door is open."
    "Her room is empty in the loud, insulting way a room gets when someone has already left and did not even have the decency to bother you first."
    mc "...Asa?"
    "No answer."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    "The table confirms it all."
    "One chair is pushed back, and crumbs stripe the table. The abandoned bowl in the sink carries one suspiciously small smear of jam."
    "Mom's mug is gone too, which means the case from work has claimed her before breakfast could become a family activity."
    "A sticky note waits on the table."
    call enter_m_show_sticky_note(("Late court prep.", "Breakfast in fridge.", "Don't forget to ice if your foot complains."), signature="Mom") from _call_enter_m_show_sticky_note_0522_1
    "{i}Breakfast in fridge. If only I had the freaking TIME.{/i}"
    "I grab a convenience-store rice ball from the fridge and shove it into my bag. Halfway to the door I notice my socks do not match."
    mc "I got a feeling that it's gonna be a wonderful day~"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The next fifteen minutes turn into a private athletic event with worse shoes."
    nier "The walk to the station is mostly a jog, and my foot protests every landing."
    call nier_clear from _call_nier_clear_0522_1
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music schooldays
    "The school corridor is doing that pre-homeroom thing where everyone moves in straight lines until someone stops in the worst possible place."
    "I round the corner and spend my last scrap of dignity pretending this was a brisk walk."
    show monika forward uniform curi om oe nobl rdown ldown at t11
    m "[player]?"
    mc "Morning."
    "It comes out too breathless to qualify as casual."
    m forward uniform worr om oe awkw rhip ldown "Did you...run here?"
    mc "I like doing some extra cardio every now and then."
    m forward uniform wry cm oe nobl rdown ldown "That's a worrying phrase."
    mc "...Autoplay tried to kill me."
    m forward uniform curi om oe nobl rhip ldown "Autoplay?"
    mc "Long story involving a toaster. My alarm never went off."
    m forward uniform nerv om ce blaw rdown ldown "...That does sound like a long story, yeah."
    # SFX SUGGESTION: The homeroom bell interrupting the conversation mid-beat.
    "The homeroom bell rings and takes the sentence off our hands."
    m forward uniform happ cm oe nobl rdown ldown "You made it, at least."
    mc "By the most lenient form of the word..."
    "We split at the classroom door, and I slide into my seat with one second left."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Thursday proceeds as if it has no idea how close it came to losing me."
    nier "Teachers keep saying midterms like repetition will make the word develop mercy."
    call nier_clear from _call_nier_clear_0522_2
    stop music fadeout 1.0
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    with dissolve_scene_full
    play music quiz
    "By the last period, my notebook has become a battlefield of arrows and tiny notes to myself that already look disappointed in me."
    "{i}If I survive Monday, I am retiring from thought.{/i}"
    # CRITIQUE (ADDRESSED): Smoothed the clunky "partly due to me being."
    "The final bell goes, and half the class stands before it finishes. I move slower because my brain is still arguing with a note I wrote three hours ago."
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 1.0
    pause 2.0
    scene bg club_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music dailyfantasy
    "The club room is not quiet this afternoon."
    play sound moddooropen
    "I hear the argument before I get the door all the way open."
    show hikari neut at t31
    show homura neut at t33
    "One girl stands near the back locker with a paper held tight in one hand. Another is by the front row of desks, one arm folded across her stomach."
    "Her other hand stays curled against her sleeve."
    "Neither has left Monika much room to stand between them."
    hikari "That's NOT what I said!"
    homura "I'm not accusing you of saying it directly!"
    homura "I am saying the implication of the ending is somewhat...dismissive."
    hikari "There it is again! You keep saying somewhat like that makes it nicer!"
    homura "I was trying to be careful, okay?!"
    hikari "No, you were trying to make simple sound stupid without having to say simple is stupid."
    "{i}Ah.{/i}"
    "{i}This is not today's first waiting room.{/i}"
    show monika forward uniform worr om oe nobl rdown ldown at t32
    m forward uniform worr om oe nobl rhip ldown "Okay, let's slow down a little..."
    hikari "I AM slow! I'm literally explaining it!"
    homura "That's not what slow down means in this context!"
    hikari "Oh my GOD, see?!"
    "Monika takes one slow breath through her nose and catches my eye."
    mc "What did I miss?"
    m forward uniform nerv om ce awkw rdown ldown "Just a little feedback gone wrong..."
    mc "That sounds optimistic."
    hikari "Homura thinks my poem ends too easy."
    homura "I said the final image resolves the tension sooner than the rest of the poem seems to want."
    hikari "That is the same thing, motherfu--"
    mc "OKAY, okay!"
    play sound moddoorclose
    "I close the door behind me and keep my hand on the handle until the latch catches."
    "{i}No sudden movements around live disputes.{/i}"
    mc "Procedural pause."
    hikari "...Procedural what?"
    mc "Pause. Fancy word so it sounds like I know what I'm doing."
    m forward uniform happ om oe nobl rdown lpoint "I'll allow it."
    "Hikari crosses her arms. Homura keeps her eyes on the paper instead of either of us."
    menu:
        "(Start with what Homura meant.)":
            $ s1_pick("club_mediation", "homura")
            mc "Homura, forget how Hikari took it for a second. What were you actually trying to say?"
            homura "That the ending feels early."
            hikari "SEE--"
            mc "Hikari."
            "Hikari clamps her mouth shut, but the paper crackles in her grip."
            homura "Not easy. Early."
            homura "The final line is memorable. I like that it's direct."
            homura "I just thought the speaker still had something she wasn't saying when the poem stopped."
            hikari "Then why did you call it simple three times?"
            homura "Because it is simple."
            "Hikari's grip tightens. Homura's mouth stays open after the sentence ends."
            hikari "Right. There it is again."
            homura "I mean the line is direct. I don't think it's worse."
            hikari "You don't get to swap the word after I get mad."

        "(Start with what Hikari heard.)":
            $ s1_pick("club_mediation", "hikari")
            mc "Hikari, forget whether she's right for a second. What did you actually hear?"
            hikari "That my ending's lazy."
            homura "I never said--"
            mc "Hang on. I'm asking what she heard, not what you said."
            "Homura catches herself and goes quiet."
            hikari "She said it resolves the tension too early."
            hikari "And then she started talking about how simple it was, so yeah. I heard 'lazy.'"
            hikari "Like I took the easy way out because I couldn't write anything better."
            mc "Okay."
            "I look over at Homura."
            mc "Was that what you were trying to tell her?"
            homura "No. Not at all."
            hikari "Then what {i}were{/i} you trying to tell me?"
            homura "That I wanted one more line."
            hikari "...What?"
            homura "One more line before the ending. I thought the speaker still had something she wasn't saying."
            "Hikari's arms do not loosen. She looks down at the page instead."
            hikari "I spent all night deciding not to hide the ending behind another metaphor. You made that sound like I ran out of ideas."
            homura "I didn't know that."
            hikari "You didn't ask."
            "Homura presses her thumbnail into the cuff of her sleeve."
            homura "No. I didn't."

        "(The secret third option)":
            $ s1_pick("club_mediation", "both")
            "{i}Wait. Why am I picking one?{/i}"
            mc "Actually, no. Both of you."
            hikari "...Both of us what?"
            mc "Hikari, tell me what you think Homura meant. Homura, don't correct her yet."
            hikari "She thinks the ending's lazy."
            hikari "That I went simple because I couldn't come up with anything better."
            "Homura's mouth opens."
            mc "Not yet."
            "It closes."
            mc "Homura. Now tell me what you meant."
            homura "I thought the ending came too soon."
            homura "I liked the final line. I just thought the speaker still had something she wasn't saying."
            mc "Those are two very different sentences."
            hikari "Not if simple means worse."
            homura "It doesn't."
            hikari "Then why did you make it sound like you were apologizing for liking it?"
            "Homura closes her mouth and looks down at her sleeve."

    "Nobody looks relieved."
    mc "Okay. We found the crossed wire, not a solution."
    hikari "I'm not mad about one note. You kept saying simple like I should be embarrassed I wrote it."
    homura "I was trying to be precise."
    hikari "You were trying not to sound mean."
    homura "Because I knew it could sound mean!"
    "Homura's voice rises again, then breaks off. She curls her hand tighter around her sleeve."
    homura "I'm sorry. I made it sound as if being direct made the poem worse."
    homura "I don't believe that."
    "The paper loosens in Hikari's hand with a soft crackle."
    hikari "Okay. Thank you."
    hikari "I'm still mad about the note."
    homura "That's fair."
    mc "Good. Mad can sit at a desk, but shouting can't."
    m forward uniform worr om oe nobl rhip ldown "Then let's separate the critique from the revision."
    m forward uniform neut om oe nobl rhip lpoint "Hikari, draft one alternate line without replacing the current ending. Homura, write one sentence about what the ending already does well."
    m forward uniform wry om oe nobl rdown ldown "Add one honest question about what feels unfinished. Swap pages only when you're both ready."
    hikari "One line. Fine."
    homura "One note and one question."
    "Hikari pulls a chair out with her heel. Homura sets her paper down with more care than the desk requires."
    mc "Great. The fire code survives another afternoon."
    hikari "Don't get smug."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Club gets quieter after that, though not comfortable. Hikari revises with one shoulder turned away from Homura."
    nier "Homura leaves her first note folded beside the page instead of handing it over."
    call nier_clear from _call_nier_clear_0522_3
    pause 2.0
    scene bg club_day
    $ show_calendar()
    $ atmos("evening")
    show monika forward uniform dist cm oe nobl rdown ldown at t11
    with wipeleft_scene
    "By the time the window light turns orange, bags are packed and three empty soda bottles remain on the floor."
    "Everyone else leaves separately but without theatrical door usage, which counts as peace."
    m forward uniform happ om oe nobl rdown ldown "That was a pretty solid save earlier."
    mc "I mostly repeated what they said with less...emotional velocity."
    m forward uniform happ om oe nobl rhip ldown "There's a term for that, you know. It's called mediation."
    mc "...Uh, yeah. Though that kinda sounds like a premium word locked behind a paywall."
    m forward uniform happ cm ce nobl rdown ldown "The club has zero clams and several pens with bite marks on them. We'll manage."
    "She stacks the remaining papers into a tidy pile. Her smile is light, but the day has left a little tiredness at the corners."
    m forward uniform curi om oe nobl rdown ldown "You okay, by the way?"
    mc "From this morning? Yeah, it just established a stricter deadline."
    m forward uniform happ cm oe nobl rhip ldown "Good. Double-check your alarm tonight before bed."
    mc "I'll consider it."
    "I grab my bag."
    mc "Later, Monika."
    m forward uniform happ om ce nobl rdown ldown "Later!"
    "No nickname this time, surprisingly."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I leave school at a normal pace and decide the rest of the day can stay mercifully undescribed."
    nier "At home, Asahina hears the toaster version of my morning, takes my phone, and schedules three alarms without asking."
    nier "She names them {i}WAKE UP{/i}, {i}STILL WAKE UP{/i}, and {i}MOM WILL KNOW{/i}. I leave all three enabled."
    call nier_clear from _call_nier_clear_0522_4
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0522_1
    jump a0523
