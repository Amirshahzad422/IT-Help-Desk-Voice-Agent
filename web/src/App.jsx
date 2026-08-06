import { useState } from "react";
import Home from "./pages/Home";
import NameModal from "./components/modal/NameModal";
import Room from "./pages/Room";

function App() {
  const [showModal, setShowModal] = useState(false);
  const [tokenData, setTokenData] = useState(null);
  const [userName, setUserName] = useState("");

  if (tokenData) {
    return (
      <Room
        tokenData={tokenData}
        userName={userName}
      />
    );
  }

  return (
    <>
      <Home
        onStart={() => setShowModal(true)}
      />

      <NameModal
          open={showModal}
          onClose={() => setShowModal(false)}
          onConnected={(data, name) => {
              setShowModal(false);
              setUserName(name);
              setTokenData(data);
          }}
      />
    </>
  );
}

export default App;