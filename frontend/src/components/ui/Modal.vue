<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  open: boolean;
  theme?: 'light' | 'dark';
}>();

const emit = defineEmits<{
  (e: "update:open", value: boolean): void;
}>();

// Clases dinámicas según theme
const overlayClass = computed(() =>
  props.theme === 'dark' ? 'absolute inset-0 bg-black/40' : 'absolute inset-0 bg-gray-200/40'
)

const contentClass = computed(() =>
  props.theme === 'dark'
    ? 'relative bg-white bg-opacity-10 backdrop-blur border border-white border-opacity-25 rounded-2xl shadow-xl w-full max-w-lg p-6'
    : 'relative bg-white/90 border border-gray-300 rounded-2xl shadow-lg w-full max-w-lg p-6'
)
</script>

<template>
  <div
    v-if="open"
    class="fixed inset-0 z-50 flex items-center justify-center mt-4"
    style="max-width: 1000px; margin: 0 auto;"
  >
    <!-- Overlay -->
    <div
      :class="overlayClass"
      @click="emit('update:open', false)"
    />

    <!-- Content -->
    <div :class="contentClass">
      <slot />
    </div>
  </div>
</template>