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

        <div style="width: 100px"></div>
      </div>

      <div class="row g-4">

        <!-- INFORMACIÓN DE TARIFAS -->
        <div class="col-12">
          <div class="card shadow-lg rounded-4 p-4"
            style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(10px);">

            <h4 class="mb-3 d-flex align-items-center">
              <i class="bi bi-cash-stack text-primary me-2"></i>
              {{ t.tariffDetail }}
            </h4>

            <div class="row g-3">

              <!-- Titulo -->
              <div class="col-12 col-sm-6">
                <span v-if="!editando">{{ tarifa.titulo }}</span>
                <input v-else v-model="tarifa.titulo" class="form-control form-control-lg text-center fw-semibold"
                  :class="{ 'is-invalid': errores.titulo }" :placeholder="tarifa.titulo" />
              </div>

              <!-- PRECIO ABONADO -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.priceSubscripcion }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.precioAbonado }} €</p>
                <input v-else type="number" min="0" step="0.01" class="form-control form-control-lg"
                  v-model.number="tarifa.precioAbonado" :class="{ 'is-invalid': errores.precioAbonado }" />
              </div>

              <!-- PRECIO UAM -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.priceUAM }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.precioUAM }} €</p>
                <input v-else type="number" min="0" step="0.01" class="form-control form-control-lg"
                  v-model.number="tarifa.precioUAM" :class="{ 'is-invalid': errores.precioUAM }" />
              </div>

              <!-- PRECIO TDA -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.priceTDA }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.precioTDA }} €</p>
                <input v-else type="number" min="0" step="0.01" class="form-control form-control-lg"
                  v-model.number="tarifa.precioTDA" :class="{ 'is-invalid': errores.precioTDA }" />
              </div>

              <!-- PRECIO OTROS -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.priceOthers }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.precioOtros }} €</p>
                <input v-else type="number" min="0" step="0.01" class="form-control form-control-lg"
                  v-model.number="tarifa.precioOtros" :class="{ 'is-invalid': errores.precioOtros }" />
              </div>

              <!-- COSTE ILUMINACION -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.lightCost }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.costeIluminacion }} €</p>
                <input v-else type="number" min="0" step="0.01" class="form-control form-control-lg"
                  v-model.number="tarifa.costeIluminacion" :class="{ 'is-invalid': errores.costeIluminacion }" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="mostrarMensaje" class="text-center mt-3 mb-3">
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
import { ref, inject, onMounted, type Ref } from 'vue';
import { useRouter } from 'vue-router';
import { Modal } from 'bootstrap'

import { getTarifaInstalacionDetalle, modificarTarifaInstalacion, eliminarTarifaInstalacion } from '@/services/detalleTarifaService';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();
const editando = ref(false);
const mensaje = ref("")
const mensajeEditar = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)

const tarifa = ref({
  id: 0,
  titulo: '',
  precioAbonado: 0,
  precioUAM: 0,
  precioTDA: 0,
  precioOtros: 0,
  costeIluminacion: 0,
});

const errores = ref({
  titulo: false,
  precioAbonado: false,
  precioUAM: false,
  precioTDA: false,
  precioOtros: false,
  costeIluminacion: false
});

const tarifaOriginal = ref<any>(null);

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensajeEditar.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true

  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
}

function validarFormulario() {
  let valido = true;

  errores.value.titulo = tarifa.value.titulo === '';
  errores.value.precioAbonado = tarifa.value.precioAbonado <= 0;
  errores.value.precioUAM = tarifa.value.precioUAM <= 0;
  errores.value.precioTDA = tarifa.value.precioTDA <= 0;
  errores.value.precioOtros = tarifa.value.precioOtros <= 0;
  errores.value.costeIluminacion = tarifa.value.costeIluminacion <= 0;

  for (const key in errores.value) {
    if (errores.value[key]) valido = false;
  }

  return valido;
}

function activarEdicion() {
  mensaje.value = ""
  tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value));
  Object.keys(errores.value).forEach(k => errores.value[k] = false);
  editando.value = true;
}

function cancelarEdicion() {
  mensaje.value = ""
  tarifa.value = JSON.parse(JSON.stringify(tarifaOriginal.value));
  editando.value = false;
}

function camposModificados() {
  const data: any = {};
  for (const key in tarifa.value) {
    if (tarifa.value[key] !== tarifaOriginal.value[key]) {
      data[key] = tarifa.value[key];
    }
  }
  return data;
}

const guardarCambios = async () => {
  if (!validarFormulario()) {
    lanzarMensaje(t.value.missing, "error")
    return
  }

  try {
    const data = camposModificados();
    if (Object.keys(data).length > 0) {
      await modificarTarifaInstalacion(tarifa.value.id, data);
      tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value));

      lanzarMensaje(t.value.correctlyUpdate, "success")
    } else {
      lanzarMensaje(t.value.noChanges, "success")
    }

    editando.value = false
  } catch (e) {
    lanzarMensaje(t.value.noModify, "error")
    console.error("Error al modificar la tarifa de instalacion", e)
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
    await eliminarTarifaInstalacion(tarifa.value.id);

    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.tariffDeleted
    eliminado.value = true
  } catch (e) {
    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.tariffNoDeleted
    eliminado.value = false
    console.error("Error al eliminar la tarifa de la instalacion", e);
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

const volver = () => router.back();

onMounted(async () => {
  const id = parseInt(props.id);

  confirmModal = new Modal(document.getElementById('confirmDeleteModal')!)
  successModal = new Modal(document.getElementById('successDeleteModal')!)

  try {
    tarifa.value = await getTarifaInstalacionDetalle(id);
    tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value));
  } catch (e) {
    mensaje.value = t.value.unexpectedError
    console.error("Error al obtener la informacion de la tarifa de la instalacion", e)

  }
});
</script>
