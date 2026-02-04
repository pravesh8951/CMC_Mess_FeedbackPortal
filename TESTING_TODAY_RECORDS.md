# Testing & Debugging Guide - Today/Future Records Fix

## Changes Made

### 1. Updated loadRecentFoodCounts()
**Change:** Switched from hardcoded January 2026 to today onwards (next 30 days)

**Before:**
```javascript
const response = await fetch('/api/food-counts?start=2026-01-01&end=2026-01-31');
```

**After:**
```javascript
const today = new Date();
const start = today.toISOString().split('T')[0];
const endDate = new Date(today.getTime() + (30 * 24 * 60 * 60 * 1000));
const end = endDate.toISOString().split('T')[0];
const response = await fetch(`/api/food-counts?start=${start}&end=${end}`);
```

**Result:** Now shows TODAY + next 30 days, not past January data

---

### 2. Updated loadRecentFines()
**Change:** Same as food counts - switched to today onwards

**Result:** Fines table now shows current and future fines only

---

### 3. Enhanced server.py with Debugging
Added print statements to trace:
- When food counts are saved
- Whether records are inserted or updated
- CSV export queries
- Number of records found

---

### 4. Added Debug Endpoint
**Endpoint:** `GET /api/debug/food-counts`

**Purpose:** Check what's actually in the database

**Response:** Shows all food count records

---

## Step-by-Step Testing

### Test 1: Add Food Count Today
```
1. Open Warden Dashboard
2. Click "Add Food Count"
3. Select Date: TODAY (or tomorrow - it defaults to tomorrow)
4. Enter counts:
   - Student Breakfast: 100
   - Student Lunch: 150
   - Student Dinner: 120
   - Faculty Breakfast: 10
   - Faculty Lunch: 15
   - Faculty Dinner: 12
5. Click "Save Food Count"
6. ✅ See success message
7. ✅ Form fields clear
8. ✅ Data should appear in Recent Food Counts table
```

### Test 2: Check Recent Food Counts Table
After adding (from Test 1):
```
1. Immediately look at "Recent Food Counts" table
2. ✅ Should see TODAY'S date (not January dates)
3. ✅ Should see YOUR counts in Breakfast/Lunch/Dinner columns
4. Maximum People Fed should be 150 (highest meal count)
```

### Test 3: Export to CSV
```
1. With today's data visible in table
2. Click "Export CSV" button
3. File downloads: food_counts_2026-02-02_to_2026-03-04.csv
4. Open in Excel or text editor
5. ✅ Should have HEADER row: date, mealType, studentCount, facultyCount, guestCount, totalCount
6. ✅ Should have DATA rows with your values
7. ✅ NOT EMPTY
```

### Test 4: Generate Report & Export
```
1. Go to "View Food Count Report"
2. Select "Custom" date range mode
3. Set Start Date: TODAY (2026-02-02)
4. Set End Date: TODAY (2026-02-02)
5. Click "Search" button
6. ✅ Should see your today's data in report
7. Click "Export CSV"
8. ✅ File downloads with your data
9. ✅ NOT EMPTY
```

### Test 5: Data Persistence
```
1. Add food counts for today
2. Close browser completely
3. Reopen browser
4. Go to Warden Dashboard
5. ✅ Data still appears in Recent Food Counts
6. ✅ Data persists after refresh
```

---

## Debugging Steps

### If CSV is Still Empty

**Step 1: Check Server Console**
```
When you add food count, you should see in terminal:
"Saving food count: date=2026-02-02, meal=breakfast, students=100, faculty=10"
"Inserting new record for 2026-02-02 - breakfast"
"Successfully saved food count"

When you export CSV, you should see:
"CSV Export: Fetching food counts from 2026-02-02 to 2026-02-02"
"CSV Export: Found 3 records"  (3 = breakfast, lunch, dinner)
"CSV Content length: 234 bytes"
```

**If not appearing:** Server not receiving the requests or saving is failing

---

### Step 2: Check Database Directly
```
In browser console (F12), run:
fetch('/api/debug/food-counts')
  .then(r => r.json())
  .then(d => console.log(d))

Or in new browser tab, open:
http://localhost:8000/api/debug/food-counts

Response should show:
{
  "total_records": 3,
  "data": [
    {
      "id": 1,
      "count_date": "2026-02-02",
      "meal": "breakfast",
      "student_count": 100,
      ...
    },
    ...
  ]
}
```

**If empty:** Data not being saved to database

---

### Step 3: Check API Directly
```
In browser console:
fetch('/api/food-counts?start=2026-02-02&end=2026-02-02')
  .then(r => r.json())
  .then(d => console.log(d))

Should return array with 3 records (breakfast, lunch, dinner)
```

**If empty:** Query issue

---

### Step 4: Check Network Requests
```
Browser F12 → Network tab
1. Add food count and save
2. Look for POST request to /api/food-counts
3. Check:
   - Status: 200 OK
   - Response: {"status": "success", ...}
   - Payload shows correct data
4. If Status: 400 or 500, error occurred
```

---

## Common Issues & Solutions

### Issue 1: CSV File Empty
**Possible causes:**
- Dates not selected when exporting
- Data not saved to database
- Database query returning no records

**Solution:**
1. Make sure you added food counts
2. Check `/api/debug/food-counts` to confirm data exists
3. Try exporting with same date as added record

---

### Issue 2: Recently Added Counts Not Showing
**Possible causes:**
- Data saved to wrong date
- loadRecentFoodCounts() not being called
- API returning empty

**Solution:**
1. Open Network tab (F12)
2. Add food count
3. Watch for POST /api/food-counts - should be Status 200
4. Watch for GET /api/food-counts - should return your data

---

### Issue 3: Showing Past Dates Instead of Today
**This is now FIXED** - loadRecentFoodCounts() now shows today onwards

**If still showing January:**
1. Clear browser cache (Ctrl+Shift+Delete)
2. Close and reopen browser
3. Restart server

---

## Quick Checklist

- [ ] Added food count for today
- [ ] Success message appeared
- [ ] Form fields cleared
- [ ] Data appears in Recent Food Counts table
- [ ] Data shows TODAY'S date (not January)
- [ ] Can export CSV with data (not empty)
- [ ] Can generate custom report with today's data
- [ ] Data persists after page refresh

---

## File Changes Summary

**warden.html:**
- Line ~1008: Updated loadRecentFoodCounts() to use today+30 days
- Line ~1415: Updated loadRecentFines() to use today+30 days

**server.py:**
- Line ~173: Enhanced CSV endpoint with debug logging
- Line ~207: Enhanced POST endpoint with debug logging
- Line ~489: Added debug endpoint `/api/debug/food-counts`

---

## Important Notes

1. **Default date for adding:** Tomorrow (not today)
   - Reason: Allows planning for next day meals
   - You can still select today if needed

2. **Recent Food Counts table:**
   - Shows next 30 days
   - Sorted by most recent first
   - Updated instantly after save

3. **CSV export:**
   - Downloads with filename: `food_counts_[START]_to_[END].csv`
   - Must select date range before exporting
   - Contains all meals for selected range

4. **Date format:** YYYY-MM-DD (2026-02-02)
   - Input type=date handles this automatically
   - Server validates and processes correctly

---

## Next Steps if Issues Persist

1. **Restart server:** Stop and restart Python server
2. **Check database:** Verify mess_management.db exists and has food_counts table
3. **Check permissions:** Ensure database file is writable
4. **Check dates:** Verify dates are in correct YYYY-MM-DD format
5. **Clear cache:** Browser cache might have old code

