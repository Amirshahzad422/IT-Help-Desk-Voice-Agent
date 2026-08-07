function AgentStatus({ connected }) {
  return (
    <div className="bg-white rounded-2xl shadow p-6">

      <h2 className="font-bold text-xl mb-4">
        AI Support Agent
      </h2>

      <div className="flex items-center gap-3">

        <span
          className={`w-3 h-3 rounded-full ${
            connected ? "bg-green-500" : "bg-yellow-500"
          }`}
        />

        <span className="font-semibold">
          {connected ? "Agent Connected" : "Waiting for Agent..."}
        </span>

      </div>

      <p className="text-gray-500 mt-4">
        {connected
          ? "Voice assistant is ready."
          : "Waiting for AI voice assistant to join the room."}
      </p>

    </div>
  );
}

export default AgentStatus;