# Full candidate syntax validation, with no source execution or AST installation.
# Resource checks apply only to changed/new supported statements; untouched legacy
# material remains byte-preserved and does not acquire new authoring restrictions.

init 25 python:
    import collections as _sw_collections
    import builtins as _sw_builtins

    def _sw_owned_pyexprs(parsed):
        """Expressions retained by the returned syntax tree, not lexer probes.

        Script.all_pyexpr is a compilation-cache hint: normal parsing also puts
        abandoned speculative expressions there. Ren'Py deliberately ignores
        failures compiling that registry (script.update_bytecode). Walk only the
        parsed tree's data fields, including C-slot annotations, without visiting
        methods, lexer objects, configured callbacks or live store/module state.
        """
        pending = [parsed]
        visited = set()
        expressions = []
        owned_modules = ("renpy.ast", "renpy.atl", "renpy.parameter", "renpy.sl2.")
        while pending:
            value = pending.pop()
            identity = id(value)
            if identity in visited:
                continue
            visited.add(identity)
            if isinstance(value, renpy.ast.PyExpr):
                expressions.append(value)
                continue
            if isinstance(value, renpy.ast.PyCode):
                # A one-line `$ assignment` may retain a PyExpr as its source,
                # but its required mode is exec/hide, not eval. The separate
                # PyCode pass below compiles it using its actual engine mode.
                continue
            # Store globals replace these names with Revertable subclasses;
            # parser containers are native Python and must be recognized too.
            if isinstance(value, _sw_builtins.dict):
                pending.extend(value.keys())
                pending.extend(value.values())
                continue
            if isinstance(value, (_sw_builtins.list, _sw_builtins.tuple,
                                  _sw_builtins.set, _sw_builtins.frozenset)):
                pending.extend(value)
                continue
            if isinstance(value, (str, bytes, int, float, bool, type(None), type)):
                continue
            value_type = type(value)
            if not value_type.__module__.startswith(owned_modules):
                continue
            fields = dict(getattr(value, "__dict__", {}))
            # This fork's C-slot optimization can remove both __dict__ entries
            # and Python slot/annotation metadata. Its public syntax fields still
            # exist, so enumerate those explicitly before the generic fallback.
            syntax_fields = ("imspec", "at_list", "atl", "expr", "paired", "with_", "condition",
                "entries", "arguments", "item_arguments", "parameters", "items", "set", "target",
                "label", "who", "index", "code", "block", "code_block", "subparses", "screen",
                "parsed", "value", "expression", "default", "statements", "duration", "properties",
                "expressions", "splines", "circles", "warp_function", "children", "transition",
                "repeats", "blocks", "choices", "time", "handlers")
            for name in syntax_fields:
                if name in fields:
                    continue
                try:
                    fields[name] = getattr(value, name)
                except AttributeError:
                    pass
            for base in value_type.__mro__:
                names = list(getattr(base, "__annotations__", {}))
                slots = getattr(base, "__slots__", ())
                names.extend((slots,) if isinstance(slots, str) else slots)
                for name in names:
                    if name in ("__dict__", "__weakref__") or name in fields:
                        continue
                    try:
                        fields[name] = getattr(value, name)
                    except AttributeError:
                        pass
            pending.extend(fields.values())
        return expressions

    def _sw_validate_image_name(name, info, layer="master", tag=None):
        parts = tuple(name.split())
        if not parts:
            raise ValueError("Choose an image.")
        image_tag = parts[0]
        registry = renpy.display.image.image_attributes.get(image_tag)
        if not registry:
            raise ValueError("Image tag '%s' is not defined." % image_tag)
        resolved = None
        try:
            resolved = info.apply_attributes(layer, tag or image_tag, parts)
        except Exception:
            # This statement may inherit a pose from a calling scene, beyond the
            # source's statically known branch. Check compatible rigs below.
            pass
        if resolved is None:
            attrs = renpy.check_image_attributes(image_tag, parts[1:])
            if attrs is not None:
                resolved = (image_tag,) + attrs
        if resolved is None:
            # An omitted pose/outfit is valid when inherited. Test each registered
            # rig prefix without inventing one for actual story playback.
            for prefix in registry:
                combined = prefix + tuple(attr for attr in parts[1:] if attr not in prefix)
                attrs = renpy.check_image_attributes(image_tag, combined)
                if attrs is not None:
                    resolved = (image_tag,) + attrs
                    break
        if resolved is None:
            raise ValueError("Image attributes are unknown or incompatible: %s." % name)
        # Inspect concrete static images only. Do not invoke DynamicDisplayable,
        # ATL, ConditionSwitch or arbitrary displayable callbacks while saving.
        for prefix, displayable in registry.items():
            if all(attr in resolved[1:] for attr in prefix) and isinstance(displayable, renpy.display.im.Image):
                filename = displayable.filename
                if isinstance(filename, str) and "[" not in filename and not renpy.loadable(filename):
                    raise ValueError("Image file is missing: %s." % filename)
        return resolved

    def _sw_validate_changed_resources(document, baseline):
        old = _SWDocument.from_bytes(baseline) if baseline is not None else None
        retained = _sw_collections.Counter(block.raw for block in old.blocks) if old is not None else _sw_collections.Counter()
        states = {(): renpy.display.image.ShownImageInfo()}
        for block in document.blocks:
            changed = not retained[block.raw]
            if retained[block.raw]:
                retained[block.raw] -= 1
            branch = tuple(block.branch)
            if branch not in states:
                ancestor = branch[:-1]
                while ancestor not in states:
                    ancestor = ancestor[:-1]
                states[branch] = renpy.display.image.ShownImageInfo(states[ancestor])
            info = states[branch]
            data = block.data
            kind = block.kind
            layer = data.get("layer") or "master"
            try:
                if kind in ("show", "scene"):
                    if kind == "scene":
                        info.predict_scene(layer)
                    if changed:
                        if layer not in config.layers or layer in ("screens", "overlay", "transient"):
                            raise ValueError("Choose a configured scene layer, such as master.")
                        resolved = _sw_validate_image_name(data.get("image", ""), info, layer, data.get("tag") or None)
                        sw_resolve_transforms(data.get("at", ""))
                        if data.get("transition"):
                            sw_resolve_transition(data["transition"])
                        if data.get("atl"):
                            _SWInlineMotion(data["atl"])
                    else:
                        try:
                            resolved = info.apply_attributes(layer, data.get("tag") or data["image"].split()[0], tuple(data["image"].split()))
                        except Exception:
                            resolved = None
                    if resolved:
                        info.predict_show(layer, (data.get("tag") or resolved[0],) + resolved[1:])
                elif kind == "hide":
                    if changed:
                        if layer not in config.layers or layer in ("screens", "overlay", "transient"):
                            raise ValueError("Choose a configured scene layer.")
                        # Hides can use an alias established by `show ... as`.
                        tag = data.get("image", "").split()[0]
                        if not info.showing(layer, (tag,)) and tag not in renpy.display.image.image_attributes:
                            raise ValueError("Hide tag '%s' is not a known image or shown alias." % tag)
                        if data.get("transition"):
                            sw_resolve_transition(data["transition"])
                    info.predict_hide(layer, tuple(data.get("image", "").split()))
                elif kind == "say":
                    alias = data.get("speaker") or "narrator"
                    character = getattr(renpy.store, alias, None)
                    if changed:
                        if not isinstance(character, renpy.character.ADVCharacter):
                            raise ValueError("Speaker '%s' is not a registered Character." % alias)
                        problem = renpy.check_text_tags(data.get("text", ""), check_unclosed=True)
                        if problem:
                            raise ValueError(problem)
                    tag = getattr(character, "image_tag", None)
                    attrs = data.get("attributes", "")
                    if attrs:
                        if changed and not tag:
                            raise ValueError("This speaker has no image tag for attached attributes.")
                        if tag:
                            if changed:
                                resolved = _sw_validate_image_name(tag + " " + attrs, info)
                            else:
                                try:
                                    resolved = info.apply_attributes("master", tag, tuple((tag + " " + attrs).split()))
                                except Exception:
                                    resolved = None
                            if resolved:
                                info.predict_show("master", resolved, show=False)
                elif changed and kind == "with":
                    sw_resolve_transition(data.get("transition", ""))
                elif changed and kind == "music" and data.get("operation") != "stop":
                    sw_resolve_music(data.get("track", ""))
                elif kind == "raw" and _sw_raw_adapters(block) is None and not _sw_ignorable(block):
                    # Unknown logic may change attributes; do not treat an earlier
                    # expression/outfit as guaranteed after this boundary.
                    states[branch] = renpy.display.image.ShownImageInfo()
            except Exception as exc:
                if changed and block.editable:
                    raise ValueError("Line %s: %s" % (block.line, exc))

    def _sw_validate_labels(document, destination):
        names = [block.data["name"] for block in document.blocks if block.kind == "label"]
        if len(names) != len(set(names)):
            raise ValueError("A label is defined more than once in this source.")
        normalize = lambda path: _sw_os.path.normcase(_sw_os.path.realpath(path))
        target = normalize(destination)
        for name in names:
            if not renpy.has_label(name):
                continue
            node = renpy.game.script.lookup(name)
            options = (normalize(_sw_os.path.join(config.basedir, node.filename)),
                       normalize(_sw_os.path.join(config.gamedir, node.filename)))
            if target not in options:
                raise ValueError("Label '%s' already belongs to another file." % name)
        wanted = set(names)
        # Newly saved sources are not in the live label registry until reload.
        # Inspect source declarations as well, so two new scenes cannot acquire
        # the same label during one writing session.
        for folder, dirs, files in _sw_os.walk(_sw_os.path.join(config.gamedir, "story")):
            for filename in files:
                if not filename.endswith(".rpy"):
                    continue
                path = _sw_os.path.join(folder, filename)
                if normalize(path) == target:
                    continue
                other = _SWDocument.load(path)
                for block in other.blocks:
                    if block.kind == "label" and block.data["name"] in wanted:
                        raise ValueError("Label '%s' already exists in %s." % (block.data["name"], _sw_os.path.relpath(path, config.gamedir)))

    def sw_validate_source(candidate, destination, baseline=None):
        """Validate full script and changed resources; restore all compiler state."""
        if not config.developer:
            raise ValueError("Story writing is available in developer mode.")
        document = _SWDocument.from_bytes(candidate, destination)
        script = renpy.game.script
        saved_script = {key: getattr(script, key) for key in ("all_pycode", "all_pyexpr", "record_pycode", "bytecode_newcache", "bytecode_dirty")}
        saved_parser = {key: getattr(renpy.parser, key) for key in ("parse_errors", "deferred_parse_errors", "translate_none_files")}
        saved_warnings = renpy.python.compile_warnings
        saved_compile_cache = renpy.python.py_compile_cache
        saved_exception_info = renpy.game.exception_info
        saved_lexer_filename = getattr(renpy.lexer, "original_filename", None)
        try:
            script.all_pycode = []
            script.all_pyexpr = []
            script.record_pycode = True
            script.bytecode_newcache = {}
            renpy.python.py_compile_cache = {}
            renpy.parser.parse_errors = []
            renpy.parser.deferred_parse_errors = _sw_collections.defaultdict(list)
            renpy.parser.translate_none_files = set()
            renpy.python.compile_warnings = []
            parsed = renpy.parser.parse(destination.replace("\\", "/"), filedata=candidate.decode("utf-8-sig"))
            renpy.parser.release_deferred_errors()
            if parsed is None or renpy.parser.parse_errors:
                raise ValueError(" ".join(str(error) for error in renpy.parser.parse_errors)[:900] or "The source could not be parsed.")
            # py_compile(cache=False) only creates Python code objects. It neither
            # executes source nor installs AST. This fork's immutable-literal
            # fast path still writes a None cache key even with cache=False, so
            # both destination cache dictionaries are private for this call.
            for expression in _sw_owned_pyexprs(parsed):
                _sw_builtins.compile(renpy.python.quote_eval(str(expression)),
                    getattr(expression, "filename", destination), "eval")
                renpy.python.py_compile(expression, "eval", cache=False)
            for pycode in tuple(script.all_pycode):
                renpy.python.py_compile(pycode.source, pycode.mode, filename=pycode.filename,
                    lineno=pycode.linenumber, py=pycode.py, hashcode=pycode.hashcode,
                    column=pycode.col_offset, cache=False)
            _sw_validate_labels(document, destination)
            _sw_validate_changed_resources(document, baseline)
            return True
        except Exception as exc:
            raise ValueError("Source was not saved: " + str(exc))
        finally:
            for key, value in saved_script.items():
                setattr(script, key, value)
            for key, value in saved_parser.items():
                setattr(renpy.parser, key, value)
            renpy.python.compile_warnings = saved_warnings
            renpy.python.py_compile_cache = saved_compile_cache
            renpy.game.exception_info = saved_exception_info
            if saved_lexer_filename is None:
                if hasattr(renpy.lexer, "original_filename"):
                    del renpy.lexer.original_filename
            else:
                renpy.lexer.original_filename = saved_lexer_filename
