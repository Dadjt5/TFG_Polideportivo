<script setup lang="ts">
import { ref, watch } from "vue";
import Modal from "../ui/Modal.vue";
import Button from "../ui/Button.vue";

const props = defineProps<{
  open: boolean;
  startTime: string;
  endTime: string;
  title: string;
  description?: string;
}>();

const emit = defineEmits<{
  (e: "update:open", value: boolean): void;
  (e: "apply", payload: { start: string; end: string }): void;
}>();

const start = ref(props.startTime);
const end = ref(props.endTime);

// Sincronizar con props cuando el modal se abre/cierra
watch(
  () => props.open,
  () => {
    start.value = props.startTime;
    end.value = props.endTime;
  }
);

const apply = () => {
  emit("apply", { start: start.value, end: end.value });
  emit("update:open", false);
};
</script>

<template>
  <Modal :open="open" @update:open="emit('update:open', $event)">

    <h3 class="fs-4 fw-semibold mb-2 mt-4">
      {{ title }}
    </h3>

    <p v-if="description" class="text-secondary mb-3">
      {{ description }}
    </p>

    <div class="d-flex gap-3 mb-3">
      <input type="time" class="form-control" v-model="start" />
      <input type="time" class="form-control" v-model="end" />
    </div>

    <div class="d-flex justify-content-end">
      <button class="btn btn-primary px-3" @click="apply()">
        Aplicar
      </button>
    </div>

  </Modal>
</template>
