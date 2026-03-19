<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center"
       style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <div class="container" style="max-width: 700px;">

      <!-- TÍTULO -->
      <div class="text-center mb-4">
        <h2 class="fw-bold text-primary mb-1" style="text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">
          {{ t.configurationSubscription }}
        </h2>
        <p class="text-muted">{{ t.configurationSubscSubtitle }}</p>
      </div>

      <div v-if="abono" class="card shadow-lg rounded-4 p-4 card-hover"
           style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(8px);">

        <div class="card-body">

          <!-- NOMBRE -->
          <h5 class="fw-bold mb-4">{{ abono.nombre }}</h5>

          <!-- ABONO DEPORTIVO -->
          <div v-if="esDeportivo">

            <!-- FORMA DE PAGO -->
            <div class="mb-3">
              <label class="form-label fw-semibold">{{ t.paymentMethod }}</label>
              <select class="form-select" v-model="seleccion.forma" :disabled="seleccion.familiar">
                <option value="Pago mensual">{{ t.monthly }}</option>
                <option value="Pago unico">{{ t.fullPayment }}</option>
              </select>
            </div>

            <!-- FAMILIAR -->
            <div class="form-check mb-3">
              <input class="form-check-input" type="checkbox" id="familiar" v-model="seleccion.familiar">
              <label class="form-check-label fw-semibold" for="familiar">{{ t.family }}</label>
            </div>

            <!-- PRECIOS BASE -->
            <div class="table-responsive mb-4">
              <table class="table table-sm table-hover">
                <tbody>
                  <tr
                    :class="{ 'table-primary fw-bold': !seleccion.familiar && usuarioStore.isUAM && seleccion.forma === 'Pago mensual' && abono.precioTotalMensual === total }">
                    <td>{{ t.monthlyPriceUAM }}</td>
                    <td class="text-end">{{ abono.precioTotalMensual }} €</td>
                  </tr>

                  <tr
                    :class="{ 'table-primary fw-bold': !seleccion.familiar && !usuarioStore.isUAM && seleccion.forma === 'Pago mensual' && abono.precioTotalMensualOtros === total }">
                    <td>{{ t.monthlyPriceOthers }}</td>
                    <td class="text-end">{{ abono.precioTotalMensualOtros }} €</td>
                  </tr>

                  <tr
                    :class="{ 'table-primary fw-bold': !seleccion.familiar && usuarioStore.isUAM && seleccion.forma === 'Pago unico' && abono.precioPagoUnicoUAM === total }">
                    <td>{{ t.totalPriceUAM }}</td>
                    <td class="text-end">{{ abono.precioPagoUnicoUAM }} €</td>
                  </tr>

                  <tr
                    :class="{ 'table-primary fw-bold': !seleccion.familiar && !usuarioStore.isUAM && seleccion.forma === 'Pago unico' && abono.precioPagoUnicoOtros === total }">
                    <td>{{ t.totalPriceOthers }}</td>
                    <td class="text-end">{{ abono.precioPagoUnicoOtros }} €</td>
                  </tr>

                  <tr :class="{ 'table-primary fw-bold': seleccion.familiar && abono.precioFamiliar === total }">
                    <td>{{ t.family }}</td>
                    <td class="text-end">{{ abono.precioFamiliar }} €</td>
                  </tr>
                </tbody>
              </table>
            </div>

          </div>

          <!-- ABONO VERANO -->
          <div v-else>
            <div class="table-responsive mb-4">
              <table class="table table-sm table-hover">
                <tbody>
                  <tr>
                    <td>TDA</td>
                    <td class="text-end">{{ abono.precioTDA }} €</td>
                  </tr>
                  <tr>
                    <td>UAM</td>
                    <td class="text-end">{{ abono.precioUAM }} €</td>
                  </tr>
                  <tr>
                    <td>{{ t.others }}</td>
                    <td class="text-end">{{ abono.precioOtros }} €</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- TOTAL -->
          <div class="border-top pt-3 mt-3">
            <div class="d-flex justify-content-between fs-5">
              <span class="fw-bold">{{ t.price }}</span>
              <span class="fw-bold text-primary">{{ total }} €</span>
            </div>
          </div>

          <!-- BOTONES -->
          <div class="d-flex justify-content-end gap-2 mt-4">
            <button class="btn btn-outline-secondary" @click="cancelar">{{ t.cancel }}</button>
            <button class="btn btn-primary" @click="continuarPago">{{ t.payContinue }}</button>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { type Ref, ref, computed, onMounted, inject } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import { useUserStore } from '@/stores/usuarioFinal'
import { comprarAbono } from '@/services/reservaPagoService'
import { getAbonoDeportivoDetalle, getAbonoVeranoDetalle } from '@/services/abonoBonoService'

import { useI18n } from "@/useI18N"
import type { Language } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const router = useRouter()
const route = useRoute()
const usuarioStore = useUserStore()

const id = Number(route.params.id)
const tipo = String(route.params.tipo)

const abono = ref<any>(null)

const seleccion = ref({
  forma: 'Pago unico',
  familiar: false
})

const esDeportivo = computed(() => {
  return tipo === 'abono_deportivo'
})

const total = computed(() => {
  if (!abono.value) return 0

  if (esDeportivo.value) {

    if (seleccion.value.familiar) {
      return abono.value.precioFamiliar
    }

    if (usuarioStore.isUAM) {
      if (seleccion.value.forma === 'Pago mensual') {
        return abono.value.precioTotalMensual
      }
      return abono.value.precioPagoUnicoUAM
    } else {
      if (seleccion.value.forma === 'Pago mensual') {
        return abono.value.precioTotalMensualOtros
      }
      return abono.value.precioPagoUnicoOtros
    }
  }

  // Abono verano
  if (usuarioStore.hasTda) {
    return abono.value.precioTDA
  } else if (usuarioStore.isUAM) {
    return abono.value.precioUAM
  }

  return abono.value.precioOtros
})


const continuarPago = async () => {
  const response = await comprarAbono(
    id,
    tipo,
    seleccion.value.forma,
    seleccion.value.familiar
  )

  const idPago = response.idPago

  router.push({
    name: 'pasarela-pago',
    params: { tipo: "comprar_abono", id: idPago }
  })
}

function cancelar() {
  router.back()
}


onMounted(async () => {
  let data

  if (esDeportivo.value) {
    data = await getAbonoDeportivoDetalle(id)
  } else {
    data = await getAbonoVeranoDetalle(id)
  }
  abono.value = data
})
</script>