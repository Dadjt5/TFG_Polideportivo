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
          <div class="col-md-4" v-for="b in bonos" :key="b.id">
            <div class="card h-100 shadow-sm rounded-4">
              <div class="card-body">
                <p v-if="b.instalacion!=''">
                  <strong>{{ t.facility }}:</strong> {{ b.instalacion }}
                </p>
                <p v-else>
                  <strong>{{ t.sport }}:</strong> {{ b.deporte }}
                </p>
                <p><strong>{{ t.uses }}:</strong> {{ b.numeroUsos }}</p>
                <p><strong>{{ t.validity }}:</strong> {{ b.validez }}</p>
                <p><strong>{{ t.price }}:</strong> {{ b.precio }}€</p>
                <p v-if="b.descripcionPrecio!=''">{{ b.descripcionPrecio }}</p>
              </div>
              <div class="card-footer bg-transparent border-0">
                <button class="btn btn-success w-100 rounded-pill">
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
          <div class="col-md-6" v-for="ab in abonos" :key="ab.id">
            <div class="card h-100 shadow-sm rounded-4 p-2">
              <div class="card-body">
                <h3 class="h5 fw-semibold mb-3">
                    <i class="bi bi-info-circle text-primary me-2 fs-4"></i>
                    {{ ab.name }}
                </h3>
                <ul class="mb-4">
                  <li v-for="(b, i) in ab.benefits" :key="i">{{ b }}</li>
                  <li>{{ ab.duracion }}</li>
                </ul>
              </div>
              <div class="card-footer bg-transparent border-0">
                <button class="btn btn-success w-100 rounded-pill py-2">
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
import { ref, computed, onMounted, inject, type Ref } from 'vue'

/* Importamos los metodos con los que obtener los bonos y abonos del backend */
import { getAbonos, getBonos } from "@/services/abonoBonoService"

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);

const abonos = computed(() => [
  {
    id: 1,
    name: t.value.sportsSubscription,
    duracion: '1 mes, 4 meses o 12 meses',
    benefits: [
      t.value.unlimitedPool,
      t.value.unlimitedGym,
      t.value.activityDiscount,
      t.value.facilityDiscount
    ]
  },
  {
    id: 2,
    name: t.value.summerSubscription,
    duracion: '12 meses',
    benefits: [t.value.summerPool, t.value.cheaper]
  }
])

const abono = ref({
  id: 0,
  nombre: "",
  tipoActividad: "",
  plazasMaximas: 0,
  plazasReservadas: 0,
  edadMinima: 0,
  año: 0,
  numeroCreditos: 0
});

const bonoBase = {
  id: 0,
  instalacion: '',
  deporte: '',
  numeroUsos: 0,
  validez: 0,
  precio: 0,
  descripcionPrecio: ''
}

type Bono = typeof bonoBase
const bonos = ref<Bono[]>([])

onMounted(async () => {
  try {
    //const responseAbonos = await getAbonos();
    const responseBonos = await getBonos() as Array<{
      id: number
      validez: number
      usos: number
      precioFinal: number
      textoPrecio: string
      nombreInstalacion: string | null
      nombreDeporte: string | null
      tipoBono: string
    }>

    bonos.value = responseBonos.map(b => ({
      id: b.id,
      instalacion: b.nombreInstalacion ?? '',
      deporte: b.nombreDeporte ?? '',
      numeroUsos: b.usos,
      validez: b.validez,
      precio: b.precioFinal,
      descripcionPrecio: b.textoPrecio
    }))
  } catch(e) {
    console.log("Error al obtener los abonos o los bonos", e)
  }
})
</script>
