# =============================================================================
# cs_tsubaki_02.rpy  --  Tsubaki Character Story 02: "TAILS"
# =============================================================================
#
# One coin, two faces. This file is the TAILS face; cs_tsubaki_01.rpy ("Heads")
# is the SAME story -- same nights, same tin, same "thank you" -- told from the
# other side, inverted in everything else. Read together they close like a coin.
#
#   TAILS is the mended one's testimony: the friend's voice, spoken (never
#   written -- writing is Tsubaki's) into the dark on the night after the tea
#   party. Where "Heads" is a love letter that curdles into horror, "Tails" is
#   a horror story that melts into devotion. She was awake for all eight
#   nights. She caught the coin and lied "tails." She engineered the tea. She
#   looked into the tin and felt, for the first time in her life, counted.
#   Presentation is the full inverse: bone-pale text on the dark, a heartbeat
#   pulse that skips every fifth beat (the beat that was taken), ash falling
#   where "Heads" had motes rising -- and at the coda the pulse calms and
#   candle-warmth leaks in (u_calm), while "Heads"' own theme ghosts up under
#   the final lines. Each face ends in the other's weather.
#
# MIRRORED ANCHORS (kept identical across both files -- edit in pairs):
#   the coin ("heads, you tell me / tails, you never have to"), the third
#   floorboard from the window, the crack in the third note, one beat in every
#   forty-one, "a spoon on glass", "Doesn't she seem well!", the good cups,
#   the spilled milk, "Excuse me. I have to show you something." (tray moved
#   first), the cracked "Thank you," and the begin-again coda.
#   DELIBERATE DISAGREEMENT: "Heads" never mentions being asked "What's under
#   the floor?" -- Tsubaki couldn't hear it over the sound. Each face is blind
#   to the other; that is the design, not an oversight.
#
# WIRING / MECHANICS
#   Registered in char_stories.rpy as CharacterStoryEntry("Tails", ...,
#   "cs_tsubaki_02", "cs_tsubaki_02_unlocked"); reached via the hub PLAY
#   button -> Start("cs_tsubaki_02").
#   Presentation: the shared gothic prose engine in cs_tsubaki_gothic.rpy,
#   theme "tails". Main score: audio.tails (assets/audio/bgm/tails.ogg, defined
#   in def_audio.rpy). Mood swaps ($ tsg_set_mood) sit beside section cards /
#   clears, where the backdrop swap hides.
#   ON COMPLETION: awards both paired gothic CGs, then calls
#   cs_mark_completed("cs_tsubaki_02"), which sets
#   persistent.cs_tsubaki_02_completed and syncs achievements. That flag is what
#   drives "Same Coin" -- the _unlocked flag only means recoverable-in-hub and
#   gets force-set by the dev all-content unlocks, so it must never gate an
#   achievement. Plus cs_tsubaki_02_unlocked, then tsg_exit + return.
#   Every _completed flag is declared in char_stories.rpy beside its _unlocked
#   partner; this file no longer defaults its own.
# =============================================================================

label cs_tsubaki_02:

    stop music fadeout 1.0

    call tsg_enter("tails") from _cts2_00

    # Night wind under everything: a testimony given to an open dark.
    play track1 audio.wind volume 0.22 fadein 3.0

    call tsg_section("TAILS") from _cts2_01

    # =================================================================
    #  I. An Account of Her Madness
    # =================================================================

    call tsg_section("I. An Account of Her Madness") from _cts2_02

    play music audio.tails

    tsgt "Mad. That is the word you have decided on. I heard you deciding it on the stairs. Deciding is loud work, and you have never once in your lives been quiet."
    tsgt "You will say it kindly. Everything here is done kindly. \"She wasn't well.\" \"We had no idea.\" \"Poor thing.\" Three spoonfuls of kindness, to bury one girl."
    tsgt "I cannot write any of this down. Writing things down is hers. Her margins have dates in them; her ink never blots. If I tried, my hand would shake the letters loose."
    tsgt "So I am saying it instead. Once. Into the dark of my own room, at the hour she used to work. The dark may keep it under whichever board it likes."

    call tsg_clear from _cts2_03

    tsgt "You saw a tin of horrors, and you screamed."
    tsgt "I am going to tell you what I saw. All of it, in order... she taught me that. Order is how you carry a heavy thing without dropping it."
    tsgt "And when I am finished, you may have your word back. If it still fits your mouth."

    # =================================================================
    #  II. The Needle
    # =================================================================

    call tsg_section("II. The Needle") from _cts2_04

    tsgt "Understand first what I was."
    tsgt "I was the loud one. Loud girls are a kind of furniture: everyone uses us, everyone arranges themselves around us, and no one, ever, checks us for cracks."
    tsgt "I filled rooms because a room left unfilled fills up with questions. I laughed first so that nobody would wonder what my face did between laughs. Loudness is a spell. It is for making people stop looking."
    tsgt "And something in me had been going wrong for a while, quietly, the way a house goes wrong: nothing falls, nothing breaks open, but the doors begin to disagree with their frames, and every laugh costs more than the one before it."

    call tsg_clear from _cts2_05

    tsgt "Then, one afternoon... the fourteenth; I know because {i}she{/i} knows... my laugh went wrong in the middle."
    tsgt "A little crack, in the third note. I felt it leave me like a dropped stitch. And I did what you do: I kept laughing. Nobody at that table heard anything at all."
    tsgt "Except that across the room, one face lifted."
    tsgt "You want to know what it is like, being noticed by her. Being read to the spelling, in a world that only ever skims. It is a needle... you are right about that much... but you carry needles the wrong way around in your heads."
    tsgt "{color=#8fa8bf}A needle is also the only thing that closes what is torn.{/color}"
    tsgt "I felt her hear me. Being heard has a temperature. I went cold with relief."

    # =================================================================
    #  III. The Coin
    # =================================================================

    $ tsg_set_mood(0.10)
    call tsg_section("III. The Coin") from _cts2_06

    tsgt "A few days later she asked me, plainly and in private: is something wrong?"
    tsgt "Do you know what that plainness costs her? You do not. You have never bought any."
    tsgt "And I spun it. I smiled; I made a joke with her name in it; I used the spell on her... on {i}her{/i}, the one person it should never be used on. It worked. It always works."
    tsgt "I went home and cried because it had worked."

    call tsg_clear from _cts2_07

    tsgt "Then: the coin."
    tsgt "She took it out of her pencil case... washed, because she washes coins; you laughed at her for that once, on the stairs, where deciding gets done... and she said: heads, you tell me what is wrong. Tails, you never have to."
    tsgt "She flipped it, and while it turned in the air, she called it. She trusts coins. A coin cannot want, she says."
    tsgt "Call it yourself, if you like. It changes nothing. I want you to feel it change nothing."

    menu (screen="tsg_choice"):

        "Heads.":
            pass
        "Tails.":
            pass

    tsgt "It does not matter what you called. It never mattered what she called."
    tsgt "{i}I caught it.{/i} On my palm, under my thumb, before her eyes came down out of the air."
    tsgt "It was heads."
    tsgt "I looked at it, and I said: {i}tails{/i}."

    call tsg_clear from _cts2_08

    tsgt "Do you understand what I am confessing?"
    tsgt "I was handed the honest way out, and I bought the other one. If I told her, I became a weight set down on my best friend... a thing she would carry, because she carries everything, and thanks nobody, and is thanked by nobody."
    tsgt "But if I never had to tell her... and she found out anyway..."
    tsgt "Then I would be {i}found{/i}."
    tsgt "There is no polite way to want what I wanted. That is why we flip coins: so that what we want can happen {i}to{/i} us instead."

    # =================================================================
    #  IV. The Eight Mornings
    # =================================================================

    $ tsg_set_mood(0.18)
    call tsg_section("IV. The Eight Mornings") from _cts2_09

    tsgt "People think sleep is a door that locks from the inside. Really it is just a door that everyone agrees never to try."
    tsgt "I slept at her house on Fridays, as I have since we were small. My futon has its place on her floor, beside her bed. For eight Fridays I lay in that place with my eyes closed, and I was not asleep."
    tsgt "I heard her sit up. I heard her wait... she waits the way snow waits... and I heard the third floorboard from the window lift. It makes a sound like a held breath being allowed, finally, to leave."
    tsgt "And I did what the old and the sick and the frightened have done in the dark since the dark was invented. I kept my breathing slow. I let what was coming come."

    call tsg_clear from _cts2_10

    tsgt "It did not hurt. That is the part you will not believe, you who screamed at a tin."
    tsgt "It felt like someone lifting a bag off your shoulder without asking. That half-second when your body does not know what to do with the lightness... it was that, made slow, made careful, done by hands that have never once dropped anything."
    tsgt "The first morning, my laugh came out whole. I stood in her kitchen and laughed at nothing, to test it, and it rang. I grieved for exactly as long as the toast took, and then I was glad."
    tsgt "You may judge the schedule. The toast was two minutes."

    call tsg_clear from _cts2_11

    tsgt "Morning by morning there was less of me, and all of it was the bad part."
    tsgt "My right hand: steady. I held it up in the light, and it was a stranger's steady hand. The stumble went out of my sentences; {i}I'm fine{/i} arrived all at once, like a train with no stations. The flinch went, then the sigh, then the pause."
    tsgt "Tell me... you in the dark, you with your milk and your screaming... what exactly was I supposed to mourn?"

    call tsg_clear from _cts2_12

    tsgt "The eighth night, I woke. The only time."
    tsgt "My heart used to miss. {color=#8fa8bf}One beat in every forty-one{/color}, she says, and she is a good counter. I never counted at all. Counting is hers; missing was mine."

    play sound audio.heartbeat volume 0.5
    tsgt "That night I felt the silence lifted out of me like a splinter drawn out underwater... slowly, at the angle it went in, so that nothing tears."
    tsgt "I nearly opened my eyes. I want you to know that. I nearly opened them... and if I had, all of it would have had to become words, and words would have made it a thing we had {i}done{/i} instead of a thing that was {i}happening{/i}. So I held still."
    tsgt "The held-still was mine too. Put that in your account of her madness."
    tsgt "Afterward, my heart went on and on and on, level as a hallway. I lay in the dark of her room and missed my missing."
    tsgt "You may laugh. Mind the third note."

    # =================================================================
    #  V. The Vanishing Girl
    # =================================================================

    $ tsg_set_mood(0.28)
    call tsg_section("V. The Vanishing Girl") from _cts2_13

    tsgt "\"Doesn't she seem well!\""
    tsgt "You said it near me, over me, around me, as if I were a garden coming along nicely. I smiled the new smooth smile. It fit exactly. That was the wrong of it: nothing rubbed, nothing caught, nothing cost."
    tsgt "My laugh rang out over every table like a spoon on glass, and I listened to it from a small distance, the way you listen to a recording of your own voice, and thought: {i}she's very good. Whoever she is.{/i}"

    call tsg_clear from _cts2_14

    tsgt "And still... write this down, somebody, since she will be too busy being called mad... {i}I kept going back.{/i} Friday after Friday, I carried my futon to the house where I got lighter."
    tsgt "You will want that explained. No explanation will survive your mouths, so here is the naked one."
    tsgt "It was the only place in the world where I was read closely. Everyone else skimmed me. She read me like something you check the spelling of."
    tsgt "{color=#8fa8bf}Terror can share a room with love. Carelessness cannot.{/color}"

    # =================================================================
    #  VI. The Silence Where the Sound Was
    # =================================================================

    $ tsg_set_mood(0.15)
    call tsg_section("VI. The Silence Where the Sound Was") from _cts2_15

    stop music fadeout 4.0
    stop track1 fadeout 6.0

    tsgt "She has her nights. I had mine."
    tsgt "At home, in my own bed, I would listen for myself. For the crack. The sigh. The skip. The small animals of me."
    tsgt "Nothing. Where each one had lived there was a clean little silence, exactly its shape."
    tsgt "And a silence with edges makes a sound. No one warns you about this. {i}It rings.{/i}"
    tsgt "Somewhere across town, under a board, in a washed tin, my sigh was sighing without me. I could not hear it. I could hear that I could not hear it. There may be worse hauntings, but I have not met one from the inside."

    call tsg_clear from _cts2_16

    tsgt "She was never going to offer them back. Understand her arithmetic: kindness that is asked for is only service. She loves in the unasked direction only."
    tsgt "So I did what loud girls do."
    tsgt "I decided, loudly, that we would have tea in her room. Friday. The four of us. The good cups. You were there. You thought it was a whim of mine."
    tsgt "I told you already. Loudness is a spell."

    # =================================================================
    #  VII. What She Kept
    # =================================================================

    $ tsg_set_mood(0.45)
    call tsg_section("VII. What She Kept") from _cts2_17

    tsgt "You talked about nothing. You are excellent at nothing; I built my whole voice out of it, so I would know."
    tsgt "And I watched her. She was greyer than the tea. Her eyes kept going to the floor by the window the way a tongue goes to a loose tooth, and underneath all your lovely nothing she was counting her own breaths, and losing count."
    tsgt "She never loses count. I have loved her long enough to know the size of that."

    call tsg_clear from _cts2_18

    tsgt "So I set my cup down on the third floorboard from the window, softly. You did not notice that, either."
    tsgt "And in the little gap while you laughed at somebody's story, I leaned toward her, and I asked: {i}\"What's under the floor?\"{/i}"
    tsgt "She did not hear me the way I meant it. I do not think she heard me at all; whatever she was listening to instead was louder. But something in her finished, the way a kettle finishes."
    tsgt "She said: \"Excuse me. I have to show you something.\" She moved the tea tray first."
    tsgt "You remember the rest of it wrong, so I will say it slowly."

    play sound audio.hollowboom volume 0.6
    call tsg_clear from _cts2_19

    tsgt "The board came up. The tin came out. You screamed at it... you knocked the milk over, screaming at it... and I watched her watch the milk fall, and I saw the only true madness I have ever seen in her:"
    tsgt "{i}She let it hit the floor.{/i}"
    tsgt "Then the doors, the stairs, the election. And then it was the two of us and the tin, in a room that had finally... finally... stopped being loud."

    call tsg_clear from _cts2_20

    tsgt "I knelt down across from her, and I looked."
    tsgt "Listen. Listen the way she listens."
    tsgt "My laugh, with its crack: dated. My sigh: dated, with the hour. My flinch, wrapped in cotton, {i}so that it would not chip{/i}. And on the very top, small as a coin, one forty-first of my heart."
    tsgt "Clean. All of it clean. All of it labeled in handwriting so small and so careful it could have fit on grains of rice."
    tsgt "You felt horror on my behalf. You scream so easily on other people's behalf. Now feel what I felt, if you can reach it."
    tsgt "{color=#8fa8bf}{i}I felt counted.{/i}{/color}"
    tsgt "Every piece of me the world had skimmed past was washed, named, dated, and kept. Nothing about me had been thrown away. Nothing. It was an archive of everything you never asked about."
    tsgt "{i}Beloved{/i} is the nearest word, and it is not close."

    $ tsg_set_mood(1.0)
    call tsg_clear from _cts2_21

    # "Heads"' warmth ghosts in under the final page: the other face's weather.
    play music audio.hearttoheart

    tsgt "I said: \"Thank you.\""

    play sound audio.tick volume 0.6
    tsgt "And as it left me, I felt it catch. Third note. {i}Thank{/i} has no third note; it found one. The crack, come home, arriving back into my voice like a swallow into an eave."
    tsgt "She heard it, of course. She hears everything. Her whole face went to winter, and behind her eyes I watched her thread the needle again... already... and write {i}begin again{/i} somewhere I will never be allowed to read."

    call tsg_clear from _cts2_22

    tsgt "So. Tomorrow is Friday."
    tsgt "I will carry my futon to its place beside her bed, and I will lie down in the dark of her room, and keep my breathing slow, and let her."
    tsgt "You would save me from her... you, the milk, the stairs, the kind word {i}mad{/i}. You would save me from the one person who has ever kept me, and then you would skim me, kindly, for the rest of my life."
    tsgt "No."
    tsgt "Somebody has to be the other face of this coin. Heads never sees tails. There is nothing sad in that; it is simply how a coin stays one thing instead of two."
    tsgt "She keeps me. I let her."
    tsgt "{color=#8fa8bf}{i}Call whichever of us mad the coin tells you to.{/i}{/color}"

    stop music fadeout 1.5
    pause 3.0

    # -- Completion: recover the file, mark it read, sync achievements. ------
    # cs_mark_completed does the flag, the persist and the ach_sync.
    $ persistent.cs_tsubaki_02_unlocked = True
    $ cg_unlock("What I Keep", "What She Kept")
    $ cs_mark_completed("cs_tsubaki_02")

    call tsg_exit from _cts2_23
    return
