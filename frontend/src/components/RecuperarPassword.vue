<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-7 col-lg-5">

          <!-- Título -->
          <h1 class="text-center fw-bold mb-4 text-primary">
            {{ t.recoverPassword }}
          </h1>

          <div class="card border-0 rounded-4 p-4 mx-auto"
            style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">

            <p class="text-center text-secondary mb-4">
              {{ t.recoverPasswordAdvice }}
            </p>

            <div v-if="step === 1">
              <div class="mb-4">
                <input type="email" class="form-control py-2 rounded-3" placeholder="Email" v-model="email"
                  @keyup.enter="sendCode" />
              </div>

              <button class="btn btn-primary w-100 py-2 fs-5 rounded-3 mb-2" @click="sendCode">
                {{ t.sendToken }}
              </button>
            </div>

            <div v-else>
              <!-- Código -->
              <div class="mb-3">
                <input type="text" class="form-control py-2 rounded-3" placeholder="Código recibido" v-model="codigo"
                  @keyup.enter="verifyCode" />
              </div>

              <button class="btn btn-outline-primary w-100 py-2 rounded-3 mb-3" @click="verifyCode">
                {{ t.verifyCode }}
              </button>
            </div>

            <!-- Mensaje global -->
            <div v-if="mostrarMensaje" class="text-center mb-0 mt-3">
              <div class="alert" :class="tipoMensaje === 'success' ? 'alert-success' : 'alert-danger'">
                {{ mensaje }}
              </div>
            </div>

            <!-- Login -->
            <router-link to="/login" class="btn btn-outline-primary w-100 py-2 fs-5 rounded-3 mt-3">
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
import { useRouter } from "vue-router";

import { sendResetCode, verifyResetCode } from '@/services/recuperarService'

import { useI18n } from "@/useI18N"
import type { Language } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const step = ref(1)
const router = useRouter();

const email = ref("")
const codigo = ref("")
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

const sendCode = async () => {
  if (!email.value) {
    lanzarMensaje(t.value.invalidEmail, 'error')
    return
  }

  try {
    await sendResetCode(email.value)
    lanzarMensaje(t.value.codeSend, 'success')
    step.value = 2
  } catch (e: any) {
    if(e.response.data.tipo == "email") {
      lanzarMensaje(t.value.noEmail, 'error')
    } else {
      lanzarMensaje(t.value.errorSendingCode, 'error')
    }
  }
}

const continuar = (id: number) => {
  router.push({
    name: 'reset-password',
    params: { id }
  });
}

const verifyCode = async () => {
  try {
    const res = await verifyResetCode(email.value, codigo.value)

    if (res.respuesta != "Codigo correcto") {
      lanzarMensaje(t.value.expiredOrIncorrectCode, 'error')
      return
    }

    continuar(res.id_usuario)
  } catch (e) {
    lanzarMensaje(t.value.errorCode, 'error')
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