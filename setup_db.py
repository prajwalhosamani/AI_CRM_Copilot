import sqlite3

conn = sqlite3.connect("crm.db")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS opportunities")
c.execute("DROP TABLE IF EXISTS accounts")
c.execute("DROP TABLE IF EXISTS cases")

c.execute("""
CREATE TABLE accounts (
    account_name TEXT PRIMARY KEY,
    industry TEXT,
    region TEXT,
    account_owner TEXT
)
""")

c.execute("""
CREATE TABLE opportunities (
    id INTEGER PRIMARY KEY,
    account_name TEXT,
    owner TEXT,
    stage TEXT,
    amount REAL,
    close_date TEXT,
    lead_source TEXT
)
""")

c.execute("""
CREATE TABLE cases (
    case_id INTEGER PRIMARY KEY,
    account_name TEXT,
    priority TEXT,
    status TEXT,
    created_date TEXT,
    closed_date TEXT
)
""")

accounts = [
    ("Acme Corp", "Manufacturing", "West", "Priya"),
    ("Globex", "Technology", "East", "Raj"),
    ("Initech", "Finance", "West", "Priya"),
    ("Umbrella", "Healthcare", "South", "Raj"),
    ("Wayne Ent.", "Manufacturing", "North", "Priya"),
    ("Stark Industries", "Technology", "East", "Raj"),
    ("Soylent Corp", "Healthcare", "South", "Priya"),
]

opportunities = [
    (1, "Acme Corp", "Priya", "Closed Won", 50000, "2026-03-01", "Referral"),
    (2, "Globex", "Raj", "Negotiation", 120000, "2026-07-15", "Website"),
    (3, "Initech", "Priya", "Closed Lost", 30000, "2026-02-10", "Cold Call"),
    (4, "Umbrella", "Raj", "Closed Won", 75000, "2026-04-20", "Referral"),
    (5, "Wayne Ent.", "Priya", "Prospecting", 200000, "2026-09-01", "Website"),
    (6, "Stark Industries", "Raj", "Closed Won", 95000, "2026-05-12", "Partner"),
    (7, "Soylent Corp", "Priya", "Closed Won", 60000, "2026-06-01", "Cold Call"),
    (8, "Globex", "Raj", "Closed Lost", 40000, "2026-01-20", "Website"),
]

cases = [
    (1, "Acme Corp", "High", "Closed", "2026-01-05", "2026-01-08"),
    (2, "Globex", "Medium", "Open", "2026-06-01", None),
    (3, "Umbrella", "Low", "Closed", "2026-02-15", "2026-02-25"),
    (4, "Wayne Ent.", "High", "Closed", "2026-03-01", "2026-03-02"),
    (5, "Stark Industries", "Medium", "Closed", "2026-04-10", "2026-04-20"),
    (6, "Soylent Corp", "High", "Open", "2026-06-10", None),
]

c.executemany("INSERT INTO accounts VALUES (?,?,?,?)", accounts)
c.executemany("INSERT INTO opportunities VALUES (?,?,?,?,?,?,?)", opportunities)
c.executemany("INSERT INTO cases VALUES (?,?,?,?,?,?)", cases)

conn.commit()
conn.close()
print("done")