label a0517:
    # --- Day 3: 2025-05-17 ---
    scene bg doorday
    $ show_calendar()
    show mood_home zorder 3 
    with dissolve_scene_full
    play music dailyfantasy
    window auto
    "Saturday morning doesn't happen at the table."
    "It happens by the door, one shoe half-tied, one hand searching my bag for a pen I am reasonably sure I never owned."
    show mom neut at t22
    show asahina neut at t21
    "Mom presses a wrapped piece of toast into my hand before I can pretend that skipping breakfast is a strategy."
    "Asahina is crouched near the shoe rack, fixing the heel of her loafer with the intensity of emergency surgery."
    mom "Lunch is in your bag. Eat the toast before you get to school, not during first period."
    mc "You're assuming first period doesn't deserve toast."
    ah "It doesn't deserve anything. It's Saturday."
    "Her voice is flat enough to iron clothes with."
    mom "Now now, both of you survived last Saturday."
    mom "Also how many times have we started school again?"
    mom "Put your big boy pants and your big girl pants on."
    mc "Survival isn't consent, you know..."
    "Mom gives me the look she reserves for sentences she is choosing not to dignify."
    mom "Glue and game. You wrote it down?"
    mc "On my phone and in the part of my brain that still fears Asa."
    ah "Totally a healthy thing, by the way."
    "She stands, catches my sleeve before I can step outside, and holds up one finger."
    ah "The glue is not optional, and don't get the tiny bottle. This stupid poster board is bigger than I thought."
    mc "Oh, so you started it?"
    ah "It's called recon, thank you muchas sumimasen!"
    mc "...Do you even know what you said?"
    "Mom smiles into her coffee, and Asahina sees it and immediately looks away."
    mc "...Medium bottle, then."
    ah "Large if it's cheap."
    mc "Your gluttony knows no bounds..."
    "Mom snaps her fingers and gestures out the door."
    mom "Go. Both of you."
    "The command lands with enough parental authority to move traffic."
    show mom at thide
    hide mom
    show asahina at thide
    hide asahina
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Asahina leaves first, still trying to pretend she is not rushing."
    nier "I follow with toast in one hand, my bag over one shoulder, and the feeling that every Saturday class was designed by someone who wanted teenagers to learn humility through inconvenience."
    play sound moddoorclose
    call nier_clear from _call_nier_clear_0517_1
    scene bg class_day
    $ show_calendar()
    show mood_afternoon zorder 3 
    with dissolve_scene_full
    # CRITIQUE: This civics lesson has strong thematic potential: rules, trust, authority, boundaries. Right now it mostly plays as a clever classroom bit; connect it harder to MC's later need to set limits.
    "Civics is the kind of easy that becomes dangerous if you mistake familiarity for safety."
    "The teacher has drawn a triangle across the board, each point labeled in clean block letters: {i}INDIVIDUAL{/i}, {i}INSTITUTION{/i}, {i}PUBLIC TRUST{/i}."
    "Under it, arrows loop in both directions like the diagram is trying to admit society is just homework with better branding."
    show civics_teacher neut at t11
    civics_teacher "A rule is not automatically legitimate because someone wrote it down."
    civics_teacher "Legitimacy depends on whether people believe the institution has earned the authority it exercises."
    "I write that down, then underline {i}earned{/i} because it sounds like it warrants a short response on the exam."
    civics_teacher "So when someone says, rules are rules, what question should follow?"
    "A few hands rise."
    "Mine does not, because I am capable of growth."
    "My mouth, unfortunately, is still on a separate development schedule, and my eyes roll on their own."
    mc "Whether the rule is doing anything useful, or whether someone just laminated a bad idea."
    civics_teacher "Interesting."
    "That word has no business being that dangerous."
    civics_teacher "[player]."
    mc "...Yeah?"
    civics_teacher "Come here for a moment."
    "That is how I learn that being right in civics can still get you punished if you say it like a scathing review."
    "I stand beside the board while the class performs the sacred ritual of pretending not to enjoy this."
    civics_teacher "Everyone, [player] is going to help us model the relationship between civic authority and public compliance."
    mc "Do I get qualified immunity?"
    "A laugh breaks somewhere near the back row and dies immediately under the teacher's stare."
    civics_teacher "You get accountability. Hold it carefully."
    "The teacher hands me a textbook and points to the center of the triangle."
    "I hold the book to my chest. It's heavier than it looks, which is either a coincidence or a very committed metaphor."
    civics_teacher "Institutional authority here. Individual rights here. Public trust here."
    civics_teacher "A society can tolerate imperfect rules for a while, but tolerated is not the same as trusted."
    "She draws one more arrow, slower than the others."
    civics_teacher "If authority relies only on compliance, it becomes brittle. If it earns trust, it becomes durable."
    "A couple of pencils start moving again. Mine, abandoned on my desk, does not."
    civics_teacher "Thank you. You can sit down now."
    mc "...Why did I have to do that again?"
    civics_teacher "Again, accountability."
    civics_teacher "Answering in a non-respectful manner does that to you."
    "I return to my desk with the mild shame of a person who made a point and became the teaching aid attached to it."
    "{i}At least I wasn't wrong.{/i}"
    show civics_teacher at thide
    hide civics_teacher
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The rest of the school day doesn't improve so much as thin out."
    nier "Everyone saves their real energy for the exact moment the final bell gives us permission to throw the building into chaotic shuffling."
    call nier_clear from _call_nier_clear_0517_2
    scene bg corridor
    $ show_calendar()
    show mood_afternoon zorder 3 
    with wipeleft_scene
    "The corridor fills fast after the last bell. Bags swing, shoes squeak, and the whole school seems to tilt toward the exit at once."
    "I step aside near the windows to check my errands before the crowd can carry me past my own plans."
    show monika 1a at t11
    m "Escaping already, eh?"
    mc "Attempting to. The building keeps putting people in the way."
    m "I won't detain you long, then. No club today, as promised."
    mc "A president who honors a day off. Rare discipline, gotta give you credit for that."
    m "Careful. Compliments like that might get you invited somewhere."
    # CRITIQUE: This is date tension, but MC flees into errands almost immediately. Give him one honest internal beat before the deflection so the romance has pulse instead of only banter.
    "She says it lightly, and then does the small Monika thing where she lets the silence after it exist just a little longer than necessary."
    "I look down at my phone again, not because the list has changed."
    mc "I'd stay and chat, but I honestly do have to get going. Store to pick up a game, then glue for Asa's poster."
    m "Wow, in a rush for just two things? Needy much?~"
    mc "My household is governed by...specific grievances. Specifically my need for this game on launch day and..."
    mc "...Why am I explaining this again?"
    m "Then I won't interfere with domestic diplomacy. Text me tomorrow morning about the movie?"
    mc "Yeah. Morning...provided I wake up on time."
    m "Good. I want enough time to pick a showing where you can't pretend you forgot."
    mc "That's a lot of distrust for a person who has never once forgotten a movie."
    m "You lost your ID card two days ago."
    mc "Nope, nuh uh, shut up. Selective priority, or something like that."
    m "Mhm. Go buy your stuff, [player]."
    "She steps back into the flow of students, clipboard against her chest. By the time I think of something better to say, she is already far enough away that calling after her would make it a scene."
    "{i}Probably for the best.{/i}"
    show monika at thide
    hide monika
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I leave school with the rest of the Saturday survivors."
    nier "The crowd thins by the station, then again by the shopping street, until the day finally feels like it belongs to people who chose to be outside."
    call nier_clear from _call_nier_clear_0517_3
    scene bg store_techsection
    $ show_calendar()
    show mood_afternoon zorder 3 
    with dissolve_scene_full
    "The supermarket has the controlled impatience of a release day that did not quite become a disaster."
    "There is a line at the counter, a line near the case, and a third line made of people pretending they are browsing accessories while clearly watching the stock behind the glass."
    "I get my copy after ten minutes and only one argument over whether a preorder receipt counts without the email confirmation."
    "The craft aisle is quieter. I grab a larger bottle of glue than Asahina asked for because it's shockingly cheap."
    "I internally celebrate until I realize I'm giddy about glue of all things."
    $ hide_calendar()
    scene black with wipeleft_scene
    scene bg store_techsection
    $ show_calendar()
    show mood_afternoon zorder 3 
    with wipeleft_scene
    "Kotonoha is at the register when I get there."
    show kotonoha neut at t11
    # CRITIQUE: "Wanton stare" is the wrong word unless you mean sexually immodest/desiring. The intended effect seems closer to flat, ancient, unreadable, or professionally vacant.
    "She stares at me with a wanton stare that gets older the more you look back."
    mc "Afternoon."
    ko "Good afternoon."
    "She scans the game, turns the case over to check the security sticker, then sets it into a separate bag before the glue gets anywhere near it."
    ko "Your receipt will be in this first bag, if that's alright."
    mc "Appreciated."
    "She points and wiggles her finger at the glue bottle."
    ko "The cap is loose on that brand sometimes."
    "She tightens it without making a production of it, the same way someone else might straighten a crooked picture frame."
    mc "Oh, uh...good catch."
    ko "It happens."
    "The register prints the receipt. She folds it once, exactly down the middle."
    ko "Have a good day."
    mc "You too."
    "That is the whole transaction: items scanned, receipt folded, Kotonoha behind the counter as if she has always belonged to that particular register."
    show kotonoha at thide
    hide kotonoha
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The walk home is uneventful, though the bag with the glue keeps bumping against my leg like it wants credit for being important."
    nier "For Asahina's sake, I keep it upright despite the dark urge to mess with it."
    call nier_clear from _call_nier_clear_0517_4
    scene bg doorday
    $ show_calendar()
    show mood_home zorder 3 
    with wipeleft_scene
    play sound moddooropen
    "Asahina meets me at the door with a strip of masking tape stuck to her sleeve."
    show asahina neut at t11
    mc "You started without me."
    
    ah "I started without the most important part. That's not the same thing."
    
    "I hand over the larger bottle. She checks the label, then tries and fails not to look pleased."
    
    ah "...Yeah, this works."
    
    mc "Glowing praise."
    
    ah "Shush, don't get greedy."
    
    "She turns the bottle over once, then tucks it beside the poster board with the rest of her supplies."
    mc "And before you ask, no, I didn't restock my own chips for you."
    
    ah "I wasn't going to ask."
    
    mc "You looked like you were about to develop the thought."
    
    ah "I said I'd handle it, didn't I?"
    ah "Go play your game or whatever."
    
    mc "After homework. Still got responsibilities, ya know?"
    
    ah "Wow...mom really has brainwashed you."
    
    mc "What do you mean? You're barely younger than me, we were both raised by her."
    show asahina at thide
    hide asahina
    "Asahina snorts, then retreats toward the living room before I can inspect the poster."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "I take the game upstairs and set it beside the console, still sealed."
    nier "That restraint lasts mostly because homework exists and because opening a new game ten minutes before mom asks whether I finished anything would be an amateur mistake."
    nier "The afternoon settles into chores, notes, and the low rustle of Asahina fighting poster board downstairs."
    call nier_clear from _call_nier_clear_0517_5
    scene bg bedroom
    $ show_calendar()
    show mood_home zorder 3 
    with wipeleft_scene
    "The game case spends the next half hour catching light from the desk lamp like it knows what it's doing."
    "I finish the homework that can be finished quickly, then stare at the assignment that cannot."
    "Eventually, I move that one to Monday's problem pile, where it joins several other things I am pretending are organized."
    "A message from Monika arrives around the time the house starts to quiet down."
    python:
        _phone_messages = [
            phone_msg("them", "Don't forget tomorrow morning. I know you won't, but now I can say I reminded you!"),
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
    nier "I step outside before the sealed game can win the argument."
    call nier_clear from _call_nier_clear_0517_6
    stop music fadeout 2.0
    pause 1.0
    scene bg house_night
    $ show_calendar()
    with wipeleft_scene
    play music fantasypassion
    window auto
    "The porch is quiet enough to make the day feel further away than it is."
    "I sit on the step with my elbows on my knees, listening to the loose click of a bicycle wheel somewhere across the street and the faint clatter of dishes through our kitchen window."
    "For a while, that is enough."
    # CRITIQUE: Sentence-level nit: "Then it isn't whenever..." is grammatically muddy. The intended beat seems closer to "Then it isn't, once my attention span..."
    "Then it isn't whenever my attention span decides to move onto the next best thing."
    "I stand, roll the stiffness out of my shoulders, and take the sidewalk with no plan beyond moving until boredom loses interest."
    $ hide_calendar()
    scene bg residential_night
    $ show_calendar()
    with wipeleft_scene
    # CRITIQUE: The tense logic is tangled in "when once-bustling places are now vacant." This would read more smoothly if the sentence stayed in one time frame.
    "The neighborhood looks different at this hour. It's always a different feeling when once-bustling places are now vacant."
    "Curtains glow. A vending machine hums near the corner. Somewhere ahead, two voices overlap: one low and careful, the other bright enough to cut through the evening air."
    "I glance down when my phone buzzes, expecting another reminder..."
    "...and walk straight into the consequence."
    # TODO: Insert sidewalk collision CG here when the dedicated asset is available.
    with hpunch
    $ ma_name = "Red Girl"
    $ ts_name = "Meek Girl"
    "My shoulder hits someone else's. Both of us go flying in the opposite direction, my phone nearly leaves my hand, and three separate apologies try to start at once."
    mc "Ah! Sorry, I wasn't--"
    show matsuda neut at t21
    show tsubaki neut at t22
    # CRITIQUE: Matsuda's entrance is memorable, but the prose-to-dialogue density is exhausting. Let the reader get one stable human impression before the performance starts swallowing the scene.
    ma "Aha! Collision as inciting incident. Crude, but effective."
    "The girl in front of me catches herself with one white-gloved hand against a fence post, then straightens as if the stumble was part of a routine she meant to perform."
    "Red hair, high ponytail, a braid on one side, and earrings still swinging from the collision: subtle is clearly not the design goal."
    "The other girl has chestnut hair close enough in color to make me look twice. She almost tosses the paper bag she's holding aside in preparation of catching one of the two bodies."
    ts "Are you hurt?! Do you need ice?!"
    mc "No, I'm fine... Hoo boy, okay, that does kinda smart..."
    mc "Is your sister okay, though?"
    "The temperature changes immediately."
    ma "...Her what?"
    ts "She's not--"
    "{i}Hoo boy, here we go...{/i}"
    ma "Sister? Do I look like I travel with understudies?"
    $ ts_name = "Tsubaki"
    ma "With all due respect, and I am generously inventing the respect as we speak, this is Tsubaki Kareda: confidante, witness, occasional conscience, and chronic apologizer!"
    ts "...Best friend is shorter."
    ma "Shorter, yes, albeit far less accurate."
    "Tsubaki gives me a small, mortified bow."
    ts "I'm so sorry about her. She gets worse when she's startled..."
    mc "...That's worse?"
    ma "'Twas restraint, my good chap."
    "She says it with such total conviction that I almost apologize to the concept of restraint."
    mc "Then I should be thankful."
    ma "You should be several things. Thankful is acceptable as a starting position for my radiant corpus!"
    ts "Matsuda..."
    "One word from Tsubaki pulls the other girl's chin down by a fraction. Not much, but enough to prove there is a leash somewhere under all the theater."
    $ ma_name = "Matsuda"
    ma "Fine. I, Matsuda Akai, forgive the collision on grounds of mutual negligence and decent reflexes."
    mc "...[player]. And for the record, my reflexes were mostly panic, okay? It was...what's that term again...a robin response, or whatever it's called."
    ma "[player]..."
    ma "Literature club, right?"
    mc "Yeah...?"
    ma "I knew it! You have the posture of someone who has been told against his will to expunge his deepest, darkest feelings with four movable desks."
    "That is specific enough to be insulting and accurate enough to be annoying as hell."
    mc "You got all that from being shoulder-checked?"
    ma "I am observant under pressure, lad."
    ts "Translation: she saw you with Monika after school."
    ma "Tsubaki, please. Let the mystique breathe and don't be a buzzkill."
    "I look between them and decide the safer option is not to ask how long a mystique {i}can{/i} hold its breath."
    mc "Well, again, sorry. I was checking my phone and thinking about how long I could avoid opening a game I bought today."
    ma "You bought a new game and left the house without opening it...?"
    "Her eyes narrow as if I just slid evidence across a table."
    mc "It seemed healthier than losing the whole evening."
    ma "My good sir! Healthy choices are where stories go to die."
    ts "You literally told me to stop you from buying snacks for dinner."
    ma "'Twas nutritional compromise! Let us not mince semantics!"
    "Tsubaki sighs through her nose, but there is affection in it."
    # CRITIQUE: "Her face is a portrayal of..." is too abstract for a physical reaction. Describe the actual mouth, eyes, or timing first, especially because Tsubaki's small expressions are one of her main characterization tools.
    "Her face is a portrayal of badly concealed laughter, complete with shut eyes and a shit-eating grin."
    mc "So anyway...you're Matsuda, she's Tsubaki, and you two are NOT sisters."
    # CRITIQUE: From here through "noted and ignored," nearly every line is a punchline. Pick the sharpest two; otherwise the characters sound like they are competing for a laugh track instead of meeting.
    ma "Progress, yes! See, my confidante?! The collision has already produced character development."
    mc "Mostly bruising."
    ma "Bruising is just character development with color, [player]."
    ts "...Please don't write that down..."
    "Matsuda has already pulled out her phone."
    ma "[player], I not-so-humbly request you give me your contact."
    "Tsubaki closes her eyes again for half a second."
    ts "She means, if you're okay with it. You don't have to."
    ma "Yes, yes, manners and civilization. I was approaching the polite version with, in my opinion, more grand pacing."
    mc "You ask everyone you crash into for contact info?"
    ma "Only the ones who recover well and accidentally insult my lineage."
    "I open my mouth in preparation to say something, but sigh instead."
    "I should say no just on principle. Instead, I find myself opening my contacts, because the evening has already stopped behaving like mine."
    mc "...Fine. But if this becomes a group chat called 'Depresso Espressos,' I'm blocking you without question."
    ma "Noted and ignored."
    "We exchange numbers. Tsubaki watches the street while we do it, giving us privacy in the least dramatic way possible."
    "My phone buzzes a moment later."
    python:
        _phone_messages = [
            phone_msg("them", "For the record, I survived."),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, status="New Contact", append=True) from _call_phone_text_conversation_0517_3
    "I look up. Matsuda is already smiling like she has signed a treaty in her own favor."
    mc "Congratulations."
    ma "Oh, thank you, my good chum! Your concern is moving."
    ts "Umm...we should let him go home. It's already getting late, you know."
    ts "Don't either of you have a curfew? ...Or is that just me?"
    ma "Fine, fine..."
    ma "[player]! We may have been cut short now, but 'tis not the end of our long-standing partnership!"
    ma "We should let fate finish speaking another time."
    mc "...Fate can text, apparently."
    ma "Exactly, yes! Adapt or be left behind, I say!"
    "She turns with a sweep that makes the paper bag under Tsubaki's arm crinkle in alarm. Tsubaki bows once more, smaller this time."
    ts "Sorry about earlier. And about the sister thing. I mean, not your fault, just..."
    mc "No, that one was definitely mine. Nice meeting you, Tsubaki."
    ts "You as well!"
    ma "We'll reconvene, [player]. Try not to collect any less interesting acquaintances before then."
    mc "...No promises."
    show matsuda at thide
    hide matsuda
    show tsubaki at thide
    hide tsubaki
    "They head toward the vending machine, Matsuda already talking with both hands while Tsubaki adjusts her pace to keep the bag from swinging."
    "I stand there long enough for my phone to buzz again."
    python:
        _phone_messages = [
            phone_msg("them", "Also, if the game is good, lie and say it's dogshit until I buy my copy."),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, status="New Contact", append=True) from _call_phone_text_conversation_0517_4
    "I type back before I can overthink it."
    python:
        _phone_messages = [
            phone_msg("me", "Terrible. Historically bad. So bad I haven't even opened it yet."),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, status="New Contact", append=True) from _call_phone_text_conversation_0517_5
    "Her reply arrives before I reach the corner."
    python:
        _phone_messages = [
            phone_thumb("them"),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, status="New Contact", append=True) from _call_phone_text_conversation_0517_6
    mc "..."
    mc "What the hell just happened?!"
    $ mark_character_met("matsuda")
    $ phone_mark_contact_met("matsuda")
    $ mark_character_met("tsubaki")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "My lap around the block ends earlier than planned."
    nier "I go home with a sore shoulder, an unopened game, and her name lighting my phone twice before I reach the gate."
    call nier_clear from _call_nier_clear_0517_7
    scene bg living_room_night
    $ show_calendar()
    show mood_home zorder 3 
    with wipeleft_scene
    play sound moddooropen
    "Asahina is on the living room floor when I come back in, surrounded by poster board, paper cutouts, and the despair of a person who remembered glue dries on its own schedule."
    show asahina neut at t11
    "My phone buzzes before I can get past her."
    "She looks up at the sound, then at my face."
    
    ah "You look weird."
    
    mc "Hello to you too, farthead."
    
    # CRITIQUE: The girlfriend teasing repeats the Monika joke pattern from earlier. Asahina can still needle him, but vary her angle so the sibling dynamic does not become one button she keeps pressing.
    ah "No, seriously. That's your trying-not-to-smile face."
    
    "I put the phone facedown against my thigh, which is not suspicious at all if you are deeply committed to denial."
    mc "I met someone while getting fresh air."
    
    ah "Met someone, or {i}met{/i} someone?"
    
    mc "Collided with someone, actually."
    
    ah "That's one way to start."
    
    mc "Well, it was more like...sidewalk traffic."
    "{i}...So, just traffic? Way to go, [player].{/i}"
    
    ah "Name?"
    
    mc "Matsuda."
    "Asahina repeats the name under her breath, testing it against whatever rumor index she keeps in her head."
    
    ah "Red hair? Obnoxious as heck?"
    
    mc "Oh, you know her?"
    
    ah "{i}E-VER-Y-ONE{/i} knows of her! Not to mention she's a performative dingus who's an attention hog."
    ah "...Or, at least, that's what my friends say. I dunno her personally."
    
    "That is fair enough that I have to let it pass."
    mc "...Uh huh."
    "I covertly slip my phone into my pocket, almost out of some sort of shame or secondhand embarrassment."
    
    ah "So did 'sIdEwAlK tRaFfIc' give you her number?"
    
    mc "Correction: contact info. Completely different undertone-slash-connotation-slash...uh..."
    mc "Listen, I don't know, okay? I didn't wanna be rude."
    
    ah "Whatever helps you sleep, bro."
    
    "She presses a cutout onto the poster and smooths it down with the side of her hand."
    "The lettering is good, annoyingly good, even with the tape on her sleeve and a ruler balanced across her knee."
    mc "Poster's coming together, I see."
    
    ah "Don't change the subject just because I'm the most talented person in the world."
    
    mc "...I'm going upstairs."
    
    ah "Remember to text your girlfriend goodnight~"
    
    mc "I'm not even gonna respond to that."
    
    ah "You just did~"
    
    "I leave before she can find a stronger angle, though her laugh follows me halfway up the stairs."
    show asahina at thide
    hide asahina
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The rest of the night folds over the house while Asahina keeps working."
    nier "Mom checks in on us twice. The second time, she tells Asahina the poster looks good, and Asahina pretends that doesn't matter as much as it obviously does."
    nier "My retreat upstairs remains so for the rest of the night."
    call nier_clear from _call_nier_clear_0517_8
    scene bg bedroom
    $ show_calendar()
    show mood_night zorder 3 
    with wipeleft_scene
    "The room is exactly how I left it, except the day has managed to put a new name in the middle of it."
    # CRITIQUE: Good triangle of attention. Consider letting MC notice that Matsuda's messages are already crowding Monika's, because this is the earliest visual version of the social displacement Act 1 needs.
    "The game waits by the console; Monika's movie reminder waits in my messages; Matsuda's texts sit adjacent to it, much to my annoyance."
    "For a while, I don't open anything."
    "I roll my shoulder. It aches faintly--not enough to matter, but just enough to make the collision feel less imaginary."
    "{i}Matsuda Akai.{/i}"
    "{i}Tsubaki Kareda.{/i}"
    "One of them entered like a curtain went up and the other spent the whole scene making sure nothing broke."
    "Somehow, both of them feel like they belong to the same sentence."
    "I set my alarm for tomorrow morning before Monika can earn the right to say she warned me."
    $ update_character_thought("matsuda", "Matsuda crashed into the evening, took my contact info, and somehow made the whole thing feel premeditated by fate.")
    $ update_character_thought("tsubaki", "Tsubaki kept apologizing around Matsuda's theatrics, but she noticed more than she said.")
    $ hide_calendar()
    stop music fadeout 2.0
    scene black with dissolve_scene_full
    call calendar_advance(days=1) from _call_calendar_advance_0517_1
    jump a0518
