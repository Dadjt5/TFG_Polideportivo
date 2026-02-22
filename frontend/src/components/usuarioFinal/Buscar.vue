<template>
  <div class="min-vh-100 bg-light">
    <main class="container-fluid mt-2 px-5 py-1">

      <div class="text-center mt-5 mb-4">
        <div class="container-fluid mt-4">
          <div class="d-flex align-items-center bg-white rounded-3 shadow p-2 border gap-3">
            <Search class="text-secondary"/>

            <input
              type="text"
              class="form-control border-0 fs-5"
              :placeholder="t.searchPlaceholder"
              v-model="textoBusqueda"
              @keyup.enter="buscar"
            />

            <button class="btn btn-primary btn-lg px-4" @click="buscar">
              {{ t.searchButton }}
            </button>
          </div>
        </div>
      </div>

      <ul class="nav nav-tabs justify-content-center mb-3">
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

      <div class="tab-content">
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
                  :theme="'light'"
                />
              </div>

            <div class="col-md-4">
              <FilterCard
                :icon="Activity"
                :title="t.activityType"
                :subtitle="selectedActivityTypes.join(', ')"
                @click="activar('A2')"
                :theme="'light'"
              />
            </div>

            <div class="col-md-4">
              <FilterCard
                :icon="Clock"
                :title="t.sessionTime"
                :subtitle="activityStartTime || activityEndTime ? `${activityStartTime} - ${activityEndTime}`: ''"
                @click="activar('A3')"
                :theme="'light'"
              />
            </div>
          </div>
        </div>

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
                :theme="'light'"
              />
            </div>

            <div class="col-md-6">
              <FilterCard
                :icon="Clock"
                :title="t.openingHours"
                :subtitle="facilityStartTime || facilityEndTime ? `${facilityStartTime} - ${facilityEndTime}`: ''"
                @click="activar('I2')"
                :theme="'light'"
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
        :theme="'light'"
      />

      <ActivityTypeFilter
        :open="activityTypeFilterOpen"
        @update:open="activityTypeFilterOpen = $event"
        :selectedTypes="selectedActivityTypes"
        @apply="selectedActivityTypes = $event"
        :tiposActividad="estadisticas.tiposActividad"
        :theme="'light'"
      />

      <TimeRangeFilter
        :open="activityTimeFilterOpen"
        @update:open="activityTimeFilterOpen = $event"
        :startTime="activityStartTime"
        :endTime="activityEndTime"
        @apply="({ start, end }) => { activityStartTime = start; activityEndTime = end }"
        title="Horario de sesión"
        description="Selecciona el rango horario."
        :theme="'light'"
      />

      <FacilityTypeFilter
        :open="facilityTypeFilterOpen"
        @update:open="facilityTypeFilterOpen = $event"
        :selectedTypes="selectedFacilityTypes"
        @apply="selectedFacilityTypes = $event"
        :tiposInstalacion="estadisticas.tiposInstalacion"
        :theme="'light'"
      />

      <TimeRangeFilter
        :open="facilityTimeFilterOpen"
        @update:open="facilityTimeFilterOpen = $event"
        :startTime="facilityStartTime"
        :endTime="facilityEndTime"
        @apply="({ start, end }) => { facilityStartTime = start; facilityEndTime = end }"
        title="Horario de apertura"
        description="Selecciona el horario de la instalación."
        :theme="'light'"
      />

      <div class="mt-4">
        <div class="d-flex justify-content-end mb-3">
          <select
            class="form-select w-auto"
            v-model="orderBy"
            >
            <option value="nombre_asc">
              {{ t.orderByNameAsc }}
            </option>
            <option value="nombre_desc">
              {{ t.orderByNameDesc }}
            </option>
          </select>
        </div>
      </div>

      <!-- RESULTADOS DE LA BUSQUEDA -->
      <div class="container-fluid mt-4 row">
        <p class="fs-2 fw-semibold text-center">{{ t.activities }}</p>
        <p class="fs-3 text-center" v-if="sinActividades">{{ t.noResults }}</p>
          <div
            v-for="act in actividadesOrdenadas"
            :key="act.id"
            class="col-12 col-sm-6 col-lg-4 mt-3"
            @click="activityDetail(act.id)"
            v-else
          >
          <ActivityCard
            :icon="Activity"
            :actividad="act"
            :theme="'light'"
          />
          </div>

        <p class="fs-2 fw-semibold text-center mt-5">{{ t.facilities }}</p>
        <p class="fs-3 text-center" v-if="sinInstalaciones">{{ t.noResults }}</p>
          <div
            v-for="inst in instalacionesOrdenadas"
            :key="inst.id"
            class="col-12 col-sm-6 col-lg-4 mt-3"
            @click="facilityDetail(inst.id)"
            v-else
          >
            <FacilityCard
              :icon="Building2"
              :instalacion="inst"
              :theme="'light'"
            />
          </div>
      </div>
    </main>
  </div>
</template>


<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { computed, type Ref, ref, inject, onMounted, watch } from 'vue';
import {
  Calendar,
  Activity,
  Clock,
  Building2
} from 'lucide-vue-next';
import FilterCard from "@/components/filters/FilterCard.vue";
import FacilityCard from "@/components/filters/FacilityCard.vue";
import ActivityCard from "@/components/filters/ActivityCard.vue";
import DayOfWeekFilter from "@/components/filters/DayOfWeekFilter.vue";
import ActivityTypeFilter from "@/components/filters/ActivityTypeFilter.vue";
import TimeRangeFilter from "@/components/filters/TimeRangeFilter.vue";
import FacilityTypeFilter from "@/components/filters/FacilityTypeFilter.vue";

/* Importamos las comunicaciones con el backend */
import { getBusqueda } from "@/services/buscarService";

import { useEstadisticasStore } from "@/stores/estadisticas";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);
const sinActividades = ref(false)
const sinInstalaciones = ref(false)
const error = ref("");

const orderBy = ref<'nombre_asc' | 'nombre_desc'>('nombre_asc')

const route = useRoute()
const router = useRouter()

interface Resultados {
  actividades: any[] | null
  instalaciones: any[] | null
}

const resultados = ref<Resultados>({
  actividades: null,
  instalaciones: null
})

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

const estadisticasStore = useEstadisticasStore();

const estadisticas = estadisticasStore.data;

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

const actividadesOrdenadas = computed(() => {
  if (!resultados.value.actividades) return []

  return [...resultados.value.actividades].sort((a, b) => {
    if (orderBy.value === 'nombre_asc') {
      return a.nombre.localeCompare(b.nombre)
    }
    return b.nombre.localeCompare(a.nombre)
  })
})

const instalacionesOrdenadas = computed(() => {
  if (!resultados.value.instalaciones) return []

  return [...resultados.value.instalaciones].sort((a, b) => {
    if (orderBy.value === 'nombre_asc') {
      return a.nombre.localeCompare(b.nombre)
    }
    return b.nombre.localeCompare(a.nombre)
  })
})

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

watch(() =>
  route.query,
  async (newQuery) => {
    try {
      resultados.value = await getBusqueda(newQuery)
      if (resultados.value.actividades != null && resultados.value.actividades.length != 0 ) {
        sinActividades.value = false
      } else {
        sinActividades.value = true
      }
      if (resultados.value.instalaciones != null && resultados.value.instalaciones.length != 0 ) {
        sinInstalaciones.value = false
      } else {
        sinInstalaciones.value = true
      }
    } catch (err) {
      error.value = "No se han encontrado resultados"
    }
  },
  { immediate: true }
)

function transformQueryArray(value: unknown): string[] {
  if (!value) return []
  return Array.isArray(value) ? value.map(String) : [String(value)]
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

const textoBusqueda = ref("")

onMounted(async () => {
  textoBusqueda.value = String(route.query.busqueda)

  selectedDays.value = transformQueryArray(route.query.dias)
  selectedActivityTypes.value = transformQueryArray(route.query.tiposActividad)
  selectedFacilityTypes.value = transformQueryArray(route.query.tiposInstalacion)

  activityStartTime.value = String(route.query.tiempoInicioActividad ?? "")
  activityEndTime.value = String(route.query.tiempoFinActividad ?? "")
  facilityStartTime.value = String(route.query.tiempoInicioInstalacion ?? "")
  facilityEndTime.value = String(route.query.tiempoFinInstalacion ?? "")

  try {
    resultados.value = await getBusqueda(route.query);
    if (resultados.value.actividades != null && resultados.value.actividades.length != 0 ) {
      sinActividades.value = false
    } else {
      sinActividades.value = true
    }
    if (resultados.value.instalaciones != null && resultados.value.instalaciones.length != 0 ) {
      sinInstalaciones.value = false
    } else {
      sinInstalaciones.value = true
    }
  } catch (err) {
    console.error(err);
  }
})

</script>
