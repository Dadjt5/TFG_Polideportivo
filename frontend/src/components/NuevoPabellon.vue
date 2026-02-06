<template>
  <div class="min-vh-100 bg-light pb-5">
    <main class="container py-5">
      <h1 class="text-center fw-bold mb-5">
        {{ t.newPavilion }}
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
              v-model="pabellon.nombre"
            />
          </div>

          <!-- DIRECCIÓN -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.address }}</label>
            <input
              type="text"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.direccion }"
              v-model="pabellon.direccion"
            />
          </div>

          <!-- IMAGEN -->
          <div class="col-md-12">
            <label class="form-label fw-semibold">{{ t.images }}</label>
            <input
              type="text"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errores.imagenURL }"
              v-model="pabellon.imagenURL"
              placeholder="https://..."
            />
          </div>

          <!-- DESCRIPCIÓN -->
          <div class="col-md-12">
            <label class="form-label fw-semibold">{{ t.description }}</label>
            <textarea
              class="form-control form-control-lg"
              rows="4"
              :class="{ 'is-invalid': errores.descripcion }"
              v-model="pabellon.descripcion"
            ></textarea>
          </div>
        </div>

        <p v-if="mensaje" class="text-center text-danger mt-4">
          {{ mensaje }}
        </p>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-5">
          <button
            class="btn btn-primary btn-lg px-5"
            @click="crearPabellon"
          >
            {{ t.newPavilion }}
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
import { ref, inject, type Ref } from "vue"
import { useRouter } from "vue-router"

import { nuevoPabellon } from "../services/crearRecursos"

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N"
import { useI18n } from "../useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const router = useRouter()

const pabellon = ref({
  nombre: "",
  descripcion: "",
  imagenURL: "",
  direccion: ""
})

const errores = ref({
  nombre: false,
  descripcion: false,
  imagenURL: false,
  direccion: false
})

const mensaje = ref("")

function validarFormulario() {
  let valido = true

  errores.value.nombre = pabellon.value.nombre === ""
  errores.value.descripcion = pabellon.value.descripcion === ""
  errores.value.imagenURL = pabellon.value.imagenURL === ""
  errores.value.direccion = pabellon.value.direccion === ""

  for (const key in errores.value) {
    if (errores.value[key]) {
      valido = false
    }
  }

  return valido
}

const volver = () => router.back();

const crearPabellon = async () => {
  if (!validarFormulario()) return

  try {
    await nuevoPabellon(pabellon.value);
    router.back();
  } catch (e) {
    console.log("Error al crear el pabellon", e);
  }
}
</script>
