<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #e0f7ff, #ffffff);">
    <main class="container py-5" style="max-width: 1120px;">
      <h1 class="text-center fw-bold mb-5 text-primary">
        {{ t.newDiscount }}
      </h1>

      <div class="card shadow-lg border-0 rounded-4 p-4"
        style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">

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
            <textarea class="form-control form-control-lg" rows="3" v-model="descuento.descripcion"></textarea>
          </div>

          <!-- FECHAS -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.startDate }}</label>
            <input type="date" class="form-control form-control-lg" v-model="descuento.fechaInicio" />
          </div>

          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.endDate }}</label>
            <input type="date" class="form-control form-control-lg" v-model="descuento.fechaFinValidez" />
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
              <div v-for="tipo in estadisticasStore.data.tiposInstalacion" :key="tipo" class="col-md-4">
                <div class="border rounded-3 p-3 h-100 cursor-pointer text-center"
                  :class="{ 'border-primary bg-white shadow-sm': descuento.tiposInstalacion.includes(tipo) }"
                  @click="toggleTipo(tipo)">
                  {{ tipo }}
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
                <div class="border rounded-3 p-3 h-100 cursor-pointer text-center"
                  :class="{ 'border-primary bg-white shadow-sm': descuento.deportes_ids.includes(deporte.id) }"
                  @click="toggleDeporte(deporte.id)">
                  {{ deporte.titulo }}
                </div>
              </div>
            </div>
          </div>

        </div>

        <div v-if="mostrarMensaje" class="text-center mb-3 mt-3">
          <div class="alert" :class="tipoMensaje === 'success' ? 'alert-success' : 'alert-danger'">
            {{ mensajeEditar }}
          </div>
        </div>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-5">
          <button class="btn btn-primary btn-lg px-5 rounded-pill shadow-sm" @click="crearDescuento">
            {{ t.newDiscount }}
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
  deportes_ids: [] as number[],
  deportes: []
})

const errores = ref({
  nombre: false,
  porcentaje: false
})

const mensajeEditar = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)
const deportes = ref<any[]>([])

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensajeEditar.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true

  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
}

function validar() {
  errores.value.nombre = descuento.value.nombre === ""
  errores.value.porcentaje =
    descuento.value.porcentaje < 0 ||
    descuento.value.porcentaje > 100

  return !errores.value.nombre && !errores.value.porcentaje
}

function toggleDeporte(id: number) {
  const index = descuento.value.deportes_ids.indexOf(id)
  if (index > -1) {
    descuento.value.deportes_ids.splice(index, 1)
  } else {
    descuento.value.deportes_ids.push(id)
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

function fechasValidas() {
  if (!descuento.value.fechaInicio || !descuento.value.fechaFinValidez) {
    return false
  }

  const inicio = new Date(descuento.value.fechaInicio)
  const fin = new Date(descuento.value.fechaFinValidez)
  const hoy = new Date()

  inicio.setHours(0,0,0,0)
  fin.setHours(0,0,0,0)
  hoy.setHours(0,0,0,0)

  if (inicio < hoy) {
    lanzarMensaje(t.value.dateError2, "error")
    return false
  }

  if (fin < inicio) {
    lanzarMensaje(t.value.dateError, "error")
    return false
  }

  return true
}

const crearDescuento = async () => {
  if (!validar()) {
    lanzarMensaje(t.value.missing, "error")
    return
  }

  if (!fechasValidas()) {
    return
  }

  if (descuento.value.tiposInstalacion.length == 0 && descuento.value.deportes_ids.length == 0) {
    lanzarMensaje(t.value.selectAtLeastOne, "error")
    return
  }

  try {
    const payload = {
      ...descuento.value,
      deportes: descuento.value.deportes_ids
    }

    await nuevoDescuento(payload)
    router.push({ name: "gestion-tarifas" })
  } catch (e) {
    lanzarMensaje(t.value.discountNoCreated, "error")
    console.error("Error al crear el descuento", e)
  }
}

function volver() {
  router.back()
}

onMounted(async () => {
  deportes.value = await getDeportes()
})
</script>