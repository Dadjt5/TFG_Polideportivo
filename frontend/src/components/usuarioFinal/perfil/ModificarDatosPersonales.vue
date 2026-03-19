<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container py-4 mb-3">
      <h2 class="mb-4 mt-3 text-center fw-bold text-primary">{{ t.personalDataTitle }}</h2>

      <!-- Información no editable -->
      <div class="card mb-5 mt-4 rounded-4" style="background-color: rgba(255,255,255,0.9); backdrop-filter: blur(10px);">
        <div class="card-body">
          <h5 class="fw-semibold mb-3 text-primary">{{ t.inmutableData }}</h5>

          <div class="row g-3">
            <div class="col-md-4">
              <label class="form-label">{{ t.name }}</label>
              <input type="text" class="form-control" v-model="usuario.nombre" disabled>
            </div>

            <div class="col-md-4">
              <label class="form-label">{{ t.surnames }}</label>
              <input type="text" class="form-control" v-model="usuario.apellidos" disabled>
            </div>

            <div class="col-md-4">
              <label class="form-label">DNI</label>
              <input type="text" class="form-control" v-model="usuario.DNI" disabled>
            </div>

            <div class="col-md-4">
              <label class="form-label">{{ t.loginCode }}</label>
              <input type="text" class="form-control" v-model="usuario.codigo_usuario" disabled>
            </div>

            <div class="col-md-4">
              <label class="form-label">{{ t.birth }}</label>
              <input type="date" class="form-control" v-model="usuario.fechaNacimiento" disabled>
            </div>
          </div>
        </div>
      </div>

      <!-- Información editable -->
      <div class="card mb-5 rounded-4" style="background-color: rgba(255,255,255,0.9); backdrop-filter: blur(10px);">
        <div class="card-body">
          <h5 class="fw-semibold mb-3 text-primary">{{ t.editableData }}</h5>

          <div class="row g-3">
            <div class="col-md-4">
              <label class="form-label">{{ t.sex }}</label>
              <select class="form-select" :class="{ 'is-invalid': errores.sexo }" v-model="usuario.sexo">
                <option value="Mujer">{{ t.female }}</option>
                <option value="Hombre">{{ t.male }}</option>
                <option value="Prefiero no decirlo">{{ t.other }}</option>
              </select>
            </div>

            <div class="col-md-4">
              <label class="form-label">{{ t.phoneNumber }}</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errores.telefono }"
                v-model="usuario.telefono">
            </div>

            <div class="col-md-4">
              <label class="form-label">{{ t.province }}</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errores.provincia }"
                v-model="usuario.provincia">
            </div>

            <div class="col-md-4">
              <label class="form-label">{{ t.municipality }}</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errores.municipio }"
                v-model="usuario.municipio">
            </div>

            <div class="col-md-4">
              <label class="form-label">{{ t.locality }}</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errores.localidad }"
                v-model="usuario.localidad">
            </div>

            <div class="col-md-4 mt-3">
              <label class="form-label">{{ t.postalCode }}</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errores.codigoPostal }"
                v-model="usuario.codigoPostal">
            </div>

            <div class="col-md-4 mt-3">
              <label class="form-label">{{ t.passwordPlaceholder }}</label>
              <div class="position-relative d-flex align-items-center">
                <input :type="showPassword ? 'text' : 'password'" class="form-control pe-5"
                  :class="{ 'is-invalid': errores.password }" v-model="usuario.password" />

                <button type="button"
                  class="position-absolute end-0 me-3 border-0 bg-transparent d-flex align-items-center justify-content-center"
                  style="height: 100%; top: 0;" @click="togglePassword">
                  <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"
                    style="font-size: 1.2rem; color: #6c757d;"></i>
                </button>
              </div>
            </div>

            <div class="col-md-4 mt-3">
              <label class="form-label">{{ t.passwordConfirm }}</label>
              <div class="position-relative d-flex align-items-center">
                <input :type="showConfirmPassword ? 'text' : 'password'" class="form-control pe-5"
                  :class="{ 'is-invalid': errores.password }" v-model="usuario.confirmPassword" />

                <button type="button"
                  class="position-absolute end-0 me-3 border-0 bg-transparent d-flex align-items-center justify-content-center"
                  style="height: 100%; top: 0;" @click="toggleConfirmPassword">
                  <i :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"
                    style="font-size: 1.2rem; color: #6c757d;"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Deportes favoritos -->
      <div class="container py-4 mb-4">
        <h2 class="mb-4 text-primary">{{ t.favoriteSports }}</h2>

        <div class="row">
          <div class="col-md-5">
            <h6 class="mb-2">{{ t.sports }}</h6>
            <ul class="list-group overflow-auto" style="max-height: 300px;">
              <li v-for="deporte in Object.values(estadisticasStore.data.tiposDeporte)" :key="deporte.id"
                class="list-group-item d-flex justify-content-between align-items-center">
                {{ deporte.titulo }}
                <button class="btn btn-sm btn-primary" @click="addFavorite(deporte)"
                  :disabled="deportesRestantes <= 0 || usuario.deportesFavoritos.includes(deporte.id)">
                  +
                </button>
              </li>
            </ul>
          </div>

          <div class="col-md-2 d-flex flex-column justify-content-center align-items-center">
            <p class="text-center mb-2">{{ t.sportsMaxNumber }}</p>
            <p><strong>{{ deportesRestantes }}</strong></p>
          </div>

          <div class="col-md-5">
            <h6 class="mb-2">{{ t.favouritesSports }}</h6>
            <ul class="list-group overflow-auto" style="max-height: 300px;">
              <li v-for="deporte in favoritosSeleccionados" :key="deporte.id"
                class="list-group-item d-flex justify-content-between align-items-center">
                {{ deporte.titulo }}
                <button class="btn btn-sm btn-danger" @click="removeFavorite(deporte)">
                  -
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- BOTÓN GUARDAR -->
      <div class="text-center mb-5">
        <button class="btn btn-primary btn-lg px-4 me-3" @click="guardarCambios">
          {{ t.saveChanges }}
        </button>

        <router-link to="/perfil" class="btn btn-secondary btn-lg px-4">
          {{ t.return }}
        </router-link>
      </div>

    </main>
  </div>
</template>


<script setup lang="ts">
import { computed, type Ref, inject, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { useUserStore } from '@/stores/usuarioFinal'
import { useEstadisticasStore } from '@/stores/estadisticas';
import { useConfiguracionStore } from "@/stores/configuracion";

import { modificarUsuarioFinal } from '@/services/usuarioFinalService';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const usuarioFinalStore = useUserStore()
const estadisticasStore = useEstadisticasStore()
const configuracionStore = useConfiguracionStore()

const router = useRouter()

const usuario = ref({
  id: 0,
  nombre: '',
  apellidos: '',
  DNI: '',
  codigo_usuario: '',
  fechaNacimiento: '',
  telefono: '',
  provincia: '',
  municipio: '',
  localidad: '',
  codigoPostal: '',
  sexo: '',
  password: '',
  confirmPassword: '',
  deportesFavoritos: [] as number[],
})

const errores = ref({
  sexo: false,
  telefono: false,
  provincia: false,
  municipio: false,
  localidad: false,
  codigoPostal: false,
  password: false,
})

const showPassword = ref(false)
const showConfirmPassword = ref(false)

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const toggleConfirmPassword = () => {
  showConfirmPassword.value = !showConfirmPassword.value
}


const deportesRestantes = ref(configuracionStore.max_deportes_por_usuario)

const favoritosSeleccionados = computed(() => {
  return Object.values(estadisticasStore.data.tiposDeporte)
    .filter((d: any) => usuario.value.deportesFavoritos.includes(d.id));
});

const addFavorite = (deporte: any) => {
  if (usuario.value.deportesFavoritos.length < 5) {
    usuario.value.deportesFavoritos.push(deporte.id);
    deportesRestantes.value -= 1
  }
};

const removeFavorite = (deporte: any) => {
  usuario.value.deportesFavoritos = usuario.value.deportesFavoritos.filter(id => id !== deporte.id);
  deportesRestantes.value += 1
};

function validarFormulario() {
  let valido = true

  errores.value.sexo = usuario.value.sexo === ''
  errores.value.telefono = usuario.value.telefono === ''
  errores.value.provincia = usuario.value.provincia === ''
  errores.value.municipio = usuario.value.municipio === ''
  errores.value.localidad = usuario.value.localidad === ''
  errores.value.codigoPostal = usuario.value.codigoPostal === ''

  errores.value.password =
    usuario.value.password === '' ||
    usuario.value.password === usuario.value.confirmPassword

  for (const key in errores.value) {
    if (errores.value[key]) {
      valido = false
    }
  }

  return valido
}

/* Solo mandamos al backend para modificar los campos que se hayan modificado */
function camposModificados() {
  const data: any = {}

  if (usuarioFinalStore.usuarioFinal.sexo != usuario.value.sexo) {
    data["sexo"] = usuario.value.sexo
  }

  if (usuarioFinalStore.usuarioFinal.telefono != usuario.value.telefono) {
    data["telefono"] = usuario.value.telefono
  }

  if (usuarioFinalStore.usuarioFinal.provincia != usuario.value.provincia) {
    data["provincia"] = usuario.value.provincia
  }

  if (usuarioFinalStore.usuarioFinal.municipio != usuario.value.municipio) {
    data["municipio"] = usuario.value.municipio
  }

  if (usuarioFinalStore.usuarioFinal.localidad != usuario.value.localidad) {
    data["localidad"] = usuario.value.localidad
  }

  if (usuarioFinalStore.usuarioFinal.codigoPostal != usuario.value.codigoPostal) {
    data["codigoPostal"] = usuario.value.codigoPostal
  }

  if (usuario.value.password) {
    data["password"] = usuario.value.password
  }

  const favoritosActuales = ((usuarioFinalStore.usuarioFinal.deportes as { id: number, titulo: string }[]) || []).map(d => d.id).sort()
  const favoritosNuevosIds = [...usuario.value.deportesFavoritos].sort()

  if (JSON.stringify(favoritosActuales) !== JSON.stringify(favoritosNuevosIds)) {
    data["deportes_ids"] = favoritosNuevosIds
  }

  return data
}

const guardarCambios = async () => {
  try {
    if (!validarFormulario) return

    const data = camposModificados()
    if (Object.keys(data).length > 0) {
      await modificarUsuarioFinal(usuario.value.id, data)
      await usuarioFinalStore.fetchUser(usuario.value.id)
      router.push({
        path: '/perfil'
      })
    }
  } catch (e) {
    console.error("Error al modificar el usuario final", e)
  }
}

/* La variable usuario nos permite cambiar el usuario final unicamente en esta pantalla */
onMounted(async () => {
  const data = usuarioFinalStore.usuarioFinal
  configuracionStore.obtenerConfiguracion()
  if (data) {
    usuario.value = {
      ...usuario.value,
      ...data,
      deportesFavoritos: data.deportesFavoritos.map((d: any) => d.id)
    }
    deportesRestantes.value -= favoritosSeleccionados.value.length
  }
})
</script>

<style scoped>
.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

h2 {
  font-size: 2rem;
}
</style>
