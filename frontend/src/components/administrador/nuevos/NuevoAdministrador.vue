<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #e0f7ff, #ffffff);">
    <main class="container py-5" style="max-width: 1120px;">
      <h1 class="text-center fw-bold mb-5 text-primary">
        {{ t.newAdminTitle }}
      </h1>

      <div class="card shadow-lg border-0 rounded-4 p-4"
           style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">

        <div class="row g-4">

          <!-- NOMBRE -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.name }}</label>
            <input type="text" class="form-control form-control-lg"
                   :class="{ 'is-invalid': errores.nombre }"
                   v-model="administrador.nombre" />
          </div>

          <!-- DNI -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">DNI</label>
            <input type="text" class="form-control form-control-lg"
                   :class="{ 'is-invalid': errores.DNI }"
                   v-model="administrador.DNI" />
          </div>

          <!-- EMAIL -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.email }}</label>
            <input type="email" class="form-control form-control-lg"
                   :class="{ 'is-invalid': errores.email }"
                   v-model="administrador.email" />
          </div>

          <!-- ROL -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.role }}</label>
            <select class="form-select form-select-lg"
                    :class="{ 'is-invalid': errores.rol }"
                    v-model="administrador.rol">
              <option value="" disabled>{{ t.selectOption }}</option>
              <option value="RAIZ">{{ t.rootAdmin }}</option>
              <option value="USUARIOS">{{ t.usersAdmin }}</option>
              <option value="ESPACIOS">{{ t.spacesAdmin }}</option>
              <option value="TARIFAS">{{ t.tariffsAdmin }}</option>
            </select>
          </div>

          <!-- PASSWORD -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.passwordPlaceholder }}</label>
            <div class="position-relative d-flex align-items-center">
              <input :type="showPassword ? 'text' : 'password'" class="form-control pe-5"
                     :class="{ 'is-invalid': errores.password }" v-model="administrador.password" />
              <button type="button"
                      class="position-absolute end-0 me-3 border-0 bg-transparent d-flex align-items-center justify-content-center"
                      style="height: 100%; top: 0;" @click="togglePassword">
                <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"
                   style="font-size: 1.2rem; color: #6c757d;"></i>
              </button>
            </div>
          </div>

          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.passwordConfirm }}</label>
            <div class="position-relative d-flex align-items-center">
              <input :type="showConfirmPassword ? 'text' : 'password'" class="form-control pe-5"
                     :class="{ 'is-invalid': errores.password }" v-model="administrador.confirmPassword" />
              <button type="button"
                      class="position-absolute end-0 me-3 border-0 bg-transparent d-flex align-items-center justify-content-center"
                      style="height: 100%; top: 0;" @click="toggleConfirmPassword">
                <i :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"
                   style="font-size: 1.2rem; color: #6c757d;"></i>
              </button>
            </div>
          </div>

        </div>

        <!-- MENSAJE ERROR -->
        <p v-if="mensaje" class="text-center text-danger mt-4">
          {{ mensaje }}
        </p>

        <!-- Mensaje del identificador único -->
        <div v-if="showIdentifier" class="text-center mt-3">
          <p class="fw-bold text-primary mb-2">
            ¡{{ t.adminIdentifier }}: <span class="text-success">{{ userIdentifier }}</span>!
          </p>
          <button class="btn btn-primary btn-sm" @click="gestionUsuarios">
            {{ t.login }}
          </button>
        </div>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-5">
          <button class="btn btn-primary btn-lg px-5 rounded-pill shadow-sm" @click="crearAdministrador">
            {{ t.createAdmin }}
          </button>
          <button class="btn btn-danger btn-lg px-5 rounded-pill shadow-sm" @click="volver">
            {{ t.return }}
          </button>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { type Ref, inject, ref } from "vue"
import { useRouter } from "vue-router"

import { registrarAdministrador } from "@/services/loginService"

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const router = useRouter()

const userIdentifier = ref("");
const showIdentifier = ref(false);
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const toggleConfirmPassword = () => {
  showConfirmPassword.value = !showConfirmPassword.value
}

const administrador = ref({
  nombre: "",
  DNI: "",
  email: "",
  password: "",
  confirmPassword: "",
  rol: ""
})

const errores = ref({
  nombre: false,
  DNI: false,
  email: false,
  password: false,
  confirmPassword: false,
  rol: false
})

const mensaje = ref("")
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function validarFormulario() {
  let valido = true

	errores.value.nombre = administrador.value.nombre === ''
	errores.value.DNI = 
		administrador.value.DNI === '' ||
		administrador.value.DNI.length !== 9
	errores.value.email =
		administrador.value.email === '' ||
		!emailRegex.test(administrador.value.email)
	errores.value.rol = administrador.value.rol === ''
  errores.value.password =
    administrador.value.password === '' ||
    administrador.value.password !== administrador.value.confirmPassword

  for (const key in errores.value) {
    if(errores.value[key]) {
      valido = false
    }
  }

  return valido
}

const crearAdministrador = async () => {
  if(!validarFormulario()) return

  try {
    const data = await registrarAdministrador(administrador.value)

    userIdentifier.value = data.codigo_usuario;
    showIdentifier.value = true;
    mensaje.value = data.mensaje
  } catch (error: any) {
    if (error.response?.data?.mensaje) {
      mensaje.value = error.response.data.mensaje
    } else {
      mensaje.value = t.value.unexpectedError
    }
  }
}

function volver() {
  router.back()
}

const gestionUsuarios = () => {
  router.push({ name: 'gestion-usuarios' });
}
</script>
