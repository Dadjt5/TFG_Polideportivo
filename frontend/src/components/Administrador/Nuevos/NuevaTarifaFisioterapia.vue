<template>
  <div class="min-vh-100 bg-light pb-5">
    <main class="container py-5">
      <h1 class="text-center fw-bold mb-5">
        {{ t.newPhysiotherapyTariff }}
      </h1>

      <div class="card shadow-sm border-0 rounded-4 p-4">
        <div class="row g-4">

          <!-- CONSULTA -->
          <h5 class="fw-semibold mt-3">{{ t.consultationPrice }}</h5>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.priceTDA }}</label>
            <input
              type="number"
              step="0.01"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.precioConsultaTDA }"
              v-model.number="tarifa.precioConsultaTDA"
            />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.priceUAM }}</label>
            <input
              type="number"
              step="0.01"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.precioConsultaUAM }"
              v-model.number="tarifa.precioConsultaUAM"
            />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.priceOthers }}</label>
            <input
              type="number"
              step="0.01"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.precioConsultaOtros }"
              v-model.number="tarifa.precioConsultaOtros"
            />
          </div>

          <!-- SESIONES 1-5 -->
          <h5 class="fw-semibold mt-4">{{ t.sessions1to5 }}</h5>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.priceTDA }}</label>
            <input
              type="number"
              step="0.01"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.precioSesiones1_5TDA }"
              v-model.number="tarifa.precioSesiones1_5TDA"
            />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.priceUAM }}</label>
            <input
              type="number"
              step="0.01"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.precioSesiones1_5UAM }"
              v-model.number="tarifa.precioSesiones1_5UAM"
            />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.priceOthers }}</label>
            <input
              type="number"
              step="0.01"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.precioSesiones1_5Otros }"
              v-model.number="tarifa.precioSesiones1_5Otros"
            />
          </div>

          <!-- SESIONES 6+ -->
          <h5 class="fw-semibold mt-4">{{ t.sessions6plus }}</h5>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.priceTDA }}</label>
            <input
              type="number"
              step="0.01"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.precioSesiones6TDA }"
              v-model.number="tarifa.precioSesiones6TDA"
            />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.priceUAM }}</label>
            <input
              type="number"
              step="0.01"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.precioSesiones6UAM }"
              v-model.number="tarifa.precioSesiones6UAM"
            />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.priceOthers }}</label>
            <input
              type="number"
              step="0.01"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.precioSesiones6Otros }"
              v-model.number="tarifa.precioSesiones6Otros"
            />
          </div>

          <!-- POR DEFECTO -->
          <div class="col-12">
            <div class="form-check form-switch mt-3">
              <input
                class="form-check-input"
                type="checkbox"
                id="porDefecto"
                v-model="tarifa.por_defecto"
              />
              <label class="form-check-label fw-semibold" for="porDefecto">
                {{ t.defaultTariff }}
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

import { nuevaTarifaFisioterapia } from "@/services/crearRecursosService"

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const router = useRouter()
const mensaje = ref("")

const tarifa = ref({
  precioConsultaTDA: 0,
  precioConsultaUAM: 0,
  precioConsultaOtros: 0,
  precioSesiones1_5TDA: 0,
  precioSesiones1_5UAM: 0,
  precioSesiones1_5Otros: 0,
  precioSesiones6TDA: 0,
  precioSesiones6UAM: 0,
  precioSesiones6Otros: 0,
  por_defecto: false
})

const errores = ref({
  precioConsultaTDA: false,
  precioConsultaUAM: false,
  precioConsultaOtros: false,
  precioSesiones1_5TDA: false,
  precioSesiones1_5UAM: false,
  precioSesiones1_5Otros: false,
  precioSesiones6TDA: false,
  precioSesiones6UAM: false,
  precioSesiones6Otros: false
})

function validarFormulario() {
  let valido = true

  for (const key in errores.value) {
    errores.value[key] = tarifa.value[key] < 0
    if (errores.value[key]) valido = false
  }

  return valido
}

const crearTarifa = async () => {
  if (!validarFormulario()) return

  try {
    await nuevaTarifaFisioterapia(tarifa.value)
    router.back()
  } catch (e) {
    console.log("Error al crear la tarifa para fisioterapia", e)
  }
}

function volver() {
  router.back()
}
</script>
