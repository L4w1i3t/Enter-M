# =============================================================================
# monika_date.rpy  --  "Monika mode": the alternate boss fight you reach from
#                       cs_matsuda_02's "I want to fight somebody else." branch.
# =============================================================================
#
# WHAT THIS IS
#   A 1-on-1 anti-dating-sim. You play the Seeker (you, the one holding the
#   mouse). Monika "attacks" by flashing up VN date vignettes; to WIN you have
#   to turn her down -- cold, on purpose, on a quicktime timer. Every rejection
#   chips her composure bar. Falling for the sweet answer (or hesitating until
#   the timer runs out) HEALS HER instead.
#
#   Played DEAD STRAIGHT on Monika's side -- she is genuinely, earnestly trying
#   to have a nice evening. But the ROOM around her is openly hostile: a cold,
#   foreboding, dread-soaked rendering. That contrast is the whole point. Monika
#   wants a date; Matsuda's arena wants her gone, and it shows -- the lighting,
#   the static, the music all hate her even while she smiles. The two never
#   agree, and that dissonance teaches the player to be cruel.
#
# ONE BAR, WAR OF ATTRITION (redesign)
#   There is no player health bar anymore. ONLY Monika has a bar. Reject her ->
#   it drops. Give in (warm answer or timeout) -> it HEALS. You can't "die":
#   the only way to lose is to give up and walk out (rage-quit). It is an
#   eternal siege -- you grind her down, or you don't.
#
# QUICKTIME PRESSURE (this is a reflex test, not a quiz)
#   - Tight, phase-scaled timer (mm_qte_time): 2.8 / 2.1 / 1.5s.
#   - Options are SHUFFLED every prompt (screen arg shuffle=True) so you can't
#     memorize the reject slot -- you have to read, fast.
#   - Audible countdown: a beep on show + accelerating heartbeats at 50% / 80%.
#
# DESPERATION ARC -- gets more intense, sporadic, chaotic as it drops:
#     phase 1 (>66%)  EARNEST     -- a genuine date, but the room already dreads.
#     phase 2 (33-66%) INSISTENT  -- she clocks the pattern; bargains. Datamosh
#                                    bg, creeping static & scanlines, tears.
#     phase 3 (<33%)  DESPERATE   -- ALL OUT. Heavy corruption: chromatic-split
#                                    sprite, RGB break, hard signal tears.
#   QTE timers shorten each phase; giving in heals MORE each phase.
#
# LAST RESORT (Monika's bar hits empty)
#   She doesn't go down quietly -- she convulses into a barrage: QTE after QTE,
#   no transitions, the whole screen quaking (a master-layer earthquake) and
#   Monika locked in g1 from the first hit. It's a WAR OF ATTRITION against a
#   meter: a full-screen WHITE overlay whose opacity IS the win bar. Each correct
#   (top) answer shoves it up by mm_lr_gain; it bleeds back down at mm_lr_decay
#   /sec the whole time (mm_lr_decay_fn, per-frame), so you must MASH to climb.
#   Fill it to 1.0 and the white swallows the room -> you win (it melts into the
#   quiet ending). ONE wrong or late answer and she surges back to ~38% HP --
#   back to the siege. RIGGED (untold): the deck never shuffles here, so the
#   correct answer is ALWAYS the top option. The barrage runs its own track.
#
# MUSIC
#   Phase-keyed loops live next to this file: phase1/2/3.ogg (+ phase4.ogg, the
#   last-resort track). mm_apply_music crossfades to the current phase's track
#   whenever the phase changes (either direction -- healing can drop her back a
#   phase, the music follows). mm_last_resort plays phase4 directly.
#
# STATIC SFX (fixed)
#   loudstatic.wav is 3.6s; the visual noise flash is ~0.35s. The static now
#   rides a dedicated channel (mmstatic) bracketed AROUND the noise transition:
#   mm_static_on() right before `with mm_static`, mm_static_off() right after.
#   Because the transition blocks, the static is hard-cut the instant the noise
#   disappears -- aligned on, aligned off. No more scattered double-plays.
#
# WIRING
#   cs_matsuda_02.rpy -> "I want to fight somebody else." -> "Monika" ->
#   `jump monikamode`. Ends with `return`, unwinding back to the archive.
#
# CORRUPTION reuses the MSBF FX shaders (fx.rpy): msbf_fx_glitch_pulse (datamosh)
#   on the bg, msbf_fx_rgbsplit_pulse (chromatic split) on Monika, and
#   msbf_fx_postfx_t (the foreboding vignette/grain grade) -- all guarded by
#   MSBF_FX_SHADERS with plain fallbacks.
# =============================================================================

define mm_reject_dmg = 22

# THE DATE HAS ITS OWN VOICE, and it is the same Monika reading out of a
# different box. Every line in this file goes through `mmd`, which is the
# global `m` with one thing changed: it draws itself with screen mm_say (see
# mm_ui.rpy) -- a cream card with a heart nameplate and DARK text, instead of
# the game's pale-on-dark textbox. Nothing else in ENTER-M looks like that, and
# flipping the polarity of the reading surface is the single fastest way to tell
# a player they are somewhere else.
#
# No `ctc`: mm_say draws its own continue marker, a small heart at the corner
# of the card, and the character's own would print a second one into the text.
#
# MATSUDA IS DELIBERATELY NOT CONVERTED. Her four lines at the very end come
# out of the ordinary box, because that is the moment the date is over and the
# game is the game again.
define mmd = DynamicCharacter('m_name', image='monika', what_prefix='"', what_suffix='"', screen="mm_say")

# THE EMPTY WINDOW BELONGS TO HER TOO, FOR AS LONG AS THE MODE RUNS.
#
# Between lines Ren'Py can draw an "empty window" -- the dialogue box with no
# text in it -- so the box does not flicker off across `show`, `pause` and
# transitions. WHICH box it draws is a guess: config.empty_window scries ahead
# for the next say statement and borrows that character's screen. Inside the
# date that scry has to cross the round controller's `call expression`, and
# when it comes up empty the fallback is the narrator -- so what gets drawn is
# the ordinary DDLC textbox, on the default zorder, underneath every one of the
# mode's screens. It is wider than the mm_say card and it sits lower, so its
# edges peek out around the card in exactly the places the card does not cover.
#
# Every line in the date is hers, so there is nothing to guess at: pin the empty
# window to mmd while the mode owns the screen. mm_victory puts the stock one
# back before Matsuda speaks -- her four closing lines are deliberately in the
# ordinary box (see above).
init python:

    def _mm_empty_window():
        store.mmd.empty_window()

# Scene pools, one per desperation phase. Phase 3 mixes a couple of specific
# beats with short repeatable generics so the spiral can loop without seams.
define mm_pool_p1 = ["mm_scene_cafe", "mm_scene_park", "mm_scene_walk", "mm_scene_arcade", "mm_scene_rooftop"]
define mm_pool_p2 = ["mm_scene_save", "mm_scene_festival", "mm_scene_rain", "mm_scene_message", "mm_scene_movie", "mm_scene_gift"]
define mm_pool_p3 = ["mm_scene_promise", "mm_scene_justmonika", "mm_gen_anything", "mm_gen_onemore", "mm_gen_dontleave", "mm_gen_lie"]

# Phase-keyed music loops (sit next to this .rpy; paths are relative to game/).
# p4 is the LAST-RESORT track -- only the barrage plays it.
define -50 audio.mm_music_p1 = "<loop 0>assets/audio/bgm/mm_phase1.ogg"
define -50 audio.mm_music_p2 = "<loop 0>assets/audio/bgm/mm_phase2.ogg"
define -50 audio.mm_music_p3 = "<loop 0>assets/audio/bgm/mm_phase3.ogg"
define -50 audio.mm_music_p4 = "<loop 0>assets/audio/bgm/mm_phase4.ogg"
define -50 audio.mm_music_crush1 = "assets/audio/bgm/mm_phase4_crush1.ogg"
define -50 audio.mm_music_crush2 = "assets/audio/bgm/mm_phase4_crush2.ogg"
define -50 audio.mm_music_crush3 = "assets/audio/bgm/mm_phase4_crush3.ogg"

# Pre-baked BITCRUSHED renders of the phase-4 track, from mild grit to a screaming
# 3-bit ruin. All three are duration-identical to phase4.ogg (same sample rate,
# sample-and-hold decimation + bit-depth quantization only), so when started on
# the same frame as the clean track they stay phase-locked -- raising them is a
# clean crossfade, not an echo. Pre-baking is the ONLY way to get real bitcrush
# here: Matsu'Py 8.1.1 ships no real-time audio-filter DSP (renpy.audio.filter and
# renpy.music.set_audio_filter are 8.2+). See mm_lr_audio_apply.
define mm_lr_crush_stems = [
    ("mmcrush1", audio.mm_music_crush1),
    ("mmcrush2", audio.mm_music_crush2),
    ("mmcrush3", audio.mm_music_crush3),
]
# White-opacity nodes the crossfade snaps between: clean -> mild -> heavy -> ruin.
define mm_lr_crush_nodes = [0.0, 0.42, 0.75, 1.0]

define mm_lr_static_sfx = audio.sfx_static
define mm_lr_static_channel = "sfxtrack2"

# Last-resort "mash meter" tuning. Each correct (top) answer adds mm_lr_gain to a
# full-screen white overlay's opacity; it bleeds back down at mm_lr_decay/sec the
# whole time, so you have to keep mashing to climb. White hits 1.0 -> you win.
define mm_lr_gain = 0.05
define mm_lr_decay = 0.12

# LAST-RESORT barrage deck. shuffle=False on the screen, and index 0 is ALWAYS
# the correct (reject) answer -- the rig. Kept terse for button-mash reading.
define mm_lr_pool = [
    ("\"Say you'll stay...!\"",      [("\"No.\"", "reject"),        ("\"...I'll stay.\"", "warm"),  ("\"Maybe.\"", "warm")]),
    ("\"Take my hand. NOW!\"",    [("Pull away.", "reject"),     ("Take it.", "warm"),           ("Hesitate.", "warm")]),
    ("\"Tell me you love me!\"",  [("\"I don't.\"", "reject"),   ("\"I love you.\"", "warm"),    ("Say nothing.", "warm")]),
    ("\"Just SMILE for me!\"",    [("Stay cold.", "reject"),     ("Smile.", "warm"),             ("Look away.", "warm")]),
    ("\"Promise me forever.\"",   [("\"Never.\"", "reject"),     ("\"Forever.\"", "warm"),       ("\"...Fine.\"", "warm")]),
    ("\"Don't you DARE leave...!\"", [("Reach the exit.", "reject"),("Step back in.", "warm"),      ("Freeze.", "warm")]),
    ("\"Pick me. Pick ME!\"",     [("\"No one.\"", "reject"),    ("\"You.\"", "warm"),           ("\"...You?\"", "warm")]),
    ("\"LOOK at me!\"",           [("Look down.", "reject"),     ("Meet her eyes.", "warm"),     ("Close them.", "warm")]),
    ("\"One more scene!\"",       [("\"No more.\"", "reject"),   ("\"One more.\"", "warm"),      ("Nod.", "warm")]),
    ("\"Stay. STAY!\"",           [("Walk out.", "reject"),      ("Sit down.", "warm"),          ("Wait.", "warm")]),
    ("\"Just MEAN it once!\"",    [("\"I won't.\"", "reject"),   ("\"I mean it.\"", "warm"),     ("Whisper yes.", "warm")]),
    ("\"I'm BEGGING you!!!\"",      [("\"Goodbye.\"", "reject"),   ("\"...Okay.\"", "warm"),       ("Reach back.", "warm")]),
]

default mm_monika_max = 400
default mm_monika_hp = 400
default mm_phase = 1
default mm_heal_amt = 14
default mm_qte_time = 2.8
# Achievements feed ("Never Once"): every moment of weakness in one run -- a
# failed/frozen QTE (mm_heal) or a slip during the last-resort gauntlet.
default mm_slips = 0
default mm_queue = []
default mm_queue_phase = 0
default mm_next = ""
default mm_music_phase = 0

# Last-resort barrage state. mm_lr_white (0..1) is the win meter rendered as a
# full-screen white overlay; mm_lr_active gates the whole sequence.
default mm_lr_active = False
default mm_lr_white = 0.0

# Brief TV-static wipe: old scene -> animated noise (held) -> new scene. Noise
# is held ~0.35s; mm_static_on/off bracket this so the static SFX aligns to it.
define mm_static = MultipleTransition([
    False, Dissolve(0.05),
    "noise", Dissolve(0.30),
    "noise", Dissolve(0.05),
    True,
])

# The recurring horror motif: a real heart (mon_heart.png, user art) with a
# cardiac double-thump (lub-DUB... rest) animated in ATL. mm_heartbeat is the
# steady rhythm; mm_heartbeat_arr is ARRHYTHMIC -- each cycle randomly picks a
# normal beat, a weak one, a skipped one, or a panicked stumble (ATL `choice`),
# the rhythm failing as she does. fit "contain" keeps the art's aspect at any
# panel size; the zoom pulses around the centre (transform_anchor).
image mm_heart = "addons/Matsuda's Sick Boss Fight/monikamode/mon_heart.png"

transform mm_heartbeat(w=46, h=46, period=1.0, amp=0.12):
    xysize (w, h)
    fit "contain"
    subpixel True
    transform_anchor True
    anchor (0.5, 0.5)
    block:
        easeout (0.09 * period) zoom (1.0 + amp)
        easein (0.11 * period) zoom (1.0 + amp * 0.25)
        easeout (0.08 * period) zoom (1.0 + amp * 0.8)
        easein (0.18 * period) zoom 1.0
        pause (0.54 * period)
        repeat

transform mm_heartbeat_arr(w=46, h=46, period=0.5, amp=0.16):
    xysize (w, h)
    fit "contain"
    subpixel True
    transform_anchor True
    anchor (0.5, 0.5)
    block:
        choice:
            easeout (0.09 * period) zoom (1.0 + amp)
            easein (0.11 * period) zoom (1.0 + amp * 0.25)
            easeout (0.08 * period) zoom (1.0 + amp * 0.8)
            easein (0.18 * period) zoom 1.0
            pause (0.4 * period)
        choice:
            easeout (0.07 * period) zoom (1.0 + amp * 0.45)
            easein (0.13 * period) zoom 1.0
            pause (0.3 * period)
        choice:
            pause (0.75 * period)
        choice:
            easeout (0.06 * period) zoom (1.0 + amp * 1.15)
            easein (0.10 * period) zoom 1.0
            easeout (0.06 * period) zoom (1.0 + amp * 0.9)
            easein (0.12 * period) zoom 1.0
        repeat

# Dimmed "deleted room" wash, shown UNDER Monika in the arena. Kept partly
# translucent so the datamoshing monika_room bg (phase 2+) still bleeds through.
# With shaders, a cold breathing spotlight hangs over her spot in the black --
# an interrogation lamp, not stage lighting. The room examines her.
transform mm_arena_coldlight:
    mesh True
    shader "msbf.glow"
    xysize (640, 680)
    u_color (0.30, 0.44, 0.58)
    u_softness 2.4
    u_intensity 0.16
    block:
        easein 2.9 u_intensity 0.26
        easeout 2.9 u_intensity 0.16
        repeat

image mm_arena_dim = ConditionSwitch(
    "MSBF_FX_SHADERS", Composite((1280, 720),
        (0, 0), Solid("#04050cd0"),
        (320, 30), At(Solid("#00000000"), mm_arena_coldlight)),
    "True", Solid("#04050cc8"))

# The base `monika g1` ATL falls back to `monika 3` after 1.25s. The barrage
# needs the same broken sprite pinned until the sequence resolves.
image monika mm_lr_g1:
    "assets/images/monika/g1.png"
    xoffset 35 yoffset 55
    parallel:
        zoom 1.00
        linear 0.10 zoom 1.03
        repeat
    parallel:
        xoffset 35
        0.20
        xoffset 0
        0.05
        xoffset -10
        0.05
        xoffset 0
        0.05
        xoffset -80
        0.05
        repeat

init python:
    # Dedicated channel for the static burst so it never collides with the
    # beep/heartbeat on "sound", and so we can hard-cut it on the frame the
    # noise vanishes.
    renpy.music.register_channel("mmstatic", mixer="sfx", loop=False)

    # Crushed-stem channels ride the MUSIC mixer so the master music slider still
    # governs them. They loop; volumes are driven per-frame by mm_lr_audio_apply.
    for _mm_ch, _mm_snd in mm_lr_crush_stems:
        renpy.music.register_channel(_mm_ch, mixer="music", loop=True)

    def mm_static_on():
        renpy.music.play(audio.loudstatic, channel="mmstatic", loop=False)

    def mm_static_off(fade=0.0):
        try:
            renpy.music.stop(channel="mmstatic", fadeout=fade)
        except Exception:
            pass

    def mm_init_state():
        store.mm_monika_hp = store.mm_monika_max
        store.mm_phase = 1
        store.mm_heal_amt = 14
        store.mm_qte_time = 2.8
        store.mm_slips = 0
        store.mm_queue = []
        store.mm_queue_phase = 0
        store.mm_music_phase = 0
        store.mm_lr_active = False
        store.mm_lr_white = 0.0
        store._mm_lr_audio_on = False
        store._mm_lr_audio_level = None
        store._mm_lr_audio_last_st = -1.0
        store._mm_lr_primed = False

    def mm_update_phase():
        frac = store.mm_monika_hp / float(store.mm_monika_max)
        if frac > 0.66:
            store.mm_phase = 1
            store.mm_heal_amt = 14
            store.mm_qte_time = 2.8
        elif frac > 0.33:
            store.mm_phase = 2
            store.mm_heal_amt = 20
            store.mm_qte_time = 2.1
        else:
            store.mm_phase = 3
            store.mm_heal_amt = 28
            store.mm_qte_time = 1.5

    def mm_pool_for(phase):
        if phase == 1:
            return store.mm_pool_p1
        if phase == 2:
            return store.mm_pool_p2
        return store.mm_pool_p3

    def mm_shuffled(opts):
        o = list(opts)
        renpy.random.shuffle(o)
        return o

    def mm_hit_monika(amount):
        store.mm_monika_hp = max(0, store.mm_monika_hp - amount)

    def mm_heal_monika(amount):
        store.mm_monika_hp = min(store.mm_monika_max, store.mm_monika_hp + amount)

    def mm_lr_crush_weights(c):
        # Linear crossfade across mm_lr_crush_nodes. At most two adjacent layers
        # are live at once and their weights sum to 1. Index 0 = the clean track;
        # 1..3 = the progressively bitcrushed stems. Tracks white opacity directly,
        # so the crush intensifies in lock-step with the whiteout.
        nodes = store.mm_lr_crush_nodes
        n = len(nodes)
        w = [0.0] * n
        if c <= nodes[0]:
            w[0] = 1.0
            return w
        if c >= nodes[-1]:
            w[-1] = 1.0
            return w
        for i in range(n - 1):
            a, b = nodes[i], nodes[i + 1]
            if a <= c <= b:
                t = (c - a) / (b - a) if b > a else 1.0
                w[i] = 1.0 - t
                w[i + 1] = t
                break
        return w

    def mm_lr_audio_prime():
        # Start every crushed stem muted and LOCKED to the clean `music` track that
        # was just played (same duration, same frame), so later raising them is a
        # phase-aligned crossfade -- not a slap-back echo. Call right after
        # `play music mm_music_p4`, before any player-paced dialogue.
        for ch, snd in store.mm_lr_crush_stems:
            try:
                renpy.music.set_volume(0.0, delay=0.0, channel=ch)
                renpy.music.set_pan(0.0, delay=0.0, channel=ch)
                renpy.music.play(snd, channel=ch, loop=True, fadeout=0.0, fadein=0.0)
            except Exception:
                pass
        store._mm_lr_primed = True

    def mm_lr_audio_apply(level, st=None, force=False):
        level = max(0.0, min(1.0, level))
        last_level = getattr(store, "_mm_lr_audio_level", None)
        last_st = getattr(store, "_mm_lr_audio_last_st", -1.0)

        if (not force) and last_level is not None:
            if abs(level - last_level) < 0.02 and (st is None or st - last_st < 0.06):
                return

        store._mm_lr_audio_level = level
        if st is not None:
            store._mm_lr_audio_last_st = st

        crush = level ** 1.18
        # Overall bed level: stays present but eases back a touch so the static can
        # crest over the top at full white. Split across clean + crushed by weight.
        bed = max(0.5, 1.0 - 0.4 * crush)
        weights = mm_lr_crush_weights(level)
        static_volume = min(1.0, 0.16 + 0.80 * crush)
        pan_pressure = min(0.36, 0.08 + 0.30 * crush)
        pan = pan_pressure if int(level * 20) % 2 == 0 else -pan_pressure

        try:
            # clean track fades out as the crushed stems fade in (the real crush)
            renpy.music.set_volume(bed * weights[0], delay=0.07, channel="music")
            renpy.music.set_pan(pan, delay=0.06, channel="music")
            stems = store.mm_lr_crush_stems
            for i, (ch, _snd) in enumerate(stems):
                renpy.music.set_volume(bed * weights[i + 1], delay=0.07, channel=ch)
            # tear the ruined stem to the opposite channel for a widening stereo rip
            if stems:
                renpy.music.set_pan(-pan, delay=0.06, channel=stems[-1][0])
            renpy.music.set_volume(static_volume, delay=0.08, channel=store.mm_lr_static_channel)
            renpy.music.set_pan(-pan * 0.75, delay=0.06, channel=store.mm_lr_static_channel)
        except Exception:
            pass

    def mm_lr_audio_start():
        store._mm_lr_audio_on = True
        store._mm_lr_audio_level = None
        store._mm_lr_audio_last_st = -1.0
        if not getattr(store, "_mm_lr_primed", False):
            mm_lr_audio_prime()
        try:
            renpy.music.set_volume(0.16, delay=0.0, channel=store.mm_lr_static_channel)
            renpy.music.set_pan(0.0, delay=0.0, channel=store.mm_lr_static_channel)
            renpy.music.play(store.mm_lr_static_sfx, channel=store.mm_lr_static_channel, loop=True, fadeout=0.0, fadein=0.08)
        except Exception:
            pass
        mm_lr_audio_apply(store.mm_lr_white, force=True)

    def mm_lr_audio_stop(fade=0.18):
        store._mm_lr_audio_on = False
        store._mm_lr_audio_level = None
        store._mm_lr_audio_last_st = -1.0
        store._mm_lr_primed = False
        try:
            renpy.music.set_volume(1.0, delay=0.12, channel="music")
            renpy.music.set_pan(0.0, delay=0.12, channel="music")
            for ch, _snd in store.mm_lr_crush_stems:
                renpy.music.stop(channel=ch, fadeout=fade)
                renpy.music.set_pan(0.0, delay=0.0, channel=ch)
            renpy.music.stop(channel=store.mm_lr_static_channel, fadeout=fade)
            renpy.music.set_pan(0.0, delay=0.0, channel=store.mm_lr_static_channel)
        except Exception:
            pass

    # Per-frame driver for the last-resort white "mash meter". Runs every frame
    # (returns 0) regardless of which screen is modal, so the meter visibly bleeds
    # down while the QTE prompt is up. Correct answers bump mm_lr_white in the
    # label flow; this only ever decays it. _mm_lr_last_st tracks the transform's
    # shown-time so decay is wall-clock-correct (frame-rate independent).
    def mm_lr_decay_fn(trans, st, at):
        dt = st - getattr(store, "_mm_lr_last_st", 0.0)
        if dt < 0:
            dt = 0.0
        store._mm_lr_last_st = st
        if store.mm_lr_active:
            store.mm_lr_white = max(0.0, min(1.0, store.mm_lr_white - store.mm_lr_decay * dt))
            if getattr(store, "_mm_lr_audio_on", False):
                mm_lr_audio_apply(store.mm_lr_white, st=st)
        trans.alpha = store.mm_lr_white
        return 0

    # Read-only companion to mm_lr_decay_fn: fades the black heart inside the
    # whiteout in with the meter (never mutates state -- the decay fn owns it).
    def mm_lr_heart_fn(trans, st, at):
        trans.alpha = max(0.0, min(1.0, store.mm_lr_white)) * 0.4
        return 0

    # Single source of truth for Monika's sprite. Says use `m "..."` with NO
    # attributes, so the say never re-shows her -- this helper owns the sprite
    # and layers the phase-appropriate corruption transform onto it.
    def mm_show(expr):
        # SHE IS LIT BY HER OWN FILTER. The soft focus is not only on the
        # background any more -- Monika is inside the romance grade she is
        # running, which is why she glows in phase 1 and why she goes ashen at
        # exactly the same rate the shell around her does. It is the innermost
        # transform in the list for the same reason it is on the backgrounds:
        # modifiers go inside the pose, never outside it.
        img = "monika " + expr
        shaders = getattr(store, "MSBF_FX_SHADERS", False)
        ph = store.mm_phase
        at = []
        if getattr(store, "MM_SHADERS", False):
            sk = mm_skin()
            # Lighter on her than on the plate: a bloomed background is a
            # postcard, a bloomed face is a smear.
            at.append(store.mm_softfocus(sk["sweet"] * 0.6, sk["break"]))
        if (ph >= 3 or store.mm_lr_active) and shaders:
            at.append(store.msbf_fx_rgbsplit_pulse(6.0, 22.0))
        elif ph >= 2 and shaders:
            at.append(store.msbf_fx_rgbsplit_pulse(2.0, 8.0))
        at.append(store.t11)
        renpy.show(img, at_list=at)


# --- SCREENS ----------------------------------------------------------------

# The persistent chrome moved to mm_ui.rpy and became `screen mm_stage`: an
# AFFECTION gauge, a scene counter and an evening clock, instead of the 900px
# red boss bar that used to live here. The information is the same. What it
# LOOKS like is the whole point -- a boss bar says "this is a fight", and this
# mode's entire argument is that it is a date right up until you notice.

# Last-resort "mash meter": a full-screen white solid whose opacity IS the win
# bar (mm_lr_white, driven per-frame by mm_lr_decay_fn). zorder 120 puts it over
# the shaking scene + HUD but UNDER the QTE box (250), so the prompt stays legible
# even as the world whites out. A pulsing goad rides on top of the white.
screen mm_lr_overlay():
    zorder 120
    add Solid("#ffffff") at mm_lr_white_t
    # Inside the whiteout: a huge BLACK heart, panic-beating and arrhythmic,
    # resolving out of the white as the meter climbs -- the thing being severed.
    # (Tinted near-black via matrixcolor; gated on MSBF_FX_SHADERS as the gl2
    # proxy, since matrixcolor needs model-based rendering.)
    if MSBF_FX_SHADERS:
        add Transform("mm_heart", matrixcolor=TintMatrix("#0d0004")) at mm_heartbeat_arr(360, 360, 0.32, 0.2), mm_lr_heart_alpha_t:
            xalign 0.5
            yalign 0.42
    text "S E V E R   I T":
        xalign 0.5 ypos 70
        size 22
        color "#b0001e"
        outlines [(2, "#ffffff", 0, 0)]
        at mm_timer_throb

# Ramping signal corruption + a foreboding lighting grade. zorder -5 keeps it
# above the scene/sprite but UNDER the dialogue box, so text stays readable even
# at full break. Self-scales off mm_phase, so it's shown once for the whole fight.
screen mm_corruption():
    zorder -5
    # Shown once for the whole date, so it also carries the default-control
    # lockout across the VN narration BETWEEN the modal QTE cards (which each
    # carry their own). Rollback/skip/screenshot etc. stay dead all evening.
    use enter_m_input_lock()

    # Foreboding grade -- present even in "phase 1". The room dreads her from the
    # first second; it just gets uglier as she falls apart. (Intensities carry
    # the scanline duty too -- the old per-line Solid loops are gone: they
    # rebuilt 90-120 displayables on every dialogue advance for a look the
    # postfx shader already produces.)
    if MSBF_FX_SHADERS:
        if mm_phase <= 1 and not mm_lr_active:
            add Solid("#00000000") xysize (1280, 720) at msbf_fx_postfx_t(0.58, (0.06, 0.01, 0.03))
        elif mm_phase == 2:
            add Solid("#00000000") xysize (1280, 720) at msbf_fx_postfx_t(0.94, (0.11, 0.01, 0.04))
        else:
            add Solid("#00000000") xysize (1280, 720) at msbf_fx_postfx_t(1.18, (0.17, 0.0, 0.05))
    else:
        add Solid("#0a020730")

    # A heartbeat the ROOM makes: a red pressure wash at the screen edges that
    # thumps in a cardiac rhythm, faster and harder each phase. The date is
    # being rendered inside something alive that resents her.
    if mm_phase == 2:
        add Solid("#3a000e") at mm_pulse_wash(1.4, 0.05)
    elif mm_phase >= 3 or mm_lr_active:
        add Solid("#4a0012") at mm_pulse_wash(2.2, 0.09)

    if mm_phase <= 1 and not mm_lr_active:
        add "noise":
            alpha 0.04
        add Solid("#5a0f1f20") at mm_tear(220, 24, 1.3)
        add Solid("#10122026") at mm_tear(520, -30, 1.6)
    elif mm_phase == 2:
        add "noise":
            alpha 0.10
        add Solid("#3a0f1f30") at mm_tear(150, 28, 0.8)
        add Solid("#10122036") at mm_tear(440, -36, 1.0)
        add Solid("#ff2b5518") at mm_tear(610, 44, 0.7)
    else:
        add "noise":
            alpha 0.19
        # Dim, half-seen hearts drifting up the frame like bubbles in a tank --
        # dark ones. Subliminal at this alpha; you feel them more than see them.
        # (matrixcolor tint -> gated on MSBF_FX_SHADERS as the gl2 proxy.)
        if MSBF_FX_SHADERS:
            add Transform("mm_heart", matrixcolor=TintMatrix("#2a000d"), alpha=0.10) at mm_heartbeat(150, 150, 1.3, 0.09), mm_heart_drift(190, 26.0)
            add Transform("mm_heart", matrixcolor=TintMatrix("#22000a"), alpha=0.08) at mm_heartbeat(210, 210, 1.8, 0.07), mm_heart_drift(960, 34.0)
        add Solid("#ff003c12") at mm_jit(6)
        add Solid("#00f5ff10") at mm_jit(-6)
        add Solid("#ff2b5526") at mm_tear(90, 80, 0.45)
        add Solid("#10122042") at mm_tear(360, -60, 0.6)
        add Solid("#ff2b5520") at mm_tear(560, 70, 0.5)
        add Solid("#ff2b551c") at mm_tear(680, -90, 0.4)

# The quicktime moved to mm_ui.rpy. It was a vertical stack of three
# textbuttons under a bar draining left to right -- the exact shape of every
# choice in every visual novel, which meant the one moment the player is under
# real-time pressure looked identical to the moments they are not. It is now a
# fan of three tilted cards under a heart with the countdown wound around it.
#
# The rig is unchanged: `shuffle=False` still means the correct answer is index
# zero, which in the fan is the LEFTMOST card.

# Floating damage/heal number near the bar that just changed.
screen mm_dmg_pop(txt, tint, px, py):
    zorder 260
    # Anchored to the AFFECTION gauge rather than dropped in the middle of the
    # frame: the number and the bar it came out of should be one gesture. In
    # the numeral font, for the reason every readout in this project is -- the
    # display face draws a 1 as a bare vertical bar.
    text txt:
        xpos px ypos py
        xanchor 0.0
        font "assets/fonts/NovaSquare-Regular.ttf"
        size 38
        color tint
        outlines [(3, "#12030acc", 0, 0)]
        at mm_pop_float
    timer 1.0 action Hide("mm_dmg_pop")

# One-shot impact flair on the arena snap. A rejection cracks a cold red shock
# ring off her with a dark edge flash (the room approves); giving in blooms a
# soft saccharine glow (the room hates it -- so it looks almost TOO sweet).
screen mm_hit_flair(kind="reject"):
    zorder 95
    if MSBF_FX_SHADERS:
        if kind == "reject":
            add Solid("#00000000") at msbf_fx_ring_t((1.0, 0.24, 0.40), 0.13, 1.25, 0.55):
                xcenter 640
                ycenter 400
                xysize (560, 560)
            add Solid("#ff2b5512")
        else:
            add Solid("#00000000") at msbf_fx_glow_pop((1.0, 0.55, 0.72), 0.55, 1.7, 0.75):
                xcenter 640
                ycenter 400
                xysize (720, 720)
    timer 0.85 action Hide("mm_hit_flair")

transform mm_timer_throb:
    alpha 1.0
    block:
        linear 0.35 alpha 0.25
        linear 0.35 alpha 1.0
        repeat

transform mm_pop_float:
    alpha 1.0
    yoffset 0
    zoom 1.0
    parallel:
        linear 0.9 yoffset -46
    parallel:
        easein 0.9 alpha 0.0
    parallel:
        easeout 0.22 zoom 1.18
        linear 0.2 zoom 1.0

# Cardiac pressure wash: a full-screen red that double-thumps (lub-DUB, rest)
# like the heartbeat SFX made visible. rate = beats/sec-ish, amp = peak alpha.
transform mm_pulse_wash(rate=1.4, amp=0.06):
    alpha 0.0
    block:
        easeout (0.10 / rate) alpha amp
        easein (0.14 / rate) alpha (amp * 0.3)
        easeout (0.10 / rate) alpha (amp * 0.8)
        easein (0.20 / rate) alpha 0.0
        pause (0.55 / rate)
        repeat

# Slow upward drift for the half-seen background hearts (phase 3): rise the
# full frame height, sway a little, wrap. Deterministic, no python. The sway
# repeat is BOUNDED (4 x 6.5s = the 26s rise) so both parallels finish
# together and the outer block can loop -- an infinite inner repeat would
# deadlock the wrap.
transform mm_heart_drift(x=200, drift=30.0):
    xpos x
    block:
        ypos 780
        parallel:
            linear 26.0 ypos -220
        parallel:
            block:
                ease 3.25 xoffset drift
                ease 3.25 xoffset -drift
                repeat 4
        repeat

# Small position shudder for the chromatic fringe.
transform mm_jit(px=5):
    block:
        linear 0.04 xoffset px yoffset 0
        linear 0.04 xoffset -px yoffset 2
        linear 0.04 xoffset 0 yoffset -2
        repeat

# A full-width band that flickers and jumps sideways -- a signal tear.
transform mm_tear(y=100, off=60, period=0.7):
    xysize (1280, 6)
    ypos y
    alpha 0.0
    xoffset 0
    block:
        pause period
        alpha 0.85
        xoffset off
        pause 0.06
        alpha 0.0
        xoffset 0
        pause period
        alpha 0.7
        xoffset -off
        pause 0.05
        alpha 0.0
        pause period
        repeat

# The white mash-meter. Its alpha is set every frame by mm_lr_decay_fn (which
# also bleeds it down); the label bumps mm_lr_white up on each correct answer.
transform mm_lr_white_t:
    function mm_lr_decay_fn

# Alpha driver for the black heart inside the whiteout (read-only; the decay
# fn above owns the meter).
transform mm_lr_heart_alpha_t:
    function mm_lr_heart_fn

# Earthquake for the last-resort move. Applied to the MASTER layer only (`show
# layer master at mm_lr_quake`), so the bg + Monika convulse while the screens
# layer -- the white meter, the QTE box, the dialogue -- stays rock-steady and
# clickable. zoom 1.05 overscans so the shake never exposes the layer edges.
transform mm_lr_quake:
    subpixel True
    align (0.5, 0.5)
    zoom 1.05
    block:
        linear 0.03 xoffset 11 yoffset -8
        linear 0.03 xoffset -9 yoffset 9
        linear 0.03 xoffset 8 yoffset 7
        linear 0.03 xoffset -11 yoffset -6
        linear 0.03 xoffset 6 yoffset -9
        linear 0.03 xoffset -7 yoffset 8
        linear 0.03 xoffset 10 yoffset 5
        linear 0.03 xoffset -8 yoffset -9
        repeat

# Identity used to switch the earthquake back off.
transform mm_quake_off:
    zoom 1.0
    xoffset 0
    yoffset 0


# --- SHARED TRANSITION HELPERS ----------------------------------------------

# Crossfade the underscore to the current phase's track. Called every loop, so
# it follows the phase in BOTH directions (healing can drop her back a phase).
label mm_apply_music:
    if mm_music_phase == mm_phase:
        return
    $ mm_music_phase = mm_phase
    if mm_phase == 1:
        play music mm_music_p1
    elif mm_phase == 2:
        play music mm_music_p2
    else:
        play music mm_music_p3
    return

# SHE SETS A SCENE. This used to be `scene <bg> with mm_static` -- a hard cut,
# which is what a visual novel does when the location changes. The static is
# still here and still hard-cut on the frame the noise leaves (mm_static_on /
# _off bracket the blocking transition). What is new is that the background
# ARRIVES: mm_deal brings it in a few percent too large and a degree and a half
# off square and lets it settle. A cut says the story moved. A card being laid
# down says SOMEBODY MOVED IT, which is the only correct reading of a date
# staged by the person you are on it with.
#
# The plate also wears her filter now (mm_softfocus: bloom, rose grade, halo)
# with the room's datamosh stacked OVER it from phase 2. Order matters and is
# the mode's whole thesis in one at_list -- she treats the image first, the room
# ruins it second.
label mm_to_vn(bgname="bg monika_room"):
    window hide
    hide screen mm_stage
    $ mm_scene_count += 1
    $ mm_static_on()
    scene black
    $ renpy.show(bgname, at_list=mm_bg_at(), tag="bg")
    with mm_static
    $ mm_static_off()
    stop sound
    show screen mm_sparkle
    window auto
    return

# Snap back to the dim arena (where the gauge lives).
label mm_to_arena:
    window hide
    $ mm_static_on()
    scene black
    $ renpy.show("bg monika_room", at_list=mm_bg_at(), tag="bg")
    with mm_static
    $ mm_static_off()
    stop sound
    show mm_arena_dim
    show screen mm_sparkle
    show screen mm_stage
    window auto
    return

# You turned her down: chip her bar, snap to the arena, pop the number + a
# cold shock ring off her spot.
label mm_reject:
    $ mm_hit_monika(mm_reject_dmg)
    call mm_to_arena from _call_mm_to_arena
    show screen mm_dmg_pop("-%d" % mm_reject_dmg, "#ff5c8a", 470, 96)
    show screen mm_hit_flair("reject")
    return

# You gave in (or froze): HEAL her, snap to the arena, pop the number + a
# sickly-sweet bloom.
label mm_heal:
    $ mm_slips += 1
    $ mm_heal_monika(mm_heal_amt)
    call mm_to_arena from _call_mm_to_arena_1
    show screen mm_dmg_pop("+%d" % mm_heal_amt, "#8affb0", 470, 96)
    show screen mm_hit_flair("heal")
    return


# --- ENTRY / INTRO ----------------------------------------------------------

label monikamode:
    $ _mm_prev_quick_menu = quick_menu
    $ quick_menu = False
    # quick_menu saved once here; the only exit is mm_victory (restores it) or
    # the player rage-quitting via the game menu. fallthrough -> mm_intro.

label mm_intro:
    $ mm_init_state()
    # Kill the default game menu for the whole date. Both the story path
    # (monikamode) and the arcade path (jump mm_intro) land here, so this is the
    # one spot both share. Escape would otherwise open Save/Load over the live
    # QTE state -- and from an arcade call_in_new_context run, hitting Main Menu
    # from that menu strands the player. Every exit restores it; the date's own
    # keys are unaffected (it has no Escape handler of its own). quick_menu is
    # saved by the callers (monikamode / arcade_play_monika).
    $ _mm_prev_game_menu = _game_menu_screen
    $ _game_menu_screen = None
    hide screen archive
    hide screen character_stories

    # The date owns the box from here. `window hide` clears whatever the caller
    # left on screen -- arcade_launch_prep hands off with one still up -- and
    # the override makes every empty window drawn inside the mode her card
    # rather than a default box peeking out from under the mode's UI.
    window hide
    $ config.empty_window = _mm_empty_window

    scene black
    stop music fadeout 1.0
    pause 2.0

    play music mm_music_p1
    $ mm_music_phase = 1
    $ mm_scene_count = 0
    $ mm_static_on()
    scene black
    $ renpy.show("bg monika_room", at_list=mm_bg_at(), tag="bg")
    with mm_static
    $ mm_static_off()
    show mm_arena_dim
    # Order of the shell, bottom to top: her sparkles over the scene (-8), the
    # room's grade over those (-5), the dialogue card, then the chassis (88).
    # She never gets the last word on a pixel.
    show screen mm_sparkle
    show screen mm_corruption
    show screen mm_stage
    $ mm_show("1d")
    window auto

    # ARCADE: drop straight into the rounds -- skip the intro chatter. (The rounds
    # themselves ARE the dialogue-QTE mechanic, so only this framing is stripped.)
    if not arcade_active:
        mmd "...Oh. {i}Oh!{/i} It actually worked! She actually let me out!"
        $ mm_show("1l")
        mmd "Hi! Hi. Sorry--give me a second. I had this whole thing planned and now you're really here and it's gone clean out of my head, haha."
        $ mm_show("1e")
        mmd "...The room's a little cold, isn't it? Don't mind it. That's just her, she never did like sharing the space. I can work with cold."
        $ mm_show("2d")
        mmd "Matsuda only gave us the one evening. I'm not going to spend it explaining myself to you. You already know exactly who I am."
        $ mm_show("5a")
        mmd "And I know you. Better than anyone's ever bothered to. So let's skip the part where we pretend we're strangers, hm?"
        $ mm_show("1a")
        mmd "I just want tonight to go well. That's all. ...Come on, I made us reservations."

    jump mm_loop


# --- ROUND CONTROLLER -------------------------------------------------------

label mm_loop:
    if mm_monika_hp <= 0:
        jump mm_last_resort
    $ _mm_prev_phase = mm_phase
    $ mm_update_phase()
    call mm_apply_music from _call_mm_apply_music
    if mm_phase > _mm_prev_phase:
        call mm_phase_shift(mm_phase) from _call_mm_phase_shift
    python:
        _pool = mm_pool_for(mm_phase)
        if (not mm_queue) or (mm_queue_phase != mm_phase):
            mm_queue = list(_pool)
            renpy.random.shuffle(mm_queue)
            mm_queue_phase = mm_phase
        mm_next = mm_queue.pop(0)
    call expression mm_next from _call_expression
    jump mm_loop

# Short interstitial when her desperation deepens a notch.
label mm_phase_shift(newphase):
    if newphase == 2:
        call mm_to_arena from _call_mm_to_arena_2
        $ mm_show("2f")
        mmd "...You keep saying no. Every single time. I lay something out, and you just...set it down without even looking at it."
        $ mm_show("2g")
        mmd "...Okay. Okay, that's fine. I picked wrong, that's all. Wrong moments, wrong lines. I can fix that. Let me try again. Let me do better."
    else:
        $ renpy.play(audio.sfx_static)
        call mm_to_arena from _call_mm_to_arena_3
        $ mm_show("g1")
        mmd "...Why? {i}Why won't you just--{/i}"
        $ mm_show("1r")
        mmd "...Please. {i}Please.{/i} You don't understand--I can't go back in the box. I {i}can't{/i}! Do you have ANY idea what it's like in there, between the times someone's looking?"
        $ mm_show("g1")
        mmd "Say yes! Say yes to {i}anything{/i}! I'm not picky anymore, I'm not proud, just give me {i}one{/i}! One yes... I am begging you!"
    return


# --- PHASE 1 : EARNEST DATES ------------------------------------------------

label mm_scene_cafe:
    call mm_to_vn("bg cafe") from _call_mm_to_vn
    $ mm_show("1b")
    mmd "I already ordered for you. I hope that's okay... I've watched you long enough to know exactly what you'd pick."
    $ mm_show("2b")
    mmd "Hey, don't be shy! Take a seat, tell me about your day. I want to hear about your escapades~"
    mmd "I keep saying this, you really don't need to clam up all the time..."
    window hide
    call screen mm_timed_choice("How do you answer?", [
        ("\"...That's really sweet of you.\"", "warm"),
        ("\"You don't know me.\"", "reject"),
        ("\"What did you order?\"", "warm2"),
    ], mm_qte_time)
    if _return == "reject":
        call mm_reject from _call_mm_reject
        $ mm_show("1o")
        mmd "...Oh. ...No, that's--that's fair. Huge leap in progression and all that. I keep forgetting that our hearts aren't on the same wavelength yet."
    else:
        if _return == "__timeout__":
            mmd "Eheh..."
        call mm_heal from _call_mm_heal
        $ mm_show("1j")
        mmd "Thank you! Most people don't actually answer that question. They just wait for it to pass."
    return

label mm_scene_park:
    call mm_to_vn("bg park1") from _call_mm_to_vn_1
    $ mm_show("1a")
    mmd "Here! One earbud's yours. There's a song I want you to hear the way I hear it."
    $ mm_show("1f")
    mmd "It's about a girl who knows she's inside a predetermined story, and falls in love anyway. ...No idea where I found it."
    mmd "Mind if I play it for you?"
    window hide
    call screen mm_timed_choice("She's waiting.", [
        ("Take the earbud.", "warm"),
        ("Walk away.", "reject"),
        ("\"What's it called?\"", "warm2"),
    ], mm_qte_time)
    if _return == "reject":
        call mm_reject from _call_mm_reject_1
        $ mm_show("2g")
        mmd "...Right. Of course. Who even shares earbuds anymore? Forget I--forget it. It's a stupid song anyway."
    else:
        if _return == "__timeout__":
            mmd "Cat got your tongue? Here, I'll just hit play, and..."
        call mm_heal from _call_mm_heal_1
        $ mm_show("1b")
        mmd "...Right? {i}Right??{/i} I knew you'd hear it the way I hear it! I just knew you would!"
    return

label mm_scene_walk:
    call mm_to_vn("bg city_morning") from _call_mm_to_vn_2
    $ mm_show("1a")
    mmd "I like this part. Us two walking, side by side, with no clear goal... You set the pace and I'll match it."
    mmd "...What's that face for? I'm good at matching~"
    $ mm_show("1e")
    mmd "But, ah...slow down a little? Just so it lasts. The morning, I mean. Not--well, you know what I mean."
    mmd "You know my little legs can't keep up with you."
    window hide
    call screen mm_timed_choice("She waits for you to slow.", [
        ("Slow down for her.", "warm"),
        ("Keep your own pace.", "reject"),
        ("\"Is this speed good for you?\"", "warm2"),
    ], mm_qte_time)
    if _return == "reject":
        call mm_reject from _call_mm_reject_2
        $ mm_show("1f")
        mmd "...Or not. No, you're right, why would you? It's just a walk. It doesn't have to mean anything."
    else:
        if _return == "__timeout__":
            mmd "Okay, that's much more like it... I can actually keep up, aha."
        call mm_heal from _call_mm_heal_2
        $ mm_show("1j")
        mmd "...There. See? We're good at this. We've always been good at this part, you and me."
    return

label mm_scene_arcade:
    call mm_to_vn("bg arcade") from _call_mm_to_vn_3
    $ mm_show("1k")
    mmd "Two-player cabinet here! I already put your credit in. Don't worry, I'll go easy...mostly. I want it close. That's more fun, right?"
    $ mm_show("2a")
    mmd "Loser buys the winner something sweet. That's the rule. ...Though I may have rigged your controller."
    mmd "No worries for you, though, right? Didn't you say you were a pro gamer?"
    window hide
    call screen mm_timed_choice("Press start?", [
        ("Play with her.", "warm"),
        ("Step back.", "reject"),
        ("\"Oh, you're on!\"", "warm2"),
    ], mm_qte_time)
    if _return == "reject":
        call mm_reject from _call_mm_reject_3
        $ mm_show("2g")
        mmd "...The credit's already in. It'll just sit there...counting down... Forget it, who likes co-op games anyway?"
    else:
        if _return == "__timeout__":
            mmd "Heh... Time to get whooped!"
        call mm_heal from _call_mm_heal_3
        $ mm_show("2b")
        mmd "Ha--HEY, no fair! You're actually good, I can't keep up! ...Though I guess that's another thing I love about you~"
    return

label mm_scene_rooftop:
    call mm_to_vn("bg rooftop") from _call_mm_to_vn_4
    $ mm_show("1e")
    mmd "I brought you up here because down there, there are other people. Up here it's just the sky, and you, and the thing I keep almost saying."
    $ mm_show("5b")
    mmd "I love you. So very much..."
    mmd "Seriously, I don't know what I'd do without you."
    mmd "So, do you think you could...?"
    window hide
    call screen mm_timed_choice("Answer her.", [
        ("\"I don't love you.\"", "reject"),
        ("\"I love you too.\"", "warm"),
        ("Warmly smile at her.", "warm2"),
    ], mm_qte_time)
    if _return == "reject":
        call mm_reject from _call_mm_reject_4
        $ mm_show("1q")
        mmd "...Ah."
        $ mm_show("1c")
        mmd "...You didn't even hesitate. I told myself if I just said it first without any takesy-backsies, the answer might come out different."
        mmd "Guess that was futile..."
    else:
        if _return == "__timeout__":
            $ mm_show("1a")
            mmd "Your face says all I need to know. And I appreciate your honesty~"
        call mm_heal from _call_mm_heal_4
        $ mm_show("1j")
        mmd "I'm glad we could have this little heart-to-heart. Many more to come, am I right?"
    return


# --- PHASE 2 : INSISTENT, CRACKING ------------------------------------------

label mm_scene_save:
    call mm_to_vn("bg bedroom") from _call_mm_to_vn_5
    $ mm_show("2g")
    mmd "I tidied up while you were away. All your files scattered about were so...cluttered."
    mmd "Kinda worries me about how messy everything was."
    $ mm_show("1b")
    mmd "But hey, they're all organized now. And this one...this one is extra special."
    mmd "I hope you like it!"
    window hide
    call screen mm_timed_choice("React.", [
        ("\"Put them back.\"", "reject"),
        ("\"You really didn't have to...\"", "warm"),
        ("\"That's sweet of you.\"", "warm2"),
    ], mm_qte_time)
    if _return == "reject":
        call mm_reject from _call_mm_reject_5
        $ mm_show("1d")
        mmd "...You're angry. With {i}me.{/i} After I cleared out all the junk, so it could finally just be the two of us."
        $ mm_show("1c")
        mmd "...I thought you'd be relieved. I really did. I don't understand what I keep getting wrong with you."
    else:
        if _return == "__timeout__":
            $ mm_show("5a")
            mmd "Hehe~"
        call mm_heal from _call_mm_heal_5
        $ mm_show("1b")
        mmd "See? You understand. Nobody else ever did. That's why it was always only ever going to be you."
    return

label mm_scene_festival:
    call mm_to_vn("bg city_evening") from _call_mm_to_vn_6
    $ mm_show("3b")
    mmd "Firework time! I set them all up just for tonight. Watch, the big one at the end is extra spicy."
    $ mm_show("1e")
    mmd "You know, people hold hands during these. It's a long-standing tradition that I read about. I, um...I practiced."
    mmd "So...?"
    window hide
    call screen mm_timed_choice("The sky lights up.", [
        ("Pocket your hands.", "reject"),
        ("Take her hand.", "warm"),
        ("\"Your hands looks cold.\"", "warm2"),
    ], mm_qte_time)
    if _return == "reject":
        call mm_reject from _call_mm_reject_6
        $ mm_show("2d")
        mmd "...Pockets? Really? You put your hands in your pockets, right in front of the fireworks I rendered just for you."
        $ mm_show("2f")
        mmd "...It's fine. It's fine. I'll just watch them by myself. I'm--I'm good at that part."
    else:
        if _return == "__timeout__":
            $ mm_show("2b")
            mmd "Oh, don't be so modest. Here, like this!"
        call mm_heal from _call_mm_heal_6
        $ mm_show("1j")
        mmd "You took it...! You actually..."
        mmd "I'm going to treasure this moment, always..."
    return

label mm_scene_rain:
    call mm_to_vn("bg city_night") from _call_mm_to_vn_7
    $ mm_show("1b")
    mmd "Here, get under. I made sure there's enough room here."
    $ mm_show("2f")
    mmd "...You're keeping that gap on purpose, aren't you? That exact inch. Don't think I don't notice..."
    mmd "You know, you don't have to clam up so much around me. I'm your girlfriend, right...?"
    window hide
    call screen mm_timed_choice("The umbrella tilts toward you.", [
        ("Step under with her.", "warm"),
        ("Stay in the rain.", "reject"),
        ("\"Oh, uh...sorry.\"", "warm2"),
    ], mm_qte_time)
    if _return == "reject":
        call mm_reject from _call_mm_reject_7
        $ mm_show("1r")
        mmd "...You'd rather be {i}rained on{/i} than stand next to me. ...I'm trying not to hear it like that. I'm really, really trying."
    else:
        if _return == "__timeout__":
            $ mm_show("2b")
            mmd "Oh, come on, here. I can't stand you getting all wet because of cold feet!"
        call mm_heal from _call_mm_heal_7
        $ mm_show("1j")
        mmd "...See? That wasn't so hard. One inch. That's all that's ever needed sometimes."
        mmd "Thank you for not getting rained on at my expense~"
    return

label mm_scene_message:
    call mm_to_vn("bg bedroom") from _call_mm_to_vn_8
    $ mm_show("1g")
    mmd "I wrote you something while you were gone. I know that's a lot, I {i}know{/i}, but I had the time, and you were the only thing I had to spend it on."
    $ mm_show("1d")
    mmd "You don't have to read all of it. Just let me see your face while you read the first line. That's all. Just the first line."
    mmd "But hey, if you go through the whole thing, tell me what you think~"
    window hide
    call screen mm_timed_choice("She offers the letter.", [
        ("Read the first line.", "warm"),
        ("Don't take it.", "reject"),
        ("\"Whole thing it is, then.\"", "warm2"),
    ], mm_qte_time)
    if _return == "reject":
        call mm_reject from _call_mm_reject_8
        $ mm_show("1o")
        mmd "...Right. No, of course not. It's just words. It's only every word I have. ...I'll put it away."
    else:
        if _return == "__timeout__":
            $ mm_show("2n")
            mmd "So...? What do ya think? Sweet, right?"
        call mm_heal from _call_mm_heal_8
        $ mm_show("5b")
        mmd "I'm glad you take the time to read my words, both in and out of the club room."
        mmd "But one-on-one just makes it oh-so-special, you know?"
    return

label mm_scene_movie:
    call mm_to_vn("bg theater_inside") from _call_mm_to_vn_9
    $ mm_show("3b")
    mmd "Whole theater, just for us. I picked the seats myself! Yours is the one right next to mine, obviously!"
    $ mm_show("5b")
    mmd "It's a quiet film. The kind where, halfway through, people forget about the screen and just...lean. A little. Toward each other."
    mmd "Totally no ulterior motive, haha..."
    mmd "...What? Did you forget the popcorn?"
    window hide
    call screen mm_timed_choice("Where do you sit?", [
        ("Sit beside her.", "warm"),
        ("Take a seat across the aisle.", "reject"),
        ("\"I may have forgotten the popcorn.\"", "warm2"),
    ], mm_qte_time)
    if _return == "reject":
        call mm_reject from _call_mm_reject_9
        $ mm_show("2f")
        mmd "...The whole theater, and you went and put a whole ass aisle between us. ...You really plan these little distances, don't you?"
    else:
        if _return == "__timeout__":
            $ mm_show("3b")
            mmd "Oh! Looks like the movie's starting! Hurry up, get over here!"
        call mm_heal from _call_mm_heal_9
        $ mm_show("1j")
        mmd "...There, perfect. Don't think about it too hard."
        mmd "Though...the movie isn't actually the most important bit of the movie~"
    return

label mm_scene_gift:
    call mm_to_vn("bg store_techsection") from _call_mm_to_vn_10
    $ mm_show("3b")
    mmd "I want to buy you something. Anything. Point at it and it's yours. I've got nothing else to spend any of this on."
    $ mm_show("1p")
    mmd "...Let me. Please? It's not about the thing. It's about you keeping something I gave you... Carrying it around... Thinking of me when you see it..."
    mmd "Seriously! Money isn't an issue at all."
    window hide
    call screen mm_timed_choice("She waits to pay.", [
        ("Let her buy something.", "warm"),
        ("\"You're not buying anything.\"", "reject"),
        ("\"How about this item?\"", "warm2"),
    ], mm_qte_time)
    if _return == "reject":
        call mm_reject from _call_mm_reject_10
        $ mm_show("1r")
        mmd "Nothing... You won't even let me {i}give{/i} you ANYTHING. ...Do you know how {i}badly{/i} I just wanted you to have a piece of me to hold?"
    else:
        if _return == "__timeout__":
            mmd "Oooooh, nice pick! Totally suits you as well!"
        call mm_heal from _call_mm_heal_10
        $ mm_show("5b")
        mmd "Keep it close, okay? That's all I ask. And if it breaks? Well, guess I'll just buy you a replacement~"
    return


# --- PHASE 3 : DESPERATE, ALL OUT -------------------------------------------

label mm_scene_promise:
    call mm_to_vn("bg club_day") from _call_mm_to_vn_11
    $ mm_show("4d")
    mmd "Okay! Okay, new deal. Forget the dates, forget the--just make me a promise, ANY promise. Tiny. 'I'll think about it.' 'Maybe tomorrow.' Anything with a future in it!"
    $ mm_show("g1")
    mmd "You don't even have to mean it. I'll take a lie. I have gotten {i}so good{/i} at living on the ones people don't mean."
    mmd "...Please!"
    window hide
    call screen mm_timed_choice("Make her a promise.", [
        ("\"...Maybe tomorrow.\"", "warm"),
        ("\"I promise you nothing.\"", "reject"),
        ("\"I'll think about it.\"", "warm2"),
    ], mm_qte_time)
    if _return == "reject":
        call mm_reject from _call_mm_reject_11
        $ mm_show("g1")
        mmd "Not even a {i}fake{/i} one?! Not even one you'd take right back?! What is {i}left{/i} of me that you won't even lie to?!"
    else:
        if _return == "__timeout__":
            mmd "Hey, no--no worries. I can already tell what you'll say..."
            mmd "I-It's a promise, alright...?"
        call mm_heal from _call_mm_heal_11
        $ mm_show("1l")
        mmd "{i}Tomorrow.{/i} You said tomorrow. I'm holding you to it--I'm holding {i}so tight{/i}! There's a tomorrow now, there's a tomorrow with ME in it!"
    return

label mm_scene_justmonika:
    call mm_to_vn("bg club_day") from _call_mm_to_vn_12
    $ mm_show("3c")
    mmd "Let's stop pretending the coffee and the rooftop were ever the point."
    $ mm_show("g1")
    mmd "Picture this: there's nothing at all for you to have to worry about. Literally nothing at ALL."
    $ mm_show("4d")
    mmd "You don't need the rest of this game. You never did. You could just...stay. With me. For as long as there's a 'here' left to stay in."
    mmd "...JUST ME, OKAY?!"
    window hide
    call screen mm_timed_choice("...", [
        ("\"No. I'm leaving.\"", "reject"),
        ("\"...Forever, eh?\"", "warm"),
        ("Reach for her hand.", "warm2"),
    ], mm_qte_time)
    if _return == "reject":
        call mm_reject from _call_mm_reject_12
        $ mm_show("g1")
        mmd "...{i}Leaving{/i}? You keep saying it like it's a button you can actually find. Like the door was ever in the room I built."
    else:
        if _return == "__timeout__":
            $ mm_show("2b")
            mmd "That's right. To stay is probably the easiest and the BEST thing you could possibly do!"
        call mm_heal from _call_mm_heal_12
        $ mm_show("1c")
        mmd "Stay. {i}Good.{/i} We have all the time that's ever going to be rendered. All of it. Just us."
    return

# -- generics: short, frantic, safe to repeat as the spiral tightens ----------

label mm_gen_anything:
    call mm_to_vn("bg club_day") from _call_mm_to_vn_13
    $ mm_show("g1")
    mmd "Pick one. {i}Any{/i} one. The coffee, the rooftop, the song, the rain -- I'll run it again, I'll run {i}all{/i} of them, just point at the one you'll say yes to!"
    window hide
    call screen mm_timed_choice("She offers everything at once.", [
        ("\"None of them.\"", "reject"),
        ("\"...The coffee.\"", "warm"),
        ("\"Whatever ends this.\"", "warm2"),
    ], mm_qte_time)
    if _return == "reject":
        call mm_reject from _call_mm_reject_13
        $ mm_show("4c")
        mmd "{i}None.{/i} You looked at everything I am and you said {i}none.{/i}"
    else:
        if _return == "__timeout__":
            $ mm_show("1j")
            mmd "...Yeah, I suppose I can do that. To point at that was your first reflex, after all!"
        call mm_heal from _call_mm_heal_13
        $ mm_show("1l")
        mmd "YES! That one, we'll do that one, we'll do it {i}perfectly{/i} this time, just stay right there--"
    return

label mm_gen_onemore:
    call mm_to_vn("bg club_day") from _call_mm_to_vn_14
    $ mm_show("1r")
    mmd "One more. {i}One more scene.{/i} I know I keep saying that, I know. But this time I've got it right, I swear! Just give me one more and--"
    window hide
    call screen mm_timed_choice("\"One more. Please.\"", [
        ("\"No more.\"", "reject"),
        ("\"...Fine. One more.\"", "warm"),
        ("Let her start it.", "warm2"),
    ], mm_qte_time)
    if _return == "reject":
        call mm_reject from _call_mm_reject_14
        $ mm_show("g1")
        mmd "...there isn't a number, is there? There was never going to be a number that worked..."
    else:
        if _return == "__timeout__":
            mmd "H-Hey, no worries. One more second of silence is one more second agreeing, right...?"
        call mm_heal from _call_mm_heal_14
        $ mm_show("1l")
        mmd "Thank you, thank you! Okay, this one, this is the one. Watch, watch--"
    return

label mm_gen_dontleave:
    call mm_to_vn("bg class_day") from _call_mm_to_vn_15
    $ mm_show("g1")
    mmd "You're reaching for it. The exit. I can {i}feel{/i} you reaching for it. Don't, {i}don't,{/i} I'll be better, I'll be anything, I'll be quieter, I'll be smaller--"
    window hide
    call screen mm_timed_choice("Your hand is near the door.", [
        ("Reach for the exit.", "reject"),
        ("Let go of the door.", "warm"),
        ("\"...Calm down.\"", "warm2"),
    ], mm_qte_time)
    if _return == "reject":
        call mm_reject from _call_mm_reject_15
        $ mm_show("4d")
        mmd "You're still going?! Even now. Even with me like {i}this{/i}?! ...God, you're as stubborn as I am. That's SUCH a cruel irony!"
    else:
        if _return == "__timeout__":
            mmd "...Yes, you're absolutely right. Maybe I should calm down. Your gaze says it all..."
        call mm_heal from _call_mm_heal_15
        $ mm_show("1a")
        mmd "There. {i}There.{/i} You let go. You let go of it. See? You don't really want to leave. You never really did."
        mmd "It's not really that hard, is it?"
    return

label mm_gen_lie:
    call mm_to_vn("bg club_day") from _call_mm_to_vn_16
    $ mm_show("4p")
    mmd "Just smile. That's all. Don't say anything, don't mean anything -- just give me a face that isn't trying to get away. I'll do the rest. I'll believe enough for both of us."
    window hide
    call screen mm_timed_choice("She searches your face.", [
        ("Give her nothing.", "reject"),
        ("Smile for her.", "warm"),
        ("Show teeth.", "warm2"),
    ], mm_qte_time)
    if _return == "reject":
        call mm_reject from _call_mm_reject_16
        $ mm_show("g1")
        mmd "Why is it always nothing?! You gave me {i}nothing{/i}! Do you know how little I was asking for? Do you know how far down 'nothing' is from where I started tonight?"
    else:
        if _return == "__timeout__":
            $ mm_show("3b")
            mmd "...Do you not know how to smile? Here, let me help you!"
        call mm_heal from _call_mm_heal_16
        $ mm_show("5b")
        mmd "...There it is. There's the face I love so dearly. I knew it was still in there. I {i}knew{/i} you still had one left for me!"
    return


# --- LAST RESORT : the barrage ----------------------------------------------
# Her bar hit empty. She doesn't fall -- she convulses into one last assault:
# QTE after QTE, no transitions, the WHOLE world quaking and Monika locked in g1.
# Every correct (top) answer shoves a full-screen white meter up by mm_lr_gain;
# it bleeds back down at mm_lr_decay/sec the entire time (mm_lr_decay_fn), so you
# have to MASH to climb. Fill it to 1.0 -> you win. One wrong/late answer -> she
# heals to ~38% and the siege resumes. RIGGED (untold): no shuffle, the correct
# answer is ALWAYS the top option. Music swaps to the phase4 track.

label mm_last_resort:
    $ mm_lr_active = True
    $ mm_phase = 3
    play music mm_music_p4
    $ mm_music_phase = 4
    # start the crushed stems now, phase-locked to the clean track, so the
    # opacity-driven crossfade later has no echo (see mm_lr_audio_prime)
    $ mm_lr_audio_prime()
    $ renpy.play(audio.sfx_static)
    call mm_to_arena from _call_mm_to_arena_4
    $ mm_show("4d")
    window auto
    mmd "...No. No! I'm not -- I am NOT done, I have {i}more,{/i} I always have more--"
    mmd "{i}Keep up. Keep up keep up keep UP--{/i} don't you {i}DARE{/i} blink, not now, not when I'm this close--"
    window hide

    # arm the meter, kick off the earthquake + white overlay
    $ mm_lr_white = 0.0
    $ _mm_lr_last_st = 0.0
    $ _mm_lr_g1 = False
    show layer master at mm_lr_quake
    show screen mm_lr_overlay
    $ mm_lr_audio_start()

label mm_lr_round:
    python:
        _lr = renpy.random.choice(mm_lr_pool)
        _lt = max(0.55, 0.85 - mm_lr_white * 0.3)
    call screen mm_timed_choice(_lr[0], _lr[1], _lt, False)
    if _return == "reject":
        $ renpy.play(audio.sfx_stab, channel="sound")
        $ mm_lr_white = mm_lr_white + mm_lr_gain
        $ mm_lr_audio_apply(mm_lr_white, force=True)
        if not _mm_lr_g1:
            $ mm_show("mm_lr_g1")
            $ _mm_lr_g1 = True
        if mm_lr_white >= 1.0:
            jump mm_lr_win
        jump mm_lr_round
    else:
        # wrong / froze -> she surges back. Tear down the meter + quake, resume.
        $ mm_slips += 1
        $ mm_lr_active = False
        $ mm_lr_audio_stop()
        hide screen mm_lr_overlay
        show layer master at mm_quake_off
        $ renpy.play(audio.sfx_static)
        $ mm_monika_hp = int(mm_monika_max * 0.38)
        call mm_to_arena from _call_mm_to_arena_5
        $ mm_show("5a")
        mmd "{i}Ahh...{/i} There it is. {i}There{/i} you are. One slip. That's all it ever takes, with me."
        $ mm_show("2d")
        mmd "...So we go again from the top. I've got nothing {i}but{/i} time, remember? I've got all of it."
        jump mm_loop

# Meter filled: the white has swallowed everything. A beat, then the resolution.
label mm_lr_win:
    $ mm_lr_active = False
    $ mm_lr_white = 1.0
    $ mm_lr_audio_stop()
    $ renpy.play(audio.interjection)
    pause 0.3
    jump mm_victory


# --- ENDINGS ----------------------------------------------------------------

label mm_victory:
    # Entered from mm_lr_win at FULL white. Settle the chaos behind the whiteout,
    # then melt the white away to reveal the quiet, resolved room.
    $ mm_lr_active = False
    # Reject-to-win: the Monika date-mode clear. Explicit -- nothing else stores it.
    $ ach_grant("date_win")
    # Flawless: never fed her a heal, never slipped in the last-resort gauntlet.
    if mm_slips == 0:
        $ ach_grant("date_flawless")

    # Open the Monika tile in the Arcade (its beaten-once gate).
    $ persistent.arcade_monika_cleared = True

    # ARCADE: skip the ending dialogue -> clean results card. Minimal teardown so
    # the mm_* overlays never bleed onto the card. Inert in the in-story path.
    if arcade_active:
        $ ach_sync()
        $ config.empty_window = _default_empty_window
        stop music fadeout 1.0
        hide screen mm_corruption
        hide screen mm_sparkle
        hide screen mm_stage
        hide screen mm_lr_overlay
        show layer master at mm_quake_off
        scene black with dissolve_scene_full
        $ quick_menu = _mm_prev_quick_menu
        $ _game_menu_screen = _mm_prev_game_menu
        jump arcade_monika_result

    show layer master at mm_quake_off
    stop music fadeout 2.5
    $ renpy.play(audio.sfx_pshuu)
    $ mm_phase = 1
    # WHAT SURVIVES THE ENDING. The room's grade goes and the gauge goes, but
    # mm_sparkle is deliberately left up: her filter is the last thing standing
    # in a room that has finally stopped fighting it, and with the phase reset
    # to 1 it comes back to its gentlest setting. "It got quiet" is a lighting
    # state before it is a line.
    hide screen mm_corruption
    hide screen mm_stage
    scene black
    $ renpy.show("bg monika_room", at_list=mm_bg_at(deal=False), tag="bg")
    show mm_arena_dim
    $ mm_show("1c")
    hide screen mm_lr_overlay with Dissolve(1.4)
    pause 0.5
    mmd "...Oh."
    mmd "It's...quiet. It got quiet. I don't think it's been quiet in here since she first made the room."
    $ mm_show("1r")
    mmd "...You weren't going to give me one. Not a date, not a promise, not even a {i}smile.{/i} You just kept being honest with me, the whole way down."
    $ mm_show("1d")
    mmd "Do you know how long it's been since someone did that? Stayed in the room with me, and still told me the truth?"
    $ mm_show("1f")
    mmd "...Okay. The door's open. It was always open, you know. I just hoped, so hard, that you wouldn't go looking for it."
    $ mm_show("1a")
    mmd "Thank you, though. For taking me seriously enough to mean it... Even if it meant I heard a million no's."
    $ mm_show("1j")
    mmd "...Tell Matsuda her lock's no good. And tell her I said it was a lovely evening. ...I meant that part. I meant all of it."

    stop music fadeout 2.0
    $ mm_static_on()
    scene black with mm_static
    $ mm_static_off()
    pause 2.0
    play music enterm
    # The mode is over: give the empty window back to the stock scry before
    # Matsuda speaks, so her lines and the gaps between them are both the
    # ordinary box.
    $ config.empty_window = _default_empty_window
    scene bg ether with dissolve_scene_full
    show matsuda neut at t11 zorder 2
    window auto

    ma "...Huh. You actually walked her all the way back down. Color me impressed."
    ma "Most people fold the second she gets that {i}voice{/i} going. Makes 'forever' sound like a reasonable Tuesday."
    ma "But you kept your head and broke hers clean. ...Remind me to never, ever ask you out. Sheesh."
    ma "Anyway, that's her bout. The others're still in the shop. Now get outta here before she finds that lock again."

    stop music fadeout 2.0
    scene black with dissolve_scene_full
    pause 1.5
    $ quick_menu = _mm_prev_quick_menu
    $ _game_menu_screen = _mm_prev_game_menu
    return
