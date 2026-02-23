<template>
  <div class="min-vh-100 bg-light">
    <main class="container-fluid mt-2 px-5 py-4">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold mb-0">
          <i class="bi bi-calendar-check text-primary me-2"></i>
          <span>{{ t.sportsSubscription }}</span>
        </h1>

        <div style="width: 100px"></div>
      </div>

      <div class="row g-4">

        <!-- INFORMACIÓN GENERAL -->
        <div class="col-lg-6">
          <div class="bg-white rounded-3 shadow-sm p-4 h-100">
            <div class="row g-3">

							<!-- nombre -->
              <div class="col-6">
                <span class="fw-medium">{{ t.name }}:</span>
                <p v-if="!editando">{{ abono.nombre }}</p>
                <input v-else type="text"
                  class="form-control"
                  v-model.number="abono.nombre"
                />
              </div>

              <!-- MESES -->
              <div class="col-6">
                <span class="fw-medium">{{ t.months }}:</span>
                <p v-if="!editando">{{ abono.meses }}</p>
                <input v-else type="number" min="1"
                  class="form-control"
                  v-model.number="abono.meses"
                />
              </div>

              <!-- PRECIO TOTAL MENSUAL UAM -->
              <div class="col-6">
                <span class="fw-medium">{{ t.monthlyPriceUAM }}:</span>
                <p v-if="!editando">{{ abono.precioTotalMensual }} €</p>
                <input v-else type="number" step="0.01" min="0"
                  class="form-control"
                  v-model.number="abono.precioTotalMensual"
                />
              </div>

              <!-- PRECIO PAGO ÚNICO UAM -->
              <div class="col-6">
                <span class="fw-medium">{{ t.totalPriceUAM }}:</span>
                <p v-if="!editando">{{ abono.precioPagoUnicoUAM }} €</p>
                <input v-else type="number" step="0.01" min="0"
                  class="form-control"
                  v-model.number="abono.precioPagoUnicoUAM"
                />
              </div>

              <!-- PRECIO FAMILIAR -->
              <div class="col-6">
                <span class="fw-medium">{{ t.familyPrice }}:</span>
                <p v-if="!editando">{{ abono.precioFamiliar }} €</p>
                <input v-else type="number" step="0.01" min="0"
                  class="form-control"
                  v-model.number="abono.precioFamiliar"
                />
              </div>

              <!-- OTROS -->
              <div class="col-6">
                <span class="fw-medium">{{ t.monthlyPriceOthers }}:</span>
                <p v-if="!editando">{{ abono.precioTotalMensualOtros }} €</p>
                <input v-else type="number" step="0.01" min="0"
                  class="form-control"
                  v-model.number="abono.precioTotalMensualOtros"
                />
              </div>

              <div class="col-6">
                <span class="fw-medium">{{ t.totalPriceOthers }}:</span>
                <p v-if="!editando">{{ abono.precioPagoUnicoOtros }} €</p>
                <input v-else type="number" step="0.01" min="0"
                  class="form-control"
                  v-model.number="abono.precioPagoUnicoOtros"
                />
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
                <input v-else type="number" step="0.1" min="0"
                  class="form-control"
                  v-model.number="abono.descuentoPrimeraActividad"
                />
              </div>

              <div class="col-12">
                <span class="fw-medium">{{ t.otherActivitiesDiscount }} (%):</span>
                <p v-if="!editando">{{ abono.descuentoRestoActividades }}</p>
                <input v-else type="number" step="0.1" min="0"
                  class="form-control"
                  v-model.number="abono.descuentoRestoActividades"
                />
              </div>

              <div class="col-12">
                <span class="fw-medium">{{ t.outdoorDiscount }} (%):</span>
                <p v-if="!editando">{{ abono.descuentoActividadesExteriores }}</p>
                <input v-else type="number" step="0.1" min="0"
                  class="form-control"
                  v-model.number="abono.descuentoActividadesExteriores"
                />
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
          {{ t.modifySportSubscription }}
        </button>

        <template v-else>
          <button
            class="btn btn-success btn-lg rounded-pill"
            @click="guardarCambios"
          >
            {{ t.saveChanges }}
          </button>

          <button
            class="btn btn-secondary btn-lg rounded-pill"
            @click="cancelarEdicion"
          >
            {{ t.cancel }}
          </button>
        </template>

        <button
          v-if="!editando"
          class="btn btn-danger btn-lg rounded-pill"
          @click="eliminar"
        >
          {{ t.delete }}
        </button>

      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, inject, onMounted, type Ref } from 'vue'
import { useRouter } from 'vue-router'

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

const errores = ref({
  nombre: false
});

function activarEdicion() {
  abonoOriginal.value = JSON.parse(JSON.stringify(abono.value));
  editando.value = true;
}

function cancelarEdicion() {
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

const guardarCambios = async () => {
  const data = camposModificados();
  if (Object.keys(data).length > 0) {
    await modificarAbonoDeportivo(abono.value.id, data);
    abonoOriginal.value = JSON.parse(JSON.stringify(abono.value));
    editando.value = false;
  }
};

const eliminar = async () => {
  await eliminarAbonoDeportivo(abono.value.id);
  router.back();
};

const volver = () => router.back();

onMounted(async () => {
  const id = parseInt(props.id);
  abono.value = await getAbonoDeportivoDetalle(id);
  abonoOriginal.value = JSON.parse(JSON.stringify(abono.value));
});
</script>