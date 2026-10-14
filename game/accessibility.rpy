# Photosensitive Mode is a persistent Asarhythm setting; other modes do not
# currently consume it. The control therefore lives in Asarhythm's settings.
# enter_m_photosensitive() reads the flag; enter_m_safe_level(value, keep)
# scales selected effects by keep when enabled. See asahina_rhythm_fx.rpy
# for the effect-specific reductions. This is not a game-wide safety guarantee.

default persistent.enter_m_photosensitive = False

init -100 python:

    def enter_m_photosensitive():
        """Whether Photosensitive Mode is on. Safe to call before the default runs."""
        return bool(getattr(persistent, "enter_m_photosensitive", False))

    def enter_m_safe_level(value, keep=0.0):
        """``value`` normally; ``value * keep`` while Photosensitive Mode is on.

        ``keep`` is how much of the effect survives the switch, so the number at
        a call site reads as the decision it is: 0 drops the effect, 1 keeps it
        whole, and anything between is a judgment about how much of that
        particular effect was light and how much of it was the picture.
        """
        return value * keep if enter_m_photosensitive() else value
