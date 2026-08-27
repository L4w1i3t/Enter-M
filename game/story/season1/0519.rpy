label a0519:
    # --- Day 5: 2025-05-19 ---
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music dailyleisure
    window auto
    # SFX SUGGESTION: A phone alarm that repeats insistently rather than stopping after one ring.
    "The alarm goes off at the responsible hour, and I meet it the way I meet most responsible things: by ignoring it until that's no longer an option. My phone buzzes against the nightstand like it already knows it'll win."
    "I drag it off the charger and squint at a screen brighter than anything else at this hour."
    python:
        _phone_messages = [
            phone_msg("them", "Okay. Official ruling from the horror committee: the rod was the promise AND the weapon!"),
            phone_msg("them", "I slept on it. The thesis survived the night."),
            phone_msg("me", "It's seven in the morning, mate."),
            phone_msg("them", "Symbolism doesn't keep office hours, [player]."),
            phone_msg("me", "Clearly neither do you."),
            phone_msg("them", "I'll spare you the footnotes until we're both at least vertical. See you at school!"),
            phone_msg("me", "Can't wait for you to talk my ear off..."),
            phone_msg("them", "Liar. But I'll allow it~"),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0519_1
    "I let the phone fall onto the blanket and stare at the ceiling while my eyes keep trying to close."
    "{i}She grabbed my sleeve in the tunnel. That's...new.{/i}"
    "{i}Nope. That fact can file for consideration later.{/i}"
    "I drag the rectangle of death back into view and thumb out of the thread. The contacts list catches on a name I still haven't done anything about."
    # SEED (for 0520): Matsuda's contact has sat unused since the Saturday collision (0517), and 0518's night narration already flagged it "renting space." Kept unopened here so SHE initiates the first real text thread on 0520.
    "{i}Matsuda Akai. Saved Saturday, untouched since.{/i}"
    "{i}Technically I did say yes, but it was like a 'no' kind of yes.{/i}"
    "I open the empty thread. The cursor blinks with all the patient menace of an unfinished form."
    "Nothing arrives, so I close it."
    "{i}Later. Later being a word I use to mean never, just politely.{/i}"
    "The new game sits by the console where I left it Saturday night, still mostly unplayed but at least unsealed. The reported average playthrough takes eighty hours."
    "The launch I'd spent weeks counting down to, now just another thing waiting patiently to earn my time."
    "I peel the blanket off and test the ol' foot against the floor. It accepts, so Monday can begin."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I drag myself through the usual rituals. By the time my uniform is on and my hair has won its argument, downstairs smells like something Asahina has almost certainly eaten most of."
    call nier_clear from _call_nier_clear_0519_1
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    show asahina uniform unamused at t11
    "My sister is at the table, already in uniform, working through a piece of toast like it personally arranged for her to be awake."
    ah "Morning, fossil."
    mc "It's too early for that. Give me until coffee."
    show asahina uniform teasing
    ah "It's never too early. That's what makes it art."
    "I lower myself into a chair more carefully than I'd like to admit. The foot that blew a gasket a month ago files a brief, formal complaint about the stairs."
    "It's better than last week, but not what I'd generously call cooperative. Today is my first day outside without athletic tape, so this is where the real game begins."
    ah "Still gimpy?"
    mc "Recovering. Huge difference there."
    ah "Right. Gimpy, but with...what's that term Mom always uses...a growth mindset."
    mc "Ah ah, you stuttered, doesn't count."
    mc "Coach is supposed to look at it before he lets me back on the track. Probably sometime this week."
    ah "So you've been nursing a sad little limp with no practice to even skip. What's the point of an injury you can't weaponize?"
    mc "You do volleyball. You of all people should understand."
    show asahina uniform smug
    ah "I understand you're slow now. Physically, I mean."
    ah "The other category was already covered, ya friggin' ret--{w=1.0}{nw}"
    mc "ALRIGHT! Point made! Geez."
    "The floor creaks Mom into the room before she gets the chance to announce herself."
    show asahina uniform neut at t21
    show mom uniform happy at l22
    "She's dressed for the office but moving at the unhurried pace of a Monday that hasn't gone wrong yet, travel mug in one hand, the other tucking a folder into her bag."
    mom "Morning, you two."
    ah "Morning."
    mc "Morning..."
    show mom uniform curious
    mom "[player], small thing. Did you ever circle back to that school I showed you last week?"
    "The printout."
    "{i}So that's a no.{/i}"
    mc "I, uh, opened the page."
    show mom uniform unamused
    mom "Opened the page..."
    mc "It's...it's progress."
    show mom uniform teasing
    mom "It's the first step. There are traditionally several after it."
    show mom uniform smug
    mom "I'm not nagging, but I {i}am{/i} establishing a paper trail for when I do."
    mc "Counselor Mom strikes again..."
    show mom uniform neut
    mom "Always. Look it over properly this week, and we'll dig in together."
    mom "Half an hour, no pressure. We'll look at it like adults."
    mc "...Yeah. Okay. This week."
    "It sounds like a plan. I make sure it isn't one."
    show mom uniform determined
    "Mom holds my eye a half second past the comfortable mark."
    mom "This week."
    show mom uniform neut
    "She repeats it lighter, then lets it go, which from her counts as mercy."
    show asahina uniform unamused
    ah "He's gonna forget by lunch."
    mc "I...resent the precision of that."
    "I get maybe three bites into breakfast before the microwave clock starts making threats. I take the hardboiled egg for the road and call that a meal on a technicality."
    mc "Anyway, I'm out. Try not to set anything on fire that isn't already scheduled to burn."
    show asahina uniform smug
    ah "No promises, gimpy."
    show mom uniform happy
    mom "Have a good day. Ice your foot if it earns it."
    "{i}It hasn't earned a thing in its entire life.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The walk to the station offers no surprises. The dog two houses down still hates me specifically and personally."
    nier "The bus arrives on its own schedule. I get a window seat, which is about the closest thing to winning available on a weekday morning."
    nier "The glass turns the city into something I can watch without being expected to answer it."
    nier "Storefronts slide past while a man loses an argument with a vending machine. A rack of identical umbrellas waits for rain the sky has not committed to yet."
    nier "I let the window do the thinking for me until the school stop arrives and takes the seat back."
    call nier_clear from _call_nier_clear_0519_2
    stop music fadeout 1.0
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with dissolve_scene_full
    play music quiz
    window auto
    "Monday officially enters the room wearing fluorescent lights and a lecture schedule."
    "Civics is already underway by the time my brain accepts that the weekend is over."
    "The teacher has written two annoying words on the board, then underlined them until the chalk started giving up."
    show civics_teacher neut at t11
    civics_teacher "Today's term is performative virtue. You'll also hear it called public moral performance or even virtue signaling."
    civics_teacher "At its simplest: a public display of values done for social approval rather than for the thing the values are supposed to be about."
    civics_teacher "Now, the tricky part here is that public moral expression is not automatically dishonest."
    civics_teacher "People are rarely operating from one motive at a time."
    "A few pens move. A few faces communicate the same desperate hope that this will not become an essay prompt."
    civics_teacher "If someone donates to a relief fund and tells others to encourage more donations, that public statement may serve a practical purpose."
    civics_teacher "But if someone posts a slogan and treats the resulting praise as the accomplishment, the action becomes more performative."
    "I write the phrase down anyway, even though I know it already."
    civics_teacher "Now, quick attention check."
    "The chalk stops."
    civics_teacher "[player]."
    mc "...Yeah?"
    civics_teacher "Which example here is the clearest case of performative virtue or virtue signaling?"
    $ atmos_pressure()
    with dissolve
    menu:
        "Donating covertly to a local shelter.":
            jump civics_wronganswer1
        "Making a post to spread awareness without actionability.":
            jump civics_rightanswer1
        "Organizing volunteers after talking about the issue.":
            jump civics_wronganswer1
    label civics_rightanswer1:
        $ atmos_pressure_clear()
        with dissolve
        civics_teacher "Correct."
        civics_teacher "The issue is not that the person spoke publicly. The issue is that the public display replaced the substance."
        "The teacher circles {i}display{/i} and {i}substance{/i} on the board."
        jump civics_answer1done
    label civics_wronganswer1:
        $ atmos_pressure_clear()
        with dissolve
        civics_teacher "Not quite."
        civics_teacher "Quiet donation is action without display. Organizing volunteers is public, but it still produces practical results."
        civics_teacher "This post example here is the clearest one because the display replaces the action."
        mc "Right...yeah. That makes sense."
        jump civics_answer1done
    label civics_answer1done:
        pass
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "By the time the bell rings, my notebook contains half a page of useful notes and a rhythm-game character sketched in the margin."
    call nier_clear from _call_nier_clear_0519_3
    stop music fadeout 1.0
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with wipeleft_scene
    play music schooldays
    "Lunch finds me in the hallway, because the cafeteria has developed its own brand of acoustic warfare and I am not qualified to survive it."
    "I've claimed a stretch of wall near the windows, food balanced on one hand, when Monika finds me."
    show monika forward uniform happ cm oe nobl rdown ldown at t11
    m forward uniform happ om oe nobl rdown lpoint "There he is! The man who survived a horror movie and lived to underrate it."
    mc "I rated it accurately. 'I liked it' is a complete sentence."
    m forward uniform happ cm ce nobl rdown ldown "It's a coward's sentence, but...alright."
    "She checks the hallway clock before settling against the wall a polite distance away. She takes another bite of something that is mostly bread doing an impression of lunch."
    m forward uniform happ om oe nobl rhip ldown "I won't keep the committee in session, don't worry. I mostly came to confirm you survived staying up to validate my theories."
    mc "I didn't stay up. I went to sleep at a perfectly reasonable hour, like a person with a future."
    m forward uniform curi om oe nobl rhip ldown "Your face is testifying against you as we speak."
    mc "Yeah, well, my face says a lot of things it can't back up."
    "She studies me a beat longer than the joke earns, then lets it go."
    show monika forward uniform happ om oe awkw rdown ldown
    m forward uniform happ om oe awkw rdown ldown "Anyway, no club today. I've got a student council thing after school that's going to eat me alive and pick its teeth with what's left."
    mc "Define 'thing.'"
    m forward uniform happ om ce n2 rdown ldown "Budget forms. So, SO many budget forms. So many they stack up the moment you look away."
    mc "Sounds like the horror committee's day job."
    m forward uniform nerv om oe awkw rdown ldown "Don't... I'm barely holding that anecdote together as is."
    m forward uniform wry cm oe nobl rhip ldown "Honestly, council's been a lot lately. Everyone wants a yes, and nobody wants to read the form that makes the yes possible."
    mc "Sounds lonely."
    m forward uniform worr om oe nobl rhip ldown "Kinda? Not really? It's just...a lot of being the person who remembers things so the other people don't have to."
    # The first open crack is annoyance, not sadness; her pause and reset below
    # need something real to follow.
    m forward uniform anno cm oe nobl rhip ldown "It's not that everyone else is a bonehead. It's just..."
    m forward uniform anno om oe nobl rhip ldown "...Some days, that is exactly what it is."
    show monika forward uniform happ om oe nobl rdown ldown
    "She closes her eyes once, then straightens and returns her voice to its usual bright register."
    m forward uniform happ om oe nobl rdown ldown "Anyway! Not your circus."
    m forward uniform happ om oe nobl rdown ldown "You've got track climbing back onto your schedule any day now. The club's already bracing to share you again."
    mc "Assuming the foot signs off on it."
    m "It will. You're too stubborn to let it not."
    mc "..."
    mc "...Are you good?"
    show monika forward uniform dist cm oe nobl rdown ldown
    m forward uniform dist cm oe nobl rdown ldown "Always."
    "The answer arrives before the question has finished settling. I keep looking at her until she lowers her eyes to the bread wrapper."
    mc "That's not what I asked."
    "Her thumb smooths a crease that is already flat. Her eyes return to the hallway clock."
    # SFX SUGGESTION: A school warning bell cutting cleanly across the unfinished moment.
    "The halfway bell rings a moment later. Monika folds the wrapper and pushes off the wall."
    show monika forward uniform happ cm oe nobl rdown ldown
    m forward uniform happ om ce nobl rdown lpoint "Go eat your sad little hallway lunch. I'll text you the footnotes."
    mc "My one true reward."
    m forward uniform happ cm ce nobl rdown ldown "Try to contain your excitement until at least fifth period~"
    show monika at thide
    hide monika
    "She peels off into the current of bodies, clipboard already materializing in one hand like she summoned it."
    "Further down the hall, near the stairwell, a red ponytail is holding court over a cluster of students, arms out at full wingspan because modest gestures have evidently been outlawed."
    "A quieter girl stands just inside the blast radius, smiling at something only she seems to find funny."
    "Whatever she's performing requires her to mime drawing a sword and then visibly regret it. The cluster laughs while the quiet girl mouths a small correction the rest of them miss entirely."
    "She doesn't see me. I protect my rations and keep it that way."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The afternoon classes pass in the usual blur of people watching the clock harder than they watch the board."
    nier "Somewhere in there, I put holes in my eraser and fail to retain a single fact about agricultural reform. The windows shift slowly from white to whitish-gold."
    call nier_clear from _call_nier_clear_0519_4
    stop music fadeout 1.0
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music dailyfantasy
    "After school, I keep to the side of the hallway, one hand on my bag strap and the other hovering near my pocket."
    "No club announcement or errand list. Absolutely no emergency acquisition side quests."
    "{i}I might actually escape cleanly.{/i}"
    show matsuda uniform happy at l11
    stop music fadeout 1.0
    ma "Lo! If it is not the wanderer of weekend roads, returned from his nocturnal collision with destiny!"
    "The sentence hits me before Matsuda fully enters my line of sight."
    "{i}Nevermind, then. Destiny has a hallway ambush mechanic.{/i}"
    mc "...Hey, Matsuda."
    play music enterm
    # Keep May 17's bright performance register until the player sets a boundary.
    ma "Hail, [player]! Survivor of shoulder-borne calamity! Witness to my radiant entrance upon the stage of your otherwise modest life!"
    mc "That's a lot before hello."
    show matsuda smug
    ma "Hello is a small door. I prefer a balcony and the occasional drawbridge upon entering stage left."
    "She falls into step beside me like we planned this, which we absolutely did not."
    "A couple students glance over. Matsuda does not lower her voice, because lowering her voice would imply privacy."
    show matsuda curious
    ma "Tell me, good sir, did the fabled game disappoint as requested? Or did it seize your evening and drag you through lands of digital peril?"
    mc "It was fine."
    show matsuda unamused
    ma "Fine? A word so pale it should be studied by physicians."
    mc "...Okay, it was fun."
    show matsuda happy
    ma "Ah, color returns to the patient! I was beginning to fear the monochrome."
    mc "Are you always like this after school?"
    show matsuda smug
    ma "Whenever school will tolerate me. At select municipal events, too."
    ma "I contain multitudes, my good--"
    menu:
        "\"Okay, stop.\"":
            $ s1_pick("matsuda_stop", "blunt")
            mc "Okay, stop."
            show matsuda shocked
            "It comes out flatter than I meant it to."
            "Matsuda freezes mid-gesture, one hand still lifted like she was about to address a balcony that does not exist."
            show matsuda neut
            mc "Sorry, just...can you not do the bard thing for five seconds?"
            mc "I'm not mad. It's just a lot."
        "\"Take it down about forty percent?\"":
            $ s1_pick("matsuda_stop", "gentle")
            mc "Could you take it down, like, forty percent?"
            show matsuda curious
            ma "Forty is oddly specific."
            mc "Thirty-five, then. I'm negotiable."
            "The hand she had raised toward a balcony that does not exist comes down."
            show matsuda unamused
            mc "It's not bad. It's just a lot, and Mondays give me enough headaches."
            show matsuda neut
        "(Ride it out.)":
            $ s1_pick("matsuda_stop", "endure")
            "I let her finish."
            show matsuda happy
            ma "--chum!"
            "She waits for an equal response. I have never generated that much wattage on purpose."
            mc "...Sorry. You lost me already."
            show matsuda neut
            "The raised hand comes down on its own."
    ma unamused "..."
    ma "...Not a fan of the bard, huh?"
    ma neut "Fine, fine. Between you and me, he is gone."
    "She draws both hands down over her face. When they fall, so does the stage voice."
    ma "Better?"
    mc "...Yeah. Thanks."
    "The hallway keeps moving around us. Without the performance filling the space, Matsuda's shoulders draw in."
    "She studies my face before she goes on."
    ma curious "I wanted to ask you more about that game. I'm still on the fence."
    ma thinking "Also, you seem like you'd undersell something you enjoyed to avoid sounding excited."
    mc "That's a...weirdly specific accusation."
    show matsuda uniform pose_shrug
    ma "Am I wrong?"
    mc "...No."
    show matsuda uniform teasing
    ma "Then I accept your apology."
    mc "I didn't apologize???"
    ma "Spiritually, you did."
    "There she is again, but quieter. Manageable, at the very least."
    mc "It's good. The combat feels better than the demo, and the story's doing that thing where it pretends to be simple before showing a knife."
    show matsuda happy
    ma "Ah, most excellent! My wallet shall suffer the hellborne wrath of--"
    show matsuda unamused
    "She catches the flourish halfway out of her mouth and clears her throat."
    ma "...Sorry. Force of habit."
    mc "That one was fine."
    show matsuda happy
    "Her smile returns without Saturday's stage lights."
    ma "Good to know."
    show matsuda neut
    ma "Anyway. I'm heading to the store before it closes."
    mc "...The store's open until nine."
    show matsuda teasing
    ma "Then I'm heading there slowly and with purpose."
    "I snort."
    show matsuda happy
    ma "Until next time, [player]!"
    mc "Later."
    show matsuda at thide
    hide matsuda
    "She slips into the crowd, less like a spotlight this time and more like someone who knows where all the exits are."
    ma "After me, my lad!"
    "{i}And you're certain you're not a theater kid?{/i}"
    "Seeing as how I have no pressing concerns, I follow suit. At least, that is until the front door."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I asked Matsuda to dial it down. She actually did, and what felt like twenty years later she verbally contorted into a different persona entirely."
    call nier_clear from _call_nier_clear_0519_5
    stop music fadeout 1.0
    pause 2.0
    scene bg dining_table_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music fantasypassion
    "Dinner is grilled fish with the usual rice and soup. Mom has also cleared out whichever vegetables were losing their lease in the fridge."
    "The table feels calmer than it did yesterday. Nobody interrogates me about a movie date before I have finished sitting down."
    show asahina neut at t21
    show mom neut at t22
    mom "How was school?"
    mc "It was...it was school."
    show asahina teasing
    ah "That means boring, right?"
    mc "'Least it's accurate."
    mom "Any homework?"
    mc "Some civics notes and a reading thing. Also twenty math problems due tomorrow."
    show asahina unamused
    ah "Sounds like a you problem."
    mom "The poster looked very nice, by the way."
    show asahina embarrassed
    "Asahina focuses very hard on her rice."
    ah "Eh, it was whatever."
    mom "And you, [player]? Anything interesting happen?"
    "Matsuda's hallway entrance replays itself with all the subtlety it lacked in person."
    mc "Not really. The usual scene, y'know?"
    show asahina smug
    ah "Liar, liar, plants for hire."
    mc "...Excuse me?"
    ah "That's your 'not really' voice. Very different from your real not-really voice."
    mc "I ran into an acquaintance. That's it, seriously, so get off my case."
    show asahina curious
    ah "With...?"
    mc "Matsuda, okay?! Happy?!"
    show asahina happy
    "Asahina's chopsticks abandon their mission."
    ah "Ohhhh, sidewalk traffic strikes again."
    mom "Sidewalk traffic?"
    ah "He crashed into a girl Saturday and got her number."
    mc "Contact info. The difference matters, though you wouldn't know it if it hit you in that empty drum you call a head."
    mc "And maybe mind your own business for once, ya motormouth."
    show asahina sad
    "I hear the edge half a second after it leaves. Asahina's grin flickers before she patches it back over."
    mc "...That was cheap. Sorry."
    ah smug "Pfft. Lucky you're not some stranger, loser."
    mom "...{i}Does{/i} it matter?"
    mom smug "Tell me more..."
    mc "You two... I'm being ganked in my own home."
    ah "Technically Mom owns it."
    "I stare at my soup. It declines representation."
    "Being discussed at a table you're sitting at has a specific, low-grade humiliation to it. I bury it under 'nothing' and reach for more rice."
    mom "Well, as long as everyone is being respectful and nobody is actually getting hurt, I think casual conversations are allowed."
    show asahina teasing
    ah "That's boring. There's gotta be some drama or dirt."
    mom "I can make it more embarrassing if you'd prefer. What about that one time you were flirting with that one boy in elementary school?"
    show asahina embarrassed
    ah "...I retract my statement."
    show asahina neut
    "Dinner settles after that."
    "Mom talks about a coworker who labels food in the shared fridge but never brings anything worth stealing. Asahina complains about volleyball practice without meaning a word of it."
    "I eat while their voices make the day small again."
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
    play music fantasyserenity
    "My room at night is a small economy of glowing screens, each quietly competing for the same finite resource, which is me."
    "I start with the old game on my console, the JRPG I've been grinding through under a pile of rules nobody asked me to invent."
    "An hour evaporates the way it does when nothing is technically wrong. Numbers go up and a boss that has personally wronged me by maxing out his evasion is made to answer for it."
    "Eventually I set the controller down and reach for my phone, where evenings go to quietly come apart."
    # SFX SUGGESTION: A single phone notification buzz, unnaturally well-timed after the pickup.
    "It buzzes the moment I pick it up, like it was waiting. Monika, making good on a threat she issued twice in one day."
    python:
        _phone_messages = [
            phone_msg("them", "The footnotes, as promised."),
            phone_msg("them", "Footnote one: see this morning, but louder and with more conviction."),
            phone_msg("them", "Footnote two: upon further reflection, the gas station clerk was the true villain, and I won't be taking questions at this time."),
            phone_msg("me", "Riveting scholarship."),
            phone_msg("them", "I know. Don't tell the committee I peaked on a Monday~"),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0519_2
    "I huff out something close to a laugh and set the phone face-up on the desk. Thirty seconds later, I pick it back up."
    "A video plays, followed by another that starts on its own. The app has quietly decided I no longer get a vote in the matter."
    "It's a man explaining how to properly sharpen a knife. I do not own a knife worth the effort, yet I watch the whole thing."
    "Doomscrolling barely feels like a decision. It's the absence of stopping, stretched out until it can pass for one."
    "Outside, the windows have gone full mirror and the street below belongs to the lamps. Every so often, a car with a loud-ass muffler pretends it has somewhere urgent to be."
    "At some point I surface, and the clock has traveled a lot further than it had any business traveling."
    "{i}That's enough of that, then.{/i}"
    "I make myself stop and turn the phone facedown."
    "Before I lock it, my thumb finds the contacts list again. Matsuda's thread is still empty."
    "I consider texting her with great thoroughness, then don't."
    "{i}Tomorrow, maybe.{/i}"
    "{i}She'll probably beat me to it. People like her always do.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Sleep comes easier, all things considered."
    nier "Tomorrow, Coach decides whether my foot is ready to return to the track. The club will want its half of me either way, the moment there's a half to give."
    nier "For tonight, Monday is content to simply be over, and so am I."
    call nier_clear from _call_nier_clear_0519_7
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0519_1
    jump a0520
