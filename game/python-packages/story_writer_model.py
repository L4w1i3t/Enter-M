"""Lossless source editing for ENTER M's developer story writer.

This module deliberately does not import Ren'Py or execute source expressions.
Only complete, recognised statements are editable; all other source is retained
verbatim. Runtime asset/transform availability is the caller's validation job.
"""

import ast
import base64
import contextlib
import copy
import datetime
import hashlib
import math
import os
import re
import tempfile
import uuid


class StoryWriterError(ValueError):
    pass


class ValidationError(StoryWriterError):
    pass


class ConflictError(StoryWriterError):
    pass


_NAME = re.compile(r"^[A-Za-z_][A-Za-z_0-9]*$")
_ATTRIBUTE = re.compile(r"^-?[A-Za-z_][A-Za-z_0-9]*$")
_NUMBER = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")
_TRACK_NAME = re.compile(r"^[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)?$")
_ATL_PROPERTIES = frozenset(("alpha", "xoffset", "yoffset", "zoom"))
_ATL_EASINGS = frozenset(("linear", "ease", "easein", "easeout", "easein_quad", "easeout_quad", "easein_cubic", "easeout_cubic"))
_BOM = b"\xef\xbb\xbf"
_MAX_SOURCE = 32 * 1024 * 1024
_STATEMENT_WORDS = frozenset(("scene", "show", "hide", "with", "pause", "play", "queue", "stop",
    "call", "jump", "return", "menu", "if", "elif", "else", "while", "python", "init",
    "label", "define", "default", "screen", "transform", "image", "window", "nvl", "voice"))
_IMAGE_CLAUSE_WORDS = frozenset(("at", "as", "onlayer", "with", "zorder", "behind"))


def _uid():
    return uuid.uuid4().hex


def _fingerprint(data):
    return hashlib.sha256(data).hexdigest()


def _text(value, field, allow_newline=False):
    if not isinstance(value, str):
        raise ValidationError("%s must be text." % field)
    if "\x00" in value or (not allow_newline and ("\n" in value or "\r" in value)):
        raise ValidationError("%s contains an invalid line break or NUL." % field)
    return value


def _name(value, field, optional=False):
    value = _text(value, field).strip()
    if not value and optional:
        return ""
    if not _NAME.fullmatch(value):
        raise ValidationError("%s must be a simple Ren'Py name." % field)
    return value


def _number(value, field, optional=False, minimum=None, maximum=None):
    if value is None and optional:
        return ""
    if isinstance(value, bool):
        raise ValidationError("%s must be a number." % field)
    value = str(value).strip()
    if not value and optional:
        return ""
    if not _NUMBER.fullmatch(value):
        raise ValidationError("%s must be a literal number." % field)
    number = float(value)
    if not math.isfinite(number) or (minimum is not None and number < minimum) or (maximum is not None and number > maximum):
        raise ValidationError("%s is outside its allowed range." % field)
    return value


def _numeric_node(node):
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        return _numeric_node(node.operand)
    return isinstance(node, ast.Constant) and type(node.value) in (int, float) and math.isfinite(node.value)


def _expression(value, field, multiple=False, optional=True):
    """Accept names and named calls with finite literal numeric arguments only."""
    value = _text(value, field).strip()
    if not value and optional:
        return ""
    try:
        node = ast.parse(value, mode="eval").body
    except (SyntaxError, ValueError, TypeError):
        raise ValidationError("%s is not a supported named transform or transition." % field)
    nodes = node.elts if multiple and isinstance(node, ast.Tuple) else [node]
    if not nodes:
        raise ValidationError("%s cannot be empty." % field)
    for item in nodes:
        if isinstance(item, ast.Name) and _NAME.fullmatch(item.id):
            continue
        if (isinstance(item, ast.Call) and isinstance(item.func, ast.Name)
                and _NAME.fullmatch(item.func.id)
                and all(_numeric_node(arg) for arg in item.args)
                and all(kw.arg is not None and _NAME.fullmatch(kw.arg) and _numeric_node(kw.value) for kw in item.keywords)):
            keyword_names = [keyword.arg for keyword in item.keywords]
            if len(keyword_names) != len(set(keyword_names)):
                raise ValidationError("%s repeats a keyword argument." % field)
            continue
        raise ValidationError("%s supports named presets with numeric arguments only." % field)
    return value


def _decode_renpy_string(value):
    # Match MatsuPy/Ren'Py Lexer.string, including the distinction between
    # literal brackets and interpolation. This is not Python string decoding.
    value = re.sub(r"[ \n]+", " ", value)

    def dequote(match):
        char = match.group(1)
        if char in ("[", "{", "%"):
            return char * 2
        if char == "n":
            return "\n"
        if char.startswith("u") and match.group(2):
            return chr(int(match.group(2), 16))
        return char

    return re.sub(r"\\(u([0-9a-fA-F]{1,4})|.)", dequote, value)


def _quoted_at(source, start=0):
    """Return (Ren'Py-decoded text, end offset) for a quoted say string."""
    if start >= len(source) or source[start] not in ('"', "'"):
        raise ValidationError("Expected a quoted Ren'Py string.")
    quote = source[start]
    if source.startswith(quote * 3, start):
        raise ValidationError("Multiline literal source remains an opaque block.")
    index = start + 1
    while index < len(source):
        char = source[index]
        if char == quote:
            return _decode_renpy_string(source[start + 1:index]), index + 1
        if char in "\r\n":
            raise ValidationError("A single-line string was not terminated.")
        if char == "\\":
            index += 1
            if index >= len(source):
                break
        index += 1
    raise ValidationError("A quoted string was not terminated.")


def quote_text(value):
    value = _text(value, "Dialogue text", allow_newline=True)
    value = value.replace("\\", "\\\\").replace('"', '\\"').replace("\r", "\\u000d").replace("\n", "\\n").replace("\t", "\\u0009")
    # Preserve deliberately repeated spaces through Ren'Py's whitespace fold.
    value = re.sub(r" {2,}", lambda match: "\\ " * len(match.group()), value)
    return '"' + value + '"'


def _track(value):
    value = _text(value, "Track").strip()
    if value.startswith(('"', "'")):
        _, end = _quoted_at(value)
        try:
            decoded = ast.literal_eval(value)
        except (ValueError, SyntaxError):
            raise ValidationError("Track must be one quoted audio path.")
        if end != len(value) or not isinstance(decoded, str) or not decoded or any(ord(char) < 32 for char in decoded):
            raise ValidationError("Track must be one quoted audio path.")
        return value
    if not _TRACK_NAME.fullmatch(value):
        raise ValidationError("Track must be an audio alias or a quoted audio path.")
    return value


def _image(value):
    value = _text(value, "Image").strip()
    parts = value.split()
    if not parts or not _NAME.fullmatch(parts[0]) or not all(_ATTRIBUTE.fullmatch(p) for p in parts[1:]):
        raise ValidationError("Image must contain an image tag and attribute names.")
    if parts[0] in ("expression", "screen", "layer"):
        raise ValidationError("Image expressions, screens and layers remain outside this editor.")
    if any(part in _IMAGE_CLAUSE_WORDS for part in parts):
        raise ValidationError("Put placement, layer and transition clauses in their own fields.")
    return " ".join(parts)


def _atl(value):
    value = _text(value, "ATL", allow_newline=True)
    output = []
    for raw in value.splitlines():
        words = raw.strip().split()
        if not words:
            continue
        prefix = []
        if words[0] in _ATL_EASINGS:
            if len(words) < 4:
                raise ValidationError("An ATL easing needs a duration and property value.")
            prefix = [words.pop(0), _number(words.pop(0), "ATL duration", minimum=0)]
        if not words or len(words) % 2:
            raise ValidationError("ATL supports property/value pairs only.")
        values = []
        for index in range(0, len(words), 2):
            prop = words[index]
            if prop not in _ATL_PROPERTIES:
                raise ValidationError("Unsupported ATL property: %s" % prop)
            minimum = 0 if prop in ("alpha", "zoom") else None
            maximum = 1 if prop == "alpha" else None
            values.extend((prop, _number(words[index + 1], "ATL " + prop, minimum=minimum, maximum=maximum)))
        output.append(" ".join(prefix + values))
    return "\n".join(output)


def normalize_statement(kind, data):
    """Validate typed fields without evaluating any expression."""
    if not isinstance(data, dict):
        raise ValidationError("Statement fields must be a dictionary.")
    schemas = {
        "say": {"speaker", "text", "attributes"},
        "show": {"image", "at", "transition", "tag", "layer", "zorder", "behind", "atl"},
        "scene": {"image", "at", "transition", "tag", "layer", "zorder", "behind", "atl"},
        "hide": {"image", "transition", "layer"},
        "with": {"transition"}, "pause": {"duration"},
        "music": {"operation", "channel", "track", "fadein", "fadeout", "loop", "volume"},
        "nier_enter": set(), "nier_exit": set(), "nier_clear": set(),
    }
    if kind not in schemas:
        raise ValidationError("This statement kind cannot be edited.")
    unknown = set(data) - schemas[kind]
    if unknown:
        raise ValidationError("Unknown statement fields: " + ", ".join(sorted(unknown)))
    if kind == "say":
        speaker = _name(data.get("speaker", ""), "Speaker", optional=True)
        if speaker in _STATEMENT_WORDS:
            raise ValidationError("Choose a Character alias, not a Ren'Py statement keyword.")
        attributes = _text(data.get("attributes", ""), "Attributes").strip()
        if attributes and (not speaker or not all(_ATTRIBUTE.fullmatch(word) for word in attributes.split())):
            raise ValidationError("Dialogue attributes require a speaker and valid attribute names.")
        return {"speaker": speaker, "text": _text(data.get("text", ""), "Dialogue text", allow_newline=True), "attributes": " ".join(attributes.split())}
    if kind in ("show", "scene"):
        behind = _text(data.get("behind", ""), "Behind").strip()
        if behind:
            behind = ", ".join(_name(word.strip(), "Behind image tag") for word in behind.split(","))
        return {"image": _image(data.get("image", "")), "at": _expression(data.get("at", ""), "Transform", multiple=True),
                "transition": _expression(data.get("transition", ""), "Transition"),
                "tag": _name(data.get("tag", ""), "Image alias", optional=True),
                "layer": _name(data.get("layer", ""), "Layer", optional=True),
                "zorder": _number(data.get("zorder", ""), "Z-order", optional=True),
                "behind": behind, "atl": _atl(data.get("atl", ""))}
    if kind == "hide":
        return {"image": _name(data.get("image", ""), "Hidden image tag"),
                "transition": _expression(data.get("transition", ""), "Transition"),
                "layer": _name(data.get("layer", ""), "Layer", optional=True)}
    if kind == "with":
        return {"transition": _expression(data.get("transition", ""), "Transition", optional=False)}
    if kind == "pause":
        return {"duration": _number(data.get("duration", ""), "Pause duration", optional=True, minimum=0)}
    if kind == "music":
        operation = data.get("operation", "play")
        channel = data.get("channel", "music")
        loop = data.get("loop", "default")
        if operation not in ("play", "queue", "stop") or channel not in ("music", "sound", "voice"):
            raise ValidationError("Audio needs play, queue or stop and a supported channel.")
        if loop not in ("default", "loop", "noloop"):
            raise ValidationError("Loop must be default, loop or noloop.")
        result = {"operation": operation, "channel": channel, "track": "" if operation == "stop" else _track(data.get("track", "")),
                  "fadein": _number(data.get("fadein", ""), "Audio fade-in", optional=True, minimum=0),
                  "fadeout": _number(data.get("fadeout", ""), "Audio fade-out", optional=True, minimum=0),
                  "loop": loop, "volume": _number(data.get("volume", ""), "Audio volume", optional=True, minimum=0, maximum=1)}
        if operation == "stop" and (data.get("track", "") or result["fadein"] or result["volume"] or loop != "default"):
            raise ValidationError("Stop audio accepts fade-out only.")
        if operation == "queue" and result["fadeout"]:
            raise ValidationError("Queue does not accept fade-out.")
        return result
    return {}


def encode_statement(kind, data, indent="    ", newline="\n"):
    data = normalize_statement(kind, data)
    if not isinstance(indent, str) or indent.strip(" \t") or newline not in ("\n", "\r\n", "\r", ""):
        raise ValidationError("Invalid source indentation or line ending.")
    if kind == "say":
        prefix = " ".join(value for value in (data["speaker"], data["attributes"]) if value)
        statement = (prefix + " " if prefix else "") + quote_text(data["text"])
    elif kind in ("scene", "show"):
        statement = kind + " " + data["image"]
        for key, clause in (("tag", "as"), ("at", "at"), ("layer", "onlayer"), ("zorder", "zorder"), ("behind", "behind"), ("transition", "with")):
            if data[key]:
                statement += " " + clause + " " + data[key]
        if data["atl"]:
            if data["transition"]:
                raise ValidationError("Use a separate transition after an inline ATL block.")
            statement += ":" + (newline or "\n") + (newline or "\n").join(indent + "    " + line for line in data["atl"].splitlines())
    elif kind == "hide":
        statement = "hide " + data["image"]
        if data["layer"]:
            statement += " onlayer " + data["layer"]
        if data["transition"]:
            statement += " with " + data["transition"]
    elif kind == "with":
        statement = "with " + data["transition"]
    elif kind == "pause":
        statement = "pause" + (" " + data["duration"] if data["duration"] else "")
    elif kind == "music":
        statement = data["operation"] + " " + data["channel"]
        if data["track"]:
            statement += " " + data["track"]
        for key in ("fadein", "fadeout"):
            if data[key]:
                statement += " " + key + " " + data[key]
        if data["loop"] != "default":
            statement += " " + data["loop"]
        if data["volume"]:
            statement += " volume " + data["volume"]
    else:
        statement = "call " + kind
    return indent + statement + newline


class Block:
    def __init__(self, kind, raw, indent, line, data=None, branch=(), editable=False, uid=None, extra=None):
        self.uid = uid or _uid()
        self.kind = kind
        self.raw = raw
        self.indent = indent
        self.line = line
        self.data = data or {}
        self.branch = tuple(branch)
        self.editable = bool(editable)
        self.extra = extra or {}


def _indent(line):
    return line[:len(line) - len(line.lstrip(" \t"))]


def _line_ending(raw):
    return "\r\n" if raw.endswith("\r\n") else "\n" if raw.endswith("\n") else "\r" if raw.endswith("\r") else ""


def _comment(source):
    quote = None
    escape = False
    depth = 0
    for index, char in enumerate(source):
        if quote:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == quote:
                quote = None
        elif char in ('"', "'"):
            quote = char
        elif char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        elif char == "#" and depth == 0:
            before = source[:index]
            clean = before.rstrip()
            return clean, before[len(clean):] + source[index:]
    return source.rstrip(), source[len(source.rstrip()):]


def _logical_end(lines, start):
    """Find continuations and multiline literals, including opaque Python data."""
    quote = None
    triple = False
    escape = False
    depth = 0
    for line_index in range(start, len(lines)):
        line = lines[line_index]
        index = 0
        while index < len(line):
            char = line[index]
            if quote:
                if escape:
                    escape = False
                elif char == "\\":
                    escape = True
                elif triple and line.startswith(quote * 3, index):
                    quote = None
                    triple = False
                    index += 2
                elif not triple and char == quote:
                    quote = None
            elif char == "#":
                break
            elif char in ('"', "'"):
                quote = char
                triple = line.startswith(char * 3, index)
                if triple:
                    index += 2
            elif char in "([{":
                depth += 1
            elif char in ")]}":
                depth = max(0, depth - 1)
            index += 1
        if quote is None and depth == 0 and not line.rstrip("\r\n").endswith("\\"):
            return line_index + 1
        if quote is not None and not triple and not line.rstrip("\r\n").endswith("\\"):
            return line_index + 1
    return len(lines)


def _block_end(lines, start, columns):
    index = start + 1
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped and not stripped.startswith("#") and len(_indent(lines[index]).expandtabs(8)) <= columns:
            break
        # A multiline Python literal can contain visually unindented lines.
        # Advance over its complete logical statement before testing the next
        # indentation boundary, or the following story label can be swallowed.
        index = _logical_end(lines, index) if stripped and not stripped.startswith("#") else index + 1
    return index


def _clauses(source, allowed):
    matches = []
    quote = None
    escape = False
    depth = 0
    for match in re.finditer(r"\S+|\s+", source):
        token = match.group()
        if quote is None and depth == 0 and token in allowed:
            matches.append((match.start(), match.end(), token))
        for char in token:
            if quote:
                if escape:
                    escape = False
                elif char == "\\":
                    escape = True
                elif char == quote:
                    quote = None
            elif char in ('"', "'"):
                quote = char
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
    if not matches:
        return source.strip(), {}
    prefix = source[:matches[0][0]].strip()
    values = {}
    for index, (_, end, name) in enumerate(matches):
        if name in values:
            raise ValidationError("Duplicate source clause.")
        stop = matches[index + 1][0] if index + 1 < len(matches) else len(source)
        values[name] = source[end:stop].strip()
        if not values[name] and name not in ("loop", "noloop"):
            raise ValidationError("An empty source clause is unsupported.")
    return prefix, values


def _parse_statement(source):
    if source.startswith(("show ", "scene ", "hide ")):
        kind, rest = source.split(None, 1)
        image, clauses = _clauses(rest, {"at", "as", "onlayer", "zorder", "behind", "with"})
        mapping = {"at": "at", "as": "tag", "onlayer": "layer", "zorder": "zorder", "behind": "behind", "with": "transition"}
        data = {"image": image}
        data.update((mapping[key], value) for key, value in clauses.items())
        return kind, normalize_statement(kind, data), {}
    if source.startswith("with "):
        return "with", normalize_statement("with", {"transition": source[5:]}), {}
    if source == "pause" or source.startswith("pause "):
        return "pause", normalize_statement("pause", {"duration": source[5:].strip()}), {}
    nier = re.fullmatch(r"call (nier_enter|nier_exit|nier_clear)(?:\(\))?(?: from ([A-Za-z_]\w*))?", source)
    if nier:
        return nier.group(1), {}, {"call_suffix": source[len("call " + nier.group(1)):]} 
    audio = re.match(r"^(play|queue|stop)\s+(music|sound|voice)(?:\s+(.*))?$", source)
    if audio:
        track, clauses = _clauses(audio.group(3) or "", {"fadein", "fadeout", "volume", "loop", "noloop"})
        data = {"operation": audio.group(1), "channel": audio.group(2), "track": track}
        for key in ("fadein", "fadeout", "volume"):
            if key in clauses:
                data[key] = clauses[key]
        if "loop" in clauses and "noloop" in clauses:
            raise ValidationError("Conflicting loop clauses.")
        for key in ("loop", "noloop"):
            if key in clauses:
                if clauses[key]:
                    raise ValidationError("Unsupported audio loop clause.")
                data["loop"] = key
        return "music", normalize_statement("music", data), {}
    quote_index = next((i for i, char in enumerate(source) if char in ('"', "'")), -1)
    if quote_index >= 0:
        if quote_index and not source[quote_index - 1].isspace():
            raise ValidationError("Raw or prefixed string literals remain opaque.")
        prefix = source[:quote_index].strip().split()
        if prefix and (not _NAME.fullmatch(prefix[0]) or prefix[0] in ("define", "default", "return", "jump", "call", "voice", "window", "image")):
            raise ValidationError("Not a supported dialogue statement.")
        text, end = _quoted_at(source, quote_index)
        if source[end:].strip():
            raise ValidationError("Additional say clauses are not supported.")
        return "say", normalize_statement("say", {"speaker": prefix[0] if prefix else "", "attributes": " ".join(prefix[1:]), "text": text}), {}
    raise ValidationError("This statement is preserved as source.")


class StoryDocument:
    def __init__(self):
        self.path = ""
        self.blocks = []
        self.newline = "\n"
        self.bom = False
        self._base_bytes = b""
        self._undo = []
        self._redo = []
        self._unsaved = False
        # Bumped by every mutation so callers can cache derived views cheaply.
        self.revision = 0
        self._structure = 0
        self._positions_key = None
        self._positions_map = {}
        self._batch_depth = 0
        self._batch_checkpointed = False

    @classmethod
    def from_bytes(cls, data, path=""):
        if not isinstance(data, bytes) or len(data) > _MAX_SOURCE:
            raise ValidationError("Story source must be UTF-8 bytes under 32 MiB.")
        document = cls()
        document.path = os.path.abspath(os.fspath(path)) if path else ""
        document.bom = data.startswith(_BOM)
        try:
            source = data.decode("utf-8-sig")
        except UnicodeDecodeError as error:
            raise ValidationError("Story writer supports UTF-8 source only.") from error
        if "\x00" in source:
            raise ValidationError("Story source contains a NUL byte.")
        endings = re.findall(r"\r\n|\n|\r", source)
        if endings:
            document.newline = max(set(endings), key=endings.count)
        document._base_bytes = data
        document._parse(source)
        return document

    @classmethod
    def load(cls, path):
        with open(path, "rb") as stream:
            return cls.from_bytes(stream.read(_MAX_SOURCE + 1), path)

    @classmethod
    def new(cls, label="story_draft"):
        label = _name(label, "Label")
        document = cls.from_bytes(("label " + label + ":\n    return\n").encode("utf-8"))
        document._unsaved = True
        return document

    def _parse(self, source):
        lines = source.splitlines(keepends=True)
        index = 0
        stack = []
        while index < len(lines):
            line = lines[index]
            indent = _indent(line)
            columns = len(indent.expandtabs(8))
            clean, comment = _comment(line[len(indent):].rstrip("\r\n"))
            trivia = not clean
            if not trivia:
                while stack and columns <= stack[-1][0]:
                    stack.pop()
            ancestry = tuple(item[1] for item in stack)
            extra = {"comment": comment, "newline": _line_ending(line)}
            end = _logical_end(lines, index)
            kind, data, editable = "raw", {}, False
            push = False
            label = re.fullmatch(r"label\s+([A-Za-z_]\w*)(?:\([^\n]*\))?(?:\s+hide)?\s*:", clean)
            control = re.match(r"^(if\s+.+|elif\s+.+|else|menu(?:\s+.*)?)\s*:$", clean)
            choice = clean.startswith(('"', "'")) and clean.endswith(":") and any(item[2] == "branch" for item in stack)
            if end == index + 1 and label:
                kind, data, push = "label", {"name": label.group(1)}, True
            elif end == index + 1 and (control or choice):
                kind, data, push = "branch", {"header": clean}, True
            elif end == index + 1 and clean.startswith(("show ", "scene ")) and clean.endswith(":"):
                end = _block_end(lines, index, columns)
                body = lines[index + 1:end]
                try:
                    # Any comments or nested blocks in ATL stay opaque as a unit.
                    if not body or any(not b.strip() or b.lstrip().startswith("#") for b in body):
                        raise ValidationError("Complex ATL remains opaque.")
                    kind, data, details = _parse_statement(clean[:-1])
                    data["atl"] = _atl("\n".join(b.strip() for b in body))
                    data = normalize_statement(kind, data)
                    encode_statement(kind, data)
                    extra.update(details)
                    editable = True
                except ValidationError:
                    kind, data = "raw", {}
            elif end == index + 1 and clean.endswith(":") and not trivia:
                end = _block_end(lines, index, columns)
            elif end == index + 1 and not trivia:
                try:
                    kind, data, details = _parse_statement(clean)
                    extra.update(details)
                    editable = True
                except ValidationError:
                    pass
            raw = "".join(lines[index:end])
            extra["newline"] = _line_ending(raw)
            block = Block(kind, raw, indent, index + 1, data, ancestry, editable, extra=extra)
            self.blocks.append(block)
            if push:
                stack.append((columns, block.uid, kind))
            index = end

    def _positions(self, rebuild=False):
        blocks = self.blocks
        key = (len(blocks), self._structure)
        if rebuild or self._positions_key is None or self._positions_key[0] is not blocks or self._positions_key[1:] != key:
            self._positions_map = {block.uid: position for position, block in enumerate(blocks)}
            self._positions_key = (blocks,) + key
        return self._positions_map

    def index_of(self, uid):
        """Position of a block id in O(1); -1 when it is not in the document."""
        position = self._positions().get(uid)
        if position is None or position >= len(self.blocks) or self.blocks[position].uid != uid:
            # Confirm misses and stale hits against the list as it is now.
            position = self._positions(rebuild=True).get(uid)
        return -1 if position is None else position

    def get(self, uid):
        position = self.index_of(uid)
        return None if position < 0 else self.blocks[position]

    def _changed(self, structure=False):
        self.revision += 1
        if structure:
            self._structure += 1

    def _require(self, uid, editable=True):
        block = self.get(uid)
        if block is None:
            raise ValidationError("The selected story block no longer exists.")
        if editable and not block.editable:
            raise ValidationError("This source block is preserved and cannot be changed here.")
        return block

    def _snapshot(self):
        return copy.deepcopy(self.blocks)

    def _checkpoint(self):
        if self._batch_depth:
            # A batch is one undo step: keep only the state before its first change.
            if self._batch_checkpointed:
                return
            self._batch_checkpointed = True
        self._undo.append(self._snapshot())
        if len(self._undo) > 64:
            del self._undo[0]
        self._redo.clear()

    @contextlib.contextmanager
    def batch(self):
        """Group compound edits into one undo step; any failure restores the start."""
        if self._batch_depth:
            self._batch_depth += 1
            try:
                yield self
            finally:
                self._batch_depth -= 1
            return
        blocks = self._snapshot()
        undo, redo = list(self._undo), list(self._redo)
        self._batch_depth, self._batch_checkpointed = 1, False
        try:
            yield self
        except BaseException:
            self.blocks = blocks
            self._undo[:], self._redo[:] = undo, redo
            self._changed(structure=True)
            raise
        finally:
            self._batch_depth, self._batch_checkpointed = 0, False

    def _reline(self):
        line = 1
        for block in self.blocks:
            block.line = line
            line += len(re.findall(r"\r\n|\n|\r", block.raw))

    def _render(self, block, data):
        newline = block.extra.get("newline", self.newline)
        raw = encode_statement(block.kind, data, block.indent, newline)
        if block.kind.startswith("nier_") and block.extra.get("call_suffix"):
            raw = raw[:len(raw) - len(newline)] if newline else raw
            raw += block.extra["call_suffix"] + newline
        comment = block.extra.get("comment", "")
        if comment:
            lines = raw.splitlines(keepends=True)
            ending = _line_ending(lines[0])
            lines[0] = (lines[0][:-len(ending)] if ending else lines[0]) + comment + ending
            raw = "".join(lines)
        return raw

    def update(self, uid, data):
        block = self._require(uid)
        merged = dict(block.data)
        merged.update(data)
        normalized = normalize_statement(block.kind, merged)
        raw = self._render(block, normalized)
        if normalized == block.data:
            return block
        self._checkpoint()
        block.data = normalized
        block.raw = raw
        self._reline()
        self._changed()
        return block

    def insert_after(self, uid, kind, data):
        anchor = self._require(uid, editable=False)
        if not anchor.editable and anchor.kind != "label":
            raise ValidationError("Insert after an editable statement or a label.")
        indent = anchor.indent + "    " if anchor.kind == "label" else anchor.indent
        branch = anchor.branch + (anchor.uid,) if anchor.kind == "label" else anchor.branch
        normalized = normalize_statement(kind, data)
        raw = encode_statement(kind, normalized, indent, self.newline)
        block = Block(kind, raw, indent, anchor.line + 1, normalized, branch, True, extra={"newline": self.newline, "comment": ""})
        self._checkpoint()
        if anchor.raw and not _line_ending(anchor.raw):
            anchor.raw += self.newline
            anchor.extra["newline"] = self.newline
        self.blocks.insert(self.index_of(anchor.uid) + 1, block)
        self._reline()
        self._changed(structure=True)
        return block

    def delete(self, uid):
        block = self._require(uid)
        siblings = [item for item in self.blocks if item.branch == block.branch and item.editable]
        if len(siblings) <= 1 and block.branch:
            # Never create an empty Ren'Py suite; opaque executable siblings also count.
            executable = [item for item in self.blocks if item.branch == block.branch and item.uid != uid and not _trivia(item) and item.kind != "label"]
            if not executable:
                raise ValidationError("Deleting this statement would leave an empty branch.")
        self._checkpoint()
        del self.blocks[self.index_of(uid)]
        self._reline()
        self._changed(structure=True)
        return True

    def duplicate(self, uid):
        original = self._require(uid)
        duplicate = copy.deepcopy(original)
        duplicate.uid = _uid()
        # A copied call needs a fresh return-site identifier (or no explicit one).
        if duplicate.kind.startswith("nier_"):
            duplicate.extra.pop("call_suffix", None)
            duplicate.raw = self._render(duplicate, duplicate.data)
        self._checkpoint()
        if not _line_ending(original.raw):
            original.raw += self.newline
            original.extra["newline"] = self.newline
        self.blocks.insert(self.index_of(original.uid) + 1, duplicate)
        self._reline()
        self._changed(structure=True)
        return duplicate

    def move(self, uid, delta):
        block = self._require(uid)
        if type(delta) is not int or delta not in (-1, 1):
            raise ValidationError("Move one story block at a time.")
        index = self.index_of(uid)
        target = index + delta
        while 0 <= target < len(self.blocks) and _trivia(self.blocks[target]):
            target += delta
        if not 0 <= target < len(self.blocks):
            raise ValidationError("There is no adjacent editable statement.")
        neighbor = self.blocks[target]
        if not neighbor.editable or neighbor.branch != block.branch or neighbor.indent != block.indent:
            raise ValidationError("Story blocks cannot move across branches or preserved logic.")
        self._checkpoint()
        self.blocks[index], self.blocks[target] = self.blocks[target], self.blocks[index]
        # A formerly final line needs a delimiter after it moves into the file.
        for position, candidate in ((target, block), (index, neighbor)):
            if position != len(self.blocks) - 1 and not _line_ending(candidate.raw):
                candidate.raw += self.newline
                candidate.extra["newline"] = self.newline
        self._reline()
        self._changed(structure=True)
        return block

    def undo(self):
        if not self._undo:
            return False
        self._redo.append(self._snapshot())
        self.blocks = self._undo.pop()
        self._changed(structure=True)
        return True

    def redo(self):
        if not self._redo:
            return False
        self._undo.append(self._snapshot())
        self.blocks = self._redo.pop()
        self._changed(structure=True)
        return True

    def to_bytes(self):
        return (_BOM if self.bom else b"") + "".join(block.raw for block in self.blocks).encode("utf-8")

    @property
    def dirty(self):
        return self._unsaved or self.to_bytes() != self._base_bytes

    def draft_payload(self):
        return {"version": 1, "path": self.path, "base": base64.b64encode(self._base_bytes).decode("ascii"),
                "content": base64.b64encode(self.to_bytes()).decode("ascii"), "unsaved": self._unsaved}

    @classmethod
    def from_draft(cls, payload):
        if not isinstance(payload, dict) or payload.get("version") != 1:
            raise ValidationError("Unsupported story draft version.")
        try:
            for key in ("base", "content"):
                if not isinstance(payload[key], str) or len(payload[key]) > (_MAX_SOURCE * 4 // 3 + 8):
                    raise ValueError("Oversized draft.")
            baseline = base64.b64decode(payload["base"], validate=True)
            content = base64.b64decode(payload["content"], validate=True)
            path = _text(payload.get("path", ""), "Draft source path")
            document = cls.from_bytes(content, path)
            cls.from_bytes(baseline)
        except (KeyError, TypeError, ValueError) as error:
            raise ValidationError("The story draft is malformed.") from error
        document._base_bytes = baseline
        document._unsaved = bool(payload.get("unsaved", False))
        return document

    def save(self, path=None, validator=None, backup_dir=None, developer=True):
        """Validate bytes, detect outside edits, back up, then atomically replace.

        validator(bytes, absolute_path) must explicitly return True. The caller
        must additionally gate destination and backup paths to its workspace.
        """
        if not developer:
            raise PermissionError("Story source writes are developer-only.")
        if not callable(validator):
            raise ValidationError("A full-script validator is required before saving source.")
        destination = os.path.abspath(os.fspath(path or self.path)) if (path or self.path) else ""
        if not destination or os.path.splitext(destination)[1].lower() != ".rpy":
            raise ValidationError("Choose a .rpy source destination.")
        same_source = bool(self.path) and os.path.normcase(os.path.realpath(destination)) == os.path.normcase(os.path.realpath(self.path))
        expected = self._base_bytes if same_source and not self._unsaved else None

        def check_disk():
            try:
                with open(destination, "rb") as stream:
                    current = stream.read(_MAX_SOURCE + 1)
            except FileNotFoundError:
                if expected is not None:
                    raise ConflictError("The original story file was removed outside the writer.")
                return
            if expected is None or _fingerprint(current) != _fingerprint(expected):
                raise ConflictError("The story file changed outside the writer. Reload or save to a new file.")

        candidate = self.to_bytes()
        if len(candidate) > _MAX_SOURCE:
            raise ValidationError("Story source exceeds 32 MiB.")
        check_disk()
        if validator(candidate, destination) is not True:
            raise ValidationError("The candidate story failed full-script validation.")
        check_disk()
        parent = os.path.dirname(destination)
        if not os.path.isdir(parent):
            raise ValidationError("The source destination folder does not exist.")
        temporary = None
        try:
            descriptor, temporary = tempfile.mkstemp(prefix=".story-writer-", suffix=".tmp", dir=parent)
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(candidate)
                stream.flush()
                os.fsync(stream.fileno())
            if expected is not None:
                backups = os.path.abspath(os.fspath(backup_dir or os.path.join(parent, ".story_writer_backups")))
                os.makedirs(backups, exist_ok=True)
                stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
                backup = os.path.join(backups, os.path.basename(destination) + "." + stamp + "." + _fingerprint(expected)[:12] + ".bak")
                with open(backup, "xb") as stream:
                    stream.write(expected)
                    stream.flush()
                    os.fsync(stream.fileno())
            check_disk()
            os.replace(temporary, destination)
            temporary = None
        finally:
            if temporary is not None:
                try:
                    os.unlink(temporary)
                except FileNotFoundError:
                    pass
        self.path = destination
        self._base_bytes = candidate
        self._unsaved = False
        return destination


def _trivia(block):
    return block.kind == "raw" and all(not line.strip() or line.lstrip().startswith("#") for line in block.raw.splitlines())
