<template>
  <div class="min-vh-100 bg-light">
    <main class="container-fluid mt-2 px-5 py-4">

      <div class="text-center mt-4 mb-5">
        <h1 class="fw-semibold">{{ pabellon.nombre }}</h1>
      </div>

      <div class="row g-4">
        <div class="col-lg-6">
          <div class="bg-white rounded-3 shadow-sm p-4 h-100">
            <h4 class="mb-3 d-flex align-items-center">
              <i class="bi bi-info-circle-fill text-primary me-2"></i>
              {{ t.pavilionDetail }}
            </h4>

            <div class="row g-3">

              <div class="col-12">
                <p>
                  <span class="fw-medium">{{ t.description }}:</span><br />
                  <span class="text-muted">
                    {{ pabellon.descripcion || t.noDescription }}
                  </span>
                </p>
              </div>

              <div class="col-12">
                <p>
                  <span class="fw-medium">{{ t.address }}:</span>
                  {{ pabellon.direccion }}
                </p>
              </div>

            </div>

            <div v-if="editando" class="mt-4 d-flex gap-3">
              <button class="btn btn-success" @click="guardarCambios">
                <i class="bi bi-check-lg me-1"></i>{{ t.save }}
              </button>

              <button class="btn btn-secondary" @click="cancelarEdicion">
                {{ t.cancel }}
              </button>
            </div>

          </div>
        </div>

        <div class="col-lg-6 d-flex flex-column gap-4">

          <div class="bg-white rounded-3 shadow-sm p-4" v-if="pabellon.imagenURL">
            <h4 class="mb-3 d-flex align-items-center gap-2">
              <i class="bi bi-images text-primary"></i>
              {{ t.images }}
            </h4>

            <div class="row g-2">
              <div class="col-6" v-for="(img, i) in pabellon.imagenURL" :key="i">
                <img :src="img" class="img-fluid rounded" alt="Pabellon" />
              </div>
            </div>
          </div>

        </div>

      </div>

      <!-- Botones -->
       <div class="d-flex justify-content-center gap-4 mt-5">
        <button v-if="authStore.role === 'administrador'" class="btn btn-danger btn-lg px-4" @click="activarEdicion">
          <i class="bi bi-pencil me-1"></i>
          {{ t.modifyPavilion }}
        </button>

        <button v-if="authStore.role === 'administrador'" class="btn btn-danger btn-lg px-4" @click="eliminar">
          <i class="bi bi-trash me-1"></i>
          {{ t.delete }}
        </button>

        <button class="btn btn-secondary btn-lg px-5" @click="volver">
          {{ t.return }}
        </button>
      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { inject, ref, onMounted, type Ref } from "vue"
import { useRouter } from "vue-router"

import { useAuthStore } from "../stores/auth"

import { getPabellon, modificarPabellon, eliminarPabellon } from "../services/detalleService"

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N"
import { useI18n } from "../useI18N"

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const authStore = useAuthStore();
const router = useRouter();

const editando = ref(false)

const pabellon = ref({
  id: 0,
  nombre: "",
  descripcion: "",
  imagenURL: "",
  direccion: ""
});

const errores = ref({
	nombre: false,
  direccion: false
})

const pabellonOriginal = ref<any>(null);

function validarFormulario() {
  let valido = true

	errores.value.nombre = pabellon.value.nombre === ''
	errores.value.direccion = pabellon.value.direccion === ''

  for (const key in errores.value) {
    if(errores.value[key]) {
      valido = false
    }
  }

  return valido
}

function activarEdicion() {
  pabellonOriginal.value = JSON.parse(JSON.stringify(pabellon.value))
	Object.keys(errores.value).forEach(k => errores.value[k] = false)
  editando.value = true
}

function cancelarEdicion() {
  pabellonOriginal.value = JSON.parse(JSON.stringify(pabellon.value))
  editando.value = false
}

/* Solo mandamos al backend para modificar los campos que se hayan modificado */
function camposModificados() {
  const data: any = {}

	if(pabellonOriginal.value.nombre != pabellon.value.nombre) {
      data["nombre"] = pabellon.value.nombre
  }

	if(pabellonOriginal.value.direccion != pabellon.value.direccion) {
      data["direccion"] = pabellon.value.direccion
  }

  return data;
}

const guardarCambios = async () => {
  try {
		if (!validarFormulario()) return

		const data = camposModificados();
    if(Object.keys(data).length > 0) {
      await modificarPabellon(pabellon.value.id, data);
    }
  } catch (e) {
    console.error("Error al modificar el pabellon", e);
  }
}

const eliminar = async () => {
  try {
    await eliminarPabellon(pabellon.value.id)
  } catch (e) {
    console.error("Error al eliminar el pabellon", e);
  }
}

const volver = () => {
  router.back();
};

onMounted(async () => {
  const id = parseInt(props.id);

  try {
    pabellon.value = await getPabellon(id);
		pabellonOriginal.value = JSON.parse(JSON.stringify(pabellon.value))
  } catch(e) {
		console.log("Error al obtener la informacion del pabellon", e);
	}
});
</script>
