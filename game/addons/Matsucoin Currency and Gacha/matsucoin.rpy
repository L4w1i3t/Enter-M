# Persistent Matsucoin wallet and earn receipts. mc_gacha spends coins;
# mc_cards owns collectibles and mc_collection displays them in the Archive.
# mc_sync() reconciles catalog-derived awards using persistent.mc_paid_keys.
# mc_award(amount, source, key=...) pays a one-time key; omit key for repeat awards.
# Permanent payout keys must not be renamed or recycled.
#
# Balance is spendable; lifetime and spent track totals. pending_notice_* persists
# a receipt for the next title-screen visit. Coins are credited immediately;
# only their notice is deferred. Balance-cap behavior must preserve unpaid keys.

default persistent.mc_balance = 0
default persistent.mc_lifetime = 0
default persistent.mc_spent = 0
default persistent.mc_paid_keys = set()
default persistent.mc_pending_notice_amount = 0
default persistent.mc_pending_notice_events = 0

init -5 python:

    # -------------------------------------------------------------------------
    # PAYOUT TABLE
    # One place for every number, because balancing a currency means moving
    # these against each other and that is impossible if they are scattered
    # across five files. A pull is 100 and a ten-pull 1000 (mc_gacha.rpy), so
    # read every value below as a fraction of one pull.
    # -------------------------------------------------------------------------

    # Hard ceiling on the wallet. Coins that do not fit are simply not credited
    # -- and a ONE-TIME payout that does not fit is not marked collected either,
    # so a full wallet DEFERS a reward instead of destroying it. Spend some and
    # the next sync pays it.
    MC_BALANCE_CAP = 99999

    # -- derived, one-time --
    MC_PAY_ACH = {                 # per achievement, by tier
        "bronze":   60,
        "silver":   120,
        "gold":     250,
    }
    MC_PAY_SIDE_UNLOCKED  = 40     # a side story becoming available
    MC_PAY_SIDE_COMPLETED = 120    # ...and actually being read to the end
    MC_PAY_CG             = 25     # per CG recovered
    MC_PAY_OUTFIT         = 20     # per wardrobe entry seen
    MC_PAY_ROSTER         = 15     # per roster slot identified
    MC_PAY_ARCHIVIST      = 200    # per Archivist fended off
    MC_PAY_CAMPAIGN       = 300    # clearing the campaign (Chapter 0.5 for now)

    # -- volatile, per arcade run --
    MC_PAY_RUN_BASE    = 15        # finishing any Arcade Original run
    MC_PAY_RUN_QUIT    = 5         # ...or bailing out of one
    MC_PAY_RUN_CAP     = 60        # most a single run's SCORE can be worth
    MC_PAY_RECORD      = 75        # beating your own best on a cabinet
    MC_PAY_FIRST_PLAY  = 100       # one-time, per cabinet
    MC_PAY_WIN         = 150       # clearing a story game mode from the Arcade
    MC_PAY_LOSS        = 30        # ...or losing one
    MC_PAY_FIRST_CLEAR = 250       # one-time, per game mode

    # Score -> coins. A run is worth score/divisor, capped at MC_PAY_RUN_CAP, so
    # every cabinet pays roughly the same for a roughly-as-good run despite
    # scores that differ by three orders of magnitude between them. The cap is
    # what stops one enormous snake run from buying the whole collection.
    # A cabinet missing from the table uses the default -- a new game pays
    # something sane on day one rather than paying nothing until somebody
    # remembers this table exists.
    MC_SCORE_DIVISOR = {
        "snake":  120,
        "brick":  200,
        "intake": 400,
        "sweep":  90,
        "chess":  40,
        "peg":    450,
    }
    MC_SCORE_DIVISOR_DEFAULT = 150

    # -------------------------------------------------------------------------
    # RUNTIME (never saved, never rolled back)
    # Only the receipt CURRENTLY BEING PRESENTED lives here. The actual pending
    # amount lives in persistent.mc_pending_notice_* above, and is acknowledged
    # only after its title-screen toast finishes. That means closing the game
    # during the toast simply presents the same receipt on the next launch.
    # -------------------------------------------------------------------------
    class _McRuntime(NoRollback):
        def __init__(self):
            # (amount, label, persisted_amount, persisted_event_count)
            self.queue = []
            self.started = None  # wall clock of the current toast; None = unrendered

    _mc_rt = _McRuntime()

    import time as _mc_time

    MC_TOAST_IN    = 0.30
    MC_TOAST_HOLD  = 2.2
    MC_TOAST_OUT   = 0.40
    MC_TOAST_TOTAL = MC_TOAST_IN + MC_TOAST_HOLD + MC_TOAST_OUT
    # -------------------------------------------------------------------------
    # WALLET
    # -------------------------------------------------------------------------
    def _mc_ensure_store():
        """Coerce the persistent state into the right types. Guards profiles
        written before this feature existed (every field reads None there) and
        profiles merged between two machines."""
        if not isinstance(getattr(persistent, "mc_paid_keys", None), set):
            persistent.mc_paid_keys = set(getattr(persistent, "mc_paid_keys", None) or [])
        for _field in (
                "mc_balance", "mc_lifetime", "mc_spent",
                "mc_pending_notice_amount", "mc_pending_notice_events"):
            if not isinstance(getattr(persistent, _field, None), int):
                try:
                    setattr(persistent, _field, int(getattr(persistent, _field, 0) or 0))
                except (TypeError, ValueError):
                    setattr(persistent, _field, 0)

        # Pending receipt fields are counters, never debts. Profiles created by
        # an interrupted dev edit or an older build should repair themselves.
        persistent.mc_pending_notice_amount = max(
            0, persistent.mc_pending_notice_amount)
        persistent.mc_pending_notice_events = max(
            0, persistent.mc_pending_notice_events)
        if persistent.mc_pending_notice_amount <= 0:
            persistent.mc_pending_notice_events = 0
        elif persistent.mc_pending_notice_events <= 0:
            persistent.mc_pending_notice_events = 1

    def mc_balance():
        _mc_ensure_store()
        return persistent.mc_balance

    def mc_can_afford(cost):
        return mc_balance() >= int(cost)

    def mc_award(amount, label=None, key=None, toast=True, save=True):
        """Credit coins. Returns what was actually credited (0 if nothing was).

        amount : coins. Non-positive amounts are a no-op, so a caller doing its
                own arithmetic can pass a computed 0 without a guard.
        label  : retained for source compatibility. Title receipts summarize
                all payout sources, so they do not display per-event labels.
        key    : ONE-TIME. With a key set, the payout happens at most once ever
                and the key is remembered in persistent.mc_paid_keys.
        """
        _mc_ensure_store()
        amount = int(amount or 0)
        if amount <= 0:
            return 0
        if key and key in persistent.mc_paid_keys:
            return 0

        # CAP. A one-time payout is all-or-nothing: half-crediting it and then
        # marking it collected would quietly destroy the rest, so if it does not
        # fit it is left unpaid AND unmarked, and comes back on the next sync
        # once there is room. A repeatable payout just tops the wallet up.
        room = MC_BALANCE_CAP - persistent.mc_balance
        if room <= 0:
            return 0
        if key:
            if amount > room:
                return 0
        else:
            amount = min(amount, room)

        if key:
            persistent.mc_paid_keys.add(key)

        persistent.mc_balance += amount
        persistent.mc_lifetime += amount

        if toast:
            mc_queue_payout_notice(amount)
        if save:
            _mc_save()
        return amount

    def mc_spend(amount):
        """Debit coins for a pull. Returns whether the balance covered it."""
        _mc_ensure_store()
        amount = int(amount or 0)
        if amount <= 0 or persistent.mc_balance < amount:
            return False
        persistent.mc_balance -= amount
        persistent.mc_spent += amount
        _mc_save()
        return True

    def _mc_save():
        try:
            renpy.save_persistent()
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # DERIVED PAYOUTS
    #
    # Each rule is (key_prefix, coins, reader, label_fn). `reader` returns the
    # list of THINGS CURRENTLY TRUE -- ids or persistent flag names -- and every
    # one of them not yet in the ledger is paid for. Readers are functions and
    # are resolved lazily for the same reason achievements.rpy's flag groups
    # are: this file may init before the catalogs it reads.
    #
    # Every reader is wrapped in a try/except by _mc_read: a catalog that has
    # not loaded (or a module that was cut) must cost the player nothing but
    # that rule's coins, not blow up the sync and silently stop every LATER
    # rule from paying out too.
    # -------------------------------------------------------------------------
    def _mc_read(fn):
        try:
            return tuple(fn() or ())
        except Exception:
            return ()

    def _mc_flags_true(flags):
        """Filter a list of persistent flag NAMES down to the set ones."""
        return tuple(f for f in flags if getattr(persistent, f, False))

    # -- readers, one per content type ---------------------------------------
    def _mc_earned_achievements():
        earned = getattr(persistent, "ach_earned", None) or ()
        catalog = globals().get("ACH_BY_ID") or {}
        return tuple(aid for aid in earned if aid in catalog)

    def _mc_side_unlocked():
        fn = globals().get("cs_all_unlock_keys", None)
        keys = _mc_read(fn) if fn else ()
        return _mc_flags_true(keys)

    def _mc_side_completed():
        fn = globals().get("cs_all_completed_keys", None)
        keys = _mc_read(fn) if fn else ()
        return _mc_flags_true(keys)

    def _mc_cgs():
        fn = globals().get("cg_all_keys", None)
        return _mc_flags_true(_mc_read(fn)) if fn else ()

    def _mc_outfits():
        fn = globals().get("roster_outfit_keys", None)
        return _mc_flags_true(_mc_read(fn)) if fn else ()

    def _mc_roster():
        fn = globals().get("roster_gated_ids", None)
        ids = _mc_read(fn) if fn else ()
        met = getattr(persistent, "roster_met_ids", None) or ()
        return tuple(i for i in ids if i in met)

    def _mc_archivists():
        # inv_fended() is the accessor that coerces the persistent value to a
        # real set (it guards profiles written before the invasions shipped);
        # fall back to the raw attribute if that file has not loaded.
        fn = globals().get("inv_fended", None)
        if fn:
            return _mc_read(fn)
        return tuple(getattr(persistent, "inv_fended", None) or ())

    def _mc_campaign():
        # Chapter 0.5 owns a permanent signal independent of where the Music
        # Room gate moves when the rest of Season 1 ships.
        return ("chapter05",) if getattr(persistent, "chapter05_completed", False) else ()

    def _mc_ach_coins(aid):
        """An achievement's payout is set by its TIER, so the rule needs a
        per-item amount rather than one flat number."""
        catalog = globals().get("ACH_BY_ID") or {}
        entry = catalog.get(aid)
        tier = getattr(entry, "tier", "bronze") if entry else "bronze"
        return MC_PAY_ACH.get(tier, MC_PAY_ACH["bronze"])

    # -- the rule table -------------------------------------------------------
    # (ledger prefix, coins-or-callable, reader)
    MC_DERIVED_RULES = (
        ("ach",      _mc_ach_coins,         _mc_earned_achievements),
        ("side_get", MC_PAY_SIDE_UNLOCKED,  _mc_side_unlocked),
        ("side_end", MC_PAY_SIDE_COMPLETED, _mc_side_completed),
        ("cg",       MC_PAY_CG,             _mc_cgs),
        ("fit",      MC_PAY_OUTFIT,         _mc_outfits),
        ("who",      MC_PAY_ROSTER,         _mc_roster),
        ("inv",      MC_PAY_ARCHIVIST,      _mc_archivists),
        ("camp",     MC_PAY_CAMPAIGN,       _mc_campaign),
    )

    def mc_sync(notify=True):
        """Pay out for every qualifying thing not yet in the ledger.

        Safe and cheap to call as often as you like -- it is a set-difference
        against persistent.mc_paid_keys, and once a profile is settled it credits
        nothing. Hooked to the same places ach_sync is (see the bottom of this
        file), so returning to a hub after a fight or a side story pays for it.
        Returns total coins credited."""
        _mc_ensure_store()
        total = 0
        events = 0

        for prefix, coins, reader in MC_DERIVED_RULES:
            for item in _mc_read(reader):
                key = "%s:%s" % (prefix, item)
                if key in persistent.mc_paid_keys:
                    continue
                amount = coins(item) if callable(coins) else coins
                # toast=False: the batch is judged as a whole below, because a
                # first sync on an established profile can settle dozens of
                # these at once.
                got = mc_award(amount, key=key, toast=False, save=False)
                if got:
                    total += got
                    events += 1

        if total:
            if notify:
                # A derived sweep can settle dozens of catalog entries. Keep
                # one persisted total instead of recreating the old toast parade.
                mc_queue_payout_notice(total, events)
            _mc_save()
        return total

    def mc_refresh():
        """VOID wrapper for screen `on "show"` handlers. A screen EVENT action
        that returns non-None ends the interaction and bubbles the value up like
        Return() -- which is what closed the Archive the instant it opened when
        ach_refresh was first written. Never return a value from here."""
        mc_sync()
        return None

    # -------------------------------------------------------------------------
    # ARCADE PAYOUTS (the volatile faucet)
    # -------------------------------------------------------------------------
    def mc_award_run(kind, title, score, outcome, new_record=False):
        """One finished Arcade Original run. Called from AGGame.finish().

        kind    : cabinet key ("snake"), used for the divisor and the ledger.
        outcome : the AGGame finish kind -- "quit" means bailed out.
        Returns the total credited, which the results card then reports."""
        total = 0
        quit_out = (outcome == "quit")

        total += mc_award(MC_PAY_RUN_QUIT if quit_out else MC_PAY_RUN_BASE,
                        title, toast=False, save=False)

        if not quit_out and score:
            div = MC_SCORE_DIVISOR.get(kind, MC_SCORE_DIVISOR_DEFAULT)
            total += mc_award(min(int(int(score) / max(div, 1)), MC_PAY_RUN_CAP),
                            title, toast=False, save=False)

        if new_record:
            total += mc_award(MC_PAY_RECORD, title, toast=False, save=False)

        if not quit_out:
            total += mc_award(MC_PAY_FIRST_PLAY, title,
                            key="first_play:%s" % kind, toast=False, save=False)

        if total:
            _mc_save()
        return total

    def mc_award_mode(slug, title, won, first_clear_key=None):
        """One finished story game mode launched from the Arcade (the boss
        fights). Flat outcome money plus a one-time first-clear bonus, because
        those modes have no comparable score to scale against each other."""
        total = mc_award(MC_PAY_WIN if won else MC_PAY_LOSS, title,
                        toast=False, save=False)
        if won:
            total += mc_award(MC_PAY_FIRST_CLEAR, title,
                            key=(first_clear_key or ("first_clear:%s" % slug)),
                            toast=False, save=False)
        if total:
            _mc_save()
        return total

    # -------------------------------------------------------------------------
    # STORY BEATS
    # The hand-placed API, for a moment in the script worth paying for that no
    # flag already records. Drop `$ mc_story_award("0523_notebook", 120)` at the
    # beat. The key is what makes it first-time-only, so it must be unique and
    # must never be recycled for a different beat.
    # -------------------------------------------------------------------------
    def mc_story_award(key, amount, label="STORY"):
        return mc_award(amount, label, key="story:%s" % key)

    # -------------------------------------------------------------------------
    # THE COIN GLYPH
    # matsucoin.png is a 15x16 pixel-art coin, so it is scaled with nearest
    # sampling -- a smoothed 15px sprite blown up to 32px is mush. Cached per
    # size because these are built inside screens, which rebuild constantly.
    # -------------------------------------------------------------------------
    MC_COIN_PATH = "addons/Matsucoin Currency and Gacha/matsucoin.png"
    MC_COIN_W, MC_COIN_H = 15, 16
    _MC_COIN_CACHE = {}

    def MatsucoinIcon(height=16):
        """The coin at a given pixel HEIGHT, aspect preserved, nearest-scaled."""
        h = max(4, int(height))
        hit = _MC_COIN_CACHE.get(h)
        if hit is None:
            zoom = float(h) / MC_COIN_H
            hit = Transform(MC_COIN_PATH, zoom=zoom, nearest=True)
            _MC_COIN_CACHE[h] = hit
        return hit

    def mc_num(n):
        """Thousands-separated balance string (matches the arcade's ag_num)."""
        try:
            return format(int(n), ",")
        except (TypeError, ValueError):
            return str(n)

    # -------------------------------------------------------------------------
    # SFX
    # Cue-with-volume entries, NOT `audio.` aliases -- the same shape the game
    # modes use (AG_SFX in ag_core.rpy, KT_SFX in kototouhou.rpy), because these
    # are played through renpy.sound.play with a per-cue level rather than by a
    # `play` statement, which is what the alias rule governs.
    #
    # "coin" is se_item00, the ZUN point-item collect -- the sound of picking
    # money up, and already this project's "pickup" cue in the Arcade Originals.
    # It replaces audio.beep, which is the CENSOR BLEEP and reads as one.
    # -------------------------------------------------------------------------
    MC_SE_DIR = "assets/audio/sfx/touhou/"
    MC_SFX = {
        "coin": (MC_SE_DIR + "se_item00.wav", 0.75),   # coins credited
        "r":    (MC_SE_DIR + "se_kira00.wav", 0.50),   # common card lands
        "sr":   (MC_SE_DIR + "se_nice.wav",   0.75),   # SR lands
        "ssr":  (MC_SE_DIR + "se_cardget.wav", 0.90),  # SSR -- the card-capture cue

        # -- the pull cinematic (mc_reveal_fx.rpy) ----------------------------
        # The four beats of a wind-up, in one rising family: the capsule
        # arriving, a rung of the tier ladder, the rung that UPGRADES, and the
        # impact under every burst. The tier stings above are what plays on top
        # of that impact, so the burst is always two layers.
        "fx_drop":    (MC_SE_DIR + "se_tan00.wav",   0.70),
        "fx_charge":  (MC_SE_DIR + "se_ch00.wav",    0.65),
        "fx_upgrade": (MC_SE_DIR + "se_powerup.wav", 0.85),
        "fx_impact":  ("assets/audio/sfx/sfx-shing.wav", 0.55),
        "fx_flip":    (MC_SE_DIR + "se_kira02.wav",  0.40),
    }

    # A POOL, not the shared "sound" channel. A ten-pull lands a card every
    # 0.16s and each one rings its rarity sting; on one channel every sting cut
    # the one before it, so nine of the ten were inaudible and the tier cues
    # sounded like they were not per-card at all. Six channels is more than the
    # reveal can ever have in flight at once.
    #
    # Allocation goes through msbf_pick_pool_channel (battle_logic.rpy), which
    # takes an IDLE channel rather than blindly rotating onto a live cue -- the
    # same helper the boss fight and the Arcade Originals use.
    MC_SFX_POOL = ["mc_sfx_%d" % i for i in range(6)]
    for _mc_ch in MC_SFX_POOL:
        if not renpy.music.channel_defined(_mc_ch):
            renpy.music.register_channel(_mc_ch, mixer="sfx", loop=False)

    def mc_se(name, volume_scale=1.0):
        """Play one Matsucoin cue. Unknown names are silently ignored, so a cue
        can be named before it has been given a file without crashing a pull."""
        entry = MC_SFX.get(name)
        if not entry:
            return
        try:
            # Resolved lazily and by name: this file inits before
            # battle_logic.rpy. Degrading to the shared "sound" channel is
            # deliberately NOT silence -- a missing helper should cost cue
            # separation, not the cue.
            picker = globals().get("msbf_pick_pool_channel", None)
            channel = picker(MC_SFX_POOL, "cursor", mc_se) if picker else "sound"
            if channel is None:
                return
            renpy.sound.play(entry[0], channel=channel,
                            relative_volume=entry[1] * volume_scale)
        except Exception:
            pass
    mc_se.cursor = 0

    # -------------------------------------------------------------------------
    # DEFERRED PAYOUT RECEIPT
    # -------------------------------------------------------------------------
    def mc_queue_payout_notice(amount, events=1):
        """Persist a receipt without presenting it during gameplay.

        This deliberately does not save on its own: mc_award and mc_sync already
        own the transaction boundary and save the wallet, ledger and receipt in
        one write. Returns the amount added for small test harnesses and console
        diagnostics.
        """
        _mc_ensure_store()
        amount = max(0, int(amount or 0))
        events = max(0, int(events or 0))
        if amount <= 0:
            return 0
        persistent.mc_pending_notice_amount += amount
        persistent.mc_pending_notice_events += max(1, events)
        return amount

    def _mc_notice_label(events):
        events = max(1, int(events or 0))
        if events == 1:
            return "PAYOUT COLLECTED"
        return "%s PAYOUTS COLLECTED" % mc_num(events)

    def mc_main_menu_enter():
        """Settle the wallet, then stage exactly one persisted title receipt.

        The pending counters are NOT cleared here. They are acknowledged only
        after the toast completes, so quitting during the title transition or
        leaving the menu quickly cannot make the notification disappear forever.
        """
        _mc_ensure_store()

        # Achievement conditions own some of this currency's derived inputs.
        # Reconcile them first so a cold relaunch after an objective (including
        # quitting during a card reveal) can pay and present the receipt on THIS
        # title visit instead of waiting for another round trip. The addon is
        # optional, and one broken condition must not block all other payouts.
        ach_sync_fn = globals().get("ach_sync", None)
        if ach_sync_fn:
            try:
                ach_sync_fn()
            except Exception:
                pass

        mc_sync()

        # A return to the title is a fresh delivery attempt. Replacing the
        # session queue also folds any interrupted receipt and any newer awards
        # into one current total without ever double-crediting the wallet.
        del _mc_rt.queue[:]
        _mc_rt.started = None

        amount = persistent.mc_pending_notice_amount
        events = persistent.mc_pending_notice_events
        if amount > 0:
            _mc_rt.queue.append(
                (amount, _mc_notice_label(events), amount, events))
        return None

    def _mc_acknowledge_notice(amount, events):
        """Remove only the portion represented by one completed receipt.

        Subtraction rather than clearing is important: a dev action can earn a
        new payout while the current title receipt is still animating.
        """
        _mc_ensure_store()
        persistent.mc_pending_notice_amount = max(
            0, persistent.mc_pending_notice_amount - max(0, int(amount or 0)))
        persistent.mc_pending_notice_events = max(
            0, persistent.mc_pending_notice_events - max(0, int(events or 0)))
        if persistent.mc_pending_notice_amount <= 0:
            persistent.mc_pending_notice_events = 0
        _mc_save()

    def _mc_toast_anim(trans, st, at):
        """ATL driver on the toast card, one call per frame while it is up.
        Wall-clock, so skip mode cannot compress it and an interaction restart
        cannot re-zero it -- and the clock only starts once the card actually
        RENDERS, so a coin awarded mid-transition still gets its full dwell."""
        if renpy.predicting():
            return 0
        if not getattr(renpy.store, "main_menu", False) or not _mc_rt.queue:
            trans.alpha = 0.0
            return 0
        now = _mc_time.time()
        if _mc_rt.started is None:
            _mc_rt.started = now
            mc_se("coin")
        el = now - _mc_rt.started

        if el < MC_TOAST_IN:
            p = el / MC_TOAST_IN
            q = p - 1.0
            ease = 1.0 + 2.70158 * q * q * q + 1.70158 * q * q   # easeOutBack
            trans.alpha = min(1.0, p * 2.0)
            trans.xoffset = 60.0 * (1.0 - ease)
        elif el < MC_TOAST_IN + MC_TOAST_HOLD:
            trans.alpha = 1.0
            trans.xoffset = 0.0
        elif el < MC_TOAST_TOTAL:
            p = (el - MC_TOAST_IN - MC_TOAST_HOLD) / MC_TOAST_OUT
            trans.alpha = 1.0 - p * p
            trans.xoffset = 40.0 * p * p
        else:
            finished = _mc_rt.queue.pop(0)
            _mc_rt.started = None
            trans.alpha = 0.0
            if len(finished) >= 4:
                _mc_acknowledge_notice(finished[2], finished[3])
            renpy.restart_interaction()
        return 0

    # -------------------------------------------------------------------------
    # DEV
    # The ECONOMY page of the Developer Hub (main menu, top-right, or F9) drives
    # all of this, and opens screen mc_dev_shop for the rest; everything below
    # is also callable straight from the Matsu'Py console with Shift+O:
    #     mc_dev_give(5000)     mc_dev_fill()     mc_dev_reset()
    # -------------------------------------------------------------------------
    def mc_dev_set(amount):
        """Set the wallet to an exact figure, clamped to [0, MC_BALANCE_CAP].
        Goes straight to the balance rather than through mc_award, because a
        dev grant is not earnings -- routing it through the wallet's income
        would inflate TOTAL EARNED and break the lifetime == balance + spent
        invariant the payout tests check."""
        _mc_ensure_store()
        persistent.mc_balance = max(0, min(int(amount), MC_BALANCE_CAP))
        _mc_save()
        renpy.restart_interaction()
        return None

    def mc_dev_give(amount=1000):
        """Add coins on top of what is there, capped."""
        _mc_ensure_store()
        return mc_dev_set(persistent.mc_balance + int(amount))

    def mc_dev_fill():
        """Straight to the cap."""
        return mc_dev_set(MC_BALANCE_CAP)

    def mc_dev_reset(keep_ledger=True):
        """Zero the wallet. keep_ledger=True (the default) leaves the one-time
        payouts marked collected, so a reset does not hand the whole derived
        pool straight back on the next sync -- which is what you want when
        testing the MACHINE, and not what you want when testing the PAYOUTS."""
        _mc_ensure_store()
        persistent.mc_balance = 0
        persistent.mc_lifetime = 0
        persistent.mc_spent = 0
        persistent.mc_pending_notice_amount = 0
        persistent.mc_pending_notice_events = 0
        del _mc_rt.queue[:]
        _mc_rt.started = None
        if not keep_ledger:
            persistent.mc_paid_keys = set()
        _mc_save()
        renpy.restart_interaction()
        return None


# -----------------------------------------------------------------------------
# TOAST SCREEN
# Hosted by config.always_shown_screens (registered at the bottom of this file)
# so it survives menu-context changes, but it renders ONLY while ``main_menu``
# is true. Gameplay can keep settling the wallet without ever drawing a receipt.
# Never show or hide it by hand.
# -----------------------------------------------------------------------------
transform mc_toast_drive:
    subpixel True
    alpha 0.0
    function _mc_toast_anim

screen matsucoin_toaster():
    # Just under the achievement toaster (400) so that if both fire for the same
    # act -- and they routinely do, since achievements PAY -- the achievement
    # reads as the headline and the coins as its receipt.
    zorder 399

    if main_menu and _mc_rt.queue:
        $ _mc_amount, _mc_label = _mc_rt.queue[0][:2]
        $ _mc_ach_queue = getattr(getattr(renpy.store, "_ach_rt", None), "queue", ())

        frame:
            style "mc_toast_frame"
            anchor (1.0, 1.0)
            # The achievement toast owns the bottom-right corner and is 62px
            # tall. When one is up, this sits on top of it instead of under it.
            pos (0.988, 0.965)
            yoffset (-70 if _mc_ach_queue else 0)
            ysize 54
            at mc_toast_drive

            hbox:
                spacing 0

                add Solid("#ffb454") xysize (5, 54)
                null width 13

                hbox:
                    yalign 0.5
                    spacing 9

                    add MatsucoinIcon(22) yalign 0.5

                    vbox:
                        spacing 1
                        yalign 0.5
                        text ("+%s" % mc_num(_mc_amount)) style "mc_toast_amount"
                        text _mc_label style "mc_toast_label" layout "nobreak"

                null width 16


# -----------------------------------------------------------------------------
# SHARED BALANCE CHIP
# The wallet readout, reused by the Arcade hub, the machine and the binder so
# the number looks the same everywhere it appears.
#   size  : text size; the coin scales with it.
#   light : True on the Archive's cyan panels, False on the Arcade's indigo.
# -----------------------------------------------------------------------------
screen mc_balance_chip(size=20, light=False):
    hbox:
        spacing 8
        add MatsucoinIcon(int(size * 1.05)) yalign 0.5
        text mc_num(mc_balance()):
            style "mc_chip_amount"
            size size
            color ("#dff8ff" if light else "#ffd98a")
            yalign 0.5


# =============================================================================
# STYLES
# The coin is the Arcade's amber (#ffb454) wherever it appears, INCLUDING on the
# Archive's cyan panels. That is deliberate: Matsucoins are an arcade object, and
# a currency that recolors itself per room stops reading as one thing.
# =============================================================================
style mc_toast_frame:
    background Solid("#181030f2")
    padding (0, 0)

style mc_toast_amount:
    font gui.interface_font
    color "#ffd98a"
    size 21
    bold True
    outlines [(2, "#02040b", 0, 0)]

style mc_toast_label is gui_text:
    font gui.interface_font
    color "#c9c0dc"
    size 11
    kerning 1.0
    outlines [(1, "#02040b", 0, 0)]

style mc_chip_amount:
    font gui.interface_font
    bold True
    outlines [(2, "#02040b", 0, 0)]


# -----------------------------------------------------------------------------
# HOOKS
# Sync on load and before every interaction so the WALLET never lags behind the
# deed. Presentation is separate: the ``before_main_menu`` label callback stages
# the persisted total exactly when the player next reaches the title screen.
# -----------------------------------------------------------------------------
init 60 python:
    if "matsucoin_toaster" not in config.always_shown_screens:
        config.always_shown_screens.append("matsucoin_toaster")

    def _mc_after_load():
        mc_sync()

    if _mc_after_load not in config.after_load_callbacks:
        config.after_load_callbacks.append(_mc_after_load)

# SETTLE EVERY INTERACTION, PRESENT ONLY AT THE TITLE.
#
# Crediting immediately keeps every wallet read correct and makes the one-time
# ledger idempotent even if the player quits mid-chapter. The receipt is a
# different concern: mc_sync adds its amount to persistent pending counters,
# and mc_main_menu_enter stages one summary later, away from story scenes.
    #
    # Running the whole sweep per interaction is affordable: it is ~130 getattr
    # lookups and a few list comprehensions against catalogs that are already in
    # memory, and it short-circuits to nothing once a profile is settled, which
    # is the state it is in for all but a handful of interactions in a session.
    # Nothing here touches disk unless a payout actually happens.
    #
    # It must stay exception-safe: this runs before EVERY interaction in the
    # game, so an exception escaping it would take the whole game down rather
    # than merely cost the player some coins. mc_sync guards each catalog reader
    # individually (_mc_read); this is the outer belt.
    def _mc_interact_sync():
        try:
            mc_sync()
        except Exception:
            pass

    if _mc_interact_sync not in config.interact_callbacks:
        config.interact_callbacks.append(_mc_interact_sync)

    def _mc_label_callback(name, abnormal):
        # Official Ren'Py lifecycle calls before_main_menu on first launch and
        # every return from gameplay. A label callback keeps this addon
        # self-contained instead of adding a hard reference to splash.rpy.
        if name != "before_main_menu":
            return
        try:
            mc_main_menu_enter()
        except Exception:
            # The callback must never make the title screen unreachable. Any
            # unpresented amount remains persistent and can be retried later.
            pass

    if _mc_label_callback not in config.label_callbacks:
        config.label_callbacks.append(_mc_label_callback)
