<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container py-4">

      <!-- TÍTULO -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="fw-semibold text-primary mb-0" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
          <i class="bi bi-calendar2-check me-2"></i>
          {{ sesion.actividad.nombre }}
        </h1>

        <span class="badge bg-primary fs-6">
          {{ sesion.dia }} · {{ sesion.horaInicio }} - {{ sesion.horaFin }}
        </span>
      </div>

      <div class="row g-4">

        <!-- DETALLES -->
        <div class="col-lg-6">
          <div class="bg-white rounded-3 shadow-sm p-4 h-100 card-hover">

            <h4 class="mb-3 d-flex align-items-center gap-2">
              <i class="bi bi-info-circle-fill text-primary"></i>
              {{ t.activityDetails }}
            </h4>

            <div class="row g-3">
              <div class="col-6">
                <i class="bi bi-clock-fill text-success me-1"></i>
                <span class="fw-medium">{{ t.period }}:</span>
                {{ sesion.actividad.periodo }}
              </div>

              <div class="col-6">
                <i class="bi bi-info-circle text-info me-1"></i>
                <span class="fw-medium">{{ t.status }}:</span>
                {{ sesion.actividad.estado }}
              </div>

              <div class="col-6">
                <i class="bi bi-building text-primary me-1"></i>
                <span class="fw-medium">{{ t.facility }}: </span>
                <span class="text-primary fw-medium" style="cursor: pointer;"
                    @click="facilityDetail(sesion.actividad.instalacion.id)">
                    {{ sesion.actividad.instalacion.nombre }}
                </span>
              </div>

              <div class="col-6">
                <i class="bi bi-bar-chart-fill text-info me-1"></i>
                <span class="fw-medium">{{ t.level }}:</span>
                {{ sesion.actividad.nivel }}
              </div>
            </div>
          </div>
        </div>

        <!-- PASAR LISTA -->
        <div class="col-lg-6">
          <div class="bg-white rounded-3 shadow-sm p-4 h-100 card-hover">

            <h4 class="mb-3 d-flex align-items-center gap-2">
              <i class="bi bi-person-check-fill text-primary"></i>
              {{ t.participants }}
            </h4>

            <div
              v-for="u in sesion.participantes"
              :key="u.id"
              class="d-flex justify-content-between align-items-center p-3 mb-2 border rounded-3 bg-light participant-hover"
            >
              <span class="fw-medium">{{ u.nombre }}</span>

              <button
                class="btn btn-sm"
                :class="u.presente ? 'btn-gradient-success' : 'btn-outline-secondary'"
                @click="cambiarAsistencia(u)"
              >
                <i :class="u.presente ? 'bi bi-check-lg' : 'bi bi-x-lg'"></i>
              </button>
            </div>

          </div>
        </div>
      </div>

      <div class="d-flex justify-content-center mt-5 gap-3">
        <button class="btn btn-gradient-success btn-lg px-5" @click="actualizarAsistencia">
          {{ t.save }}
        </button>

        <button class="btn btn-secondary btn-lg px-5" @click="volver">
          {{ t.return }}
        </button>
      </div>

    </main>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted, inject, type Ref } from "vue";
import { useRouter } from "vue-router";

import { getSesionDetalle } from "@/services/detalleService"
import { guardarAsistencia } from "@/services/monitorService";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ idAct: string , idSesion: string}>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();

const sesion = ref({
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

const facilityDetail = (id: number) => {
  router.push({
    name: 'detalle-instalacion',
    params: { id }
  });
}

const cambiarAsistencia = (u: any) => {
  u.presente = !u.presente;
};

const actualizarAsistencia = async () => {
  try {
		const respuesta = await guardarAsistencia(parseInt(props.idAct), parseInt(props.idSesion), sesion.value.participantes);
		router.back();
	} catch(e) {
		console.log("Error al guardar la asistencia de los usuarios", e)
	}
};

const volver = () => router.back();

onMounted(async () => {
	try {
	  sesion.value = await getSesionDetalle(props.idAct, props.idSesion);
	} catch(e) {
		console.log("Error al obtener la informacion de la sesion", e)
	}
});
</script>

<style scoped>
.card-hover {
  transition: all 0.3s ease;
}
.card-hover:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.15);
}

.participant-hover {
  transition: all 0.2s ease;
}
.participant-hover:hover {
  transform: translateY(-2px);
  background-color: rgba(255,255,255,0.95);
}

.btn-gradient-success {
  background: linear-gradient(135deg, #56ab2f, #a8e063);
  border: none;
  color: white;
}
.btn-gradient-success:hover {
  filter: brightness(1.1);
}
</style>