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
                <input v-else class="form-control" v-model="descuento.nombre"></input>
              </div>

              <!-- DESCRIPCIÓN -->
              <div class="col-12">
                <span class="fw-medium">{{ t.description }}:</span>
                <p v-if="!editando">{{ descuento.descripcion }}</p>
                <textarea v-else class="form-control" rows="3" v-model="descuento.descripcion"></textarea>
              </div>

              <!-- PORCENTAJE -->
              <div class="col-12">
                <span class="fw-medium">{{ t.percentage }}:</span>
                <p v-if="!editando">{{ descuento.porcentaje }}%</p>
                <input v-else type="number" min="0" max="100" class="form-control" v-model="descuento.porcentaje" />
              </div>

              <!-- FECHAS -->
              <div class="col-6">
                <span class="fw-medium">{{ t.startDate }}:</span>
                <p v-if="!editando">{{ descuento.fechaInicio }}</p>
                <input v-else type="date" class="form-control" v-model="descuento.fechaInicio" />
              </div>

              <div class="col-6">
                <span class="fw-medium">{{ t.endDate }}:</span>
                <p v-if="!editando">{{ descuento.fechaFinValidez }}</p>
                <input v-else type="date" class="form-control" v-model="descuento.fechaFinValidez" />
              </div>

              <!-- CHECKS -->
              <div class="col-6">
                <span class="fw-medium">{{ t.combinable }}:</span>
                <p v-if="!editando">{{ descuento.combinable ? "Sí" : "No" }}</p>
                <input v-else type="checkbox" class="form-check-input ms-2" v-model="descuento.combinable" />
              </div>

              <div class="col-6">
                <span class="fw-medium">{{ t.priority }}:</span>
                <p v-if="!editando">{{ descuento.prioritario ? "Sí" : "No" }}</p>
                <input v-else type="checkbox" class="form-check-input ms-2" v-model="descuento.prioritario" />
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
                <div v-for="tipo in estadisticasStore.data.tiposInstalacion" :key="tipo" class="form-check">
                  <input type="checkbox" class="form-check-input" :value="tipo" v-model="descuento.tiposInstalacion" />
                  <label class="form-check-label">
                    {{ tipo }}
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

              <div v-else class="border rounded-3 p-2 bg-light">
                <div v-for="deporte in deportes" :key="deporte.id" class="form-check">
                  <input class="form-check-input" type="checkbox" :id="'dep-' + deporte.id" :value="deporte.id"
                    v-model="descuento.deportes_ids" />

                  <label class="form-check-label" :for="'dep-' + deporte.id">
                    {{ deporte.titulo }}
                  </label>
                </div>
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

        <button v-if="!editando" class="btn btn-danger btn-lg rounded-pill" @click="abrirConfirmacion">
          <i class="bi bi-trash me-2"></i> {{ t.deleteDiscount }}
        </button>

      </div>
    </main>

    <div class="modal fade" id="confirmDeleteModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4">

          <div class="modal-header">
            <h5 class="modal-title">{{ t.confirmDelete }}</h5>
          </div>

          <div class="modal-body text-center">
            <p>{{ t.confirmDeleteDiscount }}</p>
          </div>

          <div class="modal-footer justify-content-center">
            <button class="btn btn-secondary rounded-pill" data-bs-dismiss="modal">
              {{ t.cancel }}
            </button>

            <button class="btn btn-danger rounded-pill" @click="confirmarEliminar">
              {{ t.delete }}
            </button>
          </div>

        </div>
      </div>
    </div>

    <div class="modal fade" id="successDeleteModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4 text-center">

          <div class="modal-body py-5">

            <i v-if="eliminado" class="bi bi-check-circle-fill text-success fs-1 mb-3"></i>
            <i v-else class="bi bi-exclamation-octagon-fill text-danger fs-1 mb-3"></i>

            <h4 class="fw-semibold">
              {{ mensaje }}
            </h4>

            <button class="btn btn-primary rounded-pill mt-4" @click="finalizar" data-bs-dismiss="modal">
              <span v-if="eliminado">{{ t.continue }}</span>
              <span v-else>{{ t.return }}</span>
            </button>

          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { inject, ref, onMounted, computed, type Ref } from "vue"
import { useRouter } from "vue-router"
import { Modal } from 'bootstrap'

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
const mensaje = ref("")
const mensajeEditar = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)

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
  deportes_ids: [],
  deportes: []
})

const errores = ref({
  nombre: false,
  descripcion: false,
  porcentaje: false,
  fechaInicio: false,
  fechaFinValidez: false
})

const descuentoOriginal = ref<any>(null)

const deportes = ref<any[]>([])

const nombresDeportesSeleccionados = computed(() => {
  if (!descuento.value.deportes_ids || deportes.value.length === 0) return []

  return deportes.value
    .filter((dep: any) => descuento.value.deportes_ids.includes(dep.id))
    .map((dep: any) => dep.titulo)
})

function validarFormulario() {
  let valido = true

  errores.value.nombre = descuento.value.nombre.trim() === ''
  errores.value.descripcion = descuento.value.descripcion.trim() === ''
  errores.value.porcentaje =
    descuento.value.porcentaje === '' ||
    descuento.value.porcentaje < 0 ||
    descuento.value.porcentaje > 100

  errores.value.fechaInicio = descuento.value.fechaInicio === ''
  errores.value.fechaFinValidez = descuento.value.fechaFinValidez === ''

  for (const key in errores.value) {
    if (errores.value[key]) {
      valido = false
    }
  }

  return valido
}

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensajeEditar.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true

  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
}

function activarEdicion() {
  mensaje.value = ""
  descuentoOriginal.value = JSON.parse(JSON.stringify(descuento.value))
  editando.value = true
}

function cancelarEdicion() {
  mensaje.value = ""
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
  if (!validarFormulario()) {
    lanzarMensaje(t.value.missing, "error")
    return
  }

  if (!fechasValidas()) {
    return
  }

  if (descuento.value.tiposInstalacion.length == 0 || descuento.value.deportes.length == 0) {
    lanzarMensaje(t.value.selectAtLeastOne, "error")
    return
  }

  try {
    const data = camposModificados()
    if (Object.keys(data).length > 0) {
      await modificarDescuento(descuento.value.id, data)
      lanzarMensaje(t.value.correctlyUpdate, "success")
    } else {
      lanzarMensaje(t.value.noChanges, "success")
    }

    editando.value = false
  } catch (e) {
    lanzarMensaje(t.value.noModify, "error")
    console.error('Error al modificar el descuento', e)
  }
}

let confirmModal: Modal
let successModal: Modal

const eliminado = ref(false)

function abrirConfirmacion() {
  confirmModal.show()
}

function fechasValidas() {
  if (!descuento.value.fechaInicio || !descuento.value.fechaFinValidez) {
    return false
  }

  const inicio = new Date(descuento.value.fechaInicio)
  const fin = new Date(descuento.value.fechaFinValidez)
  const hoy = new Date()

  inicio.setHours(0, 0, 0, 0)
  fin.setHours(0, 0, 0, 0)
  hoy.setHours(0, 0, 0, 0)

  if (fin < inicio) {
    lanzarMensaje(t.value.dateError, "error")
    return false
  }

  return true
}

async function confirmarEliminar() {
  try {
    await eliminarDescuento(descuento.value.id)

    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.discountDeleted
    eliminado.value = true
  } catch (e) {
    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.discountNoDeleted
    eliminado.value = false
    console.error("Error al eliminar el descuento", e);
  }
}

const finalizar = async () => {
  if (eliminado.value) {
    router.push({ name: 'gestion-tarifas' });
  } else {
    successModal.hide()
    eliminado.value = false
  }
}

const volver = () => router.back()

onMounted(async () => {
  confirmModal = new Modal(document.getElementById('confirmDeleteModal')!)
  successModal = new Modal(document.getElementById('successDeleteModal')!)

  try {
    const detalles = await getDescuentoDetalle(parseInt(props.id))

    descuento.value = detalles
    descuento.value.deportes_ids = detalles.deportes.map((d: any) => d.id)
    descuentoOriginal.value = JSON.parse(JSON.stringify(descuento.value))
    deportes.value = await getDeportes()
  } catch (e) {
    lanzarMensaje(t.value.unexpectedError, "error")
    console.error("Error al obtener la informacion del descuento", e)
  }
})
</script>