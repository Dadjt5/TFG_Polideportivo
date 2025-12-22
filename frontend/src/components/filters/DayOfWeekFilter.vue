<script setup lang="ts">
import { ref } from "vue";
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

const days = [
  "Lunes",
  "Martes",
  "Miércoles",
  "Jueves",
  "Viernes",
  "Sábado",
  "Domingo",
];

const localSelection = ref([...props.selectedDays]);

const toggleDay = (day: string) => {
  if (localSelection.value.includes(day)) {
    localSelection.value = localSelection.value.filter(d => d !== day);
  } else {
    localSelection.value.push(day);
  }
};

const apply = () => {
  emit("apply", localSelection.value);
  emit("update:open", false);
};
</script>

<template>
  <Modal :open="open" @update:open="emit('update:open', $event)">
    <h3 class="text-xl font-semibold mb-4">
      Día de la semana
    </h3>

    <div class="grid grid-cols-2 gap-3 mb-6">
      <button
        v-for="day in days"
        :key="day"
        @click="toggleDay(day)"
        class="rounded-xl px-4 py-2 border transition"
        :class="localSelection.includes(day)
          ? 'bg-blue-600 text-white'
          : 'bg-white text-slate-700'"
      >
        {{ day }}
      </button>
    </div>

    <div class="flex justify-end">
      <Button @click="apply">Aplicar</Button>
    </div>
  </Modal>
</template>
