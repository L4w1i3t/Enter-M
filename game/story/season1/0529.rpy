label a0529:
    # --- Day 15: 2025-05-29 ---
    # First day after exams (exams ran 0526-0528). Decompression contrasts exam-week tension.
    # Matsuda's post-exam ramp begins here and continues through 0530-0531 toward Chapter 1.
    # The increase should read as ordinary social momentum on a first playthrough: she makes a
    # visible effort to honor MC's request for a slower pace, casually mentions an existing plan
    # with Tsubaki, and leaves the actual invitation for later. The underlying pattern belongs to
    # hindsight, not MC's present-tense suspicion. Other meters moved: Asahina/food + Sam's
    # schedule-as-care wrong note, Mom's contract-read on both kids, track invitational ahead.
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music dailyleisure
    window auto
    "Something is missing this morning, and it takes me until the bottom of the stairs to work out what."
    "I've been waiting for the dread to clock in on schedule."
    "It doesn't."
    "{i}Just school, regular and unweaponized.{/i}"
    show mom uniform neut at t22
    show asahina uniform unamused at t21
    "The morning looks the way it did before midterms ate it."
    "Mom is dressed for work and reading something on her tablet. Asahina is hunched over toast. Her brain was given permission to stop and appears to have taken it literally."
    mom "Morning."
    mc "Morning."
    ah "Mngh."
    mc "Eloquent."
    ah "It's the only word I prepared for today."
    "She bites the toast like it personally survived the week with her."
    show mom uniform teasing
    mom "Midterm results won't post until Monday, June 2, in case either of you was planning to refresh a portal into an early grave."
    show asahina uniform annoyed
    ah "I wasn't."
    mc "She was."
    ah "I was {i}going{/i} to. There's a difference."
    "Mom turns a page without looking up."
    show mom uniform thinking
    mom "There is. One of them is healthier, and you've both historically picked the other one."
    "She says it lightly, but her eyes flick up once -- the same quick read she gives a contract before deciding whether to trust the part that sounds fine."
    "Her thumb pauses on the tablet. The glance checks Asahina's toast, my hands, the bag beside my chair."
    "{i}Still on the record, then.{/i}"
    "I let it pass and reach for the rice."
    show mom uniform curious
    mom "Track today?"
    mc "Coach said he'd reassess after exams. So probably yelling, then running, then more yelling."
    show mom uniform smug
    mom "A balanced program."
    mc "He's very holistic."
    show asahina uniform happy
    "Asahina snorts into her toast, which I count as the day's first genuine win."
    "Mom stands and gathers her bag. On her way past she slides a banana into the side pocket of mine without comment."
    "I notice. I decide not to make it a thing."
    show mom uniform determined
    mom "Eat lunch. Both of you. An actual one."
    show asahina uniform neut
    ah "I always eat lunch."
    show mom uniform neut
    mom "You always {i}bring{/i} lunch. The eating is where the data gets unreliable."
    "Asahina opens her mouth. Nothing defensible arrives, so she closes it."
    "{i}Filed quietly.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Mom leaves first, with an actual goodbye and a short list of things she expects to still be true when she gets home."
    nier "Asahina and I make it out the door without incident, which after the last few days feels like an accomplishment worth not mentioning out loud."
    nier "The walk to school is loud with a school that remembers it is allowed to be loud again."
    call nier_clear from _call_nier_clear_0529_1
    stop music fadeout 1.0
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    with dissolve_scene_full
    play music schooldays
    "Classes the day after exams are their own special theater."
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
    nier "Nobody brings a study packet to lunch, which has not happened in what feels like a geological age."
    nier "No roof invitation, no library plan, no exam to cram against. The hour is simply mine, which is rare enough that I almost don't know where to spend it."
    nier "I settle on the courtyard side of the corridor, where the windows are open and the noise has somewhere to go."
    call nier_clear from _call_nier_clear_0529_2
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    stop music fadeout 1.0
    with wipeleft_scene
    play music daily
    "The corridor has the warm, scattered energy of a school let off a leash."
    "I find a spot near the windows and unwrap my lunch slowly, because for once nothing is waiting."
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
    python:
        _phone_messages = [
            phone_msg("them", "Greetings, survivor."),
            phone_msg("them", "I trust the gauntlet did not consume you whole."),
            phone_msg("me", "Still assembled. Mostly."),
            phone_msg("them", "Good. I'm exercising restraint by not asking how it went, because you said to slow down, and I am a woman of my word."),
            phone_msg("them", "Note the restraint. It is happening. In real time. At great personal cost."),
            phone_msg("me", "Noted."),
            phone_msg("them", "Are you on campus presently?"),
            phone_msg("me", "Corridor windows. Why?"),
            phone_msg("them", "No reason of consequence."),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, status="New Contact", append=True) from _call_phone_text_conversation_0529_2
    stop music fadeout 1.0
    # SFX SUGGESTION: Fast, purposeful footsteps approaching along the corridor tile.
    "Footsteps with intent arrive from the far end of the corridor less than a minute later."
    show matsuda uniform smug at t11
    "Matsuda appears wearing the pleased expression of someone whose no-reason has produced immediate results."
    play music enterm
    ma "Aha. The phone and corridor agree. Civilization endures."
    mc "So the reason was that you were already nearby."
    show matsuda teasing
    ma "A trifling omission made in service of the reveal."
    "She drops onto the windowsill beside me with a flourish the windowsill did not consent to."
    "She has a melon bread in one hand and nothing resembling a real lunch in the other."
    mc "Where's your conscience?"
    show matsuda happy
    ma "Kareda's class rotated lunch blocks. I am operating unsupervised and at tremendous personal risk."
    mc "That explains the melon bread."
    show matsuda unamused
    ma "The melon bread is a choice, not a cry for help."
    show matsuda neut
    "She tears off a piece, eats it, and then makes a visible effort not to fill the corridor with herself."
    "For a little while, we watch the courtyard and let everyone else provide the noise."
    mc "You're being weirdly calm today."
    ma "I'm pacing myself. You requested pace. I'm giving you the artisanal, hand-poured version of me."
    mc "It looks painful."
    show matsuda unamused
    ma "Growth often is."
    "She lasts another three bites before the effort starts leaking."
    show matsuda thinking
    ma "Kareda and I may investigate a used-book clearance once the academic smoke clears. There is also an arcade nearby, allegedly stocked with machines designed to steal dignity and coins in equal measure."
    mc "That sounds more like your natural habitat."
    ma "I thrive wherever the lighting is hostile and victory produces tickets."
    show matsuda curious
    ma "We might invite you and Asahina if the plan survives contact with Kareda's common sense."
    mc "You just floated an idea without planning my weekend for me."
    show matsuda teasing
    "Matsuda points the last piece of melon bread at me."
    ma "Do not announce it. I have a reputation to mismanage."
    # SFX SUGGESTION: A paper-wrapper swish ending in a light hollow bin impact.
    "She balls up the wrapper and lobs it into the bin across the hall. It drops cleanly through."
    mc "Okay, that was decent."
    show matsuda happy
    ma "A witness! My legend grows."
    show matsuda annoyed
    "The volume comes back for one sentence. She notices, winces, and pulls it down again."
    show matsuda neut
    ma "Anyhow. I only wanted to confirm you survived and mention the possibility before I forgot how to be reasonable."
    mc "Mission accomplished. Disturbingly."
    show matsuda happy
    "She gives me a small bow on the way up and heads back into corridor traffic."
    show matsuda at thide
    hide matsuda
    stop music fadeout 1.0
    "I finish lunch. The bookstore idea sounds decent; the arcade sounds better."
    "My phone buzzes once more."
    python:
        _phone_messages = [
            phone_msg("them", "That counted as normal, yes?"),
            phone_msg("me", "Normal-adjacent."),
            phone_msg("them", "A passing mark. Splendid."),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, status="New Contact", append=True) from _call_phone_text_conversation_0529_3
    $ update_character_thought("matsuda", "Matsuda made a visible effort to keep lunch low-key. She and Tsubaki may invite Asahina and me to a bookstore and arcade once they settle the plan.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The afternoon classes finish the job of being harmless."
    nier "Nobody assigns anything real. The teachers seem as relieved as we are to coast one day before the machine starts demanding things again."
    nier "By the final bell, the only commitment I have left is the one that involves a whistle and my own bad decisions about pace."
    call nier_clear from _call_nier_clear_0529_3
    stop music fadeout 1.0
    pause 2.0
    scene bg track_day
    $ show_calendar()
    $ atmos("afternoon")
    with dissolve_scene_full
    play music daily
    "The track has that late-spring warmth that makes the rubber feel almost generous."
    "The distance group is already loitering near the infield in the loose, doomed way runners loiter before agreeing to suffer."
    "Coach is by the lane line, clipboard against his hip, watching me arrive. He knows exactly how an honor student behaves the week after exams, and he is patient about it."
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
    "I take the outside lane and let the first lap be slow on purpose this time. Small victory."
    "Last week the running was something I did between fears. Today there's nothing waiting at the end of it, so the laps get to just be laps."
    "The foot stays quiet. My shoulders try to creep up around lap four out of pure habit, and I talk them back down before Coach has to."
    "{i}Relax the hands. Let the pace stay boring. Continuing is the plan.{/i}"
    "Somewhere around the eighteenth minute my brain finally stops inventorying exams, grades, and every small ache below the knee."
    "The quiet lasts through the next curve. I let it. Coach is right that the legs hear it when the head stops arguing."
    "His whistle cuts across the track at twenty-five minutes."
    "I finish the curve before easing down, partly because stopping on a bend feels wrong and partly because my legs have remembered how to resent an interruption."
    show track_coach neut at t11
    track_coach "Walk it out."
    "I walk the outside lane while he watches the first few steps."
    track_coach "Foot?"
    mc "Quiet."
    track_coach "Anything pulling?"
    mc "Calves know they exist. Nothing specific."
    track_coach "Good."
    "He makes one mark on the clipboard, then another beside it."
    mc "Are either of those flattering?"
    track_coach "One says you finished without limping. The other says you asked whether the first mark was flattering."
    mc "So mixed review."
    track_coach "Invitational entries go in next week."
    "He says it while looking at the page, which makes the sentence sound administrative until it reaches me."
    mc "What are you thinking?"
    track_coach "Sixteen if the foot stays quiet. Thirty-two if tomorrow's form work is clean and you stop treating easy days like moral failures."
    mc "Both?"
    track_coach "Maybe."
    "Maybe has enough room inside it for confidence to start making poor decisions."
    track_coach "Do not make that face."
    mc "What face?"
    track_coach "The one where you hear maybe and start spending it like yes."
    "I look toward the back straight. The distance group is finishing strides in loose pairs, shoes tapping through the same strip of sun."
    mc "I can handle both."
    track_coach "That was not the question."
    mc "What was the question?"
    track_coach "There wasn't one. That's why your answer concerns me."
    "He finally lowers the clipboard."
    track_coach "Tomorrow after classes: drills, short strides, then you leave. Sunday is easy mileage on your own. If either day becomes a secret test of character, you fail it."
    mc "Very inspiring."
    track_coach "Inspiration is how half this team gets shin splints. I prefer instructions."
    "He points toward the infield with his pen."
    track_coach "Your fitness did not disappear during exams. You do not need to win it back in forty-eight hours."
    "The sentence is obvious enough that I should not need it."
    "I do."
    mc "Drills, short strides, leave. Easy Sunday."
    track_coach "There. Your listening comprehension survived too."
    mc "Pending external review."
    track_coach "Hydrate before the review board meets."
    show track_coach at thide
    hide track_coach
    "I collect my bottle and walk another lap."
    "The temptation to turn it into a jog lasts less than a hundred meters, which I choose to count as maturity rather than fatigue."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Practice ends clean, which is the highest compliment I can pay a Thursday."
    nier "Coach tells me to hydrate three times and mentions the foot zero times, which between the two of them is the report card I actually wanted."
    nier "I walk home the long way, because this week the long way finally doesn't cost me anything I can't afford."
    call nier_clear from _call_nier_clear_0529_4
    pause 2.0
    scene bg residential_day
    $ show_calendar()
    $ atmos("evening")
    stop music fadeout 1.0
    with wipeleft_scene
    play music schooldays
    "The neighborhood is doing its early-evening thing: long light, a dog being walked by a kid who is mostly being walked by the dog, the distant clatter of someone starting dinner with a window open."
    "I take it slow. My legs have earned slow."
    "My legs are pleasantly tired, the sort of tired with an obvious cause and a straightforward solution."
    "I pass the turn for home and circle one extra block. That counts as enjoying the weather rather than ignoring Coach's instructions."
    "The distinction is generous but survivable."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I get home with the light still hanging on and the street still warm, and the house meets me with the ordinary noises it makes when nobody is in crisis."
    nier "After a week of the building feeling like a courtroom, ordinary is almost loud."
    call nier_clear from _call_nier_clear_0529_5
    pause 2.0
    scene bg dining_table_night
    $ show_calendar()
    $ atmos("home_night")
    stop music fadeout 1.0
    with wipeleft_scene
    play music dailyleisure
    play sound moddooropen
    "Home smells like something with ginger in it and rice that finished a minute ago."
    "Asahina is at the table with her phone propped against the soy sauce, half-watching something and half-typing. Mom is still in the kitchen, sleeves pushed up, doing the thing where she cooks and reads a work email at the same time and pretends both have her full attention."
    show mom teasing at t22
    show asahina happy at t21
    mom "Shoes, hands, bag. Then you may approach the rice."
    mc "The rice has a security checkpoint now."
    show mom smug
    mom "The rice has standards."
    ah "Mom made the good ginger thing."
    mc "I can smell the good ginger thing."
    ah "It's the good one, not the lazy one."
    show mom unamused
    mom "They are the same recipe."
    show asahina determined
    ah "They are {i}not{/i}, and you know it."
    "Mom doesn't dignify that, which in this house counts as a confession."
    "I wash up and sit. Dinner assembles itself out of bowls and the low, normal argument over who gets the last of the pickles."
    "Nobody mentions grades. Nobody mentions answer keys, or the office, or any of the words that lived in this kitchen during exams."
    "The conversation finds smaller work, and lets itself stay small."
    show asahina neut
    ah "Sam said the senior portal stays locked until Monday, June 2 too."
    "It's delivered as a normal fact, eyes on her food."
    show mom neut
    mom "Then nobody has anything useful to refresh tonight."
    ah "He still offered to help me study for next time. Like, set up a whole schedule and stuff."
    show mom thinking
    "Mom's spoon doesn't pause, exactly. It just slows by a fraction on its way to the bowl."
    mom "That's thoughtful."
    mom "Did you ask him to make one?"
    "Asahina's thumb taps her phone once. The screen goes dark, but not before I catch a grid of colored blocks."
    show asahina nervous
    ah "Not, like...formally."
    ah "I said I kept losing track of what to review and he sent a draft."
    mc "A draft."
    show asahina annoyed
    ah "It's useful."
    show mom neut
    mom "You've got your brother and me for studying, though. You don't have to outsource it."
    show asahina neut
    ah "I know. It's just nice that he thinks about it."
    "She says {i}thinks about it{/i} while her phone sits facedown beside the soy sauce."
    "{i}Volleyball, dinner, review blocks -- little colored fences around time she usually loses in handfuls.{/i}"
    "{i}Useful is a hard thing to object to.{/i}"
    mc "Did you actually eat lunch today?"
    show asahina frustrated
    "Asahina receives this as treason."
    ah "Why is that the second time someone's asked me that today?"
    mc "Because you do the thing where you bring it and then donate it to the inside of your bag."
    ah "I ate {i}most{/i} of it."
    mom "Most."
    show asahina smug
    ah "Most is a passing grade in some subjects."
    show mom unamused
    mom "Not in mine."
    show mom worried
    "It's a joke. The table laughs. But Mom's eyes do the quick read again, the contract read, and this time they land on Asahina and stay a half-second too long."
    "{i}She's watching both of us. Different things, same look.{/i}"
    "I let the moment move on, because making it heavier wouldn't help, and because I'm honestly not sure I'm right about what I just saw."
    "{i}Filing it anyway. The list is getting long this week.{/i}"
    $ update_character_thought("asahina", "Asahina said Sam sent a draft study schedule before she formally asked for one. It was useful enough that objecting would sound stupid, which is exactly why I keep thinking about it.")
    $ update_character_thought("mom", "Mom pinned midterm results to Monday, June 2, but she's reading both of us like contracts this week. At dinner the read settled on Asahina too, not just me.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Dinner ends and stays a dinner. That is the whole point of a good one."
    nier "I do dishes. Asahina dries exactly four things and declares the labor union satisfied. Mom takes one more call at the table, low and clipped, then sets the phone face-down like she's deciding by force that the day is over."
    nier "The house holds together in small pieces. After the last few days, the smallness is the luxury."
    call nier_clear from _call_nier_clear_0529_6
    stop music fadeout 1.0
    pause 2.0
    scene bg living_room_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music fantasyserenity
    "I am halfway to the stairs when Mom opens the cabinet beneath the television."
    "The cabinet contains old cables, a tangle of adapters for nothing in particular, instruction manuals for appliances we no longer own, and one battered game box she guards with the seriousness of precedent."
    show mom smug at t22
    show asahina curious at t21
    mom "One round."
    ah "Of what?"
    "Mom turns the box around."
    "{i}COPPER CROWN: BUILD THE REALM, CONTROL THE MARKET.{/i}"
    "The corners have gone soft from years of use. A strip of tape reinforces one side where Asahina dropped it during a particularly contested winter break."
    mc "You said the day was over."
    show mom teasing
    mom "The workday is over. Your defeat is recreational."
    show asahina smug
    ah "Wow. She came downstairs violent."
    mom "You both survived exams. I am offering enrichment."
    mc "This is the game where you buy six useless Villages and somehow turn them into a tax engine."
    show mom unamused
    mom "They are not useless when properly represented."
    show asahina neut
    ah "I have homework."
    "Her phone remains in her hand while she says it."
    show mom smug
    mom "You moved tomorrow's biology block twice during dinner. I believe the homework has counsel."
    "Asahina appeals to me."
    mc "I cannot represent you in this matter. Conflict of interest."
    show asahina unamused
    ah "Coward."
    "She sits down on the rug and leaves the space beside her open."
    "Mom takes the floor across from her and hands me the stack of starting cards without asking whether I am joining."
    "I join."
    "Copper Crown is a deck-building game about turning seven coins, three laborers, and poor impulse control into an economy before somebody else does it better."
    "Mom does it better."
    # SFX SUGGESTION: Clean card shuffling and three hands dealt across the floor.
    "She shuffles the way she preps exhibits, then deals each of us the same miserable opening hand."
    show mom determined
    mom "Standard rules. No expansion cards."
    ah "Why not the sabotage expansion?"
    mom "Because your brother still disputes the validity of the Smuggler ruling."
    mc "The rulebook says reveal, not discard."
    show mom unamused
    mom "The errata says discard."
    mc "The errata was written by cowards after publication."
    show asahina frustrated
    ah "This is why nobody plays with either of you."
    show mom teasing
    mom "And yet here you are."
    "Asahina buys a Militia at the earliest opportunity, because she approaches deck construction the way she approaches sibling conflict: direct damage first, sustainability pending."
    "Mom buys one Quarry, then removes two starting cards from her deck."
    mc "Already thinning?"
    show mom neut
    mom "A deck is allowed to stop carrying things that no longer help it."
    show asahina unamused
    ah "That sounded targeted."
    show mom smug
    mom "It was game advice. If you felt seen, discuss it with your conscience."
    "Asahina plays Militia against both of us on her next turn and is personally restored by the act."
    show asahina happy
    ah "Conscience says draw three."
    mc "Your conscience is a war criminal."
    "By the fifth round, Asahina owns every attack card she can afford, I own a chain of engines that never assemble in the same hand, and Mom owns almost nothing and draws her entire deck every turn."
    show asahina shocked
    ah "How do you have another Crown?"
    show mom unamused
    mom "I bought it."
    ah "With what money?"
    mom "The money in my hand."
    ah "You had three cards!"
    mom "Three useful cards."
    "The pile beside Asahina has been growing all game."
    show mom neut
    mom "You have good cards. You also have all of them at once."
    show asahina smug
    ah "More good is more good."
    mom "Not if they keep each other from showing up when you need them."
    show asahina thinking
    "Asahina studies her deck as though betrayal may be visible along the edges."
    mc "She's right. Your draw is clogged."
    show asahina annoyed
    ah "Nobody asked the Observatory lobby."
    "My next hand contains two Observatories, no money, and a laborer who cannot activate either one."
    show mom teasing
    mom "Would the Observatory lobby care to revise its statement?"
    mc "The lobby declines comment."
    # SFX SUGGESTION: A work-phone ringtone intruding at full volume, then repeating below.
    "Her phone rings before she can finish it."
    "The screen lights on the coffee table with a name from work. For a moment none of us moves."
    show mom frustrated
    "Mom's hand remains above the market row, one card held between two fingers."
    mom "I told them tomorrow."
    "The phone rings again."
    show mom determined
    "She sets the card facedown."
    mom "Do not touch my board."
    show asahina teasing
    ah "We have honor."
    mc "She means do not count her points."
    mom "Especially that."
    show mom at thide
    hide mom
    "She takes the call into the kitchen."
    "Her voice drops into the level professional register that travels through walls without giving away a single useful detail."
    "Asahina counts Mom's three neat piles."
    show asahina unamused
    ah "She's winning."
    mc "By a lot."
    show asahina determined
    ah "We could form a temporary coalition."
    mc "Against our own mother during a family board game."
    ah "You say that like family has ever prevented an alliance of necessity."
    "I consider the market, her attack cards, and the Crown Mom will buy the instant she returns."
    mc "What are your terms?"
    ah "You leave the last Militia for me. I stop hitting you until she loses a Province."
    mc "Two turns."
    ah "Three."
    mc "Two and you don't call it an alliance out loud."
    ah "Deal."
    "We shake hands over the discard pile."
    "Mom returns while the alliance is still theoretical."
    show mom thinking at t22
    "She sits. The facedown card goes over, and she looks at both of us for longer than the card needs."
    mom "What did you agree to?"
    show asahina neut
    ah "Nothing."
    mc "Independent market behavior."
    show mom smug
    mom "Poorly disclosed coordination, then."
    "Mom buys the Crown. We are both too busy arguing about the word to stop her."
    "Our coalition survives exactly one round. Asahina draws both Militia cards together and attacks too early; I use the opening to buy the Workshop she wanted; she retaliates; Mom watches the arrangement collapse with the quiet satisfaction of a state benefiting from rebel infighting."
    "When the final Province leaves the market, Mom wins by eleven points."
    show asahina frustrated
    ah "That is a fraudulent margin."
    show mom unamused
    mom "Count again."
    "We do. It becomes twelve."
    mc "The audit made it worse."
    show mom smug
    mom "A valuable lesson in requesting audits."
    # SFX SUGGESTION: A soft full-body thump into the rug.
    "Asahina falls backward onto the rug and stares at the ceiling."
    show asahina determined
    ah "Rematch Sunday. Sabotage expansion."
    show mom determined
    mom "After homework."
    ah "My biology block is forty-five minutes."
    mom "Then you have made room for consequences."
    show asahina happy
    "Asahina raises one fist from the floor."
    ah "Sunday."
    show mom happy
    "Mom taps her knuckles against it."
    mom "Sunday."
    "The agreement is small and completely ordinary."
    "Mom begins sorting the market cards back into their labeled slots. I gather the starting decks. Asahina remains horizontal until handed a stack she cannot ignore."
    "For a few minutes, the only work in the room belongs to putting a game away together."
    $ update_character_thought("mom", "Mom celebrated the end of exams by destroying us at Copper Crown, took one work call mid-turn, then agreed to a Sunday rematch after Asahina's homework.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The box returns to the cabinet with its decks sorted and its taped corner intact."
    nier "Asahina goes upstairs promising a strategy so unethical the expansion may reject it. Mom takes her work phone to the kitchen but leaves it facedown beside the sink."
    nier "I retreat before recreational defeat can become best two out of three."
    call nier_clear from _call_nier_clear_0529_6_5
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music fantasypassion
    "My room at night, with no exam tomorrow, is a strange and underused environment."
    "The desk is just a desk again. The review sheets have migrated into a folder I shoved out of sight, and the calculator has gone back to being a paperweight with delusions."
    "I can play until the city under the false sky actually bores me, and only regular school will object in the morning."
    "I turn on the console and get exactly twenty minutes into a dungeon before my phone lights up the desk."
    "Matsuda Akai."
    python:
        _phone_messages = [
            phone_msg("them", "Kareda has informed me that melon bread is not dinner."),
            phone_msg("me", "Strong case."),
            phone_msg("them", "Tyranny often begins with nutrition."),
            phone_msg("me", "Eat something."),
            phone_msg("them", "Et tu, sidewalk? Fine. Goodnight, " + player + "."),
            phone_msg("me", "Night."),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, append=True) from _call_phone_text_conversation_0529_4
    # She is texting him her evening as a bit now, unprompted, twelve days in.
    # Pointing a camera at him is the next thing she would escalate to.
    $ phone_open("matsuda_video")
    "I push the phone aside and turn the game back on."
    "The party reaches a checkpoint. A horned bureaucrat asks me to state my alignment preference, and for once the question feels less abstract than it did on Saturday."
    mc "...Still tired. Still neutral."
    "The game takes its processing fee and lets me through."
    "{i}At least the game has the decency to itemize the toll.{/i}"
    $ update_character_thought("matsuda", "Matsuda kept lunch surprisingly low-key and floated a possible bookstore-and-arcade trip without trying to schedule me into it. Tsubaki is apparently enforcing dinner law.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Thursday ends the way the day after a hard week is supposed to: quietly, with nothing demanded."
    nier "Somewhere across town, Tsubaki is probably making sure Matsuda eats something with a vegetable in it."
    nier "I sleep before the game can talk me out of it."
    call nier_clear from _call_nier_clear_0529_7
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0529_1
    jump a0530
