<script setup lang="ts">
defineProps<{
  title: string;
  icon?: any; // opcional
}>();
</script>

<template>
  <div
    @click="$emit('click')"
    class="
      cursor-pointer bg-white rounded-2xl shadow-md
      border border-slate-200
      p-6 flex flex-col items-center justify-center
      gap-3 hover:shadow-lg transition
    "
  >
    <component :is="icon" class="w-8 h-8 text-blue-600" />
    <p class="text-lg font-medium text-slate-700 text-center">
      {{ title }}
    </p>
  </div>
</template>
