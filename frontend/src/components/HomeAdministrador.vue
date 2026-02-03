<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-4">
      <h1 class="text-center fs-2 fw-bold mb-5">{{ t.dashboardAdmin }}</h1>

       <div class="col-lg-12">
          <div class="card shadow-sm border-0 mb-4">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <router-link to="/notificaciones"
                  class="d-flex align-items-center gap-2 text-decoration-none text-dark">
                  <i class="bi bi-bell-fill text-primary fs-4"></i>

                  <h5 class="mb-0 text-primary">
                    {{ t.notifications }}
                  </h5>

                  <span v-if="administradorStore.unreadCount > 0" class="badge bg-danger">
                    {{ administradorStore.unreadCount }}
                  </span>
                </router-link>
              </div>

              <div v-for="notf in administradorStore.notificaciones" :key="notf.id" class="rounded p-3 mb-2"
                :class="notf.leido ? 'bg-white' : 'bg-primary bg-opacity-10'">
                <strong>{{ notf.titulo }}</strong>
                <p class="mb-0 small text-muted">
                  {{ notf.descripcion }}
                </p>
              </div>
            </div>
          </div>
        </div>

      <!-- Acciones rápidas -->
      <div class="row g-4">
        <div
          v-for="action in quickActions"
          :key="action.id"
          class="col-12 col-sm-6 col-lg-4"
        >
          <div
            class="card shadow-sm border-0 p-4 d-flex align-items-center gap-3 cursor-pointer hover-shadow"
            @click="action.action"
          >
            <component :is="action.icon" class="fs-3 text-primary" />
            <span class="fw-medium">{{ action.label }}</span>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, type Ref, inject, reactive } from 'vue';
import { User, Calendar, Settings, BarChart, Wallet, Building } from 'lucide-vue-next';

import { useAuthStore } from '../stores/auth';
import { useAdministradorStore } from '../stores/administrador';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const userStore = useAuthStore();
const administradorStore = useAdministradorStore();

const quickActions = reactive([
  { id: 1, label: t.value.manageUsers, icon: User, action: () => console.log("Gestionar usuarios") },
  { id: 2, label: t.value.manageSpaces, icon: Building, action: () => console.log("Gestionar espacios") },
  { id: 3, label: t.value.manageActivities, icon: Calendar, action: () => console.log("Gestionar actividades") },
  { id: 4, label: t.value.manageRates, icon: Wallet, action: () => console.log("Gestionar tarifas") },
  { id: 5, label: t.value.systemSettings, icon: Settings, action: () => console.log("Configuración avanzada") },
  { id: 6, label: t.value.reports, icon: BarChart, action: () => console.log("Ver informes y estadísticas") },
]);

onMounted(async () => {
  if (!administradorStore.administrador) {
    await administradorStore.fetchUser(userStore.user?.administrador_id);
  }
  if (administradorStore.notificaciones.length === 0) {
    await administradorStore.fetchNotificaciones();
  }

  administradorStore.comenzarIntervalo();
});
</script>

<style scoped>
.card.cursor-pointer {
  cursor: pointer;
}
.card.cursor-pointer:hover {
  box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.15);
  transition: 0.3s;
}
</style>
