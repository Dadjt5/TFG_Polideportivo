<script setup lang="ts">
import { watch, type Ref, ref, inject, computed } from 'vue';

const props = defineProps<{
  title: string;
  subtitle?: string;
  icon: any;
  theme?: 'light' | 'dark';
}>();

const titleClass = computed(() =>
  props.theme === 'dark' ? 'fs-5 fw-medium text-white mb-0' : 'fs-5 fw-medium text-dark mb-0'
);

const subtitleClass = computed(() =>
  props.theme === 'dark'
    ? 'text-sm text-white text-opacity-75 text-center'
    : 'text-sm text-dark text-opacity-75 text-center'
);

const cardClass = computed(() =>
  props.theme === 'dark'
    ? 'card text-center h-100 bg-white bg-opacity-10 backdrop-blur border border-white border-opacity-25 rounded-4 p-4 transition cursor-pointer'
    : 'card text-center h-100 bg-light bg-opacity-50 border border-dark border-opacity-25 rounded-4 p-4 transition cursor-pointer'
);
</script>

<template>
  <div :class="cardClass">

    <div class="card-body d-flex flex-column align-items-center justify-content-center gap-3 p-4">
      <component
        v-if="icon"
        :is="icon"
        :class="props.theme === 'dark' ? 'text-primary' : 'text-primary'"
        style="width: 32px; height: 32px;"
      />

      <p :class="titleClass">
        {{ title }}
      </p>
      <p v-if="subtitle" :class="subtitleClass">
        {{ subtitle }}
      </p>
    </div>
  </div>
</template>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}

.card:hover {
  box-shadow: 0 0.75rem 1.5rem rgba(0, 0, 0, 0.15);
}
</style>