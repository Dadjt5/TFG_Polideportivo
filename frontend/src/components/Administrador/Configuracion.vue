<template>
  <div class="container-fluid py-4">
    <h2 class="text-center mb-4">
      {{ t.configurationTitle }}
    </h2>

    <!-- TABS -->
    <ul class="nav nav-tabs justify-content-center mb-4">
      <li class="nav-item">
        <button
          class="nav-link"
          :class="{ active: activeTab === 'params' }"
          @click="activeTab = 'params'"
        >
          {{ t.tabParams }}
        </button>
      </li>
      <li class="nav-item">
        <button
          class="nav-link"
          :class="{ active: activeTab === 'notifs' }"
          @click="activeTab = 'notifs'"
        >
          {{ t.tabNotifs }}
        </button>
      </li>
    </ul>

    <!-- PARÁMETROS -->
    <form v-if="activeTab === 'params'" @submit.prevent="guardarParametros">
      <div class="row g-4">
        <div class="col-md-4" v-for="param in parametros" :key="param.key">
          <div class="card h-100 shadow-sm">
            <div class="card-body">
              <h5 class="card-title">{{ param.label }}</h5>

              <div v-if="param.range" class="d-flex gap-2">
                <input
                  type="number"
                  class="form-control"
                  :placeholder="'min'"
                  v-model.number="config[param.key].min"
                />
                <input
                  type="number"
                  class="form-control"
                  :placeholder="'max'"
                  v-model.number="config[param.key].max"
                />
              </div>

              <input
                v-else
                type="number"
                class="form-control"
                v-model.number="config[param.key]"
              />
            </div>
          </div>
        </div>
      </div>

      <div class="text-end mt-4">
        <button class="btn btn-primary px-4">
          {{ t.save }}
        </button>
      </div>
    </form>

    <!-- NOTIFICACIONES -->
    <div v-if="activeTab === 'notifs'" class="card shadow-sm">
      <div class="card-body">
        <h4 class="mb-3">{{ t.notificationTitle }}</h4>

        <div class="accordion" id="accordionNotifs">
          <div
            class="accordion-item"
            v-for="(value, key) in notifications"
            :key="key"
          >
            <h2 class="accordion-header">
              <button
                class="accordion-button collapsed"
                type="button"
                data-bs-toggle="collapse"
                :data-bs-target="'#notif-' + key"
              >
                {{ t[key] }}
              </button>
            </h2>

            <div
              :id="'notif-' + key"
              class="accordion-collapse collapse"
              data-bs-parent="#accordionNotifs"
            >
              <div class="accordion-body">
                <textarea
                  class="form-control"
                  rows="3"
                  v-model="notifications[key]"
                  :placeholder="t.configurationPlaceholder"
                />
              </div>
            </div>
          </div>
        </div>

        <div class="text-end mt-4">
          <button class="btn btn-primary px-4" @click="guardarNotificaciones">
            {{ t.save }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { type Ref, ref, inject, onMounted } from "vue";

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const activeTab = ref<"params" | "notifs">("params");

/* CONFIGURACIÓN */
const config = ref({
  cancelacionDias: 0,
  deportesFavoritosMax: 0,
  ventanaReserva: { min: 0, max: 0 },
  antelacionNotificaciones: 0,
  decisionMaxDias: 0,
});

const parametros = [
  { key: "cancelacionDias", label: "Tiempo cancelación actividad (días)" },
  { key: "deportesFavoritosMax", label: "Deportes favoritos (máx.)" },
  {
    key: "ventanaReserva",
    label: "Ventana reserva (horas)",
    range: true,
  },
  {
    key: "antelacionNotificaciones",
    label: "Antelación notificaciones (horas)",
  },
  {
    key: "decisionMaxDias",
    label: "Tiempo máximo para decidir (días)",
  },
];

const notifications = ref({
  rfc2: "",
  rfc3: "",
  rfc4: "",
  rfc5: "",
  rfc6: "",
  rfc8: "",
});

const guardarParametros = () => {
  console.log("Guardar parámetros", config.value);
};

const guardarNotificaciones = () => {
  console.log("Guardar notificaciones", notifications.value);
};
</script>
