# 💰 Expense Tracker

A full-stack web application for tracking personal expenses with visualizations and user authentication.

## ✨ Features

- User authentication with email verification
- Add, edit, delete expenses
- Category-wise expense tracking
- Interactive charts (Pie & Line charts)
- Search and filter expenses
- PDF export of monthly reports
- Profile management with photo upload
- Dark mode support
- Multi-currency support (₹, $, €, £)
- Responsive design

## 🛠️ Tech Stack

**Backend:** Python, Flask, SQLite, Flask-Login, Flask-Mail  
**Frontend:** HTML5, CSS3, JavaScript, Chart.js  
**Other:** ReportLab (PDF), Font Awesome (Icons)

## 📁 Project Structure

```
expense-tracker/
├── app.py
├── config.py
├── database.py
├── models.py
├── requirements.txt
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── expenses.py
│   ├── dashboard.py
│   └── settings.py
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── js/dashboard.js
└── templates/
    ├── index.html
    ├── login.html
    ├── signup.html
    ├── dashboard.html
    ├── settings.html
    └── profile.html
```

## 🚀 Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Email (in `config.py`)
```python
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'
```

### 3. Initialize Database
```bash
python database.py
```

### 4. Run Application
```bash
python app.py
```

Visit: `http://127.0.0.1:5000/`

## 📖 Quick Start

1. **Sign Up** - Create account and verify email
2. **Login** - Access your dashboard
3. **Add Expenses** - Click "Add Expense" button
4. **View Analytics** - See charts and statistics
5. **Export PDF** - Download monthly reports

## 🔧 Email Setup

**Get Gmail App Password:**
1. Go to Google Account → Security
2. Enable 2-Step Verification
3. Generate App Password
4. Use in `config.py`

**Skip Email Verification (Testing):**
```python
# In routes/auth.py, line 78, add verified=1:
conn.execute('INSERT INTO users (name, email, password, verified) VALUES (?, ?, ?, 1)',
            (name, email, hashed_password))
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| CSS not loading | Clear cache (Ctrl+Shift+R) |
| Email not sending | Use Gmail App Password |
| Database error | Delete `expense_tracker.db` and run `python database.py` |
| Port in use | Change port in `app.py`: `app.run(port=5001)` |

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/signup` | Register user |
| POST | `/login` | Login user |
| GET | `/dashboard` | View dashboard |
| GET | `/api/expenses` | Get expenses |
| POST | `/api/expenses` | Add expense |
| PUT | `/api/expenses/<id>` | Update expense |
| DELETE | `/api/expenses/<id>` | Delete expense |
| GET | `/api/export/pdf` | Export PDF |

## 📄 License

MIT License - Free to use and modify.



---

**Happy Tracking! 💰📊**
