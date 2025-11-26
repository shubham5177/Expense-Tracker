# Expense Tracker - Hosting Guide

This guide covers how to host your Expense Tracker Flask application on various platforms.

---

## Option 1: Heroku (Easiest for Beginners)

### Prerequisites:
- Heroku account (free tier available)
- Git installed
- Heroku CLI installed

### Steps:

1. **Create a Procfile** (tells Heroku how to run your app):
```
web: gunicorn app:app
```

2. **Update requirements.txt** (add gunicorn for production):
```bash
pip install gunicorn
pip freeze > requirements.txt
```

3. **Create a .gitignore file**:
```
.env
__pycache__/
*.pyc
*.db
*.sqlite
sent_emails.log
.DS_Store
venv/
```

4. **Initialize Git repository**:
```bash
git init
git add .
git commit -m "Initial commit"
```

5. **Create Heroku app and deploy**:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

6. **Set environment variables on Heroku**:
```bash
heroku config:set SECRET_KEY=your-production-secret-key
heroku config:set MAIL_USERNAME=your-email@gmail.com
heroku config:set MAIL_PASSWORD=your-app-password
```

7. **Initialize database on Heroku**:
```bash
heroku run python
>>> from database import init_db
>>> init_db()
>>> exit()
```

---

## Option 2: PythonAnywhere (Recommended for Flask)

### Prerequisites:
- PythonAnywhere account (free tier available)

### Steps:

1. **Upload files to PythonAnywhere**:
   - Go to PythonAnywhere Files section
   - Upload your entire project folder

2. **Set up virtual environment**:
   - Go to Web tab → Add a new web app
   - Choose Python 3.9 (or later)
   - Select Flask framework
   - PythonAnywhere will create a virtual environment

3. **Install dependencies**:
   - Open Bash console on PythonAnywhere
   - Navigate to your project
```bash
pip install -r requirements.txt
```

4. **Configure WSGI file**:
   - Edit the WSGI configuration file
   - Replace content with:

```python
import sys
path = '/home/username/expense-tracker'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

5. **Set environment variables**:
   - Go to Web tab → Edit WSGI configuration
   - Add at the top:

```python
import os
os.environ['SECRET_KEY'] = 'your-production-secret-key'
os.environ['MAIL_USERNAME'] = 'your-email@gmail.com'
os.environ['MAIL_PASSWORD'] = 'your-app-password'
```

6. **Reload web app**:
   - Click "Reload" button in Web tab

---

## Option 3: AWS (Scalable & Professional)

### Using Elastic Beanstalk (Easiest AWS option):

1. **Install EB CLI**:
```bash
pip install awsebcli
```

2. **Create Procfile** (if not done):
```
web: gunicorn app:app
```

3. **Initialize Elastic Beanstalk**:
```bash
eb init -p python-3.9 expense-tracker --region us-east-1
```

4. **Create environment and deploy**:
```bash
eb create production
eb deploy
```

5. **Set environment variables**:
```bash
eb setenv SECRET_KEY=your-production-secret-key
eb setenv MAIL_USERNAME=your-email@gmail.com
eb setenv MAIL_PASSWORD=your-app-password
```

---

## Option 4: DigitalOcean (Full Control)

### Using App Platform (Easier):

1. **Push code to GitHub**:
```bash
git remote add origin https://github.com/yourusername/expense-tracker.git
git push -u origin main
```

2. **Create App on DigitalOcean**:
   - Go to DigitalOcean dashboard
   - Click "Create" → "Apps"
   - Connect your GitHub repository
   - Choose branch (main)

3. **Configure app.yaml**:
Create file named `app.yaml` in project root:

```yaml
name: expense-tracker
services:
- name: web
  github:
    repo: yourusername/expense-tracker
    branch: main
  build_command: pip install -r requirements.txt
  run_command: gunicorn app:app
  envs:
  - key: SECRET_KEY
    value: your-production-secret-key
    scope: RUN_TIME
  - key: MAIL_USERNAME
    value: your-email@gmail.com
    scope: RUN_TIME
  - key: MAIL_PASSWORD
    value: your-app-password
    scope: RUN_TIME
  http_port: 8080
```

4. **Deploy**:
   - Click "Create App"
   - DigitalOcean will automatically deploy when you push to GitHub

---

## Option 5: Render (Modern & Easy)

### Steps:

1. **Push code to GitHub**

2. **Create Web Service on Render**:
   - Go to Render dashboard
   - Click "New +"
   - Select "Web Service"
   - Connect GitHub repository

3. **Configure**:
   - Name: `expense-tracker`
   - Runtime: `Python 3`
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`

4. **Add environment variables**:
   - In Settings → Environment
   - Add:
     - `SECRET_KEY`
     - `MAIL_USERNAME`
     - `MAIL_PASSWORD`

5. **Deploy**: Click "Create Web Service"

---

## Database Considerations

### Local SQLite (Current Setup):
- **Pros**: Simple, no setup needed
- **Cons**: Not suitable for multiple users, data loss on server restart

### For Production, upgrade to:

#### PostgreSQL (Recommended):

1. **Install adapter**:
```bash
pip install psycopg2-binary
```

2. **Update database.py**:
```python
import psycopg2
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///expenses.db')

def get_db_connection():
    if 'postgresql' in DATABASE_URL:
        conn = psycopg2.connect(DATABASE_URL)
        conn.row_factory = dict_factory
    else:
        conn = sqlite3.connect('expenses.db')
        conn.row_factory = sqlite3.Row
    return conn
```

3. **Create database on PostgreSQL provider**:
   - Heroku: `heroku addons:create heroku-postgresql:hobby-dev`
   - DigitalOcean: Create managed PostgreSQL cluster
   - AWS RDS: Create RDS instance

---

## Production Checklist

- [ ] Update `SECRET_KEY` to a strong random value
- [ ] Set `MAIL_USERNAME` and `MAIL_PASSWORD` for real email service
- [ ] Change Flask `debug=False`
- [ ] Update database to PostgreSQL
- [ ] Add SSL/HTTPS (most platforms handle this automatically)
- [ ] Set up automated backups
- [ ] Configure logging and error monitoring
- [ ] Test email functionality with real SMTP
- [ ] Set strong database password
- [ ] Enable CORS if API will be accessed from other domains
- [ ] Add rate limiting to prevent abuse

---

## Recommended Setup for Your Use Case

### For a Personal Project:
**Use: PythonAnywhere or Render**
- Free tier available
- Easy setup (no command line complexity)
- Database included
- Automatic HTTPS

### For Small Business:
**Use: DigitalOcean App Platform + PostgreSQL**
- Affordable ($5-12/month)
- Full control
- Scalable
- Good documentation

### For Enterprise:
**Use: AWS Elastic Beanstalk + RDS**
- Highly scalable
- Professional support
- Advanced monitoring
- Pay-as-you-go pricing

---

## Environment Variables Reference

When hosting, set these on your platform:

```
SECRET_KEY=<strong-random-key>
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=<your-email@gmail.com>
MAIL_PASSWORD=<your-app-password>
MAIL_DEFAULT_SENDER=<your-email@gmail.com>
```

---

## Quick Command Reference

### Generate secure SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Test local before deploying:
```bash
pip install -r requirements.txt
python app.py
```

### Create Procfile for Heroku/DigitalOcean:
```bash
echo "web: gunicorn app:app" > Procfile
```

### Initialize Git:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <github-url>
git push -u origin main
```

---

## Support & Troubleshooting

### Common Issues:

1. **"ModuleNotFoundError"**: Install missing packages
   ```bash
   pip install -r requirements.txt
   ```

2. **"Database locked"**: SQLite issue in production
   - Migrate to PostgreSQL

3. **"Email not sending"**: Check credentials
   - Verify app password (not regular password)
   - Enable 2FA on Gmail account

4. **"Static files not loading"**: Run collectstatic
   ```bash
   python -m flask --app app collect
   ```

---

For detailed setup help with your chosen platform, refer to their official documentation.
