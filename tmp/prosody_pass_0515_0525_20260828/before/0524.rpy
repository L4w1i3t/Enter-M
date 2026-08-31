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
    # scene; whichever they choose is the draft from then on, and s1_poem_echo
    # carries a quotable fragment of it into May 30 and May 31.
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
It's all I know what to do.

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
    play music schooldays
    "The gym smells like floor wax and several hundred people who did not consent to being awake."
    "The whole student body has been arranged by year and class across the floor, standing in lines that look straight from a distance and unravel up close."
    "{i}Morning pep assembly.{/i}"
    "{i}Because when a school says midterms begin Monday, apparently the next step is forced enthusiasm under fluorescent lighting.{/i}"
    "Somewhere near the front, a microphone pops."
    principal "Good morning, students of Itsuki Academy."
    "The speakers answer with a feedback squeal that makes half the gym flinch."
    "No one looks more encouraged afterward."
    principal "As you know, midterm exams begin after the weekend."
    principal "This assembly is a chance to remember that preparation, discipline, and mutual encouragement are the foundations of student success."
    "I end up with Asahina drifting back to my side and Sam one row behind me, where the lines have softened and assigned order has become theoretical."
    show asahina uniform neut at t21
    show sam uniform neut at t22
    "Asahina's sleeve cuff is folded weirdly."
    "Sam notices before she does, reaches over, fixes it with two fingers, and steps back like nothing happened."
    show asahina uniform embarrassed
    "She looks ahead harder than any person has ever looked ahead in history."
    ah "...Thanks."
    sa "Anytime."
    "If it were loud, it would be easier to mock. Like any other sane teenager, I take it upon myself to ruin it."
    mc "If you two get any more considerate, I'm committing a domestic crime."
    show asahina uniform annoyed
    ah "No one asked you, shitass."
    show sam uniform teasing
    sa "Hey, hey, we can try to keep the consideration under control, but...I can't promise anything~"
    show asahina uniform unamused
    ah "Don't enable him, dude. Gimpy here's not worth it."
    show asahina uniform happy
    show sam uniform happy
    "Sam smiles. Asahina's ears go pink, and she doesn't get defensive about it."
    show sam uniform pose_crossed
    principal "You are not merely taking tests. You are proving the discipline you have built all term, or for some of you, all of high school so far."
    "A classmate behind me mutters something about proving he built nothing and how he hates half his classes anyway."
    "{i}At least I respect the honesty.{/i}"
    principal "You may feel anxious. That is natural."
    principal "But anxiety is not an enemy. It is a signal that what you are doing matters."
    "The speech keeps going."
    "Goals and community lead into study habits. Sleep and hydration finish the usual obligatory checklist."
    "My track coach stands near the wall with his arms folded, and even from here I can tell he is mentally underlining things that apply to his athletes."
    "A projector screen at the side of the stage displays a slogan in clean blue letters:"
    "{b}YOUR EFFORT TODAY BECOMES TOMORROW'S CONFIDENCE.{/b}"
    "{i}My confidence tomorrow will be a half-dead ballpoint pen and an empty cracker jack box.{/i}"
    show sam uniform neut
    "My sister shifts her weight."
    "Sam shifts in the same direction a fraction later. It could be coincidence, if I had not started noticing these things against my will."
    "The assembly eventually reaches the part where the student council representative thanks everyone for their attention, despite the room offering little proof."
    # SFX SUGGESTION: A microphone cutoff pop, followed by the gym crowd swelling back in.
    "The microphone clicks off, and the gym exhales in one enormous, adolescent wave."
    "Bodies begin preparing to move before anyone grants permission, each row quietly daring the others to start the traffic jam."
    "Our class is the last to leave because of course it is. Asahina's class is long gone, though one last second-year class is filing past the end of our row."
    mc "...Asa, your people are long gone."
    ah smug "And? Not like anyone will notice anyway. I went to the bathroom, or something."
    show asahina uniform happy at t31
    show sam uniform neut at t32
    "Asahina spots someone near the back of the passing line and raises a hand."
    ah "Tsubaki!"
    show tsubaki uniform nervous at t33
    "Tsubaki looks over, then steps out of the traffic beside our row, hugging a notebook to her chest."
    show tsubaki uniform happy
    ts "Oh. Hi, Asahina. [player]."
    mc "Morning."
    show tsubaki uniform curious
    "Her gaze flicks to Sam. Barely a glance at all."
    show asahina uniform nervous
    ah "Tsubaki, Sam. Sam, Tsubaki. This guy's my, uh..."
    show sam uniform smug
    sa "Boyfriend."
    ah "...Yeah. That."
    show tsubaki uniform shocked
    "Tsubaki's hands tighten around the notebook, only a little."
    show tsubaki uniform nervous
    ts "Oh! Right. Nice to meet you."
    show sam uniform neut
    sa "Masayami Inugami. Sam's fine, though."
    show tsubaki uniform neut
    ts "Tsubaki Kareda."
    "She gives a shallow, polite bow. The loose sheet tucked inside her notebook slides forward, and Sam catches it before it falls."
    sa "Got it."
    show tsubaki uniform embarrassed
    ts "Ah--thank you!"
    "He hands it back, eyes anywhere but the writing."
    show sam uniform curious
    sa "Your name was on the poster note, right?"
    show tsubaki uniform curious
    ts "Poster note?"
    sa "Asahina told me someone actually gave useful feedback on the volleyball poster."
    show asahina uniform shocked
    "My sister's head snaps toward him."
    ah "I didn't say it like that!"
    show sam uniform teasing
    sa "You said, and I quote, 'she understood the motion lines, which means she has functioning eyes and taste.'"
    show asahina uniform embarrassed
    ah "You can't prove I said that!"
    mc "Too late. It's already in writing and in all our brains."
    show tsubaki uniform embarrassed
    "Tsubaki lowers her eyes toward the sheet like it might hide her face if she stares at it properly."
    ts "It was just a nice poster."
    show sam uniform happy
    sa "Still. Good eye."
    show tsubaki uniform nervous
    "Her smile starts, then slips behind a quick nod."
    ts "Thanks..."
    # SFX SUGGESTION: Two sharp handclaps with a short gymnasium echo.
    "A teacher claps twice near the doorway."
    teacher "Second-years, keep moving!"
    show tsubaki uniform worried
    ts "I should go."
    show asahina uniform teasing
    ah "Yeah, before that path is sealed forever."
    show tsubaki uniform teasing
    ts "That sounds more tactical than I expected."
    show tsubaki uniform happy
    ts "See you guys later."
    show sam uniform neut
    sa "Later, Kareda."
    show tsubaki uniform shocked
    "Her step catches by half a beat before rejoining her class."
    show tsubaki at thide
    hide tsubaki
    show asahina uniform neut at t21
    show sam uniform neut at t22
    ah "...She's nice."
    mc "You said that yesterday."
    show asahina uniform unamused
    ah "Maybe she's still nice today. Ever think of that?"
    show sam uniform thinking
    sa "She seemed jumpy."
    show asahina uniform curious
    ah "Jumpy how?"
    show sam uniform pose_thinking
    sa "She checked behind her twice and almost lost that notebook. Could just be the crowd."
    show asahina uniform thinking
    ah "Maybe. She does keep acting like she needs permission to stand somewhere, though."
    show sam uniform neut
    sa "Then you've seen more of her than I have."
    "Asahina looks toward the doorway Tsubaki used. Sam leaves his guess where it is."
    "The traffic behind us begins to push."
    mc "Okay, we should move before the gym decides we live here now."
    show asahina uniform teasing
    ah "You're so dramatic."
    show sam uniform smug
    sa "I mean, he {i}is{/i} right."
    "We move with the crowd. The hard plastic smell of the gym floor follows us out."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Homeroom becomes a distribution center for exam reminders. Civics, language arts, and biology each add a review packet to the pile."
    nier "By lunch, my binder has probably doubled in weight."
    call nier_clear from _call_nier_clear_0524_1
    stop music fadeout 1.0
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music dailyfantasy
    "Lunch comes so late that the morning already feels borrowed."
    show asahina uniform neut at t11
    "Asahina finds me by the stairwell, checking her phone with one thumb."
    ah "Roof?"
    mc "You've really streamlined the invitation process, I see."
    show asahina uniform unamused
    ah "Roof, please."
    mc "That revision really sold it."
    "She glances down the hall once."
    mc "Where's Sam?"
    show asahina uniform neut
    ah "Senior thing, or basketball. He said he'd text me after."
    mc "You sound normal about it."
    show asahina uniform smug
    ah "I'm normal about literally everything. Normal is my middle name, don'tcha know?"
    mc "Your dedication is moving."
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
    "The rooftop air feels less recycled than the rest of the building, making it inherently more valuable."
    "The sky, washed with Saturday brightness, gives off the impression that the day should have ended forever ago."
    show asahina uniform neut at t11
    "Asahina sits against the wall and opens her lunch bag while blatantly side-eying her phone."
    "A few seconds pass and she capitulates to blue light and a quaint lock screen."
    mc "Subtle."
    ah "I'm checking the time."
    mc "On a screen with a heart sticker near the camera?"
    ah "That sticker was free, aight?"
    show asahina uniform embarrassed
    "She points her chopsticks at me without looking up, ears going faintly pink."
    ah "Eat your food, slowbrain."
    "I obey, on the grounds that I am too hungry to press it."
    "The first few minutes are uneventful, as neither of us believes silence means the relationship has crashed."
    "My sister, still sporting a pinkish hue on her ears, finally puts her phone facedown on her lap."
    show asahina uniform worried
    ah "Do you think Tsubaki was okay earlier?"
    mc "In the gym?"
    show asahina uniform pose_eyeroll
    ah "No, in the Pacific Ocean. Yes, in the gym, dumbass."
    mc "She looked surprised. Not hurt, exactly."
    show asahina uniform unamused
    ah "Yeah. Like Sam handed her an award instead of one compliment."
    mc "You jelly?"
    show asahina uniform angry
    "Her head turns very slowly."
    ah "I'll kill you."
    mc "Okay, okay..."
    "The easy joke waits in front of me, yet I leave it there."
    show asahina uniform neut
    "She keeps her eyes on the skyline."
    ah "It's just...I know how nice compliments feel when you aren't fishing for them."
    ah "I don't want her thinking every nice thing is a setup."
    mc "Then keep giving her normal ones."
    show asahina uniform thinking
    ah "Without making it weird."
    mc "Impossible standard, but you can try."
    "She eats another bite and gives that the attention it deserves. For a while, the roof only asks us to finish lunch."
    show asahina uniform neut
    ah "I can do normal."
    mc "That claim needs peer review."
    "She bumps her shoe against mine, lightly this time. My phone buzzes after the silence has had somewhere to land."
    "{i}Yeah, about time for regularly scheduled contact.{/i}"
    python:
        _phone_messages = [
            phone_msg("them", "Where did you disappear to?"),
            phone_msg("them", "I checked the club room for a second and it was aggressively empty."),
            phone_msg("me", "Roof. Asa pulled rank for lunch."),
            phone_msg("them", "Kidnapped? Should I notify someone?"),
            phone_msg("me", "No, she has snacks. Negotiations are stable."),
            phone_msg("them", "Good. Stay there for a few minutes? I wanted to ask you something before afternoon classes."),
            phone_msg("me", "Sure. Door's unlocked, probably."),
            phone_msg("them", "Yay!"),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0524_1
    show asahina uniform curious
    ah "Monika?"
    mc "Yeah."
    show asahina uniform smug
    ah "Wow. She came looking?"
    mc "She wants to ask something."
    show asahina uniform teasing
    ah "Uh-huh."
    mc "That's all I know, don't gimme that."
    ah "Uh-huh..."
    mc "Can you not make that noise like you cracked a code?"
    ah "Can you not be a drooling dumbass for five seconds?"
    play sound moddooropen
    "The rooftop door opens, and the verbal hands stay mostly unthrown."
    show asahina uniform neut at t21
    show monika forward uniform happ cm oe nobl rdown ldown at t22
    "Monika steps out, a folder against her chest. The wind immediately pulls at the loose ribbon of her bow."
    m forward uniform happ om oe nobl rdown ldown "There's my guy!"
    mc "Present."
    m forward uniform happ cm oe nobl rdown ldown "Hi, Asahina!"
    ah "Yo."
    m forward uniform wry om oe nobl rdown ldown "Sorry to interrupt whatever was going on."
    "Asahina looks from Monika's folder to the fingers tightening around its edge."
    show asahina uniform neut
    ah "You're not. I was done eating anyway."
    mc "You were?"
    show asahina uniform teasing
    ah "Yep. You two have your responsible-person summit."
    m forward uniform nerv om oe awkw rdown ldown "You don't have to leave."
    show asahina uniform smug
    ah "I know. I want to catch Sam before fifth period."
    "She closes her lunch bag and gets to her feet without rushing."
    ah "Later."
    m "See you."
    mc "Don't hit your head on the way out."
    show asahina at thide
    hide asahina
    play sound moddoorclose
    "The door closes behind her, and the roof is suddenly much quieter."
    show monika forward uniform nerv cm oe awkw rdown ldown at t11
    "Monika remains standing for a second. Her thumb works at the folder's corner."
    mc "You alright?"
    m forward uniform nerv om oe awkw rhip ldown "Yeah. I just wanted to ask before I talked myself into making it overly responsible."
    mc "You say that like I shouldn't be concerned."
    "She laughs once, soft and unfinished."
    m forward uniform happ cm oe nobl rhip ldown "Tomorrow's our last full study day before exams."
    m "I know you probably already have a plan, and I know your science and math stuff is more...you know."
    mc "Soul-crushing? The kind that makes you want to throw the whole notebook off the roof?"
    m forward uniform nerv om ce blaw rdown ldown "...I was going to say STEM-oriented."
    mc "...That too."
    m forward uniform happ cm ce nobl rdown ldown "I try."
    "She sits beside me, leaving a careful space that feels more deliberate than sitting close would."
    m forward uniform nerv om oe blus rhip ldown "I was thinking we could meet at the public library in the morning."
    m "Study for a few hours, trade notes where we can, maybe quiz each other."
    m "I can help with language arts and civics, and you can keep me from getting destroyed by algebra notation. For your science classes, I can at least tell you when the explanations stop sounding human."
    mc "That's ambitious."
    m forward uniform nerv om oe blus rdown ldown "After that, if we survive, there's that new cafe downtown in the historic district, the one with the green awning near the old bank."
    "She looks down at the folder and a corner of a printed review sheet peeks out."
    m forward uniform flus cm oe blus rdown ldown "I thought lunch there might be nice."
    "{i}Ah.{/i}"
    "Monika keeps talking, each sentence arriving before the silence can settle."
    m forward uniform nerv om oe awkw rdown ldown "Not as, like, a big thing, just...exams are coming up, track is back, you have college stuff probably, and your family, and..."
    "She stops herself there."
    "Her grip loosens on the folder. When she speaks again, the practiced brightness is gone."
    m forward uniform flus cm oe blus rdown ldown "I missed talking to you without the school day pulling at our sleeves."
    mc "Didn't we just go to the movies last weekend?"
    m "I mean, yeah, but I just wanna make it more of a regular occurrence, y'know?"
    m "We've known each other for...how many months now? Eight? Nine?"
    m "What good are friends if they only meet when responsibility beats them with a stick?"
    "I look at the city and the tall buildings beyond the fence."
    mc "You do drive a solid bargain."
    mc "I'll make it easy for you here: yeah, library and lunch sounds good tomorrow."
    "She looks up."
    m forward uniform vsur om oe nobl rdown ldown "Really?"
    mc "Yeah, seriously."
    mc "I was probably going to spend the morning arguing with notes anyway. Least I can do is do it with a friend."
    mc "Not to mention I know no one else who can call out when my explanations start sounding like nonsense."
    "Her shoulders loosen."
    m forward uniform happ cm ce nobl rdown ldown "Well, that {i}is{/i} one of my core talents."
    mc "Your marketable skills are terrifying."
    m forward uniform laug cm ce nobl rdown ldown "Thank ya, thank ya."
    "Her smile returns, smaller but no longer strained."
    m forward uniform happ cm oe nobl rhip ldown "I'll send you the time tonight."
    mc "No need to. I can meet you there at, like, nine."
    m forward uniform happ om oe nobl rdown lpoint "Yeah, nine works! Don't make me text five reminders."
    mc "I would never."
    m forward uniform wry cm ce nobl rdown ldown "You absolutely would, by needing them."
    mc "Correct, albeit awfully cruel wording..."
    # SFX SUGGESTION: A distant warning bell that gently breaks the rooftop quiet.
    "Somewhere below us a bell goes, and the roof stops belonging to us."
    "Monika stands first and I follow suit."
    m "Okay! Let's get back before we're written up as runaways."
    mc "That seems reasonable."
    m "I manage it occasionally."
    "She pauses near the door."
    m forward uniform nerv om oe awkw rdown ldown "Thanks."
    mc "For...saying yes?"
    m forward uniform neut cm oe blus rdown ldown "For not making me make it smaller."
    "That one takes the air out of my joke before it forms."
    mc "...Yeah. No problem."
    show monika at thide
    hide monika
    play sound moddoorclose
    "The rooftop goes back to wind and concrete."
    $ update_character_thought("monika", "Monika reserved a study table by the second-floor windows before she asked me whether I was free. She has been at council every afternoon this week.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Chemistry uses the whole period to hand back study guides with no regard for human limits."
    nier "Math is next, and the stack comes with me."
    call nier_clear from _call_nier_clear_0524_2
    stop music fadeout 1.0
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music quiz
    "College algebra review begins with a silence only matrices can create."
    show math_teacher neut at t11
    math_teacher "Matrices are not decorative boxes. They're a way to organize operations."
    math_teacher "Some of you will find that easier, and others won't."
    math_teacher "If you treat them like a pile of numbers with cute little brackets, you will make mistakes that are very easy to avoid."
    "{i}Decorative boxes. Got it.{/i}"
    "The teacher writes two matrices on the board."
    "{i}A is two by three. B is three by two.{/i}"
    math_teacher "First check: can AB be multiplied?"
    "Several students look down, which is the international classroom signal for 'please let this question choose someone else.'"
    "I make the fatal mistake of having already written the dimensions in my notes."
    math_teacher "[player]."
    mc "...Yes?"
    math_teacher "Can AB be multiplied, and what size is the result?"
    $ atmos_pressure()
    with dissolve
    menu:
        "Yes. The result is two by two.":
            $ atmos_pressure_clear()
            with dissolve
            mc "Yes. The inside dimensions match, so the result takes the outside dimensions: two by two."
            math_teacher "Correct."
            "He circles the three and three in the middle, then boxes the two and two on the outside."
            "{i}One simple sentence, and this coming Monday feels a little less hostile.{/i}"
        "Yes. The result is three by three.":
            $ atmos_pressure_clear()
            with dissolve
            mc "Yes. Three by three."
            "The board stares back."
            "The two and two sit outside the expression like they are waiting for me to stop embarrassing both of us."
            math_teacher "Not quite."
            math_teacher "Inside confirms compatibility. The outside gives a two-by-two result."
            math_teacher "Do not average the sizes, do not guess by vibes, and do not let panic do arithmetic."
            "{i}Panic is not a reliable calculator. Duly noted.{/i}"
        "No. The dimensions do not match.":
            $ atmos_pressure_clear()
            with dissolve
            mc "No. They don't match."
            math_teacher "Check again."
            "Two by three times three by two."
            "The middle dimensions match."
            math_teacher "Inside confirms compatibility. The outside gives a two-by-two result."
            "{i}Nearly taken out by a bracket. Not my proudest moment.{/i}"
    math_teacher "Now BA."
    "The board receives a second set of arrows."
    math_teacher "Order matters. AB and BA aren't guaranteed the same size or value, and one may not exist at all."
    "{i}Order matters. Math has social boundaries too.{/i}"
    "He writes a multiplication table step by step."
    "Row times column. First column, then the second, and repeat."
    "It is so unbearably tedious that I can't help but put my hand on my chin and rest my elbow on my desk."
    math_teacher "Midterm expectation: you must show the setup."
    math_teacher "If I see a correct answer with no path, I cannot tell whether you actually understood it or rolled lucky dice."
    math_teacher "Now, I'm not usually one to make something all-or-nothing, but the whole point of exams is to show comprehension and maybe some problem-solving skills."
    "The class practices three examples."
    "By the third, someone near the windows asks whether calculators will be allowed and receives a look normally reserved for betrayal."
    math_teacher "For this one, yes. Calculators can help you multiply larger numbers or decimals, but they cannot save you from entering the wrong structure."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Algebra ends with a review sheet that bows the binder pocket. English adds vocabulary, because Saturday apparently has no interest in staying light."
    nier "One last announcement covers pencils and sleep. By the final bell, the school feels less like a building and more like a machine ejecting exhausted students into the weekend."
    call nier_clear from _call_nier_clear_0524_3
    stop music fadeout 1.0
    pause 2.0
    scene bg club_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music daily
    "The club room feels warmer than usual when I arrive. Not physically, though the afternoon sun does its best."
    "A few members are already here, notebooks open and chairs pulled into loose corners, but the room is holding a not-so-rare quiet."
    show monika forward uniform happ cm oe nobl rdown ldown at t11
    "Monika stands near the board, writing the prompt in clean letters: {i}Write about a place that holds still while you don't.{/i}"
    "She turns when she hears the door."
    m forward uniform happ om oe nobl rdown ldown "Yo."
    mc "Hey."
    "I take my usual seat and pull out my notebook. The desk has a tiny nick near the corner that my thumb finds before my brain does."
    "Same desk, same room, shifted by half an inch."
    m forward uniform happ cm oe nobl rhip ldown "I figured we could keep it low pressure today."
    m forward uniform happ om oe nobl rhip lpoint "Fifteen minutes drafting, then voluntary exchange. Rapid-fire poetry and all that."
    m "And actually voluntary this time. Everyone looks tired, and forcing feedback would only make them defensive."
    "Everyone lowers into writing. For a while, there is only paper noise."
    "Someone near the back erases until the page wrinkles, then crosses out exactly three words and keeps going."
    "I stare at the prompt longer than I should."
    "The obvious answer is school, which has all the subtlety of a backhanded motivational poster. I circle back to it anyway."
    "My pen moves before I fully decide. It starts with a bus seat by the window."
    call enter_m_showpoem(poem_0524_mc_draft) from _call_enter_m_showpoem_0524_1
    "I look at the lines."
    "{i}Not exactly the cheerful version of exam-week pressure, then.{/i}"
    m forward uniform curi om oe nobl rhip ldown "You stopped..."
    mc "For now. Stop hovering."
    m forward uniform happ cm ce nobl rhip ldown "What'd I say about getting defensive...?"
    mc "It probably was. Can't do my best with a hawk on my shoulder."
    # SFX SUGGESTION: A short, neutral timer buzz from Monika's phone.
    "Monika stands and brings her notebook to my desk once the timer on her phone buzzes."
    show monika forward uniform happ cm oe nobl rdown ldown at t11
    "{i}So much for the meaning of voluntary.{/i}"
    m forward uniform happ om oe nobl rdown ldown "Trade?"
    mc "As always."
    "We swap notebooks with very little ceremony."
    "Her handwriting is neater than mine even when she is drafting. The title is crossed out, and under it, a new one sits in smaller letters."
    "I read."
    call enter_m_showpoem(poem_0524_monika) from _call_enter_m_showpoem_0524_2
    "I stop reading for a second. Around me, nothing changes."
    "A page turns somewhere behind us. Someone asks a raspy question about whether a line is too blunt, and the answer comes back just as quietly."
    "Monika sits across from me and reads six lines without hurrying."
    "It should be easy to say something, yet it is not."
    mc "This is..."
    "Her eyes lift."
    m forward uniform worr om oe nobl rdown ldown "Too much?"
    mc "No. It's good, just a bit specific and on the nose."
    mc "It feels like the table exists. Or am I off the mark and that was just symbolic?"
    m forward uniform happ cm oe nobl rhip ldown "That was the hope."
    "She grins, then looks back down at my notebook instead of her own."
    m forward uniform happ om oe nobl rdown ldown "Yours is good too."
    "She reads it once more, slower, and her finger stops near the margin where, on any other draft, there would be a bracket."
    "This time there isn't one."
    m forward uniform happ om oe nobl rdown lpoint "Huh. No 'annotations' this time."
    mc "...Didn't need them."
    "She doesn't answer that and lets it be a true statement."
    mc "It's only six lines."
    m forward uniform happ cm oe nobl rhip ldown "Maybe that's why it works. Some poems don't need to be extravagant pieces."
    m "But the line about the seat remembering nobody is strong."
    "Her finger hovers near the page without touching it."
    m forward uniform curi om oe nobl rdown lpoint "It says something honest without explaining itself to death. So don't ruin it."
    m "My suggestion, though: add one image after these last two lines. Not an explanation."
    "She taps the air once."
    m "Something the seat or something else physically does."
    mc "Feedback and homework at once."
    m forward uniform happ cm oe nobl rhip lpoint "Just one line."
    "I turn the notebook back toward me and think."
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
    "She reads over my shoulder. I feel her attention before I see her reaction."
    m forward uniform happ cm ce blus rdown ldown "There."
    "One syllable, and she means all of it."
    mc "Yeah?"
    m "...Yeah."
    "We sit with that a second too long."
    hikari "Get a room, you two!"
    m forward uniform flus om oe blaw rdown ldown "Hey!"
    "Monika turns red so quickly that I almost feel the heat from across the desk."
    "A few people snicker without much resistance into their writing."
    m forward uniform flus om oe blaw rdown ldown "We're giving feedback over here!"
    "I press my lips together and keep quiet."
    "Monika presses the back of one hand to her cheek and tries to regain presidential authority from somewhere under the desk."
    m forward uniform flus cm oe blaw rhip lpoint "All right, new rule: no commenting on other people's feedback...for like five minutes!"
    mc "I'd say that's a perfectly reasonable rule."
    m forward uniform wry cm ce blaw rdown ldown "Thank you."
    "She looks at me first. It works, which is annoying."
    mc "...Understood."
    "For the next half hour, club actually becomes club. Some people trade drafts while others keep writing alone."
    "Monika moves around the room collecting and offering notes. She only glances at me twice."
    "...Maybe three times. In times like these, I stop myself from counting."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Club ends gently. Poetry is one of the few mediums that lets small, unfinished things stay that way."
    call nier_clear from _call_nier_clear_0524_4
    pause 2.0
    scene bg club_day
    $ show_calendar()
    $ atmos("evening")
    show monika forward uniform happ cm oe nobl rdown ldown at t11
    with wipeleft_scene
    "The room is almost empty when Monika stacks the last loose paper."
    m forward uniform nerv om oe awkw rdown ldown "Sorry about earlier. I didn't mean for...whatever that awkward moment was."
    mc "It wasn't that bad. I've been through worse."
    m "Still..."
    mc "The club noticed a thing and moved on. You know how people are."
    m forward uniform flus om ce blaw rdown ldown "Still embarrassing, though..."
    "She slides her notebook into her bag and squares the zipper with both hands."
    m forward uniform nerv om oe blus rhip ldown "Anyway! Tomorrow at nine, then?"
    mc "Tomorrow at nine. Green awning near the old bank."
    m forward uniform curi om oe nobl rdown ldown "Oh hey, you remembered~"
    mc "Oh don't be like that, I have my moments."
    m forward uniform happ cm oe nobl rdown ldown "Yes, you do..."
    "The words are simple. I look away anyway."
    m forward uniform happ cm ce nobl rdown ldown "See you tomorrow, [player]!"
    mc "Catch ya later."
    show monika at thide
    hide monika
    pause 2.0
    mc "..."
    mc "Heh."
    "I leave before the goodbye can pick up any extra weight."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The trip home is quiet. A Saturday evening does not owe me more than that."
    nier "My bag carries review sheets and eight lines about a bus seat. Tomorrow rides in the planner like a small lit window."
    call nier_clear from _call_nier_clear_0524_5
    stop music fadeout 1.0
    pause 2.0
    scene bg dining_table_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music dailyleisure
    "Dinner is quieter than usual because Asahina eats early and disappears upstairs under the noble banner of homework."
    "The fact that homework apparently requires three separate bursts of laughter through the floorboards is none of my business."
    "Mom and I take the table with curry and a tiredness that prefers not to host a full family debate."
    show mom curious at t11
    mom "How was the exam assembly?"
    mc "Mostly a nothingburger."
    mom "Oof. That bad, huh?"
    mc "It was fine. Just very...very drawn out."
    mc "...Preachy-as-heck as usual, though."
    show mom teasing
    mom "Mm. Efficient use of your time, then."
    show mom thinking
    "She takes a sip of tea and studies me over the rim."
    mom "...Though you look less annoyed than that answer suggests."
    mc "That sounds like a dangerous claim."
    show mom smug
    mom "I live dangerously, kid."
    "I push rice around my plate."
    "Saying it out loud still feels like setting an object on the table and waiting to see whether the cat knocks it off."
    mc "Monika asked if I wanted to study tomorrow."
    mom "At school?"
    mc "Public library."
    mc "Morning session, probably nine to noon or so. Then a cafe date downtown."
    show mom curious
    "Mom's eyebrows lift a fraction."
    mom "Downtown where?"
    mc "Historic district."
    mc "There's a new cafe near the old bank building. Green awning."
    mom "Ah, I think I saw that listing."
    mom "The one that turned the old stationery shop into something with plants in the windows?"
    mc "Probably. Heck if I know."
    show mom teasing
    mom "Nice area."
    "I pretend to be very concerned with my soup."
    mom "So study, then lunch."
    mc "Yeah, that pretty much sums it up."
    show mom neut
    mom "With Monika."
    mc "Generally how studying with Monika works."
    mom "I am very well aware."
    "Her voice has the terrible calm of choosing not to laugh."
    mc "Before you say anything..."
    show mom smug
    mom "I have said almost nothing."
    mc "Exactly, but I can see it all on your face."
    mom "You have midterms Monday. Organized prep with an organized person is not by any means a crime."
    mom "As long as you eat actual food and do not attempt to live on coffee and anxiety."
    mc "Oh, I would never, Mom."
    mom "You would consider it if the cafe had pastries. The magic words to your heart are 'apple fritter' and you know that~"
    mc "...No comment."
    show mom determined
    "She writes something on the corner of a grocery list."
    mom "Take your transit card and be sure to charge your phone tonight. Tell me when you get there and when you leave."
    mc "Yes, counselor."
    mom "And budget."
    mc "I have money. Don't worry."
    mom "Okay, perfect. Not the same as a budget."
    show mom unamused
    "She gives me the look."
    mc "...I will bring cash and not spend it like crazy."
    show mom smug
    mom "Beautiful. I'm touched to hear that."
    show mom happy
    "A snicker escapes me while Mom smiles, tired but present."
    mom "I'm glad you're making time with her."
    "The plainness of it makes me look up."
    show mom neut
    mom "I'm being honest when I say that. The week has been full, and next week will be worse before it gets better."
    mom "People who help you breathe deserve time on the calendar too."
    "The kitchen hum fills the space instead of me trying to be coy."
    mc "...Yeah. She does."
    "Mom nods once, accepting the answer without making me expand it."
    mom "Good."
    show mom teasing
    "She reaches for the serving spoon."
    mom "Now eat another scoop of rice before your sister comes down and says it's hers."
    mc "And when has that stopped her? Food theft is a serious household issue."
    show mom smug
    mom "And yet no prosecutor will take the case."
    "Dinner continues from there."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "After dinner, I wash dishes while Mom reviews one last work email at the table."
    nier "Asahina comes down for water and is halfway upstairs by the time I mention the call. The house goes quiet around one last scratch of Mom's pen."
    call nier_clear from _call_nier_clear_0524_6
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music fantasypassion
    "Night finally gives my room back. My desk is a negotiation between responsibility and everything else."
    "On one side, review sheets and literature notes crowd a calculator. A pencil sharpened into a weapon waits among them."
    "On the other: my console's controller, waiting with patient digital malice."
    "{i}I could study more.{/i}"
    "{i}I could also admit one more pass through matrices at ten at night will probably not make me a different person.{/i}"
    "My phone buzzes."
    python:
        _phone_messages = [
            phone_msg("them", "Confirmed: library at 9 tomorrow. I reserved one of the study tables by the second-floor windows."),
            phone_msg("them", "I may have overprepared."),
            phone_msg("me", "You? Impossible."),
            phone_msg("them", "Rude but earned."),
            phone_msg("them", "Before I forget, send me photos of your biology and chemistry review guides."),
            phone_msg("me", "That request is suspiciously specific."),
            phone_msg("them", "I need the topic list. The reason can wait until tomorrow."),
            phone_msg("me", "Fine. Give me a minute."),
            phone_msg("them", "Sleep at a reasonable time, okay?"),
            phone_msg("me", "Look who's talking."),
            phone_msg("them", "I said reasonable, not early. Two different things."),
            phone_msg("me", "Fine. See you at nine."),
            phone_msg("them", "See you at nine, " + player + "."),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0524_2
    "I drop whatever is in my hands onto the blanket before submitting to my console."
    "My game loads to a low choir over a broken city skyline. The title screen looks designed by someone who believes menus should have existential consequences."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The game is about a city sealed under a false sky after a ritual goes wrong."
    nier "Combat runs on a momentum system where hitting weaknesses grants extra turns and missing lets enemies punish the entire party."
    nier "Every time I lose, I call it bad luck. At the same time, every win is a display of pure skill."
    call nier_clear from _call_nier_clear_0524_7
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    "My party is currently in the subway underpass, which has become a cathedral for reasons the game has not yet explained and probably will explain later with great seriousness."
    "A horned bureaucrat blocks the ticket gates."
    "\"State your alignment preference.\""
    "Apparently the game expects cosmic commitment while I am looking for a save point."
    mc "...My alignment preference is tired."
    "The game does not accept tired as an answer. I choose the neutral response, because committing to cosmic ideology before bed feels wrong."
    "The bureaucrat approves, takes half my money as a processing fee, and joins my party."
    "{i}Unbelievable...{/i}"
    "The next encounter nearly wipes me because I forget that lightning skills reflect off one enemy and healing magic costs more than my current dignity can afford."
    "Annoying, but absorbing. I stay in the fray."
    "For twenty minutes, midterms become numbers in a game instead of numbers on a schedule. The library becomes a marker on tomorrow instead of a thing to overthink."
    "I save twice because I have learned from pain, then I sit for a moment with the controller in my lap."
    "My room has gone properly still. The game music loops softly through the speakers, patient and ominous."
    "{i}Monday can wait outside for one more night.{/i}"
    "I turn the console off before the next dungeon can make a liar out of my bedtime."
    $ update_character_thought("sam", "Sam fixed Asahina's sleeve cuff before she noticed it was folded. He noticed Tsubaki watching the aisle, then admitted he could be wrong about why.")
    $ update_character_thought("tsubaki", "Tsubaki's step caught for half a beat when Sam used her surname. I have no idea what that was.")
    $ hide_calendar()
    scene black with wipeleft_scene
    call nier_clear from _call_nier_clear_0524_8
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0524_1
    jump a0525
