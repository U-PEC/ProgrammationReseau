# server/shell.py
import os
import subprocess
import selectors
import pty
import socket
import uuid
from .logger import logger

def handle_session(channel, username, user_home):
    # 1. Utiliser le dossier absolu injecté par runner.py pour la persistance
    os.makedirs(user_home, exist_ok=True)

    # Générer un ID unique pour éviter les conflits si l'utilisateur ouvre plusieurs sessions
    session_id = uuid.uuid4().hex[:8]
    container_name = f"ssh_session_{username}_{session_id}"

    # 2. Préparer la commande Docker
    # -it : Interactif + TTY
    # --rm : Supprime le conteneur à l'arrêt
    # -v : Monte le dossier local dans le conteneur
    # --workdir : Définit le dossier de départ
    docker_cmd = [
        "docker", "run", "-it", "--rm",
        "--name", container_name,
        "-v", f"{user_home}:/home/{username}",
        "-w", f"/home/{username}",
        "alpine", "sh"
    ]

    # 3. Lancer Docker avec un PTY local pour que l'interactivité fonctionne
    master_fd, slave_fd = pty.openpty()
    docker_process = subprocess.Popen(
        docker_cmd,
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        preexec_fn=os.setsid # Crée une nouvelle session de processus
    )
    os.close(slave_fd)

    # 4. Le Pont (Multiplexage)
    selector = selectors.DefaultSelector()
    selector.register(channel, selectors.EVENT_READ)
    selector.register(master_fd, selectors.EVENT_READ)

    channel.send(f"\r\n--- Connexion au Container Isolé (User: {username}) ---\r\n".encode('utf-8'))

    try:
        while docker_process.poll() is None: # Tant que Docker tourne
            events = selector.select(timeout=0.1)
            for key, mask in events:
                if key.fileobj == channel:
                    try:
                        data = channel.recv(1024)
                        if not data: return
                        os.write(master_fd, data)
                    except socket.error:
                        return # SSH Déconnecté
                
                elif key.fileobj == master_fd:
                    try:
                        data = os.read(master_fd, 1024)
                        if not data: return
                        channel.send(data)
                    except OSError:
                        # Levée quand le PTY esclave se ferme (ex: user a tapé `exit` dans le conteneur)
                        return
    finally:
        selector.close()
        os.close(master_fd)
        if docker_process.poll() is None:
            # Forcer la suppression du conteneur côté démon Docker pour éviter les conteneurs zombies
            subprocess.run(["docker", "rm", "-f", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            docker_process.terminate()
        logger.info(f"Docker container {container_name} stopped and removed.")