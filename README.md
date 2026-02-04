# 🍽️ CMC Mess Management & Feedback Portal

> **A comprehensive web-based mess management and feedback system for Coimbatore Marine College (CMC) with role-based dashboards for Wardens, Vendors, and Admins.**

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [System Architecture](#system-architecture)
4. [User Roles & Dashboards](#user-roles--dashboards)
5. [Installation & Setup](#installation--setup)
6. [Login Credentials](#login-credentials)
7. [How to Use](#how-to-use)
8. [File Structure](#file-structure)
9. [Technical Stack](#technical-stack)
10. [Database Structure](#database-structure)
11. [Key Achievements](#key-achievements)

---

## 🎯 Project Overview

The **CMC Mess Management & Feedback Portal** is a modern, role-based web application designed to streamline mess operations at Coimbatore Marine College. The system enables:

- **Students** to submit feedback on food quality
- **Wardens** to monitor food counts, view feedback, and impose fines on vendors
- **Vendors** to view feedback, give justifications, and track their performance
- **Admins** to oversee all operations, manage data, and generate reports

**Purpose:** Create a transparent, efficient feedback mechanism that improves mess food quality through data-driven insights and vendor accountability.

---

## ⭐ Key Features

### 🎓 Student Feedback Form (index.html)
✅ **Simple & Intuitive Interface**
- Enter name and roll number
- Automatic meal detection (Breakfast/Lunch/Dinner based on time)
- Rate individual food items on 4 criteria:
  - **Taste** ⭐
  - **Quality** ⭐
  - **Quantity** ⭐
  - **Cleanliness** ⭐
- Add custom items not in the default menu
- Optional comments for detailed feedback
- Real-time form validation
- Responsive design (mobile-friendly)

✅ **Data Management**
- All data stored in browser's localStorage
- No server required for student feedback
- Data persists even after browser closes
- Automatic 30-day data retention

---

### 👨‍💼 Warden Dashboard (warden.html)
✅ **1. Add Next-Day Food Count**
- Date selection for meal planning
- Enter food counts for:
  - Breakfast, Lunch, Dinner (Students)
  - Breakfast, Lunch, Dinner (Faculty)
- Helps vendors prepare appropriate quantities
- Used for billing calculations

✅ **2. View Student Feedback**
- Real-time feedback monitoring
- Filter by date range
- Filter by meal type (Breakfast/Lunch/Dinner)
- View statistics:
  - Total feedbacks received
  - Average rating across all criteria
  - Item-wise feedback
  - Quality trend analysis
- Identify recurring issues
- Export feedback reports

✅ **3. Impose Fines on Vendors**
- Select vendor/mess (A, B, or C)
- Choose fine reason:
  - Poor Quality Food
  - Hygiene Issue
  - Late Service
  - Wrong Item Served
  - Expired/Spoiled Food
  - Other
- Enter fine amount
- Select meal type
- Add detailed remarks
- Fine notifications sent to vendors

✅ **4. Monitor Food Quality**
- Dashboard overview of food counts
- Recent fines imposed
- Quality metrics and trends
- Vendor performance tracking

---

### 🏪 Vendor Dashboard (vendor.html)
✅ **1. View Student Feedback**
- See all feedback about their mess
- Filter by date range
- View:
  - Item ratings
  - Overall meal ratings
  - Student comments
- Identify improvement areas
- Compare performance metrics

✅ **2. Give Justifications**
- Respond to negative feedback
- Explain quality issues
- Provide improvement plans
- Track justification history

✅ **3. View Fines**
- See all fines imposed by warden
- View fine reasons and amount
- Check fine dates and meal types
- Track payment status
- Respond with justifications

✅ **4. View Billing**
- Check billing records
- View earnings/charges
- Download billing statements
- Track payment history

---

### 👨‍💻 Admin Dashboard (admin.html)
✅ **Real-time Analytics**
- Dashboard overview with key metrics
- View all student feedback
- Monitor all vendors' performance
- Track all fines imposed
- System usage statistics

✅ **Interactive Charts**
- Average rating trends
- Meal type distribution (Pie charts)
- Top-rated items (Bar charts)
- Daily submission trends
- Vendor performance comparison

✅ **Report Generation**
- Daily reports with full details
- Weekly reports (7 separate sheets)
- Monthly reports (30 separate sheets)
- Custom date range reports
- Excel export (.xlsx format)

✅ **Data Management**
- Period filtering (Today/Week/Month/All)
- Comprehensive data tables
- Student details and roll numbers
- Fine history tracking
- Food count records
- Data consolidation (no duplicates)

---

## 🏗️ System Architecture

### Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Backend:** Python Flask (for advanced features)
- **Database:** SQLite (mess_management.db)
- **Storage:** Browser localStorage (for client-side data)
- **Charts:** Chart.js (for analytics visualization)
- **Export:** Excel (.xlsx) with custom formatting
- **Responsive Design:** Mobile-first CSS

### Data Flow
```
Student Feedback Form (index.html)
         ↓
    localStorage/SQLite Database
         ↓
Warden/Vendor/Admin Dashboards
         ↓
    Real-time Analytics & Reports
```

---

## 👥 User Roles & Dashboards

| Role | File | Purpose | Access Level |
|------|------|---------|--------------|
| **Student** | `index.html` | Submit meal feedback | Public |
| **Warden** | `warden.html` | Monitor & manage operations | Restricted |
| **Vendor** | `vendor.html` | View feedback & respond | Restricted |
| **Admin** | `admin.html` | System oversight & reports | Restricted |

---

## 🚀 Installation & Setup

### Prerequisites
- Web browser (Chrome, Firefox, Edge, Safari)
- Python 3.7+ (for server.py features)
- Git (optional, for version control)

### Step 1: Download/Clone Repository
```bash
# Clone from GitHub (if available)
git clone <repository-url>

# Or download the ZIP file and extract it
```

### Step 2: Ensure Project Structure
```
cmc-mess-feedback-portal/
├── index.html           # Student feedback form
├── login.html           # Role-based login page
├── warden.html          # Warden dashboard
├── vendor.html          # Vendor dashboard
├── admin.html           # Admin dashboard
├── server.py            # Python backend (optional)
├── assets/
│   └── logo.png         # CMC college logo
├── scripts/
│   ├── create_feedback_db.py
│   └── database/
│       └── mess_management.db
└── README.md            # This file
```

### Step 3: Start the Application
**Option A: Direct Browser Opening**
1. Navigate to: `C:\Users\hp\Desktop\Final_CMC\cmc-mess-feedback-portal`
2. Double-click `login.html` OR `index.html`
3. Your browser will open the application

**Option B: Using VS Code Live Server**
1. Open project folder in VS Code
2. Right-click on `login.html`
3. Select "Open with Live Server"
4. Browser opens automatically

**Option C: Using Python Server (for database features)**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask server
python server.py

# Access at http://localhost:5000
```

---

## 🔐 Login Credentials

### For Students
- **URL:** Open `index.html` directly
- **No login required** - Complete feedback form immediately

### For Warden
- **URL:** `login.html` → Select "Warden"
- **Username:** `warden`
- **Password:** `warden123`

### For Vendor
- **URL:** `login.html` → Select "Vendor"
- **Username:** `vendor`
- **Password:** `vendor123`
- **Mess Selection:** Choose from Mess A, B, or C

### For Admin
- **URL:** `login.html` → Select "Admin"
- **Username:** `admin`
- **Password:** `admin123`

---

## 📖 How to Use

### 🎓 For Students
1. **Open Feedback Form**
   - Open `index.html` in browser
   - No login required

2. **Enter Personal Details**
   - Full Name
   - Roll Number

3. **Rate the Food**
   - Current meal type appears automatically (Breakfast/Lunch/Dinner)
   - Rate each item using star ratings (1-5 stars)
   - Rate on: Taste, Quality, Quantity, Cleanliness

4. **Add Comments**
   - Optional: Add detailed comments for each item
   - Suggest improvements

5. **Add Custom Items**
   - Click "➕ Add Other Item" if food item not in menu
   - Rate custom items same as menu items

6. **Submit Feedback**
   - Click "✓ Submit Feedback" button
   - See confirmation message
   - Option to submit more feedback

---

### 👨‍💼 For Wardens
1. **Login**
   - Open `login.html`
   - Select "Warden" card
   - Username: `warden`, Password: `warden123`

2. **Add Next-Day Food Count**
   - Click "📅 Add Next-Day Food Count" card
   - Select date for food count
   - Enter counts for Breakfast, Lunch, Dinner (Students)
   - Enter counts for Breakfast, Lunch, Dinner (Faculty)
   - Click "Save Food Count"

3. **View Student Feedback**
   - Click "📊 View Student Feedback" card
   - Select date range
   - Filter by meal type (optional)
   - View statistics and detailed feedback
   - Identify quality issues

4. **Impose Fines**
   - Click "⚖️ Add Fines" card
   - Select vendor/mess name
   - Choose fine reason
   - Enter fine amount
   - Select meal type
   - Add remarks
   - Click "Impose Fine"

5. **Monitor Dashboard**
   - View recent food counts
   - Check recent fines
   - Monitor quality trends

---

### 🏪 For Vendors
1. **Login**
   - Open `login.html`
   - Select "Vendor" card
   - Username: `vendor`, Password: `vendor123`
   - Select your Mess (A, B, or C)

2. **View Student Feedback**
   - Click "📝 View Student Feedback" card
   - Filter by date range
   - See all feedback about your mess
   - Identify items with low ratings
   - Review student comments

3. **Give Justifications**
   - Click "💬 Give Justifications" card
   - View recent feedback
   - Provide explanations for issues
   - Explain quality issues or delays
   - Suggest improvements

4. **View Fines**
   - Click "⚖️ View Fines" card
   - See all fines imposed by warden
   - View fine amounts and reasons
   - Check fine dates
   - Respond with justifications
   - Track fine payment

5. **View Billing**
   - Click "💰 View Billing" card
   - Check billing records
   - Download billing statements
   - Track earnings

---

### 👨‍💻 For Admin
1. **Login**
   - Open `login.html`
   - Select "Admin" card
   - Username: `admin`, Password: `admin123`

2. **View Dashboard**
   - See overview of all activities
   - Key metrics and statistics
   - System usage statistics

3. **Filter Data**
   - Select period: Today / This Week / This Month / All Time
   - View updated charts and statistics
   - Real-time data updates

4. **Analyze Feedback**
   - View all student feedback
   - Analyze by meal type
   - Track top-rated items
   - Identify recurring issues
   - Monitor vendor performance

5. **Generate Reports**
   - Click "📥 Export Report" button
   - Choose report type:
     - **Daily Report** - Single day details
     - **Weekly Report** - 7 separate Excel sheets
     - **Monthly Report** - 30 separate Excel sheets
   - Download as .xlsx file
   - Import into PowerPoint or Excel for presentations

6. **Monitor Operations**
   - View all food counts
   - Track all fines imposed
   - Monitor vendor performance
   - Review billing records

---

## 📁 File Structure

```
cmc-mess-feedback-portal/
│
├── index.html                    # Student Feedback Form
├── login.html                    # Role-based Login Page (entry point)
├── warden.html                   # Warden Dashboard
├── vendor.html                   # Vendor Dashboard
├── admin.html                    # Admin Dashboard
│
├── assets/
│   └── logo.png                  # CMC College Logo
│
├── scripts/
│   ├── create_feedback_db.py     # Database initialization script
│   └── database/
│       └── mess_management.db    # SQLite Database
│
├── server.py                     # Python Flask Backend
├── requirements.txt              # Python dependencies
│
├── Documentation Files (for reference):
│   ├── README.md                 # This file
│   ├── HOW_TO_USE.md             # Detailed usage instructions
│   ├── SYSTEM_GUIDE.md           # System architecture guide
│   ├── IMPLEMENTATION_SUMMARY.md # Feature implementation details
│   └── Other docs...
│
└── .git/                         # Version control (if using Git)
```

### Key Files Description
| File | Purpose |
|------|---------|
| `index.html` | Student feedback form for submitting meal ratings |
| `login.html` | Authentication entry point for all roles |
| `warden.html` | Warden operations: food counts, feedback, fines |
| `vendor.html` | Vendor portal: feedback, justifications, fines, billing |
| `admin.html` | Admin analytics: reports, charts, data management |
| `server.py` | Python backend for database operations |
| `mess_management.db` | SQLite database storing all data |

---

## 💻 Technical Stack

### Frontend Technologies
- **HTML5** - Semantic markup
- **CSS3** - Responsive design, Gradients, Flexbox, Grid
- **JavaScript (ES6+)** - DOM manipulation, Event handling, Data validation
- **Chart.js** - Interactive data visualization
- **LocalStorage API** - Client-side data persistence

### Backend Technologies
- **Python 3.7+** - Server runtime
- **Flask 2.0+** - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **SQLite 3** - Lightweight database

### Dependencies
```
Flask>=2.0
Flask-CORS>=3.0.10
```

### Browser Compatibility
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

---

## 🗄️ Database Structure

### SQLite Database: mess_management.db

#### Tables

**1. students**
- `id` - Primary key
- `name` - Student full name
- `roll_no` - Student roll number
- `created_at` - Registration timestamp

**2. student_feedback**
- `id` - Primary key
- `student_id` - Foreign key to students
- `feedback_date` - Date of feedback
- `breakfast_rating` - Breakfast overall rating
- `lunch_rating` - Lunch overall rating
- `dinner_rating` - Dinner overall rating
- `comments` - Detailed comments

**3. food_items**
- `id` - Primary key
- `name` - Item name
- `meal_type` - Breakfast/Lunch/Dinner
- `active` - Item availability status

**4. item_ratings**
- `id` - Primary key
- `feedback_id` - Foreign key to student_feedback
- `item_id` - Foreign key to food_items
- `taste_rating` - Taste score (1-5)
- `quality_rating` - Quality score (1-5)
- `quantity_rating` - Quantity score (1-5)
- `cleanliness_rating` - Cleanliness score (1-5)

**5. vendor_fines**
- `id` - Primary key
- `vendor_id` - Vendor identification
- `fine_amount` - Fine amount
- `reason` - Fine reason
- `meal_type` - Associated meal
- `imposed_date` - When fine was imposed
- `imposed_by` - Warden who imposed fine
- `remarks` - Detailed remarks

**6. vendor_justifications**
- `id` - Primary key
- `feedback_id` - Related feedback
- `vendor_id` - Vendor response
- `justification_text` - Vendor explanation
- `created_at` - Response timestamp

**7. food_counts**
- `id` - Primary key
- `count_date` - Date of count
- `breakfast_students` - Breakfast student count
- `lunch_students` - Lunch student count
- `dinner_students` - Dinner student count
- `breakfast_faculty` - Breakfast faculty count
- `lunch_faculty` - Lunch faculty count
- `dinner_faculty` - Dinner faculty count

---

## 🏆 Key Achievements

### ✅ Completed Features
- [x] Role-based authentication system (Student, Warden, Vendor, Admin)
- [x] Interactive student feedback form with star ratings
- [x] Comprehensive warden dashboard with food count management
- [x] Fine imposition system with vendor tracking
- [x] Vendor justification and response system
- [x] Real-time analytics with Chart.js visualizations
- [x] Excel export with formatted reports (Daily, Weekly, Monthly)
- [x] Data validation and error handling
- [x] Responsive mobile-friendly design
- [x] LocalStorage data persistence
- [x] SQLite database integration
- [x] Flask backend API for data operations
- [x] CORS support for cross-origin requests

### 📊 Analytics Features
- Average ratings by criteria
- Meal type distribution
- Top-rated items tracking
- Daily submission trends
- Vendor performance metrics
- Quality improvement tracking

### 🔒 Security Features
- Password-protected authentication
- Role-based access control
- Session management
- Input validation and sanitization
- Database query parameterization

---

## 🎓 Learning Outcomes & Skills Demonstrated

### Web Development
- Modern HTML5 semantic structure
- Advanced CSS3 (Gradients, Flexbox, Grid, Animations)
- Vanilla JavaScript ES6+ (No frameworks)
- Form validation and DOM manipulation
- Event handling and data binding

### Backend Development
- Python Flask framework
- RESTful API design
- SQLite database operations
- CORS handling for API security

### Data Visualization
- Chart.js implementation
- Real-time data updates
- Interactive dashboards
- Excel export functionality

### UI/UX Design
- Responsive design principles
- Color psychology (gradient themes)
- User-centered interface design
- Accessibility considerations

### Software Engineering
- Version control with Git
- Code documentation
- Project structure organization
- Database schema design
- Testing and debugging

---

## 🐛 Troubleshooting

### Issue: Database not found
**Solution:** 
```bash
cd scripts
python create_feedback_db.py
```

### Issue: CORS errors when accessing API
**Solution:** Ensure `server.py` is running and Flask-CORS is installed:
```bash
pip install Flask-CORS
python server.py
```

### Issue: Data not persisting
**Solution:** 
- Check browser's localStorage is enabled
- Clear browser cache and retry
- For database, ensure `mess_management.db` exists in `scripts/database/`

### Issue: Charts not displaying
**Solution:**
- Ensure Chart.js is loaded (check browser console)
- Verify data exists before rendering charts
- Try refreshing the page

---

## 📞 Support & Contact

For issues or questions:
- Check existing documentation files
- Review browser console for error messages
- Ensure all files are in correct locations
- Verify database exists at `scripts/database/mess_management.db`

---

## 📝 License

This project is developed for Coimbatore Marine College (CMC). All rights reserved.

---

## 🙏 Acknowledgments

- Coimbatore Marine College for the opportunity
- Student feedback system concept
- Modern web technologies and frameworks used

---

**Last Updated:** February 3, 2026  
**Version:** 2.0  
**Status:** ✅ Production Ready
Each submission contains:
```json
{
  "student_name": "Anie",
  "student_roll": "55rf",
  "datetime": "2026-01-28T10:30:00.000Z",
  "date_readable": "1/28/2026",
  "time_readable": "4:00:00 PM",
  "meal_type": "Lunch",
  "day": "Wednesday",
  "items": [
    {
      "item_name": "Chappathi",
      "taste": 4,
      "quality": 5,
      "quantity": 4,
      "cleanliness": 4,
      "comment": "Good"
    }
  ]
}
```

### Export Format
**Daily/Weekly/Monthly Reports** (Excel format with consolidation):
| Date | Meal Type | Student Name | Roll Number | Items Reviewed | Avg Taste | Avg Quality | Avg Quantity | Avg Cleanliness | Overall Rating |
|------|-----------|--------------|-------------|----------------|-----------|-------------|--------------|-----------------|----------------|
| 1/28/2026 | Breakfast | Anie | 55rf | Idly, Vada | 4.50 | 4.50 | 4.00 | 4.50 | 4.38 |

## 🔒 Security Features

- **Password Protection**: Admin dashboard requires login
- **Session Management**: Login persists during session
- **Local Storage**: Data never sent to external servers
- **Secure Password Field**: Masked password input with show/hide toggle
- **No Credentials Display**: Login hints are hidden

## 📱 Responsive Design

- **Desktop**: Full-width layout with all features visible
- **Tablet**: Optimized grid layout
- **Mobile**: Single-column, touch-friendly interface
- **Cross-browser**: Works on Chrome, Firefox, Safari, Edge

## 🎨 UI/UX Features

- **Modern Gradient Design**: Professional blue and yellow theme
- **Smooth Animations**: Sliding, bouncing, and hover effects
- **Color-coded Badges**: High/Medium/Low ratings with visual indicators
- **Interactive Charts**: Real-time visualization using Chart.js
- **Intuitive Navigation**: Clear buttons and menu options
- **Visual Feedback**: Hover effects and state changes

## 🔧 Technical Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js 3.9.1
- **Excel Export**: XLSX 0.18.5 library
- **Data Storage**: Browser localStorage
- **No Framework**: Pure vanilla JavaScript (no jQuery, React, etc.)

## 📈 Menu Data

The system includes predefined menus for all 7 days:
- **Breakfast**: 6:00 AM - 10:00 AM
- **Lunch**: 10:00 AM - 3:00 PM
- **Dinner**: 3:00 PM onwards

Each day has different menu items for variety.

## 💾 Data Storage & Retention

- **Storage Method**: Browser's localStorage
- **Key**: `cmc_feedback`
- **Capacity**: ~5-10 MB per browser (sufficient for 1000+ responses)
- **Retention**: 30 days (older data automatically deleted)
- **Backup**: Export data regularly to Excel for permanent storage

## 🎯 Report Types

### Daily Report
- Single Excel file
- All submissions for the day
- Organized by meal type (Breakfast/Lunch/Dinner)
- One row per student per meal

### Weekly Report
- 7 separate Excel sheets
- One sheet per day of the week
- Each sheet contains all submissions for that day
- Organized chronologically

### Monthly Report
- 30+ separate Excel sheets
- One sheet per day of the month
- Complete monthly breakdown
- Perfect for detailed analysis

## 🔄 Workflow

```
Student → Fill Form → Enter Details → Rate Items → Add Comments → Submit
                                                           ↓
                                                    Data Stored Locally
                                                           ↓
Admin → Login → View Dashboard → Filter Data → Export Report → Analyze
                    ↓
            See Charts & Statistics
```

## ⚙️ Customization

### Change Admin Credentials
Edit in `login.html` line ~140:
```javascript
if(u === 'YOUR_USERNAME' && p === 'YOUR_PASSWORD') {
```

### Update Menu Items
Edit in `index.html` within `menuData` object (lines ~90-130):
```javascript
"Monday": {
    Breakfast: ["Item1", "Item2", ...],
    Lunch: ["Item1", "Item2", ...],
    Dinner: ["Item1", "Item2", ...]
}
```

### Change Colors
Update CSS variables in any HTML file:
```css
:root {
    --primary: #003366;      /* Navy blue */
    --secondary: #f4f4f4;    /* Light gray */
    --accent: #ffcc00;       /* Yellow */
}
```

## 📞 Support & Troubleshooting

### Data Not Saving?
- Check browser storage limits
- Clear cache and try again
- Ensure localStorage is enabled

### Charts Not Displaying?
- Check internet connection (Chart.js requires CDN)
- Refresh the page
- Try different browser

### Login Issues?
- Verify username and password (admin/cmc123)
- Clear browser session storage
- Check browser console for errors

### Export Not Working?
- Ensure JavaScript is enabled
- Check browser popup blockers
- Try different file format

## 📝 Browser Compatibility

| Browser | Version | Support |
|---------|---------|---------|
| Chrome | Latest | ✅ Full |
| Firefox | Latest | ✅ Full |
| Safari | Latest | ✅ Full |
| Edge | Latest | ✅ Full |
| IE | 11 | ⚠️ Limited |

## 🔐 Data Privacy

- All data is stored **locally in the browser**
- No data is sent to any server
- No external API calls (except CDN for libraries)
- Each browser has its own isolated data
- Data persists only on the same device/browser

## 📊 Analytics Metrics

The dashboard tracks:
- **Total Submissions**: Count of all feedback entries
- **Overall Average Rating**: Average of all criteria across all items
- **Students Participated**: Count of unique students
- **Items Reviewed**: Count of unique food items reviewed
- **Daily Trends**: Submissions over time
- **Item Performance**: Top and bottom-rated items
- **Meal Comparison**: Performance across Breakfast/Lunch/Dinner

## 🚀 Future Enhancements

Possible improvements:
- Backend integration with database
- User authentication system
- Email notifications
- More advanced analytics
- Mobile app version
- QR code for quick feedback
- Real-time notifications
- Student ratings history

## 📄 License

This project is created for Coimbatore Marine College.

## 👨‍💻 Development Info

- **Created**: January 2026
- **Last Updated**: January 28, 2026
- **Version**: 1.0.0
- **Status**: Production Ready

## 🙏 Acknowledgments

Built with ❤️ for CMC to improve mess food quality and student satisfaction.

---

**Need Help?** Check the files or contact the development team.

Happy Feedback! 📝✨