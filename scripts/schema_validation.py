"""Small, strict JSON Schema subset for the repository's offline contracts.

This is not a general JSON Schema implementation. Supported assertion keywords:
type, enum, const, required, properties, additionalProperties, items, minItems,
maxItems, uniqueItems, minLength, maxLength, pattern, minimum, maximum,
exclusiveMinimum, exclusiveMaximum, oneOf, anyOf, allOf, and format (date,
date-time, uri). Local JSON pointers and caller-resolved document refs work.
Unknown keywords and formats fail closed; there is no network resolver.
Date-time accepts calendar-valid RFC 3339 timestamps except leap seconds.
"""
from __future__ import annotations

from datetime import date, datetime
import math
import re
from urllib.parse import unquote, urlsplit


class SchemaValidationError(ValueError):
    """An instance does not satisfy the supported schema contract."""


class UnsupportedSchemaError(ValueError):
    """A schema is invalid or uses a keyword this validator does not enforce."""


ASSERTIONS = {
    "$ref", "type", "enum", "const", "required", "properties", "additionalProperties",
    "items", "minItems", "maxItems", "uniqueItems", "minLength", "maxLength", "pattern",
    "minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "oneOf", "anyOf", "allOf", "format",
}
ANNOTATIONS = {"$schema", "$id", "$defs", "title", "description", "default", "examples", "deprecated", "readOnly", "writeOnly"}
TYPES = {"object", "array", "string", "number", "integer", "boolean", "null"}
TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)\Z")


def _inspect(schema, seen=None):
    if isinstance(schema, bool):
        return
    if not isinstance(schema, dict):
        raise UnsupportedSchemaError("A schema must be an object or boolean")
    seen = set() if seen is None else seen
    if id(schema) in seen:
        return
    seen.add(id(schema))
    unknown = set(schema) - ASSERTIONS - ANNOTATIONS
    if unknown:
        raise UnsupportedSchemaError("Unsupported schema keyword(s): " + ", ".join(sorted(unknown)))
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not types or any(not isinstance(t, str) or t not in TYPES for t in types):
            raise UnsupportedSchemaError("Invalid schema type")
    for name in ("properties", "$defs"):
        if name in schema:
            if not isinstance(schema[name], dict) or any(not isinstance(k, str) for k in schema[name]):
                raise UnsupportedSchemaError(f"{name} must be an object")
            for child in schema[name].values():
                _inspect(child, seen)
    for name in ("items", "additionalProperties"):
        if name in schema:
            _inspect(schema[name], seen)
    for name in ("oneOf", "anyOf", "allOf"):
        if name in schema:
            if not isinstance(schema[name], list) or not schema[name]:
                raise UnsupportedSchemaError(f"{name} needs a nonempty schema array")
            for child in schema[name]:
                _inspect(child, seen)
    if "required" in schema and (not isinstance(schema["required"], list)
                                  or any(not isinstance(v, str) for v in schema["required"])
                                  or len(set(schema["required"])) != len(schema["required"])):
        raise UnsupportedSchemaError("required must contain unique property names")
    for name in ("minItems", "maxItems", "minLength", "maxLength"):
        if name in schema and (type(schema[name]) is not int or schema[name] < 0):
            raise UnsupportedSchemaError(f"{name} must be a nonnegative integer")
    for name in ("minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum"):
        if name in schema and (type(schema[name]) not in (int, float) or not math.isfinite(schema[name])):
            raise UnsupportedSchemaError(f"{name} must be finite")
    if "uniqueItems" in schema and type(schema["uniqueItems"]) is not bool:
        raise UnsupportedSchemaError("uniqueItems must be boolean")
    if "enum" in schema and (not isinstance(schema["enum"], list) or not schema["enum"]):
        raise UnsupportedSchemaError("enum must be a nonempty array")
    if "format" in schema and schema["format"] not in {"date", "date-time", "uri"}:
        raise UnsupportedSchemaError("Unsupported schema format")
    if "$ref" in schema and not isinstance(schema["$ref"], str):
        raise UnsupportedSchemaError("$ref must be a string")
    if "pattern" in schema:
        if not isinstance(schema["pattern"], str):
            raise UnsupportedSchemaError("pattern must be a string")
        try:
            re.compile(schema["pattern"])
        except re.error as exc:
            raise UnsupportedSchemaError("Invalid schema pattern") from exc


def _json_value(value, depth=0):
    if depth > 100:
        raise SchemaValidationError("JSON nesting exceeds the supported 100 levels")
    if value is None or type(value) in (str, bool, int):
        return
    if type(value) is float and math.isfinite(value):
        return
    if isinstance(value, list):
        for item in value:
            _json_value(item, depth + 1)
        return
    if isinstance(value, dict) and all(isinstance(k, str) for k in value):
        for item in value.values():
            _json_value(item, depth + 1)
        return
    raise SchemaValidationError("Expected a finite JSON-compatible value")


def _same(a, b):
    # JSON booleans are not numbers; Python's True == 1 must not satisfy const.
    if type(a) is bool or type(b) is bool:
        return type(a) is type(b) and a == b
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_same(a[k], b[k]) for k in a)
    return a == b


def _frozen(value):
    if isinstance(value, dict):
        return ("object", tuple((key, _frozen(value[key])) for key in sorted(value)))
    if isinstance(value, list):
        return ("array", tuple(_frozen(item) for item in value))
    if type(value) in (int, float):
        return ("number", value)
    return (type(value).__name__, value)


def _type(value, expected):
    return {"object": isinstance(value, dict), "array": isinstance(value, list),
            "string": isinstance(value, str), "number": type(value) in (int, float),
            "integer": type(value) is int or (type(value) is float and value.is_integer()),
            "boolean": type(value) is bool, "null": value is None}[expected]


def _format(value, kind):
    try:
        if kind == "date":
            return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)) and bool(date.fromisoformat(value))
        if kind == "date-time":
            return bool(TIMESTAMP.fullmatch(value)) and datetime.fromisoformat(value.replace("Z", "+00:00")).utcoffset() is not None
        parsed = urlsplit(value)
        return bool(re.fullmatch(r"[A-Za-z][A-Za-z0-9+.-]*", parsed.scheme)) and not re.search(r"[\s\x00-\x1f]", value) and (parsed.scheme not in {"http", "https"} or bool(parsed.netloc))
    except ValueError:
        return False


def _resolve(ref, root, resolver):
    document, _, fragment = ref.partition("#")
    if document:
        if resolver is None:
            raise UnsupportedSchemaError("Document refs require an explicit local resolver")
        root = resolver(document)
        _inspect(root)
    current = root
    if fragment:
        fragment = unquote(fragment)
        if not fragment.startswith("/"):
            raise UnsupportedSchemaError("Only JSON-pointer ref fragments are supported")
        try:
            for token in fragment[1:].split("/"):
                token = token.replace("~1", "/").replace("~0", "~")
                current = current[int(token)] if isinstance(current, list) else current[token]
        except (KeyError, IndexError, ValueError, TypeError) as exc:
            raise UnsupportedSchemaError("Unresolved local schema ref") from exc
    return current, root


def _walk(value, schema, root, resolver, path, depth=0):
    if depth > 100:
        raise UnsupportedSchemaError("Schema recursion exceeds the supported 100 levels")
    if schema is True:
        return
    if schema is False:
        raise SchemaValidationError(f"{path}: disallowed by schema")
    if "$ref" in schema:
        target, target_root = _resolve(schema["$ref"], root, resolver)
        _walk(value, target, target_root, resolver, path, depth + 1)
    if "type" in schema:
        kinds = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_type(value, kind) for kind in kinds):
            raise SchemaValidationError(f"{path}: expected {' or '.join(kinds)}")
    if "const" in schema and not _same(value, schema["const"]):
        raise SchemaValidationError(f"{path}: const mismatch")
    if "enum" in schema and not any(_same(value, choice) for choice in schema["enum"]):
        raise SchemaValidationError(f"{path}: value outside enum")
    for name in ("oneOf", "anyOf", "allOf"):
        if name not in schema:
            continue
        matched = 0
        for child in schema[name]:
            try:
                _walk(value, child, root, resolver, path, depth + 1)
                matched += 1
            except SchemaValidationError:
                pass
        if (name == "oneOf" and matched != 1) or (name == "anyOf" and matched == 0) or (name == "allOf" and matched != len(schema[name])):
            raise SchemaValidationError(f"{path}: {name} contract not satisfied")
    if isinstance(value, dict):
        missing = set(schema.get("required", [])) - value.keys()
        if missing:
            raise SchemaValidationError(f"{path}: missing {', '.join(sorted(missing))}")
        properties = schema.get("properties", {})
        for key, item in value.items():
            child = properties.get(key, schema.get("additionalProperties", True))
            _walk(item, child, root, resolver, f"{path}/{key}", depth + 1)
    elif isinstance(value, list):
        if len(value) < schema.get("minItems", 0) or len(value) > schema.get("maxItems", math.inf):
            raise SchemaValidationError(f"{path}: array length outside bounds")
        if schema.get("uniqueItems") and len({_frozen(item) for item in value}) != len(value):
            raise SchemaValidationError(f"{path}: array items must be unique")
        for index, item in enumerate(value):
            _walk(item, schema.get("items", True), root, resolver, f"{path}/{index}", depth + 1)
    elif isinstance(value, str):
        if len(value) < schema.get("minLength", 0) or len(value) > schema.get("maxLength", math.inf):
            raise SchemaValidationError(f"{path}: string length outside bounds")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            raise SchemaValidationError(f"{path}: pattern mismatch")
        if "format" in schema and not _format(value, schema["format"]):
            raise SchemaValidationError(f"{path}: invalid {schema['format']}")
    elif type(value) in (int, float):
        for key, fails in (("minimum", lambda n: value < n), ("maximum", lambda n: value > n),
                           ("exclusiveMinimum", lambda n: value <= n), ("exclusiveMaximum", lambda n: value >= n)):
            if key in schema and fails(schema[key]):
                raise SchemaValidationError(f"{path}: outside {key}")


def validate(instance, schema, root_schema=None, *, resolver=None):
    """Validate JSON data; raise a typed ValueError, return None on success.

    `resolver(document)` must return a local schema dictionary and is never
    called for an in-document ref. This module opens no files and no network.
    """
    _json_value(instance)
    _inspect(schema)
    root = schema if root_schema is None else root_schema
    _inspect(root)
    _walk(instance, schema, root, resolver, "$", 0)
