import { useState } from "react";
import {
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  Monitor,
  MonitorOff,
  PhoneOff,
} from "lucide-react";

import {
  useLocalParticipant,
  useRoomContext,
} from "@livekit/components-react";

function ControlBar({ onLeave }) {
  const room = useRoomContext();
  const { localParticipant } = useLocalParticipant();

  const [micEnabled, setMicEnabled] = useState(true);
  const [speakerEnabled, setSpeakerEnabled] = useState(true);
  const [sharing, setSharing] = useState(false);
  const [ending, setEnding] = useState(false);

  const toggleMic = async () => {
    try {
      const newState = !micEnabled;

      await localParticipant.setMicrophoneEnabled(newState);

      setMicEnabled(newState);
    } catch (err) {
      console.error("Failed to toggle microphone:", err);
    }
  };

  const toggleSpeaker = () => {
    const newState = !speakerEnabled;

    setSpeakerEnabled(newState);

    document.querySelectorAll("audio").forEach((audio) => {
      audio.muted = !newState;
    });
  };

  const toggleScreenShare = async () => {
    try {
      const newState = !sharing;

      await localParticipant.setScreenShareEnabled(newState);

      setSharing(newState);
    } catch (err) {
      console.error("Failed to toggle screen sharing:", err);
    }
  };

  const endCall = async () => {
    if (ending) return;

    try {
      setEnding(true);

      console.log("Ending call...");

      await room.disconnect();

      console.log("LiveKit room disconnected");
    } catch (err) {
      console.error("Failed to end call:", err);

      // Fallback in case disconnect throws
      onLeave();
    }
  };

  return (
    <div className="bg-white rounded-3xl shadow-2xl border border-gray-200 p-8">

      <h2 className="text-2xl font-bold text-center mb-8">
        Call Controls
      </h2>

      <div className="flex justify-center gap-10 flex-wrap">

        {/* Microphone */}
        <div className="flex flex-col items-center">

          <button
            title="Microphone"
            onClick={toggleMic}
            disabled={ending}
            className={`w-16 h-16 rounded-full shadow-lg transition-all duration-300 hover:scale-110 text-white flex items-center justify-center ${
              micEnabled
                ? "bg-blue-600 hover:bg-blue-700"
                : "bg-gray-500 hover:bg-gray-600"
            }`}
          >
            {micEnabled ? (
              <Mic size={28} />
            ) : (
              <MicOff size={28} />
            )}
          </button>

          <span className="mt-3 text-sm font-medium text-gray-700">
            Microphone
          </span>

        </div>


        {/* Speaker */}
        <div className="flex flex-col items-center">

          <button
            title="Speaker"
            onClick={toggleSpeaker}
            disabled={ending}
            className={`w-16 h-16 rounded-full shadow-lg transition-all duration-300 hover:scale-110 text-white flex items-center justify-center ${
              speakerEnabled
                ? "bg-green-600 hover:bg-green-700"
                : "bg-gray-500 hover:bg-gray-600"
            }`}
          >
            {speakerEnabled ? (
              <Volume2 size={28} />
            ) : (
              <VolumeX size={28} />
            )}
          </button>

          <span className="mt-3 text-sm font-medium text-gray-700">
            Speaker
          </span>

        </div>


        {/* Screen Share */}
        <div className="flex flex-col items-center">

          <button
            title="Share Screen"
            onClick={toggleScreenShare}
            disabled={ending}
            className={`w-16 h-16 rounded-full shadow-lg transition-all duration-300 hover:scale-110 text-white flex items-center justify-center ${
              sharing
                ? "bg-purple-600 hover:bg-purple-700"
                : "bg-gray-500 hover:bg-gray-600"
            }`}
          >
            {sharing ? (
              <MonitorOff size={28} />
            ) : (
              <Monitor size={28} />
            )}
          </button>

          <span className="mt-3 text-sm font-medium text-gray-700">
            Share Screen
          </span>

        </div>


        {/* End Call */}
        <div className="flex flex-col items-center">

          <button
            title="End Call"
            onClick={endCall}
            disabled={ending}
            className="w-16 h-16 rounded-full bg-red-600 hover:bg-red-700 disabled:bg-gray-400 shadow-lg transition-all duration-300 hover:scale-110 text-white flex items-center justify-center"
          >
            <PhoneOff size={28} />
          </button>

          <span className="mt-3 text-sm font-medium text-gray-700">
            {ending ? "Ending..." : "End Call"}
          </span>

        </div>

      </div>

    </div>
  );
}

export default ControlBar;