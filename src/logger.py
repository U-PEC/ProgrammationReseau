# server/src/logger.py
import logging
import os
import sys
from .config import LOG_DIR, LOG_FILE

# Ensure the log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Create a custom logger
logger = logging.getLogger("ssh_server")
logger.setLevel(logging.INFO)

# Prevent adding multiple handlers if imported multiple times
if not logger.handlers:
    # 1. Console Handler (Outputs to terminal)
    c_handler = logging.StreamHandler(sys.stdout)
    c_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    c_handler.setFormatter(c_format)
    c_handler.setLevel(logging.INFO)

    # 2. File Handler (Outputs to logs/server.log)
    f_handler = logging.FileHandler(LOG_FILE)
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    f_handler.setLevel(logging.INFO)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)