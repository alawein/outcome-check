import hashlib
import json
import math
import re
from datetime import datetime
from fractions import Fraction
from pathlib import Path


class InputError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise InputError(message)


def fields(value: object, keys: set[str], label: str) -> None:
    require(type(value) is dict and set(value) == keys, f"invalid {label} fields")


def identifier(value: object, label: str) -> None:
    require(
        isinstance(value, str) and bool(value.strip()) and len(value) <= 200, f"invalid {label}"
    )


def timestamp(value: str) -> datetime:
    require(type(value) is str and len(value) <= 64, "invalid timestamp type")
    # Restrict to RFC3339 calendar date/time, seconds and explicit zone.
    require(
        bool(
            re.fullmatch(
                r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
                r"(?:\.[0-9]+)?(?:Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])",
                value,
            )
        ),
        "timestamp requires RFC3339 timezone",
    )
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise InputError("invalid timestamp") from exc
    require(result.utcoffset() is not None, "timezone required")
    return result


def age_seconds(as_of: str, observed_at: str) -> Fraction:
    """Compare every supplied fractional digit without float rounding."""
    now, observed = timestamp(as_of), timestamp(observed_at)
    delta = now.replace(microsecond=0) - observed.replace(microsecond=0)

    def fraction(value: str) -> Fraction:
        match = re.search(r"\.([0-9]+)", value)
        return Fraction("0." + match[1]) if match else Fraction(0)

    return Fraction(delta.days * 86400 + delta.seconds) + fraction(as_of) - fraction(observed_at)


def json_value(value: object, depth: int = 0) -> None:
    require(depth <= 32, "JSON nesting exceeds 32")
    if value is None or type(value) in (str, bool, int):
        return
    if type(value) is float:
        require(math.isfinite(value), "nonfinite value")
        return
    if type(value) is list:
        for child in value:
            json_value(child, depth + 1)
        return
    require(type(value) is dict, "invalid JSON value")
    for key, child in value.items():
        identifier(key, "state key")
        json_value(child, depth + 1)


def validate(packet: dict) -> None:
    fields(packet, {"schema_version", "as_of", "requirements", "actions", "observations"}, "packet")
    require(
        type(packet["schema_version"]) is int and packet["schema_version"] == 1,
        "schema_version must be 1",
    )
    timestamp(packet["as_of"])
    definitions = {
        "requirements": {
            "id",
            "subject",
            "path",
            "expected",
            "observation_id",
            "max_age_seconds",
            "action_id",
        },
        "actions": {"id", "status"},
        "observations": {"id", "subject", "observed_at", "state"},
    }
    for name, keys in definitions.items():
        entries = packet[name]
        require(type(entries) is list and len(entries) <= 10000, f"invalid {name} count")
        require(name != "requirements" or bool(entries), "requirements cannot be empty")
        seen = set()
        for row in entries:
            fields(row, keys, name)
            identifier(row["id"], name + " ID")
            require(row["id"] not in seen, f"duplicate {name} ID")
            seen.add(row["id"])
            if name == "actions":
                require(
                    row["status"] in ("succeeded", "failed", "unknown"), "invalid action status"
                )
            else:
                identifier(row["subject"], "subject")
            if name == "requirements":
                require(type(row["path"]) is list and 0 < len(row["path"]) <= 32, "invalid path")
                for key in row["path"]:
                    identifier(key, "path key")
                identifier(row["observation_id"], "observation reference")
                require(
                    type(row["max_age_seconds"]) is int and row["max_age_seconds"] >= 0,
                    "invalid max_age_seconds",
                )
                if row["action_id"] is not None:
                    identifier(row["action_id"], "action reference")
                json_value(row["expected"])
            if name == "observations":
                timestamp(row["observed_at"])
                require(type(row["state"]) is dict, "state must be object")
                json_value(row["state"])


def unique_pairs(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def invalid_constant(value: str) -> None:
    raise InputError(f"nonfinite number: {value}")


def load_packet(path: Path) -> tuple[dict, str]:
    with path.open("rb") as stream:
        raw = stream.read(5 * 1024 * 1024 + 1)
    require(len(raw) <= 5 * 1024 * 1024, "input exceeds 5 MiB")
    require(not raw.startswith(b"\xef\xbb\xbf"), "BOM forbidden")
    try:
        packet = json.loads(
            raw.decode("utf-8"), object_pairs_hook=unique_pairs, parse_constant=invalid_constant
        )
        validate(packet)
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise InputError(str(exc)) from exc
    return packet, hashlib.sha256(raw).hexdigest()
