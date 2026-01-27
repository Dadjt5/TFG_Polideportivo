import api from "./api";

/* Función para recuperar el monitor con todos sus campos */
export const getMonitor = async (id) => {
  const response = await api.get(`api/v1/monitores/${id}/`)
  return response.data
};

/* Función para obtener las sesiones semanales del monitor */
export const getSesionesSemanales = async (id) => {
  const response = await api.get(`api/v1/monitores/${id}/sesiones/`)
  return response.data
}


/* Función para guardar la asistencia de los usuarios */
export const guardarAsistencia = async (idAct, idSesion, participantes) => {
  const response = await api.post(`api/v1/actividades/${idAct}/sesiones/${idSesion}/asistencia/`, { participantes })
  return response.data
}

/* Función para cambiar ciertos campos del monitor */
export const modificarMonitor = async (id, data) => {
  const response = await api.patch(`api/v1/monitores/${id}/`, data)
  return response.data
}