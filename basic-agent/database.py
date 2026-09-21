import sqlite3


def get_connection():
    return sqlite3.connect("placement.db")


def get_student(roll_no):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT roll_no, name, branch, cgpa, backlogs, grad_year
        FROM student
        WHERE roll_no = ?
    """, (roll_no,))

    student = cursor.fetchone()

    conn.close()

    return student


def get_drive(company_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            drive.id,
            company.name,
            drive.role,
            drive.ctc_lpa,
            drive.deadline,
            drive.status
        FROM drive
        JOIN company
        ON drive.company_id = company.id
        WHERE company.name = ?
    """, (company_name,))

    drive = cursor.fetchone()

    conn.close()

    return drive


def get_eligibility_rule(drive_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            min_cgpa,
            max_backlogs,
            allowed_branch,
            grad_year
        FROM eligibility_rule
        WHERE drive_id = ?
    """, (drive_id,))

    rule = cursor.fetchone()

    conn.close()

    return rule