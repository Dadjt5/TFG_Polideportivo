<template>
  <div class="min-vh-100 bg-light">
    <!-- CONTENT -->
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-7 col-lg-5">

          <h1 class="text-center fw-bold mb-4">
            {{ t.loginPage }}
          </h1>

          <div class="card shadow-lg border-0 rounded-4 p-4">

            <p class="text-center text-secondary mb-4">
              {{ t.instructions }}
            </p>

            <!-- Identifier -->
            <div class="mb-3 position-relative">
              <i
                class="bi bi-person position-absolute top-50 start-0 translate-middle-y ms-3 text-secondary"
              ></i>
              <input
                type="text"
                class="form-control py-2"
                :placeholder="t.identifierPlaceholder"
                v-model="identifier"
              />
            </div>

            <!-- Password -->
            <div class="mb-4 position-relative">
              <i
                class="bi bi-lock position-absolute top-50 start-0 translate-middle-y ms-3 text-secondary"
              ></i>
              <input
                type="password"
                class="form-control py-2"
                :placeholder="t.passwordPlaceholder"
                v-model="password"
              />
            </div>

            <!-- Login -->
            <button
              class="btn btn-primary w-100 py-2 fs-5 rounded-3"
              @click="handleLogin"
              :disabled="loading"
            >
              {{ t.loginPage }}
            </button>

            <!-- Forgot -->
            <button
              class="btn btn-link w-100 mt-2 text-decoration-none"
            >
              {{ t.forgotPassword }}
            </button>

            <!-- Message -->
            <p
              v-if="message"
              class="text-center fw-medium mt-3"
              :class="success ? 'text-success' : 'text-danger'"
            >
              {{ message }}
            </p>

            <!-- Divider -->
            <div class="d-flex align-items-center my-4">
              <hr class="flex-grow-1">
              <span class="mx-3 text-muted small">
                {{ t.newUser }}
              </span>
              <hr class="flex-grow-1">
            </div>

            <!-- Register -->
             <router-link to="/registrarse" class="btn btn-outline-primary w-100 py-2 fs-5 rounded-3">
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

/* Importamos el fichero para realizar el login y para obtener el usuario */
import { login, getMe } from "../services/loginService"

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const router = useRouter();

const identifier = ref("");
const password = ref("");
const message = ref("");
const success = ref(false);
const loading = ref(false);

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);


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

    const user = await getMe()
    if (user.is_usuario_final) {
      router.push("/home-usuario");
    } else if (user.is_monitor) {
      router.push("/home-monitor");
    } else if (user.is_administrador) {
      router.push("/home-admin");
    }
  } catch (error) {
    message.value = t.value.error;
    success.value = false;
  }
};
</script>
