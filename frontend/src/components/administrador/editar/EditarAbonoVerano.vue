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
          <span>{{ t.summerSubscription }}</span>
        </h1>

        <div style="width: 100px"></div>
      </div>

      <div class="row justify-content-center">
        <div class="col-lg-6">
          <div class="bg-white rounded-3 shadow-sm p-4">

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
      <div class="d-flex justify-content-center gap-4 mt-5">

        <button
          v-if="!editando"
          class="btn btn-primary btn-lg rounded-pill"
          @click="activarEdicion"
        >
          <i class="bi bi-pencil me-2"></i>
          {{ t.modifySummerSubscription }}
        </button>

        <template v-else>
          <button
            class="btn btn-success btn-lg rounded-pill"
            @click="guardarCambios"
          >
            <i class="bi bi-check-lg me-2"></i>
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
          <i class="bi bi-trash me-2"></i>
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