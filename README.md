# CMC Mess Feedback Portal 📋

A modern, interactive web-based feedback system for Coimbatore Marine College (CMC) to collect and analyze student feedback on mess food quality across breakfast, lunch, and dinner meals.

## 🌟 Features

### Student Feedback Form
- **Easy Data Entry**: Students enter name and roll number
- **Daily Menu Display**: Dynamic meal menu based on current time and day
- **Star Ratings**: Rate food on 4 criteria:
  - Taste
  - Quality
  - Quantity
  - Cleanliness
- **Item Reviews**: Rate individual menu items or add custom items
- **Comments**: Optional feedback comments for each item
- **Meal Types**: Separate feedback for Breakfast, Lunch, and Dinner
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices

### Admin Dashboard
- **Secure Login**: Password-protected admin access (default: admin/cmc123)
- **Real-time Analytics**: View feedback statistics and trends
- **Interactive Charts**:
  - Average rating by criteria (Taste, Quality, Quantity, Cleanliness)
  - Daily submission trends
  - Top-rated items (Top 10)
  - Meal type distribution (Pie chart)
- **Multiple Report Views**:
  - Daily Report
  - Weekly Report (7 separate sheets)
  - Monthly Report (30 separate sheets)
- **Consolidation**: One row per student per meal per day (no duplicates)
- **Excel Export**: Download reports as .xlsx files with organized data
- **Period Filtering**: View data for Today, This Week, This Month, or All Time
- **Recent Submissions**: Table showing latest feedback with student details
- **Item-wise Analysis**: Detailed ratings for each food item

### Data Management
- **Local Storage**: All data stored in browser's localStorage
- **30-Day Retention**: Automatic cleanup of data older than 1 month
- **No Server Required**: Works completely offline
- **Data Persistence**: Feedback retained even after closing browser

## 🚀 Quick Start

### Installation
1. Download or clone the repository
2. Ensure all files are in the same directory:
   - `index.html` (Student Feedback Form)
   - `login.html` (Admin Login)
   - `admin.html` (Admin Dashboard)
   - `assets/` (Logo and images folder)
3. Open `index.html` in a web browser

### For Students
1. **Open the Feedback Form**: Click on `index.html`
2. **Enter Your Details**:
   - Full Name
   - Roll Number
3. **Rate the Food**:
   - Review appears for the current meal (Breakfast/Lunch/Dinner)
   - Rate each item on 4 criteria using star ratings
   - Optionally add comments
4. **Add Custom Items**: Click "➕ Add Other Item" to review items not in the menu
5. **Submit**: Click "✓ Submit Feedback"
6. **Confirmation**: See thank you message and submit option

### For Admins
1. **Open Admin Login**: Click "🔐 Admin Login" button on feedback page or open `login.html`
2. **Enter Credentials**:
   - Username: `admin`
   - Password: `cmc123`
3. **View Dashboard**: See analytics and reports
4. **Filter Data**:
   - Select period (Today/Week/Month/All)
   - View updated charts and statistics
5. **Export Reports**:
   - Click "📥 Export Report" dropdown
   - Choose Daily, Weekly, or Monthly
   - Download as Excel file (.xlsx)
6. **Analyze Data**:
   - View item-wise ratings
   - Check recent submissions
   - Monitor trends

## 📁 File Structure

```
cmc-mess-feedback/
├── index.html          # Student feedback form
├── login.html          # Admin login page
├── admin.html          # Admin dashboard and analytics
├── assets/
│   └── logo.png        # CMC college logo
└── README.md           # This file
```

## 📊 Data Format

### Stored Data Structure
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