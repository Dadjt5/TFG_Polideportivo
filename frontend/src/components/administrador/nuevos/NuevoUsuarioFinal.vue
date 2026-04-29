<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #e0f7ff, #ffffff);">
    <div class="container py-5" style="max-width: 1120px">
      <h1 class="text-center fw-bold mb-5 text-primary">
        {{ t.newUserNoQues }}
      </h1>


      <div class="card shadow-lg border-0 rounded-4 p-4"
        style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">
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
                <option value="Mujer">{{ t.female }}</option>
                <option value="Hombre">{{ t.male }}</option>
                <option value="Prefiero no decirlo">{{ t.other }}</option>
              </select>
            </div>

            <div class="col-md-6">
              <input type="date" class="form-control" :class="{ 'is-invalid': errores.fechaNacimiento }"
                v-model="usuarioFinal.fechaNacimiento" @change="checkAge" />
            </div>

            <div class="col-md-6" v-if="!usuarioFinal.esMenor">
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
                    style="font-size: 1.2rem; color: #0072ff;"></i>
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
                  <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"
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
              ¡{{ t.usuarioFinalIdentifier }}: <span class="text-success">{{ userIdentifier }}</span>!
            </p>

            <!-- Botón para continuar -->
            <button class="btn btn-outline-secondary btn-lg px-5" @click="gestionUsuarios">
              {{ t.continue }}
            </button>
          </div>

          <!-- BOTONES -->
          <div v-else class="d-flex justify-content-center gap-4 mt-4">
            <button class="btn btn-primary btn-lg px-5" @click="nuevoUsuario">
              {{ t.newUserNoQues }}
            </button>

            <button class="btn btn-outline-secondary btn-lg px-5" @click="volver">
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

const mensajeEditar = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)

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

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensajeEditar.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true

  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
}


const checkAge = () => {
  if (!usuarioFinal.value.fechaNacimiento) return
  const birth = new Date(usuarioFinal.value.fechaNacimiento)
  const now = new Date()
  let age = now.getFullYear() - birth.getFullYear()
  const m = now.getMonth() - birth.getMonth()
  if (m < 0 || (m === 0 && now.getDate() < birth.getDate())) age--
  usuarioFinal.value.esMenor = age < 18
}

function validarFormulario() {
  let valido = true

  const hoy = new Date()
  const fechaNacimiento = new Date(usuarioFinal.value.fechaNacimiento)
  console.log(usuarioFinal.value.esMenor)
  errores.value.nombre = usuarioFinal.value.nombre === ''
  errores.value.apellidos = usuarioFinal.value.apellidos === ''
  errores.value.DNI = (usuarioFinal.value.dni === '' || !validarDNI(usuarioFinal.value.dni)) && !usuarioFinal.value.esMenor
  errores.value.sexo = usuarioFinal.value.sexo === ''
  errores.value.fechaNacimiento = usuarioFinal.value.fechaNacimiento === ''
  errores.value.telefono = usuarioFinal.value.telefono === ''
  errores.value.provincia = usuarioFinal.value.provincia === ''
  errores.value.municipio = usuarioFinal.value.municipio === ''
  errores.value.localidad = usuarioFinal.value.localidad === ''
  errores.value.codigoPostal = usuarioFinal.value.codigoPostal === ''
  errores.value.email =
    usuarioFinal.value.email === '' ||
    !emailRegex.test(usuarioFinal.value.email)
  errores.value.password = usuarioFinal.value.password === ''
  errores.value.confirmPassword = usuarioFinal.value.password !== usuarioFinal.value.confirmPassword
  errores.value.fechaNacimiento =
    !usuarioFinal.value.fechaNacimiento || fechaNacimiento >= hoy

  for (const key in errores.value) {
    if (errores.value[key]) {
      valido = false
    }
  }

  return valido
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


const nuevoUsuario = async () => {
  if (!validarFormulario()) {
    if (errores.value.DNI) {
      lanzarMensaje(t.value.DNIError, "error")
    } else {
      lanzarMensaje(t.value.missing, "error")
    }
    return
  }

  try {
    const data = await registrarse(usuarioFinal.value);

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
    console.log("Error al crear el nuevo usuario", e);
  }
};

function volver() {
  router.back()
}

const gestionUsuarios = () => {
  router.push({ name: 'gestion-usuarios' });
}
</script>
