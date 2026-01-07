<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-4">

      <h1 class="text-center fw-bold mb-4">
        {{ t.welcome }}
      </h1>

      <div class="row g-4 mb-5">
        <div class="col-lg-8">
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <div class="d-flex align-items-center gap-2">
                  <i class="bi bi-bell-fill text-primary me-2 fs-4"></i>
                  <h5 class="mb-0">{{ t.notifications }}</h5>
                  <span v-if="notificaciones.no_leidas"
                        class="badge bg-danger">
                    {{ notificaciones.no_leidas }}
                  </span>
                </div>
                <a href="#" class="text-primary small">
                  {{ t.viewAll }} →
                </a>
              </div>

              <div
                v-for="notf in notificaciones.notificaciones"
                  :key="notf.id"
                  class="bg-light rounded p-3 mb-2"
                >
                <strong>{{ notf.titulo }}</strong>
                <p class="mb-0 small text-muted">
                  {{ notf.descripcion }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-4">
          <div class="card shadow-sm mb-3">
            <div class="card-body">
              <div class="d-flex align-items-center gap-2 mb-2">
                <i class="bi bi-bar-chart-fill text-primary me-2 fs-4"></i>
                <h6 class="mb-0">{{ t.userStats }}</h6>
              </div>
              <button class="btn btn-primary w-100">
                {{ t.viewUserStats }}
              </button>
            </div>
          </div>

          <div class="card shadow-sm">
            <div class="card-body">
              <div class="d-flex align-items-center gap-2 mb-2">
                <i class="bi bi-calendar-fill text-primary me-2 fs-4"></i>
                <h6 class="mb-0">{{ t.bookingsMade }}</h6>
              </div>
              <button class="btn btn-success w-100">
                {{ t.viewBooks }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="linea-fina"></div>

      <!-- BUSQUEDAS -->
      <div class="container-fluid mt-5 mb-4">
        <div class="d-flex align-items-center bg-white rounded-3 shadow p-3 border gap-3">
          <input
            type="text"
            v-model="textoBusqueda"
            class="form-control border-0 fs-5"
            :placeholder="t.searchPlaceholder"
            @keyup.enter="buscar"
          />

          <button class="btn btn-primary btn-lg px-4"  @click="buscar">
            {{ t.searchButton }}
          </button>
        </div>
      </div>

      <!-- FILTROS -->
      <h2 class="fs-3 fw-semibold text-center text-dark mb-4">
        {{ t.filterBy }}
      </h2>

      <!-- TABS -->
      <ul class="nav nav-tabs justify-content-center mb-4">
        <li class="nav-item fs-5">
          <button
            class="nav-link"
            :class="{ active: activeTab === 'activities' }"
            @click="activeTab = 'activities'"
            type="button"
          >
            {{ t.activities }}
          </button>
        </li>

        <li class="nav-item fs-5">
          <button
            class="nav-link"
            :class="{ active: activeTab === 'facilities' }"
            @click="activeTab = 'facilities'"
            type="button"
          >
            {{ t.facilities }}
          </button>
        </li>
      </ul>

      <!-- TAB CONTENT -->
      <div class="tab-content">
        <!-- ACTIVIDADES -->
          <div
            class="tab-pane fade"
            :class="{ show: activeTab === 'activities', active: activeTab === 'activities' }"
          >
            <div class="row g-4">
              <div class="col-md-4">
                <FilterCard
                  :icon="Calendar"
                  :title="t.dayOfWeek"
                  :subtitle="orderedSelectedDays.join(', ')"
                  @click="() => activar('A1')"
                />
              </div>

            <div class="col-md-4">
              <FilterCard
                :icon="Activity"
                :title="t.activityType"
                :subtitle="selectedActivityTypes.join(', ')"
                @click="() => activar('A2')"
              />
            </div>

            <div class="col-md-4">
              <FilterCard
                :icon="Clock"
                :title="t.sessionTime"
                :subtitle="activityStartTime || activityEndTime ? `${activityStartTime} - ${activityEndTime}`: ''"
                @click="() => activar('A3')"
              />
            </div>
          </div>
        </div>

        <!-- INSTALACIONES -->
        <div
          class="tab-pane fade"
          :class="{ show: activeTab === 'facilities', active: activeTab === 'facilities' }"
        >
          <div class="row g-4 justify-content-center">
            <div class="col-md-6">
              <FilterCard
                :icon="Building2"
                :title="t.facilityType"
                :subtitle="selectedFacilityTypes.join(', ')"
                @click="() => activar('I1')"
              />
            </div>

            <div class="col-md-6">
              <FilterCard
                :icon="Clock"
                :title="t.openingHours"
                :subtitle="facilityStartTime || facilityEndTime ? `${facilityStartTime} - ${facilityEndTime}`: ''"
                @click="() => activar('I2')"
              />
            </div>
          </div>
        </div>
      </div>

      <DayOfWeekFilter
        :open="dayFilterOpen"
        @update:open="dayFilterOpen = $event"
        :selectedDays="selectedDays"
        @apply="selectedDays = $event"
      />

      <ActivityTypeFilter
        :open="activityTypeFilterOpen"
        @update:open="activityTypeFilterOpen = $event"
        :selectedTypes="selectedActivityTypes"
        @apply="selectedActivityTypes = $event"
        :tiposActividad="estadisticas.tiposActividad"
      />

      <TimeRangeFilter
        :open="activityTimeFilterOpen"
        @update:open="activityTimeFilterOpen = $event"
        :startTime="activityStartTime"
        :endTime="activityEndTime"
        @apply="({ start, end }) => { activityStartTime = start; activityEndTime = end }"
        title="Horario de sesión"
        description="Selecciona el rango horario."
      />

      <FacilityTypeFilter
        :open="facilityTypeFilterOpen"
        @update:open="facilityTypeFilterOpen = $event"
        :selectedTypes="selectedFacilityTypes"
        @apply="selectedFacilityTypes = $event"
        :tiposInstalacion="estadisticas.tiposInstalacion"
      />

      <TimeRangeFilter
        :open="facilityTimeFilterOpen"
        @update:open="facilityTimeFilterOpen = $event"
        :startTime="facilityStartTime"
        :endTime="facilityEndTime"
        @apply="({ start, end }) => { facilityStartTime = start; facilityEndTime = end }"
        title="Horario de apertura"
        description="Selecciona el horario de la instalación."
      />

    </main>
  </div>
</template>


<script setup lang="ts">
import { ref, computed, inject, type Ref, onMounted } from "vue";
import { useRouter } from 'vue-router'
import {
  Activity,
  Building2,
  Clock,
  Calendar
} from "lucide-vue-next";
import FilterCard from "./filters/FilterCard.vue";
import DayOfWeekFilter from "./filters/DayOfWeekFilter.vue";
import ActivityTypeFilter from "./filters/ActivityTypeFilter.vue";
import TimeRangeFilter from "./filters/TimeRangeFilter.vue";
import FacilityTypeFilter from "./filters/FacilityTypeFilter.vue";

/* Importamos las comunicaciones con el backend para obtener las notificaciones*/
import { getNotificaciones } from "../services/usuarioService";

/* Importamos las comunicaciones con el backend a traves de nuestro Store para guardar las estadisticas y el usuario */
import { useAuthStore } from "../stores/auth";
import { useEstadisticasStore } from "../stores/estadisticas";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const userStore = useAuthStore();
const estadisticasStore = useEstadisticasStore();
const estadisticas = estadisticasStore.data;

const router = useRouter()

const activeTab = ref('activities');

const dayFilterOpen = ref(false);
const activityTypeFilterOpen = ref(false);
const activityTimeFilterOpen = ref(false);
const facilityTypeFilterOpen = ref(false);
const facilityTimeFilterOpen = ref(false);

const selectedDays = ref<string[]>([]);
const selectedActivityTypes = ref<string[]>([]);
const activityStartTime = ref("");
const activityEndTime = ref("");
const selectedFacilityTypes = ref<string[]>([]);
const facilityStartTime = ref("");
const facilityEndTime = ref("");

/* Orden de los dias dependiendo del idioma */
const weekOrder = [
  t.value.monday,
  t.value.tuesday,
  t.value.wednesday,
  t.value.thursday,
  t.value.friday,
  t.value.saturday,
  t.value.sunday,
];

const orderedSelectedDays = computed(() =>
  weekOrder.filter(day => selectedDays.value.includes(day))
);

type BusquedaCompleta = {
  busqueda?: string
  dias?: string[]
  tiposActividad?: string[]
  tiempoInicioActividad?: string
  tiempoFinActividad?: string
  tiposInstalacion?: string[]
  tiempoInicioInstalacion?: string
  tiempoFinInstalacion?: string
}

const textoBusqueda = ref('')

function buscar() {
  const busquedaCompleta: BusquedaCompleta = {}

  /* Controlamos la existencia de cada filtro para no enviarlo en caso de no necesitarlo */

  if(textoBusqueda.value != '') {
    busquedaCompleta["busqueda"] = textoBusqueda.value
  }

  if(selectedDays.value.length > 0) {
    busquedaCompleta["dias"] = selectedDays.value
  }

  if(selectedActivityTypes.value.length > 0) {
    busquedaCompleta["tiposActividad"] = selectedActivityTypes.value
  }

  if(selectedFacilityTypes.value.length > 0) {
    busquedaCompleta["tiposInstalacion"] = selectedFacilityTypes.value
  }
  
  if(activityStartTime.value != '') {
    busquedaCompleta["tiempoInicioActividad"] = activityStartTime.value
  }

  if(activityEndTime.value != '') {
    busquedaCompleta["tiempoFinActividad"] = activityEndTime.value
  }

  if(facilityStartTime.value != '') {
    busquedaCompleta["tiempoInicioInstalacion"] = facilityStartTime.value
  }

  if(facilityEndTime.value != '') {
    busquedaCompleta["tiempoFinInstalacion"] = facilityEndTime.value
  }

  router.push({
    path: '/buscar',
    query: busquedaCompleta
  })
}

const activar = (tipo: string) => {
  dayFilterOpen.value = false;
  activityTypeFilterOpen.value = false;
  activityTimeFilterOpen.value = false;
  facilityTypeFilterOpen.value = false;
  facilityTimeFilterOpen.value = false;
  
  if(tipo === 'A1') {
    dayFilterOpen.value = true;
  } else if(tipo === 'A2') {
    activityTypeFilterOpen.value = true;
  } else if(tipo === 'A3') {
    activityTimeFilterOpen.value = true;
  } else if(tipo === 'I1') {
    facilityTypeFilterOpen.value = true;
  } else {
    facilityTimeFilterOpen.value = true;
  }
};

export type Notificacion = {
  id: number
  titulo: string
  descripcion: string
  leido: boolean
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

onMounted(async () => {
  const data = await getNotificaciones();

  notificaciones.value.notificaciones = data.notificaciones;
  notificaciones.value.no_leidas = data.no_leidas;
})

</script>

<style>
  .linea-fina {
  height: 1px;
  background-color: #ddd;
  margin: 1rem 0;
}
</style>