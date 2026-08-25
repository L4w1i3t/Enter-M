##### Entry point for the game script #####

label start:

    # Initialize variables for tracking game state
    $ anticheat = persistent.anticheat     # Anti-cheat tracking variable
    $ chapter = 0                          # Current chapter counter
    $ _dismiss_pause = config.developer    # Allow skipping pauses in developer mode
    
    # Initial character name variables before they're properly introduced
    $ s_name = "???"                       # Sayori's name placeholder
    $ m_name = "Girl 3"                    # Monika's name placeholder
    $ n_name = "Girl 2"                    # Natsuki's name placeholder
    $ y_name = "Girl 1"                    # Yuri's name placeholder
    
    # Game interface settings
    $ quick_menu = True                    # Enable the quick menu (bottom UI bar)
    $ style.say_dialogue = style.normal    # Set default dialogue style
    $ in_sayori_kill = None                # Flag for Sayori's death scene
    $ allow_skipping = True                # Allow dialogue skipping
    $ config.allow_skipping = True         # Ren'Py system setting for skipping
    
    ##### In your mod, replace ALL of the following with calls to your own mod's labels

    # Playthrough 1 (Normal route - Act 1)
    ##### You typically don't want to edit the playthrough numbers unless you're doing something akin to DDLC or some sort of NG+
    if persistent.playthrough == 0:
        $ chapter = 0
        call ch0_main from _call_ch0_main                      # Intro/title sequence
        call poem from _call_poem                          # First poem writing sequence
        
        $ chapter = 1
        call ch1_main from _call_ch1_main                      # Day 1 main gameplay
        call poemresponse_start from _call_poemresponse_start            # Character reactions to player's poem
        call ch1_end from _call_ch1_end                       # Day 1 ending
        call poem from _call_poem_1                          # Second poem writing sequence
        
        $ chapter = 2
        call ch2_main from _call_ch2_main                      # Day 2 main gameplay
        call poemresponse_start from _call_poemresponse_start_1            # Poem responses for day 2
        call ch2_end from _call_ch2_end                       # Day 2 ending
        call poem from _call_poem_2                          # Third poem writing sequence
        
        $ chapter = 3
        call ch3_main from _call_ch3_main                      # Day 3 main gameplay
        call poemresponse_start from _call_poemresponse_start_2            # Poem responses for day 3
        call ch3_end from _call_ch3_end                       # Day 3 ending
        
        $ chapter = 4
        call ch4_main from _call_ch4_main                      # Day 4 (festival prep, Sayori confession)
        
        # Create glitch file in game directory after Sayori's death
        python:
            try: renpy.file(config.basedir + "/hxppy thxughts.png")
            except: open(config.basedir + "/hxppy thxughts.png", "wb").write(renpy.file("hxppy thxughts.png").read())
        
        $ chapter = 5
        call ch5_main from _call_ch5_main                      # Sayori death scene and restart
        
        call endgame from _call_endgame                       # Show end screen
        
        return
    
    # Playthrough 2 (Post-Sayori beginning of Act 2)
    elif persistent.playthrough == 1:
        $ chapter = 0
        call ch10_main from _call_ch10_main                     # Glitched intro without Sayori
        jump playthrough2                  # Jump to shared Act 2 content
    
    # Playthrough 2 (Proper Act 2 start)
    elif persistent.playthrough == 2:
        $ chapter = 0
        call ch20_main from _call_ch20_main                     # Act 2 intro with glitches
        
        label playthrough2:                # Common content for Act 2
            call poem from _call_poem_3                      # First poem in Act 2
            
            # Create glitched file in game directory
            python:
                try: renpy.file(config.basedir + "/CAN YOU HEAR ME.txt")
                except: open(config.basedir + "/CAN YOU HEAR ME.txt", "wb").write(renpy.file("CAN YOU HEAR ME.txt").read())
            
            $ chapter = 1
            call ch21_main from _call_ch21_main                 # Act 2 day 1 (glitched)
            call poemresponse_start from _call_poemresponse_start_3        # Glitched poem responses
            call ch21_end from _call_ch21_end                  # Act 2 day 1 ending
            call poem (False) from _call_poem_4              # Second poem with glitches
            
            # Create another glitched file
            python:
                try: renpy.file(config.basedir + "/iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii.txt")
                except: open(config.basedir + "/iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii.txt", "wb").write(renpy.file("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii.txt").read())
            
            $ chapter = 2
            call ch22_main from _call_ch22_main                 # Act 2 day 2 (more glitches)
            call poemresponse_start from _call_poemresponse_start_4        # More glitched responses
            call ch22_end from _call_ch22_end                  # Act 2 day 2 ending
            call poem (False) from _call_poem_5              # Third poem with glitches
            
            $ chapter = 3
            call ch23_main from _call_ch23_main                 # Act 2 day 3 (Yuri death)
            
            # Different response paths based on player's choices
            if y_appeal >= 3:              # If player favored Yuri
                call poemresponse_start2 from _call_poemresponse_start2   # Special Yuri obsession path
            else:
                call poemresponse_start from _call_poemresponse_start_5    # Standard response path
            
            # Early termination for demo version
            if persistent.demo:
                stop music fadeout 2.0
                scene black with dissolve_cg
                "End of demo"
                return
            
            call ch23_end from _call_ch23_end                  # Weekend with Yuri scene
            
            return
    
    # Playthrough 3 (Just Monika - Act 3)
    elif persistent.playthrough == 3:
        jump ch30_main                     # Jump to Monika's room
    
    # Playthrough 4 (Post-deletion - Act 4)
    elif persistent.playthrough == 4:
        $ chapter = 0
        call ch40_main from _call_ch40_main                     # Final sequence with just Sayori
        jump credits                       # Go to credits

# Function to display end screen with a pause
label endgame(pause_length=4.0):
    $ quick_menu = False                   # Disable quick menu during end screen
    stop music fadeout 2.0                 # Fade out music
    scene black                            # Black background
    show end                               # Show end screen
    with dissolve_scene_full               # Transition effect
    pause pause_length                     # Wait for specified time
    $ quick_menu = True                    # Re-enable quick menu
    return

# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc