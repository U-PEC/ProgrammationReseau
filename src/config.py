# server/config.py

# Network settings
IP_ADDR = '0.0.0.0'
SOCKET_PORT = 6767
CONNEXION_TIMEOUT = 60

# Paths
SSH_KEY_PATH = '.ssh/server.key'
BASE_STORAGE = "users_storage"

# User database
# In a real application, this should be moved to a more secure storage,
# like a database or a properly secured file.
USERS = {
    "admin": "password123",
    "alice": "linux-forever",
    "bob": "12345"
}
