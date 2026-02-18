# 🚀 Guide de démarrage : Serveur SSH avec Paramiko

Ce projet implémente un serveur SSH basique en Python pour le cours de **Réseau Avancé**. Il permet de comprendre la négociation du transport SSH, l'authentification et la gestion des canaux.

---

## 🛠️ Installation et Configuration

### 1. Prérequis
Assurez-vous d'avoir **Python 3.8+** installé sur votre machine.

### 2. Création de l'environnement virtuel (venv)
Il est fortement recommandé d'utiliser un environnement virtuel pour isoler les dépendances.

* **Windows :**
    ```bash
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```
* **macOS / Linux :**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

### 3. Installation des dépendances
Une fois l'environnement activé, installez Paramiko via le fichier `requirements.txt`.

```bash
pip install -r requirements.txt
```

> **Contenu du fichier `requirements.txt` :**
> ```text
> paramiko>=3.4.0
> cryptography>=42.0.0
> ```

---

## 🔑 Génération de la Clé d'Hôte (Host Key)

Pour que le serveur SSH puisse s'identifier auprès des clients, il a besoin d'une clé RSA privée. Générez-la avec la commande suivante dans votre terminal :

```bash
ssh-keygen -t rsa -f server.key -N ""
```

* `-t rsa` : Type de clé (RSA).
* `-f server.key` : Nom du fichier de sortie.
* `-N ""` : Mot de passe vide (passphrase).

---

## 🏃 Lancement du serveur

Le code source étant maintenant dans un module (`src`), il doit être lancé comme tel :

```bash
python -m src
```

Le serveur écoutera par défaut sur le port **6767**.

---

## 🧪 Tester la connexion

Ouvrez un nouveau terminal et connectez-vous avec la commande `ssh` standard :

```bash
ssh admin@localhost -p 6767
```

* **Utilisateur :** `admin`
* **Mot de passe :** `password123`

---

## 📁 Structure du projet
```text
.
├── .venv/               # Environnement virtuel (non suivi par Git)
├── .ssh/                # Clés du serveur
├── docs/                # Documentation
├── logs/                # Fichiers de log
├── users_storage/       # Données des utilisateurs
├── requirements.txt     # Liste des dépendances
└── src/                 # Code source du serveur
    ├── __init__.py
    ├── __main__.py
    ├── main.py
    ├── server.py
    ├── config.py
    ├── shell.py
    └── user_manager.py
```