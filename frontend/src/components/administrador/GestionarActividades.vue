<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container py-5" style="max-width: 1100px">
      <h1 class="fw-bold text-primary mb-4 text-center">
        <i class="bi bi-gear-fill me-2"></i>
        {{ t.manageActivities }}
      </h1>

      <div class="card shadow-lg border-0 rounded-4"
           style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">
        <div class="card-body p-4">

          <!-- TABS -->
          <ul class="nav nav-tabs mb-4">
            <li class="nav-item">
              <button
                class="nav-link"
                :class="{ active: tab === 'actividades' }"
                @click="tab = 'actividades'"
              >
                <i class="bi bi-calendar-event me-1"></i>
                {{ t.activities }}
              </button>
            </li>
            <li class="nav-item">
              <button
                class="nav-link"
                :class="{ active: tab === 'deportes' }"
                @click="tab = 'deportes'"
              >
                <i class="bi bi-trophy me-1"></i>
                {{ t.sports }}
              </button>
            </li>
          </ul>

          <!-- ACTIVIDADES -->
          <div v-if="tab === 'actividades'">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="fw-semibold text-success">
                {{ t.activities }}
              </h5>
              <router-link to="/crear/actividad" class="btn btn-primary rounded-pill shadow-sm">
                <i class="bi bi-plus-lg me-1"></i> {{ t.newActivity }}
              </router-link>
            </div>

            <div class="mb-4">
              <div class="input-group shadow-sm">
                <span class="input-group-text bg-white">
                  <i class="bi bi-search"></i>
                </span>
                <input
                  type="text"
                  class="form-control"
                  :placeholder="t.searchActivities"
                  v-model="searchActividad"
                />
              </div>
            </div>

            <div class="text-center mt-5 fs-5">
              <p v-if="mensaje" class="text-danger">{{ mensaje }}</p>
            </div>

            <div class="list-group list-group-flush">
              <div
                v-for="a in actividadesFiltradas"
                :key="a.id"
                class="list-group-item d-flex justify-content-between align-items-center rounded-3 mb-2 shadow-sm border-0"
                @click="actividadDetail(a.id)"
                style="cursor:pointer; background-color: rgba(255,255,255,0.9);"
              >
                <span class="fw-medium text-primary">
                  {{ a.nombre }}
                </span>
              </div>
            </div>
          </div>

          <!-- DEPORTES -->
          <div v-if="tab === 'deportes'">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="fw-semibold text-success">
                {{ t.sports }}
              </h5>
              <button
                class="btn btn-primary rounded-pill shadow-sm"
                @click="abrirModalCrear"
              >
                <i class="bi bi-plus-lg me-1"></i> {{ t.newSport }}
              </button>
            </div>

            <div class="mb-4">
              <div class="input-group shadow-sm">
                <span class="input-group-text bg-white">
                  <i class="bi bi-search"></i>
                </span>
                <input
                  type="text"
                  class="form-control"
                  placeholder="Buscar deporte..."
                  v-model="searchDeporte"
                />
              </div>
            </div>

            <div class="text-center mt-5 fs-5">
              <p v-if="mensaje" class="text-danger">{{ mensaje }}</p>
            </div>

            <div class="list-group list-group-flush">
              <div
                v-for="d in deportesFiltrados"
                :key="d.id"
                class="list-group-item d-flex justify-content-between align-items-center rounded-3 mb-2 shadow-sm border-0"
                style="background-color: rgba(255,255,255,0.9);"
              >
                <span class="fw-medium text-primary">
                  {{ d.titulo }}
                </span>

                <div class="d-flex gap-2">
                  <button
                    class="btn btn-sm btn-outline-secondary rounded-pill"
                    @click="abrirModalEditar(d)"
                  >
                    <i class="bi bi-pencil"></i>
                  </button>

                  <button
                    class="btn btn-sm btn-outline-danger rounded-pill"
                    @click="borrarDeporte(d.id)"
                  >
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>

    <div
      class="modal fade show"
      tabindex="-1"
      v-if="mostrarModal"
      style="display:block; background: rgba(0,0,0,0.4)"
    >
      <div class="modal-dialog">
        <div class="modal-content rounded-4 border-0 shadow-lg">

          <div class="modal-header">
            <h5 class="modal-title fw-semibold">
              {{ modoEdicion ? t.modifySport : t.newSport }}
            </h5>
            <button type="button" class="btn-close" @click="cerrarModal"></button>
          </div>

          <div class="modal-body">
            <label class="form-label fw-semibold">{{ t.title }}</label>
            <input
              type="text"
              class="form-control rounded-3"
              v-model="nombreDeporte"
              placeholder="Ej: Pádel"
              @keyup.enter="guardarDeporte"
            />
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary rounded-pill" @click="cerrarModal">
              {{ t.cancel }}
            </button>
            <button
              class="btn btn-primary rounded-pill"
              @click="guardarDeporte"
              :disabled="!nombreDeporte.trim()"
            >
              {{ t.saveChanges }}
            </button>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed, inject, type Ref } from "vue"
import { useRouter } from "vue-router"

import { getActividadesSimples, getDeportes } from "@/services/listadoService"
import { modificarDeporte, eliminarDeporte } from "@/services/detalleService"
import { nuevoDeporte } from "@/services/crearRecursosService"

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const router = useRouter()

const tab = ref<"actividades" | "deportes">("actividades")

const mensaje = ref("")
const searchActividad = ref("")
const actividades = ref<any[]>([])

const actividadesFiltradas = computed(() =>
  actividades.value.filter(a =>
    a.nombre.toLowerCase().includes(searchActividad.value.toLowerCase())
  )
)

const actividadDetail = (id: number) => {
  router.push({
    name: "editar-actividad",
    params: { id }
  })
}

const searchDeporte = ref("")
const deportes = ref<any[]>([])

const deportesFiltrados = computed(() =>
  deportes.value.filter(d =>
    d.titulo.toLowerCase().includes(searchDeporte.value.toLowerCase())
  )
)

const mostrarModal = ref(false)
const modoEdicion = ref(false)
const nombreDeporte = ref("")
const deporteEditandoId = ref<number | null>(null)

const abrirModalCrear = () => {
  mensaje.value = ""
  modoEdicion.value = false
  nombreDeporte.value = ""
  deporteEditandoId.value = null
  mostrarModal.value = true
}

const abrirModalEditar = (deporte: any) => {
  mensaje.value = ""
  modoEdicion.value = true
  nombreDeporte.value = deporte.titulo
  deporteEditandoId.value = deporte.id
  mostrarModal.value = true
}

const cerrarModal = () => {
  mostrarModal.value = false
}

const guardarDeporte = async () => {
  mensaje.value = ""
  if (!nombreDeporte.value.trim()) return

  if (modoEdicion.value && deporteEditandoId.value !== null) {
    await modificarDeporte(deporteEditandoId.value, {
      titulo: nombreDeporte.value.toLowerCase()
    })
  } else {
    await nuevoDeporte({
      titulo: nombreDeporte.value.toLowerCase()
    })
  }

  deportes.value = await getDeportes()
  cerrarModal()
}

const borrarDeporte = async (id: number) => {
  try {
    mensaje.value = ""
    await eliminarDeporte(id)
    deportes.value = await getDeportes()
  } catch(e: any) {
    mensaje.value = e.response?.data?.respuesta
    console.log("Error al eliminar el deporte", e)    
  }
}

onMounted(async () => {
  try {
    actividades.value = await getActividadesSimples()
    deportes.value = await getDeportes()
  } catch (e: any) {
    mensaje.value = e.response?.data?.respuesta
    console.log("Error al cargar las actividades y/o los deportes", e)
  }
})
</script>