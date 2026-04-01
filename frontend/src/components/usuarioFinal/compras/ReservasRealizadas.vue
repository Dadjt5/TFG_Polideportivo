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
        <div v-for="reserva in reservas" :key="reserva.id" class="card-hover rounded-4 shadow-sm p-4 mb-4" :class="{
          'border-start border-4 border-primary bg-primary-subtle': reserva.tipo === 'ALQUILER',
          'border-start border-4 border-success bg-success-subtle': reserva.tipo === 'RESERVA',
          'border-start border-4 border-warning bg-warning-subtle': reserva.tipo === 'LISTA_ESPERA'
        }">
          <!-- HEADER -->
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="mb-0 fw-semibold">
              {{ reserva.actividad?.nombre || reserva.instalacion?.nombre }}
            </h5>

            <span v-if="reserva.tipo === 'ALQUILER'" class="badge bg-primary">
              {{ t.rent }}
            </span>
            <span v-else-if="reserva.tipo === 'RESERVA'" class="badge bg-success">
              {{ t.booking }}
            </span>
            <span v-else-if="reserva.tipo === 'LISTA_ESPERA'" class="badge bg-warning text-dark">
              {{ t.waitingList }}
            </span>
          </div>

          <!-- INFO DETALLADA -->
          <div class="text-muted small mb-2">

            <!-- ALQUILER -->
            <template v-if="reserva.tipo === 'ALQUILER'">
              <p class="mb-1"><i class="bi bi-calendar-event me-1 text-primary"></i>{{ t.date }}: {{ reserva.fecha }}
              </p>
              <p class="mb-1"><i class="bi bi-clock me-1 text-success"></i>{{ t.hours }}: {{ reserva.horaInicio }} - {{
                reserva.horaFin }}</p>
              <p class="mb-1"><i class="bi bi-building me-1 text-primary"></i>{{ t.facilityType }}: {{
                reserva.instalacion?.tipo }}</p>
            </template>

            <!-- RESERVA -->
            <template v-else-if="reserva.tipo === 'RESERVA'">
              <p class="mb-1"><i class="bi bi-calendar-event me-1 text-success"></i>{{ t.days }}:</p>
              <ul class="mb-1">
                <li v-for="sesion in reserva.actividad?.dias" :key="sesion.dia">
                  {{ sesion.dia }} ({{ sesion.horaInicio }} - {{ sesion.horaFin }})
                </li>
              </ul>
              <p class="mb-1"><i class="bi bi-clock me-1 text-success"></i>{{ t.weekHours }}: {{
                reserva.actividad?.horasSemanales }}</p>
              <p v-if="reserva.descuentos?.length" class="mb-0">
                <i class="bi bi-percent me-1 text-success"></i>{{ t.discounts }}:
                <span v-for="d in reserva.descuentos" :key="d.id">{{ d.nombre }} ({{ d.porcentaje }}%)</span>
              </p>
            </template>

            <!-- LISTA DE ESPERA -->
            <template v-else-if="reserva.tipo === 'LISTA_ESPERA'">
              <p class="mb-2">
                <span class="badge bg-warning text-dark fs-6 px-3 py-2 shadow-sm">
                  <i class="bi bi-trophy me-1"></i>
                  {{ t.position }}: {{ reserva.posicion }}
                </span>
              </p>

              <p class="mb-1"><i class="bi bi-calendar-event me-1 text-warning"></i>{{ t.days }}:</p>
              <ul class="mb-1">
                <li v-for="sesion in reserva.actividad?.dias" :key="sesion.dia">
                  {{ sesion.dia }} ({{ sesion.horaInicio }} - {{ sesion.horaFin }})
                </li>
              </ul>

              <p class="mb-1"><i class="bi bi-clock me-1"></i>{{ t.weekHours }}: {{
                reserva.actividad?.horasSemanales }}</p>
              <p class="mb-0">
                <i class="bi bi-info-circle me-1"></i>{{ t.waitingListInfo }}
              </p>
            </template>

          </div>

          <!-- ACCIONES -->
          <div class="mt-3 d-flex gap-2">
            <button v-if="reserva.puede_cancelar && reserva.tipo !== 'LISTA_ESPERA'" class="btn btn-outline-danger btn-sm" @click="abrirConfirmacion(reserva)">
              {{ t.cancel }}
            </button>

            <button v-if="reserva.tipo === 'LISTA_ESPERA'" class="btn btn-outline-danger btn-sm" @click="abrirConfirmacionLista(reserva)">
              {{ t.leaveWaitingList }}
            </button>
          </div>
        </div>
      </div>

      <div class="modal fade" id="confirmDeleteModal" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content rounded-4">

            <div class="modal-header">
              <h5 class="modal-title">{{ t.confirmDelete }}</h5>
            </div>

            <div class="modal-body text-center">
              <p>{{ t.confirmReservationDelete }}</p>
            </div>

            <div class="modal-footer justify-content-center">
              <button class="btn btn-secondary rounded-pill" data-bs-dismiss="modal">
                {{ t.cancel }}
              </button>

              <button class="btn btn-danger rounded-pill" @click="cancelarReserva">
                {{ t.delete }}
              </button>
            </div>

          </div>
        </div>
      </div>

      <div class="modal fade" id="confirmDeleteModalLista" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content rounded-4">

            <div class="modal-header">
              <h5 class="modal-title">{{ t.confirmExit }}</h5>
            </div>

            <div class="modal-body text-center">
              <p>{{ t.confirmLeaveListDelete }}</p>
            </div>

            <div class="modal-footer justify-content-center">
              <button class="btn btn-secondary rounded-pill" data-bs-dismiss="modal">
                {{ t.cancel }}
              </button>

              <button class="btn btn-danger rounded-pill" @click="salirListaEspera">
                {{ t.leave }}
              </button>
            </div>

          </div>
        </div>
      </div>

      <div class="modal fade" id="successDeleteModal" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content rounded-4 text-center">

            <div class="modal-body py-5">

              <i v-if="eliminado" class="bi bi-check-circle-fill text-success fs-1 mb-3"></i>
              <i v-else class="bi bi-exclamation-octagon-fill text-danger fs-1 mb-3"></i>

              <h4 class="fw-semibold">
                {{ mensaje }}
              </h4>

              <button class="btn btn-primary rounded-pill mt-4" @click="finalizar" data-bs-dismiss="modal">
                <span v-if="eliminado">{{ t.continue }}</span>
                <span v-else>{{ t.return }}</span>
              </button>

            </div>

          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, inject, type Ref } from "vue"
import { Modal } from 'bootstrap'

import { getReservasRealizadas } from "@/services/usuarioFinalService"
import { cancelarReservaActividad, cancelarAlquiler, salirLista } from "@/services/cancelarService"
import { useConfiguracionStore } from "@/stores/configuracion"

import { useI18n } from "@/useI18N"
import type { Language } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

type Reserva = {
  id: number
  estado: string
  tipo: "ALQUILER" | "RESERVA" | "LISTA_ESPERA"
  puede_cancelar?: boolean
  posicion: number

  actividad?: {
    id: number
    nombre: string
    dias?: {
      dia: string,
      horaInicio: string,
      horaFin: string,
    }[],
    horasSemanales?: number,
    periodo: string
  }
  instalacion?: {
    id: number
    nombre: string
    tipo?: string
  }

  fecha?: string
  horaInicio?: string | number
  horaFin?: string | number
  tarifa?: {
    id?: number
    nombre?: string
  }
  descuentos?: {
    id: number
    nombre: string
    porcentaje: number
  }[]
}

const configuracionStore = useConfiguracionStore();
const reservas = ref<Reserva[]>([])
const mensaje = ref("")
const eliminado = ref(false)

let confirmModal: Modal
let confirmModalLista: Modal
let successModal: Modal

const puedeCancelar = (reserva: Reserva) => {
  if (reserva.estado !== "Confirmada") return false

  if (!reserva.actividad) return reserva.tipo === "ALQUILER" ? true : false

  const hoy = new Date()
  const mesProximo = hoy.getMonth() + 2

  if (reserva.actividad.periodo === "Desde septiembre hasta enero") {
    if (mesProximo < 9 && mesProximo !== 1) {
      return false
    }
  } else if (reserva.actividad.periodo === "Desde febrero hasta mayo") {
    if (mesProximo < 2 || mesProximo > 5) {
      return false
    }
  } else if (reserva.actividad.periodo === "Meses de verano") {
    if (mesProximo < 6 || mesProximo > 8) {
      return false
    }
  }

  const primerDiaProximoMes = new Date(hoy.getFullYear(), hoy.getMonth() + 1, 1)

  const fechaLimiteCancelar = new Date(primerDiaProximoMes)
  fechaLimiteCancelar.setDate(fechaLimiteCancelar.getDate() - configuracionStore.dias_minimo_cancelacion)

  return hoy >= fechaLimiteCancelar && hoy < primerDiaProximoMes
}

const reservaElegida = ref()

function abrirConfirmacion(reserva: Reserva) {
  reservaElegida.value = reserva
  confirmModal.show()
}

function abrirConfirmacionLista(reserva: Reserva) {
  reservaElegida.value = reserva
  confirmModalLista.show()
}

function finalizar() {
  successModal.hide()
}

const cancelarReserva = async () => {
  const reserva = reservaElegida.value

  if (!puedeCancelar(reserva)) return

  try {
    if (reserva.tipo === "ALQUILER") {
      await cancelarAlquiler(reserva.id)
    } else if (reserva.tipo === "RESERVA") {
      await cancelarReservaActividad(reserva.id)
    } else {
      return
    }

    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.reservationDeleted
    eliminado.value = true
    reservas.value = reservas.value.filter(r => r.id !== reserva.id)
    reservaElegida.value = null
  } catch (e) {
    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.reservationNoDeleted
    eliminado.value = false
    reservaElegida.value = null
    console.error("Error cancelando reserva", e)
  }
}

const salirListaEspera = async () => {
  const reserva = reservaElegida.value

  try {
    if (reserva.tipo === "LISTA_ESPERA") {
      await salirLista(reserva.id)
    } else {
      return
    }

    confirmModalLista.hide()
    successModal.show()

    mensaje.value = t.value.reservationDeleted
    eliminado.value = true
    reservas.value = reservas.value.filter(r => r.id !== reserva.id)
    reservaElegida.value = null
  } catch (e) {
    confirmModalLista.hide()
    successModal.show()

    mensaje.value = t.value.reservationNoDeleted
    eliminado.value = false
    reservaElegida.value = null
    console.error("Error cancelando reserva", e)
  }
}

onMounted(async () => {
  confirmModal = new Modal(document.getElementById('confirmDeleteModal')!)
  confirmModalLista = new Modal(document.getElementById('confirmDeleteModalLista')!)
  successModal = new Modal(document.getElementById('successDeleteModal')!)

  try {
    reservas.value = await getReservasRealizadas()
    configuracionStore.obtenerConfiguracion()
  } catch (e) {
    mensaje.value = t.value.unexpectedError
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