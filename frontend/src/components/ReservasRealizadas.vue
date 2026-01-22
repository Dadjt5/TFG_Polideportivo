<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-5">
      <div class="text-center mb-5">
        <h1 class="fw-bold">{{ t.myBookings }}</h1>
      </div>

      <div v-if="reservas.length === 0" class="text-center text-muted mt-5">
        <i class="bi bi-calendar-x fs-1"></i>
        <p class="mt-3">{{ t.noBookings }}</p>
      </div>

      <!-- LISTA DE RESERVAS -->
      <div v-else class="row g-4">
        <div v-for="reserva in reservasOrdenadas" :key="reserva.id" class="col-12">
          <div class="card shadow-sm rounded-4">
            <div class="card-body d-flex justify-content-between align-items-center">

              <div>
                <h5 class="mb-1">
                  <i class="bi me-2" :class="iconoReserva(reserva)"></i>
                  {{ tituloReserva(reserva) }}
                </h5>

                <p class="mb-1 text-muted">
                  <i class="bi bi-calendar-event me-1"></i>
                  {{ formatearFecha(reserva.fechaInicio) }}
                </p>

                <p class="mb-0 text-muted">
                  <i class="bi bi-credit-card me-1"></i>
                  {{ reserva.pago?.importe }} €
                  <span v-if="reserva.descuento">
                    · {{ reserva.descuento.nombre }}
                  </span>
                </p>
              </div>

              <!-- ESTADO -->
              <span class="badge fs-6" :class="badgeEstado(reserva)">
                {{ textoEstado(reserva) }}
              </span>

            </div>
          </div>
        </div>
      </div>

    </main>
  </div>
</template>


<script setup lang="ts">
import { onMounted, type Ref, ref, inject, computed } from "vue"

import { getReservasRealizadas } from "../services/usuarioFinalService";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const language = inject < Ref < Language >> ("language")!;
const t = useI18n(language);

type Reservas = {
  alquileres: {
    id: number,
    instalacion: number,
    horario: number,
    tarifa: number,
    descuento: number,
    pago: number
  }
  reservasActividades: {
    id: number,
    actividad: number,
    tarifa: number,
    descuento: number,
    pago: number
  }
}

const reservas = ref<Reservas[]>([])

const reservasOrdenadas = computed(() => {
  return [...reservas.value].sort(
    (a, b) => new Date(a.fechaInicio) - new Date(b.fechaInicio)
  )
})

function formatearFecha(fecha) {
  return new Date(fecha).toLocaleString("es-ES", {
    dateStyle: "medium",
    timeStyle: "short"
  })
}

function iconoReserva(reserva) {
  return reserva.actividad ? "bi-person-walking" : "bi-building"
}

function tituloReserva(reserva) {
  return reserva.actividad
    ? reserva.actividad.nombre
    : reserva.instalacion.nombre
}

function textoEstado(reserva) {
  const ahora = new Date()
  const inicio = new Date(reserva.fechaInicio)

  if (inicio > ahora) return "Próxima"
  return "Finalizada"
}

function badgeEstado(reserva) {
  const ahora = new Date()
  const inicio = new Date(reserva.fechaInicio)

  return inicio > ahora
    ? "bg-success"
    : "bg-secondary"
}

onMounted(async () => {
  try {
    reservas.value = await getReservasRealizadas()
  } catch(e) {
    console.log("Error al obtener las reservas realizadas", e)
  }
})

</script>
