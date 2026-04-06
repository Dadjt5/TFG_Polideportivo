<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #fff4e0, #e0f7ff);">
    <main class="container py-5" style="max-width: 1120px;">
      <h1 class="text-center fw-bold mb-5 text-primary">
        {{ t.newActivity }}
      </h1>

      <div class="card shadow-lg border-0 rounded-4 p-4"
        style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">

        <!-- TABS -->
        <ul class="nav nav-tabs nav-fill mb-4">
          <li class="nav-item">
            <button type="button" class="nav-link" :class="{ active: tab === 1 }" @click="tab = 1">
              {{ t.data }}
            </button>
          </li>

          <li class="nav-item">
            <button type="button" class="nav-link" :class="{ active: tab === 2 }" @click="tab = 2">
              {{ t.facility }}
            </button>
          </li>

          <li class="nav-item">
            <button type="button" class="nav-link" :class="{ active: tab === 3 }" @click="tab = 3">
              {{ t.monitorTariff }}
            </button>
          </li>

          <li class="nav-item">
            <button type="button" class="nav-link" :class="{ active: tab === 4 }" @click="tab = 4">
              {{ t.sessions }}
            </button>
          </li>
        </ul>

        <!-- TAB 1 DATOS -->
        <div v-if="tab === 1" class="row g-4">
          <!-- NOMBRE -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.name }}</label>
            <input type="text" class="form-control form-control-lg" :class="{ 'is-invalid': errores.nombre }"
              v-model="actividad.nombre" />
          </div>

          <!-- DESCRIPCIÓN -->
          <div class="col-md-12">
            <label class="form-label fw-semibold">{{ t.description }}</label>
            <textarea rows="3" class="form-control form-control-lg" v-model="actividad.descripcion" />
          </div>

          <!-- IMAGEN -->
          <div class="col-md-12">
            <label class="form-label fw-semibold">{{ t.images }}</label>

            <input type="file" class="form-control form-control-lg" accept="image/*" @change="onFileChange" />

            <!-- preview -->
            <img v-if="preview" :src="preview" class="mt-3 rounded" style="max-width:250px" />
          </div>

          <!-- PLAZAS -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.maxPlaces }}</label>
            <input type="number" class="form-control form-control-lg" :class="{ 'is-invalid': errores.plazasMaximas }"
              v-model.number="actividad.plazasMaximas" />
          </div>

          <!-- PLAZAS RESERVADAS -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.reservedPlaces }}</label>
            <input type="number" class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.plazasReservadas }" v-model.number="actividad.plazasReservadas" />
          </div>

          <!-- EDAD MINIMA -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.minimumAge }}</label>
            <input type="number" class="form-control form-control-lg" :class="{ 'is-invalid': errores.edadMinima }"
              v-model.number="actividad.edadMinima" />
          </div>

          <!-- CRÉDITOS -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.credits }}</label>
            <input type="number" class="form-control form-control-lg" :class="{ 'is-invalid': errores.numeroCreditos }"
              v-model.number="actividad.numeroCreditos" />
          </div>

          <!-- NIVEL -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.level }}</label>
            <input type="text" class="form-control form-control-lg" v-model="actividad.nivel" />
          </div>

          <!-- MATERIAL -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.material }}</label>
            <input type="text" class="form-control form-control-lg" v-model="actividad.material" />
          </div>

          <!-- DEPORTE -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.sport }}</label>

            <select class="form-select form-select-lg" v-model="deporteSeleccionado"
              :class="{ 'is-invalid': errores.deporte }">
              <option disabled value="">{{ t.selectOption }}</option>

              <option v-for="d in deportes" :key="d.id" :value="d.titulo">
                {{ d.titulo }}
              </option>

              <option value="nuevo">+ {{ t.newSport }}</option>
            </select>
          </div>

          <div v-if="deporteSeleccionado === 'nuevo'" class="mt-3">
            <input type="text" class="form-control form-control-lg" v-model="nuevoDeporteNombre"
              :placeholder="t.title" />
          </div>

          <!-- TIPO ACTIVIDAD -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.activityType }}</label>
            <select class="form-select form-select-lg" :class="{ 'is-invalid': errores.tipoActividad }"
              v-model="actividad.tipoActividad">
              <option v-for="t in tiposStore.tiposActividad" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>

          <!-- RESERVA -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.reserveType }}</label>
            <select class="form-select form-select-lg" :class="{ 'is-invalid': errores.tipoReserva }"
              v-model="actividad.tipoReserva">
              <option v-for="r in tiposStore.tiposReserva" :key="r" :value="r">{{ r }}</option>
            </select>
          </div>

          <!-- TERRENO -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.terrainType }}</label>
            <select class="form-select form-select-lg" :class="{ 'is-invalid': errores.terreno }"
              v-model="actividad.terreno">
              <option v-for="t in tiposStore.terrenos" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>

          <!-- PERIODO -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.period }}</label>
            <select class="form-select form-select-lg" :class="{ 'is-invalid': errores.periodo }"
              v-model="actividad.periodo">
              <option v-for="t in tiposStore.periodos" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>


          <!-- EXTERIOR -->
          <div class="col-md-12">
            <div class="form-check form-switch mt-2">
              <input class="form-check-input" type="checkbox" v-model="actividad.exterior" />
              <label class="form-check-label fw-semibold">
                {{ t.outdoor }}
              </label>
            </div>
          </div>

          <div class="col-md-12">
            <div class="form-check form-switch mt-2">
              <input class="form-check-input" type="checkbox" v-model="actividad.inscripcion" />
              <label class="form-check-label fw-semibold">
                {{ t.userCanBook }}
              </label>
            </div>
          </div>
        </div>


        <!-- TAB 2 INSTALACION -->
        <div v-if="tab === 2">

          <div class="mb-4">
            <label class="form-label fw-semibold">{{ t.facility }}</label>
            <select class="form-select form-select-lg" :class="{ 'is-invalid': errores.instalacion }"
              v-model="actividad.instalacion">
              <option :value="null">--</option>
              <option v-for="i in instalaciones" :key="i.id" :value="i.id">
                {{ i.nombre }}
              </option>
            </select>
          </div>

          <div class="col-md-4 mb-3" v-if="callesDisponibles.length > 0">
            <label class="form-label fw-semibold">{{ t.poolStreets }}</label>
            <select class="form-select form-select-lg" v-model="calleSeleccionada">
              <option v-for="c in callesDisponibles" :key="c.id" :value="c.id">
                {{ t.street }} {{ c.numero || c.id }}
              </option>
            </select>
          </div>

          <!-- HORARIO -->
          <div v-if="instalacionSeleccionada?.agenda?.length" class="card border-0 shadow-sm rounded-4 p-4 bg-light">
            <h5 class="fw-bold mb-3">
              {{ t.weekHours }}
            </h5>

            <!-- LEYENDA -->
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
                        <div v-for="intervalo in filtrarIntervalos(dia.mapa_reservas)" :key="intervalo.id"
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

        <!-- TAB 3 MONITOR Y TARIFA -->
        <div v-if="tab === 3">

          <div class="mb-4">
            <label class="form-label fw-semibold">{{ t.monitor }}</label>
            <select class="form-select form-select-lg" :class="{ 'is-invalid': errores.monitor }"
              v-model="actividad.monitor">
              <option :value="null">--</option>
              <option v-for="m in monitores" :key="m.id" :value="m.id">
                {{ m.nombre }}
              </option>
            </select>

            <div v-if="monitorSeleccionado" class="bg-light rounded-4 p-3 mt-3">
              <strong>{{ t.weeklyWork }}:</strong>
              {{ monitorSeleccionado.carga }} {{ t.weekHours }}
            </div>
          </div>

          <div>
            <label class="form-label fw-semibold">{{ t.tariff }}</label>
            <select class="form-select form-select-lg" :class="{ 'is-invalid': errores.tarifa }"
              v-model="actividad.tarifa">
              <option :value="null">--</option>
              <option v-for="t in tarifas" :key="t.id" :value="t.id">
                {{ t.titulo }}
              </option>
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

        <!-- TAB 4 SESIONES -->
        <div v-if="tab === 4">
          <div class="row g-3 align-items-end mb-4">
            <div class="col-md-2" v-if="callesDisponibles.length > 0">
              <label class="form-label fw-semibold">{{ t.poolStreets }}</label>
              <select class="form-select form-select-lg" v-model="calleSeleccionada">
                <option value="">--</option>
                <option v-for="c in callesDisponibles" :key="c.id" :value="c.id">
                  {{ t.street }} {{ c.numero || c.id }}
                </option>
              </select>
            </div>

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
              <button type="button" class="btn btn-primary w-100" @click="agregarSesion">
                {{ t.newSession }}
              </button>
            </div>

          </div>

          <div v-if="sesiones.length" class="bg-light rounded-4 p-3">

            <div v-for="(s, index) in sesiones" :key="index"
              class="d-flex justify-content-between align-items-center mb-2">

              <span>
                {{ s.dia }} | {{ s.horaInicio }} - {{ s.horaFin }} <span
                  v-if="instalacionSeleccionada.tipoInstalacion === 'Piscina'">{{ t.street }} {{ s.calle }}</span>
              </span>

              <button type="button" class="btn btn-sm btn-danger" @click="sesiones.splice(index, 1)">
                X
              </button>
            </div>
          </div>
        </div>
        <div class="text-center mt-5 fs-5">
          <p v-if="mensaje" class="text-danger">{{ mensaje }}</p>
        </div>

        <div v-if="mostrarMensaje" class="text-center mt-3 mb-3">
          <div class="alert" :class="tipoMensaje === 'success' ? 'alert-success' : 'alert-danger'">
            {{ mensajeEditar }}
          </div>
        </div>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-4">
          <button class="btn btn-success btn-lg px-5 rounded-pill shadow-sm" @click="comprobarAlquiler">
            {{ t.createActivity }}
          </button>
          <button class="btn btn-outline-secondary btn-lg px-5 rounded-pill shadow-sm" @click="volver">
            {{ t.return }}
          </button>
        </div>
      </div>
    </main>

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

            <button class="btn btn-primary rounded-pill" @click="crearActividad">
              {{ t.continue }}
            </button>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { watch, inject, type Ref, ref, onMounted, computed } from "vue"
import { useRouter } from "vue-router"
import { Modal } from 'bootstrap'

import { nuevaActividad, revisarAlquiler } from "@/services/crearRecursosService"
import { getInstalacionesSimples, getMonitoresSimples, getTarifasActividadComun, getTarifasFisioterapia, getTarifasGrupoReducido, getDeportes } from "@/services/listadoService"

import { useTiposStore } from "@/stores/tipos"

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const tiposStore = useTiposStore();

const router = useRouter()
const añoActual = new Date().getFullYear()

const tab = ref(1)

const actividad = ref({
  nombre: "",
  descripcion: "",
  edadMinima: 18,
  plazasMaximas: 50,
  plazasReservadas: 0,
  año: añoActual,
  numeroCreditos: 0,
  nivel: "",
  material: "",
  exterior: false,
  inscripcion: true,
  instalacion: null,
  monitor: null,
  tipoActividad: "Otros",
  tarifa: null,
  tipoReserva: "",
  terreno: "",
  estado: "",
  periodo: "Todo el año",
})

const errores = ref({
  nombre: false,
  plazasMaximas: false,
  plazasReservadas: false,
  edadMinima: false,
  año: false,
  numeroCreditos: false,
  tipoActividad: false,
  tipoReserva: false,
  terreno: false,
  instalacion: false,
  monitor: false,
  deporte: false,
  tarifa: false,
  periodo: false
})

const mensaje = ref("")
const mensajeRevisar = ref("")
const instalaciones = ref<any[]>([])
const monitores = ref<any[]>([])
const tarifas = ref<any[]>([])
const deportes = ref<any[]>([])

const imagen = ref<File | null>(null)
const preview = ref<string | null>(null)
const deporteSeleccionado = ref("")
const nuevoDeporteNombre = ref("")
const callesDisponibles = ref<any[]>([])
const calleSeleccionada = ref<number | null>(null)

const mensajeEditar = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)

const sesiones = ref<any[]>([])
const crearSesion = ref({ id: -1, dia: "", horaInicio: "", horaFin: "", calle: null })

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

function esPropio(intervalo: any, dia: any) {
  return sesiones.value.some(sesion => {
    return (
      sesion.calle === intervalo.calle &&
      sesion.dia === dia.dia &&
      intervalo.horaInicio >= sesion.horaInicio &&
      intervalo.horaFin <= sesion.horaFin
    )
  })
}

function filtrarIntervalos(intervalos: any) {
  if (instalacionSeleccionada.value.tipoInstalacion !== 'Piscina') {
    return intervalos
  }

  return intervalos.filter(i => i.calle === calleSeleccionada.value)
}

const monitorSeleccionado = computed(() =>
  monitores.value.find(m => m.id === actividad.value.monitor)
)

const tarifaSeleccionada = computed(() =>
  tarifas.value.find(t => t.id === actividad.value.tarifa)
)

const instalacionSeleccionada = computed(() =>
  instalaciones.value.find(i => i.id === actividad.value.instalacion)
)

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  if (!input.files || input.files.length === 0) return

  imagen.value = input.files[0]
  preview.value = URL.createObjectURL(imagen.value)
}

function agregarSesion() {
  if (!crearSesion.value.dia ||
    !crearSesion.value.horaInicio ||
    !crearSesion.value.horaFin ||
    (instalacionSeleccionada.value.tipoInstalacion === 'Piscina' && !crearSesion.value.calle)) {
    lanzarMensaje(t.value.missing, "error")
    return
  }

  sesiones.value.push({ ...crearSesion.value })

  crearSesion.value = { id: -1, dia: "", horaInicio: "", horaFin: "", calle: null }
}

let confirmModal: Modal

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
    confirmModal.show()
    return
  }

  const usuarios = respuesta.usuarios_afectados
  const alquileres = respuesta.alquileres_afectados
  const dinero = respuesta.dinero_a_devolver

  mensajeRevisar.value = `Esta acción afectará a ${alquileres} alquiler${alquileres !== 1 ? 'es' : ''} existente${alquileres !== 1 ? 's' : ''}:
  de ${usuarios} usuario${usuarios !== 1 ? 's' : ''}
  y se devolveran ${dinero} €
  ¿Deseas continuar?`

  confirmModal.show()
}

function validarFormulario() {
  let ok = true

  errores.value.nombre = actividad.value.nombre === ""
  errores.value.plazasMaximas = actividad.value.plazasMaximas <= 0
  errores.value.plazasReservadas =
    actividad.value.plazasReservadas < 0 ||
    actividad.value.plazasReservadas > actividad.value.plazasMaximas
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
  errores.value.deporte =
    deporteSeleccionado.value === "" || (deporteSeleccionado.value === "nuevo" && nuevoDeporteNombre.value === "")

  for (const k in errores.value) {
    if (errores.value[k]) {
      ok = false
    }
  }

  return ok
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

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensajeEditar.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true

  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
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

const crearActividad = async () => {
  confirmModal.hide()

  if (!validarFormulario()) {
    lanzarMensaje(t.value.missing, "error")
    return
  }

  if (actividad.value.plazasMaximas > instalacionSeleccionada.value.aforoMaximo) {
    lanzarMensaje(t.value.errorPlaces, "error")
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

  formData.append("actividad", JSON.stringify(actividad.value))
  formData.append("sesiones", JSON.stringify(sesiones.value))
  formData.append("periodo", actividad.value.periodo)

  const deporteFinal =
    deporteSeleccionado.value === "nuevo"
      ? nuevoDeporteNombre.value
      : deporteSeleccionado.value
  formData.append("deportes", JSON.stringify(deporteFinal))

  if (imagen.value) {
    formData.append("imagen", imagen.value)
  }

  try {
    await nuevaActividad(formData)
    router.push({ name: "gestion-actividades" })
  } catch (e) {
    lanzarMensaje(t.value.noModifyActivity, "error")
    console.log("Error al crear la actividad", e)
  }
}

const volver = () => router.back()

watch(
  () => actividad.value.tipoActividad,
  async (nuevoTipo: string) => {
    actividad.value.tarifa = null
    if (!nuevoTipo) {
      tarifas.value = []
      return
    }

    if (nuevoTipo === "Otros") {
      tarifas.value = await getTarifasActividadComun()
    } else if (nuevoTipo === "Grupos reducidos") {
      tarifas.value = await getTarifasGrupoReducido()
    } else if (nuevoTipo === "Fisioterapia") {
      tarifas.value = await getTarifasFisioterapia()
    }
  }
)

watch(instalacionSeleccionada, (nuevaInstalacion) => {
  if (!nuevaInstalacion || !nuevaInstalacion.calles?.length) {
    callesDisponibles.value = []
    calleSeleccionada.value = null
    return
  }

  callesDisponibles.value = nuevaInstalacion.calles
  calleSeleccionada.value = null
})

onMounted(async () => {
  confirmModal = new Modal(document.getElementById('confirmCreateModal')!)

  instalaciones.value = await getInstalacionesSimples()
  monitores.value = await getMonitoresSimples()
  tarifas.value = await getTarifasActividadComun()
  deportes.value = await getDeportes()
})
</script>