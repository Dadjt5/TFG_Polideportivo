<template>
  <div class="min-vh-100 bg-light pb-5">
    <main class="container py-5" style="max-width: 900px;">
      <h1 class="text-center fw-bold mb-5">
        {{ t.newDiscount }}
      </h1>

      <div class="card shadow-sm border-0 rounded-4 p-4">
        <div class="row g-4">

          <!-- NOMBRE -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.name }}</label>
            <input type="text" class="form-control form-control-lg" :class="{ 'is-invalid': errores.nombre }"
              v-model="descuento.nombre" />
          </div>

          <!-- PORCENTAJE -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.percentage }}</label>
            <input type="number" min="0" max="100" class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.porcentaje }" v-model="descuento.porcentaje" />
          </div>

          <!-- DESCRIPCIÓN -->
          <div class="col-12">
            <label class="form-label fw-semibold">{{ t.description }}</label>
            <textarea class="form-control" rows="3" v-model="descuento.descripcion"></textarea>
          </div>

          <!-- FECHAS -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.startDate }}</label>
            <input type="date" class="form-control" v-model="descuento.fechaInicio" />
          </div>

          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.endDate }}</label>
            <input type="date" class="form-control" v-model="descuento.fechaFinValidez" />
          </div>

          <!-- CHECKS -->
          <div class="col-md-6 form-check">
            <input type="checkbox" class="form-check-input" v-model="descuento.combinable" />
            <label class="form-check-label fw-semibold">
              {{ t.combinable }}
            </label>
          </div>

          <div class="col-md-6 form-check">
            <input type="checkbox" class="form-check-input" v-model="descuento.prioritario" />
            <label class="form-check-label fw-semibold">
              {{ t.priority }}
            </label>
          </div>

          <!-- TIPOS INSTALACIÓN -->
          <div class="col-12">
            <label class="form-label fw-semibold mb-3 d-block">
              {{ t.facilityType }}
            </label>

            <div class="row g-3">
              <div v-for="tipo in estadisticasStore.data.tiposInstalacion" :key="tipo[0]" class="col-md-4">
                <div class="border rounded-3 p-3 h-100 cursor-pointer"
                  :class="{ 'border-primary bg-light': descuento.tiposInstalacion.includes(tipo[0]) }"
                  @click="toggleTipo(tipo[0])">
                  {{ tipo[1] }}
                </div>
              </div>
            </div>
          </div>

          <!-- DEPORTES -->
          <div class="col-12">
            <label class="form-label fw-semibold mb-3 d-block">
              {{ t.sports }}
            </label>

            <div class="row g-3">
              <div v-for="deporte in deportes" :key="deporte.id" class="col-md-3">
                <div class="border rounded-3 p-3 h-100 cursor-pointer text-center" :class="{
                  'border-primary bg-light': descuento.deportes.includes(deporte.id)
                }" @click="toggleDeporte(deporte.id)">
                  {{ deporte.titulo }}
                </div>
              </div>
            </div>
          </div>

        </div>

        <!-- MENSAJE -->
        <p v-if="mensaje" class="text-center text-danger mt-4">
          {{ mensaje }}
        </p>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-5">
          <button class="btn btn-primary btn-lg px-5" @click="crearDescuento">
            {{ t.newDiscount }}
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
import { ref, inject, type Ref, onMounted } from "vue"
import { useRouter } from "vue-router"

import { useEstadisticasStore } from "@/stores/estadisticas"
import { getDeportes } from "@/services/listadoService"
import { nuevoDescuento } from "@/services/crearRecursosService"

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const estadisticasStore = useEstadisticasStore()
const router = useRouter()

const descuento = ref({
  nombre: "",
  descripcion: "",
  porcentaje: 0,
  combinable: false,
  prioritario: false,
  fechaInicio: "",
  fechaFinValidez: "",
  tiposInstalacion: [] as string[],
  deportes: [] as number[]
})

const errores = ref({
  nombre: false,
  porcentaje: false
})

const mensaje = ref("")
const deportes = ref<any[]>([])

function validar() {
  errores.value.nombre = descuento.value.nombre === ""
  errores.value.porcentaje =
    descuento.value.porcentaje < 0 ||
    descuento.value.porcentaje > 100

  return !errores.value.nombre && !errores.value.porcentaje
}

function toggleDeporte(id: number) {
  const index = descuento.value.deportes.indexOf(id)
  if (index > -1) {
    descuento.value.deportes.splice(index, 1)
  } else {
    descuento.value.deportes.push(id)
  }
}

function toggleTipo(valor: string) {
  const index = descuento.value.tiposInstalacion.indexOf(valor)

  if (index > -1) {
    descuento.value.tiposInstalacion.splice(index, 1)
  } else {
    descuento.value.tiposInstalacion.push(valor)
  }
}

const crearDescuento = async () => {
  if (!validar()) return

  try {
    await nuevoDescuento(descuento.value)
    router.push({ name: "gestion-tarifas" })
  } catch (error: any) {
    mensaje.value = t.value.unexpectedError
  }
}

function volver() {
  router.back()
}

onMounted(async () => {
  deportes.value = await getDeportes()
})
</script>