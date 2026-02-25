<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-5" style="max-width: 1000px;">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-5">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-bold text-center display-5 mb-0">
          <span v-if="!editando">{{ tarifa.titulo }}</span>
          <input
            v-else
            v-model="tarifa.titulo"
            class="form-control form-control-lg text-center fw-semibold"
            :class="{ 'is-invalid': errores.titulo }"
            :placeholder="tarifa.titulo"
          />
        </h1>

        <div style="width: 120px"></div>
      </div>

      <!-- BLOQUES TARIFA -->
      <div class="row g-4">

        <!-- CONSULTA INDIVIDUAL -->
        <div class="col-12 col-md-6">
          <div class="bg-white rounded-4 shadow p-5 h-100">
            <h4 class="mb-4 d-flex align-items-center">
              <i class="bi bi-person-badge text-primary me-2"></i>
              {{ t.initialConsultation }}
            </h4>

            <div class="row g-4">
              <PrecioField
                label="tdaPrice"
                v-model="tarifa.precioConsultaTDA"
                :editando="editando"
                :error="errores.precioConsultaTDA"
                :t="t"
              />
              <PrecioField
                label="uamPrice"
                v-model="tarifa.precioConsultaUAM"
                :editando="editando"
                :error="errores.precioConsultaUAM"
                :t="t"
              />
              <PrecioField
                label="otherPrice"
                v-model="tarifa.precioConsultaOtros"
                :editando="editando"
                :error="errores.precioConsultaOtros"
                :t="t"
              />
            </div>
          </div>
        </div>

        <!-- BONO 1-5 -->
        <div class="col-12 col-md-6">
          <div class="bg-white rounded-4 shadow p-5 h-100">
            <h4 class="mb-4 d-flex align-items-center">
              <i class="bi bi-123 text-success me-2"></i>
              {{ t.sessions1to5 }}
            </h4>

            <div class="row g-4">
              <PrecioField
                label="tdaPrice"
                v-model="tarifa.precioSesiones1_5TDA"
                :editando="editando"
                :error="errores.precioSesiones1_5TDA"
                :t="t"
              />
              <PrecioField
                label="uamPrice"
                v-model="tarifa.precioSesiones1_5UAM"
                :editando="editando"
                :error="errores.precioSesiones1_5UAM"
                :t="t"
              />
              <PrecioField
                label="otherPrice"
                v-model="tarifa.precioSesiones1_5Otros"
                :editando="editando"
                :error="errores.precioSesiones1_5Otros"
                :t="t"
              />
            </div>
          </div>
        </div>

        <!-- BONO 6+ -->
        <div class="col-12 col-md-6 mx-auto">
          <div class="bg-white rounded-4 shadow p-5 h-100">
            <h4 class="mb-4 d-flex align-items-center">
              <i class="bi bi-plus-circle text-warning me-2"></i>
              {{ t.sessions6plus }}
            </h4>

            <div class="row g-4">
              <PrecioField
                label="tdaPrice"
                v-model="tarifa.precioSesiones6TDA"
                :editando="editando"
                :error="errores.precioSesiones6TDA"
                :t="t"
              />
              <PrecioField
                label="uamPrice"
                v-model="tarifa.precioSesiones6UAM"
                :editando="editando"
                :error="errores.precioSesiones6UAM"
                :t="t"
              />
              <PrecioField
                label="otherPrice"
                v-model="tarifa.precioSesiones6Otros"
                :editando="editando"
                :error="errores.precioSesiones6Otros"
                :t="t"
              />
            </div>
          </div>
        </div>

        <!-- POR DEFECTO -->
        <div class="col-12 text-center mt-4">
          <div class="bg-white rounded-4 shadow p-4">
            <span class="fw-medium d-block mb-2">{{ t.defaultTariff }}</span>

            <p v-if="!editando" class="fs-5 fw-semibold">
              {{ tarifa.por_defecto ? t.yes : 'No' }}
            </p>

            <div v-else class="form-check d-inline-flex align-items-center justify-content-center">
              <input
                class="form-check-input me-2"
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

      <!-- ACCIONES -->
      <div class="d-flex justify-content-center gap-4 mt-5">

        <button
          v-if="!editando"
          class="btn btn-primary btn-lg rounded-pill px-5"
          @click="activarEdicion"
        >
          <i class="bi bi-pencil me-2"></i>
          {{ t.modifyTariff }}
        </button>

        <template v-else>
          <button
            class="btn btn-success btn-lg rounded-pill px-5"
            @click="guardarCambios"
          >
            <i class="bi bi-check-lg me-2"></i>
            {{ t.saveChanges }}
          </button>

          <button
            class="btn btn-secondary btn-lg rounded-pill px-5"
            @click="cancelarEdicion"
          >
            {{ t.cancel }}
          </button>
        </template>

        <button
          v-if="!editando"
          class="btn btn-danger btn-lg rounded-pill px-5"
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
