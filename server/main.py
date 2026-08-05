import os
import uuid
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from livekit import api

load_dotenv()

app = FastAPI(
    title="IT Help Desk Voice Agent Token Server"
)

LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")


if not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET:
    raise RuntimeError(
        "LiveKit API credentials are missing. Check your .env file."
    )


@app.get("/")
def health_check():
    return {
        "status": "Token server running"
    }


@app.post("/token")
def generate_token():
    try:
        # Generate a unique room name
        room_name = f"helpdesk-{uuid.uuid4().hex[:8]}"

        # Generate a unique participant identity
        identity = f"user-{uuid.uuid4().hex[:6]}"

        # Create LiveKit JWT token
        token = (
            api.AccessToken(
                LIVEKIT_API_KEY,
                LIVEKIT_API_SECRET
            )
            .with_identity(identity)
            .with_grants(
                api.VideoGrants(
                    room_join=True,
                    room=room_name,
                    can_publish=True,
                    can_subscribe=True
                )
            )
            .to_jwt()
        )

        return {
            "server_url": LIVEKIT_URL,
            "room": room_name,
            "participant": identity,
            "token": token
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )