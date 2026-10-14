# lunchtime during school in chapter 4, on october 30th. MC, matsuda, monika, asahina, tsubaki, and sam are having a hangout session in the cafeteria during lunchtime
# everything's going fine and dandy and somehow we got into playing a legally distinct version of Uno, and then asahina gets a text that makes her actually crumple
# like, BONE-CHILLING text message (see the terror sprite). it's not explicitly said, but it's mom furiously telling her to get home immediately after school and that she has some explaining to do about sam
# she drops her cards almost dramatically so, matsuda initially thinks she's doing a bit and plays into it, and then asahina excuses herself to go to the bathroom
# someone has to tell matsuda to read the room
#
# CONTINUITY LOCKS
#   * Four days after the festival (Sat/Sun Oct 25-26), the day before Halloween.
#     Same day as ooc_1030_nothing_to_add, which is that NIGHT. This is the
#     morning side of the same guillotine and it must not know that.
#   * THE TEXT IS NEVER SHOWN AND NEVER PARAPHRASED. No phone UI, no
#     phone_text_conversation, no italicized narration of the words. MC is across
#     a table from a screen he cannot see. The terror sprite is the entire
#     delivery. Nobody in the scene ever learns what it said, including the
#     player.
#   * MC knows before anyone else does. He gets exactly one tell -- he is already
#     looking at the doors when she reaches them -- and the narration never
#     explains it. He is asked directly tonight. He is not asked here.
#   * Mom already knows Sam from May; the later private facts stay withheld.
#     Asahina says she has already cleared
#     tomorrow, in the past tense, about a thing she has not done. Nobody catches
#     it and nothing marks it.
#   * Sam is at this table. He is the subject of the message and he is four feet
#     away stealing food, and the scene never once points at that. He is also the
#     one who picks her chair up.
#   * She comes back before the bell with her face fixed. The wrongness is that
#     nothing is wrong.
#   * Tsubaki has been the rules authority all lunch. She lets the last card go
#     unchallenged. That is her whole reaction and she gets no line for it.
#   * Mom did not text MC. That is the last beat and it is not explained.
#
# THIS IS A GOOD LUNCH -- WRITE IT THAT WAY
#   The first two thirds are not setup. They are six people who have been friends
#   since May actively enjoying each other: cross-talk, food theft, a four-day-old
#   running joke everybody is sick of, an argument about a briefcase that never
#   resolves, and Matsuda standing on furniture. Tsubaki is LOOSE here -- five
#   months past the girl who apologized to a light-gun, winning and enjoying it.
#   If the reader is not sorry to lose this table, the turn does nothing.
#
# THE GAME
#   CRISIS! is a one-dollar clearance-table knockoff, badly translated, which is
#   why the mandatory one-card announcement is a full sentence -- "I AM IN
#   CRISIS" -- at "an audible volume", penalty three cards. Matsuda enforces this
#   like a magistrate. The briefcase card has no entry in the rules sheet, so she
#   rules that it means whatever she declares. That gag is funny five times and
#   then is the last thing she does in the scene.
#   Asahina must be HOLDING A HANDFUL when the phone goes -- she got the three-card
#   penalty for laughing through the announcement -- so the drop is plural and
#   loud. One card skids away face-down and stays there; that is the one she comes
#   back and plays.
#
# TIME PASSING -- FOUR DEVICES, ALL VISIBLE
#   1. fx_push on the bg for the whole lunch. Five minutes, five percent. Nobody
#      sees it happen; the room is smaller at the end than it was at the start.
#   2. The light. Bars of sun across the tile in the establishing shot, called out
#      as a countdown, gone by the last hand -- atmos("winter") -> atmos("winter_dim")
#      on a Dissolve, motivated on-screen by the sun leaving the window row.
#   3. The trays. Six full, then stacked, then pushed to the far end. Matsuda's
#      tower grows all lunch and is a running structural hazard.
#   4. Bodies. The table restages three times -- Monika arriving, Matsuda getting
#      on a chair, Sam moving up into Asahina's empty frame.
#
# AUDIO
#   emotions runs UNDER THE WHOLE LUNCH and is killed on Matsuda's SECOND bit
#   line -- after the drop, while the joke is still going. Do not fade it on the
#   buzz; the point is that the floor is already gone by the time anyone looks
#   down. Nothing replaces it, per the 12/24 rule about scoring a bad moment.
#   `ac` is on sfxtrack1 from the first frame to the last and never changes: this
#   is a tiled hall the size of a warehouse and the hum was always there. Killing
#   the music does not add a sound. It uncovers one.

label ooc_1030_uhoh:

    scene black
    stop music
    pause 1.5
    scene bg cafeteria_winter at fx_push(1.055, 300.0)
    $ atmos("winter")
    with dissolve_scene_full
    play sfxtrack1 ac loop
    play music ch4_day
    $ show_calendar()
    "The cafeteria seats four hundred and today it is doing about ninety, all of them packed down at the far end by the serving line. That leaves the window row to us and the light."
    "Our trays share a long table by the windows, where bars of sun stretch across the tile under our feet."
    show tsubaki uniform neut at t41
    show matsuda uniform neut at t42
    show asahina uniform neut at t43
    show sam uniform neut at t44
    "Matsuda has cleared a landing zone by stacking three trays on top of each other. She made us thank her before she dealt with the third."
    ma "Behold."
    "She sets a box down in the middle of the table."
    "The box is red, with a cartoon businessman sweating through his shirt while his tie points sideways. Four separate droplets, in case the title wasn't clear."
    show asahina uniform curious
    ah "What is that?"
    ma "{i}CRISIS!{/i}"
    show asahina uniform unamused
    ah "What is that?"
    ma "One dollar."
    show tsubaki uniform unamused
    ts "It was fifty cents."
    ma "It was one dollar {i}of value{/i}."
    show asahina uniform smug
    ah "Tsubaki, was it fifty cents?"
    show tsubaki uniform smug
    ts "It was fifty cents."
    ma "{i}Kareda.{/i}"
    "Tsubaki does not even look up. She has the lid off already and she is unfolding something out of the bottom of the box that keeps going."
    show tsubaki uniform thinking at h41
    ts "There are rules."
    ah "How many rules?"
    show tsubaki uniform unamused
    ts "It's the size of a road map."
    show sam uniform curious
    sa "Is that the whole thing or is that one side?"
    show tsubaki uniform empty
    ts "...This is one side."
    show asahina uniform happy
    ah "OH, that's beautiful."
    mc "Can I see the businessman again?"
    ma "You may not. He is evidence."
    "When Sam reaches for the lid, I slide it over so he can hold it beside Matsuda's face. He looks between them until she notices."
    show sam uniform smug
    sa "Yeah, no, I see it."
    ma "See {i}what{/i}?"
    show asahina uniform teasing
    ah "The tie!"
    ma "I do not wear a tie."
    ah "Spiritually!"
    "Matsuda takes the lid back with the dignity of a woman who has decided not to hear something."
    "She starts dealing before Asahina can add anything, sending the cards across the table in flat arcs. I barely catch mine before the next one lands on it."
    "Sam picks his hand up and has it sorted in about four seconds."
    show sam uniform thinking
    sa "Okay, it's the color one."
    ma "It is the color one."
    show sam uniform smug
    sa "I know the color one."
    show asahina uniform annoyed
    ah "He's going to win. He does this. He learns a game in one round and then he wins it {i}politely{/i}--"
    show sam uniform unamused
    sa "I've been here forty seconds."
    ah "--and then he says something modest and I have to sit with it."
    show sam uniform teasing
    sa "I would never."
    ah "You did it at the arcade. You did it with air hockey. You did it with air hockey against {i}me{/i}, and then you said I \"had a really strong second half.\""
    show sam uniform happy
    sa "You did have a really strong second half."
    show asahina uniform frustrated
    ah "SEE?"
    show tsubaki uniform shocked
    "Tsubaki lowers the rules sheet, checks the front of the box, and reads the same paragraph again."
    show tsubaki uniform worried
    ts "...There's a translation problem."
    ma "Read it."
    show tsubaki uniform neut
    ts "\"When the player is holding one card only, the player must announce.\""
    ma "Standard."
    ts "\"The announcement is: I AM IN CRISIS.\""
    "Asahina looks at the card in her hand, then at the title on the box."
    show asahina uniform shocked
    ah "The whole sentence?"
    ts "The whole sentence."
    ah "Out loud?"
    ts "\"At an audible volume.\""
    "Matsuda closes her eyes for a moment, the way somebody does when a gift has exceeded the occasion."
    ma "Fifty cents."
    show tsubaki uniform teasing
    ts "One dollar of value."
    ma "{i}KAREDA.{/i}"
    show tsubaki uniform happy
    "Tsubaki puts the sheet down and presses her wrist against her mouth, but that only makes the laugh come out through her nose."
    "She has to wave Matsuda away when she tries to take the rules back."
    show tsubaki uniform happy
    mc "What happens if you don't say it?"
    show tsubaki uniform neut
    ts "Three cards."
    mc "Three?"
    ts "Three."
    ma "The penalty is three because the penalty in the real game is two, and this game does not want to be sued."
    "The first hand takes a few minutes longer than it should because we keep arguing about the rules. Tsubaki settles one dispute by reading the relevant sentence twice, louder the second time."
    "Sam wins it."
    show asahina uniform smug
    ah "I {i}said{/i}."
    show sam uniform smug
    sa "I got lucky."
    ah "DON'T."
    show sam uniform teasing
    sa "...I had good cards."
    show asahina uniform annoyed
    ah "That's worse! Do you understand that that's worse?"
    "During the second hand, Asahina breaks a piece off Sam's bread. He pushes the tray closer without looking away from his cards."
    "Halfway through she holds a piece up and blows on it, twice, with enormous care."
    show asahina uniform happy
    ah "Careful. It's still hot."
    "Four days."
    ma "It has been four days."
    ah "It's still funny."
    ma "It was funny on Sunday."
    show tsubaki uniform unamused
    ts "It was funny on Sunday."
    mc "It was mildly funny on Sunday."
    show asahina uniform frustrated
    ah "You are all standing between me and the only material I have."
    show sam uniform happy
    sa "It's a little bit funny."
    show asahina uniform smug
    ah "THANK you."
    ma "He is compromised and his vote is struck."
    "Tsubaki wins the second hand."
    show tsubaki uniform happy
    "She chains four cards together before we can stop her, announces her last one, and places it squarely on the pile. Then she sits back, grinning while Asahina checks the cards."
    show asahina uniform shocked
    ah "...Okay, no."
    ts "Yes."
    ah "You were losing! You were {i}visibly{/i} losing!"
    ts "I know."
    ah "You did that on purpose?"
    show tsubaki uniform smug
    ts "Yes."
    show asahina uniform happy
    ah "MATSUDA. She's been doing a bit this whole time!"
    ma "I taught her everything she knows."
    show tsubaki uniform unamused
    ts "You taught me the shuffle."
    ma "I taught her the shuffle."
    show sam at thide
    hide sam
    show monika forward uniform happ om oe nobl rdown lpoint at t44
    "Monika arrives with a tray while we're collecting the second hand. She has a strip of laminating film stuck to her sleeve."
    m forward uniform happ cm oe nobl rdown ldown "Please tell me you have room for one more."
    ma "The civilian may sit if the civilian accepts the ruleset without amendment."
    m forward uniform curi om oe nobl rdown ldown "I'm hungry. Can I eat before I agree to anything?"
    ma "You may chew while you consider your allegiance."
    m forward uniform happ cm ce nobl rdown ldown "Deal me in."
    "I make room beside me while Sam moves past the trays at the far end. Monika sits down before Matsuda has finished dealing her cards."
    "Asahina takes one of Monika's fries during the transfer, in full view, at arm's length, with no attempt at concealment whatsoever."
    m forward uniform laug om ce nobl rdown ldown "I watched you do that."
    show asahina uniform smug
    ah "I know."
    m forward uniform happ cm oe nobl rdown ldown "You looked directly at me while you did it."
    ah "You took ages to sit down. I thought you weren't hungry."
    m forward uniform happ om oe nobl rhip ldown "I'm starving. Steal his."
    "She moves her tray out of reach and takes two of my fries before I can object."
    "Three hands in, Sam plays a card with a briefcase on it."
    "Everybody stops."
    mc "What's the briefcase?"
    show tsubaki uniform thinking
    "Tsubaki checks both columns, then turns the sheet over to study the diagram on the back."
    show tsubaki uniform frustrated
    ts "It isn't in here."
    ma "It is in the deck."
    ts "It's in the deck. It isn't in the rules."
    "Matsuda picks the card up and holds it toward the window like a jeweler."
    ma "Then the briefcase means what I say it means."
    show asahina uniform frustrated
    ah "You're making this shit up!"
    ma "It is how {i}this{/i} works, because the alternative is that we do not play, and we are playing."
    "She sets it down."
    ma "The briefcase reverses direction and is worth nine."
    show tsubaki uniform curious
    ts "Nine of what?"
    ma "Nine."
    m forward uniform laug om ce nobl rdown ldown "Nine what, though?"
    ma "NINE."
    sa "I'm fine with it."
    show asahina uniform annoyed
    ah "You're fine with it because it {i}helps{/i} you!"
    sa "I'm fine with it because I don't want to spend my lunch in a hearing."
    "Asahina aims a fry at him, holds it there, and does not come up with anything."
    show asahina uniform unamused
    ah "...Fine."
    mc "For the record, that's a suitcase."
    "The table goes up."
    ma "It is a BRIEFCASE."
    mc "It has wheels. Two of them, look."
    show tsubaki uniform unamused
    ts "That's a suitcase."
    ma "Kareda, do not do this to me."
    show tsubaki uniform smug
    ts "I'm looking at it."
    m forward uniform happ om oe nobl rdown lpoint "It's a little bit of a suitcase."
    ma "It is the briefcase, we have been calling it the briefcase all hand, and if it becomes the suitcase now then every ruling I have made today is retroactively--"
    show asahina uniform smug
    ah "Say it."
    ma "--{i}unsound{/i}."
    ah "SAY IT."
    ma "I will not."
    "Over the next four hands the briefcase also means skip everybody, draw one, draw four, and once, memorably, nothing at all, because Matsuda decides on the spot that this particular briefcase is empty."
    ah "It's a briefcase!"
    ma "Briefcases are frequently empty. It is the great tragedy of the form."
    "While we play, the bars of sunlight slide under the tables until I can no longer feel the warmth against my ankles."
    show bg cafeteria_winter_dim
    $ atmos("winter_dim")
    with Dissolve(1.6)
    "I pull my feet back under the chair as Matsuda reaches for the discard pile."
    show matsuda uniform neut at fx_lean_in, i42
    "Matsuda gets up on her chair."
    ma "RULING."
    mc "You can't be up there."
    ma "The elevation is procedural."
    show tsubaki uniform worried
    ts "The elevation is going to get us moved."
    ma "The briefcase is the briefcase. The matter is CLOSED. Kareda, strike the suitcase from the--"
    "A teacher on lunch duty says something across the room without appearing to raise her voice at all, which is a skill I have never understood."
    "Matsuda gets down."
    show matsuda uniform neut
    ma "The matter is closed."
    show asahina uniform smug
    ah "You got told off."
    ma "The matter is closed."
    "By now the trays are stacked four high at the end of the table and everybody has stopped pretending they are going to eat any more of it."
    "A phone at the next table plays the same tinny chorus twice. Monika taps it out beside her cards until I join in and she catches me watching."
    mc "So tomorrow."
    ma "TOMORROW."
    "The volume turns a couple of heads at the far end. She sees them and does not lower it much."
    ma "Tomorrow is Halloween and I have a costume that requires two people to put on."
    show asahina uniform unamused
    ah "That's not a costume, that's a job."
    ma "It is a costume, and one of you is going to be inside part of it."
    show tsubaki uniform determined
    ts "Not me."
    ma "I have not asked yet."
    show tsubaki uniform unamused
    ts "You were going to ask me."
    ma "...I was going to ask you."
    m forward uniform happ cm oe nobl rhip ldown "I can't. Council has the gym until six, and then I have to give it back in the condition I found it."
    show asahina uniform teasing
    ah "They're making you clean up as well? That sucks."
    m forward uniform laug om ce nobl rdown ldown "I agreed before they told me about the glitter."
    show asahina uniform curious
    ah "What is it, though? The costume."
    ma "You will see it tomorrow."
    ah "What is it?"
    ma "TOMORROW."
    ah "Is it the bird? Tsubaki, is it the bird?"
    show tsubaki uniform smug
    ts "I've been sworn."
    show asahina uniform happy
    ah "IT'S THE BIRD."
    ma "Nobody has confirmed a bird."
    show tsubaki uniform teasing
    ts "Nobody has confirmed a bird."
    show asahina uniform teasing
    ah "You two are the worst people I know and I'm going to be there at five."
    mc "You cleared it?"
    show asahina uniform neut
    ah "I already asked."
    "She fans her four cards, then closes them again, bending the corners against her palm."
    ah "It's fine. Friday's fine."
    sa "I can be there about five."
    ah "Five's good."
    "She says it to the cards."
    "Play comes back around. Monika drops a color change on the table and takes the whole thing sideways, and Asahina goes from four cards to one in a single turn nobody expected, including her."
    "She looks from her last card to us while Matsuda raises a finger, waiting for the announcement."
    # SFX SUGGESTION: A chair-back thump as she plants both hands and sits up.
    show asahina uniform determined
    ah "I AM IN CRISIS!"
    "It gets all the way across the room and comes back."
    "The teacher on lunch duty looks up, sees Asahina waving her card, and goes back to eating."
    ma "PENALTY."
    show asahina uniform shocked
    ah "WHAT?"
    ma "Three cards."
    show asahina uniform frustrated
    ah "I said the sentence! I said the whole sentence!"
    ma "You said it {i}laughing{/i}."
    ah "There's no--" with fx_punch_soft
    ah "Tsubaki. Tell her there's no conviction clause."
    show tsubaki uniform thinking
    "After checking the sheet, Tsubaki looks at Matsuda and folds the paper before Asahina can get a hand on it."
    show tsubaki uniform neut
    ts "There's a conviction clause."
    ah "THERE IS NOT!"
    ts "\"The announcement is made with conviction.\""
    show asahina uniform annoyed
    ah "SHOW ME."
    show tsubaki uniform smug
    ts "No."
    m forward uniform laug om ce nobl rdown ldown "Oh, that's {i}excellent{/i}."
    ah "Monika!"
    m forward uniform laug om ce nobl rdown ldown "I'm sorry. I'm so sorry. That was excellent."
    "Asahina takes the penalty cards one at a time, holding each up for Matsuda to inspect. Matsuda rests her chin on her gloves and applauds the third."
    show asahina uniform determined
    ah "I'm going to win from here."
    ma "You are four cards from the announcement and there are two players ahead of you."
    ah "I'm going to win from here and then I'm going to say the sentence so slowly."
    ma "Savor it in advance. It is the only part you are getting."
    ah "You're going to hear every word."
    ma "The reigning champion elects to savor!"
    show asahina uniform pose_hairflip
    ah "The reigning champion elects to SAVOR."
    "She taps her four cards into a neat pile while she waits for play to come around again."
    # SFX SUGGESTION: A phone buzzing face-down against a laminate table, twice.
    "Her phone goes off next to her tray."
    "She flips it over one-handed without breaking stride, the way you check a clock."
    show asahina uniform happy
    ah "And I want it noted, when it happens, that I did the whole sentence every single time even when this table--"
    "The word breaks off before she finishes it. I watch her eyes move back up the screen and start again."
    # SFX SUGGESTION: Cards hitting a laminate table and tile, scattered, not a stack.
    $ fx_shake_screen(11.0, 0.55)
    show asahina uniform terror at fx_flinch, i43
    "Her hand opens."
    "Cards go across the table, off the edge, under the chair beside her. One skids out past the tray tower and lands face-down on its own, and nobody picks anything up."
    "She has the phone in both hands now."
    "Her face has gone pale, and she keeps pressing her thumb against the edge of the phone."
    "She starts to say something, but I can't hear the word. Her mouth closes while Matsuda leans forward."
    ma "{i}Behold.{/i}"
    "Matsuda spreads her hands over the discarded cards."
    ma "The moment the challenger's nerve departs the building."
    "Asahina does not look up."
    stop music fadeout 3.0
    ma "Do not look away from this. This is where the legend fractures. This is the part they put in the documentary."
    "Sam laughs from the far end, then stops when he sees Monika's face."
    show tsubaki uniform shocked
    "Tsubaki has stopped with the rules sheet half-folded in her lap."
    ma "She's stalling. Kareda, is stalling addressed?"
    show tsubaki uniform worried
    ts "...No."
    ma "Then it is legal, and it is beneath her."
    "Asahina puts the phone face-down on the table."
    "She stands up too fast."
    # SFX SUGGESTION: A cafeteria chair going over backward onto tile, at volume.
    "Her chair goes over behind her." with fx_thud
    "Heads turn at the far end of the room."
    ah "Bathroom."
    "Her voice cracks on the second syllable. She swallows before trying again."
    ah "Bathroom. Sorry. Two seconds."
    "This time she says it in the voice she uses when she needs someone to move out of her way."
    ah "Don't let her rule anything while I'm gone."
    ma "I make no such undertaking."
    ah "Yeah."
    "She takes the phone but leaves everything else, including the drink her sleeve almost knocks over as she passes."
    # SFX SUGGESTION: Footsteps on tile crossing a large room, then a swing door and its return.
    show asahina at thide
    hide asahina
    "I am already looking at the doors when she gets to them."
    "..."
    "The far end of the room goes back to what it was doing. Trays, chairs, somebody's speaker with all the treble and none of the rest."
    ma "...Ladies and gentlemen, the reigning champion has withdrawn to consult her attorneys."
    "Monika keeps her eyes on Asahina's empty chair."
    ma "Which I want on the record is a {i}very{/i} strong--"
    m forward uniform neut cm oe nobl rdown ldown "Matsuda."
    ma "--closing statement, and--"
    m forward uniform neut cm oe nobl rdown ldown "Read the room."
    "Matsuda's hands come down."
    show tsubaki uniform afraid
    "She follows Tsubaki's gaze to the doors, then looks down at the overturned chair and the cards under it."
    ma "..."
    ma "Yeah."
    "She draws her hands back from the table and puts them in her lap."
    show sam uniform neut at t43
    "Sam comes up the table to right the chair, pushing it in before he looks toward the doors."
    show sam uniform determined
    sa "I'll go check on her."
    menu:
        "\"It's a family thing. She's fine.\"":
            $ s1_pick("ooc1030_lunch_table", "cover")
            mc "It's a family thing. She's fine."
            "I answer before he has finished turning toward me. My voice sounds too loud after sitting silent."
            show sam uniform thinking
            sa "...Okay."
            mc "Sit down. Eat your food."
        "\"I've got it.\"":
            $ s1_pick("ooc1030_lunch_table", "claim")
            mc "I've got it."
            "I do not stand up."
            show sam uniform worried
            sa "You sure?"
            mc "Yeah."
            "He waits about a second longer than he needs to."
        "(Say nothing.)":
            $ s1_pick("ooc1030_lunch_table", "silent")
            mc "..."
            "He looks at me for an answer, but I keep my hands on the table."
            show sam uniform worried
            sa "...Right."
    show sam uniform neut
    sa "Tell her I've got her tray if they start clearing."
    mc "Sure."
    "He goes back to his end and picks his cards up. He does not look at them."
    show sam at thide
    hide sam
    "Monika lays her cards facedown, then reaches toward the box."
    m forward uniform neut cm oe nobl rdown ldown "We can pack it up."
    ma "No."
    ma "Leave it exactly like this."
    "Nobody argues with her."
    "We leave the cards where they are, including Asahina's four scattered across the table and floor. One lies face-down beyond the tray tower, beside her drink."
    show tsubaki uniform worried
    "Tsubaki folds the rules sheet along its original creases, all six of them, and does not put it away."
    ts "...Should somebody--"
    m forward uniform neut cm oe nobl rdown ldown "Give her a minute."
    show tsubaki uniform sad
    ts "Okay."
    "Four minutes go by."
    "I watch the minute hand jump four times on the clock over the serving line."
    # SFX SUGGESTION: The swing door again, from across the room.
    show asahina uniform neut at t43
    "When she comes back, she pulls the chair in and places her phone facedown beside the tray."
    ah "Okay. Sorry. Whose turn?"
    "She looks from Matsuda to the pile, waiting for an answer."
    ma "Yours."
    ah "Right."
    "The card beyond the trays is the only one she can reach without getting up."
    "She reaches over and turns it up, studying it before placing the briefcase on a red card, though the case is blue."
    "The rules sheet does not get consulted."
    show tsubaki uniform neut
    "Tsubaki says nothing."
    "Matsuda takes a long time with the card."
    ma "...That wins."
    ah "It wins?"
    ma "It's the briefcase."
    ah "Ha. Yeah it is."
    "Asahina sits back while Matsuda gathers the cards, reaching under the table for the ones by her chair. She squares the deck against the laminate with three sharp taps."
    m forward uniform happ cm oe nobl rdown ldown "Undefeated."
    ah "Undefeated."
    ma "Undefeated and under review."
    ah "Undefeated!"
    # SFX SUGGESTION: The end-of-lunch bell, and the whole room standing up at once.
    "The bell goes."
    "Four hundred seats' worth of noise out of ninety people, all of it at once, chairs and trays and the doors at the far end getting a workout."
    "We stand up in the middle of it."
    ma "Tomorrow. Five o'clock. I need one volunteer for the interior."
    show tsubaki uniform unamused
    ts "Still not me."
    ma "Kareda, you are the correct height."
    show tsubaki uniform annoyed
    ts "That is a horrible reason."
    ma "It is the only reason that matters."
    ah "It's the bird."
    ma "It is not the bird."
    "Sam has both trays, his and Asahina's, stacked the way Matsuda stacks them."
    sa "Five still work for you?"
    ah "Yeah. Probably."
    "She picks up her bag."
    ah "I'll text you."
    sa "Cool."
    "Sam takes the trays to the return while Asahina shoulders her bag."
    show tsubaki at thide
    hide tsubaki
    show matsuda at thide
    hide matsuda
    show monika at thide
    hide monika
    show asahina at thide
    hide asahina
    "The others head for the stairs, with Tsubaki breaking off toward the second-year corridor. Asahina goes the other way without looking back."
    "As the room empties, I take out my phone and check the notifications."
    "Nothing from Mom."
    "I open her thread to make sure."
    $ hide_calendar()
    scene black with dissolve_scene_full
    stop sfxtrack1 fadeout 4.0
    pause 2.0
    return
