import { defineStore } from "pinia";
import {
  marcarFavoritos,
  getTDA,
  getUsuarioFinal,
  getNotificaciones,
  borrarNotificaciones,
  guardarNotificaciones
} from "../services/usuarioFinalService";

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

export interface TDA {
  id: number;
  fechaInicio: string;
  fechaExpiracion: string;
}

export const useUserStore = defineStore("user", {
  state: () => ({
    usuarioFinal: JSON.parse(localStorage.getItem("usuarioFinal") || "null"),
    tda: null as TDA | null,
    notificaciones: [] as Notificacion[],
    favoritos: {
      actividades: [] as number[],
      instalaciones: [] as number[],
    },
    cambiosPendientes: false,
    cambiosFavoritos: false,
  }),

  getters: {
    isLogged: (state) => !!state.usuarioFinal,
    hasTda: (s) => {
      if (!s.tda) return false;
      const hoy = new Date();
      const fechaExpiracion = new Date(s.tda.fechaExpiracion);
      return hoy <= fechaExpiracion;
    },
    unreadCount: (state) =>
      state.notificaciones.filter(n => !n.leido).length,
    sortedNotifications: (state) => [
      ...state.notificaciones.filter(n => n.fijado),
      ...state.notificaciones.filter(n => !n.fijado),
    ],
    activityIsFavorite: (state) => (id: number) => {
      return state.favoritos.actividades.includes(id);
    },
    facilityIsFavorite: (state) => (id: number) => {
      return state.favoritos.instalaciones.includes(id);
    },
  },

  actions: {
    async fetchUser(id: number | undefined) {
      try {
        const data = await getUsuarioFinal(id);
        this.usuarioFinal = data;
        this.favoritos.actividades = data.actividades_favoritas ?? [];
        this.favoritos.instalaciones = data.instalaciones_favoritas ?? [];
        localStorage.setItem("usuarioFinal", JSON.stringify(data));
      } catch {
        this.clear();
      }
    },

    async fetchTDA() {
      try {
        const tdas = await getTDA();
        this.tda = tdas[0]
      } catch (e) {
        console.warn("No se pudo cargar la tarjeta deportiva anual", e);
      }
    },

    async fetchNotificaciones() {
      try {
        this.notificaciones = await getNotificaciones();
      } catch (e) {
        console.warn("No se pudieron cargar notificaciones");
      }
    },

    comenzarIntervalo() {
      if (intervalId) return;

      intervalId = setInterval(() => {
        if (this.usuarioFinal) {
          this.fetchNotificaciones();
          this.sincronizarFavoritos();
        }
      }, 60 * 5000); // 5 minutos
    },

    finalizarIntervalo() {
      if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
      }
    },

    clear() {
      this.usuarioFinal = null;
      this.notificaciones = [];
      localStorage.removeItem("usuarioFinal");
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

    marcarInstalacionFavorita(id: number) {
      if (this.favoritos.instalaciones.includes(id)) {
        this.favoritos.instalaciones = this.favoritos.instalaciones.filter(
          favoritoId => favoritoId !== id
        );
      } else {
        this.favoritos.instalaciones.push(id);
      }
      this.cambiosFavoritos = true;
    },

    marcarActividadFavorita(id: number) {
      if (this.favoritos.actividades.includes(id)) {
        this.favoritos.actividades = this.favoritos.actividades.filter(
          favoritoId => favoritoId !== id
        );
      } else {
        this.favoritos.actividades.push(id);
      }
      this.cambiosFavoritos = true;
    },


    async sincronizarFavoritos() {
      if (!this.cambiosFavoritos) return;

      try {
        await marcarFavoritos({
          actividad_ids: this.favoritos.actividades,
          instalacion_ids: this.favoritos.instalaciones,
        })

        this.cambiosFavoritos = false;
      } catch (e) {
        console.warn("No se han sincronizado las actividades favoritas", e);
      }
    },
  },
});
