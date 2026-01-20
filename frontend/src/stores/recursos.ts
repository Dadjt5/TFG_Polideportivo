import { defineStore } from "pinia";
import { getActividadesInstalaciones } from "../services/detalleService";

export interface Actividad {
  id: number
  nombre: string
  tipoActividad: string
  imagenURL: string
  plazasMaximas: number
  plazasReservadas: number
  edadMinima: number
  año: number
  numeroCreditos: number
  nivel: string
  material: string
  exterior: boolean
  tipoReserva: string
  terreno: string
  periodo: string
  estado: string
  horasSemanales: number
  nombreMonitor: string
  dias: string
}

export interface Instalacion {
  id: number
  nombre: string
  horaApertura: string
  horaCierre: string
  pabellon?: {
    nombre: string
    direccion: string
  }
}

export const useResourceStore = defineStore("recursos", {
  state: () => ({
    actividadesById: {} as Record<number, Actividad>,
    instalacionesById: {} as Record<number, Instalacion>,
  }),

  getters: {
    getActividad: (state) => {
      return (id: number) => state.actividadesById[id] ?? null;
    },
    getInstalacion: (state) => {
      return (id: number) => state.instalacionesById[id] ?? null;
    },
  },

  actions: {
    async fetchActividadesInstalaciones(
      actividadIds: number[],
      instalacionIds: number[]
    ) {
      try {
        if (!actividadIds.length && !instalacionIds.length) return;

        const response = await getActividadesInstalaciones({
          actividad_ids: actividadIds,
          instalacion_ids: instalacionIds,
        });

        response.actividades.forEach((act: Actividad) => {
          this.actividadesById[act.id] = act;
        });

        response.instalaciones.forEach((ins: Instalacion) => {
          this.instalacionesById[ins.id] = ins;
        });

        return {
          actividades: response.actividades,
          instalaciones: response.instalaciones
        };

      } catch (e) {
        console.warn("No se han podido cargar las actividades e instalaciones favoritas", e);
      }
    },
  },
});
