<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center"
       style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">

    <div class="card p-4 rounded-4 shadow" style="max-width:400px; width:100%; background: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">

      <!-- Título -->
      <h1 class="text-center mb-3 text-primary fw-bold">{{ t.resetPassword }}</h1>

      <p class="text-center text-secondary mb-4">
        {{ t.newPassword }}
      </p>

      <!-- Nueva contraseña -->
      <div class="mb-3 position-relative">
        <input
          :type="showPassword ? 'text' : 'password'"
          class="form-control py-2 rounded-3"
          placeholder="Nueva contraseña"
          v-model="password"
          @keyup.enter="resetPassword"
        />
        <button type="button"
                class="position-absolute top-50 end-0 translate-middle-y me-3 border-0 bg-transparent"
                @click="showPassword = !showPassword">
          <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'" style="font-size: 1.2rem; color:#0072ff;"></i>
        </button>
      </div>

      <!-- Confirmar contraseña -->
      <div class="mb-4 position-relative">
        <input
          :type="showPassword ? 'text' : 'password'"
          class="form-control py-2 rounded-3"
          placeholder="Confirmar contraseña"
          v-model="confirmPassword"
          @keyup.enter="resetPassword"
        />
      </div>

      <!-- Botón cambiar contraseña -->
      <button class="btn btn-primary w-100 py-2 fs-5 rounded-3 mb-3"
              :disabled="loading"
              @click="resetPassword">
        {{ t.changePassword }}
      </button>

      <!-- Mensaje -->
      <p v-if="message" class="mt-2 text-center fw-medium" :class="success ? 'text-success' : 'text-danger'">
        {{ message }}
      </p>

      <!-- Volver al login -->
      <router-link to="/login" class="btn btn-outline-primary w-100 py-2 fs-5 rounded-3 mt-3">
        {{ t.login }}
      </router-link>

    </div>
  </div>
</template>

<script setup lang="ts">
import { type Ref, ref, inject } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import { confirmacionResetPassword } from '@/services/recuperarService';

import { useI18n } from "@/useI18N"
import type { Language } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const route = useRoute();
const router = useRouter();

const password = ref('');
const confirmPassword = ref('');
const message = ref('');
const success = ref(false);
const loading = ref(false);
const showPassword = ref(false);

const resetPassword = async () => {
  if (!password.value || !confirmPassword.value) {
    message.value = 'Debes completar ambos campos';
    success.value = false;
    return;
  }

  if (password.value !== confirmPassword.value) {
    message.value = 'Las contraseñas no coinciden';
    success.value = false;
    return;
  }

  loading.value = true;
  message.value = '';
  
  try {
    const token = route.params.token;

    const res = await confirmacionResetPassword(token, password.value)

    if (!res.ok) throw new Error('Error al cambiar la contraseña');

    success.value = true;
    message.value = 'Contraseña cambiada correctamente. Redirigiendo al login...';

    setTimeout(() => {
      router.push('/login');
    }, 2000);

  } catch (err) {
    success.value = false;
    message.value = 'No se pudo cambiar la contraseña. Enlace inválido o caducado.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.card input.form-control {
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
}

.card input.form-control:focus {
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
  border-color: #0d6efd;
}
</style>