<script setup lang="ts">
import { type Ref, inject, computed } from 'vue';
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";
import { useUserStore } from '@/stores/usuarioFinal';

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const usuarioFinalStore = useUserStore();

const props = defineProps<{
  actividad: {
    id: number
    nombre: string
    tipoActividad: string
    imagenURL: string
    plazasMaximas: number
    plazasReservadas: number
    edadMinima: number
    año: number
    numeroCreditos: number
    nivel: string
    material: string
    exterior: boolean
    tipoReserva: string
    terreno: string
    periodo: string
    estado: string
    horasSemanales: number
    nombreMonitor: string
    nombreDeporte: string
    dias: string
  }
  icon: any
  theme?: 'light' | 'dark';
}>()

const cambiarFavorito = () => {
  usuarioFinalStore.marcarActividadFavorita(props.actividad.id)
}

// Clases dinámicas según theme
const cardClass = computed(() =>
  props.theme === 'dark'
    ? 'card shadow-sm h-100 activity-card bg-white bg-opacity-10 border border-white border-opacity-25'
    : 'card shadow-sm h-100 activity-card bg-light border border-dark'
)

const textClass = computed(() =>
  props.theme === 'dark' ? 'text-white' : 'text-dark'
)

const textOpacityClass = computed(() =>
  props.theme === 'dark' ? 'text-white text-opacity-75' : 'text-dark text-opacity-75'
)

const iconWrapperClass = computed(() =>
  props.theme === 'dark' ? 'icon-wrapper bg-white bg-opacity-10' : 'icon-wrapper bg-light'
)

const badgeClass = computed(() =>
  props.theme === 'dark' ? 'badge rounded-pill bg-success bg-opacity-75 text-white' : 'badge rounded-pill bg-success text-dark'
)
</script>

<template>
  <div :class="cardClass">
    <div class="card-body">

      <div class="d-flex justify-content-between align-items-start mb-3">

        <div class="d-flex align-items-start gap-3">

          <div :class="iconWrapperClass">
            <component :is="icon" class="icon text-primary" />
          </div>

          <div>
            <h5 class="mb-1" :class="textClass">{{ actividad.nombre }}</h5>
            <span :class="badgeClass">
              {{ t.activity }}
            </span>
          </div>
        </div>

        <button v-if="usuarioFinalStore.isLogged" class="btn btn-link p-0 text-warning" @click.stop="cambiarFavorito">
          <i :class="[
            'bi',
            usuarioFinalStore.activityIsFavorite(actividad.id) ? 'bi-star-fill' : 'bi-star'
          ]" class="fs-4"></i>
        </button>

      </div>

      <div :class="['small', textOpacityClass]">
        <div class="d-flex justify-content-between mb-1">
          <span>{{ t.days }}</span>
          <strong>{{ actividad.dias }}</strong>
        </div>

        <div class="d-flex justify-content-between mb-1">
          <span>{{ t.places }}</span>
          <strong>
            {{ actividad.plazasReservadas }}/{{ actividad.plazasMaximas }}
          </strong>
        </div>

        <div class="d-flex justify-content-between">
          <span>{{ t.weekHours }}</span>
          <strong>{{ actividad.horasSemanales }} h</strong>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.activity-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.activity-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 0.75rem 1.5rem rgba(0, 0, 0, 0.25);
}

.icon-wrapper {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon {
  width: 20px;
  height: 20px;
}
</style>