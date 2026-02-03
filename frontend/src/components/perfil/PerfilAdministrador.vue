<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-4" style="max-width: 720px">

      <!-- CARD SUPERIOR -->
      <div class="card shadow-lg border mb-4 rounded-4">
        <div class="card-body p-4">
          <div class="row align-items-center">

            <div class="col-md-3 text-center mb-3 mb-md-0">
              <div
                class="rounded-circle bg-primary bg-opacity-10 d-flex align-items-center justify-content-center mx-auto"
                style="width: 110px; height: 110px;"
              >
                <i class="bi bi-shield-lock text-primary fs-1"></i>
              </div>
            </div>

            <div class="col-md-9 text-center text-md-start">
              <h1 class="fs-3 fw-semibold mb-1">
                {{ administradorStore.administrador.nombre }}
              </h1>

              <p class="text-muted mb-0">
                <i class="bi bi-person-badge me-2"></i>
                Administrador Raíz
              </p>
            </div>

          </div>
        </div>
      </div>

      <!-- EDICIÓN -->
      <div class="card shadow-lg border rounded-4">
        <div class="card-body p-4 p-md-5">
          <h2 class="fs-3 fw-semibold mb-4">
            {{ t.editableData }}
          </h2>

          <form class="d-grid gap-3" @submit.prevent="guardarCambios">

            <div>
              <label class="form-label fw-medium">
                {{ t.photo }}
              </label>
              <input type="file" class="form-control" />
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
                v-model="administrador.password"
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
                v-model="administrador.confirmPassword"
              />
            </div>

            <button class="btn btn-primary rounded-3 px-4 py-2">
              {{ t.saveChanges }}
            </button>
          </form>
        </div>
      </div>

      <!-- LOGOUT -->
      <div class="mt-5 d-flex justify-content-center">
        <button
          class="btn btn-danger rounded-3 px-4 d-flex align-items-center gap-2"
          @click="logout"
        >
          <i class="bi bi-box-arrow-right"></i>
          {{ t.logout }}
        </button>
      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, inject, type Ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '../../stores/auth';
import { useAdministradorStore } from '../../stores/administrador';
import { modificarAdministrador } from '../../services/administradorService';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../../useI18N";
import { useI18n } from "../../useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const administradorStore = useAdministradorStore();
const authStore = useAuthStore();
const router = useRouter()

const continuar = ref(true);

const administrador = ref({
  password: '',
  confirmPassword: ''
})

const errores = ref({
  password: false
});

/* Solo mandamos al backend para modificar los campos que se hayan modificado */
function camposModificados() {
	const data: any = {}
  continuar.value = true
  errores.value.password = false

	if (administrador.value.password) {
    if(administrador.value.password != administrador.value.confirmPassword) {
      errores.value.password = true
      continuar.value = false
    }

    data.password = administrador.value.password
	}

	return data
}

const guardarCambios = async () => {
  try {
    const data = camposModificados()

    if(!continuar.value) return

    await modificarAdministrador(administradorStore.administrador.id, data)

		if (data.password) {
      administradorStore.cerrarSesion()
   		authStore.logout()
  		router.push("/login")
  		return
		}

		await administradorStore.fetchUser(administradorStore.administrador.id)
  } catch (e) {
    console.error("Error al modificar el administrador", e)
  }
}

const logout = () => {
  administradorStore.cerrarSesion();
  authStore.logout();
  router.push("/");
};
</script>

<style scoped>
.card {
  border-radius: 1rem;
}
</style>
