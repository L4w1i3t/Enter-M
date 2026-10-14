# New Game and the developer date router share the same initial story state.

label start:

    call enter_m_new_game_state from _call_enter_m_new_game_state_1

    # Chapter Select is the player entry in both developer and release builds.
    call chapter_select_open from _call_chapter_select_open_1

    # Canceling Chapter Select returns to the title.
    return


# Direct date entry needs the same baseline that sequential story play inherits.

label enter_m_new_game_state:

    # Initialize variables for tracking game state
    $ exam_guard_reset_for_new_game()
    $ anticheat = persistent.anticheat     # Anti-cheat tracking variable
    $ chapter = 0                          # Current chapter counter
    $ _dismiss_pause = True    # Allow skipping pauses in developer mode

    $ m_name = "Monika"

    # Game interface settings
    $ quick_menu = True                    # Enable the quick menu (bottom UI bar)
    $ allow_skipping = True                # Allow dialogue skipping
    $ config.allow_skipping = True         # Matsu'Py system setting for skipping

    return
