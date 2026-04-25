<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center position-relative overflow-hidden"
       style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">

    <!-- Fondo decorativo -->
    <div class="position-absolute top-0 start-0 w-100 h-100 opacity-25"
         style="background: radial-gradient(circle at 20% 20%, #0072ff55, transparent 40%),
                                radial-gradient(circle at 80% 70%, #ff7a0055, transparent 40%);">
    </div>

    <!-- Card -->
    <div class="card p-4 p-md-5 rounded-4 shadow-lg border-0 position-relative"
         style="max-width:420px; width:100%; background: rgba(255,255,255,0.85); backdrop-filter: blur(12px);">

      <!-- Icono -->
      <div class="text-center mb-3">
        <div class="rounded-circle bg-primary d-inline-flex align-items-center justify-content-center"
             style="width:60px; height:60px;">
          <i class="bi bi-lock-fill text-white fs-4"></i>
        </div>
      </div>

      <!-- Título -->
      <h2 class="text-center text-primary fw-bold mb-1">
        {{ t.resetPassword }}
      </h2>

      <p class="text-center text-secondary mb-4 small">
        {{ t.newPassword }}
      </p>

      <!-- Nueva contraseña -->
      <div class="mb-3 position-relative">
        <input
          :type="showPassword ? 'text' : 'password'"
          class="form-control py-2 rounded-3 pe-5"
          placeholder="Nueva contraseña"
          v-model="password"
          @keyup.enter="resetPassword"
        />
        <button type="button"
                class="position-absolute top-50 end-0 translate-middle-y me-3 border-0 bg-transparent"
                @click="showPassword = !showPassword">
          <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"
             style="font-size: 1.2rem; color:#0072ff;"></i>
        </button>
      </div>

      <!-- Confirmar contraseña -->
      <div class="mb-4 position-relative">
        <input
          :type="showPassword ? 'text' : 'password'"
          class="form-control py-2 rounded-3 pe-5"
          placeholder="Confirmar contraseña"
          v-model="confirmPassword"
          @keyup.enter="resetPassword"
        />
      </div>

      <!-- Botón -->
      <button class="btn btn-primary w-100 py-2 rounded-3 fw-semibold shadow-sm"
              :disabled="loading"
              @click="resetPassword">
        <span v-if="!loading">{{ t.changePassword }}</span>
        <span v-else class="spinner-border spinner-border-sm"></span>
      </button>

      <!-- Mensaje -->
      <div v-if="message" class="alert mt-3 mb-0 py-2 text-center"
           :class="success ? 'alert-success' : 'alert-danger'">
        {{ message }}
      </div>

      <!-- Login -->
      <router-link to="/login"
                   class="btn btn-outline-primary w-100 py-2 rounded-3 mt-3 fw-medium">
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