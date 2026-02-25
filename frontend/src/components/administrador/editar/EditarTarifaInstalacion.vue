<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-5" style="max-width: 900px;">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-bold text-center mb-4 display-5">
          <span v-if="!editando">{{ tarifa.titulo }}</span>
          <input
            v-else
            v-model="tarifa.titulo"
            class="form-control form-control-lg text-center fw-semibold"
            :class="{ 'is-invalid': errores.titulo }"
            :placeholder="tarifa.titulo"
          />
        </h1>

        <div style="width: 100px"></div>
      </div>

      <div class="row g-4">

        <!-- INFORMACIÓN DE TARIFAS -->
        <div class="col-12">
          <div class="bg-white rounded-4 shadow p-5 h-100">
            <h4 class="mb-3 d-flex align-items-center">
              <i class="bi bi-cash-stack text-primary me-2"></i>
              {{ t.tariffDetail }}
            </h4>

            <div class="row g-3">

              <!-- PRECIO ABONADO -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.priceSubscripcion }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.precioAbonado }} €</p>
                <input
                  v-else
                  type="number"
                  min="0"
                  step="0.01"
                  class="form-control form-control-lg"
                  v-model.number="tarifa.precioAbonado"
                  :class="{ 'is-invalid': errores.precioAbonado }"
                />
              </div>

              <!-- PRECIO UAM -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.priceUAM }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.precioUAM }} €</p>
                <input
                  v-else
                  type="number"
                  min="0"
                  step="0.01"
                  class="form-control form-control-lg"
                  v-model.number="tarifa.precioUAM"
                  :class="{ 'is-invalid': errores.precioUAM }"
                />
              </div>

              <!-- PRECIO TDA -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.priceTDA }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.precioTDA }} €</p>
                <input
                  v-else
                  type="number"
                  min="0"
                  step="0.01"
                  class="form-control form-control-lg"
                  v-model.number="tarifa.precioTDA"
                  :class="{ 'is-invalid': errores.precioTDA }"
                />
              </div>

              <!-- PRECIO OTROS -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.priceOthers }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.precioOtros }} €</p>
                <input
                  v-else
                  type="number"
                  min="0"
                  step="0.01"
                  class="form-control form-control-lg"
                  v-model.number="tarifa.precioOtros"
                  :class="{ 'is-invalid': errores.precioOtros }"
                />
              </div>

              <!-- POR DEFECTO -->
              <div class="col-12">
                <span class="fw-medium">{{ t.defaultTariff }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.por_defecto ? t.yes : 'No' }}</p>
                <div v-else class="form-check mt-1">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    v-model="tarifa.por_defecto"
                    id="defaultCheck"
                  />
                  <label class="form-check-label" for="defaultCheck">
                    {{ t.defaultTariff }}
                  </label>
                </div>
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
          {{ t.modifyTariff }}
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
          {{ t.deleteTariff }}
        </button>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, inject, onMounted, type Ref } from 'vue';
import { useRouter } from 'vue-router';

import { getTarifaInstalacionDetalle, modificarTarifaInstalacion, eliminarTarifaInstalacion } from '@/services/detalleTarifaService';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();
const editando = ref(false);

const tarifa = ref({
  id: 0,
  titulo: '',
  precioAbonado: 0,
  precioUAM: 0,
  precioTDA: 0,
  precioOtros: 0,
  por_defecto: false
});

const errores = ref({
  titulo: false,
  precioAbonado: false,
  precioUAM: false,
  precioTDA: false,
  precioOtros: false
});

const tarifaOriginal = ref<any>(null);

function validarFormulario() {
  let valido = true;
  errores.value.titulo = tarifa.value.titulo === '';
  errores.value.precioAbonado = tarifa.value.precioAbonado < 0;
  errores.value.precioUAM = tarifa.value.precioUAM < 0;
  errores.value.precioTDA = tarifa.value.precioTDA < 0;
  errores.value.precioOtros = tarifa.value.precioOtros < 0;

  for (const key in errores.value) {
    if (errores.value[key]) valido = false;
  }

  return valido;
}

function activarEdicion() {
  tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value));
  Object.keys(errores.value).forEach(k => errores.value[k] = false);
  editando.value = true;
}

function cancelarEdicion() {
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
  if (!validarFormulario()) return;
  const data = camposModificados();
  if (Object.keys(data).length > 0) {
    await modificarTarifaInstalacion(tarifa.value.id, data);
    tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value));
    editando.value = false;
  }
}

const eliminar = async () => {
  await eliminarTarifaInstalacion(tarifa.value.id);
  router.back();
};

const volver = () => router.back();

onMounted(async () => {
  const id = parseInt(props.id);
  tarifa.value = await getTarifaInstalacionDetalle(id);
  tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value));
});
</script>
