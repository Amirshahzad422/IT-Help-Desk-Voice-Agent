import {
  LiveKitRoom,
  RoomAudioRenderer,
  BarVisualizer,
  useParticipants,
  useVoiceAssistant,
  useRoomContext,
} from "@livekit/components-react";

import CallHeader from "../components/room/CallHeader";
import UserCard from "../components/room/UserCard";
import AgentStatus from "../components/room/AgentStatus";
import RoomInfo from "../components/room/RoomInfo";
import TranscriptPanel from "../components/room/TranscriptPanel";
import ControlBar from "../components/room/ControlBar";
import RpcHandler from "../components/RpcHandler";

import { useEffect } from "react";
import { toast } from "react-hot-toast";


function SetUserIdentity({ username }) {
  const room = useRoomContext();

  useEffect(() => {
    if (!room || !username) return;

    const normalizedUsername = username.trim().toLowerCase();

    room.localParticipant
      .setAttributes({
        helpdesk_username: normalizedUsername,
      })
      .then(() => {
        console.log(
          "Help Desk username set:",
          normalizedUsername
        );
      })
      .catch((error) => {
        console.error(
          "Failed to set Help Desk username:",
          error
        );
      });
  }, [room, username]);

  return null;
}


function VoiceActivity() {
  const { state, audioTrack } = useVoiceAssistant();

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">
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
    <div className="min-h-screen">

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

  const handleDisconnected = () => {
    console.log("LiveKit room disconnected");

    // Remove every active toast from this call
    toast.dismiss();

    // Return to the previous screen
    onLeave();
  };


  return (
    <LiveKitRoom
      serverUrl={tokenData.server_url}
      token={tokenData.token}
      connect={true}
      audio={true}
      video={false}
      onDisconnected={handleDisconnected}
    >

      <SetUserIdentity
        username={userName}
      />

      <RoomContent
        tokenData={tokenData}
        userName={userName}
        onLeave={onLeave}
      />

    </LiveKitRoom>
  );
}


export default Room;