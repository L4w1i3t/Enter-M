init python:

    # Six intentional lines. MC's "It's only six lines" and Monika's "maybe
    # that's why it works" both depend on that count being literally true on
    # screen, so do not add a line here without changing the dialogue.
    poem_0524_mc_draft = Poem(
        author="mc",
        title="Window Seat (Draft)",
        text="""\
On the bus, the window turns the city
into a strip of things I am allowed to leave behind.

The seat remembers nobody.
No one asks the reflection whether it is doing well.

It only carries my face
until the glass gets too dark to give it back."""
    )

    # Three revised versions. The player picks the closing image at the club
    # scene; whichever they choose is the draft from then on. The bus ride home
    # that evening echoes it; s1_poem_echo keeps a quotable fragment for a later
    # callback (nothing quotes it yet).
    poem_0524_mc_revised_vinyl = Poem(
        author="mc",
        title="Window Seat (Draft)",
        text="""\
On the bus, the window turns the city
into a strip of things I am allowed to leave behind.

The seat remembers nobody.
No one asks the reflection whether it is doing well.

It only carries my face
until the glass gets too dark to give it back.

The vinyl keeps the shape of my leg for three stops
and lets go without comment."""
    )

    poem_0524_mc_revised_warmth = Poem(
        author="mc",
        title="Window Seat (Draft)",
        text="""\
On the bus, the window turns the city
into a strip of things I am allowed to leave behind.

The seat remembers nobody.
No one asks the reflection whether it is doing well.

It only carries my face
until the glass gets too dark to give it back.

It gives back exactly the warmth I left in it
and not one degree more."""
    )

    poem_0524_mc_revised_spring = Poem(
        author="mc",
        title="Window Seat (Draft)",
        text="""\
On the bus, the window turns the city
into a strip of things I am allowed to leave behind.

The seat remembers nobody.
No one asks the reflection whether it is doing well.

It only carries my face
until the glass gets too dark to give it back.

There is a spring under the left side
that counts every stop with me."""
    )

    poem_0524_monika = Poem(
        author="monika",
        title="Table Near the Window",
        text="""\
A review sheet lies open between two cups.

One cup is mine
because lipstick makes ownership legible.
The other is his
because he keeps turning it by the rim
when he does not know where to put a thought.

Outside, buses practice leaving.
Inside, I underline the same sentence twice
so my hands have work.
It's all I know to do.

Pressure changes shape
when someone stays long enough
to quiz you on the hard parts."""
    )


label a0524:
    # --- Day 10: 2025-05-24 ---
    pause 2.0
    scene bg schoolgym
    $ show_calendar()
    $ atmos("morning")
    with dissolve_scene_full
    play music school_day_a
    "The gym smells like floor wax and several hundred people who would rather still be in bed. We've been lined up by year and class, and the lines stay straight right up until a teacher looks away."
    "{i}Morning pep assembly.{/i}"
    "{i}Because when a school says midterms begin Monday, apparently the next step is forced enthusiasm under fluorescent lighting.{/i}"
    "Somewhere near the front, a microphone pops."
    principal "Good morning, students of Itsuki Academy."
    "The speakers answer with a squeal of feedback that makes half the gym flinch. Nobody looks any more encouraged afterward."
    principal "As you know, midterm exams begin after the weekend. Preparation, discipline, and mutual encouragement are the foundations of student success."
    "While he shuffles his notes, Asahina ditches the first-years and slips back to stand with me, right in front of Sam's row."
    show asahina uniform neut at t21
    show sam uniform neut at t22
    "Sam leans over the gap and straightens a fold in her cuff. His hand is back at his side by the time she checks it."
    show asahina uniform embarrassed
    "She faces the stage again, rubbing the cuff between two fingers."
    ah "...Thanks."
    sa "Anytime."
    "I lean back, keeping my voice under the principal's."
    mc "Fix mine while you're there?"
    show asahina uniform annoyed
    ah "Fix it yourself, damn!"
    show sam uniform teasing
    sa "You missed a button too, bud."
    show asahina uniform unamused
    ah "Don't help him! I want to see how long it takes."
    show asahina uniform happy
    show sam uniform happy
    "So of course I check, one button at a time, in front of the entire third year, while Sam's grin gets wider with every one. All present and accounted for."
    show sam uniform pose_crossed
    principal "You are not merely taking tests. You are proving the discipline you have built all term, or for some of you, all of high school so far."
    "Down our row, a guy mutters that the only thing he's built all term is a grudge against half his classes."
    "{i}At least I respect the honesty.{/i}"
    "The speech keeps going."
    "Goals and community lead into study habits, and sleep and hydration bring up the rear."
    "Coach is posted by the wall with his arms folded for all of it. I'd bet money he's underlining the sleep part."
    show sam uniform neut
    "Behind me, Sam leans in until his voice is just over my shoulder, pitched under the speech."
    if s1_was("sam_lunch", "sideways"):
        show sam uniform teasing
        sa "So. Did Tuesday's question count, in the end?"
        mc "Ruling's still pending."
    elif s1_was("sam_lunch", "wait"):
        show sam uniform happy
        sa "Y'know, you're a really good listener. Good to know for next time."
        mc "I was eating."
    else:
        sa "Hey. Thanks for Tuesday, by the way. For actually answering."
        mc "It was one question."
    show sam uniform neut
    "A projector screen at the side of the stage puts up a slogan in clean blue letters:"
    "{b}YOUR EFFORT TODAY BECOMES TOMORROW'S CONFIDENCE.{/b}"
    "{i}My confidence tomorrow will be a half-dead ballpoint pen and an empty cracker jack box.{/i}"
    "Eventually a student council rep steps up to thank everyone for their attention."
    "The room has offered very little proof of any."
    # SFX SUGGESTION: A microphone cutoff pop, followed by the gym crowd swelling back in.
    "The microphone clicks off, and the gym exhales in one enormous wave of adolescent morning breath."
    "Nobody's been dismissed yet, but every row is already leaning toward the doors, daring the others to start the traffic jam."
    "Our class is the last to leave, because of course it is."
    "By the time we're released, the first-years are long gone and the last of the second-years are filing past the end of our row."
    mc "...Asa, your class left without you."
    ah smug "And? Nobody's gonna notice. I went to the bathroom, or something."
    show asahina uniform happy at t31
    show sam uniform neut at t32
    "She spots someone near the back of the passing line and throws a hand up."
    ah "Tsubaki!"
    show tsubaki uniform nervous at t33
    "Tsubaki steps out of the traffic and over to our row, hugging a notebook to her chest."
    show tsubaki uniform happy
    ts "Hi, Asahina. Hi, [player]."
    mc "Morning."
    if dep_took("tsubaki_assignments"):
        ts "Oh--and thank you for last night! I sent the picture and then I actually slept. Like, all night."
        mc "Sounds like the trial was a success."
        "Her laugh comes out muffled by the notebook."
    else:
        show tsubaki uniform embarrassed
        "She tips the notebook open from the back, just far enough to show a fresh check mark beside the word {i}Friday{/i}."
        ts "I did the check last night. It was pretty late, but it still counts as Friday if you haven't gone to bed yet."
        show asahina uniform smug
        ah "See?! Told you it works. You're welcome~"
    show tsubaki uniform curious
    "Tsubaki's eyes go to Sam once and come straight back."
    show asahina uniform nervous
    ah "Tsubaki, Sam. Sam, Tsubaki. This guy's my--"
    show sam uniform smug
    sa "Boyfriend."
    ah "...Yeah. That."
    show tsubaki uniform neut
    "Tsubaki's arms tighten around the notebook, only a little."
    show tsubaki uniform nervous
    ts "Oh! Right. Nice to meet you."
    show sam uniform neut
    sa "Masayami Inugami. Sam, though, unless you're a teacher."
    show tsubaki uniform neut
    ts "Tsubaki Kareda."
    "She dips her head politely, and the loose sheet tucked inside her notebook picks that moment to slide out. Sam catches it an inch off the floor."
    sa "Got it."
    show tsubaki uniform embarrassed
    ts "Ah--thank you!"
    "He hands it back, eyes carefully anywhere but the writing."
    show sam uniform curious
    sa "Wait, you're the one who liked the poster?"
    show tsubaki uniform curious
    ts "Asahina's?"
    sa "Yeah. She said somebody finally gave her useful feedback on it."
    show asahina uniform shocked
    "My sister's head snaps toward him."
    ah "Okay, you don't have to tell her {i}everything{/i} I said."
    show sam uniform teasing
    sa "You said, and I quote, 'she understood the motion lines, which means she has functioning eyes and taste.'"
    show asahina uniform embarrassed
    # NUDGE KEEP: "That was private." Keep it when you trim this scene.
    ah "I was talking to you! That was private."
    mc "So you liked the compliment. Good to--"
    ah "Finish that sentence and see what happens."
    show tsubaki uniform embarrassed
    "Tsubaki suddenly gets very interested in the rescued sheet of paper."
    ts "It was {i}just{/i} a nice poster."
    show sam uniform happy
    sa "Well, she was stoked. Pointed it out to me twice on the way to class."
    show tsubaki uniform nervous
    "Tsubaki's smile starts, then ducks behind a quick nod."
    ts "Thanks..."
    # SFX SUGGESTION: Two sharp handclaps with a short gymnasium echo.
    "A teacher claps twice near the doorway."
    teacher "Second-years, keep moving!"
    show tsubaki uniform worried
    ts "Oh, that's us. I should go."
    show asahina uniform teasing
    ah "Go, go, before the path seals forever! Second-years get, like, ninety seconds."
    show tsubaki uniform teasing
    ts "I'm going! Save me some shade at lunch."
    show sam uniform neut
    sa "Later, Kareda."
    show tsubaki uniform shocked
    # NUDGE KEEP: Tsubaki's half-beat.
    "Her step catches by half a beat before she rejoins her class."
    show tsubaki at thide
    hide tsubaki
    show asahina uniform neut at t21
    show sam uniform neut at t22
    ah "...She's nice."
    mc "You said that on Wednesday."
    show asahina uniform unamused
    ah "So? Being nice isn't a limited-time offer, genius."
    show sam uniform thinking
    sa "Hope we didn't get her in trouble. Her teacher looked kinda ticked."
    show asahina uniform neut
    "Asahina keeps watching the doorway until the crowd behind us starts to push."
    mc "Okay, we should move, unless we live here now."
    show asahina uniform teasing
    ah "Then move your bag! I can't get past you."
    show sam uniform smug
    sa "Go on. See you after class."
    "We let the crowd carry us out, and the smell of floor wax follows us most of the way to homeroom."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Every class after homeroom hands out one more review packet, and by third period my binder has given up on closing. I move the biology sheets to the back and hope I remember doing it."
    call nier_clear from _call_nier_clear_0524_1
    stop music fadeout 1.0
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music day_a
    "Lunch comes so late that the morning already feels borrowed."
    show asahina uniform neut at t11
    "Asahina finds me by the stairwell, one thumb busy on her phone."
    ah "Roof?"
    mc "Wow. You've really streamlined the invitation process."
    show asahina uniform unamused
    ah "Roof, {i}please{/i}."
    mc "That revision really sold it."
    "She checks down the hall once."
    mc "No Sam?"
    show asahina uniform neut
    ah "He's playing basketball with some guys from his class. He'll text me after."
    mc "And you don't want to go watch?"
    show asahina uniform smug
    ah "I stood around in a gym all morning. I'm good."
    mc "Can't argue with that."
    show asahina uniform frustrated
    ah "Roofornoroof?!"
    mc "Roof."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg rooftop
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play sound moddooropen
    "The breeze finds the sweat under my collar the second we're through the rooftop door. From up here, you can hear the basketball game through the gym windows."
    show asahina uniform happy at t11
    "Asahina has barely got her lunch open when her phone lights up, so she props it against her bag and reads while she eats."
    mc "Subtle."
    ah "I'm checking the time."
    mc "And smiling at it?"
    ah "I can smile, dude. Last I checked, it's free."
    show asahina uniform embarrassed
    "She aims her chopsticks at me, eyes still on the screen and ears going faintly pink."
    ah "Eat your food, slowbrain. You've been holding the same bite for a whole minute."
    "I obey, on the grounds that I'm too hungry to press it."
    "We eat while somebody down in the gym argues about a foul, and eventually her phone goes facedown in her lap."
    show asahina uniform worried
    ah "Do you think Tsubaki was okay earlier? After she met Sam, I mean."
    mc "In the gym?"
    show asahina uniform pose_eyeroll
    ah "No, in the middle of the ocean. Yes, in the gym, dumbass."
    mc "She nearly dropped a page. I was watching that."
    show asahina uniform unamused
    ah "Yeah. She acted like Sam handed her an award, and it was {i}one{/i} compliment."
    ah "I hope we didn't embarrass her, going on about the poster like that."
    mc "You jelly?"
    show asahina uniform angry
    "Her head turns very slowly."
    ah "I'll kill you."
    mc "Okay, okay..."
    "I put both hands up, and she decides to let me live."
    show asahina uniform neut
    "She aims the next part at the skyline instead of me."
    ah "She was happy for, like, a second, and then everybody was staring at her."
    ah "I hate when people do that to me."
    mc "She found out somebody liked her feedback. As public humiliations go, that's a pretty mild one."
    show asahina uniform thinking
    ah "Fine. Next time I'll just say hi without announcing it to the whole gym."
    mc "On behalf of the gym, thank you."
    "She answers with a mouthful of rice, and for a while the roof asks nothing of us but lunch."
    show asahina uniform neut
    ah "I can do normal, y'know."
    mc "I'll try not to sound too surprised when it happens."
    "She bumps her shoe against mine and goes back to eating."
    "With her busy, I check my own phone. Matsuda's thread hasn't moved since last night."
    "A few bites later, it buzzes against my knee."
    "{i}Ah, right on time. Regularly scheduled contact.{/i}"
    python:
        _phone_messages = [
            phone_msg("them", "Where are you having lunch?"),
            phone_msg("them", "I tried the club room, but it's a ghost town."),
            phone_msg("me", "Roof. Asa pulled rank."),
            phone_msg("them", "Kidnapped?! Should I notify someone?"),
            phone_msg("me", "Nah, she has snacks. Negotiations are stable."),
            phone_msg("them", "Good! Can you stay put for a few minutes? There's something I wanted to ask you before afternoon classes."),
            phone_msg("me", "Sure. Door's unlocked. Probably."),
            phone_msg("them", "Yay!"),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0524_1
    show asahina uniform curious
    ah "Monika?"
    mc "Yeah."
    show asahina uniform smug
    ah "She's coming up here?"
    mc "She wants to ask me something."
    show asahina uniform teasing
    ah "Uh-huh."
    mc "That's literally all I know, so don't gimme that."
    ah "Uh-huuuh..."
    mc "You've got rice on your chin."
    "She wipes the wrong side, then catches my grin."
    show asahina uniform annoyed
    ah "Asshole."
    play sound moddooropen
    "She's still scrubbing at her chin when the door opens."
    show asahina uniform neut at t21
    show monika forward uniform neut cm oe nobl rdown ldown at t22
    "Monika steps out with a folder hugged to her chest, and the wind goes straight for the loose ribbon of her bow."
    m forward uniform happ om oe nobl rdown ldown "Found you!"
    mc "Present."
    m forward uniform happ cm oe nobl rdown ldown "Hi, Asahina!"
    ah "Yo."
    m forward uniform wry om oe nobl rdown ldown "Sorry to crash whatever this was."
    "Asahina looks from the folder to the fingers tightening around its edge."
    show asahina uniform neut
    ah "You're not. I was done eating anyway. Mostly done, which counts."
    mc "Since when?"
    show asahina uniform teasing
    ah "Since now. I'm gonna go catch Sam before he heads back to class."
    m forward uniform nerv om oe awkw rdown ldown "Oh, you don't have to leave on my account!"
    show asahina uniform smug
    ah "I know. He'll be done playing by now."
    show asahina uniform neut
    "She closes her lunch bag and gets up at her own pace, with one look along the shaded wall before she goes."
    ah "If Tsubaki comes up, tell her I'll see her Monday."
    mc "Will do."
    ah "Later, nerds."
    m "Bye, Asahina!"
    show asahina at thide
    hide asahina
    play sound moddoorclose
    "The door clangs shut behind her, and the roof gets a lot quieter."
    show monika forward uniform nerv cm oe awkw rdown ldown at t11
    "Monika stays standing, working her thumb against the corner of the folder."
    mc "You alright?"
    m forward uniform nerv om oe awkw rhip ldown "Yeah! I've just been meaning to ask you something, and we keep being in a hurry."
    mc "You say that like I shouldn't be concerned."
    "She laughs once, soft and unfinished."
    m forward uniform neut cm oe nobl rhip ldown "Tomorrow's our last full study day before exams."
    m "I know you probably already have a plan, and I know your science and math stuff is more... you know."
    mc "Full of diagrams nobody wants to look at?"
    m forward uniform nerv om ce blaw rdown ldown "...I was going to say STEM-oriented."
    mc "...That too."
    m forward uniform happ cm ce nobl rdown ldown "I'm a very diplomatic person."
    "She sits down next to me, leaving a gap about as wide as her folder."
    m forward uniform nerv om oe blus rhip ldown "So I was thinking we could meet at the public library in the morning? Study for a few hours, trade notes, maybe quiz each other?"
    m "We can split the language arts and civics work, and I really need someone to check my algebra. I won't be much use on your science papers, though."
    mc "That's ambitious."
    m forward uniform nerv om oe blus rdown ldown "And after that, if we survive, there's that new cafe downtown in the historic district? The one with the green awning, by the old bank?"
    "She studies the folder, where the corner of a printed review sheet is poking out."
    m forward uniform flus cm oe blus rdown ldown "I thought lunch there might be nice."
    "{i}Ah.{/i}"
    m forward uniform nerv om oe awkw rdown ldown "Not as, like, a big thing, just... exams are coming up, track is back, you have college stuff probably, and your family, and--"
    "She cuts herself off."
    "Her grip on the folder eases, and I lean in for whatever comes next."
    m forward uniform flus cm oe blus rdown ldown "I {i}missed{/i} this."
    m "Having somewhere to go with you that isn't the club room, I mean."
    if s1_was("movie_goodbye", "linger"):
        m forward uniform flus cm oe blus rdown ldown "Sunday was fun. And, um, what I said outside the theater? That still stands."
        "{i}There wasn't a somebody else.{/i}"
        mc "I know. It was a good day."
    elif s1_was("movie_goodbye", "joke"):
        m forward uniform nerv om oe blus rdown ldown "Sunday was fun. Even the horror committee approved, and you know how corrupt they are."
        mc "I hear they take bribes in churro popcorn."
    else:
        m forward uniform neut cm oe blus rdown ldown "Sunday was fun."
        mc "Yeah, it was. I'd do it again."
    m forward uniform nerv om oe blus rdown ldown "I want to do things like that more often. We always wait until we both happen to be free."
    m "We've been friends for a whole year! Two reasonably organized people can surely make a plan on purpose every once in a while."
    m "And I really want to try that cafe while it still has the opening-week menu."
    "Past the fence, the city goes on minding its own business."
    mc "Yeah, let's go. I'd want to even without the opening-week menu."
    "She looks up."
    m forward uniform vsur om oe nobl rdown ldown "Really?"
    mc "Seriously. Library in the morning, then we put the notes away and eat something."
    "Her shoulders come down an inch."
    m forward uniform happ cm ce nobl rdown ldown "Okay. I'll try not to bring the entire desk."
    mc "Leave the stapler. We'll cope somehow."
    m forward uniform laug cm ce nobl rdown ldown "Thank ya, thank ya."
    m forward uniform happ cm oe nobl rhip ldown "I'll send you the time tonight."
    mc "No need. I can just meet you there at, like, nine."
    m forward uniform happ om oe nobl rdown lpoint "Yeah, nine works! Don't make me text five reminders."
    mc "I would never."
    m forward uniform wry cm ce nobl rdown ldown "You absolutely would, by needing them."
    mc "I've got four alarms now. Three of them are Asa's fault."
    # SFX SUGGESTION: A distant warning bell that gently breaks the rooftop quiet.
    "The warning bell goes off somewhere below us, and Monika gets to her feet while I fold up the last of my lunch."
    m forward uniform happ om oe nobl rdown ldown "Okay! Back we go. I'd rather not get written up as a runaway twice in one term."
    mc "That seems reasonable."
    m "I manage it occasionally."
    "She stops by the door."
    m forward uniform nerv om oe awkw rdown ldown "Thanks."
    mc "For... saying yes?"
    m forward uniform neut cm oe blus rdown ldown "For saying you want to. I was starting to feel stupid asking."
    "I take the door from her so she can get through with the folder."
    mc "...Yeah. No problem."
    show monika at thide
    hide monika
    play sound moddoorclose
    "I'm not sure what was so hard about asking. Still, nine is settled, and the bell isn't going to wait while I work it out."
    $ update_character_thought("monika", "Library at nine tomorrow, then lunch with Monika at the cafe near the old bank. She wants us to make plans more often.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Chemistry hands back our practice work and walks us through every mistake on it. By algebra, the extra sheets have gone into a binder pocket that's already splitting at the corner."
    nier "Foreign language adds one last vocabulary sheet to the pile before the final bell lets us go. I wait in my seat for the doorway to clear, then head for club."
    call nier_clear from _call_nier_clear_0524_3
    stop music fadeout 1.0
    pause 2.0
    scene bg club_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music day_c
    "A few members have already dragged their chairs into the sunny corners of the club room and gone quiet over open notebooks. Nobody so much as lifts their head when I come in."
    show monika forward uniform neut cm oe nobl rdown ldown at t11
    "Monika is at the board, chalking up today's prompt in clean letters: {i}Write about a place that holds still while you don't.{/i}"
    m forward uniform happ om oe nobl rdown ldown "Oh, hey! Perfect timing."
    mc "Hey."
    "I drop into my usual seat and get my notebook out. There's a tiny nick in the corner of the desk, and my thumb finds it before my brain does."
    "It catches my nail, and I put my hand back on the notebook."
    m forward uniform happ cm oe nobl rhip ldown "I figured we could keep it low pressure today, because everyone in here is running on fumes and I would like them back on Monday."
    m forward uniform happ om oe nobl rhip lpoint "Fifteen minutes to draft, then trade if you want! Old drafts are fair game too, so nobody has to start from scratch."
    "The room settles into writing. For a while, there's nothing but paper noise."
    "Someone near the back erases until the page wrinkles, then crosses out exactly three words and keeps going."
    "I go back to Tuesday's unfinished bus poem and reread the brackets I used to dodge the last line. This time, I start on a clean page."
    call enter_m_showpoem(poem_0524_mc_draft) from _call_enter_m_showpoem_0524_1
    "{i}Not exactly the cheerful version of exam-week pressure, then.{/i}"
    m forward uniform curi om oe nobl rhip ldown "You stopped..."
    mc "I'm deciding whether I like the last line."
    m forward uniform happ cm ce nobl rhip ldown "Want me to look?"
    mc "Give me until the timer. I'll make it worse first."
    # SFX SUGGESTION: A short, neutral timer buzz from Monika's phone.
    "When the timer on her phone buzzes, Monika brings her notebook over, and I close mine on the page until she gets here."
    show monika forward uniform happ cm oe nobl rdown ldown at t11
    m forward uniform happ om oe nobl rdown ldown "Trade?"
    mc "As always."
    "We swap with very little ceremony. Her handwriting is neater than mine even in a draft, and she's crossed out her title and written a smaller one underneath."
    call enter_m_showpoem(poem_0524_monika) from _call_enter_m_showpoem_0524_2
    "I make it as far as the two cups and stop there. Across the desk, Monika is taking her time with my six lines."
    "{i}Okay. Say something about it.{/i}"
    mc "This is..."
    "Her eyes lift."
    m forward uniform worr om oe nobl rdown ldown "Too much?"
    mc "No! No, it's {i}good{/i}."
    mc "I just didn't know I turned the cup like that. Do I really do it that much?"
    m forward uniform happ cm oe nobl rhip ldown "Only when you're thinking. Sometimes I wait to see if you'll spill it."
    "She grins, then goes back to my notebook instead of her own."
    m forward uniform happ om oe nobl rdown ldown "Yours is good too, you know."
    "She reads it once more, slower, and her finger stops by the margin where, on any other draft of mine, there would be a bracket."
    "This time there isn't one."
    m forward uniform happ om oe nobl rdown lpoint "Huh. No 'annotations' this time."
    mc "...Didn't need them."
    mc "It's only six lines, though."
    m forward uniform happ cm oe nobl rhip ldown "Maybe that's why it works! Not every poem needs to be an epic."
    m forward uniform neut om oe nobl rdown ldown "But the line about the seat remembering nobody? That one's really strong."
    m forward uniform curi om oe nobl rdown lpoint "I wanted to stay on the bus a little longer when I got to the end."
    m "If it were mine, I'd add one more image after those last two lines. Not an explanation, just... something you'd see."
    m "What would you notice if you stayed on for one more stop?"
    mc "Wow. Feedback {i}and{/i} homework."
    m forward uniform happ cm oe nobl rhip lpoint "One image! You can always cross it out."
    "I pull the notebook back and think about the seat."
    menu:
        "\"The vinyl keeps the shape of my leg for three stops.\"":
            $ s1_pick_poem("vinyl")
        "\"It gives back exactly the warmth I left in it.\"":
            $ s1_pick_poem("warmth")
        "\"There's a spring under the left side that counts the stops.\"":
            $ s1_pick_poem("spring")
    "I write it under the last line:"
    if s1_was("poem_revision", "warmth"):
        call enter_m_showpoem(poem_0524_mc_revised_warmth) from _call_enter_m_showpoem_0524_3b
    elif s1_was("poem_revision", "spring"):
        call enter_m_showpoem(poem_0524_mc_revised_spring) from _call_enter_m_showpoem_0524_3c
    else:
        call enter_m_showpoem(poem_0524_mc_revised_vinyl) from _call_enter_m_showpoem_0524_3
    "She reads over my shoulder while I check that the new line hasn't made the old ending redundant."
    m forward uniform happ cm ce blus rdown ldown "There."
    "Her fingertip stays beside the new line, and she doesn't reach for another correction."
    mc "Yeah?"
    m "...Yeah."
    "Monika caps her pen and draws her hand back. The page stays between us."
    hikari "Monika? You said you'd look at mine. Like, ten minutes ago."
    m forward uniform flus om oe blaw rdown ldown "Oh! Yes! Sorry, I lost track of time."
    "She reaches for her notebook, but I've still got hold of the corner."
    mc "Can I read it again later?"
    m forward uniform happ cm oe blus rdown ldown "You can take a picture."
    "So I do, while she waits beside the desk, and then she takes her pen over to Hikari."
    "For the next half hour, club actually becomes club. Some people trade drafts, and some keep writing alone."
    "While Monika works through Hikari's draft, I read the photo again, tilting the screen away from the sun."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "As people start packing up, I copy the new ending onto a clean page and leave the crossed-out version where it is."
    call nier_clear from _call_nier_clear_0524_4
    pause 2.0
    scene bg club_day
    $ show_calendar()
    $ atmos("evening")
    show monika forward uniform dist cm oe nobl rdown ldown at t11
    with wipeleft_scene
    "The room is almost empty by the time Monika stacks the last loose paper."
    m forward uniform wry om oe nobl rdown ldown "I'd like to get out of here before someone hands me another draft. Did you finish?"
    mc "Yeah. I copied it out."
    m forward uniform neut om oe nobl rdown ldown "Good. I want to read the clean copy tomorrow."
    mc "Only if you bring yours."
    m forward uniform happ om oe blus rdown ldown "Deal. Mine too."
    "She slides her notebook into her bag and squares the zipper with both hands."
    m forward uniform nerv om oe blus rhip ldown "Anyway! Tomorrow at nine, then?"
    mc "Library at nine, then the green awning by the old bank."
    m forward uniform curi om oe nobl rdown ldown "Oh hey, you remembered~"
    mc "Oh, don't be like that. I have my moments."
    m forward uniform happ cm oe nobl rdown ldown "Yes, you do..."
    "Three plain words. I find something else to look at anyway."
    m forward uniform happ cm ce nobl rdown ldown "See you tomorrow, [player]!"
    mc "Catch ya later."
    show monika at thide
    hide monika
    pause 2.0
    mc "..."
    mc "Heh."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "On the bus, I slide the poem between two review sheets so it won't crease, then have to dig it back out when I remember I never signed it."
    # The closing image the player chose shows up on the ride home. Unremarked.
    if s1_was("poem_revision", "warmth"):
        nier "The only free seat is still warm from whoever just got off. Exactly that warm, and not one degree more. I sign my name on my knee and try not to think about it."
    elif s1_was("poem_revision", "spring"):
        nier "The seat I get has a spring loose under the left side, and it clicks at every stop like it's keeping count. I sign my name between two of them."
    else:
        nier "The seat I get is the cracked vinyl kind. By the third stop it's holding the shape of my leg, and when I shift to sign my name, it lets go without comment."
    call nier_clear from _call_nier_clear_0524_5
    stop music fadeout 1.0
    pause 2.0
    scene bg dining_table_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music house_day_a
    "Asahina has already eaten by the time I get home. She's upstairs laughing at something while Mom dishes out the curry, and whatever it is, it isn't homework."
    "That leaves the table to Mom and me, both of us a little too Saturday-tired for a full family debate."
    show mom curious at t11
    mom "So, how was the exam assembly?"
    mc "Mostly a nothingburger."
    mom "Oof. That bad?"
    mc "It went on forever. They could've put the whole thing in a notice and spared us the hydration segment."
    show mom teasing
    mom "Mm. An efficient use of your morning, then."
    mc "How'd your hearing go?"
    show mom neut
    mom "Continued."
    mc "Is that lawyer for 'good'?"
    show mom unamused
    mom "It's lawyer for 'June's problem.' Which makes it my problem until June."
    show mom thinking
    "She takes a sip of tea and studies me over the rim."
    mom "...You look less annoyed than 'nothingburger' would suggest, though."
    mc "That sounds like a dangerous claim."
    show mom smug
    mom "I live dangerously, kid."
    "I push my rice around."
    "Saying it out loud still feels like setting a glass near the edge of the table and waiting to see if the cat knocks it off."
    mc "Monika asked if I wanted to study tomorrow."
    mom "At school?"
    mc "Public library. Nine to noon, probably."
    mc "...Then lunch downtown."
    show mom curious
    "Mom's eyebrows go up a fraction."
    mom "Downtown where?"
    mc "That new cafe in the historic district. Green awning, by the old bank."
    mom "Oh, I saw that listing. The old stationery shop that suddenly has plants in every window?"
    mc "Probably? Heck if I know."
    show mom teasing
    mom "Nice area."
    "I break a chunk of potato apart with the edge of my spoon."
    show mom neut
    mom "With Monika."
    mc "That's generally how studying with Monika works, yeah."
    mom "I am very well aware."
    "Her voice has the terrible calm of a woman choosing not to laugh."
    mc "Before you say anything--"
    mom "I've said almost nothing."
    mc "Exactly! And I can still see all of it on your face."
    mom "You have midterms Monday. Organized prep with an organized person is hardly a crime."
    mom "As long as you eat actual food and don't try to live on coffee and anxiety."
    mc "Oh, I would never, Mom."
    show mom teasing
    mom "Until you see a pastry case. One apple fritter and you'd sign anything."
    mc "...No comment."
    show mom determined
    mom "Take your transit card, and charge your phone tonight. Text me when you get there, and again when you leave."
    mc "So stipulated."
    mom "And budget."
    mc "I have money, don't worry."
    show mom unamused
    "She gives me the look."
    mc "...I'll bring cash and not spend it like I won the lottery."
    show mom teasing
    mom "Beautiful. I'm touched."
    show mom happy
    "I snort, and Mom smiles, tired but present."
    mom "I'm glad you're making time with her."
    "The plainness of it makes me look up."
    show mom neut
    mom "You always come home from seeing her with something to say."
    mc "She does most of the talking."
    mom "Good."
    if s1_was("himeko_first", "relief"):
        "Mom slides last night's notebook out from under the mail and turns it to face me. {i}Relief{/i} is there in her handwriting, guilty footnote and all, and under it, in fresher ink: {i}That's allowed.{/i}"
        mc "...Is that legal advice?"
        show mom teasing
        mom "Pro bono. This once."
    elif s1_was("himeko_first", "fear"):
        "Mom slides last night's notebook out from under the mail, finds the page where she wrote {i}bad at it (everything else){/i}, and adds a line underneath, reading it aloud as she goes."
        mom "'Friday: brought me the paper. Unprompted.'"
        mc "...Are you building a case?"
        show mom teasing
        mom "Someone has to. Relax, the file's nowhere near complete."
    elif s1_was("himeko_first", "guilt"):
        "Mom slides last night's notebook out from under the mail. {i}Guilty{/i} is still sitting on its page by itself, with nothing written after it."
        mom "It's been a day. Is it still a minute?"
        mc "...It's a long minute."
        show mom teasing
        mom "Then I'll ask again in a minute."
    show mom teasing
    mom "Now have another scoop of rice before your sister comes down and claims it."
    mc "When has that ever stopped her? Food theft is a serious household issue."
    show mom smug
    mom "And yet no prosecutor will take the case."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "After dinner I take the dishes while Mom answers one last work email at the table. When Asahina comes down for water, I mention tomorrow's plan, and she calls back from the stairs that she already knows."
    nier "The house goes quiet around one last scratch of Mom's pen."
    call nier_clear from _call_nier_clear_0524_6
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music night_a
    "Back in my room, I push the review sheets up against the calculator to clear a path to the controller. I've spent enough of Saturday looking at paper."
    "{i}I could study more.{/i}"
    "{i}I could also admit that one more lap through the chemistry guide tonight is just staring with extra steps--{/i}"
    "My phone buzzes."
    python:
        _phone_messages = [
            phone_msg("them", "Confirmed: library at 9 tomorrow! I booked us one of the study tables by the second-floor windows."),
            phone_msg("them", "I may have overprepared."),
            phone_msg("me", "You? Impossible."),
            phone_msg("them", "Rude, but earned."),
            phone_msg("them", "Oh, and before I forget, can you send me photos of your biology and chemistry review guides?"),
            phone_msg("me", "That's a suspiciously specific request."),
            phone_msg("them", "I need the topic lists! The why can wait until tomorrow."),
            phone_msg("me", "Fine. Give me a minute."),
            phone_msg("them", "And sleep at a reasonable time, okay?"),
            phone_msg("me", "Look who's talking."),
            phone_msg("them", "I said reasonable, not early. Those are two very different words."),
            phone_msg("me", "See you at nine."),
            phone_msg("them", "See you at nine, " + player + "!"),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0524_2
    "I send her the two photos, then put the phone on the charger and pick up the controller."
    "The game loads to a low choir over a broken skyline. Whoever designed the title screen believes menus should have consequences."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The city is sealed under a false sky after somebody botched a ritual, and my party has been left to fix it. Hit an enemy's weakness and you get another turn. Whiff, and it can cost everyone theirs."
    nier "Which makes every loss bad luck and every win entirely my own skill."
    call nier_clear from _call_nier_clear_0524_7
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    "Tonight's stretch opens in the subway underpass, which has turned into a cathedral since I last came through. Past the ticket gates, black water fills the tracks and laps over half the platform."
    "It's dead still, and it's reflecting a clear blue sky. Overhead, there's nothing but concrete."
    "{i}Oh. The drowned station.{/i}"
    "My thumb goes for the phone out of pure reflex. Matsuda will want to know I finally crossed the threshold."
    "Her thread opens on the same two messages from last night, {i}Understood{/i} and {i}I overstepped{/i}, with nothing under them."
    "I put the phone back on the charger."
    "A horned bureaucrat blocks the ticket gates. \"State your alignment preference.\""
    mc "...My alignment preference is tired."
    "Tired isn't on the list. I pick neutral, since committing to a cosmic ideology this close to bedtime feels irresponsible."
    "He approves, charges me half my money as a processing fee, and joins my party."
    "{i}Thieving little bastard.{/i}"
    "The boss is waiting at the far end of the platform: a stationmaster with a lantern for a head, standing knee-deep in the fake sky."
    "Two turns in, he raises the lantern, and my next lightning spell bounces straight off it and back into my party. One very bright second later, the whole team is face down in the water."
    "{i}...So that was the move.{/i}"
    "On the retry, I leave the lightning alone and lean on the new recruit, who turns out to drain health with every hit. Twenty minutes of shuffling the lineup later, the stationmaster sinks back into his own reflection."
    "I save twice, because I have learned from pain."
    "{i}Monday can wait outside for one more night.{/i}"
    "It's past midnight, and my room has gone properly still. The menu music loops through the speakers, patient and ominous."
    "I'm reaching for the power button when the phone goes off. Matsuda."
    python:
        _stance = s1_stance("matsuda_callout", "flat")
        if _stance == "kind":
            _phone_messages = [
                phone_msg("them", "I've been trying to answer you since last night. You were kind about it, which somehow made it harder to read."),
                phone_msg("them", "I got excited. I told Kareda before I thought to check with you."),
                phone_msg("them", "Sorry. Truly."),
                phone_msg("them", "The Sunday proposal is withdrawn. I told her you never agreed to it."),
                phone_msg("them", "And please tell Asahina I'm sorry. Calling her a peon was a bit, and not a good one."),
                phone_msg("them", "I did want to go with you, though. That part wasn't a bit."),
                phone_msg("me", "I know. Another time, maybe."),
                phone_msg("them", "I can wait."),
                phone_msg("them", "It may involve visible effort."),
            ]
        elif _stance == "sharp":
            _phone_messages = [
                phone_msg("them", "Retraction filed."),
                phone_msg("them", "'Peon' has been struck from the record. 'Asahina' has been entered in its place."),
                phone_msg("them", "Okay. Real answer now."),
                phone_msg("them", "I got excited, and I told Kareda before I thought to check."),
                phone_msg("them", "Sorry."),
                phone_msg("them", "The Sunday proposal is withdrawn. I told her you never agreed to it."),
                phone_msg("them", "I did want to go with you. That part wasn't a bit."),
                phone_msg("me", "Then ask me next time. And wait for the answer."),
                phone_msg("them", "I can wait."),
                phone_msg("them", "It may involve visible effort."),
            ]
        else:
            _phone_messages = [
                phone_msg("them", player + "."),
                phone_msg("them", "I got excited. Told Kareda before I asked you."),
                phone_msg("them", "Sorry."),
                phone_msg("them", "Sunday's withdrawn. I told her you never agreed to it."),
                phone_msg("them", "Asahina. Got it."),
                phone_msg("them", "I did want to go with you. That part wasn't a bit."),
                phone_msg("me", "I know. Next time, ask."),
                phone_msg("them", "I can wait."),
                phone_msg("them", "It may involve visible effort."),
            ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, append=True) from _call_phone_text_conversation_0524_3
    "I leave the phone face-up on the charger and let the screen go dark on its own."
    $ update_character_thought("matsuda", "Matsuda's thread sat on two short messages all day. Late Saturday she apologized, withdrew the Sunday plan, and said she'd actually wanted to go with me. She says she can wait.")
    $ update_character_thought("sam", "Sam straightened Asahina's sleeve at assembly and gave me a reason to check my own shirt. Tsubaki met him on the way out.")
    $ update_character_thought("tsubaki", "Tsubaki's step caught for half a beat when Sam used her surname. I have no idea what that was.")
    $ hide_calendar()
    scene black with wipeleft_scene
    call nier_clear from _call_nier_clear_0524_8
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0524_1
    jump a0525
