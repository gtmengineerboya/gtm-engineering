"""Trigger Day 13 exactly once, then poll the status of that same run."""

from __future__ import annotations

import argparse
import time
from urllib.parse import quote

import requests


def run_pipeline(
    base_url: str = "http://127.0.0.1:8000",
    timeout_seconds: int = 900,
    poll_seconds: float = 3.0,
    session: requests.Session | None = None,
) -> dict:
    if timeout_seconds <= 0 or poll_seconds <= 0:
        raise ValueError("Polling timeout and interval must be positive")
    client = session or requests.Session()
    started = time.monotonic()
    trigger = client.post(
        base_url.rstrip("/") + "/run-pipeline", timeout=10
    )
    trigger.raise_for_status()
    run_id = trigger.json()["run_id"]
    status_url = (
        base_url.rstrip("/") + "/run-status/" + quote(str(run_id), safe="")
    )
    while time.monotonic() - started < timeout_seconds:
        response = client.get(status_url, timeout=10)
        response.raise_for_status()
        result = response.json()
        if result.get("status") in {"success", "failed"}:
            return result
        if result.get("status") != "running":
            raise RuntimeError(f"Unexpected pipeline status: {result!r}")
        time.sleep(poll_seconds)
    raise TimeoutError(
        f"Pipeline run {run_id} did not finish within {timeout_seconds}s"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args()
    result = run_pipeline(args.base_url, timeout_seconds=args.timeout)
    print(result)
    if result.get("status") != "success":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
