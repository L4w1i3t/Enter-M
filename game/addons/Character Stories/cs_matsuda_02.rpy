# =============================================================================
# cs_matsuda_02.rpy  --  Matsuda's character story "Ontological Seer"
#                        (the front-end that launches the BOSS FIGHT minigame)
# =============================================================================
#
# WHAT THIS IS
#   A fourth-wall-aware framing where Matsuda runs the player through her
#   turn-based boss battle. This file is the THIN STORY WRAPPER: intro patter ->
#   party select -> battle -> victory/defeat patter. The actual combat system
#   ("MSBF" = Matsuda's Sick Boss Fight) lives in:
#     game/addons/Matsuda's Sick Boss Fight/battle_logic.rpy  (rules/state)
#     game/addons/Matsuda's Sick Boss Fight/ui.rpy            (battle + select screens)
#     game/addons/Matsuda's Sick Boss Fight/fx.rpy            (shader/particle layer)
#
# WIRING (where this story is referenced from)
#   char_stories.rpy: CharacterStoryEntry("Ontological Seer", ..., "cs_matsuda_02",
#   "cs_matsuda_02_unlocked"); reached via Start("cs_matsuda_02").
#
# MSBF API USED HERE (defined in battle_logic.rpy / ui.rpy)
#   msbf_clear_battle_watch()          -> reset the per-battle watch/anim state
#   call screen msbf_party_select      -> player picks party; returns id list
#   msbf_new_battle(party_ids, id_mode) -> build a fresh battle state object
#   call screen msbf_battle_screen(st) -> run the fight; returns "victory"/other
#   msbf_stop_battle_music(fade)       -> stop the battle BGM
#   msbf_battle_menu_locked            -> guards the battle menu during intros
#
# LOCAL STATE
#   _msbf_id_mode    : harder "Id Mode" toggle (see below)
#   _msbf_party_ids  : chosen party from the select screen
#   _msbf_result     : "victory" or otherwise, returned by the battle screen
#   _msbf_party_downs : party KOs this run, snapshotted off the battle state
#       before it is torn down (the Arcade results card reads it)
#   _msbf_prev_quick_menu : saved quick_menu flag, restored after the fight
#
# UNLOCK FLAGS
#   persistent.cs_matsuda_02_unlocked : gates this story in the hub (set elsewhere
#       / by the master archive flag; this file does not set it).
#   persistent.id_mode_unlocked       : declared here; set True after the FIRST
#       NORMAL-mode victory, which then offers the harder "Id Mode" on re-entry
#       (Id Mode swaps battle BGM to epicbattlephase2 and passes id_mode=True).
#
# FLOW MAP
#   cs_matsuda_02 (intro; if id_mode_unlocked, offer Id vs Normal) ->
#   groundrules -> cs_matsuda_02_setup (party select) -> cs_matsuda_02_battle ->
#       victory -> cs_matsuda_02_victory (unlock Id Mode on normal win) -> return
#       defeat  -> cs_matsuda_02_defeat  (retry / re-pick / quit)
# =============================================================================

default persistent.id_mode_unlocked = False
default persistent.id_check = 0
default _msbf_party_downs = 0
label cs_matsuda_02:
    $ msbf_clear_battle_watch()
    $ _msbf_id_mode = False
    hide screen archive
    hide screen character_stories
    scene black
    stop music fadeout 1.0
    pause 1.0

    if persistent.id_mode_unlocked == True:
        play music enterm
        scene bg ether with dissolve_scene_full
        show matsuda curious at t11 zorder 2
        if persistent.id_check == 1:
            ma "...You know the drill."
            jump msbf_choice1
        ma "Oh, uh, hey again."
        ma "Didn't expect you to be back here so soon, or even at all."
        ma "...What's that expression for? Are you not satisfied with that sick-ass boss battle, or are you just that bored?"
        show matsuda thinking
        ma "Hmmm, what to do..."
        ma "Eh, no point in keeping it backstage. If you're that hungry for more content, I guess I do have something for ya."
        show matsuda smug
        ma "I call it 'Id Mode' and it's, uh...it's something."
        ma "Wanna do that, or do you just want to repeat the previous fight?"
        $ persistent.id_check = 1
        label msbf_choice1:
            pass
        menu:
            "Id Mode":
                $ _msbf_id_mode = True
                show matsuda happy
                ma "Okay! In that case, no cold opener, no warmup act."
                show matsuda determined
                ma "If the second form was the rehearsal, this is where the script starts eating the ground!"
                show matsuda at thide
                hide matsuda
                stop music fadeout 1.0
                scene black with dissolve_scene_full
                jump cs_matsuda_02_setup
            "Normal Mode":
                $ _msbf_id_mode = False
                show matsuda unamused
                ma "I see..."
                jump groundrules
            "I don't want you!":
                $ _msbf_id_mode = False
                show matsuda shocked
                ma "...Huh?"
                ma "You...don't want to see my badass boss fight?"
                show matsuda annoyed
                ma "Then why the hell are you even here?!"
                menu:
                    "I want to fight somebody else.":
                        show matsuda curious
                        ma "Somebody else, eh?"
                        show matsuda unamused
                        ma "...Y'know what, fine. I've been workshopping a couple of alternate acts on the side."
                        ma "A few are still half-built, but a couple of 'em are actually ready to take the stage. Who'd you have in mind?"
                        label msbf_roster_choice:
                            pass
                        menu:
                            "Monika":
                                show matsuda unamused
                                ma "...{i}Her.{/i} Of course it's her."
                                ma "She's been rattling the cage to get a turn since the second I booted this thing up. Fine. FINE."
                                show matsuda determined
                                ma "Don't say I didn't warn you, then. ...Whatever happens in there, don't fall for it."
                                jump monikamode
                            "Kotonoha":
                                # a literal touhou stage (see kotonohamode/kototouhou.rpy)
                                if not persistent.kotomode_cleared:
                                    show matsuda smug
                                    ma "...The QUIET one. Bold. Veeeeery bold."
                                    show matsuda teasing
                                    ma "Just so we're clear on the genre swap: this is a rather...hellish game."
                                jump kototouhou
                            "Tsubaki":
                                show matsuda neut
                                ma "Tsubaki? ...No. I don't have a Tsubaki fight."
                                ma "I never built her one. Every time I tried it came out wrong-- like I was borrowing a shape that didn't fit her-- so I just left the slot empty. Stuck a note on it and told myself later."
                                show matsuda shocked
                                ma "...The light over her door just came on."
                                ma "Tsuba?"
                                show matsuda worried
                                ma "...And it just locked."
                                jump tsubakimode
                            "...Never mind.":
                                show matsuda teasing
                                ma "Pfft. Cold feet. Back to the main event, then."
                                jump msbf_choice1
                    "Actually, I do want you.":
                        show matsuda happy
                        ma "Oh! Okay, then."
                        ma "Then do you want my regular mode, or Id Mode?"
                        jump msbf_choice1
                    "I want to leave.":
                        show matsuda unamused
                        ma "Really...?"
                        ma "Okay, sure, you can leave..."
                        show matsuda angry
                        ma "But just for wasting my precious ass time, I'm booting you ALL THE WAY out!"
                        show matsuda smug
                        ma "See ya!"
                        $ renpy.quit()

    "There are stories with delicate setups, carefully measured pacing, and meaningful emotional turns."
    "Colorful characters, tear-jerking plot twists, badass action sequences, you name it."
    "This is not one of those stories. It's something else entirely."

    play music dailyfantasy
    scene bg ether with dissolve_scene_full

    show matsuda smug at t11 zorder 2
    label groundrules:
        pass
    ma "Okay, ground rules:"
    ma "You get a party of four. I get a massive health bar, an unreasonable amount of confidence, and the music budget."
    ma "Press-turn rules. Hit a weakness or land a crit, you get tempo. Hit something I resist, you lose tempo. Miss, and that's that because I'm generous."
    show matsuda teasing
    ma "Passing only spends half a turn; no full-team bailout button, commit to the bit unless you're a coward."
    ma "Front row takes heat and rear row gets breathing room. Basically, put the squishies where you think squishies belong."
    ma "I'm not telling you how I operate, because why would I? I don't know your strat, so you shouldn't know mine."
    show matsuda unamused
    ma "...Though if you try to solve the fight with one button, I am legally allowed to start reading your inputs."
    ma "SO! We good? Good."
    show matsuda happy
    ma "Let's have some fun!"

    show matsuda at thide
    hide matsuda
    stop music fadeout 1.0
    scene black with dissolve_scene_full

label cs_matsuda_02_setup:
    $ msbf_clear_battle_watch()
    call screen msbf_keyboard_notice
    call screen msbf_party_select
    $ _msbf_party_ids = _return

label cs_matsuda_02_battle:
    $ msbf_clear_battle_watch()
    $ _msbf_prev_quick_menu = quick_menu
    $ quick_menu = False
    $ msbf_battle_state = msbf_new_battle(_msbf_party_ids, id_mode=_msbf_id_mode)
    $ msbf_battle_menu_locked = True

    scene bg battle_setpiece

    # THE ENTRANCE. Both routes get one, and they are deliberately opposite --
    # see the notes on the two screens in cinematics.rpy.
    #
    # Normal: she drops onto the deck out of a howling wind and an ominous
    # heartbeat, with NO battle music yet. The two loops are owned here so they
    # stop cleanly the moment the fight's music kicks in.
    #
    # Id Mode opens on the second bar and so never had an entrance at all -- the
    # fight simply started. It gets one now, and it gets NO build: no heartbeat,
    # no wind, nothing to be patient through. The image just fails to be
    # anything else until it happens to contain her.
    #
    # THE ARCADE GETS THEM TOO, and is no longer gated out. The old rule was
    # "the arcade is game modes without the VN", but an entrance is not story --
    # it is the mode's opening shot, and the arcade is precisely where somebody
    # has come back for the spectacle. Both are click-skippable either way.
    if _msbf_id_mode:
        call screen msbf_idmode_intro
        $ renpy.transition(Dissolve(0.2))
    else:
        $ renpy.music.play(MSBF_INTRO_HEARTBEAT, channel=MSBF_INTRO_HEARTBEAT_CHANNEL, loop=True, fadeout=0.0, fadein=0.4)
        $ renpy.music.play(MSBF_INTRO_WIND, channel=MSBF_INTRO_WIND_CHANNEL, loop=True, fadeout=0.0, fadein=0.8)
        call screen msbf_battle_intro
        $ renpy.music.stop(channel=MSBF_INTRO_HEARTBEAT_CHANNEL, fadeout=0.6)
        $ renpy.music.stop(channel=MSBF_INTRO_WIND_CHANNEL, fadeout=0.9)
        $ renpy.transition(Dissolve(0.4))

    if _msbf_id_mode:
        play music audio.epicbattlephase2
    else:
        play music epicbattlephase1
    call screen msbf_battle_screen(msbf_battle_state)
    $ _msbf_result = _return
    # Snapshot the whole-fight KO tally NOW: msbf_clear_battle_watch() below
    # drops msbf_battle_state to None, and the Arcade results card is rendered
    # long after that.
    $ _msbf_party_downs = getattr(msbf_battle_state, "party_downs", 0)
    # The pause menu is a persistent Show() overlay -- make sure it never lingers
    # over the result dialogue if the battle resolved on a timer while it was open.
    hide screen msbf_pause_menu
    $ msbf_clear_battle_watch()
    $ msbf_stop_battle_music(1.5)
    $ quick_menu = _msbf_prev_quick_menu

    # Pause-menu forfeit ("Quit Fight"): exit cleanly (works in story OR arcade)
    # instead of scoring it as a loss. See pause_menu.rpy / msbf_forfeit.
    if _msbf_result == "quit":
        jump msbf_forfeit

    # EVERYTHING THIS RUN EARNED, AWARDED ABOVE THE ARCADE/STORY SPLIT.
    # The result labels below only render -- if a grant lives inside one of
    # them, the other path silently stops awarding it (that is exactly how the
    # Arcade lost matsuda_id and arcade_id_cleared).
    #
    if _msbf_result == "victory":
        # The "Seer" CG is catalogued under Matsuda's Story but has no show site
        # in the fight yet (assets/cg/seer.png is drawn and unused), so
        # clearing the fight is what stands in for having seen it -- and clearing
        # it from the Arcade counts just the same, which is why the unlock sits
        # up here and not in the victory label. If it ever gets staged, move this
        # onto that beat; that is where it belongs.
        $ cg_unlock("Seer")
        if _msbf_id_mode:
            # Id Mode superboss clear -- nothing else persists this, so grant it,
            # and open the Id Mode tile in the Arcade (its own beaten-once gate).
            $ persistent.arcade_id_cleared = True
            $ ach_grant("matsuda_id")
        else:
            $ persistent.id_mode_unlocked = True
            $ ach_grant("beat_matsuda")

    # One unconditional sync also reconciles any older completed objective. The
    # two exact victory hooks above are what award this run immediately.
    $ ach_sync()

    # ARCADE: skip all VN result dialogue -> shared arcade results card. Inert in
    # the in-story path (arcade_active is only ever set by game/addons/Arcade).
    if arcade_active:
        jump arcade_msbf_result

    if _msbf_result == "victory":
        jump cs_matsuda_02_victory

    jump cs_matsuda_02_defeat

label cs_matsuda_02_defeat:
    scene black with dissolve_scene_full

    ma "Wipe. Hook, line, and sinker."
    ma "You want the salty runback, or are you just a scared wittle baby?"

    menu:
        "Retry with the same party.":
            jump cs_matsuda_02_battle
        "Choose a different party.":
            jump cs_matsuda_02_setup
        "Return to the archive.":
            ma "Aight, 'till next time, bozo."
            return

label cs_matsuda_02_victory:
    scene white
    pause 1.0
    scene black with dissolve_scene_full
    pause 1.0

    play music daily
    scene bg ether with dissolve_scene_full
    show matsuda neut at t11 zorder 2

    if _msbf_id_mode:
        ma "...Okay."
        ma "That one actually got away from me for a second."
        ma "Id Mode is supposed to be the part where I throw every genre into a blender and pretend the button labels still mean anything."
        show matsuda curious
        ma "But you kept reading the pattern anyway."
        ma "...Guess that means it stuck, huh?"
        show matsuda happy
        ma "Good fight. For real this time."
    else:
        show matsuda unamused
        ma "...Damn, I really lost."
        ma "That was actually clean, though. Not gonna lie."
        ma "Team synergy, being able to combat my strategy, hopefully not a whole lot of cheese..."
        ma "That's the good stuff, I tell ya."
        show matsuda smug
        ma "...Though, for the record, I was holding back by about ninety-nine-point-nine percent."
        ma "And for the other record, don't ask me to prove that."
        show matsuda happy
        ma "Second bar was sick, though, right? Tell me the second bar was sick."

        menu:
            "It was sick.":
                show matsuda smug
                ma "Correct answer."
            "It was kind of a lot.":
                show matsuda unamused
                ma "Also correct, but less useful for my ego."
            "It was kinda dogwater.":
                show matsuda annoyed
                ma "Okay, well screw you too, then. Think you're too good to complement my work..."

        show matsuda neut
        ma "*sigh* ...Anyway. Good fight."
        show matsuda teasing
        ma "Now get out before I start tuning a superboss version. Later, nerd!"

    # Marked on VICTORY only, and deliberately BELOW the arcade split: this is a
    # "you read the story" marker, and the Arcade path never plays a line of it.
    # (Everything the FIGHT earns is granted above the split -- see the note
    # there.) The defeat label above offers a runback and a way out; bailing
    # after a wipe is not having read the story either.
    $ cs_mark_completed("cs_matsuda_02")
    stop music fadeout 2.0
    scene black with dissolve_scene_full
    pause 2.0
    return
