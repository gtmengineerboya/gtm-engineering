-- Practice dataset for learning/sql-skills.md (SQLite). All data is synthetic.
-- Deliberate "messy real-world" features:
--   * Company 1 has TWO score rows (a history) -> sums/counts can be inflated
--   * Contacts 105 and 106 are the same person with different email casing/spaces
--   * Contact 108 points to company 99, which does not exist (orphan)
--   * Company 7 has no source, company 8 has no employee count (NULLs)

CREATE TABLE companies (
    company_id      INTEGER PRIMARY KEY,
    company_name    TEXT NOT NULL,
    country         TEXT,
    industry        TEXT,
    employees       INTEGER,
    original_source TEXT
);

CREATE TABLE contacts (
    contact_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    name       TEXT,
    job_title  TEXT,
    email      TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE lead_scores (
    score_id   INTEGER PRIMARY KEY,
    company_id INTEGER,
    icp_score  INTEGER,
    scored_at  TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE activities (
    activity_id   INTEGER PRIMARY KEY,
    company_id    INTEGER,
    activity_type TEXT,
    activity_date TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE deals (
    deal_id    INTEGER PRIMARY KEY,
    company_id INTEGER,
    amount     INTEGER,
    stage      TEXT,
    created_at TEXT,
    closed_at  TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

INSERT INTO companies VALUES
(1, 'Acme AI',        'USA',   'SaaS',    250, 'webinar'),
(2, 'Beta Finance',   'India', 'Finance',  50, 'referral'),
(3, 'CloudTech',      'USA',   'SaaS',    500, 'referral'),
(4, 'DataWorks',      'UK',    'SaaS',    120, 'webinar'),
(5, 'Evergreen Bank', 'USA',   'Finance', 900, 'outbound'),
(6, 'FlowOps',        'USA',   'SaaS',     80, 'outbound'),
(7, 'Garnet Health',  'USA',   'Health',  300, NULL),
(8, 'Helio Systems',  'India', 'SaaS',    NULL, 'webinar');

INSERT INTO contacts VALUES
(101, 1,  'John',  'CEO',            'john@acme.ai'),
(102, 1,  'Sarah', 'VP Sales',       'sarah@acme.ai'),
(103, 3,  'Mike',  'CTO',            'mike@cloudtech.com'),
(104, 4,  'David', 'CEO',            'david@dataworks.co'),
(105, 5,  'Priya', 'COO',            'Priya@evergreen.bank'),
(106, 5,  'Priya', 'COO',            ' priya@evergreen.bank '),
(107, 6,  'Lena',  'Head of Growth', 'lena@flowops.io'),
(108, 99, 'Ghost', 'CEO',            'ghost@nowhere.com');

INSERT INTO lead_scores VALUES
(1, 1, 70, '2026-09-01'),
(2, 1, 85, '2026-10-01'),
(3, 2, 40, '2026-09-15'),
(4, 3, 92, '2026-10-05'),
(5, 4, 65, '2026-09-20'),
(6, 5, 78, '2026-10-10'),
(7, 6, 55, '2026-10-12'),
(8, 7, 81, '2026-10-15');

INSERT INTO activities VALUES
(1, 1, 'email_open',  '2026-09-03'),
(2, 1, 'demo',        '2026-09-20'),
(3, 3, 'email_reply', '2026-10-06'),
(4, 3, 'demo',        '2026-10-14'),
(5, 5, 'email_open',  '2026-10-11'),
(6, 4, 'email_open',  '2026-09-22');

INSERT INTO deals VALUES
(1, 1, 12000, 'closed_won',  '2026-09-21', '2026-10-20'),
(2, 3, 30000, 'closed_won',  '2026-10-15', '2026-11-02'),
(3, 4,  8000, 'closed_lost', '2026-09-25', '2026-10-30'),
(4, 5, 45000, 'open',        '2026-10-20', NULL),
(5, 1,  5000, 'closed_lost', '2026-10-01', '2026-10-25');
