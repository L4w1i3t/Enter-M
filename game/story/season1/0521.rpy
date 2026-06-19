label a0521:
    # --- Day 7: 2025-05-21 ---
    scene bg class_day
    $ show_calendar()
    show mood_afternoon zorder 3 
    with dissolve_scene_full
    play music quiz
    window auto
    # CRITIQUE (ADDRESSED): Thinned the narrator quips at the open (and consolidated the three single-word italic lines) so the omitted-agency idea -- a direct mirror of the story's own evasions, and of MC's narration -- gets room to breathe before the lesson begins.
    "Wednesday begins in language arts, which feels a little unfair."
    "Some subjects let you survive half-awake. You copy a diagram, solve the problem in front of you, wait for a date to appear on the board like a warning label."
    "Literature is not one of them. It notices your brain running at seventy percent and decides that's the perfect moment to ask whether a comma is morally implicated."
    "The teacher has already filled half the board before the bell finishes surrendering."
    "{i}Narrative distance. Focalization. Agency through ellipsis.{/i}"
    show japanese_teacher neut at t11
    japanese_teacher "For the midterm, assume definitions are the floor, not the answer."
    japanese_teacher "If you write that focalization is merely who sees the scene, or that ellipsis is merely something left out, you have described the tool without explaining the work it performs."
    "A small wave of movement passes through the room as everyone discovers a new and personal relationship with dread."
    japanese_teacher "Yes, that means written responses."
    "The wave gets worse."
    japanese_teacher "A strong answer should move from syntax, to narrative effect, to thematic consequence."
    japanese_teacher "Device, pressure, meaning. In that order."
    "{i}Device, pressure, meaning. Cool. Literature has combos now.{/i}"
    "The teacher taps the third phrase with the end of the chalk."
    japanese_teacher "This kind of prose allows subjects to disappear without the sentence collapsing."
    japanese_teacher "That flexibility can be graceful, but in fiction it can also become evasive."
    japanese_teacher "When a passage repeatedly refuses to identify who acts, the omission does not only create ambiguity. It can redistribute guilt."
    "My pen moves because my survival instincts still have administrative skills."
    "{i}Ellipsis as evasion. Agency blurred. Reader forced to assign culpability.{/i}"
    "{i}A note that looks impressive right up until future me has to explain it with a functioning brain.{/i}"
    japanese_teacher "Now, consider the passage on the handout."
    "Pages rustle across the classroom."
    "The excerpt is short, which is usually how teachers hide knives."
    "A narrator returns home after an argument. The door is open. The light is off. A cup waits on the table."
    "A formal passive construction describes the room as having been left behind, but the person who left it that way never gets named."
    "{i}Cheerful.{/i}"
    japanese_teacher "Notice the pattern."
    japanese_teacher "The passage gives us evidence of action while withholding a stable actor."
    japanese_teacher "It also keeps the emotional vocabulary restrained, almost procedural."
    japanese_teacher "So the question is not whether the author forgot to name the subject."
    "Her eyes move across the room."
    "I make the strategic error of looking at the handout like a person who knows how to read."
    japanese_teacher "[player]."
    mc "...Yeah?"
    japanese_teacher "How does the repeated subject omission alter the reader's ability to assign agency, and how does that support the passage's treatment of guilt?"
    show mood_pressure zorder 4
    show vignette zorder 5 at ambient_vignette(0.28)
    with dissolve
    "{i}Eye contact remains undefeated in academic combat.{/i}"
    menu:
        "It makes the reader participate in assigning culpability.":
            jump japanese_rightanswer1
        "It proves the narrator did not witness the event directly.":
            jump japanese_wronganswer1
        "It shifts the passage into objective documentary style.":
            jump japanese_wronganswer1
    label japanese_rightanswer1:
        hide mood_pressure
        hide vignette
        with dissolve
        mc "It makes the reader participate in assigning culpability."
        mc "The actions are concrete enough that we know something happened, but the missing subjects keep responsibility unstable."
        mc "So the reader has to decide whether the narrator is genuinely uncertain, avoiding blame, or making someone else's guilt easier to imagine."
        japanese_teacher "Great answer!"
        "She circles the empty bracket, then draws a thin arrow from it to the phrase about guilt."
        japanese_teacher "The omission does not erase action. It forces the reader to supply the actor."
        japanese_teacher "That is why the passage implicates the reader in the same interpretive act the narrator refuses to complete."
        japanese_teacher "That is the kind of answer I expect on Monday."
        "{i}Excellent. I have become a warning to others, but with thesis support.{/i}"
        jump japanese_answer1done
    label japanese_wronganswer1:
        hide mood_pressure
        hide vignette
        with dissolve
        japanese_teacher "Not quite."
        japanese_teacher "The restrained diction may resemble objectivity, but the effect is not neutral."
        japanese_teacher "The omission controls where blame can settle."
        "She circles the empty bracket, then draws a thin arrow from it to the phrase about guilt."
        japanese_teacher "For the midterm, do not stop at tone. Explain what the syntax makes the reader {i}do{/i}."
        mc "Right. Got it."
        "{i}I am going to connect myself to a lunch break as soon as legally possible.{/i}"
        jump japanese_answer1done
    label japanese_answer1done:
        pass
    japanese_teacher "Everyone should annotate the passage with this in mind."
    japanese_teacher "Mark the verbs first, then identify where the sentence withholds the actor."
    japanese_teacher "After that, write one sentence explaining how the withheld actor changes the reader's alignment with the narrator."
    "The room lowers itself into pen scratches and page turns."
    "I underline the open door, the cup, the passive verb, and the sentence where the narrator refuses to say I without technically lying."
    show japanese_teacher at thide
    hide japanese_teacher
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Language arts continues to make implication everyone else's problem."
    nier "By the end of class, my handout looks less annotated and more like it survived one of mom's civil disputes."
    nier "When lunch finally arrives, I leave the classroom with the haunted relief of someone granted parole for forty minutes."
    call nier_clear from _call_nier_clear_0521_1
    scene bg rooftop
    $ show_calendar()
    show mood_afternoon zorder 3 
    stop music fadeout 1.0
    with wipeleft_scene
    play music schooldays
    "The rooftop is not exactly secret."
    "It is one of those places students call secret because teachers don't bother correcting the myth unless someone starts throwing things."
    "A warm breeze moves over the fence and turns the plastic around my lunch into something loud enough to qualify as percussion."
    "I sit near the shade of the access structure with my back against the wall and my food balanced on my knees."
    "{i}Rice, vegetables, and whatever mom had the strength to assemble before she bolted out the door.{/i}"
    "{i}More than what I'd put together, honestly.{/i}"
    "I get two bites in before the rooftop door opens."
    scene bg rooftop_door
    $ show_calendar()
    show mood_afternoon zorder 3 
    with wipeleft_scene
    # CRITIQUE (ADDRESSED): Kept the poster as the occasion, not the basis. Asahina's protectiveness now keys on Tsubaki's space-anxiety (she said the nice thing and immediately looked terrified she'd overstepped), and the dinner beat reinforces it ("she looked like she wanted permission to sit down in an open area"). The poster stays secondary to Tsubaki's real issue.
    show asahina neut at t11
    ah "There you are."
    
    mc "Uh oh, that sounded like a threat."
    ah "I've been trying to find you everywhere!"
    mc "...You looked for me for, what, twenty seconds?"
    ah "Hey, loyalty's all that matters."
    mc "...I'm moved, truly."
    play sound moddoorclose
    "My sister steps fully onto the roof and lets the door close behind her with a metallic click."
    "Her lunch bag hangs from one hand. The other is already busy with her phone, because apparently balance is one of her powers."
    
    ah "I texted you before last period and didn't get a response."
    
    mc "I was doing important senior business. I have a life, you know."
    
    ah "Such as eating alone like a suspicious old hermit?"
    
    "She sits beside me with the practiced lack of ceremony that siblings reserve for invading personal space."
    scene bg rooftop
    $ show_calendar()
    show mood_afternoon zorder 3 
    show asahina neut at t11
    with wipeleft_scene
    "For a minute we eat without doing anything dramatic, which is suspiciously mature of us."
    ah "Here's some news: poster went up this morning."
    mc "Oh?"
    
    ah "And it's still on the wall, so my cheap-ass tape is doing a better job than I thought."
    
    mc "Nature is healing."
    ah "Also, a couple people said it looked good."
    "She says it into her chopsticks like the rice needs to hear it more than I do."
    mc "Seems like people have good taste, then."
    ah "Don't make it weird."
    mc "...I said ONE nice thing, and you get defensive."
    
    ah "Exactly! Historically suspicious."
    
    "I put a piece of carrot in my mouth and consider launching it at her."
    "{i}Maturity wins by a narrow margin.{/i}"
    mc "Oh yeah, track starts back up for me today, by the way."
    
    ah "Yeah, mom said."
    ah "Try not to die out there. I don't wanna have to arrange your funeral."
    
    mc "I appreciate your clinical concern."
    ah "I need you alive. Who else am I supposed to blame for stuff?"
    mc "...I am touched by my strategic value."
    "She pokes at her food, then glances at me in that way people do when the next sentence has been sitting in line for a while."
    ah "Your foot {i}is{/i} actually fine, right?"
    mc "Yeah."
    mc "Mostly fine, anyway."
    mc "Coach said light practice, so today is probably just warmups, a few drills, and HOPEFULLY not me getting overzealous."
    ah "...Good."
    mc "Wooooow. Genuine concern?"
    ah "Don't use my medicine against me! I'll take it all back!"
    
    mc "No takebacks, it's already in the history books."
    "The rooftop door opens again before she can aim anything at me."
    show asahina neut at t21
    show tsubaki neut at t22
    "A girl steps out with a small lunch bag clasped in both hands."
    "For half a second, she looks relieved."
    "Then she sees us and looks like she accidentally walked into the wrong meeting room."
    ts "Ah--sorry! I thought this side was empty."
    mc "...Tsubaki?"
    ts "...Oh!"
    ts "[player], right?"
    
    ah "Wait, you two know each other?"
    
    mc "We met by...having a run-in, so to speak."
    ah "OH! Sidewalk traffic!"
    
    ts "I'm still very sorry about that."
    mc "You weren't even the one I ran into, why are {i}you{/i} apologizing?"
    ts "I still feel kinda responsible..."
    # CRITIQUE (ADDRESSED): Reframed MC's contempt as a blind spot he corrects in real time. His first read ("self-pity") is uncharitable; the scene immediately shows it's something else -- a person braced to be told she's in the way -- and he registers the misread. Keeps his sharp eye without sneering at the character we're meant to come to care about.
    "{i}That's a lot of apologizing for a crime she didn't commit.{/i}"
    "{i}For half a second I file it under self-pity. Then I notice how she's holding the bag -- braced, like she's waiting to be told she's in the way.{/i}"
    "{i}...Not self-pity, then. Something with worse footing.{/i}"
    ah "You apologized for...being a witness?"
    ts "Only a little."
    "Asahina looks at me, then back at Tsubaki."
    ah "I'm Asahina, by the way. I'm this idiot's superior sister."
    "Tsubaki's fingers tighten around the paper bag."
    "Not enough to crumple it, just enough for the sound to answer before she does."
    ts "Asahina..."
    ts "From the volleyball poster, right?"
    
    ah "Oh. Yeah."
    ah "Please tell me it didn't fall down already..."
    
    ts "No! It looked really good."
    ts "The lettering was clean, and the little motion lines around the ball made it easy to notice from the hall."
    "Asahina's face does a complicated thing where it tries to accept praise, reject praise, and ask for more praise at the same time."
    ah "...Thanks."
    ah "It was whatever, though."
    mc "That means she's about to frame your review."
    ah "I am NOT!"
    
    ts "It's okay to be proud of work."
    "Tsubaki says it softly, and for some reason that makes it harder to joke over."
    ah "...Yeah, well."
    ah "It got the job done."
    "The rooftop wind slips between us."
    "Tsubaki shifts one foot back toward the door."
    mc "You can sit if you want."
    ts "Oh, uh, I don't want to intrude if you two are doing something."
    ah "There is no lunch court up here, dude."
    ts "Right. Sorry."
    "She sits a careful distance away, close enough to be included and far enough to flee if the conversation develops teeth."
    scene bg rooftop
    $ show_calendar()
    show mood_afternoon zorder 3 
    show asahina neut at t21
    show tsubaki neut at t22
    with wipeleft_scene
    "The three of us eat in an uneven rhythm."
    "Asahina's confidence takes up space without asking."
    "Tsubaki's caution takes up space by apologizing for having any."
    "I sit between them and discover that being the common link between two people is a job I did not apply for."
    ts "Is...your shoulder better?"
    mc "Yeah. It was barely anything, I swear."
    ah "He complained about it like three times."
    mc "Do NOT make up stories about me!"
    ts "Matsuda was worried for almost seven minutes at the vending machine after you left."
    mc "...Almost seven?"
    ts "Believe it or not, that's rather long for her when the worry is not disguised as a speech."
    "That sentence comes out with the casual accuracy of someone who has spent a lot of time translating a friend for public use."
    ah "So tell me, how much of the rumors are true? She always that much?"
    ts "She's kinda like...how to put it..."
    # CRITIQUE (ADDRESSED): Swapped the general theory for a specific anecdote that shows the same thing -- Matsuda filling a dead-silent homeroom with a fake acceptance speech while her hands shook. Tsubaki reveals Matsuda (and her own role as translator) through a concrete memory instead of stating a character model.
    ts "Okay, so -- first week of school, our homeroom went dead silent during attendance. Painfully silent."
    ts "Most people would just wait it out. Matsuda stood up and gave a two-minute acceptance speech thanking the alphabet for seating her near the front."
    ts "Everyone laughed. But I was right next to her, and her hands were shaking the whole time."
    ts "The louder she gets, the more she's covering for. ...That's just my read, though. She's never explained it to me, and I'm not a therapist."
    mc "...So that was when she was nervous?"
    ts "A wee bit, yeah."
    mc "How nervous are we talking?"
    ts "Mildly."
    ts "She doesn't like looking caught off guard."
    "Tsubaki pauses, then looks down at her food as if she said more than she meant to."
    ts "Please, for the love of everything, don't tell her I said that."
    mc "My lips are sealed, don't worry."
    ah "For a fee."
    mc "Asa!"
    
    ah "Whaaaaaaat?! I didn't name a price."
    
    ts "It's fine. I have no money on me anyway."
    ts "'Sides, she's actually pretty harmless. Seriously."
    "The answer is so earnest that Asahina blinks twice before laughing."
    "Tsubaki smiles after a delay, like she is checking whether the comment was allowed to land."
    "{i}There we go.{/i}"
    ts "Anyway, I should go before the stairs get crowded."
    mc "Already?"
    ts "I need to return a book to my classroom before fifth period."
    ts "And, um, the Boogeywoman will start searching if I'm too hard to find."
    
    ah "That sounds exhausting."
    
    ts "Sometimes it is, yeah."
    ts "But honestly I'd do the same for her. Scratch my back and all that."
    "She stands and brushes a nonexistent crumb from her clothes."
    ts "It was nice meeting you, Asahina."
    ts "And seeing you again, [player]."
    
    ah "Yeah. You too."
    
    mc "Later, Tsubaki."
    ts "Later!"
    show tsubaki at thide
    hide tsubaki
    "She slips through the door with less noise than the door itself makes."
    play sound moddoorclose
    "Asahina watches the door for a second."
    show asahina neut at t11
    ah "She's nice."
    
    mc "Yeah."
    
    ah "Like, painfully nice."
    
    mc "You say that like it's a medical condition."
    
    ah "It kinda looked like one. You gotta agree, right?"
    
    "I close my lunch container."
    mc "Be decent."
    
    ah "I {i}am{/i} being decent!"
    ah "She said the one nice thing and then looked terrified she'd said too much. So she's under my protection now."
    
    mc "Powerful alliance, shiver me timbers."
    
    ah "Oh yeah, you bet your sweet bippy it is."
    
    "The bell warning rings from somewhere below us."
    "Asahina groans like the school has personally betrayed her."
    mc "Back to civilization."
    
    ah "Booooooo."
    
    "We gather our things and head for the door, two heroic survivors of a break that lasted what felt like approximately four minutes."
    show asahina at thide
    hide asahina
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The afternoon classes pass in the rhythm of things that happen after lunch: slower than legally justified and twice as hard to focus on."
    nier "Chemistry reviews ions. Algebra assigns more problems. English reminds us that vocabulary will, somehow, also be on the midterm."
    nier "By the final bell, my brain has started filing every subject under the same folder."
    call nier_clear from _call_nier_clear_0521_2
    scene bg track_day
    $ show_calendar()
    show mood_afternoon zorder 3 
    stop music fadeout 1.0
    with wipeleft_scene
    play music daily
    # CRITIQUE (ADDRESSED): Thinned the legal/courtroom jokes that intruded on the running so the physicality can breathe -- the stride beats now stay with breath, foot, and lungs instead of "filing a formal objection." Kept one framing joke and the Coach banter, since those are MC's voice rather than intrusions.
    "The track looks exactly how I remember it."
    "Red lanes, white lines, afternoon heat lifting off the surface in thin, restless waves."
    "A few team members are already jogging the curve, their shoes landing in that even rhythm that makes running look less hostile than it is."
    "{i}I have not done this since school started back up.{/i}"
    "{i}A month is not long enough to forget how to run, but it is apparently long enough for my brain to start treating the track like a courtroom where my foot is on trial.{/i}"
    show track_coach neut at t11
    track_coach "[player]!"
    "Coach's voice cuts across the infield before I can pretend to be busy tying a shoe that is already tied."
    track_coach "You're cleared for light practice, correct?"
    mc "That's the official verdict."
    track_coach "Then we follow it."
    track_coach "Warmup lap, mobility, strides at seventy percent. No heroics."
    mc "I left my cape at home."
    track_coach "Good. It would slow you down."
    track_coach "...Actually, one of these days I might have you on the parachute, so..."
    "He says it without smiling, which is how I know he's in a decent mood."
    "I join the warmup line near the outside lane."
    "The first few steps feel too careful. My body keeps checking the foot the way someone checks a door they already locked."
    "{i}Pain? No. Tightness? Maybe. Paranoia? Abundant.{/i}"
    "By the first curve, the caution starts loosening."
    "{i}Breath in. Breath out. Arms relaxed. Eyes forward.{/i}"
    "The track stops being a question and turns back into a shape."
    show track_coach at thide
    hide track_coach
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Warmups become drills. Drills become the particular humiliation of dynamic stretching in public."
    nier "High knees, skips, lunges, and leg swings that make everyone look like they're negotiating with invisible furniture."
    nier "Coach watches with the attention of a man who believes bad form is a moral failing."
    call nier_clear from _call_nier_clear_0521_3
    scene bg track_day
    $ show_calendar()
    show mood_afternoon zorder 3 
    with wipeleft_scene
    "The first stride starts at the curve."
    "Seventy percent sounds gentle until your body remembers that percentages are lies invented by coaches to sell more practice."
    "I push off anyway."
    "For three seconds, I'm braced for the foot to complain."
    "For five, I'm braced for my lungs to give out."
    "By ten, I notice I'm moving faster than I meant to, and nothing has gone wrong yet."
    "{i}Oh.{/i}"
    "{i}So the body remembered. It just didn't bother telling me first.{/i}"
    "I coast down before the end of the straightaway and walk out onto the grass, hands on my hips."
    "My breath is rough, but not wrecked. My foot is present, but not angry."
    track_coach "Again."
    mc "Was that a good again or a criminal sentencing again?"
    track_coach "Again without commentary, [player]."
    mc "...Got it."
    "A couple of nearby runners snicker and coach points to the curve."
    track_coach "Seventy percent."
    mc "That WAS seventy!"
    track_coach "That was closer to eighty."
    mc "Hey, I don't know math, okay?"
    track_coach "Then use your lungs. Play it by ear instead of metric."
    "I walk back to the start."
    "{i}Fair enough. My lungs are giving me plenty to go on.{/i}"
    "The second stride feels better because I stop waiting for disaster to RSVP."
    "The third feels worse because confidence is an idiot and tries to add speed."
    track_coach "Easy now..."
    "The words snap me back before I do something impressively stupid."
    "I pull off the pace and let the final meters roll under me."
    "{i}Right. Light practice. Not auditioning for a comeback montage.{/i}"
    "{i}...Yet.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Practice settles into restraint, which is arguably much harder than effort."
    nier "Coach lets me run enough to remember I can, then stops me before I can turn remembering into evidence of poor judgment."
    nier "The rest is cooldown laps, stretching, and watching the main group start intervals that I would normally be part of."
    call nier_clear from _call_nier_clear_0521_4
    scene bg track_day
    $ show_calendar()
    show mood_evening zorder 3 
    with wipeleft_scene
    "By the time practice breaks, the afternoon has softened around the edges."
    "I sit on the grass near my bag and tug at one shoelace until it gives."
    "Sweat cools at the back of my neck. My legs feel used, but not nearly destroyed."
    "{i}Honestly? Better than I expected.{/i}"
    show track_coach neut at t11
    track_coach "How's the foot?"
    mc "Still attached."
    track_coach "You know what I mean, [player]."
    mc "A little tight. Not painful, but kinda ever-so-slightly annoying."
    track_coach "Good. Ice it tonight if it starts talking. Friday, you tell me before practice if it changes."
    mc "Got it."
    track_coach "And study, though I don't need to be the one to tell you that."
    mc "...For track?"
    track_coach "For midterms, smartass."
    track_coach "Academic eligibility does not care how poetic your excuses are."
    mc "...I swear, every department hounds me these days..."
    track_coach "Good. People gotta keep you on your toes."
    show track_coach at thide
    hide track_coach
    "He walks off before I can decide whether that was encouragement or a threat."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I leave school tired in a cleaner way than yesterday."
    nier "The walk to the station is slower than usual, but not pathetic enough to count as a medical event."
    nier "My bag thumps against my hip, my clothes faintly like rubber, and the evening has the nerve to look peaceful while my calves begin drafting tomorrow's complaint."
    call nier_clear from _call_nier_clear_0521_5
    scene bg kitchen
    $ show_calendar()
    show mood_home zorder 3 
    stop music fadeout 1.0
    with wipeleft_scene
    play music dailyleisure
    "Dinner becomes spaghetti because we are long overdue for a grocery haul."
    "Nonetheless, it simply exists as noodles, sauce, and the possibility of making too much, which I end up doing for some reason."
    "This is not a bug; it's a feature...or something."
    "A pot boils on the stove while sauce warms in the pan with garlic, onion, and the last respectable bell pepper in the fridge."
    "My shins are starting to remember practice."
    show asahina neut at t11
    ah "Why does it smell like you tried?"
    
    mc "Because I am a provider, thank you very much."
    ah "You're putting noodles in water."
    mc "Okay, and? If you have a witty remark, just say it."
    "She leans around me to inspect the pan."
    ah "Did you put vegetables in it?"
    mc "Yeah."
    ah "...You're actually a villain."
    mc "And you're not a little kid, ya spaz. Also, aren't you an athlete? Don't you need a well-balanced diet?"
    
    ah "Yeah, but you threw the whole Amazon in there! Where's the sauce?!"
    
    "My phone buzzes on the counter before the argument can become constitutional."
    "The screen lights up with mom's name."
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
    "I set the phone down and hope Asahina doesn't get any ideas."
    "The house is quieter than it should be at this hour. Mom's the one who fills the kitchen with noise -- the radio, the running commentary, the pot lid she never quite sets back on straight."
    "Without her, dinner is just two people and a pot."
    ah "Late again?"
    mc "Yeah. She says it should lighten up after a couple days if the schedule behaves."
    ah "Yeah, sure, schedules behave on their own."
    mc "Spoken like someone who doesn't."
    ah "Wow. Wowwww. Are you seriously slandering me?"
    
    mc "Not slander if it's the truth."
    ah "...I'm telling your three girlfriends that you bully me."
    "She grabs two plates from the cabinet."
    "For all the noise she makes about independence, she still sets three places at the table by default."
    "One plate for me. One for her. One for mom, covered and waiting."
    show asahina at thide
    hide asahina
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Dinner is mostly successful."
    nier "The sauce is not too watery, the noodles are only slightly past the point where an Italian would start preparing legal action, and Asahina eats her veggies after enough theatrical suffering to make the kitchen table feel like a stage."
    call nier_clear from _call_nier_clear_0521_6
    scene bg kitchen
    $ show_calendar()
    show mood_home zorder 3 
    show asahina neut at t11
    with wipeleft_scene
    "Asahina twists spaghetti around her fork with the grim concentration of someone defusing a bomb."
    ah "So track didn't kill you."
    mc "True, but I probably flailed like a maniac."
    
    ah "That means you looked stupid."
    
    mc "...That means Coach stopped me before I made poor decisions, which, to be fair, I almost broke out into tempo pace."
    ah "Rare adult W."
    "She takes another bite, then points her fork at me."
    ah "...Rooftop girl was kinda cool."
    mc "Tsubaki?"
    ah "Yeah."
    ah "She looked like she wanted permission to sit down in an open area."
    mc "That is...weirdly accurate."
    ah "I have eyes, you know."
    mc "Pfft, debatable."
    # CRITIQUE (ADDRESSED): Swapped the boiling-water threat for a non-violent, messier one (wearing the spaghetti). With the script tracking food/body stress and family safety, a casual scalding joke read harsher than the sibling rhythm supports; the pun chain survives intact.
    ah "Keep talking and you're wearing the rest of the spaghetti!"

    mc "Sorry, already strained and down the drain."

    ah "I'll make more. I've got noodles and a grudge."

    "That is not a threat worth testing."
    mc "She's Matsuda's friend, and, like she said, the other girl I met the other night."
    ah "Yeah, I got that."
    ah "That must be exhausting, honestly."
    "I think of Tsubaki saying Matsuda was worried for almost seven minutes."
    "Then I think of Matsuda stopping mid-performance in the hallway because I asked her to."
    mc "Probably."
    mc "But I think they mean well for each other, seeing as how they both claim they're besties."
    ah "That doesn't automatically make things untiring. I have a couple friends that drain my whole social battery, so..."
    "For once, I don't have a smart answer ready."
    "{i}Huh.{/i}"
    "{i}Look at Asa, accidentally saying something with weight.{/i}"
    mc "...Yeah, I guess it doesn't."
    "She looks at me for a second, then very deliberately ruins the moment by stealing a noodle from my plate."
    mc "Hey!"
    ah "Sister tax."
    mc "For...?"
    
    ah "Making me eat LITERALLY my least favorite vegetable."
    
    mc "...This government is corrupt."
    ah "Sounds like a you problem~"
    "She leans back with the satisfaction of someone who believes the final word is a human right."
    show asahina at thide
    hide asahina
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "After dinner, I clean the kitchen because leaving sauce to dry on a pan is how civilizations decline."
    nier "Asahina helps by standing nearby and offering commentary, which she claims is emotional support."
    nier "Mom's plate goes into the fridge with a note on top."
    call nier_clear from _call_nier_clear_0521_7
    scene bg bedroom
    $ show_calendar()
    show mood_night zorder 3 
    stop music fadeout 1.0
    with wipeleft_scene
    play music fantasyserenity
    "Night finds me at my desk with one notebook open, one leg stretched under the chair, and one ice pack balanced near my ankle like a tiny medical accusation."
    "The foot itself is fine, though everything around it has decided to develop opinions."
    "I finish half a page of chemistry notes and one matrix problem before my phone starts buzzing."
    "{i}Why am I not surprised it's you?{/i}"
    call phone_call("Monika", status="Incoming Call", can_decline=False) from _call_phone_call_0521_1
    # CRITIQUE (ADDRESSED): Cut the second-best bit (the salad debate) to get to the emotional point -- Monika quietly working to make MC sound less tired -- sooner. Kept the cup conspiracy because it calls back to the day's omitted-agency lesson and carries the "you undersell yourself" beat. Also fixed the "for"→"For" cap and softened a crude aside.
    python:
        _phone_call_lines = [
            phone_call_line("me", "Welcome to Jake's pizzeria and crematorium, where yesterday's loss is today's sauce. How can I help?"),
            phone_call_line("them", "Wow...no hello?"),
            phone_call_line("me", "...Hello, this is Jake's pizzeria and crematorium."),
            phone_call_line("them", "Much better!"),
            phone_call_line("them", "So, you alive?"),
            phone_call_line("me", "Why wouldn't I be?"),
            phone_call_line("them", "Great news already. I was worried track practice might turn you into some sort of zombie."),
            phone_call_line("me", "I mean, I almost broke my own rules of light work."),
            phone_call_line("them", "'Least you're suffering responsibly, right?"),
            phone_call_line("me", "The best kind, allegedly."),
            phone_call_line("me", "Why are you calling, anyway?"),
            phone_call_line("them", "To check on you, duh doy~"),
            phone_call_line("me", "That's suspiciously direct."),
            phone_call_line("them", "What can I say? Studying's kicking my butt, so I need a distraction."),
            phone_call_line("me", "And there it is."),
            phone_call_line("them", "Hey, both things can be true, you know."),
            phone_call_line("me", "Can they, now?"),
            phone_call_line("them", "Obviously! For example, I am currently looking at my literature notes."),
            phone_call_line("me", "In the same way someone looks at a locked door?"),
            phone_call_line("them", "Exactly! Very observant, you are."),
            phone_call_line("me", "Did you also get the handout with the cup and the ominous door?"),
            phone_call_line("them", "Yep."),
            phone_call_line("them", "I decided the cup did it."),
            phone_call_line("me", "The cup, eh? Pray tell."),
            phone_call_line("them", "It had motive, or at least more of one than the door."),
            phone_call_line("me", "What motive could a cup possibly have?"),
            phone_call_line("them", "Well, there was that little blurb implying abandonment issues, so I'm leading with that."),
            phone_call_line("me", "...Did you call to just discuss our handouts?"),
            phone_call_line("them", "Nah, we're discussing literature."),
            phone_call_line("me", "...Literally the same thing, doofus."),
            phone_call_line("me", "You are figuratively accusing a cup of a petty crime."),
            phone_call_line("them", "You should read between the lines more, there's more evidence, I believe."),
            phone_call_line("me", "Name ONE."),
            phone_call_line("them", "It was left on the table. Boom. Case closed."),
            phone_call_line("me", "...Geography? That's your ace? You're better than this, Monika."),
            phone_call_line("them", "Geography can be emotional in some cases!"),
            phone_call_line("me", "Okay, fine, for the sake of the argument, the cup is lonely."),
            phone_call_line("them", "Thank you."),
            phone_call_line("me", "But the door is clearly the mastermind."),
            phone_call_line("them", "Oh?"),
            phone_call_line("me", "It was open when it should have been closed. Classic suspicious behavior."),
            phone_call_line("them", "So the door and the cup were working together, you argue..."),
            phone_call_line("me", "A domestic conspiracy."),
            phone_call_line("them", "That sounds like a title."),
            phone_call_line("me", "My mom's a lawyer--Hey! I heard that pen click! Don't make it a club pitch!"),
            phone_call_line("them", "Too late, jotting it down now~"),
            phone_call_line("me", "Monika!"),
            phone_call_line("them", "Chill! Working title only."),
            phone_call_line("me", "...Everything I say can and will be used against me."),
            phone_call_line("them", "You really undersell yourself. Seriously, you come up with some profound stuff sometimes!"),
            phone_call_line("me", "Only sometimes? Damn, I see how it is."),
            phone_call_line("them", "Hahahaha~"),
            phone_call_line("me", "Don't we have studying to wrap up? We've devolved into meaninglessness."),
            phone_call_line("them", "Good. That means it's working."),
            phone_call_line("me", "Working toward...what?"),
            phone_call_line("them", "You sounding less tired!"),
            phone_call_line("me", "...Sneaky."),
            phone_call_line("them", "A little, kinda, yeah, haha."),
            phone_call_line("me", "I mean, I still am, but...y'know."),
            phone_call_line("them", "True, but at least we have a back-and-forth going on."),
            phone_call_line("me", "Today was just full, alright?"),
            phone_call_line("them", "Track, studying... What else?"),
            phone_call_line("me", "Managing two goblins on the roof."),
            phone_call_line("them", "Huh?"),
            phone_call_line("me", "Asa found me at lunch, then another girl showed up. Tsubaki was her name."),
            phone_call_line("them", "Tsubaki Kareda?"),
            phone_call_line("me", "Yeah."),
            phone_call_line("them", "Huh. Interdasting..."),
            phone_call_line("me", "You...know her?"),
            phone_call_line("them", "Not well, but enough."),
            phone_call_line("them", "She's usually with that recent new girl, and I honestly can't get a read on their chemistry."),
            phone_call_line("me", "Yeah, that checks out...probably."),
            phone_call_line("them", "Was everything okay with her?"),
            phone_call_line("me", "Yeah. She was nice."),
            phone_call_line("me", "Nervous, which I guess she always is, but nice nonetheless."),
            phone_call_line("them", "That's a good thing."),
            phone_call_line("me", "Asa liked her, I think."),
            phone_call_line("them", "She always has had good taste in friends."),
            phone_call_line("me", "Yeah, but please don't encourage her. You have no idea..."),
            phone_call_line("them", "Sounds deep, so I won't ask."),
            phone_call_line("me", "Coward."),
            phone_call_line("them", "Still a valid tactic~"),
            phone_call_line("them", "*yawn* At any rate, turns out I'm the one dozing off. We should probably call it."),
            phone_call_line("me", "Yeah, probably."),
            phone_call_line("them", "Go ice your foot properly, track boy."),
            phone_call_line("me", "Call me that again, and your head's on a pike."),
            phone_call_line("them", "No promises~"),
            phone_call_line("me", "Goodnight, Monika."),
            phone_call_line("them", "Goodnight, " + player + "!"),
        ]
    call phone_call_conversation("Monika", _phone_call_lines, status="Connected") from _call_phone_call_conversation_0521_1
    "My room becomes quiet again, but not empty in the same way."
    "I set the phone facedown and look at the half-finished notes on my desk."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The rest of the night is quiet."
    nier "Mom gets home late enough that I only hear the careful movement of cabinet doors and the microwave starting downstairs."
    nier "I fall asleep before I can ask whether the spaghetti survived cross-examination."
    call nier_clear from _call_nier_clear_0521_8
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0521_1
    jump a0522
