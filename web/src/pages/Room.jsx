import {
  LiveKitRoom,
  RoomAudioRenderer,
  BarVisualizer,
  useParticipants,
  useVoiceAssistant,
} from "@livekit/components-react";

import CallHeader from "../components/room/CallHeader";
import UserCard from "../components/room/UserCard";
import AgentStatus from "../components/room/AgentStatus";
import RoomInfo from "../components/room/RoomInfo";
import TranscriptPanel from "../components/room/TranscriptPanel";
import ControlBar from "../components/room/ControlBar";
import RpcHandler from "../components/RpcHandler";


function VoiceActivity() {
  const { state, audioTrack } = useVoiceAssistant();

  return (
    <div className="bg-white rounded-3xl shadow-xl border border-gray-200 p-8">
      <h2 className="text-xl font-bold mb-6">
        Voice Activity
      </h2>

      <div className="h-24 flex items-center justify-center">
        {audioTrack ? (
          <BarVisualizer
            state={state}
            trackRef={audioTrack}
            barCount={7}
          />
        ) : (
          <div className="text-gray-400 text-sm">
            Waiting for voice activity...
          </div>
        )}
      </div>
    </div>
  );
}


function RoomContent({
  tokenData,
  userName,
  onLeave,
}) {
  const participants = useParticipants();

  const agentConnected = participants.length > 1;

  return (
    <div className="min-h-screen bg-gray-100">

      {/* Play remote audio */}
      <RoomAudioRenderer />

      {/* RPC notifications */}
      <RpcHandler />

      <CallHeader room={tokenData.room} />

      <div className="max-w-7xl mx-auto px-8 py-10">

        {/* Top Cards */}
        <div className="grid md:grid-cols-3 gap-8">

          <UserCard
            name={userName}
          />

          <AgentStatus
            connected={agentConnected}
          />

          <RoomInfo />

        </div>


        {/* Voice Activity */}
        <div className="mt-12">

          <VoiceActivity />

        </div>


        {/* Transcript */}
        <div className="mt-12">

          <div className="bg-white rounded-3xl shadow-xl border border-gray-200 p-6">

            <TranscriptPanel />

          </div>

        </div>


        {/* Call Controls */}
        <ControlBar
          onLeave={onLeave}
        />

      </div>

    </div>
  );
}


function Room({
  tokenData,
  userName,
  onLeave,
}) {
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
        onLeave={onLeave}
      />

    </LiveKitRoom>
  );
}


export default Room;