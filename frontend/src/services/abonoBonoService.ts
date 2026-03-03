import api from "./api";

/* Función para obtener todos los abonos */
export const getAbonos = async () => {
  const response = await api.get('/api/v1/abonos/');
  return response.data;
};

/* Función para obtener todos los bonos */
export const getBonos = async () => {
  const response = await api.get('/api/v1/bonos/');
  return response.data;
};

/* Función para obtener todos los descuentos */
export const getDescuentos = async () => {
  const response = await api.get('/api/v1/descuentos/');
  return response.data;
};


/* Función para obtener los detalles del abono deportivo */
export const getAbonoDeportivoDetalle = async (id: number) => {
  const response = await api.get(`/api/v1/abonosDeportivos/${id}/`);
  return response.data;
};

/* Función para editar los campos indicados de un abono deportivo */
export const modificarAbonoDeportivo = async (id: number, data: any) => {
  const response = await api.patch(`api/v1/abonosDeportivos/${id}/`, data);
  return response.data;
};

/* Función para eliminar un abono deportivo */
export const eliminarAbonoDeportivo = async (id: number) => {
  const response = await api.delete(`api/v1/abonosDeportivos/${id}/`);
  return response.data;
};


/* Función para obtener los detalles del abono verano */
export const getAbonoVeranoDetalle = async (id: number) => {
  const response = await api.get(`/api/v1/abonosVerano/${id}/`);
  return response.data;
};

/* Función para editar los campos indicados de un abono verano */
export const modificarAbonoVerano = async (id: number, data: any) => {
  const response = await api.patch(`api/v1/abonosVerano/${id}/`, data);
  return response.data;
};

/* Función para eliminar un abono verano */
export const eliminarAbonoVerano = async (id: number) => {
  const response = await api.delete(`api/v1/abonosVerano/${id}/`);
  return response.data;
};


/* Función para obtener los detalles de un bono */
export const getBonoDetalle = async (id: number) => {
  const response = await api.get(`/api/v1/bonos/${id}/`);
  return response.data;
};

/* Función para editar los campos indicados de un bono */
export const modificarBono = async (id: number, data: any) => {
  const response = await api.patch(`api/v1/bonos/${id}/`, data);
  return response.data;
};

/* Función para eliminar un bono */
export const eliminarBono = async (id: number) => {
  const response = await api.delete(`api/v1/bonos/${id}/`);
  return response.data;
};