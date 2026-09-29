import sqlite3

connection = sqlite3.connect("gtm.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS companies (
    company_id INTEGER PRIMARY KEY,
    company_name TEXT,
    country TEXT,
    industry TEXT,
    employees INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    contact_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    name TEXT,
    job_title TEXT,
    email TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS lead_scores (
    score_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    icp_score INTEGER,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS activities (
    activity_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    activity_type TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
)
""")

connection.commit()

print("GTM database created successfully.")

connection.close()