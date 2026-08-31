# =============================================================================
# roster_view.rpy  --  CHARACTER ROSTER + "PEOPLE / CURRENT READS" SYSTEM
# =============================================================================
#
# WHAT THIS FILE PROVIDES (two related but separate features)
#   1. THE FULL ROSTER (archive feature): big character profile cards with stats
#      and a detail popup. Data = `character_roster` (list of CharacterProfile).
#      Screens: roster_view_screen -> character_detail_screen.
#      Opened from the Archive "Roster" card (game/archive.rpy) and via the
#      `roster_view` label / `roster_view_screen` at the bottom of this file.
#
#   2. THE "PEOPLE" SCREEN (in-story quick-menu feature, titled "CURRENT READS"):
#      a running list of the protagonist's one-line read on each person he has
#      met. Data = `character_thought_catalog` (+ live overrides). Screen:
#      character_thoughts_screen. Opened from the quick menu "People" button
#      (game/screens.rpy) and unlocked progressively as the story marks people met.
#
# THE PUBLIC API STORY SCRIPTS CALL (see docs/addons/ADDON_CHEATSHEET.md)
#   - mark_character_met(id, thought=None)   : add someone to the People screen
#                                               AND unlock their Archive dossier.
#   - update_character_thought(id, thought)  : change their one-line read (also
#                                               marks met if needed).
#   These two are the ONLY things story files normally touch here. The full
#   roster is data-only (edited in init_roster() below), not driven from script.
#   Outfits need no story calls at all -- see roster_scan_worn_outfits().
#
# WHAT IS LOCKED IN HERE
#   A roster slot is a silhouette until the story marks that character met, and
#   each of her outfits is "???" until she has been on screen wearing it. The
#   Roster PANEL itself is open from the first launch (game/archive.rpy).
#
# SAVE STATE (per-save, not global persistent)
#   - met_character_ids   : list of ids the player has met (drives People list).
#   - character_thoughts  : dict id -> overridden thought text.
#   Both declared with `default` so they live in each save file.
#
# PERSISTENT STATE (global, survives across saves)
#   - persistent.roster_met_ids  : set of ids whose dossier has been unlocked.
#   - persistent.outfit_<who>_<what> : one bool per non-default outfit.
#   The Archive opens from the main menu with no save loaded, so what it shows
#   cannot live in a save file. See roster_met_ids() for the full argument.
#
# SHARED THEME BORROWED FROM game/archive.rpy
#   - screen archive_backdrop          (background + scanline)
#   - screen archive_header(...)       (title bar + return button)
#   - style archive_shell_frame        (the big outer panel)
#   - style_prefix "archive_sv"        (the cyan scrollbar look)
# =============================================================================

# Roster View Addon
# Provides a character roster viewer with character profiles and information

init python:
    import store

    # -------------------------------------------------------------------------
    # CharacterProfile: one full roster entry. Numeric stats may instead be a
    # string ("Secret", "Variable", "Unknown") -- the get_*_display() helpers
    # check for that and skip the metric conversion in those cases.
    #   fit_mode         : how the sprite meets its portrait window.
    #                      "cover" (default, and what every character uses) fills
    #                      the frame and clips the overflow, so all eight subjects
    #                      present at the same scale with no dead gutters;
    #                      "contain" letterboxes the whole image instead.
    #   portrait_focus   : 0.0..1.0 -- for "cover", WHERE in the over-tall art the
    #                      window sits. 0.0 keeps the head at the top of the frame,
    #                      which is what a dossier wants; raise it a little for a
    #                      sprite drawn with unusually generous headroom. This is
    #                      the by-eye knob if a portrait sits wrong.
    #   portrait_scale    : extra scale on top of the cover fit, for a sprite whose
    #                      subject is drawn SMALLER inside its canvas than the rest
    #                      of the cast. The seven project sprites all share one
    #                      1023x1537 canvas with the figure filling ~98% of the
    #                      height, so they sit at 1.0; Monika's DDLC art is a
    #                      960x960 square with her figure filling ~93%, which at
    #                      plain cover made her read noticeably smaller than
    #                      everyone else. Pair it with portrait_focus, which pans
    #                      through the overflow the zoom creates.
    #   instrument       : the character's "Preferred Instrument" -- their musical
    #                      motif, shown as its own strip in the dossier. "N/A" for
    #                      anyone deliberately without one.
    #   manual_exception : if set, REPLACES the "Chest" stat row with a "Build"
    #                      row showing this text (used so minors show e.g. "Slim"
    #                      / "Athletic" instead of a chest measurement).
    #   grayed_out       : True -> sprite drawn desaturated and Status reads "Dead".
    #   roster_id        : the id the story marks met with -- the SAME string
    #                      mark_character_met() takes and the People screen keys
    #                      on. It is what gates this slot: a profile whose id is
    #                      not in persistent.roster_met_ids renders as an
    #                      unidentified silhouette. None = ungated (the player).
    #   outfits          : list of CharacterOutfit, unlocked as they are worn on
    #                      screen. The FIRST one is the default and is considered
    #                      unlocked the moment the character is met; it should be
    #                      the same art as sprite_image.
    # -------------------------------------------------------------------------
    class CharacterProfile:
        def __init__(self, name, full_name, sprite_image, age, birthday, height, weight, chest, likes, dislikes, description, fit_mode="cover", manual_exception=None, grayed_out=False, instrument="N/A", portrait_focus=0.0, portrait_scale=1.0, portrait_aspect=(640.0 / 960.0), roster_id=None, outfits=None):
            self.name = name
            self.full_name = full_name
            self.sprite_image = sprite_image
            self.age = age
            self.birthday = birthday
            self.height = height      # Height in inches (or string like "Secret")
            self.weight = weight      # Weight in pounds (or string like "Secret")
            self.chest = chest        # Chest in inches (or string like "Secret")
            self.likes = likes
            self.dislikes = dislikes
            self.description = description
            self.fit_mode = fit_mode  # "cover" (fill + clip) or "contain" (letterbox)
            self.manual_exception = manual_exception  # Replaces chest with build descriptor (e.g. for minors)
            self.grayed_out = grayed_out
            self.instrument = instrument
            self.portrait_focus = portrait_focus
            self.portrait_scale = portrait_scale
            self.portrait_aspect = portrait_aspect
            self.roster_id = roster_id
            self.outfits = list(outfits or [])

            # Every outfit inherits this profile's framing unless it overrode it,
            # resolved once here so the screens never have to fall back at draw
            # time. Doing it in the constructor also means an outfit list written
            # inline (which is how they all are) needs no repetition.
            for _outfit in self.outfits:
                _outfit.bind(self)

        # Has the player met this person? Ungated profiles (roster_id None) and
        # anyone the save has marked met read as identified; everyone else is a
        # silhouette. Reads persistent, NOT the per-save met_character_ids, because
        # the Archive is reachable from the main menu with no save loaded.
        @property
        def identified(self):
            if not self.roster_id:
                return True
            return self.roster_id in roster_met_ids()

        # Outfits the player has actually seen this character wearing. The first
        # entry is the default look and comes free with the introduction.
        @property
        def unlocked_outfits(self):
            return [o for o in self.outfits if o.unlocked]

        # The three get_*_display helpers all follow the same pattern: if the
        # stat is a plain string (a secret/placeholder) return it verbatim,
        # otherwise format imperial + a rounded metric conversion in parens.
        def get_height_display(self):
            if isinstance(self.height, str):
                return self.height
            cm = round(self.height * 2.54, 1)
            return "{}\" ({} cm)".format(self.height, cm)

        def get_weight_display(self):
            if isinstance(self.weight, str):
                return self.weight
            kg = round(self.weight * 0.453592, 1)
            return "{} lb ({} kg)".format(self.weight, kg)

        def get_chest_display(self):
            if isinstance(self.chest, str):
                return self.chest
            cm = round(self.chest * 2.54, 1)
            return "{}\" ({} cm)".format(self.chest, cm)

    # -------------------------------------------------------------------------
    # CharacterOutfit: one look a roster subject can be shown in.
    #
    #   id     : short, permanent slug. It is half the persistent key, so renaming
    #            one re-locks it on every existing profile.
    #   label  : what the dossier calls it.
    #   image  : the displayable the portrait window shows for this look.
    #   attr   : the ONE sprite attribute that distinguishes this outfit from the
    #            character's default, e.g. "uniform" for `matsuda uniform neut`.
    #            The auto-unlock scan (roster_scan_worn_outfits below) watches for
    #            it. None means "this is the default look" -- it has no attribute
    #            of its own, it is what is left when none of the others apply, and
    #            it comes free with the introduction.
    #
    # WHY AN ATTRIBUTE AND NOT THE WHOLE IMAGE NAME. Matching `image` verbatim
    # against what is on screen works today only because every sprite in the cast
    # is still `neut`. The moment `matsuda uniform annoyed` exists (see the
    # emotion list in docs/project/TODO.txt) an exact-name match stops firing and the
    # uniform silently never unlocks. One distinguishing attribute survives the
    # whole expression sheet being filled in.
    #
    # The portrait_* trio is optional and defaults to the owning profile's, which
    # bind() copies in -- an outfit only overrides them if its art is framed
    # differently from the character's default sprite.
    # -------------------------------------------------------------------------
    class CharacterOutfit:
        def __init__(self, id, label, image, attr=None, note="", portrait_focus=None, portrait_scale=None, portrait_aspect=None):
            self.id = id
            self.label = label
            self.image = image
            self.attr = attr
            self.note = note
            self.portrait_focus = portrait_focus
            self.portrait_scale = portrait_scale
            self.portrait_aspect = portrait_aspect
            self.owner_id = None
            self.is_default = False

        def bind(self, profile):
            """Adopt the owning profile's id and framing (called by its ctor)."""
            self.owner_id = profile.roster_id
            self.is_default = (self.attr is None)
            self.fit_mode = profile.fit_mode

            if self.portrait_focus is None:
                self.portrait_focus = profile.portrait_focus
            if self.portrait_scale is None:
                self.portrait_scale = profile.portrait_scale
            if self.portrait_aspect is None:
                self.portrait_aspect = profile.portrait_aspect

        @property
        def persistent_key(self):
            return "outfit_%s_%s" % (self.owner_id or "unknown", self.id)

        @property
        def unlocked(self):
            # The default look is the character: seeing her at all is seeing it.
            if self.is_default:
                return (not self.owner_id) or (self.owner_id in roster_met_ids())
            return getattr(persistent, self.persistent_key, False)

    # -------------------------------------------------------------------------
    # PERSISTENT UNLOCK STATE
    # Both of these are persistent, not per-save: the Archive is reachable from
    # the main menu with nothing loaded, so "have I met her" has to be a fact
    # about the PROFILE, not about whichever save happens to be in memory.
    # met_character_ids (further down) stays per-save because the People screen
    # is an in-story readout of what THIS run knows.
    # -------------------------------------------------------------------------
    def roster_met_ids():
        """The persistent met-set, coerced to a real set (guards old profiles)."""
        value = getattr(persistent, "roster_met_ids", None)
        if not isinstance(value, set):
            value = set(value or ())
            persistent.roster_met_ids = value
        return value

    def roster_mark_met(character_id):
        """Identify a roster slot for good. Idempotent; safe to call every scene."""
        if not character_id:
            return
        met = roster_met_ids()
        if character_id not in met:
            met.add(character_id)
            renpy.save_persistent()

    def outfit_unlock(*keys):
        """
        Unlock outfits by "<roster_id>:<outfit_id>" (or a bare CharacterOutfit).

        The scan below covers everything actually worn on the master layer, so
        this is for the odd look that is only ever seen somewhere a sprite is
        not -- a CG, a minigame, a still.
        """
        changed = False

        for key in keys:
            outfit = key if isinstance(key, CharacterOutfit) else roster_find_outfit(key)
            if outfit is None:
                if config.developer:
                    raise Exception("outfit_unlock: no outfit matches %r." % (key,))
                continue
            if not getattr(persistent, outfit.persistent_key, False):
                setattr(persistent, outfit.persistent_key, True)
                changed = True

        if changed:
            renpy.save_persistent()

    def roster_find_outfit(key):
        """Resolve "<roster_id>:<outfit_id>" against the roster."""
        try:
            owner, outfit_id = str(key).split(":", 1)
        except ValueError:
            return None

        for profile in character_roster:
            if profile.roster_id != owner:
                continue
            for outfit in profile.outfits:
                if outfit.id == outfit_id:
                    return outfit
        return None

    def roster_outfit_keys():
        """Every non-default outfit's persistent key (for the dev all-content switch)."""
        return tuple(
            outfit.persistent_key
            for profile in character_roster
            for outfit in profile.outfits
            if not outfit.is_default
        )

    def roster_gated_ids():
        """Every roster id that has to be earned (for the dev all-content switch)."""
        return tuple(p.roster_id for p in character_roster if p.roster_id)

    # -------------------------------------------------------------------------
    # AUTO-UNLOCK: whatever is being worn on screen right now is unlocked.
    #
    # Registered on config.start_interact_callbacks, so it runs once per
    # interaction -- every line of dialogue, every pause, every menu. It reads
    # the master layer's shown tags and, for any tag that belongs to a roster
    # subject, checks that sprite's live attributes against her outfit list.
    #
    # WHY A CALLBACK AND NOT A `$ outfit_unlock(...)` LINE PER SCENE. Outfits are
    # not events, they are a state the cast is CONSTANTLY in: the uniform is on
    # screen in most of the school day, in every side story, in the arcade modes.
    # Hand-placing the unlock means finding the earliest show of each look and
    # then remembering to do it again for every look added later, which is a
    # standing invitation to ship a wardrobe entry nothing can ever unlock. CGs
    # are the opposite -- discrete, once, and worth reading in a diff -- so those
    # ARE explicit (see cg_unlock in CG View/cg_gallery.rpy).
    # -------------------------------------------------------------------------
    def roster_scan_worn_outfits():
        try:
            shown_tags = renpy.get_showing_tags("master")
        except Exception:
            return

        if not shown_tags:
            return

        newly_worn = []

        for profile in character_roster:
            for outfit in profile.outfits:
                if outfit.is_default or outfit.unlocked:
                    continue

                # An outfit's tag is its image's first word ("matsuda uniform
                # neut" -> "matsuda"), which is also what the show statement uses.
                tag = str(outfit.image).split()[0]
                if tag not in shown_tags:
                    continue

                attributes = renpy.get_attributes(tag, "master") or ()
                if outfit.attr in attributes:
                    newly_worn.append(outfit)

        if newly_worn:
            outfit_unlock(*newly_worn)

    # -------------------------------------------------------------------------
    # THE FULL ROSTER DATA
    # character_roster is the master list the roster_view_screen renders. It is
    # (re)built by init_roster() at init time (see `init 5 python` below). To add
    # a profile, append another CharacterProfile(...) here -- positional args map
    # to the __init__ signature above.
    #
    # PREFERRED INSTRUMENT is each character's musical motif, so the reasoning is
    # worth keeping next to the data:
    #   Matsuda  synth       -- eurobeat, obviously
    #   Kotonoha violin       -- what "virtuoso" makes everyone picture
    #   Asahina  ZUNpet       -- more than a trumpet; she is a god at bullet hell
    #   Himeko   chiptune     -- not an instrument, but she is older and plays TCGs
    #   Monika   piano        -- duh
    #   Sam      harpsichord  -- gothic, ominous, two-faced
    #   Tsubaki  cello        -- quiet, reserved, overlooked, integral
    #   MC       N/A          -- he does not get one
    # -------------------------------------------------------------------------
    # Initialize character roster
    character_roster = []

    def init_roster():
        global character_roster
        character_roster = [
            CharacterProfile(
                "Matsuda",
                "Matsuda Akai",
                "matsuda neut",
                "17-18",
                "October 14",
                69,
                158,
                36,
                "Mystery novels, sports cars, data fragments (???)",
                "Laziness, idiots, mundane tasks",
                "A theatrical transfer student who treats everyday life like she's permanently on stage. Loud, charismatic, and impossible to ignore, Matsuda has a habit of pulling people into her orbit before they realize what's happening. Whether her confidence is genuine or carefully constructed is another question entirely.",
                "cover",
                None,
                False,  # grayed_out
                instrument="Synth",
                roster_id="matsuda",
                outfits=[
                    CharacterOutfit("street", "Off Duty", "matsuda neut"),
                    CharacterOutfit("uniform", "School Uniform", "matsuda uniform neut", "uniform"),
                ],
            ),
            CharacterProfile(
                "Player",
                "Asahiko *********",
                "mc neut",
                "Variable",
                "Variable",
                70,
                150,
                36,
                "???, ???, ???",
                "???, ???, ???",
                "An academically gifted senior student-athlete who prefers structure, routine, and keeping people at arm's length. While others see him as calm and composed, the reality is more complicated: his tendency to hyperfocus, overthink, and emotionally shut down often leaves him feeling disconnected from the people around him. Still, for reasons even he doesn't fully understand, he remains deeply tied to the literature club.",
                "cover",
                None,
                False,
                instrument="N/A",
                # No roster_id: the player is the one subject who is never news.
                roster_id=None,
                outfits=[
                    CharacterOutfit("standard", "Standard", "mc neut"),
                ],
            ),
            CharacterProfile(
                "Tsubaki",
                "Tsubaki Kareda",
                "tsubaki neut",
                "16-17",
                "June 18",
                64,
                128,
                0,
                "Hygiene, note-taking, validation",
                "Egos, drama, loud noises",
                "Matsuda's closest friend and frequent damage control specialist. While considerably more reserved than the people around her, Tsubaki has an easygoing warmth that makes her easy to trust. She's the kind of person who keeps things from falling apart quietly, without expecting anyone to notice.",
                "cover",
                "Slim",  # manual_exception
                instrument="Cello",
                # Her sprite is drawn with the most headroom of the seven (~5% of
                # canvas vs ~2% for the rest), so the window starts a touch lower
                # to bring her hairline back in line with everyone else's.
                portrait_focus=0.12,
                roster_id="tsubaki",
                outfits=[
                    CharacterOutfit("casual", "Casual", "tsubaki neut"),
                    CharacterOutfit("uniform", "School Uniform", "tsubaki uniform neut", "uniform"),
                    # NOT YET WORN. Her metamorphosis is late Season 1 (Chapter
                    # 4), and `tsubaki post_neut` is drawn but no scene shows it
                    # yet. ach_audit_content() flags unreachable wardrobe rows;
                    # uncomment this the day Chapter 4 stages her.
                    # CharacterOutfit("post", "Metamorphosis", "tsubaki post_neut", "post_neut"),
                ],
            ),
            CharacterProfile(
                "Asahina",
                "Asahina *********",
                "asahina neut",
                "15-16",
                "August 9",
                64,
                139,
                0,
                "Video games, volleyball, her boyfriend",
                "Nagging, early nights, overbearing people",
                "A socially bold underclassman determined to be taken seriously by the people around her. Asahina often presents herself as more mature and experienced than she actually is, bouncing between genuine insight and complete recklessness with alarming speed. Her blunt honesty tends to catch people off guard—especially her older brother.",
                "cover",
                "Athletic",  # manual_exception
                instrument="ZUNpet",
                roster_id="asahina",
                outfits=[
                    CharacterOutfit("casual", "Casual", "asahina neut"),
                    CharacterOutfit("uniform", "School Uniform", "asahina uniform neut", "uniform"),
                ],
            ),
            CharacterProfile(
                "Sam",
                "Masayami Inugami",
                "sam neut",
                "17-18",
                "January 25",
                71,
                165,
                38,
                "Indie music, basketball, power naps",
                "Cliffhangers, sour food, micromanagement",
                "Charismatic, perceptive, and difficult to pin down, Sam effortlessly drifts between friend groups without ever seeming out of place. His relaxed attitude and easy smile make him popular with just about everyone he meets, though very few people can confidently say they truly know him.",
                "cover",
                None,
                instrument="Harpsichord",
                roster_id="sam",
                outfits=[
                    CharacterOutfit("casual", "Casual", "sam neut"),
                    CharacterOutfit("uniform", "School Uniform", "sam uniform neut", "uniform"),
                ],
            ),
            CharacterProfile(
                "Mom",
                "Himeko *********",
                "mom neut",
                "42-43",
                "November 10",
                66,
                142,
                34,
                "Her children, deck building, initiative",
                "Secrets, unforced errors, messes",
                "A civil lawyer with a calm demeanor and a dangerously accurate read on people. Himeko rarely raises her voice, but her ability to dissect situations—and the people involved in them—makes lying to her feel almost impossible. Beneath her firm exterior is someone trying her best to hold her family together, even when they make that difficult.",
                "cover",
                None,
                instrument="Chiptune",
                roster_id="mom",
                outfits=[
                    CharacterOutfit("home", "At Home", "mom neut"),
                    CharacterOutfit("work", "Counsel", "mom uniform neut", "uniform"),
                    CharacterOutfit("cardigan", "Off the Clock", "mom wasted", "wasted"),
                ],
            ),
            CharacterProfile(
                "Monika",
                "Monika",
                "monika forward uniform happ cm oe nobl ldown rdown",
                "17-18",
                "September 22",
                65,
                125,
                34,
                "Reading, piano, debate",
                "Procrastination, negativity, bugs",
                "A high-achieving senior known for her leadership, composure, and involvement in just about everything the school has to offer. Monika shares an unusually close bond with the protagonist, often acting as both a source of support and the person most capable of seeing through him. Her behavior toward him occasionally borders on flirtatious, whether intentionally or not.",
                "cover",
                None,
                False,
                instrument="Piano",
                # Her DDLC art is a 960x960 SQUARE, against the other seven's 2:3
                # canvases, so at plain cover her whole body fits inside the 360px
                # window while everyone else is cropped at ~80% -- she read visibly
                # smaller than the rest of the cast.
                #
                # 1.10 was picked by RENDERING her beside Matsuda and MC through this
                # exact code path at 1.00/1.10/1.20/1.30 and comparing head size; it
                # is not a derived number. Matching whole-FIGURE height instead (which
                # works out at ~1.32) badly overshoots, because her art has a much
                # larger head-to-body ratio than the project sprites, and it is head
                # size that reads as "scale" in a portrait this small.
                # 0.88 is a RELATIVE subject scale, not a zoom: in the 300x360
                # dossier it resolves to the 1.10 zoom that was verified by
                # rendering her beside Matsuda and MC, and it stays correct in the
                # square drawer chips too, where a fixed 1.10 left her too small.
                portrait_scale=0.88,
                portrait_focus=0.04,
                # 960x960 square, not the 640x960 the other seven are normalised to.
                portrait_aspect=1.0,
                roster_id="monika",
                # Her layeredimage's `outfit` group is uniform (the default) and
                # casual -- assets/mpt/monika_layeredimage.rpy. The casual
                # set is real art, not a recolour, and the story already uses it
                # (cs_matsuda_01), so it unlocks like any other look.
                outfits=[
                    CharacterOutfit("uniform", "School Uniform",
                                    "monika forward uniform happ cm oe nobl ldown rdown"),
                    CharacterOutfit("casual", "Casual",
                                    "monika forward casual happ cm oe nobl ldown rdown", "casual"),
                ],
            ),
            CharacterProfile(
                "Kotonoha",
                "Kotonoha",
                "kotonoha neut",
                "17-18",
                "Unknown",
                65,
                "Secret",
                "Secret",
                "Unknown",
                "Unknown",
                "A student whose existence feels more like a persistent urban legend than a real classmate. Whether she's working behind a cash register, serving customers at a restaurant, or quietly passing through the halls at school, Kotonoha always seems slightly out of place in ways people struggle to explain. Most students know of her, but very few actually know her.",
                "cover",
                None,
                instrument="Violin",
                roster_id="kotonoha",
                outfits=[
                    CharacterOutfit("casual", "Casual", "kotonoha neut"),
                    CharacterOutfit("work", "On Shift", "kotonoha work neut", "work"),
                ],
            ),
        ]

    # -------------------------------------------------------------------------
    # THE "PEOPLE / CURRENT READS" DATA
    # character_thought_catalog defines every person who CAN appear on the People
    # screen, plus their default one-line "thought". The story decides WHO is
    # actually shown by calling mark_character_met(id). "id" is the key story
    # code passes around. To add someone new to People, add a dict here AND call
    # mark_character_met("<id>") at the right story beat.
    # -------------------------------------------------------------------------
    character_thought_catalog = [
        {
            "id": "monika",
            "name": "Monika",
            "subtitle": "Literature Club president",
            "sprite_image": "monika forward uniform happ cm oe nobl ldown rdown",
            "fit_mode": "cover",
            "portrait_focus": 0.04,
            "portrait_scale": 0.88,
            "portrait_aspect": 1.0,
            "thought": "Monika runs on polish and pressure. She's easy to trust, which is exactly why I keep noticing when she is tired.",
        },
        {
            "id": "mom",
            "name": "Mom",
            "subtitle": "Family",
            "sprite_image": "mom neut",
            "fit_mode": "cover",
            "thought": "She is already thinking three moves ahead about my future, and I do not know whether that helps or corners me.",
        },
        {
            "id": "asahina",
            "name": "Asahina",
            "subtitle": "Younger sister",
            "sprite_image": "asahina neut",
            "fit_mode": "cover",
            "thought": "Asa can turn a favor into a duel, but the poster matters to her more than she wants anyone to notice.",
        },
        {
            "id": "sam",
            "name": "Sam",
            "subtitle": "Asahina's boyfriend",
            "sprite_image": "sam neut",
            "fit_mode": "cover",
            "thought": "Quiet, polite, and harder to read than he looks. Asa relaxes around him in a way she usually refuses to admit.",
        },
        {
            "id": "kotonoha",
            "name": "Kotonoha",
            "subtitle": "Store clerk",
            "sprite_image": "kotonoha neut",
            "fit_mode": "cover",
            "thought": "She makes ordinary transactions feel like they were rehearsed. Useful, distant, and almost impossible to place.",
        },
        {
            "id": "matsuda",
            "name": "Matsuda Akai",
            "subtitle": "Sidewalk collision survivor",
            "sprite_image": "matsuda neut",
            "fit_mode": "cover",
            "thought": "She entered the evening like a curtain went up, demanded my number, and somehow left me curious instead of annoyed.",
        },
        {
            "id": "tsubaki",
            "name": "Tsubaki Kareda",
            "subtitle": "Matsuda's best friend",
            "sprite_image": "tsubaki neut",
            "fit_mode": "cover",
            "portrait_focus": 0.12,
            "thought": "Tsubaki spent most of our first meeting apologizing for someone else. That says more than she probably meant it to.",
        },
    ]

    # Fast id -> catalog-entry lookup, built once from the list above.
    character_thought_index = dict((entry["id"], entry) for entry in character_thought_catalog)

    # thought_state_list / thought_state_dict: lazily fetch a named store var,
    # creating it (as [] or {}) the first time if it does not exist yet. Used so
    # met_character_ids / character_thoughts are always safe to read+mutate.
    def thought_state_list(name):
        value = getattr(store, name, None)
        if value is None:
            value = []
            setattr(store, name, value)
        return value

    def thought_state_dict(name):
        value = getattr(store, name, None)
        if value is None:
            value = {}
            setattr(store, name, value)
        return value

    # PUBLIC API: register that the player has met someone. Appends the id to
    # met_character_ids (dedup) and optionally records an initial thought override.
    #
    # This is ALSO what unlocks the Archive's roster slot, which is why story
    # files never call roster_mark_met by hand: one beat, one call, and the
    # per-save People list and the persistent dossier stay in step. The two
    # stores are deliberately separate -- see roster_met_ids() for why.
    def mark_character_met(character_id, thought=None):
        met_ids = thought_state_list("met_character_ids")
        if character_id not in met_ids:
            met_ids.append(character_id)

        roster_mark_met(character_id)

        if thought:
            thought_state_dict("character_thoughts")[character_id] = thought

    # PUBLIC API: change a person's one-line read. Also marks them met so callers
    # can do this in one step without a separate mark_character_met call.
    def update_character_thought(character_id, thought):
        mark_character_met(character_id)
        thought_state_dict("character_thoughts")[character_id] = thought

    # Build the list the People screen renders: walk met_character_ids in order,
    # skip ids not in the catalog, copy each catalog entry, and apply any thought
    # override. Returns a fresh list of dicts (safe for the screen to read).
    def get_met_character_thought_entries():
        met_ids = thought_state_list("met_character_ids")
        thought_overrides = thought_state_dict("character_thoughts")
        entries = []

        for character_id in met_ids:
            if character_id not in character_thought_index:
                continue

            entry = dict(character_thought_index[character_id])
            entry["thought"] = thought_overrides.get(character_id, entry["thought"])
            entries.append(entry)

        return entries

# Per-save state backing the People screen (see helpers above).
default met_character_ids = []
default character_thoughts = {}

# Persistent state backing the ARCHIVE roster (see roster_met_ids above).
default persistent.roster_met_ids = set()

# init 5 so it runs after the class/data above are defined; rebuilds the roster
# list on every launch (keeps it fresh if profiles change).
# Initialize roster on game start
init 5 python:
    init_roster()

# init 6 so character_roster already exists the first time the scan runs.
init 6 python:
    # Same guarded-append pattern as atmosphere.rpy / achievements.rpy. A hot
    # reload builds a new function object and so slips past the guard, but the
    # scan is idempotent, so a stale duplicate costs one extra no-op pass.
    if roster_scan_worn_outfits not in config.start_interact_callbacks:
        config.start_interact_callbacks.append(roster_scan_worn_outfits)

# =============================================================================
# TRANSFORMS (entrance animations; hover handled by button styles)
# =============================================================================
# Roster grid card: fade + rise, staggered by `delay` (screen passes idx*0.06).
# Entrance animation for roster cards (no hover -- handled by style)
transform roster_card_anim(delay=0.0):
    alpha 0.0
    yoffset 25
    subpixel True
    pause delay
    easein_back 0.4 alpha 1.0 yoffset 0

# Outer panel for roster_view_screen / character_thoughts_screen: drop in, lift out.
# Frame entrance animation
# Paging between dossiers with left/right. `slide` is 0 on a first open (which
# keeps the zoom-and-rise above), -1 when paging to the PREVIOUS profile (the new
# dossier travels in from the left) and +1 for the NEXT (in from the right), so the
# motion matches the key you pressed instead of the panel swapping its contents on
# the spot.
#
# BOTH `show` and `replace` carry the same body on purpose. Paging re-shows a
# screen that is already up, and Matsu'Py delivers `replace` for that, not `show` --
# which is exactly why the old Hide()+Show() pair popped: the only handler defined
# was `on show`, so nothing was listening at the moment it mattered.
transform detail_frame_page(slide=0):
    on show, replace:
        alpha 0.0
        zoom (1.0 if slide else 0.85)
        xoffset (120 * slide)
        yoffset (0 if slide else 80)
        parallel:
            easeout_quad 0.30 xoffset 0 yoffset 0
        parallel:
            easeout_quad 0.26 alpha 1.0 zoom 1.0
    on hide:
        alpha 1.0
        easeout_quad 0.20 alpha 0.0 zoom (1.0 if slide else 0.92)

# Directional slide-ins used to stagger the detail screen's portrait / stats /
# description so they enter from left, right, and below respectively.
# Slide-in from left/right for detail content
transform detail_slide_left(delay=0.0):
    alpha 0.0
    xoffset -25
    pause delay
    easein_quad 0.4 alpha 1.0 xoffset 0

transform detail_slide_right(delay=0.0):
    alpha 0.0
    xoffset 25
    pause delay
    easein_quad 0.4 alpha 1.0 xoffset 0

transform detail_slide_up(delay=0.0):
    alpha 0.0
    yoffset 15
    pause delay
    easein_quad 0.4 alpha 1.0 yoffset 0

# =============================================================================
# SCREEN 1: roster_view_screen  -- the grid of all roster cards
# Reached from: archive.rpy "Roster" card (Show), and the roster_view label below.
# Clicking a card opens character_detail_screen for that CharacterProfile.
# =============================================================================
# Roster View Main Screen
screen roster_view_screen():
    modal True
    key "K_ESCAPE" action Hide("roster_view_screen")
    key "game_menu" action Hide("roster_view_screen")

    use archive_backdrop   # shared bg+scanline from archive.rpy

    # Live census for the readout strip. The interesting number is how much of
    # the cast the player has actually put a name to, so that is what the strip
    # counts -- ACTIVE (i.e. not deceased) is a property of the fiction and only
    # means anything for slots that have been filled in.
    $ _r_total = len(character_roster)
    $ _r_known = sum(1 for _c in character_roster if _c.identified)

    frame:
        style "archive_shell_frame"   # shared outer panel style from archive.rpy
        at archive_frame_enter(60, 0.5, 40, 0.3)

        vbox:
            spacing 12

            use archive_header("CHARACTER ROSTER", Hide("roster_view_screen"))

            # Census / readout strip.
            use archive_readout(
                "SUBJECT REGISTRY // {} PROFILES ON FILE".format(_r_total),
                "IDENTIFIED {}/{}".format(_r_known, _r_total))

            # vpgrid scales to any roster size (no more fixed 3x3 padding).
            vpgrid:
                cols 3
                spacing 25
                xalign 0.5
                style_prefix "archive_sv"   # cyan scrollbar look from archive.rpy
                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True
                xsize 1150
                ysize 540

                # One button per roster member; opens the detail popup.
                for idx, char in enumerate(character_roster):
                    $ d = idx * 0.06   # staggered entrance delay
                    $ _r_id = "R-%02d" % (idx + 1)
                    # Three states, not two: identified-and-alive, identified-and-
                    # dead, and not met at all. `_r_live` is the only one that
                    # earns a blinking pip and a cyan rail.
                    $ _r_open = char.identified
                    $ _r_live = _r_open and not char.grayed_out

                    button:
                        style "roster_card_button"
                        at roster_card_anim(d)

                        if _r_open:
                            action Show("character_detail_screen", character=char)
                        else:
                            action Show("dialog", message="You haven't met this person yet.", ok_action=Hide("dialog"))

                        vbox:
                            spacing 0

                            # Top strip: subject ID left, live status pip right.
                            # A `fixed` with an xanchor'd right child, NOT an hbox
                            # with `null width 1 xfill True` -- inside a frame the
                            # hbox shrink-wraps, so the greedy null had no room to
                            # expand into and the two ended up jammed together.
                            frame:
                                background Solid("#07111dcc")
                                xsize 300
                                padding (12, 6)

                                fixed:
                                    xsize 276
                                    ysize 16
                                    text _r_id style "roster_card_id" xpos 0 yalign 0.5
                                    if _r_live:
                                        add Solid("#56d7ff") xysize (7, 7) xanchor 1.0 xpos 276 yalign 0.5 at console_blink
                                    else:
                                        add Solid("#4f5b67") xysize (7, 7) xanchor 1.0 xpos 276 yalign 0.5

                            # Character sprite area -- the SAME clipped portrait
                            # window the detail dossier uses (archive.rpy), so a
                            # card and its dossier frame the subject identically
                            # and every card in the grid reads at one scale. It
                            # brings its own dark backing, scanline and hairlines.
                            use archive_portrait(char.sprite_image, 300, 308,
                                                char.fit_mode, char.grayed_out,
                                                char.portrait_focus, char.portrait_scale,
                                                char.portrait_aspect, not _r_open)

                            # Name plate: name left, action tag right (same fixed
                            # treatment as the ID strip above).
                            frame:
                                background Solid("#07111dcc")
                                xsize 300
                                padding (12, 7)

                                fixed:
                                    xsize 276
                                    ysize 27

                                    if _r_open:
                                        text char.name style "roster_card_name" xpos 0 yalign 0.5
                                    else:
                                        text "???" style "roster_card_name_locked" xpos 0 yalign 0.5

                                    if not _r_open:
                                        text "LOCKED" style "roster_card_tag_dead" xanchor 1.0 xpos 276 yalign 0.5
                                    elif char.grayed_out:
                                        text "DECEASED" style "roster_card_tag_dead" xanchor 1.0 xpos 276 yalign 0.5
                                    else:
                                        text "VIEW  >" style "roster_card_tag" xanchor 1.0 xpos 276 yalign 0.5

                            # Bottom accent bar (cyan when active, grey otherwise).
                            add Solid("#56d7ff" if _r_live else "#374654"):
                                xysize (300, 3)

    # Console brackets framing the shell (cohesion with the archive hub).
    use archive_shell_brackets()

# =============================================================================
# SCREEN 2: character_detail_screen(character) -- per-character profile popup
# Shown on top of roster_view_screen (zorder 100). All display strings are
# precomputed before the screen tree so the layout stays declarative.
# Note the manual_exception fork: if set, the "Chest" row becomes a "Build" row.
# =============================================================================
# Character Detail Screen
screen character_detail_screen(character, slide=0):
    modal True
    zorder 100
    key "K_ESCAPE" action Hide("character_detail_screen")
    key "game_menu" action Hide("character_detail_screen")

    # WHICH OUTFIT THE WINDOW IS SHOWING, as an outfit ID rather than an index.
    # It has to survive paging (the screen is re-shown, not rebuilt, so screen
    # `default`s carry over) and an index would then point into a DIFFERENT
    # character's shorter list. An id degrades gracefully instead: outfit ids are
    # shared vocabulary across the cast ("uniform", "casual"), so paging with a
    # look selected keeps showing that look where the next subject has one, and
    # falls back to her default where she does not.
    default outfit_id = None

    python:
        # THE STEPPER WALKS EVERY LOOK, LOCKED ONES INCLUDED, so its counter can
        # mean the obvious thing: "you are on look 2 of 3". It used to skip the
        # locked ones and count how many were unlocked, which read as a position
        # and was not one -- a fully-unlocked wardrobe showed 3/3 while sitting
        # on the first outfit. Landing on a locked look shows the same redacted
        # portrait the unmet roster cards use, which is a better answer to "is
        # there more here" than a number ever was.
        _c_all = list(character.outfits)

        _c_outfit = None
        for _o in _c_all:
            if _o.id == outfit_id:
                _c_outfit = _o
                break
        if _c_outfit is None:
            # Opening default: her first UNLOCKED look, never a "???".
            _c_unlocked = [_o for _o in _c_all if _o.unlocked]
            if _c_unlocked:
                _c_outfit = _c_unlocked[0]
            elif _c_all:
                _c_outfit = _c_all[0]

        _c_o_locked = (_c_outfit is not None) and (not _c_outfit.unlocked)

        # No outfit list at all -> fall back to the profile's own sprite, so a
        # profile added without a wardrobe still renders.
        if _c_outfit is not None:
            _c_art = _c_outfit.image
            _c_focus = _c_outfit.portrait_focus
            _c_scale = _c_outfit.portrait_scale
            _c_aspect = _c_outfit.portrait_aspect
        else:
            _c_art = character.sprite_image
            _c_focus = character.portrait_focus
            _c_scale = character.portrait_scale
            _c_aspect = character.portrait_aspect

        # Neighbours for the stepper, wrapping.
        if _c_all:
            _c_oi = _c_all.index(_c_outfit) if _c_outfit in _c_all else 0
            _c_o_prev = _c_all[(_c_oi - 1) % len(_c_all)].id
            _c_o_next = _c_all[(_c_oi + 1) % len(_c_all)].id
        else:
            _c_oi = 0
            _c_o_prev = _c_o_next = None

    # Locate this profile so we can page to neighbours (wraps at the ends).
    # Paging walks the IDENTIFIED profiles only -- an unmet subject has no
    # dossier to show, and arrowing into one would hand the player a blank.
    python:
        _c_open = [_p for _p in character_roster if _p.identified]
        if character not in _c_open:
            _c_open = [character]
        try:
            _c_idx = _c_open.index(character)
        except ValueError:
            _c_idx = 0
        _c_n = len(_c_open)
        _c_prev = _c_open[(_c_idx - 1) % _c_n] if _c_n else character
        _c_next = _c_open[(_c_idx + 1) % _c_n] if _c_n else character
        # Paging RE-SHOWS this screen with new arguments rather than Hide()+Show().
        # Re-showing keeps one live instance and hands the panel's transform a
        # `replace` event it can animate; the old pair tore the screen down and
        # rebuilt it, which is why the next profile just appeared.
        _c_page_prev = Show("character_detail_screen", character=_c_prev, slide=-1)
        _c_page_next = Show("character_detail_screen", character=_c_next, slide=1)

    # Left/right arrows page between profiles without leaving the popup (QoL).
    if _c_n > 1:
        key "K_LEFT" action _c_page_prev
        key "K_RIGHT" action _c_page_next

    # Dim the roster behind the popup.
    add Solid("#000000") at transform:
        alpha 0.0
        linear 0.25 alpha 0.85

    # Pre-compute display strings outside the screen tree
    $ _height_str = character.get_height_display()
    $ _weight_str = character.get_weight_display()
    $ _chest_str = character.get_chest_display()
    # manual_exception present -> show "Build" + descriptor; else "Chest" + value.
    $ _build_label = "Build" if character.manual_exception else "Chest"
    $ _build_value = character.manual_exception if character.manual_exception else _chest_str
    # Stat + trait tables the screen loops over (Status is shown as a chip instead
    # of a row; Full Name is already in the header).
    $ _detail_stats = [("Age", character.age), ("Birthday", character.birthday), ("Height", _height_str), ("Weight", _weight_str), (_build_label, _build_value)]
    $ _detail_traits = [("Likes", character.likes), ("Dislikes", character.dislikes)]

    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 600
        background Solid("#050811e8")
        padding (25, 20)
        at detail_frame_page(slide)

        vbox:
            spacing 12

            use archive_header(character.full_name, Hide("character_detail_screen"), "Close")

            # Dossier readout: which profile of how many.
            use archive_readout("SUBJECT DOSSIER", "PROFILE {}/{}".format(_c_idx + 1, _c_n), 850)

            # Content area
            viewport:
                style_prefix "archive_sv"
                scrollbars "vertical"
                mousewheel True
                draggable True
                xsize 850
                ysize 452

                vbox:
                    spacing 16
                    xsize 830

                    # Top section: sprite + stats side by side
                    hbox:
                        spacing 18

                        # Character portrait window (shared scanline + rules),
                        # with the wardrobe rail directly under it so the chip
                        # you press and the art it changes are the same column.
                        vbox:
                            spacing 10
                            at detail_slide_left(0.1)

                            fixed:
                                xysize (300, 360)
                                use archive_portrait(_c_art, 300, 360,
                                                    character.fit_mode, character.grayed_out,
                                                    _c_focus, _c_scale, _c_aspect,
                                                    _c_o_locked)

                            # WARDROBE. Only drawn for a subject who HAS a second
                            # look -- a one-outfit rail is a label pretending to
                            # be a control.
                            #
                            # A STEPPER, NOT A LIST, and that is a height
                            # decision. This column sits in a 452px viewport
                            # beside a 360px portrait; a vertical row-per-outfit
                            # rail ran the column to ~527px, which pushed the
                            # whole control below the fold and left it invisible
                            # unless you thought to scroll. One 34px row always
                            # fits, and it does not grow with the wardrobe.
                            #
                            # The counter is the "there is more here" signal that
                            # the per-row "???" entries used to be: 2/3 says a
                            # look exists that you have not seen, without
                            # spending a row on it or naming it.
                            if len(character.outfits) > 1:
                                frame:
                                    style "roster_wardrobe_panel"

                                    fixed:
                                        xsize 268
                                        ysize 34

                                        textbutton "<":
                                            style "roster_wardrobe_arrow"
                                            xpos 0
                                            yalign 0.5
                                            action SetScreenVariable("outfit_id", _c_o_prev)

                                        textbutton ">":
                                            style "roster_wardrobe_arrow"
                                            xanchor 1.0
                                            xpos 268
                                            yalign 0.5
                                            action SetScreenVariable("outfit_id", _c_o_next)

                                        vbox:
                                            xalign 0.5
                                            yalign 0.5
                                            spacing 1

                                            text "WARDROBE  {}/{}".format(_c_oi + 1, len(_c_all)):
                                                style "roster_wardrobe_kicker"
                                                xalign 0.5

                                            if _c_outfit is None:
                                                text "--" style "roster_wardrobe_label" xalign 0.5
                                            elif _c_o_locked:
                                                text "???" style "roster_wardrobe_label_locked" xalign 0.5
                                            else:
                                                text _c_outfit.label style "roster_wardrobe_label" xalign 0.5

                        # Character stats
                        frame:
                            style "character_detail_stats_panel"
                            at detail_slide_right(0.15)

                            vbox:
                                spacing 10

                                # Section header, with the ALIVE/DECEASED chip
                                # pinned to the panel's right edge. A `fixed` with
                                # an xanchor'd chip, not an hbox + greedy null --
                                # measured in an isolated harness, a box given an
                                # explicit xsize stops packing its children left and
                                # spreads them instead, so the chip used to sit right
                                # against the word "Profile".
                                fixed:
                                    xsize 472
                                    ysize 30

                                    add Solid("#56d7ff"):
                                        xsize 4
                                        ysize 22
                                        xpos 0
                                        yalign 0.5

                                    text "Profile" style "character_detail_section" xpos 14 yalign 0.5

                                    if character.grayed_out:
                                        frame:
                                            xanchor 1.0
                                            xpos 472
                                            yalign 0.5
                                            background Solid("#1b2832")
                                            padding (12, 5)
                                            text "DECEASED" style "archive_chip_off_text"
                                    else:
                                        frame:
                                            xanchor 1.0
                                            xpos 472
                                            yalign 0.5
                                            background Solid("#56d7ff")
                                            padding (12, 5)
                                            text "ALIVE" style "archive_chip_on_text"

                                add Solid("#56d7ff24"):
                                    xsize 472
                                    ysize 1

                                # THE STAT / TRAIT ROWS.
                                # Both tables use the same construct: a `fixed` that
                                # is 472 wide, grows in height to fit (`yfit`), with
                                # the label at xpos 0 and the value at xpos 128 --
                                # i.e. an EXPLICITLY placed two-column grid.
                                #
                                # Everything else was tried and measured in an
                                # isolated harness first, because the value column
                                # was visibly ragged and none of the obvious fixes
                                # were doing anything:
                                #   * `xsize 344` + `text_align 0.0` on the value:
                                #     text_align is completely inert here, and the
                                #     xsize makes the value CENTRE inside its box --
                                #     which is exactly why short values like "18" sat
                                #     further right than long ones like "Dislikes".
                                #   * `hbox: xsize 472`: an explicit xsize stops a box
                                #     packing its children to the left at all.
                                # `fixed` + xpos landed every row within 1px of the
                                # column edge, wrapping values included, so that is
                                # what both tables use. `yfit` means DON'T yalign the
                                # children (they would centre in the pre-fit height);
                                # the label's 3px ypos is what puts its 14px line on
                                # the 18px value's first baseline.
                                vbox:
                                    spacing 7

                                    for _label, _value in _detail_stats:
                                        fixed:
                                            xsize 472
                                            yfit True

                                            text _label style "character_detail_stat_label" xpos 0 ypos 3
                                            text "[_value]" style "character_detail_stat_value" xpos 128 ypos 0

                                add Solid("#56d7ff16"):
                                    xsize 472
                                    ysize 1

                                # Likes/dislikes -- same grid, but these values WRAP,
                                # which is why the row height comes from yfit instead
                                # of a hard number.
                                vbox:
                                    spacing 7

                                    for _label, _value in _detail_traits:
                                        fixed:
                                            xsize 472
                                            yfit True

                                            text _label style "character_detail_stat_label" xpos 0 ypos 3
                                            text "[_value]" style "character_detail_stat_value" xpos 128 ypos 0

                                add Solid("#56d7ff16"):
                                    xsize 472
                                    ysize 1

                                # PREFERRED INSTRUMENT: the character's musical
                                # motif. Given its own strip rather than another
                                # stat row -- "Preferred Instrument" will not fit
                                # the 112px label column, and a motif deserves
                                # more presence than a measurement anyway.
                                fixed:
                                    xsize 472
                                    ysize 40

                                    add Solid("#56d7ff88"):
                                        xsize 3
                                        ysize 34
                                        xpos 0
                                        yalign 0.5

                                    text "PREFERRED INSTRUMENT" style "character_detail_kicker" xpos 14 ypos 0
                                    text character.instrument style "character_detail_motif" xpos 14 ypos 15

                    # Description section
                    frame:
                        style "character_detail_desc_panel"
                        at detail_slide_up(0.3)

                        vbox:
                            spacing 10

                            hbox:
                                spacing 10
                                yalign 0.5
                                ysize 30

                                add Solid("#56d7ff"):
                                    xsize 4
                                    ysize 22
                                    yalign 0.5

                                text "Description" style "character_detail_section" yalign 0.5

                            add Solid("#56d7ff24"):
                                xsize 798
                                ysize 1

                            text character.description style "character_detail_desc"

    # Side paging arrows (wrap-around), mirroring the CG viewer.
    if _c_n > 1:
        textbutton "<":
            xalign 0.0
            yalign 0.5
            xoffset 24
            text_size 54
            text_color "#56d7ffaa"
            text_hover_color "#ffffff"
            text_bold True
            text_outlines [(2, "#02040b", 0, 0)]
            background None
            hover_background None
            action _c_page_prev

        textbutton ">":
            xalign 1.0
            yalign 0.5
            xoffset -24
            text_size 54
            text_color "#56d7ffaa"
            text_hover_color "#ffffff"
            text_bold True
            text_outlines [(2, "#02040b", 0, 0)]
            background None
            hover_background None
            action _c_page_next


# =============================================================================
# SCREEN 3: character_thoughts_screen -- the in-story "People / CURRENT READS"
# Opened from the quick menu "People" button (game/screens.rpy).
# Renders only people the player has met, via get_met_character_thought_entries().
# Empty state shows "No one notable yet."
# =============================================================================
screen character_thoughts_screen():
    modal True
    zorder 215
    key "K_ESCAPE" action Hide("character_thoughts_screen")
    key "game_menu" action Hide("character_thoughts_screen")

    # Resolve the met-people list (catalog + live thought overrides).
    $ _thought_entries = get_met_character_thought_entries()

    use archive_backdrop

    frame:
        style "archive_shell_frame"
        at archive_frame_enter(60, 0.5, 40, 0.3)

        vbox:
            spacing 12

            use archive_header("CURRENT READS", Hide("character_thoughts_screen"), "Close")

            # Census / readout strip.
            use archive_readout(
                "PROTAGONIST NOTES // {} PEOPLE READ".format(len(_thought_entries)),
                "PERSONAL LOG")

            viewport:
                style_prefix "archive_sv"
                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True
                xsize 1150
                ysize 540

                vbox:
                    spacing 14
                    xfill True

                    if not _thought_entries:
                        # Empty state.
                        frame:
                            style "thought_entry_frame"

                            text "No one notable yet." style "thought_body":
                                xalign 0.5
                                yalign 0.5
                    else:
                        # One row per met person: sprite chip + name/subtitle/read.
                        for entry in _thought_entries:
                            frame:
                                style "thought_entry_frame"

                                hbox:
                                    spacing 18

                                    # Same clipped portrait window as the roster and
                                    # the dossier. It used to be a bare `add` with no
                                    # clipping: `fit` only scales, so a "cover" chip
                                    # rendered taller than its 118x144 box and hung
                                    # out of the top of the row.
                                    use archive_portrait(entry["sprite_image"], 118, 144,
                                                        entry.get("fit_mode", "cover"), False,
                                                        entry.get("portrait_focus", 0.0),
                                                        entry.get("portrait_scale", 1.0),
                                                        entry.get("portrait_aspect", 640.0 / 960.0))

                                    vbox:
                                        spacing 8
                                        yalign 0.5
                                        xsize 900

                                        text entry["name"] style "thought_name"
                                        text entry["subtitle"] style "thought_subtitle"

                                        add Solid("#56d7ff44"):
                                            xsize 880
                                            ysize 1

                                        text entry["thought"] style "thought_body"

    # Console brackets framing the shell (cohesion with the archive hub).
    use archive_shell_brackets()

# =============================================================================
# STYLES  -- card/detail/thought visuals. Same cyan-on-near-black palette as the
# archive theme so these screens feel continuous with the Archive hub.
# =============================================================================
# Styles
style roster_title:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 36
    color "#f4fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]


style roster_card_button:
    # 379 = ID strip 27 + portrait 308 + name plate 41 + accent bar 3. It was 372,
    # which quietly clipped the bottom of every card's name plate and accent bar.
    xysize (300, 379)
    background Solid("#07111dcc")
    hover_background Solid("#12314af2")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (0, 0)

style roster_card_name:
    size 22
    color "#dff8ff"
    bold True
    text_align 0.0
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style roster_card_name_locked is roster_card_name:
    color "#687787"

style roster_card_id:
    font gui.interface_font
    size 12
    color "#56d7ff"
    kerning 1.0
    bold True
    outlines [(1, "#02040b", 0, 0)]

# --- WARDROBE RAIL (dossier, under the portrait) -----------------------------
# 300 wide to sit flush with the portrait window above it; 268 is that minus the
# panel's 16px padding either side, and every child in the rail is measured
# against 268 so the kicker's right-hand tally lands on the panel edge.
style roster_wardrobe_panel is archive_panel:
    xsize 300
    padding (16, 8)

style roster_wardrobe_kicker is gui_text:
    font gui.interface_font
    size 11
    color "#7fcfe0"
    kerning 2.0
    bold True
    outlines [(1, "#02040b", 0, 0)]

style roster_wardrobe_arrow:
    xysize (30, 30)
    background Solid("#07111dcc")
    hover_background Solid("#12314af2")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (0, 0)

style roster_wardrobe_arrow_text:
    font gui.interface_font
    size 20
    color "#56d7ff"
    hover_color "#ffffff"
    bold True
    xalign 0.5
    yalign 0.5
    outlines [(1, "#02040b", 0, 0)]

style roster_wardrobe_label:
    font gui.interface_font
    size 16
    color "#dff8ff"
    bold True
    text_align 0.5
    outlines [(1, "#02040b", 0, 0), (1, "#56d7ff66", 1, 1)]

style roster_wardrobe_label_locked is roster_wardrobe_label:
    color "#687787"
    outlines [(1, "#02040b", 0, 0)]

style roster_card_tag:
    font gui.interface_font
    size 12
    color "#56d7ff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style roster_card_tag_dead:
    font gui.interface_font
    size 12
    color "#4f5b67"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style character_detail_title:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 38
    color "#f4fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style character_detail_section:
    size 22
    color "#f4fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style character_detail_stats_panel:
    xsize 512
    yminimum 360
    background Solid("#07111dcc")
    padding (16, 14, 16, 14)

style character_detail_info:
    size 19
    color "#dff8ff"
    outlines [(1, "#02040b", 0, 0)]

style character_detail_stat_label:
    size 14
    color "#8fb6c5"
    xsize 112
    xalign 0.0
    text_align 0.0
    outlines [(1, "#02040b", 0, 0)]

style character_detail_stat_value:
    size 18
    color "#dff8ff"
    xsize 344
    xalign 0.0
    text_align 0.0
    outlines [(1, "#02040b", 0, 0)]

# The PREFERRED INSTRUMENT strip: a small tracked-out kicker over the value, in
# the same cyan-on-near-black language as the archive's other readouts.
style character_detail_kicker:
    font gui.interface_font
    size 11
    color "#7fcfe0"
    kerning 2.0
    bold True
    outlines [(1, "#02040b", 0, 0)]

style character_detail_motif:
    size 20
    color "#f4fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style character_detail_desc_panel:
    xsize 830
    background Solid("#07111dcc")
    padding (16, 14, 16, 16)

style character_detail_desc:
    size 18
    color "#c9d8e1"
    text_align 0.0
    line_spacing 4
    xmaximum 798
    outlines [(1, "#02040b", 0, 0)]

style thought_entry_frame:
    xsize 1128
    yminimum 172
    background Solid("#07111dcc")
    padding (16, 14, 16, 14)

# (thought_sprite_frame retired: the People row now uses the shared
# archive_portrait window, which brings its own backing and rules.)

style thought_name:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 25
    color "#f4fbff"
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style thought_subtitle:
    font gui.interface_font
    size 14
    color "#8fb6c5"
    outlines [(1, "#02040b", 0, 0)]

style thought_body:
    font gui.default_font
    size 18
    color "#c9d8e1"
    line_spacing 1
    xmaximum 880
    outlines [(1, "#02040b", 0, 0)]

# -----------------------------------------------------------------------------
# Convenience label: `call roster_view` opens the full roster as a blocking
# screen call and returns when it is hidden. (archive.rpy uses Show() instead;
# this label is for story/script use.)
# -----------------------------------------------------------------------------
# Label to call roster view
label roster_view:
    call screen roster_view_screen
    return
