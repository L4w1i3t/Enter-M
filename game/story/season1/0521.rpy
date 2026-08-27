label a0521:
    # --- Day 7: 2025-05-21 ---
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with dissolve_scene_full
    play music quiz
    window auto
    # CRITIQUE (ADDRESSED): Thinned the narrator quips at the open (and consolidated the three single-word italic lines) so the omitted-agency idea -- a direct mirror of the story's own evasions, and of MC's narration -- gets room to breathe before the lesson begins.
    "Sleep took its time last night, so I walk into language arts running at about seventy percent. Naturally, this is the day the class is asked whether a comma can be morally implicated."
    "The teacher has already filled half the board before the bell finishes surrendering."
    "{i}Narrative distance. Narrative dissonance. Focalization. Agency through ellipsis.{/i}"
    show japanese_teacher neut at t11
    japanese_teacher "For the midterm, assume definitions are the bare minimum for what I ask."
    japanese_teacher "If you write that focalization is merely who sees the scene, or that ellipsis is merely something left out, you have described the tool without explaining the work it performs."
    "A small wave of movement passes through the room as everyone develops their personal relationships with dread."
    japanese_teacher "Yes, that means written responses."
    "The wave gets worse."
    "{i}Or is it just me? Maybe I'm the problem.{/i}"
    japanese_teacher "A strong answer should move from syntax, to narrative effect, to thematic consequence."
    japanese_teacher "Device, pressure, meaning. In that order. There's your bread and butter."
    "{i}Cool. I love literature combos.{/i}"
    "The teacher taps the third phrase, the chalk giving a dry click."
    japanese_teacher "This kind of prose allows subjects to disappear without the sentence collapsing."
    japanese_teacher "That flexibility can be graceful, but in fiction it can also become evasive."
    japanese_teacher "When a passage repeatedly refuses to identify who acts, the omission does not only create ambiguity. It can redistribute guilt."
    "My pen moves because my survival instincts still have administrative skills."
    japanese_teacher "Now, consider the passage on the handout."
    # SFX SUGGESTION: A brief wave of paper rustling across the classroom.
    "Pages rustle across the classroom."
    "The excerpt is short, which is usually how teachers hide knives."
    "A narrator returns home after an argument to find the light off and a cup waiting on the table. The door is still open."
    "A formal passive construction describes the room as having been left behind, but the person who left it that way never gets named."
    "{i}Cheerful.{/i}"
    japanese_teacher "Notice the pattern."
    japanese_teacher "The passage gives us evidence of action while withholding a stable actor."
    japanese_teacher "It also keeps the emotional vocabulary restrained, almost procedural."
    japanese_teacher "So the question is not whether the author forgot to name the subject."
    "I make the strategic error of looking at the handout like a person who knows how to read."
    japanese_teacher "[player]."
    mc "...Yeah?"
    japanese_teacher "Bell ringer for you: how does the repeated subject omission alter the reader's ability to assign agency, and how does that support the passage's treatment of guilt?"
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
        mc "It makes the reader participate in assigning culpability. The actions are concrete, but the missing subjects keep responsibility unstable."
        mc "The reader has to decide whether the narrator is genuinely unsure or quietly steering blame elsewhere."
        japanese_teacher "Great answer!"
        "She circles the empty bracket, then draws a thin arrow from it to the phrase about guilt."
        japanese_teacher "That is the kind of answer I expect on Monday."
        jump japanese_answer1done
    label japanese_wronganswer1:
        $ atmos_pressure_clear()
        with dissolve
        japanese_teacher "Not quite."
        japanese_teacher "The restrained diction may resemble objectivity, but the effect is not neutral."
        japanese_teacher "The omission controls where blame can settle."
        "She circles the empty bracket, then draws a thin arrow from it to the phrase about guilt."
        japanese_teacher "For the midterm, do not stop at tone. Explain what the syntax makes the reader {i}do{/i}."
        mc "Right. Got it."
        jump japanese_answer1done
    label japanese_answer1done:
        pass
    japanese_teacher "Everyone should annotate the passage with this in mind."
    japanese_teacher "Mark the verbs first, then identify where the sentence withholds the actor."
    "The room closes around the scratch of pens and turning pages."
    "I underline the evidence and the passive verb. Then I mark the sentence where the narrator refuses to say I without technically lying."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "By the end of class, my handout looks less annotated and more like a warzone of pencil lead."
    call nier_clear from _call_nier_clear_0521_1
    stop music fadeout 1.0
    pause 2.0
    scene bg rooftop
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music schooldays
    "The rooftop is one of those places students call secret because teachers don't bother correcting the myth unless someone starts throwing things."
    "A warm breeze moves over the fence and turns the plastic around my food, making it rattle like some sort of instrument."
    "{i}Mom packed rice and vegetables before bolting out the door.{/i}"
    "I get two bites in before the rooftop door opens."
    show asahina uniform neut at l11
    ah "There you are!"
    mc "Uh oh, that sounded like a threat."
    ah "I've been trying to find you everywhere!"
    mc "...You looked for me for, what, twenty seconds?"
    ah "Hey, loyalty's all that matters."
    play sound moddoorclose
    "My sister steps fully onto the roof and lets the door close behind her with a metallic click."
    scene bg rooftop
    $ show_calendar()
    $ atmos("afternoon")
    show asahina uniform neut at t11
    with dissolve
    "Her lunch bag hangs from one hand. The other is already busy with her phone, since the phone has priority over balance."
    ah "I texted you before last period and didn't get a response."
    mc "I was doing important senior business. I have a life, you know."
    ah "Such as eating alone like a suspicious old hermit?"
    "She sits beside me and claims the usual sibling share of my personal space."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg rooftop
    $ show_calendar()
    $ atmos("afternoon")
    show asahina uniform neut at t11
    with wipeleft_scene
    "For a minute we eat and nothing dramatic happens, a level of maturity neither of us has earned."
    show asahina uniform happy
    ah "Here's some news: poster went up this morning."
    mc "Oh?"
    ah "And it's still on the wall, so my cheap-ass tape is doing a better job than I thought."
    mc "Nature is healing, I see."
    ah "Also, a couple people said it looked good."
    show asahina uniform embarrassed
    "She says it into her chopsticks like the rice needs to hear it more than I do."
    mc "Seems like people have good taste, then."
    show asahina uniform annoyed
    ah "Don't make it weird."
    mc "...I say ONE nice thing, and you get defensive."
    show asahina uniform smug
    ah "Exactly! Historically suspicious."
    "I put a piece of carrot in my mouth and consider launching it at her."
    mc "Oh yeah, track starts back up for me today, by the way."
    show asahina uniform unamused
    ah "Yeah, Mom said."
    ah "Try not to die out there. I don't wanna have to arrange your funeral."
    mc "That was nearly concern. Should I document it?"
    show asahina uniform teasing
    ah "I need you alive. Who else am I supposed to blame for stuff?"
    mc "...I'm touched by my strategic value."
    show asahina uniform worried
    "She sets her chopsticks down across the lid of her food."
    ah "Your foot {i}is{/i} actually fine, right?"
    mc "Yeah."
    mc "Mostly fine, anyway."
    mc "Coach said light practice, so today is warmups and a few drills. The hard part is not getting overzealous."
    ah "...Good."
    mc "Wooooow. You meant that.~"
    show asahina uniform embarrassed
    ah "Don't make it a thing! I'll take it all back!"
    mc "No takebacks, it's already in the history books."
    "The rooftop door opens again before she can aim anything at me."
    show asahina uniform curious at t21
    show tsubaki uniform neut at l22
    "A girl steps out with a small lunch bag clasped in both hands."
    show tsubaki uniform happy
    "For a beat, she looks relieved."
    show tsubaki uniform shocked
    "Then she sees us and looks like she accidentally walked into the wrong meeting room."
    show tsubaki uniform nervous
    ts "Ah--sorry! I thought this side was empty."
    mc "...Tsubaki?"
    show tsubaki uniform curious
    ts "...Oh!"
    ts "[player], right?"
    ah "Wait, you two know each other?"
    mc "Uh...yeah...sorta."
    show asahina uniform happy
    ah "OH! Sidewalk traffic! That's her, right?!"
    mc "No...that was Matsuda, 'member? {i}She{/i} was just collateral."
    show tsubaki uniform embarrassed
    ts "I'm still very sorry about that."
    mc "You weren't even the one I ran into, why are {i}you{/i} apologizing?"
    show tsubaki uniform nervous
    ts "I still feel a little responsible..."
    "My first instinct is to call it a habit. Then the paper bag gives a soft crackle in her grip."
    "{i}Or maybe that answer is just convenient.{/i}"
    show asahina uniform unamused
    ah "You apologized for...being a witness?"
    ts "Only a little."
    show asahina uniform pose_hairflip
    ah "I'm Asahina, by the way. I'm this idiot's superior sister."
    show tsubaki uniform curious
    ts "Asahina..."
    ts "From the volleyball poster, right?"
    show asahina uniform nervous
    ah "Oh. Yeah."
    ah "Please tell me it didn't fall down already..."
    show tsubaki uniform determined
    ts "No! It looked really good."
    show tsubaki uniform happy
    ts "The lettering was clean, and the little motion lines around the ball made it easy to notice from the hall."
    show tsubaki uniform thinking
    ts "And the watermark in the corner...it weirdly works? I don't know how to explain it."
    show asahina uniform embarrassed
    ah "...Thanks."
    ah "It was whatever, though."
    mc "That means she's about to frame your review."
    show asahina uniform annoyed
    ah "I am NOT!"
    show tsubaki uniform neut
    ts "It's okay to be proud of work."
    show tsubaki uniform happy
    ts "I was glad I noticed it, if that helps!"
    ah "Don't patronize me, you--"
    "Tsubaki's correction is quiet. It lands before I can joke over it."
    show asahina uniform neut
    ah "...Yeah, well."
    ah "It got the job done."
    show tsubaki uniform nervous
    "Tsubaki shifts one foot back toward the door."
    mc "You can sit if you want."
    ts "Oh, uh, I don't want to intrude if you two are doing something."
    show asahina uniform happy
    ah "There's no lunch court up here, dude. Total free-for-all."
    show tsubaki uniform embarrassed
    ts "Right. Sorry."
    "She sits a careful distance away and keeps her lunch bag on the door side of her knees."
    scene black with wipeleft_scene
    pause 1.0
    scene bg rooftop
    $ show_calendar()
    $ atmos("afternoon")
    show asahina uniform neut at t21
    show tsubaki uniform neut at t22
    with wipeleft_scene
    "The three of us eat in an uneven rhythm. Asahina fills every pause without noticing."
    "Tsubaki waits until the openings are unmistakably hers."
    show tsubaki uniform worried
    ts "Is...your shoulder better?"
    mc "Yeah. It was barely anything, I swear."
    show asahina uniform smug
    ah "He complained about it like three times."
    mc "Do NOT make up stories about me!"
    show tsubaki uniform neut
    ts "Matsuda was worried for almost seven minutes at the vending machine after you left."
    mc "...Almost seven?"
    show tsubaki uniform smug
    ts "Hey, a win's a win. That's rather long for her when the worry isn't disguised as a speech."
    show asahina uniform curious
    ah "So tell me, how much of the rumors are true? She always that much?"
    ts thinking "She's...how do I put it?"
    # Matsuda is a third-year and Tsubaki a second-year, so the public anecdote
    # stays in a mixed-year committee. Tsubaki keeps the private ending for a
    # later lunch, after the group has earned more of her confidence.
    ts neut "At the start of the year, I got put on the supply committee. It's mixed years, and I was the only second-year there."
    ts "At the first meeting, the teacher asked who would take inventory lead. Nobody moved."
    ts teasing "Matsuda stood up and gave a two-minute acceptance speech for a job nobody had offered her."
    ts "Then she thanked the committee for its unanimous confidence in her. We hadn't voted."
    ah shocked "No."
    ts happy "Two minutes, start to finish. She got the job, obviously."
    "Tsubaki looks down and smooths the same crease in her lunch bag twice."
    mc "Oh, she's a third-year?"
    ts neut "Mhm. Same year as you."
    ts "She transferred in right at the start of it."
    mc "Huh. Don't think it ever came up."
    ah unamused "You've shared a building since April and you found her with your shoulder."
    mc "...So she volunteered herself into a job and it worked."
    ts teasing "By the second minute, saying no would have required its own speech."
    ah happy "Okay. That's actually incredible."
    ts happy "Besides, she's actually pretty harmless. Seriously."
    "The answer is so earnest that Asahina blinks twice before laughing."
    ts shocked "...Oh, shoot. I should go before the stairs get crowded."
    mc "Already?"
    ts neut "I need to return a book to my classroom before fifth period."
    ts teasing "And, um, the Boogeywoman will start searching if I'm too hard to find."
    ah unamused "That sounds exhausting."
    ts sad "Sometimes it is, yeah."
    ts neut "But honestly, I'd do the same for her. Scratch my back and all that."
    "She stands and smooths the fold out of her skirt."
    ts happy "It was nice meeting you, Asahina."
    ts "And seeing you again, [player]."
    ah "Yeah. You too."
    mc "Later, Tsubaki."
    ts "Talk later!"
    show tsubaki at thide
    hide tsubaki
    "She slips through the door with less noise than the door itself makes."
    play sound moddoorclose
    show asahina uniform determined at t11
    ah "She apologized for witnessing you walk into someone."
    ah "She's under my protection now."
    mc "I can feel the balance of power shifting. Shiver me timbers."
    ah "Yeah, obviously. Effective immediately."
    # SFX SUGGESTION: A distant school warning bell, slightly muffled by the rooftop door.
    "The warning bell rings from somewhere below us."
    show asahina uniform frustrated
    "Asahina groans like the school has personally betrayed her."
    mc "Back to civilization we go..."
    ah "Booooooo."
    "We gather our things and head for the door, two heroic survivors of a break that lasted maybe four minutes."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Chemistry reviews ions while algebra assigns more problems. English reminds us that vocabulary is also on the midterm."
    call nier_clear from _call_nier_clear_0521_2
    stop music fadeout 1.0
    pause 2.0
    scene bg track_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music daily
    # CRITIQUE (ADDRESSED): Thinned the legal/courtroom jokes that intruded on the running so the physicality can breathe -- the stride beats now stay with breath, foot, and lungs instead of "filing a formal objection." Kept one framing joke and the Coach banter, since those are MC's voice rather than intrusions.
    "The track looks exactly how I remember it."
    "Afternoon heat lifts in thin, restless waves from the red lanes and their white lines. A few team members are already jogging the curve."
    "Their shoes land in the even cadence that makes running look less hostile than it truly is."
    "{i}Have I really not done this since school started back up...? Time flies.{/i}"
    show track_coach neut at t11
    track_coach "[player]!"
    "Coach's voice cuts across the infield before I can pretend to tie an already tied shoe."
    track_coach "You're cleared for light practice, correct?"
    mc "That's the official verdict."
    track_coach "Then we follow it."
    track_coach "Warmup lap and mobility, then strides at seventy percent. No heroics."
    mc "I left my cape at home."
    track_coach "Good. It would slow you down."
    track_coach "...Actually, one of these days I might have you on the parachute, so..."
    "He says it flat, with no smile attached. That is what a decent mood looks like on him."
    "I join the warmup line near the outside lane."
    "The first few steps feel too careful."
    "{i}No pain. Maybe some tightness, plus more paranoia than either one deserves.{/i}"
    "By the first curve, the caution starts loosening."
    "{i}Breath steady. Arms loose, eyes forward.{/i}"
    "The track stops being a question and turns back into a shape."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Warmups give way to drills and the particular humiliation of dynamic stretching in public."
    nier "Every high-knee and lunge makes us look like we're negotiating with invisible furniture."
    nier "Coach watches as if bad form is a moral failing."
    call nier_clear from _call_nier_clear_0521_3
    pause 2.0
    scene bg track_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    "The first stride starts at the curve."
    "Seventy percent sounds gentle until your body remembers that percentages are lies invented by coaches to sell more practice."
    "I push off anyway."
    "I spend the first few seconds waiting for the foot to flare. By halfway, my lungs are the louder problem."
    "Then I notice I'm moving faster than I meant to, and nothing has gone wrong yet."
    "{i}Oh.{/i}"
    "{i}So the body remembered. It just didn't bother telling me first.{/i}"
    "I coast down before the end of the straightaway and walk out onto the grass, hands on my hips."
    "My breath is rough, but not wrecked. My foot is present, but not angry."
    track_coach "Again."
    mc "Was that a good again or a bad again?"
    track_coach "Again without commentary, [player]."
    mc "...Got it."
    "A couple of nearby runners snicker and Coach points to the curve."
    track_coach "Seventy percent."
    mc "Bro, that WAS seventy!"
    track_coach "That was closer to eighty."
    mc "Hey, I don't know math, okay?"
    "{i}Excellent. Next time, pick an excuse with a pulse.{/i}"
    track_coach "Then use your lungs. Play it by ear instead of metric."
    "I walk back to the start."
    "{i}Fair enough. My lungs are giving me plenty to go on.{/i}"
    "The second stride feels better because I stop waiting for disaster to RSVP."
    "The third feels worse because confidence is an idiot and tries to add speed."
    track_coach "Easy now..."
    "The words snap me back before I do something impressively stupid."
    "I pull off the pace and let the final meters roll under me."
    "{i}Right. Light practice, not a comeback montage.{/i}"
    "{i}...Yet.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The rest is cooldown and stretching while the main group starts intervals I would normally run."
    call nier_clear from _call_nier_clear_0521_4
    pause 2.0
    scene bg track_evening
    $ show_calendar()
    $ atmos("evening")
    with wipeleft_scene
    "By the time practice breaks, the afternoon has softened around the edges. I sit on the grass near my bag and tug at one shoelace until it gives."
    "Sweat cools at the back of my neck. My legs feel used, but far from destroyed."
    show track_coach neut at t11
    track_coach "How's the foot?"
    mc "Still attached."
    track_coach "You know what I mean, [player]."
    mc "A little tight. Not painful, just annoying."
    track_coach "Good. Ice it tonight if it starts talking."
    track_coach "Friday, tell me before practice if it changes."
    mc "Got it."
    track_coach "And study, though I don't need to be the one to tell you that."
    mc "...For track?"
    track_coach "For midterms, smartass."
    track_coach "Academic eligibility does not care what your excuses are."
    mc "...I swear, every department hounds me these days..."
    track_coach "Good. People gotta keep you on your toes."
    show track_coach at thide
    hide track_coach
    "He walks off before I can decide whether that was encouragement or a threat."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I leave school tired in a cleaner way than yesterday."
    nier "My bag thumps against my hip, and my clothes smell faintly of rubber. By the station, my calves have begun their slow argument with tomorrow."
    call nier_clear from _call_nier_clear_0521_5
    stop music fadeout 1.0
    pause 2.0
    scene bg kitchen_evening
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    play music dailyleisure
    # SFX SUGGESTION: Gentle bubbling water layered with a low pan sizzle.
    "A pot boils on the stove while a pan of sauce warms beside it. Garlic nearly disguises the last respectable bell pepper in the fridge."
    "Spaghetti. The traditional reward for ignoring groceries too long."
    "My shins are starting to remember practice."
    show asahina teasing at l11
    ah "Why does it smell like you tried?"
    mc "Because I'm a provider, thank you very much."
    show asahina unamused
    ah "You're putting noodles in water."
    mc "Okay, and? If you have a witty remark, just say it."
    show asahina curious
    "She leans around me to inspect the pan."
    ah "Did you put vegetables in it?"
    mc "Yeah. Your favorite, actually."
    show asahina disgusted
    ah "...You're {i}actually{/i} a villain."
    mc "You're not a little kid, ya spaz. Don't athletes need a well-balanced diet?"
    show asahina frustrated
    ah "Yeah, but you threw the whole Amazon in there! We got peppers with a side of sauce!"
    "My phone buzzes on the counter before the argument can escalate."
    "The screen lights up with Mom's name."
    # CRITIQUE (ADDRESSED): Let the house feel thinner when Mom's gone instead of treating her absence as pure logistics -- the kitchen is too quiet without the noise she usually fills it with, "just two people and a pot." Gives her later illness arc some lived-in texture to land on. (The default third place setting, covered and waiting, stays as the other half of this.)
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
    "The house is quieter than it should be at this hour. Mom usually fills the kitchen with crooked pot lids and a podcast determined to explain parliament to her."
    "Without her, dinner is just two people and a pot."
    show asahina neut
    ah "Late again?"
    mc "Yeah. She says it should lighten up after a couple days if the schedule behaves."
    ah "Yeah, sure, schedules behave on their own."
    mc "Spoken like someone who doesn't."
    show asahina shocked
    ah "Wow. Wowwww. Are you seriously slandering me?"
    mc "Not slander if it's the truth."
    show asahina smug
    ah "...I'm telling your three girlfriends that you bully me."
    "She grabs two plates from the cabinet. After a pause, she reaches for a third."
    "Mom's serving gets covered and left at her usual place."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Dinner is mostly successful."
    nier "The sauce holds together, and the noodles are only slightly past the point where an Italian would throw me overboard. Asahina eats her vegetables after putting on a respectable tragedy about it."
    call nier_clear from _call_nier_clear_0521_6
    pause 2.0
    scene bg dining_table_night
    $ show_calendar()
    $ atmos("home_night")
    show asahina determined at t11
    with wipeleft_scene
    "Asahina studies her fork as she winds spaghetti around it."
    show asahina curious
    ah "So track didn't kill you."
    mc "True, but I probably flailed like a maniac."
    show asahina teasing
    ah "That means you looked stupid."
    mc "Coach stopped me before I made a poor decision. I was about five seconds from turning light practice into tempo work."
    show asahina smug
    ah "Rare adult W."
    show asahina neut
    "She takes another bite, then points her fork at me."
    ah "...Rooftop girl was kinda cool."
    mc "Tsubaki?"
    ah "Yeah."
    ah "She looked like she wanted permission to sit down in an open area."
    mc "That's...weirdly accurate."
    show asahina unamused
    ah "I have eyes, you know."
    mc "Pfft, debatable."
    # CRITIQUE (ADDRESSED): Swapped the boiling-water threat for a non-violent, messier one (wearing the spaghetti). With the script tracking food/body stress and family safety, a casual scalding joke read harsher than the sibling rhythm supports; the pun chain survives intact.
    show asahina annoyed
    ah "Keep talking and you're wearing the rest of the spaghetti!"
    mc "Sorry, already strained and down the drain."
    show asahina smug
    ah "I'll make more. I've got noodles and a grudge."
    mc "She's Matsuda's friend, and, like she said, the other girl I met the other night."
    show asahina thinking
    ah "Yeah, I got that. That must be exhausting, honestly."
    "I remember Matsuda worrying for almost seven minutes, according to Tsubaki. I also remember her stopping mid-performance because I asked."
    mc "...Probably."
    mc "They call each other best friends. I figure they know what they're signing up for."
    show asahina neut
    ah "Best friends can still be exhausting. I have people I love who drain my whole social battery, so..."
    "I don't have a smart answer ready."
    mc "...Yeah, I guess it doesn't."
    "She reaches over and steals a noodle from my plate."
    mc "Hey!"
    show asahina teasing
    ah "Sister tax."
    mc "For...?"
    show asahina disgusted
    ah "Making me eat LITERALLY my least favorite vegetable."
    mc "...This government is corrupt."
    show asahina smug
    ah "Sounds like a you problem~"
    "She leans back like she believes the final word is her God-given human right."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "After dinner, I clean the kitchen while Asahina helps by standing nearby and offering commentary, which she claims is emotional support."
    nier "Mom's plate goes into the fridge with a note on top."
    call nier_clear from _call_nier_clear_0521_7
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music fantasyserenity
    "Night finds me at my desk with a notebook open and an ice pack balanced against my ankle."
    # SFX SUGGESTION: An incoming-call vibration rattling steadily against the desk.
    "I finish half a page of chemistry notes and one matrix problem before my phone starts buzzing."
    "{i}...Why am I not surprised it's you?{/i}"
    call phone_call("Monika", status="Incoming Call", can_decline=False) from _call_phone_call_0521_1
    python:
        _phone_call_lines = [
            phone_call_line("me", "Jake's pizzeria and crematorium, where yesterday's loss is today's sauce. How can I help?"),
            phone_call_line("them", "Wow...no hello?"),
            phone_call_line("me", "...Hello, this is Jake's pizzeria and crematorium."),
            phone_call_line("them", "Much better!"),
            phone_call_line("them", "So, you alive?"),
            phone_call_line("me", "I nearly promoted light practice to regular practice."),
            phone_call_line("them", "'Least you're suffering responsibly, right?"),
            phone_call_line("me", "The best kind, allegedly."),
            phone_call_line("me", "Why are you calling, anyway?"),
            phone_call_line("them", "To check on you, duh doy~"),
            phone_call_line("me", "That's suspiciously direct."),
            phone_call_line("them", "What can I say? Studying's kicking my butt, so I need a distraction."),
            phone_call_line("me", "There's the second motive."),
            phone_call_line("them", "Hey, both things can be true, you know!"),
            phone_call_line("them", "For example, I'm currently looking at my literature notes."),
            phone_call_line("me", "In the same way someone looks at a locked door?"),
            phone_call_line("them", "Exactly! Very observant, you are."),
            phone_call_line("me", "Speaking of, did you also get the handout with the cup and the ominous door?"),
            phone_call_line("them", "Yep. I decided the cup did it."),
            phone_call_line("me", "The cup, eh? Pray tell."),
            phone_call_line("them", "It had motive, or at least more of one than the door."),
            phone_call_line("me", "The door is clearly the mastermind. It was open when it should have been closed."),
            phone_call_line("them", "So the door and the cup were working together, you argue..."),
            phone_call_line("me", "A domestic conspiracy."),
            phone_call_line("them", "That sounds like a title."),
            phone_call_line("me", "My mom's a lawyer, so it definitely comes with the--"),
            phone_call_line("me", "Hey, I heard that pen click! Don't make it a club pitch!"),
            phone_call_line("them", "Too late, jotting it down now~"),
            phone_call_line("me", "...Everything I say can and will be used against me."),
            phone_call_line("them", "You really undersell yourself. Seriously, you come up with some profound stuff sometimes!"),
            phone_call_line("me", "Only sometimes? Damn, I see how it is."),
            phone_call_line("them", "Hahahaha~"),
            phone_call_line("me", "Okay, don't we have homework to finish? We're getting derailed, and I'd rather snip this in the butt."),
            phone_call_line("them", "Snip this in the--come ON, [player], you're better than that!"),
            phone_call_line("them", "...Or are ya just screwin' with me, hmmmmmmm?"),
            phone_call_line("me", "You tell me, Ms. Omnipotent."),
            phone_call_line("them", "Eheh... Either way, it's working."),
            phone_call_line("me", "Working toward...what?"),
            phone_call_line("them", "You sounding less tired!"),
            phone_call_line("me", "...Sneaky."),
            phone_call_line("them", "*yawn* A little, yeah. Apparently my distraction has a bedtime."),
            phone_call_line("me", "Mine should too. Track took a bite out of me before studying and two rooftop goblins got their turn."),
            phone_call_line("them", "Huh?"),
            phone_call_line("me", "...Guess I'll bite."),
            phone_call_line("me", "Asa found me at lunch, then another girl showed up. Tsubaki was her name."),
            phone_call_line("them", "Tsubaki Kareda?"),
            phone_call_line("me", "Yeah."),
            phone_call_line("them", "Huh. Interdasting..."),
            phone_call_line("me", "Do you know her?"),
            phone_call_line("them", "Not well, but enough."),
            phone_call_line("them", "She's usually with the recent transfer, and I honestly can't get a read on their chemistry."),
            phone_call_line("me", "Yeah, that checks out...probably."),
            phone_call_line("them", "Anyway, I'm going to rescue what's left of my notes and let you do the same."),
            phone_call_line("me", "A voluntary adjournment. Look at us."),
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
    "My room goes quiet again. The ice pack has slipped halfway off my ankle."
    "I set it back in place and look at the half-finished notes on my desk."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Mom gets home after I've turned out the light. I hear cabinet doors moving carefully downstairs, followed by the microwave."
    nier "I fall asleep before I can ask whether the spaghetti survived cross-exam."
    call nier_clear from _call_nier_clear_0521_8
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0521_1
    jump a0522
