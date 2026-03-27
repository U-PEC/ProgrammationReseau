# Project Overview

Brief
-----
This repository implements a teaching-grade SSH server in Python that provides an interactive, containerized shell per authenticated user. It is designed for learning and experimentation rather than production use.

Key capabilities
----------------
- Password and public-key authentication using Paramiko.
- Interactive shell per user inside an ephemeral Docker container (Alpine).
- File persistence per user under `users_storage/` and a SQLite-backed user database.

Core components (quick map)
---------------------------
- `src/runner.py` — main entry: accepts TCP connections, wraps sockets with Paramiko `Transport`, and spawns a thread per client.
- `src/server.py` — `MyServer` (Paramiko `ServerInterface`) handles authentication and channel requests.
- `src/user_manager.py` — user DB access and authentication helpers (uses salted PBKDF2 hashes via `password_utils.py`).
- `src/shell.py` — creates a PTY, starts the session Docker container and bridges I/O using `selectors`.
- `src/docker_utils.py` — Docker availability check, cleanup, container start/remove helpers.
- `src/sftp_server.py` — optional SFTP server implementation (if present).
- `docs/` — user-facing documentation and prompts history.

Quick start
-----------
1. Ensure Docker is installed and the daemon is running.
2. Create and activate a Python virtualenv.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize or reset the DB (optional): remove `server/db/users.db` to re-run `data.sql` on first start.
5. Start the server from repository root:
   ```bash
   python -m server
   ```

Notes on configuration
----------------------
- Network and runtime parameters are in `src/config.py` (reads `server.conf` if present). Notable constants: `SOCKET_PORT`, `CONNECTION_TIMEOUT`, `LISTEN_BACKLOG`.
- Host private key must be present in `server/.ssh/` as configured in `src/config.py`.

Security & operational considerations
------------------------------------
- Passwords are stored as PBKDF2-HMAC-SHA256 with per-user salt and iterations (see `src/password_utils.py`).
- User sessions run inside Docker containers mounted only with the user's home directory to reduce host exposure.
- The server includes a startup cleanup routine to remove orphaned containers named `ssh_session_*`.

Where to look for details
-------------------------
- `docs/TECHNICAL_DOCS.md` — deep technical explanations and sequence diagrams.
- `docs/USAGE.md` — examples and client commands.
- `docs/PROMPTS.md` — prompts used when designing and auditing the project.
- `docs/PRESENTATION.md` — slide outline and AI prompt template (for generating a presentation).
