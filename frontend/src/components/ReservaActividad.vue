<template>
  <div class="container py-4">

    <!-- TÍTULO -->
    <div class="text-center mb-4">
      <h2 class="fw-bold">{{ t.activityBookingTitle }}</h2>
      <p class="text-muted">
        {{ t.activityBookingSubtitle }}
      </p>
    </div>

    <div class="card shadow-sm">
      <div class="card-body">

        <h5 class="fw-bold mb-3">{{ props.nombre }}</h5>

        <ul class="list-group list-group-flush mb-4">
          <li class="list-group-item d-flex justify-content-between">
            <span>{{ t.days }}</span>
            <span class="fw-semibold">{{ props.dias }}</span>
          </li>

          <li class="list-group-item d-flex justify-content-between">
            <span>{{ t.timetable }}</span>
            <span class="fw-semibold">{{ props.horasSemanales }}</span>
          </li>
        </ul>

        <!-- TARIFAS -->
        <h6 class="fw-bold mb-2">{{ t.tariff }}</h6>

        <table v-if="reserva.tarifa.tipo === 'ACTIVIDAD_COMUN'" class="table table-sm mb-4">
          <tbody>
            <tr :class="{ 'table-primary': usuarioFinalStore.isUAM }">
              <td>UAM</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.precioUAM }} €
              </td>
            </tr>

            <tr :class="{ 'table-primary': !usuarioFinalStore.isUAM }">
              <td>{{ t.other }}</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.precioOtros }} €
              </td>
            </tr>
          </tbody>
        </table>

        <table v-else-if="reserva.tarifa.tipo === 'GRUPOS_REDUCIDOS'" class="table table-sm mb-4">
          <tbody>
            <tr>
              <td>{{ t.hours }}</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.numeroHoras }}
              </td>
            </tr>

            <tr>
              <td>{{ t.people }}</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.numeroPersonas }}
              </td>
            </tr>

            <tr>
              <td>{{ t.monthly }}</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.precioMensual }} €
              </td>
            </tr>

            <tr>
              <td>{{ t.quarterly }}</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.precioCuatrimestre }} €
              </td>
            </tr>
          </tbody>
        </table>

        <table v-else-if="reserva.tarifa.tipo === 'FISIO'" class="table table-sm mb-4">
          <tbody>
            <tr>
              <td>{{ t.initialConsultation }}</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.precioConsultaUAM }} €
              </td>
            </tr>

            <tr>
              <td>{{ t.sessions1to5 }}</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.precioSesiones1_5UAM }} €
              </td>
            </tr>

            <tr>
              <td>{{ t.sessions6plus }}</td>
              <td class="text-end">
                {{ reserva.tarifa.datos.precioSesiones6UAM }} €
              </td>
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
        <div class="border-top pt-3 mt-3">
          <div class="d-flex justify-content-between fs-5">
            <span class="fw-bold">{{ t.price }}</span>
            <span class="fw-bold">
              {{ total }} €
            </span>
          </div>
        </div>

        <div class="d-flex justify-content-end gap-2 mt-4">
          <button class="btn btn-outline-secondary" @click="cancelar">
            {{ t.cancel }}
          </button>
          <button class="btn btn-primary" @click="continuarPago">
            {{ t.payContinue }}
          </button>
        </div>

      </div>
    </div>

  </div>
</template>


<script setup lang="ts">
import { computed, inject, type Ref, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { getTarifaDescuento } from '../services/reservaPagoService';

import { useUserStore } from '../stores/usuarioFinal'

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const props = defineProps<{
  id: string
  nombre: string
  dias: string
  horasSemanales: string
}>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();
const usuarioFinalStore = useUserStore();

const otroCaso = ref(true)

const reserva = ref({
  tarifa: {
    tipo: '',
    datos: {} as any
  },
  seleccion: {},
  descuento: {
    porcentaje_total: 0,
    aplicados: [] as {
      id: number
      nombre: string
      porcentaje: number
    }[]
  }
})

function obtenerPrecioComun(precios: any) {
  let precio = precios.precioOtros;
  if (usuarioFinalStore.isUAM) {
    precio = precios.precioUAM;
  }

  const horas = parseInt(props.horasSemanales);
  const mult = horas / precios.numeroHorasSemana;

  return precio * mult;
}

function obtenerPrecioGrupo(precios: any, sel: any) {
  let precio = precios.precioMensual;
  if (!sel.mensual) {
    precio = precios.precioCuatrimestre;
  }

  // Necesitamos calcular cuanto debe subir el precio o bajar en relacion a los parametros definidos en la tarifa
  const horas = parseInt(props.horasSemanales);
  const mult1 = horas / precios.numeroHoras;
  const mult2 = precios.numeroPersonas / sel.numeroPersonas;

  return precio * mult1 * mult2;
}

function obtenerPrecioFisioterapia(precios: any) {
  let precio = precios.precioOtros;
  if (usuarioFinalStore.hasTda) {
    precio = precios.precioTDA;
  } else if (usuarioFinalStore.isUAM) {
    precio = precios.precioUAM;
  }

  return precio
}

const precioBase = computed(() => {
  const tipo = reserva.value.tarifa.tipo;
  const datos = reserva.value.tarifa.datos;
  const sel = reserva.value.seleccion;

  if (tipo === 'Actividad comun') {
    return obtenerPrecioComun(datos);
  }

  if (tipo === 'Grupos reducidos') {
    return obtenerPrecioGrupo(datos, sel)
  }

  if (tipo === 'Fisioterapia') {
    return obtenerPrecioFisioterapia(datos)
  }

  return 0
})

const total = computed(() => {
  const base = precioBase.value
  const descuento = (base * reserva.value.descuento.porcentaje_total) / 100
  return base - descuento
})

function continuarPago() {
  router.push('/pago')
}

function cancelar() {
  router.back()
}

onMounted(async () => {
  const id = parseInt(props.id);
  reserva.value = await getTarifaDescuento(id);
});
</script>
