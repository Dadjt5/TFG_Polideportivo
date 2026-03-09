<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container py-5">

      <!-- TITULO -->
      <div class="text-center mb-5">
        <h1 class="fw-bold text-primary mb-0" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
          <i class="bi bi-calendar-check me-2"></i>{{ t.myBookings }}
        </h1>
      </div>

      <!-- SIN RESERVAS -->
      <div v-if="reservas.length === 0" class="text-center text-muted mt-5">
        <i class="bi bi-calendar-x fs-1"></i>
        <p class="mt-3">{{ t.noBookings }}</p>
      </div>

      <!-- LISTA DE RESERVAS -->
      <div v-else class="row g-4">
        <div
          v-for="reserva in reservas"
          :key="reserva.id"
          class="col-md-6 col-lg-4"
        >
          <div class="rounded-3 shadow-sm p-4 h-100 card-hover"
               style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(8px);">

            <div class="d-flex flex-column justify-content-between h-100">

              <!-- INFO PRINCIPAL -->
              <div>
                <h5 class="fw-semibold mb-2 d-flex align-items-center">
                  <i v-if="reserva.tipo === 'ALQUILER'" class="bi bi-building me-2 text-primary"></i>
                  <i v-else class="bi bi-activity me-2 text-success"></i>

                  {{ reserva.tipo === "ALQUILER"
                    ? reserva.instalacion?.nombre
                    : reserva.actividad?.nombre }}
                </h5>

                <!-- ESTADO -->
                <span
                  class="badge rounded-pill"
                  :class="
                    reserva.estado === 'ACTIVO'
                      ? 'bg-success-subtle text-success'
                      : 'bg-secondary-subtle text-secondary'
                  "
                >
                  {{ reserva.estado }}
                </span>

                <!-- DIAS ACTIVIDAD -->
                <p v-if="reserva.actividad" class="mt-3 mb-0 text-muted small">
                  <i class="bi bi-calendar-event me-1"></i>
                  {{ reserva.actividad.dias.join(", ") }}
                </p>

                <!-- MENSAJE SI NO PUEDE CANCELAR -->
                <p v-if="!puedeCancelar(reserva)" class="mt-2 small text-muted">
                  {{ t.cannotCancel }}
                </p>
              </div>

              <!-- BOTON CANCELAR -->
              <div class="mt-4 text-end">
                <button
                  class="btn btn-danger btn-sm rounded-pill px-3"
                  :disabled="!puedeCancelar(reserva)"
                  @click="cancelarReserva(reserva)"
                >
                  <i class="bi bi-x-circle me-1"></i>
                  {{ t.cancel }}
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
import { useConfiguracionStore } from "@/stores/configuracion"

import { useI18n } from "@/useI18N"
import type { Language } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

type Reserva = {
  id: number
  estado: string
  tipo: "ALQUILER" | "RESERVA"
  puede_cancelar?: boolean
  actividad?: {
    id: number
    nombre: string
    dias: string[]
  }
  instalacion?: {
    id: number
    nombre: string
  }
}

const configuracionStore = useConfiguracionStore();
const reservas = ref<Reserva[]>([])

const puedeCancelar = (reserva: Reserva) => {
  if (reserva.estado !== "ACTIVO") return false

  if (!reserva.actividad) return reserva.tipo === "ALQUILER" ? true : false

  const hoy = new Date()

  const primerDiaProximoMes = new Date(hoy.getFullYear(), hoy.getMonth() + 1, 1)

  const fechaLimiteCancelar = new Date(primerDiaProximoMes)
  fechaLimiteCancelar.setDate(fechaLimiteCancelar.getDate() - configuracionStore.dias_minimo_cancelacion)

  return hoy >= fechaLimiteCancelar && hoy < primerDiaProximoMes
}

const cancelarReserva = async (reserva: Reserva) => {

  if (!puedeCancelar(reserva)) return

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

onMounted(async () => {
  try {
    reservas.value = await getReservasRealizadas()
  } catch (e) {
    console.error("Error al obtener reservas", e)
  }
})
</script>

<style scoped>
.booking-card {
  transition: all 0.2s ease;
}

.booking-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.08);
}

.badge {
  font-size: 0.75rem;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>