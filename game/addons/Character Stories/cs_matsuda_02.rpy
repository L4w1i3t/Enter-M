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
#   roster "Asahina" -> cs_asahina_rhythm (the prelude, on her stage) ->
#       cs_asahina_rhythm_play -> asahina_rhythm_mode(ar_story=True) ->
#       clear -> _victory (+ Matsuda) | failed -> _defeat | quit -> _quit |
#       backed out of song select -> _backout. Runbacks skip song select;
#       "never mind" and "maybe later" return to msbf_roster_choice.
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
        play music theme_matsuda_a
        scene bg matsudavr with dissolve_scene_full
        show matsuda curious at t53 zorder 2
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
                                ma "Tsubaki? ...No. No, I don't have one for her."
                                ma "I tried. Every version sounded like me putting words in her mouth, so I stopped. I left a card on the door: {i}ASK TSUBAKI FIRST.{/i}"
                                show matsuda shocked
                                ma "...Where's the card?"
                                ma "Hey. Why is the light on?"
                                ma "Tsuba?"
                                show matsuda worried
                                ma "Don't touch that door. Tsuba, look at me. Open it from your side."
                                ma "...It just locked."
                                jump tsubakimode
                            "Asahina":
                                show matsuda curious
                                ma "...His sister? ...Yeah, okay. She's already picked the song anyway."
                                show matsuda unamused
                                ma "Apparently my microphone wasn't 'the right shape,' and I won't exactly question the judgment of someone who thwarted me in a rhythm game before."
                                ma neut "Her room's just that way. Follow the brightly colored arrows and you should be there."
                                jump cs_asahina_rhythm
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

    play music day_a
    scene bg matsudavr with dissolve_scene_full

    show matsuda smug at t53 zorder 2
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
    if _return == "cancel_setup":
        jump msbf_cancel_setup
    call screen msbf_party_select
    if _return == "cancel_setup":
        jump msbf_cancel_setup
    $ _msbf_party_ids = _return

label cs_matsuda_02_battle:
    $ msbf_clear_battle_watch()
    $ _msbf_prev_quick_menu = quick_menu
    $ quick_menu = False
    $ msbf_battle_state = msbf_new_battle(_msbf_party_ids, id_mode=_msbf_id_mode)
    $ msbf_battle_menu_locked = True

    # Keep the authored arena underneath every entrance and its dissolve.
    scene expression msbf_seer_plate(2 if _msbf_id_mode else 1):
        xysize (1280, 720)

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

    play music day_c
    scene bg matsudavr with dissolve_scene_full
    show matsuda neut at t53 zorder 2

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
        ma "{i}*sigh*{/i} ...Anyway. Good fight."
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


# =============================================================================
# THE ASAHINA ACT  (roster "Asahina")
# =============================================================================
# Same normal-Seer-clear gate as the other alternate bosses. The Arcade calls
# asahina_rhythm_mode directly and never sees this framing. Like Kotonoha's act,
# every way out of the mode lands on a scene: a clear, a failed run, a walk-off
# mid-song, or backing out of song select before singing a note.
#
# asahina_rhythm_mode(ar_story=True) returns the last result dict, or None when
# song select was backed out of. A runback passes the chart id back in, which
# skips song select; the practice-clear runback deliberately does not, so the
# player can reach the practice switch.
# =============================================================================

default _ahr_restart_id = None
default _ahr_result = None
default _ahr_briefed = False

label cs_asahina_rhythm:
    $ _ahr_restart_id = None
    $ _ahr_tried = any(record.get("attempts", 0) for record in (persistent.asahina_rhythm_records or {}).values())
    $ _ahr_returning = persistent.asahina_rhythm_cleared or _ahr_tried or _ahr_briefed
    show matsuda at thide
    hide matsuda
    stop music fadeout 1.0
    scene black with dissolve_scene_full
    pause 0.6
    play music day_a
    scene asarhythm_stage with dissolve_scene_full
    show asahina smug at t53 zorder 2

    if persistent.asahina_rhythm_cleared:
        ah "Oh, look who came crawling back."
        show asahina unamused
        ah "Before you ask, yes, I've been practicing. Every single day. Out of spite."
        show asahina smug
        ah "You beat me once. Nobody saw it. Matsuda doesn't count as a somebody."
        ah "Coat's on the amp. Mic's on the stand. Same song, same rules."
    elif _ahr_tried:
        ah "Back for more? Good."
        show asahina teasing
        ah "I was starting to feel bad about last time. Joking. I felt amazing."
        ah "Coat's on the amp, mic's on the stand. Try to keep up this time."
    elif _ahr_briefed:
        ah "Oh, you came back. The coat's still on the amp."
        show asahina unamused
        ah "I'm not explaining everything again. The arrows on the right are yours. Hit them."
    else:
        ah "There you are! Hold this."
        show asahina teasing
        ah "You get the crappy mic, 'cause mine's built into my phone."
        ah "...Don't ask how. Spacetime shenanigans or something. We're in an AU, after all, so I guess anything goes."
        show asahina unamused
        ah "Matsuda tried to lend me hers. It has a little cape on it."
        ah "I'm not singing into something with a cape. Nobody should sing into something with a cape."
        show asahina thinking
        ah "And... let's see, what should you wear...?"
        ah "Hmmmmm..."
        show asahina smug
        ah "Ah! I got it. How about you wear the skin of my brother?"
        ah "There's a spare costume in the back, so chop chop! I don't have all day!"
        "The spare costume is a sleek black leather coat and a pair of black trousers, folded on top of an amp."
        show asahina shocked
        ah "Oh, that's creepy."
        ah "That's so creepy. You even stand like him."
        show asahina unamused
        ah "Stop standing like him."
        show asahina neut
        ah "It's a duet, so it's supposed to be me and him."
        ah "I asked. He said singing in public is 'a disturbance of the peace.'"
        show asahina frustrated
        ah "It's a stage! Disturbing the peace is the entire point of a stage!"
        show asahina smug
        ah "Also, Matsuda keeps telling people the dance machine was rigged."
        ah "It wasn't. I just beat her by a lot. By so much."
        ah "So this time it's a real stage and a whole song, and she can watch me do it again from her perch on the speaker."
        show asahina determined
        ah "Okay. Rules."
        ah "I sing first. My arrows are on the left, and you don't touch those. Yours come up on the right."
        ah "Hit them when they cross the outlines. D, F, J, K, or the arrow keys. I don't care which, just pick one and stick with it."
        ah "The long ones, you hold until the tail runs out. Let go early and it counts against you."
        ah "Mashing buttons during your part counts against you too. I'll see it on the bar."
        ah "If the bar ends up all the way on my side, you're done. If you get to the end, you win. That's not happening, but those are the rules."
        show asahina teasing
        ah "There's a practice switch on the song screen if you're scared. It doesn't count, and I'll know."
        ah "Escape pauses. Don't pause on me unless your house is on fire."

    $ _ahr_briefed = True
    menu:
        "Let's do this.":
            show asahina happy
            ah "Obviously. Mic up."
        "Go over the rules again." if _ahr_returning:
            show asahina unamused
            ah "Seriously?"
            ah "Left side is me. Right side is you. Hit your arrows on the outlines and hold the long ones."
            ah "Don't mash. If the bar ends up on my side, you lose. There, done."
        "Why a rhythm game?" if not _ahr_returning:
            show asahina curious
            ah "Because it respects athletic ability."
            show asahina smug
            ah "And because I'm good at it. Next question."
        "Actually, never mind.":
            show asahina neut
            ah "...Oh."
            show asahina annoyed
            ah "No, whatever, go. Leave the coat on the amp."
            show asahina at thide
            hide asahina
            stop music fadeout 1.0
            scene black with dissolve_scene_full
            play music theme_matsuda_a
            scene bg matsudavr with dissolve_scene_full
            show matsuda shocked at t53 zorder 2
            ma "Back already?! She hadn't even finished the sound check!"
            show matsuda annoyed
            ma "You realize she's going to blame ME for this, right? Not you--me, because apparently I'm the one who 'sent a quitter'--and I will never, ever hear the end of it."
            show matsuda neut
            ma "...Fine. Who else?"
            jump msbf_roster_choice

    show asahina determined
    ah "The song's already picked. There's only one, because it's the best one."
    show asahina at thide
    hide asahina

label cs_asahina_rhythm_play:
    stop music fadeout 1.0
    scene black with dissolve_scene_full
    call asahina_rhythm_mode(arcade=False, ar_story=True, ar_start_id=_ahr_restart_id) from _call_cs_asahina_rhythm_mode
    $ _ahr_result = _return
    $ _ahr_restart_id = None
    # The mode already folded the run into its records; reconcile any completed
    # objective here rather than at the next Archive open.
    $ ach_sync()
    if _ahr_result is None:
        jump cs_asahina_rhythm_backout
    python:
        _ahr_restart_id = _ahr_result.get("chart_id")
        ahr_rank = _ahr_result["rank"]
        ahr_accuracy = "%.2f" % _ahr_result["accuracy"]
        ahr_misses = _ahr_result["misses"]
        ahr_reached = ar_time_label(_ahr_result.get("song_time", 0))
        ahr_length = ar_time_label(_ahr_result.get("song_length", 0))
    if _ahr_result["outcome"] == "quit":
        jump cs_asahina_rhythm_quit
    if _ahr_result["outcome"] == "clear":
        jump cs_asahina_rhythm_victory
    jump cs_asahina_rhythm_defeat

label cs_asahina_rhythm_rerun:
    show asahina at thide
    hide asahina
    jump cs_asahina_rhythm_play

label cs_asahina_rhythm_exit:
    show asahina at thide
    hide asahina
    stop music fadeout 1.5
    scene black with dissolve_scene_full
    pause 1.0
    return

# Backed out of song select without playing.
label cs_asahina_rhythm_backout:
    scene asarhythm_stage with dissolve_scene_full
    play music day_a
    show asahina unamused at t53 zorder 2
    ah "You backed out of the song screen."
    ah "There's ONE song on it. It was already picked. You just had to press the button."

    menu:
        "Okay, okay. Let's go.":
            show asahina determined
            ah "Thank you. The big pink one this time."
            jump cs_asahina_rhythm_rerun
        "Maybe later.":
            show asahina neut
            ah "...Later."
            show asahina annoyed
            ah "That's what he says. Later means never. Everybody knows later means never."
            show asahina at thide
            hide asahina
            stop music fadeout 1.0
            scene black with dissolve_scene_full
            play music theme_matsuda_a
            scene bg matsudavr with dissolve_scene_full
            show matsuda unamused at t53 zorder 2
            ma "Did you seriously put on the whole costume, walk onto her stage, and then just...not sing?"
            ma "Oh, she's going to tell everyone about this--and by everyone I mean me, repeatedly, at length, in a group chat I'm not even supposed to be in!"
            show matsuda neut
            ma "...Who else, then?"
            jump msbf_roster_choice

# Walked off mid-song from the pause menu.
label cs_asahina_rhythm_quit:
    scene asarhythm_stage with dissolve_scene_full
    show asahina shocked at t53 zorder 2
    ah "Hey!"
    show asahina annoyed
    ah "You walked off! In the middle of the song! In the middle of a DUET!"
    if _ahr_result.get("song_time", 0) < 15:
        ah "You didn't even make it out of the intro. The intro is the easy part."
    ah "People don't walk off during my song. That's the one rule I actually care about."

    menu:
        "Sorry. From the top.":
            show asahina unamused
            ah "Apology accepted. Barely. Get back up there."
            jump cs_asahina_rhythm_rerun
        "I have to go.":
            show asahina neut
            ah "...Fine."
            ah "Mic goes back on the stand."
            jump cs_asahina_rhythm_exit

# The bar reached her side, or NO MISSES or FLAWLESS ended the run on one
# mistake. Practice never fails, so this is always a real run.
label cs_asahina_rhythm_defeat:
    scene asarhythm_stage with dissolve_scene_full
    play music day_b
    show asahina smug at t53 zorder 2
    if _ahr_result.get("fail_reason") in ("no_miss", "flawless"):
        ah "You turned on the rule where one mistake ends the song. And then you made a mistake."
        ah "You made it to [ahr_reached] out of [ahr_length]."
        show asahina teasing
        ah "I didn't even have to beat you. You beat you. You picked the switch that beats you."
    else:
        ah "And the bar's all the way on my side. Where it belongs."
        ah "You made it to [ahr_reached] out of [ahr_length]."
        show asahina teasing
        ah "[ahr_misses] misses. I counted along with the screen, just to be sure."
    ah "He'd have lasted about that long too, if that helps."
    show asahina unamused
    ah "It shouldn't. He's really bad at this."

    menu:
        "Run it back.":
            show asahina determined
            ah "Good. From the top. No crying this time."
            jump cs_asahina_rhythm_rerun
        "I'm done.":
            show asahina neut
            ah "...Okay."
            show asahina smug
            ah "I'm keeping the win. You can keep the coat. It looks stupid on him."
            jump cs_asahina_rhythm_exit

label cs_asahina_rhythm_victory:
    scene asarhythm_stage with dissolve_scene_full
    play music day_b

    # Practice and the EASIER modifiers both keep no records, so both land here.
    if _ahr_result.get("practice") or _ahr_result.get("assisted"):
        show asahina smug at t53 zorder 2
        if _ahr_result.get("practice"):
            ah "Congratulations. You beat me with the practice switch on."
        else:
            ah "Congratulations. You beat me with the easy switches on."
        ah "That's like winning a race while I stop to tie my shoes. After you tied them together."
        show asahina teasing
        ah "It doesn't count. The screen literally said it doesn't count."

        menu:
            "Fine. For real this time.":
                show asahina determined
                if _ahr_result.get("practice"):
                    ah "Switch it off first. I'm watching."
                else:
                    ah "Switch those off first. I'm watching."
                # Through song select on purpose: that is where the switch is.
                $ _ahr_restart_id = None
                jump cs_asahina_rhythm_rerun
            "A win's a win.":
                show asahina annoyed
                ah "It is NOT."
                jump cs_asahina_rhythm_exit

    show asahina shocked at t53 zorder 2
    ah "No. No, hold on."
    show asahina frustrated
    ah "That was the whole song. You did the whole song."
    if ahr_rank == "S+":
        ah "Without missing ONE? Were you practicing? When were you practicing?!"
    elif ahr_rank in ("S", "A"):
        show asahina unamused
        ah "[ahr_accuracy] percent. That's not bad. That's really annoying."
    else:
        show asahina smug
        ah "At [ahr_accuracy] percent, though. You won ugly, and I want that on the record. Ugly."
    show asahina unamused
    ah "Matsuda's going to say the stage was rigged. It wasn't. I built it."
    show asahina neut
    ah "...He wouldn't have finished it. He'd have quit in the second verse and said his hands were cold."
    ah "So you did his part. It was good."
    show asahina embarrassed
    ah "Stop looking at me like that. It was one song."
    show asahina determined
    ah "Rematch next time. I'm picking a harder chart. I'm picking the hardest one."

    show asahina at thide
    hide asahina
    stop music fadeout 1.0
    scene black with dissolve_scene_full
    pause 0.6
    play music theme_matsuda_a
    scene bg matsudavr with dissolve_scene_full
    show matsuda shocked at t53 zorder 2
    ma "You BEAT her?! On her stage, with her song, wearing her brother?!"
    ma "I was up on that speaker the whole time with a sandwich I was not emotionally prepared to finish, watching that bar slide the wrong way for her in real time!"
    show matsuda happy
    ma "Do you know how long I've waited for somebody to hand her a loss on a dance floor? Since the arcade! Since the MACHINE!"
    show matsuda smug
    ma "I'm telling her the stage had hometown bias. In writing. With a cover letter."
    show matsuda teasing
    ma "Now go on, get out of here! She's already looking for a harder chart, and it has your name on it!"

    stop music fadeout 2.0
    scene black with dissolve_scene_full
    pause 1.5
    return
