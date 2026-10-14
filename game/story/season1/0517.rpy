label a0517:
    # --- Day 3: 2025-05-17 ---
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with dissolve_scene_full
    play music quiz
    "Civics comes easily until I have to keep an opinion to myself. Today, the board has a triangle labeled {i}INDIVIDUAL{/i}, {i}INSTITUTION{/i}, and {i}PUBLIC TRUST{/i}."
    "Beside it, the teacher has written a case about a park closed for repairs that never seem to begin."
    "{i}I've seen that fence. Several fences, actually.{/i}"
    show civics_teacher neut at t11
    civics_teacher "The city has authority to close this park for repairs. That tells us who can make the decision, but it doesn't settle every objection."
    civics_teacher "Residents have been asking for an update for six months. The city keeps sending them a copy of the closure notice."
    civics_teacher "So the question is now: what should the residents ask for next?"
    "A few hands rise while I'm still looking at the handout."
    "The answer seems obvious enough that I forget to put mine up."
    mc "A repair schedule, for a start. Presumably somebody made one before they bought the fence."
    civics_teacher "Interesting..."
    "That word has no business being that dangerous."
    civics_teacher "[player]."
    mc "...Yeah?"
    civics_teacher "Come here for a moment."
    show civics_teacher neut
    "I stand beside the board while the girl at the next desk covers a smile with her hand."
    civics_teacher "[player] can represent the city. Let's give him the information the residents haven't been sent."
    mc "Do I... get a budget?"
    "A laugh breaks somewhere near the back row and dies immediately under the teacher's stare."
    civics_teacher "Page eighty-four. Your budget's been delayed."
    civics_teacher "Answer from what you have there. What can you reopen, and what would you need to check first?"
    mc "The paths can reopen. The playground still needs an inspection, and I don't have a date for that."
    "She draws an arrow from the city to the residents while I read the next paragraph."
    civics_teacher "Good. That's information they can use, even though the repair itself hasn't happened. Now they can ask about the missing inspection."
    "A couple of pencils start moving again. Mine is still on my desk, where I would also like to be."
    show civics_teacher neut at t11
    civics_teacher "Thank you. You can sit down now."
    mc "Can I take the budget with me?"
    civics_teacher "You can raise your hand next time."
    "{i}That would have been cheaper.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The school day thins out."
    call nier_clear from _call_nier_clear_0517_2
    stop music fadeout 1.0
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with wipeleft_scene
    # Busier than the usual operator float: this is the post-bell crush, and a
    # crowd jostles the frame rather than breathing with it.
    play music school_day_a
    # SFX SUGGESTION: The last bell giving way to layered shoe squeaks and a swelling hallway crowd.
    "The corridor fills fast after the last bell. Bags swing and shoes squeak, and the whole school seems to tilt toward the exit at once."
    "I step aside near the windows to check my errands."
    show monika forward uniform happ cm oe nobl rdown ldown at t11
    m forward uniform happ om oe nobl rhip ldown "Escaping already, eh?"
    mc "Attempting to. The building keeps putting people in the way."
    m forward uniform happ cm oe nobl rhip ldown "I won't detain you long, then. No club today, as promised!"
    mc "I'm holding you to that if somebody turns up with a literature review."
    m forward uniform sedu cm oe nobl rdown ldown "Keep that up and I might invite you out again~"
    "She stays beside the window while the crowd works its way around us."
    menu:
        "(Step into it.)":
            $ s1_pick("monika_silence", "into")
            mc "Invited where?"
            m forward uniform lsur cm oe awkw rdown ldown "..."
            m forward uniform nerv cm oe awkw rdown ldown "I haven't got that far. Let me get you to the movie first."
            mc "Planning the sequel already?"
            m forward uniform happ cm ce nobl rdown ldown "Depends on the reviews."
            mc "Uh-huh. Anyway, gotta bounce."
        "(Step around it.)":
            $ s1_pick("monika_silence", "around")
            "I look at my phone instead. The list hasn't changed, but it gives me somewhere else to put my eyes."
            m forward uniform neut om oe nobl rdown ldown "Busy man, I see."
            "She lets the silence close on its own."
            mc "Uh huh."
    show monika forward uniform happ cm oe nobl rdown ldown
    mc "Game first, before they sell my preorder. Then glue for Asa's poster, or I won't hear the end of it."
    m forward uniform nerv om oe blus rdown ldown "Ahhh, yeah, that'll do it. Get going, then. Text me tomorrow morning about the movie?"
    mc "Yeah. I've even set a reminder. Proud of me yet?"
    m forward uniform happ cm ce nobl rdown ldown "Mhm. Go buy your stuff, [player]."
    show monika at thide
    hide monika
    "She steps back into the flow of students, clipboard against her chest."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I leave school among the Saturday survivors. The crowd thins by the station, then again by the shopping street."
    call nier_clear from _call_nier_clear_0517_3
    pause 2.0
    scene bg store_techsection
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    "The supermarket is holding a release-day crowd together through sheer queue discipline."
    "There's a line at the counter, a line near the case, and a third line pretending to browse accessories."
    "I get my copy in ten minutes, somehow. Only one argument breaks out over whether a preorder receipt counts without the email confirmation."
    "The craft aisle is quiet enough to hear its ceiling speaker. I get the larger glue bottle, which costs barely more than the one beside it."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg store_checkout
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    "Kotonoha is at the register when I get there."
    show kotonoha work neut at t11
    mc "Afternoon."
    ko "Good afternoon."
    "She scans the game, turns the case over to check the security sticker, then sets it into a separate bag before the glue gets anywhere near it."
    ko "Your receipt will be in this first bag, if that's alright."
    mc "Yeah, that's fine. Appreciated."
    "She tests the glue bottle's cap before bagging it."
    ko work neut "The cap is loose on that brand sometimes."
    "It turns another half rotation under her fingers."
    mc "Oh, uh... good catch."
    ko work neut "It happens."
    show kotonoha work pose_exact_fold
    "She folds the receipt exactly down the middle as it comes out of the register."
    show kotonoha work neut
    ko "Have a good day."
    mc "You too."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg home_entry_day
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    play sound moddooropen
    show asahina neut at l11
    "Asahina meets me at the door with a strip of masking tape stuck to her sleeve."
    mc "You started without me, I see."
    ah annoyed "Yeah, I'm not letting you anywhere near my precious poster."
    show asahina happy at t11
    "I hand over the bottle, which she turns around to check the label before holding it against the light."
    ah "...Yeah, this works."
    mc "Glowing praise."
    show asahina embarrassed
    ah "Shush."
    mc "Oh, and before you ask, no, I didn't restock my own snacks for you."
    show asahina unamused
    ah "Oh my God, I said I'd handle it, didn't I?"
    ah "Go play your RPG slop or whatever."
    mc "After homework. Still got responsibilities, ya know?"
    show asahina teasing
    ah "Wow... Mom really has brainwashed you."
    mc "...You realize she raised you too, right?"
    show asahina at thide
    hide asahina
    "Asahina snorts and takes the glue back to the living room, where the floor beneath the couch is almost entirely paper and sequins."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I take my things upstairs and set my new glorified collector's item beside the console, still sealed."
    nier "Once the laundry's out of the dryer and folded in the laundry room basket, I get out my notes while Asahina's cutting and muttering carry up from downstairs."
    call nier_clear from _call_nier_clear_0517_5
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    "I finish the literature reading that can be finished quickly, then stare at the document analysis that cannot."
    "Eventually, I move that one to Monday's problem pile, where it joins several other things I'm pretending are organized."
    "A message from Monika comes in around the time the house starts to quiet down."
    python:
        _phone_messages = [
            phone_msg("them", "Oh hey, meant to tell you, they finished renovation at the library downtown!"),
            phone_msg("them", "We should go sometime! I want to see if they kept the window seats."),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0517_1
    "I check the opening hours before answering. Next Sunday looks possible, assuming exam preparation leaves us any time."
    python:
        _phone_messages = [
            phone_msg("me", "I'm in. I want to know where they moved the old movies."),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0517_2
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "By evening, the house has cooled into its usual rhythm."
    nier "While Mom brings the laundry by our bedroom doors, Asahina measures the same corner of poster board three times and starts blaming the ruler."
    nier "After dinner, I leave her to it and step outside to stretch my legs."
    call nier_clear from _call_nier_clear_0517_6
    stop music fadeout 1.0
    pause 2.0
    scene bg house_night
    $ show_calendar()
    $ atmos("night", particles="nightdrift")
    with wipeleft_scene
    play music night_a
    "I sit on the step with my elbows on my knees while dishes clatter through our kitchen window. Across the street, someone wheels a bicycle through a gate."
    "Once the stiffness eases out of my shoulders, I take the sidewalk and decide to go as far as the next corner."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg residential_night
    $ show_calendar()
    $ atmos("night", particles="nightdrift")
    with wipeleft_scene
    "Curtains glow beside a vending machine that steals half the sidewalk. Somewhere ahead, two voices overlap: one low and careful, the other pitched to carry."
    "The louder speaker is walking backward, facing her companion as both hands sketch out every sentence. The quieter one keeps a hand hovering near her sleeve."
    "My phone buzzes. I glance down for one step while the gap closes from both directions."
    stop music fadeout 1.0
    "...and we run out of sidewalk."
    # TODO: Insert sidewalk collision CG here when the dedicated asset is available.
    # SFX SUGGESTION: A blunt shoulder impact with a brief phone-and-clothing fumble.
    play sound fall2
    $ fx_shake_screen(14.0, 0.6)
    $ ma_name = "Red Girl"
    $ ts_name = "Meek Girl"
    "My shoulder catches the red-haired girl's chin before we knock into each other properly. We stagger apart, and I trap my phone against my chest."
    ts "Omigosh, we're sorry--{w=1.0}{nw}"
    ma "Woah! Sorry there, pal--{w=1.0}{nw}"
    mc "Ah! Sorry, I wasn't--{w=1.0}{nw}"
    show matsuda casual worried at t21
    show tsubaki shocked at t22
    "The girl in front of me catches herself with one white-gloved hand against a fence post."
    "She winces and rubs the side of her jaw while I check that my phone screen survived."
    show matsuda smug
    "By the time I look up, she has straightened and thrown her shoulders back."
    "{i}Hold up. The girl at the vending machine?{/i}"
    "Her red ponytail has a braid down one side, and her die earring keeps swinging even after she holds still."
    play music theme_matsuda_a
    # May 17: courtly, chivalric traveler. Her ceremonial posture and language
    # turn the collision into a parley; May 19's bard is a different performance.
    # The performance idle remains active, with ordinary teenage breaks beneath it.
    show matsuda casual pose_laughing
    ma "Ahahaha! A bold challenge, traveler! Yet let us have peace, for the road is narrow and I have no wish to meet that fence a second time!"
    "The other girl brings her paper bag back against her chest now that we're both standing. Her chestnut hair flows back and forth."
    "Her hand pats the shoulder of her companion, as if she's considerately padding off nonexistent dirt from her blue jacket."
    "The chestnut-haired girl then faces me."
    show tsubaki panicked
    ts "A-Are you hurt? There's a shop right here if you need ice!"
    mc "I'm fine, thanks. Ow... mostly fine. Caught a chin with my shoulder..."
    mc "Is, uh, is your sister okay, though?"
    "The red-haired girl stops rubbing her jaw."
    show matsuda casual curious
    ma "...Her what?"
    show tsubaki nervous
    ts "Oh, uh... Haha, she's not--"
    "{i}Here we go...{/i}"
    show matsuda annoyed
    ma "Sister?! Nay, sir! You have joined two households on remarkably little evidence!"
    $ ts_name = "Tsubaki"
    show matsuda determined
    "She puts a gloved hand over her heart and presents the other girl with a sweep that sends one earring against her cheek."
    ma "This is Tsubaki Kareda, my sworn companion: keeper of our provisions, counsel against my enemies, and counsel against me when no enemies are available!"
    show tsubaki unamused
    ts "You can just say friend."
    show matsuda smug
    ma "And strip you of your titles? My comrade, I would not treat a faithful companion so poorly!"
    show tsubaki embarrassed
    "Tsubaki gives me a small, mortified bow."
    ts "I am {i}so{/i} sorry... I tried to get her to turn around before we hit you."
    mc "Hey, don't fret, I wasn't looking either. I think we both earned that one."
    ma "Spoken honorably! Half the blame to each of us, and let no feud nor plague o' both our houses!"
    "The red-haired girl rubs her chin again, then plants one foot ahead of the other and bows, keeping her sore chin high throughout."
    $ ma_name = "Matsuda"
    show matsuda smug
    show tsubaki neut
    ma "I am Matsuda Akai. You have my word that no vengeance shall follow you home, provided you grant me what and wherefore art thou called."
    mc "...[player]. You have my word, mainly because I don't think I'd survive a rematch... probably."
    show matsuda thinking
    ma "[player]..."
    show matsuda curious
    ma "OOOOOOOOOHHHHHH! Literature club, right?!"
    mc "Yeah...?"
    show matsuda happy
    ma "Aha! An envoy from Lady Monika's court, where even the least defensible feelings receive a hearing! I knew I had seen your face from mine scholarly realm."
    mc "You got all that from... being shoulder-checked?"
    show matsuda smug
    ma "A roaring knight must know the neighboring courts, lad. No banner passes these eyes unmarked, no stranger crosses my path unremembered!"
    show tsubaki teasing
    ts "Translation: she saw you talking to Monika after school. We were by the stairs or something like that."
    show matsuda annoyed
    ma "Tsubaki, I beseech you, let me keep {i}one{/i} secret from the neighboring court. You're killing me here."
    mc "Sorry. Again. I was on my phone, thinking about a game I haven't opened."
    show matsuda shocked
    ma "You bought a new game and left the house without opening it...?"
    show matsuda unamused
    "Her eyes narrow as if I just slid evidence across a table."
    mc "I wanted some air before I lost the evening to it."
    show matsuda determined at h21
    "She takes a quick step back and raises one hand as though I'm about to confess to something worse."
    ma "Good sir! A kingdom awaits your aid, its gates stand open, and you have left its people to fend for themselves while you take the evening air?"
    show tsubaki unamused
    ts "Hey, {i}you{/i} asked me to drag you outside because you'd been on your computer all afternoon."
    show matsuda smug
    ma "For provisions! An army must be fed before it marches, and the army was me, and I was really friggin' hungry!"
    show tsubaki neut
    "Tsubaki presses her lips together into a thin smile, but a laugh escapes through her nose while Matsuda tries to look offended."
    ma casual curious "Wait. Which game is it?"
    mc "The new RPG, the one with the press-turn combat. So far I can confirm that the case is rectangular."
    ma casual shocked "Hoooooly shit, you found a copy?! The damn thing sold out online while I was in class!"
    ma casual determined "Then ride ahead and send word! Tell me whether the kingdom is worth the toll before I spend tomorrow hunting down a copy."
    mc "You trust sidewalk-collision reviews, I take it?"
    ma casual smug "You held your ground after a grievous blow. I shall trust your account of a tutorial."
    mc "I mostly staggered backward. Your standards are generous."
    mc "Look, I should probably--"
    show matsuda casual happy
    ma "Stay, traveler! Our truce lacks a means of sending messages, and I refuse to hunt you down by coat of arms!"
    mc "..."
    "I had meant to go home, but she has her phone out before I can get to that part."
    show tsubaki embarrassed
    ts embarrassed "He was trying to say something..."
    "Matsuda looks back at me with her thumb still on the screen."
    show matsuda determined
    "She presents the phone flat on one gloved palm, using the other hand to flourish over the screen."
    ma "[player]! Will you give me leave to send a messenger? No horse required, no herald waking the household, merely this humble device and perhaps a review or three."
    show tsubaki worried
    ts "She means--if you're okay with it. You don't have to."
    show matsuda unamused
    ma "I asked his leave! With witnesses and an open hand, as courtesy demands!"
    mc "You ask everyone you crash into for their number?"
    show matsuda teasing
    ma teasing "Only those who survive the encounter and possess knowledge of distant lands. Your rectangular case qualifies."
    mc "...You're getting a text, not a scroll. I want that understood."
    "She holds up the contact screen, shaking it in her palm as if beckoning me like a dog."
    menu:
        "(Grudgingly.)":
            $ s1_pick("matsuda_contact", "brisk")
            mc "...Fine. But if this becomes a group chat called 'Depresso Espressos,' I'm out."
            ma "Your objection shall be entered in the treaty, beside my objection to that name!"
        "(Play along.)":
            $ s1_pick("matsuda_contact", "wry")
            mc "I accept, provided fate covers my medical expenses."
            show matsuda happy
            ma "Alas, fate's treasury is empty! I can offer you safe passage to the corner and the goodwill of this noble company."
            show tsubaki unamused
            ts "Maybe let him get to the corner by himself."
        "(Just hand it over.)":
            $ s1_pick("matsuda_contact", "warm")
            "When I hand her my phone, she has to transfer her own to her other hand before she can take it."
            show matsuda thinking
            ma "...Hm."
            show matsuda smug
            ma "So readily offered! You place great faith in my honor, traveler."
            show tsubaki smug
            ts "She had a speech ready. A long, LONG one."
            show matsuda unamused
            ma "'Twas more like an oath. I already practiced the hand thing."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "While we exchange numbers, Tsubaki rests her bag on the low wall and flexes the hand that's been carrying it."
    call nier_clear from _call_nier_clear_0517_6half
    pause 2.0
    scene bg residential_night
    $ show_calendar()
    $ atmos("night", particles="nightdrift")
    show matsuda casual smug at t21
    show tsubaki neut at t22
    with wipeleft_scene
    "My phone buzzes a moment later."
    python:
        _phone_messages = [
            phone_msg("them", "For the record, I survived."),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, status="New Contact", append=True) from _call_phone_text_conversation_0517_3
    "Matsuda is watching over the top of her phone when I look up, smiling before I've even answered."
    mc "...Congratulations."
    show matsuda teasing
    ma "Your kind words shall sustain me through the long journey home!"
    show tsubaki worried
    ts "Matsuda, we should really get going. I'm supposed to be home by nine."
    show tsubaki embarrassed
    ts "And I'm the one carrying dinner."
    show matsuda unamused
    ma "Very well. Even a sworn companion must answer to her household."
    show matsuda happy
    "She draws herself upright and offers me a final, solemn inclination of the head."
    ma "Fare thee well, [player]! Our truce holds beyond this meeting, and I shall await news of your campaign!"
    show matsuda teasing
    ma "Should fate trouble you again, you know where to send the complaint."
    mc "...Fate can text, apparently."
    show matsuda happy
    ma "Indeed! The royal messengers have modernized, and the horses are delighted!"
    # SFX SUGGESTION: A sharp paper-bag crinkle punctuating Matsuda's sudden turn.
    show matsuda at t31
    show tsubaki embarrassed at t33
    "Matsuda's sleeve catches the paper bag when she turns. Tsubaki shifts it to her other arm before giving me a smaller bow."
    ts "I can't apologize enough for the run-in... Please just ice your shoulder."
    mc "Will do. Nice meeting you, Tsubaki."
    show tsubaki happy
    ts "You as well!"
    show matsuda at thide
    hide matsuda
    show tsubaki at thide
    hide tsubaki
    "They head toward the vending machine, Matsuda already talking with both hands while Tsubaki adjusts her pace to keep the bag from swinging."
    python:
        _phone_messages = [
            phone_msg("them", "Btw if the game is good, lie and say it's dogshit until I buy my copy."),
            phone_msg("me", "Terrible. Historically bad. So bad I haven't even opened it yet."),
            phone_thumb("them"),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, status="New Contact", append=True) from _call_phone_text_conversation_0517_4
    mc "..."
    mc "What the hell just happened?!"
    $ mark_character_met("matsuda")
    $ phone_mark_contact_met("matsuda")
    $ mark_character_met("tsubaki")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I turn home at the next corner with a sore shoulder and nine percent left on my phone. That should get me as far as the charger."
    call nier_clear from _call_nier_clear_0517_7
    stop music fadeout 1.0
    pause 2.0
    scene bg living_room_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music night_a
    play sound moddooropen
    "Asahina is on the living room floor amid poster board and paper cutouts. A glued corner has curled up while she wasn't looking."
    show asahina frustrated at t11
    "As I pass her, my phone lights up with its low-battery warning. She follows it with her eyes, then looks at my face."
    show asahina curious
    ah "You look weird."
    mc "Hello to you too, farthead."
    show asahina smug
    ah "No, seriously. That's your trying-not-to-smile face."
    "I put the phone facedown against my thigh."
    mc "I may or may not have bumped into someone while getting fresh air."
    ah "Name?"
    mc "Matsuda."
    "Asahina repeats the name under her breath."
    ah "Red hair? Obnoxious as heck?"
    mc "Oh, you know her?"
    show asahina disgusted
    ah disgusted "{i}E-VER-Y-ONE{/i} knows of her! She's a dingus who performs everything at max volume and somehow sucks at half of it."
    show asahina nervous
    ah "...Or, at least, that's what my friends say. I dunno her personally."
    "She goes back to pressing the corner of the cutout down while I wait for the rest. There isn't any."
    mc "...Uh-huh."
    show asahina teasing
    ah "Soooo did she give you her number, her address, her exact IP, all that good stuff?"
    mc "She wanted to know about the game, weirdly enough. It's not exactly a proposal, but it is what it is."
    ah "Pfft, whatever helps you sleep, bro."
    "She presses another cutout onto the poster, then smooths it flat under her palm."
    show asahina thinking
    "The lettering is annoyingly good, especially the curve she has worked around the ball. She catches me looking and covers it with her hand."
    mc "It's coming along, I see."
    show asahina smug
    ah "Don't change the subject just because I'm the most talented person in the world."
    mc "...I'm going upstairs."
    show asahina unamused
    ah "Just say if you don't want her texting you. You know you're allowed, right?"
    mc "I can manage a conversation, Asa."
    show asahina teasing
    ah "You can barely manage this one!"
    show asahina neut at thide
    hide asahina neut
    "I take the stairs and leave the argument where it is, as her laugh follows me halfway up."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Mom checks in twice. On the second pass she praises the poster, and Asahina realigns the same letter for the next five minutes."
    nier "A fresh bag of chips appears outside my door afterward, wearing a strip of leftover masking tape that reads {i}\"DEBT SETTLED. DO NOT GET EMOTIONAL\".{/i}"
    call nier_clear from _call_nier_clear_0517_8
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    "The game waits by the console, still sealed, and me honestly too lazy and too tired to do anything about it."
    "On my phone, Monika's movie reminder sits beneath a contact I saved less than an hour ago."
    "{i}I can just... pretend that one doesn't exist, yeah?{/i}"
    "I leave both threads unopened and let the screen dim."
    "My shoulder aches when I reach for the charger, so I move the phone closer and set tomorrow's alarm."
    "The reminder list opens behind it, with Saturday's last item still unchecked."
    "{i}School. Game. Glue. Tomorrow, Monika.{/i}"
    "{i}That was everything... right?{/i}"
    "I pull the planner out to see what I've missed."
    "{i}MAYBE: Look at that school with Mom.{/i}"
    mc "..."
    mc "Ah, SHIT!"
    mom "[player]?! Everything okay up there?!"
    mc "YEAH! JUST A MINOTAUR KICKING MY BUTT!"
    $ update_character_thought("matsuda", "Matsuda Akai transferred in this year, and everyone seems to know of her without actually knowing her. She took my contact info after a sidewalk collision and texted before I reached the corner.")
    $ update_character_thought("tsubaki", "Tsubaki Kareda offered to get ice after the collision, then explained where Matsuda had actually seen me. She's quieter than her friend, but she got us out of the introductions before dinner went cold.")
    $ hide_calendar()
    stop music fadeout 2.0
    scene black with dissolve_scene_full
    call calendar_advance(days=1) from _call_calendar_advance_0517_1
    jump a0518
