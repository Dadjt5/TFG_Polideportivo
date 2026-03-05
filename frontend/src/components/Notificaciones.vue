<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <div class="container py-5">

      <!-- Título -->
      <h2 class="text-center mb-5 fw-bold text-primary">
        <i class="bi bi-bell-fill fs-4 me-3"></i>
        {{ t.notifications }}
      </h2>

      <!-- Botón nueva notificación -->
      <div v-if="userStore.isAdmin" class="text-center mb-3">
        <router-link to="/notificaciones/nueva" class="btn btn-primary rounded-pill">
          <i class="bi bi-megaphone-fill me-2"></i>
          {{ t.newNotification }}
        </router-link>
      </div>

      <!-- Sin notificaciones -->
      <p v-if="activeStore.sortedNotifications.length === 0" class="text-center text-muted">
        {{ t.empty }}
      </p>

      <!-- Lista de notificaciones -->
      <div class="d-flex flex-column gap-3">
        <div v-for="notif in activeStore.sortedNotifications" :key="notif.id"
             class="card rounded-4 shadow-sm"
             :class="notif.leido ? 'bg-white' : 'bg-primary bg-opacity-10'"
             style="backdrop-filter: blur(6px);">
          <div class="card-body py-3 px-4">

            <div class="d-flex justify-content-between align-items-start">

              <!-- Contenido de la notificación -->
              <div class="d-flex gap-3 w-100">
                <div v-if="!notif.leido" class="rounded-circle bg-primary mt-1" 
                     style="width: 10px; height: 10px;"></div>

                <div>
                  <h6 class="fw-semibold mb-1 text-primary">
                    {{ notif.titulo }}
                  </h6>

                  <p class="text-secondary mb-2">
                    {{ notif.descripcion }}
                  </p>

                  <!-- Actividad asociada -->
                  <div v-if="notif.actividad" class="mb-2">
                    <small class="fw-semibold text-primary d-block">
                      {{ t.activity }}
                    </small>
                    <span class="fw-medium text-primary" style="cursor: pointer;"
                          @click="activityDetail(notif.actividad.id)">
                      {{ notif.actividad.nombre }}
                    </span>
                  </div>

                  <!-- Instalación asociada -->
                  <div v-if="notif.instalacion" class="mb-2">
                    <small class="fw-semibold text-success d-block">
                      {{ t.facility }}
                    </small>
                    <span class="fw-medium text-primary" style="cursor: pointer;"
                          @click="facilityDetail(notif.instalacion.id)">
                      {{ notif.instalacion.nombre }}
                    </span>
                  </div>

                  <!-- Pabellón asociado -->
                  <div v-if="notif.pabellon" class="mb-2">
                    <small class="fw-semibold text-warning d-block">
                      {{ t.pavilion }}
                    </small>
                    <span class="fw-medium text-primary" style="cursor: pointer;"
                          @click="pavilionDetail(notif.pabellon.id)">
                      {{ notif.pabellon.nombre }}
                    </span>
                  </div>

                  <small class="text-muted">
                    {{ notif.fecha }}
                  </small>
                </div>
              </div>

              <!-- Botones de acción -->
              <div class="d-flex gap-1 ms-3">
                <button class="btn btn-sm btn-light rounded-circle" @click="togglePin(notif.id)"
                        :title="notif.fijado ? t.unpin : t.pin">
                  <i v-if="notif.fijado" class="bi bi-pin text-primary fs-4"></i>
                  <i v-else class="bi bi-pin-fill text-primary fs-4"></i>
                </button>

                <button class="btn btn-sm btn-light rounded-circle" @click="markRead(notif.id)"
                        :title="notif.leido ? t.markUnread : t.markRead">
                  <i v-if="notif.leido" class="bi bi-envelope-open text-primary fs-4"></i>
                  <i v-else class="bi bi-envelope text-primary fs-4"></i>
                </button>

                <button class="btn btn-sm btn-light rounded-circle" @click="deleteNotif(notif.id)"
                        :title="t.delete">
                  <i class="bi bi-trash fs-4 text-danger"></i>
                </button>
              </div>

            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { inject, type Ref, onMounted, computed } from "vue";
import { onBeforeRouteLeave, useRouter } from 'vue-router'

/* Importamos el store del usuario para manejar las notificaciones */
import { useUserStore } from "@/stores/usuarioFinal";
import { useMonitorStore } from "@/stores/monitor";
import { useAdministradorStore } from "@/stores/administrador";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

import { useAuthStore } from "@/stores/auth";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const userStore = useAuthStore();
const usuarioFinalStore = useUserStore();
const monitorStore = useMonitorStore();
const administradorStore = useAdministradorStore();

const router = useRouter();

const markRead = (id: number) => activeStore.value.cambiarLeido(id);
const togglePin = (id: number) => activeStore.value.cambiarFijado(id);
const deleteNotif = (id: number) => activeStore.value.deleteNotificacion(id);


const activeStore = computed(() => {
  if (userStore.isUsuarioFinal) {
    return usuarioFinalStore;
  }

  if (userStore.isMonitor) {
    return monitorStore;
  }

  return administradorStore;
});

const activityDetail = (id: number) => {
  router.push({
    name: 'detalle-actividad',
    params: { id }
  });
}

const facilityDetail = (id: number) => {
  router.push({
    name: 'detalle-instalacion',
    params: { id }
  });
}

const pavilionDetail = (id: number) => {
  router.push({
    name: 'detalle-pabellon',
    params: { id }
  });
}

onBeforeRouteLeave(async () => {
  await activeStore.value.guardarCambios();
});

onMounted(async () => {
  if (!activeStore.value.notificaciones) {
    await activeStore.value.fetchNotificaciones();
  }
});
</script>
