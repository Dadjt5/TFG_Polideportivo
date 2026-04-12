<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #fff4e0, #e0f7ff);">
    <main class="container py-5" style="max-width: 1120px;">
      <h1 class="text-center fw-bold mb-5 text-primary">
        {{ t.newFacilityTariff }}
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

          <!-- PRECIO ABONADO -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.priceSubscripcion }}</label>
            <input type="number" step="0.01" class="form-control form-control-lg"
                   :class="{ 'is-invalid': errores.precioAbonado }" v-model.number="tarifa.precioAbonado" />
          </div>

          <!-- PRECIO UAM -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.priceUAM }}</label>
            <input type="number" step="0.01" class="form-control form-control-lg"
                   :class="{ 'is-invalid': errores.precioUAM }" v-model.number="tarifa.precioUAM" />
          </div>

          <!-- PRECIO TDA -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.priceTDA }}</label>
            <input type="number" step="0.01" class="form-control form-control-lg"
                   :class="{ 'is-invalid': errores.precioTDA }" v-model.number="tarifa.precioTDA" />
          </div>

          <!-- PRECIO OTROS -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.priceOthers }}</label>
            <input type="number" step="0.01" class="form-control form-control-lg"
                   :class="{ 'is-invalid': errores.precioOtros }" v-model.number="tarifa.precioOtros" />
          </div>

          <!-- COSTE ILUMINACION -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.lightCost }}</label>
            <input type="number" step="0.01" class="form-control form-control-lg"
                   :class="{ 'is-invalid': errores.costeIluminacion }" v-model.number="tarifa.costeIluminacion" />
          </div>
        </div>

        <div v-if="mostrarMensaje" class="text-center mb-3 mt-3">
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

import { nuevaTarifaInstalacion } from "@/services/crearRecursosService"

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const router = useRouter()

const mensajeEditar = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)

const tarifa = ref({
  titulo: '',
  precioAbonado: 0,
  precioUAM: 0,
  precioTDA: 0,
  precioOtros: 0,
  costeIluminacion: 0
})

const errores = ref({
  titulo: false,
  precioAbonado: false,
  precioUAM: false,
  precioTDA: false,
  precioOtros: false,
  costeIluminacion: false
})

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensajeEditar.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true

  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
}

function validarFormulario() {
  let valido = true

  errores.value.titulo = tarifa.value.titulo === ''
  errores.value.precioAbonado = tarifa.value.precioAbonado <= 0
  errores.value.precioUAM = tarifa.value.precioUAM <= 0
  errores.value.precioTDA = tarifa.value.precioTDA <= 0
  errores.value.precioOtros = tarifa.value.precioOtros <= 0
  errores.value.costeIluminacion = tarifa.value.costeIluminacion <= 0

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
    await nuevaTarifaInstalacion(tarifa.value)
    router.back()
  } catch (e) {
    lanzarMensaje(t.value.tariffNoCreated, "error")
    console.log("Error al crear la tarifa para la instalacion", e)
  }
};

function volver() {
  router.back()
}
</script>
