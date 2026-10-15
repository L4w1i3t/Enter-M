label a0525:
    # --- Day 11: 2025-05-25 ---
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music house_day_a
    # SFX SUGGESTION: A phone alarm, tinny and close, looping with no fade.
    "The alarm gets into the dream first."
    "It spends a while being a smoke detector, then a truck backing up, and then it's just my phone on the desk, doing exactly what I asked it to."
    "7:15, with three more alarms queued up behind it on Asahina's orders."
    "I could reach the phone if I got one arm out from under the blanket."
    "{i}I told her nine.{/i}"
    # The one sanctioned skip in Chapter 0.5. The prompt states the cost in
    # plain language on purpose -- a player who does not want a study session
    # is allowed to skip it deliberately, not tricked into it. See
    # s1_sleep_in.rpy for the full contract.
    menu:
        "The alarm keeps going."

        "Get up.":
            $ s1_sleep_in_set(False)
            "I get one arm out and shut it off mid-impression. The rest of me stays under the blanket on principle."
            # SFX SUGGESTION: Sparse house ambience: a pipe tick, low refrigerator hum, and one car passing outside.
            "A pipe ticks somewhere in the wall, and one car goes by outside. Nobody else in the house is up."
            "My bag's already packed by the desk. Apparently last night's me had a lot more faith in this morning's me than Asahina does."
            "{i}So I really have to go out today, huh? Kinda did this to myself.{/i}"
            "I sit up in one go. Negotiating with the blanket has never once gone my way."

        "Ignore it. {i}(Sleep in and skip the study session.){/i}":
            $ s1_sleep_in_set(True)
            "I turn it off."
            "Then the other three, so they won't go off while I'm deciding what to text her."
            "{i}Five minutes. I'll text her at seven-thirty, and it'll be fine.{/i}"
            "The blanket agrees with me. It has no reason to lie."
            jump a0525_slept_in
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg kitchen
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    "A covered plate is waiting on the counter, and Mom's note is stuck down beside it."
    call enter_m_show_sticky_note(("Breakfast.", "Text when you arrive.", "Do not live on pastries."), signature="Mom") from _call_enter_m_show_sticky_note_0525_1
    "I've barely got the cover off when my phone pings."
    python:
        _phone_messages = [
            phone_msg("them", "Morning! Are you awake?"),
            phone_msg("me", "Awake. Eating breakfast."),
            phone_msg("them", "Oh good, I was about to call."),
            phone_msg("me", "The alarm handled it. Several times."),
            phone_msg("them", "I'm leaving in a few minutes. I'm bringing flashcards and a frankly terrifying amount of sticky notes."),
            phone_msg("me", "Define terrifying."),
            phone_msg("them", "You'll know it when you see it."),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0525_1
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "With Asahina asleep upstairs, breakfast goes down tax-free for once."
    nier "I text Mom from the library steps, then put my phone on silent."
    call nier_clear from _call_nier_clear_0525_2
    stop music fadeout 1.0
    pause 2.0
    scene bg city_morning
    $ show_calendar()
    $ atmos_clear()
    with wipeleft_scene
    play music day_c
    "The library's doors are already propped open, but the cafe next door still has its chairs upside down on the tables."
    "{i}Even the chairs get a lie-in.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    scene bg library
    $ show_calendar()
    $ atmos_clear()
    with wipeleft_scene
    "The second floor smells like new carpet, and somebody has numbered the window seats since the last time we were here."
    show monika forward casual dist cm oe nobl rdown ldown at t11
    "Monika has fortified number four with a stack of index cards and a wall of sticky notes sorted by color. Terrifying, as promised."
    "She's mid-yawn when I reach the table, so she finishes it into her hand and sits up straight."
    m forward casual happ om oe nobl rdown ldown "Look who made it~"
    mc "They kept your window seats."
    m forward casual happ om oe nobl rhip ldown "They did! You have to book them now, so I booked one last night, and I've been sitting here since it opened feeling very smug about it."
    mc "And the films?"
    m forward casual wry cm oe nobl rhip ldown "Moved. The man at the desk wouldn't tell me where, which I've decided to take personally."
    mc "...I'll find them."
    "The chair across from her is one of the new ones, built to tip you toward the table whether you asked it to or not."
    m forward casual happ om ce nobl rhip lpoint "Aren't they amazing? My back hasn't complained once."
    mc "Mine's already drafting a formal complaint."
    show monika forward casual nerv cm oe awkw rdown ldown
    "First, as promised, we swap clean copies of yesterday's poems. Both of us put them away unread, like that's a normal thing to do."
    "I peel a sticky note off her yellow stack and write out the rules for the run."
    "{i}1. Nobody looks at an answer until we've both committed.{/i}"
    "{i}2. Nobody says \"I'm good.\"{/i}"
    m forward casual curi cm oe nobl rdown ldown "Number two feels targeted."
    "I manage not to make the number-two joke."
    mc "It's preventive."
    "She takes the pen and adds a third rule in green."
    "{i}3. Ties go to whoever brought the sticky notes.{/i}"
    mc "You just wrote yourself the tiebreaker."
    m forward casual laug om ce nobl rdown ldown "It's a rule with a very small electorate!"
    "I take the pen back and give her rule a neighbor."
    "{i}4. Loser buys dessert at the cafe.{/i}"
    m forward casual happ om oe nobl rhip lpoint "Two years of trading first and second, and {i}now{/i} you want to put dessert on it? I'm in, obviously, I just want it noted that this was your idea."
    mc "Class rank takes all year. This one's over by noon."
    "I rule a line under number four and split the rest of the note into two columns, hers and mine."
    m forward casual curi om oe nobl rdown ldown "Okay, before the cards. How's it going?"
    mc "Monday's standing behind me, breathing through its mouth."
    m forward casual happ cm ce nobl rdown ldown "That's disgustingly vivid."
    mc "You?"
    m forward casual happ om oe nobl rdown ldown "I'm good!"
    "I tap rule two."
    m forward casual nerv om ce blaw rdown ldown "That was a reflex!"
    m forward casual neut om oe nobl rdown ldown "...Tired. A little nervous. I was making cards until one."
    mc "Nervous, same. I slept, though."
    m forward casual wry cm oe nobl rhip ldown "Congratulations on your eight hours."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Civics goes to her. I burn ten minutes insisting a national minimum can stop a region from going stricter, until she asks me since when a floor is a ceiling."
    nier "Then she takes the licensing case with one question: did anybody get a hearing?"
    nier "Language arts comes back to me. Her passage has a woman wiping a counter that's already clean while her guest puts his coat on, and I call it stalling a full sentence ahead of her."
    nier "By half past ten, the tables around us are filling up. One tally in each column, and rule three hands the tie to the sticky notes for now."
    call nier_clear from _call_nier_clear_0525_3
    pause 2.0
    scene bg library
    $ show_calendar()
    $ atmos_clear()
    show monika forward casual neut cm oe nobl rdown ldown at t11
    with wipeleft_scene
    m forward casual neut om oe nobl rdown ldown "My pick, then. Chemistry."
    mc "That's my worst one."
    m forward casual happ om oe nobl rhip ldown "I know! I read your review guide."
    "She slides a second stack across the table. Yellow cards, my subjects, her handwriting."
    mc "You made cards for my classes."
    m forward casual neut om oe nobl rdown ldown "From the photos you sent. You'd have done the same for mine."
    "{i}I would have sent her a link.{/i}"
    m forward casual happ om oe nobl rhip lpoint "Biology's the warmup. Chemistry's for the tally."
    m forward casual curi om oe nobl rhip ldown "Okay, outsider question. On the cross problems, I'd have counted the big piles, but it's the tiny ones that tell you how far apart the genes are?"
    mc "Yep. The tiny ones are the crossovers. Count those, and that's your distance."
    m forward casual happ om oe nobl rhip lpoint "And the sea star's basically our council treasurer. Barely shows up on the graph, and the whole shore falls apart without it."
    mc "Small isn't the same thing as unimportant. I'm telling your treasurer you said that, though."
    "Down on the street, the cafe next door has turned its chairs right side up."
    "Chemistry gets pen caps."
    m forward casual neut om oe nobl rhip lpoint "Each cap is one-tenth of a mole. Two aluminum plus three chlorine gas makes two aluminum chloride."
    m forward casual curi om oe nobl rhip ldown "We start with three caps of each and get sixteen-hundredths of a mole of product. What limits it, and what's the yield?"
    menu:
        "Chlorine limits it. The yield is eighty percent.":
            $ s1_pick("library_chem", "right")
            mc "Chlorine. Three caps of it only cover two of aluminum, so two-tenths of a mole is the most we could make."
            mc "Sixteen-hundredths over two-tenths. Eighty."
            m forward casual happ cm oe nobl rdown ldown "Eighty! I got that too, once I stopped dividing by the starting amount."
            show monika forward casual pout cm oe nobl rdown ldown
            "She draws my tally herself. Two to one, and it's the most reluctant straight line I've ever seen."
        "Aluminum limits it. The yield is about fifty-three percent.":
            $ s1_pick("library_chem", "wrong")
            mc "Aluminum runs out first. Fifty-three percent, give or take."
            m forward casual curi om oe nobl rhip ldown "Try building one batch with the caps."
            "Two aluminum caps and three chlorine caps go into the first batch. One aluminum cap is left over with nothing to react with."
            mc "...Chlorine limits it. Two-tenths is the most we could make, so it's eighty."
            m forward casual happ om oe nobl rhip lpoint "That's exactly where I went wrong when I made the card! Last night, though, and nobody was keeping score last night."
            "The tally goes in her column. Two to one, her favor."
        "Neither limits it. The yield is eighty percent.":
            $ s1_pick("library_chem", "wrong")
            mc "They start even, so neither one limits it. Eighty percent."
            m forward casual nerv om oe awkw rdown ldown "That's what I wrote on the card the first time."
            "We put two aluminum caps and three chlorine caps into one batch. One aluminum cap is left over."
            mc "...So chlorine limits it. Same eighty, better reason."
            m forward casual neut om oe nobl rhip lpoint "Right number, wrong reason. I don't do partial credit."
            "Her column gets the mark, and she's up two to one."
    "The last card in the stack has a pencil draft on the back, crossed out but legible."
    "{i}pH 3 is three-fourths as acidic as pH 4?{/i}"
    mc "One pH unit is ten times the hydrogen ions, not a quarter off. That's worth a tally."
    m forward casual flus om ce blaw rdown ldown "It was in pencil, Mr. Smartass! Pencil isn't binding."
    "Her own folder is still under her elbow, right where it's been all morning."
    mc "Come find the films with me. I need to stand up."
    m forward casual happ om oe nobl rdown ldown "Only if I get to pick one too."
    "The films turn out to be on the mezzanine, six carpeted steps up behind the magazines."
    "I take them slowly. The foot doesn't hurt, exactly, but two hours in that chair has given it opinions."
    m forward casual curi om oe nobl rdown ldown "How's the foot?"
    mc "I'm good."
    "She pulls the rules out of her sleeve and taps number two. She brought the scoreboard."
    mc "...Stiff from sitting. It loosens up once I walk."
    m forward casual happ om oe nobl rhip ldown "Then we'll take the long way back, and I'll tell everyone it was my idea."
    "The mezzanine is two shelves of films and a display stand holding a book of old movie posters, open to a giant lizard eating a train."
    mc "That one. I want to see that one."
    m forward casual curi om oe nobl rhip ldown "You don't even know what it's about."
    mc "It's about a lizard eating a train."
    m forward casual laug om ce nobl rdown ldown "Okay, but {i}why{/i} is it eating the train?"
    mc "Because the train's carrying the one thing that can hurt it, and it knows. That's why it skipped the city."
    m forward casual vsur om oe nobl rdown ldown "...Okay, that's actually good."
    mc "It's the obvious reading."
    "She flips past a city on fire until she finds a spaceship painted over a desert, with three people standing very small underneath it."
    m forward casual happ om oe nobl rdown ldown "This one's mine. Look how small they made the people."
    mc "Pitch it."
    m forward casual neut om oe nobl rdown ldown "The ship's been hanging there so long that the whole town sets its clocks by the shadow, and then one morning the shadow's gone, and nobody wants to be the first one to look up."
    mc "...Okay. Yours is better. Don't you dare write that down."
    "She reads the caption under the painting, then reads it again."
    m forward casual anno om oe nobl rhip ldown "The spaceship never appears in the film."
    "{i}It's also three hours long. The caption mentions that part in smaller print.{/i}"
    m forward casual anno om oe nobl rhip ldown "Oh, come {i}on{/i}!"
    show monika forward casual nerv cm oe awkw rdown ldown
    "Somebody below the mezzanine shushes us."
    "I photograph the caption for evidence, and we go back down with our faces pointed at the carpet."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "We take the long way back, past a story time where nobody is afraid of the dragon puppet."
    nier "By the time we sit down again, the sun has crossed the table to her side."
    call nier_clear from _call_nier_clear_0525_4
    pause 2.0
    scene bg library
    $ show_calendar()
    $ atmos_clear()
    show monika forward casual neut cm oe nobl rdown ldown at t11
    with wipeleft_scene
    "Algebra is my pick, since she's the one who asked me to check hers."
    m forward casual neut om oe nobl rdown ldown "Then check this one. I don't trust it."
    "{i}Log base 3 of (x plus 2), plus log base 3 of (x minus 4), equals 3.{/i}"
    "Underneath, in careful green: {i}x equals 7 or negative 5.{/i}"
    m forward casual happ om oe nobl rhip lpoint "Find what's wrong with it, and the tally's yours. Miss it, and it's mine."
    "Her arithmetic is clean. It usually is."
    m forward casual curi om oe nobl rdown ldown "Well?"
    menu:
        "She kept negative five, which makes both inputs negative.":
            $ s1_pick("library_alg", "caught")
            mc "Negative five doesn't work. Plug it back in, and both logs are taking negative numbers."
            m forward casual pout om oe nobl rdown ldown "I checked that one twice!"
            mc "You checked the arithmetic twice."
            "She crosses out the negative five hard enough to dent the next page, then gives me my tally with the same pen pressure."
        "She should have added the inputs, not multiplied them.":
            $ s1_pick("library_alg", "missed")
            mc "You multiplied the inputs. Shouldn't they add?"
            m forward casual curi om oe nobl rhip ldown "Adding the logs multiplies the inputs. I'm almost sure."
            "Rule one says we check the key now. The back of her packet says seven, and only seven."
            "I plug negative five into the original, and both logs end up with negative numbers inside them."
            mc "You were right about the multiplying."
            m forward casual wry cm oe nobl rhip ldown "And wrong about the answer. You can say the whole sentence."
            "The point's hers. I committed to adding, and rule one doesn't take amendments."
        "Nothing. Both roots solve the quadratic.":
            $ s1_pick("library_alg", "missed")
            mc "Looks right to me. Both roots solve the quadratic."
            m forward casual curi om oe nobl rdown ldown "Then why does the key only say seven?"
            "We plug negative five back into the original, and both logs end up taking negative numbers."
            mc "...We both missed it."
            m forward casual happ om ce nobl rdown ldown "Good. I'd hate to be wrong by myself."
            "Then she marks it down in her own column."
            mc "You're scoring a point off your own mistake?"
            m forward casual happ om oe nobl rhip lpoint "I'm scoring it off {i}yours{/i}."
    show monika forward casual neut cm oe nobl rdown ldown
    "Her rational function hides the same kind of trap. Canceling a factor tidies up the formula, but the input the original banned stays banned."
    "She writes {i}still excluded{/i} in the margin and underlines it twice."
    "Foreign language is last. For the listening section, she gives me one of her earbuds, and the cord's short enough that we end up shoulder to shoulder."
    "We both miss the same question."
    m forward casual nerv om oe blus rdown ldown "...Well. At least we're consistent."
    mc "No blood. Play it again."
    "The second time, we both catch it: he moves the meeting because of the lab, not the weather."
    show monika forward casual dist cm oe nobl rdown ldown
    "Then I make her say {i}if I had slept last night, I would be awake right now{/i} until the tenses stop fighting. She yawns on the fifth try."
    "Her phone rattles against the table. Noon."
    m forward casual lsur om oe nobl rdown ldown "Already?"
    "Every table on the floor is taken now, and the man at the desk has started turning people away from the window seats."
    if s1_was("library_chem", "right") and s1_was("library_alg", "caught"):
        "Three tallies in my column. One in hers."
        m forward casual pout om oe nobl rdown ldown "Recount."
        mc "It's four marks."
        m forward casual wry om oe nobl rhip ldown "Recount {i}slower{/i}."
    elif s1_was("library_chem", "right") or s1_was("library_alg", "caught"):
        "Two tallies in each column. Two lines up, rule three waits in green."
        mc "...You wrote yourself the tiebreaker."
        m forward casual happ om ce nobl rhip lpoint "And you wrote rule four right underneath it, which I'm pretty sure means you agreed to it!"
    else:
        "One tally in my column. Three in hers."
        mc "...Best of seven?"
        m forward casual happ om ce nobl rdown ldown "Nope! I've been looking forward to that dessert since half past ten."
    mc "How many of yours did you get to?"
    show monika forward casual dist cm oe nobl rdown ldown
    "She tucks the pen back into the loop on her folder. The folder stays shut."
    m "I'll do mine tonight."
    mc "That isn't a number."
    m forward casual wry om oe nobl rhip ldown "I know! It's a time, though. Times are basically numbers."
    m forward casual happ om oe nobl rdown ldown "Come on. The cafe's about ten minutes from here, and we're taking the flat way."
    "Packing up turns up two stray sticky notes in her sleeve and one stuck to my knuckles."
    "I fold the rules into my wallet, tallies and all. That's where contracts go."
    "I text Mom that the library part's done and the cafe's next. Her reply beats my zipper closed."
    "{i}Actual lunch. Not a bunch of sweets.{/i}"
    m forward casual happ cm ce nobl rdown ldown "She knows you~"
    mc "Can you not peer over my shoulder like that...?"
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 1.0
    pause 2.0
    scene bg city_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music day_a
    "The sidewalks narrow once we reach the historic district, and Monika walks with her folder tucked under one arm, checking every stone building for the old bank."
    show monika forward casual happ cm oe nobl rdown ldown at t11
    m forward casual curi om oe nobl rhip ldown "Did you remember the name of that space film?"
    mc "I took a picture of the caption. Want it?"
    m forward casual happ cm ce nobl rdown ldown "Yes, please! I still want to see it, even without the ship."
    "We stop at a crosswalk while a bus exhales at the curb."
    mc "The caption also said three hours."
    m forward casual wry om oe nobl rhip ldown "You left that part out!"
    mc "I was hoping you'd discover it independently."
    m forward casual happ om oe nobl rdown ldown "We can stop halfway through. You don't have to finish a film just because you started it."
    mc "I need to know whether the ship turns up."
    m forward casual laug om ce nobl rdown ldown "You already know it doesn't!"
    "An old bookstore on the next block has handwritten recommendations taped inside its window, and the one I stop to read gives away the ending."
    "Once I say so, Monika has to lean in and read every word of it."
    "The old bank turns up at the end of the block, all pale stone and tall windows. Across from it, a green awning shades a storefront full of plants."
    m forward casual happ om oe nobl rdown lpoint "There we are! Does finding it get me a tally?"
    mc "Scoring closed at noon."
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 1.0
    jump a0525_cafe


# -----------------------------------------------------------------------------
# THE SLEEP-IN BRANCH. Reached only from the alarm menu at the top of the day.
# Skips the entire library segment and rejoins at the cafe. Contract lives in
# s1_sleep_in.rpy; nothing here punishes the player for taking it.
# -----------------------------------------------------------------------------
label a0525_slept_in:
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 2.0
    pause 3.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    "When I wake up, the sun has crossed the desk and reached the patch of wall it usually gets to around lunch."
    "11:47."
    "I check the clock a second time, then open Monika's messages."
    # SFX SUGGESTION: A phone unlocking, then three notification chimes stacked close together.
    "There are three waiting, and the timestamps are worse than the messages."
    python:
        _phone_messages = [
            phone_msg("them", "I'm here! They kept the window seats. I booked the one with the outlet."),
            phone_msg("them", "Everything okay?"),
            phone_msg("them", "I started on your cards without you. They say hi."),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0525_3
    "8:58. 9:22. 10:05."
    "I type a joke about the alarm, delete it, and start over. She's been waiting nearly three hours."
    python:
        _phone_messages = [
            phone_msg("me", "I'm up. I'm sorry."),
            phone_msg("me", "I turned the alarm off and went back to sleep. I should've texted you."),
            phone_msg("them", "Okay."),
            phone_msg("them", "Thank you for not saying your phone died."),
            phone_msg("me", "I know you booked the table. I'm sorry I left you sitting there."),
            phone_msg("them", "I was worried when you didn't answer."),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0525_4
    "I'm still working out what to say to that when her next message comes in."
    python:
        _phone_messages = [
            # NUDGE P1.2 (consider skipping): the plan wants this to cost something tomorrow, but s1_sleep_in.rpy promises "NOT PUNISHED... she lets him off, once, and means it." Pick one.
            phone_msg("them", "It's okay! Really."),
            phone_msg("them", "I got through civics and language arts, and your cards are finished, so the morning wasn't a total loss. For one of us."),
            phone_msg("them", "Kidding! Mostly."),
            phone_msg("me", "I can come now."),
            phone_msg("them", "The booking ends at noon, so you'd get here just in time to help me carry the sticky notes."),
            phone_msg("them", "Lunch is still on, though. The cafe with the plants, 1:30?"),
            phone_msg("me", "You don't have to do that."),
            phone_msg("them", "I know. I still want lunch with you."),
            phone_msg("them", "Now go eat something! You've been asleep since yesterday."),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0525_5
    "I type {i}thank you{/i} three different ways and send the shortest one."
    "Then I set a single alarm for when I need to leave and get dressed with the conversation still open on the desk."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Downstairs, Mom's plate is still covered beside a note telling me to text when I arrive. I eat standing up, which the note probably has opinions about too."
    nier "From the bus, I text her that I missed the library and I'm on my way to lunch. Her reply asks whether I've apologized to Monika."
    call nier_clear from _call_nier_clear_0525_10
    pause 2.0
    scene bg city_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music day_a
    "I step aside for a stroller and nearly swing my arm into a shop sign, because I'm used to having a bag over that shoulder."
    "Pale stone and tall windows mark the corner where the old bank sits, exactly where she said it would be."
    "Across from it, Monika is waiting under the cafe's green awning. I raise a hand, she raises hers, and then there's nothing to do but wait for the light."
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 1.0


label a0525_cafe:
    pause 2.0
    scene bg cafe
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music tendermoment
    "The cafe used to sell stationery, and its narrow wooden shelves now hold ceramic cups between trailing plants."
    "A bag of coffee by the register has a label with more to say about itself than I do most mornings."
    "A couple by the window collects their coats, leaving a table open between two potted ferns."
    show monika forward casual happ cm oe nobl rdown ldown at t22
    show kotonoha work neut at t21
    "Kotonoha stands behind the register in a dark apron, using the edge of the counter to level a row of paper cups."
    mc "Afternoon, Kotonoha."
    ko "Good afternoon."
    m forward casual happ om oe nobl rdown ldown "Hi, Kotonoha!"
    ko "Hello, Monika."
    mc "Looks like we caught your Sunday shift."
    ko "I'm here until four."
    show monika forward casual curi cm oe nobl rdown ldown
    "A small menu stands beside the register, and Monika reads every line of it. I get as far as {i}toasted chicken sandwich{/i} and stop pretending the rest has a chance."
    m forward casual curi om oe nobl rhip ldown "Is the rosemary soup good?"
    ko work thinking "Yes. The bread is better with it."
    m forward casual happ cm oe nobl rdown ldown "I'll have the soup with bread and an iced tea, please."
    mc "Chicken sandwich and iced coffee, please. And a small pastry, if you have one."
    ko "The lemon cake is small."
    if s1_slept_in:
        mc "Lemon cake, then. Thanks."
    elif s1_was("library_chem", "right") and s1_was("library_alg", "caught"):
        mc "Lemon cake, then. She's buying."
    else:
        mc "Lemon cake, then. I'm buying, under protest."
    "Kotonoha adds it to the order and reads it back from the screen."
    ko work neut "You can take the window table. I'll bring the food over."
    m forward casual happ om oe nobl rdown ldown "Thank you!"
    show kotonoha at thide
    hide kotonoha
    show monika forward casual happ cm oe nobl rdown ldown at t11
    "We claim the table between the ferns. Outside, buses pull in along the far side of the old bank and carry pieces of the street away."
    "Monika sets her folder on the seat beside her instead of between us."
    if s1_slept_in:
        "It's been opened and closed a lot for a Sunday. The edges of the tabs have gone soft."
        m forward casual happ om ce nobl rdown ldown "Oh, this is nice."
        mc "...You did the whole morning anyway."
        m forward casual wry cm oe nobl rhip ldown "That's your first observation?"
        mc "It was the one at the front."
    else:
        "For the first time since nine, the table has no work on it."
        m forward casual happ om ce nobl rdown ldown "Oh, this is nice."
        mc "The chairs are objectively better than the library."
        m forward casual wry cm oe nobl rhip ldown "That's your first observation?"
        mc "My back has a voice, and I respect it."
    "Kotonoha brings the drinks first. I move my coffee by the rim to make space for the little number stand."
    "Monika's eyes follow my hand, then settle on the cup."
    m forward casual nerv cm oe awkw rdown ldown "...Huh."
    mc "What?"
    "She doesn't answer, so I look at whatever she's looking at."
    "{i}A table near the window. Two cups. My hand on the rim--{/i}"
    "Her cup is still waiting for a lipstick mark. Outside, the buses practice leaving."
    mc "You cheated."
    m forward casual vsur om oe nobl rdown ldown "What?"
    mc "Your poem yesterday."
    show monika forward casual vsur cm oe blus rdown ldown
    "Color arrives at her cheeks in stages."
    m forward casual flus om oe blaw rdown ldown "I didn't cheat!"
    mc "You wrote today before it happened."
    m forward casual flus cm oe blus rdown ldown "I wrote a table. Tables aren't exactly--"
    m "...They're not rare, is my point."
    mc "The two cups by the window? The buses outside?"
    "She looks through the glass at a bus pulling away from the curb, which does very little for her defense."
    m forward casual nerv om ce blaw rdown ldown "Okay, maybe I had a specific table in mind."
    mc "You hadn't even been here yet."
    m forward casual nerv om oe awkw rdown ldown "I kept thinking you'd take that seat."
    "Her thumb draws a slow, clear path through the condensation on her glass."
    m forward casual neut om oe blus rdown ldown "I wanted to sit here with you. The poem got a little ahead of me."
    if s1_slept_in:
        mc "I'm glad you still wanted lunch."
        m forward casual neut om oe nobl rdown ldown "Me too. I would have been more annoyed eating on my own."
        mc "I can at least help with that part."
    else:
        mc "It did."
        m forward casual curi om oe nobl rdown ldown "The poem?"
        mc "Today, so far."
    "Her shoulders loosen."
    m forward casual happ cm ce blus rdown ldown "I'm glad."
    "A little lipstick reaches the edge of her glass when she drinks."
    "Over at the counter, the register jams, and Kotonoha fixes it at the same speed she does everything else."
    if s1_slept_in:
        mc "Did you get to any of your own stuff? Once you were done with ours, I mean."
        m forward casual nerv om oe awkw rdown ldown "Some. I finished your cards first."
        mc "Even chemistry?"
    else:
        mc "You spent more time on my subjects than yours."
        m forward casual wry om oe nobl rhip ldown "You needed to do them."
        mc "I know, but you stayed up until one making cards for two classes you don't even take."
    "She glances toward the folder on the neighboring chair."
    m forward casual nerv om oe awkw rdown ldown "Making those was easier than staring at my own notes."
    mc "Oh."
    "The espresso machine starts up behind the counter. We let it fill the space until it's done."
    m forward casual neut om oe nobl rdown ldown "I keep thinking if I organize enough things, I'll eventually feel organized."
    m "Give me a council schedule or a stack of club feedback, and I'm fine. Great, even."
    m forward casual nerv om oe awkw rdown ldown "Then I open my own folder, and it's still mine."
    mc "Which part are you stuck on?"
    m forward casual neut om oe nobl rdown ldown "I don't know. That's the annoying part, because when I look at a question now, I can do it."
    "She says it to me, not to the folder."
    m forward casual nerv om oe awkw rdown ldown "Then I think about sitting there tomorrow, and I start checking whether I really know it. Even things I just got right."
    mc "Yeah. That one I know."
    "I set my coffee down mid-mouthful, and the ice knocks against the glass."
    mc "I keep going back to questions I've already done, because they're the ones I can finish. It feels like working."
    m forward casual neut cm oe nobl rdown ldown "That's exactly it."
    mc "I hate that part too."
    "Monika looks down at the ring of water under her glass."
    m forward casual nerv om oe awkw rdown ldown "I didn't want to spend lunch talking about this, too."
    "She turns the straw once between her fingers."
    m "I'm probably going to open the folder as soon as I get home."
    mc "You still have your own review to do. Just leave the stuff you've already finished alone."
    m forward casual wry cm oe nobl rhip ldown "Will you?"
    mc "I'll try. Can't ask for much more than that."
    "She takes a drink, then slides the folder farther back on the empty chair while I finish my coffee."
    show monika forward casual happ cm oe nobl rdown ldown at t21
    show kotonoha work thinking at t22
    "Kotonoha arrives with the tray while we're moving our drinks out of the way."
    ko "Soup and bread. Chicken sandwich, and the lemon cake."
    mc "Thanks. That looks good."
    "She sets the plates down in the order she listed them."
    ko work neut "The soup bowl is hot."
    show kotonoha at thide
    hide kotonoha
    show monika forward casual happ cm oe nobl rdown ldown at t11
    "Monika offers me a piece of bread, which I dip into her soup while she tries the lemon cake."
    "My sandwich comes apart on the first bite, and I'm still rebuilding it when she tells me to just use the fork."
    "Once we've finished, I take a clean napkin from the holder and ask for her pen."
    m forward casual curi om oe nobl rdown ldown "What are you doing?"
    mc "Something Asahina does when she's bored. Draw a shape and pass it over."
    "I draw a loop with a crooked tail, then slide it across the table."
    m forward casual curi om oe nobl rdown ldown "And I turn it into something?"
    mc "Whatever you see."
    "She studies it, then gives it a pair of enormous feet."
    mc "I was expecting a fish."
    m forward casual happ om oe nobl rdown ldown "You said whatever I see! Give him a face."
    "I add a single eye, but the ink spreads into the paper until he looks like he's been punched."
    m forward casual laug om ce nobl rdown ldown "Oh, poor thing. Here, he needs another one."
    "She holds the napkin steady for the second eye, which comes out even bigger."
    mc "That hasn't helped."
    m forward casual happ om oe nobl rdown ldown "I like him. He looks surprised to be here."
    "She adds a tiny hat, and I give him a briefcase because I want to see how far the feet can carry this."
    m forward casual curi om oe nobl rdown ldown "Where is he going?"
    mc "Job interview. He's underqualified."
    m forward casual laug om ce nobl rdown ldown "Don't say that! We haven't given him any qualifications yet."
    "By the time she writes a name under him, my coffee has left a brown circle across one foot. She turns it into a bicycle wheel."
    "We try another one while the ice melts, arguing over whether the new shape is a cat until neither of us can finish drawing it."
    show monika forward casual happ cm oe blus rdown ldown
    "She is still smiling at the drawing when I set the pen down between us."
    m forward casual neut om oe blus rdown ldown "...I needed this."
    mc "The cat?"
    m forward casual wry om oe nobl rdown ldown "No, although he helped."
    "Her eyes come back to mine, and she leaves the crooked napkin where it is."
    m forward casual neut om oe blus rdown ldown "I like having you to myself for a little while."
    "{i}I know we're not in the same headspace about this. I'm still happy just having lunch with her.{/i}"
    mc "We can stay a little longer. I've got nowhere I need to be yet."
    "She lets out a small breath, and her hand settles beside the drawings."
    m forward casual happ cm oe blus rdown ldown "I'd like that."
    "I pull the second napkin back to add whiskers, and she steadies the corner before I ask."
    m forward casual wry om oe nobl rdown ldown "You said it was a radiator."
    mc "I'm willing to reconsider."
    "Her folder stays on the neighboring chair while we work out whether the creature with the briefcase would get the job. Another bus fills up and leaves, and neither of us reaches for our things."
    "I turn my empty cup once by the rim."
    m forward casual happ cm oe nobl rhip ldown "You're doing that on purpose now."
    mc "I'm supporting the arts."
    "She turns toward the window, where her smile is still visible in the glass. I check the time, then catch Kotonoha's eye at the counter."
    "The check arrives in a little wooden tray. Monika reaches first."
    mc "No."
    m forward casual curi om oe nobl rhip ldown "I invited you."
    mc "You used that at the theater. That argument's retired."
    m forward casual wry cm oe nobl rdown ldown "It still has precedent."
    if s1_slept_in:
        mc "We're splitting it. I've got my half right here."
        "Monika considers an appeal, then puts down cash for her half."
        m forward casual happ cm ce nobl rdown ldown "Fine. But I'm paying for half the cake."
        mc "I was going to bring that up."
    elif s1_was("library_chem", "right") and s1_was("library_alg", "caught"):
        mc "We're splitting lunch. I've got my half right here."
        show monika forward casual neut cm oe nobl rdown ldown
        "Monika puts down her half, then lays the cake money on top of it with the solemnity of a general surrendering her sword."
        m forward casual neut om oe nobl rhip ldown "Per rule four. Let the record show that I lose with dignity."
        mc "The record also shows three to one."
    else:
        "I take the sticky note out of my wallet and lay it in the tray, rule four up."
        mc "Precedent doesn't beat a written contract."
        m forward casual laug om ce nobl rdown ldown "You're entering a {i}sticky note{/i} into evidence?"
        mc "We split lunch, and the cake's on me. It's right there in my handwriting."
        m forward casual wry om oe nobl rhip ldown "I {i}won{/i}, and I'm still losing arguments to my own stationery."
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 1.0
    pause 2.0
    scene bg city_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music night_b
    "Outside, the old bank throws a clean block of shade across the sidewalk. The lunch crowd has given the district back to buses and people with nowhere urgent to be."
    show monika forward casual happ cm oe nobl rdown ldown at t11
    "We walk together as far as her bus stop, where she opens her folder to tuck the drawings between two clean sheets."
    mc "You're keeping those?"
    m forward casual happ om oe nobl rhip ldown "Of course! You can have the cat, if you admit that's what it is."
    mc "Still looks like a radiator to me."
    "Her bus turns onto the far end of the block."
    m forward casual neut om oe nobl rdown ldown "Light review tonight, and then you stop."
    mc "You too. I'll message you when I put mine away."
    "Before she closes the folder, she peels a yellow sticky note out of it and hands it over. Tidy block letters: {i}SLEEP IS PART OF STUDYING.{/i}"
    if s1_slept_in:
        show monika forward casual laug om ce nobl rdown ldown
        "I look from the note to her, and she's already laughing."
        mc "I followed that one a little too well."
        m forward casual wry om oe nobl rhip ldown "Sleep {i}before{/i} the plans next time."
    else:
        mc "You're handing out propaganda now?"
        m forward casual happ om ce nobl rdown ldown "Only when it's evidence-based."
    "The bus sighs to a stop beside us."
    m forward casual happ om oe nobl rdown ldown "Text me when you get home?"
    mc "Yeah. You too."
    m forward casual happ cm oe nobl rdown ldown "See you tomorrow, [player]."
    "She gets on and lifts a hand at the window as the bus pulls away."
    "I stick the note to my transit card, where I'll see it every time I get on a bus."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "By my stop, Monika has sent a picture of her folder, still shut, and I answer with the yellow note on my transit card."
    call nier_clear from _call_nier_clear_0525_7
    stop music fadeout 1.0
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    play music day_a
    "Home is quiet until I reach the dining room, where an eraser is going over the same spot for the fourth time."
    show asahina worried at t11
    "Asahina has wedged her laptop between two textbooks and pinned a review packet under her elbow. She keeps rubbing the side of her hand while she reads."
    ah "Before you say anything, I {i}am{/i} studying. I've been here all afternoon, and my hand's killing me."
    mc "I was going to ask if you wanted the light on."
    show asahina unamused
    ah "Oh. Yeah, put it on, then."
    "I switch it on, and she tilts the packet away from the glare."
    "That's when I recognize the faded cell diagram on the front, right down to the crooked arrow leading out of the nucleus."
    mc "...No way."
    show asahina curious
    ah "What?"
    mc "They still use that packet?"
    ah "Wait, you had this one?"
    "I tug it out from under her elbow far enough to read the title. {i}FIRST-YEAR BIOLOGY: MIDTERM REVIEW.{/i}"
    mc "I had this exact thing two years ago."
    show asahina annoyed
    ah "Then you can tell me what that label says, because I've been squinting at it for ten minutes."
    mc "Mitochondrion. The label's halfway across the page from it, same as it was on mine."
    "I follow the faint line with my finger, and she leans over to see where it ends."
    show asahina unamused
    ah "That's what that says? I thought it was part of the other picture."
    mc "Cell migration must be an advanced topic."
    "The civics book under it has the same city-hall photograph I remember, though somebody has taped this copy's spine back together. Her foreign language workbook is the only thing on the table that looks new."
    mc "How's it going?"
    show asahina neut
    ah "Fine."
    mc "Want me to leave you to it?"
    show asahina annoyed
    ah "Do what you want. Just don't start reading over my shoulder."
    "I get a glass of water from the kitchen and set it down across from hers."
    mc "You want help?"
    show asahina unamused
    ah "Nope."
    mc "Cool."
    "So I take that chair and check my phone instead. Monika has sent a photo of our drawing, and I save it before I open anything else."
    "Asahina erases the same box again. I keep my eyes on my phone."
    "The refrigerator hums. Her pencil taps twice, stops, then taps once more."
    ah "If they move the lamp and count oxygen bubbles, the lamp distance is independent, right?"
    "The question arrives aimed at the worksheet instead of me."
    mc "Right. That's the part the experimenter changes on purpose."
    show asahina thinking
    ah "And bubbles per minute is dependent, 'cause that's what they measure."
    mc "Exactly. Like changing how long somebody practices serving, then counting what lands in bounds."
    "That gets one eye off the page."
    ah "So they have to keep the water temperature the same, and the plant length... Same kind of plant, too?"
    mc "Yeah, and count for the same length of time. You've got it."
    show asahina unamused
    if s1_slept_in:
        ah "Don't sound surprised. I've been at this all afternoon, and you were unconscious until noon."
    else:
        ah "Don't sound surprised. I've been at this all afternoon, and you were at a library. On a date."
    mc "I said you got it. I didn't say I was surprised."
    "She writes it down, smaller than the words around it."
    show asahina neut
    ah "They could've picked words that don't look almost exactly the same. That would help."
    mc "You can put that on the exam after the correct answer."
    show asahina smug
    ah "I'll cite you."
    "I move to the chair beside her only after she nudges the packet into the space between us."
    "The next few pages come back in pieces, membranes first, then how cells store and spend energy. By the metabolism diagram, she's following arrows with the eraser end of her pencil and muttering every label under her breath."
    "When I skip an arrow, she drags me back to it, and it takes the textbook to settle where it actually goes."
    show asahina worried
    ah "Does it get easier?"
    mc "Science?"
    ah "No. Exams. All of it."
    mc "Some of it. You start recognizing the questions, even when they're worded differently."
    show asahina unamused
    ah "I don't just mean the questions."
    "I look down at the arrow we've both been staring at. That, at least, I know what to do with."
    mc "Then I don't know. I still get worked up over things I can do."
    show asahina worried
    ah "So I've got years of this?"
    mc "You don't have to do years of it tonight. We can stop after this page."
    show asahina neut
    ah "And the civics book can go to hell?"
    mc "We could put it under the table. See if that works."
    "She bumps her shoulder into mine with barely any force."
    ah "Thanks, shitass."
    mc "Anytime, assface."
    "We finish the metabolism page, and she closes the packet herself, then pulls civics out from under it. I stay where I am."
    "The late-afternoon light has slid off the table and halfway up the wall by the time the last question stops turning into three more."
    "When I stand, Asahina spots the yellow note on my transit card."
    show asahina teasing
    ah "Did your girlfriend assign you a bedtime? Because that is a girlfriend thing to do."
    mc "My friend shared evidence-based propaganda."
    ah "Uh-huh."
    mc "Don't make that noise like you cracked a code."
    show asahina smug
    ah "Uh-huh..."
    "The household is a hostile environment for original material."
    mc "I'm going for an easy jog before dinner."
    show asahina curious
    ah "Is your foot even better yet? You could barely walk on it."
    mc "Coach said I could, as long as I keep it easy."
    show asahina unamused
    ah "If you come back limping, I'm telling Mom before you can pretend you tripped on the step."
    mc "Why's everyone a regulatory agency now?"
    ah "Due process, bitch."
    "I look at her open civics book."
    mc "You know what? That earns full credit."
    "My phone buzzes with Mom asking whether the grocery list missed anything. I tell her we're good, and a thumbs-up comes straight back."
    "Asahina takes a drink of water at last, then reaches across me for her pencil."
    "By the time I leave, civics is the only book open."
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 1.0
    pause 2.0

    scene bg residential_day
    $ show_calendar()
    $ atmos("evening")
    with wipeleft_scene
    play music house_day_a
    # NUDGE P2: the pocket-dial call below is funny. Halve it.
    "The air's cooler by the end of the street, though heat keeps rising off the pavement."
    "I start slow. Actually slow, since Coach would have my hide if I turned up limping on both feet."
    # SFX SUGGESTION: Even running footfalls and measured breathing, briefly isolated from the music.
    "My foot stays quiet, thankfully. I settle into a pace where I can keep my shoulders loose, then take the longer turn around the corner instead of cutting across it."
    "My phone buzzes in my hand, cutting off the playlist and whatever rhythm I had going. It's Mom."
    "{i}If this is a reminder to hydrate, I'm going to hear Coach's voice behind hers.{/i}"
    call phone_call("Mom", status="Incoming Call", can_decline=False) from _call_phone_call_0525_1
    python:
        _phone_call_lines = [
            phone_call_line("me", "Hey, Mom."),
            phone_call_line("them", "..."),
            phone_call_line("me", "...Mom?"),
            phone_call_line("them", "...no, not those, the ones in the back aren't bruised to hell..."),
            phone_call_line("me", "Hello?"),
            phone_call_line("them", "...is this on sale, or is the little sign just lying to me..."),
            phone_call_line("me", "Mom, you're talking into my ear."),
            phone_call_line("them", "...and the list, now where did I put the-- hm?"),
            phone_call_line("me", "MOOOOOOOOOOOM!"),
            phone_call_line("them", "...What? Hold on--"),
            phone_call_line("them", "Oh, for-- did I call you? I checked your reply and shoved my phone in my bag without locking it."),
            phone_call_line("me", "I've been listening to you choose fruit."),
            phone_call_line("them", "Then you know how long I've been here."),
            phone_call_line("them", "Wait, why are you breathing like that? Are you running?"),
            phone_call_line("me", "Easy jog. Heavy emphasis on {i}easy{/i}."),
            phone_call_line("them", "I can hear the emphasis working very hard to cover for you."),
            phone_call_line("me", "I'm basically walking."),
            phone_call_line("them", "Then keep basically walking. It's the night before exams, not-- hang on--"),
            phone_call_line("them", "...yes, just these two, thank you-- no, I don't need a bag..."),
            phone_call_line("me", "...You still alive over there?"),
            phone_call_line("them", "I'm fine, just checking out right now."),
            phone_call_line("them", "Hey, miss? I have a case of water under here that still needs to be scanned."),
            phone_call_line("me", "Sounds like you're having a lot of fun."),
            phone_call_line("them", "Okay, I actually have to-- be home before it's fully dark, please."),
            phone_call_line("me", "Yeah. Already turning back."),
            phone_call_line("them", "Good. And drink some-- you know what, you already know."),
            phone_call_line("me", "There's the hydration order."),
            phone_call_line("them", "Love you, sweetheart-- ugh, the card reader won't-- okay, one second--"),
            phone_call_line("me", "Love you. Go rage against the machine."),
            phone_call_line("them", "Always do."),
        ]
    call phone_call_conversation("Mom", _phone_call_lines, status="Connected") from _call_phone_call_conversation_0525_1
    # Her still-open grocery thread pocket-called him, and she ran the whole
    # errand out loud anyway. After this, calling her about a household question
    # too trivial to justify a call is normal between them.
    $ phone_open("mom_call")
    "The call ends, and I stand on the sidewalk with the phone in my hand while the evening cools the back of my neck."
    "Then I jog home, slower than before."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Mom gets home with the case of water that survived the card reader, and I carry it in for her."
    nier "Over dinner, Asahina holds up the badly printed diagram as proof that biology started it."
    call nier_clear from _call_nier_clear_0525_8
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music night_a
    "I check the civics teacher's reminder for tomorrow's room number, then scroll past the familiar declaration that the work we submit must be our own."
    "With my tea parked out of elbow range and my phone on its charger, I open the pages I still need to check."
    "Once I've worked through the marked questions, I catch myself turning back to the first page, though there's nothing left on it to do."
    "The screen lights up beside my elbow."
    python:
        _phone_messages = [
            phone_msg("them", "Final check-in before I become a responsible person and sleep."),
            phone_msg("me", "You first."),
            phone_msg("them", "I'm literally putting my notes away right now."),
            phone_msg("me", "I'm almost putting mine away."),
            phone_msg("them", "Pics or it didn't happen."),
            phone_msg("me", "Fine."),
            phone_msg("them", "No midnight review spirals."),
            phone_msg("them", "Besides, I'd hate to lose my competition for valedictorian because you slept through half your exams."),
            phone_msg("me", "I'm sure someone would still keep you busy."),
            phone_msg("them", "I mean, sure, but where's the fun in mopping the floor with them?"),
            phone_msg("me", "You can also take your own advice. Go to sleep."),
            phone_msg("them", "Dealio!"),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0525_2
    # Their established friendship and this evening exchange support casual
    # calls on either version of the day, including the missed-library branch.
    $ phone_open("monika_video")
    "I put the notes back in their folder and send her a picture of it with my mug on top, so reopening it would at least take some effort."
    "Then I check tomorrow's alarm. Twice."
    "Downstairs, a cabinet closes."
    $ update_character_thought("monika", "Monika made flashcards for subjects she isn't taking, then admitted she'd been avoiding her own notes. She kept both of our ridiculous cafe drawings.")
    $ update_character_thought("asahina", "Asahina's first-year biology packet comes from the same master copy my class used two years ago. She nudged it between us before asking whether exams ever get easier.")
    $ update_character_thought("kotonoha", "Kotonoha works Sundays at the cafe by the old bank. She keeps the counter running like any other shift.")
    $ update_character_thought("mom", "Mom's pocket called me during my jog. Even by accident, she managed to check whether I was overdoing it.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Tomorrow, the papers turn over."
    call nier_clear from _call_nier_clear_0525_9
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0525_1
    jump a0526
