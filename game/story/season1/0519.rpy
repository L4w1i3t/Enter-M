label a0519:
    # --- Day 5: 2025-05-19 ---
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music house_day_a
    # SFX SUGGESTION: A phone alarm that repeats insistently rather than stopping after one ring.
    "The alarm goes off at a responsible hour, and I ignore it until that stops being an option. My phone buzzes against the nightstand like it already knows it'll win."
    "I drag it off the charger and squint at a screen brighter than anything else at this hour."
    python:
        _phone_messages = [
            phone_msg("them", "Okay. Official ruling from the horror committee: the rod was the promise AND the weapon!"),
            phone_msg("them", "I slept on it. The thesis survived the night."),
            phone_msg("me", "It's seven. How long have you been awake?"),
            phone_msg("them", "Long enough to find the shot you were talking about."),
            phone_msg("me", "So I was right about the poster?"),
            phone_msg("them", "Yes! I'll show you at lunch, when we're both awake."),
            phone_msg("me", "Good. I'm not taking a symbolism exam from bed."),
            phone_msg("them", "I'll save the footnotes, then. See you at school!"),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0519_1
    "I let the phone rest on the blanket until I can keep my eyes open, then scroll up to the photo from yesterday. With the brightness turned down, I can look at it without squinting."
    "{i}Could've asked if she wanted to do something next Sunday. I did say I'd get the next one.{/i}"
    "I leave that for when we're both awake and notice Matsuda's name below the thread."
    # Saturday's introduction texts are already in the thread. Matsuda still
    # initiates the next sustained conversation, and its phone unlock, on 0520.
    "{i}Still owe her that review too.{/i}"
    "Her last message is the demand that I lie about the game. I type 'tutorial's good,' then delete it when I notice the time."
    "We've met once. Seven in the morning seems early to start testing the contact privileges."
    "The game case is still sitting menacingly beside the console, with my ridiculous rules tucked inside. Eighty hours, supposedly, and I've finished two."
    "I peel the blanket off and put my foot on the floor, testing it before I stand."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "By the time I've washed and pulled my uniform on, the toaster has gone off twice downstairs. I follow the smell before Asahina takes the good slices."
    call nier_clear from _call_nier_clear_0519_1
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    show asahina uniform unamused at t11
    "Asahina is already in uniform, eating toast with one hand while she props her head up on the other."
    ah "Morning, fossil."
    mc "It's too early for that. Give me until coffee."
    show asahina uniform teasing
    ah "Nope. It's a lifestyle."
    "I pull the chair out so I can sit without twisting my foot. It's better than last week, but today will be my first day outside without the athletic tape."
    ah "Still gimpy?"
    mc "Recovering. Huge difference there."
    ah "Right, right... When are they letting you run again?"
    mc "Coach checks it this week. Hopefully I can do something before my body gets too rusty."
    ah "Start with walking. You've been using the furniture for corners."
    mc "Mate, you do volleyball. You could at least show a little solidarity."
    show asahina uniform smug
    ah "I could, yeah, but then you'd think I was being nice."
    ah "Besides, you're slow with two good feet, so maybe you're just physically a ret--{w=1.0}{nw}"
    mc "ALRIGHT, I take it back! Eat your toast and shove it."
    "The floor creaks under Mom on her way in."
    show asahina uniform neut at t21
    show mom uniform happy at l22
    "She's dressed for the office, travel mug in one hand, the other tucking a folder into her bag."
    mom "Morning, you two."
    ah "Morning."
    mc "Morning..."
    show mom uniform curious
    mom "[player], small thing. Did you ever circle back to that school I showed you last week?"
    "The printout is still beside the fruit bowl, right where she put it last night."
    mc "I, uh, opened the page."
    show mom uniform unamused
    mom "Opened the page..."
    mc "I read the course list. Didn't get much further."
    show mom uniform smug
    mom "Gotcha. Now, I'm not nagging, but I {i}am{/i} establishing a paper trail for when I do."
    mc "...Am I allowed a lawyer for this?"
    show mom uniform neut
    mom "After you've read it properly. Half an hour together this week should get us started."
    mc "...Yeah. Okay. This week."
    "I reach for the toast before she can ask me to pick a day."
    show mom uniform determined
    "Mom looks at me, still burning me with her retinas."
    mom "This week."
    show mom uniform neut
    "I nod with my mouth full, and she goes back to fastening her bag."
    show asahina uniform unamused
    ah "Put it on his phone. That got him to buy stuff for me."
    mc "Okay, I'm not {i}that{/i} bad. I'd have remembered even without the verbal warning."
    "By the time I look at the microwave clock, I need to leave. I finish the toast and take the hardboiled egg for the road."
    mc "I'm heading out. Save me a bit of that bread for lunch tomorrow."
    show asahina uniform smug
    ah "No promises, gimpy."
    show mom uniform happy
    mom "Have a good day. And don't push yourself just because you feel better."
    "{i}First day without tape. I'll settle for getting home without needing it.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The dog two houses down objects to my leaving, although it lets the woman ahead of me pass without comment. I finish my egg at the bus stop."
    nier "When the bus comes, I find a window seat and rest my bag on my knees. There is nothing I need to answer until school."
    nier "A shopkeeper wheels a rack of umbrellas onto the pavement as we pass. I watch him check the sky before the bus turns the corner."
    call nier_clear from _call_nier_clear_0519_2
    stop music fadeout 1.0
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with dissolve_scene_full
    play music quiz
    "Civics is already underway by the time my brain accepts that the weekend is over."
    "The board has three examples under a heading about public action. I've copied two before the teacher starts explaining the third."
    show civics_teacher neut at t11
    civics_teacher "We're looking at a criticism often called performative virtue, also known as virtue signaling: displaying support for a cause while doing little to advance it."
    civics_teacher "Be careful with the claim. A public statement can be useful, and these examples don't let us read anyone's private motives."
    "The guy beside me turns to a fresh page, sighs, and goes back to finish his last sentence."
    civics_teacher "If someone donates to a relief fund and tells others to encourage more donations, that public statement may serve a practical purpose."
    civics_teacher "In the second example here, the poster promises to share shelter information, then refuses requests for it and reposts only the praise they receive."
    "I add the promised information beside the second example. Leaving that out would make a different question."
    civics_teacher "Now, quick attention check."
    "The chalk stops."
    civics_teacher "[player]."
    mc "...Yeah?"
    civics_teacher "Which example on the board gives us the strongest evidence that the display has replaced the promised work?"
    $ atmos_pressure()
    with dissolve
    menu:
        "Donating covertly to a local shelter.":
            jump civics_wronganswer1
        "Posting a slogan, then withholding the promised shelter information.":
            jump civics_rightanswer1
        "Organizing volunteers after talking about the issue.":
            jump civics_wronganswer1
    label civics_rightanswer1:
        $ atmos_pressure_clear()
        with dissolve
        civics_teacher "Correct."
        civics_teacher "Yes. We have a promised action and repeated chances to do it, followed by a refusal. That's stronger evidence than publicity alone."
        "The teacher circles {i}display{/i} and {i}substance{/i} on the board."
        jump civics_answer1done
    label civics_wronganswer1:
        $ atmos_pressure_clear()
        with dissolve
        civics_teacher "Not quite."
        civics_teacher "Quiet donation is action without display. Organizing volunteers is public, but it still produces practical results."
        civics_teacher "In the post example, the person refuses requests for the information they promised. That's the evidence we need to examine."
        mc "Right... yeah. That makes sense."
        jump civics_answer1done
    label civics_answer1done:
        pass
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "By the time the bell rings, my notebook contains half a page of actually useful notes and a rhythm-game character sketched in the margin."
    call nier_clear from _call_nier_clear_0519_3
    stop music fadeout 1.0
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with wipeleft_scene
    play music school_day_a
    "Lunch finds me in the hallway, because the cafeteria has developed its own brand of acoustic warfare and I am not qualified to survive it."
    "I've claimed a stretch of wall near the windows, food balanced on one hand, when Monika finds me."
    show monika forward uniform happ cm oe nobl rdown ldown at t11
    m forward uniform happ om oe nobl rdown lpoint "Found you! I've got the poster comparison."
    mc "You did that already? Let me see."
    "She settles against the wall beside me, balancing her bread in its wrapper while she turns her phone toward us."
    m forward uniform happ om oe nobl rhip ldown "It's weird, though. The old one doesn't have the hand."
    mc "...Huh."
    m forward uniform curi om oe nobl rhip ldown "I know! I'm glad you stopped looking."
    mc "You can barely see it though... Maybe it's just my eyes."
    "She enlarges the picture again, then checks the clock and puts her phone away."
    show monika forward uniform happ om oe rdown ldown
    m forward uniform happ om oe rdown ldown "Anyway, no club today. Council's taken the afternoon, and probably some of my evening."
    mc "What've they given you this time?"
    m forward uniform happ om ce rdown ldown "Budget forms. So, SO many budget forms... The same ones I gave back Friday because nobody filled in the totals."
    mc "Sounds like the horror committee's day job."
    m forward uniform anno om oe rdown ldown "Please don't, I'm barely keeping that bit together as is."
    m forward uniform wry cm oe rhip ldown "Honestly, council's been a lot lately. Everyone wants a yes, and nobody wants to read the form that makes the yes possible."
    mc "So you're the one who ends up reading everything."
    m forward uniform anno om oe rhip ldown "AND sends them back. I'm getting very good at thanking people for reading things they haven't read."
    # The first open crack is annoyance, not sadness; her pause and reset below
    # need something real to follow.
    m lpoint "I wrote instructions right beside the empty boxes. Right there!"
    m "I'm not saying that everyone around me is incompetent or a bonehead, but... that's exactly what it is. Like, holy hell, give me a break!"
    "She rubs her temples and draws out her sigh."
    m ldown"...Sorry. I'm still mad about it."
    show monika cm
    "She takes a bite, then has to brush flour off the front of her skirt."
    m forward uniform happ om oe nobl rdown ldown "Anyway! Not your circus."
    m "You've got track climbing back onto your schedule any day now. The club's already bracing to share you again."
    mc "Assuming the foot signs off on it."
    m "Oh, you'll get back there. Just don't rush it because you're bored."
    mc "I'll try. Are you... doing okay, though?"
    show monika forward uniform dist cm oe nobl rdown ldown
    m forward uniform wry om oe nobl rdown ldown "Always."
    show monika forward uniform dist cm oe nobl rdown ldown
    "She folds the wrapper over the rest of her bread, although she has only eaten half."
    mc "...Want company on the way home? I can wait a bit."
    m forward uniform neut om oe nobl rdown ldown "Thanks, but I don't know when I'll get out. Go enjoy the afternoon for both of us."
    "If she needs something, she has my number. I finish my last bite while she checks a message, and the halfway bell rings as she types away with one hand."
    show monika forward uniform happ cm oe nobl rdown ldown
    m forward uniform happ om ce nobl rdown lpoint "I'll text you the footnotes when I get out. Something to look forward to!"
    mc "My one true reward."
    m forward uniform happ cm ce nobl rdown ldown "Try to contain your excitement until at least fifth period~"
    m "I got something to tend to, so I'll, uh, see you around!"
    mc "Yeah, totally. Take care."
    show monika at thide
    hide monika
    "She gets the clipboard out of her bag as she joins a few passing students. I stay by the wall until there is room to put my food away."
    "Further down the hall, Matsuda is telling a story to a cluster of students by the stairs, with Tsubaki standing beside her."
    "She plucks at invisible strings across her bag, then sweeps one arm wide for a bow and catches her elbow on the banister. Tsubaki moves the bag at her feet while the group laughs."
    "Matsuda doesn't look my way, and the group closes the gap before I decide whether to say hello."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The afternoon classes pass in the usual blur of people watching the clock harder than they watch the board."
    nier "By foreign language, I've poked a hole through the middle of my eraser. I turn it over to hide the damage while we compare the two translations on the board."
    call nier_clear from _call_nier_clear_0519_4
    stop music fadeout 1.0
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music day_a
    "After school, I keep to the side of the hallway, one hand on my bag strap and the other hovering near my pocket."
    "With club not happening and all my other daily side quests done, I could get home while the house is still empty."
    "{i}I might actually escape cleanly.{/i}"
    show matsuda uniform happy at l11
    stop music fadeout 1.0
    ma "Make way! Make way for the Ballad of the Boy Who Could Not Watch Where He Was Going!"
    "The announcement reaches me before Matsuda does, rising onto a note she holds all the way around the corner."
    "{i}Never mind. She found me.{/i}"
    mc "...Hey, Matsuda."
    play music theme_matsuda_a
    # May 19: bard, distinct from Saturday's courtly traveler. She composes,
    # recites, and courts an audience until MC's chosen response lowers the act.
    "She crooks one arm across her bag and plucks imaginary strings with the other, setting a brisk walking beat."
    ma "He wandered forth with lowered gaze; his games lay wrapped for better days!"
    mc "I opened it yesterday. You'll have to rewrite that."
    show matsuda smug
    ma "A fresh verse! Blessings upon the muse, who brings corrections before the first performance has even finished!"
    "She falls into step beside me like we planned this."
    "A couple students glance over, yet Matsuda does not lower her voice."
    show matsuda curious
    ma "Tell me, hero of the broken seal: did you triumph, did you fall, did you lose an entire evening and eat nothing at all?"
    mc "I only got through the opening couple hours. Combat's good, though."
    show matsuda unamused
    ma "Good?! My chorus cannot subsist on {i}good{/i}! Give me a catastrophe, a betrayal, a boss who crushed your hopes beneath one extravagantly armored foot!"
    mc "I lost the first fight. Does that help?"
    show matsuda happy
    ma "Immensely! A tragic opening, followed by a stirring rise! Unless you lost again, in which case I shall need a longer song."
    mc "Are you always like this after school?"
    show matsuda smug
    ma "Only when I have material. You, my fortunate friend, have supplied an entire cycle!"
    "She lifts a hand to cue an audience behind me. When I glance around, there are two people trying to get to the stairs."
    ma "And now, good people, join me in the--"
    menu:
        "\"Okay, stop.\"":
            $ s1_pick("matsuda_stop", "blunt")
            mc "Okay, stop."
            show matsuda shocked
            "It comes out flatter than I meant it to."
            "Matsuda freezes with her hand still raised for the chorus. The two students pass behind me without joining in."
            show matsuda neut
            mc "Sorry, just... can you not do the bard thing for five seconds?"
            mc "I'm not mad. It's just a lot, okay?"
        "\"Take it down about forty percent?\"":
            $ s1_pick("matsuda_stop", "gentle")
            mc "Could you take it down, like, forty percent?"
            show matsuda curious
            ma "Forty is oddly specific."
            mc "Thirty-five, then. I'm negotiable."
            "Her hand comes down, leaving the two passing students free of their apparent chorus duties."
            show matsuda unamused
            mc "It's not bad. It's just a lot, and Mondays give me enough headaches."
            show matsuda neut
        "(Ride it out.)":
            $ s1_pick("matsuda_stop", "endure")
            "I let her finish."
            show matsuda happy
            ma "--chorus! His heart was stout, his phone held low, and straight into a lass did he go!"
            "She holds the last note while I wait for a gap, keeping her hand raised even as the passing students continue toward the stairs."
            mc "...Sorry. You lost me already."
            show matsuda neut
            "The raised hand comes down on its own."
    ma unamused "..."
    ma "...Not a fan of the bard, huh?"
    ma neut "Fine. To-tally fine. The vihuela goes back in its case."
    "She mimes putting the instrument away, then lets her arms hang at her sides. When she speaks again, I don't have to hear her over her own echo."
    ma "Better?"
    mc "...Yeah. Thanks."
    "Matsuda draws her shoulders in as another group passes us, then looks back at me before continuing."
    ma curious "I wanted to ask you more about that game. I'm still on the fence."
    mc "On the fence, but upset you couldn't snag a copy on release day?"
    ma unamused "Don't lampshade me, man! It is I who does the lampshading!"
    mc "Okay, fine, geez... What do you want to know?"
    ma thinking "Well, first off... The demo kept slowing me down with tutorials. PLEASE tell me it stops doing that."
    mc "After the opening, yeah. You can skip the tips, too."
    show matsuda uniform frustrated
    ma "Whyyyyyyy was that not in the demo? I read the sword explanation three times cause apparently {i}some{/i} people are too stupid to swing a metal stick!"
    mc "I dunno, maybe you kept talking over it. And way to self-report."
    show matsuda uniform teasing
    ma "I was offering feedback! The man needed an editor!"
    mc "I mean, I personally robbed his house after he grew on me."
    ma "Oh, as did I. Lovely rugs."
    "She grins, and I find myself slowing down so the conversation can keep up with us."
    mc "The combat feels much snappier than the demo. I've only met two party members, but I already want to know what one of them's hiding 'cause his design looks awfully NPC-like."
    show matsuda happy
    ma "Then sing, my purse, your last lament, for every coin shall soon be--"
    show matsuda unamused
    "Her fingers twitch toward the imaginary strings before she catches herself and clears her throat."
    ma "...Sorry. Force of habit."
    mc "I think that one was fine."
    show matsuda happy
    "She smiles without lifting her hands this time."
    ma "Aha! Good to know."
    ma curious "Should I document the approved volume settings?"
    mc "Please don't make a spreadsheet about me."
    ma teasing "Right. A field guide, then."
    mc "..."
    show matsuda neut
    ma "Anyway, I'm going to see if the store has a copy. If not, I'll have to try again tomorrow."
    mc "They had a few left when I got mine. Can't say anything after that though, that was a couple days ago."
    show matsuda teasing
    ma "Wish me luck. I refuse to end this ballad with 'out of stock' yet again."
    "I snort."
    show matsuda happy
    ma "That being said, I shall spare you the closing verse."
    mc "Uh huh..."
    show matsuda at thide
    hide matsuda
    "She slips between two groups, then turns back to see whether I'm coming."
    ma "Come on, then! Tell me about that party member before we part!"
    "{i}And you're certain you're not a theater kid?{/i}"
    "I'm going that way anyway. I follow her as far as the front door, where she wants to know which party member I meant because frankly, both designs rub me the wrong way."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "We part outside after I describe the party member without giving anything away. She gets halfway down the outdoor steps before calling back that my description gave everything away, to my disappointment of nothing being a mystery."
    call nier_clear from _call_nier_clear_0519_5
    stop music fadeout 1.0
    pause 2.0
    scene bg dining_table_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music night_a
    "Dinner is grilled fish with the usual rice and soup. Mom has also cleared out whichever vegetables were losing their lease in the fridge."
    "The table feels calmer than it did yesterday, as nobody has interrogated me about a movie date yet."
    show asahina neut at t21
    show mom neut at t22
    mom "So how was school?"
    mc "Long. The bus home took forever, too."
    show asahina teasing
    ah "You got stuck by the roadworks too?"
    mc "Yeah. Watched the same cyclist pass us three times."
    mom "Any homework?"
    mc "Civics notes, reading, and twenty math problems I should've started earlier."
    show asahina unamused
    ah "Sounds like a you problem. Glad it's not mine."
    mom "Don't forget the poster tomorrow, by the way."
    show asahina smug
    "Asahina points toward the front hall with a spoon."
    mom "And you, [player]? Anything interesting happen?"
    "Matsuda's hallway entrance replays itself with all the subtlety it lacked in person."
    mc "Not really. The usual scene, y'know?"
    show asahina smug
    ah "Naaah, I saw you talking to that one girl when I was headed to practice!"
    mc "...Then why didn't you say hello?"
    ah "'Cause you looked EXTREMELY preoccupied."
    mc "Okay, yeah, cool, I ran into an acquaintance. That's it. Get off my case. Please."
    show asahina curious
    ah "The acquaintance from Saturday?"
    mc "YES, the one from Saturday! That's the one you saw me talking to."
    show asahina happy
    "She puts her chopsticks down so she can turn toward Mom."
    ah "Ohhhh, sidewalk traffic strikes again."
    mom "Sidewalk traffic?"
    ah "He crashed into her Saturday and came home with her number! Now she's finding him at school."
    mc "She wanted to ask about a game! That's all it was!"
    mc "Could you mind your own damn business for once?! Like holy crap, can I just go ONE second without you wanting to know every aspect of my freaking life?!"
    show asahina angry
    show mom unamused
    ah "I was just--"
    ah sad "...Okay."
    "She looks back down at her plate."
    ah "...Fine."
    mom "Someone from your grade?"
    mom determined "That's all I'm asking. You don't need to say anything else about it."
    mc "...Yeah, she transferred in this year. We're not in the same class."
    "I reach for the rice while Mom asks how far away she lives."
    "{i}'That's all I'm asking.' So that was a lie.{/i}"
    mc "Nearby, I think. We met around the corner, so it's gotta be around here somewhere."
    mom neut "Well, if she ever comes over, give me a little more notice than your sister did~"
    mc "Fat chance, but okay. God, you two are giving me ulcers by the day."
    show mom angry at h22
    mom "Okay, you've been an ass since coming back downstairs. Either cut it out or go into the other room."
    show asahina neut
    "Dinner settles once everyone returns to behavior more acceptable by social standards."
    show mom determined
    show asahina neut
    "Mom talks about a coworker who keeps leaving empty containers in the shared fridge. Asahina complains about tomorrow's serving drills, then demonstrates with her chopsticks."
    "I move my water before she catches it with her elbow."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Homework takes the narrow gap between dinner and free time, and longer than I will ever admit out loud."
    nier "Then the evening hands itself over to me: unstructured, a little too quiet."
    call nier_clear from _call_nier_clear_0519_6
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music night_b
    "I turn on the console once everything else is put away. The older RPG still has a boss I haven't beaten, and I want to settle that before starting another long stretch of the new one."
    "An hour goes into beating a boss who keeps raising his evasion. When I finally land the attack that finishes him, I take a screenshot before he can disappear."
    "Eventually I set the controller down and reach for my phone."
    "Monika's message has been sitting there for twenty minutes. She's finally out of council."
    python:
        _phone_messages = [
            phone_msg("them", "The footnotes, as promised."),
            phone_msg("them", "Footnote one: see this morning, but louder and with more conviction."),
            phone_msg("them", "Footnote two: upon further reflection, the gas station clerk was the true villain, and I won't be taking questions at this time."),
            phone_msg("me", "Riveting scholarship."),
            phone_msg("them", "I know. Don't tell the committee I peaked on a Monday~"),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0519_2
    "Matsuda's thread catches my eye before I power down for the night. The last message is still Saturday's terrible review."
    "I could ask if she found a copy, but after a minute, I put my phone on charge without typing anything."
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0519_1
    jump a0520
