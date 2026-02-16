<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-4">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4">

        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold mb-0">
          {{ canal.titulo }}
        </h1>

        <div style="width: 100px"></div>
      </div>

      <div class="row g-4">

        <!-- DETALLES CANAL -->
        <div class="col-lg-8 mx-auto">
          <div class="bg-white rounded-3 shadow-sm p-4">

            <h4 class="mb-4 d-flex align-items-center gap-2">
              <i class="bi bi-chat-dots-fill text-primary"></i>
              {{ t.channelDetail }}
            </h4>

            <!-- TÍTULO -->
            <div class="mb-3">
              <label class="form-label fw-medium">{{ t.title }}</label>

              <div v-if="!editando">
                {{ canal.titulo }}
              </div>

              <input
                v-else
                v-model="canal.titulo"
                class="form-control"
                :class="{ 'is-invalid': errores.titulo }"
              />
            </div>

            <!-- TEMA -->
            <div class="mb-3">
              <label class="form-label fw-medium">{{ t.theme }}</label>

              <div v-if="!editando">
                {{ canal.tema || '-' }}
              </div>

              <input
                v-else
                v-model="canal.tema"
                class="form-control"
              />
            </div>

            <!-- BANDERAS -->
            <div class="row mt-4">

              <div class="col-md-6">
                <div v-if="!editando">
                  <span class="fw-medium">{{ t.secret }}:</span>
                  {{ canal.secreto ? 'Sí' : 'No' }}
                </div>

                <div v-else class="form-check">
                  <input
                    type="checkbox"
                    class="form-check-input"
                    v-model="canal.secreto"
                    id="secreto"
                  />
                  <label class="form-check-label" for="secreto">
                    {{ t.secret }}
                  </label>
                </div>
              </div>

              <div class="col-md-6">
                <div v-if="!editando">
                  <span class="fw-medium">{{ t.hidden }}:</span>
                  {{ canal.oculto ? 'Sí' : 'No' }}
                </div>

                <div v-else class="form-check">
                  <input
                    type="checkbox"
                    class="form-check-input"
                    v-model="canal.oculto"
                    id="oculto"
                  />
                  <label class="form-check-label" for="oculto">
                    {{ t.hidden }}
                  </label>
                </div>
              </div>

            </div>

          </div>
        </div>
      </div>

      <!-- ACCIONES -->
      <div class="d-flex justify-content-center gap-4 mt-5">

        <button
          v-if="!editando"
          class="btn btn-primary btn-lg rounded-pill"
          @click="activarEdicion"
        >
          <i class="bi bi-pencil me-2"></i>
          {{ t.modifyChannel }}
        </button>

        <template v-else>
          <button
            class="btn btn-success btn-lg rounded-pill"
            @click="guardarCambios"
          >
            <i class="bi bi-check-lg me-2"></i>
            {{ t.saveChanges }}
          </button>

          <button
            class="btn btn-secondary btn-lg rounded-pill"
            @click="cancelarEdicion"
          >
            {{ t.cancel }}
          </button>
        </template>
      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, inject, type Ref } from "vue";
import { useRouter } from "vue-router";

import { getCanalAdministrador, editarCanal, eliminarCanal } from "@/services/foroService"

import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ idForo: string, idCanal: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();

const editando = ref(false)

const canal = ref({
  id: 0,
  titulo: "",
  tema: "",
  secreto: false,
  oculto: false
})

const errores = ref({
  titulo: false,
  tema: false
})

const canalOriginal = ref<any>(null);

function validarFormulario() {
  errores.value.titulo = canal.value.titulo.trim() === ""
  errores.value.tema = canal.value.tema.trim() === ""

  return !errores.value.titulo && !errores.value.tema
}

function activarEdicion() {
  canalOriginal.value = JSON.parse(JSON.stringify(canal.value))

  errores.value.titulo = false
  errores.value.tema = false

  editando.value = true
}

function cancelarEdicion() {
  canal.value = JSON.parse(JSON.stringify(canalOriginal.value))

  editando.value = false
}

function camposModificados() {
  const data: any = {}

  if (canalOriginal.value.titulo !== canal.value.titulo) {
    data["titulo"] = canal.value.titulo
  }

  if (canalOriginal.value.tema !== canal.value.tema) {
    data["tema"] = canal.value.tema
  }

  if (canalOriginal.value.secreto !== canal.value.secreto) {
    data["secreto"] = canal.value.secreto
  }

  if (canalOriginal.value.oculto !== canal.value.oculto) {
    data["oculto"] = canal.value.oculto
  }

  return data
}

const guardarCambios = async () => {
  try {
    if (!validarFormulario()) return

    const data = camposModificados()

    if (Object.keys(data).length > 0) {
      await editarCanal(canal.value.id, data)
    }

    editando.value = false
  } catch (e) {
    console.error("Error al modificar el canal", e);
  }
}

const volver = () => router.back();

onMounted(async () => {
  try {
    canal.value = await getCanalAdministrador(Number(props.idCanal))
    canalOriginal.value = JSON.parse(JSON.stringify(canal.value))
  } catch(e) {
    console.log("Error al obtener la informacion del canal", e);
  }
});
</script>
