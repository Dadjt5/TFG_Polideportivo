<template>
  <div class="min-vh-100 pt-4" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4" style="max-width: 1600px;">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4 mt-3">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold text-primary mb-2" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
          <p v-if="bono.nombreInstalacion">
            <strong>{{ t.facility }}:</strong> {{ bono.nombreInstalacion }}
          </p>
          <p v-else>
            <strong>{{ t.sport }}:</strong> {{ bono.nombreDeporte }}
          </p>
        </h1>

        <div style="width: 100px"></div>
      </div>

      <div class="row g-4">

        <!-- INFORMACIÓN GENERAL -->
        <div class="col-lg-6">
          <div class="card shadow-lg rounded-4 p-4"
               style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(10px);">

            <h4 class="mb-3 d-flex align-items-center">
              <i class="bi bi-currency-euro text-primary me-2"></i>
              {{ t.bonusDetail }}
            </h4>

            <div class="row g-3">

              <!-- USOS -->
              <div class="col-6">
                <span class="fw-medium">{{ t.uses }}:</span>
                <p v-if="!editando">{{ bono.usos }}</p>
                <input v-else type="number" min="1" class="form-control"
                       v-model.number="bono.usos"
                       :class="{ 'is-invalid': errores.usos }" />
              </div>

              <!-- VALIDEZ -->
              <div class="col-6">
                <span class="fw-medium">{{ t.validity }}:</span>
                <p v-if="!editando">{{ bono.validez }}</p>
                <input v-else type="number" min="1" class="form-control"
                       v-model.number="bono.validez"
                       :class="{ 'is-invalid': errores.validez }" />
              </div>

            </div>

          </div>
        </div>

        <!-- PRECIOS -->
        <div class="col-lg-6">
          <div class="bg-white rounded-3 shadow-sm p-4 h-100">

            <h4 class="mb-3">
              <i class="bi bi-cash-coin text-success me-2"></i>
              {{ t.prices }}
            </h4>

            <div class="row g-3">

              <div class="col-6">
                <span class="fw-medium">{{ t.priceTDA }}:</span>
                <p v-if="!editando">{{ bono.precioTDA }} €</p>
                <input v-else type="number" step="0.01" min="0" class="form-control"
                       v-model.number="bono.precioTDA"
                       :class="{ 'is-invalid': errores.precioTDA }" />
              </div>

              <div class="col-6">
                <span class="fw-medium">{{ t.priceUAM }}:</span>
                <p v-if="!editando">{{ bono.precioUAM }} €</p>
                <input v-else type="number" step="0.01" min="0" class="form-control"
                       v-model.number="bono.precioUAM"
                       :class="{ 'is-invalid': errores.precioUAM }" />
              </div>

              <div class="col-6">
                <span class="fw-medium">{{ t.priceSubscripcion }}:</span>
                <p v-if="!editando">{{ bono.precioAbono }} €</p>
                <input v-else type="number" step="0.01" min="0" class="form-control"
                       v-model.number="bono.precioAbono"
                       :class="{ 'is-invalid': errores.precioAbono }" />
              </div>

              <div class="col-6">
                <span class="fw-medium">{{ t.priceOthers }}:</span>
                <p v-if="!editando">{{ bono.precioOtros }} €</p>
                <input v-else type="number" step="0.01" min="0" class="form-control"
                       v-model.number="bono.precioOtros"
                       :class="{ 'is-invalid': errores.precioOtros }" />
              </div>

            </div>

          </div>
        </div>

        <!-- RELACIONES -->
        <div class="col-12">
          <div class="bg-white rounded-3 shadow-sm p-4">
            <div class="row g-3">

              <!-- INSTALACIÓN -->
              <div class="col-md-6">
                <span class="fw-medium">{{ t.facility }}:</span>
                <p v-if="!editando">{{ bono.nombreInstalacion || "—" }}</p>

                <select v-else class="form-select"
                        v-model="bono.instalacion"
                        :class="{ 'is-invalid': errores.instalacion }">
                  <option v-for="i in instalaciones" :key="i.id" :value="i.id">
                    {{ i.nombre }}
                  </option>
                </select>
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
          <i class="bi bi-pencil me-2"></i> {{ t.modifyBonus }}
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
          <i class="bi bi-trash me-2"></i> {{ t.deleteBonus }}
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
            <p>{{ t.confirmDeleteBonus }}</p>
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
  getBonoDetalle,
  modificarBono,
  eliminarBono,
} from '@/services/abonoBonoService'
import { getInstalacionesSimples } from '@/services/listadoService';

import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ id: string }>();
const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);
const router = useRouter();

const editando = ref(false);
const bono = ref<any>({});
const bonoOriginal = ref<any>(null);
const mensaje = ref("");

const instalaciones = ref<any[]>([]);

const errores = ref({
  usos: false,
  validez: false,
  precioTDA: false,
  precioUAM: false,
  precioAbono: false,
  precioOtros: false,
  instalacion: false
})

function activarEdicion() {
  mensaje.value = ""
  bonoOriginal.value = JSON.parse(JSON.stringify(bono.value));
  editando.value = true;
}

function cancelarEdicion() {
  mensaje.value = ""
  bono.value = JSON.parse(JSON.stringify(bonoOriginal.value));
  editando.value = false;
}

function camposModificados() {
  const data: any = {};
  for (const key in bono.value) {
    if (bono.value[key] !== bonoOriginal.value[key]) {
      data[key] = bono.value[key];
    }
  }
  return data;
}

function validar() {
  let valido = true

  errores.value.usos = bono.value.usos <= 0
  errores.value.validez = bono.value.validez <= 0
  errores.value.precioTDA = bono.value.precioTDA <= 0
  errores.value.precioUAM = bono.value.precioUAM <= 0
  errores.value.precioAbono = bono.value.precioAbono <= 0
  errores.value.precioOtros = bono.value.precioOtros <= 0
  errores.value.instalacion = !bono.value.instalacion

  for (const key in errores.value) {
    if (errores.value[key]) valido = false
  }

  return valido
}

const guardarCambios = async () => {
  mensaje.value = ""
  if (!validar()) return

  const data = camposModificados();
  if (Object.keys(data).length > 0) {
    await modificarBono(bono.value.id, data);
    bonoOriginal.value = JSON.parse(JSON.stringify(bono.value));
    editando.value = false;
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
    await eliminarBono(bono.value.id);

    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.bonusDeleted
    eliminado.value = true
  } catch (e) {
    mensaje.value = t.value.noDeleted
    eliminado.value = false
    console.error("Error al eliminar el bono", e);
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
    bono.value = await getBonoDetalle(id);
    bonoOriginal.value = JSON.parse(JSON.stringify(bono.value));
    instalaciones.value = await getInstalacionesSimples();
  } catch(e) {
    mensaje.value = t.value.unexpectedError
    console.error("Error al obtener los bonos y/o instalaciones", e)
  }
});
</script>