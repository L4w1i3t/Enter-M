# Wednesday, June 4. Lunch. MC has a hiding place in the west corridor and
# Matsuda has found it, and he has not moved. Then a boy called Daichi walks up
# and asks her out, and she takes the entire thing apart in public.
#
# WHY THIS SCENE EXISTS
#   To say, structurally and without anybody announcing it, that this is not a
#   dating sim.
#
#   Daichi's approach is a confession event with every prop in place: he picked
#   a day, he picked a place, he waited for a gap, his friends are watching from
#   the stairwell. Any player who has touched the genre knows the shape of it
#   from four seconds out. What the scene does with that shape is the point --
#   Matsuda does not answer the MAN, she answers the REQUEST, and what she
#   refuses is the transaction rather than the person. Nothing unlocks. No flag
#   moves. The menu after it is a stance menu that changes nothing, which is the
#   s1_choices contract doing the theme's job for free.
#
#   Second half of the brief: Matsuda knows exactly what she has. She says so
#   out loud, at volume, crudely, and it is not flirtation and it is not
#   modesty-fishing -- it is an inventory, delivered as a public service, by a
#   woman who has been through this before and would like to do it once.
#
# THE RULE THIS SCENE IS BUILT ON -- MC IS NOT IN THE TRIANGLE
#   Four people in the corridor and one of them is the narrator, and at no
#   point does anything wait for him. He is not asked. He does not get jealous.
#   Matsuda never checks his face. He gets exactly one line about the impulse to
#   speak -- "nothing in the corridor was waiting for me to" -- and then he
#   drinks his drink. That single line is the entire meta statement and it must
#   never be topped up with a second one. Do not let a later pass add a beat
#   where MC feels something about her turning a boy down.
#
# CONTINUITY LOCKS
#   * Eighteen days after they met on 05/17 and four days after the arcade on
#     05/31 -- MC counts it in days on-screen, because he is the narrator who
#     ran an internet search on a bottle cap. MC has decided to
#     be friends with her; the decision is administrative, not warm, and the
#     scene shows it by having him keep turning up rather than by saying it.
#   * THE ORANGE DRINK is the 05/15 bottle cap paying off (0515.rpy:167 --
#     "some sort of imported soda", planted for exactly this). Per the
#     arbitrary-setting rule nothing on the can names a country: the only word
#     on it in our alphabet is ORIGINAL.
#   * "Out of ten" is the spine. She asks four times and he refuses four times,
#     and the number he finally gives is the last line of the scene. It is
#     SEVEN, it is not generous, and that is why it works. Nobody connects it to
#     Daichi out loud and nobody may be allowed to later.
#   * The public joke and the private truth are THE SAME SENTENCE -- "if I say
#     it small they ask again on Thursday" -- once at hallway volume as a laugh
#     line, once flat, four minutes apart. If either half moves, both move.
#   * She stops drinking the moment Daichi says the television line and does not
#     pick the can up again until MC gives her the number. That is her whole
#     reaction to being told she should be famous and it gets no narration.
#   * She does not take the bard off. On 05/19 MC asked her to and she did, and
#     she has done it for him since. Here she keeps it on for the rest of lunch
#     except for one sentence. MC notices and says nothing.
#   * Two-hander on purpose. Monika, Tsubaki and Asahina are all in this
#     building and none of them may walk past.
#   * Daichi is a decent person for ninety seconds and then he is gone forever.
#     The narration takes him completely seriously the whole time. He is not a
#     joke, he is not a creep, and the game simply does not follow him.
#
# AUDIO -- THE LOUDEST DECISION IN THE FILE
#   `schooldays` runs from the first line to the last and never changes. There
#   is no second cue, no fade on the ask, no sting on the shutdown.
#   Specifically: `enterm` DOES NOT PLAY. On 05/19 Matsuda's theme starts the
#   instant she goes theatrical. Here she performs harder than she has all year
#   and the game declines to score it, because a hero cue would make this a
#   victory and it is not one. The building does not notice any of this happen.
#   That is the production note and it is the whole thesis.

label ooc_0604_out_of_ten:

    scene black
    stop music
    pause 1.5
    scene bg corridor
    $ atmos("afternoon")
    with dissolve_scene_full
    play music schooldays
    $ show_calendar()

    # SFX SUGGESTION: A corridor at lunch -- distant doors, shoes on hard floor,
    # two hundred conversations with none of the words in any of them.
    "The west corridor at lunch is loud in a way that works out in my favor."
    "Nobody tries to sit with you here. There is nowhere to sit. There is a radiator, a run of windows with the sun coming in at an angle that will be gone by fifth period, and enough noise that a person standing on his own reads as a person waiting for somebody."
    "Twenty-five minutes, back against the wall, food in one hand. I built the whole system myself and I was proud of it for about a year."
    "Last week Matsuda found it."
    "I could have moved. There is an entire building. There is a roof."
    "I keep turning up at my own hiding place on time instead, and lately there are two of us in it, and I have not put a lot of effort into examining that."

    show matsuda uniform neut at t11
    ma "--and I said to him, sir, that is not a queue, that is a CLOT."
    mc "Hey."
    ma "Hello. Hold this."

    "Two cans. One of them arrives in my hand before I agree to it."
    "They're orange. Not orange-flavored, not orange-colored. Orange the way a traffic cone commits to it."
    "The label is in a language I don't read. The only word on the whole can in our alphabet is ORIGINAL, in a font nobody has redrawn since about 1950."

    menu:
        "\"This is my spot, you know.\"":
            $ s1_pick("ooc0604_wall_spot", "claim")
            mc "You know this is my spot."
            ma "It has excellent light and no chairs. I understand the appeal completely."
            mc "That's not what I said."
            ma "It's what you'll mean by Friday."
        "(Move over.)":
            $ s1_pick("ooc0604_wall_spot", "room")
            "I shift about eight inches down the wall without deciding to."
            "She takes the eight inches."
            ma "Thank you."
        "\"How did you even find me?\"":
            $ s1_pick("ooc0604_wall_spot", "ask")
            mc "How did you find me the first time?"
            ma "You are six feet tall and you eat standing up in a corridor."
            ma "I did not find you. I noticed you, the way one notices scaffolding."

    ma "Drink it."
    mc "What is it?"
    ma "Imported."
    mc "From where?"
    ma "Away."

    "I drink some of the away."
    "..."
    "It is a lot."

    ma "Verdict."
    mc "I've had one sip."
    ma "One sip is the whole event. Everything after it is politics."
    mc "...It's orange."
    ma "That is a color."
    mc "It's aggressively orange."
    ma "That is a color with an ADVERB. I asked for a verdict."
    mc "What flavor is it supposed to be?"
    ma "It doesn't say."
    mc "It doesn't say?"
    ma "It says ORIGINAL."
    mc "Original what?"
    ma "That is the mystery, and I'd thank you not to solve it."

    "She has a swallow of hers and does the face people do when they've decided in advance that they like something."

    mc "It tastes like a candy shop that also does plumbing."
    ma "YES."
    "The volume turns a couple of heads down by the stairwell and she does not adjust for them."
    ma "Yes. Thank you. Six weeks I have been trying to land that."
    mc "Six weeks?"
    ma "I have a notebook."
    mc "You have a notebook for the orange one."
    ma "I have a notebook for several things, and the orange one has a page."
    ma "Out of ten."
    mc "No."
    ma "Why not?"
    mc "Because you'd write it down."
    ma "Obviously I'd write it down. That is what the page is FOR."
    mc "Then no."

    "She points the can at me like she's about to make a ruling, and doesn't, and drinks instead."
    "There's a stretch of about a minute where neither of us says anything and it doesn't turn into work. That's newer than I'd like to admit."

    "Then I see him coming."
    "There is a specific walk. I have never done it and I would not know how, but it's obvious from the other end of a corridor: too much purpose for a hallway, both hands empty, eyes fixed on a point that turns out to be a person."
    "He's a third-year. I've seen him around the science wing. Three of his friends have stopped at the stairwell and are looking at a phone that none of them are holding."

    show matsuda uniform neut
    show daichi neut at t22
    "He gets to us and stops about four feet out. It's the right distance, and I notice him getting it right."

    dai "Hey. Matsuda, right?"
    ma "Correct on the first attempt. A promising start."
    dai "I'm Daichi. Third year, class four."
    ma "Daichi of the fourth. Noted."

    "He has clearly rehearsed the next part and he clearly knows that we can tell, and he does it anyway, which takes something."

    dai "So there's a place by the station that does the imported stuff. The soda. The, uh--"
    "He nods at the can in her hand."
    dai "--that."
    dai "They've got a whole wall of it. Like forty kinds."
    ma "Forty."
    dai "About forty."
    dai "I thought maybe Saturday. If you're free."
    "Somebody two doors down laughs at something else entirely and it lands in the wrong place."
    dai "And--look, I'll just say it. I've seen you do the thing in the hall. The voice, the whole bit."
    dai "You should be on TV."

    "Matsuda takes the can away from her mouth."
    "She does not put it back."

    ma "..."
    ma "Say the last part again."
    dai "...Which part?"
    ma "The television part."
    dai "I said you should be on TV."
    ma "Mm."

    "She sets the can down on the windowsill. Squares it up against the frame. Turns it so the label faces the corridor, which nobody asked her to do."

    show matsuda uniform neut at fx_lean_in, i21
    ma "HOLD."

    "It goes the length of the hall and comes back."
    "The corridor does not stop, exactly. It slows to about a third and gets very interested in the middle distance."

    ma "Hold, and attend, and let it be entered into the record that a man has come before me in the lunch hour and made a REQUEST."
    dai "You don't have to--"
    ma "I do, though. I truly do."
    ma "Because if I say it small, sir, you'll ask me again on Thursday, and then I have to say it twice, and I am a busy woman."

    "Three or four people laugh. One of them is at the stairwell."

    ma "ITEM ONE. You prepared. You picked a day and you picked a place and you waited for a gap in a conversation instead of walking through one, and you did not do it in front of a teacher."
    ma "That is competence and it is going in the record in your favor."
    "The back of his neck has gone red. He is holding very still."
    ma "ITEM TWO. You have watched me. Not creepily -- sit DOWN, all of you -- attentively."
    ma "You know I do a voice. You know I do a bit. You have seen the act, and you have come here to book the act."
    dai "That's not what--"
    ma "ITEM THREE."
    ma "You do not want to take me to a shop by the station on Saturday."
    ma "You want to take me to bed, and you have selected an extremely long route."

    "The corridor makes a noise."
    "It's the noise a room makes when it has decided, all together, that it is not going to be able to un-hear something."

    ma "That is not a slight upon your character! That is arithmetic. You are eighteen, and I look like this."
    "She indicates herself, top to bottom, with the flat of one gloved hand, the way you'd present a car at a show."
    ma "I am fully aware of what I have. I have taken inventory. I do it in a mirror every morning and it takes a WHILE."
    ma "So let us not pretend the wall of soda is the load-bearing element here."

    dai "..."
    ma "And now the part that ruins it, which is the part I am actually here to say."
    ma "You'd have had a magnificent Saturday. I would have been ON. Four hours, no dead air, and you would have told people."
    "She tips two fingers toward the stairwell without looking at it."
    ma "You'd have told THEM by Sunday lunch."
    ma "And somewhere in the second hour you'd start waiting for the girl from the advertisement to arrive."
    ma "She's not running late, Daichi of the fourth. There's a woman who talks like this at a soda can and then goes home and puts the gloves in a drawer."

    "And then the volume goes."
    "All of it, at once, like something got unplugged at the wall."

    show matsuda uniform neut
    ma "No."
    ma "But thank you for saying it to my face instead of putting it in my locker. That's rarer than you'd think."

    "Daichi takes about a second and a half with that."

    dai "...Okay."
    dai "Yeah. No, that's fair."
    "He nods roughly four more times than the sentence requires."
    dai "Sorry about the--yeah."
    ma "Do not apologize for asking."
    ma "Apologize for the phrasing if you must. Never for the asking."
    dai "Right. Okay."

    "He gets his bag strap onto his shoulder on the second attempt."

    dai "For what it's worth, the TV thing wasn't a line."
    dai "I'd have said it anyway."

    "Matsuda opens her mouth."
    "Nothing comes out of it."
    "I have known this woman for eighteen days and I have not once seen that happen."

    dai "Okay. Cool."
    dai "See you around."
    show daichi at thide
    hide daichi

    "He goes."
    "Not fast. He does the entire length of that corridor at a completely ordinary speed with his shoulders exactly where a person's shoulders go, and it is the most work I have ever watched anybody do."
    "At the stairwell one of the three says something to him. I don't hear it."
    "He laughs."
    "It's a good laugh. It carries. He has been building it since he turned around."
    "They go down the stairs together and the hall closes over the place where he was standing."

    show matsuda uniform neut
    "Somewhere in the middle of all that I realized I had been holding my drink up at chest height for about a minute, ready to say something."
    "And that nothing in the corridor was waiting for me to."
    "So I drank it instead."

    menu:
        "\"You didn't have to do it like that.\"":
            $ s1_pick("ooc0604_after_the_ask", "challenge")
            mc "You didn't have to do it like that."
            ma "I did not."
            mc "He was being decent about it."
            ma "He was."
            "She doesn't argue past it. Somehow that's worse than if she had."
        "(Ask if that happens a lot.)":
            $ s1_pick("ooc0604_after_the_ask", "curious")
            mc "Does that happen a lot?"
            ma "Define a lot."
            mc "I feel like you've just answered it."
            ma "I feel like I have."
        "(Leave it alone.)":
            $ s1_pick("ooc0604_after_the_ask", "leave")
            "I don't say anything."
            "The hall goes back to being a hall around us, one conversation at a time."
            ma "You're allowed to ask."
            mc "I know."
            ma "You're not going to."
            mc "No."

    "She looks at the sill for a while. The can is still where she put it, label out."

    ma "..."
    ma "If I say it small, they ask again on Thursday."

    "That's all of it. Same sentence as before, minus everything that was holding it up."
    "Then she has it back on before I've finished registering that it was off."

    ma "ANYWAY! Fourth period approaches, and it approaches with GEOGRAPHY."
    mc "It's Wednesday. You have language arts."
    ma "It approaches with LANGUAGE ARTS, which is worse, because I will be asked to have opinions in complete sentences."

    "She does not pick the can up."
    "She talks at it for four more minutes -- something about a coastline, something about a man at the station who folds the newspapers wrong -- and it sits there on the sill going flat, and she does not pick it up."

    # SFX SUGGESTION: A single warning bell down a long corridor, half a period early.
    "The warning bell goes and the hall starts emptying itself toward the stairs."

    ma "Right. Up. Away. Go be tall somewhere else, [player]."
    mc "Matsuda."
    ma "Mm?"
    mc "Seven."
    "She stops."
    ma "...Seven."
    mc "Seven."
    ma "People say eight. To be nice."
    mc "I know."
    ma "..."
    ma "Seven's better."

    "She picks the can up off the sill, and she drinks the rest of it standing there in a hallway that has almost finished leaving."

    show matsuda at thide
    hide matsuda
    "Then she's gone toward the stairs with the empty in one hand, looking for a bin and telling somebody about the coastline on her way past."
    "I get about four steps down the corridor before I realize I never asked what the flavor was supposed to be."

    $ hide_calendar()
    scene black with dissolve_scene_full
    pause 2.0
    return
