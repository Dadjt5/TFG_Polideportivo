<template>
  <div class="min-vh-100 pt-4" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4" style="max-width: 1600px;">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4 mt-3">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold text-primary mb-2"
            style="text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">

          <span v-if="!editando">{{ tarifa.titulo }}</span>

          <input
            v-else
            v-model="tarifa.titulo"
            class="form-control form-control-lg text-center fw-semibold"
            :class="{ 'is-invalid': errores.titulo }"
          />
        </h1>

        <div style="width:100px"></div>
      </div>

      <!-- BLOQUES TARIFA -->
      <div class="row g-4">

        <!-- CONSULTA INDIVIDUAL -->
        <div class="col-12 col-md-6">
          <div class="card shadow-lg rounded-4 p-4"
          style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(10px);">

            <h4 class="mb-4 d-flex align-items-center">
              <i class="bi bi-person-badge text-primary me-2"></i>
              {{ t.initialConsultation }}
            </h4>

            <div class="row g-3">
              <PrecioField label="tdaPrice"
                v-model="tarifa.precioConsultaTDA"
                :editando="editando"
                :error="errores.precioConsultaTDA"
                :t="t"/>

              <PrecioField label="uamPrice"
                v-model="tarifa.precioConsultaUAM"
                :editando="editando"
                :error="errores.precioConsultaUAM"
                :t="t"/>

              <PrecioField label="otherPrice"
                v-model="tarifa.precioConsultaOtros"
                :editando="editando"
                :error="errores.precioConsultaOtros"
                :t="t"/>
            </div>

          </div>
        </div>


        <!-- BONO 1-5 -->
        <div class="col-12 col-md-6">
          <div class="card shadow-lg rounded-4 p-4"
          style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(10px);">

            <h4 class="mb-4 d-flex align-items-center">
              <i class="bi bi-123 text-success me-2"></i>
              {{ t.sessions1to5 }}
            </h4>

            <div class="row g-3">
              <PrecioField label="tdaPrice"
                v-model="tarifa.precioSesiones1_5TDA"
                :editando="editando"
                :error="errores.precioSesiones1_5TDA"
                :t="t"/>

              <PrecioField label="uamPrice"
                v-model="tarifa.precioSesiones1_5UAM"
                :editando="editando"
                :error="errores.precioSesiones1_5UAM"
                :t="t"/>

              <PrecioField label="otherPrice"
                v-model="tarifa.precioSesiones1_5Otros"
                :editando="editando"
                :error="errores.precioSesiones1_5Otros"
                :t="t"/>
            </div>

          </div>
        </div>


        <!-- BONO 6+ -->
        <div class="col-12 col-md-6 mx-auto">
          <div class="card shadow-lg rounded-4 p-4"
          style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(10px);">

            <h4 class="mb-4 d-flex align-items-center">
              <i class="bi bi-plus-circle text-warning me-2"></i>
              {{ t.sessions6plus }}
            </h4>

            <div class="row g-3">
              <PrecioField label="tdaPrice"
                v-model="tarifa.precioSesiones6TDA"
                :editando="editando"
                :error="errores.precioSesiones6TDA"
                :t="t"/>

              <PrecioField label="uamPrice"
                v-model="tarifa.precioSesiones6UAM"
                :editando="editando"
                :error="errores.precioSesiones6UAM"
                :t="t"/>

              <PrecioField label="otherPrice"
                v-model="tarifa.precioSesiones6Otros"
                :editando="editando"
                :error="errores.precioSesiones6Otros"
                :t="t"/>
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

        <button
          v-if="!editando"
          class="btn btn-primary btn-lg rounded-pill"
          @click="activarEdicion">

          <i class="bi bi-pencil me-2"></i>
          {{ t.modifyTariff }}
        </button>

        <template v-else>

          <button
            class="btn btn-success btn-lg rounded-pill"
            @click="guardarCambios">

            <i class="bi bi-check-lg me-2"></i>
            {{ t.saveChanges }}
          </button>

          <button
            class="btn btn-secondary btn-lg rounded-pill"
            @click="cancelarEdicion">

            {{ t.cancel }}
          </button>

        </template>

        <button
          v-if="!editando"
          class="btn btn-danger btn-lg rounded-pill"
          @click="abrirConfirmacion">

          <i class="bi bi-trash me-2"></i>
          {{ t.deleteTariff }}
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
import { ref, inject, onMounted, type Ref } from 'vue'
import { useRouter } from 'vue-router'
import { Modal } from 'bootstrap'

import {
  getTarifaFisioterapiaDetalle,
  modificarTarifaFisioterapia,
  eliminarTarifaFisioterapia
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

const tarifa = ref<any>({})
const tarifaOriginal = ref<any>(null)
const errores = ref<any>({})

function validarFormulario() {
  let valido = true

  errores.value.titulo = tarifa.value.titulo === ''

  for (const key in errores.value) {
    errores.value[key] = tarifa.value[key] <= 0
    if (errores.value[key]) valido = false
  }

  return valido
}

function activarEdicion() {
  mensaje.value = ""
  tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value))
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
  mensaje.value = ""
  if (!validarFormulario()) return
  const data = camposModificados()
  if (Object.keys(data).length > 0) {
    await modificarTarifaFisioterapia(tarifa.value.id, data)
    tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value))
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
    await eliminarTarifaFisioterapia(tarifa.value.id)

    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.tariffDeleted
    eliminado.value = true
  } catch (e) {
    mensaje.value = t.value.noDeleted
    eliminado.value = false
    console.error("Error al eliminar la tarifa de fisio", e);
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
    tarifa.value = await getTarifaFisioterapiaDetalle(id)
    tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value))
  }catch(e) {
    mensaje.value = t.value.unexpectedError
    console.error("Error al obtener la informacion de la tarifa de fisio", e)
  }
})
</script>
