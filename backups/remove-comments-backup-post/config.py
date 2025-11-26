import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-12345'
    
    # Flask-Mail Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'expensetracker'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'bro@#123'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME') or 'madaneshubham853@gmail.com'
    
    # Upload Configuration
    UPLOAD_FOLDER = 'static/uploads/profiles'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}