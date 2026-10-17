"""A small requests-based HTTP client with bounded, safe retries."""

from __future__ import annotations

import time
from collections.abc import Callable
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone
from typing import Any

import requests


RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
RETRYABLE_METHODS = {"GET", "HEAD", "OPTIONS", "PUT", "DELETE"}


def _retry_after_seconds(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return max(0.0, min(float(value), 30.0))
    except ValueError:
        try:
            retry_at = parsedate_to_datetime(value)
            if retry_at.tzinfo is None:
                retry_at = retry_at.replace(tzinfo=timezone.utc)
            return max(
                0.0,
                min((retry_at - datetime.now(timezone.utc)).total_seconds(), 30.0),
            )
        except (TypeError, ValueError, OverflowError):
            return None


def request_with_retries(
    method: str,
    url: str,
    *,
    session: requests.Session | None = None,
    timeout: float = 15.0,
    max_attempts: int = 3,
    backoff_seconds: float = 0.5,
    sleep: Callable[[float], None] = time.sleep,
    **kwargs: Any,
) -> requests.Response:
    """Send a request and retry only transient failures with safe semantics.

    POST is retried only when the caller supplies an Idempotency-Key header.
    The final response/error is returned/raised by requests, not hidden.
    """
    if timeout <= 0 or max_attempts < 1 or backoff_seconds < 0:
        raise ValueError(
            "timeout and max_attempts must be positive; "
            "backoff must be non-negative"
        )
    client = session if session is not None else requests
    verb = method.upper()
    headers = kwargs.get("headers") or {}
    has_idempotency_key = any(
        key.lower() == "idempotency-key" and str(value).strip()
        for key, value in headers.items()
    )
    can_retry = verb in RETRYABLE_METHODS or (
        verb == "POST" and has_idempotency_key
    )

    for attempt in range(1, max_attempts + 1):
        try:
            response = client.request(
                verb, url, timeout=timeout, **kwargs
            )
        except (requests.Timeout, requests.ConnectionError):
            if not can_retry or attempt == max_attempts:
                raise
            sleep(backoff_seconds * (2 ** (attempt - 1)))
            continue

        if response.status_code not in RETRYABLE_STATUS_CODES:
            response.raise_for_status()
            return response
        if not can_retry or attempt == max_attempts:
            response.raise_for_status()

        retry_after = _retry_after_seconds(
            response.headers.get("Retry-After")
        )
        delay = retry_after
        if delay is None:
            delay = backoff_seconds * (2 ** (attempt - 1))
        sleep(delay)

    raise RuntimeError("HTTP retry loop exited unexpectedly")
