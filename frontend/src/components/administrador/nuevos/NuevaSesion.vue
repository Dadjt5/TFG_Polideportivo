<template>
  <div class="min-vh-100 bg-light pb-5">
    <main class="container py-5">
      <h1 class="text-center fw-bold mb-5">
        {{ t.newSession }}
      </h1>

      <div class="card shadow-sm border-0 rounded-4 p-4">
        <div class="row g-4">
          <!-- DÍA -->
          <div class="col-md-12">
            <label class="form-label fw-semibold">{{ t.day }}</label>
            <select class="form-select form-select-lg" :class="{ 'is-invalid': errores.dia }" v-model="sesion.dia">
              <option value="">{{ t.selectOption }}</option>
              <option v-for="d in tipoStore.dias" :key="d[0]" :value="d[0]">
                {{ d[1] }}
              </option>
            </select>
          </div>

          <!-- HORARIO -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">{{ t.schedule }}</label>
            <div class="d-flex gap-2">
              <input type="time" class="form-control" v-model="sesion.horaInicio"
                :class="{ 'is-invalid': errores.horaInicio }" />
              <input type="time" class="form-control" v-model="sesion.horaFin"
                :class="{ 'is-invalid': errores.horaFin }" />
            </div>
          </div>
        </div>

        <!-- BOTONES -->
        <div class="d-flex justify-content-center gap-3 mt-5">
          <button class="btn btn-primary btn-lg px-5" @click="crearSesion">
            {{ t.newSession }}
          </button>

          <button class="btn btn-danger btn-lg px-5" @click="volver">
            {{ t.return }}
          </button>
        </div>
      </div>
    </main>
  </div>
</template>


<script setup lang="ts">
import { ref, inject, type Ref, onMounted } from "vue"
import { useRouter } from "vue-router"

import { nuevaSesion } from "@/services/crearRecursosService"

import { useTiposStore } from "@/stores/tipos"

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!
const t = useI18n(language)

const tipoStore = useTiposStore();
const router = useRouter()

const sesion = ref({
  dia: "",
  horaInicio: "",
  horaFin: "",
  actividad: null as number | null
})

const errores = ref({
  dia: false,
  horaInicio: false,
  horaFin: false
})

const actividades = ref<any[]>([])
const horarios = ref<any[]>([])

function validarFormulario() {
  let valido = true

  errores.value.dia = sesion.value.dia === ""
  errores.value.horaInicio = sesion.value.horaInicio === ""
  errores.value.horaFin =
    sesion.value.horaFin === "" ||
    sesion.value.horaFin <= sesion.value.horaInicio

  for (const key in errores.value) {
    if (errores.value[key]) valido = false
  }

  return valido
}

const volver = () => router.back()

const crearSesion = async () => {
  if (!validarFormulario()) return
  const id = parseInt(props.id);

  try {
    await nuevaSesion({
      ...sesion.value,
      horario: {
        horaInicio: sesion.value.horaInicio,
        horaFin: sesion.value.horaFin
      },
      actividad: Number(props.id)
    })
    router.back()
  } catch (e) {
    console.error("Error al crear la sesión", e)
  }
}

</script>
