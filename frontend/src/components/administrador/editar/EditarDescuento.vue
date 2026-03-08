<template>
  <div class="min-vh-100 pt-4" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4" style="max-width: 1600px;">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4 mt-3">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold text-primary mb-2" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
          {{ descuento.nombre }}
        </h1>

        <div style="width: 100px"></div>
      </div>

      <div class="row g-4">

        <!-- INFORMACIÓN GENERAL -->
        <div class="col-lg-6">
        <div class="card shadow-lg rounded-4 p-4"
            style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(10px);">

            <h4 class="mb-3">
              <i class="bi bi-percent text-primary me-2"></i>
              {{ t.discountDetail }}
            </h4>

            <div class="row g-3">

              <!-- DESCRIPCIÓN -->
              <div class="col-12">
                <span class="fw-medium">{{ t.name }}:</span>
                <p v-if="!editando">{{ descuento.nombre }}</p>
                <input
                  v-else
                  class="form-control"
                  v-model="descuento.nombre"
                ></input>
              </div>

              <!-- DESCRIPCIÓN -->
              <div class="col-12">
                <span class="fw-medium">{{ t.description }}:</span>
                <p v-if="!editando">{{ descuento.descripcion }}</p>
                <textarea
                  v-else
                  class="form-control"
                  rows="3"
                  v-model="descuento.descripcion"
                ></textarea>
              </div>

              <!-- PORCENTAJE -->
              <div class="col-12">
                <span class="fw-medium">{{ t.percentage }}:</span>
                <p v-if="!editando">{{ descuento.porcentaje }}%</p>
                <input
                  v-else
                  type="number"
                  min="0"
                  max="100"
                  class="form-control"
                  v-model="descuento.porcentaje"
                />
              </div>

              <!-- FECHAS -->
              <div class="col-6">
                <span class="fw-medium">{{ t.startDate }}:</span>
                <p v-if="!editando">{{ descuento.fechaInicio }}</p>
                <input
                  v-else
                  type="date"
                  class="form-control"
                  v-model="descuento.fechaInicio"
                />
              </div>

              <div class="col-6">
                <span class="fw-medium">{{ t.endDate }}:</span>
                <p v-if="!editando">{{ descuento.fechaFinValidez }}</p>
                <input
                  v-else
                  type="date"
                  class="form-control"
                  v-model="descuento.fechaFinValidez"
                />
              </div>

              <!-- CHECKS -->
              <div class="col-6">
                <span class="fw-medium">{{ t.combinable }}:</span>
                <p v-if="!editando">{{ descuento.combinable ? "Sí" : "No" }}</p>
                <input
                  v-else
                  type="checkbox"
                  class="form-check-input ms-2"
                  v-model="descuento.combinable"
                />
              </div>

              <div class="col-6">
                <span class="fw-medium">{{ t.priority }}:</span>
                <p v-if="!editando">{{ descuento.prioritario ? "Sí" : "No" }}</p>
                <input
                  v-else
                  type="checkbox"
                  class="form-check-input ms-2"
                  v-model="descuento.prioritario"
                />
              </div>

            </div>
          </div>
        </div>

        <!-- APLICACIÓN -->
        <div class="col-lg-6">
          <div class="bg-white rounded-3 shadow-sm p-4">
            <h4 class="mb-3">
              <i class="bi bi-gear text-primary me-2"></i>
              {{ t.appliesTo }}
            </h4>

            <!-- TIPOS INSTALACIÓN -->
            <div class="mb-4">
              <span class="fw-medium">{{ t.facilityType }}:</span>

              <div v-if="!editando">
                <p v-if="descuento.tiposInstalacion.length === 0">—</p>
                <p v-else>{{ descuento.tiposInstalacion.join(", ") }}</p>
              </div>

              <div v-else class="d-flex flex-wrap gap-3">
                <div
                  v-for="tipo in estadisticasStore.data.tiposInstalacion"
                  :key="tipo[0]"
                  class="form-check"
                >
                  <input
                    type="checkbox"
                    class="form-check-input"
                    :value="tipo[0]"
                    v-model="descuento.tiposInstalacion"
                  />
                  <label class="form-check-label">
                    {{ tipo[1] }}
                  </label>
                </div>
              </div>
            </div>

            <!-- DEPORTES -->
            <div>
              <span class="fw-medium">{{ t.sports }}:</span>

              <div v-if="!editando">
                <p v-if="descuento.deportes.length === 0">—</p>
                <p v-else>
                  {{ nombresDeportesSeleccionados.join(", ") }}
                </p>
              </div>

              <select
                v-else
                multiple
                class="form-select"
                v-model="descuento.deportes"
              >
                <option
                  v-for="deporte in deportes"
                  :key="deporte.id"
                  :value="deporte.id"
                >
                  {{ deporte.nombre }}
                </option>
              </select>
            </div>

          </div>
        </div>
      </div>

      <!-- ACCIONES -->
      <div class="d-flex justify-content-center gap-3 mt-5">
        <button v-if="!editando" class="btn btn-primary btn-lg rounded-pill" @click="activarEdicion">
          <i class="bi bi-pencil me-2"></i> {{ t.modifyDiscount }}
        </button>

        <template v-else>
          <button class="btn btn-success btn-lg rounded-pill" @click="guardarCambios">
            <i class="bi bi-check-lg me-2"></i> {{ t.saveChanges }}
          </button>
          <button class="btn btn-secondary btn-lg rounded-pill" @click="cancelarEdicion">
            {{ t.cancel }}
          </button>
        </template>

        <button v-if="!editando" class="btn btn-danger btn-lg rounded-pill" @click="eliminar">
          <i class="bi bi-trash me-2"></i> {{ t.deleteDiscount }}
        </button>

      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { inject, ref, onMounted, computed, type Ref } from "vue"
import { useRouter } from "vue-router"

import { getDescuentoDetalle, modificarDescuento, eliminarDescuento } from "@/services/detalleService"
import { getDeportes } from "@/services/listadoService"
import { useEstadisticasStore } from "@/stores/estadisticas"

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const props = defineProps<{ id: string }>()

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const estadisticasStore = useEstadisticasStore()
const router = useRouter()
const editando = ref(false)

const descuento = ref<any>({
  id: 0,
  nombre: "",
  descripcion: "",
  porcentaje: 0,
  combinable: false,
  prioritario: false,
  fechaInicio: "",
  fechaFinValidez: "",
  tiposInstalacion: [],
  deportes: []
})

const descuentoOriginal = ref<any>(null)

const deportes = ref<any[]>([])

const tiposInstalacion = ref([
  { value: "PABELLON", label: "Pabellón" },
  { value: "PISCINA", label: "Piscina" },
  { value: "PISTA", label: "Pista" }
])

const errores = ref({ nombre: false })

const nombresDeportesSeleccionados = computed(() => {
  return deportes.value
    .filter(d => descuento.value.deportes.includes(d.id))
    .map(d => d.nombre)
})

function activarEdicion() {
  descuentoOriginal.value = JSON.parse(JSON.stringify(descuento.value))
  editando.value = true
}

function cancelarEdicion() {
  descuento.value = JSON.parse(JSON.stringify(descuentoOriginal.value))
  editando.value = false
}

function camposModificados() {
  const data: any = {}

  for (const key in descuento.value) {
    if (JSON.stringify(descuento.value[key]) !== JSON.stringify(descuentoOriginal.value[key])) {
      data[key] = descuento.value[key]
    }
  }

  return data
}

const guardarCambios = async () => {
  const data = camposModificados()

  if (Object.keys(data).length > 0) {
    await modificarDescuento(descuento.value.id, data)
  }

  editando.value = false
}

const eliminar = async () => {
  await eliminarDescuento(descuento.value.id)
  router.back()
}

const volver = () => router.back()

onMounted(async () => {
  descuento.value = await getDescuentoDetalle(parseInt(props.id))
  descuentoOriginal.value = JSON.parse(JSON.stringify(descuento.value))
  deportes.value = await getDeportes()
})
</script>