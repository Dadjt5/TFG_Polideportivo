<script setup lang="ts">
defineProps<{
  open: boolean;
}>();

const emit = defineEmits<{
  (e: "update:open", value: boolean): void;
}>();
</script>

<template>
  <div
    v-if="open"
    class="fixed inset-0 z-50 flex items-center justify-center"
  >
    <!-- Overlay -->
    <div
      class="absolute inset-0 bg-black/40"
      @click="emit('update:open', false)"
    />

    <!-- Content -->
    <div
      class="relative bg-white rounded-2xl shadow-xl w-full max-w-lg p-6"
    >
      <slot />
    </div>
  </div>
</template>
