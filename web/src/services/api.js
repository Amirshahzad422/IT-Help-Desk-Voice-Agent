import axios from "axios";

const api = axios.create({
  baseURL: "/api",
});

export const getToken = async () => {
  const response = await api.post("/token");
  return response.data;
};

export default api;