



import csv
import json
import re
import time
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR.parent / "day-10" / "scored_leads.csv"
OUTPUT_FILE = BASE_DIR / "outreach_review.csv"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"
MAX_RETRIES = 3

TECH_ALIASES = {
    "aws": {"aws"},
    "azure": {"azure", "microsoft azure"},
    "gcp": {"gcp", "google cloud", "google cloud platform"},
    "python": {"python"},
    "java": {"java"},
    "spring boot": {"spring boot"},
    "react": {"react", "react.js"},
    "node.js": {"node.js"},
    "kubernetes": {"kubernetes"},
    "power bi": {"power bi"},
    "sql": {"sql"},
    "postgresql": {"postgresql", "postgres"},
    "mongodb": {"mongodb"},
    "docker": {"docker"},
    "terraform": {"terraform"},
}


def clean(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def get_evidence(company):
    return {
        "company_name": clean(company.get("company_name")),
        "industry": clean(company.get("industry")),
        "country": clean(company.get("country")),
        "employees": clean(company.get("employees")),
        "employee_segment": clean(company.get("employee_segment")),
        "technologies": [
            clean(item)
            for item in clean(company.get("technology")).split(";")
            if clean(item)
        ],
        "ai_signal": clean(company.get("ai_signal")),
        "saas_signal": clean(company.get("saas_signal")),
        "target_market": clean(company.get("target_market")),
    }


def call_ollama(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.2},
        },
        timeout=120,
    )
    response.raise_for_status()
    return json.loads(response.json()["response"])


def safe_fallback(company):
    """A factual fallback built directly from source fields."""
    data = get_evidence(company)
    name = data["company_name"]

    details = []
    if data["industry"]:
        details.append(f"industry: {data['industry']}")
    if data["country"]:
        details.append(f"country: {data['country']}")
    if data["employee_segment"]:
        details.append(f"segment: {data['employee_segment']}")
    if data["employees"]:
        details.append(f"employee count: {data['employees']}")
    if data["technologies"]:
        details.append(
            "listed technologies: " + ", ".join(data["technologies"])
        )

    if details:
        return (
            f"Hi {name} team, our prospect data lists "
            + "; ".join(details)
            + ". I'd welcome a brief conversation to learn about your "
              "priorities and explore whether our services may be relevant. "
              "Would you be open to connecting?"
        )

    return (
        f"Hi {name} team, I'd welcome a brief conversation to learn "
        "about your priorities and explore whether our services "
        "may be relevant. Would you be open to connecting?"
    )


def validate_message(message, company):
    """Apply deterministic checks; this is not a guarantee of truth."""
    message = clean(message)
    data = get_evidence(company)
    reasons = []

    if not message:
        reasons.append("Empty message")
        return False, reasons

    word_count = len(message.split())
    if not 25 <= word_count <= 100:
        reasons.append(f"Word count outside 25-100: {word_count}")

    if data["company_name"].lower() not in message.lower():
        reasons.append("Company name missing")

    # Reject unsupported rankings, claims of known needs, or asserted intent.
    risky_patterns = [
        r"\b(leading|market leader|industry-leading|best-in-class)\b",
        r"\b(you need|your team needs|your company needs)\b",
        r"\b(you are struggling|you're struggling|facing challenges)\b",
        r"\b(i noticed you need|i know you're looking for)\b",
        r"\b(your current problem|your biggest challenge)\b",
        r"\b(you are planning to|you plan to|you recently launched)\b",
        r"\b(guarantee|will increase|will reduce|will save)\b",
    ]

    for pattern in risky_patterns:
        if re.search(pattern, message, re.IGNORECASE):
            reasons.append(
                "Potential unsupported claim: " + pattern
            )

    # If a technology is mentioned, it must exist in the source data.
    known = {item.lower() for item in data["technologies"]}

    for canonical, aliases in TECH_ALIASES.items():
        for alias in aliases:
            if re.search(
                rf"(?<!\w){re.escape(alias)}(?!\w)",
                message,
                re.IGNORECASE,
            ):
                if not known.intersection(aliases):
                    reasons.append(
                        f"Technology not in source data: {alias}"
                    )
                break

    # Check employee count if the message states a count followed by "employees".
    employee_claims = re.findall(
        r"\b(\d[\d,]*)\s+employees\b",
        message,
        re.IGNORECASE,
    )
    expected_count = data["employees"].replace(",", "")

    for claimed_count in employee_claims:
        if claimed_count.replace(",", "") != expected_count:
            reasons.append(
                f"Employee count mismatch: {claimed_count}"
            )

    # Check segment labels when mentioned.
    segment_labels = ("SMB", "Growth", "Mid-Market", "Enterprise")
    for label in segment_labels:
        if re.search(rf"\b{re.escape(label)}\b", message, re.IGNORECASE):
            if label.lower() != data["employee_segment"].lower():
                reasons.append(f"Employee segment mismatch: {label}")

    # Check country names when the message explicitly mentions one.
    countries = ("USA", "India", "UK", "Canada", "Germany")
    for country in countries:
        if re.search(rf"\b{re.escape(country)}\b", message, re.IGNORECASE):
            if country.lower() != data["country"].lower():
                reasons.append(f"Country mismatch: {country}")

    return not reasons, reasons


def generate_ai_message(company):
    data = get_evidence(company)

    prompt = f"""
You write concise B2B cold outreach.

Use only this source record:
{json.dumps(data, ensure_ascii=False)}

Instructions:
- Write a natural, personalized message of 35-70 words.
- Use the company name and two or three relevant source facts.
- You may use industry, country, employee count, employee segment,
  listed technologies, or populated signal fields.
- Do not invent projects, customers, company rankings, business problems,
  buying intent, initiatives, hiring plans, or results.
- Do not imply that technology usage proves a business problem.
- Do not describe a signal as verified if the source field is empty.
- Ask an open question about priorities instead of assuming them.
- Do not invent a person's name or job title.
- Vary sentence structure naturally; avoid generic claims about being
  a leader, driving growth, or staying ahead of the curve.
- Return JSON only: {{"message": "complete message"}}
"""

    last_error = ""

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            result = call_ollama(prompt)
            message = clean(result.get("message"))

            approved, reasons = validate_message(message, company)
            if approved:
                return message, "APPROVED_AI", "Passed deterministic checks"

            last_error = "; ".join(reasons)
            print(f"  AI draft rejected ({attempt}): {last_error}")

        except (
            requests.RequestException,
            ValueError,
            TypeError,
            KeyError,
        ) as error:
            last_error = str(error)
            print(f"  AI attempt {attempt} failed: {last_error}")

        if attempt < MAX_RETRIES:
            time.sleep(1)

    # Use a factual fallback rather than sending a rejected AI draft.
    fallback = safe_fallback(company)
    approved, reasons = validate_message(fallback, company)

    if approved:
        return (
            fallback,
            "APPROVED_FALLBACK",
            f"AI draft rejected; factual fallback used. Last issue: {last_error}",
        )

    return (
        fallback,
        "REVIEW_REQUIRED",
        "Fallback needs review: " + "; ".join(reasons),
    )


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input CSV not found: {INPUT_FILE}")

    results = []

    with INPUT_FILE.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)

        required = {
            "company_name", "qualification", "industry",
            "country", "employees", "employee_segment", "technology",
        }

        if not reader.fieldnames:
            raise RuntimeError("Input CSV has no headers.")

        missing = required - set(reader.fieldnames)
        if missing:
            raise RuntimeError(
                f"Missing input columns: {', '.join(sorted(missing))}"
            )

        for company in reader:
            qualification = clean(company.get("qualification"))

            if qualification == "Not Qualified":
                continue

            if not clean(company.get("company_name")):
                print("Skipping row with missing company name.")
                continue

            name = clean(company["company_name"])
            print(f"AI personalizing: {name}...")

            message, status, reason = generate_ai_message(company)

            # Preserve the original source fields and scores.
            row = dict(company)
            row["personalized_message"] = message
            row["validation_status"] = status
            row["validation_reason"] = reason
            results.append(row)

    if not results:
        print("No qualified leads found; existing report preserved.")
        return

    # Write to a temporary file first, then replace the report.
    temp_file = OUTPUT_FILE.with_suffix(".tmp")
    with temp_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    temp_file.replace(OUTPUT_FILE)

    approved_ai = sum(
        row["validation_status"] == "APPROVED_AI" for row in results
    )
    approved_fallback = sum(
        row["validation_status"] == "APPROVED_FALLBACK" for row in results
    )
    review_required = sum(
        row["validation_status"] == "REVIEW_REQUIRED" for row in results
    )

    print(f"\nLeads processed: {len(results)}")
    print(f"AI messages passed checks: {approved_ai}")
    print(f"Approved fallback messages: {approved_fallback}")
    print(f"Review required: {review_required}")
    print(f"Report saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
