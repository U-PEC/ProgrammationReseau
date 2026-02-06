import paramiko
import threading
import socket

from server import MyServer

IP_ADDR = '0.0.0.0'
SOCKET_PORT = 6767
CONNEXION_TIMEOUT = 60
SSH_KEY_PATH = '.ssh/server.key'

def run_server():
    # 2. Configuration du socket réseau
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP_ADDR, SOCKET_PORT))
    server_socket.listen(5)
    
    print(f"[*] Serveur en attente sur le port {SOCKET_PORT}...")
    client, addr = server_socket.accept()
    print(f"[*] Connexion reçue de {addr}")

    # 3. Mise en place du transport SSH
    transport = paramiko.Transport(client)
    
    # Chargement de la clé d'hôte
    host_key = paramiko.RSAKey.from_private_key_file(SSH_KEY_PATH)
    transport.add_server_key(host_key)

    server = MyServer()
    transport.start_server(server=server)

    # 4. Attente d'un canal
    chan = transport.accept(CONNEXION_TIMEOUT)
    if chan is None:
        print("*** Pas de canal ouvert.")
        return

    chan.send("Bienvenue sur ton serveur SSH Paramiko !\r\n")
    chan.close()

if __name__ == "__main__":
    run_server()