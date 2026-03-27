# Project Overview

Purpose: provide a minimal SSH server implementation (learning project) that accepts standard SSH clients and demonstrates transport, authentication, and channel handling via Paramiko.

Main components:
- `src/server.py` — connection handling and Paramiko integration.
- `src/shell.py` — interactive shell channel handling.
- `src/user_manager.py` — user data and authentication helpers.
- `src/runner.py` / `src/__main__.py` — entry points to start the server.
- `docs/STARTUP.md` — setup and host key generation instructions.

Auth: the project currently supports simple username/password authentication (see `users_storage/` for test users such as `admin`).

Design notes:
- The code is intended to be portable; on Linux you can enable `epoll`-based selectors for scalability. On macOS the default `selectors` module will select the appropriate backend (kqueue).
