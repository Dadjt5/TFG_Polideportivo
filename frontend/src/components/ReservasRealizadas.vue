<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-5">
      <div class="text-center mb-5">
        <h1 class="fw-bold">{{ t.myBookings }}</h1>
      </div>

      <div v-if="reservas.length === 0" class="text-center text-muted mt-5">
        <i class="bi bi-calendar-x fs-1"></i>
        <p class="mt-3">{{ t.noBookings }}</p>
      </div>

      <!-- LISTA DE RESERVAS -->
      <div v-else class="row g-4">
        <div v-for="reserva in reservas" :key="reserva.id" class="col-12">
          <div class="card shadow-sm rounded-4">
            <div class="card-body d-flex justify-content-between align-items-center">

              <div>
                <h5 class="mb-1">
                  <span v-if="reserva.tipo === 'alquiler'">
                    <i class="bi bi-building me-2"></i>
                  </span>
                  <span v-else>
                    <i class="bi bi-activity me-2"></i>
                  </span>
                  {{ reserva.titulo }}
                </h5>

                <p class="mb-1 text-muted">
                  <i class="bi bi-calendar-event me-1"></i>
                  {{ reserva.fechaInicio }}
                </p>

                <p class="mb-0 text-muted">
                  <i class="bi bi-credit-card me-1"></i>
                  {{ reserva.pago.coste }} €
                </p>

              </div>
            </div>
          </div>
        </div>
      </div>

    </main>
  </div>
</template>


<script setup lang="ts">
import { onMounted, type Ref, ref, inject, computed } from "vue"

import { getReservasRealizadas } from "../services/usuarioFinalService";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

type Reservas = {
  id: number
  tipo: 'alquiler' | 'actividad'
  fechaInicio: string
  titulo: string
  id_obj: number
  horario: string
  dias: string
  pago: {
    coste: number
    estadoPago: string
  }
}

const reservas = ref<Reservas[]>([])

onMounted(async () => {
  try {
    reservas.value = await getReservasRealizadas()
  } catch(e) {
    console.log("Error al obtener las reservas realizadas", e)
  }
})
</script>
