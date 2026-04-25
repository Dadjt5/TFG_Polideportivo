<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-7 col-lg-5">

          <!-- Título -->
          <h1 class="text-center fw-bold mb-4 text-primary">
            {{ t.recoverPassword }}
          </h1>

          <!-- Card recuperar contraseña -->
          <div class="card border-0 rounded-4 p-4 mx-auto"
               style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">

            <p class="text-center text-secondary mb-4">
              {{ t.recoverPasswordAdvice }}
            </p>

            <!-- Email -->
            <div class="mb-4 position-relative">
              <input
                type="email"
                class="form-control py-2 rounded-3"
                placeholder="Email"
                v-model="email"
                @keyup.enter="sendReset"
              />
            </div>

            <!-- Enviar enlace -->
            <button
              class="btn btn-primary w-100 py-2 fs-5 rounded-3 mb-2"
              @click="sendReset"
            >
              {{ t.sendToken }}
            </button>

            <!-- Mensaje -->
            <p v-if="message" class="text-center fw-medium mt-2 text-primary">
              {{ message }}
            </p>

            <!-- Volver a login -->
            <router-link to="/login" class="btn btn-outline-primary w-100 py-2 fs-5 rounded-3">
              {{ t.login }}
            </router-link>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, inject, Ref } from "vue"

import { resetPassword } from '@/services/recuperarService'

import { useI18n } from "@/useI18N"
import type { Language } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const email = ref("")
const message = ref("")

const sendReset = async () => {
  if (!email.value) {
    message.value = "Por favor ingresa un correo válido"
    return
  }

  try {
    await resetPassword(email.value)
    message.value = "Si el email existe recibirás un enlace."
  } catch (err) {
    message.value = "Ocurrió un error, inténtalo de nuevo."
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