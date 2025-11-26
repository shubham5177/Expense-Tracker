# Expense Tracker - Production Configuration

This file contains production-ready configuration for hosting.

## Files Included:

1. **Procfile** - Tells hosting platforms (Heroku, etc.) how to run your app
2. **.gitignore** - Files to exclude from Git
3. **requirements.txt** - Python package dependencies
4. **HOSTING_GUIDE.md** - Detailed hosting instructions

## Quick Start:

### Option 1: Heroku (Easiest)
```bash
heroku create your-app-name
git push heroku main
heroku config:set SECRET_KEY=your-key MAIL_USERNAME=your-email MAIL_PASSWORD=your-pass
```

### Option 2: PythonAnywhere (Recommended)
1. Upload files to PythonAnywhere
2. Set up Flask web app
3. Add environment variables in WSGI config
4. Reload

### Option 3: DigitalOcean
1. Push to GitHub
2. Create App on DigitalOcean
3. Connect GitHub repo
4. Deploy

See **HOSTING_GUIDE.md** for detailed instructions.

## Environment Variables Needed:

```
SECRET_KEY              # Strong random key for Flask
MAIL_USERNAME           # Gmail address
MAIL_PASSWORD           # Gmail app password
MAIL_DEFAULT_SENDER     # Sender email
```

## Database:

Currently uses **SQLite** (local file).

For production with multiple users, upgrade to **PostgreSQL**:
- Heroku: `heroku addons:create heroku-postgresql:hobby-dev`
- DigitalOcean: Managed PostgreSQL service
- AWS: RDS PostgreSQL

See HOSTING_GUIDE.md for migration steps.

## Tested Platforms:

✅ Heroku  
✅ PythonAnywhere  
✅ DigitalOcean  
✅ Render  
✅ AWS Elastic Beanstalk  

## Support:

For help, refer to:
1. Platform-specific documentation
2. Flask deployment guides
3. HOSTING_GUIDE.md in this project
