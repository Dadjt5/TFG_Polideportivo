<template>
  <div class="min-vh-100 position-relative">

    <!-- Fondo con overlay oscuro -->
    <div class="position-absolute top-0 start-0 w-100 h-100" style="
        background:
          linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
          url('/images/Polideportivo.jpg') center/cover no-repeat;
      "></div>

    <main class="position-relative container py-4">

      <h1 class="text-center text-white fw-bold mb-4">
        {{ t.welcome }}
      </h1>

      <div class="row g-4 mb-5">

        <!-- Notificaciones -->
        <div class="col-lg-8">
          <div class="card shadow-sm h-100 bg-white bg-opacity-10 border border-white border-opacity-25">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <router-link to="/notificaciones"
                  class="d-flex align-items-center gap-2 text-decoration-none text-white">
                  <i class="bi bi-bell-fill text-primary fs-4"></i>

                  <h5 class="mb-0 text-white">
                    {{ t.notifications }}
                  </h5>

                  <span v-if="usuarioFinalStore.unreadCount > 0" class="badge bg-danger">
                    {{ usuarioFinalStore.unreadCount }}
                  </span>
                </router-link>
              </div>

              <div v-if="usuarioFinalStore.notificaciones.length === 0"
                class="d-flex flex-column justify-content-center align-items-center py-5 text-center">
                <i class="bi bi-bell-slash text-white fs-1 mb-3"></i>
                <p class="text-white opacity-75 fs-5 mb-0">
                  {{ t.noNotificacions }}
                </p>
              </div>
              <div v-else v-for="notf in usuarioFinalStore.notificaciones" :key="notf.id" class="rounded p-3 mb-2"
                :class="notf.leido ? 'bg-white bg-opacity-10 text-white' : 'bg-primary bg-opacity-20 text-white'">
                <strong>{{ notf.titulo }}</strong>
                <p class="mb-0 small text-white text-opacity-75">
                  {{ notf.descripcion }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Estadísticas -->
        <div class="col-lg-4">
          <div class="card shadow-sm mb-3 bg-white bg-opacity-10 border border-white border-opacity-25">
            <div class="card-body">
              <div class="d-flex align-items-center gap-2 mb-2">
                <i class="bi bi-bar-chart-fill text-primary me-2 fs-4"></i>
                <h6 class="mb-0 text-white">{{ t.userStats }}</h6>
              </div>
              <router-link to="/estadisticas/usuarioFinal" v-if="userStore.user" class="btn btn-success w-100">
                {{ t.viewUserStats }}
              </router-link>
            </div>
          </div>

          <div class="card shadow-sm bg-white bg-opacity-10 border border-white border-opacity-25">
            <div class="card-body">
              <div class="d-flex align-items-center gap-2 mb-2">
                <i class="bi bi-calendar-fill text-primary me-2 fs-4"></i>
                <h6 class="mb-0 text-white">{{ t.bookingsMade }}</h6>
              </div>
              <router-link to="/reservas-realizadas" v-if="userStore.user" class="btn btn-success w-100">
                {{ t.viewBooks }}
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <div class="linea-fina"></div>

      <!-- BUSQUEDAS -->
      <div class="text-center mt-5 mb-4">
        <div class="container-fluid mt-4">
          <div class="d-flex align-items-center 
            bg-white bg-opacity-10 
            backdrop-blur 
            rounded-4 
            shadow-lg 
            p-3 
            border border-white border-opacity-25 
            gap-3">

            <Search class="text-secondary" />

            <input type="text" v-model="textoBusqueda" class="form-control border-0 bg-transparent text-white fs-5"
              :placeholder="t.searchPlaceholder" @keyup.enter="buscar" />

            <button class="btn btn-primary btn-lg px-4" @click="buscar">
              {{ t.searchButton }}
            </button>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <ul class="nav nav-tabs justify-content-center mb-4">
        <li class="nav-item fs-5">
          <button class="nav-link" :class="{ active: activeTab === 'activities' }" @click="activeTab = 'activities'"
            type="button">
            {{ t.activities }}
          </button>
        </li>

        <li class="nav-item fs-5">
          <button class="nav-link" :class="{ active: activeTab === 'facilities' }" @click="activeTab = 'facilities'"
            type="button">
            {{ t.facilities }}
          </button>
        </li>
      </ul>

      <!-- Contenido Tabs -->
      <div class="tab-content">
        <div class="tab-pane fade" :class="{ show: activeTab === 'activities', active: activeTab === 'activities' }">
          <div class="row g-4">
            <div class="col-md-4">
              <FilterCard :icon="Calendar" :title="t.dayOfWeek" :subtitle="orderedSelectedDays.join(', ')"
                @click="() => activar('A1')" :theme="'dark'" />
            </div>
            <div class="col-md-4">
              <FilterCard :icon="Activity" :title="t.activityType" :subtitle="selectedActivityTypes.join(', ')"
                @click="() => activar('A2')" :theme="'dark'"/>
            </div>
            <div class="col-md-4">
              <FilterCard :icon="Clock" :title="t.sessionTime"
                :subtitle="activityStartTime || activityEndTime ? `${activityStartTime} - ${activityEndTime}` : ''"
                @click="() => activar('A3')" :theme="'dark'"/>
            </div>
          </div>
        </div>

        <div class="tab-pane fade" :class="{ show: activeTab === 'facilities', active: activeTab === 'facilities' }">
          <div class="row g-4 justify-content-center">
            <div class="col-md-6">
              <FilterCard :icon="Building2" :title="t.facilityType" :subtitle="selectedFacilityTypes.join(', ')"
                @click="() => activar('I1')" :theme="'dark'"/>
            </div>
            <div class="col-md-6">
              <FilterCard :icon="Clock" :title="t.openingHours"
                :subtitle="facilityStartTime || facilityEndTime ? `${facilityStartTime} - ${facilityEndTime}` : ''"
                @click="() => activar('I2')" :theme="'dark'"/>
            </div>
          </div>
        </div>
      </div>

      <!-- Filtros modales -->
      <DayOfWeekFilter :open="dayFilterOpen" @update:open="dayFilterOpen = $event" :selectedDays="selectedDays"
        @apply="selectedDays = $event" :theme="'dark'" />

      <ActivityTypeFilter :open="activityTypeFilterOpen" @update:open="activityTypeFilterOpen = $event"
        :selectedTypes="selectedActivityTypes" @apply="selectedActivityTypes = $event" :theme="'dark'" />

      <TimeRangeFilter :open="activityTimeFilterOpen" @update:open="activityTimeFilterOpen = $event"
        :startTime="activityStartTime" :endTime="activityEndTime"
        @apply="({ start, end }) => { activityStartTime = start; activityEndTime = end }" :theme="'dark'" />

      <FacilityTypeFilter :open="facilityTypeFilterOpen" @update:open="facilityTypeFilterOpen = $event"
        :selectedTypes="selectedFacilityTypes" @apply="selectedFacilityTypes = $event" :theme="'dark'" />

      <TimeRangeFilter :open="facilityTimeFilterOpen" @update:open="facilityTimeFilterOpen = $event"
        :startTime="facilityStartTime" :endTime="facilityEndTime"
        @apply="({ start, end }) => { facilityStartTime = start; facilityEndTime = end }" :theme="'dark'" />

      <!-- Favoritos -->
      <div class="container-fluid mt-5 row">
        <div v-if="longitudActividades !== 0">
          <p class="fs-2 fw-semibold text-center text-white">{{ t.activities }} {{ t.favourites }}</p>
          <div v-for="actividad in actividadesFavoritas" :key="actividad.id" class="col-12 col-sm-6 col-lg-4"
            @click="activityDetail(actividad.id)">
            <ActivityCard :icon="Activity" :actividad="actividad" :theme="'dark'"/>
          </div>
        </div>

        <div v-if="longitudInstalaciones !== 0">
          <p class="fs-2 fw-semibold text-center text-white mt-5">{{ t.facilities }} {{ t.favourites }}</p>
          <div v-for="instalacion in instalacionesFavoritas" :key="instalacion.id" class="col-12 col-sm-6 col-lg-4"
            @click="facilityDetail(instalacion.id)">
            <FacilityCard :icon="Building2" :instalacion="instalacion" :theme="'dark'"/>
          </div>
        </div>
      </div>

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
import FilterCard from "@/components/filters/FilterCard.vue";
import DayOfWeekFilter from "@/components/filters/DayOfWeekFilter.vue";
import ActivityTypeFilter from "@/components/filters/ActivityTypeFilter.vue";
import TimeRangeFilter from "@/components/filters/TimeRangeFilter.vue";
import FacilityTypeFilter from "@/components/filters/FacilityTypeFilter.vue";
import FacilityCard from '@/components/filters/FacilityCard.vue'
import ActivityCard from '@/components/filters/ActivityCard.vue'

/* Importamos las comunicaciones con el backend a traves de nuestro Store para guardar las estadisticas y el usuario */
import { useAuthStore } from "@/stores/auth";
import { useUserStore } from "@/stores/usuarioFinal";
import { useEstadisticasStore } from "@/stores/estadisticas";

import { getActividadesInstalaciones } from "@/services/detalleService";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const userStore = useAuthStore();
const usuarioFinalStore = useUserStore();
const estadisticasStore = useEstadisticasStore();

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

  if (textoBusqueda.value != '') {
    busquedaCompleta["busqueda"] = textoBusqueda.value
  }

  if (selectedDays.value.length > 0) {
    busquedaCompleta["dias"] = selectedDays.value
  }

  if (selectedActivityTypes.value.length > 0) {
    busquedaCompleta["tiposActividad"] = selectedActivityTypes.value
  }

  if (selectedFacilityTypes.value.length > 0) {
    busquedaCompleta["tiposInstalacion"] = selectedFacilityTypes.value
  }

  if (activityStartTime.value != '') {
    busquedaCompleta["tiempoInicioActividad"] = activityStartTime.value
  }

  if (activityEndTime.value != '') {
    busquedaCompleta["tiempoFinActividad"] = activityEndTime.value
  }

  if (facilityStartTime.value != '') {
    busquedaCompleta["tiempoInicioInstalacion"] = facilityStartTime.value
  }

  if (facilityEndTime.value != '') {
    busquedaCompleta["tiempoFinInstalacion"] = facilityEndTime.value
  }

  router.push({
    path: '/buscar',
    query: busquedaCompleta
  })
}

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

interface Resultados {
  actividades: any[] | null
  instalaciones: any[] | null
}

const resultados = ref<Resultados>({
  actividades: null,
  instalaciones: null
})

const actividadesFavoritas = computed(() => {
  if (!resultados.value.actividades) return []

  return [...resultados.value.actividades].sort((a, b) => {
    return a.nombre.localeCompare(b.nombre)
  })
})

const instalacionesFavoritas = computed(() => {
  if (!resultados.value.instalaciones) return []

  return [...resultados.value.instalaciones].sort((a, b) => {
    return a.nombre.localeCompare(b.nombre)
  })
})

const longitudActividades = computed(() => actividadesFavoritas.value.length);
const longitudInstalaciones = computed(() => instalacionesFavoritas.value.length);

onMounted(async () => {
  if (!estadisticasStore.data.modificado) {
    await estadisticasStore.cargarEstadisticas();
  }

  if (!usuarioFinalStore.usuarioFinal) {
    await usuarioFinalStore.fetchUser(userStore.user?.usuario_final_id)
  }

  if (usuarioFinalStore.notificaciones.length === 0) {
    await usuarioFinalStore.fetchNotificaciones();
  }

  resultados.value = await getActividadesInstalaciones({
    actividad_ids: usuarioFinalStore.favoritos.actividades,
    instalacion_ids: usuarioFinalStore.favoritos.instalaciones,
  });

  usuarioFinalStore.comenzarIntervalo();
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

.linea-fina {
  height: 1px;
  background-color: #ddd;
  margin: 1rem 0;
}
</style>