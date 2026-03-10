<template>
  <div class="min-vh-100 pt-4" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4" style="max-width: 1600px;">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>
        <h1 class="fw-semibold mb-0">{{ actividad.nombre }}</h1>
        <div style="width: 100px"></div>
      </div>

      <div class="card border-0 shadow-lg rounded-4 p-4">

        <!-- TABS -->
        <ul class="nav nav-tabs nav-fill mb-4">
          <li class="nav-item">
            <button type="button" class="nav-link" :class="{ active: tab === 1 }" @click="tab = 1">
              {{ t.data }}
            </button>
          </li>
          <li class="nav-item">
            <button type="button" class="nav-link" :class="{ active: tab === 2 }" @click="tab = 2">
              {{ t.images }}
            </button>
          </li>
          <li class="nav-item">
            <button type="button" class="nav-link" :class="{ active: tab === 3 }" @click="tab = 3">
              {{ t.facility }}
            </button>
          </li>
          <li class="nav-item">
            <button type="button" class="nav-link" :class="{ active: tab === 4 }" @click="tab = 4">
              {{ t.monitorTariff }}
            </button>
          </li>
          <li class="nav-item">
            <button type="button" class="nav-link" :class="{ active: tab === 5 }" @click="tab = 5">
              {{ t.sessions }}
            </button>
          </li>
        </ul>

        <!-- TAB 1: DATOS GENERALES -->
        <div v-if="tab === 1" class="row g-4">
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.name }}</label>
            <input type="text" class="form-control form-control-lg" v-model="actividad.nombre"
              :class="{ 'is-invalid': errores.nombre }" />
          </div>

          <div class="col-md-12">
            <label class="form-label fw-semibold">{{ t.description }}</label>
            <textarea rows="3" class="form-control form-control-lg" v-model="actividad.descripcion"></textarea>
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.maxPlaces }}</label>
            <input type="number" class="form-control form-control-lg" v-model.number="actividad.plazasMaximas"
              :class="{ 'is-invalid': errores.plazasMaximas }" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.reservedPlaces }}</label>
            <input type="number" class="form-control form-control-lg" v-model.number="actividad.plazasReservadas"
              :class="{ 'is-invalid': errores.plazasReservadas }" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.minimumAge }}</label>
            <input type="number" class="form-control form-control-lg" v-model.number="actividad.edadMinima"
              :class="{ 'is-invalid': errores.edadMinima }" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.credits }}</label>
            <input type="number" class="form-control form-control-lg" v-model.number="actividad.numeroCreditos"
              :class="{ 'is-invalid': errores.numeroCreditos }" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.level }}</label>
            <input type="text" class="form-control form-control-lg" v-model="actividad.nivel" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.material }}</label>
            <input type="text" class="form-control form-control-lg" v-model="actividad.material" />
          </div>

          <!-- DEPORTE -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.sport }}</label>
            <select class="form-select form-select-lg" v-model="actividad.nombreDeporte"
              :class="{ 'is-invalid': errores.deporte }">
              <option disabled value="">{{ t.selectOption }}</option>
              <option v-for="d in deportes" :key="d.id" :value="d.id">{{ d.titulo }}</option>
              <option value="nuevo">+ {{ t.newSport }}</option>
            </select>
          </div>

          <div v-if="actividad.nombreDeporte === 'nuevo'" class="mt-3 col-md-6">
            <input type="text" class="form-control form-control-lg" v-model="actividad.nombreDeporte"
              :placeholder=t.title />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.reserveType }}</label>
            <select class="form-select form-select-lg" v-model="actividad.tipoReserva"
              :class="{ 'is-invalid': errores.tipoReserva }">
              <option v-for="r in tiposStore.tiposReserva" :key="r[0]" :value="r[0]">{{ r[1] }}</option>
            </select>
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.terrainType }}</label>
            <select class="form-select form-select-lg" v-model="actividad.terreno"
              :class="{ 'is-invalid': errores.terreno }">
              <option v-for="t in tiposStore.terrenos" :key="t[0]" :value="t[0]">{{ t[1] }}</option>
            </select>
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.period }}</label>
            <select class="form-select form-select-lg" v-model="actividad.periodo"
              :class="{ 'is-invalid': errores.periodo }">
              <option v-for="t in tiposStore.periodos" :key="t[0]" :value="t[0]">{{ t[1] }}</option>
            </select>
          </div>

          <div class="col-md-12">
            <div class="form-check form-switch mt-2">
              <input class="form-check-input" type="checkbox" v-model="actividad.exterior" />
              <label class="form-check-label fw-semibold">{{ t.outdoor }}</label>
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

            <img :src="actividad.imagenURL" class="img-fluid rounded mb-3 img-hover" v-if="actividad.imagenURL"
              style="max-height: 300px; object-fit: cover;" />

            <input v-if="editando" type="file" class="form-control form-control-lg mt-2" @change="onFileChange" />
            <img v-if="preview" :src="preview" class="img-fluid rounded mt-3"
              style="max-height: 300px; object-fit: cover;" />
          </div>
        </div>
        <!-- TAB 3: INSTALACION -->
        <div v-if="tab === 3">
          <div class="mb-4">
            <label class="form-label fw-semibold">{{ t.facility }}</label>
            <select class="form-select form-select-lg" v-model="actividad.instalacion"
              :class="{ 'is-invalid': errores.instalacion }">
              <option :value="null">--</option>
              <option v-for="i in instalacionesFiltradas" :key="i.id" :value="i.id">{{ i.nombre }}</option>
            </select>
          </div>

          <div class="col-md-4" v-if="callesDisponibles.length > 0">
            <label class="form-label fw-semibold">{{ t.poolStreets }}</label>
            <select class="form-select" v-model="calleSeleccionada">
              <option value="" disabled>--</option>
              <option v-for="c in callesDisponibles" :key="c.id" :value="c.numero">
                {{ t.poolStreet }} {{ c.numero }}
              </option>
            </select>
          </div>

          <div v-if="instalacionSeleccionada?.agenda?.length" class="card border-0 shadow-sm rounded-4 p-4 bg-light">
            <h5 class="fw-bold mb-3">{{ t.weekHours }}</h5>

            <div class="mt-4">
              <span class="badge bg-success me-2">{{ t.free }}</span>
              <span class="badge bg-primary me-2">{{ t.selected }}</span>
              <span class="badge bg-warning text-dark">{{ t.activity }}</span>
            </div>

            <div class="row">
              <div v-for="dia in instalacionSeleccionada.agenda" :key="dia.id" class="col-md-6 mb-3">
                <div class="p-3 rounded-3 bg-white border">
                  <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="fw-semibold">{{ dia.dia }}</span>
                    <span v-if="!dia.abierto" class="text-danger fw-semibold">{{ t.close }}</span>
                  </div>
                  <div v-if="dia.abierto">
                    <div v-for="intervalo in dia.mapa_reservas" :key="intervalo.id"
                      class="small mb-1 px-2 py-1 rounded text-white" :class="{
                        'bg-success': intervalo.estado === 'LIBRE',
                        'bg-warning text-dark': intervalo.estado === 'ACTIVIDAD',
                        'bg-primary': intervalo.estado === 'PROPIO'
                      }">
                      {{ intervalo.horaInicio.slice(0, 5) }} - {{ intervalo.horaFin.slice(0, 5) }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- TAB 4: MONITOR Y TARIFA -->
        <div v-if="tab === 4">
          <div class="mb-4">
            <label class="form-label fw-semibold">{{ t.monitor }}</label>
            <select class="form-select form-select-lg" v-model="actividad.monitor"
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
            <select class="form-select form-select-lg" v-model="actividad.tarifa"
              :class="{ 'is-invalid': errores.tarifa }">
              <option :value="null">--</option>
              <option v-for="t in tarifas" :key="t.id" :value="t.id">{{ t.titulo }}</option>
            </select>

            <transition name="fade">
              <div v-if="tarifaSeleccionada" class="mt-4 p-4 bg-white rounded-4 shadow-sm border">
                <h5 class="mb-3 text-primary">{{ t.tariff }}</h5>

                <div v-if="actividad.tipoActividad === 'OTROS'" class="row g-3">
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

                <div v-else-if="actividad.tipoActividad === 'GRUPOS_REDUCIDOS'" class="row g-3">
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

                <div v-else-if="actividad.tipoActividad === 'FISIOTERAPIA'" class="row g-3 mt-3">
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
                <option v-for="d in tiposStore.dias" :key="d[0]" :value="d[0]">
                  {{ d[1] }}
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

          <!-- LISTA SESIONES -->
          <div v-if="sesiones.length" class="bg-light rounded-4 p-3">
            <div v-for="(s, index) in sesiones" :key="s.id ?? index" class="row g-2 align-items-center mb-2">
              <div class="col-md-4">
                <template v-if="editando">
                  <select class="form-select" v-model="s.dia">
                    <option v-for="d in tiposStore.dias" :key="d[0]" :value="d[0]">{{ d[1] }}</option>
                  </select>
                </template>
                <template v-else>
                  {{tiposStore.dias.find(d => d[0] === s.dia)?.[1]}}
                </template>
              </div>
              <div class="col-md-3">
                <template v-if="editando">
                  <input type="time" class="form-control" v-model="s.horaInicio">
                </template>
                <template v-else>
                  {{ s.horaInicio }}
                </template>
              </div>
              <div class="col-md-3">
                <template v-if="editando">
                  <input type="time" class="form-control" v-model="s.horaFin">
                </template>
                <template v-else>
                  {{ s.horaFin }}
                </template>
              </div>
              <div class="col-md-2 text-end">
                <button v-if="editando" class="btn btn-sm btn-danger" @click="sesiones.splice(index, 1)">X</button>
              </div>
            </div>
          </div>
        </div>

        <!-- MENSAJE -->
        <div class="text-center mt-4 fs-5">
          <p v-if="mensaje" class="text-danger">{{ mensaje }}</p>
        </div>

        <!-- ACCIONES -->
        <div class="d-flex justify-content-center gap-4 mt-5">
          <button v-if="!editando" class="btn btn-primary btn-lg rounded-pill px-4" @click="activarEdicion">
            {{ t.modifyActivity }}
          </button>

          <template v-else>
            <button class="btn btn-success btn-lg rounded-pill px-4" @click="guardarCambios">
              {{ t.saveChanges }}
            </button>
            <button class="btn btn-secondary btn-lg rounded-pill px-4" @click="cancelarEdicion">
              {{ t.cancel }}
            </button>
          </template>

          <button v-if="!editando" class="btn btn-outline-danger btn-lg rounded-pill px-4" @click="eliminar">
            {{ t.deleteActivity }}
          </button>
        </div>

      </div>
    </main>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted, inject, type Ref, computed } from "vue"
import { useRouter } from "vue-router"

import { getInstalacionesSimples, getMonitoresSimples, getTarifasActividadComun, getTarifasFisioterapia, getTarifasGrupoReducido, getDeportes } from "@/services/listadoService"
import { eliminarActividad, getActividadDetalle, modificarActividad } from "@/services/detalleService"
import { useTiposStore } from "@/stores/tipos"

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

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
  instalacion: null,
  monitor: null,
  tipoActividad: "",
  tarifa: null,
  tipoReserva: "",
  terreno: "",
  estado: "",
  periodo: "",
  nombreDeporte: ""
})

const imagen = ref<File | null>(null)
const preview = ref<string | null>(null)
const actividadOriginal = ref<any>(null);
const sesiones = ref<any[]>([])
const crearSesion = ref({ id: -1, dia: "", horaInicio: "", horaFin: "" })
const mensaje = ref("")
const editando = ref(false)
const callesDisponibles = ref<any[]>([])
const calleSeleccionada = ref<number | null>(null)

const errores = ref<any>({
  nombre: false, plazasMaximas: false, plazasReservadas: false, edadMinima: false,
  año: false, numeroCreditos: false, tipoActividad: false, tipoReserva: false,
  terreno: false, instalacion: false, monitor: false, deporte: false,
  tarifa: false, periodo: false
})

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
  mensaje.value = ""
  actividadOriginal.value = JSON.parse(JSON.stringify(actividad.value))
  Object.keys(errores.value).forEach(k => errores.value[k] = false)
  editando.value = true
}

function cancelarEdicion() {
  mensaje.value = ""
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

const eliminar = async () => {
  try {
    await eliminarActividad(actividad.value.id)
    router.push({ name: 'gestion-espacios' });
  } catch (e) {
    console.error("Error al eliminar la actividad", e);
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

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  if (!input.files || input.files.length === 0) return

  imagen.value = input.files[0]
  preview.value = URL.createObjectURL(imagen.value)
}

async function guardarCambios() {
  mensaje.value = ""
  if (!validarFormulario()) {
    mensaje.value = t.value.emptyFields
    return
  }

  if (!validarTipoInstalacion()) {
    mensaje.value = t.value.cannotChangeType
    return
  }

  if (!horasValidas()) {
    mensaje.value = t.value.wrongTimetable
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
    router.back()
  } catch (e: any) {
    mensaje.value = e.response?.data?.respuesta
    console.error(e)
  }
}

onMounted(async () => {
  const id = parseInt(props.id);
  try {
    const data = await getActividadDetalle(id);
    actividad.value = data;
    sesiones.value = data.sesiones
    actividadOriginal.value = JSON.parse(JSON.stringify(actividad.value))

    instalaciones.value = await getInstalacionesSimples()
    monitores.value = await getMonitoresSimples()
    deportes.value = await getDeportes()

    console.log(data)
    if (actividad.value.tipoActividad === "OTROS") {
      tarifas.value = await getTarifasActividadComun()
    } else if (actividad.value.tipoActividad === "GRUPOS_REDUCIDOS") {
      tarifas.value = await getTarifasGrupoReducido()
    } else if (actividad.value.tipoActividad === "FISIOTERAPIA") {
      tarifas.value = await getTarifasFisioterapia()
    }
  } catch (e: any) {
    mensaje.value = e.response?.data?.respuesta
    console.log("Error al obtener la informacion de la actividad", e);
  }
});
</script>