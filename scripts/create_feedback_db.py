import sqlite3
import random
from pathlib import Path
from datetime import date, timedelta, datetime

DB_PATH = Path("database") / "mess_management.db"


def ensure_db_dir():
    """Create database directory if it doesn't exist."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def create_schema(conn):
    """Create all required tables for the mess management system."""
    cur = conn.cursor()

    # Students Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll_no TEXT UNIQUE NOT NULL,
        email TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Food Counts Table (Updated by Warden) - Streamlined schema
    cur.execute("""
    CREATE TABLE IF NOT EXISTS food_counts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        count_date TEXT NOT NULL,
        meal TEXT NOT NULL CHECK(meal IN ('breakfast', 'lunch', 'dinner')),
        student_count INTEGER DEFAULT 0,
        faculty_count INTEGER DEFAULT 0,
        guest_count INTEGER DEFAULT 0, -- New column for guests
        total_count INTEGER DEFAULT 0, -- Sum of student + faculty + guest
        updated_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(count_date, meal)
    )
    """)

    # Student Feedback Table (Meal-wise ratings)
    # The 'comments' column is single, matching frontend & new server expectations
    cur.execute("""
    CREATE TABLE IF NOT EXISTS student_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        feedback_date TEXT NOT NULL,
        breakfast_rating INTEGER,
        lunch_rating INTEGER,
        dinner_rating INTEGER,
        comments TEXT, -- Single comments field
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
    """)

    # Fines Imposed by Warden
    cur.execute("""
    CREATE TABLE IF NOT EXISTS fines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fine_date TEXT NOT NULL,
        meal TEXT NOT NULL CHECK(meal IN ('breakfast', 'lunch', 'dinner')),
        reason TEXT NOT NULL,
        amount INTEGER NOT NULL,
        imposed_by TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Vendor Responses to Fines
    cur.execute("""
    CREATE TABLE IF NOT EXISTS vendor_responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fine_id INTEGER NOT NULL,
        vendor_response TEXT NOT NULL,
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Submitted',
        FOREIGN KEY(fine_id) REFERENCES fines(id)
    )
    """)

    # Billing Records (Auto-calculated)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS billing (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        billing_date TEXT NOT NULL,
        breakfast_count INTEGER DEFAULT 0,
        lunch_count INTEGER DEFAULT 0,
        dinner_count INTEGER DEFAULT 0,
        max_people_fed INTEGER NOT NULL,
        amount_per_person REAL DEFAULT 150.0,
        gross_amount REAL NOT NULL,
        fine_amount REAL DEFAULT 0,
        net_amount REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(billing_date)
    )
    """)

    conn.commit()


def populate_students(conn, n_students=60):
    """Populate students table with sample data."""
    cur = conn.cursor()
    
    first_names = ["Raj", "Priya", "Amit", "Anjali", "Rohan", "Sneha", "Vikram", "Deepika", 
                   "Arjun", "Kavya", "Nikhil", "Isha", "Rahul", "Pooja", "Sanjay"]
    last_names = ["Kumar", "Sharma", "Patel", "Singh", "Gupta", "Verma", "Rao", "Nair", 
                  "Iyer", "Desai", "Chopra", "Bhat", "Reddy", "Pandey", "Tiwari"]
    
    students = []
    for i in range(1, n_students + 1):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        roll_no = f"CS{i:03d}" if i % 3 == 0 else f"EC{i:03d}" if i % 3 == 1 else f"ME{i:03d}"
        email = f"student{i}@college.edu"
        students.append((name, roll_no, email))
    
    cur.executemany(
        "INSERT OR IGNORE INTO students(name, roll_no, email) VALUES(?,?,?)",
        students
    )
    conn.commit()
    print(f"✓ Inserted {n_students} students")


def populate_food_counts(conn):
    """Populate food counts for January 2026 (daily entries)."""
    cur = conn.cursor()
    
    food_counts_data = []
    for day in range(1, 32):  # January 1-31
        date_str = f"2026-01-{day:02d}"
        
        student_bf = random.randint(80, 200)
        faculty_bf = random.randint(10, 30)
        guest_bf = random.randint(0, 5)
        total_bf = student_bf + faculty_bf + guest_bf

        student_ln = random.randint(100, 220)
        faculty_ln = random.randint(12, 35)
        guest_ln = random.randint(0, 8)
        total_ln = student_ln + faculty_ln + guest_ln
        
        student_dn = random.randint(70, 190)
        faculty_dn = random.randint(8, 25)
        guest_dn = random.randint(0, 4)
        total_dn = student_dn + faculty_dn + guest_dn
        
        food_counts_data.append((
            date_str, 'breakfast', student_bf, faculty_bf, guest_bf, total_bf, 'warden_user'
        ))
        food_counts_data.append((
            date_str, 'lunch', student_ln, faculty_ln, guest_ln, total_ln, 'warden_user'
        ))
        food_counts_data.append((
            date_str, 'dinner', student_dn, faculty_dn, guest_dn, total_dn, 'warden_user'
        ))
    
    cur.executemany(
        """INSERT OR IGNORE INTO food_counts
           (count_date, meal, student_count, faculty_count, guest_count, total_count, updated_by)
           VALUES(?,?,?,?,?,?,?)""",
        food_counts_data
    )
    conn.commit()
    print(f"✓ Inserted {len(food_counts_data)} food count records")


def populate_feedback(conn, n_feedback=150):
    """Populate student feedback with meal-wise ratings."""
    cur = conn.cursor()
    
    # Get student IDs
    cur.execute("SELECT id FROM students LIMIT 60")
    student_ids = [row[0] for row in cur.fetchall()]
    
    comments_pool = [
        "Too salty", "Good taste", "More variety please", "Undercooked", "Well cooked",
        "Portions are small", "Loved the dessert", "Vegetarian options needed",
        "Temperature was low", "Clean and fresh", "Excellent service", "Needs improvement",
        "Perfect seasoning", "More spicy please", "Quantity is good"
    ]
    
    feedback_rows = []
    for i in range(n_feedback):
        student_id = random.choice(student_ids)
        
        # Random date in January
        day = random.randint(1, 31)
        feedback_date = f"2026-01-{day:02d}"
        
        # Meal-wise ratings (independent ratings for each meal)
        breakfast_rating = random.randint(1, 5)
        lunch_rating = random.randint(1, 5)
        dinner_rating = random.randint(1, 5)
        
        comments = random.choice(comments_pool)
        
        feedback_rows.append((
            student_id, feedback_date, breakfast_rating, lunch_rating, dinner_rating, comments
        ))
    
    cur.executemany(
        """INSERT INTO student_feedback
           (student_id, feedback_date, breakfast_rating, lunch_rating, dinner_rating, comments)
           VALUES(?,?,?,?,?,?)""",
        feedback_rows
    )
    conn.commit()
    print(f"✓ Inserted {n_feedback} feedback records (meal-wise ratings)")


def populate_fines(conn):
    """Populate fines imposed by warden."""
    cur = conn.cursor()
    
    reasons = [
        "poor-quality", "hygiene-issue", "late-service", "wrong-item",
        "expired-food", "quantity-shortage", "temperature-issue", "cleanliness"
    ]
    
    fines = []
    # Create ~12 fines throughout January
    for i in range(12):
        fine_date = f"2026-01-{random.randint(1, 31):02d}"
        meal = random.choice(['breakfast', 'lunch', 'dinner'])
        reason = random.choice(reasons)
        amount = random.choice([300, 500, 1000, 1500, 2000])
        
        fines.append((fine_date, meal, reason, amount, "warden_user"))
    
    cur.executemany(
        "INSERT INTO fines(fine_date, meal, reason, amount, imposed_by) VALUES(?,?,?,?,?)",
        fines
    )
    conn.commit()
    print(f"✓ Inserted {len(fines)} fine records")
    

def populate_vendor_responses(conn):
    """Populate vendor responses to fines."""
    cur = conn.cursor()
    
    vendor_responses_pool = [
        "We had supplier issues that day. Fixed now.",
        "Acknowledged. Will maintain standards.",
        "Our new staff member made a mistake. Retrained.",
        "Weather issues caused delay. Will improve.",
        "Sorry for inconvenience. Better monitoring in place.",
        "Equipment malfunction. Now serviced.",
        "Staff shortage that day. Hired additional help.",
        "Honest mistake. Quality checks strengthened.",
        "Isolated incident. Measures taken to prevent recurrence.",
        "Thank you for pointing out. Corrected immediately."
    ]
    
    # Get all fines
    cur.execute("SELECT id FROM fines")
    fine_ids = [row[0] for row in cur.fetchall()]
    
    # Add responses to ~80% of fines
    responses = []
    for fine_id in fine_ids:
        if random.random() < 0.8:  # 80% have responses
            response = random.choice(vendor_responses_pool)
            responses.append((fine_id, response, "Submitted"))
    
    cur.executemany(
        "INSERT INTO vendor_responses(fine_id, vendor_response, status) VALUES(?,?,?)",
        responses
    )
    conn.commit()
    print(f"✓ Inserted {len(responses)} vendor response records")


def populate_billing(conn):
    """Populate billing records (calculated from food counts and fines)."""
    cur = conn.cursor()
    
    billing_records = []
    
    # Get all dates in January with food counts
    cur.execute("""
        SELECT DISTINCT count_date FROM food_counts ORDER BY count_date
    """)
    dates = [row[0] for row in cur.fetchall()]
    
    for billing_date in dates:
        # Get food counts for this date, for all meals
        cur.execute("""
            SELECT meal, total_count
            FROM food_counts WHERE count_date = ?
        """, (billing_date,))
        
        meal_totals = {row['meal']: row['total_count'] for row in cur.fetchall()}
        
        breakfast_total = meal_totals.get('breakfast', 0)
        lunch_total = meal_totals.get('lunch', 0)
        dinner_total = meal_totals.get('dinner', 0)
        
        # Calculate max people (billing is based on max among three meals)
        max_people = max(breakfast_total, lunch_total, dinner_total)
        
        # Rate per person
        rate_per_person = 150.0
        gross_amount = max_people * rate_per_person
        
        # Get fines for this date
        cur.execute("""
            SELECT COALESCE(SUM(amount), 0) FROM fines WHERE fine_date = ?
        """, (billing_date,))
        
        fine_amount = cur.fetchone()[0]
        net_amount = gross_amount - fine_amount
        
        billing_records.append((
            billing_date, breakfast_total, lunch_total, dinner_total,
            max_people, rate_per_person, gross_amount, fine_amount, net_amount
        ))
    
    cur.executemany(
        """INSERT OR IGNORE INTO billing
           (billing_date, breakfast_count, lunch_count, dinner_count, max_people_fed,
            amount_per_person, gross_amount, fine_amount, net_amount)
           VALUES(?,?,?,?,?,?,?,?,?)""",
        billing_records
    )
    conn.commit()
    print(f"✓ Inserted {len(billing_records)} billing records")


def print_summary(conn):
    """Print summary statistics of the database."""
    cur = conn.cursor()
    
    print("\n" + "="*60)
    print("📊 DATABASE SUMMARY - CMC Mess Management System")
    print("="*60)
    
    cur.execute("SELECT COUNT(*) FROM students")
    print(f"\n📚 Students: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM food_counts")
    print(f"🍴 Food Count Records: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM student_feedback")
    feedback_count = cur.fetchone()[0]
    print(f"📝 Feedback Entries: {feedback_count}")
    
    # Average ratings
    cur.execute("""
        SELECT ROUND(AVG(breakfast_rating), 2), ROUND(AVG(lunch_rating), 2), 
               ROUND(AVG(dinner_rating), 2) FROM student_feedback
    """)
    avg_bf, avg_ln, avg_dn = cur.fetchone()
    print(f"\n⭐ Average Ratings:")
    print(f"   Breakfast: {avg_bf}/5 | Lunch: {avg_ln}/5 | Dinner: {avg_dn}/5")
    
    cur.execute("SELECT COUNT(*) FROM fines")
    fines_count = cur.fetchone()[0]
    print(f"\n⚖️  Fines Imposed: {fines_count}")
    
    cur.execute("SELECT SUM(amount) FROM fines")
    total_fines = cur.fetchone()[0] or 0
    print(f"💰 Total Fine Amount: ₹{total_fines}")
    
    cur.execute("SELECT COUNT(*) FROM vendor_responses")
    responses_count = cur.fetchone()[0]
    print(f"📢 Vendor Responses: {responses_count} ({round(responses_count/fines_count*100) if fines_count > 0 else 0}%)")
    
    # Billing summary
    cur.execute("""
        SELECT SUM(max_people_fed), SUM(gross_amount), SUM(fine_amount), SUM(net_amount)
        FROM billing
    """)
    total_people, total_revenue, total_fines_deducted, total_net = cur.fetchone()
    print(f"\n💳 Billing Summary:")
    print(f"   Total People Fed: {total_people}")
    print(f"   Total Revenue: ₹{total_revenue:,.0f}")
    print(f"   Total Fines Deducted: ₹{total_fines_deducted:,.0f}")
    print(f"   Net Amount Payable: ₹{total_net:,.0f}")
    
    print("\n" + "="*60)


def main():
    """Main function to create and populate the database."""
    print("\n🚀 Creating CMC Mess Management SQLite Database...\n")
    
    ensure_db_dir()
    
    # Remove old database if exists
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"🗑️  Removed old database: {DB_PATH}\n")
    
    conn = sqlite3.connect(str(DB_PATH))
    # Enable row_factory for dict-like access in populate_billing
    conn.row_factory = sqlite3.Row 
    try:
        print("🔧 Creating database schema...")
        create_schema(conn)
        print("✓ Schema created\n")
        
        print("📥 Populating database with sample data...\n")
        populate_students(conn, n_students=60)
        populate_food_counts(conn)
        populate_feedback(conn, n_feedback=150)
        populate_fines(conn)
        populate_vendor_responses(conn)
        populate_billing(conn)
        
        print_summary(conn)
        
        print(f"✅ Database successfully created at: {DB_PATH}\n")
        
    except Exception as e:
        print(f"\n❌ Error creating database: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()