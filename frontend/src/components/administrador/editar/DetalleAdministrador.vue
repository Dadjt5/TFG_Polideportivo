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
                <option value="RAIZ">{{ t.rootAdmin }}</option>
                <option value="USUARIOS">{{ t.usersAdmin }}</option>
                <option value="ESPACIOS">{{ t.spacesAdmin }}</option>
                <option value="TARIFAS">{{ t.tariffsAdmin }}</option>
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

            <button v-if="!isEditing" class="btn btn-danger btn-lg rounded-pill" @click="eliminar">
              <i class="bi bi-trash me-2"></i>
              {{ t.deleteUser }}
            </button>

          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, inject, onMounted, type Ref } from 'vue'
import { useRouter } from 'vue-router'

import { getAdministrador, modificarAdministrador, eliminarAdministrador } from '@/services/administradorService'

import type { Language } from '@/useI18N'
import { useI18n } from '@/useI18N'

const props = defineProps<{ id: string }>()

const router = useRouter()

const language = inject<Ref<Language>>('language')!
const t = useI18n(language)

const isEditing = ref(false)

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

async function guardarCambios() {
  if (!validarFormulario()) return

  const data = camposModificados()
  if (Object.keys(data).length === 0) {
    isEditing.value = false
    return
  }

  try {
    await modificarAdministrador(admin.value.id, data)
    isEditing.value = false
  } catch (e) {
    console.error('Error al modificar el administrador', e)
  }
}

const eliminar = async () => {
  try {
    await eliminarAdministrador(admin.value.id)
  } catch (e) {
    console.error("Error al eliminar el administrador", e);
  }
}

function volver() {
  router.back()
}

onMounted(async () => {
  try {
    const id = parseInt(props.id)
    admin.value = await getAdministrador(id)
    adminOriginal.value = JSON.parse(JSON.stringify(admin.value))
  } catch (e) {
    console.error('Error al cargar el administrador', e)
  }
})
</script>
