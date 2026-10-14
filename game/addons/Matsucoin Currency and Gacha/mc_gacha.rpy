# Arcade prize machine, pull transaction and shared mc_card_face rendering.
# Show("mc_gacha") overlays the Arcade hub; Hide returns to the existing hub.
# MC_RARITY (mc_cards.rpy) and pull constants below own odds, ten-pull guarantees,
# pity and duplicate refunds. Card IDs/ownership are shared with the Archive binder.
# Shader factories use opaque mesh bases at a known size; cinematic reveal effects
# live in mc_reveal_fx.rpy. Preserve transaction atomicity when changing UI actions.

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

            // SSR foil: a prismatic band riding the printed shell, not the
            // illustration. Sweeping the whole portrait looked like a filter
            // laid over an image; confining it to the rails/footer makes the
            // card itself the holographic object.
            if (u_holo > 0.0) {
                float band = uv.x * 0.72 + uv.y * 0.28 - u_sweep;
                float g = exp(-band * band * 26.0);
                float edge_x = 1.0 - smoothstep(0.10, 0.145,
                    min(uv.x, 1.0 - uv.x));
                float edge_top = 1.0 - smoothstep(0.085, 0.13, uv.y);
                // Reserve the readable nameplate. The lower foil lives on the
                // bottom hardware, while an expanded aperture mask guarantees
                // that no colorful strip can touch the illustration itself.
                float footer = smoothstep(0.865, 0.915, uv.y);
                float foil = max(edge_x, max(edge_top, footer));
                float art_mask = step(0.112, uv.x)
                    * step(uv.x, 0.888)
                    * step(0.104, uv.y)
                    * step(uv.y, 0.721);
                foil *= (1.0 - art_mask);
                vec3 rainbow = 0.5 + 0.5 * cos(6.28318 * (vec3(0.0, 0.33, 0.67)
                                + (uv.x * 0.6 + uv.y * 0.4) * 1.6));
                col += rainbow * g * 0.38 * u_holo * foil;
                col += vec3(1.0) * g * 0.09 * u_holo * foil;
            }

            // reveal flash (ATL-driven, 1 -> 0 as the card lands)
            col += u_edge.rgb * u_flash;

            // rarity edge ring
            float bw = 1.4;
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
    # The machine is PIXEL ART, drawn at 52x78 in the MATSUCOM palette (the
    # badge's Famicom red, brass, a stocked glass dome). It is only ever shown
    # at a WHOLE-NUMBER scale, nearest-neighbour: a fractional zoom makes some
    # pixel columns wider than their neighbours, which shimmers the moment
    # anything moves. So `height` is a target -- the nearest whole multiple of
    # 78 wins (452 -> 468 on the prize screen, 236 -> 234 on the hub floor).
    MC_MACHINE_PATH = "addons/Matsucoin Currency and Gacha/prize_machine_px.png"
    MC_MACHINE_W, MC_MACHINE_H = 52, 78

    @renpy.pure
    def McMachine(height=452):
        """The cabinet at the whole-number scale nearest `height` pixels tall."""
        z = max(1, int(round(float(height) / MC_MACHINE_H)))
        return Transform(MC_MACHINE_PATH, zoom=z, nearest=True)

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

        The cinematic (mc_reveal_fx.rpy) plays FIRST and hands off to the wall
        itself, unless the player has turned it off -- in which case the wall
        opens with every card already face-up, because somebody who has switched
        the spectacle off does not want a slower version of it either.

        NO click sound here. Every button that calls this already carries
        `activate_sound gui.activate_sound` through its style, so playing one
        here as well was the doubled UI click."""
        if mc_pull(count):
            if mc_fx_should_play():
                renpy.show_screen("mc_pull_cinematic")
            else:
                renpy.show_screen("mc_reveal", instant=True)
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

screen mc_card_face(card, w, h, locked=False, holo=None, radius=10.0,
                    show_title=False, show_serial=True):
    $ _mcf_holo = (1.0 if card.rarity == "ssr" else 0.0) if holo is None else holo
    $ _mcf_edge = enter_m_rgba("#3a4152" if locked else card.color, 0.62)

    fixed:
        xysize (w, h)

        # No separate backing Solid: mc_card_front composites authored tier stock
        # and the live illustration onto an opaque base of exactly (w, h). That
        # keeps every face identical in size and prevents mesh culling.
        if _mcf_holo > 0.0 and not locked:
            add mc_card_front(card, w, h) at mc_card_fx_holo(radius, _mcf_edge, _mcf_holo)
        else:
            add mc_card_front(card, w, h) at mc_card_fx(radius, _mcf_edge, (1.0 if locked else 0.0))

        # The binder and inspection view put the identity on the physical card.
        # Reveal walls keep their existing larger caption underneath by leaving
        # show_title at its default False.
        if show_title:
            $ _mcf_name = "UNRECORDED" if locked else mc_card_display_title(card, h)
            $ _mcf_subject = "ENTRY SEALED" if locked else MC_SUBJECT_LABEL.get(card.subject, card.subject.upper())

            text _mcf_name:
                style "mc_card_face_title"
                size mc_card_title_size(card, h)
                xsize int(w * (0.90 if h < 200 else 0.76))
                xalign 0.5
                yanchor 0.5
                ypos int(h * 0.800)
                text_align 0.5
                layout "subtitle"
                outlines ([(1, "#02040bdd", 0, 0)] if h < 200 else [(2, "#02040bcc", 0, 0), (1, "#56d7ff55", 1, 1)])

            if show_serial:
                text ("ARCHIVE // " + _mcf_subject):
                    style "mc_card_face_serial"
                    size max(5, int(round(h * 0.024)))
                    xanchor 1.0
                    xpos (w - int(radius) - 4)
                    yanchor 1.0
                    ypos (h - int(radius) - 4)

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
    # The cabinet rises to meet the pointer. It lives directly
    # inside the machine button, which is what gets it hover/idle dispatch.
    # Idle, it hums: a slow swell of light every few seconds, which is life,
    # not a call to action -- the player is already standing at it. Every
    # handler restates all three properties, or an event landing mid-ease
    # strands the others.
    subpixel True
    on idle:
        easein_quad 0.20 yoffset 0 zoom 1.0 matrixcolor BrightnessMatrix(0.0)
        block:
            pause 3.4
            ease 0.9 matrixcolor BrightnessMatrix(0.07)
            ease 1.3 matrixcolor BrightnessMatrix(0.0)
            repeat
    on hover:
        easein_quad 0.25 yoffset -10 zoom 1.0 matrixcolor BrightnessMatrix(0.10)
    on insensitive:
        easein_quad 0.20 yoffset 0 zoom 1.0 matrixcolor BrightnessMatrix(0.0)

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

    add "assets/backgrounds/matsudavr.png"
    add ArcadeField("#ffb454"):
        alpha 0.18
    add Solid("#0a0713b5")

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

                    # Pull-animation speed. Sits left of the wallet, in the slot
                    # the old dev pill used to occupy, so it never displaces the
                    # balance. This is a screen somebody will see several hundred
                    # times and the cinematic runs up to three seconds -- a
                    # spectacle you cannot turn down stops being one.
                    # xpos 898, not 1076: the wallet plate is 210 wide and
                    # right-anchored at 1128, so it owns everything from 918
                    # rightward -- and it is drawn AFTER this, so a pill placed
                    # inside that span is not merely crowded, it is invisible.
                    button:
                        style "mc_fx_pill"
                        xanchor 1.0
                        xpos 898
                        yalign 0.5
                        xysize (152, 30)
                        action Function(mc_fx_cycle_speed)
                        hover_sound gui.hover_sound

                        fixed:
                            xysize (152, 30)
                            text ("PULL FX  //  " + mc_fx_speed_label()):
                                style "mc_fx_pill_text"
                                align (0.5, 0.5)

                    # The coin bench below is NOT reachable from here any more.
                    # It lives on the Developer Hub (main menu, top-right, or
                    # F9), so the machine is only ever the machine.
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
                        yoffset 222

                    button:
                        style "mc_machine_button"
                        xysize (440, 512)
                        sensitive _mcg_single_ok
                        action Function(mc_pull_and_show, 1)
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
                            sensitive _mcg_single_ok
                            action Function(mc_pull_and_show, 1)
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
                            sensitive _mcg_ten_ok
                            action Function(mc_pull_and_show, MC_TEN_COUNT)
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
# DEV COIN BENCH  (config.developer only; opened from the Developer Hub --
# main menu, top-right, or F9 -- and mirrored by console calls, see
# matsucoin.rpy. It used to hang off a pill on the machine's own header; the
# hub owns every entry point now, and this screen stays here because the LOGIC
# belongs to Matsucoin.)
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

screen mc_reveal(instant=False):
    modal True
    zorder 70

    # How many cards have landed. The timer walks it up; a click completes it.
    #
    # `instant` is how a SKIP arrives here -- from the cinematic being clicked
    # through, or from the player having switched the spectacle off. Everything
    # is already down and face-up, because a skip should cost the animation and
    # never the result.
    default shown = (len(_mc_pull_rt.results) if instant else 0)

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

        # A single pull turns over slowly, because it is the only thing on
        # screen and the turn IS the payoff. A ten-pull turns over in a wave --
        # the cards arrive 0.16s apart, so a long flip would still be running
        # three cards later and the wall would never settle.
        _mcr_flip = (0.46 if _mcr_single else 0.24)
        _mcr_flip_wait = (0.10 if _mcr_single else 0.0)

        # A skip has nothing to animate: the backs would flash for a frame and
        # then be gone, which reads as a glitch rather than as a reveal.
        if instant:
            _mcr_flip, _mcr_flip_wait = 0.0, 0.0
        # One action for every way out of this screen -- click, Enter, Escape --
        # so the reveal cannot be in a state where one of them works and another
        # silently does nothing. Mid-reveal it lands the rest; once everything
        # is down it closes.
        # Skipping lands every remaining card at once, so it rings the BEST
        # rarity in the batch rather than nothing -- a skip should still tell
        # you what you got.
        # Sync only when the completed wall closes. If the thirtieth unique card
        # earns a trophy, its toast follows the reveal instead of spoiling it.
        _mcr_action = (
            [Function(mc_se, "coin", 0.7), Function(ach_grant_if_met, "cards_30"), Hide("mc_reveal")]
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

    # The first card waits for the deal to finish (each back takes 0.30s and
    # they start 0.035s apart), then the rest turn over 0.16s apart. Two timer
    # STATEMENTS, not one with a changing delay: a timer whose delay changes
    # keeps counting to its first one (see the cinematic's phase timers).
    if not _mcr_done:
        if shown == 0:
            timer (0.32 + 0.035 * _mcr_count) action [
                SetScreenVariable("shown", 1),
                Function(mc_reveal_step, 1),
            ]
        else:
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
                at mc_fx_banner_in

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
                        # THE TURN.
                        # The back and the face are both always in the tree and
                        # their ATL decides which is visible, so there is no
                        # swap to mistime. The back is tier-NEUTRAL on purpose:
                        # it is what the player is looking at while they still
                        # do not know.
                        $ _mcr_hot = (_card.rarity != "r")
                        $ _mcr_ray = int(_mcr_cw * 2.6)

                        fixed:
                            xysize (_mcr_cw, _mcr_ch)
                            # Already dealt face-down, so it does not land
                            # again; only a skip (nothing was dealt) eases in.
                            at (mc_card_land(0.0) if instant else mc_fx_still)

                            # Light behind a card worth something as it turns
                            # over, and a halo that stays turning behind an SSR.
                            if _mcr_hot and not instant:
                                add McPlate(_mcr_ray, _mcr_ray):
                                    align (0.5, 0.5)
                                    at mc_fx_card_rays(enter_m_rgba(_card.glow), _mcr_flip_wait + _mcr_flip * 0.45)
                            if _card.rarity == "ssr":
                                add McPlate(_mcr_ray, _mcr_ray):
                                    align (0.5, 0.5)
                                    at mc_fx_card_halo(enter_m_rgba(_card.glow), (0.0 if instant else _mcr_flip_wait + _mcr_flip))

                            # A soft glow behind a common (and behind every card
                            # on a skip). Anything better has its rays instead --
                            # a rectangular bloom under them read as a pale box.
                            if not (_mcr_hot and not instant):
                                add ArcadePanel(_mcr_cw + 26, _mcr_ch + 26,
                                                top=(_card.glow + "88"), bottom=(_card.color + "00"),
                                                radius=18):
                                    align (0.5, 0.5)
                                    at mc_reveal_glow

                            fixed:
                                xysize (_mcr_cw, _mcr_ch)
                                at (mc_fx_card_kick(_mcr_flip_wait + _mcr_flip * 0.5)
                                    if (_mcr_hot and not instant) else mc_fx_still)

                                if not instant:
                                    add McCardBack(_mcr_cw, _mcr_ch):
                                        at mc_fx_flip_back(_mcr_flip_wait, _mcr_flip)

                                    fixed:
                                        xysize (_mcr_cw, _mcr_ch)
                                        at mc_fx_flip_face(_mcr_flip_wait, _mcr_flip)
                                        use mc_card_face(_card, _mcr_cw, _mcr_ch)
                                else:
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
                        # Dealt face-down, waiting its turn. The back is
                        # tier-NEUTRAL: nothing here may leak the result.
                        add McCardBack(_mcr_cw, _mcr_ch) at mc_fx_deal(_i * 0.035)

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
    font "assets/fonts/SF Automaton Extended.ttf"
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

style mc_card_face_title is gui_text:
    font gui.interface_font
    color "#f4fbff"
    bold True
    outlines [(2, "#02040bcc", 0, 0), (1, "#56d7ff55", 1, 1)]

style mc_card_face_serial is gui_text:
    font gui.interface_font
    color "#9fc9d6"
    kerning 0.4
    outlines [(1, "#02040bdd", 0, 0)]

style mc_reveal_banner:
    font "assets/fonts/SF Automaton Extended.ttf"
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
