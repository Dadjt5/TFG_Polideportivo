import api from "./api";
import qs from "qs";

/* Funcion para obtener el resultado de la busqueda desde el backend */
export const getBusqueda = async (params) => {
  const response = await api.get("api/v1/buscar/", {
    params,
    paramsSerializer: (params) => qs.stringify(params, { arrayFormat: 'repeat' })
  })
  return response.data
}