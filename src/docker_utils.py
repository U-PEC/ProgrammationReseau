import os
import subprocess
from typing import Optional
from .logger import logger


def check_docker_available() -> None:
    """Checks if Docker is installed and the daemon is running.
    Raises SystemExit with a critical log message if not available.
    """
    try:
        result = subprocess.run(["docker", "info"], capture_output=True, text=True)
        if result.returncode != 0:
            logger.critical("Docker daemon is not running or accessible. Please start Docker before running the server.")
            raise SystemExit(1)
    except FileNotFoundError:
        logger.critical("Docker is not installed or not found in PATH. Please install Docker.")
        raise SystemExit(1)


def cleanup_zombie_containers() -> None:
    """Removes any orphaned Docker containers from previous unclean shutdowns."""
    try:
        logger.info("Cleaning up orphaned Docker containers...")
        result = subprocess.run(
            ["docker", "ps", "-a", "-q", "--filter", "name=ssh_session_"],
            capture_output=True, text=True
        )
        containers = [c for c in result.stdout.strip().split('\n') if c]
        if containers:
            subprocess.run(["docker", "rm", "-f"] + containers, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logger.info(f"Removed {len(containers)} orphaned container(s).")
    except FileNotFoundError:
        logger.error("Docker is not installed or not found in PATH.")
    except Exception as e:
        logger.error(f"Error cleaning up containers: {e}")


def start_container(container_name: str, user_home: str, username: str, slave_fd: int) -> subprocess.Popen:
    """Start the user session container attached to the provided slave PTY fd.

    Returns the subprocess.Popen object for the running container process.
    """
    docker_cmd = [
        "docker", "run", "-it", "--rm",
        "--name", container_name,
        "-v", f"{user_home}:/home/{username}",
        "-w", f"/home/{username}",
        "alpine", "sh"
    ]

    proc = subprocess.Popen(
        docker_cmd,
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        preexec_fn=os.setsid
    )
    return proc


def remove_container(container_name: str) -> None:
    """Force-remove a container by name (best-effort)."""
    try:
        subprocess.run(["docker", "rm", "-f", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        logger.debug("Docker not found when attempting to remove container.")
    except Exception as e:
        logger.error(f"Error removing container {container_name}: {e}")
