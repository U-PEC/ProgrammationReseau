# server/config.py
import os
import configparser

# Dynamically get the absolute path to the 'server' root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load configuration
config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'server.conf'))

# Network settings
IP_ADDR = config.get('network', 'ip_addr', fallback='0.0.0.0')
SOCKET_PORT = config.getint('network', 'socket_port', fallback=6767)
CONNECTION_TIMEOUT = config.getint('network', 'connection_timeout', fallback=60)

# Paths
SSH_KEY_PATH = os.path.join(BASE_DIR, '.ssh', 'server.key')
BASE_STORAGE = os.path.join(BASE_DIR, 'users_storage')

DB_DIR = os.path.join(BASE_DIR, 'db')
DB_PATH = os.path.join(DB_DIR, 'users.db')
INIT_SQL_PATH = os.path.join(DB_DIR, 'data.sql')
