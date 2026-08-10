import axios from "axios";

const api = axios.create({
  baseURL: "/api",
});

export const getToken = async (username) => {
  const response = await api.post("/token", {
    username: username.trim(),
  });

  return response.data;
};

export default api;