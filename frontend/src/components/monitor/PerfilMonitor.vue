<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #e0f7ff, #ffffff);">
    <main class="container py-4" style="max-width: 720px">

      <!-- Tarjeta de perfil -->
      <div class="card border-0 mb-4 rounded-4 mx-auto shadow-lg"
        style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">
        <div class="card-body p-4">
          <div class="row align-items-center">

            <!-- Avatar -->
            <div class="col-md-3 text-center mb-3 mb-md-0">
              <div class="rounded-circle d-flex align-items-center justify-content-center mx-auto shadow"
                style="width: 110px; height: 110px; background: linear-gradient(135deg, #0072ff, #00c6ff);">
                <i class="bi bi-person text-white fs-1"></i>
              </div>
            </div>

            <!-- Información -->
            <div class="col-md-9 text-center text-md-start">
              <h1 class="fs-3 fw-semibold mb-1 text-primary">
                {{ monitorStore.monitor?.nombre }} {{ monitorStore.monitor?.apellidos }}
              </h1>

              <p class="text-secondary mb-1">
                <i class="bi bi-envelope me-2 text-danger"></i>{{ authStore.user?.email }}
              </p>

              <p class="mb-0">
                <span class="fw-medium text-secondary">DNI:</span> {{ monitorStore.monitor?.DNI }}
              </p>

              <p class="mb-0">
                <span class="fw-medium text-secondary">{{ t.loginCode }}:</span> {{ monitorStore.monitor?.codigo_usuario
                }}
              </p>
            </div>

          </div>
        </div>
      </div>

      <!-- Edición -->
      <div class="card border-0 rounded-4 mx-auto shadow-lg"
        style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">
        <div class="card-body p-4 p-md-5">
          <h2 class="fs-3 fw-semibold mb-4 text-primary">
            {{ t.editableData }}
          </h2>

          <form class="d-grid gap-3" @submit.prevent="guardarCambios">

            <!-- Nombre -->
            <div>
              <label class="form-label fw-medium">{{ t.name }}</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errores.nombre }"
                :placeholder="monitorStore.monitor?.nombre" v-model="monitor.nombre" />
            </div>

            <!-- Apellidos -->
            <div>
              <label class="form-label fw-medium">{{ t.surnames }}</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errores.apellidos }"
                :placeholder="monitorStore.monitor?.apellidos" v-model="monitor.apellidos" />
            </div>

            <!-- Email -->
            <div>
              <label class="form-label fw-medium">{{ t.email }}</label>
              <input type="email" class="form-control" :class="{ 'is-invalid': errores.email }"
                :placeholder="monitorStore.monitor?.email" v-model="monitor.email" />
            </div>

            <!-- Contraseña -->
            <div>
              <label class="form-label">{{ t.passwordPlaceholder }}</label>
              <div class="position-relative d-flex align-items-center">
                <input :type="showPassword ? 'text' : 'password'" class="form-control pe-5"
                  :class="{ 'is-invalid': errores.password }" v-model="monitor.password" />
                <button type="button"
                  class="position-absolute end-0 me-3 border-0 bg-transparent d-flex align-items-center justify-content-center"
                  :style="{ height: '100%', top: '0.08rem', right: errores.password ? '1.7rem' : '0.5rem' }"
                  @click="togglePassword">
                  <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"
                    style="font-size: 1.2rem; color: #0072ff;"></i>
                </button>
              </div>
            </div>

            <!-- Confirmar contraseña -->
            <div>
              <label class="form-label">{{ t.passwordConfirm }}</label>
              <div class="position-relative d-flex align-items-center">
                <input :type="showConfirmPassword ? 'text' : 'password'" class="form-control pe-5"
                  :class="{ 'is-invalid': errores.password }" v-model="monitor.confirmPassword" />
                <button type="button"
                  class="position-absolute end-0 me-3 border-0 bg-transparent d-flex align-items-center justify-content-center"
                  :style="{ height: '100%', top: '0.08rem', right: errores.password ? '1.7rem' : '0.5rem' }"
                  @click="toggleConfirmPassword">
                  <i :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"
                    style="font-size: 1.2rem; color: #0072ff;"></i>
                </button>
              </div>
            </div>

            <div v-if="mostrarMensaje" class="text-center mb-3 mt-3">
              <div class="alert" :class="tipoMensaje === 'success' ? 'alert-success' : 'alert-danger'">
                {{ mensaje }}
              </div>
            </div>

            <!-- Guardar cambios -->
            <button type="submit" class="btn btn-primary rounded-pill px-4 py-2 shadow-sm">
              {{ t.saveChanges }}
            </button>
          </form>
        </div>
      </div>

      <!-- Logout -->
      <div class="mt-5 d-flex justify-content-center">
        <button class="btn btn-danger rounded-pill px-4 d-flex align-items-center gap-2 shadow-sm" @click="logout">
          <i class="bi bi-box-arrow-right"></i>
          {{ t.logout }}
        </button>
      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { inject, type Ref, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

import { useAuthStore } from "@/stores/auth";
import { useMonitorStore } from "@/stores/monitor";
import { modificarMonitor } from "@/services/monitorService";

import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const monitorStore = useMonitorStore();
const authStore = useAuthStore();
const router = useRouter();

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const mensaje = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)

const monitor = ref({
  nombre: '',
  apellidos: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const errores = ref({
  nombre: false,
  apellidos: false,
  email: false,
  password: false
});

const showPassword = ref(false)
const showConfirmPassword = ref(false)

const togglePassword = () => showPassword.value = !showPassword.value
const toggleConfirmPassword = () => showConfirmPassword.value = !showConfirmPassword.value

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensaje.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true

  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
}

/* 🔥 IMPORTANTE: inicializar el form con datos reales */
onMounted(() => {
  if (monitorStore.monitor) {
    monitor.value.nombre = monitorStore.monitor.nombre
    monitor.value.apellidos = monitorStore.monitor.apellidos
    monitor.value.email = monitorStore.monitor.email
  }
})

function camposModificados() {
  const data: any = {}

  // reset errores
  errores.value = {
    nombre: false,
    apellidos: false,
    email: false,
    password: false
  }

  let valido = true

  // nombre
  if (!monitor.value.nombre) {
    errores.value.nombre = true
    valido = false
  } else {
    data.nombre = monitor.value.nombre
  }

  // apellidos
  if (!monitor.value.apellidos) {
    errores.value.apellidos = true
    valido = false
  } else {
    data.apellidos = monitor.value.apellidos
  }

  // email
  if (!monitor.value.email || !emailRegex.test(monitor.value.email)) {
    errores.value.email = true
    valido = false
  } else {
    data.email = monitor.value.email
  }

  // 🔥 password SOLO si se introduce
  if (monitor.value.password || monitor.value.confirmPassword) {
    if (monitor.value.password !== monitor.value.confirmPassword) {
      errores.value.password = true
      valido = false
    } else {
      data.password = monitor.value.password
    }
  }

  return { data, valido }
}

const guardarCambios = async () => {
  try {
    const { data, valido } = camposModificados()

    if (!valido) {
      if (errores.value.password) {
        lanzarMensaje(t.value.passwordNotMatch, "error")
      } else {
        lanzarMensaje(t.value.emptyFields, "error")
      }
      return
    }

    await modificarMonitor(monitorStore.monitor.id, data)

    lanzarMensaje(t.value.correctlyUpdate, "success")

    if (data.password) {
      lanzarMensaje(t.value.passwordUpdate, "success")

      setTimeout(() => {
        monitorStore.cerrarSesion()
        authStore.logout()
        router.push("/login")
      }, 2500)

    } else {
      await monitorStore.fetchUser(monitorStore.monitor.id)
    }

  } catch (e) {
    lanzarMensaje(t.value.noModify, "error")
    console.error("Error al modificar el monitor", e)
  }
}

const logout = () => {
  monitorStore.cerrarSesion();
  authStore.logout();
  router.push("/");
};
</script>

<style scoped>
.icono-perfil {
  font-size: 5.5rem;
}

.option-card {
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  cursor: pointer;
}

.option-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
}

.linea-fina {
  height: 1px;
  background-color: #dee2e6;
}
</style>
