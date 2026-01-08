import axios from "axios";
import { useAuthStore } from "../stores/auth";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 6000,
  headers: {
    "Content-Type": "application/json",
  },
});

/* Direccion sin nada mas en la cabecera y sin timeout */
const apiAuth = axios.create({
  baseURL: import.meta.env.VITE_API_URL
});

/* Interceptor que se ejecuta en cada request solo cuando exista el token */
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  response => response,
  async error => {
    const auth = useAuthStore()
    const originalRequest = error.config

    if (error.response?.status === 401 && auth.refresh && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const res = await apiAuth.post("/auth/jwt/refresh/", {
          refresh: auth.refresh,
        })

        auth.setAccess(res.data.access)

        originalRequest.headers.Authorization = `Bearer ${res.data.access}`

        return api(originalRequest)
      } catch (err) {
        auth.logout()
        return Promise.reject(err)
      }
    }

    return Promise.reject(error)
  }
)

export default api;