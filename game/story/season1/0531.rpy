label a0531:
    # --- Day 17: 2025-05-31 ---
    # Final day of Chapter 0.5. The existing Saturday plan converges without Matsuda
    # manufacturing access: MC joins after track, Asahina joins after volleyball, and
    # Tsubaki gets the bookstore first. Matsuda becomes the day's center because the
    # group genuinely has fun with her, and the decisive next invitation comes from MC.
    # This is the clean, reciprocal beginning the later overdependence must grow from.
    # Ledger meters moved: Matsuda gains a recurring place in MC's schedule; Tsubaki
    # keeps and voices preferences; Asahina's edited schedule remains her own; Monika's
    # unfinished doorway poem retains weight; Mom's work stays ordinary but present.
    pause 2.0
    scene bg dining_table
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music dailyleisure
    "All three chairs are occupied, which has not been true on a school morning in longer than I want to count."
    "Mom is at the end of the table with her hair still pinned up from yesterday, a mug between both hands, and no folder in sight."
    "Asahina has one knee bouncing beneath her chair while she eats toast and checks the time every few bites."
    show mom teasing at t22
    show asahina determined at t21
    mom "If either of you looks at the clock again, I am charging it rent."
    ah "I have volleyball."
    mc "I have school."
    show mom smug
    mom "So does the clock. It has been attending faithfully all morning."
    "A slice of toast comes apart in half, and the interrogation begins."
    ah "You packed your arcade card, right?"
    mc "Yes."
    ah "Phone charger?"
    mc "Yes."
    ah "Actual money?"
    mc "I survived before you became logistics manager."
    show asahina smug
    ah "Debatable."
    "She checks her own bag with one hand and finds the edge of her kneepads. The blue schedule on her phone is open beside her plate, its old two-hour biology block cut down to forty-five minutes tomorrow morning."
    "Nothing else has moved into the space it left."
    show mom curious
    mom "You both remember what I said."
    show asahina unamused
    ah "Text when we leave the arcade, tell you if food happens, don't accept rides from strangers, no felonies."
    show mom unamused
    mom "I did not say the last one because I hoped it was implied."
    mc "Should've put it in writing."
    show mom happy
    mom "No felonies. There."
    ah "There goes my whole afternoon."
    "The mug covers everything except her eyes. They do the smiling for her as she sets it down."
    show mom determined
    mom "And [player], track ends before the outing begins."
    mc "Coach already made that very clear."
    show mom teasing
    mom "Your blood?"
    mc "Printer ink, probably. He has standards."
    show mom neut
    mom "If the foot hurts, you stop. An arcade will remain an arcade without you."
    mc "I know."
    show mom determined
    mom "Say the rest."
    mc "And missing one afternoon will not destroy my social life."
    show asahina teasing
    ah "What social life?"
    show mom unamused
    mom "Asahina."
    ah "Sorry. Reflex."
    show asahina happy
    "She hides the next bite behind her hand, but the grin still reaches me."
    mc "The foot gets the final say. I remember."
    mom "Good."
    "Her phone vibrates against the table."
    "She reads it, then finishes the sip already in progress before she stands. This is apparently what restraint looks like before eight on a Saturday."
    show mom at thide
    hide mom
    "She crosses the kitchen and types a short reply with both thumbs."
    show asahina curious
    ah "Work?"
    mom "A question that can survive until Monday."
    "She turns the phone facedown beside the sugar bowl and returns to her chair, letting the morning keep her after all."
    show mom determined at t22
    show asahina determined
    ah "Sunday rematch still happening?"
    mom "After biology."
    ah "Forty-five minutes."
    show mom teasing
    mom "Forty-five honest minutes. Then you may deploy every unethical expansion card you own."
    show asahina smug
    ah "Finally, a fair deal."
    "The jam moves across the table before Asahina asks for it."
    # SFX SUGGESTION: A phone vibration rattling audibly against the kitchen table.
    "My phone buzzes against the table. The chat called Saturday has developed overnight."
    python:
        _phone_messages = [
            phone_msg("them", "Matsuda: Dawn report. The bookstore opens at one."),
            phone_msg("them", "Tsubaki: It has opened at one every Saturday for twelve years."),
            phone_msg("them", "Matsuda: Reliability deserves celebration."),
            phone_msg("them", "Asahina: some of us are trying to eat"),
            phone_msg("them", "Matsuda: Then eat magnificently."),
            phone_msg("me", "Track should release me around two. I'll meet you at the bookstore if you're still there, arcade if not."),
            phone_msg("them", "Tsubaki: We'll probably still be there."),
            phone_msg("them", "Matsuda: She has discovered the clearance tables. I no longer control our departure."),
            phone_msg("them", "Tsubaki: We have not arrived yet."),
        ]
    call phone_text_conversation("Saturday", _phone_messages, status="3 participants", append=True) from _call_phone_text_conversation_0531_1
    "The phone comes down two inches and my side of the table falls under observation."
    show asahina curious
    ah "She starts early."
    mc "The bookstore has shown dangerous consistency."
    ah "I meant Matsuda."
    "A second piece of toast leaves the plate."
    show mom smug
    mom "You sound amused."
    mc "I'm choosing patience."
    show asahina smug
    ah "You typed back in seven seconds."
    mc "Efficient patience."
    "Asahina gives Mom a look that says she has proved her point. Mom declines to receive it."
    "We finish breakfast with the clock still employed and all three chairs where they belong."
    "Before we leave, Mom checks that Asahina has her water bottle and that I am not pretending my track shoes packed themselves."
    "Then she stands in the entryway and sends us out with the same instruction twice."
    show mom happy
    mom "Have fun."
    show asahina happy
    ah "We'll try."
    mc "No promises."
    show mom determined
    mom "That was not a request for modesty. Have fun."
    "The second version leaves less room to dodge."
    mc "All right."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The last school morning of May is short enough that everyone treats it like a hallway between better rooms."
    nier "Asahina peels away toward the gym. I climb the stairs with my track bag knocking against one leg and Matsuda's bookstore updates arriving against the other."
    nier "By first bell, Tsubaki has vetoed two route changes and one proposed dress code for the arcade. The plan survives all three."
    call nier_clear from _call_nier_clear_0531_1
    stop music fadeout 1.0
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    with dissolve_scene_full
    play music schooldays
    "Saturday classes make the bare minimum attempt at education."
    "Language arts returns our exam reflections without comment. Algebra assigns six problems for Monday, which inspires a low wave of betrayal across the room. Civics spends twenty minutes on committee procedure while half the class practices a less formal method of leaving early with their eyes."
    "The midterm portal stays locked until Monday."
    "Six numbers wait on the far side of the weekend, but they have lost the power to rearrange the furniture in my head."
    "I copy the algebra problems and make it to the final bell with next week still filed under next week."
    # SFX SUGGESTION: The final bell immediately overtaken by a roomful of chairs scraping back.
    "Chairs scrape back before the sound finishes."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The building empties by destination. Volleyball turns left at the gym corridor. Track cuts across the courtyard. Everyone else pours toward the gates at the speed of a student body that has just repossessed its Saturday."
    nier "I'm halfway down the stairs when Monika calls my name from above."
    call nier_clear from _call_nier_clear_0531_2
    stop music fadeout 1.0
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music dailyfantasy
    show monika forward uniform neut cm oe nobl rdown ldown at t11
    "Monika descends with a canvas bag over one shoulder and yesterday's green pen clipped to the outside pocket."
    m forward uniform happ om oe nobl rdown lpoint "You move fast when literature is no longer holding you hostage."
    mc "Track has a whistle. You only have stationery."
    m forward uniform happ cm ce nobl rdown ldown "Do not underestimate stationery."
    "She reaches the landing and falls into step beside me."
    m forward uniform curi om oe nobl rdown ldown "Still going out after practice?"
    mc "That's the plan."
    m forward uniform happ om oe nobl rdown ldown "Bookstore, arcade, mysterious third location where teenagers discover they need food?"
    mc "The group chat still hasn't picked food."
    m forward uniform laug om ce nobl rdown ldown "Good. A little uncertainty builds character."
    "She adjusts the canvas strap. One of the rescued club journals protrudes from the top."
    mc "You're taking club work home?"
    m forward uniform wry cm oe nobl rhip ldown "I'm taking one journal home. There is a difference."
    mc "How many folded prompts are in the bag?"
    "Her hand settles over the opening."
    m forward uniform nerv om oe awkw rdown ldown "Privileged information."
    mc "Thought so."
    "We reach the doors. Sunlight cuts a white rectangle across the floor between us and the courtyard."
    m forward uniform happ om oe nobl rhip lpoint "Monday. One line."
    mc "The traveler has until then."
    m forward uniform happ cm ce nobl rdown ldown "The traveler has had a full day already."
    mc "Public transit is complicated."
    m forward uniform wry om oe nobl rdown lpoint "So is going through a door, apparently."
    "The tone is light. Her fingers find the green pen and turn it once against the bag seam."
    m forward uniform neut cm oe nobl rdown ldown "I want to read where you send them."
    mc "I'll write something."
    m forward uniform happ cm oe nobl rdown ldown "That is all I ask."
    # SFX SUGGESTION: One coach's whistle blast from across the courtyard.
    "Outside, the track team is gathering beyond the fence. A whistle sounds once in warning."
    m forward uniform happ om oe nobl rhip ldown "Go. Before Coach writes me up as an accomplice."
    mc "Have a good Saturday, Ms. President."
    m forward uniform curi om oe nobl rdown ldown "You too. And [player]?"
    mc "Yeah?"
    m forward uniform happ cm oe nobl rdown ldown "You are allowed to enjoy the plan before it happens."
    "The line catches the answer I had prepared and leaves it behind."
    mc "I'll keep that under advisement."
    m forward uniform neut cm oe nobl rdown ldown "Naturally."
    "Her smile stays warm, though it takes a second to arrive."
    m forward uniform happ om oe nobl rdown ldown "See you Monday."
    mc "Monday."
    show monika at thide
    hide monika
    "She heads for the front gate. I cross the courtyard toward the track, carrying the unfinished line with me."
    $ update_character_thought("monika", "Monika took one rescued journal home and reminded me that the traveler still has to decide whether to go inside. She said I am allowed to enjoy a plan before it happens.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The last obligation between school and the station waits in six painted lanes."
    nier "Coach has set out cones, low hurdles, and exactly enough equipment to make the words short practice look dishonest."
    call nier_clear from _call_nier_clear_0531_3
    stop music fadeout 1.0
    pause 2.0
    scene bg track_day
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music daily
    "The track gives back heat through the soles of my shoes."
    "I finish the warmup at the pace Coach ordered, which means three people pass me and none of them receive the duel my pride briefly drafts."
    "He waits beside the first row of hurdles with his clipboard tucked beneath one arm."
    show track_coach neut at t11
    track_coach "Foot?"
    mc "Present. Quiet."
    track_coach "Keep it boring."
    mc "You have a gift for speeches."
    track_coach "And you have eight minutes of drills before I decide whether you get strides. High knees to the cone. Walk back."
    "I start stiff through the hips, loosen up on the second pass, and land a little too far ahead on the third. Coach taps the clipboard with his pen."
    track_coach "Under you. Do not reach for ground that is already coming."
    "I reset at the line."
    "Knee up. Foot under the hip. Shoulder loose. The motion stops arguing with itself."
    "Four strides at controlled speed. I run the first too hard because the word controlled has always sounded negotiable."
    "His whistle cuts me off before the end cone."
    track_coach "What percentage was that?"
    mc "Eighty."
    track_coach "Try an honest number."
    mc "Eighty-seven."
    track_coach "Your face said ninety-five and your shoulders were worse."
    mc "My face isn't calibrated."
    track_coach "Then I will calibrate your afternoon down to zero strides. Again at seventy-five."
    "I walk back. The foot remains quiet, but my pulse is already trying to turn permission into a test."
    "At the line, I look past the far curve instead of at it."
    "Seventy-five feels embarrassingly easy for the first four steps. Then everything lines up. My arms stop crossing, the ground arrives beneath me, and speed becomes something I pass through instead of something I have to drag into existence."
    "He lets me reach the cone."
    track_coach "That."
    mc "That was slower."
    track_coach "That was running. The first one was a hostage situation."
    "He makes a mark on the clipboard."
    track_coach "Three more like it and you leave."
    mc "That's all?"
    track_coach "And there you are."
    mc "What?"
    track_coach "Personally offended that a clean session gets to end clean."
    "I let the next argument die before it becomes extra conditioning."
    mc "Three more."
    track_coach "Seventy-five."
    "I run all three at seventy-five. The last one tempts me, but I cross the cone and ease down when I'm supposed to, letting good remain an adjective instead of turning it into another repetition."
    "He checks my first few walking steps."
    track_coach "Anything?"
    mc "No."
    track_coach "No limp, either."
    mc "You sound disappointed."
    track_coach "I sound unemployed for the next forty-eight hours. Easy mileage tomorrow. Monday we talk entries."
    "The invitational opens in my head again: sixteen, thirty-two, maybe both."
    "The pen levels at me before I can spend the maybe."
    track_coach "Do not race the train to the station."
    mc "I wasn't planning to."
    track_coach "Do not race the stairs."
    mc "Specific."
    track_coach "Do not race whoever invited you to the arcade."
    mc "That one depends on the cabinet."
    "He finally lowers the clipboard."
    track_coach "Go be eighteen somewhere that does not have lanes painted on it."
    "The sentence is almost kind. He notices and repairs the damage."
    track_coach "And hydrate before your bad decisions become somebody else's paperwork."
    mc "There he is."
    show track_coach at thide
    hide track_coach
    "I drink, change shoes, and go home. The extra lap I could have snuck in stays hypothetical. The foot makes no complaint on the stairs, and I don't test whether it has one prepared."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The route to the station takes fourteen minutes at a walk and considerably less if Coach's instructions are treated as a challenge."
    nier "I give it fourteen."
    nier "The used bookstore sits beneath a faded green awning and would be easy to miss if the clearance rack had not spilled onto the sidewalk."
    call nier_clear from _call_nier_clear_0531_4
    stop music fadeout 1.0
    pause 2.0
    scene bg bookstore
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music dailyfantasy
    "Inside, the air smells like paper, floor wax, and the dust a business only accumulates by outliving its own era."
    "Shelves divide the room into thin aisles. Handwritten price cards hang from clips, each marked with a red number that has been crossed out at least once."
    "I find Tsubaki at the old-magazine tables with two paper bags by her feet and a stack balanced against one forearm."
    show tsubaki uniform neut at t21
    "Matsuda is crouched beside a low shelf, reading the back of a mystery serial with the severity of a judge reviewing a confession."
    show matsuda uniform thinking at t22
    ma "The missing violinist was obviously the landlord."
    show tsubaki uniform unamused
    ts "You have read three sentences."
    ma "And he has already mentioned the basement twice. No innocent landlord needs that much basement."
    mc "Maybe he appreciates storage."
    show matsuda happy
    "The book closes around one gloved finger."
    ma "Track has released him!"
    "The volume turns two nearby heads. She sees them and lowers her raised hand before trying the sentence again."
    show matsuda neut
    ma "Hey. You made it."
    mc "The route was free of races and municipal peril."
    show tsubaki uniform worried
    ts "How was practice?"
    mc "Short enough that Coach accused me of being offended. Foot's good."
    show tsubaki uniform happy
    "Tsubaki stops holding her breath. Matsuda stands and inspects my shoes before working up to my face."
    show matsuda unamused
    ma "You walked here?"
    mc "Under strict instruction."
    show matsuda teasing
    ma "Responsible. Disturbing, but responsible."
    "She holds up the mystery serial. Its cover features a mansion, a red window, a thunderhead working overtime, and a detective who appears to have misplaced several vertebrae."
    ma "Seven volumes for the price of two. The prose is terrible, but the mystery looks decent."
    mc "You bought all seven?"
    "She points toward one of the paper bags."
    "The bottom is bowing beneath a rectangular burden."
    show tsubaki uniform unamused
    ts "She bought nine."
    ma "Two are supplemental."
    show tsubaki uniform smug
    ts "One is a car magazine."
    ma "A mystery of engineering."
    "Tsubaki adjusts the stack on her arm. The top three magazines are old school literary journals, their years handwritten on the spines. Beneath them sits a thin home-and-garden issue with pressed flowers on the cover."
    mc "Any inflatable-sword casualties?"
    show tsubaki uniform teasing
    ts "Not yet."
    "The satisfaction in her voice tells me she remembers the promise."
    show tsubaki uniform happy
    ts "I found the spring poetry issues from four different schools. They were practically free."
    mc "You look like you plan to audit regional metaphor use."
    show tsubaki uniform neut
    ts "I just want to see what other clubs print."
    "Her thumb holds her place against the edge of the top issue. A yellow notebook is tucked safely beneath the stack, its elastic band straight across the cover."
    show tsubaki uniform curious
    ts "Some of them put contributor notes in the back."
    mc "Research, then."
    show tsubaki uniform neut
    ts "Maybe."
    "The answer is small, but she does not apologize for it."
    "Matsuda slides the mystery book into her bag and turns toward a rotating rack near the register."
    show matsuda smug
    ma "Behold. A cultural fossil."
    "She plucks out an old children's television magazine. The cover is crowded with bright lettering and a cast of smiling people arranged around a foam creature with visible seams."
    show tsubaki uniform curious
    "Tsubaki leans closer to the cover."
    ts "Wasn't that the show you were on?"
    show matsuda unamused
    "Matsuda's fingers stop at the corner."
    mc "You were on television?"
    ma "The term on is doing heroic work."
    "She flips through the magazine faster than she read the mystery book."
    ma "I appeared in a minor foreign-market production as a minor person standing beside a more marketable child. Three lines, one reaction shot, and a promotional interview nobody watched."
    mc "How old were you?"
    ma "Old enough to remember the craft. Young enough to believe craft services meant woodworking."
    "She finds a page and goes quiet. Tsubaki spots it over her shoulder."
    show tsubaki uniform neut
    ts "There."
    "The photograph is too small to see clearly from where I stand. Matsuda reads the caption once, then again."
    show matsuda sad
    "Her thumb covers the bottom line."
    ma "They spelled my name wrong."
    "No stage voice. No outrage prepared for an audience."
    "She closes the magazine and returns it to the rack with the cover facing forward."
    mc "You don't want it?"
    ma "I own the episode."
    mc "That wasn't the question."
    "Her eyes stay on the rack."
    ma "No."
    show tsubaki uniform sad
    "Tsubaki shifts her magazines against her chest, paper settling against paper."
    ts "Okay."
    "She leaves the answer there."
    show matsuda neut
    "Matsuda hooks two fingers beneath the heavy bag and lifts it. By the time she turns back, some of the brightness has returned, though it stops short of performance volume."
    ma "Besides, this expedition was commissioned for literature and mechanical humiliation. We have secured the first."
    mc "You bought nine mystery books and a car magazine."
    ma "Literature contains multitudes."
    show tsubaki uniform unamused
    ts "You said the car magazine was engineering."
    ma "Do not split the canon in public."
    show tsubaki uniform happy
    "Tsubaki gives up on her expression."
    show tsubaki uniform determined
    "At the register, she pays for her own stack before Matsuda can move either paper bag onto the counter. Matsuda notices and moves hers back without argument."
    "The cashier wraps twine around the magazines. Tsubaki checks the knot once, then thanks him and carries the bundle herself."
    "Outside, the arcade sign flashes blue across the street despite the afternoon sun."
    ma "Phase two?"
    show tsubaki uniform happy
    ts "Phase two."
    "They both look at me."
    mc "I didn't walk fourteen responsible minutes to admire the sign."
    show matsuda happy
    "That is apparently the correct answer."
    ma "Then let the machines prepare their wills."
    show matsuda smug
    "She makes it halfway to the door before doubling back for the bag she nearly left beside the mystery shelf."
    "Tsubaki picks it up first and holds it out."
    show tsubaki uniform smug
    ts "Inventory."
    ma "A temporary clerical fluctuation."
    show matsuda neut
    "She takes the bag with both hands."
    ma "Thanks."
    show tsubaki uniform happy
    "The word is plain. Tsubaki's smile answers it the same way."
    $ update_character_thought("tsubaki", "Tsubaki found four school poetry journals at the clearance table, bought them herself, and carried her own bundle. She did not apologize for wanting to study the contributor notes.")
    $ hide_calendar()
    scene black with wipeleft_scene
    # SFX SUGGESTION: Layered arcade ambience: cabinet music, synthetic engines, light-gun fire, and prize-machine jingles.
    nier "The arcade announces itself before the doors open. Music, synthetic engines, plastic gunfire, and a hundred overlapping invitations to spend one more coin."
    nier "Matsuda steps into the noise and does not have to make the room louder to occupy it."
    call nier_clear from _call_nier_clear_0531_5
    stop music fadeout 1.0
    pause 2.0
    scene bg arcade
    $ show_calendar()
    $ atmos("afternoon")
    with wipeleft_scene
    play music daily
    "Blue and pink light moves across the carpet. Prize machines line one wall, racing cabinets line another, and the rhythm section pulses in the back like a second building trying to escape this one."
    "Tsubaki rents a locker near the entrance and places both sets of books inside. She reads the number twice before the door closes."
    "Matsuda waits for almost eight seconds before her restraint gives out."
    ma "Racing first."
    mc "You sound confident."
    ma "I have studied the machines."
    ts "She watched someone play while I was paying."
    ma "Study takes many forms."
    "She leads us to a pair of molded seats facing screens built to encourage poor judgment. One cabinet has a red car, the other blue."
    ma "Choose."
    mc "Does it matter?"
    ma "Only if you lose and need an excuse."
    "I take blue."
    "My old arcade card has enough credit for one race and a fraction of a second. Matsuda taps her own card against the red cabinet, then waits while I load mine at the kiosk instead of offering to solve it for me."
    "When I return, she is adjusting the seat one notch forward."
    mc "Ready?"
    ma "I was ready when the first wheel offended the first pedestrian."
    ts "Please don't drive outside the game."
    ma "No promises."
    "The countdown fills both screens, and the lights change."
    "Matsuda chooses a rear-wheel-drive car with terrible stability and an acceleration curve that turns every corner into an argument. I choose something sensible because one of us should."
    "She launches early. I expect a penalty. There is none. Her car takes the first corner sideways and exits ahead, missing the barrier by the width of a thought."
    mc "You have played this."
    ma "Not this one."
    mc "That answer is suspicious."
    ma "Eyes forward, sidewalk!"
    "I gain on the straight. She blocks late, laughs when I cut inside, and spends the final lap driving as though brakes are an accusation."
    "We cross less than half a second apart. Red first. Blue second."
    "Both hands leave the wheel."
    ma "A decisive demonstration of natural supremacy!"
    mc "Half a second."
    ma "History rounds upward."
    "The results screen displays the gap to three decimal places."
    ts "History seems very specific."
    ma "History is being rude."
    "I tap the continue prompt. She is half out of the seat and has to sit back down."
    mc "Again."
    "The victory speech drops out of her face before it reaches the next line."
    ma "Yeah?"
    mc "Unless natural supremacy has somewhere to be."
    "Her grin returns without the balcony attached."
    ma "Run it."
    "The second race uses a mountain course. I stop trying to beat her on the straight and wait for her to overcommit."
    "She refuses to overcommit. Every time I set up an inside line, the red car is already making the corner narrower, and every time I fake wide, she gives me exactly enough road to make the lie expensive."
    "I win by using the final guardrail as a suggestion."
    "Blue crosses first. Red arrives one tire-width later."
    mc "History rounds upward."
    ma "You hit the wall."
    mc "The wall participated voluntarily."
    ma "Fraud. Corruption. An asphalt coup."
    "She can't finish saying coup without laughing."
    "Tsubaki has taken one of the molded spectator seats. She keeps our bags between her shoes and lets the replay be as funny as it is."
    ts "One more for the tiebreaker?"
    "Matsuda and I answer at the same time."
    ma "Obviously."
    mc "Yeah."
    "The third course is rain-slicked city streets."
    "We spend two laps changing first place every few corners and the last one forgetting Tsubaki is the only witness who can settle disputed contact."
    "At the final turn, Matsuda brakes early. I read it as weakness, dive inside, and discover she has left me exactly one bad line."
    # SFX SUGGESTION: A sharp digital tire scrape and cabinet collision sound as blue clips the curb.
    "Blue clips the curb. Red passes clean."
    "She wins by 0.214 seconds."
    ma "Strategy."
    mc "Entrapment."
    ma "You lean left before you commit to an inside pass."
    "The answer comes out from under the joke, precise and immediate."
    mc "I don't."
    ts "You do."
    "She avoids my eyes."
    ts "Only a little."
    "Matsuda taps the side of her nose."
    ma "The Azure Eye misses nothing."
    mc "Retire that title before I demand video review."
    "She stands and offers me a hand out of the low seat with exaggerated dignity. I take it because my legs have spent too much of the day folded into required shapes."
    "Her grip is steady and brief."
    ma "Good race."
    mc "Good trap."
    "We move on before either line needs decorating."
    "Tsubaki chooses a cooperative light-gun game next, then apologizes to the plastic weapon when its cable catches her sleeve."
    "Matsuda takes the left side. I take the right. Tsubaki stands between us and quietly rescues every civilian the game places in unreasonable danger."
    "Between us, Matsuda and I supply enthusiasm and very little accuracy. Tsubaki finishes the first stage on top and stares at the result like the machine has exposed her private life."
    ma "Kareda."
    ts "It was mostly timing."
    ma "You have been concealing lethal talent from the party."
    ts "I played this with my cousins last summer."
    mc "Prior training. The court allows it."
    "The gun finds its cradle."
    ts "Can we do the next stage?"
    "She asks first despite nobody having to offer it to her."
    ma "Absolutely."
    "The second stage ends with all three of us shouting at a helicopter that refuses to respect conventional damage."
    "When it finally crashes, Tsubaki laughs loud enough that the game does not swallow it."
    "My phone buzzes during the score tally."
    "Asahina has sent one message to the group."
    python:
        _phone_messages = [
            phone_msg("them", "Asahina: practice over. where are you"),
            phone_msg("me", "Back wall near the light-gun games."),
            phone_msg("them", "Matsuda: Follow the sounds of victory."),
            phone_msg("them", "Tsubaki: Or the blue racing cabinets. Those are easier."),
        ]
    call phone_text_conversation("Saturday", _phone_messages, status="3 participants", append=True) from _call_phone_text_conversation_0531_2
    "Asahina appears three minutes later with her volleyball bag across her chest and the look of someone who has already judged the carpet."
    show asahina disgusted at t33
    show tsubaki uniform happy at t31
    show matsuda uniform teasing at t32
    ah "This place smells like electricity and old socks."
    ma "The perfume of competition."
    show asahina smug
    ah "You must compete in terrible buildings."
    "Matsuda absorbs the insult on the venue's behalf."
    ma "Lady Asahina arrives and immediately wounds the venue."
    show asahina unamused
    ah "Drop the Lady and I might let you recover."
    show matsuda neut
    ma "Asahina. Welcome."
    "The correction is immediate. Asahina notices."
    show asahina neut
    ah "Hey."
    "Tsubaki's hand lifts a few inches."
    show tsubaki uniform curious
    ts "How was volleyball?"
    show asahina teasing
    ah "Coach made us serve until the ball developed a personal grievance. You guys do anything good?"
    mc "Matsuda cheats at racing."
    ma "I observe body language."
    ah "So she cheats legally."
    show tsubaki uniform smug
    ts "I got the high score on the shooting game."
    show asahina shocked
    "Asahina recalibrates."
    ah "You?"
    show tsubaki uniform nervous
    "Tsubaki's fingers move toward the edge of her sleeve."
    "Then she looks back at the score screen. Her name -- three initials Matsuda insisted should be TSK -- remains above both of ours."
    show tsubaki uniform determined
    ts "Yeah. Me."
    show asahina happy
    ah "Okay, sick. Show me."
    "The sleeve stays where it is."
    "We play the first stage again. Asahina is aggressive, inaccurate, and emotionally committed to every civilian she accidentally shoots."
    show asahina frustrated
    ah "Why do they keep running in front of me?!"
    mc "They mistake volume for authority."
    ah "Shut up and cover the stairs!"
    show tsubaki uniform determined
    "Tsubaki covers the stairs. Matsuda covers everything else. I spend the boss fight reviving Asahina while she insists the game is targeting her personally."
    "Tsubaki keeps the high score."
    show asahina determined
    ah "Rematch later. I need a game that respects athletic ability."
    show matsuda determined
    ma "Dance cabinet."
    "The pulsing machines in the back acquire a new admirer."
    show asahina curious
    ah "You play?"
    ma "I possess rhythm."
    show tsubaki uniform unamused
    ts "She knows one song."
    ma "Mastery begins with specialization."
    "They choose the same song."
    "Matsuda attacks the first thirty seconds with a confidence that treats accuracy as optional. Asahina starts more carefully, finds the beat, and then turns ruthless."
    "By the chorus, Matsuda is one missed step behind and pretending the handrail is a stylistic choice."
    "Asahina wins by a margin too large for excuses."
    show asahina smug
    ah "Athletic ability."
    show matsuda frustrated
    ma "The machine showed clear hometown bias."
    show asahina unamused
    ah "We're in the same town."
    ma "Then sibling bias."
    mc "The machine has always favored her. It's why we don't let it settle family arguments."
    "She steps off the platform still running on exertion and victory."
    "Her phone lights in her open bag. Sam's name appears above a short message."
    "She reads it and types back one-handed, reaching for her water with the other."
    show tsubaki uniform worried
    ts "Everything okay?"
    show asahina neut
    ah "Yeah. He just asked if practice ran late."
    "She drinks before the cap finishes clicking against the bottle."
    show asahina happy
    ah "What next?"
    "The question closes the phone without ceremony."
    "We migrate toward the prize machines."
    show tsubaki uniform curious
    "Tsubaki stops in front of a claw cabinet filled with small cloth birds in colors no bird has requested. One pale yellow bird is wedged near the chute with its beak pressed against the glass."
    show matsuda curious
    show tsubaki uniform neut
    "She gives it two seconds, then keeps walking. Matsuda stops with her."
    ma "Kareda."
    show tsubaki uniform unamused
    ts "No."
    ma "I haven't proposed anything."
    show tsubaki uniform smug
    ts "Your hand is on your arcade card."
    "The hand retreats from the card."
    show matsuda teasing
    ma "Circumstantial."
    show tsubaki uniform neut
    ts "I don't need it."
    ma "Need is a dreary standard for a bird with that much facial resolve."
    show tsubaki uniform worried
    ts "It will take too many tries."
    show matsuda determined
    "Matsuda studies the cabinet until she finds the side angle."
    ma "One."
    show tsubaki uniform frustrated
    ts "Matsuda."
    ma "One attempt. If the machine rejects destiny, destiny can sit there and think about what it did."
    show tsubaki uniform sad
    "The yellow bird gets one more second than she meant to give it."
    show tsubaki uniform determined
    ts "One."
    "Matsuda taps her card. She centers the claw, then moves it back by less than a centimeter. The timer counts down."
    mc "No pressure."
    ma "Pressure is merely attention with a deadline."
    # SFX SUGGESTION: Claw-machine motor whir, metal clack, then the plush landing with a soft cabinet thump.
    show tsubaki uniform shocked
    "The claw drops, catches the bird around the middle, and carries it almost to the chute before one metal prong slips. The bird bounces once and lands farther from the opening than it began."
    show matsuda uniform pose_facepalm
    "For a second, nobody speaks. Matsuda stares at the machine."
    ma "I have been betrayed by geometry."
    show matsuda uniform unamused
    show tsubaki uniform happy
    "Tsubaki laughs first, and only remembers to cover it after Matsuda leans close to the glass and tells the bird to remember who tried."
    "Matsuda straightens. Her card is still in her hand."
    "Then she puts it away."
    show tsubaki uniform sad
    "Tsubaki touches two fingers to the glass near the bird's flattened beak."
    ts "Maybe next time."
    "After another round of racing, one air-hockey dispute, and a photo booth Matsuda enters before discovering nobody else followed, the overhead lights dim by a shade as evening reaches the windows."
    "Our arcade cards are lighter. My legs are tired in a way that belongs to the whole day instead of one injury."
    show tsubaki uniform neut
    "Matsuda retrieves the bookstore bags. Tsubaki checks the locker twice, then closes it with nothing left inside."
    show matsuda happy
    ma "Food. The final phase."
    ah "Burgers."
    show tsubaki uniform happy
    ts "The cafe across from the station has sandwiches too."
    mc "And chairs that don't vibrate."
    ma "The committee achieves consensus at last."
    $ update_character_thought("matsuda", "Matsuda beat me two races to one by noticing I lean before an inside pass. She respected Tsubaki's one-try limit at the claw machine, even after the yellow bird got farther away.")
    $ update_character_thought("asahina", "Asahina joined us after volleyball, beat Matsuda badly at the dance cabinet, and immediately asked Tsubaki to show her the shooting game high score.")
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "We leave the arcade carrying books, track gear, volleyball gear, and exactly zero cloth birds."
    nier "The station district has changed shifts while we were inside. Storefront lights have taken over from the sun, and the windows hold four overlapping reflections whenever we pass."
    call nier_clear from _call_nier_clear_0531_6
    stop music fadeout 1.0
    pause 2.0
    scene bg cafe
    $ show_calendar()
    $ atmos("evening")
    with wipeleft_scene
    play music dailyleisure
    "The cafe gives us a table near the front window and a basket beneath it for bags."
    "Tsubaki lowers the bookstore bundle into the basket with both hands. Matsuda's nine-volume mystery purchase lands beside it, and the tableware notices."
    "We order within the limits of four different definitions of dinner."
    "Asahina gets a grilled chicken sandwich and steals fries from my plate before hers arrives. Tsubaki orders soup and toast. Matsuda asks whether the largest burger has historical significance, then orders the normal one when the server cannot confirm it."
    show tsubaki uniform neut at t31
    show matsuda uniform unamused at t32
    show asahina shocked at t33
    ah "You were on TV?"
    "Matsuda puts the question to Tsubaki without saying it."
    show tsubaki uniform embarrassed
    ts "It came up naturally."
    ma "The bookstore unearthed archival propaganda."
    ah "What show?"
    ma "A short-lived educational adventure program produced in North America, where adults in color-coded uniforms taught children practical lessons by defeating poorly ventilated monsters."
    show asahina happy
    ah "That sounds amazing."
    ma "It was funded for thirteen episodes."
    ah "Still amazing. Who were you?"
    "Matsuda unfolds her napkin and aligns one corner with the table edge."
    ma "A student in episode seven. I alerted the heroes to a malfunctioning weather device and displayed age-appropriate concern."
    show tsubaki uniform teasing
    ts "You also screamed."
    ma "Four essential vocal contributions."
    "The table gains a very interested party."
    show asahina curious
    ah "Is it online?"
    show matsuda neut
    ma "No."
    "The answer is so fast that Asahina leans back."
    "The napkin reclaims her."
    ma "Probably. But no."
    ah "Okay, but you were, like, famous famous. For a second."
    show matsuda unamused
    ma "For roughly the length of one commercial break."
    ma "Which was still enough for everyone at that school to have a full opinion about me by lunch. You know how that goes."
    ah "Wait. That school?"
    ma "Different school. Different continent."
    "She turns the napkin ninety degrees and lines the new corner up with the table edge."
    ma "Then the show ended, and we moved, and I started here in April, and by then everybody had been friends with everybody for two years already."
    ma "Which is just what April is. Anyway."
    show asahina unamused
    ah "That was a lot of information in one breath."
    ma "I have excellent lung capacity."
    show tsubaki uniform nervous
    "Tsubaki wraps both hands around her water glass."
    show tsubaki uniform determined
    ts "They spelled her name wrong in the magazine."
    show asahina annoyed
    ah "Seriously?"
    ma "A minor clerical sin committed against a minor celebrity. History is full of them."
    "She makes the joke, but keeps smoothing the same fold in the napkin."
    mc "Their loss. The weather device never recovered."
    "That reaches her."
    show matsuda neut
    "For a moment, all she does is breathe out through her nose."
    ma "It didn't."
    "The food comes out and gives the table something else to hold."
    "For a while, we eat without talking. Plates move, ice settles, and trains arrive beyond the window with their windows lit."
    "Asahina finishes half her sandwich quickly, then slows. She moves the remaining fries into a line along the plate without eating them."
    "Tsubaki notices the arrangement and nudges the shared pickle dish toward the center without comment. Asahina takes one."
    show matsuda thinking
    show tsubaki uniform thinking
    "Matsuda tells us the mystery serial's landlord is guilty based on basement frequency. Tsubaki counters that the violinist may have staged her disappearance."
    "By the time my plate is empty, we have accused every person on the back cover."
    show asahina thinking
    ah "What if the violinist just left?"
    ma "Without explaining herself?"
    ah "People do that."
    show tsubaki uniform unamused
    ts "The title is {i}The Violinist Who Never Left{/i}."
    show asahina smug
    ah "Marketing lies."
    mc "Strong defense."
    show matsuda teasing
    "Matsuda extends a fry in her direction, ceremonially."
    ma "I respect the skepticism. You may join the inquiry."
    ah "Do I have to read nine books?"
    ma "Ideally."
    show asahina unamused
    ah "Then I resign."
    "Matsuda eats the fry and accepts the loss."
    show tsubaki uniform neut
    "When the plates are mostly clear, Tsubaki checks the train schedule."
    ts "I should leave in twenty minutes."
    ma "Your curfew?"
    show tsubaki uniform embarrassed
    ts "Yeah. The 7:18 gets me home with enough time."
    ma "Then the 7:18."
    "Tsubaki locks her phone and returns it to her bag."
    show asahina neut
    ah "Mom wants us to text when we leave."
    mc "Food happened, so we owe Mom an update."
    python:
        _phone_messages = [
            phone_msg("me", "Food happened. Cafe by the station. We're leaving in about twenty minutes."),
            phone_msg("them", "Thank you. Home by eight-thirty."),
            phone_msg("them", "And bring your sister with you."),
            phone_msg("me", "I was planning to."),
            phone_msg("them", "I enjoy written confirmation."),
        ]
    call phone_text_conversation("Mom", _phone_messages, append=True) from _call_phone_text_conversation_0531_3
    show asahina teasing
    ah "She thinks you're going to trade me for arcade credit."
    mc "The exchange rate is terrible."
    show asahina smug
    ah "You couldn't afford me."
    ma "I could arrange the exchange."
    mc "Don't encourage her."
    show tsubaki uniform embarrassed
    "Tsubaki takes a sudden interest in the ceiling."
    "The server leaves the check. Four hands move at once."
    "We split it without drama, though Matsuda attempts to classify the fries she stole from my plate as a cultural exchange."
    "Asahina goes to the counter for change. Tsubaki follows to buy a wrapped cookie for the train."
    show matsuda neut
    "For the first time since the bookstore, Matsuda and I are the only two at the table."
    "She stacks the empty sugar packets into a small square."
    ma "Can I ask a normal question?"
    mc "You can attempt one."
    show matsuda nervous
    "Her eyes remain on the sugar packets."
    ma "Was today okay?"
    "The question is quieter than the cafe requires."
    mc "Yeah."
    ma "Okay as in tolerable, or okay as in you would voluntarily repeat parts of it?"
    mc "That's already a second question."
    "Matsuda presses the packets flat with one finger."
    ma "Right. Sorry."
    "She starts to pull her hand away."
    mc "It's the second one."
    "Her hand stops beside the little square."
    ma "...Noted."
    "The espresso machine hisses behind the counter. She waits for it to stop and does not fill the space it leaves."
    "I look past her at the trains moving beyond the window."
    # The invitation itself is fixed -- it is the capstone proof that MC can
    # start something instead of waiting to be started. Only HOW he says it is
    # the player's.
    menu:
        "(Say it plainly.)":
            $ s1_pick("arcade_offer", "plain")
            mc "I want to do this again."
            "Matsuda's thumb goes still on the sugar packet."
            mc "There's another arcade across town with the full version of that racing game. Four cabinets, different courses."
            ma "I've heard of it."
            mc "Of course you have."
        "(Hide it behind the racing game.)":
            $ s1_pick("arcade_offer", "excuse")
            mc "There's another arcade across town with the full version of that racing game."
            "Matsuda's thumb goes still on the sugar packet."
            mc "Four cabinets. Different courses. Purely a research matter."
            ma "Purely."
            mc "Obviously."
        "(Almost don't.)":
            $ s1_pick("arcade_offer", "almost")
            mc "..."
            "The sentence gets as far as my teeth and stops there, the way most of them do."
            "Matsuda waits. She doesn't fill it, which is new."
            mc "...There's another arcade across town. Full version of that racing game."
            "Matsuda's thumb goes still on the sugar packet."
            ma "I've heard of it."
    show matsuda smug
    "The smile she is trying not to show reaches one corner first."
    mc "We could go sometime."
    show matsuda curious
    ma "We?"
    mc "You, me, whoever wants to lose at the helicopter again."
    "She looks toward the counter. Tsubaki is counting change into her palm. Asahina is trying to convince the cashier that two small coins stuck together should not count as one."
    show matsuda thinking
    ma "Sometime is flexible."
    mc "That's usually what the word means."
    ma "Next weekend?"
    ma "Or later. Whenever. You've got track and all that."
    mc "I've got the invitational in two weeks. Next Saturday might be messy."
    ma "Then not next Saturday."
    mc "Maybe after school one day. We can figure it out."
    show matsuda neut
    "Matsuda nods. No decoration on it."
    ma "We can figure it out."
    "She leaves the sugar packets in their square."
    ma "Thanks for coming today."
    mc "Thanks for the entrapment."
    ma "Any time."
    show tsubaki uniform neut
    "Asahina and Tsubaki return."
    show matsuda smug
    ah "Why do you both look like you just signed something?"
    mc "Sugar business."
    ma "Need-to-know."
    show tsubaki uniform curious
    ts "Does it affect the train?"
    ma "The 7:18 is untouched."
    show tsubaki uniform happy
    ts "Good."
    "We collect the bags and leave the table near the window empty again."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Tsubaki's train arrives first. She boards after one reminder about the cookie."
    nier "Matsuda waits with us until the doors close, then heads for the opposite platform with the heavy bag against one leg."
    call nier_clear from _call_nier_clear_0531_7
    stop music fadeout 1.0
    pause 2.0
    scene bg city_evening
    $ show_calendar()
    $ atmos("evening")
    with wipeleft_scene
    play music fantasyserenity
    "Asahina and I walk home beneath storefront lights and the last blue left in the sky."
    "Her volleyball bag has migrated to my shoulder. She surrendered it after insisting twice that it was not heavy."
    show asahina curious at t11
    ah "So."
    mc "Dangerous opening."
    ah "Matsuda."
    mc "Still a person."
    show asahina unamused
    ah "I know. I met her. Very difficult to miss."
    "She steps around a crack in the pavement and nudges a bottle cap into the gutter with the side of her shoe."
    show asahina neut
    ah "She's fun."
    mc "You sound surprised."
    show asahina teasing
    ah "You made her sound like a weather event."
    mc "Weather can be fun from inside a structurally sound building."
    show asahina smug
    ah "You raced her three times."
    mc "The third was necessary."
    ah "Then you talked about a different arcade for like ten minutes while we were getting change."
    mc "You were listening?"
    ah "You were visible through glass, genius."
    show asahina neut
    "She walks another few steps."
    ah "She listened when people said no."
    "The line loses the teasing around it."
    mc "Yeah."
    ah "Tsubaki said one try, so it was one try."
    mc "She is trying."
    ah "I know."
    show asahina embarrassed
    "She catches the swinging strap of my track bag before it bumps a railing."
    ah "Just saying. She could be worse."
    mc "A moving endorsement."
    show asahina annoyed
    ah "Don't make me retract it."
    "At the next light, her phone buzzes."
    "She reads the message and types while we wait."
    mc "Sam?"
    show asahina neut
    ah "Mom. She wants to know if we're at the crossing."
    "She sends a picture of the signal instead of an answer."
    show asahina smug
    ah "There. Discovery satisfied."
    "The light changes."
    "We cross at a walk."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "Home is lit when we reach it. The front window throws a warm rectangle across the path, and Mom already has the door open."
    nier "Asahina calls this surveillance. Mom says we were arguing loudly enough to save her the walk."
    call nier_clear from _call_nier_clear_0531_8
    stop music fadeout 1.0
    pause 2.0
    scene bg living_room_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music dailyleisure
    "The Copper Crown box is waiting on the coffee table for tomorrow. Beside it sits Mom's closed laptop and one legal pad with three lines crossed out."
    "Mom takes Asahina's bag from my shoulder and sets it near the stairs."
    show mom unamused at t22
    show asahina smug at t21
    mom "Eight twenty-three."
    ah "Seven minutes early."
    show mom teasing
    mom "I'm deciding how responsibly to spend them."
    mc "Bank them for our next offense."
    show mom smug
    mom "That's not how credit works in this house."
    show mom thinking
    "Her gaze drops to my feet."
    mom "How is it?"
    mc "Still quiet. Practice was clean."
    mom "And you walked?"
    show asahina teasing
    ah "He walked so slowly I almost filed a missing-person report."
    mc "You gave me your bag."
    show asahina unamused
    ah "Unrelated."
    "Mom reads one of us, then the other, and decides that will do."
    show mom neut
    mom "Did you eat?"
    show asahina neut
    ah "Yes."
    mc "Cafe by the station."
    mom "And?"
    mc "And what?"
    show mom curious
    mom "Was it fun?"
    "The question should be easy. It still waits in the room with more patience than most easy questions get."
    show asahina happy
    "Asahina drops onto the couch and pulls one leg beneath her."
    ah "I destroyed Matsuda at the dance game."
    show mom teasing
    mom "Then I assume yes."
    "She waits for my answer."
    "The arcade returns in pieces: red and blue cabinets, Tsubaki laughing at the helicopter, a yellow bird falling the wrong way, Matsuda asking whether okay meant repeatable."
    mc "Yeah. It was fun."
    "For once, I don't tack a qualification onto it."
    show mom happy
    mom "Good."
    "She picks up her mug from the table. It is empty."
    show asahina smug
    ah "He and Matsuda are planning another arcade trip."
    mc "We mentioned one."
    ah "He proposed it."
    "Mom lets one eyebrow do the work."
    mc "I didn't propose anything. I told her another arcade exists."
    ah "Then said we could go."
    show mom smug
    mom "A dangerous sequence of admissions."
    mc "I want a lawyer."
    show mom unamused
    mom "She's off duty."
    "She carries the mug toward the kitchen."
    show mom neut
    mom "Her unofficial opinion is that you're allowed to make friends without filing paperwork first."
    "The sentence follows her through the doorway."
    "Asahina delivers her verdict from the couch."
    show asahina teasing
    ah "Wow. Precedent established."
    mc "Go shower."
    ah "Already did at school."
    mc "Then go be smug upstairs."
    ah "I can multitask."
    show asahina happy
    "She stands anyway, volleyball bag in hand, and pauses near the stairs."
    ah "Wake me before Copper Crown tomorrow."
    show mom determined
    mom "Biology first."
    ah "I wasn't talking to you."
    show mom smug
    mom "I can still hear you."
    "Asahina concedes the kitchen and heads upstairs."
    show asahina at thide
    hide asahina
    "Mom returns with water in the mug and sits in the chair beside the closed laptop."
    show mom curious at t11
    mom "You proposed it?"
    mc "There really is another arcade."
    show mom thinking
    mom "I believed that part."
    "She waits for me to give her the rest."
    mc "Today was good."
    show mom teasing
    mom "That's usually when people make another plan."
    mc "So I've been told."
    show mom neut
    "Her pen rests across the top of the legal pad instead of in her hand."
    mom "You can like spending time with someone before you know exactly what to call it."
    mc "Is that lawyer advice?"
    show mom smug
    mom "No. Legal advice is billed in six-minute increments."
    mc "Then I can't afford the follow-up."
    show mom happy
    "Her mouth curves over the rim of the mug."
    mom "Go rest. Your face is starting to negotiate with gravity."
    mc "It's been a long day."
    mom "A good one, apparently."
    mc "Apparently."
    show mom neut
    "Mom opens the laptop only after I stand. The legal pad remains untouched."
    mom "Goodnight, [player]."
    mc "Night, Mom."
    $ hide_calendar()
    scene black with wipeleft_scene
    nier "The house winds down around ordinary plans. Forty-five minutes of biology. A board-game rematch. Easy mileage. Six algebra problems. One unfinished line for Monday."
    nier "Nothing about the list looks like a threshold. Most thresholds do not advertise."
    call nier_clear from _call_nier_clear_0531_9
    stop music fadeout 1.0
    pause 2.0
    scene bg bedroom_night
    $ show_calendar()
    $ atmos("home_night")
    with wipeleft_scene
    play music fantasypassion
    "My room looks exactly as I left it, except the day no longer fits inside the places I prepared for it."
    "The arcade card returns to the desk with less credit. The portable charger returns half empty. My track shoes stay by the door until I decide they can be tomorrow's problem."
    "I sit and pull the club draft from my bag."
    "The train still runs past the final station. The conductor still faces the window. Blue lights still turn red, and the staircase still waits without footprints."
    "At the bottom of the page, the last two lines remain where I left them:"
    "{i}listen for a television in the next room{/i}"
    "{i}and someone putting away dishes.{/i}"
    "Monika's question rests beneath them in green ink."
    "{i}Does the traveler go inside?{/i}"
    "My phone buzzes before I answer."
    python:
        _phone_messages = [
            phone_msg("them", "Matsuda: Final accounting: two racing victories, one tactical loss, one helicopter destroyed, zero birds liberated."),
            phone_msg("them", "Tsubaki: You lost air hockey too."),
            phone_msg("them", "Matsuda: The table was uneven."),
            phone_msg("them", "Asahina: and the dance game"),
            phone_msg("them", "Matsuda: This chat has become hostile to accurate history."),
            phone_msg("me", "Good day, then."),
            phone_msg("them", "Tsubaki: Good day."),
            phone_msg("them", "Asahina: yeah"),
            phone_msg("them", "Matsuda: Yeah."),
        ]
    call phone_text_conversation("Saturday", _phone_messages, status="3 participants", append=True) from _call_phone_text_conversation_0531_4
    "The conversation goes quiet."
    "A private message comes in a minute later."
    python:
        _phone_messages = [
            phone_msg("them", "Thanks again for coming."),
            phone_msg("me", "Thanks again for only winning two races."),
            phone_msg("them", "A mercy I will not repeat."),
            phone_msg("me", "We'll see about that."),
            phone_msg("them", "We will."),
            phone_msg("them", "Goodnight, " + player + "."),
            phone_msg("me", "Night, Matsuda."),
        ]
    call phone_text_conversation("Matsuda Akai", _phone_messages, append=True) from _call_phone_text_conversation_0531_5
    "I set the phone beside the draft."
    "Sixteen days ago, a name on a plastic card was enough to begin the story of my school year. Since then, May has collected a movie ticket, a bad foot, three exam days, one open seat beside a cafe window, and more people than my calendar knew what to do with."
    "Tomorrow changes the month. Monday returns the grades. The invitational is two weeks away. The rest has no date attached yet."
    "I pick up my pen."
    "A few pages back, the bus-seat draft is still sitting there with the line Monika made me add: [s1_poem_echo]."
    "She was right about that one. It does the work and never argues for itself."
    "The traveler at the top of the stairs has waited long enough for an answer."
    "I add one line beneath the dishes."
    "{i}The door is already open.{/i}"
    "It does not answer whether the traveler goes inside."
    "I leave it anyway."
    $ update_character_thought("matsuda", "Matsuda was on North American television for about one commercial break, moved here in April, and mentioned both of those the way you mention weather. She has not been at this school long enough to have anyone the way everyone else does. I was the one who suggested the next arcade trip.")
    $ hide_calendar()
    $ atmos_clear()
    scene black with wipeleft_scene
    nier "May ends with tomorrow arranged in small, ordinary pieces."
    nier "For the first time in a while, I don't need the pieces to explain what they are becoming."
    nier "The door can remain open until morning."
    call nier_clear from _call_nier_clear_0531_10
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0531_1
    call nier_enter from _call_nier_enter_0531_1
    call nier_section("AND THUS, THE CURTAIN CLOSES...") from _call_nier_section_0531_1
    call nier_section("...FOR NOW.") from _call_nier_section_0531_2
    call nier_exit from _call_nier_exit_0531_1
    pause 2.0
    call enter_m_prologue_trailer from _call_enter_m_prologue_trailer_0531_1
    # End-of-Chapter-0.5 archive opening. Curated on purpose: an explicit list,
    # not a loop over the catalog, so a story added later does not arrive
    # pre-unlocked, and so Purgatorium opens HERE and not before the main story
    # has had its slow read of Sam.
    #
    # ONLY THE MUSIC ROOM IS A SECTION UNLOCK NOW. The other five Archive panels
    # ship open and fill in as they are earned -- roster slots as people are met,
    # CGs as they are shown, tracks as they are heard (see the flag block in
    # game/archive.rpy). The Music Room is the exception because it is the reward
    # for finishing the campaign, and Chapter 0.5 is where the campaign currently
    # ends. WHEN SEASON 1 PROPER SHIPS, this line moves to its ending.
    python:
        persistent.archive_unlocked_music = True
        # This stays here even when the Music Room gate eventually moves: it is
        # the permanent signal for finishing the currently playable Chapter 0.5.
        persistent.chapter05_completed = True
        for _key in (
            "cs_matsuda_01_unlocked",
            "cs_matsuda_02_unlocked",
            "cs_tsubaki_01_unlocked",
            "cs_tsubaki_02_unlocked",
            "cs_asahina_01_unlocked",
            "cs_sam_01_unlocked",
            "cs_kotonoha_01_unlocked",
            "cs_kotonoha_02_unlocked",
        ):
            setattr(persistent, _key, True)
        # Exact event hook for Curtain Call (For Now). The achievement also has
        # a derived chapter05_completed fallback for old saves and reconciliation.
        ach_grant("music_on")
        renpy.save_persistent()
    nier "The Music Room is open."
    nier "Character stories unlocked:"
    nier "Matsuda — {i}Dead Fantasy{/i}, {i}Ontological Seer{/i}"
    nier "Tsubaki — {i}Heads{/i}, {i}Tails{/i}"
    nier "Asahina — {i}Hina's World{/i}"
    nier "Sam — {i}Purgatorium{/i}"
    nier "Kotonoha — {i}The Girl with Every Face{/i}, {i}The Void Hunter{/i}"
    return
