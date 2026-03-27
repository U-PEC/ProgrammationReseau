# Technical Documentation

This document collects technical details about the server implementation and design decisions.

1) Networking model
- The server listens on TCP port 6767 and negotiates SSH using Paramiko. The project is single-process Python code that handles connections via blocking sockets (or a selector loop if present).

2) Epoll and selectors
- `epoll` is a Linux kernel API optimized for waiting on large numbers of file descriptors. For portability the Python `selectors` module should be used. `selectors.DefaultSelector()` picks the platform-optimal implementation (`EpollSelector` on Linux, `KqueueSelector` on macOS/BSD).

3) Authentication and users
- User data is stored under `users_storage/` for examples. `src/user_manager.py` implements lookup and verification routines used by the Paramiko server.

4) Host keys and cryptography
- Host keys should be created with `ssh-keygen -t rsa -f server.key -N ""`. The server loads this key on startup to identify itself to clients.

5) Logs
- Server logs are written to the `logs/` directory (see `src/logger.py`). Check logs for runtime errors and auth events.

6) Running on Linux vs macOS
- If evaluation requires `epoll`, run the server on a Linux environment (VM or Docker) and ensure the server uses `selectors.EpollSelector()` or `selectors.DefaultSelector()` (which will pick epoll on Linux).

7) Extending the server
- Add key-based auth by implementing Paramiko's `ServerInterface.check_auth_publickey` and storing authorized public keys in `users_storage/<user>/.ssh/authorized_keys`.
