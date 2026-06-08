# Automatic speaker focus for visible character sprites.

default autofocus_enabled = True

init python:
    _autofocus_slots = ("41", "42", "43", "44", "31", "32", "33", "21", "22", "11")
    _autofocus_transform_families = (
        ("", ("t", "i", "f", "l", "lf", "h", "hf")),
        ("cs_m01_", ("t", "f", "l", "h", "d")),
    )
    _autofocus_default_tags = (
        "monika", "sayori", "natsuki", "yuri",
        "matsuda", "tsubaki", "asahina", "sam", "kotonoha", "mom", "mc",
        "math_teacher", "civics_teacher", "science_teacher", "japanese_teacher",
        "english_teacher", "track_coach", "hikari", "homura",
    )
    _autofocus_slot_cache = {}
    _autofocus_active_speakers = {}

    def autofocus_set_enabled(enabled):
        global autofocus_enabled
        autofocus_enabled = bool(enabled)

        if not autofocus_enabled:
            _autofocus_active_speakers.pop("master", None)

    def _autofocus_zorders(layer):
        try:
            return dict(renpy.get_zorder_list(layer))
        except Exception:
            return {}

    def _autofocus_transform(family, prefix, slot):
        return globals().get(family + prefix + slot)

    def _autofocus_slot_from_at_list(at_list):
        if at_list is None:
            return None

        for active_transform in at_list:
            for family, prefixes in _autofocus_transform_families:
                for slot in _autofocus_slots:
                    for prefix in prefixes:
                        if active_transform is _autofocus_transform(family, prefix, slot):
                            return (slot, prefix, family)

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

    def _autofocus_apply(tag, layer, slot, current_prefix, family, focused, zorders):
        transform_prefix = _autofocus_focus_prefix(current_prefix, family) if focused else "t"
        transform = _autofocus_transform(family, transform_prefix, slot)

        if transform is None and focused:
            transform_prefix = "f"
            transform = _autofocus_transform(family, transform_prefix, slot)

        if transform is None:
            return None

        kwargs = {
            "at_list": [transform],
            "layer": layer,
            "tag": tag,
        }

        if tag in zorders:
            kwargs["zorder"] = zorders[tag]

        renpy.show(tag, **kwargs)
        _autofocus_slot_cache[(layer, tag)] = (slot, transform_prefix, family)
        return transform

    def _autofocus_next_say_image_tag():
        try:
            scry = renpy.scry()

            if scry is None:
                return None

            next_scry = scry.next()

            if next_scry is None or not next_scry.say or next_scry.interacts is False:
                return None

            return getattr(next_scry.who, "image_tag", None)
        except Exception:
            return None

    def _autofocus_visible_tags(layer):
        return list(renpy.get_showing_tags(layer=layer, sort=True))

    def _autofocus_unfocus_tag(tag, layer):
        current_transform = _autofocus_current_transform(tag, layer)

        if current_transform is None:
            return

        slot, current_prefix, family = current_transform

        if current_prefix == "t" and _autofocus_slot_from_at_list(_autofocus_at_list(tag, layer)) is not None:
            return

        _autofocus_apply(tag, layer, slot, current_prefix, family, False, _autofocus_zorders(layer))

    def _autofocus_end_speaker(layer):
        speaker_tag = _autofocus_active_speakers.get(layer)

        if speaker_tag is None:
            speaker_tag = renpy.get_say_image_tag()

        if (
            speaker_tag is not None
            and renpy.showing(speaker_tag, layer=layer)
            and _autofocus_next_say_image_tag() == speaker_tag
        ):
            return

        _autofocus_active_speakers.pop(layer, None)

        if speaker_tag is not None and renpy.showing(speaker_tag, layer=layer):
            _autofocus_unfocus_tag(speaker_tag, layer)

    def autofocus_focus_speaker(event, interact=True, **kwargs):
        layer = "master"

        if not autofocus_enabled:
            _autofocus_active_speakers.pop(layer, None)
            return

        if event == "end":
            _autofocus_end_speaker(layer)
            return

        if event != "begin":
            return

        speaker_tag = renpy.get_say_image_tag()

        if speaker_tag is None:
            _autofocus_active_speakers.pop(layer, None)
            return

        if not renpy.showing(speaker_tag, layer=layer):
            _autofocus_active_speakers.pop(layer, None)
            return

        _autofocus_active_speakers[layer] = speaker_tag

        zorders = _autofocus_zorders(layer)

        for tag in _autofocus_visible_tags(layer):
            current_transform = _autofocus_current_transform(tag, layer)

            if current_transform is None:
                continue

            slot, current_prefix, family = current_transform
            focused = tag == speaker_tag
            manual_at_list = _autofocus_manual_at_list(tag, layer)

            if manual_at_list is not None:
                continue

            focus_prefix = _autofocus_focus_prefix(current_prefix, family)

            if focused:
                speaker_transform = _autofocus_transform(family, focus_prefix, slot)

                if speaker_transform is None:
                    continue

                if current_prefix == focus_prefix:
                    continue
            elif current_prefix not in ("f", "lf", "hf"):
                continue

            _autofocus_apply(tag, layer, slot, current_prefix, family, focused, zorders)

    def autofocus_clear_scene_state(layer):
        if layer != "master":
            return

        _autofocus_slot_cache.clear()
        _autofocus_active_speakers.pop(layer, None)

    config.all_character_callbacks.append(autofocus_focus_speaker)
    config.scene_callbacks.append(autofocus_clear_scene_state)

init 999 python:
    _autofocus_default_transform = _autofocus_transform("", "t", "11")

    if _autofocus_default_transform is not None:
        for _autofocus_tag in _autofocus_default_tags:
            config.tag_transform.setdefault(_autofocus_tag, _autofocus_default_transform)
