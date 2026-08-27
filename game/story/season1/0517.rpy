label a0517:
    # --- Day 3: 2025-05-17 ---
    pause 2.0
    scene bg home_entry_day
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music dailyleisure
    window auto
    "Saturday morning doesn't happen at the table. It happens by the door, one shoe half-tied and one hand searching my bag for a pen I am reasonably sure I never owned."
    show mom neut at t22
    show asahina uniform frustrated at t21
    "Asahina crouches near the shoe rack, working on the heel of her loafer like it's emergency surgery."
    mom "Lunch is in your bag. Eat the toast before you get to school, not during first period."
    mc "Bold to assume first period doesn't deserve toast."
    show asahina uniform unamused
    ah "Saturday doesn't owe you squat."
    "Her tone could press wrinkles out of a shirt."
    show mom unamused
    mom "How many times have we started school again? Put your big boy pants and your big girl pants on."
    mc "Survival isn't consent, you know..."
    "Mom gives me the look she reserves for sentences she chooses not to dignify."
    mom neut "The two G's, glue and game. You wrote it down?"
    mc "On my phone and in the homework folder in my brain."
    show asahina uniform teasing
    ah "Totally a healthy thing, by the way."
    "My sister props herself back on her feet and catches my sleeve on the way past, one finger already up."
    show asahina uniform pose_pointing
    ah "The glue isn't optional, and don't cheap out and get the tiny bottle! They gave me a bigger poster board than I thought."
    mc "Oh, so you started it?"
    show asahina uniform smug
    ah "It's called recon, thank you muchas sumimasen!"
    mc "...Do you even know what you said?"
    show mom teasing
    "Mom smiles into her coffee, and Asahina sees it and immediately looks away."
    show asahina uniform embarrassed
    mc "...Medium bottle, then."
    ah neut "Large if it's cheap."
    mc "Your supply demands know no bounds..."
    # SFX SUGGESTION: One crisp finger snap, close and dry.
    show mom determined
    "Mom snaps her fingers and gestures out the door."
    mom "Go. Both of you."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Asahina and I take our time leaving, despite Mom's best efforts. I follow behind her with toast in one hand and my bag over one shoulder."
    play sound moddoorclose
    call nier_clear from _call_nier_clear_0517_1
    stop music fadeout 1.0
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with dissolve_scene_full
    play music quiz
    "Civics always feels easy. Familiarity can pass for safety if you stop looking."
    "The teacher has drawn a triangle across the board, each point labeled in clean block letters: {i}INDIVIDUAL{/i}, {i}INSTITUTION{/i}, {i}PUBLIC TRUST{/i}."
    "{i}Society of laws and all that...{/i}"
    show civics_teacher neut at t11
    civics_teacher "A rule is not automatically legitimate because someone wrote it down."
    civics_teacher "Legitimacy depends on whether people believe the institution has earned the authority it exercises."
    "I write that down, then underline {i}earned{/i} because it sounds like it warrants a short response on the exam."
    civics_teacher "So when someone says, rules are rules, what question should follow?"
    "A few hands rise. Mine does not, because I am capable of growth."
    "My mouth, unfortunately, is still on a separate development schedule, and my eyes roll on their own."
    mc "Whether the rule is doing anything useful, or whether someone just came up with a bad idea."
    civics_teacher "Interesting..."
    "That word has no business being that dangerous."
    civics_teacher "[player]."
    mc "...Yeah?"
    civics_teacher "Come here for a moment."
    show civics_teacher neut
    "I stand beside the board while the class performs the sacred ritual of pretending not to enjoy this."
    civics_teacher "Everyone, [player] is going to help us model the relationship between civic authority and public compliance."
    mc "Do I get qualified immunity?"
    "A laugh breaks somewhere near the back row and dies immediately under the teacher's stare."
    civics_teacher "You get accountability. Hold it carefully."
    "The teacher hands me a textbook and points to the center of the triangle. I hold the unexpectedly heavy book to my chest."
    civics_teacher "Institutional authority here. Individual rights here. Public trust here."
    civics_teacher "A society can tolerate imperfect rules for a while, but tolerated is not the same as trusted."
    "She draws one more arrow, slower than the others."
    civics_teacher "If authority relies only on compliance, it becomes brittle. If it earns trust, it becomes durable."
    "A couple of pencils start moving again. Mine, abandoned on my desk, does not."
    show civics_teacher neut at t11
    civics_teacher "Thank you. You can sit down now."
    mc "...Why did I have to do that again?"
    civics_teacher "Answering disrespectfully has consequences."
    "{i}At least I wasn't wrong.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The school day thins out without improving."
    call nier_clear from _call_nier_clear_0517_2
    stop music fadeout 1.0
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with wipeleft_scene
    # Busier than the usual operator float: this is the post-bell crush, and a
    # crowd jostles the frame rather than breathing with it.
    play music schooldays
    # SFX SUGGESTION: The last bell giving way to layered shoe squeaks and a swelling hallway crowd.
    "The corridor fills fast after the last bell. Bags swing and shoes squeak, and the whole school seems to tilt toward the exit at once."
    "I step aside near the windows to check my errands before the crowd can carry me past my own plans."
    show monika forward uniform happ cm oe nobl rdown ldown at t11
    m forward uniform happ om oe nobl rhip ldown "Escaping already, eh?"
    mc "Attempting to. The building keeps putting people in the way."
    m forward uniform happ cm oe nobl rhip ldown "I won't detain you long, then. No club today, as promised."
    mc "A president who honors a day off. Rare discipline, gotta give you credit for that."
    m forward uniform sedu cm oe nobl rdown ldown "Careful. Compliments like that might get you invited somewhere."
    "She says it lightly, then leaves the silence sitting between us."
    menu:
        "(Step into it.)":
            $ s1_pick("monika_silence", "into")
            mc "Invited where?"
            m forward uniform lsur cm oe awkw rdown ldown "..."
            m forward uniform nerv cm oe awkw rdown ldown "Nowhere yet. I just like having the option on the table."
            mc "That's a terrifying amount of forward planning."
            m forward uniform happ cm ce nobl rdown ldown "It's the only kind I do."
            mc "Uh-huh. Anyway, gotta bounce."
        "(Step around it.)":
            $ s1_pick("monika_silence", "around")
            "I look at my phone instead. The list hasn't changed, but it gives me somewhere else to put my eyes."
            m forward uniform neut om oe nobl rdown ldown "Busy man, I see."
            "She lets the silence close on its own."
    show monika forward uniform happ cm oe nobl rdown ldown
    mc "Store for a game before it sells out, then glue for Asa's poster. My household is governed by...specific grievances."
    m forward uniform nerv om oe blus rdown ldown "Then I won't interfere with domestic diplomacy. Text me tomorrow morning about the movie?"
    mc "Yeah. Morning...provided I wake up on time."
    m forward uniform happ cm ce nobl rdown ldown "Mhm. Go buy your stuff, [player]."
    show monika at thide
    hide monika
    "She steps back into the flow of students, clipboard against her chest."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I leave school among the Saturday survivors. The crowd thins by the station, then again by the shopping street, until the day finally feels like it belongs to people who chose to be outside."
    call nier_clear from _call_nier_clear_0517_3
    pause 2.0
    scene bg store_techsection
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    "The supermarket is holding a release-day crowd together through sheer queue discipline."
    "There's a line at the counter, a line near the case, and a third line made of people pretending they are browsing accessories while clearly watching the stock behind the glass."
    "I get my copy in ten minutes, somehow. Only one argument breaks out over whether a preorder receipt counts without the email confirmation."
    "The craft aisle is quieter. I grab a larger bottle of glue than Asahina asked for because it's shockingly cheap."
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
    mc "Appreciated."
    "She points and wiggles her finger at the glue bottle."
    ko work worried "The cap is loose on that brand sometimes."
    "She tightens it the same way someone else might straighten a crooked picture frame."
    mc "Oh, uh...good catch."
    ko work neut "It happens."
    show kotonoha work pose_exact_fold
    "The register prints the receipt. She folds it once, exactly down the middle."
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
    mc "You started without me."
    show asahina annoyed
    ah "I started without the most important part. That's not the same thing."
    show asahina happy at t11
    "I hand over the larger bottle. She checks the label twice, and one corner of her mouth gives her away."
    ah "...Yeah, this works."
    mc "Glowing praise."
    show asahina embarrassed
    ah "Shush."
    "She turns the bottle over once, then tucks it beside the poster board among her supplies."
    mc "And before you ask, no, I didn't restock my own chips for you."
    show asahina unamused
    ah "I said I'd handle it, didn't I?"
    ah "Go play your RPG slop or whatever."
    mc "After homework. Still got responsibilities, ya know?"
    show asahina teasing
    ah "Wow...Mom really has brainwashed you."
    mc "...You do realize you were also raised by her, right?"
    show asahina at thide
    hide asahina
    "Asahina snorts, then retreats toward the living room. The poster remains classified."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I take the game upstairs and set it beside the console, still sealed."
    nier "The afternoon goes to chores and notes. Downstairs, Asahina's arts-and-crafts feud rustles on."
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
            phone_msg("them", "We're totally hanging out or studying there sometime. I'll hold you to it!"),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0517_1
    "I leave it unanswered for a minute, mostly because I can hear her smug little smile through the punctuation."
    python:
        _phone_messages = [
            phone_msg("me", "Roger wilco."),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0517_2
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "By evening, the house has cooled into its usual rhythm."
    nier "Mom checks the laundry. Asahina measures the same corner of poster board three times and mutters something that sounds like a personal grudge against rulers."
    nier "I step outside with every household argument still unresolved."
    call nier_clear from _call_nier_clear_0517_6
    stop music fadeout 1.0
    pause 2.0
    scene bg house_night
    $ show_calendar()
    $ atmos("night", particles="nightdrift")
    with wipeleft_scene
    play music fantasypassion
    window auto
    "I sit on the step with my elbows on my knees, listening to the loose click of a bicycle wheel somewhere across the street and the faint clatter of dishes through our kitchen window."
    "I stand and work the stiffness out of my shoulders, then take the sidewalk with no plan beyond moving until boredom loses interest."
    $ hide_calendar()
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
    $ ma_name = "Red Girl"
    $ ts_name = "Meek Girl"
    "My shoulder hits someone else's. Both of us stagger in the opposite direction and my phone nearly leaves my hand."
    ts "Omigosh, we're sorry--"
    ma "Woah! Sorry there, pal--"
    mc "Ah! Sorry, I wasn't--"
    show matsuda casual worried at t21
    show tsubaki shocked at t22
    "The girl in front of me catches herself with one white-gloved hand against a fence post."
    "For a moment, she only winces. One hand presses the shoulder that took the hit while her eyes sweep down the arm and back up."
    show matsuda smug
    "Then she straightens and throws her shoulders back, turning the recovery into something suspiciously rehearsed."
    "Red hair in a high ponytail, braided down one side. Her earrings are still swinging from the impact."
    play music enterm
    # The bounce is Matsuda's PERFORMANCE idle, and it is load-bearing all the
    # way to May 19: the bard is on while it runs, and the moment she drops the
    # act she goes to fx_still. Nothing else in the cast bounces.
    show matsuda casual pose_laughing
    ma "Ahahaha! Fate introduces itself with blunt force! Crude, but effective."
    "The other girl's chestnut hair is nearly the same shade as mine, which buys it a second look. She almost tosses her paper bag aside to catch whichever of us falls first."
    show tsubaki panicked
    ts "A-Are you hurt?! Do you need ice?!"
    mc "No, no... I'm fine... Hoo boy, okay, that does kinda smart... Why do chins leave such a mark...?"
    mc "Is your sister okay, though?"
    "The temperature changes immediately."
    show matsuda casual curious
    ma "...Her what?"
    show tsubaki nervous
    ts "Oh, uh, she's not--"
    "{i}Here we go...{/i}"
    show matsuda annoyed
    ma "Sister?! Do I look like I travel with understudies?!"
    $ ts_name = "Tsubaki"
    show matsuda determined
    ma "With all due respect--and I am generously inventing the respect as we speak--this is Tsubaki Kareda: confidante, witness, occasional conscience, and chronic apologizer!"
    show tsubaki unamused
    ts "...Friend is shorter."
    show matsuda smug
    ma "Shorter, yes, albeit far less accurate."
    show tsubaki embarrassed
    "Tsubaki gives me a small, mortified bow."
    ts "I'm so sorry about her. She gets worse sometimes..."
    mc "...That's worse?"
    ma "'Twas restraint, my good chap."
    "She says it with such total conviction that I almost apologize to the concept of restraint."
    "The red-haired girl clears her throat into one fist and presents Tsubaki with the other hand."
    $ ma_name = "Matsuda"
    show matsuda unamused
    show tsubaki neut
    ma "Fine. I, Matsuda Akai, forgive the collision on grounds of mutual negligence and...somewhat decent reflexes."
    mc "...[player]. And for the record, my reflexes were mostly panic, okay? It was...what's that term again...a robin response, or whatever it's called."
    show matsuda thinking
    ma "[player]..."
    show matsuda curious
    ma "Literature club, right?"
    mc "Yeah...?"
    show matsuda happy
    ma "I knew it! You don the posture of someone who has been told against his will to expunge his deepest, darkest feelings with four movable desks."
    mc "You got all that from...being shoulder-checked?"
    show matsuda smug
    ma "I am observant under pressure, lad. Mine eyes never forego glimpses into the myriad realities of my peers!"
    show tsubaki teasing
    ts "Translation: she saw you with Monika after school."
    show matsuda annoyed
    ma "Tsubaki, please. Let the mystique breathe and, uh...don't be a freaking buzzkill."
    mc "Well, again, and hopefully for the last time, sorry. I was checking my phone and thinking about how long I could not play a game I bought today."
    show matsuda shocked
    ma "You bought a new game and left the house without opening it...?"
    "Her eyes narrow as if I just slid evidence across a table."
    mc "It seemed healthier than giving in to insomnia."
    show matsuda determined at h21
    ma "My good sir! Healthy choices are where stories go to die!"
    show tsubaki unamused
    ts "You...literally told me to stop you from buying an extra large pizza for dinner."
    show matsuda smug
    ma "'Twas nutritional compromise! Let us not mince semantics!"
    show tsubaki happy
    "Tsubaki's mouth twitches and loses the fight. The laugh comes out through her nose."
    ma casual curious "Wait. Which game did you buy?"
    mc "The new release everyone was fighting over. I haven't opened it, so my review begins and ends at 'the case is rectangular.'"
    ma casual shocked "You found a copy?! Mine sold out while I was in class."
    ma casual determined "Then I require your verdict before I waste tomorrow hunting one down!"
    mc "You trust sidewalk-collision reviews?"
    ma casual smug "You bought it and left it sealed. I respect restraint in a critic!"
    mc "The restraint mostly produced bruising."
    "Keeping up stopped being an option ten seconds ago. The conversation is now a parade moving past me."
    show tsubaki embarrassed
    ts embarrassed "...Please don't encourage her."
    "Matsuda has already pulled out her phone."
    show matsuda determined
    "She plants her feet and points at me as if she's offering a duel."
    ma "[player]! I not-so-humbly request your contact information."
    show tsubaki worried
    ts "She means, if you're okay with it. You don't have to."
    show matsuda unamused
    ma "Yes, yes, manners and civilization. I was {i}approaching{/i} the polite version, with more grand pacing."
    mc "You ask everyone you crash into for their number?"
    show matsuda teasing
    ma teasing "Only the ones who recover well and owe me a game review. The lineage insult is a bonus."
    mc "What the hell are you even...huh...?"
    "She tips her chin toward the phone and wiggles it beside her cheek, beckoning me like a dog."
    menu:
        "(Grudgingly.)":
            $ s1_pick("matsuda_contact", "brisk")
            mc "...Fine. But if this becomes a group chat called 'Depresso Espressos,' I'm out."
            ma "Noted and promptly ignored."
        "(Play along.)":
            $ s1_pick("matsuda_contact", "wry")
            mc "I accept, provided fate covers my medical expenses."
            show matsuda happy
            ma "Fate is uninsured, but spiritually generous!"
            show tsubaki unamused
            ts "It really isn't."
        "(Just hand it over.)":
            $ s1_pick("matsuda_contact", "warm")
            "I hand her my phone without arguing. Matsuda blinks once."
            show matsuda thinking
            ma "...Hm."
            show matsuda smug
            ma "No resistance whatsoever. I'll allow it."
            show tsubaki smug
            ts "She had a whole speech ready."
            show matsuda unamused
            ma "I had a whole speech ready."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "We exchange numbers. Tsubaki studies the vending machine like it deserves her full attention."
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
    "I look up. Matsuda is already smiling like she has signed a treaty in her own favor."
    mc "Congratulations."
    show matsuda teasing
    ma "Oh, thank you, my good chum! Your concern is moving."
    show tsubaki worried
    ts "Umm...we should let him go home. It's already getting late, you know."
    show tsubaki embarrassed
    ts "Don't either of you have a curfew? ...Or is that just me?"
    show matsuda unamused
    ma "Fine, fine..."
    show matsuda happy
    ma "[player]! We may have been cut short now, but 'tis not the end of our long-standing partnership!"
    show matsuda teasing
    ma "We should let fate finish speaking another time."
    mc "...Fate can text, apparently."
    show matsuda happy
    ma "Exactly, yes! Adapt or be left behind, I say!"
    # SFX SUGGESTION: A sharp paper-bag crinkle punctuating Matsuda's sudden turn.
    show matsuda at t31
    show tsubaki embarrassed at t33
    "She turns with a sweep that makes the paper bag under Tsubaki's arm crinkle in alarm. Tsubaki bows once more, smaller this time."
    ts "Sorry about earlier. And about the sister thing. I mean, not your fault, just..."
    mc "No, that one was definitely mine. Nice meeting you, Tsubaki."
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
    nier "My lap around the block ends earlier than planned. I go home with a sore shoulder and an almost dead phone after forgetting to charge it."
    call nier_clear from _call_nier_clear_0517_7
    stop music fadeout 1.0
    pause 2.0
    scene bg living_room_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music fantasypassion
    play sound moddooropen
    "Asahina is on the living room floor amid poster board and paper cutouts. A glued corner has curled up while she wasn't looking."
    show asahina frustrated at t11
    "My phone buzzes at four percent on my way past her. Her eyes go from the phone to my face."
    show asahina curious
    ah "You look weird."
    mc "Hello to you too, farthead."
    show asahina smug
    ah "No, seriously. That's your trying-not-to-smile face."
    "I put the phone facedown against my thigh."
    mc "I collided with someone while getting fresh air."
    ah "Name?"
    mc "Matsuda."
    "Asahina repeats the name under her breath, testing it against whatever rumor index she keeps in her head."
    ah "Red hair? Obnoxious as heck?"
    mc "Oh, you know her?"
    show asahina disgusted
    ah disgusted "{i}E-VER-Y-ONE{/i} knows of her! She's a dingus who performs everything at max volume and somehow sucks at half of it."
    show asahina nervous
    ah "...Or, at least, that's what my friends say. I dunno her personally."
    "That's fair. I let it pass."
    mc "...Uh-huh."
    show asahina teasing
    ah "So did she give you her number?"
    mc "Correction: contact info. Different implications."
    mc "I don't know, okay? I didn't wanna be rude."
    ah "Whatever helps you sleep, bro."
    "She presses a cutout onto the poster, then smooths it flat under her palm."
    show asahina thinking
    "The lettering is annoyingly good. Tape still clings to her sleeve, and a ruler balances across her knee."
    mc "It's coming along, I see."
    show asahina smug
    ah "Don't change the subject just because I'm the most talented person in the world."
    mc "...I'm going upstairs."
    show asahina unamused
    ah "You always do this, by the way. You're such a freaking doormat."
    mc "I'm not even gonna respond to that, so ha."
    show asahina teasing
    ah "You just did~"
    show asahina neut at thide
    hide asahina neut
    "I take the stairs and leave the argument where it is. Her laugh follows me halfway up."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Mom checks in twice. On the second pass she praises the poster, and Asahina realigns the same letter for the next five minutes."
    call nier_clear from _call_nier_clear_0517_8
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    "The game waits by the console, still sealed."
    "On my charging phone, Monika's movie reminder sits beneath a contact I saved less than an hour ago."
    "{i}I can just...pretend that one doesn't exist, yeah?{/i}"
    "I leave both threads unopened and watch the screen dim around their names."
    "I roll my shoulder. The ache is faint and easy to ignore."
    "My eyes are heavy. I set tomorrow's alarm, denying Monika the right to say she warned me."
    "I lower the phone, and something in the back of my head coughs."
    "{i}School. Game. Glue. Tomorrow, Monika.{/i}"
    "{i}That was everything...right?{/i}"
    "The planner from last night flashes through my head, still open to Saturday."
    "{i}MAYBE: Look at that school with Mom.{/i}"
    mc "..."
    mc "...AH, SHIT."
    mom "[player]?! Everything okay up there?!"
    mc "YEAH! JUST A MINOTAUR KICKING MY BUTT!"
    $ update_character_thought("matsuda", "Matsuda Akai transferred in this year, and everyone seems to know of her without actually knowing her. She took my contact info after a sidewalk collision and texted before I reached the corner.")
    $ update_character_thought("tsubaki", "Tsubaki Kareda carries the bag and apologizes for whatever Matsuda just did. She noticed the chin thing before I said anything.")
    $ hide_calendar()
    stop music fadeout 2.0
    scene black with dissolve_scene_full
    call calendar_advance(days=1) from _call_calendar_advance_0517_1
    jump a0518
