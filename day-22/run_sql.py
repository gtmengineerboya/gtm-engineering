"""Execute the portable funnel query against a temporary SQLite database."""

from __future__ import annotations

import sqlite3
from pathlib import Path


DAY_DIR = Path(__file__).resolve().parent
QUERY_FILE = DAY_DIR / "funnel_analysis.sql"


def main():
    connection = sqlite3.connect(":memory:")
    connection.execute(
        """CREATE TABLE leads (
            lifecycle_stage TEXT NOT NULL,
            icp_score INTEGER NOT NULL,
            original_source TEXT NOT NULL
        )"""
    )
    connection.executemany(
        "INSERT INTO leads VALUES (?, ?, ?)",
        [
            ("Lead", 35, "webinar"),
            ("MQL", 74, "webinar"),
            ("MQL", 81, "referral"),
            ("SQL", 66, "referral"),
            ("Opportunity", 90, "webinar"),
            ("Customer", 88, "referral"),
        ],
    )
    connection.execute(
        """CREATE TABLE stage_history (
            stage TEXT NOT NULL,
            duration_days INTEGER NOT NULL
        )"""
    )
    connection.executemany(
        "INSERT INTO stage_history VALUES (?, ?)",
        [("MQL", 4), ("MQL", 7), ("SQL", 12), ("Opportunity", 20)],
    )
    for index, statement in enumerate(
        QUERY_FILE.read_text(encoding="utf-8").split(";"), start=1
    ):
        if not statement.strip():
            continue
        cursor = connection.execute(statement)
        names = [column[0] for column in cursor.description]
        print(f"Query {index}:")
        for row in cursor.fetchall():
            print(dict(zip(names, row)))
    connection.close()


if __name__ == "__main__":
    main()
