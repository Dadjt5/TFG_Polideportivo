<template>
  <div class="min-vh-100 d-flex justify-content-center align-items-start pt-5"
    style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">

    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-7 col-lg-5">

          <div class="card p-4 p-md-5 rounded-4 shadow-lg border-0 position-relative"
            style="background: rgba(255,255,255,0.85); backdrop-filter: blur(12px);">

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
            <div class="mb-3">
              <label class="form-label">{{ t.passwordPlaceholder }}</label>
              <div class="position-relative d-flex align-items-center">
                <input :type="showPassword ? 'text' : 'password'" class="form-control py-2 rounded-3 pe-5"
                  :class="{ 'is-invalid': errores.password }" placeholder="Nueva contraseña" v-model="password"
                  @keyup.enter="resetPassword" />
                <button type="button"
                  class="position-absolute end-0 me-3 border-0 bg-transparent d-flex align-items-center justify-content-center"
                  :style="{ height: '100%', top: '0.08rem', right: errores.password ? '1.7rem' : '0.5rem' }"
                  @click="togglePassword">
                  <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"
                    style="font-size: 1.2rem; color: #6c757d;"></i>
                </button>
              </div>
              <div v-if="errores.password" class="invalid-feedback d-block">
                {{ mensajeErrorPassword }}
              </div>
            </div>

            <!-- Confirmar contraseña -->
            <div class="mb-4">
              <label class="form-label">{{ t.passwordConfirm }}</label>
              <div class="position-relative d-flex align-items-center">
                <input :type="showConfirmPassword ? 'text' : 'password'" class="form-control py-2 rounded-3 pe-5"
                  :class="{ 'is-invalid': errores.confirmPassword }" placeholder="Confirmar contraseña"
                  v-model="confirmPassword" @keyup.enter="resetPassword" />
                <button type="button"
                  class="position-absolute end-0 me-3 border-0 bg-transparent d-flex align-items-center justify-content-center"
                  :style="{ height: '100%', top: '0.08rem', right: errores.confirmPassword ? '1.7rem' : '0.5rem' }"
                  @click="toggleConfirmPassword">
                  <i :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"
                    style="font-size: 1.2rem; color: #6c757d;"></i>
                </button>
              </div>
            </div>

            <!-- Botón -->
            <button class="btn btn-primary w-100 py-2 rounded-3 fw-semibold shadow-sm" @click="resetPassword">
              <span>{{ t.changePassword }}</span>
            </button>

            <!-- Mensaje global -->
            <div v-if="mostrarMensaje" class="text-center mb-0 mt-3">
              <div class="alert" :class="tipoMensaje === 'success' ? 'alert-success' : 'alert-danger'">
                {{ mensaje }}
              </div>
            </div>

            <!-- Login -->
            <router-link to="/login" class="btn btn-outline-primary w-100 py-2 rounded-3 mt-3 fw-medium">
              {{ t.login }}
            </router-link>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { type Ref, ref, inject } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import { modificarUsuarioFinal } from '@/services/usuarioFinalService';

import { useI18n } from "@/useI18N"
import type { Language } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const route = useRoute();
const router = useRouter();

const password = ref('');
const confirmPassword = ref('');
const loading = ref(false);
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const mensaje = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensaje.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true
  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
}

const errores = ref({
  password: false,
  confirmPassword: false,
})

const mensajeErrorPassword = ref('')

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const toggleConfirmPassword = () => {
  showConfirmPassword.value = !showConfirmPassword.value
}

function validarFormulario(): boolean {
  let valido = true

  errores.value.password = false
  errores.value.confirmPassword = false
  mensajeErrorPassword.value = ''

  if (!password.value) {
    errores.value.password = true
    valido = false
  }

  if (!confirmPassword.value || password.value !== confirmPassword.value) {
    errores.value.confirmPassword = true
    valido = false
  }

  if (errores.value.password || errores.value.confirmPassword){
    lanzarMensaje(t.value.missing, "error")
  }

  return valido
}

const resetPassword = async () => {
  if (!validarFormulario()) return

  try {
    const id = route.params.id
    await modificarUsuarioFinal(id, { password: password.value })

    lanzarMensaje(t.value.resetPasswordCorrect, 'success')

    setTimeout(() => {
      router.push('/login')
    }, 2000)

  } catch (err) {
    lanzarMensaje(t.value.resetPasswordError, 'error')
  }
}
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