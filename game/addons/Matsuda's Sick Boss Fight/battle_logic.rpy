# =============================================================================
# battle_logic.rpy  --  MATSUDA'S SICK BOSS FIGHT :: RULES + STATE ENGINE
# =============================================================================
#
# WHAT THIS FILE IS
#   The complete, UI-free combat engine for the boss fight: an SMT/Persona-style
#   "press-turn" battle with three phases, plus a Touhou-style bullet-hell
#   ("shmup") segment in phase three. All combat math, AI, audio, and the battle
#   state machine live here. The SCREENS that draw/drive it (party select +
#   battle screen) are in ui.rpy; the shader/particle polish is in fx.rpy.
#
# WHO DRIVES IT (the public surface used by the story front-end)
#   game/addons/Character Stories/cs_matsuda_02.rpy calls:
#     msbf_clear_battle_watch()                 -> reset global battle vars
#     call screen msbf_party_select             -> (ui.rpy) returns party id list
#     msbf_new_battle(party_ids, id_mode=)      -> build an MSBFBattleState
#     call screen msbf_battle_screen(state)     -> (ui.rpy) run the fight; returns
#                                                   "victory" / other
#     msbf_stop_battle_music(fade)              -> stop all battle channels
#   The battle SCREEN (ui.rpy) calls MSBFBattleState methods every interaction:
#   player_use_skill / player_pass / start_enemy_phase / update_shmup_segment, etc.
#
# GLOBALS (module-level `default`s)
#   msbf_battle_state       : the live MSBFBattleState (or None between fights).
#   msbf_battle_menu_locked  : when True + a battle is live, saving/loading is
#                              blocked (see msbf_save_load_locked()).
#
# THE STATE MACHINE (MSBFBattleState.turn_phase)
#   "setup" -> "player" -> "enemy" -> back to "player", with detours to
#   "phase_transition" (between phases), "shmup_segment" (the bullet-hell cast),
#   and "victory_sequence". Press-turn economy: a full icon = 2 actions, a half =
#   1; hitting weaknesses/crits converts/grants turns, resists/misses cost them.
#
# PHASES (see _configure_phase_two / _configure_phase_three)
#   1: fixed weak/resist set, drawn from MSBF_PHASE1_AFFINITY_SETS.
#   2: shuffling affinities that ADAPT after repeated weakness hits.
#   3: "Id Mode" superboss layer -- adds the shmup, layered vocal music, more.
#   DEBUG NOTE: msbf_make_boss() sets max_hp = 40 on purpose. Phases 1 & 2 are
#   one-shot test bars; only phase 3's real HP (set in _configure_phase_three)
#   matters. This is intentional per the project owner -- do not "fix" it.
#
# CROSS-FILE FEEDS (consumed by ui.rpy / fx.rpy)
#   set_fx()/fx_event + fx_serial : one-shot screen FX cue (hit/weak/crit/phase).
#   emit_float()/float_events     : the floating damage/heal number feed.
#   press_turn_*_fx               : per-icon press-turn animations.
#   These are plain data the screens poll by serial number each redraw.
# =============================================================================

# Live battle state object + the save/load lock flag (see header).
default msbf_battle_state = None
default msbf_battle_menu_locked = False

# Achievements feed ("Genre Savvy"): which phase-3 genre shifts ("shmup" /
# "typing" / "quiz") have EVER been won, across all runs. Plain string list.
default persistent.msbf_micro_wins = []

# --- MSBF SFX CHANNEL POOL ---------------------------------------------------
# Matsu'Py audio channels are MONOPHONIC: playing a new sound on a channel stops
# whatever was on it. Routing every cue through one channel therefore chops the tail
# off the previous cue -- jarring during fast keyboard nav, or when an action's
# resolve cue is immediately followed by the turn-change cue. (These channels also
# aren't Matsu'Py defaults -- only sound/music/voice/numbered exist -- and config
# version 0.1.0 forces play_channel="sound", so the mouse's button SFX use "sound".)
# So MSBF round-robins ALL its one-shots -- combat hits + their layers, danmaku
# fire/hit, keyboard UI blips -- across a small POOL of channels: consecutive cues
# land on different channels and overlap naturally instead of cutting each other off.
# All on the sfx mixer so the SFX slider governs them; channel_defined guards a
# hot-reload from re-registering.
init python:
    import time

    # FIXED pool, registered ONCE (channel_defined guard) and reused forever -- the
    # channels are NOT created per-play, so nothing leaks or accumulates across casts,
    # battles, or hot-reloads; re-running this init just re-confirms the same names.
    # Twelve rather than eight: Tsubaki mode routes its whole 60Hz cue stream
    # through here (volley + glint + throw + release can all land on one tick), and
    # the extra headroom means the allocator below almost never has to evict.
    MSBF_SFX_POOL = ["msbf_sfx_%d" % i for i in range(12)]
    for _msbf_pool_ch in MSBF_SFX_POOL:
        if not renpy.music.channel_defined(_msbf_pool_ch):
            renpy.music.register_channel(_msbf_pool_ch, mixer="sfx", loop=False)

    # --- POOL ALLOCATION: pick an IDLE channel, not merely the next one --------
    # A blind cursor rotation guarantees only that consecutive cues differ; it says
    # nothing about whether the channel it lands on is FREE. Once the cue rate is
    # high enough for the cursor to lap the pool -- trivially reached in Kotonoha
    # and Tsubaki mode, where a single tick can fire volley + hit + graze -- the
    # rotation starts landing on channels that are still mid-cue, and Matsu'Py
    # channels being monophonic, the new sound stops the old one dead. That is the
    # "sounds get cut off early even though it's round-robin" symptom: the pool was
    # rotating, it just wasn't LOOKING before it wrote.
    #
    # So ask first. Scan forward from the cursor for a channel that is playing
    # nothing and take it -- normally a hit on the first probe, so this costs one
    # cheap query per cue. Only when the pool is genuinely saturated do we fall
    # back to evicting, and then we evict the LEAST RECENTLY STARTED channel (the
    # one furthest into its cue and so with the least tail left to lose) rather
    # than whatever the cursor happened to be pointing at.
    _msbf_pool_started = {}     # channel name -> time.time() of its last cue

    def _msbf_channel_idle(channel):
        try:
            return renpy.music.get_playing(channel=channel) is None
        except Exception:
            return True

    def msbf_pick_pool_channel(pool, cursor_key="cursor", owner=None):
        # The cursor lives on a FUNCTION OBJECT (not a store var), so it is immune
        # to rollback/save churn and always advances monotonically -- a store cursor
        # could be snapped back by a rollback and pile every cue onto one channel
        # again (the exact monophonic cut-off we're avoiding).
        owner = owner or msbf_pick_pool_channel
        size = len(pool)

        if not size:
            return None

        cursor = getattr(owner, cursor_key, 0) % size
        chosen = None

        for offset in range(size):
            candidate = pool[(cursor + offset) % size]

            if _msbf_channel_idle(candidate):
                chosen = candidate
                setattr(owner, cursor_key, (cursor + offset + 1) % size)
                break

        if chosen is None:
            # Everything is busy: sacrifice the oldest cue, which has had the most
            # time to be heard. Channels never started this session sort first
            # (0.0), so a cold pool still fills before anything is interrupted.
            chosen = min(pool, key=lambda ch: _msbf_pool_started.get(ch, 0.0))
            setattr(owner, cursor_key, (pool.index(chosen) + 1) % size)

        _msbf_pool_started[chosen] = time.time()
        return chosen

    def msbf_play_pooled_sfx(path, volume=None):
        # Play a one-shot on a FREE pool channel so it never cuts off a live cue.
        if not path:
            return
        channel = msbf_pick_pool_channel(MSBF_SFX_POOL, "cursor", msbf_play_pooled_sfx)
        if channel is None:
            return
        try:
            # Use the relative_volume PARAM, not a "<volume ..>path" string tag. The
            # tag branch was the only path every volume-scaled cue took (i.e. the whole
            # shmup), and it was the suspect for the shmup going silent; the param is the
            # documented, path-agnostic way to scale a one-shot and removes all doubt.
            renpy.sound.play(path, channel=channel, relative_volume=(1.0 if volume is None else volume))
        except Exception:
            pass
    msbf_play_pooled_sfx.cursor = 0

    def msbf_stop_pooled_sfx(fadeout=0.0):
        # Graceful teardown: silence every pool channel (called on battle end) so no
        # cue is left ringing after the fight. Never unregisters -- the channels are
        # reused next battle -- so there is nothing to leak.
        for channel in MSBF_SFX_POOL:
            try:
                renpy.music.stop(channel=channel, fadeout=fadeout)
            except Exception:
                pass


# =============================================================================
# SHARED KEY LATCH  --  the "stuck direction" guard for the 60Hz game modes
# =============================================================================
# Kotonoha, Tsubaki mode, and the phase-three Id shmup all read the keyboard by
# POLLING SDL state (pygame.key.get_pressed()) once per simulation tick/frame,
# rather than by handling Matsu'Py key events. That is the right call for a realtime
# action game -- "which way is held THIS tick" is a state question, and an event
# callback answers a different one -- but it inherits SDL's one failure mode: the
# state array only changes when a key event actually reaches the process. If a
# release never arrives (the window losing focus mid-press, the OS eating the
# key-up during an alt-tab or a long hitch), that key reads as held forever and
# the player keeps sliding in one direction with nothing pressed. Rare, and
# exactly the reported bug.
#
# The fix does not replace polling -- it supervises it. Matsu'Py still delivers the
# real KEYUP to the stage displayable's event() method, so feeding those events
# in here latches the offending key OFF. The latch is released the moment polling
# agrees the key is up (we are back in sync), or instantly on a fresh KEYDOWN.
# That asymmetry is the safety property: this can only ever END a stuck key, and
# can never invent one, because any genuine press clears the latch before it is
# read. A lost window focus also blanks the whole keyboard, so a mode can never
# keep moving while the player is in another window.
# =============================================================================
init python:
    try:
        import pygame_sdl2 as _msbf_pg
    except Exception:
        _msbf_pg = None

    class MSBFKeyLatch(object):
        def __init__(self):
            # Keycodes Matsu'Py reported as released whose polled state has not yet
            # caught up. Plain ints, so this pickles with the game state fine.
            self.stuck = set()

        def handle_event(self, ev):
            # Called from the stage displayable's event(). Cheap and total: every
            # event type that is not a key event falls straight through.
            if _msbf_pg is None:
                return

            try:
                etype = ev.type
            except Exception:
                return

            if etype == _msbf_pg.KEYUP:
                try:
                    self.stuck.add(ev.key)
                except Exception:
                    pass
            elif etype == _msbf_pg.KEYDOWN:
                try:
                    self.stuck.discard(ev.key)
                except Exception:
                    pass

        def focused(self):
            # False while another window owns the keyboard. Callers zero their
            # input for the frame rather than coasting on a stale state array.
            if _msbf_pg is None:
                return True

            try:
                return bool(_msbf_pg.key.get_focused())
            except Exception:
                return True

        def pressed(self, keys, *keycodes):
            # True if ANY of `keycodes` is genuinely held right now. A latched key
            # reads as up until polling confirms the release, at which point the
            # latch drops and SDL is trusted again.
            held = False

            for code in keycodes:
                try:
                    down = bool(keys[code])
                except Exception:
                    continue

                if code in self.stuck:
                    if not down:
                        self.stuck.discard(code)
                    continue

                if down:
                    held = True

            return held

        def clear(self):
            self.stuck.clear()

# init -1 so all the data tables/classes exist before any screen references them.
init -1 python:
    import random
    import math

    # --- AFFINITY / PHASE TUNING ---------------------------------------------
    # Element ids -> display names. The PHASE1_AFFINITY_SETS are (weaknesses,
    # resists) pairs the boss randomly draws from in phase 1; the PHASE2/3_*
    # counts/ADAPT constants control how phase 2-3 reshuffle and adapt affinities.
    MSBF_AFFINITY_NAMES = {
        "slash": "Slash",
        "pierce": "Pierce",
        "fire": "Fire",
        "ice": "Ice",
        "lightning": "Lightning",
        "wind": "Wind",
        "psychic": "Psychic",
        "almighty": "Almighty",
    }

    MSBF_PHASE1_AFFINITY_SETS = [
        (["fire"], ["ice", "pierce"]),
        (["ice"], ["fire", "slash"]),
        (["lightning"], ["wind", "pierce"]),
        (["wind"], ["lightning", "slash"]),
        (["fire", "slash"], ["lightning"]),
        (["ice", "pierce"], ["fire"]),
        (["slash"], ["pierce", "psychic"]),
        (["pierce"], ["fire", "psychic"]),
        (["psychic"], ["ice", "wind"]),
        (["lightning", "psychic"], ["pierce"]),
    ]

    MSBF_PHASE2_AFFINITY_ELEMENTS = ["slash", "pierce", "fire", "ice", "lightning", "wind", "psychic"]
    MSBF_PHASE2_WEAKNESS_COUNT = 3
    MSBF_PHASE2_RESIST_COUNT = 3
    MSBF_PHASE2_ADAPT_WEAK_HITS = 3
    MSBF_PHASE3_WEAKNESS_COUNT = 2
    # Rebalanced: 3 resists (was 4) leaves weak 2 / resist 3 / neutral 2 so the
    # party's offence can actually land against 7600 HP, and the boss adapts a
    # beat slower (3 weakness hits, was 2) before nulling an exploited element.
    MSBF_PHASE3_RESIST_COUNT = 3
    MSBF_PHASE3_ADAPT_WEAK_HITS = 3
    MSBF_IDMODE_PHASE3_MUSIC_INST = audio.embracedflame_inst
    MSBF_IDMODE_PHASE3_MUSIC_VOCAL = audio.embracedflame_vocal
    MSBF_IDMODE_PHASE3_HEARTBEAT = audio.heartbeat_ominous
    MSBF_IDMODE_PHASE3_INST_CHANNEL = "track1"
    MSBF_IDMODE_PHASE3_VOCAL_CHANNEL = "track2"
    MSBF_IDMODE_PHASE3_HEARTBEAT_CHANNEL = "track3"
    MSBF_IDMODE_PHASE3_CROSSFADE = 1.45
    MSBF_IDMODE_PHASE3_VOCAL_FADEIN = 0.55
    MSBF_IDMODE_PHASE3_INST_BED = 0.18
    # --- PHASE-1 ENTRANCE CINEMATIC ------------------------------------------
    # Audio for the pre-battle dramatic entrance (screen msbf_battle_intro). The
    # heartbeat + wind loop on their own channels while the boss looms in (started
    # and stopped by cs_matsuda_02_battle so the phase-1 music only kicks in AFTER
    # the intro); the boom + thunder are one-shots fired at the name-slam climax.
    MSBF_INTRO_HEARTBEAT = audio.heartbeat_ominous
    MSBF_INTRO_WIND = audio.wind
    MSBF_INTRO_BOOM = audio.hollowboom
    MSBF_INTRO_THUNDER = audio.sfx_thunder
    MSBF_INTRO_HEARTBEAT_CHANNEL = "track3"
    MSBF_INTRO_WIND_CHANNEL = "track4"
    # --- PHASE-3 MICROGAME ("genre shift") WIN/LOSS --------------------------
    # Shared across all three genre-shift minigames (bullet-hell, typing, quiz).
    # Win: chip 3-5% of the boss's CURRENT HP (so a microgame can never kill it).
    # Loss: single-target games take 30% of ONE member's max HP; party-wide games
    # take 7% off every member. Microgame losses are non-lethal (floored at 1 HP)
    # so a genre shift can't directly wipe the party -- but they hit hard enough
    # that a microgame is a real threat, not a safe break from the superboss.
    MSBF_MICROGAME_WIN_CHIP_MIN = 0.03
    MSBF_MICROGAME_WIN_CHIP_MAX = 0.05
    MSBF_MICROGAME_LOSS_SINGLE = 0.30
    MSBF_MICROGAME_LOSS_PARTY = 0.07

    # --- PHASE-3 MICROGAME PROC RATE ----------------------------------------
    # How often Imago Rupta detours a boss ACTION (one of its 3-4 per enemy phase,
    # NOT the whole phase) into a genre shift. Two guards keep shifts "common but
    # never all you fight," so a player can't cheese the superboss by coasting on
    # winnable minigames:
    #   1) At most ONE shift per enemy phase (phase3_last_microgame_enemy_action).
    #   2) A cross-phase COOLDOWN: a fired shift suppresses RANDOM shifts for the
    #      next ~2 enemy phases (~one random shift per three phases), so they can
    #      never streak back-to-back. The one GUARANTEED shift on the vocal
    #      (<=50% HP) beat ignores the cooldown, so every run still sees at least
    #      one no matter how the dice fall.
    # Per eligible phase the chance ramps with the boss's missing HP (desperation).
    # All six are tunable starting points -- raise COOLDOWN to make shifts rarer,
    # or the chances to make eligible phases more reliably produce one.
    MSBF_PHASE3_MICROGAME_BASE_CHANCE = 0.04
    MSBF_PHASE3_MICROGAME_HP_SCALE = 0.28
    MSBF_PHASE3_MICROGAME_VOCAL_BONUS = 0.06
    MSBF_PHASE3_MICROGAME_LOW_HP_BONUS = 0.05
    MSBF_PHASE3_MICROGAME_CHANCE_CAP = 0.38
    MSBF_PHASE3_MICROGAME_COOLDOWN = 3

    # Typing QTE word bank ("the script demands a word"). Time limit scales with
    # length (see _start_phase_three_typing). Themed to the fight's meta.
    MSBF_TYPING_WORDS = [
        "REWRITE", "IMAGO", "RUPTURE", "DELETE", "GENRE", "SCRIPT", "REVISION",
        "REDACT", "NARRATIVE", "IDENTITY", "DRAFT", "EDIT", "ROLE", "MATSUDA",
        "ANTAGONIST", "PROTAGONIST", "CURTAIN", "REFUSE", "ASAHINA", "INUGAMI",
        "HIMEKO", "TSUBAKI", "GIASFELFEBREHBER", "FREEDOM", "CHAOS"
    ]
    # Typing time = a flat read/react buffer + a per-character typing allowance, so
    # a 4-letter word ("ROLE") and the 16-letter joke word ("GIASFELFEBREHBER") get
    # very different clocks. PER_CHAR ~0.36s is ~2.8 chars/sec -- tight but doable as
    # a copy-type (the word is shown), a real speed test without being unfair. MIN is
    # a floor so the shortest words can't drop below fair. Tune PER_CHAR up to soften.
    MSBF_TYPING_TIME_BASE = 1.3
    MSBF_TYPING_TIME_PER_CHAR = 0.36
    MSBF_TYPING_TIME_MIN = 2.4
    MSBF_QUIZ_TIME_LIMIT = 6.0

    # Quiz QTE bank (modeled on the Monika-mode timed choice, but self-contained).
    # Each entry: prompt, the one correct answer, and the wrong options. The
    # correct answer is the on-theme / lucid one so a player who has been paying
    # attention to the fight can reason it out -- a real test, not a coin flip.
    MSBF_QUIZ_BANK = [
        {
            "q": "She keeps switching genres. Why?",
            "correct": "It is desperate and has no real form left.",
            "wrong": ["It thinks the party will enjoy the variety.", "It is following a strict rehearsed script."],
        },
        {
            "q": "Her image is shattered. What is Matsuda actually hiding behind now?",
            "correct": "Nothing.",
            "wrong": ["A brand-new, stronger form.", "A perfect final draft."],
        },
        {
            "q": "Identity Null burns the role labels off the party. What does it punish?",
            "correct": "Being over-buffed.", "wrong": ["Guarding.", "Attacking with weapons."],
        },
        {
            "q": "What is the one honest thing left in this fight?",
            "correct": "The party's refusal to play along.",
            "wrong": ["Her next genre.", "The narrator's promises."],
        },
        {
            "q": "The script offers you a role. The right move is to:",
            "correct": "Refuse the role.", "wrong": ["Accept the lead.", "Ask for a rewrite."],
        },
        {
            "q": "Curtain Script threw danmaku at you. What genre was that?",
            "correct": "A bullet-hell shooter.", "wrong": ["A cooking show.", "A courtroom drama."],
        },
        {
            "q": "How does a genre-shift move actually end?",
            "correct": "Win it and the boss chips; lose it and the party pays.",
            "wrong": ["It always kills a party member.", "It can end the whole fight instantly."],
        },
        {
            "q": "What is (5 + 6 - 78 * 8525 + 9 / 3 - 3 % 9 + 2222222222 * 1337) * 0?",
            "correct": "0",
            "wrong": ["42", "127"],
        },
        {
            "q": "What is (5 + 6 - 78 * 8525 + 9 / 3 - 3 % 9 + 2222222222 * 1337) / 0?",
            "correct": "Undefined",
            "wrong": ["0", "127"],
        },
    ]

    # --- SHMUP (phase-3 bullet-hell) TUNING ----------------------------------
    # The dodge minigame's stage rect, player hitbox, duration, bullet cap,
    # movement speeds, and the named "spell card" patterns. One card per cast,
    # cycled so each is memorizable. Ticks run at TICK_SECONDS each; a full cast
    # is MSBF_SHMUP_DURATION_TICKS ticks (~15s). Rewards use the microgame rules.
    # Centred in the frame. These used to be (452, 30) -- the exact box the boss
    # stage occupied back when the fight was three panels, because the bullet
    # hell replaced that panel in place. The stage box is gone, so holding those
    # numbers just parked the playfield hard against the right edge with 450px
    # of dead space beside it. The field's own coordinates are stage-local, so
    # only the frame's origin moves.
    MSBF_SHMUP_STAGE_X = 247
    MSBF_SHMUP_STAGE_Y = 112
    MSBF_SHMUP_STAGE_WIDTH = 786
    MSBF_SHMUP_STAGE_HEIGHT = 458
    MSBF_SHMUP_TICK_SECONDS = 0.033
    # ~15 seconds per cast (TODO: "lasts 15 seconds").
    MSBF_SHMUP_DURATION_TICKS = int(round(15.0 / 0.033))
    MSBF_SHMUP_PLAYER_RADIUS = 6
    MSBF_SHMUP_MAX_BULLETS = 300
    MSBF_SHMUP_MAX_SPARKS = 90
    MSBF_SHMUP_GRACE_TICKS = 18
    MSBF_SHMUP_HIT_LIMIT = 3
    # Invulnerability window after a clip. Getting hit now only deletes the ONE
    # pellet that struck you (Undertale/Deltarune style -- no panic-clear of the
    # surrounding pattern), so the iframes are a touch longer to keep a hit in a
    # dense wall fair: the marker flickers for this many ticks (~0.8s) and can't be
    # clipped again until it ends.
    MSBF_SHMUP_HIT_INVULN_TICKS = 24
    # How fast the player marker blinks on/off during those iframes (ticks per
    # half-cycle); smaller = faster flicker.
    MSBF_SHMUP_IFRAME_BLINK_TICKS = 2
    # Keyboard-only player movement (px per 0.033s tick). Hold Shift to focus.
    MSBF_SHMUP_MOVE_SPEED = 6.6
    MSBF_SHMUP_FOCUS_SPEED = 2.8
    # Named spell-cards, one per cast, cycled in order so each is memorizable.
    MSBF_SHMUP_PATTERNS = ["spiral", "aimed", "walls"]
    MSBF_SHMUP_PATTERN_NAMES = {
        "spiral": "SPIRAL SCRIPTURE",
        "aimed": "REVISION SALVO",
        "walls": "MARGIN COLLAPSE",
    }
    # Needle rotation is bucketed so the bullet-field displayable (ui.rpy,
    # MSBFShmupField) can cache ONE rotated texture per (colour, size, bucket)
    # instead of rebuilding a rotate transform for every needle every tick.
    MSBF_SHMUP_ROT_BUCKETS = 48
    MSBF_SHMUP_ROT_BUCKET_DEG = 360.0 / 48

    def msbf_shmup_gate(frac):
        """Tick at `frac` of the way through one cast (0.0 = open, 1.0 = end).

        Every escalation gate in the spell cards goes through here. They used to
        be bare tick literals sized for the original 168-tick cast; when the cast
        grew to ~455 ticks, every "back half" ramp started firing inside the first
        third and each card played as one flat wall of maximum density for ten
        seconds. Stated as fractions, the cards keep their shape whatever the
        duration does next.
        """
        return int(MSBF_SHMUP_DURATION_TICKS * frac)

    MSBF_SFX_DIR = "assets/audio/sfx/msbf/"
    MSBF_FINAL_VICTORY_EXPLODE_DELAY = 0.84
    # explode.ogg is ~4.01s. The battle screen Returns 0.5s after result, then
    # cs_matsuda_02 clears pooled SFX, so the result delay must leave the tail room.
    MSBF_FINAL_VICTORY_RESULT_DELAY = 4.55
    MSBF_DAMAGE_VARIANCE_STDEV = 0.055
    MSBF_DAMAGE_VARIANCE_MIN = 0.88
    MSBF_DAMAGE_VARIANCE_MAX = 1.12
    MSBF_HEAL_VARIANCE_STDEV = 0.04
    MSBF_HEAL_VARIANCE_MIN = 0.90
    MSBF_HEAL_VARIANCE_MAX = 1.10
    MSBF_PLAYER_ACTION_CAP_MAX = 15
    MSBF_PRESS_TURN_SLOT_WIDTH = 40
    MSBF_PRESS_TURN_SLOT_SPACING = 4
    MSBF_PRESS_TURN_ROW_X = 7

    # --- SFX PATH HELPERS + SMALL MATH ---------------------------------------
    def msbf_sfx(filename):
        return MSBF_SFX_DIR + filename

    def msbf_clamp(value, lower, upper):
        return max(lower, min(upper, value))

    def msbf_gaussian_variance(stdev, lower, upper):
        return msbf_clamp(random.gauss(1.0, stdev), lower, upper)

    # --- BATTLE-WATCH / SAVE-LOCK HELPERS ------------------------------------
    # Is a battle running? Should save/load be blocked? And the teardown that
    # clears the global state + persistent battle token between fights.
    def msbf_battle_is_live():
        battle = globals().get("msbf_battle_state", None)
        return bool(battle is not None and getattr(battle, "result", None) is None)

    def msbf_save_load_locked():
        return bool(globals().get("msbf_battle_menu_locked", False) and msbf_battle_is_live())

    def msbf_clear_battle_watch():
        global msbf_battle_state
        global msbf_battle_menu_locked
        # Silence any pool cue still ringing (e.g. a danmaku hit as the fight ends) so
        # nothing bleeds into the story; the channels stay registered for next time.
        msbf_stop_pooled_sfx(0.2)
        msbf_battle_state = None
        msbf_battle_menu_locked = False
        try:
            persistent.msbf_battle_token = None
            persistent.msbf_battle_serial = 0
        except Exception:
            pass

    def msbf_stop_battle_music(fadeout=0.35):
        for channel_name in (
            "music",
            MSBF_IDMODE_PHASE3_INST_CHANNEL,
            MSBF_IDMODE_PHASE3_VOCAL_CHANNEL,
            MSBF_IDMODE_PHASE3_HEARTBEAT_CHANNEL,
        ):
            try:
                renpy.music.stop(channel=channel_name, fadeout=fadeout)
            except Exception:
                pass

    # --- SOUND TABLES --------------------------------------------------------
    # MSBF_UI_SFX: menu sounds. MSBF_SFX: every combat cue (incl. Touhou-segment
    # shot/graze/etc.). MSBF_SFX_LAYERS: extra one-shots layered UNDER a cue at a
    # given volume (e.g. "weak" also plays a quieter "hit" + "shuffle") for punch.
    MSBF_UI_SFX = {
        "hover": msbf_sfx("ui_hover.wav"),
        "accept": msbf_sfx("ui_accept.wav"),
        "denied": msbf_sfx("ui_denied.wav"),
    }

    MSBF_SFX = {
        "act": msbf_sfx("ui_accept.wav"),
        "denied": msbf_sfx("ui_denied.wav"),
        "turn": msbf_sfx("turn_ready.wav"),
        "turn_ready": msbf_sfx("turn_ready.wav"),
        "pass": msbf_sfx("pass.wav"),
        "hit": msbf_sfx("hit.wav"),
        "weak": msbf_sfx("weak.wav"),
        "crit": msbf_sfx("crit.wav"),
        "resist": msbf_sfx("resist.wav"),
        "miss": msbf_sfx("miss.wav"),
        "scan": msbf_sfx("scan.wav"),
        "heal": msbf_sfx("heal.wav"),
        "revive": msbf_sfx("revive.wav"),
        "buff": msbf_sfx("buff.wav"),
        "debuff": msbf_sfx("debuff.wav"),
        "guard": msbf_sfx("guard.wav"),
        "enemy": msbf_sfx("enemy.wav"),
        "shuffle": msbf_sfx("shuffle.wav"),
        "phase": msbf_sfx("phase.wav"),
        "explode": msbf_sfx("explode.ogg"),
        "recover": msbf_sfx("recover.wav"),
        "down": msbf_sfx("down.wav"),
        "victory": msbf_sfx("victory.wav"),
        "shmup_declare": msbf_sfx("phase.wav"),
        "shmup_shot": msbf_sfx("bullet01.ogg"),
        "shmup_burst": msbf_sfx("bullet02.ogg"),
        "shmup_hit": msbf_sfx("hit.wav"),
        "shmup_clear": msbf_sfx("recover.wav"),
        "shmup_fail": msbf_sfx("down.wav"),
        "type_key": msbf_sfx("ui_hover.wav"),
        "type_good": msbf_sfx("weak.wav"),
        "type_bad": msbf_sfx("ui_denied.wav"),
        "quiz_tick": msbf_sfx("ui_hover.wav"),
        "quiz_good": msbf_sfx("weak.wav"),
        "quiz_bad": msbf_sfx("ui_denied.wav"),
    }

    MSBF_SFX_LAYERS = {
        "hit": [("enemy", 0.16)],
        "weak": [("hit", 0.45), ("shuffle", 0.24)],
        "crit": [("hit", 0.52), ("buff", 0.28)],
        "resist": [("guard", 0.34)],
        "guard": [("buff", 0.20)],
        "enemy": [("hit", 0.18)],
        "enemy_aoe": [("hit", 0.30), ("debuff", 0.20)],
        "shuffle": [("scan", 0.22)],
        "phase": [("crit", 0.42), ("shuffle", 0.48), ("down", 0.18)],
        "victory": [("phase", 0.24)],
        "down": [("debuff", 0.32)],
    }

    # --- DATA CLASSES --------------------------------------------------------
    # MSBFSkill: one move (cost/kind/element/power/target/accuracy/crit/...).
    # `kind` is a behaviour tag the resolver switches on (damage, heal, focus,
    # guard, blue_*, phase3_*, etc.). Instances are stored once in MSBF_SKILLS.
    class MSBFSkill(object):
        def __init__(
                self,
                skill_id,
                name,
                cost=0,
                kind="damage",
                element="slash",
                power=0,
                target="boss",
                stat="offense",
                accuracy=1.0,
                crit=0.0,
                recoil=0.0,
                description=""):
            self.id = skill_id
            self.name = name
            self.cost = cost
            self.kind = kind
            self.element = element
            self.power = power
            self.target = target
            self.stat = stat
            self.accuracy = accuracy
            self.crit = crit
            self.recoil = recoil
            self.description = description

    # MSBFCombatant: one fighter (party member OR the boss). Holds stats, current
    # hp/mp, affinities, transient battle flags (guard/focus/taunt/row), buff
    # stages, and phase/adaptation bookkeeping. .skills resolves skill_ids -> the
    # shared MSBFSkill objects; .clamp() keeps values in range.
    class MSBFCombatant(object):
        def __init__(
                self,
                unit_id,
                name,
                max_hp,
                max_mp,
                offense,
                magic,
                defense,
                agility,
                attack_element="slash",
                weaknesses=None,
                resists=None,
                skills=None):
            self.id = unit_id
            self.name = name
            self.max_hp = max_hp
            self.hp = max_hp
            # Last HP the animated bar has "settled" to. The UI diffs hp vs bar_hp
            # (via MSBFBattleState._sync_bars) to spawn a draining damage-trail chip
            # so the bar reads as animating instead of snapping. See emit_bar.
            self.bar_hp = max_hp
            self.max_mp = max_mp
            self.mp = max_mp
            self.offense = offense
            self.magic = magic
            self.defense = defense
            self.agility = agility
            self.attack_element = attack_element
            self.weaknesses = list(weaknesses or [])
            self.resists = list(resists or [])
            self.skill_ids = list(skills or [])
            self.guard = False
            self.focus = False
            self.taunt = False
            self.row = "front"
            self.atk_stage = 0
            self.def_stage = 0
            self.agi_stage = 0
            self.phase = 1
            self.used_second_wind = False
            self.adapt_element = None
            self.adapt_turns = 0

        @property
        def alive(self):
            return self.hp > 0

        @property
        def hp_ratio(self):
            if self.max_hp <= 0:
                return 0.0
            return max(0.0, min(1.0, float(self.hp) / float(self.max_hp)))

        @property
        def skills(self):
            return [MSBF_SKILLS[skill_id] for skill_id in self.skill_ids]

        def clamp(self):
            self.hp = max(0, min(self.max_hp, int(self.hp)))
            self.mp = max(0, min(self.max_mp, int(self.mp)))
            self.atk_stage = max(-2, min(2, self.atk_stage))
            self.def_stage = max(-2, min(2, self.def_stage))
            self.agi_stage = max(-2, min(2, self.agi_stage))

    # --- SKILL TABLE ---------------------------------------------------------
    # The master move dictionary, keyed by id. Party skills, "enemy/blue" skills
    # (learnable flavor on Kotonoha), and the boss_*/phase3_* moves all live here.
    # Combatants reference these by id (see MSBF_ROSTER skills lists / msbf_make_boss).
    MSBF_SKILLS = {
        "attack": MSBFSkill(
            "attack",
            "Attack",
            kind="damage",
            element="weapon",
            power=68,
            accuracy=0.96,
            crit=0.06,
            description="A basic weapon strike."
        ),
        "attackpierce": MSBFSkill(
            "attackpierce",
            "Attack (Pierce)",
            kind="damage",
            element="pierce",
            power=68,
            accuracy=0.90,
            crit=0.12,
            description="A basic piercing strike."
        ),
        "ruin_edge": MSBFSkill(
            "ruin_edge",
            "Ruin Edge",
            cost=12,
            kind="damage",
            element="almighty",
            power=102,
            accuracy=0.96,
            crit=0.08,
            description="Almighty damage."
        ),
        "focus": MSBFSkill(
            "focus",
            "Focus",
            cost=5,
            kind="focus",
            element="support",
            description="Greatly strengthens the user's next attack."
        ),
        "fire": MSBFSkill(
            "fire",
            "Fire",
            cost=9,
            kind="damage",
            element="fire",
            power=118,
            stat="magic",
            accuracy=0.98,
            crit=0.03,
            description="Fire spell damage."
        ),
        "blizzard": MSBFSkill(
            "blizzard",
            "Blizzard",
            cost=9,
            kind="damage",
            element="ice",
            power=118,
            stat="magic",
            accuracy=0.98,
            crit=0.03,
            description="Ice spell damage."
        ),
        "thunder": MSBFSkill(
            "thunder",
            "Thunder",
            cost=9,
            kind="damage",
            element="lightning",
            power=118,
            stat="magic",
            accuracy=0.98,
            crit=0.03,
            description="Lightning spell damage."
        ),
        "aero": MSBFSkill(
            "aero",
            "Aero",
            cost=11,
            kind="true_damage",
            element="wind",
            power=128,
            stat="offense",
            accuracy=0.96,
            crit=0.08,
            description="Wind true damage that ignores defense, but still checks affinities."
        ),
        "firaga": MSBFSkill(
            "firaga",
            "Firaga",
            cost=22,
            kind="damage",
            element="fire",
            power=190,
            stat="magic",
            accuracy=0.94,
            crit=0.04,
            description="Expensive heavy fire spell damage."
        ),
        "scan": MSBFSkill(
            "scan",
            "Scan",
            cost=3,
            kind="analyze",
            element="support",
            description="Reveals affinities in phase 1. In phase 2, reads Matsuda's moveset instead."
        ),
        # DEV ONLY: swapped onto Seeker in place of Scan when config.developer is
        # on (see msbf_make_party), so phases can be blasted through without
        # editing HP. Always removes 50% of the boss's CURRENT max HP.
        "cleave": MSBFSkill(
            "cleave",
            "Cleave",
            cost=0,
            kind="dev_cleave",
            element="almighty",
            accuracy=1.0,
            description="DEV: always deals 50% of Matsuda's max HP."
        ),
        "aqua_breath": MSBFSkill(
            "aqua_breath",
            "Aqua Breath",
            cost=13,
            kind="damage",
            element="ice",
            power=138,
            stat="magic",
            accuracy=0.95,
            crit=0.04,
            description="Enemy skill: ice breath damage."
        ),
        "white_wind": MSBFSkill(
            "white_wind",
            "White Wind",
            cost=22,
            kind="white_wind",
            element="healing",
            power=0,
            stat="magic",
            target="party",
            description="Enemy skill: party healing based on Kotonoha's current HP."
        ),
        "thousand_needles": MSBFSkill(
            "thousand_needles",
            "1000 Needles",
            cost=18,
            kind="fixed_damage",
            element="almighty",
            power=260,
            accuracy=1.0,
            description="Enemy skill: fixed damage that ignores defense and affinities."
        ),
        "mighty_guard": MSBFSkill(
            "mighty_guard",
            "Mighty Guard",
            cost=24,
            kind="blue_guard",
            element="support",
            target="party",
            description="Enemy skill: raises party defense and guards everyone this turn."
        ),
        "bad_breath": MSBFSkill(
            "bad_breath",
            "Bad Breath",
            cost=16,
            kind="blue_debuff",
            element="support",
            description="Enemy skill: lowers Matsuda's attack, defense, and agility."
        ),
        "needle_shot": MSBFSkill(
            "needle_shot",
            "Needle Shot",
            cost=8,
            kind="damage",
            element="pierce",
            power=140,
            accuracy=0.97,
            crit=0.17,
            description="Precise pierce damage."
        ),
        "armor_piercer": MSBFSkill(
            "armor_piercer",
            "Armor Piercer",
            cost=16,
            kind="damage",
            element="pierce",
            power=188,
            accuracy=0.92,
            crit=0.20,
            description="Heavy pierce damage with high critical rate."
        ),
        "wild_swing": MSBFSkill(
            "wild_swing",
            "Wild Swing",
            cost=8,
            kind="damage",
            element="slash",
            power=170,
            accuracy=0.84,
            crit=0.32,
            description="Unstable slash damage with high critical rate."
        ),
        "reckless_blow": MSBFSkill(
            "reckless_blow",
            "Reckless Blow",
            cost=14,
            kind="damage",
            element="slash",
            power=240,
            accuracy=0.89,
            crit=0.22,
            recoil=0.10,
            description="Heavy slash damage. Costs HP after use."
        ),
        "war_cry": MSBFSkill(
            "war_cry",
            "War Cry",
            cost=12,
            kind="buff_attack_all",
            element="support",
            target="party",
            description="Raises party attack and draws attention."
        ),
        "cure": MSBFSkill(
            "cure",
            "Cure",
            cost=7,
            kind="heal",
            element="healing",
            power=170,
            stat="magic",
            target="ally",
            description="Restores HP to one wounded ally."
        ),
        "cura": MSBFSkill(
            "cura",
            "Cura",
            cost=14,
            kind="heal",
            element="healing",
            power=290,
            stat="magic",
            target="ally",
            description="Restores a large amount of HP to one ally."
        ),
        "medica": MSBFSkill(
            "medica",
            "Medica",
            cost=18,
            kind="heal_all",
            element="healing",
            power=150,
            stat="magic",
            target="party",
            description="Restores HP to all allies."
        ),
        "raise": MSBFSkill(
            "raise",
            "Raise",
            cost=20,
            kind="revive",
            element="healing",
            power=0,
            stat="magic",
            target="ally",
            description="Revives one downed ally with partial HP."
        ),
        "protect": MSBFSkill(
            "protect",
            "Protect",
            cost=10,
            kind="buff_defense_all",
            element="support",
            target="party",
            description="Raises party defense."
        ),
        "haste": MSBFSkill(
            "haste",
            "Haste",
            cost=13,
            kind="haste",
            element="support",
            target="party",
            description="Raises party agility. Once before Matsuda changes rhythm, steals one half-turn."
        ),
        "deprotect": MSBFSkill(
            "deprotect",
            "Deprotect",
            cost=11,
            kind="debuff_defense",
            element="support",
            description="Lowers Matsuda's defense."
        ),
        "slow": MSBFSkill(
            "slow",
            "Slow",
            cost=11,
            kind="debuff_attack",
            element="support",
            description="Lowers Matsuda's attack."
        ),
        "hexline": MSBFSkill(
            "hexline",
            "Hexline",
            cost=11,
            kind="damage",
            element="psychic",
            power=132,
            stat="magic",
            accuracy=0.95,
            crit=0.08,
            description="Psychic damage."
        ),
        "guard": MSBFSkill(
            "guard",
            "Guard",
            kind="guard",
            element="support",
            description="Reduces incoming damage until the enemy turn ends."
        ),
        "boss_slash": MSBFSkill(
            "boss_slash",
            "Crosscut",
            kind="damage",
            element="slash",
            power=92,
            accuracy=0.95,
            crit=0.08
        ),
        "boss_pierce": MSBFSkill(
            "boss_pierce",
            "Line Breaker",
            kind="damage",
            element="pierce",
            power=98,
            accuracy=0.94,
            crit=0.10
        ),
        "boss_fira": MSBFSkill(
            "boss_fira",
            "Fira",
            cost=0,
            kind="damage",
            element="fire",
            power=98,
            stat="magic",
            accuracy=0.96,
            crit=0.04
        ),
        "boss_blizzara": MSBFSkill(
            "boss_blizzara",
            "Blizzara",
            cost=0,
            kind="damage",
            element="ice",
            power=98,
            stat="magic",
            accuracy=0.96,
            crit=0.04
        ),
        "boss_thundara": MSBFSkill(
            "boss_thundara",
            "Thundara",
            cost=0,
            kind="damage",
            element="lightning",
            power=98,
            stat="magic",
            accuracy=0.96,
            crit=0.04
        ),
        "boss_firaga": MSBFSkill(
            "boss_firaga",
            "Firaga",
            cost=0,
            kind="damage",
            element="fire",
            power=116,
            stat="magic",
            accuracy=0.95,
            crit=0.05
        ),
        "boss_blizzaga": MSBFSkill(
            "boss_blizzaga",
            "Blizzaga",
            cost=0,
            kind="damage",
            element="ice",
            power=116,
            stat="magic",
            accuracy=0.95,
            crit=0.05
        ),
        "boss_thundaga": MSBFSkill(
            "boss_thundaga",
            "Thundaga",
            cost=0,
            kind="damage",
            element="lightning",
            power=116,
            stat="magic",
            accuracy=0.95,
            crit=0.05
        ),
        "boss_aeroga": MSBFSkill(
            "boss_aeroga",
            "Aeroga",
            cost=0,
            kind="damage",
            element="wind",
            power=66,
            target="all",
            stat="magic",
            accuracy=0.91,
            crit=0.04
        ),
        "boss_sweep": MSBFSkill(
            "boss_sweep",
            "Redline Sweep",
            kind="damage",
            element="wind",
            power=52,
            target="all",
            stat="magic",
            accuracy=0.88,
            crit=0.03
        ),
        "boss_focus": MSBFSkill(
            "boss_focus",
            "Limit Read",
            kind="focus",
            element="support"
        ),
        "boss_guard": MSBFSkill(
            "boss_guard",
            "Null Aegis",
            kind="boss_guard",
            element="support",
            target="self"
        ),
        "boss_second_wind": MSBFSkill(
            "boss_second_wind",
            "Second Wind",
            kind="heal",
            element="healing",
            power=240,
            target="self"
        ),
        # Genre-shift moves: each detours phase 3 into a real-time minigame
        # (bullet-hell / typing / quiz). Picked by the desperation-escalation
        # logic in _choose_phase_three_skill; resolved via _resolve_phase_three_*.
        # power/element/etc. are cosmetic here -- the reward/penalty is the fixed
        # microgame win/loss, not this skill's damage.
        "boss_curtain_script": MSBFSkill(
            "boss_curtain_script",
            "Curtain Script",
            kind="phase3_curtain",
            element="wind",
            power=58,
            target="all",
            stat="magic",
            accuracy=0.93,
            crit=0.04
        ),
        "boss_rewrite_order": MSBFSkill(
            "boss_rewrite_order",
            "Rewrite Order",
            kind="phase3_typing",
            element="psychic",
            target="all",
            stat="magic"
        ),
        "boss_multiple_choice": MSBFSkill(
            "boss_multiple_choice",
            "Multiple Choice Interrupt",
            kind="phase3_quiz",
            element="psychic",
            target="all",
            stat="magic"
        ),
        "boss_black_box_waltz": MSBFSkill(
            "boss_black_box_waltz",
            "Black Box Waltz",
            kind="phase3_black_box",
            element="psychic",
            power=40,
            target="all",
            stat="magic",
            accuracy=0.96,
            crit=0.02
        ),
        "boss_reticle_nightmare": MSBFSkill(
            "boss_reticle_nightmare",
            "Reticle Nightmare",
            kind="phase3_reticle",
            element="pierce",
            power=120,
            accuracy=0.96,
            crit=0.18
        ),
        "boss_identity_null": MSBFSkill(
            "boss_identity_null",
            "Identity Null",
            kind="phase3_null",
            element="almighty",
            power=60,
            target="all",
            stat="magic",
            accuracy=1.0,
            crit=0.0
        ),
    }

    # --- PLAYABLE ROSTER -----------------------------------------------------
    # The seven recruitable fighters (stats + affinities + skill loadout). The
    # party-select screen (ui.rpy) lets the player pick 4. MSBF_ROSTER_BY_ID /
    # MSBF_ALL_MEMBER_IDS are lookups built from this list just below.
    MSBF_ROSTER = [
        {
            "id": "seeker",
            "name": "Seeker",
            "role": "Spellblade",
            "summary": "All-rounder, jack-of-all-trades.",
            "max_hp": 560,
            "max_mp": 60,
            "offense": 60,
            "magic": 48,
            "defense": 50,
            "agility": 52,
            "attack_element": "slash",
            "weaknesses": [],
            "resists": [],
            "skills": ["attack", "scan", "ruin_edge", "fire", "blizzard", "thunder", "cure", "guard"],
        },
        {
            "id": "monika",
            "name": "Monika",
            "role": "Black Mage",
            "summary": "Best elemental burst and quick reads.",
            "max_hp": 400,
            "max_mp": 88,
            "offense": 32,
            "magic": 80,
            "defense": 30,
            "agility": 48,
            "attack_element": "slash",
            "weaknesses": ["pierce", "wind"],
            "resists": ["fire"],
            "skills": ["attack", "scan", "fire", "blizzard", "thunder", "firaga", "hexline", "guard"],
        },
        {
            "id": "kotonoha",
            "name": "Kotonoha",
            "role": "Blue Mage",
            "summary": "Unique skills and light utility.",
            "max_hp": 500,
            "max_mp": 82,
            "offense": 42,
            "magic": 66,
            "defense": 44,
            "agility": 56,
            "attack_element": "slash",
            "weaknesses": ["lightning"],
            "resists": ["psychic"],
            "skills": ["attack", "scan", "aqua_breath", "white_wind", "thousand_needles", "mighty_guard", "bad_breath", "guard"],
        },
        {
            "id": "asahina",
            "name": "Asahina",
            "role": "Halberdier",
            "summary": "Pierce damage and speed control.",
            "max_hp": 500,
            "max_mp": 62,
            "offense": 76,
            "magic": 28,
            "defense": 42,
            "agility": 74,
            "attack_element": "pierce",
            "weaknesses": ["fire"],
            "resists": ["pierce"],
            "skills": ["attackpierce", "needle_shot", "armor_piercer", "aero", "focus", "haste", "slow", "guard"],
        },
        {
            "id": "sam",
            "name": "Sam",
            "role": "Berserker",
            "summary": "Unrelenting strength and power.",
            "max_hp": 700,
            "max_mp": 50,
            "offense": 90,
            "magic": 22,
            "defense": 48,
            "agility": 34,
            "attack_element": "slash",
            "weaknesses": ["ice"],
            "resists": ["slash"],
            "skills": ["attack", "wild_swing", "reckless_blow", "war_cry", "focus", "ruin_edge", "deprotect", "guard"],
        },
        {
            "id": "tsubaki",
            "name": "Tsubaki",
            "role": "White Mage",
            "summary": "The primary healer.",
            "max_hp": 460,
            "max_mp": 112,
            "offense": 30,
            "magic": 76,
            "defense": 42,
            "agility": 44,
            "attack_element": "slash",
            "weaknesses": ["slash"],
            "resists": ["ice"],
            "skills": ["attack", "cure", "cura", "raise", "medica", "protect", "haste", "guard"],
        },
        {
            "id": "himeko",
            "name": "Himeko",
            "role": "Trickster",
            "summary": "Fast Scan, Haste, debuffs, and psychic burst.",
            "max_hp": 430,
            "max_mp": 76,
            "offense": 38,
            "magic": 62,
            "defense": 34,
            "agility": 76,
            "attack_element": "slash",
            "weaknesses": ["fire", "slash"],
            "resists": ["psychic"],
            "skills": ["attack", "scan", "haste", "deprotect", "slow", "hexline", "focus", "guard"],
        },
    ]

    MSBF_ROSTER_BY_ID = dict((entry["id"], entry) for entry in MSBF_ROSTER)
    MSBF_ALL_MEMBER_IDS = [entry["id"] for entry in MSBF_ROSTER]

    # --- PARTY-SELECT + UI HELPER FUNCTIONS ----------------------------------
    # Used by the party-select screen (ui.rpy) and HP/MP bars: pixel-width of a
    # bar, scroll-to-bottom, affinity/row labels, and the pick/row toggle logic
    # (max 4 members, default first two front row, can_begin requires 4 picks).
    def msbf_record_micro_win(kind):
        # Achievements feed ("Genre Savvy"): remember that this genre shift kind
        # has been won at least once. Persistent-only on purpose -- no ach_sync
        # from inside the battle sim; the victory hook in cs_matsuda_02 (or the
        # next Archive open) runs the sync and pops the toast.
        wins = list(getattr(persistent, "msbf_micro_wins", None) or [])
        if kind not in wins:
            wins.append(kind)
            persistent.msbf_micro_wins = wins

    def msbf_bar_width(value, max_value, width):
        if max_value <= 0:
            return 0
        ratio = max(0.0, min(1.0, float(value) / float(max_value)))
        return int(width * ratio)

    def msbf_scroll_adjustment_to_bottom(adjustment):
        try:
            adjustment.change(adjustment.range)
        except Exception:
            pass

    def msbf_affinity_label(elements):
        if not elements:
            return "None"
        return ", ".join(MSBF_AFFINITY_NAMES.get(element, element.title()) for element in elements)

    def msbf_row_label(row):
        return "Front" if row == "front" else "Rear"

    def msbf_default_rows(member_ids):
        rows = {}
        for idx, member_id in enumerate(member_ids):
            rows[member_id] = "front" if idx < 2 else "rear"
        return rows

    def msbf_front_count(member_ids, rows):
        return sum(1 for member_id in member_ids if rows.get(member_id, "front") == "front")

    def msbf_select_member(picks, rows, member_id):
        picks = list(picks)
        rows = dict(rows)
        if member_id in picks:
            picks.remove(member_id)
            rows.pop(member_id, None)
        elif len(picks) < 4:
            picks.append(member_id)
            rows[member_id] = "front" if msbf_front_count(picks, rows) < 2 else "rear"
        return picks, rows

    def msbf_remove_member(picks, rows, member_id):
        picks = list(picks)
        rows = dict(rows)
        if member_id in picks:
            picks.remove(member_id)
            rows.pop(member_id, None)
        return picks, rows

    def msbf_toggle_row(picks, rows, member_id):
        rows = dict(rows)
        current = rows.get(member_id, "front")
        if current == "front":
            rows[member_id] = "rear"
        else:
            rows[member_id] = "front"
        return rows

    def msbf_can_begin(picks, rows):
        return len(picks) == 4 and msbf_front_count(picks, rows) >= 1

    def msbf_party_config(member_ids, rows):
        return {
            "members": list(member_ids),
            "rows": dict(rows),
        }

    # --- BATTLE CONSTRUCTION -------------------------------------------------
    # make_party: instantiate MSBFCombatants from the chosen ids + row layout.
    # make_boss: build Matsuda (NOTE the debug max_hp=40 -- see file header).
    # new_battle: the public factory the story calls -> returns an MSBFBattleState.
    def msbf_make_party(member_ids, rows=None):
        rows = rows or msbf_default_rows(member_ids)
        party = []
        for member_id in member_ids:
            entry = MSBF_ROSTER_BY_ID[member_id]
            member_skills = entry["skills"]
            # DEV ONLY: give Seeker the Cleave test move in place of Scan.
            if config.developer and entry["id"] == "seeker":
                member_skills = ["cleave" if skill_id == "scan" else skill_id for skill_id in member_skills]
            combatant = MSBFCombatant(
                entry["id"],
                entry["name"],
                entry["max_hp"],
                entry["max_mp"],
                entry["offense"],
                entry["magic"],
                entry["defense"],
                entry["agility"],
                attack_element=entry["attack_element"],
                weaknesses=entry["weaknesses"],
                resists=entry["resists"],
                skills=member_skills
            )
            combatant.role = entry["role"]
            combatant.row = rows.get(member_id, "front")
            party.append(combatant)
        return party

    def msbf_make_boss():
        return MSBFCombatant(
            "matsuda",
            "Matsuda, Crimson-Azure",
            5200,
            999,
            68,
            70,
            50,
            54,
            attack_element="slash",
            weaknesses=["ice", "pierce"],
            resists=["fire"],
            skills=[]
        )

    def msbf_new_battle(member_config, id_mode=False):
        return MSBFBattleState(member_config, id_mode=id_mode)

    # =========================================================================
    # MSBFBattleState -- THE BATTLE BRAIN
    # Owns the party + boss combatants and ALL run-time state: turn phase, press-
    # turn icons, per-phase affinity bookkeeping, the log, the FX/float feeds, and
    # the shmup sub-state. The ui.rpy screen reads its properties to draw and calls
    # its methods to act. Roughly grouped (top->bottom): __init__ + display
    # properties -> log/FX/float/audio helpers -> turn economy -> player actions &
    # damage -> phase transitions -> enemy AI -> the phase-3 shmup simulation.
    # =========================================================================
    class MSBFBattleState(object):
        # Class-level defaults for fields added in the phase-3 microgame / HP-bar
        # pass, so a state built by older code (a mid-battle reload or an old save)
        # still resolves them instead of raising AttributeError. __init__ overrides
        # all of these with per-instance values for a fresh battle.
        #
        # THE LIST FIELDS ARE None HERE ON PURPOSE. A mutable class default is
        # shared by every state object that ever falls through to it -- which is
        # exactly the legacy path these defaults exist for -- so an .append()
        # would write hit rings and sparks into a list that outlives the battle
        # and bleeds into the next one. The three _list() accessors below install
        # a real per-instance list on first touch instead.
        bar_events = None
        bar_serial = 0
        shmup_sparks = None
        shmup_hit_fx = None
        typing_serial = 0
        typing_word = ""
        typing_input = ""
        typing_time_limit = MSBF_TYPING_TIME_MIN
        quiz_serial = 0
        quiz_prompt = ""
        quiz_options = ()
        quiz_cursor = 0
        quiz_time_limit = MSBF_QUIZ_TIME_LIMIT
        phase3_vocal_genre_done = False
        phase3_last_microgame_enemy_action = -99
        phase3_microgame_cooldown = 0
        party_downs = 0
        handover_to = None
        handover_delay = 1.15
        handover_serial = 0
        handover_mp_restored = False

        def __init__(self, member_config, id_mode=False):
            if isinstance(member_config, dict):
                member_ids = list(member_config.get("members", []))
                rows = dict(member_config.get("rows", {}))
            else:
                member_ids = list(member_config)
                rows = msbf_default_rows(member_ids)

            self.party = msbf_make_party(member_ids, rows)
            self.boss = msbf_make_boss()
            self.id_mode = bool(id_mode)
            self.phase = 1
            self.turn_phase = "setup"
            self.actor_index = 0
            self.press_turn_icons_state = []
            self.press_turn_fx_events = []
            self.press_turn_fx_serial = 0
            self.pending_half_turn = False
            self.haste_bonus_used_this_phase = False
            self.player_actions_this_phase = 0
            self.player_action_cap = MSBF_PLAYER_ACTION_CAP_MAX
            self.enemy_turns_remaining = 0
            self.enemy_bonus_remaining = 0
            self.enemy_press_turn_icons_state = []
            self.enemy_actions_this_phase = 0
            self.enemy_action_cap = 4
            self.enemy_settling = False
            self.enemy_step_delay = 0.35
            self.round_number = 0
            self.result = None
            self.analyzed = False
            self.log = []
            self.log_serial = 0
            self.fx_event = None
            self.fx_serial = 0
            self.float_events = []
            self.float_serial = 0
            self.fx_clear_delay = 0.70
            self.final_victory_whiteout = False
            self.final_victory_explode_played = False
            self.defeat_blackout = False
            self.phase_transition_delay = 0.18
            self.player_element_history = []
            self.heal_actions = 0
            self.last_player_action = None
            self.last_turn_bonus_converted = False
            self.last_enemy_target_id = None
            # Presentation feeds (read by ui.rpy each redraw): the last party
            # member to act + the element they cast (drives caster wind-up FX and
            # the element-tinted boss impact), and a serial-polled death feed that
            # fires a one-shot KO animation the instant a combatant drops.
            self.last_actor_index = None
            self.last_cast_element = None
            self.death_events = []
            self.death_serial = 0
            self.bar_events = []
            self.bar_serial = 0
            self.phase2_scan_insight_bag = []
            self.phase1_affinity_bag = []
            self.phase1_affinity_index = self._draw_phase_one_affinity_index(None)
            self.phase2_affinity_signature = None
            self.phase2_last_affinity_shift_round = -1
            self.phase2_weakness_hits = {}
            self.phase2_ai_stance = "balanced"
            self.phase2_ai_last_announced_stance = "balanced"
            self.phase2_opening_immunity = False
            self.phase2_transition_reveal_started = False
            self.phase3_started = False
            self.phase3_vocal_started = False
            self.phase3_vocal_genre_done = False
            self.phase3_last_microgame_enemy_action = -99
            self.phase3_microgame_cooldown = 0
            # Whole-fight KO tally (never reset by phase transitions) -- feeds the
            # "No One Gets Written Out" achievement check in cs_matsuda_02_victory.
            self.party_downs = 0
            self.phase3_scan_insight_bag = []
            self.phase3_genre_shift_count = 0
            self.phase3_reinforcements_added = 0
            self.shmup_serial = 0
            self.shmup_tick = 0
            self.shmup_hits = 0
            self.shmup_invuln_until_tick = 0
            self.shmup_player_x = MSBF_SHMUP_STAGE_WIDTH // 2
            self.shmup_player_y = MSBF_SHMUP_STAGE_HEIGHT - 70
            self.shmup_bullets = []
            self.shmup_source_skill_id = None
            self.shmup_sfx_cooldowns = {}
            self.shmup_focus = False
            self.shmup_poll_ok = False
            self.shmup_pattern = "spiral"
            self.shmup_source_x = MSBF_SHMUP_STAGE_WIDTH * 0.5
            self.shmup_source_y = 62.0
            self.shmup_sparks = []
            self.shmup_hit_fx = []
            # Typing / quiz QTE state (phase-3 genre-shift minigames). The live
            # inputs (typed text + quiz cursor) live HERE, not in screen vars,
            # because the overlays are `use`d inside msbf_battle_screen and screen-
            # variable scope lookups resolve against the parent screen there.
            self.typing_serial = 0
            self.typing_word = ""
            self.typing_input = ""
            self.typing_time_limit = MSBF_TYPING_TIME_MIN
            self.quiz_serial = 0
            self.quiz_prompt = ""
            self.quiz_options = []
            self.quiz_cursor = 0
            self.quiz_time_limit = MSBF_QUIZ_TIME_LIMIT
            self.phase_transition_title = "THE STAGE BEGINS ANEW"
            self.phase_transition_subtitle = "A WINGED ANGEL REWRITES THE SCRIPT"
            self.defeat_title = "THE STAGE GOES DARK"
            self.defeat_subtitle = "THE PARTY FALLS"
            self._reset_phase_two_player_read()
            if self.id_mode:
                self._configure_phase_two(restore_party=True)
                self.add_log("Id Mode skips the first bar. Tohu Imago is already awake.")
            else:
                self._set_phase_one_affinities(self.phase1_affinity_index)
            self.start_player_turn(initial=True)

        @property
        def boss_art(self):
            if self.phase == 1:
                return "msbf_matsuda_phase1"
            if self.phase == 3:
                return "msbf_matsuda_phase3"
            return "msbf_matsuda_phase2"

        @property
        def max_press_turns(self):
            alive_count = len(self.alive_party())
            return max(1, alive_count)

        @property
        def press_turn_icons(self):
            return list(self.press_turn_icons_state)

        @property
        def enemy_press_turn_icons(self):
            return list(self.enemy_press_turn_icons_state)

        @property
        def enemy_display_active(self):
            return self.enemy_phase_active or self.shmup_segment_active

        @property
        def active_press_turn_icons(self):
            if self.enemy_display_active:
                return self.enemy_press_turn_icons
            return self.press_turn_icons

        @property
        def active_actions_this_phase(self):
            if self.enemy_display_active:
                return self.enemy_actions_this_phase
            return self.player_actions_this_phase

        @property
        def active_action_cap(self):
            if self.enemy_display_active:
                return self.enemy_action_cap
            return self.player_action_cap

        @property
        def press_turn_label(self):
            if self.enemy_display_active:
                return "MATSUDA TURNS"
            return "PRESS TURNS"

        def _press_turn_fx_x(self, index):
            return MSBF_PRESS_TURN_ROW_X + (index * (MSBF_PRESS_TURN_SLOT_WIDTH + MSBF_PRESS_TURN_SLOT_SPACING))

        def _queue_press_turn_fx(self, side, kind, icon_type, index):
            if index is None:
                return

            icon_width = 36 if icon_type == "full" else 18
            icon_x = 2 if icon_type == "full" else int((MSBF_PRESS_TURN_SLOT_WIDTH - icon_width) / 2)
            self.press_turn_fx_serial += 1
            self.press_turn_fx_events.append({
                "serial": self.press_turn_fx_serial,
                "side": side,
                "kind": kind,
                "icon": icon_type,
                "index": index,
                "x": self._press_turn_fx_x(index),
                "width": icon_width,
                "icon_x": icon_x,
            })
            self.press_turn_fx_events = self.press_turn_fx_events[-6:]

        def clear_press_turn_fx(self):
            self.press_turn_fx_events = []

        @property
        def current_actor(self):
            if self.result or self.turn_phase != "player":
                return None
            for _i in range(len(self.party)):
                candidate = self.party[self.actor_index % len(self.party)]
                if candidate.alive:
                    return candidate
                self.actor_index += 1
            return None

        @property
        def enemy_phase_active(self):
            return self.turn_phase == "enemy" and not self.result

        @property
        def shmup_segment_active(self):
            return self.turn_phase == "shmup_segment" and not self.result

        @property
        def handover_active(self):
            """Between sides: the last action has landed, nobody acts yet.

            The tempo used to change on the SAME call that resolved the final
            action of a phase, so the enemy banner and the whole HUD swap landed
            on top of an impact that was still playing -- the hit was cut off by
            its own consequence. This state holds the frame for a beat so the
            action finishes, the handover reads as a deliberate beat, and only
            then does the other side get the tempo.
            """
            return self.turn_phase == "handover" and not self.result

        @property
        def typing_segment_active(self):
            return self.turn_phase == "typing_segment" and not self.result

        @property
        def quiz_segment_active(self):
            return self.turn_phase == "quiz_segment" and not self.result

        @property
        def microgame_active(self):
            # Any phase-3 "genre shift" minigame currently running as an overlay.
            return self.turn_phase in ("shmup_segment", "typing_segment", "quiz_segment") and not self.result

        @property
        def phase_transition_active(self):
            return self.turn_phase == "phase_transition" and not self.result

        @property
        def final_victory_active(self):
            return self.turn_phase == "victory_sequence" and not self.result

        @property
        def defeat_sequence_active(self):
            return self.turn_phase == "defeat_sequence" and not self.result

        @property
        def phase2_reveal_started(self):
            return bool(getattr(self, "phase2_transition_reveal_started", False))

        @property
        def active_actor_label(self):
            if self.result:
                return "Done"
            if self.turn_phase == "victory_sequence":
                return "Final Break"
            if self.turn_phase == "shmup_segment":
                return "Curtain Script"
            if self.turn_phase == "enemy":
                return "Matsuda"
            actor = self.current_actor
            if actor is None:
                return "Resolving"
            return actor.name

        def alive_party(self):
            return [member for member in self.party if member.alive]

        def defeated_party(self):
            return [member for member in self.party if not member.alive]

        def add_log(self, text):
            self.log.append(text)
            self.log_serial += 1
            if len(self.log) > 16:
                self.log = self.log[-16:]

        def clear_fx(self):
            self.fx_event = None
            self.fx_clear_delay = 0.70

        def emit_float(self, amount, kind="dmg", anchor="boss"):
            # Feed for floating combat numbers. anchor is "boss" or a party index.
            self.float_serial += 1
            self.float_events.append({
                "serial": self.float_serial,
                "amount": amount,
                "kind": kind,
                "anchor": anchor,
            })
            if len(self.float_events) > 10:
                self.float_events = self.float_events[-10:]

        def clear_float_events(self):
            self.float_events = []

        def emit_death(self, anchor):
            # One-shot KO cue. anchor is a party index (int) or "boss"; the screen
            # polls death_serial and plays a death burst at that combatant.
            # Every party KO funnels through here (enemy damage + recoil), so this
            # is also where the "No One Gets Written Out" achievement counts downs.
            if anchor != "boss":
                self.party_downs += 1
            self.death_serial += 1
            self.death_events.append({
                "serial": self.death_serial,
                "anchor": anchor,
            })
            if len(self.death_events) > 8:
                self.death_events = self.death_events[-8:]

        def clear_death_events(self):
            self.death_events = []

        # ----- HP-BAR DAMAGE TRAIL -------------------------------------------
        # A serial-polled feed (same shape as float/death events) that lets the UI
        # animate HP bars instead of snapping. _sync_bars is called once after each
        # resolved action; it diffs every combatant's hp against its settled bar_hp
        # and emits one chip event per changed bar (frm/to are 0..1 fractions).
        def _own_list(self, name):
            # Returns the INSTANCE's list for one of the None-defaulted fields at
            # the top of the class, creating it on first touch. Anything that
            # appends must go through here: on the legacy path those fields
            # resolve to the class attribute, so appending to `self.<name>`
            # directly would mutate a list every battle state shares.
            value = self.__dict__.get(name, None)
            if value is None:
                value = []
                setattr(self, name, value)
            return value

        def emit_bar(self, anchor, frm, to):
            self.bar_serial += 1
            events = self._own_list("bar_events")
            events.append({
                "serial": self.bar_serial,
                "anchor": anchor,
                "frm": frm,
                "to": to,
                "gain": to > frm,
            })
            if len(events) > 12:
                self.bar_events = events[-12:]

        def clear_bar_events(self):
            self.bar_events = []

        def _sync_one_bar(self, combatant, anchor):
            prev = getattr(combatant, "bar_hp", combatant.hp)
            if combatant.max_hp <= 0 or prev == combatant.hp:
                combatant.bar_hp = combatant.hp
                return
            frm = max(0.0, min(1.0, float(prev) / float(combatant.max_hp)))
            to = max(0.0, min(1.0, float(combatant.hp) / float(combatant.max_hp)))
            combatant.bar_hp = combatant.hp
            if abs(frm - to) < 0.002:
                return
            self.emit_bar(anchor, frm, to)

        def _sync_bars(self):
            self._sync_one_bar(self.boss, "boss")
            for idx, member in enumerate(self.party):
                self._sync_one_bar(member, idx)

        def _settle_bars(self):
            # Snap the bar trackers to current HP without emitting chips. Used when
            # HP is set directly (phase transitions / full restores) so those jumps
            # never animate as damage/heal trails.
            self.boss.bar_hp = self.boss.hp
            for member in self.party:
                member.bar_hp = member.hp

        def set_fx(self, event_name, sfx_name=None, duration=None):
            self.fx_event = event_name
            self.fx_serial += 1
            if duration is None:
                duration = 1.45 if event_name == "phase" else 0.70
            self.fx_clear_delay = duration
            if sfx_name:
                self._play_sfx(sfx_name)

        def _play_sfx(self, sfx_name):
            path = MSBF_SFX.get(sfx_name)
            if not path:
                return
            # Pooled so this cue AND the turn-change cue that often follows it both
            # ring out (they used to serialize on one channel and cut each other).
            msbf_play_pooled_sfx(path)
            for layer_name, volume in MSBF_SFX_LAYERS.get(sfx_name, []):
                layer_path = MSBF_SFX.get(layer_name)
                if layer_path:
                    msbf_play_pooled_sfx(layer_path, volume)

        def play_final_victory_explosion(self):
            if self.result or self.turn_phase != "victory_sequence":
                return
            if getattr(self, "final_victory_explode_played", False):
                return
            self.final_victory_explode_played = True
            self._play_sfx("explode")

        def _play_phase_two_music(self):
            try:
                renpy.music.play(
                    audio.epicbattlephase2,
                    channel="music",
                    loop=True,
                    fadeout=1.0,
                    fadein=0.0
                )
            except Exception:
                pass

        def _set_phase_three_layer_volumes(self, instrumental_volume, vocal_volume, delay=0.0):
            try:
                renpy.music.set_volume(instrumental_volume, delay=delay, channel=MSBF_IDMODE_PHASE3_INST_CHANNEL)
                renpy.music.set_volume(vocal_volume, delay=delay, channel=MSBF_IDMODE_PHASE3_VOCAL_CHANNEL)
            except Exception:
                pass

        def _play_phase_three_music(self, vocal=False):
            instrumental_volume = MSBF_IDMODE_PHASE3_INST_BED if vocal else 1.0
            self._set_phase_three_layer_volumes(instrumental_volume, 1.0 if vocal else 0.0)
            try:
                renpy.music.play(
                    MSBF_IDMODE_PHASE3_MUSIC_INST,
                    channel=MSBF_IDMODE_PHASE3_INST_CHANNEL,
                    loop=True,
                    fadeout=0.0,
                    fadein=0.0,
                    synchro_start=True
                )
                renpy.music.play(
                    MSBF_IDMODE_PHASE3_MUSIC_VOCAL,
                    channel=MSBF_IDMODE_PHASE3_VOCAL_CHANNEL,
                    loop=True,
                    fadeout=0.0,
                    fadein=0.0,
                    synchro_start=True
                )
                renpy.music.play(
                    MSBF_IDMODE_PHASE3_HEARTBEAT,
                    channel=MSBF_IDMODE_PHASE3_HEARTBEAT_CHANNEL,
                    loop=True,
                    fadeout=0.0,
                    fadein=0.0,
                    synchro_start=True
                )
            except Exception:
                pass

        def _crossfade_phase_three_vocal(self):
            try:
                renpy.music.set_volume(1.0, delay=0.0, channel=MSBF_IDMODE_PHASE3_INST_CHANNEL)
                renpy.music.set_volume(0.0, delay=0.0, channel=MSBF_IDMODE_PHASE3_VOCAL_CHANNEL)
                renpy.music.set_volume(1.0, delay=MSBF_IDMODE_PHASE3_VOCAL_FADEIN, channel=MSBF_IDMODE_PHASE3_VOCAL_CHANNEL)
                renpy.music.set_volume(MSBF_IDMODE_PHASE3_INST_BED, delay=MSBF_IDMODE_PHASE3_CROSSFADE, channel=MSBF_IDMODE_PHASE3_INST_CHANNEL)
            except Exception:
                pass

        def _play_current_phase_music(self):
            if self.phase == 3:
                self._play_phase_three_music(self.phase3_vocal_started)
            else:
                self._play_phase_two_music()

        def _fade_out_phase_music(self):
            msbf_stop_battle_music(0.35)

        def begin_phase_two_reveal(self):
            if self.result or self.phase not in (2, 3) or self.turn_phase != "phase_transition":
                return
            if self.phase2_reveal_started:
                return
            self.phase2_transition_reveal_started = True
            self.fx_event = "phase"
            self.fx_serial += 1
            self.fx_clear_delay = 5.25
            self._play_current_phase_music()
            self._play_sfx("phase")
            renpy.restart_interaction()

        # ----- TURN FLOW: start of the player's turn -------------------------
        # Refill press-turn icons (one per alive member), reset per-turn flags,
        # tick down boss adaptation, and log the round start.
        def start_player_turn(self, initial=False):
            if self.result:
                return
            self.clear_press_turn_fx()
            self.turn_phase = "player"
            self.enemy_turns_remaining = 0
            self.enemy_bonus_remaining = 0
            self.enemy_press_turn_icons_state = []
            self.enemy_actions_this_phase = 0
            self.enemy_settling = False
            self.round_number += 1
            self.press_turn_icons_state = ["full"] * self.max_press_turns
            self.pending_half_turn = False
            self.haste_bonus_used_this_phase = False
            self.player_actions_this_phase = 0
            self.player_action_cap = min(MSBF_PLAYER_ACTION_CAP_MAX, (self.max_press_turns * 2) + 1)
            if self.phase >= 2:
                self.phase2_opening_immunity = False
                self._reset_phase_two_player_read()
            self.actor_index = self._first_alive_index()
            for member in self.party:
                member.guard = False
                member.taunt = False
            if self.boss.adapt_turns > 0 and not initial:
                self.boss.adapt_turns -= 1
                if self.boss.adapt_turns <= 0:
                    self.add_log("Matsuda's temporary guard drops.")
                    self.boss.adapt_element = None
            if initial:
                if self.id_mode and self.phase == 2:
                    self.add_log("Tohu Imago tears the opening credits away.")
                else:
                    self.add_log("Matsuda steps onto the setpiece.")
            else:
                self.add_log("Round %d Start." % (self.round_number))

        def _first_alive_index(self):
            for idx, member in enumerate(self.party):
                if member.alive:
                    return idx
            return 0

        def can_use(self, skill):
            if self.turn_phase != "player":
                return False
            actor = self.current_actor
            if skill.kind == "revive" and not self.defeated_party():
                return False
            return actor is not None and actor.alive and actor.mp >= skill.cost

        def skill_needs_ally_target(self, skill):
            return skill.target == "ally" or skill.kind in ("heal", "revive")

        def valid_ally_targets(self, skill):
            if skill.kind == "revive":
                return self.defeated_party()
            return self.alive_party()

        def can_target(self, skill, target):
            if not self.skill_needs_ally_target(skill):
                return False
            if target is None:
                return False
            return target in self.valid_ally_targets(skill)

        def _has_press_turns(self):
            return len(self.press_turn_icons_state) > 0

        def _remove_icon(self, icon_type):
            if icon_type not in self.press_turn_icons_state:
                return False
            idx = self.press_turn_icons_state.index(icon_type)
            self.press_turn_icons_state.pop(idx)
            self._queue_press_turn_fx("player", "spend", icon_type, idx)
            return True

        def _convert_full_to_half(self):
            for idx, icon in enumerate(self.press_turn_icons_state):
                if icon == "full":
                    self.press_turn_icons_state[idx] = "half"
                    self._queue_press_turn_fx("player", "convert", "full", idx)
                    return True
            return False

        def _consume_half_priority(self):
            if self._remove_icon("half"):
                return True
            return self._remove_icon("full")

        def _consume_pass_turn(self):
            if self._remove_icon("half"):
                return
            self._convert_full_to_half()

        def _has_enemy_press_turns(self):
            return len(self.enemy_press_turn_icons_state) > 0

        def _remove_enemy_icon(self, icon_type):
            if icon_type not in self.enemy_press_turn_icons_state:
                return False
            idx = self.enemy_press_turn_icons_state.index(icon_type)
            self.enemy_press_turn_icons_state.pop(idx)
            self._queue_press_turn_fx("enemy", "spend", icon_type, idx)
            return True

        def _convert_enemy_full_to_half(self):
            for idx, icon in enumerate(self.enemy_press_turn_icons_state):
                if icon == "full":
                    self.enemy_press_turn_icons_state[idx] = "half"
                    self._queue_press_turn_fx("enemy", "convert", "full", idx)
                    return True
            return False

        def _consume_enemy_half_priority(self):
            if self._remove_enemy_icon("half"):
                return True
            return self._remove_enemy_icon("full")

        def _apply_player_turn_cost(self, outcome):
            self.last_turn_bonus_converted = False
            if outcome == "minor":
                self._consume_pass_turn()
                return

            if outcome in ("weak", "critical"):
                self.last_turn_bonus_converted = self._convert_full_to_half()
                if not self.last_turn_bonus_converted:
                    self._remove_icon("half")
                return

            self._consume_half_priority()

            if outcome == "resist" and self._has_press_turns():
                self._consume_half_priority()
                self.add_log("The resisted hit burns extra tempo.")

        def _apply_enemy_turn_cost(self, outcome):
            if outcome in ("weak", "critical"):
                if not self._convert_enemy_full_to_half():
                    self._remove_enemy_icon("half")
                return

            self._consume_enemy_half_priority()

            if outcome == "resist" and self._has_enemy_press_turns():
                self._consume_enemy_half_priority()
                self.add_log("The resisted hit burns Matsuda's tempo.")

        def _record_player_action(self):
            self.player_actions_this_phase += 1
            return self.player_actions_this_phase >= self.player_action_cap

        def _record_enemy_action(self):
            self.enemy_actions_this_phase += 1
            return self.enemy_actions_this_phase >= self.enemy_action_cap

        def _force_player_phase_limit(self):
            self.press_turn_icons_state = []
            self.add_log("Your side has reached the %d-action limit for this tempo cycle." % self.player_action_cap)

        def _force_enemy_phase_limit(self):
            self.enemy_press_turn_icons_state = []
            self.add_log("Matsuda hits the %d-action limit for this tempo cycle." % self.enemy_action_cap)

        def _finish_player_phase(self):
            self._restore_party_mp()
            self.begin_handover("enemy")

        def begin_handover(self, to_side):
            """Hand the tempo over after a beat, instead of on this frame."""
            if self.result:
                return
            # NOTE: the press-turn FX are deliberately NOT cleared here. This
            # runs on the same frame as the action that ended the phase, so
            # clearing them cancelled the spend-flash on the very last pip --
            # the one moment the player most wants to see it. The battle
            # screen's own 0.58s timer retires them, and start_player_turn /
            # start_enemy_phase both clear on the way in anyway.
            self.turn_phase = "handover"
            self.handover_to = to_side
            # The tempo cue is NOT played here either. begin_handover runs on
            # the same frame as whatever ended the phase, so a cue raised here
            # lands on top of that action's own sound -- and fires early
            # whenever the phase ends on an affinity shuffle. msbf_turnover_sweep plays
            # it instead, because that screen only exists once fx_event has
            # cleared, which is the actual start of the handover beat.
            # The serial is what the tempo card keys off. It CANNOT key off the
            # round number: start_player_turn increments that, so a card keyed
            # to the round fired once for the handover and then a second time
            # the instant the new turn began, with a different number on it.
            self.handover_serial += 1
            # The clock does not start here. The screen only begins counting
            # once fx_event has cleared, so this is the length of the handover
            # BEAT, not of the beat plus whatever impact preceded it.
            self.handover_delay = 1.15
            renpy.restart_interaction()

        def finish_handover(self):
            if self.result or self.turn_phase != "handover":
                return
            to_side = self.handover_to or "enemy"
            self.handover_to = None
            self.handover_mp_restored = False
            if to_side == "player":
                self.start_player_turn()
            else:
                self.start_enemy_phase()
            renpy.restart_interaction()

        def _restore_member_mp(self, member, ratio):
            if member.max_mp <= 0 or member.mp >= member.max_mp:
                return 0
            restore_amount = max(1, int(member.max_mp * ratio))
            old_mp = member.mp
            member.mp = min(member.max_mp, member.mp + restore_amount)
            return member.mp - old_mp

        def _restore_party_mp(self):
            total_restored = 0
            for member in self.party:
                total_restored += self._restore_member_mp(member, 0.10)
            if total_restored > 0:
                self.add_log("The party catches its breath and recovers 10% MP.")
                # NO set_fx HERE. This runs inside _finish_player_phase, on the
                # same frame as the action that ended the phase -- so setting
                # the FX slot overwrote that action's own cue ("hit") with
                # "recover_mp" the instant it was raised. The boss's recoil
                # stopped (msbf_boss_smear_for saw no hit), the camera punch and
                # deck shockwave never fired (recover_mp has no impact weight),
                # and the recover sound cut the hit sound. The entire last
                # player action of every phase was being erased one frame in.
                #
                # It is a HANDOVER event, not an impact, so the sweep shows it.
                self.handover_mp_restored = True

        def _restore_party_for_phase_two(self):
            for member in self.party:
                member.hp = member.max_hp
                member.mp = member.max_mp
                member.guard = False
                member.taunt = False
                member.clamp()

        def _summon_full_roster_for_phase_three(self):
            current_ids = [member.id for member in self.party]
            missing_ids = [member_id for member_id in MSBF_ALL_MEMBER_IDS if member_id not in current_ids]
            if not missing_ids:
                return 0

            rows = dict((member.id, member.row) for member in self.party)
            for member_id in missing_ids:
                front_count = sum(1 for current_id in current_ids if rows.get(current_id, "front") == "front")
                rows[member_id] = "front" if front_count < 3 else "rear"
                current_ids.append(member_id)

            self.party.extend(msbf_make_party(missing_ids, rows))
            return len(missing_ids)

        def _phase_two_opening_immunity_active(self):
            return self.phase in (2, 3) and self.turn_phase in ("enemy", "shmup_segment") and bool(getattr(self, "phase2_opening_immunity", False))

        def _apply_enemy_damage_to_member(self, target, damage):
            old_hp = target.hp
            if self._phase_two_opening_immunity_active() and target.hp > 0 and target.hp - damage <= 0:
                target.hp = 1
            else:
                target.hp -= damage
                target.clamp()
            dealt = max(0, old_hp - target.hp)
            try:
                _idx = self.party.index(target)
            except ValueError:
                _idx = "boss"
            self.emit_float(dealt, "enemy", _idx)
            if old_hp > 0 and target.hp <= 0 and _idx != "boss":
                self.emit_death(_idx)
            # Opening immunity can reduce lethal damage to the HP delta above;
            # callers use that exact amount for combat-log totals.
            return dealt

        def _reset_phase_two_player_read(self):
            self.phase2_player_actions_observed = 0
            self.phase2_player_turn_damage = 0
            self.phase2_player_aggression = 0.0
            self.phase2_player_defense = 0.0
            self.phase2_player_weak_hits = 0
            self.phase2_player_critical_hits = 0

        def _record_phase_two_player_action(self, actor, skill, outcome, damage_done):
            if self.phase not in (2, 3):
                return

            self.phase2_player_actions_observed += 1
            self.phase2_player_turn_damage += max(0, int(damage_done))

            if outcome == "critical":
                self.phase2_player_critical_hits += 1

            if skill is None:
                self.phase2_player_defense += 1.0
                return

            if skill.kind in ("damage", "true_damage", "fixed_damage"):
                self.phase2_player_aggression += 2.0
                damage_ratio = 0.0
                if self.boss.max_hp > 0:
                    damage_ratio = float(max(0, int(damage_done))) / float(self.boss.max_hp)
                if damage_ratio >= 0.14:
                    self.phase2_player_aggression += 1.8
                elif damage_ratio >= 0.08:
                    self.phase2_player_aggression += 1.0
                if outcome == "critical":
                    self.phase2_player_aggression += 0.6
                return

            if skill.kind in ("focus", "buff_attack_all", "debuff_defense", "haste"):
                self.phase2_player_aggression += 1.35
                return

            if skill.kind in ("heal_all", "white_wind", "revive", "blue_guard"):
                self.phase2_player_defense += 2.4
                return

            if skill.kind in ("heal", "guard", "buff_defense_all"):
                self.phase2_player_defense += 2.0
                return

            if skill.kind in ("debuff_attack", "blue_debuff"):
                self.phase2_player_defense += 1.6
                return

            if skill.kind == "analyze":
                self.phase2_player_defense += 0.5

        def _update_phase_two_ai_stance(self):
            if self.phase not in (2, 3) or self.phase2_player_actions_observed <= 0:
                self.phase2_ai_stance = "balanced"
                return

            damage_ratio = 0.0
            if self.boss.max_hp > 0:
                damage_ratio = float(self.phase2_player_turn_damage) / float(self.boss.max_hp)

            aggression = self.phase2_player_aggression + self.phase2_player_weak_hits * 0.8
            defense = self.phase2_player_defense
            next_stance = "balanced"
            if self.phase == 3 and (aggression >= defense + 1.2 or damage_ratio >= 0.10 or self.phase2_player_weak_hits >= 1):
                next_stance = "defensive"
            elif self.phase == 3 and (defense >= aggression + 1.4 or (defense >= 2.5 and damage_ratio < 0.08)):
                next_stance = "aggressive"
            elif aggression >= defense + 2.5 or damage_ratio >= 0.16 or self.phase2_player_weak_hits >= 2:
                next_stance = "defensive"
            elif defense >= aggression + 2.0 or (defense >= 3.5 and damage_ratio < 0.08):
                next_stance = "aggressive"

            if next_stance != self.phase2_ai_last_announced_stance:
                if next_stance == "defensive":
                    self.add_log("Matsuda reads the assault and folds into a defensive theorem.")
                elif next_stance == "aggressive":
                    self.add_log("Matsuda reads the stall and sharpens her killing line.")
                elif self.phase2_ai_last_announced_stance != "balanced":
                    self.add_log("Matsuda's read loosens as the party changes tempo.")
                self.phase2_ai_last_announced_stance = next_stance

            self.phase2_ai_stance = next_stance

        def _reset_phase_two_adaptation(self):
            self.phase2_weakness_hits = {}
            self.player_element_history = []
            self.boss.adapt_element = None
            self.boss.adapt_turns = 0

        def _phase_two_affinity_signature(self, weaknesses, resists):
            return (tuple(sorted(weaknesses)), tuple(sorted(resists)))

        def _phase_affinity_counts(self):
            if self.phase == 3:
                return MSBF_PHASE3_WEAKNESS_COUNT, MSBF_PHASE3_RESIST_COUNT
            return MSBF_PHASE2_WEAKNESS_COUNT, MSBF_PHASE2_RESIST_COUNT

        def _draw_phase_two_affinities(self):
            previous = self.phase2_affinity_signature
            fallback = None
            weakness_count, resist_count = self._phase_affinity_counts()
            for _i in range(12):
                elements = list(MSBF_PHASE2_AFFINITY_ELEMENTS)
                random.shuffle(elements)
                weaknesses = sorted(elements[:weakness_count])
                resists = sorted(elements[weakness_count:weakness_count + resist_count])
                signature = self._phase_two_affinity_signature(weaknesses, resists)
                if fallback is None:
                    fallback = (weaknesses, resists, signature)
                if signature != previous:
                    return weaknesses, resists, signature
            return fallback

        def _set_phase_two_affinities(self, weaknesses, resists, signature=None):
            self.boss.weaknesses = list(weaknesses)
            self.boss.resists = list(resists)
            self.phase2_affinity_signature = signature or self._phase_two_affinity_signature(weaknesses, resists)
            self._reset_phase_two_adaptation()

        def _shuffle_phase_two_affinities(self, initial=False):
            if self.phase not in (2, 3):
                return
            weaknesses, resists, signature = self._draw_phase_two_affinities()
            self._set_phase_two_affinities(weaknesses, resists, signature)
            self.phase2_last_affinity_shift_round = self.round_number
            self.phase2_scan_insight_bag = []
            self.analyzed = False
            if not initial:
                self.set_fx("shuffle", "shuffle")
                if self.phase == 3:
                    self.add_log("Imago Rupta ruptures its affinities. The read window collapses.")
                else:
                    self.add_log("Matsuda rewrites her hidden affinities. Her reads reset.")

        def finish_phase_transition(self):
            if self.result or self.turn_phase != "phase_transition":
                return
            if self.phase in (2, 3) and not self.phase2_reveal_started:
                self.begin_phase_two_reveal()
                return
            self.phase_transition_delay = 0.18
            self.start_enemy_phase()
            renpy.restart_interaction()

        def finish_final_victory(self):
            if self.result or self.turn_phase != "victory_sequence":
                return
            self.final_victory_whiteout = True
            self.clear_fx()
            self.result = "victory"
            renpy.restart_interaction()

        # ----- DEFEAT SEQUENCE -----------------------------------------------
        # A party wipe no longer flips result instantly (which the screen would
        # bounce to a 0.5s Return). Instead it enters a "defeat_sequence" phase
        # that the screen plays as a cinematic (drain -> loom -> verdict -> dark)
        # before finish_defeat() finally sets result. All six wipe sites funnel
        # through _trigger_defeat (idempotent).
        def _trigger_defeat(self):
            if self.result or self.turn_phase == "defeat_sequence":
                return
            self.turn_phase = "defeat_sequence"
            self.press_turn_icons_state = []
            self.enemy_press_turn_icons_state = []
            self.clear_press_turn_fx()
            self.shmup_bullets = []
            self._fade_out_phase_music()
            self.set_fx("final_defeat", "down", 3.4)

        def finish_defeat(self):
            if self.result or self.turn_phase != "defeat_sequence":
                return
            self.defeat_blackout = True
            self.clear_fx()
            self.result = "defeat"
            renpy.restart_interaction()

        def player_pass(self):
            if self.result or self.turn_phase != "player":
                return
            actor = self.current_actor
            if actor is None:
                return
            self._consume_pass_turn()
            self._record_phase_two_player_action(actor, None, "minor", 0)
            limit_reached = self._record_player_action()
            self.add_log("%s passes and spends half a press turn." % actor.name)
            self.set_fx("pass", "pass")
            self.actor_index = (self.actor_index + 1) % len(self.party)
            if limit_reached and self._has_press_turns():
                self._force_player_phase_limit()
            if not self._has_press_turns():
                self._finish_player_phase()
            renpy.restart_interaction()

        # ----- PLAYER ACTIONS + DAMAGE ---------------------------------------
        # player_use_skill is the entry point the battle screen calls when the
        # current actor commits a move; it spends MP, resolves the effect via
        # _resolve_player_skill, applies press-turn cost (weak/crit grant tempo,
        # resist/miss lose it), and advances to the next actor or the enemy phase.
        # The _damage_boss / _true_damage_boss / _fixed_damage_boss helpers do the
        # actual number-crunching against the boss's current affinities.
        def player_use_skill(self, skill, target=None):
            if self.result or self.turn_phase != "player":
                return
            actor = self.current_actor
            if actor is None:
                return
            if self.skill_needs_ally_target(skill) and not self.can_target(skill, target):
                self.add_log("%s needs a valid target." % skill.name)
                self._play_sfx("denied")
                renpy.restart_interaction()
                return
            if actor.mp < skill.cost:
                self.add_log("%s does not have enough MP." % actor.name)
                self._play_sfx("denied")
                renpy.restart_interaction()
                return

            actor.mp -= skill.cost
            actor.clamp()
            self.pending_half_turn = False
            boss_hp_before = self.boss.hp
            try:
                self.last_actor_index = self.party.index(actor)
            except ValueError:
                self.last_actor_index = None
            self.last_cast_element = self._actual_element(actor, skill) if skill.kind in ("damage", "true_damage") else skill.element
            outcome = self._resolve_player_skill(actor, skill, target)
            self._sync_bars()
            self._record_phase_two_player_action(actor, skill, outcome, max(0, boss_hp_before - self.boss.hp))
            self._apply_player_turn_cost(outcome)
            if self.pending_half_turn:
                self.press_turn_icons_state.append("half")
                self._queue_press_turn_fx("player", "gain", "half", len(self.press_turn_icons_state) - 1)
                self.pending_half_turn = False
            limit_reached = self._record_player_action()
            self.last_player_action = skill.id

            if outcome in ("weak", "critical"):
                self._grant_player_bonus(outcome)

            if self.result:
                renpy.restart_interaction()
                return

            if self._handle_boss_phase_thresholds():
                renpy.restart_interaction()
                return

            if self.boss.hp <= 0:
                self._handle_boss_bar_break()
                if self.result or self.phase_transition_active or self.final_victory_active:
                    renpy.restart_interaction()
                    return

            if not self.alive_party():
                self._trigger_defeat()
                renpy.restart_interaction()
                return

            self.actor_index = (self.actor_index + 1) % len(self.party)
            if limit_reached and self._has_press_turns():
                self._force_player_phase_limit()
            if not self._has_press_turns():
                self._finish_player_phase()

            renpy.restart_interaction()

        def _resolve_player_skill(self, actor, skill, target=None):
            if skill.kind == "dev_cleave":
                damage = max(1, int(self.boss.max_hp * 0.5))
                self.boss.hp -= damage
                self.boss.clamp()
                self.add_log("%s uses %s and carves away half of %s." % (actor.name, skill.name, self.boss.name))
                self.set_fx("crit", "crit")
                self.emit_float(damage, "crit", "boss")
                return "normal"

            if skill.kind == "guard":
                actor.guard = True
                recovered = self._restore_member_mp(actor, 0.10)
                if recovered > 0:
                    self.add_log("%s guards and recovers %d MP." % (actor.name, recovered))
                else:
                    self.add_log("%s guards." % actor.name)
                self.set_fx("guard", "guard")
                return "normal"

            if skill.kind == "focus":
                actor.focus = True
                self.add_log("%s focuses for the next strike." % actor.name)
                self.set_fx("buff", "buff")
                return "normal"

            if skill.kind == "analyze":
                if self.phase >= 2:
                    if self.phase == 3:
                        self.add_log("%s scans, but Imago Rupta answers in overlapping genres." % actor.name)
                    else:
                        self.add_log("%s scans, but Matsuda's new form returns only static." % actor.name)
                    self.add_log(self._phase_two_scan_insight())
                    self.set_fx("scan", "scan")
                    return "minor"

                self.analyzed = True
                self.add_log("Scan: Weak to %s. Resists %s." % (
                    msbf_affinity_label(self.boss.weaknesses),
                    msbf_affinity_label(self.boss.resists)
                ))
                self.set_fx("scan", "scan")
                return "minor"

            if skill.kind == "heal":
                if target is None:
                    target = self._lowest_wounded_ally()
                amount = self._healing_amount(actor, skill)
                old_hp = target.hp
                target.hp += amount
                target.clamp()
                self.heal_actions += 1
                self.add_log("%s casts %s. %s recovers %d HP." % (actor.name, skill.name, target.name, amount))
                self.set_fx("heal", "heal")
                try:
                    self.emit_float(max(0, target.hp - old_hp), "heal", self.party.index(target))
                except ValueError:
                    pass
                return "normal"

            if skill.kind == "heal_all":
                amount = self._healing_amount(actor, skill)
                for member in self.alive_party():
                    old_hp = member.hp
                    member.hp += amount
                    member.clamp()
                    self.emit_float(max(0, member.hp - old_hp), "heal", self.party.index(member))
                self.heal_actions += 1
                self.add_log("%s casts %s. The party recovers %d HP." % (actor.name, skill.name, amount))
                self.set_fx("heal", "heal")
                return "normal"

            if skill.kind == "white_wind":
                amount = self._white_wind_amount(actor)
                for member in self.alive_party():
                    old_hp = member.hp
                    member.hp += amount
                    member.clamp()
                    self.emit_float(max(0, member.hp - old_hp), "heal", self.party.index(member))
                self.heal_actions += 1
                self.add_log("%s calls White Wind. The party recovers %d HP from her borrowed life force." % (actor.name, amount))
                self.set_fx("heal", "heal")
                return "normal"

            if skill.kind == "revive":
                if target is None:
                    target = self._first_defeated_ally()
                if target is None:
                    self.add_log("%s casts %s, but nobody is down." % (actor.name, skill.name))
                    self.set_fx("miss", "denied")
                    return "normal"
                revive_amount = max(1, int(target.max_hp * 0.35 + actor.magic * 0.75))
                target.hp = min(target.max_hp, revive_amount)
                target.guard = True
                target.clamp()
                self.heal_actions += 1
                self.add_log("%s casts %s. %s gets back up with %d HP." % (actor.name, skill.name, target.name, target.hp))
                self.set_fx("revive", "revive")
                return "normal"

            if skill.kind == "buff_attack_all":
                for member in self.alive_party():
                    member.atk_stage += 1
                    member.clamp()
                actor.taunt = True
                self.add_log("%s uses War Cry. Attack rises, and Matsuda notices." % actor.name)
                self.set_fx("buff", "buff")
                return "normal"

            if skill.kind == "buff_defense_all":
                for member in self.alive_party():
                    member.def_stage += 1
                    member.clamp()
                self.add_log("%s casts Protect. Defense rises." % actor.name)
                self.set_fx("guard", "guard")
                return "normal"

            if skill.kind == "blue_guard":
                for member in self.alive_party():
                    member.def_stage += 1
                    member.guard = True
                    member.clamp()
                self.add_log("%s mimics Mighty Guard. The party braces behind monster magic." % actor.name)
                self.set_fx("guard", "guard")
                return "normal"

            if skill.kind == "haste":
                for member in self.alive_party():
                    member.agi_stage += 1
                    member.clamp()
                if self.haste_bonus_used_this_phase:
                    self.add_log("%s casts Haste. Agility rises, but the tempo boost is already spent." % actor.name)
                else:
                    self.pending_half_turn = True
                    self.haste_bonus_used_this_phase = True
                    self.add_log("%s casts Haste. Agility rises, and the party steals one half-turn." % actor.name)
                self.set_fx("buff", "buff")
                return "normal"

            if skill.kind == "debuff_defense":
                self.boss.def_stage -= 1
                self.boss.clamp()
                self.add_log("%s casts Deprotect. Matsuda's defense falls." % actor.name)
                self.set_fx("debuff", "debuff")
                return "normal"

            if skill.kind == "debuff_attack":
                self.boss.atk_stage -= 1
                self.boss.clamp()
                self.add_log("%s casts Slow. Matsuda's offense slips." % actor.name)
                self.set_fx("debuff", "debuff")
                return "normal"

            if skill.kind == "blue_debuff":
                self.boss.atk_stage -= 1
                self.boss.def_stage -= 1
                self.boss.agi_stage -= 1
                self.boss.clamp()
                self.add_log("%s exhales Bad Breath. Matsuda's stance, guard, and timing all foul up." % actor.name)
                self.set_fx("debuff", "debuff")
                return "normal"

            if skill.kind == "fixed_damage":
                return self._fixed_damage_boss(actor, skill)

            if skill.kind == "true_damage":
                element = self._actual_element(actor, skill)
                self._track_player_element(element)
                return self._true_damage_boss(actor, skill, element)

            if skill.kind == "damage":
                element = self._actual_element(actor, skill)
                self._track_player_element(element)
                return self._damage_boss(actor, skill, element)

            return "normal"

        def _fixed_damage_boss(self, actor, skill):
            damage = max(1, int(skill.power))
            self.boss.hp -= damage
            self.boss.clamp()
            self.add_log("%s uses %s for %d fixed damage." % (actor.name, skill.name, damage))
            self.set_fx("hit", "hit")
            self.emit_float(damage, "dmg", "boss")
            return "normal"

        def _true_damage_boss(self, actor, skill, element):
            if random.random() > self._hit_chance(actor, self.boss, skill):
                self.add_log("%s uses %s, but Matsuda slips it." % (actor.name, skill.name))
                self.set_fx("miss", "miss")
                self.emit_float("MISS", "miss", "boss")
                return "miss"

            affinity = self._boss_affinity(element)
            critical = random.random() < self._crit_chance(actor, self.boss, skill)
            damage = self._true_damage_amount(actor, skill, critical, affinity)
            self.boss.hp -= damage
            self.boss.clamp()
            self.emit_float(damage, ("crit" if critical else (affinity if affinity in ("weak", "resist") else "dmg")), "boss")

            prefix = "%s uses %s for %d true damage." % (actor.name, skill.name, damage)
            if affinity == "weak":
                prefix += " Weakness hit."
            elif affinity == "resist":
                prefix += " Matsuda resists."
            if critical:
                prefix += " Critical."
            self.add_log(prefix)
            self._track_phase_two_weakness_hit(element, affinity)
            if critical:
                self.set_fx("crit", "crit")
            elif affinity == "weak":
                self.set_fx("weak", "weak")
            elif affinity == "resist":
                self.set_fx("resist", "resist")
            else:
                self.set_fx("hit", "hit")
            return "critical" if critical else affinity

        def _damage_boss(self, actor, skill, element):
            if random.random() > self._hit_chance(actor, self.boss, skill):
                self.add_log("%s uses %s, but Matsuda slips it." % (actor.name, skill.name))
                self.set_fx("miss", "miss")
                self.emit_float("MISS", "miss", "boss")
                return "miss"

            affinity = self._boss_affinity(element)
            critical = random.random() < self._crit_chance(actor, self.boss, skill)
            damage = self._damage_amount(actor, self.boss, skill, element, critical, affinity)
            self.boss.hp -= damage
            self.boss.clamp()
            self.emit_float(damage, ("crit" if critical else (affinity if affinity in ("weak", "resist") else "dmg")), "boss")

            if skill.recoil > 0.0:
                recoil_damage = max(1, int(actor.max_hp * skill.recoil))
                actor.hp -= recoil_damage
                actor.clamp()
                try:
                    self.emit_float(recoil_damage, "enemy", self.party.index(actor))
                    if not actor.alive:
                        self.emit_death(self.party.index(actor))
                except ValueError:
                    pass

            prefix = "%s uses %s for %d damage." % (actor.name, skill.name, damage)
            if affinity == "weak":
                prefix += " Weakness hit."
            elif affinity == "resist":
                prefix += " Matsuda resists."
            if critical:
                prefix += " Critical."
            if skill.recoil > 0.0:
                prefix += " %s takes recoil." % actor.name
            self.add_log(prefix)
            self._track_phase_two_weakness_hit(element, affinity)
            if critical:
                self.set_fx("crit", "crit")
            elif affinity == "weak":
                self.set_fx("weak", "weak")
            elif affinity == "resist":
                self.set_fx("resist", "resist")
            else:
                self.set_fx("hit", "hit")
            return "critical" if critical else affinity

        def _track_player_element(self, element):
            if element in ("support", "healing", "almighty"):
                return
            self.player_element_history.append(element)
            if len(self.player_element_history) > 5:
                self.player_element_history = self.player_element_history[-5:]

        def _track_phase_two_weakness_hit(self, element, affinity):
            if self.phase not in (2, 3) or affinity != "weak":
                return
            self.phase2_player_weak_hits += 1
            if self.boss.adapt_turns > 0:
                return

            current_hits = self.phase2_weakness_hits.get(element, 0) + 1
            self.phase2_weakness_hits[element] = current_hits
            adapt_hits = MSBF_PHASE3_ADAPT_WEAK_HITS if self.phase == 3 else MSBF_PHASE2_ADAPT_WEAK_HITS
            if current_hits >= adapt_hits:
                self.phase2_weakness_hits[element] = 0
                self.boss.adapt_element = element
                self.boss.adapt_turns = 2
                if self.phase == 3:
                    self.add_log("Imago Rupta rejects the repeated %s script." % MSBF_AFFINITY_NAMES.get(element, element.title()))
                else:
                    self.add_log("Matsuda reads the repeated weakness and braces against %s." % MSBF_AFFINITY_NAMES.get(element, element.title()))

        def _boss_affinity(self, element):
            if element == "almighty":
                return "normal"
            if self.boss.adapt_element == element and self.boss.adapt_turns > 0:
                return "resist"
            if self.boss.guard and element in self.boss.weaknesses:
                return "normal"
            if element in self.boss.weaknesses:
                return "weak"
            if element in self.boss.resists:
                return "resist"
            return "normal"

        def _grant_player_bonus(self, reason):
            if not self.last_turn_bonus_converted:
                self.add_log("No full press turns remain, so the half-turn gets spent.")
                return
            if reason == "weak":
                self.add_log("The weakness hit converts the next full turn into a half turn.")
            else:
                self.add_log("The critical hit converts the next full turn into a half turn.")

        # ----- PHASE TRANSITIONS ---------------------------------------------
        # _configure_phase_* reshapes the fight when a bar breaks: phase 2 enables
        # shuffling/adapting affinities and restores the party; phase 3 ("Id Mode"
        # finale) sets the real boss HP, summons the full roster, swaps to the
        # layered vocal track, and unlocks the boss's phase3_* / shmup moves.
        # _handle_boss_bar_break / _handle_boss_phase_thresholds decide WHEN.
        def _configure_phase_two(self, restore_party=True):
            self.phase = 2
            self.boss.phase = 2
            self.boss.name = "Tohu Imago"
            self.boss.max_hp = 5200
            self.boss.hp = self.boss.max_hp
            self.boss.offense = 70
            self.boss.magic = 74
            self.boss.defense = 56
            self.boss.agility = 66
            self.boss.atk_stage = 0
            self.boss.def_stage = 0
            self.boss.agi_stage = 0
            self.boss.focus = True
            self.boss.guard = False
            self.boss.taunt = False
            self.boss.used_second_wind = False
            self.boss.adapt_element = None
            self.boss.adapt_turns = 0
            if restore_party:
                self._restore_party_for_phase_two()
            self._shuffle_phase_two_affinities(initial=True)
            self.phase2_ai_stance = "balanced"
            self.phase2_ai_last_announced_stance = "balanced"
            self.phase2_opening_immunity = True
            self.phase2_transition_reveal_started = False
            self._reset_phase_two_player_read()
            self.phase2_scan_insight_bag = []
            self.analyzed = False
            self.player_element_history = []
            self._settle_bars()

        def _begin_phase_two_transition(self):
            self._configure_phase_two(restore_party=True)
            self.phase_transition_title = "THE STAGE BEGINS ANEW"
            self.phase_transition_subtitle = "A WINGED ANGEL REWRITES THE SCRIPT"
            self.press_turn_icons_state = []
            self.enemy_press_turn_icons_state = []
            self.turn_phase = "phase_transition"
            self.phase_transition_delay = 0.12
            self._fade_out_phase_music()
            # 1.6s, not 3.4. The break is meant to be a thing that HAPPENS
            # to her; three and a half seconds of held black turned it into
            # a summoning circle. msbf_phase_break_seq is blowout, fracture,
            # and one held silence, and it is finished well inside this.
            self.set_fx("phase_blackout", "explode", 1.60)
            self.add_log("Matsuda's guard breaks. Light floods the battlefield.")
            self.add_log("The party steadies itself as HP and MP surge to full.")
            self.add_log("Her rhythm snaps into a new pattern. Olden ways are futile.")

        def _configure_phase_three(self):
            self.phase = 3
            self.phase3_started = True
            self.phase3_vocal_started = False
            self.phase3_vocal_genre_done = False
            self.phase3_last_microgame_enemy_action = -99
            self.phase3_microgame_cooldown = 0
            self.phase3_scan_insight_bag = []
            self.phase3_genre_shift_count = 0
            self.phase3_reinforcements_added = self._summon_full_roster_for_phase_three()
            self.boss.phase = 3
            self.boss.name = "Imago Rupta"
            # Superboss but fair (see TODO rebalance): 7600 HP is the ONE tuned
            # number and stays. Everything offensive was overtuned, so the stat
            # block, the free opening +1 attack stage, and the free charged Limit
            # Read were all cut back. Tweak these to redial phase-3 difficulty.
            self.boss.max_hp = 7600
            self.boss.hp = self.boss.max_hp
            self.boss.offense = 62
            self.boss.magic = 70
            self.boss.defense = 56
            self.boss.agility = 70
            self.boss.atk_stage = 0
            self.boss.def_stage = 0
            self.boss.agi_stage = 0
            self.boss.focus = False
            self.boss.guard = False
            self.boss.taunt = False
            self.boss.used_second_wind = True
            self.boss.adapt_element = None
            self.boss.adapt_turns = 0
            self._restore_party_for_phase_two()
            self._shuffle_phase_two_affinities(initial=True)
            self.phase2_ai_stance = "aggressive"
            self.phase2_ai_last_announced_stance = "aggressive"
            self.phase2_opening_immunity = True
            self.phase2_transition_reveal_started = False
            self._reset_phase_two_player_read()
            self.phase2_scan_insight_bag = []
            self.analyzed = False
            self.player_element_history = []
            self._settle_bars()

        def _begin_phase_three_transition(self):
            self._configure_phase_three()
            self.phase_transition_title = "IMAGO RUPTA"
            self.phase_transition_subtitle = "THE IMAGE RUPTURES AND THE SCRIPT CHANGES GENRE"
            self.press_turn_icons_state = []
            self.enemy_press_turn_icons_state = []
            self.clear_press_turn_fx()
            self.turn_phase = "phase_transition"
            self.phase_transition_delay = 0.10
            self._fade_out_phase_music()
            self.set_fx("phase_blackout", "explode", 1.70)
            self.add_log("Tohu Imago dies halfway through the sentence.")
            self.add_log("Matsuda grabs for another script. The image ruptures.")
            self.add_log("Imago Rupta enters Id Mode's final phase.")
            if self.phase3_reinforcements_added > 0:
                self.add_log("Every available ally forces their way onto the command deck.")

        def _handle_boss_phase_thresholds(self):
            if self.id_mode and self.phase == 2 and not self.phase3_started and self.boss.hp_ratio <= 0.50:
                self._begin_phase_three_transition()
                return True

            if self.id_mode and self.phase == 3 and not self.phase3_vocal_started and self.boss.hp > 0 and self.boss.hp_ratio <= 0.50:
                self.phase3_vocal_started = True
                self._crossfade_phase_three_vocal()
                self.add_log("Voices rupture even further.")
                self.set_fx("shuffle", "phase")

            return False

        def _handle_boss_bar_break(self):
            if self.phase == 1:
                self._begin_phase_two_transition()
            elif self.id_mode and self.phase == 2 and not self.phase3_started:
                self._begin_phase_three_transition()
            else:
                self.turn_phase = "victory_sequence"
                self.phase_transition_delay = 0.18
                self.press_turn_icons_state = []
                self.enemy_press_turn_icons_state = []
                self.clear_press_turn_fx()
                self._fade_out_phase_music()
                self.final_victory_whiteout = False
                self.final_victory_explode_played = False
                # No boom here -- the hypernova overlay plays "explode" on the
                # detonation beat, not on the quiet implosion build.
                self.set_fx("final_victory", None, MSBF_FINAL_VICTORY_RESULT_DELAY)
                self.add_log("The killing blow lands.")
                if self.phase == 3:
                    self.add_log("Imago Rupta fails to find another genre to hide in.")
                    self.add_log("Matsuda's last script shatters.")
                else:
                    self.add_log("Tohu Imago fractures under the impact.")
                    self.add_log("Matsuda's last guard shatters.")

        def _set_phase_one_affinities(self, index):
            weaknesses, resists = MSBF_PHASE1_AFFINITY_SETS[index]
            self.phase1_affinity_index = index
            self.boss.weaknesses = list(weaknesses)
            self.boss.resists = list(resists)

        def _draw_phase_one_affinity_index(self, avoid_index=None):
            if len(MSBF_PHASE1_AFFINITY_SETS) <= 1:
                return 0
            if not self.phase1_affinity_bag:
                self.phase1_affinity_bag = list(range(len(MSBF_PHASE1_AFFINITY_SETS)))
                random.shuffle(self.phase1_affinity_bag)
                if avoid_index is not None and self.phase1_affinity_bag[-1] == avoid_index:
                    self.phase1_affinity_bag.insert(0, self.phase1_affinity_bag.pop())
            return self.phase1_affinity_bag.pop()

        def _shuffle_phase_one_affinities(self):
            if self.phase != 1:
                return
            next_index = self._draw_phase_one_affinity_index(self.phase1_affinity_index)
            self._set_phase_one_affinities(next_index)
            self.analyzed = False
            self.set_fx("shuffle", "shuffle")
            self.add_log("Matsuda shuffles her guard. Scan will find the new opening.")

        def _phase_two_scan_insight(self):
            if self.phase == 3:
                if not getattr(self, "phase3_scan_insight_bag", None):
                    self.phase3_scan_insight_bag = [
                        "Moveset read: Imago Rupta carries fewer openings, more resists, and adapts after repeated weakness hits faster than Tohu Imago.",
                        "Moveset read: Imago Rupta upgrades the phase 2 spell line into Firaga, Blizzaga, Thundaga, and Aeroga.",
                        "Moveset read: The full roster can act in phase 3, but the command deck still has a hard tempo limit.",
                        "Moveset read: Black Box Waltz attacks the interface itself, burning MP and stripping stable buffs.",
                        "Moveset read: Reticle Nightmare marks a vulnerable target like a point-and-click escape room with no escape prompt.",
                        "Moveset read: Identity Null is almighty pressure. It gets worse when the party is over-buffed.",
                        "Moveset read: When this phase reaches half HP, her action economy tightens.",
                        "Moveset read: As it loses HP, Imago Rupta shifts genre in desperation.",
                        "Moveset read: Winning a genre shift only chips 3-5% of her CURRENT HP, so it can't finish her, but losing one costs the party. Play them to stall and bleed her.",
                    ]
                    random.shuffle(self.phase3_scan_insight_bag)
                return self.phase3_scan_insight_bag.pop()

            if self.boss.focus:
                return "Moveset read: Limit Read is active. Matsuda's next damaging move will spend the charge."

            if not self.boss.used_second_wind and self.boss.hp_ratio < 0.45:
                return "Moveset read: Second Wind is primed. Pushing her below 38% HP will trigger one heal and attack boost."

            if self.phase2_ai_stance == "defensive":
                return "Moveset read: She is countering burst with Null Aegis. Change tempo before hitting the same line again."

            if self.phase2_ai_stance == "aggressive":
                return "Moveset read: She is punishing the stall with heavier weakness checks and Redline Sweep pressure."

            if not getattr(self, "phase2_scan_insight_bag", None):
                alive = self.alive_party()
                exploitable = []
                for skill_id in ["boss_slash", "boss_pierce", "boss_fira", "boss_blizzara", "boss_thundara"]:
                    skill = MSBF_SKILLS[skill_id]
                    if any(skill.element in member.weaknesses and not member.guard for member in alive):
                        exploitable.append(skill.name)

                self.phase2_scan_insight_bag = [
                    "Moveset read: Her phase 2 kit includes Crosscut, Line Breaker, Fira, Blizzara, Thundara, Redline Sweep, Limit Read, Null Aegis, and one Second Wind.",
                    "Moveset read: Redline Sweep is wind magic that pressures the whole party when at least three allies are standing.",
                    "Moveset read: Limit Read is a setup turn. It charges her next damaging action instead of dealing damage immediately.",
                    "Moveset read: She checks unguarded weaknesses before choosing a target, then falls back to a mixed physical and spell pool.",
                    "Moveset read: Second Wind can happen once when her HP drops below 38%. It heals and raises her attack.",
                    "Moveset read: Her phase 2 affinities keep rotating behind the static: three weaknesses, three resists, one neutral.",
                    "Moveset read: Her weakness-read counter resets whenever her hidden affinities rewrite."
                ]
                if exploitable:
                    names = ", ".join(sorted(set(exploitable)))
                    self.phase2_scan_insight_bag.append("Moveset read: She can currently exploit unguarded party weaknesses with %s." % names)
                random.shuffle(self.phase2_scan_insight_bag)

            return self.phase2_scan_insight_bag.pop()

        # ----- ENEMY PHASE + BOSS AI -----------------------------------------
        # start_enemy_phase hands tempo to Matsuda; advance_enemy_phase steps one
        # boss action at a time (the screen ticks it). _choose_boss_skill /
        # _choose_phase_three_skill pick the move based on phase, the player's
        # recent behaviour (phase-2 stance read), and HP thresholds; _resolve_
        # enemy_skill applies it to the party.
        def start_enemy_phase(self):
            if self.result:
                return
            self.clear_press_turn_fx()
            if not self.alive_party():
                self._trigger_defeat()
                return

            # Healer-hunting keys off RECENT healing, not a lifetime counter: the
            # signal decays each enemy phase, so the boss eases off healers once
            # the party stops leaning on them (patch -- heal_actions used to latch).
            self.heal_actions = max(0, self.heal_actions - 1)

            if self.phase >= 2:
                self._update_phase_two_ai_stance()
                self.boss.guard = False
            else:
                self.phase2_ai_stance = "balanced"

            self.turn_phase = "enemy"
            self.press_turn_icons_state = []
            self.enemy_turns_remaining = 0
            self.enemy_bonus_remaining = 0
            if self.phase == 3:
                self.enemy_press_turn_icons_state = ["full", "full", "full"] if self.phase3_vocal_started else ["full", "full", "half"]
            else:
                self.enemy_press_turn_icons_state = ["full", "full"]
            self.enemy_actions_this_phase = 0
            if self.phase == 3:
                self.phase3_last_microgame_enemy_action = -99
                # Tick down the anti-streak cooldown: while >0, random genre shifts
                # are suppressed this phase, so they can't land in consecutive phases.
                if self.phase3_microgame_cooldown > 0:
                    self.phase3_microgame_cooldown -= 1
            # Phase-3 tempo trimmed from 5/4 -> 4/3: even at desperation the boss
            # tops out at 4 actions, so a stacked AoE turn can't wipe a healed party.
            self.enemy_action_cap = (4 if self.phase3_vocal_started else 3) if self.phase == 3 else 4
            self.enemy_settling = False
            # (No channel wipe here anymore -- SFX are pooled short one-shots that ring
            # out on their own; hard-stopping would defeat the point and clip the cue
            # that just played. The turn cue below simply lands on the next channel.)
            self.set_fx("enemy", "turn_ready")
            if self.phase == 3:
                self.add_log("Imago Rupta seizes the wheel.")
            else:
                self.add_log("Matsuda takes the initiative.")

        def advance_enemy_phase(self):
            if self.result or self.turn_phase != "enemy":
                return

            if not self.alive_party():
                self._trigger_defeat()
                renpy.restart_interaction()
                return

            if self.enemy_settling or not self._has_enemy_press_turns() or self.enemy_actions_this_phase >= self.enemy_action_cap:
                self._finish_enemy_phase()
                renpy.restart_interaction()
                return

            skill = self._choose_boss_skill()
            outcome = self._resolve_enemy_skill(skill)
            if self.microgame_active:
                renpy.restart_interaction()
                return
            self._sync_bars()
            self._apply_enemy_turn_cost(outcome)
            limit_reached = self._record_enemy_action()

            if not self.alive_party():
                self._trigger_defeat()
                renpy.restart_interaction()
                return

            if limit_reached and self._has_enemy_press_turns():
                self._force_enemy_phase_limit()

            if not self._has_enemy_press_turns():
                self.enemy_settling = True

            renpy.restart_interaction()

        def _finish_enemy_phase(self):
            self.enemy_press_turn_icons_state = []
            self.enemy_actions_this_phase = 0
            self.phase2_opening_immunity = False
            for member in self.party:
                member.guard = False
                member.taunt = False

            if not self.alive_party():
                self._trigger_defeat()
                return

            if self.phase == 1 and self.round_number % 2 == 0:
                self._shuffle_phase_one_affinities()
            elif self.phase == 2 and self.round_number - self.phase2_last_affinity_shift_round >= 2:
                self._shuffle_phase_two_affinities()
            elif self.phase == 3 and self.round_number - self.phase2_last_affinity_shift_round >= 1:
                self._shuffle_phase_two_affinities()
            self.begin_handover("player")

        def _choose_boss_skill(self):
            if self.phase == 3:
                return self._choose_phase_three_skill()

            if self.phase == 2 and not self.boss.used_second_wind and self.boss.hp_ratio < 0.38:
                self.boss.used_second_wind = True
                return MSBF_SKILLS["boss_second_wind"]

            stance = self.phase2_ai_stance if self.phase == 2 else "balanced"
            if self.phase == 2 and stance == "defensive":
                if self.enemy_actions_this_phase == 0 and not self.boss.guard and random.random() < 0.72:
                    return MSBF_SKILLS["boss_guard"]
                if not self.boss.focus and random.random() < 0.24:
                    return MSBF_SKILLS["boss_focus"]
            elif self.phase == 2 and stance == "aggressive":
                if not self.boss.focus and random.random() < 0.30:
                    return MSBF_SKILLS["boss_focus"]
            elif self.phase == 2 and not self.boss.focus and random.random() < 0.18:
                return MSBF_SKILLS["boss_focus"]

            alive = self.alive_party()
            sweep_chance = 0.08 if self.phase == 1 else 0.14
            if self.phase == 2 and stance == "aggressive":
                sweep_chance = 0.24
            elif self.phase == 2 and stance == "defensive":
                sweep_chance = 0.08
            if len(alive) >= 3 and random.random() < sweep_chance:
                return MSBF_SKILLS["boss_sweep"]

            exploitable = []
            for skill_id in ["boss_slash", "boss_pierce", "boss_fira", "boss_blizzara", "boss_thundara"]:
                skill = MSBF_SKILLS[skill_id]
                if any(skill.element in member.weaknesses and not member.guard for member in alive):
                    exploitable.append(skill)

            exploit_chance = 0.22 if self.phase == 1 else 0.32
            if self.phase == 2 and stance == "aggressive":
                exploit_chance = 0.52
            elif self.phase == 2 and stance == "defensive":
                exploit_chance = 0.24
            if exploitable and random.random() < exploit_chance:
                return random.choice(exploitable)

            pool = ["boss_slash", "boss_pierce", "boss_fira", "boss_blizzara", "boss_thundara"]
            return MSBF_SKILLS[random.choice(pool)]

        def _party_is_buffed(self):
            return any(
                (member.atk_stage > 0 or member.def_stage > 0 or member.agi_stage > 0)
                for member in self.alive_party()
            )

        def _phase_three_weakness_skills(self, alive):
            # The damaging moves whose element hits at least one standing, unguarded
            # party weakness right now -- so move choice and target choice agree.
            hits = []
            for skill_id in ("boss_slash", "boss_pierce", "boss_firaga", "boss_blizzaga", "boss_thundaga", "boss_aeroga"):
                skill = MSBF_SKILLS[skill_id]
                if any(skill.element in member.weaknesses and not member.guard for member in alive):
                    hits.append(skill)
            return hits

        def _phase_three_genre_shift_skill(self):
            # Desperation escalation: Imago Rupta flips genres more often the more
            # wounded it is, with one guaranteed shift on the vocal (<=50% HP) beat.
            # Considered on every boss action, but bounded three ways so shifts stay
            # common-yet-never-dominant (no coasting on winnable minigames): one per
            # enemy phase (guard 1), a cross-phase cooldown so they can't streak
            # (guard 2, see MSBF_PHASE3_MICROGAME_COOLDOWN), and the per-phase roll.
            shift_ids = ["boss_curtain_script", "boss_rewrite_order", "boss_multiple_choice"]
            # Guard 1: at most one shift per enemy phase.
            if self.phase3_last_microgame_enemy_action >= 0:
                return None
            # The guaranteed vocal-beat shift fires regardless of the cooldown, so
            # every run sees at least one; it then arms the cooldown like any other.
            if self.phase3_vocal_started and not self.phase3_vocal_genre_done:
                self.phase3_vocal_genre_done = True
                self.phase3_last_microgame_enemy_action = self.enemy_actions_this_phase
                self.phase3_microgame_cooldown = MSBF_PHASE3_MICROGAME_COOLDOWN
                return MSBF_SKILLS[random.choice(shift_ids)]
            # Guard 2: no random shift while cooling down from a recent one, so
            # shifts never streak across back-to-back enemy phases.
            if self.phase3_microgame_cooldown > 0:
                return None

            hp_missing = 1.0 - self.boss.hp_ratio
            chance = MSBF_PHASE3_MICROGAME_BASE_CHANCE + hp_missing * MSBF_PHASE3_MICROGAME_HP_SCALE
            if self.phase3_vocal_started:
                chance += MSBF_PHASE3_MICROGAME_VOCAL_BONUS
            if self.boss.hp_ratio <= 0.35:
                chance += MSBF_PHASE3_MICROGAME_LOW_HP_BONUS
            chance = min(MSBF_PHASE3_MICROGAME_CHANCE_CAP, max(0.0, chance))
            if random.random() < chance:
                self.phase3_last_microgame_enemy_action = self.enemy_actions_this_phase
                self.phase3_microgame_cooldown = MSBF_PHASE3_MICROGAME_COOLDOWN
                return MSBF_SKILLS[random.choice(shift_ids)]
            return None

        def _choose_phase_three_skill(self):
            alive = self.alive_party()
            stance = self.phase2_ai_stance
            weakness_skills = self._phase_three_weakness_skills(alive)

            # 1) Genre shift (microgame): desperation escalation.
            shift = self._phase_three_genre_shift_skill()
            if shift is not None:
                return shift

            # 2) Identity Null: almighty AoE that punishes over-buffing. Weighted up
            #    hard when the party is stacked with buffs, occasional otherwise.
            null_chance = 0.10
            if self._party_is_buffed():
                null_chance = 0.42 if self.phase3_vocal_started else 0.34
            elif self.phase3_vocal_started:
                null_chance = 0.16
            if self.boss.hp_ratio <= 0.55 and random.random() < null_chance:
                return MSBF_SKILLS["boss_identity_null"]

            # 3) Stance moves.
            if stance == "defensive":
                if self.enemy_actions_this_phase == 0 and not self.boss.guard and random.random() < 0.40:
                    return MSBF_SKILLS["boss_guard"]
                if random.random() < 0.30:
                    return MSBF_SKILLS["boss_black_box_waltz"]
            elif stance == "aggressive":
                # Limit Read with intent: only charge when there's a real payoff set
                # up (a standing weakness to convert next), not on a blind roll.
                if not self.boss.focus and weakness_skills and random.random() < 0.28:
                    return MSBF_SKILLS["boss_focus"]
                if random.random() < 0.30:
                    return MSBF_SKILLS["boss_reticle_nightmare"]

            # 4) Wide AoE when the command deck is crowded.
            if len(alive) >= 4 and random.random() < (0.26 if self.phase3_vocal_started else 0.16):
                return MSBF_SKILLS["boss_aeroga"]

            # 5) Exploit a standing weakness (coordinated with target selection).
            if weakness_skills and random.random() < (0.52 if self.phase3_vocal_started else 0.42):
                return random.choice(weakness_skills)

            # 6) Fallback mixed pool.
            pool = [
                "boss_slash",
                "boss_pierce",
                "boss_firaga",
                "boss_blizzaga",
                "boss_thundaga",
                "boss_aeroga",
                "boss_black_box_waltz",
                "boss_reticle_nightmare",
            ]
            return MSBF_SKILLS[random.choice(pool)]

        def _resolve_enemy_skill(self, skill):
            if skill.kind == "focus":
                self.boss.focus = True
                self.add_log("Matsuda uses Limit Read. Her next hit is charged.")
                self.set_fx("enemy_buff", "buff")
                return "normal"

            if skill.kind == "boss_guard":
                self.boss.guard = True
                if self.boss.def_stage < 2:
                    self.boss.def_stage += 1
                self.boss.clamp()
                self.add_log("Matsuda invokes Null Aegis. The next assault has to pierce a theorem.")
                self.set_fx("enemy_guard", "guard")
                return "normal"

            if skill.id == "boss_second_wind":
                heal_amount = 240 + (90 if self.phase == 2 else 0)
                old_hp = self.boss.hp
                self.boss.hp += heal_amount
                self.boss.atk_stage += 1
                self.boss.clamp()
                self.add_log("Matsuda catches a Second Wind and recovers %d HP." % heal_amount)
                self.set_fx("enemy_heal", "heal")
                self.emit_float(max(0, self.boss.hp - old_hp), "heal", "boss")
                return "normal"

            if skill.kind == "phase3_curtain":
                return self._resolve_phase_three_curtain(skill)

            if skill.kind == "phase3_typing":
                return self._resolve_phase_three_typing(skill)

            if skill.kind == "phase3_quiz":
                return self._resolve_phase_three_quiz(skill)

            if skill.kind == "phase3_black_box":
                return self._resolve_phase_three_black_box(skill)

            if skill.kind == "phase3_reticle":
                return self._resolve_phase_three_reticle(skill)

            if skill.kind == "phase3_null":
                return self._resolve_phase_three_null(skill)

            if skill.target == "all":
                best_outcome = "normal"
                total_damage = 0
                for member in list(self.alive_party()):
                    outcome, damage = self._damage_party_member(member, skill)
                    total_damage += damage
                    if outcome == "weak":
                        best_outcome = "weak"
                    elif outcome == "critical" and best_outcome != "weak":
                        best_outcome = "critical"
                self.add_log("Matsuda uses %s across the party for %d total damage." % (skill.name, total_damage))
                self.set_fx("enemy_aoe", "enemy")
                return best_outcome

            target = self._choose_enemy_target(skill)
            outcome, damage = self._damage_party_member(target, skill)
            self.last_enemy_target_id = target.id
            line = "Matsuda uses %s on %s for %d damage." % (skill.name, target.name, damage)
            if outcome == "weak":
                line += " Weakness hit."
            elif outcome == "resist":
                line += " %s resists." % target.name
            elif outcome == "critical":
                line += " Critical."
            elif outcome == "miss":
                line += " Miss."
            if not target.alive:
                line += " %s is down." % target.name
            self.add_log(line)
            if outcome == "weak":
                self.set_fx("enemy_weak", "weak")
            elif outcome == "critical":
                self.set_fx("enemy_crit", "crit")
            elif outcome == "resist":
                self.set_fx("enemy_resist", "resist")
            elif outcome == "miss":
                self.set_fx("miss", "miss")
            else:
                self.set_fx("enemy_hit", "enemy")
            return outcome

        # ----- PHASE-3 MICROGAME ("genre shift") SHARED WIN/LOSS -------------
        # All three genre-shift minigames (bullet-hell, typing QTE, quiz QTE) run
        # as overlays and settle through these helpers so the reward/penalty and
        # the turn-economy tail are identical. Win chips 3-5% of the boss's CURRENT
        # HP (never lethal); losses are non-lethal (floored at 1) so a microgame
        # can't directly wipe the party.
        def _microgame_win_chip(self):
            if self.boss.hp <= 1:
                return 0
            frac = random.uniform(MSBF_MICROGAME_WIN_CHIP_MIN, MSBF_MICROGAME_WIN_CHIP_MAX)
            old_hp = self.boss.hp
            self.boss.hp = max(1, self.boss.hp - max(1, int(self.boss.hp * frac)))
            dealt = old_hp - self.boss.hp
            if dealt > 0:
                self.emit_float(dealt, "dmg", "boss")
            return dealt

        def _microgame_chip_member(self, member, damage):
            old_hp = member.hp
            member.hp = max(1, member.hp - max(1, int(damage)))
            member.clamp()
            dealt = old_hp - member.hp
            if dealt > 0:
                try:
                    idx = self.party.index(member)
                except ValueError:
                    idx = "boss"
                self.emit_float(dealt, "enemy", idx)
            return dealt

        def _microgame_loss_single(self):
            alive = self.alive_party()
            if not alive:
                return None, 0
            target = random.choice(alive)
            dealt = self._microgame_chip_member(target, int(target.max_hp * MSBF_MICROGAME_LOSS_SINGLE))
            return target, dealt

        def _microgame_loss_party(self):
            total = 0
            for member in list(self.alive_party()):
                total += self._microgame_chip_member(member, int(member.max_hp * MSBF_MICROGAME_LOSS_PARTY))
            return total

        def _microgame_win_cue(self):
            # The reward flash for a won genre shift -- except the chip that
            # earned it can also carry the boss across a phase threshold, and
            # that handler sets its own, louder cue. Both land in the same frame
            # with nothing rendered between them, so whichever runs second just
            # overwrites the other and only one is ever seen. Let the threshold
            # win: run it first, and only flash if it stayed quiet. (Setting the
            # flash first and letting the handler clobber it worked by accident
            # and only in phase 3 -- from phase 2 the order was backwards and the
            # flash would have eaten the phase-three blackout.)
            before = self.fx_serial
            self._handle_boss_phase_thresholds()
            if self.fx_serial == before:
                self.set_fx("resist", "weak")

        def _finish_microgame_turn(self):
            # Shared tail: animate the bars, spend one normal boss action, record it
            # against the phase cap, guard against a wipe, then hand back to
            # advance_enemy_phase. Wins still chip HP and avoid the penalty, but do
            # not also burn extra enemy tempo like a resisted attack would -- which
            # is why this takes no outcome: the cost is "normal" either way. (It
            # used to accept one and ignore it, so the call sites read as though a
            # win cost the boss a resisted attack's tempo. It never did.)
            self._sync_bars()
            self._apply_enemy_turn_cost("normal")
            limit_reached = self._record_enemy_action()
            if not self.alive_party():
                self._trigger_defeat()
                renpy.restart_interaction()
                return
            if limit_reached and self._has_enemy_press_turns():
                self._force_enemy_phase_limit()
            if not self._has_enemy_press_turns():
                self.enemy_settling = True
            renpy.restart_interaction()

        def _resolve_phase_three_curtain(self, skill):
            self._start_phase_three_shmup(skill)
            return "minor"

        # ----- PHASE-3 SHMUP (bullet-hell dodge minigame) --------------------
        # When the boss casts "Curtain Script" in phase 3, the fight detours into
        # a real-time dodge segment. _start_phase_three_shmup arms it; the
        # MSBFShmupField displayable (ui.rpy) then steps the simulation on a
        # fixed 0.033s accumulator INSIDE its render() -- Kotonoha mode's 60fps
        # architecture; there is NO screen timer and NO per-tick interaction
        # restart any more. update_shmup_segment() spawns bullets via the named
        # _shmup_pattern_* casters, advances + collision-checks them, and ends
        # via finish_phase_three_shmup(success), whose _finish_microgame_turn
        # tail restarts the interaction ONCE to hand back to the battle screen.
        # Movement is polled per FRAME by the field (scaled to the frame delta),
        # so the ship moves at display fps while the danmaku stays deterministic
        # in the 30Hz tick.
        def _start_phase_three_shmup(self, skill):
            self.phase3_genre_shift_count += 1
            self.turn_phase = "shmup_segment"
            self.shmup_serial += 1
            self.shmup_tick = 0
            self.shmup_hits = 0
            self.shmup_invuln_until_tick = 0
            self.shmup_player_x = MSBF_SHMUP_STAGE_WIDTH // 2
            self.shmup_player_y = MSBF_SHMUP_STAGE_HEIGHT - 70
            self.shmup_bullets = []
            self.shmup_source_skill_id = skill.id
            self.shmup_sfx_cooldowns = {}
            self.shmup_focus = False
            self.shmup_poll_ok = False
            self.shmup_source_x = MSBF_SHMUP_STAGE_WIDTH * 0.5
            self.shmup_source_y = 62.0
            self.shmup_sparks = []
            self.shmup_hit_fx = []
            # One spell-card per cast, cycled in order so each is memorizable.
            self.shmup_pattern = MSBF_SHMUP_PATTERNS[(self.phase3_genre_shift_count - 1) % len(MSBF_SHMUP_PATTERNS)]
            card_name = MSBF_SHMUP_PATTERN_NAMES.get(self.shmup_pattern, "CURTAIN SCRIPT")
            self.add_log("Curtain Script declares “%s.” Read the source, weave the gaps." % card_name)
            self.set_fx("shuffle", "shuffle", 0.45)
            self._play_shmup_sfx("shmup_declare", 0, 0.55)

        @property
        def shmup_pattern_name(self):
            return MSBF_SHMUP_PATTERN_NAMES.get(getattr(self, "shmup_pattern", "spiral"), "CURTAIN SCRIPT")

        def shmup_nudge(self, dx, dy):
            # Fallback only: if live keyboard polling is working, ignore discrete
            # key-repeat nudges so movement stays smooth (no double-step).
            if not self.shmup_segment_active:
                return
            if getattr(self, "shmup_poll_ok", False):
                return
            radius = MSBF_SHMUP_PLAYER_RADIUS
            self.shmup_player_x = msbf_clamp(self.shmup_player_x + dx, radius, MSBF_SHMUP_STAGE_WIDTH - radius)
            self.shmup_player_y = msbf_clamp(self.shmup_player_y + dy, radius, MSBF_SHMUP_STAGE_HEIGHT - radius)
            self._check_shmup_collision()

        def _poll_shmup_movement(self, input_latch, scale=1.0):
            # Keyboard-only control: poll held WASD / arrow keys for smooth
            # continuous movement, with Shift to focus (precise, slow). Called
            # per FRAME by MSBFShmupField with scale = frame_dt / tick_dt, so a
            # held key covers the same px/sec as the old per-tick poll but the
            # motion itself runs at display framerate. The field owns and feeds
            # input_latch so transient SDL event state never enters battle saves.
            try:
                import pygame_sdl2 as _pg
                keys = _pg.key.get_pressed()
            except Exception:
                self.shmup_poll_ok = False
                return
            self.shmup_poll_ok = True

            # Another window owns the keyboard: rest the ship instead of
            # coasting on SDL's last sampled state.
            if not input_latch.focused():
                self.shmup_focus = False
                input_latch.clear()
                return

            dx = 0.0
            dy = 0.0
            if input_latch.pressed(keys, _pg.K_LEFT, _pg.K_a):
                dx -= 1.0
            if input_latch.pressed(keys, _pg.K_RIGHT, _pg.K_d):
                dx += 1.0
            if input_latch.pressed(keys, _pg.K_UP, _pg.K_w):
                dy -= 1.0
            if input_latch.pressed(keys, _pg.K_DOWN, _pg.K_s):
                dy += 1.0
            self.shmup_focus = input_latch.pressed(
                keys,
                _pg.K_LSHIFT,
                _pg.K_RSHIFT,
            )
            if dx == 0.0 and dy == 0.0:
                return
            if dx != 0.0 and dy != 0.0:
                dx *= 0.70710678
                dy *= 0.70710678
            speed = (MSBF_SHMUP_FOCUS_SPEED if self.shmup_focus else MSBF_SHMUP_MOVE_SPEED) * scale
            radius = MSBF_SHMUP_PLAYER_RADIUS
            self.shmup_player_x = msbf_clamp(self.shmup_player_x + dx * speed, radius, MSBF_SHMUP_STAGE_WIDTH - radius)
            self.shmup_player_y = msbf_clamp(self.shmup_player_y + dy * speed, radius, MSBF_SHMUP_STAGE_HEIGHT - radius)

        def update_shmup_segment(self):
            # One fixed 0.033s simulation tick. Driven by MSBFShmupField's
            # render-side accumulator; deliberately does NOT restart the
            # interaction (the field self-redraws every frame).
            if not self.shmup_segment_active:
                return

            self.shmup_tick += 1
            self._spawn_shmup_bullets()
            self._advance_shmup_bullets()
            self._advance_shmup_sparks()

            if self._check_shmup_collision():
                return

            if self.shmup_tick >= MSBF_SHMUP_DURATION_TICKS:
                self.finish_phase_three_shmup(True)
                return

        def _play_shmup_sfx(self, sfx_name, min_interval=6, volume=0.42):
            path = MSBF_SFX.get(sfx_name)
            if not path:
                return
            last_tick = self.shmup_sfx_cooldowns.get(sfx_name, -999)
            if self.shmup_tick - last_tick < min_interval:
                return
            self.shmup_sfx_cooldowns[sfx_name] = self.shmup_tick
            # Pooled so rapid danmaku cues (a shot, then a hit, then a burst) overlap
            # instead of each new one silencing the last.
            msbf_play_pooled_sfx(path, volume)

        def _add_shmup_bullet(self, x, y, vx, vy, size=10, color="#ff3868dd", shape="orb", sway=0.0, phase=0.0, ax=0.0, ay=0.0, ttl=None):
            rot = 0.0
            if shape == "needle":
                rot = math.degrees(math.atan2(vy, vx)) + 90.0
            self.shmup_bullets.append({
                "x": float(x),
                "y": float(y),
                "vx": float(vx),
                "vy": float(vy),
                "size": int(size),
                "color": color,
                "shape": shape,
                "sway": float(sway),
                "phase": float(phase),
                "rot": rot,
                "age": 0,
                "ax": float(ax),
                "ay": float(ay),
                "ttl": ttl,
            })

        def _add_shmup_sparks(self, x, y, n, color, spd=3.4, ttl=26):
            # Cosmetic burst (hit feedback). Capped so a bad frame can't flood
            # the renderer; sparks are advanced with the sim tick.
            sparks = self._own_list("shmup_sparks")
            room = MSBF_SHMUP_MAX_SPARKS - len(sparks)
            for i in range(min(n, max(0, room))):
                a = (math.pi * 2.0 * i / max(1, n)) + (self.shmup_tick * 0.17)
                s = spd * (0.55 + 0.45 * ((i * 7) % 3) / 2.0)
                sparks.append({
                    "x": float(x), "y": float(y),
                    "vx": math.cos(a) * s, "vy": math.sin(a) * s,
                    "age": 0, "ttl": int(ttl), "color": color,
                })

        def _advance_shmup_sparks(self):
            if not self.shmup_sparks:
                return
            kept = []
            for s in self.shmup_sparks:
                s["age"] += 1
                if s["age"] > s["ttl"]:
                    continue
                s["x"] += s["vx"]
                s["y"] += s["vy"]
                s["vx"] *= 0.95
                s["vy"] = s["vy"] * 0.95 + 0.06
                kept.append(s)
            self.shmup_sparks = kept

        def _add_shmup_radial_burst(self, x, y, count, speed, offset, color, size=9, shape="orb", sway=0.0):
            # FULL rings only. This used to take gap_every/gap_shift and skip
            # those spokes, which cut a safe pocket into every ring. Rings are
            # exactly the case the house rule names: a circle spawns closed,
            # because the dodge is already there for free -- neighbouring spokes
            # spread apart as the radius grows. Difficulty comes from density,
            # speed and layering. (Falling WALLS keep their travelling gap: a
            # full-width wall has to be passable by something. See
            # _shmup_pattern_walls.)
            for idx in range(count):
                angle = offset + (math.pi * 2.0 * idx / float(count))
                self._add_shmup_bullet(
                    x,
                    y,
                    math.cos(angle) * speed,
                    math.sin(angle) * speed,
                    size,
                    color,
                    shape,
                    sway,
                    idx * 0.37
                )

        def _shmup_source(self):
            # A single emitter drifting along a pure sine of the tick near the top
            # of the stage. Deterministic, so the "bullet source" is readable and
            # every card plays out identically each cast -- memorizable danmaku.
            cx = MSBF_SHMUP_STAGE_WIDTH * 0.5 + math.sin(self.shmup_tick * 0.030) * (MSBF_SHMUP_STAGE_WIDTH * 0.28)
            cy = 60.0
            self.shmup_source_x = cx
            self.shmup_source_y = cy
            return cx, cy

        def _shmup_aim(self, cx, cy):
            # Angle from the emitter toward the player (for aimed shots).
            return math.atan2(self.shmup_player_y - cy, self.shmup_player_x - cx)

        def _spawn_shmup_bullets(self):
            # One clean card per cast (cycled). Each ramps density past the midpoint
            # so the opening is readable and the back half is the real test.
            tick = self.shmup_tick
            cx, cy = self._shmup_source()
            pattern = getattr(self, "shmup_pattern", "spiral")
            if pattern == "aimed":
                self._shmup_pattern_aimed(tick, cx, cy)
            elif pattern == "walls":
                self._shmup_pattern_walls(tick, cx, cy)
            else:
                self._shmup_pattern_spiral(tick, cx, cy)

        # Arm palette shared by the spiral card.
        _SHMUP_SPIRAL_COLORS = ["#ff3868dd", "#55ddffdd", "#ffcf66dd", "#a66bffdd", "#f5fbffee"]

        def _shmup_pattern_spiral(self, tick, cx, cy):
            # SPIRAL SCRIPTURE: a slowly rotating multi-arm spiral (4 arms, 5 past
            # the midpoint) laid over periodic FULL rings. You dodge the spiral by
            # reading its rotation and the rings by sitting between their spokes;
            # neither has a door cut into it.
            if tick % 3 == 0:
                arms = 4 if tick < msbf_shmup_gate(0.50) else 5
                base = (tick // 3) * 0.28
                for arm in range(arms):
                    ang = base + arm * (2.0 * math.pi / arms)
                    color = self._SHMUP_SPIRAL_COLORS[arm % len(self._SHMUP_SPIRAL_COLORS)]
                    self._add_shmup_bullet(cx, cy, math.cos(ang) * 3.4, math.sin(ang) * 3.4, 9, color, "orb", 0.0, arm * 1.3)
                self._play_shmup_sfx("shmup_shot", 6, 0.8)
            if tick >= msbf_shmup_gate(0.30) and tick % 44 == 0:
                self._add_shmup_radial_burst(cx, cy, 26, 2.8, tick * 0.06, "#a66bffdd", 9, shape="orb")
                self._play_shmup_sfx("shmup_burst", 12, 0.8)

        def _shmup_pattern_aimed(self, tick, cx, cy):
            # REVISION SALVO: aimed needle fans force streaming and cutbacks; a
            # slow wobbling orb stream keeps the field honest between fans; full
            # rings layer in past the midpoint to shrink the room you stream into.
            if tick >= 10 and tick % 14 == 0:
                ang = self._shmup_aim(cx, cy)
                spread = 5 if tick < msbf_shmup_gate(0.55) else 7
                for i in range(spread):
                    off = (i - (spread - 1) / 2.0) * 0.14
                    self._add_shmup_bullet(cx, cy, math.cos(ang + off) * 5.0, math.sin(ang + off) * 5.0, 8, "#f5fbffea", "needle", 0.0, off * 8.0)
                self._play_shmup_sfx("shmup_shot", 8, 0.8)
            if tick % 6 == 3:
                ang = self._shmup_aim(cx, cy) + (0.10 if (tick // 30) % 2 == 0 else -0.10)
                self._add_shmup_bullet(cx, cy, math.cos(ang) * 3.6, math.sin(ang) * 3.6, 8, "#55ddffdd", "orb", 0.0, (tick // 6) * 0.4)
            if tick >= msbf_shmup_gate(0.55) and tick % 48 == 24:
                self._add_shmup_radial_burst(cx, cy, 24, 2.6, tick * 0.05, "#ff6b9fdd", 8, shape="orb")
                self._play_shmup_sfx("shmup_burst", 12, 0.8)

        def _shmup_pattern_walls(self, tick, cx, cy):
            # MARGIN COLLAPSE: descending walls with a 2-wide gap that slides along
            # a deterministic sine path, plus aimed needle triplets so the player
            # can't just camp the moving gap.
            #
            # The gap is deliberate and stays. The no-authored-gaps rule is about
            # RINGS -- a full-width falling wall has to be passable by something,
            # and a window that travels is the sanctioned exception. It is also
            # measurably not campable: simulated with the needles honestly
            # tracking a stationary player, every one of 180 candidate camp spots
            # is clipped inside one cast. Escalation is speed and cadence, which
            # is what the rule asks for.
            interval = 10 if tick < msbf_shmup_gate(0.50) else 8
            if tick % interval == 0:
                lanes = 15
                step = float(MSBF_SHMUP_STAGE_WIDTH) / float(lanes)
                gap = int((math.sin((tick // interval) * 0.5) * 0.5 + 0.5) * (lanes - 4)) + 1
                speed = 4.8 if tick < msbf_shmup_gate(0.50) else 5.4
                for lane in range(lanes):
                    if lane == gap or lane == gap + 1:
                        continue
                    self._add_shmup_bullet(step * (lane + 0.5), -14, 0.0, speed, 9, "#ff3868dd", "orb", 0.0, lane)
                self._play_shmup_sfx("shmup_shot", 8, 0.8)
            if tick >= msbf_shmup_gate(0.35) and tick % 22 == 11:
                ang = self._shmup_aim(cx, cy)
                for off in (-0.10, 0.0, 0.10):
                    self._add_shmup_bullet(cx, cy, math.cos(ang + off) * 4.6, math.sin(ang + off) * 4.6, 8, "#ffcf66ee", "needle", 0.0, off * 6.0)
                self._play_shmup_sfx("shmup_burst", 10, 0.8)

        def _advance_shmup_bullets(self):
            updated = []
            margin = 64
            for bullet in self.shmup_bullets:
                age = bullet.get("age", 0) + 1
                bullet["age"] = age
                ttl = bullet.get("ttl", None)
                if ttl is not None and age > ttl:
                    continue
                sway = bullet.get("sway", 0.0)
                phase = bullet.get("phase", 0.0)
                bullet["vx"] += bullet.get("ax", 0.0)
                bullet["vy"] += bullet.get("ay", 0.0)
                bullet["x"] += bullet.get("vx", 0.0) + math.sin((age + phase) * 0.20) * sway
                bullet["y"] += bullet.get("vy", 0.0)
                if bullet.get("shape") == "needle":
                    bullet["rot"] = math.degrees(math.atan2(bullet.get("vy", 0.0), bullet.get("vx", 0.0))) + 90.0
                if -margin <= bullet["x"] <= MSBF_SHMUP_STAGE_WIDTH + margin and -margin <= bullet["y"] <= MSBF_SHMUP_STAGE_HEIGHT + margin:
                    updated.append(bullet)
            # Overflow sheds the NEWEST spawns, not the oldest. Bullets are stored
            # in spawn order and every card emits from the top of the stage, so
            # the head of the list is the wave that has travelled furthest down --
            # i.e. the one the player is currently threading. Slicing the tail off
            # the front would delete pellets out of the air in front of the ship
            # while freshly spawned ones up at the emitter survive.
            self.shmup_bullets = updated[:MSBF_SHMUP_MAX_BULLETS]

        def _check_shmup_collision(self):
            if not self.shmup_segment_active:
                return False
            if self.shmup_tick < MSBF_SHMUP_GRACE_TICKS:
                return False
            if self.shmup_tick < getattr(self, "shmup_invuln_until_tick", 0):
                return False
            player_radius = MSBF_SHMUP_PLAYER_RADIUS
            for index, bullet in enumerate(self.shmup_bullets):
                bullet_radius = bullet.get("size", 10) * (0.34 if bullet.get("shape") == "needle" else 0.42)
                dx = bullet.get("x", 0) - self.shmup_player_x
                dy = bullet.get("y", 0) - self.shmup_player_y
                hit_radius = player_radius + bullet_radius
                if dx * dx + dy * dy <= hit_radius * hit_radius:
                    # Undertale/Deltarune style: only the pellet that clipped you is
                    # consumed; the rest of the pattern stays on screen and the
                    # iframes (with the flickering marker) cover the recovery.
                    del self.shmup_bullets[index]
                    return self._register_shmup_hit()
            return False

        def _register_shmup_hit(self):
            self.shmup_hits += 1
            self._play_shmup_sfx("shmup_hit", 0, 0.9)
            # Clip feedback: spark burst + an expanding ring at the impact spot
            # (drawn by MSBFShmupField via the msbf.ring shader).
            hit_fx = self._own_list("shmup_hit_fx")
            hit_fx.append({
                "x": self.shmup_player_x, "y": self.shmup_player_y,
                "tick": self.shmup_tick,
            })
            if len(hit_fx) > 3:
                del hit_fx[0]
            self._add_shmup_sparks(self.shmup_player_x, self.shmup_player_y, 14, "#ff5c7a", 4.0, 30)
            self._add_shmup_sparks(self.shmup_player_x, self.shmup_player_y, 8, "#f5fbff", 2.6, 24)

            if self.shmup_hits >= MSBF_SHMUP_HIT_LIMIT:
                self.finish_phase_three_shmup(False)
                return True

            # No panic-clear of nearby bullets anymore -- just invulnerability frames.
            # The player marker flickers on/off while they last (see msbf_shmup_overlay)
            # so the hit reads clearly and you get a fair window to reposition.
            self.shmup_invuln_until_tick = self.shmup_tick + MSBF_SHMUP_HIT_INVULN_TICKS
            self.add_log("Curtain Script clips the hitbox (%d/%d)." % (self.shmup_hits, MSBF_SHMUP_HIT_LIMIT))
            return False

        def finish_phase_three_shmup(self, success):
            if not self.shmup_segment_active:
                return

            self.shmup_bullets = []
            self.shmup_sparks = []
            self.shmup_hit_fx = []
            self.turn_phase = "enemy"

            if success:
                # Survived the cast -> chip the boss (never lethal). Fewer clips is
                # its own reward via the hit limit; the chip itself is the flat 3-5%.
                dealt = self._microgame_win_chip()
                if self.shmup_hits:
                    self.add_log("The party escapes Curtain Script (%d clip(s)). Imago Rupta buckles for %d." % (self.shmup_hits, dealt))
                else:
                    self.add_log("The party threads Curtain Script clean. Imago Rupta buckles for %d." % dealt)
                self._play_shmup_sfx("shmup_clear", 0, 0.56)
                msbf_record_micro_win("shmup")
                self._microgame_win_cue()
            else:
                # Bullet-hell is a party-wide game: 7% off every member (non-lethal).
                total = self._microgame_loss_party()
                self.add_log("Curtain Script overruns the hitbox. Identity Null splashes the whole party for %d." % total)
                self._play_shmup_sfx("shmup_fail", 0, 0.60)
                self.set_fx("enemy_aoe", "enemy")

            self._finish_microgame_turn()

        # ----- PHASE-3 TYPING QTE ("Rewrite Order") --------------------------
        # The script demands a word; type it before the timer drains. Win chips
        # the boss; timing out is a single-target loss (30% of one member).
        def _resolve_phase_three_typing(self, skill):
            self._start_phase_three_typing(skill)
            return "minor"

        def _start_phase_three_typing(self, skill):
            self.phase3_genre_shift_count += 1
            self.turn_phase = "typing_segment"
            self.typing_serial += 1
            self.typing_input = ""
            self.typing_word = random.choice(MSBF_TYPING_WORDS)
            self.typing_time_limit = max(MSBF_TYPING_TIME_MIN, MSBF_TYPING_TIME_BASE + len(self.typing_word) * MSBF_TYPING_TIME_PER_CHAR)
            self.add_log("Rewrite Order: the script demands the word “%s.” Type it before the ink dries." % self.typing_word)
            self.set_fx("shuffle", "debuff", 0.5)
            self._play_sfx("scan")

        def finish_phase_three_typing(self, success):
            if not self.typing_segment_active:
                return
            self.turn_phase = "enemy"
            if success:
                dealt = self._microgame_win_chip()
                self.add_log("The party types it back clean. The script recoils -- Imago Rupta buckles for %d." % dealt)
                msbf_record_micro_win("typing")
                self._microgame_win_cue()
            else:
                target, dealt = self._microgame_loss_single()
                if target is not None:
                    self.add_log("The ink dries first. The unfinished sentence redacts %s for %d." % (target.name, dealt))
                self.set_fx("enemy_crit", "crit")
            self._finish_microgame_turn()

        # ----- PHASE-3 QUIZ QTE ("Multiple Choice Interrupt") ----------------
        # Pick the correct answer before the timer runs out. Win chips the boss;
        # a wrong answer or timeout is a party-wide loss (7% off everyone).
        def _resolve_phase_three_quiz(self, skill):
            self._start_phase_three_quiz(skill)
            return "minor"

        def _start_phase_three_quiz(self, skill):
            self.phase3_genre_shift_count += 1
            self.turn_phase = "quiz_segment"
            self.quiz_serial += 1
            entry = random.choice(MSBF_QUIZ_BANK)
            options = [(entry["correct"], True)] + [(text, False) for text in entry["wrong"]]
            random.shuffle(options)
            self.quiz_prompt = entry["q"]
            self.quiz_options = options
            self.quiz_cursor = 0
            self.quiz_time_limit = MSBF_QUIZ_TIME_LIMIT
            self.add_log("Multiple Choice Interrupt: “%s” Answer before the timer runs out." % entry["q"])
            self.set_fx("shuffle", "scan", 0.5)
            self._play_sfx("scan")

        def quiz_move(self, delta):
            # Keyboard cursor over the quiz options (state on the battle object so
            # it survives the used-overlay screen-scope issue).
            if not self.quiz_segment_active or not self.quiz_options:
                return
            self.quiz_cursor = (self.quiz_cursor + delta) % len(self.quiz_options)
            renpy.restart_interaction()

        def quiz_confirm(self):
            if not self.quiz_segment_active or not self.quiz_options:
                return
            idx = max(0, min(self.quiz_cursor, len(self.quiz_options) - 1))
            self.answer_phase_three_quiz(self.quiz_options[idx][1])

        def answer_phase_three_quiz(self, is_correct):
            self.finish_phase_three_quiz(bool(is_correct))

        def finish_phase_three_quiz(self, success):
            if not self.quiz_segment_active:
                return
            self.turn_phase = "enemy"
            if success:
                dealt = self._microgame_win_chip()
                self.add_log("Correct read. The genre collapses back on itself -- Imago Rupta buckles for %d." % dealt)
                msbf_record_micro_win("quiz")
                self._microgame_win_cue()
            else:
                total = self._microgame_loss_party()
                self.add_log("Wrong answer. The script rewrites the whole party for %d." % total)
                self.set_fx("enemy_aoe", "enemy")
            self._finish_microgame_turn()

        def _resolve_phase_three_black_box(self, skill):
            self.phase3_genre_shift_count += 1
            best_outcome = "normal"
            total_damage = 0
            mp_burn = 0
            for member in list(self.alive_party()):
                outcome, damage = self._damage_party_member(member, skill)
                total_damage += damage
                if member.mp > 0:
                    burn = max(3, int(member.max_mp * (0.10 if member.guard else 0.18)))
                    old_mp = member.mp
                    member.mp = max(0, member.mp - burn)
                    mp_burn += old_mp - member.mp
                if member.atk_stage > 0:
                    member.atk_stage -= 1
                if member.def_stage > 0 and not member.guard:
                    member.def_stage -= 1
                if member.agi_stage > 0 and not member.guard:
                    member.agi_stage -= 1
                member.clamp()
                if outcome == "weak":
                    best_outcome = "weak"
                elif outcome == "critical" and best_outcome != "weak":
                    best_outcome = "critical"
            self.add_log("Black Box Waltz corrupts the command deck for %d damage and %d MP." % (total_damage, mp_burn))
            self.set_fx("enemy_aoe", "debuff")
            return best_outcome

        def _resolve_phase_three_reticle(self, skill):
            self.phase3_genre_shift_count += 1
            alive = self.alive_party()
            if not alive:
                return "normal"

            healers = [member for member in alive if "cure" in member.skill_ids or "medica" in member.skill_ids or "white_wind" in member.skill_ids or "raise" in member.skill_ids]
            if healers and random.random() < 0.55:
                target = min(healers, key=lambda member: member.hp_ratio)
            else:
                target = min(alive, key=lambda member: member.hp_ratio)

            outcome, damage = self._damage_party_member(target, skill)
            if target.alive and not target.guard:
                target.def_stage -= 1
                target.agi_stage -= 1
                target.clamp()
            self.last_enemy_target_id = target.id

            line = "Reticle Nightmare paints %s for %d damage." % (target.name, damage)
            if outcome == "weak":
                line += " Weakness hit."
            elif outcome == "critical":
                line += " Critical."
            elif outcome == "miss":
                line += " Miss."
            if not target.alive:
                line += " %s is down." % target.name
            self.add_log(line)
            if outcome == "critical":
                self.set_fx("enemy_crit", "crit")
            elif outcome == "weak":
                self.set_fx("enemy_weak", "weak")
            elif outcome == "miss":
                self.set_fx("miss", "miss")
            else:
                self.set_fx("enemy_hit", "enemy")
            return outcome

        def _resolve_phase_three_null(self, skill):
            self.phase3_genre_shift_count += 1
            total_damage = 0
            buffed_members = 0
            for member in list(self.alive_party()):
                buff_bonus = max(0, member.atk_stage) + max(0, member.def_stage) + max(0, member.agi_stage)
                if buff_bonus > 0:
                    buffed_members += 1
                # Rebalanced from power 76 / magic*0.82 / buff*28. Still an
                # almighty AoE that punishes over-buffing, but no longer a party
                # delete -- it must stay survivable across a ~4-action phase.
                damage = max(1, int(skill.power + self.boss.magic * 0.52 + buff_bonus * 14))
                if member.guard:
                    damage = int(damage * 0.62)
                applied_damage = self._apply_enemy_damage_to_member(member, damage)
                member.atk_stage = min(0, member.atk_stage)
                member.def_stage = min(0, member.def_stage)
                member.agi_stage = min(0, member.agi_stage)
                member.clamp()
                total_damage += applied_damage
            self.add_log("Identity Null burns the role labels off %d allies for %d total damage." % (buffed_members, total_damage))
            self.set_fx("enemy_aoe", "enemy")
            return "normal"

        def _choose_enemy_target(self, skill):
            alive = self.alive_party()
            stance = self.phase2_ai_stance if self.phase >= 2 else "balanced"
            taunters = [member for member in alive if member.taunt]
            if taunters and random.random() < (0.56 if self.phase == 3 else 0.70):
                return self._weighted_enemy_target(taunters)

            # Secure-but-fair kills: with a member already on the ropes (and not
            # guarding), sometimes press the advantage instead of spreading damage.
            # Capped so the boss can't tunnel one member every single action.
            finishers = [member for member in alive if member.hp_ratio < 0.20 and not member.guard]
            if finishers:
                finish_chance = 0.34 if stance == "aggressive" else 0.22
                if self.phase == 3:
                    finish_chance += 0.06
                if random.random() < finish_chance:
                    return min(finishers, key=lambda member: member.hp)

            if self.heal_actions >= 2:
                healers = [member for member in alive if "cure" in member.skill_ids or "medica" in member.skill_ids or "white_wind" in member.skill_ids or "raise" in member.skill_ids]
                healer_chance = 0.16
                if stance == "aggressive":
                    healer_chance = 0.36 if self.phase == 3 else 0.28
                elif stance == "defensive":
                    healer_chance = 0.12
                if healers and random.random() < healer_chance:
                    return self._weighted_enemy_target(healers)

            weak_targets = [member for member in alive if skill.element in member.weaknesses and not member.guard]
            weak_target_chance = 0.22 if self.phase == 1 else (0.30 if self.phase == 3 else 0.32)
            if stance == "aggressive":
                weak_target_chance = 0.42 if self.phase == 3 else 0.50
            elif stance == "defensive":
                weak_target_chance = 0.22 if self.phase == 3 else 0.22
            if weak_targets and random.random() < weak_target_chance:
                return self._weighted_enemy_target(weak_targets)

            lowest_hp_chance = 0.20 if self.phase == 3 else 0.18
            if stance == "aggressive":
                lowest_hp_chance = 0.28 if self.phase == 3 else 0.26
            elif stance == "defensive":
                lowest_hp_chance = 0.14 if self.phase == 3 else 0.12
            if random.random() < lowest_hp_chance:
                return min(alive, key=lambda member: member.hp_ratio)
            return self._weighted_enemy_target(alive)

        def _weighted_enemy_target(self, candidates):
            weighted = []
            for member in candidates:
                weight = 5 if member.row == "front" else 2
                if member.id == self.last_enemy_target_id and len(candidates) > 1:
                    weight = max(1, weight - 3)
                if member.hp_ratio < 0.30:
                    weight = max(1, weight - 2)
                for _i in range(weight):
                    weighted.append(member)
            if not weighted:
                return random.choice(candidates)
            return random.choice(weighted)

        def _damage_party_member(self, target, skill):
            if random.random() > self._hit_chance(self.boss, target, skill):
                return "miss", 0

            affinity = self._target_affinity(target, skill.element)
            critical = random.random() < self._crit_chance(self.boss, target, skill)
            damage = self._damage_amount(self.boss, target, skill, skill.element, critical, affinity)
            applied_damage = self._apply_enemy_damage_to_member(target, damage)
            return ("critical" if critical else affinity), applied_damage

        def _target_affinity(self, target, element):
            if target.guard and element in target.weaknesses:
                return "normal"
            if element in target.weaknesses:
                return "weak"
            if element in target.resists:
                return "resist"
            return "normal"

        def _actual_element(self, actor, skill):
            if skill.element == "weapon":
                return actor.attack_element
            return skill.element

        def _hit_chance(self, attacker, target, skill):
            chance = skill.accuracy + ((attacker.agility + attacker.agi_stage * 8) - (target.agility + target.agi_stage * 8)) * 0.0025
            if target.guard:
                chance -= 0.02
            return max(0.55, min(0.99, chance))

        def _crit_chance(self, attacker, target, skill):
            chance = skill.crit + max(0, attacker.agility - target.agility) * 0.0015
            if attacker.focus:
                chance += 0.06
            return max(0.0, min(0.45, chance))

        def _damage_amount(self, attacker, target, skill, element, critical, affinity):
            source = attacker.magic if skill.stat == "magic" else attacker.offense
            if attacker.id == "matsuda":
                if self.phase == 3:
                    # Rebalanced down from 1.08 / 1.50 / 22.0 -- phase 3 was
                    # deleting squishies in a single hit. Superboss-but-fair.
                    base = skill.power + source * 0.86 - target.defense * 0.62
                    damage_ceiling = 1.42
                    damage_floor = 18.0
                else:
                    base = skill.power + source * 1.28 - target.defense * 0.58
                    damage_ceiling = 1.70
                    damage_floor = 20.0
            else:
                base = skill.power * 0.92 + source * 1.18 - target.defense * 0.62
                damage_ceiling = 1.95
                damage_floor = 28.0
            base = max(damage_floor, base)

            stage_mult = max(0.58, 1.0 + attacker.atk_stage * 0.14 - target.def_stage * 0.12)
            damage_mult = stage_mult
            if attacker.focus:
                damage_mult *= 1.20 if attacker.id == "matsuda" else 1.32
                attacker.focus = False
            if affinity == "weak":
                damage_mult *= 1.14 if attacker.id == "matsuda" else 1.18
            elif affinity == "resist":
                damage_mult *= 0.55
            if critical:
                damage_mult *= 1.18 if attacker.id == "matsuda" else 1.25
            if target.guard:
                damage_mult *= 0.55
            if attacker.id == "matsuda" and target.row == "rear":
                if element in ("slash", "pierce"):
                    damage_mult *= 0.76
                else:
                    damage_mult *= 0.88
            damage_mult = msbf_clamp(damage_mult, 0.25, damage_ceiling)
            variance = msbf_gaussian_variance(
                MSBF_DAMAGE_VARIANCE_STDEV,
                MSBF_DAMAGE_VARIANCE_MIN,
                MSBF_DAMAGE_VARIANCE_MAX
            )
            return max(1, int(round(base * damage_mult * variance)))

        def _true_damage_amount(self, actor, skill, critical, affinity):
            source = actor.magic if skill.stat == "magic" else actor.offense
            base = max(1.0, skill.power + source * 0.72)
            damage_mult = max(0.72, 1.0 + actor.atk_stage * 0.12)
            if actor.focus:
                damage_mult *= 1.24
                actor.focus = False
            if affinity == "weak":
                damage_mult *= 1.18
            elif affinity == "resist":
                damage_mult *= 0.55
            if critical:
                damage_mult *= 1.18
            if self.boss.guard:
                damage_mult *= 0.72
            variance = msbf_gaussian_variance(
                MSBF_DAMAGE_VARIANCE_STDEV,
                MSBF_DAMAGE_VARIANCE_MIN,
                MSBF_DAMAGE_VARIANCE_MAX
            )
            return max(1, int(round(base * damage_mult * variance)))

        def _healing_amount(self, actor, skill):
            base = skill.power + actor.magic * 1.15
            variance = msbf_gaussian_variance(
                MSBF_HEAL_VARIANCE_STDEV,
                MSBF_HEAL_VARIANCE_MIN,
                MSBF_HEAL_VARIANCE_MAX
            )
            return max(1, int(round(base * variance)))

        def _white_wind_amount(self, actor):
            return max(1, int(actor.hp * 0.42 + actor.magic * 0.25))

        def _lowest_wounded_ally(self):
            alive = self.alive_party()
            wounded = [member for member in alive if member.hp < member.max_hp]
            if not wounded:
                return min(alive, key=lambda member: member.hp_ratio)
            return min(wounded, key=lambda member: member.hp_ratio)

        def _first_defeated_ally(self):
            defeated = self.defeated_party()
            if not defeated:
                return None
            return defeated[0]
