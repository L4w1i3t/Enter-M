label a0519:
    # --- Day 5: 2025-05-19 ---
    scene bg class_day
    $ show_calendar()
    show mood_afternoon zorder 3 
    with dissolve_scene_full
    play music dailyfantasy
    window auto
    "Monday enters the room wearing fluorescent lights and a lecture schedule."
    "Civics is already underway by the time my brain accepts that the weekend is over."
    "The teacher has written {i}PUBLIC VIRTUE{/i} on the board, then underlined it hard enough to threaten the chalk."
    show civics_teacher neut at t11
    # CRITIQUE: The definition is clear, but it reads like a textbook paragraph with a few jokes inserted. Since performance versus substance is a major Matsuda theme, give MC a sharper personal reaction.
    # CRITIQUE: Because "virtue signaling" is a loaded real-world phrase, decide whether you want that cultural baggage. "Performative virtue" or "public moral performance" would keep the theme without sounding like discourse shorthand.
    civics_teacher "Virtue signaling is a phrase people use often, but not always carefully."
    civics_teacher "At its simplest, it refers to the public display of moral values for social approval rather than meaningful action."
    civics_teacher "The tricky part is that public moral expression is not automatically dishonest."
    "A few pens move. A few faces communicate the same desperate hope that this will not become an essay prompt."
    civics_teacher "If someone donates to a relief fund and tells others to encourage more donations, that public statement may serve a practical purpose."
    civics_teacher "If someone posts a slogan, receives praise, and treats the praise as the accomplishment, the action becomes more performative."
    "{i}So basically: caring more about looking morally superior. Fantastic. Another human behavior with paperwork.{/i}"
    "I write the phrase down anyway despite knowing it front to back."
    civics_teacher "Now, quick check."
    "The chalk stops."
    "I make the catastrophic mistake of looking at the board right when the teacher turns around."
    civics_teacher "[player]."
    mc "...Yeah?"
    civics_teacher "Which example here is the clearest case of virtue signaling?"
    show mood_pressure zorder 4
    show vignette zorder 5 at ambient_vignette(0.28)
    with dissolve
    "{i}And there it is. The academic sniper rifle known as eye contact.{/i}"
    menu:
        "Donating quietly to a local shelter.":
            jump civics_wronganswer1
        "Making a post to spread awareness and doing nothing else.":
            jump civics_rightanswer1
        "Organizing volunteers after talking about the issue.":
            jump civics_wronganswer1
    label civics_rightanswer1:
        hide mood_pressure
        hide vignette
        with dissolve
        civics_teacher "Correct."
        civics_teacher "The issue is not that the person spoke publicly. The issue is that the public display replaced the substance."
        "The teacher circles {i}display{/i} and {i}substance{/i} on the board."
        "{i}Nice. I survived the morality pop quiz.{/i}"
        "{i}Not exactly a heroic achievement, but I'll take what I can get on a Monday.{/i}"
        jump civics_answer1done
    label civics_wronganswer1:
        hide mood_pressure
        hide vignette
        with dissolve
        civics_teacher "Not quite."
        civics_teacher "Quiet donation is action without display. Organizing volunteers is public, but it still produces practical results."
        civics_teacher "The post example is the clearest one because the display replaces the action."
        mc "Right...yeah. That makes sense."
        "Somewhere behind me, a pencil taps twice against a desk and mercifully stops."
        jump civics_answer1done
    label civics_answer1done:
        pass
    show civics_teacher at thide
    hide civics_teacher
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The rest of civics continues in the same shape."
    nier "We talk about public responsibility, social pressure, and the thin line between caring about something and caring about being seen caring about something."
    nier "By the time the bell rings, my notebook contains half a page of useful notes and one tiny drawing of a random character from a rhythm game I like."
    call nier_clear from _call_nier_clear_0519_1
    stop music fadeout 1.0
    pause 1.0
    scene bg corridor
    $ show_calendar()
    show mood_afternoon zorder 3 
    with wipeleft_scene
    play music dailyleisure
    "After school, the hallway becomes its usual disaster of bodies, bags, half-finished conversations, and people stopping in the exact worst places."
    "I keep to the side, one hand on my bag strap and the other hovering near my phone."
    "No club announcement. No errand list. No emergency glue acquisition."
    "{i}For once, I might actually escape cleanly.{/i}"
    show matsuda neut at t11
    ma "Lo! If it is not the wanderer of weekend roads, returned from his nocturnal collision with destiny!"
    "The sentence hits me before Matsuda fully enters my line of sight."
    "{i}Never mind. Destiny has a hallway ambush mechanic.{/i}"
    mc "...Hey, Matsuda."
    ma "Hail, [player]! Survivor of shoulder-borne calamity! Keeper of unopened games! Witness to my radiant entrance upon the stage of your otherwise modest life!"
    mc "That's a lot before hello."
    ma "Hello is a small door. I prefer windows, balconies, and occasionally a drawbridge."
    "She falls into step beside me like we planned this, which we absolutely did not."
    "A couple students glance over. Matsuda does not lower her voice, because lowering her voice would imply the world has earned privacy."
    ma "Tell me, good sir, did the fabled game disappoint as requested? Or did it seize your evening and drag you through lands of digital peril?"
    mc "It was fine."
    ma "Fine? A word so pale it should be studied by physicians."
    mc "...Okay, it was fun."
    ma "Ah! Color returns to the patient after all. And here I was wallowing in the realm of the monochrome."
    mc "Are you always like this after school?"
    ma "After school? Before school. During school. At select municipal events. I contain multitudes, my good--"
    # CRITIQUE: This is one of the strongest scenes so far because MC actually sets a boundary and Matsuda changes. This balance of theatrical mask and exposed person is the model to keep using.
    mc "Okay, stop."
    "The word comes out flatter than I meant it to."
    "Matsuda freezes mid-gesture, one hand still lifted like she was about to address a balcony that does not exist."
    mc "Sorry, just...can you not do the bard thing for five seconds?"
    mc "I'm not mad, it's just a lot."
    ma "...Not a fan of the bard, huh?"
    "For the first time since she appeared, her voice lands at a normal volume."
    ma "Fine. He's gone."
    "She lowers her hand and rolls her shoulders like she is taking off an invisible cape."
    ma "Better?"
    mc "...Yeah. Thanks."
    "The hallway keeps moving around us."
    "Without the performance filling the space, Matsuda looks slightly smaller. Not embarrassed exactly. More like someone waiting to see whether the floor is stable."
    ma "For the record, I was asking about the game because I'm still debating buying it."
    ma "And because you seemed like the kind of guy who would undersell a thing he enjoyed to avoid sounding excited."
    mc "That is a weirdly specific accusation."
    ma "Am I wrong?"
    mc "...No."
    ma "Then I accept your apology."
    mc "I did not apologize."
    ma "Spiritually, you did."
    "There she is again, but quieter. Manageable, at the very least."
    mc "It's good. The combat feels better than the demo, and the story's doing that thing where it pretends to be simple before showing a knife."
    ma "Ah, most excellent! My wallet shall suffer."
    mc "Condolences."
    ma "Accepted."
    ma "Also, if I buy it and hate it, I will blame you exclusively."
    mc "That feels a bit unfair..."
    ma "Fate rarely is, chum."
    "She says it with a restrained little flourish, then catches herself and clears her throat."
    ma "Sorry. Force of habit."
    mc "That one was fine."
    "Her smile returns, smaller than Saturday's but less exhausting."
    ma "Good to know."
    ma "Then I shall take my leave towards my destination, lest it shutter its doors before my arrival!"
    mc "...The store's just a few streets away."
    ma "My point still stands."
    "I snort despite myself."
    ma "Until next time, [player]!"
    mc "Later."
    show matsuda at thide
    hide matsuda
    "She slips into the crowd, less like a spotlight this time and more like someone who knows where all the exits are."
    "My phone is still in my hand, which I realize I never checked."
    "{i}Well. That was...slightly less fatal than expected.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    # CRITIQUE: The summary after this charged interaction is too abrupt. What felt refreshing: the quieter Matsuda, the successful boundary, or the fact that he was allowed to leave?
    nier "The trip home is refreshing."
    nier "{i}I wish all Mondays could be like this.{/i}"
    call nier_clear from _call_nier_clear_0519_2
    scene bg kitchen
    $ show_calendar()
    show mood_home zorder 3 
    with wipeleft_scene
    "Dinner is simple tonight: grilled fish, rice, miso soup, and whatever vegetables mom decided needed to stop taking up space in the fridge."
    "The table feels calmer than it did yesterday, which is to say nobody is interrogating me about a movie date before I even sit down."
    show asahina neut at t21
    show mom neut at t22
    mom "How was school?"
    mc "School-shaped."
    
    ah "That means boring."
    
    mc "'Least it's accurate."
    mom "Any homework?"
    mc "Some civics notes, a reading thing, and about twenty math problems that are due tomorrow."

    ah "Skill issue."
    mc "Says the person who turned arts and crafts into a weekend boss fight."
    
    ah "I won, didn't I?"
    
    mom "You did! The poster looked very nice."
    "Asahina focuses very hard on her rice."

    ah "It was whatever."
    mc "You're too modest for your own good, Asa."
    
    ah "Shut up."
    
    "Mom smiles like she has decided not to make the obvious comment."
    mom "And you, [player]? Anything interesting happen?"
    "Matsuda's hallway entrance flashes through my head with all the subtlety it lacked in person."
    mc "Not really."

    ah "Liar, liar, plants for hire."
    mc "...Excuse me?"
    
    ah "That's your 'not really' voice."
    ah "Very different from your real not-really voice."
    
    mom "You do have versions, to be fair."
    
    ah "Unfortunately."
    
    mc "I talked with a friend. That's it. Seriously."
    
    ah "With?"
    
    mc "Matsuda."
    "Asahina's chopsticks pause in midair."

    ah "Ohhhh, sidewalk traffic strikes again."
    mc "I am actually going to strangle you one of these days..."
    # CRITIQUE: The family pile-on is funny in isolation, but everyone turns into a comedy panel. MC's privacy should feel a little more violated here if this is feeding later isolation.
    mom "Sidewalk traffic?"
    mc "No."

    ah "He crashed into a girl Saturday and got her number."
    mc "Contact info. The difference matters."
    # CRITIQUE: "Maybe you'd be more popular..." is sharper than the scene's playful family teasing. If MC's defensiveness is meant to wound Asahina, let him register that; otherwise it makes him look casually mean.
    mc "And you have such a big mouth, Asa! Maybe you'd be more popular if you talked eighty percent less!"
    mom "...{i}Does{/i} it matter?"
    mc "You two... I am being ganked in my own home."
    
    ah "Technically mom owns it."
    
    "I stare at my soup as if it might defend me, much to my dismay."
    mom "Well, as long as everyone is being respectful and nobody is actually getting hurt, I think hallway conversations are allowed."
    mc "...Thank you for the official ruling."
    ah "Boring ruling. There's gotta be some drama or dirt."
    mom "I can make it more embarrassing if you'd prefer."
    
    ah "...I retract my statement."
    
    "Dinner settles after that."
    "Mom talks about a coworker who keeps labeling food in the shared fridge but never actually brings anything worth stealing."
    "Asahina complains about volleyball practice in the specific tone of someone who likes it too much to quit."
    "I eat, listen, and let Monday become small again."
    show asahina at thide
    hide asahina
    show mom at thide
    hide mom
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The rest of the evening asks very little of me."
    nier "Homework gets done. The game gets opened for a more responsible amount of time than yesterday, which is still probably less responsible than I will claim later."
    nier "No one texts anything urgent."
    nier "Bedtime encroaches in a much more respectful manner."
    call nier_clear from _call_nier_clear_0519_3
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0519_1
    jump a0520
