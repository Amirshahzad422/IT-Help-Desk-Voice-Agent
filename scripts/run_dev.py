from __future__ import annotations

import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PROCESSES: list[tuple[str, subprocess.Popen[bytes]]] = []


def read_env() -> dict[str, str]:
    """Read the simple KEY=value settings used by this project."""
    values = dict(os.environ)
    env_file = ROOT / ".env"
    if not env_file.exists():
        return values

    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    return values


def endpoint_port(url: str, setting: str) -> int:
    parsed = urlparse(url)
    if not parsed.hostname or not parsed.port:
        raise RuntimeError(f"{setting} must be a URL with an explicit port.")
    return parsed.port


def port_open(port: int, host: str = "127.0.0.1") -> bool:
    try:
        with socket.create_connection((host, port), timeout=0.5):
            return True
    except OSError:
        return False


def wait_for_port(name: str, port: int, timeout: int = 45) -> None:
    print(f"Waiting for {name} on port {port}...", flush=True)
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if port_open(port):
            return
        time.sleep(0.5)
    raise RuntimeError(f"{name} did not become available on port {port}.")


def start(name: str, command: list[str], *, cwd: Path = ROOT) -> None:
    print(f"Starting {name}: {' '.join(command)}", flush=True)
    flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    process = subprocess.Popen(command, cwd=cwd, creationflags=flags)
    PROCESSES.append((name, process))
    time.sleep(0.3)
    if process.poll() is not None:
        raise RuntimeError(f"{name} stopped immediately (exit code {process.returncode}).")


def ensure_ollama_model(model: str) -> None:
    """Make the model configured for the agent available before it starts."""
    check = subprocess.run(["ollama", "show", model], cwd=ROOT, check=False)
    if check.returncode == 0:
        print(f"Ollama model '{model}' is available.", flush=True)
        return

    print(f"Downloading Ollama model '{model}'...", flush=True)
    subprocess.run(["ollama", "pull", model], cwd=ROOT, check=True)


def stop_all() -> None:
    for name, process in reversed(PROCESSES):
        if process.poll() is not None:
            continue
        print(f"Stopping {name}...", flush=True)
        try:
            if os.name == "nt":
                process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                process.send_signal(signal.SIGINT)
            process.wait(timeout=8)
        except (OSError, subprocess.TimeoutExpired):
            process.terminate()


def main() -> None:
    env = read_env()
    whisper_port = endpoint_port(env.get("WHISPER_URL", ""), "WHISPER_URL")
    piper_port = endpoint_port(env.get("PIPER_URL", ""), "PIPER_URL")
    ollama_port = endpoint_port(env.get("OLLAMA_URL", ""), "OLLAMA_URL")
    ollama_model = env.get("OLLAMA_MODEL", "").strip()

    if whisper_port == 8000:
        raise RuntimeError(
            "WHISPER_URL cannot use port 8000: the token API and Vite proxy use it. "
            "Set Whisper to port 8001 instead."
        )
    if not ollama_model:
        raise RuntimeError("OLLAMA_MODEL is missing from .env.")

    subprocess.run(
        ["docker", "compose", "-f", "infra/docker-compose.yml", "up", "-d"],
        cwd=ROOT,
        check=True,
    )
    wait_for_port("LiveKit", 7880)

    if not port_open(ollama_port):
        start("Ollama", ["ollama", "serve"])
        wait_for_port("Ollama", ollama_port)
    else:
        print("Ollama is already running; reusing it.", flush=True)
    ensure_ollama_model(ollama_model)

    start("token API", [sys.executable, "-m", "uvicorn", "server.main:app", "--host", "127.0.0.1", "--port", "8000"])
    wait_for_port("token API", 8000)
    start("Whisper", [sys.executable, "-m", "uvicorn", "services.whisper_server:app", "--host", "127.0.0.1", "--port", str(whisper_port)])
    wait_for_port("Whisper", whisper_port, timeout=120)
    start("Piper", [sys.executable, "-m", "uvicorn", "services.piper_server:app", "--host", "127.0.0.1", "--port", str(piper_port)])
    wait_for_port("Piper", piper_port)
    start("agent worker", [sys.executable, "-m", "agent.agent", "dev"])

    print("\nBackend ready. Start the frontend separately with 'npm run dev' in web. (Ctrl+C stops the backend stack)", flush=True)
    while True:
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as error:
        print(f"\nStartup failed: {error}", file=sys.stderr, flush=True)
    finally:
        stop_all()
