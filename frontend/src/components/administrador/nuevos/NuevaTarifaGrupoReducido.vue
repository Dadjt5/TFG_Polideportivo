<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #fff4e0, #e0f7ff);">
    <main class="container py-5" style="max-width: 1120px;">
      <h1 class="text-center fw-bold mb-5 text-primary">
        {{ t.newSmallGroupsTariff }}
      </h1>

      <div class="card shadow-lg border-0 rounded-4 p-4"
           style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">

        <div class="row g-4">

          <div class="col-12">
            <label class="form-label fw-semibold">
              {{ t.title }}
            </label>
            <input type="text" class="form-control form-control-lg"
                   :class="{ 'is-invalid': errores.titulo }" v-model="tarifa.titulo" />
          </div>

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
        </div>

        <div v-if="mostrarMensaje" class="text-center mb-3">
          <div class="alert" :class="tipoMensaje === 'success' ? 'alert-success' : 'alert-danger'">
            {{ mensajeEditar }}
          </div>
        </div>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-5">
          <button class="btn btn-primary btn-lg px-5 rounded-pill shadow-sm" @click="crearTarifa">
            {{ t.save }}
          </button>

          <button class="btn btn-outline-secondary btn-lg px-5 rounded-pill shadow-sm" @click="volver">
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

import { nuevaTarifaGrupoReducido } from "@/services/crearRecursosService"

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const router = useRouter()
const mensajeEditar = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensajeEditar.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true

  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
}

const tarifa = ref({
	titulo: '',
	numeroHoras: 0,
	numeroPersonas: 0,
	precio: 0,
	precioCuatrimestre: 0,
	precioMensual: 0
})

const errores = ref({
	titulo: false,
	numeroHoras: false,
	numeroPersonas: false,
	precio: false,
	precioCuatrimestre: false,
	precioMensual: false
})

function validarFormulario() {
	let valido = true

	errores.value.titulo = tarifa.value.titulo === ''
	errores.value.numeroHoras = tarifa.value.numeroHoras <= 0
	errores.value.numeroPersonas = tarifa.value.numeroPersonas <= 0
	errores.value.precio = tarifa.value.precio <= 0
	errores.value.precioCuatrimestre = tarifa.value.precioCuatrimestre <= 0
	errores.value.precioMensual = tarifa.value.precioMensual <= 0

	for (const key in errores.value) {
		if (errores.value[key]) valido = false
	}

	return valido
}

const crearTarifa = async () => {
	if (!validarFormulario()) {
    lanzarMensaje(t.value.missing, "error")
    return
  }

	try {
		await nuevaTarifaGrupoReducido(tarifa.value)
		router.back()
	} catch (e) {
    lanzarMensaje(t.value.tariffNoCreated, "error")
		console.log("Error al crear la tarifa para grupos reducidos", e)
	}
}

function volver() {
	router.back()
}
</script>
