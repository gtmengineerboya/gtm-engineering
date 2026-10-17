"""Safe configuration readers that never echo secret values."""

from __future__ import annotations

import os
from collections.abc import Mapping


PLACEHOLDER_MARKERS = ("your_", "replace_me", "placeholder", "<")


def read_secret(
    name: str, environ: Mapping[str, str] | None = None
) -> str:
    values = environ if environ is not None else os.environ
    value = values.get(name, "").strip()
    if not value:
        raise ValueError(f"Required environment variable {name} is missing")
    if any(marker in value.casefold() for marker in PLACEHOLDER_MARKERS):
        raise ValueError(
            f"Environment variable {name} still contains a placeholder"
        )
    return value


def read_bounded_int(
    name: str,
    default: int,
    minimum: int,
    maximum: int,
    environ: Mapping[str, str] | None = None,
) -> int:
    values = environ if environ is not None else os.environ
    raw = values.get(name)
    if raw is None:
        value = default
    else:
        try:
            value = int(raw)
        except ValueError as exc:
            raise ValueError(f"{name} must be an integer") from exc
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")
    return value
