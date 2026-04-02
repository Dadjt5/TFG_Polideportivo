<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #fff4e0, #e0f7ff);">
    <main class="container py-5" style="max-width: 1120px;">
      <h1 class="text-center fw-bold mb-5 text-primary">
        {{ t.newFacility }}
      </h1>

      <div class="card shadow-lg border-0 rounded-4 p-4"
        style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">

        <!-- TABS -->
        <ul class="nav nav-tabs nav-fill mb-4">
          <li class="nav-item">
            <button type="button" class="nav-link" :class="{ active: tab === 1 }" @click="tab = 1">
              {{ t.data }}
            </button>
          </li>

          <li class="nav-item">
            <button type="button" class="nav-link" :class="{ active: tab === 2 }" @click="tab = 2">
              {{ t.pavilion }} & {{ t.tariff }}
            </button>
          </li>

          <li class="nav-item">
            <button type="button" class="nav-link" :class="{ active: tab === 3 }" @click="tab = 3">
              {{ t.weeklyHours }}
            </button>
          </li>
        </ul>

        <!-- ================= TAB 1 DATOS ================= -->
        <div v-if="tab === 1" class="row g-4">

          <!-- NOMBRE -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.name }}</label>
            <input type="text" class="form-control form-control-lg" :class="{ 'is-invalid': errores.nombre }"
              v-model="instalacion.nombre" />
          </div>

          <!-- TIPO INSTALACIÓN -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.facilityType }}</label>
            <select class="form-select form-select-lg" :class="{ 'is-invalid': errores.tipoInstalacion }"
              v-model="instalacion.tipoInstalacion">
              <option value="" disabled>--</option>
              <option v-for="t in tiposStore.tiposInstalacion" :key="t" :value="t">
                {{ t }}
              </option>
            </select>
          </div>

          <!-- NÚMERO DE CALLES (solo piscina) -->
          <div class="col-md-4" v-if="instalacion.tipoInstalacion === 'Piscina'">
            <label class="form-label fw-semibold">{{ t.poolStreets }}</label>

            <input type="number" min="1" class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.numeroCalles }" v-model.number="instalacion.numeroCalles" />
          </div>

          <!-- AFORO -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.maxCapacity }}</label>
            <input type="number" min="1" class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.aforoMaximo }" v-model.number="instalacion.aforoMaximo" />
          </div>

          <!-- PORCENTAJE TDA -->
          <div class="col-md-4">
            <label class="form-label fw-semibold">{{ t.tdaPercent }}</label>
            <input type="number" min="0" max="100" step="0.1" class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.porcentajeTDA }" v-model.number="instalacion.porcentajeTDA" />
          </div>

          <!-- LUZ -->
          <div class="col-md-4 d-flex align-items-end">
            <div class="form-check form-switch">
              <input class="form-check-input" type="checkbox" v-model="instalacion.luz" />
              <label class="form-check-label fw-semibold">
                {{ t.light }}
              </label>
            </div>
          </div>

          <!-- IMAGEN -->
          <div class="col-md-12">
            <label class="form-label fw-semibold">{{ t.images }}</label>

            <input type="file" class="form-control form-control-lg"
              accept="image/*" @change="onFileChange" />

            <!-- preview -->
            <img v-if="preview" :src="preview" class="mt-3 rounded" style="max-width:250px" />
          </div>

        </div>

        <!-- ================= TAB 2 PABELLON Y TARIFA ================= -->
        <div v-if="tab === 2" class="row g-4">

          <!-- PABELLÓN -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.pavilion }}</label>
            <select class="form-select form-select-lg" :class="{ 'is-invalid': errores.pabellon }"
              v-model="instalacion.pabellon">
              <option value="" disabled>--</option>
              <option v-for="p in pabellones" :key="p.id" :value="p.id">
                {{ p.nombre }}
              </option>
            </select>
          </div>

          <!-- TARIFA -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.tariff }}</label>
            <select class="form-select form-select-lg" v-model="instalacion.tarifa"
              :class="{ 'is-invalid': errores.tarifa }">
              <option value="">--</option>
              <option v-for="t in tarifas" :key="t.id" :value="t.id">
                {{ t.titulo }}
              </option>
            </select>
          </div>

        </div>

        <!-- ================= TAB 3 HORARIOS ================= -->
        <div v-if="tab === 3">

          <!-- HORARIOS SEMANALES -->
          <div class="card border-0 shadow-sm rounded-4 mb-4">
            <div class="card-body">
              <h5 class="fw-bold mb-4">
                {{ t.weeklyHours }}
              </h5>

              <div v-for="(d, index) in agenda" :key="index" class="d-flex align-items-center gap-3 mb-3">

                <span class="w-25 fw-semibold">
                  {{ d.dia }}
                </span>

                <template v-if="d.abierto">
                  <input type="time" v-model="d.apertura" class="form-control form-control-sm w-auto" />

                  <span>-</span>

                  <input type="time" v-model="d.cierre" class="form-control form-control-sm w-auto" />
                </template>

                <span v-else class="text-danger fw-semibold">
                  {{ t.close }}
                </span>

                <div class="form-check ms-auto">
                  <input class="form-check-input" type="checkbox" v-model="d.abierto">
                </div>
              </div>
            </div>
          </div>

          <!-- FECHAS ESPECIALES -->
          <div class="card border-0 shadow-sm rounded-4">
            <div class="card-body">
              <h5 class="fw-bold mb-4">
                {{ t.specialDates }}
              </h5>

              <input type="date" v-model="tempFecha" class="form-control mb-2" />

              <div class="form-check mb-2">
                <input type="checkbox" class="form-check-input" v-model="tempAbierto" />
                <label class="form-check-label">
                  {{ t.open }}
                </label>
              </div>

              <div v-if="tempAbierto" class="d-flex gap-2 mb-3">
                <input type="time" v-model="tempApertura" class="form-control form-control-sm" />
                <span>-</span>
                <input type="time" v-model="tempCierre" class="form-control form-control-sm" />
              </div>

              <button class="btn btn-success btn-sm mb-3" @click="handleAddFechaEspecial">
                {{ t.newSpecialDate }}
              </button>

              <div v-for="(f, index) in fechasEspeciales" :key="index"
                class="d-flex justify-content-between align-items-center mb-2 p-2 border rounded">

                <div>
                  <strong>{{ f.fecha }}</strong> -
                  <span v-if="f.abierto">
                    {{ f.apertura }} - {{ f.cierre }}
                  </span>
                  <span v-else>
                    {{ t.close }}
                  </span>
                </div>

                <button class="btn btn-danger btn-sm" @click="handleDeleteFechaEspecial(index)">
                  {{ t.delete }}
                </button>
              </div>

            </div>
          </div>

        </div>

        <div v-if="mostrarMensaje" class="text-center mt-3 mb-3">
          <div class="alert" :class="tipoMensaje === 'success' ? 'alert-success' : 'alert-danger'">
            {{ mensajeEditar }}
          </div>
        </div>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-4">
          <button class="btn btn-success btn-lg px-5 rounded-pill shadow-sm" @click="crearInstalacion">
            {{ t.createFacility }}
          </button>
          <button class="btn btn-outline-secondary btn-lg px-5 rounded-pill shadow-sm" @click="volver">
            {{ t.return }}
          </button>
        </div>

      </div>
    </main>
  </div>
</template>


<script setup lang="ts">
import { ref, inject, type Ref, onMounted, watch } from "vue"
import { useRouter } from "vue-router"

import { nuevaInstalacion } from "@/services/crearRecursosService"
import { getPabellonesSimples, getTarifasInstalacion } from "@/services/listadoService"

import { useTiposStore } from "@/stores/tipos"

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const router = useRouter()

const tiposStore = useTiposStore();
const mensaje = ref("")
const mensajeEditar = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)

const tab = ref(1)

const instalacion = ref({
  nombre: "",
  aforoMaximo: 50,
  luz: false,
  porcentajeTDA: 0,
  tarifa: null,
  pabellon: null,
  tipoInstalacion: "",
  numeroCalles: 0
})

const errores = ref({
  nombre: false,
  aforoMaximo: false,
  porcentajeTDA: false,
  pabellon: false,
  tarifa: false,
  tipoInstalacion: false,
  numeroCalles: false
})

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensajeEditar.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true

  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
}

const diasSemana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"];
const agenda = ref(diasSemana.map(d => ({
  dia: d,
  apertura: "08:00",
  cierre: "22:00",
  abierto: true
})));

const fechasEspeciales = ref<{ fecha: string; abierto: boolean; apertura: string; cierre: string }[]>([]);
const tempFecha = ref("");
const tempAbierto = ref(false);
const tempApertura = ref("08:00");
const tempCierre = ref("22:00");

const imagen = ref<File | null>(null)
const preview = ref<string | null>(null)
const pabellones = ref<any[]>([])
const tarifas = ref<any[]>([])


function handleAddFechaEspecial() {
  if (!tempFecha.value) return;
  fechasEspeciales.value.push({
    fecha: tempFecha.value,
    abierto: tempAbierto.value,
    apertura: tempApertura.value,
    cierre: tempCierre.value
  });
  tempFecha.value = "";
  tempAbierto.value = false;
  tempApertura.value = "08:00";
  tempCierre.value = "22:00";
}

function handleDeleteFechaEspecial(index: number) {
  fechasEspeciales.value.splice(index, 1);
}

function validarFormulario() {
  let valido = true

  errores.value.nombre = instalacion.value.nombre === ""
  errores.value.aforoMaximo = instalacion.value.aforoMaximo <= 0
  errores.value.porcentajeTDA =
    instalacion.value.porcentajeTDA < 0 ||
    instalacion.value.porcentajeTDA > 100
  errores.value.pabellon = instalacion.value.pabellon === null
  errores.value.tarifa = instalacion.value.tarifa === null
  errores.value.tipoInstalacion = instalacion.value.tipoInstalacion === ""
  errores.value.numeroCalles =
    instalacion.value.numeroCalles <= 0 &&
    instalacion.value.tipoInstalacion === "Piscina"

  for (const k in errores.value) {
    if (errores.value[k]) valido = false
  }

  return valido
}

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  if (!input.files || input.files.length === 0) return

  imagen.value = input.files[0]
  preview.value = URL.createObjectURL(imagen.value)
}

const crearInstalacion = async () => {
  if (!validarFormulario()) {
    lanzarMensaje(t.value.missing, "error")
    return
  }

  const formData = new FormData()

  formData.append("instalacion", JSON.stringify(instalacion.value))
  formData.append("agenda", JSON.stringify(agenda.value))
  formData.append("fechasEspeciales", JSON.stringify(fechasEspeciales.value))

  if (imagen.value) {
    formData.append("imagenURL", imagen.value)
  }

  try {
    await nuevaInstalacion(formData)
    router.push({ name: 'gestion-espacios' })
  } catch (e) {
    lanzarMensaje(t.value.facilityNoCreated, "error")
    console.log("Error al crear la instalacion", e)
  }
}

const volver = () => router.back()

watch(
  () => instalacion.value.tipoInstalacion,
  (tipo) => {
    if (tipo !== "Piscina") {
      instalacion.value.numeroCalles = 0
    }
  }
)

onMounted(async () => {
  pabellones.value = await getPabellonesSimples()
  tarifas.value = await getTarifasInstalacion()
})
</script>
