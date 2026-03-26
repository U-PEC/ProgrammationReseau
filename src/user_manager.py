# server/user_manager.py
import os
import sqlite3
import hashlib
from .config import BASE_STORAGE, DB_PATH, DB_DIR, INIT_SQL_PATH

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
            print(f"[-] Init SQL file not found at {INIT_SQL_PATH}")
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

def user_exists(username):
    """Checks if a user exists in the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def verify_public_key(username, key):
    """Verifies if the provided public key is authorized for the user by checking their authorized_keys file."""
    if not user_exists(username):
        logger.warning(f"Public key authentication failed: User '{username}' does not exist.")
        return False

    user_home = setup_user_environment(username)
    auth_keys_path = os.path.join(user_home, '.ssh', 'authorized_keys')
    
    if not os.path.exists(auth_keys_path):
        return False
        
    with open(auth_keys_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split()
            if len(parts) >= 2:
                key_type, key_base64 = parts[0], parts[1]
                if key.get_name() == key_type and key.get_base64() == key_base64:
                    logger.info(f"Public key authentication successful for user '{username}'.")
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
