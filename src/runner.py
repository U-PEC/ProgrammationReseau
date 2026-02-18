import socket
import threading
import paramiko

from .config import IP_ADDR, SOCKET_PORT, CONNEXION_TIMEOUT, SSH_KEY_PATH
from .server import MyServer
from .user_manager import setup_user_environment
from .shell import handle_session

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

            print(f"[+] Session established for user: {username}")
            user_home = setup_user_environment(username)
            handle_session(chan, user_home)

    except Exception as e:
        print(f"[-] Client error: {e}")
    finally:
        if transport:
            transport.close()

def run_server():
    """
    Starts the SSH server.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP_ADDR, SOCKET_PORT))
    server_socket.listen(10)
    
    print(f"[*] Server ready on port {SOCKET_PORT}")

    while True:
        client, _ = server_socket.accept()
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()