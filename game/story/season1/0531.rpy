label a0531:
    # --- Day 17: 2025-05-31 ---
    # Final day of Chapter 0.5. A scheduled noon dismissal for the main building's
    # ventilation replacement gives the cast a rare early start. The existing plan converges without Matsuda
    # manufacturing access: MC joins after track, Asahina joins after volleyball, and
    # Tsubaki gets the bookstore first. Matsuda becomes the day's center because the
    # group genuinely has fun with her, and the decisive next invitation comes from MC.
    # This is the clean, reciprocal beginning the later overdependence must grow from.
    # Ledger meters moved: MC wants another outing with Matsuda, with no date settled; Tsubaki
    # keeps and voices preferences; Asahina's edited schedule remains her own; Monika's
    # unfinished doorway poem retains weight; Mom's work stays ordinary but present.
    $ _exam_one_catch = exam_guard_scum_count() == 1
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music house_day_a
    "Mom is still at the table after the plates are mostly empty, her hair pinned up and both hands wrapped around her mug. There isn't a folder anywhere in sight."
    "Across from her, Asahina works through her toast with one knee bouncing under the table, sneaking looks at the clock whenever she thinks nobody's watching."
    show mom teasing at t22
    show asahina uniform determined at t21
    "She tears the toast in half and levels one piece at me across the table."
    ah "Arcade card? Charger? {i}Actual{/i} money?"
    mc "I survived outings for years before you appointed yourself logistics manager, you know."
    show asahina smug
    ah "Debatable."
    show mom smug
    mom "I was there for most of those outings, and I would also describe it as debatable."
    if _exam_one_catch:
        show mom neut
        mom "Before you leave this table, [player], I'd like to hear the terms once more. From you."
        show asahina unamused
        ah "Location stays on, he texts when track ends--"
        show mom unamused
        mom "I asked him."
        ah "I'm just saying, he knows that part."
        "Asahina reaches for the jam and finds both of us looking at her."
        mc "She's right about those, for the record. I also text when I get there and before food or any other change, and I'm home by eight-thirty unless I ask first and you say yes."
        mom "And the phone?"
        mc "Charged. The portable charger's packed, too."
        "Mom nods and lets the phone stay where it is, on my side of the table."
    "Mom's phone buzzes against the table. She reads the message and finishes her sip before she gets up and takes the phone over to the counter."
    show mom at thide
    hide mom
    show asahina curious
    ah "Work?"
    mom "A question that can survive until Monday."
    "She thumbs out a short reply and leaves the phone facedown on the counter when she comes back to the table."
    show mom determined at t22
    show asahina determined
    ah "Sunday rematch is still happening, right?"
    mom "After biology."
    "Asahina turns her phone around to show us tomorrow's schedule: one blue block of biology, forty-five minutes long, floating in an otherwise empty afternoon."
    ah "Forty-five minutes."
    show mom teasing
    mom "Forty-five honest minutes, and then you may deploy every unethical expansion card you own."
    show asahina smug
    ah "Finally, a fair deal."
    # SFX SUGGESTION: A phone vibration rattling audibly against the kitchen table.
    "My own phone has been rattling against the table this whole time, and the chat called Saturday has stacked up a row of notifications on the lock screen."
    python:
        _phone_messages = [
            phone_msg("them", "Matsuda: Dawn report! The bookstore opens at one, exactly one hour after our glorious maintenance dismissal!"),
            phone_msg("them", "Tsubaki: It's opened at one every Saturday for twelve years."),
            phone_msg("them", "Matsuda: And today we'll be standing at the door when it does. Reliability deserves a parade!"),
            phone_msg("them", "Asahina: some of us are trying to eat"),
            phone_msg("them", "Matsuda: Then eat magnificently!"),
            phone_msg("me", "Leave a few books for the rest of the city."),
            phone_msg("them", "Matsuda: Out of my hands. Kareda has discovered the clearance tables, and I no longer control our departure."),
            phone_msg("them", "Tsubaki: We haven't even left the house."),
        ]
    call phone_text_conversation("Saturday", _phone_messages, status="3 participants", append=True) from _call_phone_text_conversation_0531_1
    show asahina curious
    ah "She starts early."
    mc "The bookstore has shown dangerous consistency."
    ah "I meant {i}Matsuda{/i}."
    show mom smug
    mom "You sound amused."
    mc "I'm choosing patience."
    show asahina smug
    ah "You typed back in seven seconds."
    mc "Efficient patience."
    "Asahina shoots Mom a look of total vindication. Mom just drinks her tea."
    "Mom walks us to the door with her mug in hand while I make sure my track shoes haven't flattened my lunch."
    show mom happy
    mom "Have fun."
    show asahina happy
    ah "We'll try~"
    show mom smug
    mom "Good. I've got plans of my own, and they involve both of you being out of the house."
    mc "Say no more. We'll go be somebody else's problem."
    "The mug hides her mouth, but not the smile around her eyes."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "A crane waits behind orange fencing at the gates, the new ventilation unit strapped to its flatbed. Asahina takes it personally that the noon power cut is sparing the gym, and volleyball with it."
    nier "Morning classes crawl while the crane outside watches the clock as hard as we do, and in the group chat, Tsubaki vetoes two of Matsuda's route changes and an arcade dress code."
    # SFX SUGGESTION: The noon dismissal bell immediately overtaken by a roomful of chairs scraping back.
    nier "Chairs start scraping before the noon bell finishes. I'm halfway down the emptying stairwell when Monika calls my name from the landing above."
    call nier_clear from _call_nier_clear_0531_1
    stop music fadeout 1.0
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music day_a
    show monika forward uniform neut cm oe nobl rdown ldown at t11
    "Monika comes down the stairs two at a time, a canvas bag over one shoulder and yesterday's green pen clipped to its outside pocket."
    m forward uniform happ om oe nobl rdown lpoint "Wait up! I found the rest of the recipe!"
    mc "The onion soup?"
    m forward uniform happ cm ce nobl rdown ldown "There was a second page, and--okay, brace yourself--it gets {i}worse{/i}."
    "She reaches the landing, and we take the last flight together."
    m forward uniform wry cm oe nobl rhip ldown "Apparently the onions 'surrender their sorrow' now. I've read it four times, and I'm pretty sure that just means brown them."
    mc "Slowly, then. Leave the sorrow on low heat."
    m forward uniform nerv om oe nobl rdown ldown "See, {i}you{/i} get it! I'll send you the pages when I get home. We should actually try making it sometime."
    mc "I'd eat it. Probably. Let me read how it ends first."
    m forward uniform happ om oe nobl rdown ldown "So it's bookstore, arcade, and then the mysterious third location where everyone realizes they forgot to pick food?"
    mc "The group chat's stuck between noodles and burgers."
    m forward uniform laug om ce nobl rdown ldown "Someone's going to get hungry and decide for all of you. My money's on Asahina."
    "At the bottom of the stairs, sunlight from the courtyard doors stretches across the floor to meet us."
    m forward uniform happ om oe nobl rhip lpoint "And Monday, {i}one line{/i}, okay? I'm not assigning a second draft, so don't you dare hand me one."
    mc "The traveler has until then."
    m forward uniform neut cm oe nobl rdown ldown "Good. I'm looking forward to it."
    # SFX SUGGESTION: One coach's whistle blast from across the courtyard.
    "Out past the doors, the track team is collecting at the fence, and a whistle goes off once in warning."
    m forward uniform happ om oe nobl rhip ldown "Go, before Coach decides I'm the reason you're late."
    mc "Have a good Saturday, Ms. President."
    m forward uniform curi om oe nobl rdown ldown "You too. And, [player]?"
    mc "Yeah?"
    m forward uniform happ cm oe nobl rdown ldown "Have fun today, okay? You can tell me all about the racing game on Monday."
    mc "Yeah. I will."
    show monika forward uniform dist cm oe nobl rdown ldown
    "She hitches the canvas bag behind her shoulder so it won't knock against the door."
    m forward uniform happ om oe nobl rdown ldown "See you Monday!"
    mc "See you."
    show monika at thide
    hide monika
    "She heads for the front gate, and I cut across the courtyard toward the track."
    $ update_character_thought("monika", "Monika found the rest of the onion-soup recipe in an old journal and suggested we try making it. She still wants the traveler's last line on Monday.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Coach has set out cones and low hurdles across all six lanes, and from the gate, his promised {i}short practice{/i} already looks negotiable."
    call nier_clear from _call_nier_clear_0531_3
    stop music fadeout 1.0
    pause 2.0
    scene bg track_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music day_c
    "I eat lunch on the bleachers while Coach finishes with the first group, then warm up on the outside lane with cut grass clinging to my shoes."
    "Three runners go by at a pace I could match, and I let them have it. Strides are the prize today, and nobody earns those by winning the warmup."
    show track_coach neut at t11
    track_coach "Foot?"
    mc "Present. Quiet."
    track_coach "Keep it {i}boring{/i}."
    mc "You have a real gift for speeches."
    track_coach "And you have eight minutes of drills before I decide whether you get strides. High knees to the cone, walk back, and do not invent a race."
    "My hips loosen up by the second pass, but on the third my foot goes reaching out ahead of me, and his pen taps the clipboard before I'm back at the line."
    track_coach "Under you. Do not reach for ground that is already coming."
    "I fix it on the next pass. Then come four controlled strides, and I lean on the first one so hard that his whistle cuts me off short of the end cone."
    track_coach "What percentage was that?"
    mc "Eighty."
    track_coach "Now give me the honest number."
    mc "...Eighty-seven."
    track_coach "Your face said ninety-five, and your shoulders were trying for a hundred."
    mc "My face isn't calibrated."
    track_coach "Then I will calibrate your afternoon down to zero strides. Again at seventy-five."
    "Seventy-five feels embarrassingly easy for about four steps. Then my arms settle, the ground starts showing up where my feet expect it, and the stride starts carrying its own speed."
    "Coach lets me reach the cone."
    track_coach "That."
    mc "That was {i}slower{/i}."
    track_coach "That was {i}running{/i}. The first one was you fighting the track."
    "He makes a single mark on the clipboard."
    track_coach "Three more like it and you leave."
    "I run the last three at seventy-five and walk it off past the final cone while he watches my first few steps."
    track_coach "Anything?"
    mc "Nope."
    track_coach "No limp, either."
    mc "You sound disappointed."
    track_coach "I sound unemployed for the next forty-eight hours. Easy mileage tomorrow, and Monday we talk entries."
    "Sixteen, thirty-two, maybe both. I'm crossing the finish line of an invitational that doesn't exist yet when his pen swings up to point at me."
    track_coach "Don't run for the train if you're late."
    mc "Wasn't planning to."
    track_coach "And don't let your friends talk you onto a dance machine."
    mc "Racing cabinets. They have seats. I've planned this responsibly."
    "He finally lowers the clipboard."
    track_coach "Go be seventeen somewhere that does not have lanes painted on it, and hydrate before you leave."
    mc "There he is."
    show track_coach at thide
    hide track_coach
    "My foot's still quiet on the way out, and leaving before the distance group doesn't even sting."
    "I text the group chat that Coach has turned me loose, and Tsubaki writes back that they're still at the bookstore."
    if _exam_one_catch:
        "Before I'm out the gate, I open Mom's thread."
        python:
            _phone_messages = [
                phone_msg("me", "Leaving track now. Foot is quiet. Walking to the bookstore."),
                phone_msg("them", "Received. Walk."),
                phone_msg("me", "That was already the plan."),
                phone_msg("them", "Then we agree."),
            ]
        call phone_text_conversation("Mom", _phone_messages, append=True) from _call_phone_text_conversation_0531_exam_checkin_1
        "I lock the phone with a smile I don't bother flattening."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I walk to the station like Coach is watching. The used bookstore hides under a faded green awning, betrayed only by the clearance rack spilling onto the sidewalk."
    call nier_clear from _call_nier_clear_0531_4
    stop music fadeout 1.0
    pause 2.0
    scene bg bookstore
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music day_a
    "Inside, the air smells like old paper and floor wax, plus the patient dust of a business that has outlived several versions of the neighborhood."
    "Handwritten price cards hang over the narrow aisles, their red numbers crossed out and rewritten so many times that I have to follow the arrows to find out what anything costs."
    if _exam_one_catch:
        "I send {i}At the bookstore{/i} before I start browsing, and Mom answers with a single check mark."
    "Tsubaki is over at the old-magazine tables, two paper bags at her feet and a stack balanced against one forearm."
    show tsubaki uniform neut at t21
    "Matsuda crouches by a low shelf nearby, turning a mystery serial over to compare its cover against the blurb."
    show matsuda uniform thinking at t22
    ma "The missing violinist was obviously the landlord."
    show tsubaki uniform unamused
    ts "You've read three sentences."
    ma "And he's already mentioned the basement {i}twice{/i}! No innocent landlord needs that much basement."
    mc "Maybe he appreciates storage."
    "The book closes around one gloved finger as she turns."
    if s1_was("matsuda_bit", "flat"):
        show matsuda curious
        "She checks my face before anything else, and whatever she finds there earns me a greeting at normal indoor volume."
    else:
        show matsuda happy
        ma "Track has released him!"
        if s1_was("matsuda_bit", "play"):
            ma "Well, I'll be! Figured that coach'd keep you corralled till sundown, partn--"
            show tsubaki uniform unamused
            ts "You promised. No cowboy in the bookstore."
        elif s1_was("matsuda_bit", "tsubaki"):
            show tsubaki uniform smug
            "Over Matsuda's head, I mouth {i}how long?{/i} at Tsubaki. She mouths back {i}since one{/i} and returns to her magazines."
        "Two shoppers look up from the next aisle. Matsuda lowers the arm she flung up and tries again at a volume meant only for the three of us."
    show matsuda neut
    ma "Um... hi. I'm glad you made it."
    mc "Hey. Sorry, Coach wouldn't let me go until I'd proven I could run slowly."
    show tsubaki uniform worried
    ts "Is your foot okay?"
    mc "Didn't say a word all practice."
    show tsubaki uniform happy
    show matsuda unamused
    "Tsubaki's shoulders come down a notch. Matsuda pushes herself up off her heels and gives my shoes a suspicious once-over."
    show matsuda unamused
    ma "You {i}walked{/i} here?"
    mc "Under strict instruction."
    show matsuda teasing
    ma "Responsible! Deeply disturbing, but responsible."
    "She holds up the mystery serial, whose cover has crammed a mansion, a red window, an exhausted thunderhead, and a badly posed detective into one rectangle."
    ma "Seven volumes for the price of two! The prose looks {i}atrocious{/i}, but I simply must know how long the landlord can maintain his innocence."
    mc "You bought all seven?"
    "She nudges one of the paper bags with her toe. Its bottom is already bowing."
    show tsubaki uniform unamused
    ts "She bought nine."
    ma "Two are supplemental."
    show tsubaki uniform smug
    ts "One is a car magazine."
    ma "A mystery of engineering!"
    "Tsubaki shifts the stack on her arm: old school literary journals on top, their years handwritten on the spines, and a thin home-and-garden issue tucked underneath."
    mc "Any inflatable-sword casualties so far?"
    show tsubaki uniform teasing
    ts "Not yet."
    show tsubaki uniform happy
    ts "But look, I found spring poetry issues from four different schools, and they were practically {i}free{/i}!"
    mc "Any good?"
    show tsubaki uniform neut
    ts "This one's cover is my favorite. See, they carried the drawing all the way around the back."
    "Her thumb pins the top issue in place, and underneath the stack, her yellow notebook stays shut under its elastic."
    show tsubaki uniform curious
    ts "Some of them put contributor notes in the back, too. I want to see what they say about the writers."
    mc "You could make one of these, you know."
    show tsubaki uniform neut
    ts "I'd like to. I'd have to figure out how they printed them first."
    "Matsuda drops the latest mystery into her bag and drifts over to a rotating rack near the door."
    show matsuda smug
    ma "Behold! A cultural fossil!"
    "She plucks out an old children's television magazine, its cover crowded with bright lettering, smiling adults, and a foam creature whose seams I can see from several feet away."
    show tsubaki uniform curious
    "Tsubaki leans in for a closer look."
    ts "Wait, wasn't that the show you were on?"
    show matsuda unamused
    "Matsuda's fingers stop against one corner of the cover."
    mc "Hold on. You were on {i}television{/i}?"
    ma "The word {i}on{/i} is doing heroic work in that sentence."
    "She flips through the magazine much faster than she read the mystery, the pages whispering as they go."
    ma "I had three lines and one reaction shot. My relatives recorded it, in case any of us were ever in danger of forgetting."
    mc "How old were you?"
    ma "Old enough to remember it, and young enough to think craft services meant somebody was bringing us woodworking supplies."
    "Her thumb stops halfway through, and the next page never turns. Tsubaki sees the photograph over her shoulder."
    show tsubaki uniform neut
    ts "There."
    "The photo's too small to make out from where I'm standing, but Matsuda reads the caption twice and doesn't move on."
    show matsuda sad
    "Her thumb moves over the bottom line."
    ma "They spelled my name wrong."
    "She closes the magazine, smooths its bent corner, and slots it back into the rack with the cover facing out."
    mc "You don't want it?"
    ma "I own the episode."
    mc "I meant the magazine."
    "Her hand stays on the bent corner."
    ma "No."
    show tsubaki uniform sad
    "Tsubaki hugs her stack a little closer, and the pages settle softly between us."
    ts "Okay."
    show matsuda neut
    "A customer edges past us toward the register, and Matsuda steps aside with the heavy bag held close to her leg. For a minute or two, we drift with the ordinary traffic of the store."
    show matsuda smug
    "Then the arcade sign across the street flashes blue through the front window, and her chin comes back up."
    ma "Well! We have literature, several questionable mysteries, and an entire building of machines over there, begging to be humbled!"
    mc "You also have a car magazine."
    ma "Every afternoon is entitled to one generous definition of literature."
    show tsubaki uniform unamused
    ts "You said the car magazine was engineering."
    ma "Kareda! Do not split the canon in public!"
    show tsubaki uniform happy
    "Tsubaki lets a small laugh slip and carries her stack up to the register."
    show tsubaki uniform determined
    "Matsuda moves to set one of her bags on top of it, catches Tsubaki's look, and lowers it back to her feet."
    "The cashier ties the magazines up with twine. Tsubaki tests the knot, thanks him, and lifts the bundle herself."
    ma "Phase two?"
    show tsubaki uniform happy
    ts "Phase two."
    "They both turn to me."
    mc "I didn't follow Coach's walking orders this far just to admire the sign."
    show matsuda happy
    ma "Then let the machines tremble!"
    show matsuda smug
    "She's nearly at the door when she remembers her second bag, abandoned by the counter. By the time she doubles back, Tsubaki already has it."
    show tsubaki uniform smug
    ts "Inventory."
    ma "I was {i}coming back{/i} for it!"
    show matsuda neut
    "Matsuda takes the bag in both hands and settles its weight against the other one."
    ma "Thanks."
    show tsubaki uniform happy
    $ update_character_thought("tsubaki", "Tsubaki found four school poetry journals at the clearance table, bought them herself, and carried her own bundle. She plans to compare their contributor notes.")
    $ hide_calendar()
    scene black with wipeleft_scene
    # SFX SUGGESTION: Layered arcade ambience: cabinet music, synthetic engines, light-gun fire, and prize-machine jingles.
    nier "The arcade reaches us before its doors do. For once, Matsuda isn't the loudest thing in the building."
    call nier_clear from _call_nier_clear_0531_5
    stop music fadeout 1.0
    pause 2.0
    scene bg arcade
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music day_c
    "Blue and pink light slides across the carpet. Prize machines line one wall and racing cabinets the other, while the rhythm games thump away in the back."
    "Tsubaki rents a locker by the entrance for the books, and she checks the number on the key twice before she lets the door shut."
    show tsubaki uniform neut at t21
    show matsuda uniform thinking at t22
    "Matsuda turns a slow circle in the middle of the floor, surveying each section like a general choosing a battlefield, and ends up facing the racing cabinets."
    show matsuda uniform determined
    ma "Racing first."
    mc "You sound confident."
    ma "I have studied these machines at length and reached a conclusion."
    show tsubaki uniform unamused
    ts "She watched somebody play while I was paying."
    ma "Study takes many forms!"
    "She leads us to a pair of molded seats facing screens designed to encourage poor judgment, one cabinet marked red and the other blue."
    ma "Choose."
    mc "Does it matter?"
    show matsuda uniform teasing
    ma "Only if you lose and decide the color was responsible."
    "I claim blue and discover my card can barely afford one race, so I duck back to the kiosk while Matsuda waits in the red seat, rocking the wheel through its loose center."
    mc "Ready?"
    ma "I've been ready since the first wheel offended the first pedestrian."
    show tsubaki uniform worried
    ts "Please never drive outside the game."
    ma "Only inside the game!"
    "She picks something rear-wheel-drive and mean, and I pick whatever looks likeliest to survive my cornering."
    "At the green light, she launches hard, drifts the first turn, and comes out of it ahead with her mirror practically kissing the barrier."
    mc "You've played this before."
    ma "Not {i}this{/i} one."
    mc "That's a suspicious answer."
    ma "Eyes forward, sidewalk!"
    "I reel her in on the straight, and she blocks late, laughing when I dive inside anyway. The whole final lap turns into a shoving match over the same three feet of asphalt."
    "Red crosses the line less than half a second ahead of blue. Her hands are off the wheel before the results finish loading."
    show matsuda uniform smug
    ma "Behold! A decisive demonstration of natural supremacy!"
    mc "Half a second."
    ma "History rounds upward."
    "The results screen, unhelpfully, supplies the gap to three decimal places."
    show tsubaki uniform smug
    ts "History seems very specific."
    show matsuda uniform unamused
    ma "History is being {i}rude{/i}."
    "She's got one foot out of the seat when I tap continue, and she falls straight back into it."
    mc "Again."
    "The rest of her victory speech evaporates."
    show matsuda uniform curious
    ma "...Yeah?"
    mc "Unless natural supremacy has somewhere else to be."
    show matsuda uniform happy
    "Her grin comes back smaller, and a lot less ceremonial."
    ma "Run it."
    "The mountain course goes to me by one tire-width, mostly because I bounce off the guardrail on the last hairpin and it happens to fling me toward the line."
    mc "History rounds upward."
    show matsuda uniform annoyed
    ma "You used the {i}wall{/i}! That was fraud with a steering wheel!"
    mc "The wall participated voluntarily."
    show matsuda uniform happy
    "She tries to stay outraged and loses it to a laugh."
    show tsubaki uniform curious
    ts "Tiebreaker?"
    "Matsuda's {i}obviously{/i} lands on top of my {i}yeah{/i}."
    "The third course runs through rain-slicked city streets, and we trade first place so many times that we stop calling the contacts. Tsubaki, sitting with our bags between her shoes, is the only witness who could rule on any of it."
    "At the final turn Matsuda brakes early, and I dive for the gap on the inside. Only then do I notice she's left me exactly one line and made it the bad one."
    # SFX SUGGESTION: A sharp digital tire scrape and cabinet collision sound as blue clips the curb.
    "Blue clips the curb. Red slides past clean and takes it by 0.214 seconds."
    show matsuda uniform smug
    ma "Strategy."
    mc "Entrapment."
    ma "You lean left before you commit to an inside pass."
    mc "I do {i}not{/i}."
    show tsubaki uniform nervous
    ts "You do."
    "Tsubaki addresses the rest to the carpet."
    ts "Only a little. But you do."
    "Matsuda taps the side of her nose."
    ma "The Azure Eye misses nothing."
    mc "Retire that title before I demand video review."
    "She climbs out first and offers me a hand up out of the low seat with tremendous dignity. I take it, stiff from leaning into every corner the seat refused to lean into."
    ma "Good race."
    mc "Good trap."
    "Behind us, both cabinets slip back into attract mode and start advertising the race we just finished."
    show tsubaki uniform determined
    "Tsubaki picks next: a cooperative light-gun game. She frees her sleeve from the cable while Matsuda and I take the stations on either side of her."
    "The two of us spend the first stage yelling over the gunfire while Tsubaki quietly keeps every civilian alive, and when the tally comes up, her score sits above both of ours."
    show matsuda uniform shocked
    show tsubaki uniform embarrassed
    ma "{i}Kareda?!{/i}"
    ts "It was mostly timing."
    ma "You've been concealing this from us the {i}entire time?!{/i}"
    ts "I played it with my cousins last summer."
    mc "Next time, warn me before I put my initials in."
    "She sets the gun back in its cradle but keeps one hand on it."
    show tsubaki uniform happy
    ts "Can we do the next stage?"
    show matsuda uniform happy
    ma "Absolutely!"
    "Stage two ends with all three of us screaming at a helicopter that refuses to acknowledge conventional damage. When it finally goes down, Tsubaki's laugh rises over the explosions."
    "My phone buzzes in the middle of the score tally. Asahina."
    python:
        _phone_messages = [
            phone_msg("them", "Asahina: practice over. where are you"),
            phone_msg("me", "Back wall, by the light-gun games."),
            phone_msg("them", "Matsuda: Follow the sounds of victory!"),
            phone_msg("them", "Tsubaki: Or the blue racing cabinets. Those are easier to find."),
        ]
    call phone_text_conversation("Saturday", _phone_messages, status="3 participants", append=True) from _call_phone_text_conversation_0531_2
    "Asahina finds us a few minutes later, volleyball bag slung across her chest, and the carpet gets judged on sight."
    show asahina uniform disgusted at t33
    show tsubaki uniform happy at t31
    show matsuda uniform teasing at t32
    ah "Oh, firetruck, it's {i}warm{/i} in here! Did you guys pick the corner that smells the worst on purpose?"
    ma "The perfume of competition!"
    show asahina smug
    ah "Your perfume smells like unfettered ass."
    "Matsuda draws herself up to her full height on the building's behalf."
    ma "Lady Asahina graces us with her presence and {i}immediately{/i} insults our generous host!"
    show asahina unamused
    ah "Drop the {i}Lady{/i} or I swear you'll regret it."
    show matsuda neut
    ma "...Asahina. Welcome."
    show asahina neut
    ah "Hey."
    "Tsubaki puts one hand up between them like a crossing guard."
    show tsubaki uniform curious
    ts "How was volleyball?"
    show asahina teasing
    ah "Coach made us serve till the ball had a personal problem with every single one of us. What'd you guys do?"
    mc "Matsuda cheats at racing."
    ma "I {i}observe body language{/i}."
    ah "So she cheats with homework."
    show tsubaki uniform smug
    ts "I got the high score on the shooting game."
    show asahina shocked
    ah "Wait. {i}You{/i}?"
    show tsubaki uniform nervous
    "Tsubaki's fingers start toward her sleeve. The score screen is still up behind us, though, with TSK sitting above both of our names, and she looks back at it."
    show tsubaki uniform determined
    ts "Yeah. {i}Me{/i}."
    show asahina happy
    ah "Okay, sick! Show me."
    "Her hand drops away from the sleeve."
    "We move to the four-player cabinet, where Asahina opens fire on every corner and yells an apology at each civilian she clips."
    show asahina frustrated
    ah "Why do they keep running in front of me?!"
    mc "They mistake volume for authority."
    ah "Shut up and cover the stairs!"
    show tsubaki uniform determined
    "Tsubaki covers the stairs. Matsuda covers everything else, and I spend the boss fight reviving Asahina while she accuses the game of targeting her personally."
    "Tsubaki keeps the high score."
    show asahina determined
    ah "Rematch later. I need a game that respects athletic ability."
    "Matsuda volunteers the dance cabinet and the one song she knows, and two minutes later she's hanging off the handrail like it's choreography. Asahina wins by too much for an honest excuse."
    show matsuda frustrated
    ma "The machine showed clear hometown bias!"
    show asahina smug
    "Asahina hops off the platform flushed and smug, and Sam's name lights up the phone in her open bag. She fires off a reply one-handed and reaches for her water with the other."
    show tsubaki uniform worried
    show matsuda neut
    ts "Everything okay?"
    show asahina neut
    ah "Yeah, Sam just wanted to know if practice ran late. I told him I'm here."
    "She drops the phone back into the bag with the screen still lit."
    show asahina happy
    ah "So! What're we wrecking next?"
    "Matsuda points us toward the prize machines, and we drift after her."
    show tsubaki uniform curious
    "Tsubaki slows in front of a claw cabinet stuffed with cloth birds in impossible colors. A pale yellow one is wedged near the chute, its flattened beak squashed against the glass, and she keeps looking back at it after she's walked past."
    show matsuda curious
    show tsubaki uniform neut
    "Matsuda stops dead beside the cabinet."
    ma "Kareda."
    show tsubaki uniform unamused
    ts "No."
    ma "I haven't proposed anything!"
    show tsubaki uniform smug
    ts "Your hand is on your arcade card."
    "Matsuda removes her hand from the card."
    show matsuda teasing
    ma "The card and I were merely discussing possibilities. Nothing had been decided."
    show tsubaki uniform neut
    ts "I don't need it."
    ma "You don't have to {i}need{/i} it. Look at that face and tell me it hasn't suffered."
    show tsubaki uniform worried
    ts "It'll take too many tries."
    show matsuda determined
    "Matsuda leans against the side glass, tracing the path from the claw down to the bird."
    ma "Then let me try once."
    show tsubaki uniform frustrated
    ts "Matsuda."
    ma "One try. If the machine rejects us, the card goes away, and destiny can sit and think about its choices."
    show tsubaki uniform sad
    "Tsubaki's eyes go from the bird to the card waiting in Matsuda's hand."
    show tsubaki uniform determined
    ts "One."
    "Matsuda taps her card and lines the claw up over the bird, nudging it once as the timer starts counting down."
    mc "No pressure."
    ma "Please. Let me concentrate on the very serious bird."
    # SFX SUGGESTION: Claw-machine motor whir, metal clack, then the plush landing with a soft cabinet thump.
    show tsubaki uniform shocked
    "The claw closes around the bird's middle and carries it almost to the chute before one prong slips. The bird bounces once and lands farther from the opening than it started."
    show matsuda uniform pose_facepalm
    "Nobody says a word until it stops rolling. Matsuda lets go of the joystick and puts her whole hand over her face."
    ma "Son of a--I have been betrayed by geometry."
    show matsuda uniform unamused
    show tsubaki uniform happy
    "Tsubaki laughs first, and only covers it once Matsuda presses close to the glass to ask the bird to remember who tried. Then Matsuda straightens up and puts the card away."
    show tsubaki uniform sad
    "Tsubaki touches two fingers to the glass by the bird's beak before she follows us."
    ts "Maybe next time."
    show tsubaki uniform neut
    "Matsuda loses air hockey on a disputed goal and is still filing her appeal when she plants herself beneath a curtain printed with four cartoon faces."
    show matsuda teasing
    ma "A photo booth! A record for posterity!"
    show asahina unamused
    ah "Of what?"
    ma "Survival. Fellowship. The decisive defeat of several machines!"
    show tsubaki uniform unamused
    ts "Don't call it fellowship."
    ma "Nobody in this group respects branding."
    "She ducks through the curtain, consensus or no consensus."
    show matsuda at thide
    hide matsuda
    "We stop to shove the bags clear of the entrance, and by the time I straighten up, the curtain has fallen shut behind her."
    # SFX SUGGESTION: A photo-booth countdown chirp, then one bright camera flash.
    "Inside the booth, a countdown starts chirping."
    ma "Wait, where did everybody--"
    "The flash beats everybody to an answer."
    "On the preview screen, Matsuda sits alone on the bench, holding the curtain aside and looking out at us."
    show asahina smug
    ah "Great teamwork."
    "The curtain opens, and Matsuda takes in the three of us, then the preview."
    show matsuda uniform unamused at t32
    ma "The machine attacked before the party had assembled!"
    mc "You pressed start."
    ma "The button was {i}deceptive{/i}."
    "A second countdown starts, and Matsuda pins the curtain open with one hand."
    show matsuda neut
    ma "You're getting in, right? {i}All{/i} of you?"
    show tsubaki uniform determined
    ts "Bags stay outside. Tall people in the back."
    ah "Who put you in charge?"
    ts "The booth has one bench and four seconds. {i}Move!{/i}"
    "That gets us moving."
    show asahina at thide
    show tsubaki at thide
    show matsuda at thide
    hide asahina
    hide tsubaki
    hide matsuda
    "Tsubaki takes the front corner with Matsuda beside her, and Asahina and I wedge in behind them wherever we fit. The booth was designed for four people who don't need to breathe."
    "Matsuda's ponytail gets in my mouth twice before the flash."
    ma "Frame two: Fellowship Redeemed!"
    ah "I will leave."
    ma "Frame two: {i}Saturday{/i}."
    ah "Better."
    "The second flash gets Matsuda mid-correction and Tsubaki losing her fight with a laugh. During the next countdown, Matsuda throws both hands in the air until Tsubaki reaches over and pulls one of them down."
    ts "One normal one."
    ma "Define normal, quickly!"
    "This time, all four of us are looking at the lens."
    "Nobody has a plan for the last countdown. Asahina gives Tsubaki rabbit ears."
    "Tsubaki catches her at it just as Matsuda twists around to look, and I'm still laughing when the booth fires."
    "We spill back out into the arcade one shoulder at a time."
    show tsubaki uniform happy at t31
    show matsuda uniform happy at t32
    show asahina uniform happy at t33
    "The printer spits out two identical strips: Matsuda alone, her correction, the normal one, and the last frame nobody was ready for."
    show matsuda thinking
    ma "We could crop out the ambush."
    show tsubaki uniform neut
    ts "Don't. The timing's funny."
    "Matsuda studies the first frame a little longer before she answers."
    ma "...Fair."
    "Tsubaki tucks one strip into her yellow notebook, and I slide the other behind my arcade card with one white edge left showing."
    "By now, evening has reached the windows. Our cards are lighter, and my legs are tired in a way that belongs to the whole day instead of one injury."
    show tsubaki uniform neut
    "Matsuda reclaims the bookstore bags while Tsubaki runs a hand around the inside of the empty locker, just in case."
    show matsuda happy
    ma "Food! Before somebody mistakes a vending machine for dinner."
    ah "Burgers."
    show tsubaki uniform thinking
    ts "Could we try the cafe across from the station? I want somewhere quieter for a while."
    show asahina uniform curious
    ah "Do they even {i}have{/i} burgers? I'm starving, and some tiny little sandwich isn't gonna fix it."
    ts "I usually get the soup. They might?"
    "I pull up the menu on my phone, and Asahina leans over my shoulder to scroll past the drinks herself."
    mc "Burgers, sandwiches, and chairs that don't vibrate."
    show asahina uniform neut
    ah "Fine, that works. I'm getting fries, too."
    show matsuda happy
    ma "Excellent! Lead us to the stationary furniture!"
    show tsubaki uniform happy
    "Tsubaki heads for the doors with Matsuda on her heels, and I open Mom's thread on the way out."
    if _exam_one_catch:
        python:
            _phone_messages = [
                phone_msg("me", "Leaving the arcade. Cafe across from the station for food."),
                phone_msg("them", "Received. Home by eight-thirty."),
                phone_msg("me", "Yes."),
            ]
    else:
        python:
            _phone_messages = [
                phone_msg("me", "Leaving the arcade. Cafe across from the station for food."),
                phone_msg("them", "Thank you. Let me know when you head home."),
                phone_msg("me", "Will do."),
            ]
    call phone_text_conversation("Mom", _phone_messages, append=True) from _call_phone_text_conversation_0531_exam_checkin_2
    $ update_character_thought("matsuda", "Matsuda beat me two races to one, used one try at the claw machine after Tsubaki set the limit, and called all of us into the photo booth after its first frame caught her alone. Tsubaki kept one strip, and I took the other.")
    $ update_character_thought("asahina", "Asahina joined us after volleyball, made Tsubaki show off her shooting-game high score, and then beat Matsuda badly at the dance cabinet.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The storefronts have lit up while we were inside, and our reflections crowd into the same windows all the way to the cafe."
    call nier_clear from _call_nier_clear_0531_6
    stop music fadeout 1.0
    pause 2.0
    scene bg cafe
    $ show_calendar()
    $ atmos("evening")
    with wipeleft_scene
    play music house_day_a
    "The cafe gives us a table by the window with a basket underneath for bags. Tsubaki lowers her bundle in with both hands, and Matsuda's nine-volume purchase lands beside it with a thump that rattles the spoons."
    "Four definitions of dinner become soup and toast for Tsubaki, a chicken sandwich for Asahina, burgers for Matsuda and me, and a basket of fries that Asahina starts raiding before her own plate even arrives."
    "Matsuda asks whether the largest burger has historical significance. Nobody can tell her, so she orders the normal one."
    "The food has barely landed when the bookstore story slips out."
    show tsubaki uniform neut at t31
    show matsuda uniform unamused at t32
    show asahina uniform shocked at t33
    ah "You were on {i}TV?!{/i}"
    "Matsuda's eyes cut to Tsubaki, who lowers her menu very carefully and studies its edge."
    show tsubaki uniform embarrassed
    ts "It came up naturally! The magazine was {i}right there{/i}."
    ma "The bookstore unearthed archival propaganda."
    ah "Wait, what show?"
    ma "A kids' adventure show from overseas with color-coded adults, practical lessons, and monsters made mostly of foam. The works."
    show asahina happy
    ah "Okay, that's lowkey amazing."
    ma "It lasted thirteen episodes, so history was less enthusiastic."
    ah "Still counts! Who were you?"
    "Matsuda tears into her napkin packet and spreads the contents across her lap with enormous care."
    ma "I played a student in episode seven. I found a malfunctioning weather device, said three lines, and displayed age-appropriate concern."
    show tsubaki uniform teasing
    ts "You also screamed."
    ma "Four essential vocal contributions, all performed with conviction."
    show asahina curious
    ah "Oh my God, please tell me somebody put this online."
    show matsuda neut
    ma "Probably. But {i}no{/i}."
    show asahina neut
    "Asahina clocks how fast that answer came and takes a drink instead of asking her next question. She holds off until Matsuda starts folding the empty napkin sleeve."
    ah "Did people at your old school find it, or was it just... I dunno, around?"
    show matsuda unamused
    "Matsuda folds the sleeve badly and gives up on straightening it."
    ma "They found a rerun. By lunch, everybody had seen it and formed a complete opinion."
    ma "Then my family crossed an ocean, I started here in April, and... well, everybody already knew where they sat."
    ma "Standard transfer-student speedrun, more or less. Anyway, the landlord remains guilty."
    show tsubaki uniform determined
    ts "And they spelled her name wrong in the magazine."
    show asahina annoyed
    ah "Are you {i}serious?!{/i}"
    ma "A small typo aimed at a very small celebrity. I really don't want to turn it into a whole event."
    mc "Fair. The weather device can keep the story to itself."
    show matsuda neut
    ma "It didn't."
    show asahina neut
    "For a while, forks and glasses are all we hear. Outside the window, one lit train pulls in and another pulls out."
    "Asahina eats half her sandwich fast, then slows down and lines the leftover fries up along the edge of her plate. Tsubaki nudges the shared pickles closer, and Asahina takes one, her eyes still on Matsuda."
    show matsuda thinking
    show tsubaki uniform thinking
    "Matsuda's case against the landlord rests on three basement scenes, while Tsubaki insists the violinist staged her own disappearance. By the time my plate is empty, everyone on the back cover has been accused of something."
    show asahina thinking
    ah "What if the violinist just... left?"
    ma "Without explaining herself?"
    ah "People do that."
    show tsubaki uniform unamused
    ts "The title is {i}The Violinist Who Never Left{/i}."
    show asahina smug
    ah "Marketing lies."
    show matsuda teasing
    ma "Such skepticism! You may join the inquiry. All nine volumes, naturally."
    show asahina unamused
    ah "Then I resign."
    show tsubaki uniform neut
    "Once the plates are nearly clear, Tsubaki checks the train schedule and starts collecting the paper scraps around her plate."
    ts "I should go in about twenty minutes."
    ma "Curfew?"
    show tsubaki uniform embarrassed
    ts "Mm-hm. The 7:18 gets me home in time."
    ma "Then the 7:18 it is. We'll deliver you to it personally."
    show asahina neut
    ah "Mom wants a text when we leave, right?"
    mc "Yeah. She knows about the food, just not the train."
    if _exam_one_catch:
        python:
            _phone_messages = [
                phone_msg("me", "Still at the cafe. Leaving in about twenty minutes with Asahina."),
                phone_msg("them", "Received. Home by eight-thirty, both of you."),
                phone_msg("them", "Thank you for checking in when you said you would."),
                phone_msg("me", "We're on time."),
            ]
    else:
        python:
            _phone_messages = [
                phone_msg("me", "Still at the cafe. Leaving in about twenty minutes with Asahina."),
                phone_msg("them", "Thank you. Home by eight-thirty."),
                phone_msg("them", "And bring your sister with you."),
                phone_msg("me", "I was planning to."),
                phone_msg("them", "I enjoy written confirmation."),
            ]
    call phone_text_conversation("Mom", _phone_messages, append=True) from _call_phone_text_conversation_0531_3
    show asahina teasing
    ah "She thinks you're gonna trade me for arcade credit."
    mc "The exchange rate is terrible."
    show asahina smug
    ah "You couldn't afford me."
    ma "I could broker the deal."
    mc "Don't encourage her."
    show tsubaki uniform embarrassed
    "Tsubaki abstains by way of the ceiling. When the check comes, four hands go for it at once, and we end up splitting it four ways."
    "Matsuda moves to exempt the fries she stole as a cultural exchange, and the motion dies without a second. Asahina takes the cash up to the counter for change, and Tsubaki goes with her to buy a wrapped cookie for the train."
    show asahina at thide
    show tsubaki at thide
    hide asahina
    hide tsubaki
    show matsuda uniform neut at t11
    "With the other two at the counter, Matsuda squares the empty sugar packets into a loose stack, knocks one crooked, and starts over."
    ma "Can I ask you something without making it a whole production?"
    mc "You can attempt one."
    show matsuda nervous
    "She keeps her eyes on the sugar packets."
    ma "Was today actually good for you? You got quiet when we sat down, and I couldn't tell if you were tired or waiting to leave."
    "Her finger flattens the top packet and stays there."
    mc "Tired, yeah. But it was good. I'd even fight the helicopter again."
    show matsuda curious
    "She looks up so fast that the loose stack shifts under her hand. Behind the counter, the espresso machine hisses as a train slides past the window."
    # The invitation itself is fixed -- it is the capstone proof that MC can
    # start something instead of waiting to be started. Only HOW he says it is
    # the player's.
    menu:
        "(Say it plainly.)":
            $ s1_pick("arcade_offer", "plain")
            mc "I actually {i}want{/i} to do this again."
            mc "There's another arcade across town with four racing cabinets and the full version of the game we just played."
            "Matsuda's thumb goes still on the sugar packet."
            show matsuda unamused
            ma "I've heard of it. {i}Extensively.{/i}"
            mc "Of course you have."
        "(Hide it behind the racing game.)":
            $ s1_pick("arcade_offer", "excuse")
            mc "There's another arcade across town with four racing cabinets and the full version of the game we just played, so... we should probably investigate."
            "Matsuda's thumb goes still on the sugar packet."
            show matsuda unamused
            ma "For research."
            mc "Naturally."
        "(Almost don't.)":
            $ s1_pick("arcade_offer", "almost")
            "I get as far as opening my mouth. Matsuda looks back down at the sugar packets and leaves me to get there on my own."
            mc "There's another arcade across town with the full version of that racing game, and I thought maybe we could--you know."
            "Matsuda's thumb goes still on the sugar packet."
            ma "Go there? Together?"
    show matsuda smug
    "The smile she's trying to keep in reaches one corner of her mouth first."
    mc "Yeah. We could go sometime."
    show matsuda curious
    ma "We?"
    mc "You, me, and whoever else wants another shot at the helicopter."
    "She glances over at the counter, where Tsubaki is counting change into her palm and Asahina is arguing that two coins stuck together should still count as two."
    show matsuda thinking
    ma "{i}Sometime{/i} has a lot of room in it."
    mc "That's usually what the word means."
    show matsuda happy
    ma "What about next weekend?"
    show matsuda nervous
    ma "Or--no, later. Sorry, you've got track, and the invitational. It doesn't {i}have{/i} to be next weekend."
    mc "The invitational's in two weeks, so next Saturday might be messy."
    ma "Then not next Saturday."
    mc "Maybe after school one day. We don't have to settle it before they come back."
    show matsuda neut
    ma "Yeah. We'll figure it out."
    ma "And, uh... I'm glad you came today."
    mc "Thanks for only entrapping me on the last race."
    ma "Then come prepared next time."
    show tsubaki uniform neut at t31
    show asahina uniform curious at t33
    "Asahina and Tsubaki come back to find Matsuda folding the top sugar packet into ever-tinier squares."
    show matsuda uniform smug at t32
    ah "Why do you two look guilty?"
    mc "Sugar business."
    ma "Need-to-know."
    show tsubaki uniform curious
    ts "Does it affect the train?"
    ma "The 7:18 is untouched."
    show tsubaki uniform happy
    ts "Good."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Tsubaki's train comes first, and Matsuda reminds her about the cookie until the doors close. Then she hauls her nine mysteries to the opposite platform."
    call nier_clear from _call_nier_clear_0531_7
    stop music fadeout 1.0
    pause 2.0
    scene bg city_evening
    $ show_calendar()
    $ atmos("evening")
    with wipeleft_scene
    play music night_b
    "We walk home under streetlights and the last of the blue in the sky. Asahina spends the first two blocks insisting her volleyball bag isn't heavy, and by the third, it has somehow migrated to my shoulder."
    show asahina uniform curious at t11
    ah "So."
    mc "Dangerous opening."
    ah "Matsuda."
    mc "Still a person."
    show asahina unamused
    ah "I {i}know{/i}, I met her. Kinda hard to miss."
    "She steps over a crack in the pavement and nudges a bottle cap along with the side of her shoe."
    show asahina neut
    ah "She's... actually fun."
    mc "You sound surprised."
    show asahina teasing
    ah "You made her sound like weather with a phone number."
    mc "Weather can be fun from inside a structurally sound building."
    show asahina smug
    ah "You raced her {i}three times{/i}."
    mc "The third was necessary."
    ah "And then the minute we went up for change, you started pitching her another arcade."
    mc "You were {i}listening{/i}?"
    ah "Bro, the whole register was listening."
    show asahina neut
    "A few steps later, she kicks the bottle cap into the gutter."
    ah "If you guys do this again, tell me."
    mc "You're already in the chat."
    show asahina embarrassed
    "She grabs the strap of my track bag as it swings toward a railing and hangs onto it until we're past."
    ah "Then don't schedule it during volleyball, dumbass. I mean... I'd go."
    mc "A moving endorsement."
    show asahina annoyed
    ah "Don't make me take it back."
    "At the next light, her phone buzzes, and she checks it while we wait for the signal."
    mc "Sam?"
    show asahina neut
    ah "Mom. She wants to know if we're at the crossing yet."
    "She sends a picture of the signal instead of typing an answer."
    show asahina smug
    ah "There. She gets the entire traffic light."
    "The light changes, and we take our time crossing."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The front window is lit when we get home, and Mom opens the door while we're still on the path. Asahina calls it surveillance. Mom says our argument got here first."
    call nier_clear from _call_nier_clear_0531_8
    stop music fadeout 1.0
    pause 2.0
    scene bg living_room_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music house_day_a
    "The Copper Crown box is waiting on the coffee table beside Mom's closed laptop and a legal pad with three abandoned lines on it. Mom lifts Asahina's bag off my shoulder and sets it by the stairs."
    show mom unamused at t22
    show asahina uniform smug at t21
    if _exam_one_catch:
        show mom neut
        mom "Eight twenty-three. Location on, and every check-in exactly where you said it would be."
        mc "Foot stayed quiet, too. Practice was clean."
        mom "Good. That's two things I didn't have to ask about."
    else:
        mom "Eight twenty-three."
        ah "Seven minutes early!"
        show mom teasing
        mom "I'm deciding how responsibly to spend them."
        mc "Roll them over. The foot stayed quiet, by the way, and practice was clean."
        show mom smug
        mom "That isn't how credit works in this house, but I'll accept the report."
    show asahina teasing
    ah "He walked so slow the moss nearly passed him."
    mc "You gave me your bag."
    show asahina unamused
    ah "Unrelated."
    "Mom checks my shoes, then Asahina's bag, then the kitchen."
    show mom neut
    mom "There's food left if the cafe didn't happen."
    show asahina neut
    ah "It happened."
    show asahina happy
    "Asahina drops onto the couch with one leg folded under her."
    ah "I {i}destroyed{/i} Matsuda at the dance game!"
    show mom teasing
    mom "That sounds like fun for at least one of you."
    "Mom turns to me, but I'm busy replaying the trap on that rain-slicked final turn."
    mc "Yeah. It was fun."
    show mom happy
    mom "Good."
    "She picks up her mug, discovers it's empty, and keeps holding it anyway."
    show asahina smug
    ah "He and Matsuda are already planning arcade round two."
    mc "We {i}mentioned{/i} one."
    ah "He proposed it."
    show mom thinking
    "Mom raises one eyebrow at me over the empty mug."
    mc "I didn't propose anything. I told her another arcade exists."
    ah "And {i}then{/i} said we could go."
    show mom neut
    mom "I see."
    "She carries the mug off to the kitchen and leaves the word where she put it."
    show mom at thide
    hide mom
    mc "Go shower. You smell like the dance machine."
    ah "Already did at school."
    mc "Then go be smug upstairs."
    ah "I can multitask."
    show asahina happy
    "She gets up anyway and collects the volleyball bag, then pauses on the bottom step."
    ah "Wake me up before Copper Crown tomorrow."
    mom "Biology first."
    show asahina annoyed
    ah "I wasn't talking to you!"
    mom "I can still hear you."
    "Asahina stomps upstairs."
    show asahina at thide
    hide asahina
    "Mom comes back with water in the mug and takes the chair beside the closed laptop."
    show mom curious at t11
    mom "{i}You{/i} proposed it?"
    mc "There really is another arcade."
    show mom thinking
    mom "I believed that part."
    "She drinks and waits for the part I left out."
    mc "...Today was good."
    "Her pen stays across the top of the legal pad."
    if _exam_one_catch:
        mom "You kept every part of today's agreement."
        mc "I said I would."
        mom "And you did."
        mom "Your phone may stay upstairs tonight. The laptop still waits until after Monday's advisor meeting."
        mc "Okay."
    show mom happy
    mom "Go rest. You're starting to blink one eye at a time."
    show mom neut
    "Mom waits until I'm on my feet before she opens the laptop, and the legal pad stays untouched beside it."
    mom "Goodnight, [player]."
    mc "Night, Mom."
    $ hide_calendar()
    scene black with wipeleft_scene
    if _exam_one_catch:
        nier "My phone comes upstairs with me tonight. My laptop stays on the coffee table beside Mom's until Monday."
    else:
        nier "The house settles behind me as I carry the unfinished line upstairs."
    nier "For once, I showed up for the whole day on purpose."
    call nier_clear from _call_nier_clear_0531_9
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music night_a
    "When I empty my pockets, the photo strip slides out from behind my arcade card."
    "Its first frame still has Matsuda alone in it, holding the curtain aside and looking out."
    "I prop it face-out against the lamp and pull the club draft out of my bag."
    "The train runs past the final station toward a staircase with no footprints, and at the bottom of the page is the ending I added yesterday:"
    "{i}listen for a television in the next room{/i}"
    "{i}and someone putting away dishes.{/i}"
    "Underneath, Monika's question waits in green ink."
    "{i}Does the traveler go inside?{/i}"
    "I'm still deciding what comes next when the phone buzzes."
    python:
        _phone_messages = [
            phone_msg("them", "Matsuda: Final accounting! Two racing victories, one tactical loss, one helicopter destroyed, and zero birds liberated."),
            phone_msg("them", "Tsubaki: You lost air hockey too."),
            phone_msg("them", "Matsuda: The table was uneven."),
            phone_msg("them", "Asahina: and the dance game lmao"),
            phone_msg("them", "Matsuda: This chat has become hostile to accurate history!"),
            phone_msg("me", "Sounds like a good day to me."),
            phone_msg("them", "Tsubaki: It was."),
            phone_msg("them", "Asahina: yeah"),
            phone_msg("them", "Matsuda: Yeah."),
        ]
    call phone_text_conversation("Saturday", _phone_messages, status="3 participants", append=True) from _call_phone_text_conversation_0531_4
    "The group chat winds down. Then, after the screen has dimmed, a private message comes in."
    python:
        _stance = s1_stance("arcade_offer", "plain")
        if _stance == "excuse":
            _phone_messages = [
                phone_msg("them", "Research log, day one: I had fun today."),
                phone_msg("me", "Peer review concurs. Mostly because you only won two races."),
                phone_msg("them", "A statistical anomaly. Day two will correct it."),
                phone_msg("me", "We'll see about that."),
                phone_msg("them", "We will."),
                phone_msg("them", "Goodnight, " + player + "."),
                phone_msg("me", "Night, Matsuda."),
            ]
        elif _stance == "almost":
            _phone_messages = [
                phone_msg("them", "You finished it, by the way."),
                phone_msg("me", "Finished what?"),
                phone_msg("them", "The sentence. At the cafe. I was fully prepared to let it die on the sugar packets."),
                phone_msg("me", "It was a short sentence."),
                phone_msg("them", "It counted. I had fun today."),
                phone_msg("me", "So did I. Mostly because you only won two races."),
                phone_msg("them", "A mercy I will not repeat."),
                phone_msg("me", "We'll see about that."),
                phone_msg("them", "We will."),
                phone_msg("them", "Goodnight, " + player + "."),
                phone_msg("me", "Night, Matsuda."),
            ]
        else:
            _phone_messages = [
                phone_msg("them", "I had fun today."),
                phone_msg("me", "So did I. Mostly because you only won two races."),
                phone_msg("them", "A mercy I will not repeat."),
                phone_msg("me", "We'll see about that."),
                phone_msg("them", "We will."),
                phone_msg("them", "Goodnight, " + player + "."),
                phone_msg("me", "Night, Matsuda."),
            ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, append=True) from _call_phone_text_conversation_0531_5
    "Further down, there's a message from Monika I missed at the arcade: two photographed pages of onion soup, rhyming the whole way down. I leave the ending for tomorrow."
    "I set the phone beside the draft and let the screen go dark."
    "The strip's last frame catches the lamplight: all four of us, still moving when the flash went off."
    if _exam_one_catch:
        "Monday still means an advisor and the zero I earned."
    else:
        "Monday brings the grades."
    "The draft is open under my hand tonight."
    "I roll the pen between my fingers until it taps the desk, loud in the quiet room."
    "This time, I don't stop."
    "{i}The door is already open.{/i}"
    $ update_character_thought("matsuda", "An old magazine showed Matsuda in a foreign television episode that classmates at her former school later found in reruns. Her family crossed an ocean before she started at Itsuki in April, and I kept one photo-booth strip before suggesting the next arcade trip myself.")
    $ hide_calendar()
    window hide(None)
    stop music fadeout 5.0
    pause 2.0
    scene black with dissolve_scene_full
    $ atmos_clear()
    pause 4.0
    call calendar_advance(days=1) from _call_calendar_advance_0531_1
    pause 2.0
    call enter_m_prologue_trailer from _call_enter_m_prologue_trailer_0531_1
    # End-of-Chapter-0.5 archive opening. Curated on purpose: an explicit list,
    # not a loop over the catalog, so a story added later does not arrive
    # pre-unlocked, and so Purgatorium opens HERE and not before the main story
    # has had its slow read of Sam.
    #
    # ONLY THE MUSIC ROOM IS A SECTION UNLOCK NOW. The other five Archive panels
    # ship open and fill in as they are earned -- roster slots as people are met,
    # CGs as they are shown, tracks as they are heard (see the flag block in
    # game/archive.rpy). The Music Room is the exception because it is the reward
    # for finishing the campaign, and Chapter 0.5 is where the campaign currently
    # ends. WHEN SEASON 1 PROPER SHIPS, this line moves to its ending.
    python:
        # NUDGE P0.5: confirm this ending (trailer, "The Music Room is open.", title). ach_grant is commented out, so P4 checks Curtain Call via chapter05_completed.
        # NUDGE P0.5: renpy.save_persistent() below is commented out too. Uncomment just that line (8-space indent) so the unlock survives a crash before quit.
        persistent.archive_unlocked_music = True
    #     # This stays here even when the Music Room gate eventually moves: it is
    #     # the permanent signal for finishing the currently playable Chapter 0.5.
        persistent.chapter05_completed = True
        # Exactly the stories the end card below announces. Ontological Seer
        # stays sealed while its announcement line is commented out.
        for _key in (
            #"cs_matsuda_01_unlocked", not ready yet
            #"cs_matsuda_02_unlocked",
            "cs_tsubaki_01_unlocked",
            "cs_tsubaki_02_unlocked",
            "cs_asahina_01_unlocked",
            "cs_sam_01_unlocked",
            "cs_kotonoha_01_unlocked",
            "cs_kotonoha_02_unlocked",
        ):
            setattr(persistent, _key, True)
    #     # Exact event hook for Curtain Call (For Now). The achievement also has
    #     # a derived chapter05_completed fallback for old saves and reconciliation.
    #     ach_grant("music_on")
        renpy.save_persistent()
    call nier_enter from _call_nier_enter_0531_unlocks
    nier "The Music Room is open."
    nier "Side stories unlocked:"
    # nier "Matsuda: {i}Ontological Seer{/i}"
    nier "Tsubaki: {i}Heads{/i}, {i}Tails{/i}"
    nier "Asahina: {i}Hina's World{/i}"
    nier "Sam: {i}Purgatorium{/i}"
    nier "Kotonoha: {i}The Girl with Every Face{/i}, {i}The Void Hunter{/i}"
    call nier_exit from _call_nier_exit_0531_unlocks
    return
