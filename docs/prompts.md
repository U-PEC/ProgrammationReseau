# Historique des Prompts (IA)

Ce document retrace les différentes requêtes (prompts) soumises à l'assistant IA (Gemini Code Assist) pour la conception, le développement, la sécurisation et la documentation de ce projet de serveur SSH conteneurisé. Ce suivi répond aux exigences de traçabilité pour l'évaluation du projet.

## 1. Conception, Architecture et Core Features
- *"How can I replace the basic subprocess execution with a real PTY shell?"*
- *"What is the best way to implement logging with separation of concerns?"*
- *"How do I map an encrypted SSH network channel to a local Docker process without blocking the server using selectors?"*

## 2. Authentification et Sécurité (Base de données & Clés)
- *"How do I implement public key authentication alongside the SQLite database?"*
- *"When I try to log in with a user that does not exist it creates a user environment. Is there a problem with this implementation and How to fix the problem if there is one"*
- *"why don't we replace all this by `c.execute("SELECT 1 FROM users WHERE username = ? AND password_hash = ?", (username, hash_password(password)))`. Is there a risk ?"*
- *"I see that when trying to log in I have 3 tries before getting the following message 'Permission denied (password,publickey)'. Where is the code doing this logic?"*
- *"I noticed we do not store salt so it means that we are vulnerable to rainbow attacks, can we add salt?"*
- *"I noticed we do not store salt so it means that we are vulnerable to rainbow attacks, can we add salt?"*
- *"apply the adding of salt"*
- *"can't we keep the authenticate_user function simple by computing the hashed and salted password and running Select 1 where sql command ?\n\nno need to keep the legacy unsalted method I only have tests user I an reacreate the db. I also want you to update the data.sql file"*

## 3. Isolation, Docker et Résilience
- *"Fix the Docker Zombie Container risk if the server is killed abruptly."*
- *"I have an issue when I try to run the server from a new vm for ex it's erroring because docker is not present and then bcz it's not started or whatever. How can I fix this issue?"*
- *"i've stashed the code ... issue when i try to run server from a new vm ... docker is not present ... how can i fix this issue"*

## 4. Audits, Refactoring et Documentation
- *"Analyze my server to check for missing features and current issues."*
- *"Analyze the whole server code base and produce multiple md files one project overview one audit one issues, and the most important one that explains the whole technical flow especially about the usage of paramiko add a paramiko documentation file for me to understand what each methods we are using is doing"*
- *"Generate a powerpoint presentation about my ssh server, add the code architecture, my approach, the prompt used, the sources (even you)"*
- *"génère un fichier à donner dans ma session gemini pour lui expliquer toute la structure du code, tout les composants utilisés, etc..."*
- *"Generate a md file inside docs folder all prompts used to generate this project. My teacher asked us for this school projects to also keep track of prompts that helped us build this project"*
- *"add a paramiko documentation file for me to understand what each methods we are using is doing inside projet/docs/copilot"*
- *"SFTP Support ... Implement the `paramiko.SFTPServerInterface` and update `MyServer.check_channel_subsystem_request` to handle the 'sftp' subsystem."*
- *"analyze the whole server code base and produce multiple md files one project overview one audit one issues, and the most important one that explains the whole technical flow especially about the usage of paramiko"*
- *"yes apply the changes and do not hesitate to move utility functions in another file"*
- *"Notre prof nous a demandé de keep track of the prompts we used for this project. I've already created a prompts.md file with all gemini's prompts used I now ask you to complete it with the  prompts i gave you for this session"*

---

### 💡 Note sur la méthodologie utilisée avec l'IA
L'intelligence artificielle a été employée dans ce projet selon les principes du *Pair Programming* :
1. **Débogage de bas niveau** : Comprendre le comportement interne de bibliothèques complexes comme `paramiko` et `selectors`.
2. **Revue de code (Audit)** : Identifier les failles de sécurité potentielles (création de dossiers non autorisés, conteneurs zombies, attaques de type rainbow table).
3. **Génération de documentation** : Structurer la documentation technique et les supports de présentation (Markdown, outlines PPT).
4. **Refactoring** : Optimiser et condenser des blocs de code logiques (ex: simplification des requêtes SQL d'authentification).

Le code généré a toujours été audité, testé et intégré manuellement pour garantir une maîtrise totale de l'architecture du serveur.

---


