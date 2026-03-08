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
          @click="eliminar">

          <i class="bi bi-trash me-2"></i>
          {{ t.deleteTariff }}
        </button>

      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, inject, onMounted, type Ref } from 'vue'
import { useRouter } from 'vue-router'

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

const tarifa = ref<any>({})
const tarifaOriginal = ref<any>(null)
const errores = ref<any>({})

function validarFormulario() {
  let valido = true
  for (const key in tarifa.value) {
    if (typeof tarifa.value[key] === 'number' && tarifa.value[key] < 0) {
      errores.value[key] = true
      valido = false
    } else {
      errores.value[key] = false
    }
  }
  return valido
}

function activarEdicion() {
  tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value))
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
    await modificarTarifaFisioterapia(tarifa.value.id, data)
    tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value))
    editando.value = false
  }
}

const eliminar = async () => {
  await eliminarTarifaFisioterapia(tarifa.value.id)
  router.back()
}

const volver = () => router.back()

onMounted(async () => {
  const id = parseInt(props.id)
  tarifa.value = await getTarifaFisioterapiaDetalle(id)
  tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value))
})
</script>
