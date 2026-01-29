<template>
  <div class="container py-4">

    <!-- TÍTULO -->
    <div class="text-center mb-4">
      <h2 class="fw-bold">{{ t.activityBookingTitle }}</h2>
      <p class="text-muted">
        {{ t.activityBookingSubtitle }}
      </p>
    </div>

    <!-- CARD -->
    <div class="card shadow-sm">
      <div class="card-body">

        <!-- DATOS ACTIVIDAD -->
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

        <table class="table table-sm mb-4">
          <thead>
            <tr>
              <th class="text-end">{{ t.prices }}</th>
            </tr>
          </thead>
          <tbody>
            <tr :class="{ 'table-primary': usuarioFinalStore.hasAbono }">
              <td>{{ t.subscription }}</td>
              <td class="text-end">{{ reserva.tarifa.precioAbonado }} €</td>
            </tr>
            <tr :class="{ 'table-primary': usuarioFinalStore.isUAM }">
              <td>UAM</td>
              <td class="text-end">{{ reserva.tarifa.precioUAM }} €</td>
            </tr>
            <tr :class="{ 'table-primary': usuarioFinalStore.hasTda }">
              <td>TDA</td>
              <td class="text-end">{{ reserva.tarifa.precioTDA }} €</td>
            </tr>
            <tr :class="{ 'table-primary': otroCaso }">
              <td>{{ t.other }}</td>
              <td class="text-end">{{ reserva.tarifa.precioOtros }} €</td>
            </tr>
          </tbody>
        </table>

        <!-- DESCUENTO -->
        <div
          v-if="reserva.descuento.porcentaje"
          class="alert alert-success py-2"
        >
          {{ t.discount }}:
          <strong>
            {{ reserva.descuento.nombre }}
            ({{ reserva.descuento.porcentaje }}%)
          </strong>
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

        <!-- ACCIONES -->
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
  descuentos: [] as {
    id: number
    nombre: string
    porcentaje: number
  }[]
})


function obtenerPrecioUsuario(precios: any) {
  if (usuarioFinalStore.hasAbono) return precios.abonado
  if (usuarioFinalStore.isUAM) return precios.uam
  if (usuarioFinalStore.hasTda) return precios.tda
  return precios.otros
}

const precioBase = computed(() => {
  const tipo = reserva.value.tarifa.tipo
  const datos = reserva.value.tarifa.datos
  const sel = reserva.value.seleccion

  if (tipo === 'actividad_comun') {
    return obtenerPrecioUsuario(datos)
  }

  if (tipo === 'grupo_reducido') {
    return datos.precio * sel.personas
  }

  if (tipo === 'fisioterapia') {
    return 0
  }

  return 0
})

const total = computed(() => {
  const base = precioBase.value
  const descuento = (base * reserva.value.descuento.porcentaje) / 100
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
