# =============================================================================
# def_bullets.rpy  --  ENTER M shared bullet / effect ATLAS
# =============================================================================
#
# WHAT THIS FILE IS
#   One catalogue of every sprite cut out of the two ripped Touhou sheets in
#   mod_assets/bullets/, exposed as cached crop displayables that ANY game mode
#   can draw: Kotonoha's danmaku stage, Tsubaki's soul mode, the Archivist
#   Invasions, Matsuda's fight, the Arcade cabinets. Bullets, yes, but also the
#   art that replaces flat Solids -- laser bodies, lightning arcs, summoning
#   seals, bloom discs.
#
# WHERE THE ART LIVES
#   mod_assets/bullets/ is now the ONE folder holding every bullet sprite in
#   the project. Nothing else should keep its own:
#
#     bulletsheet_th11.png   584x828  ripped sheet (etama block + seals + booms)
#     bulletsheet_th15.png   521x818  ripped sheet (hearts, lasers, lightning)
#     bulletsheet.png        256x256  the older 32px sheet kototouhou.rpy uses
#     bullet.png pellet.png dagger.png pellet_player.png
#                                    the four shipped 16px pixel sprites, moved
#                                    here out of kotonohamode/ so Kotonoha's and
#                                    Tsubaki's modes stop reaching into each
#                                    other's folders for them
#
#   Mode-specific art (ships, boss sprites, backdrops, bomb icons) stays with
#   its mode -- this folder is bullets and bullet-adjacent FX only.
#
# WHERE THE SHEETS CAME FROM
#
#   The two sheets OVERLAP heavily. Measured, not guessed:
#     * The 16px "etama" block is byte-identical in both (0 of 16384 pixels
#       differ). It is taken from th11, because th15's copy has a RED cell where
#       th11 has a clean white one at the kunai row -- and white is the cell we
#       tint from.
#     * th11 (278,274) is a third copy of th15's hearts. Dropped; use "heart".
#     * th15's 32px block (y=257+) is the same rip as bulletsheet.png
#       (star / sphere / ring / knife / oval / spark / eyes). That file is
#       still wired into kototouhou.rpy and stays authoritative for those six
#       shapes -- they are deliberately NOT redefined here.
#   So: nothing in this catalogue duplicates anything else in this catalogue.
#
# HOW COLOUR WORKS  (the important bit)
#   Almost every family ships as one shape painted in N colourways across the
#   sheet. Do NOT pick a colourway to get a colour. Pick the NEUTRAL one -- the
#   desaturated white cell, measured saturation < 0.01 -- and tint it. That
#   keeps a shape as ONE texture family across every colour a mode needs,
#   instead of N fixed ones, which is what makes the bullet caches in these
#   modes work at all. emb_cell() defaults to the neutral cell for exactly this
#   reason; emb_tint() does the tint for you.
#
#   The exceptions are marked `tintable=False`: art painted with a corona or a
#   photo (wisp, note, seal_*, bloodmoon). Tinting those only crushes the
#   colour they were drawn with. Use them as-is, or pick a colourway index.
#
# INIT ORDER
#   Everything here is `init -20 python` so that plain `init python` blocks in
#   the game modes (priority 0) can build their own crops on top of it. If you
#   see a NameError for EMB_* at startup, your consumer is initialising too
#   early, not too late.
#
# RELATED FILES
#   Matsuda's Sick Boss Fight/kotonohamode/kototouhou.rpy -- biggest consumer
#   tsubakimode/tsubaki_soul.rpy, Archivist Invasions/*   -- also draw from here
#   def_images.rpy / def_audio.rpy / def_characters.rpy   -- the sibling tables
# =============================================================================

init -20 python:

    EMB_DIR = "mod_assets/bullets/"
    EMB_SHEET = {
        "th11": EMB_DIR + "bulletsheet_th11.png",
        "th15": EMB_DIR + "bulletsheet_th15.png",
    }

    # -------------------------------------------------------------------------
    # THE CATALOGUE
    # -------------------------------------------------------------------------
    # name: (sheet, x, y, w, h, dx, dy, cols, rows, neutral, tintable)
    #
    #   x,y,w,h   rect of colourway 0. Every rect below was measured off the
    #             sheet (tight content bounds at alpha>3, so the faint outer
    #             glow survives) -- they are NOT a nominal grid. The 16px block
    #             really does drift a pixel at its last two rows.
    #   dx,dy     step to the next colourway. dy with rows>1 means the family
    #             wraps onto a second line after `cols` entries.
    #   neutral   index of the desaturated cell to tint from.
    #   tintable  False = painted art, use its own colours.
    #
    # Index order across a row is the sheet's own ramp and is only worth caring
    # about when tintable is False.
    EMB_ATLAS_RAW = {
        # --- 16px "etama" family (th11), 16 colourways, neutral = 15 ---------
        # The small workhorse shapes. Every one of these is new to the project.
        "bar":       ("th11",   5,   7,  16,  14, 16,  0, 16, 1, 15, True),
        "arrow":     ("th11",   5,  23,  16,  16, 16,  0, 16, 1, 15, True),
        "hoop":      ("th11",   5,  39,  16,  16, 16,  0, 16, 1, 15, True),
        "ball":      ("th11",   5,  55,  16,  15, 16,  0, 16, 1, 15, True),
        "rice":      ("th11",   9,  71,   9,  16, 16,  0, 16, 1, 15, True),
        "kunai":     ("th11",   8,  87,  13,  16, 16,  0, 16, 1, 15, True),
        "grain":     ("th11",   6, 103,  14,  16, 16,  0, 16, 1, 15, True),
        "ofuda":     ("th11",   6, 119,  14,  16, 16,  0, 16, 1, 15, True),
        "slug":      ("th11",   9, 135,   9,  16, 16,  0, 16, 1, 15, True),
        "seed":      ("th11",   9, 151,   9,  16, 16,  0, 16, 1, 15, True),
        "ministar":  ("th11",   5, 166,  16,  15, 16,  0, 16, 1, 15, True),
        "gloss":     ("th11",   5, 182,  16,  16, 16,  0, 16, 1, 15, True),

        # --- 32px families (th15), 8 colourways, neutral = 7 -----------------
        "heart":     ("th15", 260,   1,  30,  30, 32,  0,  8, 1,  7, True),
        "boltarrow": ("th15", 270,  34,  10,  30, 32,  0,  8, 1,  7, True),
        "dot":       ("th15", 264,  70,  21,  20, 32,  0,  8, 1,  7, True),
        "sunburst":  ("th15", 259, 225,  32,  30, 32,  0,  8, 1,  7, True),
        # 4 across, 2 down: white core under a wide coloured corona.
        "moon":      ("th15",   1, 518,  62,  62, 64, 64,  4, 2,  7, True),

        # --- 16 laser bodies (th15), stacked vertically, neutral = 15 --------
        # 248x8 hairlines. Stretch/rotate one to build a beam.
        "lens":      ("th15", 266, 330, 248,   8,  0, 16, 16, 1, 15, True),

        # --- painted art: take it as it is -----------------------------------
        # wisp is FOUR ANIMATION FRAMES across, in two colours down (red, blue).
        "wisp":      ("th11", 279, 150,  29,  32, 32, 32,  4, 2,  0, False),
        # note is three note shapes x two colours across, two colours down.
        "note":      ("th15", 271, 586,  22,  32, 32, 32,  6, 2,  0, False),

        # --- one-offs, no colourways -----------------------------------------
        "seal_spike":  ("th11", 341,  26,  63,  60, 0, 0, 1, 1, 0, False),
        "seal_orange": ("th11", 405,  24,  62,  62, 0, 0, 1, 1, 0, False),
        "seal_blue":   ("th11", 469,  24,  62,  62, 0, 0, 1, 1, 0, False),
        "seal_yellow": ("th11", 277,  88,  62,  62, 0, 0, 1, 1, 0, False),
        "seal_green":  ("th11", 341,  88,  62,  62, 0, 0, 1, 1, 0, False),
        # Height stops at y=212: th11's item-icon row starts at 214 and the
        # hexagram has no gutter above it, so a taller rect drags a line of
        # little P / 1up / F triangles along under the seal. It is drawn 200px
        # wide in Kotonoha's mode, which magnifies that bleed enormously.
        "seal_hex":    ("th11", 405,  87, 127, 126, 0, 0, 1, 1, 0, False),
        "haze":        ("th11", 341, 232,  30,  30, 0, 0, 1, 1, 0, True),
        "frost":       ("th11", 404, 232,  32,  30, 0, 0, 1, 1, 0, True),
        # Two big discs. bloom_soft is a clean radial falloff (use it for a
        # bomb wash); bloom_hard has a textured rim (use it for an impact).
        "bloom_soft":  ("th11",  28, 562, 245, 245, 0, 0, 1, 1, 0, True),
        "bloom_hard":  ("th11", 306, 547, 255, 255, 0, 0, 1, 1, 0, True),
        "bloodmoon":   ("th15", 274, 692, 123, 122, 0, 0, 1, 1, 0, False),
        # Four lightning arcs, drawn left-to-right. Cycle them for a live bolt.
        "arc0":        ("th15",   2, 644, 252,  32, 0, 0, 1, 1, 0, True),
        "arc1":        ("th15",   3, 676, 251,  31, 0, 0, 1, 1, 0, True),
        "arc2":        ("th15",   5, 711, 249,  29, 0, 0, 1, 1, 0, True),
        "arc3":        ("th15",   5, 741, 243,  30, 0, 0, 1, 1, 0, True),
    }

    EMB_ARCS = ("arc0", "arc1", "arc2", "arc3")
    EMB_SEALS = (
        "seal_orange", "seal_blue", "seal_yellow", "seal_green",
        "seal_spike", "seal_hex",
    )

    # -------------------------------------------------------------------------
    # ACCESS
    # -------------------------------------------------------------------------
    # Crops are built once and shared: a Crop is a live window onto the sheet
    # texture, not a copy, so a hundred of these still cost one texture upload.
    _emb_cell_cache = {}
    _emb_tint_cache = {}

    def emb_spec(name):
        # The raw tuple, so a consumer can do its own arithmetic.
        try:
            return EMB_ATLAS_RAW[name]
        except KeyError:
            raise Exception(
                "def_bullets: no atlas entry %r. Known names: %s"
                % (name, ", ".join(sorted(EMB_ATLAS_RAW))))

    def emb_size(name):
        # (w, h) of one cell, in sheet pixels.
        s = emb_spec(name)
        return (s[3], s[4])

    def emb_count(name):
        # How many colourways / frames this family has.
        s = emb_spec(name)
        return s[7] * s[8]

    def emb_neutral(name):
        # Index of the cell a TintMatrix wants.
        return emb_spec(name)[9]

    def emb_tintable(name):
        return emb_spec(name)[10]

    def emb_cell(name, index=None):
        # ONE cell as a Crop displayable. index defaults to the neutral cell --
        # which is what you want unless the family is painted art.
        sheet, x, y, w, h, dx, dy, cols, rows, neutral, tint = emb_spec(name)
        if index is None:
            index = neutral
        index = int(index) % max(1, cols * rows)
        if rows > 1:
            # wraps onto a second line after `cols` entries
            cx = x + (index % cols) * dx
            cy = y + (index // cols) * dy
        else:
            # one line: dx carries a horizontal strip, dy a vertical stack
            cx = x + index * dx
            cy = y + index * dy
        key = (name, index)
        d = _emb_cell_cache.get(key)
        if d is None:
            d = Crop((cx, cy, w, h), EMB_SHEET[sheet])
            _emb_cell_cache[key] = d
        return d

    def emb_frames(name):
        # Every colourway / animation frame, in sheet order.
        return [emb_cell(name, i) for i in range(emb_count(name))]

    def emb_tint(name, color, index=None, **kwargs):
        # The neutral cell recoloured. Extra kwargs go straight to Transform
        # (zoom, alpha, rotate, ...) and become part of the cache key, so keep
        # them to a small set of repeated values -- that is what keeps a swarm
        # of these down to a handful of textures.
        key = (name, color, index, tuple(sorted(kwargs.items())))
        d = _emb_tint_cache.get(key)
        if d is None:
            kw = dict(kwargs)
            if emb_tintable(name):
                kw["matrixcolor"] = TintMatrix(color)
            d = Transform(emb_cell(name, index), **kw)
            _emb_tint_cache[key] = d
        return d

    def emb_anim(name, period=0.4, indexes=None):
        # Painted multi-frame art (wisp) as a looping Animation. `period` is
        # the length of the WHOLE loop, split evenly across the frames.
        if indexes is None:
            indexes = list(range(emb_count(name)))
        else:
            indexes = list(indexes)
        hold = period / float(max(1, len(indexes)))
        args = []
        for i in indexes:
            args.append(emb_cell(name, i))
            args.append(hold)
        return Animation(*args)


# -----------------------------------------------------------------------------
# Ready-made images
# -----------------------------------------------------------------------------
# Only for things a mode wants to `show` directly rather than blit from a
# creator-defined displayable. Bullet code should call emb_cell/emb_tint.

image emb seal orange = Transform(emb_cell("seal_orange"), zoom=2.0)
image emb seal blue = Transform(emb_cell("seal_blue"), zoom=2.0)
image emb seal yellow = Transform(emb_cell("seal_yellow"), zoom=2.0)
image emb seal green = Transform(emb_cell("seal_green"), zoom=2.0)
image emb seal hex = Transform(emb_cell("seal_hex"), zoom=2.0)
image emb bloodmoon = emb_cell("bloodmoon")
image emb wisp red = emb_anim("wisp", 0.5, (0, 1, 2, 3))
image emb wisp blue = emb_anim("wisp", 0.5, (4, 5, 6, 7))
