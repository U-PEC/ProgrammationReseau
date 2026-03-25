import socket
import threading
import paramiko
import re
import subprocess

from .config import IP_ADDR, SOCKET_PORT, CONNEXION_TIMEOUT, SSH_KEY_PATH
from .server import MyServer
from .user_manager import setup_user_environment, init_db
from .shell import handle_session

def cleanup_zombie_containers():
    """
    Removes any orphaned Docker containers from previous unclean shutdowns.
    """
    try:
        print("[*] Cleaning up orphaned Docker containers...")
        result = subprocess.run(
            ["docker", "ps", "-a", "-q", "--filter", "name=ssh_session_"],
            capture_output=True, text=True
        )
        containers = [c for c in result.stdout.strip().split('\n') if c]
        if containers:
            subprocess.run(["docker", "rm", "-f"] + containers, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"[+] Removed {len(containers)} orphaned container(s).")
    except FileNotFoundError:
        print("[-] Docker is not installed or not found in PATH.")
    except Exception as e:
        print(f"[-] Error cleaning up containers: {e}")

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

        chan = transport.accept(CONNEXION_TIMEOUT)
        
        if chan:
            server.event.wait(10)
            username = server.username
            if not username:
                print("[-] Could not retrieve username.")
                return

            # Nettoyage du username pour éviter les erreurs de nommage Docker (ex: caractères spéciaux)
            safe_username = re.sub(r'[^a-zA-Z0-9_.-]', '', username)
            if not safe_username:
                safe_username = "default_user"

            print(f"[+] Session established for user: {safe_username}")
            user_home = setup_user_environment(safe_username)
            handle_session(chan, safe_username, user_home)

    except Exception as e:
        print(f"[-] Client error: {e}")
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
    
    print(f"[*] Server ready on port {SOCKET_PORT}")

    while True:
        client, _ = server_socket.accept()
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

if __name__ == "__main__":
    run_server()