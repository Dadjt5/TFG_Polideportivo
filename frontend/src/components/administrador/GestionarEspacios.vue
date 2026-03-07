<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container py-5" style="max-width: 1100px">
      <h1 class="fw-bold text-primary mb-4 text-center">
        <i class="bi bi-grid-1x2-fill me-2"></i>
        {{ t.manageSpaces }}
      </h1>

      <div class="card shadow-lg border-0 rounded-4"
           style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">
        <div class="card-body p-4">

          <!-- TABS -->
          <ul class="nav nav-tabs mb-4">
            <li class="nav-item">
              <button
                class="nav-link"
                :class="{ active: tab === 'pabellones' }"
                @click="tab = 'pabellones'"
              >
                <i class="bi bi-building me-1"></i>
                {{ t.pavilions }}
              </button>
            </li>

            <li class="nav-item">
              <button
                class="nav-link"
                :class="{ active: tab === 'instalaciones' }"
                @click="tab = 'instalaciones'"
              >
                <i class="bi bi-geo-alt me-1"></i>
                {{ t.facilities }}
              </button>
            </li>
          </ul>

          <!-- PABELLONES -->
          <div v-if="tab === 'pabellones'">

            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="fw-semibold text-success">
                {{ t.pavilions }}
              </h5>

              <router-link to="/crear/pabellon" class="btn btn-primary rounded-pill shadow-sm">
                <i class="bi bi-plus-lg me-1"></i>
                {{ t.newPavilion }}
              </router-link>
            </div>
            <div class="list-group list-group-flush">

              <div
                v-for="p in espacios.pabellones"
                :key="p.id"
                class="list-group-item d-flex justify-content-between align-items-center rounded-3 mb-2 shadow-sm border-0"
                style="background-color: rgba(255,255,255,0.9); cursor:pointer"
                @click="PabellonDetail(p.id)"
              >
                <span class="fw-medium text-primary">
                  {{ p.nombre }}
                </span>
                <i class="bi bi-chevron-right text-muted"></i>
              </div>
            </div>
          </div>

          <!-- INSTALACIONES -->
          <div v-if="tab === 'instalaciones'">

            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="fw-semibold text-success">
                {{ t.facilities }}
              </h5>

              <router-link to="/crear/instalacion" class="btn btn-primary rounded-pill shadow-sm">
                <i class="bi bi-plus-lg me-1"></i>
                {{ t.newFacility }}
              </router-link>
            </div>

            <div class="list-group list-group-flush">
              <div
                v-for="i in espacios.instalaciones"
                :key="i.id"
                class="list-group-item d-flex justify-content-between align-items-center rounded-3 mb-2 shadow-sm border-0"
                style="background-color: rgba(255,255,255,0.9); cursor:pointer"
                @click="InstalacionDetail(i.id)"
              >
                <span class="fw-medium text-primary">
                  {{ i.nombre }}
                </span>
                <i class="bi bi-chevron-right text-muted"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, inject, type Ref, ref } from "vue"
import { useRouter } from "vue-router"

import { getEspacios } from "@/services/gestionService";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const tab = ref("pabellones")
const router = useRouter()

const espacios = ref({
  pabellones: [] as {
    id: 0,
    nombre: '',
  }[],
  instalaciones: [] as {
    id: 0,
    nombre: '',
  }[],
});

const PabellonDetail = (id: number) => {
  router.push({
    name: "editar-pabellon",
    params: { id }
  })
};

const InstalacionDetail = (id: number) => {
  router.push({
    name: "editar-instalacion",
    params: { id }
  })
};

onMounted(async () => {
  const data = await getEspacios();

  espacios.value.pabellones = data.pabellones;
  espacios.value.instalaciones = data.instalaciones;
});
</script>
