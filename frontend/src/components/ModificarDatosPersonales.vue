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
                <option value="">{{ t.selectOption }}</option>
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

          <!-- DEPORTES FAVORITOS -->
          <div class="mb-4">
            <h5 class="fw-semibold mb-3">{{ t.favoriteSports }}</h5>
            <select class="form-select" v-model="usuario.deportesFavoritos" multiple>
              <option v-for="deporte in Object.values(estadisticasStore.data.tiposDeporte)" :key="deporte.id" :value="deporte.id">
                {{ deporte.titulo }}
              </option>
            </select>
          </div>

        </div>
      </div>

      <!-- BOTÓN GUARDAR -->
      <div class="text-center mb-5">
        <button class="btn btn-primary btn-lg px-4" @click="guardarCambios">
          {{ t.saveChanges }}
        </button>
      </div>

    </main>
  </div>
</template>


<script setup lang="ts">
import { type Ref, inject, ref, onMounted } from 'vue'

import { useUserStore } from '../stores/usuarioFinal'
import { useEstadisticasStore } from '../stores/estadisticas';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const usuarioFinalStore = useUserStore()
const estadisticasStore = useEstadisticasStore()

const usuario = ref({
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
  deportesFavoritos: [] as string[],
})

const guardarCambios = async () => {
  try {
    //await actualizarUsuarioFinal(usuario.value)
  } catch (error) {
    console.error(error)
  }
}

onMounted(async () => {
  const data = usuarioFinalStore.usuarioFinal
  if (data) {
    usuario.value = {
      ...usuario.value,
      ...data,
      deportesFavoritos: data.deportesFavoritos.map((d: any) => d.id)
    }
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
