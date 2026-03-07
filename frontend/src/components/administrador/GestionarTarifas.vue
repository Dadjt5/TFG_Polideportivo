<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container py-5" style="max-width: 1100px">
      <h1 class="fw-bold text-primary mb-5 text-center">
        <i class="bi bi-cash-stack me-2"></i>{{ t.manageRates }}
      </h1>

      <div class="card shadow-lg border-0 rounded-4" style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">
        <div class="card-body p-4">

          <!-- TABS -->
          <ul class="nav nav-tabs mb-4">
            <li class="nav-item">
              <button class="nav-link" :class="{ active: tab==='tarifas' }" @click="tab='tarifas'">
                <i class="bi bi-currency-dollar me-1"></i>{{ t.manageRates }}
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link" :class="{ active: tab==='bonos' }" @click="tab='bonos'">
                <i class="bi bi-ticket-perforated me-1"></i>{{ t.bonus }}
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link" :class="{ active: tab==='abonos' }" @click="tab='abonos'">
                <i class="bi bi-ticket-perforated me-1"></i>{{ t.subscription }}
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link" :class="{ active: tab==='descuentos' }" @click="tab='descuentos'">
                <i class="bi bi-percent me-1"></i>{{ t.discounts }}
              </button>
            </li>
          </ul>

          <div class="tab-content">

            <!-- TARIFAS INSTALACIÓN -->
            <div v-if="tab==='tarifas'">
              <!-- TARIFAS INSTALACIÓN -->
              <div class="mb-5">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="fw-semibold text-success">
                    <i class="bi bi-geo-alt me-2"></i>{{ t.facilityTariff }}
                  </h5>
                  <router-link to="/crear/tarifa/instalacion" class="btn btn-primary rounded-pill shadow-sm">
                    <i class="bi bi-plus-lg me-1"></i> {{ t.newTariff }}
                  </router-link>
                </div>
                <div class="list-group list-group-flush">
                  <div v-for="tarifa in tarifasInstalacion" :key="tarifa.id"
                       class="list-group-item rounded-3 mb-2 shadow-sm border-0"
                       style="background-color: rgba(255,255,255,0.9); cursor:pointer;"
                       @click="tarifaInstalacionDetail(tarifa.id)">
                    <div class="fw-medium text-primary">{{ tarifa.titulo }}</div>
                  </div>
                </div>
              </div>

              <!-- TARIFAS TDA -->
              <div class="mb-5">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="fw-semibold text-success">
                    <i class="bi bi-geo-alt me-2"></i>{{ t.TDATariff }}
                  </h5>
                  <router-link to="/crear/tarifa/TDA" class="btn btn-primary rounded-pill shadow-sm">
                    <i class="bi bi-plus-lg me-1"></i> {{ t.newTariff }}
                  </router-link>
                </div>
                <div class="list-group list-group-flush">
                  <div v-for="tarifa in tarifasTDA" :key="tarifa.id"
                       class="list-group-item rounded-3 mb-2 shadow-sm border-0"
                       style="background-color: rgba(255,255,255,0.9); cursor:pointer;"
                       @click="tarifaTDADetail(tarifa.id)">
                    <div class="fw-medium text-primary">{{ tarifa.titulo }}</div>
                  </div>
                </div>
              </div>

              <!-- TARIFAS ACTIVIDAD COMÚN -->
              <div class="mb-5">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="fw-semibold text-success">
                    <i class="bi bi-people me-2"></i>{{ t.commonActivityTariff }}
                  </h5>
                  <router-link to="/crear/tarifa/comun" class="btn btn-primary rounded-pill shadow-sm">
                    <i class="bi bi-plus-lg me-1"></i> {{ t.newTariff }}
                  </router-link>
                </div>
                <div class="list-group list-group-flush">
                  <div v-for="tarifa in tarifasActividadComun" :key="tarifa.id"
                       class="list-group-item rounded-3 mb-2 shadow-sm border-0"
                       style="background-color: rgba(255,255,255,0.9); cursor:pointer;"
                       @click="tarifaActividadComunDetail(tarifa.id)">
                    <div class="fw-medium text-primary">{{ tarifa.titulo }}</div>
                  </div>
                </div>
              </div>

              <!-- GRUPOS REDUCIDOS -->
              <div class="mb-5">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="fw-semibold text-success">
                    <i class="bi bi-person-badge me-2"></i>{{ t.smallGroupsTariff }}
                  </h5>
                  <router-link to="/crear/tarifa/grupos" class="btn btn-primary rounded-pill shadow-sm">
                    <i class="bi bi-plus-lg me-1"></i> {{ t.newTariff }}
                  </router-link>
                </div>
                <div class="list-group list-group-flush">
                  <div v-for="tarifa in tarifasGrupoReducido" :key="tarifa.id"
                       class="list-group-item rounded-3 mb-2 shadow-sm border-0"
                       style="background-color: rgba(255,255,255,0.9); cursor:pointer;"
                       @click="tarifaGrupoReducidoDetail(tarifa.id)">
                    <div class="fw-medium text-primary">{{ tarifa.titulo }}</div>
                  </div>
                </div>
              </div>

              <!-- FISIOTERAPIA -->
              <div>
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="fw-semibold text-success">
                    <i class="bi bi-heart-pulse me-2"></i>{{ t.physiotherapyTariff }}
                  </h5>
                  <router-link to="/crear/tarifa/fisioterapia" class="btn btn-primary rounded-pill shadow-sm">
                    <i class="bi bi-plus-lg me-1"></i> {{ t.newTariff }}
                  </router-link>
                </div>
                <div class="list-group list-group-flush">
                  <div v-for="tarifa in tarifasFisioterapia" :key="tarifa.id"
                       class="list-group-item rounded-3 mb-2 shadow-sm border-0"
                       style="background-color: rgba(255,255,255,0.9); cursor:pointer;"
                       @click="tarifaFisioterapiaDetail(tarifa.id)">
                    <div class="fw-medium text-primary">{{ tarifa.titulo }}</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- TAB BONOS -->
            <div v-if="tab==='bonos'">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="fw-semibold text-success"><i class="bi bi-ticket-perforated me-2"></i>{{ t.bonus }}</h5>
                <router-link to="/crear/bono" class="btn btn-primary rounded-pill shadow-sm"><i class="bi bi-plus-lg me-1"></i> {{ t.newBonus }}</router-link>
              </div>
              <div class="list-group list-group-flush">
                <div v-for="bono in bonos" :key="bono.id"
                     class="list-group-item rounded-3 mb-2 shadow-sm border-0"
                     style="background-color: rgba(255,255,255,0.9); cursor:pointer;"
                     @click="bonoDetail(bono.id)">
                  <div class="fw-medium text-primary">{{ t.bonus }} {{ bono.nombreInstalacion }}</div>
                </div>
              </div>
            </div>

            <!-- TAB ABONOS -->
            <div v-if="tab==='abonos'">
              <!-- ABONOS DEPORTIVOS -->
              <div class="mb-4">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <h5 class="fw-semibold text-success"><i class="bi bi-ticket-perforated me-2"></i>{{ t.sportsSubscription }}</h5>
                  <router-link to="/crear/abono/deportivo" class="btn btn-primary rounded-pill shadow-sm"><i class="bi bi-plus-lg me-1"></i> {{ t.newSportSubscription }}</router-link>
                </div>
                <div class="list-group list-group-flush">
                  <div v-for="abono in abonosDeportivos" :key="abono.id"
                       class="list-group-item rounded-3 mb-2 shadow-sm border-0"
                       style="background-color: rgba(255,255,255,0.9); cursor:pointer;"
                       @click="abonoDetail(abono.id,'deportivo')">
                    <div class="fw-medium text-primary">{{ abono.nombre }}</div>
                  </div>
                </div>
              </div>

              <!-- ABONOS VERANO -->
              <div class="mb-4">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="fw-semibold text-success"><i class="bi bi-ticket-perforated me-2"></i>{{ t.summerSubscription }}</h5>
                  <router-link to="/crear/abono/verano" class="btn btn-primary rounded-pill shadow-sm"><i class="bi bi-plus-lg me-1"></i> {{ t.newSummerSubscription }}</router-link>
                </div>
                <div class="list-group list-group-flush">
                  <div v-for="abono in abonosVerano" :key="abono.id"
                       class="list-group-item rounded-3 mb-2 shadow-sm border-0"
                       style="background-color: rgba(255,255,255,0.9); cursor:pointer;"
                       @click="abonoDetail(abono.id,'verano')">
                    <div class="fw-medium text-primary">{{ abono.nombre }}</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- TAB DESCUENTOS -->
            <div v-if="tab==='descuentos'">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="fw-semibold text-success"><i class="bi bi-percent me-2"></i>{{ t.discounts }}</h5>
                <router-link to="/crear/descuento" class="btn btn-primary rounded-pill shadow-sm"><i class="bi bi-plus-lg me-1"></i> {{ t.newDiscount }}</router-link>
              </div>
              <div class="list-group list-group-flush">
                <div v-for="descuento in descuentos" :key="descuento.id"
                     class="list-group-item rounded-3 mb-2 shadow-sm border-0"
                     style="background-color: rgba(255,255,255,0.9); cursor:pointer;"
                     @click="descuentoDetail(descuento.id)">
                  <div class="fw-medium text-primary">{{ descuento.nombre }}</div>
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
import { getAbonos, getBonos, getDescuentos } from "@/services/abonoBonoService"

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();
const tab = ref("tarifas")

const abonosDeportivos = ref<any[]>([]);
const abonosVerano = ref<any[]>([]);
const bonos = ref<any[]>([]);
const descuentos = ref<any[]>([]);
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

const descuentoDetail = (id: number) => {
  router.push({
    name: "editar-descuento",
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
    descuentos.value = await getDescuentos();

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
