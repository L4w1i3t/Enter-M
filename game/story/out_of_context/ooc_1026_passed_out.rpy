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
#   * Mom already knows Sam from May. Later private facts remain withheld.
#     Drunk Mom goes one step past where sober Mom
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
#   ch4_night runs UNDER THE WHOLE COMEDY at full strength and is killed on the
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
    play music ch4_night
    $ show_calendar()
    mc "I need a shower. If I sit down first, I'm sleeping here."
    "My head throbs as I bend to untie my shoes, and I have to catch the wall before I can straighten up."
    show asahina frustrated at t11
    # SETTING RULE: "takoyaki" was a loanword; swapped for the plain-English version
    # per the arbitrary-setting sweep. Same joke, same triple.
    ah "Remind me to never, EVER, take over someone else's shift at a fry stand. Or vote to run a fry stand. Or anything involving a fryer."
    mc "You volunteered."
    show asahina unamused
    ah "I volunteered {i}you{/i}. There's a difference."
    "She toes her shoes off without untying them, which Mom has asked her not to do roughly nine hundred times."
    ah "Two days. Two days of standing in front of that damn fryer saying the same four words."
    mc "Which four?"
    ah "\"Careful, it's still hot.\""
    mc "That's five if you split the contraction."
    ah "...Two days of that. And now this."
    "She yawns so hard she has to put a hand on the wall."
    "Every light downstairs is on, though nobody answers when I push the door shut."
    mc "Mom? We're back--"
    "A glass knocks against wood in the dining room."
    pause 2.0
    scene bg dining_table_night
    $ atmos("home_night")
    with dissolve_scene_full
    "She's at the dinner table with her back to us, still in the cardigan she wears for grocery runs."
    "One glass lies on its side beside her elbow, while another stands near the middle of the table. She has a third in her hand."
    show mom wasted at t22
    show asahina shocked at t21
    mom "Oh! Is that the door?!"
    "She asks the kitchen."
    mc "...Yeah. Hi."
    mom "THERE they are!"
    "It takes her a moment to turn toward us, but when she does she grins and lifts both hands."
    mom "My children! Both of them! At the same time!"
    ah "...Uh."
    mom "Come in, come in, sit down, don't just stand there in the--in the--the doorway part thingy."
    mc "The doorway."
    mom "Thank you!"
    ah "Mom, what is happening right now?"
    mom "I am having a very nice Sunday, thank you!"
    "She lifts the upright glass to about eye level, toasts nothing in particular, and puts it back down without drinking any of it."
    mom "I only had the one."
    show asahina unamused
    ah "There are three."
    mom "There are three GLASSES. I only had the one."
    mc "How much was in the one?"
    show asahina curious
    ah "How long have you been down here?"
    mom "Since the thing finished! On the television! With the man!"
    mc "The man?"
    mom "He had a little boat!"
    ah "What channel, Mom?"
    mom "It was a LOVELY little boat, Asahina."
    ah "Okay!"
    mom "Don't 'okay' me. You weren't there. You didn't {i}see{/i} the boat."
    show asahina nervous
    "My sister turns to me with her mouth open, then clamps it shut to keep from laughing."
    ah "...I'm getting my phone."
    mom "Get your phone!"
    show asahina smug
    ah "I'm so going to record this."
    mom "{i}Record{/i} it! See the man with the boat!"
    mc "You'd ruin her image, Asa?"
    show asahina happy
    ah "Dude, does it look like I care? This is comedy gold!"
    mom "I want it on the record that I said record it!"
    "She points at the table with the same finger she uses when we leave dishes in the sink."
    mom "Are you hungry? Are you two hungry? I could do something!"
    mc "It's nine at night."
    mom "I could do the rice!"
    mc "Mom."
    mom "The rice, and the little peppers, and there's that fish in the--"
    show asahina unamused
    ah "There's no fish."
    mom "There is ALWAYS fish, my dear."
    "She starts to stand, then catches the table with both hands. I steady the chair while she lowers herself back into it."
    mom "...In a minute."
    mc "Sure."
    mom "I'm doing the fish in a minute."
    show asahina frustrated
    ah "There's no fish!!!"
    mom "In... a MINUTE."
    "My sister pulls out the chair across from her and sits, which is the first sign all night that she isn't going straight up."
    show asahina neut
    ah "We ate already with Matsuda and everyone. We're fine."
    mom "FRIENDSHIP!"
    mc "Yes, Mom. Friendship."
    ah "It was a long day."
    mom "That's my girl. That's my--that's my girl."
    "She reaches toward Asahina, misses her sleeve, and pats the table instead."
    mom "[player]."
    mc "Yeah?"
    mom "You have a very good face."
    mc "Thanks?"
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
    "Asahina's laugh cuts off while her hand is still over her eyes."
    "She lowers both hands beside her phone, which is now facedown on the table."
    ah "...What?"
    "Mom squints across the table, trying to catch her eye."
    mom "The one with the bicycle!"
    "I have never in my life heard about a boy with a bicycle."
    mom "You said! About the bicycle."
    show asahina neut
    ah "...Oh. {i}Him{/i}. Yeah, he's--he's fine."
    ah "Little twelve-year-old weirdo though."
    mom "GOOD."
    "Mom turns back to me while Asahina pulls her hands into her lap."
    mom "Daaaaamn, you two got so TALL."
    show asahina teasing
    ah "That's what happens."
    mom "I know what happens!"
    "She props her chin on her hand as she looks from one of us to the other."
    mom "I know exactly what happens."
    mom "Just think, though, how tall you'll be by the time you're my age! You'll be giants!"
    "She tries to line up the glass on its side with the others, but it rolls away each time she lifts her hand. Eventually she leaves it."
    mom "...I only had the one."
    "Nobody corrects her."
    "Asahina catches my eye and tips her head toward the stairs while Mom studies the glasses."
    show asahina determined
    ah "Should we get her upstairs?"
    menu:
        "\"I've got her. Go up.\"":
            $ s1_pick("ooc1026_mom_table", "steady")
            mc "I've got her. Go up."
            show asahina curious
            ah "You sure?"
            mc "I can help her up. Bring the water?"
        "\"...Is she okay?\"":
            $ s1_pick("ooc1026_mom_table", "ask")
            mc "...Is she okay?"
            "Asahina looks back at Mom before answering."
            show asahina unamused
            ah "I've never seen her this drunk."
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
    "She puts the glass back down to stand, so Asahina takes it while I help her out of the chair."
    "She gets an arm across my shoulders and most of her weight through it, and starts telling me about the man with the little boat."
    mom "You'd have liked him. He had a whole system going."
    mc "For... the boat?"
    mom "For the {i}boat{/i}, yes! Adapt or be left behind, I say!"
    "{i}Where have I heard that before?{/i}"
    "As we turn toward the stairs, something glossy catches the light beside the wall."
    stop music fadeout 3.0
    play sfxtrack2 tick loop
    "A pamphlet lies against the baseboard with one corner folded back over a smiling face. From here I can make out a phone number, but not the small print."
    "Mom tightens her arm around my shoulders as we reach the first step, still telling me about the boat."
    $ hide_calendar()
    scene black with dissolve_scene_full
    nier "Asahina brings up the water while I help Mom to her room. By the time we have her settled, she has started apologizing every time I move a pillow."
    call nier_clear from _call_nier_clear_1026_1
    pause 2.0
    scene bg dining_table_night
    $ atmos("home_night")
    $ show_calendar()
    with dissolve_scene_full
    show asahina worried at t11
    "Asahina is back at the table when I come down, still wearing her jacket."
    ah "Is she out?"
    mc "Nearly. She asked me to leave the door open."
    ah "...That was weird, right? Like, that was actually weird."
    ah "She's usually the one telling us to go to bed."
    mc "Yeah. I know."
    show asahina frustrated
    ah "She was being so {i}nice{/i}."
    "She pulls at her jacket cuff until it covers her fingers."
    mc "So how's the video?"
    show asahina neut
    ah "...I didn't record it."
    mc "You said about nine times that you were--"
    show asahina annoyed
    ah "I know what I said."
    "I rub my eyes, still gritty from the walk home."
    mc "Go to bed, Asa."
    show asahina teasing
    ah "{i}You{/i} go to bed."
    mc "I'm GOING to bed!"
    ah "Then go to bed!!"
    "She takes the stairs two at a time and shuts her door hard enough to rattle the frame."
    show asahina at thide
    hide asahina
    "I take the three glasses to the sink, leaving the tallest until last. I think it belongs in the cabinet over the fridge, where we keep the vases."
    "After I wash and dry it, I put it beside the vases because I can't remember where else it goes."
    "Then I go and crouch down by the wall."
    "The pamphlet is still closed when I pick it up by the bent corner."
    "I run my thumb over the crease twice, but the corner lifts again as soon as I let go."
    "I put it on the counter, square with the edge, and I turn the lights off one at a time until the only one left in the house is the one over the stairs."
    stop sfxtrack2 fadeout 4.0
    $ hide_calendar()
    scene black with dissolve_scene_full
    pause 2.0
    return
