# Player-triggered dialogue advance click via config.say_allow_dismiss.
# The engine consumes typewriter completion, skipping and auto-forward separately.
# Three non-repeating cues play on a dedicated SFX-mixer channel so story sounds
# continue uninterrupted. Audio failure must still allow dialogue to advance.

define -50 audio.text_advance_1 = "assets/audio/sfx/textadvance1.ogg"
define -50 audio.text_advance_2 = "assets/audio/sfx/textadvance2.ogg"
define -50 audio.text_advance_3 = "assets/audio/sfx/textadvance3.ogg"

init python:
    # Plain `random`, not renpy.random: renpy.random logs every draw into the
    # rollback entry so rollback can replay it, and a choice of click sound
    # has no business in the rollback log.
    import random as _text_advance_random

    TEXT_ADVANCE_CHANNEL = "text_advance"
    TEXT_ADVANCE_VOLUME = 0.55

    if not renpy.music.channel_defined(TEXT_ADVANCE_CHANNEL):
        renpy.music.register_channel(TEXT_ADVANCE_CHANNEL, mixer="sfx", loop=False)

    _text_advance_last = [None]

    def text_advance_click():
        """config.say_allow_dismiss: sound the click, then allow the dismiss."""
        cues = (audio.text_advance_1, audio.text_advance_2, audio.text_advance_3)
        choices = [c for c in cues if c != _text_advance_last[0]]
        cue = _text_advance_random.choice(choices)
        _text_advance_last[0] = cue
        try:
            renpy.sound.play(cue, channel=TEXT_ADVANCE_CHANNEL, relative_volume=TEXT_ADVANCE_VOLUME)
        except Exception:
            # Presentation only: a missing file or a dead audio device must
            # never stop the player from advancing.
            pass
        return True

    config.say_allow_dismiss = text_advance_click
