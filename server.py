import paramiko
import threading

# Simulation d'une base de données utilisateurs
USERS = {
    "admin": "password123",
    "alice": "linux-forever",
    "bob": "12345"
}

# https://docs.paramiko.org/en/stable/api/server.html
class MyServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
        self.username = None # Contiendra le nom de l'utilisateur connecté

    def check_auth_password(self, username, password):
        # Vérification dynamique dans le dictionnaire
        if username in USERS and USERS[username] == password:
            self.username = username # On mémorise qui s'est connecté
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True
        
    def check_channel_subsystem_request():
        return False

    def check_channel_window_change_request():
        return False

    def check_channel_x11_request():
        return False

    def check_channel_forward_agent_request():
        return False