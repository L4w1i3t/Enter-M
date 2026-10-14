# Shared Archivist roster, records, audio, body shader and developer launcher.
# Biography, Horror, Nonfiction and Mystery are playable; Comedy, Tragedy and
# Fiction remain roster sketches. inv_roll_for_invasion() is disabled by
# INV_ENCOUNTERS_ENABLED and has no story call site. Developer Date Jump reaches
# archivist_invasion_dev; story interruptions are not currently wired.
#
# Each encounter changes from a turn-based bout into its own real-time genre.
# Preserve the shared presentation constraints: controls/numbers/state words,
# no spoken narration or comedy, visibly distorted bodies, rupture entrances and
# exits, and telegraphed hazards that can be avoided without taking damage.
# Archivists borrow forms; Biography's use of Matsuda's image is not Matsuda.
#
# Shader names are global and must remain unique:
#   inv.flesh: shared body/heart; inv.lens, inv.panel and inv.sheet: the
#   shared kit (inv_kit.rpy); inv.soup and inv.misreg: Biography; inv.dark
#   and inv.wither: Horror (inv.pall is retired -- its name stays reserved);
#   inv.plain and inv.strike: Nonfiction; inv.lamp and inv.lacuna: Mystery.
# Presentation shared by all four (Oct 2 2026): inv_kit.rpy -- the lens pass,
# particles, the per-frame painter, panel chrome, the turn log and the retry
# overlay -- and the original FX art in fx/.
# The shared body shader warps horizontal bands independently, pivots stretch
# around the feet and erodes the silhouette during arrival/departure.

init -9 python:
    INV_FLESH_OK = False

    def _inv_register_flesh():
        renpy.register_shader("inv.flesh", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_flesh_res;
            uniform float u_flesh_t;
            uniform float u_flesh_warp;
            uniform float u_flesh_split;
            uniform vec2 u_flesh_stretch;
            uniform float u_flesh_pivot;
            uniform float u_flesh_hurt;
            uniform float u_flesh_diss;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float flesh_hash(vec2 p) {
                return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
            }
        """, fragment_300="""
            vec2 plate_uv = v_tex_coord;
            vec2 uv = v_tex_coord;
            vec2 piv = vec2(0.5, clamp(u_flesh_pivot, 0.0, 1.0));
            vec2 st = max(u_flesh_stretch, vec2(0.08));
            uv = (uv - piv) / st + piv;

            float t = u_flesh_t;
            float w = clamp(u_flesh_warp, 0.0, 4.0);
            float amp = 0.006 + 0.026 * w;

            float band = floor(uv.y * 14.0);
            float ph = flesh_hash(vec2(band, 3.7)) * 6.2831853;
            float rate = 1.3 + flesh_hash(vec2(band, 9.1)) * 2.2;
            uv.x += sin(uv.y * 21.0 + t * rate + ph) * amp;
            uv.x += sin(uv.y * 5.0 - t * 0.9) * amp * 0.55;
            uv.y += sin(uv.x * 8.0 + t * 1.7 + ph * 0.5) * amp * 0.40;

            float sp = u_flesh_split * (0.003 + 0.011 * w);
            vec4 cr = texture2D(tex0, uv + vec2(sp, 0.0));
            vec4 cg = texture2D(tex0, uv);
            vec4 cb = texture2D(tex0, uv - vec2(sp, 0.0));
            vec4 col = vec4(cr.r, cg.g, cb.b, cg.a);

            float diss = clamp(u_flesh_diss, 0.0, 1.0);
            if (diss > 0.0) {
                vec2 cell = floor(uv * vec2(52.0, 74.0));
                float n = flesh_hash(cell);
                col *= step(diss, n);
            }

            float hurt = clamp(u_flesh_hurt, 0.0, 1.0);
            col.rgb = mix(col.rgb, vec3(col.a), hurt);

            // ---- THE PLATE CONTRACT (shared by every Archivist body) -------
            // Two things every one of these shaders has to do on its last
            // line, and none of them did until Aug 23 2026.
            //
            // 1. PREMULTIPLIED ALPHA. gl2 blends src + dst * (1 - a), so a
            //    pixel whose RGB is brighter than its own alpha ADDS light --
            //    and at alpha zero with bright RGB it adds light while
            //    claiming to be invisible. Every one of these shaders moves
            //    colour around without reference to alpha somewhere, so all of
            //    them were painting the transparent MARGIN of the padded plate
            //    and drawing the plate's own rectangle on screen as a faint
            //    glowing box. Clamping RGB to alpha is the fix.
            //
            // 2. THE EDGE. A mesh shader is clipped dead at its plate
            //    rectangle, so anything still opaque at the boundary is cut in
            //    a straight line. Padding buys room; it guarantees nothing.
            //    The feather is measured in the plate's OWN untransformed
            //    coordinate, so warps, swells and strays cannot escape it.
            // THIS ONE MATTERS EVERYWHERE, not just in Biography: the heart
            // in EVERY corruptive state is drawn through this shader. The
            // chromatic split above samples red and blue at OFFSET positions,
            // so any pixel where the centre tap is transparent and an offset
            // tap is not comes out coloured at zero alpha -- a coloured haze
            // ringing the avatar, in all four fights, forever.
            vec2 pe = min(plate_uv, vec2(1.0) - plate_uv);
            col *= smoothstep(0.0, 0.045, min(pe.x, pe.y));
            gl_FragColor = vec4(min(col.rgb, vec3(col.a)), col.a);
        """)

    try:
        _inv_register_flesh()
        INV_FLESH_OK = True
    except Exception as _inv_fl_e:
        INV_FLESH_OK = False
        try:
            renpy.log("INV FX: flesh shader registration failed: %r" % _inv_fl_e)
        except Exception:
            pass


# --- ROSTER, RECORD, AND SHARED PLUMBING -------------------------------------
# init -8: everything here must exist before any individual invasion file's
# init python runs, and "Archivist Invasions" sorts before the folders whose
# helpers get borrowed at RUNTIME (battle_logic's channel picker, the input
# lock screen). Nothing in this file touches those at init time.
init -8 python:
    import random as inv_random

    INV_DIR = "addons/Archivist Invasions/"
    INV_SFX_DIR = "assets/audio/sfx/"
    INV_SE_DIR = "assets/audio/sfx/touhou/"
    INV_MSBF_SFX_DIR = "assets/audio/sfx/msbf/"

    # Fixed-step simulation, shared by every invasion's stage displayable.
    INV_TICK = 1.0 / 60.0
    INV_MAX_CATCHUP = 4

    # Breakcore, so the setpiece has a pulse to sit on. Act one only uses it
    # for ambience; act two puts hazards on it.
    INV_BPM = 174.0
    INV_BEAT_TICKS = (60.0 / INV_BPM) / INV_TICK      # ~20.7 ticks per beat

    INV_FONT = "assets/fonts/NovaSquare-Regular.ttf"   # HUD, windows, digits

    # THE PLAYER'S AVATAR IN EVERY CORRUPTIVE STATE. The SOUL heart the other
    # game modes run on (Kotonoha's cellar, borrowed by Tsubaki mode before
    # this), 12x10 pixel art -- and in here it is never drawn clean. It goes
    # through inv.flesh at a punishing warp, because whatever is standing in
    # for you in an Archivist's own genre should not look well.
    INV_HEART = "addons/Matsuda's Sick Boss Fight/kotonohamode/player.png"
    INV_HEART_W, INV_HEART_H = 12, 10

    # --- SHARED BODY DRAWING -------------------------------------------------
    # A warp shader needs somewhere to push pixels TO: applied straight to a
    # sprite, everything it displaces past the original silhouette is clipped
    # off at the edge. So every body is first composited into a transparent
    # margin, and the mesh runs on that.
    _INV_PLATE_CACHE = {}

    def inv_body_plate(path, nat_w, nat_h, zoom, pad_x=1.55, pad_y=1.28,
                    nearest=False):
        """Return (padded displayable, W, H), cached per zoom."""
        key = (path, round(zoom, 3), pad_x, pad_y, nearest)
        entry = _INV_PLATE_CACHE.get(key)
        if entry is None:
            if len(_INV_PLATE_CACHE) > 80:
                _INV_PLATE_CACHE.clear()
            w = max(2, int(nat_w * zoom))
            h = max(2, int(nat_h * zoom))
            W = max(4, int(w * pad_x))
            H = max(4, int(h * pad_y))
            inner = Transform(path, zoom=zoom, nearest=True) if nearest else \
                    Transform(path, zoom=zoom)
            entry = (Composite((W, H), ((W - w) // 2, (H - h) // 2), inner), W, H)
            _INV_PLATE_CACHE[key] = entry
        return entry

    def inv_flesh(plate, W, H, t, warp=1.0, split=1.0, stretch=(1.0, 1.0),
                pivot=0.86, hurt=0.0, diss=0.0):
        """Wrap a padded plate in the shared body-contortion shader."""
        return Transform(
            plate, mesh=True, shader="inv.flesh",
            u_flesh_res=(float(W), float(H)),
            u_flesh_t=float(t),
            u_flesh_warp=float(warp),
            u_flesh_split=float(split),
            u_flesh_stretch=(float(stretch[0]), float(stretch[1])),
            u_flesh_pivot=float(pivot),
            u_flesh_hurt=float(hurt),
            u_flesh_diss=float(diss))

    # --- THE SEVEN -----------------------------------------------------------
    # status: "live"  -> playable, the dev menu will launch it
    #         "board" -> drawing board, the dev menu shows it and refuses
    # The notes are working sketches for the design pass, NOT decided canon --
    # they exist so the dev menu has something to show and so the shape of the
    # set stays visible while only one of them is built.
    INV_ARCHIVISTS = (
        {
            "slug": "biography",
            "name": "BIOGRAPHY",
            "status": "live",
            "label": "archivist_invasion_biography",
            "form": "Wearing Matsuda. A life needs someone to have lived it.",
            "note": "The first of them, and the only one built. Fights you with a glaive "
                    "and a filing habit: it is not trying to kill the party member, it is "
                    "trying to finish the entry, and the party member is what the entry is "
                    "about.",
            "corruptive": "Open combat on a stage, shot through a camera that will not hold "
                        "still. It stops taking turns and starts swinging, and you answer "
                        "with four daggers and no fifth one -- a thrown one is spent until "
                        "you walk back over it, and they land wherever it was standing. "
                        "Hurting it means breaking its composure first, and that only "
                        "happens from inside its reach.",
        },
        {
            "slug": "horror",
            "name": "HORROR",
            "status": "live",
            "label": "archivist_invasion_horror",
            "form": "A tall bird-headed thing carrying a lantern. It is not wearing anyone.",
            "note": "The second one built. You cannot hurt it -- the lantern is the only "
                    "thing it flinches from, and light costs nerve. Act one is not about "
                    "winning, it is about keeping it far away, because how close it is when "
                    "the room turns is exactly how much head start you get.",
            "corruptive": "A chase. No attacks, no dodging into it, nothing to kill -- you "
                        "run, it follows, and the only win is distance. Sprinting costs "
                        "wind, looking back costs speed, and the less room there is between "
                        "you the less of the dark you are allowed to see.",
        },
        {
            "slug": "nonfiction",
            "name": "NONFICTION",
            "status": "live",
            "label": "archivist_invasion_nonfiction",
            "form": "Nobody in particular. A fact does not need anyone to be true.",
            "note": "The third one built. It is not trying to kill you and it is not trying "
                    "to reach you -- it is checking you against the record, and whatever it "
                    "cannot corroborate does not get to have happened. Damage is not damage "
                    "until it is sourced, and everything still unsourced can be taken back.",
            "corruptive": "The page. Every light comes up, the room turns white, and the "
                        "fight is held on a plain ruled plane that is struck out cell by "
                        "cell while you stand on it. Nothing to attack: you win by getting "
                        "ON RECORD, which means standing still on a shrinking floor.",
        },
        {
            "slug": "mystery",
            "name": "MYSTERY",
            "status": "live",
            "label": "archivist_invasion_mystery",
            "form": "The investigator. Not the culprit -- a mystery needs somebody who is "
                    "about to explain, and never anybody who does.",
            "note": "The fourth one built, and the only one of them that is on your side. It "
                    "hands you evidence, it rules things out for you for free, and every "
                    "single thing it tells you is true. What it will not do -- what it cannot "
                    "do, because the moment it does it stops existing -- is let any of it add "
                    "up. THE FIELD is how many readings are still open, and it can be brought "
                    "down to two and never to one.",
            "corruptive": "The dark, and a lineup in it. The bulb falls and every light goes "
                        "out, and what you failed to rule out in the bout is standing in the "
                        "room: one figure per open reading, each under its own frame and "
                        "glyph, all of them wearing the same coat. One is the subject. You are "
                        "a lamp. On a countdown a bell says one true thing -- whether the "
                        "subject is inside your light -- and everyone who does not match is "
                        "crossed off. It will never leave one: at two it says TWO REMAIN, and "
                        "the heartbeat has to tell you which. Accuse wrongly and the room "
                        "turns on you.",
        },
        {
            "slug": "comedy",
            "name": "COMEDY",
            "status": "board",
            "form": "Undecided.",
            "note": "Drawing board.",
            "corruptive": "Sketch: timing. Everything is a bit, the bits are on a beat, and "
                        "the fight is only survivable by playing along with something that is "
                        "not actually funny.",
        },
        {
            "slug": "tragedy",
            "name": "TRAGEDY",
            "status": "board",
            "form": "Undecided.",
            "note": "Drawing board.",
            "corruptive": "Sketch: the ending is posted in advance and it is correct. The "
                        "fight is about how much of it you are willing to sit through without "
                        "the option of preventing it.",
        },
        {
            "slug": "fiction",
            "name": "FICTION",
            "status": "board",
            "form": "Undecided.",
            "note": "Drawing board. Last of the seven for a reason.",
            "corruptive": "Sketch: it makes things up. Rules arrive mid-fight, hold for as "
                        "long as it feels like, and are replaced -- including the rules the "
                        "other six were obeying.",
        },
    )

    INV_BY_SLUG = dict((a["slug"], a) for a in INV_ARCHIVISTS)

    def inv_archivist(slug):
        """One roster record, or None."""
        return INV_BY_SLUG.get(slug)

    def inv_is_playable(slug):
        """True only for an Archivist whose fight exists AND whose label loaded."""
        entry = INV_BY_SLUG.get(slug)
        if not entry or entry.get("status") != "live":
            return False
        label_name = entry.get("label")
        return bool(label_name and renpy.has_label(label_name))

    def inv_playable_slugs():
        return tuple(a["slug"] for a in INV_ARCHIVISTS if inv_is_playable(a["slug"]))

    # --- THE RECORD ----------------------------------------------------------
    # persistent.inv_fended is the set of slugs that have been fended off. It is
    # read through a normalizer rather than trusted, because a persistent that
    # predates this file is None and a persistent written by an older shape of
    # the system could be a list (the project's persistent-default rule).
    def inv_fended():
        raw = getattr(persistent, "inv_fended", None)
        if not raw:
            return set()
        try:
            return set(raw)
        except Exception:
            return set()

    def inv_record_result(slug, won):
        """Write a finished invasion into the persistent record.

        Winning files the Archivist away for good. Losing leaves it in the pool
        -- which is the whole reason a repeat is allowed to happen.
        """
        if not slug:
            return

        fended = inv_fended()
        if won:
            fended.add(slug)
        persistent.inv_fended = fended

        losses = dict(getattr(persistent, "inv_losses", None) or {})
        if not won:
            losses[slug] = int(losses.get(slug, 0)) + 1
            persistent.inv_losses = losses

        try:
            renpy.save_persistent()
        except Exception:
            pass

    def inv_clear_record():
        """Dev switch: forget every invasion result."""
        persistent.inv_fended = set()
        persistent.inv_losses = {}
        try:
            renpy.save_persistent()
        except Exception:
            pass
        renpy.restart_interaction()

    # --- THE ENCOUNTER ROLL (INERT) ------------------------------------------
    # The drawing-board rules made concrete. Nothing calls this, and the master
    # switch keeps it from doing anything if something does by accident.
    INV_ENCOUNTERS_ENABLED = False
    INV_ENCOUNTER_ODDS = 64          # 1 in N at an eligible seam

    def inv_roll_for_invasion(rng=None):
        """Return the slug of an Archivist that should cut in right now, or None.

        Draws only from Archivists that are BUILT and still outstanding, so the
        seven-fend set can be completed without ever replaying a win.
        """
        if not INV_ENCOUNTERS_ENABLED:
            return None
        if not getattr(persistent, "playthrough", 0):
            return None

        outstanding = [s for s in inv_playable_slugs() if s not in inv_fended()]
        if not outstanding:
            return None

        rng = rng or inv_random
        if rng.randrange(INV_ENCOUNTER_ODDS) != 0:
            return None
        return rng.choice(outstanding)

    # --- AUDIO ---------------------------------------------------------------
    # Act one and act two are separate pieces, so the shift is a CUT, not a
    # cross-fade: the soup goes silent for a breath and act two lands on top of
    # the player. Aliases only -- never a raw path in a play statement.
    def inv_music_survey():
        try:
            renpy.music.play(audio.blackwolf, channel="music", fadein=0.0, loop=True)
        except Exception:
            pass

    def inv_music_corruptive():
        try:
            renpy.music.play(audio.blackwolf_corruptive, channel="music",
                            fadeout=0.0, fadein=0.0, loop=True)
        except Exception:
            pass

    def inv_music_stop(fadeout=1.2):
        try:
            renpy.music.stop(channel="music", fadeout=fadeout)
        except Exception:
            pass

    # --- SFX -----------------------------------------------------------------
    # Cues are borrowed from stock the project already ships. Playback rides its
    # own round-robin pool so a swing, a hit, and a UI blip in the same tick do
    # not cut each other off (battle_logic's picker takes an IDLE channel rather
    # than the next one in rotation).
    INV_SFX = {
        # act one -- the window UI
        "cursor":   (INV_MSBF_SFX_DIR + "uiblip.wav", 0.45),
        "confirm":  (INV_MSBF_SFX_DIR + "ui_accept.wav", 0.55),
        "cancel":   (INV_MSBF_SFX_DIR + "ui_denied.wav", 0.45),
        "text":     (INV_SFX_DIR + "tick.ogg", 0.22),
        "roll":     (INV_MSBF_SFX_DIR + "uiblip.wav", 0.20),
        "bash":     (INV_MSBF_SFX_DIR + "hit.wav", 0.75),
        "crit":     (INV_MSBF_SFX_DIR + "crit.wav", 0.85),
        "miss":     (INV_MSBF_SFX_DIR + "miss.wav", 0.60),
        "guard":    (INV_MSBF_SFX_DIR + "guard.wav", 0.70),
        "heal":     (INV_MSBF_SFX_DIR + "heal.wav", 0.75),
        "refuse":   (INV_MSBF_SFX_DIR + "resist.wav", 0.80),
        "scan":     (INV_MSBF_SFX_DIR + "scan.wav", 0.65),
        "hurt":     (INV_MSBF_SFX_DIR + "down.wav", 0.75),
        "enemy":    (INV_MSBF_SFX_DIR + "enemy.wav", 0.70),
        # the shift
        "tear":     (INV_SFX_DIR + "loudstatic.wav", 0.85),
        "slam":     (INV_SFX_DIR + "sfx-hollowboom.wav", 0.90),
        "phase":    (INV_MSBF_SFX_DIR + "phase.wav", 0.90),
        # act two -- open combat
        "swing":    (INV_SE_DIR + "se_slash.wav", 0.65),
        "wind":     (INV_SE_DIR + "se_ch00.wav", 0.55),
        "wind2":    (INV_SE_DIR + "se_ch01.wav", 0.60),
        "dash":     (INV_SE_DIR + "se_focusin.wav", 0.55),
        "cut":      (INV_SE_DIR + "se_damage00.wav", 0.55),
        "cut_big":  (INV_SE_DIR + "se_damage01.wav", 0.70),
        "clash":    (INV_SE_DIR + "se_enep00.wav", 0.70),
        "ring":     (INV_SE_DIR + "se_lazer00.wav", 0.55),
        "throw":    (INV_SE_DIR + "se_gun00.wav", 0.60),
        "note":     (INV_SE_DIR + "se_tan01.wav", 0.45),
        "graze":    (INV_SE_DIR + "se_graze.wav", 0.40),
        "struck":   (INV_SE_DIR + "se_pldead00.wav", 0.80),
        "break":    (INV_SE_DIR + "se_enep01.wav", 0.90),
        "win":      (INV_MSBF_SFX_DIR + "victory.wav", 0.85),
    }

    INV_SFX_POOL = ["inv_sfx_%d" % i for i in range(10)]
    for _inv_ch in INV_SFX_POOL:
        if not renpy.music.channel_defined(_inv_ch):
            renpy.music.register_channel(_inv_ch, mixer="sfx", loop=False)

    # A LOOPING channel of its own for a heartbeat, held under a setpiece and
    # ridden up and down by whatever is squeezing the player. Pooled one-shots
    # cannot do this: the point is that it never stops.
    INV_HEART_CHANNEL = "inv_heart"
    if not renpy.music.channel_defined(INV_HEART_CHANNEL):
        renpy.music.register_channel(INV_HEART_CHANNEL, mixer="sfx", loop=True)

    INV_HEARTBEAT = INV_SFX_DIR + "heartbeat_ominous.ogg"

    def inv_heart_start(volume=0.5):
        try:
            renpy.music.play(INV_HEARTBEAT, channel=INV_HEART_CHANNEL,
                            loop=True, fadein=0.8)
            renpy.music.set_volume(inv_clamp(volume, 0.0, 1.0),
                                channel=INV_HEART_CHANNEL)
        except Exception:
            pass

    def inv_heart_level(volume):
        """Ride the heartbeat's volume with whatever is closing in."""
        try:
            renpy.music.set_volume(inv_clamp(volume, 0.0, 1.0), delay=0.15,
                                channel=INV_HEART_CHANNEL)
        except Exception:
            pass

    def inv_heart_stop(fadeout=1.0):
        try:
            renpy.music.stop(channel=INV_HEART_CHANNEL, fadeout=fadeout)
        except Exception:
            pass

    def inv_play(name, volume_scale=1.0):
        entry = INV_SFX.get(name)
        if not entry:
            return
        try:
            channel = msbf_pick_pool_channel(INV_SFX_POOL, "cursor", inv_play)
            if channel is None:
                return
            renpy.sound.play(entry[0], channel=channel,
                            relative_volume=entry[1] * volume_scale)
        except Exception:
            pass

    def inv_stop_sfx(fadeout=0.15):
        for channel in INV_SFX_POOL:
            try:
                renpy.music.stop(channel=channel, fadeout=fadeout)
            except Exception:
                pass

    # --- SMALL MATH + SCREEN POLL --------------------------------------------
    # The keyboard. Every invasion POLLS rather than waiting on events, so the
    # shim lives here and a mode that cannot import it simply reads no input
    # rather than crashing.
    try:
        import pygame_sdl2 as inv_pg
    except Exception:
        inv_pg = None

    def inv_clamp(v, lo, hi):
        return lo if v < lo else (hi if v > hi else v)

    def inv_smooth(u):
        """Smootherstep: zero velocity AND acceleration at both ends, so
        anything driven by it starts and stops without a visible seam."""
        u = inv_clamp(u, 0.0, 1.0)
        return u * u * u * (u * (u * 6.0 - 15.0) + 10.0)

    def inv_lerp(a, b, t):
        return a + (b - a) * t

    def inv_approach(value, target, rate):
        """Move `value` toward `target` by at most `rate`."""
        if value < target:
            return min(target, value + rate)
        if value > target:
            return max(target, value - rate)
        return value

    def inv_player_name():
        """The party member's name, never sliced, never assumed non-empty."""
        name = (getattr(store, "inv_player", "") or "").strip()
        return name

    def inv_poll_result(game):
        """Slow screen timer hook: a non-None return ends the interaction with
        that value, which is how a stage hands its result back to the script
        without restarting the interaction every tick."""
        return game.result


# --- STATE -------------------------------------------------------------------
# The record, plus the dev-side launch flag. `inv_dev_test` is True whenever an
# invasion was started from the Developer Date Jump menu: the fight itself is
# identical, only the framing around it changes (no story wrapper, and it
# returns to the dev menu instead of a day file).
default persistent.inv_fended = set()
default persistent.inv_losses = {}
default inv_dev_test = False
default inv_active_slug = None

# Dev-only: skip an invasion's opening act and start in the corruptive state.
# Every invasion reads this in its constructor; it is False in every path that
# is not a developer launch.
default inv_dev_start_open = False

# Dev-only GODMODE: incoming damage is scored, sounded, shaken and shown as a
# floating number -- and then not applied. The point is to be able to sit in a
# pattern and read it properly rather than to trivialize the fight, so nothing
# else is touched: invulnerability frames, hitstop, knockback, the roll, the
# Archivist's own health and every timer behave exactly as they do in a real
# run. A fight reads it once at construction and can toggle it live (G, dev
# builds only), and the HUD says so on screen the whole time it is on.
default inv_dev_godmode = False


init -8 python:
    def inv_godmode_on():
        return bool(config.developer and getattr(store, "inv_dev_godmode", False))

    def inv_toggle_godmode():
        if not config.developer:
            return
        store.inv_dev_godmode = not getattr(store, "inv_dev_godmode", False)
        renpy.restart_interaction()


# --- DEV LAUNCHER ------------------------------------------------------------
# Called by the Developer Date Jump menu. Sets the dev framing, runs the fight,
# tears the framing back down, and returns to whatever called it.
label archivist_invasion_dev(slug, start_open=False):
    if not inv_is_playable(slug):
        return

    $ inv_dev_test = True
    $ inv_active_slug = slug
    $ inv_dev_start_open = bool(start_open)
    $ inv_player = "YOU"

    stop music fadeout 0.5
    scene black with dissolve_scene_full

    call expression inv_archivist(slug)["label"] from _call_expression_1

    $ inv_dev_test = False
    $ inv_active_slug = None
    $ inv_dev_start_open = False
    scene black
    return
