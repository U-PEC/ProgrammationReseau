import paramiko
import threading
import socket
import subprocess
import os
import shutil

from server import MyServer

# Constantes
IP_ADDR = '0.0.0.0'
SOCKET_PORT = 6767
CONNEXION_TIMEOUT = 60
SSH_KEY_PATH = '.ssh/server.key'
BASE_STORAGE = os.path.abspath("users_storage")

def setup_user_environment(username):
    """Crée le dossier de l'utilisateur s'il n'existe pas et s'y déplace."""
    user_home = os.path.join(BASE_STORAGE, username)
    if not os.path.exists(user_home):
        os.makedirs(user_home)
    
    # On déplace le processus Python dans ce dossier
    os.chdir(user_home)
    return user_home

def execute_system_command(command, user_home):
    """Exécute la commande en restant confiné dans user_home."""
    command = command.strip()
    if not command: return ""

    try:
        if command.startswith("cd "):
            target = command.split(" ", 1)[1]
            
            # Calcul du nouveau chemin absolu
            current_dir = os.getcwd()
            new_path = os.path.abspath(os.path.join(current_dir, target))

            # --- SÉCURITÉ : Empêcher de sortir du Home ---
            if not new_path.startswith(user_home):
                return "Erreur : Acces refuse (hors de votre zone).\r\n"
            
            os.chdir(new_path)
            # On affiche le chemin relatif par rapport au home pour faire "propre"
            rel_path = os.path.relpath(new_path, user_home)
            return f"CWD : ~/{rel_path if rel_path != '.' else ''}\r\n"

        # Exécution normale pour les autres commandes
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return output.replace('\n', '\r\n')

    except Exception as e:
        return f"Erreur : {str(e)}\r\n".replace('\n', '\r\n')

def handle_session(chan, username):
    """
    Gère la boucle interactive (Input / Buffer / Echo / Output).
    """
    user_home = setup_user_environment(username)
    
    chan.send(f"\r\n--- Serveur SSH (Utilisateur: {username}) ---\r\n")
    chan.send("ssh-server> ")
    
    command_buffer = ""
    while True:
        try:
            data = chan.recv(1024)
            if not data: break
            
            char = data.decode('utf-8')

            # 1. Gérer l'Entrée (On ne traite que \r, on ignore \n)
            if char == '\r':
                chan.send("\r\n")
                
                # Nettoyage profond : on enlève les espaces et caractères invisibles
                full_command = command_buffer.strip()
                
                if full_command.lower() in ['exit', 'quit']:
                    chan.send("Deconnexion...\r\n")
                    break
                
                if full_command:
                    # Exécution
                    result = execute_system_command(full_command, user_home)
                    if result:
                        chan.send(result)
                    else:
                        # Si la commande a réussi mais ne renvoie rien (ex: touch)
                        chan.send("\r\n")
                
                command_buffer = ""
                chan.send("ssh-server> ")

            elif char == '\n':
                # On ignore le Line Feed car \r a déjà déclenché l'exécution
                continue

            # 2. Retour arrière
            elif char in ['\x7f', '\x08']:
                if len(command_buffer) > 0:
                    command_buffer = command_buffer[:-1]
                    chan.send("\b \b")

            # 3. Filtrage des caractères (On ne garde que le texte "imprimable")
            elif char.isprintable() or char == ' ':
                command_buffer += char
                chan.send(char)

        except (socket.error, EOFError):
            break

def handle_client(client_socket):
    """Gère l'initialisation du Transport SSH."""
    transport = None
    try:
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(paramiko.RSAKey.from_private_key_file(SSH_KEY_PATH))
        
        server = MyServer()
        transport.start_server(server=server)

        # transport.accept() attend qu'une authentification réussisse ET qu'un canal soit ouvert
        chan = transport.accept(CONNEXION_TIMEOUT)
        
        if chan:
            server.event.wait(10)
            # DYNAMIQUE : On récupère le nom d'utilisateur depuis l'instance server
            current_user = server.username
            print(f"[+] Session etablie pour l'utilisateur : {current_user}")
            
            handle_session(chan, current_user)

    except Exception as e:
        print(f"[-] Erreur client : {e}")
    finally:
        if transport: transport.close()

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP_ADDR, SOCKET_PORT))
    server_socket.listen(10)
    
    print(f"[*] Serveur pret sur le port {SOCKET_PORT}")

    while True:
        client, _ = server_socket.accept()
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

if __name__ == "__main__":
    run_server()