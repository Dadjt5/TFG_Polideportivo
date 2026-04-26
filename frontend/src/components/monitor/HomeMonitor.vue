<template>
  <div class="min-vh-100 bg-light">

    <!-- Fondo con overlay oscuro -->
    <div class="position-absolute top-0 start-0 w-100 h-100" style="
        background:
          linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
          url('/images/Polideportivo.jpg') center/cover no-repeat;
      "></div>

    <main class="container py-4">
      <h1 class="text-center text-white fs-2 fw-bold mb-4">{{ t.monitorHomeTitle }} {{ monitorStore.monitor?.nombre }}
      </h1>
      <div class="row g-4">

        <!-- Notificaciones -->
        <div class="col-lg-12">
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

              <div v-if="monitorStore.sortedNotifications.length === 0"
                class="d-flex flex-column justify-content-center align-items-center py-5 text-center">
                <i class="bi bi-bell-slash text-white fs-1 mb-3"></i>
                <p class="text-white opacity-75 fs-5 mb-0">
                  {{ t.noNotificacions }}
                </p>
              </div>
              <div v-else v-for="notf in monitorStore.sortedNotifications.slice(0, 3)" :key="notf.id" class="rounded p-3 mb-2"
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
          <div class="card shadow-sm mb-3 bg-white bg-opacity-10 border border-white border-opacity-25">
            <div class="card-body">
              <h5 class="mb-3 d-flex align-items-center text-white gap-2">
                <i class="bi bi-calendar-fill text-primary fs-4"></i>
                {{ t.weeklyActivities }}
              </h5>

              <div class="row g-3">
                <div v-for="dia in diasOrdenados" :key="dia" class="col-md-3">
                  <div
                    class="card h-100 shadow-sm bg-white bg-opacity-10 border border-white border-opacity-25 rounded-3 p-3"
                    style="backdrop-filter: blur(10px);">
                    <!-- Header del día -->
                    <div class="text-capitalize text-white fw-semibold mb-3 border-bottom pb-2">
                      {{ dia }}
                    </div>

                    <!-- Si no hay sesiones -->
                    <div v-if="sesionesPorDia[dia].length === 0" class="text-light small py-2">
                      -
                    </div>

                    <!-- Lista de sesiones -->
                    <div v-else class="d-flex flex-column gap-2">
                      <button v-for="sesion in sesionesPorDia[dia]" :key="sesion.idSesion"
                        class="btn btn-outline-primary btn-sm text-start text-light"
                        @click="sesionDetail(sesion.idActividad, sesion.idSesion)">
                        {{ sesion.nombre }}
                        <small class="d-block text-light">
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

const DIA_KEY: Record<string, string> = {
  // Diccionario de traducción, porque del backend siempre viene en espanol
  "Lunes": "monday", "Martes": "tuesday", "Miércoles": "wednesday",
  "Jueves": "thursday", "Viernes": "friday", "Sábado": "saturday", "Domingo": "sunday",
}

const DIAS_KEYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

const diasOrdenados = computed(() =>
  DIAS_KEYS.map(key => t.value[key])
)

const sesionesPorDia = computed(() => {
  const map: Record<string, Sesion[]> = {}

  // Las keys del map son las traducciones actuales
  DIAS_KEYS.forEach(key => {
    map[t.value[key]] = []
  })

  monitorStore.sesiones.forEach(sesion => {
    const key = DIA_KEY[sesion.dia]
    const diaTraducido = key ? t.value[key] : null
    if (diaTraducido && map[diaTraducido] !== undefined) {
      map[diaTraducido].push(sesion)
    }
  })

  DIAS_KEYS.forEach(key => {
    map[t.value[key]].sort((a, b) => a.horaInicio.localeCompare(b.horaInicio))
  })

  return map
})

onMounted(async () => {
  if (!monitorStore.monitor) {
    await monitorStore.fetchUser(userStore.user?.monitor_id);
  }

  await monitorStore.fetchNotificaciones();
  monitorStore.comenzarIntervalo();
});
</script>

<style scoped>
.home-background {
  background-image: url('/images/Polideportivo.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.card {
  border-radius: 1rem;
}
</style>
