label a0529:
    # --- Day 15: 2025-05-29 ---
    # First day after exams (exams ran 0526-0528). Decompression contrasts exam-week tension.
    # Matsuda ramp-up BEGINS here and continues 0530, 0531 toward Chapter 1.
    # Threads seeded for payoff: she "does slow" as she promised on 0523 -- but the slowness is
    # studied, an acting gap; she's begun quietly mapping MC's afternoons; she rebuilt the outing
    # MC told her not to plan (0523) so the new version survives his "no"; the "holding the door,
    # not pushing" claim on MC's time. Ledger meters moved: Matsuda's claim, Asahina/food + Sam-as-
    # infrastructure, Mom's contract-read on both kids, track invitational ahead.
    scene bg kitchen
    $ show_calendar()
    show mood_home zorder 3
    with dissolve_scene_full
    play music dailyleisure
    window auto
    "Thursday morning behaves like a body that forgot it was allowed to."
    "I wake before the first alarm and lie there for a second waiting for the dread to arrive on schedule."
    "It doesn't."
    "There is no exam today. No paper face-down on a desk. No subject lying in wait with a single missing minus sign."
    "{i}Just school. Regular, unweaponized school.{/i}"
    "The realization is almost suspicious, like the week left the door open on its way out and I keep expecting it to come back for something."
    show mom neut at t22
    show asahina neut at t21
    "Downstairs, the kitchen has settled back into a shape I recognize from before midterms ate it."
    "Mom is dressed for work and reading something on her tablet. Asahina is hunched over toast with the specific slump of a person whose brain has been given permission to stop and took it too literally."
    mom "Morning."
    mc "Morning."
    ah "Mngh."
    mc "Eloquent."
    ah "It's the only word I prepared for today."
    "She bites the toast like it personally survived the week with her."
    mom "Midterm results won't post until Monday, June 2, in case either of you was planning to refresh a portal into an early grave."
    ah "I wasn't."
    mc "She was."
    ah "I was {i}going{/i} to. There's a difference."
    "Mom turns a page without looking up."
    mom "There is. One of them is healthier, and you've both historically picked the other one."
    "She says it lightly, but her eyes flick up once -- the same quick read she gives a contract before deciding whether to trust the part that sounds fine."
    "It lands on me a half-second longer than it lands on Asahina."
    "{i}She's still watching the part of the last few days I wish she hadn't seen.{/i}"
    "I let it pass and reach for the rice."
    mom "Track today?"
    mc "Coach said he'd reassess after exams. So probably yelling, then running, then more yelling."
    mom "A balanced program."
    mc "He's very holistic."
    "Asahina snorts into her toast, which I count as the day's first genuine win."
    "Mom stands, gathers her bag, and pauses at the counter to slide a banana into the side pocket of mine without comment."
    "I notice. I decide not to make it a thing."
    mom "Eat lunch. Both of you. An actual one."
    ah "I always eat lunch."
    mom "You always {i}bring{/i} lunch. The eating is where the data gets unreliable."
    "Asahina opens her mouth, finds no defense, and closes it."
    "{i}Filed. Quietly.{/i}"
    show mom at thide
    hide mom
    show asahina at thide
    hide asahina
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Mom leaves first, with an actual goodbye and a short list of things she expects to still be true when she gets home."
    nier "Asahina and I make it out the door without incident, which after the last few days feels like an accomplishment worth not mentioning out loud."
    nier "The walk to school is loud with a school that remembers it is allowed to be loud again."
    call nier_clear from _call_nier_clear_0529_1
    stop music fadeout 1.0
    scene bg class_day
    $ show_calendar()
    show mood_afternoon zorder 3
    with dissolve_scene_full
    play music schooldays
    "Classes the day after exams are a special kind of theater."
    "Teachers know nobody is going to absorb anything, and most of them have made an uneasy peace with it."
    "Civics becomes a documentary nobody fully watches. Language arts becomes the teacher reading aloud while the room pretends its eyes are open. The math teacher, to his eternal credit, puts a single review problem on the board and tells us to leave him alone with his coffee."
    "{i}I respect a man who knows when the building has nothing left to give.{/i}"
    "The mood in the halls is the inverse of Monday: loose, careless, the exam already turning into a story people tell instead of a thing that happened to them."
    "Someone two desks over is reenacting their meltdown during the biology section with theatrical hand gestures and a captive audience."
    "I half-listen and let the morning be small."
    "For the first time in a week, I don't have a single thing I'm supposed to be afraid of by the next bell."
    "{i}It's almost disorienting. Like setting down a bag you carried so long your shoulder kept the shape.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Lunch arrives without a study packet attached to it for the first time in what feels like a geological age."
    nier "No roof invitation, no library plan, no exam to cram against. The hour is simply mine, which is rare enough that I almost don't know where to spend it."
    nier "I settle on the courtyard side of the corridor, where the windows are open and the noise has somewhere to go."
    call nier_clear from _call_nier_clear_0529_2
    scene bg corridor
    $ show_calendar()
    show mood_afternoon zorder 3
    stop music fadeout 1.0
    with wipeleft_scene
    play music daily
    "The corridor has the warm, scattered energy of a school let off a leash."
    "I find a spot near the windows and unwrap my lunch with the leisure of a person who has nowhere to be."
    "My phone buzzes once."
    "Monika."
    python:
        _phone_messages = [
            phone_msg("them", "Survived day one of being a normal student again?"),
            phone_msg("me", "Barely. The lack of impending doom is hard on the nervous system."),
            phone_msg("them", "Give it a day. Club's back to real hours tomorrow, by the way. Actual writing, no bans."),
            phone_msg("me", "You banned studying. You can't un-ban the ban now."),
            phone_msg("them", "Watch me. I contain multitudes and at least two clipboards."),
            phone_msg("me", "Terrifying. See you tomorrow."),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0529_1
    "I'm halfway through a second bite when my phone buzzes again, from a different name."
    "Matsuda Akai."
    "{i}There she is.{/i}"
    "{i}Radio silence for the entire exam week, and now, the exact day the pressure lifts, the signal comes back.{/i}"
    python:
        _phone_messages = [
            phone_msg("them", "Greetings, survivor."),
            phone_msg("them", "I trust the gauntlet did not consume you whole."),
            phone_msg("me", "Still assembled. Mostly."),
            phone_msg("them", "Good. I am exercising restraint by not asking how it went, because you said to slow down, and I am a woman of my word."),
            phone_msg("them", "Note the restraint. It is happening. In real time. At great personal cost."),
            phone_msg("me", "Noted."),
            phone_msg("them", "Are you on campus presently?"),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, status="New Contact", append=True) from _call_phone_text_conversation_0529_2
    "I look at the question for a second."
    "It's a normal question. People ask it. It means nothing."
    "{i}So why does it feel like a piece on a board getting moved?{/i}"
    "I'm still deciding how to answer when the answer arrives the old-fashioned way."
    "Footsteps with intent. A flash of red at the far end of the corridor, moving against the current like she has somewhere louder to be."
    play music enterm
    show matsuda neut at t11
    "Matsuda lands at my window like she chose the spot before I did -- which, given the timing of that text, she probably did."
    ma "Aha. The phone says no answer, but the corridor says yes."
    mc "You asked where I was, then walked straight to me. That's not asking, that's confirming."
    ma "Diligence, comrade. I refuse to stage my entrances on bad intelligence."
    "She drops onto the windowsill beside me with a flourish the windowsill did not consent to."
    "She has a melon bread in one hand and nothing resembling a real lunch in the other."
    "{i}Tsubaki would have opinions.{/i}"
    mc "Where's your shadow?"
    ma "Kareda? Her class rotated to a different lunch block this week. Tragic. The conscience is unavailable, so I am operating on raw instinct."
    mc "That explains the melon bread."
    ma "The melon bread is a {i}choice{/i}, not a symptom."
    "She tears off a piece anyway and eats it like a queen sampling tribute."
    "And then -- this is the strange part -- she doesn't launch into anything."
    "No grand pronouncement. No Azure Eye prophecy. No declaration about fate finishing its sentence."
    "She just sits there, eating, watching the courtyard with me, like sitting is a thing she does."
    "{i}Huh.{/i}"
    "{i}She's actually doing the slow thing.{/i}"
    "The quiet stretches long enough to become noticeable, which is when I clock the other thing -- she keeps almost saying something and stopping, the way a person does when they've rehearsed an opening and are waiting for the natural place to put it."
    ma "You usually eat on the roof."
    "It comes out light, an observation dropped sideways."
    mc "Sometimes. When Asahina drags me up there."
    ma "Tuesdays and Thursdays, generally. Or you take the corridor windows when she has volleyball-adjacent business and you want noise without company."
    "I stop chewing."
    mc "...That's oddly specific."
    "For half a second something crosses her face -- a small recalculation, the look of someone who just played a card face-up by accident."
    "Then the performance folds back over it, smooth as a curtain dropping."
    ma "I am observant under pressure. We established this at the scene of our inciting collision."
    mc "We collided once, eleven days ago. That's not a pattern, that's an anecdote."
    ma "Everything is an anecdote until it happens twice. Then it's a story."
    "She says it like a joke. It mostly is a joke."
    "It's the part that isn't that stays with me."
    "{i}She knows my lunch schedule. By weekday. With exceptions.{/i}"
    "{i}I have known this girl for less than two weeks.{/i}"
    "I file it where I file the things I don't want to be weird about yet, and I tell myself it's just Matsuda being Matsuda, because that's the explanation that lets me keep eating."
    mc "You're being weirdly calm today."
    ma "I am pacing myself. You requested pace. I am giving you the artisanal, hand-poured version of me."
    mc "It's unsettling."
    ma "Growth often is."
    "She finishes the melon bread, balls up the wrapper with theatrical precision, and lobs it into the bin across the hall in one clean arc."
    "It goes in. She doesn't look to check. She already knew it would."
    "{i}Of course she did.{/i}"
    ma "Anyhow. I shan't monopolize your hard-won leisure. I only wished to confirm you survived the trial, and to plant one small seed for later."
    mc "I'm not signing anything."
    ma "No signatures. A proposal, lightly. The week wronged all of us. I am assembling a modest expedition once the dust settles -- Kareda, possibly your sister if she deigns, you, me. Nothing immediate. Nothing this instant."
    "She holds up both gloved hands, palms out, the way you gentle a spooked animal."
    ma "I am specifically not naming a day. I learned that lesson. See? The day stays blank, for you to fill, like a responsible adult with a calendar."
    "And there it is."
    "The same Sunday-shaped invitation she tried to launch last Friday -- the one I told her not to plan and not to call an emerging circle."
    "Except now it's wearing my own feedback as a costume."
    "{i}She didn't drop the plan. She rebuilt it to survive my objection.{/i}"
    "It's almost impressive. It would be entirely impressive if it didn't feel like watching someone reverse-engineer the lock on a door I'd already closed."
    mc "I'll think about it."
    ma "That is all I ask. Thinking is free, and I have priced it accordingly."
    "She stands, dusts crumbs that aren't there off an immaculate skirt, and gives me a small, unnecessary bow."
    ma "Rest your beleaguered student soul, [player]. The eclipse will keep."
    mc "There's still no eclipse."
    ma "There is always an eclipse somewhere. The Azure Eye does not deal in your local timezone."
    show matsuda at thide
    hide matsuda
    stop music fadeout 1.0
    "She sweeps off down the corridor, against traffic again, leaving the windowsill colder than she found it."
    "I sit with my half-finished lunch and the distinct sense of having been measured."
    "{i}She left the day blank. She wants me to feel like I'm holding the pen.{/i}"
    "{i}She also knows exactly which days I'm on the roof.{/i}"
    "My phone buzzes one more time before I can decide whether to be bothered by any of it."
    python:
        _phone_messages = [
            phone_msg("them", "I waited five whole days to text you. That is a personal record and nobody clapped."),
            phone_msg("me", "I'm clapping internally."),
            phone_msg("them", "I will accept internal applause as a down payment."),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, status="New Contact", append=True) from _call_phone_text_conversation_0529_3
    "{i}Five days. She counted.{/i}"
    "{i}Who even keeps a receipt like that???{/i}"
    $ update_character_thought("matsuda", "Matsuda 'did slow' the whole exam week, then surfaced the day pressure lifted -- and she knows my lunch schedule by weekday. She rebuilt the outing I told her not to plan so the new version survives my no.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The afternoon classes finish the job of being harmless."
    nier "Nobody assigns anything real. The teachers seem as relieved as we are to coast one day before the machine starts demanding things again."
    nier "By the final bell, the only commitment I have left is the one that involves a whistle and my own bad decisions about pace."
    call nier_clear from _call_nier_clear_0529_3
    stop music fadeout 1.0
    scene bg track_day
    $ show_calendar()
    show mood_afternoon zorder 3
    with dissolve_scene_full
    play music daily
    "The track has that late-spring warmth that makes the rubber feel almost generous."
    "The distance group is already loitering near the infield in the loose, doomed way runners loiter before agreeing to suffer."
    "Coach is by the lane line, clipboard against his hip, watching me arrive with the patience of a man who knows exactly how an honor student behaves the week after exams."
    show track_coach neut at t11
    track_coach "Exams done?"
    mc "Done."
    track_coach "Brain intact?"
    mc "Pending external review."
    track_coach "Good enough."
    "He flips a page he doesn't read."
    track_coach "Here's the reassessment I promised. Invitational's two weekends out. You're not fit enough to be a hero and too stubborn to be careful, so we split the difference."
    mc "That sounds like a threat shaped like a plan."
    track_coach "It's a plan shaped like me not wanting to scrape you off the back straight."
    track_coach "Twenty-five minutes easy. Conversational. If you can't talk while you run it, you're running it wrong."
    mc "And the foot?"
    track_coach "If it talks, you stop. It gets the only veto on this field today."
    show track_coach at thide
    hide track_coach
    "I take the outside lane and let the first lap be slow on purpose this time, which is its own small victory."
    "Last week the running was something I did between fears. Today there's nothing waiting at the end of it, so the laps get to just be laps."
    "The foot stays quiet. My shoulders try to creep up around lap four out of pure habit, and I talk them back down before Coach has to."
    "{i}Relax the hands. Let the pace stay boring. Continuing is the plan.{/i}"
    "Somewhere around the eighteenth minute my brain wanders, the way it only does when it's finally allowed to."
    "It wanders, predictably, to a red-haired girl who knows I run distance and apparently also knows which days I eat lunch on the roof."
    "{i}She slowed down because I asked. She remembered the schedule because she wanted to. Both of those are true at once, and only one of them is reassuring.{/i}"
    "I lose the thread on the next curve and let it go. Coach is right that the legs hear it when the head stops arguing."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Practice ends clean, which is the highest compliment I can pay a Thursday."
    nier "Coach tells me to hydrate three times and mentions the foot zero times, which between the two of them is the report card I actually wanted."
    nier "I walk home the long way, because for the first time in a week the long way doesn't cost me anything I can't afford."
    call nier_clear from _call_nier_clear_0529_4
    scene bg residential_day
    $ show_calendar()
    show mood_evening zorder 3
    stop music fadeout 1.0
    with wipeleft_scene
    play music schooldays
    "The neighborhood is doing its early-evening thing: long light, a dog being walked by a kid who is mostly being walked by the dog, the distant clatter of someone starting dinner with a window open."
    "I take it slow. My legs have earned slow."
    "The text thread with Matsuda sits in my pocket like a small warm stone, and I keep almost taking it out to reread it, which is exactly the impulse I don't want to examine."
    "Instead I think about the shape of the day she didn't name."
    "{i}Kareda, possibly your sister if she deigns, you, me.{/i}"
    "{i}She built the group in a single sentence. She put me in the middle of it. She left one variable open and called it my decision.{/i}"
    "It's the kind of thing that would be flattering if I hadn't watched her run the exact same move once already and get told no for it."
    "A person who hears no and stops is one thing."
    "A person who hears no and redesigns the request so the next version is harder to refuse is something I don't have a clean word for yet."
    "{i}Asahina said it the night I met her. Loud people find you, and you just let them.{/i}"
    "{i}I told her I wasn't going to respond to that. I'm still not. But I notice it sitting there.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I get home with the light still hanging on and the street still warm, and the house meets me with the ordinary noises it makes when nobody is in crisis."
    nier "After a week of the building feeling like a courtroom, ordinary is almost loud."
    call nier_clear from _call_nier_clear_0529_5
    scene bg kitchen
    $ show_calendar()
    show mood_home zorder 3
    stop music fadeout 1.0
    with wipeleft_scene
    play music dailyleisure
    play sound moddooropen
    "Home smells like something with ginger in it and the specific steam of rice that finished a minute ago."
    "Asahina is at the table with her phone propped against the soy sauce, half-watching something and half-typing. Mom is at the stove, sleeves pushed up, doing the thing where she cooks and reads a work email on the counter at the same time and pretends both have her full attention."
    show mom neut at t22
    show asahina neut at t21
    mom "Shoes, hands, bag. Then you may approach the rice."
    mc "The rice has a security checkpoint now."
    mom "The rice has standards."
    ah "Mom made the good ginger thing."
    mc "I can smell the good ginger thing."
    ah "It's the good one, not the lazy one."
    mom "They are the same recipe."
    ah "They are {i}not{/i}, and you know it."
    "Mom doesn't dignify that, which in this house counts as a confession."
    "I wash up and sit. Dinner assembles itself out of bowls and the low, normal argument over who gets the last of the pickles."
    "Nobody mentions grades. Nobody mentions answer keys, or the office, or any of the words that lived in this kitchen during exams."
    "The conversation finds smaller work, and lets itself stay small."
    ah "Sam said the senior portal stays locked until Monday too."
    "She says it like a normal fact, eyes on her food."
    mom "Then nobody has anything useful to refresh tonight."
    ah "He still offered to help me study for next time. Like, set up a whole schedule and stuff."
    "Mom's spoon doesn't pause, exactly. It just slows by a fraction on its way to the bowl."
    mom "That's thoughtful."
    mom "You've got your brother and me for studying, though. You don't have to outsource it."
    ah "I know. It's just nice that he thinks about it."
    "She says {i}thinks about it{/i} the way someone repeats a phrase they've been handed."
    "{i}He remembers what she's trying to do better than she does. He builds it into a schedule. He makes the caring look like infrastructure.{/i}"
    "{i}It's a nice thing. It keeps being a nice thing right up until I try to name what's nice about it and can't.{/i}"
    mc "Did you actually eat lunch today?"
    "Asahina looks up, betrayed."
    ah "Why is that the second time someone's asked me that today?"
    mc "Because you do the thing where you bring it and then donate it to the inside of your bag."
    ah "I ate {i}most{/i} of it."
    mom "Most."
    ah "Most is a passing grade in some subjects."
    mom "Not in mine."
    "It's a joke. The table laughs. But Mom's eyes do the quick read again, the contract read, and this time they land on Asahina and stay a half-second too long."
    "{i}She's watching both of us. Different things, same look.{/i}"
    "I let the moment move on, because making it heavier wouldn't help, and because I'm honestly not sure I'm right about what I just saw."
    "{i}Filing it anyway. The list is getting long this week.{/i}"
    show mom at thide
    hide mom
    show asahina at thide
    hide asahina
    $ update_character_thought("asahina", "Asahina repeated Sam's offer to 'set up a whole schedule' for her studying like a line she'd been handed. The caring keeps arriving as infrastructure, and I keep not having a word for why that bothers me.")
    $ update_character_thought("mom", "Mom pinned midterm results to Monday, June 2, but she's reading both of us like contracts this week. At dinner the read landed on Asahina too, not just me.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Dinner ends without becoming an event, which is the whole point of a good one."
    nier "I do dishes. Asahina dries exactly four things and declares the labor union satisfied. Mom takes one more call at the table, low and clipped, then sets the phone face-down like she's deciding by force that the day is over."
    nier "The house holds together in small pieces. After the last few days, the smallness is the luxury."
    call nier_clear from _call_nier_clear_0529_6
    stop music fadeout 1.0
    scene bg bedroom
    $ show_calendar()
    show mood_night zorder 3
    with wipeleft_scene
    play music fantasypassion
    "My room at night, with no exam tomorrow, is a strange and underused environment."
    "The desk is just a desk again. The review sheets have migrated into a folder I shoved out of sight, and the calculator has gone back to being a paperweight with delusions."
    "For the first time in a week I could play that game until the city under the false sky bores me, and nothing would punish me for it in the morning."
    "I turn on the console and get exactly twenty minutes into a dungeon before my phone lights up the desk."
    "Matsuda Akai."
    "{i}Of course.{/i}"
    python:
        _phone_messages = [
            phone_msg("them", "A question, soberly posed and free of theatrics:"),
            phone_msg("them", "When you picture the not-yet-scheduled expedition, does the idea sit well, or does it sit like a coat that is technically your size?"),
            phone_msg("me", "That's a weirdly specific way to ask if I want to hang out."),
            phone_msg("them", "I am calibrating. You told me to slow down and ask normally. This is me attempting both at a level I find physically uncomfortable."),
            phone_msg("me", "It sits fine. I just don't want it scheduled around me before I've agreed to it."),
            phone_msg("them", "Understood. Nothing is scheduled. The day stays blank. I am holding the door, not pushing you through it."),
            phone_msg("them", "Goodnight, " + player + "."),
            phone_msg("me", "Night."),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, append=True) from _call_phone_text_conversation_0529_4
    "I set the phone face-down."
    "Then I pick it up and reread it, which is becoming a habit I should probably start charging myself rent for."
    "On its own, the exchange is fine. She asked. She listened. She backed off. That's the version of Matsuda I told her I wanted, and she delivered it almost to the letter."
    "{i}Almost.{/i}"
    "{i}Holding the door, not pushing you through it.{/i}"
    "It's a good line. It's the exact line a person reaches for once they've worked out that pushing doesn't move me and standing in an open doorway does."
    "I don't think she's lying. That's the part I keep circling. I think every word of it is true, and I still can't shake the sense of a hand resting very lightly on my afternoons -- not gripping, just resting, the way you rest a hand on something you've decided is yours and are willing to be patient about."
    "{i}Two weeks ago a girl crashed into me on a sidewalk and called it an inciting incident.{/i}"
    "{i}She wasn't wrong. I just didn't know yet that she meant it as a structure and not a joke.{/i}"
    "I think about Monika's club room, where the rule on the board was {i}NO STUDYING{/i} and the entire point of the afternoon was to let the week stop."
    "Monika wanted my time, risked asking for it, and let me say no without consequence."
    "Matsuda wants my time too. The difference is in what happens to the request after the no."
    "{i}I don't have a word for that difference yet.{/i}"
    "{i}I have a feeling I'm going to.{/i}"
    "I turn the game back on, because the city under the false sky is at least a problem with a save point."
    "The party reaches a checkpoint. A horned bureaucrat asks me to state my alignment preference, and for once the question feels less abstract than it did on Saturday."
    mc "...Still tired. Still neutral."
    "The game accepts it, takes its processing fee, and lets me through."
    "{i}If only people were that upfront about the toll.{/i}"
    $ update_character_thought("matsuda", "Matsuda asked, listened, and backed off -- exactly what I asked for on 0523. She also kept the outing alive by 'leaving the day blank.' She's not pushing. She's holding the door, which works on me better than pushing would, and I think she knows it.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Thursday ends the way the day after a hard week is supposed to: quietly, with nothing demanded."
    nier "The exams are behind me. The grades are somewhere ahead, unhurried. Track has a shape again. The club reopens tomorrow."
    nier "And a new name has started arriving at the exact moments the pressure lets go -- patient, well-mannered, holding a door I never asked anyone to hold."
    nier "I sleep before the game can talk me out of it. Tomorrow can sort the rest."
    call nier_clear from _call_nier_clear_0529_7
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0529_1
    jump a0530
