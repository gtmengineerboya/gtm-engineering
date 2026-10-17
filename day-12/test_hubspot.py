import os
from unittest.mock import Mock, patch

import pytest
import requests


COMPANIES_URL = "https://api.hubapi.com/crm/v3/objects/companies"


def get_companies(token=None):
    token = token or os.getenv("HUBSPOT_TOKEN")
    if not token:
        raise RuntimeError("HUBSPOT_TOKEN is not set")

    return requests.get(
        COMPANIES_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        params={"limit": 3},
        timeout=30,
    )


def main():
    response = get_companies()
    print("HTTP Status:", response.status_code)

    if response.ok:
        data = response.json()
        print("HubSpot connection successful")
        print("Companies returned:", len(data.get("results", [])))
    else:
        print("HubSpot API request failed")
        print("Response status:", response.status_code)


def test_connection_uses_mocked_http_without_printing_token(monkeypatch, capsys):
    token = "unit-test-token"
    monkeypatch.setenv("HUBSPOT_TOKEN", token)
    response = Mock(status_code=200, ok=True)
    response.json.return_value = {"results": [{}, {}, {}]}

    with patch("requests.get", return_value=response) as get:
        main()

    get.assert_called_once_with(
        COMPANIES_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        params={"limit": 3},
        timeout=30,
    )
    output = capsys.readouterr().out
    assert "Companies returned: 3" in output
    assert token not in output


def test_missing_token_fails_only_when_connection_is_requested(monkeypatch):
    monkeypatch.delenv("HUBSPOT_TOKEN", raising=False)

    with pytest.raises(RuntimeError, match="HUBSPOT_TOKEN is not set"):
        get_companies()


@pytest.mark.integration
def test_live_hubspot_connection_when_token_is_available():
    token = os.getenv("HUBSPOT_TOKEN")
    if not token:
        pytest.skip("HUBSPOT_TOKEN is not set")

    response = get_companies(token)
    assert response.ok, (
        f"HubSpot companies endpoint returned HTTP {response.status_code}"
    )


if __name__ == "__main__":
    main()
