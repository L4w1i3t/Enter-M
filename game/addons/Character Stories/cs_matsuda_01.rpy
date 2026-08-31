# =============================================================================
# cs_matsuda_01.rpy  --  Matsuda character story 01, "Dead Fantasy"
# =============================================================================
#
# A full Fire Emblem-style war chapter, staged like a play and played completely
# straight...right up until the camera pulls back and it turns out to be a
# tabletop campaign Matsuda is running for the friend group on a Saturday night.
#
# The battle is earnest ON PURPOSE -- the parody lives in the reveal. The war
# scenes are written plain: tired people, logistics, etc. There is
# NO external narrator -- every piece of scene-setting is carried by dialogue,
# phase cards, staging, music, or SFX (FE-style: show, don't tell). The field is
# spatially legible, each reversal follows from a prior order, and every major
# unit gets a battle conversation or a death beat. The tells are behavioral, not
# winking, so the living-room turn reads as "it was visible the whole time"
# instead of a cheat:
#   - Gregor talks about himself in the third person (Asahina "in character"),
#     and drops it exactly once -- the moment he breaks.
#   - Gary is slightly over-written and over-prepared (Monika's PC; she wrote
#     him a letter, a mother, a month of counting wagons).
#   - Akai, the commander, is improbably central and never quite dies, and is
#     given the GM's own surname, Akai. Her snark bleeds through under stress,
#     and she gets a brooding solo scene nobody else gets.
#   - Akai thinks of her people as "pieces on the table."
#   - Weather changes the map because Matsuda actually built a weather system.
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
#   hotr             -> Akai's map council. Fades to silence for Akai's solo beat.
#   fantasypassion   -> the rival's fortress and mirror council.
#   flight           -> field parley, deployment, and the opening feints.
#   epicbattlephase1 -> battle joined: ravine rescue through the ridge reversal.
#   devoted          -> the storm turn and collapse of the center.
#   (hard stop)      -> the instant Tsubaki is hit; her death plays dry.
#   hopeless         -> Sam intercepts Akai; his death.
#   devoted          -> the two commanders meet; carries through the duel parley.
#   epicbattlephase2 -> the duel itself, first clash on.
#   (hard stop)      -> the simultaneous final strike. The table names the draw.
#   enterm           -> THE TABLE reveal. Cut by Monika's palm hitting the table.
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
#   Bit-part NPCs (Captain/Scout/Medic/Soldiers) are voice-only. Every named
#   battlefield role uses a purpose-built medieval sprite from def_characters.
#   Sprite placement uses the shared t11/t21/... position transforms (transforms.rpy).
#   screen cs_matsuda_fe_phase_card(...) supplies FE-like chapter/phase cards.
#
#   STRUCTURE: I. Akai's map council -> II. rival mirror council -> III. field
#   parley/deployment -> IV. center feint + ravine rescue -> V. west-ridge
#   reversal -> VI. storm/center collapse -> VII. Akai vs. Sam -> VIII. Akai vs.
#   MC -> IX. THE TABLE, where the overlay is hidden and the "battle" is revealed
#   as Matsuda's tabletop campaign (the cs_fe_* cast snap back to ma/sa/ah/ts/m/mc).
#   The table tears itself apart over the draw until Monika forces the ignored
#   medic roll; the group then argues its way back to shared ownership.
#
#   ON COMPLETION: persistent.cs_matsuda_01_unlocked = True, then return.
# =============================================================================

define cs_fe_akai    = Character("Akai", image="df_akai", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say", statement_name="say-custom")
define cs_fe_rival   = Character("MC", image="df_rival", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say", statement_name="say-custom")
define cs_fe_sam     = Character("Sam", image="df_sam", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say", statement_name="say-custom")
define cs_fe_ts      = Character("Tsubaki", image="df_tsubaki", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say", statement_name="say-custom")
define cs_fe_gary    = Character("Gary", image="gary", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say", statement_name="say-custom")
define cs_fe_gregor  = Character("Gregor", image="gregor", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say", statement_name="say-custom")
define cs_fe_leif    = Character("Leif", image="leif", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say", statement_name="say-custom")
define cs_fe_captain = Character("Captain", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say", statement_name="say-custom")
define cs_fe_scout   = Character("Scout", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say", statement_name="say-custom")
define cs_fe_medic   = Character("Medic", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say", statement_name="say-custom")
define cs_fe_soldier = Character("Soldier", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say", statement_name="say-custom")
define cs_fe_rider   = Character("Rider", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say", statement_name="say-custom")
define cs_fe_guard   = Character("Wagon Guard", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed", screen="cs_matsuda_fe_say", statement_name="say-custom")

screen cs_matsuda_fe_stage_overlay():
    zorder -20

    add Solid("#06060624") xysize (1280, 720)
    add Solid("#00000040") xpos 0 ypos 0 xysize (1280, 36)
    add Solid("#00000036") xpos 0 ypos 668 xysize (1280, 52)
    add Solid("#00000030") xpos 0 ypos 0 xysize (42, 720)
    add Solid("#00000030") xpos 1238 ypos 0 xysize (42, 720)
    add Solid("#8b7a5530") xpos 54 ypos 56 xysize (1, 590)
    add Solid("#8b7a5530") xpos 1225 ypos 56 xysize (1, 590)

screen cs_matsuda_fe_phase_card(kicker, title, objective=None):
    zorder 180

    add Solid("#03070de8")
    add Solid("#b7a46b") xpos 180 ypos 196 xysize (920, 3)
    add Solid("#b7a46b") xpos 180 ypos 502 xysize (920, 3)

    vbox:
        xalign 0.5
        yalign 0.49
        spacing 16

        text kicker:
            xalign 0.5
            size 22
            color "#d2bf82"
            kerning 3

        text title:
            xalign 0.5
            size 48
            bold True
            color "#f2f1e8"
            outlines [(2, "#000000", 1, 1)]

        if objective:
            null height 10
            text objective:
                xalign 0.5
                size 24
                color "#b8c9df"

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
    show screen cs_matsuda_fe_phase_card(
        "DEAD FANTASY",
        "GREYWAKE FIELD",
        "OBJECTIVE: FREE THE CAPTIVES AND ESCAPE NORTH"
    )
    with dissolve
    pause 2.2
    hide screen cs_matsuda_fe_phase_card
    with dissolve
    pause 0.5

    # ------------------------------------------------------------------ #
    # I. Akai's map council
    # ------------------------------------------------------------------ #
    play music hotr
    scene bg castle01_strategyroom_night with dissolve_scene_full

    show df_akai at t11
    cs_fe_captain "Commander. The north scout came back without his horse."
    cs_fe_akai "Then the horse knew something first. Say it."
    cs_fe_captain "The storm crossed Lake Orra an hour ago. Snow is already on the upper road."
    cs_fe_captain "By first light, Greywake Pass will take a wheel. By noon, it will take an army."
    cs_fe_akai "And the eastern track?"
    cs_fe_captain "Flooded. The thaw broke the bank below the ravine."
    cs_fe_akai "So the pass is the only road north."
    cs_fe_captain "Yes, Commander."
    cs_fe_akai "How many people in the wagons?"
    cs_fe_captain "Forty by the last count. Mostly families from the border villages."
    cs_fe_akai "Forty reasons not to wait for weather. Get the officers."
    cs_fe_captain "All of them?"
    cs_fe_akai "If one chair is empty, drag whoever owns it in with the chair."
    pause 0.5

    show df_akai at t11
    cs_fe_akai "Greywake is a bowl with one door. We are standing at the southern lip."
    cs_fe_akai "The Rival holds the center road. His left touches the old ford. His right climbs the west ridge."
    cs_fe_akai "The prisoner wagons sit behind his line. The north pass sits behind the wagons."
    cs_fe_akai "At dawn, the storm shuts that pass. If we are still south of it, winter finishes what his army starts."
    cs_fe_akai "If the wagons are still south of it, those forty people do not get another chance."
    cs_fe_akai "So we go before the moon clears the ridge. We cut the wagons loose, put them on the north road, and follow if the field permits."
    cs_fe_akai "The field probably won't. Plan for that version."

    show gary at l21
    show df_akai at t22
    cs_fe_gary "The eastern ravine reaches behind their reserve."
    cs_fe_akai "In single file, with a bad drop on one side."
    cs_fe_gary "I have twelve riders who can make it."
    cs_fe_akai "You had sixteen yesterday."
    cs_fe_gary "Four cannot ride quietly. I need quiet more than I need four."
    cs_fe_akai "The third wagon."
    cs_fe_gary "My mother."
    cs_fe_gary "My sisters are in the fourth, unless they moved the sick forward again."
    cs_fe_gary "I've counted those wagons every day for a month. Same hill. Same glass. Same hour."
    cs_fe_gary "Third and fourth leave ruts deeper on the right. Sixth has a cracked rear rim. The lead driver favors his left shoulder."
    cs_fe_akai "You counted the driver."
    cs_fe_gary "I ran out of wagons."
    cs_fe_akai "Good. Get into the ravine before our center advances. Do not attack until you see the red flare."
    cs_fe_gary "And if the wagons move?"
    cs_fe_akai "You are the man who counted the driver's shoulders. Find them."
    cs_fe_gary "...There's a letter in my tent."
    cs_fe_akai "No."
    cs_fe_gary "You haven't heard what it says."
    cs_fe_akai "It says nobody is to follow you, your death was your own choice, and you would like the last word because dying apparently isn't dramatic enough."
    cs_fe_gary "It says it better."
    cs_fe_akai "Burn it."
    cs_fe_gary "Commander--"
    cs_fe_akai "You get the ravine. You get twelve riders. You get your family."
    cs_fe_akai "You do not get to leave me instructions for how to fail you. Burn the letter."
    cs_fe_gary "...Taken."
    cs_fe_akai "Once the wagons turn north, you do not come back for us."
    cs_fe_gary "If your center is still standing--"
    cs_fe_akai "You do not come back."
    cs_fe_gary "...Taken twice."
    show gary at thide
    hide gary

    show gregor at l21
    show df_akai at t22
    cs_fe_gregor "Gregor has the old ford."
    cs_fe_akai "Gregor has the whole left."
    cs_fe_gregor "The whole left is a longer sentence."
    cs_fe_akai "Three shield companies. Pikes behind them. You plant at the ford and hold until my long horn."
    cs_fe_gregor "How long between the first arrow and the horn?"
    cs_fe_akai "If Gary finds the wagons where they were, forty minutes."
    cs_fe_gregor "And if he does not?"
    cs_fe_akai "Longer."
    cs_fe_gregor "At Varn's Crossing, Gregor held longer."
    cs_fe_gregor "Gregor stood in the wall and listened to his friends' voices stop one at a time."
    cs_fe_gregor "Eleven voices. Gregor still knows the order."
    cs_fe_akai "I know. I was there."
    cs_fe_gregor "Then Commander knows what she is putting back in Gregor's ears."
    cs_fe_akai "I do."
    cs_fe_gregor "And she asks anyway."
    cs_fe_akai "I ask because you're the only man on this field I trust to know the difference between breaking and bending."
    cs_fe_akai "The center can bend. The left cannot. If the ford opens, their reserve cuts Gary off from the pass."
    cs_fe_gregor "The left will hold until the long horn."
    cs_fe_akai "Even if the ridge calls for you."
    cs_fe_gregor "Even then."
    cs_fe_akai "Even if Leif calls for you."
    cs_fe_gregor "..."
    cs_fe_gregor "Gregor gives his word. Gregor has never broken it."
    cs_fe_gregor "Do not make the horn late, Commander. Gregor asks one thing."
    cs_fe_akai "I heard you."
    show gregor at thide
    hide gregor

    show leif at l21
    show df_akai at t22
    cs_fe_leif "Now tell me the west ridge is mine."
    cs_fe_akai "The west ridge is borrowed."
    cs_fe_leif "Borrowed things come back with scratches."
    cs_fe_akai "That hill comes back without you if you mistake it for a throne."
    cs_fe_leif "Their supply road runs under it. Fifty riders on top and their whole rear turns sideways."
    cs_fe_akai "Forty-eight riders. Gary took twelve of your quietest."
    cs_fe_leif "Gary takes my riders, Gregor takes my glory, and you leave me a hill."
    cs_fe_akai "I leave you the berserker."
    cs_fe_leif "Ah. So you did bring a gift."
    cs_fe_akai "Sam held the Salt Gate alone for half a day. He broke two lances with his ribs and killed the men carrying them."
    cs_fe_leif "Stories gain a corpse every time they cross a campfire."
    cs_fe_akai "This story started with enough."
    cs_fe_akai "You wait for my horn. You climb fast. You show his reserve your banner."
    cs_fe_akai "The instant they turn, you come down the north face and rejoin the center. Take the ridge. Do not keep it."
    cs_fe_leif "Take it. Turn them. Leave it."
    cs_fe_akai "Say the last part like you believe it."
    cs_fe_leif "Leave it."
    cs_fe_akai "And if Sam reaches you before the horn?"
    cs_fe_leif "Then he learns the difference between a story and a cavalry charge."
    cs_fe_akai "Leif."
    cs_fe_leif "Then I leave the ridge faster than he can take it."
    cs_fe_akai "Better."
    show leif at thide
    hide leif

    # Akai and the cleric -- the emotional spine of the campaign.
    show df_tsubaki at t21
    show df_akai at t22
    cs_fe_ts "One rider under a white branch."
    cs_fe_akai "No."
    cs_fe_ts "You said officers could challenge the plan."
    cs_fe_akai "You challenged it. I remain deeply moved."
    cs_fe_ts "Send terms again."
    cs_fe_akai "We sent them yesterday. He formed ranks while our herald was still speaking."
    cs_fe_ts "He also moved his archers out of range until the herald came back."
    cs_fe_akai "Courtesy is not surrender."
    cs_fe_ts "No. It is one reason to ask twice."
    cs_fe_ts "At midnight, when I am deciding which man gets the last clean bandage, I want to know we asked twice."
    cs_fe_akai "The ravine floods higher every hour. The pass closes at dawn. I cannot buy your conscience an hour with forty lives."
    cs_fe_ts "I know."
    cs_fe_akai "Do you?"
    cs_fe_ts "I know the arithmetic. I just hate when you use it as though hating it makes me slow."
    cs_fe_akai "..."
    cs_fe_ts "One minute, then. Across the field before the first arrow. Make him say no where everyone can hear it."
    cs_fe_akai "One minute. No rider. We ask from the line."
    cs_fe_ts "Twice is twice."
    cs_fe_akai "You will be behind the center."
    cs_fe_ts "Behind you I can reach the middle and nothing else. If the ford goes--"
    cs_fe_akai "If the ford goes, there is no field left to heal."
    cs_fe_ts "Put me between the center and Gregor."
    cs_fe_akai "Behind me, I know where you are."
    cs_fe_ts "..."
    cs_fe_ts "You would never accept that reason from me."
    cs_fe_akai "No."
    cs_fe_ts "Then do not dress it as tactics."
    cs_fe_akai "Fine. It is not tactics."
    cs_fe_akai "I am putting you behind me because I have spent six years learning the sound of your steps."
    cs_fe_akai "Tonight I will have a thousand sounds to count. I need one of them to stay where I left it."
    cs_fe_ts "And if you are the one on the ground?"
    cs_fe_akai "Then I finally learn what you say to people who ignore instructions."
    cs_fe_ts "That is still not an answer."
    cs_fe_akai "It is still the one I have."
    cs_fe_ts "If the center breaks, I go north with Gary."
    cs_fe_akai "Without arguing."
    cs_fe_ts "I reserve the right to argue while moving north."
    cs_fe_akai "Granted."
    show df_tsubaki at thide
    hide df_tsubaki

    show df_akai at t11
    cs_fe_captain "And the center, Commander?"
    cs_fe_akai "Walk forward under shields. Give ground on the first hard push."
    cs_fe_captain "A false break."
    cs_fe_akai "A believable one. Let him think he can split us before the horn."
    cs_fe_captain "The Rival does not chase easily."
    cs_fe_akai "Everyone chases something. We find his."
    cs_fe_captain "If he holds?"
    cs_fe_akai "We make the bend deeper until holding frightens him more than following."
    cs_fe_captain "If Gregor leaves the ford?"
    cs_fe_akai "He will not."
    cs_fe_captain "If the horn must sound early?"
    cs_fe_akai "Leif climbs. The center turns north. Gary does not come back."
    cs_fe_captain "And if the north road closes behind Gary?"
    cs_fe_akai "Then those forty people live somewhere we do not."
    cs_fe_captain "...Understood."

    cs_fe_akai "Officers, look at the map."
    cs_fe_akai "The center is not the objective. The enemy commander is not the objective."
    cs_fe_akai "Those wagons are the objective. Every glorious thing you imagine doing tonight is noise unless those wheels turn north."
    cs_fe_akai "Bring the pieces back if you can. Bring the people back even if you cannot."
    cs_fe_akai "Take your units. Check every strap, every shoe, every torch hood."
    cs_fe_akai "We move in twenty minutes."
    pause 0.5
    show df_akai at thide
    hide df_akai

    # The commander, alone. The music leaves with the officers.
    stop music fadeout 2.0
    pause 1.0

    show df_akai at t11
    cs_fe_akai "Twelve hours."
    cs_fe_akai "Twelve hours ago, every piece was still on this table."
    cs_fe_akai "Gary at the ravine. Gregor at the ford. Leif on the ridge. Tsubaki behind the center."
    cs_fe_akai "Move them correctly and forty people go home."
    cs_fe_akai "Move one of them wrong and the board learns how much a name weighs."
    cs_fe_akai "...Twelve hours, and every piece back on this table."
    cs_fe_akai "That is all I am asking."
    cs_fe_akai "...I do not even know who I am asking."
    show df_akai at thide
    hide df_akai

    scene black with wipeleft_scene
    pause 0.8

    # ------------------------------------------------------------------ #
    # II. The rival's mirror council
    # ------------------------------------------------------------------ #
    play music fantasypassion
    scene bg greywake_rival_keep with dissolve_scene_full

    show df_rival at t21
    show df_sam at t22
    cs_fe_sam "Six owners in ten years, this fortress, and not one bothered to hang a flag."
    cs_fe_sam "Now we're about to bleed for a building that refuses to admit whose side it is on."
    cs_fe_rival "We're not holding the fortress."
    cs_fe_sam "I noticed. The men are outside, where the weather can kill them honestly."
    cs_fe_rival "How long until the storm?"
    cs_fe_sam "The quartermaster says dawn. His left knee says sooner. I trust the knee."
    cs_fe_rival "So does Akai. She moves tonight."
    cs_fe_sam "Good. Waiting is the only thing on this field that has ever scared me."
    cs_fe_rival "Her goal is not this fortress."
    cs_fe_sam "No. It's the wagons."
    cs_fe_rival "And the road behind them. She has one night to reach both."
    cs_fe_sam "Which means she has no room to be clever."
    cs_fe_rival "Akai makes room. That is the clever part."

    cs_fe_guard "Commander, the prisoner detail is ready for inspection."
    cs_fe_rival "New order. Move every wagon behind the reserve. Use the north spur."
    cs_fe_guard "Behind the reserve?"
    cs_fe_rival "Before moonrise. Cover the lamps and take the bells off the harness."
    cs_fe_guard "The general's written order places them behind our center, sir."
    cs_fe_rival "The general is three days south and the people in those wagons are here. Move them."
    cs_fe_guard "Yes, Commander."

    cs_fe_sam "You're moving the best card in your hand where she cannot see it."
    cs_fe_rival "They're not a card."
    cs_fe_sam "To Akai they are the whole game. Leave them behind our line and she breaks her own formation reaching for them."
    cs_fe_sam "We win before the first spear touches."
    cs_fe_rival "Somebody's mother is sitting in the third wagon with her wrists tied."
    cs_fe_rival "I'm not leaving her where forty archers can turn her into an argument."
    cs_fe_sam "You were ordered to hold them."
    cs_fe_rival "I will hold them. I was not ordered to hang them from our shield wall."
    cs_fe_sam "It is still the strongest card you have."
    cs_fe_rival "Then I'll win holding a worse one."
    cs_fe_sam "Or lose beautifully."
    cs_fe_rival "If beauty survives, it can write the report."
    cs_fe_sam "Hah."
    cs_fe_sam "This is why the men like you. It is inconvenient as all hell."

    cs_fe_rival "Look at the center."
    cs_fe_sam "I am looking."
    cs_fe_rival "She advances under shields, bows backward, and invites us into the bowl."
    cs_fe_sam "Then we push until the bow snaps."
    cs_fe_rival "No. We stop."
    cs_fe_sam "We stop while she retreats?"
    cs_fe_rival "Akai does not retreat in a straight line. Her wings will be waiting for us to lean."
    cs_fe_rival "Our center takes the arrows and stays where it is. No pursuit without my horn."
    cs_fe_sam "She'll deepen the bend."
    cs_fe_rival "Let her."
    cs_fe_sam "She'll make it ugly enough that the captains move on instinct."
    cs_fe_rival "Then remind them instinct is how wolves enter a fence."

    cs_fe_rival "Her left goes to Gregor."
    cs_fe_sam "The man who talks about himself like somebody already carved the memorial."
    cs_fe_rival "He anchors the old ford. We do not spend ourselves there."
    cs_fe_rival "Press him. Make him hear the ridge. Do not give him a reason to stop listening."
    cs_fe_sam "And the ridge goes to Leif."
    cs_fe_rival "Forty-eight riders. Fast enough to turn our reserve if they reach the crest."
    cs_fe_sam "So I wait on the reverse slope."
    cs_fe_rival "Below the crest. No fires. No steel above the grass. Let him believe he arrived first."
    cs_fe_sam "Cavalry comes up. I take the cavalry."
    cs_fe_rival "Then whatever leaves Gregor's line comes looking for you."
    cs_fe_sam "I take that too."
    cs_fe_rival "You delay it."
    cs_fe_sam "That is a delicate word for the work."
    cs_fe_rival "I need you alive when her center turns."
    cs_fe_sam "Need and receive have never been close relatives."
    cs_fe_rival "Try to introduce them."

    cs_fe_scout "Commander. Twelve riders left Akai's camp eastbound. No banner."
    cs_fe_rival "The ravine."
    cs_fe_sam "Send thirty and close it."
    cs_fe_rival "No."
    cs_fe_sam "No again. Excellent council."
    cs_fe_rival "If I strip thirty from the center, Akai knows we saw them."
    cs_fe_rival "Move the wagons. Put six guards at the ravine mouth and six with the drivers."
    cs_fe_sam "Twelve riders against twelve guards."
    cs_fe_rival "And a road they have studied for a month."
    cs_fe_sam "You almost sound like you want them through."
    cs_fe_rival "I want this field won without forty bound people crushed between it."
    cs_fe_sam "That is not an answer."
    cs_fe_rival "It is the one you get."

    cs_fe_sam "She'll ask terms before the first arrow."
    cs_fe_rival "Yesterday was not enough for her cleric."
    cs_fe_sam "You noticed the cleric?"
    cs_fe_rival "She stood beside the herald and watched our archers step back."
    cs_fe_sam "What do you tell them?"
    cs_fe_rival "Lay down arms. The army lives. The prisoners remain in custody."
    cs_fe_sam "So no."
    cs_fe_rival "So the only offer I am allowed to make."
    cs_fe_sam "And when Akai makes you say it in front of both armies?"
    cs_fe_rival "I say it without hiding behind the order."

    cs_fe_sam "One more thing."
    cs_fe_rival "The west ridge was not enough?"
    cs_fe_sam "If she gets through me. If all of this narrows until it is you and her in the mud."
    cs_fe_rival "Nobody steps in."
    cs_fe_sam "You knew what I was asking."
    cs_fe_rival "Nobody finishes it for me. Not the reserve. Not an archer. Not you."
    cs_fe_sam "Even if she has you on your knees?"
    cs_fe_rival "Especially then."
    cs_fe_sam "Stupid."
    cs_fe_rival "Probably."
    cs_fe_sam "All right. Your stupid thing is safe with me."
    cs_fe_rival "And yours?"
    cs_fe_sam "Mine is simple."
    cs_fe_sam "Do not make me climb down from a famous hill to avenge you."
    cs_fe_rival "Then do not make me climb it to find you."
    cs_fe_sam "No promises."
    cs_fe_rival "I know."
    show df_sam at thide
    show df_rival at thide
    hide df_sam
    hide df_rival

    stop music fadeout 1.0
    scene black with wipeleft_scene
    pause 0.8

    # ------------------------------------------------------------------ #
    # III. Greywake Field -- parley and deployment
    # ------------------------------------------------------------------ #
    play music flight
    show screen cs_matsuda_fe_phase_card(
        "BATTLE PREPARATIONS",
        "THE SECOND ASKING",
        "ENEMY COMMANDER: MC"
    )
    with dissolve
    pause 1.7
    hide screen cs_matsuda_fe_phase_card
    with dissolve
    scene bg greywake_field_dawn with dissolve_scene_full

    show df_rival at t21
    show df_sam at t22
    cs_fe_rival "First company locks shields. Second company does not move until their red banner moves."
    cs_fe_sam "Her whole army is on the southern rise."
    cs_fe_rival "Numbers?"
    cs_fe_sam "Enough to make counting feel pessimistic."
    cs_fe_rival "The ridge?"
    cs_fe_sam "Quiet. Leif has his riders below the skyline. He thinks we cannot see the dust."
    cs_fe_rival "Go before the branch goes up."
    cs_fe_sam "You want me gone for the talking?"
    cs_fe_rival "You have never improved talking."
    cs_fe_sam "A cruel command assessment."
    cs_fe_rival "Reverse slope. No steel above the grass."
    cs_fe_sam "And if I hear you agree to anything sensible?"
    cs_fe_rival "Assume a head wound."
    cs_fe_sam "There he is."
    show df_sam at thide
    hide df_sam

    cs_fe_scout "White branch in Akai's center!"
    cs_fe_rival "One minute. Bows stay down."
    cs_fe_soldier "Sir, the general's order--"
    cs_fe_rival "Will still be wrong in one minute. Lower them."
    pause 0.4
    show df_rival at thide
    hide df_rival

    show df_akai at t21
    show df_tsubaki at t22
    cs_fe_akai "Rival Commander! Greywake has heard enough steel being checked. Hear one offer before it hears the rest."
    cs_fe_rival "I hear you, Akai."
    cs_fe_akai "Release the forty people in your wagons. Open the north road until sunrise."
    cs_fe_akai "My army crosses without loosing an arrow. Your fortress, stores, and wounded remain untouched."
    cs_fe_rival "I cannot release prisoners placed in my charge."
    cs_fe_akai "Cannot, or will not?"
    cs_fe_rival "Both answers put me in the same uniform."
    cs_fe_akai "Then take it off."
    cs_fe_rival "Lay down your army's weapons. Your soldiers live. The prisoners remain in custody."
    cs_fe_akai "You offer my people their lives in exchange for leaving forty others in chains."
    cs_fe_rival "I offer what authority I have."
    cs_fe_akai "Borrow more."
    cs_fe_rival "You first."
    cs_fe_akai "..."
    cs_fe_rival "The wagons have been moved away from the line. Whatever happens next, I will not use them as cover."
    cs_fe_ts "He told us."
    cs_fe_akai "I heard."
    cs_fe_rival "If either of us still has a voice at dawn, ask me again."
    cs_fe_akai "At dawn, the pass is closed."
    cs_fe_rival "I know."
    cs_fe_akai "So do I."
    cs_fe_rival "Then we have reached the end of the minute."
    cs_fe_akai "We have."
    cs_fe_ts "...Twice."
    cs_fe_akai "Twice."

    cs_fe_akai "Branch down. Center, shields."
    cs_fe_rival "Bows up."
    cs_fe_ts "Medic line ready. Bandages on the outside of the bags. Nobody digs for anything once they start coming back."
    cs_fe_medic "And the ones who cannot walk?"
    cs_fe_ts "Two bearers if the bleeding can be stopped. One if it cannot. Mark the ones we leave and remember where."
    cs_fe_akai "Tsubaki."
    cs_fe_ts "I know the order."
    cs_fe_akai "Say it."
    cs_fe_ts "The ones who can walk come first."
    cs_fe_akai "And?"
    cs_fe_ts "I will hate you after."
    cs_fe_akai "After is acceptable."

    cs_fe_scout "Twelve riders entering the eastern ravine."
    cs_fe_akai "No flare until Gary confirms the wagons."
    cs_fe_scout "Leif is in place below the west ridge."
    cs_fe_akai "No horn until the flare."
    cs_fe_scout "Gregor's shields are set at the old ford."
    cs_fe_akai "Tell him I know what time it is."
    cs_fe_scout "Commander?"
    cs_fe_akai "Those words exactly."

    cs_fe_ts "The wagons are moving behind their reserve."
    cs_fe_akai "He kept his word."
    cs_fe_ts "That is good for them."
    cs_fe_akai "Yes."
    cs_fe_ts "You said that like it was bad for us."
    cs_fe_akai "It means he plans to beat me without hiding behind civilians."
    cs_fe_akai "And he might."
    cs_fe_ts "Do not worry. I will only repeat it if we live."
    cs_fe_akai "Your discretion remains inspiring."

    cs_fe_captain "Center awaits your word."
    cs_fe_akai "Walking pace. Let him count every shield."
    cs_fe_akai "First rank takes the road. Second leaves three steps. Third leaves five."
    cs_fe_captain "Make the gaps visible."
    cs_fe_akai "Make them tempting."
    cs_fe_captain "And when the arrows come?"
    cs_fe_akai "We keep walking."
    cs_fe_akai "Forward."
    show df_akai at thide
    show df_tsubaki at thide
    hide df_akai
    hide df_tsubaki

    # ------------------------------------------------------------------ #
    # IV. The center feint and the ravine rescue
    # ------------------------------------------------------------------ #
    stop music fadeout 0.6
    show screen cs_matsuda_fe_phase_card(
        "PLAYER PHASE",
        "BREAK THE WAGON LINE",
        "VICTORY: ALL FORTY CAPTIVES REACH THE NORTH ROAD"
    )
    with dissolve
    pause 1.5
    hide screen cs_matsuda_fe_phase_card
    with dissolve
    play music epicbattlephase1

    play sound audio.sfx_longwoosh
    with hpunch
    cs_fe_captain "ARROWS! First rank, roof your shields! Second rank, fill the gaps!"
    cs_fe_soldier "They found the seams!"
    cs_fe_captain "Then stop giving them seams! Lock left!"

    show df_rival at t21
    show df_akai at t22
    cs_fe_rival "Third bow line, shorten ten paces. Aim behind the shields."
    cs_fe_akai "Third rank, forward. Leave five steps and make them look accidental."
    cs_fe_rival "She widened the gap."
    cs_fe_akai "He shortened the range."
    cs_fe_rival "Do not enter it."
    cs_fe_akai "Make him want it."
    cs_fe_captain "Center, give ground! Keep your faces north!"
    cs_fe_soldier "They are not following!"
    cs_fe_akai "Then we bend farther."
    cs_fe_captain "Farther puts our rear in bow range."
    cs_fe_akai "I know where it puts us. Eight more steps."
    cs_fe_rival "Still bait. Shields hold. Nobody takes those eight steps."
    cs_fe_soldier "Commander, their line is breaking!"
    cs_fe_rival "No. It is opening a mouth. Keep your hand out of it."

    play sound audio.sfx_longwoosh
    with hpunch
    show df_tsubaki at t31
    show df_akai at t32
    show df_rival at t33
    cs_fe_captain "Second volley!"
    cs_fe_ts "Walking wounded to me! If you can curse, you can crawl!"
    cs_fe_medic "This one cannot feel his legs."
    cs_fe_ts "Mark the ground. Pressure on the wound. Walkers first."
    cs_fe_medic "He is asking for you."
    cs_fe_ts "Tell him I heard him. Tell him I am coming back."
    cs_fe_akai "Tsubaki."
    cs_fe_ts "I gave your order. Do not ask me to like the sound."
    cs_fe_akai "I was going to say the right is drifting."
    cs_fe_ts "Then say useful things faster."
    cs_fe_akai "Captain, close the right by two. Leave the center ugly."
    cs_fe_rival "She corrected the drift. She is still counting."
    cs_fe_rival "No pursuit. Let her spend men proving we are patient."
    show df_rival at thide
    show df_akai at thide
    show df_tsubaki at thide
    hide df_rival
    hide df_akai
    hide df_tsubaki

    scene bg greywake_ravine with dissolve
    show gary at t11
    cs_fe_rider "Ravine mouth. Six guards where the scout promised."
    cs_fe_gary "And no wagons."
    cs_fe_rider "We came for wagons."
    cs_fe_gary "The Rival moved them. Look down."
    cs_fe_rider "Three fresh ruts north. Maybe four. Rain chewed the rest."
    cs_fe_gary "Six. The last rut drags on the right. Cracked rear rim."
    cs_fe_gary "They took the spur behind the reserve."
    cs_fe_rider "The six guards are between us and it."
    cs_fe_gary "Not for long. Unhitch that empty supply cart."
    cs_fe_rider "There is nothing in it."
    cs_fe_gary "There is a letter in my coat."
    pause 0.3
    cs_fe_gary "Commander said burn it."

    play sound audio.sfx_fwashing
    cs_fe_guard "FIRE IN THE RAVINE!"
    cs_fe_guard "Cart coming down! Clear the mouth!"
    play sound audio.sfx_wham
    with vpunch
    cs_fe_gary "Now. Ride the smoke."
    cs_fe_rider "You wrote all that just to light a cart?"
    cs_fe_gary "No. I wrote it because I was afraid."
    cs_fe_gary "The cart is what it became useful for."

    play sound audio.sfx_swing
    with hpunch
    cs_fe_guard "Riders behind us! Turn!"
    cs_fe_gary "No shouting near the wagons."
    cs_fe_guard "You are twelve men in the middle of an army."
    cs_fe_gary "Twelve riders. The men are occupied elsewhere."
    cs_fe_guard "Put down the sword."
    cs_fe_gary "Drop the keys."
    play sound audio.sfx_shing
    with hpunch
    cs_fe_guard "Ghh--"
    cs_fe_rider "Keys!"
    cs_fe_gary "First six wagons. Cut harness, not horses."
    cs_fe_gary "Three riders hold the spur. Four take chains. Five turn wheels."
    cs_fe_rider "That is twelve three different ways."
    cs_fe_gary "Then move quickly enough to be all of them."

    cs_fe_guard "Reserve! Prison break at the north spur!"
    show df_rival at t11
    cs_fe_rival "The ravine riders got through."
    cs_fe_scout "Six guards are down. The others want the reserve."
    cs_fe_rival "They do not get it. The center is still Akai's knife."
    cs_fe_scout "Then the prisoners go."
    cs_fe_rival "...Send the wagon guard. Nobody fires into the chains."
    cs_fe_scout "Sir?"
    cs_fe_rival "They are still people when they run from us. Pass the order."
    show df_rival at thide
    hide df_rival

    show gary at t11
    cs_fe_gary "First wagon open! Walk north! Do not wait for names!"
    cs_fe_gary "Second wagon, hands through the bars. I can reach the lock."
    cs_fe_rider "Wagon guard on the south bend!"
    cs_fe_gary "Two riders delay. Nobody chases. We win by leaving."
    cs_fe_gary "Third wagon!"
    pause 0.3
    cs_fe_gary "Mother."
    cs_fe_gary "Mother, look at me. Not the field. Me."
    cs_fe_gary "Where are my sisters?"
    pause 0.2
    cs_fe_gary "Fourth. I knew it. I knew they moved the sick forward."
    cs_fe_gary "You told me never to brag when I guessed right."
    cs_fe_gary "I am making an exception."

    cs_fe_rider "Sixth wheel is splitting!"
    cs_fe_gary "Cracked rim. I brought a brace for it. Saddlebag, blue strap."
    cs_fe_rider "You brought a wheel brace into a cavalry attack?"
    cs_fe_gary "I counted the wagons."
    cs_fe_rider "That answer has become frightening."
    cs_fe_gary "Brace it. Put the children in the first two wagons."
    cs_fe_gary "Everyone else walks between the wheels."
    cs_fe_gary "Count aloud."
    cs_fe_rider "Thirty-four. Thirty-five. Thirty-six."
    cs_fe_gary "The sick woman from four?"
    cs_fe_rider "Thirty-seven."
    cs_fe_gary "The twins?"
    cs_fe_rider "Thirty-eight. Thirty-nine."
    cs_fe_gary "Who is missing?"
    pause 0.3
    cs_fe_rider "Under the lead wagon! Boy, take my hand!"
    cs_fe_gary "Forty."
    cs_fe_gary "Light the red flare."
    cs_fe_gary "Commander, the whole world can see us now."
    show gary at thide
    hide gary

    scene bg greywake_field_dawn with dissolve
    cs_fe_scout "RED FLARE! East ravine!"
    show df_akai at t21
    show df_tsubaki at t22
    cs_fe_akai "Forty?"
    cs_fe_scout "Gary counted forty! Wagons turning north!"
    cs_fe_akai "Sound the horn. Leif takes the ridge."
    cs_fe_ts "And the center?"
    cs_fe_akai "Stops pretending."
    cs_fe_akai "Captain! Lock the bend and push!"
    cs_fe_captain "You heard her! Shields level! Take back every step!"

    # ------------------------------------------------------------------ #
    # V. The west-ridge reversal
    # ------------------------------------------------------------------ #
    show screen cs_matsuda_fe_phase_card(
        "ENEMY PHASE",
        "THE REVERSE SLOPE",
        "WEST RIDGE: SURVIVE"
    )
    with dissolve
    pause 1.4
    hide screen cs_matsuda_fe_phase_card
    with dissolve

    scene bg greywake_west_ridge with dissolve_scene_full
    show leif at t11
    cs_fe_leif "Horn! Riders, crest the hill! Do not stop on top!"
    cs_fe_rider "No fires. No banner. Nothing is up there."
    cs_fe_leif "Then the stories were fat. Take the ridge!"
    play sound audio.sfx_shing
    with hpunch
    cs_fe_leif "Crest is ours! Show the red banner!"
    cs_fe_rider "Their reserve is turning! We have their whole rear!"
    cs_fe_leif "North face now! We borrow, we do not keep!"
    cs_fe_sam "Leaving already?"
    pause 0.3
    show df_sam at t21
    show leif at t22
    cs_fe_leif "...Sam."
    cs_fe_sam "You climbed beautifully. Very clean line."
    cs_fe_sam "I could hear the confidence from under the grass."
    cs_fe_leif "Reverse slope."
    cs_fe_sam "Commander said you would look at an empty crown and wear it."
    cs_fe_leif "Commander said you were a story."
    cs_fe_sam "Which one?"
    cs_fe_leif "The one that dies when cavalry reaches open ground."
    cs_fe_sam "Then why are your horses backing up?"
    cs_fe_leif "They smell you."
    cs_fe_sam "They have excellent judgment."

    cs_fe_leif "First file, through him! Second file, down the north face!"
    play sound audio.sfx_longwoosh
    with hpunch
    cs_fe_rider "Pikes below the grass!"
    cs_fe_leif "Jump them!"
    play sound audio.sfx_wham
    with vpunch
    cs_fe_rider "The trail is blocked!"
    cs_fe_sam "Your fast road just became a narrow one."
    cs_fe_leif "Then I make it wide."
    cs_fe_sam "There is the man from the campfires."

    play sound audio.sfx_swing
    with hpunch
    cs_fe_leif "Too slow!"
    play sound audio.sfx_shing
    with hpunch
    cs_fe_sam "Too light."
    cs_fe_leif "I only need you looking at me."
    cs_fe_sam "No. You need me dead before the snow reaches the road."
    cs_fe_sam "That is why you are still here."
    cs_fe_leif "Riders! Break north! I hold the crest!"
    cs_fe_rider "You said we do not keep it!"
    cs_fe_leif "I changed the tenant! GO!"

    play sound audio.sfx_wham
    with vpunch
    cs_fe_leif "Ghh--"
    cs_fe_sam "Your horse is gone."
    cs_fe_leif "My sword is not."
    cs_fe_sam "The hill does not care what you call yourself on foot."
    cs_fe_leif "Good. I was tired of introducing myself."
    play sound audio.sfx_swing
    with hpunch
    cs_fe_sam "That one was almost worth the climb."
    cs_fe_leif "I was faster than every story about you."
    cs_fe_sam "Every story but this one."
    play sound audio.sfx_stab
    with vpunch
    pause 0.4
    cs_fe_leif "...Commander. I left it."
    show leif at thide
    hide leif

    cs_fe_scout "Leif is down! West riders are trapped below the crest!"
    show df_akai at t21
    show df_tsubaki at t22
    cs_fe_akai "Signal Gregor. He holds until the long horn clears them."
    cs_fe_scout "The first horn already sounded."
    cs_fe_akai "That was Leif's. Tell Gregor the long horn is coming."

    play sound audio.sfx_longwoosh
    with hpunch
    cs_fe_soldier "Snow! I cannot see the ridge!"
    cs_fe_ts "It was supposed to wait until dawn."
    cs_fe_akai "The weather does not know the plan."
    cs_fe_scout "Their reserve is moving under the storm!"
    cs_fe_akai "Where?"
    cs_fe_scout "Half to the center. Half toward Gregor."

    show gregor at t11
    cs_fe_gregor "Shields low. Snow hides their feet, not their weight."
    cs_fe_soldier "Ford line set!"
    cs_fe_gregor "Gregor hears six voices on the ridge."
    cs_fe_soldier "Do not count them."
    cs_fe_gregor "Gregor did not choose to start."
    cs_fe_soldier "Leif is pulling out. He always pulls out."
    cs_fe_gregor "Fifth voice."
    play sound audio.sfx_wham
    with hpunch
    cs_fe_soldier "Pikes! Ford!"
    cs_fe_gregor "Set. Step. Set. Do not chase what the snow invents."
    cs_fe_soldier "Fourth voice."
    cs_fe_gregor "Do not help Gregor count."

    show df_sam at t21
    show gregor at t22
    cs_fe_sam "Gregor! Your friends are waiting uphill!"
    cs_fe_gregor "Gregor has a ford."
    cs_fe_sam "Leif had a ridge. Look how that worked out."
    cs_fe_gregor "Leif was told not to keep it."
    cs_fe_sam "He obeyed in the end."
    play sound audio.sfx_shock
    with hpunch
    cs_fe_soldier "Third voice!"
    cs_fe_gregor "Commander needs the ford."
    cs_fe_sam "The dead need nothing. It is one of their better qualities."
    cs_fe_gregor "Second."
    cs_fe_sam "Come count the last one where you can see him."
    pause 0.3
    cs_fe_gregor "Gregor gave his word."
    cs_fe_sam "Then keep it."
    cs_fe_sam "Stand down there and listen."
    play sound audio.sfx_stab2
    with vpunch
    cs_fe_soldier "...Last voice."
    pause 0.5

    show df_akai at t31
    show gregor at t32
    show df_sam at t33
    cs_fe_akai "Gregor, sixty breaths! Give me sixty and I can close the center!"
    cs_fe_gregor "Leif's boys do not have sixty."
    cs_fe_akai "The ford opens if you leave. Gary is still below the pass."
    cs_fe_gregor "Gregor knows."
    cs_fe_akai "You swore."
    cs_fe_gregor "Gregor has never broken his word."
    pause 0.4
    cs_fe_gregor "So it cannot be Gregor who goes."
    cs_fe_gregor "...{i}I'm sorry.{/i}"
    show gregor at thide
    hide gregor
    cs_fe_akai "GREGOR!"
    cs_fe_soldier "The shield companies are following him!"
    cs_fe_akai "Hold the ford! That is an order!"
    cs_fe_soldier "They cannot hear us in the snow!"

    show df_sam at t21
    show gregor at t22
    cs_fe_sam "There you are."
    play sound audio.sfx_wham
    with vpunch
    cs_fe_soldier "Gregor hit the ridge!"
    cs_fe_sam "You left a whole army to find eleven ghosts."
    play sound audio.sfx_swing
    with hpunch
    cs_fe_soldier "He took the berserker's shield!"
    cs_fe_sam "No. He took my shoulder."
    play sound audio.sfx_stab
    with vpunch
    cs_fe_soldier "I lost them! Snow on the crest! I cannot see either one!"
    cs_fe_akai "Gregor! Report!"
    pause 0.5
    cs_fe_scout "No answer."
    show gregor at thide
    show df_sam at thide
    hide gregor
    hide df_sam

    # ------------------------------------------------------------------ #
    # VI. The storm turn and the collapsing center
    # ------------------------------------------------------------------ #
    stop music fadeout 0.7
    play music devoted
    scene bg greywake_field_aftermath with dissolve_scene_full
    cs_fe_akai "Sound the long horn. Release every unit still listening."
    show df_rival at t21
    show df_akai at t22
    cs_fe_rival "The ford is empty. Reserve, wheel through the gap!"
    cs_fe_akai "Captain, refuse the left! Fold the center toward the north road!"
    cs_fe_captain "We cannot fold and push at once!"
    cs_fe_akai "Then stop pushing. The objective is leaving."
    cs_fe_rival "She abandoned the field."
    cs_fe_scout "Not the field. The wagons."
    cs_fe_rival "...She never wanted the field."

    cs_fe_soldier "Enemy reserve on our left!"
    cs_fe_captain "Pikes inward! Make a wall facing west!"
    cs_fe_soldier "Their center is coming too!"
    cs_fe_akai "Sound every horn. Make them think the whole line turns."
    cs_fe_captain "Does it?"
    cs_fe_akai "It does now."
    cs_fe_rival "Her horn is early."
    cs_fe_scout "Our captains stopped to dress ranks."
    cs_fe_rival "Push through them! Every breath gives the wagons road!"

    show gary at t31
    show df_akai at t32
    show df_rival at thide
    hide df_rival
    cs_fe_gary "Commander! Forty clear! First wagon reached the north road!"
    cs_fe_akai "All forty?"
    cs_fe_gary "I counted twice."
    cs_fe_akai "Then go north."
    cs_fe_gary "Your center is folding. We can bring the riders back."
    cs_fe_akai "No."
    cs_fe_gary "We can buy you the pass."
    cs_fe_akai "You already did. Now spend it on them."
    cs_fe_gary "If I take the wagons up, the snow closes behind us."
    cs_fe_akai "I know whose road it is."
    cs_fe_gary "Commander--"
    cs_fe_akai "Gary. Your mother has waited a month. Do not make her wait for my pride."
    pause 0.3
    cs_fe_gary "...Taken."
    cs_fe_akai "Taken twice."
    cs_fe_gary "North road! Wagons together! Nobody turns around!"
    show gary at thide
    hide gary

    show df_tsubaki at t21
    show df_akai at t22
    cs_fe_ts "Medic line, move with the center! Walkers between shields!"
    cs_fe_medic "The marked wounded are behind us."
    cs_fe_ts "I know."
    cs_fe_medic "You said we would come back."
    cs_fe_ts "I know."
    cs_fe_medic "Tsubaki--"
    cs_fe_ts "Do not make me say it a third time. Move."
    cs_fe_akai "Stay close to me."
    cs_fe_ts "Right behind you. Where you know."

    play sound audio.sfx_longwoosh
    cs_fe_scout "Archer in the snow!"
    play sound audio.sfx_fwashing
    stop music
    show white zorder 200:
        alpha 0.55
        linear 0.12 alpha 0.0
    with hpunch
    pause 0.4
    hide white

    cs_fe_ts "..."
    cs_fe_akai "Tsubaki?"
    cs_fe_ts "Do not turn around yet."
    cs_fe_akai "You stopped walking."
    cs_fe_ts "One moment. I am just going to-- ah."
    cs_fe_ts "...That is deep."
    cs_fe_akai "MEDIC!"
    cs_fe_medic "I am here."
    cs_fe_akai "Do not say my name like that. Pack it. Cut the shaft."
    cs_fe_medic "The arrow is under the shoulder blade."
    cs_fe_akai "Then take it out."
    cs_fe_medic "Not here. I need time."
    cs_fe_akai "You have my entire life. Use that."

    cs_fe_ts "Akai. Move me and you spend two bearers."
    cs_fe_akai "I do not care."
    cs_fe_ts "You lose the hands holding this shut."
    cs_fe_akai "I said I do not care about the arithmetic."
    cs_fe_ts "You will. In an hour, you will need it done right."
    cs_fe_akai "You do not get to do my job from the ground."
    cs_fe_ts "Somebody has to. You are busy."
    cs_fe_akai "Tsubaki."
    cs_fe_ts "Gary needs the road. That is why we came."
    cs_fe_ts "Go. I will be right here."
    cs_fe_ts "Right behind you. Where you know where I am."
    pause 0.4
    show df_tsubaki at thide
    hide df_tsubaki

    show df_akai at t11
    cs_fe_akai "Medic. Stay with her."
    cs_fe_akai "If she speaks, keep every word and bring it to me after."
    cs_fe_akai "There is going to be an after. Say it back."
    cs_fe_medic "There is going to be an after, Commander."
    cs_fe_akai "Louder."
    cs_fe_medic "There is going to be an after!"

    # ------------------------------------------------------------------ #
    # VII. Akai and the berserker
    # ------------------------------------------------------------------ #
    play music hopeless
    show df_sam at t21
    show df_akai at t22
    cs_fe_sam "Akai."
    cs_fe_akai "You should be on the ridge."
    cs_fe_sam "I brought some of it with me."
    cs_fe_akai "That blood is not all yours."
    cs_fe_sam "Enough is."
    cs_fe_akai "Gregor?"
    cs_fe_sam "Still somewhere in the snow."
    cs_fe_akai "Leif?"
    cs_fe_sam "Stopped being faster."
    cs_fe_akai "Move."
    cs_fe_sam "Cannot. He is at the bottom of this field."
    cs_fe_sam "You do not reach him while I am standing."
    cs_fe_akai "There is nothing left to hold."
    cs_fe_sam "There is always the person behind you."
    cs_fe_akai "Then stop standing."
    cs_fe_sam "There she is."

    play sound audio.sfx_swing
    with hpunch
    cs_fe_sam "Too high."
    play sound audio.sfx_shing
    with hpunch
    cs_fe_akai "Your left shoulder is gone."
    cs_fe_sam "Gregor took it personally."
    cs_fe_akai "Good."
    play sound audio.sfx_wham
    with vpunch
    cs_fe_sam "Shield is gone."
    cs_fe_akai "I was finished carrying it."
    play sound audio.sfx_swing
    with hpunch
    cs_fe_sam "And there go two fingers."
    cs_fe_akai "Two. You count badly."
    cs_fe_sam "You all talk like that near the end."
    cs_fe_akai "How many ends have you seen?"
    cs_fe_sam "Enough to recognize one."

    play sound audio.sfx_swing
    with hpunch
    cs_fe_akai "Your axe is dragging."
    cs_fe_sam "Your sword is shaking."
    cs_fe_akai "Mine only has to arrive once."
    cs_fe_sam "So does mine."
    play sound audio.sfx_shing
    with vpunch
    cs_fe_sam "Hah! Better."
    cs_fe_akai "You are enjoying this."
    cs_fe_sam "No."
    cs_fe_sam "I am making it worth what it costs."
    cs_fe_akai "That is not the same thing."
    cs_fe_sam "It has to be tonight."

    play sound audio.sfx_stab
    show white zorder 200:
        alpha 0.6
        linear 0.16 alpha 0.0
    with hpunch
    pause 0.3
    hide white
    cs_fe_sam "...There."
    cs_fe_akai "Sit down."
    cs_fe_sam "Tried. Legs disagreed."
    cs_fe_akai "I can call the medic."
    cs_fe_sam "The cleric has her. I saw."
    cs_fe_akai "Do not look back there."
    cs_fe_sam "Was not going to say anything."
    pause 0.3
    cs_fe_sam "Do me one thing."
    cs_fe_sam "Tell him the ridge held. He will want it from somebody there."
    cs_fe_akai "He knows what he asked of you."
    cs_fe_sam "That is why. He will do sums with it forever."
    cs_fe_sam "Tell him it held."
    cs_fe_sam "Tell him I would have gone up anyway. Knowing."
    cs_fe_sam "Say it exactly."
    cs_fe_akai "The ridge held. You would have gone up anyway. Knowing."
    cs_fe_sam "Good. Hate leaving a thing half--"
    show df_sam at thide
    hide df_sam

    show df_akai at t11
    cs_fe_akai "..."
    cs_fe_akai "I will tell him."
    cs_fe_akai "On whatever is left of us, I will tell him."

    stop music fadeout 1.0
    scene black with wipeleft_scene
    pause 0.7

    # ------------------------------------------------------------------ #
    # VIII. The rival commanders
    # ------------------------------------------------------------------ #
    play music devoted
    scene bg greywake_field_aftermath with dissolve_scene_full
    show df_rival at t21
    show df_akai at t22
    cs_fe_rival "Where is Sam?"
    cs_fe_akai "The ridge."
    cs_fe_rival "Alive?"
    cs_fe_akai "No."
    pause 0.3
    cs_fe_akai "He held it."
    cs_fe_akai "He said he would have gone up anyway. Knowing."
    cs_fe_akai "He made me repeat it so I would get it right."
    cs_fe_rival "...That sounds like him."
    cs_fe_rival "Did he say anything else?"
    cs_fe_akai "He hated leaving a thing half-finished."
    cs_fe_rival "That sounds like him too."
    pause 0.3
    cs_fe_rival "Your cleric?"
    cs_fe_akai "The center. Arrow under the shoulder."
    cs_fe_rival "Alive?"
    cs_fe_akai "When I left her."
    cs_fe_rival "Gregor?"
    cs_fe_akai "No body."
    cs_fe_rival "Leif?"
    cs_fe_akai "You know."
    cs_fe_rival "I do."

    cs_fe_scout "Commander, their right is exposed. Give us the word."
    cs_fe_rival "No."
    cs_fe_scout "Akai is alone."
    cs_fe_rival "So am I. Hold the line."
    cs_fe_captain "Commander, one rush and we can pull you clear."
    cs_fe_akai "Stay where you are."
    cs_fe_captain "We can still reach the road together."
    cs_fe_akai "You can reach it without me. That is an order."
    cs_fe_rival "They are not moving."
    cs_fe_akai "Neither are yours."
    cs_fe_rival "Did you order them to stop?"
    cs_fe_akai "No."
    cs_fe_rival "Neither did I."
    cs_fe_akai "Perhaps they are tired of our orders."
    cs_fe_rival "They chose an excellent time to develop judgment."

    cs_fe_rival "Order the retreat, Akai."
    cs_fe_akai "The wagons are not through the pass."
    cs_fe_rival "My army is looking at you, not the road."
    cs_fe_akai "Exactly."
    cs_fe_rival "You plan to keep us looking."
    cs_fe_akai "As long as it takes."
    cs_fe_rival "There is nothing here left worth having."
    cs_fe_akai "Forty people would disagree."
    cs_fe_rival "They are already gone."
    cs_fe_akai "Not far enough."
    cs_fe_rival "We could stop. Both of us."
    cs_fe_rival "Who is even left to make us continue?"
    cs_fe_akai "Everyone we spent getting here."
    cs_fe_rival "...I knew you would say that."
    cs_fe_rival "I needed the other answer said once, so it existed."
    cs_fe_akai "It exists."
    cs_fe_rival "And changes nothing."
    cs_fe_akai "Not nothing."
    cs_fe_rival "No. Not nothing."

    cs_fe_rival "Quarter. Last time."
    cs_fe_akai "I know. Thank you."
    cs_fe_akai "No."
    cs_fe_rival "Give me one reason that is not pride."
    cs_fe_akai "Gary is north with forty freed people."
    cs_fe_akai "If I kneel now, everything bought a surrender."
    cs_fe_akai "It has to end standing."
    cs_fe_rival "For the people behind you."
    cs_fe_akai "For Gregor, who broke one promise for a friend."
    cs_fe_akai "For Leif, faster than every story but one."
    cs_fe_akai "For the ones Tsubaki could not go back for."
    pause 0.3
    cs_fe_akai "For Tsubaki."
    cs_fe_rival "...For Sam."
    cs_fe_akai "Meet me in the middle."
    cs_fe_rival "Standing up, then."

    show screen cs_matsuda_fe_phase_card(
        "BOSS",
        "THE RIVAL COMMANDER",
        "DEFEAT THE ENEMY COMMANDER"
    )
    with dissolve
    pause 1.7
    hide screen cs_matsuda_fe_phase_card
    with dissolve
    play music epicbattlephase2

    # First exchange: each commander tests the habits seen across the field.
    show df_rival at t21
    show df_akai at t22
    cs_fe_rival "Ready?"
    cs_fe_akai "No."
    cs_fe_rival "Neither am I."
    play sound audio.sfx_shing
    show white zorder 200:
        alpha 0.4
        linear 0.16 alpha 0.0
    with hpunch
    pause 0.2
    hide white
    cs_fe_akai "You lead with the shoulder."
    cs_fe_rival "You give ground on purpose."
    cs_fe_akai "You noticed."
    cs_fe_rival "You built a battle out of it."
    cs_fe_akai "And you did not follow."
    cs_fe_rival "I am following now."
    play sound audio.sfx_swing
    with hpunch
    cs_fe_akai "Too far."
    cs_fe_rival "You left the opening."
    cs_fe_akai "For you."
    play sound audio.sfx_shing
    with vpunch
    cs_fe_rival "And closed it behind me."
    cs_fe_akai "Almost."

    cs_fe_soldier "Commander! His flank is open!"
    cs_fe_rival "Stay back!"
    cs_fe_captain "Akai, let us end him!"
    cs_fe_akai "Nobody crosses the wagon tracks!"
    cs_fe_rival "They listen to you even now."
    cs_fe_akai "They are pretending."
    cs_fe_rival "Mine too."
    cs_fe_akai "Good soldiers."
    cs_fe_rival "Terrible survivors."

    play sound audio.sfx_swing
    with hpunch
    cs_fe_rival "Your right hand is slow."
    cs_fe_akai "Sam broke two fingers."
    cs_fe_rival "He always preferred thorough work."
    cs_fe_akai "Your left leg drags."
    cs_fe_rival "Leif's last rider found my boot."
    cs_fe_akai "Then he reached the center."
    cs_fe_rival "For one strike."
    cs_fe_akai "Sometimes one arrives."
    play sound audio.sfx_stab2
    with vpunch
    cs_fe_rival "Your sleeve is red."
    cs_fe_akai "So is the field. Be specific."
    cs_fe_rival "Upper arm. Shallow."
    cs_fe_akai "Your cheek. Shallower."
    cs_fe_rival "We are keeping score now?"
    cs_fe_akai "I like to know how badly I am losing."

    # Second exchange: the duel leaves clean ground and enters the wreckage.
    play sound audio.sfx_longwoosh
    with hpunch
    cs_fe_scout "Wind turned! Snow across the center!"
    cs_fe_rival "I cannot see your feet."
    cs_fe_akai "Neither can I."
    cs_fe_rival "You know where yours are."
    cs_fe_akai "An unfair advantage."
    play sound audio.sfx_swing
    with hpunch
    cs_fe_rival "There."
    cs_fe_akai "Banner pole."
    play sound audio.sfx_wham
    with vpunch
    cs_fe_rival "You dropped the field standard on me."
    cs_fe_akai "I had stopped using it."
    cs_fe_rival "Your soldiers may object."
    cs_fe_akai "They can write a complaint after the war."

    play sound audio.sfx_shing
    with hpunch
    cs_fe_akai "Your sword caught."
    cs_fe_rival "In somebody's shield."
    cs_fe_akai "Leave it."
    cs_fe_rival "You first."
    play sound audio.sfx_wham
    with vpunch
    cs_fe_rival "You kicked me."
    cs_fe_akai "The histories may omit it."
    cs_fe_rival "The histories are cowards."
    cs_fe_akai "Agreed."
    play sound audio.sfx_swing
    with hpunch
    cs_fe_rival "Got it free."
    cs_fe_akai "I noticed."
    cs_fe_rival "Your guard is low."
    cs_fe_akai "Your boot is filling with blood."
    cs_fe_rival "We all have problems."
    cs_fe_akai "That was my line."
    cs_fe_rival "I captured it."

    play sound audio.sfx_stab
    with hpunch
    cs_fe_akai "Ghh--"
    cs_fe_rival "Drop the sword."
    cs_fe_akai "No."
    cs_fe_rival "I cut your hand."
    cs_fe_akai "You cut the glove."
    cs_fe_rival "There is blood on it."
    cs_fe_akai "There was blood on it before you."
    cs_fe_rival "Akai."
    cs_fe_akai "Do not become reasonable this late."
    cs_fe_rival "I am trying to keep one person alive."
    cs_fe_akai "So was I."
    cs_fe_rival "Forty."
    cs_fe_akai "Forty-one."
    cs_fe_rival "The cleric."
    cs_fe_akai "The cleric."

    # Third exchange: both lose the weapon line, then choose to restore it.
    play sound audio.sfx_shing
    with hpunch
    cs_fe_rival "Your sword!"
    cs_fe_akai "Still within reach."
    cs_fe_rival "Not before mine reaches you."
    pause 0.3
    cs_fe_akai "Then reach."
    cs_fe_rival "..."
    cs_fe_akai "What are you waiting for?"
    cs_fe_rival "The person who moved prisoners out of arrow range."
    cs_fe_akai "He is holding a sword at my throat."
    cs_fe_rival "He is reconsidering."
    cs_fe_akai "That sounds exhausting."
    cs_fe_rival "It has been a long night."
    pause 0.4
    cs_fe_rival "Pick it up."
    cs_fe_akai "You offered quarter already."
    cs_fe_rival "This is not quarter."
    cs_fe_rival "It is me refusing to win against somebody unarmed."
    cs_fe_akai "Pride, then."
    cs_fe_rival "You said I could have one reason."
    cs_fe_akai "That was for me."
    cs_fe_rival "I borrowed it."
    cs_fe_akai "You are stealing an alarming amount tonight."
    cs_fe_rival "Pick up the sword."
    cs_fe_akai "...Fine."

    play sound audio.sfx_shing
    with hpunch
    cs_fe_akai "My turn."
    cs_fe_rival "For what?"
    play sound audio.sfx_wham
    with vpunch
    cs_fe_rival "Ghh--"
    cs_fe_akai "Your sword."
    cs_fe_rival "In the mud."
    cs_fe_akai "Within reach."
    cs_fe_rival "Not before yours reaches me."
    cs_fe_akai "Then reach."
    cs_fe_rival "You are enjoying this too much."
    cs_fe_akai "I am enjoying it exactly enough."
    cs_fe_rival "And if I leave it there?"
    cs_fe_akai "Then I wait and become unbearable."
    cs_fe_rival "Too late."
    cs_fe_akai "Pick it up."
    pause 0.3
    cs_fe_rival "...Fine."

    # Fourth exchange: exhaustion turns the tactical duel into a war of inches.
    play sound audio.sfx_longwoosh
    with hpunch
    cs_fe_scout "North ridge vanished! The pass is closing!"
    cs_fe_rival "Your wagons have minutes."
    cs_fe_akai "Then I need minutes."
    cs_fe_rival "You have been dragging this out."
    cs_fe_akai "I thought you noticed everything."
    cs_fe_rival "I noticed. I hoped I was wrong."
    cs_fe_akai "Push harder."
    cs_fe_rival "Gladly."

    play sound audio.sfx_swing
    with hpunch
    play sound audio.sfx_shing
    with vpunch
    cs_fe_rival "One."
    cs_fe_akai "Counting?"
    cs_fe_rival "Your steps."
    cs_fe_akai "Then count backward."
    play sound audio.sfx_swing
    with hpunch
    cs_fe_rival "Two."
    cs_fe_akai "That was sideways."
    cs_fe_rival "It was still away from the road."
    cs_fe_akai "You are herding me."
    cs_fe_rival "You did it to an army."
    cs_fe_akai "An army was easier."
    play sound audio.sfx_shing
    with vpunch
    cs_fe_rival "Three."
    cs_fe_akai "No."
    play sound audio.sfx_wham
    with hpunch
    cs_fe_rival "Knee?"
    cs_fe_akai "Pommel."
    cs_fe_rival "Dishonorable."
    cs_fe_akai "Put it in the report."

    cs_fe_captain "Commander! Green lantern beyond the pass!"
    cs_fe_scout "The last wagon crossed!"
    pause 0.4
    cs_fe_akai "Forty."
    cs_fe_rival "You got them out."
    cs_fe_akai "Gary got them out."
    cs_fe_rival "You gave him the field."
    cs_fe_akai "He brought a wheel brace."
    cs_fe_rival "What?"
    cs_fe_akai "It would take too long."
    cs_fe_rival "We appear to have time."
    cs_fe_akai "No."
    cs_fe_akai "Now we finish."

    # Final exchange: neither has a clean victory, and neither will take help.
    cs_fe_soldier "Commander, the wagons are gone! Let us cross!"
    cs_fe_rival "Nobody moves."
    cs_fe_captain "Akai, the road is won!"
    cs_fe_akai "Nobody moves!"
    cs_fe_rival "You could leave now."
    cs_fe_akai "Through your line?"
    cs_fe_rival "I can open it."
    cs_fe_akai "And explain that to your dead?"
    cs_fe_rival "Can you explain this to yours?"
    cs_fe_akai "No."
    cs_fe_rival "Neither can I."
    cs_fe_akai "That is why we are still here."

    play sound audio.sfx_swing
    with hpunch
    cs_fe_rival "Your guard is gone."
    cs_fe_akai "So take it."
    cs_fe_rival "Akai, I can see your whole side."
    cs_fe_akai "Take the opening or stop narrating it!"
    play sound audio.sfx_shing
    with vpunch
    cs_fe_rival "You were waiting for that."
    cs_fe_akai "Since the first exchange."
    cs_fe_rival "You gave me the same opening four times."
    cs_fe_akai "You needed to believe I was too tired to close it."
    cs_fe_rival "Are you?"
    cs_fe_akai "We are about to find out."

    play sound audio.sfx_swing
    with hpunch
    cs_fe_akai "Your point is past my guard."
    cs_fe_rival "Yours is under mine."
    cs_fe_akai "One step."
    cs_fe_rival "For both of us."
    cs_fe_akai "You can pull away."
    cs_fe_rival "So can you."
    pause 0.4
    cs_fe_rival "The wagons went north."
    cs_fe_akai "That is what it was for."
    cs_fe_rival "Then let the field keep the rest."
    cs_fe_akai "Standing up."
    cs_fe_rival "Standing up."

    play sound audio.sfx_stab2
    stop music
    window hide(None)
    show white zorder 200:
        alpha 0.7
        linear 0.22 alpha 0.0
    with vpunch
    pause 0.35
    scene cg dead_fantasy_greywake_draw with dissolve
    $ cg_unlock("Greywake Draw")
    pause 2.4
    scene black
    pause 1.5

    # ------------------------------------------------------------------ #
    # IX. The table
    # ------------------------------------------------------------------ #
    hide screen cs_matsuda_fe_stage_overlay
    scene bg living_room_tabletop_night with dissolve_scene_full
    play music enterm
    show sam neut at t41
    show matsuda neut at t42
    show asahina neut at t43
    show tsubaki neut at t44
    ma "...And the die clips my notebook."
    ma "Both attacks hit."
    ma "Akai goes down with your blade in her side. Your commander--hers under his ribs."
    ma "Neither one gets back up. Neither army moves."
    ma "The wagons are gone. The pass closes behind them."
    ma "Greywake ends in a draw."
    pause 0.7
    sa "..."
    ah "..."
    ts "..."
    mc "..."
    show matsuda curious
    ma "Guys?"
    show sam shocked
    sa "...No."
    ma "No?"
    show sam angry
    sa "No, fuck {i}that.{/i}"
    ma "That's not usually how an outcome works--"
    sa "A {i}draw.{/i}"
    show matsuda annoyed
    ma "Yes, Sam, that's the word I just said--"
    show sam frustrated
    sa "A fucking {i}draw?{/i}"
    ma "Can you not scream directly into my face?"
    sa "{i}Nineteen rounds.{/i}"
    ma "I know how many--"
    sa "Then say it. Say the stupid number."
    ma "Nineteen!"
    sa "Nineteen goddamn rounds on that ridge!"
    sa "I tracked rations. I did math about my own death."
    sa "I gave a speech so good I cried at my own fake man--"
    ma "It {i}was{/i} a good speech!"
    sa "I {i}know!{/i} That's why this is bullshit."
    sa "All that, and the leads get a poetic participation ribbon?"
    ma "Those nineteen rounds are why the wagons got out!"
    sa "Don't pat me on the fucking head with the wagons."
    ma "I am not {i}patting{/i} you--"
    sa "'Good boy, Sam, your massacre had narrative purpose.'"
    ma "Don't put words in my mouth."

    # Tsubaki fate question 1 of 4.
    show tsubaki worried
    ts "...Did she live?"

    show asahina angry
    ah "No, wait--the left wing. What happened to my left wing?"
    sa "I'm not done!"
    ah "Neither am I, asshole!"
    ma "Could one person yell at me at a--"
    ah "You don't get to ask for orderly complaints {i}now.{/i}"
    ma "The left wing broke because you abandoned the ford!"
    ah "Because you put every dying rider right in Gregor's ear."
    ah "You counted them down. One by one. Like a psychopath with a metronome."
    ma "You told me that was his trigger in session zero!"
    ah "For {i}drama!{/i} Not so you could beat me to death with my own sheet."
    ma "That's what backstory is {i}for!{/i}"
    show asahina disgusted
    ah "Then you made me roll Wisdom to {i}ignore it.{/i}"
    ma "To hold the line--"
    ah "Same thing when they're screaming his name."
    ma "You rolled a {i}four{/i}. In the open. Everybody saw it."
    ah "Gregor didn't need Wisdom. Gregor needed his friends {i}alive.{/i}"
    show matsuda frustrated
    ma "Gregor handed my entire center to MC's reserve. What was I supposed to do, give him a cookie?"
    ah "Oh, eat my ass with that."
    ma "Excuse me?"
    ah "Your entire plan had one hinge! You made the hinge a traumatized man--"
    ma "That is not--"
    ah "--then acted shocked when it did what hinges {i}do.{/i}"
    ma "Hinges open doors, Asahina!"
    ah "Yes! That's my entire point!"
    sa "What does that even--"
    ah "Don't help her!"

    # Tsubaki fate question 2 of 4.
    show tsubaki nervous
    ts "{i}Matsuda.{/i} Did the medic reach her or not?"

    show sam angry
    sa "And the draw--was that already in your notebook?"
    show matsuda shocked
    ma "...What did you just ask me?"
    sa "You heard me. Before we ever sat down--was {i}this{/i} your ending?"
    sa "Mirrored commanders. Mutual respect. Tragic sword pose. Snow everywhere."
    sa "Because it sure as hell smells prewritten from this side of the table."
    show matsuda angry
    ma "Take that back."
    sa "Answer it."
    ma "You're calling me a coward with extra fucking syllables."
    sa "If you dragged us through eight sessions toward your ending--"
    ma "I rolled {i}every attack{/i} where you could see it!"
    ma "Leif. The storm. The arrow. {i}All of it.{/i}"
    sa "That doesn't answer me--"
    ma "I almost called a break after the arrow!"
    ma "I needed five minutes to go scream into the refrigerator."
    sa "Then maybe you should've taken them."
    ma "Maybe you should've taken a break on round twelve."
    sa "Maybe you should've stopped spawning cavalry."
    ma "They were already on the map, Sam!"

    show mc neut at t22
    mc "Can everybody lower it one notch--"
    show sam unamused
    sa "Oh, good, the duel guy has notes."
    mc "I'm not 'the duel guy.'"
    show asahina smug
    ah "You got six pages of boss dialogue. You're the duel guy."
    mc "I also got every person under my command killed or scattered!"
    sa "Yeah. {i}Cinematically.{/i} In the snow. With a soundtrack."
    mc "You think I {i}liked{/i} stabbing Akai?"
    ma "Technically you rolled to--"
    mc "Not helping, Matsuda!"
    mc "I spent that whole duel begging for one way both armies could stop--"
    ah "Oh, congratulations--"
    mc "--and every answer slammed shut because all our earlier choices mattered!"
    ah "Your pain still got close-ups!"
    mc "And yours got an {i}entire hill.{/i}"
    show asahina frustrated
    ah "My guy disappeared inside a {i}weather system!{/i}"
    mc "I didn't write the weather system!"
    ma "Somebody finally mentions my weather system and it's an insult. Fantastic."
    sa "Stop being proud of the murder cloud!"
    ma "It was a blizzard!"

    # Tsubaki fate question 3 of 4.
    show tsubaki frustrated
    ts "Can we {i}please{/i} roll the medic?"

    ma "I'm doing the epilogue in order!"
    sa "We haven't settled whether the epilogue is bullshit!"
    mc "Nothing's getting settled while everybody screams over everybody--"
    ah "You tried to referee us thirty seconds ago."
    mc "Because you all sound deranged!"
    show sam angry
    sa "{i}You{/i} were halfway over the table for the entire duel!"
    mc "Of course I was! I was fighting for my life."
    ma "Thank you! Somebody respected the encounter design--"
    mc "Don't recruit me! I'm mad at you too!"
    ma "For what?!"
    mc "You made me choose between forty civilians and every soldier I had. Then you made both groups know I chose!"
    ma "That was the {i}point{/i}, dumbass."
    mc "I {i}know!{/i} A point can be good and still make me want to throw your screen out a window."
    ma "That screen cost thirty dollars!"
    mc "Then stop making it smug!"

    show asahina angry
    ah "And somehow Gary gets out clean. Whoopty-freaking-doo."
    ah "Monika writes a small novel and suddenly the dice kiss her feet--"
    m "Oh, fuck {i}off.{/i} Gary survived because Gary prepared."
    show sam unamused
    sa "And here comes the wagon defense attorney."
    m "I counted every prisoner for a month!"
    m "Bad wheel. Driver's shoulder. The sisters switching places. I wrote {i}all of it{/i} down!"
    m "I bought the brace before we even knew there'd be a battle!"
    ah "A wheel brace is not a personality!"
    m "Neither is talking in third person, but we all made room."
    show asahina shocked
    ah "Oh, you {i}bitch.{/i}"
    m "The character bit! Don't twist that into something else."
    show asahina angry
    ah "It was already something else! We're screaming over graph paper."
    m "Gary made good choices. That's not cheating."
    sa "He burned his goodbye letter to win an encounter."
    m "Yes, and it {i}ruled!{/i}"
    mc "It did rule!"
    ah "Stop forming a competent-preparation coalition in my face!"
    sa "I'm not in the coalition--"
    mc "Neither am I--"
    m "You literally just joined it!"

    show matsuda angry
    ma "You know what? No. If everybody's going to shit on my work--"
    sa "Oh my god, here we--"
    ma "No! {i}I'm talking now!{/i}"
    ma "{i}Three weeks!{/i} I spent three weeks on Greywake."
    ma "I drew two maps because Sam drowned the first one in soda!"
    sa "That cup was outside the grid!"
    ma "It {i}flowed{/i}, Sam! Liquids don't respect the grid!"
    ma "I made army sheets. I did voices. I built a weather table--"
    ah "Nobody asked for meteorology!"
    ma "A {i}real{/i} one! Pressure, wind, visibility--{i}all of it.{/i}"
    ma "Nobody asks for the work that makes a world feel alive until they want to piss on the ending!"
    ma "Gary's mother has a name and a favorite soup."
    m "I know. I wrote both."
    ma "You gave me {i}six FUCKING pages{/i} of family notes!"
    m "And you used every page! You're welcome."
    sa "The soup didn't fix the ending!"
    ma "It wasn't supposed to fix the ending!"
    ma "You got the honest result the dice gave us!"
    sa "You got your {i}self-insert{/i} into the final shot!"
    ma "Akai is {i}not{/i} a self-insert!"
    ah "Your commander has one name, and it's {i}your last name!{/i}"
    ma "Akai is a common name!"
    mc "It's still literally your last name!"
    ma "It's thematically resonant!"

    # Tsubaki fate question 4 of 4.
    show tsubaki angry
    play sound "assets/audio/sfx/msbf/resist.wav"
    ts "IS SHE DEAD, MATSUDA?!" with vpunch

    show sam frustrated
    sa "Tsubaki, give me one second--"
    ma "No! You give {i}me{/i} one--"
    ah "Neither of you has had one good second all night."
    show tsubaki empty
    ts "..."
    show tsubaki sad
    ts "Fine. Keep screaming. Maybe you'll hear me when I stop talking."

    stop music
    play sound audio.sfx_wham
    show mc at thide
    hide mc
    show monika forward casual vang om oe nobl rhip lpoint at t11
    show matsuda shocked
    show sam shocked
    show asahina shocked
    show tsubaki shocked
    show white zorder 200:
        alpha 0.75
        linear 0.1 alpha 0.0
    with vpunch
    hide white
    m forward casual vang om oe nobl rhip lpoint "SHUT THE FUCK UP!!!"
    ma "..."
    sa "..."
    ah "..."
    mc "{size=12}...Ow. The table hit my knee...{/size}"
    m forward casual angr om oe nobl rhip lpoint "Good. Maybe it knocked basic hearing back into your thick skull."
    m forward casual vang om oe nobl rhip lpoint "Tsubaki asked the same thing {i}four times.{/i}"
    m forward casual angr om oe nobl rhip lpoint "I counted because none of you assholes could be bothered."
    show sam nervous
    sa "I heard her. I was just--"
    m forward casual vang om oe nobl rhip lpoint "Finishing your sentence. Every time."
    sa "I--"
    m forward casual angr om oe nobl rhip lpoint "Don't you {i}dare{/i} finish that one too."
    show asahina nervous
    ah "Monika--"
    m forward casual vang om oe nobl rhip lpoint "You heard her. Asahina heard her. Matsuda {i}absolutely{/i} heard her."
    mc "I was trying to--"
    m forward casual angr om oe nobl rhip lpoint "You were trying to sound reasonable while the rest of us caught fire. It didn't work."
    m forward casual vang om oe nobl rhip lpoint "And {i}you.{/i} You have had that medic check sitting behind your screen all night."
    ma "I said it'd happen in the epilogue--"
    m forward casual angr om oe nobl rhip lpoint "We {i}are{/i} in the epilogue, Matsuda."
    m forward casual vang om oe nobl rhip lpoint "Roll it. Right now. Before I shove that weather table down your throat sideways."
    show matsuda annoyed
    ma "It's called dramatic timing."
    m forward casual vang om oe nobl rhip lpoint "YOUR TIMING IS {i}SHIT.{/i}"
    ma "I was trying to land the--"
    m forward casual angr om oe nobl rhip lpoint "{i}Land the die.{/i}"
    m forward casual vang om oe nobl rhip lpoint "I loved tonight, okay? I cried over a fake wagon and a fictional wheel brace."
    m forward casual vang om oe nobl rhip lpoint "That rescue was the best scene I've ever had here, and now I want to strangle every person at this table."
    ah angry "Don't act like you're all innocent, you bit--"
    m forward casual angr om oe nobl rhip lpoint "ROLL. The die before I commit a hate crime."
    ma "..."
    ma "...Fine. Fine."

    show matsuda worried
    ma "Tsubaki--take the die."
    show tsubaki afraid
    ts "{i}Me?{/i}"
    ma "Your cleric, your hands."
    ma "The medic reaches her in time on a nine or better."
    show tsubaki panicked
    ts "Why would you make {i}me{/i} do this?"
    ts "What if I roll a two? I still have to {i}live here{/i} after this."
    ma "Because she isn't mine."
    ts "You shot her!"
    ma "I borrowed her for the war. You decide what her hands do now."
    ts "That is a beautiful sentiment, and I hate you for it."
    show tsubaki nervous
    ts "Fine. I'm rolling. Nobody say a word."
    pause 0.7
    show tsubaki afraid
    ts "I can't look. Somebody else look."
    pause 0.3
    ts "Monika."
    m forward casual sad cm oe nobl rdown ldown "..."
    show tsubaki frustrated
    ts "{i}Monika!{/i}"
    m forward casual vsur om oe blus rdown ldown "...Eleven."
    play music roster_place
    m forward casual happ om oe blus rdown ldown "{i}Eleven{/i} against nine. She lives!"
    m forward casual happ om oe blus rdown ldown "Your dumb, stubborn cleric {i}lives!{/i}"
    show tsubaki crying
    ts "Oh, you are all {i}awful.{/i}"
    ts "She lives. She actually {i}lives!{/i}"
    sa "She lives!"
    ah "Eleven!"
    mc "Holy shit--"
    ts "Nobody look at me. Eyes somewhere else. {i}Now.{/i}"
    show sam happy
    sa "Nobody's looking."
    ts "You're literally pointing at me."
    sa "Spiritually, I'm pointing at the ceiling."
    ah "That's not how pointing works."
    sa "NOT THE TIME, ASAHINA!"

    pause 0.5
    show sam embarrassed
    sa "Tsubaki, I--"
    ts "You told me to give you a second."
    sa "I know."
    ts "After I gave you about sixty."
    sa "I know. I heard you and decided my thing was louder. That was shitty. I'm sorry."
    ah "Same. Mine too. I heard you and kept going."
    sa "Stop piggybacking on my apology."
    show asahina angry
    ah "I'm not piggybacking. You don't {i}own being sorry.{/i}"
    ts "Could both of you stop turning your apologies into another contest?"
    sa "Right. Sorry. Again."
    ah "Shit. Sorry. Separately. Mine."
    mc "I heard you too. I did the calm voice instead."
    ts "The calm voice was worse."
    mc "Yeah. It was. Sorry."
    show matsuda sad
    ma "And I knew. The whole time."
    ts "I know."
    ma "I kept thinking, 'after this sentence,' and then there was another sentence, and then Sam called me a coward--"
    ts "Matsuda."
    ma "Right. No excuse. I was being an asshole. I'm sorry."
    show tsubaki embarrassed
    ts "...Good. You're all still assholes."
    sa "Yeah."
    ah "Huge ones."
    mc "No argument."
    m forward casual angr cm oe nobl rhip lpoint "I'm still considering biting."
    ma "Please don't bleed on the map."
    m forward casual vang om oe nobl rhip lpoint "I will bleed where I want."

    show matsuda determined
    ma "And, Sam--you wanted an answer? Fine."
    show sam neut
    ma "I wanted Akai to win. {i}Badly.{/i}"
    ah "Obviously. She has your last name and your personality."
    ma "Can I get six seconds without you jumping on my throat?"
    ah "Apparently none of us can. Keep going."
    ma "I wanted her to win from the day I drew Greywake."
    ma "I knew her last speech. I knew exactly where her blade was supposed to land."
    ma "Then the dice said no. {i}In the open. Three times.{/i}"
    ma "You saw the numbers. All of you."
    sa "You still could've called one of them wrong."
    ma "Yes. I could've lied."
    sa "I didn't say--"
    ma "One number behind the screen and Akai gets my perfect ending. You'd never know."
    ma "But then Gregor's four is fake. Your nineteen rounds are fake."
    ma "Gary's preparation--"
    m forward casual angr om oe nobl rhip lpoint "Don't drag Gary into your defense."
    ma "--and Tsubaki's eleven. Fake. {i}All of it.{/i}"
    show tsubaki annoyed
    ts "My eleven is not your courtroom exhibit."
    ma "I know. That's the point. It belongs to {i}you.{/i}"
    ma "If the dice only matter when they agree with me, then none of you are playing."
    ma "I'm just reading a story {i}at{/i} you while you hold props."
    ma "The draw is what this loud, horrible table made together."
    ma "I hated it. I {i}still{/i} hate it. And I kept it."
    pause 0.4
    show sam annoyed
    sa "...I'm still pissed."
    show matsuda smug
    ma "Good. It was a war. Somebody should be."
    sa "Don't say that like we agree."
    ma "We agree that you're pissed."
    sa "That's not--screw you."
    show sam frustrated
    sa "It was a good war, okay? That's the infuriating part."
    sa "If it sucked, I could call it shit and go home."
    ma "...That might be the nicest thing you've ever screamed at me."
    sa "DON'T MAKE IT WEIRD!"

    # The old rhythm returns crookedly, with the argument still hot underneath it.
    show asahina teasing
    ah "Great. Beautiful. {i}Now{/i} can we address the self-insert?"
    show matsuda annoyed
    ma "Oh my God, no."
    ah "I haven't even--"
    ma "Akai is not a self-insert."
    m forward casual happ cm ce nobl rdown ldown "You named her Akai. You didn't even give her a surname."
    ma "She doesn't need one."
    mc "Because you already gave her yours."
    ma "{i}Thematic resonance.{/i}"
    show sam teasing
    sa "She got a private monologue after everybody left the room."
    ah "She whispered vows at the map."
    mc "She fought a duel after two battles and an arrow storm."
    ma "She did {i}not{/i} win. We just spent ten minutes screaming about that."
    sa "She got the cool half of not winning."
    ma "SHE GOT STABBED IN THE SIDE!"
    m forward casual laug om ce nobl rdown ldown "Very heroically."
    show matsuda frustrated
    ma "I hate this table. None of you respect atmosphere."

    show asahina determined
    ah "And we're {i}not{/i} ending until we deal with Gregor."
    ma "Deal with--"
    ah "He said, '{i}I'm sorry.{/i}'"
    ma "Yeah."
    ah "First person. Once. The only time in eight sessions."
    ah "He couldn't let the bit be the thing that broke the promise."
    show matsuda sad
    ma "We noticed."
    ah "Don't do that voice."
    ma "What voice?"
    ah "The soft GM voice that makes everything sound like a funeral."
    ma "I was trying to say it was really good."
    show asahina embarrassed
    ah "Oh. Well. It fucking was."
    ma "Yes. It was."
    show asahina determined
    ah "And he's not dead."
    ma "He charged Sam uphill through a blizzard."
    sa "It was a very thorough blizzard."
    ah "Did you describe his body?"
    ma "I described the entire left wing disappearing."
    ah "THAT IS NOT A BODY!"
    ma "Asahina--"
    ah "{i}Body.{/i} Yes or no."
    pause 0.3
    show matsuda smug
    ma "...No body was described at this table."
    show asahina happy
    ah "THEN GREGOR HOLDS! Somewhere, Gregor holds."
    show sam happy
    sa "My next character finds him half-frozen in a ditch."
    ah "Still doing third person at the vultures."
    ma "Stop co-writing my sequel at me."
    m forward casual laug om ce nobl rdown ldown "She's writing it down."
    show matsuda unamused
    ma "I am {i}not.{/i}"
    mc "You have the Gregor voice in quotation marks."
    ma "That could be anything."

    show tsubaki curious
    ts "What happens after Greywake?"
    show matsuda thinking
    ma "Oh, now everybody wants my epilogue?"
    ts "Matsuda. Don't start."
    ma "I am {i}allowed{/i} to note the irony."
    ts "Epilogue."
    ma "Fine. Gary gets all forty to the treeline before dawn."
    ma "He keeps going north until the war is just an accent people notice."
    ma "Years later, he names his daughter after a commander nobody there remembers."
    m forward casual sad om ce nobl rdown ldown "Goddamn it."
    m forward casual sad om ce nobl rdown ldown "I built him to survive. Why does that hurt {i}more?{/i}"
    ma "Because you did a good job."
    m forward casual angr om oe nobl rhip lpoint "I hate you."
    ma "You're welcome."
    ma "The cleric wakes two days later."
    ma "She insults the medic's stitching and outlives everyone in the campaign."
    show tsubaki happy
    ts "Correct. Finally, a sensible ruling."
    ma "Both commanders wake in different field hospitals."
    sa "Wait, they both--"
    ma "I said they don't get back up. I didn't say they die."
    sa "You manipulative little--"
    ma "{i}Let me finish.{/i}"
    ma "The draw holds. Nobody fights over Greywake again."
    ma "Akai and the Rival never meet in person after that night."
    ma "They write letters for the rest of their lives."
    ma "Because the only person who understands the cost paid the other half."
    show tsubaki sad
    ts "That's {i}horrible.{/i}"
    mc "No, that's--that's kind of beautiful."
    ts "It can be {i}both.{/i}"
    ma "Thank you. It's the good version of the sad thing."
    ah "That sentence is nonsense."
    ma "You understood it."
    ah "Unfortunately."

    show sam determined
    sa "RUNBACK!"
    ma "Excuse me?"
    sa "I want the sequel. New guy."
    sa "Strong opinions about ridges. Never holds one alone."
    show matsuda teasing
    ma "The first hill he charges gets hit by the weather system."
    sa "Deal. No promises."
    mc "There it is."
    show tsubaki determined
    ts "The medic roll is canon. Say it."
    ma "The medic roll is canon."
    ts "All eleven of it."
    ma "{i}All eleven.{/i}"
    show tsubaki happy
    ts "Good."
    ma "Now somebody find my d20. It went under the couch during the coward accusation."
    show sam teasing
    sa "I called the {i}ending{/i} cowardly. Take better notes."
    show matsuda smug
    ma "I hate every single one of you."
    pause 0.5
    show matsuda worried
    ma "...Same time next Saturday?"
    pause 0.7
    show sam happy
    sa "Are you kidding? {i}Obviously.{/i}"
    show asahina happy
    ah "You think I'm letting this campaign end without Gregor's body? Obviously."
    ts "Obviously. Somebody has to make you people hear words."
    mc "Obviously. I'll bring knee pads for the next table intervention."
    m forward casual happ cm oe nobl rdown ldown "Try and stop us."
    pause 0.4
    m forward casual laug om ce nobl rdown ldown "Good. {i}Now{/i} I can tell you idiots I made an irresponsible charcuterie board."
    m forward casual happ om oe nobl rdown lpoint "Help me kill it before all this crying makes the cheese warm."
    show asahina smug
    ah "Grief burns carbohydrates."
    show matsuda shocked
    ma "NOBODY GET BRIE ON MY MAP!"
    show sam teasing
    sa "Liquids don't respect the grid, Matsuda."
    ma "CHEESE ISN'T A LIQUID, SAM!"
    sa "Not with that attitude."

    scene black with dissolve_scene_full
    stop music fadeout 2.0
    pause 2.0

    $ persistent.cs_matsuda_01_unlocked = True
    $ cs_mark_completed("cs_matsuda_01")
    return
