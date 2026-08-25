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
    $ atmos("afternoon")
    with dissolve_scene_full
    play music schooldays
    window auto
    "The gym smells like floor wax and several hundred people who did not consent to being awake."
    "The whole student body has been arranged by year and class across the floor, standing in lines that look straight from a distance but teeter off."
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
    principal "You are not merely taking tests. You are proving the discipline you have built all term--and some of you, all of high school up to this point."
    "A classmate behind me mutters something about proving he built nothing and how he hates half his classes anyway."
    "{i}At least I respect the honesty.{/i}"
    principal "You may feel anxious. That is natural."
    principal "But anxiety is not an enemy. It is a signal that what you are doing matters."
    "The speech keeps going."
    "Goals. Community. Study habits. Sleep. Hydration. The usual snooze-inducing, egregious, obligatory checklist."
    "My track coach stands near the wall with his arms folded, and even from here I can tell he is mentally underlining things that apply to his athletes."
    "A projector screen at the side of the stage displays a slogan in clean blue letters:"
    "{b}YOUR EFFORT TODAY BECOMES TOMORROW'S CONFIDENCE.{/b}"
    "{i}My confidence tomorrow will be a half-dead ballpoint pen and an empty cracker jack box.{/i}"
    show sam uniform neut
    "My sister shifts her weight."
    "Sam replicates her actions a fraction later. It could be coincidence, if I had not started noticing these things against my will."
    "The assembly eventually reaches the part where the student council representative thanks everyone for their attention, despite the room offering little proof."
    # SFX SUGGESTION: A microphone cutoff pop, followed by the gym crowd swelling back in.
    "The microphone clicks off, and the gym exhales in one enormous, adolescent wave."
    "Bodies begin preparing to move before anyone grants permission, almost like everyone is desperate to cause a crowd crush and maybe some casualties."
    "Our class is the last to leave because of course it is, so we watch the first-years and second-years enjoy temporary freedom before we do."
    mc "...Asa, your people are long gone."
    ah smug "And? Not like anyone will notice anyway. I went to the bathroom, or something."
    show asahina uniform neut at t31
    show sam uniform neut at t32
    show tsubaki uniform nervous at t33
    "A familiar face appears at the edge of our row with a notebook hugged to her chest."
    ts uniform embarrassed "Sorry, excuse me... I think my class is cutting through here."
    show asahina uniform happy
    ah "Oh, Tsubaki!"
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
    sa "Masayami Inugami."
    sa "Sam's fine, though."
    show tsubaki uniform neut
    ts "Tsubaki Kareda."
    "She bows, polite and shallow, and the loose sheet tucked inside her notebook slips forward, where it's caught by someone too smooth for his own good."
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
    mc "Too late. It's already in writing. In all our brains."
    show tsubaki uniform embarrassed
    "Tsubaki lowers her eyes toward the sheet like it might hide her face if she believes hard enough."
    ts "It was just a nice poster."
    show sam uniform happy
    sa "Still. Good eye."
    show tsubaki uniform nervous
    "Her smile starts, panics, and becomes something she stores safely behind a nod."
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
    sa "She seems awfully skiddish."
    show asahina uniform curious
    ah "Skiddish...how?"
    show sam uniform pose_thinking
    sa "You not see how she was constantly looking over her shoulders? And how she didn't commit to her grip?"
    "All our voices fall flat as none of us can come up with a witty remark."
    show asahina uniform thinking
    ah "...Huh."
    "The traffic behind us begins to push."
    mc "Okay, we should move before the gym decides we live here now."
    show asahina uniform teasing
    ah "Dramatic."
    show sam uniform smug
    sa "I mean, he {i}is{/i} right."
    "We move with the crowd, and the assembly disappears behind us with the hard plastic smell of the gym floor."
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
    "Lunch feels like it comes too late to feel embedded in reality."
    show asahina uniform neut at t11
    "Asahina finds me by the stairwell, checking her phone with one thumb."
    ah "Roof?"
    mc "You've really streamlined the invitation process, I see."
    show asahina uniform unamused
    ah "Roof, please."
    mc "Powerful revision."
    "She glances down the hall once."
    mc "Where's Sam?"
    show asahina uniform neut
    ah "Senior thing."
    ah "Or basketball thing. Or both. He said he'd text me after."
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
    ah "No, in the Pacific ocean--YES, in the gym, dumbass."
    mc "She seemed...Tsubaki."
    show asahina uniform unamused
    ah "...The hell is that supposed to mean?"
    mc "It means what it means."
    ah "Yeah, whatever in the world {i}that{/i} means."
    "She pokes at her food."
    show asahina uniform thinking
    ah "Sam gave her a compliment, and she looked like he handed her an award."
    mc "You jelly?"
    show asahina uniform angry
    "Her head turns very slowly."
    ah "I'll kill you."
    mc "Okay, okay..."
    "The easy joke waits in front of me, yet I leave it there."
    show asahina uniform neut
    "She keeps her eyes on the skyline."
    ah "It's just...I dunno."
    ah "I get how nice compliments feel when you aren't fishing for 'em."
    "The idea of the poster hangs between the words without being named."
    mc "...Perchance."
    "My phone buzzes, not letting the sentence take any more time to breathe."
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
    ah "Uh huh."
    mc "That's all I know, don't gimme that."
    ah "Uh huh..."
    mc "Can you not make that noise like you cracked a code?"
    ah "Can you not be a drooling dumbass for five seconds?"
    play sound moddooropen
    "The rooftop door opens, and the verbal hands stay mostly unthrown."
    show asahina uniform neut at t21
    show monika forward uniform happ cm oe nobl rdown ldown at t22
    "Monika steps out with a folder against her chest and wind immediately pulling at the loose ribbon of her bow."
    m forward uniform happ om oe nobl rdown ldown "There's my guy!"
    mc "Present."
    m forward uniform happ cm oe nobl rdown ldown "Hi, Asahina!"
    ah "Yo."
    m forward uniform wry om oe nobl rdown ldown "Sorry to interrupt whatever was going on."
    show asahina uniform teasing
    ah "You're not. I was about to return to civilization anyway."
    mc "You were?"
    ah "Yes. Because I'm responsible and have..."
    # SFX SUGGESTION: A single phone vibration muffled by the lunch bag.
    "Her phone buzzes once in her lap."
    ah "...a thing."
    mc "A senior thing? Basketball thing?"
    show asahina uniform smug
    ah "A leaving thing."
    "She packs with a speed that fails to look innocent."
    ah "Later."
    m "See you."
    mc "Don't hit your head on the way out."
    show asahina at thide
    hide asahina
    play sound moddoorclose
    "The door closes behind her, and the roof is suddenly much quieter."
    show monika forward uniform nerv cm oe awkw rdown ldown at t11
    "Monika remains standing for a second, fingers tightening around the folder."
    mc "You alright?"
    m forward uniform nerv cm oe awkw rdown ldown "Yeah."
    m forward uniform nerv om oe awkw rhip ldown "I just wanted to ask before I talked myself into making it overly responsible."
    mc "Concerning phrase."
    "She laughs once, soft and not quite enough."
    m forward uniform happ cm oe nobl rhip ldown "Tomorrow's our last full study day before exams."
    m "I know you probably already have a plan, and I know your science and math stuff is more...you know."
    mc "Soul-crushing? Stress-inducing? Guilty of making you want to blow your head off?"
    m forward uniform nerv om ce blaw rdown ldown "...STEM-oriented."
    mc "...That too."
    m forward uniform happ cm ce nobl rdown ldown "I try."
    "She sits beside me, leaving a careful space that feels more deliberate than sitting close would."
    m forward uniform nerv om oe blus rhip ldown "I was thinking we could meet at the public library in the morning."
    m "Study for a few hours, trade notes where we can, maybe quiz each other."
    m "I can help with language arts and civics, you can help me not get destroyed by algebra notation, and we can both pretend biology is a normal subject."
    mc "Bold plan."
    m forward uniform nerv om oe blus rdown ldown "After that, if we survive, there's that new cafe downtown in the historic district--the one with the green awning near the old bank."
    "She looks down at the folder and a corner of a printed review sheet peeks out."
    m forward uniform flus cm oe blus rdown ldown "I thought lunch there might be nice."
    "{i}Ah.{/i}"
    "Monika keeps talking as a means to not draw attention to growing silence."
    m forward uniform nerv om oe awkw rdown ldown "Not as, like, a big thing, just...exams are coming up, track is back, you have college stuff probably, and your family, and..."
    "She stops herself there."
    "For a second, the president version of Monika disappears."
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
    "The smile returns, but smaller. Like a weird, contorted smirk."
    m forward uniform happ cm oe nobl rhip ldown "I'll send you the time tonight."
    mc "No need to. I can meet you there at, like, nine."
    m "Yeah, nine works!"
    m forward uniform happ om oe nobl rdown lpoint "Don't make me text five reminders."
    mc "I would never."
    m forward uniform wry cm ce nobl rdown ldown "You absolutely would, by needing them."
    mc "Correct, albeit awfully cruel wording..."
    # SFX SUGGESTION: A distant warning bell that gently breaks the rooftop quiet.
    "Somewhere below us a bell goes, and the roof stops belonging to us."
    "Monika stands first and I follow suit."
    m "Okay! Let's get back before we're written up as runaways."
    mc "Reasonable."
    m "Occasionally."
    "She pauses near the door."
    m forward uniform nerv om oe awkw rdown ldown "Thanks."
    mc "For...saying yes?"
    m forward uniform neut cm oe blus rdown ldown "For not making me make it smaller."
    "That one takes the air out of my joke before it forms."
    mc "...Yeah."
    mc "No problem."
    show monika at thide
    hide monika
    play sound moddoorclose
    "The rooftop goes back to wind and concrete, with no man or woman in sight."
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
    math_teacher "Matrices are not decorative boxes."
    math_teacher "Instead, they are a way to organize operations. To some, it's easier. Some, harder."
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
            mc "Yes. The inside dimensions match, so the result takes the outside dimensions."
            mc "Two by two."
            math_teacher "Correct."
            "He circles the three and three in the middle, then boxes the two and two on the outside."
            "{i}A sentence simple enough to make this coming Monday feel a little less hostile.{/i}"
        "Yes. The result is three by three.":
            $ atmos_pressure_clear()
            with dissolve
            mc "Yes. Three by three."
            "The board stares back."
            "The two and two sit outside the expression like they are waiting for me to stop embarrassing both of us."
            math_teacher "Not quite."
            math_teacher "Inside confirms compatibility. Outside gives the result. Two by two."
            math_teacher "Do not average the sizes, do not guess by vibes, and do not let panic do arithmetic."
            "{i}Panic is not a reliable calculator. Duly noted.{/i}"
        "No. The dimensions do not match.":
            $ atmos_pressure_clear()
            with dissolve
            mc "No. They don't match."
            math_teacher "Check again."
            "Two by three times three by two."
            "The middle dimensions match."
            math_teacher "Inside confirms compatibility. Outside gives the result. Two by two."
            "{i}Nearly taken out by a bracket. Not my proudest moment.{/i}"
    math_teacher "Now BA."
    "The board receives a second set of arrows."
    math_teacher "Order matters."
    math_teacher "AB and BA are not guaranteed to have the same size, the same value, or even both exist."
    "{i}Order matters. Math has social boundaries too.{/i}"
    "He writes a multiplication table step by step."
    "Row times column. Row one, column one. Row one, column two. Then repeat."
    "It is so unbearably tedious that I can't help but put my hand on my chin and rest my elbow on my desk."
    math_teacher "Midterm expectation: you must show the setup."
    math_teacher "If I see a correct answer with no path, I cannot tell whether you actually understood it or rolled lucky dice."
    math_teacher "Now, I'm not usually one to make something all-or-nothing, but the whole point of exams is to show comprehension and maybe some problem solving skills."
    "The class practices three examples."
    "By the third, someone near the windows asks whether calculators will be allowed and receives a look normally reserved for betrayal."
    math_teacher "For this one, yes. Calculators can help you multiply larger numbers or decimals, but they cannot save you from entering the wrong structure."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Algebra finishes with a review sheet heavy enough to change the weather in my binder. English hands back vocabulary sheets, because Saturday apparently has no interest in staying light."
    nier "The school day ends with one more announcement about pencils and the moral necessity of sleeping before an exam."
    nier "By the final bell, the school feels less like a building and more like a machine ejecting dead students into the weekend."
    call nier_clear from _call_nier_clear_0524_3
    stop music fadeout 1.0
    pause 2.0
    scene bg club_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music daily
    "The club room is warmer than usual when I arrive -- not physically, though the afternoon sun does its best."
    "A few members are already here, notebooks open and chairs pulled into loose corners, but the room is holding a not-so-rare quiet."
    show monika forward uniform happ cm oe nobl rdown ldown at t11
    "Monika stands near the board, writing the prompt in clean letters."
    "{i}Write about a place that holds still while you don't.{/i}"
    "She turns when she hears the door."
    m forward uniform happ om oe nobl rdown ldown "Yo."
    mc "Hey."
    "I take my usual seat and pull out my notebook. The desk has a tiny nick near the corner that my thumb finds before my brain does."
    "Same desk, same room, shifted by half an inch."
    m forward uniform happ cm oe nobl rhip ldown "I figured we could keep it low pressure today."
    m forward uniform happ om oe nobl rhip lpoint "Fifteen minutes drafting, then voluntary exchange. Rapid-fire poetry and all that."
    m "And actually voluntary this time. Everyone looks tired enough that forcing feedback would just get everyone defensive."
    "Everyone lowers into writing. For a while, there is only paper noise."
    "Someone near the back erases a line so hard the page wrinkles."
    "He writes steadily, pauses, crosses out exactly three words, and keeps going."
    "I stare at the prompt longer than I should."
    "The obvious answer is school."
    "The smarter answer is not to write the obvious answer if I don't want to sound like a backhanded motivational poster."
    "And the even smarter answer is to circle back to the obvious answer to never let Monika know my next move."
    "My pen moves before I fully decide. The bus arrives first, then the window, then the seat."
    call enter_m_showpoem(poem_0524_mc_draft) from _call_enter_m_showpoem_0524_1
    "I look at the lines."
    "{i}Not exactly the cheerful version of exam-week pressure, then.{/i}"
    m forward uniform curi om oe nobl rhip ldown "You stopped..."
    mc "For now, now stop hovering."
    m forward uniform happ cm ce nobl rhip ldown "What'd I say about getting defensive...?"
    mc "It probably was. Can't do my best with a hawk on my shoulder."
    # SFX SUGGESTION: A short, neutral timer buzz from Monika's phone.
    "Monika stands and brings her notebook to my desk once the timer on her phone buzzes."
    show monika forward uniform happ cm oe nobl rdown ldown at t11
    "{i}So much for the meaning of voluntary.{/i}"
    m forward uniform happ om oe nobl rdown ldown "Trade?"
    mc "As always."
    "We swap notebooks in an indiscrete fashion."
    "Her handwriting is neater than mine even when she is drafting. The title is crossed out, and under it, a new one sits in smaller letters."
    "I read."
    call enter_m_showpoem(poem_0524_monika) from _call_enter_m_showpoem_0524_2
    "I stop reading for a second."
    "Around me, nothing changes."
    "A page turns somewhere behind us. Someone asks a raspy question about whether a line is too blunt, and the answer comes back just as quietly."
    "Monika sits across from me and reads six lines without hurrying."
    "It should be easy to say something, yet it is not."
    mc "This is..."
    "Her eyes lift."
    m forward uniform worr om oe nobl rdown ldown "Too much?"
    mc "No, not at all."
    mc "No, it's good. A bit specific and on the nose, but I like it."
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
    m "But the bus seat remembers nobody line is strong."
    "Her finger hovers near the page without touching it."
    m forward uniform neut cm oe nobl rhip ldown "It says something honest without explaining itself to death."
    m forward uniform curi om oe nobl rdown lpoint "So don't ruin it."
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
    "She reads over my shoulder, close enough that I can feel her attention before I see her reaction."
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
    "I stay quiet with pressed lips into the inside of my mouth."
    "Monika presses the back of one hand to her cheek and tries to regain presidential authority from somewhere under the desk."
    m forward uniform flus cm oe blaw rhip lpoint "All right, new rule."
    m "No commenting on other people's feedback...for like five minutes!"
    mc "I'd say that's a perfectly reasonable rule."
    m forward uniform wry cm ce blaw rdown ldown "Thank you."
    "She looks at me first. It works, which is annoying."
    mc "...Understood."
    "For the next half hour, club actually becomes club."
    "A few people trade drafts and a few keep writing alone."
    "Monika gives notes, takes notes, and only glances at me twice."
    "...Maybe three times. In times like these, I stop myself from counting."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Club ends gently. The poems remain small, unfinished things, and this is one of the very few media where that's allowed."
    call nier_clear from _call_nier_clear_0524_4
    pause 2.0
    scene bg club_day
    $ show_calendar()
    $ atmos("evening")
    show monika forward uniform happ cm oe nobl rdown ldown at t11
    with wipeleft_scene
    "The room is almost empty when Monika stacks the last loose paper."
    m forward uniform nerv om oe awkw rdown ldown "Sorry about earlier, didn't mean for...whatever that awkward moment was."
    mc "It wasn't that bad, I've been through worse."
    m "Still..."
    mc "The club noticed a thing and moved on. You know how people are."
    m forward uniform flus om ce blaw rdown ldown "Still embarrassing, though..."
    "She slides her notebook into her bag before physically and mentally pivoting."
    m forward uniform nerv om oe blus rhip ldown "Anyway! Tomorrow at nine, then?"
    mc "Tomorrow at nine. Green awning near the old bank."
    m forward uniform curi om oe nobl rdown ldown "Oh hey, you remembered~"
    mc "Oh don't be like that, I have my moments."
    m forward uniform happ cm oe nobl rdown ldown "Yes, you do..."
    "Her words are simple enough that I have to look away."
    m forward uniform happ cm ce nobl rdown ldown "See you tomorrow, [player]!"
    mc "Catch ya later."
    show monika at thide
    hide monika
    window hide
    pause 2.0
    window auto
    mc "..."
    mc "Heh."
    "I leave while the goodbye is still light enough to carry."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The trip home is quiet. A Saturday evening does not owe me more than that."
    nier "My bag carries review sheets, my notebook carries eight lines about a bus seat, and my planner carries tomorrow like a small lit window."
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
    mc "Yeah, pretty much sums it up."
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
    mc "I have money, don't worry."
    mom "Okay, perfect, not the same as a budget."
    show mom unamused
    "She gives me the look."
    mc "...I will bring cash and not spend it like crazy."
    show mom smug
    mom "Beautiful. I'm touched to hear that."
    show mom happy
    "A snigger gets out of me sideways while Mom smiles, fatigued but present."
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
    nier "Asahina comes down long enough to steal a glass of water, deny she was on a call, and vanish again, all of it faster than a follow-up question."
    nier "The house holds together in small domestic pieces and Mom's pen scratching once before going still."
    call nier_clear from _call_nier_clear_0524_6
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music fantasypassion
    "Night finally gives my room back."
    "My desk is a negotiation between responsibility and everything else."
    "On one side: review sheets, calculator, literature notes, a pencil that has been sharpened into a weapon against my hand."
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
            phone_msg("them", "Sleep at a reasonable time, okay?"),
            phone_msg("me", "Look who's talking."),
            phone_msg("them", "I said reasonable, not early. Two different things."),
            phone_msg("me", "Fine. See you at nine."),
            phone_msg("them", "See you at nine, " + player + "."),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0524_2
    "I drop whatever is in my hands onto the blanket before submitting to my console."
    "My game loads with a low choir, a broken city skyline, and a title screen that looks like it was designed by someone who believes menus should have existential consequences."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The game is about a city sealed under a false sky after a ritual goes wrong."
    nier "Combat runs on a momentum system where hitting weaknesses grants extra turns and missing lets enemies punish the entire party."
    nier "Every time I lose, I call it bad luck. At the same time, every win is a display of pure skill."
    call nier_clear from _call_nier_clear_0524_7
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    "My party is currently in the subway underpass, which has become a cathedral for reasons the game has not yet explained and probably will explain later with great seriousness."
    "A horned bureaucrat blocks the ticket gates."
    "\"State your alignment preference,\" it says, despite the fact that I only wanted to find a save point."
    mc "...My alignment preference is tired."
    "The game does not accept tired as an answer."
    "I choose the neutral response, because committing to cosmic ideology before bed feels wrong."
    "The bureaucrat approves, takes half my money as a processing fee, and joins my party."
    "{i}Unbelievable...{/i}"
    "The next encounter nearly wipes me because I forget that lightning skills reflect off one enemy and healing magic costs more than my current dignity can afford."
    "Annoying, but absorbing just enough to keep me in the fray."
    "For twenty minutes, midterms become numbers in a game instead of numbers on a schedule. The library becomes a marker on tomorrow instead of a thing to overthink."
    "I save twice because I have learned from pain, then I sit for a moment with the controller in my lap."
    "My room has gone properly still. The game music loops softly through the speakers, patient and ominous."
    "{i}Monday can wait outside for one more night.{/i}"
    "I turn the console off before the next dungeon can make a liar out of my bedtime."
    $ update_character_thought("sam", "Sam fixed Asahina's sleeve cuff before she noticed it was folded, and had Tsubaki read in about thirty seconds. Neither is a bad thing to be able to do.")
    $ update_character_thought("tsubaki", "Tsubaki's step caught for half a beat when Sam used her surname. I have no idea what that was.")
    $ hide_calendar()
    scene black with wipeleft_scene
    call nier_clear from _call_nier_clear_0524_8
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0524_1
    jump a0525
