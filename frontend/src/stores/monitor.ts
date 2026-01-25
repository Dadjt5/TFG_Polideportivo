import { defineStore } from "pinia";
import { getMonitor, getSesionesSemanales } from "../services/monitorService";
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
  actividad: number | null;
  instalacion: number | null;
  pabellon: number | null;
}

export interface Sesion {
  idActividad: number;
  idSesion: number;
  nombre: string;
  dia: string;
  horaInicio: string;
  horaFin: string;
}

export const useMonitorStore = defineStore("monitor", {
  state: () => ({
    monitor: JSON.parse(localStorage.getItem("monitor") || "null"),
    notificaciones: JSON.parse(localStorage.getItem("notificaciones_monitor") || "[]") as Notificacion[],
    sesiones: JSON.parse(localStorage.getItem("sesiones") || "[]") as Sesion[],
    cambiosPendientes: false,
  }),

  getters: {
    isLogged: (state) => !!state.monitor,
    unreadCount: (state) =>
      state.notificaciones.filter(n => !n.leido).length,
    sortedNotifications: (state) => [
      ...state.notificaciones.filter(n => n.fijado),
      ...state.notificaciones.filter(n => !n.fijado),
    ],
  },

  actions: {
    async fetchUser(id: number | undefined) {
      try {
        const data = await getMonitor(id);
        const sesiones = await getSesionesSemanales(id)
        this.monitor = data;
        localStorage.setItem("monitor", JSON.stringify(data));
        localStorage.setItem("sesiones", JSON.stringify(sesiones));
      } catch {
        this.cerrarSesion();
      }
    },

    async fetchNotificaciones() {
      try {
        this.notificaciones = await getNotificaciones();
        localStorage.setItem("notificaciones_monitor", JSON.stringify(this.notificaciones));
      } catch (e) {
        console.warn("No se pudieron cargar notificaciones");
      }
    },

    comenzarIntervalo() {
      if (intervalId) return;

      intervalId = setInterval(() => {
        if (this.monitor) {
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
      this.monitor = null;
      this.notificaciones = [];
      localStorage.removeItem("monitor");
      localStorage.removeItem("notificaciones_monitor");
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
