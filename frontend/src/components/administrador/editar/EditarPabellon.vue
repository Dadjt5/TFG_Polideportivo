<template>
  <div class="min-vh-100 pt-4" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4" style="max-width: 1600px;">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4 mt-3">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold text-primary mb-2" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
          {{ pabellon.nombre}}
        </h1>

        <div style="width: 100px"></div>
      </div>

      <div class="row g-4">

        <!-- INFORMACIÓN -->
        <div class="col-lg-6">
          <div class="card shadow-lg rounded-4 p-4"
            style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(10px);">

            <h4 class="mb-4 d-flex align-items-center">
              <i class="bi bi-info-circle-fill text-primary me-2"></i>
              {{ t.pavilionDetail }}
            </h4>

            <div class="row g-3">

              <!-- NOMBRE -->
              <div class="col-12">
                <label class="form-label fw-semibold">{{ t.name }}</label>
                <input v-model="pabellon.nombre"
                  :class="['form-control', 'form-control-lg', { 'is-invalid': errores.nombre }]"
                  :readonly="!editando" />
              </div>

              <!-- DESCRIPCION -->
              <div class="col-12">
                <label class="form-label fw-semibold">{{ t.description }}</label>
                <textarea v-model="pabellon.descripcion" class="form-control form-control-lg" rows="3"
                  :readonly="!editando"></textarea>
              </div>

              <!-- DIRECCION -->
              <div class="col-12">
                <label class="form-label fw-semibold">{{ t.address }}</label>
                <input v-model="pabellon.direccion" class="form-control form-control-lg" :readonly="!editando" />
              </div>

            </div>
          </div>
        </div>

        <!-- IMAGEN -->
        <div class="col-lg-6">
          <div class="card shadow-lg rounded-4 p-4"
            style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(10px);" v-if="pabellon.imagenURL">

            <h4 class="mb-3 d-flex align-items-center gap-2">
              <i class="bi bi-images text-primary"></i>
              {{ t.images }}
            </h4>

            <img :src="pabellon.imagenURL" class="img-fluid rounded mb-3 img-hover" />

            <input v-if="editando" v-model="pabellon.imagenURL" class="form-control form-control-lg"
              placeholder="URL imagen" />
          </div>
        </div>

      </div>

      <!-- ACCIONES -->
      <div class="d-flex justify-content-center gap-3 mt-5">
        <button v-if="!editando" class="btn btn-primary btn-lg rounded-pill" @click="activarEdicion">
          <i class="bi bi-pencil me-2"></i> {{ t.modifyPavilion }}
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
          <i class="bi bi-trash me-2"></i> {{ t.deletePavilion }}
        </button>

      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { inject, ref, onMounted, type Ref } from 'vue';
import { useRouter } from "vue-router";

import { getPabellonDetalle, modificarPabellon, eliminarPabellon } from "@/services/detalleService";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();

const editando = ref(false)

const pabellon = ref({
  id: 0,
  nombre: "",
  descripcion: "",
  imagenURL: "",
  direccion: ""
})

const errores = ref({
  nombre: false
})

const pabellonOriginal = ref<any>(null);

function validarFormulario() {
  let valido = true
  errores.value.nombre = pabellon.value.nombre.trim() === ''
  if (errores.value.nombre) valido = false
  return valido
}

function activarEdicion() {
  pabellonOriginal.value = JSON.parse(JSON.stringify(pabellon.value))
  errores.value.nombre = false
  editando.value = true
}

function cancelarEdicion() {
  pabellon.value = JSON.parse(JSON.stringify(pabellonOriginal.value))
  editando.value = false
}

function camposModificados() {
  const data: any = {}

  if (pabellonOriginal.value.nombre !== pabellon.value.nombre) {
    data.nombre = pabellon.value.nombre
  }
  if (pabellonOriginal.value.descripcion !== pabellon.value.descripcion) {
    data.descripcion = pabellon.value.descripcion
  }
  if (pabellonOriginal.value.direccion !== pabellon.value.direccion) {
    data.direccion = pabellon.value.direccion
  }
  if (pabellonOriginal.value.imagenURL !== pabellon.value.imagenURL) {
    data.imagenURL = pabellon.value.imagenURL
  }

  return data
}

const guardarCambios = async () => {
  if (!validarFormulario()) return
  const data = camposModificados()
  if (Object.keys(data).length > 0) {
    try {
      await modificarPabellon(pabellon.value.id, data)
      editando.value = false
    } catch (e) {
      console.error("Error al modificar el pabellon", e)
    }
  } else {
    editando.value = false
  }
}

const eliminar = async () => {
  try {
    await eliminarPabellon(pabellon.value.id)
    router.back()
  } catch (e) {
    console.error("Error al eliminar el pabellon", e)
  }
}

const volver = () => router.back();

onMounted(async () => {
  try {
    pabellon.value = await getPabellonDetalle(parseInt(props.id))
    pabellonOriginal.value = JSON.parse(JSON.stringify(pabellon.value))
  } catch (e) {
    console.error("Error al obtener información del pabellon", e)
  }
})
</script>