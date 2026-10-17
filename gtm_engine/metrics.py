"""Unit-aware GTM funnel and revenue metrics."""

from __future__ import annotations

from typing import Any


def _rate(numerator: float, denominator: float) -> float | None:
    return numerator / denominator if denominator else None


def calculate_metrics(data: dict[str, Any]) -> dict[str, Any]:
    counts = data["funnel_counts"]
    customers = counts["customer"]
    spend = data.get("sales_marketing_spend_usd")
    mrr = data.get("monthly_recurring_revenue_usd")
    lifetime_months = data.get("average_customer_lifetime_months")
    average_deal = data.get("average_deal_value_usd")
    opportunities = counts["opportunity"]
    sales_cycle_days = data.get("average_sales_cycle_days")
    conversion = {
        "lead_to_mql_rate": _rate(counts["mql"], counts["lead"]),
        "mql_to_sql_rate": _rate(counts["sql"], counts["mql"]),
        "sql_to_opportunity_rate": _rate(opportunities, counts["sql"]),
        "opportunity_to_customer_rate": _rate(customers, opportunities),
    }
    cac = _rate(spend, customers) if spend is not None else None
    arpa_monthly = _rate(mrr, customers) if mrr is not None else None
    ltv = (
        arpa_monthly * lifetime_months
        if arpa_monthly is not None and lifetime_months is not None
        else None
    )
    pipeline = opportunities * average_deal if average_deal is not None else None
    win_rate = conversion["opportunity_to_customer_rate"]
    velocity = (
        pipeline * win_rate / sales_cycle_days
        if pipeline is not None and win_rate is not None
        and sales_cycle_days
        else None
    )
    return {
        **conversion,
        "customer_acquisition_cost_usd_per_customer": cac,
        "lifetime_value_usd_per_customer": ltv,
        "mrr_usd_per_month": mrr,
        "arr_usd_per_year": mrr * 12 if mrr is not None else None,
        "pipeline_value_usd": pipeline,
        "pipeline_velocity_usd_per_day": velocity,
        "assumptions": [
            "All counts and revenue inputs are synthetic.",
            "CAC uses supplied sales/marketing spend divided by new customers.",
            "LTV uses MRR per customer multiplied by average lifetime months.",
            "Pipeline velocity uses open opportunities, average deal value, "
            "opportunity win rate, and average sales-cycle days.",
        ],
    }
