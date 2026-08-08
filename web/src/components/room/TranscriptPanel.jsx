import { useEffect, useRef, useState } from "react";
import { RoomEvent } from "livekit-client";
import { useRoomContext } from "@livekit/components-react";

function TranscriptPanel() {
  const room = useRoomContext();

  const [segments, setSegments] = useState([]);

  // Reference to ONLY the transcript box
  const transcriptBoxRef = useRef(null);

  useEffect(() => {
    if (!room) return;

    const handleTranscription = (
      transcriptionSegments,
      participant
    ) => {
      console.log(
      "LIVE TRANSCRIPT:",
      JSON.stringify(transcriptionSegments, null, 2),
      "PARTICIPANT:",
      participant?.identity
    );
      setSegments((previous) => {
        const updated = [...previous];

        for (const segment of transcriptionSegments) {
          const existingIndex = updated.findIndex(
            (item) => item.id === segment.id
          );

          if (existingIndex >= 0) {
            // Update existing segment
            // while preserving its original order.
            updated[existingIndex] = {
              ...updated[existingIndex],
              ...segment,
              participant,
            };
          } else {
            // First time this segment was received
            updated.push({
              ...segment,
              participant,
              firstReceivedTimestamp: Date.now(),
            });
          }
        }

        // Sort by first-received timestamp
        updated.sort(
          (a, b) =>
            a.firstReceivedTimestamp -
            b.firstReceivedTimestamp
        );

        return updated;
      });
    };

    room.on(
      RoomEvent.TranscriptionReceived,
      handleTranscription
    );

    return () => {
      room.off(
        RoomEvent.TranscriptionReceived,
        handleTranscription
      );
    };
  }, [room]);

  // Scroll ONLY the transcript box
  useEffect(() => {
    const box = transcriptBoxRef.current;

    if (!box) return;

    box.scrollTo({
      top: box.scrollHeight,
      behavior: "smooth",
    });
  }, [segments]);

  return (
    <div className="bg-white rounded-2xl shadow p-6 h-[420px]">

      <h2 className="text-xl font-bold mb-5">
        Conversation
      </h2>

      {/* ONLY THIS BOX SCROLLS */}
      <div
        ref={transcriptBoxRef}
        className="h-[320px] overflow-y-auto space-y-4 pr-2"
      >
        {segments.length === 0 ? (
          <div className="flex justify-center items-center h-full text-gray-400">
            Waiting for conversation...
          </div>
        ) : (
          segments.map((segment) => {
            const isUser =
              segment.participant?.identity ===
              room.localParticipant.identity;

            return (
              <div
                key={segment.id}
                className={`flex ${
                  isUser
                    ? "justify-end"
                    : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                    isUser
                      ? "bg-blue-600 text-white"
                      : "bg-gray-100 text-gray-800"
                  }`}
                >
                  <div className="text-xs font-semibold mb-1 opacity-70">
                    {isUser ? "You" : "Agent"}
                  </div>

                  <div className="text-sm">
                    {segment.text}
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>

    </div>
  );
}

export default TranscriptPanel;
