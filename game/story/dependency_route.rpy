# =============================================================================
# dependency_route.rpy  --  LEDGER FOR THE HIDDEN ROUTE ("dependence route")
# =============================================================================
#
# WHAT THIS IS
#   The hidden route is not entered by a choice, and it is not entered by a
#   score. It is entered by an UNBROKEN CHAIN: the player must take the
#   substitution branch at EVERY insertion point in the main story. Every box
#   ticked, in order, with nothing missed. One different menu option -- or one
#   different action anywhere the route is watching -- and the route is over
#   for that playthrough. There is no partial credit and no recovery.
#
#   This is deliberately the strictest gate in the game, and it is the reason
#   the route is allowed to end where it ends. A player who arrives at Dec 24
#   did not drift there; they chose substitution over collaboration every
#   single time they were offered the pair.
#
# WHY NOT A THRESHOLD
#   An earlier draft of this file counted removals and fired at N. That was
#   wrong for this story: a threshold convicts a player of a pattern they only
#   partly chose, and it lets a route that ends in "you became the replacement"
#   trigger off a majority rather than a commitment. All-or-nothing means the
#   ending is only ever addressed to someone who actually did all of it.
#
# WHY ITS OWN FILE
#   The route is a chain, not a stance. It needs a ledger of what MC took
#   over (the planner cards), a break that never undoes itself, and a manifest
#   that stops a partial chain from firing early -- more than s1_choices'
#   one-word stances hold.
#
# THE RULE FOR ADDING ONE
#   Both branches must read as sincere support. The distinction is never
#   kindness versus cruelty -- it is COLLABORATION versus SUBSTITUTION. And the
#   substitution branch must be the better-written scene: faster relief, warmer
#   payoff, visible gratitude. A blind player should finish it believing they
#   found the most attentive way to care for her. Nothing may be ominous.
#
#   Every new insertion MUST add its key to DEP_REQUIRED below, or the chain
#   will complete without it and the gate will fire early.
#
# THE CARD TEXT
#   Every dep_take() carries `card` -- one line in Tsubaki's own shorthand, as
#   it will appear on a note card clipped into her planner on Dec 24. Write it
#   the way she would write it to herself, not the way the scene described it.
#   "[player]" stays literal; Matsu'Py interpolates it when the card is displayed.
#
# LEDGER SO FAR (day -- key -- what MC took over)
#   0523  tsubaki_assignments   checking her work before it is due
# =============================================================================

# EVERY insertion key the route requires, in story order. INCOMPLETE -- the
# remaining insertions between June and the culture festival are not written
# yet. Until they are, dep_on_route() is gated behind DEP_MANIFEST_COMPLETE so
# a partial chain can never fire the Dec 24 skip by accident.
define DEP_REQUIRED = [
    "tsubaki_assignments",   # 0523, rooftop -- the extension form
]

# Flip to True only when DEP_REQUIRED lists every insertion in the finished
# main story. This is the safety catch on an unfinished route.
define DEP_MANIFEST_COMPLETE = False

# One dict per thing MC took over: {"key", "card", "day"}. Order is the order
# it happened, which is the order the planner shows them in.
default dep_ledger = []

# The chain is broken. Once True it never goes back to False for this
# playthrough -- that is the whole point of the gate.
default dep_broken = False

# Why it broke. Not shown to the player; it exists so a dev jumping into a late
# scene can tell "never on the route" from "was on it and stepped off."
default dep_break_reason = None


init python:

    def dep_take(key, card, day=None):
        """Record MC removing one decision from Tsubaki -- one box ticked.

        Idempotent per key, so a scene replayed after a rollback cannot
        double-count. Does NOT un-break a broken chain: once the player has
        taken a different option anywhere, taking this one is just a nice
        thing MC did, not a step back onto the route.
        """
        if any(entry["key"] == key for entry in dep_ledger):
            return
        dep_ledger.append({"key": key, "card": card, "day": day})

    def dep_break(reason=None):
        """End the route for this playthrough. Irreversible by design.

        Call this from the collaborative branch of any insertion, and from any
        other action the route watches -- the contract is that ANY deviation
        ends it, not just the paired menus.
        """
        global dep_broken
        global dep_break_reason
        if not dep_broken:
            dep_broken = True
            dep_break_reason = reason

    def dep_took(key):
        """True if MC took this particular thing over."""
        return any(entry["key"] == key for entry in dep_ledger)

    def dep_count():
        """How many boxes are ticked. Diagnostic only -- never a gate."""
        return len(dep_ledger)

    def dep_missing():
        """Required keys not yet taken. Diagnostic / dev-jump aid."""
        taken = set(entry["key"] for entry in dep_ledger)
        return [key for key in DEP_REQUIRED if key not in taken]

    def dep_intact():
        """True while the player is still a candidate for the route.

        Use this for anything that should only happen to a player who has not
        stepped off yet -- it is true early, before the chain is complete.
        """
        return not dep_broken

    def dep_cards():
        """The planner note cards, in the order she started needing them."""
        return [entry["card"] for entry in dep_ledger]

    def dep_on_route():
        """True only on a complete, unbroken chain. The culture festival gate.

        Every required key taken, nothing skipped, nothing deviated from. While
        DEP_MANIFEST_COMPLETE is False this always returns False, so the
        unfinished route cannot fire.
        """
        if not DEP_MANIFEST_COMPLETE:
            return False
        return dep_intact() and not dep_missing()
