# Developer tools hub, reached through F9 or the main-menu developer control.
# DEV_HUB_PAGES defines the available pages. The hub owns the sprite viewer;
# achievement, currency, routing and writing tools remain in their own modules.
# dev_hub_has() guards optional tool references. Entry points require
# config.developer; options.rpy excludes this folder from release builds.
# Solid/Text/ATL terminal controls remain readable before shader warmup.

init python:

    # -------------------------------------------------------------------------
    # PAGES
    # One row per page: (key, rail label, the line under the rail label).
    # The dispatcher at the bottom of screen dev_hub() has a matching branch.
    # -------------------------------------------------------------------------
    DEV_HUB_PAGES = (
        ("routing",  "ROUTING",  "Where a session starts."),
        ("unlocks",  "UNLOCKS",  "Side content and achievements."),
        ("firsts",   "FLAGS",   "One-time moments, re-armed."),
        ("economy",  "ECONOMY",  "Matsucoins and the binder."),
        ("combat",   "COMBAT",   "Fights, invasions, godmode."),
        ("sprites",  "SPRITES",  "Cast viewer -- poses and faces."),
        ("writing",  "WRITING",  "Prose, staging and music cues."),
        ("system",   "SYSTEM",   "Build, engine, Ren'Py tools."),
    )

    def dev_hub_has(*names):
        """
        True only if EVERY name is live in the store.

        Every button in the hub reaches into some other addon. That addon may
        not be installed (the folders are independent), may have been renamed,
        or may simply not have loaded yet. Asking first is what lets the hub
        report "NOT INSTALLED" instead of dying on a missing name.
        """
        for name in names:
            if not hasattr(renpy.store, name):
                return False
        return True

    def dev_hub_call(name, *args, **kwargs):
        """Call a store function by name if it exists; otherwise say so."""
        fn = getattr(renpy.store, name, None)
        if fn is None:
            renpy.notify("DEV HUB: %s is not installed." % name)
            return None
        return fn(*args, **kwargs)

    def dev_hub_show(name):
        """Show a screen owned by another addon, or explain why it did not."""
        if not renpy.has_screen(name):
            renpy.notify("DEV HUB: screen %s is not installed." % name)
            return None
        renpy.show_screen(name)
        renpy.restart_interaction()
        return None

    def dev_hub_open_rhythm_editor():
        """Keep the title's menu identity out of the chart editor context."""
        if not config.developer:
            return None
        if not renpy.has_label("asahina_rhythm_chart_editor"):
            renpy.notify("DEV HUB: Asahina's chart editor is not installed.")
            return None
        renpy.call_in_new_context("dev_hub_rhythm_editor_context")
        return None

    def dev_hub_flag(value):
        """(text, colour) for a live on/off/partial readout."""
        if value is True or value == "ENABLED":
            return ("ENABLED", "#37e08a")
        if value == "PARTIAL":
            return ("PARTIAL", "#ffd166")
        if value is None:
            return ("UNAVAILABLE", "#5d7886")
        return ("DISABLED", "#ff6680")

    # -------------------------------------------------------------------------
    # LIVE INVENTORY
    # The hub reports on the modules it fronts rather than duplicating them, so
    # each of these is a read with a fallback and never a copy of a catalog.
    # -------------------------------------------------------------------------
    def dev_hub_route_count():
        if not dev_hub_has("dev_date_jump_available_codes"):
            return None
        try:
            return len(dev_date_jump_available_codes())
        except Exception:
            return None

    def dev_hub_chapter_counts():
        """(open, total) read off Chapter Select's own table, or None if gone.

        Chapter Select decides what is playable by asking the script which
        entry labels exist, so this readout cannot drift from what New Game
        will actually offer -- there is no second list to disagree with.
        """
        if not dev_hub_has("chapter_select_rows"):
            return None
        try:
            rows = chapter_select_rows()
            return (sum(1 for row in rows if row[4]), len(rows))
        except Exception:
            return None

    def dev_hub_ooc_count():
        if not dev_hub_has("dev_out_of_context_scene_catalog"):
            return None
        return len(dev_out_of_context_scene_catalog)

    def dev_hub_ach_counts():
        """(earned, total) or None."""
        if not dev_hub_has("ach_earned_count", "ACHIEVEMENTS"):
            return None
        try:
            return (ach_earned_count(), len(ACHIEVEMENTS))
        except Exception:
            return None

    def dev_hub_ach_ready():
        """How many achievements are satisfied but not yet granted."""
        if not dev_hub_has("ach_status", "ACHIEVEMENTS"):
            return None
        try:
            return len([a for a in ACHIEVEMENTS if ach_status(a) == "ready"])
        except Exception:
            return None

    def dev_hub_card_counts():
        if not dev_hub_has("mc_collection_counts"):
            return None
        try:
            return mc_collection_counts()
        except Exception:
            return None

    def dev_hub_invasion_counts():
        """(playable, fended, total) or None."""
        if not dev_hub_has("INV_ARCHIVISTS", "inv_is_playable", "inv_fended"):
            return None
        try:
            fended = inv_fended()
            return (
                len([a for a in INV_ARCHIVISTS if inv_is_playable(a["slug"])]),
                len([a for a in INV_ARCHIVISTS if a["slug"] in fended]),
                len(INV_ARCHIVISTS),
            )
        except Exception:
            return None

    def dev_hub_side_content_state():
        if not dev_hub_has("dev_date_jump_side_content_state"):
            return None
        try:
            return dev_date_jump_side_content_state()
        except Exception:
            return None

    # -------------------------------------------------------------------------
    # FIRST-TIME FLAGS
    # Every persistent flag that stands between the player and a moment the
    # game plays exactly ONCE. The hub owns this table and nothing else: each
    # row names the file that owns the flag plus a label, screen or store name
    # from that file, and a row whose owner is missing reports NOT INSTALLED
    # rather than offering to write a flag that nothing reads.
    #
    # `armed` is the value the owner reads as "not seen yet" -- the flag's own
    # declared default -- so re-arming puts a profile back exactly where a new
    # install starts. Every write goes through renpy.save_persistent(): a
    # boot-time moment can only be re-tested by quitting and relaunching, and a
    # persistent write that was never flushed does not survive that.
    #
    # DELIBERATELY NOT OFFERED, and listed read-only on the page instead:
    #   one-time MIGRATIONS, which fire on a profile rather than in front of a
    #   player, and flags that share their key with PROGRESS. Re-arming those is
    #   a side effect, not a replay. Per-SAVE one-time flags are not in the
    #   table at all -- the hub runs from the title with no save loaded, and a
    #   new game re-arms them anyway.
    # -------------------------------------------------------------------------
    DEV_HUB_FLAGS = (
        dict(
            key="vault_greeted", label="VAULT GREETING",
            owner="addons/Vault/vault.rpy",
            guard=("label", "vault_greeting"), armed=False,
            replays="Kotonoha waiting in the Vault, the next time it is opened from the Archive."),
        dict(
            key="first_run", label="FIRST-BOOT NOTICE",
            owner="splash.rpy + first_boot_notice.rpy",
            guard=("screen", "enter_m_first_boot_notice"), armed=None,
            replays="The PLEASE READ notice. It lives in the splashscreen, so it plays on the next LAUNCH -- quit and relaunch to see it."),
        dict(
            key="first_poem", label="FIRST POEM HINT",
            owner="addons/poem_display.rpy",
            guard=("label", "enter_m_showpoem"), armed=None,
            replays="The click-to-dismiss hint drawn over the next poem shown."),
        dict(
            key="first_load", label="FIRST LOAD HINT",
            owner="splash.rpy (after_load)",
            guard=("label", "after_load"), armed=None,
            replays="The Skip-button hint after the next load. splash.rpy never shows it while config.developer is True, so it is only testable in a non-developer run."),
    )

    DEV_HUB_ONE_TIME_OTHER = (
        dict(
            key="archive_open_shell_migrated", label="ARCHIVE SHELL MIGRATION",
            owner="archive.rpy", guard=("screen", "archive"), kind="MIGRATION",
            why="Forces five Archive panels open on a profile from before they shipped open. Re-running it only re-opens panels that already ship open."),
        dict(
            key="ach_chapter05_migration_done", label="CHAPTER 0.5 TROPHY MIGRATION",
            owner="Achievements/achievements.rpy", guard=("name", "ACHIEVEMENTS"), kind="MIGRATION",
            why="Copies a pre-rebuild Music Room unlock into chapter05_completed once. The sentinel is what stops ALL SIDE CONTENT's Music Room from counting as finishing Chapter 0.5."),
        dict(
            key="cs_df_tactics_release_seen", label="DEAD FANTASY RELEASE GRANT",
            owner="Character Stories/cs_matsuda_01.rpy", guard=("name", "cs_df_field_dispatch"), kind="MIGRATION",
            why="Grants the side story at init 950 to readers who finished Chapter 0.5 before it shipped -- a boot-time grant, not a scene."),
        dict(
            key="autofocus_dim_mode_chosen", label="SPEAKER FOCUS DEFAULT",
            owner="Autofocus/autofocus.rpy", guard=("name", "autofocus_set_dim_mode"), kind="MIGRATION",
            why="Moves an untouched profile from Opaque to Darken, and is also set when the player picks a mode -- clearing it would second-guess a real choice."),
        dict(
            key="asahina_rhythm_speed_rescaled", label="ASARHYTHM SCROLL SPEED RESCALE",
            owner="Asahina Rhythm/asahina_rhythm.rpy", guard=("name", "ar_scroll_factor"), kind="MIGRATION",
            why="Halves a stored scroll speed once, because 1.0x now means what 2.0x used to. An untouched old 1.0x becomes the new 1.0x instead. Clearing it halves the speed again at the next boot."),
        dict(
            key="kotomode_cleared", label="KOTONOHA MODE CLEAR",
            owner="kotonohamode/kototouhou.rpy", guard=("label", "kototouhou"), kind="PROGRESS",
            why="Picks her first-visit intro over the 'Welcome back' one, but it IS the clear flag -- clearing it re-locks progress rather than replaying a moment."),
    )

    def dev_hub_first_owner_live(entry):
        """Is the file that reads this flag actually installed?"""
        kind, name = entry["guard"]
        if kind == "label":
            return renpy.has_label(name)
        if kind == "screen":
            return renpy.has_screen(name)
        return dev_hub_has(name)

    def dev_hub_first_state(entry):
        """(text, colour): ARMED plays next time, SPENT has already played."""
        if not dev_hub_first_owner_live(entry):
            return ("NOT INSTALLED", "#5d7886")
        if getattr(persistent, entry["key"], None):
            return ("SPENT", "#7f95a3")
        return ("ARMED", "#37e08a")

    def dev_hub_first_set(key, value):
        """Write one first-time flag, flushed so it survives a relaunch."""
        setattr(persistent, key, value)
        renpy.save_persistent()
        renpy.notify("DEV HUB: persistent.%s = %r" % (key, value))
        renpy.restart_interaction()
        return None

    def dev_hub_first_rearm_all():
        """Re-arm every installed first-time moment in one flush."""
        for entry in DEV_HUB_FLAGS:
            if dev_hub_first_owner_live(entry):
                setattr(persistent, entry["key"], entry["armed"])
        renpy.save_persistent()
        renpy.notify("DEV HUB: every installed first-time moment re-armed.")
        renpy.restart_interaction()
        return None


# =============================================================================
# SPRITE VIEWER -- MODEL
# =============================================================================
# WHAT IT READS
#   Nothing is hand-listed. The viewer walks Ren'Py's own image registry
#   (renpy.display.image.image_attributes: {tag: {attribute-tuple: displayable}})
#   and, for anything built with `layeredimage`, the rig's own attribute table.
#   So a face added to def_characters.rpy shows up here the moment it exists,
#   and a sprite folder nobody wired to a Character still appears.
#
# THE THREE AXES
#   POSE    -- which RIG. A tag can own more than one (`layeredimage monika
#              forward` and `layeredimage monika lean`), and each has its own
#              groups, so switching pose resets the selection to that rig's
#              defaults rather than trying to carry attributes across.
#   RIG     -- a layeredimage. Pick one attribute per group (outfit x face x
#              ...) and the composition is live. This is where expressions live.
#              A group that declares no `default` starts EMPTY and can be
#              cleared back to empty, because that is what the engine does with
#              it -- MPT's one-attribute `special` group is exactly that case.
#   VARIANT -- a discrete `image tag a b = ...`. Matsuda's full-body poses are
#              these: they sit OUTSIDE the rig on purpose (def_characters.rpy
#              explains why), so the viewer treats them as their own list rather
#              than pretending they are another face.
#
# WHY SELECTION STATE IS AN init python OBJECT
#   Deliberately session-only. This is a main-menu tool; parking its state in a
#   `default` would write "which face was I looking at" into every save. An
#   init-python object is not saved and not rolled back, which is exactly right
#   here -- see the init-state-not-saved note for the times that is a BUG
#   rather than the intent.
# =============================================================================

init python:

    # Sprites with neither a rig nor a speaking Character to find them by. Add a
    # tag here if a new one-off sprite should be inspectable; ALL TAGS in the
    # viewer's header shows every image tag in the game regardless, so nothing
    # is ever actually hidden -- this list only decides the tidy default view.
    DEV_SPRITE_EXTRA_TAGS = (
        "purg_girl", "purg_girl_day7", "purg_girl_yukata",
        "gary", "gregor", "leif",
    )

    class _DevSpriteState(renpy.object.Object):
        """Everything the viewer is currently looking at."""

        def __init__(self):
            self.tag = None
            self.rig = 0          # which of the tag's rigs (poses) is up
            self.groups = {}      # group name -> chosen attribute
            self.free = set()     # chosen ungrouped attributes
            self.variant = None   # attribute tuple of a discrete image, or None
            self.zoom = 1.0
            self.panx = 0
            self.pany = 0
            self.backdrop = 0
            self.show_all = False
            self.row = 0          # which group row the arrow keys drive

    _dev_sprite = _DevSpriteState()

    # Built on demand and held until REFRESH, because walking every image tag in
    # the game is not free and the answer only changes on a hot reload.
    _dev_sprite_cache = {}

    def dev_sprite_refresh():
        """Drop the cached catalog so a hot-reloaded sprite file is picked up."""
        _dev_sprite_cache.clear()
        renpy.restart_interaction()
        return None

    def _dev_sprite_is_rig(d):
        """True for a layeredimage -- the only thing with a group table."""
        return hasattr(d, "attributes") and hasattr(d, "group_to_attributes")

    def _dev_sprite_entries(tag):
        return renpy.display.image.image_attributes.get(tag, {})

    def dev_sprite_tags(show_all=False):
        """
        Every image tag worth looking at, sorted.

        Three sources, because no single one covers the cast: a layeredimage is
        a character rig by construction; a Character given `image=` names its
        own tag; and the leftovers (the purgatory girl and the Nier forest
        placeholders) are neither, so they are listed by hand above.
        """
        key = "all" if show_all else "cast"
        if key in _dev_sprite_cache:
            return _dev_sprite_cache[key]

        table = renpy.display.image.image_attributes

        if show_all:
            found = set(k for k, v in table.items() if v)
        else:
            found = set()

            for tag, entries in table.items():
                for d in entries.values():
                    if _dev_sprite_is_rig(d):
                        found.add(tag)
                        break

            try:
                for value in list(vars(renpy.store).values()):
                    if isinstance(value, renpy.character.ADVCharacter):
                        image_tag = getattr(value, "image_tag", None)
                        if image_tag and image_tag in table:
                            found.add(image_tag)
            except Exception:
                pass

            for tag in DEV_SPRITE_EXTRA_TAGS:
                if tag in table:
                    found.add(tag)

        result = tuple(sorted(found))
        _dev_sprite_cache[key] = result
        return result

    def dev_sprite_look(tag):
        """
        Split one tag's registry entries into RIGS and VARIANTS.

        A tag can own SEVERAL rigs: `layeredimage monika forward` and
        `layeredimage monika lean` are two poses of one character, registered
        under ("forward",) and ("lean",). Treating all but one of them as a
        discrete image would have hidden half the DDLC cast's poses behind a
        chip that ignored every expression control, so a pose is its own axis.
        """
        cache_key = ("look", tag)
        if cache_key in _dev_sprite_cache:
            return _dev_sprite_cache[cache_key]

        entries = _dev_sprite_entries(tag)

        rigs = []
        variants = []

        for attrs in sorted(entries.keys()):
            d = entries[attrs]
            if _dev_sprite_is_rig(d):
                rigs.append((tuple(attrs), d))
            else:
                variants.append(tuple(attrs))

        look = {"rigs": rigs, "variants": variants}
        _dev_sprite_cache[cache_key] = look
        return look

    def dev_sprite_rig_look(tag, index):
        """
        One rig's own group table, in declaration order.

        Returns None if the tag has no rig, or the index is off the end.
        Otherwise a dict of:
            prefix   -- the attributes the rig is registered under, which every
                        name for it must carry
            rig      -- the LayeredImage
            groups   -- [(group, (attribute, ...)), ...]
            defaults -- {group: attribute} for groups that declared a `default`
            free     -- ungrouped attributes, which are independent toggles
        """
        cache_key = ("rig", tag, index)
        if cache_key in _dev_sprite_cache:
            return _dev_sprite_cache[cache_key]

        rigs = dev_sprite_look(tag)["rigs"]
        if not rigs or index >= len(rigs):
            return None

        prefix, rig = rigs[index]

        order = []
        members = {}
        defaults = {}
        free = []
        seen_pair = set()
        seen_free = set()

        # Declaration order matters and set order does not, so the rig's
        # `attributes` list is walked directly rather than reading
        # group_to_attributes (which is a defaultdict of sets).
        for a in getattr(rig, "attributes", ()):
            group, name = a.group, a.attribute

            if group is None:
                if name not in seen_free:
                    seen_free.add(name)
                    free.append(name)
                continue

            if group not in members:
                members[group] = []
                order.append(group)

            if (group, name) not in seen_pair:
                seen_pair.add((group, name))
                members[group].append(name)

            if a.default and group not in defaults:
                defaults[group] = name

        rig_look = {
            "prefix": tuple(prefix),
            "rig": rig,
            "groups": [(g, tuple(members[g])) for g in order],
            "defaults": defaults,
            "free": tuple(free),
        }
        _dev_sprite_cache[cache_key] = rig_look
        return rig_look

    def dev_sprite_current_rig():
        """The rig look the viewer is pointed at, or None."""
        if _dev_sprite.tag is None:
            return None
        return dev_sprite_rig_look(_dev_sprite.tag, _dev_sprite.rig)

    def dev_sprite_apply_rig_defaults():
        """
        Reset every group to what the rig itself declares.

        A group with NO `default` marker starts EMPTY, and is meant to: that is
        exactly what the engine does with it. Falling back to "first declared"
        instead looked reasonable and was wrong -- MPT's `special` group holds
        one attribute, s_scream, nothing marks it default, and every DDLC girl
        opened the viewer mid-scream.
        """
        rig_look = dev_sprite_current_rig()

        _dev_sprite.groups = {}
        if rig_look is None:
            return

        for group, _names in rig_look["groups"]:
            if group in rig_look["defaults"]:
                _dev_sprite.groups[group] = rig_look["defaults"][group]

    def dev_sprite_select_tag(tag):
        """Point the viewer at a character and reset it to that rig's defaults."""
        look = dev_sprite_look(tag)

        _dev_sprite.tag = tag
        _dev_sprite.rig = 0
        _dev_sprite.free = set()
        _dev_sprite.row = 0
        _dev_sprite.panx = 0
        _dev_sprite.pany = 0
        _dev_sprite.variant = None

        if look["rigs"]:
            dev_sprite_apply_rig_defaults()
        elif look["variants"]:
            # A tag with no rig at all (a lone `image purg_girl = ...`) only has
            # variants, so one of them has to be the opening view.
            _dev_sprite.variant = look["variants"][0]

        renpy.restart_interaction()
        return None

    def dev_sprite_select_rig(index):
        """
        Switch pose.

        Group membership is per-rig, so the selection cannot carry across --
        `forward` and `lean` do not have to name their groups the same way, let
        alone their attributes. Reset to the new rig's own defaults.
        """
        _dev_sprite.variant = None
        _dev_sprite.rig = index
        _dev_sprite.row = 0
        _dev_sprite.free = set()
        dev_sprite_apply_rig_defaults()
        renpy.restart_interaction()
        return None

    def dev_sprite_cycle_rig(step):
        rigs = dev_sprite_look(_dev_sprite.tag)["rigs"] if _dev_sprite.tag else []
        if len(rigs) < 2:
            return None
        return dev_sprite_select_rig((_dev_sprite.rig + step) % len(rigs))

    def dev_sprite_ensure():
        """Make sure something is selected before the viewer tries to draw."""
        tags = dev_sprite_tags(_dev_sprite.show_all)
        if not tags:
            return None
        if _dev_sprite.tag not in tags:
            dev_sprite_select_tag(tags[0])
        return _dev_sprite.tag

    def dev_sprite_set(group, name):
        """
        Choose one attribute inside a group, and leave variant mode.

        Clicking also moves the ACTIVE ROW to that group, so the arrow keys keep
        driving whatever the mouse last touched instead of some other row the
        keyboard was left pointing at.
        """
        _dev_sprite.variant = None
        _dev_sprite.groups[group] = name

        rig_look = dev_sprite_current_rig()
        if rig_look is not None:
            for index, (candidate, _names) in enumerate(rig_look["groups"]):
                if candidate == group:
                    _dev_sprite.row = index
                    break

        renpy.restart_interaction()
        return None

    def dev_sprite_clear(group):
        """Take a group back to showing nothing. Only legal without a default."""
        _dev_sprite.variant = None
        _dev_sprite.groups.pop(group, None)
        renpy.restart_interaction()
        return None

    def dev_sprite_toggle_free(name):
        """Ungrouped attributes are independent, so they toggle rather than pick."""
        _dev_sprite.variant = None
        if name in _dev_sprite.free:
            _dev_sprite.free.discard(name)
        else:
            _dev_sprite.free.add(name)
        renpy.restart_interaction()
        return None

    def dev_sprite_set_variant(attrs):
        _dev_sprite.variant = tuple(attrs) if attrs is not None else None
        renpy.restart_interaction()
        return None

    def dev_sprite_cycle_variant(step):
        variants = dev_sprite_look(_dev_sprite.tag)["variants"] if _dev_sprite.tag else []
        if not variants:
            return None
        try:
            index = variants.index(_dev_sprite.variant)
        except ValueError:
            index = -1 if step > 0 else 0
        return dev_sprite_set_variant(variants[(index + step) % len(variants)])

    def dev_sprite_group_options(rig_look, group):
        """
        Everything the active row can cycle to.

        A group with no declared default can legitimately show NOTHING, so None
        is a real option in the ring rather than a missing one.
        """
        names = dict(rig_look["groups"]).get(group, ())
        options = list(names)
        if group not in rig_look["defaults"]:
            options.append(None)
        return options

    def dev_sprite_cycle_group(step):
        """Arrow-key cycling through the active group's attributes."""
        tag = dev_sprite_ensure()
        if tag is None:
            return None

        rig_look = dev_sprite_current_rig()
        if rig_look is None or not rig_look["groups"]:
            return dev_sprite_cycle_variant(step)

        row = max(0, min(_dev_sprite.row, len(rig_look["groups"]) - 1))
        group = rig_look["groups"][row][0]

        options = dev_sprite_group_options(rig_look, group)
        if not options:
            return None

        try:
            index = options.index(_dev_sprite.groups.get(group))
        except ValueError:
            index = 0

        chosen = options[(index + step) % len(options)]
        return dev_sprite_clear(group) if chosen is None else dev_sprite_set(group, chosen)

    def dev_sprite_cycle_row(step):
        tag = dev_sprite_ensure()
        if tag is None:
            return None
        rig_look = dev_sprite_current_rig()
        if rig_look is None or not rig_look["groups"]:
            return None
        _dev_sprite.row = (_dev_sprite.row + step) % len(rig_look["groups"])
        renpy.restart_interaction()
        return None

    def dev_sprite_cycle_tag(step):
        tags = dev_sprite_tags(_dev_sprite.show_all)
        if not tags:
            return None
        try:
            index = tags.index(_dev_sprite.tag)
        except ValueError:
            index = 0
        return dev_sprite_select_tag(tags[(index + step) % len(tags)])

    def dev_sprite_toggle_show_all():
        _dev_sprite.show_all = not _dev_sprite.show_all
        _dev_sprite_cache.pop("cast", None)
        _dev_sprite_cache.pop("all", None)
        dev_sprite_ensure()
        renpy.restart_interaction()
        return None

    # --- the composed image ---------------------------------------------------

    def dev_sprite_attributes():
        """The attribute list the current selection resolves to."""
        if _dev_sprite.tag is None:
            return ()

        if _dev_sprite.variant is not None:
            return tuple(_dev_sprite.variant)

        rig_look = dev_sprite_current_rig()
        if rig_look is None:
            return ()

        attrs = list(rig_look["prefix"])
        for group, _names in rig_look["groups"]:
            chosen = _dev_sprite.groups.get(group)
            if chosen:
                attrs.append(chosen)
        attrs.extend(sorted(_dev_sprite.free))
        return tuple(attrs)

    def dev_sprite_show_line():
        """The exact `show` statement for what is on the stage, ready to paste."""
        if _dev_sprite.tag is None:
            return ""
        return " ".join(("show", _dev_sprite.tag) + dev_sprite_attributes())

    def dev_sprite_displayable(width, height):
        """
        The current selection, fitted into a box and then zoomed and panned.

        Fit and zoom are two NESTED Transforms rather than one: `fit` sizes the
        child against xysize, and stacking a zoom into the same Transform would
        make the order they apply in a matter of engine internals instead of a
        matter of what is written here.
        """
        if _dev_sprite.tag is None:
            return None

        name = " ".join((_dev_sprite.tag,) + dev_sprite_attributes())

        try:
            fitted = Transform(name, fit="contain", xysize=(width, height))
            return Transform(
                fitted,
                zoom=_dev_sprite.zoom,
                xoffset=_dev_sprite.panx,
                yoffset=_dev_sprite.pany,
            )
        except Exception:
            return None

    def dev_sprite_unsatisfied():
        """
        Selected attributes whose own if_all / if_any / if_not rules exclude
        them from this combination -- so they contribute NOTHING to the picture.

        This is the failure the viewer exists to make visible: a face that only
        has a casual plate, shown over the uniform body, does not error. It
        quietly draws a body with no face on it.
        """
        if _dev_sprite.tag is None or _dev_sprite.variant is not None:
            return ()

        rig_look = dev_sprite_current_rig()
        if rig_look is None:
            return ()

        try:
            attrs = set(dev_sprite_attributes())
            missing = []

            for name in sorted(attrs):
                known = False
                drawn = False

                for a in rig_look["rig"].attributes:
                    if a.attribute != name:
                        continue
                    known = True
                    if a.check(attrs):
                        drawn = True
                        break

                if known and not drawn:
                    missing.append(name)

            return tuple(missing)
        except Exception:
            return ()

    def _dev_sprite_filename(d, depth=0):
        """Dig a real file path out of whatever the rig wrapped the layer in."""
        if d is None or depth > 8:
            return None

        name = getattr(d, "filename", None)
        if isinstance(name, basestring):
            return name

        try:
            children = d.visit()
        except Exception:
            return None

        for child in (children or ()):
            found = _dev_sprite_filename(child, depth + 1)
            if found:
                return found

        return None

    def dev_sprite_layer_files():
        """
        [(group, attribute, path)] for every layer actually drawn right now.

        The point is sprite AUTHORING: when a face looks wrong, this says which
        file on disk is the one to go and fix. A layer whose art is a Null (the
        MPT rigs use those to carry mood and outfit as pure state) has no path,
        and says so rather than being dropped.
        """
        if _dev_sprite.tag is None:
            return ()

        rig_look = dev_sprite_current_rig()

        if _dev_sprite.variant is not None or rig_look is None:
            entries = _dev_sprite_entries(_dev_sprite.tag)
            attrs = tuple(_dev_sprite.variant or ())
            path = _dev_sprite_filename(entries.get(attrs))
            return ((("-", " ".join(attrs) or "(base)", path or "--"),))

        try:
            attrs = set(dev_sprite_attributes())
            rows = []

            for a in rig_look["rig"].attributes:
                if a.attribute in attrs and a.check(attrs):
                    rows.append((
                        a.group or "-",
                        a.attribute,
                        _dev_sprite_filename(a.image) or "--",
                    ))

            return tuple(rows)
        except Exception:
            return ()

    # --- layout ---------------------------------------------------------------

    def dev_sprite_chip_width(label):
        """
        Width of one attribute chip.

        Chips are laid out by hand because Ren'Py has no flow box, so the width
        used for the wrap arithmetic and the width the button is actually given
        have to be the SAME number -- otherwise rows silently overflow the panel
        they are wrapped inside.
        """
        return max(46, int(7.4 * len(str(label))) + 22)

    def dev_sprite_wrap(labels, width, gap=6):
        """Chunk chips into rows that fit `width`."""
        rows = []
        row = []
        used = 0

        for label in labels:
            chip = dev_sprite_chip_width(label)
            if row and used + gap + chip > width:
                rows.append(row)
                row, used = [], 0
            used += (gap if row else 0) + chip
            row.append(label)

        if row:
            rows.append(row)

        return rows

    DEV_SPRITE_BACKDROPS = (
        ("DARK",  "#0b0f16"),
        ("BLACK", "#000000"),
        ("GREY",  "#7f7f7f"),
        ("WHITE", "#ffffff"),
        ("KEY",   "#ff00ff"),
    )

    DEV_SPRITE_ZOOMS = (0.5, 0.75, 1.0, 1.5, 2.0, 3.0)

    # The active-row marker, U+2023, as a literal character. Measured: every
    # triangle glyph this project has reached for draws as tofu in all three
    # fonts EXCEPT this one in the interface font. It lives here rather than
    # inline in the screen because a screen string is not a Python string --
    # the lexer hands a backslash-u escape straight through to the font.
    DEV_SPRITE_MARK = u"‣"

    def dev_sprite_zoom_step(step):
        try:
            index = DEV_SPRITE_ZOOMS.index(_dev_sprite.zoom)
        except ValueError:
            index = 2
        bounded = max(0, min(index + step, len(DEV_SPRITE_ZOOMS) - 1))
        _dev_sprite.zoom = DEV_SPRITE_ZOOMS[bounded]
        renpy.restart_interaction()
        return None

    def dev_sprite_set_backdrop(index):
        _dev_sprite.backdrop = index % len(DEV_SPRITE_BACKDROPS)
        renpy.restart_interaction()
        return None

    def dev_sprite_pan(dx, dy):
        _dev_sprite.panx += dx
        _dev_sprite.pany += dy
        renpy.restart_interaction()
        return None

    def dev_sprite_reset_view():
        _dev_sprite.zoom = 1.0
        _dev_sprite.panx = 0
        _dev_sprite.pany = 0
        renpy.restart_interaction()
        return None


# =============================================================================
# ANIMATION
# Everything here is ATL over Solids and Text. No shaders and no u_time: the
# hub opens off a cold main menu, and a dev tool that needs the GPU warmed up
# is a dev tool that fails exactly when you need it.
# =============================================================================

transform dev_hub_panel_in(delay=0.0, yoff=18):
    subpixel True
    alpha 0.0
    yoffset yoff
    pause delay
    easeout_quad 0.28 alpha 1.0 yoffset 0

transform dev_hub_slide_in(delay=0.0, xoff=-20):
    subpixel True
    alpha 0.0
    xoffset xoff
    pause delay
    easeout_quad 0.24 alpha 1.0 xoffset 0

transform dev_hub_scan:
    subpixel True
    ypos -40
    block:
        ypos -40
        linear 6.0 ypos 720
        pause 2.0
        repeat

transform dev_hub_pill_lamp:
    alpha 1.0
    block:
        easeout 0.6 alpha 0.2
        easein 0.6 alpha 1.0
        repeat


# =============================================================================
# THE MOUNT
# The hub's ONLY hook into the rest of the game: one `use dev_hub_mount` in
# screen main_menu, itself guarded by renpy.has_screen so pulling this folder
# does not leave a dangling reference behind. It sits in the top-right corner
# under the build stamp -- clear of the title block, the stage monitor, the
# telemetry stack and the channel rail, so it costs the desk nothing.
# =============================================================================
label dev_hub_rhythm_editor_context:
    if not config.developer or not renpy.has_label("asahina_rhythm_chart_editor"):
        return
    python:
        renpy.context_dynamic("main_menu", "_menu", "_game_menu_screen",
            "quick_menu", "arcade_active")
        main_menu = False
        _menu = False
        _game_menu_screen = None
        quick_menu = False
        arcade_active = False
        renpy.context()._menu = False
        renpy.context()._main_menu = False
    hide screen dev_hub
    scene black
    call asahina_rhythm_chart_editor from _call_dev_hub_rhythm_editor
    return


screen dev_hub_mount():

    if config.developer:

        key "K_F9" action ShowMenu("dev_hub")

        button:
            style "dev_hub_pill"
            xpos 1150
            ypos 50
            xysize (86, 26)
            action ShowMenu("dev_hub")

            # One direct child, deliberately: hover events reach a button's
            # immediate child and stop there. Colour changes ride on styles,
            # which do recurse. (Same rule as the main menu's channel cards.)
            fixed:
                xysize (86, 26)
                add Solid("#ff315b") xysize (5, 5) xpos 10 ypos 11 at dev_hub_pill_lamp
                text "DEV" style "dev_hub_pill_text" xpos 26 ypos 5


# =============================================================================
# THE HUB
# =============================================================================
screen dev_hub():

    tag menu
    modal True

    default dh_page = "routing"

    key "K_ESCAPE" action Return()
    key "game_menu" action Return()

    add "menu_bg"
    add Solid("#02040af6")
    add Solid("#ff315b0e") xysize (1280, 60) at dev_hub_scan

    # Structural accents. Red-led, so this is never mistaken for a player screen.
    add Solid("#ff315b66") xysize (1280, 2) ypos 82
    add Solid("#ff315b33") xysize (3, 528) xpos 300 ypos 96

    # --- header ---------------------------------------------------------------
    hbox:
        xpos 44
        ypos 32
        spacing 9
        add Solid("#ff315b") xysize (7, 7) yalign 0.5 at console_blink
        text "DEVELOPER HUB // 0x4D" style "dh_kicker" yalign 0.5

    text "EVERY DEV-ONLY FEATURE, ONE DOOR":
        style "dh_micro"
        xpos 44
        ypos 54

    text "BUILD v[config.version]  ::  DEVELOPER [config.developer!r]":
        style "dh_micro"
        xanchor 1.0
        xpos 1108
        ypos 40

    textbutton "CLOSE":
        style "dh_button"
        xanchor 1.0
        xpos 1236
        ypos 30
        xysize (120, 38)
        action Return()

    # --- the rail -------------------------------------------------------------
    # Eight 46px pages with 6px gaps end at y 510, above MODULES at 528.
    vbox:
        xpos 44
        ypos 100
        spacing 6

        for dh_i, (dh_key, dh_label, dh_strap) in enumerate(DEV_HUB_PAGES):

            button:
                style "dh_rail_button"
                id ("dh_page_" + dh_key)
                xysize (238, 46)
                action SetScreenVariable("dh_page", dh_key)
                selected (dh_page == dh_key)
                at dev_hub_slide_in(0.03 + 0.03 * dh_i)

                fixed:
                    xysize (238, 46)
                    add Solid("#ff315b" if dh_page == dh_key else "#2a3a47") xysize (4, 46)
                    text dh_label:
                        style ("dh_rail_label_on" if dh_page == dh_key else "dh_rail_label")
                        xpos 18
                        ypos 7
                    text dh_strap:
                        style "dh_rail_strap"
                        xpos 18
                        ypos 30
                        xmaximum 206

    # --- rail footer: what the hub is fronting, live -------------------------
    vbox:
        xpos 44
        ypos 528
        spacing 5
        at dev_hub_slide_in(0.24)

        text "MODULES" style "dh_section"
        add Solid("#ff315b33") xysize (238, 1)

        for dh_mod, dh_name in (
            ("dev_date_jump_available_codes", "Date Router"),
            ("ach_dev_grant", "Achievements"),
            ("mc_dev_give", "Matsucoins"),
            ("inv_toggle_godmode", "Invasions"),
        ):
            $ dh_live = dev_hub_has(dh_mod)
            hbox:
                spacing 8
                add Solid("#37e08a" if dh_live else "#ff315b") xysize (5, 5) yalign 0.5
                text dh_name style "dh_micro" yalign 0.5
                text ("LOADED" if dh_live else "ABSENT"):
                    style "dh_micro"
                    color ("#5f8f76" if dh_live else "#ff6680")
                    yalign 0.5

    # --- content --------------------------------------------------------------
    frame:
        style "dh_pane"
        xpos 320
        ypos 96
        xysize (916, 528)
        at dev_hub_panel_in(0.10)

        viewport:
            style_prefix "dh_sv"
            xysize (864, 476)
            mousewheel True
            scrollbars "vertical"

            vbox:
                xsize 848
                spacing 16

                if dh_page == "routing":
                    use dev_hub_page_routing
                elif dh_page == "unlocks":
                    use dev_hub_page_unlocks
                elif dh_page == "firsts":
                    use dev_hub_page_firsts
                elif dh_page == "economy":
                    use dev_hub_page_economy
                elif dh_page == "combat":
                    use dev_hub_page_combat
                elif dh_page == "sprites":
                    use dev_hub_page_sprites
                elif dh_page == "writing":
                    use dev_hub_page_writing
                else:
                    use dev_hub_page_system

    # --- footer ---------------------------------------------------------------
    add Solid("#ff315b1f") xysize (1192, 2) xpos 44 ypos 648

    text "DEV BUILD ONLY  //  F9 OPENS THIS FROM THE TITLE  //  ESC CLOSES":
        style "dh_micro"
        xpos 44
        ypos 660

    text "NOTHING HERE SHIPS -- addons/Dev Hub/ IS EXCLUDED FROM THE BUILD":
        style "dh_micro"
        xanchor 1.0
        xpos 1236
        ypos 660

    use console_brackets(14, 14, 1252, 692, "#ff315b52", 26, 2)


# =============================================================================
# PAGE FURNITURE
# Three transcluding screens so every page is built out of the same three
# shapes: a titled block, a right-aligned readout row, and a row of buttons.
# The readout uses `fixed` + xalign rather than an hbox with a greedy null --
# a box given an explicit xsize floats its children toward the middle instead
# of packing them left, which is measured and has bitten this project before.
# =============================================================================
screen dh_block(title, note=""):
    vbox:
        xsize 848
        spacing 9

        text title style "dh_title"
        add Solid("#ff315b44") xysize (848, 2)

        if note:
            text note style "dh_body" xmaximum 840

        transclude


screen dh_stat(label, value, col="#e7f3fa"):
    fixed:
        xsize 848
        yfit True

        text label style "dh_stat_label"
        text value:
            style "dh_stat_value"
            color col
            xalign 1.0


screen dh_missing(what):
    frame:
        style "dh_missing_frame"
        text ("[what!t] IS NOT INSTALLED -- nothing on this card is available."):
            style "dh_body"
            color "#ff9db1"


# =============================================================================
# PAGE // ROUTING
# THIS PAGE IS THE DATE ROUTER'S ONLY DOOR. It used to be a second one: New
# Game in a developer build jumped straight to the router, so the hub merely
# reported on a screen you were going to hit anyway. That fork is gone --
# script.rpy sends every build to Chapter Select now, because the route players
# take should be the route development walks. The router is unchanged and is
# still not reimplemented here; it discovers its own routes and hosts the
# out-of-context catalog and the invasion launcher. This page counts what it
# holds and opens it, via `dev_date_jump_start`, which lays down the same fresh
# session state `start` does.
# =============================================================================
screen dev_hub_page_routing():

    python:
        _dh_routes = dev_hub_route_count()
        _dh_ooc = dev_hub_ooc_count()
        _dh_inv = dev_hub_invasion_counts()
        _dh_router = (
            dev_hub_has("dev_date_jump_available_codes")
            and renpy.has_label("dev_date_jump_start"))
        _dh_chapters = dev_hub_chapter_counts()

    use dh_block(
        "STORY ROUTING",
        "Two doors out of the title, and they are not the same door. New Game opens Chapter "
        "Select in every build. The date router is dev-only and starts a clean session at any "
        "day that has a label -- it is reached from here and nowhere else.",
    ):

        use dh_stat("ROUTES ONLINE", ("%d" % _dh_routes) if _dh_routes is not None else "--",
                    "#37e08a" if _dh_routes else "#ff6680")
        use dh_stat("CHAPTERS OPEN",
                    ("%d of %d" % _dh_chapters) if _dh_chapters else "--",
                    "#37e08a" if (_dh_chapters and _dh_chapters[0]) else "#ff6680")
        use dh_stat("OUT OF CONTEXT SCENES", ("%d" % _dh_ooc) if _dh_ooc is not None else "--")
        use dh_stat("ARCHIVIST INVASIONS BUILT",
                    ("%d of %d" % (_dh_inv[0], _dh_inv[2])) if _dh_inv else "--")

        null height 4

        hbox:
            spacing 12
            textbutton "OPEN DATE ROUTER":
                style "dh_button_wide"
                action Start("dev_date_jump_start")
                sensitive _dh_router
            textbutton "OPEN CHAPTER SELECT":
                style "dh_button_wide"
                action Start()
                sensitive renpy.has_label("chapter_select_open")

    use dh_block(
        "WHAT THE ROUTER HOLDS",
        "Everything below is inside it. None of it is duplicated here on purpose.",
    ):
        use dh_stat("MMDD / DISC", "type a date, or DISC for the full opening", "#8fb4c4")
        use dh_stat("ROUTE CHIPS", "every discovered aMMDD label, one click each", "#8fb4c4")
        use dh_stat("SCENE CATALOG", "dated out-of-context scenes, playable early", "#8fb4c4")
        use dh_stat("INVASION LAUNCHER", "the seven, plus start-in-corruptive-state", "#8fb4c4")
        use dh_stat("ALL SIDE CONTENT", "the unlock-everything switch (also on UNLOCKS)", "#8fb4c4")


# =============================================================================
# PAGE // UNLOCKS
# The two switches that decide what the Archive is holding: the everything
# toggle, and the achievement shop's one-at-a-time grant/revoke.
# =============================================================================
screen dev_hub_page_unlocks():

    python:
        _dh_side = dev_hub_side_content_state()
        _dh_side_text, _dh_side_col = dev_hub_flag(_dh_side)
        _dh_side_verb = "DISABLE" if _dh_side == "ENABLED" else "ENABLE"
        _dh_ach = dev_hub_ach_counts()
        _dh_ready = dev_hub_ach_ready()
        _dh_auto = getattr(getattr(renpy.store, "_ach_rt", None), "autounlock", None)

    use dh_block(
        "ALL SIDE CONTENT",
        "One switch over every gated catalog, read live from its owner rather than copied: "
        "Archive modules, side stories, CGs, outfits, soundtrack entries and roster slots. "
        "It toggles both ways, so a locked-state pass is one click away.",
    ):

        use dh_stat("STATE", _dh_side_text, _dh_side_col)

        null height 4

        hbox:
            spacing 12
            textbutton "[_dh_side_verb] ALL SIDE CONTENT":
                style "dh_button_wide"
                action Function(dev_hub_call, "dev_date_jump_toggle_all_side_content")
                sensitive dev_hub_has("dev_date_jump_toggle_all_side_content")

    if not dev_hub_has("ACHIEVEMENTS"):
        use dh_missing("Achievements")
    else:
        use dh_block(
            "ACHIEVEMENTS",
            "AUTO-UNLOCK off is session-only: turn it off, then grant the satisfied ones by "
            "hand to watch each toast land on its own. CLEAR ALL keeps READY history; a "
            "REVOKE inside the shop hard-relocks.",
        ):

            use dh_stat("EARNED", ("%d / %d" % _dh_ach) if _dh_ach else "--")
            use dh_stat("SATISFIED BUT NOT GRANTED",
                        ("%d" % _dh_ready) if _dh_ready is not None else "--",
                        "#8ad9a2" if _dh_ready else "#7f95a3")
            use dh_stat("AUTO-UNLOCK", dev_hub_flag(_dh_auto)[0], dev_hub_flag(_dh_auto)[1])

            null height 4

            hbox:
                spacing 12

                textbutton "OPEN ACHIEVEMENT SHOP":
                    style "dh_button_wide"
                    action Function(dev_hub_show, "ach_dev_shop")

                textbutton ("AUTO-UNLOCK: ON" if _dh_auto else "AUTO-UNLOCK: OFF"):
                    style "dh_button"
                    action Function(dev_hub_call, "ach_dev_toggle_autounlock")
                    sensitive dev_hub_has("ach_dev_toggle_autounlock")

            hbox:
                spacing 12

                textbutton "SYNC NOW":
                    style "dh_button"
                    action Function(dev_hub_call, "ach_refresh")
                    sensitive dev_hub_has("ach_refresh")

                textbutton "CLEAR ALL EARNED":
                    style "dh_button_warn"
                    action Function(dev_hub_call, "ach_dev_clear")
                    sensitive dev_hub_has("ach_dev_clear")


# =============================================================================
# PAGE // FLAGS
# Every moment the game plays exactly once, and the flag that remembers it has
# played. The table is DEV_HUB_FLAGS in the init block; this page only draws
# it. RE-ARM writes the flag's own declared default back, so the moment plays
# again as it would on a new install; MARK SPENT does the reverse, for checking
# what a returning player sees. The second card lists the one-time flags that
# are NOT offered here and why, so their absence reads as a decision.
# =============================================================================
screen dev_hub_page_firsts():

    use dh_block(
        "FIRST-TIME MOMENTS",
        "ARMED plays the next time its trigger is reached; SPENT has already played on this "
        "profile. Every write is flushed to disk at once, so a boot-time moment survives the "
        "relaunch it needs.",
    ):

        for dh_first in DEV_HUB_FLAGS:

            $ dh_first_live = dev_hub_first_owner_live(dh_first)
            $ dh_first_text, dh_first_col = dev_hub_first_state(dh_first)

            frame:
                style "dh_card"

                vbox:
                    spacing 6

                    fixed:
                        xsize 812
                        yfit True

                        text dh_first["label"] style "dh_card_title"
                        text dh_first_text:
                            style "dh_card_key"
                            color dh_first_col
                            xalign 1.0

                    text ("persistent.%s  //  %s" % (dh_first["key"], dh_first["owner"])):
                        style "dh_micro"

                    text dh_first["replays"] style "dh_card_note" xmaximum 812

                    hbox:
                        spacing 10

                        textbutton "RE-ARM":
                            style "dh_button_row"
                            action Function(dev_hub_first_set, dh_first["key"], dh_first["armed"])
                            sensitive dh_first_live

                        textbutton "MARK SPENT":
                            style "dh_button_row"
                            action Function(dev_hub_first_set, dh_first["key"], True)
                            sensitive dh_first_live

        null height 2

        hbox:
            spacing 12
            textbutton "RE-ARM ALL":
                style "dh_button_wide"
                action Function(dev_hub_first_rearm_all)

    use dh_block(
        "ONE-TIME, BUT NOT A MOMENT",
        "These fire once too. A MIGRATION runs on a profile rather than in front of a player; "
        "PROGRESS shares its key with something the player earned. Re-arming either is a side "
        "effect, not a replay -- use the console if that is genuinely what you mean.",
    ):

        for dh_other in DEV_HUB_ONE_TIME_OTHER:

            $ dh_other_live = dev_hub_first_owner_live(dh_other)
            $ dh_other_val = getattr(persistent, dh_other["key"], None)

            frame:
                style "dh_card"

                vbox:
                    spacing 6

                    fixed:
                        xsize 812
                        yfit True

                        text dh_other["label"] style "dh_card_title"
                        text (("%s  //  %s" % (dh_other["kind"], "SET" if dh_other_val else "UNSET")) if dh_other_live else "NOT INSTALLED"):
                            style "dh_card_key"
                            color ("#ffd166" if dh_other_live else "#5d7886")
                            xalign 1.0

                    text ("persistent.%s  //  %s" % (dh_other["key"], dh_other["owner"])):
                        style "dh_micro"

                    text dh_other["why"] style "dh_card_note" xmaximum 812

    use dh_block(
        "ONE-TIME PER SAVE",
        "Not persistent, so not on this page: Hina's World's hinas_world_seen_* flags and "
        "hw_browser_opened_once, and the phone's phone_random_seen. They live inside a save; the "
        "hub runs from the title with none loaded, and a new game re-arms them.",
    ):
        null height 0

# =============================================================================
# PAGE // ECONOMY
# The wallet and the binder. Grants go straight to the balance rather than
# through mc_award, so a dev top-up does not inflate TOTAL EARNED or break the
# lifetime == balance + spent invariant -- that is mc_dev_set's job, and the
# reason these buttons call it rather than doing the arithmetic here.
# =============================================================================
screen dev_hub_page_economy():

    python:
        _dh_wallet = dev_hub_has("mc_balance")
        _dh_bal = mc_balance() if _dh_wallet else None
        _dh_cards = dev_hub_card_counts()

    if not _dh_wallet:
        use dh_missing("Matsucoin Currency and Gacha")
    else:
        use dh_block(
            "WALLET",
            "A grant is not earnings. These write the balance directly, which is why TOTAL "
            "EARNED does not move when you use them.",
        ):

            use dh_stat("BALANCE", "%s / %s" % (mc_num(_dh_bal), mc_num(MC_BALANCE_CAP)), "#ffb454")
            use dh_stat("LIFETIME EARNED", mc_num(getattr(persistent, "mc_lifetime", 0) or 0))
            use dh_stat("SPENT", mc_num(getattr(persistent, "mc_spent", 0) or 0))

            null height 4

            hbox:
                spacing 10
                for _dh_lbl, _dh_amt in (("+100", 100), ("+1K", 1000), ("+10K", 10000)):
                    textbutton _dh_lbl:
                        style "dh_button_sm"
                        action Function(dev_hub_call, "mc_dev_give", _dh_amt)
                textbutton "MAX":
                    style "dh_button_sm"
                    action Function(dev_hub_call, "mc_dev_fill")
                textbutton "ZERO":
                    style "dh_button_sm"
                    action Function(dev_hub_call, "mc_dev_reset")

        use dh_block(
            "BINDER",
            "RESET LEDGER wipes the one-time payout record, so every derived payout becomes "
            "claimable again and the next sync re-pays the lot. That is for testing the "
            "EARNING path; ZERO above is for testing the machine.",
        ):

            use dh_stat("CARDS COLLECTED", ("%d / %d" % _dh_cards) if _dh_cards else "--")
            use dh_stat("PULLS", mc_num(getattr(persistent, "mc_pulls_total", 0) or 0))
            use dh_stat("PITY", "%d" % (getattr(persistent, "mc_pity", 0) or 0))

            null height 4

            hbox:
                spacing 12

                textbutton "OPEN COIN BENCH":
                    style "dh_button_wide"
                    action Function(dev_hub_show, "mc_dev_shop")

                textbutton "GRANT ALL CARDS":
                    style "dh_button"
                    action Function(dev_hub_call, "mc_dev_grant_all")
                    sensitive dev_hub_has("mc_dev_grant_all")

            hbox:
                spacing 12

                textbutton "CLEAR CARDS":
                    style "dh_button_warn"
                    action Function(dev_hub_call, "mc_dev_clear_cards")
                    sensitive dev_hub_has("mc_dev_clear_cards")

                textbutton "RESET PAYOUT LEDGER":
                    style "dh_button_warn"
                    action Function(dev_hub_call, "mc_dev_reset", keep_ledger=False)
                    sensitive dev_hub_has("mc_dev_reset")


# =============================================================================
# PAGE // COMBAT
# Two halves. The top is live -- switches that can be thrown from a menu. The
# bottom is a REGISTER of the dev affordances that only exist inside a running
# fight, because a key you press mid-danmaku cannot be a button here. They were
# scattered across five files and undiscoverable; listing them is the whole
# point of having one hub.
# =============================================================================
screen dev_hub_page_combat():

    python:
        _dh_inv = dev_hub_invasion_counts()
        _dh_god = inv_godmode_on() if dev_hub_has("inv_godmode_on") else None

        # (where, key or route, what it does)
        _dh_infight = (
            ("Every boss fight", "F3",
             "Live frame profiler -- frame time, worst frame, per-section cost."),
            ("Archivist Invasions", "G",
             "Godmode. Hits still land, sound, shake and print their damage; only the "
             "subtraction is skipped, so a pattern can be sat in and read."),
            ("Kotonoha (Touhou stage)", "Menu: Debug reading",
             "Every shot one-shots a bar."),
            ("Kotonoha (Touhou stage)", "Menu: Debug wave viewer",
             "Read any single wave, your pick, from a grid."),
            ("Tsubaki (soul fight)", "Menu: Open the door (DEV)",
             "Fast routes -- skips to the branch ends."),
            ("Asarhythm", "Setup: Chart Editor (DEV)",
             "Chart notes and sustains against the song, then playtest from the editor."),
            ("Matsuda (main fight)", "Party: Seeker",
             "Scan is swapped for a move that always deals 50% of Matsuda's max HP."),
        )

    if not _dh_inv:
        use dh_missing("Archivist Invasions")
    else:
        use dh_block(
            "ARCHIVIST INVASIONS",
            "Nothing in the story rolls for these yet -- the date router's launcher is the "
            "only way in. Godmode survives into the fight and is also togglable there with G.",
        ):

            use dh_stat("BUILT", "%d of %d" % (_dh_inv[0], _dh_inv[2]))
            use dh_stat("FENDED OFF", "%d of %d" % (_dh_inv[1], _dh_inv[2]),
                        "#37e08a" if _dh_inv[1] else "#7f95a3")
            use dh_stat("GODMODE", dev_hub_flag(_dh_god)[0], dev_hub_flag(_dh_god)[1])

            null height 4

            hbox:
                spacing 12

                textbutton ("GODMODE: ON" if _dh_god else "GODMODE: OFF"):
                    style "dh_button_wide"
                    action Function(dev_hub_call, "inv_toggle_godmode")
                    sensitive dev_hub_has("inv_toggle_godmode")

                textbutton "CLEAR INVASION RECORD":
                    style "dh_button_warn"
                    action Function(dev_hub_call, "inv_clear_record")
                    sensitive dev_hub_has("inv_clear_record")

    if config.developer:
        use dh_block(
            "ASARHYTHM",
            "Build and edit song charts, preview the music, and playtest the note timing.",
        ):
            textbutton "OPEN CHART EDITOR":
                id "dh_rhythm_editor"
                style "dh_button_wide"
                action Function(dev_hub_open_rhythm_editor)
                sensitive renpy.has_label("asahina_rhythm_chart_editor")

    use dh_block(
        "IN-FIGHT AFFORDANCES",
        "These live inside a running fight and cannot be thrown from here. This is the "
        "register of them, so none of it has to be remembered or grepped for again.",
    ):

        for _dh_where, _dh_key, _dh_what in _dh_infight:

            frame:
                style "dh_card"

                vbox:
                    xsize 812
                    spacing 4

                    fixed:
                        xsize 812
                        yfit True

                        text _dh_where style "dh_card_title"
                        text _dh_key:
                            style "dh_card_key"
                            xalign 1.0

                    text _dh_what style "dh_card_note" xmaximum 812


# =============================================================================
# PAGE // SPRITES
# =============================================================================
screen dev_hub_page_writing():
    use dh_block("STORY WRITER", "Write prose with the scene beside it. Arrange backgrounds, sprites and ATL; place music cues; then read the unsaved scene in the game."):
        if config.developer and dev_hub_has("story_writer_open"):
            textbutton "OPEN STORY WRITER":
                style "dh_button_wide"
                action Function(dev_hub_call, "story_writer_open")
        else:
            use dh_missing("Story Writer")
    use dh_block("YOUR STORY FILES", "Open existing chapters or create a scene. Custom Python and poem logic remain preserved source. Draft recovery and source backups live outside the game's loaded scripts."):
        use dh_stat("WRITE", "Textboxes, speakers, expressions and Nier prose", "#8fb4c4")
        use dh_stat("STAGE", "Images, slots, transitions and animation preview", "#8fb4c4")
        use dh_stat("MUSIC", "Track audition, play / queue / stop, fades and looping", "#8fb4c4")
        use dh_stat("SAVE", "Ordinary .rpy source, validated before replacement", "#8fb4c4")


screen dev_hub_page_sprites():

    python:
        _dh_cast = len(dev_sprite_tags(False))
        _dh_all = len(dev_sprite_tags(True))

    use dh_block(
        "SPRITE VIEWER",
        "Every character sprite in the game, composed live. Pick a face and an outfit and "
        "watch them go together; step the full-body poses that live outside the rig; and see "
        "which attribute combinations draw nothing, which is the one sprite failure that does "
        "not raise an error anywhere.",
    ):

        use dh_stat("CAST TAGS", "%d" % _dh_cast)
        use dh_stat("IMAGE TAGS IN THE GAME", "%d" % _dh_all, "#8fb4c4")

        null height 4

        hbox:
            spacing 12

            textbutton "OPEN SPRITE VIEWER":
                style "dh_button_wide"
                action Show("dev_sprite_viewer")

            textbutton "RESCAN IMAGES":
                style "dh_button"
                action Function(dev_sprite_refresh)

    use dh_block(
        "WHAT IT READS",
        "Nothing is hand-maintained. It walks Ren'Py's image registry and, for a "
        "layeredimage, that rig's own group table -- so a face added to def_characters.rpy "
        "appears the moment it exists.",
    ):
        use dh_stat("POSE", "a tag can own several rigs; each has its own groups", "#8fb4c4")
        use dh_stat("RIG", "layeredimage -- one attribute per group, composed live", "#8fb4c4")
        use dh_stat("VARIANT", "a discrete `image tag a b` -- the full-body poses", "#8fb4c4")
        use dh_stat("ALL TAGS", "in the viewer's header: every image tag, not just cast", "#8fb4c4")
        use dh_stat("LAYER FILES", "the path on disk for each plate actually drawn", "#8fb4c4")


# =============================================================================
# PAGE // SYSTEM
# Build state, and Ren'Py's OWN developer tools, which are otherwise only
# reachable through Shift+D. They are wired individually rather than by opening
# the stock _developer menu, so the hub really is the one door.
# =============================================================================
screen dev_hub_page_system():

    python:
        try:
            _dh_renderer = renpy.get_renderer_info().get("renderer", "?")
        except Exception:
            _dh_renderer = "?"

        _dh_fps = enter_m_fps_measured() if dev_hub_has("enter_m_fps_measured") else None

    if dev_hub_has("enter_m_fps_sample"):
        timer 1.0 repeat True action Function(enter_m_fps_sample)

    use dh_block("BUILD"):
        use dh_stat("VERSION", "v[config.version]")
        use dh_stat("RENDERER", _dh_renderer, "#8fb4c4")
        use dh_stat("config.developer", "%r" % (config.developer,), "#37e08a")
        use dh_stat("config.autoreload", "%r" % (renpy.get_autoreload(),),
                    "#37e08a" if renpy.get_autoreload() else "#7f95a3")
        use dh_stat("MEASURED FRAME RATE",
                    ("%s fps" % _dh_fps) if _dh_fps is not None else "--", "#8fb4c4")

    # The throttle itself lives in spec_emulator.rpy; this is only its door.
    if dev_hub_has("DEV_SPEC", "DEV_SPEC_PRESETS"):
        use dh_block(
            "SPEC EMULATOR",
            "Plays the game as a slower machine would. Each frame's real CPU and GPU time is "
            "measured, and the frame is held until it has cost what it would there, presented "
            "on a 60Hz panel. Pick a machine, then go play the mode you are worried about -- the "
            "readout sits bottom-left. The factors are estimates from published benchmarks; "
            "spec_emulator.rpy lists what this does not model.",
        ):
            $ _dh_spec_state = (DEV_SPEC.label if DEV_SPEC.active else
                                ("ARMING" if DEV_SPEC.pending is not None else "OFF"))
            use dh_stat("EMULATING", _dh_spec_state,
                        "#37e08a" if DEV_SPEC.active else "#7f95a3")
            use dh_stat("GPU TIMER", DEV_SPEC.gl_note or "starts with the first emulated frame",
                        "#8fb4c4")

            null height 2

            hbox:
                spacing 10
                textbutton "OFF":
                    style "dh_button_row"
                    action Function(dev_spec_select, None)
                    selected (not DEV_SPEC.active and DEV_SPEC.pending is None)
                for _dh_sp in DEV_SPEC_PRESETS[:3]:
                    textbutton _dh_sp[1]:
                        style "dh_button_row"
                        action Function(dev_spec_select, _dh_sp[0])
                        selected (DEV_SPEC.key == _dh_sp[0])
            hbox:
                spacing 10
                for _dh_sp in DEV_SPEC_PRESETS[3:]:
                    textbutton _dh_sp[1]:
                        style "dh_button_row"
                        action Function(dev_spec_select, _dh_sp[0])
                        selected (DEV_SPEC.key == _dh_sp[0])

            hbox:
                spacing 12
                textbutton ("PIN GPU CLOCKS: ON" if DEV_SPEC.pin else "PIN GPU CLOCKS: OFF"):
                    style "dh_button_wide"
                    action ToggleField(DEV_SPEC, "pin")
                textbutton ("READOUT: ON" if DEV_SPEC.overlay else "READOUT: OFF"):
                    style "dh_button_wide"
                    action Function(dev_spec_toggle_overlay)

            text ("PIN GPU CLOCKS keeps this graphics card at full clocks while measuring. At this "
                    "game's load it otherwise idles at a fraction of them, which inflates every GPU "
                    "reading (by up to 11x, measured) and so throttles GPU-heavy modes far harder "
                    "than the named machine would. It costs power and fan noise while it is on."):
                style "dh_body"
                xmaximum 840

            for _dh_sp in DEV_SPEC_PRESETS:
                use dh_stat(_dh_sp[1],
                            "CPU x%.1f  GPU x%.0f  %s" % (_dh_sp[2], _dh_sp[3], _dh_sp[6]),
                            "#8fb4c4")

    use dh_block(
        "REN'PY DEVELOPER TOOLS",
        "The stock Shift+D menu, unpacked so it is in the same place as everything else.",
    ):

        hbox:
            spacing 12
            # _console.enter alone, and NOT after a Return(): Return ends the
            # interaction immediately, so anything after it in the list never
            # runs. The console opens over the hub, same as Shift+O does.
            textbutton "PYTHON CONSOLE (Shift+O)":
                style "dh_button_wide"
                action (_console.enter if dev_hub_has("_console") else NullAction())
                sensitive dev_hub_has("_console")
            textbutton "RELOAD GAME (Shift+R)":
                style "dh_button_wide"
                action renpy.reload_script

        hbox:
            spacing 12
            textbutton "VARIABLE VIEWER":
                style "dh_button_wide"
                action ui.callsinnewcontext("_variable_viewer")
            textbutton "PERSISTENT VIEWER":
                style "dh_button_wide"
                action ui.callsinnewcontext("_persistent_viewer")

        hbox:
            spacing 12
            textbutton "IMAGE LOCATION PICKER":
                style "dh_button_wide"
                action ui.callsinnewcontext("_image_location_picker")
            textbutton "FILENAME LIST":
                style "dh_button_wide"
                action ui.callsinnewcontext("_filename_list")

        hbox:
            spacing 12
            textbutton "IMAGE ATTRIBUTES":
                style "dh_button_wide"
                action ui.callsinnewcontext("_image_attributes")
            if renpy.get_screen("_image_load_log"):
                textbutton "HIDE IMAGE LOAD LOG (F4)":
                    style "dh_button_wide"
                    action Hide("_image_load_log")
            else:
                textbutton "SHOW IMAGE LOAD LOG (F4)":
                    style "dh_button_wide"
                    action Show("_image_load_log")

    use dh_block(
        "KEYS THAT ONLY EXIST IN A DEV BUILD",
        "Live everywhere, no menu needed.",
    ):
        use dh_stat("F9", "open this hub from the title screen", "#8fb4c4")
        use dh_stat("Shift+O", "Python console", "#8fb4c4")
        use dh_stat("Shift+D", "Ren'Py developer menu", "#8fb4c4")
        use dh_stat("Shift+R", "reload the script in place", "#8fb4c4")
        use dh_stat("Shift+E", "open the current line in the editor", "#8fb4c4")
        use dh_stat("F3", "frame profiler, inside any boss fight", "#8fb4c4")
        use dh_stat("F4", "image load log", "#8fb4c4")


# =============================================================================
# SPRITE VIEWER -- SCREEN
# =============================================================================
# LAYOUT
#   Three columns: the cast rail, the stage, and the look panel. The stage is
#   deliberately NOT clipped -- a sprite zoomed to 3x to read an eyeline is
#   supposed to spill. It spills UNDER the side panels, which are opaque and
#   drawn afterwards, so the overflow is masked by z-order rather than by a
#   viewport. (A viewport would have worked for the clipping and then eaten the
#   negative offsets that panning needs; that trap is documented in the project's
#   row-alignment notes.)
#
# GEOMETRY
#   header  y   0..78      stage  x 244..868, y 78..624
#   rail    x   0..244     look   x 868..1280
#   footer  y 624..720
# =============================================================================
screen dev_sprite_viewer():

    modal True
    zorder 300

    python:
        dev_sprite_ensure()

        _dsv_tags = dev_sprite_tags(_dev_sprite.show_all)
        _dsv_count = len(_dsv_tags)
        _dsv_tag = _dev_sprite.tag
        _dsv_look = dev_sprite_look(_dsv_tag) if _dsv_tag else None
        _dsv_rig = dev_sprite_current_rig()
        _dsv_rigs = _dsv_look["rigs"] if _dsv_look else []
        _dsv_bad = dev_sprite_unsatisfied()
        _dsv_line = dev_sprite_show_line()
        _dsv_backdrop = DEV_SPRITE_BACKDROPS[_dev_sprite.backdrop][1]
        _dsv_d = dev_sprite_displayable(560, 500)
        _dsv_files = dev_sprite_layer_files()

    key "K_ESCAPE" action Hide("dev_sprite_viewer")
    key "game_menu" action Hide("dev_sprite_viewer")
    key "K_LEFT" action Function(dev_sprite_cycle_group, -1)
    key "K_RIGHT" action Function(dev_sprite_cycle_group, 1)
    key "K_UP" action Function(dev_sprite_cycle_row, -1)
    key "K_DOWN" action Function(dev_sprite_cycle_row, 1)
    key "K_PAGEUP" action Function(dev_sprite_cycle_tag, -1)
    key "K_PAGEDOWN" action Function(dev_sprite_cycle_tag, 1)
    key "K_TAB" action Function(dev_sprite_cycle_rig, 1)
    key "K_v" action Function(dev_sprite_cycle_variant, 1)
    key "K_EQUALS" action Function(dev_sprite_zoom_step, 1)
    key "K_MINUS" action Function(dev_sprite_zoom_step, -1)
    key "K_0" action Function(dev_sprite_reset_view)
    key "K_w" action Function(dev_sprite_pan, 0, -24)
    key "K_s" action Function(dev_sprite_pan, 0, 24)
    key "K_a" action Function(dev_sprite_pan, -24, 0)
    key "K_d" action Function(dev_sprite_pan, 24, 0)

    # --- the stage, bottom of the stack --------------------------------------
    add Solid(_dsv_backdrop)

    if _dsv_d is not None:
        fixed:
            xpos 244
            ypos 78
            xysize (624, 546)
            add _dsv_d xalign 0.5 yalign 0.5

    # --- the opaque furniture that masks the overflow ------------------------
    add Solid("#05080e") xpos 0 ypos 0 xysize (244, 720)
    add Solid("#05080e") xpos 868 ypos 0 xysize (412, 720)
    add Solid("#05080e") xpos 0 ypos 0 xysize (1280, 78)
    add Solid("#05080e") xpos 0 ypos 624 xysize (1280, 96)

    add Solid("#ff315b55") xpos 0 ypos 76 xysize (1280, 2)
    add Solid("#ff315b33") xpos 242 ypos 78 xysize (2, 546)
    add Solid("#ff315b33") xpos 868 ypos 78 xysize (2, 546)
    add Solid("#ff315b55") xpos 0 ypos 624 xysize (1280, 2)

    # --- header ---------------------------------------------------------------
    hbox:
        xpos 24
        ypos 18
        spacing 9
        add Solid("#ff315b") xysize (7, 7) yalign 0.5 at console_blink
        text "SPRITE VIEWER // 0x4D" style "dh_kicker" yalign 0.5

    text (_dsv_tag or "NO SPRITES FOUND"):
        style "dsv_tag_name"
        xpos 24
        ypos 38

    text ("ZOOM %.2fx   //   PAN %d, %d" % (_dev_sprite.zoom, _dev_sprite.panx, _dev_sprite.pany)):
        style "dh_micro"
        xanchor 1.0
        xpos 1130
        ypos 30

    textbutton "CLOSE":
        style "dh_button"
        xanchor 1.0
        xpos 1256
        ypos 20
        xysize (110, 36)
        action Hide("dev_sprite_viewer")

    # --- cast rail ------------------------------------------------------------
    text "CAST // [_dsv_count]":
        style "dh_section"
        xpos 20
        ypos 92

    textbutton ("ALL TAGS: ON" if _dev_sprite.show_all else "ALL TAGS: OFF"):
        style "dsv_toggle"
        xpos 20
        ypos 112
        xysize (204, 26)
        action Function(dev_sprite_toggle_show_all)

    viewport:
        style_prefix "dh_sv"
        xpos 20
        ypos 148
        xysize (204, 462)
        mousewheel True
        scrollbars "vertical"

        vbox:
            spacing 3

            for _dsv_t in _dsv_tags:
                textbutton _dsv_t:
                    style ("dsv_cast_on" if _dsv_t == _dsv_tag else "dsv_cast")
                    xysize (186, 28)
                    action Function(dev_sprite_select_tag, _dsv_t)

    # --- look panel -----------------------------------------------------------
    text "LOOK":
        style "dh_section"
        xpos 888
        ypos 92

    viewport:
        style_prefix "dh_sv"
        xpos 888
        ypos 112
        xysize (368, 498)
        mousewheel True
        scrollbars "vertical"

        vbox:
            spacing 12

            if _dsv_look is None:
                text "Nothing to show." style "dh_body"

            else:

                # --- POSE: which rig, when the tag owns more than one ---
                if len(_dsv_rigs) > 1:
                    vbox:
                        spacing 5
                        text "  POSE" style "dsv_group"

                        $ _dsv_pose_names = [(" ".join(_p) or "(base)") for _p, _r in _dsv_rigs]

                        for _dsv_row in dev_sprite_wrap(_dsv_pose_names, 344):
                            hbox:
                                spacing 6
                                for _dsv_pl in _dsv_row:
                                    $ _dsv_pi = _dsv_pose_names.index(_dsv_pl)
                                    textbutton _dsv_pl:
                                        style ("dsv_chip_on" if (_dev_sprite.variant is None and _dev_sprite.rig == _dsv_pi) else "dsv_chip")
                                        xysize (dev_sprite_chip_width(_dsv_pl), 26)
                                        action Function(dev_sprite_select_rig, _dsv_pi)

                # --- the selected rig's groups ---
                if _dsv_rig is not None:

                    for _dsv_i, (_dsv_g, _dsv_names) in enumerate(_dsv_rig["groups"]):

                        vbox:
                            spacing 5

                            # The active row is what the arrow keys drive, so it
                            # has to be visible without hunting for it.
                            $ _dsv_active = (_dsv_i == _dev_sprite.row)
                            text ((DEV_SPRITE_MARK + " " if _dsv_active else "  ") + _dsv_g.upper()):
                                style ("dsv_group_on" if _dsv_active else "dsv_group")

                            # A group with no declared default may legitimately
                            # show nothing, so NONE is offered as a real state
                            # rather than left unreachable.
                            $ _dsv_optional = (_dsv_g not in _dsv_rig["defaults"])
                            $ _dsv_labels = (["NONE"] if _dsv_optional else []) + list(_dsv_names)

                            for _dsv_row in dev_sprite_wrap(_dsv_labels, 344):
                                hbox:
                                    spacing 6
                                    for _dsv_a in _dsv_row:
                                        if _dsv_a == "NONE":
                                            textbutton "NONE":
                                                style ("dsv_chip_on" if _dev_sprite.groups.get(_dsv_g) is None else "dsv_chip")
                                                xysize (dev_sprite_chip_width("NONE"), 26)
                                                action Function(dev_sprite_clear, _dsv_g)
                                        else:
                                            $ _dsv_on = (_dev_sprite.variant is None and _dev_sprite.groups.get(_dsv_g) == _dsv_a)
                                            textbutton _dsv_a:
                                                style ("dsv_chip_bad" if (_dsv_on and _dsv_a in _dsv_bad) else ("dsv_chip_on" if _dsv_on else "dsv_chip"))
                                                xysize (dev_sprite_chip_width(_dsv_a), 26)
                                                action Function(dev_sprite_set, _dsv_g, _dsv_a)

                    # --- ungrouped attributes, which are independent toggles ---
                    if _dsv_rig["free"]:
                        vbox:
                            spacing 5
                            text "  EXTRAS" style "dsv_group"

                            for _dsv_row in dev_sprite_wrap(_dsv_rig["free"], 344):
                                hbox:
                                    spacing 6
                                    for _dsv_a in _dsv_row:
                                        textbutton _dsv_a:
                                            style ("dsv_chip_on" if _dsv_a in _dev_sprite.free else "dsv_chip")
                                            xysize (dev_sprite_chip_width(_dsv_a), 26)
                                            action Function(dev_sprite_toggle_free, _dsv_a)

                # --- discrete images that sit outside the rig ---
                if _dsv_look["variants"]:
                    vbox:
                        spacing 5

                        fixed:
                            xsize 344
                            yfit True
                            text "  POSES / VARIANTS" style "dsv_group"
                            if _dev_sprite.variant is not None and _dsv_rigs:
                                textbutton "BACK TO RIG":
                                    style "dsv_chip_on"
                                    xysize (108, 22)
                                    xalign 1.0
                                    action Function(dev_sprite_select_rig, _dev_sprite.rig)

                        $ _dsv_vlabels = [(" ".join(v) or "(base)") for v in _dsv_look["variants"]]

                        for _dsv_row in dev_sprite_wrap(_dsv_vlabels, 344):
                            hbox:
                                spacing 6
                                for _dsv_label in _dsv_row:
                                    $ _dsv_v = _dsv_look["variants"][_dsv_vlabels.index(_dsv_label)]
                                    textbutton _dsv_label:
                                        style ("dsv_chip_on" if _dev_sprite.variant == _dsv_v else "dsv_chip")
                                        xysize (dev_sprite_chip_width(_dsv_label), 26)
                                        action Function(dev_sprite_set_variant, _dsv_v)

                # --- where the plates actually live ---
                if _dsv_files:
                    vbox:
                        spacing 4
                        text "  LAYER FILES" style "dsv_group"

                        for _dsv_grp, _dsv_attr, _dsv_path in _dsv_files:
                            vbox:
                                spacing 1
                                text ("%s / %s" % (_dsv_grp, _dsv_attr)):
                                    style "dsv_file_head"
                                text _dsv_path:
                                    style "dsv_file_path"
                                    xmaximum 344

    # --- footer: the line you paste, and the view controls -------------------
    text "SHOW LINE":
        style "dh_micro"
        xpos 24
        ypos 634

    text (_dsv_line or "--"):
        style "dsv_show_line"
        xpos 108
        ypos 630
        xmaximum 800

    # The one sprite failure that raises nothing: an attribute whose own
    # if_all / if_any / if_not rules exclude it from this combination draws
    # NOTHING, and a body with no face on it looks like an art bug rather than
    # a wiring one. Say so out loud.
    if _dsv_bad:
        text ("DRAWS NOTHING HERE: " + ", ".join(_dsv_bad)):
            style "dsv_warn"
            xanchor 1.0
            xpos 1256
            ypos 632
            xmaximum 340

    hbox:
        xpos 24
        ypos 664
        spacing 6

        text "ZOOM" style "dh_micro" yalign 0.5
        textbutton "-":
            style "dsv_chip"
            xysize (34, 26)
            action Function(dev_sprite_zoom_step, -1)
        for _dsv_z in DEV_SPRITE_ZOOMS:
            textbutton ("%gx" % _dsv_z):
                style ("dsv_chip_on" if _dev_sprite.zoom == _dsv_z else "dsv_chip")
                xysize (48, 26)
                action SetField(_dev_sprite, "zoom", _dsv_z)
        textbutton "+":
            style "dsv_chip"
            xysize (34, 26)
            action Function(dev_sprite_zoom_step, 1)

        null width 14

        text "STAGE" style "dh_micro" yalign 0.5
        for _dsv_bi, (_dsv_bl, _dsv_bc) in enumerate(DEV_SPRITE_BACKDROPS):
            textbutton _dsv_bl:
                style ("dsv_chip_on" if _dev_sprite.backdrop == _dsv_bi else "dsv_chip")
                xysize (dev_sprite_chip_width(_dsv_bl), 26)
                action Function(dev_sprite_set_backdrop, _dsv_bi)

        null width 14

        textbutton "RESET VIEW":
            style "dsv_chip"
            xysize (108, 26)
            action Function(dev_sprite_reset_view)

    text "PGUP/PGDN CHARACTER  //  UP/DOWN GROUP  //  LEFT/RIGHT ATTRIBUTE  //  TAB POSE  //  V VARIANT  //  WASD PAN  //  -/= ZOOM  //  0 RESET  //  ESC CLOSE":
        style "dh_micro"
        xpos 24
        ypos 698

    use console_brackets(8, 8, 1264, 704, "#ff315b3a", 22, 2)


# =============================================================================
# STYLES
# The terminal family the rest of the game uses, shifted red. Every plate is a
# Solid: this has to draw correctly on the first frame after a cold boot.
# =============================================================================

style dh_kicker is gui_text:
    font gui.interface_font
    size 15
    color "#ff315b"
    bold True
    kerning 3

style dh_micro is gui_text:
    font gui.interface_font
    size 12
    color "#7f95a3"
    outlines [(1, "#02040a", 0, 1)]

style dh_section is gui_text:
    font gui.interface_font
    size 13
    color "#ff6680"
    bold True
    kerning 2

style dh_title is gui_text:
    font gui.interface_font
    size 26
    color "#e7f3fa"
    outlines [(2, "#02040a", 0, 1)]

style dh_body is gui_text:
    font gui.interface_font
    size 16
    color "#9fb3c0"
    line_spacing 4

style dh_stat_label is gui_text:
    font gui.interface_font
    size 15
    color "#7f95a3"

style dh_stat_value is gui_text:
    font gui.interface_font
    size 15
    color "#e7f3fa"
    bold True

style dh_pane is empty:
    background Solid("#070d16f2")
    foreground Solid("#ff315b1c")
    padding (26, 26)

style dh_missing_frame is empty:
    background Solid("#1b0c12f0")
    xsize 848
    padding (22, 18)

# --- the corner mount -------------------------------------------------------

style dev_hub_pill is button:
    background Solid("#1b0812e8")
    hover_background Solid("#3a0f1f")
    xmaximum None
    ymaximum None
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style dev_hub_pill_text is gui_text:
    font gui.interface_font
    size 13
    color "#ff8fa5"
    hover_color "#ffffff"
    bold True
    kerning 2

# --- buttons ----------------------------------------------------------------

# `is button` inherits gui.button_properties("button"), which pins BOTH
# yminimum and ymaximum to gui.button_height. Anything here that has to be
# taller or shorter than that clears the inherited maxima; anything that sets
# its own xysize in the screen still needs the maxima cleared or
# config.enforce_window_max_size clamps it back.

style dh_button is button:
    background Solid("#131f2b")
    hover_background Solid("#22394a")
    insensitive_background Solid("#0b131a")
    selected_background Solid("#3a0f1f")
    xmaximum None
    ymaximum None
    xsize 214
    ysize 40
    padding (12, 8)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style dh_button_text is button_text:
    font gui.interface_font
    size 15
    color "#d6e6ee"
    hover_color "#ff6680"
    insensitive_color "#4c5b64"
    xalign 0.5

style dh_button_wide is dh_button:
    xsize 300

style dh_button_wide_text is dh_button_text:
    size 14

style dh_button_sm is dh_button:
    xsize 92
    ysize 34

style dh_button_sm_text is dh_button_text:
    size 14

style dh_button_warn is dh_button:
    background Solid("#2a0e18")
    hover_background Solid("#48182b")

style dh_button_warn_text is dh_button_text:
    color "#ff9db1"
    hover_color "#ffffff"

style dh_button_row is dh_button:
    xsize 150
    ysize 34
    padding (10, 6)

style dh_button_row_text is dh_button_text:
    size 13

# --- the rail ---------------------------------------------------------------

style dh_rail_button is button:
    background Solid("#0a121b")
    hover_background Solid("#16242f")
    selected_background Solid("#1d0d15")
    selected_hover_background Solid("#2a1119")
    xmaximum None
    ymaximum None
    padding (0, 0)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style dh_rail_label is gui_text:
    font gui.interface_font
    size 18
    color "#8fa6b3"
    bold True
    kerning 1

style dh_rail_label_on is dh_rail_label:
    color "#ffffff"

style dh_rail_strap is gui_text:
    font gui.interface_font
    size 12
    color "#5d7280"

# --- the in-fight register cards --------------------------------------------

style dh_card is empty:
    background Solid("#0a121bcc")
    xsize 848
    padding (18, 14)

style dh_card_title is gui_text:
    font gui.interface_font
    size 17
    color "#e7f3fa"
    bold True

style dh_card_key is gui_text:
    font gui.interface_font
    size 14
    color "#ffd166"
    bold True
    kerning 1

style dh_card_note is gui_text:
    font gui.interface_font
    size 14
    color "#8fa6b3"
    line_spacing 3

# --- shared scrollbars ------------------------------------------------------
# Both viewports carry style_prefix "dh_sv"; anything not named here is
# auto-created from the matching base style (dh_sv_viewport -> viewport).

style dh_sv_vscrollbar is vscrollbar:
    xsize 10
    base_bar Solid("#0a1119")
    thumb Solid("#5a2233")
    hover_thumb Solid("#ff315b")

style dh_sv_side is side:
    spacing 6

# --- sprite viewer ----------------------------------------------------------

style dsv_tag_name is gui_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 30
    color "#f2fbff"
    outlines [(2, "#02040a", 0, 1), (1, "#ff315b88", 0, 0)]

style dsv_toggle is dh_button:
    xsize 204
    ysize 26
    padding (8, 4)

style dsv_toggle_text is dh_button_text:
    size 12

style dsv_cast is button:
    background Solid("#0a121b")
    hover_background Solid("#16242f")
    xmaximum None
    ymaximum None
    padding (10, 4)
    hover_sound gui.hover_sound

style dsv_cast_text is button_text:
    font gui.interface_font
    size 14
    color "#9fb3c0"
    hover_color "#ffffff"

style dsv_cast_on is dsv_cast:
    background Solid("#3a0f1f")
    hover_background Solid("#4d1428")

style dsv_cast_on_text is dsv_cast_text:
    color "#ffffff"
    bold True

style dsv_group is gui_text:
    font gui.interface_font
    size 13
    color "#6f8592"
    bold True
    kerning 2

style dsv_group_on is dsv_group:
    color "#ff6680"

style dsv_chip is button:
    background Solid("#0d1822")
    hover_background Solid("#1d3040")
    xmaximum None
    ymaximum None
    padding (4, 3)
    hover_sound gui.hover_sound

style dsv_chip_text is button_text:
    font gui.interface_font
    size 13
    color "#9fd8ec"
    hover_color "#ffffff"
    xalign 0.5

style dsv_chip_on is dsv_chip:
    background Solid("#3a0f1f")
    hover_background Solid("#4d1428")

style dsv_chip_on_text is dsv_chip_text:
    color "#ffffff"
    bold True

# Selected, but its own layer rules exclude it from this combination -- so it
# is drawing nothing at all.
style dsv_chip_bad is dsv_chip:
    background Solid("#4a3208")
    hover_background Solid("#5e4009")

style dsv_chip_bad_text is dsv_chip_text:
    color "#ffd166"
    bold True

style dsv_show_line is gui_text:
    font gui.interface_font
    size 17
    color "#8ad9a2"
    bold True

style dsv_warn is gui_text:
    font gui.interface_font
    size 13
    color "#ffd166"
    bold True

style dsv_file_head is gui_text:
    font gui.interface_font
    size 12
    color "#6f8592"
    bold True

style dsv_file_path is gui_text:
    font gui.interface_font
    size 12
    color "#8fb4c4"
