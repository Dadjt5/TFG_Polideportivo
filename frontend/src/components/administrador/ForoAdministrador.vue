<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">

    <!-- CABECERA -->
    <div class="container py-5">
      <h1 class="text-center fw-bold text-primary mb-3">
        <i class="bi bi-chat-left-dots-fill me-2"></i>
        {{ t.forumTitle }}
      </h1>
      <p class="text-center text-dark fs-5 mb-5">{{ t.forumSubtitle }}</p>

      <!-- LISTADO DE CANALES / CREAR CANAL -->
      <div v-if="!canalSeleccionado">
        <div class="row g-4">
          <div v-for="canal in foro.canales" :key="canal.id" class="col-sm-6 col-lg-4">
            <div class="card h-100 shadow-lg border-0 rounded-4 text-center cursor-pointer"
              style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);"
              @click="seleccionarCanal(canal.id)">
              <div class="card-body py-5">
                <i class="bi bi-chat-dots fs-1 text-primary mb-3"></i>
                <h5 class="fw-semibold">{{ canal.titulo }}</h5>
              </div>
            </div>
          </div>
        </div>

        <div class="d-flex justify-content-center gap-3 mt-5">
          <button class="btn btn-primary btn-lg rounded-pill px-4 shadow-sm" @click="crearCanal(foro.id)">
            <i class="bi bi-plus-circle me-2"></i>
            {{ t.newChannel }}
          </button>
        </div>

      </div>

      <!-- CANAL SELECCIONADO -->
      <div v-else class="row g-4">

        <div class="col-12">

          <!-- FILA SUPERIOR -->
          <div class="d-flex justify-content-between align-items-center mb-3">

            <button class="btn btn-secondary rounded-pill px-3" @click="canalSeleccionado = null">
              ← {{ t.return }}
            </button>

            <div class="d-flex gap-2">
              <button class="btn btn-outline-primary rounded-pill px-3"
                @click="modificarCanal(foro.id, canalSeleccionado.id)">
                <i class="bi bi-pencil me-1"></i>
                {{ t.modifyChannel }}
              </button>
            </div>

          </div>

          <!-- TÍTULO -->
          <h2 class="fw-bold text-primary mb-4">
            {{ canalSeleccionado.titulo }}
          </h2>

        </div>

        <!-- MENSAJES -->
        <div class="col-lg-8">
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
            <input type="text" class="form-control form-control-lg rounded-3 shadow-sm" v-model="textoMensaje"
              :placeholder="t.writeMessage" @keyup.enter="enviarMensajeCanal" />
            <button class="btn btn-primary btn-lg rounded-3 px-4 shadow-sm" @click="enviarMensajeCanal">
              <i class="bi bi-send-fill"></i>
            </button>
          </div>
        </div>

        <!-- USUARIOS DEL CANAL -->
        <div class="col-lg-4">
          <div class="card shadow-lg border-0 rounded-4 p-3"
            style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">
            <h5 class="fw-bold text-primary mb-3">
              <i class="bi bi-people-fill me-2"></i>
              {{ t.channelUsers }}
            </h5>
            <div v-for="user in canalSeleccionado.usuarios || []" :key="user.usuarioFinal"
              class="d-flex justify-content-between align-items-center mb-2 p-2 bg-light rounded-3">
              <span class="fw-medium">{{ user.nombre }}</span>
              <div class="d-flex gap-2">
                <button class="btn btn-warning btn-sm rounded-pill px-3"
                  @click="alterarSilencioUsuario(user.usuarioFinal)">
                  {{ user.silenciado ? t.unmute : t.mute }}
                </button>

                <button class="btn btn-danger btn-sm rounded-pill px-3"
                  @click="alterarExpulsionUsuario(user.usuarioFinal)">
                  {{ user.expulsado ? t.unkick : t.kick }}
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, inject, type Ref, onMounted, computed, nextTick, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

import {
  getForo, getMensajes, modificarUsuarioFinal,
  enviarMensaje, getCanalAdministrador, eliminarCanal
} from '@/services/foroService';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>('language')!;
const t = useI18n(language);

interface Mensaje {
  id: number
  texto: string
  fechaEnvio: string
  nombre: string
  es_admin: boolean
  usuario: number
}

const foro = ref({
  id: 0,
  numeroParticipantes: 0,
  canales: [] as {
    id: 0,
    titulo: "",
  }[]
});

const router = useRouter();

const canalSeleccionado = ref();
const mensajes = ref<Mensaje[]>([]);
const textoMensaje = ref('');
const chatBox = ref<HTMLElement | null>(null)
const authStore = useAuthStore()

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

const seleccionarCanal = async (id: number) => {
  try {
    canalSeleccionado.value = await getCanalAdministrador(id)
    mensajes.value = await getMensajes(id)
  } catch (e) {
    console.log("Error al obtener los mensajes del canal", e)
  }
}

const borrarCanal = async () => {
  try {
    await eliminarCanal(canalSeleccionado.value.id)

    foro.value.canales = foro.value.canales.filter(
      canal => canal.id !== canalSeleccionado.value.id
    )
    canalSeleccionado.value = null
  } catch (e) {
    console.log("Error al eliminar el canal", e)
  }
}

const enviarMensajeCanal = async () => {
  if (!textoMensaje.value.trim() || !canalSeleccionado.value) return;

  await enviarMensaje(canalSeleccionado.value.id, { texto: textoMensaje.value });

  textoMensaje.value = '';
  mensajes.value = await getMensajes(canalSeleccionado.value.id)
};

const crearCanal = (id: number) => {
  router.push({
    name: "crear-canal",
    params: { id }
  })
}

const modificarCanal = (idForo: number, idCanal: number) => {
  router.push({
    name: "editar-canal",
    params: { idForo, idCanal }
  })
}

const alterarSilencioUsuario = async (usuarioId: number) => {
  if (!canalSeleccionado.value) return;

  await modificarUsuarioFinal(canalSeleccionado.value.id, usuarioId, "silenciar");

  const usuario = canalSeleccionado.value.usuarios.find(
    u => u.usuarioFinal === usuarioId
  );

  if (usuario) {
    usuario.silenciado = !usuario.silenciado;
  }
};

const alterarExpulsionUsuario = async (usuarioId: number) => {
  if (!canalSeleccionado.value) return;

  await modificarUsuarioFinal(canalSeleccionado.value.id, usuarioId, "expulsar");

  const usuario = canalSeleccionado.value.usuarios.find(
    u => u.usuarioFinal === usuarioId
  );

  if (usuario) {
    usuario.expulsado = !usuario.expulsado;
  }
};

watch(mensajesAgrupados, () => {
  scrollToBottom()
}, { deep: true })


onMounted(async () => {
  foro.value = await getForo();
  scrollToBottom()
});
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
</style>
