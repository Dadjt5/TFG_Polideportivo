<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #fff4e0, #e0f7ff);">
    <main class="container py-5" style="max-width: 1120px;">
      <h1 class="text-center fw-bold mb-5 text-primary">
        {{ t.newTDATariff }}
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

          <!-- PRECIO UAM -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">
              {{ t.priceUAM }}
            </label>
            <input type="number" step="0.01" class="form-control form-control-lg"
                   :class="{ 'is-invalid': errores.precioUAM }" v-model.number="tarifa.precioUAM" />
          </div>

          <!-- PRECIO OTROS -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">
              {{ t.priceOthers }}
            </label>
            <input type="number" step="0.01" class="form-control form-control-lg"
                   :class="{ 'is-invalid': errores.precioOtros }" v-model.number="tarifa.precioOtros" />
          </div>

          <!-- PRECIO REPOSICION -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">
              {{ t.repositionPrice }}
            </label>
            <input type="number" step="0.01" class="form-control form-control-lg"
                   :class="{ 'is-invalid': errores.precioReposicion }"
                   v-model.number="tarifa.precioReposicion" />
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

import { nuevaTarifaTDA } from "@/services/crearRecursosService"

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const router = useRouter()

const tarifa = ref({
	titulo: '',
	precioUAM: 0,
	precioOtros: 0,
	precioReposicion: 0
})

const errores = ref({
	titulo: false,
	precioUAM: false,
	precioOtros: false,
	precioReposicion: false
})

function validarFormulario() {
	let valido = true

	errores.value.titulo = tarifa.value.titulo === ''
	errores.value.precioUAM = tarifa.value.precioUAM < 0
	errores.value.precioOtros = tarifa.value.precioOtros < 0
	errores.value.precioReposicion = tarifa.value.precioReposicion < 0

	for (const key in errores.value) {
		if (errores.value[key as keyof typeof errores.value]) {
			valido = false
		}
	}

	return valido
}

const crearTarifa = async () => {
	if (!validarFormulario()) return

	try {
		await nuevaTarifaTDA(tarifa.value)
		router.back()
	} catch (e) {
		console.log("Error al crear la tarifa TDA", e)
	}
}

function volver() {
	router.back()
}
</script>
