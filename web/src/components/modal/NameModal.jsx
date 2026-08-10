import { useState } from "react";
import { User, X } from "lucide-react";
import useToken from "../../hooks/useToken";
import toast from "react-hot-toast";

function NameModal({
  open,
  onClose,
  onConnected,
}) {
  const [username, setUsername] = useState("");
  const { fetchToken, loading } = useToken();

  const handleContinue = async () => {
    const normalizedUsername = username.trim().toLowerCase();

    if (!normalizedUsername) {
      toast.error("Please enter your username.");
      return;
    }

    try {
      const tokenData = await fetchToken(normalizedUsername);

      onConnected(tokenData, normalizedUsername);
    } catch (err) {
      console.error("Token request failed:", err);

      const message =
        err?.response?.data?.detail ||
        "Unable to connect to support server.";

      toast.error(message);
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
          <X size={22} />
        </button>

        <div className="flex justify-center mb-5">
          <div className="bg-blue-100 p-4 rounded-full">
            <User className="text-blue-600" size={34} />
          </div>
        </div>

        <h2 className="text-3xl font-bold text-center">
          Welcome
        </h2>

        <p className="text-center text-gray-500 mt-2 mb-7">
          Enter your username to begin voice support.
        </p>

        <input
          type="text"
          placeholder="Your username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && username.trim() && !loading) {
              handleContinue();
            }
          }}
          className="w-full border rounded-xl p-4 outline-none focus:ring-2 focus:ring-blue-500"
        />

        <button
          onClick={handleContinue}
          disabled={!username.trim() || loading}
          className="mt-6 w-full bg-blue-600 text-white py-4 rounded-xl hover:bg-blue-700 disabled:bg-gray-300"
        >
          {loading ? "Connecting..." : "Continue"}
        </button>

      </div>

    </div>
  );
}

export default NameModal;