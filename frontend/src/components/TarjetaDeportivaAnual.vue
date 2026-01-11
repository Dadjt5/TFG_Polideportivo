<template>
  <div class="min-vh-100 bg-light">
    <div class="container py-5">
      <h1 class="text-center mb-5">{{ t.pageTitle }}</h1>

      <div class="card shadow-lg rounded-4 mx-auto p-4" style="max-width: 480px;">
        <div class="card-body text-center">
          <i class="bi bi-credit-card-fill text-primary display-4 mb-3"></i>
          <p class="mb-4">{{ t.instructions }}</p>

          <input
            type="text"
            class="form-control text-center mb-3"
            :placeholder="t.inputPlaceholder"
            v-model="tdaId"
          />

          <button class="btn btn-primary w-100 mb-3" @click="handleLink">{{ t.linkButton }}</button>

          <p v-if="message" :class="messageClass">{{ message }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// Datos del usuario (ejemplo)
const user = {
  name: "Carlos Rodríguez",
  email: "carlos.rodriguez@uam.es",
};

const tdaId = ref('');
const message = ref('');
const language = ref('es');

const translations = {
  es: {
    pageTitle: 'Vincular Tarjeta Deportiva Anual',
    instructions: 'Introduce el código de tu tarjeta para vincularla a tu cuenta y generar tu código QR.',
    inputPlaceholder: 'ID de tu tarjeta',
    linkButton: 'Vincular tarjeta',
    success: 'Tarjeta vinculada correctamente.',
    error: 'ID no válido o ya vinculado.',
  },
  en: {
    pageTitle: 'Link Annual Sports Card',
    instructions: 'Enter your card code to link it to your account and generate your QR code.',
    inputPlaceholder: 'Your card ID',
    linkButton: 'Link card',
    success: 'Card linked successfully.',
    error: 'Invalid ID or already linked.',
  }
};

const t = computed(() => translations[language.value]);

const toggleLanguage = () => {
  language.value = language.value === 'es' ? 'en' : 'es';
};

const handleLink = () => {
  if (tdaId.value.trim() === '') {
    message.value = t.value.error;
    return;
  }
  // Simulación de éxito
  message.value = t.value.success;
};

const messageClass = computed(() => {
  return message.value === t.value.success ? 'text-success fw-medium mt-2' : 'text-danger fw-medium mt-2';
});
</script>

<style scoped>
body {
  background: linear-gradient(to bottom right, #f8fafc, #e0f2ff, #f8fafc);
}
</style>
