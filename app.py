from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail
from database import init_db
from models import User
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

# Initialize Flask-Mail
mail = Mail(app)

# Create upload folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

# Import routes
from routes.auth import auth_bp
from routes.expenses import expenses_bp
from routes.dashboard import dashboard_bp
from routes.settings import settings_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(expenses_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(settings_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)