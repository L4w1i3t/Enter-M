# =============================================================================
# char_stories.rpy  --  CHARACTER STORIES HUB (archive feature)
# =============================================================================
#
# WHAT THIS FILE PROVIDES
#   The "Side Stories" browser: a sidebar of characters on the left, and on the
#   right a panel listing that character's standalone short stories. Each story
#   is its own Matsu'Py label living in a sibling cs_<name>_NN.rpy file; selecting
#   one starts that label in a clean game store (leaving the menu entirely).
#
# HOW IT IS REACHED
#   - Archive "Side Stories" card -> Show("character_stories")  (see game/archive.rpy;
#     note the card is labelled "Side Stories" but opens this "character_stories" screen).
#
# THE DATA MODEL (character_story_catalog, built in init python below)
#   character_story_catalog = [ CharacterStoryCatalog(...) , ... ]
#   - CharacterStoryEntry(title, description, label_name, persistent_key)
#       label_name     : the Matsu'Py label to launch (defined in a cs_*.rpy file).
#       persistent_key : name of the persistent bool gating this story.
#       .unlocked      : getattr(persistent, persistent_key) -> is it playable?
#   - CharacterStoryCatalog(name, sprite_image, [entries], fit_mode)
#       .any_unlocked / .unlocked_count : roll-ups used to drive the UI state.
#
# UNLOCK FLAGS (one persistent bool per story, all default False)
#   cs_matsuda_01_unlocked, cs_matsuda_02_unlocked, cs_tsubaki_01_unlocked,
#   cs_tsubaki_02_unlocked, cs_asahina_01_unlocked, cs_sam_01_unlocked,
#   cs_mom_01_unlocked, cs_monika_01_unlocked, cs_kotonoha_01_unlocked,
#   cs_kotonoha_02_unlocked.
#   These are the ONLY gate. persistent.archive_unlocked_character_stories opens
#   the Archive card and nothing else, and it now ships True. A locked story
#   keeps its slip in the drawer but reads "SEALED FILE" with its title withheld
#   -- a side story's title is a spoiler in a way a CG thumbnail or a roster
#   silhouette is not. The set is flipped by the curated list at the end of
#   0531.rpy, and by the ALL SIDE CONTENT switch in
#   Developer Date Jump/dev_date_jump.rpy.
#
# WHERE THE STORY LABELS LIVE (label_name -> file)
#   cs_matsuda_01/02  -> Character Stories/cs_matsuda_01.rpy / cs_matsuda_02.rpy
#   cs_player_01      -> cs_player_01.rpy           cs_tsubaki_01 -> cs_tsubaki_01.rpy
#   cs_asahina_01     -> cs_asahina_01.rpy          cs_tsubaki_02 -> cs_tsubaki_02.rpy
#   cs_mom_01         -> cs_mom_01.rpy              cs_sam_01     -> cs_sam_01.rpy
#   cs_kotonoha_01/02 -> cs_kotonoha_01.rpy / cs_kotonoha_02.rpy  cs_monika_01 -> cs_monika_01.rpy
#   (The Tsubaki pair shares a themed prose engine: cs_tsubaki_gothic.rpy.)
#
# SHARED THEME BORROWED FROM game/archive.rpy
#   - screen archive_backdrop, screen archive_header(...)
#   - styles archive_shell_frame / archive_sidebar_panel / archive_panel
#   - viewport style_prefix "archive_sv"; generic "dialog" screen for locked rows.
# =============================================================================

# Character Stories addon
# A catalog of single short-stories pertaining to each character in the mod,
# independent of the main story and its continuity. Stories unlock as the player
# meets each character, providing extra development, worldbuilding, and "what-if"
# scenarios. Accessed from the archive menu.

# ----- Data Definitions -----

init python:
    class CharacterStoryEntry:
        """Represents a single story for a character."""
        def __init__(self, title, description, label_name, persistent_key):
            self.title = title
            self.description = description
            self.label_name = label_name        # standalone label to launch
            self.persistent_key = persistent_key # persistent bool gating it

        # Live lock state, read straight off persistent each render.
        @property
        def unlocked(self):
            # An empty key (the "???" placeholder entry) is never unlockable,
            # even when the master archive flag flips every real story on.
            if not self.persistent_key:
                return False
            return getattr(persistent, self.persistent_key, False)

        # UNLOCKED vs COMPLETED are two different questions and the drawer shows
        # both: "can I read this" and "have I read it". The completion key is
        # DERIVED from the unlock key rather than being a second field, so a
        # story can never be catalogued with one and not the other.
        @property
        def completed_key(self):
            if not self.persistent_key:
                return None
            return self.persistent_key.replace("_unlocked", "_completed")

        @property
        def completed(self):
            key = self.completed_key
            return bool(key) and bool(getattr(persistent, key, False))

        # The state the NEW badge is for: yours, and you have not read it.
        @property
        def unread(self):
            return self.unlocked and not self.completed

    class CharacterStoryCatalog:
        """Groups stories under a character with a display image.

        The portrait_* trio matches CharacterProfile in roster_view.rpy and feeds
        archive_portrait / ArchivePortraitCrop: `focus` is where in the over-tall
        art the window sits, `scale` is how big the subject should read relative to
        a standard sprite (window-normalised, NOT a raw zoom), and `aspect` is the
        source's w/h (640x960 for every normalised character sprite, 1.0 for
        Monika's square DDLC layeredimage).
        """
        def __init__(
            self, name, sprite_image, stories, fit_mode="cover",
            portrait_focus=0.0, portrait_scale=1.0,
            portrait_aspect=(640.0 / 960.0),
        ):
            self.name = name
            self.sprite_image = sprite_image
            self.stories = stories
            self.fit_mode = fit_mode
            self.portrait_focus = portrait_focus
            self.portrait_scale = portrait_scale
            self.portrait_aspect = portrait_aspect

        # Used by the sidebar to show progress / locked state per character.
        @property
        def any_unlocked(self):
            return any(s.unlocked for s in self.stories)

        @property
        def unlocked_count(self):
            return sum(1 for s in self.stories if s.unlocked)

        @property
        def completed_count(self):
            return sum(1 for s in self.stories if s.completed)

        # Drives the drawer tab's unread dot: how many files this subject is
        # holding that the player has not opened yet.
        @property
        def unread_count(self):
            return sum(1 for s in self.stories if s.unread)

        # Total number of *real* (unlockable) stories for this character.
        @property
        def total(self):
            return sum(1 for s in self.stories if s.persistent_key)

        # True if this character has at least one real, unlockable story
        # (i.e. not the empty "???" placeholder and not an empty roster).
        @property
        def has_real_stories(self):
            return self.total > 0

    # -------------------------------------------------------------------------
    # MASTER CATALOG. Each entry's label_name must match a label in the matching
    # cs_*.rpy file, and persistent_key must match a default below. The trailing
    # "???" catalog with empty label/key is an intentional locked placeholder.
    # -------------------------------------------------------------------------
    # Master catalog
    character_story_catalog = [
        CharacterStoryCatalog(
            "Matsuda",
            "matsuda neut",
            [
                CharacterStoryEntry("Dead Fantasy", "Choose an army. Fight Greywake. Decide who comes home.", "cs_matsuda_01", "cs_matsuda_01_unlocked"),
                CharacterStoryEntry("Ontological Seer", "You guys like RPGs, right?", "cs_matsuda_02", "cs_matsuda_02_unlocked"),
            ],
        ),
        CharacterStoryCatalog(
            "Player",
            "mc neut",
            [
                # CharacterStoryEntry("Coming Soon", "This story hasn't been written yet.", "cs_player_01", "cs_player_01_unlocked"),
            ],
        ),
        CharacterStoryCatalog(
            "Tsubaki",
            "tsubaki neut",
            [
                CharacterStoryEntry("Heads", "You will say that I was kind.", "cs_tsubaki_01", "cs_tsubaki_01_unlocked"),
                CharacterStoryEntry("Tails", "You will say that she was mad.", "cs_tsubaki_02", "cs_tsubaki_02_unlocked"),
            ],
        ),
        CharacterStoryCatalog(
            "Asahina",
            "asahina neut",
            [
                CharacterStoryEntry("Hina's World", "Inspired by the Lacey Games horror series.", "cs_asahina_01", "cs_asahina_01_unlocked"),
            ],
        ),
        CharacterStoryCatalog(
            "Sam",
            "sam neut",
            [
                CharacterStoryEntry("Purgatorium", "Never download weird apps from Aptoide.", "cs_sam_01", "cs_sam_01_unlocked"),
            ],
        ),
        CharacterStoryCatalog(
            "Himeko",
            "mom neut",
            [
                # CharacterStoryEntry("Continuance", "A case file with no verdict.", "cs_mom_01", "cs_mom_01_unlocked"),
            ],
        ),
        CharacterStoryCatalog(
            "Monika",
            "monika forward uniform happ cm oe nobl ldown rdown",
            [
                # CharacterStoryEntry("Lies and Poems", "Let's check out Emily's first mod.", "cs_monika_01", "cs_monika_01_unlocked"),
            ],
            fit_mode="cover",
            # 960x960 square DDLC art rather than the 640x960 the rest are
            # normalised to; the zoom brings her head up to the cast's scale.
            portrait_focus=0.04,
            # Relative subject scale, window-normalised -- see ArchivePortraitCrop.
            portrait_scale=0.88,
            portrait_aspect=1.0,
        ),
        CharacterStoryCatalog(
            "Kotonoha",
            "kotonoha neut",
            [
                CharacterStoryEntry("The Girl with Every Face", "Who is she?", "cs_kotonoha_01", "cs_kotonoha_01_unlocked"),
                CharacterStoryEntry("The Void Hunter", "When you stare into the abyss, the abyss stares back.", "cs_kotonoha_02", "cs_kotonoha_02_unlocked"),
            ],
        ),
        # CharacterStoryCatalog(
        #     "???",
        #     "assets/dump/icon_placeholder.png",
        #     [
        #         CharacterStoryEntry("???", "This story is still locked.", "", ""),
        #     ],
        # ),
    ]

    # -------------------------------------------------------------------------
    # PUBLIC API: cs_mark_completed("cs_sam_01") -- "the player has READ this".
    #
    # Called from the story's own ending, by label name, so a story that can end
    # several ways decides for itself which endings count. The rule the catalog
    # follows: reaching an ENDING completes it, losing or bailing does not --
    # Matsuda's fight marks on victory and not on the defeat menu, Kotonoha's
    # two mark on their real ending and not on the attention-check failure.
    #
    # Idempotent, and it persists immediately: the player's next stop after a
    # side story is usually the Archive, and the badge has to already be right.
    # -------------------------------------------------------------------------
    def cs_mark_completed(label_name):
        entry = cs_find_story(label_name)

        if entry is None:
            if config.developer:
                raise Exception("cs_mark_completed: no story has label %r." % (label_name,))
            return

        key = entry.completed_key
        if key and not getattr(persistent, key, False):
            setattr(persistent, key, True)
            renpy.save_persistent()
            # Keep the global trophy state current when a story closes.
            if "ach_sync" in globals():
                ach_sync()

    def cs_find_story(label_name):
        for category in character_story_catalog:
            for story in category.stories:
                if story.label_name == label_name:
                    return story
        return None

    def cs_all_unlock_keys():
        return tuple(
            s.persistent_key
            for c in character_story_catalog
            for s in c.stories
            if s.persistent_key
        )

    def cs_all_completed_keys():
        return tuple(
            s.completed_key
            for c in character_story_catalog
            for s in c.stories
            if s.completed_key
        )

    def cs_unread_total():
        return sum(c.unread_count for c in character_story_catalog)

# Persistent unlock flags (default False) -- one per story above.
default persistent.cs_matsuda_01_unlocked = False
default persistent.cs_matsuda_02_unlocked = False
default persistent.cs_tsubaki_01_unlocked = False
default persistent.cs_tsubaki_02_unlocked = False
default persistent.cs_asahina_01_unlocked = False
default persistent.cs_sam_01_unlocked = False
default persistent.cs_mom_01_unlocked = False
default persistent.cs_monika_01_unlocked = False
default persistent.cs_kotonoha_01_unlocked = False
default persistent.cs_kotonoha_02_unlocked = False

# ...and one _completed per story, set by cs_mark_completed() from the story's
# own ending. Declared here beside their _unlocked partners rather than in each
# cs_*.rpy, so "which stories exist" is one list to read. (The Tsubaki pair used
# to declare theirs locally; those two were the first to have completion flags.)
default persistent.cs_matsuda_01_completed = False
default persistent.cs_matsuda_02_completed = False
default persistent.cs_tsubaki_01_completed = False
default persistent.cs_tsubaki_02_completed = False
default persistent.cs_asahina_01_completed = False
default persistent.cs_sam_01_completed = False
default persistent.cs_mom_01_completed = False
default persistent.cs_monika_01_completed = False
default persistent.cs_kotonoha_01_completed = False
default persistent.cs_kotonoha_02_completed = False
# archive_unlocked_character_stories gates the Archive's Character Stories
# SECTION. It no longer implies "every story inside it is readable" -- the
# story flags above are set individually by the script at the point each story
# has been earned (see the curated unlock at the end of 0531.rpy). Keeping the
# two separate is what lets Chapter 0.5 open the section without spoiling
# Purgatorium, and stops any story added to the catalog later from arriving
# pre-unlocked on an existing save.

# RETIRED (2026-08): there used to be an `init 10` here that, in developer mode,
# read archive_unlocked_character_stories as "unlock every story too". That was
# safe while the section flag was itself earned at the end of Chapter 0.5 -- but
# the flag now ships True (game/archive.rpy: the Archive shell is open from the
# first launch), so the hook would have force-unlocked the entire catalog on
# every dev boot AND undone the dev switch's own DISABLE the next time the game
# started. The ENABLE/DISABLE ALL SIDE CONTENT button in the Developer Date Jump
# menu is now the single dev override, and it covers strictly more than this did.

# =============================================================================
# TRANSFORMS
# =============================================================================
# THE METAPHOR: this screen is a READING ROOM, not a menu. The left rail is a
# shelf holding one cloth-bound volume per subject (the "tabs" below); the right
# pane is that volume lying open. Every animation below exists to sell that --
# volumes slide out of the shelf, the book is laid open afresh when you change
# subject, and the contents lines slide out under the pointer. Nothing here
# fades in place, because paper does not fade.
# =============================================================================

# Whole-shell entrance / exit.
# A SUBJECT TAB in the drawer. Tabs sit recessed in their runners; the selected
# one has been drawn fully forward and stays there, and hovering any other nudges
# it out far enough to say "this one moves too".
#
# THE PULL IS DRIVEN BY BUTTON STATE, NOT BY A PARAMETER. It used to take a `sel`
# argument, which meant that changing the selection rebuilt EVERY tab's transform
# -- and a rebuilt transform restarts its opening block, so all eight tabs replayed
# their staggered fade-in at once. On screen that read as the outgoing tab ghosting
# out, the incoming one ghosting in, and a hole in the drawer where the tab you
# just clicked had not faded up yet. Matsu'Py already dispatches selected_idle /
# selected_hover to a transform inside a button whose `selected` is true, so the
# tab can react to its own state without the transform ever being re-created --
# which means the opening block runs exactly once, on entry.
#
# `delay` is the only parameter and it is constant per row, so the screen language
# reuses the same transform object across updates.
#
# EVERY OFFSET HERE IS >= 0, AND THAT IS NOT A STYLE CHOICE. These tabs live in a
# viewport, and a viewport CLIPS: the old version parked the unselected tabs at
# xoffset -14, which put their left 14px (the whole 5px spine and the folder notch
# with it) outside the viewport and simply cut them off. On screen that did not
# read as "recessed" at all -- every tab started on the same left edge and the
# unselected ones just ended 14px short, i.e. as a ragged right margin. So the
# pull now runs the other way: a tab sits flush in the drawer at 0 and is drawn
# out to the RIGHT, toward the sheet it opens. The entry slide comes from +26 for
# the same reason.
transform cs_tab(delay=0.0):
    subpixel True
    alpha 0.0
    xoffset 26
    pause delay
    easeout_quad 0.30 alpha 1.0 xoffset 0
    on idle:
        easeout_quad 0.20 alpha 1.0 xoffset 0
    on hover:
        easeout_quad 0.16 alpha 1.0 xoffset 10
    on selected_idle:
        easeout_quad 0.22 alpha 1.0 xoffset 14
    on selected_hover:
        easeout_quad 0.16 alpha 1.0 xoffset 14

# THE PULLED SHEET. This one DOES want to be rebuilt on every subject change --
# that is the whole point, the new file being lifted out of the drawer -- so it
# takes the selection as a parameter purely to force that rebuild. Nothing in the
# body uses `key`.
transform cs_sheet_pull(key=0):
    subpixel True
    alpha 0.0
    yoffset 26
    zoom 0.985
    parallel:
        easeout_quad 0.34 yoffset 0 zoom 1.0
    parallel:
        easeout_quad 0.22 alpha 1.0

# A FILE SLIP inside the sheet. The stack deals itself out on entry (staggered by
# `delay`), and the pointer pulls one clear of the others.
#
# THE STACK IS NO LONGER FANNED AT REST. It used to take a per-row `rest` offset
# (row n sat 7px further right than row n-1), which is a lovely idea on paper and
# reads as a misprint on screen: every slip's left edge, index tab and PULL chip
# landed on a different column, and none of them lined up with the rule above the
# stack. The motion carries the paper metaphor on its own -- the deal-in and the
# hover pull -- so the resting stack is square. (Reinstating the fan is one
# `xoffset (sidx * 7)` in the screen, if it ever looks worth it again.)
#
# Offsets stay >= 0: like the drawer tabs, these live in a clipping viewport, so
# the entry slide comes from the right rather than out through the left wall.
transform cs_slip(delay=0.0):
    subpixel True
    alpha 0.0
    xoffset 30
    pause delay
    easeout_quad 0.30 alpha 1.0 xoffset 0
    on idle:
        easeout_quad 0.18 xoffset 0
    on hover:
        easeout_quad 0.14 xoffset 16

# The bookplate: pasted onto the frontispiece, slightly off-square. `key` is
# unused in the body; passing the volume restarts it on every subject change
# (an ATL with different arguments does not inherit the old timeline).
#
# rotate_pad TRUE, deliberately. With it False the rotated render keeps the
# child's UNROTATED size, so anything the rotation swings outside that box is
# cropped -- and a wide, shallow box turned 11 degrees swings a long way: a
# 215x40 stamp needs 219x80 to land in, so the corners were being sliced off.
transform cs_stamp(ang=-11, key=None):
    subpixel True
    rotate ang
    rotate_pad True
    alpha 0.0
    zoom 1.35
    pause 0.18
    parallel:
        easeout_quad 0.14 zoom 1.0
    parallel:
        linear 0.10 alpha 1.0

# ----- Main Screen (the shelf + the open book) -----
# selected_idx (screen-local) picks which volume lies open on the right: a
# shelf of cloth-bound volumes on the left, one per subject, and the chosen
# one open across two pages -- frontispiece and bookplate on the left, the
# contents on the right.

# One cloth per volume, in shelf order, so the shelf reads as a run of real
# books. An unopened volume is bound in plain grey board instead.
define CS_VOLUME_CLOTH = ("#5b2f3c", "#2c5b59", "#4a3a5c", "#3a4f6b", "#5c4a2e", "#3e5a45", "#6b3f2e", "#2f3e4f")
define CS_ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X")

init python:
    def cs_roman(n):
        return CS_ROMAN[n - 1] if 0 < n <= len(CS_ROMAN) else str(n)

screen character_stories():
    modal True

    # Selected character index -- defaults to first in list.
    default selected_idx = 0

    use archive_backdrop

    key "game_menu" action Hide("character_stories", transition=enter_m_menu_doorway)
    key "K_ESCAPE" action Hide("character_stories", transition=enter_m_menu_doorway)

    # Live census for the readout strip.
    $ _cs_subject_total = len(character_story_catalog)
    $ _cs_subjects_seen = sum(1 for _c in character_story_catalog if _c.any_unlocked)
    $ _cs_files_found = sum(_c.unlocked_count for _c in character_story_catalog)
    $ _cs_files_total = sum(_c.total for _c in character_story_catalog)
    $ _cs_files_unread = cs_unread_total()

    frame:
        style "archive_shell_frame"
        padding (24, 20)
        at archive_frame_enter(50, 0.5, 30)

        vbox:
            spacing 12

            use archive_header("SIDE STORIES", Hide("character_stories", transition=enter_m_menu_doorway))

            # The right-hand readout answers the question the player actually
            # opened this screen with -- "is there anything in here I have not
            # read" -- and falls back to the volume census once there is not.
            if _cs_files_unread:
                $ _cs_right_readout = "{} UNREAD".format(_cs_files_unread)
            else:
                $ _cs_right_readout = "{} OF {} VOLUMES OPEN".format(_cs_subjects_seen, _cs_subject_total)

            use archive_readout(
                "THE READING ROOM / {} OF {} STORIES RECOVERED".format(_cs_files_found, _cs_files_total),
                _cs_right_readout)

            # THE CONTENT ROW IS 1150 WIDE AND CENTRED, because that is the width
            # of the readout rail above it (archive_readout's default, and the
            # house grid every archive sub-screen is built on). 320 + 10 + 820 =
            # 1150, and the xalign makes it land on the rail exactly.
            hbox:
                spacing 0
                xalign 0.5

                # =========================================================
                # LEFT: THE SHELF
                # One volume per subject. The runner is 312 wide (306 of it
                # usable, 6 for the scrollbar) and a volume is 286, so the
                # selected one -- drawn 14px out toward the open book by
                # cs_tab() -- ends exactly on the shelf label's right edge at
                # 300, while the ones still shelved sit flush at 0. See cs_tab
                # for why the pull may not run the other way.
                # =========================================================
                frame:
                    xsize 320
                    ysize 520
                    style "archive_sidebar_panel"
                    padding (8, 12, 0, 12)

                    vbox:
                        spacing 8

                        fixed:
                            xsize 300
                            ysize 18
                            text "SHELF A" style "cs_drawer_label" xpos 0 yalign 0.5
                            text "VOLUMES" style "cs_drawer_label" xanchor 1.0 xpos 300 yalign 0.5

                        add Solid("#d9cdb633") xysize (300, 1)

                        viewport:
                            style_prefix "archive_sv"
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            xsize 312
                            ysize 462

                            vbox:
                                spacing 7

                                for idx, catalog in enumerate(character_story_catalog):
                                    $ _sb_delay = idx * 0.04
                                    $ _sb_sel = (idx == selected_idx)
                                    $ _vol_live = catalog.any_unlocked
                                    $ _vol_cloth = CS_VOLUME_CLOTH[idx % len(CS_VOLUME_CLOTH)] if _vol_live else "#34373b"

                                    button:
                                        xsize 286
                                        ysize 74
                                        padding (0, 0)
                                        hover_sound gui.hover_sound
                                        activate_sound gui.activate_sound
                                        at cs_tab(_sb_delay)
                                        action SetScreenVariable("selected_idx", idx)
                                        # `selected` is what lets cs_tab react to
                                        # the selection through selected_idle /
                                        # selected_hover instead of being rebuilt.
                                        selected _sb_sel
                                        # Unprefixed, so it holds in every state:
                                        # a volume does not change cloth when
                                        # touched, it moves (cs_tab).
                                        background Solid(_vol_cloth)

                                        fixed:
                                            xysize (286, 74)

                                            # Cloth shading, weave, gilt bands. An
                                            # unopened volume's foil is half gone.
                                            add "assets/gui/menu/illustrated/archive/volume_cloth.svg" alpha (1.0 if _vol_live else 0.5)

                                            # The cameo on the cover, in a gilt rim --
                                            # the same stateless clipper the roster
                                            # uses, so a tall sprite cannot bleed.
                                            fixed:
                                                xysize (54, 54)
                                                xpos 16
                                                yalign 0.5
                                                add Solid("#d9b77b" if _vol_live else "#6f6a63") xysize (54, 54)
                                                add Solid("#1a1418") xpos 1 ypos 1 xysize (52, 52)
                                                add ArchivePortraitCrop(catalog.sprite_image, 50, 50, catalog.portrait_focus, catalog.portrait_scale, catalog.portrait_aspect):
                                                    xpos 2
                                                    ypos 2
                                                    if not _vol_live:
                                                        matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(-0.18)

                                            if _vol_live:
                                                text catalog.name style "cs_sidebar_name" xpos 92 ypos 12

                                                # Progress as one pip per story,
                                                # THREE states, because "I have it"
                                                # and "I have read it" are different
                                                # questions and the player is
                                                # trying to answer the second:
                                                #   paper     read
                                                #   ribbon    recovered, not read yet
                                                #   recessed  still sealed
                                                hbox:
                                                    spacing 4
                                                    xpos 92
                                                    ypos 47
                                                    for _p in range(catalog.total):
                                                        if _p < catalog.completed_count:
                                                            add Solid("#f0e6d2") xysize (12, 4) yalign 0.5
                                                        elif _p < catalog.unlocked_count:
                                                            add Solid("#d0603f") xysize (12, 4) yalign 0.5
                                                        else:
                                                            add Solid("#00000066") xysize (12, 4) yalign 0.5
                                                    text "{}/{}".format(catalog.unlocked_count, catalog.total):
                                                        style "cs_sidebar_count"
                                                        yalign 0.5
                                                        xoffset 6
                                            elif catalog.has_real_stories:
                                                text catalog.name style "cs_sidebar_name_locked" xpos 92 ypos 12
                                                text "SEALED" style "cs_sidebar_count_locked" xpos 92 ypos 47
                                            else:
                                                text catalog.name style "cs_sidebar_name_locked" xpos 92 ypos 12
                                                text "UNWRITTEN" style "cs_sidebar_count_locked" xpos 92 ypos 47

                                            # A ribbon left in a volume that still
                                            # owes the player a story they have not
                                            # read, so it shows without opening it.
                                            if catalog.unread_count:
                                                add "assets/gui/menu/illustrated/archive/bookmark_ribbon.svg" xpos 240 ypos 40

                # The shelf's inner wall: a soft shadow falling onto the book, so
                # the book reads as lying in front of the shelf.
                fixed:
                    xysize (10, 520)
                    add Solid("#02050a66") xysize (8, 520) xpos 1

                # =========================================================
                # RIGHT: THE OPEN BOOK
                # Keyed on selected_idx so the whole spread re-plays
                # cs_sheet_pull -- the chosen volume is laid open every time.
                # Page geometry matches open_book.svg: left page x 18..406,
                # right page x 408..796, gutter at 407.
                # =========================================================
                $ _sel_catalog = character_story_catalog[selected_idx]
                $ _sel_seen = _sel_catalog.any_unlocked
                $ _sel_real = _sel_catalog.has_real_stories
                # THREE bookplate states, because the volume can be complete in
                # two different senses and the player cares about the stricter
                # one. RECOVERED = you hold every story but have not read them
                # all; READ = you have been through the lot. Everything else is
                # INCOMPLETE, i.e. there are still stories you do not have.
                $ _sel_has_all = _sel_real and _sel_catalog.unlocked_count >= _sel_catalog.total
                $ _sel_done = _sel_real and _sel_catalog.completed_count >= _sel_catalog.total
                if _sel_done:
                    $ _cs_plate_word = "Read"
                    $ _cs_plate_style = "cs_plate_word"
                elif _sel_has_all:
                    $ _cs_plate_word = "Recovered"
                    $ _cs_plate_style = "cs_plate_word_new"
                else:
                    $ _cs_plate_word = "Incomplete"
                    $ _cs_plate_style = "cs_plate_word_warn"

                frame:
                    xsize 820
                    ysize 520
                    padding (0, 0)
                    background "assets/gui/menu/illustrated/archive/open_book.svg"
                    at cs_sheet_pull(selected_idx)

                    fixed:
                        xysize (820, 520)

                        # --- LEFT PAGE: the frontispiece ------------------
                        text ("VOLUME " + cs_roman(selected_idx + 1)) style "cs_page_kicker" xpos 212 xanchor 0.5 ypos 30

                        # The portrait, ruled round like a plate in an old book.
                        # ArchivePortraitCrop under archive_portrait, not a
                        # viewport -- a viewport keeps the PREVIOUS subject's
                        # pan when the screen is re-shown, which is exactly
                        # what changing volumes does.
                        add Solid("#71496699") xpos 121 ypos 52 xysize (182, 1)
                        add Solid("#71496699") xpos 121 ypos 265 xysize (182, 1)
                        add Solid("#71496699") xpos 121 ypos 52 xysize (1, 214)
                        add Solid("#71496699") xpos 302 ypos 52 xysize (1, 214)
                        fixed:
                            xpos 127
                            ypos 58
                            xysize (170, 202)
                            use archive_portrait(_sel_catalog.sprite_image, 170, 202, "cover", not _sel_seen, _sel_catalog.portrait_focus, _sel_catalog.portrait_scale, _sel_catalog.portrait_aspect)

                        text _sel_catalog.name style "cs_panel_charname" xpos 212 xanchor 0.5 ypos 276

                        if _sel_seen:
                            text "{} OF {} STORIES RECOVERED".format(_sel_catalog.unlocked_count, _sel_catalog.total):
                                style "cs_panel_subtitle"
                                xpos 212
                                xanchor 0.5
                                ypos 320
                        elif _sel_real:
                            text "SUBJECT NOT YET ENCOUNTERED" style "cs_panel_subtitle_locked" xpos 212 xanchor 0.5 ypos 320
                        else:
                            text "NO STORIES ON RECORD" style "cs_panel_subtitle_locked" xpos 212 xanchor 0.5 ypos 320

                        # The bookplate, pasted in at a slight tilt. Keyed on the
                        # volume so it settles afresh each time one is opened.
                        if _sel_real:
                            frame:
                                style "cs_bookplate"
                                xpos 212
                                ypos 410
                                anchor (0.5, 0.5)
                                at cs_stamp(-3, selected_idx)

                                vbox:
                                    spacing 2
                                    text "EX LIBRIS" style "cs_plate_kicker" xalign 0.5
                                    text _cs_plate_word style _cs_plate_style xalign 0.5

                        text str(selected_idx * 2 + 1) style "cs_folio" xpos 212 xanchor 0.5 ypos 482

                        # --- RIGHT PAGE: the contents ---------------------
                        add Solid("#714966") xysize (6, 6) rotate 45 xpos 540 ypos 33
                        text "CONTENTS" style "cs_toc_head" xpos 602 xanchor 0.5 ypos 30
                        add Solid("#714966") xysize (6, 6) rotate 45 xpos 658 ypos 33
                        add Solid("#9b816766") xpos 452 ypos 56 xysize (300, 1)

                        # The column is 330 wide starting at x 440; the viewport
                        # adds 16px for the hover pull to travel into and 6 for
                        # the scrollbar, so a pulled line is never clipped.
                        viewport:
                            style_prefix "archive_sv"
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            xpos 440
                            ypos 70
                            xsize 352
                            ysize 400

                            vbox:
                                spacing 6

                                if _sel_real:
                                    # KEYED ON THE VOLUME, NOT ON THE LINE'S
                                    # POSITION. SL2 caches a loop's children by
                                    # LOOP COUNTER unless told otherwise, so
                                    # switching volumes handed the new book the
                                    # old one's displayables wherever the
                                    # positions lined up -- transform and all,
                                    # already settled at the end of its entrance.
                                    # The catalog's name rather than the story's
                                    # own key, so a re-enabled "???" placeholder
                                    # -- which carries no key at all -- cannot
                                    # collide with another one.
                                    for sidx, story index (_sel_catalog.name, sidx) in enumerate(_sel_catalog.stories):
                                        # Skip empty placeholder entries entirely.
                                        if story.persistent_key:
                                            button:
                                                style "cs_toc_button"
                                                at cs_slip(sidx * 0.07)

                                                # Unlocked -> leave both menu screens and
                                                # start with clean per-game state. Locked -> dialog.
                                                if story.unlocked:
                                                    action Function(archive_start_isolated_content, story.label_name)
                                                else:
                                                    action Show("dialog", message="This story is still locked.", ok_action=Hide("dialog"))

                                                fixed:
                                                    xysize (330, 100)

                                                    text (cs_roman(sidx + 1) + "."):
                                                        style ("cs_story_num" if story.unlocked else "cs_story_num_locked")
                                                        xpos 0
                                                        ypos 9

                                                    vbox:
                                                        xpos 42
                                                        ypos 9
                                                        spacing 4
                                                        xmaximum 238
                                                        if story.unlocked:
                                                            text story.title style "cs_story_title"
                                                            if story.description:
                                                                text story.description style "cs_story_desc"
                                                        else:
                                                            text "Sealed" style "cs_story_title_locked"
                                                            text "Encounter this character in the story to recover it." style "cs_story_locked_label"

                                                    # An unread story keeps its
                                                    # ribbon; a read one just says
                                                    # so, quietly.
                                                    if story.unread:
                                                        text "NEW" style "cs_story_state_new" xanchor 1.0 xpos 312 ypos 12
                                                        add "assets/gui/menu/illustrated/archive/bookmark_ribbon.svg" xpos 318 ypos 0
                                                    elif story.unlocked:
                                                        text "READ" style "cs_story_state" xanchor 1.0 xpos 330 ypos 12
                                                    else:
                                                        text "SEALED" style "cs_story_state_locked" xanchor 1.0 xpos 330 ypos 12

                                                    add Solid("#9b816744") xysize (330, 1) ypos 99
                                else:
                                    # Empty state -- a volume with nothing in it yet.
                                    fixed:
                                        xysize (330, 300)
                                        text "This volume has not been written yet." style "cs_story_locked_label" xalign 0.5 ypos 140

                        text str(selected_idx * 2 + 2) style "cs_folio" xpos 602 xanchor 0.5 ypos 482

    # Engraved corners framing the shell (cohesion with the archive hub).
    use archive_shell_brackets()

# ----- Styles -----
# Cloth, gilt and printer's ink: gilt lettering on the shelf, ink on the pages.

# The shelf
style cs_drawer_label is archive_meta_text:
    size 10
    kerning 3.0

style cs_sidebar_name is gui_text:
    font gui.default_font
    size 20
    color "#ead6a8"
    outlines [(1, "#00000066", 0, 1)]

style cs_sidebar_name_locked is cs_sidebar_name:
    color "#8c8478"
    outlines []

style cs_sidebar_count is gui_text:
    font gui.interface_font
    size 10
    kerning 1.2
    color "#e3d3b0"
    outlines []

style cs_sidebar_count_locked is cs_sidebar_count:
    color "#77716a"

# The frontispiece page
style cs_page_kicker is gui_text:
    font gui.interface_font
    size 10
    kerning 2.4
    color "#714966"
    outlines []

style cs_panel_charname is gui_text:
    font gui.default_font
    size 30
    color IM_INK
    outlines []

style cs_panel_subtitle is cs_page_kicker:
    kerning 1.4
    color "#6c5f66"

style cs_panel_subtitle_locked is cs_panel_subtitle:
    color "#988d88"

style cs_folio is gui_text:
    font gui.default_font
    size 13
    color "#8a7d72"
    outlines []

# The bookplate: plum ink on a pasted label, the word coloured by state.
style cs_bookplate is frame:
    background Frame("assets/gui/menu/illustrated/archive/bookplate.svg", 14, 14)
    padding (26, 10, 26, 12)

style cs_plate_kicker is cs_page_kicker:
    size 9

style cs_plate_word is gui_text:
    font gui.default_font
    size 21
    color "#2c5b59"
    outlines []

style cs_plate_word_new is cs_plate_word:
    color "#714966"

style cs_plate_word_warn is cs_plate_word:
    color "#8a3b3b"

# The contents page
style cs_toc_head is cs_page_kicker:
    size 12
    kerning 3.0

style cs_toc_button:
    xysize (330, 100)
    padding (0, 0)
    background None
    hover_background Solid("#71496612")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style cs_story_num is gui_text:
    font gui.default_font
    size 21
    color "#714966"
    outlines []

style cs_story_num_locked is cs_story_num:
    color "#a39a92"

style cs_story_title is gui_text:
    font gui.default_font
    size 20
    color IM_INK
    hover_color "#246c60"
    outlines []

style cs_story_title_locked is cs_story_title:
    color "#958b84"
    hover_color "#7d736d"

style cs_story_desc is gui_text:
    font gui.default_font
    size 15
    color "#5e5558"
    outlines []

style cs_story_locked_label is cs_story_desc:
    size 14
    color "#958b84"

style cs_story_state is gui_text:
    font gui.interface_font
    size 10
    kerning 1.4
    color "#2c5b59"
    outlines []

style cs_story_state_new is cs_story_state:
    color "#b8492f"

style cs_story_state_locked is cs_story_state:
    color "#a39a92"
