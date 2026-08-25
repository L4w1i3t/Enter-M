# =============================================================================
# mc_gacha.rpy  --  THE PRIZE MACHINE (Arcade lobby)
# =============================================================================
#
# WHAT THIS FILE IS
#   The capsule machine the player feeds Matsucoins into, the pull maths behind
#   it, and the reveal. It also owns THE SHARED CARD FACE (screen mc_card_face
#   + the enter_m.mc_card shader), because this is where a card is drawn first
#   and biggest -- the binder in mc_collection.rpy uses the same widget, so a
#   card looks identical in the machine that gave it to you and the album it
#   ends up in.
#
# WHERE IT LIVES AND WHY
#   The Arcade lobby, not the Archive. A gachapon machine is a physical
#   coin-op object that stands next to cabinets, and the Arcade is already the
#   room with the coin-op language -- the main menu's Donate channel has said
#   "PUT A COIN IN THE SLOT" since long before this feature existed. So the
#   machine wears the hub's indigo/amber jewel-case palette and its shaders
#   (ArcadePanel / _arcade_mix / arcade_keycap_chip), and the COLLECTION goes
#   to the Archive instead, where the game's other collections already live.
#
# SHOWN AS A MODAL OVERLAY
#   Show("mc_gacha") over the still-shown hub, dismissed with Hide -- the same
#   arrangement cg_gallery and character_stories use over the Archive. It is
#   NOT `tag menu`: replacing the hub would tear down the screen the player
#   came from and the way back would have to be rebuilt.
#
# THE ODDS (all of it is in MC_RARITY in mc_cards.rpy plus the four numbers
# below, so tuning the machine never means reading this file's screens)
#   R 70 / SR 25 / SSR 5, a guaranteed SR-or-better in every ten-pull, and a
#   hard pity that forces an SSR on the 50th pull without one. Duplicates
#   convert to coins rather than being lost, at well under the price of the
#   pull that produced them.
#
# SHADERS
#   Registered at init -10 like the Arcade's own three, and for the same
#   reasons: a shader only engages via the mesh/model path, so every factory
#   sets `mesh True` on a Transform whose xysize defines u_model_size, over an
#   OPAQUE base -- a transparent base is culled before the shader can run.
#   Registration happens in `init python`, which does NOT re-run on hot reload:
#   editing the GLSL below needs a FULL restart, not a Shift+R.
# =============================================================================

# --- pull configuration ------------------------------------------------------
define MC_COST_SINGLE = 100
define MC_COST_TEN = 1000
define MC_TEN_COUNT = 10
# Pulls without an SSR before one is forced. Counted in persistent.mc_pity.
define MC_PITY_HARD = 50

init -10 python:
    def _mc_register_shaders():

        # ---- card: the card face -------------------------------------------
        # Takes the child (the framed art) and makes a trading card of it:
        # rounded corners, a rarity edge ring, a top gloss, an inner vignette,
        # a dimming pass for cards the player does not own yet (u_locked), and
        # the SSR treatment -- a prismatic band travelling across the face,
        # positioned by u_sweep.
        #
        # u_sweep is ATL-interpolated, NOT keyed to u_time, which is the same
        # decision (and the same measured reason) as the Arcade's cartridge
        # glint: a frame only exists if some displayable asked Matsu'Py to draw
        # it, nothing on a settled menu asks continuously, and a u_time-keyed
        # sweep therefore freezes solid for seconds at a time and then snaps.
        # A running `linear` requests a redraw every frame, so interpolating
        # u_sweep makes the holo pay for its own smoothness.
        renpy.register_shader("enter_m.mc_card", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_model_size;
            uniform float u_radius;
            uniform vec4 u_edge;
            uniform float u_locked;
            uniform float u_holo;
            uniform float u_sweep;
            uniform float u_flash;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float enterm_mc_rr(vec2 p, vec2 b, float r) {
                vec2 q = abs(p) - b + vec2(r);
                return min(max(q.x, q.y), 0.0) + length(max(q, 0.0)) - r;
            }
        """, fragment_300="""
            vec2 size = max(u_model_size, vec2(1.0));
            vec2 uv = v_tex_coord;
            vec2 p = uv * size - size * 0.5;
            vec2 halfb = size * 0.5;
            float rad = clamp(u_radius, 0.0, min(halfb.x, halfb.y));
            float d = enterm_mc_rr(p, halfb, rad);
            float aa = 1.25;
            float fill = 1.0 - smoothstep(0.0, aa, d);
            if (fill <= 0.0) {
                gl_FragColor = vec4(0.0);
                return;
            }

            vec4 src = texture2D(tex0, uv);
            vec3 col = src.rgb;
            float a = src.a;

            // Unowned: desaturate hard and sink it, so a locked slot is a
            // silhouette rather than a readable picture.
            if (u_locked > 0.0) {
                float g = dot(col, vec3(0.299, 0.587, 0.114));
                col = mix(col, vec3(g) * 0.30, u_locked);
            }

            // top gloss + inner vignette
            col += vec3(1.0) * smoothstep(0.42, 0.0, uv.y) * 0.055 * a;
            vec2 vv = (uv - vec2(0.5)) * vec2(1.05, 1.0);
            col *= 1.0 - smoothstep(0.42, 0.95, length(vv)) * 0.40;

            // SSR holo: a wide prismatic band riding the diagonal
            if (u_holo > 0.0) {
                float band = uv.x * 0.72 + uv.y * 0.28 - u_sweep;
                float g = exp(-band * band * 26.0);
                vec3 rainbow = 0.5 + 0.5 * cos(6.28318 * (vec3(0.0, 0.33, 0.67)
                                + (uv.x * 0.6 + uv.y * 0.4) * 1.6));
                col += rainbow * g * 0.42 * u_holo;
                col += vec3(1.0) * g * 0.10 * u_holo;
            }

            // reveal flash (ATL-driven, 1 -> 0 as the card lands)
            col += u_edge.rgb * u_flash;

            // rarity edge ring
            float bw = 3.0;
            float band2 = (1.0 - smoothstep(bw - aa, bw + aa, abs(d))) * step(d, 0.0);
            col = mix(col, u_edge.rgb, band2 * u_edge.a);
            a = mix(a, max(a, u_edge.a), band2);

            a *= fill;
            gl_FragColor = vec4(clamp(col, 0.0, 1.0) * a, a);
        """)

    _mc_register_shaders()


init -3 python:
    import random as _mc_random

    # -------------------------------------------------------------------------
    # DISPLAYABLE FACTORIES
    # -------------------------------------------------------------------------
    # The machine is a SPRITE, not geometry. It used to be drawn in code -- an
    # SDF glass dome, a seeded field of capsule circles, a red body built out of
    # rounded panels -- and all of that is gone, because a drawn machine is a
    # drawing of a machine and this is the actual object.
    MC_MACHINE_PATH = "addons/Matsucoin Currency and Gacha/gachamachine.png"
    MC_MACHINE_W, MC_MACHINE_H = 218, 312

    def McMachine(height=452):
        """The cabinet at a given pixel HEIGHT, aspect preserved."""
        h = int(height)
        w = int(round(MC_MACHINE_W * (float(h) / MC_MACHINE_H)))
        return Transform(MC_MACHINE_PATH, xysize=(w, h), fit="contain")

    def McCapsule(size, top, bottom):
        """A capsule. A circle is just a rounded panel whose radius is half its
        size, so this rides the Arcade's own panel shader instead of adding
        another one. Still used by the reveal, for a card that has not landed
        yet -- it is the capsule the card is notionally still inside."""
        s = int(size)
        return ArcadePanel(s, s, top=top, bottom=bottom, radius=s / 2.0)

    # -------------------------------------------------------------------------
    # PULL RUNTIME
    # The results of the pull being revealed. NoRollback and created at init for
    # the same reason the toast queues are: a `default` store variable would be
    # rolled back with the game and pickled into every save -- and this one
    # would be holding McCard objects, which is exactly the shape that made the
    # achievement queue crash saves on pickling before it was moved off-store.
    # -------------------------------------------------------------------------
    class _McPullRuntime(NoRollback):
        def __init__(self):
            self.results = []    # [(McCard, is_new, refund)]
            self.spent = 0
            self.refunded = 0

        @property
        def best(self):
            """The rarest thing in the batch -- what the reveal's flash, sound
            and banner are keyed to."""
            rank = {r: i for i, r in enumerate(MC_RARITY_ORDER)}
            best = "r"
            for card, _new, _ref in self.results:
                if rank.get(card.rarity, 0) > rank.get(best, 0):
                    best = card.rarity
            return best

        @property
        def new_count(self):
            return sum(1 for _c, is_new, _r in self.results if is_new)

    _mc_pull_rt = _McPullRuntime()

    # -------------------------------------------------------------------------
    # THE PULL
    # -------------------------------------------------------------------------
    def _mc_roll_rarity():
        """One rarity roll, honouring (and advancing) hard pity.

        Pity counts pulls since the last SSR. When the NEXT pull would be the
        MC_PITY_HARD'th without one, it is forced -- so the guarantee is "an SSR
        at least every 50 pulls", not "on the 51st"."""
        _mc_ensure_cards()
        pity = persistent.mc_pity

        if pity + 1 >= MC_PITY_HARD:
            rarity = "ssr"
        else:
            roll = _mc_random.random() * 100.0
            ssr_w = MC_RARITY["ssr"]["weight"]
            sr_w = MC_RARITY["sr"]["weight"]
            if roll < ssr_w:
                rarity = "ssr"
            elif roll < ssr_w + sr_w:
                rarity = "sr"
            else:
                rarity = "r"

        persistent.mc_pity = 0 if rarity == "ssr" else pity + 1
        return rarity

    def mc_pull(count):
        """Spend, roll `count` cards, bank them, and stage the reveal.

        Returns True if the pull happened. The caller is expected to have
        checked affordability for the button state, but this re-checks anyway --
        a screen action can fire on a stale frame, and the check is one integer
        comparison against the double-spend it prevents."""
        cost = MC_COST_TEN if count >= MC_TEN_COUNT else MC_COST_SINGLE
        if not mc_spend(cost):
            return False

        _mc_ensure_cards()
        rarities = [_mc_roll_rarity() for _ in range(count)]

        # TEN-PULL FLOOR: every ten-pull owes at least one SR or better. Applied
        # to the LAST slot so the reveal's running order still has somewhere to
        # go, and only when the batch genuinely came up empty.
        if count >= MC_TEN_COUNT and not any(r in ("sr", "ssr") for r in rarities):
            rarities[-1] = "sr"

        results = []
        refunded = 0
        for rarity in rarities:
            card = _mc_random.choice(MC_CARDS_BY_RARITY[rarity])
            is_new = mc_card_add(card.id)
            refund = 0 if is_new else card.refund
            if refund:
                # toast=False: a ten-pull would otherwise fire ten coin toasts
                # over the reveal it is interrupting. The refund is reported on
                # the reveal card and folded into the total below.
                refunded += mc_award(refund, "DUPLICATE", toast=False, save=False)
            results.append((card, is_new, refund))

        persistent.mc_pulls_total += count

        _mc_pull_rt.results = results
        _mc_pull_rt.spent = cost
        _mc_pull_rt.refunded = refunded

        try:
            renpy.save_persistent()
        except Exception:
            pass
        return True

    def mc_pull_and_show(count):
        """Button action: pull, then open the reveal. A failed pull (not enough
        coins) does nothing rather than opening an empty reveal.

        NO click sound here. Every button that calls this already carries
        `activate_sound gui.activate_sound` through its style, so playing one
        here as well was the doubled UI click."""
        if mc_pull(count):
            renpy.show_screen("mc_reveal")
        renpy.restart_interaction()
        return None

    def _mc_reveal_sound(rarity):
        # One vocabulary with the coin toast (MC_SFX in matsucoin.rpy): a soft
        # sparkle for a common, a bonus chime for an SR, and the spell-card
        # capture cue for an SSR.
        mc_se(rarity if rarity in MC_SFX else "r")

    def mc_reveal_step(shown):
        """Called by the reveal's timer as each card lands: plays that card's
        rarity sting. Returns None -- a screen action that returns a value ends
        the interaction and bubbles it up like Return()."""
        results = _mc_pull_rt.results
        if 0 < shown <= len(results):
            _mc_reveal_sound(results[shown - 1][0].rarity)
        return None

    # Odds, formatted for the rates panel. Read from MC_RARITY so the panel can
    # never disagree with the machine -- a hand-typed "5%" that survives a
    # rebalance is a lie the player has no way to catch.
    def mc_rate_rows():
        return [
            (MC_RARITY[r]["label"], "%.4g%%" % MC_RARITY[r]["weight"],
            MC_RARITY[r]["color"], len(MC_CARDS_BY_RARITY[r]))
            for r in reversed(MC_RARITY_ORDER)
        ]


# =============================================================================
# THE SHARED CARD FACE
# Used by the reveal below AND by the binder in mc_collection.rpy.
#   card     : an McCard
#   w, h     : face size in px
#   locked   : draw it as an unowned silhouette
#   holo     : 0..1 prismatic strength (SSR cards pass 1.0)
#   flash    : 0..1 reveal blowout, driven by the caller's ATL
# =============================================================================
# Shader uniforms are ATL properties, NOT `add` statement properties -- an
# inline `add art: u_radius 10` does not parse. So the card's whole shader setup
# is a parameterised transform applied with `at`, which is the same shape the
# Arcade's cartridge uses (arcade_cart_fx).
transform mc_card_fx(radius=10.0, edge=(1.0, 1.0, 1.0, 1.0), locked=0.0):
    mesh True
    shader "enter_m.mc_card"
    u_radius radius
    u_edge edge
    u_locked locked
    u_holo 0.0
    u_sweep 0.0
    u_flash 0.0

# The SSR variant, with the prismatic band's travel folded in. ATL-interpolated
# (never u_time) -- see the note on the shader above. The pause is deliberately
# cheap: nothing moves during it, so no redraws are requested and a settled
# binder full of SSRs still idles at zero cost.
transform mc_card_fx_holo(radius=10.0, edge=(1.0, 1.0, 1.0, 1.0), holo=1.0):
    mesh True
    shader "enter_m.mc_card"
    u_radius radius
    u_edge edge
    u_locked 0.0
    u_holo holo
    u_flash 0.0
    block:
        u_sweep -0.35
        linear 1.6 u_sweep 1.35
        pause 2.4
        repeat

screen mc_card_face(card, w, h, locked=False, holo=None, radius=10.0):
    $ _mcf_holo = (1.0 if card.rarity == "ssr" else 0.0) if holo is None else holo
    $ _mcf_edge = enter_m_rgba("#3a4152" if locked else card.color)

    fixed:
        xysize (w, h)

        # No separate backing Solid: mc_card_art already composites the art onto
        # an opaque base of exactly (w, h). That is what keeps every card face
        # the same size AND what stops the mesh being culled for transparency --
        # see the contract note on mc_card_art in mc_cards.rpy.
        if _mcf_holo > 0.0 and not locked:
            add mc_card_art(card, w, h) at mc_card_fx_holo(radius, _mcf_edge, _mcf_holo)
        else:
            add mc_card_art(card, w, h) at mc_card_fx(radius, _mcf_edge, (1.0 if locked else 0.0))

        # Rarity chip, bottom-left of the face. Inset past the corner radius so
        # it does not overhang the rounded edge it is sitting on.
        #
        # DARK plate, BRIGHT tier ink -- not a tier-coloured plate with
        # near-black ink. The old way put a small bold glyph in #0d0a16 on a
        # mid-tone fill and it was barely readable at R, where the fill is a
        # muted steel; and it sat on top of card art, which the fill only ever
        # partly covers. A dark plate is legible over any artwork, and moving
        # the tier's identity into the INK keeps the badge tier-coded while
        # raising R's contrast from about 4.5:1 to roughly 9:1.
        frame:
            background Solid("#0b0818ee")
            padding (7, 2)
            xpos (int(radius) + 3)
            yanchor 1.0
            ypos (h - int(radius) - 3)
            text (card.tier["label"]):
                style "mc_rarity_chip"
                color ("#5c6577" if locked else card.glow)


# =============================================================================
# THE MACHINE
# =============================================================================
transform mc_panel_in(delay=0.0, yoff=26):
    subpixel True
    alpha 0.0
    yoffset yoff
    pause delay
    easeout 0.42 alpha 1.0 yoffset 0

transform mc_machine_idle:
    # The cabinet breathing, and rising to meet the pointer. It lives directly
    # inside the machine button, which is what gets it hover/idle dispatch --
    # an intermediate container would swallow those events (the same
    # button-direct-child rule the Arcade's cartridges follow).
    subpixel True
    on idle:
        block:
            easeout 1.8 yoffset -3
            easein 1.8 yoffset 0
            repeat
    on hover:
        easeout 0.25 yoffset -10 zoom 1.03

screen mc_gacha():
    modal True
    zorder 60

    # Coins earned since the hub was last synced (a fight that just paid out,
    # an achievement earned on the way here) land before the balance is drawn.
    on "show" action Function(mc_refresh)

    key "game_menu" action [Function(renpy.play, audio.uiselect, channel="sound"), Hide("mc_gacha")]
    key "K_ESCAPE" action [Function(renpy.play, audio.uiselect, channel="sound"), Hide("mc_gacha")]

    python:
        _mcg_owned, _mcg_total = mc_collection_counts()
        _mcg_single_ok = mc_can_afford(MC_COST_SINGLE)
        _mcg_ten_ok = mc_can_afford(MC_COST_TEN)
        _mcg_pity = persistent.mc_pity
        _mcg_pity_left = max(0, MC_PITY_HARD - _mcg_pity)

    add ArcadeField("#ffb454")
    add Solid("#0a0713a8")

    frame:
        background ArcadePanel(1188, 656, top="#221a4ae8", bottom="#0f0a20f2",
                            radius=22, border=1.5, border_color="#ffb45455")
        xalign 0.5
        yalign 0.5
        xysize (1188, 656)
        padding (30, 22)

        vbox:
            spacing 14

            # --- header -----------------------------------------------------
            fixed:
                xsize 1128
                ysize 46

                hbox:
                    spacing 14
                    yalign 0.5
                    text "PRIZE MACHINE" style "mc_title" yalign 0.5
                    # Badge: the plate and its label are stacked in one fixed so
                    # the text is centred ON the plate. Setting the label's
                    # xoffset by hand to walk it back over the plate breaks the
                    # moment either the copy or the plate width changes.
                    fixed:
                        xysize (150, 24)
                        yalign 0.5
                        add ArcadePanel(150, 24, top="#2b2250", bottom="#191330",
                                        radius=12, border=1.0, border_color="#ffb45488")
                        text "MATSUCOM" style "mc_title_sub" align (0.5, 0.5)

                # Wallet, right-aligned. A `fixed` with xanchor 1.0, not an
                # hbox with a greedy null -- giving a box an explicit xsize
                # stops it packing children left and floats them toward the
                # middle instead (measured; see the note on archive_readout).
                fixed:
                    xsize 1128
                    ysize 46

                    # Dev-only coin bench. Sits left of the wallet so it never
                    # displaces it. Hidden entirely in release builds.
                    if config.developer:
                        textbutton "DEV":
                            style "mc_dev_pill"
                            xanchor 1.0
                            xpos 1056
                            yalign 0.5
                            action Show("mc_dev_shop")

                    frame:
                        background ArcadePanel(210, 42, top="#2b2250", bottom="#171130",
                                            radius=11, border=1.0, border_color="#ffb45466")
                        xanchor 1.0
                        xpos 1128
                        yalign 0.5
                        xysize (210, 42)
                        padding (0, 0)
                        hbox:
                            align (0.5, 0.5)
                            use mc_balance_chip(22)

            add ArcadePanel(1128, 3, top="#ffb454aa", bottom="#ffb45400",
                            radius=1.5, horiz=True)

            hbox:
                spacing 30

                # --- LEFT: the cabinet --------------------------------------
                # The machine is itself the single-pull button. A gachapon
                # machine you cannot touch is a picture of one, and the pointer
                # lifting it is the whole tell that it is operable -- the PULL
                # plates on the right stay as the explicit, labelled route.
                fixed:
                    xysize (440, 512)
                    at mc_panel_in(0.05)

                    add ArcadePanel(440, 512, top="#2a2150e0", bottom="#150e2af0",
                                    radius=18, border=1.0, border_color="#ffb45433")

                    # Warm pool under the cabinet so it is standing on something
                    # rather than floating in the alcove.
                    add ArcadePanel(300, 46, top="#ffb45420", bottom="#ffb45400",
                                    radius=23):
                        align (0.5, 0.5)
                        yoffset 196

                    button:
                        style "mc_machine_button"
                        xysize (440, 512)
                        action (Function(mc_pull_and_show, 1) if _mcg_single_ok else NullAction())
                        hover_sound gui.hover_sound

                        # Direct child of the button, so hover/idle reach it.
                        add McMachine(452):
                            align (0.5, 0.5)
                            yoffset -14
                            at mc_machine_idle

                    text ("TURN THE CRANK  //  %s" % mc_num(MC_COST_SINGLE)
                        if _mcg_single_ok else "OUT OF COINS"):
                        style "mc_machine_label"
                        align (0.5, 1.0)
                        yoffset -16

                # --- RIGHT: readouts + controls -----------------------------
                vbox:
                    spacing 12
                    at mc_panel_in(0.12)

                    # collection census
                    frame:
                        background ArcadePanel(618, 92, top="#241c4ce0", bottom="#150f2ce8",
                                            radius=13, border=1.0, border_color="#ffffff14")
                        xysize (618, 92)
                        padding (20, 14)

                        vbox:
                            spacing 8
                            hbox:
                                spacing 10
                                text "COLLECTION" style "mc_kicker" yalign 0.5
                                text ("%d / %d" % (_mcg_owned, _mcg_total)):
                                    style "mc_readout"
                                    yalign 0.5
                            fixed:
                                xysize (578, 8)
                                add ArcadePanel(578, 8, top="#ffffff12", bottom="#ffffff0c", radius=4)
                                if _mcg_owned:
                                    add ArcadePanel(max(8, int(578.0 * _mcg_owned / max(_mcg_total, 1))), 8,
                                                    top="#ffd98a", bottom="#ffb454", radius=4)

                    # odds + pity
                    frame:
                        background ArcadePanel(618, 168, top="#241c4ce0", bottom="#150f2ce8",
                                            radius=13, border=1.0, border_color="#ffffff14")
                        xysize (618, 168)
                        padding (20, 14)

                        vbox:
                            spacing 9

                            text "ODDS PER PULL" style "mc_kicker"

                            for _rl, _rp, _rc, _rn in mc_rate_rows():
                                hbox:
                                    spacing 10
                                    ysize 22
                                    add Solid(_rc) xysize (4, 15) yalign 0.5
                                    text _rl:
                                        style "mc_rate_label"
                                        color _rc
                                        yalign 0.5
                                    text _rp style "mc_rate_value" yalign 0.5
                                    text ("%d cards" % _rn) style "mc_rate_note" yalign 0.5

                            null height 1
                            text ("Guaranteed SSR within %d more pull%s."
                                % (_mcg_pity_left, "" if _mcg_pity_left == 1 else "s")):
                                style "mc_rate_note"

                    # pull buttons
                    hbox:
                        spacing 14

                        button:
                            style "mc_pull_button"
                            xysize (302, 92)
                            action (Function(mc_pull_and_show, 1) if _mcg_single_ok else NullAction())
                            background ArcadePanel(302, 92, top=("#3a2c5e" if _mcg_single_ok else "#241f38"),
                                                bottom=("#1d1636" if _mcg_single_ok else "#171327"),
                                                radius=12, border=1.0,
                                                border_color=("#ffb45499" if _mcg_single_ok else "#4a4460"))
                            hover_background ArcadePanel(302, 92, top="#584077", bottom="#2c2049",
                                                        radius=12, border=2.0, border_color="#ffd98a")
                            hover_sound gui.hover_sound

                            vbox:
                                align (0.5, 0.5)
                                spacing 5
                                text "SINGLE PULL":
                                    style "mc_pull_label"
                                    color ("#fbf6ee" if _mcg_single_ok else "#7d7595")
                                    xalign 0.5
                                hbox:
                                    spacing 7
                                    xalign 0.5
                                    add MatsucoinIcon(18) yalign 0.5
                                    text mc_num(MC_COST_SINGLE):
                                        style "mc_pull_cost"
                                        color ("#ffd98a" if _mcg_single_ok else "#6f6889")
                                        yalign 0.5

                        button:
                            style "mc_pull_button"
                            xysize (302, 92)
                            action (Function(mc_pull_and_show, MC_TEN_COUNT) if _mcg_ten_ok else NullAction())
                            background ArcadePanel(302, 92, top=("#5c3f2a" if _mcg_ten_ok else "#241f38"),
                                                bottom=("#2e1f1c" if _mcg_ten_ok else "#171327"),
                                                radius=12, border=1.0,
                                                border_color=("#ffb454cc" if _mcg_ten_ok else "#4a4460"))
                            hover_background ArcadePanel(302, 92, top="#8a5c35", bottom="#442a24",
                                                        radius=12, border=2.0, border_color="#ffe6a8")
                            hover_sound gui.hover_sound

                            vbox:
                                align (0.5, 0.5)
                                spacing 5
                                text "TEN-PULL":
                                    style "mc_pull_label"
                                    color ("#fbf6ee" if _mcg_ten_ok else "#7d7595")
                                    xalign 0.5
                                hbox:
                                    spacing 7
                                    xalign 0.5
                                    add MatsucoinIcon(18) yalign 0.5
                                    text mc_num(MC_COST_TEN):
                                        style "mc_pull_cost"
                                        color ("#ffd98a" if _mcg_ten_ok else "#6f6889")
                                        yalign 0.5

                    if not _mcg_single_ok:
                        text "Not enough Matsucoins. Play something.":
                            style "mc_rate_note"
                            color "#e0919e"
                    else:
                        text "One SR or better guaranteed in every ten-pull.":
                            style "mc_rate_note"

                    # Lifetime ledger. Balance alone is a bad readout for a
                    # currency you are meant to spend -- a player who has just
                    # emptied the wallet on a ten-pull has not earned nothing,
                    # and this is where that is visible.
                    frame:
                        background ArcadePanel(618, 62, top="#241c4ce0", bottom="#150f2ce8",
                                            radius=13, border=1.0, border_color="#ffffff14")
                        xysize (618, 62)
                        padding (20, 12)

                        hbox:
                            spacing 0
                            yalign 0.5

                            # `coin` is False for PULLS -- it is a count of
                            # attempts, not an amount of money, and stamping the
                            # currency glyph on it would read as a third balance.
                            for _wl, _wv, _wcoin in (("TOTAL EARNED", persistent.mc_lifetime, True),
                                                    ("SPENT", persistent.mc_spent, True),
                                                    ("PULLS", persistent.mc_pulls_total, False)):
                                vbox:
                                    xsize 192
                                    spacing 3
                                    text _wl style "mc_kicker" size 10
                                    hbox:
                                        spacing 6
                                        if _wcoin:
                                            add MatsucoinIcon(14) yalign 0.5
                                        text mc_num(_wv) style "mc_readout" size 16 yalign 0.5

            # --- footer -----------------------------------------------------
            fixed:
                xsize 1128
                ysize 26

                hbox:
                    spacing 9
                    yalign 0.5
                    use arcade_keycap_chip("ESC")
                    text "BACK TO THE FLOOR" style "mc_footer" yalign 0.5
                    text "//" style "mc_footer_sep" yalign 0.5
                    text "COLLECTION LIVES IN THE ARCHIVE" style "mc_footer" yalign 0.5

                text ("PULLS %s  //  %d/%d COLLECTED" % (mc_num(persistent.mc_pulls_total), _mcg_owned, _mcg_total)):
                    style "mc_footer"
                    xanchor 1.0
                    xpos 1128
                    yalign 0.5


# =============================================================================
# DEV COIN BENCH  (config.developer only; opened from the DEV pill on the
# machine's header, and mirrored by console calls -- see matsucoin.rpy)
#
# Grants go straight to the balance rather than through mc_award, so a dev top-up
# does not inflate TOTAL EARNED or break the lifetime == balance + spent
# invariant. The wallet is hard-capped at MC_BALANCE_CAP; MAX sets it there.
# =============================================================================
screen mc_dev_shop():
    modal True
    zorder 80

    key "game_menu" action Hide("mc_dev_shop")
    key "K_ESCAPE" action Hide("mc_dev_shop")

    add Solid("#05030cdd")
    dismiss action Hide("mc_dev_shop")

    frame:
        background ArcadePanel(560, 400, top="#241c4cf5", bottom="#120c24f8",
                            radius=18, border=1.5, border_color="#ffb45488")
        align (0.5, 0.5)
        xysize (560, 400)
        padding (28, 22)
        at arcade_pop

        # Every row is measured against the 504px content width (560 less the
        # 2x28 padding). The grant row is five buttons, so those use the compact
        # 94px plate: 5*94 + 4*8 = 502. Full-width plates in that row overflowed
        # the panel and pushed Close off the bottom.
        vbox:
            spacing 10
            xfill True

            text "DEV // COIN BENCH" style "mc_kicker" size 14

            hbox:
                spacing 10
                yalign 0.5
                add MatsucoinIcon(24) yalign 0.5
                text mc_num(mc_balance()) style "mc_readout" size 30 yalign 0.5
                text ("/ %s" % mc_num(MC_BALANCE_CAP)):
                    style "mc_rate_note"
                    yalign 0.5

            add ArcadePanel(504, 2, top="#ffb45466", bottom="#ffb45400",
                            radius=1, horiz=True)

            text "GRANT" style "mc_kicker" size 11

            hbox:
                spacing 8
                for _dl, _dv in (("+100", 100), ("+1K", 1000), ("+10K", 10000)):
                    textbutton _dl:
                        style "mc_dev_button_sm"
                        action Function(mc_dev_give, _dv)
                textbutton "MAX":
                    style "mc_dev_button_sm"
                    action Function(mc_dev_fill)
                textbutton "ZERO":
                    style "mc_dev_button_sm"
                    action Function(mc_dev_reset)

            text "COLLECTION" style "mc_kicker" size 11

            hbox:
                spacing 10
                textbutton "GRANT ALL CARDS":
                    style "mc_dev_button"
                    action Function(mc_dev_grant_all)
                textbutton "CLEAR CARDS":
                    style "mc_dev_button"
                    action Function(mc_dev_clear_cards)

            text "PAYOUT LEDGER" style "mc_kicker" size 11

            hbox:
                spacing 10
                # Wipes persistent.mc_paid_keys, so every derived payout
                # (achievements, side stories, CGs...) becomes claimable again
                # and the next interaction re-pays the lot. For testing the
                # EARNING path rather than the machine.
                textbutton "RESET LEDGER":
                    style "mc_dev_button"
                    action Function(mc_dev_reset, keep_ledger=False)
                textbutton _("Close"):
                    style "mc_dev_button"
                    action Hide("mc_dev_shop")


# =============================================================================
# THE REVEAL
# One screen for both pull sizes: a single pull is a 1-card grid. Cards land one
# at a time on a timer; clicking anywhere lands the rest immediately, so nobody
# is ever held hostage by an animation they have seen a hundred times.
# =============================================================================
transform mc_card_land(delay=0.0):
    subpixel True
    alpha 0.0
    zoom 0.82
    yoffset 18
    pause delay
    parallel:
        easeout 0.26 alpha 1.0
    parallel:
        easein_back 0.34 zoom 1.0 yoffset 0

transform mc_reveal_glow:
    subpixel True
    alpha 0.0
    easeout 0.20 alpha 0.55
    easein 0.75 alpha 0.0

screen mc_reveal():
    modal True
    zorder 70

    # How many cards have landed. The timer walks it up; a click completes it.
    default shown = 0

    python:
        _mcr_results = _mc_pull_rt.results
        _mcr_count = len(_mcr_results)
        _mcr_done = (shown >= _mcr_count)
        _mcr_best = _mc_pull_rt.best
        _mcr_tier = MC_RARITY.get(_mcr_best, MC_RARITY["r"])
        # A single pull gets one big card; a ten-pull gets a 5x2 wall.
        # Both grid dimensions are computed HERE rather than inline: `grid` takes
        # two bare positional arguments and does not accept a parenthesised
        # expression for either of them.
        _mcr_single = (_mcr_count == 1)
        _mcr_cw, _mcr_ch = ((300, 420) if _mcr_single else (168, 236))
        _mcr_cols = 1 if _mcr_single else 5
        _mcr_grid_rows = 1 if _mcr_single else 2
        # One action for every way out of this screen -- click, Enter, Escape --
        # so the reveal cannot be in a state where one of them works and another
        # silently does nothing. Mid-reveal it lands the rest; once everything
        # is down it closes.
        # Skipping lands every remaining card at once, so it rings the BEST
        # rarity in the batch rather than nothing -- a skip should still tell
        # you what you got.
        _mcr_action = (
            [Function(mc_se, "coin", 0.7), Hide("mc_reveal")]
            if _mcr_done
            else [Function(mc_se, _mcr_best), SetScreenVariable("shown", _mcr_count)]
        )

    add Solid("#05030ce8")
    add ArcadePanel(1280, 720, top=(_mcr_tier["color"] + "1c"),
                    bottom="#00000000", radius=0)

    # Land everything on a click, then close on the next one.
    #
    # `dismiss`, NOT a full-screen `button`. A button with xfill/yfill, no child
    # and `background None` renders no hit area, so the click target was dead --
    # which is why CLICK TO CLOSE did nothing and only the timer ever advanced
    # the reveal. dismiss is the engine's own click-anywhere primitive
    # (renpy.display.behavior.DismissBehavior): it registers an unbounded focus,
    # so it catches a click at any coordinate, and it works under `modal True`.
    dismiss action _mcr_action

    key "K_ESCAPE" action _mcr_action
    key "game_menu" action _mcr_action

    if not _mcr_done:
        timer 0.16 repeat True action [
            SetScreenVariable("shown", min(shown + 1, _mcr_count)),
            Function(mc_reveal_step, shown + 1),
        ]

    vbox:
        align (0.5, 0.5)
        spacing 20

        # Banner keyed to the best thing in the batch.
        if _mcr_done and _mcr_best != "r":
            text (("SSR" if _mcr_best == "ssr" else "SR") + "  //  " + _mcr_tier["full"]):
                style "mc_reveal_banner"
                color _mcr_tier["glow"]
                xalign 0.5
                at mc_panel_in(0.0, 10)

        grid _mcr_cols _mcr_grid_rows:
            spacing 14
            xalign 0.5

            for _i, (_card, _is_new, _refund) in enumerate(_mcr_results):
                # The cell reserves the card's height plus a fixed caption well.
                # 56, not 46: a two-line name ("The Unwritten Act // Encore")
                # plus its NEW/DUPLICATE line runs past 46 and spilled into the
                # grid gap above the next row.
                fixed:
                    xysize (_mcr_cw, _mcr_ch + 56)

                    if _i < shown:
                        fixed:
                            xysize (_mcr_cw, _mcr_ch)
                            at mc_card_land(0.0)

                            # rarity bloom behind the card as it lands
                            add ArcadePanel(_mcr_cw + 26, _mcr_ch + 26,
                                            top=(_card.glow + "88"), bottom=(_card.color + "00"),
                                            radius=18):
                                align (0.5, 0.5)
                                at mc_reveal_glow

                            use mc_card_face(_card, _mcr_cw, _mcr_ch)

                        # name + NEW / duplicate refund, under the card.
                        # TOP-anchored 10px below the card rather than bottom-
                        # anchored to the cell, so the gap is guaranteed and the
                        # caption grows downward into the well instead of upward
                        # into the art.
                        vbox:
                            ypos (_mcr_ch + 10)
                            xsize _mcr_cw
                            spacing 1

                            text _card.name:
                                style "mc_reveal_name"
                                xalign 0.5
                                text_align 0.5
                                size (17 if _mcr_single else 12)

                            if _is_new:
                                text "NEW" style "mc_reveal_new" xalign 0.5
                            else:
                                hbox:
                                    spacing 4
                                    xalign 0.5
                                    text "DUPLICATE  +" style "mc_reveal_dupe" yalign 0.5
                                    add MatsucoinIcon(11) yalign 0.5
                                    text str(_refund) style "mc_reveal_dupe" yalign 0.5
                    else:
                        # Not landed yet: the capsule it is still inside.
                        add McCapsule(int(_mcr_cw * 0.42), "#4a4270", "#241d44"):
                            align (0.5, 0.42)

        if _mcr_done:
            hbox:
                xalign 0.5
                spacing 16
                at mc_panel_in(0.1, 8)

                if _mc_pull_rt.refunded:
                    hbox:
                        spacing 6
                        yalign 0.5
                        text "CONVERTED" style "mc_reveal_foot" yalign 0.5
                        add MatsucoinIcon(13) yalign 0.5
                        text ("+%s" % mc_num(_mc_pull_rt.refunded)):
                            style "mc_reveal_foot"
                            color "#ffd98a"
                            yalign 0.5
                    text "//" style "mc_footer_sep" yalign 0.5

                text ("%d NEW" % _mc_pull_rt.new_count) style "mc_reveal_foot" yalign 0.5
                text "//" style "mc_footer_sep" yalign 0.5
                text "CLICK TO CLOSE" style "mc_reveal_foot" yalign 0.5
        else:
            text "CLICK TO SKIP" style "mc_reveal_foot" xalign 0.5


# =============================================================================
# STYLES  (the Arcade's palette: indigo field, warm off-white ink, amber accent)
# =============================================================================
style mc_title:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 34
    color "#f7f0e6"
    bold True
    outlines [(2, "#0b0818", 0, 0), (2, "#ffb45499", 1, 1)]

style mc_title_sub is gui_text:
    font gui.interface_font
    size 12
    color "#ffd98a"
    kerning 2.0
    bold True

style mc_kicker is gui_text:
    font gui.interface_font
    size 12
    color "#ffb454"
    kerning 2.0
    bold True
    outlines [(1, "#0b0818", 0, 0)]

style mc_readout is gui_text:
    font gui.interface_font
    size 19
    color "#f7f0e6"
    bold True
    outlines [(1, "#0b0818", 0, 0)]

style mc_rate_label is gui_text:
    font gui.interface_font
    size 15
    bold True
    outlines [(1, "#0b0818", 0, 0)]

style mc_rate_value is gui_text:
    font gui.interface_font
    size 15
    color "#f7f0e6"
    outlines [(1, "#0b0818", 0, 0)]

style mc_rate_note is gui_text:
    font gui.interface_font
    size 12
    color "#a99fc4"
    outlines [(1, "#0b0818", 0, 0)]

style mc_machine_label is gui_text:
    font gui.interface_font
    size 11
    color "#ffd98acc"
    kerning 1.5
    bold True
    outlines [(1, "#0b0818", 0, 0)]

style mc_machine_button:
    background None
    hover_background None
    padding (0, 0)
    activate_sound gui.activate_sound

style mc_dev_pill:
    background ArcadePanel(64, 24, top="#5c3f2a", bottom="#2e1f1c", radius=12, border=1.0, border_color="#ffb45499")
    hover_background ArcadePanel(64, 24, top="#8a5c35", bottom="#442a24", radius=12, border=2.0, border_color="#ffe6a8")
    xysize (64, 24)
    padding (0, 0)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style mc_dev_pill_text:
    font gui.interface_font
    size 11
    color "#ffe6a8"
    bold True
    kerning 1.5
    xalign 0.5
    yalign 0.5

style mc_dev_button:
    background ArcadePanel(150, 38, top="#2a2148", bottom="#1c1636", radius=9, border=1.0, border_color="#ffffff22")
    hover_background ArcadePanel(150, 38, top="#43336a", bottom="#2a1f4a", radius=9, border=2.0, border_color="#ffd98a")
    xysize (150, 38)
    padding (0, 0)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style mc_dev_button_text:
    font gui.interface_font
    size 13
    color "#f7f0e6"
    bold True
    xalign 0.5
    yalign 0.5

style mc_dev_button_sm is mc_dev_button:
    background ArcadePanel(94, 38, top="#2a2148", bottom="#1c1636", radius=9, border=1.0, border_color="#ffffff22")
    hover_background ArcadePanel(94, 38, top="#43336a", bottom="#2a1f4a", radius=9, border=2.0, border_color="#ffd98a")
    xysize (94, 38)

style mc_dev_button_sm_text is mc_dev_button_text

style mc_pull_button:
    padding (0, 0)
    activate_sound gui.activate_sound

style mc_pull_label:
    font gui.interface_font
    size 21
    bold True
    outlines [(2, "#0b0818", 0, 0)]

style mc_pull_cost:
    font gui.interface_font
    size 17
    bold True
    outlines [(1, "#0b0818", 0, 0)]

style mc_footer is gui_text:
    font gui.interface_font
    size 11
    color "#8f86a8"
    kerning 1.0

style mc_footer_sep is gui_text:
    font gui.interface_font
    size 11
    color "#4e4767"

style mc_rarity_chip:
    font gui.interface_font
    size 11
    color "#a9b8cf"
    bold True
    kerning 1.0
    outlines [(1, "#02040b", 0, 0)]

style mc_reveal_banner:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 30
    bold True
    kerning 3.0
    outlines [(2, "#0b0818", 0, 0)]

style mc_reveal_name is gui_text:
    font gui.interface_font
    color "#f7f0e6"
    bold True
    outlines [(1, "#0b0818", 0, 0)]

style mc_reveal_new is gui_text:
    font gui.interface_font
    size 11
    color "#7ce0a8"
    bold True
    kerning 1.5
    outlines [(1, "#0b0818", 0, 0)]

style mc_reveal_dupe is gui_text:
    font gui.interface_font
    size 11
    color "#8f86a8"
    outlines [(1, "#0b0818", 0, 0)]

style mc_reveal_foot is gui_text:
    font gui.interface_font
    size 13
    color "#c9c0dc"
    kerning 1.0
    outlines [(1, "#0b0818", 0, 0)]
