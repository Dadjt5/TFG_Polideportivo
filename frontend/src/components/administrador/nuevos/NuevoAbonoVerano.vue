<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #fff4e0, #e0f7ff);">
    <main class="container py-5" style="max-width: 1120px;">
      <h1 class="text-center fw-bold mb-5 text-primary">
        {{ t.newSummerSubscription }}
      </h1>

      <div class="card shadow-lg border-0 rounded-4 p-4"
           style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">

        <div class="row g-4">

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.name }}</label>
            <input class="form-control form-control-lg" v-model="abono.nombre" :class="{ 'is-invalid': errores.nombre }" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.priceTDA }}</label>
            <input type="number" step="0.01" class="form-control form-control-lg" v-model.number="abono.precioTDA" :class="{ 'is-invalid': errores.precioTDA }" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.priceUAM }}</label>
            <input type="number" step="0.01" class="form-control form-control-lg" v-model.number="abono.precioUAM" :class="{ 'is-invalid': errores.precioUAM }"/>
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.priceOthers }}</label>
            <input type="number" step="0.01" class="form-control form-control-lg" v-model.number="abono.precioOtros" :class="{ 'is-invalid': errores.precioOtros }"/>
          </div>

        </div>

        <div class="d-flex justify-content-center gap-3 mt-5">
          <button class="btn btn-primary btn-lg px-5 rounded-pill shadow-sm" @click="crear">
            {{ t.createSummerSubscription }}
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
import { type Ref, ref, inject } from "vue"
import { useRouter } from "vue-router"

import { nuevoAbonoVerano } from "@/services/crearRecursosService"

import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter()

const abono = ref({
  nombre: "",
  precioTDA: 0,
  precioUAM: 0,
  precioOtros: 0
})

const errores = ref({
  nombre: false,
  precioTDA: false,
  precioUAM: false,
  precioOtros: false,
})

function validar() {
  let valido = true

  errores.value.nombre = abono.value.nombre.trim() === ""
  errores.value.precioTDA = abono.value.precioTDA <= 0
  errores.value.precioUAM = abono.value.precioUAM <= 0
  errores.value.precioOtros = abono.value.precioOtros <= 0

	for (const key in errores.value) {
		if (errores.value[key]) valido = false
	}

	return valido
}

const crear = async () => {
  if (!validar()) return

  try {
    await nuevoAbonoVerano(abono.value)
    router.back()
  } catch (error) {
    console.error("Error creando abono de verano:", error)
  }
}

const volver = () => {
  router.back()
}
</script>