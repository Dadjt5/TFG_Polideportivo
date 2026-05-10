<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4">

      <!-- Cabecera -->
      <div class="d-flex justify-content-center align-items-center mt-4 mb-5 gap-2">
        <h1 class="fw-semibold text-primary mb-0" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
          <i class="bi bi-calendar2-event me-2"></i>{{ instalacion.nombre }}
        </h1>

        <button v-if="usuarioFinalStore.isLogged" class="btn btn-link p-0 text-warning" @click.stop="cambiarFavorito"
          :title="usuarioFinalStore.facilityIsFavorite(instalacion.id) ? 'Quitar de favoritos' : 'Agregar a favoritos'">
          <i :class="['bi', usuarioFinalStore.facilityIsFavorite(instalacion.id) ? 'bi-star-fill' : 'bi-star']"
            class="fs-2"></i>
        </button>
      </div>

      <div class="card shadow-lg border-0 rounded-4 p-4"
        style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">

        <!-- NAV TABS -->
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
            <button class="nav-link fw-bold" data-bs-toggle="pill" data-bs-target="#horarioEspecial">
              {{ t.specialDates }}
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link fw-bold" data-bs-toggle="pill" data-bs-target="#imagenes">
              {{ t.images }}
            </button>
          </li>
        </ul>

        <!-- CONTENIDO -->
        <div class="tab-content">

          <!-- TAB INFO -->
          <div class="tab-pane fade show active" id="info">
            <div class="row g-3">

              <div class="col-12 col-sm-6">
                <p><i class="bi bi-people-fill text-success me-1"></i>
                  <span class="fw-medium">{{ t.capacity }}:</span> {{ instalacion.aforoMaximo }}
                </p>
              </div>

              <div class="col-12 col-sm-6">
                <p><i class="bi bi-lightbulb-fill text-warning me-1"></i>
                  <span class="fw-medium">{{ t.light }}:</span> {{ instalacion.luz ? t.yes : "No" }}
                </p>
              </div>

              <div class="col-12 col-sm-6">
                <p><i class="bi bi-percent text-info me-1"></i>
                  <span class="fw-medium">{{ t.tdaPercent }}:</span> {{ instalacion.porcentajeTDA }} %
                </p>
              </div>

              <div class="col-12 col-sm-6" v-if="instalacion.pabellon">
                <p>
                  <i class="bi bi-building text-primary me-1"></i>
                  <span class="fw-medium">{{ t.pavilion }}: </span>
                  <span class="text-primary fw-medium" style="cursor: pointer;"
                    @click="pavilionDetail(instalacion.pabellon.id)">
                    {{ instalacion.pabellon.nombre }}
                  </span>
                </p>
              </div>

              <div class="col-12 col-sm-6" v-if="instalacion.pabellon">
                <p><i class="bi bi-geo-alt-fill text-danger me-1"></i>
                  <span class="fw-medium">{{ t.address }}:</span>
                  {{ instalacion.pabellon.direccion }}
                </p>
              </div>

              <div class="col-12 col-sm-6" v-if="instalacion.tipoInstalacion">
                <p><i class="bi bi-door-open-fill text-primary me-1"></i>
                  <span class="fw-medium">{{ t.facilityType }}:</span>
                  {{ instalacion.tipoInstalacion }}
                </p>
              </div>

            </div>
          </div>

          <!-- TAB 2: HORARIO -->
          <div class="tab-pane fade" id="horario">
            <div class="row g-3">

              <div v-if="agenda.length" class="card border-0 shadow-sm rounded-4 p-4 bg-light">
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
                        <option v-for="c in instalacion.calles" :key="c.id" :value="c.numero">
                          {{ t.street }} {{ c.numero || c.id }}
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
                      {{ t.close || 'Instalación cerrada' }}
                    </span>
                  </div>
                </div>
              </div>

              <button class="btn btn-outline-primary mt-4" @click="descargarPDF">
                <i class="bi bi-file-earmark-pdf"></i> {{ t.downloadTimetable }}
              </button>

            </div>
          </div>

          <!-- TAB 3: FECHAS ESPECIALES -->
          <div class="tab-pane fade" id="horarioEspecial">

            <!-- Lista -->
            <div v-if="fechasEspeciales?.length" class="row g-3">
              <div class="col-md-6 col-lg-4" v-for="(fecha, index) in fechasEspeciales" :key="index">

                <div class="card border-1 border-light shadow-sm rounded-4 p-3">

                  <!-- Fecha -->
                  <div class="d-flex justify-content-between align-items-center mb-3">
                    <div class="fw-bold fs-5 text-dark">
                      {{ fecha.fecha }}
                    </div>
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

          <!-- TAB HORARIO -->
          <div class="tab-pane fade" id="horario">
            <div class="row g-3">
              <div class="col-md-6 col-lg-4" v-for="dia in agenda" :key="dia.dia">
                <div class="card border-1 border-light shadow-sm rounded-4 h-100">
                  <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                      <strong class="fs-5">{{ dia.dia }}</strong>
                      <span class="badge" :class="dia.abierto ? 'bg-success' : 'bg-danger'">
                        {{ dia.abierto ? 'Abierto' : 'Cerrado' }}
                      </span>
                    </div>

                    <div v-if="dia.abierto">
                      <div class="d-flex align-items-center justify-content-center gap-2 py-2 bg-white rounded border">
                        <span class="fw-semibold text-primary">{{ dia.horaApertura?.slice(0, 5) }}</span>
                        <span class="text-muted">-</span>
                        <span class="fw-semibold text-primary">{{ dia.horaCierre?.slice(0, 5) }}</span>
                      </div>
                    </div>

                  </div>
                </div>
              </div>
            </div>

            <button class="btn btn-outline-primary mt-4" @click="descargarPDF">
              <i class="bi bi-file-earmark-pdf"></i> {{ t.downloadTimetable }}
            </button>
          </div>

          <!-- TAB IMÁGENES -->
          <div class="tab-pane fade" id="imagenes">
            <div v-if="instalacion.imagen" class="d-flex justify-content-center">
              <img :src="instalacion.imagen" class="img-fluid rounded shadow"
                style="max-height: 400px; object-fit: cover;" />
            </div>

            <div v-else class="text-center text-muted mt-5">
              <i class="bi bi-image fs-1"></i>
              <p class="mt-3">{{ t.noImage }}</p>
            </div>
          </div>

        </div>
      </div>

      <!-- Reserva y Volver -->
      <div class="d-flex justify-content-center align-items-center mt-5 gap-3 flex-wrap">

        <!-- RESERVAR -->
        <button v-if="usuarioFinalStore.isLogged" class="btn btn-success btn-lg px-5 shadow-sm" @click="reservar">
          {{ t.booking }}
        </button>

        <!-- VOLVER -->
        <button class="btn btn-outline-secondary btn-lg px-5" @click="volver">
          {{ t.return }}
        </button>
      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { inject, ref, onMounted, type Ref, watch, computed } from 'vue';
import { useRouter } from "vue-router";

/* Importamos la comunicacion para recuperar la informacion de instalaciones del backend */
import { getInstalacionDetalleSinAgenda, getAlquileresPorDia, getAgendaInstalacion } from "@/services/detalleService";
import { useUserStore } from '@/stores/usuarioFinal';
import { useTiposStore } from '@/stores/tipos';
import { descargarHorario } from '@/services/crearRecursosService';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();

const tiposStore = useTiposStore();
const usuarioFinalStore = useUserStore();

const agenda = ref<any[]>([])
const fechasEspeciales = ref<any[]>([])
const tipoVista = ref<'actividades' | 'alquileres'>('actividades')
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
});

const reserva = ref({
  fecha: null as any,
  seleccion: {
    fecha: new Date().toISOString().slice(0, 10),
  },
})


const cambiarFavorito = () => {
  usuarioFinalStore.marcarInstalacionFavorita(instalacion.value.id)
}

async function descargarPDF() {
  try {
    const data = await descargarHorario(instalacion.value.id)

    const blob = new Blob([data], { type: 'application/pdf' })

    const url = window.URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "horarios.pdf"
    a.click()
    window.URL.revokeObjectURL(url)

  } catch (error) {
    console.error("Error descargando PDF:", error)
  }
}

const reservasActuales = computed(() => {
  if (!reserva.value.fecha) return []

  if (reserva.value.fecha.numeroCalles === 0) {
    return reserva.value.fecha.slots || []
  }

  const calle = reserva.value.fecha.calles?.find(
    (c: any) => c.numero === calleSeleccionada.value
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

function filtrarIntervalos(intervalos: any) {
  if (instalacion.value.tipoInstalacion !== 'Piscina') {
    return intervalos
  }

  return intervalos.filter(i => i.calle === calleSeleccionada.value)
}

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

function getClaseIntervalo(intervalo: any) {
  if (tipoVista.value === 'actividades') {
    return {
      'bg-success': intervalo.estado === 'Libre' || !esOcupadoPorPeriodo(intervalo),
      'bg-primary': intervalo.estado === 'Reserva actividad',
      'bg-danger': intervalo.estado === 'Reserva usuario'
    }
  }

  // NUEVO alquileres
  return {
    'bg-success': intervalo.estado === 'Libre',
    'bg-danger': intervalo.estado === 'Reservado',
  }
}


const pavilionDetail = (id: number) => {
  router.push({
    name: 'detalle-pabellon',
    params: { id }
  });
}

const reservar = () => {
  router.push({
    name: 'reservar-instalacion',
    params: { id: instalacion.value.id }
  })
}

const volver = () => {
  router.back();
};

watch(() => periodo, () => {
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

  try {
    const data = await getInstalacionDetalleSinAgenda(id)

    const agendasInstalacion = await Promise.all(
      data.agenda.map((agendaId: number) =>
        getAgendaInstalacion(agendaId)
      )
    )

    const agendaCompleta = agendasInstalacion.flat()
    tiposStore.obtenerTipos()

    agenda.value = agendaCompleta.filter((a: any) => a.dia && !a.fecha)
    fechasEspeciales.value = agendaCompleta
      .filter((a: any) => a.fecha)
      .map((a: any) => ({
        fecha: a.fecha
      }))

    calleSeleccionada.value = data.calles?.[0]?.numero

    instalacion.value = {
      ...data,
      agenda: agenda.value
    }

    const alquileres = await getAlquileresPorDia(id, reserva.value.seleccion.fecha)
    reserva.value.fecha = alquileres
  } catch (e) {
    console.log("Error al obtener la informacion de instalaciones", e);
  }
});
</script>
