import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const getToken = async () => {
  const response = await api.post("/token");
  return response.data;
};

export default api;