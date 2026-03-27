# 🚀 Guide de démarrage : Serveur SSH avec Paramiko

Ce projet fournit un serveur SSH minimal pour apprentissage et tests. Le document ci‑dessous explique l'installation, le démarrage et des notes de portabilité (epoll vs kqueue).

---

## 🛠️ Prérequis
- Python 3.8+
- `ssh-keygen` (fourni par OpenSSH)
- Virtualenv recommandé

## Création de l'environnement virtuel

macOS / Linux :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell) :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## Installation des dépendances

```bash
pip install -r requirements.txt
```

Contenu attendu de `requirements.txt` :

```text
paramiko>=4.0.0
cryptography>=42.0.0
```

---

## 🔑 Génération de la clé d'hôte (host key)

Le serveur doit disposer d'une clé privée pour s'identifier auprès des clients. Depuis la racine du projet :

```bash
ssh-keygen -t rsa -f server.key -N ""
```

Placez `server.key` dans le dossier racine du projet (même répertoire que `requirements.txt`). Le fichier public `server.key.pub` est généré automatiquement.

---

## 🏃 Démarrage du serveur

Depuis la racine du projet :

```bash
source .venv/bin/activate
python -m src
```

Par défaut le serveur écoute sur le port `6767`. Voir `src/config.py` si vous souhaitez changer le port ou l'adresse d'écoute.

---

## 🔎 Tester la connexion

Ouvrez un autre terminal et connectez‑vous :

```bash
ssh admin@localhost -p 6767
```

Compte de test inclus : `admin` (mot de passe `password123`) — voir `users_storage/`.

---

## 🧭 Epoll, selectors et portabilité

- `epoll` est l'API Linux recommandée pour gérer efficacement un grand nombre de sockets.
- macOS / BSD utilisent `kqueue` au lieu d'`epoll`.
- Le module Python `selectors` offre une interface portable : `selectors.DefaultSelector()` sélectionne automatiquement `EpollSelector` sur Linux ou `KqueueSelector` sur macOS.

Recommandations :
- Pour le développement local sur macOS, utiliser `selectors.DefaultSelector()` suffit.
- Si l'évaluation exige explicitement `epoll`, exécutez le serveur sur une machine Linux (VM/Docker) et activez `selectors.EpollSelector()` si nécessaire.

Exemple rapide d'utilisation :

```python
import selectors
sel = selectors.DefaultSelector()
```

---

## 🛠️ Dépannage

- Connexion refusée : vérifier que `python -m src` tourne et que le port `6767` est ouvert.
- Clé d'hôte manquante : générez `server.key` comme indiqué ci‑dessus.
- Erreurs d'authentification : consultez `users_storage/` et `logs/`.

---

## 📁 Structure du projet (résumé)

```
.  # racine du projet
├── server.key           # clé d'hôte (générée)
├── requirements.txt
├── docs/
│   ├── STARTUP.md
│   ├── USAGE.md
│   ├── PROJECT_OVERVIEW.md
│   └── TECHNICAL_DOCS.md
├── logs/
├── users_storage/
└── src/
    ├── __main__.py
    ├── server.py
    ├── runner.py
    ├── shell.py
    └── user_manager.py
```

---

Si vous voulez que j'ajoute une commande `docker-compose` pour exécuter le serveur dans un conteneur Linux (utile pour tester `epoll`), dites‑le et je la prépare.
