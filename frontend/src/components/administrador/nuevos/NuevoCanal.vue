<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #e0f7ff, #ffffff);">
    <main class="container py-5" style="max-width: 1120px;">
      <h1 class="text-center fw-bold mb-5 text-primary">
        {{ t.newChannel }}
      </h1>

      <div class="card shadow-lg border-0 rounded-4 p-4"
           style="background-color: rgba(180,220,255,0.6); backdrop-filter: blur(10px);">

        <div class="row g-4">

          <!-- TÍTULO -->
          <div class="col-12">
            <label class="form-label fw-semibold">{{ t.channelName }}</label>
            <input type="text" class="form-control form-control-lg"
                   v-model="canal.titulo"
                   :class="{ 'is-invalid': errores.titulo }" />
          </div>

          <!-- TEMA -->
          <div class="col-12">
            <label class="form-label fw-semibold">{{ t.theme }}</label>
            <input type="text" class="form-control form-control-lg"
                   v-model="canal.tema"
                   :class="{ 'is-invalid': errores.tema }" />
          </div>

          <!-- OPCIONES -->
          <div class="col-md-6">
            <div class="form-check form-switch fs-5">
              <input class="form-check-input" type="checkbox" v-model="canal.secreto" id="secretoSwitch" />
              <label class="form-check-label" for="secretoSwitch">
                {{ t.secret }}
              </label>
            </div>
          </div>

          <div class="col-md-6">
            <div class="form-check form-switch fs-5">
              <input class="form-check-input" type="checkbox" v-model="canal.oculto" id="ocultoSwitch" />
              <label class="form-check-label" for="ocultoSwitch">
                {{ t.hidden }}
              </label>
            </div>
          </div>

        </div>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-5">
          <button class="btn btn-primary btn-lg px-5 rounded-pill shadow-sm" @click="crearCanal">
            {{ t.newChannel }}
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

import { nuevoCanal } from "@/services/foroService"

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const router = useRouter()

const canal = ref({
  titulo: "",
  tema: "",
  secreto: false,
  oculto: false
})

const errores = ref({
  titulo: false,
  tema: false
})

function validarFormulario() {
  let valido = true

  errores.value.titulo = canal.value.titulo.trim() === ""
  errores.value.tema = canal.value.tema === ""

  for (const key in errores.value) {
    if (errores.value[key]) valido = false
  }

  return valido
}

const volver = () => router.back()

const crearCanal = async () => {
  if (!validarFormulario()) return
	const id = parseInt(props.id)

  try {
    await nuevoCanal(id, canal.value)
    router.back()
  } catch (e) {
    console.error("Error al crear el canal", e)
  }
}
</script>
