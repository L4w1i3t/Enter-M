default persistent.id_mode_unlocked = False
label cs_matsuda_02:
    $ msbf_clear_battle_watch()
    $ _msbf_id_mode = False
    hide screen archive
    hide screen character_stories
    scene black
    stop music fadeout 1.0
    pause 1.0

    if persistent.id_mode_unlocked == True:
        play music dailyfantasy
        scene bg ether with dissolve_scene_full
        show matsuda neut at t11 zorder 2
        window auto
        ma "Oh, uh, hey again."
        ma "Didn't expect you to be back here so soon, or even at all."
        ma "...What's that expression for? Are you not satisfied with that sick-ass boss battle, or are you just that bored?"
        ma "Hmmm, what to do..."
        ma "Eh, no point in keeping it backstage. If you're that hungry for more content, I guess I do have something for ya."
        ma "I call it 'Id Mode' and it's, uh...it's something."
        ma "Wanna do that, or do you just want to repeat the previous fight?"
        menu:
            "Id Mode":
                $ _msbf_id_mode = True
                ma "Okay. No cold open, no warmup act."
                ma "If the second form was the rehearsal, this is where the script starts eating the stage."
                show matsuda at thide
                hide matsuda
                stop music fadeout 0.8
                jump cs_matsuda_02_setup
            "Normal Mode":
                $ _msbf_id_mode = False
                ma "I see..."
                jump groundrules

    window auto
    "There are stories with delicate setups, carefully measured pacing, and meaningful emotional turns."
    "Colorful characters, tear-jerking plot twists, badass action sequences, you name it."
    "This is not one of those stories. It's something else entirely."

    play music dailyfantasy
    scene bg ether with dissolve_scene_full

    show matsuda neut at t11 zorder 2
    label groundrules:
        pass
    ma "Okay, ground rules:"
    ma "You get a party of four. I get a massive health bar, an unreasonable amount of confidence, and the music budget."
    ma "Press-turn rules. Hit a weakness or land a crit, you get tempo. Hit something I resist, you lose tempo. Miss, and that's that because I'm generous."
    ma "Passing only spends half a turn; no full-team bailout button, commit to the bit unless you're a coward."
    ma "Front row takes heat and rear row gets breathing room. Basically, put the squishies where you think squishies belong."
    ma "I'm not telling you how I operate, because why would I? I don't know your strat, so you shouldn't know mine."
    ma "...Though if you try to solve the fight with one button, I am legally allowed to start reading your inputs."
    ma "SO! We good? Good."
    ma "Let's have some fun!"

    show matsuda at thide
    hide matsuda
    stop music fadeout 0.8

label cs_matsuda_02_setup:
    window hide
    $ msbf_clear_battle_watch()
    call screen msbf_party_select
    $ _msbf_party_ids = _return

label cs_matsuda_02_battle:
    $ msbf_clear_battle_watch()
    $ _msbf_prev_quick_menu = quick_menu
    $ quick_menu = False
    $ msbf_battle_state = msbf_new_battle(_msbf_party_ids, id_mode=_msbf_id_mode)
    $ msbf_battle_menu_locked = True

    scene bg battle_setpiece
    if _msbf_id_mode:
        play music "mod_assets/bgm/epicbattlephase2.ogg" fadein 0.5
    else:
        play music epicbattlephase1
    call screen msbf_battle_screen(msbf_battle_state)
    $ _msbf_result = _return
    $ msbf_clear_battle_watch()
    $ msbf_stop_battle_music(1.5)
    $ quick_menu = _msbf_prev_quick_menu

    if _msbf_result == "victory":
        jump cs_matsuda_02_victory

    jump cs_matsuda_02_defeat

label cs_matsuda_02_defeat:
    scene black with dissolve_scene_full
    window auto

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
    window auto

    if _msbf_id_mode:
        ma "...Okay."
        ma "That one actually got away from me for a second."
        ma "Id Mode is supposed to be the part where I throw every genre into a blender and pretend the button labels still mean anything."
        ma "But you kept reading the pattern anyway."
        ma "...Guess that means it stuck, huh?"
        ma "Good fight. For real this time."
    else:
        ma "...Damn, I really lost."
        ma "That was actually clean, though. Not gonna lie."
        ma "Team synergy, being able to combat my strategy, hopefully not a whole lot of cheese..."
        ma "That's the good stuff, I tell ya."
        ma "...Though, for the record, I was holding back by about ninety-nine-point-nine percent."
        ma "And for the other record, don't ask me to prove that."
        ma "Second bar was sick, though, right? Tell me the second bar was sick."

        menu:
            "It was sick.":
                ma "Correct answer."
            "It was kind of a lot.":
                ma "Also correct, but less useful for my ego."
            "It was kinda dogwater.":
                ma "Okay, well screw you too, then. Think you're too good to complement my work..."

        ma "*sigh* ...Anyway. Good fight."
        ma "Now get out before I start tuning a superboss version. Later, nerd!"

    stop music fadeout 2.0
    scene black with dissolve_scene_full
    pause 2.0

    if not _msbf_id_mode:
        $ persistent.id_mode_unlocked = True
    return
