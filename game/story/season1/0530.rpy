init python:
    poem_0530_mc_draft = Poem(
        author="mc",
        title="Past the Final Station (Draft)",
        text="""\
Take the train past the final station.
The doors will open where the map runs out of ink.

Do not ask the conductor which platform you need.
He has been facing the same window
longer than the city has had a name.

Follow the blue lights until they turn red.
At the end of the platform,
choose the staircase with no footprints."""
    )

    poem_0530_mc_revised = Poem(
        author="mc",
        title="Past the Final Station (Draft)",
        text="""\
Take the train past the final station.
The doors will open where the map runs out of ink.

Do not ask the conductor which platform you need.
He has been facing the same window
longer than the city has had a name.

Follow the blue lights until they turn red.
At the end of the platform,
choose the staircase with no footprints.

When you reach the top,
listen for a television in the next room
and someone putting away dishes."""
    )

    poem_0530_monika = Poem(
        author="monika",
        title="Five Directions",
        text="""\
1. Pass the old bank with the clock
    that loses three minutes every rainstorm.

2. Turn beneath the green awning.

3. Take the table beside the window,
    unless somebody else needs it more.

4. Put two cups down.
    One can stay empty for a while.

5. Wait until the place becomes real."""
    )


label a0530:
    # --- Day 16: 2025-05-30 ---
    # Post-exam ramp, day two. The increase in Matsuda's presence should feel like ordinary
    # social momentum on a first playthrough, not encroachment and not a mystery the narrator
    # is already solving. She is mentioned once at lunch, appears only after club, remembers
    # MC's request to slow down, asks one normal question, and accepts the practical limits on
    # Saturday without another scramble. Her relationship with Monika and access to the club remain
    # future developments. The day's acting bit is comic and human: once challenged on a grating
    # cowboy persona, she commits harder and carries it through the follow-up to yesterday's invitation. Tsubaki gets the
    # last word, and the practical plan still remains clear beneath the performance.
    # Ledger meters moved quietly: Matsuda joins an existing after-school plan; Tsubaki protects
    # her own preferences; Monika and MC restore their club routine; Mom's work thins the house;
    # Sam's schedule remains useful enough that Asahina sees no reason to question it.
    $ _exam_one_catch = exam_guard_scum_count() == 1
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music house_day_a
    "Mom's chair is already pushed in. She's left a note under the sugar bowl instead, with the last two lines squeezed into the corner."
    call enter_m_show_sticky_note(("Early case meeting.", "Rice is warm.", "Eat something with a color.", "Home late.", "Love you both."), signature="Mom") from _call_enter_m_show_sticky_note_0530_1
    if _exam_one_catch:
        "My phone came off the kitchen charger on my way down. The laptop is still shut on the living-room table, its new permanent address."
        "Both of them are mine again, on parole. The laptop doesn't leave the living room, and the phone clocks back in on the charger at ten."
    show asahina uniform thinking at t11
    "Asahina is frowning at the schedule on her phone, a piece of egg parked halfway to her mouth."
    mc "You planning to eat that, or is this a demonstration?"
    ah "{i}Shh!{/i} I'm trying to move one thing and not knock the rest of the day over."
    mc "The egg?"
    ah "Saturday after school, genius."
    "She drags a blue block across the screen, then puts it right back where it was, frowning like it gave her attitude."
    "I get a look before she angles the screen away: volleyball, review, dinner, and one blank strip wedged in between."
    mc "You're renovating Saturday at the breakfast table?"
    show asahina uniform neut
    ah "Sam stuck two whole hours of biology in there. I'm cutting it down."
    mc "Wasn't this thing supposed to save you time?"
    show asahina uniform annoyed
    ah "It {i}will{/i}, once I'm done fixing it!"
    "She says it fast, but the next drag takes her two careful tries before she'll let go of the block."
    ah "Exams are done, they literally handed us half a Saturday, and I'm gonna use it."
    mc "Your mitochondria can fend for themselves."
    show asahina uniform smug
    ah "Exactly. The powerhouse of the cell can take a day off."
    "The egg completes its trip."
    show asahina uniform curious
    ah "You've got club today, right?"
    mc "First real meeting since exams."
    show asahina uniform disgusted
    ah "Ew. You sound happy about it."
    mc "I'm allowed to like one thing a week."
    show asahina uniform curious
    ah "And track?"
    mc "Coach gave me today off. Practice is back tomorrow after classes, as long as the foot behaves."
    ah "So... after practice, you're free."
    mc "Technically."
    show asahina uniform neut
    "She taps the edge of the blank strip with her thumb and slides the phone a little farther from her bowl."
    ah "Got any plans?"
    mc "Matsuda pitched the arcade. She and Tsubaki are hitting a used-book sale first."
    show asahina uniform unamused
    ah "Okay, and? Are you going?"
    if s1_was("arcade_invite", "yes"):
        mc "I said yes before she'd even finished asking."
        show asahina uniform teasing
        ah "Wow. She says {i}arcade{/i} one time and you fold like a lawn chair."
        mc "I haven't touched a decent racing cabinet since winter. Folding was the correct play."
    elif s1_was("arcade_invite", "why"):
        mc "I asked her why she was inviting us. She answered with an entire performance instead, so... I still don't really know."
        ah "That's not what I asked. Also, you asked her {i}why{/i}? Bro, that's how people get uninvited."
        mc "I want to go, though. I haven't touched a decent racing cabinet since winter."
    else:
        mc "I told her to let me know if the plan survives."
        ah "That's not an answer, dude. Do you {i}want{/i} to go?"
        mc "...I'd like to. I haven't touched a decent racing cabinet since winter."
        show asahina uniform teasing
        ah "Then say {i}that{/i} to her! God."
    "She tips the phone so I can see the blank strip, then locks it and picks up her bowl with both hands."
    show asahina uniform neut
    ah "And tell me once the time's sorted. I'm not giving that slot back to a cell diagram."
    mc "Why?"
    show asahina uniform embarrassed
    ah "Because I'd go too, dumbass! You're allowed to bring your sister."
    "She takes her bowl to the sink and clears out of the room at a speed that doesn't invite follow-up questions."
    show asahina at thide
    hide asahina
    "I wash up, since Mom isn't here to beat me to it, and slide her note back under the sugar bowl."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The walk to school is nothing but other people's Saturday plans, and Asahina has opinions about every one she overhears."
    call nier_clear from _call_nier_clear_0530_1
    stop music fadeout 1.0
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    with dissolve_scene_full
    play music school_day_a
    if _exam_one_catch:
        "Language arts wants a reflection on the exam, and my blank page looks uncomfortably like the incident form I signed yesterday."
    else:
        "Language arts wants a reflection on the exam. Five minutes in, my page has one dark dot on it, right where the pen sat too long."
    # Saturday's half-day is practical rather than ceremonial: the main
    # academic wing must be empty before a ventilation replacement and power cut.
    "Then the intercom clicks on to repeat tomorrow's half-day in its careful bad-news voice. The academic wing loses power at noon so maintenance can crane a new ventilation unit onto the roof."
    "The gym and track run on their own circuit, so they stay open. The announcement calls that convenient, and everybody in the room with practice tomorrow has a less flattering word for it."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Volleyball business claims Asahina for lunch, and a student-council handoff claims Monika. I take my food up to the roof alone."
    call nier_clear from _call_nier_clear_0530_2
    stop music fadeout 1.0
    pause 2.0
    scene bg rooftop
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music day_a
    play sound moddooropen
    "The rooftop door scrapes open, and Tsubaki raises a hand from the shade along the wall. Next to her lunch sits a stack of index cards held together by a pale blue clip."
    show tsubaki uniform happy at t11
    ts "Hey."
    mc "Hey. Roof still quiet?"
    show tsubaki uniform teasing
    ts "So far. The wind keeps showing off, though."
    mc "I can live with that."
    "As I sit down by the door, leaving a polite stretch of concrete between my lunch and her cards, she wipes the condensation off her drink and moves it away from her notebook."
    mc "Studying already? The exams are barely cold."
    show tsubaki uniform neut
    ts "No. Inventory."
    "She turns the top card toward me: a short list in small, very straight handwriting."
    ts "I kept mixing up what was in my bag and what was still in Matsuda's after Wednesday, so... separate lists. Before anything else disappears."
    mc "You inventoried {i}her{/i} bag?"
    show tsubaki uniform unamused
    ts "My things {i}in{/i} her bag. She keeps saying she'll bring them tomorrow, and then tomorrow she shows up with a different bag."
    mc "How much of your stuff is she holding hostage?"
    show tsubaki uniform annoyed
    ts "Two books and the good ruler. I want the ruler back before she uses it to open a parcel."
    "She clips the cards and tucks them under her notebook, out of the wind's reach."
    show tsubaki uniform neut
    "We eat one-handed, the other hand pinning down whatever the wind is after. She's saving a piece of fried chicken in the corner of her lunchbox and working through the rice around it."
    show tsubaki uniform curious
    ts "How was track yesterday?"
    mc "Boring in the medically approved way."
    ts "That's good, right?"
    mc "Very. Coach might put me in both races at the invitational."
    show tsubaki uniform teasing
    ts "Both? You wanted that, didn't you?"
    mc "Badly. I'm keeping a straight face about it until he decides."
    "The saved piece of chicken goes next, way ahead of schedule."
    show tsubaki uniform neut
    ts "Did Matsuda tell you about Saturday?"
    mc "Book sale, then arcade. She said she'd send times."
    show tsubaki uniform happy
    ts "Yeah. Honestly, I'm going for the old magazines. I missed the last clearance."
    show tsubaki uniform thinking
    "She smooths the paper sleeve from her chopsticks flat against her knee."
    ts "We planned it before exams, but every time we picked a day, one of us had something to study."
    mc "The arcade half sounds compelling."
    show tsubaki uniform smug
    ts "I figured it might."
    mc "What, am I that easy to market to?"
    show tsubaki uniform teasing
    ts "You talk about games. A lot."
    mc "...Can't argue with the data."
    show tsubaki uniform neut
    "She takes another bite and checks the door, once."
    ts "She said she'd figure out when you could meet us, so... I'm leaving that part with her."
    mc "I'll ask her after club."
    show tsubaki uniform determined
    ts "Thank you. I like her, I do, but I {i}don't{/i} want to become her secretary."
    mc "Can't say I blame you."
    show tsubaki uniform smug
    ts "Or her noise protection, depending on the day."
    show tsubaki uniform happy
    "The joke reaches me on a delay. When I laugh, she lets one out too and hides the rest of it behind her drink."
    show tsubaki uniform determined
    ts "Also, I want the bookstore first. The magazine tables are awful once people start dragging arcade prizes through them."
    mc "That sounds like the voice of experience."
    show tsubaki uniform annoyed
    ts "Last time, somebody hit me with an inflatable sword."
    mc "So it's personal."
    show tsubaki uniform unamused
    ts "Deeply."
    show tsubaki uniform neut
    # SFX SUGGESTION: A distant warning bell carrying through the rooftop door.
    "A thin warning bell carries up through the rooftop door. She packs as it rings, cards and containers each into the right bag, and never once checks either list."
    show tsubaki uniform happy
    ts "I should go."
    mc "See you."
    "She gets as far as the door, then turns around with her hand on the bar."
    show tsubaki uniform nervous
    ts "And, um... you don't have to come just because we mentioned it."
    if _exam_one_catch:
        mc "I know. It still sounds fun, but I have to ask at home first."
    else:
        mc "I know. It still sounds fun."
    show tsubaki uniform happy
    "That gets a quick smile out of her, and then she's down the stairs ahead of the crowd."
    show tsubaki at thide
    hide tsubaki
    play sound moddoorclose
    "The door swings shut behind her. The wind gets the roof back."
    $ update_character_thought("tsubaki", "Tsubaki keeps index-card inventories so her things stop vanishing into Matsuda's bag. She told me plainly that she won't become Matsuda's secretary, and that the bookstore comes before the arcade.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "By seventh period the notebooks are closing early, and every conversation has skipped ahead to whatever fits after tomorrow's half-day."
    call nier_clear from _call_nier_clear_0530_3
    stop music fadeout 1.0
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music school_day_a
    "One corridor short of the club room, I find Monika holding a cardboard box together by force of will. The bottom has started to split."
    show monika forward uniform neut cm oe awkw rdown ldown at t11
    "She's got three notebooks pinned under one arm and her chin clamped down on the flap, and a few folded slips are poking out of her pocket."
    mc "Want another pair of hands?"
    m forward uniform nerv om oe awkw rdown ldown "Yes, please! I just need the bottom to stay attached until the next door!"
    "I take the box before the cardboard makes any decisions, and its full weight settles across my forearms."
    mc "What did you steal?"
    m forward uniform happ om oe nobl rdown ldown "{i}Rescued!{/i} The library's clearing old literary journals and duplicate anthologies out of storage, and I objected to their methods."
    "The top layer is school publications older than both of us, their covers faded through several different shades of beige."
    m forward uniform happ cm oe nobl rdown ldown "They were going to recycle the whole lot, so I asked if the club could take a box first."
    mc "One box."
    "Her gaze slides past me to the corner, where a second box is waiting against the wall."
    mc "Of course."
    m forward uniform pout om oe awkw rdown ldown "There are good things in there! Probably! Which is exactly why I couldn't let them get recycled unopened."
    "She stacks her notebooks on top of my box and keeps a hand on them while I shift it against my hip."
    m forward uniform happ cm oe nobl rdown ldown "And these are for us. Everyone's been writing on exam paper for a week, so I thought clean notebooks might make the room feel like ours again."
    "I rest the box on the windowsill to fix my grip, and she runs her thumb along the soft cardboard edge."
    m forward uniform neut cm oe nobl rdown ldown "The club got really quiet this week."
    mc "Everyone had exams."
    m forward uniform neut om ce nobl rdown ldown "I know. I missed having everyone there."
    m forward uniform happ om oe nobl rdown ldown "Hikari and Homura barely said two words to each other all week. I actually started missing their arguments, which can't be healthy."
    "Still smiling, she pulls the slips out of her pocket: three prompts, each folded twice and marked in a different color."
    m forward uniform happ om oe nobl rdown lpoint "Help me pick? Blue, red, or black. No peeking."
    mc "What do the colors mean?"
    m forward uniform happ cm ce nobl rdown ldown "If I tell you, the highly scientific process turns into personal preference."
    "She fans them facedown over the box. I tap blue, and she unfolds it against the top notebook."
    m forward uniform happ cm oe nobl rdown ldown "Give directions to a place that does not exist."
    mc "And the others?"
    "She opens red."
    m forward uniform neut om oe nobl rdown ldown "Write an apology from an object that has outlived its use."
    mc "Cheerful."
    "Black reads: {i}Describe a room one minute after everyone leaves.{/i}"
    mc "These are all a little empty for a room you're trying to wake up."
    m forward uniform wry om oe awkw rdown ldown "They're post-exam prompts. Apparently my imagination is still... clearing the building."
    mc "Directions is the least likely to cause a group crisis."
    m forward uniform laug om ce nobl rdown ldown "Honestly? I'll accept that as a presidential metric today."
    "She folds the rejects away."
    mc "You already wanted blue, though."
    m forward uniform curi om oe nobl rdown ldown "What makes you say that?"
    mc "You used the nice pen."
    "The blue slip is written in the green ink she saves for finished headings. The other two got plain ballpoint."
    "She studies the slip instead of denying it."
    m forward uniform happ cm oe nobl rdown ldown "I wanted a second opinion from somebody likely to agree with me."
    mc "That's a much narrower service."
    m forward uniform happ om oe nobl rdown lpoint "And you provided it! Blue wins."
    "She hoists the lighter second box onto her hip, and we haul everything down the last corridor. At the club-room door, she works the handle with her elbow while I hold the sagging bottom of mine together with one knee."
    m forward uniform wry om oe awkw rdown ldown "If this box breaks now, I'm resigning."
    mc "I'll say something moving at your memorial."
    m forward uniform wry cm oe nobl rdown ldown "You are not touching my stationery."
    mc "There goes my speech."
    "She gets the door open, and both boxes make it over the threshold in one piece."
    show monika at thide
    hide monika
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 1.0
    pause 2.0
    scene bg club_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music day_c
    "Hikari is having it out with a stapler by the windows. Homura has already claimed the back desk and three colors of pen."
    show monika forward uniform neut cm oe nobl rdown ldown at t11
    "On the board, in Monika's handwriting: {i}Give directions to a place that does not exist.{/i}"
    m forward uniform happ om oe nobl rhip lpoint "You've got twenty minutes! Prose, poem, list, fake instruction manual... whatever actually gets you there."
    hikari "If it doesn't exist, how do we know if the directions work?"
    m forward uniform curi om oe nobl rhip lpoint "Commit to the premise!"
    homura "That means she doesn't know either."
    m forward uniform happ om oe nobl rdown ldown "And you! First pick of the clean notebooks, for hauling the box."
    mc "The blue one, before somebody more deserving gets it."
    "Pens start scratching all around me. I write the prompt across the top of the blue notebook's first page, then strike it out and give the space to the city under the false sky."
    "That game had most of my free hours until exams took custody of the console, so it gets a train, a conductor and some deeply hostile municipal lighting. Then the pen runs out of things I know."
    call enter_m_showpoem(poem_0530_mc_draft) from _call_enter_m_showpoem_0530_1
    "I like the conductor. What happens after the stairs, I have no idea."
    "Monika makes a slow lap of the room, answering one question and refusing two attempts to make her define {i}nonexistent{/i} for everyone."
    m forward uniform curi om oe nobl rdown ldown "Stuck?"
    mc "I'm giving the place time to exist."
    m forward uniform happ cm ce nobl rdown ldown "Generous of you."
    "She rests two fingers on the empty desk beside mine."
    m forward uniform curi om oe nobl rdown ldown "Okay, but where are they trying to go?"
    mc "That seems outside the prompt."
    m forward uniform neut om oe nobl rdown ldown "It might help with the stairs. What's at the top?"
    "I reread the last line while she waits."
    mc "Home... probably."
    m forward uniform curi om oe nobl rdown ldown "Their home, or somebody else's?"
    mc "I haven't decided where home is yet."
    m forward uniform happ om oe nobl rdown lpoint "Then write the part you {i}do{/i} know. You can always change it later."
    "She taps the blank space under my last line and moves on to the next desk."
    "Somebody behind me picks a fight with a highlighter. I add one sentence."
    call enter_m_showpoem(poem_0530_mc_revised) from _call_enter_m_showpoem_0530_2
    # SFX SUGGESTION: A short timer tone, followed three seconds later by Monika's single sharp clap.
    "The timer goes off mid-debate over whether the new ending is too obvious. Saved from improving it into something worse."
    m forward uniform happ om oe nobl rhip lpoint "Pens down! Or, at least, pens hovering guiltily."
    "A few pens ignore her. Monika lets them finish whatever word they're on, then claps once."
    m "Voluntary exchange! Find someone, trade pages, and ask one useful question."
    homura "I called president."
    hikari "You can't call president!"
    homura "I {i}just did{/i}."
    "Hikari turns the other way and finds me already holding out my notebook."
    hikari "Trade?"
    mc "Was I selected, or just nearest?"
    hikari "Nearest. Don't make it sentimental."
    "Her directions lead to an elevator on the moon with a broken call button, a floor display that counts backward and a destination called {i}somewhere with weather{/i}."
    "She reads my train piece standing beside my desk, a pen cap caught between her teeth."
    hikari "Why are there no footprints if these directions exist?"
    mc "Maybe nobody follows them."
    "She takes the cap out of her mouth."
    hikari "Then say that."
    "She underlines {i}no footprints{/i} and holds the notebook out until I look."
    "I tap the broken call button on her first page."
    mc "If nobody can summon the elevator, who keeps leaving directions to it?"
    "Hikari takes her notebook back and rereads the first line with her mouth pulled to one side."
    hikari "Rude."
    mc "Useful?"
    hikari "Unfortunately."
    "Across the room, Homura is holding Monika's numbered list at arm's length."
    homura "This is a real cafe."
    m forward uniform nerv om oe awkw rdown ldown "Yes. I may have... skipped a key word in my own prompt."
    homura "There are two cups on the table."
    m forward uniform wry om oe awkw rdown ldown "I like the cups. Can they stay while I fix the rest?"
    homura "The cups can stay. The bank has to go."
    "Monika writes in Homura's margin, and Homura strikes two lines from Monika's page in return. Neither of them asks twice."
    "When the exchange ends, Monika comes by to read Hikari's underline, then the lines I added about the television and the dishes."
    m forward uniform neut om oe nobl rdown ldown "Keep those two lines exactly how they are."
    "She uncaps the green pen and writes one question beneath them: {i}Does the traveler go inside?{/i}"
    mc "Homework?"
    m forward uniform happ cm oe nobl rhip lpoint "One line. Monday."
    "She's already moved on to the next pair, and my objection dies in draft."
    "For the rest of the hour, drafts keep changing hands. Homura deletes a paragraph outright and sinks into her chair like she's set down something heavy."
    "Monika settles a dispute over whether titles count toward the word limit and calls time."
    $ update_character_thought("monika", "Monika used a directions prompt for the first regular club meeting after midterms. She wrote her question under my lines in green ink and wants one more line by Monday: whether the traveler goes inside.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Monika stays behind to finish attendance. I take my one line of homework out into the corridor, where Tsubaki is waiting."
    nier "She isn't alone."
    call nier_clear from _call_nier_clear_0530_4
    stop music fadeout 1.0
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("evening")
    with wipeleft_scene
    play music school_day_a
    show tsubaki uniform neut at t21
    show matsuda uniform teasing at t22
    "Matsuda pushes off the wall in no particular hurry and plants her feet two floor tiles apart, one hand hanging loose beside an imaginary holster."
    "She waits until I'm looking at her, then tips a hat she isn't wearing."
    stop music fadeout 1.0
    play music theme_matsuda_a
    ma "Well, look what finally wandered outta the book barn! Reckon the president kept you in there sortin' sonnets till the sun plumb gave up on us!"
    "The drawl stretches every vowel farther than it was ever built to go."
    ma "Had half a mind to round up a search party, but Kareda here said a man oughta be let to find his own way home."
    show tsubaki uniform unamused
    ts "I said the meeting ends at the same time every Friday."
    show matsuda uniform smug
    ma "A woman of few words and considerable wilderness experience."
    # Converging. All three land on Tsubaki's answer; what changes is how MC
    # meets a sustained cowboy performance. Keep the drawl, frontier manners,
    # and physical business through the Saturday arrangements and her departure;
    # this is not her ordinary voice with a single 'partner' appended.
    # Registered in s1_choices.rpy as 0530 matsuda_bit.
    menu:
        "She is committed to this."

        "Ask what's wrong with her.":
            $ s1_pick("matsuda_bit", "flat")
            mc "...Why do you sound like that?"

        "Play along.":
            $ s1_pick("matsuda_bit", "play")
            mc "...Reckon I've had a long one myself, ma'am."
            "It comes out somewhere between two regions and a head cold."
            show matsuda determined
            ma "Well, son, we'll get that accent seen to by a doctor once we reach town. Till then, you ride with us!"
            show tsubaki uniform unamused
            ts "Please do not encourage this."

        "Ask Tsubaki.":
            $ s1_pick("matsuda_bit", "tsubaki")
            mc "How long has this been happening?"
            show tsubaki uniform unamused
            "Tsubaki doesn't ask who I'm talking to."

    ts "Since lunch. She has not taken a break."
    show tsubaki uniform annoyed
    ts "She's never even {i}been{/i} to that region."
    show matsuda uniform determined
    ma "Ain't no border fence tall enough to keep art penned up where it was born, partner!"
    mc "Did you watch an entire Western last night?"
    show matsuda unamused
    "She squints off down the corridor as though the answer might come riding in from the other end of it. What comes instead is Monika, done with attendance, the club folder tucked against her side."
    "Monika doesn't slow down or say a word. She watches Matsuda the whole way past, and Matsuda holds the squint until the footsteps have gone down the stairwell."
    ma "A man sees things out on the trail. Things that change him."
    show tsubaki uniform neut
    ts "Three movies. She sent me the trailers."
    "Matsuda hooks both thumbs where a gun belt would be and drops the drawl another register."
    show matsuda determined
    ma "Three hard winters, and I ain't prepared to discuss 'em."
    mc "Okay. Did you two at least work out tomorrow?"
    show matsuda smug
    if s1_was("arcade_invite", "yes"):
        ma "Sure did! Now, seein' as you signed on to this here expedition 'fore I'd even finished my pitch--you still got track before you can ride out with us?"
    elif s1_was("arcade_invite", "why"):
        ma "Sure did. Now, that expedition I mentioned yesterday--and before you go askin' again, a cowpoke don't explain who she rides with--you still got track before you can join us?"
    else:
        ma "Sure did. That expedition I mentioned yesterday survived the night, just like you asked. Now, you still got track before you can join us?"
    mc "Yeah. Don't wait around school for me."
    ma "Then you send word the minute Coach turns you loose, tenderfoot, and we'll tell you which saloon we're holed up in."
    if _exam_one_catch:
        mc "That works, {i}if{/i} Mom says yes. I still need to ask her tonight."
        show matsuda determined
        ma "Then you go ask your ma proper. A promise you can't keep ain't worth the spit on the handshake, and the trail'll wait on your answer."
    else:
        mc "All right. I'll text when I'm done."
        show matsuda happy
        ma "Well, hell! Much obliged."
    "She checks with Tsubaki first and gets the smallest nod in return."
    ma "I'll send word to Asahina my own self. She can mosey on in whenever volleyball turns her loose, long as she's still fit to travel."
    show tsubaki uniform determined
    ts "And don't tell him to meet us at the arcade while I'm still looking at books."
    show matsuda teasing
    ma "Wouldn't dream of it! I ain't some lawless varmint, draggin' innocent readers past a clearance table!"
    "She lays one hand over her heart and raises the other, palm out, like she's being sworn in."
    ma "On my horse, my hat and my deeply questionable reputation, nobody touches a steerin' wheel till this lady has her books."
    mc "You don't have a horse or a hat."
    show matsuda determined
    ma "Then you know what I'm puttin' on the line."
    show tsubaki uniform unamused
    "Tsubaki rolls her eyes toward the ceiling and leaves them there."
    ts "Bruh."
    show matsuda smug
    ma "Knew you'd come around eventually, pardner."
    if _exam_one_catch:
        ma "You send word once you've asked your ma. We'll keep a lantern lit on the trail."
        mc "I'll text."
    else:
        ma "Catch you after track, buckaroo."
        mc "Are you going to keep talking like this tomorrow?"
        ma "Can't rightly say what tomorrow holds, friend. That's frontier livin'."
    show tsubaki uniform happy
    ts "See you tomorrow."
    mc "See you."
    show matsuda at thide
    show tsubaki at thide
    hide matsuda
    hide tsubaki
    stop music fadeout 1.0
    "Tsubaki heads for the east gate. Matsuda backs after her for two slow steps, watching me from under the brim of her absent hat."
    "She only turns around when Tsubaki calls her name, and she keeps the wide, rolling walk all the way to the stairs."
    if _exam_one_catch:
        "I walk home rehearsing how to ask Mom, and every version turns into an announcement halfway through."
        $ update_character_thought("matsuda", "Matsuda kept a cowboy accent from first word to last while we worked out how I'd catch up after track. I still have to ask Mom before I can confirm.")
    else:
        "I walk home doing math on the coin jar on my desk, and none of it comes out in my favor."
        $ update_character_thought("matsuda", "Matsuda kept a cowboy accent from first word to last while we worked out how I'd catch up after track. I'll text when Coach lets me go, and they'll tell me where to meet them.")
    $ hide_calendar()
    scene black with wipeleft_scene
    # SFX SUGGESTION: The front door latch closing into an empty house with a slight room echo.
    nier "Nobody answers when the front door shuts behind me."
    nier "The house has gone the flat gray that comes before anyone bothers with a lamp, and Mom's note is right where I left it this morning, under the sugar bowl."
    call nier_clear from _call_nier_clear_0530_5
    stop music fadeout 1.0
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    play music night_a
    play sound moddooropen
    "Asahina gets in not long after, shouldering the door open with her gym bag while she finishes reading something on her phone."
    show asahina uniform unamused at t11
    ah "Okay, why does the Azure Eye text like a trumpet's supposed to play after every message?"
    mc "You came in swinging."
    ah "She asked if I wanted to meet you guys at the arcade after volleyball. Full sentences, actual order of operations, and no weird group name. Yet."
    mc "Give her time."
    show asahina teasing
    ah "She called me {i}ma'am{/i}, so I offered to help her cross the road."
    mc "So? Are you going?"
    # SFX SUGGESTION: A gym bag thump followed by the refrigerator seal pulling open.
    show asahina neut
    "She drops the gym bag by a chair and heads straight for the refrigerator."
    ah "{i}Maybe.{/i}"
    mc "You said yes."
    show asahina smug
    ah "I said I'll show up if practice doesn't kill me first. That's not a yes, that's a maybe with terms and conditions."
    "She pulls out the covered leftovers and finds Mom's second note, this one stuck to the lid."
    call enter_m_show_sticky_note(("Heat three minutes.", "Stir.", "One more minute.", "I mean it."), signature="Mom") from _call_enter_m_show_sticky_note_0530_2
    ah "She saw us coming."
    mc "We're a known quantity."
    "We follow the microwave instructions to the letter, mostly so we won't hear about it from across town."
    "Dinner takes three trips, since Mom is usually the one who remembers drinks and chopsticks and vegetables before anybody sits down."
    # NUDGE KEEP: Asahina setting Mom's place.
    "Asahina comes back with the chopsticks, reaches for the third bowl, and only then notices she's set Mom's place too."
    show asahina sad
    "Her hand stays on the back of Mom's chair."
    ah "...Oh."
    "She puts the bowl back in the cabinet while I pour the drinks, and neither of us says anything about it. The table looks bigger afterward."
    mc "Mom said {i}late{/i}, not never."
    show asahina neut
    ah "I know."
    "She sits, and we eat with the refrigerator humming through the part of dinner Mom usually fills with questions we pretend are invasive."
    show asahina curious
    ah "So you're actually going tomorrow?"
    if _exam_one_catch:
        mc "If Mom says yes."
    else:
        mc "After track."
    ah "Huh."
    mc "What?"
    if _exam_one_catch:
        show asahina neut
        ah "Nothing."
        "She turns her glass on the table, a quarter turn at a time."
        ah "I hope she says yes, okay?"
        mc "Me too."
    else:
        show asahina teasing
        ah "Nothing. Usually you need three days' notice and a written invitation before you'll admit you want to have fun."
        mc "The arcade simplified the math."
        ah "Understandable."
    "Her phone lights up next to her bowl. Sam's name sits at the top for exactly as long as it takes her to flip it over with the side of her hand."
    mc "You get the biology block moved?"
    show asahina neut
    ah "Yep. Forty-five minutes Sunday instead."
    mc "And he was okay with that?"
    show asahina embarrassed
    ah "Yeah, he said it was fine and that I'd earned a break. Which was... nice, I guess. Not that I needed permission."
    "She eats another mouthful and glances at the dark phone."
    show asahina neut
    ah "Then he asked which arcade we were going to."
    mc "Did you tell him?"
    show asahina curious
    ah "Yeah? Why wouldn't I tell him?"
    mc "...No reason. Just asking."
    show asahina unamused
    "Asahina leans back and gives me a long, flat stare across the table."
    ah "You get weird every time his name comes up. Like, every single time."
    mc "You brought him up. I asked a question."
    "She doesn't let up, so I go for the serving bowl. If she's happy with the arrangement, I don't need to keep up with the details."
    "The phone stays facedown."
    "We finish dinner with Mom's chair between us and the cabinet still holding its extra bowl."
    "Mom texts that the meeting has turned into document review. Asahina sends a thumbs-up, and I tell her we saved a plate."
    $ update_character_thought("mom", "Mom left before breakfast for a case meeting and stayed late for document review. Asahina set her place at dinner by accident and put the extra bowl away.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The evening separates into rooms. Asahina takes a call behind a mostly closed door and repacks her bag twice."
    nier "Much later, Mom gets home with two folders under one arm and the night air following her in. She squeezes my shoulder on her way to the couch."
    call nier_clear from _call_nier_clear_0530_6
    stop music fadeout 1.0
    pause 2.0
    scene bg living_room_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music house_day_a
    "Mom has wedged herself into one end of the couch with a folder on her knee and the plate balanced on top of it, so she's reading and eating and doing neither very well."
    show mom uniform unamused at t11
    mc "The folder is not a placemat."
    mom "It is rigid, flat, and currently protecting the couch."
    mc "Persuasive. Still wrong."
    "I set a glass of water on the coffee table and slide the folder out from under the plate. Her hand follows it, a little late, and drops to the cushion once it's out of reach."
    show mom uniform neut
    mom "Thank you."
    "She takes her first real bite of dinner. The steam is long gone, but the ginger still slows her down."
    mc "How bad was it?"
    show mom uniform frustrated
    mom "Boring bad."
    mc "Technical term?"
    mom "Half the documents went to the wrong address, and then six adults spent an hour rebuilding a timeline nobody had thought to write down."
    mc "So, group-project bad."
    show mom uniform smug
    mom "And six salaries."
    show mom uniform neut
    "She drinks half the water and sets the glass down."
    mom "It should have taken twenty minutes."
    "She tracks the folder in my hand."
    mom "You can put that beside me now."
    mc "You may finish eating first."
    show mom uniform unamused
    mom "Bossy child."
    mc "Inherited."
    show mom uniform happy
    "Her mouth twitches around the next bite."
    "I park the folder at the far end of the coffee table and come back from the kitchen with the cucumbers we saved for her."
    show mom uniform curious
    mom "What is this?"
    mc "Something with a color."
    show mom uniform embarrassed
    "She looks past me toward the dining room, where her morning note is still tucked under the sugar bowl."
    mom "...Ah."
    mc "What did you have for lunch?"
    mom "There were crackers in the conference room. I had more than one."
    mc "Beige doesn't count."
    show mom uniform teasing
    mom "They came in a green packet."
    mc "Nice try. Eat the cucumbers."
    "She eats them without further appeal, and I sit down across from her. The TV stays off, and upstairs, a laugh bursts out of Asahina's room and gets muffled halfway."
    show mom uniform curious
    mom "You two managed dinner?"
    mc "We followed both notes and only set one unnecessary place."
    show mom uniform thinking
    "Mom stops with her chopsticks over the plate."
    mom "Asahina?"
    mc "Habit. She fixed it."
    show mom uniform sad
    "She doesn't say anything to that. The next bite just takes her longer."
    show mom uniform neut
    if _exam_one_catch:
        show mom uniform thinking
        mom "You have something to ask me."
        "The folder stays where I parked it. She sets her plate down and turns to me instead of reaching for it."
        mc "Matsuda and Tsubaki asked me to meet them after track tomorrow. By the time Coach lets me go, they'll probably be at the arcade."
        mom "Are you asking to go?"
        mc "Yes."
        show mom uniform unamused
        mom "I told you that anything after track had to be asked, not announced."
        mc "I know."
        mom "Then tell me why I should change the restriction."
        "Everything I rehearsed on the walk home suddenly sounds arranged."
        mc "I don't know if you should yet. I just... want you to, and I can make it easy for you to know where I am."
        "Mom waits and doesn't help me finish."
        mc "Location sharing stays on, and I'll message when I leave track, when I get to the arcade, and before we leave for food or home."
        mom "And if everybody wants to stay past the time we agree on?"
        mc "I ask before anything changes. If you say no, I leave when we agreed."
        show mom uniform determined
        "She studies me while the plate cools between us. I catch myself trying to look trustworthy, then let my face do whatever it is already doing."
        mom "I want to be able to say yes when you ask me things. I'm going to trust you to keep that agreement."
        mom "You may go tomorrow, with location sharing on and your phone answered when I call."
        mc "I--"
        mom "You are home by eight-thirty unless you ask me and I approve a change first."
        "The breath I've been holding finally reaches the bottom of my lungs."
        mc "Okay. ... Thank you."
        mom "Your phone stays with you until you are home. The laptop remains downstairs, and Monday's advisor meeting has not moved."
        mc "I know."
        show mom uniform unamused
        mom "Don't make {i}I know{/i} carry the whole agreement for you."
        mc "I'll check in when I said I would."
        "Mom nods and picks up her water."
    else:
        mom "What's happening tomorrow after school? Your sister's message contained {i}arcade{/i}, {i}volleyball{/i} and {i}do not be weird about it{/i}. It did not contain a time."
        mc "Track first, then I'm meeting Matsuda and Tsubaki at the arcade. Asa might join when volleyball lets out."
        mom "Matsuda... sidewalk traffic?"
        mc "The very same."
        mom "And Tsubaki is the quiet girl from the roof?"
        mc "You know an alarming amount about my week."
        show mom uniform smug
        mom "Your sister narrates at volume. Some of it survives."
        "She takes another cucumber."
        mom "Do I know where this arcade is?"
        mc "Near the used bookstore by the station. That's where they're starting."
        show mom uniform determined
        mom "All right. Keep your phone charged, and tell me when you leave the arcade, especially if dinner gets involved. Home by eight-thirty, and that goes for your sister too."
        mc "Okay."
        show mom uniform teasing
        mom "Look at that. Cooperation."
        mc "In the spirit of full disclosure, Sam isn't going."
        show mom uniform curious
        "One of Mom's eyebrows climbs over the edge of the plate."
        mom "I was not going to ask."
        mc "You did the eyebrow."
        show mom uniform smug
        mom "The eyebrow was a comment. It was not a question."
        show mom uniform thinking
        "Her eyes drift up to the ceiling, in the direction of that laugh, and come down to me again."
        mom "You sound like you're looking forward to tomorrow."
        mc "It's an arcade."
        show mom uniform smug
        mom "You dodged."
        mc "No, that was the whole answer."
        show mom uniform happy
        "She smiles and lets it stand."
    "She finishes the rice and sets the plate down next to the water."
    show mom uniform neut
    mom "I'm going to sit here for five minutes and not read anything."
    mc "Bold plan."
    mom "After that, I'll check the address list and the timeline once more and go to bed."
    mc "Sustainable."
    "She leans back with her eyes closed, both hands open in her lap. I take her plate and glass to the kitchen and leave the folder exactly where it is."
    if _exam_one_catch:
        $ update_character_thought("mom", "I asked Mom before treating Saturday as settled, and she noticed. Her yes comes with check-ins, a curfew, and Monday's advisor meeting still ahead.")
    else:
        $ update_character_thought("mom", "Mom came home late after a case meeting turned into an hour of rebuilding a missing timeline. She ate the dinner we saved and accepted her own something-with-color rule.")
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music night_b
    "By the time I've changed, my floor has become a staging area: school bag by the desk, uniform shirt over the chair, and my wallet and portable charger lined up next to an arcade card that hasn't seen daylight in months."
    "I squint at the card's faded balance and try to decide how much cash to bring. My phone buzzes halfway through the decision."
    "Matsuda has made a group chat called Saturday so we can find each other after practice."
    if _exam_one_catch:
        python:
            _phone_messages = [
                phone_msg("them", "Matsuda: By solemn and completely unanimous agreement, tomorrow's order is bookstore, arcade, food!"),
                phone_msg("them", "Tsubaki: It was not unanimous. I'm the one who asked for the bookstore first."),
                phone_msg("them", "Asahina: i'll meet you at the arcade whenever volleyball releases me"),
                phone_msg("me", "Mom said yes. I need to check in when I leave track, when I get there, and before food."),
                phone_msg("me", "So don't hold the bookstore for me."),
                phone_msg("them", "Tsubaki: Okay. We'll keep the location simple."),
                phone_msg("them", "Matsuda: No surprise detours and no improvising with the clock. Understood."),
            ]
    else:
        python:
            _phone_messages = [
                phone_msg("them", "Matsuda: By solemn and completely unanimous agreement, tomorrow's order is bookstore, arcade, food!"),
                phone_msg("them", "Tsubaki: It was not unanimous. I'm the one who asked for the bookstore first."),
                phone_msg("them", "Matsuda: You failed to object in time, Kareda. Destiny has spoken!"),
                phone_msg("them", "Asahina: i'll meet you at the arcade whenever volleyball releases me"),
                phone_msg("me", "Same for track. Don't hold the bookstore for me."),
                phone_msg("them", "Tsubaki: Works for me."),
                phone_msg("them", "Matsuda: Then it is written!"),
                phone_msg("me", "You named this chat Saturday. I'm proud of you."),
                phone_msg("them", "Matsuda: The first six names were rejected by people with no poetry in their souls!"),
                phone_msg("them", "Tsubaki: They all had the word fellowship in them."),
                phone_msg("them", "Asahina: i would have left instantly"),
                phone_msg("them", "Matsuda: Philistines! All of you!"),
            ]
    call phone_text_conversation("Saturday", _phone_messages, status="3 participants", append=True) from _call_phone_text_conversation_0530_1
    "The thread goes quiet with food still deadlocked between noodles and burgers. I slide the arcade card into my wallet, and the phone goes off again on its way to the desk."
    python:
        _phone_messages = [
            phone_msg("them", "I opened one of the rescued journals and found a recipe for onion soup!"),
            phone_msg("me", "Literature's finally useful."),
            phone_msg("them", "It's written as a love poem. An actual LOVE POEM. I can't even tell when you're supposed to add the stock."),
            phone_msg("me", "As long as nobody throws the stock away. Send a picture and I'll figure it out."),
            phone_msg("them", "Tomorrow! I'm already in bed, and the journal's all the way downstairs."),
            phone_msg("them", "Have fun tomorrow, " + player + "!"),
            phone_msg("me", "Thanks. Night, Monika."),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0530_2
    $ hide_calendar()
    scene black with wipeleft_scene
    if _exam_one_catch:
        nier "At ten, the phone goes downstairs to the kitchen charger. Monday's advisor meeting waits on the far side of a Saturday full of school, track and every check-in I promised."
    else:
        nier "For once, nobody has assigned the weekend a purpose. Tomorrow is school, then track, then an arcade, if my left foot keeps its opinions to itself."
    nier "In my school bag, the traveler is still standing at the top of the stairs."
    call nier_clear from _call_nier_clear_0530_7
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0530_1
    jump a0531
