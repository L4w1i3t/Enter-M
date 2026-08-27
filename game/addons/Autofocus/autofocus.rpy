# =============================================================================
# autofocus.rpy  --  AUTOMATIC SPEAKER FOCUS for character sprites
# =============================================================================
#
# WHAT IT DOES
#   Whenever a character speaks, the speaking sprite pops to a "focus" pose while
#   every other on-screen character is gently pushed into the background -- a
#   spotlight effect that makes conversations readable without the writer
#   hand-managing it per line. Fully automatic: it hooks Matsu'Py's character +
#   scene callbacks (bottom of file).
#
# TWO LAYERS PER MANAGED SPRITE
#   A managed sprite is shown with a 2-entry at_list: [grade, pose] (grade inner,
#   pose outermost -- see _autofocus_apply for why the order is load-bearing).
#     - pose  : the slot transform (t = rest, f = focus, ...) that handles the
#               speaker's forward "pop". The existing naming contract, untouched.
#     - grade : a function-driven dimming layer that pushes listeners back. It is
#               the ONLY layer that ever carries alpha/matrixcolor (so a dim never
#               "sticks" to a pose via Matsu'Py's take_state). Its eased fraction
#               lives in Python (_autofocus_grade_cur), so it resumes -- never pops
#               -- even when the writer resets the at_list with `show <tag> at ...`.
#
# DIMMING MODES (persistent.autofocus_dim_mode -- wired to a settings option)
#     "darken"  : listeners darken via matrixcolor (stay opaque). gl2 only. DEFAULT.
#     "opaque"  : listeners fade to autofocus_dim_alpha (translucent).
#     "none"    : no dimming -- just the speaker's forward pop.
#   The grade function reads persistent.autofocus_dim_mode live, so all three modes
#   flow through it, and a settings change re-flows the live scene on the spot.
#   "darken" is the default because a translucent listener lets the BACKGROUND
#   show through them, which reads as a ghost rather than as depth; darkening
#   keeps the sprite solid and pushes it back the way stage lighting would.
#
# THE NAMING CONTRACT (poses)
#   Position transforms come in "families" of prefixed variants per slot. A slot
#   is a screen position id like "21"/"32"/"11" (see game/transforms.rpy). Per
#   family, prefixes encode the pose:
#     family ""        : t=rest, i=instant, f=focus, l/lf=left(+focus),
#                        h/hf=hop(+focus).
#   So sprite at transform `t21` is "resting in slot 21"; this addon swaps it to
#   `f21` (focus) when that character speaks, and back to `t21` otherwise.
#
# KEY FLOW (autofocus_focus_speaker, the character callback)
#   Only "begin" does work. It focuses the speaker (pose -> f) with a clear grade
#   and dims every other visible sprite (grade -> dim), skipping sprites placed
#   with a MANUAL, non-slot transform and never interrupting an entrance. On a
#   narration line (no on-screen speaker) it releases the whole scene back to
#   neutral. "end" is ignored: the focus/dim persists until the next "begin"
#   re-evaluates it -- so a character speaking several lines in a row holds steady
#   instead of flickering (no scry guessing of the next speaker).
#   _autofocus_slot_cache caches each tag's (slot,prefix,family); _autofocus_-
#   grade_state caches each tag's grade ("dim"/"clear"). Both cleared on scene
#   change so a sprite mid-transition still matches.
#
# PUBLIC API
#   autofocus_enabled       (default True)   -- whole system on/off.
#   persistent.autofocus_dim_mode       ("darken")      -- "none" | "opaque" | "darken".
#   autofocus_dim_alpha      (0.72)          -- listener alpha in "opaque" mode.
#   autofocus_dim_dark       (-0.35)         -- brightness delta in "darken" mode.
#   autofocus_set_enabled(bool) / autofocus_set_dim_mode(str) -- setters safe to
#       wire to a settings option; they tidy the live sprites on change.
#
# PERFORMANCE
#   Live pose transforms are reverse-mapped to (slot, prefix, family) through a
#   pair of lookup tables built once on first use, instead of re-scanning every
#   family x slot x prefix combination per sprite, per line.
#
# WHY THERE ARE TWO LOOKUP TABLES (the reload/load bug)
#   The fast path keys on id(), which is only valid for the transform objects the
#   CURRENT init built. Two things invalidate it while sprites are still on
#   screen: a hot reload (init re-runs and rebuilds every t*/f*/... object, but
#   the live sprites keep referencing the OLD ones) and loading a save (Matsu'Py
#   pickles the image stack, so the restored at_list holds COPIES). In both cases
#   every id() missed, the sprite looked like a manual placement, and autofocus
#   silently did nothing until the next `scene` re-showed everyone.
#   So the id() map is backed by a second map keyed on the pose's ATL block
#   location -- (filename, line), a plain VALUE tuple that both survives a
#   re-parse and pickles intact -- which makes the reverse mapping identity-free.
#
# init 999 (last): enables sticky positions so image-attribute say lines and
#   bare sprite refreshes retain the current slot unless the script explicitly
#   provides `at ...`. The DEFAULT rest transform (t11) is still registered for
#   each known character tag so their first bare show lands in a tracked slot.
# =============================================================================

# Automatic speaker focus for visible character sprites.

default autofocus_enabled = True
default persistent.autofocus_dim_mode = "darken"   # "none" | "opaque" | "darken"

# One-shot migration for persistents written before "darken" became the default.
# autofocus_dim_mode_chosen is set the moment the player touches the Speaker Focus
# setting, so an existing profile that never expressed a preference gets moved to
# the new default, while a deliberate "Opaque" pick is left alone forever.
default persistent.autofocus_dim_mode_chosen = False

# Look-and-feel constants (define = fixed, not saved). Tune to taste.
define autofocus_dim_alpha = 0.72        # listener opacity in "opaque" mode
define autofocus_dim_dark = -0.35        # listener brightness in "darken" mode
define autofocus_dim_time = 0.24         # dim/undim cross-fade, seconds

# The dim is applied by a function-driven "grade" transform (built in init python
# below) layered UNDER the pose. Its eased state lives in Python
# (_autofocus_grade_cur), NOT in the transform chain -- so it survives the writer
# freely re-showing a sprite with `show <tag> at <slot>`, which resets the at_list
# and would otherwise drop the grade and pop the dim mid-fade. The function reads
# the live mode, so "none"/"opaque"/"darken" all flow through the one transform.

init python:
    # Position slots (screen spots) and the transform "families"/prefixes that
    # encode each pose -- the naming contract described in the header.
    # Stages of one through six -- the slot table in game/transforms.rpy.
    _autofocus_slots = (
        "61", "62", "63", "64", "65", "66",
        "51", "52", "53", "54", "55",
        "41", "42", "43", "44",
        "31", "32", "33",
        "21", "22",
        "11")
    _autofocus_transform_families = (
        ("", ("t", "i", "f", "l", "lf", "h", "hf")),
    )
    # Tags that get a default rest transform registered at init 999 (below).
    # The roster is ENTER_M_SPRITE_TAGS, declared next to the `image` lines in
    # game/asset_definitions/def_characters.rpy -- a copy kept here went stale every
    # time a sprite was added there, and the failure is silent (a bare
    # `show <tag>` just never gets a tracked slot). Read at init 999.
    def _autofocus_default_tags():
        return getattr(store, "ENTER_M_SPRITE_TAGS", ())
    _autofocus_slot_cache = {}      # (layer, tag) -> (slot, prefix, family)
    _autofocus_grade_state = {}     # (layer, tag) -> "dim" | "clear" (the target)
    _autofocus_grade_cur = {}       # (layer, tag) -> eased dim fraction 0.0..1.0
    _autofocus_grade_last_st = {}   # (layer, tag) -> last shown-time, for ease dt
    _autofocus_active_speakers = {} # layer -> speaker tag
    _autofocus_lookup = {}          # id(pose transform) -> (slot, prefix, family)
    _autofocus_loc_lookup = {}      # pose ATL (filename, line) -> (slot, prefix, family)
    _autofocus_force_reapply = False  # one-shot: next "begin" repaints everything

    # The grade: a function transform (layered UNDER the pose) that eases a stored
    # dim fraction toward its target each frame and writes the matrixcolor/alpha
    # for the current mode. The fraction lives in _autofocus_grade_cur (Python),
    # so re-showing the sprite -- even after the writer reset its at_list, or after
    # several still lines -- resumes the ease from exactly where it was instead of
    # popping. Returns None once settled (no idle redraw); the plugin re-shows on
    # every target change, which restarts the function from the stored fraction.
    def _autofocus_grade_function(trans, st, at, layer, tag):
        key = (layer, tag)
        target = 1.0 if _autofocus_grade_state.get(key) == "dim" else 0.0
        cur = _autofocus_grade_cur.get(key, 0.0)

        # dt is integrated per-frame, so it MUST be a true frame delta. `last` is
        # dropped by _autofocus_apply on every target change (see there), so the
        # first frame of a freshly-installed grade has last=None -> dt=0 and
        # anchors `last` to whatever st this transform reports. That makes the
        # ease correct whether Matsu'Py reset st to 0 or carried the old
        # transform's st forward via take_state -- the latter, left unhandled,
        # produced a multi-second first-frame dt that snapped the dim instantly.
        last = _autofocus_grade_last_st.get(key)
        _autofocus_grade_last_st[key] = st
        dt = 0.0 if (last is None or st < last) else (st - last)

        if autofocus_dim_time <= 0:
            cur = target
        elif cur < target:
            cur = min(target, cur + dt / autofocus_dim_time)
        elif cur > target:
            cur = max(target, cur - dt / autofocus_dim_time)

        _autofocus_grade_cur[key] = cur

        mode = persistent.autofocus_dim_mode if autofocus_enabled else "none"

        if cur <= 0.0 or mode == "none":
            trans.matrixcolor = None
            trans.alpha = 1.0
        elif mode == "darken":
            trans.matrixcolor = BrightnessMatrix(autofocus_dim_dark * cur)
            trans.alpha = 1.0
        else:  # opaque
            trans.matrixcolor = None
            trans.alpha = 1.0 - (1.0 - autofocus_dim_alpha) * cur

        return 0 if cur != target else None

    # The grade callable MUST be picklable: the resulting Transform is attached to
    # a shown sprite, and Matsu'Py pickles the whole image stack on every save
    # (quicksave, rollback, the `_reload-1` hot-reload autosave...). A local
    # closure can't be pickled -- "Can't pickle local object" -- and crashes the
    # save. A module-level class instance carrying (layer, tag) as plain string
    # attributes pickles cleanly and looks up _autofocus_grade_function by name at
    # call time (so the function itself is never stored).
    class _AutofocusGrade(object):
        def __init__(self, layer, tag):
            self.layer = layer
            self.tag = tag

        def __call__(self, trans, st, at):
            return _autofocus_grade_function(trans, st, at, self.layer, self.tag)

    def _autofocus_grade_transform(layer, tag):
        return Transform(function=_AutofocusGrade(layer, tag))

    # Forget cached dim/pose state for tags that are no longer on screen, so a
    # sprite that was dimmed, hidden, and later re-shown starts fresh (neutral)
    # instead of resuming a stale dark fraction. Runs each "begin"; cheap.
    def _autofocus_prune_hidden(layer):
        for key in list(_autofocus_grade_cur.keys()):
            key_layer, key_tag = key

            if key_layer == layer and not renpy.showing(key_tag, layer=layer):
                _autofocus_grade_cur.pop(key, None)
                _autofocus_grade_last_st.pop(key, None)
                _autofocus_grade_state.pop(key, None)
                _autofocus_slot_cache.pop(key, None)

    def autofocus_set_enabled(enabled):
        global autofocus_enabled
        autofocus_enabled = bool(enabled)

        try:
            if not autofocus_enabled:
                _autofocus_active_speakers.pop("master", None)
                _autofocus_reset_all("master")
            else:
                autofocus_focus_speaker("begin")
        except Exception:
            pass

    def autofocus_set_dim_mode(mode):
        if mode not in ("none", "opaque", "darken"):
            mode = "darken"

        persistent.autofocus_dim_mode = mode
        # The player has now expressed a preference, so the one-time migration at
        # the bottom of this file must never second-guess it again.
        persistent.autofocus_dim_mode_chosen = True

        # Re-flow the live scene so the change is visible immediately: re-evaluate
        # who is dimmed (handles "none" <-> dimmed) and re-paint the dim sprites
        # so an opaque <-> darken switch cross-fades.
        try:
            if autofocus_enabled and _autofocus_active_speakers.get("master") is not None:
                autofocus_focus_speaker("begin")
            else:
                _autofocus_reset_all("master")
            _autofocus_reflow_dims("master")
        except Exception:
            pass

    def _autofocus_zorders(layer):
        try:
            return dict(renpy.get_zorder_list(layer))
        except Exception:
            return {}

    def _autofocus_transform(family, prefix, slot):
        return globals().get(family + prefix + slot)

    # A pose transform's identity that OUTLIVES this session's objects. Every
    # t*/f*/l*/h* pose is an ATLTransform, and its `.atl` is the RawBlock the
    # `transform` statement parsed; RawStatement.loc is a plain (filename, line)
    # tuple. Being a value rather than an object reference, it compares equal
    # across a hot-reload re-parse AND across the pickle/unpickle a save does to
    # the image stack -- which is exactly where id() fails (see the file header).
    # The grade layer is a plain Transform with no .atl, so it returns None and
    # is skipped, same as before.
    def _autofocus_atl_loc(transform):
        atl = getattr(transform, "atl", None)

        if atl is None:
            return None

        loc = getattr(atl, "loc", None)

        return loc if isinstance(loc, tuple) else None

    # Build the reverse maps once: every known {family+prefix+slot} pose object ->
    # its (slot, prefix, family) tuple, keyed BOTH by id() (the fast path for
    # sprites shown this session) and by ATL location (the durable path). init
    # re-runs on hot-reload, which clears both dicts, so nothing goes stale.
    def _autofocus_build_lookup():
        _autofocus_lookup.clear()
        _autofocus_loc_lookup.clear()
        for family, prefixes in _autofocus_transform_families:
            for slot in _autofocus_slots:
                for prefix in prefixes:
                    transform = _autofocus_transform(family, prefix, slot)
                    if transform is not None:
                        _autofocus_lookup[id(transform)] = (slot, prefix, family)
                        loc = _autofocus_atl_loc(transform)

                        if loc is not None:
                            _autofocus_loc_lookup[loc] = (slot, prefix, family)

    # Reverse-map a sprite's live `at` transform list back to (slot, prefix,
    # family). The grade layer isn't a pose, so it isn't in the lookup and is
    # skipped. Returns None if the sprite isn't using a known slot transform.
    def _autofocus_slot_from_at_list(at_list):
        if not at_list:
            return None

        if not _autofocus_lookup:
            _autofocus_build_lookup()

        for active_transform in at_list:
            match = _autofocus_lookup.get(id(active_transform))

            if match is not None:
                return match

        # id() missed on every entry. Either this sprite really is manually
        # placed, or its poses are pre-reload / post-load objects -- so fall back
        # to the location map before declaring it unmanaged.
        for active_transform in at_list:
            loc = _autofocus_atl_loc(active_transform)

            if loc is None:
                continue

            match = _autofocus_loc_lookup.get(loc)

            if match is not None:
                return match

        return None

    def _autofocus_at_list(tag, layer):
        try:
            at_list = renpy.get_at_list(tag, layer=layer)
        except Exception:
            return []

        return list(at_list or [])

    def _autofocus_manual_at_list(tag, layer):
        at_list = _autofocus_at_list(tag, layer)

        if at_list and _autofocus_slot_from_at_list(at_list) is None:
            return at_list

        return None

    def _autofocus_current_transform(tag, layer):
        if not renpy.showing(tag, layer=layer):
            _autofocus_slot_cache.pop((layer, tag), None)
            _autofocus_grade_state.pop((layer, tag), None)
            _autofocus_grade_cur.pop((layer, tag), None)
            _autofocus_grade_last_st.pop((layer, tag), None)
            return None

        at_list = _autofocus_at_list(tag, layer)
        current_transform = _autofocus_slot_from_at_list(at_list)

        if current_transform is not None:
            _autofocus_slot_cache[(layer, tag)] = current_transform
            return current_transform

        cached_transform = _autofocus_slot_cache.get((layer, tag))

        if cached_transform is not None:
            return cached_transform

        return None

    def _autofocus_focus_prefix(current_prefix, family):
        if family:
            return "f"

        if current_prefix in ("l", "lf"):
            return "lf"

        if current_prefix in ("h", "hf"):
            return "hf"

        return "f"

    # Re-show `tag` with [grade, pose], preserving its z-order, and remember the
    # resulting (slot, prefix, family) + grade kind. The workhorse that actually
    # changes a sprite's pose and/or dim.
    def _autofocus_apply(tag, layer, slot, family, target_prefix, grade_kind, zorders):
        pose = _autofocus_transform(family, target_prefix, slot)

        if pose is None:
            pose = _autofocus_transform(family, "t", slot)
            target_prefix = "t"

        if pose is None:
            return

        # Set the target BEFORE building the grade so the function's first frame
        # eases toward the right value from the stored fraction.
        _autofocus_grade_state[(layer, tag)] = grade_kind

        # Drop the dt baseline so the new grade Transform restarts its per-frame
        # integration cleanly. The new transform may inherit the old one's
        # shown-time (st) via take_state; a stale `last` here would make the grade
        # function see a huge first-frame dt and SNAP to the target instead of
        # easing. The eased fraction (_autofocus_grade_cur) is preserved, so the
        # dim still resumes from where it was rather than popping.
        _autofocus_grade_last_st.pop((layer, tag), None)

        # Order matters: the LAST at_list entry is the OUTERMOST transform, and
        # Matsu'Py's take_state copies a replaced transform's whole state (zoom,
        # position, ...) onto its replacement. So the grade MUST be inner and the
        # pose OUTER -- otherwise the grade would inherit the old pose's zoom and
        # multiply it into the new pose, shrinking/misplacing the sprite. As the
        # inner layer the grade only tints/fades the sprite the outer pose scales.
        grade = _autofocus_grade_transform(layer, tag)
        at_list = [grade, pose]

        kwargs = {
            "at_list": at_list,
            "layer": layer,
            "tag": tag,
        }

        if tag in zorders:
            kwargs["zorder"] = zorders[tag]

        renpy.show(tag, **kwargs)
        _autofocus_slot_cache[(layer, tag)] = (slot, target_prefix, family)

    def _autofocus_apply_if_changed(tag, layer, slot, family, prefix, target_prefix, grade_kind, zorders):
        current_grade = _autofocus_grade_state.get((layer, tag), "clear")

        # _autofocus_force_reapply is armed by autofocus_after_load: the cached
        # grade state is gone but the sprites on screen are still wearing the
        # saved session's dim, so "nothing changed" is a lie exactly once.
        if not _autofocus_force_reapply and prefix == target_prefix and grade_kind == current_grade:
            return

        _autofocus_apply(tag, layer, slot, family, target_prefix, grade_kind, zorders)

    def _autofocus_visible_tags(layer):
        return list(renpy.get_showing_tags(layer=layer, sort=True))

    # Lift every managed sprite back to a neutral, undimmed rest: focus poses ->
    # rest, any dim grade -> clear. Leaves manual placements and entrance/gesture
    # poses (i, l, h, d) where they are; only the grade clears.
    def _autofocus_reset_all(layer):
        zorders = _autofocus_zorders(layer)

        for tag in _autofocus_visible_tags(layer):
            current = _autofocus_current_transform(tag, layer)

            if current is None:
                continue

            if _autofocus_manual_at_list(tag, layer) is not None:
                continue

            slot, prefix, family = current
            current_grade = _autofocus_grade_state.get((layer, tag), "clear")
            target_prefix = "t" if prefix in ("f", "lf", "hf") else prefix

            if not _autofocus_force_reapply and prefix == target_prefix and current_grade == "clear":
                continue

            _autofocus_apply(tag, layer, slot, family, target_prefix, "clear", zorders)

    # Re-paint the currently-dimmed sprites in place (same pose, same dim) so the
    # grade re-evaluates persistent.autofocus_dim_mode -- used when the mode changes between
    # "opaque" and "darken" while a line is on screen.
    def _autofocus_reflow_dims(layer):
        zorders = _autofocus_zorders(layer)

        for tag in _autofocus_visible_tags(layer):
            if _autofocus_grade_state.get((layer, tag)) != "dim":
                continue

            current = _autofocus_current_transform(tag, layer)

            if current is None:
                continue

            if _autofocus_manual_at_list(tag, layer) is not None:
                continue

            slot, prefix, family = current
            _autofocus_apply(tag, layer, slot, family, prefix, "dim", zorders)

    # THE CHARACTER CALLBACK (registered below). Fires on each say "begin"/"end".
    # We only act on "begin": it focuses the new speaker (clear grade) + dims the
    # rest, or -- on a narration line -- releases the whole scene. Honors
    # autofocus_enabled, skips manual placements, and never interrupts an entrance.
    def autofocus_focus_speaker(event, interact=True, **kwargs):
        global _autofocus_force_reapply
        layer = "master"

        if not autofocus_enabled:
            _autofocus_active_speakers.pop(layer, None)
            return

        # Deliberately do NOTHING on "end". Every transition is driven by the next
        # "begin", so the focus/dim simply persists between lines. Releasing on
        # "end" used to depend on scry-predicting the next speaker; when that
        # guessed wrong it un-dimmed and the following "begin" re-dimmed -- a
        # visible flicker (worst in "darken" mode) every time the same character
        # spoke two lines in a row. Holding until the next "begin" is flicker-free.
        if event != "begin":
            return

        _autofocus_prune_hidden(layer)

        speaker_tag = renpy.get_say_image_tag()

        # Narration line, or the speaker has no on-screen sprite: nobody to focus,
        # so release any standing dim from a previous line. After a load there is
        # no recorded speaker to pop, but the restored sprites may still be wearing
        # one -- hence the force flag also triggering the release here.
        if speaker_tag is None or not renpy.showing(speaker_tag, layer=layer):
            had_speaker = _autofocus_active_speakers.pop(layer, None) is not None

            if had_speaker or _autofocus_force_reapply:
                _autofocus_reset_all(layer)

            _autofocus_force_reapply = False
            return

        _autofocus_active_speakers[layer] = speaker_tag

        dim_wanted = persistent.autofocus_dim_mode != "none"
        zorders = _autofocus_zorders(layer)

        for tag in _autofocus_visible_tags(layer):
            current = _autofocus_current_transform(tag, layer)

            if current is None:
                continue

            if _autofocus_manual_at_list(tag, layer) is not None:
                continue

            slot, prefix, family = current
            focused = tag == speaker_tag

            if focused:
                target_prefix = _autofocus_focus_prefix(prefix, family)

                if _autofocus_transform(family, target_prefix, slot) is None:
                    target_prefix = prefix

                grade_kind = "clear"
            else:
                # Pull a previously-focused listener back to rest; otherwise leave
                # the pose alone (the grade handles the dim on its own layer).
                target_prefix = "t" if prefix in ("f", "lf", "hf") else prefix
                grade_kind = "dim" if dim_wanted else "clear"

            _autofocus_apply_if_changed(tag, layer, slot, family, prefix, target_prefix, grade_kind, zorders)

        # The forced repaint is spent: every managed sprite has just been re-shown
        # with a grade this session actually owns.
        _autofocus_force_reapply = False

    def autofocus_clear_scene_state(layer):
        if layer != "master":
            return

        _autofocus_slot_cache.clear()
        _autofocus_grade_state.clear()
        _autofocus_grade_cur.clear()
        _autofocus_grade_last_st.clear()
        _autofocus_active_speakers.pop(layer, None)

    # Loading a save (or a Shift+R reload, which loads _reload-1) drops a whole
    # new image stack on us: its sprites were shown -- and graded -- in the SAVED
    # session, so none of this session's per-tag caches describe them, and the
    # restored grade Transforms carry a dim fraction that the now-empty
    # _autofocus_grade_cur no longer agrees with. Matsu'Py re-runs the interrupted
    # say statement right after this, which fires "begin" and heals the poses; the
    # only thing that CAN'T heal on its own is a grade, because the empty cache
    # reads as "clear" and _autofocus_apply_if_changed would then skip a sprite
    # that is still visibly dark. So arm a one-shot flag that makes the next
    # "begin" re-apply every managed sprite unconditionally.
    def autofocus_after_load():
        global _autofocus_force_reapply
        autofocus_clear_scene_state("master")
        _autofocus_lookup.clear()
        _autofocus_loc_lookup.clear()
        _autofocus_force_reapply = True

    # Hook into Matsu'Py: run on every say begin/end, reset cache on scene change,
    # and resync the whole scene after a save is loaded / the game is reloaded.
    config.all_character_callbacks.append(autofocus_focus_speaker)
    config.scene_callbacks.append(autofocus_clear_scene_state)
    config.after_load_callbacks.append(autofocus_after_load)

# init 999 (after transforms.rpy defines t11): let implicit sprite refreshes keep
# their current slot, and give first-time bare shows a tracked default slot.
init 999 python:
    config.sticky_positions = True

    # ONE-TIME DEFAULT MIGRATION ("opaque" -> "darken").
    # `default persistent.x` never overwrites a value an existing profile already
    # carries, so simply changing the default above would leave every returning
    # player on the old mode forever. autofocus_dim_mode_chosen is only ever set
    # by autofocus_set_dim_mode (i.e. by the player using the Speaker Focus
    # setting), so a False here means "this is the old default, not a choice".
    if not persistent.autofocus_dim_mode_chosen:
        if persistent.autofocus_dim_mode == "opaque":
            persistent.autofocus_dim_mode = "darken"

        persistent.autofocus_dim_mode_chosen = True

    _autofocus_default_transform = _autofocus_transform("", "t", "11")

    if _autofocus_default_transform is not None:
        for _autofocus_tag in _autofocus_default_tags():
            config.tag_transform.setdefault(_autofocus_tag, _autofocus_default_transform)
