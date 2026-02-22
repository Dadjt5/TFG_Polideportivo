<script setup lang="ts">
import { watch, type Ref, ref, inject, computed } from 'vue';
import Modal from "@/components/ui/Modal.vue";
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const props = defineProps<{
  open: boolean;
  startTime: string;
  endTime: string;
  theme?: 'light' | 'dark';
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

// Clases dinámicas según el theme
const inputClasses = computed(() => {
  return [
    'form-control',
    'rounded-3',
    'border',
    props.theme === 'dark'
      ? 'bg-white bg-opacity-10 text-white border-white border-opacity-25'
      : 'bg-light text-dark border-dark'
  ].join(' ');
});

// Mensaje de error segun theme
const errorClasses = computed(() => {
  return props.theme === 'dark'
    ? 'alert alert-danger py-2 mt-3 text-white text-opacity-75'
    : 'alert alert-danger py-2 mt-3 text-dark';
});
</script>

<template>
  <Modal :open="open" :theme="props.theme" @update:open="emit('update:open', $event)">

    <h3 :class="['fs-4 fw-semibold mb-2 mt-4 text-center', props.theme === 'dark' ? 'text-white' : 'text-dark']">
      {{ t.sessionTime }}
    </h3>

    <p :class="['mb-3 text-center', props.theme === 'dark' ? 'text-white text-opacity-75' : 'text-muted']">
      {{ t.subtitleHours }}
    </p>

    <div style="max-width: 1000px; margin: 0 auto;" class="d-flex gap-3 mb-4 px-3">
      <input type="time" :class="inputClasses" v-model="start" />
      <input type="time" :class="inputClasses" v-model="end" />
    </div>

    <div v-if="error" :class="errorClasses">
      {{ t.invalidTimeRange }}
    </div>

    <div class="d-flex justify-content-center mb-3">
      <button :class="['btn px-3', props.theme === 'dark' ? 'btn-primary' : 'btn-dark']" @click="apply()">
        {{ t.apply }}
      </button>
    </div>

  </Modal>
</template>

<style scoped>
input[type="time"] {
  color-scheme: dark;
}
</style>