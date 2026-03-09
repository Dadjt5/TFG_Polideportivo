<template>
  <div class="min-vh-100 pt-4" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4" style="max-width: 1600px;">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4 mt-3">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold text-primary mb-2" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
          {{ tarifa.titulo }}
        </h1>

        <div style="width: 100px"></div>
      </div>

      <div class="row g-4">

        <div class="col-12">
          <div class="card shadow-lg rounded-4 p-4"
            style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(10px);">

            <h4 class="mb-3 d-flex align-items-center">
              <i class="bi bi-people-fill text-primary me-2"></i>
              {{ t.tariffDetail }}
            </h4>

            <div class="row g-3">

              <!-- Titulo -->
                <div class="col-12 col-sm-6">
                  <span v-if="!editando">{{ tarifa.titulo }}</span>
                  <input v-else v-model="tarifa.titulo" class="form-control form-control-lg text-center fw-semibold"
                    :class="{ 'is-invalid': errores.titulo }" :placeholder="tarifa.titulo" />
                </div>

              <!-- NUMERO HORAS -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.numberOfHours }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.numeroHoras }}</p>
                <input
                  v-else
                  type="number"
                  min="0"
                  class="form-control form-control-lg"
                  v-model.number="tarifa.numeroHoras"
                  :class="{ 'is-invalid': errores.numeroHoras }"
                />
              </div>

              <!-- NUMERO PERSONAS -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.numberOfPeople }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.numeroPersonas }}</p>
                <input
                  v-else
                  type="number"
                  min="1"
                  class="form-control form-control-lg"
                  v-model.number="tarifa.numeroPersonas"
                  :class="{ 'is-invalid': errores.numeroPersonas }"
                />
              </div>

              <!-- PRECIO BASE -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.price }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.precio }} €</p>
                <input
                  v-else
                  type="number"
                  min="0"
                  step="0.01"
                  class="form-control form-control-lg"
                  v-model.number="tarifa.precio"
                  :class="{ 'is-invalid': errores.precio }"
                />
              </div>

              <!-- PRECIO CUATRIMESTRE -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.quarterPrice }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.precioCuatrimestre }} €</p>
                <input
                  v-else
                  type="number"
                  min="0"
                  step="0.01"
                  class="form-control form-control-lg"
                  v-model.number="tarifa.precioCuatrimestre"
                  :class="{ 'is-invalid': errores.precioCuatrimestre }"
                />
              </div>

              <!-- PRECIO MENSUAL -->
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.monthlyPrice }}:</span>
                <p v-if="!editando" class="fs-5 fw-semibold">{{ tarifa.precioMensual }} €</p>
                <input
                  v-else
                  type="number"
                  min="0"
                  step="0.01"
                  class="form-control form-control-lg"
                  v-model.number="tarifa.precioMensual"
                  :class="{ 'is-invalid': errores.precioMensual }"
                />
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- ACCIONES -->
      <div class="d-flex justify-content-center gap-3 mt-5">
        <button v-if="!editando" class="btn btn-primary btn-lg rounded-pill" @click="activarEdicion">
          <i class="bi bi-pencil me-2"></i> {{ t.modifyTariff }}
        </button>

        <template v-else>
          <button class="btn btn-success btn-lg rounded-pill" @click="guardarCambios">
            <i class="bi bi-check-lg me-2"></i> {{ t.saveChanges }}
          </button>
          <button class="btn btn-secondary btn-lg rounded-pill" @click="cancelarEdicion">
            {{ t.cancel }}
          </button>
        </template>

        <button v-if="!editando" class="btn btn-danger btn-lg rounded-pill" @click="eliminar">
          <i class="bi bi-trash me-2"></i> {{ t.deleteTariff }}
        </button>

      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, inject, onMounted, type Ref } from 'vue'
import { useRouter } from 'vue-router'

import {
  getTarifaGrupoReducidoDetalle,
  modificarTarifaGrupoReducido,
  eliminarTarifaGrupoReducido
} from '@/services/detalleTarifaService'

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter()
const editando = ref(false)

const tarifa = ref({
  id: 0,
  titulo: '',
  numeroHoras: 0,
  numeroPersonas: 0,
  precio: 0,
  precioCuatrimestre: 0,
  precioMensual: 0
})

const errores = ref({
	titulo: false,
  numeroHoras: false,
  numeroPersonas: false,
  precio: false,
  precioCuatrimestre: false,
  precioMensual: false
})

const tarifaOriginal = ref<any>(null)

function validarFormulario() {
  let valido = true

  errores.value.titulo = tarifa.value.titulo === ''
  errores.value.numeroHoras = tarifa.value.numeroHoras <= 0
  errores.value.numeroPersonas = tarifa.value.numeroPersonas <= 0
  errores.value.precio = tarifa.value.precio <= 0
  errores.value.precioCuatrimestre = tarifa.value.precioCuatrimestre <= 0
  errores.value.precioMensual = tarifa.value.precioMensual <= 0

  for (const key in errores.value) {
    if (errores.value[key]) valido = false
  }

  return valido
}

function activarEdicion() {
  tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value))
  Object.keys(errores.value).forEach(k => errores.value[k] = false)
  editando.value = true
}

function cancelarEdicion() {
  tarifa.value = JSON.parse(JSON.stringify(tarifaOriginal.value))
  editando.value = false
}

function camposModificados() {
  const data: any = {}
  for (const key in tarifa.value) {
    if (tarifa.value[key] !== tarifaOriginal.value[key]) {
      data[key] = tarifa.value[key]
    }
  }
  return data
}

const guardarCambios = async () => {
  if (!validarFormulario()) return

  const data = camposModificados()
  if (Object.keys(data).length > 0) {
    await modificarTarifaGrupoReducido(tarifa.value.id, data)
    tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value))
    editando.value = false
  }
}

const eliminar = async () => {
  await eliminarTarifaGrupoReducido(tarifa.value.id)
  router.back()
}

const volver = () => router.back()

onMounted(async () => {
  const id = parseInt(props.id)
  tarifa.value = await getTarifaGrupoReducidoDetalle(id)
  tarifaOriginal.value = JSON.parse(JSON.stringify(tarifa.value))
})
</script>
