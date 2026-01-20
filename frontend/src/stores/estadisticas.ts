import { defineStore } from "pinia";
import { ref } from "vue";
import { getEstadisticas } from "../services/estadisticasService";

export const useEstadisticasStore = defineStore("estadisticas", () => {
  const data = ref({
    instalaciones: 0,
    actividades: 0,
    pabellones: 0,
    deportes: 0,
    usuarios: 0,
    tiposActividad: JSON.parse(localStorage.getItem("tiposActividad") || "[]") as string[],
    tiposInstalacion: JSON.parse(localStorage.getItem("tiposInstalacion") || "[]") as string[],
  });

  const cargarEstadisticas = async () => {
    const estadisticasBackend = await getEstadisticas();

    data.value.instalaciones = estadisticasBackend.instalaciones;
    data.value.actividades = estadisticasBackend.actividades;
    data.value.pabellones = estadisticasBackend.pabellones;
    data.value.deportes = estadisticasBackend.deportes;
    data.value.usuarios = estadisticasBackend.usuarios;

    data.value.tiposActividad = estadisticasBackend.tiposActividad;
    data.value.tiposInstalacion = estadisticasBackend.tiposInstalacion;

    localStorage.setItem("tiposActividad", JSON.stringify(data.value.tiposActividad));
    localStorage.setItem("tiposInstalacion", JSON.stringify(data.value.tiposInstalacion));
  };

  return { data, cargarEstadisticas };
});
