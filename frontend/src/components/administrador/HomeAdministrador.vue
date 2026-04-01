<template>
  <div class="min-vh-100 bg-light">

    <!-- Fondo con overlay oscuro -->
    <div class="position-absolute top-0 start-0 w-100 h-100" style="
        background:
          linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
          url('/images/Polideportivo.jpg') center/cover no-repeat;
      "></div>

    <main class="container py-4">
      <h1 class="text-center text-white fs-2 fw-bold mb-5">{{ t.monitorHomeTitle }} {{ administradorStore.administrador?.nombre }}</h1>

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

                  <span v-if="administradorStore.unreadCount > 0" class="badge bg-danger">
                    {{ administradorStore.unreadCount }}
                  </span>
                </router-link>
              </div>

              <div v-if="administradorStore.notificaciones.length === 0"
                class="d-flex flex-column justify-content-center align-items-center py-5 text-center">
                <i class="bi bi-bell-slash text-white fs-1 mb-3"></i>
                <p class="text-white opacity-75 fs-5 mb-0">
                  {{ t.noNotificacions }}
                </p>
              </div>
              <div v-else v-for="notf in administradorStore.notificaciones" :key="notf.id" class="rounded p-3 mb-2"
                :class="notf.leido ? 'bg-white bg-opacity-10 text-white' : 'bg-primary bg-opacity-20 text-white'">
                <strong>{{ notf.titulo }}</strong>
                <p class="mb-0 small text-white text-opacity-75">
                  {{ notf.descripcion }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Acciones rápidas -->
      <div class="row g-4 mt-4">
        <div class="col-md-6" v-if="userStore.isAdminRaiz || userStore.isAdminUsuarios">
          <router-link to="/gestion/usuarios" class="text-decoration-none text-dark">
            <div class="card shadow-sm mb-3 bg-white bg-opacity-10 border border-white border-opacity-25">
              <div class="card-body">
                <div class="d-flex align-items-center gap-3">
                  <i class="bi bi-person-fill text-primary fs-3"></i>
                  <div>
                    <h6 class="mb-1 text-white">{{ t.manageUsers }}</h6>
                  </div>
                </div>
              </div>
            </div>
          </router-link>
        </div>

        <div class="col-md-6" v-if="userStore.isAdminRaiz || userStore.isAdminEspacios">
          <router-link to="/gestion/espacios" class="text-decoration-none text-dark">
            <div class="card shadow-sm mb-3 bg-white bg-opacity-10 border border-white border-opacity-25">
              <div class="card-body">
                <div class="d-flex align-items-center gap-3">
                  <i class="bi bi-building-fill text-primary fs-3"></i>
                  <div>
                    <h6 class="mb-1 text-white">{{ t.manageSpaces }}</h6>
                  </div>
                </div>
              </div>
            </div>
          </router-link>
        </div>

        <div class="col-md-6" v-if="userStore.isAdminRaiz || userStore.isAdminEspacios">
          <router-link to="/gestion/actividades" class="text-decoration-none text-dark">
            <div class="card shadow-sm mb-3 bg-white bg-opacity-10 border border-white border-opacity-25">
              <div class="card-body">
                <div class="d-flex align-items-center gap-3">
                  <i class="bi bi-activity text-primary fs-3"></i>
                  <div>
                    <h6 class="mb-1 text-white">{{ t.manageActivities }}</h6>
                  </div>
                </div>
              </div>
            </div>
          </router-link>
        </div>

        <div class="col-md-6" v-if="userStore.isAdminRaiz || userStore.isAdminTarifas">
          <router-link to="/gestion/tarifas" class="text-decoration-none text-dark">
            <div class="card shadow-sm mb-3 bg-white bg-opacity-10 border border-white border-opacity-25">
              <div class="card-body">
                <div class="d-flex align-items-center gap-3">
                  <i class="bi bi-ticket-fill text-primary fs-3"></i>
                  <div>
                    <h6 class="mb-1 text-white">{{ t.manageRates }}</h6>
                  </div>
                </div>
              </div>
            </div>
          </router-link>
        </div>

        <div class="col-md-6" v-if="userStore.isAdminRaiz || userStore.isAdminRaiz">
          <router-link to="/configuracion" class="text-decoration-none text-dark">
            <div class="card shadow-sm mb-3 bg-white bg-opacity-10 border border-white border-opacity-25">
              <div class="card-body">
                <div class="d-flex align-items-center gap-3">
                  <i class="bi bi-nut-fill text-primary fs-3"></i>
                  <div>
                    <h6 class="mb-1 text-white">{{ t.systemSettings }}</h6>
                  </div>
                </div>
              </div>
            </div>
          </router-link>
        </div>

        <div class="col-md-6">
          <router-link to="/estadisticas/administrador" class="text-decoration-none text-dark">
            <div class="card shadow-sm mb-3 bg-white bg-opacity-10 border border-white border-opacity-25">
              <div class="card-body">
                <div class="d-flex align-items-center gap-3">
                  <i class="bi bi-bar-chart-fill text-primary fs-3"></i>
                  <div>
                    <h6 class="mb-1 text-white">{{ t.reports }}</h6>
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

import { useAuthStore } from '@/stores/auth';
import { useAdministradorStore } from '@/stores/administrador';
import { useTiposStore } from '@/stores/tipos';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const userStore = useAuthStore();
const administradorStore = useAdministradorStore();
const tiposStore = useTiposStore();

onMounted(async () => {
  if (!administradorStore.administrador) {
    await administradorStore.fetchUser(userStore.user?.administrador_id);
  }

  if (!tiposStore.modificado) {
    tiposStore.obtenerTipos();
  }

  await administradorStore.fetchNotificaciones();
  administradorStore.comenzarIntervalo();
});
</script>


<style scoped>
.home-background {
  background-image: url('/images/Polideportivo.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.card.cursor-pointer {
  cursor: pointer;
}

.card.cursor-pointer:hover {
  box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.15);
  transition: 0.3s;
}
</style>
