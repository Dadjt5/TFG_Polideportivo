<template>
  <div class="min-vh-100 pt-4" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4" style="max-width: 1600px;">

      <div class="d-flex justify-content-between align-items-center mb-4">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold mb-0">{{ monitor.nombre }}</h1>

        <div style="width: 100px"></div>
      </div>

      <div class="card shadow-sm rounded-4">
        <div class="card-body p-4 p-md-5">

          <!-- MONITOR -->
          <div class="d-flex flex-column flex-md-row align-items-center gap-4 mb-4">
            <div class="rounded-circle bg-success bg-opacity-10 d-flex align-items-center justify-content-center"
              style="width:96px;height:96px">
              <i class="bi bi-person-badge-fill text-success fs-1"></i>
            </div>

            <div class="flex-fill text-center text-md-start">
              <h3 class="fw-semibold mb-1">
                {{ monitor.nombre }} {{ monitor.apellidos }}
              </h3>
              <p class="text-muted mb-0">{{ t.monitor }}</p>
            </div>
          </div>

          <!-- DATOS -->
          <div class="row g-3">

            <!-- NOMBRE -->
            <div class="col-md-4">
              <label class="form-label">{{ t.name }}</label>
              <input v-if="isEditing" class="form-control" v-model="monitor.nombre"
                :class="{ 'is-invalid': errores.nombre }" />
              <p v-else class="form-control-plaintext">
                {{ monitor.nombre || '-' }}
              </p>
            </div>

            <!-- APELLIDOS -->
            <div class="col-md-4">
              <label class="form-label">{{ t.surnames }}</label>
              <input v-if="isEditing" class="form-control" v-model="monitor.apellidos"
                :class="{ 'is-invalid': errores.apellidos }" />
              <p v-else class="form-control-plaintext">
                {{ monitor.apellidos || '-' }}
              </p>
            </div>

            <!-- DNI -->
            <div class="col-md-4">
              <label class="form-label">DNI</label>
              <p class="form-control-plaintext">
                {{ monitor.DNI || '-' }}
              </p>
            </div>

            <!-- Codigo usuarios -->
            <div class="col-md-4">
              <label class="form-label">{{ t.loginCode }}</label>
              <p class="form-control-plaintext">
                {{ monitor.codigo_usuario || '-' }}
              </p>
            </div>

            <!-- Correo -->
            <div class="col-md-4">
              <label class="form-label">{{ t.email }}</label>
              <p class="form-control-plaintext">
                {{ monitor.email }}
              </p>
            </div>

          </div>

          <div v-if="mostrarMensaje" class="text-center mb-3">
            <div class="alert" :class="tipoMensaje === 'success' ? 'alert-success' : 'alert-danger'">
              {{ mensajeEditar }}
            </div>
          </div>

          <!-- ACCIONES -->
          <div class="d-flex justify-content-center gap-4 mt-5">

            <button v-if="!isEditing" class="btn btn-primary btn-lg rounded-pill" @click="activarEdicion">
              <i class="bi bi-pencil me-2"></i>
              {{ t.modifyUser }}
            </button>

            <template v-else>
              <button class="btn btn-success btn-lg rounded-pill" @click="guardarCambios">
                <i class="bi bi-check-lg me-2"></i>
                {{ t.saveChanges }}
              </button>

              <button class="btn btn-secondary btn-lg rounded-pill" @click="cancelarEdicion">
                {{ t.cancel }}
              </button>
            </template>

            <button v-if="!isEditing" class="btn btn-danger btn-lg rounded-pill" @click="abrirConfirmacion">
              <i class="bi bi-trash me-2"></i>
              {{ t.delete }}
            </button>

          </div>

        </div>
      </div>
    </main>

    <div class="modal fade" id="confirmDeleteModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4">

          <div class="modal-header">
            <h5 class="modal-title">{{ t.confirmDelete }}</h5>
          </div>

          <div class="modal-body text-center">
            <p>{{ t.confirmDeleteMonitor }}</p>
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
import { ref, inject, onMounted, type Ref } from 'vue'
import { useRouter } from 'vue-router'
import { Modal } from 'bootstrap'

import { getMonitor, modificarMonitor, eliminarMonitor } from '@/services/monitorService'

import type { Language } from '@/useI18N'
import { useI18n } from '@/useI18N'

const props = defineProps<{ id: string }>()

const router = useRouter()

const language = inject<Ref<Language>>('language')!
const t = useI18n(language)

const mensaje = ref("")
const isEditing = ref(false)
const mensajeEditar = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)

const monitor = ref({
  id: 0,
  nombre: '',
  apellidos: '',
  DNI: '',
  codigo_usuario: '',
  email: ''
})

const monitorOriginal = ref<any>(null)

const errores = ref({
  nombre: false,
  apellidos: false,
})

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensajeEditar.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true

  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
}

function validarFormulario() {
  let valido = true

  errores.value.nombre = monitor.value.nombre === ''
  errores.value.apellidos = monitor.value.apellidos === ''

  for (const key in errores.value) {
    if (errores.value[key as keyof typeof errores.value]) {
      valido = false
    }
  }

  return valido
}

function activarEdicion() {
  mensaje.value = ""
  monitorOriginal.value = JSON.parse(JSON.stringify(monitor.value))
  Object.keys(errores.value).forEach(
    k => (errores.value[k as keyof typeof errores.value] = false)
  )
  isEditing.value = true
}

function cancelarEdicion() {
  mensaje.value = ""
  monitor.value = JSON.parse(JSON.stringify(monitorOriginal.value))
  isEditing.value = false
}

function camposModificados() {
  const data: any = {}

  if (monitorOriginal.value.nombre !== monitor.value.nombre) {
    data.nombre = monitor.value.nombre
  }

  if (monitorOriginal.value.apellidos !== monitor.value.apellidos) {
    data.apellidos = monitor.value.apellidos
  }

  if (monitorOriginal.value.DNI !== monitor.value.DNI) {
    data.DNI = monitor.value.DNI
  }

  if (monitorOriginal.value.email !== monitor.value.email) {
    data.email = monitor.value.email
  }

  return data
}

let confirmModal: Modal
let successModal: Modal

const eliminado = ref(false)

function abrirConfirmacion() {
  confirmModal.show()
}

async function confirmarEliminar() {
  try {
    await eliminarMonitor(monitor.value.id)

    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.monitorDeleted
    eliminado.value = true
  } catch (e) {
    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.monitorNoDeleted
    eliminado.value = false
    console.error("Error al eliminar el monitor", e);
  }
}

async function guardarCambios() {
  if (!validarFormulario()) {
    lanzarMensaje(t.value.missing, "error")
    return
  }

  const data = camposModificados()
  if (Object.keys(data).length === 0) {
    lanzarMensaje(t.value.noChanges, "success")
    isEditing.value = false
    return
  }

  try {
    await modificarMonitor(monitor.value.id, data)
    lanzarMensaje(t.value.correctlyUpdate, "success")
    isEditing.value = false
  } catch (e) {
    lanzarMensaje(t.value.noModify, "error")
    console.error('Error al modificar el monitor', e)
  }
}

const finalizar = async () => {
  if (eliminado.value) {
    router.push({ name: 'gestion-usuarios' });
  } else {
    successModal.hide()
    eliminado.value = false
  }
}

function volver() {
  router.back()
}

onMounted(async () => {
  const id = parseInt(props.id)

  confirmModal = new Modal(document.getElementById('confirmDeleteModal')!)
  successModal = new Modal(document.getElementById('successDeleteModal')!)

  try {
    monitor.value = await getMonitor(id)
    monitorOriginal.value = JSON.parse(JSON.stringify(monitor.value))
  } catch (e) {
    mensaje.value = t.value.unexpectedError
    console.error('Error al obtener informacion del monitor', e)
  }
})
</script>
