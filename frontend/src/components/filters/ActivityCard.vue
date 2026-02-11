<script setup lang="ts">
import { type Ref, inject } from 'vue';

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
    dias: string
  }
  icon: any
}>()

const cambiarFavorito = () => {
  usuarioFinalStore.marcarActividadFavorita(props.actividad.id)
}

</script>

<template>
  <div class="card shadow-sm h-100 activity-card">
    <div class="card-body">

      <div class="d-flex justify-content-between align-items-start mb-3">

        <div class="d-flex align-items-start gap-3">

          <div class="icon-wrapper bg-primary-subtle">
            <component :is="icon" class="icon text-primary" />
          </div>

          <div>
            <h5 class="mb-1">{{ actividad.nombre }}</h5>
            <span class="badge rounded-pill text-bg-primary">
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

      <div class="text-muted small">
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
  box-shadow: 0 0.75rem 1.5rem rgba(0, 0, 0, 0.15);
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
