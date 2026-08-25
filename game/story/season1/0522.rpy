label a0522:
    # --- Day 8: 2025-05-22 ---
    pause 2.0
    scene bg ether
    $ show_calendar()
    $ atmos("pressure")
    show noise zorder 4 at noise_alpha
    with dissolve_scene_full
    play music holdmusic
    window auto
    # CRITIQUE (ADDRESSED): Reduced the gag density so the dream reads as subconscious pressure, not a sketch. Kept the strong images (waiting room, blank ticket, cup, open door, conveyor belt), cut the joke class names entirely, and pointed the classroom board at the day's omitted-agency lesson -- a passive sentence with no named actor, which is also a mirror of MC's own evasive narration.
    "The dream gives me a waiting room."
    "Before me is a row of plastic chairs, a number dispenser, and a plant that looks awfully lopsided."
    "The music is polite. It is also, after ninety seconds, permanent."
    "{i}Please remain where you are while your regularly assigned programming is located.{/i}"
    "I look down at the ticket in my hand."
    "It says A-17, except the seven keeps trying to become a question mark."
    mc "...That seems rather concerning."
    # SFX SUGGESTION: An old PA speaker click with a faint electrical crackle.
    "A speaker clicks overhead."
    "\"Now serving: everyone who thought one more video would be fine.\""
    "The chairs turn toward me without moving."
    "The number dispenser coughs out--LITERALLY coughs out--another ticket."
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
    "The waiting room becomes that classroom without committing to the bit."
    "Desks float in neat rows over a floor that reflects too much light. Every clock on the wall points to a different form of late."
    "At the front of the room, the board is already full."
    "It's a single sentence, written over and over in a hand that might be mine."
    "{i}The room was left this way.{/i}"
    "{i}The room was left this way. The room was left this way.{/i}"
    mc "...Teacher, I think there's something wrong with--"
    "A floating piece of chalk underlines a formula by itself."
    "A cup waits on the teacher's desk."
    "A door stands open beside it, almost expecting someone to enter."
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
    "Then my ceiling turns back into my ceiling, my blanket into my blanket, and the rectangle of light beside my pillow into my motormouthed android."
    "{i}Autoplay.{/i}"
    "{i}Of course.{/i}"
    "Apparently, at some point after Monika's call, my phone slipped from responsible background noise into a bottomless staircase of increasingly unrelated videos."
    "The current one involves a man in safety goggles explaining how to polish a toaster with common household objects."
    mc "...No."
    stop music fadeout 0.4
    # SFX SUGGESTION: Several frantic touchscreen taps ending in an abrupt audio cutoff.
    "I jab the screen until the music dies."
    hide noise
    "Silence falls so suddenly that it feels like the room took a breath."
    "Then I see the time."
    "7:47."
    mc "...SHIT."
    "I sit up too fast and regret the entire maneuver."
    # CRITIQUE (ADDRESSED): Gave the panic one non-funny beat so the consequence reads as real -- he never set the alarm because he let the autoplay keep going. The evidence is left on the page without MC diagnosing what it means about him.
    "My alarm is sitting under the edge of my notebook, smothered by last night's chemistry notes and a mechanical pencil."
    "I never set it. I meant to. I remember meaning to, right up until the phone offered me one more video and I let it."
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
    "One chair pushed back, crumbs left on the table, one bowl abandoned in the sink through the doorway, one suspiciously tiny smear of jam."
    "Mom's mug is gone too, which means the case from work has claimed her before breakfast could become a family activity."
    "A sticky note waits on the table."
    call enter_m_show_sticky_note(("Late court prep.", "Breakfast in fridge.", "Don't forget to ice if your foot complains."), signature="Mom") from _call_enter_m_show_sticky_note_0522_1
    "{i}Breakfast in fridge.{/i}"
    "{i}If only I had the FREAKING TIME TO.{/i}"
    "I grab a convenience-store rice ball from the fridge and shove it into my bag. Halfway to the door I notice my socks do not match."
    mc "I got a feeling that it's gonna be a wonderful day~"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The next fifteen minutes turn into a private athletic event with worse shoes."
    nier "The walk to the station is mostly a jog, which my foot spends the whole way objecting to in writing."
    call nier_clear from _call_nier_clear_0522_1
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music schooldays
    "The school corridor is doing that pre-homeroom thing where everyone moves in straight lines until someone stops in the worst possible place."
    "I round the corner with exactly enough dignity left to pretend this was a brisk walk."
    show monika forward uniform curi om oe nobl rdown ldown at t11
    m "[player]?"
    mc "Morning."
    "It comes out too breathless to qualify as casual."
    m forward uniform worr om oe awkw rhip ldown "Did you...run here?"
    mc "I like doing some extra cardio every now and then."
    m forward uniform wry cm oe nobl rdown ldown "That's a worrying phrase."
    mc "...Autoplay tried to kill me."
    m forward uniform curi om oe nobl rhip ldown "Autoplay?"
    mc "Long story. Involves a toaster, a chair...I think, and my alarm just not going off at all."
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
    "The final bell goes and half the class stands before the sound finishes. I move slower, partly because I'm an airhead lost in thoughts all alone about some random nonsense."
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
    "One girl stands near the back locker with a paper held tight in one hand."
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
    show monika forward uniform worr om oe nobl rdown ldown at t32
    m forward uniform worr om oe nobl rhip ldown "Okay, let's slow down a little..."
    hikari "I AM slow! I'm literally explaining it!"
    homura "That's not what slow down means in this context!"
    hikari "Oh my GOD, see?!"
    "Monika's expression enters emergency management mode."
    "She catches my eye."
    mc "What did I miss?"
    m forward uniform nerv om ce awkw rdown ldown "Just a little feedback gone wrong..."
    mc "That sounds optimistic."
    hikari "Homura thinks my poem ends too easy."
    homura "I said the final image resolves the tension sooner than the rest of the poem seems to want."
    hikari "That is the same thing, motherfu--"
    mc "OKAY, Okay!"
    play sound moddoorclose
    "I close the door behind me with practiced patience."
    "{i}No sudden movements around live disputes.{/i}"
    mc "Procedural pause."
    hikari "...Procedural what?"
    mc "Pause. Fancy word so it sounds like I know what I'm doing."
    m forward uniform happ om oe nobl rdown lpoint "I'll allow it."
    "Hikari crosses her arms."
    "Homura keeps her eyes on the paper instead of either of us."
    menu:
        "(Start with what Homura meant.)":
            $ s1_pick("club_mediation", "homura")
            mc "Homura, forget how Hikari took it for a second. What were you actually trying to say?"
            homura "That the ending feels early."
            hikari "SEE--"
            mc "Hikari."
            hikari "..."
            homura "Not easy. Early."
            homura "The final line is memorable. I actually like that it's direct."
            hikari "...You do?"
            homura "Yes."
            homura "I just thought the speaker still had something she wasn't saying."
            homura "So when the poem ended there, it felt like she stopped herself."
            mc "So you'd keep the same kind of ending."
            homura "Probably."
            mc "Just later."
            homura "Exactly."
            "Hikari stares at her for a second."
            hikari "Okay, that is NOT how you made it sound."
            homura "I...can see that now."
            hikari "You made it sound like 'simple' was something I needed to fix."

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
            hikari "Then what WERE you trying to tell me?"
            homura "That I wanted one more line."
            hikari "...What?"
            homura "One more line before the ending."
            homura "I thought the speaker still had something she wasn't saying."
            "Hikari's arms loosen by about half an inch."
            hikari "Then why didn't you just SAY that?"
            homura "I thought I did."
            hikari "You absolutely did not."
        "(The secret third option)":
            $ s1_pick("club_mediation", "both")
            "{i}Wait.{/i}"
            "{i}Why am I picking one?{/i}"
            mc "Actually, no. Both of you."
            hikari "...Both of us what?"
            mc "Hikari, tell me what you think Homura meant."
            mc "Homura, don't correct her yet."
            hikari "She thinks the ending's lazy."
            hikari "That I went simple because I couldn't come up with anything better."
            "Homura's mouth opens."
            mc "Not yet."
            "It closes."
            mc "Homura. Now tell me what you meant."
            homura "I thought the ending came too soon."
            homura "I liked the final line. I just thought the speaker still had something she wasn't saying."
            "Hikari takes that in."
            hikari "..."
            homura "..."
            mc "Those are two very different sentences."
            hikari "...Yeah."
            homura "Apparently."
            mc "Great. We've discovered language."

    m forward uniform happ om ce nobl rhip ldown "There we go, we're getting somewhere!"
    m forward uniform wry om oe nobl rhip lpoint "New club rule: nobody gets to translate someone else's feedback into the least charitable version and then argue with that."
    "The corner of Hikari's mouth twitches like it is fighting for neutrality. Homura exhales, quiet but visible."
    homura "I should have phrased it better..."
    homura "The ending really made me feel as if the piece wanted to stop before the speaker was finished being honest."
    hikari "..."
    hikari "Okay, that's...actually useful."
    homura "And I did like the image with the paper cup."
    "{i}The cup did it.{/i}"
    hikari "Fine."
    hikari "Maybe I can hold the ending for one more line."
    hikari "Not, like, smother it in metaphors or whatever."
    homura "I wasn't asking you to smother it."
    hikari "I know, I'm just saying."
    "The argument deflates, and the room stops bracing for impact."
    m forward uniform happ om oe nobl rhip lpoint "How about this?"
    m forward uniform neut cm oe nobl rhip lpoint "Hikari tries one alternate ending. Homura writes one note about what the current ending does well."
    m forward uniform wry om oe nobl rdown ldown "Then nobody touches each other's dignity for the rest of the afternoon."
    hikari "...Fine."
    homura "That sounds fair."
    mc "And here I was ready to sell tickets."
    hikari "...I will turn your skin into shoes."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Club calms down after that."
    call nier_clear from _call_nier_clear_0522_3
    pause 2.0
    scene bg club_day
    $ show_calendar()
    $ atmos("evening")
    show monika forward uniform dist cm oe nobl rdown ldown at t11
    with wipeleft_scene
    "By sun's descent, bags are packed and there are three too many empty bottles of soda on the floor."
    "Everyone else leaves separately but without theatrical door usage, which counts as peace."
    m forward uniform happ om oe nobl rdown ldown "That was a pretty solid save earlier."
    mc "I mostly repeated what they said with less...emotional velocity."
    m forward uniform happ om oe nobl rhip ldown "There's a term for that, you know. It's called mediation."
    mc "...Uh, yeah. Though that kinda sounds like a premium word locked behind a paywall."
    m forward uniform happ cm ce nobl rdown ldown "The club has zero clams and several pens with bite marks on them. We'll manage."
    "She stacks the remaining papers into a tidy pile."
    "Her smile is light, but the day has left a little tiredness at the corners."
    m forward uniform curi om oe nobl rdown ldown "You okay, by the way?"
    mc "From this morning? Yeah. I was just given a more...strict time limit."
    m forward uniform happ cm oe nobl rhip ldown "Good. Double check your alarm tonight before bed."
    mc "No promises."
    "I grab my bag."
    mc "Later, Monika."
    m forward uniform happ om ce nobl rdown ldown "Later!"
    "No nickname this time, surprisingly."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I leave school at a normal pace and decide the rest of the day can stay mercifully undescribed."
    call nier_clear from _call_nier_clear_0522_4
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0522_1
    jump a0523
