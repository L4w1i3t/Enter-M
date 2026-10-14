define planner_0516_saturday = (
    ("SCHOOL", "Turn in my foreign language homework, finish essay rough draft, survive classes."),
    ("ERRAND", "Get game."),
    ("ERRAND", "Grab glue for Stinky's poster."),
    ("MAYBE", "Look at that school with Mom."),
)

define planner_0516_sunday = (
    ("TEXT", "Monika in the morning, don't let her beat you."),
    ("PLAN", "Horror flick with Monika."),
    ("REMINDER", "Do NOT get lost in press-turn battles."),
    ("MAYBE", "Work on that piece I promised I would.")
)


label a0516:
    # --- Day 2: 2025-05-16 ---
    pause 2.0
    scene bg bedroom
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music house_day_a
    "My alarm goes off with all of my reminders still sitting above it. My family has found a way to get in first without being in the room."
    # SFX SUGGESTION: A phone vibrating against wood, followed by a distant toaster pop.
    "I nearly kick the corner of the bed reaching for the phone as it buzzes toward the edge of the desk. Downstairs, the toaster pops before I can even shut it off."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    $ atmos("home", particles="motes")
    with wipeleft_scene
    show mom uniform neut at t22
    "Mom is still in the kitchen when I come in, working between the sink and the stove."
    show asahina uniform thinking at t21
    "Asahina sits at the table with her head tilted over one shoulder while she tries to fix a twist in her sleeve by feel alone."
    mc "'Sup."
    mom "Morning, [player]."
    show mom uniform teasing
    mom "Eggs are almost done, so don't disappear upstairs again."
    show asahina uniform neut
    ah "He just got here, Mom."
    show mom curious
    mom "Uh..."
    mc "No, no, she does have a point."
    show mom uniform smug
    mom "...Well, sure, I'll take that."
    "I take my seat and reach for the cranberry juice in front of me."
    "While my sister finishes fighting her sleeve, I retrieve the butter she's pulled to her end of the table."
    "The toaster pops again, and Mom catches the new slices of toast--one minimally browned and one pretty much charred--on the plate she's carrying."
    show mom uniform unamused
    mom "Whoever put the empty juice carton back in the refrigerator, I want you to know I have narrowed it down to two people."
    mc "..."
    show asahina uniform neut
    ah "..."
    mc "...?"
    show mom uniform smug
    mom "I'm not mad, just disappointed."
    "Asahina catches me looking at the sleeve and narrows her eyes."
    mc "...I wasn't going to say anything!"
    show asahina uniform unamused
    ah "You were staring! Fix your own stupid collar."
    "I feel along my neck. She's right, which I could have done without."
    "Mom plates the eggs and sets them down."
    show mom uniform neut
    mom "Alrighty, food first, commentary after."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Mom asks about homework while I answer vaguely but descriptive enough to keep the ball rolling. Across the table, Asahina pretends not to smile at whatever lit up her phone."
    nier "As breakfast goes on I zone out and blur all conversation around me, until a gnat lands on my forehead and snaps me back to reality."
    call nier_clear from _call_nier_clear_0516_1
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    show mom uniform neut at t22
    show asahina uniform neut at t21
    $ atmos("home")
    with wipeleft_scene
    "I finish the last of my toast and pull my glass of juice closer to me."
    mc "Glue tomorrow. Big bottle, not the stick, right?"
    ah "Mhm."
    show mom uniform smug
    mom "The poster you were supposed to start last week?"
    "Asahina's chewing slows."
    show asahina uniform unamused
    ah "Yes, that poster. I've got the layout in my head, so I just need to actually make it."
    mc "So it's gone from idea to actual threat, I see. Hey, we all start somewhere."
    show asahina uniform smug
    ah "Keep talking and I'm putting you on it. Huge face, right in the middle. With extra detail to that peach fuzz you call a beard."
    mc "Yeah, I'd rather die. Catch me leaving the whole country so that you can't have any reference photos."
    show asahina uniform pose_hairflip
    ah "With THAT bum foot? HA!"
    show mom uniform teasing
    mom "I'd frame the attempt, at least."
    mc "...Et tu, Brute...?"
    "{i}At least the eggs are good.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Asahina leaves while I'm still looking for my shoes. Through the doorway, I watch her shorten the strap of the bag that keeps hitting her knee."
    nier "Mom calls after us about the weather. I check the sky, then go back for the folding umbrella by the door."
    nier "Bag, wallet, umbrella, ID in the zipped pocket, a lanyard that's basically a corpse."
    nier "{i}That should be everything, I think.{/i}"
    call nier_clear from _call_nier_clear_0516_2
    stop music fadeout 1.0
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with dissolve_scene_full
    play music quiz
    "In what feels like absolutely no time whatsoever, my day has faded into the early afternoon."
    "Sixth period is college-level Algebra. My notes start neatly enough, then the graph takes over the page."
    show math_teacher neut at t11
    math_teacher "All right, everyone. Last time we covered transformations of logarithmic functions."
    math_teacher "Today, we're combining that with... domain restrictions!"
    "Chalk taps against the board."
    show math_teacher neut
    math_teacher "Take f(x) = log2(x - 1) + 3. The entire x minus one is inside the logarithm."
    math_teacher "Before we talk about the graph itself, can anyone tell me what the domain is?"
    "Somebody's been clicking a pen for the last four minutes. I turn to see who it is and find three people looking back."
    "Unfortunately, I make the mistake of looking halfway attentive."
    math_teacher "[player], start us off with a layup. What values of x can we use?"
    $ atmos_pressure()
    with dissolve
    "{i}Right. Death by eye contact. Classic mistake.{/i}"
    menu:
        "x greater than one":
            jump rightanswer1
        "x less than one":
            jump wronganswer1
        "x":
            jump wronganswer1
    label rightanswer1:
        $ atmos_pressure_clear()
        with dissolve
        math_teacher "Correct. Why?"
        mc "Because the argument of the logarithm has to be positive, so x minus one has to be greater than zero."
        "The teacher underlines the x minus one part twice."
        show math_teacher neut
        math_teacher "Good! Mark that restriction before you draw the curve."
        math_teacher "Then check what happens as x approaches one from the right. The graph and the numbers should agree."
        "I sketch the asymptote while the pen behind me resumes clicking."
        math_teacher "Now, for the vertical shift..."
        jump answer1done
    label wronganswer1:
        $ atmos_pressure_clear()
        with dissolve
        math_teacher "Not quite. Remember that the argument of a logarithm must be positive."
        math_teacher "So x minus one has to be greater than zero, which means x must be greater than 1."
        mc "Oh... right. Got it."
        "A few students murmur and write the correction down."
        jump answer1done
    label answer1done:
        pass
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "We work through more graphs while the teacher circles the room. When someone asks whether this will be on the exam, he points to the review date on the board."
    nier "By the end of class, my notebook has more arrows than actual words."
    nier "{i}Such is math...{/i}"
    nier "The bell sends me to my foreign language, where I finish the practice sheet early and spend the remaining time sketching a better route through tomorrow's errands."
    call nier_clear from _call_nier_clear_0516_35
    stop music fadeout 1.0
    pause 2.0
    scene bg club_day
    $ show_calendar()
    $ atmos("afternoon", particles="motes")
    with wipeleft_scene
    play music day_a
    "A queue outside the bathroom makes me late to my obligatory club meeting. By the time I get here, the corridor has almost emptied."
    "I expect the usual occupied desks and overlapping voices, probably centered on whether a poem can be too purple."
    show monika forward uniform dist cm oe nobl rdown ldown at t11
    "Monika is here, flipping through a thin notebook with a pen tucked behind her ear. Nobody else is."
    m forward uniform happ om oe nobl rdown ldown "Hey, you made it!"
    mc "Against all odds. Where is everybody?"
    m forward uniform neut cm oe nobl rdown ldown "Hikari has tutoring on Fridays, and Homura goes wherever Hikari goes."
    m forward uniform happ om oe nobl rhip ldown "I'm sure they'll be back another day to argue about commas or something else random. Or maybe Hikari bites everyone's throats out, whichever comes first..."
    m forward uniform happ om oe nobl rdown ldown "The other two have rehearsal. They told me at lunch, which was nice of them, considering I asked yesterday."
    mc "So we've got the place to ourselves, is what you're saying."
    m "Yeppers!"
    mc "So excited to spend this time with you..."
    m forward uniform curi om oe nobl rdown ldown "Rough day?"
    mc "Not really, just in one of those moods today."
    mc "Got called on in math though, but that was about as exciting as you'd expect."
    m forward uniform happ om oe nobl rdown lpoint "Well? Did you at least survive with your dignity?"
    mc "I answered without anyone throwing anything, which is all I really ask."
    m forward uniform wry cm ce nobl rdown ldown "A quiet triumph, then."
    "I take my usual seat and drop my bag beside the desk."
    "She closes her notebook halfway, keeping one finger between the pages."
    m forward uniform happ om oe nobl rhip ldown "So! Given today's showing, today's agenda is pretty light. I was thinking we could read for a bit, then workshop whatever you brought yesterday some more."
    m "That is, if you're fine with that. We could also just skip straight to the second one!"
    mc "You mean the draft with all the brackets still in it?"
    m "That's the one~"
    m forward uniform neut cm oe nobl rhip ldown "I like the first set. It's like you're leaning over to tell me something you left out."
    mc "You're making my bad habits sound organized."
    m forward uniform wry cm oe nobl rhip ldown "You do go back and put more of them in. I've seen the drafts."
    show monika forward uniform curi cm oe nobl rdown ldown
    m forward uniform curi om oe nobl rdown ldown "You left 'smug' in."
    mc "I tried 'golden.' Absolutely hated it, don't care what you say."
    m forward uniform laug om ce nobl rhip ldown "Okay, I hate that too--definitely makes you sound like a cornball. But you have more than two options!"
    mc "It's the right word."
    m forward uniform wry cm oe nobl rhip ldown "Then make me hear it. Yesterday you practically swallowed it and it fell flat on its face."
    mc "Alright, alright... But you're getting the full obnoxious sunset this time, 'cause frick you."
    m forward uniform laug om ce nobl rdown ldown "That's what I've been asking for!"
    "She marks two more places on the page--minute etchings, meant for some sort of boundary."
    mc "You're really not gonna tell me what those are for?"
    m forward uniform wry cm oe nobl rhip ldown "Nope! You'll find them when you read it out loud, and if you don't find them then they weren't the problem I thought they were."
    mc "Oh my God..."
    m forward uniform happ om ce nobl "Chop chop!"
    "Reluctantly, I get through the whole text without lowering my voice. Monika crosses out one of her marks and leaves the other."
    "Down the hall, somebody laughs. I stop listening for footsteps."
    "I'm six lines into the next draft when I notice that her pen has stopped moving."
    show monika forward uniform dist cm oe nobl rdown ldown
    "Monika is looking at the window with her pen still resting on the page."
    "{i}She's allowed to stare out of a window. I've done most of a school day that way.{/i}"
    show monika forward uniform happ cm oe nobl rdown ldown
    m forward uniform neut om oe nobl rdown lpoint "Oh--sorry. I lost my place."
    mc "We can leave it a minute. Did you see the new trailer for Sunday?"
    m forward uniform curi om oe nobl rdown ldown "No! Does it give too much away?"
    mc "Probably, I dunno, it's all out of context. I stopped when they started explaining the tunnel."
    m forward uniform nerv om oe nobl rdown ldown "Then don't tell me. I want at least one surprise left."
    "I put my draft down and pull up a movie promo instead. She leans over until we're both looking at my phone."
    mc "This guy totally dies first. Look at that expression. He's about to say he'll be right back."
    m forward uniform laug om ce nobl rdown ldown "Too obvious. He'll be the one who finds the bodies."
    mc "You're putting a lot of trust in a man holding a flashlight backward."
    m forward uniform curi om oe nobl rdown ldown "He is not--oh, he is!"
    "She takes my phone to enlarge the picture. We spend the next few minutes assigning terrible futures to the rest of the cast."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "When we get back to the draft, Monika has to read the first page again. I write our first-victim predictions on a scrap of paper while she catches up."
    call nier_clear from _call_nier_clear_0516_4
    pause 2.0
    scene bg club_day
    $ show_calendar()
    show monika forward uniform anno cm oe nobl rdown ldown at t11
    $ atmos("evening")
    with wipeleft_scene
    "By the time the light outside begins to wane, Monika stacks her notebook on top of mine."
    m forward uniform happ om oe nobl rdown ldown "There. Nothing too brutal, right?"
    mc "I still have most of a poem. Could've gone worse."
    "She turns my second page around. Beside a line I'd buried three brackets deep, her neat slant reads:"
    "{i}What happens if you let this bit stand on its own? Try it without the next bracket.{/i}"
    "I reread the passage with the bracket covered, then move my thumb and read it again."
    mc "You know... I think that might actually work."
    m forward uniform happ om ce nobl rdown lpoint "I say try it. You can always put it back, I won't stop ya."
    "I slip the pages into my bag with the movie predictions on top."
    mc "Anything I need to remember for tomorrow?"
    m forward uniform curi om oe nobl rhip ldown "Tomorrow? Survive classes, first of all."
    mc "Hadn't planned that far ahead."
    show monika forward uniform laug om ce nobl rdown ldown at h11
    m forward uniform laug om ce nobl rdown ldown "You'll be fine! And when the bell goes, you're free! TGIS, am I right?"
    show monika at t11
    m forward uniform wry om oe nobl rhip ldown "No club afterward, though. I'm not spending my free afternoon pretending to be responsible."
    mc "You not being responsible? Really? You throwing in the academic towel now?~"
    m forward anno om oe "Yeah, uh, remind me who's in front of who right now."
    mc "Mate, we've been trading places for, what, two years now? I dunno about you, but I'm chilling."
    m forward uniform happ cm oe nobl rhip ldown "Yeah, yeah, ahah... Text me Sunday morning so we can pick a time."
    "I set a reminder before she can watch me forget."
    mc "I don't think you'll have to hound me."
    m forward uniform wry om oe nobl rdown lpoint "Great! Now go home before I find a chore to hand you."
    mc "Before the list grows, then. Later, Monika."
    show monika at thide
    hide monika
    play sound moddoorclose
    "She waves me off as I turn into the corridor."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The walk home follows its usual route until the vending machine."
    nier "The orange soda is sold out again. I check the label against the cap still in my pocket, then buy my usual drink."
    nier "{i}Oh, right... imported.{/i}"
    nier "Off to the side of the vending machine, there's a girl with strikingly red hair almost chugging a bottle of that same sold-out soda."
    call nier_clear from _call_nier_clear_0516_5
    pause 2.0
    scene bg residential_day
    $ show_calendar()
    $ atmos("overcast")
    with wipeleft_scene
    "Near the corner store, I slow down when I recognize the girl waiting by the curb with a folded umbrella under one arm."
    show kotonoha casual neut at t11
    "It's Kotonoha, who is technically in my grade, though most people know her by sight before they know anything else."
    "We share a few classes, but I usually catch her between stops like this and nowhere else."
    mc "Oh. Hey, Kotonoha."
    ko "Good afternoon, [player]."
    mc "Waiting for someone?"
    ko "A bus."
    mc "Right, yeah... That would make sense at a bus stop."
    ko casual unamused "It's running late."
    mc "Yeah... they do that."
    "Her convenience-store bag crinkles in the breeze while she adjusts its handles around her fingers."
    show kotonoha casual neut
    mc "Coming from work?"
    ko "One of them."
    "I nod and keep the line moving."
    mc "Long day, then?"
    ko "Average."
    "{i}For her, maybe.{/i}"
    mc "So I guess you're headed home?"
    ko "After the laundromat."
    mc "The one by the station? Good luck with that one, their dryer ate my money last time."
    ko casual thinking "Number three?"
    mc "...Yeah, actually."
    show kotonoha casual neut
    ko "Use four. Three's door doesn't latch properly."
    "I make a mental note."
    "{i}That would have been useful last week.{/i}"
    # SFX SUGGESTION: Wet tires passing close, ending in a short gutter splash.
    "A car rolls by, kicking up a brief hiss of water from a shallow gutter puddle. She steps back as the water reaches the curb."
    mc "Woah, good timing."
    ko "That puddle's deeper than it looks."
    mc "...Good thing I stopped here, then."
    ko casual thinking "Your shoes would have taken most of it."
    # SFX SUGGESTION: A distant bus engine groan with a soft pneumatic-brake hiss.
    show kotonoha casual neut
    "The bus finally groans around the corner in the distance."
    ko "Oh, that's mine."
    mc "Yeah. Guess I'll see you around."
    ko casual teasing "Tomorrow, probably."
    show kotonoha casual neut
    "She gives a small bow, then steps toward the curb as the bus pulls in."
    show kotonoha at thide
    hide kotonoha
    "The bus leaves a wet tread mark along the curb and a fading engine groan."
    $ mark_character_met("kotonoha")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The rest of the walk goes quiet. My brain starts making gibberish out of normal things."
    nier "I look along the power lines and imagine a badass dude running on them without any other objective."
    nier "{i}Damn, I wish that were me.{/i}"
    call nier_clear from _call_nier_clear_0516_6
    play sound moddooropen
    pause 2.0
    scene bg home_entry_day
    $ show_calendar()
    $ atmos("home")
    with wipeleft_scene
    play sound moddoorclose
    "When I step inside my house, an unfamiliar pair of men's loafers occupies the space where I usually leave my shoes."
    "{i}Please don't let this be one of Mom's surprise errands in human form...{/i}"
    "The shoes are lined up neatly, toes to the wall. Asahina's pair has been moved to make room."
    mc "I'm home..."
    ah "Living room!"
    "I put my bag down beside the stairs and follow her voice, already mentally prepared to endure whatever obnoxious sounds her voice can conjure."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg living_room
    $ show_calendar()
    show asahina uniform determined at t31
    show sam uniform neut at t33
    $ atmos("home")
    with wipeleft_scene
    "Asahina stands near the couch with a guy with silky blond hair and a jawline that can cut diamonds. I've seen him around school, usually with more people around him."
    ah smug "So this is Sam..."
    "She unfolds her arms to point between us, then seems to decide we've got it from here."
    sa "Masayami Inugami. Sam's easier, though. That's what everyone calls me."
    mc "[player]. The brother, if she hasn't warned you."
    show sam uniform happy
    sa "She's mentioned you a few times, so I had some idea what I was walking into."
    show asahina uniform happy
    ah "All good things though, so don't get mad."
    mc "Good things, huh?"
    show sam uniform smug
    sa "...Mostly good things."
    "Asahina elbows him in the side, although it seems to hurt her more than him."
    show asahina uniform annoyed
    ah "I said ALL good things."
    show sam uniform teasing
    sa "You said he was smart, sarcastic, and impossible in the morning."
    mc "Hey, that's more of a profile than I expected. I figured she'd trash me."
    sa "She also told me you save every healing item until after the final boss. I dunno, I say that one's fine though."
    mc "That's called being resourceful."
    show asahina uniform teasing
    ah "That's called ending the game with ninety potions that you may as well not have."
    "He offers his hand, and we shake before I have to find something else to say."
    show sam uniform neut
    "I shift aside so I don't accidentally fall onto the couch or stumble on something that someone may have left on the floor."
    mc "So, uh... welcome."
    sa "Thanks for having me."
    show sam uniform nervous
    sa "Sorry about the, ah... short notice. I honestly thought she'd told you."
    show asahina uniform teasing
    ah "There was some warning, ya goof~"
    mc "There was?"
    show asahina uniform smug
    ah "Yeah! I told Mom, which is {i}basically{/i} the same as telling you."
    mc "Must've missed the announcement while I was at school. With both of you. You know, in person."
    show sam uniform smug
    sa "If it helps, I'm not on the list either. I found out about tonight, what, a couple hours ago?"
    "I nearly let out some semblance of a laugh. Asahina sits on the couch arm, looking between us."
    play sound moddooropen
    "The front door opens before she can add anything."
    play sound moddoorclose
    show mom uniform happy at t32
    mom "Ah, you're home!"
    mom "Sam, this is my son, [player]. [player], this is Sam."
    mc "We got through the tutorial already."
    show mom uniform smug
    mom "Good. Asahina, did you tell him the house rules?"
    show asahina uniform embarrassed
    ah "..."
    show mom uniform teasing
    mom "...I'll take that look as a no."
    ah "Mom..."
    show sam uniform pose_crossed
    "She points at my sister."
    mom uniform determined "Doors stay open. Finish what you need for tomorrow before the movie starts."
    mom "After that, entertain yourselves. I have work to finish."
    "She turns toward the kitchen, already pushing up her sleeves."
    show mom uniform neut
    mom "And if anyone gets hungry, there are leftovers."
    "Sam's eyes flick toward Asahina, then back to Mom."
    sa uniform determined "Understood, ma'am."
    show mom uniform smug
    mom "Ooh, good answer."
    show asahina uniform smug
    ah "See? He's not an alien, bro."
    mc "I never said he was! Don't put words in my mouth."
    show asahina uniform unamused
    ah "You did the face thing again."
    mc "That's just my regular face. I can't take it off."
    sa "So... am I supposed to be answering questions? I feel like I skipped a step."
    mc "Depends. Have you been briefed?"
    sa uniform curious "She said not to take you seriously until you'd eaten or something like that."
    "{i}Useful briefing. Wish she'd given it to me.{/i}"
    mc "Well, you've survived the first round."
    sa "And how many are there?"
    mc "...Classified."
    "He looks toward the kitchen, then back at me."
    sa uniform happy "I should probably eat before round two, then, heh."
    show asahina uniform neut
    ah "Don't encourage him, he's a freaking weirdo."
    "A smile keeps tugging at one corner of her mouth."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "While Mom heats the leftovers using the air fryer, Asahina brings her books down and spreads them across most of the coffee table."
    call nier_clear from _call_nier_clear_0516_7
    pause 2.0
    scene bg living_room
    $ show_calendar()
    show asahina uniform thinking at t21
    show sam uniform neut at t22
    $ atmos("home")
    with wipeleft_scene
    "Asahina has three notebooks on the table and a fourth on her knee, where she writes until the page slides sideways. Sam holds the corner down with his book."
    show asahina uniform frustrated
    ah "Gah, this one's wrong...!"
    sa "Which part?"
    ah "The answer says negative six. I keep getting six, and I've done it three times!"
    show sam uniform teasing
    sa "Let me see your working. Maybe it's a typo."
    "She turns the notebook toward him so he can follow the pencil marks without leaning across her."
    show sam uniform neut
    sa "Ah, here. You lost the minus when you copied this down. The factoring's right."
    show asahina uniform annoyed
    ah "Oh, for firetruck's sake! I checked that bit!"
    mom "Asahina..."
    sa "No worries, I do it all the time, as does everyone else and their mothers. Try putting the new line underrrrrr... this one."
    "He circles around a line while she rewrites it next to the original problem, checks the next two answers from her working, and snaps the lead while underlining the last one."
    ah uniform frustrated "Grrrrrrrrrrraaaaaaaaaaaaaaahhhhhhhhhh...!"
    mom "Plates are out! Come get it while it's hot, you three!"
    show asahina uniform neut
    ah "Yeah, in a minute!"
    "Sam gets up while she looks for another pencil. When he comes back, he puts one of the two plates beside her notebooks."
    show asahina uniform unamused
    ah "I said in a minute, dude."
    sa "I know. It's just there now, so you don't have to get up when you're ready."
    "She moves a notebook to make room for the plate, then picks up a new, slightly shorter pencil and starts the next question."
    show sam uniform curious
    sa "Oh, hey, settle something for me. She says you finish the main story and then never touch the postgame."
    "I stop on my way to the kitchen."
    menu:
        "\"It's a scheduling thing.\"":
            $ s1_pick("sam_first_read", "guarded")
            mc "It's a scheduling thing."
            mc "...Mostly."
        "\"The credits change the game.\"":
            $ s1_pick("sam_first_read", "honest")
            mc "Credits roll and it stops being the same game. So I stop."
            mc "Well, actually, back that up. There {i}are{/i} exceptions."
        "\"I'm actually a completionist.\"":
            $ s1_pick("sam_first_read", "joking")
            mc "Nah, I do everything from start to finish and everything in between."
            mc "Gotta get that one-hundred percent achievement, y'know?"
    show sam uniform happy
    sa "Eh, fair 'nuff. I keep finding other stuff to do. By the time I finish the story, I've forgotten how it even started or what I'm supposed to do."
    show asahina uniform smug
    ah "Four hundred whole hours in the sandbox game, which is a lot for him. He showed me the clock like he was proud of it."
    sa "I mean, I did get a lot done, so..."
    mc "And most of that was side-questing?"
    show asahina uniform teasing
    ah "Don't get him started! He'll show you the house and everything that he spent literal days farming resources for."
    mc "There's a house, eh?"
    sa "There are a few. I kiiiiinda got carried away with the building tools."
    "He finds a picture on his phone. One of his houses has a moat, which raises several questions I ask while getting my dinner."
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg kitchen_evening
    $ show_calendar()
    show mom neut at t22
    show sam uniform neut at t21
    $ atmos("home")
    with wipeleft_scene
    "Later, I find the guy in the kitchen rinsing a glass while Mom packs the last of the rice into a container."
    mom curious "You don't have to do that, Sam."
    sa "It's fine, really. I used it, so I should clean it."
    mc "Careful now. Keep that up and she'll invite you back."
    mom smug "He can come back."
    "Sam's grin gets away from him."
    sa uniform happy "I'd like that."
    "Asahina, from the living room, makes a triumphant noise."
    ah "Booyah!"
    mom annoyed "Homework done, then?"
    ah "Ages ago! Can we have the movie now?"
    mom "{i}*sigh*{/i} ...Go on."
    "I can hear the living room TV booting up to a streaming service before Mom can change her mind."
    show sam uniform neut
    mom curious "Think Asahina will take this for lunch tomorrow? She barely touched dinner."
    "By now, the TV has deafened any other sound in the next two rooms over with trailers and ads, leaving us to have our conversation with no prying ears."
    "Sam dries the glass and glances toward the living room. The towel stops in his hands."
    sa uniform thinking "She's been trying to cut back on junk food."
    mc "She told you that?"
    sa uniform neut "Yeah. Asked me not to make a big deal out of it, though."
    mom curious "What did she say?"
    sa uniform thinking "That she wants to eat better. So I brought dinner over and left her to it, hence why... well, her plate felt neglected."
    mc "And did she eat?"
    sa uniform neut "Some. I wasn't watching everything she did, but y'know."
    "He says it to the glass."
    "Mom's closer to him than I am. I leave her to answer and rinse the fork I've been carrying."
    sa uniform worried "I don't want every meal turning into a thing about what she's eating. I really shouldn't be the one to say all this, I'm literally just some guy you met."
    mc "She gets annoyed when we ask, too."
    sa uniform neut "Yeah. Better to let her eat than keep asking why she isn't. Something, something, forgiveness over permission, right?"
    show mom worried
    "Mom has to press the lid twice before it seals, holding the container against the counter with her other hand."
    "She writes Asahina's name across the lid in black marker, then puts the container on the refrigerator's front shelf."
    $ mark_character_met("sam")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Sam leaves sometime after dinner. Asahina walks him to the door and takes three times longer than necessary to come back inside."
    nier "Nobody comments on it."
    call nier_clear from _call_nier_clear_0516_8
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music night_a
    "By nightfall, I am back in my room with my phone in one hand and my planner open on my desk."
    "I only get the planner out when memory alone starts to feel like a bad idea. Saturday still has school attached to it like a punishment with better branding."
    call enter_m_show_planner("SATURDAY", "MAY 17", planner_0516_saturday, "SUNDAY", "MAY 18", planner_0516_sunday, "chip restitution = Asa's problem", "'date' is a normal word. stop thinking about it.") from _call_enter_m_show_planner_0516_1
    "{i}My free time already feels pre-owned.{/i}"
    "A muffled laugh rises from downstairs, probably Asahina texting Sam. Mom says something after that, too faint for me to catch."
    "I underline the 'MAYBE' beside the school printout, as though making it more tentative will help me get to it."
    "..."
    "I remember the lunch container on the front shelf, with her name written across the lid."
    $ hide_calendar()
    scene black with dissolve_scene_full
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0516_1
    jump a0517
