<template>
<div class="min-vh-100 position-relative">
  <div
  class="position-absolute top-0 start-0 w-100 h-100"
  style="
    background: 
      linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
      url('/images/Polideportivo.jpg') center/cover no-repeat;
  "
  ></div>

  <main class="position-relative container-fluid py-5 px-4 px-lg-5">
      <!-- INTRO -->
      <div class="text-center mt-5 mb-4">
        <h1 class="fs-1 fw-bold text-white">
          {{ t.welcome }}
        </h1>
        <p class="fs-5 text-white text-opacity-75 mt-2">
          {{ t.welcome2 }}
        </p>

        <!-- BUSQUEDAS -->
        <div class="container-fluid mt-4">
          <div class="d-flex align-items-center 
            bg-white bg-opacity-10 
            backdrop-blur 
            rounded-4 
            shadow-lg 
            p-3 
            border border-white border-opacity-25 
            gap-3">

            <input
              type="text"
              v-model="textoBusqueda"
              class="form-control border-0 bg-transparent text-white fs-5"
              :placeholder="t.searchPlaceholder"
              @keyup.enter="buscar"
            />

            <button class="btn btn-primary btn-lg px-4"  @click="buscar">
              {{ t.searchButton }}
            </button>
          </div>
        </div>
      </div>

      <!-- FILTROS -->
      <h2 class="fs-3 fw-semibold text-center text-white mb-4">
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
                  @click="activar('A1')"
                  :theme="'dark'"
                />
              </div>

            <div class="col-md-4">
              <FilterCard
                :icon="Activity"
                :title="t.activityType"
                :subtitle="selectedActivityTypes.join(', ')"
                @click="activar('A2')"
                :theme="'dark'"
              />
            </div>

            <div class="col-md-4">
              <FilterCard
                :icon="Clock"
                :title="t.sessionTime"
                :subtitle="activityStartTime || activityEndTime ? `${activityStartTime} - ${activityEndTime}`: ''"
                @click="activar('A3')"
                :theme="'dark'"
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
                @click="activar('I1')"
                :theme="'dark'"
              />
            </div>

            <div class="col-md-6">
              <FilterCard
                :icon="Clock"
                :title="t.openingHours"
                :subtitle="facilityStartTime || facilityEndTime ? `${facilityStartTime} - ${facilityEndTime}`: ''"
                @click="activar('I2')"
                :theme="'dark'"
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
        :theme="'dark'"
      />

      <ActivityTypeFilter
        :open="activityTypeFilterOpen"
        @update:open="activityTypeFilterOpen = $event"
        :selectedTypes="selectedActivityTypes"
        @apply="selectedActivityTypes = $event"
        :tiposActividad="estadisticasStore.data.tiposActividad"
        :theme="'dark'"
      />

      <TimeRangeFilter
        :open="activityTimeFilterOpen"
        @update:open="activityTimeFilterOpen = $event"
        :startTime="activityStartTime"
        :endTime="activityEndTime"
        @apply="({ start, end }) => { activityStartTime = start; activityEndTime = end }"
        title="Horario de sesión"
        description="Selecciona el rango horario."
        :theme="'dark'"
      />

      <FacilityTypeFilter
        :open="facilityTypeFilterOpen"
        @update:open="facilityTypeFilterOpen = $event"
        :selectedTypes="selectedFacilityTypes"
        @apply="selectedFacilityTypes = $event"
        :tiposInstalacion="estadisticasStore.data.tiposInstalacion"
        :theme="'dark'"
      />

      <TimeRangeFilter
        :open="facilityTimeFilterOpen"
        @update:open="facilityTimeFilterOpen = $event"
        :startTime="facilityStartTime"
        :endTime="facilityEndTime"
        @apply="({ start, end }) => { facilityStartTime = start; facilityEndTime = end }"
        title="Horario de apertura"
        description="Selecciona el horario de la instalación."
        :theme="'dark'"
      />

      <!-- ESTADISTICAS -->
      <div class="mt-5 py-5 rounded-4 
          bg-white bg-opacity-10 
          backdrop-blur 
          border border-white border-opacity-25">

        <h2 class="fs-2 fw-semibold text-center text-white mb-4">
          {{t.statsTitle}}
        </h2>

        <div v-if="error" class="text-center fs-4">{{ error }}</div>

        <div v-else class="row text-center gy-4">
          <div class="col-6 col-md-4 col-lg">
            <p class="fs-3 text-primary fw-bold mb-1">{{ estadisticasStore.data.actividades }}</p>
            <p class="fs-5 text-white text-opacity-75 mb-0">{{t.activities}}</p>
          </div>

          <div class="col-6 col-md-4 col-lg">
            <p class="fs-3 text-primary fw-bold mb-1">{{ estadisticasStore.data.instalaciones }}</p>
            <p class="fs-5 text-white text-opacity-75 mb-0">{{t.facilities}}</p>
          </div>

          <div class="col-6 col-md-4 col-lg">
            <p class="fs-3 text-primary fw-bold mb-1">{{ estadisticasStore.data.pabellones }}</p>
            <p class="fs-5 text-white text-opacity-75 mb-0">{{t.pavilions}}</p>
          </div>

          <div class="col-6 col-md-4 col-lg">
            <p class="fs-3 text-primary fw-bold mb-1">{{ estadisticasStore.data.deportes }}</p>
            <p class="fs-5 text-white text-opacity-75 mb-0">{{t.sports}}</p>
          </div>

          <div class="col-6 col-md-4 col-lg">
            <p class="fs-3 text-primary fw-bold mb-1">{{ estadisticasStore.data.usuarios }}</p>
            <p class="fs-5 text-white text-opacity-75 mb-0">{{t.users}}</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, type Ref, ref, inject, onMounted } from 'vue';
import { useRouter } from 'vue-router'
import {
  Calendar,
  Activity,
  Clock,
  Building2
} from 'lucide-vue-next';
import FilterCard from "@/components/filters/FilterCard.vue";
import DayOfWeekFilter from "@/components/filters/DayOfWeekFilter.vue";
import ActivityTypeFilter from "@/components/filters/ActivityTypeFilter.vue";
import TimeRangeFilter from "@/components/filters/TimeRangeFilter.vue";
import FacilityTypeFilter from "@/components/filters/FacilityTypeFilter.vue";

/* Importamos las comunicaciones con el backend a traves de nuestro Store para guardar las estadisticas */
import { useEstadisticasStore } from "@/stores/estadisticas";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const router = useRouter()
const textoBusqueda = ref('')

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);
const error = ref("");

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
  if (tipo === 'A1') {
    dayFilterOpen.value = !dayFilterOpen.value;

    activityTypeFilterOpen.value = false;
    activityTimeFilterOpen.value = false;
    facilityTypeFilterOpen.value = false;
    facilityTimeFilterOpen.value = false;
  } else if (tipo === 'A2') {
    activityTypeFilterOpen.value = !activityTypeFilterOpen.value;
    
    dayFilterOpen.value = false;
    activityTimeFilterOpen.value = false;
    facilityTypeFilterOpen.value = false;
    facilityTimeFilterOpen.value = false;
  } else if (tipo === 'A3') {
    activityTimeFilterOpen.value = !activityTimeFilterOpen.value;

    dayFilterOpen.value = false;
    activityTypeFilterOpen.value = false;
    facilityTypeFilterOpen.value = false;
    facilityTimeFilterOpen.value = false;
  } else if (tipo === 'I1') {
    facilityTypeFilterOpen.value = !facilityTypeFilterOpen.value;

    dayFilterOpen.value = false;
    activityTypeFilterOpen.value = false;
    activityTimeFilterOpen.value = false;
    facilityTimeFilterOpen.value = false;
  } else {
    facilityTimeFilterOpen.value = !facilityTimeFilterOpen.value;

    dayFilterOpen.value = false;
    activityTypeFilterOpen.value = false;
    activityTimeFilterOpen.value = false;
    facilityTypeFilterOpen.value = false;
  }
};

const estadisticasStore = useEstadisticasStore();

onMounted(async () => {
  textoBusqueda.value=''
  try {
    if(!estadisticasStore.data.modificado) {
      await estadisticasStore.cargarEstadisticas();
    }
  } catch (err) {
    error.value = "No se han podido cargar las estadisticas";
    console.error(err);
  }
})
</script>

<style scoped>
.home-background {
  background-image: url('/images/Polideportivo.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

input::placeholder {
  color: rgba(255, 255, 255, 0.8);
  opacity: 1;
}
</style>