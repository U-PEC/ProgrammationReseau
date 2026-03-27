# SSH Server (Paramiko) — Project

This repository contains a basic SSH server implemented in Python using Paramiko for the Programming Réseau course.

**Quick facts**
- **Listen port:** 6767 (default)
- **Start command:** `python -m src`
- **Host key:** `server.key` (see docs/STARTUP.md)
- **Python:** 3.8+

**Install**
1. Create and activate a venv:

```bash
python3 -m venv .venv
source .venv/bin/activate
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```

**Generate host key (if missing)**

```bash
ssh-keygen -t rsa -f server.key -N ""
```

**Run**

```bash
python -m src
```

**Testing**

Open a separate terminal and connect using a standard SSH client:

```bash
ssh admin@localhost -p 6767
```

See the `docs` folder for more details: [docs/STARTUP.md](docs/STARTUP.md), [docs/USAGE.md](docs/USAGE.md), [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md), [docs/TECHNICAL_DOCS.md](docs/TECHNICAL_DOCS.md).
