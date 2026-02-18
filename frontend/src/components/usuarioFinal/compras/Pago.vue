<template>
  <div class="min-vh-100 bg-light d-flex align-items-center justify-content-center">
    <div class="card shadow-lg p-4" style="width: 500px;">

      <!-- Título -->
      <h3 class="text-center mb-4">Finalizar pago</h3>

      <!-- Resumen reserva -->
      <div class="mb-3">
        <h5>Resumen</h5>
        <p class="mb-1">
          <strong>Actividad:</strong> {{ resumen.actividad }}
        </p>
        <p class="mb-1">
          <strong>Fecha:</strong> {{ resumen.fecha }}
        </p>
        <p class="mb-1">
          <strong>Precio final:</strong>
          <span class="text-success fw-bold">
            {{ resumen.precio }} €
          </span>
        </p>
      </div>

      <hr />

      <!-- Formulario Stripe -->
      <form @submit.prevent="pagar">

        <div class="mb-3">
          <label class="form-label">Datos de la tarjeta</label>
          <div id="card-element" class="form-control p-2"></div>
        </div>

        <!-- Error -->
        <div v-if="error" class="alert alert-danger">
          {{ error }}
        </div>

        <!-- Botón pagar -->
        <button
          type="submit"
          class="btn btn-primary w-100 mt-3"
          :disabled="loading"
        >
          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
          {{ loading ? "Procesando..." : `Pagar ${resumen.precio} €` }}
        </button>

      </form>

    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue"
import { loadStripe } from "@stripe/stripe-js"
import { useRoute, useRouter } from "vue-router"
import axios from "axios"

const route = useRoute()
const router = useRouter()

const resumen = ref({
  actividad: "",
  fecha: "",
  precio: 0
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
  }
}, 1000)

const pagar = async () => {
  loading.value = true
  error.value = ""

  const result = await stripe.confirmCardPayment(clientSecret, {
    payment_method: {
      card: cardElement
    }
  })

  if (result.error) {
    error.value = result.error.message
    loading.value = false
  } else {
    await axios.post("/api/confirmar-pago/", {
      reserva_id: route.query.reserva_id
    })

    router.push("/reserva-confirmada")
  }
}

onMounted(async () => {
  const reservaId = route.query.reserva_id

  const resumenResponse = await axios.get(`/api/reserva/${reservaId}/`)
  resumen.value = resumenResponse.data

  const pagoResponse = await axios.post("/api/crear-intento-pago/", {
    reserva_id: reservaId
  })

  clientSecret = pagoResponse.data.client_secret

  stripe = await loadStripe("pk_test_TU_PUBLIC_KEY")

  const elements = stripe.elements()
  cardElement = elements.create("card")
  cardElement.mount("#card-element")
})
</script>
