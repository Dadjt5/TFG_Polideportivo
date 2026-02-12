import api from "./api";

/* Función para obtener la informacion de una tarifa de una instalacion */
export const getTarifaInstalacionDetalle = async (id: number) => {
  const response = await api.get(`/api/v1/tarifasInstalacion/${id}/`);
  return response.data;
};

/* Función para editar los campos indicados de una tarifa de una instalación */
export const modificarTarifaInstalacion = async (id: number, data: any) => {
  const response = await api.patch(`api/v1/tarifasInstalacion/${id}/`, data);
  return response.data;
};

/* Función para eliminar una tarifa de una instalación */
export const eliminarTarifaInstalacion = async (id: number) => {
  const response = await api.delete(`api/v1/tarifasInstalacion/${id}/`);
  return response.data;
};


/* Función para obtener la informacion de una tarifa de la TDA */
export const getTarifaTDADetalle = async (id: number) => {
  const response = await api.get(`/api/v1/tarifasTDA/${id}/`);
  return response.data;
};

/* Función para editar los campos indicados de una tarifa de la TDA */
export const modificarTarifaTDA = async (id: number, data: any) => {
  const response = await api.patch(`api/v1/tarifasTDA/${id}/`, data);
  return response.data;
};

/* Función para eliminar una tarifa de la TDA */
export const eliminarTarifaTDA = async (id: number) => {
  const response = await api.delete(`api/v1/tarifasTDA/${id}/`);
  return response.data;
};


/* Función para obtener la informacion de una tarifa de una actividad comun */
export const getTarifaActividadComunDetalle = async (id: number) => {
  const response = await api.get(`/api/v1/actividadesComunes/${id}/`);
  return response.data;
};

/* Función para editar los campos indicados de una tarifa de una actividad comun */
export const modificarTarifaActividadComun = async (id: number, data: any) => {
  const response = await api.patch(`api/v1/actividadesComunes/${id}/`, data);
  return response.data;
};

/* Función para eliminar una tarifa de una actividad comun */
export const eliminarTarifaActividadComun = async (id: number) => {
  const response = await api.delete(`api/v1/actividadesComunes/${id}/`);
  return response.data;
};


/* Función para obtener la informacion de una tarifa de un grupo reducido */
export const getTarifaGrupoReducidoDetalle = async (id: number) => {
  const response = await api.get(`/api/v1/gruposReducidos/${id}/`);
  return response.data;
};

/* Función para editar los campos indicados de una tarifa de un grupo reducido */
export const modificarTarifaGrupoReducido = async (id: number, data: any) => {
  const response = await api.patch(`api/v1/gruposReducidos/${id}/`, data);
  return response.data;
};

/* Función para eliminar una tarifa de un grupo reducido */
export const eliminarTarifaGrupoReducido = async (id: number) => {
  const response = await api.delete(`api/v1/gruposReducidos/${id}/`);
  return response.data;
};


/* Función para obtener la informacion de una tarifa de fisioterapia */
export const getTarifaFisioterapiaDetalle = async (id: number) => {
  const response = await api.get(`/api/v1/fisioterapias/${id}/`);
  return response.data;
};

/* Función para editar los campos indicados de una tarifa de fisioterapia */
export const modificarTarifaFisioterapia = async (id: number, data: any) => {
  const response = await api.patch(`api/v1/fisioterapias/${id}/`, data);
  return response.data;
};

/* Función para eliminar una tarifa de fisioterapia */
export const eliminarTarifaFisioterapia = async (id: number) => {
  const response = await api.delete(`api/v1/fisioterapias/${id}/`);
  return response.data;
};