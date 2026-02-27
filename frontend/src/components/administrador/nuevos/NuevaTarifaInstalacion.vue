<template>
  <div class="min-vh-100 bg-light pb-5">
    <main class="container py-5">
      <h1 class="text-center fw-bold mb-5">
        {{ t.newFacilityTariff }}
      </h1>

      <div class="card shadow-sm border-0 rounded-4 p-4">
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
            <input
              type="number"
              step="0.01"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.precioAbonado }"
              v-model.number="tarifa.precioAbonado"
            />
          </div>

          <!-- PRECIO UAM -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.priceUAM }}</label>
            <input
              type="number"
              step="0.01"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.precioUAM }"
              v-model.number="tarifa.precioUAM"
            />
          </div>

          <!-- PRECIO TDA -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.priceTDA }}</label>
            <input
              type="number"
              step="0.01"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.precioTDA }"
              v-model.number="tarifa.precioTDA"
            />
          </div>

          <!-- PRECIO OTROS -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.priceOthers }}</label>
            <input
              type="number"
              step="0.01"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.precioOtros }"
              v-model.number="tarifa.precioOtros"
            />
          </div>

        </div>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-5">
          <button
            class="btn btn-primary btn-lg px-5"
            @click="crearTarifa"
          >
            {{ t.save }}
          </button>

          <button
            class="btn btn-danger btn-lg px-5"
            @click="volver"
          >
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

const tarifa = ref({
  titulo: '',
  precioAbonado: 0,
  precioUAM: 0,
  precioTDA: 0,
  precioOtros: 0
})

const errores = ref({
  titulo: false,
  precioAbonado: false,
  precioUAM: false,
  precioTDA: false,
  precioOtros: false
})

function validarFormulario() {
  let valido = true

  errores.value.titulo = tarifa.value.titulo === ''
  errores.value.precioAbonado = tarifa.value.precioAbonado < 0
  errores.value.precioUAM = tarifa.value.precioUAM < 0
  errores.value.precioTDA = tarifa.value.precioTDA < 0
  errores.value.precioOtros = tarifa.value.precioOtros < 0

  for (const key in errores.value) {
    if (errores.value[key]) valido = false
  }

  return valido
}

const crearTarifa = async () => {
  if (!validarFormulario()) return

  try {
    await nuevaTarifaInstalacion(tarifa.value)
    router.back()
  } catch (e) {
    console.log("Error al crear la tarifa para la instalacion", e)
  }
};

function volver() {
  router.back()
}
</script>
