# =============================================================================
# s1_choices.rpy  --  CONVERGING EXPRESSIVE CHOICES for Chapter 0.5
# =============================================================================
#
# WHAT THIS IS
#   Chapter 0.5's menus used to be exclusively academic -- "did you remember
#   the lesson?" These are the other kind. The player picks TONE, ATTENTION, or
#   HONESTY; never an outcome. Every branch converges on the same next line:
#   the invitation still happens, the poem still gets written, Himeko still
#   asks her question, Monika still goes to the movie. What changes is which
#   version of MC the player has been playing, plus a handful of later lines
#   that remember it.
#
# WHY A DICT AND NOT ONE FLAG PER CHOICE
#   Later days ask soft questions -- "has he been naming things out loud, or
#   deflecting?" -- that read several answers at once. s1_stance() keeps that a
#   one-liner instead of a pile of booleans, and returns a fallback cleanly
#   when a menu was never reached (dev scene jumps, a save made mid-chapter).
#
# THE RULE FOR ADDING ONE
#   No branch may change an event, a location, who is present, or what anyone
#   decides. If deleting the menu would change the plot, it is the wrong menu.
#   The judgment test from the review applies in reverse here: these choices
#   are never punished, because the story is not asking the player to guess.
#
# THE EXCEPTIONS (there are VERY few, and they do not live in this file)
#   The main story is not choice-driven and is not going to become choice-
#   driven. Where a player action does reach the plot at all, it should
#   overwhelmingly change the ORDER things happen in, not whether they happen.
#   Anything that genuinely branches gets its own store and its own contract,
#   so that this file's promise stays literally true rather than "true except
#   for the ones we forgot to list."
#     - The hidden route -- game/story/dependency_route.rpy. All-or-nothing:
#       the substitution branch at EVERY insertion or the route is over. It
#       keeps a separate ledger precisely because it breaks this contract.
#   Add to this list before writing any second exception, not after.
#
# KEYS IN USE (day -- key -- values)
#   0515  monika_invite   joke | plain | swallowed
#   0515  asahina_plate   joke | quiet | named
#   0517  monika_silence  into | around
#   0517  matsuda_contact brisk | warm | wry
#   0518  movie_time      noon | afternoon    ("evening" retired -- see below)
#   0518  movie_goodbye   joke | plain | linger
#   0519  matsuda_stop    blunt | gentle
#   0522  club_mediation  tsubaki | matsuda | room
#   0523  himeko_first    tired | angry | scared
#   0523  matsuda_callout flat | kind | sharp
#   0524  poem_revision   keep | cut | open
#   0531  arcade_offer    plain | excuse | almost
#
# KEYS FROM OUT-OF-CONTEXT SCENES
#   The dict is shared, so dated scenes written ahead of their chapter register
#   here too rather than inventing a second store. Same contract.
#   0604  ooc0604_wall_spot     claim | room | ask
#   0604  ooc0604_after_the_ask challenge | curious | leave
#   1026  ooc1026_mom_table     steady | ask | joke
#   1030  ooc1030_lunch_table   cover | claim | silent
# =============================================================================

default s1_choices = {}

# 0518 only. The showtime the player picks reshapes four time-of-day lines in
# the date scene. These are plain saved variables rather than a lookup at the
# point of use, because Matsu'Py's [interpolation] cannot call a function and an
# underscore-prefixed temp would not survive a save made mid-date.
#
# The starting values ARE the "noon" row of _S1_MOVIE_SLOTS below (the default
# if the player never picks). `default` is evaluated after every init block, so
# it can read the table -- which beats keeping a second copy of a 200-character
# prose line that would silently diverge the first time either was edited.
default s1_mv_label = _S1_MOVIE_SLOTS["noon"][0]
default s1_mv_street = _S1_MOVIE_SLOTS["noon"][1]
default s1_mv_out = _S1_MOVIE_SLOTS["noon"][2]
default s1_mv_atmos = _S1_MOVIE_SLOTS["noon"][3]

# 0524 only. The closing image the player adds to "Window Seat" is quoted back
# on May 30 and May 31, so the fragment lives here rather than being rebuilt
# from the poem object at each callback site.
default s1_poem_echo = _S1_POEM_ECHOES["vinyl"]

# Exam week. Wrong answers now STAY wrong -- the menus stopped self-correcting,
# which is what makes the save/load rule a real temptation instead of theater.
# Nothing punishes a low count; it only colors a couple of later lines. Only
# the WRONG count is kept: a right-answer tally had no reader anywhere.
default s1_exam_wrong = 0


init python:

    def s1_pick(key, value):
        """Record one expressive choice.

        Converging by contract: callers set a stance and keep going. Nothing in
        the main story may branch control flow on what this stored -- only
        prose may vary, and only for a line or two.
        """
        store.s1_choices[key] = value

    def s1_stance(key, fallback=None):
        """Read a stance back, or `fallback` if that menu was never reached."""
        return store.s1_choices.get(key, fallback)

    def s1_was(key, *values):
        """True when the recorded stance is any of `values`. Convenience for
        the later payoff lines, which usually only care about one grouping."""
        return store.s1_choices.get(key) in values

    # --- 0518: showtime -----------------------------------------------------
    # One call from each menu branch. Records the stance and fills in the four
    # lines the date scene reads back, so the rest of May 18 plays at the hour
    # the player actually chose.
    _S1_MOVIE_SLOTS = {
        "noon": (
            "Noon",
            "Late morning settles over the shopping street in layers: delivery carts along the curb, steam leaking from a noodle shop vent, the soft clatter of shutters being pulled up for lunch.",
            "Outside, the afternoon hits us with the heat it had been saving.",
            "afternoon",
        ),
        "afternoon": (
            "The two o'clock",
            "Early afternoon sits heavy on the shopping street: delivery carts parked in whatever shade they could find, steam leaking from a noodle shop vent, one shutter already half down over a place that gave up on the lunch rush.",
            "Outside, the afternoon has gone soft and orange around its edges.",
            "afternoon",
        ),
        # UNREACHABLE, kept on purpose. The evening showing sells out in
        # Monika's morning texts, so the menu's "Evening." branch is a gag that
        # loops back instead of a third path -- Kotonoha's two "afternoon"
        # greetings at the concession stand are hardcoded and read as errors
        # once the date runs past dark. Restore the branch only alongside
        # time-aware variants for those lines.
        "evening": (
            "The evening showing",
            "Evening comes down over the shopping street in stages: the noodle shop vent still going, shutters rattling closed one storefront at a time, the streetlights deciding all at once that they are needed.",
            "Outside, the street has handed itself over to streetlight and neon while we weren't looking.",
            "evening",
        ),
    }

    def s1_pick_movie_time(slot):
        """Record the 0518 showtime and stage the lines that depend on it."""
        s1_pick("movie_time", slot)
        label, street, out, atmos_key = _S1_MOVIE_SLOTS[slot]
        store.s1_mv_label = label
        store.s1_mv_street = street
        store.s1_mv_out = out
        store.s1_mv_atmos = atmos_key

    # --- 0524: the closing image of "Window Seat" ---------------------------
    # Monika's note is "add one image, not an explanation -- something the seat
    # physically does." All three obey that; none of them explains anything.
    # The stored echo is what May 30 and May 31 quote back.
    _S1_POEM_ECHOES = {
        "vinyl": "the vinyl keeping the shape of his leg for three stops",
        "warmth": "a seat that gives back exactly the warmth it was left",
        "spring": "a spring under the left side counting the stops with him",
    }

    def s1_pick_poem(variant):
        """Record the 0524 revision and stage the fragment later days quote."""
        s1_pick("poem_revision", variant)
        store.s1_poem_echo = _S1_POEM_ECHOES[variant]

    # --- 0526-0528: exam answers ---------------------------------------------
    def s1_exam_mark(correct):
        """Record one marked exam answer. Called from every exam menu branch.

        Nothing reads this to punish the player; it exists so a wrong answer is
        a thing that happened rather than a thing MC talks himself out of, and
        so one or two later lines can acknowledge the paper he actually handed
        in.
        """
        if not correct:
            store.s1_exam_wrong += 1

    def s1_exam_shaky():
        """True if he left enough marks he wasn't sure about to feel it."""
        return store.s1_exam_wrong >= 5
