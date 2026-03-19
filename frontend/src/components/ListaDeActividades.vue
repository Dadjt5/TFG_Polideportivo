<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #fff4e0, #e0f7ff);">
    <main class="container py-5" style="max-width: 1120px;">

    <!-- HEADER -->
    <div class="text-center mb-5">
      <h1 class="fw-bold text-primary">{{ t.activities }}</h1>
    </div>

    <div class="tab-content">
      <div class="row g-4">
        <div class="col-md-4">
          <FilterCard :icon="Calendar" :title="t.dayOfWeek" :subtitle="orderedSelectedDays.join(', ')"
            @click="activar('A1')" :theme="'light'"/>
        </div>

        <div class="col-md-4">
          <FilterCard :icon="Activity" :title="t.activityType" :subtitle="selectedActivityTypes.join(', ')"
            @click="activar('A2')" :theme="'light'"/>
        </div>

        <div class="col-md-4">
          <FilterCard :icon="Clock" :title="t.sessionTime"
            :subtitle="activityStartTime || activityEndTime ? `${activityStartTime} - ${activityEndTime}` : ''"
            @click="activar('A3')" :theme="'light'"/>
        </div>
      </div>
    </div>

    <DayOfWeekFilter :open="dayFilterOpen" @update:open="dayFilterOpen = $event" :selectedDays="selectedDays"
      @apply="selectedDays = $event" :theme="'light'"/>

    <ActivityTypeFilter :open="activityTypeFilterOpen" @update:open="activityTypeFilterOpen = $event"
      :selectedTypes="selectedActivityTypes" @apply="selectedActivityTypes = $event" :theme="'light'"/>

    <TimeRangeFilter :open="activityTimeFilterOpen" @update:open="activityTimeFilterOpen = $event"
      :startTime="activityStartTime" :endTime="activityEndTime"
      @apply="({ start, end }) => { activityStartTime = start; activityEndTime = end }" :theme="'light'"/>


    <div class="row g-4 mt-5">
      <div v-for="actividad in actividadesFiltradas" :key="actividad.id" class="col-12 col-sm-6 col-lg-4"
        @click="activityDetail(actividad.id)">
        <ActivityCard :icon="Activity" :actividad="actividad" :theme="'light'"/>
      </div>

      <div v-if="!actividadesFiltradas.length" class="text-center text-muted py-5">
        <i class="bi bi-emoji-frown fs-1 d-block mb-3"></i>
        {{ t.noResults }}
      </div>
    </div>
  </main>
  </div>
</template>


<script setup lang="ts">
import { computed, onMounted, ref, inject, type Ref } from "vue"
import { useRouter } from "vue-router"
import {
  Activity,
  Clock,
  Calendar
} from "lucide-vue-next";
import FilterCard from "@/components/filters/FilterCard.vue";
import DayOfWeekFilter from "@/components/filters/DayOfWeekFilter.vue";
import ActivityTypeFilter from "@/components/filters/ActivityTypeFilter.vue";
import TimeRangeFilter from "@/components/filters/TimeRangeFilter.vue";
import ActivityCard from '@/components/filters/ActivityCard.vue'

import { getActividades } from "@/services/listadoService"

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter()

const dayFilterOpen = ref(false);
const activityTypeFilterOpen = ref(false);
const activityTimeFilterOpen = ref(false);

const selectedDays = ref<string[]>([]);
const selectedActivityTypes = ref<string[]>([]);
const activityStartTime = ref("");
const activityEndTime = ref("");

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

const actividades = ref<any[]>([])

const activar = (tipo: string) => {
  if (tipo === 'A1') {
    dayFilterOpen.value = !dayFilterOpen.value;

    activityTypeFilterOpen.value = false;
    activityTimeFilterOpen.value = false;
  } else if (tipo === 'A2') {
    activityTypeFilterOpen.value = !activityTypeFilterOpen.value;

    dayFilterOpen.value = false;
    activityTimeFilterOpen.value = false;
  } else if (tipo === 'A3') {
    activityTimeFilterOpen.value = !activityTimeFilterOpen.value;

    dayFilterOpen.value = false;
    activityTypeFilterOpen.value = false;
  }
};

const actividadesFiltradas = computed(() => {
  return actividades.value.filter(act => {

    if (selectedDays.value.length) {
      const diasActividad = Array.isArray(act.dias)
        ? act.dias
        : act.dias?.split(",").map((d: string) => d.trim())

      const coincideDia = selectedDays.value.some(d =>
        diasActividad?.includes(d)
      )

      if (!coincideDia) return false
    }

    if (selectedActivityTypes.value.length) {
      if (!selectedActivityTypes.value.includes(act.tipoActividad)) {
        return false
      }
    }

    if (activityStartTime.value || activityEndTime.value) {
      if (activityStartTime.value && act.horaInicio < activityStartTime.value) {
        return false
      }
      if (activityEndTime.value && act.horaFin > activityEndTime.value) {
        return false
      }
    }

    return true
  })
})

const activityDetail = (id: number) => {
  router.push({
    name: 'detalle-actividad',
    params: { id }
  });
}

onMounted(async () => {
  try {
    actividades.value = await getActividades()
  } catch (e) {
    console.log("Error al obtener las actividades", e)
  }
})
</script>


<style scoped>
.activity-card {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.activity-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 0.75rem 1.5rem rgba(0, 0, 0, 0.15);
}

.card-img-top {
  height: 160px;
  object-fit: cover;
}
</style>
