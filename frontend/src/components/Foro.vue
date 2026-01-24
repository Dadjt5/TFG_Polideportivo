<template>
  <div class="min-vh-100 bg-light">

    <!-- CONTENIDO -->
    <div class="container py-5">
      <h1 class="text-center fw-semibold mb-3">{{ t.forumTitle }}</h1>
      <p class="text-center text-secondary fs-5 mb-5">{{ t.forumSubtitle }}</p>

      <!-- LISTA DE CANALES -->
      <div v-if="!canalSeleccionado" class="row g-4">
        <div
          v-for="canal in canales"
          :key="canal.id"
          class="col-sm-6 col-lg-4"
        >
          <div
            class="card h-100 shadow-sm border-0 rounded-4 text-center cursor-pointer"
            @click="canalSeleccionado=canal, abrirCanal(canal.id)"
          >
            <div class="card-body py-5">
              <i class="bi bi-chat-dots fs-1 text-primary mb-3"></i>
              <h5 class="fw-medium">{{ canal.titulo }}</h5>
            </div>
          </div>
        </div>
      </div>

      <!-- CANAL SELECCIONADO -->
      <div v-else class="card shadow-lg border-0 rounded-4 p-4">
        <button
          class="btn btn-secondary mb-4 align-self-start"
          @click="canalSeleccionado=undefined"
        >
          ← {{ t.back }}
        </button>

        <h2 class="fw-semibold mb-4">{{ canalSeleccionado.titulo }}</h2>
        <p class="text-center text-secondary fs-5 mb-5">{{ canalSeleccionado.tema }}</p>

        <div
          class="border rounded-4 p-3 mb-4 overflow-auto"
          style="max-height: 320px"
        >
          <div v-if="!canalSeleccionado.secreto">
            <div
              v-for="m in mensajes"
              :key="m.id"
              class="bg-white border rounded-3 p-3 mb-2"
            >
              <p class="fw-medium mb-1">{{ m.nombreUsuario }}</p>
              <p class="mb-0 text-secondary">{{ m.texto }}</p>
            </div>
          </div>

          <p
            v-else
            class="text-center text-muted fst-italic"
          >
            {{ t.hiddenMessages }}
          </p>
        </div>

        <div class="d-flex gap-3">
          <input
            type="text"
            class="form-control form-control-lg rounded-3"
            v-model="textoMensaje"
            :disabled="canalSeleccionado.silenciado"
            :placeholder="canalSeleccionado.silenciado === false ? t.writeMessage : t.cantWriteMessage"
          />
          <span v-if="!canalSeleccionado.silenciado">
            <button class="btn btn-primary px-4 rounded-3" @click="enviar(canalSeleccionado.id)">
              {{ t.send }}
            </button>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, inject, type Ref, ref } from 'vue'

import { getForo, getMensajes, enviarMensaje } from "../services/foroService"
import { useUserStore } from "../stores/usuarioFinal";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

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
  nombreUsuario: string
}

const usuarioFinalStore = useUserStore();

const canales = ref<Canal[]>([]);
const mensajes = ref<Mensaje[]>([]);

const canalSeleccionado = ref<Canal>();

const textoMensaje = ref("")

const abrirCanal = async (id: number) => {
  try {
    mensajes.value = await getMensajes(id)
  } catch(e) {
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
  } catch(e) {
    console.log("Error al enviar el mensaje", e)
  }
}

onMounted(async () => {
  try {
    canales.value = await getForo()
  } catch(e) {
    console.log("Error al obtener los canales del foro", e)
  }
})
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
</style>
