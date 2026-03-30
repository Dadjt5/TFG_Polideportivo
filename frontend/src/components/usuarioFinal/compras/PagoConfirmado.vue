<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center"
       style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">

    <div class="container" style="max-width: 700px;">

      <div class="card rounded-4 shadow-lg border-0 p-5 card-hover text-center"
           style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(8px);">

        <!-- ICONO -->
        <div class="mb-4">
          <div class="bg-success bg-opacity-10 rounded-circle d-inline-flex align-items-center justify-content-center"
               style="width: 90px; height: 90px;">
            <i class="bi bi-check-lg text-success" style="font-size: 3rem;"></i>
          </div>
        </div>

        <!-- TITULO -->
        <h2 class="fw-bold text-success mb-3" style="text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">
          {{ t.confirmPayTitle }}
        </h2>

        <p class="text-muted mb-4">{{ t.confirmPaySubtitle }}</p>

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
            <div class="col-6 text-end text-success">- {{ pago.descuentoAplicado }} €</div>
          </div>

          <hr class="my-3">

          <div class="row mb-3">
            <div class="col-6 fw-bold">{{ t.price }}:</div>
            <div class="col-6 text-end fw-bold text-success">{{ pago.costeFinal }} €</div>
          </div>

          <div class="row mb-2">
            <div class="col-6 fw-semibold">{{ t.date }}:</div>
            <div class="col-6 text-end">{{ pago.fecha }}</div>
          </div>

          <div class="row mb-4">
            <div class="col-6 fw-semibold">{{ t.payState }}:</div>
            <div class="col-6 text-end">
              <span class="badge bg-success rounded-pill">{{ pago.estadoPago }}</span>
            </div>
          </div>

        </div>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-4">
          <router-link to="/" class="btn btn-success rounded-3 px-5 py-2">
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

import { confirmarPago, getPago } from "@/services/reservaPagoService";
import { useUserStore } from "@/stores/usuarioFinal";

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const props = defineProps<{id: string}>();

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const router = useRouter();
const usuarioFinalStore = useUserStore();

const pago = ref()

onMounted(async () => {
  const id = parseInt(props.id)

  try {
    await confirmarPago(id)
    pago.value = await getPago(id)
    usuarioFinalStore.fetchUser(usuarioFinalStore.usuarioFinal.id)
  } catch(e) {
    console.log("Error al confirmar el pago", e)
  }
})
</script>
