import { useEffect } from "react";
import { useRoomContext } from "@livekit/components-react";
import toast from "react-hot-toast";

function RpcHandler() {
  const room = useRoomContext();

  useEffect(() => {
    if (!room) {
      console.log("RPC Handler: room not available");
      return;
    }

    const registerHandler = () => {
      console.log("RPC Handler: room connected");
      console.log("Registering RPC method: show_notification");

      const handleNotification = async (request) => {
        try {
          console.log("RPC notification received:", request);

          let data;

          try {
            const payload =
              typeof request.payload === "string"
                ? request.payload
                : new TextDecoder().decode(request.payload);

            data = JSON.parse(payload);
          } catch {
            data = {
              type: "info",
              message: String(request.payload),
            };
          }

          console.log("RPC notification data:", data);

          const type = data.type || "info";
          const message =
            data.message || "Agent notification received.";

          switch (type) {
            case "success":
              toast.success(message);
              break;

            case "error":
              toast.error(message);
              break;

            case "warning":
              toast(message, {
                icon: "⚠️",
              });
              break;

            case "info":
            default:
              toast(message);
              break;
          }

          return JSON.stringify({
            success: true,
          });

        } catch (error) {
          console.error("RPC notification error:", error);

          return JSON.stringify({
            success: false,
          });
        }
      };

      room.localParticipant.registerRpcMethod(
        "show_notification",
        handleNotification
      );

      console.log(
        "RPC method registered successfully: show_notification"
      );
    };

    if (room.state === "connected") {
      registerHandler();
    } else {
      const handleConnected = () => {
        registerHandler();
      };

      room.on("connected", handleConnected);

      return () => {
        room.off("connected", handleConnected);

        try {
          room.localParticipant.unregisterRpcMethod(
            "show_notification"
          );
        } catch {
          // Already unregistered
        }
      };
    }

    return () => {
      try {
        room.localParticipant.unregisterRpcMethod(
          "show_notification"
        );
      } catch {
        // Already unregistered
      }
    };
  }, [room]);

  return null;
}

export default RpcHandler;