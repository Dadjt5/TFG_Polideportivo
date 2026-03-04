<template>
  <div class="container py-4">
    <div class="text-center mb-4">
      <h2 class="fw-bold">{{ t.facilityReservationTitle }}</h2>
      <p class="text-muted">
        {{ t.facilityReservationRule }}
      </p>
    </div>

    <!-- INFO INSTALACIÓN -->
    <div class="card shadow-sm mb-4">
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

    <!-- HORARIOS -->
    <div class="card shadow-sm">
      <div class="card-body">

        <!-- TARIFAS -->
        <h5 class="fw-bold mb-2">{{ t.tariff }}</h5>

        <div class="mb-3">
          <label class="form-label">{{ t.selectedDate }}</label>
          <input type="date" class="form-control" v-model="reserva.seleccion.fecha" />
        </div>

        <h6 class="fw-bold">{{ t.prices }}</h6>
        <table class="table table-sm mb-4">
          <tbody>
            <tr :class="{ 'table-primary': usuarioFinalStore.hasAbono }">
              <td>{{ t.subscription }}</td>
              <td class="text-end">{{ reserva.tarifa.datos.precioAbonado }} €</td>
            </tr>
            <tr :class="{ 'table-primary': usuarioFinalStore.isUAM }">
              <td>UAM</td>
              <td class="text-end">{{ reserva.tarifa.datos.precioUAM }} €</td>
            </tr>
            <tr :class="{ 'table-primary': usuarioFinalStore.hasTda }">
              <td>TDA</td>
              <td class="text-end">{{ reserva.tarifa.datos.precioTDA }} €</td>
            </tr>
            <tr :class="{ 'table-primary': otroCaso }">
              <td>{{ t.other }}</td>
              <td class="text-end">{{ reserva.tarifa.datos.precioOtros }} €</td>
            </tr>
          </tbody>
        </table>

        <!-- DESCUENTOS -->
        <div v-if="reserva.descuento.aplicados.length" class="alert alert-success py-2">
          <div class="fw-bold mb-1">
            {{ t.discount }}:
            {{ reserva.descuento.porcentaje_total }}%
          </div>

          <ul class="mb-0 ps-3">
            <li v-for="descuento in reserva.descuento.aplicados" :key="descuento.id">
              {{ descuento.nombre }} ({{ descuento.porcentaje }}%)
            </li>
          </ul>
        </div>

        <!-- TOTAL -->
        <div class="pt-3 mt-3">
          <div class="d-flex justify-content-between fs-5">
            <span class="fw-bold">{{ t.price }}</span>
            <span class="fw-bold">
              {{ total }} €
            </span>
          </div>
        </div>

        <h5 class="fw-bold mt-3 mb-3">{{ t.timetable }}</h5>

        <div v-if="mensaje" class="text-center mt-5 fs-5">
          <p class="text-danger">{{ mensaje }}</p>
        </div>

        <div v-else class="d-flex flex-wrap gap-2">
          <button v-for="hora in reserva.tarifa.reservas" :key="hora.horaInicio" class="btn" :class="claseHora(hora)" :disabled="estaBloqueada(hora)"
            @click="toggleHora(hora)">
            {{ hora.horaInicio }} - {{ hora.horaFin }}
          </button>
        </div>

        <!-- LEYENDA -->
        <div class="mt-4">
          <span class="badge bg-success me-2">{{ t.free }}</span>
          <span class="badge bg-primary me-2">{{ t.selected }}</span>
          <span class="badge bg-danger me-2">{{ t.reserved }}</span>
          <span class="badge bg-warning text-dark">{{ t.activity }}</span>
        </div>

        <!-- ACCIONES -->
        <div class="d-flex justify-content-end mt-4 gap-2">
          <button class="btn btn-outline-secondary" @click="cancelar">
            {{ t.cancel }}
          </button>

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

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{
  id: string
}>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();
const usuarioFinalStore = useUserStore();

const otroCaso = ref(false)

const reserva = ref({
  tarifa: {
    idInstalacion: 0,
    nombre: '',
    horaApertura: '',
    horaCierre: '',
    abierto: true,
    datos: {} as any,
    reservas: [] as {
      horaInicio: string,
      horaFin: string,
      estado: 'LIBRE' | 'USUARIO' | 'ACTIVIDAD'
    }[]
  },
  seleccion: {
    fecha: new Date().toISOString().slice(0, 10),
    horas1: "",
    horas2: "",
    modalidad: 'total',
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

const mensaje = ref("")
const horasSeleccionadas = ref<string[]>([])

const horaATime = (horaStr: string) => {
  return parseInt(horaStr.split(':')[0])
}

const estaBloqueada = (intervalo: any) => {
  return intervalo.estado !== 'LIBRE'
}

const claseHora = (intervalo: any) => {

  if (horasSeleccionadas.value.includes(intervalo.horaInicio)) {
    return 'btn-primary'
  }

  if (intervalo.estado === 'USUARIO') {
    return 'btn-danger'
  }

  if (intervalo.estado === 'ACTIVIDAD') {
    return 'btn-warning'
  }

  return 'btn-outline-success'
}

const toggleHora = (intervalo: any) => {
  if (intervalo.estado !== 'LIBRE') return

  const key = intervalo.horaInicio

  if (horasSeleccionadas.value.includes(key)) {
    horasSeleccionadas.value =
      horasSeleccionadas.value.filter(h => h !== key)
    return
  }

  if (horasSeleccionadas.value.length >= 2) return

  horasSeleccionadas.value.push(key)
}

const total = computed(() => {
  let base = reserva.value.tarifa.datos.precioOtros
  otroCaso.value = true

  if(usuarioFinalStore.hasAbono) {
    base = reserva.value.tarifa.datos.precioAbonado
    otroCaso.value = false
  } else if(usuarioFinalStore.isUAM) {
    base = reserva.value.tarifa.datos.precioUAM
    otroCaso.value = false
  } else if(usuarioFinalStore.hasTda) {
    base = reserva.value.tarifa.datos.precioTDA
    otroCaso.value = false
  }

  const descuento = (base * reserva.value.descuento.porcentaje_total) / 100
  return base - descuento
})

const continuarPago = async () => {
  const complementos = {
    fecha: reserva.value.seleccion.fecha,
    horas: horasSeleccionadas.value
  }

  const response = await alquilar(reserva.value.tarifa.idInstalacion, { complementos })

  const idPago = response.idPago

  router.push({
    name: 'pasarela-pago',
    params: { tipo: "alquiler_instalacion", id: idPago }
  })
}

const cancelar = () => {
  router.back()
}

watch(
  () => reserva.value.seleccion.fecha,
  async (nuevaFecha) => {
    if (!nuevaFecha) return;
    mensaje.value = ""
    try {
      const id = parseInt(props.id);
      const data = await getTarifaDescuentoInstalacion(id, reserva.value.seleccion.fecha)

      reserva.value.tarifa = data.tarifa
      reserva.value.descuento = data.descuento
    } catch (e: any) {
      mensaje.value = e.response?.data?.respuesta
      console.error("Error al actualizar la fecha:", e);
    }
  }
);


onMounted(async () => {
  const id = parseInt(props.id);

  try {
    const data = await getTarifaDescuentoInstalacion(id, reserva.value.seleccion.fecha)

    reserva.value.tarifa = data.tarifa
    reserva.value.descuento = data.descuento
  } catch(e: any) {
    mensaje.value = e.response?.data?.respuesta
    console.error("Error al actualizar la fecha:", e);
  }
});
</script>
