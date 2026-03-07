import api from "./api";

/* Función para mandar una nueva contraseña */
export const resetPassword = async (email: string) => {
  const response = await api.post("/api/v1/password_reset/", { email });
  return response.data;
};

/* Función para resetear una contraseña */
export const confirmacionResetPassword = async (token: any, password: string) => {
  const response = await api.post('/api/password_reset/confirm/', { token, password });
  return response.data;
};