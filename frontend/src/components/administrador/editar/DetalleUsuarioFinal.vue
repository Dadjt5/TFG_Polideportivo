<template>
  <div class="min-vh-100 pt-4" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4" style="max-width: 1600px;">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4 mt-3">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold text-primary mb-2" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
          {{ usuario.nombre }}
        </h1>

        <div style="width: 100px"></div>
      </div>

      <div class="card shadow-sm rounded-4">
        <div class="card shadow-lg rounded-4 p-4"
            style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(10px);">

            <h4 class="mb-3 d-flex align-items-center">
              <i class="bi bi-currency-euro text-primary me-2"></i>
              {{ t.userDetail }}
            </h4>


          <!-- DATOS PERSONALES -->
          <div class="row g-3">

						<!-- Nombre -->
            <div class="col-md-4">
              <label class="form-label">{{ t.name }}</label>
              <input
                v-if="isEditing"
                class="form-control"
                v-model="usuario.nombre"
								:class="{ 'is-invalid': errores.nombre }"
              />
              <p v-else class="form-control-plaintext">
                {{ usuario.nombre || '-' }}
              </p>
            </div>

						<!-- Apellidos -->
            <div class="col-md-4">
              <label class="form-label">{{ t.surnames }}</label>
              <input
                v-if="isEditing"
                class="form-control"
                v-model="usuario.apellidos"
								:class="{ 'is-invalid': errores.apellidos }"
              />
              <p v-else class="form-control-plaintext">
                {{ usuario.apellidos || '-' }}
              </p>
            </div>

            <!-- DNI -->
            <div class="col-md-4">
              <label class="form-label">DNI</label>
              <p class="form-control-plaintext">
                {{ usuario.DNI || '-' }}
              </p>
            </div>

            <!-- Codigo usuario -->
            <div class="col-md-4">
              <label class="form-label">{{ t.loginCode }}</label>
              <p class="form-control-plaintext">
                {{ usuario.codigo_usuario || '-' }}
              </p>
            </div>

            <!-- SEXO -->
            <div class="col-md-4">
              <label class="form-label">{{ t.sex }}</label>
              <select v-if="isEditing" class="form-select" :class="{ 'is-invalid': errores.sexo }" v-model="usuario.sexo">
                <option value="MUJER">{{ t.female }}</option>
                <option value="HOMBRE">{{ t.male }}</option>
                <option value="NINGUNO">{{ t.other }}</option>
              </select>
              <p v-else class="form-control-plaintext">{{ usuario.sexo || '-' }}</p>
            </div>

            <!-- FECHA NACIMIENTO -->
            <div class="col-md-4">
              <label class="form-label">{{ t.birth }}</label>
              <input
                v-if="isEditing"
                type="date"
                class="form-control"
                v-model="usuario.fechaNacimiento"
								:class="{ 'is-invalid': errores.fechaNacimiento }"
              />
              <p v-else class="form-control-plaintext">
                {{ usuario.fechaNacimiento || '-' }}
              </p>
            </div>

            <!-- TELÉFONO -->
            <div class="col-md-4">
              <label class="form-label">{{ t.phoneNumber }}</label>
              <input
                v-if="isEditing"
                class="form-control"
                v-model="usuario.telefono"
								:class="{ 'is-invalid': errores.telefono }"
              />
              <p v-else class="form-control-plaintext">
                {{ usuario.telefono || '-' }}
              </p>
            </div>

            <!-- PROVINCIA -->
            <div class="col-md-4">
              <label class="form-label">{{ t.province }}</label>
              <input
                v-if="isEditing"
                class="form-control"
                v-model="usuario.provincia"
								:class="{ 'is-invalid': errores.provincia }"
              />
              <p v-else class="form-control-plaintext">
                {{ usuario.provincia || '-' }}
              </p>
            </div>

            <!-- MUNICIPIO -->
            <div class="col-md-4">
              <label class="form-label">{{ t.municipality }}</label>
              <input
                v-if="isEditing"
                class="form-control"
                v-model="usuario.municipio"
								:class="{ 'is-invalid': errores.municipio }"
              />
              <p v-else class="form-control-plaintext">
                {{ usuario.municipio || '-' }}
              </p>
            </div>

            <!-- LOCALIDAD -->
            <div class="col-md-4">
              <label class="form-label">{{ t.locality }}</label>
              <input
                v-if="isEditing"
                class="form-control"
                v-model="usuario.localidad"
								:class="{ 'is-invalid': errores.localidad }"
              />
              <p v-else class="form-control-plaintext">
                {{ usuario.localidad || '-' }}
              </p>
            </div>

            <!-- CÓDIGO POSTAL -->
            <div class="col-md-4">
              <label class="form-label">{{ t.postalCode }}</label>
              <input
                v-if="isEditing"
                class="form-control"
                v-model="usuario.codigoPostal"
								:class="{ 'is-invalid': errores.codigoPostal }"
              />
              <p v-else class="form-control-plaintext">
                {{ usuario.codigoPostal || '-' }}
              </p>
            </div>

            <!-- ACTIVIDADES -->
            <div class="col-md-4">
              <label class="form-label">{{ t.madeActivities }}</label>
              <p class="form-control-plaintext">
                {{ usuario.actividadesRealizadas }}
              </p>
            </div>

            <!-- Correo -->
            <div class="col-md-4">
              <label class="form-label">{{ t.email }}</label>
              <p class="form-control-plaintext">
                {{ usuario.email }}
              </p>
            </div>
          </div>

          <!-- ESTADOS -->
          <div class="mt-4">
            <h5 class="fw-semibold mb-3">{{ t.userStatus }}</h5>

            <div v-if="isEditing" class="d-flex gap-4 flex-wrap">
              <div class="form-check form-switch">
                <input class="form-check-input" type="checkbox" v-model="usuario.esUAM">
                <label class="form-check-label">{{ t.UAMuser }}</label>
              </div>

              <div class="form-check form-switch">
                <input class="form-check-input" type="checkbox" v-model="usuario.tieneAbono">
                <label class="form-check-label">{{ t.hasSubscripcion }}</label>
              </div>

              <div class="form-check form-switch">
                <input class="form-check-input" type="checkbox" v-model="usuario.tieneTDA">
                <label class="form-check-label">{{ t.hasTDA }}</label>
              </div>
            </div>

            <div v-else class="d-flex gap-3 flex-wrap">
              <span class="badge" :class="usuario.esUAM ? 'bg-success' : 'bg-secondary'">
                {{ usuario.esUAM ? t.UAMuser : t.externalUser }}
              </span>
              <span class="badge" :class="usuario.tieneAbono ? 'bg-primary' : 'bg-secondary'">
                {{ usuario.tieneAbono ? t.hasSubscripcion : t.hasntSubscripcion  }}
              </span>
              <span class="badge" :class="usuario.tieneTDA ? 'bg-warning text-dark' : 'bg-secondary'">
                {{ usuario.tieneTDA ? t.hasTDA : t.hasntTDA  }}
              </span>
            </div>
          </div>

          <!-- MENSAJE -->
          <p v-if="mensaje" class="text-center text-danger mt-4">
            {{ mensaje }}
          </p>

          <!-- ACCIONES -->
      <div class="d-flex justify-content-center gap-3 mt-5">
        <button v-if="!isEditing" class="btn btn-primary btn-lg rounded-pill" @click="activarEdicion">
          <i class="bi bi-pencil me-2"></i> {{ t.modifyUser }}
        </button>

        <template v-else>
          <button class="btn btn-success btn-lg rounded-pill" @click="guardarCambios">
            <i class="bi bi-check-lg me-2"></i> {{ t.saveChanges }}
          </button>
          <button class="btn btn-secondary btn-lg rounded-pill" @click="cancelarEdicion">
            {{ t.cancel }}
          </button>
        </template>

        <button v-if="!isEditing" class="btn btn-danger btn-lg rounded-pill" @click="abrirConfirmacion">
          <i class="bi bi-trash me-2"></i> {{ t.deleteUser }}
        </button>

      </div>
        </div>
      </div>
    </main>

    <div class="modal fade" id="confirmDeleteModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4">

          <div class="modal-header">
            <h5 class="modal-title">{{ t.confirmDelete }}</h5>
          </div>

          <div class="modal-body text-center">
            <p>{{ t.confirmDeleteFinalUser }}</p>
          </div>

          <div class="modal-footer justify-content-center">
            <button class="btn btn-secondary rounded-pill" data-bs-dismiss="modal">
              {{ t.cancel }}
            </button>

            <button class="btn btn-danger rounded-pill" @click="confirmarEliminar">
              {{ t.deleteUser }}
            </button>
          </div>

        </div>
      </div>
    </div>

    <div class="modal fade" id="successDeleteModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4 text-center">

          <div class="modal-body py-5">

            <i v-if="eliminado" class="bi bi-check-circle-fill text-success fs-1 mb-3"></i>
            <i v-else class="bi bi-exclamation-octagon-fill text-danger fs-1 mb-3"></i>

            <h4 class="fw-semibold">
              {{ mensaje }}
            </h4>

            <button class="btn btn-primary rounded-pill mt-4" @click="finalizar" data-bs-dismiss="modal">
              <span v-if="eliminado">{{ t.continue }}</span>
              <span v-else>{{ t.return }}</span>
            </button>

          </div>

        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { type Ref, ref, inject, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Modal } from 'bootstrap'

import { getUsuarioFinal, modificarUsuarioFinal, eliminarUsuarioFinal } from '@/services/usuarioFinalService';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter()
const isEditing = ref(false);

const usuario = ref({
	id: 0,
  nombre: '',
  apellidos: '',
  DNI: '',
  codigo_usuario: '',
  email: '',
  sexo: '',
  fechaNacimiento: '',
  telefono: '',
  provincia: '',
  municipio: '',
  localidad: '',
  codigoPostal: '',
  actividadesRealizadas: 0,
  esUAM: false,
  tieneAbono: false,
  tieneTDA: false,
  deportesFavoritos: []
});

const errores = ref({
	nombre: false,
  apellidos: false,
  sexo: false,
  fechaNacimiento: false,
  telefono: false,
  provincia: false,
  municipio: false,
  localidad: false,
  codigoPostal: false,
})


const usuarioOriginal = ref<any>(null);

function validarFormulario() {
  let valido = true

	errores.value.nombre = usuario.value.nombre === ''
	errores.value.apellidos = usuario.value.apellidos === ''
  errores.value.sexo = usuario.value.sexo === ''
  errores.value.fechaNacimiento = usuario.value.fechaNacimiento === ''
  errores.value.telefono = usuario.value.telefono === ''
  errores.value.provincia = usuario.value.provincia === ''
  errores.value.municipio = usuario.value.municipio === ''
  errores.value.localidad = usuario.value.localidad === ''
  errores.value.codigoPostal = usuario.value.codigoPostal === ''

  for (const key in errores.value) {
    if(errores.value[key]) {
      valido = false
    }
  }

  return valido
}

const mensaje = ref("")

function activarEdicion() {
  mensaje.value = ""
  usuarioOriginal.value = JSON.parse(JSON.stringify(usuario.value))
	Object.keys(errores.value).forEach(k => errores.value[k] = false)
  isEditing.value = true
}

function cancelarEdicion() {
  mensaje.value = ""
  usuarioOriginal.value = JSON.parse(JSON.stringify(usuario.value))
  isEditing.value = false
}

/* Solo mandamos al backend para modificar los campos que se hayan modificado */
function camposModificados() {
  const data: any = {}

  const camposDirectos = [
    "nombre",
    "apellidos",
    "DNI",
    "email",
    "sexo",
    "fechaNacimiento",
    "telefono",
    "provincia",
    "municipio",
    "localidad",
    "codigoPostal",
    "esUAM",
    "tieneAbono",
    "tieneTDA"
  ];

  camposDirectos.forEach(campo => {
    if(usuarioOriginal.value[campo] !== usuario.value[campo]) {
      data[campo] = usuario.value[campo];
    }
  });

  const favoritosActuales = ((usuarioOriginal.value.deportes as {id: number, titulo: string}[]) || []).map(d => d.id).sort();
  const favoritosNuevosIds = [...usuario.value.deportesFavoritos].sort();

  if(JSON.stringify(favoritosActuales) !== JSON.stringify(favoritosNuevosIds)) {
    data["deportes_ids"] = favoritosNuevosIds;
  }

  return data;
}

const guardarCambios = async () => {
  mensaje.value = ""
  try {
		if (!validarFormulario()) return

		const data = camposModificados();
    console.log(data)
    if(Object.keys(data).length > 0) {
      await modificarUsuarioFinal(usuario.value.id, data);
    }
    isEditing.value = false
  } catch (e) {
    console.error("Error al modificar el usuario final", e);
  }
}

let confirmModal: Modal
let successModal: Modal

const eliminado = ref(false)

function abrirConfirmacion() {
  confirmModal.show()
}

async function confirmarEliminar() {
  try {
    await eliminarUsuarioFinal(usuario.value.id)

    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.finalUserDeleted
    eliminado.value = true
  } catch (e) {
    confirmModal.hide()
    successModal.show()

    mensaje.value = t.value.finalUserNoDeleted
    eliminado.value = false
    console.error("Error al eliminar el usuario final", e);
  }
}

const finalizar = async () => {
  if (eliminado.value) {
    router.push({ name: 'gestion-usuarios' });
  } else {
    successModal.hide()
    eliminado.value = false
  }
}

function volver() {
  router.back()
}

onMounted(async () => {
  const id = parseInt(props.id);

  confirmModal = new Modal(document.getElementById('confirmDeleteModal')!)
  successModal = new Modal(document.getElementById('successDeleteModal')!)

	try {
	  usuario.value = await getUsuarioFinal(id);
    console.log(usuario.value)
		usuarioOriginal.value = JSON.parse(JSON.stringify(usuario.value))
	} catch(e) {
    mensaje.value = t.value.unexpectedError
		console.log("Error al obtener informacion del usuario final", e);
	}
});
</script>