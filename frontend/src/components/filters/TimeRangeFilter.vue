<script setup lang="ts">
import { watch, type Ref, ref, inject } from 'vue';
import Modal from "@/components/ui/Modal.vue";
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const props = defineProps<{
  open: boolean;
  startTime: string;
  endTime: string;
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

const error = ref(false);

const apply = () => {
  if (start.value > end.value) {
    error.value = true;
    return;
  }

  error.value = false;
  emit("apply", { start: start.value, end: end.value });
  emit("update:open", false);
};
</script>

<template>
  <Modal :open="open" @update:open="emit('update:open', $event)">

    <h3 class="fs-4 fw-semibold mb-2 mt-4">
      {{ t.sessionTime }}
    </h3>

    <p class="text-secondary mb-3">
      {{ t.subtitleHours }}
    </p>

    <div class="d-flex gap-3 mb-3">
      <input type="time" class="form-control" v-model="start" />
      <input type="time" class="form-control" v-model="end" />
    </div>

    <div v-if="error" class="alert alert-danger py-2 mt-3">
      {{ t.invalidTimeRange }}
    </div>

    <div class="d-flex justify-content-end">
      <button class="btn btn-primary px-3" @click="apply()">
        {{t.apply}}
      </button>
    </div>

  </Modal>
</template>
