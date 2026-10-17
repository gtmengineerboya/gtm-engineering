"""Calculate synthetic funnel/revenue metrics and write CSV/Markdown reports."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gtm_engine.metrics import calculate_metrics


DAY_DIR = Path(__file__).resolve().parent
METRIC_UNITS = {
    "lead_to_mql_rate": "ratio (0-1)",
    "mql_to_sql_rate": "ratio (0-1)",
    "sql_to_opportunity_rate": "ratio (0-1)",
    "opportunity_to_customer_rate": "ratio (0-1)",
    "customer_acquisition_cost_usd_per_customer": "USD/customer",
    "lifetime_value_usd_per_customer": "USD/customer",
    "mrr_usd_per_month": "USD/month",
    "arr_usd_per_year": "USD/year",
    "pipeline_value_usd": "USD",
    "pipeline_velocity_usd_per_day": "USD/day",
}


def main():
    data = json.loads(
        (DAY_DIR / "sample_metrics.json").read_text(encoding="utf-8")
    )
    metrics = calculate_metrics(data)
    output = DAY_DIR / "output"
    output.mkdir(parents=True, exist_ok=True)
    with (output / "metrics.csv").open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["metric", "value", "unit"])
        for name, value in metrics.items():
            if isinstance(value, list):
                continue
            writer.writerow([
                name,
                "" if value is None else value,
                METRIC_UNITS.get(name, "count or seconds"),
            ])
    lines = [
        "# Synthetic GTM metrics",
        "",
        "All numbers below use synthetic sample inputs, not actual business results.",
        "",
    ]
    lines.extend(
        f"- **{name}:** {value if value is not None else 'N/A'} "
        f"({METRIC_UNITS.get(name, 'count or seconds')})"
                 for name, value in metrics.items()
                 if not isinstance(value, list))
    lines.extend(["", "## Assumptions", ""])
    lines.extend(f"- {item}" for item in metrics["assumptions"])
    (output / "metrics.md").write_text("\n".join(lines) + "\n",
                                       encoding="utf-8")
    print(f"Reports created under {output}")


if __name__ == "__main__":
    main()
