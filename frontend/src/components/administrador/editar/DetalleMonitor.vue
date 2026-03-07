<template>
  <div class="min-vh-100 bg-light pb-5">
    <main class="container py-5" style="max-width: 900px">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold mb-0">{{ t.monitorDetail }}</h1>

        <div style="width: 100px"></div>
      </div>

      <div class="card shadow-sm rounded-4">
        <div class="card-body p-4 p-md-5">

          <!-- MONITOR -->
          <div class="d-flex flex-column flex-md-row align-items-center gap-4 mb-4">
            <div
              class="rounded-circle bg-success bg-opacity-10 d-flex align-items-center justify-content-center"
              style="width:96px;height:96px"
            >
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
              <input
                v-if="isEditing"
                class="form-control"
                v-model="monitor.nombre"
                :class="{ 'is-invalid': errores.nombre }"
              />
              <p v-else class="form-control-plaintext">
                {{ monitor.nombre || '-' }}
              </p>
            </div>

            <!-- APELLIDOS -->
            <div class="col-md-4">
              <label class="form-label">{{ t.surnames }}</label>
              <input
                v-if="isEditing"
                class="form-control"
                v-model="monitor.apellidos"
                :class="{ 'is-invalid': errores.apellidos }"
              />
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

          <!-- ACCIONES -->
          <div class="d-flex justify-content-center gap-4 mt-5">

            <button
              v-if="!isEditing"
              class="btn btn-primary btn-lg rounded-pill"
              @click="activarEdicion"
            >
              <i class="bi bi-pencil me-2"></i>
              {{ t.modifyUser }}
            </button>

            <template v-else>
              <button
                class="btn btn-success btn-lg rounded-pill"
                @click="guardarCambios"
              >
                <i class="bi bi-check-lg me-2"></i>
                {{ t.saveChanges }}
              </button>

              <button
                class="btn btn-secondary btn-lg rounded-pill"
                @click="cancelarEdicion"
              >
                {{ t.cancel }}
              </button>
            </template>

            <button
              v-if="!isEditing"
              class="btn btn-danger btn-lg rounded-pill"
              @click="eliminar"
            >
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

import { getMonitor, modificarMonitor, eliminarMonitor } from '@/services/monitorService'

import type { Language } from '@/useI18N'
import { useI18n } from '@/useI18N'

const props = defineProps<{ id: string }>()

const router = useRouter()

const language = inject<Ref<Language>>('language')!
const t = useI18n(language)

const isEditing = ref(false)

const monitor = ref({
  id: 0,
  nombre: '',
  apellidos: '',
  DNI: '',
  codigo_usuario: '',
  email:''
})

const monitorOriginal = ref<any>(null)

const errores = ref({
  nombre: false,
  apellidos: false,
})

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
  monitorOriginal.value = JSON.parse(JSON.stringify(monitor.value))
  Object.keys(errores.value).forEach(
    k => (errores.value[k as keyof typeof errores.value] = false)
  )
  isEditing.value = true
}

function cancelarEdicion() {
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
    await modificarMonitor(monitor.value.id, data)
    isEditing.value = false
  } catch (e) {
    console.error('Error al modificar el monitor', e)
  }
}

const eliminar = async () => {
  try {
    await eliminarMonitor(monitor.value.id)
  } catch (e) {
    console.error("Error al eliminar el monitor", e);
  }
}

function volver() {
  router.back()
}

onMounted(async () => {
  const id = parseInt(props.id)

  try {
    monitor.value = await getMonitor(id)
    monitorOriginal.value = JSON.parse(JSON.stringify(monitor.value))
  } catch (e) {
    console.error('Error al obtener informacion del monitor', e)
  }
})
</script>
