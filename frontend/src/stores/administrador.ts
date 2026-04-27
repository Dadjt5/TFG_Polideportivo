import { defineStore } from "pinia";
import { getAdministrador } from "../services/administradorService";
import {
  getNotificaciones,
  borrarNotificaciones,
  guardarNotificaciones
} from "../services/notificacionService";

let intervalId: number | null = null;

export interface Notificacion {
  id: number;
  titulo: string;
  descripcion: string;
  leido: boolean;
  fijado: boolean;
  fecha: string;
  hora: string;
  debeMarcar: boolean;
  actividad: {
    id: number;
    nombre: string;
  };
  instalacion: {
    id: number;
    nombre: string;
  };
  pabellon: {
    id: number;
    nombre: string;
  };
}

export interface Sesion {
  idActividad: number;
  idSesion: number;
  nombre: string;
  dia: string;
  horaInicio: string;
  horaFin: string;
}

export const useAdministradorStore = defineStore("administrador", {
  state: () => ({
    administrador: JSON.parse(localStorage.getItem("administrador") || "null"),
    notificaciones: JSON.parse(localStorage.getItem("notificaciones_administrador") || "[]") as Notificacion[],
    cambiosPendientes: false,
  }),

  getters: {
    isLogged: (state) => !!state.administrador,
    unreadCount: (state) =>
      state.notificaciones.filter(n => !n.leido).length,
    sortedNotifications: (state) => [
      ...state.notificaciones.filter(n => n.fijado && !n.leido),
      ...state.notificaciones.filter(n => n.fijado && n.leido),
      ...state.notificaciones.filter(n => !n.fijado && !n.leido),
      ...state.notificaciones.filter(n => !n.fijado && n.leido),
    ],
    sortedNotificationsHome: (state) => [
      ...state.notificaciones.filter(n => !n.leido),
      ...state.notificaciones.filter(n => n.leido),
    ],
  },

  actions: {
    async fetchUser(id: number | undefined) {
      try {
        if(id == null){
          return
        }
        const data = await getAdministrador(id);

        this.administrador = data;

        localStorage.setItem("administrador", JSON.stringify(data));
      } catch {
        this.cerrarSesion();
      }
    },

    async fetchNotificaciones() {
      try {
        this.notificaciones = await getNotificaciones();
        localStorage.setItem("notificaciones_administrador", JSON.stringify(this.notificaciones));
      } catch (e) {
        console.warn("No se pudieron cargar notificaciones");
      }
    },

    comenzarIntervalo() {
      if (intervalId) return;

      intervalId = setInterval(() => {
        if (this.administrador) {
          this.fetchNotificaciones();
        }
      }, 60 * 5000); // 5 minutos
    },

    finalizarIntervalo() {
      if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
      }
    },

    cerrarSesion() {
      this.administrador = null;
      this.notificaciones = [];
      localStorage.removeItem("administrador");
      localStorage.removeItem("notificaciones_administrador");
      this.finalizarIntervalo();
    },

    cambiarLeido(id: number) {
      const notif = this.notificaciones.find(n => n.id === id);
      if (notif) {
        notif.leido = !notif.leido;
        this.cambiosPendientes = true;
      }
    },

    cambiarFijado(id: number) {
      const notif = this.notificaciones.find(n => n.id === id);
      if (notif) {
        notif.fijado = !notif.fijado;
        this.cambiosPendientes = true;
      }
    },

    async deleteNotificacion(id: number) {
      this.notificaciones = this.notificaciones.filter(n => n.id !== id);
      await borrarNotificaciones(id);
    },

    async guardarCambios() {
      if (!this.cambiosPendientes) return;
      await guardarNotificaciones({
        notificaciones: this.notificaciones.map(n => ({
          id: n.id,
          leido: n.leido,
          fijado: n.fijado
        }))
      });
      this.cambiosPendientes = false;
    },
  },
});
