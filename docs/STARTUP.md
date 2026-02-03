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

Exécutez le script principal (assurez-vous que votre fichier se nomme `main.py` ou adaptez le nom) :

```bash
python main.py
```

Le serveur écoutera par défaut sur le port **2222**.

---

## 🧪 Tester la connexion

Ouvrez un nouveau terminal et connectez-vous avec la commande `ssh` standard :

```bash
ssh admin@localhost -p 2222
```

* **Utilisateur :** `admin`
* **Mot de passe :** `password123`

---

## 📁 Structure du projet
```text
.
├── .venv/               # Environnement virtuel (non suivi par Git)
├── server.key           # Clé privée du serveur (générée)
├── requirements.txt     # Liste des dépendances
└── main.py              # Code source du serveur
```