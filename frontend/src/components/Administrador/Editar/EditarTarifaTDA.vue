<template>
  <div class="min-vh-100 bg-light">
    <main class="container-fluid mt-2 px-5 py-4">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold mb-0">
          <span v-if="!editando">{{ tarifa.nombre }}</span>
          <input
            v-else
            v-model="tarifa.nombre"
            class="form-control text-center fw-semibold"
            :class="{ 'is-invalid': errores.nombre }"
            placeholder="t.tariffName"
          />
        </h1>

        <div style="width: 100px"></div>
      </div>

      <div class="row g-4">

        <div class="col-lg-6">
          <div class="bg-white rounded-3 shadow-sm p-4 h-100">
            <h4 class="mb-3 d-flex align-items-center">
              <i class="bi bi-currency-euro text-primary me-2"></i>
              {{ t.tariffDetail }}
            </h4>

            <div class="row g-3">

              <!-- PRECIO UAM -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.priceUAM }}:</span>
                <p v-if="!editando">{{ tarifa.precioUAM }} €</p>
                <input
                  v-else
                  type="number"
                  min="0"
                  step="0.01"
                  class="form-control"
                  v-model.number="tarifa.precioUAM"
                  :class="{ 'is-invalid': errores.precioUAM }"
                />
              </div>

              <!-- PRECIO OTROS -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.priceOthers }}:</span>
                <p v-if="!editando">{{ tarifa.precioOtros }} €</p>
                <input
                  v-else
                  type="number"
                  min="0"
                  step="0.01"
                  class="form-control"
                  v-model.number="tarifa.precioOtros"
                  :class="{ 'is-invalid': errores.precioOtros }"
                />
              </div>

              <!-- PRECIO REPOSICIÓN -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.repositionPrice }}:</span>
                <p v-if="!editando">{{ tarifa.precioReposicion }} €</p>
                <input
                  v-else
                  type="number"
                  min="0"
                  step="0.01"
                  class="form-control"
                  v-model.number="tarifa.precioReposicion"
                  :class="{ 'is-invalid': errores.precioReposicion }"
                />
              </div>

							<!-- POR DEFECTO -->
              <div class="col-12">
                <span class="fw-medium">{{ t.defaultTariff }}:</span>
                <p v-if="!editando">{{ tarifa.por_defecto ? t.yes : 'No' }}</p>
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
          {{ t.modifyTDATariff }}
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
  getTarifaTDADetalle,
  modificarTarifaTDA,
  eliminarTarifaTDA
} from '@/services/detalleTarifaService'

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter()
const editando = ref(false)

const tarifa = ref({
  id: 0,
  nombre: '',
  precioUAM: 0,
  precioOtros: 0,
  precioReposicion: 0,
	por_defecto: false
})

const errores = ref({
  nombre: false,
  precioUAM: false,
  precioOtros: false,
  precioReposicion: false
})

const tarifaOriginal = ref<any>(null)

function validarFormulario() {
  let valido = true

  errores.value.precioUAM = tarifa.value.precioUAM < 0
  errores.value.precioOtros = tarifa.value.precioOtros < 0
  errores.value.precioReposicion = tarifa.value.precioReposicion < 0

  for (const key in errores.value) {
    if (errores.value[key]) valido = false
  }

  return valido
}

function activarEdicion() {
  tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value))
  Object.keys(errores.value).forEach(k => errores.value[k] = false)
  editando.value = true
}

function cancelarEdicion() {
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
  if (!validarFormulario()) return

  const data = camposModificados()
  if (Object.keys(data).length > 0) {
    await modificarTarifaTDA(tarifa.value.id, data)
    tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value))
    editando.value = false
  }
}

const eliminar = async () => {
  await eliminarTarifaTDA(tarifa.value.id)
  router.back()
}

const volver = () => router.back()

onMounted(async () => {
  const id = parseInt(props.id)
  tarifa.value = await getTarifaTDADetalle(id)
  tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value))
})
</script>
