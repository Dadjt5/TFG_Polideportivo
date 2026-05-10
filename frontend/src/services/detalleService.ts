import api from "./api";

/* Función para obtener la informacion de una actividad */
export const getActividadDetalle = async (id: number) => {
  const response = await api.get(`/api/v1/actividades/${id}/`);
  return response.data;
};

/* Función para editar los campos indicados de una actividad */
export const modificarActividad = async (id: number, payload: FormData): Promise<any> => {
  const response = await api.post(`/api/v1/actividades/${id}/editar/`, payload, {
    headers: { "Content-Type": "multipart/form-data" }
  })
  return response.data
}

/* Función para eliminar una actividad */
export const eliminarActividad = async (id: number) => {
  const response = await api.delete(`api/v1/actividades/${id}/`);
  return response.data;
};

/* Función para editar los campos indicados de un deporte */
export const modificarDeporte = async (id: number, data: any) => {
  const response = await api.patch(`api/v1/deportes/${id}/`, data);
  return response.data;
};

/* Función para eliminar un deporte */
export const eliminarDeporte = async (id: number) => {
  const response = await api.delete(`api/v1/deportes/${id}/`);
  return response.data;
};

/* Función para obtener la agenda de una instalacion sin la agenda*/
export const getInstalacionDetalleSinAgenda = async (id: number) => {
  const response = await api.get(`/api/v1/instalacionesSinAgenda/${id}/`);
  return response.data;
};

/* Función para obtener la informacion de una instalacion */
export const getInstalacionDetalle = async (id: number) => {
  const response = await api.get(`/api/v1/instalaciones/${id}/`);
  return response.data;
};

/* Función para obtener la agenda de una instalacion */
export const getAgendaInstalacion = async (id: number) => {
  const response = await api.get(`/api/v1/agendas/${id}/`);
  return response.data;
};

/* Función para editar instalación usando FormData */
export const modificarInstalacion = async (id: number, payload: FormData): Promise<any> => {
  const response = await api.post(`/api/v1/instalaciones/${id}/editar/`, payload, {
    headers: { "Content-Type": "multipart/form-data" }
  })
  return response.data
}

/* Función para eliminar una instalacion */
export const eliminarInstalacion = async (id: number) => {
  const response = await api.delete(`api/v1/instalaciones/${id}/`);
  return response.data;
};

/* Función para obtener los alquileres en una instalación un dia concreto */
export const getAlquileresPorDia = async (id: number, fecha: string) => {
  const response = await api.get(`api/v1/instalaciones/${id}/obtener/alquileres/`, {
    params: { fecha }
  });
  return response.data;
}


/* Función para obtener la informacion de un pabellon */
export const getPabellonDetalle = async (id: number) => {
  const response = await api.get(`/api/v1/pabellones/${id}/`);
  return response.data;
};

/* Función para editar los campos indicados de un pabellón */
export const modificarPabellon = async (id: number, payload: FormData): Promise<any> => {
  const response = await api.patch(`/api/v1/pabellones/${id}/`, payload, {
    headers: { "Content-Type": "multipart/form-data" }
  })
  return response.data
}

/* Función para eliminar un pabellón */
export const eliminarPabellon = async (id: number) => {
  const response = await api.delete(`api/v1/pabellones/${id}/`);
  return response.data;
};

/* Función para obtener la informacion de instalaciones y actividades indicadas */
export const getActividadesInstalaciones = async (payload: any) => {
  const response = await api.post('/api/v1/obtener/instalaciones/actividades/', payload);
  return response.data;
};

/* Función para obtener la informacion de instalaciones y actividades favoritas */
export const getActividadesInstalacionesFavoritas = async () => {
  const response = await api.post('/api/v1/obtener/favoritas/');
  return response.data;
};


/* Función para obtener la informacion de una sesión */
export const getSesionDetalle = async (idActividad: string, idSesion: string) => {
  const response = await api.get(`/api/v1/actividades/${idActividad}/sesiones/${idSesion}/`);
  return response.data;
};

/* Función para editar los campos indicados de una sesion */
export const modificarSesion = async (id: string, data: any) => {
  const response = await api.patch(`api/v1/sesiones/${id}/`, data);
  return response.data;
};

/* Función para eliminar una sesion */
export const eliminarSesion = async (id: string) => {
  const response = await api.delete(`api/v1/sesiones/${id}/`);
  return response.data;
};

/* Función para obtener la informacion de un descuento */
export const getDescuentoDetalle = async (id: number) => {
  const response = await api.get(`/api/v1/descuentos/${id}/`);
  return response.data;
};

/* Función para editar los campos indicados de un descuento */
export const modificarDescuento = async (id: string, data: any) => {
  const response = await api.patch(`api/v1/descuentos/${id}/`, data);
  return response.data
}

/* Función para eliminar un descuento */
export const eliminarDescuento = async (id: number) => {
  const response = await api.delete(`api/v1/descuentos/${id}/`);
  return response.data;
};
