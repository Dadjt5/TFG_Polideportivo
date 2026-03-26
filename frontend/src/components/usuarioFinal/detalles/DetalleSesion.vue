<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container py-4">

      <!-- HEADER PRINCIPAL -->
      <div class="bg-white rounded-4 shadow-sm p-4 mb-4 d-flex justify-content-between align-items-center">

        <div>
          <h2 class="fw-bold mb-1 text-primary">
            <i class="bi bi-calendar2-check me-2"></i>
            {{ sesion?.actividad?.nombre }}
          </h2>

          <div class="text-muted">
            {{ sesion?.dia }} · {{ sesion?.horaInicio }} - {{ sesion?.horaFin }}
          </div>
        </div>

        <div class="text-end">
          <div class="fs-4 fw-bold text-success">
            {{ sesion.presentes }} / {{ sesion.totalParticipantes }}
          </div>

          <small class="text-muted">{{ t.assistance }}</small>

          <!-- Barra progreso -->
          <div class="progress mt-2" style="height: 6px; width: 120px;">
            <div
              class="progress-bar bg-success"
              role="progressbar"
              :style="{
                width: (sesion.totalParticipantes
                  ? (sesion.presentes / sesion.totalParticipantes) * 100
                  : 0) + '%'
              }"
            ></div>
          </div>
        </div>

      </div>

      <div class="row g-4">

        <!-- DETALLES -->
        <div class="col-lg-5">
          <div class="bg-white rounded-4 shadow-sm p-4 h-100">

            <h5 class="mb-3">
              <i class="bi bi-info-circle-fill text-primary me-2"></i>
              {{ t.activityDetails }}
            </h5>

            <div class="row g-3 small">

              <div class="col-6">
                <span class="text-muted">{{ t.period }}</span><br>
                <strong>{{ sesion?.actividad?.periodo }}</strong>
              </div>

              <div class="col-6">
                <span class="text-muted">{{ t.terrain }}</span><br>
                <strong>{{ sesion?.actividad?.terreno }}</strong>
              </div>

              <div class="col-6">
                <span class="text-muted">{{ t.facility }}</span><br>
                <span class="text-primary fw-semibold" style="cursor: pointer;"
                  @click="facilityDetail(sesion?.actividad?.instalacion.id)">
                  {{ sesion?.actividad?.instalacion.nombre }}
                </span>
              </div>

              <div class="col-6">
                <span class="text-muted">{{ t.level }}</span><br>
                <strong>{{ sesion?.actividad?.nivel || '-' }}</strong>
              </div>

              <div class="col-6">
                <span class="text-muted">{{ t.duration }}</span><br>
                <strong>{{ sesion.duracion }} min</strong>
              </div>

              <div class="col-6">
                <span class="text-muted">{{ t.registeredUsers }}</span><br>
                <strong>{{ sesion.totalParticipantes }}</strong>
              </div>

            </div>
          </div>
        </div>

        <!-- PASAR LISTA -->
        <div class="col-lg-7">
          <div class="bg-white rounded-4 shadow-sm p-4 h-100 d-flex flex-column">

            <!-- HEADER -->
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="mb-0">
                <i class="bi bi-people-fill text-primary me-2"></i>
                {{ t.participants }}
              </h5>

              <div class="d-flex gap-2">
                <button class="btn btn-sm btn-outline-success" @click="marcarTodos(true)">
                  {{ t.all }} ✓
                </button>
                <button class="btn btn-sm btn-outline-danger" @click="marcarTodos(false)">
                  {{ t.anyone }} ✕
                </button>
              </div>
            </div>

            <!-- FILTROS -->
            <div class="d-flex gap-2 mb-3">
              <button
                class="btn btn-sm"
                :class="filtro === 'todos' ? 'btn-primary' : 'btn-outline-primary'"
                @click="filtro = 'todos'"
              >
                {{ t.all }}
              </button>

              <button
                class="btn btn-sm"
                :class="filtro === 'presentes' ? 'btn-success' : 'btn-outline-success'"
                @click="filtro = 'presentes'"
              >
                {{ t.attendees }}
              </button>

              <button
                class="btn btn-sm"
                :class="filtro === 'ausentes' ? 'btn-danger' : 'btn-outline-danger'"
                @click="filtro = 'ausentes'"
              >
                {{ t.absentes }}
              </button>
            </div>

            <!-- LISTA -->
            <div style="max-height: 400px; overflow-y: auto;">

              <div
                v-for="u in participantesFiltrados"
                :key="u.id"
                class="d-flex align-items-center justify-content-between p-3 mb-2 rounded-3 border participant-card"
              >
                <div class="d-flex align-items-center gap-3">

                  <div class="avatar">
                    {{ u.nombre.charAt(0) }}
                  </div>

                  <div>
                    <div class="fw-semibold">{{ u.nombre }}</div>
                    <small :class="u.presente ? 'text-success' : 'text-muted'">
                      {{ u.presente ? 'Presente' : 'Ausente' }}
                    </small>
                  </div>
                </div>

                <button
                  class="btn"
                  :class="u.presente ? 'btn-success' : 'btn-outline-secondary'"
                  @click="cambiarAsistencia(u)"
                >
                  <i :class="u.presente ? 'bi bi-check-lg' : 'bi bi-x-lg'"></i>
                </button>
              </div>

            </div>

          </div>
        </div>

      </div>

      <!-- BOTONES -->
      <div class="d-flex justify-content-center mt-5 gap-3">
        <button class="btn btn-success btn-lg px-5" @click="actualizarAsistencia">
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
import { ref, onMounted, inject, type Ref, computed } from "vue";
import { useRouter } from "vue-router";

import { getSesionDetalle } from "@/services/detalleService"
import { guardarAsistencia } from "@/services/monitorService";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ idAct: string, idSesion: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();

const sesion = ref({
  id: 0,
  dia: "",
  horaInicio: "",
  horaFin: "",
  duracion: 0,
  totalParticipantes: 0,
  presentes: 0,
  actividad: {
    nombre: "",
    periodo: "",
    terreno: "",
    nivel: "",
    instalacion: {
      id: 0,
      nombre: ""
    }
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
  } catch (e) {
    console.log("Error al guardar la asistencia de los usuarios", e)
  }
};

const filtro = ref<'todos' | 'presentes' | 'ausentes'>('todos');

const participantesFiltrados = computed(() => {
  if (filtro.value === 'presentes') {
    return sesion.value.participantes.filter(p => p.presente);
  }
  if (filtro.value === 'ausentes') {
    return sesion.value.participantes.filter(p => !p.presente);
  }
  return sesion.value.participantes;
  
});

const marcarTodos = (terreno: boolean) => {
  sesion.value.participantes.forEach(p => {
    p.presente = terreno;
  });
};

const volver = () => router.back();

onMounted(async () => {
  try {
    sesion.value = await getSesionDetalle(props.idAct, props.idSesion);
  } catch (e) {
    console.log("Error al obtener la informacion de la sesion", e)
  }
});
</script>

<style>
.avatar {
  width: 40px;
  height: 40px;
  background: #0d6efd;
  color: white;
  font-weight: bold;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.participant-card {
  transition: all 0.2s ease;
}

.participant-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}
</style>