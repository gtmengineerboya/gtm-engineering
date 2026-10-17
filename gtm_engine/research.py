"""Structured, evidence-constrained company research with an offline fallback."""

from __future__ import annotations

import json
from typing import Any, Callable

import requests


FACT_FIELDS = (
    "company_name", "industry", "country", "employees",
    "employee_segment", "technology", "icp_score",
)


def fallback_research(record: dict[str, Any], reason: str) -> dict[str, Any]:
    facts = [
        {"field": field, "value": str(record[field])}
        for field in FACT_FIELDS
        if record.get(field) not in (None, "")
    ]
    return {
        "observed_facts": facts,
        "hypotheses": [],
        "confidence": 0.0,
        "sources": [fact["field"] for fact in facts],
        "limitations": ["Only supplied synthetic input fields were used."],
        "fallback_reason": reason,
    }


def validate_research(
    result: dict[str, Any], record: dict[str, Any]
) -> dict[str, Any]:
    if not isinstance(result, dict):
        raise ValueError("Research output must be a JSON object")
    facts = result.get("observed_facts")
    hypotheses = result.get("hypotheses")
    confidence = result.get("confidence")
    limitations = result.get("limitations")
    sources = result.get("sources")
    if not all(isinstance(value, list) for value in
               (facts, hypotheses, limitations, sources)):
        raise ValueError("Research lists are missing or invalid")
    if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        raise ValueError("confidence must be between 0 and 1")
    for fact in facts:
        if not isinstance(fact, dict):
            raise ValueError("Observed facts must be objects")
        field = fact.get("field")
        if field not in FACT_FIELDS or str(record.get(field, "")) != str(
            fact.get("value", "")
        ):
            raise ValueError("Observed fact is not supported by the input")
    available_fields = {
        field for field in FACT_FIELDS if record.get(field) not in (None, "")
    }
    for hypothesis in hypotheses:
        if (
            not isinstance(hypothesis, dict)
            or hypothesis.get("label") != "hypothesis"
            or not isinstance(hypothesis.get("claim"), str)
            or not isinstance(hypothesis.get("evidence_fields"), list)
        ):
            raise ValueError("Each hypothesis needs a label, claim, and evidence")
        if (
            not hypothesis["evidence_fields"]
            or not set(hypothesis["evidence_fields"]).issubset(available_fields)
        ):
            raise ValueError(
                "Hypothesis must cite fields present in the input record"
            )
    if not set(sources).issubset(available_fields):
        raise ValueError("Source list references a field absent from the input")
    if any(not isinstance(item, str) for item in (*limitations, *sources)):
        raise ValueError("Sources and limitations must be strings")
    return result


def research_with_ollama(
    record: dict[str, Any],
    *,
    enabled: bool = False,
    model: str = "llama3.2:3b",
    url: str = "http://localhost:11434/api/generate",
    post: Callable[..., Any] = requests.post,
) -> dict[str, Any]:
    if not enabled:
        return fallback_research(record, "Ollama not requested")
    prompt = (
        "Return JSON with observed_facts (objects with field/value copied "
        "exactly from the input), hypotheses (each label='hypothesis', "
        "claim, evidence_fields), confidence from 0 to 1, sources, "
        "limitations. Never invent observed facts. Input: "
        + json.dumps(record, ensure_ascii=True)
    )
    try:
        response = post(
            url,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {"temperature": 0},
            },
            timeout=30,
        )
        response.raise_for_status()
        outer = response.json()
        result = json.loads(outer["response"])
        return validate_research(result, record)
    except (
        requests.RequestException,
        KeyError,
        TypeError,
        ValueError,
        json.JSONDecodeError,
    ) as exc:
        return fallback_research(
            record, f"Ollama result was unavailable or invalid: {type(exc).__name__}"
        )
