"""Load seed.sql into a throwaway in-memory SQLite database, then run a .sql file.

Usage (from C:\gtm-engineering):
    .\.venv\Scripts\python.exe learning\sql-practice\run_practice.py
    .\.venv\Scripts\python.exe learning\sql-practice\run_practice.py learning\sql-practice\answers.sql

The database is rebuilt on every run, so you cannot break anything.
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent


def split_statements(text: str) -> list[str]:
    """Split on semicolons that really end a statement (not inside quotes)."""
    statements, buffer = [], ""
    for line in text.splitlines(keepends=True):
        buffer += line
        if sqlite3.complete_statement(buffer):
            statements.append(buffer.strip())
            buffer = ""
    return statements


def print_table(columns: list[str], rows: list[tuple]) -> None:
    if not rows:
        print("  (no rows)")
        return
    widths = [
        max(len(str(col)), *(len(str(row[i])) for row in rows))
        for i, col in enumerate(columns)
    ]
    print("  " + " | ".join(str(c).ljust(w) for c, w in zip(columns, widths)))
    print("  " + "-+-".join("-" * w for w in widths))
    for row in rows:
        print("  " + " | ".join(str(v).ljust(w) for v, w in zip(row, widths)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query_file", nargs="?", type=Path,
                        default=HERE / "my_answers.sql")
    args = parser.parse_args()

    connection = sqlite3.connect(":memory:")
    connection.executescript((HERE / "seed.sql").read_text(encoding="utf-8"))

    ran = 0
    # Keep only statements that contain real SQL (not just comments).
    for number, statement in enumerate(
        split_statements(args.query_file.read_text(encoding="utf-8")), start=1
    ):
        has_sql = any(
            line.strip() and not line.strip().startswith("--")
            for line in statement.splitlines()
        )
        if not has_sql:
            continue
        ran += 1
        print(f"Statement {number}:")
        try:
            cursor = connection.execute(statement)
        except sqlite3.Error as error:
            print(f"  ERROR: {error}")
            continue
        if cursor.description:
            print_table([d[0] for d in cursor.description], cursor.fetchall())
        else:
            print(f"  OK ({cursor.rowcount} rows changed)")
    if ran == 0:
        print(f"No queries found in {args.query_file.name} yet. "
              "Write your answer under a -- Q heading and run again.")
    connection.close()


if __name__ == "__main__":
    main()
