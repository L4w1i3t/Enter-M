# scene after MC and asahina get home from the second day of the culture fest and also hanging out with friends. by the time they get home, it's late at night (around 9PM)
# they find mom completely hammered at the dinner table (like, five drinks too many kind of drunk)
# mom's always been modest, so this is a rarity for the siblings to see
# after MC agrees to Asa that he can get mom into bed with some water, his peripheral vision sees a medical pamphlet on the floor and somewhat tattered, like it was chucked against the wall very forcefully.
#
# CONTINUITY LOCKS
#   * The festival is Sat/Sun Oct 25-26. This is the back half of day two plus the
#     thing with friends afterward, so it is late and everyone is spent.
#   * THE PAMPHLET IS THE ONLY SEED AND IT IS NEVER READ. Seen sideways while Mom
#     has an arm across his shoulders, so he physically cannot go to it; picked up
#     at the end, smoothed flat, left square on the counter, unopened. No sting, no
#     score, no line about what it might be. ooc_1030 picks this up with the word
#     "scan" four days from now -- the reader is meant to feel it there, not here.
#   * Mom threw it. Modest, careful, squares-up-the-glasses Mom threw something at
#     a wall tonight, and the only evidence is a bent corner. Nobody mentions it.
#   * Asahina is still hiding Sam. Drunk Mom goes one step past where sober Mom
#     stops, asks the exact right question, then supplies her own wrong answer, and
#     Asahina lets her have it. Unremarked. It lands on 10/30.
#   * "I only had the one." There are three glasses. Nobody corrects her.
#   * MC asks once and lets it go. The narration never notes that he let it go.
#
# SHAPE
#   Play it FUNNY. Mom is loud, exclamatory, delighted, and completely gone, and
#   the first two thirds are a comedy about two exhausted kids and their wrecked
#   mother. The pamphlet is the rug pull, and it only works in proportion to how
#   much the room was laughing a minute earlier -- so nothing before it is allowed
#   to telegraph, and nothing after it is allowed to explain.
#
# AUDIO
#   smoothsailing runs UNDER THE WHOLE COMEDY at full strength and is killed on the
#   line where he sees the pamphlet -- mid-joke, while Mom is still talking about
#   the boat. That cut IS the rug pull; do not fade it earlier to "prepare" the
#   turn. No sad cue replaces it, per the 12/24 rule about scoring a bad moment.
#   The wall clock takes over on sfxtrack2 (the PROP channel) and runs to the end.

label ooc_1026_passed_out:

    scene black
    stop music
    pause 2.0
    play sound moddooropen
    scene bg home_entry_night
    $ atmos("home_night")
    with dissolve_scene_full
    play sound moddoorclose
    play music smoothsailing
    $ show_calendar()
    mc "Damn, I feel like I've been carrying a sack of rocks around all day..."
    mc "Cannot wait for this shower and date with my bed..."
    "My head slightly throbs, half from dehydration and half from the sheer amount of social convention."
    show asahina frustrated at t11
    # SETTING RULE: "takoyaki" was a loanword; swapped for the plain-English version
    # per the arbitrary-setting sweep. Same joke, same triple.
    ah "Remind me to never, EVER, take over someone else's shift at a fry stand. Or vote to run a fry stand. Or anything involving a fryer."
    mc "You volunteered."
    show asahina unamused
    ah "I volunteered {i}you{/i}. There's a difference."
    "She toes her shoes off without untying them, which Mom has asked her not to do roughly nine hundred times."
    ah "Two days. Two days of standing in front of hot oil saying the same four words."
    mc "Which four?"
    ah "\"Careful, it's still hot.\""
    mc "That's five if you split the contraction."
    ah "...Two days of that. And now this."
    "She yawns so hard she has to put a hand on the wall."
    "Every light downstairs is on."
    mc "Mom? We're back--"
    "The house answers before she does. Something small and glass, set down a little too hard on wood."
    pause 2.0
    scene bg living_room_night
    $ atmos("home_night")
    with dissolve_scene_full
    "She's at the dinner table with her back to us, still in the cardigan she wears for grocery runs."
    "Three glasses. One upright, one on its side, one out near the middle of the table like it got put down on the way to somewhere else."
    show mom wasted at t22
    show asahina shocked at t21
    mom "Oh! Is that the door?!"
    "She asks the kitchen."
    mc "...Yeah. Hi."
    mom "THERE they are!"
    "She gets around about a second and a half after that, and lights up like we've come back from a war."
    mom "My children! Both of them! At the same time!"
    ah "...Uh."
    mom "Come in, come in, sit down, don't just stand there in the--in the--the doorway part thingy."
    mc "The doorway."
    mom "Thank you!"
    ah "Mom, what is happening right now?"
    mom "I'm having a Sunday, mah dude!"
    "She lifts the upright glass to about eye level, toasts nothing in particular, and puts it back down without drinking any of it."
    mom "I only had the one."
    show asahina unamused
    ah "There are three."
    mom "There are three GLASSES. I only had the one."
    mc "...Yeah, no, that tracks...I think."
    show asahina curious
    ah "How long have you been down here?"
    mom "Since the thing finished! On the television! With the man!"
    mc "The man?"
    mom "He had a little boat!"
    ah "...I genuinely don't know what to do with that."
    mom "It was a LOVELY little boat, Asahina."
    ah "Okay!"
    mom "Don't 'okay' me. You weren't there. You didn't {i}see{/i} the boat."
    show asahina nervous
    "My sister turns and looks at me with an expression I have never seen on her before, somewhere between delight and calling for help."
    ah "...I'm getting my phone."
    mom "Get your phone!"
    show asahina smug
    ah "I'm so going to record this."
    mom "{i}Record{/i} it! See the man with the boat!"
    mc "You'd ruin her image, Asa?"
    show asahina happy
    ah "Dude, does it look like I care? This is comedy gold!"
    mom "I want it on the record that I said record it!"
    "She has, at some point in the last ten seconds, adopted an entirely different voice for this."
    mom "Are you hungry? Are you two hungry? I could do something!"
    mc "It's nine at night."
    mom "I could do the rice!"
    mc "Mom."
    mom "The rice, and the little peppers, and there's that fish in the--"
    show asahina unamused
    ah "There's no fish."
    mom "There is ALWAYS fish, my dear."
    "She stands up to prove it."
    "...Then she gets about two thirds of the way, discovers the table with both hands, and lowers herself back down without ever once admitting she was going anywhere."
    mom "...In a minute."
    mc "Sure."
    mom "I'm doing the fish in a minute."
    show asahina frustrated
    ah "There's no fish!!!"
    mom "In...a MINUTE."
    "My sister pulls out the chair across from her and sits, which is the first sign all night that she isn't going straight up."
    show asahina neut
    ah "We ate already with Matsuda and everyone. We're fine."
    mom "FRIENDSHIP!"
    mc "????????????"
    ah "It was a long day."
    mom "That's my girl. That's my--that's my girl."
    "She loses the middle of that one and just uses both ends."
    mom "[player]."
    mc "Yeah?"
    mom "You have a very good face."
    mc "...Thank you???"
    mom "I made that face."
    show asahina embarrassed
    ah "Oh my {i}God{/i}, Mom."
    mom "I MADE it."
    mc "Okay..."
    mom "With my {i}body{/i}!"
    show asahina happy
    ah "OKAY!"
    "She is laughing so hard she has to put a hand over her eyes."
    mom "Was everybody there? Today?"
    ah "Yeah, basically the whole class came through by four, so we sold out, so everyone kind of stayed after--"
    mom "Is he nice?"
    show asahina empty
    "My sister stops laughing all in one piece, like something got unplugged."
    "Her hands go flat on the table on either side of her phone, and her phone is face down, and I don't remember her putting it there."
    ah "...What?"
    "Mom's eyes are pointed at her without being aimed at her."
    mom "The one with the bicycle!"
    "I have never in my life heard about a boy with a bicycle."
    mom "You said! About the bicycle."
    show asahina neut
    ah "...Oh. {i}Him{/i}. Yeah, he's--he's fine."
    ah "Little twelve-year-old weirdo though."
    mom "GOOD."
    "And she's off it. Whatever that was, it doesn't come back."
    "Something goes out of my sister's shoulders."
    mom "Daaaaamn, you two got so TALL."
    show asahina teasing
    ah "That's what happens."
    mom "I know what happens!"
    "Her chin ends up in her hand. She isn't holding it up so much as parking it there."
    mom "I know exactly what happens."
    mom "Just think, though, how tall you'll be by the time you're my age! You'll be giants!"
    "She pushes at the glass on its side to line it up with the other two. She overshoots, and pushes it back, and overshoots that, and leaves it."
    mom "...I only had the one."
    "Nobody corrects her."
    "Asahina catches my eye across the table and tips her head at the stairs, and for once neither of us has to say it out loud."
    show asahina determined
    ah "...Standard procedure?"
    menu:
        "\"I've got her. Go up.\"":
            $ s1_pick("ooc1026_mom_table", "steady")
            mc "I've got her. Go up."
            show asahina curious
            ah "You sure?"
            mc "She'll be less embarrassed with one of us. Go on."
        "\"...Is she okay?\"":
            $ s1_pick("ooc1026_mom_table", "ask")
            mc "...Is she okay?"
            "Asahina receives the question like I have asked her to do long division."
            show asahina unamused
            ah "She's wiggedy {i}wasted{/i}."
            mc "Right. Yeah."
            ah "...Water and bed."
        "\"Water, stairs, and tomorrow this never happened.\"":
            $ s1_pick("ooc1026_mom_table", "joke")
            mc "Water, stairs, and tomorrow this never happened."
            show asahina smug
            ah "Deal. I'm taking it to my grave."
            ah "My grave and also every family thing for the rest of our lives."
    "I take a clean glass down, fill it at the sink, and put it in her hand. She holds it like I've given her something to look after."
    mc "Alright. Up we go."
    mom "Woooooo, UP we go!"
    "She puts the glass straight back down on the table to stand up, so I end up carrying it."
    "She gets an arm across my shoulders and most of her weight through it, and starts telling me about the man with the little boat."
    mom "You'd have liked him. He had a whole system going."
    mc "For...the boat?"
    mom "For the {i}boat{/i}, yes! Adapt or be left behind, I say!"
    "{i}Where have I heard that before?{/i}"
    "That's when I see it. Off to the side and low down, how you pick up on anything you aren't looking for."
    stop music fadeout 3.0
    play sfxtrack2 tick loop
    "A pamphlet, against the baseboard by the wall. Glossy. Somebody smiling on the front of it, and a phone number, and a crease across the middle that isn't a crease so much as a corner bent right back on itself."
    "It didn't fall there."
    "It's four steps away. Mom has both hands on my shoulder now, and she's still on the boat."
    $ hide_calendar()
    scene black with dissolve_scene_full
    nier "Getting her into her room takes about four minutes. Getting her to stop apologizing for it takes six."
    call nier_clear from _call_nier_clear_1026_1
    pause 2.0
    scene bg living_room_night
    $ atmos("home_night")
    $ show_calendar()
    with dissolve_scene_full
    show asahina worried at t11
    "Asahina is exactly where I left her, still in her jacket, elbows on the table."
    ah "Is she out?"
    mc "Like a light."
    ah "...That was weird, right? Like, that was actually weird."
    ah "As if things just took a really weird route right about now."
    mc "..."
    mc "You come up with that one yourself?"
    mc "But yeah, it was...something."
    show asahina frustrated
    ah "She was being so {i}nice{/i}."
    "She says it like an accusation, which is the most sixteen-year-old thing that has happened all day."
    mc "So how's the video?"
    show asahina neut
    ah "...I didn't record it."
    mc "You said about nine times that you were--"
    show asahina annoyed
    ah "I know what I said."
    mc "{i}*sigh*{/i} Go to bed."
    show asahina teasing
    ah "{i}You{/i} go to bed."
    mc "I'm GOING to bed!"
    ah "Then go to bed!!"
    "She goes first. She takes the stairs two at a time even now, and her door does the thing her door does."
    show asahina at thide
    hide asahina
    "And then it's me and the table."
    "I take the glasses to the sink. Two, and then the third."
    "The third one came out of the cabinet over the fridge. The one we keep the vases in."
    "I wash it and dry it and put it back, and I don't know which end of the shelf it lives on, so I pick one."
    "Then I go and crouch down by the wall."
    "It comes off the baseboard easily. Whatever it hit, it hit hard enough to land closed."
    "I press the corner flat between my thumb and the heel of my hand, and run it along the crease twice, and it stays about eighty percent flat."
    "I put it on the counter, square with the edge, and I turn the lights off one at a time until the only one left in the house is the one over the stairs."
    stop sfxtrack2 fadeout 4.0
    $ hide_calendar()
    scene black with dissolve_scene_full
    pause 2.0
    return
