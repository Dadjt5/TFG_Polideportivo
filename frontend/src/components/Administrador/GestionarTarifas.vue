<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-5" style="max-width: 1100px">
      <h1 class="text-center mb-5 fw-semibold">
        {{ t.manageRates }}
      </h1>

      <div class="card shadow-sm rounded-4">
        <div class="card-body p-4">

          <!-- TARIFAS INSTALACIÓN -->
          <div class="mb-5">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="fw-semibold text-success">
                <i class="bi bi-geo-alt me-2"></i>{{ t.facilityTariff }}
              </h5>
							<router-link to="/crear/tarifa/instalacion" class="btn btn-primary rounded-pill">
                <i class="bi bi-plus-lg me-1"></i> {{ t.newTariff }}
              </router-link>
            </div>

            <div class="list-group list-group-flush">
              <div
                v-for="tarifa in tarifasInstalacion"
                :key="tarifa.id"
                class="list-group-item rounded-3 mb-2 shadow-sm d-flex justify-content-between align-items-center"
                @click="tarifaInstalacionDetail(tarifa.id)"
              >
                <div>
                  <div class="fw-medium text-primary">
                    {{ tarifa.titulo }}
                  </div>
                  <div class="text-muted small">
                    UAM: {{ tarifa.precioUAM }}€ ·
                    {{ t.subscription }}: {{ tarifa.precioAbonado }}€ ·
                    {{ t.other }}: {{ tarifa.precioOtros }}€
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- TARIFAS TDA -->
          <div class="mb-5">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="fw-semibold text-success">
                <i class="bi bi-geo-alt me-2"></i>{{ t.TDATariff }}
              </h5>
							<router-link to="/crear/tarifa/TDA" class="btn btn-primary rounded-pill">
                <i class="bi bi-plus-lg me-1"></i> {{ t.newTariff }}
              </router-link>
            </div>

            <div class="list-group list-group-flush">
              <div
                v-for="tarifa in tarifasTDA"
                :key="tarifa.id"
                class="list-group-item rounded-3 mb-2 shadow-sm d-flex justify-content-between align-items-center"
                @click="tarifaTDADetail(tarifa.id)"
              >
                <div>
                  <div class="fw-medium text-primary">
                    {{ tarifa.titulo }}
                  </div>
                  <div class="text-muted small">
                    UAM: {{ tarifa.precioUAM }}€ ·
                    {{ t.other }}: {{ tarifa.precioOtros }}€
                    {{ t.repositionPrice }}: {{ tarifa.precioReposicion }}€
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- ACTIVIDAD COMÚN -->
          <div class="mb-5">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="fw-semibold text-success">
                <i class="bi bi-people me-2"></i>{{ t.commonActivityTariff }}
              </h5>
							<router-link to="/crear/tarifa/comun" class="btn btn-primary rounded-pill">
                <i class="bi bi-plus-lg me-1"></i> {{ t.newTariff }}
              </router-link>
            </div>

            <div class="list-group list-group-flush">
              <div
                v-for="tarifa in tarifasActividadComun"
                :key="tarifa.id"
                class="list-group-item rounded-3 mb-2 shadow-sm"
                @click="tarifaActividadComunDetail(tarifa.id)"
              >
                <div class="fw-medium text-primary">
                   {{ t.weekHours }}: {{ tarifa.numeroHorasSemana }}h
                </div>
                <div class="text-muted small">
                  UAM: {{ tarifa.precioUAM }}€ · {{ t.other }}: {{ tarifa.precioOtros }}€
                </div>
              </div>
            </div>
          </div>

          <!-- GRUPOS REDUCIDOS -->
          <div class="mb-5">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="fw-semibold text-success">
                <i class="bi bi-person-badge me-2"></i>{{ t.smallGroupsTariff }}
              </h5>
							<router-link to="/crear/tarifa/grupos" class="btn btn-primary rounded-pill">
                <i class="bi bi-plus-lg me-1"></i> {{ t.newTariff }}
              </router-link>
            </div>

            <div class="list-group list-group-flush">
              <div
                v-for="tarifa in tarifasGrupoReducido"
                :key="tarifa.id"
                class="list-group-item rounded-3 mb-2 shadow-sm"
                @click="tarifaGrupoReducidoDetail(tarifa.id)"
              >
                <div class="fw-medium text-primary">
                  {{ tarifa.numeroPersonas }} {{ t.people }} · {{ tarifa.numeroHoras }}h
                </div>
                <div class="text-muted small">
                  {{ t.price }}: {{ tarifa.precio }}€
                </div>
              </div>
            </div>
          </div>

          <!-- FISIOTERAPIA -->
          <div>
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="fw-semibold text-success">
                <i class="bi bi-heart-pulse me-2"></i>{{ t.physiotherapyTariff }}
              </h5>
							<router-link to="/crear/tarifa/fisioterapia" class="btn btn-primary rounded-pill">
                <i class="bi bi-plus-lg me-1"></i> {{ t.newTariff }}
              </router-link>
            </div>

            <div class="list-group list-group-flush">
              <div
                v-for="tarifa in tarifasFisioterapia"
                :key="tarifa.id"
                class="list-group-item rounded-3 mb-2 shadow-sm"
                @click="tarifaFisioterapiaDetail(tarifa.id)"
              >
                <div class="fw-medium text-primary">
                  {{ t.physiotherapyTariff }}
                </div>
                <div class="text-muted small">
                  UAM: {{ tarifa.precioConsultaUAM }}€ · {{ t.other }}: {{ tarifa.precioConsultaOtros }}€
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
import { ref, inject, type Ref, onMounted } from "vue"
import { useRouter } from "vue-router"

import { getTarifas } from "@/services/gestionService"

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();

const tarifasInstalacion = ref<any[]>([]);
const tarifasTDA = ref<any[]>([]);
const tarifasActividadComun = ref<any[]>([]);
const tarifasGrupoReducido = ref<any[]>([]);
const tarifasFisioterapia = ref<any[]>([]);


const tarifaInstalacionDetail = (id: number) => {
  router.push({
    name: "editar-tarifa-instalacion",
    params: { id }
  })
};

const tarifaTDADetail = (id: number) => {
  router.push({
    name: "editar-tarifa-TDA",
    params: { id }
  })
};

const tarifaActividadComunDetail = (id: number) => {
  router.push({
    name: "editar-tarifa-actividad-comun",
    params: { id }
  })
};

const tarifaGrupoReducidoDetail = (id: number) => {
  router.push({
    name: "editar-tarifa-grupo-reducido",
    params: { id }
  })
};

const tarifaFisioterapiaDetail = (id: number) => {
  router.push({
    name: "editar-tarifa-fisioterapia",
    params: { id }
  })
};

onMounted(async () => {
  try {
    const data = await getTarifas();

    tarifasInstalacion.value = data.tarifasInstalacion
    tarifasTDA.value = data.tarifasTDA
    tarifasActividadComun.value = data.tarifasActividadComun
    tarifasGrupoReducido.value = data.tarifasGrupoReducido
    tarifasFisioterapia.value = data.tarifasFisioterapia
  } catch(e) {
    console.log("Error al obtener las tarifas", e);
  }
});
</script>
