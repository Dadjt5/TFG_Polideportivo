<template>
  <div class="min-vh-100 bg-light">
    <main class="container py-4">
      <h1 class="text-center fw-bold mb-4">
        <i class="bi bi-ticket-perforated text-primary me-2 fs-1"></i>
        {{ t.purchase }}
      </h1>

      <section class="mb-5">
        <h2 class="fw-semibold mb-3">{{ t.bonus }}</h2>

        <div class="row g-4">
          <div class="col-md-4" v-for="b in bonuses" :key="b.id">
            <div class="card h-100 shadow-sm rounded-4">
              <div class="card-body">
                <p><strong>{{ b.sport }}</strong></p>
                <p><strong>{{ t.uses }}:</strong> {{ b.uses }}</p>
                <p><strong>{{ t.validity }}:</strong> {{ b.validity }} año</p>
                <p><strong>Precio:</strong> {{ b.price }}€</p>
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
import { ref, computed, onMounted } from 'vue'

const language = ref('es')

const translations = {
  es: {
    home: 'Inicio',
    forum: 'Foro',
    contact: 'Contacto',
    faq: 'FAQ',
    logout: 'Logout',
    purchase: 'Compra de bonos y abonos',
    bonus: 'Bonos',
    subscription: 'Abonos',
    uses: 'Número de usos',
    validity: 'Años de validez',
    buy: 'Comprar',
    sports: 'Abono deportivo',
    summer: 'Abono de verano',
    unlimitedPool: 'Acceso ilimitado a la piscina',
    unlimitedGym: 'Acceso ilimitado a la sala de musculación',
    activityDiscount: 'Descuento del 30% en actividades',
    facilityDiscount: 'Reducción de precios en reserva de instalaciones',
    summerPool: 'Acceso a la piscina de verano',
    cheaper: 'Más barato que el abono deportivo'
  },
  en: {
    home: 'Home',
    forum: 'Forum',
    contact: 'Contact',
    faq: 'FAQ',
    logout: 'Logout',
    purchase: 'Purchase Bonuses and Subscriptions',
    bonus: 'Bonuses',
    subscription: 'Subscriptions',
    uses: 'Number of uses',
    validity: 'Years of validity',
    buy: 'Buy',
    sports: 'Sports subscription',
    summer: 'Summer subscription'
  }
}

const t = computed(() => translations[language.value])

const toggleLanguage = () => {
  language.value = language.value === 'es' ? 'en' : 'es'
}

const bonuses = ref([
  { id: 1, sport: 'Instalación: Piscina', uses: 10, validity: 1, price: 40 },
  { id: 2, sport: 'Instalación: Sala musculación', uses: 20, validity: 1, price: 40 },
  { id: 3, sport: 'Deporte: Tenis', uses: 15, validity: 1, price: 30 }
])

const abonos = computed(() => [
  {
    id: 1,
    name: t.value.sports,
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
    name: t.value.summer,
    duracion: '12 meses',
    benefits: [t.value.summerPool, t.value.cheaper]
  }
])

interface Abonos {
  actividades: any[] | null
  instalaciones: any[] | null
}

const resultados = ref<Abonos>({
  actividades: null,
  instalaciones: null
})


const abono = ref({
  id: 0,
  nombre: "",
  tipoActividad: "",
  plazasMaximas: 0,
  plazasReservadas: 0,
  edadMinima: 0,
  año: 0,
  numeroCreditos: 0,
  nivel: "",
  material: "",
  exterior: false,
  tipoReserva: "",
  terreno: "",
  periodo: "",
  estado: "",
  dias: ""
});

onMounted(async () => {
  try {
    const abonos = await getAbonos();
    const bonos = await getBonos();

    data.value = {
      nombre: user.nombre,
      apellidos: user.apellidos,
      email: userStore.user?.email || '',
      rol: user.rol
    };
  } catch(e) {
    console.log("Error al obtener el usuario", e)
  }
})
</script>
