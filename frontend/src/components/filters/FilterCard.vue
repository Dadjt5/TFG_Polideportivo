<script setup lang="ts">
defineProps<{
  title: string;
  subtitle?: string;
  icon: any;
}>();
</script>

<template>
  <div
    class="card text-center h-100 shadow-sm border cursor-pointer">
    <div class="card-body d-flex flex-column align-items-center justify-content-center gap-3 p-4">
      <component
        v-if="icon"
        :is="icon"
        class="text-primary"
        style="width: 32px; height: 32px;"
      />

      <p class="fs-5 fw-medium text-secondary mb-0">
        {{ title }}
      </p>
      <p v-if="subtitle" class="text-sm text-secondary text-center">
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
