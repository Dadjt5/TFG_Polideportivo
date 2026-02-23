<template>
  <div class="min-vh-100 bg-light pb-5">
    <main class="container py-5">
      <h1 class="text-center fw-bold mb-5">
        {{ t.newSummerSubscription }}
      </h1>

      <div class="card shadow-sm border-0 rounded-4 p-4">
        <div class="row g-4">

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.name }}</label>
            <input class="form-control form-control-lg"
              v-model="abono.nombre" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.priceTDA }}</label>
            <input type="number" step="0.01"
              class="form-control form-control-lg"
              v-model.number="abono.precioTDA" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.priceUAM }}</label>
            <input type="number" step="0.01"
              class="form-control form-control-lg"
              v-model.number="abono.precioUAM" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.priceOthers }}</label>
            <input type="number" step="0.01"
              class="form-control form-control-lg"
              v-model.number="abono.precioOtros" />
          </div>

        </div>

        <div class="d-flex justify-content-center gap-3 mt-5">
          <button class="btn btn-primary btn-lg px-5"
            @click="crear">
            {{ t.createSummerSubscription }}
          </button>

          <button class="btn btn-danger btn-lg px-5"
            @click="volver">
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
  nombre: false
})

function validar() {
  errores.value.nombre = abono.value.nombre.trim() === ""
  return !errores.value.nombre
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