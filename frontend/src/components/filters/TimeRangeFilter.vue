<script setup lang="ts">
import { ref, watch } from "vue";
import Modal from "../ui/Modal.vue";
import Button from "../ui/Button.vue";
import Input from "../ui/Input.vue";

const props = defineProps<{
  open: boolean;
  startTime: string;
  endTime: string;
  title: string;
  description?: string;
}>();

const emit = defineEmits<{
  (e: "update:open", value: boolean): void;
  (e: "apply", start: string, end: string): void;
}>();

const start = ref(props.startTime);
const end = ref(props.endTime);

watch(
  () => props.open,
  () => {
    start.value = props.startTime;
    end.value = props.endTime;
  }
);

const apply = () => {
  emit("apply", start.value, end.value);
  emit("update:open", false);
};
</script>

<template>
  <Modal :open="open" @update:open="emit('update:open', $event)">
    <h3 class="text-xl font-semibold mb-2">
      {{ title }}
    </h3>

    <p v-if="description" class="text-slate-600 mb-4">
      {{ description }}
    </p>

    <div class="flex gap-4 mb-6">
      <Input type="time" v-model="start" />
      <Input type="time" v-model="end" />
    </div>

    <div class="flex justify-end">
      <Button @click="apply">Aplicar</Button>
    </div>
  </Modal>
</template>
