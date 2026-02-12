<template>
  <div class="min-vh-100 bg-light pb-5">
    <main class="container py-5">
      <h1 class="text-center fw-bold mb-5">
        {{ t.newActivity }}
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
              v-model="actividad.nombre"
            />
          </div>

          <!-- AÑO -->
          <div class="col-md-3">
            <label class="form-label fw-semibold">{{ t.academicYear }}</label>
            <input
              type="number"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.año }"
              v-model.number="actividad.año"
            />
          </div>

          <!-- ESTADO -->
          <div class="col-md-3">
            <label class="form-label fw-semibold">{{ t.status }}</label>
            <select
              class="form-select form-select-lg"
              :class="{ 'is-invalid': errores.estado }"
              v-model="actividad.estado"
            >
              <option disabled value="">--</option>
              <option v-for="e in tiposStore.estados" :key="e" :value="e">{{ e }}</option>
            </select>
          </div>

          <!-- DESCRIPCIÓN -->
          <div class="col-md-12">
            <label class="form-label fw-semibold">{{ t.description }}</label>
            <textarea
              rows="3"
              class="form-control form-control-lg"
              v-model="actividad.descripcion"
            />
          </div>

          <!-- IMAGEN -->
          <div class="col-md-12">
            <label class="form-label fw-semibold">{{ t.images }}</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="actividad.imagenURL"
              placeholder="https://@."
            />
          </div>

          <!-- PLAZAS -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.maxPlaces }}</label>
            <input
              type="number"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.plazasMaximas }"
              v-model.number="actividad.plazasMaximas"
            />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.reservedPlaces }}</label>
            <input
              type="number"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.plazasReservadas }"
              v-model.number="actividad.plazasReservadas"
            />
          </div>

          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.minimumAge }}</label>
            <input
              type="number"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.edadMinima }"
              v-model.number="actividad.edadMinima"
            />
          </div>

          <!-- CRÉDITOS -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.credits }}</label>
            <input
              type="number"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.numeroCreditos }"
              v-model.number="actividad.numeroCreditos"
            />
          </div>

          <!-- NIVEL -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.level }}</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="actividad.nivel"
            />
          </div>

          <!-- MATERIAL -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.material }}</label>
            <input
              type="text"
              class="form-control form-control-lg"
              v-model="actividad.material"
            />
          </div>

          <!-- INSTALACIÓN -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.facility }}</label>
            <select
              class="form-select form-select-lg"
              :class="{ 'is-invalid': errores.instalacion }"
              v-model="actividad.instalacion"
            >
              <option disabled value="">--</option>
              <option v-for="i in instalaciones" :key="i.id" :value="i.id">
                {{ i.nombre }}
              </option>
            </select>
          </div>

          <!-- MONITOR -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.monitorName }}</label>
            <select
              class="form-select form-select-lg"
              v-model="actividad.monitor"
            >
              <option disabled value="">--</option>
              <option v-for="m in monitores" :key="m.id" :value="m.id">
                {{ m.nombre }}
              </option>
            </select>
          </div>

          <!-- TIPO ACTIVIDAD -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.activityType }}</label>
            <select
              class="form-select form-select-lg"
              :class="{ 'is-invalid': errores.tipoActividad }"
              v-model="actividad.tipoActividad"
            >
              <option v-for="t in tiposStore.tiposActividad" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>

          <!-- RESERVA -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.reserveType }}</label>
            <select
              class="form-select form-select-lg"
              :class="{ 'is-invalid': errores.tipoReserva }"
              v-model="actividad.tipoReserva"
            >
              <option v-for="r in tiposStore.tiposReserva" :key="r" :value="r">{{ r }}</option>
            </select>
          </div>

          <!-- TERRENO -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.terrainType }}</label>
            <select
              class="form-select form-select-lg"
              :class="{ 'is-invalid': errores.terreno }"
              v-model="actividad.terreno"
            >
              <option v-for="t in tiposStore.terrenos" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>

          <!-- EXTERIOR -->
          <div class="col-md-12">
            <div class="form-check form-switch mt-2">
              <input
                class="form-check-input"
                type="checkbox"
                v-model="actividad.exterior"
              />
              <label class="form-check-label fw-semibold">
                {{ t.outdoor }}
              </label>
            </div>
          </div>
        </div>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-5">
          <button class="btn btn-primary btn-lg px-5" @click="crearActividad">
            {{ t.createActivity }}
          </button>

          <button class="btn btn-danger btn-lg px-5" @click="volver">
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

import { nuevaActividad } from "@/services/crearRecursosService"
import { getInstalacionesSimples, getMonitoresSimples } from "@/services/listadoService"

import { useTiposStore } from "@/stores/tipos"

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const tiposStore = useTiposStore();

const router = useRouter()
const añoActual = new Date().getFullYear()

const actividad = ref({
  nombre: "",
  descripcion: "",
  imagenURL: "",
  edadMinima: 18,
  plazasMaximas: 50,
  plazasReservadas: 0,
  año: añoActual,
  numeroCreditos: 0,
  nivel: "",
  material: "",
  exterior: false,
  instalacion: "",
  monitor: "",
  tipoActividad: "",
  tipoReserva: "",
  terreno: "",
  estado: "",
  periodo: "ANUAL"
})

const errores = ref({
  nombre: false,
  plazasMaximas: false,
  plazasReservadas: false,
  edadMinima: false,
  año: false,
  numeroCreditos: false,
  tipoActividad: false,
  tipoReserva: false,
  terreno: false,
  estado: false,
  instalacion: false
})

const instalaciones = ref<any[]>([])
const monitores = ref<any[]>([])

function validarFormulario() {
  let ok = true

  errores.value.nombre = actividad.value.nombre === ""
  errores.value.plazasMaximas = actividad.value.plazasMaximas <= 0
  errores.value.plazasReservadas =
    actividad.value.plazasReservadas < 0 ||
    actividad.value.plazasReservadas > actividad.value.plazasMaximas
  errores.value.edadMinima = actividad.value.edadMinima <= 0
  errores.value.año = actividad.value.año < añoActual
  errores.value.numeroCreditos = actividad.value.numeroCreditos < 0
  errores.value.tipoActividad = actividad.value.tipoActividad === ""
  errores.value.tipoReserva = actividad.value.tipoReserva === ""
  errores.value.terreno = actividad.value.terreno === ""
  errores.value.estado = actividad.value.estado === ""
  errores.value.instalacion = actividad.value.instalacion === ""

  for (const k in errores.value) {
    if (errores.value[k]) ok = false
  }

  return ok
}

const crearActividad = async () => {
  if (!validarFormulario()) return

  try {
    await nuevaActividad(actividad.value)
    router.back()
  } catch(e) {
    console.log("Error al crear la actividad", e)
  }
}

const volver = () => router.back()

onMounted(async () => {
  instalaciones.value = await getInstalacionesSimples()
  monitores.value = await getMonitoresSimples()
})
</script>
