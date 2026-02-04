<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-5" style="max-width: 1100px">
      <h1 class="text-center mb-5 fw-semibold">{{ t.usersHandle }}</h1>

      <!-- TABS -->
      <div class="card shadow-sm rounded-4">
        <div class="card-body p-4">
          <ul class="nav nav-tabs mb-4" role="tablist">
            <li class="nav-item">
              <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#admins">
                {{ t.admin }}
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link" data-bs-toggle="tab" data-bs-target="#monitores">
                Monitores
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link" data-bs-toggle="tab" data-bs-target="#usuarios">
                {{ t.finalUser }}
              </button>
            </li>
          </ul>

          <div class="tab-content">
            <!-- ADMINISTRADORES -->
            <div class="tab-pane fade show active" id="admins">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="fw-semibold">{{ t.admins }}</h5>
                <router-link to="/registrar/administrador" class="btn btn-primary rounded-pill">
                  {{ t.newAdminTitle }}
                </router-link>
              </div>

              <div class="list-group list-group-flush">
                <div
                  v-for="a in usuarios.administradores"
                  :key="a.id"
                  class="list-group-item d-flex justify-content-between align-items-center rounded-3 mb-2 shadow-sm"
                >

                  <div class="text-primary fw-medium" style="cursor: pointer;"
                    @click="AdministradorDetail(a.id)">
                    <span class="fw-medium">{{ a.nombre }}</span>
                    <span class="text-muted ms-2">({{ a.rol }})</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- MONITORES -->
            <div class="tab-pane fade" id="monitores">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="fw-semibold">{{ t.monitors }}</h5>
                <router-link to="/registrar/monitor" class="btn btn-primary rounded-pill">
                  {{ t.newMonitorTitle }}
                </router-link>
              </div>

              <input
                v-model="searchMonitores"
                type="text"
                class="form-control mb-3"
                placeholder="Buscar monitor..."
              />

              <div class="list-group list-group-flush">
                <div
                  v-for="m in filteredMonitores"
                  :key="m.id"
                  class="list-group-item d-flex justify-content-between align-items-center rounded-3 mb-2 shadow-sm"
                >
									<div class="text-primary fw-medium" style="cursor: pointer;"
                    @click="MonitorDetail(m.id)">
                  	<span class="fw-medium">{{ m.nombre }}</span>
									</div>
                </div>
              </div>
            </div>

            <!-- USUARIOS FINALES -->
            <div class="tab-pane fade" id="usuarios">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="fw-semibold">{{ t.finalUsers }}</h5>
                <router-link to="/registrar/usuario" class="btn btn-primary rounded-pill">
                  {{ t.newFinalUser }}
                </router-link>
              </div>

              <input
                v-model="searchUsuarios"
                type="text"
                class="form-control mb-3"
                placeholder="Buscar usuario..."
              />

              <div class="list-group list-group-flush">
                <div
                  v-for="u in filteredUsuarios"
                  :key="u.id"
                  class="list-group-item d-flex justify-content-between align-items-center rounded-3 mb-2 shadow-sm"
                >
									<div class="text-primary fw-medium" style="cursor: pointer;"
                    @click="UsuarioFinalDetail(u.id)">
      	            <span class="fw-medium">{{ u.nombre }} {{ u.tieneAbono }} {{ u.tieneTDA }} {{ u.esUAM }}</span>
									</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, inject, type Ref, ref, computed } from 'vue'
import { useRouter } from "vue-router";

import { getUsuarios } from '../services/gestionService';

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();

const searchMonitores = ref('')
const searchUsuarios = ref('')

const usuarios = ref({
  finales: [] as {
    id: 0,
    nombre: '',
    tieneTDA: false,
    tieneAbono: false,
    esUAM: false
  }[],
  monitores: [] as {
    id: 0,
    nombre: '',
  }[],
  administradores: [] as {
    id: 0,
    nombre: '',
    rol: ''
  }[]
})

const filteredMonitores = computed(() =>
  usuarios.value.monitores.filter(m =>
    m.nombre.toLowerCase().includes(searchMonitores.value.toLowerCase())
  )
)

const filteredUsuarios = computed(() =>
  usuarios.value.finales.filter(u =>
    u.nombre.toLowerCase().includes(searchUsuarios.value.toLowerCase())
  )
)

const UsuarioFinalDetail = (id: number) => {
  router.push({
    name: 'detalle-usuarioFinal',
    params: { id }
  });
}

const MonitorDetail = (id: number) => {
  router.push({
    name: 'detalle-monitor',
    params: { id }
  });
}

const AdministradorDetail = (id: number) => {
  router.push({
    name: 'detalle-administrador',
    params: { id }
  });
}

onMounted(async () => {
  const data = await getUsuarios()

  usuarios.value.finales = data.usuariosFinales
  usuarios.value.monitores = data.monitores
  usuarios.value.administradores = data.administradores
});
</script>
