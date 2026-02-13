<template>
  <div class="min-vh-100 bg-light pb-5">
    <main class="container py-5" style="max-width: 1100px">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <button class="btn btn-secondary rounded-pill" @click="volver">
          ← {{ t.return }}
        </button>

        <h1 class="fw-semibold mb-0">{{ t.userDetail }}</h1>

        <div style="width: 100px"></div>
      </div>

      <div class="card shadow-sm rounded-4">
        <div class="card-body p-4 p-md-5">

          <!-- USUARIO -->
          <div class="d-flex flex-column flex-md-row align-items-center gap-4 mb-4">
            <div
              class="rounded-circle bg-primary bg-opacity-10 d-flex align-items-center justify-content-center"
              style="width:96px;height:96px"
            >
              <i class="bi bi-person-fill text-primary fs-1"></i>
            </div>

            <div class="flex-fill text-center text-md-start">
              <h3 class="fw-semibold mb-1">
                {{ usuario.nombre }} {{ usuario.apellidos }}
              </h3>
            </div>
          </div>

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
              <input
                v-if="isEditing"
                class="form-control"
                v-model="usuario.DNI"
								:class="{ 'is-invalid': errores.DNI }"
              />
              <p v-else class="form-control-plaintext">
                {{ usuario.DNI || '-' }}
              </p>
            </div>

            <!-- SEXO -->
            <div class="col-md-4">
              <label class="form-label">{{ t.sex }}</label>
              <select v-if="isEditing" class="form-select" :class="{ 'is-invalid': errores.sexo }" v-model="usuario.sexo">
                <option value="M">{{ t.male }}</option>
                <option value="F">{{ t.female }}</option>
                <option value="N">{{ t.other }}</option>
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

            <!-- CUENTA -->
            <div class="col-md-4">
              <label class="form-label">{{ t.account }}</label>
              <input
                v-if="isEditing"
                class="form-control"
                v-model="usuario.cuentaBancaria"
								:class="{ 'is-invalid': errores.cuentaBancaria }"
              />
              <p v-else class="form-control-plaintext">
                {{ usuario.cuentaBancaria || '-' }}
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

          <!-- ACCIONES -->
          <div class="d-flex justify-content-center gap-4 mt-5">

            <button
              v-if="!isEditing"
              class="btn btn-primary btn-lg rounded-pill"
              @click="activarEdicion"
            >
              <i class="bi bi-pencil me-2"></i>
              {{ t.modifyUser }}
            </button>

            <template v-else>
              <button
                class="btn btn-success btn-lg rounded-pill"
                @click="guardarCambios"
              >
                <i class="bi bi-check-lg me-2"></i>
                {{ t.saveChanges }}
              </button>

              <button
                class="btn btn-secondary btn-lg rounded-pill"
                @click="cancelarEdicion"
              >
                {{ t.cancel }}
              </button>
            </template>

            <button
              v-if="!isEditing"
              class="btn btn-danger btn-lg rounded-pill"
              @click="eliminar"
            >
              <i class="bi bi-trash me-2"></i>
              {{ t.deleteUser }}
            </button>

          </div>
        </div>
      </div>
    </main>
  </div>
</template>


<script setup lang="ts">
import { type Ref, ref, inject, onMounted } from 'vue'
import { useRouter } from 'vue-router'

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
  email: '',
  sexo: '',
  fechaNacimiento: '',
  telefono: '',
  provincia: '',
  municipio: '',
  localidad: '',
  codigoPostal: '',
  cuentaBancaria: '',
  actividadesRealizadas: 0,
  esUAM: false,
  tieneAbono: false,
  tieneTDA: false,
  deportesFavoritos: []
});

const errores = ref({
	nombre: false,
  apellidos: false,
  DNI: false,
  sexo: false,
  fechaNacimiento: false,
  telefono: false,
  provincia: false,
  municipio: false,
  localidad: false,
  codigoPostal: false,
  cuentaBancaria: false,
})


const usuarioOriginal = ref<any>(null);

function validarFormulario() {
  let valido = true

	errores.value.nombre = usuario.value.nombre === ''
	errores.value.apellidos = usuario.value.apellidos === ''
	errores.value.DNI = 
		usuario.value.DNI === '' ||
		usuario.value.DNI.length !== 9
  errores.value.sexo = usuario.value.sexo === ''
  errores.value.fechaNacimiento = usuario.value.fechaNacimiento === ''
  errores.value.telefono = usuario.value.telefono === ''
  errores.value.provincia = usuario.value.provincia === ''
  errores.value.municipio = usuario.value.municipio === ''
  errores.value.localidad = usuario.value.localidad === ''
  errores.value.codigoPostal = usuario.value.codigoPostal === ''

  errores.value.cuentaBancaria =
    usuario.value.cuentaBancaria !== '' &&
    usuario.value.cuentaBancaria.length < 20

  for (const key in errores.value) {
    if(errores.value[key]) {
      valido = false
    }
  }

  return valido
}

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

	if(usuarioOriginal.value.nombre != usuario.value.nombre) {
      data["nombre"] = usuario.value.nombre
  }

	if(usuarioOriginal.value.apellidos != usuario.value.apellidos) {
      data["apellidos"] = usuario.value.apellidos
  }

	if(usuarioOriginal.value.DNI != usuario.value.DNI) {
      data["DNI"] = usuario.value.DNI
  }

  if(usuarioOriginal.value.sexo != usuario.value.sexo) {
      data["sexo"] = usuario.value.sexo
  }

  if(usuarioOriginal.value.telefono != usuario.value.telefono) {
    data["telefono"] = usuario.value.telefono
  }

  if(usuarioOriginal.value.provincia != usuario.value.provincia) {
    data["provincia"] = usuario.value.provincia
  }

  if(usuarioOriginal.value.municipio != usuario.value.municipio) {
    data["municipio"] = usuario.value.municipio
  }

  if(usuarioOriginal.value.localidad != usuario.value.localidad) {
    data["localidad"] = usuario.value.localidad
  }

  if(usuarioOriginal.value.codigoPostal != usuario.value.codigoPostal) {
    data["codigoPostal"] = usuario.value.codigoPostal
  }

  if(usuarioOriginal.value.cuentaBancaria != usuario.value.cuentaBancaria) {
    data["cuentaBancaria"] = usuario.value.cuentaBancaria
  }

  const favoritosActuales = ((usuarioOriginal.value.deportes as {id: number, titulo: string}[]) || []).map(d => d.id).sort()
  const favoritosNuevosIds = [...usuario.value.deportesFavoritos].sort()

  if(JSON.stringify(favoritosActuales) !== JSON.stringify(favoritosNuevosIds)) {
    data["deportes_ids"] = favoritosNuevosIds;
  }

  return data;
}

const guardarCambios = async () => {
  try {
		if (!validarFormulario()) return

		const data = camposModificados();
    if(Object.keys(data).length > 0) {
      await modificarUsuarioFinal(usuario.value.id, data);
    }
  } catch (e) {
    console.error("Error al modificar el usuario final", e);
  }
}

const eliminar = async () => {
  try {
    await eliminarUsuarioFinal(usuario.value.id)
  } catch (e) {
    console.error("Error al eliminar el usuario final", e);
  }
}

function volver() {
  router.back()
}

onMounted(async () => {
  const id = parseInt(props.id);

	try {
	  usuario.value = await getUsuarioFinal(id);
		usuarioOriginal.value = JSON.parse(JSON.stringify(usuario.value))
	} catch(e) {
		console.log("Error al obtener informacion del usuario final", e);
	}
});
</script>