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

### 4. Start Backend File

```bash
python.exe scripts\run_dev.py
```
### 5. Start Frontend

Open a new terminal:

```powershell
scripts\run_frontend.bat
```

## Project Report Notes

### Contributors

- Track A: Musfirah Zunnoon
- Track B: Sajeela Affaq Abbasi


### Latency Tuning

Latency was tuned by capping model output with `MAX_TOKENS = 80` and instructing the agent to answer in one or two short sentences.

End-to-end latency reported by the application:

| Turn | Latency |
| --- | ---: |
| 1 | 10,884 ms |
| 2 | 4,401 ms |
| 3 | 4,169 ms |
| 4 | 4,116 ms |
| 5 | 3,437 ms |
| 6 | 3,892 ms |

Average end-to-end latency: approximately **4.32 seconds**.
