# server/config.py
import os

# Dynamically get the absolute path to the 'server' root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Network settings
IP_ADDR = '0.0.0.0'
SOCKET_PORT = 6767
CONNEXION_TIMEOUT = 60

# Paths
SSH_KEY_PATH = os.path.join(BASE_DIR, '.ssh', 'server.key')
BASE_STORAGE = os.path.join(BASE_DIR, 'users_storage')

DB_DIR = os.path.join(BASE_DIR, 'db')
DB_PATH = os.path.join(DB_DIR, 'users.db')
INIT_SQL_PATH = os.path.join(DB_DIR, 'data.sql')
