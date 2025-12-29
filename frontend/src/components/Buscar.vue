<template>
  <div class="min-vh-100 bg-light">

    <!-- MAIN -->
    <main class="container-fluid mt-2 px-5 py-1">

      <!-- INTRO -->
      <div class="text-center mt-5 mb-4">
        <h1 class="fs-1 fw-bold text-dark">
          {{ t.welcome }}
        </h1>
        <p class="fs-5 text-secondary mt-2">
          {{ t.welcome2 }}
        </p>

        <!-- BUSQUEDAS -->
        <div class="container-fluid mt-4">
          <div class="d-flex align-items-center bg-white rounded-3 shadow p-3 border gap-3">
            <Search class="text-secondary"/>

            <input
              type="text"
              class="form-control border-0 fs-5"
              :placeholder="t.searchPlaceholder"
            />

            <button class="btn btn-primary btn-lg px-4">
              {{ t.searchButton }}
            </button>
          </div>
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
import { useRoute } from 'vue-router'
import { computed, type Ref, ref, inject, onMounted } from 'vue';
import {
  Calendar,
  Activity,
  Clock,
  Building2
} from 'lucide-vue-next';
import FilterCard from "./filters/FilterCard.vue";
import DayOfWeekFilter from "./filters/DayOfWeekFilter.vue";
import ActivityTypeFilter from "./filters/ActivityTypeFilter.vue";
import TimeRangeFilter from "./filters/TimeRangeFilter.vue";
import FacilityTypeFilter from "./filters/FacilityTypeFilter.vue";

/* Importamos las comunicaciones con el backend */
import { getBusqueda } from "../services/buscarService";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);
const loading = ref(true);
const error = ref("");

const route = useRoute()
  
const busqueda = route.query.busqueda || ''
const tiposActividad = route.query.tiposActividad || ''
const tiposInstalacion = route.query.tiposInstalacion || ''
const tiempoInicioActividad = route.query.tiempoInicioActividad || ''
const tiempoFinActividad = route.query.tiempoFinActividad || ''
const tiempoInicioInstalacion = route.query.tiempoInicioInstalacion || ''
const tiempoFinInstalacion = route.query.tiempoFinInstalacion || ''

const resultados = ref({
  actividades: null,
  instalaciones: null
});

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

const orderedSelectedDays = computed(() =>
  weekOrder.filter(day => selectedDays.value.includes(day))
);

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

onMounted(async () => {
  try {
    resultados.value = await getBusqueda();
  } catch (err) {
    error.value = "No se han encontrado resultados";
    console.error(err);
  } finally {
    loading.value = false;
  }
})
</script>
