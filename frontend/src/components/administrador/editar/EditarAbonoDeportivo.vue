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

      <div class="row g-4">

        <!-- INFORMACIÓN GENERAL -->
        <div class="col-lg-6">
          <div class="card shadow-lg rounded-4 p-4"
            style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(10px);">

            <h4 class="mb-3 d-flex align-items-center">
              <i class="bi bi-currency-euro text-primary me-2"></i>
              {{ t.sportsSubscriptionDetail }}
            </h4>

            <div class="row g-3">

              <!-- NOMBRE -->
              <div class="col-6">
                <span class="fw-medium">{{ t.name }}:</span>
                <p v-if="!editando">{{ abono.nombre }}</p>
                <input v-else type="text" class="form-control" v-model="abono.nombre"
                  :class="{ 'is-invalid': errores.nombre }" />
              </div>

              <!-- MESES -->
              <div class="col-6">
                <span class="fw-medium">{{ t.months }}:</span>
                <p v-if="!editando">{{ abono.meses }}</p>
                <input v-else type="number" min="1" class="form-control" v-model.number="abono.meses"
                  :class="{ 'is-invalid': errores.meses }" />
              </div>

              <!-- PRECIO TOTAL MENSUAL UAM -->
              <div class="col-6">
                <span class="fw-medium">{{ t.monthlyPriceUAM }}:</span>
                <p v-if="!editando">{{ abono.precioTotalMensual }} €</p>
                <input v-else type="number" step="0.01" min="0" class="form-control"
                  v-model.number="abono.precioTotalMensual" :class="{ 'is-invalid': errores.precioTotalMensual }" />
              </div>

              <!-- PRECIO PAGO ÚNICO UAM -->
              <div class="col-6">
                <span class="fw-medium">{{ t.totalPriceUAM }}:</span>
                <p v-if="!editando">{{ abono.precioPagoUnicoUAM }} €</p>
                <input v-else type="number" step="0.01" min="0" class="form-control"
                  v-model.number="abono.precioPagoUnicoUAM" :class="{ 'is-invalid': errores.precioPagoUnicoUAM }" />
              </div>

              <!-- PRECIO FAMILIAR -->
              <div class="col-6">
                <span class="fw-medium">{{ t.familyPrice }}:</span>
                <p v-if="!editando">{{ abono.precioFamiliar }} €</p>
                <input v-else type="number" step="0.01" min="0" class="form-control"
                  v-model.number="abono.precioFamiliar" :class="{ 'is-invalid': errores.precioFamiliar }" />
              </div>

              <!-- OTROS -->
              <div class="col-6">
                <span class="fw-medium">{{ t.monthlyPriceOthers }}:</span>
                <p v-if="!editando">{{ abono.precioTotalMensualOtros }} €</p>
                <input v-else type="number" step="0.01" min="0" class="form-control"
                  v-model.number="abono.precioTotalMensualOtros"
                  :class="{ 'is-invalid': errores.precioTotalMensualOtros }" />
              </div>

              <div class="col-6">
                <span class="fw-medium">{{ t.totalPriceOthers }}:</span>
                <p v-if="!editando">{{ abono.precioPagoUnicoOtros }} €</p>
                <input v-else type="number" step="0.01" min="0" class="form-control"
                  v-model.number="abono.precioPagoUnicoOtros" :class="{ 'is-invalid': errores.precioPagoUnicoOtros }" />
              </div>

            </div>
          </div>
        </div>

        <!-- DESCUENTOS -->
        <div class="col-lg-6">
          <div class="bg-white rounded-3 shadow-sm p-4 h-100">
            <h4 class="mb-3">
              <i class="bi bi-percent text-success me-2"></i>
              {{ t.discount }}
            </h4>

            <div class="row g-3">

              <div class="col-12">
                <span class="fw-medium">{{ t.firstActivityDiscount }} (%):</span>
                <p v-if="!editando">{{ abono.descuentoPrimeraActividad }}</p>
                <input v-else type="number" step="0.1" min="0" class="form-control"
                  v-model.number="abono.descuentoPrimeraActividad"
                  :class="{ 'is-invalid': errores.descuentoPrimeraActividad }" />
              </div>

              <div class="col-12">
                <span class="fw-medium">{{ t.otherActivitiesDiscount }} (%):</span>
                <p v-if="!editando">{{ abono.descuentoRestoActividades }}</p>
                <input v-else type="number" step="0.1" min="0" class="form-control"
                  v-model.number="abono.descuentoRestoActividades"
                  :class="{ 'is-invalid': errores.descuentoRestoActividades }" />
              </div>

              <div class="col-12">
                <span class="fw-medium">{{ t.outdoorDiscount }} (%):</span>
                <p v-if="!editando">{{ abono.descuentoActividadesExteriores }}</p>
                <input v-else type="number" step="0.1" min="0" class="form-control"
                  v-model.number="abono.descuentoActividadesExteriores"
                  :class="{ 'is-invalid': errores.descuentoActividadesExteriores }" />
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
          <i class="bi bi-pencil me-2"></i> {{ t.modifySportSubscription }}
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
  getAbonoDeportivoDetalle,
  modificarAbonoDeportivo,
  eliminarAbonoDeportivo
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
const mensaje = ref("")

// ERRORES
const errores = ref({
  nombre: false,
  meses: false,
  precioTotalMensual: false,
  precioPagoUnicoUAM: false,
  precioFamiliar: false,
  precioTotalMensualOtros: false,
  precioPagoUnicoOtros: false,
  descuentoPrimeraActividad: false,
  descuentoRestoActividades: false,
  descuentoActividadesExteriores: false
})

function activarEdicion() {
  mensaje.value = ""
  abonoOriginal.value = JSON.parse(JSON.stringify(abono.value));
  editando.value = true;
}

function cancelarEdicion() {
  mensaje.value = ""
  abono.value = JSON.parse(JSON.stringify(abonoOriginal.value));
  editando.value = false;
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
  errores.value.meses = abono.value.meses <= 0;
  errores.value.precioTotalMensual = abono.value.precioTotalMensual <= 0;
  errores.value.precioPagoUnicoUAM = abono.value.precioPagoUnicoUAM <= 0;
  errores.value.precioFamiliar = abono.value.precioFamiliar <= 0;
  errores.value.precioTotalMensualOtros = abono.value.precioTotalMensualOtros <= 0;
  errores.value.precioPagoUnicoOtros = abono.value.precioPagoUnicoOtros <= 0;
  errores.value.descuentoPrimeraActividad = abono.value.descuentoPrimeraActividad <= 0;
  errores.value.descuentoRestoActividades = abono.value.descuentoRestoActividades <= 0;
  errores.value.descuentoActividadesExteriores = abono.value.descuentoActividadesExteriores <= 0;

  for (const key in errores.value) {
    if (errores.value[key]) valido = false;
  }

  return valido;
}

const guardarCambios = async () => {
  mensaje.value = ""
  if (!validar()) return;

  const data = camposModificados();
  if (Object.keys(data).length > 0) {
    await modificarAbonoDeportivo(abono.value.id, data);
    abonoOriginal.value = JSON.parse(JSON.stringify(abono.value));
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
    await eliminarAbonoDeportivo(abono.value.id)

    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.subscriptionDeleted
    eliminado.value = true
  } catch (e) {
    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.subscriptionNoDeleted
    eliminado.value = false
    console.error("Error al eliminar el abono deportivo", e);
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
    abono.value = await getAbonoDeportivoDetalle(id);
    abonoOriginal.value = JSON.parse(JSON.stringify(abono.value));
  } catch (e) {
    mensaje.value = t.value.unexpectedError
    console.log("Error al obtener la informacion de los abonos deportivos", e)
  }
});
</script>