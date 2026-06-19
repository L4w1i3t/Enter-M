##### Entry point for the game script #####

label start:

    # Initialize variables for tracking game state
    $ exam_guard_reset_for_new_game()
    $ anticheat = persistent.anticheat     # Anti-cheat tracking variable
    $ chapter = 0                          # Current chapter counter
    $ _dismiss_pause = config.developer    # Allow skipping pauses in developer mode
    
    # Initial character name variables before they're properly introduced
    $ s_name = "???"                       # Sayori's name placeholder
    $ m_name = "Monika"                    # Monika's name placeholder
    $ n_name = "Girl 2"                    # Natsuki's name placeholder
    $ y_name = "Girl 1"                    # Yuri's name placeholder
    
    # Game interface settings
    $ quick_menu = True                    # Enable the quick menu (bottom UI bar)
    $ in_sayori_kill = None                # Flag for Sayori's death scene
    $ allow_skipping = True                # Allow dialogue skipping
    $ config.allow_skipping = True         # Ren'Py system setting for skipping
    
    ##### In your mod, replace ALL of the following with calls to your own mod's labels

    ##### You typically don't want to edit the playthrough values (persistent.playthrough) unless you're doing something akin to DDLC or some sort of NG+
    if persistent.playthrough == 0:

        ### CALL YOUR STORY SCRIPTS HERE ###
        
        #call dev_scene_manager
        call disclaimer from _call_disclaimer_script_1
