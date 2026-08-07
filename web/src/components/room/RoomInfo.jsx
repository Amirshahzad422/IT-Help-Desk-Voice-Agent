import { useParticipants } from "@livekit/components-react";
import { Users } from "lucide-react";

function RoomInfo() {
  const participants = useParticipants();

  return (
    <div className="bg-white rounded-2xl shadow p-6">

      <div className="flex items-center gap-3">

        <Users className="text-blue-600" />

        <h2 className="font-bold">
          Participants
        </h2>

      </div>

      <p className="mt-4 text-4xl font-bold">
        {participants.length}
      </p>

    </div>
  );
}

export default RoomInfo;