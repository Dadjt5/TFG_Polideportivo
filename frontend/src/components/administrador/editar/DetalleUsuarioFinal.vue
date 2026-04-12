<template>
  <div class="min-vh-100 pt-4" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4" style="max-width: 1600px;">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4 mt-3">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold mb-0">{{ usuario.nombre }}</h1>

        <div style="width: 100px"></div>
      </div>

      <!-- CARD PRINCIPAL -->
      <div class="card shadow-sm rounded-4 p-4 p-md-5" style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(8px);">

        <!-- AVATAR -->
        <div class="d-flex flex-column flex-md-row align-items-center gap-4 mb-4">
          <div class="rounded-circle bg-info bg-opacity-10 d-flex align-items-center justify-content-center"
               style="width:96px;height:96px">
            <i class="bi bi-person-circle text-info fs-1"></i>
          </div>

          <div class="flex-fill text-center text-md-start">
            <h3 class="fw-semibold mb-1">
              {{ usuario.nombre }} {{ usuario.apellidos }}
            </h3>
            <p class="text-muted mb-0">{{ t.userDetail }}</p>
          </div>
        </div>

        <!-- DATOS PERSONALES -->
        <div class="row g-3">

          <div class="col-md-4">
            <label class="form-label">{{ t.name }}</label>
            <input v-if="isEditing" class="form-control" v-model="usuario.nombre" :class="{ 'is-invalid': errores.nombre }" />
            <p v-else class="form-control-plaintext">{{ usuario.nombre || '-' }}</p>
          </div>

          <div class="col-md-4">
            <label class="form-label">{{ t.surnames }}</label>
            <input v-if="isEditing" class="form-control" v-model="usuario.apellidos" :class="{ 'is-invalid': errores.apellidos }" />
            <p v-else class="form-control-plaintext">{{ usuario.apellidos || '-' }}</p>
          </div>

          <div class="col-md-4">
            <label class="form-label">{{ t.sex }}</label>
            <select v-if="isEditing" class="form-select" :class="{ 'is-invalid': errores.sexo }" v-model="usuario.sexo">
              <option value="Mujer">{{ t.female }}</option>
              <option value="Hombre">{{ t.male }}</option>
              <option value="Prefiero no decirlo">{{ t.other }}</option>
            </select>
            <p v-else class="form-control-plaintext">{{ usuario.sexo || '-' }}</p>
          </div>

          <div class="col-md-4">
            <label class="form-label">{{ t.birth }}</label>
            <input v-if="isEditing" type="date" class="form-control" v-model="usuario.fechaNacimiento" :class="{ 'is-invalid': errores.fechaNacimiento }" />
            <p v-else class="form-control-plaintext">{{ usuario.fechaNacimiento || '-' }}</p>
          </div>

          <div class="col-md-4">
            <label class="form-label">{{ t.phoneNumber }}</label>
            <input v-if="isEditing" class="form-control" v-model="usuario.telefono" :class="{ 'is-invalid': errores.telefono }" />
            <p v-else class="form-control-plaintext">{{ usuario.telefono || '-' }}</p>
          </div>

          <div class="col-md-4">
            <label class="form-label">{{ t.province }}</label>
            <input v-if="isEditing" class="form-control" v-model="usuario.provincia" :class="{ 'is-invalid': errores.provincia }" />
            <p v-else class="form-control-plaintext">{{ usuario.provincia || '-' }}</p>
          </div>

          <div class="col-md-4">
            <label class="form-label">{{ t.municipality }}</label>
            <input v-if="isEditing" class="form-control" v-model="usuario.municipio" :class="{ 'is-invalid': errores.municipio }" />
            <p v-else class="form-control-plaintext">{{ usuario.municipio || '-' }}</p>
          </div>

          <div class="col-md-4">
            <label class="form-label">{{ t.locality }}</label>
            <input v-if="isEditing" class="form-control" v-model="usuario.localidad" :class="{ 'is-invalid': errores.localidad }" />
            <p v-else class="form-control-plaintext">{{ usuario.localidad || '-' }}</p>
          </div>

          <div class="col-md-4">
            <label class="form-label">{{ t.postalCode }}</label>
            <input v-if="isEditing" class="form-control" v-model="usuario.codigoPostal" :class="{ 'is-invalid': errores.codigoPostal }" />
            <p v-else class="form-control-plaintext">{{ usuario.codigoPostal || '-' }}</p>
          </div>

          <div class="col-md-4">
            <label class="form-label">DNI</label>
            <p class="form-control-plaintext">{{ usuario.DNI || '-' }}</p>
          </div>

          <div class="col-md-4">
            <label class="form-label">{{ t.email }}</label>
            <p class="form-control-plaintext">{{ usuario.email }}</p>
          </div>

          <div class="col-md-4">
            <label class="form-label">{{ t.loginCode }}</label>
            <p class="form-control-plaintext">{{ usuario.codigo_usuario || '-' }}</p>
          </div>

          <div class="col-md-4">
            <label class="form-label">{{ t.madeActivities }}</label>
            <p class="form-control-plaintext">{{ usuario.actividadesRealizadas }}</p>
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
        <div v-if="mostrarMensaje" class="text-center mb-3 mt-3">
          <div class="alert" :class="tipoMensaje === 'success' ? 'alert-success' : 'alert-danger'">
            {{ mensajeEditar }}
          </div>
        </div>

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
            <i class="bi bi-trash me-2"></i> {{ t.delete }}
          </button>
        </div>

      </div>
    </main>

    <!-- MODALES -->
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
            <button class="btn btn-secondary rounded-pill" data-bs-dismiss="modal">{{ t.cancel }}</button>
            <button class="btn btn-danger rounded-pill" @click="confirmarEliminar">{{ t.deleteUser }}</button>
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
            <h4 class="fw-semibold">{{ mensaje }}</h4>
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
const mensajeEditar = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)

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

  const hoy = new Date()
  const fechaNacimiento = new Date(usuario.value.fechaNacimiento)

	errores.value.nombre = usuario.value.nombre === ''
	errores.value.apellidos = usuario.value.apellidos === ''
  errores.value.sexo = usuario.value.sexo === ''
  errores.value.fechaNacimiento = usuario.value.fechaNacimiento === ''
  errores.value.telefono = usuario.value.telefono === ''
  errores.value.provincia = usuario.value.provincia === ''
  errores.value.municipio = usuario.value.municipio === ''
  errores.value.localidad = usuario.value.localidad === ''
  errores.value.codigoPostal = usuario.value.codigoPostal === ''

  errores.value.fechaNacimiento =
    !usuario.value.fechaNacimiento || fechaNacimiento >= hoy

  for (const key in errores.value) {
    if(errores.value[key]) {
      valido = false
    }
  }

  return valido
}

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensajeEditar.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true

  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
}

const mensaje = ref("")

function activarEdicion() {
  usuarioOriginal.value = JSON.parse(JSON.stringify(usuario.value))
	Object.keys(errores.value).forEach(k => errores.value[k] = false)
  isEditing.value = true
}

function cancelarEdicion() {
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
  if (!validarFormulario()) {
    lanzarMensaje(t.value.missing, "error")
    return
  }
  
  try {
		const data = camposModificados();
    if(Object.keys(data).length > 0) {
      await modificarUsuarioFinal(usuario.value.id, data);
      lanzarMensaje(t.value.correctlyUpdate, "success")
    } else {
      lanzarMensaje(t.value.noChanges, "success")
    }

    isEditing.value = false
  } catch (e) {
    lanzarMensaje(t.value.noModify, "error")
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
		usuarioOriginal.value = JSON.parse(JSON.stringify(usuario.value))
	} catch(e) {
    mensaje.value = t.value.unexpectedError
		console.log("Error al obtener informacion del usuario final", e);
	}
});
</script>