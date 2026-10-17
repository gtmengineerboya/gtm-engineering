"""Small redaction helpers for logs and operational status output."""

from __future__ import annotations

import re


_SECRET_PATTERNS = (
    (re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+"), "Bearer [REDACTED]"),
    (re.compile(r"\bpat-[A-Za-z0-9_-]{12,}\b"), "[REDACTED_TOKEN]"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{12,}\b"), "[REDACTED_TOKEN]"),
    (
        re.compile(r"(?i)\b(token|api[_-]?key|password|secret)\s*[:=]\s*\S+"),
        r"\1=[REDACTED]",
    ),
    (
        re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        "[REDACTED_EMAIL]",
    ),
)


def redact_sensitive_text(value: str) -> str:
    result = str(value or "")
    for pattern, replacement in _SECRET_PATTERNS:
        result = pattern.sub(replacement, result)
    return result
