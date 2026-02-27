import { defineStore } from "pinia";
import { getMe } from "../services/loginService";

export interface User {
  id: number;
  username: string;
  email: string;

  is_usuario_final: boolean;
  is_monitor: boolean;
  is_administrador: boolean;

  usuario_final_id: number,
  monitor_id: number,
  administrador_id: number

  rol?: string | null;
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null as User | null,
    access: localStorage.getItem("access"),
    refresh: localStorage.getItem("refresh"),
    loading: false,
  }),

  getters: {
    isAuthenticated: (state) => !!state.access,

    isUsuarioFinal: (state) => state.user?.is_usuario_final ?? false,
    isMonitor: (state) => state.user?.is_monitor ?? false,
    isAdmin: (state) => state.user?.is_administrador ?? false,

    adminRole: (state) => state.user?.rol ?? null,

    isAdminRaiz: (state) =>
      state.user?.is_administrador && state.user?.rol === "RAIZ",

    isAdminUsuarios: (state) =>
      state.user?.is_administrador && state.user?.rol === "USUARIOS",

    isAdminEspacios: (state) =>
      state.user?.is_administrador && state.user?.rol === "ESPACIOS",

    isAdminTarifas: (state) =>
      state.user?.is_administrador && state.user?.rol === "TARIFAS",
  },

  actions: {
    async fetchUser() {
      if (!this.access) return;

      this.user = await getMe();
    },

    setAccess(token: string) {
      this.access = token
      localStorage.setItem('access', token)
    },

    logout() {
      this.user = null;
      this.access = null;
      this.refresh = null;
      localStorage.clear();
    },
  },
});
