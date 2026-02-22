<script setup lang="ts">
import { ref, watch, inject, type Ref, computed } from "vue";
import Modal from "@/components/ui/Modal.vue";
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const props = defineProps<{
  open: boolean;
  selectedDays: string[];
  theme?: 'light' | 'dark';
}>();

const emit = defineEmits<{
  (e: "update:open", value: boolean): void;
  (e: "apply", value: string[]): void;
}>();

// Lista de días de la semana
const days = [
  t.value.monday,
  t.value.tuesday,
  t.value.wednesday,
  t.value.thursday,
  t.value.friday,
  t.value.saturday,
  t.value.sunday,
];

// Copia local de la selección
const localSelection = ref<string[]>([...props.selectedDays]);

watch(() => props.selectedDays, (newVal) => {
  localSelection.value = [...newVal];
});

// Alternar la selección de un día
const toggleDay = (day: string) => {
  if (localSelection.value.includes(day)) {
    localSelection.value = localSelection.value.filter(d => d !== day);
  } else {
    localSelection.value.push(day);
  }
};

// Aplicar cambios y cerrar modal
const apply = () => {
  emit("apply", localSelection.value);
  emit("update:open", false);
};

// Computed para clases según el tema
const buttonClass = (day: string) => {
  const selected = localSelection.value.includes(day);
  if (props.theme === 'dark') {
    return selected ? 'btn btn-primary text-white' : 'btn btn-outline-light text-white text-opacity-75';
  } else {
    return selected ? 'btn btn-primary text-dark' : 'btn btn-outline-secondary text-dark text-opacity-75';
  }
};

const titleClass = computed(() => props.theme === 'dark' ? 'fs-4 fw-semibold mb-4 mt-4 text-white text-center' : 'fs-4 fw-semibold mb-4 mt-4 text-dark text-center');
</script>

<template>
  <Modal :open="open" :theme="props.theme" @update:open="emit('update:open', $event)">
    <h3 :class="titleClass">
      {{ t.dayOfWeek }}
    </h3>

    <!-- Botones para cada día -->
    <div style="max-width: 750px; margin: 0 auto;" class="d-grid gap-3 mb-4">
      <button
        v-for="day in days"
        :key="day"
        type="button"
        :class="buttonClass(day)"
        @click="toggleDay(day)"
      >
        {{ day }}
      </button>
    </div>

    <!-- Botones de acción -->
    <div class="d-flex justify-content-center mb-3">
      <button :class="props.theme === 'dark' ? 'btn btn-primary px-3' : 'btn btn-primary px-3'" @click="apply()">
        {{ t.apply }}
      </button>
    </div>
  </Modal>
</template>