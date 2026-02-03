import paramiko
import threading
import socket

# 1. Définition du comportement du serveur
class MyServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    # Vérification du mot de passe
    def check_auth_password(self, username, password):
        if (username == 'admin') and (password == 'password123'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    # Autoriser l'ouverture d'un canal de type "session"
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED