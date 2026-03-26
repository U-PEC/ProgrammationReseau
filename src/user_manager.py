# server/user_manager.py
import os
import sqlite3
import hashlib
from .config import BASE_STORAGE, DB_PATH, DB_DIR, INIT_SQL_PATH
from .logger import logger

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def init_db():
    """Initializes the SQLite database and creates default users if empty."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password_hash TEXT)''')
    
    # Insert default users if the table is empty (for testing purposes)
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        if os.path.exists(INIT_SQL_PATH):
            with open(INIT_SQL_PATH, 'r') as f:
                c.executescript(f.read())
            conn.commit()
        else:
            logger.warning(f"Init SQL file not found at {INIT_SQL_PATH}. Database created empty.")
    conn.close()

def authenticate_user(username, password):
    """Checks if the provided username and password match the database record."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    
    if row and row[0] == hash_password(password):
        return True
    return False

def setup_user_environment(username):
    """
    Creates a home directory for the user if it doesn't exist.
    Returns the absolute path to the user's home directory.
    """
    user_home = os.path.abspath(os.path.join(BASE_STORAGE, username))
    if not os.path.exists(user_home):
        os.makedirs(user_home)
    return user_home
