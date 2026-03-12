<template>
  <div class="min-vh-100 pt-4" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4" style="max-width: 1600px;">

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
          <div class="card shadow-lg rounded-4 p-4"
            style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(10px);">

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

      <!-- MENSAJE -->
      <p v-if="mensaje" class="text-center text-danger mt-4">
        {{ mensaje }}
      </p>

      <!-- ACCIONES -->
      <div class="d-flex justify-content-center gap-3 mt-5">
        <button v-if="!editando" class="btn btn-primary btn-lg rounded-pill" @click="activarEdicion">
          <i class="bi bi-pencil me-2"></i> {{ t.modifyChannel }}
        </button>

        <template v-else>
          <button class="btn btn-success btn-lg rounded-pill" @click="guardarCambios">
            <i class="bi bi-check-lg me-2"></i> {{ t.saveChanges }}
          </button>
          <button class="btn btn-secondary btn-lg rounded-pill" @click="cancelarEdicion">
            {{ t.cancel }}
          </button>
        </template>

        <button v-if="!editando" class="btn btn-danger btn-lg rounded-pill" @click="abrirConfirmacion">
          <i class="bi bi-trash me-2"></i> {{ t.deleteChannel }}
        </button>
      </div>
    </main>

    <div class="modal fade" id="confirmDeleteModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4">

          <div class="modal-header">
            <h5 class="modal-title">{{ t.confirmDelete }}</h5>
          </div>

          <div class="modal-body text-center">
            <p>{{ t.confirmDeleteChannel }}</p>
          </div>

          <div class="modal-footer justify-content-center">
            <button class="btn btn-secondary rounded-pill" data-bs-dismiss="modal">
              {{ t.cancel }}
            </button>

            <button class="btn btn-danger rounded-pill" @click="confirmarEliminar">
              {{ t.deleteUser }}
            </button>
          </div>

        </div>
      </div>
    </div>

    <div class="modal fade" id="successDeleteModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4 text-center">

          <div class="modal-body py-5">

            <i class="bi bi-check-circle-fill text-success fs-1 mb-3"></i>

            <h4 class="fw-semibold">
              {{ mensaje }}
            </h4>

            <button class="btn btn-primary rounded-pill mt-4" @click="finalizar" data-bs-dismiss="modal">
              {{ t.continue }}
            </button>

          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, inject, type Ref } from "vue";
import { useRouter } from "vue-router";
import { Modal } from 'bootstrap'

import { getCanalAdministrador, editarCanal, eliminarCanal } from "@/services/foroService"

import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ idForo: string, idCanal: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();
const mensaje = ref("");

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
  mensaje.value = ""
  canalOriginal.value = JSON.parse(JSON.stringify(canal.value))

  errores.value.titulo = false
  errores.value.tema = false

  editando.value = true
}

function cancelarEdicion() {
  mensaje.value = ""
  canal.value = JSON.parse(JSON.stringify(canalOriginal.value))

  editando.value = false
}

let confirmModal: Modal
let successModal: Modal

const eliminado = ref(false)

function abrirConfirmacion() {
  confirmModal.show()
}

async function confirmarEliminar() {
  try {
    await eliminarCanal(canal.value.id)

    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.channelDeleted
    eliminado.value = true
  } catch (e) {
    mensaje.value = t.value.noDeleted
    eliminado.value = false
    console.error("Error al eliminar el canal", e);
  }
}

const finalizar = async () => {
  if (eliminado.value) {
    router.push({ name: 'foro' });
  } else {
    successModal.hide()
    eliminado.value = false
  }
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
  mensaje.value = ""
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
  confirmModal = new Modal(document.getElementById('confirmDeleteModal')!)
  successModal = new Modal(document.getElementById('successDeleteModal')!)

  try {
    canal.value = await getCanalAdministrador(Number(props.idCanal))
    canalOriginal.value = JSON.parse(JSON.stringify(canal.value))
  } catch(e) {
    mensaje.value = t.value.unexpectedError
    console.error("Error al obtener la informacion del canal", e);
  }
});
</script>
