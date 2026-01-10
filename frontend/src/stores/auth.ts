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
    role: (state) => {
      if (!state.user) return null;
      if (state.user.is_usuario_final) return "usuario_final";
      if (state.user.is_monitor) return "monitor";
      if (state.user.is_administrador) return "admin";
      return null;
    },
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
