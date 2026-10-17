"""Run the local webhook receiver on loopback only."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gtm_engine.webhooks import app

__all__ = ["app"]
