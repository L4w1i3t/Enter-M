# =============================================================================
# s1disc.rpy -- the pre-Day-1 notice.
#
# The notice does two jobs and should not be allowed to blur them: it gives
# real reader guidance, and it hands the player the story's contract. The
# contract line is on loan from the May 31 trailer -- it promises the SHAPE of
# what is coming (that this is the part worth noticing) without spending any
# of the trailer's events. Keep it restrained; the payoff still lives at the
# end of Chapter 0.5.
# =============================================================================
label disclaimer:
    stop music fadeout 1.0
    call nier_enter from _call_nier_enter_s1disc_1
    call nier_section("NOTICE") from _call_nier_section_s1disc_1
    nier "What follows is a work of fiction. Any resemblance to persons living or dead is coincidental."
    nier "Though coincidence, I have found, is only a pattern the reader has not finished tracing."
    nier "Some of what waits inside is heavier than it first appears. Reader discretion is advised."
    menu (screen="nier_nvl_choice"):
        "Proceed":
            pass
        # Declining returns to the main menu -- it does NOT quit the game.
        # A content warning whose only honest answer closes the application is
        # not offering a choice, it is charging one. The narrator keeps the
        # haughty line because it is in voice; the player keeps their session.
        "Do not proceed":
            call nier_clear from _call_nier_clear_s1disc_1
            nier "...Then I cannot allow you any further."
            return
    call nier_clear from _call_nier_clear_s1disc_2
    nier "Understood."
    nier "This story takes place within one school year, spanning from May to the March that follows." # May 15 to March 7
    # Chapter 0.5 (May 15 to May 31)
    # Chapter 1 (June 1 to July 15)
    # Chapter 2 (July 16 to September 1)
    # Chapter 3 (September 2 to October 15)
    # Chapter 4 (October 16 to December 31)
    # Chapter 5 (January 1 to March 7)
    # Japanese school schedule
    nier "It is a generous-looking stretch of road. Most of it only looks that way from where you are standing now."
    nier "Make the most of your time here."
    call nier_exit from _call_nier_exit_s1disc_1
    pause 2.0
    jump a0515
