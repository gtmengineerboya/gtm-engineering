"""Create the Day 4 GTM practice database: companies, contacts, lead_scores, activities.

Run it from any folder:
    .\.venv\Scripts\python.exe day-04\gtm_database.py

The database file is <repo root>\gtm.db (git-ignored). Running this again is safe:
every table uses CREATE TABLE IF NOT EXISTS, so existing data is kept.
"""

import sqlite3
from contextlib import closing
from pathlib import Path

# Anchored to this file, so the database is always the same file, not "wherever you ran Python".
DB_PATH = Path(__file__).resolve().parent.parent / "gtm.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS companies (
    company_id INTEGER PRIMARY KEY,
    company_name TEXT,
    country TEXT,
    industry TEXT,
    employees INTEGER
);

CREATE TABLE IF NOT EXISTS contacts (
    contact_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    name TEXT,
    job_title TEXT,
    email TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS lead_scores (
    score_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    icp_score INTEGER,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS activities (
    activity_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    activity_type TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);
"""


def create_database(db_path: Path = DB_PATH) -> Path:
    """Create the tables (if missing) and return the database path."""
    with closing(sqlite3.connect(db_path)) as connection:
        # SQLite ignores FOREIGN KEY rules unless you switch them on for each connection.
        # Do this whenever you INSERT, otherwise a contact can point at a missing company.
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA)
        connection.commit()
    return db_path


if __name__ == "__main__":
    created = create_database()
    print(f"GTM database ready: {created}")
