<template>
	<div class="min-vh-100 bg-light pb-5">
		<main class="container py-5">
			<h1 class="text-center fw-bold mb-5">
				{{ t.newReducedGroupRate }}
			</h1>

			<div class="card shadow-sm border-0 rounded-4 p-4">
				<div class="row g-4">

					<!-- Nº HORAS -->
					<div class="col-md-6">
						<label class="form-label fw-semibold">
							{{ t.numberOfHours }}
						</label>
						<input type="number" min="1" class="form-control form-control-lg"
							:class="{ 'is-invalid': errores.numeroHoras }" v-model.number="tarifa.numeroHoras" />
					</div>

					<!-- Nº PERSONAS -->
					<div class="col-md-6">
						<label class="form-label fw-semibold">
							{{ t.numberOfPeople }}
						</label>
						<input type="number" min="1" class="form-control form-control-lg"
							:class="{ 'is-invalid': errores.numeroPersonas }" v-model.number="tarifa.numeroPersonas" />
					</div>

					<!-- PRECIO BASE -->
					<div class="col-md-4">
						<label class="form-label fw-semibold">
							{{ t.basePrice }}
						</label>
						<input type="number" step="0.01" class="form-control form-control-lg"
							:class="{ 'is-invalid': errores.precio }" v-model.number="tarifa.precio" />
					</div>

					<!-- PRECIO CUATRIMESTRE -->
					<div class="col-md-4">
						<label class="form-label fw-semibold">
							{{ t.quarterPrice }}
						</label>
						<input type="number" step="0.01" class="form-control form-control-lg"
							:class="{ 'is-invalid': errores.precioCuatrimestre }" v-model.number="tarifa.precioCuatrimestre" />
					</div>

					<!-- PRECIO MENSUAL -->
					<div class="col-md-4">
						<label class="form-label fw-semibold">
							{{ t.monthlyPrice }}
						</label>
						<input type="number" step="0.01" class="form-control form-control-lg"
							:class="{ 'is-invalid': errores.precioMensual }" v-model.number="tarifa.precioMensual" />
					</div>

					<!-- POR DEFECTO -->
					<div class="col-12">
						<div class="form-check form-switch mt-3">
							<input class="form-check-input" type="checkbox" id="porDefecto" v-model="tarifa.por_defecto" />
							<label class="form-check-label fw-semibold" for="porDefecto">
								{{ t.defaultRate }}
							</label>
						</div>
					</div>
				</div>

				<p v-if="mensaje" class="text-center text-danger mt-4">
					{{ mensaje }}
				</p>

				<!-- BOTONES -->
				<div class="d-flex justify-content-center gap-3 mt-5">
					<button class="btn btn-primary btn-lg px-5" @click="crearTarifa">
						{{ t.save }}
					</button>

					<button class="btn btn-danger btn-lg px-5" @click="volver">
						{{ t.return }}
					</button>
				</div>
			</div>
		</main>
	</div>
</template>

<script setup lang="ts">
import { ref, inject, type Ref } from "vue"
import { useRouter } from "vue-router"

import { crearTarifaGrupoReducido } from "../services/tarifasService"

import type { Language } from "../useI18N"
import { useI18n } from "../useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const router = useRouter()
const mensaje = ref("")

const tarifa = ref({
	numeroHoras: 0,
	numeroPersonas: 0,
	precio: 0,
	precioCuatrimestre: 0,
	precioMensual: 0,
	por_defecto: false
})

const errores = ref({
	numeroHoras: false,
	numeroPersonas: false,
	precio: false,
	precioCuatrimestre: false,
	precioMensual: false
})

function validarFormulario() {
	let valido = true

	errores.value.numeroHoras = tarifa.value.numeroHoras <= 0
	errores.value.numeroPersonas = tarifa.value.numeroPersonas <= 0
	errores.value.precio = tarifa.value.precio < 0
	errores.value.precioCuatrimestre = tarifa.value.precioCuatrimestre < 0
	errores.value.precioMensual = tarifa.value.precioMensual < 0

	for (const key in errores.value) {
		if (errores.value[key]) valido = false
	}

	return valido
}

const crearTarifa = async () => {
	if (!validarFormulario()) return

	try {
		await crearTarifaGrupoReducido(tarifa.value)
		router.back()
	} catch (e) {
		console.log("Error al crear la tarifa para grupos reducidos", e)
	}

}

function volver() {
	router.back()
}
</script>
