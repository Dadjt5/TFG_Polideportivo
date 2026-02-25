<template>
  <div class="min-vh-100 bg-light">
    <main class="container-fluid mt-2 px-5 py-4">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold mb-0 text-center flex-grow-1">
          <span v-if="!editando">{{ instalacion.nombre }}</span>
          <input
            v-else
            v-model="instalacion.nombre"
            class="form-control text-center fw-semibold"
            :class="{ 'is-invalid': errores.nombre }"
          />
        </h1>

        <div style="width: 120px"></div>
      </div>

      <div class="row g-4">

        <!-- COLUMNA IZQUIERDA: INFO GENERAL + IMÁGENES -->
        <div class="col-lg-6 d-flex flex-column gap-4">

          <!-- INFORMACIÓN GENERAL -->
          <div class="bg-white rounded-4 shadow-sm p-4">
            <h4 class="mb-4 d-flex align-items-center">
              <i class="bi bi-info-circle-fill text-primary me-2"></i>
              {{ t.facilityDetails }}
            </h4>

            <div class="row g-3">
              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.capacity }}:</span>
                <p v-if="!editando">{{ instalacion.aforoMaximo }}</p>
                <input
                  v-else
                  type="number"
                  min="1"
                  class="form-control"
                  v-model.number="instalacion.aforoMaximo"
                  :class="{ 'is-invalid': errores.aforoMaximo }"
                />
              </div>

              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.light }}:</span>
                <p v-if="!editando">{{ instalacion.luz ? t.yes : 'No' }}</p>
                <div v-else class="form-check mt-1">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    v-model="instalacion.luz"
                    id="luzCheck"
                  />
                  <label class="form-check-label" for="luzCheck">{{ t.light }}</label>
                </div>
              </div>

              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.tdaPercent }}:</span>
                <p v-if="!editando">{{ instalacion.porcentajeTDA }} %</p>
                <input
                  v-else
                  type="number"
                  min="0"
                  max="100"
                  class="form-control"
                  v-model.number="instalacion.porcentajeTDA"
                  :class="{ 'is-invalid': errores.porcentajeTDA }"
                />
              </div>

              <div class="col-12 col-sm-6">
                <span class="fw-medium">{{ t.facilityType }}:</span>
                <p v-if="!editando">{{ instalacion.tipoInstalacion }}</p>
                <select
                  v-else
                  class="form-select"
                  v-model="instalacion.tipoInstalacion"
                >
                  <option value="">---</option>
                  <option value="Pista">Pista</option>
                  <option value="Sala">Sala</option>
                  <option value="Piscina">Piscina</option>
                </select>
              </div>

              <div class="col-12 col-sm-6" v-if="instalacion.pabellon">
                <span class="fw-medium">{{ t.pavilion }}:</span>
                <p>{{ instalacion.pabellon.nombre }}</p>
              </div>

              <div class="col-12 col-sm-6" v-if="instalacion.pabellon">
                <span class="fw-medium">{{ t.address }}:</span>
                <p>{{ instalacion.pabellon.direccion }}</p>
              </div>
            </div>
          </div>

          <!-- IMÁGENES -->
          <div class="bg-white rounded-4 shadow-sm p-4" v-if="instalacion.imagenURL.length">
            <h4 class="mb-3 d-flex align-items-center gap-2">
              <i class="bi bi-images text-primary"></i>
              {{ t.images }}
            </h4>

            <div class="row g-3">
              <div class="col-6" v-for="(img, i) in instalacion.imagenURL" :key="i">
                <img :src="img" class="img-fluid rounded mb-2 shadow-sm" />
                <input
                  v-if="editando"
                  v-model="instalacion.imagenURL[i]"
                  class="form-control"
                  placeholder="URL imagen"
                />
              </div>
            </div>
          </div>

        </div>

        <!-- COLUMNA DERECHA: HORARIO -->
        <div class="col-lg-6">

          <div class="bg-white rounded-4 shadow-sm p-4 h-100">

            <h5 class="fw-semibold mb-3 d-flex align-items-center">
              <i class="bi bi-clock text-primary me-2"></i>
              Horario semanal
            </h5>

            <div
              v-for="(dia, index) in instalacion.agenda"
              :key="dia.dia"
              class="border rounded-4 p-3 mb-3 bg-light"
            >
              <div class="d-flex justify-content-between align-items-center mb-2">
                <strong>{{ dia.dia }}</strong>

                <div v-if="editando" class="form-check form-switch">
                  <input class="form-check-input" type="checkbox" v-model="dia.abierto" />
                  <label class="form-check-label">
                    {{ dia.abierto ? 'Abierto' : 'Cerrado' }}
                  </label>
                </div>

                <span
                  v-else
                  class="fw-semibold"
                  :class="dia.abierto ? 'text-success' : 'text-danger'"
                >
                  {{ dia.abierto ? 'Abierto' : 'Cerrado' }}
                </span>
              </div>

              <div v-if="dia.abierto" class="row g-2">
                <div class="col-6">
                  <label class="small text-muted">Apertura</label>
                  <p v-if="!editando" class="mb-0">{{ dia.horaApertura?.slice(0,5) }}</p>
                  <input v-else type="time" class="form-control" v-model="dia.horaApertura" />
                </div>
                <div class="col-6">
                  <label class="small text-muted">Cierre</label>
                  <p v-if="!editando" class="mb-0">{{ dia.horaCierre?.slice(0,5) }}</p>
                  <input v-else type="time" class="form-control" v-model="dia.horaCierre" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ACCIONES -->
      <div class="d-flex justify-content-center gap-4 mt-5">
        <button v-if="!editando" class="btn btn-primary btn-lg rounded-pill px-4" @click="activarEdicion">
          <i class="bi bi-pencil me-2"></i>
          {{ t.modifyFacility }}
        </button>

        <template v-else>
          <button class="btn btn-success btn-lg rounded-pill px-4" @click="guardarCambios">
            <i class="bi bi-check-lg me-2"></i>
            {{ t.saveChanges }}
          </button>

          <button class="btn btn-secondary btn-lg rounded-pill px-4" @click="cancelarEdicion">
            {{ t.cancel }}
          </button>
        </template>

        <button v-if="!editando" class="btn btn-danger btn-lg rounded-pill px-4" @click="eliminar">
          <i class="bi bi-trash me-2"></i>
          {{ t.deleteFacility }}
        </button>
      </div>

    </main>
  </div>
</template>
yyy

<script setup lang="ts">
import { inject, ref, onMounted, type Ref } from 'vue';
import { useRouter } from "vue-router";

/* Importamos la comunicacion para recuperar la informacion de instalaciones del backend */
import { getInstalacionDetalle, modificarInstalacion, eliminarInstalacion } from "@/services/detalleService";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();

const editando = ref(false)

const instalacion = ref({
  id: 0,
  nombre: "",
  imagenURL: [] as string[],
  aforoMaximo: 50,
  luz: false,
  porcentajeTDA: 0,
  pabellon: { id: -1, nombre: "", direccion: "" },
  tipoInstalacion: "",
  agenda: [] as any[]
});

const errores = ref({
	nombre: false,
  aforoMaximo: false,
  porcentajeTDA: false,
  horaApertura: false,
  horaCierre: false,
  tipoInstalacion: false
})

const instalacionOriginal = ref<any>(null);

function validarFormulario() {
  let valido = true

	errores.value.nombre = instalacion.value.nombre === ''
	errores.value.aforoMaximo = instalacion.value.aforoMaximo <= 0
	errores.value.porcentajeTDA = instalacion.value.porcentajeTDA <= 0
	errores.value.tipoInstalacion = instalacion.value.tipoInstalacion === ''

  for (const key in errores.value) {
    if(errores.value[key]) {
      valido = false
    }
  }

  return valido
}

function activarEdicion() {
  instalacionOriginal.value = JSON.parse(JSON.stringify(instalacion.value))
	Object.keys(errores.value).forEach(k => errores.value[k] = false)
  editando.value = true
}

function cancelarEdicion() {
  instalacionOriginal.value = JSON.parse(JSON.stringify(instalacion.value))
  editando.value = false
}

/* Solo mandamos al backend para modificar los campos que se hayan modificado */
function camposModificados() {
  const data: any = {}

	if(instalacionOriginal.value.nombre != instalacion.value.nombre) {
      data["nombre"] = instalacion.value.nombre
  }

	if(instalacionOriginal.value.porcentajeTDA != instalacion.value.porcentajeTDA) {
      data["porcentajeTDA"] = instalacion.value.porcentajeTDA
  }

	if(instalacionOriginal.value.aforoMaximo != instalacion.value.aforoMaximo) {
      data["aforoMaximo"] = instalacion.value.aforoMaximo
  }

	if(instalacionOriginal.value.luz != instalacion.value.luz) {
      data["luz"] = instalacion.value.luz
  }

	if(instalacionOriginal.value.tipoInstalacion != instalacion.value.tipoInstalacion) {
      data["tipoInstalacion"] = instalacion.value.tipoInstalacion
  }

  return data;
}


const guardarCambios = async () => {
  try {
		if (!validarFormulario()) return

		const data = camposModificados();
    if(Object.keys(data).length > 0) {
      await modificarInstalacion(instalacion.value.id, data);
    }
  } catch (e) {
    console.error("Error al modificar la instalacion", e);
  }
}

const eliminar = async () => {
  try {
    await eliminarInstalacion(instalacion.value.id)
  } catch (e) {
    console.error("Error al eliminar la instalacion", e);
  }
}

const volver = () => {
  router.back();
};

onMounted(async () => {
  const id = parseInt(props.id);

  try {
    instalacion.value = await getInstalacionDetalle(id);
    instalacionOriginal.value = JSON.parse(JSON.stringify(instalacion.value))
  } catch(e) {
    console.log("Error al obtener la informacion de la instalacion", e);
  }
});
</script>
