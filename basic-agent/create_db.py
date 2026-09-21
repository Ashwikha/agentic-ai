import sqlite3

conn = sqlite3.connect("placement.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    branch TEXT NOT NULL,
    cgpa REAL NOT NULL,
    backlogs INTEGER NOT NULL,
    grad_year INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS company (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS drive (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    ctc_lpa REAL,
    deadline TEXT,
    status TEXT,
    FOREIGN KEY (company_id) REFERENCES company(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS eligibility_rule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drive_id INTEGER NOT NULL,
    min_cgpa REAL,
    max_backlogs INTEGER,
    allowed_branch TEXT,
    grad_year INTEGER,
    FOREIGN KEY (drive_id) REFERENCES drive(id)
)
""")

conn.commit()
conn.close()

print("Database created successfully.")