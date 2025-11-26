"""
Settings routes - profile, password, currency, photo upload, account deletion
"""
from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from database import get_db_connection
import os

# Create Blueprint
settings_bp = Blueprint('settings', __name__)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@settings_bp.route('/settings')
@login_required
def settings():
    """Render settings page"""
    return render_template('settings.html', user=current_user)

@settings_bp.route('/api/settings/update-profile', methods=['POST'])
@login_required
def update_profile():
    """Update user profile name"""
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    conn = get_db_connection()
    conn.execute('UPDATE users SET name = ? WHERE id = ?', (name, current_user.id))
    conn.commit()
    conn.close()
    
    current_user.name = name
    return jsonify({'message': 'Profile updated successfully'})

@settings_bp.route('/api/settings/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not current_password or not new_password:
        return jsonify({'error': 'All fields are required'}), 400
    
    if not check_password_hash(current_user.password, current_password):
        return jsonify({'error': 'Current password is incorrect'}), 400
    
    if len(new_password) < 6:
        return jsonify({'error': 'New password must be at least 6 characters'}), 400
    
    hashed_password = generate_password_hash(new_password)
    
    conn = get_db_connection()
    conn.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, current_user.id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Password changed successfully'})

@settings_bp.route('/api/settings/change-currency', methods=['POST'])
@login_required
def change_currency():
    """Change user currency preference"""
    data = request.get_json()
    currency = data.get('currency')
    
    if not currency or currency not in ['₹', '$', '€', '£']:
        return jsonify({'error': 'Invalid currency'}), 400
    
    conn = get_db_connection()
    conn.execute('UPDATE users SET currency = ? WHERE id = ?', (currency, current_user.id))
    conn.commit()
    conn.close()
    
    current_user.currency = currency
    return jsonify({'message': 'Currency updated successfully'})

@settings_bp.route('/api/settings/upload-photo', methods=['POST'])
@login_required
def upload_photo():
    """Upload profile photo"""
    if 'photo' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['photo']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only PNG, JPG, JPEG, GIF allowed'}), 400
    
    # Generate unique filename
    filename = secure_filename(f"user_{current_user.id}_{file.filename}")
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    # Delete old photo if not default
    if current_user.photo != 'default.png':
        old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.photo)
        if os.path.exists(old_path):
            os.remove(old_path)
    
    file.save(filepath)
    
    conn = get_db_connection()
    conn.execute('UPDATE users SET photo = ? WHERE id = ?', (filename, current_user.id))
    conn.commit()
    conn.close()
    
    current_user.photo = filename
    return jsonify({'message': 'Photo uploaded successfully', 'photo': filename})

@settings_bp.route('/api/settings/delete-account', methods=['POST'])
@login_required
def delete_account():
    """Delete user account"""
    data = request.get_json()
    password = data.get('password')
    
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    if not check_password_hash(current_user.password, password):
        return jsonify({'error': 'Incorrect password'}), 400
    
    conn = get_db_connection()
    
    # Delete expenses
    conn.execute('DELETE FROM expenses WHERE user_id = ?', (current_user.id,))
    
    # Delete user
    conn.execute('DELETE FROM users WHERE id = ?', (current_user.id,))
    conn.commit()
    conn.close()
    
    # Delete profile photo
    if current_user.photo != 'default.png':
        photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.photo)
        if os.path.exists(photo_path):
            os.remove(photo_path)
    
    logout_user()
    return jsonify({'message': 'Account deleted successfully'})