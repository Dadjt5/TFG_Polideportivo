import { defineStore } from "pinia";
import {
  marcarFavoritos,
  getTDA,
  getUsuarioFinal,
} from "../services/usuarioFinalService";
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

export interface TDA {
  id: number;
  fechaInicio: string;
  fechaExpiracion: string;
  estado: string;
}

export const useUserStore = defineStore("user", {
  state: () => ({
    usuarioFinal: JSON.parse(localStorage.getItem("usuarioFinal") || "null"),
    tda: null as TDA | null,
    notificaciones: JSON.parse(localStorage.getItem("notificaciones") || "[]") as Notificacion[],
    favoritos: {
      actividades: JSON.parse(localStorage.getItem("actividadesFavoritas") || "[]") as number[],
      instalaciones: JSON.parse(localStorage.getItem("instalacionesFavoritas") || "[]") as number[],
    },
    cambiosPendientes: false,
    cambiosFavoritos: false,
  }),

  getters: {
    isLogged: (state) => !!state.usuarioFinal,
    hasTda: (s) => {
      if (!s.tda) return false;
      if (s.tda.estado != "Confirmada") return false;
      const hoy = new Date();
      const fechaExpiracion = new Date(s.tda.fechaExpiracion);
      return hoy <= fechaExpiracion;
    },
    isUAM: (s) => {
      return s.usuarioFinal.esUAM
    },
    hasAbono: (s) => {
      return s.usuarioFinal.tieneAbono;
    },
    edad: (state) => {
      const hoy = new Date()
      const nacimiento = new Date(state.usuarioFinal.fechaNacimiento)

      let edad = hoy.getFullYear() - nacimiento.getFullYear()

      const mes = hoy.getMonth() - nacimiento.getMonth()

      // Restamos si aun no ha cumplido años este año
      if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
        edad--
      }

      return edad
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
        localStorage.setItem("actividadesFavoritas", JSON.stringify(this.favoritos.actividades));
        localStorage.setItem("instalacionesFavoritas", JSON.stringify(this.favoritos.instalaciones));
        localStorage.setItem("usuarioFinal", JSON.stringify(data));
      } catch {
        this.cerrarSesion();
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
        localStorage.setItem("notificaciones", JSON.stringify(this.notificaciones));
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

    cerrarSesion() {
      this.usuarioFinal = null;
      this.notificaciones = [];
      localStorage.removeItem("usuarioFinal");
      localStorage.removeItem("notificaciones");
      localStorage.removeItem("actividadesFavoritas");
      localStorage.removeItem("instalacionesFavoritas");
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

      localStorage.setItem("instalacionesFavoritas", JSON.stringify(this.favoritos.instalaciones));
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

      localStorage.setItem("actividadesFavoritas", JSON.stringify(this.favoritos.actividades));
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
