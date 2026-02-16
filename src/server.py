import paramiko
import threading
from .config import USERS

# https://docs.paramiko.org/en/stable/api/server.html
class MyServer(paramiko.ServerInterface):
    """
    Implements the Paramiko ServerInterface to handle SSH authentication and channel requests.
    """
    def __init__(self):
        self.event = threading.Event()
        self.username = None  # Will hold the username of the connected user

    def check_auth_password(self, username, password):
        """
        Authenticate a user based on a password.
        """
        if username in USERS and USERS[username] == password:
            self.username = username
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        """
        Called when a client requests a new channel.
        We only accept 'session' channels.
        """
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        """
        Called when a client requests a pseudo-terminal.
        This is required for an interactive shell.
        """
        return True

    def check_channel_shell_request(self, channel):
        """
        Called when a client requests a shell.
        """
        self.event.set()
        return True

    # The following channel requests are not implemented in this server
    def check_channel_subsystem_request(self, channel, name):
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_window_change_request(self, channel, width, height, pixelwidth, pixelheight):
        return True

    def check_channel_x11_request(self, channel, single_connection, auth_protocol, auth_cookie, screen_number):
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_forward_agent_request(self, channel):
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED