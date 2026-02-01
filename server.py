from flask import Flask, request, jsonify, send_from_directory, make_response
import sqlite3
import csv
import io
from pathlib import Path

APP = Flask(__name__, static_folder='.')
DB_PATH = Path('database') / 'feedback_january.db'


def query_feedback(start: str, end: str, meal: str | None = None):
    if not DB_PATH.exists():
        return []
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    sql = """
    SELECT s.name AS studentName, s.roll_no AS rollNumber,
           f.feedback_date AS date, f.meal AS mealType,
           f.rating AS overallRating, f.comments AS comments
    FROM feedback f
    LEFT JOIN students s ON s.id = f.student_id
    WHERE f.feedback_date >= ? AND f.feedback_date <= ?
    """
    params = [start, end]
    if meal:
        sql += " AND f.meal = ?"
        params.append(meal)
    sql += " ORDER BY f.feedback_date ASC"
    cur.execute(sql, params)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


@APP.route('/api/feedback')
def api_feedback():
    start = request.args.get('start')
    end = request.args.get('end')
    meal = request.args.get('meal') or None
    if not start or not end:
        return jsonify({'error': 'start and end query params required (YYYY-MM-DD)'}), 400
    rows = query_feedback(start, end, meal)
    return jsonify(rows)


@APP.route('/api/feedback/csv')
def api_feedback_csv():
    start = request.args.get('start')
    end = request.args.get('end')
    meal = request.args.get('meal') or None
    if not start or not end:
        return jsonify({'error': 'start and end query params required (YYYY-MM-DD)'}), 400
    rows = query_feedback(start, end, meal)

    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(['studentName', 'rollNumber', 'date', 'mealType', 'overallRating', 'comments'])
    for r in rows:
        writer.writerow([r.get('studentName',''), r.get('rollNumber',''), r.get('date',''), r.get('mealType',''), r.get('overallRating',''), r.get('comments','')])

    output = make_response(si.getvalue())
    output.headers['Content-Type'] = 'text/csv; charset=utf-8'
    output.headers['Content-Disposition'] = f'attachment; filename=feedback_{start}_to_{end}.csv'
    return output


@APP.route('/', defaults={'path': 'index.html'})
@APP.route('/<path:path>')
def static_proxy(path):
    # Serve static files from repo root
    return send_from_directory('.', path)


if __name__ == '__main__':
    print('Starting server on http://0.0.0.0:8000 (serving repo root)')
    APP.run(host='0.0.0.0', port=8000, debug=True)
