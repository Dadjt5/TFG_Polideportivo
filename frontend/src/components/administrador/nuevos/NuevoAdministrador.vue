<template>
  <div class="min-vh-100 bg-light pb-5">
    <main class="container py-5">
      <h1 class="text-center fw-bold mb-5">
        {{ t.newAdminTitle }}
      </h1>

      <div class="card shadow-sm border-0 rounded-4 p-4">
        <div class="row g-4">

          <!-- NOMBRE -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.name }}</label>
            <input
              type="text"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.nombre }"
              v-model="administrador.nombre"
            />
          </div>

          <!-- DNI -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">DNI</label>
            <input
              type="text"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.DNI }"
              v-model="administrador.DNI"
            />
          </div>

          <!-- EMAIL -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.email }}</label>
            <input
              type="email"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.email }"
              v-model="administrador.email"
            />
          </div>

          <!-- ROL -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.role }}</label>
            <select
              class="form-select form-select-lg"
              :class="{ 'is-invalid': errores.rol }"
              v-model="administrador.rol"
            >
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
            <input
              type="password"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.password }"
              v-model="administrador.password"
            />
          </div>

          <!-- CONFIRM PASSWORD -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.passwordConfirm }}</label>
            <input
              type="password"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.password }"
              v-model="administrador.confirmPassword"
            />
          </div>
        </div>

        <!-- MENSAJE ERROR -->
        <p v-if="mensaje" class="text-center text-danger mt-4">
          {{ mensaje }}
        </p>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-5">
          <button
            class="btn btn-primary btn-lg px-5"
            @click="crearAdministrador"
          >
            {{ t.createAdmin }}
          </button>

          <button
            class="btn btn-danger btn-lg px-5"
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
import { type Ref, inject, ref } from "vue"
import { useRouter } from "vue-router"

import { registrarAdministrador } from "@/services/loginService"

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const router = useRouter()
const continuar = ref(true)

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
    mensaje.value = data.mensaje
    router.push({ name: 'gestion-usuarios' });
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
</script>
