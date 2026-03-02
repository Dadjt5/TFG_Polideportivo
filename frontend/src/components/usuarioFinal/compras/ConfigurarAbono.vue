<template>
  <div class="container py-4">

    <!-- TÍTULO -->
    <div class="text-center mb-4">
      <h2 class="fw-bold">
        Configurar abono
      </h2>
      <p class="text-muted">
        Revisa las opciones antes de continuar al pago
      </p>
    </div>

    <div v-if="abono" class="card shadow-sm">
      <div class="card-body">

        <!-- NOMBRE -->
        <h5 class="fw-bold mb-4">
          {{ abono.nombre }}
        </h5>

        <!-- ========================= -->
        <!-- ABONO DEPORTIVO -->
        <!-- ========================= -->
        <div v-if="esDeportivo">

          <!-- FORMA DE PAGO -->
          <div class="mb-3">
            <label class="form-label fw-semibold">
              Forma de pago
            </label>

            <select class="form-select"
                    v-model="seleccion.forma">
              <option value="MENSUAL">Mensual</option>
              <option value="TOTAL">Pago único</option>
            </select>
          </div>

          <!-- FAMILIAR -->
          <div class="form-check mb-3">
            <input class="form-check-input"
                   type="checkbox"
                   id="familiar"
                   v-model="seleccion.familiar">

            <label class="form-check-label"
                   for="familiar">
              Abono familiar
            </label>
          </div>

          <!-- PRECIOS BASE -->
          <div class="table-responsive mb-4">
            <table class="table table-sm">
              <tbody>
                <tr>
                  <td>Mensual UAM</td>
                  <td class="text-end">
                    {{ abono.precioTotalMensual }} €
                  </td>
                </tr>

                <tr>
                  <td>Mensual Otros</td>
                  <td class="text-end">
                    {{ abono.precioTotalMensualOtros }} €
                  </td>
                </tr>

                <tr>
                  <td>Pago único UAM</td>
                  <td class="text-end">
                    {{ abono.precioPagoUnicoUAM }} €
                  </td>
                </tr>

                <tr>
                  <td>Pago único Otros</td>
                  <td class="text-end">
                    {{ abono.precioPagoUnicoOtros }} €
                  </td>
                </tr>

                <tr>
                  <td>Familiar</td>
                  <td class="text-end">
                    {{ abono.precioFamiliar }} €
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

        </div>

        <!-- ========================= -->
        <!-- ABONO VERANO -->
        <!-- ========================= -->
        <div v-else>

          <div class="table-responsive mb-4">
            <table class="table table-sm">
              <tbody>
                <tr>
                  <td>TDA</td>
                  <td class="text-end">
                    {{ abono.precioTDA }} €
                  </td>
                </tr>

                <tr>
                  <td>UAM</td>
                  <td class="text-end">
                    {{ abono.precioUAM }} €
                  </td>
                </tr>

                <tr>
                  <td>Otros</td>
                  <td class="text-end">
                    {{ abono.precioOtros }} €
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

        </div>

        <!-- TOTAL -->
        <div class="border-top pt-3 mt-3">
          <div class="d-flex justify-content-between fs-5">
            <span class="fw-bold">Total</span>
            <span class="fw-bold text-primary">
              {{ total }} €
            </span>
          </div>
        </div>

        <!-- BOTONES -->
        <div class="d-flex justify-content-end gap-2 mt-4">
          <button class="btn btn-outline-secondary"
                  @click="cancelar">
            Cancelar
          </button>

          <button class="btn btn-primary"
                  @click="continuarPago">
            Continuar al pago
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import { useUserStore } from '@/stores/usuarioFinal'

import { comprarAbono } from '@/services/reservaPagoService'
import { getAbonoDeportivoDetalle, getAbonoVeranoDetalle } from '@/services/abonoBonoService'

const router = useRouter()
const route = useRoute()
const usuarioStore = useUserStore()

const id = parseInt(route.params.id as string)
const tipo = route.params.tipo as string

const abono = ref<any>(null)

const seleccion = ref({
  forma: 'TOTAL',
  familiar: false
})

const esDeportivo = computed(() => {
  return tipo === 'abono_deportivo'
})

/* ========================= */
/* CÁLCULO PRECIO            */
/* ========================= */

const total = computed(() => {
  if (!abono.value) return 0

  if (esDeportivo.value) {

    if (seleccion.value.familiar) {
      return abono.value.precioFamiliar
    }

    if (usuarioStore.isUAM) {
      if (seleccion.value.forma === 'MENSUAL') {
        return abono.value.precioTotalMensual
      }
      return abono.value.precioPagoUnicoUAM
    } else {
      if (seleccion.value.forma === 'MENSUAL') {
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

/* ========================= */
/* ACCIONES                  */
/* ========================= */

const continuarPago = async () => {
  const response = await comprarAbono(
    id,
    tipo,
    seleccion.value.forma,
    seleccion.value.familiar
  )

  const idPago = response.data.idPago

  router.push({
    name: 'pasarela-pago',
    params: { tipo: "comprar_abono", id: idPago }
  })
}

function cancelar() {
  router.back()
}

/* ========================= */
/* CARGA DATOS               */
/* ========================= */

onMounted(async () => {
  let data

  if(esDeportivo.value) {
    data = await getAbonoDeportivoDetalle(id)
  } else {
    data = await getAbonoVeranoDetalle(id)
  }
  abono.value = data
})
</script>