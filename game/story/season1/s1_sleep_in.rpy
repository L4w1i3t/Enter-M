# =============================================================================
# s1_sleep_in.rpy  --  THE SLEEP-IN BRANCH (May 25's alarm)
# =============================================================================
#
# WHAT THIS IS
#   May 25's alarm. The player chooses to get up or to ignore it, and ignoring
#   it SKIPS AN ENTIRE SEGMENT OF THE DAY -- the whole library study session
#   with Monika. MC surfaces near noon and reaches the cafe in time for lunch
#   and nothing else.
#
# WHY IT HAS ITS OWN FLAG
#   It was written (Sep 4 2026) as an exception to s1_choices' old rule that
#   no choice may change what happens. The author retired that rule on Sep 21
#   2026, so branching needs no exception now. The flag stays where it is; it
#   works the same either way.
#
# THE CONTRACT
#   1. The branch is SIGNPOSTED. The menu tells the player, in the prompt,
#      that ignoring the alarm costs them a segment of the day. This is not a
#      trap and is not a test of virtue; a player who does not want to sit
#      through a study session is allowed to not sit through it, on purpose,
#      with their eyes open.
#   2. The branch is NOT PUNISHED. Nothing scolds the player, no stat moves,
#      no content is permanently locked. Monika is annoyed because a person
#      who was stood up would be annoyed, not because the game is docking
#      points. She lets him off, once, and means it.
#   3. THE DAY STILL CONVERGES. Both branches arrive at the same cafe table,
#      the same poem payoff, the same yellow sticky note, and the same evening.
#      Only the morning differs, plus a handful of lines downstream that would
#      otherwise reference a study session that did not happen.
#   4. It is READABLE LATER. `s1_slept_in` is a plain flag so later days can
#      remember it. Nothing reads it yet on purpose -- the choices-mattering
#      system waits until the whole story exists.
#
# WHAT READS IT TODAY
#   Only 0525 itself: the branch and scene variants that keep later dialogue
#   from citing shared library events MC missed. Count the current branches
#   in the script instead of relying on a historical line count.
# =============================================================================

default s1_slept_in = False


init python:

    def s1_sleep_in_set(slept):
        """Record the May 25 alarm choice.

        `slept` True means the player ignored the alarm and skipped the study
        session. Kept as its own flag rather than an s1_choices key -- see the
        header.
        """
        store.s1_slept_in = bool(slept)
