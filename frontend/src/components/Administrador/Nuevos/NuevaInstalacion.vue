<template>
  <div class="min-vh-100 bg-light pb-5">
    <main class="container py-5">
      <h1 class="text-center fw-bold mb-5">
        {{ t.newFacility }}
      </h1>

      <div class="card shadow-sm border-0 rounded-4 p-4">
        <div class="row g-4">

          <!-- NOMBRE -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.name }}</label>
            <input
              type="text"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.nombre }"
              v-model="instalacion.nombre"
            />
          </div>

          <!-- TIPO INSTALACIÓN -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.facilityType }}</label>
            <select
              class="form-select form-select-lg"
              :class="{ 'is-invalid': errores.tipoInstalacion }"
              v-model="instalacion.tipoInstalacion"
            >
              <option value="" disabled>--</option>
              <option
                v-for="t in tiposStore.tiposInstalacion"
                :key="t"
                :value="t"
              >
                {{ t }}
              </option>
            </select>
          </div>

          <!-- PABELLÓN -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.pavilion }}</label>
            <select
              class="form-select form-select-lg"
              :class="{ 'is-invalid': errores.pabellon }"
              v-model="instalacion.pabellon"
            >
              <option value="" disabled>--</option>
              <option
                v-for="p in pabellones"
                :key="p.id"
                :value="p.id"
              >
                {{ p.nombre }}
              </option>
            </select>
          </div>

          <!-- TARIFA -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.tariff }}</label>
            <select
              class="form-select form-select-lg"
              v-model="instalacion.tarifa"
            >
              <option value="">--</option>
              <option
                v-for="t in tarifas"
                :key="t.id"
                :value="t.id"
              >
                {{ t.nombre }}
              </option>
            </select>
          </div>

          <!-- AFORO -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.maxCapacity }}</label>
            <input
              type="number"
              min="1"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.aforoMaximo }"
              v-model.number="instalacion.aforoMaximo"
            />
          </div>

          <!-- PORCENTAJE TDA -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.tdaPercent }}</label>
            <input
              type="number"
              min="0"
              max="100"
              step="0.1"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.porcentajeTDA }"
              v-model.number="instalacion.porcentajeTDA"
            />
          </div>

          <!-- LUZ -->
          <div class="col-md-4 d-flex align-items-end">
            <div class="form-check form-switch">
              <input
                class="form-check-input"
                type="checkbox"
                v-model="instalacion.luz"
              />
              <label class="form-check-label fw-semibold">
                {{ t.light }}
              </label>
            </div>
          </div>

          <!-- IMAGEN -->
          <div class="col-md-12">
            <label class="form-label fw-semibold">{{ t.images }}</label>
            <input
              type="text"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.imagenURL }"
              v-model="instalacion.imagenURL"
              placeholder="https://@."
            />
          </div>

        </div>

        <p v-if="mensaje" class="text-center text-danger mt-4">
          {{ mensaje }}
        </p>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-5">
          <button
            class="btn btn-primary btn-lg px-5"
            @click="crearInstalacion"
          >
            {{ t.createFacility }}
          </button>

          <button
            class="btn btn-danger btn-lg px-5"
            @click="volver"
          >
            {{ t.return }}
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, inject, type Ref, onMounted } from "vue"
import { useRouter } from "vue-router"

import { nuevaInstalacion } from "@/services/crearRecursos"
import { getPabellonesSimples, getTarifasInstalacion } from "@/services/listadoService"

import { useTiposStore } from "@/stores/tipos"

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const router = useRouter()

const tiposStore = useTiposStore();

const instalacion = ref({
  nombre: "",
  imagenURL: "",
  aforoMaximo: 50,
  luz: false,
  porcentajeTDA: 0,
  pabellon: "",
  tarifa: "",
  tipoInstalacion: ""
})

const errores = ref({
  nombre: false,
  imagenURL: false,
  aforoMaximo: false,
  porcentajeTDA: false,
  pabellon: false,
  tipoInstalacion: false
})

const mensaje = ref("")

const pabellones = ref<any[]>([])
const tarifas = ref<any[]>([])

function validarFormulario() {
  let valido = true

  errores.value.nombre = instalacion.value.nombre === ""
  errores.value.imagenURL = instalacion.value.imagenURL === ""
  errores.value.aforoMaximo = instalacion.value.aforoMaximo <= 0
  errores.value.porcentajeTDA =
    instalacion.value.porcentajeTDA < 0 ||
    instalacion.value.porcentajeTDA > 100
  errores.value.pabellon = instalacion.value.pabellon === ""
  errores.value.tipoInstalacion = instalacion.value.tipoInstalacion === ""

  for (const k in errores.value) {
    if (errores.value[k]) valido = false
  }

  return valido
}

const crearInstalacion = async () => {
  if (!validarFormulario()) return

  try {
    await nuevaInstalacion(instalacion.value)
    router.back()
  } catch(e) {
    console.log("Error al crear la instalacion", e)
  }
}

const volver = () => router.back()

onMounted(async () => {
  pabellones.value = await getPabellonesSimples()
  tarifas.value = await getTarifasInstalacion()
})
</script>
