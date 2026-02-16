<template>
  <div class="min-vh-100 bg-light">

    <!-- CABECERA -->
    <div class="container py-5">
      <h1 class="text-center fw-semibold mb-3">{{ t.forumTitle }}</h1>
      <p class="text-center text-secondary fs-5 mb-5">{{ t.forumSubtitle }}</p>

      <!-- LISTADO DE CANALES / CREAR CANAL -->
      <div v-if="!canalSeleccionado">
        <div class="row g-4">
          <div v-for="canal in foro.canales" :key="canal.id" class="col-sm-6 col-lg-4">
            <div class="card h-100 shadow-sm border-0 rounded-4 text-center cursor-pointer"
              @click="seleccionarCanal(canal.id)">
              <div class="card-body py-5">
                <i class="bi bi-chat-dots fs-1 text-primary mb-3"></i>
                <h5 class="fw-medium">{{ canal.titulo }}</h5>
              </div>
            </div>
          </div>
        </div>

        <div class="d-flex justify-content-center gap-3 mt-5">
          <button class="btn btn-primary btn-lg" @click="crearCanal(foro.id)">
            {{ t.newChannel }}
          </button>
        </div>

      </div>

      <!-- CANAL SELECCIONADO -->
      <div v-else class="row g-4">

        <div class="col-12">

          <!-- FILA SUPERIOR -->
          <div class="d-flex justify-content-between align-items-center mb-3">

            <button class="btn btn-secondary" @click="canalSeleccionado = null">
              ← {{ t.return }}
            </button>

            <div class="d-flex gap-2">
              <button class="btn btn-outline-primary" @click="modificarCanal(foro.id, canalSeleccionado.id)">
                {{ t.modifyChannel }}
              </button>

              <button class="btn btn-outline-danger" @click="borrarCanal">
                {{ t.delete }}
              </button>
            </div>

          </div>

          <!-- TÍTULO -->
          <h2 class="fw-semibold mb-4">
            {{ canalSeleccionado.titulo }}
          </h2>

        </div>

        <!-- MENSAJES -->
        <div class="col-lg-8">
          <div class="border rounded-4 p-3 mb-3 overflow-auto" style="max-height: 400px;">
            <div v-for="(msg, idx) in mensajes" :key="idx"
            class="border rounded-3 p-3 mb-2"
            :class="msg.es_admin ? 'bg-primary text-white' : 'bg-white text-secondary'">
              <p class="fw-medium mb-1">{{ msg.nombre }}</p>
              <p class="mb-0">{{ msg.texto }}</p>
            </div>
          </div>

          <div class="d-flex gap-3">
            <input type="text" class="form-control form-control-lg rounded-3" v-model="textoMensaje"
              :placeholder="t.writeMessage" @keyup.enter="enviarMensajeCanal" />
            <button class="btn btn-primary btn-lg" @click="enviarMensajeCanal">
              {{ t.send }}
            </button>
          </div>
        </div>

        <!-- USUARIOS DEL CANAL -->
        <div class="col-lg-4">
          <div class="card shadow-sm border-0 rounded-4 p-3">
            <h5 class="fw-semibold mb-3">{{ t.channelUsers }}</h5>
            <div v-for="user in canalSeleccionado.usuarios || []" :key="user.usuarioFinal"
              class="d-flex justify-content-between align-items-center mb-2 p-2 bg-light rounded-3">
              <span>{{ user.nombre }}</span>
              <div class="d-flex gap-2">
                <button class="btn btn-warning btn-sm" @click="alterarSilencioUsuario(user.usuarioFinal)">
                  {{ user.silenciado ? t.unmute : t.mute }}
                </button>

                <button class="btn btn-danger btn-sm" @click="alterarExpulsionUsuario(user.usuarioFinal)">
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
import { ref, inject, type Ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

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
}

const Canal = ref({
  id: 0,
  titulo: "",
  numeroParticipantes: 0,
  tema: "",
  secreto: false,
  oculto: false,
  usuarios: [] as {
    usuarioFinal: 0,
    nombre: "",
    silenciado: false,
    expulsado: false,
    fechaEntrada: ""
  }[]
});

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

onMounted(async () => {
  foro.value = await getForo();
});
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
</style>
