import sqlite3

conn = sqlite3.connect("placement.db")
cursor = conn.cursor()

# Students
students = [
    ("23CSE001", "Ashwikha", "CSE", 8.8, 0, 2029),
    ("23CSE002", "Danish", "CSE", 7.2, 1, 2029),
    ("23ECE001", "Rahul", "ECE", 8.5, 0, 2029)
]

cursor.executemany("""
INSERT OR IGNORE INTO student
(roll_no, name, branch, cgpa, backlogs, grad_year)
VALUES (?, ?, ?, ?, ?, ?)
""", students)


# Companies
companies = [
    ("TCS",),
    ("Infosys",)
]

cursor.executemany("""
INSERT OR IGNORE INTO company (name)
VALUES (?)
""", companies)


# Drives
cursor.execute("""
SELECT id FROM company WHERE name = 'TCS'
""")

tcs_id = cursor.fetchone()[0]

cursor.execute("""
SELECT id FROM company WHERE name = 'Infosys'
""")

infosys_id = cursor.fetchone()[0]


cursor.execute("""
INSERT INTO drive
(company_id, role, ctc_lpa, deadline, status)
VALUES (?, ?, ?, ?, ?)
""", (tcs_id, "Software Engineer", 7.5, "2026-10-15", "open"))

tcs_drive_id = cursor.lastrowid


cursor.execute("""
INSERT INTO drive
(company_id, role, ctc_lpa, deadline, status)
VALUES (?, ?, ?, ?, ?)
""", (infosys_id, "Systems Engineer", 6.0, "2026-10-20", "open"))

infosys_drive_id = cursor.lastrowid


# Eligibility rules
cursor.execute("""
INSERT INTO eligibility_rule
(drive_id, min_cgpa, max_backlogs, allowed_branch, grad_year)
VALUES (?, ?, ?, ?, ?)
""", (tcs_drive_id, 7.5, 0, "CSE,IT", 2029))


cursor.execute("""
INSERT INTO eligibility_rule
(drive_id, min_cgpa, max_backlogs, allowed_branch, grad_year)
VALUES (?, ?, ?, ?, ?)
""", (infosys_drive_id, 7.0, 1, "CSE,IT,ECE", 2029))


conn.commit()
conn.close()

print("Sample data inserted.")