import { Mic, MicOff, PhoneOff, Volume2, VolumeX } from "lucide-react";
import { useLocalParticipant } from "@livekit/components-react";
import { useState } from "react";

function CallControls() {
  const { localParticipant } = useLocalParticipant();

  const [muted, setMuted] = useState(false);
  const [speaker, setSpeaker] = useState(true);

  const toggleMic = async () => {
    await localParticipant.setMicrophoneEnabled(muted);
    setMuted(!muted);
  };

  const toggleSpeaker = () => {
    // UI only for now
    setSpeaker(!speaker);
  };

  return (
    <div className="flex justify-center gap-8 mt-8">

      <button
        onClick={toggleMic}
        className="bg-blue-600 text-white p-4 rounded-full hover:bg-blue-700"
      >
        {muted ? <MicOff /> : <Mic />}
      </button>

      <button
        onClick={() => window.location.reload()}
        className="bg-red-600 text-white p-4 rounded-full hover:bg-red-700"
      >
        <PhoneOff />
      </button>

      <button
        onClick={toggleSpeaker}
        className="bg-gray-700 text-white p-4 rounded-full"
      >
        {speaker ? <Volume2 /> : <VolumeX />}
      </button>

    </div>
  );
}

export default CallControls;