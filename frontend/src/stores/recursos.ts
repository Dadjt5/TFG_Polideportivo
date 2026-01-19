import { defineStore } from "pinia";
import { getActividadesInstalaciones } from "../services/detalleService";

export interface Actividad {
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

export interface Instalacion {
  id: number;
  nombre: string;
  imagenURL: string | null;
  descripcion: string;
  aforoMaximo: number;
  luz: boolean;
  porcentajeTDA: number;
  pabellon: number | null;
  tipoInstalacion: string;
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

      } catch (e) {
        console.warn("No se han podido cargar las actividades e instalaciones favoritas", e);
      }
    },
  },
});
