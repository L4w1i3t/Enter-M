# =============================================================================
# mika_credits.rpy  --  end card for the Mika lost record
#
# WHAT THIS FILE IS
#   The closing splash sequence shared by both Mika records: title card, the
#   non-profit / support-the-official-release notice, then a Yes/No prompt that
#   either full-restarts the game or quits.
#
#   It is a terminal label ON PURPOSE. The Mika record is framed as a separate
#   piece of media rather than a side story you step back out of, so there is no
#   return path to the archive.
#
# USED BY
#   ch_mika.rpy and ch_mika_rewrite.rpy, at the end of each record.
# =============================================================================
label mika_credits:

    play music mika_ye
    show mika_splash_warning "MIKA: A DDLC SHORT STORY"
    pause 2.0
    show mika_splash_warning "MIKA: A DDLC SHORT STORY":
        easeout 1.0 alpha 0
    pause 1.0
    show mika_splash_warning "WRITTEN AND CODED BY L4W1I3T":
        alpha 1.0
    pause 2.0
    show mika_splash_warning "WRITTEN AND CODED BY L4W1I3T":
        easeout 1.0 alpha 0
    pause 1.0
    show mika_splash_warning "KID MONIKA SPRITES BY NORMALLYAVERAGE":
        alpha 1.0
    pause 2.5
    show mika_splash_warning "KID MONIKA SPRITES BY NORMALLYAVERAGE":
        easeout 1.0 alpha 0
    pause 1.0
    show mika_splash_warning "PARK, CITY, AND STAIRS BACKGROUNDS BY THE DDMC":
        alpha 1.0
    pause 2.5
    show mika_splash_warning "PARK, CITY, AND STAIRS BACKGROUNDS BY THE DDMC":
        easeout 1.0 alpha 0
    pause 1.0
    show mika_splash_warning "CUSTOM BGM BY AN JONE AND YUZZY, BOTH IN THE YOUTUBE AUDIO LIBRARY":
        alpha 1.0
    pause 3.0
    show mika_splash_warning "CUSTOM BGM BY AN JONE AND YUZZY, BOTH IN THE YOUTUBE AUDIO LIBRARY":
        easeout 1.0 alpha 0
    pause 1.0
    show mika_splash_warning "DOKI DOKI LITERATURE CLUB AND ITS ASSETS BY TEAM SALVATO":
        alpha 1.0
    pause 3.0
    show mika_splash_warning "DOKI DOKI LITERATURE CLUB AND ITS ASSETS BY TEAM SALVATO":
        easeout 1.0 alpha 0
    pause 1.0
    show mika_splash_warning "THIS MOD IS A NON-PROFIT FAN BASED NARRATIVE.":
        alpha 1.0
    pause 3.0
    show mika_splash_warning "PLEASE SUPPORT THE OFFICIAL RELEASE." as sp1:
        ycenter 395
    pause 3.0
    show mika_splash_warning "THIS MOD IS A NON-PROFIT FAN BASED NARRATIVE.":
        easeout 1.0 alpha 0
    show mika_splash_warning "PLEASE SUPPORT THE OFFICIAL RELEASE." as sp1:
        ycenter 395
        easeout 0.5 alpha 0
    pause 1.0
    pause 3.0

    "Return to the main menu?"
    menu:
        "Yes":
            $ renpy.full_restart()
        "No":
            "Goodbye, then."
            $ renpy.quit()
