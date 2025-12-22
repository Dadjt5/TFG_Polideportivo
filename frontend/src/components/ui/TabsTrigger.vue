<script setup lang="ts">
import { inject, computed } from "vue";

const props = defineProps<{
  value: string;
}>();

const activeTab = inject<any>("activeTab");
const setActiveTab = inject<any>("setActiveTab");

const isActive = computed(() => activeTab.value === props.value);
</script>

<template>
  <button
    @click="setActiveTab(value)"
    class="w-full px-4 py-2 rounded-lg transition"
    :class="isActive
      ? 'bg-white shadow font-semibold'
      : 'text-slate-600 hover:bg-white/50'"
  >
    <slot />
  </button>
</template>
