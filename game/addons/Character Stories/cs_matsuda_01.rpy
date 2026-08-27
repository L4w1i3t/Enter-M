# =============================================================================
# cs_matsuda_01.rpy  --  Matsuda character story 01, "Dead Fantasy"
# =============================================================================
#
# A Fire Emblem-style war story, staged like a play and played completely
# straight...right up until the camera pulls back and it turns out to be a
# tabletop campaign Matsuda is running for the friend group on a Saturday night.
#
# The battle is earnest ON PURPOSE -- the parody lives in the reveal. The war
# scenes are written plain: tired people, logistics, short sentences. There is
# NO external narrator -- every piece of scene-setting is carried by dialogue,
# staging, music, or SFX (FE-style: show, don't tell). The tells are behavioral,
# not winking, so the living-room turn reads as "it was visible the whole time"
# instead of a cheat:
#   - Gregor talks about himself in the third person (Asahina "in character"),
#     and drops it exactly once -- the moment he breaks.
#   - Gary is slightly over-written and over-prepared (Monika's PC; she wrote
#     him a letter, a mother, a month of counting wagons).
#   - Akai, the commander, is improbably central and never quite dies, and is
#     named after the GM (Matsuda Akai). Her snark bleeds through under stress,
#     and she gets a brooding solo scene nobody else gets.
#   - Akai thinks of her people as "pieces on the table."
#   - The whole thing ends on a draw -- the dice writing a better ending than
#     the author would have.
#
# Table mapping:
#   Matsuda = GM   -> voices Akai (her self-insert commander), Leif, and the
#                     Captain / Scout / Medic bit-NPCs.
#   MC             -> the rival commander.
#   Sam            -> the berserker who holds the west ridge.
#   Tsubaki        -> the cleric.
#   Asahina        -> Gregor. Actually built a character. Plays him third-person.
#   Monika         -> Gary. Actually built a character. Wrote him a backstory.
#                     Has a great night right up until the room gets ugly -- then
#                     she blows the whistle, not to calm anyone down, but because
#                     Tsubaki's one question keeps getting steamrolled.
#
# MUSIC MAP (campaign scored like an SRPG; silence is used as a cue):
#   hotr             -> war council. Fades to silence for Akai's solo beat.
#   fantasypassion   -> the rival's fortress (the mirror council, at night).
#   flight           -> armies maneuvering, pre-contact.
#   epicbattlephase1 -> battle joined, from the arrow storm on.
#   (hard stop)      -> the instant Tsubaki is hit; her death plays dry.
#   hopeless         -> Sam intercepts Akai; his death.
#   devoted          -> the two commanders meet; carries into the duel's parley.
#   epicbattlephase2 -> the duel itself, first clash on.
#   (hard stop)      -> the mutual freeze; the draw is agreed to in silence.
#   enterm           -> THE TABLE reveal. Cut by the interjection sting.
#   roster_place     -> re-enters only when the medic roll lands ("She lives").
#
# WIRING / MECHANICS
#   Registered in char_stories.rpy as CharacterStoryEntry("Dead Fantasy", ...,
#   "cs_matsuda_01", "cs_matsuda_01_unlocked"); reached via Start("cs_matsuda_01").
#
#   CUSTOM DIALOGUE UI (defined just below):
#     screen cs_matsuda_fe_say(who, what)     -> a hand-built FE/SRPG dialogue box
#       (gold border + navy body), drawn from plain Solids instead of `frame`
#       ON PURPOSE: the mod's themed `style frame` injects a Frame background +
#       border padding that shoves text around in a fixed-size box. See the
#       "custom say-UI gotchas" project note.
#     screen cs_matsuda_fe_stage_overlay()    -> letterbox + theatrical side bars
#     The cs_fe_* Characters all route through screen="cs_matsuda_fe_say".
#   Bit-part NPCs (Captain/Scout/Medic) use placeholder sprite images defined here.
#   Sprite placement uses the shared t11/t21/... position transforms (transforms.rpy).
#
#   STRUCTURE: I. war council -> II. rival's fortress -> III. Greywake Field ->
#   IV. the duel (ends in a draw) -> V. THE TABLE, where the overlay is hidden and
#   the "battle" is revealed as Matsuda's tabletop campaign (the cs_fe_* cast snap
#   back to the real characters: ma/sa/ah/ts/m/mc) -- and the table loses its
#   collective mind over the ending until the medic roll lands the plane.
#
#   ON COMPLETION: persistent.cs_matsuda_01_unlocked = True, then return.
# =============================================================================

define cs_fe_akai    = Character("Akai", image="matsuda", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")
define cs_fe_rival   = Character("MC", image="mc", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")
define cs_fe_sam     = Character("Sam", image="sam", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")
define cs_fe_ts      = Character("Tsubaki", image="tsubaki", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")
define cs_fe_gary    = Character("Gary", image="gary", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")
define cs_fe_gregor  = Character("Gregor", image="gregor", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")
define cs_fe_leif    = Character("Leif", image="leif", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")
define cs_fe_captain = Character("Captain", image="cs_matsuda_captain", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")
define cs_fe_scout   = Character("Scout", image="cs_matsuda_scout", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")
define cs_fe_medic   = Character("Medic", image="cs_matsuda_medic", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")

image cs_matsuda_captain = Transform("assets/characters/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image cs_matsuda_scout = Transform("assets/characters/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image cs_matsuda_medic = Transform("assets/characters/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))

screen cs_matsuda_fe_stage_overlay():
    zorder -20

    add Solid("#06060624") xysize (1280, 720)
    add Solid("#00000040") xpos 0 ypos 0 xysize (1280, 36)
    add Solid("#00000036") xpos 0 ypos 668 xysize (1280, 52)
    add Solid("#00000030") xpos 0 ypos 0 xysize (42, 720)
    add Solid("#00000030") xpos 1238 ypos 0 xysize (42, 720)
    add Solid("#8b7a5530") xpos 54 ypos 56 xysize (1, 590)
    add Solid("#8b7a5530") xpos 1225 ypos 56 xysize (1, 590)

screen cs_matsuda_fe_say(who, what):
    # soft band to seat the box against the letterboxed stage
    add Solid("#00000048") xpos 0 ypos 506 xysize (1280, 214)

    # dialogue box: gold border + navy body, drawn as plain Solids with an
    # explicitly-positioned text. Built without `frame` on purpose -- the mod's
    # themed `style frame` injects a Frame() background and border padding that
    # shoves the text around once the box is given a fixed size + xfill/yfill.
    add Solid("#b7a46b") xpos 120 ypos 548 xysize (1040, 168)
    add Solid("#0b1626f4") xpos 123 ypos 551 xysize (1034, 162)

    text what id "what":
        style "cs_matsuda_fe_dialogue"
        xpos 158 ypos 576
        xmaximum 962

    # nameplate: auto-sizes to the speaker's name, seated on the box's top edge.
    if who is not None:
        frame:
            xpos 150 ypos 514
            padding (2, 2)
            background Solid("#6d5830")

            frame:
                padding (20, 6)
                background Solid("#d2bf82")

                text who id "who" style "cs_matsuda_fe_label"

    use quick_menu

style cs_matsuda_fe_label is default:
    size 24
    color "#2a1d10"
    bold True
    outlines [(1, "#f6e9b4", 0, 0)]

style cs_matsuda_fe_dialogue is default:
    size 30
    color "#f2f1e8"
    line_spacing 6
    outlines [(2, "#000000cc", 1, 1)]
    layout "tex"

label cs_matsuda_01:
    hide screen archive
    hide screen character_stories

    scene black
    stop music fadeout 1.0
    stop sound
    show screen cs_matsuda_fe_stage_overlay
    window hide
    pause 1.0

    # ------------------------------------------------------------------ #
    # I. The war council
    # ------------------------------------------------------------------ #
    play music hotr
    scene bg castle01_strategyroom with dissolve_scene_full

    show cs_matsuda_captain at l21
    show matsuda thinking at t22
    cs_fe_captain "Commander. Scouts are in. Snow's moving on the pass above Greywake -- by dawn it's shut, and the east road goes with it."
    cs_fe_akai "...Dawn."
    cs_fe_captain "Dawn, if we're lucky."
    cs_fe_akai "Get the officers. All of them, now."
    show cs_matsuda_captain at thide
    hide cs_matsuda_captain
    pause 0.5

    show matsuda determined at t11
    cs_fe_akai "You've heard by now, or you're about to: come morning, the snow shuts the pass, and every road home shuts with it."
    cs_fe_akai "Nobody across that field intends to feed us through a winter."
    cs_fe_akai "So we go tonight."
    cs_fe_akai "I know what tonight is. I won't stand here and call it fair."
    cs_fe_akai "Gary. You first. Say your piece before I give the order."

    show gary at l21
    show matsuda annoyed at t22
    cs_fe_gary "The third wagon, Commander. My mother is in the third wagon -- I watched them load her in. My sisters are in the fourth."
    cs_fe_gary "I've counted those wagons every day for a month. From the ridge, through a spyglass, until my eye watered."
    cs_fe_gary "Give me the ravine and a dozen riders. I can have them out before the lines even touch."
    cs_fe_akai "And if you can't?"
    cs_fe_gary "...There's a letter in my tent. It says no one is to come after me."
    cs_fe_akai "Burn the letter, Gary."
    cs_fe_gary "Commander--"
    cs_fe_akai "You get the ravine, you get the riders, and you burn the letter. That's the deal. Take it or sit down."
    cs_fe_gary "Taken."
    show gary at thide
    hide gary

    show matsuda neut at t11
    cs_fe_akai "Gregor."

    show gregor at l21
    show matsuda sad at t22
    cs_fe_gregor "Gregor is here."
    cs_fe_akai "The left. You hold it until my horn -- however long that takes, whatever comes up that field. The plan hangs off the left staying planted."
    cs_fe_gregor "..."
    cs_fe_gregor "At Varn's Crossing, Gregor held. Gregor stood in the wall and listened to his friends' voices stop, one at a time. Eleven of them."
    cs_fe_gregor "Gregor still knows the order they went quiet in."
    cs_fe_akai "I know. I was there."
    cs_fe_gregor "Then you know what you're asking."
    cs_fe_akai "I do. And I'm asking anyway, because you're the only man on this field I'd bet the center on."
    cs_fe_gregor "The left will hold. Gregor gives his word, and Gregor has never broken it."
    cs_fe_gregor "Just -- don't let the horn be late, Commander. Gregor asks one thing. Don't let it be late."
    show gregor at thide
    hide gregor

    show matsuda neut at t11
    cs_fe_akai "Leif."

    show leif at l21
    show matsuda unamused at t22
    cs_fe_leif "The west ridge. Tell me it's the west ridge."
    cs_fe_akai "It's the west ridge."
    cs_fe_leif "Ha! Their supply road runs right under it. Put my riders up there and their rear folds sideways just trying to keep an eye on me."
    cs_fe_akai "And their berserker comes up that hill to take it back. You've heard the same stories I have."
    cs_fe_leif "Stories grow a foot every campfire they cross."
    cs_fe_akai "This one doesn't need to grow. You go on my horn, you turn their line -- and then you get {i}off{/i} that ridge. Take it. Don't try to keep it."
    cs_fe_leif "Take it, don't keep it. On your horn."
    cs_fe_leif "...And if he's faster than the stories?"
    cs_fe_akai "Then be faster than that."
    show leif at thide
    hide leif

    # Akai and the cleric -- the emotional spine of the campaign.
    show matsuda worried at t22
    show tsubaki determined at t21
    cs_fe_ts "One more rider. Under the white branch. It costs us an hour."
    cs_fe_akai "We sent terms yesterday. He formed ranks while our herald was still talking."
    show tsubaki neut
    cs_fe_ts "I know. I watched him do it."
    show tsubaki sad
    cs_fe_ts "I'd still like us to have asked twice. At midnight, when I'm sewing men shut, I want to be able to think: we asked twice."
    cs_fe_akai "We don't have the hour, Tsubaki."
    show tsubaki neut
    cs_fe_ts "No. We don't."
    cs_fe_akai "You'll be behind the center. Behind me."
    show tsubaki worried
    cs_fe_ts "Behind you I can reach the middle of the field and nothing else. If a wing goes down--"
    cs_fe_akai "Behind me, I know where you are."
    cs_fe_ts "..."
    show tsubaki sad
    cs_fe_ts "You'd never take that reason from me."
    cs_fe_akai "No. I wouldn't."
    cs_fe_ts "..."
    cs_fe_akai "If the center breaks, you go north with Gary. You don't argue, and you don't come looking for me."
    show tsubaki afraid
    cs_fe_ts "And if it's you on the ground?"
    cs_fe_akai "Then I finally get to learn what you say to people who won't follow instructions."
    show tsubaki frustrated
    cs_fe_ts "That's not an answer, Akai."
    cs_fe_akai "It's the one I've got."
    show matsuda at thide
    show tsubaki at thide
    hide matsuda
    hide tsubaki

    # The commander, alone. The music leaves with the officers.
    stop music fadeout 2.0
    pause 1.0

    show matsuda sad at t11
    cs_fe_akai "Twelve hours."
    cs_fe_akai "Twelve hours, and every piece back on this table. That's all I'm asking."
    cs_fe_akai "...I don't even know who I'm asking."
    show matsuda at thide
    hide matsuda

    window hide
    scene black with wipeleft_scene
    pause 0.6

    # ------------------------------------------------------------------ #
    # II. The rival's fortress
    # ------------------------------------------------------------------ #
    play music fantasypassion
    scene bg fortress with dissolve_scene_full

    show mc neut at t21
    show sam neut at t22
    cs_fe_sam "Six owners in ten years, this heap, and not one of them ever bothered to fly a flag over it. And here we are, about to bleed for the view."
    cs_fe_rival "She comes tonight. She has to -- the pass shuts at dawn, and she knows it better than we do."
    show sam determined
    cs_fe_sam "Good. The waiting is the only thing on this field that's ever scared me."
    cs_fe_rival "Before it starts, the prisoners get moved. Behind the reserve, out of reach."
    show sam unamused
    cs_fe_sam "You're joking."
    cs_fe_rival "Do I do that?"
    show sam frustrated
    cs_fe_sam "Those wagons are the whole reason she's charging! Leave them where she can see them and she'll break her own line trying to reach them. That's the battle, won, before it starts."
    cs_fe_rival "They're prisoners, Sam. Somebody's mother is sitting in one of those wagons with her wrists tied. I'm not making her the cheese in a trap."
    cs_fe_sam "It's the best card in your hand."
    cs_fe_rival "Then I'll lose holding a worse one. Move them."
    show sam smug
    cs_fe_sam "Hah."
    cs_fe_sam "This is why the men actually like you, you know that? It is inconvenient as all hell."
    cs_fe_rival "The west ridge. When her cavalry comes for it -- and it will come -- you're what's waiting at the top."
    show sam thinking
    cs_fe_sam "Cavalry. Then whatever she sends when the cavalry doesn't come back. Then whatever she sends after that."
    cs_fe_sam "You're handing me the hill people are going to name, aren't you."
    cs_fe_rival "I'm handing it to you because you're the only one who might still be standing on it in the morning."
    cs_fe_sam "'Might.' You're a real comfort, Commander."
    show sam worried
    cs_fe_sam "And if she cuts through all of it? If it ends up just the two of you, in the mud somewhere?"
    cs_fe_rival "Then nobody steps in. Nobody finishes it for me. That includes you."
    cs_fe_sam "'Course it does."
    show sam determined
    cs_fe_sam "Then don't lose. I am not climbing down off a famous hill to avenge anybody."
    show sam at thide
    show mc neut at thide
    hide sam
    hide mc

    stop music fadeout 1.0
    window hide
    scene black with wipeleft_scene
    pause 0.5

    # ------------------------------------------------------------------ #
    # III. Greywake Field
    # ------------------------------------------------------------------ #
    play music flight
    scene bg battlefield01 with dissolve_scene_full

    show mc neut at t21
    show sam determined at t22
    cs_fe_rival "Shield wall. Second company doesn't move until their red banner does."
    cs_fe_sam "Ridge is quiet."
    cs_fe_rival "Enjoy it while it lasts."
    show mc neut at thide
    show sam at thide
    hide mc
    hide sam

    show matsuda thinking at t21
    show tsubaki neut at t22
    cs_fe_akai "Center forward. Walking pace. Let him spend the approach counting us."
    show tsubaki shocked
    cs_fe_ts "Akai -- the wagons. The wagons are moving. Back, behind their reserve."
    cs_fe_akai "...He pulled the prisoners off the line."
    show tsubaki curious
    cs_fe_ts "That's good. Isn't it? For them?"
    cs_fe_akai "For them. For us, it means he plans to beat me fair."
    cs_fe_akai "And he might. Don't repeat that."
    show matsuda at thide
    show tsubaki at thide
    hide matsuda
    hide tsubaki

    stop music fadeout 0.8
    play music epicbattlephase1
    play sound audio.sfx_longwoosh
    with hpunch

    show cs_matsuda_captain at t11
    cs_fe_captain "ARROWS! Shields UP -- UP, get them UP--"
    show cs_matsuda_captain at thide
    hide cs_matsuda_captain

    show mc neut at t21
    show sam determined at t22
    cs_fe_rival "Hold! Let the shields eat it!"
    cs_fe_sam "Her center's bending. There's your push -- take it, take it now--"
    cs_fe_rival "It's bait. She bends on purpose so her wings can fold on me the second I lean in. We hold."
    show sam unamused
    cs_fe_sam "You're no fun at all."
    cs_fe_rival "Go. Your ridge is about to stop being quiet."
    show mc neut at thide
    show sam at thide
    hide mc
    hide sam

    show matsuda determined at t21
    show tsubaki worried at t22
    cs_fe_akai "Gary -- the ravine, now. Leif -- the horn is coming, hold your riders until it sounds."
    cs_fe_ts "The first wounded are coming back through the center. It's a lot, Akai. Already, it's a lot."
    cs_fe_akai "...Treat the ones who can still walk."
    show tsubaki frustrated
    cs_fe_ts "..."
    cs_fe_akai "Tsubaki. The ones who can walk."
    show tsubaki sad
    cs_fe_ts "I heard you."
    show tsubaki determined
    cs_fe_ts "When this is over, you'll say that order again for me. Once. So you hear what it costs."
    cs_fe_akai "Fine. After."

    show gary at t31
    show matsuda neut at t32
    show tsubaki worried at t33
    cs_fe_gary "Ravine unit's mounted, Commander."
    cs_fe_akai "Then go. Bring them home."
    cs_fe_gary "...Yes ma'am."
    show gary at thide
    hide gary
    show matsuda at thide
    show tsubaki at thide
    hide matsuda
    hide tsubaki

    play sound audio.sfx_shing
    show white zorder 200:
        alpha 0.45
        linear 0.18 alpha 0.0
    with hpunch
    pause 0.25
    hide white

    show gary at t11
    cs_fe_gary "Mother. {i}Mother!{/i} It's me -- hey. Hey. Look at me, not the field. We're going. All of you, everyone, right now -- we're going."
    cs_fe_gary "I counted the wagons. Every single day, I counted. I always knew exactly where you were."
    show gary at thide
    hide gary

    show leif at t21
    cs_fe_leif "The ridge is OURS! Their rear is turning -- Commander, it's working, they're peeling half the line just to face us--"
    show leif at thide
    hide leif

    play sound audio.sfx_wham
    with vpunch

    show cs_matsuda_scout at t11
    cs_fe_scout "Berserker! Berserker on the west ridge -- Leif's riders are breaking, they're-- gods, they're GONE, he went through them like a door--"
    show cs_matsuda_scout at thide
    hide cs_matsuda_scout

    show matsuda shocked at t21
    show tsubaki shocked at t22
    cs_fe_akai "Signal the left. Gregor holds -- the horn is COMING, tell him the horn is nearly there--"
    cs_fe_ts "Akai. He's not looking at the signal."

    show gregor at t31
    show matsuda afraid at t32
    show tsubaki afraid at t33
    cs_fe_gregor "Gregor hears the ridge. Gregor knows those voices."
    cs_fe_akai "Gregor, sixty breaths! The horn is sixty breaths away, that is ALL I need from you--"
    cs_fe_gregor "Leif's boys don't have sixty."
    cs_fe_gregor "Gregor swore his word to you, Commander. Gregor has never once broken it. So it can't be Gregor who goes."
    cs_fe_gregor "...{i}I'm{/i} sorry."
    show gregor at thide
    hide gregor
    show matsuda panicked at t21
    show tsubaki shocked at t22
    cs_fe_akai "GREGOR--!"
    play sound audio.sfx_shock
    with hpunch
    show tsubaki panicked
    cs_fe_ts "The left is going with him. All of it -- they won't let him charge that thing alone."
    cs_fe_akai "No, no, no -- the center's wide open, Gary is still in the ravine--"
    cs_fe_akai "The horn! Sound the horn, sound EVERYTHING -- if we're early, then we're early, GO!"

    show gary at t31
    show matsuda determined at t32
    show tsubaki afraid at t33
    cs_fe_gary "They're out! Commander, they're out, they're clear -- but the reserve is wheeling back, it's all coming down on the center now--"
    show gary at thide
    hide gary
    show matsuda worried at t21
    show tsubaki determined at t22
    cs_fe_akai "North, Gary. You don't stop, you don't turn around. You go NORTH."
    cs_fe_ts "Akai -- if he takes the north road, it closes behind him. That's our road home."
    cs_fe_akai "I know whose road it is."
    show tsubaki sad
    cs_fe_ts "..."
    cs_fe_akai "Stay close to me."

    play sound audio.sfx_fwashing
    stop music
    show white zorder 200:
        alpha 0.5
        linear 0.12 alpha 0.0
    with hpunch
    pause 0.4
    hide white

    show tsubaki shocked
    cs_fe_ts "..."
    cs_fe_akai "Tsubaki?"
    show tsubaki afraid
    cs_fe_ts "Don't turn around yet."
    cs_fe_akai "Tsubaki--"
    cs_fe_ts "One moment. Give me one moment, I'm just going to-- ah."
    show tsubaki empty
    cs_fe_ts "...That's deep."
    cs_fe_akai "MEDIC!"

    show cs_matsuda_medic at t31
    show matsuda shocked at t32
    show tsubaki empty at t33
    cs_fe_medic "...Commander."
    show cs_matsuda_medic at thide
    hide cs_matsuda_medic

    show matsuda frustrated at t21
    show tsubaki sad at t22
    cs_fe_akai "Don't say my name like that. Pack the wound, cut the shaft, we carry her--"
    cs_fe_ts "Akai."
    show tsubaki determined
    cs_fe_ts "Move me, and you spend two bearers and lose the hands holding this shut. You taught me that arithmetic."
    cs_fe_akai "I don't care about the arithmetic--"
    cs_fe_ts "You will. In an hour, you'll need it to have been done right."
    cs_fe_akai "Do not-- you do not get to do my job from the ground."
    show tsubaki teasing
    cs_fe_ts "Somebody has to. You're busy."
    cs_fe_akai "Tsubaki--"
    cs_fe_ts "Gary needs the road. That's the reason we came. You said it in the keep, and I believed you."
    show tsubaki happy
    cs_fe_ts "So go. I'll be right here."
    show tsubaki sad
    cs_fe_ts "...Right behind you. Where you know where I am."
    pause 0.4
    show tsubaki at thide
    hide tsubaki

    show matsuda determined at t11
    cs_fe_akai "Medic. Stay with her. If she says anything, you keep every word, and you bring it to me after."
    cs_fe_akai "There is going to be an after. Say it back."
    cs_fe_medic "...There's going to be an after, Commander."

    play music hopeless
    show sam determined at t21
    show matsuda angry at t22
    cs_fe_sam "Akai."
    cs_fe_akai "...Move."
    cs_fe_sam "Can't. You know I can't."
    cs_fe_akai "You're him. The ridge."
    show sam sad
    cs_fe_sam "What's left of it."
    cs_fe_akai "You held. There's nothing up there left to hold. {i}Move.{/i}"
    show sam determined
    cs_fe_sam "He's at the bottom of this field. And you don't get to him while I'm standing. So."
    cs_fe_akai "Then stop standing."
    show sam smug
    cs_fe_sam "Hah."
    cs_fe_sam "There she is. They told me you'd be polite about it."

    play sound audio.sfx_swing
    show white zorder 200:
        alpha 0.35
        linear 0.10 alpha 0.0
    with hpunch
    pause 0.18
    hide white
    play sound audio.sfx_stab
    show white zorder 200:
        alpha 0.65
        linear 0.18 alpha 0.0
    with vpunch
    pause 0.25
    hide white

    show sam empty
    cs_fe_sam "...Hah."
    cs_fe_sam "Do me one thing. Tell him the ridge held. He'll want it from somebody who was up there."
    cs_fe_akai "He knows what he asked of you."
    cs_fe_sam "That's why. He'll be doing sums with it for the rest of his life."
    cs_fe_sam "Tell him it held. And tell him I'd have gone up anyway. Knowing. Say it just like that."
    cs_fe_akai "...It held. You'd have gone up anyway. Knowing."
    cs_fe_sam "Good. Hate to leave a thing half--"
    show sam at thide
    hide sam

    show matsuda sad at t11
    cs_fe_akai "..."
    cs_fe_akai "I'll tell him. On whatever's left of us, I'll tell him."

    stop music fadeout 1.0
    window hide
    scene black with wipeleft_scene
    pause 0.5

    play music devoted
    scene bg battlefield01 with dissolve_scene_full
    show mc neut at t21
    show matsuda neut at t22
    cs_fe_rival "Where's Sam?"
    cs_fe_akai "The ridge."
    cs_fe_rival "..."
    cs_fe_akai "He held it. He wanted you to know it held -- and that he'd have gone up anyway. Knowing. He made me say it back so I'd get it right."
    cs_fe_rival "...That sounds like him."
    cs_fe_rival "...Your cleric?"
    cs_fe_akai "The center."
    cs_fe_rival "..."
    cs_fe_rival "Order the retreat, Akai. Please. There's nothing here left worth having."
    cs_fe_akai "The prisoners are out. The north road stays open while your army is looking at me."
    cs_fe_rival "So you'll stand there and keep us looking."
    cs_fe_akai "As long as it takes."
    cs_fe_rival "We could stop. Both of us. Right now. Who's even left to make us?"
    cs_fe_akai "...Everyone we spent getting here."
    cs_fe_rival "...Yeah. I knew what you'd say. I just needed the other thing said out loud once. So it existed."
    cs_fe_akai "Meet me in the middle, then."

    window hide
    scene black with dissolve_scene_full
    pause 0.8

    # ------------------------------------------------------------------ #
    # IV. The duel
    # ------------------------------------------------------------------ #
    # The dedicated duel CG (cg campaign) was cut with its asset; the ruined
    # field itself carries the scene until replacement art exists.
    scene bg battlefield01 with dissolve_scene_full
    pause 0.8

    show mc neut at t21
    show matsuda determined at t22
    cs_fe_rival "...They've stopped. Both armies. Did you order yours to stand down?"
    cs_fe_akai "No."
    cs_fe_rival "Neither did I."
    cs_fe_rival "You can barely lift that."
    cs_fe_akai "You're bleeding through your boot. We've all got problems."
    cs_fe_rival "Quarter. Last time I offer it."
    cs_fe_akai "I know. Thank you."
    cs_fe_akai "No."
    cs_fe_rival "{i}Why?{/i} Give me one reason that isn't pride--"
    cs_fe_akai "Gary is on the north road with forty freed people and everything I have left. If this ends with me kneeling, then all of it bought a surrender. It has to end standing up."
    cs_fe_akai "For Gregor, who broke his word once in his life, for a friend."
    cs_fe_akai "For Leif, who was faster than every story but one."
    cs_fe_akai "...For Tsubaki."
    cs_fe_akai "..."
    cs_fe_rival "...For Sam."
    cs_fe_rival "All right, Akai. Standing up, then."

    play music epicbattlephase2
    play sound audio.sfx_shing
    show white zorder 200:
        alpha 0.45
        linear 0.20 alpha 0.0
    with hpunch
    pause 0.25
    hide white

    cs_fe_akai "Again."
    cs_fe_rival "Your guard is gone. Akai, your guard is {i}gone,{/i} I can see--"
    cs_fe_akai "Then take the opening or stop narrating it!"

    play sound audio.sfx_swing
    with hpunch
    pause 0.2
    play sound audio.sfx_stab2
    stop music
    show white zorder 200:
        alpha 0.65
        linear 0.20 alpha 0.0
    with vpunch
    pause 0.4
    hide white

    cs_fe_rival "..."
    cs_fe_akai "..."
    cs_fe_rival "...I can't move."
    cs_fe_akai "Your point's at my throat."
    cs_fe_rival "Yours is under my ribs."
    cs_fe_akai "So if either of us finishes it--"
    cs_fe_rival "...Both of us finish."
    cs_fe_rival "..."
    cs_fe_rival "...A draw."
    cs_fe_akai "...A draw."
    cs_fe_rival "All of it. All of {i}them.{/i} For a draw."
    cs_fe_akai "..."
    cs_fe_akai "The wagons went north."
    cs_fe_akai "That's what it was for. Let the field keep the rest."

    window hide
    scene black with dissolve_scene_full
    pause 1.5

    # ------------------------------------------------------------------ #
    # V. The table
    # ------------------------------------------------------------------ #
    hide screen cs_matsuda_fe_stage_overlay
    play music enterm
    scene bg living_room with dissolve_scene_full
    show sam neut at t41
    show matsuda neut at t42
    show asahina neut at t43
    show tsubaki neut at t44
    window auto

    ma "...And the die rolls to a stop against my notebook."
    ma "Both blades land. Neither of them has enough left to stand back up. The Commander and the Rival go down in the same breath -- swords still in each other."
    ma "That's it. That's Greywake."
    ma "...A draw."
    sa "..."
    show asahina shocked
    ah "..."
    show tsubaki shocked
    ts "..."
    show matsuda curious
    ma "...Guys?"
    show sam shocked
    sa "A draw."
    ma "A draw!"
    show sam angry
    sa "A {i}DRAW?!{/i}"
    show matsuda unamused
    ma "Why are we saying it more times?!"
    show sam frustrated
    sa "NINETEEN ROUNDS, MATSUDA. I held that ridge for NINETEEN ROUNDS. I did MATH about my own death! I gave a whole SPEECH!"
    ma "It was a great speech--"
    show sam angry
    sa "I KNOW it was a great speech! I nearly cried at my own guy, which is the single most humiliating thing that has ever happened to me at a folding table, and it was all the setup for a TIE?!"
    ma "It's not a tie, it's a mutual--"
    sa "IF NOBODY WINS, IT'S A TIE."
    show matsuda frustrated
    ma "Those nineteen rounds are the only reason the wagons got out! You carried the entire--"
    show sam frustrated
    sa "DON'T. Don't you dare hand me a participation ribbon for the ridge!"
    show tsubaki worried
    ts "...Did she live?"
    show asahina angry
    ah "No. No no no, Sam can get in line, because I have been sitting on this since the LEFT WING."
    ah "You put Leif's unit dying in Gregor's {i}earshot.{/i} You described the voices, Matsuda. You looked me dead in the eye, described his friends' voices getting cut off one at a time, and then made me roll to not care."
    ma "That's what a Wisdom save IS--"
    ah "You call that a save?! That was ENTRAPMENT!"
    show matsuda annoyed
    ma "You rolled a FOUR!"
    show asahina frustrated
    ah "GREGOR DOESN'T NEED WISDOM! GREGOR NEEDS HIS FRIENDS TO STOP DYING ELEVEN AT A TIME!"
    ma "Then maybe Gregor shouldn't have handed the entire center to--"
    show asahina disgusted
    ah "Oh. OHHHH. So it's GREGOR'S fault now. Your plan had ONE hinge, the hinge was a man you KNEW would break, and the blame goes on HIS sheet?!"
    ma "It was a FAIR battle! I rolled everything in the open! Do you people have any idea what other GMs {i}do?!{/i}"
    show tsubaki nervous
    ts "Excuse me -- the medic. Did the medic reach--"
    show sam casual pose_open_hand
    sa "Here's my question. Here's my actual question."
    sa "The draw. Was it in the notebook?"
    show matsuda shocked
    ma "...What?"
    sa "Before session one. 'Two commanders, mirrors of each other, doomed by fate,' all of that. Did you have the ending written down the whole time? Because if you did, that's COWARDICE. Narrative COWARDICE."
    show matsuda angry
    ma "..."
    ma "Take that back."
    show sam casual unamused
    sa "It's a question--"
    ma "Take it BACK. I have never railroaded an ending in my LIFE. I rolled Tsubaki's arrow in the open and it made me feel SICK. I almost called a break so I could go stare into the fridge!"
    m "Guys."
    show sam frustrated
    sa "All I know is the two protagonists got a poetic mutual KO like a Saturday matinee, and my guy is a FOOTNOTE on a HILL--"
    show mc neut at t22
    mc "Okay. Everybody's tired. Maybe we take five, and--"
    show sam angry
    sa "Oh, don't you DARE."
    show asahina smug
    ah "The duel guy speaks!"
    mc "...What did {i}I{/i} do?"
    show asahina frustrated
    ah "You got the CINEMATIC ending! You got 'meet me in the middle'! Of course the draw works for you -- you were IN it!"
    mc "I lost my entire army!"
    show sam frustrated
    sa "You got a sword-crossing freeze-frame! I got LEFT on a HILL!"
    mc "...I'm gonna go sit by the snacks."
    show mc neut at thide
    hide mc
    show asahina angry
    ah "And while we're at it -- GARY?! Gary gets a flawless rescue?! Zero casualties?! Monika writes four paragraphs of backstory and suddenly the dice can do no wrong!"
    m "Gary succeeded because Gary made good choices and went in at night."
    show sam unamused
    sa "Oh, she's insufferable now."
    m "I counted the wagons every session for a MONTH, Sam. Foreshadowing pays for itself."
    ah "THAT IS NOT A MECHANIC!"
    show matsuda teasing
    ma "It's a little bit of a mechanic--"
    show asahina annoyed
    ah "DON'T reward her!"
    show tsubaki frustrated
    ts "Please. Can somebody just tell me if--"
    show matsuda angry
    ma "And you know WHAT?! Since we're all listing grievances tonight--"
    ma "THREE WEEKS. I spent three weeks on that field! I drew a MAP. I did VOICES. I built a WEATHER SYSTEM that not one of you ever asked about! I gave Gary's mother a NAME, Monika -- she has a favorite SOUP--"
    show sam angry
    sa "NOBODY ASKED FOR SOUP LORE! WE ASKED FOR AN ENDING!"
    ma "You GOT an ending! You got the only honest ending on the table, and if you would stop screaming for five seconds you might actually--"
    show tsubaki angry
    ts "DID SHE LIVE OR NOT?!" with vpunch
    sa "--In a SECOND, Tsubaki, I am about to WIN this--"
    ma "You are NOT--"
    show asahina frustrated
    ah "NOBODY is winning! That is the entire PROBLEM!"
    show tsubaki empty
    ts "..."
    show tsubaki sad
    ts "...Fine. Forget it. It's fine."

    # Monika detonates. Not to restore the peace -- to get the question answered.
    stop music fadeout 0.35
    window hide(None)
    show white zorder 200
    play sound interjection
    pause 0.06
    hide white
    show monika forward casual vang om oe nobl rhip lpoint at t11
    show matsuda shocked
    m forward casual vang om oe nobl rhip lpoint "STOOOOOOOOOOOOOOOOOOOOOOOP!" with hpunch
    window show(None)
    show sam shocked
    sa "..."
    show asahina shocked
    ah "..."
    ma "..."
    show tsubaki shocked
    ts "..."
    mc "{size=12}...You punched me outta my seat...{/size}"
    m forward casual vang om oe nobl rhip lpoint "Tsubaki has asked ONE question tonight. One! She has asked it FOUR TIMES."
    m forward casual angr om oe nobl rhip lpoint "I know it was four because I sat here and COUNTED, like her little lawyer, waiting for literally any one of you to be a person about it!"
    show sam nervous
    sa "...I was going to--"
    m forward casual angr om oe nobl rhip lpoint "FOUR, Sam!"
    show sam embarrassed
    sa "..."
    show tsubaki embarrassed
    m forward casual vang om oe nobl rhip lpoint "And YOU."
    ma "...Moi?!"
    m forward casual angr om oe nobl rhip lpoint "You have had that medic check in your pocket for half an hour. 'We'll roll it at the epilogue.' We are AT the epilogue! You are hoarding a woman's life for AMBIANCE!"
    show matsuda annoyed
    ma "It's called dramatic timi--"
    m forward casual vang om oe nobl rhip lpoint "ROLL. IT."
    show matsuda neut
    ma "..."
    m forward casual worr cm oe nobl rhip ldown "And since apparently tonight we're all screaming our feelings:"
    m forward casual worr cm oe nobl rhip ldown "I {i}cried{/i} at this table. Over a wagon. That scene was the best thing I have gotten to play in any campaign, ever -- and you are all having a fistfight on top of it."
    show sam neut
    sa "...The wagon scene was legitimately great."
    show asahina embarrassed
    ah "...It was stupidly good. I hate this table so much."

    ma "...Okay."
    ma "Okay. ...Tsubaki. You roll it."
    show tsubaki afraid
    ts "...Me?"
    ma "Your cleric. Your hands. The medic reaches her in time on a nine or better."
    show tsubaki panicked
    ts "Why would you make ME do it?! What if I roll a two, Matsuda?! I have to LIVE here!"
    ma "Because she was never mine. I just borrowed her for the war."
    show tsubaki nervous
    ts "..."
    show tsubaki determined
    ts "...Okay. Okay. Rolling. I'm rolling it."
    show tsubaki afraid
    ts "I can't look. I'm not looking. Somebody who isn't me looks."
    m forward casual sad cm oe nobl rdown ldown "..."
    ts "...Monika."
    m forward casual sad cm oe nobl rdown ldown "..."
    show tsubaki frustrated
    ts "MONIKA."
    m forward casual vsur om oe blus rdown ldown "Eleven."
    play music roster_place
    m forward casual happ om oe blus rdown ldown "She lives, Tsubaki. Your dumb, stubborn cleric lives."
    show tsubaki crying
    ts "...oh."
    ts "...Okay. Okay, good. That's-- yeah."
    ts "Nobody look at me. I mean it. Eyes elsewhere."
    show sam happy
    sa "Nobody's looking at you, champ."

    show matsuda determined
    ma "...Since half this room has decided I scripted it: I wanted Akai to win."
    ma "I have wanted Akai to win that field since I drew it {i}last month{/i}"
    show asahina unamused
    ah "We know. She's named after you."
    ma "--And the dice said no. At the end, with every one of you watching, the dice said no. Three times."
    ma "I could have fudged it. One number behind a screen, and Akai gets her victory, and none of you ever finds out."
    ma "But then it's not ours anymore. It's just mine. A bedtime story I read {i}at{/i} you."
    ma "The draw is the only ending this table actually rolled. So I kept it."
    show sam annoyed
    sa "..."
    sa "...I'm still mad."
    show matsuda smug
    ma "Good. It was a war. Somebody should be."
    show sam smug
    sa "It was a good war, though. That's the annoying part. That's why I'm like this."
    show matsuda neut
    ma "...I know. Thank you."

    # The air clears. The ribbing returns -- gentler now.
    show asahina teasing
    ah "Okay, but we ARE circling back to how your self-insert walked out of the entire war without a scratch."
    show matsuda annoyed
    ma "Akai is not a self-insert!"
    m forward casual happ cm ce nobl rdown ldown "Her name is Matsuda Akai."
    ma "It's a COMMON name--"
    show sam teasing
    sa "You did her voice in first person for four hours!"
    ma "That's called GMING--"
    show asahina smug
    ah "You gave yourself a SOLO SCENE! Everyone leaves the war room, and she stays behind to whisper doomed little vows at the map!"
    show matsuda frustrated
    ma "THAT WAS ATMOSPHERE."
    show asahina neut
    ah "..."
    ah "...He said 'I'm sorry,' you know. First person. Only time all campaign."
    ah "Eight sessions committed to that voice -- and the one time it mattered, it couldn't be the bit talking."
    show matsuda neut
    ma "...Yeah. I noticed."
    ma "Everyone noticed, Asahina. It was really good."
    show asahina embarrassed
    ah "...Thank you."
    show asahina determined
    ah "...Anyway, he's not dead."
    ma "He charged a berserker. On foot. {i}Uphill.{/i}"
    ah "Did you describe a body?"
    ma "The entire left wing--"
    ah "Did. You. Describe. A body."
    ma "..."
    show matsuda smug
    ma "...No body was described at this table."
    show asahina neut
    ah "Then Gregor holds. Somewhere out there, Gregor holds."
    show sam happy
    sa "My new guy finds him. Half-frozen on the ridge, too stubborn to die, still doing the third-person thing at the vultures--"
    ma "Do NOT co-write my sequel at me."
    m forward casual laug om ce nobl rdown ldown "She's writing it down."
    show matsuda unamused
    ma "I am NOT."
    m forward casual laug om ce nobl rdown ldown "She's got the pen and everything."

    show tsubaki curious
    ts "...What happens to them? After."
    show matsuda thinking
    ma "...Gary gets everyone to the treeline by dawn. Keeps going north until the war is just an accent people notice he has."
    ma "Years later, he names a daughter after a commander nobody up there has ever heard of."
    m forward casual sad om ce nobl rdown ldown "...Damn it. I built him to make it out. Why does it hurt {i}more?{/i}"
    ma "The cleric wakes up two days later, complains about the stitching, and outlives every other person in this story."
    ma "The draw holds. Nobody ever fights over Greywake again."
    ma "And the two commanders never see each other again. They just spend the rest of their lives writing letters, because the only person who understands what it cost is the one who paid the other half."
    show tsubaki sad
    ts "...That's so sad."
    show matsuda neut
    ma "It's a draw, Tsubaki. That's the good version of the sad thing."

    show sam determined
    sa "Runback. I want the sequel, I want a new guy, and I want him to have OPINIONS about the ridge."
    show matsuda teasing
    ma "Granted, granted, and god help us all. If he charges one hill alone, I'm feeding him to the weather system."
    sa "Deal. No promises."
    mc "There it is."
    m forward casual happ om oe nobl rdown lpoint "Sequel starts after snacks, though. I went way too hard on the charcuterie board and I refuse to be alone in that."
    show asahina smug
    ah "Seconded. Grief burns carbohydrates."
    show matsuda unamused
    ma "...Fine. Snacks. Nobody touches the map."
    show tsubaki determined
    ts "And the medic roll is canon. Say it's canon."
    ma "...The medic roll is canon."
    show tsubaki happy
    ts "Good."
    ma "Now somebody find my d20. It went under the couch right around the time Sam called me a coward."
    show sam teasing
    sa "I called the ENDING cowardly. Take better notes."
    show matsuda smug
    ma "...I hate every single one of you. Same time next Saturday?"
    show sam happy
    sa "Obviously."
    show asahina happy
    ah "Obviously."
    ts "...Wouldn't miss it."
    m forward casual happ cm oe nobl rdown ldown "Try and stop us."

    scene black with dissolve_scene_full
    stop music fadeout 2.0
    pause 2.0

    $ persistent.cs_matsuda_01_unlocked = True
    $ cs_mark_completed("cs_matsuda_01")
    return
