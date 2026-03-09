import { defineStore } from "pinia";

import { getConfiguracion, editarConfiguracion } from "@/services/administradorService";

export const useConfiguracionStore = defineStore("configuracion", {
	state: () => ({
		id: 0,
		max_deportes_por_usuario: 0,
		dias_minimo_alquiler: 0,
		dias_maximo_alquiler: 0,
		dias_minimo_cancelacion: 0,
		horas_alquiler_consecutivas: 0,
		porcentaje_maximo: 0,
		titulo_cambios_cancelaciones: '',
		titulo_avisos_actividades: '',
		titulo_problemas_pago: '',
		titulo_salida_lista_espera: '',
		titulo_ausencias: '',
		titulo_material_especial: '',
		texto_cambios_cancelaciones: '',
		texto_avisos_actividades: '',
		texto_problemas_pago: '',
		texto_salida_lista_espera: '',
		texto_ausencias: '',
		texto_material_especial: '',
		modificado: false
	}),

	actions: {
		async obtenerConfiguracion() {
			try {
				const data = await getConfiguracion();

				this.id = data.id;
				this.max_deportes_por_usuario = data.max_deportes_por_usuario;
				this.dias_minimo_alquiler = data.dias_minimo_alquiler;
				this.dias_minimo_cancelacion = data.dias_minimo_cancelacion;
				this.porcentaje_maximo = data.porcentaje_maximo;
				this.dias_maximo_alquiler = data.dias_maximo_alquiler;
				this.horas_alquiler_consecutivas = data.horas_alquiler_consecutivas;

				this.titulo_cambios_cancelaciones = data.titulo_cambios_cancelaciones;
				this.titulo_avisos_actividades = data.titulo_avisos_actividades;
				this.titulo_problemas_pago = data.titulo_problemas_pago;
				this.titulo_salida_lista_espera = data.titulo_salida_lista_espera;
				this.titulo_ausencias = data.titulo_ausencias;
				this.titulo_material_especial = data.titulo_material_especial;

				this.texto_cambios_cancelaciones = data.texto_cambios_cancelaciones;
				this.texto_avisos_actividades = data.texto_avisos_actividades;
				this.texto_problemas_pago = data.texto_problemas_pago;
				this.texto_salida_lista_espera = data.texto_salida_lista_espera;
				this.texto_ausencias = data.texto_ausencias;
				this.texto_material_especial = data.texto_material_especial;

				this.guardarEnLocalStorage();

				this.modificado = true;
			} catch (e) {
				console.log("Error al obtener la configuración", e);
			}
		},

		async editarConfiguracion() {
			try {
				const payload = {
					max_deportes_por_usuario: this.max_deportes_por_usuario,
					dias_minimo_alquiler: this.dias_minimo_alquiler,
					dias_minimo_cancelacion: this.dias_minimo_cancelacion,
					porcentaje_maximo: this.porcentaje_maximo,
					dias_maximo_alquiler: this.dias_maximo_alquiler,
					horas_alquiler_consecutivas: this.horas_alquiler_consecutivas,
					titulo_cambios_cancelaciones: this.titulo_cambios_cancelaciones,
					titulo_avisos_actividades: this.titulo_avisos_actividades,
					titulo_problemas_pago: this.titulo_problemas_pago,
					titulo_salida_lista_espera: this.titulo_salida_lista_espera,
					titulo_ausencias: this.titulo_ausencias,
					titulo_material_especial: this.titulo_material_especial,
					texto_cambios_cancelaciones: this.texto_cambios_cancelaciones,
					texto_avisos_actividades: this.texto_avisos_actividades,
					texto_problemas_pago: this.texto_problemas_pago,
					texto_salida_lista_espera: this.texto_salida_lista_espera,
					texto_ausencias: this.texto_ausencias,
					texto_material_especial: this.texto_material_especial,
				};

				const data = await editarConfiguracion(payload);

				Object.assign(this, data);
				this.guardarEnLocalStorage();

				this.modificado = true;
				return true;
			} catch (e) {
				console.log("Error al editar la configuración", e);
				return false;
			}
		},

		guardarEnLocalStorage() {
			localStorage.setItem("configuracion", JSON.stringify({
				id: this.id,
				max_deportes_por_usuario: this.max_deportes_por_usuario,
				dias_minimo_alquiler: this.dias_minimo_alquiler,
				dias_minimo_cancelacion: this.dias_minimo_cancelacion,
				porcentaje_maximo: this.porcentaje_maximo,
				dias_maximo_alquiler: this.dias_maximo_alquiler,
				horas_alquiler_consecutivas: this.horas_alquiler_consecutivas,
				titulo_cambios_cancelaciones: this.titulo_cambios_cancelaciones,
				titulo_avisos_actividades: this.titulo_avisos_actividades,
				titulo_problemas_pago: this.titulo_problemas_pago,
				titulo_salida_lista_espera: this.titulo_salida_lista_espera,
				titulo_ausencias: this.titulo_ausencias,
				titulo_material_especial: this.titulo_material_especial,
				texto_cambios_cancelaciones: this.texto_cambios_cancelaciones,
				texto_avisos_actividades: this.texto_avisos_actividades,
				texto_problemas_pago: this.texto_problemas_pago,
				texto_salida_lista_espera: this.texto_salida_lista_espera,
				texto_ausencias: this.texto_ausencias,
				texto_material_especial: this.texto_material_especial,
			}));
		}
	}
});
