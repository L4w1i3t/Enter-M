# Gates the one-time "Evening." gag in the showtime menu so a curious player
# cannot spam the thread with it. A `default` rather than an underscore-prefixed
# temp because the menu condition has to survive a save made at that menu.
default a0518_evening_joked = False


label a0518:
    # --- Day 4: 2025-05-18 ---
    pause 2.0
    scene bg living_room
    show asahina frustrated at t11
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music house_day_a
    ah "Ugggh, why is there nothing good on?!"
    "My sister attacks the channel button like the TV started it."
    show asahina annoyed
    ah "Why did the Geographic have to have downtime now of all times?!"
    mc "You could put a film on. We own a few."
    show asahina smug
    ah "I would, if you'd give me back my DVD of 'The Grandfather.'"
    mc "...I have no idea what you're talking about."
    ah "You've had it for two weeks, which is longer than the actual rental places let you have things!"
    "I remain silent with a long sip of coffee."
    "{i}Tastes awfully thick...{/i}"
    "The channel lands on a cooking show, holds for four seconds, and moves on."
    show asahina unamused
    ah "There are ninety channels, and half of them are selling the same blender."
    mc "And yet you probably watched two of those channels."
    ah "It was crushing a phone! I wanted to see if it'd actually do it, m'kay?"
    mc "Well, did it?"
    show asahina smug
    ah "Yeah. So don't tell me I wasted my morning."
    # SFX SUGGESTION: A short, fabric-muted phone vibration.
    "My phone buzzes in my pocket."
    mc "Ah frick, she beat me..."
    show asahina teasing
    ah "Oh? Mooooonika?"
    mc "Yes, Monika. We're going to that horror movie today, if I ever get back to her."
    "She lightly punches my upper arm while I set my cup back on the coaster."
    mc "Give me a second to sort the time out. Also, how much milk did you put in this?"
    show asahina neut
    ah "Hm? I didn't make it, Mom did."
    mc "...Be real."
    "I keep staring while I wake my phone."
    python:
        _phone_messages = [
            phone_msg("them", "Morning! I looked online and there are showings at noon and a couple hours after that."),
            phone_msg("them", "I did try for the evening one first. Full disclosure."),
            phone_msg("me", "Committing to the horror bit."),
            phone_msg("them", "Obviously. Except the site crashed on me with two seats already in the cart."),
            phone_msg("them", "By the time it loaded again, the evening was sold out."),
            phone_msg("me", "Brutal."),
            phone_msg("them", "It still kept offering to show me the seating plan. Very helpful."),
            phone_msg("them", "So! Noon or the afternoon. I don't really mind which, so I'll leave it up to you."),
            phone_msg("me", "Let me check the buses."),
            phone_msg("them", "Sure. I'll book once you've picked."),
            phone_msg("me", "Okay, either works. Let's do..."),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0518_1
    # Only two canonical showtimes. "Evening." is a gag that loops back rather
    # than a third path: she just explained it sold out, so picking it only
    # proves MC skimmed the message. Reset here as well as `default`ed so a dev
    # scene jump gets the joke back.
    $ a0518_evening_joked = False
label a0518_showtime_pick:
    menu:
        "Noon.":
            $ s1_pick_movie_time("noon")
        "A couple hours after that.":
            $ s1_pick_movie_time("afternoon")
        "Evening." if not a0518_evening_joked:
            $ a0518_evening_joked = True
            python:
                _phone_messages = [
                    phone_msg("me", "Evening. Lock it in."),
                    phone_msg("them", "..."),
                    phone_msg("them", "[player]."),
                    phone_msg("them", "Did you miss the part where I couldn't book it?"),
                    phone_msg("me", "I read some of it. Not necessarily in order."),
                    phone_msg("them", "The evening is SOLD OUT. Pick one of the other two!"),
                    phone_msg("me", "Right. Sorry. Let me try that again."),
                    phone_msg("them", "Take your time~"),
                    phone_msg("them", "Actually don't. We'd be here all day and then we'd have no showing at all.")
                ]
            call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0518_1a
            jump a0518_showtime_pick
    python:
        _phone_messages = [
            phone_msg("me", s1_mv_label + ", then?"),
            phone_msg("them", "Works for me! Meet up at the theater, or what's convenient for you?"),
            phone_msg("me", "Theater's fine."),
            phone_msg("them", "Great! See you then!"),
            phone_msg("them", "Bring our predictions. I want proof when I'm right.")
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0518_1b
    # She texted first, out of school hours, about something that could have
    # waited -- so the line is open for idle chatter from here.
    $ phone_open("monika")
    "I check that the reminder saved, then lower the phone. Asahina is still watching me."
    show asahina curious
    ah "Why are you so wound up? It's Monika."
    mc "I'm trying to send one message without a running commentary."
    show asahina unamused
    "Her thumb stops over the remote."
    mc "Sorry. It's just... she called it a date when she asked."
    mc "We hang out all the time. Now I keep wondering if I'm supposed to do something differently."
    show asahina thinking
    ah "Like what? She's seen you eat. She's also probably seen you go number two. It can't get worse."
    mc "Here, look. Just this conversation, though. Don't scroll up."
    "I hand her the phone. Her thumb moves through the thread without a single wasted swipe."
    "She tosses it back and reaches for her own. A few taps later, my phone vibrates."
    python:
        _phone_messages = [
            phone_msg("them", "dude shes so into u"),
            phone_msg("me", "Yeah, no shit, Asa."),
            phone_msg("them", "well why dont u go for her? shes nice and pretty"),
            phone_msg("them", "i can be ur wingwoman if u want"),
            phone_msg("me", "You're the last person I want for that job."),
            phone_msg("me", "Why are we texting when we're sitting right next to each other?"),
        ]
    call phone_text_conversation("Asa", _phone_messages, append=True) from _call_phone_text_conversation_0518_2
    # She texted him from the same couch about nothing. That IS the idle-chatter
    # register, so hers opens on the beat that establishes it.
    $ phone_open("asa")
    show asahina smug
    ah "You're welcome, by the way."
    mc "For what?"
    ah "For not sending that to her instead of you. I had it in the other thread and everything."
    mc "..."
    show asahina teasing
    ah "I'm KIDDING, Jesus!"
    mc "You really think I buy that?"
    ah "I didn't send anything! Check, if you don't believe me."
    show asahina smug
    "She shrugs and goes back to flipping through channels neither of us actually cares about."
    "{i}Still got time before I need to get ready.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "After finishing my coffee in the living room, I find myself back upstairs."
    call nier_clear from _call_nier_clear_0518_1
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    mc "Alright, game... Let's see what you got..."
    "I peel the seal off and save it to pick at while the game installs. Leaving a new release unopened overnight deserves some kind of award."
    "..."
    "{i}Okay. Rules.{/i}"
    "{i}No fast travel until the second region. No selling anything. No looking anything up.{/i}"
    "I write the rules on the back of a receipt, although nobody else will ever check whether I stick to them."
    "The tutorial gives me a man who takes twenty minutes to explain a sword. By the end, I've grown attached to him and stolen everything in his house."
    "I lose the first real fight because I'm saving an item I could've used. The second attempt goes better once I stop doing that."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    "I reach a clean save point right as the alarm I set for the movie cuts in."
    "{i}Good place to stop. Matsuda can have a review of the first couple hours, at least.{/i}"
    "I save again to be sure, then leave the controller on the desk while I get ready."
    "{i}I want to see this. I want to see it with her. Getting dressed should be the easy part.{/i}"
    "I try a second shirt, then put the first one back on because it doesn't bunch up under my bag strap."
    "The hair takes longer. I give up on the bit at the back and check that I've packed my wallet and the scrap with our predictions."
    "On the stairs, I remember Asahina's DVD and leave it outside her room."
    $ hide_calendar()
    stop music fadeout 2.0
    scene black with dissolve_scene_full
    pause 2.0
    scene bg city_day
    $ show_calendar()
    $ atmos(s1_mv_atmos)
    with dissolve_scene_full
    # A shopping street on a weekend: the frame gets shouldered along by people
    # who are also going somewhere, which is the whole reason MC walks into one
    # of them the night before.
    play music day_c
    # SFX SUGGESTION: Light delivery-cart wheels and metal storefront shutters clattering in the distance.
    "[s1_mv_street]"
    "The bus drops me a block from the theater, behind a man carrying a cake box with both hands. I give him some room at the crossing."
    "While we wait for the light, I tell Monika I'm nearly there, with her replying that she's just getting off her bus."
    "The signal changes before I can put the phone away."
    "I pocket the phone and cross with the crowd, careful this time to keep my eyes ahead."
    "A kid by the corner holds up a bottle from a cooler, trying to get the attention of two women arguing over a parking space. Neither looks around."
    "I'm eleven minutes early, so there's time to look around. A line has already gathered under the {i}Iron Rod{/i} banner by the theater entrance."
    "{i}Seems like the hype and promos did their job...{/i}"
    "{i}Now where is she...?{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg theater_day
    $ show_calendar()
    $ atmos(s1_mv_atmos)
    with wipeleft_scene
    "The theater entrance is louder than the street. A staff member tapes one more {i}Iron Rod{/i} notice to the glass while the line inches around him."
    "Near the ticket machines, two kids in plastic wrist morphers argue over their favorite Lightning Squad member. One looks personally betrayed that Yellow Arc isn't the obvious answer."
    "I stand near the display case, half-watching the crowd and half-listening for any potential calls or texts."
    "The collector cups in the case are from a film that came out two years ago. One has a sword for a handle, which would make it an absolute pain to wash."
    "I look up the price anyway, then quickly close the page."
    show monika forward casual happ om oe nobl rdown ldown at l11
    m forward casual laug om ce nobl rdown ldown "Hey! Look who beat me here!"
    "Monika lifts a hand as she comes through the crowd. Her pace is quick until she sees me, then it eases."
    "She tucks a loose strand of hair behind her ear as she reaches me."
    show monika forward casual happ om oe nobl rdown ldown
    mc "Only just. I was looking at those cups over there."
    m forward casual happ om oe nobl rdown lpoint "The sword one? Well, you stopped yourself just in time."
    mc "I thought about it. We could get a picture with the poster for slightly less money."
    m forward casual happ om oe nobl rdown ldown "Afterward? I want to know if I like the movie first!"
    "She checks the queue by the doors while I tuck my phone away."
    m forward casual happ cm oe nobl rhip ldown "I exchanged the vouchers after you picked. [s1_mv_label] still had two seats together, so lucky us!"
    "She pulls two tickets from her handbag."
    mc "For a one-day-old movie, that's kind of wild."
    m forward casual happ om oe nobl rhip ldown "To be fair, people have been talking about {i}Iron Rod{/i} for months."
    # The HOLD in the middle of fx_hand_off is the beat the line is about.
    "She hands me one ticket. Her fingers brush mine, then draw back."
    mc "Got the predictions, too. Last chance to change your mind."
    m forward casual happ om oe nobl rdown ldown "I'm sticking with the flashlight guy. He looks too miserable to die early."
    mc "See, that's what the director {i}wants{/i} you to think."
    "She unfolds the scrap and checks our two names while the crowd moves around us."
    "The poster looms above her shoulder. Up close, the dark smear behind the lead actor looks less like a shadow and more like another person."
    mc "Actually, don't look too hard at the poster. It probably leans too much into spoiler territory."
    m forward casual curi om oe nobl rdown ldown "You're rubbing your shoulder."
    "I hadn't realized I was doing it."
    mc "Oh. Yeah, it's a bit bruised. I ran into someone last night."
    m forward casual curi om oe nobl rdown ldown "Ran into, as in...?"
    mc "Like, literally. My brain took the night off."
    show monika forward casual worr cm oe nobl rdown ldown
    "Monika's mouth tightens, then settles."
    m forward casual worr cm oe nobl rdown ldown "Well... are you good?"
    mc "Yeah. Just sore. No vapor rub required."
    m forward casual neut cm oe awkw rdown ldown "Ah."
    "She closes her fingers around the ticket and nods toward the entrance."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg theater_lobby
    $ show_calendar()
    $ atmos(s1_mv_atmos)
    with wipeleft_scene
    play sound moddooropen
    show monika forward casual happ cm oe nobl rdown ldown at t11
    "Inside, the air conditioning cuts through the heat at once. The lobby smells like vegetable oil pretending to be butter and floor cleaner losing a fight with spilled cola."
    "The line for concessions moves with practiced slowness."
    show monika at t21
    show kotonoha work neut at t22
    "Kotonoha slides a tray of nachos across the counter, then looks up as we reach the register."
    show kotonoha work neut
    mc "Yo."
    ko "Good afternoon, [player], Monika."
    "Her work shirt is neat alongside the concession apron, and the name tag sits exactly level."
    "Monika steps up beside me and studies the menu board."
    m forward casual happ cm oe nobl rhip ldown "Do you want anything?"
    mc "A drink and popcorn. Whatever the price board's about to do to me."
    "I move beside her so we can both read the combinations."
    m "Let's go with that then."
    "Behind Kotonoha, the popcorn machine rattles as a new batch tumbles into the bin."
    ko "Combo B is cheaper with two drinks."
    mc "Is it actually, though? Or do we have to buy more to get the discount?"
    ko work thinking "The second one."
    mc "...Appreciate the honesty."
    ko work neut "For two drinks, you save about... this much."
    "She taps on the screen in front of us."
    m forward casual happ om oe nobl rhip ldown "Oooh, combo B, then, please. Medium popcorn."
    ko work curious "Salted?"
    "Monika tilts her chin toward me."
    mc "Sure."
    show monika forward casual laug om ce nobl rdown ldown at h21
    m forward casual laug om ce nobl rdown ldown "Salted and churro toppings!"
    mc "On your half! I learned from last time."
    show monika forward casual happ om oe nobl rhip ldown
    show kotonoha work neut
    "Kotonoha taps the order in while Monika marks an imaginary halfway point on the counter. Her half seems optimistic."
    ko "{i}Iron Rod{/i} is in theater three. Doors open in five minutes."
    m forward casual lsur om oe nobl rdown ldown "Oh wow, that soon?"
    ko "The trailers are longer than usual."
    "Kotonoha spends the next half minute prepping our food and drinks more skillfully than I've seen people who have worked these jobs for years."
    show kotonoha work neut at t22
    show monika forward casual happ cm oe nobl rdown ldown at t21
    ko "Your total is on the screen."
    "The total looks like it includes admission to a second movie. Monika pays before I get my wallet halfway out."
    mc "...I can get it. Seriously."
    m forward casual happ om ce awkw rdown ldown "Aaapapap--{i}I{/i} invited {i}you{/i}. Let me get this one."
    "She snaps the lid onto her cup while I take the popcorn and put my wallet away."
    mc "Alrighty then. In that case, I'm getting the next one."
    m forward casual happ om oe nobl rdown ldown "Fine by me~"
    ko "Enjoy the film."
    mc "Thanks, you too--"
    mc "...Uh..."
    show kotonoha work teasing
    m forward casual happ om oe blus rdown ldown "Thank you, Kotonoha!"
    "Kotonoha nods once and turns to the next customer."
    show kotonoha at thide
    hide kotonoha
    show monika forward casual happ cm oe nobl rdown ldown at t11
    "Past the concession stand, theater three's doors stand propped open over a crooked strip of red carpet."
    "Monika balances both drinks against her chest, then leans one toward me."
    m forward casual happ om oe nobl rdown ldown "Ready?"
    mc "As ready as I'm getting."
    "She passes me my drink and glances toward the dark doorway."
    show monika forward casual happ cm ce nobl rdown ldown
    m forward casual happ cm ce nobl rdown ldown "Yeah. Let's go before I reconsider."
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 1.0
    pause 2.0
    scene bg theater_inside
    $ show_calendar()
    $ atmos(s1_mv_atmos)
    with wipeleft_scene
    play music hearttoheart
    show monika forward casual happ cm oe nobl rdown ldown at t11
    # HOUSE LIGHTS. See theater_fx.rpy. Three steps down, one back up, then off
    # on the way out: half-light for the ad loop, further for the trailers, out
    # for the feature, and up again at the credits. It must be cleared before
    # the lobby -- `scene` does not touch the cinematic layer.
    $ theater_lights(0.45, secs=1.8)
    "Theater three is dim, with an advertisement loop showing enormous drinks and slow-motion popcorn. Somewhere behind the screen, a cheerful voice tries to sell us what we're already carrying."
    "Monika finds our row before I do."
    m forward casual curi om oe nobl rdown ldown "This should be us..."
    "She steps aside so I can take the inside seat, then settles beside me with her bag between her feet."
    "The popcorn bucket lands between us."
    mc "Comfy?"
    m forward casual wry cm oe nobl rdown ldown "I will be when this chair lets me sit up."
    m forward casual curi om oe nobl rdown lpoint "Does yours tilt this far back?"
    mc "Did you push the back?"
    m forward casual laug om ce nobl rdown ldown "Oh! Much better, thank you."
    "I reach for the salted side, but the churro topping has already spread across it. Cinnamon coats my fingers when I pull them out."
    mc "...This is a crime."
    m forward casual happ om oe nobl rdown lpoint "It's good, though, right?"
    mc "That's {i}not{/i} what I said."
    $ theater_lights(0.78, secs=2.2)
    "She passes me a napkin and takes some popcorn as the lights dim another step. Around us, conversations drop to whispers."
    "{i}So why am I suddenly aware of the exact inch of air between our shoulders?{/i}"
    m forward casual curi om oe nobl rdown ldown "Hey."
    mc "Hm?"
    m forward casual happ cm oe nobl rhip ldown "You can laugh if the movie gets stupid, by the way. I won't report you to the horror fan committee."
    mc "...There's a committee? How long has that been a thing?"
    m forward casual happ om oe nobl rdown lpoint "Oh, {i}years{/i}. We meet in a basement and complain about remakes. Very exclusive."
    mc "Sounds credible..."
    "The row in front fills with a group who have brought an entire second steak dinner in with them."
    "{i}They definitely look the part... heh.{/i}"
    m forward casual happ cm oe nobl rhip ldown "Are you going to keep watching through the bad bits? You went very quiet during the trailer."
    mc "If I look away, I won't know when it's safe to look back."
    m forward casual laug om ce nobl rdown ldown "Oh lord, that's terrible logic... I see the problem, though."
    mc "You can tell me if you figure it out."
    "She settles back, and I move the bucket so we can both reach it without knocking the drinks."
    $ theater_lights(1.0, secs=1.1)
    play sound sfx_thunder
    "The opening starts with a thunderclap. Someone in the front three rows jumps."
    "Monika jolts toward the screen already grinning."
    show monika forward casual happ cm oe nobl rdown ldown
    "{i}Alright. Movie time.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    # DELIBERATE: the house lights are NOT cleared for these interludes. `scene`
    # only clears the master layer, so the projector wash carries over the black
    # and the narration plays against a screen that is still running. Clearing
    # and restoring it here would mean the film politely stops every time the
    # narrator summarizes it.
    nier "The movie opens at an empty railway crossing, where a missing-person flyer keeps lifting away from its staple. I keep watching the road behind it."
    nier "The first death proves both our predictions wrong, although Monika points out that her choice was at least in the room. We start again, more quietly."
    nier "Forty minutes in, someone two rows down starts explaining the plot. Their companion shushes them, and we miss whatever happens next."
    nier "At some other point in time, someone's egregiously loud ringtone goes off as one of the workers tells them to either silence their phone or walk out to take the call."
    call nier_clear from _call_nier_clear_0518_3
    pause 2.0
    scene bg theater_inside
    $ show_calendar()
    $ atmos(s1_mv_atmos)
    show monika forward casual neut cm oe nobl rdown ldown at t11
    with wipeleft_scene
    "The film keeps holding on empty rooms after people leave them. I lean forward for a glimpse into a doorway, then catch Monika doing the same thing."
    "A long argument at the gas station loses me, although the clerk gets a laugh out of her. By the time they finally leave, we have worked our way halfway through the popcorn."
    "{i}Probably the most unrealistic part about this. I'd have crushed it by the fifteen minute mark.{/i}"
    "About what feels like an hour and ten minutes in, the lead climbs into a maintenance tunnel he has no business entering."
    "The score thins down to a single held note. His flashlight finds a wall of something that should not be behind another wall."
    "A low, wet sound comes from off-screen, close enough that I feel it in the back of my neck. Someone behind us sucks in a breath."
    show monika forward casual nerv cm oe blaw rdown ldown
    "Monika's hand closes around my sleeve."
    "Her fingers catch the fabric just above my wrist. I leave my arm where it is while the flashlight drags across the wall."
    "On the next cut to daylight she lets go and smooths the fabric like she can erase the evidence, staring very hard at the screen the whole time."
    "I slide the bucket back toward her when the music starts again."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "By the last return to the crossing, I want the lead to put the rod down and leave. He gives a speech instead, while someone near the back whispers, 'Get in the car.'"
    call nier_clear from _call_nier_clear_0518_4
    pause 2.0
    scene bg theater_inside
    $ show_calendar()
    $ atmos(s1_mv_atmos)
    show monika forward casual nerv cm oe blaw rdown ldown at f11
    with wipeleft_scene
    # Credits are the one part of a film that is reliably bright, and the
    # ushers bring the house halfway up under them.
    $ theater_lights(0.34, secs=2.0)
    "The credits crawl up the screen while half the audience stands and blocks the row."
    "I stay seated while the people beside us negotiate the safe evacuation of their popcorn."
    m forward casual curi om oe nobl rdown ldown "...Well?"
    mc "I liked it. The tunnel was a cheap shot, though."
    m forward casual happ cm oe nobl rhip ldown "Hey, cheap shots work sometimes. That's sort of the whole point of them."
    "Her hand has drifted to her own sleeve, smoothing the same spot she grabbed on mine."
    mc "...Says the person who tried to tear my arm off."
    show monika at f11
    m forward casual flus om oe blaw rdown ldown "I didn't!"
    $ theater_lights(0.0, secs=1.3)
    "Her face goes pink faster than the house lights come up."
    m forward casual nerv om oe awkw rdown ldown "I was startled for maybe, like, half a second."
    mc "You held on through the next scene."
    m forward casual flus om ce blaw rhip ldown "Okay, okay! Fine, it got me {i}once{/i}!"
    "She folds her empty straw wrapper into a tiny rectangle, then folds it again."
    m forward casual pout om oe nobl rdown lpoint "But {i}you{/i} jumped at the opening thunder."
    mc "Just a louder audio mix than I expected..."
    show monika forward casual laug cm ce nobl rdown ldown at t11
    m forward casual laug cm ce nobl rdown ldown "Suuuuuuuure, let's go with that."
    "Once the row clears, I take the empty bucket while she retrieves the lid that rolled under her seat."
    $ theater_clear()
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 1.0
    pause 2.0
    scene bg theater_lobby
    $ show_calendar()
    $ atmos(s1_mv_atmos)
    show monika forward casual happ cm oe nobl rdown ldown at t21
    show kotonoha work neut at t22
    with wipeleft_scene
    play music day_b
    "The lobby is full of spilled reactions now: people arguing over the ending, parents corralling children, someone near the poster loudly insisting the book did it better."
    ko "Was the movie satisfactory?"
    mc "Yeah, I liked it. Got me with the sound in a couple places."
    m forward casual happ om oe nobl rhip ldown "It was good! A little amateurish at a couple points, but good."
    ko work thinking "People have been coming out arguing about it all day. You have no idea how many times I've heard that the book did it better."
    show kotonoha work neut
    "She gathers abandoned napkins from the counter and squares the stack."
    mc "You seen it yet?"
    ko "No. We are told to avoid spoilers, as per our training."
    mc "Sounds like a line from the handbook."
    ko work teasing "It should be."
    "Monika laughs into her cup lid."
    show monika forward casual happ cm oe nobl rdown ldown
    m forward casual happ om oe nobl rdown ldown "Rest assured, we won't yell, at least."
    ko work neut "I appreciate that."
    "A customer waves from the other end of the counter. Kotonoha looks over, then back at us."
    ko "Have a good afternoon."
    mc "You too."
    m forward casual happ om ce nobl rdown ldown "Bye, Kotonoha!"
    show monika forward casual happ cm oe nobl rdown ldown at t11
    show kotonoha at thide
    hide kotonoha
    "She nods once and returns to work."
    "Monika and I drift toward the doors with the crowd."
    "A kid works his way across the carpet one red square at a time, so Monika waits until he reaches the far side before moving."
    "I hold the door while she gets her bag out of the child's way."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg theater_day
    $ show_calendar()
    $ atmos(s1_mv_atmos)
    show monika forward casual happ cm oe nobl rdown ldown at t11
    with wipeleft_scene
    "[s1_mv_out]"
    "The next queue is forming by the poster, but the spot in front of it is free. I stop Monika before we reach the street."
    mc "Still want the picture? I'd say it earned one."
    m forward casual happ om oe nobl rdown ldown "Only if we can look as miserable as the flashlight guy."
    "I hold up my phone while she moves beside me, turning her cup into a flashlight. The first attempt mostly gets my thumb."
    m forward casual laug om ce nobl rdown ldown "Move it farther away! You've cut my head off in this one!"
    mc "I'd say it's accurate."
    "On the second try, I get us both and just enough of the title to prove we went. She's laughing in it, so I take another for the serious version."
    m forward casual happ om oe nobl rdown lpoint "Send the bad one too. I want that one."
    "I do as she says before pocketing everything."
    m forward casual happ om oe blus rdown ldown "So..."
    mc "So."
    menu:
        "\"Thanks for inviting me.\"":
            $ s1_pick("movie_goodbye", "plain")
            mc "Thanks for inviting me. That was fun."
            m forward casual happ om oe nobl rdown ldown "It was, wasn't it?"
        "\"Your horror committee sounds corrupt.\"":
            $ s1_pick("movie_goodbye", "joke")
            mc "Your horror committee sounds corrupt."
            m forward casual laug om ce nobl rdown ldown "Oh, extremely. But they have good snacks and tea!"
        "(Say the true one.)":
            $ s1_pick("movie_goodbye", "linger")
            mc "I'm glad you asked me and not somebody else."
            show monika forward casual nerv cm oe blaw rdown ldown
            "That was more honest than I had budgeted for."
            m forward casual nerv cm oe blaw rdown ldown "..."
            show monika forward casual flus cm oe blus rdown ldown at f11
            m forward casual flus cm oe blus rdown ldown "There wasn't a somebody else."
            mc "...Okay."
    "She adjusts her bag on her shoulder and looks down the street."
    m forward casual nerv om ce blaw rhip ldown "I should head back. I promised I'd be home for dinner, and I still have to stop at the store."
    mc "Yeah, I should go too. Send me that shot if you find the poster online."
    m forward casual curi om oe nobl rdown ldown "The shadow?"
    mc "I want to check if it was there the whole time. It was bothering me."
    m forward casual happ om oe nobl rdown lpoint "Oh, absolutely. We're not finished with this movie."
    show monika forward casual happ om oe nobl rdown lpoint at t11
    "She starts to leave, then pauses."
    m forward casual curi om oe nobl rdown ldown "Hey, [player]?"
    mc "Yeah?"
    m forward casual happ cm oe blus rdown ldown "Thanks for coming with me."
    mc "Yeah. Anytime."
    m forward casual happ cm ce nobl rdown ldown "Good."
    "Then she waves and heads down the sidewalk, ponytail swaying behind her."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "On the bus, I look through the photos again. Monika has managed to keep a straight face in the third one, but I haven't."
    nier "My sleeve rides up when I zoom in. I smooth it back down, remembering her fingers there during the tunnel."
    nier "The bus takes a corner before I can decide which picture to keep, to which I save all three."
    call nier_clear from _call_nier_clear_0518_6
    stop music fadeout 1.0
    pause 2.0
    scene bg living_room
    $ show_calendar()
    $ atmos("evening")
    with wipeleft_scene
    play music house_day_a
    play sound moddooropen
    "When I get home, Asahina is still in the living room. The poster is propped against the couch now, promoted from crisis to object."
    "She's finished the block letters and drawn stitching around the volleyball, right down to the tiny curve where it disappears behind the title."
    show asahina curious at t11
    ah "Well?"
    mc "Well what?"
    show asahina teasing
    ah "Movie, date, whatever. Spill it."
    mc "It was... a movie."
    show asahina unamused
    ah "Wow. Thank you for the important info. Really riveting stuff, that."
    "I put my shoes by the door, then join her beside the couch. She shifts a pair of scissors out of the way."
    mc "It was fun. We both enjoyed it."
    show asahina teasing
    ah "Awwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww." # purposefully goes off the textbox as a meta gag
    show asahina smug
    mc "{i}Don't{/i}."
    ah "I didn't say anything! Not one single word!"
    mc "You said it with your stupid face."
    show asahina embarrassed
    ah "Shut up! You haven't stopped smiling since you got in!"
    mc "...How mature of you."
    "She leans back on her hands. Her eyes cut to the poster, then back to me."
    "With the TV off, I can hear the poster's stiff paper scrape against the couch as she adjusts it. Most of a sandwich sits politely on a plate on the coffee table."
    mc "Coming along nicely, I see. Especially the lettering."
    show asahina nervous
    ah "...Yeah?"
    mc "Yeah."
    "She turns away too quickly."
    show asahina neut
    ah "Cool. Now go away before your cinnamon smell ruins it."
    mc "Oh, gladly."
    "I head toward the stairs, then stop near the first step."
    mc "Oh, and Asa?"
    ah "What?"
    mc "If the volleyball team doesn't appreciate it, I'm calling them tasteless swines."
    show asahina worried
    ah "Please don't. I have to see these people at practice."
    mc "We'll see."
    show asahina happy
    ah "...Thanks, birdbrain."
    "I keep walking, and the smirk stays on the side of my face she cannot see."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I get my bag ready for Monday while Mom warms dinner. Before I can start anything else, she calls us down."
    call nier_clear from _call_nier_clear_0518_7
    pause 2.0
    scene bg dining_table_night
    $ show_calendar()
    show asahina neut at t21
    show mom neut at t22
    $ atmos("home_night")
    with wipeleft_scene
    mom "So. The movie. How'd things go?"
    mc "It was good."
    show asahina teasing
    ah "It was terrifying and he {i}screamed{/i}."
    mc "Oh my God, here we go..."
    ah "He screamed so loud they had to stop the film and check on the building."
    show mom curious
    mom "They stopped the film...?"
    ah "They did. Ask anyone who was there."
    mc "...You're saying {i}you{/i} were there? Come on, which one of us actually watched the thing?"
    show asahina smug
    ah "Your testimony is biased, so shut up."
    "I swallow my pride and let her have it. Correcting the story would take longer than the story."
    show mom smug
    mom "And you were polite to Monika? You... did put cologne and deodorant on, right?"
    mc "For--YES! I did, Mom! And we had a great time, and we thoroughly enjoyed ourselves!"
    mom neut "And you offered to pay at least half of things?"
    mc "I mean, I offered, but she absolutely insisted, so..."
    show mom worried
    mom "So she paid for everything. Come on, you know better..."
    mc "What else was I supposed to--{i}*sigh*{/i}"
    "While I decide whether to defend myself, Mom turns to Asahina and asks where the poster is going."
    show mom curious
    show asahina embarrassed
    ah "It's done. It's fine. It exists."
    mom "Is it going up, or is it going to live against the couch for however long?"
    ah "Tuesday. They said Tuesday."
    show asahina neut
    "She finishes the rice while telling Mom where she wants the poster hung."
    "The rest of dinner goes to mostly dull ramblings between Mom and Asahina about a variety of topics."
    "I mostly listen, moving the serving dish within Asahina's reach when she leans across me."
    show mom thinking
    "When we clear the table, Mom sets the school printout back down by my elbow, face-up this time."
    "Neither of us mentions the printout as I move my glass to make room for it."
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music night_b
    "When I get back upstairs, I hear something rustling outside the window until my phone buzzes over it."
    python:
        _phone_messages = [
            phone_msg("them", "Okay, theory: the iron rod wasn't actually the weapon. It was the promise."),
            phone_msg("them", "Wait, that sounded better in my head."),
            phone_msg("me", "No, keep going. I want to see how deep the committee corruption goes."),
            phone_msg("them", "You joke, but I have notes and stuff."),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0518_3
    "I ask for the notes, then send her the promotional graphic with a circle around the shadow. When she replies, I sit on the edge of the bed to read it."
    "The controller is still on the desk, but I'm curious about what she thinks happened at the crossing."
    "{i}The game will still be there tomorrow. She might have figured this out by then.{/i}"
    "I clamp the receipt with the rules on it inside the case."
    "The serious photo goes into my favorites, followed by the one she wanted. I check that I haven't accidentally sent either to the family chat."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I find one unfinished worksheet while checking my bag, and Monika's messages keep arriving as I work through it."
    nier "By the time I finish answering both, my eyes feel heavy enough to not warrant any further time awake."
    call nier_clear from _call_nier_clear_0518_8
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0518_1
    jump a0519
