import { useConnectionState } from "@livekit/components-react";
import { ConnectionState } from "livekit-client";

function ConnectionStatus() {
  const state = useConnectionState();

  let color = "bg-gray-500";
  let text = "Unknown";

  switch (state) {
    case ConnectionState.Connecting:
      color = "bg-yellow-500";
      text = "Connecting...";
      break;

    case ConnectionState.Connected:
      color = "bg-green-500";
      text = "Connected";
      break;

    case ConnectionState.Reconnecting:
      color = "bg-orange-500";
      text = "Reconnecting...";
      break;

    case ConnectionState.Disconnected:
      color = "bg-red-500";
      text = "Disconnected";
      break;

    default:
      break;
  }

  return (
    <div className="flex items-center gap-3">
      <span className={`w-3 h-3 rounded-full ${color}`}></span>
      <span className="font-semibold">{text}</span>
    </div>
  );
}

export default ConnectionStatus;