# =============================================================================
# s1disc.rpy -- the pre-Day-1 notice.
#
# The notice does two jobs and should not be allowed to blur them: it gives
# real reader guidance, and it hands the player the story's contract. It uses
# the dedicated main-story threshold format so it cannot be mistaken for MC's
# ordinary first-person narration or for a Nier travel interstitial.
#
# The contract line is on loan from the May 31 trailer -- it promises the SHAPE
# of what is coming (that this is the part worth noticing) without spending any
# of the trailer's events. Keep it restrained; the payoff still lives at the
# end of Chapter 0.5.
# =============================================================================
label disclaimer:
    stop music fadeout 1.0
    pause 3.0
    call msd_enter from _call_msd_enter_s1disc_1
    call msd_card("FICTION", "What follows is a work of fiction. Any resemblance to persons living or dead is coincidental.", 1, 2) from _call_msd_card_s1disc_1
    call msd_card("CONTENT ADVISORY", "Some of what waits inside is heavier than it first appears. Reader discretion is advised.", 2, 2) from _call_msd_card_s1disc_2
    menu (screen="main_story_disclaimer_choice"):
        "Proceed":
            pass
        # Declining returns to the main menu -- it does NOT quit the game.
        # A content warning whose only honest answer closes the application is
        # not offering a choice, it is charging one. The narrator keeps the
        # haughty line because it is in voice; the player keeps their session.
        "Do not proceed":
            call msd_card("ACCESS DENIED", "...Then I cannot allow you any further.", 1, 1) from _call_msd_card_s1disc_3
            call msd_exit from _call_msd_exit_s1disc_1
            return
    call msd_card("CONTRACT", "Understood.", 1, 3) from _call_msd_card_s1disc_4
    call msd_card("TIME INDEX", "We begin in May, with most of a school year still ahead.", 2, 3) from _call_msd_card_s1disc_5 # Act 1: May 15 to March 7
    # Chapter 0.5 (May 15 to May 31)
    # Chapter 1 (June 1 to July 15)
    # Chapter 2 (July 16 to September 1)
    # Chapter 3 (September 2 to October 15)
    # Chapter 4 (October 16 to December 31)
    # Chapter 5 (January 1 to March 7)
    # Japanese school schedule
    call msd_card("ENTRY", "Make the most of your time here.", 3, 3) from _call_msd_card_s1disc_6
    call msd_exit from _call_msd_exit_s1disc_2
    pause 2.0
    jump a0515
