<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid px-5 py-4">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="fw-bold m-0 text-primary">
          <i class="bi bi-bar-chart-line-fill me-2"></i>
          {{ t.generalStats }}
        </h2>
      </div>

      <!-- FILTROS -->
      <div class="d-flex flex-wrap gap-3 mb-4 align-items-end">

        <div>
          <label class="form-label fw-semibold">{{ t.month }}</label>
          <input type="month" v-model="filtroMes" class="form-control">
        </div>

        <div>
          <label class="form-label fw-semibold">{{ t.activity }}</label>
          <select v-model="actividadSeleccionada" class="form-select">
            <option value="">{{ t.all }}</option>
            <option v-for="act in actividades" :key="act.id" :value="act.id">
              {{ act.nombre }}
            </option>
          </select>
        </div>

        <div class="d-flex gap-2">
          <button class="btn btn-primary mt-2" @click="cargarDatos">
            <i class="bi bi-funnel me-1"></i>
            {{ t.filter }}
          </button>

          <button class="btn btn-outline-secondary mt-2" @click="resetFiltros">
            <i class="bi bi-x-circle me-1"></i>
            {{ t.cleanFilters }}
          </button>
        </div>

      </div>

      <!-- KPIs -->
      <div class="row g-4 mb-4">
        <div class="col-md-4 col-xl-2" v-for="kpi in kpis" :key="kpi.key">
          <div class="card shadow-lg border-0 rounded-4 h-100 text-center"
            style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">
            <div class="card-body d-flex flex-column justify-content-center">
              <h6 class="text-muted mb-2">{{ kpi.title }}</h6>
              <h3 class="fw-bold text-dark">{{ kpi.value }}</h3>
            </div>
          </div>
        </div>
      </div>

      <!-- GRÁFICOS -->
      <div class="row g-4 mb-4">
        <div class="col-lg-6">
          <div class="card shadow-lg border-0 rounded-4">
            <div class="card-body">
              <h5 class="fw-bold mb-3 text-primary">
                <i class="bi bi-graph-up-arrow me-2"></i>
                {{ t.activityReservations12Months }}
              </h5>
              <div class="chart-placeholder">
                <canvas ref="chartReservasRef"></canvas>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-6">
          <div class="card shadow-lg border-0 rounded-4">
            <div class="card-body">
              <h5 class="fw-bold mb-3 text-primary">
                <i class="bi bi-cash-coin me-2"></i>
                {{ t.incomeForType }}
              </h5>

              <div class="chart-placeholder">
                <canvas ref="chartIngresosRef"></canvas>
              </div>

            </div>
          </div>
        </div>

        <div class="col-lg-12">
          <div class="card shadow-lg border-0 rounded-4"
            style="background-color: rgba(255,255,255,0.85); backdrop-filter: blur(10px);">
            <div class="card-body">
              <h5 class="fw-bold mb-3 text-primary">
                <i class="bi bi-people-fill me-2"></i>
                {{ t.activityInscriptions }}
              </h5>
              <div class="chart-placeholder">
                <canvas ref="chartInscripcionesRef"></canvas>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- USO PABELLONES -->
      <div class="card shadow-lg border-0 rounded-4">
        <div class="card-body">
          <h5 class="fw-bold mb-3 text-primary">
            <i class="bi bi-building me-2"></i>
            {{ t.pavilionUses }}
          </h5>

          <table class="table">
            <thead>
              <tr>
                <th>{{ t.facility }}</th>
                <th>{{ t.hoursUsed }}</th>
                <th>{{ t.occupancy }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in usoPabellones" :key="p.nombre">
                <td>{{ p.nombre }}</td>
                <td>{{ p.horas }}</td>
                <td>{{ p.ocupacion }}%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { type Ref, ref, onMounted, inject, computed } from 'vue'

import { getEstadisticasAdministrador } from "@/services/administradorService"
import { getActividadesSimples } from '@/services/listadoService'

import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const language = inject<Ref<Language>>('language')!;
const t = useI18n(language);

import {
  Chart,
  LineController,
  LineElement,
  BarElement,
  PointElement,
  LinearScale,
  CategoryScale,
  PieController,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js'

Chart.register(
  LineController,
  LineElement,
  PointElement,
  BarElement,
  LinearScale,
  CategoryScale,
  PieController,
  ArcElement,
  Tooltip,
  Legend
)

const filtroMes = ref(new Date().toISOString().slice(0, 7))
const actividadSeleccionada = ref("")

const chartReservasRef = ref(null)
const chartIngresosRef = ref(null)
const chartInscripcionesRef = ref<HTMLCanvasElement | null>(null)

let chartReservas: any = null
let chartIngresos: any = null
let chartInscripciones: Chart | null = null

const actividades = ref([])
const usoPabellones = ref([])

// DATOS BASE
const kpisData = ref({
  usuarios: 0,
  monitores: 0,
  sesiones: 0,
  inscripciones: 0,
  reservas: 0,
  ingresos: 0
})

// KPIs REACTIVOS
const kpis = computed(() => [
  { key: 'usuarios', title: t.value.users, value: kpisData.value.usuarios },
  { key: 'monitores', title: t.value.monitors, value: kpisData.value.monitores },
  { key: 'sesiones', title: t.value.sessions, value: kpisData.value.sesiones },
  { key: 'inscripciones', title: t.value.inscriptions, value: kpisData.value.inscripciones },
  { key: 'reservas', title: t.value.rents, value: kpisData.value.reservas },
  { key: 'ingresos', title: t.value.income, value: kpisData.value.ingresos + ' €' }
])

const resetFiltros = () => {
  filtroMes.value = new Date().toISOString().slice(0, 7)
  actividadSeleccionada.value = ""
  cargarDatos()
}

const renderCharts = (data: any) => {

  if (chartReservas) chartReservas.destroy()
  if (chartIngresos) chartIngresos.destroy()

  chartReservas = new Chart(chartReservasRef.value, {
    type: 'line',
    data: {
      labels: data.reservas_12_meses.map((r: any) => r.mes),
      datasets: [{
        label: t.value.reservations,
        data: data.reservas_12_meses.map((r: any) => r.total),
        tension: 0.3,
        borderColor: '#2196F3',
        backgroundColor: 'rgba(33, 150, 243, 0.2)',
        fill: true
      }]
    },
    options: { responsive: true }
  })

  chartIngresos = new Chart(chartIngresosRef.value, {
    type: 'pie',
    data: {
      labels: Object.keys(data.ingresos_detallados),
      datasets: [{
        data: Object.values(data.ingresos_detallados),
        backgroundColor: [
          '#4CAF50',
          '#2196F3',
          '#FFC107',
          '#FF5722',
          '#9C27B0'
        ]
      }]
    },
    options: {
    responsive: true,
    plugins: {
      tooltip: {
        callbacks: {
          label: (context) => {
            const value = context.parsed
            const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0)
            const percentage = ((value / total) * 100).toFixed(1)
            return ` ${context.label}: ${value} € (${percentage}%)`
          }
        }
      }
    }
  }
  })
}

const renderInscripciones = (inscripciones: any[]) => {
  if (chartInscripciones) chartInscripciones.destroy()

  chartInscripciones = new Chart(chartInscripcionesRef.value!, {
    type: 'bar',
    data: {
      labels: inscripciones.map(i => i.actividad),
      datasets: [{
        label: t.value.inscriptions,
        data: inscripciones.map(i => i.inscritos),
        backgroundColor: '#4CAF50'
      }]
    },
    options: { responsive: true }
  })
}

const cargarDatos = async () => {
  try {
    const [anio, mes] = filtroMes.value.split("-")

    const data = await getEstadisticasAdministrador(anio, mes, actividadSeleccionada.value)

    kpisData.value = {
      usuarios: data.usuarios,
      monitores: data.monitores,
      sesiones: data.sesiones,
      inscripciones: data.inscripciones,
      reservas: data.reservas_mes,
      ingresos: data.ingresos_mes
    }

    usoPabellones.value = data.uso_pabellones || []

    renderCharts(data)
    renderInscripciones(data.inscripciones_por_actividad || [])

  } catch (e) {
    console.error(e)
  }
}

const cargarActividades = async () => {
  actividades.value = await getActividadesSimples()
}

onMounted(() => {
  cargarActividades()
  cargarDatos()
})
</script>

<style scoped>
.chart-placeholder {
  height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-radius: 1rem;
}
</style>