<template>
  <div class="min-vh-100 bg-light py-4">
    <main class="container">
      <h2 class="mb-4 text-center fw-bold">{{ t.personalDataTitle }}</h2>

      <!-- Información no editable -->
      <div class="card shadow-sm mb-4">
        <div class="card-body">
          <h5 class="fw-semibold mb-3">{{ t.inmutableData }}</h5>

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
          </div>

          <div class="row g-3 mt-3">
            <div class="col-md-4">
              <label class="form-label">{{ t.birth }}</label>
              <input type="date" class="form-control" v-model="usuario.fechaNacimiento" disabled>
            </div>
          </div>
        </div>
      </div>

      <!-- Información editable -->
      <div class="card shadow-sm mb-4">
        <div class="card-body">
          <h5 class="fw-semibold mb-3">{{ t.editableData }}</h5>

          <div class="row g-3">
            <div class="col-md-4">
              <label class="form-label">{{ t.sex }}</label>
              <select class="form-select" v-model="usuario.sexo">
                <option value="male">{{ t.male }}</option>
                <option value="female">{{ t.female }}</option>
                <option value="other">{{ t.other }}</option>
              </select>
            </div>

            <div class="col-md-4">
              <label class="form-label">{{ t.phoneNumber }}</label>
              <input type="text" class="form-control" v-model="usuario.telefono">
            </div>

            <div class="col-md-4">
              <label class="form-label">{{ t.province }}</label>
              <input type="text" class="form-control" v-model="usuario.provincia">
            </div>

            <div class="col-md-4">
              <label class="form-label">{{ t.municipality }}</label>
              <input type="text" class="form-control" v-model="usuario.municipio">
            </div>

            <div class="col-md-4">
              <label class="form-label">{{ t.locality }}</label>
              <input type="text" class="form-control" v-model="usuario.localidad">
            </div>

            <div class="col-md-4 mt-3">
              <label class="form-label">{{ t.postalCode }}</label>
              <input type="text" class="form-control" v-model="usuario.codigoPostal">
            </div>
          </div>

          <!-- CUENTA -->
          <div class="mb-4 mt-4">
            <h5 class="fw-semibold mb-3">{{ t.account }}</h5>
            <input type="text" class="form-control" v-model="usuario.cuentaBancaria">
          </div>
        </div>
      </div>

      <!-- Deportes favoritos -->
      <div class="container py-4 mb-4">
        <h2 class="mb-4">{{ t.favoriteSports }}</h2>

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

import { useUserStore } from '../stores/usuarioFinal'
import { useEstadisticasStore } from '../stores/estadisticas';

import { modificarUsuarioFinal } from '../services/usuarioFinalService';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const usuarioFinalStore = useUserStore()
const estadisticasStore = useEstadisticasStore()

const router = useRouter()

const usuario = ref({
  id: 0,
  nombre: '',
  apellidos: '',
  DNI: '',
  fechaNacimiento: '',
  telefono: '',
  provincia: '',
  municipio: '',
  localidad: '',
  codigoPostal: '',
  cuentaBancaria: '',
  sexo: '',
  deportesFavoritos: [] as number[],
})

const deportesRestantes = ref(5)

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

/* Solo mandamos al backend para modificar los campos que se hayan modificado */
function camposModificados() {
  const data: any = {}

  if(usuarioFinalStore.usuarioFinal.sexo != usuario.value.sexo) {
      data["sexo"] = usuario.value.sexo
  }

  if(usuarioFinalStore.usuarioFinal.telefono != usuario.value.telefono) {
    data["telefono"] = usuario.value.telefono
  }

  if(usuarioFinalStore.usuarioFinal.provincia != usuario.value.provincia) {
    data["provincia"] = usuario.value.provincia
  }

  if(usuarioFinalStore.usuarioFinal.municipio != usuario.value.municipio) {
    data["municipio"] = usuario.value.municipio
  }

  if(usuarioFinalStore.usuarioFinal.localidad != usuario.value.localidad) {
    data["localidad"] = usuario.value.localidad
  }

  if(usuarioFinalStore.usuarioFinal.codigoPostal != usuario.value.codigoPostal) {
    data["codigoPostal"] = usuario.value.codigoPostal
  }

  if(usuarioFinalStore.usuarioFinal.cuentaBancaria != usuario.value.cuentaBancaria) {
    data["cuentaBancaria"] = usuario.value.cuentaBancaria
  }

  const favoritosActuales = ((usuarioFinalStore.usuarioFinal.deportes as {id: number, titulo: string}[]) || []).map(d => d.id).sort()
  const favoritosNuevosIds = [...usuario.value.deportesFavoritos].sort()

  if(JSON.stringify(favoritosActuales) !== JSON.stringify(favoritosNuevosIds)) {
    data["deportes_ids"] = favoritosNuevosIds
  }

  return data
}

const guardarCambios = async () => {
  try {
    const data = camposModificados()
    if(Object.keys(data).length > 0) {
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
  if(data) {
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
