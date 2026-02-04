from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_cors import CORS
import sqlite3
import csv
import io
from pathlib import Path
from datetime import datetime

APP = Flask(__name__, static_folder='.')
CORS(APP)

DB_PATH = Path("C:/Users/hp/Desktop/Final_CMC/cmc-mess-feedback-portal/scripts/database/mess_management.db")
def get_db_connection():
    """Create a database connection to mess_management.db."""
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at {DB_PATH}. Please ensure it exists.")
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

# ============================================================================
# STUDENT FEEDBACK ENDPOINTS
# ============================================================================

def query_feedback(start: str, end: str):
    """
    Query student feedback from mess_management.db within a date range.
    Uses the single 'comments' field.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql = """
        SELECT sf.id, s.name AS studentName, s.roll_no AS rollNumber,
               sf.feedback_date AS date,
               sf.breakfast_rating AS breakfastRating,
               sf.lunch_rating AS lunchRating,
               sf.dinner_rating AS dinnerRating,
               sf.comments AS comments -- Corrected to single comments field
        FROM student_feedback sf
        LEFT JOIN students s ON s.id = sf.student_id
        WHERE sf.feedback_date BETWEEN ? AND ?
        ORDER BY sf.feedback_date DESC, s.roll_no ASC
        """
        cur.execute(sql, [start, end])
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows
    except Exception as e:
        print(f"Error querying feedback: {e}")
        return []


@APP.route('/api/feedback')
def api_feedback():
    """Get student feedback."""
    start = request.args.get('start')
    end = request.args.get('end')
    if not start or not end:
        return jsonify({'error': 'start and end query params required (YYYY-MM-DD)'}), 400
    rows = query_feedback(start, end)
    return jsonify(rows)


@APP.route('/api/feedback/csv')
def api_feedback_csv():
    """Download student feedback as CSV."""
    start = request.args.get('start')
    end = request.args.get('end')
    if not start or not end:
        return jsonify({'error': 'start and end query params required (YYYY-MM-DD)'}), 400
    rows = query_feedback(start, end)

    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow([
        'studentName', 'rollNumber', 'date',
        'breakfastRating',
        'lunchRating',
        'dinnerRating', 'comments' # Corrected header
    ])
    for r in rows:
        writer.writerow([
            r.get('studentName', ''), r.get('rollNumber', ''), r.get('date', ''),
            r.get('breakfastRating', ''),
            r.get('lunchRating', ''),
            r.get('dinnerRating', ''), r.get('comments', '') # Corrected data field
        ])

    output = make_response(si.getvalue())
    output.headers['Content-Type'] = 'text/csv; charset=utf-8'
    output.headers['Content-Disposition'] = f'attachment; filename=feedback_{start}_to_{end}.csv'
    return output

@APP.route('/api/feedback', methods=['POST'])
def save_feedback():
    """Save student feedback to the database."""
    try:
        data = request.get_json()
        
        # Get or create student
        student_name = data.get('student_name', 'Unknown')
        student_roll = data.get('student_roll', 'Unknown')
        feedback_date = data.get('feedback_date', datetime.now().strftime('%Y-%m-%d')) # Corrected key to 'feedback_date'
        meal_type = data.get('meal_type', 'Lunch')
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if student exists by roll number
        cur.execute("SELECT id FROM students WHERE roll_no = ?", [student_roll])
        student = cur.fetchone()
        student_id = None
        
        if student:
            student_id = student['id']
        else:
            # Create new student if not exists
            cur.execute("""
                INSERT INTO students (name, roll_no)
                VALUES (?, ?)
            """, [student_name, student_roll])
            student_id = cur.lastrowid
        
        # Calculate meal ratings from items (average of taste and cleanliness ratings for the meal type)
        items = data.get('items', [])
        avg_quality = 0
        if items:
            # Average both taste and cleanliness ratings
            all_ratings = []
            for item in items:
                taste = item.get('taste', 0)
                cleanliness = item.get('cleanliness', 0)
                if taste > 0:
                    all_ratings.append(taste)
                if cleanliness > 0:
                    all_ratings.append(cleanliness)
            avg_quality = sum(all_ratings) / len(all_ratings) if all_ratings else 0
        
        # Determine which meal column to update based on meal_type
        meal_column = f"{meal_type.lower()}_rating"
        
        # Check if record exists for this date
        cur.execute("""
            SELECT id FROM student_feedback 
            WHERE student_id = ? AND feedback_date = ?
        """, [student_id, feedback_date])
        
        existing = cur.fetchone()
        
        # Build the overall comment
        comments = data.get('overall_comment', '')
        
        if existing:
            # Update existing record
            cur.execute(f"""
                UPDATE student_feedback 
                SET {meal_column} = ?, comments = ?
                WHERE id = ?
            """, [int(avg_quality), comments, existing['id']])
        else:
            # Insert new feedback record
            cur.execute("""
                INSERT INTO student_feedback (student_id, feedback_date, breakfast_rating, lunch_rating, dinner_rating, comments)
                VALUES (?, ?, ?, ?, ?, ?)
            """, [student_id, feedback_date, 
                  int(avg_quality) if meal_type.lower() == 'breakfast' else 0,
                  int(avg_quality) if meal_type.lower() == 'lunch' else 0,
                  int(avg_quality) if meal_type.lower() == 'dinner' else 0,
                  comments])
        
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'Feedback saved successfully'}), 200
    except Exception as e:
        print(f"Error saving feedback: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# FOOD COUNTS ENDPOINTS
# ============================================================================

def query_food_counts(start: str, end: str, meal: str | None = None):
    """
    Query food counts from mess_management.db by date range and optional meal filter.
    Uses the new 'student_count', 'faculty_count', 'guest_count', 'total_count' schema.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql = """
        SELECT id, count_date AS date, meal AS mealType,
               student_count AS studentCount, faculty_count AS facultyCount,
               guest_count AS guestCount, total_count AS totalCount
        FROM food_counts
        WHERE count_date BETWEEN ? AND ?
        """
        params = [start, end]
        if meal:
            sql += " AND meal = ?"
            params.append(meal)
        sql += " ORDER BY count_date ASC, meal ASC"
        cur.execute(sql, params)
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows
    except Exception as e:
        print(f"Error querying food counts: {e}")
        return []


@APP.route('/api/food-counts')
def api_food_counts():
    """Get food counts by date range, with optional meal filter."""
    start = request.args.get('start')
    end = request.args.get('end')
    meal = request.args.get('meal') or None
    if not start or not end:
        return jsonify({'error': 'start and end query params required (YYYY-MM-DD)'}), 400
    rows = query_food_counts(start, end, meal)
    return jsonify(rows)


@APP.route('/api/food-counts/csv')
def api_food_counts_csv():
    """Download food counts as CSV."""
    start = request.args.get('start')
    end = request.args.get('end')
    meal = request.args.get('meal') or None
    if not start or not end:
        return jsonify({'error': 'start and end query params required (YYYY-MM-DD)'}), 400
    
    print(f"CSV Export: Fetching food counts from {start} to {end}")
    rows = query_food_counts(start, end, meal)
    print(f"CSV Export: Found {len(rows)} records")

    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(['date', 'mealType', 'studentCount', 'facultyCount', 'guestCount', 'totalCount'])
    for r in rows:
        writer.writerow([
            r.get('date', ''), r.get('mealType', ''), r.get('studentCount', ''),
            r.get('facultyCount', ''), r.get('guestCount', ''), r.get('totalCount', '')
        ])

    csv_content = si.getvalue()
    print(f"CSV Content length: {len(csv_content)} bytes")
    
    output = make_response(csv_content)
    output.headers['Content-Type'] = 'text/csv; charset=utf-8'
    output.headers['Content-Disposition'] = f'attachment; filename=food_counts_{start}_to_{end}.csv'
    return output

@APP.route('/api/food-counts', methods=['POST'])
def save_food_count():
    """Save a food count record to the database."""
    try:
        data = request.get_json()
        count_date = data.get('date')
        meal = data.get('meal')
        student_count = data.get('student_count', 0)
        faculty_count = data.get('faculty_count', 0)
        guest_count = data.get('guest_count', 0)
        
        print(f"Saving food count: date={count_date}, meal={meal}, students={student_count}, faculty={faculty_count}")
        
        if not count_date or not meal:
            return jsonify({'error': 'date and meal are required'}), 400
        
        total_count = student_count + faculty_count + guest_count
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if record exists for this date and meal
        cur.execute(
            "SELECT id FROM food_counts WHERE count_date = ? AND meal = ?",
            (count_date, meal)
        )
        existing = cur.fetchone()
        
        if existing:
            print(f"Updating existing record for {count_date} - {meal}")
            # Update existing record
            cur.execute("""
                UPDATE food_counts 
                SET student_count = ?, faculty_count = ?, guest_count = ?, total_count = ?
                WHERE count_date = ? AND meal = ?
            """, (student_count, faculty_count, guest_count, total_count, count_date, meal))
        else:
            print(f"Inserting new record for {count_date} - {meal}")
            # Insert new record
            cur.execute("""
                INSERT INTO food_counts (count_date, meal, student_count, faculty_count, guest_count, total_count)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (count_date, meal, student_count, faculty_count, guest_count, total_count))
        
        conn.commit()
        conn.close()
        
        print(f"Successfully saved food count")
        return jsonify({'status': 'success', 'message': 'Food count saved successfully'}), 200
    except Exception as e:
        print(f"Error saving food count: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# FOOD QUALITY ENDPOINTS
# ============================================================================

def get_avg_food_quality(start: str, end: str, meal: str | None = None):
    """
    Get average food quality ratings from student_feedback for a date range.
    Returns averages for specific meal if 'meal' is provided, otherwise all three.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        ratings = {}

        if meal == 'breakfast':
            query = "SELECT ROUND(AVG(breakfast_rating), 2) AS avg_rating, COUNT(breakfast_rating) AS feedback_count FROM student_feedback WHERE feedback_date BETWEEN ? AND ? AND breakfast_rating IS NOT NULL"
            cur.execute(query, (start, end))
            result = cur.fetchone()
            if result and result['avg_rating'] is not None:
                ratings['breakfast_rating'] = result['avg_rating']
                ratings['breakfast_feedback_count'] = result['feedback_count']
        elif meal == 'lunch':
            query = "SELECT ROUND(AVG(lunch_rating), 2) AS avg_rating, COUNT(lunch_rating) AS feedback_count FROM student_feedback WHERE feedback_date BETWEEN ? AND ? AND lunch_rating IS NOT NULL"
            cur.execute(query, (start, end))
            result = cur.fetchone()
            if result and result['avg_rating'] is not None:
                ratings['lunch_rating'] = result['avg_rating']
                ratings['lunch_feedback_count'] = result['feedback_count']
        elif meal == 'dinner':
            query = "SELECT ROUND(AVG(dinner_rating), 2) AS avg_rating, COUNT(dinner_rating) AS feedback_count FROM student_feedback WHERE feedback_date BETWEEN ? AND ? AND dinner_rating IS NOT NULL"
            cur.execute(query, (start, end))
            result = cur.fetchone()
            if result and result['avg_rating'] is not None:
                ratings['dinner_rating'] = result['avg_rating']
                ratings['dinner_feedback_count'] = result['feedback_count']
        else: # No specific meal, get all
            query = """
                SELECT
                    ROUND(AVG(breakfast_rating), 2) AS avg_breakfast_rating,
                    COUNT(breakfast_rating) AS breakfast_feedback_count,
                    ROUND(AVG(lunch_rating), 2) AS avg_lunch_rating,
                    COUNT(lunch_rating) AS lunch_feedback_count,
                    ROUND(AVG(dinner_rating), 2) AS avg_dinner_rating,
                    COUNT(dinner_rating) AS dinner_feedback_count
                FROM student_feedback
                WHERE feedback_date BETWEEN ? AND ?
            """
            cur.execute(query, (start, end))
            result = cur.fetchone()
            if result:
                for key, value in result.items():
                    if value is not None:
                        ratings[key] = value

        conn.close()
        return ratings
    except Exception as e:
        print(f"Error getting average food quality: {e}")
        return {}


@APP.route('/api/food-quality')
def api_food_quality():
    """
    Get average food quality ratings for a period.
    Optional 'meal' param (breakfast, lunch, dinner) to get specific meal's average.
    """
    start = request.args.get('start')
    end = request.args.get('end')
    meal = request.args.get('meal') or None
    if not start or not end:
        return jsonify({'error': 'start and end query params required (YYYY-MM-DD)'}), 400
    quality = get_avg_food_quality(start, end, meal)
    return jsonify(quality)

# ============================================================================
# FINES ENDPOINTS (NEW)
# ============================================================================

def query_fines(start: str, end: str, response_status_filter: str = 'all'):
    """
    Query fines within a date range, optionally filtered by vendor response status.
    Returns fines with their associated vendor response.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql = """
        SELECT f.id, f.fine_date AS date, f.meal, f.reason, f.amount, f.imposed_by AS imposedBy,
               vr.vendor_response AS vendorResponse,
               vr.status AS responseStatus
        FROM fines f
        LEFT JOIN vendor_responses vr ON f.id = vr.fine_id
        WHERE f.fine_date BETWEEN ? AND ?
        """
        params = [start, end]

        if response_status_filter == 'submitted':
            sql += " AND vr.vendor_response IS NOT NULL"
        elif response_status_filter == 'not_submitted':
            sql += " AND vr.vendor_response IS NULL"
        # 'all' needs no additional WHERE clause

        sql += " ORDER BY f.fine_date DESC"
        cur.execute(sql, params)
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows
    except Exception as e:
        print(f"Error querying fines: {e}")
        return []

@APP.route('/api/fines')
def api_fines():
    """Get fines by date range, with optional response status filter."""
    start = request.args.get('start')
    end = request.args.get('end')
    response_status_filter = request.args.get('response_status', 'all') # 'all', 'submitted', 'not_submitted'

    if not start or not end:
        return jsonify({'error': 'start and end query params required (YYYY-MM-DD)'}), 400
    rows = query_fines(start, end, response_status_filter)
    return jsonify(rows)

@APP.route('/api/fines/csv')
def api_fines_csv():
    """Download fines as CSV."""
    start = request.args.get('start')
    end = request.args.get('end')
    response_status_filter = request.args.get('response_status', 'all')

    if not start or not end:
        return jsonify({'error': 'start and end query params required (YYYY-MM-DD)'}), 400
    rows = query_fines(start, end, response_status_filter)

    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(['date', 'meal', 'reason', 'amount', 'imposedBy', 'vendorResponse', 'responseStatus']) # Added vendorResponse and responseStatus
    for r in rows:
        writer.writerow([
            r.get('date', ''), r.get('meal', ''), r.get('reason', ''),
            r.get('amount', ''), r.get('imposedBy', ''),
            r.get('vendorResponse', ''), r.get('responseStatus', '')
        ])
    output = make_response(si.getvalue())
    output.headers['Content-Type'] = 'text/csv; charset=utf-8'
    output.headers['Content-Disposition'] = f'attachment; filename=fines_{start}_to_{end}.csv'
    return output

@APP.route('/api/fines', methods=['POST'])
def save_fine():
    """Save a new fine to the database."""
    try:
        data = request.get_json()
        fine_date = data.get('date')
        meal = data.get('meal')
        reason = data.get('reason')
        amount = data.get('amount')
        imposed_by = data.get('imposedBy')
        
        if not all([fine_date, meal, reason, amount, imposed_by]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO fines (fine_date, meal, reason, amount, imposed_by)
            VALUES (?, ?, ?, ?, ?)
        """, [fine_date, meal, reason, int(amount), imposed_by])
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Fine imposed successfully'}), 201
    except Exception as e:
        print(f"Error saving fine: {e}")
        return jsonify({'error': str(e)}), 500

@APP.route('/api/fines/<int:fine_id>', methods=['DELETE'])
def delete_fine(fine_id):
    """Delete a fine from the database."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # First delete any associated vendor responses
        cur.execute("DELETE FROM vendor_responses WHERE fine_id = ?", [fine_id])
        
        # Then delete the fine
        cur.execute("DELETE FROM fines WHERE id = ?", [fine_id])
        conn.commit()
        
        rows_deleted = cur.rowcount
        conn.close()
        
        if rows_deleted == 0:
            return jsonify({'error': 'Fine not found'}), 404
        
        return jsonify({'success': True, 'message': 'Fine deleted successfully'}), 200
    except Exception as e:
        print(f"Error deleting fine: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# VENDOR RESPONSES ENDPOINTS (NEW)
# ============================================================================

def query_vendor_responses(fine_id: int | None = None):
    """Query vendor responses, optionally filtered by fine_id."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql = """
        SELECT id, fine_id, vendor_response, submitted_at AS submittedAt, status
        FROM vendor_responses
        """
        params = []
        if fine_id:
            sql += " WHERE fine_id = ?"
            params.append(fine_id)
        sql += " ORDER BY submitted_at DESC"
        cur.execute(sql, params)
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows
    except Exception as e:
        print(f"Error querying vendor responses: {e}")
        return []

@APP.route('/api/vendor-responses')
def api_vendor_responses():
    """Get vendor responses, optionally filtered by fine_id."""
    fine_id = request.args.get('fine_id', type=int)
    rows = query_vendor_responses(fine_id)
    return jsonify(rows)

@APP.route('/api/vendor-responses', methods=['POST'])
def save_vendor_response():
    """Save or update a vendor response to a fine."""
    try:
        data = request.get_json()
        fine_id = data.get('fine_id')
        vendor_response_text = data.get('vendor_response')
        status = data.get('status', 'Submitted') # Default status
        
        if not all([fine_id, vendor_response_text]):
            return jsonify({'error': 'Missing required fields: fine_id, vendor_response'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if a response already exists for this fine_id
        cur.execute("SELECT id FROM vendor_responses WHERE fine_id = ?", [fine_id])
        existing_response = cur.fetchone()
        
        if existing_response:
            # Update existing response
            cur.execute("""
                UPDATE vendor_responses
                SET vendor_response = ?, submitted_at = CURRENT_TIMESTAMP, status = ?
                WHERE id = ?
            """, [vendor_response_text, status, existing_response['id']])
        else:
            # Insert new response
            cur.execute("""
                INSERT INTO vendor_responses (fine_id, vendor_response, status)
                VALUES (?, ?, ?)
            """, [fine_id, vendor_response_text, status])
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Vendor response saved successfully'}), 201
    except Exception as e:
        print(f"Error saving vendor response: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# BILLING ENDPOINTS (NEW)
# ============================================================================

def query_billing(start: str, end: str):
    """Query billing records within a date range."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql = """
        SELECT id, billing_date AS date,
               breakfast_count AS breakfastCount,
               lunch_count AS lunchCount,
               dinner_count AS dinnerCount,
               max_people_fed AS maxPeopleFed,
               amount_per_person AS amountPerPerson,
               gross_amount AS grossAmount,
               fine_amount AS fineAmount,
               net_amount AS netAmount
        FROM billing
        WHERE billing_date BETWEEN ? AND ?
        ORDER BY billing_date ASC
        """
        cur.execute(sql, [start, end])
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows
    except Exception as e:
        print(f"Error querying billing: {e}")
        return []

@APP.route('/api/billing')
def api_billing():
    """Get billing records by date range."""
    start = request.args.get('start')
    end = request.args.get('end')
    if not start or not end:
        return jsonify({'error': 'start and end query params required (YYYY-MM-DD)'}), 400
    rows = query_billing(start, end)
    return jsonify(rows)

@APP.route('/api/billing/csv')
def api_billing_csv():
    """Download billing records as CSV."""
    start = request.args.get('start')
    end = request.args.get('end')
    if not start or not end:
        return jsonify({'error': 'start and end query params required (YYYY-MM-DD)'}), 400
    rows = query_billing(start, end)

    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow([
        'date', 'breakfastCount', 'lunchCount', 'dinnerCount',
        'maxPeopleFed', 'amountPerPerson', 'grossAmount', 'fineAmount', 'netAmount'
    ])
    for r in rows:
        writer.writerow([
            r.get('date', ''), r.get('breakfastCount', ''), r.get('lunchCount', ''),
            r.get('dinnerCount', ''), r.get('maxPeopleFed', ''), r.get('amountPerPerson', ''),
            r.get('grossAmount', ''), r.get('fineAmount', ''), r.get('netAmount', '')
        ])
    output = make_response(si.getvalue())
    output.headers['Content-Type'] = 'text/csv; charset=utf-8'
    output.headers['Content-Disposition'] = f'attachment; filename=billing_{start}_to_{end}.csv'
    return output

# ============================================================================
# DEBUG ENDPOINTS
# ============================================================================

@APP.route('/api/debug/food-counts')
def debug_food_counts():
    """Debug endpoint - get all food counts in database."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM food_counts ORDER BY count_date DESC LIMIT 20")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        
        total = len(rows)
        print(f"Debug: Found {total} food count records")
        return jsonify({'total_records': total, 'data': rows})
    except Exception as e:
        print(f"Debug error: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# HEALTH CHECK
# ============================================================================

@APP.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM students")
        count = cur.fetchone()[0]
        conn.close()

        return jsonify({
            'status': 'OK',
            'database': 'Connected',
            'students_count': count
        })
    except Exception as e:
        return jsonify({'status': 'ERROR', 'message': str(e)}), 500

# ============================================================================
# SERVE STATIC FILES
# ============================================================================

@APP.route('/', defaults={'path': 'index.html'})
@APP.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('.', path)


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Starting CMC Mess Management API Server")
    print("="*60)
    print("\n📍 Server running at: http://0.0.0.0:8000")
    print("\n✅ API Endpoints Available:")
    print("   - /api/feedback?start=YYYY-MM-DD&end=YYYY-MM-DD")
    print("   - /api/feedback/csv?start=YYYY-MM-DD&end=YYYY-MM-DD")
    print("   - /api/food-counts?start=YYYY-MM-DD&end=YYYY-MM-DD[&meal=breakfast|lunch|dinner]")
    print("   - /api/food-counts/csv?start=YYYY-MM-DD&end=YYYY-MM-DD[&meal=breakfast|lunch|dinner]")
    print("   - /api/food-quality?start=YYYY-MM-DD&end=YYYY-MM-DD[&meal=breakfast|lunch|dinner]")
    print("   - /api/fines?start=YYYY-MM-DD&end=YYYY-MM-DD[&response_status=all|submitted|not_submitted]")
    print("   - /api/fines/csv?start=YYYY-MM-DD&end=YYYY-MM-DD[&response_status=all|submitted|not_submitted]")
    print("   - POST /api/fines (create fine)")
    print("   - DELETE /api/fines/<fine_id> (delete fine)")
    print("   - /api/vendor-responses[&fine_id=ID]")
    print("   - POST /api/vendor-responses (create/update vendor response)")
    print("   - /api/billing?start=YYYY-MM-DD&end=YYYY-MM-DD")
    print("   - /api/billing/csv?start=YYYY-MM-DD&end=YYYY-MM-DD")
    print("   - /api/health")
    print("\n💾 Database: database/mess_management.db")
    print("="*60 + "\n")

    APP.run(host='0.0.0.0', port=8000, debug=True)