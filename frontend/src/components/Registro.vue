<template>
  <div class="min-vh-100 bg-light">
    <!-- CONTENIDO -->
    <div class="container py-5">
      <h1 class="text-center mb-2">{{ t.registerPage }}</h1>
      <p class="text-center text-secondary mb-4">{{ t.instructionsRegister }}</p>

      <div class="card shadow rounded-4 p-4">
        <!-- PASO 1: Datos personales -->
        <div v-if="step === 1">
          <h4 class="mb-3">{{ t.personalData }}</h4>
          <div class="row g-3">
            <div class="col-md-6">
              <input
                type="text"
                class="form-control"
                :class="{ 'is-invalid': errores.nombre }"
                :placeholder=t.name
                v-model="formData.nombre"
              >
            </div>
            <div class="col-md-6">
              <input
                type="text"
                class="form-control"
                :class="{ 'is-invalid': errores.apellidos }"
                :placeholder= t.surnames
                v-model="formData.apellidos"
              >
            </div>

            <div class="col-12">
              <label class="form-label">{{ t.sex }}</label>
              <select class="form-select" :class="{ 'is-invalid': errores.sexo }" v-model="formData.sexo">
                <option value="">{{ t.selectOption }}</option>
                <option value="male">{{ t.male }}</option>
                <option value="female">{{ t.female }}</option>
                <option value="other">{{ t.other }}</option>
              </select>
            </div>

            <div class="col-12">
              <label class="form-label">{{ t.birth }}</label>
              <input
                type="date"
                class="form-control"
                :class="{ 'is-invalid': errores.fechaNacimiento }"
                v-model="formData.fechaNacimiento"
                @change="checkAge"
              >
            </div>

            <div class="col-12" v-if="!formData.esMenor">
              <input
                type="text"
                class="form-control"
                :class="{ 'is-invalid': errores.dni }"
                placeholder="DNI"
                v-model="formData.dni"
              >
            </div>
          </div>
        </div>

        <!-- PASO 2: Contacto y dirección -->
        <div v-if="step === 2">
          <h4 class="mb-3">{{ t.contact }}</h4>
          <div class="row g-3">
            <div class="col-md-6">
              <input
                type="text"
                class="form-control"
                :class="{ 'is-invalid': errores.telefono }"
                :placeholder= t.phoneNumber
                v-model="formData.telefono"
              >
            </div>
            <div class="col-md-6">
              <input
                type="email"
                class="form-control"
                :class="{ 'is-invalid': errores.email }"
                :placeholder= t.email
                v-model="formData.email"
              >
            </div>
          </div>

          <h4 class="mt-4 mb-3">{{ t.address }}</h4>
          <div class="row g-3">
            <div class="col-md-6">
              <input
                type="text"
                class="form-control"
                :class="{ 'is-invalid': errores.provincia }"
                :placeholder= t.province
                v-model="formData.provincia"
              >
            </div>
            <div class="col-md-6">
              <input
                type="text"
                class="form-control"
                :class="{ 'is-invalid': errores.municipio }"
                :placeholder= t.municipality
                v-model="formData.municipio"
              >
            </div>
            <div class="col-md-6">
              <input
                type="text"
                class="form-control"
                :class="{ 'is-invalid': errores.localidad }"
                :placeholder= t.locality
                v-model="formData.localidad"
              >
            </div>
            <div class="col-md-6">
              <input
                type="text"
                class="form-control"
                :class="{ 'is-invalid': errores.codigoPostal }"
                :placeholder= t.postalCode
                v-model="formData.codigoPostal"
              >
            </div>
          </div>
        </div>

        <!-- PASO 3: Credenciales y pago -->
        <div v-if="step === 3">
          <h4 class="mb-3">{{ t.credentials }}</h4>
          <div class="row g-3">
            <div class="col-md-6">
              <input
                type="password"
                class="form-control"
                :class="{ 'is-invalid': errores.password }"
                :placeholder= t.passwordPlaceholder
                v-model="formData.password"
              >
            </div>
            <div class="col-md-6">
              <input
                type="password"
                class="form-control"
                :class="{ 'is-invalid': errores.confirmPassword }"
                :placeholder=t.passwordConfirm
                v-model="formData.confirmPassword"
              >
            </div>
          </div>

          <h4 class="mt-4 mb-3">{{t.payment}}</h4>
          <div class="form-check mb-2">
            <input type="checkbox" class="form-check-input" id="pagoFraccionado" v-model="formData.pagoFraccionado">
            <label class="form-check-label" for="pagoFraccionado">{{ t.account }}</label>
          </div>
          <div v-if="formData.pagoFraccionado">
            <input
              type="text"
              class="form-control"
              :class="{ 'is-invalid': errores.cuentaBancaria }"
              :placeholder= t.account
              v-model="formData.cuentaBancaria"
            >
          </div>
        </div>

        <!-- BOTONES -->
        <div class="d-flex justify-content-between mt-4">
          <button class="btn btn-outline-primary" :disabled="step === 1" @click="step--">{{ t.back }}</button>
          <button class="btn btn-primary" v-if="step < 3" @click="siguiente()">{{ t.next }}</button>
          <button class="btn btn-success" v-else @click="handleFinish">{{ t.finish }}</button>
        </div>

        <!-- MENSAJE -->
        <p v-if="mensaje" class="text-center">
          {{ mensaje }}
        </p>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, inject, Ref, reactive } from "vue";
import { useRouter } from "vue-router";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

/* Importamos el fichero para realizar el registro */
import { registrarse } from "../services/loginService"

const router = useRouter();

const continuar = ref(true);

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const formData = reactive({
  nombre: '',
  apellidos: '',
  sexo: '',
  fechaNacimiento: '',
  esMenor: false,
  dni: '',
  telefono: '',
  email: '',
  provincia: '',
  municipio: '',
  localidad: '',
  codigoPostal: '',
  password: '',
  confirmPassword: '',
  pagoFraccionado: false,
  cuentaBancaria: '',
})

const errores = ref({
  nombre: false,
  apellidos: false,
  sexo: false,
  fechaNacimiento: false,
  dni: false,
  telefono: false,
  email: false,
  provincia: false,
  municipio: false,
  localidad: false,
  codigoPostal: false,
  password: false,
  confirmPassword: false,
  pagoFraccionado: false,
  cuentaBancaria: false,
});

const step = ref(1)
const mensaje = ref("")

/* Expresion regular para comprobar el email */
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

/* Para evitar multiples llamadas al backend realizamos aqui ciertas comprobaciones */
const siguiente = () => {
  continuar.value = true

  if(step.value == 1) {      
    if(formData.nombre == '') {
      errores.value.nombre = true
      continuar.value = false
    } else {
      errores.value.nombre = false
    }

    if(formData.apellidos == '') {
      errores.value.apellidos = true
      continuar.value = false
    } else {
      errores.value.apellidos = false
    }

    if(formData.sexo == '') {
      errores.value.sexo = true
      continuar.value = false
    } else {
      errores.value.sexo = false
    }

    if(formData.fechaNacimiento == '') {
      errores.value.fechaNacimiento = true
      continuar.value = false
    } else {
      errores.value.fechaNacimiento = false
    }

    if(formData.dni == '' && !formData.esMenor) {
      errores.value.dni = true
      continuar.value = false
    } else {
      errores.value.dni = false
    }
  } else if(step.value == 2) {
    if(formData.telefono == '') {
      errores.value.telefono = true
      continuar.value = false
    } else {
      errores.value.telefono = false
    }

    if(formData.email == '' || !emailRegex.test(formData.email)) {
      errores.value.email = true
      continuar.value = false
    } else {
      errores.value.email = false
    }

    if(formData.provincia == '') {
      errores.value.provincia = true
      continuar.value = false
    } else {
      errores.value.provincia = false
    }

    if(formData.municipio == '') {
      errores.value.municipio = true
      continuar.value = false
    } else {
      errores.value.municipio = false
    }

    if(formData.localidad == '') {
      errores.value.localidad = true
      continuar.value = false
    } else {
      errores.value.localidad = false
    }

    if(formData.codigoPostal == '') {
      errores.value.codigoPostal = true
      continuar.value = false
    } else {
      errores.value.codigoPostal = false
    }
  }

  if(continuar.value) {
    step.value += 1
  }
}

const checkAge = () => {
  if (!formData.fechaNacimiento) return
  const birth = new Date(formData.fechaNacimiento)
  const now = new Date()
  let age = now.getFullYear() - birth.getFullYear()
  const m = now.getMonth() - birth.getMonth()
  if (m < 0 || (m === 0 && now.getDate() < birth.getDate())) age--
  formData.esMenor = age < 18
}

const handleFinish = async () => {
  /* Ultimas comprobaciones */
  if(formData.password == '') {
    errores.value.password = true
    continuar.value = false
  } else {
    errores.value.password = false
  }

  if(formData.confirmPassword == '' || formData.password != formData.confirmPassword) {
    errores.value.confirmPassword = true
    continuar.value = false
  } else {
    errores.value.confirmPassword = false
  }

  if(formData.cuentaBancaria == '' || formData.pagoFraccionado) {
    errores.value.cuentaBancaria = true
    continuar.value = false
  } else {
    errores.value.cuentaBancaria = false
  }

  try {
    const data = await registrarse(formData);
    mensaje.value = data.mensaje;

    router.push("/login");
  } catch (error: any) {
    if (error.response && error.response.data?.mensaje) {
      mensaje.value = error.response.data.mensaje;
    } else {
      mensaje.value = t.value.unexpectedError
    }
  }
}
</script>

