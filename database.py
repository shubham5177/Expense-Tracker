import sqlite3 
from datetime import datetime 

def get_db_connection ():
    """Create and return a database connection"""
    conn =sqlite3 .connect ('expense_tracker.db')
    conn .row_factory =sqlite3 .Row 
    return conn 

def init_db ():
    """Initialize the database with required tables"""
    conn =get_db_connection ()
    cursor =conn .cursor ()


    cursor .execute ('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            verified INTEGER DEFAULT 0,
            currency TEXT DEFAULT '₹',
            photo TEXT DEFAULT 'default.png',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')


    cursor .execute ('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    conn .commit ()
    conn .close ()
    print ("✓ Database initialized successfully!")
    return True 

if __name__ =='__main__':
    init_db ()