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
    play music dailyleisure
    ah "Ugggh, why is there nothing good on?!"
    "My sister continues to flip through the channels on the TV with a force that makes you think it offended her."
    show asahina annoyed
    ah "Why did the Geographic have to have downtime now of all times?!"
    mc "Maybe this is the universe's way of telling you to expand your horizons or something."
    show asahina smug
    ah "I'll expand them whenever YOU give me back my DVD of 'The Grandfather.'"
    mc "...I have no idea what you're talking about."
    ah "You've had it for two weeks now!"
    "I plead the fifth with a long sip of coffee."
    "{i}Tastes awfully thick...{/i}"
    # SFX SUGGESTION: A short, fabric-muted phone vibration.
    "My phone buzzes in my pocket."
    mc "Ah frick, she beat me..."
    show asahina teasing
    ah "Oh? Care to share?"
    ah "Is it your girlfriend?"
    mc "Once again, Asa, she's not my--"
    mc "...Actually, no. We're not doing this."
    mc "Monika and I made plans to catch a movie today, that's all."
    "She lightly punches my shoulder."
    show asahina happy
    "I lay my cup back on the coaster."
    mc "...We still need to pick a time, so let me follow up with her real quick."
    mc "Also, you put WAY too much milk in the coffee this morning."
    show asahina neut
    ah "Hm? I didn't make it, Mom did."
    mc "...Be real."
    "I continue to give my sister the stare of skepticism as I press the power button on my phone."
    python:
        _phone_messages = [
            phone_msg("them", "Morning! I looked online and there are showings at noon and a couple hours after that."),
            phone_msg("them", "I did try for the evening one first. Full disclosure."),
            phone_msg("me", "Committing to the horror bit."),
            phone_msg("them", "Obviously. Except the site crashed on me with two seats already in the cart."),
            phone_msg("them", "I refreshed, and the entire evening block was gone. Sold out. In the time it took a little circle to finish spinning."),
            phone_msg("me", "Brutal."),
            phone_msg("them", "I stared at the screen for a full minute like it was going to apologize."),
            phone_msg("them", "So! Noon or the afternoon. I don't really mind which, so I'll leave it up to you."),
            phone_msg("me", "You know I'm bad at decisions, Monika."),
            phone_msg("them", "Oh, don't be like that. I know you can do it!"),
            phone_msg("me", "Fine, uh..."),
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
                    phone_msg("me", "Evening works."),
                    phone_msg("them", "..."),
                    phone_msg("them", "[player]."),
                    phone_msg("them", "Did you read any of that, or did you just watch the shape of it go past?"),
                    phone_msg("me", "I read some of it. Not necessarily in order."),
                    phone_msg("them", "The evening is SOLD OUT. I watched it sell out. I was there."),
                    phone_msg("me", "Right. Sorry. Let me try that again."),
                    phone_msg("them", "Take your time~"),
                ]
            call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0518_1a
            jump a0518_showtime_pick
    python:
        _phone_messages = [
            phone_msg("me", s1_mv_label + ", then?"),
            phone_msg("them", "Works for me! Meet up at the theater, or what's convenient for you?"),
            phone_msg("me", "Theater's fine."),
            phone_msg("them", "Great! See you then!"),
            phone_msg("them", "Don't stand me up now!")
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0518_1b
    # She texted first, out of school hours, about something that could have
    # waited -- so the line is open for idle chatter from here.
    $ phone_open("monika")
    "I take a deep breath."
    show asahina curious
    ah "You good there? I can hear you grinding your teeth from over here."
    mc "Just a nosy sister that gets under my skin."
    show asahina unamused
    "The stare I get back is not amused."
    mc "...Okay, fine, real talk, jokes aside."
    mc "It's not that I'm annoyed, per se..."
    mc "It's just--when somebody's that direct about things, I don't know where to put my hands. Or my face. Or, uh."
    mc "...Forget it."
    show asahina thinking
    ah "I think I get it..."
    mc "Here, I'll just show you."
    mc "And I swear to everything holy, do NOT scroll too far up or start digging through things."
    "I turn over my phone's chat history to her and she reads through the texts in a scarily surgical manner."
    "Half a minute passes before she tosses it back to me and reaches for her own."
    "Some tapping and typing later, and I feel a vibration."
    python:
        _phone_messages = [
            phone_msg("them", "dude shes so into u"),
            phone_msg("me", "I'm not dense, Asa."),
            phone_msg("them", "well why dont u go for her? shes nice and pretty"),
            phone_msg("them", "i can be ur wingwoman if u want"),
            phone_msg("me", "You're the last person I want for that job."),
            phone_msg("me", "And why are we texting when we're sitting right next to each other?"),
        ]
    call phone_text_conversation("Asa", _phone_messages, append=True) from _call_phone_text_conversation_0518_2
    # She texted him from one room away about nothing. That IS the idle-chatter
    # register, so hers opens on the beat that establishes it.
    $ phone_open("asa")
    show asahina smug
    "She shrugs and goes back to flipping through channels neither of us actually care about."
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
    mc "Alright, game..."
    mc "Let's see what you got..."
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
    play music daily
    # SFX SUGGESTION: Light delivery-cart wheels and metal storefront shutters clattering in the distance.
    "[s1_mv_street]"
    "I check my phone at the crosswalk. Monika's last message is still there, still wearing more exclamation points than the sentence needed."
    "The signal changes before I finish reading it for the third time and contemplating whether I should let her know I'm on my way."
    "I pocket the phone and cross with the crowd, careful this time to keep my eyes ahead."
    "By the time the theater sign comes into view, a small line has already gathered under the {i}Iron Rod{/i} banner."
    "{i}Seems like the hype and promos did their job...{/i}"
    "{i}Now where is she...?{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg theater_day
    $ show_calendar()
    $ atmos(s1_mv_atmos)
    with wipeleft_scene
    "The theater entrance is louder than the street."
    "A staff member tapes one more {i}Iron Rod{/i} notice to the glass while the line inches around him without complaint."
    "Near the ticket machines, two kids in plastic wrist morphers argue over their favorite members of the Mighty Lightning Squad. One of them looks personally betrayed by the idea that Yellow Arc is not the obvious answer."
    "I stand near the display case, half-watching the crowd and half-listening for my phone."
    show monika forward casual happ om oe nobl rdown ldown at l11
    m forward casual laug om ce nobl rdown ldown "Hey! Look who beat me here!"
    "Monika lifts a hand as she comes through the crowd. Her pace is quick until she sees me, then it eases."
    "A loose strand of hair has slipped free near her cheek. She tucks it back with the side of one finger."
    show monika forward casual happ om oe nobl rdown ldown
    mc "Yeah... Something tells me I should've left earlier."
    m forward casual happ om oe nobl rdown lpoint "I know, right? Like three different groups are taking pictures with the poster by the doors."
    mc "Yeah, not out of the ordinary. You wanna take one?"
    mc "...Cause I don't. Count me out."
    "For a second we both look at the banner instead of each other."
    m forward casual happ cm oe nobl rhip ldown "I exchanged the vouchers when I checked the times. [s1_mv_label] still had seats together."
    "She pulls two tickets from her bag."
    mc "For a movie less than a day old, that's kind of wild."
    m forward casual happ om oe nobl rhip ldown "To be fair, people have been talking about {i}Iron Rod{/i} for months."
    # The HOLD in the middle of fx_hand_off is the beat the line is about.
    "She hands me one ticket. Her fingers brush mine, then draw back."
    mc "And the other half of the crowd?"
    m forward casual nerv om ce blaw rdown ldown "Here to be scared on purpose...or something...maybe."
    mc "You know that it's alright to not have the answer to everything, right?"
    "I look down at the ticket, then at the poster beside us."
    "The longer I stare at both, the more it starts looking like something waiting to move."
    mc "...Right. Anyway..."
    m forward casual curi om oe nobl rdown ldown "You're rubbing your shoulder."
    "I hadn't realized I was doing it."
    mc "...Yeah?"
    mc "I ran into someone last night."
    m forward casual curi om oe nobl rdown ldown "Ran into, as in...?"
    mc "Literally. My brain straight up wasn't on. Not exactly my finest moment."
    "Monika's expression shifts, just a little. Not alarmed."
    m forward casual worr cm oe nobl rdown ldown "Well...are you good?"
    mc "Yeah. Just a little sore, no need for vapor rub or anything like that."
    m forward casual neut cm oe awkw rdown ldown "Ah."
    "She folds her ticket against her palm and nods toward the entrance."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg theater_lobby
    $ show_calendar()
    $ atmos(s1_mv_atmos)
    with wipeleft_scene
    play sound moddooropen
    show monika forward casual happ cm oe nobl rdown ldown at t11
    "Inside, the air conditioning cuts through the heat at once."
    "The lobby smells like popcorn, floor cleaner, and spilled cola that someone has already mopped but not quite defeated."
    "The line for concessions moves with practiced slowness."
    show monika at t21
    show kotonoha work neut at t22
    "At the register, Kotonoha slides a tray of nachos across the counter, checks the next order on the screen, and looks up."
    show kotonoha work neut
    mc "Yo."
    ko "Good afternoon, [player], Monika."
    "Her work shirt is neat beneath the concession apron, and the name tag sits exactly level."
    "Monika steps up beside me and studies the menu board."
    m forward casual happ cm oe nobl rhip ldown "Do you want anything?"
    mc "Maybe a drink, I guess."
    "She waits. The rest of the decision stays where she left it."
    mc "...And popcorn is probably smarter before the movie starts."
    m "Let's go with that then."
    ko "Combo B is cheaper with two drinks."
    m forward casual happ om oe nobl rhip ldown "Combo B, then, please. Medium popcorn."
    ko "Salted?"
    "Monika defers to me."
    mc "Sure."
    show monika forward casual laug om ce nobl rdown ldown at h21
    m forward casual laug om ce nobl rdown ldown "Salted and churro toppings!"
    mc "That is not what I ordered!"
    show monika forward casual happ om oe nobl rhip ldown
    "Kotonoha taps the order in and reaches for two cups with her eyes still on the register."
    show kotonoha work neut
    ko "{i}Iron Rod{/i} is in theater three. Doors open in five minutes."
    m forward casual lsur om oe nobl rdown ldown "Oh, that soon?"
    ko "The trailers are longer than usual."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Kotonoha spends the next half minute prepping our food and drinks."
    call nier_clear() from _call_nier_clear_0518_2
    pause 2.0
    scene bg theater_lobby
    $ show_calendar()
    $ atmos(s1_mv_atmos)
    with wipeleft_scene
    show kotonoha work neut at t22
    show monika forward casual happ cm oe nobl rdown ldown at t21
    ko "Your total is on the screen."
    "The number is higher than two snacks have any business being."
    "Monika pays before I get my wallet halfway out."
    mc "...I can get it. Seriously."
    m forward casual nerv om oe awkw rdown ldown "Hey, I was the one who invited you. I got this, brochacho."
    "Monika busies herself with the cup lids instead of answering."
    "I take the popcorn because it gives my hands something to do."
    ko "Enjoy the film."
    mc "Thanks, you too--"
    mc "...Uh..."
    m forward casual happ om oe blus rdown ldown "Thank you, Kotonoha!"
    show kotonoha at thide
    hide kotonoha
    show monika forward casual happ cm oe nobl rdown ldown at t11
    "Kotonoha nods once and turns to the next customer."
    "Past the concession stand, theater three waits with its doors propped open and a strip of red carpet rolled crookedly across the threshold."
    "Monika balances both drinks against her chest, then leans one toward me."
    m forward casual happ om oe nobl rdown ldown "Ready?"
    mc "...Sure."
    "She smiles, softer than before."
    show monika forward casual happ cm ce nobl rdown ldown
    m forward casual happ cm ce nobl rdown ldown "Good, me neither."
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
    "Theater three is dark so that it asks you to forget the outside world exists."
    "The screen is still blank, but the speakers are already filling the room with a low advertisement loop that makes every snack look like it was photographed by someone with too much confidence."
    "Monika finds our row before I do."
    m forward casual curi om oe nobl rdown ldown "This should be us..."
    "She steps aside to let me in first. I take the inside seat, partly because it's polite and partly because the aisle seat feels like it belongs to someone who has an escape plan."
    "The popcorn bucket lands between us."
    mc "You know, I feel like theater popcorn used to be cheaper."
    m forward casual wry cm oe nobl rdown ldown "Everything used to be cheaper."
    m forward casual happ om oe nobl rdown lpoint "That's how time works, don'tcha know?"
    mc "I don't like your tone, Ms. Economy."
    m forward casual laug om ce nobl rdown ldown "Then stop making easy observations, haha!"
    "I reach for popcorn and immediately regret it when the churro topping coats my fingers in a layer of cinnamon that could be entered as evidence."
    mc "...This is a crime."
    m forward casual happ om oe nobl rdown lpoint "It's good, though, right?"
    mc "That's {i}not{/i} what I said."
    $ theater_lights(0.78, secs=2.2)
    "She takes a piece for herself, then looks at the screen as the lights dim another step."
    "The room settles into the shared hush of strangers agreeing to be quiet at the same time."
    "{i}So why am I suddenly aware of the exact inch of air between our shoulders?{/i}"
    m forward casual curi om oe nobl rdown ldown "Hey."
    mc "Hm?"
    m forward casual happ cm oe nobl rhip ldown "You can laugh if the movie gets stupid, by the way."
    m "I won't report you to the horror fan committee."
    mc "...There's a committee?"
    m forward casual happ om oe nobl rdown lpoint "Obviously! They meet in a basement and argue about which VHS tapes are best all the friggin' time."
    mc "Sounds credible..."
    $ theater_lights(1.0, secs=1.1)
    play sound sfx_thunder
    "The opening starts with a thunderclap. Someone in the front three rows jumps."
    "She tries not to smile and fails miserably."
    show monika forward casual happ cm oe nobl rdown ldown
    "{i}Alright. Movie time.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    # DELIBERATE: the house lights are NOT cleared for these interludes. `scene`
    # only clears the master layer, so the projector wash carries over the black
    # and the narration plays against a screen that is still running. Clearing
    # and restoring it here would mean the film politely stops every time the
    # narrator summarizes it.
    nier "The movie opens on an empty railway crossing, a missing-person flyer, and a rural silence that makes the whole theater play the straight man."
    nier "Nobody in the room leaves. No one ever leaves. Horror runs on bad real estate decisions and people investigating noises any reasonable person would pay to never hear again."
    call nier_clear from _call_nier_clear_0518_3
    pause 2.0
    scene bg theater_inside
    $ show_calendar()
    $ atmos(s1_mv_atmos)
    show monika forward casual neut cm oe nobl rdown ldown at t11
    with wipeleft_scene
    "It's uneven, but when it works, it works. Monika watches with the focus she usually saves for poems."
    "I catch myself eyerolling at one point because of how much a scene insists upon itself."
    "About an hour in, the lead climbs into a maintenance tunnel he has no business entering."
    "The score thins down to a single held note. His flashlight finds a wall of something that should not be behind a wall."
    "Then a sound comes from off-screen, low and wet and far too close, and the whole theater does that collective half-flinch where everyone pretends they didn't."
    "Monika's hand closes around my sleeve."
    "Not even my hand, my {i}sleeve{/i} of all things."
    "I don't move, partly because the tunnel sound is genuinely doing numbers on my spine."
    show monika forward casual nerv cm oe blaw rdown ldown
    "On the next cut to daylight she lets go and smooths the fabric like she can erase the evidence, staring very hard at the screen the whole time."
    "Neither of us says a word about it while the movie is still happening."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The rest plays out the way these things do: one character makes a noble sacrifice, another makes a stupid one, and the titular iron rod collects exactly the amount of symbolic weight the budget could afford."
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
    "The credits crawl up the screen while half the audience begins the annual tradition of blocking the row before anyone can stand."
    "I stay seated, mostly because the people beside us are still negotiating popcorn logistics with the intensity of a hostage situation."
    m forward casual curi om oe nobl rdown ldown "...Well?"
    mc "I liked it."
    mc "The maintenance tunnel was a cheap shot, though."
    m forward casual happ cm oe nobl rhip ldown "Cheap shots work sometimes. That's sort of the whole point of them."
    "Her hand has drifted to her own sleeve, smoothing the same spot she grabbed on mine."
    mc "...Says the person who tried to tear my arm off, by the way."
    show monika at f11
    m forward casual flus om oe blaw rdown ldown "I didn't!"
    $ theater_lights(0.0, secs=1.3)
    "Her face goes pink faster than the house lights come up."
    m forward casual nerv om oe awkw rdown ldown "I was startled for maybe, like, half a second."
    mc "Talk about a grippy half-second then."
    m forward casual flus om ce blaw rhip ldown "Okay, okay! Fine, it got me {i}once{/i}!"
    "She folds her empty straw wrapper into a tiny rectangle, then folds it again."
    m forward casual pout om oe nobl rdown lpoint "But you jumped at the opening thunder."
    mc "Just a louder audio mix than I expected..."
    show monika forward casual laug cm ce nobl rdown ldown at t11
    m forward casual laug cm ce nobl rdown ldown "Suuuuuuuure, let's go with that."
    "We stand once the row clears, carrying the remains of our refreshments like raccoons smuggling out trash from a dumpster."
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
    play music daily
    "The lobby is full of spilled reactions now: people arguing over the ending, parents corralling children, someone near the poster loudly insisting the book did it better."
    ko "Was the movie satisfactory?"
    mc "That's a very...customer-service way to ask."
    m forward casual happ om oe nobl rhip ldown "It was good! A little amateurish at a couple points, but good."
    ko "Messy is usually more memorable."
    "She gathers abandoned napkins from the counter and stacks them with precision."
    show kotonoha work neut
    mc "You seen it yet?"
    ko "No. Employees are encouraged to avoid spoilers so we can maintain neutrality when customers yell about endings."
    mc "Sounds like a line from the handbook."
    ko "It should be."
    "Monika laughs into her cup lid."
    show monika forward casual happ cm oe nobl rdown ldown
    m forward casual happ om oe nobl rdown ldown "Rest assured, we won't yell, at least."
    ko "I appreciate that."
    "A customer waves from the other end of the counter. Kotonoha looks over, then back at us."
    ko "Have a good afternoon."
    mc "You too."
    m forward casual happ om ce nobl rdown ldown "Bye, Kotonoha!"
    show monika forward casual happ cm oe nobl rdown ldown at t11
    show kotonoha at thide
    hide kotonoha
    "She nods once and returns to work."
    "Monika and I drift toward the doors with the crowd."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg theater_day
    $ show_calendar()
    $ atmos(s1_mv_atmos)
    show monika forward casual happ cm oe nobl rdown ldown at t11
    with wipeleft_scene
    "[s1_mv_out]"
    "The line for the next showing has already started curling toward the poster again."
    "Neither of us moves."
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
            m forward casual laug om ce nobl rdown ldown "Oh, extremely."
            m "But they have good snacks and tea!"
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
    m forward casual nerv om ce blaw rhip ldown "I should probably head home before I talk myself into buying a second ticket just to overanalyze a five-second interaction."
    mc "...You'd do that?"
    m forward casual flus cm oe blus rdown ldown "No."
    m forward casual nerv om oe awkw rdown ldown "...Maybe."
    m forward casual happ om oe nobl rdown lpoint "Does it matter?"
    mc "Dangerous honesty."
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
    nier "The ride home gives me too much time to think, which is rude of public transportation."
    nier "The held note before the tunnel. The flashlight finding the wrong wall. The parts that worked and the parts that were only doing the bare minimum."
    nier "And that Matsuda girl's name, sitting in my messages like it rented space there."
    call nier_clear from _call_nier_clear_0518_6
    pause 2.0
    scene bg living_room
    $ show_calendar()
    $ atmos("evening")
    stop music fadeout 1.0
    with wipeleft_scene
    play music dailyleisure
    play sound moddooropen
    "When I get home, Asahina is still in the living room."
    "The poster is propped against the couch now, which means it has graduated from crisis to object."
    "Big block letters, clean spacing, and a volleyball drawn in more detail than anyone pretending not to care would bother with."
    show asahina curious at t11
    ah "Well?"
    mc "Well what?"
    show asahina teasing
    ah "Movie. Date. Whatever. Spill it."
    mc "It was...a movie."
    show asahina unamused
    ah "Wow. Thank you for the important info."
    "I take my shoes off and decide whether honesty is worth the ammunition."
    "Unfortunately, my mouth has historically been bad at being unilateral."
    mc "It was fun. Monika and I both seemed to enjoy it."
    show asahina teasing
    ah "Awwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww." # purposefully goes off the textbox as a meta gag
    show asahina smug
    mc "{i}Don't{/i}."
    ah "I didn't say anything!"
    mc "You said it with your stupid face."
    show asahina embarrassed
    ah "Shut up! You're one to talk!"
    mc "...How mature of you."
    "She leans back on her hands, then glances at the poster like she's pretending not to wait for me to notice it."
    mc "Poster looks good. Especially the lettering."
    show asahina nervous
    ah "...Yeah?"
    mc "Yeah."
    "She turns away too quickly."
    show asahina neut
    ah "Cool."
    ah "Now go away before your cinnamon smell ruins it."
    mc "Gladly."
    "I head toward the stairs, then stop near the first step."
    mc "Oh, and Asa?"
    ah "What?"
    mc "If the volleyball team doesn't appreciate the poster, I will personally call them tasteless swines."
    show asahina worried
    ah "Please don't, they're still my friends."
    mc "No promises."
    show asahina happy
    ah "...Thanks, birdbrain."
    "I keep walking, and the smirk stays on the side of my face she cannot see."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Sunday evening drifts in without asking permission."
    nier "Mom asks about the movie over dinner. Asahina answers half the questions for me, confidently, exaggerated, and incorrectly."
    nier "I correct none of it unless absolutely necessary."
    call nier_clear from _call_nier_clear_0518_7
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music fantasyserenity
    "My room is still when I finally get back to it, with the occasional rustle of leaves or trash outside."
    "My phone waits on my nightstand, considerably less quiet than everything around it."
    python:
        _phone_messages = [
            phone_msg("them", "Okay, theory: the iron rod wasn't actually the weapon. It was the promise."),
            phone_msg("them", "Wait, that sounded better in my head."),
            phone_msg("me", "No, keep going. I want to see how deep the committee corruption goes."),
            phone_msg("them", "You joke, but I have notes and stuff."),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0518_3
    "A movie, a poster, a few messages..."
    "{i}Normal things.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The rest of the night slips by in fragments: homework I remember too late, a game I open for exactly long enough to lose track of time, and Monika's theory messages arriving in theoretical clusters."
    call nier_clear from _call_nier_clear_0518_8
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0518_1
    jump a0519
