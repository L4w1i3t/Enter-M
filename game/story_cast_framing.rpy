# ENTER M -- main-story cast framing: one head size, heights from the roster,
# and each figure seated inside its own story panel.
#
# This changes the size of a SHOWN story sprite, never its registered image.
# ArchivePortraitCrop, phone photos, the roster and all screen `add` consumers
# therefore continue to receive the original displayable at its original size.
# Slot ATL stays outermost: entrances, focus, hops and crowd scales still own
# the same position/animation state. Standalone custom transforms and inline
# ATL opt out. A compound [slot, custom] at-list follows Autofocus's existing
# slot ownership; it is not a second independently authored camera system.
#
# THE EQUALIZER (rebuilt Sep 26 2026). The registered art does not share a
# camera: every PNG is contained in the same 640x960 box, but each figure was
# drawn at its own distance, and eye lines sit 110px apart for reasons that have
# nothing to do with height (Monika is DDLC's 960x960 plate). Each figure is
# measured once, on its registered neutral image, and framed from:
#
#   * CAMERA -- a per-art correction to one house camera distance, judged
#     against the cast that already agree (Sam, MC, Matsuda, Kotonoha).
#     Tsubaki and Asahina are drawn ~6% closer (their faces and shoulders
#     both measure larger than their peers'), Monika's plate runs large, Mom
#     slightly. Face length alone was tried and rejected: it is a style
#     feature, not a distance (Sam's tilted head measures 20% "bigger").
#   * STATURE -- a mild whole-figure scale, (height / reference) ** 0.5. Height
#     shown by placement alone made the two shortest girls read as standing
#     CLOSER to the camera rather than as smaller people, because their
#     bodies were drawn as large as everyone else's.
#   * HEIGHT -- the eye line sits ENTER_M_CAST_PPI px higher per inch of
#     canonical height, around ENTER_M_CAST_EYE_Y for the reference. The
#     frame is cropped below the eye (never padded past its own art) so the
#     slot's bottom anchor lands it there.
#   * HOUSE CAMERA (Oct 11 2026) -- ENTER_M_CAST_ZOOM scales the whole framed
#     cast about the slots' floor line, after the three rules above. Every
#     relationship between figures (sizes, eye spacing per inch) scales with
#     it, and because it lives in the frame rather than the slots, every slot
#     family and every stage size from one to eight inherits it.
#
# Outfits, expression plates and pose images are registered to their base, so
# one entry per character covers all of them. Incidental cast have no Roster
# heights, so theirs are read off their art and their role (see the table).
#
# THE CAST MASK. While Story Panels are engaged, each framed sprite is masked to
# its own panel (enter_m.cast_mask, geometry published by stage_panels.rpy), so
# a gutter cuts the cast exactly where it cuts the room and every panel is a
# shot rather than a strip of wallpaper behind a row of standees. The speaker's
# mask is let out past their cuts (the pop-out), and listener panels -- figure
# and room together -- fall back as one camera. With Speaker Focus on "Darken"
# the panel does that darkening, so Autofocus's matrixcolor is withheld for a
# masked sprite; "Opaque" and "None" are untouched.

init 999 python:

    # tag: (eye line y, camera correction, canonical height in inches), the
    # eye line measured at 4x on the registered neutral image at its registered
    # size (mean of the pupils). The named cast's heights are the Roster's;
    # None stands a figure on the reference line.
    ENTER_M_CAST_BODY = {
        "sam": (177.0, 1.00, 71),
        "mc": (168.75, 1.00, 70),
        "matsuda": (219.5, 1.00, 69),
        "mom": (172.4, 0.97, 66),
        "monika": (279.0, 0.94, 65),
        "kotonoha": (190.75, 1.00, 65),
        "tsubaki": (231.5, 0.94, 64),
        "asahina": (196.75, 0.94, 64),
        # Incidental cast (Oct 11 2026). No canon heights, so each is read
        # off the art and the role. Cameras match pupil distance against the
        # reference group (Sam, MC and Kotonoha all measure about 72.5px); the
        # photographic adults match on shoulder width instead, since a
        # photographed face cannot be compared with a drawn one.
        "charlie": (174.5, 1.00, 69),         # lean teenage distance runner
        # Hikari and Homura are drawn with the same head (pupils 75px apart,
        # crown to chin 246 vs 251), so they share a camera and only their
        # heights differ. Hikari's BODY is drawn small because she is petite,
        # not because the camera is far: the old 1.08, which matched her
        # shoulders to her peers', made her head the largest on stage.
        "homura": (214.0, 0.97, 67),          # tall, long-legged
        "hikari": (382.0, 0.97, 60),          # petite
        "math_teacher": (149.0, 1.00, 70),    # average middle-aged man
        "civics_teacher": (158.0, 1.00, 64),  # average middle-aged woman
        # At 1.00 his shoulders measured narrower than the math teacher's.
        # Eye re-read at 8x on Oct 11: the irises sit at 134.5, not 143.
        "track_coach": (134.5, 1.08, 72),     # tall, athletic
        # Photographic teacher cutouts added Oct 11. Pupil means measured on
        # their 1024x1536 art, then scaled to the registered 640x960 images.
        "science_teacher": (130.3, 1.00, 64),
        "japanese_teacher": (154.7, 1.00, 64),
        "english_teacher": (158.4, 1.00, 64),
        # Daichi still uses the shared placeholder, sized as a teenage boy.
        "daichi": (170.0, 1.00, 69),
    }

    ENTER_M_CAST_REF_HEIGHT = 66.0  # inches that stand on the reference eye line
    ENTER_M_CAST_STATURE = 0.5      # whole-figure scale exponent on relative height
    ENTER_M_CAST_EYE_Y = 262.0      # screen y of that eye line at slot zoom 0.80
    ENTER_M_CAST_PPI = 14.0         # screen px per inch of height at slot zoom 0.80
    ENTER_M_CAST_FLOOR = 741.6      # the slots' bottom anchor: ypos 1.03 * 720
    ENTER_M_CAST_REF_ZOOM = 0.80    # the one- to three-person slot zoom

    # The house camera, applied about the floor line after everything above
    # (EYE_Y and PPI are measured at 1.0). At 1.0 the tallest head, Sam's,
    # rested 61px under the top of the frame; at 1.06 it rests 20px under,
    # and while he speaks the focus pose (4.5% about the floor) takes the
    # top 17px of his hair past the edge (32px at 1.08).
    ENTER_M_CAST_ZOOM = 1.06

    # Stage size -> the slot zoom in transforms.rpy / story_crowd_slots.rpy,
    # and the closer zoom a masked crowd is framed at instead. Seven and eight
    # share panels, so neighbours overlap at the shoulder there, but faces
    # stay clear at 0.70 and 0.66; left at their slot zooms, every face sank
    # into the lower half of the frame (Oct 11 2026).
    ENTER_M_CAST_SLOT_ZOOM = {1: 0.80, 2: 0.80, 3: 0.80, 4: 0.74, 5: 0.68,
        6: 0.63, 7: 0.58, 8: 0.54}
    ENTER_M_CAST_CROWD_ZOOM = {4: 0.78, 5: 0.76, 6: 0.74, 7: 0.70, 8: 0.66}

    def _story_cast_framing(tag):
        """(scale, eye line in the unscaled image, frame depth below the eye)."""
        eye, camera, height = ENTER_M_CAST_BODY[tag]

        if height is None:
            height = ENTER_M_CAST_REF_HEIGHT

        relative = float(height) / ENTER_M_CAST_REF_HEIGHT
        scale = (ENTER_M_CAST_ZOOM * float(camera)
            * relative ** ENTER_M_CAST_STATURE)
        eye_screen = (ENTER_M_CAST_EYE_Y
            - (float(height) - ENTER_M_CAST_REF_HEIGHT) * ENTER_M_CAST_PPI)
        # Zooming about the floor scales the depth below the eye with the
        # figure, so the art left below the crop grows too: no hem can show.
        depth = (ENTER_M_CAST_ZOOM * (ENTER_M_CAST_FLOOR - eye_screen)
            / ENTER_M_CAST_REF_ZOOM)

        return (round(scale, 5), float(eye), round(depth, 3))

    def _story_cast_in_menu():
        return bool(getattr(renpy.context(), "_menu", False)
            or getattr(store, "main_menu", False))

    def _story_cast_active(layer="master"):
        # Deliberately independent of persistent.enter_m_panels: switching off
        # background splits should not change the cast's apparent stature.
        return (layer == "master"
            and not _story_cast_in_menu()
            and bool(_stage_state["scope"])
            and _stage_state["suspend"] <= 0)

    def _story_cast_mask_entry(tag):
        """This tag's panel cut, or None when the cast is not being masked."""
        if not (ENTER_M_STAGE_PANEL_SHADER and _stage_panels_active()):
            return None

        return _stage_mask_for(tag)

    def _story_cast_mask_moving():
        """True while the cuts are still easing AND a bg is driving them."""
        if _stage_panels_settled():
            return False

        now = getattr(renpy.display.interface, "frame_time", None)
        painted = _stage_mask["t"]

        # No paint in the last half second means nothing is advancing the
        # layout (an opted-out bg, a CG): asking for frames would spin forever.
        return now is not None and painted is not None and now - painted < 0.5

    class _StoryCastFrame(renpy.Displayable):
        """One local sizing layer; no polling or alpha-bound scans per frame."""

        def __init__(self, child, tag, layer):
            super(_StoryCastFrame, self).__init__()
            self.child = child
            self.tag = tag
            self.layer = layer
            self._framing_signature = None
            self._refresh_framing()
            self.active = _story_cast_active(layer)

        def _refresh_framing(self):
            signature = _story_cast_framing(self.tag)
            if getattr(self, "_framing_signature", None) == signature:
                return False
            # Saved displayables may carry an earlier scale/crop pair. Refresh
            # the cached child once; the new signature replaces it for good.
            self.framing_scale, self.eye_y, self.frame_depth = signature
            self.framed = Transform(self.child,
                zoom=self.framing_scale, subpixel=True)
            self._framing_signature = signature
            return True

        def _current_mode(self):
            # A game-menu context can render the frozen story underneath it.
            # Keep that picture's last camera distance while rejecting NEW
            # menu shows at the integration seam below.
            if _story_cast_in_menu():
                return self.active
            return _story_cast_active(self.layer)

        def per_interact(self):
            changed = self._refresh_framing()
            active = self._current_mode()
            if active != self.active or changed:
                self.active = active
                renpy.redraw(self, 0)

        def render(self, width, height, st, at):
            self._refresh_framing()
            self.active = self._current_mode()

            if not self.active:
                child_render = renpy.render(self.child, width, height, st, at)
                w, h = child_render.get_size()
                result = renpy.Render(w, h)
                result.blit(child_render, (0, 0))
                return result

            child_render = renpy.render(self.framed, width, height, st, at)
            w, h = child_render.get_size()

            # Crop below the eye so the slot's bottom anchor puts the eye line
            # where this character's height says. Never pad past the art: a
            # frame taller than the image would lift the cut-off hem into view.
            depth = self.eye_y * self.framing_scale + self.frame_depth
            frame_h = max(1.0, min(h, depth))

            if frame_h < h:
                child_render = child_render.subsurface((0, 0, w, frame_h))

            entry = (_story_cast_mask_entry(self.tag)
                if id(self) in _story_cast_members else None)
            boost = self._crowd_boost() if entry is not None else 1.0

            result = renpy.Render(w * boost, frame_h * boost)

            if boost != 1.0:
                result.zoom(boost, boost)

            if entry is not None:
                left, right, fx, slack, _width, voice, _count = entry
                slant, gap = _stage_mask["edge"]
                result.add_shader("enter_m.cast_mask")
                result.add_uniform("u_em_cm_edge", (left, right, slant, gap))
                result.add_uniform("u_em_cm_look", _stage_mask["look"])
                result.add_uniform("u_em_cm_fx", (fx[0], fx[1], fx[2], slack))
                result.add_uniform("u_em_cm_acc", voice)
                result.add_uniform("u_em_cm_glow", ENTER_M_PANEL_GLOW)

                if _story_cast_mask_moving():
                    renpy.redraw(self, 0)

            result.blit(child_render, (0, 0))
            return result

        def _crowd_boost(self):
            # A masked crowd cannot pile up, so it no longer has to stand back:
            # frame it at ENTER_M_CAST_CROWD_ZOOM instead of the slot's own
            # zoom. Scaling the whole frame about its bottom keeps every eye
            # line on the same height rule. Rides engagement, so switching the
            # panels off eases the crowd back rather than popping it.
            try:
                match = _autofocus_slot_from_at_list(
                    list(renpy.get_at_list(self.tag, layer=self.layer) or ()))
            except Exception:
                match = None
            if match is not None:
                self.stage_size = int(match[0][0])
            size = getattr(self, "stage_size", None)
            crowd = ENTER_M_CAST_CROWD_ZOOM.get(size)
            if not crowd:
                return 1.0
            slot = ENTER_M_CAST_SLOT_ZOOM[size]
            return 1.0 + (crowd / slot - 1.0) * max(0.0, min(1.0, _stage_state["amt"]))

        def event(self, ev, x, y, st):
            return (self.framed if self.active else self.child).event(ev, x, y, st)

        def visit(self):
            # The framed transform already visits the same unscaled child.
            return [self.framed]

    class _StoryCastFrameFactory(object):
        """Picklable at-list entry, recognised by type after save/rollback."""

        def __init__(self, tag, layer):
            self.tag = tag
            self.layer = layer

        def __call__(self, child):
            return _StoryCastFrame(child, self.tag, self.layer)

    class _StoryCastGradeFactory(object):
        """Compose sizing beneath Autofocus's existing, unchanged grade."""

        def __init__(self, grade, tag, layer):
            self.grade = grade
            self.tag = tag
            self.layer = layer

        def __call__(self, child):
            return self.grade(child=_StoryCastFrame(child, self.tag, self.layer))

    # THE PANEL WAKES THE CAST. A new layout target redraws the bg (whose driver
    # then runs every frame until settled); the masks have to be kicked the
    # same way, after which each keeps asking for frames while the cuts move.
    def _story_cast_frames_under(displayable, depth=0):
        if displayable is None or depth > 12:
            return
        if isinstance(displayable, _StoryCastFrame):
            yield displayable
            return
        try:
            children = displayable.visit() or ()
        except Exception:
            return
        for child in children:
            for frame in _story_cast_frames_under(child, depth + 1):
                yield frame

    # WHICH FRAMES ARE ON THE STAGE NOW. A dissolve re-renders the OUTGOING
    # scene's sprites every frame, and the cut geometry is global: measured
    # mid-dissolve, an old centre-slot Kotonoha was clipped by the NEW scene's
    # right-hand panel because the new scene also had a Kotonoha. So a frame
    # is masked only while it belongs to the master layer's current entries
    # (hiding ones included, so an exit still closes on its panel). This is
    # re-derived at every interaction start rather than stamped, so rollback
    # and load restore it for free; `scene` empties it until the next one.
    _story_cast_members = set()

    def _story_cast_collect():
        frames = []
        try:
            entries = renpy.game.context().scene_lists.layers.get("master", ())
        except Exception:
            entries = ()
        for entry in entries:
            # A hiding sprite's entry is re-tagged "hide$<tag>" while its
            # hide ATL runs (scenelists.py); it still belongs to this stage.
            tag = (entry.tag or "").rpartition("$")[2]
            if tag not in ENTER_M_CAST_BODY:
                continue
            frames.extend(_story_cast_frames_under(entry.displayable))
        _story_cast_members.clear()
        _story_cast_members.update(id(frame) for frame in frames)
        return frames

    def _story_cast_wake():
        for frame in _story_cast_collect():
            renpy.redraw(frame, 0)

    def _story_cast_scene(layer):
        if layer == "master":
            _story_cast_members.clear()

    _stage_panels_wake_hooks.append(_story_cast_wake)
    config.scene_callbacks.append(_story_cast_scene)

    # With Speaker Focus on "Darken", a masked story sprite is darkened by its
    # panel (one grade for figure and room), so the grade's own matrixcolor is
    # withheld. The grade still eases and still owns "Opaque" alpha.
    _story_cast_previous_grade_function = _autofocus_grade_function

    def _autofocus_grade_function(trans, st, at, layer, tag):
        result = _story_cast_previous_grade_function(trans, st, at, layer, tag)
        if (trans.matrixcolor is not None
                and layer == "master"
                and tag in ENTER_M_CAST_BODY
                and _stage_panel_dim_strength() > 0.0
                and _story_cast_active(layer)
                and _story_cast_mask_entry(tag) is not None):
            trans.matrixcolor = None
        return result

    _story_cast_previous_show = config.show
    _story_cast_previous_grade = _autofocus_grade_transform

    def _story_cast_grade_transform(layer, tag):
        # Autofocus's resumed-say callback precedes the panel callback after a
        # load, which deliberately cleared the scope latch. Prove it now.
        _stage_panels_scope_update()
        grade = _story_cast_previous_grade(layer, tag)
        # Autofocus calls renpy.show directly, so config.show cannot intercept
        # its replacement [grade, pose]. Its caller has already proved a slot.
        if tag in ENTER_M_CAST_BODY and _story_cast_active(layer):
            return _StoryCastGradeFactory(grade, tag, layer)
        return grade

    def _story_cast_is_exit(transforms):
        # `show tag at thide; hide tag` is the story's standard exit idiom.
        # thide intentionally owns no scale, so it must retain the previous
        # slot's inner framing while its outer ATL inherits pose state.
        expected = _autofocus_atl_loc(thide)
        return len(transforms) == 1 and (
            transforms[0] is thide
            or (expected is not None
                and _autofocus_atl_loc(transforms[0]) == expected))

    def _story_cast_show(name, at_list=(), layer=None, what=None, zorder=None,
            tag=None, behind=(), atl=None, transient=False, munge_name=True):
        names = tuple(name.split()) if isinstance(name, str) else tuple(name)
        key = tag or names[0]
        if key not in ENTER_M_CAST_BODY:
            return _story_cast_previous_show(name, at_list=at_list,
                layer=layer, what=what, zorder=zorder, tag=tag, behind=behind,
                atl=atl, transient=transient, munge_name=munge_name)
        target_layer = renpy.exports.default_layer(layer, key)
        _stage_panels_scope_update()

        inherited = list(renpy.get_at_list(key, layer=target_layer) or ())
        transforms = list(at_list or ())
        if not transforms and config.sticky_positions:
            transforms = list(inherited)
        if not transforms:
            fallback = config.tag_transform.get(key)
            if fallback is not None:
                transforms = list(fallback) if isinstance(fallback, (list, tuple)) else [fallback]

        # Rebuild exactly once around the source image. Repeated bare shows,
        # attribute updates, and restored at-lists cannot multiply the scale.
        transforms = [item for item in transforms
            if not isinstance(item, _StoryCastFrameFactory)]
        known_exit = (_story_cast_is_exit(transforms)
            and any(isinstance(item, (_StoryCastFrameFactory,
                _StoryCastGradeFactory)) for item in inherited))
        eligible = (_story_cast_active(target_layer)
            and what is None and atl is None
            and (_autofocus_slot_from_at_list(transforms) is not None or known_exit))

        if eligible:
            if not any(isinstance(item, _StoryCastGradeFactory)
                    for item in transforms):
                transforms.insert(0, _StoryCastFrameFactory(key, target_layer))
        else:
            # A new custom placement or out-of-scope show must not inherit a
            # framed grade left behind in the sticky position list.
            transforms = [item.grade if isinstance(item, _StoryCastGradeFactory)
                else item for item in transforms]

        return _story_cast_previous_show(name, at_list=transforms,
            layer=target_layer, what=what, zorder=zorder, tag=tag,
            behind=behind, atl=atl, transient=transient, munge_name=munge_name)

    config.show = _story_cast_show
    _autofocus_grade_transform = _story_cast_grade_transform

    _story_cast_restore_pending = False

    def _story_cast_after_load():
        global _story_cast_restore_pending
        _story_cast_restore_pending = True

    def _story_cast_restore_legacy_stage():
        global _story_cast_restore_pending
        if not _story_cast_restore_pending:
            return
        _story_cast_restore_pending = False
        _stage_panels_scope_update()
        if not _story_cast_active():
            return

        # An older save has no sizing layer, including when Speaker Focus is
        # disabled. Repair only its known slots once, preserving attributes,
        # ordering and pose. New saves already contain their picklable layer.
        for tag in renpy.get_showing_tags(layer="master"):
            if tag not in ENTER_M_CAST_BODY:
                continue
            transforms = list(renpy.get_at_list(tag, layer="master") or ())
            if (not any(isinstance(item, (_StoryCastFrameFactory,
                    _StoryCastGradeFactory)) for item in transforms)
                    and _autofocus_slot_from_at_list(transforms) is not None):
                config.show(tag, layer="master", at_list=transforms)

    config.after_load_callbacks.append(_story_cast_after_load)
    config.start_interact_callbacks.append(_story_cast_restore_legacy_stage)
    # Last, after anything above that may re-show a sprite this interaction.
    config.start_interact_callbacks.append(_story_cast_collect)
