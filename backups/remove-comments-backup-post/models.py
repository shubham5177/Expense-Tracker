"""
User and Expense models for the Expense Tracker application
"""
from flask_login import UserMixin
from database import get_db_connection


class User(UserMixin):
    """User model for authentication and profile management"""
    
    def __init__(self, id, name, email, password, verified, currency, photo, created_at):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.verified = verified
        self.currency = currency
        self.photo = photo
        self.created_at = created_at
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        conn = get_db_connection()
        user_data = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        
        if user_data:
            return User(
                id=user_data['id'],
                name=user_data['name'],
                email=user_data['email'],
                password=user_data['password'],
                verified=user_data['verified'],
                currency=user_data['currency'],
                photo=user_data['photo'],
                created_at=user_data['created_at']
            )
        return None
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        conn = get_db_connection()
        user_data = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user_data:
            return User(
                id=user_data['id'],
                name=user_data['name'],
                email=user_data['email'],
                password=user_data['password'],
                verified=user_data['verified'],
                currency=user_data['currency'],
                photo=user_data['photo'],
                created_at=user_data['created_at']
            )
        return None
    
    def is_verified(self):
        """Check if user email is verified"""
        return self.verified == 1


class Expense:
    """Expense model for tracking user expenses"""
    
    def __init__(self, id, user_id, title, category, amount, date, notes, created_at):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.category = category
        self.amount = amount
        self.date = date
        self.notes = notes
        self.created_at = created_at
    
    @staticmethod
    def get_by_user(user_id):
        """Get all expenses for a user"""
        conn = get_db_connection()
        expenses_data = conn.execute(
            'SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC',
            (user_id,)
        ).fetchall()
        conn.close()
        
        expenses = []
        for exp in expenses_data:
            expenses.append(Expense(
                id=exp['id'],
                user_id=exp['user_id'],
                title=exp['title'],
                category=exp['category'],
                amount=exp['amount'],
                date=exp['date'],
                notes=exp['notes'],
                created_at=exp['created_at']
            ))
        return expenses