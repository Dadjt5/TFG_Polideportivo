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

      <div v-else class="row g-4">
        <div v-for="reserva in reservas" :key="reserva.id" class="col-md-6 col-lg-4">
          <div class="card shadow-sm rounded-4 h-100">
            <div class="card-body d-flex flex-column justify-content-between">

              <!-- INFO PRINCIPAL -->
              <div>
                <h5 class="fw-semibold mb-2">
                  <span v-if="reserva.tipo === 'ALQUILER'">
                    <i class="bi bi-building me-2"></i>{{ reserva.instalacion?.nombre }}
                  </span>
                  <span v-else>
                    <i class="bi bi-activity me-2"></i>{{ reserva.actividad?.nombre }}
                  </span>
                </h5>

                <!-- ESTADO -->
                <span class="badge" :class="reserva.estado === 'ACTIVO' ? 'bg-success' : 'bg-secondary'">
                  {{ reserva.estado }}
                </span>

                <!-- DÍAS (solo actividades) -->
                <p v-if="reserva.actividad" class="mt-2 mb-0 text-muted small">
                  <i class="bi bi-calendar-event me-1"></i>
                  {{ reserva.actividad.dias.join(", ") }}
                </p>
              </div>

              <!-- BOTONES -->
              <div class="mt-3 text-end">
                <button class="btn btn-outline-danger btn-sm"
                  @click="cancelarReserva(reserva)">
                  <i class="bi bi-x-circle me-1"></i>{{ t.cancel }}
                </button>
              </div>

            </div>
          </div>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, inject, type Ref } from "vue"

import { getReservasRealizadas } from "@/services/usuarioFinalService"
import { cancelarReservaActividad, cancelarAlquiler } from "@/services/cancelarService"

import { useI18n } from "@/useI18N"
import type { Language } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

type Reserva = {
  id: number
  estado: string
  tipo: 'ALQUILER' | 'RESERVA'
  actividad?: { id: number, nombre: string, dias: string[] }
  instalacion?: { id: number, nombre: string }
}

const reservas = ref<Reserva[]>([])

onMounted(async () => {
  try {
    reservas.value = await getReservasRealizadas()
  } catch (e) {
    console.error("Error al obtener reservas", e)
  }
})

const cancelarReserva = async (reserva: Reserva) => {
  try {
    if (reserva.tipo === "ALQUILER") {
      await cancelarAlquiler(reserva.id)
    } else {
      await cancelarReservaActividad(reserva.id)
    }

    reservas.value = reservas.value.filter(r => r.id !== reserva.id)

  } catch (e) {
    console.error("Error cancelando reserva", e)
  }
}
</script>