<template>
  <div class="min-vh-100 pt-4" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4" style="max-width: 1600px;">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold mb-0">{{ instalacion.nombre }}</h1>

        <div style="width: 100px"></div>
      </div>

      <!-- TABS -->
      <ul class="nav nav-pills mb-4">
        <li class="nav-item">
          <button class="nav-link active" data-bs-toggle="pill" data-bs-target="#info">
            {{ t.facilityDetails }}
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" data-bs-toggle="pill" data-bs-target="#horario">
            {{ t.timetable }}
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" data-bs-toggle="pill" data-bs-target="#especiales">
            {{ t.specialDates }}
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" data-bs-toggle="pill" data-bs-target="#imagenes">
            {{ t.images }}
          </button>
        </li>
      </ul>

      <div class="tab-content">

        <!-- INFORMACIÓN -->
        <div class="tab-pane fade show active" id="info">
          <div class="card border-0 shadow-sm rounded-4 p-4">
            <div class="row g-4">

              <div class="col-md-6">
                <label class="fw-medium">{{ t.name }}</label>
                <input v-if="editando" class="form-control" v-model="instalacion.nombre"
                  :class="{ 'is-invalid': errores.nombre }" />
                <p v-else>{{ instalacion.nombre }}</p>
              </div>

              <div class="col-md-6">
                <label class="fw-medium">{{ t.capacity }}</label>
                <input v-if="editando" type="number" min="1" class="form-control"
                  v-model.number="instalacion.aforoMaximo" />
                <p v-else>{{ instalacion.aforoMaximo }}</p>
              </div>

              <div class="col-md-6">
                <label class="fw-medium">{{ t.light }}</label>
                <div v-if="editando" class="form-check">
                  <input class="form-check-input" type="checkbox" v-model="instalacion.luz" />
                </div>
                <p v-else>{{ instalacion.luz ? t.yes : 'No' }}</p>
              </div>

              <div class="col-md-6">
                <label class="fw-medium">TDA (%)</label>
                <input v-if="editando" type="number" min="0" max="100" class="form-control"
                  v-model.number="instalacion.porcentajeTDA" />
                <p v-else>{{ instalacion.porcentajeTDA }}%</p>
              </div>

              <div class="col-md-6">
                <label class="fw-medium">{{ t.facilityType }}</label>
                <select v-if="editando" class="form-select" v-model="instalacion.tipoInstalacion">
                  <option value="" disabled>--</option>
                  <option v-for="t in tiposStore.tiposInstalacion" :key="t[0]" :value="t[0]">
                    {{ t[1] }}
                  </option>
                </select>
                <p v-else>{{ instalacion.tipoInstalacion }}</p>
              </div>

            </div>
          </div>
        </div>

        <!-- HORARIO SEMANAL -->
        <div class="tab-pane fade" id="horario">
          <div class="row g-3">
            <div class="col-md-6 col-lg-4" v-for="dia in agenda" :key="dia.dia">
              <div class="card border-0 shadow-sm rounded-4 h-100">
                <div class="card-body">

                  <div class="d-flex justify-content-between align-items-center mb-3">
                    <strong>{{ dia.dia }}</strong>

                    <div v-if="editando">
                      <div class="form-check form-switch">
                        <input class="form-check-input" type="checkbox" v-model="dia.abierto" />
                      </div>
                    </div>

                    <span v-else class="badge" :class="dia.abierto ? 'bg-success' : 'bg-danger'">
                      {{ dia.abierto ? 'Abierto' : 'Cerrado' }}
                    </span>
                  </div>

                  <div v-if="dia.abierto">

                    <!-- MODO EDICIÓN -->
                    <div v-if="editando" class="row g-2">
                      <div class="col-6">
                        <label class="small text-muted">Apertura</label>
                        <input type="time" class="form-control" v-model="dia.horaApertura" />
                      </div>
                      <div class="col-6">
                        <label class="small text-muted">Cierre</label>
                        <input type="time" class="form-control" v-model="dia.horaCierre" />
                      </div>
                    </div>

                    <!-- MODO LECTURA -->
                    <div v-else class="small text-muted">
                      {{ dia.horaApertura?.slice(0, 5) }} -
                      {{ dia.horaCierre?.slice(0, 5) }}
                    </div>

                  </div>

                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- FECHAS ESPECIALES -->
        <div class="tab-pane fade" id="especiales">

          <!-- BOTÓN AÑADIR -->
          <div v-if="editando" class="mb-4">
            <button class="btn btn-outline-primary rounded-pill" @click="fechasEspeciales.push({
              fecha: '',
              horaApertura: '',
              horaCierre: '',
              abierto: true
            })">
              + Añadir fecha especial
            </button>
          </div>

          <div v-if="fechasEspeciales?.length" class="row g-3">
            <div class="col-md-4" v-for="(fecha, index) in fechasEspeciales" :key="index">
              <div class="card border-0 shadow-sm rounded-4 p-3">

                <!-- CABECERA -->
                <div class="d-flex justify-content-between align-items-center mb-3">

                  <!-- FECHA -->
                  <div v-if="editando">
                    <input type="date" class="form-control" v-model="fecha.fecha" />
                  </div>

                  <div v-else class="fw-semibold">
                    {{ fecha.fecha }}
                  </div>

                  <!-- ELIMINAR -->
                  <button v-if="editando" class="btn btn-sm btn-outline-danger"
                    @click="fechasEspeciales.splice(index, 1)">
                    ✕
                  </button>
                </div>

                <!-- ABIERTO / CERRADO -->
                <div class="mb-3">
                  <div v-if="editando" class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" v-model="fecha.abierto" />
                    <label class="form-check-label">
                      Abierto
                    </label>
                  </div>

                  <span v-else class="badge" :class="fecha.abierto ? 'bg-success' : 'bg-danger'">
                    {{ fecha.abierto ? 'Abierto' : 'Cerrado' }}
                  </span>
                </div>

                <!-- HORAS -->
                <div v-if="fecha.abierto">

                  <div v-if="editando" class="row g-2">
                    <div class="col-6">
                      <label class="small text-muted">Apertura</label>
                      <input type="time" class="form-control" v-model="fecha.horaApertura" />
                    </div>
                    <div class="col-6">
                      <label class="small text-muted">Cierre</label>
                      <input type="time" class="form-control" v-model="fecha.horaCierre" />
                    </div>
                  </div>

                  <div v-else class="small">
                    {{ fecha.horaApertura?.slice(0, 5) }} -
                    {{ fecha.horaCierre?.slice(0, 5) }}
                  </div>

                </div>

              </div>
            </div>
          </div>

          <div v-else class="text-muted">
            {{ t.noSpecialDates }}
          </div>

        </div>

        <!-- IMÁGENES -->
        <div class="tab-pane fade" id="imagenes">
          <div class="row g-3">
            <div class="col-md-4" v-for="(img, i) in instalacion.imagenURL" :key="i">
              <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
                <img :src="img" class="img-fluid" />
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- MENSAJE -->
      <div class="text-center mt-4 fs-5">
        <p v-if="mensaje" class="text-danger">{{ mensaje }}</p>
      </div>

      <!-- ACCIONES -->
      <div class="d-flex justify-content-center gap-4 mt-5">
        <button v-if="!editando" class="btn btn-primary btn-lg rounded-pill px-4" @click="activarEdicion">
          {{ t.modifyFacility }}
        </button>

        <template v-else>
          <button class="btn btn-success btn-lg rounded-pill px-4" @click="guardarCambios">
            {{ t.saveChanges }}
          </button>

          <button class="btn btn-secondary btn-lg rounded-pill px-4" @click="cancelarEdicion">
            {{ t.cancel }}
          </button>
        </template>

        <button v-if="!editando" class="btn btn-outline-danger btn-lg rounded-pill px-4" @click="eliminar">
          {{ t.deleteFacility }}
        </button>
      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { inject, ref, onMounted, type Ref } from 'vue';
import { useRouter } from "vue-router";

/* Importamos la comunicacion para recuperar la informacion de instalaciones del backend */
import { getInstalacionDetalle, modificarInstalacion, eliminarInstalacion } from "@/services/detalleService";

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

const agenda = ref<any[]>([])
const fechasEspeciales = ref<any[]>([])

const instalacion = ref({
  id: 0,
  nombre: "",
  imagenURL: [] as string[],
  aforoMaximo: 50,
  luz: false,
  porcentajeTDA: 0,
  pabellon: { id: -1, nombre: "", direccion: "" },
  tipoInstalacion: "",
  agenda: [] as any[],
});

const errores = ref({
  nombre: false,
  aforoMaximo: false,
  porcentajeTDA: false,
  horaApertura: false,
  horaCierre: false,
  tipoInstalacion: false
})

const instalacionOriginal = ref<any>(null);

function validarFormulario() {
  let valido = true

  errores.value.nombre = instalacion.value.nombre === ''
  errores.value.aforoMaximo = instalacion.value.aforoMaximo <= 0
  errores.value.porcentajeTDA = instalacion.value.porcentajeTDA <= 0
  errores.value.tipoInstalacion = instalacion.value.tipoInstalacion === ''

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
  editando.value = false
}

async function guardarCambios() {
  mensaje.value = ""
  if (!validarFormulario()) {
    mensaje.value = t.value.emptyFields
    return
  }

  try {
    await modificarInstalacion(
      parseInt(props.id),
      instalacion.value,
      agenda.value,
      fechasEspeciales.value
    )
    router.back()
  } catch (e: any) {
    mensaje.value = e.response?.data?.respuesta
    console.error(e)
  }
}

const eliminar = async () => {
  try {
    await eliminarInstalacion(instalacion.value.id)
    router.push({ name: 'gestion-espacios' });
  } catch (e) {
    console.error("Error al eliminar la instalacion", e);
  }
}

const volver = () => {
  router.back();
};

onMounted(async () => {
  const id = parseInt(props.id);

  try {
    const data = await getInstalacionDetalle(id)

    agenda.value = data.agenda.filter((a: any) => a.dia && !a.fecha)
    fechasEspeciales.value = data.agenda.filter((a: any) => a.fecha)

    instalacion.value = {
      ...data,
      agenda: agenda.value
    }

    instalacionOriginal.value = JSON.parse(JSON.stringify(instalacion.value))

  } catch (e) {
    console.log("Error al obtener la informacion de la instalacion", e);
  }
});
</script>
