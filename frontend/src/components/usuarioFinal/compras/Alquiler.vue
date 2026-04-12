<template>
  <div class="container py-4">

    <!-- TÍTULO -->
    <div class="text-center mb-4">
      <h2 class="fw-bold">{{ t.facilityReservationTitle }}</h2>
      <p class="text-muted">{{ t.facilityReservationRule }}: {{ configuracionStore.horas_alquiler_consecutivas }}</p>
    </div>

    <!-- INFO INSTALACIÓN -->
    <div class="card shadow-sm rounded-4 mb-4" style="backdrop-filter: blur(6px); background: rgba(255,255,255,0.85);">
      <div class="card-body">
        <h5 class="fw-bold mb-2 fs-3">{{ reserva.tarifa.nombre }}</h5>
        <p v-if="reserva.tarifa.abierto" class="mb-0 fs-4 text-primary">
          {{ t.timetable }}: {{ reserva.tarifa.horaApertura }} - {{ reserva.tarifa.horaCierre }}
        </p>
        <p v-else class="mb-0 fs-4 text-danger">
          {{ t.close }}
        </p>
      </div>
    </div>

    <!-- HORARIOS Y TARIFAS -->
    <div class="card shadow-sm rounded-4" style="backdrop-filter: blur(6px); background: rgba(255,255,255,0.85);">
      <div class="card-body">

        <!-- TARIFAS -->
        <h5 class="fw-bold mb-2">{{ t.tariff }}</h5>

        <div class="mb-3">
          <label class="form-label">{{ t.selectedDate }}</label>
          <input type="date" class="form-control" v-model="reserva.seleccion.fecha" :min="minFecha"
            :max="maxFecha" />
        </div>

        <div v-if="reserva.tarifa.numeroCalles > 0" class="mb-3">
          <label class="form-label">{{ t.poolStreet }}</label>

          <select class="form-select" v-model="reserva.seleccion.calle">
            <option v-for="calle in reserva.tarifa.calles" :key="calle.numero" :value="calle.numero">
              {{ t.poolStreet }} {{ calle.numero }}
            </option>
          </select>
        </div>

        <h6 class="fw-bold">{{ t.prices }}</h6>
        <table class="table table-sm mb-4">
          <tbody>
            <tr :class="{ 'table-primary': usuarioFinalStore.hasAbono }">
              <td>{{ t.subscription }}</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.precioAbonado }} € × {{ horasSeleccionadas.length }}
                = {{ (reserva.tarifa.datos.precioAbonado * horasSeleccionadas.length).toFixed(2) }} €
              </td>
            </tr>
            <tr :class="{ 'table-primary': usuarioFinalStore.isUAM && !usuarioFinalStore.hasAbono }">
              <td>UAM</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.precioUAM }} € × {{ horasSeleccionadas.length }}
                = {{ (reserva.tarifa.datos.precioUAM * horasSeleccionadas.length).toFixed(2) }} €
              </td>
            </tr>
            <tr :class="{ 'table-primary': usuarioFinalStore.hasTda && !usuarioFinalStore.isUAM}">
              <td>TDA</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.precioTDA }} € × {{ horasSeleccionadas.length }}
                = {{ (reserva.tarifa.datos.precioTDA * horasSeleccionadas.length).toFixed(2) }} €
              </td>
            </tr>
            <tr :class="{ 'table-primary': otroCaso }">
              <td>{{ t.others }}</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.precioOtros }} € × {{ horasSeleccionadas.length }}
                = {{ (reserva.tarifa.datos.precioOtros * horasSeleccionadas.length).toFixed(2) }} €
              </td>
            </tr>
          </tbody>
        </table>

        <!-- DESCUENTOS -->
        <div v-if="reserva.descuento.aplicados.length" class="alert alert-success py-2">
          <div class="fw-bold mb-1">{{ t.discount }}: {{ reserva.descuento.porcentaje_total }}%</div>
          <ul class="mb-0 ps-3">
            <li v-for="descuento in reserva.descuento.aplicados" :key="descuento.id">
              {{ descuento.nombre }} ({{ descuento.porcentaje }}%)
            </li>
          </ul>
        </div>

        <!-- LUZ -->
        <div v-if="reserva.tarifa.tieneLuz" class="form-check mb-3">
          <input class="form-check-input" type="checkbox" id="luzCheck" v-model="reserva.seleccion.luz">
          <label class="form-check-label" for="luzCheck">
            {{ t.light }}
          </label>
        </div>

        <!-- TOTAL -->
        <div class="pt-3 mt-3 border-top">
          <div class="d-flex justify-content-between fs-5">
            <span class="fw-bold">{{ t.price }}</span>
            <span class="fw-bold text-primary">{{ total }} €</span>
          </div>
        </div>

        <!-- HORARIOS -->
        <h5 class="fw-bold mt-3 mb-3">{{ t.timetable }}</h5>

        <div v-if="!error" class="d-flex flex-wrap gap-2">
          <button v-for="hora in reservasActuales" :key="hora.horaInicio" class="btn btn-outline-primary"
            :class="claseHora(hora)" :disabled="estaBloqueada(hora)" @click="toggleHora(hora)">
            {{ hora.horaInicio }} - {{ hora.horaFin }}
          </button>
        </div>

        <!-- LEYENDA -->
        <div class="mt-4 d-flex flex-wrap gap-2">
          <span class="badge bg-success">{{ t.free }}</span>
          <span class="badge bg-primary">{{ t.selected }}</span>
          <span class="badge bg-danger">{{ t.reserved }}</span>
          <span class="badge bg-warning text-dark">{{ t.activity }}</span>
        </div>

        <div v-if="mostrarMensaje" class="text-center mb-3 mt-3">
          <div class="alert" :class="tipoMensaje === 'success' ? 'alert-success' : 'alert-danger'">
            {{ mensaje }}
          </div>
        </div>

        <!-- ACCIONES -->
        <div class="d-flex justify-content-end mt-4 gap-2">
          <button class="btn btn-outline-secondary" @click="cancelar">{{ t.cancel }}</button>
          <button class="btn btn-primary" :disabled="horasSeleccionadas.length === 0" @click="continuarPago">
            {{ t.continue }}
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { computed, watch, onMounted, inject, type Ref, ref } from 'vue'
import { useRouter } from 'vue-router'

import { alquilar, getTarifaDescuentoInstalacion } from '@/services/reservaPagoService';
import { useUserStore } from '@/stores/usuarioFinal'
import { useConfiguracionStore } from '@/stores/configuracion';
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);
const router = useRouter();

const usuarioFinalStore = useUserStore();
const configuracionStore = useConfiguracionStore();

const otroCaso = ref(false)

type ReservaMapa = {
  horaInicio: string;
  horaFin: string;
  estado: 'Libre' | 'Reserva usuario' | 'Reserva actividad';
};

type CalleMapa = {
  numero: number;
  reservas: ReservaMapa[];
};

const reserva = ref({
  tarifa: {
    idInstalacion: 0,
    nombre: '',
    horaApertura: '',
    horaCierre: '',
    tieneLuz: '',
    abierto: true,
    numeroCalles: 0,
    datos: {} as any,
    reservas: [] as {
      horaInicio: string,
      horaFin: string,
      periodo: string,
      estado: 'Libre' | 'Reserva usuario' | 'Reserva actividad'
    }[],
    alquileres: [] as {
      id: number,
      fecha: string,
      horaFin: string,
      horaInicio: string,
      nombre: string,
      numeroHoras: number
    }[],
    calles: [] as CalleMapa[]
  },
  seleccion: {
    fecha: new Date().toISOString().slice(0, 10),
    calle: 1,
    luz: false
  },
  descuento: {
    porcentaje_total: 0,
    aplicados: [] as {
      id: number
      nombre: string
      porcentaje: number
    }[]
  }
})

const horasSeleccionadas = ref<string[]>([])
const mensaje = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)


function periodoPorFecha(fechaStr: string) {
  const fecha = new Date(fechaStr)
  const mes = fecha.getMonth() + 1

  if (mes >= 9 || mes === 1) return "Desde septiembre hasta enero"
  if (mes >= 2 && mes <= 5) return "Desde febrero hasta mayo"
  if (mes >= 6 && mes <= 8) return "Meses de verano"
  return "Todo el año"
}



function esActividadValida(intervalo: any, fecha: string) {
  const periodoActual = periodoPorFecha(fecha)

  return (
    intervalo.estado === "Reserva actividad" &&
    (intervalo.periodo.includes(periodoActual) || intervalo.periodo.includes("Todo el año"))
  )
}

const claseHora = (hora: any) => {
  if (esAlquilerUsuario(hora)) return "bg-danger text-white"
  if (esActividadValida(hora, reserva.value.seleccion.fecha)) return "bg-warning text-dark"
  
  return horasSeleccionadas.value.includes(hora.horaInicio)
    ? "bg-primary text-white"
    : "bg-success text-white"
}

// Se debe revisar si es una piscina o no, si lo es se deben mostrar las reservas por calle
const reservasActuales = computed(() => {

  if (reserva.value.tarifa.numeroCalles === 0)
    return reserva.value.tarifa.reservas

  const calle = reserva.value.tarifa.calles.find(
    c => c.numero === reserva.value.seleccion.calle
  )

  return calle ? calle.reservas : []

})

// Mínimo y máximo de fecha
const minFecha = computed(() => {
  const fecha = new Date()
  fecha.setDate(fecha.getDate() + (configuracionStore.dias_minimo_alquiler || 0))
  return fecha.toISOString().slice(0, 10)
})

const maxFecha = computed(() => {
  const fecha = new Date()
  const dias = configuracionStore.dias_maximo_alquiler || 7

  fecha.setDate(fecha.getDate() + dias)

  if (isNaN(fecha.getTime())) return ''

  return fecha.toISOString().slice(0, 10)
})

const estaBloqueada = (hora: any) => {
  if (!reserva.value.seleccion.fecha) return true

  if (esAlquilerUsuario(hora)) return true
  if (esActividadValida(hora, reserva.value.seleccion.fecha)) return true

  const hoy = new Date()

  const fechaSeleccionada = new Date(reserva.value.seleccion.fecha)
  const esHoy = hoy.toISOString().slice(0, 10) === fechaSeleccionada.toISOString().slice(0, 10)

  if (fechaSeleccionada < new Date(minFecha.value) || fechaSeleccionada > new Date(maxFecha.value)) {
    return true
  }

  if (esHoy) {
    const [h, m] = hora.horaInicio.split(":").map(Number)
    const horaReserva = new Date()
    horaReserva.setHours(h, m, 0, 0)
    if (horaReserva < hoy) return true
  }

  return false
}

const esAlquilerUsuario = (hora: any) => {
  const fechaSeleccionada = reserva.value.seleccion.fecha
  return reserva.value.tarifa.alquileres.some(a => {
    if (a.fecha !== fechaSeleccionada) return false
    return hora.horaInicio >= a.horaInicio && hora.horaInicio < a.horaFin
  })
}

const toggleHora = (intervalo: any) => {
  if (estaBloqueada(intervalo)) return

  const fechaSeleccionada = new Date(reserva.value.seleccion.fecha)
  fechaSeleccionada.setHours(0, 0, 0, 0)

  const fechaMin = new Date()

  fechaMin.setDate(fechaMin.getDate() + (configuracionStore.dias_minimo_alquiler))
  fechaMin.setHours(0, 0, 0, 0)

  const fechaMax = new Date()
  fechaMax.setDate(fechaMax.getDate() + (configuracionStore.dias_maximo_alquiler))
  fechaMax.setHours(0, 0, 0, 0)

  if (fechaSeleccionada < fechaMin || fechaSeleccionada > fechaMax) return

  const key = intervalo.horaInicio
  if (horasSeleccionadas.value.includes(key)) {
    horasSeleccionadas.value = horasSeleccionadas.value.filter(h => h !== key)
    return
  }

  if (horasSeleccionadas.value.length >= configuracionStore.horas_alquiler_consecutivas) return

  if (horasSeleccionadas.value.length === 0) {
    horasSeleccionadas.value.push(key)
    return
  }

  const horas = reserva.value.tarifa.reservas.map(r => r.horaInicio)
  const indexActual = horas.indexOf(key)
  const indexSeleccionada = horas.indexOf(horasSeleccionadas.value[0])

  if (Math.abs(indexActual - indexSeleccionada) === 1) {
    horasSeleccionadas.value.push(key)
    horasSeleccionadas.value.sort()
  }
}

const total = computed(() => {
  let base = reserva.value.tarifa.datos.precioOtros
  otroCaso.value = true

  if (usuarioFinalStore.hasAbono) {
    base = reserva.value.tarifa.datos.precioAbonado
    otroCaso.value = false
  } else if (usuarioFinalStore.isUAM) {
    base = reserva.value.tarifa.datos.precioUAM
    otroCaso.value = false
  } else if (usuarioFinalStore.hasTda) {
    base = reserva.value.tarifa.datos.precioTDA
    otroCaso.value = false
  }

  base = base * horasSeleccionadas.value.length

  if (reserva.value.seleccion.luz) {
    base = base + reserva.value.tarifa.datos.costeIluminacion
  }

  const descuento = (base * reserva.value.descuento.porcentaje_total) / 100
  return base - descuento
})

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensaje.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true

  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
}


const continuarPago = async () => {
  const complementos = {
    fecha: reserva.value.seleccion.fecha,
    horas: horasSeleccionadas.value,
    calle: reserva.value.seleccion.calle,
    luz: reserva.value.seleccion.luz
  }

  try {
    const response = await alquilar(reserva.value.tarifa.idInstalacion, { complementos })
    const idPago = response.idPago

    router.push({
      name: 'pasarela-pago',
      params: { tipo: "alquiler_instalacion", id: idPago }
    })
  } catch (e) {
    lanzarMensaje(t.value.noFacilityReservation, "error")
    console.error("Error al alquilar:", e);
  }
}

const cancelar = () => {
  router.back()
}

watch(
  () => reserva.value.seleccion.fecha,
  async (nuevaFecha) => {
    if (!nuevaFecha) return;
    mensaje.value = ""
    horasSeleccionadas.value = []

    try {
      const id = parseInt(props.id);
      const data = await getTarifaDescuentoInstalacion(id, reserva.value.seleccion.fecha)
      reserva.value.tarifa = data.tarifa
      reserva.value.descuento = data.descuento
    } catch (e: any) {
      lanzarMensaje(t.value.unexpectedError, "error")
      console.error("Error al actualizar la fecha:", e);
    }
  }
);

watch(
  () => reserva.value.seleccion.calle,
  () => {
    horasSeleccionadas.value = []
  }
);

const error = ref(false)

onMounted(async () => {
  const id = parseInt(props.id);
  try {
    const data = await getTarifaDescuentoInstalacion(id, reserva.value.seleccion.fecha)
    configuracionStore.obtenerConfiguracion()
    reserva.value.tarifa = data.tarifa
    reserva.value.descuento = data.descuento
    console.log(data)
  } catch (e: any) {
    error.value = true
    console.error("Error al actualizar la fecha:", e);
  }
});
</script>