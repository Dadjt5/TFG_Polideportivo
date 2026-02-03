<template>
  <div class="min-vh-100 bg-light pb-5">
    <main class="container py-5" style="max-width: 1100px">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <button class="btn btn-secondary rounded-pill">
          ← {{ t.return }}
        </button>
        <h1 class="fw-semibold mb-0">{{ t.userDetail }}</h1>
        <div style="width: 100px"></div>
      </div>

      <!-- CARD PRINCIPAL -->
      <div class="card shadow-sm rounded-4">
        <div class="card-body p-4 p-md-5">
          <!-- CABECERA -->
          <div class="d-flex flex-column flex-md-row align-items-center gap-4 mb-4">
            <div class="rounded-circle bg-primary bg-opacity-10 d-flex align-items-center justify-content-center" style="width:96px;height:96px">
              <i class="bi bi-person-fill text-primary fs-1"></i>
            </div>
            <div class="flex-fill text-center text-md-start">
              <h3 class="fw-semibold mb-1">{{ usuario.nombre }} {{ usuario.apellidos }}</h3>
              <span class="badge bg-info">{{ usuario.rol }}</span>
            </div>
          </div>

          <!-- DATOS -->
          <div class="row g-3">
            <InfoItem label="DNI" :value="usuario.DNI" />
            <InfoItem label="Sexo" :value="usuario.sexo" />
            <InfoItem label="Fecha de nacimiento" :value="usuario.fechaNacimiento" />
            <InfoItem label="Teléfono" :value="usuario.telefono" />
            <InfoItem label="Provincia" :value="usuario.provincia" />
            <InfoItem label="Municipio" :value="usuario.municipio" />
            <InfoItem label="Localidad" :value="usuario.localidad" />
            <InfoItem label="Código postal" :value="usuario.codigoPostal" />

            <InfoItem
              v-if="usuario.cuentaBancaria"
              label="Cuenta bancaria"
              :value="usuario.cuentaBancaria"
            />

            <InfoItem
              label="Actividades realizadas"
              :value="usuario.actividadesRealizadas"
            />
          </div>

          <!-- ESTADOS -->
          <div class="d-flex flex-wrap gap-3 mt-4">
            <span class="badge" :class="usuario.esUAM ? 'bg-success' : 'bg-secondary'">
              {{ usuario.esUAM ? 'Usuario UAM' : 'Usuario externo' }}
            </span>
            <span class="badge" :class="usuario.tieneAbono ? 'bg-primary' : 'bg-secondary'">
              {{ usuario.tieneAbono ? 'Tiene abono' : 'Sin abono' }}
            </span>
            <span class="badge" :class="usuario.tieneTDA ? 'bg-warning text-dark' : 'bg-secondary'">
              {{ usuario.tieneTDA ? 'Tiene TDA' : 'Sin TDA' }}
            </span>
          </div>

          <!-- DEPORTES -->
          <div class="mt-4">
            <h5 class="fw-semibold">{{ t.favouritesSports }}</h5>
            <div class="d-flex flex-wrap gap-2 mt-2">
              <span
                v-for="d in usuario.deportesFavoritos"
                :key="d"
                class="badge bg-light text-dark border"
              >
                {{ d }}
              </span>
              <span v-if="usuario.deportesFavoritos.length === 0" class="text-muted">
                {{ t. }}
              </span>
            </div>
          </div>

          <!-- ACCIONES -->
          <div class="d-flex justify-content-center gap-4 mt-5">
            <button class="btn btn-primary btn-lg rounded-pill">
							<i class="bi bi-pencil text-primary fs-4"></i>
              {{ t.modifyUser }}
            </button>
            <button class="btn btn-danger btn-lg rounded-pill">
							<i class="bi bi-trash text-primary fs-4"></i>
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

import { getUsuarioFinal } from '../services/usuarioFinalService';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const usuario = ref({
  nombre: '',
  apellidos: '',
  DNI: '',
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
  rol: '',
  deportesFavoritos: []
})

onMounted(async () => {
  const id = parseInt(props.id);

	try {
	  usuario.value = await getUsuarioFinal(id);
	} catch(e) {
		console.log("Error al obtener informacion del usuario final", e)
	}
});
</script>