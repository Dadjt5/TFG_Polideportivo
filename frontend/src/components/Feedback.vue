<template>
  <div class="min-vh-100 bg-light p-4">
    <div v-if="!isSuperUser">
      <!-- FORMULARIO DE ENVÍO PARA USUARIOS -->
      <div class="card shadow-sm p-4 rounded-4 mx-auto" style="max-width: 600px;">
        <h3 class="fw-bold mb-4 text-center">Enviar Feedback</h3>

        <div class="mb-3">
          <label class="form-label fw-semibold">Tipo de comentario</label>
          <select v-model="tipo" class="form-select">
            <option value="GENERAL">General</option>
            <option value="MEJORA">Mejora</option>
            <option value="BUG">Bug</option>
            <option value="SUGERENCIA">Sugerencia</option>
          </select>
        </div>

        <div class="mb-3">
          <label class="form-label fw-semibold">Valoración</label>
          <div>
            <span
              v-for="i in 5"
              :key="i"
              class="fs-3 me-1"
              @click="valoracion = i"
              style="cursor: pointer;"
            >
              <span v-if="i <= valoracion">★</span>
              <span v-else>☆</span>
            </span>
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label fw-semibold">Mensaje</label>
          <textarea
            v-model="mensaje"
            class="form-control"
            rows="4"
            placeholder="Escribe aquí tu comentario..."
          ></textarea>
        </div>

        <div class="text-center">
          <button
            class="btn btn-primary rounded-pill px-5"
            :disabled="loading || !mensaje"
            @click="enviarFeedback"
          >
            {{ loading ? "Enviando..." : "Enviar" }}
          </button>
        </div>

        <div v-if="success" class="alert alert-success mt-3 text-center">
          ¡Gracias! Tu comentario ha sido enviado.
        </div>

        <div v-if="error" class="alert alert-danger mt-3 text-center">
          {{ error }}
        </div>
      </div>
    </div>

    <div v-else>
      <!-- VISTA ADMIN PARA SUPERUSER -->
      <h3 class="fw-bold mb-4 text-center">Feedback de Usuarios</h3>

      <div class="mb-3 d-flex justify-content-between align-items-center">
        <div>
          <label class="form-label fw-semibold me-2">Filtrar por tipo:</label>
          <select v-model="filtroTipo" class="form-select d-inline-block w-auto">
            <option value="">Todos</option>
            <option value="GENERAL">General</option>
            <option value="MEJORA">Mejora</option>
            <option value="BUG">Bug</option>
            <option value="SUGERENCIA">Sugerencia</option>
          </select>
        </div>
        <div>
          <button class="btn btn-success" @click="cargarFeedbacks">Recargar</button>
        </div>
      </div>

      <div v-if="loading" class="text-center my-4">
        Cargando feedbacks...
      </div>

      <div v-else>
        <table class="table table-striped table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>Usuario</th>
              <th>Tipo</th>
              <th>Valoración</th>
              <th>Mensaje</th>
              <th>Fecha</th>
              <th>Revisado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="fb in feedbacksFiltrados" :key="fb.id">
              <td>{{ fb.usuario || "Anónimo" }}</td>
              <td>{{ fb.tipo }}</td>
              <td>
                <span v-if="fb.valoracion">
                  <span v-for="i in 5" :key="i">
                    <span v-if="i <= fb.valoracion">★</span>
                    <span v-else>☆</span>
                  </span>
                </span>
              </td>
              <td>{{ fb.mensaje }}</td>
              <td>{{ new Date(fb.fecha).toLocaleString() }}</td>
              <td>
                <span v-if="fb.revisado" class="badge bg-success">Sí</span>
                <span v-else class="badge bg-secondary">No</span>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="feedbacksFiltrados.length === 0" class="text-center text-muted my-4">
          No hay feedbacks para mostrar
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { nuevoFeedback, getFeedback } from '@/services/feedbackService'

// --- Estado del formulario ---
const tipo = ref('GENERAL')
const valoracion = ref<number | null>(null)
const mensaje = ref('')
const loading = ref(false)
const success = ref(false)
const error = ref('')

// --- Estado admin ---
const feedbacks = ref<any[]>([])
const filtroTipo = ref('')
const isSuperUser = ref(false) // Se detectará desde backend o token

// --- Funciones del formulario ---
const enviarFeedback = async () => {
  if (!mensaje.value) return

  loading.value = true
  success.value = false
  error.value = ''

  try {
    await nuevoFeedback(tipo.value, mensaje.value, valoracion.value)
    success.value = true
    mensaje.value = ''
    valoracion.value = null
    tipo.value = 'GENERAL'
  } catch (e: any) {
    console.error(e)
    error.value = e.response?.data?.detail || 'Error enviando el feedback'
  } finally {
    loading.value = false
  }
}

const cargarFeedbacks = async () => {
  loading.value = true
  try {
    const data = await getFeedback()
    feedbacks.value = data
  } catch (e: any) {
    console.error('Error cargando feedbacks', e)
  } finally {
    loading.value = false
  }
}

const feedbacksFiltrados = computed(() => {
  if (!filtroTipo.value) return feedbacks.value
  return feedbacks.value.filter(fb => fb.tipo === filtroTipo.value)
})

// --- Detectar superuser y cargar feedbacks si aplica ---
onMounted(async () => {
  // Aquí podrías obtener info del usuario desde el backend
  // Por ejemplo, un endpoint /api/v1/me que devuelva { is_superuser: true }
  // Para demo, lo ponemos a true o false
  isSuperUser.value = /* lógica para detectar superuser */ false

  if (isSuperUser.value) {
    await cargarFeedbacks()
  }
})
</script>

<style scoped>
textarea {
  resize: none;
}

table td {
  vertical-align: middle;
}
</style>