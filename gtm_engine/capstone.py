"""Offline end-to-end GTM practice using only synthetic input data."""

from __future__ import annotations

import csv
import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from gtm_engine.crm import dry_run_plan, validate_and_normalize
from gtm_engine.config import read_bounded_int
from gtm_engine.funnel import route
from gtm_engine.outreach import evaluate_message
from gtm_engine.metrics import calculate_metrics
from gtm_engine.research import research_with_ollama


def score_record(record: dict[str, str]) -> int:
    score = 0
    if record.get("industry", "").casefold() in {"saas", "software"}:
        score += 30
    raw_employees = record.get("employees", "").replace(",", "").strip()
    if not raw_employees.isdigit():
        raise ValueError("employees must be a non-negative integer")
    employees = int(raw_employees)
    if employees >= 100:
        score += 20
    if record.get("country", "").casefold() in {
        "usa", "united states", "us", "canada",
    }:
        score += 15
    if record.get("buying_signal", "").strip().casefold() == "demo request":
        score += 35
    return min(score, 100)


def build_draft(record: dict[str, str]) -> str:
    name = record["company_name"]
    industry = record.get("industry", "unknown")
    country = record.get("country", "unknown")
    return (
        f"Hi {name}, your supplied profile lists {industry} and {country}. "
        "I would welcome a conversation to learn about your current go-to-market "
        "priorities and explore whether our workflow approach could be relevant. "
        "Would you be open to a brief introductory discussion next week?"
    )


def run_capstone(
    input_path: Path,
    output_dir: Path,
    *,
    use_ollama: bool = False,
) -> dict[str, Any]:
    started = time.monotonic()
    max_leads = read_bounded_int("MAX_LEADS", 100, 1, 1000)
    with input_path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        leads = []
        for row in reader:
            if len(leads) >= max_leads:
                raise ValueError(
                    f"Capstone input exceeds the configured limit of "
                    f"{max_leads} leads"
                )
            leads.append(row)
    if not leads:
        raise ValueError("Synthetic input has no lead rows")

    report_rows = []
    for raw in leads:
        record = validate_and_normalize(raw)
        record["icp_score"] = str(score_record(record))
        routed = route(record)
        research = research_with_ollama(
            {
                **record,
                "icp_score": record["icp_score"],
                "employee_segment": record.get("employee_segment", ""),
            },
            enabled=use_ollama,
        )
        message = build_draft(record)
        quality = evaluate_message(
            record["company_name"],
            message,
            [record.get("industry", ""), record.get("country", "")],
        )
        crm_plan = dry_run_plan([record])[0]
        report_rows.append({
            "company_name": record["company_name"],
            "email": record["email"],
            "icp_score": record["icp_score"],
            "lifecycle_stage": routed["lifecycle_stage"],
            "owner_queue": routed["owner_queue"],
            "routing_reason": routed["routing_reason"],
            "research_facts_count": len(research["observed_facts"]),
            "research_hypotheses_count": len(research["hypotheses"]),
            "research_facts": json.dumps(
                research["observed_facts"], ensure_ascii=True
            ),
            "research_hypotheses": json.dumps(
                research["hypotheses"], ensure_ascii=True
            ),
            "research_limitations": json.dumps(
                research["limitations"], ensure_ascii=True
            ),
            "enrichment_source": "synthetic_profile_normalized_locally",
            "outreach_message": message,
            "outreach_quality_status": quality["status"],
            "approval_status": "HUMAN_APPROVAL_REQUIRED",
            "crm_plan": crm_plan["planned_contact_operation"],
            "crm_mode": "DRY_RUN",
            "message_sent": "NO",
        })

    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "capstone_report.csv"
    with report_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(report_rows[0]))
        writer.writeheader()
        writer.writerows(report_rows)
    run_log = {
        "run_id": str(uuid.uuid4()),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": "SUCCESS",
        "leads_processed": len(report_rows),
        "human_approval_required": len(report_rows),
        "crm_writes": 0,
        "messages_sent": 0,
        "duration_seconds": round(time.monotonic() - started, 4),
        "pipeline_metrics": calculate_metrics({
            "funnel_counts": {
                stage.casefold(): sum(
                    row["lifecycle_stage"] == stage for row in report_rows
                )
                for stage in ("Lead", "MQL", "SQL", "Opportunity", "Customer")
            },
        }),
    }
    (output_dir / "run_summary.json").write_text(
        json.dumps(run_log, indent=2), encoding="utf-8"
    )
    return {"report": report_path, **run_log}
