<script setup lang="ts">
import { ref, watch } from "vue";
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


const localSelection = ref<string[]>([]);

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
</script>

<template>
  <Modal :open="open" @update:open="emit('update:open', $event)">

    <h3 class="fs-4 fw-semibold mb-4 mt-4">
      Tipo de actividad
    </h3>

    <div class="d-grid gap-3 mb-4">
      <button
        v-for="type in types"
        :key="type"
        type="button"
        class="btn text-start"
        :class="localSelection.includes(type)
          ? 'btn-primary'
          : 'btn-outline-secondary'"
        @click="toggleType(type)"
      >
        {{ type }}
      </button>
    </div>

    <div class="d-flex justify-content-end">
      <button class="btn btn-primary px-3" @click="apply()">
        Aplicar
      </button>
    </div>

  </Modal>
</template>
