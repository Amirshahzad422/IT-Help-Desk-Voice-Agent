import { useState } from "react";
import Home from "./pages/Home";
import NameModal from "./components/modal/NameModal";
import Room from "./pages/Room";

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

  if (tokenData) {
    return (
      <Room
        tokenData={tokenData}
        userName={userName}
        onLeave={handleLeave}
      />
    );
  }

  return (
    <>
      <Home onStart={() => setShowModal(true)} />

      <NameModal
        open={showModal}
        onClose={() => setShowModal(false)}
        onConnected={handleConnected}
      />
    </>
  );
}

export default App;