import { useState } from "react";
import { getToken } from "../services/api";

export default function useToken() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchToken = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getToken();

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