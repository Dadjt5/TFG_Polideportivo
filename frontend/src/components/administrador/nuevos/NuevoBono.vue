<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #e0f7ff, #ffffff);">
    <main class="container py-5" style="max-width: 1120px;">
      <h1 class="text-center fw-bold mb-5 text-primary">
        {{ t.newBonus }}
      </h1>

      <div class="card shadow-lg border-0 rounded-4 p-4"
           style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">

        <div class="row g-4">

          <div class="col-md-3">
            <label class="form-label fw-semibold">{{ t.uses }}</label>
            <input type="number" class="form-control form-control-lg"
                   v-model.number="bono.usos"
                   :class="{ 'is-invalid': errores.usos }" />
          </div>

          <div class="col-md-3">
            <label class="form-label fw-semibold">{{ t.validity }}</label>
            <input type="number" class="form-control form-control-lg"
                   v-model.number="bono.validez"
                   :class="{ 'is-invalid': errores.validez }" />
          </div>

          <div class="col-md-3">
            <label class="form-label fw-semibold">{{ t.priceUAM }}</label>
            <input type="number" step="0.01" class="form-control form-control-lg"
                   v-model.number="bono.precioUAM" />
          </div>

          <div class="col-md-3">
            <label class="form-label fw-semibold">{{ t.priceOthers }}</label>
            <input type="number" step="0.01" class="form-control form-control-lg"
                   v-model.number="bono.precioOtros" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.facility }}</label>
            <select class="form-select form-select-lg"
                    :class="{ 'is-invalid': errores.instalacion }"
                    v-model="bono.instalacion">
              <option :value="null">--</option>
              <option v-for="i in instalaciones" :key="i.id" :value="i.id">
                {{ i.nombre }}
              </option>
            </select>
          </div>

        </div>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-5">
          <button class="btn btn-primary btn-lg px-5 rounded-pill shadow-sm" @click="crearAbono">
            {{ t.createBonuses }}
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
import { type Ref, ref, inject, onMounted } from "vue"
import { useRouter } from "vue-router"

import { nuevoBono } from "@/services/crearRecursosService"
import { getInstalacionesSimples } from "@/services/listadoService"

import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter()

const bono = ref({
  usos: 10,
  validez: 1,
  precioTDA: 0,
  precioUAM: 0,
  precioAbono: 0,
  precioOtros: 0,
  instalacion: null as number | null
})

const instalaciones = ref<any[]>([])

const errores = ref({
  usos: false,
  validez: false,
  instalacion: false
})

function validar() {
  errores.value.usos = bono.value.usos <= 0
  errores.value.validez = bono.value.validez <= 0
  errores.value.instalacion = bono.value.instalacion == null

  return !errores.value.usos
}

const cargarDatos = async () => {
  try {
    instalaciones.value = await getInstalacionesSimples()
  } catch (e) {
    console.error("Error cargando datos:", e)
  }
}

const crearAbono = async () => {
  if (!validar()) return

  try {
    await nuevoBono(bono.value)
    router.back()
  } catch (e) {
    console.error("Error creando bono", e);
  }
}

const volver = () => {
  router.back()
}

onMounted(cargarDatos)
</script>