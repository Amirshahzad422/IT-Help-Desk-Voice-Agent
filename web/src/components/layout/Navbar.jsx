import { Headset } from "lucide-react";

function Navbar({ onStart }) {
  return (
    <nav className="w-full bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-xl text-white">
            <Headset size={22} />
          </div>

          <div>
            <h1 className="font-bold text-xl text-gray-800">
              IT Help Desk
            </h1>

            <p className="text-xs text-gray-500">
              AI Voice Assistant
            </p>
          </div>
        </div>

        <button
            onClick={onStart}
            className="bg-blue-600 hover:bg-blue-700 transition text-white px-5 py-2 rounded-xl"
        >
            Support
        </button>
      </div>
    </nav>
  );
}

export default Navbar;