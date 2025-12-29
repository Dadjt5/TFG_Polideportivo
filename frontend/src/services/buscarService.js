import api from "./api";

/* Funcion para obtener el resultado de la busqueda desde el backend */
export const getBusqueda = async () => {
  const response = await api.get("buscar/");
  return response.data;
};
