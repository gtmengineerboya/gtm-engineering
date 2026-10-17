"""Day 15 import surface for the reusable HTTP reliability helper."""

import requests

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gtm_engine.http_client import request_with_retries

__all__ = ["request_with_retries"]


class DemoSession:
    """Simulate a temporary server error, then a successful response."""

    def __init__(self):
        self.calls = 0

    def request(self, method, url, **kwargs):
        self.calls += 1
        response = requests.Response()
        response.status_code = 503 if self.calls == 1 else 200
        response._content = b'{"ok": true}'
        response.headers = {}
        return response


def main():
    session = DemoSession()
    response = request_with_retries(
        "GET",
        "https://example.test/demo",
        session=session,
        sleep=lambda _: None,
    )
    print(f"Final status: {response.status_code}; attempts: {session.calls}")


if __name__ == "__main__":
    main()
