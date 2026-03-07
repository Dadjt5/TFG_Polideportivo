<template>
  <div class="min-vh-100 bg-light">
    <div class="container py-5" style="max-width: 1100px">
      <h1 class="text-center fw-semibold mb-4">
        {{ t.newUserNoQues }}
      </h1>

      <div class="card shadow-sm rounded-4">
        <div class="card-body p-4 p-md-5">

          <!-- DATOS PERSONALES -->
          <h5 class="fw-semibold mb-3">{{ t.personalData }}</h5>
          <div class="row g-3 mb-4">
            <div class="col-md-6">
              <input class="form-control" :class="{ 'is-invalid': errores.nombre }" :placeholder="t.name"
                v-model="usuarioFinal.nombre" />
            </div>

            <div class="col-md-6">
              <input class="form-control" :class="{ 'is-invalid': errores.apellidos }" :placeholder="t.surnames"
                v-model="usuarioFinal.apellidos" />
            </div>

            <div class="col-md-6">
              <select class="form-select" :class="{ 'is-invalid': errores.sexo }" v-model="usuarioFinal.sexo">
                <option value="">{{ t.selectOption }}</option>
                <option value="male">{{ t.male }}</option>
                <option value="female">{{ t.female }}</option>
                <option value="other">{{ t.other }}</option>
              </select>
            </div>

            <div class="col-md-6">
              <input type="date" class="form-control" :class="{ 'is-invalid': errores.fechaNacimiento }"
                v-model="usuarioFinal.fechaNacimiento" @change="checkAge" />
            </div>

            <div class="col-md-6" v-if="!esMenor">
              <input class="form-control" :class="{ 'is-invalid': errores.DNI }" placeholder="DNI"
                v-model="usuarioFinal.dni" />
            </div>

            <div class="col-md-6">
              <div class="form-check mb-2">
                <input type="checkbox" class="form-check-input" id="esUAM" v-model="usuarioFinal.esUAM">
                <label class="form-check-label" for="esUAM">{{ t.UAMmember }}</label>
              </div>
            </div>
          </div>

          <!-- CONTACTO -->
          <h5 class="fw-semibold mb-3">{{ t.contact }}</h5>
          <div class="row g-3 mb-4">
            <div class="col-md-6">
              <input class="form-control" :class="{ 'is-invalid': errores.telefono }" :placeholder="t.phoneNumber"
                v-model="usuarioFinal.telefono" />
            </div>

            <div class="col-md-6">
              <input class="form-control" :class="{ 'is-invalid': errores.email }" :placeholder="t.email"
                v-model="usuarioFinal.email" />
            </div>
          </div>

          <!-- DIRECCIÓN -->
          <h5 class="fw-semibold mb-3">{{ t.address }}</h5>
          <div class="row g-3 mb-4">
            <div class="col-md-6">
              <input class="form-control" :class="{ 'is-invalid': errores.provincia }" :placeholder="t.province"
                v-model="usuarioFinal.provincia" />
            </div>

            <div class="col-md-6">
              <input class="form-control" :class="{ 'is-invalid': errores.municipio }" :placeholder="t.municipality"
                v-model="usuarioFinal.municipio" />
            </div>

            <div class="col-md-6">
              <input class="form-control" :class="{ 'is-invalid': errores.localidad }" :placeholder="t.locality"
                v-model="usuarioFinal.localidad" />
            </div>

            <div class="col-md-6">
              <input class="form-control" :class="{ 'is-invalid': errores.codigoPostal }" :placeholder="t.postalCode"
                v-model="usuarioFinal.codigoPostal" />
            </div>
          </div>

          <!-- CREDENCIALES -->
          <h5 class="fw-semibold mb-3">{{ t.credentials }}</h5>
          <div class="row g-3 mb-4">

            <!-- PASSWORD -->
            <div class="col-md-6">
              <label class="form-label fw-semibold">{{ t.passwordPlaceholder }}</label>
              <div class="position-relative d-flex align-items-center">
                <input :type="showPassword ? 'text' : 'password'" class="form-control pe-5"
                  :class="{ 'is-invalid': errores.password }" v-model="usuarioFinal.password" />

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
                  :class="{ 'is-invalid': errores.password }" v-model="usuarioFinal.confirmPassword" />

                <button type="button"
                  class="position-absolute end-0 me-3 border-0 bg-transparent d-flex align-items-center justify-content-center"
                  style="height: 100%; top: 0;" @click="toggleConfirmPassword">
                  <i :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"
                    style="font-size: 1.2rem; color: #6c757d;"></i>
                </button>
              </div>
            </div>
          </div>

          <!-- MENSAJE -->
          <p v-if="mensaje" class="text-center text-danger">
            {{ mensaje }}
          </p>

          <!-- Mensaje del identificador único -->
        <div v-if="showIdentifier" class="text-center mt-3">
          <p class="fw-bold text-primary mb-2">
            ¡{{ t.usuarioFinalIdentifier }}: <span class="text-success">{{ userIdentifier }}</span>!
          </p>

          <!-- Botón para ir a login -->
          <button class="btn btn-primary btn-sm" @click="gestionUsuarios">
            {{ t.login }}
          </button>
        </div>

          <!-- BOTONES -->
          <div class="d-flex justify-content-center gap-4 mt-4">
            <button class="btn btn-primary btn-lg px-5" @click="nuevoUsuario">
              {{ t.newUserNoQues }}
            </button>

            <button class="btn btn-secondary btn-lg px-5" @click="volver">
              {{ t.return }}
            </button>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, inject, Ref } from "vue";
import { useRouter } from "vue-router";

import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

import { registrarse } from "@/services/loginService";

const router = useRouter();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const userIdentifier = ref("");
const showIdentifier = ref(false);
const esMenor = ref(false)

const usuarioFinal = ref({
  nombre: '',
  apellidos: '',
  dni: '',
  sexo: '',
  esUAM: false,
  esMenor: false,
  fechaNacimiento: '',
  telefono: '',
  email: '',
  provincia: '',
  municipio: '',
  localidad: '',
  codigoPostal: '',
  pagoFraccionado: false,
  cuentaBancaria: '',
  password: '',
  confirmPassword: '',
});

const errores = ref({
  nombre: false,
  apellidos: false,
  sexo: false,
  fechaNacimiento: false,
  DNI: false,
  telefono: false,
  email: false,
  provincia: false,
  municipio: false,
  localidad: false,
  codigoPostal: false,
  pagoFraccionado: false,
  cuentaBancaria: false,
  password: false,
  confirmPassword: false,
});

const mensaje = ref('');
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const showPassword = ref(false)
const showConfirmPassword = ref(false)

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const toggleConfirmPassword = () => {
  showConfirmPassword.value = !showConfirmPassword.value
}

const checkAge = () => {
  if (!usuarioFinal.value.fechaNacimiento) return
  const birth = new Date(usuarioFinal.value.fechaNacimiento)
  const now = new Date()
  let age = now.getFullYear() - birth.getFullYear()
  const m = now.getMonth() - birth.getMonth()
  if (m < 0 || (m === 0 && now.getDate() < birth.getDate())) age--
  esMenor.value = age < 18
}

function validarFormulario() {
  let valido = true

  errores.value.nombre = usuarioFinal.value.nombre === ''
  errores.value.apellidos = usuarioFinal.value.apellidos === ''
  errores.value.DNI = usuarioFinal.value.dni === '' && !esMenor.value
  errores.value.sexo = usuarioFinal.value.sexo === ''
  errores.value.telefono = usuarioFinal.value.telefono === ''
  errores.value.provincia = usuarioFinal.value.provincia === ''
  errores.value.municipio = usuarioFinal.value.municipio === ''
  errores.value.localidad = usuarioFinal.value.localidad === ''
  errores.value.codigoPostal = usuarioFinal.value.codigoPostal === ''
  errores.value.email =
    usuarioFinal.value.email === '' ||
    !emailRegex.test(usuarioFinal.value.email)
  errores.value.cuentaBancaria =
    usuarioFinal.value.cuentaBancaria !== '' &&
    usuarioFinal.value.cuentaBancaria.length < 20
  errores.value.password = usuarioFinal.value.password === ''
  errores.value.confirmPassword = usuarioFinal.value.password !== usuarioFinal.value.confirmPassword

  for (const key in errores.value) {
    if (errores.value[key]) {
      valido = false
    }
  }

  return valido
}

const nuevoUsuario = async () => {
  if (!validarFormulario()) return

  try {
    const data = await registrarse(usuarioFinal.value);

    userIdentifier.value = data.codigo_usuario;
    showIdentifier.value = true;
    mensaje.value = data.mensaje;
  } catch (e) {
    console.log("Error al registrar el usuario final", e)
  }
};

function volver() {
  router.back()
}

const gestionUsuarios = () => {
  router.push({ name: 'gestion-usuarios' });
}
</script>
