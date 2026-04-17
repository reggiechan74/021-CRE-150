"""Stdlib replacements for the subset of pydantic we need.

Three small primitives are enough for cam-reconciliation-cre:

- ValidationError: raised on unknown, missing, or bad-typed input fields.
- ManifestJSONEncoder: JSON encoder that knows how to serialize Decimal,
  datetime/date, Enum, and dataclass instances.
- check_unknown_keys: replaces pydantic's ``ConfigDict(extra="forbid")``
  at the Manifest root.

We deliberately do not ship a generic ``from_dict`` coercion engine.
Each dataclass writes its own explicit classmethod that names its fields
and coerces at the field level. See plan-rewrite-cam-reconciliation-cre.md
Step 2 for the rationale.
"""

from __future__ import annotations

import json
from dataclasses import fields, is_dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum


class ValidationError(ValueError):
    """Raised on unknown fields, missing required fields, or bad types."""


class ManifestJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        if isinstance(o, Enum):
            return o.value
        if is_dataclass(o):
            return {f.name: getattr(o, f.name) for f in fields(o)}
        return super().default(o)


def check_unknown_keys(cls, data, known_keys) -> None:
    unknown = set(data) - set(known_keys)
    if unknown:
        raise ValidationError(
            f"{cls.__name__} got unknown fields: {sorted(unknown)}"
        )
