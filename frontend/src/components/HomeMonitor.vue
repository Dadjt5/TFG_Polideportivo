<template>
  <div class="min-vh-100 bg-light">
    <!-- NAVBAR -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary sticky-top shadow-sm">
      <div class="container">
        <span class="navbar-brand fs-5 fw-bold">Polideportivo XX</span>

        <div class="d-flex align-items-center ms-auto gap-3">
          <button class="btn btn-light" @click="toggleLanguage" :title="language === 'es' ? 'Switch to English' : 'Cambiar a Español'">
            {{ language === 'es' ? '🇪🇸' : '🇬🇧' }}
          </button>
          <button class="btn btn-light" @click="logout">{{ t.logout }}</button>
          <button class="btn btn-light rounded-circle p-2">
            <User class="text-primary" />
          </button>
        </div>
      </div>
    </nav>

    <main class="container py-4">
      <h1 class="text-center fs-2 fw-bold mb-4">{{ t.dashboard }}</h1>

      <div class="row g-4">
        <!-- NOTIFICACIONES -->
        <div class="col-lg-12">
          <div class="card shadow-sm border-0 mb-4">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="mb-0 d-flex align-items-center gap-2">
                  <Bell class="text-primary fs-4" />
                  {{ t.notifications }}
                  <span v-if="usuarioFinalStore.unreadCount > 0" class="badge bg-danger">
                    {{ usuarioFinalStore.unreadCount }}
                  </span>
                </h5>
                <button class="btn btn-link text-primary" @click="verTodasNotificaciones">{{ t.seeAll }}</button>
              </div>

              <div class="row g-3">
                <div
                  v-for="notf in usuarioFinalStore.notificaciones"
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

        <!-- ACTIVIDADES DE LA SEMANA -->
        <div class="col-lg-12">
          <div class="card shadow-sm border-0">
            <div class="card-body">
              <h5 class="mb-3 d-flex align-items-center gap-2">
                <Calendar class="text-primary" /> {{ t.weeklyActivities }}
              </h5>

              <div class="row g-3">
                <div v-for="day in weeklyActivities" :key="day.id" class="col text-center">
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
import { ref, inject, type Ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { User, Bell, Calendar } from 'lucide-vue-next';
import { useAuthStore } from '../stores/auth';
import { useUserStore } from '../stores/usuarioFinal';
import { useI18n } from '../useI18N';

const language = ref('es');
const t = computed(() => {
  const translations = {
    es: {
      home: "Inicio", logout: "Logout", dashboard: "Panel principal de Laura",
      notifications: "Notificaciones", seeAll: "Ver todas", weeklyActivities: "Actividades de la semana"
    },
    en: {
      home: "Home", logout: "Logout", dashboard: "Monitor Dashboard",
      notifications: "Notifications", seeAll: "See all", weeklyActivities: "Weekly Activities"
    }
  };
  return translations[language.value];
});

const toggleLanguage = () => language.value = language.value === 'es' ? 'en' : 'es';
const logout = () => console.log("Logout"); // Implementa tu logout

const userStore = useAuthStore();
const usuarioFinalStore = useUserStore();
const router = useRouter();

const weeklyActivities = ref([
  { id: 1, day: 'Lunes', activities: [{ id: 101, name: 'Natación' }, { id: 102, name: 'Musculación' }] },
  { id: 2, day: 'Martes', activities: [{ id: 103, name: 'Pádel' }] },
  { id: 3, day: 'Miércoles', activities: [{ id: 104, name: 'Yoga' }, { id: 105, name: 'CrossFit' }] },
  { id: 4, day: 'Jueves', activities: [] },
  { id: 5, day: 'Viernes', activities: [{ id: 106, name: 'Natación' }] },
  { id: 6, day: 'Sábado', activities: [] },
  { id: 7, day: 'Domingo', activities: [] },
]);

const activityDetail = (id: number) => {
  router.push({ name: 'detalle-actividad', params: { id } });
};

const verTodasNotificaciones = () => {
  router.push('/notificaciones');
};

onMounted(async () => {
  if (!usuarioFinalStore.usuarioFinal) {
    await usuarioFinalStore.fetchUser(userStore.user?.usuario_final_id);
  }
  if (usuarioFinalStore.notificaciones.length === 0) {
    await usuarioFinalStore.fetchNotificaciones();
  }
});
</script>

<style scoped>
/* Ajustes finos */
.card {
  border-radius: 1rem;
}
</style>
