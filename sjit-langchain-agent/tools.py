import sqlite3
from langchain.tools import tool

DB_NAME = "students.db"


@tool
def get_student_info(student_id: str) -> str:
    """Get the student's name and department using their student ID."""

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, department
        FROM students
        WHERE student_id = ?
    """, (student_id,))

    result = cursor.fetchone()

    conn.close()

    if result is None:
        return f"No student found with ID {student_id}"

    name, department = result

    return f"Name: {name}, Department: {department}"


@tool
def get_student_marks(student_id: str) -> str:
    """Get Python, Database, AI, and Web marks for a student."""

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT python, database, ai, web
        FROM students
        WHERE student_id = ?
    """, (student_id,))

    result = cursor.fetchone()

    conn.close()

    if result is None:
        return f"No student found with ID {student_id}"

    python_mark, database_mark, ai_mark, web_mark = result

    return (
        f"Python: {python_mark}, "
        f"Database: {database_mark}, "
        f"AI: {ai_mark}, "
        f"Web: {web_mark}"
    )


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression such as 85+72+90+78 or (85+72+90+78)/4."""

    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)

    except Exception as e:
        return f"Calculation error: {str(e)}"


@tool
def get_passing_rules() -> str:
    """Get the university passing requirements."""

    return (
        "University passing rules: "
        "minimum overall average is 40%, "
        "and minimum mark in each subject is 35%."
    )