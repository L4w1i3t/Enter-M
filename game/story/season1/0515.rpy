label a0515:
    stop music # here for scene viewer later on
    # --- Day 1: 2025-05-15 ---
    $ calendar.set_date(2025, 5, 15)
    scene bg corridor
    $ show_calendar()
    show mood_afternoon zorder 3 
    with dissolve_scene_full
    window auto
    # Short sequence before the player can finally enter MC's name. Monika finds MC's ID card on the floor and returns it to him.
    show monika 1b at t11
    m "...Of course, see you then!"
    window hide
    pause 1.0
    pause 1.0
    window auto
    m "...Ah. Inappropriate flyer here..."
    m 1n "Why am I always cleaning up others' messes...?"
    window hide
    pause 1.5
    window auto
    m "Aaaaand...of course he left this thing here."
    m "Come on, you're better than this..."
    window hide
    pause 2.0
    pause 2.0
    window auto
    m "...What?"
    window hide(None)
    show monika at thide
    hide monika
    scene black
    pause 2.0
    scene bg club_day
    show mood_afternoon zorder 3 
    with dissolve_scene_soft
    play music dailyfantasy
    window auto
    # Perspective shift immediately onto MC
    # CRITIQUE: The observational opening is confident, but it assumes the reader already understands MC and Monika's rhythm. Give one tiny emotional register from MC before the shoulder-tap bit so the familiarity feels earned instead of merely clever.
    "My pen rolls between my fingers, taps once against the desk, and becomes the loudest thing in the club room."
    "When the room gets this quiet, the small details start volunteering themselves:"
    "...the closet door left at a perfect right angle, a speck of pencil lead on someone else's desk, the thin line of afternoon light caught along the window frame."
    "I roll my shoulders to loosen the tension in my neck, and a fingertip taps the right one before I can settle back down."
    "{i}Same shoulder. Same timing. She is getting predictable.{/i}"
    $ player = "?"
    mc "...Monika."
    "She pivots seamlessly into my line of sight."
    show monika 1n at t11
    m "You knew it was me."
    mc "You always tap the right shoulder. At some point it stops being a surprise and starts being a signature."
    m "A signature sounds more sophisticated than a habit, so I'll take it."
    "I lean back, giving her room to step into my line of sight."
    mc "So, what did I do this time?"
    "Monika flicks up her hand."
    m "Well, for starters..."
    "She makes a slight of hand and reveals an ID card."
    m "Looks like this has your name on it."
    m "Found it in the hallway. It was face-down near the stairs, which felt dramatic for a piece of plastic."
    "{i}That would explain why my lanyard felt suspiciously decorative.{/i}"
    mc "I was wondering where that went. Thanks."
    "Monika flips the card toward me as if it were a coin, and I catch it between two fingers mostly by accident."
    m "Anytime. Try not to make a hobby of it."
    "{i}Alright, let's slip that back into my lanyard...{/i}"
    "I hold the card face up and get a good look at my information."
    show monika at thide
    hide monika
    $ hide_calendar()
    scene black with dissolve_scene_full
    scene bg ether with wipeleft_scene
    call screen id_card_info_entry
    scene bg club_day
    show mood_afternoon zorder 3 
    $ show_calendar()
    with dissolve_scene_full
    window auto
    "There it is. My name, my birthday, and the rest of the details that make the card mine."
    show monika 3k at t11
    m "Be sure not to lose it again, 'kay?"
    mc "Yeah, yeah..."
    "She giggles at that and gives me a light nudge on the shoulder."
    mc "So...what's on the agenda today?"
    m "Honestly, I didn't get around to planning anything special today."
    m "I had a few ideas this morning, then classes happened, and now those ideas are somewhere under a pile of other people's paperwork."
    "Monika shrugs, but the smile she gives me is practiced enough to hide how tired she probably is."
    mc "Usual routine works for me. I brought something you can tear apart, actually."
    m "Tear apart sounds harsh. I prefer carefully disassemble."
    mc "That's what people say when they own red pens."
    "I pull the pages from my bag before I can change my mind."
    mc "Just don't make the margins bleed too much."
    show monika at thide
    hide monika
    $ hide_calendar()
    scene black with wipeleft_scene
    # CRITIQUE: You skip the first actual literature-club activity after setting it up. Since Monika is supposed to be MC's crutch and the club matters long-term, show one concrete workshop note or poem exchange instead of summarizing the routine.
    nier "My routine after-school club activities are often mundane. Same old writing, same old presentations, same old friends..."
    nier "I don't hate it though. Monotonous, yes, but it's a different kind of monotony, if that makes sense."
    nier "Everyone needs a go-to place to just be themselves, after all."
    call nier_clear from _call_nier_clear_0515_1
    nier "Today's activities carried on without much incident."
    nier "Come dinnertime, all members had already shuffled out, leaving just Monika and me to lock up."
    call nier_clear from _call_nier_clear_0515_2
    scene bg club_day
    show mood_evening zorder 3 
    show monika 1a at t11
    $ show_calendar()
    with wipeleft_scene
    mc "Alrighty, so, same time tomorrow?"
    m "You betcha!"
    m "Oh, and I was actually thinking, [player]..."
    m "I got two tickets to that neat-looking horror flick coming out on Sunday, so..."
    "I look at the calendar app on my phone."
    mc "Let's see...do I have anything going on that day..."
    mc "Nope, doesn't look like it. I'm free."
    m "Great! It's a date, then!"
    play sound moddooropen
    "Monika waltzes to the door and begins her exit."
    m "I'm outta here now, so see you tomorrow!"
    "I hold my hand up in a wave."
    mc "Later, Ms. President."
    show monika at thide
    hide monika
    play sound moddoorclose
    # CRITIQUE (ADDRESSED): "Out of eye shot" is awkward idiom. "Out of sight" or "out of earshot" would be cleaner depending on what MC means.
    "Once she is out of both sight and earshot, I let out a long sigh and sling my bag over my shoulder."
    $ phone_mark_contact_met("monika")
    $ mark_character_met("monika")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The ride home was uneventful. Bus stop, bus ride, short walk home, the usual route."
    nier "I don't have much to say about it, really. I just...went home."
    call nier_clear from _call_nier_clear_0515_3
    scene bg house
    $ show_calendar()
    show mood_afternoon zorder 3 
    with wipeleft_scene
    "By the time I reach the front gate, the first thing I smell is smoked meat, melted cheese, and the particular kind of salt that only comes from a paper bag with grease spots."
    "My little sister Asahina is on the swing in the yard, one foot planted in the dirt so she can keep herself rocking while she eats."
    show asahina neut at t11
    "She looks up at me and gives me a small upward nod, mid-bite."
    mc "Bill's Flamey Double again?"
    "She swallows her bite."
    ah "...Yeah, what about it?"
    mc "I'm starting to think they put your name on a stool in there."
    ah "And your point is?"
    mc "Nothing. I'm just saying the cashier probably starts the order when he sees you cross the street."
    ah "Yeah, well, I have money, practice burns it off, and the cashier does not know my name."
    # CRITIQUE (ADDRESSED): The sibling bite is clear, but "fatass" and "bagged obesity" are harsher than the surrounding affection supports. This risks making MC read cruel instead of merely teasing.
    mc "Whatever you say, fatass."
    "Before I can even smile at my own comment, a fry hits me on the cheek."
    ah "Okay, listen here you little--!"
    "I then find the moment to snicker."
    "{i}It's always too easy with her...{/i}"
    mc "Anyway, I'm heading in. Enjoy your bagged obesity."
    ah "Screw you too."
    show asahina at thide
    hide asahina
    $ phone_mark_contact_met("asahina")
    $ mark_character_met("asahina")
    $ hide_calendar()
    scene black with wipeleft_scene
    scene bg doorday
    $ show_calendar()
    show mood_home zorder 3 
    with wipeleft_scene
    play sound moddooropen
    mc "Hey, mom."
    show mom neut at t11
    mom "Ah, hey there, [player]!"
    mom "Just in time, actually. I wanted to go over something with you, whenever you're available."
    mc "Oh, uh, alright."
    mc "I have nothing going on at the moment, just let me get in the door first..."
    mom "Take your time."
    mom "Oh, wait, question: katsudon sound good for dinner? I'm trying to find an excuse to use these pork loins before they expire."
    # CRITIQUE (ADDRESSED): Proofreading nit: "porkloins" should probably be "pork loin" or "pork loins"; the food detail is grounded, so the compound-word error stands out.
    mc "Yeah, fine by me. Anyway, off I go."
    "I give mom a gesture towards my room upstairs and subtly lift my bag from my shoulder to express my intent."
    show mom at thide
    hide mom
    scene bg bedroom with wipeleft_scene
    "I drop my bag by the side of my desk and stretch my arms overhead."
    "My room looks exactly how I left it this morning."
    "{i}Figures.{/i}"
    "I pull my phone out of my pocket and check the time."
    "{i}Still early...{/i}"
    "{i}I could probably get a head start on something.{/i}"
    "..."
    "I don't."
    "I flop onto my bed and stare at the ceiling for a moment."
    "{i}Same day, same routine.{/i}"
    "{i}...Guess that's not the worst thing in the world.{/i}"
    $ phone_mark_contact_met("mom")
    $ mark_character_met("mom")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Before long, I find myself back downstairs."
    call nier_clear from _call_nier_clear_0515_4
    scene bg kitchen
    $ show_calendar()
    show mood_home zorder 3 
    with wipeleft_scene
    "Mom's already at the counter, prepping different vegetables and a spice mix."
    "The pork loins are currently thawing in the sink, submerged in cold water."
    show mom neut at t11
    mc "Need a hand?"
    mom "You know it, kiddo."
    "She gestures at the cutting board beside her."
    mom "You're better than me at dicing onions, so have at it."
    "{i}Gonna make me cry, huh?{/i}"
    show mom at thide
    hide mom
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Time passes as I cut vegetables, keep watch on the thawing loins, and look in the fridge for anything we may have missed in our prep."
    nier "Mom covers the bases of cooking the rice and other tasks that require passivity above all."
    nier "Eventually, we reach the step of beating, breading, and frying the loins."
    call nier_clear from _call_nier_clear_0515_5
    scene bg kitchen
    show mom neut at t11
    $ show_calendar()
    show mood_home zorder 3 
    with wipeleft_scene
    "Once we have the meat in the pan, we both almost simultaneously take a deep breath."
    mc "So...you wanted to run something by me?"
    mom "Yes! So, I was digging around earlier today..."
    mom "Found a university that I think would be a good fit for you..."
    # CRITIQUE: The college conversation is important but list-shaped. One specific program detail, brochure image, commute number, or MC physical reaction would make the future feel concrete instead of like exposition.
    mc "...Already, huh?"
    mom "Oh, don't be like that. If anything, we're a little late to the party."
    mom "You're graduating in literally less than a year. I don't wanna be that kind of overbearing parent who nags, but it's time to start thinking about what comes next."
    "I widen my eyes and slowly nod."
    mc "...When you put it that way..."
    mc "True, I know of at least a few classmates who have already made it clear what they're wanting to do."
    "{i}Monika probably already has this figured out...{/i}"
    mc "Anyway, I'm still listening."
    mom "The one I looked at, it has a lot of boxes checked off."
    mom "It has a {i}very{/i} strong program in what you seem to be enthusiastic about, so that's already a plus."
    mom "Not to mention great reputation, and a decent distance from home. I know you said recently that you want to go and see the world, so..."
    mom "You think we could do more digging together sometime soon? Completely up to you, I won't force you."
    mc "I, uh..."
    mc "...Yeah, I mean, sure. I'm down."
    "{i}Surely I'm not behind the curve...right?{/i}"
    "{i}School, extracurriculars, clubs, home...{/i}"
    "{i}And I'm really supposed to decide what comes after all that, huh?{/i}"
    mom "You know, you don't have to commit to anything right {i}now{/i}."
    mom "Buuut you {i}do{/i} have to start thinking about it."
    mom "You hear me on that?"
    "I shuffle the pan a little bit."
    mc "Crystal clear."
    show mom at thide
    hide mom
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "About fifteen, maybe twenty minutes pass as we finish preparing the katsudon and readying our plates."
    nier "One for me, one for mom, and one for my sister."
    nier "The last plate didn't have much on it. One wedge of pork and exactly one spoon of rice."
    call nier_clear from _call_nier_clear_0515_6
    scene bg kitchen
    $ show_calendar()
    show mom neut at t22
    show asahina neut at t21
    show mood_home zorder 3 
    with wipeleft_scene
    "My sister takes her seat, not even giving her own plate the time of day."
    ah "...Smells good."
    mom "That's all you're having?"
    ah "Yeah."
    ah "I'm not that hungry today."
    "I take a sip of water."
    mc "...Really, Asa?"
    mom "Asahina, you should really eat something proper."
    mom "I don't think those empty bags of chips in your room are all that filling."
    mom "And fast food isn't exactly a balanced diet, either."
    mc "Wait... so that's where my snacks have been going?!"
    mc "...You owe me."
    "Asahina pauses for a second before picking up her chopsticks and nudging the pork slightly."
    ah "Yeah, I guess..."
    "She takes a small bite, like she's expecting the fork to stab back."
    "{i}Not that she'd admit she already ate, knowing mom was cooking.{/i}"
    "Mom watches for a moment before letting it go."
    # CRITIQUE: This is a major warning light if Asahina's later side story involves food scrutiny. Do not let the narration wave it away as "nothing" unless that denial is clearly MC's blind spot.
    "{i}Same old, same old.{/i}"
    "{i}It's always something with Asa.{/i}"
    "{i}Nothing worth making a fuss over, though.{/i}"
    show mom at thide
    hide mom
    show asahina at thide
    hide asahina
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Dinner ends with plates cleared, lights dimmed, and everyone drifting back into their usual routines."
    nier "On my end, I spend my time cranking out whatever homework I have in five minutes flat--or at least that's what it feels like."
    nier "With nothing else to do, I fall back on the usual. A poem for Monika's club, the occasional book, gaming via going through a JRPG with about fifteen self-imposed restrictions, the works."
    nier "Time passes without much resistance..."
    call nier_clear from _call_nier_clear_0515_7
    stop music fadeout 2.0
    pause 1.0
    scene bg doornight
    $ show_calendar()
    show mood_night zorder 3 
    with wipeleft_scene
    play music fantasypassion
    # CRITIQUE: "Stygian embrace" is much too purple for a glue-fetch scene unless the melodrama is deliberately being mocked. The prose and the errand are fighting each other.
    "Night has enveloped the world with its stygian embrace."
    "The house is quieter than other days. Usually someone's up to some sort of hijinks."
    "Today we have mom flipping the pages of her book in the living room, and Asahina on the floor tapping away at her handheld."
    "As for me, I decide to wrap things up early. My previous night of doomscrolling random wiki articles is to thank."
    "Before clocking out, I take a couple drinks of water, take my medication, and--"
    show asahina neut at t11
    ah "You know if we have any glue anywhere? The white, sticky kind, not the sticks."
    "{i}Dude, phrasing...{/i}"
    mc "...Uhhh...I don't know, actually."
    mc "You check that one drawer yet?"
    ah "You think I haven't?! Uuuuughhhhh, what do I do...?"
    mc "What do you need it for, anyway?"
    ah "Stupid me completely forgot to make this poster that I've been putting off for a week now!"
    ah "Volleyball team wants ME of all people to be the outreach member for all the dumbass recruiting and stuff!"
    mom "Language, Asahina!"
    ah "S-Sorry, mom..."
    ah "So, anyway...yeah."
    mc "...What do you want me to do about it? You've always been the artsy one."
    mc "Me? I can't draw a straight line with a ruler."
    ah "Urgh, I dunno....."
    mc "When do you need it done by?"
    ah "They never gave me a deadline, just 'as soon as humanly possible' and that's it..."
    mc "I see, I see..."
    "I ponder my options for a couple seconds."
    mc "Well, I was going to pick up this new game on launch Saturday..."
    mc "If you want me to grab some glue while I'm out, I can do that."
    "Asahina sighs and takes a subtle bow."
    ah "Yes, that'd be amazing!"
    ah "And, uh, in return, I can...uhhh...restock your chips! Yeah!"
    mc "Yeah, sure, why not. It's a deal."
    "I inadvertently finish the bottle of water that was in my hand."
    mc "Now, I hate to be that guy, but I'm dozing off as we speak."
    ah "Then go to bed, doofus!"
    mc "Says the one stalling me."
    ah "Whatever you say..."
    show asahina at thide
    hide asahina
    "As Asahina trails off, I make my way back upstairs and into the comfort of my room."
    "{i}Way for her to trip me into doing her fetch quests...{/i}"
    $ hide_calendar()
    scene black with dissolve_scene_full
    nier "The rest of my waking night falls into the same pit I was in yesterday."
    nier "Nonetheless, I set a reminder on my phone to grab an extra item at the store after school on Saturday."
    nier "With everything for the day crossed off my list and an ever-looming boredom, I set my phone aside with a video playing."
    nier "{i}Another day down...{/i}"
    nier "{i}And plenty more just like it ahead.{/i}"
    call nier_clear from _call_nier_clear_0515_8
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0515_1
    jump a0516
