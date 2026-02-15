<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-4" style="max-width: 720px">
      <div class="card shadow-lg border mb-4 rounded-4">
        <div class="card-body p-4">
          <div class="row align-items-center">

            <div class="col-md-3 text-center mb-3 mb-md-0">
              <div
                class="rounded-circle bg-primary bg-opacity-10 d-flex align-items-center justify-content-center mx-auto"
                style="width: 110px; height: 110px;"
              >
                <i class="bi bi-person text-primary fs-1"></i>
              </div>
            </div>

            <div class="col-md-9 text-center text-md-start">
              <h1 class="fs-3 fw-semibold mb-1">
                {{ monitorStore.monitor?.nombre }} {{ monitorStore.monitor?.apellidos }}
              </h1>

              <p class="text-muted mb-1">
                <i class="bi bi-envelope me-2"></i>{{ authStore.user?.email }}
              </p>

              <p class="mb-0">
                <span class="fw-medium text-muted">DNI:</span> {{ monitorStore.monitor?.DNI }}
              </p>
            </div>

          </div>
        </div>
      </div>

      <!-- Edicción -->
      <div class="card shadow-lg border rounded-4">
        <div class="card-body p-4 p-md-5">
          <h2 class="fs-3 fw-semibold mb-4">
            {{ t.editableData }}
          </h2>

          <form class="d-grid gap-3">
            <div>
              <label class="form-label fw-medium">
                {{ t.photo }}
              </label>
              <input type="file" class="form-control" />
            </div>

            <div>
              <label class="form-label fw-medium">
                {{ t.email }}
              </label>
              <input
                type="email"
                class="form-control"
                :class="{ 'is-invalid': errores.email }"
                :placeholder="monitorStore.monitor?.email"
                v-model="monitor.email"
              />
            </div>

            <div>
              <label class="form-label fw-medium">
                {{ t.passwordPlaceholder }}
              </label>
              <input
                type="password"
                class="form-control"
                :class="{ 'is-invalid': errores.password }"
                placeholder="********"
                v-model="monitor.password"
              />
            </div>

            <div>
              <label class="form-label fw-medium">
                {{ t.passwordConfirm }}
              </label>
              <input
                type="password"
                class="form-control"
                :class="{ 'is-invalid': errores.password }"
                placeholder="********"
                v-model="monitor.confirmPassword"
              />
            </div>

            <button class="btn btn-primary rounded-3 px-4 py-2" @click="guardarCambios">
              {{ t.saveChanges }}
            </button>
          </form>
        </div>
      </div>

      <div class="mt-5 d-flex justify-content-center">
        <button class="btn btn-danger rounded-3 px-4 d-flex align-items-center gap-2" @click="logout">
          <i class="bi bi-box-arrow-right"></i>
          {{ t.logout }}
        </button>
      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, inject, type Ref, ref } from 'vue';
import { useRouter } from 'vue-router';

import { useAuthStore } from "@/stores/auth";
import { useMonitorStore } from "@/stores/monitor";

import { modificarMonitor } from "@/services/monitorService";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const monitorStore = useMonitorStore();
const authStore = useAuthStore();
const router = useRouter();

/* Expresion regular para comprobar el email */
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const continuar = ref(true);

const monitor = ref({
  email: '',
  password: '',
  confirmPassword: ''
})

const errores = ref({
  email: false,
  password: false
});

/* Solo mandamos al backend para modificar los campos que se hayan modificado */
function camposModificados() {
	const data: any = {}
  continuar.value = true
  errores.value.email = false
  errores.value.password = false

	if (monitor.value.email) {
    if(monitor.value.email == '' || !emailRegex.test(monitor.value.email)) {
      errores.value.email = true
      continuar.value = false
    }

    data.email = monitor.value.email
	}

	if (monitor.value.password) {
    if(monitor.value.password != monitor.value.confirmPassword) {
      errores.value.password = true
      continuar.value = false
    }

    data.password = monitor.value.password
	}

	return data
}

const guardarCambios = async () => {
  try {
    const data = camposModificados()

    if(!continuar.value) return

    await modificarMonitor(monitorStore.monitor.id, data)

		if (data.password) {
      monitorStore.cerrarSesion()
   		authStore.logout()
  		router.push("/login")
  		return
		}

		await monitorStore.fetchUser(monitorStore.monitor.id)
  } catch (e) {
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
