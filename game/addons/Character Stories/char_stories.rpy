# =============================================================================
# char_stories.rpy  --  CHARACTER STORIES HUB (archive feature)
# =============================================================================
#
# WHAT THIS FILE PROVIDES
#   The "Side Stories" browser: a sidebar of characters on the left, and on the
#   right a panel listing that character's standalone short stories. Each story
#   is its own Matsu'Py label living in a sibling cs_<name>_NN.rpy file; selecting
#   an unlocked story Starts that label (leaving the menu entirely).
#
# HOW IT IS REACHED
#   - Archive "Side Stories" card -> Show("character_stories")  (see game/archive.rpy;
#     note the card is labelled "Side Stories" but opens this "character_stories" screen).
#
# THE DATA MODEL (character_story_catalog, built in init python below)
#   character_story_catalog = [ CharacterStoryCatalog(...) , ... ]
#   - CharacterStoryEntry(title, description, label_name, persistent_key)
#       label_name     : the Matsu'Py label to Start() (defined in a cs_*.rpy file).
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
            self.label_name = label_name        # label to Start() when picked
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
                CharacterStoryEntry("Dead Fantasy", "Two armies meet at Greywake Field.", "cs_matsuda_01", "cs_matsuda_01_unlocked"),  # not ready yet
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
# THE METAPHOR: this screen is a FILE DRAWER, not a menu. The left rail is the
# drawer itself, holding one hanging tab per subject; the right pane is the sheet
# you have pulled out of it. Every animation below exists to sell that -- tabs
# ride sideways in their runners, the sheet lifts up out of the drawer when you
# change subject, and the individual file slips slide further out under the
# pointer. Nothing here fades in place, because paper does not fade.
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

# Pulsing accent rail marking the selected tab / sheet spine.
# The status stamp: a rubber stamp thumped onto the sheet, slightly off-square.
#
# rotate_pad TRUE, deliberately. With it False the rotated render keeps the
# child's UNROTATED size, so anything the rotation swings outside that box is
# cropped -- and a wide, shallow box turned 11 degrees swings a long way: a
# 215x40 stamp needs 219x80 to land in, so the corners were being sliced off. The
# stamp is centred in a fixed holder, so padding it out costs nothing but the
# transparent margin.
transform cs_stamp(ang=-11):
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

# ----- Main Screen (subject roster + dossier) -----
# selected_idx (screen-local) picks which character's "case file" shows on the
# right. The layout reads as a recovered-files dossier: a roster of subjects on
# the left; a portrait + progress header and a stack of FILE cards on the right.
screen character_stories():
    modal True

    # Selected character index -- defaults to first in list.
    default selected_idx = 0

    use archive_backdrop

    key "game_menu" action Hide("character_stories")
    key "K_ESCAPE" action Hide("character_stories")

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

            use archive_header("SIDE STORIES", Hide("character_stories"))

            # Subsystem readout strip (mirrors the archive hub meta line).
            # `fixed` + xanchor, not an hbox with a greedy `null xfill`: a box given
            # an explicit xsize stops packing its children left and spreads them
            # instead, so the right-hand readout never reached the right edge.
            # The shared archive readout strip, kept in the dossier typeface.
            # The right-hand readout answers the question the player actually
            # opened this screen with -- "is there anything in here I have not
            # read" -- and falls back to the subject census once there is not.
            if _cs_files_unread:
                $ _cs_right_readout = "{} UNREAD".format(_cs_files_unread)
            else:
                $ _cs_right_readout = "SUBJECTS {}/{}".format(_cs_subjects_seen, _cs_subject_total)

            use archive_readout(
                "SIDE-STORY ARCHIVE // {}/{} FILES RECOVERED".format(_cs_files_found, _cs_files_total),
                _cs_right_readout,
                text_style="cs_meta_text")

            # THE CONTENT ROW IS 1150 WIDE AND CENTRED, because that is the width
            # of the readout rail above it (archive_readout's default, and the
            # house grid every archive sub-screen is built on). The rail centres
            # itself in the shell's 1152px inner width; this row used to total
            # 1148 and pack left, so the rail overhung the panels by 3px on the
            # right and sat 1px inside them on the left. 320 + 10 + 820 = 1150,
            # and the xalign makes it land on the rail exactly.
            hbox:
                spacing 0
                xalign 0.5

                # =========================================================
                # LEFT: THE DRAWER
                # A stack of hanging tabs, one per subject. The runner is 312 wide
                # (306 of it usable, 6 for the scrollbar) and a tab is 286, so the
                # selected tab -- drawn 14px out toward the sheet by cs_tab() --
                # ends exactly on the drawer label's right edge at 300, while the
                # ones still stowed sit flush on its left edge at 0. See cs_tab
                # for why the pull may not run the other way.
                # =========================================================
                frame:
                    xsize 320
                    ysize 520
                    style "archive_sidebar_panel"
                    padding (8, 12, 0, 12)

                    vbox:
                        spacing 8

                        # Drawer label, stencilled on the front of the drawer. Its
                        # two ends are the two ends of a tab's travel: 0 is where a
                        # stowed tab starts, 300 is where a pulled one finishes.
                        fixed:
                            xsize 300
                            ysize 18
                            text "DRAWER 01" style "cs_drawer_label" xpos 0 yalign 0.5
                            text "SUBJECTS" style "cs_drawer_label" xanchor 1.0 xpos 300 yalign 0.5

                        add Solid("#56d7ff2e") xysize (300, 1)

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

                                        # A pulled tab catches the light; the ones
                                        # still in the drawer sit in its shadow.
                                        # Set unconditionally and let the button's
                                        # own state pick, so a selection change
                                        # never rebuilds this subtree.
                                        background Solid("#060d16d8")
                                        hover_background Solid("#0d1c2bee")
                                        selected_background Solid("#12314af2")
                                        selected_hover_background Solid("#17415fee")

                                        fixed:
                                            xysize (286, 74)

                                            # The tab's spine, and the notch that
                                            # makes it read as a folder tab rather
                                            # than a list row: the spine is inset
                                            # top and bottom so the corners cut in.
                                            if _sb_sel:
                                                add Solid("#56d7ff") xysize (5, 54) xpos 0 yalign 0.5 at enter_m_pip_pulse
                                                add Solid("#56d7ff") xysize (18, 2) xpos 5 ypos 10
                                                add Solid("#56d7ff") xysize (18, 2) xpos 5 ypos 62
                                            else:
                                                add Solid("#16303f") xysize (5, 54) xpos 0 yalign 0.5

                                            # Subject thumbnail -- the same stateless
                                            # clipper the roster uses, so a tall
                                            # sprite cannot bleed out of the chip.
                                            fixed:
                                                xysize (52, 52)
                                                xpos 18
                                                yalign 0.5
                                                add Solid("#07101add") xysize (52, 52)
                                                add ArchivePortraitCrop(catalog.sprite_image, 52, 52, catalog.portrait_focus, catalog.portrait_scale, catalog.portrait_aspect):
                                                    if not catalog.any_unlocked:
                                                        matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(-0.18)
                                                add Solid("#56d7ff44") xysize (52, 1) ypos 51

                                            vbox:
                                                spacing 5
                                                xpos 82
                                                yalign 0.5

                                                if catalog.any_unlocked:
                                                    text catalog.name style "cs_sidebar_name"

                                                    # Progress as FILE NOTCHES -- one
                                                    # notch per file in the folder.
                                                    # A drawer does not have a
                                                    # percentage bar. THREE states,
                                                    # not two, because "I have it" and
                                                    # "I have read it" are different
                                                    # questions and the player is
                                                    # trying to answer the second one:
                                                    #   amber  recovered, not read yet
                                                    #   cyan   read
                                                    #   dark   still sealed
                                                    # Amber is the archive's existing
                                                    # attention colour (the dev menu's
                                                    # PARTIAL state), and it is the
                                                    # unread one because unread is the
                                                    # state the player is looking for.
                                                    hbox:
                                                        spacing 4
                                                        yalign 0.5
                                                        for _p in range(catalog.total):
                                                            if _p < catalog.completed_count:
                                                                add Solid("#56d7ff") xysize (14, 5) yalign 0.5
                                                            elif _p < catalog.unlocked_count:
                                                                add Solid("#ffd166") xysize (14, 5) yalign 0.5
                                                            else:
                                                                add Solid("#22303c") xysize (14, 5) yalign 0.5
                                                        text "{}/{}".format(catalog.unlocked_count, catalog.total):
                                                            style "cs_sidebar_count"
                                                            yalign 0.5
                                                            xoffset 6
                                                elif catalog.has_real_stories:
                                                    text catalog.name style "cs_sidebar_name_locked"
                                                    text "SEALED" style "cs_sidebar_count_locked"
                                                else:
                                                    text catalog.name style "cs_sidebar_name_locked"
                                                    text "EMPTY FOLDER" style "cs_sidebar_count_locked"

                                            # UNREAD FLAG on the tab itself, so the
                                            # player can see which folders still owe
                                            # them something without opening each one.
                                            # Pinned to the tab's right edge; it
                                            # breathes, because a static dot in a
                                            # screen this busy just reads as trim.
                                            if catalog.unread_count:
                                                fixed:
                                                    xysize (26, 26)
                                                    xpos 252
                                                    ypos 8
                                                    add Solid("#ffd166") xysize (9, 9) align (0.5, 0.5) at enter_m_pip_pulse

                # The drawer's inner wall: a hard edge plus a soft shadow falling
                # onto the sheet, so the sheet reads as being IN FRONT of the rail.
                fixed:
                    xysize (10, 520)
                    add Solid("#56d7ff55") xysize (2, 520) xpos 0
                    add Solid("#02050a66") xysize (8, 520) xpos 2

                # =========================================================
                # RIGHT: THE SHEET YOU PULLED OUT
                # A folder cover (tab, binder margin, punch marks, stamp) with the
                # subject's file slips fanned inside it. Keyed on selected_idx so
                # the whole thing re-plays cs_sheet_pull -- the sheet lifts out of
                # the drawer every time you change tab.
                # =========================================================
                $ _sel_catalog = character_story_catalog[selected_idx]
                $ _sel_seen = _sel_catalog.any_unlocked
                $ _sel_real = _sel_catalog.has_real_stories
                # THREE stamp states now, because the folder can be complete in
                # two different senses and the player cares about the stricter
                # one. RECOVERED = you hold every file but have not read them
                # all; READ = you have been through the lot. Everything else is
                # INCOMPLETE, i.e. there are still files you do not have.
                $ _sel_has_all = _sel_real and _sel_catalog.unlocked_count >= _sel_catalog.total
                $ _sel_done = _sel_real and _sel_catalog.completed_count >= _sel_catalog.total
                $ _sel_unread = _sel_catalog.unread_count

                # Stamp ink. The fills are the OPAQUE equivalents of the washes
                # they replace (#56d7ff26 / #ff6a8a1c over the panel) -- the box
                # is now a border frame wrapping a fill frame, so a translucent
                # fill would let the border colour flood the whole interior. The
                # amber middle state matches the unread notches and the drawer
                # tab dot, so one colour means one thing everywhere on the screen.
                if _sel_done:
                    $ _cs_stamp_label = "READ"
                    $ _cs_stamp_edge = "#56d7ffcc"
                    $ _cs_stamp_fill = "#122c3a"
                    $ _cs_stamp_style = "cs_stamp_text"
                elif _sel_has_all:
                    $ _cs_stamp_label = "RECOVERED"
                    $ _cs_stamp_edge = "#ffd166cc"
                    $ _cs_stamp_fill = "#2a2313"
                    $ _cs_stamp_style = "cs_stamp_text_new"
                else:
                    $ _cs_stamp_label = "INCOMPLETE"
                    $ _cs_stamp_edge = "#ff6a8aaa"
                    $ _cs_stamp_fill = "#211824"
                    $ _cs_stamp_style = "cs_stamp_text_warn"

                fixed:
                    xysize (820, 520)

                    frame:
                        xsize 820
                        ysize 520
                        style "archive_panel"
                        padding (0, 0)
                        at cs_sheet_pull(selected_idx)

                        fixed:
                            xysize (820, 520)

                            # --- the folder's own edges -------------------
                            # A lit top edge and a dark bottom edge give the sheet
                            # thickness; the binder margin down the left, with its
                            # punch marks, is what makes it a sheet of paper rather
                            # than another panel.
                            add Solid("#7fe6ff3a") xysize (820, 1) ypos 0
                            add Solid("#000308aa") xysize (820, 2) ypos 518

                            # The binder margin. It has to be a shade LIGHTER than
                            # the sheet, not darker: drawn dark it vanished into the
                            # gutter beside the drawer wall and the punch marks were
                            # left reading as three loose squares floating in the
                            # divider. Lighter, with its own rule, it reads as the
                            # strip of card the holes are punched through.
                            add Solid("#122636") xysize (46, 520) xpos 0
                            add Solid("#56d7ff3a") xysize (1, 520) xpos 46
                            add Solid("#7fe6ff1c") xysize (46, 1) ypos 0

                            # Punch holes: a dark bore with a lit top lip and a
                            # shadowed bottom one, so each reads as a hole in the
                            # card rather than a printed square.
                            for _hy in (96, 252, 408):
                                add Solid("#01030799") xysize (16, 16) xpos 15 ypos (_hy + 1)
                                add Solid("#02050a") xysize (14, 14) xpos 16 ypos _hy
                                add Solid("#8fe4ff4a") xysize (14, 1) xpos 16 ypos _hy
                                add Solid("#00040a88") xysize (14, 1) xpos 16 ypos (_hy + 13)

                            # --- the tab this sheet came out of -----------
                            # Same cyan as the selected drawer tab, sitting on the
                            # sheet's top-left, so the eye connects the two.
                            fixed:
                                xysize (170, 26)
                                xpos 62
                                ypos 0
                                add Solid("#56d7ff") xysize (170, 3) ypos 0
                                add Solid("#0e2233") xysize (170, 23) ypos 3
                                text _sel_catalog.name.upper() style "cs_sheet_tab" xpos 8 ypos 8

                            # THE SHEET'S TYPE COLUMN: 684px wide, starting 62px in
                            # (16px clear of the binder rule at 46). EVERYTHING in
                            # here is measured against those two numbers -- the
                            # header row, the divider, and the file slips all start
                            # at 62 and end at 746. They used to be three different
                            # widths (674 / 700 / 654 + a per-row fan), which is
                            # what made the stack look like it had slipped.
                            #   header hbox : 150 + 22 + 300 + 22 + 190 = 684
                            #   divider     : 684
                            #   file slips  : 684, in a 706 viewport (684 + the
                            #                 16px hover pull + 6px scrollbar)
                            vbox:
                                xpos 62
                                ypos 30
                                spacing 14

                                # Header: portrait + nameplate + notch progress.
                                hbox:
                                    spacing 22

                                    # Portrait window. ArchivePortraitCrop, not a
                                    # viewport -- a viewport keeps the PREVIOUS
                                    # subject's pan when the screen is re-shown,
                                    # which is exactly what changing tabs does.
                                    use archive_portrait(_sel_catalog.sprite_image, 150, 158, "cover", not _sel_seen, _sel_catalog.portrait_focus, _sel_catalog.portrait_scale, _sel_catalog.portrait_aspect)

                                    vbox:
                                        yalign 0.5
                                        spacing 9

                                        fixed:
                                            xsize 300
                                            ysize 40
                                            add Solid("#56d7ff") xysize (9, 9) xpos 0 yalign 0.5 at console_blink
                                            text _sel_catalog.name style "cs_panel_charname" xpos 19 yalign 0.5

                                        if _sel_seen:
                                            text "{} of {} files recovered".format(_sel_catalog.unlocked_count, _sel_catalog.total):
                                                style "cs_panel_subtitle"
                                        elif _sel_real:
                                            text "Subject not yet encountered":
                                                style "cs_panel_subtitle_locked"
                                        else:
                                            text "No side stories on record":
                                                style "cs_panel_subtitle_locked"

                                        # Progress as file notches, matching the
                                        # drawer tabs -- a row of card edges, one
                                        # per file, rather than a percentage bar.
                                        if _sel_real:
                                            hbox:
                                                spacing 5
                                                for _p in range(_sel_catalog.total):
                                                    if _p < _sel_catalog.completed_count:
                                                        fixed:
                                                            xysize (34, 16)
                                                            add Solid("#56d7ff") xysize (34, 13) ypos 3
                                                            add Solid("#9fe9ff") xysize (34, 3) ypos 0
                                                    elif _p < _sel_catalog.unlocked_count:
                                                        fixed:
                                                            xysize (34, 16)
                                                            add Solid("#ffd166") xysize (34, 13) ypos 3
                                                            add Solid("#ffe9ab") xysize (34, 3) ypos 0
                                                    else:
                                                        fixed:
                                                            xysize (34, 16)
                                                            add Solid("#16222c") xysize (34, 13) ypos 3
                                                            add Solid("#22303c") xysize (34, 3) ypos 0

                                    # The status stamp, thumped on at an angle.
                                    #
                                    # THE BOX IS DRAWN BY THE TEXT, NOT AROUND IT.
                                    # It used to be a hand-sized 130x34 fixed with
                                    # the four edges laid in as Solids and the
                                    # caption floated on top -- and a `fixed` does
                                    # not clip, so "COMPLETE" (~150px in this
                                    # extended face) already hung out of both ends
                                    # and "INCOMPLETE" (~185px) hung further. Two
                                    # nested frames instead: the outer one's 2px
                                    # padding IS the border, the inner one's is the
                                    # margin, and both shrink-wrap the caption, so
                                    # any label of any length is boxed exactly.
                                    # The holder stays a fixed 190 so the header
                                    # row keeps one width for every subject; the
                                    # stamp centres in it and may overhang.
                                    if _sel_real:
                                        fixed:
                                            xysize (190, 158)
                                            yalign 0.5
                                            frame:
                                                align (0.5, 0.5)
                                                background Solid(_cs_stamp_edge)
                                                padding (2, 2)
                                                at cs_stamp(-11)

                                                frame:
                                                    background Solid(_cs_stamp_fill)
                                                    padding (16, 7)
                                                    text _cs_stamp_label style _cs_stamp_style

                                add Solid("#56d7ff22"):
                                    xsize 684
                                    ysize 1

                                # =================================================
                                # THE FILE SLIPS
                                # Individual sheets sticking out of the folder. They
                                # deal themselves out on entry and the pointer pulls
                                # one clear of its neighbours; at rest the stack is
                                # square (see cs_slip). The index sits on a tab
                                # hanging off the slip's left edge rather than in a
                                # boxed column, which is what makes a row read as
                                # paper instead of a table cell.
                                #
                                # The viewport is 22px wider than a slip on purpose:
                                # 16 for the hover pull to travel into and 6 for the
                                # scrollbar, so a hovered slip is never clipped.
                                # =================================================
                                viewport:
                                    style_prefix "archive_sv"
                                    scrollbars "vertical"
                                    mousewheel True
                                    draggable True
                                    xsize 706
                                    ysize 268

                                    vbox:
                                        spacing 9

                                        if _sel_real:
                                            # KEYED ON THE CHARACTER, NOT ON THE
                                            # SLIP'S POSITION. SL2 caches a loop's
                                            # children by LOOP COUNTER unless told
                                            # otherwise, so switching characters
                                            # handed the new folder the old one's
                                            # displayables wherever the positions
                                            # lined up -- transform and all,
                                            # already settled at the end of its
                                            # entrance. Only the surplus slips
                                            # animated, and two characters with
                                            # the same number of stories animated
                                            # nothing at all.
                                            #
                                            # The catalog's name rather than the
                                            # story's own key, so a re-enabled
                                            # "???" placeholder -- which carries
                                            # no key at all -- cannot collide with
                                            # another one.
                                            for sidx, story index (_sel_catalog.name, sidx) in enumerate(_sel_catalog.stories):
                                                # Skip empty placeholder entries entirely.
                                                if story.persistent_key:
                                                    $ _sr_delay = sidx * 0.07
                                                    $ _story_num = "{:02d}".format(sidx + 1)
                                                    # The slip's spine takes the unread
                                                    # amber, so a folder full of files
                                                    # you have not opened is legible as
                                                    # a column of amber edges at a
                                                    # glance -- the same read as looking
                                                    # at real tabs in a real drawer.
                                                    if story.unread:
                                                        $ _sr_ink = "#ffd166"
                                                    elif story.unlocked:
                                                        $ _sr_ink = "#56d7ff"
                                                    else:
                                                        $ _sr_ink = "#3b4b58"

                                                    button:
                                                        xsize 684
                                                        ysize 88
                                                        padding (0, 0)
                                                        hover_sound gui.hover_sound
                                                        activate_sound gui.activate_sound
                                                        at cs_slip(_sr_delay)

                                                        # Unlocked -> tear down BOTH menu screens
                                                        # then Start the label. Locked -> dialog.
                                                        if story.unlocked:
                                                            background Solid("#0a1622ee")
                                                            hover_background Solid("#12314af2")
                                                            action [Hide("character_stories"), Hide("archive"), Start(story.label_name)]
                                                        else:
                                                            background Solid("#050b12dd")
                                                            hover_background Solid("#08131fee")
                                                            action Show("dialog", message="This story is still locked.", ok_action=Hide("dialog"))

                                                        fixed:
                                                            xysize (684, 88)

                                                            # Paper edges: lit top, shadowed bottom.
                                                            add Solid("#7fe6ff26") xysize (684, 1) ypos 0
                                                            add Solid("#00040aaa") xysize (684, 2) ypos 86

                                                            # The slip's index tab, hanging off its
                                                            # left edge like a stuck-on label.
                                                            add Solid(_sr_ink) xysize (4, 88) xpos 0
                                                            fixed:
                                                                xysize (58, 58)
                                                                xpos 4
                                                                yalign 0.5
                                                                add Solid("#56d7ff14" if story.unlocked else "#02060b99") xysize (58, 58)
                                                                text "FILE":
                                                                    style ("cs_file_tag" if story.unlocked else "cs_file_tag_locked")
                                                                    xalign 0.5
                                                                    ypos 9
                                                                text _story_num:
                                                                    style ("cs_story_num" if story.unlocked else "cs_story_num_locked")
                                                                    xalign 0.5
                                                                    ypos 24

                                                            # Title + description.
                                                            vbox:
                                                                xpos 82
                                                                yalign 0.5
                                                                spacing 5
                                                                if story.unlocked:
                                                                    text story.title style "cs_story_title"
                                                                    if story.description:
                                                                        text story.description style "cs_story_desc"
                                                                else:
                                                                    text "SEALED FILE" style "cs_story_title_locked"
                                                                    text "Encounter this character in the story to recover it." style "cs_story_locked_label"

                                                            # Pull affordance, pinned right.
                                                            # An unread file gets the
                                                            # amber chip and says so; a
                                                            # read one keeps the ordinary
                                                            # cyan PULL, because "you have
                                                            # been here" should be the
                                                            # quiet state, not a second
                                                            # thing shouting for attention.
                                                            if story.unread:
                                                                frame:
                                                                    xanchor 1.0
                                                                    xpos 668
                                                                    yalign 0.5
                                                                    background Solid("#ffd166")
                                                                    padding (14, 6)
                                                                    text "UNREAD  >" style "archive_chip_on_text"
                                                            elif story.unlocked:
                                                                frame:
                                                                    xanchor 1.0
                                                                    xpos 668
                                                                    yalign 0.5
                                                                    background Solid("#56d7ff")
                                                                    padding (14, 6)
                                                                    text "RE-READ  >" style "archive_chip_on_text"
                                                            else:
                                                                frame:
                                                                    xanchor 1.0
                                                                    xpos 668
                                                                    yalign 0.5
                                                                    background Solid("#1b2832")
                                                                    padding (14, 6)
                                                                    text "SEALED" style "archive_chip_off_text"
                                        else:
                                            # Empty state -- an empty folder, drawn as
                                            # one blank slip with nothing written on it.
                                            fixed:
                                                xysize (684, 150)
                                                add Solid("#050b12cc") xysize (684, 150)
                                                add Solid("#7fe6ff1a") xysize (684, 1) ypos 0
                                                add Solid("#22303c") xysize (4, 150) xpos 0
                                                vbox:
                                                    align (0.5, 0.5)
                                                    spacing 10
                                                    text "EMPTY FOLDER":
                                                        xalign 0.5
                                                        style "cs_story_title_locked"
                                                    text "No side stories have been filed under this subject yet.":
                                                        xalign 0.5
                                                        style "cs_story_desc"

    # Console brackets framing the shell (cohesion with the archive hub).
    use archive_shell_brackets()

# ----- Styles ----- (cyan-on-near-black, matching the archive theme)

style cs_title:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 36
    color "#f4fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

# Sidebar styles
style cs_sidebar_name:
    size 20
    color "#dff8ff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style cs_sidebar_name_locked:
    size 20
    color "#687787"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style cs_sidebar_count:
    size 14
    color "#9fc9d6"
    outlines [(1, "#02040b", 0, 0)]

style cs_sidebar_count_locked:
    size 14
    color "#4f5b67"
    outlines [(1, "#02040b", 0, 0)]

# Right panel styles
style cs_panel_charname:
    size 32
    color "#f4fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style cs_panel_subtitle:
    size 16
    color "#9fc9d6"
    outlines [(1, "#02040b", 0, 0)]

style cs_panel_subtitle_locked:
    size 16
    color "#4f5b67"
    outlines [(1, "#02040b", 0, 0)]

# Story row styles
style cs_story_title:
    size 21
    color "#dff8ff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style cs_story_desc:
    size 14
    color "#9fc9d6"
    outlines [(1, "#02040b", 0, 0)]

style cs_story_title_locked:
    size 21
    color "#4f5b67"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style cs_story_locked_label:
    size 13
    color "#4f5b67"
    outlines [(1, "#02040b", 0, 0)]

style cs_story_num:
    size 22
    color "#56d7ff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style cs_story_num_locked:
    size 22
    color "#374654"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style cs_story_status:
    size 13
    color "#56d7ff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style cs_story_status_locked:
    size 12
    color "#4f5b67"
    bold True
    outlines [(1, "#02040b", 0, 0)]

# --- New chrome styles (readout strip, FILE tag, status chips) ---------------
style cs_meta_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 13
    color "#5fbcd6"
    outlines [(1, "#02040b", 0, 0)]

style cs_file_tag:
    size 10
    color "#56d7ffaa"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style cs_file_tag_locked:
    size 10
    color "#3a4753"
    bold True
    outlines [(1, "#02040b", 0, 0)]

# --- Drawer / sheet chrome ---------------------------------------------------
# Stencilled label on the front of the drawer.
style cs_drawer_label:
    font gui.interface_font
    size 10
    color "#4f8fa5"
    kerning 3.0
    bold True
    outlines [(1, "#02040b", 0, 0)]

# The tab printed on the pulled sheet, matching the drawer tab it came from.
style cs_sheet_tab:
    font gui.interface_font
    size 11
    color "#9fe9ff"
    kerning 2.0
    bold True
    outlines [(1, "#02040b", 0, 0)]

# The rubber stamp across the header.
style cs_stamp_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 17
    color "#9fe9ff"
    bold True
    kerning 2.0
    outlines [(1, "#02040b", 0, 0)]

style cs_stamp_text_warn is cs_stamp_text:
    color "#ffa8bc"

# "RECOVERED" -- every file is in the folder but not all of them have been read.
# Amber is the unread colour everywhere on this screen: the drawer tab dots, the
# file notches, the slip spines and the UNREAD chip all use it.
style cs_stamp_text_new is cs_stamp_text:
    color "#ffe9ab"
