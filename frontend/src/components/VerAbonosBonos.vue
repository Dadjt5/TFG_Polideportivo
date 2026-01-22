<template>
  <div class="min-vh-100 bg-light">
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
            <div class="card h-100 shadow-sm rounded-4">
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
                  <div
                    class="progress-bar"
                    role="progressbar"
                    :style="{ width: porcentajeUso(b) + '%' }"
                  ></div>
                </div>

                <p>
                  <strong>{{ t.expires }}:</strong>
                  {{ new Date(b.fechaExpiracion).toLocaleDateString() }}
                </p>
              </div>
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
            <div class="card h-100 shadow-sm rounded-4 p-2">
              <div class="card-body">
                <h3 class="h5 fw-semibold mb-3">
                  <i class="bi bi-info-circle text-primary me-2 fs-4"></i>
                  <span v-if="a.abonoDeportivo">
                    {{ t.sportsSubscription }}
                  </span>
                  <span v-else>
                    {{ t.summerSubscription }}
                  </span>
                </h3>

                <p><strong>{{ t.startDate }}:</strong> {{ a.fecha }}</p>
                <p><strong>{{ t.endDate }}:</strong> {{ a.fechaExpiracion }}</p>

                <p>
                  <strong>{{ t.remainingDays }}:</strong>
                  {{ a.diasRestantes }}
                </p>
  
                <span
                  class="badge"
                  :class="a.valido ? 'bg-success' : 'bg-secondary'"
                >
                  {{ a.valido ? t.active : t.expires }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, inject, type Ref } from 'vue'

import { getAbonos, getBonos } from '../services/usuarioFinalService'

import type { Language } from "../useI18N"
import { useI18n } from "../useI18N"

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
  fechaExpiracion: string
  valido: boolean
  diasRestantes: number
  pago: number
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

onMounted(async () => {
  try {
    bonos.value = await getBonos();
    abonos.value = await getAbonos();
  } catch(e) {
    console.log("Error al obtener los bonos o abonos comprados", e)
  }
})
</script>
