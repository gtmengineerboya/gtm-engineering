"""Deterministic outreach quality signals; no message sending is implemented."""

from __future__ import annotations

import json
import re
from typing import Any, Callable

import requests


UNSUPPORTED_CLAIMS = (
    re.compile(r"\b(you need|your team needs|you are struggling)\b", re.I),
    re.compile(r"\b(guarantee|will increase|will reduce)\b", re.I),
    re.compile(r"\b(market leader|best-in-class|industry-leading)\b", re.I),
)
GENERIC_OPENERS = ("hope you're well", "just checking in", "dear sir or madam")


def evaluate_message(
    company_name: str,
    message: str,
    known_facts: list[str] | None = None,
) -> dict[str, object]:
    clean_message = " ".join((message or "").split())
    reasons = []
    word_count = len(clean_message.split())
    if not clean_message:
        reasons.append("Message is empty")
    if not 25 <= word_count <= 100:
        reasons.append(f"Word count outside 25-100: {word_count}")
    if company_name and company_name.casefold() not in clean_message.casefold():
        reasons.append("Company name is not mentioned")
    lower = clean_message.casefold()
    if any(opener in lower for opener in GENERIC_OPENERS):
        reasons.append("Generic opening detected")
    for pattern in UNSUPPORTED_CLAIMS:
        if pattern.search(clean_message):
            reasons.append("Potential unsupported claim: " + pattern.pattern)
    facts = [fact.casefold() for fact in (known_facts or []) if fact]
    if facts and not any(fact in lower for fact in facts):
        reasons.append("No supplied evidence phrase found")
    return {
        "status": "REVIEW_REQUIRED" if reasons else "PASS_AUTOMATED_CHECKS",
        "word_count": word_count,
        "reasons": reasons,
        "human_review_required": True,
        "automated_pass_is_not_quality_guarantee": True,
    }


MODEL_RATINGS = {
    "tone",
    "clarity",
    "call_to_action",
    "personalization",
    "factual_grounding",
}


def model_judgment(
    message: str,
    evidence: list[str],
    *,
    enabled: bool = False,
    model: str = "llama3.2:3b",
    url: str = "http://localhost:11434/api/generate",
    post: Callable[..., Any] = requests.post,
) -> dict[str, Any]:
    if not enabled:
        return {"status": "NOT_RUN", "reason": "Ollama was not requested"}
    prompt = (
        "Assess this synthetic B2B outreach draft. Return JSON with integer "
        "ratings 1-5 for tone, clarity, call_to_action, personalization, "
        "factual_grounding, plus a short rationale. Do not invent facts. "
        f"Evidence: {json.dumps(evidence)}\nDraft: {message}"
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
        judgment = json.loads(response.json()["response"])
        if not isinstance(judgment, dict):
            raise ValueError("Model judgment must be a JSON object")
        if set(judgment) - (MODEL_RATINGS | {"rationale"}):
            raise ValueError("Model judgment contains unknown fields")
        if any(
            not isinstance(judgment.get(key), int)
            or not 1 <= judgment[key] <= 5
            for key in MODEL_RATINGS
        ):
            raise ValueError("Every model rating must be an integer from 1 to 5")
        if not isinstance(judgment.get("rationale"), str):
            raise ValueError("Model rationale must be text")
        return {"status": "COMPLETED", **judgment}
    except (
        requests.RequestException,
        KeyError,
        TypeError,
        ValueError,
        json.JSONDecodeError,
    ) as exc:
        return {
            "status": "UNAVAILABLE_OR_INVALID",
            "reason": type(exc).__name__,
        }
