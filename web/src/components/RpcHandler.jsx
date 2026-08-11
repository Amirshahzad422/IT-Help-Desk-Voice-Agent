import { useEffect } from "react";
import { useRoomContext } from "@livekit/components-react";
import { RoomEvent } from "livekit-client";
import { toast } from "react-hot-toast";

function RpcHandler() {
  const room = useRoomContext();

  useEffect(() => {
    if (!room) {
      console.log("RPC Handler: no room");
      return;
    }

    console.log("RPC Handler mounted");
    console.log("Current room state:", room.state);

    const handleShowNotification = async (data) => {
      console.log("====================================");
      console.log("RPC RECEIVED!");
      console.log("RPC data:", data);

      try {
        let payload;

        if (typeof data.payload === "string") {
          payload = data.payload;
        } else {
          payload = new TextDecoder().decode(data.payload);
        }

        console.log("RPC payload:", payload);

        const notification = JSON.parse(payload);

        console.log("RPC notification:", notification);

        if (notification.type === "success") {
          toast.success(
            notification.message ||
              "Your account has been successfully unlocked.",
            {
              id: "account-unblocked-toast",
              duration: 4000,
              position: "top-right",
            }
          );
        }
      } catch (error) {
        console.error("RPC processing error:", error);
      }
    };

    const registerRpc = async () => {
      try {
        console.log("====================================");
        console.log("REGISTERING RPC METHOD");
        console.log("Method: show_notification");

        await room.localParticipant.registerRpcMethod(
          "show_notification",
          handleShowNotification
        );

        console.log("====================================");
        console.log("RPC REGISTERED SUCCESSFULLY!");
        console.log("Method: show_notification");
        console.log("====================================");
      } catch (error) {
        console.error("RPC REGISTRATION FAILED:", error);
      }
    };

    if (room.state === "connected") {
      registerRpc();
    }

    const handleConnected = () => {
      console.log("RPC Handler detected LiveKit connected");
      registerRpc();
    };

    room.on(RoomEvent.Connected, handleConnected);

    return () => {
      console.log("RPC Handler cleanup");

      room.off(RoomEvent.Connected, handleConnected);

      try {
        room.localParticipant.unregisterRpcMethod(
          "show_notification"
        );
      } catch (error) {
        console.error("RPC unregister error:", error);
      }

      toast.dismiss("account-unblocked-toast");
    };
  }, [room]);

  return null;
}

export default RpcHandler;