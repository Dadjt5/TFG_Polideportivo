<template>
  <div class="min-vh-100 pt-4" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4" style="max-width: 1600px;">

      <div class="d-flex justify-content-between align-items-center mb-4">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold mb-0">{{ admin.nombre }}</h1>

        <div style="width: 100px"></div>
      </div>

      <div class="card border-0 shadow-lg rounded-4">
        <div class="card-body p-4 p-md-5">

          <!-- DATOS -->
          <div class="row g-3">

            <!-- NOMBRE -->
            <div class="col-md-4">
              <label class="form-label">{{ t.name }}</label>
              <input v-if="isEditing" class="form-control" v-model="admin.nombre"
                :class="{ 'is-invalid': errores.nombre }" />
              <p v-else class="form-control-plaintext">
                {{ admin.nombre || '-' }}
              </p>
            </div>

            <!-- DNI -->
            <div class="col-md-4">
              <label class="form-label">DNI</label>
              <p class="form-control-plaintext">
                {{ admin.DNI || '-' }}
              </p>
            </div>

            <!-- Codigo usuario -->
            <div class="col-md-4">
              <label class="form-label">{{ t.loginCode }}</label>
              <p class="form-control-plaintext">
                {{ admin.codigo_usuario || '-' }}
              </p>
            </div>

            <!-- ROL -->
            <div class="col-md-4">
              <label class="form-label">{{ t.role }}</label>
              <select v-if="isEditing" class="form-select form-select-lg" :class="{ 'is-invalid': errores.rol }"
                v-model="admin.rol">
                <option value="" disabled>{{ t.selectOption }}</option>
                <option value="Administrador raiz">{{ t.rootAdmin }}</option>
                <option value="Administrador de usuarios">{{ t.usersAdmin }}</option>
                <option value="Administrador de espacios">{{ t.spacesAdmin }}</option>
                <option value="Administrador de tarifas">{{ t.tariffsAdmin }}</option>
              </select>

              <p v-else class="form-control-plaintext">
                {{ admin.rol || '-' }}
              </p>
            </div>

            <!-- Correo -->
            <div class="col-md-4">
              <label class="form-label">{{ t.email }}</label>
              <p class="form-control-plaintext">
                {{ admin.email }}
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

            <button v-if="!isEditing && !esYo()" class="btn btn-primary btn-lg rounded-pill" @click="activarEdicion">
              <i class="bi bi-pencil me-2"></i>
              {{ t.modifyUser }}
            </button>

            <template v-if="isEditing && !esYo()">
              <button class="btn btn-success btn-lg rounded-pill" @click="guardarCambios">
                <i class="bi bi-check-lg me-2"></i>
                {{ t.saveChanges }}
              </button>

              <button class="btn btn-secondary btn-lg rounded-pill" @click="cancelarEdicion">
                {{ t.cancel }}
              </button>
            </template>

            <button v-if="!isEditing && !esYo()" class="btn btn-danger btn-lg rounded-pill" @click="abrirConfirmacion">
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
            <p>{{ t.confirmDeleteAdmin }}</p>
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

import { getAdministrador, modificarAdministrador, eliminarAdministrador } from '@/services/administradorService'
import { useAuthStore } from '@/stores/auth'

import type { Language } from '@/useI18N'
import { useI18n } from '@/useI18N'
import { useAdministradorStore } from '@/stores/administrador'

const props = defineProps<{ id: string }>()

const router = useRouter()

const language = inject<Ref<Language>>('language')!
const t = useI18n(language)

const isEditing = ref(false)
const authStore = useAuthStore()
const mensaje = ref("")
const eliminado = ref(false)
const mensajeEditar = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)

const admin = ref({
  id: 0,
  nombre: '',
  DNI: '',
  codigo_usuario: '',
  email: '',
  rol: ''
})

const adminOriginal = ref<any>(null)

const errores = ref({
  nombre: false,
  rol: false
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

  errores.value.nombre = admin.value.nombre === ''
  errores.value.rol = admin.value.rol === ''

  for (const key in errores.value) {
    if (errores.value[key as keyof typeof errores.value]) {
      valido = false
    }
  }

  return valido
}

function activarEdicion() {
  adminOriginal.value = JSON.parse(JSON.stringify(admin.value))
  Object.keys(errores.value).forEach(
    k => (errores.value[k as keyof typeof errores.value] = false)
  )
  isEditing.value = true
}

function cancelarEdicion() {
  admin.value = JSON.parse(JSON.stringify(adminOriginal.value))
  isEditing.value = false
}

function camposModificados() {
  const data: any = {}

  if (adminOriginal.value.nombre !== admin.value.nombre) {
    data.nombre = admin.value.nombre
  }

  if (adminOriginal.value.DNI !== admin.value.DNI) {
    data.DNI = admin.value.DNI
  }

  if (adminOriginal.value.rol !== admin.value.rol) {
    data.rol = admin.value.rol
  }

  return data
}

function comprobarPermisos() {
  if (!authStore.isAdminRaiz && (adminOriginal.value.rol == "Administrador raiz" || admin.value.rol == "Administrador raiz")) {
    return false
  }

  return true
}

const administradorStore = useAdministradorStore();

async function guardarCambios() {
  if (!validarFormulario()) {
    lanzarMensaje(t.value.missing, "error")
    return
  }

  if (!comprobarPermisos()) {
    lanzarMensaje(t.value.noPermissions, "error")
    return
  }

  const data = camposModificados()
  if (Object.keys(data).length === 0) {
    lanzarMensaje(t.value.noChanges, "success")
    isEditing.value = false
    return
  }

  try {
    await modificarAdministrador(admin.value.id, data)
    lanzarMensaje(t.value.correctlyUpdate, "success")
    isEditing.value = false
  } catch (e) {
    lanzarMensaje(t.value.noModify, "error")
    console.error('Error al modificar el administrador', e)
  }
}

function esYo() {
  return admin.value.id === administradorStore.administrador.id
}

let confirmModal: Modal
let successModal: Modal

function abrirConfirmacion() {
  confirmModal.show()
}

async function confirmarEliminar() {
  try {
    await eliminarAdministrador(admin.value.id)

    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.adminDeleted
    eliminado.value = true
  } catch (e) {
    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.adminNoDeleted
    eliminado.value = false
    console.error("Error al eliminar el administrador", e);
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
    admin.value = await getAdministrador(id)
    adminOriginal.value = JSON.parse(JSON.stringify(admin.value))
  } catch (e) {
    mensaje.value = t.value.unexpectedError
    console.error('Error al cargar el administrador', e)
  }
})
</script>
