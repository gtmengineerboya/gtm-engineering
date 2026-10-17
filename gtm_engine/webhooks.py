"""A local synthetic webhook receiver with SQLite event-id deduplication."""

from __future__ import annotations

import hmac
import hashlib
import json
import os
import re
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Request


MAX_BODY_BYTES = 64 * 1024
EVENT_ID_PATTERN = re.compile(r"^[A-Za-z0-9_.:-]{1,128}$")


def validate_event(payload: Any) -> dict[str, str]:
    if not isinstance(payload, dict):
        raise ValueError("Event must be a JSON object")
    event_id = payload.get("event_id")
    event_type = payload.get("event_type")
    if not isinstance(event_id, str) or not EVENT_ID_PATTERN.fullmatch(event_id):
        raise ValueError("event_id must be 1-128 safe characters")
    if (
        not isinstance(event_type, str)
        or not event_type.strip()
        or len(event_type) > 80
    ):
        raise ValueError("event_type must be 1-80 characters")
    return {"event_id": event_id, "event_type": event_type.strip()}


def record_event(database: Path, event: dict[str, str]) -> bool:
    database.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(database)) as connection:
        with connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS received_events (
                    event_id TEXT PRIMARY KEY,
                    event_type TEXT NOT NULL,
                    received_at_utc TEXT NOT NULL
                )"""
            )
            cursor = connection.execute(
                "INSERT OR IGNORE INTO received_events VALUES (?, ?, ?)",
                (
                    event["event_id"],
                    event["event_type"],
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            inserted = cursor.rowcount == 1
    return inserted


def verify_signature(body: bytes, supplied: str, secret: str) -> bool:
    expected = "sha256=" + hmac.new(
        secret.encode("utf-8"), body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, supplied or "")


def create_app(database: Path | None = None) -> FastAPI:
    app = FastAPI(title="Local GTM synthetic webhook")
    db_path = (
        database
        or Path(__file__).resolve().parents[1]
        / "day-24"
        / "webhook_events.sqlite3"
    )

    @app.post("/webhooks/events")
    async def receive_event(
        request: Request,
        x_webhook_signature: str | None = Header(default=None),
    ) -> dict[str, Any]:
        content_length = request.headers.get("content-length")
        try:
            declared_length = int(content_length) if content_length else 0
        except ValueError as exc:
            raise HTTPException(
                status_code=400, detail="Invalid Content-Length"
            ) from exc
        if declared_length > MAX_BODY_BYTES:
            raise HTTPException(status_code=413, detail="Payload too large")
        body_buffer = bytearray()
        async for chunk in request.stream():
            body_buffer.extend(chunk)
            if len(body_buffer) > MAX_BODY_BYTES:
                raise HTTPException(status_code=413, detail="Payload too large")
        body = bytes(body_buffer)

        expected = os.getenv("WEBHOOK_SHARED_SECRET")
        if expected:
            if not verify_signature(body, x_webhook_signature or "", expected):
                raise HTTPException(status_code=401, detail="Invalid signature")
        try:
            payload = json.loads(body)
            event = validate_event(payload)
        except (json.JSONDecodeError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        created = record_event(db_path, event)
        return {
            "event_id": event["event_id"],
            "status": "accepted" if created else "duplicate",
        }

    return app


app = create_app()
