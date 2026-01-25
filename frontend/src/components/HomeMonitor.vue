<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-4">
      <h1 class="text-center fs-2 fw-bold mb-4">{{ t.monitorHomeTitle }}</h1>
      <div class="row g-4">

        <div class="col-lg-12">
          <div class="card shadow-sm border-0 mb-4">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <router-link to="/notificaciones">
                  <h5 class="mb-0 d-flex align-items-center gap-2">
                    <i class="bi bi-bell-fill text-primary fs-4"></i>
                    {{ t.notifications }}
                    <span v-if="monitorStore.unreadCount > 0" class="badge bg-danger">
                      {{ monitorStore.unreadCount }}
                    </span>
                  </h5>
                </router-link>
              </div>

              <div class="row g-3">
                <div
                  v-for="notf in monitorStore.notificaciones"
                  :key="notf.id"
                  class="col-md-4"
                >
                  <div :class="['p-3 rounded shadow-sm', notf.leido ? 'bg-white' : 'bg-primary bg-opacity-10']">
                    <div class="d-flex justify-content-between mb-2">
                      <strong>{{ notf.titulo }}</strong>
                      <span class="text-muted small">{{ notf.fecha }}</span>
                    </div>
                    <p class="mb-0 text-muted small">{{ notf.descripcion }}</p>
                  </div>
                </div>
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
                <div v-for="day in actividadesSemanales" :key="day.id" class="col text-center">
                  <div class="border rounded p-2 bg-light h-100">
                    <div class="fw-semibold mb-2 border-bottom pb-1">{{ day.day }}</div>
                    <div v-if="day.activities.length === 0" class="text-muted small py-2">-</div>
                    <div v-else class="d-flex flex-column gap-2">
                      <button
                        v-for="act in day.activities"
                        :key="act.id"
                        class="btn btn-outline-primary btn-sm"
                        @click="activityDetail(act.id)"
                      >
                        {{ act.name }}
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
import { ref, inject, type Ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

import { useAuthStore } from '../stores/auth';
import { useMonitorStore } from '../stores/monitor';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const userStore = useAuthStore();
const monitorStore = useMonitorStore();
const router = useRouter();

const actividadesSemanales = ref([
  { id: 1, day: 'Lunes', activities: [{ id: 101, name: 'Natación' }, { id: 102, name: 'Musculación' }] },
  { id: 2, day: 'Martes', activities: [{ id: 103, name: 'Pádel' }] },
  { id: 3, day: 'Miércoles', activities: [{ id: 104, name: 'Yoga' }, { id: 105, name: 'CrossFit' }] },
  { id: 4, day: 'Jueves', activities: [] },
  { id: 5, day: 'Viernes', activities: [{ id: 106, name: 'Natación' }] },
  { id: 6, day: 'Sábado', activities: [] },
  { id: 7, day: 'Domingo', activities: [] },
]);

const activityDetail = (id: number) => {
  router.push({
    name: 'detalle-actividad',
    params: { id }
  });
};

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
