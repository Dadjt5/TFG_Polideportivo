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
            <input type="text" class="form-control form-control-lg" :class="{ 'is-invalid': errores.nombre }"
              v-model="instalacion.nombre" />
          </div>

          <!-- TIPO INSTALACIÓN -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.facilityType }}</label>
            <select class="form-select form-select-lg" :class="{ 'is-invalid': errores.tipoInstalacion }"
              v-model="instalacion.tipoInstalacion">
              <option value="" disabled>--</option>
              <option v-for="t in tiposStore.tiposInstalacion" :key="t[0]" :value="t[0]">
                {{ t[1] }}
              </option>
            </select>
          </div>

          <!-- PABELLÓN -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.pavilion }}</label>
            <select class="form-select form-select-lg" :class="{ 'is-invalid': errores.pabellon }"
              v-model="instalacion.pabellon_id">
              <option value="" disabled>--</option>
              <option v-for="p in pabellones" :key="p.id" :value="p.id">
                {{ p.nombre }}
              </option>
            </select>
          </div>

          <!-- TARIFA -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.tariff }}</label>
            <select class="form-select form-select-lg" v-model="instalacion.tarifa">
              <option value="">--</option>
              <option v-for="t in tarifas" :key="t.id" :value="t.id">
                {{ t.titulo }}
              </option>
            </select>
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
            <input type="text" class="form-control form-control-lg" :class="{ 'is-invalid': errores.imagenURL }"
              v-model="instalacion.imagenURL" placeholder="https://@." />
          </div>

        </div>

        <!-- Horarios semanales -->
        <div class="card border-0 shadow-sm rounded-4 mt-4">
          <div class="card-body d-flex justify-content-between align-items-center cursor-pointer"
            style="cursor: pointer;" @click="openAgenda = !openAgenda">
            <div class="d-flex align-items-center gap-2">
              <i class="bi bi-calendar-event fs-5 text-primary"></i>
              <span class="fw-semibold">
                {{ t.weeklyHours }}
              </span>
            </div>

            <i class="bi" :class="openAgenda ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
          </div>
          <transition name="fade">
            <div v-if="openAgenda" class="px-4 pb-4">
              <div v-for="(d, index) in agenda" :key="index" class="d-flex align-items-center gap-3 mb-3">

                <!-- Día -->
                <span class="w-25 fw-semibold">
                  {{ d.dia }}
                </span>

                <!-- Si NO está cerrado -->
                <template v-if="d.abierto">
                  <input type="time" v-model="d.apertura" class="form-control form-control-sm w-auto" />

                  <span>-</span>

                  <input type="time" v-model="d.cierre" class="form-control form-control-sm w-auto" />
                </template>

                <!-- Texto cuando está cerrado -->
                <span v-else class="text-danger fw-semibold">
                  {{ t.close }}
                </span>

                <!-- Checkbox -->
                <div class="form-check ms-auto">
                  <input class="form-check-input" type="checkbox" v-model="d.abierto" :id="'abierto-' + index">
                  <label class="form-check-label small" :for="'abierto-' + index">
                    {{ t.open }}
                  </label>
                </div>

              </div>
            </div>
          </transition>
        </div>

        <!-- Fechas especiales -->
        <div class="card border-0 shadow-sm rounded-4 mt-4">
          <div class="card-body d-flex justify-content-between align-items-center cursor-pointer"
            style="cursor: pointer;" @click="openEspeciales = !openEspeciales">
            <div class="d-flex align-items-center gap-2">
              <i class="bi bi-calendar-event fs-5 text-primary"></i>
              <span class="fw-semibold">
                {{ t.specialDates }}
              </span>
            </div>

            <i class="bi" :class="openEspeciales ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
          </div>

          <transition name="fade">
            <div v-if="openEspeciales" class="px-4 pb-4">

              <div class="mb-3">
                <input type="date" v-model="tempFecha" class="form-control mb-2" />
                <div class="form-check mb-2">
                  <input type="checkbox" class="form-check-input" v-model="tempAbierto" id="abiertoCheck" />
                  <label for="abiertoCheck" class="form-check-label">{{ t.open }}</label>
                </div>
                <div v-if="tempAbierto" class="d-flex gap-2 mb-2">
                  <input type="time" v-model="tempApertura" class="form-control form-control-sm" />
                  <span>-</span>
                  <input type="time" v-model="tempCierre" class="form-control form-control-sm" />
                </div>
                <button class="btn btn-success btn-sm" @click="handleAddFechaEspecial">{{ t.newSpecialDate }}</button>
              </div>

              <div v-for="(f, index) in fechasEspeciales" :key="index"
                class="d-flex justify-content-between align-items-center mb-1 p-2 border rounded">
                <div>
                  <strong>{{ f.fecha }}</strong> -
                  <span v-if="f.abierto">{{ f.apertura }} a {{ f.cierre }}</span>
                  <span v-else>{{ t.close }}</span>
                </div>
                <button class="btn btn-danger btn-sm" @click="handleDeleteFechaEspecial(index)">{{ t.delete }}</button>
              </div>
            </div>
          </transition>
        </div>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-5">
          <button class="btn btn-primary btn-lg px-5" @click="crearInstalacion">
            {{ t.createFacility }}
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

const instalacion = ref({
  nombre: "",
  imagenURL: "",
  aforoMaximo: 50,
  luz: false,
  porcentajeTDA: 0,
  pabellon_id: null,
  tarifa: null,
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

const diasSemana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"];
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

const openAgenda = ref(false);
const openEspeciales = ref(false);

const pabellones = ref<any[]>([])
const tarifas = ref<any[]>([])

function handleAgendaChange(index: number, field: "apertura" | "cierre", value: string) {
  agenda.value[index][field] = value;
}

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
  errores.value.imagenURL = instalacion.value.imagenURL === ""
  errores.value.aforoMaximo = instalacion.value.aforoMaximo <= 0
  errores.value.porcentajeTDA =
    instalacion.value.porcentajeTDA < 0 ||
    instalacion.value.porcentajeTDA > 100
  errores.value.pabellon = instalacion.value.pabellon_id === ""
  errores.value.tipoInstalacion = instalacion.value.tipoInstalacion === ""

  for (const k in errores.value) {
    if (errores.value[k]) valido = false
  }

  return valido
}

const crearInstalacion = async () => {
  mensaje.value = ""
  if (!validarFormulario()) {
    mensaje.value = t.value.emptyFields
    return
  }

  try {
    await nuevaInstalacion(
      instalacion.value,
      agenda.value,
      fechasEspeciales.value
    )

    router.push({ name: 'gestion-espacios' })
  } catch (e: any) {
    mensaje.value = e.response?.data?.respuesta
    console.log("Error al crear la instalacion", e)
  }
}

const volver = () => router.back()

onMounted(async () => {
  pabellones.value = await getPabellonesSimples()
  tarifas.value = await getTarifasInstalacion()
})
</script>
