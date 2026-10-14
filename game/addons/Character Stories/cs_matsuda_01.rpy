# Dead Fantasy / Greywake Field -- September 4, 2026.
# Two exclusive coalition perspectives, one playable tactical chapter.
# The Last Exchange is a declared scenario rule. Casualties are play-dependent.
# Table cast: Matsuda GM/Akai/Leif, MC rival, Sam berserker,
# Asahina Gregor, Monika Gary, Tsubaki cleric. Fantasy is played earnestly.
# The imported engine lives in python-packages/greywake.py; screen/wrappers
# in greywake_tactics.rpy. Battle state is per-game, never persistent.

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

default cs_df_side = None
default cs_df_result = None
default cs_df_previous_rollback = True
default cs_df_previous_quick_menu = True

default persistent.cs_df_tactics_release_seen = False

init 950 python:
    # Grant once to readers who cleared Chapter 0.5 before this release.
    # Later developer lock changes are respected.
    if not persistent.cs_df_tactics_release_seen:
        if persistent.chapter05_completed:
            persistent.cs_matsuda_01_unlocked = True
        persistent.cs_df_tactics_release_seen = True

init python:
    def cs_df_field_dispatch(battle):
        """Reports received at the chosen command, never the other council."""
        if battle.round not in (3, 5, 8):
            return None
        if battle.round == 3:
            if battle.side == "akai":
                return ("Akai", "The eastern league has fallen back to the orchard wall. They sent their last runners here; there is no one coming behind us. Keep the crossing open.", "akai")
            return ("The rival commander", "The capital column has stopped answering the horn. Orren's men saw them carrying wounded down the bank. We hold with the companies already here.", "rival")
        if battle.round == 5:
            if battle.side == "akai":
                if battle.unit("tsubaki")["dead"] or battle.unit("tsubaki")["down"]:
                    return ("Southern runner", "The hospital banner is down. The ford is rising and the horses won't enter it. Bring the bearers by the bridge while there's still a road.", None)
                return ("Tsubaki", "The water is over the stepping stones. Send the riders to the bridge. And tell the men who can walk to carry someone who can't.", "tsubaki")
            if battle.unit("sam")["dead"] or battle.unit("sam")["down"]:
                return ("Northern runner", "Sam's banner is down. The west companies are holding without him. The ford is rising; mounted units need the bridge.", None)
            return ("Sam", "Can't see the far end of the ridge. If anyone sends me another order to advance, wrap it around a dry pair of gloves. Horses need the bridge now.", "sam")
        secured = sum(o["secured"] for o in battle.objectives if o["kind"] == "granary")
        if secured == 2:
            return ("Field runner", "The quartermasters are sharing sacks across the road. Neither side asked permission. The surviving banners are pulling toward the two lords.", None)
        return ("Field runner", "The men are cutting leather off abandoned saddles to boil. We need the remaining grain under guard. The surviving banners are pulling toward the two lords.", None)

screen cs_df_choose_side():
    modal True
    add "bg greywake_field_dawn"
    add Solid("#07101be8")
    text "DEAD FANTASY" xpos 64 ypos 36 size 22 color "#d3bf83" kerning 5
    text "Choose your standard." xpos 64 ypos 78 size 46 color "#f5edda"
    text "One army. One account of the war. The other council stays behind its doors." xpos 66 ypos 140 size 22 color "#becad4"
    for side, title, commander, portrait, people, purpose, xx in (
        ("akai", "SOUTHERN COMPACT", "Akai", "akai", "Orra towns / Varn shields / border companies", "Break the cordon. Recover the grain and the displaced.", 64),
        ("rival", "NORTHERN CONCORD", "The rival commander", "rival", "Capital levies / Salt Coast / upland barons", "Hold the corridor. Get the starving columns through.", 658)):
        fixed:
            xpos xx ypos 198 xysize (558, 380)
            add Solid("#998259")
            add Solid("#111e2d") xpos 2 ypos 2 xysize (554, 376)
            add Transform("assets/extra_sprites/dead_fantasy/" + portrait + ".png", fit="contain", xysize=(210, 270)) xpos 10 ypos 66
            text title xpos 22 ypos 22 size 24 color "#ead39b" bold True
            text commander xpos 220 ypos 78 size 25 color "#fff2d9" xmaximum 310
            text people xpos 220 ypos 126 size 20 color "#aebccc" xmaximum 306
            text purpose xpos 220 ypos 200 size 22 color "#e9e0cd" xmaximum 306
            textbutton "Follow this army":
                xpos 218 ypos 303 xysize (314, 54)
                background Solid("#30485f") hover_background Solid("#496783")
                text_size 24 text_color "#fff2d9" text_hover_color "#ffffff"
                action Return(side)
    text "GREYWAKE'S LAST EXCHANGE" xpos 66 ypos 604 size 20 color "#d3bf83"
    text "Only the lords can defeat one another. Their final blows resolve together: a draw.\nYour orders decide the dead, the wounded, the wagons, and the winter stores." xpos 66 ypos 637 size 22 color "#d6dee4"

label cs_matsuda_01:
    hide screen archive
    hide screen character_stories
    $ atmos_clear()
    scene black
    stop music fadeout 1.0
    stop sound
    window hide
    $ cs_df_battle = None
    $ cs_df_result = None
    $ cs_df_side = None
    call screen cs_df_choose_side
    $ cs_df_side = _return
    $ renpy.block_rollback()
    show screen cs_matsuda_fe_stage_overlay
    if cs_df_side == "akai":
        call cs_df_southern_campaign from _call_cs_df_southern_campaign
    else:
        call cs_df_northern_campaign from _call_cs_df_northern_campaign
    call cs_df_greywake_orders from _call_cs_df_greywake_orders

    scene bg greywake_field_dawn with dissolve_scene_full
    hide screen cs_matsuda_fe_stage_overlay
    window hide
    play music epicbattlephase1 fadein 1.0
    $ cs_df_battle = GreywakeBattle(cs_df_side)
    $ cs_df_previous_rollback = _rollback
    $ cs_df_previous_quick_menu = quick_menu
    $ _rollback = False
    $ quick_menu = False
    $ renpy.retain_after_load()
    call screen cs_df_tactical_map(cs_df_battle)
    $ cs_df_result = _return
    $ _rollback = cs_df_previous_rollback
    $ quick_menu = cs_df_previous_quick_menu
    $ renpy.block_rollback()
    call cs_df_field_silence from _call_cs_df_field_silence
    call cs_df_table from _call_cs_df_table
    scene black with dissolve_scene_full
    stop music fadeout 2.0
    $ atmos_clear()
    $ persistent.cs_matsuda_01_unlocked = True
    $ cs_mark_completed("cs_matsuda_01")
    return

label cs_df_southern_campaign:
    show screen cs_matsuda_fe_phase_card("THE SIXTH WINTER", "SOUTHERN COMPACT", "Orra's road to Greywake / eleven days before the battle")
    with dissolve
    pause 2.0
    hide screen cs_matsuda_fe_phase_card
    play music hotr fadein 1.0
    scene bg castle01_strategyroom_night with dissolve_scene_full
    show df_akai at t21
    show gregor at t22
    cs_fe_captain "The south coast signed. Three towns, the shipwrights, and what is left of the fleet."
    cs_fe_akai "Ships?"
    cs_fe_captain "Sailors. They broke up the ships for firewood."
    cs_fe_gregor "Gregor can give them shields. Some still have hands inside the straps."
    cs_fe_akai "Take the hands out first."
    cs_fe_captain "Their delegates want a place beside your banner."
    cs_fe_akai "Give them a place beside the cook. Feed them before they discover what they've joined."
    cs_fe_scout "Varn's Crossing fell again."
    cs_fe_gregor "Which bank?"
    cs_fe_scout "Both. They fought across the mill dam until it broke."
    cs_fe_gregor "There was a school above that dam."
    cs_fe_scout "There was."
    pause 0.5
    cs_fe_akai "The children?"
    cs_fe_scout "I brought the people I found."
    cs_fe_akai "How many?"
    cs_fe_scout "Seven."
    cs_fe_gregor "Gregor will meet them."
    hide gregor
    show df_akai at t11
    cs_fe_captain "The eastern league is asking for two thousand men. The barley road is cut in three places."
    cs_fe_akai "Two thousand is every person here who can still march without leaning on somebody."
    cs_fe_captain "They say they will leave the Compact."
    cs_fe_akai "And march where?"
    cs_fe_captain "They did not say."
    cs_fe_akai "Send the spare horses. Say I need them back with the seed carts."
    cs_fe_captain "Those are the remounts."
    cs_fe_akai "Then the next man whose horse dies walks."
    scene bg greywake_ravine with wipeleft_scene
    show gary at t21
    show leif at t22
    cs_fe_rider "We broke their checkpoint. Seventeen prisoners, two wagons."
    cs_fe_leif "And the flour?"
    cs_fe_rider "Sawdust in the bottom half. The top half was already gone."
    cs_fe_gary "The prisoners can ride in them."
    cs_fe_leif "Those are our wounded wagons."
    cs_fe_gary "I know what they are."
    cs_fe_leif "Gary. We have wounded too."
    cs_fe_gary "Put the ones who can sit on the front boards. Bind two poles between the horses for the others."
    cs_fe_rider "One prisoner says your mother's column reached Greywake."
    cs_fe_gary "Was she walking?"
    cs_fe_rider "He didn't see her. He saw the wagons."
    cs_fe_gary "Six?"
    cs_fe_rider "Three groups. Forty people, he thinks."
    cs_fe_gary "Did he see a wheel braced with a door hinge?"
    cs_fe_rider "I'll ask."
    hide leif
    show df_tsubaki at t22
    cs_fe_ts "Gary, hold this. Above the knot."
    cs_fe_gary "Is that one of theirs?"
    cs_fe_ts "It is an artery. Higher."
    pause 0.4
    cs_fe_gary "Sorry."
    cs_fe_ts "You haven't let go. That's all I need."
    scene bg castle01_strategyroom_night with dissolve_scene_full
    show df_akai at t21
    show df_tsubaki at t22
    cs_fe_captain "Greywake's the last open military road. Every surviving northern column is moving toward it."
    cs_fe_akai "And ours?"
    cs_fe_captain "Twenty-three banners. Some have fewer than a hundred under them."
    cs_fe_akai "Put them on the map anyway."
    cs_fe_captain "They'll cover the valley."
    cs_fe_akai "They used to cover the country."
    cs_fe_ts "The abbey cannot take another wagon. They've put beds in the bread ovens."
    cs_fe_akai "There are two grain stores on the field. Winter grain and seed."
    cs_fe_ts "And an army in front of them."
    cs_fe_akai "Several armies. One coat of paint, several armies. The capital needs the road; the Salt Coast needs the grain."
    cs_fe_ts "What do we need?"
    cs_fe_akai "For the first field we sow in spring to stay a field until autumn."
    cs_fe_ts "You used to say the capital."
    cs_fe_akai "I used to have cavalry."
    cs_fe_ts "You still have Leif."
    cs_fe_akai "Yes. He keeps reminding me."
    cs_fe_ts "Ask for terms before you send him up another hill."
    cs_fe_akai "I've sent terms to six councils."
    cs_fe_ts "Send them to the man standing opposite you."
    cs_fe_akai "He isn't the six councils."
    cs_fe_ts "He is the one who can hear the horn."
    pause 0.6
    cs_fe_akai "Bring a white branch."
    return

label cs_df_northern_campaign:
    show screen cs_matsuda_fe_phase_card("THE SIXTH WINTER", "NORTHERN CONCORD", "The Salt Gate road / eleven days before the battle")
    with dissolve
    pause 2.0
    hide screen cs_matsuda_fe_phase_card
    play music night_a fadein 1.0
    scene bg greywake_rival_keep with dissolve_scene_full
    show df_rival at t21
    show df_sam at t22
    cs_fe_captain "The upland barons have joined the Concord. On condition their men stay under their own officers."
    cs_fe_rival "They can keep the officers. Can they bring oats?"
    cs_fe_captain "They ask whether we can provision their horses."
    cs_fe_sam "A stirring beginning to an alliance."
    cs_fe_rival "Tell them the men eat before the horses. Put it in the treaty if they need wax on it."
    cs_fe_scout "Salt Gate is ours again."
    cs_fe_sam "Again?"
    cs_fe_scout "The third assault took the lower street. They burned the warehouses before withdrawing."
    cs_fe_sam "Then what did you take?"
    cs_fe_scout "The lower street."
    pause 0.4
    cs_fe_rival "And the regiment?"
    cs_fe_scout "Their banner came back with the stretcher party."
    cs_fe_sam "Who was carrying it?"
    cs_fe_scout "No one you knew."
    cs_fe_sam "You don't know who I knew."
    cs_fe_rival "Sam. Go and see."
    hide df_sam
    show df_rival at t11
    cs_fe_captain "The capital has ordered us to recover the coast before the snow."
    cs_fe_rival "With the regiment that just came back on a stretcher?"
    cs_fe_captain "The order was written last month."
    cs_fe_rival "Send them this month's return. Don't round anything up."
    scene bg greywake_west_ridge with wipeleft_scene
    show df_sam at t21
    show df_rival at t22
    cs_fe_sam "They came across the upland road in the dark. No boots on the front rank."
    cs_fe_rival "Trying to stay quiet?"
    cs_fe_sam "Trying to find boots."
    cs_fe_rival "Our losses?"
    cs_fe_sam "Nine before the horn. Four more while we were arguing about whose horn it was."
    cs_fe_rival "Prisoners?"
    cs_fe_sam "Two. One asked if surrender came with breakfast."
    cs_fe_rival "Does it?"
    cs_fe_sam "I gave him mine. Don't look so fucking surprised."
    cs_fe_rival "I was wondering what you ate."
    cs_fe_sam "The second man's breakfast. I remain a terrible person."
    cs_fe_guard "Commander. The displaced column is refusing to move."
    cs_fe_rival "Refusing?"
    cs_fe_guard "They say the axle will fail. The escort says it's an excuse."
    cs_fe_rival "Which of them inspected the axle?"
    cs_fe_guard "The woman in the third wagon."
    cs_fe_rival "Give her tools."
    cs_fe_guard "She is on the detention list. Family of a southern officer."
    cs_fe_rival "Then she can repair it under arrest. Remove the rope from her hands."
    cs_fe_sam "The general wanted them where Akai could see them."
    cs_fe_rival "She can see our soldiers. That should occupy her."
    cs_fe_sam "You're giving away a useful threat."
    cs_fe_rival "I've read the lists, Sam. There are children on both sides of every surname."
    cs_fe_sam "I know."
    cs_fe_rival "Then stop making me say it."
    scene bg greywake_rival_keep with dissolve_scene_full
    show df_rival at t21
    show df_sam at t22
    cs_fe_captain "The western column reached Greywake. The southern one won't."
    cs_fe_rival "Cut off?"
    cs_fe_captain "Disbanded. They divided the last stores and went home."
    cs_fe_sam "At least one officer in this country has had a good idea."
    cs_fe_rival "The Compact is coming here too."
    cs_fe_captain "Every banner they can still raise."
    cs_fe_rival "So this is where it finishes."
    cs_fe_sam "I've heard that before. First winter. Second winter."
    cs_fe_rival "There isn't another road, Sam."
    cs_fe_captain "Both granaries hold winter rations and seed. The sacks have different seals."
    cs_fe_sam "Men are eating seed already."
    cs_fe_rival "Then in spring they'll be eating the men who told them to. Put guards on both stores."
    cs_fe_captain "Our allies have brought separate locks."
    cs_fe_rival "Remove them."
    cs_fe_captain "The barons will object."
    cs_fe_rival "I will be outside. They can object while helping me count the sacks."
    cs_fe_sam "Akai sent a herald. White branch."
    cs_fe_rival "Move our archers back."
    cs_fe_sam "You haven't heard the terms."
    cs_fe_rival "I'd like to hear them before somebody improves them with an arrow."
    return

label cs_df_greywake_orders:
    scene bg greywake_field_dawn with dissolve_scene_full
    show screen cs_matsuda_fe_phase_card("THE LAST ROAD", "GREYWAKE FIELD", "Twenty-three southern banners. Nineteen northern. No reserve army.")
    pause 2.0
    hide screen cs_matsuda_fe_phase_card
    play music flight fadein 1.0
    # The parley is visible from the chosen command. Neither council is revisited.
    show df_akai at t21
    show df_rival at t22
    if cs_df_side == "akai":
        cs_fe_akai "I sent terms to your capital. The messenger came home carrying the seal. No letter."
        cs_fe_rival "It took them three weeks to tell me to hold a town that had burned down."
        cs_fe_akai "Then let's leave them out of this."
    else:
        cs_fe_rival "Your herald said you could speak for all twenty-three banners."
        cs_fe_akai "I can make them stop long enough to hear me. This morning that will have to do."
        cs_fe_rival "Mine too."
    cs_fe_akai "Open the road. Release the detained families. We divide the stores by mouths, not flags."
    cs_fe_rival "My wounded pass first. Your cavalry stays west of the river until they're through."
    cs_fe_akai "If I stand here another day, I lose the Orra towns. They have people in those wagons."
    cs_fe_rival "If I let your companies through first, the barons cut the road behind us."
    cs_fe_akai "So you can't move and I can't wait."
    cs_fe_rival "I can bring you one other thing."
    cs_fe_akai "Say it."
    cs_fe_rival "The command compact. All our seals. If I fall to you, my banners stop. No next commander. No seventh winter."
    cs_fe_akai "And you want mine."
    cs_fe_rival "I don't want to kill your captains one at a time while someone miles away appoints replacements."
    cs_fe_akai "My captains signed at dawn."
    cs_fe_rival "You knew I'd ask?"
    cs_fe_akai "I knew what was left to offer."
    cs_fe_rival "The wounded and the grain stay outside it. Whoever can reach them gets them clear."
    cs_fe_akai "And if neither of us can stand?"
    cs_fe_rival "Then nobody gets to call it a victory."
    pause 0.7
    play sound audio.sfx_wham
    with hpunch
    cs_fe_scout "The south ford! They've started without the horn!"
    if cs_df_side == "akai":
        hide df_rival
        show df_akai at t22
        show gregor at t21
        cs_fe_gregor "Varn's men saw the coast shields. Gregor can stop them or hold the ford. He cannot do both."
        cs_fe_akai "Hold the ford. I'll get the order down the line."
        cs_fe_gregor "There are boys wearing those shields now."
        cs_fe_akai "I know."
        cs_fe_gregor "Gregor will try to tell them."
        hide gregor
        show gary at t21
        cs_fe_gary "Three wagon groups. The hinge is on the northern one."
        cs_fe_akai "I can't send the army after your mother."
        cs_fe_gary "I wasn't asking you to. I need a lane and someone to keep it open."
        cs_fe_akai "You get your company. Decide what you can bring back."
        cs_fe_gary "People. If I have to leave the horses."
        hide gary
        show leif at t21
        cs_fe_leif "Sam's flag is below the western crest. He wants me to climb."
        cs_fe_akai "Then for once disappoint him. There's a road around the ridge."
        cs_fe_leif "And leave him there?"
        cs_fe_akai "Leif, if you die for a better view I will have your statue face a wall."
        hide leif
        show df_tsubaki at t21
        cs_fe_ts "I'll stay between Gregor and the crossing. Send the wounded toward my banner."
        cs_fe_akai "You won't be able to reach everyone."
        cs_fe_ts "Then don't make them die where I can almost reach them."
        cs_fe_captain "Vey's archers and Bran's militia are ready. The other banners will hold the flanks while you take the crossing."
        cs_fe_akai "Tell them what the two stores contain. Let them know what they're holding for."
    else:
        hide df_akai
        show df_rival at t21
        show df_sam at t22
        cs_fe_sam "The coast companies recognized Varn's colors. They don't want terms."
        cs_fe_rival "They'll obey the compact. Get Orren in front of them."
        cs_fe_sam "He has forty shields."
        cs_fe_rival "Then lend him yours."
        cs_fe_sam "You keep turning my dramatic last stand into a job for two people."
        cs_fe_rival "I like jobs that finish with two people."
        cs_fe_captain "Rusk's upland riders are waiting by the eastern store. Nera has the road; Sable is watching the crossing."
        cs_fe_rival "Keep the riders away from the ford when the thaw rises. The bridge stays open."
        cs_fe_captain "And the detention wagons?"
        cs_fe_rival "Move them. Ours, theirs, whoever has a hand free. Leave no one tied to a wheel when the water comes."
        cs_fe_sam "That will look a great deal like helping Gary."
        cs_fe_rival "If Gary gets there first, help Gary."
        cs_fe_sam "And if he brings a lance?"
        cs_fe_rival "Try talking before you bury it in him."
        cs_fe_medic "Ilen's hospital detail is ready. We have clean cloth for one hard engagement."
        cs_fe_rival "After that?"
        cs_fe_medic "We turn it over."
        pause 0.4
        cs_fe_rival "Put your flag where the southern cleric can see it. She may need somewhere to send people."
    scene bg greywake_field_dawn with dissolve_scene_full
    cs_fe_scout "Snow over Lake Orra. It's moving faster than the columns."
    if cs_df_side == "akai":
        show df_akai at t11
        cs_fe_akai "Get the stores under cover. When the ford rises, take the bridge."
        cs_fe_akai "And when somebody falls, go back for them while there is still someone to bring back."
    else:
        show df_rival at t11
        cs_fe_rival "No pursuit past a fallen company. Bring our people in before you look for another fight."
        cs_fe_rival "The capital can call that cowardice when it has enough hands to bury them."
    return

label cs_df_field_silence:
    stop music fadeout 1.2
    scene bg greywake_field_aftermath with dissolve_scene_full
    show screen cs_matsuda_fe_stage_overlay
    # The on-map paired exchange has already resolved. The camera follows only
    # the chosen lord; the rival speaks here in their shared physical space.
    if cs_df_side == "akai":
        show df_akai at t21
        show df_rival at t22
        cs_fe_akai "Don't pull it out."
        cs_fe_rival "Yours or mine?"
        cs_fe_akai "Either."
    else:
        show df_rival at t21
        show df_akai at t22
        cs_fe_rival "I can't feel my left hand."
        cs_fe_akai "It's still there."
        cs_fe_rival "Useful report. Thank you."
    cs_fe_akai "Are they stopping?"
    cs_fe_rival "I can hear the horns."
    cs_fe_akai "Those could be ours."
    cs_fe_rival "There's a second one. Wait."
    pause 1.0
    cs_fe_akai "...There."
    scene cg dead_fantasy_greywake_draw with dissolve
    $ cg_unlock("Greywake Draw")
    pause 1.8
    scene bg greywake_field_aftermath with dissolve_scene_full
    if cs_df_side == "akai":
        show df_akai at t11
    else:
        show df_rival at t11
    cs_fe_medic "Don't try to stand. Cut the straps, you two. Lift together."
    if cs_df_result["civilians_evacuated"] == 40:
        cs_fe_scout "All three groups reached shelter. Forty counted at the north road."
        if cs_df_side == "akai":
            cs_fe_akai "The woman with the hinge?"
            cs_fe_scout "Still arguing with the driver."
            cs_fe_akai "Good."
        else:
            cs_fe_rival "Take their names off the detention roll. Every one."
            cs_fe_scout "Whose authority?"
            cs_fe_rival "Mine. I haven't finished bleeding yet."
    elif cs_df_result["civilians_evacuated"] > 0:
        cs_fe_scout "[cs_df_result[civilians_evacuated]] people through. We lost the rest."
        if cs_df_side == "akai":
            cs_fe_akai "Did someone count them at the other shelter?"
        else:
            cs_fe_rival "Check the lower road before you close the roll."
        cs_fe_scout "We checked both."
        pause 0.6
    else:
        cs_fe_scout "No wagons reached the shelter."
        cs_fe_medic "Keep pressure on it. Commander, look at me."
        cs_fe_scout "I can come back."
        if cs_df_side == "akai":
            cs_fe_akai "No. Finish."
        else:
            cs_fe_rival "Stay. I asked for the return."
    if cs_df_result["supplies_secured"] == 2:
        cs_fe_captain "Both stores under guard. They're issuing grain to either coat."
        cs_fe_medic "Keep the seed separate. Write it on the sacks if you have to."
    elif cs_df_result["supplies_secured"] == 1:
        cs_fe_captain "One store secured. The quartermasters are dividing what we brought in."
        cs_fe_medic "They'll need smaller measures."
    else:
        cs_fe_captain "Neither store secured. No grain came back with the columns."
        cs_fe_medic "Then get the horses under cover. We're going to need everything that can pull a cart."
    cs_fe_scout "The ridge has stopped. The ford too. There are still shots past the keep."
    if cs_df_side == "akai":
        cs_fe_akai "Send the signed order again. Send someone they know."
    else:
        cs_fe_rival "Show them my seal. If the captain can't read it, find someone who can."
    cs_fe_medic "You can give orders from the stretcher."
    scene black with dissolve_scene_full
    pause 0.8
    return

label cs_df_table:
    hide screen cs_matsuda_fe_stage_overlay
    scene bg living_room_tabletop_night with dissolve_scene_full
    play music theme_matsuda_a fadein 0.7
    show sam neut at t61
    show matsuda neut at t62
    show asahina neut at t63
    show tsubaki neut at t64
    show monika forward casual neut cm oe nobl rdown ldown at t65
    show mc neut at t66
    ma "Both lords down. Both command compacts invoked. Greywake is a draw."
    sa "Oh, fuck your compacts."
    show matsuda annoyed
    ma "You signed one."
    sa "I signed a lot of shit! There was a customs form for my sword!"
    if cs_df_result["unit_status"]["sam"] == "dead":
        sa "My man is dead in a ditch and the two leads get matching orthopedic problems."
    elif cs_df_result["unit_status"]["sam"] == "wounded":
        sa "I have more bandages than skin and neither of you even had the courtesy to win."
    else:
        sa "I kept him alive through the whole fucking field. He has to walk home and tell people this was the plan."
    ma "It was on the first page! Last Exchange, simultaneous damage!"
    mc "Being informed has done very little for my stab wound."
    show asahina angry
    if cs_df_result["unit_status"]["gregor"] == "dead":
        ah "Gregor's dead. Don't do the funny commander voice over his square."
        ma "I wasn't--"
        ah "You were winding it up. I can see your fucking shoulders."
    elif cs_df_result["unit_status"]["gregor"] == "wounded":
        ah "Gregor would like to invoice somebody for the contents of his body. Most of them are on your ford."
        ma "He's on the hospital roll."
        ah "Gregor was stapled! There is a difference!"
    else:
        ah "Gregor survived. Gregor would like that written in ink before you invent another weather condition."
        ma "I don't invent weather conditions."
        ah "You gave sleet a fucking initiative score!"
    show tsubaki worried
    ts "The hospital list. Can we finish it?"
    if cs_df_result["civilians_evacuated"] == 40:
        m forward casual happ om oe nobl rdown ldown "Forty out. All forty. I'm putting a box around that."
        sa "Of course Gary's family gets the deluxe evacuation package."
        m forward casual angr om oe nobl rhip lpoint "Oh, bite me. Somebody actually spent the actions."
        if cs_df_side == "rival":
            mc "Our actions, for at least part of that."
            m forward casual neut om oe nobl rdown ldown "Yes. Thank you. Gary is going to hate writing that letter."
    elif cs_df_result["civilians_evacuated"] > 0:
        m forward casual sad om oe nobl rdown ldown "[cs_df_result[civilians_evacuated]] out of forty. Stop calling it the wagon win."
        ma "I didn't say win."
        m forward casual angr om oe nobl rhip lpoint "Then don't reach for the green marker."
    else:
        m forward casual sad om oe nobl rdown ldown "I wrote their names on the backs of the tokens."
        show matsuda worried
        ma "Monika--"
        m forward casual angr om oe nobl rhip lpoint "Leave them face up. I know who's on them."
    show sam angry
    sa "You still built a whole war where your self-insert has a reserved appointment with the other protagonist."
    show matsuda angry
    ma "Yes! The lords' ending is fixed! The fucking burial list wasn't!"
    ma "I didn't move your companies for you. I'm not moving the bodies afterward because I don't like where they landed."
    mc "We can be angry about a rule we agreed to."
    ma "Apparently at considerable volume!"
    play sound audio.sfx_wham
    with vpunch
    show asahina shocked
    ah "Jesus! You hit the table hard enough to annex the chips!"
    show tsubaki annoyed
    ts "The hospital list."
    sa "One second, Tsubaki, I--"
    stop music
    play sound audio.sfx_wham
    show monika forward casual vang om oe nobl rhip lpoint
    with vpunch
    m "FINISH THE FUCKING LIST."
    pause 0.3
    mc "My knee. Again."
    m forward casual angr om oe nobl rhip lpoint "She's asked twice. The third time I'm feeding somebody this die."
    show matsuda worried
    ma "Right. Tsubaki."
    # The game already resolved triage; the table cannot reroll it away.
    if cs_df_result["unit_status"]["tsubaki"] == "dead":
        ma "They didn't reach her before she bled out. She's dead."
        show tsubaki sad
        ts "Leave her name on the sheet."
        ma "Of course."
        ts "And don't give her last words. I would have said them."
        ma "Okay."
        pause 0.6
        m forward casual sad cm oe nobl rdown ldown "..."
    elif cs_df_result["unit_status"]["tsubaki"] == "wounded":
        ma "She's on the hospital roll. Alive. No extra check."
        show tsubaki crying
        ts "You could have said that before everyone started breaking the furniture."
        ma "Yes. I could have."
        ts "I'm keeping the little bandage token."
    else:
        ma "Your cleric is alive. Still working."
        show tsubaki frustrated
        ts "Then she wants help. She's not doing both armies by herself while you two pose on stretchers."
        mc "A reasonable staffing complaint."
        ts "Pick up a bucket."
    if cs_df_result["unit_status"]["gary"] == "dead":
        ma "Gary is on the dead roll too."
        m forward casual sad om oe nobl rdown ldown "Put the letter with him. The one in his tent."
        ma "The goodbye letter?"
        m forward casual sad om oe nobl rdown ldown "The address is on the outside. Somebody can still deliver it."
    elif cs_df_result["unit_status"]["gary"] == "wounded":
        m forward casual sad om oe nobl rdown ldown "Gary's hospital, too. Spell it correctly. He's going to complain in writing."
    else:
        m forward casual neut om oe nobl rdown ldown "Gary can take a bucket. He has hands free now."
    show sam embarrassed
    sa "...Sorry, Tsubaki."
    ts "You can give me your second now."
    pause 1.0
    show matsuda sad
    ma "The field stops. It takes three days to make the last companies believe the orders."
    ma "The armies exchange their hospital lists before they exchange prisoners. There are names on both."
    if cs_df_result["supplies_secured"] == 2:
        ma "The quartermasters use both granaries as neutral ground. By thaw, the first seed carts are moving south."
    elif cs_df_result["supplies_secured"] == 1:
        ma "One granary feeds the hospitals. The first peace delegation goes abroad to buy seed on credit."
    else:
        ma "The peace delegation leaves to beg for grain. People keep dying after the soldiers stop."
    ma "Nobody signs an order for a seventh campaign. There isn't a company left willing to carry it."
    mc "And the commanders?"
    ma "Different hospitals. Neither can travel."
    ma "They start writing because there are still things on the map they have to settle."
    show asahina unamused
    ah "If this becomes a love letter I'm biting your pencil in half."
    ma "The first letter asks for six wagons and a surgeon."
    ah "Acceptable."
    play music archive fadein 1.5
    show matsuda worried
    ma "...I'm leaving the map up until next week. If anyone wants to put anything on it."
    if cs_df_result["unit_status"]["gregor"] == "dead":
        ah "I'm putting Gregor's name on the ford."
        ma "I'll get the fine pen."
    else:
        ah "Gregor would like a bridge named after him. One that doesn't try to fucking eat him."
        ma "I'll put it in the rebuilding costs."
    if cs_df_result["unit_status"]["sam"] == "dead":
        sa "My next guy is a carpenter. Violently opposed to ridges."
    else:
        sa "My guy is retiring. If you want a sequel, invade his fishing shed."
    show matsuda teasing
    ma "Does the shed have a defensive bonus?"
    sa "It has a lock. You're not fucking invited."
    m forward casual neut om oe nobl rdown ldown "There's food in the kitchen. Bring the sheets if you need them."
    show tsubaki neut
    ts "And leave the dice here."
    pause 0.6
    return
