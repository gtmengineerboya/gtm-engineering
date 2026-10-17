"""Deterministic lifecycle qualification and territory/segment routing."""

from __future__ import annotations


STAGES = ("Lead", "MQL", "SQL", "Opportunity", "Customer")


def qualify(record: dict[str, str]) -> tuple[str, str]:
    try:
        score = int(record.get("icp_score", ""))
    except (TypeError, ValueError):
        return "Lead", "Missing or invalid ICP score"
    if score < 0 or score > 100:
        return "Lead", "ICP score must be between 0 and 100"
    if record.get("buying_signal", "").strip().casefold() == "demo request":
        return "SQL", "Explicit demo request"
    if score >= 70:
        return "MQL", "ICP score is at least 70"
    if score >= 45:
        return "Lead", "Score is below the MQL threshold"
    return "Lead", "Not currently qualified"


def route(record: dict[str, str]) -> dict[str, str]:
    stage, reason = qualify(record)
    country = (record.get("country") or "").strip().casefold()
    segment = (record.get("employee_segment") or "").strip().casefold()
    if stage == "Lead":
        owner = "Unassigned - needs review"
    elif country in {"usa", "united states", "us"}:
        owner = "North America - " + (segment or "general")
    elif country in {"uk", "united kingdom", "germany", "france"}:
        owner = "EMEA - " + (segment or "general")
    else:
        owner = "International - " + (segment or "general")
    return {**record, "lifecycle_stage": stage, "owner_queue": owner,
            "routing_reason": reason}
