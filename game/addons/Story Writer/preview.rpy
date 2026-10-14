# Developer Story Writer: typed scene adapters and isolated reading preview.
# Source expressions are never evaluated by this module. Registered images and
# the explicitly listed authored transforms retain their normal engine behavior.

init 20 python:
    import ast as _sw_ast
    import copy as _sw_copy
    import math as _sw_math
    import re as _sw_re
    import traceback as _sw_traceback

    _sw_catalog_cache = {}
    _sw_preview_active = False
    _sw_preview_nvl_page = False
    _sw_audition_paused = {}
    _SW_PREVIEW_CHANNELS = {
        "music": "sw_preview_music", "sound": "sw_preview_sound",
        "voice": "sw_preview_voice",
    }
    _SW_NAME_DEFAULTS = {
        "player": "Asahiko", "m_name": "Monika", "ma_name": "Matsuda",
        "ts_name": "Tsubaki", "as_name": "Asahina", "sa_name": "Sam",
        "ko_name": "Kotonoha", "mom_name": "Mom",
    }
    _SW_TRANSFORM_SIGNATURES = {
        "tcommon": ("x", "z"), "tinstant": ("x", "z"),
        "focus": ("x", "z"), "sink": ("x", "z"), "hop": ("x", "z"),
        "hopfocus": ("x", "z"), "leftin": ("x", "z"),
        "leftfocus": ("x", "z"), "thide": ("z",), "noise_alpha": (),
        "fx_flinch": ("reach",), "fx_lean_in": ("z", "secs"),
        "fx_push": ("z", "secs"),
        "fx_shake_decay": ("amp", "secs", "over", "curve", "start"),
        "truecenter": (), "center": (), "left": (), "right": (),
        "topleft": (), "topright": (), "top": (), "reset": (), "s11": (),
    }
    for _sw_family in ("t", "i", "f", "h", "l", "hf", "lf"):
        for _sw_count in range(1, 7):
            for _sw_slot in range(1, _sw_count + 1):
                _SW_TRANSFORM_SIGNATURES["%s%d%d" % (_sw_family, _sw_count, _sw_slot)] = ()

    _SW_TRANSITION_SIGNATURES = {
        "None": (), "dissolve": (), "fade": (), "pixellate": (),
        "vpunch": (), "hpunch": (), "wipeleft": (), "wiperight": (),
        "wipeup": (), "wipedown": (), "slideleft": (), "slideright": (),
        "slideup": (), "slidedown": (), "move": (), "moveinleft": (),
        "moveinright": (), "moveoutleft": (), "moveoutright": (),
        "Dissolve": ("time",), "Fade": ("out_time", "hold_time", "in_time"),
        "Pixellate": ("time", "steps"),
        "dissolve_scene_full": (), "dissolve_scene_half": (),
        "dissolve_scene_soft": (), "wipeleft_scene": (),
    }

    class SWPreviewBoundary(Exception):
        """A preserved expression/statement needs explicit author setup."""
        pass

    class SWPreviewCancelled(Exception):
        pass

    def sw_catalog_images():
        if "images" not in _sw_catalog_cache:
            _sw_catalog_cache["images"] = tuple(sorted(
                name if isinstance(name, str) else " ".join(name)
                for name in renpy.list_images()
                if name and not (name if isinstance(name, str) else name[0]).startswith("_")))
        return _sw_catalog_cache["images"]

    def _sw_character_name(character, values=None):
        name = character.name
        if character.dynamic:
            if not isinstance(name, str) or name not in _SW_NAME_DEFAULTS:
                raise SWPreviewBoundary("This speaker's dynamic name needs a preview adapter.")
            name = (values or {}).get(name, _SW_NAME_DEFAULTS[name])
        return name

    def sw_catalog_speakers():
        if "speakers" not in _sw_catalog_cache:
            found = [("", "Narration")]
            for alias, character in sorted(vars(renpy.store).items()):
                if alias.startswith("_") or alias in ("narrator", "adv", "nvl", "nvl_narrator"):
                    continue
                if not isinstance(character, renpy.character.ADVCharacter):
                    continue
                try:
                    display = _sw_character_name(character) or ("Nier prose" if alias == "nier" else alias)
                except SWPreviewBoundary:
                    continue
                found.append((alias, str(display)))
            _sw_catalog_cache["speakers"] = tuple(found)
        return _sw_catalog_cache["speakers"]

    def sw_catalog_music():
        if "music" not in _sw_catalog_cache:
            found = []
            for alias, path in sorted(vars(renpy.store.audio).items()):
                if alias.startswith("_") or not isinstance(path, str):
                    continue
                if path.lower().endswith((".ogg", ".mp3", ".wav", ".opus", ".flac")):
                    found.append((alias, path))
            _sw_catalog_cache["music"] = tuple(found)
        return _sw_catalog_cache["music"]

    def _sw_number(node):
        if isinstance(node, _sw_ast.Constant) and type(node.value) in (int, float):
            value = node.value
        elif isinstance(node, _sw_ast.UnaryOp) and isinstance(node.op, (_sw_ast.USub, _sw_ast.UAdd)):
            value = _sw_number(node.operand) * (-1 if isinstance(node.op, _sw_ast.USub) else 1)
        else:
            raise SWPreviewBoundary("Preview arguments must be literal numbers.")
        if not _sw_math.isfinite(value) or abs(value) > 1000000:
            raise SWPreviewBoundary("Preview argument is outside the supported numeric range.")
        return value

    def _sw_resolve_node(node, signatures):
        if isinstance(node, _sw_ast.Constant) and node.value is None and signatures is _SW_TRANSITION_SIGNATURES:
            return None
        call = isinstance(node, _sw_ast.Call)
        name_node = node.func if call else node
        if not isinstance(name_node, _sw_ast.Name) or name_node.id not in signatures:
            raise SWPreviewBoundary("Choose a supported named motion or transition preset.")
        name = name_node.id
        value = getattr(renpy.store, name, None)
        if value is None:
            raise SWPreviewBoundary("Preset '%s' is not defined in this game." % name)
        required_transition = signatures is _SW_TRANSITION_SIGNATURES and name in ("Dissolve", "Fade", "Pixellate")
        if not call:
            if required_transition:
                raise SWPreviewBoundary("%s needs its duration arguments, for example Dissolve(0.4)." % name)
            return value
        parameters = signatures[name]
        if len(node.args) > len(parameters):
            raise SWPreviewBoundary("Too many arguments for '%s'." % name)
        positional = [_sw_number(arg) for arg in node.args]
        keywords = {}
        for keyword in node.keywords:
            if keyword.arg not in parameters or keyword.arg in parameters[:len(positional)] or keyword.arg in keywords:
                raise SWPreviewBoundary("Unsupported or duplicate argument for '%s'." % name)
            keywords[keyword.arg] = _sw_number(keyword.value)
        if required_transition:
            supplied = dict(zip(parameters, positional))
            supplied.update(keywords)
            if any(parameter not in supplied for parameter in parameters):
                raise SWPreviewBoundary("%s needs arguments: %s." % (name, ", ".join(parameters)))
            for parameter, numeric in supplied.items():
                if parameter == "steps":
                    if type(numeric) is not int or numeric < 1:
                        raise SWPreviewBoundary("Pixellate steps must be a positive integer.")
                elif numeric < 0 or (name == "Pixellate" and numeric == 0):
                    raise SWPreviewBoundary("Transition durations must be nonnegative; Pixellate needs positive time.")
        return value(*positional, **keywords)

    def sw_resolve_transforms(text):
        if not text or not text.strip():
            return []
        try:
            node = _sw_ast.parse(text.strip(), mode="eval").body
        except SyntaxError:
            raise SWPreviewBoundary("Incomplete transform stack.")
        nodes = node.elts if isinstance(node, _sw_ast.Tuple) else [node]
        return [_sw_resolve_node(item, _SW_TRANSFORM_SIGNATURES) for item in nodes]

    def sw_resolve_transition(text):
        if not text or text.strip() == "None":
            return None
        try:
            node = _sw_ast.parse(text.strip(), mode="eval").body
        except SyntaxError:
            raise SWPreviewBoundary("Incomplete transition preset.")
        return _sw_resolve_node(node, _SW_TRANSITION_SIGNATURES)

    def sw_resolve_music(token):
        token = token.strip()
        if token.startswith(("'", '"')):
            try:
                path = _sw_ast.literal_eval(token)
            except (SyntaxError, ValueError):
                raise SWPreviewBoundary("Incomplete music filename.")
        else:
            alias = token[6:] if token.startswith("audio.") else token
            if not _sw_re.fullmatch(r"[A-Za-z_]\w*", alias):
                raise SWPreviewBoundary("Choose a music alias or a quoted audio filename.")
            path = dict(sw_catalog_music()).get(alias)
        if not isinstance(path, str) or not path or "<" in path or "[" in path:
            raise SWPreviewBoundary("This music expression needs a preview adapter.")
        if not renpy.loadable(path):
            raise SWPreviewBoundary("Audio file is missing: %s" % path)
        return path

    def sw_audition(alias):
        if not config.developer:
            return
        # enqueue() marks audio seen synchronously. Keep audition from unlocking
        # the track in the player's Music Room while leaving its queue independent.
        seen = dict(persistent._seen_audio)
        try:
            path = sw_resolve_music(alias)
            for channel in _sw_native_audio_channels():
                if channel not in _sw_audition_paused and renpy.music.get_playing(channel=channel):
                    # Replacing the audition track must retain the original
                    # pause flag, rather than snapshotting our own pause again.
                    _sw_audition_paused[channel] = renpy.music.get_pause(channel=channel)
                    renpy.music.set_pause(True, channel=channel)
            renpy.music.play(path, channel="sw_writer_audition", loop=False, fadeout=0.15)
        except Exception:
            sw_stop_audition()
            raise
        finally:
            persistent._seen_audio.clear()
            persistent._seen_audio.update(seen)

    def sw_stop_audition():
        global _sw_audition_paused
        paused = _sw_audition_paused
        _sw_audition_paused = {}
        try:
            # Stop before resuming the original tracks so the final fraction of
            # an audition does not mix over the restored music.
            renpy.music.stop(channel="sw_writer_audition", fadeout=0)
        finally:
            for channel, value in paused.items():
                renpy.music.set_pause(value, channel=channel)

    def _sw_ignorable(block):
        return block.kind == "raw" and all(not line.strip() or line.lstrip().startswith("#") for line in block.raw.splitlines())

    def _sw_plain_return(block):
        if block.kind != "raw":
            return False
        lines = [line.strip() for line in block.raw.splitlines() if line.strip() and not line.lstrip().startswith("#")]
        return len(lines) == 1 and _sw_re.fullmatch(r"return\s*(?:#.*)?", lines[0]) is not None

    def _sw_raw_adapters(block):
        """Recognize complete curated presentation statements, never execute AST.

        Raw spans may group several physical lines. Every non-comment line must
        match an adapter before any of it can run; mixed story logic stays opaque.
        """
        if block.kind != "raw":
            return None
        operations = []
        for line in block.raw.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if not line.startswith("$"):
                return None
            try:
                statements = _sw_ast.parse(line[1:].strip(), mode="exec").body
                if len(statements) != 1:
                    return None
                statement = statements[0]
                if isinstance(statement, _sw_ast.Assign):
                    if len(statement.targets) != 1 or not isinstance(statement.targets[0], _sw_ast.Name):
                        return None
                    name = statement.targets[0].id
                    if name not in _SW_NAME_DEFAULTS or not isinstance(statement.value, _sw_ast.Constant) or not isinstance(statement.value.value, str):
                        return None
                    operations.append(("name", {"name": name, "value": statement.value.value}))
                    continue
                if not isinstance(statement, _sw_ast.Expr) or not isinstance(statement.value, _sw_ast.Call):
                    return None
                call = statement.value
                if not isinstance(call.func, _sw_ast.Name):
                    return None
                name = call.func.id
                signature = {
                    "show_calendar": (), "hide_calendar": (),
                    "atmos": ("preset", "particles", "zorder", "secs"),
                    "atmos_clear": (), "atmos_hold": (),
                    "atmos_pressure": ("zorder",), "atmos_pressure_clear": (),
                }.get(name)
                if signature is None or len(call.args) > len(signature):
                    return None
                kwargs = {}
                pairs = list(zip(signature, call.args))
                pairs.extend((kw.arg, kw.value) for kw in call.keywords)
                for key, node in pairs:
                    if key not in signature or key in kwargs:
                        return None
                    if isinstance(node, _sw_ast.Constant) and (node.value is None or type(node.value) in (str, bool, int, float)):
                        value = node.value
                    else:
                        value = _sw_number(node)
                    kwargs[key] = value
                if name == "atmos":
                    if not isinstance(kwargs.get("preset"), str) or kwargs["preset"] not in renpy.store.ATMOS_PRESETS:
                        return None
                    if kwargs.get("particles") not in (None,) + tuple(renpy.store._ATMOS_PARTICLE_VALUES):
                        return None
                if "zorder" in kwargs and (type(kwargs["zorder"]) is not int or abs(kwargs["zorder"]) > 1000000):
                    return None
                if "secs" in kwargs and (type(kwargs["secs"]) not in (int, float) or not 0 <= kwargs["secs"] <= 3600):
                    return None
                operations.append((name, kwargs))
            except (SyntaxError, ValueError, SWPreviewBoundary):
                return None
        return operations

    def sw_preview_plan(document, uid):
        """Follow only known ancestry; never pick a route by evaluating code."""
        blocks = document.blocks
        selected = next((i for i, block in enumerate(blocks) if block.uid == uid), 0)
        if not blocks:
            return {"blocks": [], "warning": "This document is empty.", "start_uid": None, "requires_setup": False}
        branch = tuple(blocks[selected].branch)
        compatible = lambda block: tuple(block.branch) == branch[:len(block.branch)]
        start = None
        boundary = ""
        for i, block in enumerate(blocks[:selected + 1]):
            if not compatible(block):
                continue
            if block.kind in ("label", "branch"):
                if block.uid not in branch:
                    start = None
                continue
            if block.kind == "raw" and _sw_raw_adapters(block) is None:
                start = None
                boundary = "Earlier preserved logic has unknown effects."
            elif block.kind in ("scene", "nier_enter"):
                start = i
                boundary = ""
        requires_setup = start is None
        if start is None:
            start = selected
            boundary = (boundary + " Start here with an empty stage and preview names.").strip()
        result = []
        end_warning = ""
        for block in blocks[start:]:
            if not compatible(block):
                if result:
                    end_warning = "Preview ends at the next branch boundary."
                    break
                continue
            if block.kind in ("label", "branch"):
                if block.uid in branch:
                    continue
                end_warning = "Preview ends at the next label or branch."
                break
            if _sw_ignorable(block):
                continue
            if _sw_plain_return(block):
                break
            if block.kind == "raw" and _sw_raw_adapters(block) is None:
                end_warning = "Preview stops before preserved logic at line %s." % block.line
                break
            result.append(block)
        if any(op == "show_calendar" for block in result if block.kind == "raw" for op, args in (_sw_raw_adapters(block) or [])):
            end_warning += " Calendar date is unresolved; the badge is marked PREVIEW."
        return {"blocks": result, "warning": " ".join(filter(None, (boundary, end_warning))),
                "start_uid": blocks[start].uid, "requires_setup": requires_setup}

    def _sw_layer(data):
        layer = data.get("layer") or "master"
        if layer not in ("master", "foreground", "background") or layer not in config.layers:
            raise SWPreviewBoundary("Preview supports configured scene layers only: %s." % layer)
        return layer

    def _sw_image(data, info):
        name = tuple(data.get("image", "").split())
        if not name:
            return None
        if any(not _sw_re.fullmatch(r"-?[A-Za-z0-9_]+", part) for part in name):
            raise SWPreviewBoundary("Image expression is outside the supported image-name syntax.")
        tag = data.get("tag") or name[0]
        resolved = info.apply_attributes(_sw_layer(data), tag, name)
        if resolved is None:
            raise SWPreviewBoundary("Image or attributes not found: %s" % " ".join(name))
        return resolved

    def sw_stage_state(blocks, uid=None):
        """Cheap, side-effect-free composition using a private attribute tracker."""
        info = renpy.display.image.ShownImageInfo()
        shown = {}
        speaker = text = warning = ""
        values = dict(_SW_NAME_DEFAULTS)
        atmosphere = None
        calendar_visible = False
        for block in blocks:
            data = block.data
            try:
                if block.kind in ("scene", "show"):
                    layer = _sw_layer(data)
                    if block.kind == "scene":
                        info.predict_scene(layer)
                        shown = {key: value for key, value in shown.items() if key[0] != layer}
                    name = _sw_image(data, info)
                    if name:
                        tag = data.get("tag") or name[0]
                        key = (layer, tag)
                        previous = shown.get(key, {})
                        info.predict_show(layer, (tag,) + name[1:])
                        shown[key] = {"name": " ".join(name), "tag": tag, "layer": layer,
                                      "at": data.get("at") or previous.get("at", ""),
                                      "atl": data.get("atl") or ("" if data.get("at") else previous.get("atl", "")),
                                      "zorder": int(data.get("zorder") or previous.get("zorder", 0))}
                elif block.kind == "hide":
                    layer = _sw_layer(data)
                    name = tuple(data.get("image", "").split())
                    if name:
                        info.predict_hide(layer, name)
                        shown.pop((layer, name[0]), None)
                elif block.kind == "say":
                    speaker, text = data.get("speaker", ""), data.get("text", "")
                    who = getattr(renpy.store, speaker or "narrator", None)
                    tag = getattr(who, "image_tag", None)
                    attrs = data.get("attributes", "")
                    if tag and attrs:
                        name = _sw_image({"image": tag + " " + attrs}, info)
                        info.predict_show("master", name, show=False)
                        if ("master", tag) in shown:
                            shown[("master", tag)]["name"] = " ".join(name)
                elif block.kind in ("nier_enter", "nier_exit"):
                    shown.clear()
                    info.predict_scene("master")
                    shown[("master", "black")] = {"name": "black", "tag": "black", "layer": "master", "at": "", "atl": "", "zorder": 0}
                elif block.kind == "raw":
                    operations = _sw_raw_adapters(block)
                    if operations is None:
                        warning = "Composition stops at preserved logic."
                        break
                    for operation, args in operations:
                        if operation == "name":
                            values[args["name"]] = args["value"]
                        elif operation == "atmos":
                            atmosphere = dict(args)
                        elif operation == "atmos_clear":
                            atmosphere = None
                        elif operation in ("show_calendar", "hide_calendar"):
                            calendar_visible = operation == "show_calendar"
            except Exception as exc:
                warning = str(exc)
                break
            if uid is not None and block.uid == uid:
                break
        return {"images": sorted(shown.values(), key=lambda item: item["zorder"]),
                "speaker": speaker, "text": text, "warning": warning,
                "values": values, "atmosphere": atmosphere, "calendar_visible": calendar_visible}

    def _sw_float(text, default=0.0, minimum=0.0, maximum=3600.0):
        if text in (None, ""):
            return default
        try:
            value = float(text)
        except (TypeError, ValueError):
            raise SWPreviewBoundary("Expected a literal number.")
        if not _sw_math.isfinite(value) or not minimum <= value <= maximum:
            raise SWPreviewBoundary("Number is outside the supported preview range.")
        return value

    class _SWInlineMotion(object):
        """Typed property keyframes; no ATL parsing or Python expression evaluation."""
        def __init__(self, text):
            self.steps = []
            for line in text.splitlines():
                words = line.strip().split()
                if not words or words[0].startswith("#"):
                    continue
                easing, duration = "set", 0.0
                if words[0] in ("linear", "ease", "easein", "easeout", "easein_quad", "easeout_quad", "easein_cubic", "easeout_cubic"):
                    easing = words.pop(0)
                    if not words:
                        raise SWPreviewBoundary("Motion needs a duration.")
                    duration = _sw_float(words.pop(0))
                if len(words) % 2:
                    raise SWPreviewBoundary("Motion properties need numeric values.")
                props = {}
                for prop, token in zip(words[::2], words[1::2]):
                    if prop not in ("alpha", "xoffset", "yoffset", "zoom", "xzoom", "yzoom", "rotate"):
                        raise SWPreviewBoundary("Inline ATL property '%s' needs an adapter." % prop)
                    bounds = (0.0, 1.0) if prop == "alpha" else (-100000.0, 100000.0)
                    props[prop] = _sw_float(token, minimum=bounds[0], maximum=bounds[1])
                self.steps.append((easing, duration, props))
            self.initial = None

        def __call__(self, trans, st, at):
            if self.initial is None:
                properties = {key for _, _, props in self.steps for key in props}
                self.initial = {key: getattr(trans, key) for key in properties}
            current = dict(self.initial)
            elapsed = 0.0
            running = False
            for easing, duration, target in self.steps:
                if easing == "set" or st >= elapsed + duration or duration == 0:
                    current.update(target)
                    elapsed += duration
                    continue
                portion = max(0.0, min(1.0, (st - elapsed) / duration))
                if easing == "ease":
                    portion = (1.0 - _sw_math.cos(portion * _sw_math.pi)) / 2.0
                elif easing == "easein":
                    portion = _sw_math.sin(portion * _sw_math.pi / 2.0)
                elif easing == "easeout":
                    portion = 1.0 - _sw_math.cos(portion * _sw_math.pi / 2.0)
                elif easing == "easein_quad":
                    portion = 1.0 - (1.0 - portion) ** 2
                elif easing == "easeout_quad":
                    portion = portion ** 2
                elif easing == "easein_cubic":
                    portion = 1.0 - (1.0 - portion) ** 3
                elif easing == "easeout_cubic":
                    portion = portion ** 3
                for key, value in target.items():
                    current[key] += (value - current[key]) * portion
                running = True
                break
            for key, value in current.items():
                setattr(trans, key, value)
            return 0 if running else None

    def sw_resolve_inline_motion(text):
        return Transform(function=_SWInlineMotion(text))

    def _sw_preview_text(text, values):
        # Ren'Py's substitution engine evaluates arbitrary bracket expressions.
        # Resolve only the known names and escape every remaining bracket before
        # the real Character receives the text. Never strip unknown expressions.
        result = []
        i = 0
        while i < len(text):
            if text.startswith("[[", i):
                result.append("[[")
                i += 2
            elif text[i] == "[":
                end = text.find("]", i + 1)
                key = text[i + 1:end] if end >= 0 else ""
                if key not in values:
                    raise SWPreviewBoundary("Unresolved preview value: [%s]." % key)
                result.append(str(values[key]).replace("[", "[[").replace("{", "{{"))
                i = end + 1
            else:
                result.append(text[i])
                i += 1
        safe = "".join(result)
        for tag in _sw_re.findall(r"(?<!\{)\{(/?[^{}]+)\}", safe):
            name = tag.lstrip("/").split("=", 1)[0]
            if name not in ("b", "i", "u", "s", "plain", "color", "alpha", "size", "font", "outlinecolor", "k", "rt", "rb", "art", "vspace", "space", "cps", "w", "p", "nw", "fast", "done", "noalt", "alt", "clear"):
                raise SWPreviewBoundary("Text tag '%s' needs a preview adapter." % name)
        return safe

    def _sw_preview_say(data, values):
        alias = data.get("speaker") or "narrator"
        if alias not in {item[0] or "narrator" for item in sw_catalog_speakers()}:
            raise SWPreviewBoundary("Speaker '%s' is not a supported Character." % alias)
        character = getattr(renpy.store, alias)
        name = _sw_character_name(character, values)
        if name is not None:
            name = str(name).replace("[", "[[")
        # Retain the real NVL/ADV type, quotes, namebox and textbox styles while
        # excluding custom speaker callbacks, conditions and dynamic expressions.
        preview_character = Character(name, kind=character, dynamic=False, condition=None, callback=[])
        renpy.game.context().say_attributes = tuple(data.get("attributes", "").split()) or None
        renpy.say(preview_character, _sw_preview_text(data.get("text", ""), values))

    def _sw_preview_block(block, values):
        kind, data = block.kind, block.data
        if kind in ("scene", "show"):
            layer = _sw_layer(data)
            if kind == "scene":
                renpy.scene(layer=layer)
            image = _sw_image(data, renpy.game.context().images)
            if image:
                transforms = sw_resolve_transforms(data.get("at", ""))
                if data.get("atl"):
                    if not transforms:
                        tag = data.get("tag") or image[0]
                        transforms = list(renpy.get_at_list(tag, layer=layer) or [])
                        if not transforms and tag in config.tag_transform:
                            inherited = config.tag_transform[tag]
                            transforms = list(inherited) if isinstance(inherited, (list, tuple)) else [inherited]
                    transforms.append(sw_resolve_inline_motion(data["atl"]))
                # Use the same presentation seam as a real `show` statement,
                # including main-story cast framing before the first say.
                config.show(image, layer=layer, tag=data.get("tag") or None,
                           at_list=transforms, behind=data.get("behind", "").replace(",", " ").split(),
                           zorder=int(data["zorder"]) if data.get("zorder") not in (None, "") else None)
            if data.get("transition"):
                renpy.with_statement(sw_resolve_transition(data["transition"]))
        elif kind == "hide":
            renpy.hide(data.get("image", ""), layer=_sw_layer(data))
            if data.get("transition"):
                renpy.with_statement(sw_resolve_transition(data["transition"]))
        elif kind == "say":
            _sw_preview_say(data, values)
        elif kind == "pause":
            renpy.pause(_sw_float(data.get("duration")) if data.get("duration") else None)
        elif kind == "with":
            renpy.with_statement(sw_resolve_transition(data.get("transition", "")))
        elif kind == "music":
            logical_channel = data.get("channel", "music")
            if logical_channel not in _SW_PREVIEW_CHANNELS:
                raise SWPreviewBoundary("This audio channel needs a preview adapter.")
            channel = _SW_PREVIEW_CHANNELS[logical_channel]
            operation = data.get("operation", "play")
            if operation == "stop":
                renpy.music.stop(channel=channel, fadeout=_sw_float(data.get("fadeout")))
                return
            track = sw_resolve_music(data.get("track", ""))
            loop = data.get("loop", "default")
            kwargs = {"channel": channel, "loop": None if loop == "default" else loop == "loop",
                      "fadein": _sw_float(data.get("fadein")),
                      "relative_volume": _sw_float(data.get("volume"), default=1.0, maximum=1.0)}
            if operation == "play":
                renpy.music.play(track, fadeout=_sw_float(data.get("fadeout")), **kwargs)
            elif operation == "queue":
                renpy.music.queue(track, **kwargs)
            else:
                raise SWPreviewBoundary("Unsupported music operation.")
        elif kind in ("nier_enter", "nier_exit", "nier_clear"):
            if kind in ("nier_clear", "nier_exit"):
                renpy.store.nvl_clear()
            if kind == "nier_enter":
                renpy.store.nier_ta_prev_quick_menu = renpy.store.quick_menu
                renpy.store.nier_ta_active = True
                renpy.store.quick_menu = False
                renpy.scene()
                renpy.show("black")
                renpy.pause(0.8)
            elif kind == "nier_exit":
                renpy.store.nier_ta_active = False
                renpy.store.quick_menu = renpy.store.nier_ta_prev_quick_menu
                renpy.scene()
                renpy.show("black")
        elif kind == "raw" and _sw_raw_adapters(block) is not None:
            for operation, args in _sw_raw_adapters(block):
                if operation == "name":
                    values[args["name"]] = args["value"]
                    setattr(renpy.store, args["name"], args["value"])
                else:
                    # Function selection is the explicit allowlist above. All
                    # arguments are already typed literals, not executable AST.
                    getattr(renpy.store, operation)(**args)
        elif not _sw_ignorable(block):
            raise SWPreviewBoundary("Preview stopped at preserved %s content." % kind)

    class _SWPreviewCalendar(object):
        """The real calendar badge with an honest unresolved-date placeholder."""
        def __init__(self):
            self.display_enabled = False

        def show(self):
            self.display_enabled = True

        def hide(self):
            self.display_enabled = False

        def get_snapshot(self, date_value=None):
            return {"month_short": "DATE", "day_padded": "--", "dow_short": "PREVIEW", "is_weekend": False}

    def sw_cancel_preview():
        raise SWPreviewCancelled()

    def _sw_force_story_scope():
        renpy.store._stage_state["scope"] = True

    def _sw_native_audio_channels():
        # Default Channel.name values can themselves be legacy integers, even
        # though the same objects are available through "music"/"sound" aliases.
        # Prefer a string alias, retain unaliased legacy integers, and pause each
        # object only once. Private channels stay excluded through every alias.
        registry = renpy.audio.audio.channels
        entries = list(registry.items())
        private = set(id(channel) for name, channel in entries if isinstance(name, str) and name.startswith("sw_"))
        preferred = [(name, registry[name]) for name in ("music", "sound", "voice") if name in registry]
        aliases = preferred + [(name, channel) for name, channel in entries if isinstance(name, str)]
        aliases.extend((name, channel) for name, channel in entries if type(name) is int)
        result = []
        seen = set()
        for name, channel in aliases:
            if id(channel) in seen or id(channel) in private:
                continue
            seen.add(id(channel))
            result.append(name)
        return result

    def _sw_nvl_clear_ahead(blocks, start):
        # NVL's normal helper scries the executing AST, which a Python preview
        # context does not have. Read the supported cue stream instead, stopping
        # at the next interaction just as the native helper does.
        for block in blocks[start:start + 10]:
            if block.kind in ("nier_clear", "nier_exit"):
                return True
            if block.kind in ("say", "pause", "with", "nier_enter") or block.data.get("transition"):
                return False
        return False

    def _sw_preview_clear_next():
        return renpy.store._sw_preview_nvl_page

    def _sw_preview_body(blocks, values):
        dynamic = ("main_menu", "_game_menu_screen", "quick_menu", "_history_list", "_history", "_in_replay",
                   "_skipping", "_dismiss_pause", "_window", "_window_auto", "_window_subtitle", "_window_next",
                   "nier_ta_active", "nier_ta_prev_quick_menu", "nvl_list", "nvl_variant", "_nvl_language",
                   "_side_image_attributes", "_side_image_attributes_reset", "_last_say_who", "_last_say_what",
                   "_last_say_args", "_last_say_kwargs", "nvl_clear_next", "_sw_preview_nvl_page")
        for name in dynamic + tuple(_SW_NAME_DEFAULTS):
            renpy.context_dynamic(name)
        renpy.store.main_menu = False
        renpy.context()._main_menu = False
        renpy.store.quick_menu = False
        renpy.store._game_menu_screen = None
        renpy.store._history_list = []
        renpy.store._history = False
        renpy.store._in_replay = "sw_writer_preview"
        renpy.store._skipping = False
        renpy.store._window = False
        renpy.store._window_auto = True
        renpy.store.nvl_list = None
        renpy.store.nier_ta_active = False
        renpy.store.nvl_clear_next = _sw_preview_clear_next
        for name, value in values.items():
            setattr(renpy.store, name, value)
        renpy.scene()
        renpy.show("black")
        renpy.show_screen("sw_reading_controls")
        for index, block in enumerate(blocks):
            renpy.store._sw_preview_nvl_page = _sw_nvl_clear_ahead(blocks, index + 1)
            _sw_preview_block(block, values)
        # Let the final staging/music cue actually render before returning.
        renpy.show_screen("sw_preview_finished")
        renpy.pause()

    def sw_play_preview(blocks, values=None, on_finish=None):
        """Synchronous reading session; returns status after unconditional cleanup."""
        global _sw_preview_active
        if not config.developer or _sw_preview_active:
            return {"status": "unavailable", "message": "Story Writer preview requires developer mode."}
        values = {key: (values or {}).get(key, fallback) for key, fallback in _SW_NAME_DEFAULTS.items()}
        # Replace init-time mutable caches, preserving the exact old objects.
        mutable_names = ("_stage_state", "_stage_panels", "_autofocus_slot_cache", "_autofocus_grade_state",
                         "_autofocus_grade_cur", "_autofocus_grade_last_st", "_autofocus_active_speakers",
                         "_autofocus_lookup", "_autofocus_loc_lookup", "_autofocus_force_reapply", "_atmos_state", "calendar")
        saved_store = {name: getattr(renpy.store, name) for name in mutable_names if hasattr(renpy.store, name)}
        config_names = ("start_interact_callbacks", "interact_callbacks", "all_character_callbacks",
                        "character_callback", "say_arguments_callback", "overlay_screens", "always_shown_screens",
                        "overlay_functions", "no_replay_seen", "allow_skipping", "skipping")
        saved_config = {name: getattr(config, name) for name in config_names}
        seen = {name: _sw_copy.copy(getattr(persistent, name)) for name in ("_seen_images", "_seen_audio")}
        saved_scope_update = renpy.store._stage_panels_scope_update
        paused = {}
        result = {"status": "complete", "message": "Preview finished."}
        try:
            _sw_preview_active = True
            sw_stop_audition()
            for name, value in saved_store.items():
                setattr(renpy.store, name, _sw_copy.deepcopy(value))
            renpy.store._stage_panels = []
            renpy.store._stage_state.update(scope=True, suspend=0, amt=0.0, amt_target=0.0,
                speaker=None, frame=None, snap=True, signature=None, zoomv=1.0, zoom_target=1.0, narrowv=1.0, narrow_target=1.0)
            for name in mutable_names:
                if name.startswith("_autofocus_") and isinstance(getattr(renpy.store, name, None), dict):
                    getattr(renpy.store, name).clear()
            renpy.store._atmos_state = renpy.store._atmos_default_state()
            renpy.store.calendar = _SWPreviewCalendar()
            renpy.store._stage_panels_scope_update = _sw_force_story_scope
            config.start_interact_callbacks = [renpy.store._stage_panels_interact]
            config.interact_callbacks = []
            config.all_character_callbacks = [renpy.store._stage_panels_speaker, renpy.store.autofocus_focus_speaker]
            config.character_callback = None
            config.say_arguments_callback = None
            config.overlay_screens = []
            config.always_shown_screens = []
            config.overlay_functions = []
            config.no_replay_seen = True
            config.allow_skipping = False
            config.skipping = None
            # Dedicated preview channels preserve every original queue, loop and
            # playback position; only their pause flags change during this call.
            for channel in _sw_native_audio_channels():
                if renpy.music.get_playing(channel=channel):
                    paused[channel] = renpy.music.get_pause(channel=channel)
                    renpy.music.set_pause(True, channel=channel)
            renpy.invoke_in_new_context(_sw_preview_body, blocks, values, _clear_layers=True)
        except SWPreviewCancelled:
            result = {"status": "cancelled", "message": "Returned to Story Writer."}
        except renpy.game.CONTROL_EXCEPTIONS:
            raise
        except Exception as exc:
            trace = _sw_traceback.format_exc()
            result = {"status": "boundary" if isinstance(exc, SWPreviewBoundary) else "error", "message": str(exc), "traceback": trace}
            renpy.write_log("Story Writer preview: " + trace)
        finally:
            for channel in _SW_PREVIEW_CHANNELS.values():
                renpy.music.stop(channel=channel, fadeout=0)
            for channel, value in paused.items():
                renpy.music.set_pause(value, channel=channel)
            for name, value in saved_store.items():
                setattr(renpy.store, name, value)
            renpy.store._stage_panels_scope_update = saved_scope_update
            for name, value in saved_config.items():
                setattr(config, name, value)
            for name, value in seen.items():
                current = getattr(persistent, name)
                current.clear()
                current.update(value)
            _sw_preview_active = False
        if on_finish is not None:
            on_finish(result)
        return result

    if config.developer:
        renpy.music.register_channel("sw_writer_audition", mixer="music", loop=False)
        for _sw_logical, _sw_channel in _SW_PREVIEW_CHANNELS.items():
            renpy.music.register_channel(_sw_channel, mixer="music" if _sw_logical == "music" else ("voice" if _sw_logical == "voice" else "sfx"), loop=_sw_logical == "music")

screen sw_reading_controls():
    zorder 10000
    key "game_menu" action Function(sw_cancel_preview)
    key ["rollback", "rollforward", "skip", "toggle_skip", "fast_skip", "toggle_afm", "hide_windows", "reload_game", "developer", "console", "bubble_editor"] action NullAction()
    frame:
        background "#10151de6"
        xalign 0.0
        # Nier prose occupies y=36..684. Keep its controls in the remaining
        # bottom margin so the first line and a full accumulated page stay clear.
        yalign (1.0 if nier_ta_active else 0.0)
        xfill nier_ta_active
        ysize (36 if nier_ta_active else 56)
        padding (12, 2)
        hbox:
            spacing 20
            yalign 0.5
            text "STORY PREVIEW" size 14 color "#a9b6c6" yalign 0.5
            textbutton "Return to Writer  (Esc)" text_size 16 padding (6, 0) ysize 32 action Function(sw_cancel_preview)

screen sw_preview_finished():
    zorder 9999
    frame:
        background "#10151de6"
        align (0.5, 0.08)
        padding (24, 14)
        text "End of this preview. Click to return to writing." size 20 color "#ffffff"
