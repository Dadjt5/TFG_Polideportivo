import api from "./api";

/* Función para enviar un codigo de verificacion */
export const sendResetCode = async (email: any) => {
  const response = await api.post('api/v1/password_reset/', {"email": email, "tipo": "enviar"});
  return response.data;
};

/* Función para validar un codigo de verificacion */
export const verifyResetCode = async (email: any, codigo: any) => {
  const response = await api.post('api/v1/password_reset/', { "email": email, "codigo": codigo, "tipo": "verificar" });
  return response.data;
};
