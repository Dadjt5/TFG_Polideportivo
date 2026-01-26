<template>
  <div class="min-vh-100 bg-light pb-5">
    <main class="container py-5">
      <h1 class="text-center fw-bold mb-5">
        Crear nuevo monitor
      </h1>

      <div class="card shadow-sm border-0 rounded-4 p-4">
        <div class="row g-4">

          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.name }}</label>
            <input
              type="text"
              class="form-control form-control-lg"
							:class="{ 'is-invalid': errores.nombre }"
              v-model="form.nombre"
            />
          </div>

          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.surnames }}</label>
            <input
              type="text"
              class="form-control form-control-lg"
							:class="{ 'is-invalid': errores.apellidos }"
              v-model="form.apellidos"
            />
          </div>

          <div class="col-md-6">
            <label class="form-label fw-semibold">DNI</label>
            <input
              type="text"
              class="form-control form-control-lg"
							:class="{ 'is-invalid': errores.dni }"
              v-model="form.dni"
            />
          </div>

          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.email }}</label>
            <input
              type="email"
              class="form-control form-control-lg"
							:class="{ 'is-invalid': errores.email }"
              v-model="form.email"
            />
          </div>

          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.passwordPlaceholder }}</label>
            <input
              type="password"
              class="form-control form-control-lg"
							:class="{ 'is-invalid': errores.password }"
              v-model="form.password"
            />
          </div>

					<div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.passwordConfirm }}</label>
            <input
              type="password"
              class="form-control form-control-lg"
							:class="{ 'is-invalid': errores.confirmPassword }"
              v-model="form.confirmPassword"
            />
          </div>
        </div>

				<p v-if="mensaje" class="text-center text-danger mt-4">
        	{{ mensaje }}
	      </p>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-5">
          <button
            class="btn btn-primary btn-lg px-5"
            @click="crearMonitor"
          >
            {{ t.newMonitor }}
          </button>

          <button
            class="btn btn-danger btn-lg px-5"
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

import { registrarMonitor } from "../services/loginService";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();
const continuar = ref(true);

const form = ref({
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

const crearMonitor = async () => {
	continuar.value = true

	if(form.value.nombre == '') {
    errores.value.nombre = true
    continuar.value = false
  } else {
    errores.value.nombre = false
  }

	if(form.value.apellidos == '') {
    errores.value.apellidos = true
    continuar.value = false
  } else {
    errores.value.apellidos = false
  }

	if(form.value.dni == '') {
    errores.value.dni = true
    continuar.value = false
  } else {
    errores.value.dni = false
  }

	if(form.value.email == '' || !emailRegex.test(form.value.email)) {
      errores.value.email = true
      continuar.value = false
    } else {
      errores.value.email = false
    }

	if(form.value.password == '') {
    errores.value.password = true
    continuar.value = false
  } else {
    errores.value.password = false
  }

  if(form.value.confirmPassword == '' || form.value.password != form.value.confirmPassword) {
    errores.value.confirmPassword = true
    continuar.value = false
  } else {
    errores.value.confirmPassword = false
  }

	if (!continuar.value) {
    return
  }

	try {
    const data = await registrarMonitor(form.value);
    mensaje.value = data.mensaje;

    router.push("/");
  } catch (error: any) {
    if (error.response && error.response.data?.mensaje) {
      mensaje.value = error.response.data.mensaje;
    } else {
      mensaje.value = t.value.unexpectedError
    }
  }
};
</script>
