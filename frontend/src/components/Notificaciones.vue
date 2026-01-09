<template>
  <div class="min-vh-100 bg-light">
    <div class="container py-5">
      <h2 class="text-center mb-2 fw-semibold">
        <i class="bi bi-bell-fill text-primary fs-4 me-3"></i>
        {{ t.notifications }}
      </h2>
      <p class="text-center text-muted fs-5 mb-4">
        {{ t.notSubtitle }}
      </p>

      <p v-if="sortedNotifications.length === 0" class="text-center text-muted">
        {{ t.empty }}
      </p>

      <div class="d-flex flex-column gap-3">
        <div
          v-for="notif in sortedNotifications"
          :key="notif.id"
          class="card rounded-4 shadow-sm"
          :class="notif.leido ? 'bg-white' : 'bg-primary bg-opacity-10'"
        >
          <div class="card-body py-3 px-4">
            <div class="d-flex justify-content-between align-items-start">

              <div class="d-flex gap-3 w-100">
                <div
                  v-if="!notif.leido"
                  class="rounded-circle bg-primary mt-1"
                  style="width: 10px; height: 10px;"
                ></div>

                <div>
                  <h6 class="fw-semibold mb-1">
                    {{ notif.titulo }}
                  </h6>
                  <p class="text-muted mb-1">
                    {{ notif.descripcion }}
                  </p>
                  <small class="text-muted">
                    {{ notif.fecha }}
                  </small>
                </div>
              </div>

              <div class="d-flex gap-1 ms-3">
                <button
                  class="btn btn-sm btn-light rounded-circle"
                  @click="togglePin(notif.id)"
                  :title="notif.fijado ? t.unpin : t.pin"
                >
                  <i v-if="notif.fijado" class="bi bi-pin text-primary fs-4"></i>
                  <i v-else class="bi bi-pin-fill text-primary fs-4"></i>
                </button>

                <button
                  class="btn btn-sm btn-light rounded-circle"
                  @click="markRead(notif.id, !notif.leido)"
                  :title="notif.leido ? t.markUnread : t.markRead"
                >
                  <i v-if="notif.leido" class="bi bi-envelope-open text-primary fs-4"></i>
                  <i v-else class="bi bi-envelope text-primary fs-4"></i>
                </button>

                <button
                  class="btn btn-sm btn-light rounded-circle"
                  @click="deleteNotif(notif.id)"
                  :title="t.delete"
                >
                  <i class="bi bi-trash fs-4 text-danger" title="Eliminar notificación"></i>
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
import { inject, type Ref, ref, computed, onMounted } from "vue";
import { onBeforeRouteLeave } from 'vue-router'

/* Importamos las comunicaciones con el backend para obtener, editar o guardar las notificaciones*/
import { getNotificaciones, guardarNotificaciones, borrarNotificaciones } from "../services/usuarioService";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const cambiosPendientes = ref(false)

const markRead = (id: number, value: boolean) => {
  notificaciones.value.notificaciones = notificaciones.value.notificaciones.map(n =>
    n.id === id ? { ...n, leido: value } : n
  );

  cambiosPendientes.value = true
};

const togglePin = (id: number) => {
  notificaciones.value.notificaciones = notificaciones.value.notificaciones.map(n =>
    n.id === id ? { ...n, fijado: !n.fijado } : n
  );

  cambiosPendientes.value = true
};

const deleteNotif = async (id: number) => {
  notificaciones.value.notificaciones = notificaciones.value.notificaciones.filter(n => n.id !== id);

  await borrarNotificaciones(id)
};

const sortedNotifications = computed(() => [
  ...notificaciones.value.notificaciones.filter(n => n.fijado),
  ...notificaciones.value.notificaciones.filter(n => !n.fijado),
]);

export type Notificacion = {
  id: number
  titulo: string
  descripcion: string
  leido: boolean
  fijado: boolean
  fecha: string
  hora: string
  actividad: number | null
  instalacion: number | null
  pabellon: number | null
}

export type NotificacionesResponse = {
  notificaciones: Notificacion[]
  no_leidas: number
}

const notificaciones = ref<NotificacionesResponse>({
  notificaciones: [],
  no_leidas: 0
});

onBeforeRouteLeave(async (to, from) => {
  if (from.path === '/notificaciones' && cambiosPendientes.value) {
    try {
      await guardarNotificaciones({
        notificaciones: notificaciones.value.notificaciones.map(n => ({
          id: n.id,
          leido: n.leido,
          fijado: n.fijado
        }))
      })
      cambiosPendientes.value = false
    } catch (e) {
      console.error('Error guardando notificaciones:', e)
    }
  }
})

onMounted(async () => {
  const data = await getNotificaciones();

  notificaciones.value.notificaciones = data.notificaciones;
  notificaciones.value.no_leidas = data.no_leidas;
})
</script>
