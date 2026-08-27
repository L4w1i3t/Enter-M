# =============================================================================
# poems_special.rpy  --  the Mika record's special poem
# =============================================================================
#
# Special poem shown during the Mika lost record. The original mod shipped a
# pool of eleven; only "Can You Hear Me?" (#2) survived into the ENTER-M cut,
# so the rest were removed (they live on in git history if ever needed).
#
# Shown by `call mika_poem_special_2` from inside a record.
# =============================================================================

image mika_poem_special2 = "assets/images/poem_special/poem_special2.png" # Can You Hear Me?

label mika_poem_special_2:
    $ quick_menu = False
    play sound page_turn
    show mika_poem_special2 with Dissolve(1.0)
    $ pause()
    play sound audio.mika_laugh
    $ quick_menu = True
    return
