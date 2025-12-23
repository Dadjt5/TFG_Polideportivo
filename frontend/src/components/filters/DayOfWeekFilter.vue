<script setup lang="ts">
import { ref, watch } from "vue";
import Modal from "../ui/Modal.vue";
import Button from "../ui/Button.vue";

const props = defineProps<{
  open: boolean;
  selectedDays: string[];
}>();

const emit = defineEmits<{
  (e: "update:open", value: boolean): void;
  (e: "apply", value: string[]): void;
}>();

// Lista de días de la semana
const days = [
  "Lunes",
  "Martes",
  "Miércoles",
  "Jueves",
  "Viernes",
  "Sábado",
  "Domingo",
];

// Copia local de la selección para poder modificarla sin afectar el prop directamente
const localSelection = ref<string[]>([...props.selectedDays]);

// Mantener la copia local sincronizada si cambia el prop
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

// Limpiar selección
const clear = () => {
  localSelection.value = [];
};
</script>

<template>
  <Modal :open="open" @update:open="emit('update:open', $event)">
    <h3 class="text-xl font-semibold mb-4">Día de la semana</h3>

    <!-- Botones para cada día -->
    <div class="grid grid-cols-2 gap-3 mb-6">
      <button
        v-for="day in days"
        :key="day"
        @click="toggleDay(day)"
        class="rounded-xl px-4 py-2 border transition"
        :class="localSelection.includes(day)
          ? 'bg-blue-600 text-white'
          : 'bg-white text-slate-700 hover:bg-slate-100'"
      >
        {{ day }}
      </button>
    </div>

    <!-- Botones de acción -->
    <div class="flex justify-between">
      <Button variant="outline" @click="clear">Limpiar</Button>
      <Button @click="apply">Aplicar</Button>
    </div>
  </Modal>
</template>
