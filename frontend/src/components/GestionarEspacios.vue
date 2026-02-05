<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-5" style="max-width: 1000px">
      <h1 class="text-center mb-5 fw-semibold">
        {{ t.manageSpaces }}
      </h1>

      <div class="card shadow-sm rounded-4">
        <div class="card-body p-4">

          <!-- PABELLONES -->
          <div class="mb-5">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="fw-semibold text-primary">
                <i class="bi bi-building me-2"></i>{{ t.pavilions }}
              </h5>
              <button class="btn btn-primary rounded-pill">
                <i class="bi bi-plus-lg me-1"></i> {{ t.new }}
              </button>
            </div>

            <div class="list-group list-group-flush">
              <div
                v-for="p in espacios.pabellones"
                :key="p.id"
                class="list-group-item d-flex justify-content-between align-items-center rounded-3 mb-2 shadow-sm"
              >
                <span class="fw-medium">{{ p.nombre }}</span>
                <button
                  class="btn btn-success btn-sm rounded-pill"
                  @click="verPabellon(p.id)"
                >
                </button>
              </div>
            </div>
          </div>

          <!-- INSTALACIONES -->
          <div>
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="fw-semibold text-success">
                <i class="bi bi-geo-alt me-2"></i>{{ t.facilities }}
              </h5>
              <button class="btn btn-primary rounded-pill">
                <i class="bi bi-plus-lg me-1"></i> {{ t.new }}
              </button>
            </div>

            <div class="list-group list-group-flush">
              <div
                v-for="i in espacios.instalaciones"
                :key="i.id"
                class="list-group-item d-flex justify-content-between align-items-center rounded-3 mb-2 shadow-sm"
              >
                <span class="fw-medium">{{ i.nombre }}</span>
                <button
                  class="btn btn-success btn-sm rounded-pill"
                  @click="verInstalacion(i.id)"
                >
                </button>
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

import { getEspacios } from "../services/gestionService";

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "../useI18N";
import { useI18n } from "../useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

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
})

const verPabellon = (id: number) => {
  router.push({
    name: "detalle-pabellon",
    params: { id }
  })
}

const verInstalacion = (id: number) => {
  router.push({
    name: "detalle-instalacion",
    params: { id }
  })
}

onMounted(async () => {
  const data = await getEspacios();

  espacios.value.pabellones = data.pabellones;
  espacios.value.instalaciones = data.instalaciones;
});
</script>
