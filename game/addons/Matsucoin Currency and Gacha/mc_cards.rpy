# =============================================================================
# mc_cards.rpy  --  THE CARD CATALOG + collection state
# =============================================================================
#
# WHAT THIS FILE IS
#   Every collectible card, what it is worth, and the record of which ones the
#   player owns. It owns NO UI: the machine that hands cards out is mc_gacha.rpy
#   and the binder that shows them off is mc_collection.rpy. Coins are
#   matsucoin.rpy.
#
# THE THREE TIERS, AND WHAT DECIDES ONE
#   R   -- the cast as the story shows them. Default sprites, uniform or casual,
#          plus the four full-body reaction poses and the faces from around
#          school. If you have played the game you have seen every R card.
#   SR  -- the cast as something else. The seven MSBF party archetypes, the
#          16-bit Kotonoha, Tsubaki after the metamorphosis, the Purgatorium
#          girl: alternative sprites and portraits that exist because some mode
#          or side story needed her to look different.
#   SSR -- what was at the other end of a fight. Final phases, superboss forms,
#          and the Archivists. Every SSR is something that was trying to end a
#          run when you last saw it.
#
# ART IS REFERENCED, NEVER COPIED
#   Cards point at sprites and mode art that already ship. Nothing in this
#   feature adds an image file, which is why a 42-card set was affordable at
#   all -- and it means a card is automatically consistent with the thing it
#   depicts, because it IS the thing it depicts.
#
# PIXEL SOURCES
#   Three cards (the 16-bit Kotonoha and both marionette Tsubaki phases) use
#   low-resolution pixel sprites. They carry pixel=True, which pre-scales them
#   with nearest sampling before the portrait cropper ever sees them. Without
#   it, sprite art blown up to a 300px card face is mush; the crop's own scaling
#   is smooth, so the source has to arrive already large.
#
# ADDING A CARD
#   Append one McCard(...) below. The id is a permanent ledger key -- it is what
#   persistent.mc_cards_owned stores -- so never recycle one for a different
#   subject, and never rename one that has shipped.
# =============================================================================

# -----------------------------------------------------------------------------
# COLLECTION STATE
# owned : the SET of card ids the player has. Not a count.
#
#   DUPLICATES ARE NOT KEPT. A duplicate's entire job is to turn into coins at
#   the moment it is pulled (card.refund), and it does that inside mc_pull --
#   after which there is nothing left to remember. Storing copy counts bought a
#   "x3" badge and a SPARES readout that told the player a number they could
#   never spend, act on, or care about. So a card is owned or it is not, which
#   also makes it structurally impossible for a duplicate to re-flag something
#   as NEW.
#
# pity  : pulls since the last SSR (see mc_gacha.rpy for how it is spent).
# -----------------------------------------------------------------------------
default persistent.mc_cards_owned = set()
default persistent.mc_pulls_total = 0
default persistent.mc_pity = 0
default persistent.mc_new_ids = set()

init -4 python:

    # -------------------------------------------------------------------------
    # RARITY TABLE
    # weight  : pull odds, as a percentage. Must total 100 (asserted below in
    #           developer builds -- a silent 97% table would quietly bias every
    #           pull and nothing would ever look wrong enough to investigate).
    # refund  : coins a DUPLICATE converts to. Deliberately well under a pull:
    #           a dupe should soften the disappointment, not refund the attempt.
    # color   : the tier's ink, used for rails, chips, borders and the card edge.
    # glow    : the brighter accent for fills and the reveal flash.
    # -------------------------------------------------------------------------
    MC_RARITY_ORDER = ["r", "sr", "ssr"]
    MC_RARITY = {
        "r": {
            "label": "R", "full": "RECORDED",
            "weight": 70.0, "refund": 25,
            "color": "#6f7d95", "glow": "#a9b8cf",
        },
        "sr": {
            "label": "SR", "full": "SUPER RECORDED",
            "weight": 25.0, "refund": 60,
            "color": "#a274ff", "glow": "#d3bcff",
        },
        "ssr": {
            "label": "SSR", "full": "SPECIAL SUPER RECORDED",
            "weight": 5.0, "refund": 150,
            "color": "#ffb454", "glow": "#ffe6a8",
        },
    }

    class McCard(object):
        """One collectible card.

        id      : permanent ledger key. Never recycle or rename a shipped one.
        rarity  : "r" / "sr" / "ssr".
        name    : what the card is called.
        subject : grouping key for the binder's sidebar -- normally a roster id,
                but "seer"/"archivist"/"school" for the ones that are not a
                cast member in their own right.
        flavor  : one line under the art. Written to be readable by someone who
                has not reached that content yet: no card spoils its own
                source, the same rule the Side Stories list follows.
        image   : image name or path. Anything Matsu'Py can turn into a displayable.
        focus   : 0..1, where in over-tall art the card window sits (0 = heads).
        scale   : size RELATIVE to a standard 640x960 sprite -- NOT a raw zoom.
                See ArchivePortraitCrop in game/archive.rpy for why the window
                aspect has to be folded in.
        aspect  : the SOURCE's width/height. Defaults to the 640x960 every
                character sprite is normalised to by def_characters.rpy.
        xfocus  : 0..1 across the width, for subjects who do not stand in the
                middle of their own art (anyone holding a weapon out to one
                side).
        pixel   : pre-scale with nearest sampling. See the file header.
        fit     : "cover" (default) crops the art to fill the whole face.
                "contain" letterboxes the whole image against the card base --
                for art whose subject is destroyed by a portrait crop.
        """
        def __init__(self, id, rarity, name, subject, flavor, image,
                    focus=0.0, scale=1.0, aspect=(640.0 / 960.0), xfocus=0.5,
                    pixel=False, fit="cover"):
            self.fit = fit
            self.id = id
            self.rarity = rarity
            self.name = name
            self.subject = subject
            self.flavor = flavor
            self.image = image
            self.focus = focus
            self.scale = scale
            self.aspect = aspect
            self.xfocus = xfocus
            self.pixel = pixel

        @property
        def tier(self):
            return MC_RARITY.get(self.rarity, MC_RARITY["r"])

        @property
        def color(self):
            return self.tier["color"]

        @property
        def glow(self):
            return self.tier["glow"]

        @property
        def refund(self):
            return self.tier["refund"]

        @property
        def owned(self):
            return mc_card_owned(self.id)

    # -- art path constants ---------------------------------------------------
    # The MSBF folder has an apostrophe in its name, which is legal in a path
    # and legal in a double-quoted Python string, but is worth keeping in one
    # place rather than retyping per card.
    MC_MSBF   = "addons/Matsuda's Sick Boss Fight/"
    MC_ARCH   = MC_MSBF + "archetypes/"
    MC_KOTO   = MC_MSBF + "kotonohamode/"
    MC_TSUBA  = MC_MSBF + "tsubakimode/"
    MC_IDMODE = MC_MSBF + "idmode/"
    MC_INV    = "addons/Archivist Invasions/"

    # The archetype plates and the two boss stills are 1023x1537 -- 2:3, same as
    # a normalised character sprite, so they need no aspect override.
    MC_A_TALL = 1023.0 / 1537.0

    # -------------------------------------------------------------------------
    # THE CATALOG
    # -------------------------------------------------------------------------
    MC_CARDS = [

        # ===== R -- the cast as the story shows them =========================
        McCard("r_matsuda_casual", "r", "Off Duty", "matsuda",
            "Nobody is watching and she is performing anyway.",
            "matsuda casual happy", focus=0.02),
        McCard("r_matsuda_uniform", "r", "School Uniform", "matsuda",
            "Second period. She has already decided how today goes.",
            "matsuda uniform smug", focus=0.02),
        McCard("r_matsuda_chuuni", "r", "Full Chuuni", "matsuda",
            "The pose came first. The reason will be along shortly.",
            "matsuda uniform pose_chuuni", focus=0.05),
        McCard("r_matsuda_facepalm", "r", "Not Again", "matsuda",
            "You did the thing. She saw you do the thing.",
            "matsuda uniform pose_facepalm", focus=0.05),
        McCard("r_matsuda_shrug", "r", "Search Me", "matsuda",
            "An answer shaped exactly like not having one.",
            "matsuda uniform pose_shrug", focus=0.05),
        McCard("r_matsuda_laughing", "r", "Genuinely Funny", "matsuda",
            "Rare, and over before you can check whether it was real.",
            "matsuda casual pose_laughing", focus=0.05),
        McCard("r_matsuda_convention", "ssr", "Forever Young", "matsuda",
                "Gotta go all out on anime conventions, right?",
                "assets/characters/matsuda/convention_fullbody.png"),

        McCard("r_tsubaki_casual", "r", "Casual", "tsubaki",
            "Standing slightly outside the group photo, as usual.",
            "tsubaki neut", focus=0.02),
        McCard("r_tsubaki_uniform", "r", "School Uniform", "tsubaki",
            "Present every day. Remembered by almost nobody.",
            "tsubaki uniform neut", focus=0.02),

        McCard("r_asahina_casual", "r", "Casual", "asahina",
            "Off the clock, out of the uniform, still keeping score.",
            "asahina neut", focus=0.02),
        McCard("r_asahina_uniform", "r", "School Uniform", "asahina",
            "Small, loud, and faster than you at everything that counts.",
            "asahina uniform neut", focus=0.02),

        McCard("r_sam_casual", "r", "Casual", "sam",
            "Perfectly pleasant. Ask a second question and see.",
            "sam neut", focus=0.02),
        McCard("r_sam_uniform", "r", "School Uniform", "sam",
            "The face he wears to be agreed with.",
            "sam uniform neut", focus=0.02),

        McCard("r_kotonoha_casual", "r", "Casual", "kotonoha",
            "Everyone knows of her. Almost nobody knows her.",
            "kotonoha neut", focus=0.02),
        McCard("r_kotonoha_work", "r", "On Shift", "kotonoha",
            "Behind a register somewhere she has definitely not worked before.",
            "kotonoha work neut", focus=0.02),

        McCard("r_mom_home", "r", "At Home", "mom",
            "The kitchen light is on. She waited up. Again.",
            "mom neut", focus=0.02),
        McCard("r_mom_work", "r", "Counsel", "mom",
            "The version of her that other people are allowed to need.",
            "mom uniform neut", focus=0.02),

        # Her DDLC layeredimage is a 960x960 SQUARE, not the 640x960 the rest of
        # the cast is normalised to, so a cover crop into a portrait card shows
        # her full height and trims the empty air at her sides. No `scale`: on a
        # card, scale only ever zooms further IN (see _mc_cover).
        McCard("r_monika_uniform", "r", "School Uniform", "monika",
            "Club president. Still, after everything, running the meeting.",
            "monika forward uniform happ cm oe nobl ldown rdown",
            focus=0.04, aspect=1.0),
        McCard("r_monika_casual", "r", "Casual", "monika",
            "Off the clock in a club that no longer meets.",
            "monika forward casual happ cm oe nobl ldown rdown",
            focus=0.04, aspect=1.0),

        McCard("r_mc", "r", "Standard Issue", "mc",
            "Academically gifted. Emotionally unavailable. Present.",
            "mc neut", focus=0.02),

        McCard("r_hikari", "r", "Hikari", "school",
            "A classmate. She has a whole life you will never open.",
            "hikari neut", focus=0.02),
        McCard("r_homura", "r", "Homura", "school",
            "A classmate. Same deal.",
            "homura neut", focus=0.02),
        McCard("r_coach", "r", "Track Coach", "school",
            "Still alive, whatever that trial insisted.",
            "track_coach neut", focus=0.02),
        McCard("r_math", "r", "Math Teacher", "school",
            "Owns your third period and one recurring nightmare.",
            "math_teacher neut", focus=0.02),
        McCard("r_civics", "r", "Civics Teacher", "school",
            "Grades on participation, which you have never once done.",
            "civics_teacher neut", focus=0.02),

        # ===== SR -- the cast as something else ==============================
        McCard("sr_arch_mc", "sr", "The Spellblade", "mc",
            "Somebody handed him a sword and he did the reading on it.",
            MC_ARCH + "mcspellblade.png", focus=0.03, aspect=MC_A_TALL),
        McCard("sr_arch_monika", "sr", "The Mage", "monika",
            "She has read the manual. She helped write the manual.",
            MC_ARCH + "monikamage.png", focus=0.03, aspect=MC_A_TALL),
        McCard("sr_arch_kotonoha", "sr", "The Ink Mage", "kotonoha",
            "Casting in a language the party agreed not to ask about.",
            MC_ARCH + "kotomage.png", focus=0.03, aspect=MC_A_TALL),
        McCard("sr_arch_asahina", "sr", "The Halberdier", "asahina",
            "The shortest reach on the field and the longest weapon.",
            MC_ARCH + "asahalberdier.png", focus=0.03, aspect=MC_A_TALL),
        McCard("sr_arch_sam", "sr", "The Berserker", "sam",
            "The pleasant one, with the safety off.",
            MC_ARCH + "samberserker.png", focus=0.03, aspect=MC_A_TALL),
        McCard("sr_arch_tsubaki", "sr", "The Quiet Mage", "tsubaki",
            "Overlooked right up until the casting finishes.",
            MC_ARCH + "tsubakimage.png", focus=0.03, aspect=MC_A_TALL),
        McCard("sr_arch_mom", "sr", "The Trickster", "mom",
            "She plays cards. You did not know she plays cards like this.",
            MC_ARCH + "himekotrickster.png", focus=0.03, aspect=MC_A_TALL),

        # The two superseded archetype plates. They are in the build, they are
        # real art, and they are no longer what those two look like -- which is
        # exactly the kind of thing this Archive keeps.
        McCard("sr_arch_mc_old", "sr", "The Spellblade (Revision A)", "mc",
            "An earlier draft of the same swordsman. Still filed.",
            MC_ARCH + "mcspellbladeold.png", focus=0.03, aspect=MC_A_TALL),
        McCard("sr_arch_asahina_old", "sr", "The Halberdier (Revision A)", "asahina",
            "Before the redesign. She kept the reach.",
            MC_ARCH + "asahalberdierold.png", focus=0.03, aspect=MC_A_TALL),

        McCard("sr_koto_16bit", "sr", "Sixteen Bits", "kotonoha",
            "Sixty pixels tall and the hardest read in the building.",
            MC_KOTO + "archive/kotobosssprite_legacy.png",
            focus=0.0, aspect=60.0 / 102.0, pixel=True),

        McCard("sr_tsubaki_post", "sr", "Metamorphosis", "tsubaki",
            "Whatever was being saved up finished arriving.",
            "tsubaki post_neut", focus=0.02),
        McCard("sr_tsubaki_revelation", "sr", "Revelation", "tsubaki",
            "She worked something out. It did not improve her mood.",
            "tsubaki post_revelation", focus=0.02),

        McCard("sr_asahina_terror", "sr", "Come Home Immediately", "asahina",
            "One text. She has read it four times.",
            "asahina uniform terror", focus=0.02),

        McCard("sr_mom_cardigan", "sr", "Off the Clock", "mom",
            "The cardigan, the couch, and nobody left to be composed for.",
            "mom wasted", focus=0.02),

        McCard("sr_purg_girl", "sr", "The Girl in Purgatorium", "purg",
            "She has been in this classroom longer than the classroom has.",
            "purg_girl", focus=0.03, aspect=1024.0 / 1536.0),
        McCard("sr_purg_day7", "sr", "Day Seven", "purg",
            "Six days of composure, spent.",
            "purg_girl_day7", focus=0.03, aspect=1024.0 / 1536.0),
        McCard("sr_purg_yukata", "sr", "Festival Night", "purg",
            "A summer that is not going to happen, dressed for.",
            "purg_girl_yukata", focus=0.03, aspect=1024.0 / 1296.0),

        # ===== SSR -- what was at the other end of a fight ===================
        McCard("ssr_seer_1", "ssr", "Ontological Seer", "seer",
            "The transfer student, four-on-one, and still ahead on tempo.",
            MC_MSBF + "phase1.png", focus=0.03, aspect=MC_A_TALL),
        McCard("ssr_seer_2", "ssr", "Ontological Seer // Second Movement", "seer",
            "The stage stopped pretending to be a classroom.",
            MC_MSBF + "phase2.png", focus=0.06, scale=1.15,
            aspect=1426.0 / 1103.0),
        McCard("ssr_seer_id", "ssr", "ONTOLOGICAL SEER: ID", "seer",
            "She swore she would never build it. She built it.",
            MC_IDMODE + "idphase.png", focus=0.06, scale=1.15,
            aspect=1536.0 / 1024.0),

        McCard("ssr_tsuba_act1", "ssr", "The Unwritten Act", "tsubaki",
            "Somebody is holding the strings and it is not her.",
            MC_TSUBA + "phase1.png",
            focus=0.0, aspect=184.0 / 344.0, pixel=True),
        McCard("ssr_tsuba_act2", "ssr", "The Unwritten Act // Encore", "tsubaki",
            "The house lights came up and she kept performing.",
            MC_TSUBA + "phase2.png",
            focus=0.0, aspect=184.0 / 344.0, pixel=True),

        # The only `contain` card in the set. Its art is a single centred heart
        # on a wider-than-tall canvas; cover-cropping it into a portrait window
        # slices both lobes off and leaves an unreadable red band.
        McCard("ssr_a_fine_date", "ssr", "A Fine Date", "monika",
            "One evening, one exit, and something beating between them.",
            MC_MSBF + "monikamode/mon_heart.png",
            aspect=376.0 / 336.0, scale=0.86, fit="contain"),

        McCard("ssr_inv_biography", "ssr", "BIOGRAPHY", "archivist",
            "It is not trying to kill her. It is trying to finish the entry.",
            MC_INV + "biography.png", focus=0.03, aspect=MC_A_TALL),
        McCard("ssr_inv_horror", "ssr", "HORROR", "archivist",
            "It is not wearing anyone. It brought its own light.",
            MC_INV + "horror.png", focus=0.05, scale=1.05, aspect=1.0),
        McCard("ssr_inv_nonfiction", "ssr", "NONFICTION", "archivist",
            "Whatever it cannot corroborate does not get to have happened.",
            MC_INV + "nonfiction.png", focus=0.03,
            aspect=1024.0 / 1536.0),
    ]

    MC_CARD_BY_ID = {c.id: c for c in MC_CARDS}

    # Pre-split per tier. The pull picks a tier and then picks uniformly inside
    # it, so these are built once instead of filtered on every one of ten pulls.
    MC_CARDS_BY_RARITY = {
        rarity: [c for c in MC_CARDS if c.rarity == rarity]
        for rarity in MC_RARITY_ORDER
    }

    # -- SUBJECT GROUPS (the binder's sidebar) --------------------------------
    # Ordered deliberately, not alphabetically: the cast in roster order, then
    # the three groups that are not a single cast member.
    MC_SUBJECTS = [
        ("matsuda",   "MATSUDA"),
        ("tsubaki",   "TSUBAKI"),
        ("asahina",   "ASAHINA"),
        ("sam",       "SAM"),
        ("kotonoha",  "KOTONOHA"),
        ("mom",       "MOM"),
        ("monika",    "MONIKA"),
        ("mc",        "PLAYER"),
        ("seer",      "THE SEER"),
        ("archivist", "ARCHIVISTS"),
        ("purg",      "PURGATORIUM"),
        ("school",    "SCHOOL"),
    ]

    # -------------------------------------------------------------------------
    # COLLECTION ACCESS
    # -------------------------------------------------------------------------
    def _mc_ensure_cards():
        """Coerce collection state (guards pre-feature profiles, same reasoning
        as _mc_ensure_store in matsucoin.rpy).

        MIGRATION: mc_cards_owned used to be {card_id: copies}. Copy counts are
        gone, so an old dict collapses to its key set -- which loses nothing,
        because the coins those duplicates were worth were paid out at the
        moment each one was pulled."""
        owned = getattr(persistent, "mc_cards_owned", None)
        if not isinstance(owned, set):
            persistent.mc_cards_owned = set(owned or ())
        if not isinstance(getattr(persistent, "mc_new_ids", None), set):
            persistent.mc_new_ids = set(getattr(persistent, "mc_new_ids", None) or [])
        for field in ("mc_pulls_total", "mc_pity"):
            if not isinstance(getattr(persistent, field, None), int):
                try:
                    setattr(persistent, field, int(getattr(persistent, field, 0) or 0))
                except (TypeError, ValueError):
                    setattr(persistent, field, 0)

    def mc_card_owned(card_id):
        _mc_ensure_cards()
        return card_id in persistent.mc_cards_owned

    def mc_card_add(card_id):
        """Record a card. -> True if this is the FIRST copy, which is exactly
        the question the pull asks: a first copy is NEW, anything else is a
        duplicate and gets refunded instead of stored.

        The set is COPIED, written and REASSIGNED rather than mutated in place,
        for the reason ag_set_best spells out in ag_core.rpy: Matsu'Py pickles
        persistent wholesale so an in-place mutation would in fact be saved, but
        assignment is the form that is unambiguously correct under every path
        including a persistent merge between two machines."""
        _mc_ensure_cards()
        if card_id in persistent.mc_cards_owned:
            return False
        owned = set(persistent.mc_cards_owned)
        owned.add(card_id)
        persistent.mc_cards_owned = owned
        new_ids = set(persistent.mc_new_ids)
        new_ids.add(card_id)
        persistent.mc_new_ids = new_ids
        return True

    def mc_card_seen(card_id):
        """Clear one card's NEW badge (the binder does this as you look at it)."""
        _mc_ensure_cards()
        if card_id in persistent.mc_new_ids:
            new_ids = set(persistent.mc_new_ids)
            new_ids.discard(card_id)
            persistent.mc_new_ids = new_ids
        return None

    def mc_is_new(card_id):
        _mc_ensure_cards()
        return card_id in persistent.mc_new_ids

    # -- census ---------------------------------------------------------------
    def mc_collection_counts(rarity=None):
        """(owned, total) over the whole catalog or one tier."""
        pool = MC_CARDS if rarity is None else MC_CARDS_BY_RARITY.get(rarity, [])
        return (sum(1 for c in pool if mc_card_owned(c.id)), len(pool))

    def mc_subject_counts(subject):
        pool = [c for c in MC_CARDS if c.subject == subject]
        return (sum(1 for c in pool if mc_card_owned(c.id)), len(pool))

    def mc_cards_for(subject):
        """A subject's cards, rarest first, so a group's best sits at the top."""
        order = {r: i for i, r in enumerate(reversed(MC_RARITY_ORDER))}
        return sorted(
            (c for c in MC_CARDS if c.subject == subject),
            key=lambda c: (order.get(c.rarity, 9), c.name),
        )


    # -------------------------------------------------------------------------
    # CARD ART
    # One builder for both the machine and the binder, so a card is framed
    # identically wherever it is drawn.
    #
    # THE CONTRACT: every card face is EXACTLY (w, h). No exceptions, whatever
    # the source's aspect is.
    #
    # This is why it does NOT use ArchivePortraitCrop. That cropper deliberately
    # normalises a subject's size against a reference 2:3 sprite (read the long
    # note on it in game/archive.rpy), so a source with a different aspect
    # renders SMALLER than the window and is centred inside it. That is correct
    # for a dossier, which draws its own opaque frame around the result -- and
    # wrong here, because the card shader is a MESH whose u_model_size comes
    # from the displayable it wraps. A narrow marionette sprite once resolved
    # to a 102x134 render inside a 152x213 slot, so the shader drew a 102x134
    # CARD: visibly narrower than its neighbours, with its border misplaced.
    #
    # So: cover-and-crop to exactly (w, h), then composite onto an opaque base
    # of exactly (w, h). The base doubles as the guarantee that the mesh is
    # never culled for transparency, and as what a `contain` card letterboxes
    # against.
    # -------------------------------------------------------------------------
    MC_CARD_BASE = "#0b0818"
    _MC_ART_CACHE = {}

    def _mc_cover(img, w, h, aspect, focus, xfocus, zoom):
        """Scale `img` so it COVERS (w, h) (times `zoom`), then crop back to
        exactly (w, h) -- panned `xfocus` across and `focus` down. Always
        returns a displayable of exactly (w, h).

        `zoom` is floored at 1.0: below it the art would no longer cover the
        window and the crop would come back SHORT, which is precisely the
        failure this function exists to prevent."""
        aspect = max(float(aspect), 0.01)
        zoom = max(1.0, float(zoom))
        mul = max(float(w) / aspect, float(h)) * zoom
        rw = mul * aspect
        rh = mul
        frac_w = min(1.0, float(w) / rw)
        frac_h = min(1.0, float(h) / rh)
        crop_x = (1.0 - frac_w) * max(0.0, min(1.0, float(xfocus)))
        crop_y = (1.0 - frac_h) * max(0.0, min(1.0, float(focus)))
        scaled = Transform(img, fit="cover",
                        xysize=(int(round(rw)), int(round(rh))))
        return Transform(scaled, crop=(crop_x, crop_y, frac_w, frac_h),
                        crop_relative=True)

    def _mc_contain(img, w, h, aspect, scale):
        """The whole image, letterboxed. -> (width, height, displayable)."""
        aspect = max(float(aspect), 0.01)
        scale = max(0.05, min(1.0, float(scale)))
        bw = min(float(w), float(h) * aspect) * scale
        bh = bw / aspect
        bw, bh = int(round(bw)), int(round(bh))
        return bw, bh, Transform(img, fit="contain", xysize=(bw, bh))

    def mc_card_art(card, w, h):
        """`card` framed into exactly (w, h), opaque."""
        key = (card.id, int(w), int(h))
        hit = _MC_ART_CACHE.get(key)
        if hit is not None:
            return hit

        w, h = int(w), int(h)
        source = card.image

        if card.pixel:
            # Integer nearest zoom up to roughly the card height BEFORE the
            # smooth cropper sees it. Integer keeps the pixel grid square; the
            # crop's own sub-pixel scaling is then a small correction instead of
            # a 5x smear.
            native_h = max(1.0, float(w) / max(card.aspect, 0.01))
            factor = max(1, int(round(float(h) / native_h)))
            source = Transform(source, zoom=factor, nearest=True)

        if card.fit == "contain":
            bw, bh, art = _mc_contain(source, w, h, card.aspect, card.scale)
            offset = ((w - bw) // 2, (h - bh) // 2)
        else:
            art = _mc_cover(source, w, h, card.aspect, card.focus,
                            card.xfocus, card.scale)
            offset = (0, 0)

        # Composite, not Fixed: Composite takes an EXPLICIT size and renders at
        # exactly that, which is the guarantee this whole function is for. A
        # Fixed sizes itself from its children / available space.
        out = Composite(
            (w, h),
            (0, 0), Solid(MC_CARD_BASE, xysize=(w, h)),
            offset, art,
        )
        _MC_ART_CACHE[key] = out
        return out

    # -------------------------------------------------------------------------
    # DEV
    # Developer Hub -> ECONOMY, or the console (Shift+O):
    #     mc_dev_grant_all() / mc_dev_clear_cards()
    # -------------------------------------------------------------------------
    def mc_dev_grant_all():
        _mc_ensure_cards()
        persistent.mc_cards_owned = set(c.id for c in MC_CARDS)
        try:
            renpy.save_persistent()
        except Exception:
            pass
        renpy.restart_interaction()
        return None

    def mc_dev_clear_cards():
        _mc_ensure_cards()
        persistent.mc_cards_owned = set()
        persistent.mc_new_ids = set()
        persistent.mc_pulls_total = 0
        persistent.mc_pity = 0
        try:
            renpy.save_persistent()
        except Exception:
            pass
        renpy.restart_interaction()
        return None


# -----------------------------------------------------------------------------
# CATALOG SELF-CHECK (developer builds only)
# Three ways this catalog can be quietly wrong, all of them invisible in play:
# a duplicate id silently drops a card out of the dict; rarity weights that do
# not total 100 bias every pull with nothing on screen looking wrong; and an
# empty tier makes its roll crash the machine mid-pull. Fail at launch instead.
# -----------------------------------------------------------------------------
init 5 python:
    if config.developer:
        _mc_ids = [c.id for c in MC_CARDS]
        if len(_mc_ids) != len(set(_mc_ids)):
            _mc_dupes = sorted(set(i for i in _mc_ids if _mc_ids.count(i) > 1))
            raise Exception("mc_cards: duplicate card id(s): %s" % ", ".join(_mc_dupes))

        _mc_weight = sum(MC_RARITY[r]["weight"] for r in MC_RARITY_ORDER)
        if abs(_mc_weight - 100.0) > 0.001:
            raise Exception("mc_cards: rarity weights total %.3f, not 100." % _mc_weight)

        for _r in MC_RARITY_ORDER:
            if not MC_CARDS_BY_RARITY.get(_r):
                raise Exception("mc_cards: rarity %r has no cards to pull." % _r)

        for _c in MC_CARDS:
            if _c.subject not in dict(MC_SUBJECTS):
                raise Exception("mc_cards: card %r has subject %r, which is not "
                                "in MC_SUBJECTS -- it would be unreachable in "
                                "the binder." % (_c.id, _c.subject))
            if _c.fit not in ("cover", "contain"):
                raise Exception("mc_cards: card %r has fit %r; expected "
                                "'cover' or 'contain'." % (_c.id, _c.fit))
            # A cover card with scale < 1 is a silent framing bug: _mc_cover
            # floors the zoom at 1.0 to keep the face exactly sized, so the
            # author's number would just be ignored. Say so instead.
            if _c.fit == "cover" and _c.scale < 1.0:
                raise Exception("mc_cards: card %r is fit='cover' with scale "
                                "%.3g. On a card, scale only zooms further IN "
                                "-- use fit='contain' to make art smaller than "
                                "the face." % (_c.id, _c.scale))
