<script setup lang="ts">
import { watch, type Ref, ref, inject, computed } from 'vue';
import Modal from "@/components/ui/Modal.vue";
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

import { useEstadisticasStore } from "@/stores/estadisticas";

const estadisticasStore = useEstadisticasStore();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const props = defineProps<{
  open: boolean;
  selectedTypes: string[];
  theme?: 'light' | 'dark';
}>();

const emit = defineEmits<{
  (e: "update:open", value: boolean): void;
  (e: "apply", value: string[]): void;
}>();

const localSelection = ref([...props.selectedTypes]);

watch(
  () => props.selectedTypes,
  (value) => {
    localSelection.value = [...value];
  },
  { immediate: true }
);

const toggleType = (type: string) => {
  if (localSelection.value.includes(type)) {
    localSelection.value = localSelection.value.filter(t => t !== type);
  } else {
    localSelection.value.push(type);
  }
};

const apply = () => {
  emit("apply", localSelection.value);
  emit("update:open", false);
};

// Computed para clases de botones según theme y selección
const buttonClasses = (selected: boolean) => {
  if (props.theme === 'dark') {
    return selected
      ? 'btn btn-primary text-white'
      : 'btn btn-outline-light text-white text-opacity-75';
  } else {
    return selected
      ? 'btn btn-dark text-white'
      : 'btn btn-outline-dark text-dark text-opacity-75';
  }
};

// Clase para el título según theme
const titleClass = computed(() =>
  props.theme === 'dark'
    ? 'fs-4 fw-semibold mb-3 mt-4 text-white text-center'
    : 'fs-4 fw-semibold mb-3 mt-4 text-dark text-center'
);

// Clase para el botón de aplicar según theme
const applyBtnClass = computed(() =>
  props.theme === 'dark' ? 'btn btn-primary px-3' : 'btn btn-dark px-3'
);
</script>

<template>
  <Modal :open="open" :theme="props.theme" @update:open="emit('update:open', $event)">

    <h3 :class="titleClass">
      {{ t.facilityType }}
    </h3>

    <div style="max-width: 750px; margin: 0 auto;" class="d-grid gap-3 mb-4">
      <button
        v-for="type in estadisticasStore.data.tiposInstalacion"
        :key="type[0]"
        type="button"
        :class="buttonClasses(localSelection.includes(type[1]))"
        @click="toggleType(type[1])"
      >
        {{ type[1] }}
      </button>
    </div>

    <div class="d-flex justify-content-center mb-3">
      <button :class="applyBtnClass" @click="apply()">
        {{ t.apply }}
      </button>
    </div>

  </Modal>
</template>