"""Demonstrate safe configuration handling without reading a secret file."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gtm_engine.config import read_bounded_int, read_secret
from gtm_engine.security import redact_sensitive_text


def main():
    limit = read_bounded_int("MAX_LEADS", 100, 1, 10000)
    print(f"Configured lead limit: {limit}")
    print("Example redaction: " + redact_sensitive_text(
        "Bearer synthetic-token email person@example.test"
    ))
    if "HUBSPOT_ACCESS_TOKEN" in os.environ:
        read_secret("HUBSPOT_ACCESS_TOKEN")
        print("HubSpot token is configured (value not displayed).")
    else:
        print("HubSpot token is optional for offline lessons.")


if __name__ == "__main__":
    main()
