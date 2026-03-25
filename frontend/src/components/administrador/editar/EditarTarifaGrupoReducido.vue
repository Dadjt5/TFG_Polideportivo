<template>
  <div class="min-vh-100 pt-4" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4" style="max-width: 1600px;">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4 mt-3">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold text-primary mb-2" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
          {{ tarifa.titulo }}
        </h1>

        <div style="width: 100px"></div>
      </div>

      <div class="row g-4">

        <div class="col-12">
          <div class="card shadow-lg rounded-4 p-4"
            style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(10px);">

            <h4 class="mb-3 d-flex align-items-center">
              <i class="bi bi-people-fill text-primary me-2"></i>
              {{ t.tariffDetail }}
            </h4>

            <div class="row g-3">

              <!-- Titulo -->
              <div class="col-12 col-sm-6">
                <span v-if="!editando">{{ tarifa.titulo }}</span>
                <input v-else v-model="tarifa.titulo" class="form-control form-control-lg text-center fw-semibold"
                  :class="{ 'is-invalid': errores.titulo }" :placeholder="tarifa.titulo" />
              </div>

              <!-- NUMERO HORAS -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.numberOfHours }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.numeroHoras }}</p>
                <input v-else type="number" min="0" class="form-control form-control-lg"
                  v-model.number="tarifa.numeroHoras" :class="{ 'is-invalid': errores.numeroHoras }" />
              </div>

              <!-- NUMERO PERSONAS -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.numberOfPeople }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.numeroPersonas }}</p>
                <input v-else type="number" min="1" class="form-control form-control-lg"
                  v-model.number="tarifa.numeroPersonas" :class="{ 'is-invalid': errores.numeroPersonas }" />
              </div>

              <!-- PRECIO BASE -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.price }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.precio }} €</p>
                <input v-else type="number" min="0" step="0.01" class="form-control form-control-lg"
                  v-model.number="tarifa.precio" :class="{ 'is-invalid': errores.precio }" />
              </div>

              <!-- PRECIO CUATRIMESTRE -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.quarterPrice }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.precioCuatrimestre }} €</p>
                <input v-else type="number" min="0" step="0.01" class="form-control form-control-lg"
                  v-model.number="tarifa.precioCuatrimestre" :class="{ 'is-invalid': errores.precioCuatrimestre }" />
              </div>

              <!-- PRECIO MENSUAL -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.monthlyPrice }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.precioMensual }} €</p>
                <input v-else type="number" min="0" step="0.01" class="form-control form-control-lg"
                  v-model.number="tarifa.precioMensual" :class="{ 'is-invalid': errores.precioMensual }" />
              </div>
            </div>
          </div>
        </div>

      </div>

      <div v-if="mostrarMensaje" class="text-center mb-3">
        <div class="alert" :class="tipoMensaje === 'success' ? 'alert-success' : 'alert-danger'">
          {{ mensajeEditar }}
        </div>
      </div>

      <!-- ACCIONES -->
      <div class="d-flex justify-content-center gap-3 mt-5">
        <button v-if="!editando" class="btn btn-primary btn-lg rounded-pill" @click="activarEdicion">
          <i class="bi bi-pencil me-2"></i> {{ t.modifyTariff }}
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
          <i class="bi bi-trash me-2"></i> {{ t.deleteTariff }}
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
            <p>{{ t.confirmDeleteTariff }}</p>
          </div>

          <div class="modal-footer justify-content-center">
            <button class="btn btn-secondary rounded-pill" data-bs-dismiss="modal">
              {{ t.cancel }}
            </button>

            <button class="btn btn-danger rounded-pill" @click="confirmarEliminar">
              {{ t.delete }}
            </button>
          </div>

        </div>
      </div>
    </div>

    <div class="modal fade" id="successDeleteModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4 text-center">

          <div class="modal-body py-5">

            <i v-if="eliminado" class="bi bi-check-circle-fill text-success fs-1 mb-3"></i>
            <i v-else class="bi bi-exclamation-octagon-fill text-danger fs-1 mb-3"></i>

            <h4 class="fw-semibold">
              {{ mensaje }}
            </h4>

            <button class="btn btn-primary rounded-pill mt-4" @click="finalizar" data-bs-dismiss="modal">
              <span v-if="eliminado">{{ t.continue }}</span>
              <span v-else>{{ t.return }}</span>
            </button>

          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, inject, onMounted, type Ref } from 'vue'
import { useRouter } from 'vue-router'
import { Modal } from 'bootstrap'

import {
  getTarifaGrupoReducidoDetalle,
  modificarTarifaGrupoReducido,
  eliminarTarifaGrupoReducido
} from '@/services/detalleTarifaService'

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter()
const editando = ref(false)
const mensaje = ref("")
const mensajeEditar = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)

const tarifa = ref({
  id: 0,
  titulo: '',
  numeroHoras: 0,
  numeroPersonas: 0,
  precio: 0,
  precioCuatrimestre: 0,
  precioMensual: 0
})

const errores = ref({
  titulo: false,
  numeroHoras: false,
  numeroPersonas: false,
  precio: false,
  precioCuatrimestre: false,
  precioMensual: false
})

const tarifaOriginal = ref<any>(null)

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensajeEditar.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true

  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
}

function validarFormulario() {
  let valido = true

  errores.value.titulo = tarifa.value.titulo === ''
  errores.value.numeroHoras = tarifa.value.numeroHoras <= 0
  errores.value.numeroPersonas = tarifa.value.numeroPersonas <= 0
  errores.value.precio = tarifa.value.precio <= 0
  errores.value.precioCuatrimestre = tarifa.value.precioCuatrimestre <= 0
  errores.value.precioMensual = tarifa.value.precioMensual <= 0

  for (const key in errores.value) {
    if (errores.value[key]) valido = false
  }

  return valido
}

function activarEdicion() {
  mensaje.value = ""
  tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value))
  Object.keys(errores.value).forEach(k => errores.value[k] = false)
  editando.value = true
}

function cancelarEdicion() {
  mensaje.value = ""
  tarifa.value = JSON.parse(JSON.stringify(tarifaOriginal.value))
  editando.value = false
}

function camposModificados() {
  const data: any = {}
  for (const key in tarifa.value) {
    if (tarifa.value[key] !== tarifaOriginal.value[key]) {
      data[key] = tarifa.value[key]
    }
  }
  return data
}

const guardarCambios = async () => {
  if (!validarFormulario()) {
    lanzarMensaje(t.value.missing, "error")
    return
  }

  try {
    const data = camposModificados()
    if (Object.keys(data).length > 0) {
      await modificarTarifaGrupoReducido(tarifa.value.id, data)
      tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value))

      lanzarMensaje(t.value.correctlyUpdate, "success")
    } else {
      lanzarMensaje(t.value.noChanges, "success")
    }

    editando.value = false
  } catch(e) {
    lanzarMensaje(t.value.noModify, "error")
    console.error("Error al modificar la tarifa de grupo reducido", e)
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
    await eliminarTarifaGrupoReducido(tarifa.value.id)

    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.tariffDeleted
    eliminado.value = true
  } catch (e) {
    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.tariffNoDeleted
    eliminado.value = false
    console.error("Error al eliminar la tarifa de grupo reducido", e);
  }
}

const finalizar = async () => {
  if (eliminado.value) {
    router.push({ name: 'gestion-tarifas' });
  } else {
    successModal.hide()
    eliminado.value = false
  }
}

const volver = () => router.back()

onMounted(async () => {
  const id = parseInt(props.id)

  confirmModal = new Modal(document.getElementById('confirmDeleteModal')!)
  successModal = new Modal(document.getElementById('successDeleteModal')!)

  try {
    tarifa.value = await getTarifaGrupoReducidoDetalle(id)
    tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value))
  } catch (e) {
    mensaje.value = t.value.unexpectedError
    console.error("Error al obtener la informacion de la tarifa de grupo reducido", e)
  }
})
</script>
