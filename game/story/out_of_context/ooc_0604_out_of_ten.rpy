# Wednesday, June 4, lunch. Unwired future main-story draft.
# Revised 2026-09-05 after reading the current May introduction sequence.
#
# Scene contracts: MC and Matsuda share their corridor lunch spot; the orange
# drink recalls his May 15 bottle cap. Daichi asks Matsuda out, and she declines
# without consulting MC or turning him into a romantic rival. Her public
# overreach remains hers: neither Daichi nor the narrator validates claims she
# cannot know about his motives. His awkwardness does not revoke his dignity.
#
# The television compliment stops her drinking. Keep its significance private;
# no biography, explanation, or premature meta disclosure belongs here. The
# repeated Thursday line changes in delivery when the audience is gone. She
# resumes drinking after MC finally rates the soda seven out of ten.
#
# Both menus change MC's stance only. Keep the single school_day_a cue, the
# isolated return, and the absence of other cast entrances. These are staging
# and continuity notes, not sentence-length or repetition quotas.

label ooc_0604_out_of_ten:

    scene black
    stop music
    pause 1.5
    scene bg corridor
    $ atmos("afternoon")
    with dissolve_scene_full
    play music school_day_a
    $ show_calendar()

    # SFX SUGGESTION: A corridor at lunch -- distant doors, shoes on hard floor,
    # two hundred conversations with none of the words in any of them.
    "The west corridor is loud at lunch, but people mostly pass through on their way somewhere else. If I stand beside the radiator, I can eat without having to move for them."
    "The windows get sun until fifth period, and there's a ledge wide enough for a drink. It took a few lunches to find the spot where I could lean without catching my bag on a valve."
    "Last week Matsuda found me here. Today, I leave my bag by my feet so she'll have somewhere to put hers."

    show matsuda uniform neut at t11
    ma "--and I said to him, sir, that is not a queue, that is a CLOT."
    mc "Hey."
    ma "Hello. Hold this."

    "She puts one of her two cans into my free hand while she gets her bag off her shoulder."
    "I recognize the orange logo from the bottle cap I found last month. The can is just as bright, with ORIGINAL printed across a silver band."

    menu:
        "\"This is my spot, you know.\"":
            $ s1_pick("ooc0604_wall_spot", "claim")
            mc "You know this is my spot."
            ma "It has excellent light and no chairs. I understand the appeal completely."
            mc "That's not what I said."
            ma "It's what you'll mean by Friday."
        "(Move over.)":
            $ s1_pick("ooc0604_wall_spot", "room")
            "I shift along the wall so she can stand clear of the valve. She puts her bag beside mine."
            ma "Thank you."
        "\"How did you even find me?\"":
            $ s1_pick("ooc0604_wall_spot", "ask")
            mc "How did you find me the first time?"
            ma "You're tall and you eat standing up by a window. I could see you from the stairs, lad."

    ma "Go on. I've brought enough for an independent verdict."
    mc "Where'd you find it? The machine by my stop is always sold out."
    ma "I have a supplier. A specialist."
    mc "A shop?"
    ma "An excellent shop. Drink."

    "I take a sip and pull the can away before the fizz gets up my nose. Whatever I expected the orange to mean, it wasn't this."

    show matsuda uniform curious
    ma "Well? Out of ten."
    mc "Give me a second. I still can't work out what flavor it's supposed to be."
    ma "Original, as the label so helpfully informs you."
    mc "Original what? It starts like bubblegum, then there's something else."
    ma "The manufacturer guards that mystery with its life. Or I failed to read the website."

    "She takes a swallow of hers, pressing her lips together while the fizz settles. I try another mouthful."

    mc "It tastes like a candy shop that also does plumbing."
    show matsuda uniform happy
    ma "YES! The pipes! That's what's been missing from every description!"
    "A couple of people near the stairwell look over as she fishes a notebook out of her bag."
    mc "You brought notes?"
    ma "I keep a page for it. Tsubaki wrote 'orange' and refused to elaborate."
    mc "I'd have accepted that as a complete review."
    ma "You see my difficulty. Give me a number, at least."
    mc "No, because you'll write it down before I've finished the can."
    show matsuda uniform smug
    ma "An interim score, then. I permit revisions."
    mc "I know how interim scores work. You frame them and call them promises."

    "She writes down the candy shop and plumbing while I unwrap the second half of my lunch. When I need a napkin, she passes one from her bag without looking up."

    "A boy from the science wing looks toward us from the stairwell, says something to the three people with him, and comes over."
    "I think he's in our year. He slows when Matsuda starts to speak, then waits for her to finish reading Tsubaki's review aloud."

    show matsuda uniform neut at t21
    show daichi neut at t22
    "He stops clear of the radiator and shifts his bag strap before saying anything."

    dai "Hey. Matsuda, right?"
    ma "Correct on the first attempt. A promising start."
    dai "I'm Daichi. Third year, class four."
    ma "Daichi of the fourth. Noted."

    "He glances at the can in her hand, then starts again when two passing students force him closer to the wall."

    dai "There's a place by the station with a whole wall of imported drinks. They've got the one you're having, and--"
    "He nods at the can in her hand."
    dai "Well, about forty others."
    ma "Forty."
    dai "About forty."
    dai "I wondered if you'd want to go with me Saturday, if you're free."
    "Someone two doors down laughs, and he looks over before returning to her."
    dai "I see you around sometimes. You're funny, and I wanted to ask you properly."
    dai "You should be on TV."

    "Matsuda lowers the can from her mouth, keeping it level in her hand."

    ma "..."
    ma "Say the last part again."
    dai "...Which part?"
    ma "The television part."
    dai "I said you should be on TV."
    ma "Mm."

    "She puts the can on the windowsill and turns the label toward the corridor, using both hands to set it against the frame."

    show matsuda uniform neut at fx_lean_in, i21
    ma "HOLD."

    "Two students behind him stop talking, and one of the boys at the stairwell turns around."

    ma "Hold, and attend, and let it be entered into the record that a man has come before me in the lunch hour and made a REQUEST."
    dai "You don't have to--"
    ma "I do, though. I truly do."
    ma "Because if I say it small, they ask again on Thursday, and then I have to do it twice!"

    "Three or four people laugh. One of them is at the stairwell."

    show matsuda uniform determined
    ma "First, credit where it's due: you picked a day and a place, and you came over yourself. Several of your predecessors could not manage that!"
    ma "Second, you have seen me perform in a hallway, which is an extremely misleading brochure for a Saturday afternoon."
    "His neck reddens above his collar while she counts the points on her fingers."
    dai "I'm asking you on a date. I don't need you to do a show."
    show matsuda uniform smug
    ma "Quite! A date. Let us put the soda aside and acknowledge that I am hot enough to make a man develop an interest in imported beverages!"
    dai "I already like the drinks."
    ma "Then we share a taste for questionable flavorings! It remains a poor basis for putting me in your bed."

    "Somebody by the stairwell laughs. Daichi looks toward the sound, then back at her."

    dai "That's not what I asked."
    "She still has one hand raised to continue the list. He waits until she lowers it."
    dai "You can say no. I wasn't going to argue."

    dai "..."
    show matsuda uniform unamused
    ma "Then no, Daichi. I don't want to go on a date."
    "Her gloved hand catches against the seam of her skirt when she brings it down."
    ma "And yes, I could have started there."

    "The last sentence barely reaches beyond the three of us."

    show matsuda uniform neut
    ma "Thank you for asking me yourself. I do mean that part."

    "Daichi looks down the corridor while a group passes between us and the stairs."

    dai "...Okay."
    dai "Thanks for telling me. I could've done without the rest."
    "He shifts his bag strap again, pulling it clear of his collar."
    dai "I'll leave you to your lunch."
    ma "For what it's worth, the rest wasn't all about you."
    dai "I don't really know what to do with that."

    "She looks at him without answering, and he turns toward the stairs."

    dai "The TV thing wasn't a line. I'd have said it anyway."

    "Matsuda opens her mouth as if to call him back, then closes it. I've known her eighteen days, and I'm still waiting when he says goodbye."

    dai "Right. See you around."
    show daichi at thide
    hide daichi

    "He walks back to the stairs without looking around. One of his friends speaks as he gets there, too quietly for me to hear."
    "Daichi laughs once and keeps walking. The others follow him down, leaving a gap that fills with people coming the other way."

    show matsuda uniform neut
    "I've been holding my drink near my mouth without taking a sip. I lower it and wipe the condensation off my hand."

    menu:
        "\"You didn't have to do it like that.\"":
            $ s1_pick("ooc0604_after_the_ask", "challenge")
            mc "You didn't have to do it like that."
            ma "No. I didn't."
            mc "He gave you room to answer. You could've let him finish."
            ma "I know. I heard him."
            "She pushes her notebook farther along the sill, away from the wet ring under her drink."
        "(Ask if that happens a lot.)":
            $ s1_pick("ooc0604_after_the_ask", "curious")
            mc "Does that happen a lot?"
            ma "Enough that I have stopped finding new ways to answer."
            mc "He seemed pretty surprised by that one."
            ma "Yes. He did."
        "(Leave it alone.)":
            $ s1_pick("ooc0604_after_the_ask", "leave")
            "I finish the last of my lunch while the passing conversations fill the space where Daichi stood."
            ma "You're allowed to ask."
            mc "I know."
            ma "You're not going to."
            mc "No."

    "She watches a bead of water move down the can, which is still on the sill with its label facing out."

    ma "..."
    ma "If I say it small, they ask again on Thursday."

    "I can barely hear her over the students passing behind us. She picks at her notebook, and I check the time instead of trying to guess what I'm supposed to say."

    show matsuda uniform determined
    ma "ANYWAY! The afternoon approaches with murderous intent, and I have neglected to finish my lunch!"
    mc "You've got a few minutes. Your bag's by your feet."
    ma "Excellent intelligence. I shall make use of it immediately."

    "She unwraps the rest of her sandwich and tells me about a man at the station who kept opening his newspaper across her seat. The story takes most of the time we have left."
    "I finish my drink while she demonstrates the newspaper with both hands, holding the sandwich between two fingers. Her can stays on the sill."

    # SFX SUGGESTION: The end-of-lunch warning bell down the corridor.
    "The warning bell goes and the hall starts emptying itself toward the stairs."

    ma "Right. Up. Away. Go be tall somewhere else, [player]."
    mc "Matsuda."
    ma "Mm?"
    mc "Seven."
    "She stops with her bag halfway onto her shoulder."
    ma "...Seven."
    mc "For the drink. I'd buy it again, but I'd want something salty with it."
    ma "People usually say eight when I give them one."
    mc "Then stop asking people while you're watching them take the first sip."
    ma "..."
    show matsuda uniform teasing
    ma "Seven, pending snacks. I can work with that."

    "She adds 'snacks required' to the notebook, then picks up her drink while I put my lunch wrapper away. By the time she finishes the can, most of the corridor has emptied."

    show matsuda at thide
    hide matsuda
    "She heads toward the stairs with the empty can in one hand, calling to someone to hold the door. I collect my bag and check the radiator ledge for anything we've left."
    "Her notebook has a fresh line beneath Tsubaki's review: 'Candy shop. Plumbing. Snacks required.' I catch up to return it before she reaches the stairs."

    $ hide_calendar()
    scene black with dissolve_scene_full
    pause 2.0
    return
