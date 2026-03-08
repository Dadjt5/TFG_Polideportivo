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
              <div class="col-6">
                <span class="fw-medium">{{ t.name }}:</span>
                <p v-if="!editando">{{ abono.nombre }}</p>
                <input v-else type="text"
                  class="form-control"
                  v-model.number="abono.nombre"
                />
              </div>

            <div class="row g-3">

              <!-- PRECIO TDA -->
              <div class="col-12">
                <span class="fw-medium">{{ t.priceTDA }}:</span>
                <p v-if="!editando">{{ abono.precioTDA }} €</p>
                <input
                  v-else
                  type="number"
                  step="0.01"
                  min="0"
                  class="form-control"
                  v-model.number="abono.precioTDA"
                />
              </div>

              <!-- PRECIO UAM -->
              <div class="col-12">
                <span class="fw-medium">{{ t.priceUAM }}:</span>
                <p v-if="!editando">{{ abono.precioUAM }} €</p>
                <input
                  v-else
                  type="number"
                  step="0.01"
                  min="0"
                  class="form-control"
                  v-model.number="abono.precioUAM"
                />
              </div>

              <!-- PRECIO OTROS -->
              <div class="col-12">
                <span class="fw-medium">{{ t.priceOthers }}:</span>
                <p v-if="!editando">{{ abono.precioOtros }} €</p>
                <input
                  v-else
                  type="number"
                  step="0.01"
                  min="0"
                  class="form-control"
                  v-model.number="abono.precioOtros"
                />
              </div>

            </div>

          </div>
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

        <button v-if="!editando" class="btn btn-danger btn-lg rounded-pill" @click="eliminar">
          <i class="bi bi-trash me-2"></i> {{ t.delete }}
        </button>

      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, inject, onMounted, type Ref } from 'vue'
import { useRouter } from 'vue-router'

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
    await modificarAbonoVerano(abono.value.id, data);
    abonoOriginal.value = JSON.parse(JSON.stringify(abono.value));
    editando.value = false;
  }
};

const eliminar = async () => {
  await eliminarAbonoVerano(abono.value.id);
  router.back();
};

const volver = () => router.back();

onMounted(async () => {
  const id = parseInt(props.id);
  abono.value = await getAbonoVeranoDetalle(id);
  abonoOriginal.value = JSON.parse(JSON.stringify(abono.value));
});
</script>