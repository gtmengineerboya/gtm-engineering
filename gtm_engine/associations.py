"""Explicitly configured HubSpot contact/company association operations."""

from __future__ import annotations

from typing import Any, Protocol


class AssociationClient(Protocol):
    def verify_objects(self, contact_id: str, company_id: str) -> None: ...
    def associate(self, contact_id: str, company_id: str,
                  category: str, type_id: int) -> None: ...
    def read_associations(self, contact_id: str) -> list[dict[str, Any]]: ...


def association_plan(
    contact_id: str,
    company_id: str,
    category: str | None,
    type_id: int | None,
    *,
    live: bool = False,
) -> dict[str, str]:
    if not contact_id or not company_id:
        raise ValueError("Contact and company IDs are required")
    if live and (not category or type_id is None):
        raise ValueError(
            "Inspect the live HubSpot association schema and supply its "
            "category and type ID; this lesson will not guess them."
        )
    return {
        "contact_id": contact_id,
        "company_id": company_id,
        "association_category": category or "UNCONFIGURED - inspect schema",
        "association_type_id": (
            str(type_id) if type_id is not None
            else "UNCONFIGURED - inspect schema"
        ),
        "mode": "DRY_RUN",
    }


def associate_and_verify(
    client: AssociationClient,
    contact_id: str,
    company_id: str,
    category: str,
    type_id: int,
) -> str:
    client.verify_objects(contact_id, company_id)
    client.associate(contact_id, company_id, category, type_id)
    associations = client.read_associations(contact_id)
    if not any(str(item.get("id")) == str(company_id) for item in associations):
        raise RuntimeError("HubSpot read-back did not include the company")
    return "VERIFIED"
