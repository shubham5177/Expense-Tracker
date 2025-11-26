"""
Expense management routes - CRUD operations
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from database import get_db_connection
from datetime import datetime

# Create Blueprint
expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/api/expenses', methods=['GET'])
@login_required
def get_expenses():
    """Get all expenses for current user with optional filters"""
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    conn = get_db_connection()
    query = 'SELECT * FROM expenses WHERE user_id = ?'
    params = [current_user.id]
    
    if search:
        query += ' AND (title LIKE ? OR notes LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    
    if category:
        query += ' AND category = ?'
        params.append(category)
    
    query += ' ORDER BY date DESC'
    
    expenses = conn.execute(query, params).fetchall()
    conn.close()
    
    expenses_list = []
    for exp in expenses:
        expenses_list.append({
            'id': exp['id'],
            'title': exp['title'],
            'category': exp['category'],
            'amount': exp['amount'],
            'date': exp['date'],
            'notes': exp['notes']
        })
    
    return jsonify({'expenses': expenses_list})

@expenses_bp.route('/api/expenses', methods=['POST'])
@login_required
def add_expense():
    """Add a new expense"""
    data = request.get_json()
    
    title = data.get('title')
    category = data.get('category')
    amount = data.get('amount')
    date = data.get('date')
    notes = data.get('notes', '')
    
    if not all([title, category, amount, date]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        amount = float(amount)
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400
    
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO expenses (user_id, title, category, amount, date, notes) VALUES (?, ?, ?, ?, ?, ?)',
        (current_user.id, title, category, amount, date, notes)
    )
    conn.commit()
    expense_id = cursor.lastrowid
    conn.close()
    
    return jsonify({
        'message': 'Expense added successfully',
        'id': expense_id
    }), 201

@expenses_bp.route('/api/expenses/<int:expense_id>', methods=['PUT'])
@login_required
def update_expense(expense_id):
    """Update an existing expense"""
    data = request.get_json()
    
    conn = get_db_connection()
    expense = conn.execute(
        'SELECT * FROM expenses WHERE id = ? AND user_id = ?',
        (expense_id, current_user.id)
    ).fetchone()
    
    if not expense:
        conn.close()
        return jsonify({'error': 'Expense not found'}), 404
    
    title = data.get('title', expense['title'])
    category = data.get('category', expense['category'])
    amount = data.get('amount', expense['amount'])
    date = data.get('date', expense['date'])
    notes = data.get('notes', expense['notes'])
    
    conn.execute(
        'UPDATE expenses SET title = ?, category = ?, amount = ?, date = ?, notes = ? WHERE id = ?',
        (title, category, amount, date, notes, expense_id)
    )
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Expense updated successfully'})

@expenses_bp.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
@login_required
def delete_expense(expense_id):
    """Delete an expense"""
    conn = get_db_connection()
    expense = conn.execute(
        'SELECT * FROM expenses WHERE id = ? AND user_id = ?',
        (expense_id, current_user.id)
    ).fetchone()
    
    if not expense:
        conn.close()
        return jsonify({'error': 'Expense not found'}), 404
    
    conn.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Expense deleted successfully'})