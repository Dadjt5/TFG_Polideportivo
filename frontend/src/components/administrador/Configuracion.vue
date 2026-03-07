<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #e0f7ff, #ffffff);">
    <main class="container py-5" style="max-width: 1100px">

      <h2 class="text-center mb-4 fw-bold text-primary">
        {{ t.configurationTitle }}
      </h2>

      <!-- TABS -->
      <ul class="nav nav-tabs justify-content-center mb-4">
        <li class="nav-item">
          <button class="nav-link" :class="{ active: activeTab === 'params' }" @click="activeTab = 'params'">
            {{ t.tabParams }}
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="{ active: activeTab === 'notifs' }" @click="activeTab = 'notifs'">
            {{ t.tabNotifs }}
          </button>
        </li>
      </ul>

      <!-- PARÁMETROS -->
      <form v-if="activeTab === 'params'" @submit.prevent="guardarConfiguracion">
        <div class="row g-4">

          <!-- MAX DEPORTES POR USUARIO -->
          <div class="col-md-4">
            <div class="card h-100 shadow-lg rounded-4"
                 style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">
              <div class="card-body">
                <h5 class="card-title">{{ t.sportsMaxNumber }}</h5>
                <input type="number" class="form-control" v-model.number="configuracionStore.max_deportes_por_usuario" />
              </div>
            </div>
          </div>

          <!-- DIAS MINIMO RESERVA -->
          <div class="col-md-4">
            <div class="card h-100 shadow-lg rounded-4"
                 style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">
              <div class="card-body">
                <h5 class="card-title">{{ t.minDaysActivityReservation }}</h5>
                <input type="number" class="form-control" v-model.number="configuracionStore.dias_minimo_reserva_actividad" />
              </div>
            </div>
          </div>

          <!-- DIAS MAXIMO RESERVA -->
          <div class="col-md-4">
            <div class="card h-100 shadow-lg rounded-4"
                 style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">
              <div class="card-body">
                <h5 class="card-title">{{ t.maxDaysActivityReservation }}</h5>
                <input type="number" class="form-control" v-model.number="configuracionStore.dias_maximo_reserva_actividad" />
              </div>
            </div>
          </div>

          <!-- DIAS MAXIMO ALQUILER -->
          <div class="col-md-4">
            <div class="card h-100 shadow-lg rounded-4"
                 style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">
              <div class="card-body">
                <h5 class="card-title">{{ t.maxDaysFacilityReservation }}</h5>
                <input type="number" class="form-control" v-model.number="configuracionStore.dias_maximo_alquiler" />
              </div>
            </div>
          </div>

          <!-- DIAS MAXIMO ALQUILER -->
          <div class="col-md-4">
            <div class="card h-100 shadow-lg rounded-4"
                 style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">
              <div class="card-body">
                <h5 class="card-title">{{ t.consecutiveHours }}</h5>
                <input type="number" class="form-control" v-model.number="configuracionStore.horas_alquiler_consecutivas" />
              </div>
            </div>
          </div>

          <!-- DIAS MINIMO CANCELACION -->
          <div class="col-md-4">
            <div class="card h-100 shadow-lg rounded-4"
                 style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">
              <div class="card-body">
                <h5 class="card-title">{{ t.minCancellationDays }}</h5>
                <input type="number" class="form-control" v-model.number="configuracionStore.dias_minimo_cancelacion" />
              </div>
            </div>
          </div>

          <!-- HORAS PREVIAS NOTIFICACION -->
          <div class="col-md-4">
            <div class="card h-100 shadow-lg rounded-4"
                 style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">
              <div class="card-body">
                <h5 class="card-title">{{ t.previousNotificationHours }}</h5>
                <input type="number" class="form-control" v-model.number="configuracionStore.horas_previas_notificacion" />
              </div>
            </div>
          </div>

          <!-- PORCENTAJE MAXIMO -->
          <div class="col-md-4">
            <div class="card h-100 shadow-lg rounded-4"
                 style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">
              <div class="card-body">
                <h5 class="card-title">{{ t.maxPercentage }}</h5>
                <input type="number" class="form-control" v-model.number="configuracionStore.porcentaje_maximo" />
              </div>
            </div>
          </div>

        </div>
      </form>


      <!-- NOTIFICACIONES -->
      <div v-if="activeTab === 'notifs'" class="card shadow-lg rounded-4"
           style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">
        <div class="card-body">
          <h4 class="mb-4">{{ t.notificationTitle }}</h4>

          <!-- CAMBIOS Y CANCELACIONES -->
          <div class="mb-4">
            <label class="form-label fw-semibold">{{ t.title }} - {{ t.textChangesCancellations }}</label>
            <input type="text" class="form-control mb-2"
              v-model="configuracionStore.titulo_cambios_cancelaciones" />

            <label class="form-label fw-semibold">{{ t.textChangesCancellations }}</label>
            <textarea class="form-control" rows="3"
              v-model="configuracionStore.texto_cambios_cancelaciones" />
          </div>

          <!-- AVISOS ACTIVIDADES -->
          <div class="mb-4">
            <label class="form-label fw-semibold">{{ t.title }} - {{ t.textActivityNotices }}</label>
            <input type="text" class="form-control mb-2"
              v-model="configuracionStore.titulo_avisos_actividades" />

            <label class="form-label fw-semibold">{{ t.textActivityNotices }}</label>
            <textarea class="form-control" rows="3"
              v-model="configuracionStore.texto_avisos_actividades" />
          </div>

          <!-- PROBLEMAS PAGO -->
          <div class="mb-4">
            <label class="form-label fw-semibold">{{ t.title }} - {{ t.textPaymentProblems }}</label>
            <input type="text" class="form-control mb-2"
              v-model="configuracionStore.titulo_problemas_pago" />

            <label class="form-label fw-semibold">{{ t.textPaymentProblems }}</label>
            <textarea class="form-control" rows="3"
              v-model="configuracionStore.texto_problemas_pago" />
          </div>

          <!-- SALIDA LISTA ESPERA -->
          <div class="mb-4">
            <label class="form-label fw-semibold">{{ t.title }} - {{ t.textWaitingListExit }}</label>
            <input type="text" class="form-control mb-2"
              v-model="configuracionStore.titulo_salida_lista_espera" />

            <label class="form-label fw-semibold">{{ t.textWaitingListExit }}</label>
            <textarea class="form-control" rows="3"
              v-model="configuracionStore.texto_salida_lista_espera" />
          </div>

          <!-- AUSENCIAS -->
          <div class="mb-4">
            <label class="form-label fw-semibold">{{ t.title }} - {{ t.textAbsences }}</label>
            <input type="text" class="form-control mb-2"
              v-model="configuracionStore.titulo_ausencias" />

            <label class="form-label fw-semibold">{{ t.textAbsences }}</label>
            <textarea class="form-control" rows="3"
              v-model="configuracionStore.texto_ausencias" />
          </div>

          <!-- MATERIAL ESPECIAL -->
          <div class="mb-4">
            <label class="form-label fw-semibold">{{ t.title }} - {{ t.textSpecialMaterial }}</label>
            <input type="text" class="form-control mb-2"
              v-model="configuracionStore.titulo_material_especial" />

            <label class="form-label fw-semibold">{{ t.textSpecialMaterial }}</label>
            <textarea class="form-control" rows="3"
              v-model="configuracionStore.texto_material_especial" />
          </div>

        </div>
      </div>

      <div class="text-center mt-4">
        <button class="fs-4 btn btn-primary rounded-pill px-4 mt-4" @click="guardarConfiguracion">
          {{ t.save }}
        </button>
      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { type Ref, ref, inject, onMounted } from "vue";

import { useConfiguracionStore } from "@/stores/configuracion";

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const configuracionStore = useConfiguracionStore();
const activeTab = ref<"params" | "notifs">("params");

const guardarConfiguracion = async () => {
  configuracionStore.editarConfiguracion()
};

onMounted(async () => {
  if (!configuracionStore.modificado) {
    configuracionStore.obtenerConfiguracion()
  }
});
</script>
