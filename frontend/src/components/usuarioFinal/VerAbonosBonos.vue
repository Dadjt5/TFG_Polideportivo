<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container py-4">

      <!-- TÍTULO -->
      <h1 class="text-center fw-bold mb-5">
        <i class="bi bi-wallet2 text-primary me-2 fs-1"></i>
        {{ t.mySubscripcions }}
      </h1>

      <!-- BONOS -->
      <section class="mb-5">
        <h2 class="fw-semibold mb-3">
          <i class="bi bi-ticket-detailed text-primary me-2"></i>
          {{ t.bonus }}
        </h2>

        <div v-if="bonos.length === 0" class="text-muted text-center fs-4">
          {{ t.noBonus }}
        </div>

        <div class="row g-4">
          <div class="col-md-6" v-for="b in bonos" :key="b.id">
            <div class="card h-100 rounded-4" style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(8px);">
              <div class="card-body">
                <p v-if="b.bono.nombreInstalacion">
                  <strong>{{ t.facility }}:</strong> {{ b.bono.nombreInstalacion }}
                </p>
                <p v-else>
                  <strong>{{ t.sport }}:</strong> {{ b.bono.nombreDeporte }}
                </p>

                <p>
                  <strong>{{ t.remainingUses }}:</strong>
                  {{ b.usosRestantes }} / {{ b.bono.usos }}
                </p>

                <div class="progress mb-3" style="height: 8px;">
                  <div class="progress-bar bg-primary" role="progressbar" :style="{ width: porcentajeUso(b) + '%' }"></div>
                </div>

                <p>
                  <strong>{{ t.expires }}:</strong>
                  {{ new Date(b.fechaExpiracion).toLocaleDateString() }}
                </p>
              </div>
            </div>
            <div class="mt-3 text-end" v-if="b.valido">
              <button class="btn btn-outline-danger btn-sm" @click="abrirConfirmacion(b.id, 'bono')">
                <i class="bi bi-x-circle me-1"></i>
                {{ t.cancel }}
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- ABONOS -->
      <section>
        <h2 class="fw-semibold mb-3">
          <i class="bi bi-calendar text-primary me-2"></i>
          {{ t.subscription }}
        </h2>

        <div v-if="abonos.length === 0" class="text-muted text-center fs-4">
          {{ t.noSubscripcion }}
        </div>

        <div class="row g-4">
          <div class="col-md-6" v-for="a in abonos" :key="a.id">
            <div class="card h-100 rounded-4 p-2" style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(8px);">
              <div class="card-body">
                <h3 class="h5 fw-semibold mb-3">
                  <i class="bi bi-info-circle text-primary me-2 fs-4"></i>
                  <span v-if="a.abonoDeportivo">{{ t.sportsSubscription }}</span>
                  <span v-else>{{ t.summerSubscription }}</span>
                </h3>

                <p><strong>{{ t.startDate }}:</strong> {{ fechaInicio(a) }}</p>
                <p><strong>{{ t.endDate }}:</strong> {{ fechaFin(a) }}</p>

                <p><strong>{{ t.remainingDays }}:</strong> {{ diasRestantes(a) }}</p>

                <span class="badge" :class="esValido(a) ? 'bg-success' : 'bg-secondary'">
                  {{ esValido(a) ? t.active : t.expires }}
                </span>
              </div>
            </div>

            <div class="mt-3 text-end" v-if="esValido(a)">
              <button class="btn btn-outline-danger btn-sm" @click="abrirConfirmacion(a.id, 'abono')">
                <i class="bi bi-x-circle me-1"></i>
                {{ t.cancel }}
              </button>
            </div>
          </div>
        </div>
      </section>

    <div class="modal fade" id="confirmDeleteModalBono" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4">

          <div class="modal-header">
            <h5 class="modal-title">{{ t.confirmDelete }}</h5>
          </div>

          <div class="modal-body text-center">
            <p>{{ t.confirmDeleteBonus }}</p>
          </div>

          <div class="modal-footer justify-content-center">
            <button class="btn btn-secondary rounded-pill" data-bs-dismiss="modal">
              {{ t.cancel }}
            </button>

            <button class="btn btn-danger rounded-pill" @click="cancelarCompraBono">
              {{ t.deleteUser }}
            </button>
          </div>

        </div>
      </div>
    </div>

    <div class="modal fade" id="confirmDeleteModalAbono" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4">

          <div class="modal-header">
            <h5 class="modal-title">{{ t.confirmDelete }}</h5>
          </div>

          <div class="modal-body text-center">
            <p>{{ t.confirmDeleteSubscription }}</p>
          </div>

          <div class="modal-footer justify-content-center">
            <button class="btn btn-secondary rounded-pill" data-bs-dismiss="modal">
              {{ t.cancel }}
            </button>

            <button class="btn btn-danger rounded-pill" @click="cancelarCompraAbono">
              {{ t.delete }}
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
import { onMounted, ref, inject, type Ref } from 'vue'
import { Modal } from 'bootstrap'

import { getAbonos, getBonos } from '@/services/usuarioFinalService'
import { cancelarAbono, cancelarBono } from '@/services/cancelarService'

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

type BonoComprado = {
  id: number
  bono: {
    id: number,
    usos: number,
    nombreInstalacion: string,
    nombreDeporte: string
  }
  fechaExpiracion: string
  usosRestantes: number
  valido: boolean
  fecha: string
  pago: number
}

const bonos = ref<BonoComprado[]>([])

const porcentajeUso = (b: BonoComprado) =>
  (b.usosRestantes / b.bono.usos) * 100

type AbonoActivo = {
  id: number
  fecha: string
  estado: string
  abonoDeportivo: {
    id: number,
    meses: number
    descuentoPrimeraActividad: number,
    descuentoRestoActividades: number,
    descuentoActividadesExteriores: number,
    precioTotalMensual: number,
    precioPagoUnicoUAM: number,
    precioFamiliar: number,
    precioTotalMensualOtros: number,
    precioPagoUnicoOtros: number
  }
  abonoVerano: number
}

const abonos = ref<AbonoActivo[]>([])
const mensaje = ref("")
const eliminado = ref(false)

let confirmModalAbono: Modal
let confirmModalBono: Modal
let successModal: Modal

const getInicioVerano = () => {
  const year = new Date().getFullYear()
  return new Date(year, 5, 1)
}

const getFinVerano = () => {
  const year = new Date().getFullYear()
  return new Date(year, 7, 31)
}

const fechaInicio = (a: AbonoActivo) => {
  if (a.abonoVerano) {
    return getInicioVerano().toLocaleDateString()
  }

  return new Date(a.fecha).toLocaleDateString()
}

const diasRestantes = (a: AbonoActivo) => {
  if (a.abonoVerano) {
    const hoy = new Date()
    const fin = getFinVerano()

    const diff = fin.getTime() - hoy.getTime()
    return Math.max(0, Math.ceil(diff / (1000 * 60 * 60 * 24)))
  }

  return a.diasRestantes
}

const fechaFin = (a: AbonoActivo) => {
  if (a.abonoVerano) {
    return getFinVerano().toLocaleDateString()
  }

  return new Date(a.fechaExpiracion).toLocaleDateString()
}

const esValido = (a: AbonoActivo) => {
  if (a.abonoVerano) {
    return new Date() <= getFinVerano()
  }

  return a.valido
}

const id_objeto = ref()

function abrirConfirmacion(id: number, tipo: string) {
  id_objeto.value = id
  if(tipo == "abono") {
    confirmModalAbono.show()
  } else {
    confirmModalBono.show()
  }
}

function finalizar() {
  successModal.hide()
}

const cancelarCompraBono = async () => {
  const id = id_objeto.value
  try {
    await cancelarBono(id)

    confirmModalBono.hide()
    successModal.show()

    mensaje.value = t.value.bonusDeleted
    eliminado.value = true
    bonos.value = bonos.value.filter(b => b.id !== id)
    id_objeto.value = null
  } catch (e) {
    confirmModalBono.hide()
    successModal.show()

    mensaje.value = t.value.bonusNoDeleted
    eliminado.value = false
    id_objeto.value = null
    console.error("Error cancelando bono", e)
  }
}

const cancelarCompraAbono = async () => {
  const id = id_objeto.value
  try {
    await cancelarAbono(id)

    confirmModalAbono.hide()
    successModal.show()

    mensaje.value = t.value.subscriptionDeleted
    eliminado.value = true
    abonos.value = abonos.value.filter(a => a.id !== id)
    id_objeto.value = null
  } catch (e) {
    confirmModalAbono.hide()
    successModal.show()

    mensaje.value = t.value.subscriptionNoDeleted
    eliminado.value = false
    console.error("Error cancelando abono", e)
    id_objeto.value = null
  }
}

onMounted(async () => {
  confirmModalAbono = new Modal(document.getElementById('confirmDeleteModalAbono')!)
  confirmModalBono = new Modal(document.getElementById('confirmDeleteModalBono')!)
  successModal = new Modal(document.getElementById('successDeleteModal')!)

  try {
    bonos.value = await getBonos();
    abonos.value = await getAbonos();
  } catch (e) {
    console.log("Error al obtener los bonos o abonos comprados", e)
  }
})
</script>
