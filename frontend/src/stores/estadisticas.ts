import { defineStore } from "pinia";
import { ref } from "vue";
import {getEstadisticas} from "../services/estadisticasService";

export const useEstadisticasStore = defineStore("estadisticas", () => {
  const data = ref({
    instalaciones: 0,
    actividades: 0,
    pabellones: 0,
    deportes: 0,
    usuarios: 0,
    tiposActividad: [],
    tiposInstalacion:[]
  });

  const cargarEstadisticas = async () => {
    const estadisticasBackend = await getEstadisticas();
    data.value = estadisticasBackend;
  };

  return { data, cargarEstadisticas };
});
