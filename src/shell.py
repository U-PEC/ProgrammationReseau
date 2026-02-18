# server/shell.py
import os
import pty
import selectors
import termios
import struct
import fcntl
import signal

def handle_session(chan, user_home):
    """
    Gère une session shell réelle en utilisant un PTY et un Selector (epoll/kqueue).
    """
    # 1. Création du terminal virtuel (PTY)
    master_fd, slave_fd = pty.openpty()

    # 2. Fork du processus pour lancer le vrai Shell
    pid = os.fork()

    if pid == 0:  # --- PROCESSUS ENFANT ---
        os.close(master_fd)
        os.login_tty(slave_fd)
        
        # On se place dans le dossier de l'utilisateur
        os.chdir(user_home)
        
        # Lancement du shell système (zsh sur Mac, bash sur Linux)
        # On définit un environnement minimal pour éviter les bugs
        env = os.environ.copy()
        env["TERM"] = "xterm-256color"
        os.execve('/bin/zsh', ['/bin/zsh', '-i'], env)

    else:  # --- PROCESSUS PARENT (Le serveur SSH) ---
        os.close(slave_fd)
        
        # Configuration du sélecteur (utilisera epoll sur Linux, kqueue sur Mac)
        sel = selectors.DefaultSelector()
        
        # On enregistre le canal SSH et le PTY master pour la lecture
        sel.register(chan, selectors.EVENT_READ)
        sel.register(master_fd, selectors.EVENT_READ)

        chan.send(f"\r\n--- Vrai Shell System (Session: {os.path.basename(user_home)}) ---\r\n")

        try:
            while True:
                # On attend une activité sur l'un des deux descripteurs
                events = sel.select(timeout=None)
                for key, mask in events:
                    
                    # CAS A : Données venant du client SSH -> On les écrit dans le PTY
                    if key.fileobj == chan:
                        data = chan.recv(1024)
                        if not data:
                            return # Déconnexion client
                        os.write(master_fd, data)

                    # CAS B : Données venant du Shell (Zsh) -> On les envoie au client SSH
                    elif key.fileobj == master_fd:
                        try:
                            data = os.read(master_fd, 1024)
                            if not data:
                                return # Shell fermé
                            chan.send(data)
                        except OSError:
                            return

        except Exception as e:
            print(f"[-] Erreur dans la boucle de session : {e}")
        finally:
            # Ménage
            sel.unregister(chan)
            sel.unregister(master_fd)
            sel.close()
            os.close(master_fd)
            try:
                os.kill(pid, signal.SIGTERM)
            except:
                pass