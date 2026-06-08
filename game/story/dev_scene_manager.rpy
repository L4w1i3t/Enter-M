# File to write out random scenes for the story, but are currently out of context.
label dev_scene_manager:
    stop music
    scene black
    # set MC's name to MC for now
    $ dev_player_name = "MC"
    $ player = dev_player_name
    "Select a scene:"
    menu:
        "Asahina Grill":
            jump dev_asahina_grill
        "Act 3 Implicit *** Scene":
            jump dev_act3_implicit_scene
        "Tsubaki Completely Ruined":
            jump dev_tsubaki_completely_ruined
        "MC Breaking Point (w/ Monika)":
            jump mc_breaking_point
        "More Scenes":
            menu:
                "Mom Reveals Her Diagnosis":
                    jump dev_mom_cancer_reveal
                "Monika Tells MC She's Disbanding the Club":
                    jump dev_monika_disbands_club
                "Return":
                    jump dev_scene_manager
        "Jump to enable/disable menu":
            menu:
                "Enable/Disable ALL Content":
                    $ _all_on = persistent.archive_unlocked_roster and persistent.archive_unlocked_music and persistent.archive_unlocked_cgs and persistent.archive_unlocked_character_stories and persistent.archive_unlocked_lost_records
                    if _all_on:
                        python:
                            persistent.archive_unlocked_roster = False
                            persistent.archive_unlocked_music = False
                            persistent.archive_unlocked_cgs = False
                            persistent.archive_unlocked_character_stories = False
                            persistent.archive_unlocked_lost_records = False
                            for _cat in character_story_catalog:
                                for _story in _cat.stories:
                                    if _story.persistent_key:
                                        setattr(persistent, _story.persistent_key, False)
                            for _act in cg_gallery_catalog:
                                for _ch in _act.chapters:
                                    for _cg in _ch.cgs:
                                        if _cg.persistent_key:
                                            setattr(persistent, _cg.persistent_key, False)
                        "All content disabled."
                    else:
                        python:
                            persistent.archive_unlocked_roster = True
                            persistent.archive_unlocked_music = True
                            persistent.archive_unlocked_cgs = True
                            persistent.archive_unlocked_character_stories = True
                            persistent.archive_unlocked_lost_records = True
                            for _cat in character_story_catalog:
                                for _story in _cat.stories:
                                    if _story.persistent_key:
                                        setattr(persistent, _story.persistent_key, True)
                            for _act in cg_gallery_catalog:
                                for _ch in _act.chapters:
                                    for _cg in _ch.cgs:
                                        if _cg.persistent_key:
                                            setattr(persistent, _cg.persistent_key, True)
                        "All content enabled."
                "Enable/Disable Roster Archive":
                    if persistent.archive_unlocked_roster:
                        $ persistent.archive_unlocked_roster = False
                        "Roster Archive Disabled."
                    else:
                        $ persistent.archive_unlocked_roster = True
                        "Roster Archive Enabled."
                "Enable/Disable Music Archive":
                    if persistent.archive_unlocked_music:
                        $ persistent.archive_unlocked_music = False
                        "Music Archive Disabled."
                    else:
                        $ persistent.archive_unlocked_music = True
                        "Music Archive Enabled."
                "Enable/Disable CG Gallery":
                    if persistent.archive_unlocked_cgs:
                        python:
                            persistent.archive_unlocked_cgs = False
                            for _act in cg_gallery_catalog:
                                for _ch in _act.chapters:
                                    for _cg in _ch.cgs:
                                        if _cg.persistent_key:
                                            setattr(persistent, _cg.persistent_key, False)
                        "CG Gallery Disabled."
                    else:
                        python:
                            persistent.archive_unlocked_cgs = True
                            for _act in cg_gallery_catalog:
                                for _ch in _act.chapters:
                                    for _cg in _ch.cgs:
                                        if _cg.persistent_key:
                                            setattr(persistent, _cg.persistent_key, True)
                        "CG Gallery Enabled."
                "More":
                    menu:
                        "Enable/Disable Character Stories":
                            if persistent.archive_unlocked_character_stories:
                                python:
                                    persistent.archive_unlocked_character_stories = False
                                    for _cat in character_story_catalog:
                                        for _story in _cat.stories:
                                            if _story.persistent_key:
                                                setattr(persistent, _story.persistent_key, False)
                                "Character Stories Disabled."
                            else:
                                python:
                                    persistent.archive_unlocked_character_stories = True
                                    for _cat in character_story_catalog:
                                        for _story in _cat.stories:
                                            if _story.persistent_key:
                                                setattr(persistent, _story.persistent_key, True)
                                "Character Stories Enabled."
                        "Enable/Disable Lost Records":
                            if persistent.archive_unlocked_lost_records:
                                $ persistent.archive_unlocked_lost_records = False
                                "Lost Records Disabled."
                            else:
                                $ persistent.archive_unlocked_lost_records = True
                                "Lost Records Enabled."
                "Return to scene selection":
                    jump dev_scene_manager
    return

label dev_asahina_grill:
    # Scene in act 1 where MC comes home to Asahina getting ripped a new one by mom in the living room, due to mom finding out that Asahina ended up doing some not-so-innocent things with Sam (you know...sex).
    scene black
    stop music
    pause 2.0

    # Scene starts as MC is entering the house after school.
    scene bg living_room with dissolve_scene_full
    play music "mod_assets/bgm/roster_place.ogg"
    "I step into the house, dropping my bag by the door."
    "Mom's voice carries from the living room."
    "Not the usual 'how was your day' tone either."
    "Asa's backpack is on the floor. A couple books. A jacket. The dog's favorite pillow."
    "Whatever this is, it's already been going on for a while."
    show asahina neut at t41
    ah "Mom, please! I'm sorry! It won't happen again, I swear!"
    
    show mom neut at t43
    mom "You're {i}sorry{/i}? Asahina, do you have any FUCKING idea—"
    show mom neut
    "They both turn."
    "Shit."
    
    ah "Oh god, [player]—"
    
    "Her hands fly up to cover her face."
    mc "I—I'm just gonna...go to my room—"
    show mom neut
    mom "[player]. Stay."
    show mom neut
    mc "But I don't think I should really be—"
    show mom neut
    mom "I said {i}stay{/i}."
    show mom neut
    "That tone doesn't leave room for negotiation."
    "I cannot remember the last time I heard her use it."
    
    ah "Mom, please, not in front of—"
    
    show mom neut
    mom "You lost the right to 'please' when you decided to LIE to me for the past two months!"
    show mom neut
    "Asahina's hands are trembling."
    "She won't look at either of us."
    show mom neut
    mom "Asahina, look at me."
    show mom neut
    
    ah "..."
    
    show mom neut
    mom "Asahina."
    show mom neut
    "Asahina lifts her head."
    show mom neut
    mom "You are {i}sixteen years old{/i}."
    mom "Sixteen. Do you understand what that means?"
    show mom neut
    
    ah "I know, but we were careful, and it's not like—"
    
    show mom neut
    mom "Careful? {i}Careful{/i}?"
    mom "You think being 'careful' makes this okay?"
    show mom neut
    "Mom's voice cracks."
    show mom neut
    mom "What if something had gone wrong? What if you'd gotten pregnant?"
    mom "What if he'd pressured you into something you weren't ready for?"
    show mom neut
    
    ah "He didn't! I {i}wanted{/i} to—"
    
    "She stops mid-sentence."
    "Oh god, I did {i}not{/i} need to hear that."
    mc "Okay, seriously, I really don't need to be here for this—"
    show mom neut
    mom "[player], sit down."
    show mom neut
    mc "Mom—"
    show mom neut
    mom "Sit. DOWN."
    show mom neut
    "I sink into the chair by the door."
    "As far from the couch as I can get."
    
    ah "Can we {i}please{/i} talk about this without—"
    
    show mom neut
    mom "No. Because you know what? You want to act like an adult? Fine."
    mom "Adults don't get to hide behind closed doors when they mess up."
    mom "Adults face the consequences of their actions."
    show mom neut
    "The silence stretches out."
    "I stare at the floor."
    
    ah "I thought...I thought I was ready..."
    ah "I'm sorry, Mom. I'm so sorry..."
    
    show mom neut
    mom "I know you think you're grown up enough to make these decisions."
    mom "But sweetheart, you're not. Not yet."
    show mom neut
    "Mom sits down on the couch."
    show mom neut
    mom "And I blame myself for not seeing this coming."
    mom "For not talking to you about these things sooner."
    show mom neut
    
    ah "It's not your fault—"
    
    show mom neut
    mom "But that doesn't change what happened."
    mom "So here's what's going to happen."
    mom "First, you're grounded. Completely. One month."
    mom "School and back. No hanging out with friends. No phone except for emergencies."
    mom "And when you {i}do{/i} get your phone and social privileges back, I'm installing a tracking app on it, and so help me GOD if I find out you uninstall or disable it."
    show mom neut
    
    ah "A whole month?!"
    
    show mom neut
    mom "Second, we're making an appointment with the doctor. You're getting a full checkup."
    mom "And we're going to have a {i}real{/i} conversation about protection, consent, and everything else you should have talked to me about {i}before{/i} making this choice."
    show mom neut
    
    ah "Mom, that's so embarrassing—"
    
    show mom neut
    mom "Embarrassing? You think {i}that's{/i} embarrassing?"
    mom "Try getting a phone call from Sam's mother asking if I knew my daughter was sexually active."
    show mom neut
    "I wince."
    "So that's how it came out."
    show mom neut
    mom "Third, I'm calling Sam's parents. We're all going to sit down and have a conversation about you and him."
    mom "You're included in this too, [player]."
    show mom neut
    "I throw both my arms up in exasperation."
    show mom neut
    mom "Don't look at me like that."
    show mom neut
    
    ah "No, no, no, please don't—"
    
    show mom neut
    mom "This isn't a negotiation, Asahina."
    show mom neut
    "Asahina buries her face in her hands."
    mc "Um...can I be excused now? Please?"
    show mom neut
    mom "No."
    show mom neut
    "Wait, what?"
    show mom neut
    mom "[player], you're eighteen. You're about to graduate."
    mom "You think this doesn't apply to you too?"
    show mom neut
    mc "I didn't—I mean, I wasn't—"
    show mom neut
    mom "I know you weren't. But you {i}are{/i} going to think about what you're going to do if you ever find yourself in a situation like this."
    mom "Because I won't always be around to have these conversations, and {i}you're{/i} about to enter a very unforgiving adult world."
    show mom neut
    "I sink lower in my chair."
    show mom neut
    mom "Do you understand me?"
    show mom neut
    mc "...Yes, ma'am."
    show mom neut
    mom "Good. {i}Now{/i} you can go."
    show mom neut
    "I stand up, keeping my head down."
    "As I reach the stairs, Mom's voice softens behind me."
    show mom neut
    mom "Come here, baby..."
    show mom neut
    "I don't stick around."
    "Why did it feel like I was getting scolded too?"
    "The hell did I even do?"
    
    scene bg bedroom with wipeleft_scene
    "I close my door and lean against it."
    "That was..."
    "Yeah."
    
    scene black with dissolve_scene_full
    stop music fadeout 2.0
    pause 2.0
    
    jump dev_scene_manager
    #return #END SCENE

label dev_act3_implicit_scene:
    # This scene is more of a hidden scene if the player meets a series of conditions. Mainly a fanservice scene for the extra horny audience
    scene black
    stop music
    pause 2.0

    # Scene starts as MC and Matsuda are entering the latter's home.
    scene bg kitchen with dissolve_scene_full
    play music "mod_assets/bgm/roster_place.ogg"
    "The front door clicks shut behind us."
    "Matsu kicks off her shoes and heads to the kitchen, flicking on light switches one by one."
    show matsuda neut at t11
    "She opens the fridge, stares into it for a few seconds, then closes it without taking anything."
    mc "You eaten today?"
    show matsuda neut
    ma "Does coffee count?"
    show matsuda neut
    mc "No."
    show matsuda neut
    ma "Then no."
    show matsuda neut
    mc "...What...could I fix you to eat? Nutrition is important, you know."
    show matsuda neut
    ma "I'm fine."
    show matsuda neut
    mc "That's not what I asked."
    show matsuda neut
    ma "I said I'm fine, damn."
    show matsuda neut
    mc "Alright..."
    "A moment passes."
    show matsuda neut
    ma "Come on. Kitchen's depressing."
    show matsuda neut
    "She walks toward the hallway, snapping her fingers in my direction as a means of beckoning me to follow."
    
    scene bg hallway with dissolve_scene_half
    "I cannot remember the last time I was in her house."
    "This time, I take note of the inoffensive decor."
    "A few posters on the walls, some art prints. Normal stuff."
    show matsuda neut at t11
    ma "Upstairs."
    show matsuda neut
    "She ascends without another word, and I reluctantly yet confusingly join her."

    scene bg bedroom with dissolve_scene_half
    "Her room's cleaner than I expected."
    "Matsu drops onto her bed and stares at the ceiling."
    show matsuda neut at t11
    mc "So."
    show matsuda neut
    ma "So."
    show matsuda neut
    "I sit on the edge of the bed, effectively inviting myself."
    mc "What a wild sequence of events lately..."
    mc "If you asked high school me what I thought my life would be like now, I never would have guessed any of this."
    show matsuda neut
    ma "Yeah."
    show matsuda neut
    "She sits up."
    show matsuda neut
    ma "Can I ask you something?"
    show matsuda neut
    mc "Sure."
    show matsuda neut
    ma "You ever just...get tired of everything being so complicated?"
    show matsuda neut
    mc "...Yeah. More often than I'd like."
    show matsuda neut
    "She looks at me for a moment, then glances toward the corner of her room."
    mc "But I gotta say, Koto showing up like that felt like...like some sort of saving grace."
    mc "After that, we didn't really even have to think, yeah?"
    show matsuda neut
    ma "Mhm."
    show matsuda neut
    "She scoots over to the corner of her bed, pulling at a fitted sheet."
    mc "At any rate, I {i}do{/i} think we've earned some down time, and I was thinking..."
    mc "That VR lab downtown's having their grand opening next week. Maybe we could check it out then?"
    show matsuda neut
    ma "Sure."
    show matsuda neut
    "She pulls out a small box from between the mattress and wall."
    mc "I mean, you don't have to, but I figured I'd offer."
    show matsuda neut
    ma "Yeah, sounds good."
    show matsuda neut
    mc "We could grab lunch, make a whole thing of it..."
    "Matsu's still fumbling with whatever she pulled out."
    mc "...You're not listening to me at all, are you?"
    mc "Matsu?"
    mc "You good?"
    mc "I can take 'no' for an answer, you know."
    mc "It's not like I'm forcing you to do anyt—{w=1.0}{nw}"
    "She turns to me and tosses something at me, and I catch it on reflex."
    "It's a small wrapper with..."
    show matsuda neut
    stop music
    ma "So we doing this, or are you gonna keep yapping with your pants still on?"
    show matsuda neut
    mc "..."
    mc "...Ah."
    
    scene black with dissolve_scene_full
    stop music fadeout 3.0
    
    pause 2.0
    
    jump dev_scene_manager
    #return #END SCENE

label dev_tsubaki_completely_ruined:
    # At school, almost finals week before graduation. Near the end of the story of Act 1. MC is getting rather fed up with Matsuda's controlling and manipulative tendencies. MC and Matsu are in a classroom after school, and they are met by Tsubaki, who presents as completely disheveled and broken. Not even the same girl as from months ago. This is from a gradual deterioration and loss of agency throughout the story (due to Sam--Asahina's boyfriend).
    scene black
    stop music
    pause 2.0
    scene bg class_day
    show vignette zorder 99:
        alpha 0.5
    with dissolve_scene_full
    play music roster_place
    # Lunchtime in a room with just MC and Matsu in it
    "The smell of finished bento and wasabi lingers in the air."
    "Matsu takes a rather loud swig of her ramune after popping the ball in like a gun."
    show matsuda neut at t11
    # Matsu's up to her usual bullshit
    ma "So about the student council thing..."
    mc "I already told you, I'm not interested."
    show matsuda neut
    ma "Come on, it'd look great for—"
    show matsuda neut
    mc "Matsu. No."
    "She crosses her arms."
    show matsuda neut
    ma "You don't have to be such a dick about it."
    show matsuda neut
    mc "And you don't have to keep pushing things I've already said no to."
    "The silence stretches. I can feel the tension building."
    "This has been happening more and more lately—every conversation with her feels like a negotiation I didn't agree to participate in."
    show matsuda neut
    ma "Whatever. Your loss."
    show matsuda neut
    "I'm about to respond when the classroom door slides open."
    stop music fadeout 2.0
    "We both turn."
    show matsuda neut at t41
    show tsubaki post at t43
    "Tsubaki stands in the doorway. At least...I think it's Tsubaki."
    "Her chestnut hair with blonde highlights falls completely loose around her face, disheveled and unwashed."
    "Makeup's smeared down her cheeks—mascara tracks cutting through foundation. She's been crying. A lot."
    "Dark circles under her eyes that no amount of concealer could hide."
    "Her uniform's a disaster—wrinkled shirt, collar undone, blazer tied haphazardly around her waist."
    "She looks like someone who tried too hard to hold it together and gave up halfway. She's staring at the floor."
    mc "...Tsubaki?"
    "She doesn't look up."
    play music hopeless
    show tsubaki post
    ts "Sorry. I didn't know anyone was...I can go."
    show tsubaki post
    mc "No, it's fine, we were just—"
    show matsuda neut
    ma "Hey, you good? You look like shit."
    show matsuda neut
    "Subtle as a brick, as always."
    show tsubaki post
    ts "I'm fine."
    show tsubaki post
    "Tsubaki takes a few steps into the room, moving like she's operating on autopilot. She sits down at a desk near the window, staring out at nothing."
    mc "Tsubaki, seriously, are you okay?"
    show tsubaki post
    ts "I said I'm fine."
    show tsubaki post
    show matsuda neut
    ma "When's the last time you slept?"
    show matsuda neut
    show tsubaki post
    ts "I don't know."
    show tsubaki post
    show matsuda neut
    ma "You don't know?"
    show matsuda neut
    show tsubaki post
    ts "Does it matter?"
    show tsubaki post
    "I exchange a glance with Matsu. For once, she looks as concerned as I feel."
    mc "Tsubaki...what's going on?"
    "She doesn't answer. Just keeps staring out the window."
    mc "This is about Sam, isn't it?"
    "Her shoulders tense."
    show tsubaki post
    ts "He's...he's been stressed lately. Finals coming up and everything."
    show tsubaki post
    "That line again."
    "I've heard it from Asa, or at least something similar."
    mc "Okay, but that doesn't explain why {i}you{/i} look like you haven't eaten or slept in days."
    show tsubaki post
    ts "I'm just trying to be supportive."
    show tsubaki post
    show matsuda neut
    ma "Supportive? Tsuba, you look like you're about to collapse."
    show matsuda neut
    show tsubaki post
    ts "I'm fine. He needs me right now, that's all."
    show tsubaki post
    mc "What about what {i}you{/i} need?"
    show tsubaki post
    ts "I don't...I'm fine."
    show tsubaki post
    show matsuda neut
    ma "Has he been...?"
    show matsuda neut
    "Matsu trails off, but the implication hangs in the air."
    show tsubaki post
    ts "No. He's not like that. He just...he has a lot going on, and I want to help."
    show tsubaki post
    mc "Tsubaki, you can barely stand. How are you supposed to help anyone when you can't even help yourself?"
    show tsubaki post
    ts "I can handle it."
    show tsubaki post
    mc "You really can't."
    show tsubaki post
    ts "You don't understand."
    show tsubaki post
    mc "Then help me understand, because he's been using you as an emotional punching bag."
    show tsubaki post
    ts "He's not—"
    ts "He loves me."
    show tsubaki post
    show matsuda neut
    ma "Love doesn't look like this, Tsuba."
    show matsuda neut
    show tsubaki post
    ts "You don't know him like I do."
    show tsubaki post
    mc "Maybe not. But I know you."
    mc "Or at least, I knew you."
    mc "And whoever this is..."
    "I gesture at her."
    mc "This isn't you."
    "Her hands are shaking."
    "She curls them into fists, nails digging into her palms."
    show tsubaki post
    ts "I'm still me."
    show tsubaki post
    mc "Are you?"
    mc "Because the Tsubaki I knew wouldn't let anyone treat her like this."
    mc "The Tsubaki I knew would've seen through his bullshit months ago."
    show tsubaki post
    ts "Maybe you didn't know me as well as you thought."
    show tsubaki post
    "..."
    show matsuda neut
    ma "Tsubaki, listen—"
    show matsuda neut
    show tsubaki post
    ts "I don't need a lecture from you, Matsuda."
    show tsubaki post
    show matsuda neut
    ma "I'm not lecturing. I'm trying to—"
    show matsuda neut
    show tsubaki post
    ts "To what? Fix me?"
    ts "I'm not broken."
    show tsubaki post
    mc "No one's saying you're broken."
    show tsubaki post
    ts "You're both looking at me like I'm some kind of...charity case."
    ts "Like I'm pathetic."
    show tsubaki post
    mc "That's not—"
    show tsubaki post
    ts "I'm {i}fine{/i}."
    show tsubaki post
    "She stands abruptly."
    "The chair scrapes against the floor."
    show tsubaki post
    ts "I shouldn't have come here."
    show tsubaki post
    mc "Tsubaki, wait—"
    show tsubaki post
    ts "Just...leave me alone."
    show tsubaki post
    "Her hand hovers on the door handle for a second. Maybe less. She's at the door before I can stop her."
    show tsubaki post at thide
    hide tsubaki post
    "The door slides shut."
    "And then it's just me and Matsu."
    show matsuda neut at t11
    "Neither of us says anything for a long moment."
    show matsuda neut
    ma "...Fuck."
    show matsuda neut
    mc "Yeah."
    show matsuda neut
    ma "That was bad. Really bad."
    "I sink into a chair."
    "My chest feels tight."
    mc "Why didn't we do something sooner?"
    show matsuda neut
    ma "I mean, we...we tried, but..."
    show matsuda neut
    "A beat passes."
    mc "Someone needs to talk to Sam."
    show matsuda neut
    ma "Good luck with that. Guy's a manipulative, dickless piece of shit."
    show matsuda neut
    mc "He's already doing this to Asa. I can't just—"
    show matsuda neut
    ma "And when that doesn't work?"
    show matsuda neut
    mc "..."
    show matsuda neut
    ma "This is so fucked up."
    show matsuda neut
    mc "What else is new?"
    "Finals are in two weeks, and graduation's right around the corner."
    "At this very moment, I don't trust myself to stay in this room."
    mc "I need some water."
    show matsuda neut
    ma "Fountain down the hall."
    show matsuda neut
    
    scene bg corridor
    show vignette zorder 99:
        alpha 0.5
    with wipeleft_scene
    "I step out into the hallway, water bottle in hand. The fountain's at the far end, near the stairs."
    "As I walk, voices drift from around the corner. Two jocks. Laughing."
    npc1 "Yo, you see that girl just now?"
    npc2 "The one that looked like shit? Yeah."
    npc1 "Wasn't that Tsubaki or whatever?"
    npc2 "Dude, she looks like a used up, worn out sack."
    npc1 "Bro, I'm saying! The fuck happened?"
    npc2 "She's banging Sam, right? Dude's got like three bitches."
    npc1 "Wait, for real? She knows?"
    npc2 "Prolly. Girls like that always know. They just desperate."
    npc1 "That's fucked."
    npc2 "That's pathetic. Yo, we're late, let's go."
    "Their footsteps fade. I stand there, water bottle still in my hand. Still empty."
    "..."
    
    scene black with dissolve_scene_full
    menu:
        "Continue":
            jump sam_encounter_99
        "Exit":
            stop music fadeout 2.0
            pause 2.0
            
            jump dev_scene_manager

label sam_encounter_99:
    # MC is leaving school, trying to catch the bus. He has a run-in with Sam. This happens after the Tsubaki scene, MC is already aware of Sam's pattern with both Asahina and Tsubaki.
    scene bg residential_day
    show vignette zorder 99:
        alpha 0.5
    with dissolve_scene_full
    "The final bell rang twenty minutes ago."
    "Most people have already left. I should have too, but I needed to finish up some work in the computer lab."
    "Now I'm cutting it close. If I miss this bus, the next one doesn't come for another little bit."
    "I push through the doors and head down the steps, checking my phone for the time."
    "{i}Three minutes.{/i}"
    "I can make it if I run."
    "I'm halfway across the courtyard when I see him."
    show sam neut at t11
    "Sam's leaning against the fence near the bus stop, scrolling through his phone."
    "Perfect."
    "I slow my pace. Maybe if I hang back, the bus will come and he'll get on without noticing me."
    "But then he looks up."
    show sam neut
    sa "Yo, [player]."
    show sam neut
    "Dammit."
    mc "Sam."
    show sam neut
    sa "Heading home?"
    show sam neut
    mc "That's usually what happens after school."
    show sam neut
    sa "Ha. Fair."
    show sam neut
    "He puts his phone away and walks over. Too casual. Too friendly."
    "I've heard this version of him before."
    show sam neut
    sa "You been good? Haven't seen you around much."
    show sam neut
    mc "Busy."
    show sam neut
    sa "Yeah, I feel that. Finals and all that shit, right?"
    show sam neut
    mc "Right."
    "The bus still isn't here. I check my phone again."
    "Two minutes late."
    "Of course."
    show sam neut
    sa "Hey, you talked to Asa lately?"
    show sam neut
    "There it is."
    mc "She's my sister. I see her every day."
    show sam neut
    sa "Right, yeah. How's she doing? She been good?"
    show sam neut
    mc "Why are you asking me?"
    show sam neut
    sa "Just, you know, checking in. She's been kinda...I don't know, distant lately."
    show sam neut
    mc "Distant."
    show sam neut
    sa "Yeah. Like, I'll text her and she won't respond for hours. Or she'll say she's busy when I try to hang out."
    show sam neut
    "He's looking at me like I'm supposed to sympathize."
    "Like I'm supposed to help him figure out why his girlfriend isn't giving him enough attention."
    mc "Maybe she actually is busy."
    show sam neut
    sa "Maybe. I just...I don't know, man. I feel like she's pulling away or something."
    show sam neut
    mc "And you want me to do what, exactly?"
    show sam neut
    sa "I don't know. Just...if you hear anything, let me know?"
    show sam neut
    "Un-fucking-believable."
    mc "You want me to spy on my own sister for you."
    show sam neut
    sa "What? No, that's not—"
    sa "I'm just saying, if she mentions anything about us, or if something's going on, I'd want to know."
    show sam neut
    mc "If something's going on between you two, that's between you two."
    show sam neut
    sa "Come on, man. We're cool, right? I'm just trying to make sure she's okay."
    show sam neut
    "'Make sure she's okay.'"
    "Like he gives a shit."
    mc "If you're so worried about her, maybe ask {i}her{/i} instead of me."
    show sam neut
    sa "I have. She just says everything's fine, but I know her."
    show sam neut
    "The way he says it. Like he's the victim here."
    "Like Asa's the one being unreasonable."
    mc "Then maybe everything {i}is{/i} fine, and you're overthinking it."
    show sam neut
    sa "Yeah...maybe."
    show sam neut
    "He doesn't sound convinced. He sounds like he's already decided what the problem is and just wants confirmation."
    "The bus finally turns the corner. Thank god."
    show sam neut
    sa "Hey, real talk though—"
    show sam neut
    mc "Bus is here."
    "The doors open with a hiss."
    "I move toward it, but Sam doesn't follow."
    "He stays right where he is, hands in his pockets."
    show sam neut
    sa "Nah. I'll wait."
    show sam neut
    mc "You're not getting on?"
    show sam neut
    sa "Got some stuff to take care of. Catch you later, yeah?"
    show sam neut
    "He pulls out his phone again. Already typing something."
    "..."
    scene bg bus_interior
    show vignette zorder 99:
        alpha 1.0
    with dissolve_scene_half
    "I board the bus and take a seat near the window."
    "Through the glass, I can see Sam still standing there."
    "Still on his phone."
    "The bus doors close. The engine rumbles."
    "My phone buzzes."
    "A text from Asa."
    "\"{i}did you already leave? im still at school and i need a hand{/i}\""
    "I look back out the window."
    "Sam's walking back toward the school."
    "Taking his sweet, beautiful time. Like he has until the heat death of the universe."
    "Like he knew she'd still be there."
    "And that scared me more than anything he said."
    mc "..."
    scene black with dissolve_scene_full
    stop music fadeout 2.0
    pause 2.0
    
    jump dev_scene_manager
    #return #END SCENE

label mc_breaking_point:
    # Late Act 1. MC is at his breaking point, caught between Matsuda's increasingly toxic behavior and the Sam situation affecting both Tsubaki and Asahina. He confides in Monika, one of the few people he still trusts. This scene takes place after the Tsubaki and Sam encounters.
    scene black
    stop music
    pause 2.0
    
    scene bg club_day
    show vignette zorder 99:
        alpha 0.5
    with dissolve_scene_full
    play music hopeless
    "The literature club room is empty. It's after hours, past the time anyone usually stays."
    "I told Matsuda I had to study, and I told Asa I'd be home late for no particular reason."
    "I needed somewhere quiet, somewhere I could just breathe for a minute."
    "The door opens behind me."
    show monika 1a at t11
    m "[player]? I thought everyone left already."
    show monika
    mc "Hey, Monika."
    show monika 1c
    m "You okay? You look awful."
    show monika 1c
    mc "Thanks. Really needed to hear that."
    show monika 1g
    m "I'm serious. When's the last time you slept?"
    show monika 1g
    "I lean back in the chair. When was the last time I actually slept properly?"
    mc "I don't know. Does it matter?"
    "A couple days ago, I think to myself."
    show monika 1f
    m "About?"
    show monika 1f
    mc "Everything. Nothing."
    mc "I don't—I don't even know anymore."
    "Monika pulls up a chair across from me."
    show monika 2c
    m "Talk to me."
    show monika 2c
    mc "..."
    mc "I don't even know where to start."
    show monika 2f
    m "Start anywhere. I've got time."
    show monika 2f
    "..."
    "Where do I even begin?"
    mc "Do you ever feel like you're stuck? Like no matter what you do, you're going to hurt someone?"
    mc "Like there's no right answer?"
    show monika 2g
    m "...Yeah. More than you'd think."
    show monika 2g
    mc "I can't keep doing this, Monika."
    mc "Matsu...she's—"
    "I stop. How do I even explain this?"
    show monika 2c
    m "She's what?"
    show monika 2c
    mc "She's {i}everywhere{/i}. All the time."
    mc "Every text. Every call. Every single plan I try to make that doesn't involve her—she finds a way to be part of it."
    mc "And if I say no, if I try to do {i}anything{/i} for myself, she makes me feel like I'm the bad guy."
    mc "Like I'm hurting her."
    show monika 2f
    m "That sounds exhausting."
    show monika 2f
    mc "It {i}is{/i}."
    mc "But she's my friend. She doesn't mean to—"
    "Do I even believe that anymore?"
    show monika 2g
    m "Does she know she's doing this to you?"
    show monika 2g
    mc "I've {i}tried{/i} talking to her. I've tried setting boundaries—"
    mc "Every time, she acts like I'm abandoning her."
    mc "And maybe—maybe I am. Maybe it's my fault for not—"
    mc "I don't know anymore. I don't."
    show monika 1p
    m "You're not overreacting."
    show monika 1p
    "The certainty in her voice catches me off guard."
    mc "How do you know?"
    show monika 1o
    m "Because I can see what it's doing to you."
    m "You barely talk to anyone else anymore, you're always stressed, your grades are slipping..."
    m "And when's the last time you did something just because {i}you{/i} wanted to?"
    show monika 1o
    mc "..."
    "I don't have an answer."
    show monika 1f
    m "What else is going on?"
    show monika 1f
    mc "It's not just Matsu."
    mc "My sister...she's dating this guy. Sam."
    show monika 1c
    m "I've heard of him. Ladies' man type, right?"
    show monika 1c
    mc "Yeah. That's putting it mildly."
    mc "He's—I don't even know how to describe him."
    mc "He acts like he cares, but everything he does feels like he's playing a fucking game and everyone's just pieces on the board."
    show monika 1g
    m "And Asahina's caught up in it."
    show monika 1g
    mc "Not just her."
    mc "Tsubaki. You remember her?"
    show monika 2c
    m "Matsuda's friend, right?"
    show monika 2c
    mc "Yeah."
    mc "I ran into her the other day. She looked..."
    "I can still see her. The makeup. The exhaustion."
    mc "She looked like she'd given up."
    show monika 2f
    m "Because of Sam?"
    show monika 2f
    mc "He's got his claws in her too. I don't know the full story, but..."
    mc "She's not the same person anymore."
    mc "And Asa—she's starting to pull away from him, I think. But he's not letting go."
    mc "I saw him the other day at the bus stop."
    mc "He asked me to spy on my own sister for him."
    show monika 1p
    m "He {i}what{/i}?"
    show monika 1p
    mc "Said she was being 'distant.' Asked me to let him know if I heard anything."
    mc "Like I'm supposed to be his informant."
    show monika 1r
    m "That's—"
    show monika 1r
    mc "Disgusting? Yeah. I {i}know{/i}."
    mc "And I can't do anything about it cause it's not my life!"
    mc "If I confront him, Asa gets caught in the crossfire. If I tell her, she won't believe me—she {i}likes{/i} him...I think."
    mc "So I just—I just sit there and {i}watch{/i} him tear through everyone like it's nothing!"
    "I bury my face in my hands."
    mc "I'm stuck, Monika."
    mc "Matsu won't let me breathe. Sam's destroying everyone around me. And I can't—"
    "My voice cracks."
    mc "I don't know what to do anymore."
    show monika 2g
    m "..."
    m "[player], look at me."
    show monika 2g
    "I lift my head."
    show monika 2f
    m "Tsubaki's already made her choice. You saw that."
    m "She defended him even after everything."
    show monika 2f
    mc "So what, I just give up on her? Let her further put herself in a damn coffin?"
    show monika 2g
    m "I'm not saying that. But she has to want help first."
    m "And Asahina's smart. She'll figure him out."
    show monika 2g
    mc "But what if she doesn't? What if by the time she does, it's too late?"
    show monika 2g
    m "Then you be there for her when she needs you."
    m "But you're falling apart trying to fix everyone else's problems."
    show monika 2g
    mc "..."
    mc "So what am I supposed to do? Just watch?"
    show monika 1f
    m "As for Matsuda..."
    show monika 1f
    mc "I know what you're going to say."
    show monika 1g
    m "Do you?"
    show monika 1g
    mc "Set boundaries. Talk to her. I've {i}heard it all before{/i}."
    "My voice is rising."
    mc "You think I haven't tried?!"
    mc "Every single time, she makes it about {i}her{/i}. Like I'm the villain for wanting—for needing—five minutes to myself!"
    show monika 1p
    m "Then stop trying to spare her feelings."
    m "Because you're the only one getting hurt here."
    show monika 1p
    "..."
    mc "I don't want to lose her."
    mc "I know that sounds stupid, but I don't."
    show monika 1o
    m "Even if keeping her means losing yourself?"
    show monika 1o
    "I don't answer."
    "I don't know how to."
    show monika 2f
    m "You need to take care of yourself."
    show monika 2f
    mc "I'm just so tired, Monika."
    mc "I'm tired of pretending everything's fine when it's {i}not{/i}."
    mc "I'm tired of—of holding it together when I can barely—"
    "I trail off."
    mc "I don't know how much longer I can keep doing this."
    show monika 2g
    m "I know."
    show monika 2g
    "She reaches across the table and rests her hand on mine."
    show monika 2k
    m "But you're not alone. Okay?"
    m "I'm not going anywhere."
    show monika 2k
    "For the first time in weeks, something in my chest loosens."
    "Not much, but enough."
    mc "...Thanks."
    show monika 1a
    m "Don't thank me yet. I'm making you take a break this weekend."
    m "No Matsuda. No Sam drama. No egos. Heck, no stinky literature club members blowing up your messages."
    m "Plus, Koto said she wanted to chill out too."
    show monika 1a
    mc "I don't know if I can—"
    show monika 3b
    m "Not a suggestion, [player]. You're taking a break."
    m "Even if I have to physically drag you away from your phone."
    show monika 3b
    "I manage a weak smile."
    mc "Alright. Alright."
    show monika 1a
    m "Good."
    show monika 1a
    "We sit in silence for a while. It's not uncomfortable."
    "For the first time in a long time, I don't feel like I have to perform."
    "Maybe it's just hyperbole, but..."
    scene black with dissolve_scene_full
    "Eventually, I leave."
    "The weight's still there."
    "But at least for tonight, I don't have to carry it alone."
    
    stop music fadeout 2.0
    pause 2.0
    
    jump dev_scene_manager
    #return #END SCENE

label dev_mom_cancer_reveal:
    # Chapter 4 test scene. Mom tells MC about her cancer diagnosis after getting enough information to make the fear concrete.
    scene black
    stop music
    pause 2.0

    $ calendar.set_date(2025, 11, 20)
    $ show_calendar()
    scene bg living_room_night
    show mood_night zorder 3
    with dissolve_scene_full
    play music family fadein 2.0

    "The house is too quiet for a Thursday."
    "No television from the living room. No Asahina yelling into her phone. No Mom humming from the kitchen while pretending she does not hum."
    "Just the refrigerator, the wall clock, and the low buzz of lights that are usually drowned out by everyone being alive around them."
    "I toe off my shoes and set my bag by the door."
    mc "I'm home."
    "Mom answers from the living room."
    mom "In here, [player]."
    "Not angry."
    "Not tired, either."
    "That is what makes my hand stay on the strap of my bag a little too long."
    show mom neut at t11
    "She is sitting on the couch with a folder on the table in front of her."
    "White paper. A clipped packet. A pen resting exactly parallel to the edge."
    "Mom organizes bad news like it might behave if the corners line up."
    mc "Am I in trouble?"
    show mom neut
    mom "No."
    show mom neut
    "Somehow that is worse."
    mc "Asa?"
    show mom neut
    mom "Asleep. Volleyball wiped her out."
    show mom neut
    "The clock ticks twice."
    "I can feel both of them."
    show mom neut
    mom "Sit down for me."
    show mom neut
    mc "Can I ask what this is about before I do that?"
    show mom neut
    mom "You can."
    show mom neut
    "She does not answer the question."
    "So I sit."
    show mom neut
    mom "I need to tell you something, and I need you to let me finish before you start trying to solve it."
    show mom neut
    mc "That sentence has never led anywhere good."
    show mom neut
    mom "[player]."
    show mom neut
    "Flat. Gentle."
    "The kind of voice she uses when the joke is allowed to exist, but not allowed to steer."
    mc "...Okay."
    show mom neut
    mom "I was diagnosed with cancer."
    show mom neut
    "The refrigerator stops humming."
    "Or maybe I stop hearing it."
    mc "What?"
    show mom neut
    mom "I was diagnosed with cancer."
    show mom neut
    "She says it the same way the second time."
    "Not softer. Not louder."
    "Like changing the delivery would make it less true, and she refuses to insult either of us by pretending."
    mc "When?"
    show mom neut
    mom "Early November. The first appointment raised enough concern for more tests. The confirmation came last week."
    show mom neut
    mc "Last week?"
    "My voice comes out wrong."
    "Too small for the room."
    mc "You knew last week?"
    show mom neut
    mom "I knew enough to be scared last week."
    mom "I did not know enough to explain it to you."
    show mom neut
    mc "That is not the same thing as not telling me."
    show mom neut
    mom "No. It is not."
    show mom neut
    "She takes the hit without flinching."
    "I hate that more."
    mc "What kind?"
    show mom neut
    mom "A rare subtype."
    mom "Rare enough that the doctors are being careful with their language."
    show mom neut
    mc "What does that mean?"
    show mom neut
    mom "It means there are treatment options."
    mom "It also means they do not have clean numbers for me."
    show mom neut
    mc "Numbers."
    show mom neut
    mom "Survival rates. Fatality rates. Long-term outcomes."
    mom "The sample size is too small for anyone to hand me a percentage that means anything."
    show mom neut
    "I stare at the folder."
    "The pen."
    "The stupid perfect line it makes with the table."
    mc "So they do not know if you are going to die."
    show mom neut
    mom "Nobody knows that about anyone."
    show mom neut
    mc "Mom."
    show mom neut
    mom "I do not know."
    show mom neut
    "There it is."
    "No statistic. No plan. No parental trick where she turns fear into homework and makes it manageable."
    "Just three words sitting between us like a glass on the edge of a table."
    mc "Okay."
    "I nod."
    mc "Okay, so...treatment. What happens next?"
    show mom neut
    mom "We meet with the oncology team next week."
    mom "They want more imaging. They are also looking into whether a specialist outside town has seen enough cases to be useful."
    show mom neut
    mc "Good. Specialist is good."
    show mom neut
    mom "It can be."
    show mom neut
    mc "And you are going to do treatment."
    show mom neut
    mom "Most likely."
    show mom neut
    mc "Most likely?"
    show mom neut
    mom "I am going to make informed decisions with my doctors."
    show mom neut
    mc "That sounds like lawyer wording."
    show mom neut
    mom "It is mother wording."
    mom "Which is worse, because you are contractually obligated to listen to it."
    show mom neut
    "I almost laugh."
    "It dies before it becomes anything useful."
    mc "Does Asa know?"
    show mom neut
    mom "Not yet."
    show mom neut
    mc "You are telling me first?"
    show mom neut
    mom "Yes."
    show mom neut
    mc "Why?"
    show mom neut
    mom "Because you notice things and then decide silence is helpful."
    mom "Because you will try to become very useful very quickly."
    mom "Because I need to tell you, clearly, that your job is not to become a third parent."
    show mom neut
    "My mouth opens."
    "Nothing comes out."
    "That must be answer enough."
    show mom neut
    mom "You can help. You can be scared. You can be angry with me for waiting."
    mom "But you do not get to disappear into responsibility so you can avoid feeling any of it."
    show mom neut
    mc "I was not going to."
    show mom neut
    mom "[player]."
    show mom neut
    "...Right."
    mc "Okay."
    mc "When are you telling Asa?"
    show mom neut
    mom "Tomorrow, after school."
    mom "I want her to sleep tonight."
    show mom neut
    mc "So what do I do until then?"
    show mom neut
    mom "You sleep too."
    show mom neut
    mc "That is optimistic."
    show mom neut
    mom "It is an instruction."
    show mom neut
    "For a second, the old rhythm almost returns."
    "Mom says something impossible with total confidence. I pretend to argue. She wins because she is Mom."
    "Then the folder on the table exists again."
    mc "Are you scared?"
    show mom neut
    mom "Yes."
    show mom neut
    "No hesitation."
    "No armor."
    show mom neut
    mom "I am very scared."
    show mom neut
    "I look down before she can see whatever my face is doing."
    mc "I do not know what to say."
    show mom neut
    mom "You do not have to say the correct thing."
    show mom neut
    mc "There is a correct thing?"
    show mom neut
    mom "Probably not."
    show mom neut
    "She moves the folder aside, clearing the space between us by a few inches."
    show mom neut
    mom "Can you sit with me for a minute?"
    show mom neut
    "It should be an easy request."
    "It is sitting."
    "I have been doing it my whole life."
    "But my legs feel like they belong to someone who has already started running."
    mc "Yeah."
    show mom neut
    mom "Good."
    show mom neut
    "So I sit."
    "The refrigerator starts humming again."
    "Or maybe I start hearing it."
    "Either way, neither of us moves."

    scene black with dissolve_scene_full
    $ hide_calendar()
    stop music fadeout 2.0
    pause 2.0

    jump dev_scene_manager
    #return #END SCENE

label dev_monika_disbands_club:
    # A school day before finals week, near the end of Act 1. Monika tells MC that due to everyone in the literature club graduating, the club will be disbanding as a result.
    scene black
    stop music
    pause 2.0

    $ calendar.set_date(2026, 2, 24)
    $ show_calendar()
    scene bg class_day
    show vignette zorder 99:
        alpha 0.5
    with dissolve_scene_full
    play music twelveam
    "I'm sitting by the window, watching the courtyard. Finals are next week."
    "Monika's at the desk across from me, picking at her lunch."
    "Not something organized this time. She just has a haphazardly thrown together sandwich."
    "She's been quiet today. More than usual."
    show monika 2f at t11
    mc "You good?"
    show monika 2c
    m "Hm? Yeah, I'm fine."
    show monika 2c
    mc "You sure? You've barely said anything."
    show monika 2f
    m "Just thinking."
    show monika 2f
    mc "About?"
    "Monika pauses, contemplative for a moment."
    show monika 1f
    m "Question."
    show monika 1f
    mc "Answer."
    show monika 1c
    m "What are you doing after graduation?"
    show monika 1c
    mc "I mean...college, I guess. Haven't really decided where yet. Got like five places that accepted me."
    mc "Why?"
    show monika 2f
    m "Just curious."
    show monika 2f
    "She goes back to picking at her food."
    "Almost surgically so."
    mc "Monika."
    show monika 2c
    m "...I'm disbanding the club."
    show monika 2c
    "I look at her, mouth slightly agape."
    mc "...What?"
    show monika 2g
    m "The literature club. After graduation, it's done."
    show monika 2g
    mc "Wait, why?"
    show monika 1f
    m "It just makes sense."
    m "Everyone's graduating. Me, you, the others. Literally everybody."
    m "There's no one left to keep it going."
    show monika 1f
    mc "Can't you pass it on to someone? Underclassmen?"
    show monika 1g
    m "To who? We barely had enough people to qualify as a club in the first place."
    show monika 1g
    "She's right. It was always just a handful of us."
    show monika 2f
    m "I thought about it. Tried to recruit more members earlier in the year."
    m "No one was interested."
    show monika 2f
    mc "So that's it? We just...close up shop?"
    show monika 2g
    m "Yeah."
    m "Clubs end. People graduate."
    m "No one's really at fault."
    show monika 2g
    mc "Does everyone else know?"
    show monika 1f
    m "Not yet. I'll tell them next meeting."
    m "But I wanted to tell you first."
    show monika 1f
    mc "Why me?"
    show monika 1a
    m "Because...well..."
    m "I plead the fifth, aha~"
    m "Besides, you really did care about it, even after the indifference all that time ago."
    show monika 1a
    mc "Yeah, well...it was a good place to hide from everything else."
    show monika 1c
    m "Hide?"
    show monika 1c
    mc "You know what I mean."
    show monika 1f
    m "Yeah. I do."
    show monika 1f
    "We sit in silence for a bit."
    "The club always felt like stepping into a pocket dimension. Separate from everything else."
    "It always felt like it would be there."
    "Turns out that was never guaranteed, and maybe I'm an idiot for believing in fairy tales."
    mc "Feels kind of anticlimactic, doesn't it?"
    show monika 2c
    m "What do you mean?"
    show monika 2c
    mc "I don't know. I just thought we'd do more, I guess."
    mc "Make a bigger impact or something."
    show monika 1a
    m "It mattered to us. That's not nothing, right?"
    show monika 1a
    mc "Maybe."
    show monika 1f
    m "You're disappointed."
    show monika 1f
    mc "I mean, yeah. A little."
    mc "It's just...everything's ending, you know?"
    mc "School, the club, people are moving on."
    mc "And I don't know if I'm ready for that."
    show monika 2f
    m "Nobody ever is."
    show monika 2f
    mc "That's not reassuring."
    show monika 1a
    m "I'm not trying to reassure you, I'm being honest."
    show monika 1a
    mc "...Then what about you? What are you doing after graduation?"
    show monika 1c
    m "College. Probably somewhere out of town. Maybe even out of the country."
    m "I did get accepted to a couple good ones, after all."
    show monika 1c
    mc "You sound sure about that."
    show monika 1a
    m "I've been planning it for a while."
    m "Fresh start, you know?"
    show monika 1a
    mc "Yeah. I get that."
    "Another silence."
    mc "So when's the last meeting?"
    show monika 2c
    m "Friday. Nice little closer."
    show monika 2c
    mc "Are we doing anything special?"
    show monika 2a
    m "I was thinking we could just hang out. Read, talk, write, maybe even enjoy some pastries..."
    m "Same as always."
    show monika 2a
    mc "Sounds good."
    show monika 1a
    m "You'll be there, right?"
    show monika 1a
    mc "Yeah. I'll be there."
    show monika 1k
    m "Good."
    show monika 1k
    "She finally takes a few bites of her sandwich."
    show monika 1a
    m "Thanks for understanding, [player]. And of course...thanks for listening."
    show monika 1a
    mc "Yeah. No problem."
    "But it is a problem."
    "The club, high school, 'friendships...' Life as I know it, really."
    "I don't know what comes after."
    "Monika folds the rest of her sandwich back into the wrapper, carefully and deliberately."
    
    scene black with dissolve_scene_full
    "The next period bell rings."
    "Monika packs up her things and leaves almost hastily."
    "I stay behind for a minute, staring out the window."
    "Friday."
    "One more meeting."
    "I add it to my calendar."
    
    stop music fadeout 2.0
    pause 2.0
    
    jump dev_scene_manager
    #return #END SCENE
