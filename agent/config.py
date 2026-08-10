from dotenv import load_dotenv
import os

load_dotenv()

LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

WHISPER_URL = os.getenv("WHISPER_URL")
PIPER_URL = os.getenv("PIPER_URL")

MAX_TOKENS = 80