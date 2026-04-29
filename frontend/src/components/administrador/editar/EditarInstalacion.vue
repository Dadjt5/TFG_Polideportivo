<template>
  <div class="min-vh-100 pt-4" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4" style="max-width: 1600px;">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold mb-0 text-primary">{{ instalacion.nombre }}</h1>

        <div style="width: 100px"></div>
      </div>

      <!-- CARD PRINCIPAL -->
      <div class="card shadow-lg border-0 rounded-4 p-4 mb-4"
        style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">

        <!-- NAV DE TABS -->
        <ul class="nav nav-pills nav-fill mb-4">
          <li class="nav-item">
            <button class="nav-link active fw-bold" data-bs-toggle="pill" data-bs-target="#info">
              {{ t.facilityDetails }}
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link fw-bold" data-bs-toggle="pill" data-bs-target="#horario">
              {{ t.timetable }}
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link fw-bold" data-bs-toggle="pill" data-bs-target="#especiales">
              {{ t.specialDates }}
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link fw-bold" data-bs-toggle="pill" data-bs-target="#imagenes">
              {{ t.images }}
            </button>
          </li>
        </ul>

        <!-- CONTENIDO DE TABS -->
        <div class="tab-content">

          <!-- TAB 1: INFO -->
          <div class="tab-pane fade show active" id="info">
            <div class="row g-4">
              <div class="col-md-6">
                <label class="form-label fw-semibold">{{ t.name }}</label>
                <input v-if="editando" type="text" class="form-control form-control-lg" v-model="instalacion.nombre"
                  :class="{ 'is-invalid': errores.nombre }" />
                <div v-else class="form-control form-control-lg bg-light text-muted">{{ instalacion.nombre }}</div>
              </div>

              <div class="col-md-6">
                <label class="form-label fw-semibold">{{ t.facilityType }}</label>
                <select v-if="editando" class="form-select form-select-lg" v-model="instalacion.tipoInstalacion"
                  :class="{ 'is-invalid': errores.tipoInstalacion }">
                  <option value="" disabled>--</option>
                  <option v-for="t in tiposStore.tiposInstalacion" :key="t" :value="t">{{ t }}</option>
                </select>
                <div v-else class="form-control form-control-lg bg-light text-muted">{{ instalacion.tipoInstalacion || '---' }}</div>
              </div>

              <div class="col-md-4" v-if="instalacion.tipoInstalacion === 'Piscina'">
                <label class="form-label fw-semibold">{{ t.poolStreets }}</label>
                <input v-if="editando" type="number" min="1" class="form-control form-control-lg"
                  v-model.number="instalacion.numeroCalles" :class="{ 'is-invalid': errores.numeroCalles }" />
                <div v-else class="form-control form-control-lg bg-light text-muted">{{ instalacion.numeroCalles }}
                </div>
              </div>

              <div class="col-md-4">
                <label class="form-label fw-semibold">{{ t.capacity }}</label>
                <input v-if="editando" type="number" min="1" class="form-control form-control-lg"
                  v-model.number="instalacion.aforoMaximo" :class="{ 'is-invalid': errores.aforoMaximo }" />
                <div v-else class="form-control form-control-lg bg-light text-muted">{{ instalacion.aforoMaximo }}</div>
              </div>

              <div class="col-md-4">
                <label class="form-label fw-semibold">TDA (%)</label>
                <input v-if="editando" type="number" min="0" max="100" step="0.1" class="form-control form-control-lg"
                  v-model.number="instalacion.porcentajeTDA" :class="{ 'is-invalid': errores.porcentajeTDA }" />
                <div v-else class="form-control form-control-lg bg-light text-muted">
                  {{ instalacion.porcentajeTDA }}%
                </div>
              </div>

              <div class="col-md-6">
                <label class="form-label fw-semibold">{{ t.pavilion || 'Pabellón' }}</label>
                <select v-if="editando" class="form-select form-select-lg" v-model="instalacion.pabellon.id"
                  :class="{ 'is-invalid': errores.pabellon }">
                  <option value="-1" disabled>--</option>
                  <option v-for="p in pabellones" :key="p.id" :value="p.id">{{ p.nombre }}</option>
                </select>
                <div v-else class="form-control form-control-lg bg-light text-muted">{{ instalacion.pabellon?.nombre ||
                  '---' }}</div>
              </div>

              <div class="col-md-6">
                <label class="form-label fw-semibold">{{ t.tariff || 'Tarifa' }}</label>

                <select v-if="editando" class="form-select form-select-lg" v-model="instalacion.tarifa"
                  :class="{ 'is-invalid': errores.tarifa }">
                  <option :value="null">--</option>
                  <option v-for="tar in tarifas" :key="tar.id" :value="tar.id">
                    {{ tar.titulo }}
                  </option>
                </select>

                <div v-else class="form-control form-control-lg bg-light text-muted">
                  {{tarifas.find(t => t.id === instalacion.tarifa)?.titulo || '---'}}
                </div>
              </div>

              <div class="col-md-12 d-flex align-items-center mt-4">
                <div class="form-check form-switch fs-5">
                  <input class="form-check-input" type="checkbox" v-model="instalacion.luz" :disabled="!editando" />
                  <label class="form-check-label fw-semibold ms-2">{{ t.light }}</label>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB 2: HORARIO -->
          <div class="tab-pane fade" id="horario">
            <div class="row g-3">

              <!-- VISTA NORMAL -->
              <div v-if="agenda.length && !editando" class="card border-0 shadow-sm rounded-4 p-4 bg-light">
                <h5 class="fw-bold mb-3">
                  {{ t.timetable }}
                </h5>

                <div class="card border-0 shadow-sm rounded-4 p-3 bg-light mb-3">
                  <div class="row g-3 align-items-end">

                    <!-- Tipo de reserva -->
                    <div class="col-md-4">
                      <label class="form-label fw-semibold">{{ t.reserveType }}</label>
                      <select class="form-select form-select-lg" v-model="tipoVista">
                        <option value="actividades">{{ t.activities }}</option>
                        <option value="alquileres">{{ t.rents }}</option>
                      </select>
                    </div>

                    <!-- Periodo (solo reservas de actividades) -->
                    <div class="col-md-4" v-if="tipoVista === 'actividades'">
                      <label class="form-label fw-semibold">{{ t.period }}</label>
                      <select class="form-select form-select-lg" v-model="periodo">
                        <option v-for="p in tiposStore.periodos" :key="p" :value="p">{{ p }}</option>
                      </select>
                    </div>

                    <!-- Dia (solo alquileres de instalaciones) -->
                    <div class="col-md-4" v-if="tipoVista === 'alquileres'">
                      <label class="form-label fw-semibold">{{ t.selectedDate }}</label>
                      <input type="date" class="form-control form-control-lg" v-model="reserva.seleccion.fecha" />
                    </div>

                    <!-- Calle (solo piscina) -->
                    <div class="col-md-4" v-if="instalacion.tipoInstalacion === 'Piscina'">
                      <label class="form-label fw-semibold">{{ t.poolStreet }}</label>
                      <select class="form-select form-select-lg" v-model="calleSeleccionada">
                        <option v-for="c in instalacion.calles" :key="c.id" :value="c.id">
                          {{ t.street }} {{ c.numero }}
                        </option>
                      </select>
                    </div>

                  </div>
                </div>

                <!-- LEYENDA -->
                <div class="mt-4 mb-2">
                  <span class="badge bg-success me-2">{{ t.free }}</span>

                  <template v-if="tipoVista === 'actividades'">
                    <span class="badge bg-primary">{{ t.activity }}</span>
                  </template>

                  <template v-else>
                    <span class="badge bg-danger me-2">{{ t.rented }}</span>
                    <span class="badge bg-warning text-dark me-2">{{ t.rentedNoPay }}</span>
                  </template>
                </div>

                <div class="row" :key="`${tipoVista}-${periodo}-${calleSeleccionada}`">
                  <div v-if="tipoVista === 'actividades'" v-for="dia in agenda" :key="dia.id" class="col-12 mb-3">
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

                      <!-- DESPLEGABLE -->
                      <transition name="fade">
                        <div v-if="dia.abierto && isOpen(dia.id)" class="mt-2">
                          <div class="d-flex flex-wrap gap-2">
                            <div v-for="intervalo in filtrarIntervalos(dia.mapa_reservas)" :key="intervalo.id"
                              class="small text-white text-center px-3 py-2 rounded"
                              :class="getClaseIntervalo(intervalo)">
                              {{ intervalo.horaInicio.slice(0, 5) }} - {{ intervalo.horaFin.slice(0, 5) }}
                            </div>
                          </div>
                        </div>
                      </transition>

                    </div>
                  </div>
                  <div v-else-if="reserva.fecha.abierto" class="d-flex flex-wrap gap-2">
                    <button v-for="hora in reservasActuales" :key="hora.horaInicio"
                      class="small text-white text-center px-3 py-2 rounded" :class="getClaseIntervalo(hora)">
                      {{ hora.horaInicio }} - {{ hora.horaFin }}
                    </button>
                  </div>

                  <div v-else class="text-center w-100 py-4">
                    <span class="badge bg-danger fs-6 px-4 py-3">
                      {{ t.close }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- VISTA EDICIÓN -->
              <div v-else class="row">
                <div class="col-md-6 col-lg-4" v-for="dia in agenda" :key="dia.dia">
                  <div class="card border-1 border-light shadow-sm rounded-4 h-100">
                    <div class="card-body">

                      <!-- Cabecera -->
                      <div class="d-flex justify-content-between align-items-center mb-3">
                        <strong class="fs-5">{{ dia.dia }}</strong>

                        <!-- Switch abierto/cerrado -->
                        <div class="form-check form-switch">
                          <input class="form-check-input" type="checkbox" v-model="dia.abierto">
                        </div>
                      </div>

                      <!-- Horario editable -->
                      <div v-if="dia.abierto">
                        <div class="d-flex gap-2 align-items-center">
                          <input type="time" class="form-control" v-model="dia.horaApertura" />

                          <span class="text-muted">-</span>

                          <input type="time" class="form-control" v-model="dia.horaCierre" />
                        </div>
                      </div>

                      <!-- Mensaje si está cerrado -->
                      <div v-else class="text-muted small text-center mt-2">
                        {{ t.close }}
                      </div>

                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>

          <!-- TAB 3: FECHAS ESPECIALES -->
          <div class="tab-pane fade" id="especiales">

            <!-- Botón añadir -->
            <div v-if="editando" class="mb-4">
              <button class="btn btn-danger rounded-pill px-4 shadow-sm" @click="fechasEspeciales.push({ fecha: '' })">
                <i class="bi bi-plus-circle me-2"></i> + {{ t.newSpecialDate }}
              </button>
            </div>

            <!-- Lista -->
            <div v-if="fechasEspeciales?.length" class="row g-3">
              <div class="col-md-6 col-lg-4" v-for="(fecha, index) in fechasEspeciales" :key="index">

                <div class="card border-1 border-light shadow-sm rounded-4 p-3" :class="{ 'bg-light': !editando }">

                  <!-- Fecha -->
                  <div class="d-flex justify-content-between align-items-center mb-3">

                    <div v-if="editando" class="w-75">
                      <input type="date" class="form-control" v-model="fecha.fecha" />
                    </div>

                    <div v-else class="fw-bold fs-5 text-dark">
                      {{ fecha.fecha }}
                    </div>

                    <button v-if="editando" class="btn btn-sm btn-outline-danger"
                      @click="fechasEspeciales.splice(index, 1)">
                      ✕
                    </button>
                  </div>

                  <!-- Estado (siempre cerrado) -->
                  <div class="text-center">
                    <span class="badge bg-danger fs-6 px-3 py-2">
                      {{ t.close }}
                    </span>
                  </div>

                </div>
              </div>
            </div>

            <!-- Vacío -->
            <div v-else class="text-center p-5 text-muted bg-light rounded-4 border">
              <p class="mb-0 fs-5">{{ t.noSpecialDates }}</p>
            </div>

          </div>

          <!-- TAB 4: IMÁGENES -->
          <div class="tab-pane fade" id="imagenes">
            <div class="d-flex justify-content-center">
              <div class="card shadow rounded-4 p-3 text-center"
                style="max-width: 500px; width: 100%; background-color: rgba(255,255,255,0.75); backdrop-filter: blur(8px);">
                <h5 class="mb-3 d-flex justify-content-center align-items-center gap-2">
                  <i class="bi bi-images text-primary"></i> {{ t.images }}
                </h5>

                <img v-if="instalacion.imagen && !preview" :src="instalacion.imagen"
                  class="img-fluid rounded mb-3 shadow-sm" style="max-height: 300px; object-fit: cover;" />

                <div v-if="editando" class="mt-2">
                  <label class="form-label fw-semibold">{{ t.changeImage }}</label>
                  <input type="file" class="form-control form-control-lg" accept="image/*" @change="onFileChange" />
                </div>

                <img v-if="preview" :src="preview" class="img-fluid rounded shadow-sm border border-primary mt-3"
                  style="max-height: 300px; object-fit: cover;" />
              </div>
            </div>
          </div>

        </div>
      </div>

      <div v-if="mostrarMensaje" class="text-center mt-3 mb-3">
        <div class="alert" :class="tipoMensaje === 'success' ? 'alert-success' : 'alert-danger'">
          {{ mensajeEditar }}
        </div>
      </div>

      <!-- ACCIONES -->
      <div class="d-flex justify-content-center gap-4 mt-4 mb-5">
        <button v-if="!editando" class="btn btn-primary btn-lg rounded-pill" @click="activarEdicion">
          <i class="bi bi-pencil me-2"></i> {{ t.modifyFacility }}
        </button>

        <template v-else>
          <button class="btn btn-success btn-lg rounded-pill px-5 shadow" @click="guardarCambios">
            {{ t.saveChanges }}
          </button>
          <button class="btn btn-secondary btn-lg rounded-pill px-5 shadow" @click="cancelarEdicion">
            {{ t.cancel }}
          </button>
        </template>

        <button v-if="!editando" class="btn btn-danger btn-lg rounded-pill" @click="abrirConfirmacion">
          <i class="bi bi-trash me-2"></i> {{ t.deleteFacility }}
        </button>
      </div>
    </main>

    <div class="modal fade" id="confirmDeleteModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4">

          <div class="modal-header">
            <h5 class="modal-title">{{ t.confirmDelete }}</h5>
          </div>

          <div class="modal-body text-center">
            <p>{{ t.confirmDeleteFacility }}</p>
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
import { inject, ref, onMounted, type Ref, watch, computed } from 'vue';
import { useRouter } from "vue-router";
import { Modal } from 'bootstrap'

/* Importamos la comunicacion para recuperar la informacion de instalaciones del backend */
import { getInstalacionDetalle, modificarInstalacion, eliminarInstalacion, getAlquileresPorDia } from "@/services/detalleService";
import { getPabellonesSimples, getTarifasInstalacion } from "@/services/listadoService"

import { useTiposStore } from '@/stores/tipos';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const tiposStore = useTiposStore();
const router = useRouter();

const editando = ref(false)
const mensaje = ref("")
const mensajeEditar = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)

const imagen = ref<File | null>(null)
const preview = ref<string | null>(null)
const agenda = ref<any[]>([])
const fechasEspeciales = ref<any[]>([])
const pabellones = ref<any[]>([])
const tarifas = ref<any[]>([])
const periodo = ref("Todo el año")
const calleSeleccionada = ref()

const instalacion = ref({
  id: 0,
  nombre: "",
  imagen: "",
  aforoMaximo: 50,
  estado: "",
  pagada: false,
  luz: false,
  porcentajeTDA: 0,
  plazasMinimas: 0,
  pabellon: null,
  tarifa: null,
  calles: null,
  tipoInstalacion: "",
  numeroCalles: 0,
  agenda: [] as any[],
  reservas_usuarios: [] as any[],
});

const reserva = ref({
  fecha: null as any,
  seleccion: {
    fecha: new Date().toISOString().slice(0, 10),
  },
})

const errores = ref({
  nombre: false,
  aforoMaximo: false,
  porcentajeTDA: false,
  horaApertura: false,
  tarifa: false,
  pabellon: false,
  horaCierre: false,
  tipoInstalacion: false,
  numeroCalles: false
})

const reservasActuales = computed(() => {
  if (!reserva.value.fecha) return []

  if (reserva.value.fecha.numeroCalles === 0) {
    return reserva.value.fecha.slots || []
  }

  const calle = reserva.value.fecha.calles?.find(
    (c: any) => c.id === calleSeleccionada.value
  )

  return calle ? calle.slots : []
})


const openDias = ref([])

const toggleDia = (id: any) => {
  if (openDias.value.includes(id)) {
    openDias.value = openDias.value.filter(i => i !== id)
  } else {
    openDias.value.push(id)
  }
}

const isOpen = (id: any) => openDias.value.includes(id)

const instalacionOriginal = ref<any>(null);

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

  errores.value.nombre = instalacion.value.nombre === ''
  errores.value.aforoMaximo = instalacion.value.aforoMaximo <= 0
  errores.value.porcentajeTDA = instalacion.value.porcentajeTDA < 0
  errores.value.pabellon = instalacion.value.pabellon === null
  errores.value.tarifa = instalacion.value.tarifa === null
  errores.value.tipoInstalacion = instalacion.value.tipoInstalacion === ''
  errores.value.tarifa
  errores.value.numeroCalles =
    instalacion.value.numeroCalles <= 0 &&
    instalacion.value.tipoInstalacion === "Piscina"

  for (const key in errores.value) {
    if (errores.value[key]) {
      valido = false
    }
  }

  return valido
}

const diasSemana = [
  "Lunes",
  "Martes",
  "Miercoles",
  "Jueves",
  "Viernes",
  "Sabado",
  "Domingo"
];

function esOcupadoPorPeriodo(intervalo: any) {
  const periodos = intervalo.periodo || []

  if (periodo.value === "Todo el año") {
    return periodos.length > 0
  }

  return (
    periodos.includes(periodo.value) ||
    periodos.includes("Todo el año")
  )
}

function filtrarIntervalos(intervalos: any) {
  if (instalacion.value.tipoInstalacion !== 'Piscina') {
    return intervalos
  }

  return intervalos.filter(i => i.calle === calleSeleccionada.value)
}

const tipoVista = ref<'actividades' | 'alquileres'>('actividades')

function getClaseIntervalo(intervalo: any) {
  if (tipoVista.value === 'actividades') {
    return {
      'bg-success': intervalo.estado === 'Libre' || !esOcupadoPorPeriodo(intervalo),
      'bg-primary': intervalo.estado === 'Reserva actividad',
      'bg-danger': intervalo.estado === 'Reserva usuario' && intervalo.pagada
    }
  }

  // NUEVO alquileres
  return {
    'bg-success': intervalo.estado === 'Libre',
    'bg-danger': intervalo.estado === 'Reservado' && intervalo.pagada,
    'bg-warning text-dark': intervalo.estado === 'Reservado' && !intervalo.pagada,
  }
}

function estaDentro(intervalo: any, reserva: any) {
  const inicioIntervalo = intervalo.horaInicio.slice(0, 5);
  const finIntervalo = intervalo.horaFin.slice(0, 5);

  const inicioReserva = reserva.horaInicio.slice(0, 5);
  const finReserva = reserva.horaFin.slice(0, 5);

  return (
    inicioIntervalo >= inicioReserva &&
    finIntervalo <= finReserva
  );
}

function activarEdicion() {
  mensaje.value = ""
  instalacionOriginal.value = JSON.parse(JSON.stringify(instalacion.value))
  Object.keys(errores.value).forEach(k => errores.value[k] = false)
  editando.value = true
}

function cancelarEdicion() {
  mensaje.value = ""
  instalacion.value = JSON.parse(JSON.stringify(instalacionOriginal.value))
  agenda.value = JSON.parse(JSON.stringify(instalacionOriginal.value.agenda))
  preview.value = null
  imagen.value = null
  editando.value = false
}

function validarTipoInstalacion() {
  // Si el tipo es piscina no puede ser otro y viceversa
  if (instalacion.value.tipoInstalacion == "Piscina" && instalacionOriginal.value.tipoInstalacion != "Piscina") {
    errores.value.tipoInstalacion = true;
    return false;
  }

  if (instalacion.value.tipoInstalacion != "Piscina" && instalacionOriginal.value.tipoInstalacion == "Piscina") {
    errores.value.tipoInstalacion = true;
    return false;
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
  if (!validarFormulario()) {
    lanzarMensaje(t.value.missing, "error")
    return
  }

  if (instalacion.value.aforoMaximo < instalacion.value.plazasMinimas) {
    lanzarMensaje(t.value.errorPlaces2, "error")
    return
  }

  if (instalacion.value.tipoInstalacion == "Piscina") {
    if (instalacion.value.plazasMinimas > instalacion.value.aforoMaximo/instalacion.value.numeroCalles) {
      lanzarMensaje(t.value.errorPlaces2, "error")
      return
    }
  }

  if (!validarTipoInstalacion()) {
    lanzarMensaje(t.value.cannotChangeType, "error")
    return
  }

  const formData = new FormData()

  formData.append("instalacion", JSON.stringify(instalacion.value))
  formData.append("agenda", JSON.stringify(agenda.value))
  formData.append("fechasEspeciales", JSON.stringify(fechasEspeciales.value.map(f => ({fecha: f.fecha})))
)

  if (imagen.value) {
    formData.append("imagen", imagen.value)
  }

  try {
    await modificarInstalacion(parseInt(props.id), formData)
    lanzarMensaje(t.value.correctlyUpdate, "success")
    cancelarEdicion()

    const data = await getInstalacionDetalle(parseInt(props.id))

    agenda.value = data.agenda.filter((a: any) => a.dia && !a.fecha)
    fechasEspeciales.value = data.agenda.filter((a: any) => a.fecha)

    instalacion.value = {
      ...data,
      agenda: agenda.value
    }

    instalacionOriginal.value = JSON.parse(JSON.stringify(instalacion.value))
  } catch (e: any) {
    if (e.response.data.tipo == "sesiones") {
      lanzarMensaje(t.value.noModifyActivity, "error")
    } else if (e.response.data.tipo == "otro") {
      lanzarMensaje(t.value.noModify, "error")
    } else if (e.response.data.tipo == "aforo") {
      lanzarMensaje(t.value.errorPlaces, "error")
    }
    
    console.error("Error al modificar la instalacion", e)
  }
}

let confirmModal: Modal
let successModal: Modal

const eliminado = ref(false)

function abrirConfirmacion() {
  confirmModal.show()
}

async function confirmarEliminar() {
  try {
    await eliminarInstalacion(instalacion.value.id)

    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.facilityDeleted
    eliminado.value = true
  } catch (e) {
    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.facilityNoDeleted
    eliminado.value = false
    console.error("Error al eliminar la instalacion", e);
  }
}

const finalizar = async () => {
  if (eliminado.value) {
    router.push({ name: 'gestion-espacios' });
  } else {
    successModal.hide()
    eliminado.value = false
  }
}

const volver = () => {
  router.back();
};

watch(
  () => instalacion.value.tipoInstalacion,
  (tipo) => {
    mensaje.value = ""
    if (tipo !== "Piscina") {
      instalacion.value.numeroCalles = 0
    }
  }
)

watch(() => periodo.value, () => {
  openDias.value = []
})

watch(calleSeleccionada, () => {
  openDias.value = []
})

watch(
  () => reserva.value.seleccion.fecha,
  async (nuevaFecha) => {
    const data = await getAlquileresPorDia(instalacion.value.id, nuevaFecha)
    reserva.value.fecha = data
  }
)

onMounted(async () => {
  const id = parseInt(props.id);

  confirmModal = new Modal(document.getElementById('confirmDeleteModal')!)
  successModal = new Modal(document.getElementById('successDeleteModal')!)

  try {
    const data = await getInstalacionDetalle(id)
    pabellones.value = await getPabellonesSimples()
    tarifas.value = await getTarifasInstalacion()

    agenda.value = data.agenda.filter((a: any) => a.dia && !a.fecha)
    fechasEspeciales.value = data.agenda
      .filter((a: any) => a.fecha)
      .map((a: any) => ({
      fecha: a.fecha
    }))
  
    calleSeleccionada.value = data.calles?.[0]?.id

    instalacion.value = {
      ...data,
      agenda: agenda.value
    }

    instalacionOriginal.value = JSON.parse(JSON.stringify(instalacion.value))

    const alquileres = await getAlquileresPorDia(id, reserva.value.seleccion.fecha)
    reserva.value.fecha = alquileres

  } catch (e) {
    mensaje.value = t.value.unexpectedError
    console.log("Error al obtener la informacion de la instalacion", e);
  }
});
</script>
