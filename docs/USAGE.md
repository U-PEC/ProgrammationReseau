# Usage

This document shows common usage examples for the SSH server.

Start the server (from project root):

```bash
source .venv/bin/activate
python -m src
```

Connect with the system `ssh` client:

```bash
ssh admin@localhost -p 6767
```

If you use PuTTY on Windows, configure host `localhost` and port `6767`, and set username `admin`.

Troubleshooting:
- If the server refuses the connection, ensure the host key `server.key` exists.
- Check `logs/` for server logs.
- Ensure `requirements.txt` dependencies are installed.
