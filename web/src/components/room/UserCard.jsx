import { User, Mic } from "lucide-react";
import { useLocalParticipant } from "@livekit/components-react";

function UserCard({ name }) {
  const { isMicrophoneEnabled } = useLocalParticipant();

  return (
    <div className="bg-white rounded-2xl shadow p-6">

      <div className="flex items-center gap-5">

        <div className="bg-blue-100 p-5 rounded-full">
          <User className="text-blue-600" />
        </div>

        <div>

          <h2 className="font-bold text-xl">
            {name}
          </h2>

          <div className="flex items-center gap-2 mt-2">

            <Mic
              size={18}
              className={
                isMicrophoneEnabled
                  ? "text-green-600"
                  : "text-red-600"
              }
            />

            <span>
              {isMicrophoneEnabled
                ? "Microphone On"
                : "Microphone Muted"}
            </span>

          </div>

        </div>

      </div>

    </div>
  );
}

export default UserCard;