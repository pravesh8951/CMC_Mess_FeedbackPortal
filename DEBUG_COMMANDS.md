# Quick Debug Commands

## Browser Console Commands (Press F12, go to Console tab)

### Check database contents
```javascript
fetch('/api/debug/food-counts')
  .then(r => r.json())
  .then(d => console.log('Total records:', d.total_records, 'Data:', d.data))
```

### Query API directly for today
```javascript
const today = new Date().toISOString().split('T')[0];
const tomorrow = new Date(Date.now() + 86400000).toISOString().split('T')[0];
fetch(`/api/food-counts?start=${today}&end=${tomorrow}`)
  .then(r => r.json())
  .then(d => console.log('Records found:', d.length, 'Data:', d))
```

### Test CSV generation
```javascript
const today = new Date().toISOString().split('T')[0];
const tomorrow = new Date(Date.now() + 86400000).toISOString().split('T')[0];
fetch(`/api/food-counts/csv?start=${today}&end=${tomorrow}`)
  .then(r => r.text())
  .then(text => console.log('CSV rows:', text.split('\n').length, 'Content:', text))
```

### Manually trigger save (for testing)
```javascript
// This saves breakfast counts for tomorrow
const tomorrow = new Date(Date.now() + 86400000).toISOString().split('T')[0];
fetch('/api/food-counts', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        date: tomorrow,
        meal: 'breakfast',
        student_count: 100,
        faculty_count: 10,
        guest_count: 0
    })
})
.then(r => r.json())
.then(d => console.log('Save response:', d))
```

### Refresh recent counts table
```javascript
loadRecentFoodCounts()
```

---

## PowerShell / Terminal Commands

### Check if database file exists
```powershell
Test-Path "C:\Users\hp\Desktop\Final_CMC\cmc-mess-feedback-portal\scripts\database\mess_management.db"
```

### Query database directly (if sqlite3 installed)
```powershell
sqlite3 "C:\Users\hp\Desktop\Final_CMC\cmc-mess-feedback-portal\scripts\database\mess_management.db" "SELECT * FROM food_counts ORDER BY count_date DESC LIMIT 10"
```

### Check recent food counts
```powershell
sqlite3 "C:\Users\hp\Desktop\Final_CMC\cmc-mess-feedback-portal\scripts\database\mess_management.db" "SELECT COUNT(*) as total_records FROM food_counts"
```

### View table structure
```powershell
sqlite3 "C:\Users\hp\Desktop\Final_CMC\cmc-mess-feedback-portal\scripts\database\mess_management.db" ".schema food_counts"
```

### Get today's records
```powershell
$today = (Get-Date).ToString("yyyy-MM-dd")
sqlite3 "C:\Users\hp\Desktop\Final_CMC\cmc-mess-feedback-portal\scripts\database\mess_management.db" "SELECT * FROM food_counts WHERE count_date = '$today'"
```

---

## Server Terminal Output to Watch For

### When Adding Food Count
```
Saving food count: date=2026-02-02, meal=breakfast, students=100, faculty=10
Inserting new record for 2026-02-02 - breakfast
Successfully saved food count
```

### When Exporting CSV
```
CSV Export: Fetching food counts from 2026-02-02 to 2026-02-02
CSV Export: Found 3 records
CSV Content length: 234 bytes
```

### When Querying API
```
GET /api/food-counts?start=2026-02-02&end=2026-02-02
```

---

## Troubleshooting Checklist

- [ ] Server running: `python server.py` in terminal
- [ ] Database exists at: `scripts/database/mess_management.db`
- [ ] Can access: `http://localhost:8000`
- [ ] Can see debug endpoint: `http://localhost:8000/api/debug/food-counts`
- [ ] Database returns data: Run SQLite query for food_counts
- [ ] API returns data: Call `/api/food-counts` with today's date
- [ ] Save works: Check server console for "Successfully saved" message
- [ ] CSV generated: Check server console for "CSV Content length" > 50 bytes

---

## Quick Fix Steps

### If CSV Still Empty After Adding Data

1. **Restart server:**
```powershell
# Press Ctrl+C in server terminal
# Then run again:
python server.py
```

2. **Clear browser cache:**
```
Ctrl+Shift+Delete in browser
Select "All time"
Check "Cookies and other site data"
Click Clear
```

3. **Test with debug endpoint:**
   - Open: `http://localhost:8000/api/debug/food-counts`
   - Should show records in JSON format

4. **Manually test CSV:**
```
http://localhost:8000/api/food-counts/csv?start=2026-02-02&end=2026-02-02
```

5. **Check server logs:**
   - Look for "CSV Export: Found X records"
   - If "Found 0 records" = data not in database
   - If "Found 3 records" = data exists but CSV export issue

---

## Date Calculations

### Today's date format
```javascript
new Date().toISOString().split('T')[0]  // Returns: 2026-02-02
```

### Tomorrow's date format
```javascript
new Date(Date.now() + 86400000).toISOString().split('T')[0]  // Returns: 2026-02-03
```

### 30 days from today
```javascript
new Date(Date.now() + (30 * 24 * 60 * 60 * 1000)).toISOString().split('T')[0]
```

---

## API Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/food-counts` | GET | Get food counts (with date range) |
| `/api/food-counts` | POST | Save new/update food count |
| `/api/food-counts/csv` | GET | Export food counts to CSV |
| `/api/debug/food-counts` | GET | View all records in database |
| `/api/feedback` | GET | Get feedback |
| `/api/feedback` | POST | Save feedback |
| `/api/feedback/csv` | GET | Export feedback to CSV |

---

## Important Files

- **Database:** `scripts/database/mess_management.db`
- **Server:** `server.py`
- **Warden Page:** `warden.html`
- **Current Date:** 2026-02-02

---

## Connection String

```
Database: C:/Users/hp/Desktop/Final_CMC/cmc-mess-feedback-portal/scripts/database/mess_management.db
Server: Flask on http://0.0.0.0:8000
Frontend: file:///.../warden.html (opened via server)
```

