<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-4">

      <!-- TÍTULO -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold mb-0">
          {{ sesion.actividad.nombre }}
        </h1>

        <!-- BADGE HORARIO -->
        <span class="badge bg-primary fs-6" v-if="!editando">
          {{ sesion.dia }} · {{ sesion.horaInicio }} - {{ sesion.horaFin }}
        </span>

        <div v-else class="d-flex gap-2 align-items-center">
          <input
            type="text"
            class="form-control form-control-sm text-center"
            v-model="sesion.dia"
            style="width: 110px"
						:class="{ 'is-invalid': errores.dia }"
          />

          <input
            type="time"
            class="form-control form-control-sm"
            v-model="sesion.horaInicio"
						:class="{ 'is-invalid': errores.horaInicio }"
          />

          <span>—</span>

          <input
            type="time"
            class="form-control form-control-sm"
            v-model="sesion.horaFin"
						:class="{ 'is-invalid': errores.horaFin }"
          />
        </div>

        <div style="width: 100px"></div>
      </div>

      <div class="row g-4">

        <!-- DETALLES ACTIVIDAD -->
        <div class="col-lg-6">
          <div class="bg-white rounded-3 shadow-sm p-4 h-100">

            <h4 class="mb-3 d-flex align-items-center gap-2">
              <i class="bi bi-info-circle-fill text-primary"></i>
              {{ t.activityDetails }}
            </h4>

            <div class="row g-3">
              <div class="col-6">
                <span class="fw-medium">{{ t.period }}:</span>
                {{ sesion.actividad.periodo }}
              </div>

              <div class="col-6">
                <span class="fw-medium">{{ t.status }}:</span>
                {{ sesion.actividad.estado }}
              </div>

              <div class="col-6">
                <span class="fw-medium">{{ t.facility }}:</span>
                <span
                  class="text-primary fw-medium"
                  style="cursor: pointer"
                  @click="facilityDetail(sesion.actividad.instalacion.id)"
                >
                  {{ sesion.actividad.instalacion.nombre }}
                </span>
              </div>

              <div class="col-6">
                <span class="fw-medium">{{ t.level }}:</span>
                {{ sesion.actividad.nivel }}
              </div>
            </div>
          </div>
        </div>

        <!-- PARTICIPANTES -->
        <div class="col-lg-6">
          <div class="bg-white rounded-3 shadow-sm p-4 h-100">

            <h4 class="mb-3 d-flex align-items-center gap-2">
              <i class="bi bi-person-check-fill text-primary"></i>
              {{ t.participants }}
            </h4>

            <div
              v-for="u in sesion.participantes"
              :key="u.id"
              class="d-flex justify-content-between align-items-center p-3 mb-2 border rounded-3 bg-light"
            >
              <span class="fw-medium">{{ u.nombre }}</span>
            </div>

          </div>
        </div>
      </div>

      <!-- ACCIONES -->
      <div class="d-flex justify-content-center gap-4 mt-5">

        <button
          v-if="!editando"
          class="btn btn-primary btn-lg rounded-pill"
          @click="activarEdicion"
        >
          <i class="bi bi-pencil me-2"></i>
          {{ t.modifySession }}
        </button>

        <template v-else>
          <button
            class="btn btn-success btn-lg rounded-pill"
            @click="guardarCambios"
          >
            <i class="bi bi-check-lg me-2"></i>
            {{ t.saveChanges }}
          </button>

          <button
            class="btn btn-secondary btn-lg rounded-pill"
            @click="cancelarEdicion"
          >
            {{ t.cancel }}
          </button>
        </template>

        <button
          v-if="!editando"
          class="btn btn-danger btn-lg rounded-pill"
          @click="eliminar"
        >
          <i class="bi bi-trash me-2"></i>
          {{ t.deleteSession }}
        </button>

      </div>

    </main>
  </div>
</template>



<script setup lang="ts">
import { ref, onMounted, inject, type Ref } from "vue";
import { useRouter } from "vue-router";

import { getSesionDetalle, modificarSesion, eliminarSesion } from "@/services/detalleService"

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ idAct: string , idSesion: string}>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();

const editando = ref(false)

const sesion = ref({
	id: '',
  dia: "",
  horaInicio: "",
  horaFin: "",
  actividad: {
    nombre: "",
    periodo: "",
    estado: "",
    instalacion: {
        id: 0,
        nombre: ""
    },
    nivel: ""
  },
  participantes: [] as {
    id: number
    nombre: string
    presente: boolean
  }[]
});

const errores = ref({
  dia: false,
  horaInicio: false,
  horaFin: false
})

const sesionOriginal = ref<any>(null);

function validarFormulario() {
  let valido = true

	errores.value.dia = sesion.value.dia === ''
	errores.value.horaInicio = sesion.value.horaInicio === ''
	errores.value.horaFin = 
		sesion.value.horaFin === '' ||
		sesion.value.horaInicio >= sesion.value.horaFin

  for (const key in errores.value) {
    if(errores.value[key]) {
      valido = false
    }
  }

  return valido
}

function activarEdicion() {
  sesionOriginal.value = JSON.parse(JSON.stringify(sesion.value))
	Object.keys(errores.value).forEach(k => errores.value[k] = false)
  editando.value = true
}

function cancelarEdicion() {
  sesionOriginal.value = JSON.parse(JSON.stringify(sesion.value))
  editando.value = false
}

/* Solo mandamos al backend para modificar los campos que se hayan modificado */
function camposModificados() {
  const data: any = {}

	if(sesionOriginal.value.dia != sesion.value.dia) {
      data["dia"] = sesion.value.dia
  }

	if(sesionOriginal.value.horaInicio != sesion.value.horaInicio) {
      data["horaInicio"] = sesion.value.horaInicio
  }

	if(sesionOriginal.value.horaFin != sesion.value.horaFin) {
      data["horaFin"] = sesion.value.horaFin
  }

  return data;
}

const guardarCambios = async () => {
  try {
		if (!validarFormulario()) return

		const data = camposModificados();
    if(Object.keys(data).length > 0) {
      await modificarSesion(sesion.value.id, data);
    }
  } catch (e) {
    console.error("Error al modificar la sesion", e);
  }
}

const eliminar = async () => {
  try {
    await eliminarSesion(sesion.value.id)
  } catch (e) {
    console.error("Error al eliminar la sesion", e);
  }
}

const facilityDetail = (id: number) => {
  router.push({
    name: 'editar-instalacion',
    params: { id }
  });
}

const volver = () => router.back();

onMounted(async () => {
  try {
    sesion.value = await getSesionDetalle(props.idAct, props.idSesion);
    sesionOriginal.value = JSON.parse(JSON.stringify(sesion.value))
  } catch(e) {
    console.log("Error al obtener la informacion de la sesion", e);
  }
});
</script>
