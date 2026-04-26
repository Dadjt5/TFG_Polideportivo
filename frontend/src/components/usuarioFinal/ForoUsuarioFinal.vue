<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <div class="container py-5">

      <!-- Título -->
      <h1 class="text-center fw-semibold mb-3 text-primary">{{ t.forumTitle }}</h1>
      <p class="text-center text-secondary fs-5 mb-5">{{ t.forumSubtitle }}</p>

      <!-- LISTA DE CANALES -->
      <div v-if="!canalSeleccionado" class="row g-4">
        <div v-for="canal in canales" :key="canal.id" class="col-sm-6 col-lg-4">
          <div class="card h-100 shadow-sm border-0 rounded-4 text-center cursor-pointer"
            style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(8px);"
            @click="canalSeleccionado = canal; abrirCanal(canal.id)">
            <div class="card-body py-5">
              <i class="bi bi-chat-dots fs-1 text-primary mb-3"></i>
              <h5 class="fw-medium">{{ canal.titulo }}</h5>
            </div>
          </div>
        </div>
      </div>

      <!-- CANAL SELECCIONADO -->
      <div v-else class="card shadow-lg border-0 rounded-4 p-4"
        style="background-color: rgba(255,255,255,0.9); backdrop-filter: blur(10px);">
        <button class="btn btn-secondary mb-4 align-self-start" @click="canalSeleccionado = undefined">
          ← {{ t.return }}
        </button>

        <h2 class="fw-semibold mb-4 text-primary">{{ canalSeleccionado.titulo }}</h2>
        <p class="text-center text-secondary fs-5 mb-5">{{ canalSeleccionado.tema }}</p>

        <div ref="chatBox" class="border rounded-4 p-3 mb-4 overflow-auto chat-box"
          style="max-height: 320px; background-color: rgba(255,255,255,0.6);">
          <template v-if="!canalSeleccionado.secreto">

            <div v-for="[dia, mensajesDia] in mensajesAgrupados" :key="dia">

              <!-- Día -->
              <div class="text-center my-3">
                <span class="badge bg-light text-secondary px-3 py-2 rounded-pill">
                  {{ formatearDia(mensajesDia[0].fechaEnvio) }}
                </span>
              </div>

              <!-- Mensajes -->
              <div v-for="m in mensajesDia" :key="m.id" class="d-flex mb-3" :class="{
                'justify-content-end': m.usuario === authStore.user?.id,
                'justify-content-start': m.usuario !== authStore.user?.id
              }">
                <div class="message-bubble p-3 rounded-4 shadow-sm" :class="{
                  'bg-primary text-white': m.es_admin,
                  'bg-white border text-dark': !m.es_admin,
                  'message-own': m.usuario === authStore.user?.id,
                  'message-other': m.usuario !== authStore.user?.id
                }">
                  <div class="d-flex justify-content-between align-items-center mb-1">
                    <small class="fw-semibold">{{ m.nombre }}</small>
                    <small class="ms-3" :class="m.es_admin ? 'text-white-50' : 'text-muted'">
                      {{ formatearHora(m.fechaEnvio) }}
                    </small>
                  </div>

                  <p class="mb-0">{{ m.texto }}</p>
                </div>
              </div>

            </div>

          </template>

          <p v-else class="text-center text-muted fst-italic">
            {{ t.hiddenMessages }}
          </p>
        </div>

        <div class="d-flex gap-3">
          <input type="text" class="form-control form-control-lg rounded-3" v-model="textoMensaje"
            :disabled="canalSeleccionado.silenciado"
            :placeholder="canalSeleccionado.silenciado === false ? t.writeMessage : t.cantWriteMessage">
          <span v-if="!canalSeleccionado.silenciado">
            <button class="btn btn-primary px-4 rounded-3" @keyup.enter="enviar(canalSeleccionado.id)"
              @click="enviar(canalSeleccionado.id)">
              {{ t.send }}
            </button>
          </span>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, inject, type Ref, ref, computed, nextTick, watch } from 'vue'

import { getForo, getMensajes, enviarMensaje } from "@/services/foroService"
import { useAuthStore } from '@/stores/auth';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

type Canal = {
  id: number,
  titulo: string,
  numeroParticipantes: number,
  tema: string,
  secreto: boolean,
  silenciado: boolean
}

type Mensaje = {
  id: number,
  texto: string,
  fechaEnvio: string,
  nombre: string,
  es_admin: boolean,
  usuario: number
}

const canales = ref<Canal[]>([]);
const mensajes = ref<Mensaje[]>([]);
const chatBox = ref<HTMLElement | null>(null)
const authStore = useAuthStore()

const canalSeleccionado = ref<Canal>();

const textoMensaje = ref("")

function scrollToBottom() {
  nextTick(() => {
    if (chatBox.value) {
      chatBox.value.scrollTop = chatBox.value.scrollHeight
    }
  })
}

const formatearHora = (fecha: string) => {
  return new Date(fecha).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit"
  })
}

const formatearDia = (fecha: string) => {
  return new Date(fecha).toLocaleDateString([], {
    day: "numeric",
    month: "long",
    year: "numeric"
  })
}

const mensajesAgrupados = computed(() => {
  const grupos: Record<string, Mensaje[]> = {}

  mensajes.value.forEach(msg => {
    const dia = new Date(msg.fechaEnvio).toDateString()

    if (!grupos[dia]) {
      grupos[dia] = []
    }

    grupos[dia].push(msg)
  })

  return Object.entries(grupos)
})

const abrirCanal = async (id: number) => {
  try {
    mensajes.value = await getMensajes(id)
  } catch (e) {
    console.log("Error al obtener los mensajes del canal", e)
  }
}

const enviar = async (id: number) => {
  if (!textoMensaje.value.trim()) return

  try {
    const data = {
      "texto": textoMensaje.value
    }
    await enviarMensaje(id, data)
    textoMensaje.value = ""
    mensajes.value = await getMensajes(id)
  } catch (e) {
    console.log("Error al enviar el mensaje", e)
  }
}

watch(mensajesAgrupados, () => {
  scrollToBottom()
}, { deep: true })

onMounted(async () => {
  try {
    canales.value = await getForo()
    scrollToBottom()
  } catch (e) {
    console.log("Error al obtener los canales del foro", e)
  }
})
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}

.chat-box {
  max-height: 420px;
  background-color: rgba(255, 255, 255, 0.55);
  backdrop-filter: blur(8px);
}

.message-bubble {
  max-width: 75%;
  transition: all 0.2s ease;
}

.message-own {
  background: #dbeafe;
  color: #1e3a8a;
}

.message-other {
  background: white;
  color: #374151;
}

.message-bubble:hover {
  transform: translateY(-1px);
}
</style>
