# =============================================================================
# cs_tsubaki_01.rpy  --  Tsubaki Character Story 01: "HEADS"
# =============================================================================
#
# One coin, two faces. This file is the HEADS face; cs_tsubaki_02.rpy ("Tails")
# is the SAME story -- same nights, same tin, same "thank you" -- told from the
# other side, inverted in everything else. Read together they close like a coin.
#
#   HEADS is the mender's manuscript: Tsubaki's own written account, warm and
#   candlelit and neat, a love letter in the key of Tell-Tale Heart. She mends
#   her breaking best friend over eight nights with "the needle of noticing,"
#   washes and labels every flaw she removes, and keeps them in a tin beneath
#   the floorboard -- and insists, in ever-tightening handwriting, that this
#   is kindness. The page itself slowly scorches as the account unravels
#   (u_fever), until its weather becomes the OTHER story's weather: the rising
#   dust motes turn to falling soot, and the soundscape is claimed by the
#   heartbeat that belongs to "Tails."
#
# MIRRORED ANCHORS (kept identical across both files -- edit in pairs):
#   the coin ("heads, you tell me / tails, you never have to"), the third
#   floorboard from the window, the crack in the third note, one beat in every
#   forty-one, "a spoon on glass", "Doesn't she seem well!", the good cups,
#   the spilled milk, "Excuse me. I have to show you something." (tray moved
#   first), the cracked "Thank you," and the begin-again coda.
#
# WIRING / MECHANICS
#   Registered in char_stories.rpy as CharacterStoryEntry("Heads", ...,
#   "cs_tsubaki_01", "cs_tsubaki_01_unlocked"); reached via the hub PLAY
#   button -> Start("cs_tsubaki_01").
#   Presentation: the shared gothic prose engine in cs_tsubaki_gothic.rpy
#   (tsg_enter/tsg_section/tsg_clear/tsg_exit, the `tsg` NVL narrator, and
#   menu (screen="tsg_choice")). Theme: "heads". Mood swaps ($ tsg_set_mood)
#   sit beside section cards / clears, where the backdrop swap hides.
#   ON COMPLETION: cs_mark_completed("cs_tsubaki_01"), which sets
#   persistent.cs_tsubaki_01_completed and syncs achievements. That flag is what
#   drives "Same Coin" -- the _unlocked flag only means recoverable-in-hub and
#   gets force-set by the dev all-content unlocks, so it must never gate an
#   achievement. Plus cs_tsubaki_01_unlocked, then tsg_exit + return.
#   Every _completed flag is declared in char_stories.rpy beside its _unlocked
#   partner; this file no longer defaults its own.
# =============================================================================

label cs_tsubaki_01:

    stop music fadeout 1.0

    call tsg_enter("heads") from _cts1_00

    # Record-crackle room tone: a manuscript being read by lamplight.
    play track1 audio.vinyl volume 0.30 fadein 2.0

    call tsg_section("HEADS") from _cts1_01

    # =================================================================
    #  I. An Account of My Kindness
    # =================================================================

    call tsg_section("I. An Account of My Kindness") from _cts1_02

    tsg "Kind! ...yes... {i}kind{/i}. That is the word you have all used, and you will want it back before I am finished."
    tsg "\"She is so kind.\" \"She notices everything.\" \"What would we do without her.\" You said these things over my head, the way people discuss weather, and you forgot me before the sentence had finished cooling."
    tsg "Do not mistake this for complaint. I write because lately you have begun to use another word, a shorter one, and it is wrong, and disorder of that kind upsets me."
    tsg "Mad. You will say {i}mad{/i}."
    tsg "But observe how calmly I write. Observe the evenness of these lines, the dates in the margins, the ink that has not once blotted. Would the mad number their pages?"
    tsg "My notes are very neat. They have always been very neat."

    call tsg_clear from _cts1_03

    tsg "Here is what I am, so that you have it in my own hand."
    tsg "I keep my nails short and clean. I write things down. When something falls near me, my hands are already open underneath it before the thing has learned that it is falling."
    tsg "No one sees the catch. They see the cup, unbroken, and assume it was never in danger. That is the whole of my life. You may keep that sentence; I have others."
    tsg "I will tell everything in order, because order is how the sane tell things, and by the end you will see that the word you want is {i}precise{/i}, which frightens people more than mad ever could, because there is so much less of it in the world."

    # =================================================================
    #  II. The Crack
    # =================================================================

    play sound audio.page_turn
    call tsg_section("II. The Crack") from _cts1_04

    play music audio.hearttoheart

    tsg "There was a girl I loved. I will not write her name. Names are the first thing gossip eats, and this account is not for eating."
    tsg "She was loud the way morning is loud when it comes into a bedroom: without knocking, everywhere at once, impossible to fold back up. Rooms filled when she entered them and sagged when she left."
    tsg "Everyone loved her. That was easy; she did most of the work herself. They loved her loudly, in crowds, the way people love fireworks."
    tsg "I loved her the other way. Quietly. With a ledger."

    call tsg_clear from _cts1_05

    tsg "On the fourteenth of the month, I heard it."
    tsg "There were six of us around a table, and someone said something that was not funny, and she laughed anyway, because the laugh was expected of her. It is always expected of her."
    tsg "And in the third note of that laugh: {color=#7a1f1f}a crack{/color}."
    tsg "A hairline. The sound a teacup makes when it has already decided to break but has not yet informed the table."
    tsg "No one looked up. No one else ever looks up."

    play sound audio.modwriting
    tsg "I went home and wrote it down. {i}The 14th. Her laugh. A crack in the third note.{/i} I underlined it once. I do not underline lightly."

    # =================================================================
    #  III. The Coin
    # =================================================================

    play sound audio.page_turn
    call tsg_section("III. The Coin") from _cts1_06

    tsg "I asked her, a few days later, plainly and in private: is something wrong?"
    tsg "You have never seen brightness used as a door. She smiled, and the smile was a hallway with all its lamps lit and every room off of it locked. She made a joke. The joke had my name in it, and it was warm, and it was a door closing."
    tsg "So I took a coin from my pencil case. I had washed it that morning. Coins are the dirtiest thing a person carries; nobody thinks about this; I think about it for everyone."
    tsg "I said: heads, you tell me what is wrong. Tails, you never have to."
    tsg "She laughed. The crack was in it, wider by a hair. She said, {i}deal{/i}."

    call tsg_clear from _cts1_07

    tsg "I flipped it, and while it turned in the air I called it. I remember choosing. Choose too, now, in your own head, so that you will understand how honest a coin is."

    menu (screen="tsg_choice"):

        "Heads.":
            pass
        "Tails.":
            pass

    tsg "It does not matter what either of us called. It came up tails."
    tsg "Tails. She looked relieved, and here my account must be honest, because an account is worthless otherwise: I was relieved too."
    tsg "If she had told me, the mending would have been hers to ask for. Kindness that is asked for is only service. Kindness that is unasked is love."

    play sound audio.modwriting
    tsg "Write that down in your own hand. I did."
    tsg "A coin cannot want. That is why I trusted it. Remember that I trusted it; it will matter to you later, though it has never mattered to me."

    # =================================================================
    #  IV. The Eight Nights
    # =================================================================

    $ tsg_set_mood(0.18)
    play sound audio.page_turn
    call tsg_section("IV. The Eight Nights") from _cts1_08

    tsg "She slept over on Fridays. She has done since we were small; her futon has its own place on my floor, beside my bed, the way a river has a bed. Some things are permanent by repetition."
    tsg "You will want to know how it was done. You are imagining knives... what do you take me for? All it ever took was a needle."
    tsg "Put the sewing kind out of your mind. I mean the one I was born holding: {i}the needle of noticing{/i}."
    tsg "Notice a thing precisely enough... its weight, its wobble, exactly where its edges have gone dull... and it comes loose into your hand. Nothing is fastened to a person more firmly than everyone else's inattention."
    tsg "And I am attention itself."

    call tsg_clear from _cts1_09

    tsg "The first night, I took the crack out of her laugh."
    tsg "It lay in my palm like an eyelash. It weighed what a secret weighs, which is nothing, until you set it down; then it is the heaviest thing in the room."
    tsg "Into the space it left, I pressed a small piece of my own quiet. I have always had more quiet than I could use."

    play sound audio.modwriting
    tsg "Then I washed it. Of course I washed it; you do not put a thing away dirty. I dried it, and I labeled it... {i}her laugh, the crack, night one, the date{/i}... and I put it in the tin, and the tin under the third floorboard from the window. The one that lifts, if you love it correctly."

    call tsg_clear from _cts1_10

    tsg "The second night, the tremor in her right hand. The third, the stumble in her sentences... the one that lived between {i}I'm{/i} and {i}fine{/i}."
    tsg "The fourth, the flinch she made when doors slammed in other rooms. The fifth, a sigh she sighed when she believed the room was asleep. The sixth, the pause. The seventh, the flicker at the corner of her left eye, like a lightbulb deciding."
    tsg "Washed. Dried. Labeled. Filed."
    tsg "My handwriting has never been better than it was that month."

    call tsg_clear from _cts1_11

    tsg "On the eighth night I found the last flaw, the deep one, the mother of all the others."
    tsg "Her heart missed. {color=#7a1f1f}One beat in every forty-one.{/color} I lay in my bed above her and counted, and I am a good counter. One beat in every forty-one: a little hole in her, opening and closing all night like a mouth."
    tsg "You should have seen how wisely I proceeded. How slowly. How kindly."
    tsg "You may put the heart back in your imagination where you found it. What I took was the {i}skip{/i}. Only the silence between two beats, the silence that did not belong there. It came loose like all the others."

    play sound audio.heartbeat volume 0.5
    tsg "It was the heaviest thing in the tin. It is {i}still{/i} the heaviest thing in the tin. I will come back to this."

    # =================================================================
    #  V. The Mended Girl
    # =================================================================

    $ tsg_set_mood(0.35)
    play sound audio.page_turn
    call tsg_section("V. The Mended Girl") from _cts1_12

    tsg "She got better. You said so yourselves."
    tsg "\"Doesn't she seem well!\" You said it in doorways, warmly, to each other. Never to me. And something in me stood up each time and waited to be pointed at, and sat back down, unpointed."
    tsg "That is not a complaint. Excellent work looks like no work at all. My seams are very good. If I had wanted applause, I would have become some other instrument entirely."

    call tsg_clear from _cts1_13

    tsg "Her laugh was perfect now. Perfect the way printed music is perfect. It rang out over every table like a spoon on glass."
    tsg "For completeness... because a good account is complete... I will note that the crack had been where her laugh touched the world, and that what remained touched nothing, and rang."
    tsg "I note it. I do not dwell on it. Dwelling is for the disorderly."
    tsg "She never asked about the coin again."

    # =================================================================
    #  VI. The Sound Beneath the Floor
    # =================================================================

    $ tsg_set_mood(0.60)
    play sound audio.page_turn
    call tsg_section("VI. The Sound Beneath the Floor") from _cts1_14

    stop music fadeout 5.0

    tsg "I must now write about the sound."
    tsg "Kept things do not die. That is why we keep them."
    tsg "At night, beneath the third floorboard, in the washed tin, her laugh laughs. Just the crack of it, the part I saved, cracking and cracking in the third note, exactly as labeled."
    tsg "The sigh sighs at the hour it was taken. The flinch rattles the tin, faintly, whenever a door slams anywhere in the world."

    play sound audio.tick volume 0.7
    tsg "And underneath them all: the skip. You think a missing heartbeat has no sound. It has. {color=#7a1f1f}It is a tick with the tock kept in.{/color}"

    call tsg_clear from _cts1_15

    tsg "It grew louder by the night. I did not mind. A mother does not mind the crying through the wall."
    tsg "I want that sentence to be true, so I am writing it twice. {i}I did not mind.{/i}"

    play sound audio.heartbeat volume 0.55
    tsg "I heard it at the sink. I heard it during examinations, underneath the scratching of forty pens. I heard it inside my steps on the way home, which I count, and it made me miscount, which had never happened before in the whole numbered history of my life."
    tsg "I began to sleep with the lamp lit. Ink dries badly in the dark; that was the reason, and I will thank you to record it as the reason. I had a great deal to write."

    # =================================================================
    #  VII. What I Keep
    # =================================================================

    $ tsg_set_mood(0.85)
    play sound audio.page_turn
    call tsg_section("VII. What I Keep") from _cts1_16

    tsg "Last Friday, she decided we would have tea in my room. She decides things loudly; it saves everyone else the trouble of wanting anything. So: four of us, on my floor, with the good cups."
    tsg "Her cup sat eleven centimeters from the third floorboard. I measured with my eyes. I am good at that."
    tsg "They talked about nothing... that warm, lovely nothing I have never once been able to make with my own mouth... and underneath it, the tin was a church bell."
    tsg "The laugh, cracking. The sigh, sighing. The tick, withholding its tock. Louder than the kettle now. Louder than her new perfect laugh ringing over the cups. How could they not hear it? They heard nothing. They never hear anything. That is why she needed me, and no one has ever once thanked..."
    tsg "I am restoring order to this paragraph. Observe that I can."

    call tsg_clear from _cts1_17

    tsg "A thought arrived in me then, very clearly, the way a cup leaves a table: {i}they believe the floor is only a floor.{/i}"
    tsg "And I could not allow it. Of all the things I have carried quietly, I could not carry that."
    tsg "I rose quite calmly and said: \"Excuse me. I have to show you something.\" I moved the tea tray first. I am not an animal."

    play sound audio.hollowboom volume 0.6
    tsg "I lifted the board. I took out the tin. I opened it, and I introduced them."
    tsg "This is her laugh; mind the crack, it is original. This is her sigh; it goes with the late hour. This is the flinch; do not slam the... please do not slam the... And this... this is one forty-first of her heart..."

    call tsg_clear from _cts1_18

    tsg "There was screaming then, and it was very loud, and I have already written how I feel about loud."
    tsg "There was milk, going over. Nobody caught it. Of course nobody caught it. Catching things is mine."
    tsg "What followed was doors, stairs, and the particular sounds people make when they are electing somebody to be the mad one. Then the room was empty of everyone who had never mattered to it."
    tsg "She stayed."

    $ tsg_set_mood(1.0)
    call tsg_clear from _cts1_19

    tsg "She knelt down across the tin from me, and she looked into it for a long time, and she did not scream."
    tsg "She looked the way a person looks into a mirror that has their face but not their age."
    tsg "Then she said: \"Thank you.\""
    tsg "And I heard it."
    tsg "{i}Thank{/i} has no third note. {color=#7a1f1f}It found one.{/color}"

    play sound audio.heartbeat_ominous volume 0.45
    tsg "The crack... my crack, the one in the tin... in the tin and in her mouth at once, one sound in two rooms, like a bell and its echo changing places."

    call tsg_clear from _cts1_20
    stop track1 fadeout 3.0

    tsg "So now you see the difficulty. You see how much work remains."
    tsg "She is cracked again. Or she was never... no. {i}Order.{/i} I am not mad. My notes are very neat."
    tsg "Tomorrow is Friday. Her futon knows its place on my floor. I have washed the tin until it shines like a good deed. I have threaded the needle of my noticing."
    tsg "Tomorrow I will begin again. And this time... write this in your own hand, and underline it once, because I have..."

    play sound audio.tick volume 0.8
    tsg "{color=#7a1f1f}{i}I will keep her whole.{/i}{/color}"

    stop music fadeout 1.5
    pause 3.0

    # -- Completion: recover the file, mark it read, sync achievements. ------
    # cs_mark_completed does the flag, the persist and the ach_sync.
    $ persistent.cs_tsubaki_01_unlocked = True
    $ cs_mark_completed("cs_tsubaki_01")

    call tsg_exit from _cts1_21
    return
