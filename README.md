# IT Help Desk Voice Agent

A self-hosted AI-powered voice-enabled IT Help Desk Agent built using LiveKit, Ollama, SQLite, and FastAPI.

## Requirements

- Python 3.11+
- Node.js 20+
- Docker Desktop
- LiveKit Server
- Ollama (llama3.2:3b)
- SQLite
- faster-whisper
- Piper

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd IT-Help-Desk-Voice-Agent
```

### 2. Create a virtual environment

```bash
uv venv
```

Activate it:

**PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
uv pip install -r requirements.txt
```

or

```bash
pip install -r requirements.txt
```

### 4. Start LiveKit

```bash
docker compose -f infra/docker-compose.yml up
```

### 5. Start Ollama

```bash
ollama serve
```


### 6. Start Whisper

powershell
uvicorn services.whisper_server:app --host 127.0.0.1 --port 8000


### 7. Start Piper

powershell
uvicorn services.piper_server:app --host 127.0.0.1 --port 5000


### 8. Start Agent Worker

powershell
python -m agent.agent dev

Expected successful line:

text
registered worker