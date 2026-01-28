<template>
  <div class="container py-4">

    <!-- TÍTULO -->
    <div class="text-center mb-4">
      <h2 class="fw-bold">{{ t.activityBookingTitle }}</h2>
      <p class="text-muted">
        {{ t.activityBookingSubtitle }}
      </p>
    </div>

    <!-- CARD RESUMEN -->
    <div class="card shadow-sm">
      <div class="card-body">

        <h5 class="fw-bold mb-3">{{ t.bookingData }}</h5>

        <ul class="list-group list-group-flush mb-4">
          <li class="list-group-item d-flex justify-content-between">
            <span class="fw-semibold">
              {{ reserva.actividad.nombre }}
            </span>
          </li>

          <li
            class="list-group-item d-flex justify-content-between"
          >
            <span>{{ t.days }}</span>
            <span class="fw-semibold">
              {{ reserva.actividad.dias }}
            </span>
          </li>

          <li
            class="list-group-item d-flex justify-content-between"
          >
            <span>{{ t.timetable }}</span>
            <span class="fw-semibold">
              {{ reserva.actividad.horasSemanales }}
            </span>
          </li>

          <li class="list-group-item d-flex justify-content-between">
            <span>{{ t.tariff }}</span>
            <span class="fw-semibold">
              {{ reserva.tarifa }} €
            </span>
          </li>

          <li
            v-if="reserva.descuento"
            class="list-group-item d-flex justify-content-between text-success"
          >
            <span>{{ t.discount }}</span>
            <span>- {{ reserva.descuento }} €</span>
          </li>

          <li class="list-group-item d-flex justify-content-between fs-5">
            <span class="fw-bold">{{ t.price }}</span>
            <span class="fw-bold">
              €
            </span>
          </li>
        </ul>

        <!-- ACCIONES -->
        <div class="d-flex justify-content-end gap-2">
          <button
            class="btn btn-outline-secondary"
            @click="cancelar"
          >
            {{ t.cancel }}
          </button>

          <button
            class="btn btn-primary"
            @click="continuarPago"
          >
            {{ t.payContinue }}
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { inject, type Ref, ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { getReservaActividad } from '../services/reservaPagoService';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter()

const reserva = ref({
  id: 0,
  actividad: {
    id: 0,
    nombre: '',
    horasSemanales: '',
    dias: '',
    estado: ''
  },
  tarifa: {
    precioAbonado: 0,
    precioUAM: 0,
    precioTDA: 0,
    precioOtros: 0
  },
  descuento: {
    nombre: '',
    porcentaje: 0
  }
})

function continuarPago() {
  router.push('/pago')
}

function cancelar() {
  router.back()
}

onMounted(async () => {
  const id = parseInt(props.id);
  reserva.value = await getReservaActividad(id);
});
</script>
