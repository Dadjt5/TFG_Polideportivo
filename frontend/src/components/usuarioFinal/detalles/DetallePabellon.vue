<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4">

      <!-- Cabecera -->
      <div class="text-center mt-4 mb-5">
        <h1 class="fw-semibold text-primary mb-0" style="text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
          <i class="bi bi-building me-2"></i>{{ pabellon.nombre }}
        </h1>
      </div>

      <div class="row g-4">

        <!-- DETALLES -->
        <div class="col-lg-6">
          <div class="bg-white rounded-3 shadow-sm p-4 h-100 card-hover">

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
                  <i class="bi bi-geo-alt-fill text-danger me-1"></i>
                  <span class="fw-medium">{{ t.address }}:</span><br />
                  {{ pabellon.direccion }}
                </p>
              </div>

            </div>

          </div>
        </div>

        <!-- IMÁGENES -->
        <div class="col-lg-6 d-flex flex-column gap-4">
          <div class="card shadow-lg rounded-4 p-4"
            style="background-color: rgba(255,255,255,0.75); backdrop-filter: blur(10px);">

            <h4 class="mb-3 d-flex align-items-center gap-2">
              <i class="bi bi-images text-primary"></i>
              {{ t.images }}
            </h4>

            <span v-if="pabellon.imagen">
              <img :src="pabellon.imagen" class="img-fluid rounded mb-3 img-hover" />
            </span>
            <span v-else class="text-center text-muted mt-5">
              <i class="bi bi-image fs-1"></i>
              <p class="mt-3">{{ t.noImage }}</p>
            </span>
          </div>
        </div>

      </div>

      <!-- INSTALACIONES -->
      <div class="mt-5">
        <div class="bg-white rounded-4 shadow-sm p-4 card-hover">
          <h4 class="mb-4 d-flex align-items-center">
            <i class="bi bi-grid-3x3-gap-fill text-primary me-2"></i>
            {{ t.facilities }}
          </h4>

          <div v-if="pabellon.instalaciones?.length" class="row g-4">
            <div v-for="instalacion in pabellon.instalaciones" :key="instalacion.id" class="col-md-6 col-xl-4">
              <div class="border rounded-4 p-3 h-100 shadow-sm facility-card" style="cursor: pointer;" @click="facilityDetail(instalacion.id)">
                <img v-if="instalacion.imagen" :src="instalacion.imagen" class="img-fluid rounded mb-3"
                  style="height: 180px; width: 100%; object-fit: cover;" />

                <div v-else class="text-center text-muted py-4">
                  <i class="bi bi-image fs-2"></i>
                </div>

                <h5 class="fw-semibold">
                  {{ instalacion.nombre }}
                </h5>

                <p class="text-muted small mb-2">
                  {{ instalacion.tipoInstalacion }}
                </p>

                <p class="mb-0">
                  <i class="bi bi-people-fill me-1 text-primary"></i>
                  {{ t.capacity }}: {{ instalacion.aforoMaximo }}
                </p>
              </div>
            </div>
          </div>

          <div v-else class="text-center text-muted">
            <i class="bi bi-grid fs-1"></i>
            <p class="mt-3">{{ t.noFacilities }}</p>
          </div>
        </div>
      </div>

      <!-- Botones -->
      <div class="d-flex justify-content-center gap-4 mt-5">
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

import { getPabellonDetalle } from "@/services/detalleService"

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const props = defineProps<{ id: string }>();

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();

const pabellon = ref({
  id: 0,
  nombre: "",
  descripcion: "",
  imagen: "",
  direccion: "",
  instalaciones: [] as {
    id: number
    nombre: string
    imagen?: string
    tipoInstalacion: string
    aforoMaximo: number
  }[]
});

const pabellonOriginal = ref<any>(null);

const facilityDetail = (id: number) => {
  router.push({
    name: 'detalle-instalacion',
    params: { id }
  });
}

const volver = () => {
  router.back();
};

onMounted(async () => {
  const id = parseInt(props.id);

  try {
    pabellon.value = await getPabellonDetalle(id);
    pabellonOriginal.value = JSON.parse(JSON.stringify(pabellon.value))
  } catch (e) {
    console.log("Error al obtener la informacion del pabellon", e);
  }
});
</script>
