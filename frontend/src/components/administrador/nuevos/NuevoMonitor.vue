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

        <div v-if="mostrarMensaje" class="text-center mb-3 mt-3">
          <div class="alert" :class="tipoMensaje === 'success' ? 'alert-success' : 'alert-danger'">
            {{ mensajeEditar }}
          </div>
        </div>

        <!-- Mensaje del identificador único -->
        <div v-if="showIdentifier" class="text-center mt-4">
          <p class="fw-bold text-primary mb-2 fs-4">
            ¡{{ t.monitorIdentifier }}: <span class="text-success">{{ userIdentifier }}</span>!
          </p>

          <!-- Botón para continuar -->
          <button class="btn btn-outline-secondary btn-lg px-5" @click="gestionUsuarios">
            {{ t.continue }}
          </button>
        </div>

        <!-- BOTONES -->
        <div v-else class="d-flex justify-content-center gap-3 mt-5">
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
const mensajeEditar = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)

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

const showPassword = ref(false)
const showConfirmPassword = ref(false)

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensajeEditar.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true

  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
}

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const toggleConfirmPassword = () => {
  showConfirmPassword.value = !showConfirmPassword.value
}

/* Letras para calcular la correcta letra del DNI */
const letrasDNI = "TRWAGMYFPDXBNJZSQVHLCKE"

function validarDNI(dni: string): boolean {
  const regex = /^(\d{8})([A-Z])$/i
  const match = dni.toUpperCase().match(regex)

  if (!match) return false

  const numero = parseInt(match[1], 10)
  const letra = match[2]

  const letraCorrecta = letrasDNI[numero % 23]

  return letra === letraCorrecta
}


function validarFormulario() {
  let valido = true

	errores.value.nombre = monitor.value.nombre === ''
  errores.value.apellidos = monitor.value.apellidos === ''
	errores.value.dni = 
		monitor.value.dni === '' ||
		monitor.value.dni.length !== 9 ||
    !validarDNI(monitor.value.dni)
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
	if (!validarFormulario()) {
    lanzarMensaje(t.value.missing, "error")
    return
  }

	try {
    const data = await registrarMonitor(monitor.value);

    userIdentifier.value = data.codigo_usuario;
    showIdentifier.value = true;
  } catch (e: any) {
    if (e.response.data.tipo === "dni") {
      lanzarMensaje(t.value.noRegisterDNI, "error")
    } else if(e.response.data.tipo === "email") {
      lanzarMensaje(t.value.noRegisterEmail, "error")
    } else {
      lanzarMensaje(t.value.userNoCreated, "error")
    }
    console.error("Error al crear el nuevo monitor", e)
  }
};

function volver() {
  router.back()
}

const gestionUsuarios = () => {
  router.push({ name: 'gestion-usuarios' });
}
</script>
