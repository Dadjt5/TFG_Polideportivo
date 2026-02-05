<template>
  <div class="min-vh-100 bg-light pb-5">
    <main class="container py-5">
      <h1 class="text-center fw-bold mb-5">
        {{ t.newMonitorTitle }}
      </h1>

      <div class="card shadow-sm border-0 rounded-4 p-4">
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

          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.passwordPlaceholder }}</label>
            <input
              type="password"
              class="form-control form-control-lg"
							:class="{ 'is-invalid': errores.password }"
              v-model="monitor.password"
            />
          </div>

					<div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.passwordConfirm }}</label>
            <input
              type="password"
              class="form-control form-control-lg"
							:class="{ 'is-invalid': errores.confirmPassword }"
              v-model="monitor.confirmPassword"
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
            {{ t.createMonitor }}
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

function volver() {
  router.back()
}
</script>
