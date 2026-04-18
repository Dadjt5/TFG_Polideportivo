import axios, { type AxiosError, type InternalAxiosRequestConfig } from "axios"
import { useAuthStore } from "../stores/auth"

/* Creamos instancia principal */
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL as string,
  timeout: 6000,
  headers: {
    "Content-Type": "application/json",
  },
})

const apiAuth = axios.create({
  baseURL: import.meta.env.VITE_API_URL as string,
})


/* REQUEST */

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem("access")

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  }
)

/* RESPONSE */

api.interceptors.response.use(
  response => response,
  async (error: AxiosError) => {
    const auth = useAuthStore()

    const originalRequest = error.config as InternalAxiosRequestConfig & {
      _retry?: boolean
    }

    if (
      error.response?.status === 401 &&
      auth.refresh &&
      !originalRequest._retry
    ) {
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

        localStorage.removeItem("access")
        localStorage.removeItem("refresh")

        window.location.href = "/login"

        return Promise.reject(err)
      }
    }

    return Promise.reject(error)
  }
)

export default api
