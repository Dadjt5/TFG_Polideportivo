import { defineStore } from "pinia";
import { getMe } from "../services/loginService";

export interface User {
  id: number;
  username: string;
  email: string;

  is_usuario_final: boolean;
  is_monitor: boolean;
  is_administrador: boolean;
  is_superuser: boolean;

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
    isSuperUser: (state) => state.user?.is_superuser,

    isUsuarioFinal: (state) => state.user?.is_usuario_final ?? false,
    isMonitor: (state) => state.user?.is_monitor ?? false,
    isAdmin: (state) => state.user?.is_administrador ?? false,

    adminRole: (state) => state.user?.rol ?? null,

    isAdminRaiz: (state) =>
      state.user?.is_administrador && state.user?.rol === "Administrador raiz",

    isAdminUsuarios: (state) =>
      state.user?.is_administrador && state.user?.rol === "Administrador de usuarios",

    isAdminEspacios: (state) =>
      state.user?.is_administrador && state.user?.rol === "Administrador de espacios",

    isAdminTarifas: (state) =>
      state.user?.is_administrador && state.user?.rol === "Administrador de tarifas",
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
