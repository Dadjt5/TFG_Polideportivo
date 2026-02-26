<template>
  <div class="min-vh-100 bg-light">
    <main class="container-fluid mt-2 px-5 py-4">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <button class="btn btn-outline-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold mb-0 text-center flex-grow-1">
          <span v-if="!editando">{{ instalacion.nombre }}</span>
          <input
            v-else
            v-model="instalacion.nombre"
            class="form-control text-center fw-semibold"
            :class="{ 'is-invalid': errores.nombre }"
          />
        </h1>

        <div style="width: 120px"></div>
      </div>

      <!-- TARJETAS RESUMEN -->
      <div class="row g-3 mb-4">

        <div class="col-md-3">
          <div class="card shadow-sm rounded-4 border-0 p-3 text-center">
            <div class="fs-4 fw-bold">{{ instalacion.aforoMaximo }}</div>
            <div class="text-muted small">{{ t.capacity }}</div>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card shadow-sm rounded-4 border-0 p-3 text-center">
            <div class="fs-4 fw-bold">
              {{ instalacion.luz ? t.yes : 'No' }}
            </div>
            <div class="text-muted small">{{ t.light }}</div>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card shadow-sm rounded-4 border-0 p-3 text-center">
            <div class="fs-4 fw-bold">
              {{ instalacion.porcentajeTDA }}%
            </div>
            <div class="text-muted small">TDA</div>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card shadow-sm rounded-4 border-0 p-3 text-center">
            <div class="fw-semibold">
              {{ instalacion.tipoInstalacion }}
            </div>
            <div class="text-muted small">{{ t.facilityType }}</div>
          </div>
        </div>

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
                <label class="fw-medium">{{ t.capacity }}</label>
                <input
                  v-if="editando"
                  type="number"
                  min="1"
                  class="form-control"
                  v-model.number="instalacion.aforoMaximo"
                />
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
                <input
                  v-if="editando"
                  type="number"
                  min="0"
                  max="100"
                  class="form-control"
                  v-model.number="instalacion.porcentajeTDA"
                />
                <p v-else>{{ instalacion.porcentajeTDA }}%</p>
              </div>

              <div class="col-md-6">
                <label class="fw-medium">{{ t.facilityType }}</label>
                <select
                  v-if="editando"
                  class="form-select"
                  v-model="instalacion.tipoInstalacion"
                >
                  <option value="" disabled>--</option>
                  <option
                    v-for="t in tiposStore.tiposInstalacion"
                    :key="t[0]"
                    :value="t[0]"
                  >
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
            <div
              class="col-md-6 col-lg-4"
              v-for="dia in instalacion.agenda"
              :key="dia.dia"
            >
              <div
                class="card border-0 shadow-sm rounded-4 h-100"
                :class="dia.abierto ? 'border-success' : 'border-danger'"
              >
                <div class="card-body">

                  <div class="d-flex justify-content-between mb-2">
                    <strong>{{ dia.dia }}</strong>

                    <span
                      class="badge"
                      :class="dia.abierto ? 'bg-success' : 'bg-danger'"
                    >
                      {{ dia.abierto ? 'Abierto' : 'Cerrado' }}
                    </span>
                  </div>

                  <div v-if="dia.abierto" class="small text-muted">
                    {{ dia.horaApertura?.slice(0,5) }} -
                    {{ dia.horaCierre?.slice(0,5) }}
                  </div>

                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- FECHAS ESPECIALES -->
        <div class="tab-pane fade" id="especiales">
          <div v-if="instalacion.fechasEspeciales?.length" class="row g-3">
            <div
              class="col-md-4"
              v-for="fecha in instalacion.fechasEspeciales"
              :key="fecha.fecha"
            >
              <div
                class="card border-0 shadow-sm rounded-4 p-3"
                :class="fecha.abierto ? 'bg-success-subtle' : 'bg-danger-subtle'"
              >
                <div class="fw-semibold">
                  {{ fecha.fecha }}
                </div>

                <div v-if="fecha.abierto" class="small">
                  {{ fecha.apertura }} - {{ fecha.cierre }}
                </div>

                <div v-else class="small text-danger">
                  {{ t.close }}
                </div>
              </div>
            </div>
          </div>

          <div v-else class="text-muted">
            No hay fechas especiales configuradas.
          </div>
        </div>

        <!-- IMÁGENES -->
        <div class="tab-pane fade" id="imagenes">
          <div class="row g-3">
            <div
              class="col-md-4"
              v-for="(img, i) in instalacion.imagenURL"
              :key="i"
            >
              <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
                <img :src="img" class="img-fluid" />
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- ACCIONES -->
      <div class="d-flex justify-content-center gap-4 mt-5">
        <button
          v-if="!editando"
          class="btn btn-primary btn-lg rounded-pill px-4"
          @click="activarEdicion"
        >
          {{ t.modifyFacility }}
        </button>

        <template v-else>
          <button
            class="btn btn-success btn-lg rounded-pill px-4"
            @click="guardarCambios"
          >
            {{ t.saveChanges }}
          </button>

          <button
            class="btn btn-secondary btn-lg rounded-pill px-4"
            @click="cancelarEdicion"
          >
            {{ t.cancel }}
          </button>
        </template>

        <button
          v-if="!editando"
          class="btn btn-outline-danger btn-lg rounded-pill px-4"
          @click="eliminar"
        >
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

const instalacion = ref({
  id: 0,
  nombre: "",
  imagenURL: [] as string[],
  aforoMaximo: 50,
  luz: false,
  porcentajeTDA: 0,
  pabellon: { id: -1, nombre: "", direccion: "" },
  tipoInstalacion: "",
  agenda: [] as any[]
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
  instalacionOriginal.value = JSON.parse(JSON.stringify(instalacion.value))
  Object.keys(errores.value).forEach(k => errores.value[k] = false)
  editando.value = true
}

function cancelarEdicion() {
  instalacionOriginal.value = JSON.parse(JSON.stringify(instalacion.value))
  editando.value = false
}

/* Solo mandamos al backend para modificar los campos que se hayan modificado */
function camposModificados() {
  const data: any = {}

  if (instalacionOriginal.value.nombre != instalacion.value.nombre) {
    data["nombre"] = instalacion.value.nombre
  }

  if (instalacionOriginal.value.porcentajeTDA != instalacion.value.porcentajeTDA) {
    data["porcentajeTDA"] = instalacion.value.porcentajeTDA
  }

  if (instalacionOriginal.value.aforoMaximo != instalacion.value.aforoMaximo) {
    data["aforoMaximo"] = instalacion.value.aforoMaximo
  }

  if (instalacionOriginal.value.luz != instalacion.value.luz) {
    data["luz"] = instalacion.value.luz
  }

  if (instalacionOriginal.value.tipoInstalacion != instalacion.value.tipoInstalacion) {
    data["tipoInstalacion"] = instalacion.value.tipoInstalacion
  }

  return data;
}


const guardarCambios = async () => {
  try {
    if (!validarFormulario()) return

    const data = camposModificados();
    if (Object.keys(data).length > 0) {
      await modificarInstalacion(instalacion.value.id, data);
      await actualizarAgenda(instalacion.value.id, agenda.value, fechasEspeciales.value)
      editando.value = false
    }
  } catch (e) {
    console.error("Error al modificar la instalacion", e);
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
    instalacion.value = await getInstalacionDetalle(id);
    instalacionOriginal.value = JSON.parse(JSON.stringify(instalacion.value))
  } catch (e) {
    console.log("Error al obtener la informacion de la instalacion", e);
  }
});
</script>
