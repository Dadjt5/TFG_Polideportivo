<template>
  <div class="min-vh-100 pt-4" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4" style="max-width: 1600px;">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold mb-0 text-primary">{{ instalacion.nombre }}</h1>

        <div style="width: 100px"></div>
      </div>

      <!-- CARD PRINCIPAL -->
      <div class="card shadow-lg border-0 rounded-4 p-4 mb-4"
        style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">

        <!-- NAV DE TABS -->
        <ul class="nav nav-pills nav-fill mb-4">
          <li class="nav-item">
            <button class="nav-link active fw-bold" data-bs-toggle="pill" data-bs-target="#info">
              {{ t.facilityDetails }}
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link fw-bold" data-bs-toggle="pill" data-bs-target="#horario">
              {{ t.timetable }}
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link fw-bold" data-bs-toggle="pill" data-bs-target="#especiales">
              {{ t.specialDates }}
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link fw-bold" data-bs-toggle="pill" data-bs-target="#imagenes">
              {{ t.images }}
            </button>
          </li>
        </ul>

        <!-- CONTENIDO DE TABS -->
        <div class="tab-content">

          <!-- TAB 1: INFO -->
          <div class="tab-pane fade show active" id="info">
            <div class="row g-4">
              <div class="col-md-6">
                <label class="form-label fw-semibold">{{ t.name }}</label>
                <input v-if="editando" type="text" class="form-control form-control-lg" v-model="instalacion.nombre"
                  :class="{ 'is-invalid': errores.nombre }" />
                <div v-else class="form-control form-control-lg bg-light text-muted">{{ instalacion.nombre }}</div>
              </div>

              <div class="col-md-6">
                <label class="form-label fw-semibold">{{ t.facilityType }}</label>
                <select v-if="editando" class="form-select form-select-lg" v-model="instalacion.tipoInstalacion"
                  :class="{ 'is-invalid': errores.tipoInstalacion }">
                  <option value="" disabled>--</option>
                  <option v-for="t in tiposStore.tiposInstalacion" :key="t" :value="t">{{ t }}</option>
                </select>
                <div v-else class="form-control form-control-lg bg-light text-muted">{{ instalacion.tipoInstalacion ||
                  '---' }}</div>
              </div>

              <div class="col-md-4" v-if="instalacion.tipoInstalacion === 'Piscina'">
                <label class="form-label fw-semibold">{{ t.poolStreets }}</label>
                <input v-if="editando" type="number" min="1" class="form-control form-control-lg"
                  v-model.number="instalacion.numeroCalles" :class="{ 'is-invalid': errores.numeroCalles }" />
                <div v-else class="form-control form-control-lg bg-light text-muted">{{ instalacion.numeroCalles }}
                </div>
              </div>

              <div class="col-md-4">
                <label class="form-label fw-semibold">{{ t.capacity }}</label>
                <input v-if="editando" type="number" min="1" class="form-control form-control-lg"
                  v-model.number="instalacion.aforoMaximo" :class="{ 'is-invalid': errores.aforoMaximo }" />
                <div v-else class="form-control form-control-lg bg-light text-muted">{{ instalacion.aforoMaximo }}</div>
              </div>

              <div class="col-md-4">
                <label class="form-label fw-semibold">TDA (%)</label>
                <input v-if="editando" type="number" min="0" max="100" step="0.1" class="form-control form-control-lg"
                  v-model.number="instalacion.porcentajeTDA" :class="{ 'is-invalid': errores.porcentajeTDA }" />
                <div v-else class="form-control form-control-lg bg-light text-muted">{{ instalacion.porcentajeTDA }}%
                </div>
              </div>

              <div class="col-md-6">
                <label class="form-label fw-semibold">{{ t.pavilion || 'Pabellón' }}</label>
                <select v-if="editando" class="form-select form-select-lg" v-model="instalacion.pabellon.id"
                  :class="{ 'is-invalid': errores.pabellon }">
                  <option value="-1" disabled>--</option>
                  <option v-for="p in pabellones" :key="p.id" :value="p.id">{{ p.nombre }}</option>
                </select>
                <div v-else class="form-control form-control-lg bg-light text-muted">{{ instalacion.pabellon?.nombre ||
                  '---' }}</div>
              </div>

              <div class="col-md-6">
                <label class="form-label fw-semibold">{{ t.tariff || 'Tarifa' }}</label>

                <select v-if="editando" class="form-select form-select-lg" v-model="instalacion.tarifa"
                  :class="{ 'is-invalid': errores.tarifa }">
                  <option :value="null">--</option>
                  <option v-for="tar in tarifas" :key="tar.id" :value="tar.id">
                    {{ tar.titulo }}
                  </option>
                </select>

                <div v-else class="form-control form-control-lg bg-light text-muted">
                  {{tarifas.find(t => t.id === instalacion.tarifa)?.titulo || '---'}}
                </div>
              </div>

              <div class="col-md-12 d-flex align-items-center mt-4">
                <div class="form-check form-switch fs-5">
                  <input class="form-check-input" type="checkbox" v-model="instalacion.luz" :disabled="!editando" />
                  <label class="form-check-label fw-semibold ms-2">{{ t.light }}</label>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB 2: HORARIO -->
          <div class="tab-pane fade" id="horario">
            <div class="row g-3">
              <div class="col-md-6 col-lg-4" v-for="dia in agenda" :key="dia.dia">
                <div class="card border-1 border-light shadow-sm rounded-4 h-100" :class="{ 'bg-light': !editando }">
                  <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                      <strong class="fs-5">{{ dia.dia }}</strong>
                      <div class="form-check form-switch" v-if="editando">
                        <input class="form-check-input" type="checkbox" v-model="dia.abierto" />
                      </div>
                      <span v-else class="badge" :class="dia.abierto ? 'bg-success' : 'bg-danger'">
                        {{ dia.abierto ? 'Abierto' : 'Cerrado' }}
                      </span>
                    </div>

                    <div v-if="dia.abierto">
                      <div v-if="editando" class="row g-2">
                        <div class="col-6">
                          <label class="small text-muted fw-bold">{{ t.openHour }}</label>
                          <input type="time" class="form-control form-control-sm" v-model="dia.horaApertura" />
                        </div>
                        <div class="col-6">
                          <label class="small text-muted fw-bold">{{ t.closeHour }}</label>
                          <input type="time" class="form-control form-control-sm" v-model="dia.horaCierre" />
                        </div>
                      </div>
                      <div v-else
                        class="d-flex align-items-center justify-content-center gap-2 py-2 bg-white rounded border">
                        <span class="fw-semibold text-primary">{{ dia.horaApertura?.slice(0, 5) }}</span>
                        <span class="text-muted">-</span>
                        <span class="fw-semibold text-primary">{{ dia.horaCierre?.slice(0, 5) }}</span>
                      </div>
                    </div>

                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB 3: FECHAS ESPECIALES -->
          <div class="tab-pane fade" id="especiales">
            <div v-if="editando" class="mb-4">
              <button class="btn btn-primary rounded-pill px-4 shadow-sm"
                @click="fechasEspeciales.push({ fecha: '', horaApertura: '08:00', horaCierre: '22:00', abierto: true })">
                <i class="bi bi-plus-circle me-2"></i> + {{ t.newSpecialDate }}
              </button>
            </div>

            <div v-if="fechasEspeciales?.length" class="row g-3">
              <div class="col-md-6 col-lg-4" v-for="(fecha, index) in fechasEspeciales" :key="index">
                <div class="card border-1 border-light shadow-sm rounded-4 p-3" :class="{ 'bg-light': !editando }">
                  <div class="d-flex justify-content-between align-items-center mb-3">
                    <div v-if="editando" class="w-75">
                      <input type="date" class="form-control" v-model="fecha.fecha" />
                    </div>
                    <div v-else class="fw-bold fs-5 text-dark">{{ fecha.fecha }}</div>
                    <button v-if="editando" class="btn btn-sm btn-outline-danger"
                      @click="fechasEspeciales.splice(index, 1)">✕</button>
                  </div>
                  <div class="mb-3">
                    <div v-if="editando" class="form-check form-switch">
                      <input class="form-check-input" type="checkbox" v-model="fecha.abierto" />
                      <label class="form-check-label fw-medium ms-1">{{ t.open }}</label>
                    </div>
                    <span v-else class="badge" :class="fecha.abierto ? 'bg-success' : 'bg-danger'">{{ fecha.abierto ?
                      'Abierto' : 'Cerrado' }}</span>
                  </div>
                  <div v-if="fecha.abierto">
                    <div v-if="editando" class="row g-2">
                      <div class="col-6">
                        <label class="small text-muted fw-bold">{{ t.openHour }}</label>
                        <input type="time" class="form-control form-control-sm" v-model="fecha.horaApertura" />
                      </div>
                      <div class="col-6">
                        <label class="small text-muted fw-bold">{{ t.closeHour }}</label>
                        <input type="time" class="form-control form-control-sm" v-model="fecha.horaCierre" />
                      </div>
                    </div>
                    <div v-else
                      class="d-flex align-items-center justify-content-center gap-2 py-2 bg-white rounded border">
                      <span class="fw-semibold text-primary">{{ fecha.horaApertura?.slice(0, 5) }}</span>
                      <span class="text-muted">-</span>
                      <span class="fw-semibold text-primary">{{ fecha.horaCierre?.slice(0, 5) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="text-center p-5 text-muted bg-light rounded-4 border">
              <p class="mb-0 fs-5">{{ t.noSpecialDates }}</p>
            </div>
          </div>

          <!-- TAB 4: IMÁGENES -->
          <div class="tab-pane fade" id="imagenes">
            <div class="d-flex justify-content-center">
              <div class="card shadow rounded-4 p-3 text-center"
                style="max-width: 500px; width: 100%; background-color: rgba(255,255,255,0.75); backdrop-filter: blur(8px);">
                <h5 class="mb-3 d-flex justify-content-center align-items-center gap-2">
                  <i class="bi bi-images text-primary"></i> {{ t.images }}
                </h5>

                <img v-if="instalacion.imagenURL && !preview" :src="instalacion.imagenURL"
                  class="img-fluid rounded mb-3 shadow-sm" style="max-height: 300px; object-fit: cover;" />

                <div v-if="editando" class="mt-2">
                  <label class="form-label fw-semibold">{{ t.changeImage }}</label>
                  <input type="file" class="form-control form-control-lg" accept="image/*" @change="onFileChange" />
                </div>

                <img v-if="preview" :src="preview" class="img-fluid rounded shadow-sm border border-primary mt-3"
                  style="max-height: 300px; object-fit: cover;" />
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- MENSAJE -->
      <div class="text-center mt-3 fs-5">
        <p v-if="mensaje" class="text-danger fw-bold">{{ mensaje }}</p>
      </div>

      <!-- ACCIONES -->
      <div class="d-flex justify-content-center gap-4 mt-4 mb-5">
        <button v-if="!editando" class="btn btn-primary btn-lg rounded-pill px-5 shadow" @click="activarEdicion">
          {{ t.modifyFacility }}
        </button>

        <template v-else>
          <button class="btn btn-success btn-lg rounded-pill px-5 shadow" @click="guardarCambios">
            {{ t.saveChanges }}
          </button>
          <button class="btn btn-secondary btn-lg rounded-pill px-5 shadow" @click="cancelarEdicion">
            {{ t.cancel }}
          </button>
        </template>

        <button v-if="!editando" class="btn btn-outline-danger btn-lg rounded-pill px-5 bg-white"
          @click="abrirConfirmacion">
          {{ t.deleteFacility }}
        </button>
      </div>
    </main>

    <div class="modal fade" id="confirmDeleteModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4">

          <div class="modal-header">
            <h5 class="modal-title">{{ t.confirmDelete }}</h5>
          </div>

          <div class="modal-body text-center">
            <p>{{ t.confirmDeleteFacility }}</p>
          </div>

          <div class="modal-footer justify-content-center">
            <button class="btn btn-secondary rounded-pill" data-bs-dismiss="modal">
              {{ t.cancel }}
            </button>

            <button class="btn btn-danger rounded-pill" @click="confirmarEliminar">
              {{ t.delete }}
            </button>
          </div>

        </div>
      </div>
    </div>

    <div class="modal fade" id="successDeleteModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4 text-center">

          <div class="modal-body py-5">

            <i v-if="eliminado" class="bi bi-check-circle-fill text-success fs-1 mb-3"></i>
            <i v-else class="bi bi-exclamation-octagon-fill text-danger fs-1 mb-3"></i>

            <h4 class="fw-semibold">
              {{ mensaje }}
            </h4>

            <button class="btn btn-primary rounded-pill mt-4" @click="finalizar" data-bs-dismiss="modal">
              <span v-if="eliminado">{{ t.continue }}</span>
              <span v-else>{{ t.return }}</span>
            </button>

          </div>

        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { inject, ref, onMounted, type Ref, watch } from 'vue';
import { useRouter } from "vue-router";
import { Modal } from 'bootstrap'

/* Importamos la comunicacion para recuperar la informacion de instalaciones del backend */
import { getInstalacionDetalle, modificarInstalacion, eliminarInstalacion } from "@/services/detalleService";
import { getPabellonesSimples, getTarifasInstalacion } from "@/services/listadoService"

import { useTiposStore } from '@/stores/tipos';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const tiposStore = useTiposStore();
const router = useRouter();

const editando = ref(false)
const mensaje = ref("")

const imagen = ref<File | null>(null)
const preview = ref<string | null>(null)
const agenda = ref<any[]>([])
const fechasEspeciales = ref<any[]>([])
const pabellones = ref<any[]>([])
const tarifas = ref<any[]>([])

const instalacion = ref({
  id: 0,
  nombre: "",
  imagenURL: "",
  aforoMaximo: 50,
  luz: false,
  porcentajeTDA: 0,
  pabellon: null,
  tarifa: null,
  tipoInstalacion: "",
  numeroCalles: 0,
  agenda: [] as any[],
});

const errores = ref({
  nombre: false,
  aforoMaximo: false,
  porcentajeTDA: false,
  horaApertura: false,
  tarifa: false,
  pabellon: false,
  horaCierre: false,
  tipoInstalacion: false,
  numeroCalles: false
})

const instalacionOriginal = ref<any>(null);

function validarFormulario() {
  let valido = true

  errores.value.nombre = instalacion.value.nombre === ''
  errores.value.aforoMaximo = instalacion.value.aforoMaximo <= 0
  errores.value.porcentajeTDA = instalacion.value.porcentajeTDA < 0
  errores.value.pabellon = instalacion.value.pabellon === null
  errores.value.tarifa = instalacion.value.tarifa === null
  errores.value.tipoInstalacion = instalacion.value.tipoInstalacion === ''
  errores.value.tarifa
  errores.value.numeroCalles =
    instalacion.value.numeroCalles <= 0 &&
    instalacion.value.tipoInstalacion === "Piscina"

  for (const key in errores.value) {
    if (errores.value[key]) {
      valido = false
    }
  }

  return valido
}

function activarEdicion() {
  mensaje.value = ""
  instalacionOriginal.value = JSON.parse(JSON.stringify(instalacion.value))
  Object.keys(errores.value).forEach(k => errores.value[k] = false)
  editando.value = true
}

function cancelarEdicion() {
  mensaje.value = ""
  instalacion.value = JSON.parse(JSON.stringify(instalacionOriginal.value))
  agenda.value = JSON.parse(JSON.stringify(instalacionOriginal.value.agenda))
  preview.value = null
  imagen.value = null
  editando.value = false
}

function validarTipoInstalacion() {
  // Si el tipo es piscina no puede ser otro y viceversa
  if (instalacion.value.tipoInstalacion == "Piscina" && instalacionOriginal.value.tipoInstalacion != "Piscina") {
    errores.value.tipoInstalacion = true;
    return false;
  }

  if (instalacion.value.tipoInstalacion != "Piscina" && instalacionOriginal.value.tipoInstalacion == "Piscina") {
    errores.value.tipoInstalacion = true;
    return false;
  }

  return true
}

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  if (!input.files || input.files.length === 0) return
  imagen.value = input.files[0]
  preview.value = URL.createObjectURL(imagen.value)
}

async function guardarCambios() {
  mensaje.value = ""
  if (!validarFormulario()) {
    mensaje.value = t.value.emptyFields
    return
  }

  if (!validarTipoInstalacion()) {
    mensaje.value = t.value.cannotChangeType
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
    await modificarInstalacion(parseInt(props.id), formData)
    router.back()
  } catch (e: any) {
    mensaje.value = e.response?.data?.respuesta
    console.error(e)
  }
}

let confirmModal: Modal
let successModal: Modal

const eliminado = ref(false)

function abrirConfirmacion() {
  confirmModal.show()
}

async function confirmarEliminar() {
  try {
    await eliminarInstalacion(instalacion.value.id)

    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.facilityDeleted
    eliminado.value = true
  } catch (e) {
    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.facilityNoDeleted
    eliminado.value = false
    console.error("Error al eliminar la instalacion", e);
  }
}

const finalizar = async () => {
  if (eliminado.value) {
    router.push({ name: 'gestion-espacios' });
  } else {
    successModal.hide()
    eliminado.value = false
  }
}

const volver = () => {
  router.back();
};

watch(
  () => instalacion.value.tipoInstalacion,
  (tipo) => {
    mensaje.value = ""
    if (tipo !== "Piscina") {
      instalacion.value.numeroCalles = 0
    }
  }
)

onMounted(async () => {
  const id = parseInt(props.id);

  confirmModal = new Modal(document.getElementById('confirmDeleteModal')!)
  successModal = new Modal(document.getElementById('successDeleteModal')!)

  try {
    const data = await getInstalacionDetalle(id)
    pabellones.value = await getPabellonesSimples()
    tarifas.value = await getTarifasInstalacion()

    agenda.value = data.agenda.filter((a: any) => a.dia && !a.fecha)
    fechasEspeciales.value = data.agenda.filter((a: any) => a.fecha)

    instalacion.value = {
      ...data,
      agenda: agenda.value
    }

    instalacionOriginal.value = JSON.parse(JSON.stringify(instalacion.value))
  } catch (e) {
    mensaje.value = t.value.unexpectedError
    console.log("Error al obtener la informacion de la instalacion", e);
  }
});
</script>
