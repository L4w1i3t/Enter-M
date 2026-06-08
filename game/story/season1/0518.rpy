label a0518:
    # --- Day 4: 2025-05-18 ---
    scene bg living_room
    show asahina neut at t11
    $ show_calendar()
    with dissolve_scene_full
    play music dailyleisure
    
    ah "Ugggh, why is there nothing good on?!"
    "My sister continues to flip through the channels on the TV with a force that makes you think it offended her."
    ah "Why did the Geographic have to have downtime now of all times?!"
    
    mc "Maybe this is the universe's way of telling you to expand your horizons."
    
    ah "I'll expand them whenever YOU give me back my DVD of 'The Grandfather.'"
    
    mc "...I have no idea what you're talking about."
    ah "You've had it for two weeks now!"
    
    "I plead the fifth with a long sip of coffee."
    "{i}Tastes awfully thick...{/i}"
    # CRITIQUE: Proofreading nit: "could" shifts this sentence into past conditional while the surrounding narration is present/present-perfect. Keep the tense consistent unless the stumble is intentional.
    "And before I could put the cup down, I feel my phone buzz in my pocket."
    mc "Ah frick, she beat me..."
    
    ah "Oh? Care to share?"
    ah "Is it your girlfriend?"
    
    mc "Once again, Asa, she is not my--"
    mc "...Actually, no. We're not doing this."
    mc "It's really not that deep. Monika and I made plans to catch a movie today, that's all."
    "Asahina lightly punches my shoulder."
    
    ah "Ohhhh. Watch out, if your girlfriend catches wind of your other girlfriend, things'll get bad real quick~"
    
    "I lay my cup back on the coaster."
    mc "...We still need to pick a time, so let me follow up with her real quick."
    mc "Also, you put WAY too much milk in the coffee this morning."
    
    ah "Hm? I didn't make it, mom did."
    
    mc "...Be real."
    "I continue to give my sister the stare of skepticism as I press the power button on my phone."
    python:
        _phone_messages = [
            phone_msg("them", "Morning! I looked online and it looks like there are available showings at noon, a couple hours after that, and the evening. I don't really mind which, so I'll leave it up to you."),
            phone_msg("me", "You know I'm bad at decisions, Monika."),
            phone_msg("them", "Oh, don't be like that. I know you can do it~"),
            phone_msg("me", "Fine, uh..."),
            phone_msg("me", "Noon, then?"),
            phone_msg("them", "Works for me! Meet up at the theater, or what's convenient for you?"),
            phone_msg("me", "Theater's fine."),
            phone_msg("them", "Great! See you then!"),
            phone_msg("them", "Don't stand me up now!")
    ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0518_1
    "I take a deep breath."
    
    ah "You good there? Looks like something's annoying you."
    
    mc "Just a nosy sister that gets under my skin."
    "Asahina looks at me, unamused."
    mc "...Okay, fine, real talk, jokes aside."
    mc "It's not that I'm annoyed, per se..."
    mc "Sometimes I just don't know what to do when somebody's so in your face about things."
    
    ah "I think I get it..."
    
    mc "Here, I'll just show you."
    mc "And I swear to everything that is holy, do NOT scroll too far up or start digging through things."
    "I turn over my phone's chat history to her and she reads through the texts in a scarily surgical manner."
    "Half a minute passes before she hands me back my phone and reaches for her own."
    # CRITIQUE: Texting while sitting next to each other is a funny bit, but it also repeats information the scene could handle through body language. Use the text format only if secrecy or timing adds something.
    "Some tapping and typing later, and I feel a vibration."
    python:
        _phone_messages = [
            phone_msg("them", "dude she is so into u"),
            phone_msg("me", "I'm not dense, Asa."),
            phone_msg("them", "well why dont u go for her? shes nice and pretty"),
            phone_msg("them", "i can be ur wingwoman if u want"),
            phone_msg("me", "You are the last person I want for that job."),
            phone_msg("me", "And why are we texting when we're sitting right next to each other?"),
        ]
    call phone_text_conversation("Asa", _phone_messages, append=True) from _call_phone_text_conversation_0518_2
    "Asahina looks at me and shrugs."
    "She then proceeds to return to flipping through channels on the TV that neither of us care about."
    "{i}Noon...{/i}"
    "{i}Still got a couple hours before I need to get ready.{/i}"
    "{i}Might as well kill time the usual way...{/i}"
    show asahina at thide
    hide asahina
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "After finishing my coffee in the living room, I find myself back upstairs."
    call nier_clear from _call_nier_clear_0518_1
    scene bg bedroom
    $ show_calendar()
    with wipeleft_scene
    mc "Alright, game..."
    mc "Time to sink my teeth into you..."
    mc "...But only a moderate amount cause I have a life."
    $ hide_calendar()
    stop music fadeout 2.0
    scene black with dissolve_scene_full
    scene bg city_day
    $ show_calendar()
    with dissolve_scene_full
    play music daily
    "Late morning settles over the shopping street in layers: delivery carts along the curb, steam leaking from a noodle shop vent, the soft clatter of shutters being pulled up for lunch, et cetera."
    "I check my phone at the crosswalk. Monika's last message is still there, cheerful enough to make the screen feel brighter than it is."
    "The signal changes before I finish reading it for the third time and contemplating whether I should let her know I'm on my way."
    "I pocket the phone and cross with the crowd, careful this time to keep my eyes ahead."
    "My shoulder aches with a faint reminder from yesterday evening."
    "Nothing major, but just enough to make me notice the space between people."
    "By the time the theater sign comes into view, a small line has already gathered under the {i}Iron Rod{/i} banner."
    "{i}Seems like the hype and promos did their job...{/i}"
    "{i}Now where is she...?{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    scene bg theater_day
    $ show_calendar()
    with wipeleft_scene
    "The theater entrance is louder than the street."
    "A staff member tapes one more {i}Iron Rod{/i} notice to the glass while the line inches around him without complaint."
    "Near the ticket machines, two kids in plastic wrist morphers argue over their favorite members of the Mighty Lightning Squad."
    "One keeps insisting Blue Surge has the best finisher. The other looks personally betrayed by the idea that Yellow Arc is not the obvious answer."
    "{i}Are they even here for the same movie?{/i}"
    "Their parents let the debate happen and stare at the showtime board with the patience of individuals who have played these games before."
    "I stand near the display case, half-watching the crowd and half-listening for my phone."
    show monika 1b at t11
    m "Hey! Look who beat me here!"
    "Monika lifts a hand as she comes through the crowd. Her pace is quick until she sees me, then it eases."
    "A loose strand of hair has slipped free near her cheek. She tucks it back with the side of one finger."
    mc "Yeah... Something tells me I should've left earlier."
    m "I know, right? Like three different groups are taking pictures with the poster by the doors."
    mc "Yeah, not out of the ordinary. You wanna take one?"
    mc "...Cause I don't. Count me out."
    "For a second we both look at the banner instead of each other."
    m "I exchanged the vouchers when I checked the times. Noon still had seats together."
    m "The later showings were already getting picked over, to absolutely nobody's surprise."
    "She pulls two tickets from her bag, already folded once down the middle."
    mc "For a movie that hasn't even premiered yet, that's kind of wild."
    m "To be fair, people have been talking about {i}Iron Rod{/i} for months."
    m "At this point, half the audience is probably here to find out if the hype was lying."
    "She hands me one ticket. Her fingers brush mine, then draw back without making anything out of it."
    mc "And the other half?"
    m "Here to be scared on purpose...or something...maybe."
    mc "You know that it's alright to not have the answer to everything, right?"
    "I look down at the ticket, then at the poster beside us."
    "The longer I stare at both, the more it starts looking like something waiting to move."
    mc "...Right. Anyway..."
    m "You're rubbing your shoulder."
    # CRITIQUE: Good intimate cue. Do not rush past Monika noticing his body before he explains it; this is the sort of quiet attention that makes her affection believable.
    mc "...Yeah?"
    mc "I ran into someone last night."
    m "Ran into, as in...?"
    mc "Literally. Phone out, brain elsewhere. Not exactly my finest moment."
    "Monika's expression shifts, just a little. Not alarmed. More like she is deciding whether to ask the next question."
    m "Well...are you good?"
    mc "Yeah. Just a little sore, no need for vapor rub or anything like that."
    m "Ah."
    "The automatic doors open again, spilling cold air over the sidewalk."
    "Monika folds her ticket against her palm and nods toward the entrance."
    show monika at thide
    hide monika
    $ hide_calendar()
    scene black with wipeleft_scene
    scene bg theater_lobby
    $ show_calendar()
    with wipeleft_scene
    play sound moddooropen
    show monika 1a at t11
    "Inside, the air conditioning cuts through the heat at once."
    "The lobby smells like popcorn, floor cleaner, and spilled cola that someone has already mopped but not quite defeated."
    "The line for concessions moves with practiced slowness."
    "At the register, Kotonoha slides a tray of nachos across the counter, checks the next order on the screen, and looks up."
    show monika at t21
    show kotonoha neut at t22
    mc "Yo."
    ko "Good afternoon, [player], Monika."
    "Her theater vest is buttoned straight, and the name tag sits exactly level."
    "Monika steps up beside me and studies the menu board."
    m "Do you want anything?"
    mc "Maybe a drink, I guess."
    "She waits long enough for me to notice she is leaving the rest of the decision alone."
    mc "...And popcorn is probably smarter before the movie starts."
    m "Let's go with that then."
    ko "Combo B is cheaper with two drinks."
    "Kotonoha says it with the same calm certainty she used for the loose glue cap yesterday."
    m "Combo B, please. Medium popcorn."
    ko "Salted?"
    "Monika glances at me."
    mc "Sure."
    m "Salted and churro toppings!"
    # CRITIQUE: The concession scene stacks "second mother," "brochacho," the price shock, and the huge tip too tightly. One joke can sharpen awkward date energy; four jokes turn it into sketch comedy.
    mc "That is not what I said...!"
    "{i}I swear, what is she, my second mother?!{/i}"
    "Kotonoha taps the order in, then reaches for two cups without looking away from the register."
    ko "{i}Iron Rod{/i} is in theater three. Doors open in five minutes."
    m "Oh, that soon?"
    ko "The trailers are longer than usual."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Kotonoha spends the next half minute prepping our food and drinks."
    nier "Her pace matches that of professionals, with half the visible effort."
    nier "Our combo order consists of one extra large bucket of popcorn and two drinks, as insisted."
    call nier_clear() from _call_nier_clear_0518_2
    scene bg theater_lobby
    $ show_calendar()
    with wipeleft_scene
    show kotonoha neut at t22
    show monika 1a at t21
    ko "Your total is on the screen."
    "{i}SHIT, that's a lot!{/i}"
    "Monika pays before I get my wallet halfway out."
    mc "...I can get it. Seriously."
    m "Hey, I was the one who invited you. I got this, brochacho."
    "Monika looks down first, busying herself with the cup lids."
    "I take the popcorn because it gives my hands something to do."
    "{i}WHY DID YOU TIP TWENTY-FIVE PERCENT, MONIKA?!{/i}"
    ko "Enjoy the film."
    mc "Thanks, you too--"
    mc "...Uh..."
    "{i}And thus begins my walk of shame out of this social transaction.{/i}"
    m "Thank you, Kotonoha!"
    show kotonoha at thide
    hide kotonoha
    show monika at t11
    "Kotonoha nods once and turns to the next customer."
    "Past the concession stand, theater three waits with its doors propped open and a strip of red carpet rolled crookedly across the threshold."
    "Monika balances both drinks against her chest, then leans one toward me."
    m "Ready?"
    mc "...Sure."
    "She smiles, softer than before."
    m "Good, me neither."
    "We head in before either of us can make that sound more important than it is."
    show monika at thide
    hide monika
    $ hide_calendar()
    scene black with wipeleft_scene
    scene bg theater_inside
    $ show_calendar()
    with wipeleft_scene
    show monika 1a at t11
    "Theater three has the particular darkness of a room pretending the outside world does not exist."
    "The screen is still blank, but the speakers are already filling the room with a low advertisement loop that makes every snack look like it was photographed by someone with too much confidence."
    "Monika finds our row before I do, because of course she does."
    m "This should be us..."
    "She steps aside to let me in first. I take the inside seat, partly because it's polite and partly because the aisle seat feels like it belongs to someone who has an escape plan."
    "The popcorn bucket lands between us like a treaty."
    mc "You know, I feel like theater popcorn used to be cheaper."
    m "Everything used to be cheaper."
    m "That's how time works, don'tcha know?"
    mc "I don't like your tone, Ms. Economy."
    m "Then stop making easy observations, haha!"
    "I reach for popcorn and immediately regret it when the churro topping announces itself with enough cinnamon to make my fingers look like evidence."
    mc "...This is a crime."
    m "It's good, though, right?"
    mc "That is {i}not{/i} what I said."
    m "Don't worry, I know what you meant~"
    "She takes a piece for herself, then looks at the screen as the lights dim another step."
    "The room settles into the shared hush of strangers agreeing to be quiet at the same time."
    "For a while, neither of us says anything."
    "It should be normal. It IS normal."
    # CRITIQUE: "Nanoangstrom" is funny, but it is so self-consciously technical that it briefly pulls attention away from the physical intimacy. Consider whether MC would think in this exact unit under romantic pressure.
    "{i}So why am I suddenly aware of every nanoangstrom between our shoulders?{/i}"
    m "Hey."
    mc "Hm?"
    m "You can laugh if the movie gets stupid, by the way."
    m "I won't report you to the horror fan committee."
    mc "...There's a committee?"
    m "Obviously! They meet in a basement and argue about which VHS tapes are best all the friggin' time."
    mc "Sounds credible..."
    "The opening starts with a thunderclap loud enough to make someone in the front row jump."
    "Monika tries not to smile and fails miserably."
    "{i}Alright. Movie time.{/i}"
    show monika at thide
    hide monika
    $ hide_calendar()
    scene black with wipeleft_scene
    # CRITIQUE: The movie is summarized right when it could mirror the date. Show one scene and one shared reaction in real time so the sleeve-grab later feels rooted, not reported.
    nier "The movie begins with a slow shot of an empty railway crossing, a missing-person flyer, and a rural silence that makes every audience member decide the characters should simply leave."
    nier "They do not leave, as no characters do in these kinds of movies."
    nier "This is because horror movies are powered by bad real estate decisions and people hearing a noise in the basement."
    call nier_clear from _call_nier_clear_0518_3
    nier "{i}Iron Rod{/i} isn't bad, actually."
    nier "It's uneven in places, sure. The second act gets a little too impressed with its own symbolism, and one of the token side characters exists solely to hold a flashlight wrong."
    nier "But when it works, it works."
    nier "Monika watches with the focus she gives poems, only this time nobody's margins are in danger."
    call nier_clear from _call_nier_clear_0518_4
    nier "At one point, her hand finds my sleeve during a scene involving a maintenance tunnel and a sound that absolutely did not need to come from behind us."
    nier "She lets go immediately after."
    nier "Neither of us mentions it while the movie is still happening."
    call nier_clear from _call_nier_clear_0518_5
    scene bg theater_inside
    $ show_calendar()
    show monika 1a at t11
    with wipeleft_scene
    "The credits crawl up the screen while half the audience starts the sacred ritual of blocking the row before anyone can stand."
    "I stay seated, mostly because the people beside us are still negotiating popcorn logistics with the intensity of a hostage situation."
    m "...Well?"
    mc "I liked it."
    mc "The part with the maintenance tunnel was cheap, though."
    # CRITIQUE: The sleeve-grab was emotionally charged, but the aftermath immediately becomes a retort chain. Let embarrassment sit for two or three lines before joking over it.
    # CRITIQUE: This line appears malformed. The intended idiom might be "cheap tricks work sometimes" or "don't count cheap out"; as written, it reads like a draft error.
    m "Hey, don't cut cheap out sometimes."
    mc "...Says the person who tried to tear my arm off."
    m "I did not!"
    "Her face goes pink faster than the house lights come up."
    mc "I'm not judging. If a movie wants to jumpscare you with plumbing, that's between you and said plumbing."
    m "I was startled for maybe, like, half a second."
    mc "Talk about a grippy half-second then."
    m "Okay, okay! Fine, it got me {i}once{/i}."
    "She folds her empty straw wrapper into a tiny rectangle, then folds it again."
    m "But you jumped at the opening thunder."
    mc "Just a louder audio mix than I expected..."
    m "Suuuuuuuure, let's go with that."
    "We stand once the row clears, carrying the remains of our snacks like evidence from a crime scene."
    show monika at thide
    hide monika
    $ hide_calendar()
    scene black with wipeleft_scene
    scene bg theater_lobby
    $ show_calendar()
    show mood_afternoon zorder 3 
    show monika 1a at t21
    show kotonoha neut at t22
    with wipeleft_scene
    "The lobby has changed flavors while we were gone."
    "Earlier it was anticipation, but now it's spilled reactions: people arguing over the ending, parents corralling children, someone near the poster loudly insisting the book did it better."
    ko "Was the movie satisfactory?"
    mc "That's a very...customer-service way to ask."
    m "It was good! A little messy at a couple points, but good."
    ko "Messy is usually more memorable."
    "Kotonoha gathers abandoned napkins from the counter and stacks them with surgical neatness."
    mc "You seen it yet?"
    ko "No."
    ko "Employees are encouraged to avoid spoilers so we can maintain neutrality when customers yell about endings."
    mc "Sounds like a line from the handbook."
    ko "It should be. Maybe I'll bring that up at the next staff meeting."
    "Monika laughs into her cup lid."
    m "For what it's worth, we won't yell."
    ko "I appreciate that."
    "A customer waves from the other end of the counter. Kotonoha looks over, then back at us."
    ko "Have a good afternoon."
    mc "You too."
    m "Bye, Kotonoha!"
    show monika at t11
    show kotonoha at thide
    hide kotonoha
    "She nods once and returns to work."
    "Monika and I drift toward the doors with the crowd."
    show monika at thide
    hide monika
    $ hide_calendar()
    scene black with wipeleft_scene
    scene bg theater_day
    $ show_calendar()
    show mood_afternoon zorder 3 
    show monika 1a at t11
    with wipeleft_scene
    "Outside, the afternoon hits us with the heat it had been saving."
    "The line for the next showing has already started curling toward the poster again."
    "For a second, neither of us moves."
    m "So..."
    mc "So."
    "There are several normal things I could say."
    "Thanks for inviting me. That was fun. Sorry about making you buy popcorn with dessert seasoning. Please never tell anyone I almost pissed myself."
    "My brain, ever the professional, files all of them incorrectly."
    mc "Your horror committee sounds corrupt."
    m "Oh, extremely."
    m "But they have good snacks and tea!"
    "She adjusts her bag on her shoulder and looks down the street."
    m "I should probably head home before I talk myself into buying a second ticket just to overanalyze the ending."
    mc "...You'd do that?"
    m "No."
    m "...Maybe."
    m "Does it matter?"
    mc "Dangerous honesty."
    m "I'll text you later if I come up with any grand theories."
    mc "Looking forward to your essay."
    m "It'll be very professional, trust."
    "She starts to leave, then pauses like she remembered something she had already decided not to say."
    m "Hey, [player]?"
    mc "Yeah?"
    m "Thanks for coming with me."
    "The simple version of the sentence lands harder than it has any right to."
    mc "Yeah. Anytime."
    m "Good."
    "Then she waves and heads down the sidewalk, ponytail swaying behind her."
    show monika at thide
    hide monika
    "I wait until she reaches the corner before checking my phone, because apparently today I am committed to having no idea what to do with my hands."
    "{i}Anytime, huh?{/i}"
    "{i}Real smooth, man.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The ride home gives me too much time to think, which is rude of public transportation."
    # CRITIQUE: "I think about an analysis of the movie" is abstract phrasing. "I think about analyzing the movie" or one concrete image from it would read more naturally.
    nier "I think about an analysis of the movie, with both the good and bad parts."
    nier "I think about that Matsuda girl's name sitting in my messages like it rented space there."
    nier "I think about the fact that Sunday has somehow become less restful than Saturday."
    call nier_clear from _call_nier_clear_0518_6
    stop music fadeout 1.0
    pause 1.0
    scene bg living_room
    $ show_calendar()
    show mood_evening zorder 3 
    with wipeleft_scene
    play music dailyleisure
    play sound moddooropen
    "When I get home, Asahina is still in the living room."
    "The poster is propped against the couch now, which means it has graduated from crisis to object."
    "Big block letters, clean spacing, a volleyball drawn with enough detail to make me suspicious of how much effort she pretended not to spend on it."
    show asahina neut at t11
    ah "Well?"
    
    mc "Well what?"
    
    ah "Movie. Date. Whatever. Spill it."
    
    mc "It was...a movie."
    
    ah "Wow. Thank you for the important info."
    
    "I take my shoes off and decide whether honesty is worth the ammunition."
    "Unfortunately, my mouth has historically been bad at committee decisions."
    mc "It was fun. Monika and I both seemed to enjoy it."
    
    # CRITIQUE: This homecoming has genuine warmth around the poster, but the "stupid face" and "birdbrain" tags keep yanking tenderness back into insult mode. Space the barbs out or the praise cannot breathe.
    ah "Awwwwwwwwwwwwwwwwwwwwwwwww."
    
    mc "Do not."
    
    ah "I didn't say anything!"
    
    mc "You said it with your stupid face."
    ah "S-Shut up! You're one to talk!"
    
    mc "...How mature of you."
    "She leans back on her hands, then glances at the poster like she is pretending not to wait for me to notice it."
    mc "Poster looks good, by the way."
    
    ah "Obviously."
    
    "Her voice tries for casual and misses by a small, embarrassing margin."
    mc "Especially the lettering."
    
    ah "...Yeah?"
    
    mc "Yeah."
    "She turns away too quickly, which is how I know that one actually landed."
    
    ah "Cool."
    ah "Now go away before your cinnamon smell ruins it."
    
    mc "Gladly."
    "I head toward the stairs, then stop near the first step."
    mc "Oh, and Asa?"
    
    ah "What?"
    
    mc "If the volleyball team doesn't appreciate the poster, I will personally call them tasteless hacks."
    
    ah "Please don't, they're still my friends."
    
    mc "No promises."
    
    ah "...Thanks, birdbrain."
    
    "I keep walking before she can see the smirk on my face."
    show asahina at thide
    hide asahina
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Sunday evening drifts in without asking permission."
    nier "Mom asks about the movie over dinner. Asahina answers half the questions for me, confidently and incorrectly."
    nier "I correct none of it unless absolutely necessary."
    call nier_clear from _call_nier_clear_0518_7
    stop music fadeout 1.0
    pause 1.0
    scene bg bedroom
    $ show_calendar()
    show mood_night zorder 3 
    with wipeleft_scene
    play music fantasyserenity
    "My room is quiet when I finally get back to it."
    "My new game still waits by the console."
    "My phone waits beside it, considerably less quiet."
    python:
        _phone_messages = [
            phone_msg("them", "Okay, theory: the iron rod wasn't actually the weapon. It was the promise."),
            phone_msg("them", "Wait, that sounded better in my head."),
            phone_msg("me", "No, keep going. I want to see how deep the committee corruption goes."),
            phone_msg("them", "You joke, but I have notes and stuff."),
        ]
    call phone_text_conversation("Monika", _phone_messages, append=True) from _call_phone_text_conversation_0518_3
    "I set the phone down and stare at the ceiling."
    "A movie, a poster, a few messages..."
    "{i}Normal things.{/i}"
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The rest of the night slips by in fragments: homework I remember too late, a game I open for exactly long enough to lose track of time, and Monika's theory messages arriving in clusters."
    nier "By the time I finally sleep, the day has left too many tabs open in my head."
    call nier_clear from _call_nier_clear_0518_8
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0518_1
    jump a0519
