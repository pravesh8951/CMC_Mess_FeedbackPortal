# 🍽️ CMC Mess Management System - Role-Based Portal

## System Overview

A complete web-based mess management system for Coimbatore Marine College with three distinct role-based dashboards: **Warden**, **Vendor**, and **Admin**.

---

## 📁 File Structure

```
cmc-mess-feedback-portal/
├── login.html          ← Role-based login page
├── warden.html         ← Warden Dashboard
├── vendor.html         ← Vendor Dashboard  
├── admin.html          ← Admin Dashboard
├── index.html          ← Student Feedback Form
├── README.md           ← Original documentation
├── assets/
│   └── logo.png
└── .git/               ← Git repository
```

---

## 🔐 Login Credentials

### **Warden Login**
- **URL:** `login.html`
- **Role:** Warden
- **Username:** `warden`
- **Password:** `warden123`

### **Vendor Login**
- **URL:** `login.html`
- **Role:** Vendor
- **Username:** `vendor`
- **Password:** `vendor123`
- **Select Mess:** Choose from Mess A, B, or C

### **Admin Login**
- **URL:** `login.html`
- **Role:** Admin
- **Username:** `admin`
- **Password:** `admin123`

---

## 👨‍💼 Warden Dashboard (`warden.html`)

### Features:

#### 1️⃣ **Add Next-Day Food Count**
- Select date for food count entry
- Enter breakfast, lunch, and dinner counts for:
  - Students
  - Faculty/Teachers
- **Use Case:** Vendor preparation and billing calculation
- **Data Storage:** localStorage (foodCounts)

#### 2️⃣ **View Student Feedback**
- View feedback by date or date range
- Filter by meal type (Breakfast/Lunch/Dinner)
- See:
  - Student name and roll number
  - Overall ratings
  - Item-wise feedback
  - Comments and remarks
- **Statistics:** Total feedbacks, average ratings, quality trends

#### 3️⃣ **Impose Fines**
- Select vendor/mess for fine
- Choose reason:
  - Poor quality food
  - Hygiene issue
  - Late service
  - Wrong item served
  - Expired/spoiled food
  - Other
- Enter fine amount and meal type
- Add detailed remarks
- **Tracking:** All fines stored and visible to vendors and admin

#### 4️⃣ **Monitor Food Quality**
- Review recent food counts
- Track quality issues through feedback
- Take action based on vendor performance

---

## 🏪 Vendor Dashboard (`vendor.html`)

### Features:

#### 1️⃣ **View Student Feedback**
- See all feedback from students
- Filter by date range
- View:
  - Overall ratings
  - Item-wise ratings
  - Taste, Quality, Quantity feedback
  - Student comments
- **Statistics:** Total feedbacks, average rating, low rating analysis

#### 2️⃣ **Give Justifications for Complaints**
- Select date and view low-rating complaints
- Submit explanation for each complaint
- Provide detailed remarks on how issues will be addressed
- **Status Tracking:** See justification history

#### 3️⃣ **View Fines Imposed**
- See all fines imposed by warden
- View:
  - Date of issue
  - Reason for fine
  - Amount charged
  - Meal affected
  - Warden's remarks
- **Respond to Fines:** Submit justification for each fine

#### 4️⃣ **View Billing**
- Select month to view billing details
- **Statistics:**
  - Total students fed
  - Total staff fed
  - Total amount (₹)
- **Daily Breakdown:**
  - Date-wise entry
  - Number of people fed
  - Amount per date
  - Meal-wise split

---

## 📊 Admin Dashboard (`admin.html`)

### Features:

#### 1️⃣ **View Feedback Reports**
- **Period Filtering:** All Time, Today, This Week, This Month
- **Statistics Dashboard:**
  - Total submissions
  - Overall average rating
  - Unique students participated
  - Unique food items reviewed
- **Charts & Analytics:**
  - Average rating by criteria (Taste, Quality, Quantity, Cleanliness)
  - Daily submission trends
  - Top 10 rated items
  - Meal type distribution (Breakfast/Lunch/Dinner)
- **Recent Submissions Table:**
  - Latest feedback with student details
  - Item count and average ratings
- **Item-wise Analysis:**
  - Each food item's rating breakdown
  - Quality trends over time

#### 2️⃣ **View Complete Billing Reports**
- **Summary Report:**
  - Total students fed
  - Total staff fed
  - Total meals served
  - Total amount spent
- **Detailed Report:**
  - Date-wise breakdown
  - Breakfast, lunch, dinner counts
  - Students vs. teachers count
  - Amount spent per date
- **Export Options:** Generate Excel reports

#### 3️⃣ **View All Fines & Justifications**
- **Fines Summary:**
  - Total fines imposed
  - Total fine amount
  - Pending justifications count
- **Detailed Fines Table:**
  - Vendor/mess name
  - Reason for fine
  - Amount and meal type
  - Warden who imposed fine
  - Status (Imposed/Responded)
- **Vendor Justifications:** View all vendor responses

#### 4️⃣ **Export Reports**
- **Daily Report:** Single sheet with all daily data
- **Weekly Report:** 7 separate sheets (one per day)
- **Monthly Report:** 30 separate sheets (one per day)
- Format: Excel (.xlsx) with proper formatting

---

## 💾 Data Storage (LocalStorage Keys)

The system uses browser's localStorage for data persistence:

| Key | Content | Used By |
|-----|---------|---------|
| `currentUser` | Current logged-in user info | All roles |
| `feedbackData` | Student feedback submissions | Warden, Vendor, Admin |
| `foodCounts` | Daily food count entries | Warden, Vendor, Admin |
| `fines` | Fines imposed by warden | Warden, Vendor, Admin |
| `vendorJustifications` | Vendor responses to complaints | Vendor, Admin |

---

## 🎨 Design Features

- **Modern UI:** Clean, professional design with gradient backgrounds
- **Responsive:** Works on desktop, tablet, and mobile
- **Color Scheme:**
  - **Login Page:** Purple/Violet gradient
  - **Warden:** Purple theme
  - **Vendor:** Teal/Green theme
  - **Admin:** Original blue theme
- **Interactive Charts:** Real-time visualization using Chart.js
- **Smooth Transitions:** All actions have smooth animations

---

## 🔄 User Flow

### First Time User:
1. Open `login.html`
2. Select role (Warden/Vendor/Admin)
3. Enter credentials
4. Get redirected to role-specific dashboard
5. User info stored in localStorage

### Returning User:
- Auto-redirect to dashboard if already logged in
- Data persists across sessions

### Logout:
- Clears user session
- Redirects to login page
- Data retained for future sessions

---

## 📱 Integration with Student Feedback

The system integrates with the existing student feedback form (`index.html`):
- Students submit feedback with name, roll number, meal type, ratings
- Data stored in `feedbackData` localStorage
- All roles can view and analyze this data

---

## 🚀 Getting Started

1. **Open Login Page:**
   ```
   file:///path/to/login.html
   ```

2. **Select Role & Login:**
   - Choose role from three cards
   - Enter credentials
   - Click Login

3. **Use Dashboard:**
   - Navigate through features
   - Data persists in browser localStorage
   - Export reports as needed

---

## ✨ Key Highlights

✅ **Three Complete Role-Based Systems**
- Separate dashboards with role-specific features
- User authentication with localStorage
- Automatic session management

✅ **Comprehensive Data Management**
- Food counts tracking
- Feedback collection and analysis
- Fine management system
- Billing reports

✅ **Export & Reporting**
- Excel report generation
- Multiple report formats
- Customizable date ranges

✅ **Professional UI/UX**
- Modern design with animations
- Responsive layout
- Intuitive navigation
- Real-time charts and statistics

✅ **No Backend Required**
- Everything runs in the browser
- Pure HTML/CSS/JavaScript
- Data persists in localStorage
- Perfect for offline use

---

## 📝 Notes

- All data is stored locally in the browser
- Clearing browser cache will delete all data
- For production use, consider implementing a backend database
- Demo credentials provided for testing purposes
- Each role has specific permissions and data access

---

## 🎯 Future Enhancements

- Backend API integration for data persistence
- User management and role creation
- Advanced analytics and reporting
- Email notifications for fines
- Mobile app development
- Multi-language support

---

**Created:** January 2026  
**System:** CMC Mess Feedback Portal  
**Version:** 1.0
