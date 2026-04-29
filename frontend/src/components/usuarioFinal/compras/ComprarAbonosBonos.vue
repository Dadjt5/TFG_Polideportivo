<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container py-5">

      <!-- TITULO PRINCIPAL -->
      <h1 class="text-center fw-bold mb-5 text-primary" style="text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">
        <i class="bi bi-ticket-perforated me-2 fs-1"></i>
        {{ t.ticketsTitle }}
      </h1>

      <!-- NAV TABS PRINCIPALES -->
      <ul class="nav nav-tabs mb-4 justify-content-center" id="ticketsTab" role="tablist">
        <li class="nav-item" role="presentation">
          <button class="nav-link active" id="bonos-tab" data-bs-toggle="tab" data-bs-target="#bonos" type="button"
            role="tab">
            <i class="bi bi-gift me-2"></i>
            {{ t.bonus }}
          </button>
        </li>

        <li class="nav-item" role="presentation">
          <button class="nav-link" id="abonos-tab" data-bs-toggle="tab" data-bs-target="#abonos" type="button"
            role="tab">
            <i class="bi bi-card-list me-2"></i>
            {{ t.subscription }}
          </button>
        </li>
      </ul>

      <div class="tab-content" id="ticketsTabContent">

        <!-- ================= BONOS ================= -->
        <div class="tab-pane fade show active" id="bonos" role="tabpanel">
          <div class="row g-4">
            <div class="col-md-4" v-for="b in bonos" :key="b.id">
              <div class="card h-100 shadow-sm rounded-4 border-0 card-hover"
                style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(8px);">
                <div class="card-body">
                  <p><strong>{{ t.facility }}:</strong> {{ b.nombreInstalacion }}</p>
                  <p><strong>{{ t.uses }}:</strong> {{ b.usos }}</p>
                  <p><strong>{{ t.validity }}:</strong> {{ b.validez }}</p>
                  <p><strong>{{ t.price }}:</strong> {{ b.precioFinal }}€</p>
                  <p v-if="b.textoPrecio != ''">{{ b.textoPrecio }}</p>
                </div>
                <div class="card-footer bg-transparent border-0">
                  <div v-if="mostrarMensaje" class="text-center mb-3 mt-3">
                    <div class="alert" :class="tipoMensaje === 'success' ? 'alert-success' : 'alert-danger'">
                      {{ mensaje }}
                    </div>
                  </div>
                  <button class="btn btn-success w-100 rounded-pill" @click="nuevoBono(b.id)">
                    {{ t.buy }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ================= ABONOS ================= -->
        <div class="tab-pane fade" id="abonos" role="tabpanel">

          <!-- SUBTABS ABONOS -->
          <ul class="nav nav-pills mb-4 justify-content-center">
            <li class="nav-item">
              <button class="nav-link active" data-bs-toggle="pill" data-bs-target="#deportivos" type="button">
                <i class="bi bi-activity me-2"></i>
                {{ t.sportsSubscription }}
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link" data-bs-toggle="pill" data-bs-target="#verano" type="button">
                <i class="bi bi-sun me-2"></i>
                {{ t.summerSubscription }}
              </button>
            </li>
          </ul>

          <div class="tab-content">

            <!-- ===== ABONOS DEPORTIVOS ===== -->
            <div class="tab-pane fade show active" id="deportivos">

              <!-- BENEFICIOS ABONO DEPORTIVO -->
              <div class="card border-0 shadow-sm rounded-4 mb-4 bg-primary bg-opacity-10">
                <div class="card-body py-3 d-flex flex-wrap gap-3">
                  <span class="badge bg-white text-primary px-3 py-2 rounded-pill shadow-sm">
                    <i class="bi bi-water me-2"></i>
                    {{ t.unlimitedPool }}
                  </span>
                  <span class="badge bg-white text-primary px-3 py-2 rounded-pill shadow-sm">
                    <i class="bi bi-lightning-charge me-2"></i>
                    {{ t.unlimitedGym }}
                  </span>
                  <span class="badge bg-white text-primary px-3 py-2 rounded-pill shadow-sm">
                    <i class="bi bi-lightning-charge me-2"></i>
                    {{ t.advantagesWithPrices }}
                  </span>
                </div>
              </div>

              <div class="row g-4">
                <div class="col-md-6 col-lg-4" v-for="ab in abonos.abonosDeportivos" :key="'dep-' + ab.id">
                  <div class="card h-100 border-0 shadow rounded-4 p-3 card-hover">
                    <div class="card-body d-flex flex-column">
                      <h5 class="fw-bold mb-3 text-primary">{{ ab.nombre }}</h5>
                      <ul class="list-unstyled small mb-3 flex-grow-1">
                        <li class="mb-2">{{ t.months }}: <strong>{{ ab.meses }}</strong></li>
                        <li class="mb-2">{{ t.firstActivityDiscount }}: <strong>{{ ab.descuentoPrimeraActividad
                            }}%</strong></li>
                        <li class="mb-2">{{ t.otherActivitiesDiscount }}: <strong>{{ ab.descuentoRestoActividades
                            }}%</strong></li>
                        <li>{{ t.outdoorDiscount }}: <strong>{{ ab.descuentoActividadesExteriores }}%</strong></li>
                        <li>{{ t.rentDiscount }}: <strong>{{ ab.descuentoAlquileres }}%</strong></li>
                      </ul>
                      <div class="border-top pt-3 mt-auto">
                        <p class="mb-1"><strong>{{ t.monthlyPrice }}:</strong> {{ ab.precioTotalMensual }}€</p>
                        <p class="mb-1"><strong>{{ t.singlePaymentUAM }}:</strong> {{ ab.precioPagoUnicoUAM }}€</p>
                        <p class="mb-0"><strong>{{ t.familyPrice }}:</strong> {{ ab.precioFamiliar }}€</p>
                      </div>
                    </div>
                    <div class="card-footer bg-transparent border-0 pt-0">
                      <button class="btn btn-primary w-100 rounded-pill" @click="nuevoAbono(ab.id, 'abono_deportivo')">
                        {{ t.buy }}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- ===== ABONOS VERANO ===== -->
            <div class="tab-pane fade" id="verano">

              <div class="card border-0 shadow-sm rounded-4 mb-4 bg-primary bg-opacity-10">
                <div class="card-body py-3 d-flex flex-wrap gap-3">
                  <span class="badge bg-white text-primary px-3 py-2 rounded-pill shadow-sm">
                    <i class="bi bi-water me-2"></i>
                    {{ t.unlimitedPool }}
                  </span>
                  <span class="badge bg-white text-primary px-3 py-2 rounded-pill shadow-sm">
                    <i class="bi bi-lightning-charge me-2"></i>
                    {{ t.advantagesWithPrices }}
                  </span>
                </div>
              </div>

              <div class="row g-4">
                <div class="col-md-6 col-lg-4" v-for="ab in abonos.abonosVerano" :key="'ver-' + ab.id">
                  <div class="card h-100 border-0 shadow rounded-4 p-3 card-hover">
                    <div class="card-body d-flex flex-column">
                      <h5 class="fw-bold mb-3 text-warning">{{ ab.nombre }}</h5>
                      <ul class="list-unstyled small flex-grow-1">
                        <li class="mb-2"><strong>{{ t.priceTDA }}:</strong> {{ ab.precioTDA }}€</li>
                        <li class="mb-2"><strong>{{ t.priceUAM }}:</strong> {{ ab.precioUAM }}€</li>
                        <li><strong>{{ t.priceOthers }}:</strong> {{ ab.precioOtros }}€</li>
                      </ul>
                    </div>
                    <div class="card-footer bg-transparent border-0 pt-0">
                      <button class="btn btn-warning w-100 rounded-pill text-white"
                        @click="nuevoAbono(ab.id, 'abono_verano')">
                        {{ t.buy }}
                      </button>
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
import { ref, onMounted, inject, type Ref } from 'vue'
import { useRouter } from 'vue-router'

/* Importamos los metodos con los que obtener los bonos y abonos del backend */
import { getAbonos, getBonos } from "@/services/abonoBonoService"

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";
import { comprarBono } from '@/services/reservaPagoService';

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();

const mensaje = ref('')
const tipoMensaje = ref<'success' | 'error' | ''>('')
const mostrarMensaje = ref(false)

const abonos = ref({
  abonosDeportivos: [] as {
    id: 0,
    nombre: "",
    meses: 0,
    descuentoPrimeraActividad: 0.0,
    descuentoRestoActividades: 0.0,
    descuentoActividadesExteriores: 0.0,
    descuentoAlquileres: 0.0,
    precioTotalMensual: 0.0,
    precioPagoUnicoUAM: 0.0,
    precioFamiliar: 0.0,
    precioTotalMensualOtros: 0.0,
    precioPagoUnicoOtros: 0.0
  }[],
  abonosVerano: [] as {
    id: 0,
    nombre: "",
    precioTDA: 0.0,
    precioUAM: 0.0,
    precioOtros: 0.0
  }[]
});

const bonos = ref<any[]>([])

function lanzarMensaje(texto: string, tipo: 'success' | 'error') {
  mensaje.value = texto
  tipoMensaje.value = tipo
  mostrarMensaje.value = true

  setTimeout(() => {
    mostrarMensaje.value = false
  }, 5000)
}


const nuevoAbono = async (id: number, tipoAbono: string) => {
  router.push({
    name: 'configurar-abono',
    params: { "id": id, "tipo": tipoAbono }
  })
}

const nuevoBono = async (id: number) => {
  try {
    const response = await comprarBono(id)

    const idPago = response.idPago

    router.push({
      name: 'pasarela-pago',
      params: { tipo: "comprar_bono", id: idPago }
    })
  } catch (e) {
    lanzarMensaje(t.value.noBonusBuy, "error")
    console.error("Error al comprar el bono", e)
  }
}

onMounted(async () => {
  try {
    abonos.value = await getAbonos();
    bonos.value = await getBonos();
  } catch (e) {
    console.log("Error al obtener los abonos o los bonos", e)
  }
})
</script>

<style scoped>
.hover-shadow {
  transition: all 0.3s ease;
}

.hover-shadow:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.section-header {
  font-size: 1.4rem;
}
</style>