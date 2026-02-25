<template>
  <div class="min-vh-100 bg-light pb-5">
    <main class="container py-5" style="max-width: 1100px;">
      <h1 class="text-center fw-bold mb-5 display-6">
        {{ t.newActivity }}
      </h1>

      <div class="card border-0 shadow-lg rounded-4 p-4">

        <!-- TABS -->
        <ul class="nav nav-tabs nav-fill mb-4">
          <li class="nav-item" v-for="n in 4" :key="n">
            <button type="button" class="nav-link" :class="{ active: tab === n }" @click="tab = n">
              {{ tabLabels[n] }}
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

          <!-- AÑO -->
          <div class="col-md-3">
            <label class="form-label fw-semibold">{{ t.academicYear }}</label>
            <input type="number" class="form-control form-control-lg" :class="{ 'is-invalid': errores.año }"
              v-model.number="actividad.año" />
          </div>

          <!-- ESTADO -->
          <div class="col-md-3">
            <label class="form-label fw-semibold">{{ t.status }}</label>
            <select class="form-select form-select-lg" :class="{ 'is-invalid': errores.estado }"
              v-model="actividad.estado">
              <option disabled value="">--</option>
              <option v-for="e in tiposStore.estados" :key="e[0]" :value="e[0]">{{ e[1] }}</option>
            </select>
          </div>

          <!-- DESCRIPCIÓN -->
          <div class="col-md-12">
            <label class="form-label fw-semibold">{{ t.description }}</label>
            <textarea rows="3" class="form-control form-control-lg" v-model="actividad.descripcion" />
          </div>

          <!-- IMAGEN -->
          <div class="col-md-12">
            <label class="form-label fw-semibold">{{ t.images }}</label>
            <input type="text" class="form-control form-control-lg" v-model="actividad.imagenURL"
              placeholder="https://@." />
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

            <input type="text" class="form-control form-control-lg" :class="{ 'is-invalid': errores.deporte }"
              v-model="nombreDeporte" list="listaDeportes" placeholder="Ej: Fútbol" />

            <datalist id="listaDeportes">
              <option v-for="d in deportes" :key="d.id" :value="d.titulo" />
            </datalist>
          </div>

          <!-- TIPO ACTIVIDAD -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.activityType }}</label>
            <select class="form-select form-select-lg" :class="{ 'is-invalid': errores.tipoActividad }"
              v-model="actividad.tipoActividad">
              <option v-for="t in tiposStore.tiposActividad" :key="t[0]" :value="t[0]">{{ t[1] }}</option>
            </select>
          </div>

          <!-- RESERVA -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.reserveType }}</label>
            <select class="form-select form-select-lg" :class="{ 'is-invalid': errores.tipoReserva }"
              v-model="actividad.tipoReserva">
              <option v-for="r in tiposStore.tiposReserva" :key="r[0]" :value="r[0]">{{ r[1] }}</option>
            </select>
          </div>

          <!-- TERRENO -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.terrainType }}</label>
            <select class="form-select form-select-lg" :class="{ 'is-invalid': errores.terreno }"
              v-model="actividad.terreno">
              <option v-for="t in tiposStore.terrenos" :key="t[0]" :value="t[0]">{{ t[1] }}</option>
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
        </div>

        <!-- TAB 2 INSTALACION -->
        <div v-if="tab === 2">

          <div class="mb-4">
            <label class="form-label fw-semibold">{{ t.facility }}</label>
            <select class="form-select form-select-lg" v-model="actividad.instalacion_id">
              <option :value="null">--</option>
              <option v-for="i in instalaciones" :key="i.id" :value="i.id">
                {{ i.nombre }}
              </option>
            </select>
          </div>

          <!-- HORARIO -->
          <div v-if="instalacionSeleccionada?.agenda?.length" class="card border-0 shadow-sm rounded-4 p-4 bg-light">

            <h5 class="fw-bold mb-3">
              {{ t.weekHours }}
            </h5>

            <div class="row">

              <div v-for="dia in instalacionSeleccionada.agenda" :key="dia.dia" class="col-md-6 mb-2">

                <div class="d-flex justify-content-between
                    p-2 rounded-3 bg-white border">

                  <span class="fw-semibold">
                    {{ dia.dia }}
                  </span>

                  <span v-if="!dia.abierto" class="text-danger fw-semibold">
                    {{ t.close }}
                  </span>

                  <span v-else class="text-success">
                    {{ dia.horaApertura.slice(0, 5) }} -
                    {{ dia.horaCierre.slice(0, 5) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- TAB 3 MONITOR Y TARIFA -->
        <div v-if="tab === 3">

          <div class="mb-4">
            <label class="form-label fw-semibold">{{ t.monitor }}</label>
            <select class="form-select form-select-lg" v-model="actividad.monitor_id">
              <option :value="null">--</option>
              <option v-for="m in monitores" :key="m.id" :value="m.id">
                {{ m.nombre }}
              </option>
            </select>

            <div v-if="monitorSeleccionado" class="bg-light rounded-4 p-3 mt-3">
              <strong>Carga actual:</strong>
              {{ monitorSeleccionado.carga }} {{ t.weekHours }}
            </div>
          </div>

          <div>
            <label class="form-label fw-semibold">{{ t.tariff }}</label>
            <select class="form-select form-select-lg" v-model="actividad.tarifa">
              <option :value="null">--</option>
              <option v-for="t in tarifas" :key="t.id" :value="t.id">
                {{ t.titulo }}
              </option>
            </select>

            <div v-if="tarifaSeleccionada" class="bg-light rounded-4 p-3 mt-3">
              <strong>{{ t.priceSubscripcion }}:</strong>
              {{ tarifaSeleccionada.precioAbonado }} €
            </div>
          </div>

        </div>

        <!-- TAB 4 SESIONES -->
        <div v-if="tab === 4">

          <div class="row g-3 align-items-end mb-4">

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
              <button type="button" class="btn btn-primary w-100" @click="agregarSesion">
                {{ t.newSession }}
              </button>
            </div>

          </div>

          <div v-if="sesiones.length" class="bg-light rounded-4 p-3">

            <div v-for="(s, index) in sesiones" :key="index"
              class="d-flex justify-content-between align-items-center mb-2">

              <span>
                {{ s.dia }} | {{ s.horaInicio }} - {{ s.horaFin }}
              </span>

              <button type="button" class="btn btn-sm btn-danger" @click="sesiones.splice(index, 1)">
                X
              </button>

            </div>

          </div>

        </div>

        <!-- BOTONES -->
        <div class="d-flex justify-content-between mt-5">
          <button class="btn btn-outline-secondary" type="button" @click="volver">
            {{ t.return }}
          </button>

          <button class="btn btn-success px-4" type="button" @click="crearActividad">
            {{ t.createActivity }}
          </button>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { watch, inject, type Ref, ref, onMounted, computed } from "vue"
import { useRouter } from "vue-router"

import { nuevaActividad, actualizarDeportes, nuevaSesion } from "@/services/crearRecursosService"
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

const tabLabels = {
  1: t.value.data,
  2: t.value.facility,
  3: t.value.monitor,
  4: t.value.sessions
}

const actividad = ref({
  nombre: "",
  descripcion: "",
  imagenURL: "",
  edadMinima: 18,
  plazasMaximas: 50,
  plazasReservadas: 0,
  año: añoActual,
  numeroCreditos: 0,
  nivel: "",
  material: "",
  exterior: false,
  instalacion_id: null,
  monitor_id: null,
  tipoActividad: "OTROS",
  tarifa: null,
  tipoReserva: "",
  terreno: "",
  estado: "",
  periodo: "ANUAL",
  deporte_id: null,
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
  estado: false,
  instalacion: false,
  monitor: false,
  deporte: false
})

const instalaciones = ref<any[]>([])
const monitores = ref<any[]>([])
const tarifas = ref<any[]>([])
const deportes = ref<any[]>([])

const nombreDeporte = ref("")

const sesiones = ref<any[]>([])
const crearSesion = ref({
  dia: "",
  horaInicio: "",
  horaFin: ""
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

function agregarSesion() {
  if (!crearSesion.value.dia ||
    !crearSesion.value.horaInicio ||
    !crearSesion.value.horaFin) return

  sesiones.value.push({ ...crearSesion.value })
  crearSesion.value = { dia: "", horaInicio: "", horaFin: "" }
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
  errores.value.estado = actividad.value.estado === ""
  errores.value.instalacion = actividad.value.instalacion_id === ""
  errores.value.monitor = actividad.value.monitor_id === ""
  errores.value.deporte = nombreDeporte.value === ""

  for (const k in errores.value) {
    if (errores.value[k]) {
      ok = false
    }
  }

  return ok
}

const crearActividad = async () => {
  if (!validarFormulario()) return

  try {
    const actividadObj = await nuevaActividad(actividad.value)
    await nuevaSesion(actividadObj.id, sesiones.value)
    await actualizarDeportes(actividadObj.id, nombreDeporte.value)
    router.push({ name: 'gestion-actividades' });
  } catch (e) {
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

    if (nuevoTipo === "OTROS") {
      tarifas.value = await getTarifasActividadComun()
    } else if (nuevoTipo === "GRUPOS_REDUCIDOS") {
      tarifas.value = await getTarifasGrupoReducido()
    } else if (nuevoTipo === "FISIOTERAPIA") {
      tarifas.value = await getTarifasFisioterapia()
    }
  }
)

onMounted(async () => {
  instalaciones.value = await getInstalacionesSimples()
  monitores.value = await getMonitoresSimples()
  tarifas.value = await getTarifasActividadComun()
  deportes.value = await getDeportes()
})
</script>