<script setup lang="ts">
  defineProps<{
    type?: "button" | "submit" | "reset";
    disabled?: boolean;
  }>();
</script>

<template>
  <button
    :type="type || 'button'"
    :disabled="disabled"
    class="
      inline-flex items-center justify-center
      rounded-xl px-4 py-2
      font-medium transition
      bg-blue-700 text-white
      hover:bg-blue-800
      focus:outline-none focus:ring-2 focus:ring-blue-400
      disabled:opacity-50 disabled:pointer-events-none
    "
  >
    <slot />
  </button>
</template>
