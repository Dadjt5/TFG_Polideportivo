<script setup lang="ts">
import { type Ref, inject } from 'vue';
import type { Language } from "../../useI18N";
import { useI18n } from "../../useI18N";

import { useUserStore } from '../../stores/usuarioFinal';

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const usuarioFinalStore = useUserStore();

const props = defineProps<{
  instalacion: {
    id: number
    nombre: string
    horaApertura: string
    horaCierre: string
    pabellon?: {
      nombre: string
      direccion: string
    }
  }
  icon: any
}>()

const cambiarFavorito = () => {
  usuarioFinalStore.marcarInstalacionFavorita(props.instalacion.id)
}
</script>

<template>
  <div class="card shadow-sm h-100 installation-card">
    <div class="card-body">

      <div class="d-flex justify-content-between align-items-start mb-3">

        <div class="d-flex align-items-start gap-3">

          <div class="icon-wrapper bg-primary-subtle">
            <component :is="icon" class="icon text-primary" />
          </div>

          <div>
            <h5 class="mb-1">{{ instalacion.nombre }}</h5>
            <span class="badge rounded-pill text-bg-success">
              {{ t.facility }}
            </span>
          </div>
        </div>

        <button v-if="usuarioFinalStore.isLogged" class="btn btn-link p-0 text-warning" @click.stop="cambiarFavorito">
          <i :class="[
            'bi',
            usuarioFinalStore.facilityIsFavorite(instalacion.id) ? 'bi-star-fill' : 'bi-star'
          ]" class="fs-4"></i>
        </button>

      </div>

      <div class="text-muted small">
        <div class="d-flex justify-content-between mb-1">
          <span>{{ t.schedule }}</span>
          <strong>
            {{ instalacion.horaApertura }} - {{ instalacion.horaCierre }}
          </strong>
        </div>

        <div v-if="instalacion.pabellon" class="d-flex justify-content-between">
          <span>{{ t.pavilions }}</span>
          <strong>{{ instalacion.pabellon.nombre }}</strong>
        </div>
      </div>

    </div>
  </div>
</template>


<style scoped>
.installation-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.installation-card:hover {
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
