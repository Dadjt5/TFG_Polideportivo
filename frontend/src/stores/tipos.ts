import { defineStore } from "pinia";

import { getTipos } from "../services/listadoService"; 

export const useTiposStore = defineStore("tipos", {
  state: () => ({
    tiposActividad: JSON.parse(localStorage.getItem("tiposActividad") || "[]") as string[],
    tiposInstalacion: JSON.parse(localStorage.getItem("tiposInstalacion") || "[]") as string[],
    tiposReserva: JSON.parse(localStorage.getItem("tiposReserva") || "[]") as string[],
    terrenos: JSON.parse(localStorage.getItem("terrenos") || "[]") as string[],
    estados: JSON.parse(localStorage.getItem("estados") || "[]") as string[],
    dias: JSON.parse(localStorage.getItem("dias") || "[]") as string[],
    periodos: JSON.parse(localStorage.getItem("periodos") || "[]") as string[],
		modificado: false
  }),

  actions: {
    async obtenerTipos() {
      try {
        const data = await getTipos();

        this.tiposInstalacion = data.tiposInstalacion;
        this.tiposActividad = data.tiposActividad;
				this.tiposReserva = data.tiposReserva;
				this.terrenos = data.terrenos;
				this.estados = data.estados;
        this.dias = data.dias;
        this.periodos = data.periodos;

				localStorage.setItem("tiposActividad", JSON.stringify(this.tiposActividad));
    		localStorage.setItem("tiposInstalacion", JSON.stringify(this.tiposInstalacion));
				localStorage.setItem("tiposReserva", JSON.stringify(this.tiposReserva));
				localStorage.setItem("terrenos", JSON.stringify(this.terrenos));
				localStorage.setItem("estados", JSON.stringify(this.estados));
        localStorage.setItem("dias", JSON.stringify(this.dias));
        localStorage.setItem("periodos", JSON.stringify(this.periodos));

				this.modificado = true
      } catch (e) {
        console.log("Error al obtener los tipos", e);
      }
    },
  },
});
