
<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-100">

    <!-- MAIN -->
    <main class="max-w-7xl mx-auto px-6 py-10">
      <!-- HERO -->
      <div class="text-center mb-6">
        <h1 class="text-3xl font-bold text-slate-900">
          {{ t.welcome }}
        </h1>
        <p class="text-lg text-slate-600 mt-2">
          {{ t.welcome2 }}
        </p>

        <!-- SEARCH -->
        <div class="max-w-2xl mx-auto mt-4">
          <div class="flex gap-3 bg-white rounded-2xl shadow-lg p-3 border border-slate-200">
            <div class="flex-1 flex items-center gap-3 px-2">
              <Search class="w-6 h-6 text-slate-500" />
              <Input
                type="text"
                :placeholder="t.searchPlaceholder"
                class="text-lg border-0 focus:ring-0"
              />
            </div>
            <Button class="px-8 py-2 text-lg bg-blue-700 hover:bg-blue-800">
              {{ t.searchButton }}
            </Button>
          </div>
        </div>
      </div>

      <!-- FILTERS -->
      <h2 class="text-2xl font-semibold text-center text-slate-800 mb-4">
        {{ t.filterBy }}
      </h2>

      <Tabs default-value="activities" class="w-full">
        <TabsList class="grid w-full max-w-lg mx-auto grid-cols-2 mb-4 text-lg">
          <TabsTrigger value="activities">
            {{ t.activities }}
          </TabsTrigger>
          <TabsTrigger value="facilities">
            {{ t.facilities }}
          </TabsTrigger>
        </TabsList>

        <!-- ACTIVITIES -->
        <TabsContent value="activities">
          <div class="grid md:grid-cols-3 gap-6">
            <FilterCard
              :icon="Calendar"
              :title="t.dayOfWeek"
              @click="dayFilterOpen = true"
            />
            <FilterCard
              :icon="Activity"
              :title="t.activityType"
              @click="activityTypeFilterOpen = true"
            />
            <FilterCard
              :icon="Clock"
              :title="t.sessionTime"
              @click="activityTimeFilterOpen = true"
            />
          </div>
        </TabsContent>

        <!-- FACILITIES -->
        <TabsContent value="facilities">
          <div class="grid md:grid-cols-2 gap-6 max-w-3xl mx-auto">
            <FilterCard
              :icon="Building2"
              :title="t.facilityType"
              @click="facilityTypeFilterOpen = true"
            />
            <FilterCard
              :icon="Clock"
              :title="t.openingHours"
              @click="facilityTimeFilterOpen = true"
            />
          </div>
        </TabsContent>
      </Tabs>

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
import { ref, computed } from "vue";
import {
  Search,
  Activity,
  Building2,
  Clock,
  Calendar,
} from "lucide-vue-next";

import Button from "./ui/Button.vue";
import Input from "./ui/Input.vue";
import Tabs from "./ui/Tabs.vue";
import TabsList from "./ui/TabsList.vue";
import TabsTrigger from "./ui/TabsTrigger.vue";
import TabsContent from "./ui/TabsContent.vue";

import FilterCard from "./filters/FilterCard.vue";
import DayOfWeekFilter from "./filters/DayOfWeekFilter.vue";
import ActivityTypeFilter from "./filters/ActivityTypeFilter.vue";
import TimeRangeFilter from "./filters/TimeRangeFilter.vue";
import FacilityTypeFilter from "./filters/FacilityTypeFilter.vue";


/* ------------------ Estados ------------------ */
const dayFilterOpen = ref(false);
const activityTypeFilterOpen = ref(false);
const activityTimeFilterOpen = ref(false);
const facilityTypeFilterOpen = ref(false);
const facilityTimeFilterOpen = ref(false);

const language = ref<"es" | "en">("es");

const selectedDays = ref<string[]>([]);
const selectedActivityTypes = ref<string[]>([]);
const activityStartTime = ref("");
const activityEndTime = ref("");

const selectedFacilityTypes = ref<string[]>([]);
const facilityStartTime = ref("");
const facilityEndTime = ref("");

/* ------------------ Traducciones ------------------ */
const translations = {
  es: {
    home: "Inicio",
    forum: "Foro",
    contact: "Contacto",
    faq: "FAQ",
    login: "Log-in",
    welcome: "Bienvenido al Polideportivo XX",
    welcome2: "Inicia sesión para acceder a todas las funcionalidades",
    searchPlaceholder: "Buscar actividades o instalaciones...",
    searchButton: "Buscar",
    filterBy: "Filtrar por",
    activities: "Actividades",
    facilities: "Instalaciones",
    dayOfWeek: "Día de la semana",
    activityType: "Tipo de actividad",
    sessionTime: "Horario de sesión",
    facilityType: "Tipo de instalación",
    openingHours: "Horario de apertura",
  },
  en: {
    home: "Home",
    forum: "Forum",
    contact: "Contact",
    faq: "FAQ",
    login: "Log-in",
    welcome: "Welcome to Sports Center XX",
    welcome2: "Log in to access all features",
    searchPlaceholder: "Search activities or facilities...",
    searchButton: "Search",
    filterBy: "Filter by",
    activities: "Activities",
    facilities: "Facilities",
    dayOfWeek: "Day of the week",
    activityType: "Activity type",
    sessionTime: "Session time",
    facilityType: "Facility type",
    openingHours: "Opening hours",
  },
};

const t = computed(() => translations[language.value]);

const toggleLanguage = () => {
  language.value = language.value === "es" ? "en" : "es";
};
</script>
