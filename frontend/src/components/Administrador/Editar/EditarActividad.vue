<template>
  <div class="min-vh-100 bg-light">
    <main class="container-fluid mt-2 px-5 py-4">
      <!-- HEADER -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold mb-0 w-50 text-center">
          <span v-if="!editando">{{ actividad.nombre }}</span>
          <input v-else v-model="actividad.nombre" class="form-control text-center fw-semibold"
            :class="{ 'is-invalid': errores.nombre }" />
        </h1>

        <div style="width: 100px"></div>
      </div>

      <div class="row g-4">
        <div class="col-lg-6">
          <div class="bg-white rounded-3 shadow-sm p-4 h-100">
            <h4 class="mb-3 d-flex align-items-center">
              <i class="bi bi-info-circle-fill text-primary me-2"></i>
              {{ t.activityDetails }}
            </h4>

            <div class="row g-3">

              <!-- PERIODO -->
              <div class="col-12 col-sm-4">
                <span class="fw-medium">{{ t.period }}:</span>
                <span v-if="!editando"> {{ actividad.periodo }}</span>
                <input v-else v-model="actividad.periodo" class="form-control"
                  :class="{ 'is-invalid': errores.periodo }" />
              </div>

              <!-- ESTADO -->
              <div class="col-12 col-sm-4">
                <span class="fw-medium">{{ t.status }}:</span>
                <span v-if="!editando"> {{ actividad.estado }}</span>
                <input v-else v-model="actividad.estado" class="form-control"
                  :class="{ 'is-invalid': errores.estado }" />
              </div>

              <!-- EDAD MINIMA -->
              <div class="col-12 col-sm-4">
                <span class="fw-medium">{{ t.minimumAge }}:</span>
                <span v-if="!editando"> {{ actividad.edadMinima }}</span>
                <input v-else type="number" v-model.number="actividad.edadMinima" class="form-control"
                  :class="{ 'is-invalid': errores.edadMinima }" />
              </div>

              <!-- PLAZAS MAX -->
              <div class="col-12 col-sm-4">
                <span class="fw-medium">{{ t.availablePlaces }}:</span>
                <span v-if="!editando"> {{ actividad.plazasMaximas }}</span>
                <input v-else type="number" v-model.number="actividad.plazasMaximas" class="form-control"
                  :class="{ 'is-invalid': errores.plazasMaximas }" />
              </div>

              <!-- PLAZAS RESERVADAS -->
              <div class="col-12 col-sm-4">
                <span class="fw-medium">{{ t.reservedPlaces }}:</span>
                <span v-if="!editando"> {{ actividad.plazasReservadas }}</span>
                <input v-else type="number" v-model.number="actividad.plazasReservadas" class="form-control"
                  :class="{ 'is-invalid': errores.plazasReservadas }" />
              </div>

              <!-- TIPO ACTIVIDAD -->
              <div class="col-12 col-sm-4">
                <span class="fw-medium">{{ t.activityType }}:</span>
                <span v-if="!editando"> {{ actividad.tipoActividad }}</span>
                <input v-else v-model="actividad.tipoActividad" class="form-control"
                  :class="{ 'is-invalid': errores.tipoActividad }" />
              </div>

              <!-- TERRENO -->
              <div class="col-12 col-sm-4">
                <span class="fw-medium">{{ t.terrainType }}:</span>
                <span v-if="!editando"> {{ actividad.terreno }}</span>
                <input v-else v-model="actividad.terreno" class="form-control"
                  :class="{ 'is-invalid': errores.terreno }" />
              </div>

              <!-- TIPO RESERVA -->
              <div class="col-12 col-sm-4">
                <span class="fw-medium">{{ t.reserveType }}:</span>
                <span v-if="!editando"> {{ actividad.tipoReserva }}</span>
                <input v-else v-model="actividad.tipoReserva" class="form-control"
                  :class="{ 'is-invalid': errores.tipoReserva }" />
              </div>

              <!-- CREDITOS -->
              <div class="col-12 col-sm-4">
                <span class="fw-medium">{{ t.credits }}:</span>
                <span v-if="!editando"> {{ actividad.numeroCreditos }}</span>
                <input v-else type="number" v-model.number="actividad.numeroCreditos" class="form-control"
                  :class="{ 'is-invalid': errores.numeroCreditos }" />
              </div>

              <!-- AÑO -->
              <div class="col-12 col-sm-4">
                <span class="fw-medium">{{ t.academicYear }}:</span>
                <span v-if="!editando"> {{ actividad.año }}</span>
                <input v-else type="number" v-model.number="actividad.año" class="form-control"
                  :class="{ 'is-invalid': errores.año }" />
              </div>

            </div>
          </div>
        </div>

        <!-- DERECHA -->
        <div class="col-lg-6 d-flex flex-column gap-4">

          <!-- IMAGENES -->
          <div class="bg-white rounded-3 shadow-sm p-4">
            <h4 class="mb-3 d-flex align-items-center gap-2">
              <i class="bi bi-images text-primary"></i>
              {{ t.images }}
            </h4>

            <div class="row g-2">
              <div class="col-6" v-for="(img, i) in actividad.imagenURL" :key="i">
                <img :src="img" class="img-fluid rounded" alt="Actividad" />
              </div>
            </div>
          </div>

          <!-- SESIONES -->
          <div class="bg-white rounded-3 shadow-sm p-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h4 class="mb-0 d-flex align-items-center gap-2">
                <i class="bi bi-calendar-event text-primary"></i>
                {{ t.sessions }}
              </h4>

              <button class="btn btn-primary btn-sm rounded-pill" @click="nuevaSesion(actividad.id)">
                <i class="bi bi-plus-lg me-1"></i>
                {{ t.newSession }}
              </button>
            </div>

            <!-- LISTADO -->
            <div v-if="actividad.sesiones.length > 0">
              <div v-for="s in actividad.sesiones" :key="s.id"
                class="d-flex justify-content-between align-items-center p-3 mb-2 border rounded-3 bg-light"
                style="cursor: pointer" @click="sesionDetail(s.id)">
                <div>
                  <div class="fw-semibold">
                    {{ s.dia }}
                  </div>
                  <div class="text-muted small">
                    {{ s.horario.horaInicio }} - {{ s.horario.horaFin }}
                  </div>
                </div>

                <i class="bi bi-chevron-right text-muted"></i>
              </div>
            </div>

            <!-- EMPTY STATE -->
            <div v-else class="text-muted text-center py-4">
              <i class="bi bi-calendar-x fs-4 d-block mb-2"></i>
              {{ t.noSession }}
            </div>
          </div>


        </div>
      </div>

      <!-- ACCIONES -->
      <div class="d-flex justify-content-center gap-4 mt-5">

        <button v-if="!editando" class="btn btn-primary btn-lg rounded-pill" @click="activarEdicion">
          <i class="bi bi-pencil me-2"></i>
          {{ t.modifyUser }}
        </button>

        <template v-else>
          <button class="btn btn-success btn-lg rounded-pill" @click="guardarCambios">
            <i class="bi bi-check-lg me-2"></i>
            {{ t.saveChanges }}
          </button>

          <button class="btn btn-secondary btn-lg rounded-pill" @click="cancelarEdicion">
            {{ t.cancel }}
          </button>
        </template>

        <button v-if="!editando" class="btn btn-danger btn-lg rounded-pill" @click="eliminar">
          <i class="bi bi-trash me-2"></i>
          {{ t.deleteUser }}
        </button>

      </div>
    </main>
  </div>
</template>



<script setup lang="ts">
import { inject, type Ref, ref, onMounted } from 'vue';
import { useRouter } from "vue-router";

/* Importamos la comunicacion para recuperar la informacion de actividades del backend y el usuario*/
import { getActividadDetalle, modificarActividad, eliminarActividad } from "@/services/detalleService";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();

type Generic = {
  id: number
  nombre: string
}

const actividad = ref({
  id: 0,
  nombre: "",
  tipoActividad: "",
  imagenURL: [] as string[],
  plazasMaximas: 0,
  plazasReservadas: 0,
  edadMinima: 0,
  año: 0,
  numeroCreditos: 0,
  nivel: "",
  material: "",
  exterior: false,
  tipoReserva: "",
  terreno: "",
  periodo: "",
  estado: "",
  dias: "",
  horasSemanales: "",
  instalacion: {
    id: -1,
    nombre: ""
  } as Generic,

  monitor: {
    id: -1,
    nombre: ""
  } as Generic,

  sesiones: [] as any[]
});

const errores = ref({
  nombre: false,
  tipoActividad: false,
  plazasMaximas: false,
  plazasReservadas: false,
  edadMinima: false,
  año: false,
  numeroCreditos: false,
  tipoReserva: false,
  terreno: false,
  periodo: false,
  estado: false
})

const editando = ref(false)
const añoActual = new Date().getFullYear()
const actividadOriginal = ref<any>(null);

function validarFormulario() {
  let valido = true

  errores.value.nombre = actividad.value.nombre === ''
  errores.value.plazasMaximas = actividad.value.plazasMaximas <= 0
  errores.value.plazasReservadas =
    actividad.value.plazasReservadas <= 0 ||
    actividad.value.plazasReservadas > actividad.value.plazasMaximas
  errores.value.tipoActividad = actividad.value.tipoActividad === ''
  errores.value.edadMinima = actividad.value.edadMinima <= 0
  errores.value.año = actividad.value.año < añoActual
  errores.value.numeroCreditos = actividad.value.numeroCreditos <= 0
  errores.value.tipoReserva = actividad.value.tipoReserva === ''
  errores.value.terreno = actividad.value.terreno === ''
  errores.value.periodo = actividad.value.periodo === ''
  errores.value.estado = actividad.value.estado === ''


  for (const key in errores.value) {
    if (errores.value[key]) {
      valido = false
    }
  }

  return valido
}

function activarEdicion() {
  actividadOriginal.value = JSON.parse(JSON.stringify(actividad.value))
  Object.keys(errores.value).forEach(k => errores.value[k] = false)
  editando.value = true
}

function cancelarEdicion() {
  actividadOriginal.value = JSON.parse(JSON.stringify(actividad.value))
  editando.value = false
}

/* Solo mandamos al backend para modificar los campos que se hayan modificado */
function camposModificados() {
  const data: any = {}

  if (actividadOriginal.value.nombre !== actividad.value.nombre) {
    data.nombre = actividad.value.nombre
  }

  if (actividadOriginal.value.plazasMaximas !== actividad.value.plazasMaximas) {
    data.plazasMaximas = actividad.value.plazasMaximas
  }

  if (actividadOriginal.value.plazasReservadas !== actividad.value.plazasReservadas) {
    data.plazasReservadas = actividad.value.plazasReservadas
  }

  if (actividadOriginal.value.tipoActividad !== actividad.value.tipoActividad) {
    data.tipoActividad = actividad.value.tipoActividad
  }

  if (actividadOriginal.value.edadMinima !== actividad.value.edadMinima) {
    data.edadMinima = actividad.value.edadMinima
  }

  if (actividadOriginal.value.año !== actividad.value.año) {
    data.año = actividad.value.año
  }

  if (actividadOriginal.value.numeroCreditos !== actividad.value.numeroCreditos) {
    data.numeroCreditos = actividad.value.numeroCreditos
  }

  if (actividadOriginal.value.tipoReserva !== actividad.value.tipoReserva) {
    data.tipoReserva = actividad.value.tipoReserva
  }

  if (actividadOriginal.value.terreno !== actividad.value.terreno) {
    data.terreno = actividad.value.terreno
  }

  if (actividadOriginal.value.periodo !== actividad.value.periodo) {
    data.periodo = actividad.value.periodo
  }

  if (actividadOriginal.value.estado !== actividad.value.estado) {
    data.estado = actividad.value.estado
  }

  return data
}


const guardarCambios = async () => {
  try {
    if (!validarFormulario()) return

    const data = camposModificados();
    if (Object.keys(data).length > 0) {
      await modificarActividad(actividad.value.id, data);
    }
  } catch (e) {
    console.error("Error al modificar la actividad", e);
  }
}

const eliminar = async () => {
  try {
    await eliminarActividad(actividad.value.id)
  } catch (e) {
    console.error("Error al eliminar la actividad", e);
  }
}

const sesionDetail = (id: number) => {
  router.push({
    name: 'editar-sesion',
    params: { id }
  });
}

const nuevaSesion = (id: number) => {
  router.push({
    name: 'crear-sesion',
    params: { id }
  });
}

const volver = () => {
  router.back();
};

onMounted(async () => {
  const id = parseInt(props.id);

  try {
    actividad.value = await getActividadDetalle(id);
    actividadOriginal.value = JSON.parse(JSON.stringify(actividad.value))
  } catch (e) {
    console.log("Error al obtener la informacion de la actividad", e);
  }
});
</script>
