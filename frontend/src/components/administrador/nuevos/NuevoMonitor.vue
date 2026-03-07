<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #e0f7ff, #ffffff);">
    <main class="container py-5" style="max-width: 1120px">
      <h1 class="text-center fw-bold mb-5 text-primary">
        {{ t.newMonitorTitle }}
      </h1>

      <div class="card shadow-lg border-0 rounded-4 p-4"
           style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">

        <div class="row g-4">

          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.name }}</label>
            <input
              type="text"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.nombre }"
              v-model="monitor.nombre"
            />
          </div>

          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.surnames }}</label>
            <input
              type="text"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.apellidos }"
              v-model="monitor.apellidos"
            />
          </div>

          <div class="col-md-6">
            <label class="form-label fw-semibold">DNI</label>
            <input
              type="text"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.dni }"
              v-model="monitor.dni"
            />
          </div>

          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.email }}</label>
            <input
              type="email"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.email }"
              v-model="monitor.email"
            />
          </div>

          <!-- PASSWORD -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.passwordPlaceholder }}</label>
            <div class="position-relative d-flex align-items-center">
              <input :type="showPassword ? 'text' : 'password'" class="form-control pe-5"
                     :class="{ 'is-invalid': errores.password }" v-model="monitor.password" />
              <button type="button"
                      class="position-absolute end-0 me-3 border-0 bg-transparent d-flex align-items-center justify-content-center"
                      style="height: 100%; top: 0;" @click="togglePassword">
                <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"
                   style="font-size: 1.2rem; color: #0072ff;"></i>
              </button>
            </div>
          </div>

          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.passwordConfirm }}</label>
            <div class="position-relative d-flex align-items-center">
              <input :type="showConfirmPassword ? 'text' : 'password'" class="form-control pe-5"
                     :class="{ 'is-invalid': errores.password }" v-model="monitor.confirmPassword" />
              <button type="button"
                      class="position-absolute end-0 me-3 border-0 bg-transparent d-flex align-items-center justify-content-center"
                      style="height: 100%; top: 0;" @click="toggleConfirmPassword">
                <i :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"
                   style="font-size: 1.2rem; color: #0072ff;"></i>
              </button>
            </div>
          </div>
        </div>

        <p v-if="mensaje" class="text-center text-danger mt-4">
          {{ mensaje }}
        </p>

        <!-- Mensaje del identificador único -->
        <div v-if="showIdentifier" class="text-center mt-3">
          <p class="fw-bold text-primary mb-2">
            ¡{{ t.monitorIdentifier }}: <span class="text-success">{{ userIdentifier }}</span>!
          </p>

          <!-- Botón para ir al login -->
          <button class="btn btn-primary btn-sm shadow-sm" @click="gestionUsuarios">
            {{ t.login }}
          </button>
        </div>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-5">
          <button
            class="btn btn-primary btn-lg px-5 rounded-pill shadow-sm"
            @click="crearMonitor"
          >
            {{ t.createMonitor }}
          </button>

          <button
            class="btn btn-outline-secondary btn-lg px-5 rounded-pill shadow-sm"
            @click="volver"
          >
            {{ t.return }}
          </button>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { type Ref, inject, ref } from "vue";
import { useRouter } from "vue-router";

import { registrarMonitor } from "@/services/loginService";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();

const userIdentifier = ref("");
const showIdentifier = ref(false);

const monitor = ref({
  nombre: "",
  apellidos: "",
  dni: "",
  email: "",
  password: "",
	confirmPassword: ""
});

const errores = ref({
  nombre: false,
  apellidos: false,
  dni: false,
  email: false,
  password: false,
	confirmPassword: false
});

/* Expresion regular para comprobar el email */
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const mensaje = ref("")

const showPassword = ref(false)
const showConfirmPassword = ref(false)

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const toggleConfirmPassword = () => {
  showConfirmPassword.value = !showConfirmPassword.value
}

function validarFormulario() {
  let valido = true

	errores.value.nombre = monitor.value.nombre === ''
  errores.value.apellidos = monitor.value.apellidos === ''
	errores.value.dni = 
		monitor.value.dni === '' ||
		monitor.value.dni.length !== 9
	errores.value.email =
		monitor.value.email === '' ||
		!emailRegex.test(monitor.value.email)
  errores.value.password =
    monitor.value.password === '' ||
    monitor.value.password !== monitor.value.confirmPassword

  for (const key in errores.value) {
    if(errores.value[key]) {
      valido = false
    }
  }

  return valido
}

const crearMonitor = async () => {
	if(!validarFormulario()) return

	try {
    const data = await registrarMonitor(monitor.value);

    userIdentifier.value = data.codigo_usuario;
    showIdentifier.value = true;
    mensaje.value = data.mensaje;
  } catch (error: any) {
    if (error.response && error.response.data?.mensaje) {
      mensaje.value = error.response.data.mensaje;
    } else {
      mensaje.value = t.value.unexpectedError
    }
  }
};

function volver() {
  router.back()
}

const gestionUsuarios = () => {
  router.push({ name: 'gestion-usuarios' });
}
</script>
