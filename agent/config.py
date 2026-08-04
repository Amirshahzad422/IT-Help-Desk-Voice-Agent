import os
from dotenv import load_dotenv

load_dotenv()

# LiveKit
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "ws://localhost:7880")

LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")

LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

# Ollama
OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/v1"
)

OLLAMA_MODEL = "llama3.2:3b"

# Whisper 
WHISPER_URL = os.getenv(
    "WHISPER_URL",
    "http://localhost:8000/v1"
)

# Piper 
PIPER_URL = os.getenv(
    "PIPER_URL",
    "http://localhost:5000"
)

MAX_TOKENS = 100