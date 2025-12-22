<script setup lang="ts">
defineProps<{
  modelValue?: string | number;
  type?: string;
  placeholder?: string;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string | number): void;
}>();
</script>

<template>
  <input
    :type="type || 'text'"
    :placeholder="placeholder"
    :value="modelValue"
    @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    class="
      w-full rounded-xl border border-slate-300
      px-4 py-2 text-base
      focus:outline-none focus:ring-2 focus:ring-blue-400
    "
  />
</template>
