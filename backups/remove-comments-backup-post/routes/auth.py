"""
Authentication routes for user signup, login, logout, and email verification
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import os
from database import get_db_connection
from models import User

# Create Blueprint
auth_bp = Blueprint('auth', __name__)

def generate_token(email):
    """Generate email verification token"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-verification')

def verify_token(token, expiration=1800):
    """Verify email token (30 minutes expiration)"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-verification', max_age=expiration)
        return email
    except (SignatureExpired, BadSignature):
        return None

def send_verification_email(email, token):
    """Send verification email to user"""
    from app import mail
    verification_link = url_for('auth.verify_email', token=token, _external=True)

    # If mail settings are placeholders (development), write link to a local log file
    mail_user = current_app.config.get('MAIL_USERNAME', '')
    mail_pass = current_app.config.get('MAIL_PASSWORD', '')
    if mail_user.startswith('your-email') or mail_pass.startswith('your-app-password'):
        # Development mode / no real SMTP configured — save link so developer can open it
        log_msg = f"DEV EMAIL - Verification link for {email}: {verification_link}"
        current_app.logger.info(log_msg)
        try:
            log_path = os.path.join(current_app.root_path, 'sent_emails.log')
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(log_msg + '\n')
        except Exception as e:
            current_app.logger.error('Failed to write dev email to log: %s', e, exc_info=True)
        return True

    try:
        msg = Message('Verify Your Email - Expense Tracker', recipients=[email])
        msg.body = f"Welcome to Expense Tracker!\n\nPlease verify your email by clicking the link below:\n{verification_link}\n\nThis link will expire in 30 minutes.\n\nIf you didn't create an account, please ignore this email."
        msg.html = f"""
        <h2>Welcome to Expense Tracker!</h2>
        <p>Please verify your email by clicking the button below:</p>
        <a href=\"{verification_link}\" style=\"display:inline-block;padding:10px 20px;background-color:#007bff;color:white;text-decoration:none;border-radius:5px;\">Verify Email</a>
        <p>This link will expire in 30 minutes.</p>
        <p>If you didn't create an account, please ignore this email.</p>
        """
        mail.send(msg)
        return True
    except Exception as e:
        # Log the detailed error to help debugging (don't expose internals to users)
        current_app.logger.error('Failed to send verification email: %s', e, exc_info=True)
        return False

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validation
        if not name or not email or not password:
            flash('All fields are required!', 'error')
            return redirect(url_for('auth.signup'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return redirect(url_for('auth.signup'))
        
        # Check if user exists
        conn = get_db_connection()
        existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        
        if existing_user:
            conn.close()
            flash('Email already registered!', 'error')
            return redirect(url_for('auth.signup'))
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Insert user with verified=1 (no email verification required)
        conn.execute('INSERT INTO users (name, email, password, verified) VALUES (?, ?, ?, ?)',
                    (name, email, hashed_password, 1))
        conn.commit()
        conn.close()
        
        # Show success message
        flash('Registration completed successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required!', 'error')
            return redirect(url_for('auth.login'))
        
        user = User.get_by_email(email)
        
        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password!', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard.dashboard'))
    
    return render_template('login.html')

@auth_bp.route('/verify/<token>')
def verify_email(token):
    """Verify user email with token"""
    email = verify_token(token)
    
    if not email:
        flash('Verification link is invalid or has expired!', 'error')
        return redirect(url_for('auth.login'))
    
    conn = get_db_connection()
    conn.execute('UPDATE users SET verified = 1 WHERE email = ?', (email,))
    conn.commit()
    conn.close()
    
    flash('Email verified successfully! You can now log in.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))