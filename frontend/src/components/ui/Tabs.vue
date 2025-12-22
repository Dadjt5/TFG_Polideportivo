<script setup lang="ts">
import { provide, ref } from "vue";

const props = defineProps<{
  defaultValue: string;
}>();

const activeTab = ref(props.defaultValue);

provide("activeTab", activeTab);
provide("setActiveTab", (value: string) => {
  activeTab.value = value;
});
</script>

<template>
  <div>
    <slot />
  </div>
</template>
