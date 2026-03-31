<script setup lang="ts">
import { type Ref, inject, computed } from 'vue';
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";
import { useUserStore } from '@/stores/usuarioFinal';

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const usuarioFinalStore = useUserStore();

const props = defineProps<{
  instalacion: {
    id: number;
    nombre: string;
    tipoInstalacion: string;
    pabellon?: {
      nombre: string;
      direccion: string;
    };
  };
  icon: any;
  theme?: 'light' | 'dark';
}>();

const cambiarFavorito = () => {
  usuarioFinalStore.marcarInstalacionFavorita(props.instalacion.id);
};

// Computed para clases dinámicas según el tema
const cardClass = computed(() =>
  props.theme === 'dark'
    ? 'card shadow-sm h-100 installation-card bg-white bg-opacity-10 border border-white border-opacity-25'
    : 'card shadow-sm h-100 installation-card bg-light bg-opacity-50 border border-dark border-opacity-25'
);

const textClass = computed(() =>
  props.theme === 'dark'
    ? 'text-white text-opacity-75 small'
    : 'text-dark text-opacity-75 small'
);

const iconWrapperClass = computed(() =>
  props.theme === 'dark'
    ? 'icon-wrapper bg-white bg-opacity-10'
    : 'icon-wrapper bg-dark bg-opacity-10'
);

const titleClass = computed(() =>
  props.theme === 'dark' ? 'mb-1 text-white' : 'mb-1 text-dark'
);

const badgeClass = computed(() =>
  props.theme === 'dark'
    ? 'badge rounded-pill bg-success bg-opacity-75 text-white'
    : 'badge rounded-pill bg-success bg-opacity-50 text-dark'
);
</script>

<template>
  <div :class="cardClass">
    <div class="card-body">

      <div class="d-flex justify-content-between align-items-start mb-3">

        <div class="d-flex align-items-start gap-3">
          <div :class="iconWrapperClass">
            <component :is="icon" :class="props.theme === 'dark' ? 'icon text-white' : 'icon text-dark'" />
          </div>

          <div>
            <h5 :class="titleClass">{{ instalacion.nombre }}</h5>
            <span :class="badgeClass">{{ t.facility }}</span>
          </div>
        </div>

        <button v-if="usuarioFinalStore.isLogged" class="btn btn-link p-0 text-warning" @click.stop="cambiarFavorito">
          <i :class="[
            'bi',
            usuarioFinalStore.facilityIsFavorite(instalacion.id) ? 'bi-star-fill' : 'bi-star'
          ]" class="fs-4"></i>
        </button>

      </div>

      <div :class="textClass">
        <div class="d-flex justify-content-between mb-1">
          <span>{{ t.facilityType }}</span>
          <strong>{{ instalacion.tipoInstalacion }}</strong>
        </div>

        <div v-if="instalacion.pabellon" class="d-flex justify-content-between">
          <span>{{ t.pavilion }}</span>
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