<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #e0f7ff, #ffffff);">
    <main class="container py-5" style="max-width: 1120px">
      <h1 class="text-center fw-bold mb-5 text-primary">
        {{ t.newPavilion }}
      </h1>

      <div class="card shadow-lg border-0 rounded-4 p-4"
        style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">

        <div class="row g-4">

          <!-- NOMBRE -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.name }}</label>
            <input type="text" class="form-control form-control-lg" :class="{ 'is-invalid': errores.nombre }"
              v-model="pabellon.nombre" />
          </div>

          <!-- DIRECCIÓN -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.address }}</label>
            <input type="text" class="form-control form-control-lg" :class="{ 'is-invalid': errores.direccion }"
              v-model="pabellon.direccion" />
          </div>

          <!-- IMAGEN -->
          <div class="col-md-12">
            <label class="form-label fw-semibold">{{ t.images }}</label>

            <input type="file" class="form-control form-control-lg"
              accept="image/*" @change="onFileChange" />

            <!-- preview -->
            <img v-if="preview" :src="preview" class="mt-3 rounded" style="max-width:250px" />
          </div>

          <!-- DESCRIPCIÓN -->
          <div class="col-md-12">
            <label class="form-label fw-semibold">{{ t.description }}</label>
            <textarea class="form-control form-control-lg" rows="4" :class="{ 'is-invalid': errores.descripcion }"
              v-model="pabellon.descripcion"></textarea>
          </div>
        </div>

        <p v-if="mensaje" class="text-center text-danger mt-4">
          {{ mensaje }}
        </p>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-5">
          <button class="btn btn-primary btn-lg px-5 rounded-pill shadow-sm" @click="crearPabellon">
            {{ t.newPavilion }}
          </button>

          <button class="btn btn-outline-secondary btn-lg px-5 rounded-pill shadow-sm" @click="volver">
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

import { nuevoPabellon } from "@/services/crearRecursosService"

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const router = useRouter()

const pabellon = ref({
  nombre: "",
  descripcion: "",
  direccion: ""
})

const errores = ref({
  nombre: false,
  descripcion: false,
  direccion: false
})

const mensaje = ref("")
const imagen = ref<File | null>(null)
const preview = ref<string | null>(null)

function validarFormulario() {
  let valido = true

  errores.value.nombre = pabellon.value.nombre === ""
  errores.value.descripcion = pabellon.value.descripcion === ""
  errores.value.direccion = pabellon.value.direccion === ""

  for (const key in errores.value) {
    if (errores.value[key]) {
      valido = false
    }
  }

  return valido
}

const volver = () => router.back();

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  if (!input.files || input.files.length === 0) return

  imagen.value = input.files[0]
  preview.value = URL.createObjectURL(imagen.value)
}

const crearPabellon = async () => {
  if (!validarFormulario()) return

  const formData = new FormData()

  formData.append("nombre", pabellon.value.nombre)
  formData.append("descripcion", pabellon.value.descripcion)
  formData.append("direccion", pabellon.value.direccion)

  if (imagen.value) {
    formData.append("imagenURL", imagen.value)
  }

  try {
    await nuevoPabellon(formData)
    router.back();
  } catch (e) {
    console.log("Error al crear el pabellon", e);
  }
}
</script>
