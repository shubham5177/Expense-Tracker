# 💰 Expense Tracker

A full-stack web application for tracking personal expenses with beautiful visualizations, user authentication, and comprehensive expense management features.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📸 Screenshots

### Home Page
Beautiful landing page with animated hero section and feature showcase.

### Dashboard
Real-time expense tracking with interactive charts and statistics.

### Analytics
Category-wise breakdown and monthly spending trends visualization.

---

## ✨ Features

### 🔐 Authentication & Security
- User registration with email verification
- Secure password hashing (Werkzeug)
- Session-based authentication (Flask-Login)
- Token-based email verification (30-minute expiry)
- Account deletion with password confirmation

### 💵 Expense Management
- **Add, Edit, Delete** expenses with ease
- **Categorize** expenses (Food, Transport, Shopping, Entertainment, Bills, Health, Other)
- **Search & Filter** expenses by title, notes, or category
- **Date tracking** for all transactions
- **Notes field** for additional details

### 📊 Data Visualization
- **Category-wise Pie Chart** - Visual breakdown of spending by category
- **Monthly Trend Line Chart** - Last 6 months spending analysis
- **Real-time Statistics**:
  - Total spending (all-time)
  - Monthly spending (current month)
  - Today's spending
  - Average expense per transaction
  - Most active day of the week
  - Top spending category

### 🎨 User Interface
- **Modern, Clean Design** with smooth animations
- **Fully Responsive** - Works on desktop, tablet, and mobile
- **Dark Mode Toggle** with localStorage persistence
- **Animated Modal Popups** for adding/editing expenses
- **FAQ Accordion** on landing page
- **Interactive Charts** powered by Chart.js

### 📄 Reports & Export
- **PDF Export** - Monthly expense reports with ReportLab
- Detailed report includes user info and expense table
- Professional formatting with totals and summaries

### ⚙️ Settings & Customization
- **Update Profile** - Change name and information
- **Profile Photo Upload** - PNG, JPG, JPEG, GIF (max 5MB)
- **Change Password** - Secure password update
- **Currency Selection** - ₹ (INR), $ (USD), € (EUR), £ (GBP)
- **Theme Selection** - Light/Dark mode preferences

### 👤 Profile Page
- View account statistics and spending habits
- Account verification status
- User ID and registration date
- Total expenses count and amount
- Average spending metrics

---

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **Flask 2.3.0** - Web framework
- **SQLite** - Database
- **Flask-Login** - User session management
- **Flask-Mail** - Email verification
- **Werkzeug** - Password hashing
- **itsdangerous** - Token generation
- **ReportLab** - PDF generation

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with CSS Variables
- **JavaScript (Vanilla)** - Interactivity
- **Chart.js** - Data visualization
- **Font Awesome 6.0** - Icons

---

## 📁 Project Structure

```
expense-tracker/
│
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── database.py                 # Database initialization
├── models.py                   # User and Expense models
├── requirements.txt            # Python dependencies
│
├── routes/
│   ├── __init__.py            # Routes package initializer
│   ├── auth.py                # Authentication routes
│   ├── expenses.py            # Expense CRUD operations
│   ├── dashboard.py           # Dashboard & statistics
│   └── settings.py            # User settings management
│
├── static/
│   ├── css/
│   │   └── style.css          # Complete styling
│   ├── js/
│   │   ├── script.js          # Main JavaScript
│   │   └── dashboard.js       # Dashboard functionality
│   └── uploads/
│       └── profiles/          # User profile photos
│           └── default.png    # Default avatar
│
├── templates/
│   ├── index.html             # Landing page
│   ├── login.html             # Login page
│   ├── signup.html            # Registration page
│   ├── dashboard.html         # Main dashboard
│   ├── settings.html          # Settings page
│   └── profile.html           # User profile
│
└── expense_tracker.db         # SQLite database (auto-generated)
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Gmail account (for email verification)

### Step 1: Clone or Download
```bash
# Clone the repository
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker

# Or download and extract the ZIP file
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Email Settings

Edit `config.py` and update the email settings:

```python
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-16-char-app-password'
MAIL_DEFAULT_SENDER = 'your-email@gmail.com'
```

**Get Gmail App Password:**
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification**
3. Go to **App Passwords**
4. Generate password for "Mail"
5. Copy the 16-character password
6. Paste in `config.py`

**For Testing (Skip Email Verification):**

Option 1: Use the manual verification script (see Testing section)

Option 2: Modify `routes/auth.py` line 78 to auto-verify:
```python
conn.execute('INSERT INTO users (name, email, password, verified) VALUES (?, ?, ?, 1)',
            (name, email, hashed_password))
```

### Step 5: Create Default Profile Picture
```bash
# Create the directory
mkdir -p static/uploads/profiles

# Add a default.png image (any square image, 200x200 recommended)
# Or the app will handle missing images gracefully
```

### Step 6: Initialize Database
```bash
python database.py
```

You should see: `✓ Database initialized successfully!`

### Step 7: Run the Application
```bash
python app.py
```

The application will start at `http://127.0.0.1:5000/`

---

## 📖 Usage Guide

### First Time Setup

1. **Visit the Homepage**
   - Navigate to `http://127.0.0.1:5000/`
   - Explore features and FAQ

2. **Create an Account**
   - Click "Get Started Free" or "Sign Up"
   - Fill in your name, email, and password
   - Check your email for verification link
   - Click the verification link (expires in 30 minutes)

3. **Login**
   - Go to the login page
   - Enter your email and password
   - You'll be redirected to the dashboard

### Managing Expenses

**Add an Expense:**
1. Click "Add Expense" button
2. Fill in the form:
   - Title (e.g., "Grocery Shopping")
   - Category (Food, Transport, etc.)
   - Amount
   - Date
   - Notes (optional)
3. Click "Save"

**Edit an Expense:**
1. Find the expense in the table
2. Click the edit (pencil) icon
3. Modify the details
4. Click "Save"

**Delete an Expense:**
1. Find the expense in the table
2. Click the delete (trash) icon
3. Confirm deletion

**Search Expenses:**
- Use the search bar to find expenses by title or notes
- Use the category dropdown to filter by category

**Export PDF Report:**
- Click "Export PDF" button
- Download current month's expense report

### Dashboard Features

**Statistics Cards:**
- **Total Spending** - All-time total
- **This Month** - Current month total
- **Today** - Today's total

**Charts:**
- **Category Breakdown** - Pie chart of spending by category
- **Monthly Trend** - Line chart of last 6 months

### Profile Management

**View Profile:**
- Click "Profile" in the sidebar
- See your account statistics
- View spending habits and patterns

**Update Settings:**
- Click "Settings" in the sidebar
- Update your name
- Upload a profile photo
- Change your password
- Select preferred currency
- Toggle between light/dark mode
- Delete your account (if needed)

### Dark Mode
- Click the moon/sun icon in the top right
- Your preference is saved automatically
- Works across all pages

---

## 🧪 Testing

### Manual User Verification (For Testing)

If email verification isn't working, use this script:

Create `verify_user.py`:
```python
from database import get_db_connection

email = input("Enter email to verify: ")
conn = get_db_connection()
conn.execute('UPDATE users SET verified = 1 WHERE email = ?', (email,))
conn.commit()
conn.close()
print(f"✓ User '{email}' verified successfully!")
```

Run it:
```bash
python verify_user.py
```

### Test Email Configuration

Create `test_email.py`:
```python
from flask import Flask
from flask_mail import Mail, Message
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)

with app.app_context():
    msg = Message('Test Email', recipients=['test@example.com'])
    msg.body = 'Test email from Expense Tracker'
    try:
        mail.send(msg)
        print("✓ Email sent successfully!")
    except Exception as e:
        print(f"✗ Error: {e}")
```

---

## 🔧 Troubleshooting

### Issue: CSS/JS Not Loading
**Solution:**
1. Clear browser cache (Ctrl + Shift + R)
2. Check browser console (F12) for errors
3. Verify files exist in `static/css/` and `static/js/`
4. Try accessing directly: `http://127.0.0.1:5000/static/css/style.css`

### Issue: Email Verification Not Working
**Solutions:**
1. Check Gmail credentials in `config.py`
2. Use Gmail App Password (not regular password)
3. Enable 2-Step Verification in Google Account
4. Check spam folder
5. Use manual verification script (see Testing section)

### Issue: Database Errors
**Solution:**
```bash
# Delete existing database
rm expense_tracker.db

# Recreate database
python database.py
```

### Issue: Port Already in Use
**Solution:**
```python
# In app.py, change the port:
app.run(debug=True, port=5001)
```

### Issue: Import Errors
**Solution:**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Issue: Profile Picture Not Showing
**Solution:**
- Create `static/uploads/profiles/` folder
- Add `default.png` file (any square image)
- Or use any image - app handles missing defaults

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    verified INTEGER DEFAULT 0,
    currency TEXT DEFAULT '₹',
    photo TEXT DEFAULT 'default.png',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Expenses Table
```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
```

---

## 🔒 Security Features

- **Password Hashing** - Werkzeug secure password hashing
- **SQL Injection Prevention** - Parameterized queries
- **XSS Protection** - Input sanitization
- **CSRF Protection** - Flask session security
- **Secure Sessions** - HTTP-only cookies
- **Token Expiry** - Email verification tokens expire in 30 minutes
- **Password Validation** - Minimum 6 characters required

---

## 🎨 Customization

### Change Primary Color
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #007bff;  /* Change this */
}
```

### Add More Categories
Edit the category select options in:
- `templates/dashboard.html`
- Update both the form and filter dropdown

Example:
```html
<option value="Education">Education</option>
<option value="Travel">Travel</option>
<option value="Investment">Investment</option>
```

### Modify Email Template
Edit `routes/auth.py` → `send_verification_email()` function

### Change Currency Options
Edit `templates/settings.html`:
```html
<option value="¥">¥ Japanese Yen (JPY)</option>
<option value="₩">₩ Korean Won (KRW)</option>
```

---

## 🌐 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/signup` | User registration |
| GET/POST | `/login` | User login |
| GET | `/verify/<token>` | Email verification |
| GET | `/logout` | User logout |

### Expenses
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/expenses` | Get all expenses |
| POST | `/api/expenses` | Add new expense |
| PUT | `/api/expenses/<id>` | Update expense |
| DELETE | `/api/expenses/<id>` | Delete expense |

### Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard` | Dashboard page |
| GET | `/profile` | Profile page |
| GET | `/api/dashboard/stats` | Get statistics |
| GET | `/api/export/pdf` | Export PDF report |

### Settings
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/settings` | Settings page |
| POST | `/api/settings/update-profile` | Update name |
| POST | `/api/settings/change-password` | Change password |
| POST | `/api/settings/change-currency` | Update currency |
| POST | `/api/settings/upload-photo` | Upload photo |
| POST | `/api/settings/delete-account` | Delete account |

---

## 🚀 Deployment

### Production Checklist
- [ ] Change `SECRET_KEY` in `config.py` to a random string
- [ ] Set `debug=False` in `app.py`
- [ ] Use environment variables for sensitive data
- [ ] Set up HTTPS/SSL
- [ ] Use a production WSGI server (Gunicorn, uWSGI)
- [ ] Switch to PostgreSQL or MySQL for production
- [ ] Set up automated backups
- [ ] Add rate limiting
- [ ] Configure proper logging
- [ ] Set up monitoring

### Deploy to Heroku
```bash
# Install Heroku CLI and login
heroku login

# Create new Heroku app
heroku create your-expense-tracker

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set MAIL_USERNAME=your-email@gmail.com
heroku config:set MAIL_PASSWORD=your-app-password

# Deploy
git push heroku main

# Run migrations
heroku run python database.py
```

### Deploy to PythonAnywhere
1. Upload files to PythonAnywhere
2. Create a new web app with Flask
3. Configure WSGI file
4. Set up virtual environment
5. Install dependencies
6. Initialize database
7. Configure static files mapping

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guide for Python
- Add comments for complex logic
- Test all features before submitting PR
- Update README if adding new features
- Keep commits atomic and descriptive

---

## 🐛 Known Issues

- Email verification may fail with "Less secure apps" error → Use App Password
- PDF export may have encoding issues with special characters → Use UTF-8
- Chart.js may not render in very old browsers → Use modern browsers

---

## 📝 Future Enhancements

Planned features for future versions:

- [ ] Budget setting and tracking
- [ ] Recurring expenses automation
- [ ] Multi-currency with real-time conversion
- [ ] Expense sharing with family/friends
- [ ] Receipt image upload and OCR
- [ ] Mobile app (React Native)
- [ ] Expense reminders and notifications
- [ ] CSV/Excel import/export
- [ ] Financial insights and AI recommendations
- [ ] Multi-language support
- [ ] Two-factor authentication (2FA)
- [ ] Social login (Google, Facebook)
- [ ] Advanced analytics and reporting
- [ ] API for third-party integrations

---

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 Expense Tracker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com
- Website: [yourwebsite.com](https://yourwebsite.com)

---

## 🙏 Acknowledgments

- **Flask** - Lightweight web framework
- **Chart.js** - Beautiful JavaScript charts
- **Font Awesome** - Icon library
- **ReportLab** - PDF generation
- **SQLite** - Embedded database
- **Bootstrap** concepts for responsive design
- All contributors and users of this project

---

## 📞 Support

Need help? Here are your options:

1. **Documentation** - Read this README thoroughly
2. **Issues** - Open an issue on GitHub
3. **Email** - Contact at support@expensetracker.com
4. **FAQ** - Check the FAQ section on the website

---

## ⭐ Star History

If you find this project helpful, please consider giving it a star on GitHub!

---

## 📈 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/expense-tracker)
![GitHub forks](https://img.shields.io/github/forks/yourusername/expense-tracker)
![GitHub issues](https://img.shields.io/github/issues/yourusername/expense-tracker)
![GitHub license](https://img.shields.io/github/license/yourusername/expense-tracker)

---

<div align="center">
  <h3>Made with ❤️ for better financial management</h3>
  <p>Happy Tracking! 💰📊</p>
</div>
