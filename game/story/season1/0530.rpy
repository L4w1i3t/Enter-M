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
    # Saturday without negotiation. Her relationship with Monika and access to the club remain
    # future developments. The single acting gap is comic and human: a grating hillbilly persona
    # collapses into her plain voice when she realizes she is doing the voice thing again.
    # Ledger meters moved quietly: Matsuda joins an existing after-school plan; Tsubaki protects
    # her own preferences; Monika and MC restore their club routine; Mom's work thins the house;
    # Sam's schedule remains useful enough that Asahina sees no reason to question it.
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music dailyleisure
    window auto
    "Mom's chair is empty, and a note has been pinned under the sugar bowl to stand in for her."
    "Her handwriting leans harder to the right when she writes in a hurry. This one looks like it nearly outran the paper."
    call enter_m_show_sticky_note(("Early client meeting.", "Rice is warm.", "Eat something with a color.", "Home late.", "Love you both."), signature="Mom") from _call_enter_m_show_sticky_note_0530_1
    "Three instructions and one forecast, with an emotional clause tucked at the bottom so neither of us can object to the contract."
    show asahina uniform thinking at t11
    "Asahina sits across from the empty chair with her phone beside her bowl and a piece of egg held between her chopsticks."
    "The egg has been airborne long enough to need clearance from air traffic control."
    mc "You planning to eat that, or is this a demonstration?"
    ah "Shh. I'm moving something."
    mc "The egg?"
    ah "Saturday after school."
    "She drags a blue block across the screen, frowns, and drags it back."
    "I catch labels before she tilts the phone away: volleyball, review, dinner, and one blank strip in the middle that keeps changing its mind."
    mc "The hours after final bell need zoning approval now?"
    show asahina uniform neut
    ah "Sam made the study grid. I'm editing it."
    mc "Bold. Does the architect allow renovations?"
    show asahina uniform annoyed
    ah "It's my schedule, genius."
    "She says it quickly, then moves the review block again with more care than the sentence suggests."
    ah "Also, I don't need two hours of biology after a full Saturday of school when exams are already over."
    mc "Reasonable. Your mitochondria can fend for themselves."
    show asahina uniform smug
    ah "Exactly. Their weekend starts when mine does."
    "The egg finally completes its journey."
    "Mom's chair stays empty while we eat. Her mug is gone, her case folder is gone, and nobody reaches over to turn Asahina's phone facedown when it starts stealing breakfast."
    "The kitchen works without her. It just takes longer to decide what shape to hold."
    show asahina uniform curious
    ah "You have club today, right?"
    mc "Real hours, according to the president. Actual writing and everything."
    show asahina uniform pose_eyeroll
    ah "Wow. Literature at the literature club. Risky pivot."
    mc "We're testing the market."
    show asahina uniform curious
    ah "And track?"
    mc "Coach gave me today off. Practice is back tomorrow after classes, assuming the foot continues respecting the ceasefire."
    ah "So you're free after practice."
    mc "Technically."
    show asahina uniform neut
    "Her eyes go to the blank strip on her screen, then to me."
    ah "Any plans?"
    mc "Nothing scheduled."
    show asahina uniform unamused
    ah "That's not what I asked."
    mc "Then ask a lawyer."
    ah "We have one, but she fled the jurisdiction."
    "She nods toward the note."
    show asahina uniform worried
    "For a second both of us look at Mom's chair."
    "She locks her phone and picks up her bowl."
    show asahina uniform neut
    ah "Whatever. If something comes up, tell me before I commit to staring at a cell diagram all evening."
    mc "Why?"
    show asahina uniform embarrassed
    ah "Because I may have an opening. Don't make it weird."
    "She takes her bowl to the sink before I can turn that into a cross-examination."
    show asahina at thide
    hide asahina
    "I finish breakfast and wash the extra dish Mom normally catches first. Her note goes back under the sugar bowl instead of into the trash."
    "There is no practical reason to keep it."
    "I keep it."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Asahina and I leave on time, which feels less like competence than the house releasing us after a brief inspection."
    nier "The walk to school is bright, warm, and full of students discussing everything they plan to do once Saturday finally lets them go."
    nier "I contribute nothing to any of it and reach the first bell with time to spare."
    call nier_clear from _call_nier_clear_0530_1
    stop music fadeout 1.0
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    with dissolve_scene_full
    play music schooldays
    "Friday classes make a respectable attempt at returning to normal."
    "Physical education is mostly stretching and collective dishonesty about how sore everyone is. Civics gives us a reading for next week. Language arts asks for a reflection on the exam, which feels like making the victim write the incident report."
    "By biology, even the teachers have stopped pretending the room will remember anything introduced today."
    "The midterm portal remains locked. Monday waits behind it with six numbers and no interest in how pleasant Sunday was."
    "I write the date at the top of a clean page and copy the biology assignment beneath it. Staying awake for the parts in between is the harder assignment."
    "A modest return to form, but a return."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Lunch releases the building into its usual migration."
    nier "Asahina has volleyball business and Monika is trapped in a student-council handoff, so I take my food to the roof and skip the committee stage entirely."
    nier "Someone has beaten me there."
    call nier_clear from _call_nier_clear_0530_2
    stop music fadeout 1.0
    pause 2.0
    scene bg rooftop
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music dailyfantasy
    play sound moddooropen
    "The rooftop door gives its usual metal complaint."
    "Tsubaki is already near the shaded wall, her lunch arranged beside a stack of index cards held together with a pale blue binder clip."
    "She looks up, lets an unaudited smile through, and lifts one hand."
    show tsubaki uniform happy at t11
    ts "Hey."
    mc "Hey. Roof still in its responsible-volume phase?"
    "Her smile stays this time."
    show tsubaki uniform teasing
    ts "So far. The wind has been a little disruptive."
    mc "I'll note the violation."
    "I sit a polite distance away and unpack lunch."
    "She has already wiped a bead of condensation from her drink and turned the label outward. Her index cards are numbered in the upper-right corner despite the exams being over."
    mc "Studying already?"
    show tsubaki uniform neut
    ts "No. Inventory."
    show tsubaki uniform neut
    "She lifts the top card. It contains a short list written in straight, small lettering."
    ts "I kept mixing up what was in my school bag and what was in Matsuda's after she carried my things on Wednesday."
    ts "So I made separate lists."
    mc "You inventoried her bag?"
    show tsubaki uniform panicked
    ts "Only the things she gave back to me! I wasn't searching it."
    show tsubaki uniform nervous
    "Her fingers close around the cards."
    show tsubaki uniform sad
    ts "That sounded invasive. Sorry."
    mc "It sounded organized. You're allowed to know where your own pens are."
    show tsubaki uniform neut
    "Her grip loosens one finger at a time."
    ts "Right. Yeah."
    "She slides the cards beneath her notebook, safe from the wind and further questions."
    show tsubaki uniform neut
    "For a little while, we eat without asking the silence to perform."
    "Her lunch is as neat as it was last week: rice in one section, vegetables in another, one piece of fried chicken saved until everything else is halfway gone."
    show tsubaki uniform curious
    ts "How was track yesterday?"
    mc "Boring in the medically approved way."
    ts "That's good, right?"
    mc "Very. Coach only told me to hydrate three times."
    show tsubaki uniform teasing
    ts "Only?"
    mc "A glowing review."
    "The saved piece of fried chicken gets promoted ahead of schedule."
    show tsubaki uniform neut
    ts "Matsuda said she might ask you to come with us after school tomorrow."
    mc "She mentioned a possible bookstore thing."
    show tsubaki uniform happy
    ts "Yeah. The used place near the station is clearing out old magazines, then we were going to the arcade."
    show tsubaki uniform thinking
    "She straightens the paper sleeve around her chopsticks."
    ts "We planned it before exams. It kept getting moved because of studying."
    mc "The arcade part sounds compelling."
    show tsubaki uniform smug
    ts "I figured it might."
    mc "What, I look that easy to market to?"
    show tsubaki uniform teasing
    ts "You talk about games a lot."
    mc "Fair."
    show tsubaki uniform worried
    "She takes another bite, then glances toward the door."
    ts "She wanted to ask you herself, though."
    mc "Then I will avoid accepting the invitation through unauthorized counsel."
    show tsubaki uniform determined
    ts "Thank you. I don't want to be her secretary."
    show tsubaki uniform shocked
    "The sentence comes out cleanly. Tsubaki seems surprised by how much she means it."
    mc "You'd need benefits."
    show tsubaki uniform smug
    ts "And noise protection."
    "She delivers it quietly, and it takes me a second."
    show tsubaki uniform happy
    "I laugh. She does too, one short sound through her nose that she did not authorize."
    show tsubaki uniform determined
    ts "I want the bookstore first, by the way."
    mc "Noted."
    show tsubaki uniform neut
    ts "The magazine tables are easier before people start carrying arcade prizes through them."
    mc "Specific concern."
    show tsubaki uniform annoyed
    ts "It happened last time. Someone hit me with an inflatable sword."
    mc "A casualty of poor route planning."
    show tsubaki uniform unamused
    ts "Exactly."
    # SFX SUGGESTION: A distant warning bell carrying through the rooftop door.
    "The warning bell rings below us."
    show tsubaki uniform neut
    "She clips the index cards together and returns everything to the correct bag on the first try."
    show tsubaki uniform happy
    ts "See you later."
    mc "Later."
    "She gets to the door, pauses, and turns back."
    show tsubaki uniform nervous
    ts "You don't have to come, obviously."
    mc "I know. It still sounds fun."
    show tsubaki uniform happy
    "That earns a quick smile."
    "Then she heads downstairs before the staircase fills."
    show tsubaki at thide
    hide tsubaki
    play sound moddoorclose
    "I finish the last two bites of lunch and follow."
    $ update_character_thought("tsubaki", "Tsubaki keeps an inventory so her things do not disappear into Matsuda's bag. She also said plainly that she is not Matsuda's secretary, then insisted the bookstore comes before the arcade.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Afternoon classes pass through the part of Friday that already belongs to after school."
    nier "By seventh period, notebooks close a little early and every conversation points past tomorrow's classes toward whatever can fit afterward."
    nier "I head for the club room ready to write something that is not an exam answer."
    call nier_clear from _call_nier_clear_0530_3
    stop music fadeout 1.0
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music schooldays
    "I find Monika one corridor short of the club room, carrying a cardboard box that has already begun negotiating its own collapse."
    show monika forward uniform nerv cm oe awkw rdown ldown at t11
    "Her chin holds the top flap down. Three thin notebooks are wedged beneath one arm, and several folded slips of paper protrude from her blazer pocket like surrender flags."
    mc "Need a permit for that load?"
    m forward uniform nerv om oe awkw rdown ldown "I need the bottom not to fall out before the next door."
    "I take the box before gravity gets involved."
    "It is heavier than the notebooks on top suggested."
    mc "What did you steal?"
    m forward uniform happ om oe nobl rdown ldown "Rescued. The library was clearing old literary journals and duplicate anthologies from storage."
    "The top layer contains slim school publications that predate both of us, their covers faded into several historical shades of beige."
    m forward uniform happ cm oe nobl rdown ldown "They were going to recycle all of it. I asked whether the club could take a box first."
    mc "One box."
    "Monika finds something interesting in the corner behind us."
    "A second box waits beside the wall."
    mc "Of course."
    m forward uniform pout om oe awkw rdown ldown "There were good things in there!"
    mc "You have not opened most of them."
    m forward uniform nerv om oe awkw rdown ldown "There are potentially good things in there."
    "She moves the notebooks from under her arm to the top of my box and catches one before it slides."
    m forward uniform happ cm oe nobl rdown ldown "Also, everyone has been writing on exam paper for a week. I thought fresh notebooks might help reset the atmosphere."
    mc "Bribery through stationery."
    m forward uniform happ om oe nobl rdown ldown "Presidential morale policy."
    "She laughs, but keeps one hand on the box after I have its weight."
    "Her thumb rubs the cardboard edge."
    m forward uniform neut cm oe nobl rdown ldown "The club got very quiet this week."
    mc "Everyone had exams."
    m forward uniform neut om ce nobl rdown ldown "I know."
    "She adjusts one of the folded slips in her pocket."
    m forward uniform worr om oe nobl rdown ldown "I just don't want exam quiet to become normal quiet. Hikari and Homura only stopped fighting because neither of them had time to write anything worth fighting over."
    mc "A fragile peace."
    m forward uniform nerv om ce blaw rdown ldown "Terrible for literature."
    "She smiles, then pulls the slips free."
    "Three prompts, each folded twice and marked with a different ink color."
    m forward uniform happ om oe nobl rdown ldown "Help me pick."
    mc "You are delegating presidential authority in a public corridor."
    m forward uniform happ om oe nobl rdown lpoint "I'm crowdsourcing. It sounds more modern."
    "She fans the slips out facedown."
    m forward uniform happ om oe nobl rdown lpoint "Blue, red, or black."
    mc "What do the colors mean?"
    m forward uniform happ cm ce nobl rdown ldown "That would undermine the highly scientific process."
    "I shift the box against my hip and choose blue."
    "She unfolds it."
    m forward uniform happ cm oe nobl rdown ldown "Give directions to a place that does not exist."
    mc "What were the others?"
    "She opens red."
    m forward uniform neut om oe nobl rdown ldown "Write an apology from an object that has outlived its use."
    mc "Cheerful."
    "Black reads: {i}Describe a room one minute after everyone leaves.{/i}"
    mc "You prepared three different kinds of absence."
    m forward uniform happ om oe nobl rdown ldown "I prepared three post-exam prompts."
    "She looks at them together and makes a face."
    m forward uniform nerv om ce blaw rdown ldown "...Okay, maybe I had a theme."
    mc "Directions is the least likely to cause a group crisis."
    m forward uniform laug om ce nobl rdown ldown "An excellent presidential metric."
    "She refolds the other two and puts them away."
    mc "You already wanted blue."
    m forward uniform curi om oe nobl rdown ldown "Why do you say that?"
    mc "You used the nice pen."
    "The prompt is written in the same green ink she reserves for finished headings and notes she wants people to keep."
    "She keeps her eyes on the paper, caught."
    m forward uniform happ cm oe nobl rdown ldown "I wanted a second opinion."
    mc "You wanted ratification."
    m forward uniform happ om oe nobl rdown lpoint "And I received it. Democracy works."
    "She takes the second box. It is lighter, though she carries it like accepting help should not exempt her from proving she could have managed both."
    m forward uniform happ cm oe nobl rdown ldown "I want today to feel like the club came back."
    mc "Then let's bring it back."
    "She nods once."
    "We carry the rescued journals, the clean notebooks, and the scientifically selected prompt down the final stretch of corridor."
    "At the club-room door, she reaches for the handle with her elbow."
    m forward uniform wry om oe awkw rdown ldown "If the box breaks now, I am resigning."
    mc "I'll record the transition of power."
    m forward uniform wry cm oe nobl rdown ldown "You are not next in line."
    mc "Then history loses nothing."
    "She gets the door open. The box survives."
    show monika at thide
    hide monika
    $ hide_calendar()
    stop music fadeout 1.0
    pause 2.0
    scene bg club_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music daily
    "The literature club is alive again."
    "This is not the exam-week version, with folders colonizing every table and Monika banning the word study by presidential decree. The room is actually alive."
    "Hikari is arguing with a stapler near the windows. Homura has claimed the back desk and three colors of pen. Somebody has opened the back locker and immediately regretted learning what lives behind the bottom shelf."
    "The rescued journals occupy the front table. The clean notebooks disappear almost immediately, and Monika pretends not to watch."
    "At the front, Monika writes the day's prompt on the board."
    show monika forward uniform happ cm oe nobl rdown ldown at t11
    "{i}Give directions to a place that does not exist.{/i}"
    m forward uniform happ om oe nobl rhip lpoint "Twenty minutes. Prose, poem, list, fake instruction manual -- whatever gets you there."
    hikari "If it doesn't exist, how do we know whether the directions work?"
    m forward uniform curi om oe nobl rhip lpoint "Commit to the premise."
    homura "That means she doesn't know either."
    m forward uniform wry om oe nobl rdown lpoint "That means leadership delegates uncertainty."
    "Monika sets the chalk down in the tray and turns toward me."
    m forward uniform wry om oe nobl rdown ldown "You're late by almost a minute."
    mc "I was delayed by a staircase."
    m forward uniform happ cm oe nobl rhip ldown "A known hazard. Sit down."
    "Her smile takes the accusation out of it."
    "I take my usual desk. The nick in the corner finds my thumb again, exactly where I left it."
    "Paper settles across the room. The club lowers into the scratch of pens, the occasional chair shift, and the communal effort of pretending a blank page is not looking back."
    "I write the prompt once, then cross it out because copying instructions is not the same as following them."
    "The city under the false sky comes to mind."
    "It occupied most of my free hours before exams took custody of the console, so it has earned a page."
    "My pen starts moving."
    "I stop when it runs out."
    call enter_m_showpoem(poem_0530_mc_draft) from _call_enter_m_showpoem_0530_1
    "It is an image, technically. Several images in a coat, hoping nobody asks for a destination."
    "Monika makes a slow circuit of the room, answering one question and refusing two attempts to make her define nonexistent."
    "When she reaches my desk, she looks down without leaning in to read."
    m forward uniform curi om oe nobl rdown ldown "Stuck?"
    mc "I'm giving the place time to exist."
    m forward uniform happ cm ce nobl rdown ldown "Generous."
    mc "So far it has a train and hostile municipal lighting."
    m forward uniform wry cm oe nobl rdown ldown "Sounds welcoming."
    "She rests two fingers on the empty desk beside mine."
    m forward uniform curi om oe nobl rdown ldown "Where does the person want to go?"
    mc "That seems outside the prompt."
    m forward uniform neut om oe nobl rdown ldown "That's why I'm asking."
    "I look back at the page."
    "The traveler has instructions, a conductor, a timetable nobody wrote down, and multiple colors of warning. Wanting something never occurred to me."
    mc "Home, probably."
    m forward uniform curi om oe nobl rdown ldown "Probably?"
    mc "I haven't decided where home is."
    m forward uniform happ om oe nobl rdown lpoint "Then that is your useful problem."
    "She taps the empty space beneath my last line and continues to the next desk."
    "I add one sentence."
    call enter_m_showpoem(poem_0530_mc_revised) from _call_enter_m_showpoem_0530_2
    "It is less clever than the train."
    "It is also the first line that points anywhere."
    # SFX SUGGESTION: A short timer tone, followed three seconds later by Monika's single sharp clap.
    "The timer sounds before I can make it prettier."
    m forward uniform happ om oe nobl rhip lpoint "Pens down, or at least pens hovering guiltily."
    "A few people keep writing through the instruction. Monika permits the rebellion for three seconds before clapping once."
    m "Voluntary exchange. Find someone, trade pages, and ask one useful question."
    "Hikari turns toward Homura before the last word finishes."
    "Monika reaches my desk with her notebook already extended."
    m forward uniform happ om oe nobl rdown ldown "Trade?"
    mc "Presidential coercion."
    m forward uniform wry om oe nobl rdown lpoint "Voluntary presidential coercion."
    "We swap."
    "Her piece is written as a numbered list."
    call enter_m_showpoem(poem_0530_monika) from _call_enter_m_showpoem_0530_3
    "I look up."
    "Monika is reading my train piece with one finger resting near the last line."
    mc "This place exists."
    m forward uniform nerv om oe awkw rdown ldown "Not when I wrote the directions."
    mc "The old bank and awning are doing a lot of evidentiary work."
    m forward uniform nerv om ce blaw rdown ldown "Details can be aspirational."
    mc "And the second cup?"
    "Her gaze drops to the notebook."
    m "Also aspirational."
    "The club keeps moving around us. A page turns. The stapler finally loses its argument with Hikari. Somebody near the back locker asks whether dust can stain a uniform."
    "I read Monika's final line again."
    mc "I like it."
    m forward uniform curi om oe nobl rdown ldown "Even though I cheated?"
    mc "Especially because you cheated. It made somewhere real without pretending you invented it."
    "Her smile is small and immediate."
    m forward uniform happ cm oe nobl rdown ldown "Your last line works."
    mc "The dishes?"
    m forward uniform happ cm oe nobl rdown ldown "The dishes."
    "She turns my notebook so the line faces both of us."
    m forward uniform neut cm oe nobl rdown ldown "Everything before it tells me what the place looks like. That line tells me why someone would keep walking."
    mc "I thought the hostile lighting was carrying the piece."
    m forward uniform happ cm ce nobl rdown ldown "It contributes atmosphere."
    mc "A dignified demotion."
    "Monika returns my notebook."
    m forward uniform neut om oe nobl rdown ldown "Keep the train. Keep the television. Decide whether the traveler goes inside."
    mc "Homework?"
    m forward uniform happ cm oe nobl rhip lpoint "One line. Monday."
    mc "This club has become academically compromised."
    m forward uniform laug om ce nobl rdown ldown "And yet you keep attending."
    "She moves on before I can produce a defense."
    "For the rest of the hour, club gets to be club."
    "Drafts move across desks. Hikari's moon elevator acquires a broken call button. Homura removes one entire paragraph and looks physically lighter afterward."
    "Monika circulates, gives notes, takes one argument about semicolons under advisement, and squares the chalk in the tray at the exact center of the board."
    "Nobody studies for an exam or says midterm."
    "The room remembers what it was for."
    $ update_character_thought("monika", "Monika restored the club with a directions prompt and turned my fake train station toward a television and dishes. She wants one more line on Monday.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Club ends at its real hour, with pages in bags and the board still carrying directions to nowhere."
    nier "Monika stays behind to finish attendance. I shoulder my bag and join the corridor with my homework capped at one line."
    nier "Tsubaki is waiting near the windows. She is not alone."
    call nier_clear from _call_nier_clear_0530_4
    stop music fadeout 1.0
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("evening")
    with wipeleft_scene
    play music schooldays
    show tsubaki uniform unamused at t21
    show matsuda uniform teasing at t22
    "Matsuda pushes off the wall when she sees me."
    stop music fadeout 1.0
    play music enterm
    ma "Well, look what finally wandered outta the book barn! Been posted up by this here window so long I near took root."
    "The accent hits my ears like a screen door slamming in a storm."
    mc "Why do you sound like that?"
    ma "Ain't nothin' wrong with how I sound, partner. Reckon I found me a voice with grit."
    ts "She's been doing this since lunch."
    ma "Kareda ain't got no appreciation for regional splendor."
    show tsubaki uniform annoyed
    ts "You have never lived in that region."
    ma "Ain't gotta live somewhere to appreciate the local craftsmanship."
    mc "Your heart needs to roam several meters away from my ears."
    "Matsuda clutches one gloved hand to her chest, mortally offended."
    ma "Well, shoot. Fella comes outta his fancy word corral swingin'."
    mc "Every vowel is getting longer."
    show tsubaki uniform unamused
    ts "I warned you."
    "Matsuda ignores both of us and plants her feet like the corridor has become a porch."
    ma "Now, me an' Kareda are fixin' to mosey on down to that used-book place after school tomorrow, then haul ourselves over to the arcade, an' we were wonderin' if y'all might--"
    "She stops."
    show matsuda unamused
    "Her mouth stays open around the next mangled syllable, then closes."
    "The accent disappears when she speaks again."
    ma "...Okay, stiff crowd today."
    "She rolls one shoulder and looks briefly annoyed with herself rather than either of us."
    ma "Guess I'm being me again. I'll shelf the hick..."
    ma "Sorry."
    "The apology is plain, and it takes the fight out of my next line."
    show matsuda neut
    show tsubaki uniform neut
    "Tsubaki watches her, index cards held loosely against her bag."
    ma "Normal question. Kareda and I are going to the used bookstore after school tomorrow, then the arcade, then probably food."
    ma "You have track. If you want to meet us at the arcade whenever practice ends, would you like to come?"
    "She leaves the question there without a speech behind it."
    mc "Yeah. That sounds fun."
    show matsuda happy
    "Matsuda's whole prepared speech goes unused."
    ma "Cool."
    "She glances at Tsubaki, who gives the smallest nod."
    ma "I'll make a group chat after I ask Asahina herself. She can join whenever volleyball lets her go, if she wants."
    mc "Works for me."
    show tsubaki uniform determined
    ts "Bookstore first."
    ma "Bookstore first."
    show tsubaki uniform happy
    ts "Thank you."
    "She clips her cards together. The order has apparently survived committee."
    show matsuda teasing
    ma "Well then, I reckon--"
    show tsubaki uniform unamused
    ts "No."
    show matsuda unamused
    "Matsuda closes her eyes and lets the accent die."
    ma "Fine."
    show matsuda smug
    "I lose the laugh completely. She points at me, vindicated."
    ma "You laughed. The voice stays in rotation."
    mc "That was relief."
    ma "History will misquote you."
    "The accent does not return. She only looks pleased that I said yes."
    ma "See you tomorrow, [player]."
    mc "After track."
    ma "After track."
    show tsubaki uniform happy
    ts "See you."
    mc "Later."
    show matsuda at thide
    show tsubaki at thide
    hide matsuda
    hide tsubaki
    stop music fadeout 1.0
    "They head toward the east gate, Tsubaki half a step ahead while Matsuda argues that one reckon should be permitted per hour."
    "I take the road home alone, thinking mostly about whether I still have enough coins in the jar on my desk."
    $ update_character_thought("matsuda", "Matsuda tried a hillbilly voice that made every vowel feel physically longer. She caught herself, dropped it, and asked normally whether I wanted to meet her and Tsubaki at the arcade after track. I said yes.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Home is dark when I reach it."
    # SFX SUGGESTION: The front door latch closing into an empty house with a slight room echo.
    nier "Not night-dark. Empty-house dark: curtains half open, kitchen clock bright enough to be rude, no voice answering the door before it closes."
    nier "Mom's shoes are still gone. Her note remains under the sugar bowl where I left it."
    call nier_clear from _call_nier_clear_0530_5
    stop music fadeout 1.0
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    play music fantasypassion
    play sound moddooropen
    "Asahina comes in not long after me with her gym bag on one shoulder and her phone already unlocked."
    show asahina unamused at t11
    ah "Your redhead friend writes like she's filing a royal decree."
    mc "Hello to you too."
    ah "She asked if I want to meet you guys at the arcade after volleyball. Full sentences, actual order of operations, no weird group name."
    mc "Give her time."
    show asahina teasing
    ah "She called me Lady Asahina once, but I think that's a manageable contaminant level."
    mc "Did you say yes?"
    # SFX SUGGESTION: A gym bag thump followed by the refrigerator seal pulling open.
    show asahina neut
    "She drops her bag beside the chair and swings through to the refrigerator."
    ah "Maybe."
    mc "You said yes."
    show asahina smug
    ah "I said I might appear if practice doesn't kill me. Different legal standard."
    "She pulls out the covered leftovers and reads Mom's second note, this one attached to the lid."
    call enter_m_show_sticky_note(("Heat three minutes.", "Stir.", "One more minute.", "I mean it."), signature="Mom") from _call_enter_m_show_sticky_note_0530_2
    ah "She anticipated us."
    mc "Our methods are discoverable."
    "We follow the microwave instructions with the respect due a binding order."
    "Dinner becomes rice, leftover ginger chicken, cucumbers, and the two of us making three separate trips because Mom usually remembers the things neither of us does."
    "On the second trip, I get drinks. On the third, Asahina retrieves chopsticks and stares at the table."
    "Three places are set."
    show asahina sad
    "Her hand rests on the back of Mom's chair."
    ah "Oh."
    "She removes the extra bowl and returns it to the cabinet."
    "Neither of us says anything while she does it."
    "The table looks larger afterward."
    mc "Mom said late, not never."
    show asahina neut
    ah "I know."
    "She sits."
    "We start eating. The refrigerator hums into the part of dinner Mom usually fills by asking questions we pretend are invasive."
    show asahina curious
    ah "So you're actually going tomorrow?"
    mc "After track."
    ah "Huh."
    mc "What?"
    show asahina teasing
    ah "Nothing. You usually require several business days to approve fun."
    mc "The arcade expedited the application."
    ah "Understandable."
    "Her phone lights beside her bowl. Sam's name is visible at the top before she turns it over."
    mc "You move the biology block?"
    show asahina neut
    ah "Yep. Forty-five minutes Sunday instead."
    mc "And the planning commission?"
    show asahina happy
    ah "He said it was fine and that I earned a break."
    "She takes another bite."
    show asahina neut
    ah "Then he asked which arcade."
    mc "Did you tell him?"
    show asahina curious
    ah "Yeah. Why wouldn't I?"
    mc "No reason."
    show asahina thinking
    "Asahina's attention crosses the table and stays there."
    ah "You do the weirdest pauses whenever his name comes up."
    mc "I pause weirdly in general. It's one of my defining traits."
    "She keeps looking for another second, then lets the subject go."
    "Her phone stays facedown."
    "We finish dinner around the empty chair."
    "Mom texts that the meeting became document review and she will be home late. Asahina sends a thumbs-up. I send an actual sentence so the household remains diversified."
    "Then we split the dishes between us. It does not require a negotiation."
    $ update_character_thought("mom", "Mom left before breakfast and came home late because a client meeting became document review. The house worked without her, but Asahina still set her place at dinner.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The evening separates into rooms."
    nier "Asahina showers, calls someone with her door mostly closed, and moves around upstairs far too much for someone with an empty tomorrow, which is how I know she has plans after school."
    nier "I do the dishes and check my foot. The Saturday uniform gets held up to the light and declared presentable enough to survive one more day."
    nier "Much later, Mom comes home carrying two folders and the smell of outside air. She kisses the top of Asahina's head, squeezes my shoulder, and accepts the plate we saved instead of claiming she already ate."
    nier "She takes dinner into the living room with the first folder still open."
    call nier_clear from _call_nier_clear_0530_6
    stop music fadeout 1.0
    pause 2.0
    scene bg living_room_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music dailyleisure
    "Mom has arranged herself at one end of the couch with the folder on her knee and the plate balanced on top of it."
    "This configuration allows her to read, eat, and do neither particularly well."
    show mom uniform unamused at t11
    mc "The folder is not a placemat."
    mom "It is rigid, flat, and currently protecting the couch."
    mc "Compelling opening argument. Still wrong."
    "I set a glass of water on the coffee table and slide the folder out from beneath the plate. Her objection arrives a second late and goes nowhere."
    "Mom lets me."
    show mom uniform neut
    mom "Thank you."
    "She takes the first real bite of dinner."
    "The ginger chicken has lost most of its steam. The flavor made it through anyway."
    mc "How bad was it?"
    show mom uniform frustrated
    mom "Boring bad."
    mc "Technical term?"
    mom "Settlement language changed after everyone had supposedly agreed to it. Then everyone spent an hour insisting the change was obvious, minor, and authored by somebody else."
    mc "So group project bad."
    show mom uniform smug
    mom "With invoices."
    show mom uniform neut
    "She drinks half the water before returning the glass."
    mom "Nothing dangerous. Nothing you need to solve. Just adults making an expensive problem out of a paragraph."
    "Her eyes move toward the folder in my hand."
    mom "You may put that beside me."
    mc "You may finish eating first."
    show mom uniform unamused
    mom "Hostile household takeover."
    mc "Emergency nutritional injunction."
    show mom uniform happy
    "Something happens at the corner of Mom's mouth, unauthorized."
    mom "Counsel has become insufferable."
    mc "Learned from precedent."
    "I put the folder on the far end of the coffee table, beyond comfortable reach."
    "There is a small pile of cucumber left in the kitchen. I retrieve it and add it to her plate."
    show mom uniform curious
    mom "What is this?"
    mc "Something with a color."
    show mom uniform embarrassed
    "She looks toward the kitchen, where her morning note is still tucked beneath the sugar bowl."
    mom "Ah."
    mc "What did you have for lunch?"
    mom "There were crackers in the conference room."
    mc "Cracker color does not count."
    show mom uniform teasing
    mom "They had a green label."
    mc "The court rejects the packaging defense."
    "Mom accepts the cucumbers without further appeal."
    "For a few minutes she eats while I sit in the chair opposite the couch."
    "The television is off. Asahina laughs once upstairs, then lowers her voice as though the floor reported her."
    show mom uniform curious
    mom "You two managed dinner?"
    mc "We followed both notes and only set one unnecessary place."
    show mom uniform thinking
    "Mom's chopsticks pause above the plate."
    mom "Asahina?"
    mc "Habit. She fixed it."
    show mom uniform sad
    "Mom nods. The next bite takes a little longer."
    show mom uniform neut
    mom "What is happening tomorrow after school? Her message contained the words arcade, volleyball, and do not be weird about it."
    mc "Track first. Then I'm meeting Matsuda and Tsubaki at the arcade. Asa might join when volleyball ends."
    mom "Matsuda. Sidewalk traffic?"
    mc "The very same."
    mom "And Tsubaki is the quiet girl from the roof?"
    mc "You have a concerningly complete case file."
    show mom uniform smug
    mom "Your sister narrates at volume. I retain things."
    "She takes another cucumber."
    mom "Do I know where this arcade is?"
    mc "Near the used bookstore by the station. Matsuda and Tsubaki are starting there."
    show mom uniform determined
    mom "All right. Keep your phone charged. Let me know when you leave the arcade, especially if dinner becomes part of the plan."
    mc "Reasonable."
    show mom uniform teasing
    mom "I treasure these rare rulings."
    mc "Sam isn't going, before you ask."
    show mom uniform curious
    "Mom's eyebrow rises over the edge of the plate."
    mom "I was not going to ask."
    mc "You did the eyebrow."
    show mom uniform smug
    mom "My face is not admissible evidence."
    mc "Asa says mine testifies against me all the time."
    show mom uniform unamused
    mom "Her standards are inconsistent."
    "The line is dry, but her eyes travel briefly toward the ceiling."
    "Then she looks back at me."
    show mom uniform thinking
    mom "You sound like you want to go."
    mc "It's an arcade."
    show mom uniform smug
    mom "That was not an answer."
    mc "It was the entire answer."
    show mom uniform happy
    "Mom smiles and lets me keep it."
    "She finishes the last of the rice and sets the plate on the table."
    "The folder remains beyond reach."
    show mom uniform neut
    mom "I am going to sit here for five minutes without reading anything."
    mc "Bold plan."
    mom "Then I will look at the paragraph again, discover it has not improved in my absence, and go to bed."
    mc "Sustainable."
    "She leans back and closes her eyes."
    "Her hands rest open in her lap instead of reaching for the folder."
    "I take the empty plate and glass to the kitchen and leave it at that."
    $ update_character_thought("mom", "Mom came home late after adults turned one changed paragraph into an expensive problem. She ate the dinner we saved, accepted her own something-with-color rule, and left the folder closed for five minutes.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Mom is home. The house does not become less tired, but it regains its center."
    nier "Upstairs, Asahina ends her call. In the living room, five quiet minutes begin."
    nier "I leave both of them alone and take tomorrow's ordinary problems to my room."
    call nier_clear from _call_nier_clear_0530_6_5
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music fantasyserenity
    "My bedroom floor has become a small staging area."
    "School bag by the desk. Uniform shirt on the chair. Wallet, portable charger, and the arcade card I have not used since winter lined up beside the alarm clock."
    "I check the arcade card balance on an app. It holds almost enough credit to be useful, which makes it tomorrow's problem."
    "My phone lights with a new conversation."
    python:
        _phone_messages = [
            phone_msg("them", "Matsuda: By unanimous and legally sound agreement, tomorrow's order is bookstore, arcade, food."),
            phone_msg("them", "Tsubaki: The agreement was not unanimous. I asked to put the bookstore first."),
            phone_msg("them", "Matsuda: A motion unopposed becomes destiny."),
            phone_msg("them", "Asahina: i'll meet you at the arcade whenever volleyball releases me"),
            phone_msg("me", "Same for track. Don't hold the bookstore for me."),
            phone_msg("them", "Tsubaki: Works for me."),
            phone_msg("them", "Matsuda: Then it is written."),
            phone_msg("me", "You named this chat Saturday. I'm proud of you."),
            phone_msg("them", "Matsuda: The first six names were vetoed by a hostile committee."),
            phone_msg("them", "Tsubaki: They had the word fellowship in them."),
            phone_msg("them", "Asahina: i would have left instantly"),
            phone_msg("them", "Matsuda: Philistines, all of you."),
        ]
    call phone_text_conversation("Saturday", _phone_messages, status="3 participants", append=True) from _call_phone_text_conversation_0530_1
    "The thread goes quiet after that. The only open question is whether food means ramen or burgers, and nobody has the energy to argue it tonight."
    "I put the arcade card in my wallet."
    "Another message arrives before the phone reaches the desk."
    python:
        _phone_messages = [
            phone_msg("them", "You left before I could remind you about your final line."),
            phone_msg("me", "You assigned it. That was the reminder."),
            phone_msg("them", "Good. I expect to learn whether the traveler goes inside on Monday."),
            phone_msg("me", "Aggressive investment in fictional transit."),
            phone_msg("them", "Occupational hazard~"),
            phone_msg("them", "Have fun tomorrow, " + player + "."),
            phone_msg("me", "Thanks. Night, Monika."),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0530_2
    "I set the phone beside the wallet and look at the unfinished draft sticking out of my school bag."
    "The traveler has all weekend to decide whether to go inside."
    "I have classes, track, and an arcade before any fictional person gets an answer out of me."
    "That seems like a fair order of operations."
    "I set the usual Saturday alarm and turn off the desk lamp."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Friday ends. Nobody assigns the weekend a purpose."
    nier "Tomorrow still contains school. After that comes track, then an arcade if Coach and my left foot both cooperate."
    nier "Tsubaki gets her bookstore first. Asahina joins when volleyball releases her. Matsuda has been forbidden from naming the group anything involving fellowship."
    nier "May gets one more day. For now, that is plenty."
    call nier_clear from _call_nier_clear_0530_7
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0530_1
    jump a0531
