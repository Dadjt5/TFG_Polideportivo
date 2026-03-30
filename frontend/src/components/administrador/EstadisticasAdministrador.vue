<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #ffe7d1, #d1f0ff);">
    <main class="container-fluid mt-2 px-5 py-4">

      <!-- CABECERA -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="fw-bold m-0 text-primary">
          <i class="bi bi-bar-chart-line-fill me-2"></i>
          {{ t.generalStats }}
        </h2>
      </div>

      <!-- FILTROS -->
      <div class="d-flex flex-wrap gap-3 mb-4 align-items-end">

        <!-- MES -->
        <div>
          <label class="form-label fw-semibold">{{ t.month }}</label>
          <input type="month" v-model="filtroMes" class="form-control">
        </div>

        <!-- ACTIVIDAD -->
        <div>
          <label class="form-label fw-semibold">{{ t.activity }}</label>
          <select v-model="actividadSeleccionada" class="form-select">
            <option value="">{{ t.all }}</option>
            <option v-for="act in actividades" :key="act.id" :value="act.id">
              {{ act.nombre }}
            </option>
          </select>
        </div>

        <!-- BOTONES -->
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
        <div class="col-md-4 col-xl-2" v-for="kpi in kpis" :key="kpi.title">
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

        <!-- INGRESOS -->
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

        <!-- INSCRIPCIONES POR ACTIVIDAD -->
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
import { type Ref, ref, onMounted, inject } from 'vue'

import { getEstadisticasAdministrador } from "@/services/administradorService"
import { getActividadesSimples } from '@/services/listadoService'

/* Importamos la funcion de uso y tambien los valores posibles de lenguaje */
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
let chartInscripciones: Chart | null = null

let chartReservas: any = null
let chartIngresos: any = null

const actividades = ref([])
const usoPabellones = ref([])
const ingresosPorTipo = ref({})

const kpis = ref([])

const resetFiltros = () => {
  filtroMes.value = new Date().toISOString().slice(0, 7)
  actividadSeleccionada.value = ""
  cargarDatos()
}

const renderCharts = (data: any) => {

  if (chartReservas) chartReservas.destroy()
  if (chartIngresos) chartIngresos.destroy()

  const labelsReservas = data.reservas_12_meses.map((r: any) => r.mes)
  const valoresReservas = data.reservas_12_meses.map((r: any) => r.total)

  chartReservas = new Chart(chartReservasRef.value, {
    type: 'line',
    data: {
      labels: labelsReservas,
      datasets: [{
        label: 'Reservas',
        data: valoresReservas,
        tension: 0.3,
        borderColor: '#2196F3',
        backgroundColor: 'rgba(33, 150, 243, 0.2)',
        fill: true
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: true },
        tooltip: { enabled: true }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  })

  const labelsIngresos = Object.keys(data.ingresos_detallados)
  const valoresIngresos = Object.values(data.ingresos_detallados)

  chartIngresos = new Chart(chartIngresosRef.value, {
    type: 'pie',
    data: {
      labels: labelsIngresos,
      datasets: [{
        data: valoresIngresos,
        backgroundColor: [
          '#4CAF50', // verde
          '#2196F3', // azul
          '#FFC107', // amarillo
          '#FF5722', // naranja
          '#9C27B0'  // morado
        ]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        tooltip: {
          callbacks: {
            label: (ctx: any) => {
              const label = ctx.label || '';
              const value = ctx.raw || 0;
              return `${label}: ${value} €`;
            }
          }
        },
        legend: {
          display: true,
          position: 'bottom'
        }
      }
    }
  });
}

const renderInscripciones = (inscripciones: any[]) => {
  if (chartInscripciones) chartInscripciones.destroy()

  const labels = inscripciones.map(i => i.actividad)
  const dataValues = inscripciones.map(i => i.inscritos)

  chartInscripciones = new Chart(chartInscripcionesRef.value!, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Inscritos',
        data: dataValues,
        backgroundColor: '#4CAF50'
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx: any) => `${ctx.raw} inscritos`
          }
        }
      },
      scales: {
        x: { beginAtZero: true }
      }
    }
  })
}

const cargarDatos = async () => {
  try {
    const [anio, mes] = filtroMes.value.split("-")

    const data = await getEstadisticasAdministrador(anio, mes, actividadSeleccionada.value)

    kpis.value = [
      { title: 'Usuarios', value: data.usuarios },
      { title: 'Monitores', value: data.monitores },
      { title: 'Sesiones', value: data.sesiones },
      { title: 'Inscripciones', value: data.inscripciones },
      { title: 'Alquileres', value: data.reservas_mes },
      { title: 'Ingresos', value: data.ingresos_mes + " €" }
    ]

    usoPabellones.value = data.uso_pabellones || []
    ingresosPorTipo.value = data.ingresos_detallados || {}

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