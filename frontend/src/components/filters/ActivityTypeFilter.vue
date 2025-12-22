<script setup lang="ts">
import { ref } from "vue";
import Modal from "../ui/Modal.vue";
import Button from "../ui/Button.vue";

const props = defineProps<{
  open: boolean;
  selectedTypes: string[];
}>();

const emit = defineEmits<{
  (e: "update:open", value: boolean): void;
  (e: "apply", value: string[]): void;
}>();

const types = [
  "Fitness",
  "Natación",
  "Artes marciales",
  "Deportes colectivos",
  "Yoga",
];

const localSelection = ref([...props.selectedTypes]);

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
</script>

<template>
  <Modal :open="open" @update:open="emit('update:open', $event)">
    <h3 class="text-xl font-semibold mb-4">
      Tipo de actividad
    </h3>

    <div class="grid grid-cols-1 gap-3 mb-6">
      <button
        v-for="type in types"
        :key="type"
        @click="toggleType(type)"
        class="rounded-xl px-4 py-2 border transition text-left"
        :class="localSelection.includes(type)
          ? 'bg-blue-600 text-white'
          : 'bg-white text-slate-700'"
      >
        {{ type }}
      </button>
    </div>

    <div class="flex justify-end">
      <Button @click="apply">Aplicar</Button>
    </div>
  </Modal>
</template>
