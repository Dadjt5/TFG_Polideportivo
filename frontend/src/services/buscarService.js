import api from "./api";

/* Funcion para obtener el resultado de la busqueda desde el backend */
export const getBusqueda = async (params) => {
  const response = await api.get("buscar/", {
    params
  })
  return response.data
}
