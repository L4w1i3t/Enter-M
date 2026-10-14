label a0521:
    # --- Day 7: 2025-05-21 ---
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with dissolve_scene_full
    play music quiz
    "Sleep took its time last night. I walk into language arts running at about seventy percent."
    "Naturally, this is the day the class is asked whether a comma can be morally implicated."
    "The teacher has filled half the board before the bell stops."
    show japanese_teacher neut at t11
    japanese_teacher "For the midterm, assume definitions are the bare minimum for what I ask."
    japanese_teacher "If you write that focalization is merely who sees the scene, or that ellipsis is something that was just left out, you have described the tool without explaining the work it performs."
    "The girl in front of me puts down her highlighter and takes out a second sheet of paper."
    japanese_teacher "...Yes, that means a lot of written responses."
    "A few more people do the same."
    "{i}I should probably leave more room under these headings...{/i}"
    japanese_teacher "A strong answer should move from syntax, to narrative effect, to thematic consequence."
    japanese_teacher "A correct label gets you started. The evidence is where the marks are."
    "{i}Cool. I love literature combos.{/i}"
    "The teacher taps the third phrase, the chalk giving a dry click."
    japanese_teacher "This kind of prose allows subjects to disappear without the sentence collapsing."
    japanese_teacher "That flexibility can be graceful, but in fiction it can also become evasive."
    # NUDGE KEEP: this line is the key to how the chapter's prose works.
    japanese_teacher "When a passage repeatedly refuses to identify who acts, the omission does not only create ambiguity. It can redistribute guilt."
    japanese_teacher "Now, consider the passage on the handout."
    # SFX SUGGESTION: A brief wave of paper rustling across the classroom.
    "A formal passive construction describes the room as having been left behind, but the person who left it that way never gets named."
    "{i}Cheerful.{/i}"
    japanese_teacher "Notice the pattern."
    japanese_teacher "The passage gives us evidence of action while withholding a stable actor."
    japanese_teacher "It also keeps the emotional vocabulary restrained, almost procedural."
    japanese_teacher "So the question is not whether the author forgot to name the subject."
    "I make the strategic error of looking at the handout like a person who knows how to read."
    japanese_teacher "[player]."
    mc "...Yes?"
    japanese_teacher "How does the repeated subject omission alter the reader's ability to assign agency, and how does that support the passage's treatment of guilt?"
    $ atmos_pressure()
    with dissolve
    menu:
        "It makes the reader participate in assigning culpability.":
            jump japanese_rightanswer1
        "It proves the narrator did not witness the event directly.":
            jump japanese_wronganswer1
        "It shifts the passage into objective documentary style.":
            jump japanese_wronganswer1
    label japanese_rightanswer1:
        $ atmos_pressure_clear()
        with dissolve
        mc "It makes the reader participate in assigning culpability."
        mc "We know what happened to the room, but we have to supply whoever did it."
        mc "That leaves us deciding whether the narrator doesn't know, or just doesn't want to say."
        japanese_teacher "Great answer!"
        "She circles the gap she left for the missing subject and draws an arrow to the sentence about guilt."
        japanese_teacher "{i}That{/i} is the kind of answer I expect on Monday."
        jump japanese_answer1done
    label japanese_wronganswer1:
        $ atmos_pressure_clear()
        with dissolve
        japanese_teacher "Not quite."
        japanese_teacher "The restrained diction may resemble objectivity, but the effect is not neutral."
        japanese_teacher "The omission controls where blame can settle."
        "She circles the gap she left for the missing subject and draws an arrow to the sentence about guilt."
        japanese_teacher "For the midterm, do not stop at tone. Explain what the syntax makes the reader {i}do{/i}."
        mc "Right. Got it."
        jump japanese_answer1done
    label japanese_answer1done:
        pass
    japanese_teacher "Everyone should annotate the passage with this in mind."
    japanese_teacher "Mark the verbs first, then identify where the sentence withholds the actor."
    "The room closes around the scratch of pens and shuffling paper."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "By the end of class, I need an arrow just to find the second half of my answer."
    call nier_clear from _call_nier_clear_0521_1
    stop music fadeout 1.0
    pause 2.0
    scene bg rooftop
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music school_day_a
    "The rooftop is one of those places students call secret because teachers don't bother correcting the myth unless someone starts throwing things."
    "The wind keeps lifting the plastic around my lunch, and I trap it under the lid before anything worse can occur."
    "{i}Definitely looks thrown together.{/i}"
    "I get two bites in before the rooftop door opens."
    show asahina uniform happy at l11
    ah "There you are!"
    mc "Uh oh, that sounded like a threat."
    ah "You weren't in the hallway. I nearly gave up and ate on the stairs."
    mc "...You looked for me for, what, twenty seconds?"
    ah "Twenty seconds? Try taking the stairs with actual children going both ways."
    play sound moddoorclose
    "My sister steps fully onto the roof and lets the door close behind her with a metallic click."
    scene bg rooftop
    $ show_calendar()
    $ atmos("afternoon")
    show asahina uniform neut at t11
    with dissolve
    "Her lunch bag hangs from one hand. The other is already busy with her phone, since that evidently has priority over balance."
    ah "I texted you before last period and didn't get a response."
    mc "Sorry. Phone's been on silent since class."
    ah "Well, check it occasionally. I could've been dying, y'know."
    "She sits beside me and claims the usual sibling share of my personal space."
    "She opens her lunch bag beside mine and reaches over for the napkin I'm sitting on."
    show asahina uniform happy
    ah "So here's some news: poster went up this morning."
    mc "Oh?"
    ah "And it's still on the wall! Cheap-ass tape. Better than I thought."
    mc "...How much tape did you use?"
    ah "A whole roll, no biggie. Also, a couple people said it looked good."
    show asahina uniform embarrassed
    "She says it into her food like the rice needs to hear it more than I do."
    mc "Seems like people have good--"
    show asahina uniform annoyed
    ah "Don't make it weird."
    mc "...I say {i}one{/i} nice thing, and you get defensive."
    show asahina uniform smug
    ah "Because you do that voice! Like you're about to bite my head off!"
    "I put a piece of carrot in my mouth and consider launching it at her."
    mc "Track starts back up today, by the way."
    show asahina uniform unamused
    ah "Yeah, Mom said."
    ah "Try not to die out there. I'm not arranging a funeral 'cause I have my own practice."
    mc "That was nearly concern. Should I document it?"
    show asahina uniform teasing
    ah "You'd make me carry your bag again. It weighs a freaking ton."
    mc "...I'm touched by my strategic value."
    show asahina uniform worried
    "She sets her chopsticks down across the lid of her food."
    ah "Your foot {i}is{/i} actually fine, right? Because Mom asks me first and I'm not lying for you."
    mc "Mostly fine. Coach is keeping it light today, so I'll try to remember that when everyone passes me."
    ah "...Good."
    mc "You can keep the blackmail for later."
    show asahina uniform embarrassed
    ah "Oh, I have plenty already."
    mc "Good to know."
    play sound moddooropen
    "I move my bag so it's out of her way, when the rooftop door opens again."
    show asahina uniform curious at t21
    show tsubaki uniform neut at l22
    "A girl steps out with a small lunch bag clasped in both hands."
    show tsubaki uniform happy
    "For a beat, she looks relieved."
    show tsubaki uniform shocked
    "Then she sees us and stops with one hand still on the door."
    show tsubaki uniform nervous
    ts "Ah--sorry! I thought this side was empty."
    mc "...Tsubaki?"
    show tsubaki uniform curious
    ts "...Oh!"
    ts "[player], right?"
    ah "Wait, you two know each other?"
    mc "We met Saturday."
    show asahina uniform happy
    ah "OOHH! Sidewalk traffic! That's her, right?!"
    mc "That was Matsuda. This girl, Tsubaki, was with her."
    show tsubaki uniform embarrassed
    ts "I'm still sorry about that. Really."
    mc "You weren't even the one I ran into, why are {i}you{/i} apologizing?"
    show tsubaki uniform nervous
    ts "I was supposed to be watching where we were going. She'd started doing her stupid thing again."
    "Her bag crackles as she shifts her grip."
    show asahina uniform pose_hairflip
    ah "I'm Asahina, by the way. I'm this idiot's superior sister."
    show tsubaki uniform curious
    ts "Asahina..."
    ts "That was your name on the bottom right corner of the volleyball poster, right?"
    show asahina uniform curious
    ah "Oh. Yeah."
    mc "Okay, surely you can't be the only person in this school named Asahina, right?"
    ah unamused "Bitch, I can guarantee that I am, now shut up."
    mc "Wow, alright. Harsh."
    ah nervous "And please don't tell me it already fell down..."
    show tsubaki uniform determined
    ts "No! It looked really good."
    show tsubaki uniform happy
    ts "I liked how the motion lines led into the lettering. I could read the larger words from the stairs."
    show tsubaki uniform thinking
    ts "And you really didn't have to go that in detail with the watermark."
    show asahina uniform embarrassed
    ah "...Thanks."
    ah "Yeah. Took longer than the ball, which was stupid."
    mc "That means she's about to frame your review."
    show asahina uniform annoyed
    ah "I am NOT!"
    show tsubaki uniform neut
    ts "Oh, I do that {i}all{/i} the time. Spend an hour fixing something nobody's going to look at, much less remember."
    show tsubaki uniform happy
    ts "You could make it bigger next time. It's a good signature."
    "Asahina looks down at the initials inked on her own lunch bag."
    show asahina uniform neut
    ah "...Yeah, well."
    ah "It got the job done."
    show tsubaki uniform nervous
    "Tsubaki shifts one foot back toward the door."
    mc "You can sit if you want."
    ts "Are you sure? I can go round the other side."
    show asahina uniform happy
    ah "Sit down. You're making me nervous standing there."
    show tsubaki uniform embarrassed
    ts "Right, uh... Sorry."
    "She sits a careful distance away and keeps her own bag on the door side of her knees."
    "Asahina keeps talking between bites, and Tsubaki waits until she's busy with her drink before starting a sentence."
    show tsubaki uniform worried
    ts "Is, um... your shoulder better?"
    mc "Yeah. It was barely anything, I swear."
    show asahina uniform smug
    ah "He complained about it three times. In one day. One in writing."
    mc "Do NOT make up stories about me!"
    show tsubaki uniform neut
    ts "Matsuda spent almost seven minutes worrying by the vending machine after you left."
    mc "...Almost seven?"
    show tsubaki uniform smug
    ts "I was waiting for my drink. She kept asking if you looked annoyed."
    show asahina uniform curious
    mc "Is she always like that? I could hear her halfway down the alley even after the exchange."
    ts thinking "She's... how do I put it?"
    # Matsuda is a third-year and Tsubaki a second-year, so the public anecdote
    # stays in a mixed-year committee. Tsubaki keeps the private ending for a
    # later lunch, after the group has earned more of her confidence.
    ts neut "Okay, so... We were on the supply committee together in April. I was the only second-year."
    ts "At the first meeting, nobody wanted to do inventory."
    ts teasing "Matsuda stood up and gave an acceptance speech. Nobody had offered her the job."
    ts "She thanked us for our confidence before anybody could interrupt."
    ah shocked "Dear God..."
    ts "Oh, believe me, there's more."
    ah "No..."
    ts happy "She brought notes. I still don't know when she wrote them."
    "Tsubaki looks down and smooths the same crease in her lunch bag twice."
    mc "So it's true that she's a third-year?"
    ts neut "Mhm. Same year as... remind me, are you a third-year?"
    mc "Yep. Basically one foot in the grave."
    ts thinking "Ah."
    ts neut "She transferred in at the start of the year."
    mc "Huh. Don't think it ever came up."
    ah unamused "You've shared a building since April and you found her with your shoulder."
    mc "...So she volunteered herself into a job and it worked."
    ts teasing "The teacher gave her the clipboard halfway through and she kept going on and on and on."
    ah happy "Okay, that's actually incredible. Somebody should carve that into the supply closet door."
    ts curious "We did get the inventory done. She just wanted us to call the mop cupboard the armory for... some odd reason."
    "Tsubaki folds the top of her lunch bag closed."
    ts shocked "Oh crap, what time is it? I need to get going before things get crowded again!"
    mc "Already? It's not even halfway."
    ts neut "I borrowed someone's book and she desperately needs it back before fifth."
    ts teasing "And I should tell Matsuda where I went, before she starts a search party."
    ah unamused "Does... she seriously come looking every lunch?"
    ts sad "Sometimes. Usually we eat together."
    ts neut "She'll have been waiting downstairs because I, ah... forgot to let her know."
    "She stands and smooths the fold out of her skirt."
    ts happy "It was nice meeting you, Asahina."
    ts "And seeing you again, [player]."
    ah "Yeah. You too."
    mc "Later, Tsubaki."
    ts "Talk later!"
    show tsubaki at thide
    hide tsubaki
    play sound moddooropen
    "She slips through the door with less noise than the door itself makes."
    play sound moddoorclose
    show asahina uniform determined at t11
    ah "I like her. She actually looked at the poster."
    mc "I looked at it too."
    ah "You said the glue smelled weird. Doesn't count."
    mc "Yeah, yeah..."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Chemistry works through reaction yields while algebra assigns more problems. Foreign language reminds us that vocabulary is also on the midterm."
    call nier_clear from _call_nier_clear_0521_2
    stop music fadeout 1.0
    pause 2.0
    scene bg track_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music day_c
    "Heat lifts off the red lanes while a few teammates jog the curve in an easy, even rhythm. A month ago, I'd have been halfway through the warmup before any of them showed up."
    "{i}A whole month of walking past this place. I'm sick of watching.{/i}"
    show track_coach neut at t11
    track_coach "[player]!"
    "Coach's voice carries across the infield and catches me crouched over a shoelace that's already tied."
    track_coach "You're cleared for light practice, correct?"
    mc "That's the official verdict."
    track_coach "Then we follow it."
    track_coach "Warmup lap and mobility, then strides at seventy percent. No heroics."
    mc "I left my cape at home."
    track_coach "Good. It would slow you down."
    track_coach "Keep joking and I'll get the resistance parachute out. When you're cleared for it."
    "He says all of it without a flicker of a smile. For Coach, that's practically giddy."
    "I take the outside of the warmup line, where nobody's going to clip me while I test the first few steps."
    "{i}No pain. A little tightness, and way more paranoia than either one deserves.{/i}"
    "By the first curve the caution starts to loosen, and by the back straight I've quit staring at my shoes."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Drills come next: high knees and walking lunges across the grass, like somebody scattered invisible furniture for us to step over."
    nier "I rush the last lunge and make myself redo it, mostly so Coach doesn't get the satisfaction of telling me to."
    call nier_clear from _call_nier_clear_0521_3
    pause 2.0
    scene bg track_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    "The first stride starts at the curve, and seventy percent sounds gentle right up until my body remembers that percentages are a scam coaches invented to sell more practice."
    "For the first few seconds I'm braced for the foot to flare. By halfway my lungs are the louder complaint, and by the time I clock how fast I'm going, I've stopped waiting for the pain altogether."
    "I'd happily take another straightaway at this pace. Instead I coast down early and walk it off on the grass, hands on my hips, while a faint pull through the arch fades a little more with every step."
    track_coach "Again."
    mc "Was that a good again, or a bad--"
    track_coach "Again without commentary, [player]."
    mc "...Got it."
    "A couple of the guys nearby snicker while Coach points me back to the curve."
    track_coach "Seventy percent."
    mc "That {i}was{/i} seventy!"
    track_coach "That was closer to eighty."
    mc "Okay, fine. I was trying to catch him."
    "Coach tips his head at the runner cooling down past the finish line."
    track_coach "Let him go. You've got your own session."
    "On the second stride I keep my eyes on the bend and let everybody else's race stay their problem."
    "The third goes worse, because confidence is an idiot and decides to add speed."
    track_coach "Easy now..."
    "Two words, and they yank me back from something impressively stupid. I ease off and let the last few meters roll out under me."
    "{i}Right. Light practice, not a comeback montage.{/i}"
    "{i}... Yet.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The rest is cooldown and stretching while the main group starts the intervals I'd normally be suffering through with them."
    call nier_clear from _call_nier_clear_0521_4
    pause 2.0
    scene bg track_evening
    $ show_calendar()
    $ atmos("evening")
    with wipeleft_scene
    "By the time practice breaks up, the afternoon has gone soft around the edges. I drop onto the grass by my bag and pick at a stubborn shoelace while the sweat cools on the back of my neck."
    "{i}Used, but nowhere near destroyed. I'll take it.{/i}"
    show track_coach neut at t11
    track_coach "How's the foot?"
    mc "Still attached."
    track_coach "You know what I mean, [player]."
    mc "A little tight. Not painful, just annoying."
    track_coach "Good. Ice it tonight if it starts talking."
    track_coach "One more thing. The district invitational is the second weekend of June, and entries go in the first week."
    track_coach "So once exams are done, you and I are having a conversation about what you're running."
    mc "Sixteen hundred and thirty-two hundred. Conversation over."
    track_coach "That isn't a conversation. That's a wish list."
    mc "It's a very reasonable wish list."
    track_coach "We'll see what the foot has to say about it."
    track_coach "If it changes its mind before Friday, you tell me before practice. Not after."
    mc "Got it."
    track_coach "And study, though I don't need to be the one to tell you that."
    mc "I've got it covered."
    track_coach "Good. Then I expect you back Friday with the same foot."
    mc "Wasn't planning to swap it."
    track_coach "Go home, [player]."
    show track_coach at thide
    hide track_coach
    "He walks off, and I honestly can't tell whether that was encouragement or a threat."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "My calves start tightening on the walk to the station, so I slow down and let the bag bump along against my hip. By the time I'm home, I've planned dinner three different ways."
    call nier_clear from _call_nier_clear_0521_5
    stop music fadeout 1.0
    pause 2.0
    scene bg kitchen_evening
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    play music house_day_a
    # SFX SUGGESTION: Gentle bubbling water layered with a low pan sizzle.
    "A pot boils on the stove while a pan of sauce warms beside it. Garlic nearly disguises the last respectable bell pepper in the fridge."
    "Spaghetti: The traditional reward for ignoring groceries too long."
    "My shins are starting to remember practice."
    show asahina teasing at l11
    ah "Wait, you're actually cooking? I thought we were microwaving stuff."
    mc "Because I'm a provider, thank you very much."
    show asahina unamused
    ah "You're boiling noodles. Calm down."
    mc "The sauce is in the pan. Try that before you complain."
    show asahina curious
    "She leans around me to inspect the pan."
    ah "Are those peppers? You put peppers in it?"
    mc "Yeah. Your favorite, actually."
    show asahina disgusted
    ah "...You're {i}actually{/i} a villain."
    mc "You can pick them out if you want."
    mc "Or just try one. I cooked them this time. That, or you can explain to Mom why little Asa doesn't eat her veggies."
    show asahina frustrated
    ah "Last time they were crunchy! You barely warmed them up!"
    "My phone buzzes on the counter before the argument can escalate."
    "The screen lights up with Mom's name."
    python:
        _phone_messages = [
            phone_msg("them", "Court ran long and the file is still fighting back."),
            phone_msg("them", "Please do not wait dinner on me. I'll be home late again, unfortunately."),
            phone_msg("them", "If everything stays on schedule, the workload should lighten after the next couple days."),
            phone_msg("me", "We have spaghetti. I'll save you a plate."),
            phone_msg("them", "Thank you. Please make sure your sister eats something that isn't junk."),
            phone_msg("me", "peber"),
            phone_msg("them", "Proud of you."),
        ]
    call phone_text_conversation("Mom", _phone_messages, append=True) from _call_phone_text_conversation_0521_1
    # Her first real thread rather than a note left on the counter, and it ends
    # with her being warm at him. Idle texting with Mom opens here.
    $ phone_open("mom")
    "Without Mom's podcast playing from the counter, I can hear the pot lid rattle against its rim. I turn down the heat while Asahina gets plates."
    show asahina curious
    ah "Late again?"
    mc "Yeah."
    mc "She says it should ease up in a couple days."
    ah neut "She said that on Monday."
    mc "I know. Pass me a plate?"
    show asahina shocked
    ah "Are you giving her all the good sauce? I've got, like, one spoonful."
    mc "You were {i}just{/i} complaining about the sauce."
    show asahina smug
    ah "...I'm telling your three girlfriends that you bully me."
    "She grabs two plates from the cabinet. After a pause, she reaches for a third."
    "Mom's serving gets covered and left at her usual place."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Dinner is mostly successful."
    nier "The sauce holds together. The noodles are a minute past the point where an Italian would throw me overboard."
    nier "Asahina actually ends up eating her vegetables, though she puts on a respectable tragedy about it first."
    call nier_clear from _call_nier_clear_0521_6
    pause 2.0
    scene bg dining_table_night
    $ show_calendar()
    $ atmos("home_night")
    show asahina determined at t11
    with wipeleft_scene
    "My sister studies her fork as she winds spaghetti around it."
    show asahina curious
    ah "So track didn't kill you, which is disappointing for at least one of us."
    mc "True, but I probably flailed like a maniac."
    show asahina teasing
    ah "So you looked stupid. How stupid we talking?"
    mc "Coach stopped me before I turned light practice into a race, if that amounts to anything."
    show asahina smug
    ah "Rare adult W."
    show asahina neut
    "She takes another bite, then points her fork at me."
    ah "...Rooftop girl was kinda cool."
    mc "Tsubaki?"
    ah "Yeah."
    ah "She was going to leave until you asked her to sit down."
    mc "That's... I mean, yeah."
    show asahina unamused
    ah "I was sitting right there, dumbass."
    mc "Pfft, debatable."
    show asahina annoyed
    ah "Keep talking and you're wearing the rest of the spaghetti!"
    mc "Okay, okay, I'm sorry! Put the fork down."
    show asahina smug
    ah "Relax, it's spaghetti. Worst case, you catch a wet noodle to the face."
    mc "Anyway, she's Matsuda's friend. The quiet one from Saturday."
    show asahina thinking
    ah "Yeah, no, I got that part. Must be exhausting, honestly."
    "Matsuda's three-part review of that game's menu screen from last night drifts back to me, and I end up grinning at my plate."
    mc "Eh, Matsuda's fun. Who else is gonna trash a game's menu design with me at eleven at night?"
    mc "Besides, Tsubaki's been her friend since April. She can't hate it that much."
    show asahina neut
    ah "Liking somebody and wanting to eat lunch with them every single day are two different things."
    "I open my mouth, and nothing smart comes out of it."
    mc "...Yeah. Fair."
    "Her fork darts across the table and comes back with a noodle off my plate."
    mc "Hey!"
    show asahina teasing
    ah "Sister tax."
    mc "Tax on {i}what{/i}?"
    show asahina disgusted
    ah "On making me eat {i}literally{/i} my least favorite vegetable. Pay up."
    mc "...This government is corrupt."
    show asahina smug
    ah "Sounds like a you problem~"
    "She hooks an ankle around the chair leg and takes her sweet time twirling the stolen noodle."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I wash and Asahina dries, though mostly she argues about which cabinet everything lives in. Mom's plate goes into the fridge with a note on the lid, and we head upstairs."
    call nier_clear from _call_nier_clear_0521_7
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music night_b
    "Night finds me at my desk with a notebook open and an ice pack balanced against my ankle."
    # SFX SUGGESTION: An incoming-call vibration rattling steadily against the desk.
    "I've gotten through half a page of chemistry and exactly one matrix problem when my phone starts rattling against the desk."
    "{i}... Why am I not surprised it's you?{/i}"
    call phone_call("Monika", status="Incoming Call", can_decline=False) from _call_phone_call_0521_1
    python:
        _phone_call_lines = [
            phone_call_line("me", "Jake's pizzeria and crematorium, where yesterday's loss is today's sauce. How can I help?"),
            phone_call_line("them", "Wow, not even a hello?"),
            phone_call_line("me", "...Hello, this is Jake's pizzeria and crematorium."),
            phone_call_line("them", "Why hello, Jake! How was practice?"),
            phone_call_line("me", "I nearly promoted light practice to regular practice."),
            phone_call_line("them", "Did Coach catch you?"),
            phone_call_line("me", "Across the entire field. Everyone heard and it was kind of baffling."),
            phone_call_line("them", "Good. Saves me doing it tomorrow!"),
            phone_call_line("me", "I really missed running, though. Even the bit where I feel terrible afterward."),
            phone_call_line("them", "I get that. My legs itch if I spend a whole afternoon sitting down."),
            phone_call_line("me", "Then why are you still sitting there?"),
            phone_call_line("them", "Because I keep thinking I'll finish this page if I stay another five minutes."),
            phone_call_line("me", "Let me guess: the handout with the cup and the ominous door?"),
            phone_call_line("them", "Yes! I understand the passage. I just don't like anything I've written about it."),
            phone_call_line("me", "Say the cup did it. They'll {i}have{/i} to give you marks for originality."),
            phone_call_line("them", "Something tells me they won't."),
            phone_call_line("me", "Leave it a minute. I found something you'll like."),
            phone_call_line("them", "If this is another man restoring a knife for forty minutes--"),
            phone_call_line("me", "Three minutes. Monster effects. I'm sending it now."),
            phone_call_line("them", "Oh! They actually built that thing?"),
            phone_call_line("me", "Different film. Same guy doing the creatures, apparently."),
            phone_call_line("them", "Wait, don't start. I'm getting my headphones."),
            phone_call_line("me", "Ready? Three, two, one."),
            phone_call_line("them", "Eeeugh, I hate those teeth. Why did they make them move separately?"),
            phone_call_line("me", "Watch underneath. There are two people in there."),
            phone_call_line("them", "I can see the shoes! Oh, that ruins it."),
            phone_call_line("me", "It makes it better. Imagine being the back half of that thing all day."),
            phone_call_line("them", "I'd want to be the front. If I'm going to sweat inside a monster, I'm getting the teeth."),
            phone_call_line("me", "Naturally. I'd be the guy shaking the fence right here."),
            phone_call_line("them", "You'd get bored and shake it before the monster arrived."),
            phone_call_line("me", "Wind. Very atmospheric."),
            phone_call_line("them", "Hold on, play that bit again. Did its head just fall off?"),
            phone_call_line("me", "Yeah. He's still doing the claws."),
            phone_call_line("them", "He can't see! Someone tell him!"),
            phone_call_line("me", "Wait for it..."),
            phone_call_line("them", "Oh, he's looking through its neck... That's horrible... I love it."),
            phone_call_line("me", "I'll keep an eye out for the film. We should watch it when it's out."),
            phone_call_line("them", "Yes! Even if the reviews are less than savory."),
            phone_call_line("me", "{i}Especially{/i} then."),
            phone_call_line("them", "Okay, I needed that. I was starting to hate that stupid cup."),
            phone_call_line("me", "You're welcome. Asa would've complained about me pausing it."),
            phone_call_line("them", "Because you do pause things constantly."),
            phone_call_line("me", "Only the good bits."),
            phone_call_line("them", "That's when I want to watch them! How is she, anyway?"),
            phone_call_line("me", "Pleased with her poster. She had lunch with me and Tsubaki today."),
            phone_call_line("them", "Tsubaki Kareda?"),
            phone_call_line("me", "Yeah."),
            phone_call_line("them", "Oh, I've seen her around."),
            phone_call_line("me", "Do you know her? And am I the only one who doesn't think there's only one person with their own name at school?!"),
            phone_call_line("them", "Ahhhhh, trust me, there's one one Tsubaki at school. Council has the whole roster, remember?"),
            phone_call_line("me", "Uh huh... But yeah, you know her?"),
            phone_call_line("them", "Only to say hello. She helped carry some council supplies in April."),
            phone_call_line("me", "She knows Matsuda. Told us a story about her taking over the supply committee."),
            phone_call_line("them", "That explains how a box of marker pens arrived labeled 'armaments.'"),
            phone_call_line("me", "That sounds about right."),
            phone_call_line("them", "Well, anyhoo, I'm going to try that page once more, then stop. You should get some sleep."),
            phone_call_line("me", "Yeah. Thanks for calling."),
            phone_call_line("them", "Go ice your foot properly, track boy."),
            phone_call_line("me", "Call me that again and your head's on a pike."),
            phone_call_line("them", "Hahaha~"),
            phone_call_line("me", "Goodnight, Monika."),
            phone_call_line("them", "Goodnight, " + player + "!"),
        ]
    call phone_call_conversation("Monika", _phone_call_lines, status="Connected") from _call_phone_call_conversation_0521_1
    # A long, aimless late call that neither of them needed to make. Calling her
    # about nothing is now a normal thing to do.
    $ phone_open("monika_call")
    "After she hangs up, I retrieve the ice pack from wherever it slid off to and finish the chemistry notes with the monster clip still paused in the corner of my screen."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "After I turn out the light, I hear Mom come in and open the fridge downstairs. I'm still awake when the microwave beeps, but not when she comes up."
    call nier_clear from _call_nier_clear_0521_8
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0521_1
    jump a0522
