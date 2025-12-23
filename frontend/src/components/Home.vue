
<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-100">

    <!-- MAIN -->
    <main class="container-fluid mt-5 max-w-7xl mx-auto px-6 py-10">
      <!-- INTRO -->
      <div class="text-center mt-10 mb-6">
        <h1 class="text-3xl font-bold text-slate-900">
          {{ t.welcome }}
        </h1>
        <p class="text-lg text-slate-600 mt-2">
          {{ t.welcome2 }}
        </p>

        <!-- BUSQUEDAS -->
        <div class="container-fluid mx-auto mt-4">
          <div class="d-flex gap-3 align-items-center bg-white rounded-4 shadow-lg p-3 border">
            <div class="d-flex align-items-center gap-3 flex-grow-1 px-2">
              <Search class="text-secondary"/>
                <input
                  type="text"
                  class="form-control border-0 fs-5"
                  :placeholder="t.searchPlaceholder"
                />
            </div>

            <button class="btn btn-primary btn-lg px-4">
              {{ t.searchButton }}
            </button>
          </div>
        </div>
      </div>

      <!-- FILTROS -->
      <h2 class="text-2xl font-semibold text-center text-slate-800 mt-5 mb-3">
        {{ t.filterBy }}
      </h2>

    <!-- Tabs triggers -->
    <ul class="nav nav-tabs justify-content-center mb-4" role="tablist">
      <li class="nav-item" role="presentation">
        <button
          class="nav-link"
          :class="{ active: activeTab === 'activities' }"
          @click="activeTab = 'activities'"
          type="button"
          role="tab"
        >
          {{ t.activities }}
        </button>
      </li>
      <li class="nav-item" role="presentation">
        <button
          class="nav-link"
          :class="{ active: activeTab === 'facilities' }"
          @click="activeTab = 'facilities'"
          type="button"
          role="tab"
        >
          {{ t.facilities }}
        </button>
      </li>
    </ul>

    <!-- Tabs content -->
    <div class="tab-content">
      <div
        class="tab-pane fade"
        :class="{ show: activeTab === 'activities', active: activeTab === 'activities' }"
      >
        <!-- Aquí va el contenido de "Activities" -->
        <div class="row g-3">
          <div class="col-md-4">
            <FilterCard title="Día de la semana" @click="dayFilterOpen = true" icon="null" />
          </div>
          <div class="col-md-4">
            <FilterCard title="Tipo de actividad" @click="activityTypeFilterOpen = true" />
          </div>
          <div class="col-md-4">
            <FilterCard title="Horario" @click="activityTimeFilterOpen = true" />
          </div>
        </div>
      </div>

      <div
        class="tab-pane fade"
        :class="{ show: activeTab === 'facilities', active: activeTab === 'facilities' }"
      >
        <!-- Aquí va el contenido de "Facilities" -->
        <div class="row g-3">
          <div class="col-md-6">
            <FilterCard title="Tipo de instalación" @click="facilityTypeFilterOpen = true" />
          </div>
          <div class="col-md-6">
            <FilterCard title="Horario de apertura" @click="facilityTimeFilterOpen = true" />
          </div>
        </div>
      </div>
    </div>

      <!-- DIALOGS -->
      <DayOfWeekFilter
        :open="dayFilterOpen"
        @update:open="dayFilterOpen = $event"
        :selected-days="selectedDays"
        @apply="selectedDays = $event"
      />

      <ActivityTypeFilter
        :open="activityTypeFilterOpen"
        @update:open="activityTypeFilterOpen = $event"
        :selected-types="selectedActivityTypes"
        @apply="selectedActivityTypes = $event"
      />

      <TimeRangeFilter
        :open="activityTimeFilterOpen"
        @update:open="activityTimeFilterOpen = $event"
        :start-time="activityStartTime"
        :end-time="activityEndTime"
        title="Horario de sesión"
        description="Selecciona el rango horario"
        @apply="(start, end) => {
          activityStartTime = start;
          activityEndTime = end;
        }"
      />

      <FacilityTypeFilter
        :open="facilityTypeFilterOpen"
        @update:open="facilityTypeFilterOpen = $event"
        :selected-types="selectedFacilityTypes"
        @apply="selectedFacilityTypes = $event"
      />

      <TimeRangeFilter
        :open="facilityTimeFilterOpen"
        @update:open="facilityTimeFilterOpen = $event"
        :start-time="facilityStartTime"
        :end-time="facilityEndTime"
        title="Horario de apertura"
        description="Selecciona el horario de la instalación"
        @apply="(start, end) => {
          facilityStartTime = start;
          facilityEndTime = end;
        }"
      />

      <!-- STATS -->
      <div class="mt-10">
        <h2 class="text-3xl font-semibold text-center text-slate-900 mb-6">
          Nuestros números
        </h2>

        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-8 text-center">
          <div v-for="stat in [
            ['+50', 'Actividades'],
            ['15', 'Instalaciones'],
            ['5', 'Pabellones'],
            ['+10', 'Deportes'],
            ['+3000', 'Usuarios'],
          ]" :key="stat[1]">
            <p class="text-3xl text-blue-600 font-bold">
              {{ stat[0] }}
            </p>
            <p class="text-slate-600 text-lg">
              {{ stat[1] }}
            </p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue';
  import FilterCard from "./filters/FilterCard.vue";
  import DayOfWeekFilter from "./filters/DayOfWeekFilter.vue";
  import ActivityTypeFilter from "./filters/ActivityTypeFilter.vue";
  import TimeRangeFilter from "./filters/TimeRangeFilter.vue";
  import FacilityTypeFilter from "./filters/FacilityTypeFilter.vue";


  const activeTab = ref('activities');

  const dayFilterOpen = ref(false);
  const activityTypeFilterOpen = ref(false);
  const activityTimeFilterOpen = ref(false);
  const facilityTypeFilterOpen = ref(false);
  const facilityTimeFilterOpen = ref(false);

  defineProps<{
    t: Record<string, string>
  }>();

  const selectedDays = ref<string[]>([]);
  const selectedActivityTypes = ref<string[]>([]);
  const activityStartTime = ref("");
  const activityEndTime = ref("");
  const selectedFacilityTypes = ref<string[]>([]);
  const facilityStartTime = ref("");
  const facilityEndTime = ref("");
</script>
