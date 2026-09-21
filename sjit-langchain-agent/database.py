import sqlite3

DB_NAME = "students.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            python INTEGER NOT NULL,
            database INTEGER NOT NULL,
            ai INTEGER NOT NULL,
            web INTEGER NOT NULL
        )
    """)

    students = [
        ("22CS045", "Dhanushya", "Computer Science", 85, 72, 90, 78),
        ("22CS046", "Rahul", "Computer Science", 65, 70, 68, 72),
        ("22CS047", "Priya", "Information Technology", 92, 88, 95, 90),
        ("22CS048", "Arun", "Information Technology", 55, 60, 58, 62),
        ("22CS049", "Meena", "Computer Science", 78, 85, 80, 88)
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO students
        (student_id, name, department, python, database, ai, web)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, students)

    conn.commit()
    conn.close()

    print("Database created successfully!")


if __name__ == "__main__":
    create_database()