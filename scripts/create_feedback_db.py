#!/usr/bin/env python3
"""Create a SQLite database with ~60 student feedback rows for January.

Usage: python scripts/create_feedback_db.py
This writes `database/feedback_january.db` relative to the repo root.
"""
import sqlite3
import random
from pathlib import Path
from datetime import date, timedelta

DB_PATH = Path("database") / "feedback_january.db"


def ensure_db_dir():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def create_schema(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        roll_no TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY,
        student_id INTEGER NOT NULL,
        feedback_date TEXT NOT NULL,
        meal TEXT NOT NULL,
        rating INTEGER NOT NULL,
        comments TEXT,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
    """)
    conn.commit()


def random_january_date(year=2026):
    start = date(year, 1, 1)
    day_offset = random.randint(0, 30)  # 0..30 -> Jan 1..31
    return (start + timedelta(days=day_offset)).isoformat()


def populate(conn, n_students=60, n_feedback=60):
    cur = conn.cursor()

    # Insert students
    students = []
    for i in range(1, n_students + 1):
        name = f"Student {i}"
        roll = f"R{i:03d}"
        students.append((i, name, roll))
    cur.executemany("INSERT OR IGNORE INTO students(id, name, roll_no) VALUES(?,?,?)", students)

    comments_pool = [
        "Too salty",
        "Good taste",
        "More variety please",
        "Undercooked",
        "Well cooked",
        "Portions are small",
        "Loved the dessert",
        "Vegetarian options needed",
        "Temperature was low",
        "Clean and fresh",
    ]
    meals = ["breakfast", "lunch", "dinner"]

    feedback_rows = []
    for i in range(n_feedback):
        student_id = random.randint(1, n_students)
        fdate = random_january_date()
        meal = random.choice(meals)
        rating = random.randint(1, 5)
        comment = random.choice(comments_pool)
        feedback_rows.append((student_id, fdate, meal, rating, comment))

    cur.executemany(
        "INSERT INTO feedback(student_id, feedback_date, meal, rating, comments) VALUES(?,?,?,?,?)",
        feedback_rows,
    )
    conn.commit()


def main():
    ensure_db_dir()
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(str(DB_PATH))
    try:
        create_schema(conn)
        populate(conn, n_students=60, n_feedback=60)
        print(f"Created SQLite DB with sample feedback at: {DB_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
