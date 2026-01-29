<template>
  <div class="container py-4">
    <div class="text-center mb-4">
      <h2 class="fw-bold">Reserva de instalación</h2>
      <p class="text-muted">
        Selecciona un máximo de 2 horas consecutivas
      </p>
    </div>

    <!-- INFO INSTALACIÓN -->
    <div class="card shadow-sm mb-4">
      <div class="card-body">
        <h5 class="fw-bold mb-2">{{ instalacion.nombre }}</h5>
        <p class="mb-0">
          Horario: {{ apertura }}:00 - {{ cierre }}:00
        </p>
      </div>
    </div>

    <!-- HORARIOS -->
    <div class="card shadow-sm">
      <div class="card-body">

        <h5 class="fw-bold mb-3">Horario disponible</h5>

        <div class="d-flex flex-wrap gap-2">
          <button
            v-for="hora in horas"
            :key="hora"
            class="btn"
            :class="claseHora(hora)"
            :disabled="estaBloqueada(hora)"
            @click="toggleHora(hora)"
          >
            {{ hora }}:00 - {{ hora + 1 }}:00
          </button>
        </div>

        <!-- LEYENDA -->
        <div class="mt-4">
          <span class="badge bg-success me-2">Libre</span>
          <span class="badge bg-primary me-2">Seleccionado</span>
          <span class="badge bg-danger me-2">Reservado</span>
          <span class="badge bg-warning text-dark">Actividad</span>
        </div>

        <!-- ACCIONES -->
        <div class="d-flex justify-content-end mt-4 gap-2">
          <button class="btn btn-outline-secondary" @click="cancelar">
            Cancelar
          </button>

          <button
            class="btn btn-primary"
            :disabled="horasSeleccionadas.length === 0"
            @click="continuar"
          >
            Continuar
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

/* ===============================
   DATOS DE LA INSTALACIÓN
================================ */
const instalacion = {
  id: 1,
  nombre: 'Pista Polideportiva'
}

const apertura = 8
const cierre = 22

/* ===============================
   HORAS YA OCUPADAS
   (esto vendrá del backend)
================================ */

// Alquileres de usuarios
const horasReservadas = [10, 11, 18]

// Actividades dirigidas
const horasActividades = [16, 17]

/* ===============================
   GENERAR HORAS DISPONIBLES
================================ */
const horas = ref<number[]>([])

for (let h = apertura; h < cierre; h++) {
  horas.value.push(h)
}

/* ===============================
   SELECCIÓN USUARIO
================================ */
const horasSeleccionadas = ref<number[]>([])

/* ===============================
   MÉTODOS
================================ */
const estaBloqueada = (hora: number) => {
  return (
    horasReservadas.includes(hora) ||
    horasActividades.includes(hora)
  )
}

const claseHora = (hora: number) => {
  if (horasSeleccionadas.value.includes(hora)) {
    return 'btn-primary'
  }

  if (horasReservadas.includes(hora)) {
    return 'btn-danger'
  }

  if (horasActividades.includes(hora)) {
    return 'btn-warning'
  }

  return 'btn-outline-success'
}

const toggleHora = (hora: number) => {
  if (estaBloqueada(hora)) return

  if (horasSeleccionadas.value.includes(hora)) {
    horasSeleccionadas.value =
      horasSeleccionadas.value.filter(h => h !== hora)
    return
  }

  // Máximo 2 horas
  if (horasSeleccionadas.value.length >= 2) return

  // Deben ser consecutivas
  if (
    horasSeleccionadas.value.length === 1 &&
    Math.abs(horasSeleccionadas.value[0] - hora) !== 1
  ) {
    return
  }

  horasSeleccionadas.value.push(hora)
  horasSeleccionadas.value.sort()
}

const continuar = () => {
  router.push({
    name: 'resumen-alquiler',
    state: {
      instalacionId: instalacion.id,
      horas: horasSeleccionadas.value
    }
  })
}

const cancelar = () => {
  router.back()
}
</script>
