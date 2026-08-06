import { useState } from "react";
import { User, X } from "lucide-react";
import useToken from "../../hooks/useToken";
import toast from "react-hot-toast";

function NameModal({ open, onClose, onConnected }) {
  const [name, setName] = useState("");
  const { fetchToken, loading } = useToken();
  const handleContinue = async () => {
    try {
        const tokenData = await fetchToken();

        toast.success("Connected successfully!");

        onConnected(tokenData, name);

        // Next step:
        // We'll pass tokenData into the LiveKit room.
    } catch (err) {
        toast.error("Connection failed.");
    }
};

  if (!open) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex justify-center items-center z-50">

      <div className="bg-white w-[420px] rounded-3xl shadow-2xl p-8 relative">

        <button
          onClick={onClose}
          className="absolute right-5 top-5 text-gray-500 hover:text-black"
        >
          <X size={22}/>
        </button>

        <div className="flex justify-center mb-5">

          <div className="bg-blue-100 p-4 rounded-full">
            <User className="text-blue-600" size={34}/>
          </div>

        </div>

        <h2 className="text-3xl font-bold text-center">
          Welcome
        </h2>

        <p className="text-center text-gray-500 mt-2 mb-7">
          Enter your name to begin voice support.
        </p>

        <input
          type="text"
          placeholder="Your full name"
          value={name}
          onChange={(e)=>setName(e.target.value)}
          className="w-full border rounded-xl p-4 outline-none focus:ring-2 focus:ring-blue-500"
        />

        <button
        onClick={handleContinue}
        disabled={!name.trim() || loading}
          className="mt-6 w-full bg-blue-600 text-white py-4 rounded-xl hover:bg-blue-700 disabled:bg-gray-300"
        >
          {loading ? "Connecting..." : "Continue"}
        </button>

      </div>

    </div>
  );
}

export default NameModal;