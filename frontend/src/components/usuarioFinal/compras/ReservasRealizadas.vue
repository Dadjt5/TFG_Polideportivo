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
                  <!-- ICONO SEGÚN TIPO -->
                  <span v-if="reserva.tipo === 'ALQUILER'">
                    <i class="bi bi-building me-2"></i>
                    {{ reserva.instalacion?.nombre }}
                  </span>

                  <span v-else>
                    <i class="bi bi-activity me-2"></i>
                    {{ reserva.actividad?.nombre }}
                  </span>
                </h5>

                <!-- ESTADO -->
                <p class="mb-1 text-muted">
                  <i class="bi bi-info-circle me-1"></i>
                  {{ reserva.estado }}
                </p>

                <!-- DÍAS (solo si es actividad) -->
                <p v-if="reserva.actividad" class="mb-0 text-muted">
                  <i class="bi bi-calendar-event me-1"></i>
                  {{ reserva.actividad.dias.join(", ") }}
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

import { getReservasRealizadas } from "@/services/usuarioFinalService";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

type Reserva = {
  id: number
  estado: string
  tipo: 'ALQUILER' | 'RESERVA'
  descuentos: {
    id: number
  }[]
  actividad: {
    id: number
    nombre: string
    horasSemanales: number
    dias: string[]
    estado: string
  }
  instalacion: {
    id: number
    nombre: string
  }
}

const reservas = ref<Reserva[]>([])

onMounted(async () => {
  try {
    reservas.value = await getReservasRealizadas()
  } catch (e) {
    console.log("Error al obtener las reservas realizadas", e)
  }
})
</script>
