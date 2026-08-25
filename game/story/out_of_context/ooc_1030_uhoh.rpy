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
#   * Asahina is still hiding Sam from Mom. She says she has already cleared
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
    scene bg cafeteria at fx_push(1.055, 300.0)
    $ atmos("winter")
    with dissolve_scene_full
    play sfxtrack1 ac loop
    play music emotions
    $ show_calendar()
    "The cafeteria seats four hundred and today it is doing about ninety, all of them packed down at the far end by the serving line. That leaves the window row to us and the light."
    "Six trays. One long table. Four bars of sun lying across the tile at an angle that gives them about twenty minutes to live."
    show tsubaki uniform neut at t41
    show matsuda uniform neut at t42
    show asahina uniform neut at t43
    show sam uniform neut at t44
    "Matsuda has cleared a landing zone by stacking three trays on top of each other. She performed this as a public service and narrated it as one."
    ma "Behold."
    "She sets a box down in the middle of the table."
    "It is red. It is loud. A cartoon businessman is coming apart on the front of it, tie horizontal, four separate sweat droplets rendered with real commitment."
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
    "Sam reaches across me for the box lid and I let him have it, and then he holds it up next to Matsuda's face and looks between the two of them for a while."
    show sam uniform smug
    sa "Yeah, no, I see it."
    ma "See {i}what{/i}?"
    show asahina uniform teasing
    ah "The tie!"
    ma "I do not wear a tie."
    ah "Spiritually!"
    "Matsuda takes the lid back with the dignity of a woman who has decided not to hear something."
    "She deals. She deals in white gloves, at speed, and the cards come off the deck in clean flat arcs that reach each of us face-down and square."
    "Nobody comments on it. I think we all decided months ago that asking would cost us something."
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
    "Tsubaki has gone very still behind the rules sheet in the way she does when a document turns out to be worse than expected."
    show tsubaki uniform worried
    ts "...There's a translation problem."
    ma "Read it."
    show tsubaki uniform neut
    ts "\"When the player is holding one card only, the player must announce.\""
    ma "Standard."
    ts "\"The announcement is: I AM IN CRISIS.\""
    "There is a pause at the table that lasts about a second and a half."
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
    "That one gets Tsubaki properly, and she has to put the sheet down on the table and press the back of her wrist against her mouth, and she is no good for about ten seconds."
    "In May she would have apologized for that."
    show tsubaki uniform happy
    mc "What happens if you don't say it?"
    show tsubaki uniform neut
    ts "Three cards."
    mc "Three?"
    ts "Three."
    ma "The penalty is three because the penalty in the real game is two, and this game does not want to be sued."
    "The first hand takes eleven minutes and produces two rules disputes, one of which Tsubaki settles by reading the same sentence out loud twice until everybody hears it the same way."
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
    "Somewhere in the second hand my sister discovers that Sam's tray has the good bread on it and begins a slow annexation that he does not contest at any point."
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
    "She wins it from four cards down with a chain nobody sees coming, and she puts her last card on the pile and then sits back and folds her hands and does not say anything at all, and the smile she is doing is not a small one."
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
    "Monika arrives at the end of it with a tray and the expression of someone who has spent forty minutes in a room with a laminator."
    m forward uniform happ cm oe nobl rdown ldown "Is this a closed table, or may a civilian sit down?"
    ma "The civilian may sit if the civilian accepts the ruleset without amendment."
    m forward uniform curi om oe nobl rdown ldown "That is the kind of sentence people say right before you find out about the ruleset."
    ma "It is exactly that."
    m forward uniform happ cm ce nobl rdown ldown "Deal me in."
    "The whole table shunts down one to make it work. Sam ends up past the tray tower at the far end, where he will spend the rest of lunch being a voice with an arm attached."
    "Asahina takes one of Monika's fries during the transfer, in full view, at arm's length, with no attempt at concealment whatsoever."
    m forward uniform laug om ce nobl rdown ldown "I watched you do that."
    show asahina uniform smug
    ah "I know."
    m forward uniform happ cm oe nobl rdown ldown "You looked directly at me while you did it."
    ah "It's a courtesy. So you know it's happening."
    m forward uniform happ om oe nobl rhip ldown "I appreciate the transparency."
    ah "It's the only kind of theft I respect."
    "Three hands in, Sam plays a card with a briefcase on it."
    "Everybody stops."
    mc "What's the briefcase?"
    show tsubaki uniform thinking
    "Tsubaki turns the sheet over. Turns it back. Runs a finger down one column and then the other, and then down the back of it, where there is nothing but a diagram of a hand."
    show tsubaki uniform frustrated
    ts "It isn't in here."
    ma "It is in the deck."
    ts "It's in the deck. It isn't in the rules."
    "Matsuda picks the card up and holds it toward the window like a jeweler."
    ma "Then the briefcase means what I say it means."
    show asahina uniform frustrated
    ah "That's not how anything works!"
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
    mc "It has a handle on the long side."
    show tsubaki uniform unamused
    ts "That's a suitcase."
    ma "Kareda, do not do this to me."
    show tsubaki uniform smug
    ts "I'm looking at it."
    m forward uniform happ om oe nobl rdown lpoint "It's a little bit of a suitcase."
    ma "It is the briefcase, it has been the briefcase for three hands, and if it becomes the suitcase now then every ruling I have made today is retroactively--"
    show asahina uniform smug
    ah "Say it."
    ma "--{i}unsound{/i}."
    ah "SAY IT."
    ma "I will not."
    "Over the next four hands the briefcase also means skip everybody, draw one, draw four, and once, memorably, nothing at all, because Matsuda decides on the spot that this particular briefcase is empty."
    ah "It's a briefcase!"
    ma "Briefcases are frequently empty. It is the great tragedy of the form."
    "The light comes off the window row somewhere in there."
    "It goes the way it always goes, which is all at once and then not at all: the bars on the tile shorten, slide under the tables, and are gone, and the room turns the flat gray-white it stays until the end of the day."
    $ atmos("winter_dim")
    with Dissolve(1.6)
    "Nobody looks up. Ninety people at the far end and not one of them notices the building change color."
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
    "Somebody's phone is playing something at the next table over with the treble turned all the way up, and Monika has been quietly conducting it with one finger for about a minute without seeming to know she is doing it."
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
    ah "That's so sad. That's the saddest thing anybody's said at this table."
    m forward uniform laug om ce nobl rdown ldown "Thank you. I've been sitting with it since Tuesday."
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
    "She has four cards left, and she is fanning them out and closing them again, over and over, in a way that is going to absolutely destroy the corners."
    ah "It's fine. Friday's fine."
    sa "I can be there about five."
    ah "Five's good."
    "She says it to the cards."
    "Play comes back around. Monika drops a color change on the table and takes the whole thing sideways, and Asahina goes from four cards to one in a single turn nobody expected, including her."
    "She looks at the card in her hand."
    "She looks up."
    "Everybody at the table understands what is about to happen and not one person moves to stop it."
    # SFX SUGGESTION: A chair-back thump as she plants both hands and sits up.
    show asahina uniform determined
    ah "I AM IN CRISIS!"
    "It gets all the way across the room and comes back."
    "At the far end, the teacher on lunch duty looks up, identifies the source, evaluates the threat, and returns to a plate of something beige."
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
    "Tsubaki reads the sheet for a long moment."
    "Then she looks at Matsuda."
    "Then she folds the sheet in half."
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
    "Asahina takes her three cards one at a time, with a look on her face for each one, and Matsuda watches her do it with her chin on her gloved hands like a woman at the theater."
    show asahina uniform determined
    ah "I'm going to win from here."
    ma "You are four cards from the announcement and there are two players ahead of you."
    ah "I'm going to win from here and then I'm going to say the sentence so slowly."
    ma "Savor it in advance. It is the only part you are getting."
    ah "You're going to hear every word."
    ma "The reigning champion elects to savor!"
    show asahina uniform pose_hairflip
    ah "The reigning champion elects to SAVOR."
    "She sheds two on her next turn and the table starts making noise about it."
    # SFX SUGGESTION: A phone buzzing face-down against a laminate table, twice.
    "Her phone goes off next to her tray."
    "She flips it over one-handed without breaking stride, the way you check a clock."
    show asahina uniform happy
    ah "And I want it noted, when it happens, that I did the whole sentence every single time even when this table--"
    "She stops."
    "She stops in the middle of a word."
    "..."
    "I watch her eyes go back up to the top and start it over."
    # SFX SUGGESTION: Cards hitting a laminate table and tile, scattered, not a stack.
    $ fx_shake_screen(11.0, 0.55)
    show asahina uniform terror at fx_flinch, i43
    "Her hand opens."
    "Cards go across the table, off the edge, under the chair beside her. One skids out past the tray tower and lands face-down on its own, and nobody picks anything up."
    "She has the phone in both hands now."
    "There is no color in my sister's face. None. She has gone the shade of the tile."
    "She tries to say something and the front half of it comes out with nothing behind it, so she stops and does not try again."
    ma "{i}Behold.{/i}"
    "Matsuda has both hands out over the table like a woman presenting a body."
    ma "The moment the challenger's nerve departs the building."
    "Asahina does not look up."
    stop music fadeout 3.0
    ma "Do not look away from this. This is where the legend fractures. This is the part they put in the documentary."
    "Sam laughs. It's a good line."
    "Nobody else does."
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
    "Ninety people at the far end of the room look at us all at once."
    ah "Bathroom."
    "It comes out wrong. It comes out about half an octave off and with a break in the middle of a two-syllable word, and she hears it happen."
    "So she stops. And she resets. And she does it again."
    ah "Bathroom. Sorry. Two seconds."
    "That one is perfect."
    "That one sounds exactly like my sister."
    ah "Don't let her rule anything while I'm gone."
    ma "I make no such undertaking."
    ah "Yeah."
    "She takes the phone."
    "She leaves her tray, her bag, her drink, and her cards all over the floor, and my sister has never once in her life left a table without her drink."
    # SFX SUGGESTION: Footsteps on tile crossing a large room, then a swing door and its return.
    show asahina at thide
    hide asahina
    "I am already looking at the doors when she gets to them."
    "..."
    "The far end of the room goes back to what it was doing. Trays, chairs, somebody's speaker with all the treble and none of the rest."
    ma "...Ladies and gentlemen, the reigning champion has withdrawn to consult her attorneys."
    "It lands on the table and does not do anything."
    ma "Which I want on the record is a {i}very{/i} strong--"
    m forward uniform neut cm oe nobl rdown ldown "Matsuda."
    ma "--closing statement, and--"
    m forward uniform neut cm oe nobl rdown ldown "Read the room."
    "Matsuda's hands come down."
    show tsubaki uniform afraid
    "She looks at Tsubaki, who is looking at the doors. She looks at the chair on its back on the tile. She looks at the tray, and the drink, and the cards all over the table and the floor."
    ma "..."
    ma "Yeah."
    "That is all she says. She does not apologize, and nobody asks her to, and I think if she had it would have been worse."
    show sam uniform neut at t43
    "Sam comes up the table and rights the chair and pushes it back in, and then he does not sit down in it."
    show sam uniform determined
    sa "I'll go check on her."
    menu:
        "\"It's a family thing. She's fine.\"":
            $ s1_pick("ooc1030_lunch_table", "cover")
            mc "It's a family thing. She's fine."
            "It comes out level, and it comes out fast, and it is the first thing I have said in about ninety seconds."
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
            "I look at him until he stops asking."
            show sam uniform worried
            sa "...Right."
    show sam uniform neut
    sa "Tell her I've got her tray if they start clearing."
    mc "Sure."
    "He goes back to his end and picks his cards up. He does not look at them."
    show sam at thide
    hide sam
    "Monika has stacked her hand neatly in front of her and put both palms flat on the table on either side of it."
    m forward uniform neut cm oe nobl rdown ldown "We can pack it up."
    ma "No."
    ma "Leave it exactly like this."
    "Nobody argues with her."
    "So it sits there. Five hands face-down, Asahina's four all over the table and the floor, one of them out past the tray tower on its own, and a drink nobody is going to finish."
    show tsubaki uniform worried
    "Tsubaki folds the rules sheet along its original creases, all six of them, and does not put it away."
    ts "...Should somebody--"
    m forward uniform neut cm oe nobl rdown ldown "Give her a minute."
    show tsubaki uniform sad
    ts "Okay."
    "Four minutes go by."
    "I know it is four because the clock over the serving line is the kind with a hand that jumps, and I watch all of them."
    # SFX SUGGESTION: The swing door again, from across the room.
    show asahina uniform neut at t43
    "She comes back."
    "She sits down, pulls the chair in, and puts her phone face-down beside her tray with the screen against the table."
    ah "Okay. Sorry. Whose turn?"
    "Her face is completely fine."
    "That is the part."
    ma "Yours."
    ah "Right."
    "The only card left in front of her is the one that went out past the trays on its own."
    "She reaches over and turns it up."
    "She checks it for a second, like it might have changed since it landed, and then she plays it, and it is the briefcase, and the color on the table has been wrong for two turns."
    "The rules sheet does not get consulted."
    show tsubaki uniform neut
    "Tsubaki says nothing."
    "Matsuda takes a long time with the card."
    ma "...That wins."
    ah "It wins?"
    ma "It's the briefcase."
    ah "Ha. Yeah it is."
    "She sits back and lets herself have it, and Matsuda starts collecting the cards in, gloves and all, off the table and then off the floor, squaring them against the laminate in three sharp taps."
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
    "And that is it. That is the whole thing."
    show tsubaki at thide
    hide tsubaki
    show matsuda at thide
    hide matsuda
    show monika at thide
    hide monika
    show asahina at thide
    hide asahina
    "They go one way toward the third-year stairs and Asahina goes the other way with the rest of her year, and the tile where the light was is the same flat gray as the rest of it."
    "I stand there for a second with the room emptying around me."
    "Then I take my phone out."
    "..."
    "Nothing."
    "No missed call. No message. Not from Mom, not from anybody."
    "I check it twice, in case."
    $ hide_calendar()
    scene black with dissolve_scene_full
    stop sfxtrack1 fadeout 4.0
    pause 2.0
    return
