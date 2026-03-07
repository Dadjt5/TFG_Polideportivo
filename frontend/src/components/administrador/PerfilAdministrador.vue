<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container py-5" style="max-width: 820px">
      <!-- PERFIL ADMIN -->
      <div class="card shadow-lg border-0 rounded-4 mb-4"
        style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">
        <div class="card-body p-4">
          <div class="row align-items-center">
            <div class="col-md-3 text-center mb-3 mb-md-0">
              <div
                class="rounded-circle bg-primary bg-opacity-10 d-flex align-items-center justify-content-center mx-auto"
                style="width: 110px; height: 110px;">
                <i class="bi bi-shield-lock text-primary fs-1"></i>
              </div>
            </div>

            <div class="col-md-9 text-center text-md-start">
              <h1 class="fw-bold text-primary mb-1">
                {{ administradorStore.administrador.nombre }}
              </h1>

              <p class="text-dark mb-1">
                <i class="bi bi-person-badge me-2"></i>
                {{ t.rootAdmin }}
              </p>
              <p class="text-secondary mb-0">
                {{ t.loginCode }}: {{ administradorStore.administrador.codigo_usuario }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- EDICION -->
      <div class="card shadow-lg border-0 rounded-4"
        style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">

        <div class="card-body p-4 p-md-5">

          <h2 class="fw-bold text-primary mb-4">
            {{ t.editableData }}
          </h2>

          <form class="d-grid gap-4" @submit.prevent="guardarCambios">

            <!-- FOTO -->
            <div>
              <label class="form-label fw-medium">{{ t.photo }}</label>
              <input type="file" class="form-control rounded-3"/>
            </div>

            <!-- PASSWORD -->
            <div>
              <label class="form-label">{{ t.passwordPlaceholder }}</label>

              <div class="position-relative d-flex align-items-center">

                <input
                  :type="showPassword ? 'text' : 'password'"
                  class="form-control pe-5 rounded-3"
                  :class="{ 'is-invalid': errores.password }"
                  v-model="administrador.password"
                />

                <button
                  type="button"
                  class="position-absolute end-0 me-3 border-0 bg-transparent d-flex align-items-center justify-content-center"
                  style="height:100%; top:0;"
                  @click="togglePassword">

                  <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"
                    style="font-size:1.2rem; color:#6c757d;"></i>

                </button>

              </div>
            </div>

            <!-- CONFIRM PASSWORD -->
            <div>
              <label class="form-label">{{ t.passwordConfirm }}</label>

              <div class="position-relative d-flex align-items-center">

                <input
                  :type="showConfirmPassword ? 'text' : 'password'"
                  class="form-control pe-5 rounded-3"
                  :class="{ 'is-invalid': errores.password }"
                  v-model="administrador.confirmPassword"
                />

                <button
                  type="button"
                  class="position-absolute end-0 me-3 border-0 bg-transparent d-flex align-items-center justify-content-center"
                  style="height:100%; top:0;"
                  @click="toggleConfirmPassword">

                  <i :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"
                    style="font-size:1.2rem; color:#6c757d;"></i>
                </button>
              </div>
            </div>

            <!-- BOTON -->
            <button class="btn btn-primary rounded-3 py-2 fw-semibold">
              {{ t.saveChanges }}
            </button>
          </form>
        </div>
      </div>

      <!-- LOGOUT -->
      <div class="mt-5 d-flex justify-content-center">
        <button
          class="btn btn-danger rounded-3 px-4 py-2 d-flex align-items-center gap-2 shadow-sm"
          @click="logout">

          <i class="bi bi-box-arrow-right"></i>
          {{ t.logout }}
        </button>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, inject, type Ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from "@/stores/auth";
import { useAdministradorStore } from "@/stores/administrador";
import { modificarAdministrador } from "@/services/administradorService";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const administradorStore = useAdministradorStore();
const authStore = useAuthStore();
const router = useRouter()

const continuar = ref(true);

const showPassword = ref(false)
const showConfirmPassword = ref(false)

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const toggleConfirmPassword = () => {
  showConfirmPassword.value = !showConfirmPassword.value
}

const administrador = ref({
  password: '',
  confirmPassword: ''
})

const errores = ref({
  password: false
});

/* Solo mandamos al backend para modificar los campos que se hayan modificado */
function camposModificados() {
  const data: any = {}
  continuar.value = true
  errores.value.password = false

  if (administrador.value.password) {
    if (administrador.value.password != administrador.value.confirmPassword) {
      errores.value.password = true
      continuar.value = false
    }

    data.password = administrador.value.password
  }

  return data
}

const guardarCambios = async () => {
  try {
    const data = camposModificados()

    if (!continuar.value) return

    await modificarAdministrador(administradorStore.administrador.id, data)

    if (data.password) {
      administradorStore.cerrarSesion()
      authStore.logout()
      router.push("/login")
      return
    }

    await administradorStore.fetchUser(administradorStore.administrador.id)
  } catch (e) {
    console.error("Error al modificar el administrador", e)
  }
}

const logout = () => {
  administradorStore.cerrarSesion();
  authStore.logout();
  router.push("/");
};
</script>

<style scoped>
.card {
  border-radius: 1rem;
}
</style>
