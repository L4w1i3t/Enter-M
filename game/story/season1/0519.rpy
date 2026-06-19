label a0519:
    # --- Day 5: 2025-05-19 ---
    scene bg bedroom
    $ show_calendar()
    show mood_home zorder 3
    with dissolve_scene_full
    play music dailyleisure
    window auto
    "The alarm goes off at the responsible hour, and I meet it the way I meet most responsible things -- by ignoring it until ignoring it stops being an option."
    "The ceiling offers no new information. I offer it none back. We have an understanding."
    "My phone is awake before I am, buzzing against the nightstand with the smug persistence of something that already knows it'll win."
    "I drag it off the charger and squint at a screen brighter than anything has a right to be at this hour."
    python:
        _phone_messages = [
            phone_msg("them", "Okay. Official ruling from the horror committee: the iron rod was the promise AND the weapon. I've decided I contain multitudes."),
            phone_msg("them", "I slept on it. The thesis survived the night."),
            phone_msg("me", "It's seven in the morning."),
            phone_msg("them", "Symbolism doesn't keep office hours, [player]."),
            phone_msg("me", "Clearly neither do you."),
            phone_msg("them", "I'll spare you the footnotes until we're both at least vertical. See you at school!"),
            phone_msg("me", "Can't wait for the footnotes."),
            phone_msg("them", "Liar. But I'll allow it~"),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0519_1
    "I let the phone drop onto the blanket and stare at the ceiling for one second longer than the morning can afford."
    "The movie was yesterday. The theory texts apparently never got the memo that it ended."
    "{i}She grabbed my sleeve in the tunnel scene. Not my hand. My sleeve.{/i}"
    "{i}I'm choosing not to have a relationship with that piece of information this early in the day.{/i}"
    "I thumb out of the thread, and the contacts list catches on a name I still haven't done anything about."
    # SEED (for 0520): Matsuda's contact has sat unused since the Saturday collision (0517), and 0518's night narration already flagged it "renting space." Kept unopened here so SHE initiates the first real text thread on 0520.
    "{i}Matsuda Akai.{/i} Saved Saturday, parked in my phone ever since like it signed a lease I don't remember approving."
    "I open the empty thread. The cursor blinks at me. I have absolutely nothing to put in front of it, so I close it again."
    "{i}Later. Later being a word I use to mean never, with extra steps.{/i}"
    "The new game sits by the console where I left it Saturday night, still mostly unplayed -- the launch I'd spent weeks counting down to, now just another thing waiting patiently for me to earn it."
    "{i}I keep treating it like a reward and never quite doing the part that would make it one. There's probably a word for that. I'd rather not look it up.{/i}"
    "I peel the blanket off, test the foot against the floor, and decide it can be Monday now whether or not I'm ready to ratify the decision."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I drag myself through the usual rituals -- uniform, teeth, a doomed negotiation with my hair -- and head down toward the smell of something Asahina has almost certainly already eaten most of."
    call nier_clear from _call_nier_clear_0519_1
    scene bg kitchen
    $ show_calendar()
    show mood_home zorder 3
    with wipeleft_scene
    show asahina neut at t11
    "Asahina is at the counter, already in uniform, working through a piece of toast with the focus of someone who deeply resents being conscious."
    ah "Morning, fossil."
    mc "It's too early for the fossil bit."
    ah "It's never too early. That's what makes it art."
    "I lower myself into a chair a little more carefully than I'd like to admit, and my foot files a brief, formal complaint about the stairs I just came down."
    "It's better than it was last week. It is not yet what I'd generously call cooperative."
    ah "Still gimpy?"
    mc "Recovering. There's a difference."
    ah "Right. Gimpy, but with a growth mindset."
    mc "Coach is supposed to look at it before he lets me back on the track. Probably this week."
    ah "So you've been nursing a sad little limp with no practice to even skip. What's the point of an injury you can't weaponize?"
    mc "I contain depths you will never understand, Asa."
    ah "I understand you're slow now. Like, medically."
    "She says it around the last of her toast, which robs the insult of roughly none of its commitment."
    "The floor creaks mom into the room before she gets the chance to announce herself."
    show asahina neut at t21
    show mom neut at t22
    "She's dressed for the office but moving at the unhurried pace of a Monday that hasn't gone wrong yet -- travel mug in one hand, the other tucking a folder into her bag."
    mom "Morning, you two."
    ah "Morning."
    mc "Morning."
    mom "[player], small thing. Did you ever circle back to that school I showed you last week?"
    "The printout. Glass courtyard, grass too green to be real, one program highlighted in yellow that I'd have circled myself if I were braver about admitting I'd already looked it up."
    "{i}So that's a no.{/i}"
    mc "I, uh, opened the page."
    mom "Opened the page."
    mc "It's a step in the process."
    mom "It's the first step. There are traditionally several after it."
    "She says it without heat, in the tone she saves for things she fully intends to circle back to."
    mom "I'm not nagging. I'm establishing a paper trail for when I do."
    mc "Counselor mom strikes again."
    mom "Always. Look it over properly this week, and we'll dig in together. Half an hour, no pressure, just looking at it like adults."
    mc "...Yeah. Okay. This week."
    "It comes out agreeable enough to sound like a plan and vague enough to stay one in name only."
    "Mom holds my eye a half second past the comfortable mark, the way she does when she's quietly filing something for later reference."
    mom "This week."
    "She repeats it lighter, then lets it go, which from her counts as mercy."
    ah "He's gonna forget by lunch."
    mc "I resent the precision of that."
    "I get maybe three bites into my own breakfast before the clock on the microwave starts making threats I'm legally obligated to take seriously."
    mc "Anyway, I'm out. Try not to set anything on fire that isn't already scheduled to burn."
    ah "No promises, gimpy."
    mom "Have a good day. Ice the foot if it earns it."
    mc "It hasn't earned a thing in its life."
    show asahina at thide
    hide asahina
    show mom at thide
    hide mom
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The walk to the station is the same as it always is: same cracked curb, same dog two houses down that hates me specifically and personally, same bus that arrives precisely when it feels like arriving."
    nier "My foot holds up fine at a walking pace, a fact it makes a great show of advertising right up until I have to take a stair two at a time and it changes its mind."
    nier "I get a window seat, which on a morning bus is about the closest thing to winning available to a person my age."
    nier "The glass turns the city into something I can watch without being expected to answer it -- storefronts, a man losing an argument with a vending machine, a row of identical umbrellas waiting for rain the sky hasn't committed to yet."
    nier "I don't think about the highlighted program, or the unanswered name in my phone, or the foot. I let the window do the thinking for me until the school stop arrives and takes the seat back."
    call nier_clear from _call_nier_clear_0519_2
    scene bg class_day
    $ show_calendar()
    show mood_afternoon zorder 3
    stop music fadeout 1.0
    with dissolve_scene_full
    play music quiz
    window auto
    "Monday enters the room wearing fluorescent lights and a lecture schedule."
    "Civics is already underway by the time my brain accepts that the weekend is over."
    "The teacher has written {i}PUBLIC VIRTUE{/i} on the board, then underlined it hard enough to threaten the chalk."
    show civics_teacher neut at t11
    # CRITIQUE (ADDRESSED): Dropped the loaded real-world phrase "virtue signaling" for "performative virtue" / "public moral performance," keeping the theme without the discourse baggage. Also gave MC a sharper, personal reaction below -- tying performance-vs-substance to Matsuda AND to himself -- instead of a textbook gloss.
    civics_teacher "Today's term is performative virtue. You'll also hear it called public moral performance."
    civics_teacher "At its simplest: a public display of values done for social approval rather than for the thing the values are supposed to be about."
    civics_teacher "The tricky part is that public moral expression is not automatically dishonest."
    "A few pens move. A few faces communicate the same desperate hope that this will not become an essay prompt."
    civics_teacher "If someone donates to a relief fund and tells others to encourage more donations, that public statement may serve a practical purpose."
    civics_teacher "If someone posts a slogan, receives praise, and treats the praise as the accomplishment, the action becomes more performative."
    "{i}So: caring about looking like you care, more than caring.{/i}"
    "{i}I think about a red ponytail addressing a hallway like it's a balcony. Then I think about myself, underselling a movie I actually liked so nobody clocks that I liked it.{/i}"
    "{i}Different costumes. Same fitting room.{/i}"
    "I write the phrase down anyway, despite knowing it front to back."
    civics_teacher "Now, quick check."
    "The chalk stops."
    "I make the catastrophic mistake of looking at the board right when the teacher turns around."
    civics_teacher "[player]."
    mc "...Yeah?"
    civics_teacher "Which example here is the clearest case of performative virtue?"
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
    call nier_clear from _call_nier_clear_0519_3
    scene bg corridor
    $ show_calendar()
    show mood_afternoon zorder 3
    stop music fadeout 1.0
    with wipeleft_scene
    play music schooldays
    "Lunch finds me in the hallway, which is a generous way of saying I'm avoiding the cafeteria and its particular brand of acoustic warfare."
    "I've claimed a stretch of wall near the windows, lunch balanced on one hand, when a familiar voice arrives a half second ahead of its owner."
    show monika 1a at t11
    m "There he is. The man who survived a horror movie and lived to underrate it."
    mc "I rated it accurately. 'I liked it' is a complete sentence."
    m "It's a coward's sentence, but I'll allow it."
    "She settles against the wall a polite distance away, unwrapping something that is mostly bread doing an impression of lunch."
    m "I won't keep the committee in session, don't worry. I mostly came to confirm you survived staying up to validate my theories."
    mc "I didn't stay up. I went to sleep at a perfectly reasonable hour, like a person with a future."
    m "Your face is testifying against you as we speak."
    mc "My face says a lot of things it can't back up."
    "She studies me a beat longer than the joke earns, then lets it go, which I appreciate more than I'd say out loud."
    "There's still a faint smell of cinnamon on my fingers that no amount of washing has fully convinced to leave. Neither of us mentions the popcorn. Some crimes are better left unprosecuted."
    m "Anyway. No club today -- I've got a student council thing after school that's going to eat me alive and pick its teeth with what's left."
    mc "Define 'thing.'"
    m "Budget forms. So, so many budget forms. The kind that multiply when you look away from them."
    mc "Sounds like the horror committee's day job."
    m "Don't. I'm barely holding that metaphor together as it is."
    show monika 1d at t11
    "She says it lightly, but there's a tiredness underneath it the smile doesn't quite reach -- the look of someone running three jobs and pretending two of them are hobbies."
    m "Honestly, council's been a lot lately. Everyone wants a yes, and nobody wants to read the form that makes the yes possible."
    mc "Sounds lonely."
    m "It's not lonely. It's just...a lot of being the person who remembers things so the other people don't have to."
    "She catches herself, and the brightness flips back on like a light left ready for company."
    m "Anyway! Not your circus. And you've got track climbing back onto your schedule any day now -- the club's already bracing to share you again."
    mc "Assuming the foot signs off on it."
    m "It will. You're too stubborn to let it not."
    mc "...You good?"
    m "Always."
    "It lands a beat too quickly to fully believe, but the warning bell rings before either of us has to do anything about it."
    show monika 1a at t11
    m "Go on. Eat your sad little hallway lunch. I'll text you the footnotes."
    mc "My one true reward."
    m "Try to contain your excitement until at least fifth period~"
    show monika at thide
    hide monika
    "She peels off into the current of bodies, clipboard already materializing in one hand like she summoned it."
    "Further down the hall, near the stairwell, a red ponytail is holding court over a cluster of students, arms wide enough to suggest the story requires a full wingspan to land."
    "A quieter girl stands just inside the blast radius, a paper bag held against her chest, smiling at something only she seems to find funny."
    "{i}Matsuda. Of course.{/i}"
    "Whatever she's performing requires her to mime drawing a sword and then, a beat later, visibly regret it. The cluster laughs. The quiet girl mouths a small correction the rest of them miss entirely."
    "She doesn't see me. I decide, with the cowardice of a man holding a lunch, to keep it that way."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The afternoon classes pass in the usual blur of people watching the clock harder than they watch the board."
    nier "Somewhere in there I finish my lunch, fail to retain a single fact about agricultural reform, and watch the windows do their slow shift from white to gold."
    call nier_clear from _call_nier_clear_0519_4
    scene bg corridor
    $ show_calendar()
    show mood_afternoon zorder 3
    stop music fadeout 1.0
    with wipeleft_scene
    play music dailyfantasy
    "After school, the hallway becomes its usual disaster of bodies, bags, half-finished conversations, and people stopping in the exact worst places."
    "I keep to the side, one hand on my bag strap and the other hovering near my phone."
    "No club announcement, no errand list, no emergency glue acquisition."
    "{i}For once, I might actually escape cleanly.{/i}"
    show matsuda neut at t11
    stop music fadeout 1.0
    ma "Lo! If it is not the wanderer of weekend roads, returned from his nocturnal collision with destiny!"
    "The sentence hits me before Matsuda fully enters my line of sight."
    "{i}Never mind. Destiny has a hallway ambush mechanic.{/i}"
    mc "...Hey, Matsuda."
    play music enterm
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
    # CRITIQUE (ADDRESSED / MODEL): This boundary scene is exactly the target -- MC sets a limit, Matsuda drops the bard, and a real person shows underneath. Left intact and treated as the template for her dosage everywhere else (the wince at her debut, the plain register on May 23).
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
    "Without the performance filling the space, Matsuda looks slightly smaller -- not embarrassed exactly, more like someone waiting to see whether the floor is stable."
    ma "So, I wanted to also ask about that one game more because I'm still on the fence about it."
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
    # CRITIQUE (ADDRESSED): Expanded the too-abrupt summary to name what was refreshing -- not that Matsuda got quieter, but that MC asked her to and was allowed to leave on his own time. It also banks the clean version of a respected boundary, so its later erosion has a baseline to be measured against.
    nier "The trip home is refreshing in a way I have to sit with for a second to name."
    nier "It isn't that Matsuda got quieter. It's that I asked her to, and she did, and the sky stayed up."
    nier "I told someone the volume was too much, and instead of a fight or a sulk, I just...got to go. On my own time."
    nier "{i}I wish all Mondays could be like this.{/i}"
    call nier_clear from _call_nier_clear_0519_5
    stop music fadeout 1.0
    scene bg kitchen
    $ show_calendar()
    show mood_home zorder 3
    with wipeleft_scene
    # MUSIC FIX: the busy/public "daily" track from the after-school corridor was bleeding straight into the calm home dinner. Switched to fantasypassion (calm/wistful home) here, which also underscores the quiet isolation beat at the table.
    play music fantasypassion
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
    ah "Sounds like a you problem."
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
    # CRITIQUE (ADDRESSED): Kept the pile-on affectionate but gave MC a private beat of feeling exposed (below) -- the low-grade discomfort of being the subject of a table you're sitting at, his day narrated back by people who weren't there. A small isolation seed, filed under "nothing" in his usual way.
    mom "Sidewalk traffic?"
    mc "No."

    ah "He crashed into a girl Saturday and got her number."
    mc "Contact info. The difference matters."
    # CRITIQUE (ADDRESSED): Cut the popularity dig (it aimed straight at Asahina's actual social insecurity) and let MC register the overstep instead -- her grin flickers, he clocks it, walks it back. A small repair beat rather than a casually mean line the narration ignores.
    mc "And maybe mind your own business for once, motormouth."
    "It comes out with more edge than I meant. Asahina's grin flickers, just for a second, before she patches it back over."
    "{i}Too far. Recalibrate.{/i}"
    mc "...That was uncalled for. Sorry."
    ah "Pfft. Lucky you're cute, loser."
    mom "...{i}Does{/i} it matter?"
    mc "You two... I am being ganked in my own home."

    ah "Technically mom owns it."

    "I stare at my soup as if it might defend me, much to my dismay."
    "It's all in good fun. It is. Mostly."
    "There's just a specific, low-grade feeling to being the subject of a table you're sitting at -- watching your own day get narrated back to you by people who weren't there for it."
    "I file it under 'nothing,' the way I file most things, and reach for more rice."
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
    nier "Homework happens in the narrow gap between dinner and free time, in the five-minutes-that-felt-like-it way it always does when I refuse to look directly at how long it actually took."
    nier "Then the evening hands itself over to me -- unstructured, a little too quiet -- and I do with it exactly what I always do with unstructured and quiet."
    call nier_clear from _call_nier_clear_0519_6
    scene bg bedroom
    $ show_calendar()
    show mood_night zorder 3
    stop music fadeout 1.0
    with wipeleft_scene
    play music fantasyserenity
    "My room at night is a small economy of glowing rectangles: the game on the console, the phone on the desk, each quietly competing for the same finite resource, which is me."
    "I start with the game, because it's the one I can at least pretend is a hobby with edges."
    "It's the JRPG I've been grinding through with about fifteen self-imposed restrictions, most of which exist purely so I can feel something when I break them."
    "An hour evaporates the way it does when nothing is technically wrong. Numbers go up. A boss that has personally wronged me is made to answer for it."
    "A responsible amount of time later -- by my own famously generous accounting -- I set the controller down and reach for the phone instead, which is where my evenings tend to go to quietly come apart."
    "It buzzes the moment I pick it up, like it was waiting. Monika, making good on a threat she issued twice in one day."
    python:
        _phone_messages = [
            phone_msg("them", "The footnotes, as promised."),
            phone_msg("them", "Footnote one: the rod is the promise. Footnote two: see footnote one, but louder and with more conviction."),
            phone_msg("them", "Footnote three: upon further reflection, the gas station clerk was the true monster, and I will not be taking questions at this time."),
            phone_msg("me", "Riveting scholarship."),
            phone_msg("them", "I know. Don't tell the committee I peaked on a Monday~"),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0519_2
    "I huff out something that is almost a laugh and set the phone face-up on the desk."
    "Then I pick it back up maybe thirty seconds later, for no reason I could defend in a court of law, and that's all it ever takes."
    # SEED (for 0522): the autoplay/doomscroll slide that detonates as the May 22 oversleep. Tonight he still catches it -- the habit is forming, not yet costing him. The "file it under nothing" ledger note links to the same line on 0515 / 0522.
    "A video plays. The next one starts on its own, because at some point the app quietly decided I no longer get a vote in the matter."
    "It's a man explaining how to properly sharpen a knife. I do not own a knife worth the effort. I watch the whole thing."
    "The one after that is about deep-sea fish that make their own light. The one after that, I genuinely could not tell you anything about, including whether I was awake for it."
    "This is the part no one warns you about -- not the decision to keep watching, because there isn't one, but the absence of any decision to stop, stretched out long enough that it starts to resemble a choice I made on purpose."
    "Outside, the windows have gone full mirror, the street below long since handed over to streetlights and the occasional car pretending it has somewhere to be."
    "At some point I surface long enough to notice the clock has traveled considerably further than I authorized."
    "{i}Okay. That's enough of that.{/i}"
    "I make myself stop, which tonight is still something I'm capable of doing."
    "I notice that I had to make myself, which is the part I don't love. I file it under nothing, the way I file most things, and turn the phone face-down."
    "Before the screen dies, the contact list surfaces that name one more time. Still there. Still unanswered."
    "{i}Matsuda Akai. Day three of paying rent on a conversation that hasn't started.{/i}"
    "I think about texting her. I think about it the way I think about most things -- thoroughly, and then not at all."
    "{i}Tomorrow, maybe.{/i}"
    "{i}She'll probably beat me to it. People like her always do.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Sleep comes easier than it has any real right to, all things considered."
    nier "Tomorrow, Coach decides whether the foot has done enough recovering to earn its way back onto the track. The club will want its half of me regardless, the moment there's a half to give."
    nier "For tonight, Monday is content to simply be over, and for once, so am I."
    call nier_clear from _call_nier_clear_0519_7
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0519_1
    jump a0520
