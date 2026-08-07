import os
import uuid
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from livekit import api
from livekit.api import LiveKitAPI
from livekit.protocol.room import ListRoomsRequest


load_dotenv()

app = FastAPI(
    title="IT Help Desk Voice Agent Token Server"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

if not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET:
    raise RuntimeError(
        "LiveKit API credentials are missing. Check your .env file."
    )


# LiveKit server API client
livekit_api = LiveKitAPI(
    url=LIVEKIT_URL,
    api_key=LIVEKIT_API_KEY,
    api_secret=LIVEKIT_API_SECRET
)


@app.get("/")
def health_check():
    return {
        "status": "Token server running"
    }


@app.post("/api/token")
async def generate_token():
    try:
        # Get currently active rooms
        rooms_response = await livekit_api.room.list_rooms(
            ListRoomsRequest()
        )

        active_rooms = [
            room.name
            for room in rooms_response.rooms
        ]

        # Generate room name and avoid collisions
        while True:
            room_name = f"helpdesk-{uuid.uuid4().hex[:8]}"

            if room_name not in active_rooms:
                break

        # Generate participant identity
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