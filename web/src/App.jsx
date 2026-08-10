import { useState } from "react";
import Home from "./pages/Home";
import NameModal from "./components/modal/NameModal";
import Room from "./pages/Room";
import { Toaster } from "react-hot-toast";

function App() {
  const [showModal, setShowModal] = useState(false);
  const [tokenData, setTokenData] = useState(null);
  const [userName, setUserName] = useState("");

  const handleConnected = (token, name) => {
    setTokenData(token);
    setUserName(name);
    setShowModal(false);
  };

  const handleLeave = () => {
    setTokenData(null);
    setUserName("");
    setShowModal(false);
  };

  return (
    <>
      {tokenData ? (
        <Room
          tokenData={tokenData}
          userName={userName}
          onLeave={handleLeave}
        />
      ) : (
        <>
          <Home onStart={() => setShowModal(true)} />

          <NameModal
            open={showModal}
            onClose={() => setShowModal(false)}
            onConnected={handleConnected}
          />
        </>
      )}

      {/* IMPORTANT: Toaster must ALWAYS exist */}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
        }}
      />
    </>
  );
}

export default App;