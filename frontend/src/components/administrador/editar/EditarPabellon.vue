<template>
  <div class="min-vh-100 pt-4" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4" style="max-width: 1600px;">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4 mt-3">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold text-primary mb-2" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
          {{ pabellon.nombre}}
        </h1>

        <div style="width: 100px"></div>
      </div>

      <div class="row g-4">

        <!-- INFORMACIÓN -->
        <div class="col-lg-6">
          <div class="card shadow-lg rounded-4 p-4"
            style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(10px);">

            <h4 class="mb-4 d-flex align-items-center">
              <i class="bi bi-info-circle-fill text-primary me-2"></i>
              {{ t.pavilionDetail }}
            </h4>

            <div class="row g-3">

              <!-- NOMBRE -->
              <div class="col-12">
                <label class="form-label fw-semibold">{{ t.name }}</label>
                <input v-model="pabellon.nombre"
                  :class="['form-control', 'form-control-lg', { 'is-invalid': errores.nombre }]"
                  :readonly="!editando" />
              </div>

              <!-- DESCRIPCION -->
              <div class="col-12">
                <label class="form-label fw-semibold">{{ t.description }}</label>
                <textarea v-model="pabellon.descripcion" class="form-control form-control-lg" rows="3"
                  :readonly="!editando"></textarea>
              </div>

              <!-- DIRECCION -->
              <div class="col-12">
                <label class="form-label fw-semibold">{{ t.address }}</label>
                <input v-model="pabellon.direccion" class="form-control form-control-lg" :readonly="!editando" />
              </div>

            </div>
          </div>
        </div>

        <!-- IMAGEN -->
        <div class="col-lg-6">
          <div class="card shadow-lg rounded-4 p-4"
            style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(10px);">

            <h4 class="mb-3 d-flex align-items-center gap-2">
              <i class="bi bi-images text-primary"></i>
              {{ t.images }}
            </h4>

            <img :src="pabellon.imagenURL" class="img-fluid rounded mb-3 img-hover" />

            <input v-if="editando" type="file" class="form-control form-control-lg" @change="onFileChange" />
            <img v-if="preview" :src="preview" class="img-fluid rounded mb-3" />
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
          <i class="bi bi-pencil me-2"></i> {{ t.modifyPavilion }}
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
          <i class="bi bi-trash me-2"></i> {{ t.deletePavilion }}
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
            <p>{{ t.confirmDeletePavilion }}</p>
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
import { inject, ref, onMounted, type Ref } from 'vue';
import { useRouter } from "vue-router";
import { Modal } from 'bootstrap'

import { getPabellonDetalle, modificarPabellon, eliminarPabellon } from "@/services/detalleService";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();

const editando = ref(false)
const imagen = ref<File | null>(null)
const preview = ref<string | null>(null)
const mensaje = ref("")

const pabellon = ref({
  id: 0,
  nombre: "",
  descripcion: "",
  imagenURL: "",
  direccion: ""
})

const errores = ref({
  nombre: false
})

const pabellonOriginal = ref<any>(null);

function validarFormulario() {
  let valido = true
  errores.value.nombre = pabellon.value.nombre.trim() === ''
  if (errores.value.nombre) valido = false
  return valido
}

function activarEdicion() {
  mensaje.value = ""
  pabellonOriginal.value = JSON.parse(JSON.stringify(pabellon.value))
  errores.value.nombre = false
  editando.value = true
}

function cancelarEdicion() {
  mensaje.value = ""
  pabellon.value = JSON.parse(JSON.stringify(pabellonOriginal.value))
  preview.value = null
  imagen.value = null
  editando.value = false
}

function camposModificados() {
  const data: any = {}

  if (pabellonOriginal.value.nombre !== pabellon.value.nombre) {
    data.nombre = pabellon.value.nombre
  }
  if (pabellonOriginal.value.descripcion !== pabellon.value.descripcion) {
    data.descripcion = pabellon.value.descripcion
  }
  if (pabellonOriginal.value.direccion !== pabellon.value.direccion) {
    data.direccion = pabellon.value.direccion
  }
 
  return data
}

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  if (!input.files || input.files.length === 0) return
  imagen.value = input.files[0]
  preview.value = URL.createObjectURL(imagen.value)
}

const guardarCambios = async () => {
  mensaje.value = ""
  if (!validarFormulario()) return

  const data = camposModificados()
  const formData = new FormData()

  Object.entries(data).forEach(([key, value]) => {
    formData.append(key, String(value))
  })

  if (imagen.value) {
    formData.append("imagenURL", imagen.value)
  }

  if (formData.has("nombre") || formData.has("descripcion") || formData.has("direccion") || imagen.value) {
    try {
      await modificarPabellon(pabellon.value.id, formData)
      editando.value = false
    } catch (e) {
      console.error("Error al modificar el pabellon", e)
    }
  } else {
    editando.value = false
  }
}

let confirmModal: Modal
let successModal: Modal

const eliminado = ref(false)

function abrirConfirmacion() {
  confirmModal.show()
}

async function confirmarEliminar() {
  try {
    await eliminarPabellon(pabellon.value.id)

    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.pavilionDeleted
    eliminado.value = true
  } catch (e) {
    mensaje.value = t.value.noDeleted
    eliminado.value = false
    console.error("Error al eliminar el pabellon", e);
  }
}

const finalizar = async () => {
  if (eliminado.value) {
    router.push({ name: 'gestion-espacios' });
  } else {
    successModal.hide()
    eliminado.value = false
  }
}

const volver = () => router.back();

onMounted(async () => {
  confirmModal = new Modal(document.getElementById('confirmDeleteModal')!)
  successModal = new Modal(document.getElementById('successDeleteModal')!)

  try {
    pabellon.value = await getPabellonDetalle(parseInt(props.id))
    pabellonOriginal.value = JSON.parse(JSON.stringify(pabellon.value))
  } catch (e) {
    mensaje.value = t.value.unexpectedError
    console.error("Error al obtener información del pabellon", e)
  }
})
</script>