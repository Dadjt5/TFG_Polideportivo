<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center"
       style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">

    <div class="card rounded-4 shadow-lg p-5 card-hover"
         style="width: 500px; background-color: rgba(255,255,255,0.85); backdrop-filter: blur(8px);">

      <!-- Título -->
      <h3 class="text-center text-primary mb-4 fw-bold" style="text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">
        {{ t.paymentTitle }}
      </h3>

      <!-- Resumen pago -->
      <div class="mb-4">
        <h5 class="fw-semibold">{{ t.reservationSummary }}</h5>

        <!-- Nombre del recurso -->
        <p class="mb-1">{{ resumen.nombre }}</p>

        <!-- Descuento aplicado -->
        <p class="mb-1" v-if="resumen.pago.descuentoAplicado > 0">
          <strong>{{ t.discount }}:</strong>
          <span class="text-success fw-semibold">
            {{ resumen.pago.descuentoAplicado }} %
          </span>
        </p>

        <!-- Precio final -->
        <p class="mb-1">
          <strong>{{ t.price }}: </strong>
          <span class="text-success fw-bold">
            {{ resumen.pago.costeFinal.toFixed(2) }} €
          </span>
        </p>
      </div>

      <hr class="my-3"/>

      <!-- Tiempo restante -->
      <div class="mb-3">
        <div class="alert d-flex align-items-center justify-content-center fw-semibold"
             :class="tiempoRestante <= 60 ? 'alert-danger' : 'alert-warning'">
          <i class="bi bi-hourglass-split me-2"></i>
          {{ t.timeRemaining }}:
          <strong class="ms-1">{{ minutos }}:{{ segundos }}</strong>
        </div>
      </div>

      <!-- Formulario Stripe -->
      <form @submit.prevent="pagar">

        <div class="mb-3">
          <label class="form-label fw-semibold">{{ t.cardInfo }}</label>
          <div id="payment-element" class="rounded-2 p-2"
               style="background-color: rgba(255,255,255,0.95); border: 1px solid #dee2e6;"></div>
        </div>

        <!-- Error -->
        <div v-if="error" class="alert alert-danger rounded-2">
          {{ error }}
        </div>

        <!-- Botón pagar -->
        <button type="submit" class="btn btn-primary w-100 mt-3 rounded-3"
                :disabled="loading">
          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
          {{ loading 
            ? `${t.processing}...` 
            : `${t.payment} ${resumen.pago.costeFinal.toFixed(2)} €` 
          }}
        </button>

      </form>

    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, type Ref, ref, inject } from "vue"
import { useRouter } from "vue-router"
import { loadStripe } from "@stripe/stripe-js"

import { confirmarPago, intentarPago, getResumenPago } from "@/services/reservaPagoService";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{
  tipo: "reserva" | "abono" | "bono",
  id: string
}>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter()

const resumen = ref({
	id: 0,
	estado: '',
	nombre: '',
	pago: {
		concepto: '',
    coste: 0.0,
    costeFinal: 0.0,
    descuentoAplicado: 0.0,
    fecha: '',
    estadoPago: '',    
	}
})

const loading = ref(false)
const error = ref("")

let stripe: any
let cardElement: any
let clientSecret = ""

const tiempoRestante = ref(900)

const countdown = setInterval(() => {
  tiempoRestante.value -= 1

  if (tiempoRestante.value <= 0) {
    clearInterval(countdown)
    error.value = "Se ha cancelado la reserva por tiempo agotado."
    
    setTimeout(() => {
      router.replace("/")
    }, 3000)
  }
}, 1000)

const minutos = computed(() => {
  const m = Math.floor(tiempoRestante.value / 60)
  return m.toString().padStart(2, "0")
})

const segundos = computed(() => {
  const s = tiempoRestante.value % 60
  return s.toString().padStart(2, "0")
})

let elements: any

const pagar = async () => {
  loading.value = true
  error.value = ""

  const { error: stripeError } = await stripe.confirmPayment({
    elements,
    confirmParams: {
      return_url: `${window.location.origin}/pago/finalizado/${props.id}`
    },
  })

  if (stripeError) {
    error.value = stripeError.message
    loading.value = false
  }}

onMounted(async () => {
  try {
    const resumenResponse = await getResumenPago(parseInt(props.id), props.tipo)
    resumen.value = resumenResponse

    const pagoResponse = await intentarPago(parseInt(props.id))
    clientSecret = pagoResponse.client_secret

    stripe = await loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY)

    elements = stripe.elements({ clientSecret })
    const paymentElement = elements.create("payment")
    paymentElement.mount("#payment-element")
    cardElement = paymentElement
  } catch (e) {
    error.value = "Error al cargar el pago"
    console.error(e)
  }
})

</script>
