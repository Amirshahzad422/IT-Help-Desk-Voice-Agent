import { LiveKitRoom, useParticipants } from "@livekit/components-react";

import CallHeader from "../components/room/CallHeader";
import UserCard from "../components/room/UserCard";
import AgentStatus from "../components/room/AgentStatus";
import RoomInfo from "../components/room/RoomInfo";
import TranscriptPanel from "../components/room/TranscriptPanel";
import CallControls from "../components/room/CallControls";

function RoomContent({ tokenData, userName }) {
  const participants = useParticipants();

  const agentConnected = participants.length > 1;

  return (
    <div className="min-h-screen bg-gray-100">

      <CallHeader room={tokenData.room} />

      <div className="max-w-7xl mx-auto p-8">

        <div className="grid md:grid-cols-3 gap-8">

          <UserCard
            name={userName}
          />

          <AgentStatus
            connected={agentConnected}
          />

          <RoomInfo />

        </div>

        <div className="mt-8">

          <TranscriptPanel />

        </div>

        <CallControls />

      </div>

    </div>
  );
}

function Room({ tokenData, userName }) {
  return (
    <LiveKitRoom
      serverUrl={tokenData.server_url}
      token={tokenData.token}
      connect
      audio
      video={false}
    >
      <RoomContent
        tokenData={tokenData}
        userName={userName}
      />
    </LiveKitRoom>
  );
}

export default Room;