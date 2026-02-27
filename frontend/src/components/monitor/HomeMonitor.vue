<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-4">
      <h1 class="text-center fs-2 fw-bold mb-4">{{ t.monitorHomeTitle }} {{ monitorStore.monitor?.nombre }}</h1>
      <div class="row g-4">

        <!-- Notificaciones -->
        <div class="col-lg-8">
          <div class="card shadow-sm h-100 bg-white bg-opacity-10 border border-white border-opacity-25">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <router-link to="/notificaciones"
                  class="d-flex align-items-center gap-2 text-decoration-none text-white">
                  <i class="bi bi-bell-fill text-primary fs-4"></i>

                  <h5 class="mb-0 text-white">
                    {{ t.notifications }}
                  </h5>

                  <span v-if="monitorStore.unreadCount > 0" class="badge bg-danger">
                    {{ monitorStore.unreadCount }}
                  </span>
                </router-link>
              </div>

              <div v-if="monitorStore.notificaciones.length === 0"
                class="d-flex flex-column justify-content-center align-items-center py-5 text-center">
                <i class="bi bi-bell-slash text-white fs-1 mb-3"></i>
                <p class="text-white opacity-75 fs-5 mb-0">
                  {{ t.noNotificacions }}
                </p>
              </div>
              <div v-else v-for="notf in monitorStore.notificaciones" :key="notf.id" class="rounded p-3 mb-2"
                :class="notf.leido ? 'bg-white bg-opacity-10 text-white' : 'bg-primary bg-opacity-20 text-white'">
                <strong>{{ notf.titulo }}</strong>
                <p class="mb-0 small text-white text-opacity-75">
                  {{ notf.descripcion }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-12">
          <div class="card shadow-sm border-0">
            <div class="card-body">
              <h5 class="mb-3 d-flex align-items-center gap-2">
                <i class="bi bi-calendar text-primary fs-4"></i>
                {{ t.weeklyActivities }}
              </h5>

              <div class="row g-3">
                <div v-for="dia in diasOrdenados" :key="dia" class="col-md-3">
                  <div class="border rounded p-2 bg-light h-100">
                    <div class="text-capitalize fw-semibold mb-2 border-bottom pb-1">
                      {{ dia }}
                    </div>

                    <div v-if="sesionesPorDia[dia].length === 0" class="text-muted small py-2">
                      -
                    </div>

                    <div v-else class="d-flex flex-column gap-2">
                      <button v-for="sesion in sesionesPorDia[dia]" :key="sesion.idSesion"
                        class="btn btn-outline-primary btn-sm" @click="sesionDetail(sesion.idActividad, sesion.idSesion)">
                        {{ sesion.nombre }}
                        <small class="d-block text-muted">
                          {{ sesion.horaInicio }} - {{ sesion.horaFin }}
                        </small>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, inject, type Ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

import { useAuthStore } from '@/stores/auth';
import { useMonitorStore } from '@/stores/monitor';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const userStore = useAuthStore();
const monitorStore = useMonitorStore();
const router = useRouter();

export interface Sesion {
  idActividad: number;
  idSesion: number;
  nombre: string;
  dia: string;
  horaInicio: string;
  horaFin: string;
}

const sesionDetail = (idAct: number, idSesion: number) => {
  router.push({
    name: 'detalle-sesion',
    params: { idAct, idSesion }
  });
};

const diasOrdenados = [
  t.value.monday,
  t.value.tuesday,
  t.value.wednesday,
  t.value.thursday,
  t.value.friday,
  t.value.saturday,
  t.value.sunday
]

const sesionesPorDia = computed(() => {
  const map: Record<string, Sesion[]> = {}

  diasOrdenados.forEach(dia => {
    map[dia] = []
  })

  monitorStore.sesiones.forEach(sesion => {
    if (map[sesion.dia]) {
      map[sesion.dia].push(sesion)
    }
  })

  Object.keys(map).forEach(dia => {
    map[dia].sort((a, b) =>
      a.horaInicio.localeCompare(b.horaInicio)
    )
  })

  return map
})

onMounted(async () => {
  if (!monitorStore.monitor) {
    await monitorStore.fetchUser(userStore.user?.monitor_id);
  }
  if (monitorStore.notificaciones.length === 0) {
    await monitorStore.fetchNotificaciones();
  }

  monitorStore.comenzarIntervalo();
});
</script>

<style scoped>
.card {
  border-radius: 1rem;
}
</style>
