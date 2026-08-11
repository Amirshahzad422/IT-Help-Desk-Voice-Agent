import { useState } from "react";
import { getToken } from "../services/api";

export default function useToken() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchToken = async (username) => {
    try {
      setLoading(true);
      setError("");

      const data = await getToken(username);

      return data;
    } catch (err) {
      setError("Unable to connect to support server.");
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    fetchToken,
    loading,
    error,
  };
}