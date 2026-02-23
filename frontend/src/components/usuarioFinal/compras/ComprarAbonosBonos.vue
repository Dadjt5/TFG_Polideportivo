<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-4">
      <h1 class="text-center fw-bold mb-4">
        <i class="bi bi-ticket-perforated text-primary me-2 fs-1"></i>
        {{ t.ticketsTitle }}
      </h1>

      <section class="mb-5">
        <h2 class="fw-semibold mb-3">{{ t.bonus }}</h2>

        <div class="row g-4">
          <div class="col-md-4" v-for="b in bonos.bonos" :key="b.id">
            <div class="card h-100 shadow-sm rounded-4">
              <div class="card-body">
                <p v-if="b.instalacion != ''">
                  <strong>{{ t.facility }}:</strong> {{ b.instalacion }}
                </p>
                <p v-else>
                  <strong>{{ t.sport }}:</strong> {{ b.deporte }}
                </p>
                <p><strong>{{ t.uses }}:</strong> {{ b.numeroUsos }}</p>
                <p><strong>{{ t.validity }}:</strong> {{ b.validez }}</p>
                <p><strong>{{ t.price }}:</strong> {{ b.precio }}€</p>
                <p v-if="b.descripcionPrecio != ''">{{ b.descripcionPrecio }}</p>
              </div>
              <div class="card-footer bg-transparent border-0">
                <button class="btn btn-success w-100 rounded-pill" @click="nuevoBono(b.id)">
                  {{ t.buy }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section>
        <h2 class="fw-semibold mb-3">{{ t.subscription }}</h2>

        <div class="row g-4">

          <!-- ABONOS DEPORTIVOS -->
          <div class="col-12">
            <h4 class="fw-semibold mb-3 text-primary">
              <i class="bi bi-activity me-2"></i>
              {{ t.sportsSubscription }}
            </h4>
          </div>

          <ul class="small text-muted mb-3">
            <li>{{ t.unlimitedPool }}</li>
            <li>{{ t.unlimitedGym }}</li>
          </ul>

          <div class="col-md-6 col-lg-4" v-for="ab in abonos.abonosDeportivos" :key="'dep-' + ab.id">
            <div class="card h-100 shadow-sm rounded-4 p-3 border-primary border-opacity-25">
              <div class="card-body">

                <h5 class="fw-bold mb-3">
                  {{ ab.nombre }}
                </h5>

                <ul class="mb-3 small">
                  <li>{{ t.months }}: {{ ab.meses }}</li>
                  <li>{{ t.firstActivityDiscount }}: {{ ab.descuentoPrimeraActividad }}%</li>
                  <li>{{ t.otherActivitiesDiscount }}: {{ ab.descuentoRestoActividades }}%</li>
                  <li>{{ t.outdoorDiscount }}: {{ ab.descuentoActividadesExteriores }}%</li>
                </ul>

                <div class="mb-2">
                  <p class="mb-1">
                    <strong>{{ t.monthlyPrice }}:</strong> {{ ab.precioTotalMensual }}€
                  </p>
                  <p class="mb-1">
                    <strong>{{ t.singlePaymentUAM }}:</strong> {{ ab.precioPagoUnicoUAM }}€
                  </p>
                  <p class="mb-1">
                    <strong>{{ t.familyPrice }}:</strong> {{ ab.precioFamiliar }}€
                  </p>
                </div>

              </div>

              <div class="card-footer bg-transparent border-0">
                <button class="btn btn-primary w-100 rounded-pill" @click="nuevoAbono(ab.id, 'abono_deportivo')">
                  {{ t.buy }}
                </button>
              </div>
            </div>
          </div>


          <!-- ABONOS DE VERANO -->
          <div class="col-12 mt-5">
            <h4 class="fw-semibold mb-3 text-warning">
              <i class="bi bi-sun me-2"></i>
              {{ t.summerSubscription }}
            </h4>
          </div>

          <ul class="small text-muted mb-3">
            <li>{{ t.summerPool }}</li>
            <li>{{ t.cheaper }}</li>
          </ul>


          <div class="col-md-6 col-lg-4" v-for="ab in abonos.abonosVerano" :key="'ver-' + ab.id">
            <div class="card h-100 shadow-sm rounded-4 p-3 border-warning border-opacity-25">
              <div class="card-body">

                <h5 class="fw-bold mb-3">
                  {{ ab.nombre }}
                </h5>

                <ul class="mb-3 small">
                  <li><strong>{{ t.priceTDA }}:</strong> {{ ab.precioTDA }}€</li>
                  <li><strong>{{ t.priceUAM }}:</strong> {{ ab.precioUAM }}€</li>
                  <li><strong>{{ t.priceOthers }}:</strong> {{ ab.precioOtros }}€</li>
                </ul>

              </div>

              <div class="card-footer bg-transparent border-0">
                <button class="btn btn-warning w-100 rounded-pill text-white"
                  @click="nuevoAbono(ab.id, 'abono_verano')">
                  {{ t.buy }}
                </button>
              </div>
            </div>
          </div>

        </div>
      </section>
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
import { comprarAbono, comprarBono } from '@/services/reservaPagoService';

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const router = useRouter();

const abonos = ref({
  abonosDeportivos: [] as {
    id: 0,
    nombre: "",
    meses: 0,
    descuentoPrimeraActividad: 0.0,
    descuentoRestoActividades: 0.0,
    descuentoActividadesExteriores: 0.0,
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

const bonos = ref({
  bonos: [] as {
    id: 0,
    instalacion: '',
    deporte: '',
    numeroUsos: 0,
    validez: 0,
    precio: 0,
    descripcionPrecio: ''
  }[]
});

const nuevoAbono = async (id: number, tipoAbono: string) => {
  const response = await comprarAbono(id, tipoAbono)

  const idPago = response.data.idPago

  router.push({
    name: 'pasarela-pago',
    params: { tipo: "comprar_abono", id: idPago }
  })
}

const nuevoBono = async (id: number) => {
  const response = await comprarBono(id)

  const idPago = response.data.idPago

  router.push({
    name: 'pasarela-pago',
    params: { tipo: "comprar_bono", id: idPago }
  })
}

onMounted(async () => {
  try {
    const abonosResponse = await getAbonos();
    const bonosResponse = await getBonos();

    abonos.value = abonosResponse;
    bonos.value = bonosResponse;

  } catch (e) {
    console.log("Error al obtener los abonos o los bonos", e)
  }
})
</script>
