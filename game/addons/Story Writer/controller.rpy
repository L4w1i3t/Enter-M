# Project-local authoring. Drafts and backups live outside game/.
init 10 python:
    import os as _sw_os
    import json as _sw_json
    import time as _sw_time
    import re as _sw_re
    import hashlib as _sw_hashlib
    from story_writer_model import StoryDocument as _SWDocument

    SW_INK = "#eee7db"
    SW_MUTED = "#a7aaa7"
    SW_ACCENT = "#a7d7c8"
    SW_TYPES = (("say", "Textbox"), ("scene", "Background"), ("show", "Sprite / image"),
        ("hide", "Hide image"), ("music", "Music cue"), ("with", "Transition"),
        ("pause", "Pause"), ("nier_enter", "Enter Nier"), ("nier_clear", "Nier page break"),
        ("nier_exit", "Leave Nier"))

    from collections import OrderedDict as _SWOrderedDict

    SW_FONT = "DejaVuSans.ttf"
    SW_FONT_BOLD = "DejaVuSans-Bold.ttf"
    SW_WARN = "#e8be88"
    SW_ERROR = "#f0a9a2"
    SW_KIND_WORDS = {"scene": "scene", "show": "show", "hide": "hide", "with": "with",
        "pause": "pause", "music": "music", "nier_enter": "nier", "nier_clear": "nier",
        "nier_exit": "nier"}
    SW_KIND_COLORS = {"say": SW_ACCENT, "scene": "#8fb3d9", "show": "#b9a3de", "hide": "#b9a3de",
        "with": "#9fb0a8", "pause": "#9fb0a8", "music": "#d9b77a", "nier": "#a9cf86",
        "label": "#e6dcc6", "branch": "#dba27f", "logic": "#7f8b90", "note": "#7f8b90"}
    # The insert palette; "…" marks entries that open a chooser first.
    SW_PALETTE = (("Prose", (("say", "Textbox"), ("pause", "Pause"))),
        ("Stage", (("scene", "Background…"), ("show", "Sprite…"), ("hide", "Hide"), ("with", "Transition"))),
        ("Music", (("play", "Play…"), ("queue", "Queue…"), ("stop", "Stop"))),
        ("Nier", (("nier_enter", "Enter"), ("nier_clear", "Page break"), ("nier_exit", "Leave"))))

    # Workspace geometry at 1280x720. Screens and controller share these numbers,
    # so editor widths and the virtual list window can never disagree.
    SW_LEFT_X, SW_LEFT_W = 20, 640
    SW_RIGHT_X, SW_RIGHT_W = 676, 584
    SW_FULL_W = 1240
    SW_ROW_H, SW_ROW_PITCH, SW_ROW_BUFFER = 30, 32, 8
    SW_LIST_Y, SW_LIST_H = 128, 256
    SW_DETAIL_Y, SW_DETAIL_H, SW_DETAIL_PAD = 396, 288, 14
    SW_PROSE_H = 168
    SW_STAGE_H = 328

    _sw_fit_cache = _SWOrderedDict()

    def sw_fit(value, width, size=15, font=None):
        """A one-line caption cut with an ellipsis at a measured pixel width."""
        value = " ".join(str(value).split())
        key = (value, int(width), size, font)
        cached = _sw_fit_cache.get(key)
        if cached is not None:
            _sw_fit_cache.move_to_end(key)
            return cached
        def measure(candidate):
            return Text(candidate.replace("{", "{{"), substitute=False, font=font or SW_FONT,
                size=size, layout="nobreak").size(32768, 2048)[0]
        fitted = value
        if value and measure(value) > width:
            low, high = 0, len(value)
            while low < high:
                middle = (low + high + 1) // 2
                if measure(value[:middle].rstrip() + "…") <= width:
                    low = middle
                else:
                    high = middle - 1
            fitted = value[:low].rstrip() + "…"
        fitted = sw_caption(fitted)
        _sw_fit_cache[key] = fitted
        if len(_sw_fit_cache) > 4096:
            _sw_fit_cache.popitem(last=False)
        return fitted

    def sw_caption(value):
        return str(value).replace("[", "[[").replace("{", "{{")

    def sw_short(value, length=78):
        value = " ".join(str(value).split())
        return value if len(value) <= length else value[:length - 1] + "…"

    def sw_source_path(relative):
        """Author only ordinary sources inside game/story, including new sources."""
        base = _sw_os.path.realpath(_sw_os.path.join(config.gamedir, "story"))
        relative = relative.replace("\\", "/")
        if relative.startswith("story/"):
            relative = relative[6:]
        target = _sw_os.path.realpath(_sw_os.path.join(base, relative))
        if _sw_os.path.commonpath((base, target)) != base or not target.lower().endswith(".rpy"):
            raise ValueError("Choose a .rpy file inside game/story.")
        return target

    def sw_sprite_load(name):
        """Point the Dev Hub sprite browser at an existing image's pose and choices."""
        parts = str(name or "").split()
        if not parts or not dev_hub_has("dev_sprite_select_tag"):
            return False
        tag, attributes = parts[0], parts[1:]
        if tag not in dev_sprite_tags(True):
            return False
        dev_sprite_select_tag(tag)
        look = dev_sprite_look(tag)
        if tuple(attributes) in look["variants"]:
            dev_sprite_set_variant(tuple(attributes))
            return True
        rigs = [(len(prefix), index) for index, (prefix, _rig) in enumerate(look["rigs"])
            if all(part in attributes for part in prefix)]
        if rigs:
            dev_sprite_select_rig(max(rigs)[1])
        rig = dev_sprite_current_rig()
        if rig is None:
            return False
        for group, names in rig["groups"]:
            for part in attributes:
                if part in names:
                    _dev_sprite.groups[group] = part
        _dev_sprite.free = set(part for part in attributes if part in rig["free"])
        return True

    class SWSession(object):
        # Class defaults keep lightweight sessions (tests build them with __new__) valid.
        tab = "stage"
        confirm = None
        music_target = None
        advanced = False
        disk_changed = False
        auditioning = False
        list_adjustment = None
        speakers = ()
        last_text_change = 0.0
        _speaker_names = None
        _rows = ()
        _rows_doc = None
        _rows_revision = -1
        _row_positions = None
        _rendered_rows = (0, 0)
        _stage_signature = None
        _last_draft_time = 0.0
        _disk_checked = 0.0
        _disk_stamp = None
        _label_edited = False
        _filter_cache = None
        _source_cache = None

        def __init__(self):
            self.doc = _SWDocument.new("writer_scene")
            self.selected = self.doc.blocks[0].uid
            self.fields = {}
            self.widgets = {}
            self._last_editor = None
            self._stage_dirty = True
            self.pending = False
            self.status = "Choose Open for an existing chapter, or New for a scene."
            self.error = False
            self.font_size = 24
            self.focus_mode = False
            self.tab = "stage"
            self.modal = None
            self.search = ""
            self.asset_mode = "backgrounds"
            self.asset_target = "insert"
            self.asset_name = "bg bedroom"
            self.new_path = "season1/writer_scene.rpy"
            self.new_label = "writer_scene"
            self.music_alias = "audio.day_c"
            self.stage_at = "t11"
            self.stage_transition = "dissolve"
            self.version = 0
            self.plan = {"blocks": [], "warning": "", "start_uid": None}
            self.stage = None
            self.stage_warning = ""
            self.auditioning = False
            self.list_adjustment = ui.adjustment(step=SW_ROW_PITCH * 3, changed=self._list_scrolled)
            self.file_catalog = []
            self.draft_catalog = []
            self.image_catalog = sw_catalog_images()
            self.music_catalog = sw_catalog_music()
            self.speakers = sw_catalog_speakers()
            self.draft_dir = _sw_os.path.join(config.basedir, "dev", "story_writer")
            self.draft_file = _sw_os.path.join(self.draft_dir, "recovery.json")
            self.last_draft = None
            self.last_text_change = 0.0
            self._load_fields()
            self.refresh_files()
            if _sw_os.path.isfile(self.draft_file):
                self.status = "A recovery draft is available. Open → Recover last draft."

        @property
        def block(self):
            return self.doc.get(self.selected)

        @property
        def dirty(self):
            return self.pending or self.doc.dirty

        @property
        def filename(self):
            path = getattr(self.doc, "path", "")
            if not path:
                return "New scene · not saved to story"
            return _sw_os.path.relpath(path, config.gamedir).replace("\\", "/")

        def report(self, message, error=False):
            self.status, self.error = str(message), error
            renpy.restart_interaction()

        def refresh_files(self):
            base = _sw_os.path.join(config.gamedir, "story")
            self.file_catalog = sorted(_sw_os.path.relpath(_sw_os.path.join(folder, name), base).replace("\\", "/")
                for folder, dirs, names in _sw_os.walk(base) for name in names
                if name.endswith(".rpy") and "sync-conflict" not in name)

        def blur(self):
            for widget in self.widgets.values():
                widget.set_focus(False)

        def _load_fields(self):
            self.blur()
            self.fields = dict(self.block.data)
            self.pending = False
            self.widgets.clear()
            self._last_editor = None
            self.rebuild_stage()

        def field_changed(self, key, text):
            self.fields[key] = text
            self._last_editor = self.widgets.get((self.selected, key))
            if key != "text":
                self._stage_dirty = True
            self.last_text_change = _sw_time.monotonic()
            if not self.pending:
                self.pending = True
                renpy.restart_interaction()

        def field(self, key, width=180, height=40, multiline=False):
            # Layout changes must not replace the active paragraph's undo/cursor.
            cache_key = (self.selected, key)
            if cache_key not in self.widgets:
                value = self.fields.get(key, "")
                if value is None:
                    value = ""
                self.widgets[cache_key] = SWTextEditor(str(value),
                    changed=lambda value, key=key: self.field_changed(key, value),
                    submit=self.next_textbox if key == "text" else self.apply,
                    width=width, height=height, font_size=self.font_size if multiline else 18,
                    multiline=multiline, placeholder="Write the next beat…" if key == "text" else "")
            widget = self.widgets[cache_key]
            widget.width, widget.height = width, height
            widget.set_font_size(self.font_size if multiline else 18)
            return widget

        def utility_field(self, key, width=300):
            cache_key = ("utility", key)
            if cache_key not in self.widgets:
                self.widgets[cache_key] = SWTextEditor(str(getattr(self, key)),
                    changed=lambda value, key=key: self.set_utility(key, value),
                    submit=lambda: None, width=width, height=40, font_size=18, multiline=False)
            self.widgets[cache_key].width = width
            return self.widgets[cache_key]

        def set_utility(self, key, value):
            setattr(self, key, value)
            if key == "search":
                self._filter_cache = None
            elif key == "new_label":
                self._label_edited = True
            elif key == "new_path" and not self._label_edited:
                # The label follows the filename until the author types their own.
                stem = _sw_re.sub(r"\W+", "_", _sw_os.path.splitext(_sw_os.path.basename(value))[0]).strip("_")
                if stem:
                    self.new_label = stem if _sw_re.match(r"[A-Za-z_]", stem) else "scene_" + stem
                    widget = self.widgets.get(("utility", "new_label"))
                    if widget is not None and widget.text != self.new_label:
                        widget.set_text(self.new_label)
            renpy.restart_interaction()

        def story_folders(self):
            base = _sw_os.path.join(config.gamedir, "story")
            try:
                return sorted(name for name in _sw_os.listdir(base) if _sw_os.path.isdir(_sw_os.path.join(base, name)))
            except OSError:
                return []

        def set_new_folder(self, folder):
            value = folder + "/" + (_sw_os.path.basename(self.new_path.replace("\\", "/")) or "writer_scene.rpy")
            widget = self.widgets.get(("utility", "new_path"))
            if widget is not None:
                widget.set_text(value)
            self.set_utility("new_path", value)
            return None

        def new_problem(self):
            """Why the New / Save-as dialog cannot proceed yet, or an empty string."""
            try:
                target = sw_source_path(self.new_path)
            except ValueError as exc:
                return str(exc)
            if _sw_os.path.exists(target):
                return "That file already exists. Open it instead, or choose another name."
            if self.modal == "new":
                if not _sw_re.fullmatch(r"[A-Za-z_]\w*", self.new_label or ""):
                    return "The label needs letters, numbers and underscores, starting with a letter."
                if renpy.has_label(self.new_label):
                    return "Label '%s' already exists in the game." % self.new_label
            return ""

        def filtered(self, kind, limit=240):
            """Search results computed once per query rather than on every screen update."""
            key = (kind, self.search.lower(), self.asset_mode)
            if self._filter_cache is None or self._filter_cache[0] != key:
                needle = key[1]
                if kind == "files":
                    items = [name for name in self.file_catalog if needle in name.lower()]
                elif kind == "music":
                    items = [(alias, path) for alias, path in self.music_catalog if needle in (alias + " " + path).lower()]
                elif kind == "cast":
                    items = [tag for tag in dev_sprite_tags(False) if needle in tag.lower()]
                else:
                    backgrounds = self.asset_mode == "backgrounds"
                    items = [name for name in self.image_catalog
                        if (not backgrounds or name.startswith("bg ")) and needle in name.lower()]
                self._filter_cache = (key, items)
            items = self._filter_cache[1]
            return items[:limit], max(0, len(items) - limit)

        def commit(self):
            if not self.pending:
                return True
            try:
                self.doc.update(self.selected, dict(self.fields))
                self.pending = False
                self.version += 1
                self.error = False
                return True
            except (ValueError, OSError) as exc:
                self.report(exc, True)
                return False

        def apply(self):
            self.blur()
            if self.commit():
                self.rebuild_stage()
                self.report("Change applied to draft.")
            return None

        def select(self, uid):
            if uid == self.selected and self.doc.get(uid) is not None:
                # Re-clicking the current beat must not reset its caret or undo.
                self.reveal()
                self.focus_primary()
                return None
            self.blur()
            if not self.commit() or self.doc.get(uid) is None:
                return None
            self.selected = uid
            self._load_fields()
            self.error = False
            self.reveal()
            self.focus_primary()
            renpy.restart_interaction()
            return None

        def prose_width(self):
            return (SW_FULL_W if self.focus_mode else SW_LEFT_W) - 2 * SW_DETAIL_PAD

        def focus_primary(self):
            """Typing lands in the prose after any action that leaves a textbox selected."""
            block = self.block
            if self.modal or block is None or block.kind != "say":
                return None
            self.field("text", self.prose_width(), SW_PROSE_H, True).set_focus(True)
            return None

        def step_selection(self, delta):
            rows = self.rows()
            if not rows:
                return None
            index = max(0, self.row_index())
            return self.select(rows[max(0, min(len(rows) - 1, index + delta))].uid)

        def _select_near(self, position):
            """After a deletion, land on a visible beat, preferring editable ones."""
            blocks = self.doc.blocks
            visible = lambda block: bool(block.raw.strip() or block.editable)
            after = [block for block in blocks[position:] if visible(block)]
            before = [block for block in reversed(blocks[:position]) if visible(block)]
            choice = next((block for block in after[:1] + before if block.editable), None)
            self.selected = (choice or (after or before or blocks)[0]).uid

        def speaker_label(self, alias):
            if not alias:
                return "Narration"
            if alias == "nier":
                return "Nier"
            if self._speaker_names is None:
                self._speaker_names = dict(self.speakers)
            return self._speaker_names.get(alias, alias)

        def beat_summary(self, block):
            data, kind = block.data, block.kind
            if kind in ("scene", "show"):
                parts = [data.get("image", "")]
                parts += ["at " + data["at"]] if data.get("at") else []
                parts += ["inline motion"] if data.get("atl") else []
                parts += ["with " + data["transition"]] if data.get("transition") else []
                return "  ·  ".join(parts)
            if kind == "hide":
                return "  ·  ".join([data.get("image", "")] + (["with " + data["transition"]] if data.get("transition") else []))
            if kind == "with":
                return data.get("transition", "")
            if kind == "pause":
                return data["duration"] + " seconds" if data.get("duration") else "wait for a click"
            if kind == "music":
                operation = data.get("operation", "play")
                parts = ["%s %s" % (operation.title(), data.get("channel", "music"))]
                parts += [data.get("track", "")] if operation != "stop" else []
                parts += ["fade in " + data["fadein"]] if data.get("fadein") else []
                parts += ["fade out " + data["fadeout"]] if data.get("fadeout") else []
                parts += [{"loop": "loop", "noloop": "once"}[data["loop"]]] if data.get("loop") in ("loop", "noloop") else []
                parts += ["volume " + data["volume"]] if data.get("volume") else []
                return "  ·  ".join(parts)
            return {"nier_enter": "Enter Nier prose", "nier_clear": "Nier page break",
                "nier_exit": "Leave Nier prose"}.get(kind, block.raw.strip())

        def row_parts(self, block):
            """(tag, tag colour, summary, summary colour, depth) for one script row."""
            kind, depth = block.kind, max(0, len(block.branch) - 1)
            if kind == "say":
                speaker, text = block.data.get("speaker", ""), block.data.get("text", "")
                return (self.speaker_label(speaker), SW_ACCENT if speaker else SW_MUTED,
                    text.replace("\n", " / ") or "(empty textbox)", SW_INK if text else SW_MUTED, depth)
            if kind == "label":
                return ("label", SW_KIND_COLORS["label"], block.data.get("name", ""), SW_KIND_COLORS["label"], 0)
            if kind == "branch":
                return ("branch", SW_KIND_COLORS["branch"], block.data.get("header", ""), "#e3c7b4", depth)
            if kind == "raw":
                lines = [line.strip() for line in block.raw.splitlines() if line.strip()]
                summary = (lines[0] if lines else "") + ("   (+%d lines)" % (len(lines) - 1) if len(lines) > 1 else "")
                tag = "note" if summary.startswith("#") else "logic"
                return (tag, SW_KIND_COLORS[tag], summary, SW_MUTED if tag == "note" else "#aab3b1", depth)
            word = SW_KIND_WORDS.get(kind, kind)
            return (word, SW_KIND_COLORS.get(word, SW_MUTED), self.beat_summary(block), SW_INK, depth)

        def row_title(self, block):
            tag, _, summary, _, _ = self.row_parts(block)
            return tag + "  ·  " + summary

        def rows(self):
            doc = self.doc
            if self._rows_doc is not doc or self._rows_revision != doc.revision:
                self._rows = [block for block in doc.blocks if block.raw.strip() or block.editable]
                self._row_positions = {block.uid: index for index, block in enumerate(self._rows)}
                self._rows_doc, self._rows_revision = doc, doc.revision
            return self._rows

        def row_index(self, uid=None):
            self.rows()
            return self._row_positions.get(self.selected if uid is None else uid, -1)

        def list_height(self):
            return max(SW_LIST_H, len(self.rows()) * SW_ROW_PITCH)

        def window_rows(self):
            """Only rows near the viewport become displayables; a chapter has ~1100."""
            rows = self.rows()
            value = self.list_adjustment.value if self.list_adjustment is not None else 0
            first = int(value // SW_ROW_PITCH)
            start = max(0, first - SW_ROW_BUFFER)
            end = min(len(rows), first + SW_LIST_H // SW_ROW_PITCH + 1 + SW_ROW_BUFFER)
            self._rendered_rows = (start, end)
            return [(index, rows[index]) for index in range(start, end)]

        def _list_scrolled(self, value):
            start, end = self._rendered_rows
            first = int(value // SW_ROW_PITCH)
            last = first + SW_LIST_H // SW_ROW_PITCH + 1
            if (start > 0 and first < start + 2) or (end < len(self.rows()) and last > end - 2):
                renpy.restart_interaction()
            return None

        def breadcrumb(self, block):
            labels = []
            for uid in block.branch:
                parent = self.doc.get(uid)
                if parent is not None:
                    labels.append(("label " + parent.data["name"]) if parent.kind == "label" else parent.raw.strip().rstrip(":"))
            return "  ›  ".join(labels)

        def reveal(self):
            index = self.row_index()
            adjustment = self.list_adjustment
            if index < 0 or adjustment is None:
                return None
            # The viewport may not have measured this document yet; give the
            # adjustment its real range so a jump is not clamped to the old one.
            limit = max(0, len(self.rows()) * SW_ROW_PITCH - SW_LIST_H)
            if adjustment.range != limit:
                adjustment.range = limit
            top = index * SW_ROW_PITCH
            if top < adjustment.value or top + SW_ROW_PITCH > adjustment.value + SW_LIST_H:
                adjustment.change(max(0, min(limit, top - SW_ROW_PITCH * 3)))
            renpy.restart_interaction()
            return None

        def add(self, kind, data=None):
            self.blur()
            if not self.commit():
                return None
            defaults = {
                "say": {"speaker": self.fields.get("speaker", "") if self.block.kind == "say" else "", "text": "", "attributes": ""},
                "scene": {"image": self.asset_name if self.asset_name.startswith("bg ") else "bg bedroom", "at": "", "transition": "dissolve_scene_full"},
                "show": {"image": self.asset_name if not self.asset_name.startswith("bg ") else "matsuda casual neut", "at": self.stage_at},
                "hide": {"image": self.hide_default_tag()},
                "with": {"transition": self.stage_transition}, "pause": {"duration": "0.5"},
                "music": {"operation": "play", "channel": "music", "track": self.music_alias, "fadein": "1.0", "fadeout": "1.0", "loop": "loop", "volume": "1.0"},
                "nier_enter": {}, "nier_exit": {}, "nier_clear": {},
            }
            try:
                added = self.doc.insert_after(self.selected, kind, data if data is not None else defaults[kind])
                self.selected = added.uid
                self.version += 1
                self._load_fields()
                self.modal = None
                self.reveal()
                # A success clears an earlier problem; the red chip used to stick.
                self.status, self.error = "Added " + dict(SW_TYPES).get(kind, kind).lower() + ".", False
                if kind == "music":
                    self.tab = "music"
                self.focus_primary()
                renpy.restart_interaction()
            except (ValueError, OSError) as exc:
                self.report(exc, True)
            return None

        def next_textbox(self):
            return self.add("say")

        def stage_images(self, before=True):
            """Images on stage just before (or including) the selected beat."""
            plan = getattr(self, "plan", None)
            blocks = list(plan.get("blocks", [])) if isinstance(plan, dict) else []
            uids = [block.uid for block in blocks]
            if self.selected in uids:
                blocks = blocks[:uids.index(self.selected) + (0 if before else 1)]
            try:
                images = sw_stage_state(blocks).get("images", [])
            except Exception:
                return []
            return [entry for entry in images if entry.get("tag") not in ("bg", "black")]

        def hide_default_tag(self):
            if self.block.kind == "show" and self.fields.get("image"):
                return self.fields["image"].split()[0]
            tags = [entry["tag"] for entry in self.stage_images(before=False)]
            return tags[-1] if tags else "matsuda"

        def insert_allowed(self):
            block = self.block
            return block is not None and (block.editable or block.kind == "label")

        def outline_blocks(self):
            return [block for block in self.rows() if block.kind in ("label", "branch", "scene", "nier_enter")]

        def outline_here(self):
            """The outline entry that contains the selected beat."""
            line, here = (self.block.line if self.block is not None else 0), None
            for block in self.outline_blocks():
                if block.line > line:
                    break
                here = block.uid
            return here

        def set_asset_mode(self, mode):
            self.blur()
            self.asset_mode, self.search, self._filter_cache = mode, "", None
            search = self.widgets.get(("utility", "search"))
            if search is not None:
                search.set_text("")
                search.set_focus(True)
            if mode == "cast" and dev_hub_has("dev_sprite_ensure"):
                dev_sprite_ensure()
            renpy.restart_interaction()
            return None

        def asset_result(self):
            """The image name the asset chooser would write right now."""
            if self.asset_mode == "cast":
                if not dev_hub_has("dev_sprite_attributes") or _dev_sprite.tag is None:
                    return ""
                return " ".join((_dev_sprite.tag,) + tuple(dev_sprite_attributes()))
            return self.asset_name or ""

        def palette_insert(self, kind):
            """Insert palette: kinds that need a choice open their picker first."""
            if not self.insert_allowed():
                return self.report("Select an editable beat or a scene label, then insert after it.", True)
            if kind == "scene":
                return self.browse_assets("backgrounds", "insert")
            if kind == "show":
                return self.browse_assets("cast", "insert")
            if kind in ("play", "queue"):
                self.music_target = "insert_" + kind
                return self.open_modal("music")
            if kind == "stop":
                return self.add("music", {"operation": "stop", "channel": "music", "fadeout": "1.0"})
            return self.add(kind)

        def change_field(self, key, value):
            self.blur()
            if key == "speaker" and value != self.fields.get("speaker", ""):
                self.fields["attributes"] = ""
                attributes_widget = self.widgets.get((self.selected, "attributes"))
                if attributes_widget is not None:
                    attributes_widget.set_text("")
            self.fields[key] = value
            if self.block.kind == "music" and key == "operation":
                if value == "stop":
                    for removed in ("track", "fadein", "loop", "volume"):
                        self.fields[removed] = "default" if removed == "loop" else ""
                    self.fields.setdefault("fadeout", "1.0")
                else:
                    if not self.fields.get("track"):
                        self.fields["track"] = self.music_alias
                    self.fields.setdefault("loop", "loop" if value == "play" else "noloop")
                    if not self.fields.get("volume"):
                        self.fields["volume"] = "1.0"
                    if value == "queue":
                        self.fields["fadein"] = ""
                        self.fields["fadeout"] = ""
                    else:
                        if not self.fields.get("fadein"):
                            self.fields["fadein"] = "1.0"
                        if not self.fields.get("fadeout"):
                            self.fields["fadeout"] = "1.0"
                for cache_key in list(self.widgets):
                    if cache_key[0] == self.selected:
                        replacement = str(self.fields.get(cache_key[1], ""))
                        if self.widgets[cache_key].text != replacement:
                            self.widgets[cache_key].set_text(replacement)
            for cache_key in list(self.widgets):
                if len(cache_key) > 1 and cache_key[1] == key:
                    self.widgets[cache_key].set_text(str(value))
            self.pending = True
            self.commit()
            self.rebuild_stage()
            renpy.restart_interaction()
            return None

        def motion_state(self):
            """(motion, cast size, slot, focused) read from a slot transform, else None."""
            match = _sw_re.fullmatch(r"(t|i|f|h|hf|l|lf|s)([1-6])([1-6])", (self.fields.get("at") or "").strip())
            if not match or int(match.group(3)) > int(match.group(2)):
                return None
            family = match.group(1)
            return ({"f": "t", "hf": "h", "lf": "l"}.get(family, family), int(match.group(2)),
                int(match.group(3)), family in ("f", "hf", "lf"))

        def set_motion(self, motion=None, count=None, slot=None, focused=None):
            """Compose the project's txx/ixx/fxx/hxx/lxx slot names from plain choices."""
            state = self.motion_state() or ("t", 1, 1, False)
            motion = state[0] if motion is None else motion
            count = state[1] if count is None else count
            slot = min(state[2] if slot is None else slot, count)
            focused = (state[3] if focused is None else focused) and motion in ("t", "h", "l")
            if motion == "s":
                count = slot = 1
            family = {"t": "f", "h": "hf", "l": "lf"}[motion] if focused else motion
            return self.change_field("at", "%s%d%d" % (family, count, slot))

        def source_context(self, radius=28):
            """Numbered source lines around the selected beat, cached per revision."""
            key = (self.doc, self.doc.revision, self.selected)
            if self._source_cache is None or self._source_cache[0] != key:
                lines = self.doc.to_bytes().decode("utf-8-sig").splitlines()
                block = self.block
                first = block.line if block is not None else 1
                span = max(1, len(block.raw.splitlines())) if block is not None else 1
                start, end = max(1, first - radius), min(len(lines), first + span - 1 + radius)
                self._source_cache = (key, [(number, lines[number - 1].replace("\t", "    "),
                    first <= number < first + span) for number in range(start, end + 1)])
            return self._source_cache[1]

        def minimal_attributes(self, name):
            """The fewest say attributes that turn the on-stage sprite into `name`.

            Outfit and pose inherit from the shown image, as in hand-written
            scenes, so a new face writes `happy` rather than the whole rig.
            Anything that does not verifiably resolve falls back to the full list.
            """
            parts = name.split()
            tag, wanted = parts[0], parts[1:]
            try:
                shown = next((entry["name"].split() for entry in self.stage_images(before=True) if entry["tag"] == tag), None)
                if not shown:
                    return wanted
                added = [part for part in wanted if part not in shown[1:]]
                removed = ["-" + part for part in shown[1:] if part not in wanted]
                if not added and not removed:
                    return []
                target = renpy.display.image.ShownImageInfo().apply_attributes("master", tag, tuple(parts))
                for candidate in (added, added + removed):
                    if not candidate:
                        continue
                    info = renpy.display.image.ShownImageInfo()
                    info.predict_show("master", tuple(shown))
                    result = info.apply_attributes("master", tag, (tag,) + tuple(candidate))
                    if result is not None and target is not None and set(result[1:]) == set(target[1:]):
                        return candidate
            except Exception:
                pass
            return wanted

        def replay_stage(self):
            self.blur()
            if self.commit():
                self.rebuild_stage(replay=True)
                renpy.restart_interaction()
            self.focus_primary()
            return None

        def edit_operation(self, operation):
            if operation in ("undo", "redo"):
                focused = next((widget for widget in self.widgets.values() if widget.focused), None)
                # The field sees mouse-down outside it before the toolbar's
                # mouse-up action. Retain the last edited target across that blur.
                target = focused or self._last_editor
                if target is not None and target in self.widgets.values() and getattr(target.buffer, operation + "_stack"):
                    getattr(target, operation)()
                    target.set_focus(True)
                    return None
            self.blur()
            if not self.commit():
                return None
            try:
                if operation in ("undo", "redo"):
                    if not getattr(self.doc, operation)():
                        return self.report("Nothing to %s." % operation)
                    if self.doc.get(self.selected) is None:
                        self._select_near(0)
                elif operation == "duplicate":
                    self.selected = self.doc.duplicate(self.selected).uid
                elif operation == "delete":
                    position = self.doc.index_of(self.selected)
                    self.doc.delete(self.selected)
                    self._select_near(position)
                elif operation in ("up", "down"):
                    self.doc.move(self.selected, -1 if operation == "up" else 1)
                self.version += 1
                self._load_fields()
                self.reveal()
                self.report({"undo": "Undid the last change.", "redo": "Redid the change.",
                    "duplicate": "Duplicated the beat.", "delete": "Deleted the beat.",
                    "up": "Moved the beat up.", "down": "Moved the beat down."}[operation])
                self.focus_primary()
            except (ValueError, OSError) as exc:
                self.report(exc, True)
            return None

        def split_text(self):
            if self.block.kind != "say":
                return None
            widget = self.field("text", self.prose_width(), SW_PROSE_H, True)
            caret = getattr(widget, "caret_position", len(widget.text))
            text = widget.text
            head, tail = text[:caret].rstrip(" \n"), text[caret:].lstrip(" \n")
            if not head or not tail:
                return self.report("Put the cursor between two sentences to split the textbox there.", True)
            self.blur()
            try:
                # One undo step. The second box inherits the expression, as a
                # hand-written continuation would, so it restates no attributes.
                with self.doc.batch():
                    self.doc.update(self.selected, dict(self.fields, text=head))
                    added = self.doc.insert_after(self.selected, "say",
                        {"speaker": self.fields.get("speaker", ""), "attributes": "", "text": tail})
            except (ValueError, OSError) as exc:
                return self.report(exc, True)
            self.pending = False
            self.version += 1
            self.selected = added.uid
            self._load_fields()
            self.reveal()
            self.focus_primary()
            self.field("text", self.prose_width(), SW_PROSE_H, True).buffer.move(0)
            return self.report("Split into two textboxes.")

        def join_text(self):
            self.blur()
            if not self.commit():
                return None
            first = self.block
            position = self.doc.index_of(self.selected)
            # Blank lines are not a boundary; comments, staging and logic are.
            second = next((block for block in self.doc.blocks[position + 1:] if block.raw.strip()), None)
            if first.kind != "say" or second is None or second.kind != "say":
                return self.report("Join needs the next beat to be a textbox.", True)
            if first.branch != second.branch or first.data.get("speaker", "") != second.data.get("speaker", ""):
                return self.report("Join needs the same speaker in the same branch.", True)
            if second.data.get("attributes", "") not in ("", first.data.get("attributes", "")):
                return self.report("The next textbox changes expression. Clear its expression first, or keep it separate.", True)
            head, tail = first.data.get("text", "").rstrip(" \n"), second.data.get("text", "").lstrip(" \n")
            try:
                with self.doc.batch():
                    self.doc.update(first.uid, {"text": " ".join(part for part in (head, tail) if part)})
                    self.doc.delete(second.uid)
            except (ValueError, OSError) as exc:
                return self.report(exc, True)
            self.version += 1
            self._load_fields()
            self.focus_primary()
            self.field("text", self.prose_width(), SW_PROSE_H, True).buffer.move(len(head) + (1 if head and tail else 0))
            return self.report("Joined the next textbox.")

        def open_modal(self, name):
            self.blur()
            if not self.commit():
                return None
            self.modal, self.search = name, ""
            self._filter_cache = None
            search_widget = self.widgets.get(("utility", "search"))
            if search_widget is not None:
                search_widget.set_text("")
            if name in ("files", "music", "assets"):
                # A searchable list opens with the cursor already in its search.
                self.utility_field("search").set_focus(True)
            if name == "music" and self.music_target is None:
                self.music_target = "edit" if self.block.kind == "music" else "browse"
            if name in ("new", "destination"):
                self._label_edited = False
            if name == "files":
                self.refresh_files()
            elif name == "drafts":
                found = []
                if _sw_os.path.isdir(self.draft_dir):
                    for filename in _sw_os.listdir(self.draft_dir):
                        if not filename.endswith(".json") or filename == "recovery.json":
                            continue
                        path = _sw_os.path.join(self.draft_dir, filename)
                        try:
                            with open(path, "r", encoding="utf-8") as handle:
                                draft = _sw_json.load(handle)
                            source = draft.get("document", {}).get("path", "")
                            caption = _sw_os.path.relpath(source, config.gamedir) if source else "New scene"
                            for prefix, kind in (("before-recovery-", "Before recovery"), ("before-reload-", "Before reload")):
                                if filename.startswith(prefix):
                                    stamp = filename[len(prefix):-len(".json")]
                                    if stamp.isdigit():
                                        stamp = _sw_time.strftime("%Y-%m-%d %H:%M:%S", _sw_time.localtime(int(stamp) / 1000000000.0))
                                    caption = kind + " · " + stamp + " · " + caption
                            modified = _sw_os.path.getmtime(path)
                            caption += " · saved " + _sw_time.strftime("%b %d %H:%M", _sw_time.localtime(modified))
                            found.append((modified, path, caption.replace("\\", "/")))
                        except (ValueError, OSError):
                            continue
                self.draft_catalog = [(path, caption) for modified, path, caption in sorted(found, reverse=True)]
            renpy.restart_interaction()
            return None

        def close_modal(self):
            self.blur()
            self.modal, self.confirm, self.music_target = None, None, None
            renpy.restart_interaction()
            self.focus_primary()
            return None

        def ask(self, title, message, label, action):
            self.blur()
            self.confirm = {"title": title, "message": message, "label": label, "action": action}
            self.modal = "confirm"
            renpy.restart_interaction()
            return None

        def confirm_accept(self):
            action = (self.confirm or {}).get("action")
            self.modal, self.confirm = None, None
            if action == "discard_close":
                self.pending = False
                self._load_fields()
                self.save_draft(quiet=True)
                renpy.end_interaction("close")
            elif action == "force_close":
                renpy.end_interaction("close")
            elif action == "reload_disk":
                self.reload_from_disk(confirmed=True)
            renpy.restart_interaction()
            return None

        def open_file(self, relative):
            # An untouched starting scene is not worth a draft file.
            keep = bool(self.version or getattr(self.doc, "path", "")) and self.dirty
            previous = self.filename
            if keep and not self.save_draft(quiet=True):
                return None
            try:
                self.doc = _SWDocument.load(sw_source_path(relative))
                self.selected = next((b.uid for b in self.doc.blocks if b.kind == "say"), self.doc.blocks[0].uid)
                self._load_fields()
                self.modal = None
                self.last_draft = None
                self.disk_changed, self._disk_stamp = False, None
                self.reveal()
                self.focus_primary()
                self.report("Opened " + relative + "." + (" Unsaved changes to " + previous + " are kept in Drafts." if keep else ""))
            except (ValueError, OSError) as exc:
                self.report(exc, True)
            return None

        def create_new(self):
            if not self.save_draft(quiet=True):
                return None
            try:
                target = sw_source_path(self.new_path)
                if _sw_os.path.exists(target):
                    raise ValueError("That source already exists. Open it, or choose a new filename.")
                if not _sw_re.fullmatch(r"[A-Za-z_]\w*", self.new_label) or renpy.has_label(self.new_label):
                    raise ValueError("Choose a unique label using letters, numbers and underscores.")
                self.doc = _SWDocument.new(self.new_label)
                self.doc.path = target
                self.selected = self.doc.blocks[0].uid
                self._load_fields()
                self.add("say")
                self.modal = None
                self.last_draft = None
                self.report("New scene ready. Save to Story creates the source file.")
            except (ValueError, OSError) as exc:
                self.report(exc, True)
            return None

        def save_draft(self, quiet=False):
            if not config.developer or not self.commit():
                return False
            try:
                payload = {"schema": 1, "document": self.doc.draft_payload(), "selected": self.selected,
                    "selected_line": self.block.line, "selected_kind": self.block.kind,
                    "new_path": self.new_path, "new_label": self.new_label, "font_size": self.font_size}
                encoded = _sw_json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
                digest = _sw_hashlib.sha256(encoded).hexdigest()
                if digest != self.last_draft:
                    _sw_os.makedirs(self.draft_dir, exist_ok=True)
                    # Per-source drafts survive opening another file; recovery is the last document.
                    key = _sw_hashlib.sha256(self.filename.encode("utf-8")).hexdigest()[:20]
                    for destination in (_sw_os.path.join(self.draft_dir, key + ".json"), self.draft_file):
                        temporary = destination + ".tmp"
                        with open(temporary, "wb") as handle:
                            handle.write(encoded)
                            handle.flush()
                            _sw_os.fsync(handle.fileno())
                        _sw_os.replace(temporary, destination)
                    self.last_draft = digest
                if not quiet:
                    self.report("Draft saved. Story source is unchanged.")
                return True
            except (ValueError, OSError) as exc:
                self.report("Draft save failed: " + str(exc), True)
                return False

        def save_draft_action(self):
            self.blur()
            self.save_draft()
            return None

        def recover(self, draft_path=None):
            try:
                selected_draft = _sw_os.path.realpath(draft_path or self.draft_file)
                if _sw_os.path.commonpath((_sw_os.path.realpath(self.draft_dir), selected_draft)) != _sw_os.path.realpath(self.draft_dir):
                    raise ValueError("Choose a draft in this writer's recovery folder.")
                with open(selected_draft, "r", encoding="utf-8") as handle:
                    payload = _sw_json.load(handle)
                document = _SWDocument.from_draft(payload["document"])
                if document.path:
                    relative = _sw_os.path.relpath(document.path, _sw_os.path.join(config.gamedir, "story"))
                    if sw_source_path(relative) != _sw_os.path.realpath(document.path):
                        raise ValueError("Recovery source is outside this project's story folder.")
                # Read the chosen draft first: saving the current one may update
                # recovery.json. Keep a separately discoverable snapshot before
                # replacing unsaved work, including another draft of this file.
                if self.dirty and not self._snapshot_draft("before-recovery-"):
                    return None
                self.doc = document
                self.selected = payload.get("selected", self.doc.blocks[0].uid)
                if not any(b.uid == self.selected for b in self.doc.blocks):
                    # Parsing recovery source creates fresh block IDs. Its saved
                    # line/kind remain stable because those exact bytes are restored.
                    selected_line = payload.get("selected_line")
                    selected_kind = payload.get("selected_kind")
                    selected_block = next((b for b in self.doc.blocks
                        if b.line == selected_line and (not selected_kind or b.kind == selected_kind)), None)
                    if selected_block is None:
                        selected_block = next((b for b in self.doc.blocks if b.kind == "say"), self.doc.blocks[0])
                    self.selected = selected_block.uid
                self.font_size = max(18, min(34, int(payload.get("font_size", 24))))
                self.new_path = payload.get("new_path", self.new_path)
                self.new_label = payload.get("new_label", self.new_label)
                self._load_fields()
                self.modal = None
                self.last_draft = None
                self.save_draft(quiet=True)
                self.reveal()
                self.report("Recovered draft. Source save checks for external edits before writing.")
            except (ValueError, KeyError, OSError) as exc:
                self.report("Cannot recover: " + str(exc), True)
            return None

        def save_shortcut(self):
            # Keyboard save should leave writing/undo at the same cursor, even
            # when a source conflict is reported. A destination dialog owns focus.
            resume_editor = next((widget for widget in self.widgets.values() if widget.focused), None)
            try:
                self.save_source()
            finally:
                if not self.modal and resume_editor is not None and resume_editor in self.widgets.values():
                    resume_editor.set_focus(True)
            return None

        def save_source(self):
            self.blur()
            if not self.commit() or not self.save_draft(quiet=True):
                return None
            if not getattr(self.doc, "path", ""):
                self.modal = "destination"
                renpy.restart_interaction()
                return None
            try:
                path = sw_source_path(_sw_os.path.relpath(self.doc.path, _sw_os.path.join(config.gamedir, "story")))
                self.doc.save(path=path, validator=lambda candidate, target: sw_validate_source(candidate, target, self.doc._base_bytes),
                    backup_dir=_sw_os.path.join(self.draft_dir, "backups"), developer=bool(config.developer))
                self.last_draft = None
                self.disk_changed, self._disk_stamp = False, None
                self.save_draft(quiet=True)
                self.report("Saved to story. Reload after leaving the writer to use the updated source in normal play.")
                self.refresh_files()
            except (ValueError, OSError) as exc:
                self.report(exc, True)
            return None

        def export_source(self):
            self.blur()
            if not self.commit() or not self.save_draft(quiet=True):
                return None
            try:
                source = self.doc.to_bytes()
                target = self.doc.path or sw_source_path(self.new_path)
                sw_validate_source(source, target, self.doc._base_bytes)
                folder = _sw_os.path.join(self.draft_dir, "exports")
                _sw_os.makedirs(folder, exist_ok=True)
                filename = _sw_os.path.splitext(_sw_os.path.basename(target))[0] + "-" + str(_sw_time.time_ns()) + ".rpy"
                destination = _sw_os.path.join(folder, filename)
                with open(destination, "xb") as handle:
                    handle.write(source)
                    handle.flush()
                    _sw_os.fsync(handle.fileno())
                self.report("Exported " + _sw_os.path.relpath(destination, config.basedir).replace("\\", "/") + ". This copy is not loaded by the game.")
            except (ValueError, OSError) as exc:
                self.report(exc, True)
            return None

        def choose_destination(self):
            try:
                path = sw_source_path(self.new_path)
                if _sw_os.path.exists(path):
                    raise ValueError("Choose a new source filename; open existing files to edit them.")
                self.doc.path = path
                self.modal = None
                self.save_source()
            except (ValueError, OSError) as exc:
                self.report(exc, True)
            return None

        def tick(self):
            """Idle work. Its timer does not rebuild the screen unless something changed."""
            now = _sw_time.monotonic()
            if self.pending and now - self.last_text_change > 0.8:
                if self.commit():
                    if self._stage_dirty:
                        self.rebuild_stage()
                    self.save_draft(quiet=True)
                    renpy.restart_interaction()
            if now - self._disk_checked > 3.0:
                self._disk_checked = now
                self.check_disk()
            return None

        def check_disk(self):
            """Notice a Syncthing or outside-editor write before a save would conflict."""
            path = getattr(self.doc, "path", "")
            if not path or getattr(self.doc, "_unsaved", True):
                return None
            try:
                stat = _sw_os.stat(path)
                stamp = (path, stat.st_size, stat.st_mtime_ns)
            except OSError:
                # None means unchecked; a missing source must trigger its first
                # comparison too. Include the path when switching recovery drafts.
                stamp = (path, None, None)
            if stamp == self._disk_stamp:
                return None
            self._disk_stamp = stamp
            try:
                with open(path, "rb") as handle:
                    changed = handle.read() != self.doc._base_bytes
            except OSError:
                changed = True
            if changed != self.disk_changed:
                self.disk_changed = changed
                renpy.restart_interaction()
            return None

        def reload_from_disk(self, confirmed=False):
            if not getattr(self.doc, "path", ""):
                return None
            if self.dirty and not confirmed:
                return self.ask("Reload this file from disk?",
                    "It changed outside the writer. Your unsaved version is kept in Drafts as \"Before reload\".",
                    "Keep a draft and reload", "reload_disk")
            if self.dirty and not self._snapshot_draft("before-reload-"):
                return None
            line = self.block.line if self.block is not None else 1
            relative = _sw_os.path.relpath(self.doc.path, _sw_os.path.join(config.gamedir, "story")).replace("\\", "/")
            self.pending = False
            self.open_file(relative)
            self.disk_changed, self._disk_stamp = False, None
            self._select_line(line)
            return None

        def _snapshot_draft(self, prefix):
            if not self.save_draft(quiet=True):
                return False
            try:
                snapshot = _sw_os.path.join(self.draft_dir, prefix + str(_sw_time.time_ns()) + ".json")
                with open(self.draft_file, "rb") as previous, open(snapshot, "xb") as output:
                    output.write(previous.read())
                    output.flush()
                    _sw_os.fsync(output.fileno())
                return True
            except OSError as exc:
                self.report("Could not keep a draft: " + str(exc), True)
                return False

        def _select_line(self, line, kind=None):
            if line is None:
                return None
            block = next((block for block in self.doc.blocks if block.line >= line
                and (block.raw.strip() or block.editable) and (not kind or block.kind == kind)), None)
            if block is not None:
                self.select(block.uid)
            return None

        def restore_last_session(self):
            """Reopen what the author was writing when the writer last closed."""
            try:
                with open(self.draft_file, "r", encoding="utf-8") as handle:
                    payload = _sw_json.load(handle)
                document = _SWDocument.from_draft(payload["document"])
            except (OSError, ValueError, KeyError, TypeError):
                return False
            untouched = document.to_bytes() == document._base_bytes
            if document.path:
                relative = _sw_os.path.relpath(document.path, _sw_os.path.join(config.gamedir, "story")).replace("\\", "/")
                try:
                    if sw_source_path(relative) != _sw_os.path.realpath(document.path):
                        return False
                except ValueError:
                    return False
                if untouched and not document._unsaved:
                    if not _sw_os.path.isfile(document.path):
                        return False
                    self.open_file(relative)
                    self._select_line(payload.get("selected_line"), payload.get("selected_kind"))
                    self.report("Reopened " + relative + " where you left off.")
                    return True
            elif untouched:
                return False
            self.doc = document
            self.selected = document.blocks[0].uid
            self.font_size = max(18, min(34, int(payload.get("font_size", self.font_size))))
            self.new_path = payload.get("new_path", self.new_path)
            self.new_label = payload.get("new_label", self.new_label)
            self._load_fields()
            self._select_line(payload.get("selected_line"), payload.get("selected_kind"))
            self.last_draft = None
            self.reveal()
            self.report("Restored unsaved work on " + self.filename + " from your last session.")
            return True

        def resize_text(self, delta):
            self.blur()
            if self.commit():
                self.font_size = max(18, min(34, self.font_size + delta))
                for cache_key, widget in self.widgets.items():
                    if cache_key[0] == self.selected and widget.multiline:
                        widget.set_font_size(self.font_size)
                renpy.restart_interaction()
                self.focus_primary()
            return None

        def toggle_focus(self):
            self.blur()
            if self.commit():
                self.focus_mode = not self.focus_mode
                renpy.restart_interaction()
                self.focus_primary()
            return None

        def pick_speaker(self, alias):
            self.modal = None
            self.change_field("speaker", alias)
            return None

        def browse_assets(self, mode="backgrounds", target="insert"):
            self.asset_mode, self.asset_target = mode, target
            if target == "edit" and self.block.kind in ("show", "scene") and self.fields.get("image"):
                self.asset_name = self.fields["image"]
            if mode == "cast" and dev_hub_has("dev_sprite_ensure"):
                dev_sprite_ensure()
                if target == "attributes":
                    speaker = getattr(renpy.store, self.fields.get("speaker", "") or "narrator", None)
                    tag = getattr(speaker, "image_tag", None)
                    if not tag:
                        return self.report("This speaker has no sprite. Choose a character speaker before attaching an expression.", True)
                    # Start from what is on stage at this beat, not the rig defaults.
                    current = next((entry["name"] for entry in self.stage_images(before=False) if entry["tag"] == tag), tag)
                    if not sw_sprite_load(current):
                        dev_sprite_select_tag(tag)
                elif target == "edit" and self.block.kind == "show":
                    sw_sprite_load(self.fields.get("image", ""))
            self.open_modal("assets")
            return None

        def pick_asset(self, name):
            self.asset_name = name
            renpy.restart_interaction()
            return None

        def use_asset(self):
            if self.asset_mode == "cast":
                self.asset_name = " ".join((_dev_sprite.tag,) + dev_sprite_attributes())
            if self.asset_target == "attributes":
                speaker = getattr(renpy.store, self.fields.get("speaker", "") or "narrator", None)
                expected = getattr(speaker, "image_tag", None)
                selected_tag = self.asset_name.split()[0] if self.asset_name else ""
                if not expected or selected_tag != expected:
                    return self.report("Choose an expression for %s; this textbox's speaker uses that sprite." % (expected or "a character speaker"), True)
                self.modal = None
                self.change_field("attributes", " ".join(self.minimal_attributes(self.asset_name)))
            elif self.asset_target == "edit" and self.block.kind in ("show", "scene", "hide"):
                self.modal = None
                self.change_field("image", self.asset_name)
            else:
                kind = "scene" if self.asset_mode == "backgrounds" else "show"
                data = {"image": self.asset_name, "at": "" if kind == "scene" else self.stage_at}
                if kind == "scene":
                    data["transition"] = "dissolve_scene_full"
                self.add(kind, data)
            return None

        def pick_music(self, alias):
            self.blur()
            self.music_alias = alias if alias.startswith("audio.") else "audio." + alias
            target, self.music_target = self.music_target, None
            self.modal = None
            if target in ("insert_play", "insert_queue"):
                operation = target[len("insert_"):]
                data = {"operation": operation, "channel": "music", "track": self.music_alias,
                    "loop": "loop" if operation == "play" else "noloop", "volume": "1.0"}
                if operation == "play":
                    data.update(fadein="1.0", fadeout="1.0")
                return self.add("music", data)
            if self.block.kind == "music":
                self.change_field("track", self.music_alias)
            renpy.restart_interaction()
            self.focus_primary()
            return None

        def audition(self, alias=None):
            self.blur()
            try:
                sw_audition(alias or self.fields.get("track") or self.music_alias)
                self.auditioning = True
                self.report("Auditioning track. Stop audition resumes the previous audio.")
            except Exception as exc:
                self.report(exc, True)
            return None

        def stop_audition(self):
            sw_stop_audition()
            self.auditioning = False
            renpy.restart_interaction()
            return None

        def rebuild_stage(self, replay=False):
            self._stage_dirty = False
            try:
                self.plan = sw_preview_plan(self.doc, self.selected)
                state = sw_stage_state(self.plan.get("blocks", []), self.selected)
                self.stage_warning = state.get("warning", "") or self.plan.get("warning", "")
                images = sorted(state.get("images", []), key=lambda item: item.get("zorder", 0))
                signature = tuple((entry["name"], entry.get("tag"), entry.get("layer"), entry.get("at", ""),
                    entry.get("atl", ""), entry.get("zorder", 0)) for entry in images)
                if not replay and self.stage is not None and signature == self._stage_signature:
                    # Same composition: keep the settled transforms. Rebuilding
                    # replayed every entrance whenever another beat was clicked.
                    return
                children = [Solid("#111820")]
                for entry in images:
                    child = ImageReference(entry["name"])
                    expressions = entry.get("at", "")
                    transforms = list(sw_resolve_transforms(expressions)) if expressions else []
                    if not transforms:
                        tag = entry.get("tag") or entry["name"].split()[0]
                        default_transform = config.tag_transform.get(tag)
                        if default_transform is not None:
                            transforms = list(default_transform) if isinstance(default_transform, (list, tuple)) else [default_transform]
                    if entry.get("atl"):
                        transforms.append(sw_resolve_inline_motion(entry["atl"]))
                    child = sw_composition_show(child, transforms)
                    children.append(child)
                scene = Fixed(*children, xysize=(1280, 720))
                self.stage = SWPreviewSurface(Transform(scene, zoom=SW_RIGHT_W / 1280.0, crop=(0, 0, 1280, 720)), SW_RIGHT_W, SW_STAGE_H)
                self._stage_signature = signature
            except Exception as exc:
                self.stage = Solid("#111820", xysize=(SW_RIGHT_W, SW_STAGE_H))
                self._stage_signature = None
                self.stage_warning = str(exc)

        def play(self, from_here=False):
            resume_editor = next((widget for widget in self.widgets.values() if widget.focused), None) or self._last_editor
            self.blur()
            if not self.commit():
                return None
            self.rebuild_stage()
            if self.plan.get("requires_setup") and not from_here:
                self.modal = "preview_setup"
                renpy.restart_interaction()
                return None
            blocks = self.plan.get("blocks", [])
            if not blocks:
                self.report(self.plan.get("warning") or "Select prose or a staging cue to preview.", True)
                return None
            self.modal = None
            self.stop_audition()
            renpy.hide_screen("story_writer")
            try:
                result = sw_play_preview(blocks)
                self.status = "Returned from preview. " + (str(result.get("message", "")) if isinstance(result, dict) else "")
                self.error = isinstance(result, dict) and result.get("status") in ("boundary", "error", "unavailable")
            except Exception as exc:
                self.status, self.error = "Preview stopped: " + str(exc), True
            finally:
                renpy.show_screen("story_writer", session=self)
                if resume_editor is not None and resume_editor in self.widgets.values():
                    resume_editor.set_focus(True)
                renpy.restart_interaction()
            return None

        def exit(self):
            self.blur()
            if self.modal:
                self.close_modal()
                return None
            if self.pending and not self.commit():
                # An invalid field used to make the writer impossible to close.
                return self.ask("This beat has a value that cannot be saved",
                    str(self.status) + "\n\nClosing discards only that field's change. Everything else is kept as a draft.",
                    "Discard it and close", "discard_close")
            if self.save_draft(quiet=True):
                renpy.end_interaction("close")
                return None
            return self.ask("The recovery draft could not be written", str(self.status),
                "Close without a draft", "force_close")

        def escape(self):
            return self.close_modal() if self.modal else self.exit()

    def story_writer_open():
        if config.developer and renpy.has_label("story_writer_entry"):
            renpy.call_in_new_context("story_writer_entry")
        return None

label story_writer_entry:
    if not config.developer:
        return
    python:
        renpy.context_dynamic("main_menu", "_menu", "quick_menu", "_game_menu_screen", "_skipping", "_sw_session", "_sw_previous_autoreload")
        main_menu = False
        _menu = False
        quick_menu = False
        _game_menu_screen = None
        _skipping = None
        renpy.context()._menu = False
        renpy.context()._main_menu = False
        _sw_previous_autoreload = config.autoreload
        config.autoreload = False
        renpy.hide_screen("dev_hub")
        try:
            _sw_session = SWSession()
            _sw_session.restore_last_session()
            renpy.call_screen("story_writer", session=_sw_session)
        finally:
            sw_stop_audition()
            config.autoreload = _sw_previous_autoreload
    return
