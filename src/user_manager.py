# server/user_manager.py
import os
from .config import BASE_STORAGE

def setup_user_environment(username):
    """
    Creates a home directory for the user if it doesn't exist.
    Returns the absolute path to the user's home directory.
    """
    user_home = os.path.abspath(os.path.join(BASE_STORAGE, username))
    if not os.path.exists(user_home):
        os.makedirs(user_home)
    return user_home
