<template>
  <div class="min-vh-100 bg-light d-flex align-items-center justify-content-center">
    <div class="card shadow-lg p-5 text-center" style="max-width: 600px; width: 100%;">

      <!-- Icono éxito -->
      <div class="mb-4">
        <i class="bi bi-check-circle-fill text-success" style="font-size: 4rem;"></i>
      </div>

      <!-- Título -->
      <h2 class="text-success mb-3">{{ t.reservationConfirmed }}</h2>

      <!-- Mensaje -->
      <p class="mb-4">
        {{ t.thankYouMessage }}
      </p>

      <hr />

      <!-- Datos del pago/reserva -->
      <div class="text-start mt-4">
        <!-- Nombre del recurso -->
        <p>
          {{ reserva.nombre }}
        </p>

        <!-- Descuento aplicado -->
        <p>
          <strong>{{ t.discount }}:</strong> {{ reserva.pago.descuentoAplicado }} %
        </p>

        <!-- Precio final -->
        <p>
          <strong>{{ t.price }}:</strong> 
          {{ reserva.pago.costeFinal.toFixed(2) }} €
        </p>

        <!-- Estado del pago -->
        <p>
          <strong>{{ t.status }}:</strong> 
          <span 
            class="badge" 
            :class="{
              'bg-success': reserva.pago.estadoPago === 'PAGADO',
              'bg-warning': reserva.pago.estadoPago === 'PENDIENTE',
              'bg-danger': reserva.pago.estadoPago === 'CANCELADO'
            }"
          >
            {{ reserva.pago.estadoPago }}
          </span>
        </p>
      </div>

      <!-- Botones -->
      <div class="mt-5 d-flex justify-content-center gap-3">
        <button class="btn btn-primary" @click="irReservas">
          {{ t.myBookings }}
        </button>

        <button class="btn btn-outline-secondary" @click="irHome">
          {{ t.home }}
        </button>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, inject, type Ref } from "vue"
import { useRouter } from "vue-router"

import { getReservaActividadSimplificado } from "@/services/reservaPagoService";

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const props = defineProps<{id: string}>();

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const router = useRouter()

const reserva = ref({
	id: 0,
	estado: '',
	nombre: '',
	pago: {
		concepto: '',
    coste: 0.0,
    costeFinal: 0.0,
    descuentoAplicado: 0.0,
    fecha: '',
    estadoPago: '',    
	}
})

const irReservas = () => {
  router.push("/reservas-realizadas")
}

const irHome = () => {
  router.push("/")
}

onMounted(async () => {
  const reservaId = parseInt(props.id)

  const response = await getReservaActividadSimplificado(reservaId)
  reserva.value = response.data
})
</script>
