import ConnectionStatus from "./ConnectionStatus";
import CallTimer from "./CallTimer";

function CallHeader({ room }) {
  return (
    <header className="bg-white shadow px-8 py-5 flex justify-between items-center">

      <div>
        <h1 className="text-2xl font-bold text-gray-800">
          IT Help Desk Voice Agent
        </h1>

        <p className="text-gray-500 mt-1">
          Room: {room}
        </p>
      </div>

      <div className="flex items-center gap-8">
        <CallTimer />
        <ConnectionStatus />
      </div>

    </header>
  );
}

export default CallHeader;