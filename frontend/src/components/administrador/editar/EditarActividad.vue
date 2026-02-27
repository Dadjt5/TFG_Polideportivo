<template>
  <div class="min-vh-100 bg-light pb-5">
    <main class="container py-5" style="max-width: 1100px;">
      <h1 class="text-center fw-bold mb-5 display-6">
        {{ t.editActivity }}
      </h1>

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

        <!-- TAB 1: DATOS -->
        <div v-if="tab === 1" class="row g-4">
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.name }}</label>
            <input type="text" class="form-control form-control-lg" v-model="actividad.nombre" :class="{ 'is-invalid': errores.nombre }" />
          </div>

          <div class="col-md-3">
            <label class="form-label fw-semibold">{{ t.academicYear }}</label>
            <input type="number" class="form-control form-control-lg" v-model.number="actividad.año" :class="{ 'is-invalid': errores.año }" />
          </div>

          <div class="col-md-3">
            <label class="form-label fw-semibold">{{ t.status }}</label>
            <select class="form-select form-select-lg" v-model="actividad.estado" :class="{ 'is-invalid': errores.estado }">
              <option disabled value="">--</option>
              <option v-for="e in tiposStore.estados" :key="e[0]" :value="e[0]">{{ e[1] }}</option>
            </select>
          </div>

          <div class="col-md-12">
            <label class="form-label fw-semibold">{{ t.description }}</label>
            <textarea rows="3" class="form-control form-control-lg" v-model="actividad.descripcion"></textarea>
          </div>

          <div class="col-md-12">
            <label class="form-label fw-semibold">{{ t.images }}</label>
            <input type="text" class="form-control form-control-lg" v-model="actividad.imagenURL" placeholder="https://@." />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.maxPlaces }}</label>
            <input type="number" class="form-control form-control-lg" v-model.number="actividad.plazasMaximas" :class="{ 'is-invalid': errores.plazasMaximas }" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.reservedPlaces }}</label>
            <input type="number" class="form-control form-control-lg" v-model.number="actividad.plazasReservadas" :class="{ 'is-invalid': errores.plazasReservadas }" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.minimumAge }}</label>
            <input type="number" class="form-control form-control-lg" v-model.number="actividad.edadMinima" :class="{ 'is-invalid': errores.edadMinima }" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.credits }}</label>
            <input type="number" class="form-control form-control-lg" v-model.number="actividad.numeroCreditos" :class="{ 'is-invalid': errores.numeroCreditos }" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.level }}</label>
            <input type="text" class="form-control form-control-lg" v-model="actividad.nivel" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.material }}</label>
            <input type="text" class="form-control form-control-lg" v-model="actividad.material" />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.sport }}</label>
            <input type="text" class="form-control form-control-lg" v-model="nombreDeporte" list="listaDeportes" placeholder="Ej: Fútbol" :class="{ 'is-invalid': errores.deporte }" />
            <datalist id="listaDeportes">
              <option v-for="d in deportes" :key="d.id" :value="d.titulo" />
            </datalist>
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.activityType }}</label>
            <select class="form-select form-select-lg" v-model="actividad.tipoActividad" :class="{ 'is-invalid': errores.tipoActividad }">
              <option v-for="t in tiposStore.tiposActividad" :key="t[0]" :value="t[0]">{{ t[1] }}</option>
            </select>
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.reserveType }}</label>
            <select class="form-select form-select-lg" v-model="actividad.tipoReserva" :class="{ 'is-invalid': errores.tipoReserva }">
              <option v-for="r in tiposStore.tiposReserva" :key="r[0]" :value="r[0]">{{ r[1] }}</option>
            </select>
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.terrainType }}</label>
            <select class="form-select form-select-lg" v-model="actividad.terreno" :class="{ 'is-invalid': errores.terreno }">
              <option v-for="t in tiposStore.terrenos" :key="t[0]" :value="t[0]">{{ t[1] }}</option>
            </select>
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.period }}</label>
            <select class="form-select form-select-lg" v-model="actividad.periodo" :class="{ 'is-invalid': errores.periodo }">
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

        <!-- TAB 2: INSTALACION -->
        <div v-if="tab === 2">
          <div class="mb-4">
            <label class="form-label fw-semibold">{{ t.facility }}</label>
            <select class="form-select form-select-lg" v-model="actividad.instalacion_id" :class="{ 'is-invalid': errores.instalacion }">
              <option :value="null">--</option>
              <option v-for="i in instalaciones" :key="i.id" :value="i.id">{{ i.nombre }}</option>
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

        <!-- TAB 3: MONITOR Y TARIFA -->
        <div v-if="tab === 3">
          <div class="mb-4">
            <label class="form-label fw-semibold">{{ t.monitor }}</label>
            <select class="form-select form-select-lg" v-model="actividad.monitor_id" :class="{ 'is-invalid': errores.monitor }">
              <option :value="null">--</option>
              <option v-for="m in monitores" :key="m.id" :value="m.id">{{ m.nombre }}</option>
            </select>

            <div v-if="monitorSeleccionado" class="bg-light rounded-4 p-3 mt-3">
              <strong>{{ t.weeklyWork }}:</strong> {{ monitorSeleccionado.carga }} {{ t.weekHours }}
            </div>
          </div>

          <div>
            <label class="form-label fw-semibold">{{ t.tariff }}</label>
            <select class="form-select form-select-lg" v-model="actividad.tarifa" :class="{ 'is-invalid': errores.tarifa }">
              <option :value="null">--</option>
              <option v-for="t in tarifas" :key="t.id" :value="t.id">{{ t.titulo }}</option>
            </select>
          </div>
        </div>

        <!-- TAB 4: SESIONES -->
        <div v-if="tab === 4">
          <div class="row g-3 align-items-end mb-4">
            <div class="col-md-4">
              <label class="form-label fw-semibold">{{ t.day }}</label>
              <select class="form-select" v-model="crearSesion.dia">
                <option value="">--</option>
                <option v-for="d in tiposStore.dias" :key="d[0]" :value="d[0]">{{ d[1] }}</option>
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
              <button type="button" class="btn btn-primary w-100" @click="agregarSesion">{{ t.newSession }}</button>
            </div>
          </div>

          <div v-if="sesiones.length" class="bg-light rounded-4 p-3">
            <div v-for="(s, index) in sesiones" :key="index" class="d-flex justify-content-between align-items-center mb-2">
              <span>{{ s.dia }} | {{ s.horaInicio }} - {{ s.horaFin }}</span>
              <button type="button" class="btn btn-sm btn-danger" @click="sesiones.splice(index, 1)">X</button>
            </div>
          </div>
        </div>

        <!-- MENSAJE -->
        <div class="text-center mt-4 fs-5">
          <p v-if="mensaje" class="text-danger">{{ mensaje }}</p>
        </div>

        <!-- BOTONES -->
        <div class="d-flex justify-content-between mt-5">
          <button class="btn btn-outline-secondary" type="button" @click="volver">{{ t.return }}</button>
          <button class="btn btn-success px-4" type="button" @click="guardarCambios">{{ t.saveChanges }}</button>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, inject, type Ref, computed } from "vue"
import { useRouter } from "vue-router"
import { getActividadDetalle, modificarActividad } from "@/services/detalleService"
import { useTiposStore } from "@/stores/tipos"
import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const props = defineProps<{ id: string }>()
const router = useRouter()
const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

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
  instalacion_id: null,
  monitor_id: null,
  tipoActividad: "",
  tarifa: null,
  tipoReserva: "",
  terreno: "",
  estado: "",
  periodo: "",
})

const sesiones = ref<any[]>([])
const crearSesion = ref({ dia: "", horaInicio: "", horaFin: "" })
const nombreDeporte = ref("")
const mensaje = ref("")

const errores = ref<any>({
  nombre: false, plazasMaximas: false, plazasReservadas: false, edadMinima: false,
  año: false, numeroCreditos: false, tipoActividad: false, tipoReserva: false,
  terreno: false, estado: false, instalacion: false, monitor: false, deporte: false,
  tarifa: false, periodo: false
})

const monitorSeleccionado = computed(() =>
  monitores.value.find(m => m.id === actividad.value.monitor_id)
)
const tarifaSeleccionada = computed(() =>
  tarifas.value.find(t => t.id === actividad.value.tarifa)
)
const instalacionSeleccionada = computed(() =>
  instalaciones.value.find(i => i.id === actividad.value.instalacion_id)
)

const instalaciones = ref<any[]>([])
const monitores = ref<any[]>([])
const tarifas = ref<any[]>([])
const deportes = ref<any[]>([])

function agregarSesion() {
  if (!crearSesion.value.dia || !crearSesion.value.horaInicio || !crearSesion.value.horaFin) return
  sesiones.value.push({ ...crearSesion.value })
  crearSesion.value = { dia: "", horaInicio: "", horaFin: "" }
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
  errores.value.estado = actividad.value.estado === ""
  errores.value.periodo = actividad.value.periodo === ""
  errores.value.instalacion = actividad.value.instalacion_id === null
  errores.value.monitor = actividad.value.monitor_id === null
  errores.value.tarifa = actividad.value.tarifa === null
  errores.value.deporte = nombreDeporte.value === ""
  for (const k in errores.value) if (errores.value[k]) ok = false
  return ok
}

async function guardarCambios() {
  mensaje.value = ""
  if (!validarFormulario()) {
    mensaje.value = t.value.emptyFields
    return
  }

  try {
    await modificarActividad(parseInt(props.id), { ...actividad.value, sesiones: sesiones.value, nombreDeporte: nombreDeporte.value })
    router.back()
  } catch (e) {
    console.error(e)
    mensaje.value = "Error al guardar cambios"
  }
}

onMounted(async () => {
  const id = parseInt(props.id);
  try {
    actividad.value = await getActividadDetalle(id);
    console.log(actividad)
    //actividadOriginal.value = JSON.parse(JSON.stringify(actividad.value))
  } catch (e) {
    console.log("Error al obtener la informacion de la actividad", e);
  }
});
</script>