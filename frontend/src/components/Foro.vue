<template>
  <div class="min-vh-100 bg-light">

    <!-- CONTENIDO -->
    <div class="container py-5">
      <h1 class="text-center fw-semibold mb-3">{{ t.forumTitle }}</h1>
      <p class="text-center text-secondary fs-5 mb-5">{{ t.forumSubtitle }}</p>

      <!-- LISTA DE CANALES -->
      <div v-if="!selectedChannel" class="row g-4">
        <div
          v-for="channel in channels"
          :key="channel.id"
          class="col-sm-6 col-lg-4"
        >
          <div
            class="card h-100 shadow-sm border-0 rounded-4 text-center cursor-pointer"
            @click="selectedChannel = channel"
          >
            <div class="card-body py-5">
              <i class="bi bi-chat-dots fs-1 text-primary mb-3"></i>
              <h5 class="fw-medium">{{ channel.name }}</h5>
            </div>
          </div>
        </div>
      </div>

      <!-- CANAL SELECCIONADO -->
      <div v-else class="card shadow-lg border-0 rounded-4 p-4">
        <button
          class="btn btn-secondary mb-4 align-self-start"
          @click="selectedChannel = null"
        >
          ← {{ t.back }}
        </button>

        <h2 class="fw-semibold mb-4">{{ selectedChannel.name }}</h2>

        <div
          class="border rounded-4 p-3 mb-4 overflow-auto"
          style="max-height: 320px"
        >
          <div v-if="!selectedChannel.hideMessages">
            <div
              v-for="(msg, index) in allMessages[selectedChannel.id]"
              :key="index"
              class="bg-white border rounded-3 p-3 mb-2"
            >
              <p class="fw-medium mb-1">{{ msg.user }}</p>
              <p class="mb-0 text-secondary">{{ msg.text }}</p>
            </div>
          </div>

          <p
            v-else
            class="text-center text-muted fst-italic"
          >
            {{ language === 'es'
              ? 'Los mensajes están ocultos en este buzón.'
              : 'Messages are hidden in this box.' }}
          </p>
        </div>

        <div class="d-flex gap-3">
          <input
            type="text"
            class="form-control form-control-lg rounded-3"
            :placeholder="language === 'es'
              ? 'Escribe tu mensaje...'
              : 'Write your message...'"
          />
          <button class="btn btn-primary px-4 rounded-3">
            {{ language === 'es' ? 'Enviar' : 'Send' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, inject, type Ref, ref, computed } from 'vue'

import { getForo } from "../services/foroService"

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const selectedChannel = ref<any>(null)

const channels = computed(() => [
  { id: 'sala-musculacion', name: language.value === 'es' ? 'Sala de musculación' : 'Gym room' },
  { id: 'piscina', name: language.value === 'es' ? 'Piscina' : 'Swimming pool' },
  { id: 'tenis', name: language.value === 'es' ? 'Tenis' : 'Tennis' },
  { id: 'sugerencias', name: t.value.suggestionBox, hideMessages: true },
  { id: 'actividades', name: t.value.newActivitiesBox },
])

const allMessages: Record<string, { user: string; text: string }[]> = {
  sugerencias: [
    { user: 'Usuario123', text: 'Sería genial añadir más máquinas en la sala de musculación.' },
    { user: 'Ana Gómez', text: 'Propongo ampliar el horario de la piscina los fines de semana.' },
  ],
  tenis: [
    { user: 'Jorge', text: '¿Alguien quiere jugar dobles el sábado?' },
    { user: 'Lucía', text: 'Estoy disponible por la mañana.' },
    { user: 'Carlos', text: 'Perfecto, nos vemos en la pista 2.' },
  ],
}

type Foro = {
  id: number
  canales: {
    id: number,
    titulo: string,
    numeroParticipantes: number,
    tema: string,
    secreto: boolean
  }
}

const foro = ref<Foro[]>([])


onMounted(async () => {
  try {
    foro.value = await getForo()
  } catch(e) {
    console.log("Error al obtener las reservas realizadas", e)
  }
})
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
</style>
