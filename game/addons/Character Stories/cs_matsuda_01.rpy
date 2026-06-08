# Matsuda Character Story 01 -- "Dead Fantasy"

define cs_matsuda_fe_ma = DynamicCharacter('ma_name', image='matsuda', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")
define cs_matsuda_fe_ts = DynamicCharacter('ts_name', image='tsubaki', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")
define cs_matsuda_fe_sa = DynamicCharacter('sa_name', image='sam', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")
define cs_matsuda_fe_mc = DynamicCharacter('player', image='mc', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")

define cs_matsuda_gary = Character("Gary", image="gary", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")
define cs_matsuda_gregor = Character("Gregor", image="gregor", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")
define cs_matsuda_leif = Character("Leif", image="leif", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")
define cs_matsuda_captain = Character("Captain", image="cs_matsuda_captain", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")
define cs_matsuda_scout = Character("Scout", image="cs_matsuda_scout", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")
define cs_matsuda_medic = Character("Medic", image="cs_matsuda_medic", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say")

image cs_matsuda_captain = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image cs_matsuda_scout = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image cs_matsuda_medic = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))

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
    add Solid("#0000003c") xpos 0 ypos 480 xysize (1280, 196)

    frame:
        style "cs_matsuda_fe_window"

        fixed:
            add Solid("#0a1627f6") xpos 0 ypos 0 xysize (1040, 170)
            add Solid("#122846dd") xpos 12 ypos 12 xysize (1016, 146)
            add Solid("#071222f0") xpos 20 ypos 20 xysize (1000, 130)
            add Solid("#b7a46b88") xpos 6 ypos 6 xysize (1028, 2)
            add Solid("#b7a46b70") xpos 6 ypos 162 xysize (1028, 2)
            add Solid("#b7a46b70") xpos 6 ypos 6 xysize (2, 158)
            add Solid("#b7a46b70") xpos 1032 ypos 6 xysize (2, 158)
            add Solid("#0000002e") xpos 46 ypos 116 xysize (948, 1)

            text what id "what" style "cs_matsuda_fe_dialogue"

    if who is not None:
        frame:
            style "cs_matsuda_fe_namebox"

            fixed:
                add Solid("#d2bf82f4") xpos 0 ypos 0 xysize (214, 38)
                add Solid("#6d5830cc") xpos 0 ypos 0 xysize (214, 3)
                add Solid("#6d5830aa") xpos 0 ypos 35 xysize (214, 3)
                add Solid("#efe0a970") xpos 12 ypos 7 xysize (190, 1)
                text who id "who" style "cs_matsuda_fe_label"

    use quick_menu

style cs_matsuda_fe_window is default:
    xpos 120
    ypos 550
    xsize 1040
    ysize 170
    padding (0, 0)
    background None

style cs_matsuda_fe_namebox is default:
    xpos 146
    ypos 520
    xsize 214
    ysize 38
    padding (0, 0)
    background None

style cs_matsuda_fe_label is default:
    xpos 18
    ypos 5
    xsize 178
    size 24
    color "#2a1d10"
    bold True
    text_align 0.5
    outlines [(1, "#f6e9b4", 0, 0)]

style cs_matsuda_fe_dialogue is default:
    xpos 520
    xanchor 0.5
    ypos 48
    xsize 900
    size 30
    color "#f2f1e8"
    line_spacing 4
    outlines [(2, "#000000cc", 1, 1)]
    text_align 0.5
    layout "tex"

label cs_matsuda_01:
    hide screen archive
    hide screen character_stories
    $ ma_name = "Matsuda"
    $ ts_name = "Tsubaki"
    $ sa_name = "Sam"
    $ cs_matsuda_rival = "MC"

    scene black
    stop music fadeout 1.0
    stop sound
    show screen cs_matsuda_fe_stage_overlay
    window hide
    pause 1.0

    play music hotr
    scene bg castle01_strategyroom with dissolve_scene_full
    window auto

    show matsuda neut at t11
    cs_matsuda_fe_ma "Greywake Field by dusk. The pass closes behind us if we wait, and [cs_matsuda_rival]'s army knows it."
    cs_matsuda_fe_ma "I need a plan that opens the eastern road without feeding half our line into his spears."
    cs_matsuda_fe_ma "Gary."

    show gary at t21
    show matsuda neut at t22
    cs_matsuda_gary "Their prison wagons are behind the right wing. My family should be there."
    cs_matsuda_gary "If we can draw their center forward, I can take a small unit through the ravine and reach them."
    show gary at thide
    hide gary

    show matsuda neut
    cs_matsuda_fe_ma "Then the road and the prisoners are the same objective."
    cs_matsuda_fe_ma "Gregor."

    show gregor at t21
    show matsuda neut
    cs_matsuda_gregor "Gregor breaks center. Gregor kills [cs_matsuda_rival]. No more prison wagons."
    show gregor at thide
    hide gregor

    show matsuda neut
    cs_matsuda_fe_ma "No."
    cs_matsuda_fe_ma "You hold the left until my horn. If you move early, his cavalry folds us in half."

    show gregor at t21
    show matsuda neut
    cs_matsuda_gregor "Gregor can hold."
    cs_matsuda_gregor "Gregor hates holding."
    show gregor at thide
    hide gregor

    show matsuda neut
    cs_matsuda_fe_ma "Good. Hate it quietly."
    cs_matsuda_fe_ma "Leif."

    show leif at t21
    show matsuda neut
    cs_matsuda_leif "Their vanguard is disciplined, but the rear is thin."
    cs_matsuda_leif "If I take riders along the west ridge, I can threaten their supply line and force the center to turn."
    show leif at thide
    hide leif

    show matsuda neut
    cs_matsuda_fe_ma "That gives Gary his opening."
    cs_matsuda_fe_ma "It also gives [cs_matsuda_rival] a reason to send Sam after you."

    show leif at t21
    show matsuda neut
    cs_matsuda_leif "Then I need to move before Sam can turn the flank into a slaughter."
    show leif at thide
    hide leif

    show matsuda neut
    cs_matsuda_fe_ma "You move on my horn. Not before."

    show tsubaki neut at t21
    show matsuda neut
    cs_matsuda_fe_ts "Could we send terms one more time?"
    cs_matsuda_fe_ts "If the prisoners are still alive, someone on their side may be willing to listen."
    show tsubaki neut
    show matsuda neut
    cs_matsuda_fe_ma "We sent terms yesterday."
    cs_matsuda_fe_ma "He answered with a formation."
    show matsuda neut
    show tsubaki neut
    cs_matsuda_fe_ts "I know."
    cs_matsuda_fe_ts "I just wanted to ask before the wounded start coming back."
    show tsubaki neut
    show matsuda neut
    cs_matsuda_fe_ma "Stay behind me when they do."
    show matsuda neut
    show tsubaki neut
    cs_matsuda_fe_ts "Behind you, I can only reach the center."
    show tsubaki neut
    show matsuda neut
    cs_matsuda_fe_ma "Behind me, I know where you are."
    show matsuda neut
    show tsubaki neut
    cs_matsuda_fe_ts "Matsuda."
    show tsubaki neut
    show matsuda neut
    cs_matsuda_fe_ma "If the center collapses, you leave with Gary."
    cs_matsuda_fe_ma "If I fall, you leave with Gary."
    show matsuda neut
    show tsubaki neut
    cs_matsuda_fe_ts "And if you order me to abandon you?"
    show tsubaki neut
    show matsuda neut
    cs_matsuda_fe_ma "Then you remember I outrank you."
    show matsuda neut
    show tsubaki neut
    cs_matsuda_fe_ts "I remember too many things."
    show tsubaki neut
    show matsuda neut
    cs_matsuda_fe_ma "Then remember this. We are not here for glory."
    cs_matsuda_fe_ma "We open the road. We free the prisoners. We leave with whoever still draws breath."

    show matsuda neut at thide
    show tsubaki neut at thide
    hide matsuda
    hide tsubaki

    scene black with wipeleft_scene
    pause 0.6

    scene bg fortress with dissolve_scene_full
    show mc neut at t21
    show sam neut at t22
    cs_matsuda_fe_mc "Matsuda will strike before dusk."
    cs_matsuda_fe_mc "She needs the eastern road, and she knows I cannot abandon the pass."
    show mc neut
    show sam neut
    cs_matsuda_fe_sa "Then let her chase the road. I hit the flank, you take the commander."
    show sam neut
    show mc neut
    cs_matsuda_fe_mc "The prisoners move behind the reserve before the battle starts."
    show mc neut
    show sam neut
    cs_matsuda_fe_sa "You're giving up clean bait."
    show sam neut
    show mc neut
    cs_matsuda_fe_mc "They are prisoners, not bait."
    cs_matsuda_fe_mc "If I need families in chains to win a field, I have already lost more than the field."
    show mc neut
    show sam neut
    cs_matsuda_fe_sa "Then where do you want me?"
    show sam neut
    show mc neut
    cs_matsuda_fe_mc "Watch the west ridge. Leif will try to split us there."
    cs_matsuda_fe_mc "If you break him fast, Matsuda has to choose between the prisoners and her own line."
    show mc neut
    show sam neut
    cs_matsuda_fe_sa "She'll choose the line."
    show sam neut
    show mc neut
    cs_matsuda_fe_mc "No. She will try to save both."
    show mc neut
    show sam neut
    cs_matsuda_fe_sa "You sound like you respect her."
    show sam neut
    show mc neut
    cs_matsuda_fe_mc "I do."
    cs_matsuda_fe_mc "That is why we do not give her time."
    show mc neut
    show sam neut
    cs_matsuda_fe_sa "And if she reaches you?"
    show sam neut
    show mc neut
    cs_matsuda_fe_mc "Then no one interferes."
    show mc neut
    show sam neut
    cs_matsuda_fe_sa "Even me?"
    show sam neut
    show mc neut
    cs_matsuda_fe_mc "Especially you."
    show mc neut
    show sam neut
    cs_matsuda_fe_sa "Understood."
    cs_matsuda_fe_sa "Try not to make me regret understanding."

    show sam neut at thide
    show mc neut at thide
    hide sam
    hide mc

    scene black with wipeleft_scene
    pause 0.5

    play music flight fadein 1.0
    scene bg battlefield01 with dissolve_scene_full
    show mc neut at t21
    show sam neut at t22
    cs_matsuda_fe_mc "First company, lock shields."
    cs_matsuda_fe_mc "Second company, hold until the red banner commits."
    show mc neut
    show sam neut
    cs_matsuda_fe_sa "West ridge is quiet."
    show sam neut
    show mc neut
    cs_matsuda_fe_mc "It will not stay quiet."

    show mc neut at thide
    show sam neut at thide
    hide mc
    hide sam

    show matsuda neut at t21
    show tsubaki neut at t22
    cs_matsuda_fe_ma "Center forward at walking pace."
    cs_matsuda_fe_ma "Let him see discipline. Let him wonder how much of it is real."
    show matsuda neut
    show tsubaki neut
    cs_matsuda_fe_ts "Wagons are moving behind their reserve."
    show tsubaki neut
    show matsuda neut
    cs_matsuda_fe_ma "He moved the prisoners."
    show matsuda neut
    show tsubaki neut
    cs_matsuda_fe_ts "That's good, isn't it?"
    show tsubaki neut
    show matsuda neut
    cs_matsuda_fe_ma "It means he still has a conscience."
    cs_matsuda_fe_ma "It also means he knows exactly how to hurt us without using them."

    show matsuda neut at thide
    show tsubaki neut at thide
    hide matsuda
    hide tsubaki

    stop music fadeout 0.8
    play music devoted fadein 0.5
    play sound "mod_assets/sfx/sfx-longwoosh.wav"
    with hpunch

    show cs_matsuda_captain at t11
    cs_matsuda_captain "Arrows!"
    show cs_matsuda_captain at thide
    hide cs_matsuda_captain

    show mc neut at t21
    show sam neut at t22
    cs_matsuda_fe_mc "Shields up!"
    show mc neut
    show sam neut
    cs_matsuda_fe_sa "Red center is bending."
    show sam neut
    show mc neut
    cs_matsuda_fe_mc "Because she wants me to push."
    cs_matsuda_fe_mc "Hold."

    show mc neut at thide
    show sam neut at thide
    hide mc
    hide sam

    show matsuda neut at t21
    show tsubaki neut at t22
    cs_matsuda_fe_ma "Gary, take the ravine."
    cs_matsuda_fe_ma "Leif, west ridge on my horn."
    show matsuda neut
    show tsubaki neut
    cs_matsuda_fe_ts "The first wounded are coming through."
    show tsubaki neut
    show matsuda neut
    cs_matsuda_fe_ma "Treat only who can move."
    show matsuda neut
    show tsubaki neut
    cs_matsuda_fe_ts "I hate that order."
    show tsubaki neut
    show matsuda neut
    cs_matsuda_fe_ma "So do I."

    show gary at t31
    show matsuda neut at t32
    show tsubaki neut at t33
    cs_matsuda_gary "Ravine unit ready."
    show gary at thide
    hide gary
    show matsuda neut at t21
    show tsubaki neut at t22
    cs_matsuda_fe_ma "Go."
    show matsuda neut at thide
    show tsubaki neut at thide
    hide matsuda
    hide tsubaki

    play sound "mod_assets/sfx/sfx-shing.wav"
    show white zorder 200:
        alpha 0.45
        linear 0.18 alpha 0.0
    with hpunch
    pause 0.25
    hide white

    show leif at t21
    cs_matsuda_leif "West ridge taken."
    cs_matsuda_leif "Their rear is turning."
    show leif at thide
    hide leif

    show sam neut at t21
    cs_matsuda_fe_sa "Found you."
    cs_matsuda_fe_sa "Third company, with me."
    show sam neut at thide
    hide sam

    play sound "mod_assets/sfx/sfx-wham.wav"
    with vpunch

    show cs_matsuda_scout at t11
    cs_matsuda_scout "Berserker on the west ridge!"
    cs_matsuda_scout "Leif's riders are breaking!"
    show cs_matsuda_scout at thide
    hide cs_matsuda_scout

    show matsuda neut at t21
    show tsubaki neut at t22
    cs_matsuda_fe_ma "Gregor, hold the left."
    show matsuda neut
    show tsubaki neut
    cs_matsuda_fe_ts "Sam is cutting toward Leif."
    show tsubaki neut
    show matsuda neut
    cs_matsuda_fe_ma "I see him."
    cs_matsuda_fe_ma "Gregor holds until I give the horn."

    show gregor at t31
    show matsuda neut at t32
    show tsubaki neut at t33
    cs_matsuda_gregor "Gregor hears west dying."
    cs_matsuda_gregor "Gregor does not hold."
    show gregor at thide
    hide gregor

    show matsuda neut at t21
    show tsubaki neut at t22
    cs_matsuda_fe_ma "Gregor!"
    play sound "mod_assets/sfx/sfx-shock.wav"
    with hpunch
    show matsuda neut
    show tsubaki neut
    cs_matsuda_fe_ts "Left wing is moving."
    show tsubaki neut
    show matsuda neut
    cs_matsuda_fe_ma "Then the center has no hinge."
    cs_matsuda_fe_ma "Gary has minutes."

    show gary at t31
    show matsuda neut at t32
    show tsubaki neut at t33
    cs_matsuda_gary "Prisoners are free, but the reserve is coming back on us."
    show gary at thide
    hide gary
    show matsuda neut at t21
    show tsubaki neut at t22
    cs_matsuda_fe_ma "Take them north."
    show matsuda neut
    show tsubaki neut
    cs_matsuda_fe_ts "Matsuda, if Gary leaves, our retreat closes."
    show tsubaki neut
    show matsuda neut
    cs_matsuda_fe_ma "Then we buy him the road."
    show matsuda neut
    show tsubaki neut
    cs_matsuda_fe_ts "We?"
    show tsubaki neut
    show matsuda neut
    cs_matsuda_fe_ma "Stay close."

    play sound "mod_assets/sfx/sfx-fwashing.wav"
    show white zorder 200:
        alpha 0.5
        linear 0.12 alpha 0.0
    with hpunch
    pause 0.25
    hide white

    show matsuda neut
    show tsubaki neut
    cs_matsuda_fe_ts "Matsuda..."
    cs_matsuda_fe_ts "Don't turn around yet."
    show tsubaki neut
    show matsuda neut
    cs_matsuda_fe_ma "Tsubaki?"
    show matsuda neut
    show tsubaki neut
    cs_matsuda_fe_ts "I think I need you to be calm."
    show tsubaki neut
    show matsuda neut
    cs_matsuda_fe_ma "Medic!"

    show cs_matsuda_medic at t31
    show matsuda neut at t32
    show tsubaki neut at t33
    cs_matsuda_medic "My lady, the shaft is deep."
    show cs_matsuda_medic at thide
    hide cs_matsuda_medic

    show matsuda neut at t21
    show tsubaki neut at t22
    cs_matsuda_fe_ma "Then cut it short and move her."
    show matsuda neut
    show tsubaki neut
    cs_matsuda_fe_ts "No."
    cs_matsuda_fe_ts "If you move me, you lose two hands and gain a body to carry."
    show tsubaki neut
    show matsuda neut
    cs_matsuda_fe_ma "Do not make command decisions from the ground."
    show matsuda neut
    show tsubaki neut
    cs_matsuda_fe_ts "Then stop teaching me by example."
    show tsubaki neut
    show matsuda neut
    cs_matsuda_fe_ma "Tsubaki."
    show matsuda neut
    show tsubaki neut
    cs_matsuda_fe_ts "Gary needs the road."
    cs_matsuda_fe_ts "You said that was why we came."
    show tsubaki neut
    pause 0.4
    show tsubaki neut at thide
    hide tsubaki

    show matsuda neut at t11
    cs_matsuda_fe_ma "Medic, stay with her."
    cs_matsuda_fe_ma "If she speaks again, listen."

    show sam neut at t21
    show matsuda neut at t22
    cs_matsuda_fe_sa "Matsuda Akai."
    show sam neut
    show matsuda neut
    cs_matsuda_fe_ma "Not now."
    show matsuda neut
    show sam neut
    cs_matsuda_fe_sa "The ridge is lost. Your left is loose. If you fall, this ends."
    show sam neut
    show matsuda neut
    cs_matsuda_fe_ma "If I fall, it ends badly for you."
    show matsuda neut
    show sam neut
    cs_matsuda_fe_sa "I can live with that risk."
    show sam neut
    show matsuda neut
    cs_matsuda_fe_ma "No."
    cs_matsuda_fe_ma "You cannot."

    play sound "mod_assets/sfx/sfx-swing.wav"
    show white zorder 200:
        alpha 0.35
        linear 0.10 alpha 0.0
    with hpunch
    pause 0.18
    hide white
    play sound "mod_assets/sfx/sfx-stab.wav"
    show white zorder 200:
        alpha 0.65
        linear 0.18 alpha 0.0
    with vpunch
    pause 0.25
    hide white

    show sam neut
    show matsuda neut
    cs_matsuda_fe_sa "Tell him I held the ridge."
    show sam neut
    show matsuda neut
    cs_matsuda_fe_ma "He knows."
    show matsuda neut
    show sam neut
    cs_matsuda_fe_sa "Tell him anyway."
    show sam neut at thide
    hide sam

    show matsuda neut at t11
    cs_matsuda_fe_ma "I will."

    scene black with wipeleft_scene
    pause 0.5

    scene bg battlefield01 with dissolve_scene_full
    show mc neut at t21
    show matsuda neut at t22
    cs_matsuda_fe_mc "Where is Sam?"
    show mc neut
    show matsuda neut
    cs_matsuda_fe_ma "The west ridge."
    cs_matsuda_fe_ma "He held it."
    show matsuda neut
    show mc neut
    cs_matsuda_fe_mc "And Tsubaki?"
    show mc neut
    show matsuda neut
    cs_matsuda_fe_ma "The center."
    cs_matsuda_fe_ma "She held it."
    show matsuda neut
    show mc neut
    cs_matsuda_fe_mc "Then order the retreat."
    show mc neut
    show matsuda neut
    cs_matsuda_fe_ma "I freed the prisoners."
    show matsuda neut
    show mc neut
    cs_matsuda_fe_mc "And lost your road."
    show mc neut
    show matsuda neut
    cs_matsuda_fe_ma "You moved the wagons."
    show matsuda neut
    show mc neut
    cs_matsuda_fe_mc "I would not win that way."
    show mc neut
    show matsuda neut
    cs_matsuda_fe_ma "No."
    cs_matsuda_fe_ma "You found a cleaner knife."
    show matsuda neut
    show mc neut
    cs_matsuda_fe_mc "Matsuda."
    show mc neut
    show matsuda neut
    cs_matsuda_fe_ma "If either of us steps back now, our soldiers keep dying to prove we meant it."
    show matsuda neut
    show mc neut
    cs_matsuda_fe_mc "Then this is command?"
    show mc neut
    show matsuda neut
    cs_matsuda_fe_ma "This is what remains of it."

    stop music fadeout 1.0
    scene black with dissolve_scene_full
    pause 0.8

    play music devoted fadein 0.6
    scene cg campaign with dissolve_scene_full
    pause 0.8
    window auto

    cs_matsuda_fe_mc "Your line is broken."
    cs_matsuda_fe_ma "Your cavalry is spent."
    cs_matsuda_fe_mc "My blade reaches farther from horseback."
    cs_matsuda_fe_ma "Your horse is tired."
    cs_matsuda_fe_mc "You are bleeding."
    cs_matsuda_fe_ma "So are you."
    cs_matsuda_fe_mc "I can still offer quarter."
    cs_matsuda_fe_ma "And I can still refuse it."
    cs_matsuda_fe_mc "For pride?"
    cs_matsuda_fe_ma "For Gary, who is running north with children in prison coats."
    cs_matsuda_fe_ma "For Gregor, who broke too early because he could not bear another order that sounded like waiting."
    cs_matsuda_fe_ma "For Tsubaki, who asked me to remember why we came."
    cs_matsuda_fe_mc "For Sam, who trusted me to end this before he had to die on a ridge."
    cs_matsuda_fe_ma "Then end it."
    cs_matsuda_fe_mc "I do not want to kill you."
    cs_matsuda_fe_ma "Good."
    cs_matsuda_fe_ma "Hesitation is the only advantage I have left."

    play sound "mod_assets/sfx/sfx-shing.wav"
    show white zorder 200:
        alpha 0.45
        linear 0.20 alpha 0.0
    with hpunch
    pause 0.25
    hide white

    cs_matsuda_fe_ma "Again."
    cs_matsuda_fe_mc "Your guard is open."
    cs_matsuda_fe_ma "Then take it."

    play sound "mod_assets/sfx/sfx-swing.wav"
    with hpunch
    pause 0.2
    play sound "mod_assets/sfx/sfx-stab2.wav"
    show white zorder 200:
        alpha 0.65
        linear 0.20 alpha 0.0
    with vpunch
    pause 0.4
    hide white

    cs_matsuda_fe_mc "..."
    cs_matsuda_fe_ma "..."
    cs_matsuda_fe_mc "My sword is at your throat."
    cs_matsuda_fe_ma "Mine is under your ribs."
    cs_matsuda_fe_mc "A draw."
    cs_matsuda_fe_ma "A draw."
    cs_matsuda_fe_mc "All of this for a draw."
    cs_matsuda_fe_ma "No."
    cs_matsuda_fe_ma "All of this, and the draw is what survived."

    stop music fadeout 2.0
    scene black with dissolve_scene_full
    pause 1.5

    hide screen cs_matsuda_fe_stage_overlay
    play music dailyleisure fadein 1.0
    scene bg living_room with dissolve_scene_full
    show matsuda neut at t41
    show mc neut at t42
    show tsubaki neut at t43
    show sam neut at t44

    ma "...A draw."
    show matsuda neut
    show sam neut
    sa "You're keeping the roll?"
    show sam neut
    show matsuda neut
    ma "His attack hits. My counter hits. Neither has enough health left to stand after the exchange."
    show matsuda neut
    show mc neut
    mc "The die is leaning against the notebook."
    show mc neut
    show matsuda neut
    ma "The die is legible."
    show matsuda neut
    show tsubaki neut
    ts "My cleric still dies?"
    show tsubaki neut
    show matsuda neut
    ma "She lives if the medic reaches her before the epilogue."
    show matsuda neut
    show tsubaki neut
    ts "That is not an answer."
    show tsubaki neut
    show matsuda neut
    ma "It is a promise to roll for it where everyone can see."
    show matsuda neut
    show sam neut
    sa "And my berserker?"
    show sam neut
    show matsuda neut
    ma "Dead."
    show matsuda neut
    show sam neut
    sa "Naturally."
    show sam neut
    show mc neut
    mc "It fits, though."
    mc "Neither commander wins. Both armies have to live with what they spent."
    show mc neut
    show matsuda neut
    ma "Exactly."
    ma "Dead Fantasy is not about the crown changing hands."
    ma "It is about what the field asks for before it lets anyone leave."
    show matsuda neut
    show tsubaki neut
    ts "That sounds like something you decided after seeing the roll."
    show tsubaki neut
    show matsuda neut
    ma "Half of running a campaign is knowing when the dice have written a better ending than you did."
    show matsuda neut
    show sam neut
    sa "I still want the runback."
    show sam neut
    show matsuda neut
    ma "You may have the sequel."
    ma "But next time, if you charge a ridge alone, I am not accepting complaints."
    show matsuda neut
    show sam neut
    sa "I accept nothing."
    show sam neut
    show tsubaki neut
    ts "Can the sequel start after snacks?"
    show tsubaki neut
    show mc neut
    mc "Seconded."
    show mc neut
    show matsuda neut
    ma "Fine."
    ma "Snacks first. Epilogue after."
    show matsuda neut
    show tsubaki neut
    ts "And the medic roll."
    show tsubaki neut
    show matsuda neut
    ma "And the medic roll."

    stop music fadeout 2.0
    scene black with dissolve_scene_full
    pause 1.5

    $ persistent.cs_matsuda_01_unlocked = True
    return
