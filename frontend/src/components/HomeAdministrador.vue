<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-4">
      <h1 class="text-center fs-2 fw-bold mb-5">{{ t.monitorHomeTitle }} {{ administradorStore.administrador?.nombre }}</h1>

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
        <div class="col-md-6">
          <router-link to="/gestion/usuarios" class="text-decoration-none text-dark">
            <div class="card shadow-sm h-100 option-card">
              <div class="card-body">
                <div class="d-flex align-items-center gap-3">
                  <i class="bi bi-person-fill text-primary fs-3"></i>
                  <div>
                    <h6 class="mb-1">{{ t.manageUsers }}</h6>
                  </div>
                </div>
              </div>
            </div>
          </router-link>
        </div>

        <div class="col-md-6">
          <router-link to="/gestion/espacios" class="text-decoration-none text-dark">
            <div class="card shadow-sm h-100 option-card">
              <div class="card-body">
                <div class="d-flex align-items-center gap-3">
                  <i class="bi bi-building text-primary fs-3"></i>
                  <div>
                    <h6 class="mb-1">{{ t.manageSpaces }}</h6>
                  </div>
                </div>
              </div>
            </div>
          </router-link>
        </div>

        <div class="col-md-6">
          <router-link to="/gestion/actividades" class="text-decoration-none text-dark">
            <div class="card shadow-sm h-100 option-card">
              <div class="card-body">
                <div class="d-flex align-items-center gap-3">
                  <i class="bi bi-activity text-primary fs-3"></i>
                  <div>
                    <h6 class="mb-1">{{ t.manageActivities }}</h6>
                  </div>
                </div>
              </div>
            </div>
          </router-link>
        </div>

        <div class="col-md-6">
          <router-link to="/gestion/tarifas" class="text-decoration-none text-dark">
            <div class="card shadow-sm h-100 option-card">
              <div class="card-body">
                <div class="d-flex align-items-center gap-3">
                  <i class="bi bi-ticket-perforated text-primary fs-3"></i>
                  <div>
                    <h6 class="mb-1">{{ t.manageRates }}</h6>
                  </div>
                </div>
              </div>
            </div>
          </router-link>
        </div>

        <div class="col-md-6">
          <router-link to="/configuracion/administrador" class="text-decoration-none text-dark">
            <div class="card shadow-sm h-100 option-card">
              <div class="card-body">
                <div class="d-flex align-items-center gap-3">
                  <i class="bi bi-nut text-primary fs-3"></i>
                  <div>
                    <h6 class="mb-1">{{ t.systemSettings }}</h6>
                  </div>
                </div>
              </div>
            </div>
          </router-link>
        </div>

        <div class="col-md-6">
          <router-link to="/estadisticas/administrador" class="text-decoration-none text-dark">
            <div class="card shadow-sm h-100 option-card">
              <div class="card-body">
                <div class="d-flex align-items-center gap-3">
                  <i class="bi bi-bar-chart-fill text-primary fs-3"></i>
                  <div>
                    <h6 class="mb-1">{{ t.reports }}</h6>
                  </div>
                </div>
              </div>
            </div>
          </router-link>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, type Ref, inject } from 'vue';

import { useAuthStore } from '../stores/auth';
import { useAdministradorStore } from '../stores/administrador';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const userStore = useAuthStore();
const administradorStore = useAdministradorStore();

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
