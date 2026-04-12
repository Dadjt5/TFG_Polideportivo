<template>
  <div class="min-vh-100 pt-4" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4" style="max-width: 1600px;">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4 mt-3">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold text-primary mb-2" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
          {{ abono.nombre }}
        </h1>

        <div style="width: 100px"></div>
      </div>

      <div class="row justify-content-center">
        <div class="col-lg-6">
          <div class="card shadow-lg rounded-4 p-4"
            style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(10px);">

            <h4 class="mb-3 d-flex align-items-center">
              <i class="bi bi-currency-euro text-primary me-2"></i>
              {{ t.summerSubscriptionDetail }}
            </h4>

            <!-- nombre -->
            <div class="col-6 mb-3">
              <span class="fw-medium">{{ t.name }}:</span>
              <p v-if="!editando">{{ abono.nombre }}</p>
              <input v-else type="text" class="form-control" v-model="abono.nombre"
                :class="{ 'is-invalid': errores.nombre }" />
            </div>

            <div class="row g-3">

              <!-- PRECIO TDA -->
              <div class="col-12 mb-3">
                <span class="fw-medium">{{ t.priceTDA }}:</span>
                <p v-if="!editando">{{ abono.precioTDA }} €</p>
                <input v-else type="number" step="0.01" min="0" class="form-control" v-model.number="abono.precioTDA"
                  :class="{ 'is-invalid': errores.precioTDA }" />
              </div>

              <!-- PRECIO UAM -->
              <div class="col-12 mb-3">
                <span class="fw-medium">{{ t.priceUAM }}:</span>
                <p v-if="!editando">{{ abono.precioUAM }} €</p>
                <input v-else type="number" step="0.01" min="0" class="form-control" v-model.number="abono.precioUAM"
                  :class="{ 'is-invalid': errores.precioUAM }" />
              </div>

              <!-- PRECIO OTROS -->
              <div class="col-12 mb-3">
                <span class="fw-medium">{{ t.priceOthers }}:</span>
                <p v-if="!editando">{{ abono.precioOtros }} €</p>
                <input v-else type="number" step="0.01" min="0" class="form-control" v-model.number="abono.precioOtros"
                  :class="{ 'is-invalid': errores.precioOtros }" />
              </div>

            </div>

          </div>
        </div>
      </div>

      <div v-if="mostrarMensaje" class="text-center mb-3 mt-3">
        <div class="alert" :class="tipoMensaje === 'success' ? 'alert-success' : 'alert-danger'">
          {{ mensajeEditar }}
        </div>
      </div>

      <!-- ACCIONES -->
      <div class="d-flex justify-content-center gap-3 mt-5">
        <button v-if="!editando" class="btn btn-primary btn-lg rounded-pill" @click="activarEdicion">
          <i class="bi bi-pencil me-2"></i> {{ t.modifySummerSubscription }}
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
          <i class="bi bi-trash me-2"></i> {{ t.delete }}
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
            <p>{{ t.confirmDeleteSubscription }}</p>
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
  getAbonoVeranoDetalle,
  modificarAbonoVerano,
  eliminarAbonoVerano
} from '@/services/abonoBonoService'

import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ id: string }>();
const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);
const router = useRouter();

const editando = ref(false);
const abono = ref<any>({});
const abonoOriginal = ref<any>(null);
const mensaje = ref("");
const mensajeEditar = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)

// ERRORES
const errores = ref({
  nombre: false,
  precioTDA: false,
  precioUAM: false,
  precioOtros: false
})

function activarEdicion() {
  abonoOriginal.value = JSON.parse(JSON.stringify(abono.value));
  editando.value = true;
}

function cancelarEdicion() {
  abono.value = JSON.parse(JSON.stringify(abonoOriginal.value));
  editando.value = false;
}

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensajeEditar.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true

  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
}

function camposModificados() {
  const data: any = {};
  for (const key in abono.value) {
    if (abono.value[key] !== abonoOriginal.value[key]) {
      data[key] = abono.value[key];
    }
  }
  return data;
}

// VALIDACIÓN
function validar() {
  let valido = true;

  errores.value.nombre = !abono.value.nombre || abono.value.nombre.trim() === '';
  errores.value.precioTDA = abono.value.precioTDA <= 0;
  errores.value.precioUAM = abono.value.precioUAM <= 0;
  errores.value.precioOtros = abono.value.precioOtros <= 0;

  for (const key in errores.value) {
    if (errores.value[key]) valido = false;
  }

  return valido;
}

const guardarCambios = async () => {
  if (!validar()) {
    lanzarMensaje(t.value.missing, "error")
    return
  }

  const data = camposModificados();

  try {
    if (Object.keys(data).length > 0) {
      await modificarAbonoVerano(abono.value.id, data);
      abonoOriginal.value = JSON.parse(JSON.stringify(abono.value));

      lanzarMensaje(t.value.correctlyUpdate, "success")
      editando.value = false;
    } else {
      lanzarMensaje(t.value.noChanges, "success")
      return;
    }
  } catch(e) {
    lanzarMensaje(t.value.noModify, "error")
    console.error('Error al modificar el abono de verano', e) 
  }
};

let confirmModal: Modal
let successModal: Modal

const eliminado = ref(false)

function abrirConfirmacion() {
  confirmModal.show()
}

async function confirmarEliminar() {
  try {
    await eliminarAbonoVerano(abono.value.id)

    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.subscriptionDeleted
    eliminado.value = true
  } catch (e) {
    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.subscriptionNoDeleted
    eliminado.value = false
    console.error("Error al eliminar el abono de verano", e);
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
    abono.value = await getAbonoVeranoDetalle(id);
    abonoOriginal.value = JSON.parse(JSON.stringify(abono.value));
  } catch (e) {
    mensaje.value = t.value.unexpectedError
    console.error("Error al obtener la informacion de los abonos", e)
  }
});
</script>