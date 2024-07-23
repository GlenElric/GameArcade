import sqlite3
import os

def get_db_connection():
    # Ensure the directory exists
    db_dir = 'database'
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        
    # Connect to the database
    conn = sqlite3.connect(os.path.join(db_dir, 'arcade.db'))
    return conn

def setup_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            game TEXT NOT NULL,
            score INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()
