label a0522:
    # --- Day 8: 2025-05-22 ---
    pause 2.0
    scene bg ether
    $ show_calendar()
    $ atmos("pressure")
    show noise zorder 4 at noise_alpha
    with dissolve_scene_full
    play music holdmusic
    "I'm in a waiting room where the plastic chairs all face a number dispenser and the only plant slouches against the wall."
    "The music is polite. It is also, after ninety seconds, permanent."
    "{i}Please remain where you are while your regularly assigned programming is located.{/i}"
    "The ticket in my hand says A-17, except the seven keeps trying to become a question mark."
    mc "...Pretty sure that's not how numbers work."
    # SFX SUGGESTION: An old PA speaker click with a faint electrical crackle.
    "A speaker clicks overhead."
    "\"Now serving: everyone who thought one more video would be fine.\""
    "The chairs turn toward me without moving."
    "The number dispenser coughs out a wet ticket with nothing printed on it. The plant takes it."
    mc "...Okay. Sure."
    # SFX SUGGESTION: A heavily muffled school bell with a submerged, warbling reverb.
    "While a classroom bell rings underwater to my left, a microwave on the other side counts toward a number it never reaches."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg classroom_purg
    $ show_calendar()
    $ atmos("pressure")
    show noise zorder 4 at noise_alpha
    with wipeleft_scene
    "I blink, and the number dispenser is gone. Desks float around my chair in neat rows, over a floor that reflects too much light."
    "Every clock on the wall points to a different form of late."
    "At the front, a single sentence fills the board, written over and over in a hand that might be mine."
    "{i}The room was left this way.{/i}"
    "{i}The room was left this way. The room was left this way.{/i}"
    mc "...Teacher, I think there's something wrong with--"
    "A floating piece of chalk underlines the last word."
    "A cup waits on the teacher's desk, beside a door that has been left open."
    "The cup slides an inch closer to the door."
    "The speaker clicks again."
    "\"For today's lesson, please identify the actor responsible for your own sleep schedule.\""
    "{i}Objection.{/i}"
    "My desk becomes a bus seat."
    "The bus seat becomes my bed."
    "My bed becomes a conveyor belt."
    "Notebooks. Spaghetti. Track shoes, one lonely cup, and a radio still playing the cheerful waiting music."
    "The radio gets louder as the conveyor carries it toward my head."
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
    "The ceiling settles back into place, then the blanket, and the waiting-room music plays on through all of it, piped out of the phone wedged beside my pillow."
    "{i}Autoplay. Of course.{/i}"
    "Last night I let the videos keep rolling after the light went out, strictly as background noise, and apparently nobody told them I fell asleep."
    "The current one involves a man in safety goggles explaining how to polish a toaster with common household objects."
    mc "...No."
    stop music fadeout 0.4
    # SFX SUGGESTION: Several frantic touchscreen taps ending in an abrupt audio cutoff.
    "I jab the screen until the music dies."
    hide noise
    "The silence that follows is so sudden that the room seems to be holding its breath."
    "Then I see the time: 7:47."
    mc "...SHIT."
    "I sit up too fast and regret the entire maneuver, head rush and drool spot included."
    "My alarm clock sits on the desk under last night's chemistry notes, set for absolutely nothing."
    "I remember meaning to set it. Then the phone offered one more video, and I let it."
    "Across the hall, Asahina's door hangs open with an empty uniform hanger still swinging from the handle. Nobody knocked."
    mc "...Asa?"
    "No answer."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    "Downstairs, one chair is pushed back from a stripe of toast crumbs, and there's a jam-smeared plate in the sink. Mom's travel mug is gone too, but she's left a sticky note on the table."
    call enter_m_show_sticky_note(("Late court prep.", "Breakfast in fridge.", "Don't forget to ice if your foot complains."), signature="Mom") from _call_enter_m_show_sticky_note_0522_1
    "{i}Breakfast in fridge. If only I had the freaking TIME.{/i}"
    "I shove a convenience-store rice ball into my bag instead and make for the door. Halfway there, I notice my socks don't match."
    mc "I got a feeling that it's gonna be a wonderful day~"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I jog toward the bus stop until my foot starts to pull, then downgrade to the fastest walk I can get away with. For once in its life, the bus is running late too."
    call nier_clear from _call_nier_clear_0522_1
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music school_day_a
    "The school corridor is doing that pre-homeroom thing where everyone moves in straight lines until some idiot stops in the worst possible place."
    "I round the last corner and spend my final scrap of dignity pretending this was a brisk walk."
    show monika forward uniform curi om oe nobl rdown ldown at t11
    m "[player]?"
    mc "Oh, hey. Morning."
    "It comes out about three breaths short of casual."
    m forward uniform worr om oe awkw rhip ldown "Wait, did you just {i}run{/i} here?"
    mc "Squeezing in some bonus cardio."
    m forward uniform wry cm oe nobl rdown ldown "On that foot? The one you were {i}supposed{/i} to ice last night?"
    mc "...Autoplay tried to kill me."
    m forward uniform curi om oe nobl rhip ldown "I'm sorry, autoplay did {i}what{/i}?"
    mc "Long story. There's a toaster involved. Also, my alarm never went off."
    m forward uniform nerv om ce blaw rdown ldown "Okay, I need the whole toaster saga later, but right now you're blocking the door."
    # SFX SUGGESTION: The homeroom bell interrupting the conversation mid-beat.
    "The homeroom bell goes off over our heads, and she steers me out of the doorway by the elbow so the line piling up behind me can get through."
    m forward uniform happ cm oe nobl rdown ldown "You made it, at least!"
    mc "Under the most lenient reading of the rules, sure."
    "She heads off down the hall toward her own homeroom, and I drop into my seat two names before attendance reaches mine."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Thursday proceeds as if it has no idea how close it came to losing me."
    nier "Teachers keep saying {i}midterms{/i}, like enough repetition might teach the word some mercy."
    call nier_clear from _call_nier_clear_0522_2
    stop music fadeout 1.0
    pause 2.0
    scene bg club_day
    $ show_calendar()
    $ atmos("afternoon")
    with dissolve_scene_full
    play music club_b
    "The club room is not quiet this afternoon."
    play sound moddooropen
    hikari "Simple isn't the same as STUPID!"
    show hikari angry at t31
    show homura frustrated at t33
    "Hikari has planted herself by the back lockers with a sheet of paper crushed in one fist. Homura faces her from the front row, one arm folded across her stomach while the other hand tugs her sleeve down over her knuckles."
    homura "I-I'm sorry, but I never said it was! I merely meant that the ending's implications were somewhat... dismissive."
    hikari "There it is again! You keep saying {i}somewhat{/i} like that makes it nicer!"
    "{i}I could still leave. Neither of them has seen me yet.{/i}"
    show monika forward uniform worr om oe nobl rdown ldown at t32
    m forward uniform worr om oe nobl rhip ldown "Hikari, let her finish. Homura, you don't have to qualify every single--"
    hikari "She's not FINISHING, she's just saying it LONGER!"
    "Monika spots me in the doorway, and her shoulders come down about an inch."
    mc "...What did I miss?"
    m forward uniform wry om oe nobl rhip ldown "Oh, not much! I've said \"let her finish\" fourteen times. I know it's fourteen because I've been counting, since it turns out you can't do council forms from the middle of a crossfire."
    m forward uniform happ om oe nobl rdown ldown "...Anyway! Welcome to club!"
    mc "Can I see the page?"
    show monika forward uniform worr cm oe nobl rdown ldown
    hikari "She thinks my poem ends too easy!"
    homura "I {i}said{/i} the final image resolves its tension sooner than the rest of the poem seems to want."
    hikari "That's the same damn thing with BIGGER WORDS!"
    play sound moddoorclose
    "I shut the door behind me and keep a hand on it until the latch catches."
    "{i}No sudden movements around live disputes.{/i}"
    mc "Okay. One at a time, because right now I physically can't hear either of you."
    menu:
        "(Start with what Homura meant.)":
            $ s1_pick("club_mediation", "homura")
            mc "Homura, you first. Short version, if you can."
            homura thinking "That the ending comes early. Not {i}easy{/i}. {i}Early{/i}."
            homura "The last line is memorable, and I genuinely admire how direct it is. I only felt that the speaker still had something she wasn't saying when the poem stopped, so I wanted... one more line."
            hikari unamused "Then why'd you call it simple three times?"
            homura frustrated "Because it {i}is{/i} simple! I-I mean direct! Simple as in {i}direct{/i}, not as in--"
            hikari "Nope. You don't get to swap the word after I get mad."

        "(Start with what Hikari heard.)":
            $ s1_pick("club_mediation", "hikari")
            mc "Hikari, you first. Which part are you actually mad about?"
            hikari sad "She said my ending comes too soon, then went on and on about how {i}simple{/i} it was. So yeah, I heard {i}lazy{/i}. Like I took the easy way out 'cause I couldn't write anything better."
            homura nervous "That isn't--I only wanted one more line! I thought the speaker still had something she wasn't saying..."
            hikari "I spent all night deciding {i}not{/i} to hide that ending behind another metaphor. You made it sound like I ran out of ideas."
            homura embarrassed "I... didn't know that."
            hikari unamused "You didn't ask."
            "Homura presses her thumbnail into the cuff of her sleeve."
            homura "...No. I didn't."

        "(The secret third option)":
            $ s1_pick("club_mediation", "both")
            "{i}Wait. Why am I picking one?{/i}"
            mc "Actually, know what? Both of you. Hikari, what did she say about your ending? Homura, no corrections until she's done."
            hikari sad "That it's lazy. Like I went simple 'cause I couldn't come up with anything better."
            homura thinking "And what I {i}meant{/i} was that I wanted one more line. I liked the ending, truly! I just thought the speaker still had something she wasn't saying."
            mc "Those are two very different sentences."
            hikari unamused "Not if simple means worse."
            homura frustrated "It doesn't!"
            hikari "Then why'd you sound like you were apologizing for liking it?"

    "Nobody looks relieved."
    "{i}I can referee a line of poetry. Whatever else this is, they can keep.{/i}"
    mc "...Can we at least sit down? People are starting to stare through the door."
    "Neither of them reaches for a chair."
    hikari determined "...I'm still not replacing the ending."
    m forward uniform happ om oe nobl rhip ldown "Nobody's confiscating it, Hikari!"
    m forward uniform neut om oe nobl rhip lpoint "If you want to try another line, write it under the draft, not over it. And Homura, when you write your note, start with the part you liked."
    m forward uniform neut om oe nobl rdown ldown "Then add one honest question about whatever feels unfinished, and you two swap pages when you're {i}both{/i} ready. Not before, okay?"
    hikari "One line. Fine."
    homura nervous "One note. And... one question."
    "Hikari drags a chair out with her heel. Homura lowers herself into hers and sets the page down with more care than any desk could possibly need."
    mc "Great. The fire code survives another afternoon."
    hikari unamused "Don't get smug."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Club gets quieter after that. Not comfortable, just quieter."
    nier "Hikari spends the rest of the hour revising with one shoulder turned away from Homura."
    nier "Homura's first note sits folded beside her page until the bell. She never passes it across."
    call nier_clear from _call_nier_clear_0522_3
    pause 2.0
    scene bg club_day
    $ show_calendar()
    $ atmos("evening")
    show monika forward uniform dist cm oe nobl rdown ldown at t11
    with wipeleft_scene
    "By the time the window light goes orange, the others have filed out one at a time. Nobody slams the door, and around here that's practically a peace treaty."
    "Three empty soda bottles stay behind on the floor by the back desks."
    m forward uniform happ om oe nobl rdown ldown "Thanks for staying. I really thought Hikari was going to tear that page in half."
    mc "I kept hoping somebody would hand me the poem. I still haven't read it."
    m forward uniform neut om oe nobl rhip ldown "Neither have I. I think Homura's the only one who's actually read it."
    mc "Well, nobody threw anything. I'm calling that a pass."
    "She knocks the leftover papers into a neat stack. One gets away from her anyway, and she has to crouch to fish it out from under a desk."
    m forward uniform curi om oe nobl rdown ldown "You okay, by the way?"
    mc "Yeah. I'm gonna eat something that isn't a rice ball and set an actual alarm."
    m forward uniform happ cm oe nobl rhip ldown "Good! I'll run these bottles down to recycling, and then I am {i}out{/i} of here."
    mc "Give 'em here. Recycling's on my way out."
    "I collect the bottles while she checks under the other desks for anything else the afternoon left behind."
    m forward uniform happ om ce nobl rdown ldown "Okay, that's everything! Let's go before somebody comes back for a pen."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "We stop at the vending machine on the way out because I want something cold, and Monika buys the grape soda she keeps telling me is disgusting."
    nier "She pulls a face at the first sip and then keeps going. By the time we split at the station, the can is empty, and she tries to blame the burp on me."
    nier "At home, Asahina hears about the toaster and confiscates my phone to set three alarms."
    nier "She names them {i}WAKE UP{/i}, {i}STILL WAKE UP{/i}, and {i}MOM WILL KNOW{/i}. I leave all three enabled."
    call nier_clear from _call_nier_clear_0522_4
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0522_1
    jump a0523
