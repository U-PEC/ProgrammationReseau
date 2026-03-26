import socket
import threading
import paramiko
import re
import subprocess

from .config import IP_ADDR, SOCKET_PORT, CONNECTION_TIMEOUT, SSH_KEY_PATH
from .server import MyServer
from .user_manager import setup_user_environment, init_db
from .shell import handle_session
from .logger import logger

def cleanup_zombie_containers():
    """
    Removes any orphaned Docker containers from previous unclean shutdowns.
    """
    try:
        logger.info("Cleaning up orphaned Docker containers...")
        result = subprocess.run(
            ["docker", "ps", "-a", "-q", "--filter", "name=ssh_session_"],
            capture_output=True, text=True
        )
        containers = [c for c in result.stdout.strip().split('\n') if c]
        if containers:
            subprocess.run(["docker", "rm", "-f"] + containers, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logger.info(f"Removed {len(containers)} orphaned container(s).")
    except FileNotFoundError:
        logger.error("Docker is not installed or not found in PATH.")
    except Exception as e:
        logger.error(f"Error cleaning up containers: {e}")

def handle_client(client_socket):
    """
    Handles a single client connection.
    """
    transport = None
    try:
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(paramiko.RSAKey.from_private_key_file(SSH_KEY_PATH))
        
        server = MyServer()
        transport.start_server(server=server)

        channel = transport.accept(CONNECTION_TIMEOUT)
        
        if channel:
            server.event.wait(10)
            username = server.username
            if not username:
                logger.warning("Could not retrieve username. Connection aborted.")
                return

            # Nettoyage du username pour éviter les erreurs de nommage Docker (ex: caractères spéciaux)
            safe_username = re.sub(r'[^a-zA-Z0-9_.-]', '', username)
            if not safe_username:
                safe_username = "default_user"

            logger.info(f"Session established for user: {safe_username}")
            user_home = setup_user_environment(safe_username)
            handle_session(channel, safe_username, user_home)

    except Exception as e:
        logger.error(f"Client error: {e}")
    finally:
        if transport:
            transport.close()

def run_server():
    """
    Starts the SSH server.
    """
    # Clean up zombie containers left over from sudden crashes
    cleanup_zombie_containers()

    # Initialize the database before starting the server
    init_db()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP_ADDR, SOCKET_PORT))
    server_socket.listen(10)
    
    logger.info(f"Server ready and listening on {IP_ADDR}:{SOCKET_PORT}")

    try:
        while True:
            client, address = server_socket.accept()
            logger.info(f"Incoming connection from {address[0]}:{address[1]}")
            threading.Thread(target=handle_client, args=(client,), daemon=True).start()
    except KeyboardInterrupt:
        logger.info("Server shutting down gracefully (Ctrl+C).")
    finally:
        server_socket.close()

if __name__ == "__main__":
    run_server()