<template>
  <div class="min-vh-100 bg-light d-flex align-items-center justify-content-center">
    <div class="container" style="max-width: 700px;">

      <div class="card border-0 shadow-lg rounded-4 p-5 text-center">

        <!-- ICONO -->
        <div class="mb-4">
          <div class="bg-success bg-opacity-10 rounded-circle d-inline-flex align-items-center justify-content-center"
               style="width: 90px; height: 90px;">
            <i class="bi bi-check-lg text-success" style="font-size: 3rem;"></i>
          </div>
        </div>

        <!-- TITULO -->
        <h2 class="fw-bold text-success mb-3">
          {{ t.confirmPayTitle }}
        </h2>

        <p class="text-muted mb-4">
          {{ t.confirmPaySubtitle }}
        </p>

        <!-- RESUMEN -->
        <div v-if="pago" class="text-start mt-4">

          <div class="row mb-2">
            <div class="col-6 fw-semibold">{{ t.concept }}:</div>
            <div class="col-6 text-end">{{ pago.concepto }}</div>
          </div>

          <div class="row mb-2">
            <div class="col-6 fw-semibold">{{ t.basePrice }}:</div>
            <div class="col-6 text-end">{{ pago.coste }} €</div>
          </div>

          <div class="row mb-2" v-if="pago.descuentoAplicado > 0">
            <div class="col-6 fw-semibold text-success">{{ t.discount }}:</div>
            <div class="col-6 text-end text-success">
              - {{ pago.descuentoAplicado }} €
            </div>
          </div>

          <hr>

          <div class="row mb-3">
            <div class="col-6 fw-bold">{{ t.price }}:</div>
            <div class="col-6 text-end fw-bold text-success">
              {{ pago.costeFinal }} €
            </div>
          </div>

          <div class="row mb-2">
            <div class="col-6 fw-semibold">{{ t.date }}:</div>
            <div class="col-6 text-end">
              {{ pago.fecha }}
            </div>
          </div>

          <div class="row mb-4">
            <div class="col-6 fw-semibold">{{ t.payState }}:</div>
            <div class="col-6 text-end">
              <span class="badge bg-success">
                {{ pago.estadoPago }}
              </span>
            </div>
          </div>

        </div>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-4">
          <router-link to="/" class="btn btn-success rounded-3 px-4">
            {{ t.returnHome }}
          </router-link>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, inject, type Ref } from "vue"
import { useRouter } from "vue-router"

import { getPago } from "@/services/reservaPagoService";

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const props = defineProps<{id: string}>();

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const router = useRouter()

const pago = ref()

const irReservas = () => {
  router.push("/reservas-realizadas")
}

const irHome = () => {
  router.push("/")
}

onMounted(async () => {
  const id = parseInt(props.id)

  try {
    pago.value = await getPago(id)
  } catch(e) {
    console.log("Error al obtener el pago", e)
  }
})
</script>
