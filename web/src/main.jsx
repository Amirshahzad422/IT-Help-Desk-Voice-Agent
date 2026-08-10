import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Toaster } from "react-hot-toast";
import "@livekit/components-styles";

import App from "./App.jsx";
import "./index.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <>
      <Toaster position="top-right" />
      <App />
    </>
  </StrictMode>
);