<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid mt-2 px-5 py-4">

      <!-- CABECERA -->
      <div class="d-flex justify-content-center align-items-center mb-4 mt-3">
        <h2 class="fw-bold m-0 text-primary">{{ t.myStadistics }}</h2>
      </div>

      <!-- KPIs -->
      <div class="row g-4 mb-4 mt-3">

        <div class="col-md-4 col-xl-2" v-for="kpi in kpis" :key="kpi.title">
          <div class="card shadow-sm border-0 rounded-4 h-100">
            <div class="card-body text-center">
              <h6 class="text-muted">{{ kpi.title }}</h6>
              <h3 class="fw-bold">{{ kpi.value }}</h3>
            </div>
          </div>
        </div>

      </div>

      <!-- GRÁFICOS -->
      <div class="row g-4 mb-4">

        <!-- Reservas por mes -->
        <div class="col-lg-6">
          <div class="card shadow-sm border-0 rounded-4">
            <div class="card-body">
              <h5 class="fw-bold mb-3">{{ t.myBookingsByMonth }}</h5>

              <Line
                v-if="reservasChart"
                :data="reservasChart"
                :options="chartOptions"
              />

            </div>
          </div>
        </div>

        <!-- Actividades favoritas -->
        <div class="col-lg-6">
          <div class="card shadow-sm border-0 rounded-4">
            <div class="card-body">
              <h5 class="fw-bold mb-3">{{ t.moreReservedActivities }}</h5>

              <Bar
                v-if="actividadesChart"
                :data="actividadesChart"
                :options="chartOptions"
              />

            </div>
          </div>
        </div>

      </div>

      <!-- RESERVAS POR DIA -->
      <div class="card shadow-sm border-0 rounded-4 mb-4">
        <div class="card-body">

          <h5 class="fw-bold mb-3">{{ t.weeklyDayReservations }}</h5>

          <Bar
            v-if="diasChart"
            :data="diasChart"
            :options="chartOptions"
          />

        </div>
      </div>

      <div class="text-center">
        <button class="btn btn-primary fs-4 mt-4 rounded-pill" @click="volver">
          {{ t.return }}
        </button>
      </div>

    </main>
  </div>
</template>

<script setup lang="ts">

import { inject, type Ref, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { Line, Bar } from 'vue-chartjs'

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement
} from 'chart.js'

import { getEstadisticasUsuarioFinal } from "@/services/administradorService"

import type { Language } from "@/useI18N"
import { useI18n } from "@/useI18N"

const language = inject<Ref<Language>>('language')!
const t = useI18n(language)

const router = useRouter()

const volver = () => {
  router.back()
}

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement
)

const kpis = ref([
  { title: 'Reservas totales', value: 0 },
  { title: 'Reservas este mes', value: 0 },
  { title: 'Cancelaciones', value: 0 },
  { title: 'Dinero gastado', value: '0 €' },
  { title: 'Actividad favorita', value: '-' },
  { title: 'Pabellón favorito', value: '-' }
])

const reservasChart = ref<any>(null)
const actividadesChart = ref<any>(null)
const diasChart = ref<any>(null)

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: false
    }
  }
}

onMounted(async () => {

  try {

    const data = await getEstadisticasUsuarioFinal()

    kpis.value = [
      { title: 'Reservas totales', value: data.reservas_totales },
      { title: 'Reservas este mes', value: data.reservas_mes },
      { title: 'Cancelaciones', value: data.cancelaciones },
      { title: 'Dinero gastado', value: data.dinero_total + " €" },
      { title: 'Actividad favorita', value: data.actividad_favorita },
      { title: 'Pabellón favorito', value: data.pabellon_favorito }
    ]

    reservasChart.value = {
      labels: data.reservas_por_mes.labels,
      datasets: [
        {
          label: "Reservas",
          data: data.reservas_por_mes.data,
          borderColor: "#0d6efd",
          backgroundColor: "rgba(13,110,253,0.2)",
          tension: 0.3
        }
      ]
    }

    actividadesChart.value = {
      labels: data.actividades_usuario.labels,
      datasets: [
        {
          label: "Reservas",
          data: data.actividades_usuario.data,
          backgroundColor: "#198754"
        }
      ]
    }

    diasChart.value = {
      labels: data.reservas_por_dia.labels,
      datasets: [
        {
          label: "Reservas",
          data: data.reservas_por_dia.data,
          backgroundColor: "#ffc107"
        }
      ]
    }

  } catch (e) {
    console.error("Error cargando estadísticas", e)
  }
})
</script>

<style scoped>
.chart-placeholder {
  height: 250px;
}
</style>