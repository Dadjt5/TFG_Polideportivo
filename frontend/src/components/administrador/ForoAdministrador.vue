<template>
  <div class="min-vh-100 bg-light">

    <!-- CABECERA -->
    <div class="container py-5">
      <h1 class="text-center fw-semibold mb-3">{{ t.forumTitle }}</h1>
      <p class="text-center text-secondary fs-5 mb-5">{{ t.forumSubtitle }}</p>

      <!-- LISTADO DE CANALES / CREAR CANAL -->
      <div v-if="!canalSeleccionado">
        <div class="d-flex gap-3 mb-4">
          <input
            type="text"
            class="form-control form-control-lg rounded-3"
            v-model="nuevoNombreCanal"
            :placeholder="t.channelName"
          />
          <button class="btn btn-primary btn-lg" @click="crearCanal">
            {{ t.newChannel }}
          </button>
        </div>

        <div class="row g-4">
          <div
            v-for="canal in canales"
            :key="canal.id"
            class="col-sm-6 col-lg-4"
          >
            <div
              class="card h-100 shadow-sm border-0 rounded-4 text-center cursor-pointer"
              @click="seleccionarCanal(canal)"
            >
              <div class="card-body py-5">
                <i class="bi bi-chat-dots fs-1 text-primary mb-3"></i>
                <h5 class="fw-medium">{{ canal.nombre }}</h5>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CANAL SELECCIONADO -->
      <div v-else class="row g-4">

        <div class="col-12">
          <button class="btn btn-secondary mb-4" @click="canalSeleccionado = null">
            ← {{ t.back }}
          </button>

          <h2 class="fw-semibold mb-4">{{ canalSeleccionado.nombre }}</h2>
        </div>

        <!-- MENSAJES -->
        <div class="col-lg-8">
          <div class="border rounded-4 p-3 mb-3 overflow-auto" style="max-height: 400px;">
            <div v-for="(msg, idx) in mensajes" :key="idx" class="bg-white border rounded-3 p-3 mb-2">
              <p class="fw-medium mb-1">{{ msg.usuario }}</p>
              <p class="mb-0 text-secondary">{{ msg.texto }}</p>
            </div>
          </div>

          <div class="d-flex gap-3">
            <input
              type="text"
              class="form-control form-control-lg rounded-3"
              v-model="textoMensaje"
              :placeholder="t.writeMessage"
            />
            <button class="btn btn-primary btn-lg" @click="enviarMensajeCanal">
              {{ t.send }}
            </button>
          </div>
        </div>

        <!-- USUARIOS DEL CANAL -->
        <div class="col-lg-4">
          <div class="card shadow-sm border-0 rounded-4 p-3">
            <h5 class="fw-semibold mb-3">{{ t.channelUsers }}</h5>
            <div v-for="user in canalUsuarios[canalSeleccionado.id] || []" :key="user.id" class="d-flex justify-content-between align-items-center mb-2 p-2 bg-light rounded-3">
              <span>{{ user.nombre }}</span>
              <div class="d-flex gap-2">
                <button class="btn btn-warning btn-sm" @click="alterarSilencioUsuario(user.id)">{{ t.mute }}</button>
                <button class="btn btn-danger btn-sm" @click="expulsarUsuario(user.id)">{{ t.kick }}</button>
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

import { getForo, getMensajes, nuevoCanal, modificarUsuarioFinal, enviarMensaje } from '@/services/foroService';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>('language')!;
const t = useI18n(language);

type Canal = { id: number, nombre: string };
type Mensaje = { usuario: string, texto: string };
type Usuario = { id: number, nombre: string };

const canales = ref<Canal[]>([]);
const canalSeleccionado = ref<Canal | null>(null);
const mensajes = ref<Mensaje[]>([]);
const textoMensaje = ref('');
const nuevoNombreCanal = ref('');
const canalUsuarios = ref<Record<string, Usuario[]>>({});

const seleccionarCanal = async (canal: Canal) => {
  canalSeleccionado.value = canal;
  mensajes.value = await getMensajes(canal.id);
  canalUsuarios.value[canal.id] = canalUsuarios.value[canal.id] || [];
};

const enviarMensajeCanal = async () => {
  if (!textoMensaje.value.trim() || !canalSeleccionado.value) return;
  await enviarMensaje(canalSeleccionado.value.id, { texto: textoMensaje.value });
  textoMensaje.value = '';
  mensajes.value = await getMensajes(canalSeleccionado.value.id);
};

const crearCanal = async () => {
  if (!nuevoNombreCanal.value.trim()) return;
  const canal = await nuevoCanal({ nombre: nuevoNombreCanal.value });
  canales.value.push(canal);
  nuevoNombreCanal.value = '';
};

const alterarSilencioUsuario = async (usuarioId: number) => {
  if (!canalSeleccionado.value) return;
  await modificarUsuarioFinal(canalSeleccionado.value.id, usuarioId, "silenciar");
};

const expulsarUsuario = async (usuarioId: number) => {
  if (!canalSeleccionado.value) return;
  await modificarUsuarioFinal(canalSeleccionado.value.id, usuarioId, "expulsar");
  canalUsuarios.value[canalSeleccionado.value.id] = canalUsuarios.value[canalSeleccionado.value.id].filter(u => u.id !== usuarioId);
};

onMounted(async () => {
  canales.value = await getForo();
});
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
</style>
