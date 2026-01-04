import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 6000,
  headers: {
    "Content-Type": "application/json",
  },
});

/* Interceptor que se ejecuta en cada request solo cuando exista el token */
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;