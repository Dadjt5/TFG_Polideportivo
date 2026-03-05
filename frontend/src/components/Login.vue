<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-7 col-lg-5">

          <!-- Título -->
          <h1 class="text-center fw-bold mb-4 text-primary">
            {{ t.loginPage }}
          </h1>

          <!-- Card login -->
          <div class="card border-0 rounded-4 p-4 mx-auto"
               style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">

            <p class="text-center text-secondary mb-4">
              {{ t.instructions }}
            </p>

            <!-- Identifier -->
            <div class="mb-3 position-relative">
              <input type="text" class="form-control py-2 rounded-3" 
                     :placeholder="t.identifierPlaceholder" v-model="identifier"
                     @keyup.enter="handleLogin" />
            </div>

            <!-- Password -->
            <div class="mb-4 position-relative">
              <input :type="showPassword ? 'text' : 'password'" class="form-control py-2 rounded-3 pe-5"
                     :placeholder="t.passwordPlaceholder" v-model="password" @keyup.enter="handleLogin" />
              <button type="button"
                      class="position-absolute top-50 end-0 translate-middle-y me-3 border-0 bg-transparent d-flex align-items-center justify-content-center"
                      style="height: 100%; top: 0;" 
                      @click="togglePassword">
                <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'" 
                   style="font-size: 1.2rem; color: #0072ff;"></i>
              </button>
            </div>

            <!-- Login button -->
            <button class="btn btn-primary w-100 py-2 fs-5 rounded-3 mb-2" 
                    @click="handleLogin" :disabled="loading">
              {{ t.loginPage }}
            </button>

            <!-- Forgot password -->
            <button class="btn btn-link w-100 text-decoration-none text-primary mb-3">
              {{ t.forgotPassword }}
            </button>

            <!-- Message -->
            <p v-if="message" class="text-center fw-medium mt-2" :class="success ? 'text-success' : 'text-danger'">
              {{ message }}
            </p>

            <!-- Divider -->
            <div class="d-flex align-items-center my-4">
              <hr class="flex-grow-1 border-primary border-opacity-25">
              <span class="mx-3 text-primary small fw-semibold">
                {{ t.newUser }}
              </span>
              <hr class="flex-grow-1 border-primary border-opacity-25">
            </div>

            <!-- Register -->
            <router-link to="/registrarse" 
                         class="btn btn-outline-primary w-100 py-2 fs-5 rounded-3">
              {{ t.register }}
            </router-link>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, inject, Ref } from "vue";
import { useRouter } from "vue-router";

/* Importamos el fichero para realizar el login y redirigir a la pantalla indicada guardando el usuario */
import { login } from "@/services/loginService"
import { useAuthStore } from "@/stores/auth";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const router = useRouter();

const identifier = ref("");
const password = ref("");
const message = ref("");
const success = ref(false);
const loading = ref(false);

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const showPassword = ref(false)

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const handleLogin = async () => {
  /* Nos ahorramos comunicaciones con el backend si algún campo esta vacio */
  if (!identifier.value || !password.value) {
    message.value = t.value.error;
    success.value = false;
    return;
  }

  try {
    const data = await login({
      username: identifier.value,
      password: password.value,
    });

    message.value = t.value.success;
    success.value = true;

    localStorage.setItem("access", data.access);
    localStorage.setItem("refresh", data.refresh);

    const auth = useAuthStore();

    auth.access = data.access;
    auth.refresh = data.refresh;

    await auth.fetchUser();

    router.push("/");
  } catch (error) {
    message.value = t.value.error;
    success.value = false;
  }
};
</script>
