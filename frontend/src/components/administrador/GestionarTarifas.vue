<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-5" style="max-width: 1100px">
      <h1 class="text-center mb-5 fw-semibold">
        {{ t.manageRates }}
      </h1>

      <div class="card shadow-sm rounded-4">
        <div class="card-body p-4">

          <!-- TABS -->
          <ul class="nav nav-tabs mb-4" role="tablist">
            <li class="nav-item">
              <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#tarifas" type="button">
                {{ t.manageRates }}
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link" data-bs-toggle="tab" data-bs-target="#bonos" type="button">
                {{ t.bonus }}
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link" data-bs-toggle="tab" data-bs-target="#abonos" type="button">
                {{ t.subscription }}
              </button>
            </li>
          </ul>

          <div class="tab-content">

            <!-- TAB ABONOS -->
            <div class="tab-pane fade" id="abonos">

              <!-- ABONOS -->
              <div class="mb-5">

                <!-- ABONOS DEPORTIVOS -->
                <div class="mb-4">
                  <div class="d-flex justify-content-between align-items-center mb-2">
                    <h5 class="fw-semibold text-success">
                      <i class="bi bi-ticket-perforated me-2"></i>{{ t.sportsSubscription }}
                    </h5>

                    <router-link to="/crear/abono/deportivo" class="btn btn-primary rounded-pill">
                      <i class="bi bi-plus-lg me-1"></i> {{ t.newSportSubscription }}
                    </router-link>
                  </div>

                  <div class="list-group list-group-flush">
                    <div v-for="abono in abonosDeportivos" :key="abono.id"
                      class="list-group-item rounded-3 mb-2 shadow-sm d-flex justify-content-between align-items-center"
                      @click="abonoDetail(abono.id, 'deportivo')">
                      <div class="fw-medium text-primary">
                        {{ abono.nombre }}
                      </div>
                    </div>
                  </div>
                </div>

                <!-- ABONOS VERANO -->
                <div class="mb-4">
                  <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5 class="fw-semibold text-success">
                      <i class="bi bi-ticket-perforated me-2"></i>{{ t.summerSubscription }}
                    </h5>

                    <router-link to="/crear/abono/verano" class="btn btn-primary rounded-pill">
                      <i class="bi bi-plus-lg me-1"></i> {{ t.newSummerSubscription }}
                    </router-link>
                  </div>

                  <div class="list-group list-group-flush">
                    <div v-for="abono in abonosVerano" :key="abono.id"
                      class="list-group-item rounded-3 mb-2 shadow-sm d-flex justify-content-between align-items-center"
                      @click="abonoDetail(abono.id, 'verano')">
                      <div class="fw-medium text-primary">
                        {{ abono.nombre }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            </div>

            <!-- TAB BONOS -->
            <div class="tab-pane fade" id="bonos">
              <!-- BONOS -->
              <div>
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="fw-semibold text-success">
                    <i class="bi bi-ticket-perforated me-2"></i>{{ t.bonus }}
                  </h5>

                  <router-link to="/crear/bono" class="btn btn-primary rounded-pill">
                    <i class="bi bi-plus-lg me-1"></i> {{ t.newBonus }}
                  </router-link>
                </div>

                <div class="list-group list-group-flush">
                  <div v-for="bono in bonos" :key="bono.id"
                    class="list-group-item rounded-3 mb-2 shadow-sm d-flex justify-content-between align-items-center"
                    @click="bonoDetail(bono.id)">
                    <div class="fw-medium text-primary">
                      {{ t.bonus }} {{ bono.nombreInstalacion }}
                    </div>
                  </div>
                </div>
              </div>

            </div>

            <!-- TAB TARIFAS -->
            <div class="tab-pane fade show active" id="tarifas">

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
                  <div v-for="tarifa in tarifasInstalacion" :key="tarifa.id"
                    class="list-group-item rounded-3 mb-2 shadow-sm d-flex justify-content-between align-items-center"
                    @click="tarifaInstalacionDetail(tarifa.id)">
                    <div>
                      <div class="fw-medium text-primary">
                        {{ tarifa.titulo }}
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
                  <div v-for="tarifa in tarifasTDA" :key="tarifa.id"
                    class="list-group-item rounded-3 mb-2 shadow-sm d-flex justify-content-between align-items-center"
                    @click="tarifaTDADetail(tarifa.id)">
                    <div>
                      <div class="fw-medium text-primary">
                        {{ tarifa.titulo }}
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
                  <div v-for="tarifa in tarifasActividadComun" :key="tarifa.id"
                    class="list-group-item rounded-3 mb-2 shadow-sm" @click="tarifaActividadComunDetail(tarifa.id)">
                    <div class="fw-medium text-primary">
                      {{ tarifa.titulo }}
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
                  <div v-for="tarifa in tarifasGrupoReducido" :key="tarifa.id"
                    class="list-group-item rounded-3 mb-2 shadow-sm" @click="tarifaGrupoReducidoDetail(tarifa.id)">
                    <div class="fw-medium text-primary">
                      {{ tarifa.titulo }}
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
                  <div v-for="tarifa in tarifasFisioterapia" :key="tarifa.id"
                    class="list-group-item rounded-3 mb-2 shadow-sm" @click="tarifaFisioterapiaDetail(tarifa.id)">
                    <div class="fw-medium text-primary">
                      {{ tarifa.titulo }}
                    </div>
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
import { ref, inject, type Ref, onMounted } from "vue"
import { useRouter } from "vue-router"

import { getTarifas } from "@/services/gestionService"

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"
import { getAbonos, getBonos } from "@/services/abonoBonoService"

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();

const abonosDeportivos = ref<any[]>([]);
const abonosVerano = ref<any[]>([]);
const bonos = ref<any[]>([]);
const tarifasInstalacion = ref<any[]>([]);
const tarifasTDA = ref<any[]>([]);
const tarifasActividadComun = ref<any[]>([]);
const tarifasGrupoReducido = ref<any[]>([]);
const tarifasFisioterapia = ref<any[]>([]);


const abonoDetail = (id: number, tipo: string) => {
  if (tipo === "deportivo") {
    router.push({
      name: "editar-abono-deportivo",
      params: { id }
    })
  } else {
    router.push({
      name: "editar-abono-verano",
      params: { id }
    })
  }
};

const bonoDetail = (id: number) => {
  router.push({
    name: "editar-bono",
    params: { id }
  })
};

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
    name: "editar-tarifa-comun",
    params: { id }
  })
};

const tarifaGrupoReducidoDetail = (id: number) => {
  router.push({
    name: "editar-tarifa-grupos",
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
    const abonos = await getAbonos();
    bonos.value = await getBonos();

    abonosDeportivos.value = abonos.abonosDeportivos
    abonosVerano.value = abonos.abonosVerano

    tarifasInstalacion.value = data.tarifasInstalacion
    tarifasTDA.value = data.tarifasTDA
    tarifasActividadComun.value = data.tarifasActividadComun
    tarifasGrupoReducido.value = data.tarifasGrupoReducido
    tarifasFisioterapia.value = data.tarifasFisioterapia
  } catch (e) {
    console.log("Error al obtener las tarifas, bonos o abonos", e);
  }
});
</script>
