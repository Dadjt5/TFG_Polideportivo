import api from "./api";

/* Función para realizar el login y obtener el token JWT */
export const login = async (credentials: { username: string; password: string }) => {
  const response = await api.post("auth/jwt/create/",
    credentials
  );
  return response.data;
};

/* Función para obtener los datos del usuario registrado y logueado */
export const getMe = async () => {
  const response = await api.get("api/v1/me/");
  return response.data;
};

/* Función para realizar el registro, posteriormente se debe realizar el login */
export const registrarse = async (payload: any) => {
  const response = await api.post("api/v1/registrarse/", payload);
  return response.data;
};

/* Función para realizar el registro del monitor por parte del admin */
export const registrarMonitor = async (payload: any) => {
  const response = await api.post("api/v1/registrar/monitor/", payload);
  return response.data;
};

/* Función para realizar el registro del administrador por parte del admin encargado */
export const registrarAdministrador = async (payload: any) => {
  const response = await api.post("api/v1/registrar/administrador/", payload);
  return response.data;
};