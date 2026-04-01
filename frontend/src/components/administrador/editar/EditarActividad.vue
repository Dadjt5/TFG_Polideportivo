<template>
  <div class="min-vh-100 pt-4" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4" style="max-width: 1600px;">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>
        <h1 class="fw-semibold mb-0 text-primary">{{ actividad.nombre }}</h1>
        <div style="width: 100px"></div>
      </div>

      <!-- CARD PRINCIPAL -->
      <div class="card shadow-lg border-0 rounded-4 p-4"
        style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">

        <!-- NAV DE TABS -->
        <ul class="nav nav-pills nav-fill mb-4">
          <li class="nav-item">
            <button class="nav-link fw-bold" :class="{ active: tab === 1 }" @click="tab = 1">
              {{ t.data }}
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link fw-bold" :class="{ active: tab === 2 }" @click="tab = 2">
              {{ t.images }}
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link fw-bold" :class="{ active: tab === 3 }" @click="tab = 3">
              {{ t.facility }}
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link fw-bold" :class="{ active: tab === 4 }" @click="tab = 4">
              {{ t.monitorTariff }}
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link fw-bold" :class="{ active: tab === 5 }" @click="tab = 5">
              {{ t.sessions }}
            </button>
          </li>
        </ul>


        <!-- TAB 1: DATOS GENERALES -->
        <div v-if="tab === 1" class="row g-4">
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.name }}</label>
            <input type="text" class="form-control form-control-lg" v-model="actividad.nombre" :disabled="!editando"
              :class="{ 'is-invalid': errores.nombre }" />
          </div>

          <div class="col-md-12">
            <label class="form-label fw-semibold">{{ t.description }}</label>
            <textarea rows="3" class="form-control form-control-lg" v-model="actividad.descripcion"
              :disabled="!editando"></textarea>
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.maxPlaces }}</label>
            <input type="number" class="form-control form-control-lg" v-model.number="actividad.plazasMaximas"
              :disabled="!editando" :class="{ 'is-invalid': errores.plazasMaximas }" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.reservedPlaces }}</label>
            <input type="number" class="form-control form-control-lg" v-model.number="actividad.plazasReservadas"
              :disabled="!editando" :class="{ 'is-invalid': errores.plazasReservadas }" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.minimumAge }}</label>
            <input type="number" class="form-control form-control-lg" v-model.number="actividad.edadMinima"
              :disabled="!editando" :class="{ 'is-invalid': errores.edadMinima }" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.credits }}</label>
            <input type="number" class="form-control form-control-lg" v-model.number="actividad.numeroCreditos"
              :disabled="!editando" :class="{ 'is-invalid': errores.numeroCreditos }" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.level }}</label>
            <input type="text" class="form-control form-control-lg" v-model="actividad.nivel" :disabled="!editando" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.material }}</label>
            <input type="text" class="form-control form-control-lg" v-model="actividad.material"
              :disabled="!editando" />
          </div>

          <!-- DEPORTE -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.sport }}</label>
            <select class="form-select form-select-lg" v-model="actividad.deportes" :disabled="!editando"
              :class="{ 'is-invalid': errores.deporte }">
              <option disabled value="">{{ t.selectOption }}</option>
              <option v-for="d in deportes" :key="d.id" :value="d.id">{{ d.titulo }}</option>
            </select>
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.reserveType }}</label>
            <select class="form-select form-select-lg" v-model="actividad.tipoReserva" :disabled="!editando"
              :class="{ 'is-invalid': errores.tipoReserva }">
              <option v-for="r in tiposStore.tiposReserva" :key="r" :value="r">{{ r }}</option>
            </select>
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.terrainType }}</label>
            <select class="form-select form-select-lg" v-model="actividad.terreno" :disabled="!editando"
              :class="{ 'is-invalid': errores.terreno }">
              <option v-for="t in tiposStore.terrenos" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.period }}</label>
            <select class="form-select form-select-lg" v-model="actividad.periodo" :disabled="!editando"
              :class="{ 'is-invalid': errores.periodo }">
              <option v-for="t in tiposStore.periodos" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>

          <div class="col-md-12">
            <div class="form-check form-switch mt-2">
              <input class="form-check-input" type="checkbox" v-model="actividad.exterior" :disabled="!editando" />
              <label class="form-check-label fw-semibold">{{ t.outdoor }}</label>
            </div>
          </div>
          
          <div class="col-md-12">
            <div class="form-check form-switch mt-2">
              <input class="form-check-input" type="checkbox" v-model="actividad.inscripcion" :disabled="!editando" />
              <label class="form-check-label fw-semibold">{{ t.userCanBook }}</label>
            </div>
          </div>
        </div>

        <!-- TAB 2: IMAGEN -->
        <div v-if="tab === 2" class="d-flex justify-content-center">
          <div class="card shadow rounded-4 p-3 text-center"
            style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(8px); max-width: 500px; width: 100%;">

            <h5 class="mb-3 d-flex justify-content-center align-items-center gap-2">
              <i class="bi bi-images text-primary"></i> {{ t.images }}
            </h5>

            <img :src="actividad.imagenURL" class="img-fluid rounded mb-3 img-hover"
              v-if="actividad.imagenURL && !preview" style="max-height: 300px; object-fit: cover;" />

            <input v-if="editando" type="file" class="form-control form-control-lg mt-2" @change="onFileChange" />

            <img v-if="preview" :src="preview" class="img-fluid rounded mt-3"
              style="max-height: 300px; object-fit: cover;" />
          </div>
        </div>

        <!-- TAB 3: INSTALACION -->
        <div v-if="tab === 3">
          <div class="mb-4">
            <label class="form-label fw-semibold">{{ t.facility }}</label>
            <select class="form-select form-select-lg" v-model="actividad.instalacion" :disabled="!editando"
              :class="{ 'is-invalid': errores.instalacion }">
              <option :value="null">--</option>
              <option v-for="i in instalacionesFiltradas" :key="i.id" :value="i.id">{{ i.nombre }}</option>
            </select>
          </div>

          <div class="col-md-4" v-if="callesDisponibles.length > 0">
            <label class="form-label fw-semibold">{{ t.poolStreets }}</label>
            <select class="form-select" v-model="calleSeleccionada" :disabled="!editando">
              <option value="" disabled>--</option>
              <option v-for="c in callesDisponibles" :key="c.id" :value="c.numero">
                {{ t.poolStreet }} {{ c.numero }}
              </option>
            </select>
          </div>

          <div v-if="instalacionSeleccionada?.agenda?.length" class="card border-0 shadow-sm rounded-4 p-4 bg-light">
            <h5 class="fw-bold mb-3">{{ t.weekHours }}</h5>

            <div class="mt-4 mb-2">
              <span class="badge bg-success me-2">{{ t.free }}</span>
              <span class="badge bg-primary me-2">{{ t.selected }}</span>
              <span class="badge bg-warning text-dark">{{ t.activity }}</span>
            </div>

            <div class="row">
              <div v-for="dia in instalacionSeleccionada.agenda" :key="dia.id" class="col-12 mb-3">
                <div class="p-3 rounded-3 bg-white border shadow-sm">

                  <!-- CABECERA CLICKABLE -->
                  <div class="d-flex justify-content-between align-items-center cursor-pointer"
                    @click="toggleDia(dia.id)">
                    <span class="fw-semibold">{{ dia.dia }}</span>
                    <span v-if="!dia.abierto" class="text-danger fw-semibold">{{ t.close }}</span>
                    <span v-else>
                      <i v-if="isOpen(dia.id)" class="bi bi-chevron-up"></i>
                      <i v-else class="bi bi-chevron-down"></i>
                    </span>
                  </div>

                  <!-- DESPLEGABLE DE INTERVALOS -->
                  <transition name="fade">
                    <div v-if="dia.abierto && isOpen(dia.id)" class="mt-2">
                      <div class="d-flex flex-wrap gap-2">
                        <div v-for="intervalo in dia.mapa_reservas" :key="intervalo.id"
                          class="small text-white text-center px-3 py-2 rounded" :class="{
                            'bg-primary': esPropio(intervalo, dia),
                            'bg-warning text-dark': !esPropio(intervalo, dia) && esOcupadoPorPeriodo(intervalo),
                            'bg-success': !esPropio(intervalo, dia) && !esOcupadoPorPeriodo(intervalo)
                          }">
                          {{ intervalo.horaInicio.slice(0, 5) }} - {{ intervalo.horaFin.slice(0, 5) }}
                        </div>
                      </div>
                    </div>
                  </transition>

                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- TAB 4: MONITOR Y TARIFA -->
        <div v-if="tab === 4">

          <div class="mb-4">
            <label class="form-label fw-semibold">{{ t.monitor }}</label>
            <select class="form-select form-select-lg" v-model="actividad.monitor" :disabled="!editando"
              :class="{ 'is-invalid': errores.monitor }">
              <option :value="null">--</option>
              <option v-for="m in monitores" :key="m.id" :value="m.id">{{ m.nombre }}</option>
            </select>

            <div v-if="monitorSeleccionado" class="bg-light rounded-4 p-3 mt-3">
              <strong>{{ t.weeklyWork }}:</strong> {{ monitorSeleccionado.carga }} {{ t.weekHours }}
            </div>
          </div>

          <div>
            <label class="form-label fw-semibold">{{ t.tariff }}</label>
            <select class="form-select form-select-lg" v-model="actividad.tarifa" :disabled="!editando"
              :class="{ 'is-invalid': errores.tarifa }">
              <option :value="null">--</option>
              <option v-for="t in tarifas" :key="t.id" :value="t.id">{{ t.titulo }}</option>
            </select>

            <transition name="fade">
              <div v-if="tarifaSeleccionada" class="mt-4 p-4 bg-white rounded-4 shadow-sm border">
                <h5 class="mb-3 text-primary">{{ t.tariff }}</h5>

                <div v-if="actividad.tipoActividad === 'Otros'" class="row g-3">
                  <div class="col-md-6">
                    <div class="p-3 bg-light rounded-3">
                      <strong>{{ t.priceUAM }}:</strong> {{ tarifaSeleccionada.precioUAM }} €
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="p-3 bg-light rounded-3">
                      <strong>{{ t.priceOthers }}:</strong> {{ tarifaSeleccionada.precioOtros }} €
                    </div>
                  </div>
                  <div class="col-12">
                    <div class="p-3 bg-light rounded-3">
                      <strong>{{ t.weekHours }}:</strong> {{ tarifaSeleccionada.numeroHorasSemana }}
                    </div>
                  </div>
                </div>

                <div v-else-if="actividad.tipoActividad === 'Grupos reducidos'" class="row g-3">
                  <div class="col-md-4">
                    <div class="p-3 bg-light rounded-3">
                      <strong>{{ t.price }}:</strong> {{ tarifaSeleccionada.precio }} €
                    </div>
                  </div>
                  <div class="col-md-4">
                    <div class="p-3 bg-light rounded-3">
                      <strong>{{ t.monthlyPrice }}:</strong> {{ tarifaSeleccionada.precioMensual }} €
                    </div>
                  </div>
                  <div class="col-md-4">
                    <div class="p-3 bg-light rounded-3">
                      <strong>{{ t.quarterPrice }}:</strong> {{ tarifaSeleccionada.precioCuatrimestre }} €
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="p-3 bg-light rounded-3">
                      <strong>{{ t.weekHours }}:</strong> {{ tarifaSeleccionada.numeroHoras }}
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="p-3 bg-light rounded-3">
                      <strong>{{ t.people }}:</strong> {{ tarifaSeleccionada.numeroPersonas }}
                    </div>
                  </div>
                </div>

                <div v-else-if="actividad.tipoActividad === 'Fisioterapia'" class="row g-3 mt-3">
                  <!-- TDA -->
                  <div class="col-md-4">
                    <div class="p-3 bg-light rounded-3 shadow-sm">
                      <h6 class="text-primary">{{ t.priceTDA }}</h6>
                      <p class="mb-1">{{ t.consultationPrice }}: {{ tarifaSeleccionada.precioConsultaTDA }} €</p>
                      <p class="mb-1">{{ t.sessions1to5 }}: {{ tarifaSeleccionada.precioSesiones1_5TDA }} €</p>
                      <p class="mb-1">{{ t.sessions6plus }}: {{ tarifaSeleccionada.precioSesiones6TDA }} €</p>
                    </div>
                  </div>

                  <!-- UAM -->
                  <div class="col-md-4">
                    <div class="p-3 bg-light rounded-3 shadow-sm">
                      <h6 class="text-success">{{ t.priceUAM }}</h6>
                      <p class="mb-1">{{ t.consultationPrice }}: {{ tarifaSeleccionada.precioConsultaUAM }} €</p>
                      <p class="mb-1">{{ t.sessions1to5 }}: {{ tarifaSeleccionada.precioSesiones1_5UAM }} €</p>
                      <p class="mb-1">{{ t.sessions6plus }}: {{ tarifaSeleccionada.precioSesiones6UAM }} €</p>
                    </div>
                  </div>

                  <!-- Others -->
                  <div class="col-md-4">
                    <div class="p-3 bg-light rounded-3 shadow-sm">
                      <h6 class="text-warning">{{ t.priceOthers }}</h6>
                      <p class="mb-1">{{ t.consultationPrice }}: {{ tarifaSeleccionada.precioConsultaOtros }} €</p>
                      <p class="mb-1">{{ t.sessions1to5 }}: {{ tarifaSeleccionada.precioSesiones1_5Otros }} €</p>
                      <p class="mb-1">{{ t.sessions6plus }}: {{ tarifaSeleccionada.precioSesiones6Otros }} €</p>
                    </div>
                  </div>

                  <!-- Información general -->
                  <div class="col-6">
                    <div class="p-3 bg-light rounded-3 shadow-sm">
                      <strong>{{ t.weekHours }}:</strong> {{ tarifaSeleccionada.numeroHoras }}
                    </div>
                  </div>
                  <div class="col-6">
                    <div class="p-3 bg-light rounded-3 shadow-sm">
                      <strong>{{ t.people }}:</strong> {{ tarifaSeleccionada.numeroPersonas }}
                    </div>
                  </div>
                </div>
              </div>
            </transition>
          </div>

        </div>

        <!-- TAB 5: SESIONES -->
        <div v-if="tab === 5">

          <!-- CREAR SESIÓN -->
          <div v-if="editando" class="row g-3 align-items-end mb-4">
            <div class="col-md-4">
              <label class="form-label fw-semibold">{{ t.day }}</label>
              <select class="form-select" v-model="crearSesion.dia">
                <option value="">--</option>
                <option v-for="d in tiposStore.dias" :key="d" :value="d">
                  {{ d }}
                </option>
              </select>
            </div>

            <div class="col-md-3">
              <label class="form-label fw-semibold">{{ t.startHour }}</label>
              <input type="time" class="form-control" v-model="crearSesion.horaInicio" />
            </div>

            <div class="col-md-3">
              <label class="form-label fw-semibold">{{ t.endHour }}</label>
              <input type="time" class="form-control" v-model="crearSesion.horaFin" />
            </div>

            <div class="col-md-2">
              <button class="btn btn-primary w-100" @click="agregarSesion">
                {{ t.newSession }}
              </button>
            </div>
          </div>

          <!-- LISTA DE SESIONES -->
          <div class="row g-3">
            <div v-for="sesion in sesiones" :key="sesion.id" class="col-md-6">
              <div class="card shadow rounded-4 p-3"
                style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(8px);">

                <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">

                  <!-- MODO EDICIÓN -->
                  <template v-if="editando">
                    <div class="d-flex gap-2 flex-wrap align-items-center">

                      <!-- DIA -->
                      <select class="form-select form-select-sm" v-model="sesion.dia" style="width: 130px;">
                        <option v-for="d in tiposStore.dias" :key="d" :value="d">
                          {{ d }}
                        </option>
                      </select>

                      <!-- HORA INICIO -->
                      <input type="time" class="form-control form-control-sm" v-model="sesion.horaInicio"
                        style="width: 120px;" />

                      <!-- HORA FIN -->
                      <input type="time" class="form-control form-control-sm" v-model="sesion.horaFin"
                        style="width: 120px;" />
                    </div>
                  </template>

                  <!-- MODO VISUAL -->
                  <template v-else>
                    <div>
                      <strong>{{ sesion.dia }}</strong> |
                      {{ sesion.horaInicio }} - {{ sesion.horaFin }}
                    </div>
                  </template>

                  <!-- BOTÓN ELIMINAR -->
                  <button v-if="editando" class="btn btn-sm btn-danger" @click="eliminarSesion(sesion.id)">
                    {{ t.delete }}
                  </button>

                </div>
              </div>
            </div>

            <!-- SIN SESIONES -->
            <div v-if="sesiones.length === 0" class="col-12 text-center text-muted mt-3">
              {{ t.noSessions }}
            </div>
          </div>

        </div>
        <div v-if="mostrarMensaje" class="text-center mt-5">
          <div class="alert" :class="tipoMensaje === 'success' ? 'alert-success' : 'alert-danger'">
            {{ mensajeEditar }}
          </div>
        </div>

        <!-- ACCIONES -->
        <div class="d-flex justify-content-center gap-4 mt-5">
          <button v-if="!editando" class="btn btn-primary btn-lg rounded-pill" @click="activarEdicion">
            <i class="bi bi-pencil me-2"></i> {{ t.modifyActivity }}
          </button>

          <template v-else>
            <button class="btn btn-success btn-lg rounded-pill px-5" @click="comprobarAlquiler">
              {{ t.saveChanges }}
            </button>
            <button class="btn btn-secondary btn-lg rounded-pill px-5" @click="cancelarEdicion(true)">
              {{ t.cancel }}
            </button>
          </template>

          <button v-if="!editando" class="btn btn-danger btn-lg rounded-pill" @click="abrirConfirmacion">
            <i class="bi bi-trash me-2"></i> {{ t.deleteActivity }}
          </button>
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
            <p>{{ t.confirmDeleteActivity }}</p>
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

    <div class="modal fade" id="confirmCreateModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4">

          <div class="modal-header">
            <h5 class="modal-title">{{ t.confirmCreate }}</h5>
          </div>

          <div class="modal-body text-center">
            <p>{{ mensajeRevisar }}</p>
          </div>

          <div class="modal-footer justify-content-center">
            <button class="btn btn-secondary rounded-pill" data-bs-dismiss="modal">
              {{ t.cancel }}
            </button>

            <button class="btn btn-primary rounded-pill" @click="guardarCambios">
              {{ t.continue }}
            </button>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted, inject, type Ref, computed } from "vue"
import { useRouter } from "vue-router"
import { Modal } from 'bootstrap'

import { getInstalacionesSimples, getMonitoresSimples, getTarifasActividadComun, getTarifasFisioterapia, getTarifasGrupoReducido, getDeportes } from "@/services/listadoService"
import { eliminarActividad, getActividadDetalle, modificarActividad } from "@/services/detalleService"
import { useTiposStore } from "@/stores/tipos"

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"
import { revisarAlquiler } from "@/services/crearRecursosService"

const props = defineProps<{ id: string }>()

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const router = useRouter()
const tiposStore = useTiposStore()
const tab = ref(1)
const añoActual = new Date().getFullYear()

const actividad = ref<any>({
  nombre: "",
  descripcion: "",
  imagenURL: "",
  plazasMaximas: 0,
  plazasReservadas: 0,
  edadMinima: 0,
  año: añoActual,
  numeroCreditos: 0,
  nivel: "",
  material: "",
  exterior: false,
  inscripcion: false,
  instalacion: null,
  monitor: null,
  tipoActividad: "",
  tarifa: null,
  tipoReserva: "",
  terreno: "",
  estado: "",
  periodo: "",
  nombreDeporte: "",
  deportes: null,
})

const imagen = ref<File | null>(null)
const preview = ref<string | null>(null)
const actividadOriginal = ref<any>(null);
const sesiones = ref<any[]>([])
const crearSesion = ref({ id: -1, dia: "", horaInicio: "", horaFin: "" })
const mensaje = ref("")
const mensajeEditar = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)
const editando = ref(false)
const callesDisponibles = ref<any[]>([])
const calleSeleccionada = ref<number | null>(null)

const errores = ref<any>({
  nombre: false, plazasMaximas: false, plazasReservadas: false, edadMinima: false,
  año: false, numeroCreditos: false, tipoActividad: false, tipoReserva: false,
  terreno: false, instalacion: false, monitor: false, deporte: false,
  tarifa: false, periodo: false
})

function esPropio(intervalo: any, dia: any) {
  return sesiones.value.some(sesion => {
    return (
      sesion.dia === dia.dia &&
      intervalo.horaInicio >= sesion.horaInicio &&
      intervalo.horaFin <= sesion.horaFin
    )
  })
}

function esOcupadoPorPeriodo(intervalo: any) {
  const periodos = intervalo.periodo || []

  if (actividad.value.periodo === "Todo el año") {
    return periodos.length > 0
  }

  return (
    
    periodos.includes(actividad.value.periodo) ||
    periodos.includes("Todo el año")
  )
}

const openDias = ref([])

const toggleDia = (id: any) => {
  if (openDias.value.includes(id)) {
    openDias.value = openDias.value.filter(i => i !== id)
  } else {
    openDias.value.push(id)
  }
}

const isOpen = (id: any) => openDias.value.includes(id)

const monitorSeleccionado = computed(() =>
  monitores.value.find(m => m.id === actividad.value.monitor)
)
const tarifaSeleccionada = computed(() =>
  tarifas.value.find(t => t.id === actividad.value.tarifa)
)
const instalacionSeleccionada = computed(() =>
  instalaciones.value.find(i => i.id === actividad.value.instalacion)
)

const instalaciones = ref<any[]>([])
const monitores = ref<any[]>([])
const tarifas = ref<any[]>([])
const deportes = ref<any[]>([])
const sesionesOriginal = ref<any[]>([])

const instalacionesFiltradas = computed(() => {
  if (!actividad.value.instalacion) return instalaciones.value
  const instalacionActual = instalaciones.value.find(i => i.id === actividad.value.instalacion)
  if (!instalacionActual) return instalaciones.value
  if (instalacionActual.tipoInstalacion === "PISCINA") {
    return instalaciones.value.filter(i => i.tipoInstalacion === "PISCINA")
  } else {
    return instalaciones.value.filter(i => i.tipoInstalacion !== "PISCINA")
  }
})

function activarEdicion() {
  actividadOriginal.value = JSON.parse(JSON.stringify(actividad.value))
  sesionesOriginal.value = JSON.parse(JSON.stringify(sesiones.value))
  Object.keys(errores.value).forEach(k => errores.value[k] = false)
  editando.value = true
}

function cancelarEdicion(eliminarSesiones: boolean) {
  if (eliminarSesiones) {
    sesiones.value = JSON.parse(JSON.stringify(sesionesOriginal.value))
  }

  actividadOriginal.value = JSON.parse(JSON.stringify(actividad.value))
  preview.value = null
  imagen.value = null
  editando.value = false
}

function agregarSesion() {
  if (!crearSesion.value.dia ||
    !crearSesion.value.horaInicio ||
    !crearSesion.value.horaFin ||
    (callesDisponibles.value.length > 0 && !calleSeleccionada.value)) {
    mensaje.value = t.value.selectLane
    return
  }

  sesiones.value.push({
    ...crearSesion.value,
    calle: calleSeleccionada.value || null
  })

  crearSesion.value = { id: -1, dia: "", horaInicio: "", horaFin: "" }
  calleSeleccionada.value = null
}

function eliminarSesion(id: number) {
  sesiones.value = sesiones.value.filter(s => s.id !== id)
}

const mensajeRevisar = ref("")

const comprobarAlquiler = async () => {
  if (!validarFormulario()) {
    lanzarMensaje(t.value.missing, "error")
    return
  }

  if (sesiones.value.length === 0) {
    lanzarMensaje(t.value.noSessionWarning, "error")
    return
  }

  if (!horasValidas()) {
    lanzarMensaje(t.value.wrongTimetable, "error")
    return
  }

  if (!horasEnPunto()) {
    lanzarMensaje(t.value.onTheHourWarning, "error")
    return
  }

  const formData = new FormData()

  formData.append("sesiones", JSON.stringify(sesiones.value))
  formData.append("periodo", actividad.value.periodo)

  const respuesta = await revisarAlquiler(actividad.value.instalacion, formData)

  if (!respuesta?.conflicto) {
    mensajeRevisar.value = "No hay conflictos con alquileres existentes."
    confirmCreationModal.show()
    return
  }

  const usuarios = respuesta.usuarios_afectados
  const alquileres = respuesta.alquileres_afectados
  const dinero = respuesta.dinero_a_devolver

  mensajeRevisar.value = `Esta acción afectará a ${alquileres} alquiler${alquileres !== 1 ? 'es' : ''} existente${alquileres !== 1 ? 's' : ''}:
  de ${usuarios} usuario${usuarios !== 1 ? 's' : ''}
  y se devolveran ${dinero} €
  ¿Deseas continuar?`

  confirmCreationModal.show()
}

let confirmCreationModal: Modal
let confirmModal: Modal
let successModal: Modal

const eliminado = ref(false)

function abrirConfirmacion() {
  confirmModal.show()
}

async function confirmarEliminar() {
  try {
    await eliminarActividad(actividad.value.id)

    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.activityDeleted
    eliminado.value = true
  } catch (e) {
    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.activityNoDeleted
    eliminado.value = false
    console.error("Error al eliminar la actividad", e);
  }
}

const finalizar = async () => {
  if (eliminado.value) {
    router.push({ name: 'gestion-actividades' });
  } else {
    successModal.hide()
    eliminado.value = false
  }
}

function volver() { router.back() }

function validarFormulario() {
  let ok = true
  errores.value.nombre = actividad.value.nombre === ""
  errores.value.plazasMaximas = actividad.value.plazasMaximas <= 0
  errores.value.plazasReservadas = actividad.value.plazasReservadas < 0 || actividad.value.plazasReservadas > actividad.value.plazasMaximas
  errores.value.edadMinima = actividad.value.edadMinima <= 0
  errores.value.año = actividad.value.año < añoActual
  errores.value.numeroCreditos = actividad.value.numeroCreditos < 0
  errores.value.tipoActividad = actividad.value.tipoActividad === ""
  errores.value.tipoReserva = actividad.value.tipoReserva === ""
  errores.value.terreno = actividad.value.terreno === ""
  errores.value.periodo = actividad.value.periodo === ""
  errores.value.instalacion = actividad.value.instalacion === null
  errores.value.monitor = actividad.value.monitor === null
  errores.value.tarifa = actividad.value.tarifa === null
  errores.value.deporte = actividad.value.nombreDeporte.value === ""
  for (const k in errores.value) if (errores.value[k]) ok = false
  return ok
}

function horasValidas() {
  for (const s of sesiones.value) {
    if (s.horaInicio >= s.horaFin) {
      return false
    }
  }
  return true
}

function horasEnPunto() {
  for (const s of sesiones.value) {
    const [hIni, mIni] = s.horaInicio.split(":").map(Number)
    const [hFin, mFin] = s.horaFin.split(":").map(Number)

    if (mIni !== 0 || mFin !== 0) return false
  }
  return true
}

function limpiarHora(h: string) {
  return h ? h.slice(0, 5) : h
}

function validarTipoInstalacion() {
  const inst = instalaciones.value.find(i => i.id === actividad.value.instalacion)
  if (!inst) return false

  const instOriginal = instalaciones.value.find(i => i.id === actividadOriginal.value.instalacion)
  if (!instOriginal) return false

  // Si el tipo es piscina no puede ser otro y viceversa
  if (inst.tipoInstalacion == "PISCINA" && instOriginal.tipoInstalacion != "PISCINA") {
    return false;
  }

  if (inst.tipoInstalacion != "PISCINA" && instOriginal.tipoInstalacion == "PISCINA") {
    return false
  }

  return true
}

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensajeEditar.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true

  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
}

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  if (!input.files || input.files.length === 0) return

  imagen.value = input.files[0]
  preview.value = URL.createObjectURL(imagen.value)
}

async function guardarCambios() {
  confirmCreationModal.hide()

  if (!validarFormulario()) {
    lanzarMensaje(t.value.missing, "error")
    return
  }

  if (!validarTipoInstalacion()) {
    lanzarMensaje(t.value.cannotChangeType, "error")
    return
  }

  if (!horasValidas()) {
    lanzarMensaje(t.value.wrongTimetable, "error")
    return
  }

  if (!horasEnPunto()) {
    lanzarMensaje(t.value.onTheHourWarning, "error")
    return
  }

  sesiones.value = sesiones.value.map(s => ({
    ...s,
    horaInicio: limpiarHora(s.horaInicio),
    horaFin: limpiarHora(s.horaFin)
  }))

  const formData = new FormData()

  formData.append("actividad", JSON.stringify(actividad.value))
  formData.append("sesiones", JSON.stringify(sesiones.value))
  formData.append("deportes", JSON.stringify(actividad.value.nombreDeporte))

  if (imagen.value) {
    formData.append("imagenURL", imagen.value)
  }

  try {
    await modificarActividad(parseInt(props.id), formData)
    lanzarMensaje(t.value.correctlyUpdate, "success")
    cancelarEdicion(false)
  } catch (e) {
    lanzarMensaje(t.value.noModify, "error")
    console.error("No se ha podido editar la actividad", e)
  }
}

onMounted(async () => {
  const id = parseInt(props.id);

  confirmCreationModal = new Modal(document.getElementById('confirmCreateModal')!)
  confirmModal = new Modal(document.getElementById('confirmDeleteModal')!)
  successModal = new Modal(document.getElementById('successDeleteModal')!)

  try {
    const data = await getActividadDetalle(id);
    actividad.value = data;
    sesiones.value = data.sesiones
    actividadOriginal.value = JSON.parse(JSON.stringify(actividad.value))

    instalaciones.value = await getInstalacionesSimples()
    monitores.value = await getMonitoresSimples()
    deportes.value = await getDeportes()

    if (actividad.value.tipoActividad === "Otros") {
      tarifas.value = await getTarifasActividadComun()
    } else if (actividad.value.tipoActividad === "Grupos reducidos") {
      tarifas.value = await getTarifasGrupoReducido()
    } else if (actividad.value.tipoActividad === "Fisioterapia") {
      tarifas.value = await getTarifasFisioterapia()
    }
  } catch (e: any) {
    mensaje.value = t.value.unexpectedError
    console.log("Error al obtener la informacion de la actividad", e);
  }
});
</script>